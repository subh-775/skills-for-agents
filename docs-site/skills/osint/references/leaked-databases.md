# Leaked Database Reference

Sources and methods for checking leaked credentials and data breaches.

## HIBP (Have I Been Pwned)

```bash
# Breach check
curl -H "hibp-api-key: KEY" "https://haveibeenpwned.com/api/v3/breachedaccount/email@example.com"

# Paste check
curl -H "hibp-api-key: KEY" "https://haveibeenpwned.com/api/v3/pasteaccount/email@example.com"

# Password hash check (k-anonymity)
curl "https://api.pwnedpasswords.com/range/SHA1_PREFIX"
```

## DeHashed

Raw breach data search. Requires account.

## IntelX

Darknet buckets, stealer logs, paste monitoring.

## Stealer Log Databases

Infostealer credential dumps — often more recent than traditional breaches.
