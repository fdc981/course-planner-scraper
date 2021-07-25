import unittest
import bs4
import datetime
from pathlib import Path
from tests.scraper import validate_html

class TestSnapshotDataValidity(unittest.TestCase):
    def test_all_pages_are_valid(self):
        p = Path("data/snapshots")
        page_paths = p.glob("*/%s/*.html" % str(datetime.date.today()))
        for page_path in page_paths:
            with open(str(page_path)) as page:
                soup = bs4.BeautifulSoup(page.read(), features="lxml")
                self.assertTrue(validate_html(soup), "Invalid html for: %s" % page_path)


if __name__ == "__main__":
    unittest.main()
