# 🎓 Student Attendance Management System Using Python & Data Science

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)
[![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Framework](https://img.shields.io/badge/Framework-Streamlit-red.svg)](https://streamlit.io/)

A complete, beginner-friendly, and interactive **Student Attendance Management System** developed using **Python, Pandas, NumPy, Matplotlib, and Streamlit**. 

This system helps educators and academic institutions track daily attendance, automatically compute attendance percentages, identify students with attendance shortages below the mandatory 75% threshold, calculate exact recovery targets, edit student and attendance records, and visualize comprehensive academic insights through exploratory data analysis (EDA).

---

## 📌 Table of Contents

1. [Project Overview](#-1-project-overview)
2. [Technologies Used](#-2-technologies-used)
3. [Key Features](#-3-key-features)
4. [Data Science Principles Applied](#-4-data-science-principles-applied)
5. [Project Architecture & Structure](#-5-project-architecture--structure)
6. [Local Installation & Setup in VS Code](#-6-local-installation--setup-in-vs-code)
7. [Deployment Guide (Streamlit Community Cloud)](#-7-deployment-guide-streamlit-community-cloud)
8. [Automated Testing & Verification](#-8-automated-testing--verification)
9. [Sample Data Specification](#-9-sample-data-specification)
10. [License & Acknowledgements](#-10-license--acknowledgements)

---

## 🌟 1. Project Overview

Traditional attendance registers are prone to manual calculation errors, lack instant visibility into attendance shortages, and offer no actionable academic analytics. 

This project solves these challenges by combining:
* **Interactive UI**: A Streamlit dashboard that enables educators to take and edit attendance with minimal clicks.
* **Data Science Concepts**: Utilizing **Pandas** for robust data pipelines and deduplication, **NumPy** for descriptive statistics and vectorized calculations, and **Matplotlib** for publication-quality visual analytics.
* **Persistent Lightweight Storage**: Relies on transparent, portable CSV files (`attendance_data.csv` and `students.csv`) without needing expensive or complex database servers.

---

## 🛠️ 2. Technologies Used

| Technology | Role in System |
| :--- | :--- |
| **Python** | Core language for business logic, data models, and calculations |
| **Pandas** | Tabular data collection, cleaning, deduplication, grouping, aggregations, and pivot matrices |
| **NumPy** | Vectorized mathematical operations, descriptive statistics (mean, median, std dev), and rule-based classifications |
| **Matplotlib** | Data visualizations (bar charts with threshold lines, department graphs, donut charts, and turnout trends) |
| **Streamlit** | Interactive web application framework for front-end rendering and state management |
| **CSV** | File-based persistent storage preserving data across application restarts |

---

## 🎯 3. Key Features

### 📊 1. Dashboard & Insights
* **Summary KPI Cards**: Real-time metrics showing Total Enrolled Students, Total Sessions Held, Class Average Attendance %, and Defaulters Count ($< 75\%$).
* **Insight Highlights**: Top Student(s) with highest attendance, lowest attendance student(s), and statistical metrics (Median, Standard Deviation).
* **Multi-Aspect Matplotlib Visualizations**:
  * **Student Bar Chart**: Every student's attendance percentage, conditionally color-coded (Green for $\ge 75\%$, Red for $< 75\%$) with a red dashed line at the 75% threshold.
  * **Department Comparison**: Aggregated average turnout by academic department.
  * **Eligibility Donut Chart**: Proportion of compliant students vs. defaulters.
  * **Daily Turnout Trend**: Line plot charting attendance fluctuations day by day.

### 📝 2. Mark Daily Attendance
* Interactive date picker with automatic ISO formatting (`YYYY-MM-DD`).
* All enrolled students loaded dynamically with radio controls for `Present` or `Absent`.
* Bulk action buttons: **"Mark All Present"** and **"Mark All Absent"** for single-click operations.
* **Deduplication Engine**: Re-submitting an existing date updates records cleanly without creating duplicate rows.

### ✏️ 3. Edit & Update Records (Data Management)
* **Change Student Name & Roll Number**: Select any student from a dropdown to modify their Name, Roll Number (Student ID), or Department. All historical attendance logs automatically synchronize!
* **Modify Daily Attendance**:
  * *Quick Single Entry Edit*: Pick any date and student to flip their status between `Present` and `Absent`.
  * *Bulk Day Turnout Editor*: Adjust attendance for all students on a given date at once.
  * *Delete Attendance Date*: Easily purge accidental entries (e.g. marked on holidays).
* **Interactive Spreadsheet Editor**:
  * Double-click cells to edit the **Student Roster** or **Attendance Logs** directly in an Excel-like grid (`st.data_editor`) and save changes.

### ⚠️ 4. Attendance Shortage (<75%) & Action Plan
* Automatically isolates students who fail to meet the mandatory 75% requirement.
* **Actionable Shortage Recovery Formula**:
  $$\text{Consecutive Classes Needed} = \max(0, \lceil 3 \times \text{Total} - 4 \times \text{Present} \rceil)$$
  Tells each student exactly how many continuous upcoming classes they must attend without an absence to regain eligibility.
* Severity tags: *Warning* (60%–74.9%) and *Critical* (< 60%).
* One-click download for the **Defaulters Report (CSV)**.

### 📋 5. Attendance Register & Pivot Matrix
* **Date-Wise Pivot Matrix**: Cross-tabulation viewing students as rows and class dates as columns, providing a complete attendance register grid.
* **Filterable Raw Logs**: Search by student name/ID or filter by department and status.

### 👤 6. Student Registration & Roster Management
* Register new students with Roll Number, Full Name, and Department.
* **Input Validation**: Enforces non-empty values and strictly prevents duplicate Roll Numbers / Student IDs.

### 📁 7. CSV Import & Export
* Download the **Student Attendance Summary (CSV)** with calculated percentages and status tags.
* Download **Raw Attendance Logs (CSV)** and standard **CSV Templates**.
* Upload external CSV files with **Append** or **Overwrite** options.
* Reset button to reload the default sample dataset at any time.

### 🔬 8. Built-in Data Science Explainer
* Dedicated tab explaining how Pandas, NumPy, and Matplotlib were utilized with mathematical formulas and code snippets.

---

## 🔬 4. Data Science Principles Applied

```
+-------------------------------------------------------------+
|                     DATA SCIENCE PIPELINE                   |
+-------------------------------------------------------------+
| 1. DATA COLLECTION      --> CSV Ingestion & Local Storage   |
| 2. DATA PREPROCESSING   --> Pandas Cleaning & Deduplication |
| 3. AGGREGATIONS & EDA   --> Groupby, Pivots & Proportions   |
| 4. STATISTICAL METRICS  --> NumPy Mean, Median, Std Dev     |
| 5. CLASSIFICATION       --> Rule-Based 75% Eligibility Logic|
| 6. VISUAL ANALYTICS     --> Matplotlib Charts & Thresholds  |
+-------------------------------------------------------------+
```

### A. Data Collection & Persistence (CSV Storage)
Structured data is stored in tabular CSV format:
* `attendance_data.csv`: Columns `Date`, `StudentID`, `Name`, `Department`, `Status`.
* `students.csv`: Columns `StudentID`, `Name`, `Department`.

### B. Data Cleaning & Preprocessing (Pandas)
* **Missing Value Imputation**: Uses `fillna(0)` on numerical counts and `dropna()` on primary identifiers.
* **Text Normalization**: Trims whitespaces (`.str.strip()`), standardizes case (`.str.upper()`, `.str.title()`).
* **Entity Integrity**: Enforces uniqueness on `(Date, StudentID)` with `drop_duplicates(keep='last')`.

### C. Exploratory Data Analysis & Grouping (Pandas)
```python
# Aggregate attendance counts per student
total_marked = attendance_df.groupby("StudentID")["Date"].nunique().rename("TotalClasses")
present_marked = attendance_df[attendance_df["Status"] == "Present"].groupby("StudentID")["Date"].nunique().rename("PresentClasses")

# Cross-tabulate into matrix
pivot = attendance_df.pivot_table(index=["StudentID", "Name", "Department"], columns="Date", values="Status", aggfunc="first")
```

### D. Statistical Analysis (NumPy)
* **Vectorized Percentage Calculation** (guarded against zero-division):
  $$\text{Percentage} = \text{np.where}(\text{Total} > 0, \text{np.round}((\text{Present} / \text{Total}) \times 100, 2), 0.0)$$
* **Descriptive Metrics**:
  * **Mean ($\mu$)**: `np.mean()` measures overall class turnout.
  * **Median ($M$)**: `np.median()` measures central tendency resistant to extreme defaulter outliers.
  * **Standard Deviation ($\sigma$)**: `np.std()` measures variance and spread in attendance behavior across students.
  * **Min / Max**: Identifies highest and lowest attendees.

### E. Rule-Based Classification
Implemented using `np.select` for transparent, auditable academic grading without unnecessary ML complexity:
* $\ge 90\% \implies$ **Excellent**
* $75\% - 89.9\% \implies$ **Good / Eligible**
* $60\% - 74.9\% \implies$ **Warning / Needs Improvement**
* $< 60\% \implies$ **Critical Shortage**

### F. Data Visualization (Matplotlib)
* Custom bar plots featuring a horizontal 75% threshold line via `ax.axhline(75.0, color='red', linestyle='--')`.
* Dynamic conditional color mapping: Green (`#2ECC71`) for compliant students and Red (`#E74C3C`) for shortages.
* Bar annotations directly displaying values above bars with `ax.annotate()`.

---

## 📂 5. Project Architecture & Structure

```text
Attendance-Management-/
│
├── .streamlit/
│   └── config.toml         # Streamlit server and telemetry configuration
│
├── app.py                  # Main application: UI, data pipeline, and analytics
├── attendance_data.csv     # Primary dataset: Daily attendance logs
├── students.csv            # Enrolled student roster
├── test_system.py          # Automated unit test suite
├── requirements.txt        # Python library dependencies
├── .gitignore              # Files excluded from git tracking
└── README.md               # Complete project documentation
```

---

## 💻 6. Local Installation & Setup in VS Code

### Prerequisites
* **Python 3.9+** installed on your system.
* **Git** installed on your system.

### Step 1: Clone or Open the Repository
In your terminal, clone the repository:
```bash
git clone https://github.com/tharun-bytes/Attendance-Management-.git
cd Attendance-Management-
```
*(Or open the folder in **VS Code** via `File > Open Folder...`)*

### Step 2: Open the Built-in Terminal
Press <kbd>Ctrl</kbd> + <kbd>`</kbd> (backtick) or go to **Terminal** > **New Terminal**.

### Step 3: Set Up a Virtual Environment (Recommended)
* **Windows (PowerShell)**:
  ```powershell
  python -m venv .venv
  .\.venv\Scripts\Activate.ps1
  ```
  *(If execution policy errors occur, run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process` first)*
* **Windows (Command Prompt)**:
  ```cmd
  python -m venv .venv
  .\.venv\Scripts\activate.bat
  ```
* **macOS / Linux**:
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Launch the Application
```bash
streamlit run app.py
```
The application will launch in your browser at **`http://localhost:8501`**.

---

## ☁️ 7. Deployment Guide (Streamlit Community Cloud)

You can deploy this application for free to the web using **Streamlit Community Cloud** in 3 simple steps:

1. **Push your code to GitHub**:
   Ensure your code is pushed to your GitHub repository:
   `https://github.com/tharun-bytes/Attendance-Management-`
2. **Sign up / Log in to Streamlit Community Cloud**:
   Go to **[share.streamlit.io](https://share.streamlit.io/)** and sign in using your GitHub account.
3. **Deploy the App**:
   * Click **New app**.
   * Select your repository: `tharun-bytes/Attendance-Management-`.
   * Set Branch: `main`.
   * Set Main file path: `app.py`.
   * Click **Deploy!**

Within 1–2 minutes, your Student Attendance Management System will be live with a public URL accessible from any device!

---

## 🧪 8. Automated Testing & Verification

An automated test suite is provided in `test_system.py` covering computations, edge cases, and visualizations:

To run all tests:
```bash
python test_system.py
```

### Test Coverage Summary:
* ✅ `test_compute_student_summary`: Validates percentage calculations, rule-based classification, and shortage recovery formula.
* ✅ `test_compute_class_statistics`: Validates mean, median, standard deviation, min, and max.
* ✅ `test_matplotlib_plots_render_without_errors`: Verifies all 4 Matplotlib figures render without graphical errors.
* ✅ `test_edge_case_zero_classes`: Confirms zero-division safety when no classes have been conducted.
* ✅ `test_live_data_persistence`: Checks CSV loading, column validation, and deduplication.
* ✅ `test_update_student_record_cascades`: Confirms student name and ID updates automatically synchronize with attendance logs.
* ✅ `test_update_student_duplicate_id_rejected`: Ensures duplicate student IDs cannot be assigned.
* ✅ `test_update_single_attendance`: Tests single attendance status modifications.

---

## 📊 9. Sample Data Specification

The application comes pre-populated with a realistic dataset of **14 enrolled students** across **4 academic departments** over **10 dates**:
* **Departments**: Computer Science, Data Science, Information Technology, Electronics & Communication.
* **Profiles**:
  * High performers ($\ge 90\%$)
  * Satisfactory attendees ($75\% - 85\%$)
  * Borderline warning cases ($70\%$)
  * Critical shortage defaulters ($40\% - 60\%$)

---

## 📄 10. License & Acknowledgements

* **License**: Open-source under the [MIT License](LICENSE).
* **Developed With**: Python, Pandas, NumPy, Matplotlib, and Streamlit.
* **Author**: [tharun-bytes](https://github.com/tharun-bytes)
