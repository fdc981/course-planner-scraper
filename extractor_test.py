import unittest
from extract_from_html import Extractor

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

if __name__ == "__main__":
    unittest.main()
