# OSINT Techniques Comprehensive Survey

**Research Date:** 2026-05-21
**Purpose:** Comprehensive OSINT skill building for AI agents
**Scope:** 10 major OSINT categories with tools, techniques, commands, APIs, and methods

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

---

## 1. Email OSINT

### 1.1 Finding Social Media Accounts from Email

**Holehe** — Checks if email is registered on 120+ websites by leveraging password recovery and registration flows. Does NOT alert the target.

```bash
# Installation
pip3 install holehe

# CLI Usage
holehe test@gmail.com

# Docker
docker build . -t my-holehe-image
docker run my-holehe-image holehe test@gmail.com
```

**Python API:**
```python
import trio
import httpx
from holehe.modules.social_media.snapchat import snapchat

async def check_email():
    client = httpx.AsyncClient()
    out = []
    await snapchat("target@email.com", client, out)
    print(out)  # [{'name': 'snapchat', 'rateLimit': False, 'exists': True/False, ...}]
    await client.aclose()

trio.run(check_email)
```

**Module Output Format:**
- `name` — service name
- `rateLimit` — whether rate-limited
- `exists` — whether account exists for that email
- `emailrecovery` — partially obfuscated recovery email
- `phoneNumber` — partially obfuscated recovery phone
- `others` — additional info

**Detection Methods:**
1. Registration endpoint checks (~90+ sites)
2. Login endpoint checks (Amazon, Snapchat, Yahoo)
3. Password recovery (Adobe, mail.ru, Odnoklassniki)
4. Other methods (Gravatar, Office365, Protonmail)

**Supported Platforms (120+):**
- Social: Twitter, Instagram, Snapchat, Tumblr, Pinterest, Discord
- Developer: GitHub, Docker, Replit, CodePen, Codecademy
- Commerce: Amazon, eBay, Venmo, Deliveroo
- Entertainment: Spotify, SoundCloud, Wattpad, Last.fm
- Productivity: Evernote, LastPass, WordPress

**Maltego Integration:** holehe-maltego for visual link analysis

---

### 1.2 Checking Data Breaches

**Have I Been Pwned (HIBP) API v3:**

```bash
# Check single email
curl -H "hibp-api-key: YOUR_API_KEY" \
  "https://haveibeenpwned.com/api/v3/breachedaccount/test@example.com"

# Check with truncated response (k-anonymity)
curl "https://api.pwnedpasswords.com/range/XXXXX"  # First 5 chars of SHA1 hash

# Get all breaches
curl "https://haveibeenpwned.com/api/v3/breaches"

# Get single breach
curl "https://haveibeenpwned.com/api/v3/breach/BreachName"

# Get all data classes
curl "https://haveibeenpwned.com/api/v3/dataclasses"

# Stealer logs for email
curl -H "hibp-api-key: YOUR_API_KEY" \
  "https://haveibeenpwned.com/api/v3/stealerlogsbyemail/test@example.com"
```

**API Requirements:**
- API key required (obtained from account.hibp-api-key.com)
- User-Agent header required
- Rate limiting applies
- Breached account search requires paid API key

**DeHashed** — Search engine for leaked credentials. Requires registration. Supports search by email, username, IP address, name, phone, domain.

**LeakCheck:**
- 7+ billion records
- Plans from $2.99/day (15 lookups) to $69.99 lifetime (400/day)
- Enterprise: unlimited lookups, reverse password search, domain monitoring
- API access on all tiers
- Telegram bot available
- Search by email, username, keyword, domain, password

**IntelX (Intelligence X):**
- Search engine for leaked data, dark web, paste sites
- API available
- Search by email, phone, domain, IP, URL, Bitcoin address
- Archives of leaked data and paste sites

---

### 1.3 Finding Email Owner Information

**theHarvester** — Gathers names, emails, IPs, subdomains, URLs from 40+ public sources.

```bash
# Installation
curl -LsSf https://astral.sh/uv/install.sh | sh
git clone https://github.com/laramies/theHarvester
cd theHarvester
uv sync

# Usage
uv run theHarvester -d example.com -b all
uv run theHarvester -d example.com -b google,bing,yahoo
uv run theHarvester -d example.com -b hunter -l 200
```

**Data Sources (40+):**
- Search Engines: Baidu, Brave, DuckDuckGo, Yahoo, Mojeek, FOFA, ZoomEye
- Certificate/SSL: Censys, CertSpotter, crt.sh, BufferOverUn
- DNS/Domain: DNSDumpster, RapidDNS, SecurityTrails, SubdomainCenter
- Breach/Leak: DeHashed, HaveIBeenPwned, LeakIX, LeakLookup
- Email Discovery: Hunter, RocketReach, Tomba
- Code Search: GitHub code search
- Threat Intelligence: CriminalIP, IntelX, SecurityScorecard, VirusTotal

**Hunter.io** — Find professional email addresses by domain.

```bash
# API usage
curl "https://api.hunter.io/v2/domain-search?domain=example.com&api_key=YOUR_KEY"

# Email finder
curl "https://api.hunter.io/v2/email-finder?domain=example.com&first_name=John&last_name=Doe&api_key=YOUR_KEY"

# Email verifier
curl "https://api.hunter.io/v2/email-verifier?email=john@example.com&api_key=YOUR_KEY"
```

**Free tier:** 50 searches/month, 25 verifications/month

---

### 1.4 Email Header Analysis

**Techniques:**
1. Extract `Received:` headers to trace email path
2. Parse `X-Originating-IP` for sender IP
3. Check `Authentication-Results` for SPF/DKIM/DMARC
4. Analyze `Message-ID` for originating server
5. Extract `X-Mailer` for client information
6. Check `Return-Path` vs `From` for spoofing

