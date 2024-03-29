import bs4
import requests
import re
import datetime
import pathlib
import requests
import time
import os
import urllib.parse
from tests.scraper import validate_html

# add some sort of way to restore progress when interrupted?

class Scraper:

    def __init__(self):
        self.count = 1
        pass


    def file_with_substring_exists(self, path_str : str, substr : str):
        globbed = pathlib.Path(path_str).glob(f"*{substr}*")

        try:
            next(globbed)
            self.count += 1
            return True
        except StopIteration:
            return False


    def get(self, url : str, retry_time : int = -1, double_time : bool = False) -> str:
        """Wrapper for requests.get which requests again upon failure.

        retry_time : integer value that determines the retry time in seconds. If negative, then
                     this function will prompt the user whether to retry.

        double_time : if true and retry_time is nonnegative, doubles retry_time after each retry"""
        while True:
            try:
                res = requests.get(url, timeout=60)
                return res
            except BaseException as e:
                if retry_time < 0:
                    print('\a')
                    c = input("Requests ended with error: \"%s\". Try again [y/N]? " % str(e))
                    if c.lower() == 'y':
                        print("Continuing...")
                        continue
                    else:
                        print("Stopping...")
                        break
                else:
                    print("Requests ended with error: \"%s\". Retrying in %d seconds." % (str(e), retry_time))
                    time.sleep(retry_time)
                    if double_time:
                        retry_time *= 2
                    continue


    def scrape_url(self, url : str, dir_name : str, scrape_once : bool = True):
        """Retrieves a page from the course planner, storing it in a file under dir_name."""
        while True:
            course_id = url.split('=')[-1]

            if scrape_once and self.file_with_substring_exists(dir_name, course_id):
                print(f"({self.count}) Already scraped, skipping page with:", course_id)
                self.count += 1
                return

            course_page = self.get(url, 5, True)
            course_page_soup = bs4.BeautifulSoup(course_page.text, features="lxml")
            course_title = course_page_soup.title.text.replace('/', '-')

            print(f"({self.count}) Scraping:", course_title, "-", course_id)

            course_page_source = str(course_page_soup)

            if not validate_html(course_page_soup):
                print('\a')
                print("** Warning: data may be missing for", course_title, "with url", url)
                x = input("Repeat this scrape [Y/n]? ")
                if x.lower() == "n":
                    print("Skipping...")
                    self.count += 1
                    return
                else:
                    continue
            else:
                break

        html_file = open(dir_name + '/' + course_title + " - " + course_id + ".html", 'w')
        html_file.write(course_page_source)
        html_file.close()

        self.count += 1


    def get_course_list(self, year_to_retrieve : int = datetime.date.today().year):
        """Obtains a list of URLs pointing to the pages of every course accessible in the course planner."""
        while True:
            search_page_html = self.get('https://access.adelaide.edu.au/courses/search.asp', 5, True)
            search_page_soup = bs4.BeautifulSoup(search_page_html.text, features="lxml")

            select_dropdown = search_page_soup.find('select')
            if select_dropdown == None:
                print('\a')
                print("** Warning: missing dropdown in main course planner page.")
                x = input("Repeat this scrape [Y/n]? ")
                if x.lower() == "n":
                    print("Skipping...")
                    self.count += 1
                    return
                else:
                    continue
            else:
                break

        # get list of subject areas from dropdown box
        subject_areas = []
        for option in select_dropdown.find_all('option'):
            subject_areas.append(option.text)

        subject_areas.remove('All Subject Areas')

        # scrape course list for each subject area
        for full_subject_name in subject_areas:
            courses_to_scrape = []
            subject_dir = "data/course_lists/%s" % full_subject_name
            pathlib.Path(subject_dir).mkdir(parents=True, exist_ok=True)

            subject_area = full_subject_name.split(' -')[0]

            print("Scraping:", subject_area)

            while True:
                course_listing_link = f"https://access.adelaide.edu.au/courses/search.asp?year={year_to_retrieve}&m=r&title=&subject={urllib.parse.quote(subject_area)}&catalogue=&action=Search&term=&career=&campus=&class=&sort=" 
                course_listing_page = self.get(course_listing_link, 5, True)
                course_listing_soup = bs4.BeautifulSoup(course_listing_page.text, features="lxml")

                if not course_listing_soup.find("th", attrs={'class': ['course']}) and not course_listing_soup.find('a', href=re.compile(r'details')):
                    print('\a')
                    print(f"** Warning: missing course list details for {subject_area}.")
                    x = input("Repeat this scrape [Y/n]? ")
                    if x.lower() == "n":
                        print("Skipping...")
                        return
                    else:
                        continue
                else:
                    break

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
