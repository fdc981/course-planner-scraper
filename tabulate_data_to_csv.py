# Based on checkpoint Wed Nov 20
# Input: html files
# Output: csv file containing compiled data.

import os
import bs4
import re
import pandas as pd

def fix_html():
    # For all matches of 'Note: ' or 'Topic: ', wrap the 'td' tag it belongs with a 'tr'
    # AND only do so if it does not already belong to a <tr>
    for elem in relevant.find_all(string=re.compile(r'Note:|Topic:')):
        if (elem.parent.parent.name == 'td') and (elem.parent.parent.parent.name != 'tr'):
            elem.parent.parent.wrap(course_soup.new_tag('tr'))

    # For the time being the data on groups is omitted by removing all <tr> with class 'trgroup'.
    for trgroup in relevant.find_all("tr", attrs={"class":"trgroup"}):
        print(trgroup.extract())
            
    # Remove warnings and errors
    warnings = relevant.find_all("b", text=re.compile('Warning:'))
    errors = relevant.find_all("b", text=re.compile('Errors:'))
    
    for elem in warnings:
        print("Warning found.")
        print(elem.parent.parent.extract())
        
    for elem in errors:
        print("Error found.")
        print(elem.parent.parent.extract())
        
    dfs = pd.read_html(str(relevant.table))

course_html_files = os.listdir('snapshots')
csv_output = open('compiled_data.csv', 'w')

for course_num in range(len(course_html_files)):
    print(course_num)
    f = open('snapshots/' + course_html_files[course_num], 'r')
    course_soup = bs4.BeautifulSoup(f.read())
    relevant = course_soup.find('div', attrs={'class': 'content'}).find("div", {"id":"hidedata04_1"})
    
    # If there are class details, create the dataframe.
    if relevant is not None:

        # Flatten table.

        # Get the required data via the first MultiIndex and typecast all data into str type.
        df = dfs[0].astype(str)

        # Remove irrelevant indices from the MultiIndex of df by selecting the indicies of level 2.
        df.columns = df.columns.get_level_values(1)
        
        # Delete irrelevant columns.

        for col in df.columns:
            if col not in ['Class Nbr', 'Section', 'Size', 'Available', 'Dates', 'Days', 'Time', 'Location']:
                del df[col]

        df['Enrolment Class'] = 'other'

        # loop breaking at `Related:` but what if there is no `Related:` and instead another section?
        for i in range(len(df)):
            if 'Related' in df.iloc[i].Location:
                break
            else:
                df.loc[i, 'Enrolment Class'] = 'enrolment'

        # Filtering of useless data.

        # Filter all rows with "Related Class: ... " and rows which contain column names, via the Location column.
        df = df[~df.Location.str.contains('Related|Location|Note|Enrolment Class|Topic:')]

        # Filter all rows with 'Automatic Enrolment Class: ...' via the Class Nbr column.
        df = df[~df['Class Nbr'].str.contains('Auto')]

        # Using to_numeric, convert the 'available' column to a numeric type, and for theur non-numeric entries convert to NaN.
        df['Available'] = pd.to_numeric(df['Available'], errors = 'coerce').fillna(0).astype(int)
        df['Size'] = pd.to_numeric(df['Size'], errors = 'coerce').fillna(0).astype(int)

        df['Filled Spots'] = df['Size'] - df['Available']

        # Prettified text requires more processing.
        course_term = course_soup.find('th', text=re.compile(r'Term')).parent.td.text.strip()
        df['Term'] = course_term

        course_units = course_soup.find('a', href="help.asp?topic=units").parent.parent.td.text.strip()
        df['Units'] = course_units

        course_subject_area = course_soup.title.text.strip().split(' -')[0].split(' ')[:-1]
        df['Subject Area'] = ' '.join(course_subject_area)

        course_cat_number = course_soup.title.text.strip().split(' -')[0].split(' ')[-1]
        df['Catalogue Number'] = course_cat_number

        course_title = course_soup.title.text.strip().split('- ')[-1]
        df['Course Title'] = course_title

        course_campus = course_soup.find('th', text=re.compile(r'Campus')).parent.td.text.strip()
        df['Campus'] = course_campus

        course_career = course_soup.find('a', href='help.asp?topic=career').parent.parent.td.text.strip()
        df['Career'] = course_career
        
        course_id = course_html_files[course_num].split(' - ')[-1].split('.')[0]
        df['Course ID'] = course_id

        if course_num == 0:
            df.to_csv(csv_output, header=True)
        else:
            df.to_csv(csv_output, header=False)

    else:
        df = pd.DataFrame(index = [0], 
                          columns = ['Class Nbr', 'Section', 
                                     'Size', 'Available', 
                                     'Dates', 'Days', 
                                     'Time', 'Location', 
                                     'Enrolment Class', 'Filled Spots',
                                     'Term', 'Units',
                                     'Subject Area', 'Catalogue Number',
                                     'Course Title', 'Campus',
                                     'Career'])
        df = df.fillna('na')

        # Prettified text requires more processing.
        course_term = course_soup.find('th', text=re.compile(r'Term')).parent.td.text.strip()
        df['Term'] = course_term

        course_units = course_soup.find('a', href="help.asp?topic=units").parent.parent.td.text.strip()
        df['Units'] = course_units

        course_subject_area = course_soup.title.text.strip().split(' -')[0].split(' ')[:-1]
        df['Subject Area'] = ' '.join(course_subject_area)

        course_cat_number = course_soup.title.text.strip().split(' -')[0].split(' ')[-1]
        df['Catalogue Number'] = course_cat_number

        course_title = course_soup.title.text.strip().split('- ')[-1]
        df['Course Title'] = course_title

        course_campus = course_soup.find('th', text=re.compile(r'Campus')).parent.td.text.strip()
        df['Campus'] = course_campus

        course_career = course_soup.find('a', href='help.asp?topic=career').parent.parent.td.text.strip()
        df['Career'] = course_career
        
        course_id = course_html_files[course_num].split(' - ')[-1].split('.')[0]
        df['Course ID'] = course_id
        
        if course_num == 0:
            df.to_csv(csv_output, header=True)
        else:
            df.to_csv(csv_output, header=False)
    
f.close()
csv_output.close()