**Tools:**
- MXToolbox Header Analyzer (online)
- Google Admin Toolbox Messageheader
- mailheader.org
- Python `email` stdlib module for programmatic parsing

**Header Fields of Interest:**
```
Received: from mail-server.example.com (IP) by recipient-server
X-Originating-IP: [sender-ip]
X-Mailer: Microsoft Outlook 16.0
Authentication-Results: spf=pass dkim=pass dmarc=pass
Message-ID: <unique-id@mail-server.com>
Return-Path: <sender@example.com>
```

---

### 1.5 Email OSINT Tools Summary

| Tool | Purpose | Key Feature |
|------|---------|-------------|
| holehe | Email to registered accounts | 120+ sites, no alert to target |
| theHarvester | Email/domain enumeration | 40+ data sources |
| email2phonenumber | Email to phone number | Password reset scraping |
| Infoga | Email OSINT | Multiple data sources |
| Hunter.io | Professional email finder | Domain search, email verifier |
| HIBP API | Breach checking | 14+ billion accounts indexed |
| DeHashed | Leaked credential search | Reverse lookups |
| LeakCheck | Breach search | 7B+ records, API access |

---

## 2. Phone Number OSINT

### 2.1 PhoneInfoga

Advanced phone number scanning tool. Written in Go. REST API + Web UI.

```bash
# Docker installation
docker pull sundowndev/phoneinfoga
docker run -p 8080:8080 sundowndev/phoneinfoga serve

# CLI usage
phoneinfoga scan -n +1234567890
phoneinfoga serve  # Starts web UI on :8080
```

**Capabilities:**
- Validates phone number existence
- Collects country, line type, carrier info
- OSINT footprinting via external APIs, phone books, search engines
- Reputation reports and social media presence checks
- Disposable number database checks
- REST API with Swagger documentation
- Web GUI for browser-based scanning

**Status:** Stable but unmaintained (v2.11.0, Feb 2024)

---

### 2.2 NumVerify API

```bash
# Phone number validation and carrier lookup
curl "http://apilayer.net/api/validate?access_key=YOUR_KEY&number=14158586273"
```

**Response includes:**
- `valid` — boolean
- `local_format` / `international_format`
- `country_prefix`, `country_code`, `country_name`
- `location` — city/region
- `carrier` — telecom provider
- `line_type` — mobile, landline, voip, etc.

**Free tier:** 100 requests/month

---

### 2.3 TrueCaller API

Reverse phone lookup service with crowdsourced caller ID.

**API endpoints:**
- Search by phone number
- Returns: name, address, carrier, spam score
- Requires authentication (Google/TrueCaller login)

**Alternative approaches:**
- Sync.me — crowdsourced caller ID
- Numspy — phone number lookup
- CallerID API — reverse lookup service

---

### 2.4 Finding Social Media from Phone Number

**Techniques:**
1. Use holehe with phone number (some sites support phone-based checks)
2. Search phone number on social platforms directly (Facebook, LinkedIn)
3. Use WhatsApp profile picture retrieval tools
4. Check Telegram user info via phone number
5. Use Viber user lookup

**Phone to Social Media Tools:**
- phoneinfoga — social media presence checks
- social-analyzer — supports phone-based searches on some platforms
- Manual platform searches (Facebook, LinkedIn phone search)

---

### 2.5 Phone Number Carrier/Location/Type Detection

```python
# Using phonenumbers library (Python)
import phonenumbers
from phonenumbers import carrier, geocoder, timezone

number = phonenumbers.parse("+14158586273", None)
print(carrier.name_for_number(number, "en"))  # Carrier name
print(geocoder.description_for_number(number, "en"))  # Location
print(timezone.time_zones_for_number(number))  # Timezone
print(phonenumbers.is_valid_number(number))  # Validity
print(phonenumbers.number_type(number))  # Type (mobile/landline)
```

**npm equivalent:** `libphonenumber-js`

---

## 3. Username/Social Media OSINT

### 3.1 Sherlock

Hunt down social media accounts by username across 400+ social networks.

```bash
# Installation
pipx install sherlock-project
# or
pip install sherlock-project
# or Docker
docker run -it --rm sherlock/sherlock

# Single username
sherlock user123

# Multiple usernames
sherlock user1 user2 user3

# Limit to specific sites
sherlock --site twitter --site instagram user123

# Export results
sherlock --csv user123
sherlock --xlsx user123
sherlock --json results.json user123

# With proxy
sherlock --proxy socks5://127.0.0.1:1080 user123

# Show all results (including not found)
sherlock --print-all user123

# Open results in browser
sherlock --browse user123

# Include NSFW sites
sherlock --nsfw user123

# Timeout setting
sherlock --timeout 30 user123

# Wildcard variants
sherlock "user{?}name"  # checks user_name, user-name, user.name
```

**Output:** Results saved to `username.txt` with found profile URLs.

**v0.16.0** — Latest release (Sep 2025), 83.6k stars

---

### 3.2 Maigret

Collects dossier on a person by username only. Checks 3,000+ sites. No API keys required.

```bash
# Installation
pip install maigret

# Basic usage
maigret username

# HTML report
maigret user --html

# PDF report
maigret user --pdf

# JSON output
maigret user --json ndjson

# CSV export
maigret user --csv

# Interactive graph
maigret user --graph

# Filter by tags
maigret user --tags photo,dating

# Multiple users, all sites
maigret user1 user2 user3 -a

# AI analysis (requires OpenAI-compatible API)
maigret user --ai

# Parse specific profile URL
maigret --parse https://example.com/profile

# Generate username permutations
maigret --permute "John Doe"

# Web interface
maigret --web 5000  # Then open http://127.0.0.1:5000

# With Tor
maigret user --tor-proxy socks5://127.0.0.1:9050

# Cloudflare bypass (experimental)
maigret user --cloudflare-bypass
```

