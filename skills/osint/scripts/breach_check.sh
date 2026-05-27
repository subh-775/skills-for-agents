#!/usr/bin/env bash
# Breach & Leak Check — HIBP + DeHashed + credential databases
# Usage: bash breach_check.sh <email_or_username> [output_dir]
# Output: JSON with breach data, exposed credentials, paste hits

set -euo pipefail
source "$(dirname "$0")/utils.sh"

TARGET="${1:?Usage: breach_check.sh <email_or_username> [output_dir]}"
OUTPUT_DIR="${2:-$(ensure_output_dir "breach_${TARGET%%@*}")}"
JSON_FILE="${OUTPUT_DIR}/data/breach_check.json"

log_info "=== Breach & Leak Check: ${TARGET} ==="
json_init "$TARGET" "$JSON_FILE"

# Determine if target is email or username
if [[ "$TARGET" == *"@"* ]]; then
    TARGET_TYPE="email"
else
    TARGET_TYPE="username"
fi

json_merge "$JSON_FILE" "target_info" "{\"value\": \"$TARGET\", \"type\": \"$TARGET_TYPE\"}"

# --- HIBP Breaches ---
if [[ "$TARGET_TYPE" == "email" ]]; then
    log_info "Checking HIBP breaches..."
    
    if [[ -n "${HIBP_API_KEY:-}" ]]; then
        # Breach check
        BREACHES=$(curl -s -H "hibp-api-key: ${HIBP_API_KEY}" \
            -H "user-agent: osint-skill" \
            "https://haveibeenpwned.com/api/v3/breachedaccount/${TARGET}?truncateResponse=false" 2>/dev/null || echo "[]")
        
        BREACH_COUNT=$(echo "$BREACHES" | jq 'length' 2>/dev/null || echo "0")
        
        # Paste check
        PASTES=$(curl -s -H "hibp-api-key: ${HIBP_API_KEY}" \
            -H "user-agent: osint-skill" \
            "https://haveibeenpwned.com/api/v3/pasteaccount/${TARGET}" 2>/dev/null || echo "[]")
        
        PASTE_COUNT=$(echo "$PASTES" | jq 'length' 2>/dev/null || echo "0")
        
        json_merge "$JSON_FILE" "hibp" "{
            \"tool\": \"hibp\",
            \"breaches\": $BREACHES,
            \"breach_count\": $BREACH_COUNT,
            \"pastes\": $PASTES,
            \"paste_count\": $PASTE_COUNT
        }"
        log_ok "HIBP: ${BREACH_COUNT} breaches, ${PASTE_COUNT} pastes"
        
        rate_limit 3
    else
        log_warn "HIBP_API_KEY not set"
        json_merge "$JSON_FILE" "hibp" '{"tool":"hibp","status":"api_key_missing"}'
    fi
fi

# --- h8mail ---
if require_tool h8mail 2>/dev/null; then
    log_info "Running h8mail..."
    H8MAIL_FILE="${OUTPUT_DIR}/data/h8mail_breach.txt"
    
    h8mail -t "$TARGET" -o "$H8MAIL_FILE" 2>/dev/null || true
    
    if [[ -f "$H8MAIL_FILE" ]]; then
        H8_FINDINGS=$(wc -l < "$H8MAIL_FILE" | tr -d ' ')
        json_merge "$JSON_FILE" "h8mail" "{
            \"tool\": \"h8mail\",
            \"findings\": $H8_FINDINGS,
            \"results_file\": \"$(basename "$H8MAIL_FILE")\"
        }"
        log_ok "h8mail: ${H8_FINDINGS} findings"
    fi
else
    log_warn "h8mail not installed"
    json_merge "$JSON_FILE" "h8mail" '{"tool":"h8mail","status":"not_installed"}'
fi

# --- IntelX (if API key available) ---
if [[ -n "${INTELX_API_KEY:-}" ]]; then
    log_info "Checking IntelX..."
    
    # IntelX intelligence search
    INTELX_RESULT=$(curl -s -H "x-key: ${INTELX_API_KEY}" \
        -H "Content-Type: application/json" \
        -d "{\"term\":\"${TARGET}\",\"maxresults\":20,\"media\":0,\"target\":0,\"terminate\":[]}" \
        "https://2.intelx.io/intelligent/search" 2>/dev/null)
    
    if [[ -n "$INTELX_RESULT" ]]; then
        INTELX_ID=$(echo "$INTELX_RESULT" | jq -r '.id // empty')
        
        if [[ -n "$INTELX_ID" ]]; then
            sleep 5  # Wait for results to compile
            INTELX_RECORDS=$(curl -s -H "x-key: ${INTELX_API_KEY}" \
                "https://2.intelx.io/intelligent/search/result?id=${INTELX_ID}&limit=20" 2>/dev/null)
            
            RECORDS_COUNT=$(echo "$INTELX_RECORDS" | jq '.records | length' 2>/dev/null || echo "0")
            
            json_merge "$JSON_FILE" "intelx" "{
                \"tool\": \"intelx\",
                \"records_found\": $RECORDS_COUNT,
                \"search_id\": \"$INTELX_ID\"
            }"
            log_ok "IntelX: ${RECORDS_COUNT} records"
        fi
    fi
else
    json_merge "$JSON_FILE" "intelx" '{"tool":"intelx","status":"api_key_missing"}'
fi

# --- Summary ---
TOTAL_BREACHES=$(jq '.results.hibp.breach_count // 0' "$JSON_FILE")
TOTAL_PASTES=$(jq '.results.hibp.paste_count // 0' "$JSON_FILE")

log_info "=== Breach Check Summary ==="
log_info "  Breaches: ${TOTAL_BREACHES}"
log_info "  Pastes:   ${TOTAL_PASTES}"
log_info "  Results:  ${JSON_FILE}"
