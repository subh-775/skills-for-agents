#!/usr/bin/env python3
"""
OSINT Toolkit — Python-based OSINT tools that work without external dependencies.
Only uses stdlib: urllib, socket, json, subprocess, ssl, re, sys, os, datetime.

Usage:
    python osint_core.py username <username>     # Sherlock + Maigret style username search
    python osint_core.py email <email>            # Email OSINT + breach check
    python osint_core.py domain <domain>          # Domain recon (DNS, whois, certs)
    python osint_core.py ip <ip>                  # IP recon (geo, ports, org)
    python osint_core.py phone <phone>            # Phone validation
    python osint_core.py metadata <file>          # File metadata extraction
    python osint_core.py social <username>        # Social media profiles
    python osint_core.py breach <email>           # Breach/leak check
    python osint_core.py dork <domain>            # Google dork queries
    python osint_core.py orchestrator <target> <type>  # Full recon
"""

import urllib.request
import urllib.parse
import urllib.error
import socket
import json
import subprocess
import ssl
import re
import sys
import os
import time
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# --- Config ---
OSINT_OUTPUT_DIR = os.environ.get("OSINT_OUTPUT_DIR", os.path.expanduser("~/osint"))
HIBP_API_KEY = os.environ.get("HIBP_API_KEY", "")
SHODAN_API_KEY = os.environ.get("SHODAN_API_KEY", "")
IPINFO_TOKEN = os.environ.get("IPINFO_TOKEN", "")
VT_API_KEY = os.environ.get("VT_API_KEY", "")

# SSL context for HTTPS requests
SSL_CTX = ssl.create_default_context()

def http_get(url, headers=None, timeout=10):
    """Safe HTTP GET — returns response text or empty string."""
    try:
        req = urllib.request.Request(url, headers=headers or {"User-Agent": "osint-skill/1.0"})
        with urllib.request.urlopen(req, timeout=timeout, context=SSL_CTX) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except Exception:
        return ""

def http_get_json(url, headers=None, timeout=10):
    """Safe HTTP GET — returns parsed JSON or empty dict."""
    try:
        text = http_get(url, headers, timeout)
        return json.loads(text) if text else {}
    except Exception:
        return {}

def make_output_dir(tag):
    """Create output directory with timestamp."""
    clean_tag = re.sub(r'[^a-zA-Z0-9_]', '_', tag)[:50]
    ts = datetime.now().strftime("%d_%b_%Y")
    out_dir = os.path.join(OSINT_OUTPUT_DIR, f"{clean_tag}_{ts}")
    os.makedirs(os.path.join(out_dir, "data"), exist_ok=True)
    os.makedirs(os.path.join(out_dir, "assets"), exist_ok=True)
    return out_dir

def save_json(out_dir, filename, data):
    """Save JSON to data/ subdirectory."""
    path = os.path.join(out_dir, "data", filename)
    with open(path, "w") as f:
        json.dump(data, f, indent=2, default=str)
    return path

def log(msg, level="INFO"):
    """Print log message."""
    colors = {"INFO": "\033[94m", "OK": "\033[92m", "WARN": "\033[93m", "ERROR": "\033[91m"}
    reset = "\033[0m"
    c = colors.get(level, "")
    print(f"{c}[{level}]{reset} {msg}", flush=True)

# ============================================================
# USERNAME ENUMERATION
# ============================================================