**Key Features:**
- 3,000+ sites (500 checked by default, use `-a` for all)
- Extracts account owner info from profiles and APIs
- Recursive search using discovered usernames/IDs
- Tag filtering (categories, countries)
- Detects and partially bypasses blocks/CAPTCHA
- Auto-updates site database (once per 24 hours)
- Works with Tor and I2P websites
- Web interface with graph visualization
- Standalone Windows exe available

---

### 3.3 Social Analyzer

API, CLI, and Web App for finding person's profile across 1,000+ social media sites.

```bash
# Python package
pip3 install social-analyzer
python3 -m social-analyzer --username "johndoe" --metadata

# Node.js CLI
nodejs app.js --username "johndoe"
nodejs app.js --username "johndoe,janedoe" --metadata --top 100

# Web app
npm install && npm start  # Access at http://0.0.0.0:9005/app.html
```

**Detection Methods:**
- String & name analysis with permutations
- HTTPS library requests + browser-based (Selenium) checks
- Multilayer detections: OCR, normal, advanced, special
- Metadata & pattern extraction
- Search engine lookups (Google API, DuckDuckGo API)

**Analysis Modes:**
- `FindUserProfilesFast` — quick check
- `FindUserProfilesSlow` — thorough check
- `FindUserProfilesSpecial` — special detections for Facebook, Gmail, Google

**Output:** Confidence scores 0-100 for each result

---

### 3.4 Twint (Twitter/X OSINT — Archived)

Twitter scraping tool. No authentication, no API, no limits. (Archived March 2023)

```bash
# Installation
git clone --depth=1 https://github.com/twintproject/twint.git
cd twint
pip3 install . -r requirements.txt

# Scrape user tweets
twint -u username

# Search tweets
twint -s "search term"

# User + search
twint -u username -s "keyword"

# Date filter
twint -u username --since "2023-01-01"

# Export
twint -u username -o output.csv --csv
twint -u username -o output.json --json

# Find contact info
twint -u username --email --phone

# Follower/following lists
twint -u username --followers
twint -u username --following

# Favorites
twint -u username --favorites

# Timeline (including retweets)
twint -u username --timeline

# Geolocation scraping
twint -g="48.880048,2.385939,1km" -o file.csv --csv

# Elasticsearch output
twint -u username -es localhost:9200
```

**Python API:**
```python
import twint

c = twint.Config()
c.Username = "target"
c.Search = "keyword"
c.Limit = 100
c.Store_csv = True
c.Output = "results.csv"
twint.run.Search(c)
```

---

### 3.5 Instaloader (Instagram OSINT)

```bash
# Installation
pip3 install instaloader

# Download all posts from profile
instaloader profile target_username

# Fast update (skip already downloaded)
instaloader --fast-update profile target_username

# Download stories
instaloader --stories target_username

# Download with login (for private profiles you follow)
instaloader --login=your_username profile target_username

# Download comments and geotags
instaloader --comments --geotags profile target_username

# Download highlights
instaloader --highlights target_username

# Download tagged posts
instaloader --tagged target_username

# Download reels
instaloader --reels target_username

# Download by hashtag
instaloader "#hashtag"

# Download feed
instaloader :feed
```

---

### 3.6 Osintgram (Instagram OSINT — Interactive)

```bash
# Installation
git clone https://github.com/Datalux/Osintgram.git
cd Osintgram
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Configure Instagram credentials in config/credentials.ini

# Interactive mode
python3 main.py target_username

# Direct command
python3 main.py target_username --command info
```

**Commands:**
| Command | Description |
|---------|-------------|
| `addrs` | Registered addresses from target photos |
| `captions` | Photo captions |
| `comments` | Total comments on posts |
| `followers` / `followings` | Follower/following lists |
| `fwersemail` / `fwingsemail` | Emails from followers/following |
| `fwersnumber` / `fwingsnumber` | Phone numbers from followers/following |
| `hashtags` | Hashtags used by target |
| `info` | Account information |
| `likes` | Total likes on posts |
| `mediatype` | Post types (photo/video) |
| `photos` / `propic` / `stories` | Download media |
| `tagged` | Users tagged by target |
| `wcommented` / `wtagged` | Who commented/tagged the target |

---

## 4. Google Dorks for OSINT

### 4.1 Core Operators

| Operator | Purpose | Example |
|----------|---------|---------|
| `site:` | Restrict to specific domain | `site:example.com` |
| `filetype:` | Filter by file extension | `filetype:pdf` |
| `ext:` | Same as filetype | `ext:sql` |
| `inurl:` | Text in URL | `inurl:admin` |
| `intitle:` | Text in page title | `intitle:"index of"` |
| `intext:` | Text in page body | `intext:"password"` |
| `allintext:` | All words in body | `allintext:admin password` |
| `allinurl:` | All words in URL | `allinurl:admin login` |
| `allintitle:` | All words in title | `allintitle:admin panel` |
| `cache:` | Cached version of page | `cache:example.com` |
| `link:` | Pages linking to URL | `link:example.com` |
| `related:` | Related sites | `related:example.com` |
| `numrange:` | Number range | `numrange:1000-2000` |
| `daterange:` | Date range (Julian) | `daterange:2459580-2459640` |
| `before:` | Before date | `before:2024-01-01` |
| `after:` | After date | `after:2023-01-01` |
| `info:` | Info about a page | `info:example.com` |
| `define:` | Definition of term | `define:osint` |
| `*` | Wildcard | `"password * admin"` |
| `""` | Exact phrase | `"confidential document"` |
| `OR` | Boolean OR | `admin OR administrator` |
| `-` | Exclude term | `admin -site:google.com` |
| `..` | Number range | `"year 2020..2024"` |

---

### 4.2 Dorks for Exposed Databases and Admin Panels

