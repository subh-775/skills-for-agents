#!/usr/bin/env bash
# OSINT Toolkit Setup — installs all free, open-source OSINT tools
# Run once: bash setup.sh
# Works on: Linux, macOS, WSL, Git-Bash (Windows)

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LOG_FILE="${SCRIPT_DIR}/setup.log"

log() { echo "[$(date '+%H:%M:%S')] $*" | tee -a "$LOG_FILE"; }
check_cmd() { command -v "$1" &>/dev/null; }

log "=== OSINT Toolkit Setup ==="

# --- Python tools (pip) ---
PYTHON_TOOLS=(
    "sherlock-project"      # Username enumeration (400+ sites)
    "holehe"                # Email to platform check (120+ sites)
    "maigret"               # Extended username search (3000+ sites)
    "theHarvester"          # Emails, subdomains from public sources
    "h8mail"                # Email breach checker
    "photon"                # Fast web crawler for OSINT
    "social-analyzer"       # Cross-platform social media analysis
    "instaloader"           # Instagram profile/post scraper
    "exiftool"              # Metadata extraction (via PyExifTool)
)

log "Installing Python OSINT tools..."
for tool in "${PYTHON_TOOLS[@]}"; do
    if pip install --quiet "$tool" 2>/dev/null; then
        log "  [OK] $tool"
    else
        log "  [WARN] $tool — may need manual install"
    fi
done

# --- Go tools ---
if check_cmd go; then
    log "Installing Go OSINT tools..."
    go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest 2>/dev/null && log "  [OK] subfinder" || log "  [WARN] subfinder failed"
else
    log "  [SKIP] Go not installed — subfinder requires Go"
fi

# --- System tools ---
log "Checking system tools..."
SYS_TOOLS=("whois" "dig" "curl" "jq" "exiftool")
for tool in "${SYS_TOOLS[@]}"; do
    if check_cmd "$tool"; then
        log "  [OK] $tool"
    else
        log "  [MISSING] $tool — install via: apt install $tool / brew install $tool"
    fi
done

# --- PhoneInfoga (binary) ---
if ! check_cmd phoneinfoga; then
    log "PhoneInfoga not found. Install from: https://github.com/sundowndev/phoneinfoga/releases"
    log "  Or: docker pull sundowndev/phoneinfoga"
else
    log "  [OK] phoneinfoga"
fi

log "=== Setup complete ==="
log "Run individual scripts or use osint_orchestrator.sh for full recon"
