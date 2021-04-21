# Obtains a list of URLs pointing to the pages of every course accessible in the course planner.

import bs4
import requests
import re
import datetime
import pathlib
from requests_wrapper import get

year_to_retrieve = '2021'


search_page_html = get('https://access.adelaide.edu.au/courses/search.asp')
search_page_soup = bs4.BeautifulSoup(search_page_html.text, features="lxml")

# get list of subject areas from dropdown box
subject_areas = []
for option in search_page_soup.find('select').find_all('option'):
    subject_areas.append(option.text)

subject_areas.remove('All Subject Areas')

# scrape course list for each subject area
for full_subject_name in subject_areas:
    courses_to_scrape = []
    subject_dir = "data/course_lists/%s" % full_subject_name
    pathlib.Path(subject_dir).mkdir(parents=True, exist_ok=True)

    subject_area = full_subject_name.split(' -')[0]

    print("Scraping:", subject_area)

    course_listing_link = 'https://access.adelaide.edu.au/courses/search.asp?year=' + year_to_retrieve + '&m=r&title=&subject=' + subject_area + '&catalogue=&action=Search&term=&career=&campus=&class=&sort='
    course_listing_page = get(course_listing_link)
    course_listing_soup = bs4.BeautifulSoup(course_listing_page.text, features="lxml")

    for link in course_listing_soup.find_all('a', href=re.compile(r'details')):
        courses_to_scrape.append('https://access.adelaide.edu.au/courses/' + link.attrs['href'])

    course_list_txt = '\n'.join(courses_to_scrape)
    f = open("%s/course_list_%s.txt" % (subject_dir, str(datetime.date.today())), 'w')
    f.write(course_list_txt)
    f.close()
