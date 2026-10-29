# Test Results

Python version used: 3.13.13 | Date: 29/10/2926


| # | Input | Expected result | Actual result | Pass/Fail |
|---|-------|-----------------|---------------|-----------|
| 1 | https://www.example.com/login | No listed warning signs | No listed warning signs found. This does NOT prove safety. | PASS |
| 2 | http://192.0.2.10/account | IP address + HTTP | Uses an IP address instead of a familiar domain.; Uses HTTP. HTTPS alone does not prove trust. | PASS |
| 3 | http://example.com@sample.invalid/login | @ symbol + HTTP | Contains an @ symbol; inspect carefully.; Uses HTTP. HTTPS alone does not prove trust. | PASS |
| 4 | https://a.b.c.d.e.example.invalid/path | Many hostname segments | Contains many hostname segments/subdomains. | PASS |
| 5 | https://xn--example.invalid/ | Punycode-style hostname | Contains a punycode-style hostname. | PASS |

## Bonus checks

| Input | Result |
|-------|--------|
| (empty, just Enter) | No URL entered. |
| www.example.com | Uses HTTP. (missing scheme is treated as http://) |
| https://secure-login.example.invalid | No listed warning signs found. A tricky name can slip through. |
| http://[bad | This text is not a valid URL format. (no crash after Improvement C) |

## Notes

All five required sample URL's produced the expected warning categories in this run.
Four bonus inputs with edge cases also behaved as expected including the malformed URL.

I learned how to identify potentially suspicious URLs by checking their pattern domain 
names & other signs which may associate with phishing attacks. But these all combined 
also cannot guarantee that URL is fishy or not.