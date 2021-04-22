import unittest
import os
import pandas as pd
from pathlib import Path
from src.extractor import Extractor

class TestCourseDataIntegrity(unittest.TestCase):
    COURSE_COLS = ["Career",
                   "Units",
                   "Term",
                   "Campus",
                   "Contact",
                   "Restriction",
                   "Available for Study Abroad and Exchange",
                   "Available for Non-Award Study",
                   "Pre-Requisite",
                   "Assessment",
                   "Syllabus",
                   "Course ID",
                   "Co-Requisite",
                   "Discovery Experience â Global",
                   "Discovery Experience â Working",
                   "Assumed Knowledge",
                   "Incompatible",
                   "Session",
                   "Quota",
                   "Discovery Experience â Community",
                   "Biennial Course"]

    def test_existence_of_required_columns(self):
        course_details_path = Path("data/compiled_data/course_details/")
        for filename in course_details_path.iterdir():
            df = pd.read_csv(str(filename))
            for col in self.COURSE_COLS:
                self.assertTrue(col in df.columns)


class TestClassDataIntegrity(unittest.TestCase):
    CLASS_COLS = ["Class Nbr",
                  "Section",
                  "Size",
                  "Available",
                  "Dates",
                  "Days",
                  "Time",
                  "Location",
                  "Class Type",
                  "Group",
                  "Note",
                  "Subject Area",
                  "Catalogue Number",
                  "Course Title",
                  "Course ID"]

    def test_existence_of_required_columns(self):
        class_details_path = Path("data/compiled_data/class_details/")
        for filename in class_details_path.iterdir():
            df = pd.read_csv(str(filename))
            for col in self.CLASS_COLS:
                self.assertTrue(col in df.columns, "Missing column '%s' in %s" % (col, str(filename)))

    def test_class_number_data(self):
        class_details_path = Path("data/compiled_data/class_details/")
        for filename in class_details_path.iterdir():
            df = pd.read_csv(str(filename))

            # column must not have missing values
            na = df[df['Class Nbr'].isna()]
            self.assertTrue(len(na) == 0, "%d missing values found in the Class Nbr column for %s" % (len(na), str(filename)))

            # column cannot have non integer values
            selected = df[~(df['Class Nbr'].str.isdigit())]
            self.assertTrue(len(selected) == 0, "%d non-integer values found in the Class Nbr column for %s" % (len(selected), str(filename)))


if __name__ == "__main__":
    unittest.main()
