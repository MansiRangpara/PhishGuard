from flask import Flask, render_template, request
import pandas as pd
import joblib
import requests
from feature_extractor import extract_features
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Load trained model
model = joblib.load("phishing_model_final.pkl")

# Google Safe Browsing API
API_KEY = os.getenv("GOOGLE_SAFE_BROWSING_API_KEY")
API_URL = "https://safebrowsing.googleapis.com/v4/threatMatches:find"

def check_google_safe_browsing(url):
    payload = {
        "client": {
            "clientId": "phishing-detector",
            "clientVersion": "1.0"
        },
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING",
                            "UNWANTED_SOFTWARE", "POTENTIALLY_HARMFUL_APPLICATION"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url}]
        }
    }
    try:
        headers = {
         "X-Goog-Api-Key": API_KEY,
         "Content-Type": "application/json"
        }

        response = requests.post(API_URL, headers=headers, json=payload)
        data = response.json()
        if "matches" in data:
            return False
        else:
            return True
    except:
        return None

@app.route("/", methods=["GET", "POST"])
def index():
    result = {}
    if request.method == "POST":
        urls = list(dict.fromkeys([url.strip() for url in request.form.get("urls").splitlines() if url.strip()]))
        if urls:
            X_test = pd.DataFrame([extract_features(url) for url in urls])
            probs = model.predict_proba(X_test)

            for url, prob in zip(urls, probs):
                phishing_prob = prob[1] * 100
                status = ""

                if phishing_prob >= 70:
                    api_safe = check_google_safe_browsing(url)
                    if api_safe is True:
                        status = "Safe"
                    elif api_safe is False:
                        status = "Dangerous"
                    else:
                        status = f"Dangerous ({phishing_prob:.2f}% phishing probability)"
                else:
                    if phishing_prob < 30:
                        status = "Safe"
                    else:
                        status = f"Medium Risk ({phishing_prob:.2f}% phishing probability)"

                if status in ["Medium Risk", "Dangerous"]:
                    result[url] = {"type": status, "prob": f"{phishing_prob:.2f}"}
                else:
                     result[url] = {"type": status, "prob": ""}


    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)  