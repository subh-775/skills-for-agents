# OSINT Tool Playbook

Quick reference for common OSINT tools.

## Account Discovery

| Tool | Command | Scope |
|------|---------|-------|
| holehe | `holehe user@example.com` | 120+ platforms |
| sherlock | `sherlock user123` | 400+ social networks |
| maigret | `maigret user123` | 3,000+ sites |

## Infrastructure Recon

| Tool | Command | Scope |
|------|---------|-------|
| subfinder | `subfinder -d domain.com` | Subdomain enum |
| crt.sh | `curl "https://crt.sh/?q=%25.domain.com&output=json"` | Certificate transparency |
| Shodan | `shodan search "org:Company"` | Exposed services |
| WhatWeb | `whatweb domain.com` | Technology fingerprinting |

## Phone OSINT

```bash
curl "http://apilayer.net/api/validate?access_key=KEY&number=+1234567890"
phoneinfoga scan -n "+1234567890"
```

## Geolocation

```bash
exiftool -gps:all image.jpg
curl "https://ipinfo.io/IP/json?token=TOKEN"
```
