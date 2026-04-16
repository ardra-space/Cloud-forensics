# 📚 Cloud Forensics Automation: Final Project Documentation

This document consolidates all the high-level design, technical context, and project intellectual property into one place. It is designed for human presentation and AI-assisted development.

---

## 🏛️ Part 1: High-Level Design (HLD)

### 1.1 System Overview
The **Cloud Forensics Automation System** is a lightweight tool for e-commerce security audits. It extracts OS-level metadata to identify anomalies in file structures post-breach.

### 1.2 Component Architecture
- **Ingestion**: Flask-driven multi-file upload.
- **Analysis**: Python `os.path` time-delta algorithm.
- **Storage**: CSV evidence logging.
- **View**: Responsive Jinja2 dashboard.

### 1.3 Forensic Logic
Logic: `Anomaly = (Modification Time > Creation Time)`. This is the core indicator of a "tampered" script in high-integrity environments.

---

## 📄 Part 2: Master Project Report
(See [MASTER_PROJECT_REPORT.md](MASTER_PROJECT_REPORT.md) for the full detailed audit of features and technical stack.)

### 2.1 Key Objectives
- Automate evidence collection.
- Minimize human error in metadata extraction.
- Provide clear visual prioritization (Red/Green flagging).

---

## 🤖 Part 3: AI Technical Prompt (For ChatGPT/Claude)

*Copy the text below to give any AI a full understanding of your project.*

```text
[CONTEXT LOAD: CLOUD FORENSICS AUTOMATION SYSTEM]

I am building a Cloud Forensics Automation Tool. I need you to assist me based on the following architecture:

- Backend: Python 3.12 (Flask Framework)
- Frontend: Vanilla HTML5, CSS3, ES6 JavaScript
- Storage: Flat-file CSV (forensics_results.csv)
- Logic: Time-delta analysis (mtime > ctime)

KEY FILES & LOGIC:
1. app.py: Handles metadata extraction via `os.path.getmtime` and `os.path.getctime`.
2. style.css: Uses CSS Variables for enterprise theming.
3. Templates: Jinja2 Loops for dynamic evidence log rendering.

I need you to help me with High-Level Design (HLD) improvements, code analysis, and future module development. 
```

---
*End of Documentation*
