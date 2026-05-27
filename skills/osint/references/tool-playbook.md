# OSINT Tool Playbook — Installation & Usage

> Reference for the /osint skill. Contains installation commands, usage examples, and API endpoints for all OSINT tools.

---

## Email OSINT Tools

### holehe (11k stars)
Checks if email is registered on 120+ platforms using password recovery, registration, and login flows.

```bash
# Install
pip3 install holehe

# Usage
holehe user@example.com

# Output: service name, exists (bool), emailrecovery, phoneNumber
```

**Supported platforms:** Twitter, Instagram, Snapchat, Discord, Spotify, GitHub, Google, Amazon, Pinterest, Tumblr, Flickr, eBay, Patreon, Yahoo, WordPress, Venmo, and 100+ more.

**Online version:** osint.industries

### theHarvester (16.3k stars)
Collects names, emails, IPs, subdomains, URLs from 40+ public sources.

```bash
# Install
git clone https://github.com/laramies/theHarvester
cd theHarvester && uv sync

# Usage
uv run theHarvester -d domain.com -b all
uv run theHarvester -d domain.com -b google,bing,yahoo
uv run theHarvester -d domain.com -b shodan -l 500
```

**Data sources:** Baidu, Yahoo, DuckDuckGo, Brave, Mojeek, FOFA, ZoomEye, crt.sh, Cert Spotter, Censys, SecurityTrails, RapidDNS, DNSDumpster, BufferOverun, HaveIBeenPwned, OTX, ThreatMiner, CriminalIP, LeakIX, LeakLookup, Dehashed, Shodan, Hunter.io, FullHunt, Netlas, Onyphe, BuiltWith, URLScan, PentestTools, ProjectDiscovery, HackerTarget, RocketReach, Tomba, IntelX, BeVigil, SubdomainCenter, SubdomainFinderC99, THC, WhoisXML, SecurityScorecard, GitHub Code Search

---

## Phone OSINT Tools

### PhoneInfoga (16.5k stars)
Phone number scanning and OSINT footprinting.

```bash
# Install (Docker)
docker run -it --rm sundowndev/phoneinfoga scan -n "+1234567890"

# Install (Go)
go install github.com/sundowndev/phoneinfoga/v2/cmd/phoneinfoga@latest
phoneinfoga scan -n "+1234567890"

# REST API
phoneinfoga serve -p 8080
# Then: GET /api/v1/numbers/+1234567890/scan
```

**Features:** Verify existence, collect country/line type/carrier, OSINT footprinting, reputation reports, social media checks, disposable number detection.

### NumVerify API
Phone number validation and carrier lookup.

```bash
# API endpoint
curl "http://apilayer.net/api/validate?access_key=KEY&number=+1234567890"

# Returns: valid, local_format, international_format, country_prefix,
#          country_code, country_name, location, carrier, line_type
```

**Free tier:** 100 requests/month.

---

## Username / Social Media OSINT Tools

### Sherlock (83.6k stars)
Hunt down social media accounts by username across 400+ social networks.

```bash
# Install
pipx install sherlock-project

# Usage
sherlock user123
sherlock user1 user2 user3
sherlock user123 --verbose --output results.txt --csv
sherlock user123 --site Twitter --site Instagram
sherlock user123 --proxy socks5://127.0.0.1:1080
sherlock user123 --browse  # open results in browser
```

**Key flags:** `--verbose`, `--output FILE`, `--folderoutput DIR`, `--csv`, `--xlsx`, `--site SITE_NAME`, `--proxy`, `--json JSON_FILE`, `--timeout`, `--print-all`, `--browse`, `--nsfw`, `--txt`, `--no-color`

### maigret (3,000+ sites)
Collects dossier by username only, checks 3,000+ sites, extracts profile data.

```bash
# Install
pip install maigret

# Usage
maigret user123
maigret user123 --html  # HTML report
maigret user123 --pdf   # PDF report
maigret user123 --ai    # AI analysis (requires OPENAI_API_KEY)
maigret user123 --web 5000  # web interface on port 5000
maigret user1 user2 user3 -a  # multiple usernames
maigret user123 --tags photo,dating  # filter by tags
maigret user123 --permute  # try username permutations
maigret user123 --parse URL  # recursive from URL
maigret user123 --proxy socks5://127.0.0.1:1080
```

**Features:** Profile extraction via socid_extractor, recursive search (auto-uses discovered usernames), tag filtering, block/CAPTCHA detection, auto-updating database, Tor/I2P support, Cloudflare bypass via FlareSolverr.

**Report formats:** HTML, PDF, XMind, JSON, CSV, TXT, interactive D3 graph.

### social-analyzer (22.9k stars)
API, CLI, and Web App for finding profiles across 1,000+ social media/sites.

```bash
# Install
pip3 install social-analyzer

# Usage
python3 -m social-analyzer --username "johndoe"
python3 -m social-analyzer --username "johndoe" --websites "twitter,instagram"
python3 -m social-analyzer --username "johndoe" --mode fast --output json
python3 -m social-analyzer --username "johndoe" --filter good --extract --metadata
```

**Features:** String/name analysis with permutations, profile finding via HTTPS and Webdriver, multi-profile search, multilayer detections (OCR, normal, advanced, special), metadata extraction, force-directed graph visualization, search by Alexa ranking or country, search by type (adult, music), profile screenshots, name origins.

### Instaloader (12.4k stars)
Download public/private profiles, hashtags, stories, feeds, saved media.

```bash
# Install
pip3 install instaloader

# Usage
instaloader profile [profile ...]
instaloader --comments --geotags profile
instaloader --stories --highlights profile
instaloader --login YOUR-USERNAME profile  # access private profiles
instaloader --fast-update profile  # only new posts
instaloader "#hashtag"  # download hashtag posts
```

