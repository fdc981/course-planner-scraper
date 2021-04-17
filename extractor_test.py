import unittest
from extract_from_html import Extractor

f = open("/home/neb/Documents/projects/course-planner-scraper/data/snapshots/AGRIC - Agriculture & Natural Resource/2021-04-13/AGRIC 1520WT - Agricultural Production I - 105341+1+4120+1.html", 'r').read()
e = Extractor(f)
x = e.course_details_as_df()
y = e.class_details_as_df()
z = e.compile_df()
