# 🎓 Students' Study Guide: Cloud Forensics Automation Project

This document provides a line-by-line and section-by-section breakdown of the project code. It is designed to help you understand **how** it works and **why** each part was added.

---

## 1. Backend: `app.py` (The Engine) ⚙️
The `app.py` file is the brain of the project. It uses the **Flask** framework to handle web requests and the **OS** library to perform forensic analysis.

### Key Logic Blocks:

#### A. Data Extraction (`extract_metadata`)
```python
def extract_metadata(filepath):
    ctime_raw = os.path.getctime(filepath)  # Creation Time
    mtime_raw = os.path.getmtime(filepath)  # Last Modified Time
    # ...
    suspicious = mtime_raw > ctime_raw  # The Forensic Check
```
*   **How it works**: We use `os.path.getctime` and `os.path.getmtime` to fetch the exact timestamps from the computer's file system. 
*   **The Study Logic**: If a file was modified *after* it was created, it indicates the content has changed. In high-security e-commerce environments, this is a "red flag" for tampering.

#### B. Data Storage (`save_to_csv`)
```python
with open(CSV_FILE, "w", newline="", encoding="utf-8") as csvfile:
```
*   **The 'w' mode**: We use `"w"` (Write mode). This is a design choice. It means every time you upload new files, the old ones are wiped. 
*   **Why?**: This ensures the dashboard stays clean and only shows the results of your **current** investigation session.

#### C. The Routing (`@app.route`)
*   **`@app.route("/")`**: This "maps" the base URL to your `index.html` (Upload Page).
*   **`@app.route("/upload")`**: This is a POST route. It collects the files you selected, saves them to the `uploads/` folder, and triggers the `extract_metadata` function for each one.

---

## 2. Frontend: `index.html` (The Ingestion Page) 📁
This page is where the user interacts with the system.

### Key Features:
*   **`enctype="multipart/form-data"`**: This is mandatory in HTML whenever you are uploading files. Without it, the browser won't send the files to Python.
*   **JavaScript (Simple Upload Logic)**:
    ```javascript
    fileInput.addEventListener('change', function() { ... })
    ```
    *   **How it works**: This "listener" waits for you to choose files. As soon as you do, it counts them and updates the text on the button to say "Upload 3 Files."
    *   **The Hover Warning**: We added a feature where the button turns Amber and says "Select a file first!" if you hover without choosing anything. This is **UX (User Experience) Design** to prevent user errors.

---

## 3. Frontend: `dashboard.html` (The Analysis Page) 📊
This is where the forensics data is visualized.

### Key Features:
*   **Jinja2 Template Engine**: You will see tags like `{% for record in records %}`.
    *   **How it works**: Flask takes the CSV data and "shovels" it into this HTML file. The `{% for ... %}` tag is a **Loop**. It creates a table row (`<tr>`) for every single file in the CSV automatically.
*   **Dynamic Highlighting**:
    ```html
    <tr class="{{ 'row-suspicious' if record.suspicious else '' }}">
    ```
    *   **The Study Logic**: This is a "Conditional Class." It tells the browser: "If the Python code flagged this file as suspicious, apply the Red Background style."

---

## 4. Designing the Look: `style.css` 🎨
The CSS provides the "Enterprise" feel.

*   **CSS Variables (`:root`)**: We used variables like `--accent` and `--bg-page`. This makes it incredibly easy to change the entire theme of the website just by changing one line at the top.
*   **Zebra-Striping**: 
    ```css
    .forensics-table tbody tr:nth-child(even) { background: var(--row-alt); }
    ```
    *   This makes large amounts of forensic data easier to read by alternating colors for each row.

---

## 5. Why did we build it this way? (Summary)
1.  **Ease of Explanation**: We used standard browser functions (like `confirm()` for the clear button) instead of complex custom code so that a student can easily explain it in a viva.
2.  **Professional Appearance**: By focusing on a clean "Excel-style" table and high-tech colors, the project looks like a real security tool used by companies.
3.  **Real-World Logic**: The comparison of `ctime` and `mtime` is a genuine forensic technique used for finding unauthorized file changes.

---
*Generated for technical study purposes.*