```
# Admin panels
site:example.com inurl:admin
site:example.com inurl:login
site:example.com intitle:"admin panel"
site:example.com intitle:"dashboard"
site:example.com inurl:cpanel
site:example.com inurl:phpmyadmin
site:example.com intitle:"phpMyAdmin"
site:example.com inurl:wp-admin

# Database files
filetype:sql "INSERT INTO" "password"
filetype:sql "CREATE TABLE" "username"
filetype:sql inurl:backup
filetype:bak inurl:backup
filetype:mdb inurl:database
filetype:db inurl:backup

# Exposed config files
filetype:env "DB_PASSWORD"
filetype:env "SECRET_KEY"
filetype:conf inurl:config
filetype:yml "password"
filetype:xml inurl:config "password"
filetype:ini "password"
filetype:cfg "password"
```

---

### 4.3 Dorks for Sensitive Documents

```
# PDF documents
filetype:pdf "confidential"
filetype:pdf "not for distribution"
filetype:pdf "internal use only"
filetype:pdf "restricted"
filetype:pdf site:example.com

# Word documents
filetype:doc "confidential"
filetype:docx "internal"
filetype:doc "password"

# Spreadsheets
filetype:xlsx "email" "password"
filetype:csv "email" "phone"
filetype:xls "username" "password"
filetype:xlsx "ssn" "social security"

# Presentations
filetype:ppt "internal"
filetype:pptx "confidential"

# Text files
filetype:txt "password"
filetype:log "password"
filetype:log "error" "failed login"
```

---

### 4.4 Dorks for Login Pages and Authentication

```
# Login pages
intitle:"login" inurl:login
intitle:"sign in" inurl:signin
intitle:"log in" inurl:login
intitle:"admin login"
intitle:"portal login"
inurl:login.php
inurl:login.jsp
inurl:login.asp

# Password reset
intitle:"forgot password"
intitle:"reset password"
inurl:password-reset
inurl:forgot-password

# Default credentials
intitle:"default password"
"default password" filetype:pdf
"default credentials" inurl:admin
```

---

### 4.5 Dorks for Exposed API Keys and Credentials

```
# API keys
intext:"api_key" filetype:env
intext:"api_secret" filetype:env
intext:"apikey" filetype:json
intext:"sk-" filetype:env
intext:"AKIA" filetype:env  # AWS keys
intext:"AIza" filetype:env  # Google API keys

# AWS credentials
intext:"AKIAIOSFODNN7EXAMPLE"
intext:"aws_access_key_id"
intext:"aws_secret_access_key"
filetype:pem "PRIVATE KEY"

# Database credentials
intext:"DB_PASSWORD" filetype:env
intext:"DATABASE_URL" filetype:env
intext:"MONGO_URI" filetype:env
intext:"REDIS_URL" filetype:env

# GitHub secrets
site:github.com "password"
site:github.com "api_key"
site:github.com "secret_key"
site:github.com "token"
site:github.com "BEGIN RSA PRIVATE KEY"
site:github.com "BEGIN OPENSSH PRIVATE KEY"

# GitLab secrets
site:gitlab.com "password"
site:gitlab.com "api_key"
```

---

### 4.6 Dorks for Camera Feeds and IoT Devices

```
# IP cameras
intitle:"webcam" inurl:viewer
intitle:"camera" inurl:view
intitle:"live view" inurl:camera
inurl:viewer?mode=real
inurl:axis-cgi/mjpg
inurl:oneshotimage
intitle:"IP Camera" inurl:main

# IoT devices
intitle:"router" inurl:status
intitle:"NAS" inurl:login
intitle:"printer" inurl:status
intitle:"switch" inurl:config

# Specific brands
inurl:"/cgi-bin/guestimage.html"  # Panasonic cameras
inurl:"/tmp/snap.jpg"  # Various IP cameras
intitle:"Blue Iris" inurl:login  # Blue Iris DVR
```

---

### 4.7 Dorks for Social Media and Contact Info

```
# Email addresses
"@gmail.com" filetype:csv
"@yahoo.com" filetype:xlsx
"email" "password" filetype:csv
intext:"@example.com" site:pastebin.com

# Phone numbers
intext:"phone" filetype:xlsx
intext:"+1" filetype:csv

# Social media profiles
site:linkedin.com "company name"
site:twitter.com "target"
site:facebook.com "target"

# Employee lists
site:example.com filetype:xlsx "employee"
site:example.com filetype:csv "staff"
"employee list" filetype:xlsx
"staff directory" filetype:pdf
```

---

### 4.8 GHDB Categories (Google Hacking Database)

1. **Footholds** — Entry points into systems
2. **Files Containing Usernames** — User enumeration files
3. **Sensitive Directories** — Exposed directory listings
4. **Web Server Detection** — Server identification
5. **Vulnerable Files** — Files with known vulnerabilities
6. **Vulnerable Servers** — Servers with known issues
7. **Error Messages** — Information leakage via errors
8. **Files Containing Juicy Info** — Sensitive data files
9. **Files Containing Passwords** — Credential files
10. **Sensitive Shopping Info** — E-commerce data exposure
11. **Network or Vulnerability Data** — Network configuration leaks
12. **Pages Containing Login Portals** — Authentication pages
13. **Various Online Devices** — IoT and embedded devices
14. **Advisories and Vulnerabilities** — Security advisories

**Associated Tags:** WordPress, SQL Injection (SQLi), XSS, LFI/RFI, CSRF, DoS, Code Injection, Command Injection, Authentication Bypass, SSRF, XXE, Race Condition, Buffer Overflow

---

## 5. Leaked Database Checks

### 5.1 Have I Been Pwned (HIBP)

