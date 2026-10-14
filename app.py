"""
Student Attendance Management System
Built using Python, Pandas, NumPy, Matplotlib, and Streamlit.

This application demonstrates core Data Science concepts:
1. Data Collection & Persistence: Storing tabular attendance in CSV.
2. Data Cleaning & Preprocessing: Pandas validation, deduplication, missing value handling.
3. Statistical Analysis: NumPy & Pandas metrics (mean, median, std dev, percentages).
4. Exploratory Data Analysis (EDA): Grouping, aggregations, and pivot tables.
5. Data Visualization: Clean Matplotlib bar charts, histograms, and donut charts.
6. Rule-Based Classification: Categorizing students by attendance eligibility (>= 75%).
"""

import os
import io
import math
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# ==========================================
# 1. APPLICATION CONFIGURATION & CONSTANTS
# ==========================================
DATA_FILE = "attendance_data.csv"
STUDENTS_FILE = "students.csv"
ATTENDANCE_THRESHOLD = 75.0  # Mandatory threshold percentage

# Configure Streamlit page settings
st.set_page_config(
    page_title="Student Attendance Management System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced UI styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        opacity: 0.85;
        margin-bottom: 1.5rem;
    }
    .stButton>button {
        border-radius: 6px;
        font-weight: 600;
    }
    /* Eliminate unnecessary text cursor (I-beam) and blinking caret on date inputs */
    div[data-testid="stDateInput"] input {
        cursor: pointer !important;
        caret-color: transparent !important;
        user-select: none !important;
    }
    div[data-testid="stDateInput"],
    div[data-testid="stDateInput"] div {
        cursor: pointer !important;
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# 2. DATA ACCESS & PREPROCESSING (PANDAS)
# ==========================================
def initialize_sample_data():
    """Generates default sample attendance records if no file exists."""
    sample_records = [
        ("2026-03-02", "CS101", "Alice Johnson", "Computer Science", "Present"),
        ("2026-03-02", "CS102", "Bob Smith", "Computer Science", "Present"),
        ("2026-03-02", "CS103", "Catherine Lee", "Computer Science", "Absent"),
        ("2026-03-02", "DS101", "David Miller", "Data Science", "Present"),
        ("2026-03-02", "DS102", "Emma Watson", "Data Science", "Present"),
        ("2026-03-02", "DS103", "Frank Castle", "Data Science", "Absent"),
        ("2026-03-02", "IT101", "Grace Hopper", "Information Technology", "Present"),
        ("2026-03-02", "IT102", "Henry Cavill", "Information Technology", "Absent"),
        ("2026-03-02", "IT103", "Isabella Swan", "Information Technology", "Present"),
        ("2026-03-02", "EC101", "Jack Ryan", "Electronics & Communication", "Present"),
        ("2026-03-02", "EC102", "Karen Gillan", "Electronics & Communication", "Present"),
        ("2026-03-02", "EC103", "Luke Skywalker", "Electronics & Communication", "Absent"),

        ("2026-03-03", "CS101", "Alice Johnson", "Computer Science", "Present"),
        ("2026-03-03", "CS102", "Bob Smith", "Computer Science", "Absent"),
        ("2026-03-03", "CS103", "Catherine Lee", "Computer Science", "Present"),
        ("2026-03-03", "DS101", "David Miller", "Data Science", "Present"),
        ("2026-03-03", "DS102", "Emma Watson", "Data Science", "Present"),
        ("2026-03-03", "DS103", "Frank Castle", "Data Science", "Present"),
        ("2026-03-03", "IT101", "Grace Hopper", "Information Technology", "Present"),
        ("2026-03-03", "IT102", "Henry Cavill", "Information Technology", "Present"),
        ("2026-03-03", "IT103", "Isabella Swan", "Information Technology", "Present"),
        ("2026-03-03", "EC101", "Jack Ryan", "Electronics & Communication", "Present"),
        ("2026-03-03", "EC102", "Karen Gillan", "Electronics & Communication", "Present"),
        ("2026-03-03", "EC103", "Luke Skywalker", "Electronics & Communication", "Absent"),

        ("2026-03-04", "CS101", "Alice Johnson", "Computer Science", "Present"),
        ("2026-03-04", "CS102", "Bob Smith", "Computer Science", "Present"),
        ("2026-03-04", "CS103", "Catherine Lee", "Computer Science", "Present"),
        ("2026-03-04", "DS101", "David Miller", "Data Science", "Present"),
        ("2026-03-04", "DS102", "Emma Watson", "Data Science", "Present"),
        ("2026-03-04", "DS103", "Frank Castle", "Data Science", "Absent"),
        ("2026-03-04", "IT101", "Grace Hopper", "Information Technology", "Present"),
        ("2026-03-04", "IT102", "Henry Cavill", "Information Technology", "Present"),
        ("2026-03-04", "IT103", "Isabella Swan", "Information Technology", "Present"),
        ("2026-03-04", "EC101", "Jack Ryan", "Electronics & Communication", "Present"),
        ("2026-03-04", "EC102", "Karen Gillan", "Electronics & Communication", "Present"),
        ("2026-03-04", "EC103", "Luke Skywalker", "Electronics & Communication", "Present"),

        ("2026-03-05", "CS101", "Alice Johnson", "Computer Science", "Present"),
        ("2026-03-05", "CS102", "Bob Smith", "Computer Science", "Absent"),
        ("2026-03-05", "CS103", "Catherine Lee", "Computer Science", "Present"),
        ("2026-03-05", "DS101", "David Miller", "Data Science", "Present"),
        ("2026-03-05", "DS102", "Emma Watson", "Data Science", "Present"),
        ("2026-03-05", "DS103", "Frank Castle", "Data Science", "Present"),
        ("2026-03-05", "IT101", "Grace Hopper", "Information Technology", "Present"),
        ("2026-03-05", "IT102", "Henry Cavill", "Information Technology", "Absent"),
        ("2026-03-05", "IT103", "Isabella Swan", "Information Technology", "Present"),
        ("2026-03-05", "EC101", "Jack Ryan", "Electronics & Communication", "Present"),
        ("2026-03-05", "EC102", "Karen Gillan", "Electronics & Communication", "Present"),
        ("2026-03-05", "EC103", "Luke Skywalker", "Electronics & Communication", "Absent"),

        ("2026-03-06", "CS101", "Alice Johnson", "Computer Science", "Present"),
        ("2026-03-06", "CS102", "Bob Smith", "Computer Science", "Present"),
        ("2026-03-06", "CS103", "Catherine Lee", "Computer Science", "Present"),
        ("2026-03-06", "DS101", "David Miller", "Data Science", "Present"),
        ("2026-03-06", "DS102", "Emma Watson", "Data Science", "Absent"),
        ("2026-03-06", "DS103", "Frank Castle", "Data Science", "Absent"),
        ("2026-03-06", "IT101", "Grace Hopper", "Information Technology", "Present"),
        ("2026-03-06", "IT102", "Henry Cavill", "Information Technology", "Present"),
        ("2026-03-06", "IT103", "Isabella Swan", "Information Technology", "Absent"),
        ("2026-03-06", "EC101", "Jack Ryan", "Electronics & Communication", "Present"),
        ("2026-03-06", "EC102", "Karen Gillan", "Electronics & Communication", "Present"),
        ("2026-03-06", "EC103", "Luke Skywalker", "Electronics & Communication", "Absent"),

        ("2026-03-09", "CS101", "Alice Johnson", "Computer Science", "Present"),
        ("2026-03-09", "CS102", "Bob Smith", "Computer Science", "Present"),
        ("2026-03-09", "CS103", "Catherine Lee", "Computer Science", "Present"),
        ("2026-03-09", "DS101", "David Miller", "Data Science", "Present"),
        ("2026-03-09", "DS102", "Emma Watson", "Data Science", "Present"),
        ("2026-03-09", "DS103", "Frank Castle", "Data Science", "Present"),
        ("2026-03-09", "IT101", "Grace Hopper", "Information Technology", "Present"),
        ("2026-03-09", "IT102", "Henry Cavill", "Information Technology", "Present"),
        ("2026-03-09", "IT103", "Isabella Swan", "Information Technology", "Present"),
        ("2026-03-09", "EC101", "Jack Ryan", "Electronics & Communication", "Present"),
        ("2026-03-09", "EC102", "Karen Gillan", "Electronics & Communication", "Present"),
        ("2026-03-09", "EC103", "Luke Skywalker", "Electronics & Communication", "Present"),

        ("2026-03-10", "CS101", "Alice Johnson", "Computer Science", "Present"),
        ("2026-03-10", "CS102", "Bob Smith", "Computer Science", "Absent"),
        ("2026-03-10", "CS103", "Catherine Lee", "Computer Science", "Absent"),
        ("2026-03-10", "DS101", "David Miller", "Data Science", "Present"),
        ("2026-03-10", "DS102", "Emma Watson", "Data Science", "Present"),
        ("2026-03-10", "DS103", "Frank Castle", "Data Science", "Absent"),
        ("2026-03-10", "IT101", "Grace Hopper", "Information Technology", "Present"),
        ("2026-03-10", "IT102", "Henry Cavill", "Information Technology", "Present"),
        ("2026-03-10", "IT103", "Isabella Swan", "Information Technology", "Present"),
        ("2026-03-10", "EC101", "Jack Ryan", "Electronics & Communication", "Present"),
        ("2026-03-10", "EC102", "Karen Gillan", "Electronics & Communication", "Present"),
        ("2026-03-10", "EC103", "Luke Skywalker", "Electronics & Communication", "Absent"),

        ("2026-03-11", "CS101", "Alice Johnson", "Computer Science", "Present"),
        ("2026-03-11", "CS102", "Bob Smith", "Computer Science", "Present"),
        ("2026-03-11", "CS103", "Catherine Lee", "Computer Science", "Present"),
        ("2026-03-11", "DS101", "David Miller", "Data Science", "Present"),
        ("2026-03-11", "DS102", "Emma Watson", "Data Science", "Present"),
        ("2026-03-11", "DS103", "Frank Castle", "Data Science", "Present"),
        ("2026-03-11", "IT101", "Grace Hopper", "Information Technology", "Present"),
        ("2026-03-11", "IT102", "Henry Cavill", "Information Technology", "Present"),
        ("2026-03-11", "IT103", "Isabella Swan", "Information Technology", "Present"),
        ("2026-03-11", "EC101", "Jack Ryan", "Electronics & Communication", "Present"),
        ("2026-03-11", "EC102", "Karen Gillan", "Electronics & Communication", "Absent"),
        ("2026-03-11", "EC103", "Luke Skywalker", "Electronics & Communication", "Present"),

        ("2026-03-12", "CS101", "Alice Johnson", "Computer Science", "Absent"),
        ("2026-03-12", "CS102", "Bob Smith", "Computer Science", "Present"),
        ("2026-03-12", "CS103", "Catherine Lee", "Computer Science", "Present"),
        ("2026-03-12", "DS101", "David Miller", "Data Science", "Present"),
        ("2026-03-12", "DS102", "Emma Watson", "Data Science", "Present"),
        ("2026-03-12", "DS103", "Frank Castle", "Data Science", "Absent"),
        ("2026-03-12", "IT101", "Grace Hopper", "Information Technology", "Present"),
        ("2026-03-12", "IT102", "Henry Cavill", "Information Technology", "Absent"),
        ("2026-03-12", "IT103", "Isabella Swan", "Information Technology", "Present"),
        ("2026-03-12", "EC101", "Jack Ryan", "Electronics & Communication", "Absent"),
        ("2026-03-12", "EC102", "Karen Gillan", "Electronics & Communication", "Present"),
        ("2026-03-12", "EC103", "Luke Skywalker", "Electronics & Communication", "Absent"),

        ("2026-03-13", "CS101", "Alice Johnson", "Computer Science", "Present"),
        ("2026-03-13", "CS102", "Bob Smith", "Computer Science", "Absent"),
        ("2026-03-13", "CS103", "Catherine Lee", "Computer Science", "Absent"),
        ("2026-03-13", "DS101", "David Miller", "Data Science", "Present"),
        ("2026-03-13", "DS102", "Emma Watson", "Data Science", "Absent"),
        ("2026-03-13", "DS103", "Frank Castle", "Data Science", "Present"),
        ("2026-03-13", "IT101", "Grace Hopper", "Information Technology", "Present"),
        ("2026-03-13", "IT102", "Henry Cavill", "Information Technology", "Present"),
        ("2026-03-13", "IT103", "Isabella Swan", "Information Technology", "Present"),
        ("2026-03-13", "EC101", "Jack Ryan", "Electronics & Communication", "Present"),
        ("2026-03-13", "EC102", "Karen Gillan", "Electronics & Communication", "Present"),
        ("2026-03-13", "EC103", "Luke Skywalker", "Electronics & Communication", "Present"),
    ]
    df = pd.DataFrame(sample_records, columns=["Date", "StudentID", "Name", "Department", "Status"])
    df.to_csv(DATA_FILE, index=False)
    return df


def load_attendance_data():
    """
    Data Science Step: Data Loading & Preprocessing
    Loads attendance records from CSV, cleans whitespace, validates columns,
    and removes any duplicated entries on (Date, StudentID).
    """
    if not os.path.exists(DATA_FILE):
        return initialize_sample_data()

    try:
        df = pd.read_csv(DATA_FILE)
    except Exception as e:
        st.error(f"Error reading CSV file: {e}")
        return pd.DataFrame(columns=["Date", "StudentID", "Name", "Department", "Status"])

    expected_cols = ["Date", "StudentID", "Name", "Department", "Status"]
    for col in expected_cols:
        if col not in df.columns:
            df[col] = ""

    # Preprocessing: strip whitespace and standardize formats
    df["Date"] = df["Date"].astype(str).str.strip()
    df["StudentID"] = df["StudentID"].astype(str).str.strip().str.upper()
    df["Name"] = df["Name"].astype(str).str.strip()
    df["Department"] = df["Department"].astype(str).str.strip()
    df["Status"] = df["Status"].astype(str).str.strip().str.capitalize()

    # Data Cleaning: Handle missing values
    df = df.dropna(subset=["StudentID", "Date"])
    df = df[df["StudentID"] != ""]
    df = df[df["Date"] != ""]

    # Filter only valid status
    df["Status"] = df["Status"].apply(lambda s: "Present" if s in ["Present", "P", "1"] else "Absent")

    # Data Cleaning: Drop exact duplicate logs for the same date and student
    df = df.drop_duplicates(subset=["Date", "StudentID"], keep="last")
    return df


def save_attendance_data(df):
    """Saves cleaned DataFrame back to CSV storage."""
    df_sorted = df.sort_values(by=["Date", "StudentID"]).reset_index(drop=True)
    df_sorted.to_csv(DATA_FILE, index=False)


def load_students_roster(attendance_df):
    """
    Maintains a list of registered students.
    Reads from students.csv if available; otherwise derives unique students from attendance_data.csv.
    """
    if os.path.exists(STUDENTS_FILE):
        try:
            roster_df = pd.read_csv(STUDENTS_FILE)
            roster_df["StudentID"] = roster_df["StudentID"].astype(str).str.strip().str.upper()
            roster_df["Name"] = roster_df["Name"].astype(str).str.strip()
            roster_df["Department"] = roster_df["Department"].astype(str).str.strip()
            roster_df = roster_df.drop_duplicates(subset=["StudentID"], keep="last")
            return roster_df
        except Exception:
            pass

    # Fallback / derivation from attendance_df
    if not attendance_df.empty:
        roster_df = attendance_df[["StudentID", "Name", "Department"]].drop_duplicates(subset=["StudentID"])
    else:
        roster_df = pd.DataFrame(columns=["StudentID", "Name", "Department"])

    roster_df.to_csv(STUDENTS_FILE, index=False)
    return roster_df


def save_students_roster(roster_df):
    """Saves updated student roster to students.csv."""
    roster_df = roster_df.sort_values(by="StudentID").reset_index(drop=True)
    roster_df.to_csv(STUDENTS_FILE, index=False)


def update_student_record(old_id, new_id, new_name, new_dept, roster_df, attendance_df):
    """
    Updates student roll number/ID, name, and department.
    Cascades changes from students.csv to attendance_data.csv so history remains intact.
    """
    old_id = str(old_id).strip().upper()
    new_id = str(new_id).strip().upper()
    new_name = str(new_name).strip().title()
    new_dept = str(new_dept).strip()

    if not new_id:
        return False, "Roll number / Student ID cannot be empty."
    if not new_name:
        return False, "Student name cannot be empty."
    if not new_dept:
        return False, "Department cannot be empty."

    # If ID changed, ensure new ID is not already used by another student
    if new_id != old_id:
        existing_ids = roster_df[roster_df["StudentID"].str.upper() != old_id]["StudentID"].str.upper().tolist()
        if new_id in existing_ids:
            return False, f"Student ID / Roll number '{new_id}' is already assigned to another student!"

    # 1. Update in roster
    mask_roster = roster_df["StudentID"].str.upper() == old_id
    if not mask_roster.any():
        return False, f"Student '{old_id}' not found in roster."

    roster_df.loc[mask_roster, "StudentID"] = new_id
    roster_df.loc[mask_roster, "Name"] = new_name
    roster_df.loc[mask_roster, "Department"] = new_dept
    save_students_roster(roster_df)

    # 2. Cascade update to attendance_data.csv
    updated_attendance_count = 0
    if not attendance_df.empty:
        mask_att = attendance_df["StudentID"].str.upper() == old_id
        updated_attendance_count = int(mask_att.sum())
        if updated_attendance_count > 0:
            attendance_df.loc[mask_att, "StudentID"] = new_id
            attendance_df.loc[mask_att, "Name"] = new_name
            attendance_df.loc[mask_att, "Department"] = new_dept
            save_attendance_data(attendance_df)

    return True, f"Successfully updated student: '{new_name}' ({new_id}). Synchronized {updated_attendance_count} attendance records."


def delete_student_record(student_id, roster_df, attendance_df, delete_attendance=True):
    """
    Deletes a student from the roster and optionally deletes their attendance history.
    """
    student_id = str(student_id).strip().upper()
    roster_df = roster_df[roster_df["StudentID"].str.upper() != student_id]
    save_students_roster(roster_df)

    deleted_count = 0
    if delete_attendance and not attendance_df.empty:
        mask = attendance_df["StudentID"].str.upper() == student_id
        deleted_count = int(mask.sum())
        attendance_df = attendance_df[~mask]
        save_attendance_data(attendance_df)

    return True, f"Removed student '{student_id}'. Deleted {deleted_count} historical attendance records."


def update_single_attendance(date_str, student_id, new_status, attendance_df, roster_df):
    """
    Updates or creates an attendance record for a specific student and date.
    """
    student_id = str(student_id).strip().upper()
    date_str = str(date_str).strip()
    new_status = "Present" if new_status in ["Present", "P", "1"] else "Absent"

    roster_match = roster_df[roster_df["StudentID"].str.upper() == student_id]
    if roster_match.empty:
        name = "Unknown"
        dept = "Unknown"
    else:
        name = roster_match.iloc[0]["Name"]
        dept = roster_match.iloc[0]["Department"]

    mask = (attendance_df["Date"] == date_str) & (attendance_df["StudentID"].str.upper() == student_id)
    if mask.any():
        attendance_df.loc[mask, "Status"] = new_status
        attendance_df.loc[mask, "Name"] = name
        attendance_df.loc[mask, "Department"] = dept
        action = "Updated"
    else:
        new_row = pd.DataFrame([{
            "Date": date_str,
            "StudentID": student_id,
            "Name": name,
            "Department": dept,
            "Status": new_status
        }])
        attendance_df = pd.concat([attendance_df, new_row], ignore_index=True)
        action = "Recorded"

    save_attendance_data(attendance_df)
    return True, f"{action} attendance for {name} ({student_id}) on {date_str} as '{new_status}'."


def delete_attendance_date(date_str, attendance_df):
    """Deletes all attendance records for a specific date."""
    date_str = str(date_str).strip()
    mask = attendance_df["Date"] == date_str
    count = int(mask.sum())
    if count == 0:
        return False, f"No records found for date {date_str}."
    updated_df = attendance_df[~mask]
    save_attendance_data(updated_df)
    return True, f"Deleted {count} attendance records for date {date_str}."



# ==========================================
# 3. STATISTICAL ANALYSIS & EDA (NUMPY + PANDAS)
# ==========================================
def compute_student_summary(attendance_df, roster_df):
    """
    Data Science Step: Aggregation, Feature Engineering, & Rule-Based Classification
    Calculates:
    - Total Sessions Held
    - Sessions Attended (Present)
    - Sessions Missed (Absent)
    - Attendance Percentage
    - Rule-based Status (Eligible vs Shortage)
    - Actionable classes needed to reach 75%
    """
    if roster_df.empty:
        return pd.DataFrame(columns=[
            "StudentID", "Name", "Department", "TotalClasses",
            "PresentClasses", "AbsentClasses", "AttendancePercentage",
            "Status", "NeedsImprovement", "ClassesNeededFor75"
        ])

    # Distinct dates count in the attendance log
    if attendance_df.empty:
        summary_df = roster_df.copy()
        summary_df["TotalClasses"] = 0
        summary_df["PresentClasses"] = 0
        summary_df["AbsentClasses"] = 0
        summary_df["AttendancePercentage"] = 0.0
        summary_df["Status"] = "Shortage (<75%)"
        summary_df["NeedsImprovement"] = True
        summary_df["ClassesNeededFor75"] = 0
        return summary_df

    # Aggregate attendance records per student
    # 1. Total days marked for each student
    total_marked = attendance_df.groupby("StudentID")["Date"].nunique().rename("TotalClasses")

    # 2. Total days Present
    present_marked = (
        attendance_df[attendance_df["Status"] == "Present"]
        .groupby("StudentID")["Date"]
        .nunique()
        .rename("PresentClasses")
    )

    # Merge with roster
    summary_df = roster_df.merge(total_marked, on="StudentID", how="left")
    summary_df = summary_df.merge(present_marked, on="StudentID", how="left")

    # Data Cleaning: Handle NaN with 0 using Pandas
    summary_df["TotalClasses"] = summary_df["TotalClasses"].fillna(0).astype(int)
    summary_df["PresentClasses"] = summary_df["PresentClasses"].fillna(0).astype(int)
    summary_df["AbsentClasses"] = summary_df["TotalClasses"] - summary_df["PresentClasses"]

    # Numerical calculation using NumPy (Prevent division by zero)
    summary_df["AttendancePercentage"] = np.where(
        summary_df["TotalClasses"] > 0,
        np.round((summary_df["PresentClasses"] / summary_df["TotalClasses"]) * 100.0, 2),
        0.0
    )

    # Rule-Based Classification:
    # Students with >= 75% are 'Eligible', otherwise 'Shortage (<75%)'
    summary_df["NeedsImprovement"] = summary_df["AttendancePercentage"] < ATTENDANCE_THRESHOLD
    summary_df["Status"] = np.where(
        summary_df["AttendancePercentage"] >= ATTENDANCE_THRESHOLD,
        "Eligible (≥75%)",
        "Shortage (<75%)"
    )

    # Fine-grained categorization for insights:
    conditions = [
        summary_df["AttendancePercentage"] >= 90.0,
        (summary_df["AttendancePercentage"] >= 75.0) & (summary_df["AttendancePercentage"] < 90.0),
        (summary_df["AttendancePercentage"] >= 60.0) & (summary_df["AttendancePercentage"] < 75.0),
        summary_df["AttendancePercentage"] < 60.0,
    ]
    choices = ["Excellent (≥90%)", "Good (75-89%)", "Warning (60-74%)", "Critical (<60%)"]
    summary_df["PerformanceGrade"] = np.select(conditions, choices, default="Unclassified")

    # Statistical computation: Calculate how many upcoming consecutive classes
    # a student must attend to reach the 75% threshold.
    # Formula: (Present + x) / (Total + x) >= 0.75  ==>  x >= 3*Total - 4*Present
    total_val = summary_df["TotalClasses"].values
    pres_val = summary_df["PresentClasses"].values
    classes_needed = np.maximum(0, np.ceil(3 * total_val - 4 * pres_val).astype(int))
    summary_df["ClassesNeededFor75"] = np.where(summary_df["NeedsImprovement"], classes_needed, 0)

    # Sort by StudentID
    summary_df = summary_df.sort_values(by="StudentID").reset_index(drop=True)
    return summary_df


def compute_class_statistics(summary_df):
    """
    Data Science Step: Descriptive Statistical Analysis using NumPy
    Calculates summary statistics: Mean, Median, Min, Max, Standard Deviation.
    """
    if summary_df.empty or summary_df["TotalClasses"].sum() == 0:
        return {
            "total_students": len(summary_df),
            "mean_attendance": 0.0,
            "median_attendance": 0.0,
            "std_attendance": 0.0,
            "min_attendance": 0.0,
            "max_attendance": 0.0,
            "defaulters_count": 0,
            "defaulters_pct": 0.0,
            "eligible_count": 0,
        }

    pct_values = summary_df["AttendancePercentage"].values
    total_students = len(summary_df)
    defaulters = int(np.sum(pct_values < ATTENDANCE_THRESHOLD))
    eligible = total_students - defaulters

    stats = {
        "total_students": total_students,
        "mean_attendance": float(np.round(np.mean(pct_values), 2)),
        "median_attendance": float(np.round(np.median(pct_values), 2)),
        "std_attendance": float(np.round(np.std(pct_values), 2)),
        "min_attendance": float(np.round(np.min(pct_values), 2)),
        "max_attendance": float(np.round(np.max(pct_values), 2)),
        "defaulters_count": defaulters,
        "defaulters_pct": float(np.round((defaulters / total_students) * 100.0, 2)) if total_students > 0 else 0.0,
        "eligible_count": eligible,
    }
    return stats


# ==========================================
# 4. DATA VISUALIZATION (MATPLOTLIB)
# ==========================================
def plot_student_attendance_bar(summary_df):
    """
    Data Science Step: Exploratory Data Visualization
    Bar chart showing each student's attendance percentage.
    Bars are color-coded: Green for >= 75%, Red for < 75%.
    Includes a 75% threshold benchmark line.
    """
    if summary_df.empty:
        fig, ax = plt.subplots(figsize=(8, 3))
        ax.text(0.5, 0.5, "No attendance data available to plot", ha="center", va="center")
        ax.axis("off")
        return fig

    # Create figure and axis
    fig, ax = plt.subplots(figsize=(10, 5.5))

    names = summary_df["Name"].tolist()
    percentages = summary_df["AttendancePercentage"].tolist()
    student_ids = summary_df["StudentID"].tolist()
    labels = [f"{sid}\n{name.split()[0]}" for sid, name in zip(student_ids, names)]

    # Rule-based conditional color mapping
    colors = ["#2ECC71" if p >= ATTENDANCE_THRESHOLD else "#E74C3C" for p in percentages]

    # Plot bars
    bars = ax.bar(labels, percentages, color=colors, width=0.6, edgecolor="#2C3E50", linewidth=0.8)

    # 75% benchmark threshold line
    ax.axhline(
        ATTENDANCE_THRESHOLD,
        color="#C0392B",
        linestyle="--",
        linewidth=2,
        label=f"Minimum Required Threshold ({ATTENDANCE_THRESHOLD}%)"
    )

    # Add data labels on top of each bar
    for bar in bars:
        height = bar.get_height()
        ax.annotate(
            f"{height:.1f}%",
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 4),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=8.5,
            fontweight="bold"
        )

    ax.set_ylim(0, 115)
    ax.set_ylabel("Attendance Percentage (%)", fontsize=11, fontweight="bold")
    ax.set_xlabel("Students", fontsize=11, fontweight="bold")
    ax.set_title("Student Attendance Percentage vs. 75% Benchmark", fontsize=13, fontweight="bold", pad=12)
    ax.grid(axis="y", linestyle=":", alpha=0.6)
    ax.legend(loc="upper right", framealpha=0.9)
    plt.xticks(rotation=20, ha="right", fontsize=9)
    plt.tight_layout()
    return fig