# Top 100 sites to check username on (no API needed, just HTTP)
USERNAME_SITES = {
    "GitHub": "https://github.com/{username}",
    "Twitter/X": "https://x.com/{username}",
    "Instagram": "https://www.instagram.com/{username}/",
    "Reddit": "https://www.reddit.com/user/{username}",
    "YouTube": "https://www.youtube.com/@{username}",
    "TikTok": "https://www.tiktok.com/@{username}",
    "LinkedIn": "https://www.linkedin.com/in/{username}",
    "Pinterest": "https://www.pinterest.com/{username}/",
    "Tumblr": "https://{username}.tumblr.com",
    "Medium": "https://medium.com/@{username}",
    "DeviantArt": "https://www.deviantart.com/{username}",
    "Flickr": "https://www.flickr.com/people/{username}",
    "Vimeo": "https://vimeo.com/{username}",
    "SoundCloud": "https://soundcloud.com/{username}",
    "Spotify": "https://open.spotify.com/user/{username}",
    "Twitch": "https://www.twitch.tv/{username}",
    "Steam": "https://steamcommunity.com/id/{username}",
    "Keybase": "https://keybase.io/{username}",
    "HackerNews": "https://news.ycombinator.com/user?id={username}",
    "ProductHunt": "https://www.producthunt.com/@{username}",
    "Dribbble": "https://dribbble.com/{username}",
    "Behance": "https://www.behance.net/{username}",
    "GitLab": "https://gitlab.com/{username}",
    "Bitbucket": "https://bitbucket.org/{username}",
    "CodePen": "https://codepen.io/{username}",
    "Replit": "https://replit.com/@{username}",
    "Kaggle": "https://www.kaggle.com/{username}",
    "Gravatar": "https://en.gravatar.com/{username}",
    "About.me": "https://about.me/{username}",
    "Linktree": "https://linktr.ee/{username}",
    "Mastodon": "https://mastodon.social/@{username}",
    "Patreon": "https://www.patreon.com/{username}",
    "Imgur": "https://imgur.com/user/{username}",
    "Giphy": "https://giphy.com/{username}",
    "Roblox": "https://www.roblox.com/user.aspx?username={username}",
    "Chess.com": "https://www.chess.com/member/{username}",
    "Duolingo": "https://www.duolingo.com/profile/{username}",
    "Last.fm": "https://www.last.fm/user/{username}",
    "Wattpad": "https://www.wattpad.com/user/{username}",
    "Goodreads": "https://www.goodreads.com/{username}",
    "MyAnimeList": "https://myanimelist.net/profile/{username}",
    "Poki": "https://poki.com/en/g/{username}",
    "ReverbNation": "https://www.reverbnation.com/{username}",
    "Bandcamp": "https://{username}.bandcamp.com",
    "500px": "https://500px.com/p/{username}",
    "CashApp": "https://cash.app/${username}",
    "Venmo": "https://venmo.com/{username}",
    "Letterboxd": "https://letterboxd.com/{username}",
    "Strava": "https://www.strava.com/athletes/{username}",
    "AllTrails": "https://www.alltrails.com/members/{username}",
}

