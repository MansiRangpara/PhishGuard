
from flask import Flask, render_template, request
import pandas as pd
import joblib
import requests
import os

from dotenv import load_dotenv

from feature_extractor import (
    extract_features,
    is_trusted_domain,
    get_registered_domain,
    suspicious_brand_in_hostname
)

load_dotenv()

app = Flask(__name__)


# =========================================================
# MODEL
# =========================================================

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "phishing_model_final.pkl"
)

try:
    model = joblib.load(MODEL_PATH)

    print("Phishing model loaded successfully.")
    print("Model classes:", model.classes_)
    print("Model features:", model.feature_names_in_)

except Exception as e:
    print("ERROR loading model:", e)
    model = None


# =========================================================
# GOOGLE SAFE BROWSING
# =========================================================

API_KEY = os.getenv(
    "GOOGLE_SAFE_BROWSING_API_KEY"
)

if API_KEY:
    API_URL = (
        "https://safebrowsing.googleapis.com/"
        "v4/threatMatches:find?key="
        + API_KEY
    )
else:
    API_URL = None

    print(
        "WARNING: Google Safe Browsing API key "
        "is not configured."
    )


def check_google_safe_browsing(url):
    """
    Returns:
        False -> Google found a threat
        True  -> Google found no threat
        None  -> API request failed / unavailable
    """

    if not API_URL:
        print(
            "Google Safe Browsing API key is missing."
        )
        return None

    payload = {
        "client": {
            "clientId": "phishguard",
            "clientVersion": "1.0"
        },
        "threatInfo": {
            "threatTypes": [
                "MALWARE",
                "SOCIAL_ENGINEERING",
                "UNWANTED_SOFTWARE",
                "POTENTIALLY_HARMFUL_APPLICATION"
            ],
            "platformTypes": [
                "ANY_PLATFORM"
            ],
            "threatEntryTypes": [
                "URL"
            ],
            "threatEntries": [
                {
                    "url": url
                }
            ]
        }
    }

    try:
        response = requests.post(
            API_URL,
            json=payload,
            timeout=10
        )

        print(
            f"Google Safe Browsing status for {url}: "
            f"{response.status_code}"
        )

        print(
            "Google response:",
            response.text
        )

        # Google API request failed
        if response.status_code != 200:
            return None

        data = response.json()

        # Google found a threat
        if data.get("matches"):
            return False

        # Google did not find a threat
        return True

    except requests.RequestException as e:

        print(
            f"Google Safe Browsing request error "
            f"for {url}: {e}"
        )

        if getattr(e, "response", None) is not None:
            print(
                "Google error response:",
                e.response.text
            )

        return None

    except Exception as e:

        print(
            "Unexpected Google Safe Browsing error:",
            e
        )

        return None


# =========================================================
# HOME
# =========================================================