def plot_department_analysis(summary_df):
    """
    Bar chart comparing average attendance percentage across academic departments.
    Demonstrates aggregation with Pandas groupby and visualization with Matplotlib.
    """
    if summary_df.empty or "Department" not in summary_df.columns:
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.text(0.5, 0.5, "No department data available", ha="center", va="center")
        ax.axis("off")
        return fig

    dept_stats = summary_df.groupby("Department")["AttendancePercentage"].mean().reset_index()
    dept_stats["AttendancePercentage"] = dept_stats["AttendancePercentage"].round(2)

    fig, ax = plt.subplots(figsize=(8, 4.5))
    departments = dept_stats["Department"].tolist()
    dept_pcts = dept_stats["AttendancePercentage"].tolist()
    colors = ["#3498DB", "#9B59B6", "#1ABC9C", "#F39C12", "#E67E22"][:len(departments)]

    bars = ax.bar(departments, dept_pcts, color=colors, width=0.5, edgecolor="#34495E", linewidth=0.8)
    ax.axhline(ATTENDANCE_THRESHOLD, color="#E74C3C", linestyle="--", linewidth=1.8, label="75% Requirement")

    for bar in bars:
        height = bar.get_height()
        ax.annotate(
            f"{height:.1f}%",
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 3),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=9.5,
            fontweight="bold"
        )

    ax.set_ylim(0, 115)
    ax.set_ylabel("Average Attendance (%)", fontsize=10, fontweight="bold")
    ax.set_title("Department-Wise Average Attendance Comparison", fontsize=12, fontweight="bold", pad=10)
    ax.grid(axis="y", linestyle=":", alpha=0.5)
    ax.legend(loc="lower right")
    plt.xticks(rotation=15, ha="right")
    plt.tight_layout()
    return fig


