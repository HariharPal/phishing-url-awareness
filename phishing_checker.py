# re library provide regex checks which is used to check whether a url format is correct or not
# urlparse is used to break url string into it's core components
# we need both as needed to checking the format as well as block'ing the component of url
import re
from urllib.parse import urlparse

INFO_MESSAGES = ("No URL entered", "Could not identify", "This text is not", "No listed warning")

REASONS = {
    "Contains an @": "The browser ignores text before @, so the link can look like one site but go to another.",
    "Unusually long": "Long links can hide the real destination far to the right.",
    "Uses an IP": "Honest services normally use readable names; a bare number hides who owns the site.",
    "Contains many": "Stacking many names makes a link look official while hiding the real domain.",
    "Contains a punycode": "Punycode can hide look-alike foreign letters that mimic a real name.",
    "Uses HTTP": "HTTP is not encrypted, so data can be seen on the way.",
}


def inspect_url(raw_url):
    url = raw_url.strip()
    findings = []

    # edge cases
    if not url:
        return ["No URL entered."]

    # entering default configuration based on url we have (not adding ssh key safety if not provided)
    candidate = url if "://" in url else "http://" + url

    try:
        parsed = urlparse(candidate)
        host = (parsed.hostname or "").lower()
    except ValueError:
        return ["This text is not a valid URL format."]

    if not host:
        return ["Could not identify a hostname."]

    # symbol might be used in changing the base url & making more fake url's like
    # if we google abcde@google.com it will redirect us to google.com problematic for
    # user to see real url.
    if "@" in candidate:
        findings.append("Contains an @ symbol; inspect carefully.")

    # Long url may redirect us to another site (possible)
    if len(url) > 100:
        findings.append("Unusually long URL (over 100 characters).")

    # Ip address resolve the ip after it called so dns resolution happen afterward and till that
    # we've opened the site & our data might be compromised so first search ip before calling one
    if re.fullmatch(r"(?:\d{1,3}\.){3}\d{1,3}", host):
        findings.append("Uses an IP address instead of a familiar domain.")

    # Multiple hostname or subdomain looks legitimate company but might be malicious site.
    labels = [part for part in host.split(".") if part]
    if len(labels) >= 5:
        findings.append("Contains many hostname segments/subdomains.")

    # Foreign site with language may use them but still carefull inspection needed
    if "xn--" in host:
        findings.append("Contains a punycode-style hostname.")

    # not given certificate to validate the authenticity is what multiple time differ the
    # phishing link as it need verified certificate from authentic 3rd party. May be good site
    # but without certificate
    if parsed.scheme.lower() == "http":
        findings.append("Uses HTTP. HTTPS alone does not prove trust.")

    # In the end authenticity doens't only rely on the url's it hides so perfectly
    # even professionals may gets into such sites.
    if not findings:
        findings.append("No listed warning signs found. This does NOT prove safety.")

    return findings


def has_warnings(findings):
    return not findings[0].startswith(INFO_MESSAGES)


def explain(finding):
    for start, reason in REASONS.items():
        if finding.startswith(start):
            return reason
    return None


def main():
    print("EWB Phishing URL Awareness Checker")
    print("Text checks only - this program does not open URLs.")

    while True:
        try:
            raw_url = input("\nEnter a sample URL (or type q to quit): ")
        except EOFError:
            print("\nGoodbye! Stay alert online.")
            break
        if raw_url.strip().lower() in ("q", "quit", "exit"):
            print("Goodbye! Stay alert online.")
            break

        findings = inspect_url(raw_url)
        print("\nResult:")
        for number, item in enumerate(findings, start=1):
            print(str(number) + ". " + item)
            reason = explain(item)
            if reason:
                print("   Why it matters: " + reason)

        if has_warnings(findings):
            print("\nREVIEW CAREFULLY: " + str(len(findings)) + " warning sign(s) found.")
        print("Never enter passwords from unexpected links.")


if __name__ == "__main__":
    main()
