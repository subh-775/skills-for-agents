---
title: OSINT
description: Open Source Intelligence engine for deep background research
---

# OSINT

Open Source Intelligence engine for deep background research on any target.

**Domain:** Analysis
**Composable:** Yes
**Yields to:** Process

## Overview

Takes minimal input (email, phone, name, username, company, IP, domain) and produces comprehensive intelligence: social media accounts, leaked credentials, workplace, location, network infrastructure, exposed documents, dark web presence, and more.

## Triggers

- `/osint`
- "osint", "recon", "intelligence", "background check", "investigate"
- "find info on", "look up", "search for"
- "email lookup", "phone lookup", "username search"
- "breach check", "leak check", "social media search"
- "people search", "company research", "domain recon"
- "subdomain enum", "port scan", "google dork", "dark web search"

## Examples

### Email reconnaissance
```
/osint investigate target@example.com — find all accounts, breaches, social media
```

### Username search across platforms
```
/osint search for username "bsbarkur" across 3400+ sites
```

### Domain recon
```
/osint recon example.com — subdomains, tech stack, exposed services
```

### Phone lookup
```
/osint who owns phone number +1-555-123-4567?
```

### Breach check
```
/osint check if my email has been in any data breaches
```

### Company research
```
/osint research Acme Corp — employees, infrastructure, public filings
```

## Input Types

| Input | Pattern | Primary Path |
|-------|---------|-------------|
| Email | `user@domain.com` | holehe -> HIBP -> social media -> breach check |
| Phone | `+123****7890` | NumVerify -> carrier/location -> social media |
| Username | `@handle` | Sherlock + maigret -> 3,400+ sites |
| Name | `First Last` | People search -> LinkedIn -> public records |
| Company | Company name | Hunter.io -> employees -> Shodan -> subdomains |
| IP | `x.x.x.x` | Shodan -> geolocation -> open ports -> services |
| Domain | `example.com` | Subfinder -> crt.sh -> Shodan -> Google dorks |

## OSINT Pipeline

### Phase 1: Passive Reconnaissance

1. **Account Discovery** — holehe, Sherlock, maigret, social-analyzer
2. **Breach & Leak Check** — HIBP, DeHashed, IntelX
3. **Social Media Deep Dive** — Instaloader, Google cache, Wayback Machine
4. **People Search** — Pipl, Spokeo, WhitePages, public records
5. **Infrastructure Recon** — Subfinder, Amass, crt.sh, Shodan, WhatWeb
6. **Document Discovery** — Google dorks, GitHub dorking, paste sites
7. **Dark Web Monitoring** — IntelX darknet, Ahmia, stealer logs

### Phase 2: Analysis & Correlation

- Identity resolution across platforms
- Location triangulation
- Workplace verification
- Credential exposure aggregation
- Network mapping

### Phase 3: Intelligence Report

Structured JSON output with identity, social media, breaches, infrastructure, documents, dark web findings, and confidence scoring.

## Output Format

All OSINT reports are saved as **visual HTML dashboards** — not plain text.

### Folder Structure

```
~/osint/<tag>_<DD>_<MONTH>_<YYYY>/
├── index.html          # Executive dashboard (entry point)
├── identity.html       # Identity & social media profiles
├── infrastructure.html # Network, domains, tech stack
├── breaches.html       # Breach/leak data + dark web findings
├── sources.html        # Full source list + methodology
├── assets/
│   ├── style.css       # Dark-theme stylesheet
│   └── charts.js       # Chart.js visualizations
└── data/
    └── findings.json   # Machine-readable backup
```

### Visual Design

- **Dark theme** (#0d1117 background, light text, accent colors)
- **Stat cards** — confidence level, platforms found, breach count, risk score
- **Charts** — breach timeline (bar), platform presence (doughnut), risk radar
- **Color-coded badges** — green (high confidence), yellow (medium), red (low)
- **Collapsible sections** for verbose data (raw breaches, full source list)
- **Responsive** — works on desktop and mobile
- **Self-contained** — Chart.js (CDN) is the only external dependency

### index.html Dashboard

The main report opens with impact stat cards, a platform presence grid, breach timeline chart, risk assessment radar, and key findings cards. Links to supporting pages (identity, infrastructure, breaches, sources).

## Automation Scripts

OSINT ships with production-ready scripts that chain multiple tools together.

### Quick Start

```bash
# Primary: Python-based (no external deps, works everywhere)
python scripts/osint_core.py orchestrator <target> <type>

# Individual tools
python scripts/osint_core.py username <username>   # 50+ sites
python scripts/osint_core.py email <email>          # platforms + domain
python scripts/osint_core.py domain <domain>        # DNS + certs + headers
python scripts/osint_core.py ip <ip>                # geo + ports + reputation
python scripts/osint_core.py social <username>      # GitHub + Reddit + npm
python scripts/osint_core.py dork <domain>          # 20+ Google dork queries
```

### Scripts

**Primary (osint_core.py — no deps, single output dir):**

| Command | What It Does |
|---------|-------------|
| `orchestrator <target> <type>` | Full recon, all tools, one folder |
| `username <user>` | 50+ sites via parallel HTTP |
| `email <email>` | Platforms + domain + username |
| `domain <domain>` | DNS + crt.sh + headers + robots.txt |
| `ip <ip>` | ipinfo + Shodan + AbuseIPDB + VirusTotal |
| `social <user>` | GitHub + Reddit + Keybase + npm + PyPI |
| `dork <domain>` | 20+ Google dork queries |

**Supplementary (bash — requires CLI tools via `setup.sh`):**

| Script | What It Does |
|--------|-------------|
| `username_enum.sh` | Sherlock + Maigret (3400+ sites) |
| `email_osint.sh` | Holehe + HIBP + h8mail |
| `domain_recon.sh` | theHarvester + Subfinder |
| `setup.sh` | Install all CLI tools |

### Target Types

```
email    → platforms + breaches + domain recon
phone    → carrier + location + social links
username → 50+ sites + social profiles
domain   → DNS + certs + headers + dorks
ip       → geo + ports + services + reputation
person   → username + social + email
```

All output goes to ONE folder: `~/osint/<target>_<date>/`. Orchestrator merges everything into `master_report.json`.

## Composability

**Leads:** Any request to gather intelligence on a target
**Defers to:** Process (output structure), Content (broader synthesis), Density (compression)

## References

- [Google Dorks](/skills/osint/references/google-dorks)
- [Leaked Databases](/skills/osint/references/leaked-databases)
- [Tool Playbook](/skills/osint/references/tool-playbook)