def plot_status_donut(summary_df):
    """
    Donut chart showing student attendance status breakdown:
    Eligible (>= 75%) vs. Shortage (< 75%).
    """
    if summary_df.empty:
        fig, ax = plt.subplots(figsize=(4, 4))
        ax.axis("off")
        return fig

    eligible_count = int(np.sum(summary_df["AttendancePercentage"] >= ATTENDANCE_THRESHOLD))
    shortage_count = len(summary_df) - eligible_count

    fig, ax = plt.subplots(figsize=(4.5, 4.5))
    labels = [f"Eligible (≥75%)\n[{eligible_count}]", f"Shortage (<75%)\n[{shortage_count}]"]
    counts = [eligible_count, shortage_count]
    colors = ["#2ECC71", "#E74C3C"]

    # Donut chart
    wedges, texts, autotexts = ax.pie(
        counts,
        labels=labels,
        colors=colors,
        autopct="%1.1f%%",
        startangle=140,
        pctdistance=0.75,
        textprops=dict(color="#2C3E50", fontweight="bold", fontsize=9.5),
        wedgeprops=dict(width=0.45, edgecolor="white", linewidth=2)
    )

    for autotext in autotexts:
        autotext.set_fontsize(10)
        autotext.set_color("white")

    ax.set_title("Attendance Eligibility Distribution", fontsize=11, fontweight="bold", pad=10)
    plt.tight_layout()
    return fig


