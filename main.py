from src.scraper import Scraper

s = Scraper()

print("Retrieving course list...")
s.get_course_list()

print("Retrieving course pages...")
s.get_courses_html()
