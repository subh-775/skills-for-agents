#!/usr/bin/env bash
# Shared utility functions for OSINT scripts
# Source this file: source "$(dirname "$0")/utils.sh"

set -euo pipefail

# Ensure common tool locations are on PATH
export PATH="$HOME/bin:$HOME/go/bin:/usr/local/bin:$PATH"

# --- Config ---
OSINT_OUTPUT_DIR="${OSINT_OUTPUT_DIR:-$HOME/osint}"
TIMESTAMP=$(date '+%d_%b_%Y')
JSON_INDENT=2

# --- Colors ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# --- Logging ---
log_info()  { echo -e "${BLUE}[INFO]${NC} $*"; }
log_ok()    { echo -e "${GREEN}[OK]${NC} $*"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC} $*"; }
log_error() { echo -e "${RED}[ERROR]${NC} $*"; }

# --- JSON helpers ---
json_init() {
    local target="$1"
    local file="$2"
    mkdir -p "$(dirname "$file")"
    echo "{}" | jq --arg t "$target" --arg d "$(date -Iseconds)" '
        {target: $t, timestamp: $d, results: {}}
    ' > "$file"
    echo "$file"
}

json_merge() {
    local file="$1" key="$2" value="$3"
    local tmp="${file}.tmp"
    jq --arg k "$key" --argjson v "$value" '.results[$k] = $v' "$file" > "$tmp" && mv "$tmp" "$file"
}

json_add_array() {
    local file="$1" key="$2" value="$3"
    local tmp="${file}.tmp"
    jq --arg k "$key" --argjson v "$value" '.results[$k] = $v' "$file" > "$tmp" && mv "$tmp" "$file"
}

# --- Output directory ---
ensure_output_dir() {
    local tag="$1"
    local dir="${OSINT_OUTPUT_DIR}/${tag}_${TIMESTAMP}"
    mkdir -p "$dir"/{data,assets}
    echo "$dir"
}

# --- Tool check ---
require_tool() {
    local tool="$1"
    if ! command -v "$tool" &>/dev/null; then
        log_warn "$tool not installed — skipping"
        return 1
    fi
    return 0
}

# --- Safe command runner (never kills script on failure) ---
safe_run() {
    "$@" 2>/dev/null || true
}

# --- Timeout wrapper ---
with_timeout() {
    local timeout_sec="$1"
    shift
    timeout "$timeout_sec" "$@" 2>/dev/null || true
}

# --- Rate limit ---
rate_limit() {
    local seconds="${1:-3}"
    sleep "$seconds"
}