**API Endpoints:**
```
GET /api/v3/breachedaccount/{account}     — Check email for breaches
GET /api/v3/breaches                       — All breaches in system
GET /api/v3/breach/{name}                  — Single breach details
GET /api/v3/dataclasses                    — All data classes
GET /api/v3/pasteaccount/{account}         — Paste searches for email
GET /api/v3/stealerlogsbyemail/{email}     — Stealer logs for email
GET /api/v3/stealerlogsbywebsitedomain/{domain} — Stealer logs for domain
```

**Password Check (k-anonymity):**
```bash
# Get SHA1 hash of password, send first 5 chars
curl "https://api.pwnedpasswords.com/range/5BAA6"
# Response: list of hash suffixes with counts
```

**Requirements:**
- API key required for breached account search
- User-Agent header required
- Rate limiting applies

---

### 5.2 DeHashed

- Search engine for leaked credentials
- Supports: email, username, IP, name, phone, domain, password
- Reverse lookups available
- API access for automation
- Requires registration

---

### 5.3 LeakCheck

| Plan | Price | Lookups |
|------|-------|---------|
| Basic | $2.99/day | 15 emails |
| Monthly | $9.99/month | 200 emails/usernames/day |
| Lifetime | $69.99 one-time | 400 emails/usernames/day |
| Enterprise | From $179/quarter | Unlimited |

**Features:**
- 7+ billion records
- Instant search (~1 second)
- Bulk check (100,000 lines)
- Search by email, username, keyword, domain, password
- Telegram bot access
- API on all tiers
- No-log policy

---

### 5.4 Intelligence X (IntelX)

- Search engine for leaked data, dark web, paste sites
- Archives of leaked data
- API available
- Search by: email, phone, domain, IP, URL, Bitcoin address
- Integration with other OSINT tools

---

### 5.5 Paste Site Monitoring

**Techniques:**
1. Search Pastebin via Google: `site:pastebin.com "target@email.com"`
2. Use IntelX paste search API
3. Monitor paste sites with RSS feeds
4. Use dedicated paste monitoring services

**Tools:**
- PasteHunter — paste site scanner
- PhishTank — phishing URL database
- IntelX paste search

---

### 5.6 GitHub Credential Exposure

**Google Dorks:**
```
site:github.com "target.com" "password"
site:github.com "target.com" "api_key"
site:github.com "target.com" "secret"
site:github.com "target.com" "token"
site:github.com "target.com" "BEGIN RSA PRIVATE KEY"
site:github.com "target.com" "aws_access_key_id"
site:github.com "target.com" "AKIA"
```

**Tools:**
- **TruffleHog** — scans git repos for secrets
- **GitLeaks** — scans git repos for credentials
- **GitRob** — scans GitHub orgs for sensitive files
- **detect-secrets** — Yelp's secret detection tool

```bash
# TruffleHog
pip install trufflehog
trufflehog git https://github.com/target/repo

# GitLeaks
gitleaks detect --source /path/to/repo
```

---

## 6. Network/Infrastructure OSINT

### 6.1 Shodan

Search engine for Internet-connected devices.

```python
# Python library
pip install shodan

from shodan import Shodan
api = Shodan('YOUR_API_KEY')

# Host lookup
host = api.host('8.8.8.8')
print(host['os'], host['ports'], host['vulns'])

# Search
for banner in api.search_cursor('http.title:"hacked by"'):
    print(banner)

# Count results
count = api.count('tag:ics')

# Exploit search
exploits = api.exploits.search('apache')
```

**CLI:**
```bash
shodan init YOUR_API_KEY
shodan search "apache country:US"
shodan host 8.8.8.8
shodan scan submit 8.8.8.8
shodan stats --facets country port
shodan download results "apache country:US"
shodan parse results.json.gz
```

**Key Search Filters:**
- `port:` — specific port
- `country:` — country code
- `city:` — city name
- `org:` — organization
- `hostname:` — hostname
- `os:` — operating system
- `net:` — CIDR range
- `tag:` — tags (ics, iot, etc.)
- `vuln:` — CVE vulnerability
- `http.title:` — page title
- `ssl.cert.subject.cn:` — SSL certificate common name
- `product:` — software product
- `version:` — software version

---

### 6.2 Censys

Internet-wide scanning platform.

```python
# Installation
pip install censys

# Configuration
censys config  # Set CENSYS_API_ID and CENSYS_API_SECRET

# CLI
censys search "services.http.response.html_title: 'Dashboard'"
censys view 8.8.8.8
censys subdomains example.com
```

**Python API:**
```python
from censys.search import CensysHosts

h = CensysHosts()
for host in h.search("services.http.response.html_title: 'Dashboard'"):
    print(host)
```

**Capabilities:**
- Search internet-wide scan datasets
- Bulk certificate lookups
- Download bulk data
- Attack Surface Management (ASM)
- Asset, event, and seed management

---

### 6.3 Nmap

Network scanning and service detection.

```bash
# Basic scan
nmap target.com

# Port range scan
nmap -p 1-65535 target.com

# Service version detection
nmap -sV target.com

# OS detection
nmap -O target.com

# Aggressive scan (all)
nmap -A target.com

# Stealth scan
nmap -sS target.com

# UDP scan
nmap -sU target.com

# Script scan
nmap --script vuln target.com

# Output formats
nmap -oN output.txt target.com  # Normal
nmap -oX output.xml target.com  # XML
nmap -oG output.gnmap target.com  # Grepable
nmap -oA output target.com  # All formats

# Scan network range
nmap 192.168.1.0/24

# Exclude hosts
nmap 192.168.1.0/24 --exclude 192.168.1.1

# Timing templates
nmap -T4 target.com  # Aggressive timing
nmap -T0 target.com  # Paranoid (IDS evasion)
```

