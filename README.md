# 🔍 Cloud Forensics Automation Platform
> **Enterprise-grade File Evidence Collector & Breach Detection Simulator**

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Framework-Flask-lightgrey.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Topic](https://img.shields.io/badge/Domain-Cloud%20Forensics-orange.svg)

## 📋 Table of Contents
- [Overview](#overview)
- [How It Works](#how-it-works)
- [Key Features](#key-features)
- [Project Structure](#project-structure)
- [Setup & Installation](#setup--installation)
- [Educational Value](#educational-value)

---

## 🌟 Overview
The **Cloud Forensics Automation Platform** is a specialized tool designed for digital forensic investigators and security students. It simulates a **post-breach e-commerce scenario** where an investigator must collect evidence from potentially tampered file systems. 

This platform extracts mandatory file metadata (Creation & Last Modified dates) and uses a custom algorithm to flag suspicious activity, helping detect if payment gateways, product logs, or transaction scripts have been compromised.

---

## ⚙️ How It Works
The system follows a standard forensics workflow:
1.  **Ingestion**: Files are uploaded to the secure `uploads/` directory.
2.  **Analysis**: The Python backend uses the `os` library to extract system-level timestamps.
3.  **Detection**: The algorithm compares `ctime` vs `mtime` to find backdated or tampered files.
4.  **Logging**: Data is permanently recorded into a secure `forensics_results.csv` report.
5.  **Visualization**: Results are displayed in a professional, enterprise-style "Excel" dashboard.

---

## ✨ Key Features
- **🚨 Suspicious Activity Flagging**: Automatically highlights files where the modification date is newer than the creation date.
- **📊 Professional Dashboard**: A clean, light-themed forensics console for easy data review.
- **📄 Secure CSV Reporting**: Generates a standard CSV log for use in legal or administrative reporting.
- **📏 Metadata Accuracy**: Captures precise file sizes and human-readable timestamps.
- **🚀 One-Click Cleanup**: Securely wipe all evidence logs to reset the system for a new investigation.

---

## 📁 Project Structure
```bash
├── app.py                  # Core backend logic & forensic algorithms
├── static/
│   └── css/
│       └── style.css       # Professional Enterprise-theme stylesheet
├── templates/
│   ├── index.html          # Upload interface
│   └── dashboard.html      # Forensic database & results view
├── PROJECT_EXPLANATION.md  # Detailed student presentation guide
├── forensics_results.csv   # Secure evidence log (excluded from Git)
└── README.md               # Project documentation
```

---

## 🚀 Setup & Installation
### Prerequisites
- Python 3.8 or higher installed on your system.

### Build Instructions
1. **Clone the repo**:
   ```bash
   git clone https://github.com/ardra-space/Cloud-forensics.git
   ```
2. **Install Flask**:
   ```bash
   pip install flask
   ```
3. **Run the App**:
   ```bash
   python app.py
   ```
4. **Access**: Open your browser at `http://127.0.0.1:5000`.

---

## 🎓 Educational Value
This project demonstrates key concepts in:
- **Digital Forensics**: Metadata extraction and timestamp analysis.
- **Web Security**: Secure file handling and breach identification.
- **Python Backend**: Interfacing with the Operating System for data retrieval.
- **UI/UX for Security**: Building clear, actionable dashboards for analysts.

---
*Developed by ardra-space. Built for educational excellence in Cybersecurity and Cloud Forensics.*
