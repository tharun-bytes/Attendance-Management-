"""
Automated Test Suite for Student Attendance Management System
Validates all data science calculations, Pandas aggregations, NumPy statistics,
and Matplotlib plotting routines.
"""

import os
import unittest
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Import the core application
import app


class TestStudentAttendanceSystem(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Isolate testing files from live application data
        cls.orig_data_file = app.DATA_FILE
        cls.orig_students_file = app.STUDENTS_FILE
        cls.test_data_file = "test_attendance_temp.csv"
        cls.test_students_file = "test_students_temp.csv"

        app.DATA_FILE = cls.test_data_file
        app.STUDENTS_FILE = cls.test_students_file

        # Initialize temporary test files with standard sample data
        app.initialize_sample_data()

    @classmethod
    def tearDownClass(cls):
        # Restore original paths
        app.DATA_FILE = cls.orig_data_file
        app.STUDENTS_FILE = cls.orig_students_file

        # Clean up temporary test files
        for f in [cls.test_data_file, cls.test_students_file]:
            if os.path.exists(f):
                os.remove(f)

    def setUp(self):
        # Create an isolated mock DataFrame for testing
        self.mock_roster = pd.DataFrame([
            {"StudentID": "TEST01", "Name": "Alice Wonder", "Department": "Computer Science"},
            {"StudentID": "TEST02", "Name": "Bob Builder", "Department": "Data Science"},
            {"StudentID": "TEST03", "Name": "Charlie Chaplin", "Department": "Computer Science"},
            {"StudentID": "TEST04", "Name": "Daisy Duck", "Department": "Data Science"},
        ])

        # 4 dates of attendance
        # TEST01: 4/4 Present = 100% (Eligible)
        # TEST02: 3/4 Present = 75%  (Eligible)
        # TEST03: 2/4 Present = 50%  (Shortage)
        # TEST04: 1/4 Present = 25%  (Shortage)
        self.mock_attendance = pd.DataFrame([
            # Date 1
            {"Date": "2026-03-01", "StudentID": "TEST01", "Name": "Alice Wonder", "Department": "Computer Science", "Status": "Present"},
            {"Date": "2026-03-01", "StudentID": "TEST02", "Name": "Bob Builder", "Department": "Data Science", "Status": "Present"},
            {"Date": "2026-03-01", "StudentID": "TEST03", "Name": "Charlie Chaplin", "Department": "Computer Science", "Status": "Present"},
            {"Date": "2026-03-01", "StudentID": "TEST04", "Name": "Daisy Duck", "Department": "Data Science", "Status": "Absent"},
            # Date 2
            {"Date": "2026-03-02", "StudentID": "TEST01", "Name": "Alice Wonder", "Department": "Computer Science", "Status": "Present"},
            {"Date": "2026-03-02", "StudentID": "TEST02", "Name": "Bob Builder", "Department": "Data Science", "Status": "Present"},
            {"Date": "2026-03-02", "StudentID": "TEST03", "Name": "Charlie Chaplin", "Department": "Computer Science", "Status": "Absent"},
            {"Date": "2026-03-02", "StudentID": "TEST04", "Name": "Daisy Duck", "Department": "Data Science", "Status": "Present"},
            # Date 3
            {"Date": "2026-03-03", "StudentID": "TEST01", "Name": "Alice Wonder", "Department": "Computer Science", "Status": "Present"},
            {"Date": "2026-03-03", "StudentID": "TEST02", "Name": "Bob Builder", "Department": "Data Science", "Status": "Present"},
            {"Date": "2026-03-03", "StudentID": "TEST03", "Name": "Charlie Chaplin", "Department": "Computer Science", "Status": "Present"},
            {"Date": "2026-03-03", "StudentID": "TEST04", "Name": "Daisy Duck", "Department": "Data Science", "Status": "Absent"},
            # Date 4
            {"Date": "2026-03-04", "StudentID": "TEST01", "Name": "Alice Wonder", "Department": "Computer Science", "Status": "Present"},
            {"Date": "2026-03-04", "StudentID": "TEST02", "Name": "Bob Builder", "Department": "Data Science", "Status": "Absent"},
            {"Date": "2026-03-04", "StudentID": "TEST03", "Name": "Charlie Chaplin", "Department": "Computer Science", "Status": "Absent"},
            {"Date": "2026-03-04", "StudentID": "TEST04", "Name": "Daisy Duck", "Department": "Data Science", "Status": "Absent"},
        ])

    def test_compute_student_summary(self):
        """Test calculation of attendance percentages and rule-based classifications."""
        summary = app.compute_student_summary(self.mock_attendance, self.mock_roster)
        self.assertEqual(len(summary), 4)

        # Check percentages
        s1 = summary[summary["StudentID"] == "TEST01"].iloc[0]
        self.assertEqual(s1["AttendancePercentage"], 100.0)
        self.assertEqual(s1["Status"], "Eligible (≥75%)")
        self.assertFalse(s1["NeedsImprovement"])
        self.assertEqual(s1["ClassesNeededFor75"], 0)

        s2 = summary[summary["StudentID"] == "TEST02"].iloc[0]
        self.assertEqual(s2["AttendancePercentage"], 75.0)
        self.assertEqual(s2["Status"], "Eligible (≥75%)")
        self.assertFalse(s2["NeedsImprovement"])
        self.assertEqual(s2["ClassesNeededFor75"], 0)

        s3 = summary[summary["StudentID"] == "TEST03"].iloc[0]
        self.assertEqual(s3["AttendancePercentage"], 50.0)
        self.assertEqual(s3["Status"], "Shortage (<75%)")
        self.assertTrue(s3["NeedsImprovement"])
        # Total = 4, Present = 2 ==> Classes needed = 3*4 - 4*2 = 12 - 8 = 4 classes
        self.assertEqual(s3["ClassesNeededFor75"], 4)

        s4 = summary[summary["StudentID"] == "TEST04"].iloc[0]
        self.assertEqual(s4["AttendancePercentage"], 25.0)
        self.assertEqual(s4["Status"], "Shortage (<75%)")
        self.assertTrue(s4["NeedsImprovement"])
        # Total = 4, Present = 1 ==> Classes needed = 3*4 - 4*1 = 12 - 4 = 8 classes
        self.assertEqual(s4["ClassesNeededFor75"], 8)

    def test_compute_class_statistics(self):
        """Test statistical metrics: Mean, Median, Min, Max, Std."""
        summary = app.compute_student_summary(self.mock_attendance, self.mock_roster)
        stats = app.compute_class_statistics(summary)

        # Percentages: [100.0, 75.0, 50.0, 25.0]
        # Mean = 250 / 4 = 62.5%
        # Median = (75.0 + 50.0) / 2 = 62.5%
        # Min = 25.0%, Max = 100.0%
        # Defaulters: 2 (TEST03, TEST04)
        self.assertEqual(stats["total_students"], 4)
        self.assertAlmostEqual(stats["mean_attendance"], 62.5, places=1)
        self.assertAlmostEqual(stats["median_attendance"], 62.5, places=1)
        self.assertEqual(stats["min_attendance"], 25.0)
        self.assertEqual(stats["max_attendance"], 100.0)
        self.assertEqual(stats["defaulters_count"], 2)
        self.assertEqual(stats["eligible_count"], 2)
        self.assertEqual(stats["defaulters_pct"], 50.0)

    def test_matplotlib_plots_render_without_errors(self):
        """Test that all visualization functions generate valid Matplotlib Figures."""
        summary = app.compute_student_summary(self.mock_attendance, self.mock_roster)

        fig1 = app.plot_student_attendance_bar(summary)
        self.assertIsInstance(fig1, plt.Figure)
        plt.close(fig1)

        fig2 = app.plot_department_analysis(summary)
        self.assertIsInstance(fig2, plt.Figure)
        plt.close(fig2)

        fig3 = app.plot_status_donut(summary)
        self.assertIsInstance(fig3, plt.Figure)
        plt.close(fig3)

        fig4 = app.plot_daily_attendance_trend(self.mock_attendance)
        self.assertIsInstance(fig4, plt.Figure)
        plt.close(fig4)

    def test_edge_case_zero_classes(self):
        """Test system behavior when roster exists but zero classes have taken place."""
        empty_attendance = pd.DataFrame(columns=["Date", "StudentID", "Name", "Department", "Status"])
        summary = app.compute_student_summary(empty_attendance, self.mock_roster)
        self.assertEqual(len(summary), 4)
        self.assertTrue((summary["AttendancePercentage"] == 0.0).all())

        stats = app.compute_class_statistics(summary)
        self.assertEqual(stats["total_students"], 4)
        self.assertEqual(stats["mean_attendance"], 0.0)

    def test_live_data_persistence(self):
        """Test actual attendance_data.csv file loading and parsing."""
        live_df = app.load_attendance_data()
        self.assertFalse(live_df.empty)
        self.assertTrue(set(["Date", "StudentID", "Name", "Department", "Status"]).issubset(live_df.columns))

        roster = app.load_students_roster(live_df)
        self.assertGreaterEqual(len(roster), 10)

        summary = app.compute_student_summary(live_df, roster)
        self.assertFalse(summary.empty)
        # Verify 75% threshold filter identifies students
        defaulters = summary[summary["AttendancePercentage"] < 75.0]
        self.assertGreater(len(defaulters), 0)

    def test_update_student_record_cascades(self):
        """Test updating student name and roll number updates both roster and attendance records."""
        roster_copy = self.mock_roster.copy()
        att_copy = self.mock_attendance.copy()

        # Update TEST01 to NEW01 and Alice Wonder to Alice Wonderland
        ok, msg = app.update_student_record("TEST01", "NEW01", "Alice Wonderland", "Data Science", roster_copy, att_copy)
        self.assertTrue(ok)

        # Check roster was updated
        updated_stu = roster_copy[roster_copy["StudentID"] == "NEW01"]
        self.assertEqual(len(updated_stu), 1)
        self.assertEqual(updated_stu.iloc[0]["Name"], "Alice Wonderland")
        self.assertEqual(updated_stu.iloc[0]["Department"], "Data Science")

        # Check attendance records were cascaded
        updated_att = att_copy[att_copy["StudentID"] == "NEW01"]
        self.assertEqual(len(updated_att), 4)
        self.assertTrue((updated_att["Name"] == "Alice Wonderland").all())
        self.assertTrue((updated_att["Department"] == "Data Science").all())

    def test_update_student_duplicate_id_rejected(self):
        """Test that updating an ID to an already existing ID is rejected."""
        roster_copy = self.mock_roster.copy()
        att_copy = self.mock_attendance.copy()

        # Attempt to change TEST01 to TEST02 (which already exists)
        ok, msg = app.update_student_record("TEST01", "TEST02", "Alice Wonder", "Computer Science", roster_copy, att_copy)
        self.assertFalse(ok)
        self.assertIn("already assigned", msg)

    def test_update_single_attendance(self):
        """Test changing attendance status for a student on a specific date."""
        att_copy = self.mock_attendance.copy()
        roster_copy = self.mock_roster.copy()

        # TEST03 was Absent on 2026-03-02, change to Present
        target = att_copy[(att_copy["Date"] == "2026-03-02") & (att_copy["StudentID"] == "TEST03")]
        self.assertEqual(target.iloc[0]["Status"], "Absent")

        ok, msg = app.update_single_attendance("2026-03-02", "TEST03", "Present", att_copy, roster_copy)
        self.assertTrue(ok)

        reloaded = app.load_attendance_data()
        updated_rec = reloaded[(reloaded["Date"] == "2026-03-02") & (reloaded["StudentID"] == "TEST03")]
        self.assertEqual(updated_rec.iloc[0]["Status"], "Present")


if __name__ == "__main__":
    unittest.main()