**NSE Scripts:**
```bash
# Vulnerability scripts
nmap --script vuln target.com

# Discovery scripts
nmap --script discovery target.com

# Safe scripts
nmap --script safe target.com

# Specific scripts
nmap --script http-enum target.com
nmap --script ssl-enum-ciphers target.com
nmap --script smb-enum-shares target.com
```

---

### 6.4 Subdomain Enumeration

**Amass (OWASP):**
```bash
# Installation
go install -v github.com/owasp-amass/amass/v5/...@master

# Passive enumeration
amass enum -passive -d target.com

# Active enumeration
amass enum -active -d target.com

# With all data sources
amass enum -d target.com -src

# Brute force
amass enum -brute -d target.com

# Output
amass enum -d target.com -o output.txt
amass enum -d target.com -oA output  # All formats
```

**Subfinder:**
```bash
# Installation
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest

# Basic usage
subfinder -d target.com

# All sources
subfinder -d target.com -all

# Specific sources
subfinder -d target.com -s crtsh,github

# JSON output
subfinder -d target.com -oJ output.json

# Include sources in output
subfinder -d target.com -cs -oJ output.json

# Multiple domains
subfinder -dL domains.txt

# Active subdomains only
subfinder -d target.com -nW

# Rate limiting
subfinder -d target.com -rl 100

# With proxy
subfinder -d target.com -proxy http://proxy:8080
```

**Other Tools:**
- **crt.sh** — Certificate Transparency logs
- **DNSDumpster** — DNS recon
- **SecurityTrails** — DNS and domain data
- **Amass** — OWASP flagship, comprehensive
- **Sublist3r** — Subdomain enumeration
- **Knockpy** — Subdomain scan

---

### 6.5 Technology Identification

**WhatWeb:**
```bash
# Installation
gem install whatweb

# Basic scan
whatweb target.com

# Verbose output
whatweb -v target.com

# Aggression level
whatweb -a 3 target.com  # Aggressive

# JSON output
whatweb --log-json=output.json target.com

# Proxy
whatweb --proxy http://proxy:8080 target.com

# Custom headers
whatweb --header "Authorization: Bearer token" target.com

# IP range
whatweb 192.168.1.0/24
```

**WhatWeb Identifies:**
- CMS (WordPress, Joomla, Drupal)
- JavaScript libraries (jQuery, React, Angular)
- Web servers (Apache, Nginx, IIS)
- Analytics packages (Google Analytics, Matomo)
- Embedded devices
- Version numbers
- Email addresses
- Account IDs

**Other Technology Detection Tools:**
- **Wappalyzer** — Browser extension + CLI
- **BuiltWith** — Website technology profiler
- **Netcraft** — Site report tool
- **Retire.js** — JavaScript library vulnerability scanner

---

## 7. Geolocation OSINT

### 7.1 EXIF Data from Photos

**ExifTool:**
```bash
# Installation (varies by OS)
# Windows: download from exiftool.org
# Linux: apt install libimage-exiftool-perl
# macOS: brew install exiftool

# Extract all metadata
exiftool photo.jpg

# GPS coordinates specifically
exiftool -GPS:all photo.jpg

# Specific tags
exiftool -filename -imagesize -exif:fnumber photo.jpg

# All tags in a group
exiftool -EXIF:all photo.jpg

# Group names displayed
exiftool -G photo.jpg

# JSON output
exiftool -json photo.jpg

# Remove all metadata
exiftool -all= photo.jpg

# Batch process directory
exiftool -r -json /path/to/photos/ > output.json

# Rename files by date
exiftool "-FileName<CreateDate" -d "%Y%m%d_%H%M%S.%%e" DIR

# Shift dates
exiftool "-DateTimeOriginal+=5:10:2 10:48:0" DIR
```

**GPS Data Fields:**
- `GPSLatitude` / `GPSLongitude` — coordinates
- `GPSAltitude` — elevation
- `GPSTimeStamp` — time at location
- `GPSDateStamp` — date at location
- `GPSMapDatum` — coordinate system
- `GPSImgDirection` — camera direction

**Supported Formats:** 300+ including JPEG, TIFF, PNG, RAW (CR2, CR3, NEF, ARW, DNG), HEIC/HEIF, PDF, MOV, MP4, AVI

---

### 7.2 Geolocation from Social Media Posts

**Techniques:**
1. Check post metadata for location tags
2. Analyze photo backgrounds (landmarks, signs, vegetation)
3. Cross-reference timezone with posting patterns
4. Look for location-specific content (weather, events)
5. Use reverse image search for location identification
6. Check geotags on Instagram/Twitter posts

**Tools:**
- **GeoSpy** — AI-based geolocation from photos
- **Google Earth/Maps** — Satellite imagery comparison
- **SunCalc** — Sun position analysis for time/location
- **Windy** — Weather pattern matching

---

### 7.3 IP Address Geolocation

**APIs:**
```bash
# IPinfo
curl https://ipinfo.io/8.8.8.8
curl https://ipinfo.io/8.8.8.8/json

# IP-API
curl http://ip-api.com/json/8.8.8.8

# ipstack
curl http://api.ipstack.com/8.8.8.8?access_key=YOUR_KEY

# MaxMind GeoIP2 (local database)
# Download GeoLite2-City.mmdb
```

**Python:**
```python
import requests

# IPinfo
r = requests.get("https://ipinfo.io/8.8.8.8/json")
data = r.json()
print(data['city'], data['region'], data['country'], data['loc'])

# ip-api
r = requests.get("http://ip-api.com/json/8.8.8.8")
data = r.json()
print(data['city'], data['regionName'], data['country'], data['lat'], data['lon'])
```

**Free Tiers:**
- IPinfo: 50,000 requests/month
- ip-api: 45 requests/minute (non-commercial)
- ipstack: 100 requests/month

---

### 7.4 Geolocation Tools Summary

