# Cloud Forensics Automation System for E-commerce Breach Detection

## Overview
This project is a **Cloud Forensics Automation System** designed to simulate file evidence collection during an e-commerce data breach. It extracts critical forensic metadata (Creation time, Last Modified time) and records it into a secure CSV report.

The system automatically flags files as **"Suspicious"** if the Last Modified date is newer than the Creation date, helping forensic analysts identify potentially tampered or backdated files.

## Features
- **File Metadata Extraction**: Automatically logs file system timestamps.
- **Breach Detection**: Identifies suspicious file modification patterns.
- **Professional Dashboard**: Displays forensic results in a clean, Excel-style table.
- **E-commerce Context**: Specifically framed for scenarios like payment script tampering or product data manipulation.
- **Secure CSV Export**: All findings are saved to `forensics_results.csv` for reporting.

## Tech Stack
- **Backend**: Python (Flask)
- **Frontend**: HTML5, Vanilla CSS, JavaScript
- **Core Libraries**: `os`, `datetime`, `csv`, `flask`

## How to Run
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `python app.py`
4. Visit `http://127.0.0.1:5000` in your browser.

---
*Developed for student project demonstration on Cloud Forensics and E-commerce Breach Detection.*
