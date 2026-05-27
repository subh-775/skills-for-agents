#!/usr/bin/env bash
# OSINT Orchestrator — Master script that chains all OSINT tools
# Usage: bash osint_orchestrator.sh <target> <type> [output_dir]
# Types: email, phone, username, domain, ip, file, person
# Output: Comprehensive JSON report + summary

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "${SCRIPT_DIR}/utils.sh"

TARGET="${1:?Usage: osint_orchestrator.sh <target> <type> [output_dir]}"
TYPE="${2:?Type: email|phone|username|domain|ip|file|person}"
OUTPUT_DIR="${3:-$(ensure_output_dir "osint_${TARGET//[^a-zA-Z0-9]/_}")}"

log_info "╔══════════════════════════════════════════╗"
log_info "║        OSINT ORCHESTRATOR                ║"
log_info "╚══════════════════════════════════════════╝"
log_info "Target: ${TARGET}"
log_info "Type:   ${TYPE}"
log_info "Output: ${OUTPUT_DIR}"
log_info ""

MASTER_JSON="${OUTPUT_DIR}/data/master_report.json"
json_init "$TARGET" "$MASTER_JSON"
jq --arg t "$TYPE" '.target_type = $t' "$MASTER_JSON" > "${MASTER_JSON}.tmp" && mv "${MASTER_JSON}.tmp" "$MASTER_JSON"

START_TIME=$(date +%s)

case "$TYPE" in
    email)
        log_info ">>> Phase 1: Email OSINT"
        bash "${SCRIPT_DIR}/email_osint.sh" "$TARGET" "$OUTPUT_DIR" 2>&1 || true
        
        log_info ">>> Phase 2: Username from email"
        USERNAME="${TARGET%%@*}"
        bash "${SCRIPT_DIR}/username_enum.sh" "$USERNAME" "$OUTPUT_DIR" 2>&1 || true
        
        log_info ">>> Phase 3: Domain recon on email domain"
        DOMAIN="${TARGET#*@}"
        bash "${SCRIPT_DIR}/domain_recon.sh" "$DOMAIN" "$OUTPUT_DIR" 2>&1 || true
        
        log_info ">>> Phase 4: Breach check"
        bash "${SCRIPT_DIR}/breach_check.sh" "$TARGET" "$OUTPUT_DIR" 2>&1 || true
        ;;
    
    phone)
        log_info ">>> Phase 1: Phone OSINT"
        bash "${SCRIPT_DIR}/phone_osint.sh" "$TARGET" "$OUTPUT_DIR" 2>&1 || true
        
        log_info ">>> Phase 2: Username from phone"
        CLEAN_PHONE="${TARGET//[^0-9]/}"
        bash "${SCRIPT_DIR}/username_enum.sh" "$CLEAN_PHONE" "$OUTPUT_DIR" 2>&1 || true
        ;;
    
    username)
        log_info ">>> Phase 1: Username enumeration"
        bash "${SCRIPT_DIR}/username_enum.sh" "$TARGET" "$OUTPUT_DIR" 2>&1 || true
        
        log_info ">>> Phase 2: Social media profiles"
        bash "${SCRIPT_DIR}/social_media.sh" "$TARGET" "username" "$OUTPUT_DIR" 2>&1 || true
        
        log_info ">>> Phase 3: Breach check on username"
        bash "${SCRIPT_DIR}/breach_check.sh" "$TARGET" "$OUTPUT_DIR" 2>&1 || true
        ;;
    
    domain)
        log_info ">>> Phase 1: Domain reconnaissance"
        bash "${SCRIPT_DIR}/domain_recon.sh" "$TARGET" "$OUTPUT_DIR" 2>&1 || true
        
        log_info ">>> Phase 2: Google dorking"
        bash "${SCRIPT_DIR}/google_dork.sh" "$TARGET" "$OUTPUT_DIR" 2>&1 || true
        
        log_info ">>> Phase 3: Social media search"
        bash "${SCRIPT_DIR}/social_media.sh" "$TARGET" "url" "$OUTPUT_DIR" 2>&1 || true
        ;;
    
    ip)
        log_info ">>> Phase 1: IP reconnaissance"
        bash "${SCRIPT_DIR}/ip_recon.sh" "$TARGET" "$OUTPUT_DIR" 2>&1 || true
        
        log_info ">>> Phase 2: Reverse DNS → domain recon"
        RDNS=$(dig +short -x "$TARGET" 2>/dev/null | sed 's/\.$//' || echo "")
        if [[ -n "$RDNS" && "$RDNS" != *"NXDOMAIN"* ]]; then
            DOMAIN_FROM_RDNS=$(echo "$RDNS" | awk -F. '{print $(NF-1)"."$NF}')
            log_info "  Found domain: ${DOMAIN_FROM_RDNS} — running domain recon"
            bash "${SCRIPT_DIR}/domain_recon.sh" "$DOMAIN_FROM_RDNS" "$OUTPUT_DIR" 2>&1 || true
        fi
        ;;
    
    file)
        log_info ">>> Phase 1: Metadata extraction"
        bash "${SCRIPT_DIR}/metadata_extract.sh" "$TARGET" "$OUTPUT_DIR" 2>&1 || true
        
        log_info ">>> Phase 2: File hash check (VirusTotal if key available)"
        if [[ -f "$TARGET" ]]; then
            SHA256=$(sha256sum "$TARGET" 2>/dev/null | awk '{print $1}')
            if [[ -n "${VT_API_KEY:-}" ]]; then
                VT_RESULT=$(curl -s -H "x-apikey: ${VT_API_KEY}" "https://www.virustotal.com/api/v3/files/${SHA256}" 2>/dev/null)
                VT_MALICIOUS=$(echo "$VT_RESULT" | jq -r '.data.attributes.last_analysis_stats.malicious // 0' 2>/dev/null)
                VT_SUSPICIOUS=$(echo "$VT_RESULT" | jq -r '.data.attributes.last_analysis_stats.suspicious // 0' 2>/dev/null)
                
                jq --arg sha "$SHA256" --argjson mal "$VT_MALICIOUS" --argjson sus "$VT_SUSPICIOUS" \
                    '.results.virustotal = {sha256: $sha, malicious: $mal, suspicious: $sus}' \
                    "$MASTER_JSON" > "${MASTER_JSON}.tmp" && mv "${MASTER_JSON}.tmp" "$MASTER_JSON"
                log_ok "VirusTotal: ${VT_MALICIOUS} malicious, ${VT_SUSPICIOUS} suspicious"
            else
                log_warn "VT_API_KEY not set — skipping VirusTotal"
            fi
        fi
        ;;
    
    person)
        log_info ">>> Phase 1: Username enumeration"
        bash "${SCRIPT_DIR}/username_enum.sh" "$TARGET" "$OUTPUT_DIR" 2>&1 || true
        
        log_info ">>> Phase 2: Social media deep dive"
        bash "${SCRIPT_DIR}/social_media.sh" "$TARGET" "username" "$OUTPUT_DIR" 2>&1 || true
        
        log_info ">>> Phase 3: Email check (if email format)"
        if [[ "$TARGET" == *"@"* ]]; then
            bash "${SCRIPT_DIR}/email_osint.sh" "$TARGET" "$OUTPUT_DIR" 2>&1 || true
            bash "${SCRIPT_DIR}/breach_check.sh" "$TARGET" "$OUTPUT_DIR" 2>&1 || true
        fi
        ;;
    
    *)
        log_error "Unknown type: ${TYPE}"
        log_info "Valid types: email, phone, username, domain, ip, file, person"
        exit 1
        ;;
