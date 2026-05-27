#!/usr/bin/env bash
# Domain Reconnaissance — theHarvester + subfinder + whois + DNS
# Usage: bash domain_recon.sh <domain> [output_dir]
# Output: JSON with subdomains, emails, DNS, whois, tech stack

set -euo pipefail
source "$(dirname "$0")/utils.sh"

DOMAIN="${1:?Usage: domain_recon.sh <domain> [output_dir]}"
OUTPUT_DIR="${2:-$(ensure_output_dir "domain_${DOMAIN}")}"
JSON_FILE="${OUTPUT_DIR}/data/domain_recon.json"

log_info "=== Domain Recon: ${DOMAIN} ==="
json_init "$DOMAIN" "$JSON_FILE"

# --- WHOIS ---
log_info "Running WHOIS..."
WHOIS_FILE="${OUTPUT_DIR}/data/whois_raw.txt"
if require_tool whois 2>/dev/null; then
    whois "$DOMAIN" > "$WHOIS_FILE" 2>/dev/null || true
    
    REGISTRAR=$(grep -i "registrar:" "$WHOIS_FILE" | head -1 | sed 's/.*Registrar:\s*//' || echo "unknown")
    CREATED=$(grep -i "creation date\|created:" "$WHOIS_FILE" | head -1 | sed 's/.*:\s*//' || echo "unknown")
    EXPIRES=$(grep -i "expir" "$WHOIS_FILE" | head -1 | sed 's/.*:\s*//' || echo "unknown")
    NAMESERVERS=$(grep -i "name server:" "$WHOIS_FILE" | sed 's/.*:\s*//' | jq -R -s 'split("\n") | map(select(length > 0))')
    
    json_merge "$JSON_FILE" "whois" "{
        \"registrar\": \"$REGISTRAR\",
        \"created\": \"$CREATED\",
        \"expires\": \"$EXPIRES\",
        \"nameservers\": $NAMESERVERS
    }"
    log_ok "WHOIS: registrar=${REGISTRAR}"
else
    log_warn "whois not installed"
    json_merge "$JSON_FILE" "whois" '{"status":"not_installed"}'
fi

# --- DNS Records ---
log_info "Querying DNS records..."
A_RECORDS=$(dig +short A "$DOMAIN" 2>/dev/null | jq -R -s 'split("\n") | map(select(length > 0))')
AAAA_RECORDS=$(dig +short AAAA "$DOMAIN" 2>/dev/null | jq -R -s 'split("\n") | map(select(length > 0))')
MX_RECORDS=$(dig +short MX "$DOMAIN" 2>/dev/null | jq -R -s 'split("\n") | map(select(length > 0))')
TXT_RECORDS=$(dig +short TXT "$DOMAIN" 2>/dev/null | jq -R -s 'split("\n") | map(select(length > 0))')
NS_RECORDS=$(dig +short NS "$DOMAIN" 2>/dev/null | jq -R -s 'split("\n") | map(select(length > 0))')
CNAME_RECORD=$(dig +short CNAME "$DOMAIN" 2>/dev/null | head -1 || echo "")

json_merge "$JSON_FILE" "dns" "{
    \"a\": $A_RECORDS,
    \"aaaa\": $AAAA_RECORDS,
    \"mx\": $MX_RECORDS,
    \"txt\": $TXT_RECORDS,
    \"ns\": $NS_RECORDS,
    \"cname\": \"$CNAME_RECORD\"
}"
log_ok "DNS: $(echo "$A_RECORDS" | jq 'length') A records"

# --- Subfinder (passive subdomain enumeration) ---
if require_tool subfinder 2>/dev/null; then
    log_info "Running Subfinder..."
    SUBFINDER_FILE="${OUTPUT_DIR}/data/subdomains.txt"
    
    subfinder -d "$DOMAIN" -silent -o "$SUBFINDER_FILE" 2>/dev/null || true
    
    if [[ -f "$SUBFINDER_FILE" ]]; then
        SUB_COUNT=$(wc -l < "$SUBFINDER_FILE" | tr -d ' ')
        SUBS_JSON=$(cat "$SUBFINDER_FILE" | jq -R -s 'split("\n") | map(select(length > 0))')
        
        json_merge "$JSON_FILE" "subfinder" "{
            \"tool\": \"subfinder\",
            \"subdomain_count\": $SUB_COUNT,
            \"subdomains\": $SUBS_JSON
        }"
        log_ok "Subfinder: ${SUB_COUNT} subdomains"
    fi
