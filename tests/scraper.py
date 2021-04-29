import os
import bs4
import re
import pandas as pd

def validate_html(soup) -> bool:
    """Checks that all required data is within the given soup of the course planner page.
    Outputs warning messages."""
    test_passed = True

    course_details_table = soup.find("div", {"id" : "hidedata01_1"})

    if course_details_table == None:
        test_passed = False
        print("** Warning: missing course details table")
    elif len(course_details_table.find_all("tr")) < 11:
        #test_passed = False
        print("** Warning: missing data in course details table")

    class_details_table = soup.find("div", {"id" : "hidedata04_1"})

    if class_details_table == None:
        print("** Note: no class details table found, checking if no classes available.")
        test_passed = False
        for elem in soup(text=re.compile(r'No classes available')):
            test_passed=True

        if not test_passed:
            print("** Warning: missing class details")

    footer = soup.find("div", {"id" : "footer"})

    # if footer does not exist, response did not contain entire page
    if footer == None:
        test_passed = False
        print("** Warning: missing footer")

    return test_passed
