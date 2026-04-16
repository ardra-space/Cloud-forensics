# 🚀 Cloud Forensics Automation Platform: Master Project Report

> **Project Title**: Cloud Forensics Automation Tool for E-commerce Breach Detection
> **Framework**: Python Flask
> **Focus**: Metadata Extraction, Timestamp Analysis, and Evidence Logging

---

## 1. Executive Summary 📄
This project is an automated digital forensics tool designed to collect and analyze file metadata from cloud environments. It specifically addresses **E-commerce breach scenarios**, such as unauthorized changes to payment gateway scripts, product availability files, or transaction logs. 

By comparing **File Creation Time** vs. **Last Modified Time**, the system identifies files that have been edited post-creation—a common signature of a data breach or unauthorized code injection.

---

## 2. Functional Architecture ⚙️
The system follows a 4-layer architecture:
1.  **Ingestion Layer**: User uploads files through a clean, modern web interface.
2.  **Analysis Layer (Core Logic)**: Python's `os` and `datetime` libraries extract the `ctime` (creation) and `mtime` (modified) timestamps.
3.  **Database Layer**: Extracted data is structured and saved into a secure CSV (`forensics_results.csv`).
4.  **Presentation Layer**: A professional, React-style dashboard displays the evidence log with clear color-coded statuses (Clean vs. Suspicious).

---

## 3. Forensic Logic Deep-Dive 🔍
The "Suspicious" detection algorithm is based on the following principle:
*   **Normal File**: `Creation Time ≈ Modified Time` or `Creation Time > Modified Time` (in some OS environments).
*   **Tampered File**: `Modified Time > Creation Time`. 

When a hacker modifies a payment script after it was originally deployed (created), the operating system updates the "Modified Time." Our tool identifies this delta and flags the file in **Red** for immediate human investigation.

---

## 4. Full Source Code 💻
Below is the complete, simplified source code for the entire project. This can be used for local deployment or given to an AI (LLM) for deep technical analysis.

### A. Backend (`app.py`)
```python
import os
import csv
import time
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "cloud_forensics_secret_key"
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
CSV_FILE = "forensics_results.csv"

def format_size(bytes_size):
    if bytes_size < 1024: return f"{bytes_size} B"
    elif bytes_size < 1024 * 1024: return f"{bytes_size / 1024:.2f} KB"
    else: return f"{bytes_size / (1024 * 1024):.2f} MB"

def extract_metadata(filepath):
    ctime_raw = os.path.getctime(filepath)
    mtime_raw = os.path.getmtime(filepath)
    size_bytes = os.path.getsize(filepath)
    creation_time  = datetime.fromtimestamp(ctime_raw).strftime("%Y-%m-%d %H:%M:%S")
    modified_time  = datetime.fromtimestamp(mtime_raw).strftime("%Y-%m-%d %H:%M:%S")
    suspicious = mtime_raw > ctime_raw
    return {
        "filename": os.path.basename(filepath),
        "creation_time": creation_time,
        "modified_time": modified_time,
        "size_display": format_size(size_bytes),
        "size_kb": round(size_bytes / 1024, 2),
        "suspicious": suspicious,
    }

def save_to_csv(records):
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["filename", "creation_time", "modified_time", "size_display", "size_kb", "suspicious"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for record in records: writer.writerow(record)

def read_from_csv():
    if not os.path.isfile(CSV_FILE): return []
    records = []
    with open(CSV_FILE, "r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row["suspicious"] = row["suspicious"] == "True"
            records.append(row)
    return records

@app.route("/")
def index(): return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    files = request.files.getlist("files")
    if not files or all(f.filename == "" for f in files):
        flash("No files selected.", "warning")
        return redirect(url_for("index"))
    records = []
    for file in files:
        if file.filename == "": continue
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        records.append(extract_metadata(filepath))
    if records: save_to_csv(records)
    return redirect(url_for("dashboard"))

@app.route("/dashboard")
def dashboard():
    records = read_from_csv()
    return render_template("dashboard.html", records=records)

@app.route("/clear", methods=["POST"])
def clear():
    if os.path.isfile(CSV_FILE): os.remove(CSV_FILE)
    for f in os.listdir(UPLOAD_FOLDER): os.remove(os.path.join(UPLOAD_FOLDER, f))
    return redirect(url_for("index"))

if __name__ == "__main__": app.run(debug=True, port=5000)
```

### B. Stylesheet (`static/css/style.css`)
```css
:root {
  --bg-page: #f0f4f8; --bg-card: #ffffff; --bg-header: #0f172a;
  --accent: #0891b2; --accent-hover: #0369a1; --text-primary: #0f172a;
  --text-secondary: #475569; --border: #cbd5e1; --row-alt: #f8fafc;
  --red-tint: #fff1f2; --red-text: #be123c; --green-text: #15803d;
  --font-main: 'Inter', sans-serif; --font-mono: 'JetBrains Mono', monospace;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: var(--font-main); background: var(--bg-page); color: var(--text-primary); }
.topbar { background: var(--bg-header); color: #fff; padding: 0 2rem; height: 60px; display: flex; align-items: center; justify-content: space-between; }
.page-wrapper { max-width: 900px; margin: 0 auto; padding: 2.5rem 1.5rem; }
.page-wrapper.wide { max-width: 1200px; }
.card { background: var(--bg-card); border: 1px solid var(--border); border-radius: 10px; padding: 1.5rem; }
.forensics-table { width: 100%; border-collapse: collapse; }
.forensics-table thead { background: #1e293b; color: #fff; }
.forensics-table th, .forensics-table td { padding: 0.8rem; border-bottom: 1px solid var(--border); }
.row-suspicious { background: var(--red-tint) !important; }
.badge { padding: 0.2rem 0.6rem; border-radius: 999px; font-weight: 700; }
.badge.suspicious { background: #fecdd3; color: var(--red-text); }
.btn { padding: 0.6rem 1.2rem; border-radius: 6px; font-weight: 600; cursor: pointer; border: none; }
.btn-primary { background: var(--accent); color: #fff; }
```

---

## 5. Metadata Logic Table 📋
| Feature | Implementation | Logic Outcome |
| :--- | :--- | :--- |
| **Filename** | `os.path.basename` | Human-readable ID |
| **Creation Date** | `os.path.getctime` | Baseline timestamp |
| **Modified Date** | `os.path.getmtime` | Activity signature |
| **Evidence Storage** | `csv.DictWriter` | Permanent trace |
| **UI Highlighting** | `Jinja2 Condition` | Immediate visual alert |

---

## 6. AI/LLM Master Context 🤖
> **Instruction for AI Agents**:
> This project is a Cloud Forensics simulation. It is a Flask-based Single Page Application (SPA) architecture. Use the source code above to debug, extend, or explain the project. Specifically focus on the `extract_metadata` function in `app.py` as it represents the core forensic algorithm. The UI uses CSS Custom Properties (Variables) for theming.

---
*End of Report*
