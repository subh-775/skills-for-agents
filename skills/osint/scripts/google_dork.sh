#!/usr/bin/env bash
# Google Dorking — Automated search queries for exposed data
# Usage: bash google_dork.sh <domain> [output_dir]
# Output: JSON with categorized dork results

set -euo pipefail
source "$(dirname "$0")/utils.sh"

DOMAIN="${1:?Usage: google_dork.sh <domain> [output_dir]}"
OUTPUT_DIR="${2:-$(ensure_output_dir "dork_${DOMAIN}")}"
JSON_FILE="${OUTPUT_DIR}/data/google_dorks.json"

log_info "=== Google Dorking: ${DOMAIN} ==="
json_init "$DOMAIN" "$JSON_FILE"

# --- Define dork categories ---
declare -A DORKS=(
    # Exposed files
    ["pdf_files"]="site:${DOMAIN} filetype:pdf"
    ["excel_files"]="site:${DOMAIN} filetype:xlsx OR filetype:csv"
    ["word_files"]="site:${DOMAIN} filetype:docx OR filetype:doc"
    ["presentations"]="site:${DOMAIN} filetype:pptx OR filetype:ppt"
    
    # Sensitive directories
    ["open_directories"]="site:${DOMAIN} intitle:\"index of\""
    ["git_repos"]="site:${DOMAIN} intitle:\"index of\" .git"
    ["env_files"]="site:${DOMAIN} filetype:env"
    ["config_files"]="site:${DOMAIN} filetype:xml OR filetype:conf OR filetype:cfg"
    ["log_files"]="site:${DOMAIN} filetype:log"
    ["backup_files"]="site:${DOMAIN} filetype:bak OR filetype:sql OR filetype:dump"
    
    # Login pages
    ["admin_panels"]="site:${DOMAIN} inurl:admin OR inurl:login OR inurl:portal"
    ["cpanel"]="site:${DOMAIN} intitle:\"cPanel Login\""
    ["phpmyadmin"]="site:${DOMAIN} inurl:phpmyadmin"
    
    # Exposed info
    ["emails"]="site:${DOMAIN} \"@${DOMAIN}\""
    ["phone_numbers"]="site:${DOMAIN} \"phone\" OR \"tel\" OR \"contact\""
    ["error_pages"]="site:${DOMAIN} intitle:\"error\" OR intitle:\"404\" OR intitle:\"500\""
    
    # Social media
    ["linkedin"]="site:linkedin.com/in \"${DOMAIN}\""
    ["github"]="site:github.com \"${DOMAIN}\""
    ["twitter"]="site:twitter.com \"${DOMAIN}\""
    
    # Credentials/keys (GitHub)
    ["github_secrets"]="site:github.com \"${DOMAIN}\" \"api_key\" OR \"password\" OR \"secret\" OR \"token\""
    ["github_env"]="site:github.com \"${DOMAIN}\" filetype:env"
    ["pastebin"]="site:pastebin.com \"${DOMAIN}\""
)

# --- Execute dorks (via Google Custom Search API or curl) ---
log_info "Generating dork queries..."

DORK_RESULTS="{}"
DORK_COUNT=0

for category in "${!DORKS[@]}"; do
    query="${DORKS[$category]}"
    DORK_COUNT=$((DORK_COUNT + 1))
    
    # Store the query — actual execution depends on API availability
    DORK_RESULTS=$(echo "$DORK_RESULTS" | jq --arg cat "$category" --arg q "$query" \
        '. + {($cat): {"query": $q, "status": "generated"}}')
done

# Save all dork queries
json_merge "$JSON_FILE" "dork_queries" "$DORK_RESULTS"
json_merge "$JSON_FILE" "summary" "{
    \"total_dorks\": $DORK_COUNT,
    \"domain\": \"$DOMAIN\",
    \"note\": \"Execute these queries manually or via Google Custom Search API (requires API key)\"
}"

# --- If Google Custom Search API key is available ---
if [[ -n "${GOOGLE_API_KEY:-}" && -n "${GOOGLE_CSE_ID:-}" ]]; then
    log_info "Executing dorks via Google Custom Search API..."
    
    EXECUTED=0
    for category in "${!DORKS[@]}"; do
        query="${DORKS[$category]}"
        
        RESULT=$(curl -s "https://www.googleapis.com/customsearch/v1?key=${GOOGLE_API_KEY}&cx=${GOOGLE_CSE_ID}&q=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$query'))")&num=5" 2>/dev/null)
        
        if [[ -n "$RESULT" ]]; then
            ITEMS=$(echo "$RESULT" | jq '[.items[]? | {title: .title, url: .link, snippet: .snippet}]' 2>/dev/null || echo "[]")
            COUNT=$(echo "$ITEMS" | jq 'length')
            
            if [[ "$COUNT" -gt 0 ]]; then
                DORK_RESULTS=$(echo "$DORK_RESULTS" | jq --arg cat "$category" --argjson items "$ITEMS" \
                    '.[$cat].results = $items | .[$cat].status = "executed" | .[$cat].count = ($items | length)')
                EXECUTED=$((EXECUTED + 1))
            fi
        fi
        
        rate_limit 1  # Respect API rate limits
    done
    
    json_merge "$JSON_FILE" "dork_queries" "$DORK_RESULTS"
    log_ok "Executed ${EXECUTED} dorks with results"
else
    log_warn "GOOGLE_API_KEY / GOOGLE_CSE_ID not set"
    log_info "Dork queries saved — execute manually in browser or set API keys"
fi

log_info "=== Google Dorking Summary ==="
log_info "  Total dorks: ${DORK_COUNT}"
log_info "  Results:     ${JSON_FILE}"