esac

# --- Merge all sub-reports into master ---
log_info ""
log_info ">>> Merging results..."

for json_file in "${OUTPUT_DIR}/data/"*.json; do
    [[ -f "$json_file" ]] || continue
    [[ "$json_file" == "$MASTER_JSON" ]] && continue
    
    TOOL_NAME=$(basename "$json_file" .json)
    TOOL_DATA=$(cat "$json_file")
    
    jq --arg name "$TOOL_NAME" --argjson data "$TOOL_DATA" \
        '.results[$name] = $data' "$MASTER_JSON" > "${MASTER_JSON}.tmp" && mv "${MASTER_JSON}.tmp" "$MASTER_JSON"
done

# --- Final summary ---
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

TOOLS_RUN=$(jq '.results | keys | length' "$MASTER_JSON")
log_info ""
log_info "╔══════════════════════════════════════════╗"
log_info "║        OSINT COMPLETE                    ║"
log_info "╚══════════════════════════════════════════╝"
log_info "Target:   ${TARGET}"
log_info "Type:     ${TYPE}"
log_info "Tools:    ${TOOLS_RUN} run"
log_info "Duration: ${DURATION}s"
log_info "Report:   ${MASTER_JSON}"
log_info "Output:   ${OUTPUT_DIR}/"
log_info ""
log_info "Next steps:"
log_info "  1. Review ${MASTER_JSON} for structured data"
log_info "  2. Generate HTML report from JSON"
log_info "  3. Cross-reference findings across tools"
