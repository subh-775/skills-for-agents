#!/usr/bin/env bash
# Username Enumeration — Sherlock + Maigret
# Usage: bash username_enum.sh <username> [output_dir]
# Output: JSON results + summary

set -euo pipefail
source "$(dirname "$0")/utils.sh"

USERNAME="${1:?Usage: username_enum.sh <username> [output_dir]}"
OUTPUT_DIR="${2:-$(ensure_output_dir "username_${USERNAME}")}"
JSON_FILE="${OUTPUT_DIR}/data/username_enum.json"

log_info "=== Username Enumeration: ${USERNAME} ==="
json_init "$USERNAME" "$JSON_FILE"

# --- Sherlock (400+ sites) ---
SHERLOCK_RESULTS=""
if require_tool sherlock 2>/dev/null; then
    log_info "Running Sherlock..."
    SHERLOCK_FILE="${OUTPUT_DIR}/data/sherlock_raw.txt"
    
    # Sherlock outputs one URL per line for found accounts
    sherlock "$USERNAME" --print-found --timeout 10 --output "$SHERLOCK_FILE" 2>/dev/null || true
    
    if [[ -f "$SHERLOCK_FILE" ]]; then
        SHERLOCK_COUNT=$(wc -l < "$SHERLOCK_FILE" | tr -d ' ')
        SHERLOCK_SITES=$(cat "$SHERLOCK_FILE" | grep -oP 'https?://[^\s]+' | head -50)
        
        # Build JSON array
        SHERLOCK_JSON=$(echo "$SHERLOCK_SITES" | jq -R -s 'split("\n") | map(select(length > 0)) | map({"url": .})')
        
        json_merge "$JSON_FILE" "sherlock" "{
            \"tool\": \"sherlock\",
            \"sites_found\": $SHERLOCK_COUNT,
            \"results\": $SHERLOCK_JSON
        }"
        log_ok "Sherlock: found ${SHERLOCK_COUNT} sites"
    else
        log_warn "Sherlock: no results file generated"
        json_merge "$JSON_FILE" "sherlock" '{"tool":"sherlock","sites_found":0,"results":[]}'
    fi
else
    log_warn "Sherlock not installed — skipping"
    json_merge "$JSON_FILE" "sherlock" '{"tool":"sherlock","status":"not_installed"}'
fi

rate_limit 2

# --- Maigret (3000+ sites, with profile extraction) ---
if require_tool maigret 2>/dev/null; then
    log_info "Running Maigret..."
    MAIGRET_FILE="${OUTPUT_DIR}/data/maigret_results.txt"
    MAIGRET_JSON="${OUTPUT_DIR}/data/maigret_${USERNAME}.json"
    
    # Maigret can output JSON
    maigret "$USERNAME" --timeout 10 --print-not-found --json-simple "$MAIGRET_JSON" 2>/dev/null || true
    
    # Also get text output
    maigret "$USERNAME" --timeout 10 --print-not-found -o "$MAIGRET_FILE" 2>/dev/null || true
    
    if [[ -f "$MAIGRET_JSON" && -s "$MAIGRET_JSON" ]]; then
        MAIGRET_COUNT=$(jq 'length' "$MAIGRET_JSON" 2>/dev/null || echo "0")
        json_merge "$JSON_FILE" "maigret" "{
            \"tool\": \"maigret\",
            \"sites_found\": $MAIGRET_COUNT,
            \"results_file\": \"$(basename "$MAIGRET_JSON")\"
        }"
        log_ok "Maigret: found ${MAIGRET_COUNT} sites"
    elif [[ -f "$MAIGRET_FILE" ]]; then
        MAIGRET_COUNT=$(grep -c "^\[" "$MAIGRET_FILE" 2>/dev/null || echo "0")
        json_merge "$JSON_FILE" "maigret" "{
            \"tool\": \"maigret\",
            \"sites_found\": $MAIGRET_COUNT,
            \"results_file\": \"$(basename "$MAIGRET_FILE")\"
        }"
        log_ok "Maigret: found ${MAIGRET_COUNT} sites"
    else
        log_warn "Maigret: no results"
        json_merge "$JSON_FILE" "maigret" '{"tool":"maigret","sites_found":0,"results":[]}'
    fi
else
    log_warn "Maigret not installed — skipping"
    json_merge "$JSON_FILE" "maigret" '{"tool":"maigret","status":"not_installed"}'
fi

# --- Summary ---
TOTAL_SHERLOCK=$(jq '.results.sherlock.sites_found // 0' "$JSON_FILE")
TOTAL_MAIGRET=$(jq '.results.maigret.sites_found // 0' "$JSON_FILE")

log_info "=== Username Enum Summary ==="
log_info "  Sherlock: ${TOTAL_SHERLOCK} sites"
log_info "  Maigret:  ${TOTAL_MAIGRET} sites"
log_info "  Results:  ${JSON_FILE}"
log_info "  Output:   ${OUTPUT_DIR}/"
