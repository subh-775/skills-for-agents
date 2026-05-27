# Comprehensive OSINT Research Report
## Skills-for-Agents OSINT Skill Development

**Author:** Bauna Intern  
**Date:** 2026-05-21  
**Purpose:** Research for building a comprehensive OSINT skill for AI agents

---

## Table of Contents

1. [Email OSINT](#1-email-osint)
2. [Phone Number OSINT](#2-phone-number-osint)
3. [Username/Social Media OSINT](#3-username-social-media-osint)
4. [Google Dorks for OSINT](#4-google-dorks-for-osint)
5. [Leaked Database Checks](#5-leaked-database-checks)
6. [Network/Infrastructure OSINT](#6-network-infrastructure-osint)
7. [Geolocation OSINT](#7-geolocation-osint)
8. [People Search Engines](#8-people-search-engines)
9. [Company/Workplace OSINT](#9-company-workplace-osint)
10. [Deep Web/Dark Web OSINT](#10-deep-web-dark-web-osint)
11. [OSINT Automation Frameworks](#11-osint-automation-frameworks)
12. [Tool Installation Reference](#12-tool-installation-reference)

---

## 1. Email OSINT

### 1.1 Finding Social Media Accounts from Email

**Holehe** — The primary tool for email-to-account discovery.

- **Coverage:** 120+ websites
- **Methods:** Registration checks, login verification, password recovery
- **Stealth:** Does NOT alert the target email
- **Detection methods breakdown:**
  - `register` — checks via registration endpoint
  - `login` — checks via login endpoint
  - `password recovery` — uses forgot password flow
  - `other` — miscellaneous methods
- **Rate-limited platforms:** Instagram, Spotify, Google, eBay, Yahoo, Venmo, Patreon
- **Workaround:** Change IP / use proxy
- **Online version:** https://osint.industries
- **Maltego integration:** https://github.com/megadose/holehe-maltego
- **Stars:** ~11k | **Forks:** ~1.3k | **License:** GPL-3.0

```bash
# Installation
pip3 install holehe

# CLI usage
holehe test@gmail.com

# Docker
docker build . -t my-holehe-image
docker run my-holehe-image holehe test@gmail.com
```

**Python API:**
```python
import trio
import httpx
from holehe.modules.social_media.instagram import instagram

async def main():
    out = []
    async with httpx.AsyncClient() as client:
        await instagram("test@gmail.com", client, out)
    print(out)

trio.run(main)
```

**Output format per module:**
```json
{
  "name": "instagram",
  "rateLimit": false,
  "exists": true,
  "emailrecovery": "t***@g***.com",
  "phoneNumber": null,
  "others": null
}
```

**Supported platforms by detection method:**
| Method | Platforms |
|--------|-----------|
| Register check | Twitter, Instagram, Discord, GitHub, Pinterest, Tumblr, SoundCloud, Docker, Nike, Samsung, Firefox, Spotify |
| Login check | Amazon, Snapchat, eBay, Evernote, Flickr, WordPress, Yahoo, Zoho |
| Password recovery | Adobe, mail.ru, Odnoklassniki |
| Other | Gravatar, Protonmail, Office365 |

**Rate-limited platforms:** Instagram, Spotify, Google, eBay, Yahoo  
**Workaround:** Change IP / use proxy

**Online version:** https://osint.industries  
**Maltego integration:** https://github.com/megadose/holehe-maltego

---

### 1.2 Checking Data Breaches (Have I Been Pwned)

**HIBP API v3** — Base URL: `https://haveibeenpwned.com/api/v3`

**Authentication:** API key via `hibp-api-key` header + `user-agent` header (required, or 403)

**Key Endpoints:**

| Endpoint | Purpose |
|----------|---------|
| `GET /breachedAccount/{email}` | Check if email appears in breaches |
| `GET /breaches` | List all ~993 breaches |
| `GET /breach/{name}` | Details on specific breach |
| `GET /latestBreach` | Most recent breach added |
| `GET /dataClasses` | All types of compromised data |
| `GET /breachedDomain/{domain}` | All breached emails on verified domain |
| `GET /pasteAccount/{email}` | Pastes containing the address |

**Stealer Logs (Pro+ tier):**
| Endpoint | Purpose |
|----------|---------|
| `GET /stealerLogsByEmail/{email}` | Domains from stealer logs for email |
| `GET /stealerLogsByWebsiteDomain/{domain}` | Emails captured at specific site |
| `GET /stealerLogsByEmailDomain/{domain}` | Email aliases and associated domains |

**Pwned Passwords (FREE, no API key):**
```bash
# K-anonymity model - only sends first 5 SHA-1 chars
curl "https://api.pwnedpasswords.com/range/{first_5_sha1_chars}"

# NTLM support
curl "https://api.pwnedpasswords.com/range/{first_5_sha1_chars}?mode=ntlm"
```

**Response Codes:**
| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Bad format |
| 401 | Invalid/missing API key |
| 403 | Missing user agent |
| 404 | Email not found in breaches |
| 429 | Rate limit exceeded |

**Licensing:** Creative Commons Attribution 4.0 (must credit HIBP)

---

### 1.3 Email Header Analysis

**Technique:** Parse email headers to extract:
- Originating IP address
- Mail server hops (Received: headers)
- Authentication results (SPF, DKIM, DMARC)
- Sender's email client/User-Agent
- Timestamps for each hop

**Tools:**
- Google Admin Toolbox Message Header Analyzer: https://toolbox.googleapps.com/apps/messageheader/
- MXToolbox Header Analyzer: https://mxtoolbox.com/HeaderAnalyzer.aspx

**Key header fields to extract:**
```
Received:          — Server hop chain
From:              — Sender address
Reply-To:          — Actual reply destination
Return-Path:       — Bounce address
X-Originating-IP: — Sender's IP (if present)
X-Mailer:          — Email client used
Authentication-Results: — SPF/DKIM/DMARC status
Message-ID:        — Unique message identifier (contains sending server domain)
```

---

### 1.4 Finding Email Owner Details

**Hunter.io** — Email finding and verification platform.

**API Base:** `https://api.hunter.io/v2/`

| Endpoint | Purpose |
|----------|---------|
| `GET /domain-search` | All emails for a domain |
| `GET /email-finder` | Find email by name + domain |
| `GET /email-verifier` | Verify email validity |
| `GET /discover` | Find companies by ICP criteria |

**Returns:** Name, employment, seniority, social profiles (Twitter, LinkedIn, GitHub), timezone, geo coordinates, email format patterns (e.g., `{first}` for first-name-only)

**Free tier:** 50 credits/month

**Epieos** — Reverse email lookup tool (https://epieos.com)
- Finds associated online accounts from email
- Identifies linked services and platforms
- Useful for digital forensics investigations

---

### 1.5 Additional Email OSINT Tools

**theHarvester** — Comprehensive email and subdomain gathering:
```bash
# Installation
git clone https://github.com/laramies/theHarvester
cd theHarvester
uv sync
uv run theHarvester

# Usage
uv run theHarvester -d target.com -b all
uv run theHarvester -d target.com -b google,bing,yahoo
uv run theHarvester -d target.com -b hunter -l 200
```

**44+ passive sources including:**
- Search engines: baidu, brave, duckduckgo, mojeek, yahoo
- Certificate/DNS: censys, certspotter, crtsh, securityTrails, rapiddns
- Email/breach: hunter, haveibeenpwned, dehashed, intelx, leakix, leaklookup, rocketreach, tomba
- Attack surface: shodan, zoomeye, netlas, onyphe, otx, fullhunt, fofa

**email2phonenumber** — Find phone numbers from email:
```bash
git clone https://github.com/martinvigo/email2phonenumber
cd email2phonenumber
pip3 install beautifulsoup4 requests

# Scrape phone digits from password reset flows
python3 email2phonenumber.py scrape -e target@email.com

# Generate valid phone numbers from mask (X = unknown digits)
python3 email2phonenumber.py generate -m 555XXX1234 -o /tmp/dic.txt

# Bruteforce with proxies to bypass rate limits
python3 email2phonenumber.py bruteforce -m 555XXX1234 -e target@email.com -p /tmp/proxies.txt -q
```

**Status:** Proof-of-concept, largely non-functional today. Supported services (eBay, LastPass, Amazon, Twitter) have added protections (email verification codes, CAPTCHAs). Author recommends successor tool: **Phonerator** for generating valid phone numbers from numbering plans.

**Epieos** (epieos.com) — Reverse email lookup
- Finds associated online accounts from email
- Identifies linked services and platforms
- Useful for digital forensics investigations
- Behind DataDome CAPTCHA protection

**Hunter.io** — Email finding and verification platform
- Domain Search: reveals email patterns and contacts for a company domain
- Email Finder: name-to-email resolution with verification
- Email Verifier: checks deliverability
- API at hunter.io/api
- Chrome extension (600k+ users, 4.7 rating)
- Identifies email format patterns (e.g., `{first}.{last}@domain.com`)
- Free tier: 50 credits/month

**Infoga** — Email intelligence gathering (REMOVED from GitHub, no longer available)

---

## 2. Phone Number OSINT

### 2.1 PhoneInfoga

**The most advanced phone number OSINT tool.**

**Installation:**
```bash
# Binary
curl -sSL https://raw.githubusercontent.com/sundowndev/phoneinfoga/master/support/scripts/install.sh | bash

# Docker
docker run -it sundowndev/phoneinfoga scan -n +1234567890

# Go install
go install github.com/sundowndev/phoneinfoga/v2/cmd/phoneinfoga@latest
```

**Usage:**
```bash
# Basic scan
phoneinfoga scan -n +1234567890

# With specific scanners
phoneinfoga scan -n +1234567890 -s numverify

# Serve web UI
phoneinfoga serve -p 8080
```

**Capabilities:**
- Country, carrier, and line type identification
- VoIP provider identification
- Reputation scanning (spam reports, social media presence)
- Disposable number detection
- REST API with Swagger/OpenAPI docs
- Web GUI for browser-based scanning
- Plugin architecture for custom scanners

**API endpoints (when serving):**
```
GET  /api/v1/numbers/{number}/scan
POST /api/v1/numbers/{number}/scan
GET  /api/v1/config/scanners
```

**Status:** Stable but unmaintained (v2.11.0, Feb 2024)

---

### 2.2 Carrier & Location Lookup

**NumVerify API:**
```
http://apilayer.net/api/validate?access_key=YOUR_KEY&number=14158586273
```

**Returns:** valid, local_format, international_format, country_prefix, country_code, country_name, location, carrier, line_type

**Free tier:** 100 requests/month

**NumVerify alternative — Abstract API:**
```
https://phonevalidation.abstractapi.com/v1/?api_key=YOUR_KEY&phone=14158586273
```

---

### 2.3 TrueCaller API

**TrueCaller** — Reverse phone lookup with name identification.

**API access:** Requires authentication via TrueCaller app OAuth token

**Alternative approaches:**
- Use the TrueCaller website directly
- Scraping not recommended (anti-bot measures)
- Alternative: https://www.truecaller.com/search/{country}/{number}

---

### 2.4 Additional Phone OSINT Techniques

**Phone number format validation:**
```python
import phonenumbers
from phonenumbers import carrier, geocoder, timezone

number = phonenumbers.parse("+14158586273")
print(phonenumbers.is_valid_number(number))  # True/False
print(carrier.name_for_number(number, "en"))  # Carrier name
print(geocoder.description_for_number(number, "en"))  # Location
print(timezone.time_zones_for_number(number))  # Timezone
```

**Social media lookup by phone:**
- Facebook: Search phone number directly
- WhatsApp: Check if number is on WhatsApp (profile photo visible)
- Telegram: Check if number has Telegram account
- Viber: Similar check

---

## 3. Username/Social Media OSINT

### 3.1 Sherlock

**Hunt down social media accounts by username across 400+ social networks.**

```bash
# Installation
pipx install sherlock-project

# Docker
docker run -it --rm sherlock/sherlock

# Fedora
dnf install sherlock-project
```

**Usage:**
```bash
# Single username
sherlock user123

# Multiple usernames
sherlock user1 user2 user3

# With specific options
sherlock user123 --timeout 30 --proxy socks5://127.0.0.1:1080

# Export formats
sherlock user123 --csv
sherlock user123 --xlsx
sherlock user123 --json results.json

# Filter by site
sherlock user123 --site twitter --site instagram

# Include NSFW sites
sherlock user123 --nsfw

# Open results in browser
sherlock user123 --browse

# Silent mode (only found results)
sherlock user123 --print-found

# Check similar usernames
sherlock "user{?}123"  # checks user_123, user-123, user.123
```

**Options:**
| Flag | Description |
|------|-------------|
| `--output / -o` | Save results to file |
| `--folderoutput / -fo` | Save multi-user results to folder |
| `--csv` | CSV export |
| `--xlsx` | Excel export |
| `--site` | Limit to specific site(s) |
| `--proxy / -p` | Route through proxy |
| `--timeout` | Request timeout (default: 60s) |
| `--print-all` | Show all sites (including not found) |
| `--print-found` | Show only found |
| `--no-color` | Disable colored output |
| `--browse / -b` | Open in browser |
| `--nsfw` | Include NSFW sites |
| `--ignore-exclusions` | Bypass upstream exclusions |

**Version:** 0.16.0 | **License:** MIT | **Stars:** 83.6k

---

### 3.2 Maigret

**Collects a dossier on a person by username only, checking 3,000+ sites.**

```bash
# Installation
pip install maigret

# Basic usage
maigret user

# Multiple usernames, all sites
maigret user1 user2 user3 -a

# HTML report
maigret user --html

# PDF report
pip install 'maigret[pdf]'
maigret user --pdf

# JSON/NDJSON
maigret user --json ndjson

# Filter by tags
maigret user --tags photo,dating

# AI-assisted summary
maigret user --ai

# Web interface
maigret --web 5000

# Parse URL and extract IDs for recursive search
maigret --parse https://twitter.com/username

# Generate username permutations
maigret --permute "john doe"

# Proxy support
maigret user --proxy socks5://127.0.0.1:1080
maigret user --tor-proxy socks5://127.0.0.1:9050
maigret user --i2p-proxy http://127.0.0.1:4444
```

**Key advantages over Sherlock:**
| Feature | Maigret | Sherlock |
|---------|---------|----------|
| Sites covered | 3,000+ (5,000+ commercial) | 400+ |
| Data extraction | Full profile data via socid_extractor | Existence check only |
| Recursive search | Auto-follows discovered usernames | Single-pass |
| Report formats | HTML, PDF, XMind, JSON, CSV, TXT, D3 graph | TXT, CSV, XLSX |
| AI analysis | Built-in OpenAI-compatible summarization | None |
| Web interface | Built-in with graph visualization | None |
| Tor/I2P | Native support | Varies |
| Cloudflare bypass | Experimental FlareSolverr | None |

**Docker:**
```bash
# CLI mode
docker run soxoj/maigret:latest maigret user

# Web UI mode (port 5000)
docker run -p 5000:5000 soxoj/maigret:web
```

**Python library:**
```python
import maigret
import asyncio

results = asyncio.run(maigret.search("username"))
```

**License:** MIT | **Stars:** 11k+ | **Python:** 3.10+

---

### 3.3 Social Analyzer

**API, CLI, and Web App for analyzing profiles across 1,000+ social media websites.**

```bash
# Python installation
pip3 install social-analyzer
python3 -m social-analyzer --username "johndoe"

# Node.js installation
git clone https://github.com/qeeqbox/social-analyzer
cd social-analyzer
npm install
nodejs app.js --username "johndoe"

# Web UI
npm start  # runs at http://0.0.0.0:9005/app.html
```

**CLI arguments:**
```bash
# Fast mode
python3 -m social-analyzer --username "johndoe" --mode fast

# Filter by country
python3 -m social-analyzer --username "johndoe" --countries us br ru

# Filter by type
python3 -m social-analyzer --username "johndoe" --type Adult

# Top N sites
python3 -m social-analyzer --username "johndoe" --top 50

# JSON output
python3 -m social-analyzer --username "johndoe" --output json

# Extract metadata
python3 -m social-analyzer --username "johndoe" --extract --metadata

# Specific websites
python3 -m social-analyzer --username "johndoe" --websites youtube tiktok

# Filter results
python3 -m social-analyzer --username "johndoe" --filter good,maybe
```

**Python library:**
```python
from importlib import import_module
SocialAnalyzer = import_module("social-analyzer").SocialAnalyzer()
results = SocialAnalyzer.run_as_object(username="johndoe", silent=True)
print(results)
```

**Special detections:**
| Platform | Method |
|----------|--------|
| Facebook | Phone number, name, or profile name |
| Gmail | Email address |
| Google | Email address |

**Detection techniques:** OCR, normal, advanced, and special methods with rating 0-100

**License:** AGPL-3.0 | **Stars:** 22.9k

---

### 3.4 Instaloader (Instagram)

```bash
# Installation
pip3 install instaloader

# Download all posts from a profile
instaloader profile target_username

# Fast update (skip existing)
instaloader --fast-update profile target_username

# Include comments and geotags
instaloader --comments --geotags profile target_username

# Download stories
instaloader target_username:stories

# Download highlights
instaloader --highlights target_username

# Download tagged posts
instaloader --tagged target_username

# Download reels
instaloader --reels target_username

# Download by hashtag
instaloader "#hashtag"

# Download private profile (requires login)
instaloader --login=your_username profile target_username

# Download saved posts
instaloader :saved

# Download feed
instaloader :feed

# Latest stamps for incremental
instaloader --latest-stamps -- profile target_username
```

**Python API:**
```python
import instaloader

L = instaloader.Instaloader()
L.login("your_username", "password")

profile = instaloader.Profile.from_username(L.context, "target_username")
print(f"Followers: {profile.followers}")
print(f"Following: {profile.followees}")
print(f"Posts: {profile.mediacount}")
print(f"Bio: {profile.biography}")
print(f"External URL: {profile.external_url}")

for post in profile.get_posts():
    L.download_post(post, target=profile.username)
```

**License:** MIT | **Stars:** 12.4k

---

### 3.5 Twint (Twitter/X) — ARCHIVED

**Status:** Archived (March 2023), no longer maintained. Last release v2.1.4 (Oct 2019). 16.4k stars, MIT license.

```bash
# Installation (may not work with current Twitter)
pip3 install twint

# Scrape all tweets from user
twint -u username

# Search tweets
twint -u username -s "search term"

# Export to CSV
twint -u username -o file.csv --csv

# Find emails and phones in tweets
twint -u username --email --phone

# Scrape followers
twint -u username --followers

# Scrape following
twint -u username --following

# Favorites
twint -u username --favorites

# Timeline (including retweets)
twint -u username --timeline

# Elasticsearch output
twint -u username -es localhost:9200

# SQLite output
twint -u username --database tweets.db

# Geolocation-based scraping (1km radius)
twint -g="48.880048,2.385939,1km" -o file.csv --csv

# Verified accounts only
twint -s "topic" --verified

# Date filtering
twint -u username --since "2015-12-20 20:30:15"
twint -u username --year 2014

# Full profile info
twint -u username --user-full

# Resume interrupted scrape
twint -u username --resume resume_file.txt

# Translation
twint -u username --csv --output none.csv --lang en --translate --translate-dest it --limit 100
```

**Python module usage:**
```python
import twint

c = twint.Config()
c.Username = "target"
c.Search = "keyword"
c.Limit = 100
c.Store_csv = True
c.Output = "results"
twint.run.Search(c)
```

**Note:** Twitter/X has significantly restricted scraping. Twint is no longer functional with current Twitter/X API changes.

---

### 3.6 Finding Deleted Posts and Archives

**Techniques:**
1. **Wayback Machine** (web.archive.org) — Archive.org's cached snapshots
   ```
   https://web.archive.org/web/*/twitter.com/username/status/*
   ```

2. **Google Cache** — `cache:url` operator
   ```
   cache:twitter.com/username/status/1234567890
   ```

3. **Unddit / Reveddit** — Reddit removed/deleted post recovery

4. **Wayback Machine API:**
   ```
   https://archive.org/wayback/available?url=twitter.com/username
   ```

5. **Pushshift** (Reddit) — Historical Reddit data (API restricted as of 2023)

6. **Social media archive services:**
   - Thread Reader App (Twitter threads)
   - Perma.cc (legal/archival)
   - Archive.today (archive.is)

---

## 4. Google Dorks for OSINT

### 4.1 Core Operators

| Operator | Purpose | Example |
|----------|---------|---------|
| `site:` | Restrict to domain | `site:example.com` |
| `filetype:` / `ext:` | Filter by extension | `filetype:pdf` |
| `inurl:` | Search within URLs | `inurl:admin` |
| `intitle:` | Search page titles | `intitle:"index of"` |
| `intext:` | Search body text | `intext:"password"` |
| `before:` | Date filter (before) | `before:2024-01-01` |
| `after:` | Date filter (after) | `after:2023-01-01` |
| `cache:` | View cached version | `cache:example.com` |
| `related:` | Find similar sites | `related:example.com` |
| `" "` | Exact phrase match | `"confidential report"` |
| `-` | Exclude terms | `login -register` |
| `*` | Wildcard | `"default * password"` |
| `OR` | Boolean OR | `admin OR administrator` |
| `allintitle:` | All words in title | `allintitle: admin login portal` |
| `allinurl:` | All words in URL | `allinurl: admin panel` |
| `allintext:` | All words in body | `allintext: username password` |
| `link:` | Pages linking to URL | `link:example.com` |
| `numrange:` | Number range | `numrange:1000-2000` |
| `loc:` / `location:` | Geographic restriction | `loc:"new york"` |

---

### 4.2 Dorks by Category (GHDB)

**Exposed Directories:**
```
intitle:"index of" "parent directory"
intitle:"index of" /etc/
intitle:"index of" /config/
intitle:"index of" wp-content/uploads/
intitle:"index of" ".git"
intitle:"index of" "backup"
intitle:"index of" "database"
```

**Login Portals:**
```
inurl:admin/login
inurl:wp-admin
inurl:phpmyadmin
intitle:"admin panel" login
intitle:"cPanel" login
site:example.com inurl:login
inurl:"/admin/config.php"
```

**Sensitive Documents:**
```
filetype:pdf site:example.com "confidential"
filetype:doc site:example.com "internal use only"
filetype:xlsx site:example.com "password"
filetype:csv site:example.com "email" "password"
ext:sql "INSERT INTO" "password"
filetype:log "password" "username"
filetype:env "DB_PASSWORD"
filetype:yml "password"
filetype:json "api_key"
```

**Exposed Credentials:**
```
intext:"password" filetype:conf
intext:"username" intext:"password" filetype:ini
filetype:env "SECRET_KEY"
filetype:env "AWS_ACCESS_KEY"
filetype:env "DATABASE_URL"
inurl:".git" "password"
intext:"BEGIN RSA PRIVATE KEY"
intext:"BEGIN OPENSSH PRIVATE KEY"
```

**API Keys and Secrets:**
```
intext:"api_key" filetype:env
intext:"secret_key" filetype:env
intext:"sk-" filetype:txt
intext:"AIza" filetype:json
intext:"AKIA" filetype:txt
intext:"SG." filetype:env
filetype:json "private_key_id"
```

**Exposed Databases:**
```
intitle:"MongoDB" "database" inurl:":28017"
intitle:"phpMyAdmin" "Welcome to phpMyAdmin"
intitle:"Elasticsearch" inurl:":9200"
intitle:"Kibana" inurl:":5601"
intitle:"Redis" inurl:":6379"
inurl:"/_utils" "CouchDB"
```

**Camera Feeds and IoT:**
```
inurl:"/view.shtml"
intitle:"Live View / - AXIS"
inurl:"CgiStart?page="
inurl:"viewerframe?mode="
intitle:"NetCam" inurl:"/viewer"
intitle:"WJ-NT104 Main Page"
inurl:"/webcapture.html"
intitle:"TENVIS" inurl:"/tmpfs/"
```

**Error Messages:**
```
intext:"sql syntax error" site:example.com
intext:"Warning: mysql_" site:example.com
intext:"Traceback (most recent call last)" site:example.com
intext:"Fatal error:" site:example.com
intext:"Parse error:" site:example.com
intext:"ODBC SQL Server Driver" site:example.com
```

**Vulnerable Files/Servers:**
```
filetype:php inurl:"phpinfo.php"
filetype:asp inurl:"error"
inurl:"/wp-config.php.bak"
inurl:"/config.php.bak"
filetype:log "SELECT" "FROM" "WHERE"
inurl:"/phpmyadmin/setup.php"
```

**Social Media Profiles:**
```
site:linkedin.com "Company Name" "engineer"
site:twitter.com "target" "email"
site:facebook.com "target name"
site:github.com "target" "password" OR "api_key"
site:pastebin.com "target.com" "password"
```

**Email and Contact Information:**
```
"@target.com" site:linkedin.com
"@target.com" filetype:pdf
"@target.com" filetype:xlsx
"@target.com" -www site:target.com
intext:"@target.com" "phone" OR "mobile"
```

---

### 4.3 GHDB Categories

The Google Hacking Database (maintained by OffSec at exploit-db.com) organizes dorks into 14 categories:

1. **Footholds** — Compromised/controlled system entry points
2. **Files Containing Usernames** — Exposed user account data
3. **Files Containing Passwords** — Credential files left exposed
4. **Sensitive Directories** — Directory listings that shouldn't be public
5. **Web Server Detection** — Server type/config identification
6. **Vulnerable Files** — Files with known vulnerabilities
7. **Vulnerable Servers** — Servers running vulnerable software
8. **Error Messages** — Verbose error output revealing internals
9. **Files Containing Juicy Info** — Sensitive documents accidentally indexed
10. **Sensitive Online Shopping Info** — E-commerce data leaks
11. **Network or Vulnerability Data** — Exposed network configs
12. **Pages Containing Login Portals** — Authentication pages discoverable
13. **Various Online Devices** — IoT devices, cameras, routers
14. **Advisories and Vulnerabilities** — CVEs and security bulletins

**Historical note:** Johnny Long coined "Googledork" around 2000 and popularized Google hacking. The GHDB was handed to OffSec in November 2010.

---

### 4.4 Advanced Dorking Techniques

**Combine multiple operators:**
```
site:example.com ext:sql | ext:dbf | ext:mdb
site:example.com inurl:admin | inurl:login | inurl:portal
site:example.com intitle:"index of" | intitle:"directory listing"
```

**Use with other search engines:**
- Bing: `site:` works, plus `ip:` for IP-based searches
- DuckDuckGo: Supports `site:`, `filetype:`, `intitle:`
- Shodan: Device-specific queries (see Network OSINT section)

**GitHub dorks:**
```
"target.com" password
"target.com" api_key
"target.com" secret
org:target "password" OR "api_key" OR "secret"
filename:.env "target.com"
```

---

## 5. Leaked Database Checks

### 5.1 Have I Been Pwned (HIBP)

**Website:** https://haveibeenpwned.com  
**API:** https://haveibeenpwned.com/api/v3

**Usage:**
```bash
# Check email against breaches
curl -H "hibp-api-key: YOUR_KEY" \
     -H "user-agent: YourApp" \
     "https://haveibeenpwned.com/api/v3/breachedaccount/test@example.com"

# Check with truncation (breach names only)
curl -H "hibp-api-key: YOUR_KEY" \
     -H "user-agent: YourApp" \
     "https://haveibeenpwned.com/api/v3/breachedaccount/test@example.com?truncateResponse=true"

# Check pastes
curl -H "hibp-api-key: YOUR_KEY" \
     -H "user-agent: YourApp" \
     "https://haveibeenpwned.com/api/v3/pasteaccount/test@example.com"
```

**Pricing:** API key required for breach/paste endpoints. Pwned Passwords is free.

---

### 5.2 DeHashed

**Website:** https://dehashed.com

**Features:**
- Search leaked/breached databases by email, username, IP, name, phone
- Supports wildcard searches
- Filter by specific breach
- API access for programmatic queries
- Requires paid subscription

**Search operators:**
```
email:target@example.com
username:targetuser
name:"John Doe"
ip:192.168.1.1
phone:+1234567890
domain:example.com
```

---

### 5.3 LeakCheck

**Website:** https://leakcheck.io

**Features:**
- Search by email, username, password hash, or domain
- API available for automated checks
- Shows breach name, date, and data types exposed
- Free tier with limited queries

---

### 5.4 Intelligence X (IntelX)

**Website:** https://intelx.io  
**API:** https://public.intelx.io/

**Data sources indexed:**
- Pastes (Pastebin, etc.)
- Darknet (Tor / I2P)
- Whois records
- Usenet archives
- Leaks and COMB (Compilation of Many Breaches)
- Stealer logs
- WikiLeaks archives
- Public leaks / Dumpster
- DNS records
- Sci-Hub

**Search selectors:**
- Email addresses
- Domains
- IP addresses
- CIDR ranges
- Phone numbers

**Advanced features:**
- Date range filtering
- Sort by relevance or date
- Media type filtering (PDFs, Word, Excel, Images, Pastes, etc.)
- Group similar results

**API tiers:**
| Tier | Lookups/Day |
|------|-------------|
| Free | 50 |
| Researcher | 200 |
| Paid/Pro | Higher limits + all PRO buckets |

**Phonebook.cz** — Companion tool for discovering URLs, email addresses, and domains (paid)

---

### 5.5 GitHub Credential Exposure

**Techniques for finding leaked credentials on GitHub:**

```bash
# Search for specific domain
github-dorker -d target.com -t "password OR api_key OR secret"

# Manual GitHub search
# Go to github.com/search and use:
"target.com" password
"target.com" api_key
"target.com" secret
"target.com" token
"target.com" credentials
org:target filename:.env
org:target filename:config.yml
org:target filename:credentials
```

**Tools:**
- **truffleHog** — Scans git repos for secrets
  ```bash
  pip install trufflehog
  trufflehog git https://github.com/target/repo
  ```

- **git-secrets** — Prevents secrets from being committed
  ```bash
  git secrets --install
  git secrets --scan
  ```

- **Gitleaks** — Scans git repos for secrets
  ```bash
  gitleaks detect --source . -v
  ```

- **GitLeaks** — Scan entire GitHub org
  ```bash
  gitleaks detect --source github.com/target --org
  ```

---

### 5.6 Paste Site Monitoring

**Techniques:**
```
# Search Pastebin via Google
site:pastebin.com "target.com"
site:pastebin.com "target@email.com"

# IntelX paste search
intelx search "target@email.com" -t pastes

# GitHub gist search
site:gist.github.com "target.com" "password"
```

**Tools for paste monitoring:**
- **PasteHunter** — Scans paste sites for content
- **Pastespider** — Automated paste site scraping
- **IntelX API** — Programmatic paste searching

---

## 6. Network/Infrastructure OSINT

### 6.1 Shodan

**Website:** https://shodan.io  
**Developer API:** https://developer.shodan.io

**Key search filters:**

| Filter | Purpose | Example |
|--------|---------|---------|
| `port:` | Open port | `port:22` |
| `product:` | Software name | `product:Apache` |
| `version:` | Software version | `version:2.4.41` |
| `os:` | Operating system | `os:"Windows 10"` |
| `country:` | Country code | `country:US` |
| `city:` | City name | `city:"New York"` |
| `org:` | Organization | `org:"Google"` |
| `hostname:` | Hostname | `hostname:.example.com` |
| `net:` | CIDR range | `net:192.168.0.0/16` |
| `asn:` | AS number | `asn:AS15169` |
| `http.title:` | Page title | `http.title:"Dashboard"` |
| `http.component:` | Web framework | `http.component:php` |
| `http.waf:` | Web firewall | `http.waf:"Cloudflare"` |
| `ssl.cert.issuer.cn:` | SSL issuer | `ssl.cert.issuer.cn:"Let's Encrypt"` |
| `has_screenshot:` | Has screenshot | `has_screenshot:true` |
| `has_vuln:` | Has vulnerability | `has_vuln:true` |
| `cloud.provider:` | Cloud provider | `cloud.provider:"AWS"` |

**Common Shodan queries:**
```
# Find cameras
product:"webcam" has_screenshot:true

# Find databases
port:27017 product:MongoDB
port:3306 product:MySQL
port:5432 product:PostgreSQL
port:6379 product:Redis
port:9200 product:Elasticsearch

# Find admin panels
http.title:"admin" http.status:200

# Find default credentials
"default password" http.title:"login"

# Find specific organization
org:"Target Company" has_screenshot:true

# Find IoT devices
product:"IoT" country:US

# Find RDP servers
port:3389

# Find exposed Jenkins
product:Jenkins

# Find exposed Grafana
product:Grafana

# Find VPN servers
product:"OpenVPN" port:1194
```

**Shodan Python API:**
```python
import shodan

api = shodan.Shodan("YOUR_API_KEY")

# Search
results = api.search("product:Apache country:US")
for result in results['matches']:
    print(f"IP: {result['ip_str']}")
    print(f"Port: {result['port']}")
    print(f"Org: {result.get('org', 'N/A')}")

# Host lookup
host = api.host("8.8.8.8")
print(f"OS: {host.get('os', 'Unknown')}")
for item in host['data']:
    print(f"Port: {item['port']} - {item.get('product', 'Unknown')}")
```

**API pricing:** $69-$359/month for API access

---

### 6.2 Censys

**Website:** https://search.censys.io  
**API:** https://api.censys.io

**Search query language:**
```
# Search hosts
services.port:443
services.http.response.html_title:"Dashboard"
ip:192.168.1.1
autonomous_system.asn:15169
location.country:"United States"

# Search certificates
parsed.subject.common_name:example.com
parsed.issuer.common_name:"Let's Encrypt"
```

**API endpoints:**
```
GET /v2/hosts/search
GET /v2/hosts/{ip}
GET /v1/data
```

**Free tier:** Limited queries, paid plans for expanded access

---

### 6.3 Subdomain Enumeration

**Subfinder** — Passive subdomain discovery:
```bash
# Installation
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest

# Basic usage
subfinder -d target.com

# Silent mode (only subdomains)
subfinder -d target.com -silent

# All sources
subfinder -d target.com -all

# JSON output
subfinder -d target.com -oJ results.json

# File output
subfinder -d target.com -o results.txt

# Specific sources
subfinder -d target.com -s crtsh,github,shodan

# From file of domains
subfinder -dL domains.txt

# With resolver
subfinder -d target.com -r 8.8.8.8,1.1.1.1

# Include sources in output
subfinder -d target.com -cs -oJ results.json

# List available sources
subfinder -ls

# Rate limiting
subfinder -d target.com -rl 100

# Max time
subfinder -d target.com -max-time 5
```

**Amass** — OWASP subdomain enumeration:
```bash
# Installation
go install -v github.com/owasp-amass/amass/v5/...@master

# Docker
docker pull owaspamass/amass

# Passive enumeration
amass enum -passive -d target.com

# Active enumeration
amass enum -active -d target.com

# With specific data sources
amass enum -d target.com -src

# Brute force
amass enum -brute -d target.com

# Output
amass enum -d target.com -o results.txt

# JSON output
amass enum -d target.com -json results.json

# Visualization
amass viz -d target.com
```

**Amass details:**
- Latest: v5.1.1 (April 2026)
- 14.6k stars, Apache 2.0 license
- Integrates with: WhoisXML API, certificate transparency, DNS databases
- Maltego integration available
- Both passive OSINT and active reconnaissance
- Docs: owasp-amass.github.io/docs

**Additional subdomain tools:**
```bash
# crt.sh (Certificate Transparency)
curl -s "https://crt.sh/?q=%25.target.com&output=json" | jq -r '.[].name_value' | sort -u

# Sublist3r
python3 sublist3r.py -d target.com

# Amass (OWASP)
amass enum -d target.com

# assetfinder
assetfinder --subs-only target.com

# findomain
findomain -t target.com

# knockpy
knockpy target.com
```

---

### 6.4 Port Scanning & Service Detection

**Nmap** — The standard network scanner:
```bash
# Basic scan
nmap target.com

# All ports
nmap -p- target.com

# Service version detection
nmap -sV target.com

# OS detection
nmap -O target.com

# Aggressive scan (OS, version, scripts, traceroute)
nmap -A target.com

# Fast scan (top 100 ports)
nmap -F target.com

# Specific ports
nmap -p 22,80,443,8080 target.com

# TCP SYN scan (stealth)
nmap -sS target.com

# UDP scan
nmap -sU target.com

# Script scan
nmap --script=vuln target.com

# Output formats
nmap -oN results.txt target.com    # Normal
nmap -oX results.xml target.com    # XML
nmap -oG results.gnmap target.com  # Greppable
nmap -oA results target.com        # All formats

# Scan from file
nmap -iL targets.txt

# Timing (T0=paranoid, T5=insane)
nmap -T4 target.com

# NSE scripts
nmap --script=http-title target.com
nmap --script=ssl-cert target.com
nmap --script=dns-brute target.com
nmap --script=http-enum target.com
```

---

### 6.5 Technology Identification

**WhatWeb** — Website technology fingerprinting:
```bash
# Installation
gem install whatweb

# Basic scan
whatweb target.com

# Verbose
whatweb -v target.com

# Aggressive scan
whatweb -a 3 target.com

# Heavy scan
whatweb -a 4 target.com

# JSON output
whatweb --log-json=results.json target.com

# XML output
whatweb --log-xml=results.xml target.com

# Proxy support
whatweb --proxy http://127.0.0.1:8080 target.com

# Tor support
whatweb --proxy socks5://127.0.0.1:9050 target.com

# Scan multiple targets
whatweb -i targets.txt

# Show Google dorks for plugins
whatweb --dorks target.com

# Specific plugins
whatweb -p wordpress,apache target.com

# Custom user agent
whatweb --user-agent "Mozilla/5.0..." target.com

# Threads
whatweb -t 50 target.com
```

**WhatWeb identifies:**
- CMS platforms (WordPress, Joomla, Drupal)
- JavaScript libraries (jQuery, React, Angular)
- Web servers (Apache, Nginx, IIS)
- Analytics (Google Analytics, Matomo)
- Security headers (HSTS, CSP, X-Frame-Options)
- Over 1,800 plugins for detection

**BuiltWith** — Website technology profiler:
- Website: https://builtwith.com
- Shows technology stack, frameworks, analytics, CDN, hosting
- Free tier with limited lookups

---

## 7. Geolocation OSINT

### 7.1 EXIF Data Extraction

**ExifTool** — The gold standard for metadata extraction:
```bash
# Read all metadata
exiftool photo.jpg

# GPS coordinates only
exiftool -GPS:All photo.jpg

# GPS in decimal degrees
exiftool -n -GPSLatitude -GPSLongitude photo.jpg

# Specific tags
exiftool -CreateDate -Make -Model photo.jpg

# Camera info
exiftool -Make -Model -Software photo.jpg

# All GPS with formatting
exiftool -c "%.6f degrees" -GPSLatitude -GPSLongitude photo.jpg

# Recursive directory scan
exiftool -r -GPS:All /path/to/photos/

# Filter for photos with GPS
exiftool -filename -if '$GPSLatitude' -r /path/to/photos/

# Export to CSV
exiftool -common -csv /path/to/photos/ > metadata.csv

# JSON output
exiftool -json /path/to/photos/

# Remove metadata (for privacy)
exiftool -all= photo.jpg

# Geotag from GPX track
exiftool -geotag track.gpx photo.jpg
```

**Key EXIF fields for geolocation:**
```
GPSLatitude         — Latitude coordinate
GPSLongitude        — Longitude coordinate
GPSAltitude         — Altitude above sea level
GPSTimeStamp        — Time of GPS fix
GPSDateStamp        — Date of GPS fix
GPSImgDirection     — Direction camera was facing
GPSDestBearing      — Bearing to destination
GPSMapDatum         — Geodetic survey data
```

**Other EXIF fields useful for OSINT:**
```
Make                — Camera manufacturer
Model               — Camera model
Software            — Software used to process
DateTime            — When photo was taken
DateTimeOriginal    — When shutter clicked
DateTimeDigitized   — When image was digitized
ImageWidth/Height   — Image dimensions
XResolution/YResolution — DPI
Artist              — Photographer name
Copyright           — Copyright info
UserComment         — User-added comments
LensModel           — Lens used
SerialNumber        — Camera serial number
OwnerName           — Camera owner name
```

---

### 7.2 Geolocation from Social Media

**Techniques:**
1. **Instagram geotags** — Posts tagged with locations
2. **Twitter/X location data** — Tweet geolocation (if enabled)
3. **Flickr** — Photo geolocation (often very precise)
4. **Facebook check-ins** — Location-based posts
5. **Snapchat Snap Map** — Public snaps on map
6. **Strava/fitness apps** — Activity routes and heatmaps

**Tools:**
- **Instaloader** — Extract geotags from Instagram posts (see Section 3.4)
- **Maltego** — Visual link analysis with geolocation transforms
- **Echosec** — Social media geolocation search (commercial)

---

### 7.3 IP Geolocation

**Services:**
```bash
# IPinfo
curl https://ipinfo.io/8.8.8.8
# Returns: city, region, country, loc (lat,lon), org, timezone

# IP-API
curl http://ip-api.com/json/8.8.8.8
# Returns: country, regionName, city, zip, lat, lon, isp, org, as

# MaxMind GeoLite2 (free, requires registration)
# Database download + geoiplookup tool

# IPStack
curl http://api.ipstack.com/8.8.8.8?access_key=YOUR_KEY

# Abstract API
curl https://ipgeolocation.abstractapi.com/v1/?api_key=YOUR_KEY&ip_address=8.8.8.8
```

**Python:**
```python
import requests
response = requests.get("https://ipinfo.io/8.8.8.8/json")
data = response.json()
print(f"City: {data['city']}")
print(f"Region: {data['region']}")
print(f"Country: {data['country']}")
print(f"Coordinates: {data['loc']}")
print(f"Organization: {data['org']}")
```

---

### 7.4 Geolocation Estimation Techniques

**From photos:**
1. Extract EXIF GPS data (if present)
2. Use visual clues (landmarks, signs, vegetation, architecture)
3. Google Street View comparison
4. Sun position analysis (shadow angles for time estimation)
5. Language/sign text identification

**From IP addresses:**
1. IP geolocation databases (MaxMind, IP2Location)
2. WHOIS data (registrant country/city)
3. BGP routing data (AS number to country mapping)
4. DNS resolver location (may indicate user location)

**GeoSpy** — AI-based photo geolocation:
- Website: https://geospy.ai
- Upload photo, get estimated location
- Uses machine learning for visual analysis

---

## 8. People Search Engines

### 8.1 Commercial People Search Sites

| Site | URL | Features |
|------|-----|----------|
| Pipl | pipl.com | Deep web people search, social profiles, contact info |
| Spokeo | spokeo.com | Name, address, phone, email, social profiles, relatives |
| WhitePages | whitepages.com | Address, phone, relatives, property records |
| BeenVerified | beenverified.com | Background checks, criminal records, contact info |
| TruthFinder | truthfinder.com | Background checks, dark web monitoring |
| Intelius | intelius.com | People search, background checks, reverse phone |
| PeopleFinder | peoplefinders.com | Address history, phone, relatives |
| Radaris | radaris.com | Public records, social profiles |
| ThatsThem | thatsthem.com | Free people search by name, email, phone, IP |
| FastPeopleSearch | fastpeoplesearch.com | Free people search with address and phone |

---

### 8.2 Public Records Searches

**Types of public records available:**
- Court records (criminal, civil, bankruptcy)
- Property records (deeds, mortgages, tax assessments)
- Business filings (incorporation, licenses)
- Voter registration records
- Marriage/divorce records
- Birth/death records
- Professional licenses
- UCC filings (secured transactions)

**Resources:**
- **PACER** (Public Access to Court Electronic Records) — Federal court records
- **State court websites** — Vary by state
- **County assessor websites** — Property records
- **Secretary of State websites** — Business filings
- **FOIA requests** — Government agency records

---

### 8.3 Free People Search Techniques

**Google search:**
```
"John Doe" "New York"
"John Doe" site:linkedin.com
"John Doe" "phone" OR "email" OR "address"
"John Doe" filetype:pdf
```

**Social media search:**
- Facebook: Search by name, location, workplace, school
- LinkedIn: Professional profiles with company and title
- Twitter/X: Bio and location data
- Instagram: Profile information

**Username correlation:**
- Use Sherlock/Maigret to find accounts from username
- Cross-reference found accounts for identity details

---

## 9. Company/Workplace OSINT

### 9.1 Finding Employees

**LinkedIn techniques:**
```
site:linkedin.com/in "Company Name"
site:linkedin.com/in "Company Name" "engineer"
site:linkedin.com/in "Company Name" "manager"
site:linkedin.com/in "Company Name" "director"
```

**Hunter.io:**
```bash
# Find email format for domain
curl "https://api.hunter.io/v2/domain-search?domain=target.com&api_key=YOUR_KEY"

# Returns: email pattern (e.g., {first}.{last}@target.com), employees, confidence scores
```

**TheHarvester:**
```bash
uv run theHarvester -d target.com -b linkedin
uv run theHarvester -d target.com -b hunter
```

---

### 9.2 Company Infrastructure

**Techniques:**
```bash
# Subdomain enumeration
subfinder -d target.com -silent
amass enum -passive -d target.com

# Technology stack
whatweb target.com
builtwith.com/target.com

# DNS records
dig target.com ANY
dig target.com MX
dig target.com TXT
dig target.com NS

# WHOIS
whois target.com

# SSL certificate details
echo | openssl s_client -connect target.com:443 2>/dev/null | openssl x509 -text

# Certificate Transparency
curl "https://crt.sh/?q=%25.target.com&output=json"

# Wayback Machine
web.archive.org/web/*/target.com
```

**Crunchbase:**
- Website: https://crunchbase.com
- Company funding, employees, acquisitions, competitors
- Free tier with limited access

**Glassdoor:**
- Website: https://glassdoor.com
- Employee reviews, salary data, interview questions
- Company culture insights

---

### 9.3 Email Format Discovery

**Common email patterns:**
```
{first}@domain.com              — john@target.com
{last}@domain.com               — doe@target.com
{first}.{last}@domain.com       — john.doe@target.com
{f}{last}@domain.com            — jdoe@target.com
{first}{l}@domain.com           — johnd@target.com
{first}_{last}@domain.com       — john_doe@target.com
{first}-{last}@domain.com       — john-doe@target.com
{last}.{first}@domain.com       — doe.john@target.com
{first}{last}@domain.com        — johndoe@target.com
```

**Discovery tools:**
- **Hunter.io** — Identifies email pattern + provides employee list
- **theHarvester** — Collects emails from multiple sources
- **Phonebook.cz** (IntelX) — Email discovery from domain
- **Clearbit Connect** — Gmail extension for email finding

---

## 10. Deep Web/Dark Web OSINT

### 10.1 Dark Web Search Engines

**Ahmia:**
- Clearnet: https://ahmia.fi
- Searches Tor hidden services (.onion)
- Open source (GitHub)
- Content policies against abuse material
- Submit hidden services to index

**Other dark web search engines:**
- **Torch** (xmh57jrknzkhv6y3ls3ubitzfqnkrwxhopf5aygthi7d6r4vk4no4id.onion)
- **DuckDuckGo** (duckduckgogg42xjoc72x3sjasowoarfbgcmvfimaftt6twagswzczad.onion)
- **Not Evil** — Dark web search engine
- **Haystak** — Large dark web index
- **Candle** — Google-like dark web search
- **Recon** — Dark web market search

---

### 10.2 Dark Web Monitoring

**Techniques for brand/person monitoring:**
1. **Tor hidden service directories** — Lists of .onion sites
2. **Dark web forums** — Monitor for leaked data, mentions
3. **Marketplace monitoring** — Track listings for stolen data
4. **Paste site monitoring** — Check for leaked credentials

**Tools and services:**
- **SpiderFoot** — Has Tor integration for dark web searching
  ```bash
  # SpiderFoot with Tor
  python3 ./sf.py -l 127.0.0.1:5001
  # Configure Tor proxy in settings: socks5://127.0.0.1:9050
  ```

- **IntelX** — Indexes darknet (Tor/I2P) content
  ```
  intelx search "target.com" -buckets darknet
  ```

- **Flare Systems** — Commercial dark web monitoring
- **Recorded Future** — Threat intelligence with dark web coverage
- **DarkOwl** — Dark web data provider

---

### 10.3 Dark Web Navigation

**Access requirements:**
- Tor Browser (https://www.torproject.org)
- I2P Router (https://geti2p.net)
- Tails OS (https://tails.net) for operational security

**Hidden service directories:**
- **The Hidden Wiki** — Directory of .onion sites
- **Daniel's Hosting** — List of active .onion services
- **Tor.taxi** — Dark web directory

**Safety considerations:**
- Never log into personal accounts over Tor
- Use burner accounts for dark web research
- Document findings without downloading illegal content
- Be aware of honeypots and exit node monitoring

---

## 11. OSINT Automation Frameworks

### 11.1 Recon-ng

**Metasploit-like interface for OSINT.**

```bash
# Installation
git clone https://github.com/lanmaster53/recon-ng
cd recon-ng
pip3 install -r REQUIREMENTS

# Docker
docker-compose up

# Usage
recon-ng
[recon-ng][default] > workspaces create target
[recon-ng][target] > marketplace search
[recon-ng][target] > marketplace install all
[recon-ng][target] > modules load recon/domains-hosts/hackertarget
[recon-ng][target] > options set SOURCE target.com
[recon-ng][target] > run
```

**Interfaces:**
- `recon-ng` — Interactive shell
- `recon-cli` — Command-line interface
- `recon-web` — Web interface

**License:** GPL-3.0 | **Stars:** 5.6k

---

### 11.2 SpiderFoot

**OSINT automation with 200+ modules.**

```bash
# Installation
wget https://github.com/smicallef/spiderfoot/archive/v4.0.tar.gz
tar zxvf v4.0.tar.gz
cd spiderfoot-4.0
pip3 install -r requirements.txt

# Run web UI
python3 ./sf.py -l 127.0.0.1:5001

# Docker
docker run -p 5001:5001 smicallef/spiderfoot:latest
```

**Supported target types:**
- IP addresses, domains/sub-domains, hostnames
- Network subnets (CIDR), ASN numbers
- Email addresses, phone numbers
- Usernames, person names
- Bitcoin addresses

**Module categories:**
- Free API, Tiered API, Commercial API, Internal (no API)
- Integrations: Shodan, HIBP, GreyNoise, AlienVault, SecurityTrails
- Cloud storage enumeration: S3, Azure Blob, DigitalOcean Spaces, Google Object Storage
- Threat intel: Abuse.ch, AbuseIPDB, AlienVault, CINS Army, PhishTank, Pulsedive
- DNS: crt.sh, CertSpotter, DNSDB, DNSDumpster, SecurityTrails
- Breach data: HIBP, Dehashed, LeakIX, Leak-Lookup, IntelX, PasteBin
- Dark web: Ahmia, Onion.link, Onionsearchengine.com
- Social media: Account Finder (500+ sites), Gravatar, Keybase, Hunter.io, Clearbit, FullContact
- Network: BGPView, Censys, Shodan, BinaryEdge, FullHunt, HackerTarget
- Crypto: Bitcoin finder, Blockchain balance, Etherscan, Ethereum address extractor

**Correlation engine:** YAML-configurable with 37 pre-defined rules (v4.0+)
**Internal extractors:** Email, phone, human name, Bitcoin/Ethereum, credit card, IBAN, company name, country, base64, hash extractors + DNS brute-forcer, port scanner, file metadata analyzer

**Export formats:** CSV, JSON, GEXF
**Backend:** SQLite
**License:** MIT | **Stars:** 17.9k | **Forks:** 3k

**SpiderFoot HX (commercial cloud):** Multi-user, attack surface monitoring, REST API, data feeds to Splunk/ElasticSearch, screenshotting, custom modules

---

### 11.3 Maltego

**Visual link analysis and investigation platform.**

**Products:**
- **Maltego Graph** — Deep investigation with link analysis
- **Maltego Search** — Quick OSINT searches
- **Maltego Monitor** — Real-time social media monitoring
- **Maltego Evidence** — Social media data preservation
- **Maltego Data** — 120+ data partners

**Key features:**
- Transforms (automated queries) from multiple data sources
- Graph visualization of relationships
- Integrations with VirusTotal, Splunk, Recorded Future, MISP
- Social media coverage: Facebook, X/Twitter, Instagram, TikTok, Snapchat, YouTube, VK
- Identity services: Constella Intelligence, PIPL, Epieos
- Corporate databases: Open Corporates, DomainTools

**Target users:** Law enforcement, cyber threat intelligence, corporate security, financial investigations

**Maltego technical details:**
- 200,000+ users worldwide
- 2,000+ government organizations
- 4,000+ private companies
- 60%+ of Dow 30 companies
- ISO 27001:2022 certified
- Frost & Sullivan 2025 Product Leadership Award
- Desktop client + web (app.maltego.com)
- Docs: docs.maltego.com
- Free Community Edition available

**Maltego Cases & Admin:**
- **Maltego Cases** — Store and cross-correlate investigations in one format
- **Maltego Admin** — Audit and analyze organization usage, billing, access authorization

---

## 12. Tool Installation Reference

### Quick Install Commands

```bash
# Python tools
pip3 install sherlock-project          # Sherlock
pip3 install maigret                   # Maigret
pip3 install holehe                    # Holehe
pip3 install instaloader               # Instaloader
pip3 install social-analyzer           # Social Analyzer
pip3 install phonenumbers              # Phone number library

# Go tools
go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install github.com/owasp-amass/amass/v5/...@master
go install github.com/sundowndev/phoneinfoga/v2/cmd/phoneinfoga@latest

# Ruby tools
gem install whatweb

# Nmap
apt install nmap                       # Debian/Ubuntu
brew install nmap                      # macOS

# theHarvester
git clone https://github.com/laramies/theHarvester
cd theHarvester && uv sync

# ExifTool
apt install libimage-exiftool-perl     # Debian/Ubuntu
brew install exiftool                  # macOS

# Recon-ng
git clone https://github.com/lanmaster53/recon-ng
cd recon-ng && pip3 install -r REQUIREMENTS

# SpiderFoot
pip3 install spiderfoot

# Docker alternatives
docker run -it --rm sherlock/sherlock
docker run -it sundowndev/phoneinfoga scan -n +1234567890
docker run soxoj/maigret:latest maigret user
docker run -p 5001:5001 smicallef/spiderfoot:latest
```

---

## 13. GitHub Dorks (Complete Reference)

**Source:** github.com/techgaun/github-dorks (Apache-2.0)

**Automation Tool:** github-dork.py uses github3.py to query GitHub Search API

```bash
export GH_TOKEN=your_github_token
python3 github-dork.py -r techgaun/github-dorks   # Single repo
python3 github-dork.py -u techgaun                  # All user repos
python3 github-dork.py -u dev-nepal                 # All org repos
```

### Private Keys and SSH Credentials
| Dork | Finds |
|------|-------|
| `extension:pem private` | Private keys in PEM files |
| `extension:ppk private` | PuTTYgen private keys |
| `filename:id_rsa or filename:id_dsa` | Private SSH keys |

### Database Credentials
| Dork | Finds |
|------|-------|
| `extension:sql mysql dump` | MySQL dump files |
| `extension:sql mysql dump password` | MySQL dumps with passwords |
| `filename:.pgpass` | PostgreSQL password files |
| `filename:robomongo.json` | MongoDB credentials |
| `rds.amazonaws.com password` | AWS RDS credentials |
| `filename:dbeaver-data-sources.xml` | DBeaver credential configs |

### Cloud Provider Keys
| Dork | Finds |
|------|-------|
| `filename:credentials aws_access_key_id` | AWS credentials |
| `filename:.s3cfg` | S3 configuration files |
| `extension:yaml cloud.redislabs.com` | Redis Labs credentials |

### Environment and App Configs
| Dork | Finds |
|------|-------|
| `filename:.env DB_USERNAME NOT homestead` | Laravel .env files |
| `filename:wp-config.php` | WordPress configs |
| `filename:settings.py SECRET_KEY` | Django secret keys |
| `filename:secrets.yml password` | Rails credentials |
| `filename:master.key path:config` | Rails master key |
| `filename:configuration.php JConfig password` | Joomla configs |

### API Keys and Tokens
| Dork | Finds |
|------|-------|
| `HEROKU_API_KEY language:shell` | Heroku API keys |
| `shodan_api_key language:python` | Shodan API keys |
| `xoxp OR xoxb` | Slack tokens |
| `"https://hooks.slack.com/services/"` | Slack webhooks |
| `"api_hash" "api_id"` | Telegram API tokens |
| `SF_USERNAME salesforce` | Salesforce credentials |

### Git, Shell History, and System Files
| Dork | Finds |
|------|-------|
| `filename:.git-credentials` | Git credentials |
| `filename:.bash_history` | Bash history with secrets |
| `filename:shadow path:etc` | Encrypted passwords |
| `filename:passwd path:etc` | User account info |
| `filename:filezilla.xml Pass` | FTP credentials |
| `filename:sftp.json path:.vscode` | VSCode SFTP credentials |

---

## 14. Expanded Shodan Filters

### Tracking Pixel Analysis (Link Related Websites)
| Filter | Purpose |
|--------|---------|
| `google_analytics` | Sites sharing a Google Analytics ID |
| `google_ads` | Sites sharing a Google Ads ID |
| `google_tag_manager` | Sites sharing GTM container |
| `meta_pixel` | Sites sharing Facebook Pixel ID |
| `tiktok_pixel` | Sites sharing TikTok Pixel ID |
| `x_pixel` | Sites sharing X/Twitter Pixel ID |

### Cloud Infrastructure
| Filter | Purpose |
|--------|---------|
| `cloud.provider` | AWS, Azure, GCP |
| `cloud.region` | Deployment region |
| `cloud.service` | Service type |

### SSL/TLS Certificate Intelligence
| Filter | Purpose |
|--------|---------|
| `ssl.cert.fingerprint` | Certificate fingerprint matching |
| `ssl.cert.issuer.cn` | Certificate issuer |
| `ssl.cert.subject.cn` | Certificate subject |
| `ssl.jarm` | JARM TLS server fingerprint |
| `ssl.ja3s` | JA3 server fingerprint |
| `ssl.cert.expired` | Expired certificates |

### Protocol-Specific Filters
- **SNMP:** `snmp.contact`, `snmp.location`, `snmp.name`
- **NTP:** `ntp.ip`, `ntp.ip_count`, `ntp.port`
- **Telnet:** `telnet.do`, `telnet.dont`, `telnet.will`, `telnet.wont`
- **SSH:** `ssh.hassh`, `ssh.type`
- **Bitcoin:** `bitcoin.ip`, `bitcoin.port`, `bitcoin.version`

---

## 15. WiGLE (Wireless Network Mapping)

**URL:** wigle.net | **API:** api.wigle.net (v2) | **Active since:** 2001

**Data:** WiFi networks with geolocation, Bluetooth devices, cell towers, signal quality, encryption tracking

**Search by:** SSID, BSSID (MAC), coordinates, date range

```bash
curl -H "Authorization: Basic BASE64" "https://api.wigle.net/api/v2/network/search?ssid=NetworkName"
curl -H "Authorization: Basic BASE64" "https://api.wigle.net/api/v2/network/search?netid=AA:BB:CC:DD:EE:FF"
```

---

## 16. Tool Comparison Matrix

### Username Discovery
| Tool | Sites | Stars | Unique Features |
|------|-------|-------|-----------------|
| Sherlock | 400+ | 83.6k | Classic, fast, simple |
| Maigret | 3,000+ | 29.8k | Recursive, AI analysis, Tor/I2P |
| social-analyzer | 1,000+ | 22.9k | OCR, screenshots, rating system |

### Email OSINT
| Tool | Method | Platforms |
|------|--------|-----------|
| holehe | Password recovery | 120+ |
| theHarvester | Passive collection | 45+ sources |
| Hunter.io | Domain search | API-based |

### Subdomain Enumeration
| Tool | Stars | Sources | Type |
|------|-------|---------|------|
| Subfinder | 13.7k | 30+ | Passive |
| Amass | 14.6k | 50+ | Passive + Active |
| theHarvester | 16.3k | 45+ | Passive |

### Automation Frameworks
| Tool | Modules | Interface | License |
|------|---------|-----------|---------|
| SpiderFoot | 200+ | Web UI, CLI | MIT |
| Recon-ng | 100+ | Console, CLI, Web | GPL-3.0 |
| Maltego | 120+ partners | GUI | Commercial |

---

## 17. API Quick Reference

| Service | Endpoint | Auth |
|---------|----------|------|
| HIBP | `https://haveibeenpwned.com/api/v3` | API Key header |
| Pwned Passwords | `https://api.pwnedpasswords.com/range/{hash}` | None |
| IntelX | `https://public.intelx.io/` | API Key |
| Shodan | `https://api.shodan.io/` | API Key query param |
| Hunter.io | `https://api.hunter.io/v2/` | API Key header |
| NumVerify | `http://apilayer.net/api/validate` | API Key query param |
| WiGLE | `https://api.wigle.net/api/v2/` | Basic Auth |
| ipinfo.io | `https://ipinfo.io/{ip}` | Token |
| Censys | `https://api.censys.io/` | API Key |

---

## 18. OSINT Methodology Checklist

### Phase 1: Passive Reconnaissance
- [ ] Google dorking for target information
- [ ] Email harvesting (theHarvester, Hunter.io)
- [ ] Subdomain enumeration (Subfinder, Amass)
- [ ] WHOIS and DNS analysis
- [ ] Certificate Transparency logs
- [ ] Social media enumeration (Sherlock, Maigret)
- [ ] Breach data checks (HIBP, DeHashed, IntelX)
- [ ] GitHub dorking for credentials
- [ ] Shodan/Censys infrastructure discovery

### Phase 2: Active Reconnaissance
- [ ] Port scanning (Nmap)
- [ ] Service identification (WhatWeb)
- [ ] Directory bruteforcing
- [ ] DNS bruteforcing
- [ ] Web application fingerprinting

### Phase 3: Analysis and Correlation
- [ ] Cross-reference findings across sources
- [ ] Build relationship maps
- [ ] Identify attack surface
- [ ] Document evidence with timestamps
- [ ] Generate actionable intelligence report

---

## Summary: OSINT Skill Categories for AI Agent

### Category 1: Email Intelligence
- **Tools:** holehe, theHarvester, email2phonenumber, Epieos, Hunter.io
- **Techniques:** Account discovery, breach checking, header analysis, owner identification
- **APIs:** HIBP v3, Hunter.io v2, NumVerify

### Category 2: Phone Intelligence
- **Tools:** PhoneInfoga, phonenumbers (Python), NumVerify API
- **Techniques:** Carrier lookup, location identification, social media correlation
- **APIs:** NumVerify, Abstract API, TrueCaller

### Category 3: Username/Social Media
- **Tools:** Sherlock, Maigret, Social Analyzer, Instaloader
- **Techniques:** Cross-platform account discovery, profile scraping, recursive search
- **Coverage:** 3,000+ sites (Maigret), 400+ (Sherlock), 1,000+ (Social Analyzer)

### Category 4: Google Dorking
- **Operators:** site, filetype, inurl, intitle, intext, before, after, cache
- **Categories:** 14 GHDB categories (OffSec)
- **Targets:** Directories, credentials, databases, cameras, login portals

### Category 5: Breach/Leak Detection
- **Tools:** HIBP, DeHashed, LeakCheck, IntelX, truffleHog, Gitleaks
- **Techniques:** Email breach checking, paste monitoring, GitHub credential scanning
- **APIs:** HIBP v3, IntelX public API

### Category 6: Network/Infrastructure
- **Tools:** Shodan, Censys, Nmap, Subfinder, Amass, WhatWeb
- **Techniques:** Port scanning, subdomain enumeration, technology fingerprinting
- **APIs:** Shodan API, Censys API

### Category 7: Geolocation
- **Tools:** ExifTool, GeoSpy, IPinfo, IP-API
- **Techniques:** EXIF extraction, IP geolocation, social media geotags, visual analysis
- **APIs:** IPinfo, IP-API, MaxMind GeoLite2

### Category 8: People Search
- **Sites:** Pipl, Spokeo, WhitePages, BeenVerified, Intelius
- **Techniques:** Public records, court records, property records, voter registration
- **Resources:** PACER, county assessor, secretary of state

### Category 9: Company/Workplace
- **Tools:** Hunter.io, Crunchbase, Glassdoor, LinkedIn, theHarvester
- **Techniques:** Employee discovery, email format identification, infrastructure mapping
- **APIs:** Hunter.io v2, Crunchbase API

### Category 10: Dark Web
- **Tools:** Ahmia, SpiderFoot, IntelX, Tor Browser
- **Techniques:** Hidden service search, forum monitoring, marketplace tracking
- **Directories:** Hidden Wiki, Daniel's Hosting, Tor.taxi

### Category 11: Automation Frameworks
- **Tools:** Recon-ng, SpiderFoot, Maltego
- **Features:** Modular architecture, 200+ data sources, visual analysis

---

## References

- OSINT Framework: https://osintframework.com
- Google Hacking Database: https://exploit-db.com/google-hacking-database
- Sherlock: https://github.com/sherlock-project/sherlock
- Maigret: https://github.com/soxoj/maigret
- Holehe: https://github.com/megadose/holehe
- PhoneInfoga: https://github.com/sundowndev/phoneinfoga
- theHarvester: https://github.com/laramies/theHarvester
- Subfinder: https://github.com/projectdiscovery/subfinder
- Amass: https://github.com/owasp-amass/amass
- WhatWeb: https://github.com/urbanadventurer/WhatWeb
- SpiderFoot: https://github.com/smicallef/spiderfoot
- Recon-ng: https://github.com/lanmaster53/recon-ng
- Instaloader: https://github.com/instaloader/instaloader
- Social Analyzer: https://github.com/qeeqbox/social-analyzer
- HIBP API: https://haveibeenpwned.com/API/v3
- Shodan: https://shodan.io
- Censys: https://search.censys.io
- IntelX: https://intelx.io
- Hunter.io: https://hunter.io/api
- ExifTool: https://exiftool.org
- Maltego: https://maltego.com

---

*Report compiled by Bauna Intern for skills-for-agents OSINT skill development.*  
*Co-Authored-By: Bauna Intern <bauna-intern@shaurya.dev>*  
*© 2025 IsNoobGrammer. All Rights Reserved.*