| Tool | Purpose | Input |
|------|---------|-------|
| ExifTool | EXIF/GPS metadata extraction | Photo files |
| GeoSpy | AI geolocation from photos | Photo files |
| SunCalc | Sun position analysis | Location + time |
| IPinfo | IP geolocation | IP address |
| MaxMind | Local IP geolocation database | IP address |
| Google Earth | Satellite imagery | Coordinates |
| EarthCam | Live camera feeds | Location |

---

## 8. People Search Engines

### 8.1 Commercial People Search Sites

| Site | Features | Pricing |
|------|----------|---------|
| **Pipl** | Deep web people search, social profiles, contact info | API available, enterprise pricing |
| **Spokeo** | Name, address, phone, email, social profiles | From $13.95/month |
| **WhitePages** | Address, phone, relatives, background | Free basic, premium from $4.99/month |
| **BeenVerified** | Background checks, contact info, social profiles | From $17.48/month |
| **TruthFinder** | Background checks, criminal records | From $28.05/month |
| **Intelius** | People search, background checks | From $22.86/month |
| **Radaris** | People search, public records | Free basic search |
| **TruePeopleSearch** | Free people search | Free |
| **FastPeopleSearch** | Free people search | Free |
| **ThatsThem** | Free people search | Free |

---

### 8.2 Public Records Searches

**Types of Public Records:**
- Property records (ownership, deeds, tax assessments)
- Court records (civil, criminal, bankruptcy)
- Voter registration records
- Business filings and corporate records
- Professional licenses
- Birth/death/marriage/divorce records
- UCC filings (secured transactions)
- Sex offender registries
- Arrest records and mugshots

**Access Methods:**
1. County clerk websites (many free online)
2. State court electronic filing systems
3. PACER (federal court records) — $0.10/page
4. State vital records offices
5. Property assessor websites

---

### 8.3 Court Records and Legal Documents

**Federal:**
- PACER (Public Access to Court Electronic Records) — pacer.uscourts.gov
- RECAP (free mirror of PACER) — courtlistener.com/recap
- Supreme Court records — supremecourt.gov

**State:**
- Each state has its own court record system
- Many available through state judiciary websites
- Some require registration or payment

**Tools:**
- CourtListener — Free legal research
- Justia — Free case law
- Google Scholar — Case law search

---

## 9. Company/Workplace OSINT

### 9.1 Finding Employees

**LinkedIn Techniques:**
- `site:linkedin.com/in "Company Name"`
- `site:linkedin.com/in "Company Name" "Engineer"`
- LinkedIn Sales Navigator (paid, advanced filters)
- LinkedIn Recruiter (enterprise)

**Tools:**
- **LinkedIn2Username** — Convert LinkedIn profiles to username lists
- **CrossLinked** — LinkedIn enumeration tool
- **LinkedIn Scraper** — Python library for LinkedIn data

```bash
# CrossLinked
pip install crosslinked
crosslinked -f "FirstLast" company_name
```

---

### 9.2 Company Infrastructure

**Tools:**
- **Shodan** — Search company infrastructure
  ```
  org:"Company Name"
  ssl.cert.subject.cn:"example.com"
  hostname:".example.com"
  ```

- **Censys** — Certificate and host search
- **BuiltWith** — Technology profiler
- **Wappalyzer** — Technology detection
- **Netcraft** — Site report

**Subdomain Enumeration:**
```bash
# Find all subdomains
subfinder -d example.com -all
amass enum -d example.com

# Certificate transparency
curl https://crt.sh/?q=%25.example.com&output=json

# DNSDumpster
# Visit dnsdumpster.com and search for domain
```

---

### 9.3 Company Email Formats

**Hunter.io:**
```bash
# Find email format
curl "https://api.hunter.io/v2/domain-search?domain=example.com&api_key=YOUR_KEY"

# Response includes:
# - email_format (e.g., {first}.{last}@example.com)
# - list of discovered emails
# - confidence scores
```

**Common Email Formats:**
- `{first}.{last}@domain.com` (most common)
- `{first}{last}@domain.com`
- `{f}{last}@domain.com`
- `{first}_{last}@domain.com`
- `{first}@domain.com`
- `{last}@domain.com`
- `{first}.{last}@domain.co.uk`

**Tools for Email Discovery:**
- Hunter.io — Domain search, email finder, verifier
- RocketReach — Email and phone finder
- Tomba — Email finder
- Snov.io — Email drip campaigns
- Voila Norbert — Email finder

---

### 9.4 LinkedIn Scraping Techniques

**Manual Techniques:**
1. Google dorking: `site:linkedin.com/in "company" "title"`
2. LinkedIn People Search (with account)
3. LinkedIn Sales Navigator (paid)
4. Company page employee list

**Automated Tools:**
- linkedin-api (Python, unofficial)
- linkedin-scraper (Python)
- CrossLinked (OSINT focused)

**Data Points Available:**
- Full name, headline, location
- Current and past positions
- Education
- Skills and endorsements
- Connections count
- Profile URL

---

### 9.5 Company OSINT Data Sources

| Source | Data Available |
|--------|---------------|
| **Crunchbase** | Funding, investors, employees, acquisitions |
| **Glassdoor** | Reviews, salaries, interviews |
| **LinkedIn** | Employees, company info, job postings |
| **SEC EDGAR** | Financial filings, corporate structure |
| **OpenCorporates** | Company registrations worldwide |
| **WHOIS** | Domain registration info |
| **BuiltWith** | Technology stack |
| **SimilarWeb** | Traffic, competitors |
| **Wayback Machine** | Historical website snapshots |

---

## 10. Deep Web/Dark Web OSINT

### 10.1 Dark Web Search Engines

**Ahmia:**
- Clearnet: https://ahmia.fi
- Onion: juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion
- Indexes Tor hidden services
- Open source (ahmia/ahmia-site on GitHub)
- Maintains blacklist of banned .onion services
- Submit new services via "Add Service" feature

