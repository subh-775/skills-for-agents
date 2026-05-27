#!/usr/bin/env bash
# Email OSINT — Holehe + HIBP + h8mail
# Usage: bash email_osint.sh <email> [output_dir]
# Output: JSON results + breach data

set -euo pipefail
source "$(dirname "$0")/utils.sh"

EMAIL="${1:?Usage: email_osint.sh <email> [output_dir]}"
OUTPUT_DIR="${2:-$(ensure_output_dir "email_${EMAIL%%@*}")}"
JSON_FILE="${OUTPUT_DIR}/data/email_osint.json"

log_info "=== Email OSINT: ${EMAIL} ==="
json_init "$EMAIL" "$JSON_FILE"

# --- Holehe (email → 120+ platforms) ---
if require_tool holehe 2>/dev/null; then
    log_info "Running Holehe..."
    HOLEHE_FILE="${OUTPUT_DIR}/data/holehe_results.txt"
    
    # Holehe outputs platform:yes/no
    holehe "$EMAIL" 2>/dev/null | tee "$HOLEHE_FILE" || true
    
    if [[ -f "$HOLEHE_FILE" ]]; then
        # Count registered platforms
        REGISTERED=$(grep -c "\[+\]" "$HOLEHE_FILE" 2>/dev/null || echo "0")
        
        # Extract platform names
        PLATFORMS=$(grep "\[+\]" "$HOLEHE_FILE" | sed 's/.*\[+\] //' | jq -R -s 'split("\n") | map(select(length > 0))')
        
        json_merge "$JSON_FILE" "holehe" "{
            \"tool\": \"holehe\",
            \"platforms_registered\": $REGISTERED,
            \"platforms\": $PLATFORMS
        }"
        log_ok "Holehe: ${REGISTERED} platforms registered"
    fi
else
    log_warn "Holehe not installed — skipping"
    json_merge "$JSON_FILE" "holehe" '{"tool":"holehe","status":"not_installed"}'
fi

rate_limit 3

# --- HIBP (Have I Been Pwned) ---
log_info "Checking HIBP (Have I Been Pwned)..."
HIBP_FILE="${OUTPUT_DIR}/data/hibp_breaches.json"

# HIBP v3 API — requires API key for account search
# Fallback: check password range (no key needed)
if [[ -n "${HIBP_API_KEY:-}" ]]; then
    HIBP_RESPONSE=$(curl -s -H "hibp-api-key: ${HIBP_API_KEY}" \
        -H "user-agent: osint-skill" \
        "https://haveibeenpwned.com/api/v3/breachedaccount/${EMAIL}?truncateResponse=false" 2>/dev/null || echo "[]")
    
    echo "$HIBP_RESPONSE" > "$HIBP_FILE"
    BREACH_COUNT=$(echo "$HIBP_RESPONSE" | jq 'length' 2>/dev/null || echo "0")
    
    json_merge "$JSON_FILE" "hibp" "{
        \"tool\": \"hibp\",
        \"breaches_found\": $BREACH_COUNT,
        \"breaches\": $HIBP_RESPONSE
    }"
    log_ok "HIBP: ${BREACH_COUNT} breaches found"
else
    log_warn "HIBP_API_KEY not set — skipping account search"
    log_info "Set HIBP_API_KEY env var for breach checking"
    json_merge "$JSON_FILE" "hibp" '{"tool":"hibp","status":"api_key_missing","note":"Set HIBP_API_KEY env var"}'
fi

rate_limit 2

# --- h8mail (breach checker, no API key needed for basic) ---
if require_tool h8mail 2>/dev/null; then
    log_info "Running h8mail..."
    H8MAIL_FILE="${OUTPUT_DIR}/data/h8mail_results.txt"
    
    h8mail -t "$EMAIL" -o "$H8MAIL_FILE" 2>/dev/null || true
    
    if [[ -f "$H8MAIL_FILE" ]]; then
        H8_BREACHES=$(grep -c "breach\|pwn\|leak" "$H8MAIL_FILE" 2>/dev/null || echo "0")
        json_merge "$JSON_FILE" "h8mail" "{
            \"tool\": \"h8mail\",
            \"findings\": $H8_BREACHES,
            \"results_file\": \"$(basename "$H8MAIL_FILE")\"
        }"
        log_ok "h8mail: ${H8_BREACHES} findings"
    fi
else
    log_warn "h8mail not installed — skipping"
    json_merge "$JSON_FILE" "h8mail" '{"tool":"h8mail","status":"not_installed"}'
fi

# --- Email domain analysis ---
DOMAIN="${EMAIL#*@}"
log_info "Analyzing email domain: ${DOMAIN}"

# MX records
MX_RECORDS=$(dig +short MX "$DOMAIN" 2>/dev/null | jq -R -s 'split("\n") | map(select(length > 0))')
# SPF record
SPF=$(dig +short TXT "$DOMAIN" 2>/dev/null | grep -i spf | head -1 || echo "none")
# DMARC
DMARC=$(dig +short TXT "_dmarc.${DOMAIN}" 2>/dev/null | head -1 || echo "none")

json_merge "$JSON_FILE" "domain_analysis" "{
    \"domain\": \"$DOMAIN\",
    \"mx_records\": $MX_RECORDS,
    \"spf\": \"$SPF\",
    \"dmarc\": \"$DMARC\"
}"

log_info "=== Email OSINT Summary ==="
log_info "  Results: ${JSON_FILE}"
log_info "  Output:  ${OUTPUT_DIR}/"
