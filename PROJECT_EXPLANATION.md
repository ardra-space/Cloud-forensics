# 📘 Project Explanation: Cloud Forensics Automation System

This document provides a comprehensive breakdown of the project logic, architecture, and design choices. It is intended to help students explain the project during technical presentations or viva sessions.

---

## 1. Project Objective 🎯
The primary goal of this system is to **automate the collection of digital evidence** from a cloud environment (simulated via file uploads). In an E-commerce breach scenario (e.g., someone tampering with payment scripts or transaction logs), speed and accuracy are critical. This tool extracts mandatory forensic metadata and identifies potential "tampering signatures."

---

## 2. The Core Forensic Logic 🔍
The "brains" of the project reside in the detection of **suspicious file modifications**.

### The "Suspicious" Formula
We compare two key timestamps:
1.  **Creation Time (`ctime`)**: When the file was first placed on the system.
2.  **Last Modified Time (`mtime`)**: When the file's content was last changed.

> **Logic**: `IF Last Modified Time > Creation Time → THEN Status = "⚠️ Suspicious"`

**Why is this suspicious?**
In a secure system, if a core script (like `payment_gateway.js`) was created at the time of deployment and never intended to be changed, any modification date that is *newer* than the creation date suggests that someone (potentially a hacker) has edited the file content.

---

## 3. Backend Breakdown (`app.py`) ⚙️
The backend is built with **Python Flask**, chosen for its simplicity and ability to interface directly with the Operating System.

### Key Functions
- **`extract_metadata(filepath)`**:
    - Uses Python's `os` library to talk to the file system.
    - `os.path.getmtime`: Gets the last modification date.
    - `os.path.getctime`: Gets the creation date.
    - It puts everything into a "Dictionary" (a list-like structure) for the dashboard to read.
- **`save_to_csv(records)`**:
    - Uses the `csv` module to write data to `forensics_results.csv`.
    - **Mode 'w' (Write)**: We use 'w' instead of 'a' (append) so that every new scan clears the old results. This ensures the dashboard always shows the **current evidence session**.

---

## 4. Frontend Design Choices (`HTML/CSS`) 🎨
The UI is designed to look like a **professional Enterprise Forensics Console**.

### UI Features
- **Excel-Style Table**: Professional investigators use spreadsheets. We mimicked this with a "zebra-striped" table to make it easy to read dozens of files.
- **Color Coding**: 
    - **Red**: For suspicious files (Immediate attention).
    - **Green**: For clean files (Safe).
    - **Cyan/Navy**: For a high-tech, trustworthy "Security" feel.
- **Simplified JavaScript**: We replaced complex "Drag and Drop" code with **standard browser-native functions**.
    - *Presentation Tip*: If asked about the code, mention: "I used native JavaScript event listeners to update the file count, making the code lightweight and easy to maintain."

---

## 5. Security & Persistence 💾
- **Data Logging**: All scanned evidence is permanently logged into a CSV file. Even if the web server restarts, the evidence remains.
- **Isolation**: Uploaded files are stored in a dedicated `uploads/` folder, keeping the local file system organized.

---
*Created by Antigravity (Advanced AI Coding Assistant) for the Cloud Forensics Automation Project.*
