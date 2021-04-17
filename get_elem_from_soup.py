import os
import bs4
import re
import pandas as pd

def get_table(course_soup):
    return course_soup.find("body").find("div", {"id":"hidedata04_1"})

def preprocess(table_soup):


    # For all matches of 'Note:' or 'Topic:', wrap the <td> tag it belongs to with a <tr>
    # AND only do so if it does not already belong to a <tr>
    for elem in relevant.find_all(string=re.compile(r'Note:|Topic:')):
        if (elem.parent.parent.name == 'td') and (elem.parent.parent.parent.name != 'tr'):
            elem.parent.parent.wrap(course_soup.new_tag('tr'))