def check_username_site(name, url_template, username, timeout=8):
    """Check if username exists on a single site."""
    url = url_template.format(username=username)
    try:
        req = urllib.request.Request(url, method="GET", headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        with urllib.request.urlopen(req, timeout=timeout, context=SSL_CTX) as resp:
            if resp.status == 200:
                return {"site": name, "url": url, "status": "found", "http_status": 200}
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return {"site": name, "url": url, "status": "not_found", "http_status": 404}
        elif e.code == 403:
            return {"site": name, "url": url, "status": "possible", "http_status": 403}
        return {"site": name, "url": url, "status": "error", "http_status": e.code}
    except Exception:
        return {"site": name, "url": url, "status": "timeout", "http_status": 0}

def username_enum(username, out_dir=None, max_workers=20):
    """Enumerate username across sites using parallel HTTP requests."""
    out_dir = out_dir or make_output_dir(f"username_{username}")
    log(f"=== Username Enumeration: {username} ===")
    log(f"Checking {len(USERNAME_SITES)} sites with {max_workers} threads...")

    results = []
    found = []

    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = {
            pool.submit(check_username_site, name, url, username): name
            for name, url in USERNAME_SITES.items()
        }
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            if result["status"] == "found":
                found.append(result)
                log(f"  [+] {result['site']}: {result['url']}", "OK")

    report = {
        "target": username,
        "type": "username",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "total_sites_checked": len(results),
        "accounts_found": len(found),
        "found": found,
        "possible": [r for r in results if r["status"] == "possible"],
        "all_results": results,
    }

    save_json(out_dir, "username_enum.json", report)
    log(f"=== Summary: {len(found)}/{len(USERNAME_SITES)} sites found ===", "OK")
    return report

# ============================================================
# EMAIL OSINT
# ============================================================

def email_osint(email, out_dir=None):
    """Email OSINT: platform check + domain analysis + breach check."""
    out_dir = out_dir or make_output_dir(f"email_{email.split('@')[0]}")
    log(f"=== Email OSINT: {email} ===")

    report = {
        "target": email,
        "type": "email",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    # Domain analysis
    domain = email.split("@")[1]
    log(f"Analyzing domain: {domain}")

    # MX records
    mx_records = []
    try:
        result = subprocess.run(["nslookup", "-type=MX", domain], capture_output=True, text=True, timeout=10)
        mx_records = re.findall(r'mail exchanger = (.+)', result.stdout)
    except Exception:
        pass

    # TXT records (SPF, DMARC)
    spf = ""
    dmarc = ""
    try:
        result = subprocess.run(["nslookup", "-type=TXT", domain], capture_output=True, text=True, timeout=10)
        for line in result.stdout.split("\n"):
            if "spf" in line.lower():
                spf = line.strip()
            if "dmarc" in line.lower():
                dmarc = line.strip()
    except Exception:
        pass

    report["domain_analysis"] = {
        "domain": domain,
        "mx_records": mx_records,
        "spf": spf,
        "dmarc": dmarc,
    }
    log(f"MX: {mx_records}", "OK")

    # Username from email local part
    username = email.split("@")[0]
    log(f"Running username search on: {username}")
    username_report = username_enum(username, out_dir)
    report["username_enum"] = {
        "total_sites_checked": username_report["total_sites_checked"],
        "accounts_found": username_report["accounts_found"],
        "found": username_report["found"],
    }

    # HIBP breach check
    if HIBP_API_KEY:
        log("Checking HIBP breaches...")
        breaches = http_get_json(
            f"https://haveibeenpwned.com/api/v3/breachedaccount/{urllib.parse.quote(email)}?truncateResponse=false",
            headers={"hibp-api-key": HIBP_API_KEY, "user-agent": "osint-skill"}
        )
        if isinstance(breaches, list):
            report["breaches"] = breaches
            report["breach_count"] = len(breaches)
            log(f"HIBP: {len(breaches)} breaches found", "OK")
        else:
            report["breaches"] = []
            report["breach_count"] = 0
    else:
        log("HIBP_API_KEY not set — skipping breach check", "WARN")
        report["breaches"] = []
        report["breach_count"] = 0

    save_json(out_dir, "email_osint.json", report)
    log(f"=== Email OSINT complete ===", "OK")
    return report

# ============================================================
# DOMAIN RECON
# ============================================================

def dns_query(domain, record_type):
    """DNS lookup using nslookup (cross-platform)."""
    try:
        result = subprocess.run(
            ["nslookup", f"-type={record_type}", domain],
            capture_output=True, text=True, timeout=10
        )
        lines = result.stdout.split("\n")
        records = []
        for line in lines:
            line = line.strip()
            if record_type == "A" and "Address:" in line and not line.startswith("Server:"):
                addr = line.split("Address:")[-1].strip()
                if addr and ":" not in addr:  # Skip IPv6 for A records
                    records.append(addr)
            elif record_type == "MX" and "mail exchanger" in line:
                records.append(line.split("=")[-1].strip())
            elif record_type == "NS" and "nameserver" in line:
                records.append(line.split("=")[-1].strip())
            elif record_type == "TXT":
                # Extract quoted strings from TXT records
                txt_matches = re.findall(r'"([^"]*)"', line)
                if txt_matches:
                    records.append(" ".join(txt_matches))
                elif "text =" in line:
                    val = line.split("text =", 1)[-1].strip()
                    if val and val != '=':
                        records.append(val)
        return records
    except Exception:
        return []

def crtsh_query(domain):
    """Query crt.sh for certificate transparency subdomains."""
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "osint-skill/1.0"})
        with urllib.request.urlopen(req, timeout=30, context=SSL_CTX) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
        data = json.loads(raw)
    except Exception as e:
        log(f"crt.sh request failed: {e}", "WARN")
        return []
    if not isinstance(data, list):
        return []
    subs = set()
    for entry in data:
        name = entry.get("name_value", "")
        for sub in name.split("\n"):
            sub = sub.strip().lower()
            if sub.endswith(domain) and "*" not in sub:
                subs.add(sub)
    return sorted(subs)

def github_search_org(domain):
    """Search GitHub for organization info."""
    url = f"https://api.github.com/search/users?q={domain}+in:login"
    data = http_get_json(url)
    users = []
    for item in data.get("items", [])[:10]:
        users.append({
            "login": item.get("login"),
            "url": item.get("html_url"),
            "type": item.get("type"),
        })
    return users

