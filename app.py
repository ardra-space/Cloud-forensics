"""
Cloud Forensics Automation System
==================================
A simple Flask web application that allows users to upload files,
extract forensic metadata, and display the results in a dashboard.

Author  : Student Project
Purpose : Demonstrate basic digital forensics concepts using Python + Flask
"""

import os
import csv
import time
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

# ─────────────────────────────────────────────
#  App Configuration
# ─────────────────────────────────────────────
app = Flask(__name__)

# Secret key needed for flash messages (session security)
app.secret_key = "cloud_forensics_secret_key_2024"

# Folder where uploaded files are temporarily stored for analysis
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Create folder if it doesn't exist

# CSV file that permanently stores the forensic results
CSV_FILE = "forensics_results.csv"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
# Max upload size = 50 MB per request
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024


# ─────────────────────────────────────────────
#  Helper Functions
# ─────────────────────────────────────────────

def format_size(bytes_size):
    """Convert raw byte size to a human-readable string (KB or MB)."""
    if bytes_size < 1024:
        return f"{bytes_size} B"
    elif bytes_size < 1024 * 1024:
        return f"{bytes_size / 1024:.2f} KB"
    else:
        return f"{bytes_size / (1024 * 1024):.2f} MB"





def extract_metadata(filepath):
    """
    Extract forensic metadata from a file.

    Returns a dictionary with:
      - filename        : Name of the file
      - creation_time   : When the file was first created (ctime)
      - modified_time   : When the file was last modified (mtime)
      - size_display    : Human-readable size (e.g., '12.5 KB')
      - size_kb         : Size in KB (numeric, used for chart)
      - suspicious      : True if modified_time > creation_time (potential tampering)
    """
    # os.path.getctime → creation time on Windows
    ctime_raw = os.path.getctime(filepath)
    # os.path.getmtime → last modified time
    mtime_raw = os.path.getmtime(filepath)
    # os.path.getsize → file size in bytes
    size_bytes = os.path.getsize(filepath)

    # Convert Unix timestamps to readable datetime strings
    creation_time  = datetime.fromtimestamp(ctime_raw).strftime("%Y-%m-%d %H:%M:%S")
    modified_time  = datetime.fromtimestamp(mtime_raw).strftime("%Y-%m-%d %H:%M:%S")

    # Suspicious: if the file was modified AFTER it was created
    # (Could indicate backdating or tampering in a real forensics scenario)
    suspicious = mtime_raw > ctime_raw

    return {
        "filename"      : os.path.basename(filepath),
        "creation_time" : creation_time,
        "modified_time" : modified_time,
        "size_display"  : format_size(size_bytes),
        "size_kb"       : round(size_bytes / 1024, 2),
        "suspicious"    : suspicious,
    }


def save_to_csv(records):
    """
    Save a list of forensic metadata records to the CSV file.
    Overwrites the file so only the latest upload session is displayed.
    """
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["filename", "creation_time", "modified_time",
                      "size_display", "size_kb", "suspicious"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Always write header since we are overwriting
        writer.writeheader()

        for record in records:
            writer.writerow(record)


def read_from_csv():
    """
    Read all forensic records from the CSV file.
    Returns a list of dictionaries (one per file row).
    Returns empty list if CSV doesn't exist yet.
    """
    if not os.path.isfile(CSV_FILE):
        return []

    records = []
    with open(CSV_FILE, "r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Convert the string "True"/"False" back to Python bool
            row["suspicious"] = row["suspicious"] == "True"
            records.append(row)
    return records


# ─────────────────────────────────────────────
#  Routes
# ─────────────────────────────────────────────

@app.route("/")
def index():
    """
    HOME PAGE — Shows the file upload interface.
    """
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    """
    UPLOAD HANDLER — Processes the uploaded files.

    Steps:
      1. Accept files from the form submission
      2. Save each file temporarily to the uploads/ folder
      3. Extract forensic metadata from each file
      4. Save all metadata to the CSV log
      5. Redirect the user to the dashboard
    """
    # Retrieve the list of uploaded files from the form
    files = request.files.getlist("files")

    # Guard: if no files were selected, go back with a warning
    if not files or all(f.filename == "" for f in files):
        flash("⚠️ No files were selected. Please choose at least one file.", "warning")
        return redirect(url_for("index"))

    records = []  # Will hold metadata for all uploaded files

    for file in files:
        if file.filename == "":
            continue  # Skip any empty file slots

        # Sanitize the filename to prevent directory traversal attacks
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

        # Save the file temporarily so we can inspect its metadata
        file.save(filepath)

        # Extract forensic metadata from the saved file
        metadata = extract_metadata(filepath)
        records.append(metadata)

    if records:
        # Persist the extracted metadata to our CSV log
        save_to_csv(records)
        flash(f"✅ Successfully analysed {len(records)} file(s). Results saved.", "success")
    else:
        flash("⚠️ No valid files were processed.", "warning")

    return redirect(url_for("dashboard"))


@app.route("/dashboard")
def dashboard():
    """
    DASHBOARD PAGE — Reads the CSV and displays forensic results.
    """
    records = read_from_csv()
    return render_template("dashboard.html", records=records)


@app.route("/clear", methods=["POST"])
def clear():
    """
    CLEAR ROUTE — Deletes the CSV log and all uploaded files.
    Useful for resetting the system during demos.
    """
    # Remove CSV log
    if os.path.isfile(CSV_FILE):
        os.remove(CSV_FILE)

    # Remove all files in the uploads folder
    for f in os.listdir(UPLOAD_FOLDER):
        os.remove(os.path.join(UPLOAD_FOLDER, f))

    flash("🗑️ All records have been cleared.", "info")
    return redirect(url_for("index"))


# ─────────────────────────────────────────────
#  Entry Point
# ─────────────────────────────────────────────
if __name__ == "__main__":
    # debug=True → auto-reloads server on code changes (useful during development)
    app.run(debug=True, port=5000)
