# feature_extractor.py
import re
from urllib.parse import urlparse

def has_random_string(s):
    return int(bool(re.search(r'[a-zA-Z]{8,}', s)))

def extract_features(url):
    parsed = urlparse(url)
    hostname = parsed.hostname or ""
    path = parsed.path or ""
    query = parsed.query or ""

    features = {
        "UrlLength": len(url),
        "UrlLengthRT": len(url) ** 0.5,
        "HostnameLength": len(hostname),
        "PathLength": len(path),
        "QueryLength": len(query),
        "NumDot": hostname.count("."),
        "NumDashInHostname": hostname.count("-"),
        "NumHash": url.count("#"),
        "NumAmpersand": url.count("&"),
        "PathLevel": path.count("/"),
        "RandomString": has_random_string(path),
        "NoHttps": int(parsed.scheme != "https"),
        "EmbeddedBrandName": int(bool(re.search(r'(paypal|google|linkedin|facebook|amazon)', url, re.I))),
        "AtSymbol": int("@" in url),
        "SubdomainLevel": hostname.count(".") - 1,
        "DomainInPaths": int(hostname.split(".")[0] in path)
    }
    return features
