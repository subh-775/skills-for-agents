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

## Input Types

| Input | Pattern | Primary Path |
|-------|---------|-------------|
| Email | `user@domain.com` | holehe -> HIBP -> social media -> breach check |
| Phone | `+1234567890` | NumVerify -> carrier/location -> social media |
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

## Composability

**Leads:** Any request to gather intelligence on a target
**Defers to:** Process (output structure), Content (broader synthesis), Density (compression)

## References

- [Google Dorks](/skills/osint/references/google-dorks)
- [Leaked Databases](/skills/osint/references/leaked-databases)
- [Tool Playbook](/skills/osint/references/tool-playbook)