def domain_recon(domain, out_dir=None):
    """Full domain reconnaissance."""
    out_dir = out_dir or make_output_dir(f"domain_{domain}")
    log(f"=== Domain Recon: {domain} ===")

    report = {
        "target": domain,
        "type": "domain",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    # DNS records
    log("Querying DNS...")
    report["dns"] = {
        "A": dns_query(domain, "A"),
        "AAAA": dns_query(domain, "AAAA"),
        "MX": dns_query(domain, "MX"),
        "NS": dns_query(domain, "NS"),
        "TXT": dns_query(domain, "TXT"),
    }
    log(f"A records: {report['dns']['A']}", "OK")

    # Whois via HTTP API
    log("Querying WHOIS...")
    whois_data = http_get(f"https://whois.arin.net/rest/domain/{domain}.json")
    if whois_data:
        try:
            whois_json = json.loads(whois_data)
            report["whois"] = whois_json
        except json.JSONDecodeError:
            report["whois"] = {"raw": whois_data[:500]}
    else:
        report["whois"] = {"status": "no_data"}

    # crt.sh certificate transparency
    log("Checking certificate transparency (crt.sh)...")
    crtsh_subs = crtsh_query(domain)
    report["crtsh"] = {
        "subdomains_from_certs": crtsh_subs,
        "count": len(crtsh_subs),
    }
    log(f"crt.sh: {len(crtsh_subs)} subdomains", "OK")

    # GitHub org search
    log("Searching GitHub...")
    gh_users = github_search_org(domain)
    report["github"] = gh_users

    # HTTP headers from main domain
    log("Fetching HTTP headers...")
    try:
        req = urllib.request.Request(f"https://{domain}", headers={"User-Agent": "osint-skill/1.0"})
        with urllib.request.urlopen(req, timeout=10, context=SSL_CTX) as resp:
            report["http_headers"] = dict(resp.headers)
            report["http_status"] = resp.status
    except Exception as e:
        report["http_headers"] = {}
        report["http_status"] = str(e)

    # robots.txt
    log("Checking robots.txt...")
    robots = http_get(f"https://{domain}/robots.txt")
    if robots and "User-agent" in robots:
        report["robots_txt"] = robots[:2000]

    # security.txt
    log("Checking security.txt...")
    sec_txt = http_get(f"https://{domain}/.well-known/security.txt")
    if sec_txt and len(sec_txt) > 10:
        report["security_txt"] = sec_txt[:2000]

    save_json(out_dir, "domain_recon.json", report)
    log(f"=== Domain Recon complete ===", "OK")
    return report

# ============================================================
# IP RECON
# ============================================================

def ip_recon(ip, out_dir=None):
    """IP reconnaissance: geolocation, org, reputation."""
    out_dir = out_dir or make_output_dir(f"ip_{ip.replace('.', '_')}")
    log(f"=== IP Recon: {ip} ===")

    report = {
        "target": ip,
        "type": "ip",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    # Reverse DNS
    log("Reverse DNS lookup...")
    try:
        hostname = socket.gethostbyaddr(ip)
        report["reverse_dns"] = hostname[0]
    except Exception:
        report["reverse_dns"] = "none"

    # ipinfo.io
    log("Querying ipinfo.io...")
    ipinfo_url = f"https://ipinfo.io/{ip}/json"
    if IPINFO_TOKEN:
        ipinfo_url += f"?token={IPINFO_TOKEN}"
    ipinfo = http_get_json(ipinfo_url)
    if ipinfo:
        report["ipinfo"] = ipinfo
        log(f"ipinfo: {ipinfo.get('org', 'unknown')} ({ipinfo.get('city', 'unknown')})", "OK")

    # Shodan
    if SHODAN_API_KEY:
        log("Querying Shodan...")
        shodan = http_get_json(f"https://api.shodan.io/shodan/host/{ip}?key={SHODAN_API_KEY}")
        if "ip_str" in shodan:
            report["shodan"] = {
                "ports": shodan.get("ports", []),
                "os": shodan.get("os"),
                "org": shodan.get("org"),
                "vulns": shodan.get("vulns", []),
                "services": [
                    {"port": d.get("port"), "product": d.get("product"), "version": d.get("version")}
                    for d in shodan.get("data", [])
                ],
            }
            log(f"Shodan: {len(shodan.get('ports', []))} ports", "OK")
        else:
            report["shodan"] = {"status": "no_data"}
    else:
        log("SHODAN_API_KEY not set", "WARN")
        report["shodan"] = {"status": "api_key_missing"}

    # AbuseIPDB
    abuse_key = os.environ.get("ABUSEIPDB_KEY", "")
    if abuse_key:
        log("Checking AbuseIPDB...")
        abuse = http_get_json(
            f"https://api.abuseipdb.com/api/v2/check?ipAddress={ip}",
            headers={"Key": abuse_key, "Accept": "application/json"}
        )
        if "data" in abuse:
            report["abuseipdb"] = {
                "score": abuse["data"].get("abuseConfidenceScore", 0),
                "reports": abuse["data"].get("totalReports", 0),
                "country": abuse["data"].get("countryCode"),
                "isp": abuse["data"].get("isp"),
            }
            log(f"AbuseIPDB: score={report['abuseipdb']['score']}", "OK")

    # VirusTotal (IP lookup)
    if VT_API_KEY:
        log("Checking VirusTotal...")
        vt = http_get_json(
            f"https://www.virustotal.com/api/v3/ip_addresses/{ip}",
            headers={"x-apikey": VT_API_KEY}
        )
        if "data" in vt:
            stats = vt["data"].get("attributes", {}).get("last_analysis_stats", {})
            report["virustotal"] = {
                "malicious": stats.get("malicious", 0),
                "suspicious": stats.get("suspicious", 0),
                "harmless": stats.get("harmless", 0),
            }
            log(f"VirusTotal: {stats.get('malicious', 0)} malicious", "OK")

    save_json(out_dir, "ip_recon.json", report)
    log(f"=== IP Recon complete ===", "OK")
    return report

# ============================================================
# SOCIAL MEDIA PROFILES
# ============================================================

def social_media(username, out_dir=None):
    """Check social media profiles via public APIs."""
    out_dir = out_dir or make_output_dir(f"social_{username}")
    log(f"=== Social Media OSINT: {username} ===")

    report = {
        "target": username,
        "type": "social",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "profiles": {},
    }

    # GitHub API (no auth needed)
    log("Checking GitHub...")
    gh = http_get_json(f"https://api.github.com/users/{username}")
    if "login" in gh:
        report["profiles"]["github"] = {
            "name": gh.get("name"),
            "bio": gh.get("bio"),
            "public_repos": gh.get("public_repos", 0),
            "followers": gh.get("followers", 0),
            "following": gh.get("following", 0),
            "company": gh.get("company"),
            "location": gh.get("location"),
            "email": gh.get("email"),
            "blog": gh.get("blog"),
            "created_at": gh.get("created_at"),
            "url": gh.get("html_url"),
        }
        log(f"GitHub: {gh.get('public_repos', 0)} repos, {gh.get('followers', 0)} followers", "OK")

    # Reddit API (no auth needed for basic)
    log("Checking Reddit...")
    reddit = http_get_json(
        f"https://www.reddit.com/user/{username}/about.json",
        headers={"User-Agent": "osint-skill/1.0"}
    )
    if "data" in reddit:
        d = reddit["data"]
        report["profiles"]["reddit"] = {
            "total_karma": d.get("total_karma", 0),
            "comment_karma": d.get("comment_karma", 0),
            "link_karma": d.get("link_karma", 0),
            "account_created": datetime.fromtimestamp(d.get("created_utc", 0), tz=timezone.utc).isoformat(),
            "is_gold": d.get("is_gold", False),
            "is_mod": d.get("is_mod", False),
        }
        log(f"Reddit: {d.get('total_karma', 0)} karma", "OK")

    # Keybase
    log("Checking Keybase...")
    kb = http_get_json(f"https://keybase.io/_/api/1.0/user/lookup.json?username={username}")
    if kb.get("them"):
        report["profiles"]["keybase"] = {
            "basics": kb["them"][0].get("basics", {}),
        }
        log(f"Keybase: found", "OK")

    # npm registry
    log("Checking npm...")
    npm = http_get_json(f"https://registry.npmjs.org/-/v1/search?text=maintainer:{username}&size=5")
    if npm.get("objects"):
        pkgs = [obj["package"]["name"] for obj in npm["objects"]]
        report["profiles"]["npm"] = {"packages": pkgs, "count": len(pkgs)}
        log(f"npm: {len(pkgs)} packages", "OK")

    # PyPI
    log("Checking PyPI...")
    pypi_search = http_get(f"https://pypi.org/user/{username}/")
    if pypi_search and "404" not in pypi_search[:200]:
        report["profiles"]["pypi"] = {"exists": True}
        log(f"PyPI: profile found", "OK")

    save_json(out_dir, "social_media.json", report)
    log(f"=== Social Media OSINT complete ===", "OK")
    return report

# ============================================================
# GOOGLE DORK QUERIES
# ============================================================

def generate_dorks(domain, out_dir=None):
    """Generate Google dork queries for a domain."""
    out_dir = out_dir or make_output_dir(f"dork_{domain}")
    log(f"=== Google Dork Generator: {domain} ===")

    dorks = {
        "exposed_files": {
            "pdf": f'site:{domain} filetype:pdf',
            "excel": f'site:{domain} filetype:xlsx OR filetype:csv',
            "word": f'site:{domain} filetype:docx OR filetype:doc',
            "presentations": f'site:{domain} filetype:pptx OR filetype:ppt',
            "sql_dumps": f'site:{domain} filetype:sql',
        },
        "sensitive_dirs": {
            "open_directories": f'site:{domain} intitle:"index of"',
            "git_repos": f'site:{domain} intitle:"index of" .git',
            "env_files": f'site:{domain} filetype:env',
            "config_files": f'site:{domain} filetype:xml OR filetype:conf',
            "log_files": f'site:{domain} filetype:log',
            "backup_files": f'site:{domain} filetype:bak OR filetype:sql OR filetype:dump',
        },
        "login_pages": {
            "admin": f'site:{domain} inurl:admin OR inurl:login',
            "cpanel": f'site:{domain} intitle:"cPanel Login"',
            "phpmyadmin": f'site:{domain} inurl:phpmyadmin',
            "wp_admin": f'site:{domain} inurl:wp-admin',
        },
        "info_leaks": {
            "emails": f'site:{domain} "@{domain}"',
            "phone_numbers": f'site:{domain} "phone" OR "tel" OR "contact"',
            "error_pages": f'site:{domain} intitle:"error" OR intitle:"500"',
            "stack_traces": f'site:{domain} "stack trace" OR "exception"',
        },
        "github_leaks": {
            "secrets": f'site:github.com "{domain}" "api_key" OR "password" OR "secret"',
            "env_files": f'site:github.com "{domain}" filetype:env',
            "credentials": f'site:github.com "{domain}" "credentials" OR "token"',
        },
        "social_media": {
            "linkedin": f'site:linkedin.com/in "{domain}"',
            "github_org": f'site:github.com "{domain}"',
            "twitter": f'site:twitter.com "{domain}"',
        },
        "pastebin": {
            "paste_search": f'site:pastebin.com "{domain}"',
        },
    }

    # Count total dorks
    total = sum(len(cat) for cat in dorks.values())
    log(f"Generated {total} dork queries across {len(dorks)} categories", "OK")

    report = {
        "target": domain,
        "type": "dorks",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "total_dorks": total,
        "categories": dorks,
        "note": "Paste these into Google search or use Google Custom Search API (GOOGLE_API_KEY + GOOGLE_CSE_ID)",
    }

    save_json(out_dir, "google_dorks.json", report)
    return report

# ============================================================
# ORCHESTRATOR
# ============================================================

def orchestrator(target, target_type, out_dir=None):
    """Full OSINT orchestrator — chains all tools into a SINGLE output directory."""
    # ONE directory per investigation — all tools write here
    if out_dir is None:
        clean_tag = re.sub(r'[^a-zA-Z0-9_]', '_', target)[:50]
        ts = datetime.now().strftime("%d_%b_%Y")
        out_dir = os.path.join(OSINT_OUTPUT_DIR, f"{clean_tag}_{ts}")
        os.makedirs(os.path.join(out_dir, "data"), exist_ok=True)
        os.makedirs(os.path.join(out_dir, "assets"), exist_ok=True)

    log(f"╔══════════════════════════════════════════╗")
    log(f"║        OSINT ORCHESTRATOR                ║")
    log(f"╚══════════════════════════════════════════╝")
    log(f"Target: {target}")
    log(f"Type:   {target_type}")
    log(f"Output: {out_dir}")

    start = time.time()
    report = {
        "target": target,
        "type": target_type,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "output_directory": out_dir,
        "phases": {},
    }

    # All tools write to the same out_dir — no separate slug folders
    phases = {
        "email": [
            ("Email OSINT", lambda: email_osint(target, out_dir)),
            ("Domain Recon", lambda: domain_recon(target.split("@")[1], out_dir)),
        ],
        "phone": [
            ("Phone Lookup", lambda: username_enum(re.sub(r'[^0-9]', '', target), out_dir)),
        ],
        "username": [
            ("Username Enumeration", lambda: username_enum(target, out_dir)),
            ("Social Media Profiles", lambda: social_media(target, out_dir)),
        ],
        "domain": [
            ("Domain Recon", lambda: domain_recon(target, out_dir)),
            ("Google Dorks", lambda: generate_dorks(target, out_dir)),
        ],
        "ip": [
            ("IP Recon", lambda: ip_recon(target, out_dir)),
        ],
        "person": [
            ("Username Enumeration", lambda: username_enum(target, out_dir)),
            ("Social Media Profiles", lambda: social_media(target, out_dir)),
        ],
    }

    phase_list = phases.get(target_type, [])
    for i, (name, func) in enumerate(phase_list, 1):
        log(f"\n>>> Phase {i}: {name}")
        try:
            result = func()
            report["phases"][name] = {"status": "complete"}
        except Exception as e:
            log(f"Phase failed: {e}", "ERROR")
            report["phases"][name] = {"status": "error", "error": str(e)}

    duration = time.time() - start
    report["duration_seconds"] = round(duration, 1)

    # Merge all JSON files from data/ into master
    data_dir = os.path.join(out_dir, "data")
    for fname in os.listdir(data_dir):
        if fname == "master_report.json":
            continue
        if fname.endswith(".json"):
            try:
                with open(os.path.join(data_dir, fname)) as f:
                    tool_data = json.load(f)
                tool_name = fname.replace(".json", "")
                report["phases"][tool_name] = tool_data
            except Exception:
                pass

    save_json(out_dir, "master_report.json", report)

    log(f"\n╔══════════════════════════════════════════╗")
    log(f"║        OSINT COMPLETE                    ║")
    log(f"╚══════════════════════════════════════════╝")
    log(f"Duration: {duration:.1f}s")
    log(f"Files:    {len(os.listdir(data_dir))} JSON reports in {data_dir}")
    log(f"Master:   {out_dir}/data/master_report.json", "OK")

    return report

# ============================================================
# CLI
# ============================================================

COMMANDS = {
    "username": ("username_enum", "<username>"),
    "email": ("email_osint", "<email>"),
    "domain": ("domain_recon", "<domain>"),
    "ip": ("ip_recon", "<ip>"),
    "social": ("social_media", "<username>"),
    "dork": ("generate_dorks", "<domain>"),
    "orchestrator": ("orchestrator", "<target> <type>"),
}

def main():
    if len(sys.argv) < 3:
        print("Usage: python osint_core.py <command> <target> [type]")
        print("\nCommands:")
        for cmd, (func, args) in COMMANDS.items():
            print(f"  {cmd:15s} {args}")
        print("\nTarget types for orchestrator: email, phone, username, domain, ip, person")
        print("\nAPI keys (set as env vars):")
        print("  HIBP_API_KEY, SHODAN_API_KEY, IPINFO_TOKEN, VT_API_KEY, ABUSEIPDB_KEY")
        sys.exit(1)

    command = sys.argv[1]
    target = sys.argv[2]

    if command == "orchestrator":
        if len(sys.argv) < 4:
            print("Usage: python osint_core.py orchestrator <target> <type>")
            sys.exit(1)
        orchestrator(target, sys.argv[3])
    elif command in COMMANDS:
        func_name = COMMANDS[command][0]
        globals()[func_name](target)
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