@app.route(
    "/",
    methods=["GET", "POST"]
)
@app.route("/", methods=["GET", "POST"])
def index():

    result = {}

    if request.method == "POST":

        raw_urls = request.form.get("urls", "")

        urls = list(
            dict.fromkeys(
                url.strip()
                for url in raw_urls.splitlines()
                if url.strip()
            )
        )

        for url in urls:

            # =================================================
            # GOOGLE SAFE BROWSING
            # =================================================

            google_result = check_google_safe_browsing(url)

            print(
                f"[Google] {url} -> {google_result}"
            )

            # Google explicitly detected a threat
            if google_result is False:

                result[url] = {
                    "type": "Dangerous",
                    "prob": "100.00",
                    "message":
                        "Google Safe Browsing reported a threat.",
                    "google_checked": True,
                    "google_threat": True
                }

                continue


            # =================================================
            # EXTRACT HOSTNAME
            # =================================================

            try:

                from urllib.parse import urlparse

                parse_url = url

                if not (
                    parse_url.startswith("http://")
                    or parse_url.startswith("https://")
                ):
                    parse_url = "http://" + parse_url

                parsed = urlparse(parse_url)

                hostname = (
                    parsed.hostname or ""
                ).lower()

            except Exception:

                result[url] = {
                    "type": "Unknown",
                    "prob": "",
                    "message": "Invalid URL.",
                    "google_checked":
                        google_result is not None,
                    "google_threat": False
                }

                continue


            # =================================================
            # TRUSTED DOMAIN CHECK
            # =================================================

            if is_trusted_domain(hostname):

                registered_domain = (
                    get_registered_domain(hostname)
                )

                print(
                    f"[Trusted Domain] {url} -> "
                    f"{registered_domain}"
                )

                result[url] = {
                    "type": "Safe",
                    "prob": "0.00",
                    "message":
                        f"Recognized trusted domain: "
                        f"{registered_domain}",
                    "google_checked":
                        google_result is not None,
                    "google_threat": False
                }

                continue


            # =================================================
            # BRAND IMPERSONATION CHECK
            # =================================================

            if suspicious_brand_in_hostname(hostname):

                print(
                    f"[Brand Warning] {url}"
                )

                result[url] = {
                    "type": "Dangerous",
                    "prob": "100.00",
                    "message":
                        "Possible brand impersonation detected.",
                    "google_checked":
                        google_result is not None,
                    "google_threat":
                        google_result is False
                }

                continue


            # =================================================
            # FEATURE EXTRACTION
            # =================================================

            try:

                features = extract_features(url)

                X_test = pd.DataFrame(
                    [features]
                )

            except Exception as e:

                print(
                    f"Feature extraction error "
                    f"for {url}: {e}"
                )

                result[url] = {
                    "type": "Unknown",
                    "prob": "",
                    "message":
                        "Could not extract URL features.",
                    "google_checked":
                        google_result is not None,
                    "google_threat": False
                }

                continue


            # =================================================
            # MODEL CHECK
            # =================================================

            if model is None:

                result[url] = {
                    "type": "Unknown",
                    "prob": "",
                    "message":
                        "Phishing model is unavailable.",
                    "google_checked":
                        google_result is not None,
                    "google_threat": False
                }

                continue


            # =================================================
            # ML PREDICTION
            # =================================================

            try:

                probabilities = (
                    model.predict_proba(X_test)[0]
                )

                class_list = list(
                    model.classes_
                )

                phishing_index = (
                    class_list.index(1)
                )

                phishing_prob = (
                    probabilities[
                        phishing_index
                    ] * 100
                )

            except Exception as e:

                print(
                    f"Prediction error "
                    f"for {url}: {e}"
                )

                result[url] = {
                    "type": "Unknown",
                    "prob": "",
                    "message":
                        "Model prediction failed.",
                    "google_checked":
                        google_result is not None,
                    "google_threat": False
                }

                continue


            # =================================================
            # DEBUG
            # =================================================

            print(
                f"[PhishGuard] {url} | "
                f"ML phishing probability: "
                f"{phishing_prob:.2f}% | "
                f"Google result: "
                f"{google_result}"
            )


            # =================================================
            # FINAL CLASSIFICATION
            # =================================================

            if phishing_prob >= 70:

                status = "Dangerous"

                message = (
                    "High phishing probability "
                    "detected by the ML model."
                )

            elif phishing_prob >= 30:

                status = "Medium Risk"

                message = (
                    "The ML model detected "
                    "suspicious URL characteristics."
                )

            else:

                status = "Safe"

                message = (
                    "No major suspicious characteristics "
                    "were detected."
                )


            # =================================================
            # SAVE RESULT
            # =================================================

            result[url] = {

                "type": status,

                "prob":
                    f"{phishing_prob:.2f}",

                "message":
                    message,

                "google_checked":
                    google_result is not None,

                "google_threat":
                    google_result is False
            }


    return render_template(
        "index.html",
        result=result
    )


# =========================================================
# RUN FLASK
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=False
    )