**Other Dark Web Search Engines:**
- **Torch** — One of the oldest Tor search engines
- **Not Evil** — Dark web search engine
- **DuckDuckGo Onion** — Privacy-focused search on Tor
- **Haystak** — Dark web search engine
- **Kilos** — Dark web search for marketplaces
- **DarkSearch** — API for dark web search

---

### 10.2 Tor Hidden Service Directories

**Directories:**
- **The Hidden Wiki** — Directory of .onion sites
- **Daniel's Hosting** — Hidden service directory
- **Tor Links** — Link directory
- **Fresh Onions** — Crawled .onion directory

**Access Methods:**
1. Tor Browser — Required for .onion access
2. Tor2web proxies — Access .onion from clearnet (less secure)
3. Tor API services — Programmatic access

---

### 10.3 Monitoring Dark Web for Brand Mentions

**Commercial Services:**
- Recorded Future — Threat intelligence
- Digital Shadows — Digital risk protection
- SpyCloud — Credential exposure monitoring
- DarkOwl — Dark web data provider
- Flashpoint — Threat intelligence

**Techniques:**
1. Monitor paste sites for leaked data
2. Search dark web forums for company mentions
3. Monitor marketplace listings for stolen credentials
4. Track ransomware leak sites
5. Monitor Telegram channels for leaked data

---

### 10.4 Dark Web OSINT Tools

**Tor-Based:**
- Tor Browser — Required for .onion access
- Torsocks — Route any app through Tor
- Nyx — Tor monitoring tool

**Scraping/Crawling:**
- OnionScan — Scan .onion sites for issues
- Fresh Onions — .onion crawler
- TorBot — Dark web crawler

**Intelligence Gathering:**
- OnionSearch — Search engine scraper for .onion
- Ahmia API — Programmatic dark web search
- DarkSearch API — Dark web search API

---

### 10.5 Dark Web Forum Monitoring

**Techniques:**
1. Register accounts on forums (with caution)
2. Use Tor Browser for anonymous access
3. Monitor RSS feeds where available
4. Use commercial threat intelligence platforms
5. Track forum mirrors and backups

**Data Points of Interest:**
- Leaked credentials
- Stolen data listings
- Exploit discussions
- Malware samples
- Attack planning discussions
- Company/target mentions

---

## Appendix A: OSINT Framework Summary

### Email OSINT Tools
| Tool | Purpose | Command |
|------|---------|---------|
| holehe | Email to accounts | `holehe email@test.com` |
| theHarvester | Email/domain enum | `theHarvester -d domain -b all` |
| email2phonenumber | Email to phone | `python3 email2phonenumber.py scrape -e email` |
| Hunter.io | Professional emails | API: `/v2/domain-search?domain=` |
| HIBP | Breach check | API: `/v3/breachedaccount/{email}` |

### Phone OSINT Tools
| Tool | Purpose | Command |
|------|---------|---------|
| PhoneInfoga | Phone scanning | `phoneinfoga scan -n +1234567890` |
| NumVerify | Validation/carrier | API: `/api/validate?number=` |
| phonenumbers | Python library | `phonenumbers.parse("+1...")` |

### Username OSINT Tools
| Tool | Purpose | Command |
|------|---------|---------|
| Sherlock | 400+ sites | `sherlock username` |
| Maigret | 3000+ sites | `maigret username` |
| social-analyzer | 1000+ sites | `python3 -m social-analyzer --username "user"` |
| Twint | Twitter (archived) | `twint -u username` |
| Instaloader | Instagram | `instaloader profile username` |
| Osintgram | Instagram | `python3 main.py username` |

### Network OSINT Tools
| Tool | Purpose | Command |
|------|---------|---------|
| Shodan | Device search | `shodan search "apache"` |
| Censys | Internet scan | `censys search "query"` |
| Nmap | Port scanning | `nmap -sV target.com` |
| Amass | Subdomain enum | `amass enum -d domain` |
| Subfinder | Subdomain enum | `subfinder -d domain` |
| WhatWeb | Tech detection | `whatweb target.com` |

### Geolocation OSINT Tools
| Tool | Purpose | Command |
|------|---------|---------|
| ExifTool | EXIF extraction | `exiftool photo.jpg` |
| IPinfo | IP geolocation | API: `/8.8.8.8/json` |
| GeoSpy | Photo geolocation | Web-based |

---

## Appendix B: API Endpoints Quick Reference

```
HIBP:      https://haveibeenpwned.com/api/v3/
IPinfo:    https://ipinfo.io/{ip}/json
IP-API:    http://ip-api.com/json/{ip}
crt.sh:    https://crt.sh/?q=%25.{domain}&output=json
Hunter:    https://api.hunter.io/v2/
NumVerify: http://apilayer.net/api/validate
Shodan:    https://api.shodan.io/
Censys:    https://search.censys.io/api/
```

---

## Appendix C: Legal and Ethical Considerations

1. **Authorization** — Always obtain proper authorization before conducting OSINT on targets
2. **Terms of Service** — Respect platform ToS when scraping
3. **Privacy Laws** — Comply with GDPR, CCPA, and local privacy regulations
4. **Data Handling** — Securely store and handle collected data
5. **Responsible Disclosure** — Report discovered vulnerabilities appropriately
6. **Scope Limitation** — Stay within authorized scope of engagement
7. **Documentation** — Maintain records of authorization and methods used

---

**Document compiled by:** Bauna Intern (bauna-intern@shaurya.dev)
**Research sources:** GitHub repositories, official documentation, API documentation, OSINT framework websites
**Last updated:** 2026-05-21

Co-Authored-By: Bauna Intern <bauna-intern@shaurya.dev>