def plot_daily_attendance_trend(attendance_df):
    """
    Line chart tracking overall class attendance percentage day-by-day.
    Demonstrates time-series aggregation using Pandas.
    """
    if attendance_df.empty:
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.text(0.5, 0.5, "No daily attendance logs found", ha="center", va="center")
        ax.axis("off")
        return fig

    # Group by Date and calculate daily %
    daily = attendance_df.groupby("Date").apply(
        lambda g: (np.sum(g["Status"] == "Present") / len(g)) * 100.0
    ).reset_index(name="DailyPercentage")
    daily["DailyPercentage"] = daily["DailyPercentage"].round(2)
    daily = daily.sort_values(by="Date")

    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(daily["Date"], daily["DailyPercentage"], marker="o", color="#2980B9", linewidth=2.2, markersize=6)
    ax.axhline(ATTENDANCE_THRESHOLD, color="#E74C3C", linestyle="--", linewidth=1.5, label="75% Target")

    for i, row in daily.iterrows():
        ax.annotate(
            f"{row['DailyPercentage']:.0f}%",
            xy=(row["Date"], row["DailyPercentage"]),
            xytext=(0, 6),
            textcoords="offset points",
            ha="center",
            fontsize=8.5,
            fontweight="bold"
        )

    ax.set_ylim(0, 115)
    ax.set_ylabel("Present %", fontsize=10, fontweight="bold")
    ax.set_xlabel("Date", fontsize=10, fontweight="bold")
    ax.set_title("Daily Attendance Turnout Trend", fontsize=12, fontweight="bold", pad=10)
    ax.grid(True, linestyle=":", alpha=0.5)
    ax.legend(loc="lower left")
    plt.xticks(rotation=30, ha="right", fontsize=8.5)
    plt.tight_layout()
    return fig


