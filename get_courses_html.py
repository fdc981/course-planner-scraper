# Scrapes all webpages in the url provided by the list of course planner URLs,

import requests
import bs4
import os
import datetime
import pathlib
from verify import validate_html
from requests_wrapper import get

def scrape_url(url : str, dir_name : str):
    course_page = get(url)
    course_page_soup = bs4.BeautifulSoup(course_page.text, features="lxml")
    course_id = url.split('=')[-1]
    course_title = course_page_soup.title.text.replace('/', '-')

    print("Scraping:", course_title, "-", course_id)

    course_page_source = str(course_page_soup)

    if not validate_html(course_page_soup):
        print("** Warning: data may be missing for", course_title, "with url", url)
        x = input("Repeat this scrape [Y/n]? ")
        if x.lower() != "n":
            scrape_url(url, dir_name)

    html_file = open(dir_name + '/' + course_title + " - " + course_id + ".html", 'w')
    html_file.write(course_page_source)
    html_file.close()


course_lists = os.listdir("data/course_lists")

for course_list_path in course_lists:
    # create directory
    file_path = "data/course_lists/%s/course_list_%s.txt" % (course_list_path, str(datetime.date.today()))

    full_subject_area = course_list_path.split('/')[-1]
    snapshot_path = "data/snapshots/%s/%s" % (full_subject_area, str(datetime.date.today()))
    pathlib.Path(snapshot_path).mkdir(parents=True, exist_ok=True)

    # check if course list is empty
    if os.stat(file_path).st_size == 0:
        print("Skipping empty course list for subject %s." % course_list_path)
        continue

    print("Scraping URLs for:", full_subject_area)

    course_list_file = open(file_path, 'r')
    course_list = course_list_file.read().split('\n')
    course_list_file.close()

    print("Number of courses in %s:" % course_list_path, len(course_list))

    for course_url in course_list:
        scrape_url(course_url, snapshot_path)
