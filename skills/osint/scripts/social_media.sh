#!/usr/bin/env bash
# Social Media OSINT — Instaloader + Photon + platform-specific
# Usage: bash social_media.sh <target> <type:username|url|hashtag> [output_dir]
# Output: JSON with profile data, posts, connections

set -euo pipefail
source "$(dirname "$0")/utils.sh"

TARGET="${1:?Usage: social_media.sh <target> <type> [output_dir]}"
TYPE="${2:-username}"
OUTPUT_DIR="${3:-$(ensure_output_dir "social_${TARGET//[^a-zA-Z0-9]/_}")}"
JSON_FILE="${OUTPUT_DIR}/data/social_media.json"

log_info "=== Social Media OSINT: ${TARGET} (${TYPE}) ==="
json_init "$TARGET" "$JSON_FILE"

# --- Instaloader (Instagram) ---
if require_tool instaloader 2>/dev/null; then
    log_info "Running Instaloader..."
    INSTA_DIR="${OUTPUT_DIR}/data/instagram"
    mkdir -p "$INSTA_DIR"
    
    # Download profile metadata only (no posts to save time)
    instaloader --no-videos --no-posts --no-compress-json \
        --dirname-pattern="$INSTA_DIR" \
        -- "$TARGET" 2>/dev/null || true
    
    # Check for profile JSON
    PROFILE_JSON="${INSTA_DIR}/${TARGET}/${TARGET}.json"
    if [[ -f "$PROFILE_JSON" ]]; then
        FOLLOWERS=$(jq -r '.edge_followed_by.count // 0' "$PROFILE_JSON" 2>/dev/null)
        FOLLOWING=$(jq -r '.edge_follow.count // 0' "$PROFILE_JSON" 2>/dev/null)
        POSTS=$(jq -r '.edge_owner_to_timeline_media.count // 0' "$PROFILE_JSON" 2>/dev/null)
        BIO=$(jq -r '.biography // "none"' "$PROFILE_JSON" 2>/dev/null)
        FULL_NAME=$(jq -r '.full_name // "unknown"' "$PROFILE_JSON" 2>/dev/null)
        IS_PRIVATE=$(jq -r '.is_private // false' "$PROFILE_JSON" 2>/dev/null)
        IS_VERIFIED=$(jq -r '.is_verified // false' "$PROFILE_JSON" 2>/dev/null)
        
        json_merge "$JSON_FILE" "instagram" "{
            \"platform\": \"instagram\",
            \"username\": \"$TARGET\",
            \"full_name\": \"$FULL_NAME\",
            \"followers\": $FOLLOWERS,
            \"following\": $FOLLOWING,
            \"posts\": $POSTS,
            \"bio\": $(echo "$BIO" | jq -Rs '.'),
            \"is_private\": $IS_PRIVATE,
            \"is_verified\": $IS_VERIFIED
        }"
        log_ok "Instagram: ${FOLLOWERS} followers, ${POSTS} posts"
    else
        json_merge "$JSON_FILE" "instagram" '{"platform":"instagram","status":"profile_not_found"}'
    fi
else
    log_warn "Instaloader not installed"
    json_merge "$JSON_FILE" "instagram" '{"platform":"instagram","status":"not_installed"}'
fi

rate_limit 2

