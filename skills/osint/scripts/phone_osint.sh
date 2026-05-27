#!/usr/bin/env bash
# Phone OSINT — PhoneInfoga + carrier lookup + validation
# Usage: bash phone_osint.sh <phone_number> [output_dir]
# Output: JSON results with carrier, location, validity

set -euo pipefail
source "$(dirname "$0")/utils.sh"

PHONE="${1:?Usage: phone_osint.sh <phone_number> [output_dir]}"
OUTPUT_DIR="${2:-$(ensure_output_dir "phone_${PHONE//[^0-9]/}")}"
JSON_FILE="${OUTPUT_DIR}/data/phone_osint.json"

log_info "=== Phone OSINT: ${PHONE} ==="
json_init "$PHONE" "$JSON_FILE"

# --- PhoneInfoga ---
if require_tool phoneinfoga 2>/dev/null; then
    log_info "Running PhoneInfoga..."
    INFOGA_FILE="${OUTPUT_DIR}/data/phoneinfoga.json"
    
    phoneinfoga scan -n "$PHONE" --json > "$INFOGA_FILE" 2>/dev/null || true
    
    if [[ -f "$INFOGA_FILE" && -s "$INFOGA_FILE" ]]; then
        CARRIER=$(jq -r '.carrier // "unknown"' "$INFOGA_FILE" 2>/dev/null)
        COUNTRY=$(jq -r '.country // "unknown"' "$INFOGA_FILE" 2>/dev/null)
        LINE_TYPE=$(jq -r '.line_type // "unknown"' "$INFOGA_FILE" 2>/dev/null)
        
        json_merge "$JSON_FILE" "phoneinfoga" "{
            \"tool\": \"phoneinfoga\",
            \"carrier\": \"$CARRIER\",
            \"country\": \"$COUNTRY\",
            \"line_type\": \"$LINE_TYPE\",
            \"raw\": $(cat "$INFOGA_FILE")
        }"
        log_ok "PhoneInfoga: carrier=${CARRIER}, country=${COUNTRY}"
    else
        log_warn "PhoneInfoga: no results"
        json_merge "$JSON_FILE" "phoneinfoga" '{"tool":"phoneinfoga","status":"no_results"}'
    fi
else
    log_warn "PhoneInfoga not installed"
    log_info "Install: https://github.com/sundowndev/phoneinfoga/releases"
    json_merge "$JSON_FILE" "phoneinfoga" '{"tool":"phoneinfoga","status":"not_installed"}'
fi

rate_limit 2

# --- NumVerify (free API, 100 req/month) ---
if [[ -n "${NUMVERIFY_API_KEY:-}" ]]; then
    log_info "Running NumVerify lookup..."
    NUMVERIFY_FILE="${OUTPUT_DIR}/data/numverify.json"
    
    curl -s "http://apilayer.net/api/validate?access_key=${NUMVERIFY_API_KEY}&number=${PHONE}&country_code=&format=1" \
        > "$NUMVERIFY_FILE" 2>/dev/null || true
    
    if [[ -f "$NUMVERIFY_FILE" && -s "$NUMVERIFY_FILE" ]]; then
        VALID=$(jq -r '.valid // false' "$NUMVERIFY_FILE" 2>/dev/null)
        LOCAL=$(jq -r '.local_format // "unknown"' "$NUMVERIFY_FILE" 2>/dev/null)
        INTL=$(jq -r '.international_format // "unknown"' "$NUMVERIFY_FILE" 2>/dev/null)
        CARRIER_NV=$(jq -r '.carrier // "unknown"' "$NUMVERIFY_FILE" 2>/dev/null)
        LOC=$(jq -r '.location // "unknown"' "$NUMVERIFY_FILE" 2>/dev/null)
        
        json_merge "$JSON_FILE" "numverify" "{
            \"tool\": \"numverify\",
            \"valid\": $VALID,
            \"local_format\": \"$LOCAL\",
            \"international_format\": \"$INTL\",
            \"carrier\": \"$CARRIER_NV\",
            \"location\": \"$LOC\"
        }"
        log_ok "NumVerify: valid=${VALID}, location=${LOC}"
    fi
else
    log_warn "NUMVERIFY_API_KEY not set — skipping"
    json_merge "$JSON_FILE" "numverify" '{"tool":"numverify","status":"api_key_missing"}'
fi

# --- Basic validation ---
log_info "Running basic number analysis..."
# Extract country code and number type from format
CLEAN_PHONE="${PHONE//[^0-9+]/}"
json_merge "$JSON_FILE" "basic_analysis" "{
    \"input\": \"$PHONE\",
    \"cleaned\": \"$CLEAN_PHONE\",
    \"length\": ${#CLEAN_PHONE},
    \"starts_with_plus\": $([ "${PHONE:0:1}" = "+" ] && echo true || echo false)
}"

log_info "=== Phone OSINT Summary ==="
log_info "  Results: ${JSON_FILE}"
