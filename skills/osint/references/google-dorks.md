# Google Dorks Reference — OSINT Search Operators

> Reference for the /osint skill. Contains Google dork operators and categorized dork patterns for finding exposed data.

---

## Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `site:` | Restrict to specific domain | `site:linkedin.com "John Smith"` |
| `filetype:` | Filter by file extension | `filetype:pdf "confidential"` |
| `ext:` | Same as filetype | `ext:sql "password"` |
| `inurl:` | Term must appear in URL | `inurl:admin login` |
| `intitle:` | Term must appear in title | `intitle:"index of"` |
| `allintitle:` | All terms in title | `allintitle: admin login portal` |
| `intext:` | Term in page body | `intext:"ssn" filetype:xls` |
| `allintext:` | All terms in body | `allintext: username password email` |
| `inanchor:` | Term in link anchor text | `inanchor:"click here"` |
| `cache:` | Show cached version | `cache:example.com` |
| `link:` | Pages linking to URL | `link:example.com` |
| `related:` | Similar sites | `related:example.com` |
| `before:` | Before date | `before:2024-01-01` |
| `after:` | After date | `after:2023-01-01` |
| `..` | Number range | `"phone" 555..999` |
| `*` | Wildcard | `"the * jumped over"` |
| `OR` / `|` | Boolean OR | `site:github.com OR site:gitlab.com` |
| `-` | Exclude term | `"password" -site:github.com` |
| `" "` | Exact phrase | `"exact match"` |
| `( )` | Grouping | `(site:gov OR site:mil) filetype:pdf` |

---

## Dork Categories

### Exposed Credentials & API Keys

```
site:github.com "api_key" "password" "domain.com"
filetype:env "DB_PASSWORD"
"AKIA" filetype:env
"BEGIN RSA PRIVATE KEY" filetype:key
filetype:json "api_key"
filetype:yml "password" inurl:config
filetype:properties "password"
```

### Sensitive Documents

```
site:domain.com filetype:pdf
site:domain.com filetype:xlsx "confidential"
site:domain.com filetype:docx "internal"
"@domain.com" filetype:pdf
"@domain.com" filetype:xlsx
filetype:csv "ip address" "name"
```

### Exposed Databases

```
intitle:"index of" "database.sql"
filetype:sql "CREATE TABLE" "password"
intitle:"MongoDB" "database" inurl:27017
filetype:sql "INSERT INTO" "password"
filetype:log "username password"
```

### Login Portals

```
inurl:/admin/login.php
inurl:wp-login.php
intitle:"cPanel Login"
intitle:"phpMyAdmin" "Welcome to phpMyAdmin"
inurl:/wp-admin
intitle:"Dashboard [Jenkins]"
```

### Exposed Directories

```
intitle:"index of" "parent directory"
intitle:"index of" "/backup"
intitle:"index of" "/config"
intitle:"index of" "/uploads"
intitle:"index of" ".git"
intitle:"index of" "passwords.txt"
```

### Error Messages

```
"Warning: mysql_connect()" "error"
"ORA-00921: unexpected end of SQL command"
"Microsoft OLE DB Provider for ODBC Drivers error"
"Fatal error: require()"
```

### Webcams & IoT

```
inurl:top.htm inurl:currenttime
intitle:"webcamXP"
intitle:"IP Camera"
intitle:"Home" "View Camera"
intitle:"HP LaserJet" ininfo:hpp/
```

### Social Media Profiles

```
site:linkedin.com/in "company name"
site:twitter.com "target"
site:facebook.com "email@domain.com"
site:reddit.com "username"
```

### Email Discovery

```
"@domain.com" filetype:pdf
"@domain.com" filetype:xlsx
site:domain.com "@domain.com"
"email" "domain.com" filetype:csv
```

### Vulnerable Servers

```
intitle:"Apache HTTP Server" intitle:"documentation"
intitle:"IIS Windows Server"
intitle:"nginx" "Welcome to nginx!"
intitle:"setup" "broadband router"
```

### Network & Vulnerability Data

```
filetype:csv "ip address" "name"
intitle:"nessus scan report"
filetype:pcap
"SQL injection" site:exploit-db.com
filetype:pdf "CVE"
```
