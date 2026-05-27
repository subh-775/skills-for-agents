# Google Dorks Reference

Common Google dork patterns for OSINT reconnaissance.

## Credential Discovery

```
site:github.com "api_key" "password" "domain.com"
filetype:env "DB_PASSWORD"
"AKIA" filetype:env
```

## Sensitive Documents

```
site:domain.com filetype:pdf
site:domain.com filetype:xlsx "confidential"
```

## Login Portals

```
inurl:/admin/login.php
intitle:"cPanel Login"
```

## Exposed Directories

```
intitle:"index of" "parent directory"
intitle:"index of" ".git"
```

## Social Media Profiles

```
site:linkedin.com/in "company name"
site:twitter.com "target"
```
