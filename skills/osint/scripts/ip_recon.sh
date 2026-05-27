#!/usr/bin/env bash
# IP Reconnaissance — Shodan + ipinfo + nmap + reverse DNS
# Usage: bash ip_recon.sh <ip_address> [output_dir]
# Output: JSON with geolocation, open ports, services, org

set -euo pipefail
source "$(dirname "$0")/utils.sh"

IP="${1:?Usage: ip_recon.sh <ip> [output_dir]}"
OUTPUT_DIR="${2:-$(ensure_output_dir "ip_${IP//\./_}")}"
JSON_FILE="${OUTPUT_DIR}/data/ip_recon.json"

log_info "=== IP Recon: ${IP} ==="
json_init "$IP" "$JSON_FILE"

# --- Reverse DNS ---
log_info "Reverse DNS lookup..."
RDNS=$(dig +short -x "$IP" 2>/dev/null || echo "unknown")
json_merge "$JSON_FILE" "reverse_dns" "{\"ptr\": \"$RDNS\"}"
log_ok "rDNS: ${RDNS}"

# --- ipinfo.io (free, 50k req/month) ---
log_info "Querying ipinfo.io..."
if [[ -n "${IPINFO_TOKEN:-}" ]]; then
    IPINFO=$(curl -s "https://ipinfo.io/${IP}/json?token=${IPINFO_TOKEN}" 2>/dev/null)
else
    IPINFO=$(curl -s "https://ipinfo.io/${IP}/json" 2>/dev/null)
fi

if [[ -n "$IPINFO" ]]; then
    echo "$IPINFO" > "${OUTPUT_DIR}/data/ipinfo.json"
    
    CITY=$(echo "$IPINFO" | jq -r '.city // "unknown"')
    REGION=$(echo "$IPINFO" | jq -r '.region // "unknown"')
    COUNTRY=$(echo "$IPINFO" | jq -r '.country // "unknown"')
    ORG=$(echo "$IPINFO" | jq -r '.org // "unknown"')
    LOC=$(echo "$IPINFO" | jq -r '.loc // "unknown"')
    
    json_merge "$JSON_FILE" "ipinfo" "{
        \"city\": \"$CITY\",
        \"region\": \"$REGION\",
        \"country\": \"$COUNTRY\",
        \"org\": \"$ORG\",
        \"coordinates\": \"$LOC\"
    }"
    log_ok "ipinfo: ${ORG} (${CITY}, ${COUNTRY})"
fi

rate_limit 2

# --- Shodan (requires API key) ---
if [[ -n "${SHODAN_API_KEY:-}" ]]; then
    log_info "Querying Shodan..."
    SHODAN_FILE="${OUTPUT_DIR}/data/shodan.json"
    
    SHODAN_DATA=$(curl -s "https://api.shodan.io/shodan/host/${IP}?key=${SHODAN_API_KEY}" 2>/dev/null)
    echo "$SHODAN_DATA" > "$SHODAN_FILE"
    
    if echo "$SHODAN_DATA" | jq -e '.ip_str' &>/dev/null; then
        PORTS=$(echo "$SHODAN_DATA" | jq '[.ports[]]' 2>/dev/null || echo "[]")
        SERVICES=$(echo "$SHODAN_DATA" | jq '[.data[] | {port: .port, transport: .transport, product: .product, version: .version}]' 2>/dev/null || echo "[]")
        VULNS=$(echo "$SHODAN_DATA" | jq '[.vulns // []]' 2>/dev/null || echo "[]")
        OS=$(echo "$SHODAN_DATA" | jq -r '.os // "unknown"')
        
        json_merge "$JSON_FILE" "shodan" "{
            \"tool\": \"shodan\",
            \"ports\": $PORTS,
            \"services\": $SERVICES,
            \"vulns\": $VULNS,
            \"os\": \"$OS\"
        }"
        log_ok "Shodan: $(echo "$PORTS" | jq 'length') open ports"
    else
        log_warn "Shodan: no data for this IP"
        json_merge "$JSON_FILE" "shodan" '{"tool":"shodan","status":"no_data"}'
    fi
else
    log_warn "SHODAN_API_KEY not set — skipping"
    json_merge "$JSON_FILE" "shodan" '{"tool":"shodan","status":"api_key_missing"}'
fi

# --- nmap (if installed, quick scan) ---
if require_tool nmap 2>/dev/null; then
    log_info "Running nmap quick scan..."
    NMAP_FILE="${OUTPUT_DIR}/data/nmap_quick.txt"
    
    # Quick scan: top 100 ports, service detection
    nmap -sV --top-ports 100 -T4 --open -oN "$NMAP_FILE" "$IP" 2>/dev/null || true
    
    if [[ -f "$NMAP_FILE" ]]; then
        OPEN_PORTS=$(grep "^[0-9]" "$NMAP_FILE" | grep "open" | wc -l | tr -d ' ')
        PORT_DETAILS=$(grep "^[0-9]" "$NMAP_FILE" | grep "open" | awk '{print "{\"port\":"$1",\"state\":\""$2"\",\"service\":\""$3"\",\"version\":\""substr($0, index($0,$4))"\"}"}' | jq -s '.')
        
        json_merge "$JSON_FILE" "nmap" "{
            \"tool\": \"nmap\",
            \"open_ports\": $OPEN_PORTS,
            \"details\": $PORT_DETAILS
        }"
        log_ok "nmap: ${OPEN_PORTS} open ports"
    fi
else
    log_warn "nmap not installed — skipping port scan"
    json_merge "$JSON_FILE" "nmap" '{"tool":"nmap","status":"not_installed"}'
fi

# --- AbuseIPDB (free tier) ---
if [[ -n "${ABUSEIPDB_KEY:-}" ]]; then
    log_info "Checking AbuseIPDB..."
    ABUSE=$(curl -s -H "Key: ${ABUSEIPDB_KEY}" -H "Accept: application/json" \
        "https://api.abuseipdb.com/api/v2/check?ipAddress=${IP}" 2>/dev/null)
    
    if [[ -n "$ABUSE" ]]; then
        SCORE=$(echo "$ABUSE" | jq -r '.data.abuseConfidenceScore // 0')
        REPORTS=$(echo "$ABUSE" | jq -r '.data.totalReports // 0')
        
        json_merge "$JSON_FILE" "abuseipdb" "{
            \"tool\": \"abuseipdb\",
            \"abuse_score\": $SCORE,
            \"total_reports\": $REPORTS
        }"
        log_ok "AbuseIPDB: score=${SCORE}, reports=${REPORTS}"
    fi
else
    json_merge "$JSON_FILE" "abuseipdb" '{"tool":"abuseipdb","status":"api_key_missing"}'
fi

log_info "=== IP Recon Summary ==="
log_info "  Results: ${JSON_FILE}"
