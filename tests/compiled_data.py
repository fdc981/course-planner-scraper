import unittest
import pandas as pd
from pathlib import Path
from src.extractor import Extractor
import re
import tests.expected_types as expected

class TestCourseDataIntegrity(unittest.TestCase):
    def test_existence_of_required_columns(self):
        course_details_path = Path("data/compiled_data/course_details/")
        for filename in course_details_path.iterdir():
            df = pd.read_csv(str(filename), dtype=str)
            for col in df.columns:
                assert col in expected.course_col_types, f"Unexpected column {col}."

    def test_data_consistency(self):
        course_details_path = Path("data/compiled_data/course_details/")
        for filename in course_details_path.iterdir():
            df = pd.read_csv(str(filename), dtype=str)
            for col in df.columns:
                for el in df[col]:
                    assert re.match(expected.course_col_types[col], str(el)), f"Element `{el}` with type {type(el)} of column {col} did not pass regex test {expected.course_col_types[col]}."

    def test_no_unexpected_na(self):
        course_details_path = Path("data/compiled_data/course_details/")
        for filename in course_details_path.iterdir():
            df = pd.read_csv(str(filename), dtype=str)
            if df.isna().any(axis=None):
                print(df[df.isna().any(axis=1)])
                raise Exception("NaN values present in DataFrame (see above output)")


class TestClassDataIntegrity(unittest.TestCase):
    def test_existence_of_required_columns(self):
        class_details_path = Path("data/compiled_data/class_details/")
        for filename in class_details_path.iterdir():
            df = pd.read_csv(str(filename), dtype=str)
            for col in df.columns:
                assert col in expected.class_col_types, f"Unexpected column {col}."

    def test_data_consistency(self):
        class_details_path = Path("data/compiled_data/class_details/")
        for filename in class_details_path.iterdir():
            df = pd.read_csv(str(filename), dtype=str)
            for col in df.columns:
                for el in df[col]:
                    assert re.match(expected.class_col_types[col], str(el)), f"Element `{el}` with type {type(el)} of column {col} did not pass regex test {expected.class_col_types[col]}."

    def test_no_unexpected_na(self):
        class_details_path = Path("data/compiled_data/class_details/")
        for filename in class_details_path.iterdir():
            df = pd.read_csv(str(filename), dtype=str)
            if df.isna().any(axis=None):
                print(df[df.isna().any(axis=1)])
                raise Exception("NaN values present in DataFrame (see above output)")


if __name__ == "__main__":
    unittest.main()
