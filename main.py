from src.scraper import Scraper
from src.prepare import compile_to_csv

s = Scraper()

print("Retrieving course list...")
s.get_course_list()

print("Retrieving course pages...")
s.get_courses_html()

print("Compiling data...")
compile_to_csv()