# --- Photon (web crawler for social links) ---
if require_tool photon 2>/dev/null; then
    log_info "Running Photon web crawler..."
    PHOTON_DIR="${OUTPUT_DIR}/data/photon"
    
    # If target looks like a URL, crawl it
    if [[ "$TARGET" =~ ^https?:// ]] || [[ "$TYPE" == "url" ]]; then
        photon -u "$TARGET" -o "$PHOTON_DIR" --keys --only-urls 2>/dev/null || true
        
        if [[ -d "$PHOTON_DIR" ]]; then
            # Extract social media links
            SOCIAL_LINKS=$(cat "$PHOTON_DIR/externals.txt" 2>/dev/null | grep -iE "facebook|twitter|instagram|linkedin|youtube|tiktok|github" | sort -u | jq -R -s 'split("\n") | map(select(length > 0))')
            EMAILS_PHOTON=$(cat "$PHOTON_DIR/externals.txt" 2>/dev/null | grep -oP '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}' | sort -u | jq -R -s 'split("\n") | map(select(length > 0))')
            
            json_merge "$JSON_FILE" "photon_crawl" "{
                \"tool\": \"photon\",
                \"social_links\": $SOCIAL_LINKS,
                \"emails\": $EMAILS_PHOTON
            }"
            log_ok "Photon: $(echo "$SOCIAL_LINKS" | jq 'length') social links"
        fi
    else
        log_info "Photon: target is not a URL — skipping web crawl"
    fi
else
    log_warn "Photon not installed"
fi

# --- GitHub user recon (free, no auth needed) ---
if [[ "$TYPE" == "username" ]]; then
    log_info "Checking GitHub profile..."
    GH_RESPONSE=$(curl -s "https://api.github.com/users/${TARGET}" 2>/dev/null)
    
    if echo "$GH_RESPONSE" | jq -e '.login' &>/dev/null; then
        GH_NAME=$(echo "$GH_RESPONSE" | jq -r '.name // "unknown"')
        GH_BIO=$(echo "$GH_RESPONSE" | jq -r '.bio // "none"')
        GH_PUBLIC_REPOS=$(echo "$GH_RESPONSE" | jq -r '.public_repos // 0')
        GH_FOLLOWERS=$(echo "$GH_RESPONSE" | jq -r '.followers // 0')
        GH_FOLLOWING=$(echo "$GH_RESPONSE" | jq -r '.following // 0')
        GH_COMPANY=$(echo "$GH_RESPONSE" | jq -r '.company // "none"')
        GH_LOCATION=$(echo "$GH_RESPONSE" | jq -r '.location // "none"')
        GH_BLOG=$(echo "$GH_RESPONSE" | jq -r '.blog // "none"')
        GH_EMAIL=$(echo "$GH_RESPONSE" | jq -r '.email // "none"')
        
        json_merge "$JSON_FILE" "github" "{
            \"platform\": \"github\",
            \"username\": \"$TARGET\",
            \"name\": \"$GH_NAME\",
            \"bio\": $(echo "$GH_BIO" | jq -Rs '.'),
            \"public_repos\": $GH_PUBLIC_REPOS,
            \"followers\": $GH_FOLLOWERS,
            \"following\": $GH_FOLLOWING,
            \"company\": \"$GH_COMPANY\",
            \"location\": \"$GH_LOCATION\",
            \"blog\": \"$GH_BLOG\",
            \"email\": \"$GH_EMAIL\"
        }"
        log_ok "GitHub: ${GH_PUBLIC_REPOS} repos, ${GH_FOLLOWERS} followers"
    else
        json_merge "$JSON_FILE" "github" '{"platform":"github","status":"user_not_found"}'
    fi
fi

rate_limit 1

# --- Reddit user check ---
if [[ "$TYPE" == "username" ]]; then
    log_info "Checking Reddit profile..."
    REDDIT_RESPONSE=$(curl -s -H "User-Agent: osint-skill/1.0" "https://www.reddit.com/user/${TARGET}/about.json" 2>/dev/null)
    
    if echo "$REDDIT_RESPONSE" | jq -e '.data.name' &>/dev/null; then
        R_KARMA=$(echo "$REDDIT_RESPONSE" | jq -r '.data.total_karma // 0')
        R_CREATED=$(echo "$REDDIT_RESPONSE" | jq -r '.data.created_utc // 0')
        R_COMMENT_KARMA=$(echo "$REDDIT_RESPONSE" | jq -r '.data.comment_karma // 0')
        R_LINK_KARMA=$(echo "$REDDIT_RESPONSE" | jq -r '.data.link_karma // 0')
        
        # Convert epoch to date
        R_DATE=$(date -d "@${R_CREATED}" '+%Y-%m-%d' 2>/dev/null || date -r "${R_CREATED}" '+%Y-%m-%d' 2>/dev/null || echo "unknown")
        
        json_merge "$JSON_FILE" "reddit" "{
            \"platform\": \"reddit\",
            \"username\": \"$TARGET\",
            \"total_karma\": $R_KARMA,
            \"comment_karma\": $R_COMMENT_KARMA,
            \"link_karma\": $R_LINK_KARMA,
            \"account_created\": \"$R_DATE\"
        }"
        log_ok "Reddit: ${R_KARMA} karma, created ${R_DATE}"
    else
        json_merge "$JSON_FILE" "reddit" '{"platform":"reddit","status":"user_not_found"}'
    fi
fi

log_info "=== Social Media OSINT Summary ==="
log_info "  Results: ${JSON_FILE}"