---

## Network / Infrastructure OSINT Tools

### Subfinder (13.7k stars)
Passive subdomain enumeration.

```bash
# Install
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest

# Usage
subfinder -d domain.com
subfinder -d domain.com -o subdomains.txt -oJ subdomains.json
subfinder -d domain.com -s crtsh,github -recursive
subfinder -d domain.com --rls "hackertarget=10/s,shodan=15/s"
```

### Amass (14.6k stars)
OWASP network mapping and attack surface discovery.

```bash
# Install (Docker)
docker pull owasp/amass

# Usage
amass enum -d domain.com
amass enum -d domain.com -o subdomains.txt
amass enum -passive -d domain.com  # passive only
amass viz -d domain.com  # visualization
```

### Shodan
Internet-connected device search engine.

```bash
# CLI install
pip3 install shodan
shodan init YOUR_API_KEY

# Usage
shodan search "org:Company Name"
shodan host 1.2.3.4
shodan stats --facets port:100 country:US
shodan scan submit 1.2.3.0/24

# Search filters
# port:, hostname:, org:, product:, vuln:, country:, city:, os:, net:, asn:
```

### Nmap
Network discovery and security auditing.

```bash
# Basic scan
nmap target

# Service version detection
nmap -sV target

# OS detection
nmap -O target

# Full scan
nmap -v -A target

# Script scanning
nmap --script=default target

# Port range
nmap -p 1-1000 target

# UDP scan
nmap -sU target
```

### WhatWeb (6.6k stars)
Website identification with 1,800+ plugins.

```bash
# Install
git clone https://github.com/urbanadventurer/WhatWeb
cd WhatWeb && gem install bundler && bundle install

# Usage
./whatweb example.com
./whatweb -v reddit.com
./whatweb -a 3 target  # aggressive scan
./whatweb --log-json output.json target
```

### crt.sh — Certificate Transparency

```bash
# Query certificates for domain
curl "https://crt.sh/?q=%25.domain.com&output=json" | jq '.[] | .name_value' | sort -u

# Python script
curl -s "https://crt.sh/?q=%25.domain.com&output=json" | python3 -c "
import json, sys
data = json.load(sys.stdin)
for cert in data:
    for name in cert['name_value'].split('\n'):
        print(name)
" | sort -u
```

---

## Leaked Database Check Tools

### Have I Been Pwned (HIBP) API

```bash
# Breach check (requires API key)
curl -H "hibp-api-key: KEY" \
     -H "user-agent: OSINT-Tool" \
     "https://haveibeenpwned.com/api/v3/breachedaccount/user@example.com?truncateResponse=false"

# Paste check
curl -H "hibp-api-key: KEY" \
     -H "user-agent: OSINT-Tool" \
     "https://haveibeenpwned.com/api/v3/pasteaccount/user@example.com"

# All breaches
curl "https://haveibeenpwned.com/api/v3/breaches"

# Password hash check (free, no auth)
curl "https://api.pwnedpasswords.com/range/SHA1_PREFIX"
```

### IntelX API

```bash
# Search (requires API key)
curl -H "x-key: KEY" "https://public.intelx.io/intelligent/search" \
     -d '{"term":"user@example.com","buckets":[],"lookuplevel":0,"maxresults":100,"timeout":5,"datefrom":"","dateto":""}'

# Results
curl -H "x-key: KEY" "https://public.intelx.io/intelligent/search/result?id=SEARCH_ID&limit=100"
```

---

## Geolocation OSINT Tools

### ExifTool

```bash
# Install (Linux/macOS)
sudo apt install exiftool  # or brew install exiftool

# Usage
exiftool image.jpg  # all metadata
exiftool -gps:all image.jpg  # GPS coordinates
exiftool -filename -imagesize image.jpg  # specific tags
exiftool -r -gps:all /path/to/directory/  # recursive
```

### IPinfo API

```bash
# IP geolocation
curl "https://ipinfo.io/8.8.8.8/json?token=TOKEN"

# Returns: city, region, country, org, timezone, loc (coordinates)
```

---

## People Search Services

| Service | URL | Search By | Returns |
|---------|-----|-----------|---------|
| Pipl | pipl.com | name, email, phone, username | addresses, employment, education, social profiles, relatives |
| Spokeo | spokeo.com | name, email, phone, address | contact info, location history, family, social profiles |
| WhitePages | whitepages.com | name, phone, address | reverse lookup, background checks |
| BeenVerified | beenverified.com | name, phone, email, address, username | contact info, social profiles, property, court records |
| IntelX Phonebook | phonebook.cz | email, domain, phone | URLs, email addresses, domains |

---

## Company OSINT Tools

### Hunter.io

```bash
# Domain search (find emails from company)
curl "https://api.hunter.io/v2/domain-search?domain=company.com&api_key=KEY"

# Email finder
curl "https://api.hunter.io/v2/email-finder?domain=company.com&first_name=John&last_name=Smith&api_key=KEY"

# Email verifier
curl "https://api.hunter.io/v2/email-verifier?email=user@company.com&api_key=KEY"
```

**Free tier:** 50 credits/month.

---

## Multi-Purpose OSINT Frameworks

### Recon-ng (5.6k stars)
Modular OSINT framework with Metasploit-like interface.

```bash
# Install
apt install recon-ng  # or git clone

# Usage
recon-ng
workspaces create osint
db insert companies
modules load recon/domains-hosts/hackertarget
options set SOURCE domain.com
run
```

### Maltego (Commercial)
Link analysis and visualization with 120+ data partners.

- Free community tier available
- Transforms for automated queries
- Visual graph-based analysis
- Export to various formats
