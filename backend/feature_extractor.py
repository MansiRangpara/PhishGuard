import re
from urllib.parse import urlparse


# =========================================================
# TRUSTED DOMAINS
# =========================================================

TRUSTED_DOMAINS = {
    "google.com",
    "youtube.com",
    "gmail.com",
    "amazon.com",
    "microsoft.com",
    "apple.com",
    "github.com",
    "linkedin.com",
    "facebook.com",
    "instagram.com",
    "wikipedia.org",
    "reddit.com",
    "netflix.com",
    "paypal.com",
    "stackoverflow.com",
    "mozilla.org",
    "python.org",
    "ubuntu.com",
    "yahoo.com",
    "bing.com"
}


# =========================================================
# URL NORMALIZATION
# =========================================================

def normalize_url(url):
    """
    Adds a temporary scheme when the user enters:

        google.com

    instead of:

        https://google.com
    """

    url = str(url).strip()

    if not url:
        return "", None

    if not re.match(
        r"^[a-zA-Z][a-zA-Z0-9+.-]*://",
        url
    ):
        parse_url = "http://" + url
    else:
        parse_url = url

    try:
        parsed = urlparse(parse_url)
        return url, parsed

    except Exception:
        return url, None


# =========================================================
# REGISTERED DOMAIN
# =========================================================

def get_registered_domain(hostname):
    """
    Example:

        www.google.com
        -> google.com

        accounts.google.com
        -> google.com
    """

    hostname = hostname.lower().strip(".")

    parts = hostname.split(".")

    if len(parts) >= 2:
        return ".".join(parts[-2:])

    return hostname


# =========================================================
# TRUSTED DOMAIN CHECK
# =========================================================

def is_trusted_domain(hostname):

    registered_domain = get_registered_domain(
        hostname
    )

    return registered_domain in TRUSTED_DOMAINS


# =========================================================
# RANDOM STRING DETECTION
# =========================================================

def has_random_string(path):

    tokens = re.findall(
        r"[A-Za-z0-9]{10,}",
        path
    )

    for token in tokens:

        has_letters = bool(
            re.search(r"[A-Za-z]", token)
        )

        has_numbers = bool(
            re.search(r"\d", token)
        )

        if has_letters and has_numbers:
            return 1

    return 0


# =========================================================
# BRAND IMPERSONATION
# =========================================================

def suspicious_brand_in_hostname(hostname):

    hostname = hostname.lower()

    brands = [
        "paypal",
        "google",
        "linkedin",
        "facebook",
        "amazon",
        "microsoft",
        "apple"
    ]

    registered_domain = get_registered_domain(
        hostname
    )

    for brand in brands:

        if brand in hostname:

            official_domain = f"{brand}.com"

            if registered_domain != official_domain:
                return 1

    return 0


# =========================================================
# FEATURE EXTRACTION
# =========================================================

def extract_features(url):

    original_url, parsed = normalize_url(url)

    # -----------------------------------------------------
    # Invalid URL
    # -----------------------------------------------------

    if parsed is None:

        return {
            "UrlLength": len(original_url),
            "UrlLengthRT": len(original_url) ** 0.5,
            "HostnameLength": 0,
            "PathLength": len(original_url),
            "QueryLength": 0,
            "NumDot": 0,
            "NumDashInHostname": 0,
            "NumHash": original_url.count("#"),
            "NumAmpersand": original_url.count("&"),
            "PathLevel": 0,
            "RandomString": 0,
            "NoHttps": 1,
            "EmbeddedBrandName": 0,
            "AtSymbol": int("@" in original_url),
            "SubdomainLevel": 0,
            "DomainInPaths": 0
        }

    hostname = (
        parsed.hostname or ""
    ).lower()

    path = parsed.path or ""

    query = parsed.query or ""

    # -----------------------------------------------------
    # Features
    # -----------------------------------------------------

    features = {

        "UrlLength":
            len(original_url),

        "UrlLengthRT":
            len(original_url) ** 0.5,

        "HostnameLength":
            len(hostname),

        "PathLength":
            len(path),

        "QueryLength":
            len(query),

        "NumDot":
            hostname.count("."),

        "NumDashInHostname":
            hostname.count("-"),

        "NumHash":
            original_url.count("#"),

        "NumAmpersand":
            original_url.count("&"),

        "PathLevel":
            len([
                part
                for part in path.split("/")
                if part
            ]),

        "RandomString":
            has_random_string(path),

        "NoHttps":
            int(
                parsed.scheme.lower() != "https"
            ),

        "EmbeddedBrandName":
            suspicious_brand_in_hostname(
                hostname
            ),

        "AtSymbol":
            int("@" in original_url),

        "SubdomainLevel":
            max(
                0,
                hostname.count(".") - 1
            ),

        "DomainInPaths":
            int(
                bool(hostname)
                and hostname.split(".")[0]
                in path.lower()
            )
    }

    return features