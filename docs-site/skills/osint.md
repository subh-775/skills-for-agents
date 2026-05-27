1|---
     2|title: OSINT
     3|description: Open Source Intelligence engine for deep background research
     4|---
     5|
     6|# OSINT
     7|
     8|Open Source Intelligence engine for deep background research on any target.
     9|
    10|**Domain:** Analysis
    11|**Composable:** Yes
    12|**Yields to:** Process
    13|
    14|## Overview
    15|
    16|Takes minimal input (email, phone, name, username, company, IP, domain) and produces comprehensive intelligence: social media accounts, leaked credentials, workplace, location, network infrastructure, exposed documents, dark web presence, and more.
    17|
    18|## Triggers
    19|
    20|- `/osint`
    21|- "osint", "recon", "intelligence", "background check", "investigate"
    22|- "find info on", "look up", "search for"
    23|- "email lookup", "phone lookup", "username search"
    24|- "breach check", "leak check", "social media search"
    25|- "people search", "company research", "domain recon"
    26|- "subdomain enum", "port scan", "google dork", "dark web search"
    27|
    28|## Input Types
    29|
    30|| Input | Pattern | Primary Path |
    31||-------|---------|-------------|
    32|| Email | `user@domain.com` | holehe -> HIBP -> social media -> breach check |
    33|| Phone | `+123****7890` | NumVerify -> carrier/location -> social media |
    34|| Username | `@handle` | Sherlock + maigret -> 3,400+ sites |
    35|| Name | `First Last` | People search -> LinkedIn -> public records |
    36|| Company | Company name | Hunter.io -> employees -> Shodan -> subdomains |
    37|| IP | `x.x.x.x` | Shodan -> geolocation -> open ports -> services |
    38|| Domain | `example.com` | Subfinder -> crt.sh -> Shodan -> Google dorks |
    39|
    40|## OSINT Pipeline
    41|
    42|### Phase 1: Passive Reconnaissance
    43|
    44|1. **Account Discovery** — holehe, Sherlock, maigret, social-analyzer
    45|2. **Breach & Leak Check** — HIBP, DeHashed, IntelX
    46|3. **Social Media Deep Dive** — Instaloader, Google cache, Wayback Machine
    47|4. **People Search** — Pipl, Spokeo, WhitePages, public records
    48|5. **Infrastructure Recon** — Subfinder, Amass, crt.sh, Shodan, WhatWeb
    49|6. **Document Discovery** — Google dorks, GitHub dorking, paste sites
    50|7. **Dark Web Monitoring** — IntelX darknet, Ahmia, stealer logs
    51|
    52|### Phase 2: Analysis & Correlation
    53|
    54|- Identity resolution across platforms
    55|- Location triangulation
    56|- Workplace verification
    57|- Credential exposure aggregation
    58|- Network mapping
    59|
    60|### Phase 3: Intelligence Report
    61|
    62|Structured JSON output with identity, social media, breaches, infrastructure, documents, dark web findings, and confidence scoring.
    63|
    64|## Composability
    65|
    66|**Leads:** Any request to gather intelligence on a target
    67|**Defers to:** Process (output structure), Content (broader synthesis), Density (compression)
    68|
    69|## References
    70|
    71|- [Google Dorks](/skills/osint/references/google-dorks)
    72|- [Leaked Databases](/skills/osint/references/leaked-databases)
    73|- [Tool Playbook](/skills/osint/references/tool-playbook)
    74|

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