else
    log_warn "Subfinder not installed (requires Go)"
    json_merge "$JSON_FILE" "subfinder" '{"status":"not_installed"}'
fi

rate_limit 2

# --- theHarvester (emails, subdomains, names) ---
if require_tool theHarvester 2>/dev/null; then
    log_info "Running theHarvester..."
    HARVESTER_FILE="${OUTPUT_DIR}/data/theharvester.xml"
    
    # theHarvester -d domain -b all (all sources) -f output.xml
    theHarvester -d "$DOMAIN" -b all -f "$HARVESTER_FILE" 2>/dev/null || true
    
    # Parse emails from theHarvester output
    if [[ -f "$HARVESTER_FILE" ]]; then
        EMAILS=$(grep -oP '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}' "$HARVESTER_FILE" 2>/dev/null | sort -u | jq -R -s 'split("\n") | map(select(length > 0))')
        HOSTS=$(grep -oP '[a-zA-Z0-9.-]+\.'"$(echo "$DOMAIN" | sed 's/\./\\./g')"'"' "$HARVESTER_FILE" 2>/dev/null | sort -u | jq -R -s 'split("\n") | map(select(length > 0))')
        
        EMAIL_COUNT=$(echo "$EMAILS" | jq 'length')
        
        json_merge "$JSON_FILE" "theharvester" "{
            \"tool\": \"theHarvester\",
            \"emails_found\": $EMAIL_COUNT,
            \"emails\": $EMAILS,
            \"hosts\": $HOSTS
        }"
        log_ok "theHarvester: ${EMAIL_COUNT} emails found"
    else
        json_merge "$JSON_FILE" "theharvester" '{"tool":"theHarvester","status":"no_output"}'
    fi
else
    log_warn "theHarvester not installed"
    json_merge "$JSON_FILE" "theharvester" '{"status":"not_installed"}'
fi

# --- crt.sh (certificate transparency) ---
log_info "Checking certificate transparency (crt.sh)..."
CRT_FILE="${OUTPUT_DIR}/data/crtsh.json"

CRT_RESPONSE=$(curl -s "https://crt.sh/?q=%25.${DOMAIN}&output=json" 2>/dev/null || echo "[]")
echo "$CRT_RESPONSE" > "$CRT_FILE"

if [[ -s "$CRT_FILE" ]]; then
    CRT_SUBS=$(echo "$CRT_RESPONSE" | jq -r '.[].name_value' 2>/dev/null | sort -u | jq -R -s 'split("\n") | map(select(length > 0))')
    CRT_COUNT=$(echo "$CRT_SUBS" | jq 'length')
    
    json_merge "$JSON_FILE" "crtsh" "{
        \"tool\": \"crt.sh\",
        \"unique_subdomains\": $CRT_COUNT,
        \"subdomains\": $CRT_SUBS
    }"
    log_ok "crt.sh: ${CRT_COUNT} unique subdomains from certificates"
fi

# --- Summary ---
SUBFINDER_COUNT=$(jq '.results.subfinder.subdomain_count // 0' "$JSON_FILE")
CRT_COUNT=$(jq '.results.crtsh.unique_subdomains // 0' "$JSON_FILE")
EMAIL_COUNT=$(jq '.results.theharvester.emails_found // 0' "$JSON_FILE")

log_info "=== Domain Recon Summary ==="
log_info "  Subfinder:    ${SUBFINDER_COUNT} subdomains"
log_info "  crt.sh:       ${CRT_COUNT} subdomains"
log_info "  theHarvester: ${EMAIL_COUNT} emails"
log_info "  Results:      ${JSON_FILE}"