# ==========================================
# 5. STREAMLIT USER INTERFACE & NAVIGATION
# ==========================================
def main():
    # Load data
    attendance_df = load_attendance_data()
    roster_df = load_students_roster(attendance_df)
    summary_df = compute_student_summary(attendance_df, roster_df)
    stats = compute_class_statistics(summary_df)

    # Sidebar Header & Navigation
    with st.sidebar:
        st.markdown("## 🎓 Attendance Portal")
        st.caption("Python & Data Science System")
        st.markdown("---")

        menu = st.radio(
            "Select Section",
            [
                "📊 Dashboard & Insights",
                "📝 Mark Daily Attendance",
                "✏️ Edit & Update Records",
                "⚠️ Attendance Shortage (<75%)",
                "📋 Attendance Register",
                "👤 Student Registration",
                "📁 CSV Import & Export",
                "🔬 Data Science Concepts"
            ],
            index=0
        )

        st.markdown("---")
        st.markdown("### 📌 Quick Overview")
        st.markdown(f"**Total Enrolled:** `{stats['total_students']}` students")
        st.markdown(f"**Average Attendance:** `{stats['mean_attendance']}%`")
        st.markdown(f"**Below 75% Threshold:** `{stats['defaulters_count']}` students")
        st.caption("Data saved to `attendance_data.csv`")

    # ----------------------------------------------------
    # SECTION 1: DASHBOARD & INSIGHTS
    # ----------------------------------------------------
    if menu == "📊 Dashboard & Insights":
        st.markdown('<p class="main-header">📊 Student Attendance Dashboard</p>', unsafe_allow_html=True)
        st.markdown('<p class="sub-header">Real-time attendance analysis, KPI metrics, and graphical visualizations.</p>', unsafe_allow_html=True)

        # KPI Metrics Row
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Students", stats["total_students"], help="Total registered students in roster")
        with col2:
            total_sessions = attendance_df["Date"].nunique() if not attendance_df.empty else 0
            st.metric("Total Sessions Held", total_sessions, help="Distinct dates where attendance was recorded")
        with col3:
            st.metric(
                "Class Average Attendance",
                f"{stats['mean_attendance']}%",
                delta=f"{stats['mean_attendance'] - ATTENDANCE_THRESHOLD:.1f}% vs 75% Goal",
                help="Mean attendance percentage across all enrolled students"
            )
        with col4:
            defaulter_delta = f"{stats['defaulters_pct']}% of class"
            st.metric(
                "Below 75% Threshold",
                stats["defaulters_count"],
                delta=f"-{stats['defaulters_count']} at risk",
                delta_color="inverse",
                help="Students requiring attendance improvement"
            )

        st.markdown("---")

        # Key Data Insights Cards
        st.markdown("### 💡 Key Data Insights")
        in_col1, in_col2, in_col3 = st.columns(3)

        with in_col1:
            with st.container(border=True):
                st.markdown("#### 🏆 Highest Attendance")
                if not summary_df.empty and summary_df["TotalClasses"].sum() > 0:
                    highest_val = summary_df["AttendancePercentage"].max()
                    top_students = summary_df[summary_df["AttendancePercentage"] == highest_val]
                    top_names = ", ".join(top_students["Name"].tolist()[:2])
                    st.markdown(f"**{top_names}** ({highest_val}%)")
                    st.caption(f"Department: {top_students.iloc[0]['Department']}")
                else:
                    st.write("No attendance marked yet.")

        with in_col2:
            with st.container(border=True):
                st.markdown("#### 🔻 Lowest Attendance")
                if not summary_df.empty and summary_df["TotalClasses"].sum() > 0:
                    lowest_val = summary_df["AttendancePercentage"].min()
                    low_students = summary_df[summary_df["AttendancePercentage"] == lowest_val]
                    low_names = ", ".join(low_students["Name"].tolist()[:2])
                    st.markdown(f"**{low_names}** ({lowest_val}%)")
                    st.caption(f"Department: {low_students.iloc[0]['Department']}")
                else:
                    st.write("No attendance marked yet.")

        with in_col3:
            with st.container(border=True):
                st.markdown("#### 📈 Statistical Summary (NumPy)")
                st.markdown(f"• **Median Attendance:** `{stats['median_attendance']}%`")
                st.markdown(f"• **Standard Deviation:** `{stats['std_attendance']}%`")
                st.markdown(f"• **Eligible Ratio:** `{stats['eligible_count']} / {stats['total_students']}`")

        # Attendance Visualizations Row
        st.markdown("### 📉 Attendance Visualizations (Matplotlib)")
        chart_tab1, chart_tab2, chart_tab3 = st.tabs([
            "📊 Student-Wise Attendance",
            "🏢 Department Breakdown & Eligibility",
            "📅 Daily Attendance Trend"
        ])

        with chart_tab1:
            st.pyplot(plot_student_attendance_bar(summary_df), clear_figure=True)
            st.caption("Green bars indicate students meeting or exceeding the 75% target; red bars represent attendance shortages.")

        with chart_tab2:
            c1, c2 = st.columns([1.3, 1])
            with c1:
                st.pyplot(plot_department_analysis(summary_df), clear_figure=True)
            with c2:
                st.pyplot(plot_status_donut(summary_df), clear_figure=True)

        with chart_tab3:
            st.pyplot(plot_daily_attendance_trend(attendance_df), clear_figure=True)

        # Quick summary table
        st.markdown("---")
        st.markdown("### 📋 Student Attendance Summary Snapshot")
        view_cols = ["StudentID", "Name", "Department", "TotalClasses", "PresentClasses", "AbsentClasses", "AttendancePercentage", "Status"]
        display_df = summary_df[view_cols].rename(columns={
            "TotalClasses": "Total Classes",
            "PresentClasses": "Attended",
            "AbsentClasses": "Missed",
            "AttendancePercentage": "Attendance %"
        })

        # Styling with Streamlit dataframe highlighting
        st.dataframe(
            display_df.style.map(
                lambda val: "background-color: #FEE2E2; color: #991B1B; font-weight: bold;" if val == "Shortage (<75%)"
                else ("background-color: #DCFCE7; color: #166534; font-weight: bold;" if val == "Eligible (≥75%)" else ""),
                subset=["Status"]
            ),
            use_container_width=True
        )

    # ----------------------------------------------------
    # SECTION 2: MARK DAILY ATTENDANCE
    # ----------------------------------------------------
    elif menu == "📝 Mark Daily Attendance":
        st.markdown('<p class="main-header">📝 Record Daily Attendance</p>', unsafe_allow_html=True)
        st.markdown('<p class="sub-header">Select a date and mark each student as Present or Absent.</p>', unsafe_allow_html=True)

        if roster_df.empty:
            st.warning("⚠️ No students found in the roster! Please add students first in the 'Student Registration' section.")
            return

        col_date, col_actions = st.columns([1, 2])
        with col_date:
            selected_date = st.date_input("Attendance Date", value=datetime.date.today(), format="YYYY-MM-DD")
            date_str = selected_date.strftime("%Y-%m-%d")

        # Check if attendance is already recorded for this date
        existing_date_records = attendance_df[attendance_df["Date"] == date_str]
        is_already_marked = not existing_date_records.empty

        with col_actions:
            if is_already_marked:
                st.info(f"ℹ️ Attendance for **{date_str}** has already been recorded ({len(existing_date_records)} entries). Submitting again will update the records for this date.")
            else:
                st.success(f"✨ Ready to record new attendance for **{date_str}**.")

        st.markdown("---")
        st.markdown(f"### Student List for {date_str}")

        # Quick bulk action buttons
        bulk_col1, bulk_col2, _ = st.columns([1, 1, 3])
        mark_all_present = bulk_col1.button("✅ Mark All Present", use_container_width=True)
        mark_all_absent = bulk_col2.button("❌ Mark All Absent", use_container_width=True)

        # Build attendance input table
        # Map previous status if already marked for this date
        prev_status_map = {}
        if is_already_marked:
            prev_status_map = dict(zip(existing_date_records["StudentID"], existing_date_records["Status"]))

        with st.form("mark_attendance_form"):
            attendance_entries = []

            # Display students in an easy-to-use checklist/radio format
            for idx, student in roster_df.iterrows():
                sid = student["StudentID"]
                sname = student["Name"]
                sdept = student["Department"]

                # Determine default state
                if mark_all_present:
                    default_status = "Present"
                elif mark_all_absent:
                    default_status = "Absent"
                else:
                    default_status = prev_status_map.get(sid, "Present")

                c1, c2, c3, c4 = st.columns([1, 2, 2, 2])
                c1.write(f"**{sid}**")
                c2.write(sname)
                c3.write(sdept)
                status_choice = c4.radio(
                    f"Status for {sid}",
                    options=["Present", "Absent"],
                    index=0 if default_status == "Present" else 1,
                    horizontal=True,
                    key=f"status_{sid}_{date_str}",
                    label_visibility="collapsed"
                )

                attendance_entries.append({
                    "Date": date_str,
                    "StudentID": sid,
                    "Name": sname,
                    "Department": sdept,
                    "Status": status_choice
                })

            submitted = st.form_submit_button("💾 Save Attendance Records", use_container_width=True)

        if submitted:
            new_date_df = pd.DataFrame(attendance_entries)
            # Remove existing records for this date to prevent duplicate rows
            cleaned_attendance = attendance_df[attendance_df["Date"] != date_str]
            # Concatenate updated entries
            updated_df = pd.concat([cleaned_attendance, new_date_df], ignore_index=True)
            save_attendance_data(updated_df)

            p_count = (new_date_df["Status"] == "Present").sum()
            a_count = (new_date_df["Status"] == "Absent").sum()
            st.success(f"🎉 Attendance successfully saved for **{date_str}**! (Present: {p_count}, Absent: {a_count})")
            st.rerun()

    # ----------------------------------------------------
    # SECTION 3: EDIT & UPDATE RECORDS
    # ----------------------------------------------------
    elif menu == "✏️ Edit & Update Records":
        st.markdown('<p class="main-header">✏️ Edit & Manage Data</p>', unsafe_allow_html=True)
        st.markdown('<p class="sub-header">Change student names, roll numbers (IDs), departments, or modify attendance records.</p>', unsafe_allow_html=True)

        edit_tab1, edit_tab2, edit_tab3 = st.tabs([
            "👤 Edit Student Details (Name & Roll No)",
            "📅 Edit Daily Attendance Entries",
            "📊 Interactive Spreadsheet Editor"
        ])

        # TAB 1: EDIT STUDENT (NAME, ROLL NO / ID, DEPT)
        with edit_tab1:
            st.markdown("### 👤 Modify Student Information")
            st.caption("Change a student's roll number, name, or department. All historical attendance logs will be automatically updated.")

            if roster_df.empty:
                st.warning("⚠️ No students found in roster to edit.")
            else:
                student_options = [
                    f"{row['StudentID']} - {row['Name']} ({row['Department']})"
                    for _, row in roster_df.iterrows()
                ]
                selected_student_str = st.selectbox(
                    "Select Student to Modify",
                    student_options,
                    key="select_edit_student"
                )

                # Extract selected student ID
                selected_sid = selected_student_str.split(" - ")[0].strip()
                selected_row = roster_df[roster_df["StudentID"] == selected_sid].iloc[0]

                c_form, c_info = st.columns([1.5, 1])

                with c_form:
                    with st.form("edit_student_form"):
                        st.markdown(f"#### Edit Details for: `{selected_sid}`")
                        new_sid = st.text_input("Roll Number / Student ID*", value=selected_row["StudentID"]).strip().upper()
                        new_name = st.text_input("Full Name*", value=selected_row["Name"]).strip()

                        dept_list = [
                            "Computer Science",
                            "Data Science",
                            "Information Technology",
                            "Electronics & Communication",
                            "Mechanical Engineering",
                            "Other"
                        ]
                        current_dept = selected_row["Department"]
                        dept_idx = dept_list.index(current_dept) if current_dept in dept_list else dept_list.index("Other")
                        new_dept_choice = st.selectbox("Department*", dept_list, index=dept_idx)
                        if new_dept_choice == "Other":
                            new_dept = st.text_input("Custom Department Name*", value=current_dept if current_dept not in dept_list else "").strip()
                        else:
                            new_dept = new_dept_choice

                        submitted_edit = st.form_submit_button("💾 Save Student Changes", use_container_width=True)

                    if submitted_edit:
                        success, msg = update_student_record(
                            selected_sid, new_sid, new_name, new_dept, roster_df, attendance_df
                        )
                        if success:
                            st.success(f"🎉 {msg}")
                            st.rerun()
                        else:
                            st.error(f"❌ {msg}")

                with c_info:
                    st.markdown("#### 📌 Current Attendance Record")
                    stu_summary = summary_df[summary_df["StudentID"] == selected_sid]
                    if not stu_summary.empty:
                        s_row = stu_summary.iloc[0]
                        st.markdown(f"• **Current Attendance:** `{s_row['AttendancePercentage']}%`")
                        st.markdown(f"• **Total Classes Held:** `{s_row['TotalClasses']}`")
                        st.markdown(f"• **Classes Attended:** `{s_row['PresentClasses']}`")
                        st.markdown(f"• **Status:** `{s_row['Status']}`")
                    else:
                        st.write("No attendance records found for this student.")

                    st.markdown("---")
                    with st.expander("🗑️ Delete This Student", expanded=False):
                        st.warning(f"Are you sure you want to delete **{selected_row['Name']} ({selected_sid})**?")
                        confirm_delete = st.checkbox("Yes, permanently remove this student", key=f"del_confirm_{selected_sid}")
                        del_attendance_too = st.checkbox("Also delete all their attendance history", value=True, key=f"del_att_{selected_sid}")
                        if st.button("🗑️ Delete Student", type="secondary", disabled=not confirm_delete):
                            _, del_msg = delete_student_record(selected_sid, roster_df, attendance_df, del_attendance_too)
                            st.success(f"🗑️ {del_msg}")
                            st.rerun()

        # TAB 2: EDIT DAILY ATTENDANCE ENTRIES
        with edit_tab2:
            st.markdown("### 📅 Modify Attendance Entries")
            att_mode = st.radio(
                "Choose Edit Mode",
                ["Quick Single Entry Edit", "Bulk Day Attendance Editor", "Delete Attendance for a Date"],
                horizontal=True
            )

            if att_mode == "Quick Single Entry Edit":
                st.caption("Change the attendance status (Present / Absent) for a specific student on a specific date.")
                q_col1, q_col2, q_col3 = st.columns(3)

                with q_col1:
                    edit_date = st.date_input("Select Date", value=datetime.date.today(), key="quick_date", format="YYYY-MM-DD")
                    edit_date_str = edit_date.strftime("%Y-%m-%d")

                with q_col2:
                    stu_choices = [
                        f"{r['StudentID']} - {r['Name']}" for _, r in roster_df.iterrows()
                    ] if not roster_df.empty else []
                    selected_q_stu = st.selectbox("Select Student", stu_choices, key="quick_stu")
                    selected_q_sid = selected_q_stu.split(" - ")[0].strip() if selected_q_stu else ""

                # Find current status
                curr_status = "Not Recorded"
                if not attendance_df.empty and selected_q_sid:
                    match_rec = attendance_df[
                        (attendance_df["Date"] == edit_date_str) &
                        (attendance_df["StudentID"] == selected_q_sid)
                    ]
                    if not match_rec.empty:
                        curr_status = match_rec.iloc[0]["Status"]

                with q_col3:
                    st.markdown(f"**Current Recorded Status:** `{curr_status}`")
                    new_status_choice = st.radio(
                        "Set New Status",
                        ["Present", "Absent"],
                        index=0 if curr_status == "Present" else 1,
                        horizontal=True,
                        key="quick_new_status"
                    )

                if st.button("💾 Update Attendance Entry", use_container_width=True):
                    if not selected_q_sid:
                        st.error("Please select a student.")
                    else:
                        success, update_msg = update_single_attendance(
                            edit_date_str, selected_q_sid, new_status_choice, attendance_df, roster_df
                        )
                        st.success(f"🎉 {update_msg}")
                        st.rerun()

            elif att_mode == "Bulk Day Attendance Editor":
                st.caption("View and modify attendance for all students on a chosen date at once.")
                all_recorded_dates = sorted(attendance_df["Date"].unique().tolist(), reverse=True) if not attendance_df.empty else []

                bulk_date_sel = st.selectbox(
                    "Choose an existing date to edit, or select 'Custom Date'",
                    all_recorded_dates + ["Custom Date..."],
                    key="bulk_date_picker"
                )

                if bulk_date_sel == "Custom Date...":
                    custom_d = st.date_input("Pick Date", value=datetime.date.today(), key="bulk_custom_d", format="YYYY-MM-DD")
                    target_date_str = custom_d.strftime("%Y-%m-%d")
                else:
                    target_date_str = bulk_date_sel

                date_records = attendance_df[attendance_df["Date"] == target_date_str]
                existing_map = dict(zip(date_records["StudentID"], date_records["Status"]))

                st.markdown(f"#### Attendance for **{target_date_str}** ({len(date_records)} recorded):")

                b_col1, b_col2, _ = st.columns([1, 1, 3])
                b_all_p = b_col1.button("✅ All Present", key="bulk_p_all")
                b_all_a = b_col2.button("❌ All Absent", key="bulk_a_all")

                with st.form("bulk_day_edit_form"):
                    updated_entries = []
                    for _, stu in roster_df.iterrows():
                        sid = stu["StudentID"]
                        sname = stu["Name"]
                        sdept = stu["Department"]

                        if b_all_p:
                            def_st = "Present"
                        elif b_all_a:
                            def_st = "Absent"
                        else:
                            def_st = existing_map.get(sid, "Present")

                        c1, c2, c3, c4 = st.columns([1, 2, 2, 2])
                        c1.write(f"**{sid}**")
                        c2.write(sname)
                        c3.write(sdept)
                        st_val = c4.radio(
                            f"Status {sid}",
                            ["Present", "Absent"],
                            index=0 if def_st == "Present" else 1,
                            horizontal=True,
                            key=f"bulk_st_{sid}_{target_date_str}",
                            label_visibility="collapsed"
                        )
                        updated_entries.append({
                            "Date": target_date_str,
                            "StudentID": sid,
                            "Name": sname,
                            "Department": sdept,
                            "Status": st_val
                        })

                    if st.form_submit_button("💾 Save All Changes for This Date", use_container_width=True):
                        new_day_df = pd.DataFrame(updated_entries)
                        cleaned = attendance_df[attendance_df["Date"] != target_date_str]
                        updated_all = pd.concat([cleaned, new_day_df], ignore_index=True)
                        save_attendance_data(updated_all)
                        st.success(f"🎉 Updated attendance for {target_date_str} successfully!")
                        st.rerun()

            elif att_mode == "Delete Attendance for a Date":
                st.caption("Remove an entire date's attendance log (e.g. if marked on a holiday or by mistake).")
                all_recorded_dates = sorted(attendance_df["Date"].unique().tolist(), reverse=True) if not attendance_df.empty else []
                if not all_recorded_dates:
                    st.write("No recorded dates to delete.")
                else:
                    del_date = st.selectbox("Select Date to Delete", all_recorded_dates, key="del_date_sel")
                    count_to_del = (attendance_df["Date"] == del_date).sum()
                    st.warning(f"This will delete all **{count_to_del} records** on **{del_date}**.")
                    confirm_del_date = st.checkbox("I confirm I want to delete this date's records", key="confirm_del_date")
                    if st.button("🗑️ Delete This Date's Attendance", disabled=not confirm_del_date, type="secondary"):
                        success, d_msg = delete_attendance_date(del_date, attendance_df)
                        st.success(f"🗑️ {d_msg}")
                        st.rerun()

        # TAB 3: INTERACTIVE SPREADSHEET EDITOR (DATA_EDITOR)
        with edit_tab3:
            st.markdown("### 📊 Interactive Spreadsheet Editor")
            st.caption("Double-click any cell to edit data directly in the grid, add new rows, or delete rows. Then click 'Save Changes'.")

            grid_choice = st.radio("Choose Table to Edit", ["👤 Student Roster Table", "📅 Attendance Logs Table"], horizontal=True)

            if grid_choice == "👤 Student Roster Table":
                st.info("💡 Edit student names, roll numbers (IDs), or departments directly below. Duplicate Student IDs will be prevented upon saving.")
                edited_roster = st.data_editor(
                    roster_df,
                    num_rows="dynamic",
                    use_container_width=True,
                    key="grid_roster_editor"
                )

                if st.button("💾 Save Roster Table Changes", use_container_width=True):
                    # Validation
                    edited_roster["StudentID"] = edited_roster["StudentID"].astype(str).str.strip().str.upper()
                    edited_roster["Name"] = edited_roster["Name"].astype(str).str.strip().str.title()
                    edited_roster["Department"] = edited_roster["Department"].astype(str).str.strip()

                    # Drop empties
                    edited_roster = edited_roster[(edited_roster["StudentID"] != "") & (edited_roster["Name"] != "")]

                    # Check uniqueness
                    if edited_roster["StudentID"].duplicated().any():
                        dups = edited_roster[edited_roster["StudentID"].duplicated()]["StudentID"].tolist()
                        st.error(f"❌ Duplicate Student IDs found: {dups}. Each Student ID must be unique!")
                    else:
                        save_students_roster(edited_roster)

                        # Sync names & departments to attendance_df
                        for _, r in edited_roster.iterrows():
                            mask = attendance_df["StudentID"].str.upper() == r["StudentID"]
                            attendance_df.loc[mask, "Name"] = r["Name"]
                            attendance_df.loc[mask, "Department"] = r["Department"]
                        save_attendance_data(attendance_df)

                        st.success("🎉 Student roster updated and synchronized with attendance records!")
                        st.rerun()

            elif grid_choice == "📅 Attendance Logs Table":
                st.info("💡 Edit dates or change status (Present / Absent) directly in the table.")

                # Filter controls for convenience
                fc1, fc2 = st.columns(2)
                with fc1:
                    filter_d = st.selectbox(
                        "Filter by Date",
                        ["All Dates"] + sorted(attendance_df["Date"].unique().tolist(), reverse=True) if not attendance_df.empty else ["All Dates"]
                    )
                with fc2:
                    filter_s = st.selectbox(
                        "Filter by Student",
                        ["All Students"] + sorted(attendance_df["StudentID"].unique().tolist()) if not attendance_df.empty else ["All Students"]
                    )

                display_att = attendance_df.copy()
                if filter_d != "All Dates":
                    display_att = display_att[display_att["Date"] == filter_d]
                if filter_s != "All Students":
                    display_att = display_att[display_att["StudentID"] == filter_s]

                edited_att = st.data_editor(
                    display_att,
                    column_config={
                        "Status": st.column_config.SelectboxColumn(
                            "Status",
                            help="Attendance Status",
                            options=["Present", "Absent"],
                            required=True
                        )
                    },
                    num_rows="dynamic",
                    use_container_width=True,
                    key="grid_att_editor"
                )

                if st.button("💾 Save Attendance Table Changes", use_container_width=True):
                    # Clean and validate
                    edited_att["Date"] = edited_att["Date"].astype(str).str.strip()
                    edited_att["StudentID"] = edited_att["StudentID"].astype(str).str.strip().str.upper()
                    edited_att["Status"] = edited_att["Status"].apply(lambda s: "Present" if s in ["Present", "P", "1"] else "Absent")

                    # If filtered, merge back into attendance_df
                    if filter_d != "All Dates" or filter_s != "All Students":
                        cleaned_base = attendance_df.copy()
                        if filter_d != "All Dates":
                            cleaned_base = cleaned_base[cleaned_base["Date"] != filter_d]
                        if filter_s != "All Students":
                            cleaned_base = cleaned_base[cleaned_base["StudentID"] != filter_s]
                        merged_att = pd.concat([cleaned_base, edited_att], ignore_index=True)
                    else:
                        merged_att = edited_att

                    merged_att = merged_att.drop_duplicates(subset=["Date", "StudentID"], keep="last")
                    save_attendance_data(merged_att)
                    st.success("🎉 Attendance logs successfully saved!")
                    st.rerun()

    # ----------------------------------------------------
    # SECTION 4: ATTENDANCE SHORTAGE (< 75%)
    # ----------------------------------------------------
    elif menu == "⚠️ Attendance Shortage (<75%)":
        st.markdown('<p class="main-header">⚠️ Attendance Improvement Required</p>', unsafe_allow_html=True)
        st.markdown('<p class="sub-header">Students whose attendance is below the mandatory 75% requirement.</p>', unsafe_allow_html=True)

        defaulters_df = summary_df[summary_df["NeedsImprovement"]].copy()

        if defaulters_df.empty:
            st.balloons()
            st.success("🎉 Excellent! All enrolled students currently maintain an attendance percentage of 75% or higher!")
        else:
            st.error(f"⚠️ **{len(defaulters_df)} student(s)** currently do not meet the 75% attendance criterion.")

            # Summary metrics for defaulters
            c1, c2, c3 = st.columns(3)
            c1.metric("Shortage Students Count", len(defaulters_df))
            c2.metric("Shortage Percentage of Class", f"{stats['defaulters_pct']}%")
            avg_defaulter_pct = np.round(np.mean(defaulters_df["AttendancePercentage"].values), 2)
            c3.metric("Defaulters Average Attendance", f"{avg_defaulter_pct}%")

            st.markdown("---")
            st.markdown("### 📋 Defaulters List & Target Action Plan")

            display_cols = [
                "StudentID", "Name", "Department", "TotalClasses",
                "PresentClasses", "AttendancePercentage", "ClassesNeededFor75", "PerformanceGrade"
            ]
            defaulter_table = defaulters_df[display_cols].rename(columns={
                "TotalClasses": "Total Classes",
                "PresentClasses": "Attended",
                "AttendancePercentage": "Current %",
                "ClassesNeededFor75": "Consecutive Classes Needed For 75%",
                "PerformanceGrade": "Severity"
            })

            st.dataframe(
                defaulter_table.style.map(
                    lambda val: "background-color: #FEE2E2; color: #991B1B; font-weight: bold;" if "Critical" in str(val)
                    else ("background-color: #FEF3C7; color: #92400E; font-weight: bold;" if "Warning" in str(val) else ""),
                    subset=["Severity"]
                ),
                use_container_width=True
            )

            # Actionable insight note
            st.info("""
            **💡 How "Consecutive Classes Needed" is calculated:**
            Using the formula: `x = max(0, ceil(3 * Total - 4 * Present))`.
            This tells the student exactly how many continuous upcoming classes they must attend without an absence to bring their attendance percentage back to 75%.
            """)

            # CSV Download for defaulters
            csv_buffer = io.StringIO()
            defaulters_df.to_csv(csv_buffer, index=False)
            st.download_button(
                label="📥 Download Defaulters Report (CSV)",
                data=csv_buffer.getvalue(),
                file_name=f"defaulters_below_75_{datetime.date.today()}.csv",
                mime="text/csv",
                use_container_width=True
            )

    # ----------------------------------------------------
    # SECTION 4: FULL ATTENDANCE REGISTER
    # ----------------------------------------------------
    elif menu == "📋 Attendance Register":
        st.markdown('<p class="main-header">📋 Complete Attendance Register</p>', unsafe_allow_html=True)
        st.markdown('<p class="sub-header">Search, filter, and view date-wise attendance records.</p>', unsafe_allow_html=True)

        tab_matrix, tab_raw = st.tabs(["🗓️ Date-Wise Matrix View", "📄 Raw Attendance Logs"])

        with tab_matrix:
            st.markdown("#### Student Attendance Pivot Table")
            if not attendance_df.empty:
                # Pivot table: Rows = StudentID & Name, Columns = Date, Values = Status
                pivot = attendance_df.pivot_table(
                    index=["StudentID", "Name", "Department"],
                    columns="Date",
                    values="Status",
                    aggfunc="first",
                    fill_value="Not Recorded"
                ).reset_index()

                # Add percentage column
                pivot = pivot.merge(summary_df[["StudentID", "AttendancePercentage", "Status"]], on="StudentID", how="left")
                pivot = pivot.rename(columns={"AttendancePercentage": "Attendance %", "Status": "Eligibility"})
                st.dataframe(pivot, use_container_width=True)
            else:
                st.write("No attendance logs found.")

        with tab_raw:
            st.markdown("#### Filterable Raw Attendance Records")
            f_col1, f_col2, f_col3 = st.columns(3)
            with f_col1:
                dept_filter = st.selectbox(
                    "Filter by Department",
                    ["All"] + sorted(attendance_df["Department"].unique().tolist()) if not attendance_df.empty else ["All"]
                )
            with f_col2:
                status_filter = st.selectbox("Filter by Status", ["All", "Present", "Absent"])
            with f_col3:
                search_query = st.text_input("Search Student Name or ID", "")

            filtered_df = attendance_df.copy()
            if dept_filter != "All":
                filtered_df = filtered_df[filtered_df["Department"] == dept_filter]
            if status_filter != "All":
                filtered_df = filtered_df[filtered_df["Status"] == status_filter]
            if search_query.strip():
                q = search_query.strip().lower()
                filtered_df = filtered_df[
                    filtered_df["Name"].str.lower().str.contains(q) |
                    filtered_df["StudentID"].str.lower().str.contains(q)
                ]

            st.write(f"Showing **{len(filtered_df)}** records:")
            st.dataframe(filtered_df, use_container_width=True)

    # ----------------------------------------------------
    # SECTION 5: STUDENT REGISTRATION
    # ----------------------------------------------------
    elif menu == "👤 Student Registration":
        st.markdown('<p class="main-header">👤 Student Management</p>', unsafe_allow_html=True)
        st.markdown('<p class="sub-header">Add new students, update existing student names, or change roll numbers.</p>', unsafe_allow_html=True)

        reg_tab1, reg_tab2, reg_tab3 = st.tabs([
            "➕ Register New Student",
            "✏️ Edit Existing Student (Name / Roll No)",
            "📋 Enrolled Students Roster"
        ])

        with reg_tab1:
            existing_ids = roster_df["StudentID"].tolist() if not roster_df.empty else []

            with st.form("add_student_form", clear_on_submit=True):
                st.markdown("#### Enter New Student Information")
                c1, c2 = st.columns(2)
                with c1:
                    new_id = st.text_input("Roll Number / Student ID (e.g. CS104, DS105)*", "").strip().upper()
                    new_name = st.text_input("Full Name*", "").strip()
                with c2:
                    dept_options = [
                        "Computer Science",
                        "Data Science",
                        "Information Technology",
                        "Electronics & Communication",
                        "Mechanical Engineering",
                        "Other"
                    ]
                    selected_dept = st.selectbox("Department*", dept_options, key="add_stu_dept")
                    if selected_dept == "Other":
                        custom_dept = st.text_input("Enter Department Name*", key="add_stu_custom_dept").strip()
                        department = custom_dept
                    else:
                        department = selected_dept

                submitted = st.form_submit_button("➕ Register Student", use_container_width=True)

            if submitted:
                # Input validation
                if not new_id:
                    st.error("❌ Student ID cannot be empty.")
                elif not new_name:
                    st.error("❌ Student Name cannot be empty.")
                elif not department:
                    st.error("❌ Department cannot be empty.")
                elif new_id in existing_ids:
                    st.error(f"❌ Student ID '{new_id}' already exists! Please use a unique Student ID.")
                else:
                    new_entry = pd.DataFrame([{
                        "StudentID": new_id,
                        "Name": new_name.title(),
                        "Department": department
                    }])
                    updated_roster = pd.concat([roster_df, new_entry], ignore_index=True)
                    save_students_roster(updated_roster)
                    st.success(f"🎉 Student **{new_name.title()} ({new_id})** registered successfully!")
                    st.rerun()

        with reg_tab2:
            st.markdown("#### Modify Student Name, Roll Number, or Department")
            if roster_df.empty:
                st.warning("No students available to edit.")
            else:
                student_options = [
                    f"{row['StudentID']} - {row['Name']} ({row['Department']})"
                    for _, row in roster_df.iterrows()
                ]
                sel_stu = st.selectbox("Select Student to Edit", student_options, key="reg_edit_select")
                target_sid = sel_stu.split(" - ")[0].strip()
                cur_row = roster_df[roster_df["StudentID"] == target_sid].iloc[0]

                with st.form("reg_edit_student_form"):
                    e_c1, e_c2 = st.columns(2)
                    with e_c1:
                        e_id = st.text_input("Roll Number / Student ID*", value=cur_row["StudentID"]).strip().upper()
                        e_name = st.text_input("Full Name*", value=cur_row["Name"]).strip()
                    with e_c2:
                        dept_list = [
                            "Computer Science",
                            "Data Science",
                            "Information Technology",
                            "Electronics & Communication",
                            "Mechanical Engineering",
                            "Other"
                        ]
                        cur_dept = cur_row["Department"]
                        d_idx = dept_list.index(cur_dept) if cur_dept in dept_list else dept_list.index("Other")
                        e_dept_sel = st.selectbox("Department*", dept_list, index=d_idx, key="reg_edit_dept_sel")
                        if e_dept_sel == "Other":
                            e_dept = st.text_input("Custom Department Name*", value=cur_dept if cur_dept not in dept_list else "", key="reg_edit_cust_dept").strip()
                        else:
                            e_dept = e_dept_sel

                    submit_e = st.form_submit_button("💾 Save Changes", use_container_width=True)

                if submit_e:
                    ok, msg = update_student_record(target_sid, e_id, e_name, e_dept, roster_df, attendance_df)
                    if ok:
                        st.success(f"🎉 {msg}")
                        st.rerun()
                    else:
                        st.error(f"❌ {msg}")

        with reg_tab3:
            st.markdown("### 📋 Enrolled Students Roster")
            st.dataframe(roster_df, use_container_width=True)

    # ----------------------------------------------------
    # SECTION 6: CSV IMPORT & EXPORT
    # ----------------------------------------------------
    elif menu == "📁 CSV Import & Export":
        st.markdown('<p class="main-header">📁 Data Management (Upload & Download)</p>', unsafe_allow_html=True)
        st.markdown('<p class="sub-header">Export reports or import external attendance CSV files.</p>', unsafe_allow_html=True)

        exp_col1, exp_col2 = st.columns(2)

        with exp_col1:
            st.markdown("### 📤 Download Reports")
            # 1. Download Attendance Summary
            summary_csv = io.StringIO()
            summary_df.to_csv(summary_csv, index=False)
            st.download_button(
                label="📥 Download Student Attendance Summary (CSV)",
                data=summary_csv.getvalue(),
                file_name=f"attendance_summary_{datetime.date.today()}.csv",
                mime="text/csv",
                use_container_width=True
            )

            # 2. Download Raw Attendance Logs
            raw_csv = io.StringIO()
            attendance_df.to_csv(raw_csv, index=False)
            st.download_button(
                label="📥 Download Raw Attendance Records (CSV)",
                data=raw_csv.getvalue(),
                file_name=f"attendance_raw_{datetime.date.today()}.csv",
                mime="text/csv",
                use_container_width=True
            )

            # 3. Download Sample Template
            template_csv = "Date,StudentID,Name,Department,Status\n2026-03-15,CS101,Alice Johnson,Computer Science,Present\n"
            st.download_button(
                label="📄 Download CSV Template Format",
                data=template_csv,
                file_name="attendance_template.csv",
                mime="text/csv",
                use_container_width=True
            )

        with exp_col2:
            st.markdown("### 📥 Upload CSV File")
            uploaded_file = st.file_uploader("Upload an Attendance CSV", type=["csv"])

            if uploaded_file is not None:
                try:
                    uploaded_df = pd.read_csv(uploaded_file)
                    st.write("Uploaded File Preview:")
                    st.dataframe(uploaded_df.head(), use_container_width=True)

                    required_cols = {"Date", "StudentID", "Name", "Department", "Status"}
                    if not required_cols.issubset(set(uploaded_df.columns)):
                        st.error(f"❌ Uploaded file is missing required columns: {required_cols - set(uploaded_df.columns)}")
                    else:
                        upload_mode = st.radio("Import Mode", ["Append to Existing Records", "Overwrite Existing Records"])
                        if st.button("Apply Uploaded Data", use_container_width=True):
                            if upload_mode == "Overwrite Existing Records":
                                save_attendance_data(uploaded_df)
                            else:
                                combined = pd.concat([attendance_df, uploaded_df], ignore_index=True)
                                combined = combined.drop_duplicates(subset=["Date", "StudentID"], keep="last")
                                save_attendance_data(combined)

                            # Also sync roster
                            roster_from_upload = uploaded_df[["StudentID", "Name", "Department"]].drop_duplicates(subset=["StudentID"])
                            save_students_roster(roster_from_upload)
                            st.success("🎉 Attendance data successfully imported!")
                            st.rerun()
                except Exception as e:
                    st.error(f"Error processing CSV: {e}")

        st.markdown("---")
        st.markdown("### 🔄 Reset to Sample Data")
        if st.button("Re-initialize Default Sample Data", type="secondary"):
            initialize_sample_data()
            if os.path.exists(STUDENTS_FILE):
                os.remove(STUDENTS_FILE)
            st.success("Reset completed with standard 12-student sample dataset!")
            st.rerun()

    # ----------------------------------------------------
    # SECTION 7: DATA SCIENCE CONCEPTS EXPLAINER
    # ----------------------------------------------------
    elif menu == "🔬 Data Science Concepts":
        st.markdown('<p class="main-header">🔬 Data Science Concepts in This Project</p>', unsafe_allow_html=True)
        st.markdown('<p class="sub-header">How Pandas, NumPy, and Matplotlib are applied in student attendance management.</p>', unsafe_allow_html=True)

        ds_tab1, ds_tab2, ds_tab3, ds_tab4 = st.tabs([
            "🐼 Pandas Data Pipeline",
            "🔢 NumPy Numerical & Statistical Operations",
            "📊 Matplotlib Visualization Principles",
            "🎯 Rule-Based Classification"
        ])

        with ds_tab1:
            st.markdown("""
            ### 1. Data Manipulation with Pandas
            * **Data Ingestion & Persistence (`pd.read_csv`, `to_csv`)**:
              Reads persistent CSV files and saves state across app restarts.
            * **Data Cleaning & Handling Missing Values**:
              Handles `NaN` values using `fillna(0)` and removes corrupt entries with `dropna()`.
            * **Deduplication (`drop_duplicates`)**:
              Enforces primary key integrity on `(Date, StudentID)` so updating a date overwrites obsolete entries cleanly.
            * **Grouping & Aggregation (`groupby`)**:
              Aggregates logs by student and department to compute total sessions and present counts:
            ```python
            total_classes = df.groupby('StudentID')['Date'].nunique()
            present_classes = df[df['Status'] == 'Present'].groupby('StudentID')['Date'].nunique()
            ```
            * **Pivot Tables (`pivot_table`)**:
              Transforms flat log records into an intuitive date-wise attendance matrix.
            """)

        with ds_tab2:
            st.markdown(r"""
            ### 2. Numerical Analysis with NumPy
            * **Vectorized Percentage Calculation (`np.where`)**:
              Computes percentages across entire series while guarding against zero division:
            ```python
            attendance_pct = np.where(
                total_classes > 0,
                np.round((present_classes / total_classes) * 100.0, 2),
                0.0
            )
            ```
            * **Descriptive Statistics**:
              * **Mean ($\mu$)**: `np.mean(percentages)` gives the overall class average attendance.
              * **Median ($M$)**: `np.median(percentages)` measures central tendency resilient to outliers.
              * **Standard Deviation ($\sigma$)**: `np.std(percentages)` quantifies attendance variance among students.
              * **Min / Max**: Identifies the lowest and highest performing students.
            * **Defaulter Target Estimation**:
              Computes future classes needed to recover from shortage:
              $$\text{Classes Needed} = \max(0, \lceil 3 \times \text{Total} - 4 \times \text{Present} \rceil)$$
            """)

        with ds_tab3:
            st.markdown("""
            ### 3. Exploratory Data Visualization with Matplotlib
            * **Benchmarking & Thresholding (`ax.axhline`)**:
              Draws a dashed red line at 75% to provide instant visual reference.
            * **Conditional Color Mapping**:
              Dynamically maps bar colors based on rule evaluation:
            ```python
            colors = ['#2ECC71' if pct >= 75.0 else '#E74C3C' for pct in percentages]
            ax.bar(students, percentages, color=colors)
            ```
            * **Direct Data Annotation (`ax.annotate`)**:
              Displays exact percentages directly above each bar for accessibility.
            * **Multi-Aspect EDA**:
              * **Student Bar Chart**: Granular comparison of individual performance.
              * **Department Bar Chart**: Group-level comparison.
              * **Status Donut Chart**: Proportion of compliant vs. non-compliant students.
              * **Time-Series Trend Line**: Daily attendance turnout over time.
            """)

        with ds_tab4:
            st.markdown(r"""
            ### 4. Rule-Based Classification
            Rather than black-box machine learning, student attendance is classified using transparent, rule-based criteria:
            * **Binary Classification**:
              * $\ge 75\%$ $\implies$ **Eligible**
              * $< 75\%$ $\implies$ **Shortage (Defaulter)**
            * **Multi-Class Performance Grading (`np.select`)**:
              * $\ge 90\%$ $\implies$ **Excellent**
              * $75\% - 89.9\%$ $\implies$ **Good / Eligible**
              * $60\% - 74.9\%$ $\implies$ **Warning / Needs Improvement**
              * $< 60\%$ $\implies$ **Critical Shortage**
            """)


if __name__ == "__main__":
    main()
