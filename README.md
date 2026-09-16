# PhishGuard

AI-powered phishing URL detection system built with **Python, Flask, XGBoost, and Google Safe Browsing API**.

## Overview

PhishGuard analyzes URLs and provides a risk classification to help identify potentially malicious links.

The application combines a machine learning model with Google Safe Browsing API checks to provide an additional layer of URL risk assessment.

## Features

- Phishing URL detection using **XGBoost**
- Probability-based risk classification
- URL categories:
  - Safe
  - Medium Risk
  - Dangerous
- Google Safe Browsing API integration
- Batch URL analysis
- Web-based interface using Flask
- Persistent analysis results

## Tech Stack

- **Python**
- **Flask**
- **XGBoost**
- **Google Safe Browsing API**
- **HTML / CSS / JavaScript**

## Project Structure

```text
PhishGuard/
├── app.py
├── data.py
├── feature_extractor.py
├── prepare_dataset.py
├── train.py
├── requirements.txt
├── phishing_model_final.json
├── phishing_model_final.pkl
├── static/
└── templates/
