import bs4
import requests
import re
import datetime
import pathlib
from src.requests_wrapper import get
import os
from src.verify import validate_html


class Scraper:
    def __init__(self):
        pass

    def scrape_url(self, url : str, dir_name : str):
        """Retrieves a page from the course planner, storing it in a file under data/."""
        while True:
            course_page = get(url, 5, True)
            course_page_soup = bs4.BeautifulSoup(course_page.text, features="lxml")
            course_id = url.split('=')[-1]
            course_title = course_page_soup.title.text.replace('/', '-')

            print("Scraping:", course_title, "-", course_id)

            course_page_source = str(course_page_soup)

            if not validate_html(course_page_soup):
                print("** Warning: data may be missing for", course_title, "with url", url)
                x = input("Repeat this scrape [Y/n]? ")
                if x.lower() == "n":
                    break
            else:
                break

        html_file = open(dir_name + '/' + course_title + " - " + course_id + ".html", 'w')
        html_file.write(course_page_source)
        html_file.close()

    def get_course_list(self, year_to_retrieve : int = datetime.date.today().year):
        """Obtains a list of URLs pointing to the pages of every course accessible in the course planner."""
        search_page_html = get('https://access.adelaide.edu.au/courses/search.asp', 5, True)
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

            course_listing_link = "https://access.adelaide.edu.au/courses/search.asp?year=%s&m=r&title=&subject=%s&catalogue=&action=Search&term=&career=&campus=&class=&sort=" % (str(year_to_retrieve), subject_area)
            course_listing_page = get(course_listing_link, 5, True)
            course_listing_soup = bs4.BeautifulSoup(course_listing_page.text, features="lxml")

            for link in course_listing_soup.find_all('a', href=re.compile(r'details')):
                courses_to_scrape.append('https://access.adelaide.edu.au/courses/' + link.attrs['href'])

            course_list_txt = '\n'.join(courses_to_scrape)
            f = open("%s/course_list_%s.txt" % (subject_dir, str(datetime.date.today())), 'w')
            f.write(course_list_txt)
            f.close()

    def get_courses_html(self):
        """Scrapes all webpages in the url provided by the list of course planner URLs."""
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
                self.scrape_url(course_url, snapshot_path)
