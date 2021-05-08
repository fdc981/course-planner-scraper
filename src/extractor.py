# Functions that

import pandas as pd
import bs4
import tests.expected_types as expected

class Extractor:
    """Extracts data from a course planner HTML file."""

    def __init__(self, html_str : str):
        self.soup = bs4.BeautifulSoup(html_str, features="lxml")
        self.course_details = self.soup.find("div", {"id": "hidedata01_1"})
        self.class_details = self.soup.find("div", {"id": "hidedata04_1"})

    def __is_group_header(self, elem_soup):
        """Determines the given element is a group header for the corresponding class details table"""
        attrs = elem_soup.attrs
        return "class" in attrs and attrs["class"] == ["trgroup"]

    def __is_class_type_header(self, elem_soup):
        """Determines the given element is a header indicating class type for the corresponding class details table"""
        return elem_soup.find("th", {"class" : "course", "colspan" : 8})

    def __is_start_of_class_subtable(self, elem_soup):
        """Determines whether an element is part of a subclass"""
        return self.__is_group_header(elem_soup) or self.__is_class_type_header(elem_soup)

    def __is_class_data_header(self, elem_soup):
        """Determines the given element is a header containing the column names of the table"""
        attrs = elem_soup.attrs
        return "class" in attrs and attrs["class"] == ["trheader"]

    def __sanitise(self, df : pd.DataFrame) -> None:
        """Checks whether the input dataframe passes tests"""
        # check for foreign columns
        for col in df.columns:
            if col not in expected.class_col_types:
                raise Exception(f"Unexpected column {col}.")

    def course_details_as_df(self) -> pd.DataFrame:
        """Return the course details table as a dataframe."""
        dfs = pd.read_html(str(self.course_details), index_col = 0)

        assert len(dfs) == 1, "Unexpected size of table while parsing: len(dfs) == %d != 1" % len(dfs)

        df = dfs[0]
        df.index = [ind.replace(':', '') for ind in df.index]

        return df.transpose()

    def class_details_as_df(self) -> pd.DataFrame:
        """Return the class details tables as a single dataframe."""
        # check whether there are no class details
        if self.class_details == None:
            return pd.DataFrame()

        # wrap all immediate <td>s in the <table> with <tr>
        tds = self.class_details.table.find_all("td", recursive=False)
        for td in tds:
            wrapper = self.soup.new_tag("tr")
            wrapper.attrs = {"class" : "note"}
            td.wrap(wrapper)

        # Split the html up.

        # ensure no `NavigableString`s are present
        table_soup = self.class_details.table.find_all("tr", recursive=False)
        table_str = [str(el) for el in table_soup]

        if len(table_soup) < 3:
            print(table_soup)
            print("** Warning: no contents in class details table")
            return pd.DataFrame()

        i = 0
        start = 0
        result = ""
        while i < len(table_soup):
            while start != len(table_soup) and not self.__is_start_of_class_subtable(table_soup[start]):
                start += 1

            # skips either <tr class="trheader"> or <tr class="data">
            i = start + 2

            while i < len(table_soup) and not self.__is_start_of_class_subtable(table_soup[i]):
                i += 1

            result += "<table>" + ''.join(table_str[start:i]) + "</table>"
            start = i

        self.result = result

        # collapse all group and class type data into each subtable
        result_soup = bs4.BeautifulSoup(result, features="lxml")
        group = "" # allow group data to carry through iterations
        for table in result_soup.find_all("table"):
            tc = table.contents

            # find the position of the <tr class="trheader"> tag
            trheader_index = 0
            while not self.__is_class_data_header(tc[trheader_index]):
                trheader_index += 1

            if trheader_index > 2:
                raise Exception("Unexpected position for trheader: %d" % trheader_index)
            elif trheader_index < 1:
                raise Exception("Missing class type data from class details subtable.")

            class_type = tc[trheader_index - 1].string

            if trheader_index > 1:
                group = tc[trheader_index - 2].get_text()
                del tc[1]

            del tc[0]

            if not self.__is_class_data_header(tc[0]):
                raise Exception("First element is not class data header")

            if tc[-1].get_text().find("Note:") != -1:
                note = tc[-1].get_text()
                del tc[-1]
            else:
                note = ""

            # append extra headers to trheader
            class_type_header = result_soup.new_tag("th")
            class_type_header.string = "Class Type"

            group_header = result_soup.new_tag("th")
            group_header.string = "Group"

            note_header = result_soup.new_tag("th")
            note_header.string = "Note"

            tc[0].append(class_type_header)
            tc[0].append(group_header)
            tc[0].append(note_header)

            # check whether there are no rows of information in the table
            if len(tc) == 1:
                print("** Warning: table has no contents, skipping")
                break;

            rowspan_tag = tc[1].find("td", {"rowspan" : True})
            if rowspan_tag == None:
                print("** Warning: unable to find tag containg rowspan, setting rowspan = 1")
                rowspan = 1
            else:
                rowspan = int(rowspan_tag.attrs["rowspan"])

            # if note exists
            if note != "":
                # exclude an extra row
                for el in tc[1].find_all("td", {"rowspan" : rowspan}):
                    el["rowspan"] = int(el["rowspan"]) - 1
                rowspan -= 1

            # insert extra data into <tr class="data">
            class_type_tag = result_soup.new_tag("td")
            class_type_tag.attrs = {"class" : "odd", "rowspan" : rowspan}
            class_type_tag.string = class_type

            group_tag = result_soup.new_tag("td")
            group_tag.attrs = {"class" : "odd", "rowspan" : rowspan}
            group_tag.string = group

            note_tag = result_soup.new_tag("td")
            note_tag.attrs = {"class" : "odd", "rowspan" : rowspan}
            note_tag.string = note

            tc[1].append(class_type_tag)
            tc[1].append(group_tag)
            tc[1].append(note_tag)

        dfs = pd.read_html(str(result_soup))

        for df in dfs:
            self.__sanitise(df)

        # merge all data into one dataframe
        df = pd.concat(dfs)

        # insert additional data from course title
        full_course_title = self.soup.title.string.strip().split(' - ')
        df["Subject Area"] = ' '.join(full_course_title[0].split(' ')[:-1])
        df["Catalogue Number"] = full_course_title[0].split(' ')[-1]
        df["Course Title"] = full_course_title[-1]

        return df

    def compile_df(self) -> pd.DataFrame:
        """Returns a list of two dataframes, the first containing the course details and the second containing the class details.
        In addition, the course ID is supplied for both dataframes as an identifying attribute between courses."""
        # join course and class details sideways
        course_df = self.course_details_as_df()
        class_df = self.class_details_as_df()

        # obtain course id
        tag = self.soup.find("a", string="Add this course to your cart")
        href = tag.attrs["href"]
        start_ind = href.find("add=") + 4
        end_ind = href.find("&", start_ind)
        course_id = href[start_ind:end_ind]

        course_df["Course ID"] = course_id
        class_df["Course ID"] = course_id

        return [course_df, class_df]
