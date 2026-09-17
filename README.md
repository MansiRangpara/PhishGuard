# 🛡️ PhishGuard

### ML-Based Phishing URL Detection System

PhishGuard is a web-based phishing URL detection system built with **Python, Flask, XGBoost, and Google Safe Browsing**.

It analyzes submitted URLs using URL-based machine-learning features and an external Safe Browsing threat check, then classifies URLs as **Safe, Medium Risk, or Dangerous**.

🚀 Live Demo: https://phishguard-mocha-ten.vercel.app/
---

## 🚀 Features

* 🔍 Scan single or multiple URLs at once
* 🤖 XGBoost-based phishing detection
* 📊 Phishing probability score
* 🌐 Google Safe Browsing integration
* 🛡️ Trusted-domain recognition
* ⚠️ Brand impersonation detection
* 📈 Risk classification
* 💻 Interactive Flask web interface
* 🔐 API key stored through environment variables
* 📁 Modular feature extraction and model-training scripts

---

## 🧠 How PhishGuard Works

```text
                    User enters URL
                          │
                          ▼
                  URL Normalization
                          │
                          ▼
                 Feature Extraction
                          │
             ┌────────────┴────────────┐
             │                         │
             ▼                         ▼
       Trusted Domain?          Brand Impersonation?
             │                         │
          Yes│                         │Yes
             ▼                         ▼
           SAFE                    DANGEROUS
             │
            No
             │
             ▼
       XGBoost ML Model
             │
             ▼
     Phishing Probability
             │
             ▼
     Google Safe Browsing
             │
             ▼
       Final Classification
```

---

## 📊 Risk Classification

|                 Phishing Probability | Result         |
| -----------------------------------: | -------------- |
|                          0% – 29.99% | 🟢 Safe        |
|                         30% – 69.99% | 🟡 Medium Risk |
|                           70% – 100% | 🔴 Dangerous   |
| Google Safe Browsing threat detected | 🔴 Dangerous   |

Google Safe Browsing can independently identify URLs that match known threat data.

---

## 🧪 URL Features

The XGBoost model uses 16 URL-based features:

```text
UrlLength
UrlLengthRT
HostnameLength
PathLength
QueryLength
NumDot
NumDashInHostname
NumHash
NumAmpersand
PathLevel
RandomString
NoHttps
EmbeddedBrandName
AtSymbol
SubdomainLevel
DomainInPaths
```

These features are extracted by `feature_extractor.py`.

---

## 🛠️ Tech Stack

### Backend

* Python
* Flask

### Machine Learning

* XGBoost
* Scikit-learn
* Pandas
* Joblib

### Security / Threat Intelligence

* Google Safe Browsing API

### Frontend

* HTML
* CSS
* JavaScript

---

## 📂 Project Structure

```text
PhishGuard/
│
├── .gitignore
├── README.md
│
└── backend/
    ├── app.py
    ├── data.py
    ├── feature_extractor.py
    ├── phishing_model_final.pkl
    ├── prepare_dataset.py
    ├── requirements.txt
    ├── train.py
    │
    ├── static/
    │   ├── favicon.ico
    │   ├── hyperspeed.js
    │   ├── script.js
    │   └── style.css
    │
    └── templates/
        └── index.html
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/MansiRangpara/PhishGuard.git
cd PhishGuard
```

### 2. Install dependencies

```bash
python -m pip install -r backend/requirements.txt
```

The project pins the XGBoost version used by the trained model:

```text
xgboost==3.4.1
```

### 3. Configure Google Safe Browsing

Create a file:

```text
backend/.env
```

Add:

```text
GOOGLE_SAFE_BROWSING_API_KEY=YOUR_API_KEY
```

Do not commit `.env` to GitHub.

The application reads the API key using an environment variable.

---

## ▶️ Run PhishGuard

From the project root:

```bash
cd backend
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

---

## 🔐 Security

Sensitive and unnecessary files are excluded from the repository using `.gitignore`.

The following files should remain local:

```text
.env
data.csv
dataset_features.csv
__pycache__/
.venv/
```

The Google Safe Browsing API key should never be hard-coded into `app.py` or committed to GitHub.

---

## 🧪 Retraining the Model

The raw dataset is intentionally not included in the repository.

To retrain the model locally:

1. Place the dataset in:

```text
backend/data.csv
```

2. Generate the feature dataset:

```bash
python backend/prepare_dataset.py
```

3. Train the XGBoost model:

```bash
python backend/train.py
```

This generates:

```text
backend/phishing_model_final.pkl
```

---

## 📝 Dataset

The project uses a labeled URL dataset containing benign and malicious URL examples.

The raw dataset and generated feature dataset are excluded from GitHub because of their size and because they are not required to run the already-trained application.

---

## 🌐 Google Safe Browsing

PhishGuard sends submitted URLs to Google Safe Browsing for an additional threat check.

The application combines:

```text
Machine Learning
       +
Google Safe Browsing
       +
Trusted Domain / Brand Checks
       ↓
Final Risk Result
```

A Google Safe Browsing threat match results in a **Dangerous** classification.

---

## ⚠️ Important Note

PhishGuard is a security research and educational project.

A URL classified as **Safe** does not guarantee that the website is completely harmless. The system combines machine-learning predictions, URL characteristics, trusted-domain rules, and available Safe Browsing results to estimate risk.

---

## 👩‍💻 Author

**Mansi Rangpara**

GitHub: [@MansiRangpara](https://github.com/MansiRangpara)

---

## ⭐ Future Improvements

* Improve the ML model with additional URL and domain features
* Add domain age and WHOIS-based analysis
* Add IP reputation checks
* Improve probability calibration
* Add scan history and analytics
* Add model performance dashboard
* Deploy PhishGuard as a production web application

````

Now let's update the actual file **one command at a time**.

From:

```text
C:\Users\MANSI RANGPARA\Documents\PhishGuard
````

run:

```cmd
notepad README.md
```

Replace the existing README with the content above, save it, and tell me `done`. Then we'll check it before pushing.
