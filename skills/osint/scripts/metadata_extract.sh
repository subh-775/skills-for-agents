#!/usr/bin/env bash
# Metadata Extraction — ExifTool + file analysis
# Usage: bash metadata_extract.sh <file_or_directory> [output_dir]
# Output: JSON with EXIF data, GPS coordinates, camera info, hidden data

set -euo pipefail
source "$(dirname "$0")/utils.sh"

TARGET="${1:?Usage: metadata_extract.sh <file_or_dir> [output_dir]}"
OUTPUT_DIR="${2:-$(ensure_output_dir "metadata_$(basename "$TARGET" | tr '.' '_')")}"
JSON_FILE="${OUTPUT_DIR}/data/metadata.json"

log_info "=== Metadata Extraction: ${TARGET} ==="
json_init "$TARGET" "$JSON_FILE"

# --- ExifTool ---
if require_tool exiftool 2>/dev/null; then
    log_info "Running ExifTool..."
    
    if [[ -d "$TARGET" ]]; then
        # Directory — extract from all files
        EXIF_DIR="${OUTPUT_DIR}/data/exif"
        mkdir -p "$EXIF_DIR"
        
        FILE_COUNT=0
        GPS_FOUND=0
        CAMERA_FOUND=0
        
        for file in "$TARGET"/*; do
            [[ -f "$file" ]] || continue
            FILE_COUNT=$((FILE_COUNT + 1))
            
            BASENAME=$(basename "$file")
            exiftool -json "$file" > "${EXIF_DIR}/${BASENAME}.json" 2>/dev/null || true
            
            # Check for GPS
            if jq -e '.[0].GPSLatitude' "${EXIF_DIR}/${BASENAME}.json" &>/dev/null; then
                GPS_FOUND=$((GPS_FOUND + 1))
            fi
            # Check for camera
            if jq -e '.[0].Make // .[0].Model' "${EXIF_DIR}/${BASENAME}.json" &>/dev/null; then
                CAMERA_FOUND=$((CAMERA_FOUND + 1))
            fi
        done
        
        json_merge "$JSON_FILE" "exiftool" "{
            \"tool\": \"exiftool\",
            \"files_processed\": $FILE_COUNT,
            \"gps_data_found\": $GPS_FOUND,
            \"camera_data_found\": $CAMERA_FOUND,
            \"exif_dir\": \"exif/\"
        }"
        log_ok "ExifTool: ${FILE_COUNT} files, ${GPS_FOUND} with GPS, ${CAMERA_FOUND} with camera"
        
    elif [[ -f "$TARGET" ]]; then
        # Single file
        EXIF_FILE="${OUTPUT_DIR}/data/exif_$(basename "$TARGET").json"
        exiftool -json "$TARGET" > "$EXIF_FILE" 2>/dev/null || true
        
        if [[ -s "$EXIF_FILE" ]]; then
            # Extract key fields
            GPS_LAT=$(jq -r '.[0].GPSLatitude // "none"' "$EXIF_FILE")
            GPS_LON=$(jq -r '.[0].GPSLongitude // "none"' "$EXIF_FILE")
            CAMERA=$(jq -r '.[0].Make // "unknown"') 
            MODEL=$(jq -r '.[0].Model // "unknown"')
            DATE=$(jq -r '.[0].DateTimeOriginal // .[0].CreateDate // "unknown"')
            SOFTWARE=$(jq -r '.[0].Software // "unknown"')
            
            json_merge "$JSON_FILE" "exiftool" "{
                \"tool\": \"exiftool\",
                \"gps\": {\"lat\": \"$GPS_LAT\", \"lon\": \"$GPS_LON\"},
                \"camera\": \"$CAMERA\",
                \"model\": \"$MODEL\",
                \"date_taken\": \"$DATE\",
                \"software\": \"$SOFTWARE\",
                \"full_exif\": \"$(basename "$EXIF_FILE")\"
            }"
            log_ok "ExifTool: GPS=${GPS_LAT},${GPS_LON} Camera=${CAMERA} ${MODEL}"
        fi
    fi
else
    log_warn "exiftool not installed"
    json_merge "$JSON_FILE" "exiftool" '{"tool":"exiftool","status":"not_installed"}'
fi

# --- File type analysis ---
if [[ -f "$TARGET" ]]; then
    log_info "Analyzing file type..."
    FILE_TYPE=$(file -b "$TARGET" 2>/dev/null || echo "unknown")
    FILE_SIZE=$(stat -c%s "$TARGET" 2>/dev/null || stat -f%z "$TARGET" 2>/dev/null || echo "0")
    MD5=$(md5sum "$TARGET" 2>/dev/null | awk '{print $1}' || md5 -q "$TARGET" 2>/dev/null || echo "unknown")
    SHA256=$(sha256sum "$TARGET" 2>/dev/null | awk '{print $1}' || shasum -a 256 "$TARGET" 2>/dev/null | awk '{print $1}' || echo "unknown")
    
    json_merge "$JSON_FILE" "file_info" "{
        \"type\": \"$FILE_TYPE\",
        \"size_bytes\": $FILE_SIZE,
        \"md5\": \"$MD5\",
        \"sha256\": \"$SHA256\"
    }"
    log_ok "File: ${FILE_TYPE}, ${FILE_SIZE} bytes"
fi

# --- Strings extraction (hidden text in binaries) ---
if [[ -f "$TARGET" ]] && require_tool strings 2>/dev/null; then
    log_info "Extracting strings..."
    STRINGS_FILE="${OUTPUT_DIR}/data/strings.txt"
    
    strings -n 8 "$TARGET" > "$STRINGS_FILE" 2>/dev/null || true
    
    # Look for interesting patterns
    URLS=$(grep -oP 'https?://[^\s"<>]+' "$STRINGS_FILE" 2>/dev/null | sort -u | jq -R -s 'split("\n") | map(select(length > 0))')
    EMAILS_STR=$(grep -oP '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}' "$STRINGS_FILE" 2>/dev/null | sort -u | jq -R -s 'split("\n") | map(select(length > 0))')
    IPS_STR=$(grep -oP '\b[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\b' "$STRINGS_FILE" 2>/dev/null | sort -u | jq -R -s 'split("\n") | map(select(length > 0))')
    
    json_merge "$JSON_FILE" "strings_analysis" "{
        \"urls_found\": $URLS,
        \"emails_found\": $EMAILS_STR,
        \"ips_found\": $IPS_STR,
        \"total_strings\": $(wc -l < "$STRINGS_FILE" | tr -d ' ')
    }"
    log_ok "Strings: $(echo "$URLS" | jq 'length') URLs, $(echo "$EMAILS_STR" | jq 'length') emails"
fi

log_info "=== Metadata Extraction Summary ==="
log_info "  Results: ${JSON_FILE}"
