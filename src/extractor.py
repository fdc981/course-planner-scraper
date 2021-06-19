import pandas as pd
import bs4
import tests.expected_types as expected
import re

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
        """Checks whether the input class detail dataframe passes tests"""
        # check for foreign columns
        for col in df.columns:
            assert col in expected.class_col_types, f"Unexpected column {col}."

        for col in df.columns:
            for el in df[col]:
                assert re.match(expected.class_col_types[col], str(el)), f"Element `{el}` with type {type(el)} of column {col} did not pass regex test {expected.class_col_types[col]}."

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

        # check whether class does not have any timetabled face-to-face sessions
        no_face_to_face_tags = self.class_details.table.find_all("td", attrs={"colspan": "4"})
        if len(no_face_to_face_tags) != 0:
            print(f"** Warning: table has classes with {len(no_face_to_face_tags)} no face to face sessions")
            for tag in no_face_to_face_tags:
                tag.string = "No schedule"

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
        result_soup = bs4.BeautifulSoup(result, features="lxml")

        # collapse all group and class type data into each subtable
        group = "none" # allow group data to carry through iterations
        for table in result_soup.find_all("table"):
            tc = table.contents

            # check whether there are no rows of information in the table
            if len(tc) == 1:
                print("** Warning: table has no contents, skipping")
                continue

            # check whether class does not have any timetabled face-to-face sessions
            no_face_to_face_tag = tc[2].find("td", attrs={"colspan": "4"})
            print("no_face_to_face_tag:", no_face_to_face_tag)
            if no_face_to_face_tag:
                print("** Warning: course has no face to face sessions")
                no_face_to_face_tag.string = "No schedule"

            # find the position of the <tr class="trheader"> tag
            trheader_index = 0
            while not self.__is_class_data_header(tc[trheader_index]):
                trheader_index += 1

            if trheader_index > 2:
                raise Exception("Unexpected position for trheader: %d" % trheader_index)
            elif trheader_index < 1:
                raise Exception("Missing class type data from class details subtable.")


            extra_data = {}

            extra_data["Class Type"] = tc[trheader_index - 1].string

            if trheader_index > 1:
                group = tc[trheader_index - 2].get_text() # carries through iterations
                del tc[1]
            del tc[0]

            if len(tc) == 1:
                print("** Warning: table has no rows, skipping")
                continue

            extra_data["Group"] = group

            if not self.__is_class_data_header(tc[0]):
                raise Exception("First element is not class data header")


            extra_data["Annotation"] = []

            i = 0
            past_data_tag = None
            # go through the table and collect notes, decreasing rowspan where appropriate.
            while i != len(tc):
                if "class" in tc[i].attrs and tc[i].attrs["class"] == ["data"]:
                    past_data_tag = tc[i]
                    i += 1
                elif re.search(r"Note|Topic|Warning", tc[i].get_text()):
                    extra_data["Annotation"].append(tc[i].get_text())
                    for tag in past_data_tag.find_all("td"):
                        if "rowspan" in tag.attrs:
                            tag.attrs["rowspan"] = int(tag.attrs["rowspan"]) - 1

                    del tc[i]
                else:
                    i += 1

            extra_data["Annotation"] = str(extra_data["Annotation"])

            # Currently: this rowspan is not accurate. Sometimes the tables can span many, many rows, and some cells may have rowspan < true number of rows in table.
            rowspan = len(tc) - 1

            # append all the extra data as additional columns
            for name in extra_data:
                header_tag = result_soup.new_tag("th")
                header_tag.string = name
                tc[0].append(header_tag)

                container_tag = result_soup.new_tag("td")
                container_tag.attrs = {"class" : "odd", "rowspan" : rowspan}
                container_tag.string = extra_data[name]
                tc[1].append(container_tag)

        dfs = pd.read_html(str(result_soup))

        # post-processing and sanitisation
        for df in dfs:
            # change all entries in the "Available" column with value "FULL" to the maximum capacity of the class
            df.loc[df["Available"] == "FULL", "Available"] = df.loc[df["Available"] == "FULL", "Size"]
            df["Available"] = df["Available"].astype(int)
            df["Location"] = df["Location"].astype(str)

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
