import unittest
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
        # note: also contains "Days" entries with multiple days listed (instead of having just one)
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

    def test_page_with_multiple_annotations_within_table_rows(self):
        # note: column 'Location' contains empty data
        filename = "data/snapshots/ANIML SC - Animal Science/2021-05-15/ANIML SC 1015RW - Animal Handling & Husbandry I - 104099+1+4110+1.html"
        with open(filename, 'r') as f:
            e = Extractor(f.read())
            x = e.course_details_as_df()
            y = e.class_details_as_df()
            z = e.compile_df()

    def test_page_with_topic_annotation(self):
        filename = "data/snapshots/APP MTH - Applied Mathematics/2021-05-15/APP MTH 7048 - Applied Mathematics Topic A - 008510+1+4110+1.html"
        with open(filename, 'r') as f:
            e = Extractor(f.read())
            x = e.course_details_as_df()
            y = e.class_details_as_df()
            z = e.compile_df()

    def test_page_with_no_timetabled_face_to_face_sections(self):
        filename = "data/snapshots/PPE - Philosophy, Politics & Econ/2021-06-03/PPE 2002 - Foundations of Public Policy - 110079+1+4110+1.html"
        with open(filename, 'r') as f:
            e = Extractor(f.read())
            x = e.course_details_as_df()
            y = e.class_details_as_df()
            z = e.compile_df()

    def test_page_with_no_timetabled_face_to_face_sessions_in_middle_of_table(self):
        filename = "data/snapshots/FREN - French/2021-06-01/FREN 1003 - French IB: Beginners' French - 001962+1+4120+1.html"
        with open(filename, 'r') as f:
            e = Extractor(f.read())
            x = e.course_details_as_df()
            y = e.class_details_as_df()
            z = e.compile_df()

    def test_page_with_no_day_time_location_data(self):
        filename = "data/snapshots/COMMGMT - Management/2021-06-21/COMMGMT 7030A - Cyber Security Industry Project (Management) Part A - 110771+1+4120+FM1.html"
        with open(filename, 'r') as f:
            e = Extractor(f.read())
            x = e.course_details_as_df()
            y = e.class_details_as_df()
            z = e.compile_df()


if __name__ == "__main__":
    unittest.main()
