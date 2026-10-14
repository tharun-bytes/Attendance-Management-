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
- [📖 6. In-Depth Project Explanation & How It Works](#-6-in-depth-project-explanation--how-it-works)
  - [🏛️ System Architecture & Workflow](#️-system-architecture--workflow)
  - [👤 Student Roster & Cascading Integrity](#-student-roster--cascading-integrity)
  - [📝 Attendance Entry & Deduplication](#-attendance-entry--deduplication)
  - [📐 Mathematical Shortage Recovery Model (75% Threshold)](#-mathematical-shortage-recovery-model-75-threshold)
  - [📋 Cross-Tabulated Attendance Matrix](#-cross-tabulated-attendance-matrix-pivot-table)
  - [📈 Visual Analytics & Insights Engine](#-visual-analytics--insights-engine)
  - [💾 Data Persistence Architecture](#-data-persistence-architecture-zero-database-philosophy)
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

## 📖 6. In-Depth Project Explanation & How It Works

This project is an end-to-end, data-driven academic analytics system engineered to replace inefficient manual attendance registers with an automated, reliable, and mathematically sound workflow.

### 🏛️ System Architecture & Workflow

The architecture follows a modular data processing pipeline where raw records move from user interaction through data validation, statistical computation, and finally to graphical rendering:

```
+-----------------------------------------------------------------------------------+
|                            SYSTEM WORKFLOW & ARCHITECTURE                         |
+-----------------------------------------------------------------------------------+
| [ 1. User Interaction ]      -->  Streamlit Web UI (Forms, Date Pickers, Grid)    |
|                                         │                                         |
| [ 2. Data Validation ]       -->  Input sanitization, whitespace trim, ID uppercase|
|                                   Deduplication on (Date + StudentID) composite key|
|                                         │                                         |
| [ 3. Storage & Relational ]  -->  students.csv (Master Roster)                    |
|                                   attendance_data.csv (Historical Attendance Logs)|
|                                   Cascading updates on roll number / name changes |
|                                         │                                         |
| [ 4. Computing Engine ]      -->  Pandas: Grouping, Aggregation & Pivot Matrices   |
|                                   NumPy: Vectorized percentages, Mean, Median, Std|
|                                         │                                         |
| [ 5. Rules & Recommendations]-->  Rule-based classification into 4 performance tiers|
|                                   Shortage detection (< 75% threshold)            |
|                                   Consecutive recovery target calculation (3T - 4P)|
|                                         │                                         |
| [ 6. Visual Presentation ]   -->  Matplotlib: Threshold Bar, Donut & Turnout Trend|
|                                   Streamlit KPI metric cards & interactive filters|
|                                   One-click CSV / Excel export                    |
+-----------------------------------------------------------------------------------+
```

---

### 👤 Student Roster & Cascading Integrity

1. **Entity Management (`students.csv`)**:
   - Each student is registered with a unique `StudentID` (roll number), `Name`, and `Department`.
   - **ID Uniqueness Enforcement**: The system strictly validates inputs upon submission. If a user attempts to register an ID that already exists (case-insensitive check), the submission is rejected with a clear warning, preventing corrupted or split records.
   - **Data Normalization**: Student IDs are automatically capitalized (e.g., `cs101` becomes `CS101`) and names are title-cased with trimmed whitespace.

2. **Cascading Relational Updates**:
   - In real-world educational institutions, student roll numbers or misspelled names often need correction after attendance has already been logged for several weeks.
   - When a student's ID or Name is updated via the **Edit Records** interface, the system executes a **cascading update**:
     - It modifies the master profile in `students.csv`.
     - It scans all historical rows matching that student in `attendance_data.csv` and synchronizes the ID and Name across every previous date.
     - This ensures zero orphaned records, zero loss of historical attendance data, and complete relational integrity without needing an external relational database.

---

### 📝 Attendance Entry & Deduplication

1. **Daily Marking Workflow**:
   - The faculty member selects any date using the date picker.
   - The current enrolled student list is fetched from `students.csv`. If attendance was already partially or fully recorded for that date, the app pre-fills the existing statuses; otherwise, all students default to **Present**.
   - **Batch Productivity Actions**: Faculty can click **"Mark All Present"** or **"Mark All Absent"** to toggle the entire class status in one click before adjusting individual exceptions.

2. **Idempotent Storage & Conflict Resolution**:
   - Traditional file systems often append duplicates if a user submits attendance for the same day twice.
   - This application uses Pandas subset deduplication:
     ```python
     combined_df = combined_df.drop_duplicates(subset=["Date", "StudentID"], keep="last")
     ```
   - Re-submitting attendance for an existing date seamlessly updates the existing records instead of creating duplicate or conflicting rows.

---

### 📐 Mathematical Shortage Recovery Model (75% Threshold)

A core data science feature of this system is the **Automated Attendance Recovery Recommendation Engine**.

#### 1. Why 75% Attendance Matters
Most higher education regulatory bodies (such as UGC, AICTE, and universities globally) establish a strict **75% minimum attendance rule** for students to be eligible to sit for final semester examinations. Falling below this threshold often results in academic penalties, detentions, or mandatory remedial work.

#### 2. The Attendance Percentage Formula
For any given student with $P$ present classes out of $T$ total sessions conducted:
$$\text{Attendance Percentage} = \left(\frac{P}{T}\right) \times 100$$
Using NumPy, this calculation is vectorized across the entire roster and protected against zero-division:
```python
summary_df["AttendancePercentage"] = np.where(
    summary_df["TotalClasses"] > 0,
    np.round((summary_df["PresentClasses"] / summary_df["TotalClasses"]) * 100.0, 2),
    0.0
)
```

#### 3. Mathematical Derivation of the Consecutive Classes Recovery Formula
When a student falls below 75%, telling them *"your attendance is 60%"* is not actionable. What the student and academic counselor need to know is: **"How many consecutive upcoming classes must I attend without missing a single session to bring my attendance up to 75%?"**

Let $x$ be the number of consecutive future classes attended:
- Total classes attended becomes: $P + x$
- Total classes conducted becomes: $T + x$

The required condition is:
$$\frac{P + x}{T + x} \ge 0.75 = \frac{3}{4}$$

Cross-multiplying (since $T + x > 0$):
$$4(P + x) \ge 3(T + x)$$
$$4P + 4x \ge 3T + 3x$$
$$4x - 3x \ge 3T - 4P$$
$$x \ge 3T - 4P$$

Because classes are discrete integers and attendance cannot be negative, the exact number of required consecutive sessions is:
$$x = \max\left(0, \; \lceil 3T - 4P \rceil\right)$$

#### 4. Real-World Calculation Examples

* **Case 1: Severe Shortage ($50\%$)**
  - Classes held: $T = 10$, Classes attended: $P = 5$
  - Current rate: $5 / 10 = 50.0\%$
  - Target: $x = 3(10) - 4(5) = 30 - 20 = 10$ consecutive classes.
  - *Verification*: After 10 future classes attended, new present classes $P' = 5 + 10 = 15$, new total classes $T' = 10 + 10 = 20$. New percentage: $15 / 20 = 75.0\%$ ✅

* **Case 2: Borderline Shortage ($70\%$)**
  - Classes held: $T = 10$, Classes attended: $P = 7$
  - Current rate: $7 / 10 = 70.0\%$
  - Target: $x = 3(10) - 4(7) = 30 - 28 = 2$ consecutive classes.
  - *Verification*: After 2 future classes attended, $P' = 7 + 2 = 9$, $T' = 10 + 2 = 12$. New percentage: $9 / 12 = 75.0\%$ ✅

* **Case 3: Already Eligible ($80\%$)**
  - Classes held: $T = 10$, Classes attended: $P = 8$
  - Current rate: $8 / 10 = 80.0\%$
  - Formula: $3(10) - 4(8) = 30 - 32 = -2 \implies \max(0, -2) = 0$ classes needed ✅

---

### 📋 Cross-Tabulated Attendance Matrix (Pivot Table)

Daily logs stored as normalized rows `(Date, StudentID, Status)` are optimal for storage, but difficult for educators to read across multiple weeks.

The application leverages Pandas **Pivot Tables** to dynamically pivot flat records into a complete academic attendance register:
```python
pivot = attendance_df.pivot_table(
    index=["StudentID", "Name", "Department"],
    columns="Date",
    values="Status",
    aggfunc="first",
    fill_value="Not Recorded"
)
```
- **Rows**: Each unique student.
- **Columns**: Chronological calendar dates of all recorded classes.
- **Cells**: Status (`Present`, `Absent`, or `Not Recorded` if a student was enrolled after that date).
- Educators can view and export this entire register matrix directly into Excel/CSV.

---

### 📈 Visual Analytics & Insights Engine

Rather than relying purely on text tables, the system applies **Exploratory Data Analysis (EDA)** using Matplotlib to produce four analytical perspectives:

1. **Student Attendance Bar Chart with Threshold Boundary**:
   - Visualizes every student's percentage side-by-side.
   - Highlights compliance: **Green** for eligible students ($\ge 75\%$) and **Red** for students facing shortages ($< 75\%$).
   - A bold dashed horizontal reference line at $75\%$ provides an immediate visual benchmark.
2. **Department Turnout Comparison**:
   - Compares mean attendance across departments (Computer Science, Data Science, IT, Electronics) to identify faculty cohorts requiring institutional intervention.
3. **Classroom Eligibility Donut Chart**:
   - Renders a clean donut chart displaying the exact proportion of students eligible for exams versus defaulters.
4. **Turnout Trend Over Time**:
   - Plots daily class turnout percentages across chronological dates to detect dips on specific weekdays, preceding holidays, or examination preparation periods.

---

### 💾 Data Persistence Architecture (Zero-Database Philosophy)

The application intentionally utilizes transparent, comma-separated values (CSV) storage:
* **No Database Configuration Overhead**: Users do not need to install, configure, or run MySQL, PostgreSQL, or MongoDB servers.
* **Inspectability & Portability**: Faculty and administrators can inspect, backup, or open `attendance_data.csv` and `students.csv` directly in Microsoft Excel, Google Sheets, or any text editor.
* **Data Science Realism**: Most real-world data science workflows begin with tabular CSV datasets. The application demonstrates authentic data ingestion, cleaning, mutation, and persistence using native Python and Pandas file I/O.

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
