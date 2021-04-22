import unittest
import bs4
import datetime
from pathlib import Path
from src.verify import validate_html

class TestSnapshotDataValidity(unittest.TestCase):
    def test_specific_invalid_pages(self):
        filename = "data/snapshots/MATHS - Mathematical Sciences/2021-04-22/500 - Internal server error. - 110010+1+4120+1.html"
        with open(filename) as page:
            soup = bs4.beautifulSoup(page.read(), features="lxml")
            self.assertFalse(validate_html(soup))

    def test_all_pages_are_valid(self):
        p = Path("data/snapshots")
        page_paths = p.glob("*/%s/*.html" % str(datetime.date.today()))
        for page_path in page_paths:
            with open(str(page_path)) as page:
                soup = bs4.BeautifulSoup(page.read(), features="lxml")
                self.assertTrue(validate_html(soup), "Invalid html for: %s" % page_path)


if __name__ == "__main__":
    unittest.main()
