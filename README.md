# 🎓 Student Attendance Management System

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-150458?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-1.24%2B-013243?style=for-the-badge&logo=numpy&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.7%2B-11557C?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

A beginner-friendly, locally-hosted **Student Attendance Management System** developed using **Python and core Data Science concepts**. 

This system helps educators, faculty, and institutions record daily student attendance, calculate attendance percentages automatically, identify attendance shortages below the mandatory 75% threshold, compute consecutive recovery targets, edit student and attendance records, and visualize actionable academic insights through interactive charts.

---

## 📌 Table of Contents

- [🌟 1. Project Overview](#-1-project-overview)
- [🛠️ 2. Tools & Technologies Deep-Dive](#️-2-tools--technologies-deep-dive)
  - [🔢 NumPy](#-numpy-numerical-computing--statistics)
  - [🐼 Pandas](#-pandas-data-manipulation--pipelines)
  - [📊 Matplotlib](#-matplotlib-data-visualization)
  - [⚡ Streamlit](#-streamlit-interactive-user-interface)
  - [🐍 Python](#-python-core-engine)
  - [📄 CSV Files](#-csv-files-persistent-storage)
- [🎯 3. Application Features](#-3-application-features)
- [🔬 4. Data Science Principles in Action](#-4-data-science-principles-in-action)
- [📂 5. Project Directory Structure](#-5-project-directory-structure)
- [💻 6. Local Installation & Setup Guide (VS Code)](#-6-local-installation--setup-guide-vs-code)
- [🧪 7. Automated Unit Testing](#-7-automated-unit-testing)
- [📊 8. Sample Dataset Overview](#-8-sample-dataset-overview)
- [📄 9. License](#-9-license)

---

## 🌟 1. Project Overview

Manual attendance management using paper registers or simple spreadsheets is time-consuming, prone to human calculation errors, and fails to give educators immediate analytical insights.

This application provides an **automated, offline-capable local desktop solution** built specifically around data science fundamentals:
1. **Automated Analytics**: Instant computation of attendance percentages, class averages, standard deviation, and median attendance.
2. **Shortage Warning (< 75%)**: Automatically tags students who fall below the university-standard 75% attendance criterion and calculates exactly how many future classes they must attend to recover.
3. **Flexible Data Management**: Full ability to add students, modify student names, change roll numbers (IDs), update past attendance, or edit records in an interactive spreadsheet grid.
4. **Visual Exploratory Analysis**: Generates publication-ready Matplotlib bar charts, department comparisons, eligibility donuts, and turnout trend lines.
5. **Completely Local & Zero-Cost**: Runs 100% on your local machine using standard CSV storage—no paid APIs, no external database servers, and no cloud dependencies required.

---

## 🛠️ 2. Tools & Technologies Deep-Dive

This project demonstrates how standard Python data science libraries work together to build an end-to-end management pipeline:

```
+---------------------------------------------------------------------------------+
|                                APPLICATION STACK                                |
+---------------------------------------------------------------------------------+
|  [ Presentation Layer ]  -->  Streamlit (GUI Dashboard, Forms & Data Editors)   |
|  [ Visualization ]       -->  Matplotlib (Bar Charts, Donut Plots, Trend Lines) |
|  [ Numerical Engine ]    -->  NumPy (Vectorized Calculations & Statistics)     |
|  [ Data Pipeline ]       -->  Pandas (Cleaning, Grouping, Aggregation & Pivoting)|
|  [ Storage Layer ]       -->  CSV Files (attendance_data.csv & students.csv)   |
+---------------------------------------------------------------------------------+
```

---

### 🔢 NumPy (Numerical Computing & Statistics)

**NumPy** serves as the mathematical and numerical foundation for all statistical analysis and conditional logic in the application.

* **Vectorized Percentage Calculations**:
  Computes attendance percentages across arrays without Python `for` loops, safely handling zero division:
  ```python
  summary_df["AttendancePercentage"] = np.where(
      summary_df["TotalClasses"] > 0,
      np.round((summary_df["PresentClasses"] / summary_df["TotalClasses"]) * 100.0, 2),
      0.0
  )
  ```
* **Descriptive Statistical Metrics**:
  * **Mean ($\mu$)**: `np.mean(pct_values)` calculates overall class turnout.
  * **Median ($M$)**: `np.median(pct_values)` measures central attendance tendency, unaffected by extreme defaulter outliers.
  * **Standard Deviation ($\sigma$)**: `np.std(pct_values)` quantifies the spread/variance in attendance across the student cohort.
  * **Min & Max**: `np.min()` and `np.max()` detect the lowest and highest attendance records.
* **Rule-Based Multi-Class Classification**:
  Applies `np.select()` to assign academic performance tiers:
  ```python
  conditions = [
      summary_df["AttendancePercentage"] >= 90.0,
      (summary_df["AttendancePercentage"] >= 75.0) & (summary_df["AttendancePercentage"] < 90.0),
      (summary_df["AttendancePercentage"] >= 60.0) & (summary_df["AttendancePercentage"] < 75.0),
      summary_df["AttendancePercentage"] < 60.0,
  ]
  choices = ["Excellent (≥90%)", "Good (75-89%)", "Warning (60-74%)", "Critical (<60%)"]
  summary_df["PerformanceGrade"] = np.select(conditions, choices, default="Unclassified")
  ```
* **Consecutive Classes Shortage Recovery Formula**:
  Uses NumPy's `np.ceil()` and `np.maximum()` to compute the exact number of consecutive upcoming sessions $x$ a student must attend to reach $\ge 75\%$:
  $$\frac{P + x}{T + x} \ge 0.75 \implies x \ge 3T - 4P \implies x = \max(0, \lceil 3T - 4P \rceil)$$
  ```python
  classes_needed = np.maximum(0, np.ceil(3 * total_classes - 4 * present_classes).astype(int))
  ```

---

### 🐼 Pandas (Data Manipulation & Pipelines)

**Pandas** powers all data collection, cleaning, restructuring, aggregation, and tabular transformations.

* **Data Ingestion & Type Casting**:
  Reads CSV files and normalizes text fields (stripping whitespace, standardizing uppercase roll numbers):
  ```python
  df["Date"] = df["Date"].astype(str).str.strip()
  df["StudentID"] = df["StudentID"].astype(str).str.strip().str.upper()
  df["Name"] = df["Name"].astype(str).str.strip().str.title()
  ```
* **Data Cleaning & Handling Missing Values**:
  * Removes corrupt entries missing dates or student IDs: `df.dropna(subset=["StudentID", "Date"])`
  * Fills unrecorded or missing attendance totals with zeros: `df["PresentClasses"].fillna(0)`
* **Entity Deduplication**:
  Enforces uniqueness on `(Date, StudentID)` so updating a date overwrites obsolete entries cleanly without creating duplicate records:
  ```python
  df = df.drop_duplicates(subset=["Date", "StudentID"], keep="last")
  ```
* **Grouping & Aggregation**:
  Aggregates raw daily entries to calculate total sessions held and attended:
  ```python
  total_marked = attendance_df.groupby("StudentID")["Date"].nunique().rename("TotalClasses")
  present_marked = attendance_df[attendance_df["Status"] == "Present"].groupby("StudentID")["Date"].nunique().rename("PresentClasses")
  summary_df = roster_df.merge(total_marked, on="StudentID", how="left").merge(present_marked, on="StudentID", how="left")
  ```
* **Date-Wise Pivot Table (Cross-Tabulation)**:
  Transforms flat log rows into an intuitive spreadsheet-style matrix where students are rows and class dates are columns:
  ```python
  pivot = attendance_df.pivot_table(
      index=["StudentID", "Name", "Department"],
      columns="Date",
      values="Status",
      aggfunc="first",
      fill_value="Not Recorded"
  )
  ```
* **Relational Synchronization**:
  When a student's roll number or name is edited, Pandas cascades the changes to all historical attendance logs in `attendance_data.csv`.

---

### 📊 Matplotlib (Data Visualization)

**Matplotlib** provides customized, publication-quality graphical charts to reveal patterns and trends in attendance data.

* **Student Attendance Percentage Bar Chart**:
  * Draws vertical bars for each student with conditional color mapping: **Green (`#2ECC71`)** for $\ge 75\%$ and **Red (`#E74C3C`)** for shortages.
  * Adds a benchmark threshold line using `ax.axhline(75.0, color="#C0392B", linestyle="--", linewidth=2)`.
  * Renders exact percentage values on top of every bar using `ax.annotate()`.
* **Department-Wise Turnout Comparison**:
  * Bar plot comparing average attendance rates across Computer Science, Data Science, IT, and Electronics departments.
* **Attendance Eligibility Donut Chart**:
  * Donut chart (`ax.pie(..., wedgeprops=dict(width=0.45))`) displaying the proportion of compliant students vs. defaulters.
* **Daily Turnout Trend Line**:
  * Time-series plot charting overall turnout percentage fluctuations date-by-date (`ax.plot(dates, turnout, marker="o")`).

---

### ⚡ Streamlit (Interactive User Interface)

**Streamlit** provides the reactive, browser-based user interface, converting Python scripts into a web app.

* **Theme-Agnostic Containers (`st.container(border=True)`)**:
  Renders KPI cards that automatically adjust to both **Dark Mode** and **Light Mode**.
* **Direct Spreadsheet Editing (`st.data_editor`)**:
  Allows users to edit the student roster or daily attendance records directly in an interactive grid with dropdown status selectors.
* **Date Picker (`st.date_input`)**:
  Integrated date selector with custom CSS removing unnecessary text cursors/carets and standardizing formatting (`YYYY-MM-DD`).
* **Sidebar Navigation (`st.sidebar.radio`)**:
  Intuitive section switching between Dashboard, Attendance Marking, Editing, Defaulters, and CSV tools.
* **State Management & Instant Feedback**:
  Uses `st.rerun()`, `st.success()`, `st.error()`, and `st.metric()` for real-time interface updates.

---

### 🐍 Python (Core Engine)

* Standard library modules (`os`, `io`, `math`, `datetime`, `unittest`).
* Object-oriented and functional modular programming.
* Form validation, error handling, and robust exception management.

---

### 📄 CSV Files (Persistent Storage)

* **`attendance_data.csv`**: Contains all daily attendance logs (`Date`, `StudentID`, `Name`, `Department`, `Status`).
* **`students.csv`**: Master roster storing registered students (`StudentID`, `Name`, `Department`).
* Provides zero-configuration local persistence that retains data after restarting the application.

---

## 🎯 3. Application Features

| Section | Description |
| :--- | :--- |
| **📊 Dashboard & Insights** | Summary KPI cards (Total Students, Sessions, Class Average %, Defaulters count), highest/lowest attendees, statistical summary (Median, Std Dev), and 4 Matplotlib charts. |
| **📝 Mark Daily Attendance** | Date picker to mark attendance for any date. Features **"Mark All Present"** and **"Mark All Absent"** buttons and automatic deduplication. |
| **✏️ Edit & Update Records** | Modify student names, update roll numbers (IDs) with automatic history sync, change single/bulk attendance entries, or edit records via an Excel-like grid. |
| **⚠️ Attendance Shortage (<75%)** | Dedicated defaulters table displaying the exact number of consecutive future classes each student must attend to reach 75%, with CSV export. |
| **📋 Attendance Register** | Date-wise cross-tabulated Pivot Matrix view and filterable raw attendance records with student name/ID search. |
| **👤 Student Management** | Register new students, edit existing student profiles, and validate roll number uniqueness to prevent duplicates. |
| **📁 CSV Import & Export** | Download summary reports, raw attendance records, sample templates, or import external CSV files (Append/Overwrite). |
| **🔬 Data Science Concepts** | Built-in interactive explainer breaking down the math, Pandas code snippets, and NumPy statistics used in the system. |

---

## 🔬 4. Data Science Principles in Action

```
[1. Raw CSV Data] 
       │
       ▼
[2. Data Cleaning & Validation] ──► dropna(), str.strip(), drop_duplicates()
       │
       ▼
[3. Feature Engineering & Grouping] ──► groupby(['StudentID'])['Date'].nunique()
       │
       ▼
[4. Statistical Computations] ──► np.mean(), np.median(), np.std(), 75% Formula
       │
       ▼
[5. Rule-Based Classification] ──► np.select() into [Excellent, Good, Warning, Critical]
       │
       ▼
[6. Visual Analytics] ──► Matplotlib Bar Charts, Threshold Lines & Donut Plots
```

---

## 📂 5. Project Directory Structure

```text
Attendance-Management-/
│
├── .streamlit/
│   └── config.toml         # Streamlit local configuration (telemetry disabled)
│
├── app.py                  # Core application (Streamlit UI, Data Science pipeline)
├── attendance_data.csv     # Persistent CSV file storing attendance logs
├── students.csv            # Master roster of enrolled students
├── test_system.py          # Automated unit test suite (8 test cases)
├── requirements.txt        # Python library dependencies
├── .gitignore              # Files excluded from version control
├── LICENSE                 # MIT License
└── README.md               # Comprehensive project documentation
```

---

## 💻 6. Local Installation & Setup Guide (VS Code)

Follow these steps to run the application completely offline on your local machine:

### Prerequisites
* **Python 3.9 or higher** installed ([Download Python](https://www.python.org/downloads/)).
* **VS Code** installed ([Download VS Code](https://code.visualstudio.com/)).

---

### Step 1: Open the Project in VS Code
1. Open **Visual Studio Code**.
2. Go to **File** > **Open Folder...** and select the `Attendance-Management-` folder.

---

### Step 2: Open the Integrated Terminal
In VS Code, press <kbd>Ctrl</kbd> + <kbd>`</kbd> (backtick) or click **Terminal** > **New Terminal** in the top menu.

---

### Step 3: Create and Activate a Virtual Environment

It is recommended to run the project within a virtual environment:

* **Windows (PowerShell)**:
  ```powershell
  python -m venv .venv
  .\.venv\Scripts\Activate.ps1
  ```
  *(If execution policies block script activation, run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process` first)*

* **Windows (Command Prompt / cmd)**:
  ```cmd
  python -m venv .venv
  .\.venv\Scripts\activate.bat
  ```

* **macOS / Linux**:
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

---

### Step 4: Install Dependencies
Install all required libraries (`pandas`, `numpy`, `matplotlib`, `streamlit`) using `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

### Step 5: Launch the Application
Start the Streamlit local web server:

```bash
streamlit run app.py
```

The application will launch and automatically open in your default browser at:
👉 **`http://localhost:8501`**

---

### 🛑 How to Stop the App
In the VS Code terminal where Streamlit is running, press <kbd>Ctrl</kbd> + <kbd>C</kbd>.

---

## 🧪 7. Automated Unit Testing

The repository includes a comprehensive unit test suite in `test_system.py` to ensure all data science logic and plotting routines function correctly:

To run all automated unit tests:
```bash
python test_system.py
```

**Expected Test Output:**
```text
........
----------------------------------------------------------------------
Ran 8 tests in 1.199s

OK
```

### What the Test Suite Verifies:
1. `test_compute_student_summary`: Validates percentage calculations and rule-based classifications.
2. `test_compute_class_statistics`: Verifies Mean, Median, Standard Deviation, Min, and Max.
3. `test_matplotlib_plots_render_without_errors`: Verifies all 4 Matplotlib figure objects render without errors.
4. `test_edge_case_zero_classes`: Confirms zero-division safety when no classes have taken place.
5. `test_live_data_persistence`: Verifies data loading, column validation, and deduplication.
6. `test_update_student_record_cascades`: Confirms renaming student names or roll numbers updates all attendance logs.
7. `test_update_student_duplicate_id_rejected`: Ensures duplicate roll numbers are strictly rejected.
8. `test_update_single_attendance`: Tests single attendance status toggling.

---

## 📊 8. Sample Dataset Overview

The system includes pre-loaded, realistic sample data for **14 students across 4 departments** spanning **10 academic dates**:

* **Departments Represented**:
  * Computer Science
  * Data Science
  * Information Technology
  * Electronics & Communication
* **Diverse Attendance Profiles**:
  * High performers ($90\% - 100\%$)
  * Satisfactory attendees ($75\% - 85\%$)
  * Borderline warning cases ($70\%$)
  * Critical shortage defaulters ($25\% - 60\%$)

---

## 📄 9. License

This project is open-source and distributed under the **[MIT License](LICENSE)**.

Developed by **[tharun-bytes](https://github.com/tharun-bytes)**.
