# Leaked Databases Reference — OSINT Breach & Leak Sources

> Reference for the /osint skill. Contains breach databases, leak sources, and techniques for checking credential exposure.

---

## Breach Databases

### Have I Been Pwned (HIBP)
**URL:** haveibeenpwned.com
**API:** haveibeenpwned.com/api/v3
**Auth:** `hibp-api-key` header (32-char hex key), `user-agent` header required

**Endpoints:**
- `GET /breachedAccount/{email}` — breaches for email; `?truncateResponse=false`, `?Domain=`
- `GET /breaches` — all breaches (993+)
- `GET /breach/{name}` — single breach details
- `GET /latestBreach` — most recent breach
- `GET /dataClasses` — all data classes
- `GET /pasteAccount/{email}` — paste records
- `GET /stealerLogsByEmail/{email}` — stealer log domains (Pro+)
- `GET /stealerLogsByWebsiteDomain/{domain}` — emails from stealer logs (Pro+)

**Pwned Passwords (free, no auth):**
- `GET https://api.pwnedpasswords.com/range/{first 5 SHA-1 chars}`
- k-anonymity: only first 5 chars of SHA-1 hash sent

**Privacy:** k-anonymity (6 chars for emails, 5 for passwords)
**Rate limits:** HTTP 429 with retry-after header
**License:** CC BY 4.0 for breach data, no attribution for passwords

### DeHashed
**URL:** dehashed.com
**Search by:** email, username, IP address, name, phone number, domain
**Returns:** hashed passwords, plain text passwords (from combo lists), addresses, phone numbers
**API:** Available for bulk queries
**Requires:** Subscription

### Intelligence X (IntelX)
**URL:** intelx.io
**Selectors:** email, domains, IPs, CIDRs, and more
**Data sources:** Pastes (PRO), Darknet Tor (PRO), Darknet I2P (PRO), Whois (PRO), Usenet (PRO), Leaks, Leaks COMB (PRO), Stealer Logs (PRO), WikiLeaks, Public Leaks, Dumpster, Sci-Hub, DNS (PRO), Public Web

**API:**
```bash
# Search
curl -H "x-key: KEY" "https://public.intelx.io/intelligent/search" \
     -d '{"term":"user@example.com","buckets":[],"lookuplevel":0,"maxresults":100,"timeout":5,"datefrom":"","dateto":""}'

# Results
curl -H "x-key: KEY" "https://public.intelx.io/intelligent/search/result?id=SEARCH_ID&limit=100"
```

**Phonebook feature:** phonebook.cz — discover URLs, email addresses, domains
**Free tier:** 50 lookups/day; Researcher tier: 200 lookups/day

### LeakCheck
**URL:** leakcheck.io
**Search by:** email, username, password hash
**API:** Available

---

## Paste Sites

### Monitoring Paste Sites

**Google Dork:**
```
site:pastebin.com "email@domain.com"
site:pastebin.com "password" "domain.com"
site:paste.ee "email@domain.com"
site:ghostbin.com "email@domain.com"
```

**HIBP Paste Endpoint:**
```bash
curl -H "hibp-api-key: KEY" \
     -H "user-agent: OSINT-Tool" \
     "https://haveibeenpwned.com/api/v3/pasteaccount/user@example.com"
```

**IntelX Paste Bucket:**
- Search in "Pastes" bucket for email/domain
- Pro subscription required

---

## Stealer Logs

Stealer logs are databases of credentials stolen by info-stealing malware (RedLine, Raccoon, Vidar, etc.). They contain:
- Website URLs
- Username/email
- Password (plain text)
- IP address
- Timestamp

**Access methods:**
- HIBP Stealer Logs API (Pro+): `GET /stealerLogsByEmail/{email}`
- IntelX Stealer Logs bucket (Pro)
- Dedicated stealer log search services
- Telegram channels (unofficial, use with caution)

---

## GitHub Credential Exposure

**Google Dorks:**
```
site:github.com "password" "email@domain.com"
site:github.com "api_key" "domain.com"
"password" filename:.env "domain.com"
"BEGIN RSA PRIVATE KEY" filename:.pem
"AKIA" filename:.env
```

**Tools:**
- truffleHog — scan git repos for secrets
- git-secrets — prevent secrets from being committed
- gitleaks — scan git repos for secrets
- GitHub Secret Scanning (built-in for public repos)

---

## Dark Web Sources

### Tor Hidden Service Directories

**Ahmia** (ahmia.fi)
- Clearnet accessible Tor search engine
- Indexes .onion sites
- API available

**DarkSearch** (darksearch.io)
- Dark web search engine
- API available for automated searching

**Fresh Onions** (freshonions.net)
- Tor crawler
- Indexes .onion services

**Dark.fail**
- Verified .onion links
- Uptime monitoring

**Tor.taxi**
- Directory of .onion services
- Categorized links

### I2P Sources

**Intelligence X I2P Bucket**
- Pro subscription required
- Search eepsites (.i2p domains)

**I2P Router**
- Install I2P router for direct access
- Access eepsites through I2P network

---

## Monitoring Techniques

### Brand/Domain Monitoring

1. **HIBP Domain Search:** Monitor all breaches for your domain
2. **IntelX Alerts:** Set up alerts for domain mentions
3. **Google Alerts:** Monitor for domain mentions in search results
4. **Paste Monitoring:** Regular dork searches on paste sites
5. **Dark Web Monitoring:** IntelX darknet buckets

### Credential Monitoring

1. **HIBP Notifications:** Register domain for breach notifications
2. **Stealer Log Monitoring:** Regular checks via HIBP Pro or IntelX
3. **GitHub Monitoring:** Regular dork searches for exposed credentials
4. **Paste Monitoring:** Automated paste site scanning

---

## Rate Limits & Pricing

| Service | Free Tier | Paid Tier | Rate Limits |
|---------|-----------|-----------|-------------|
| HIBP API | Password check only | $3.50/month (10k emails) | 429 with retry-after |
| IntelX | 50 lookups/day | Researcher: 200/day | Varies by tier |
| DeHashed | None | Subscription required | Varies |
| LeakCheck | Limited | Subscription required | Varies |
| Shodan | Limited | $69/month (Freelancer) | Varies |
| Hunter.io | 50 credits/month | 12k credits/year ($34) | Varies |
