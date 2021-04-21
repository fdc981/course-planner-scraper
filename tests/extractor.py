import unittest
import os
import pandas as pd
from pathlib import Path
from src.extractor import Extractor

class TestExtractorMethods(unittest.TestCase):
    def test_page_with_class_details(self):
        filename = "data/snapshots/AGRIC - Agriculture & Natural Resource/2021-04-13/AGRIC 1520WT - Agricultural Production I - 105341+1+4120+1.html"
        with open(filename, 'r') as f:
            e = Extractor(f.read())
            x = e.course_details_as_df()
            y = e.class_details_as_df()
            z = e.compile_df()

    def test_page_with_group(self):
        filename = "data/snapshots/ANIML SC - Animal Science/2021-04-16/ANIML SC 1016RW - Principles in Animal Behaviour Welfare Ethics I - 104097+1+4120+1.html"
        with open(filename, 'r') as f:
            e = Extractor(f.read())
            x = e.course_details_as_df()
            y = e.class_details_as_df()
            z = e.compile_df()

    def test_page_with_single_row_of_class_details(self):
        filename = "data/snapshots/ORALHLTH - Oral Health/2021-04-16/ORALHLTH 3201AHO - Dental & Health Science IIIOH Part 1 - 101509+1+4110+FY1.html"
        with open(filename, 'r') as f:
            e = Extractor(f.read())
            x = e.course_details_as_df()
            y = e.class_details_as_df()
            z = e.compile_df()

    def test_page_with_no_class_details(self):
        filename = "data/snapshots/DEVT - Development Studies/2021-04-16/DEVT 2010EX - Coffey International Development Internship - 110040+1+4115+1.html"
        with open(filename, 'r') as f:
            e = Extractor(f.read())
            x = e.course_details_as_df()
            y = e.class_details_as_df()
            z = e.compile_df()

    def test_page_with_no_rows(self):
        filename = "data/snapshots/EDUC - Education/2021-04-16/EDUC 4525A - Instrumental Music Curriculum & Method A (UG) - 105768+1+4142+1.html"
        with open(filename, 'r') as f:
            e = Extractor(f.read())
            x = e.course_details_as_df()
            y = e.class_details_as_df()
            z = e.compile_df()


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
