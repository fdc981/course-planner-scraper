# Functions that

import pandas as pd
import bs4

class Extractor:
    """Extracts data from a course planner HTML file."""

    def __init__(self, html_str : str):
        self.soup = bs4.BeautifulSoup(html_str, features="lxml")
        self.course_details = self.soup.find("div", {"id": "hidedata01_1"})
        self.class_details = self.soup.find("div", {"id": "hidedata04_1"})

    def course_details_as_df(self) -> pd.DataFrame:
        """Return the course details table as a dataframe."""
        dfs = pd.read_html(str(self.course_details), index_col = 0)

        assert len(dfs) == 1, "Unexpected size of table while parsing: len(dfs) == %d != 1" % len(dfs)

        df = dfs[0]
        df.index = [ind.replace(':', '') for ind in df.index]

        return df.transpose()

    def class_details_as_df(self) -> pd.DataFrame:
        """Return the class details tables as a single dataframe."""
        if len(self.class_details) == 0:
            return pd.DataFrame()

        # wrap all immediate <td>s in the <table> with <tr>
        tds = self.class_details.table.find_all("td", recursive=False)
        for td in tds:
            td.wrap(self.soup.new_tag("tr"))

        # Split the html up, wrapping all tds with tr

        table_soup = self.class_details.table.find_all("tr", recursive=False)
        table_str = [str(el) for el in table_soup]

        start = 0
        result = ""
        for i, tr in enumerate(table_soup):
            if i != 0 and len(tr.find_all("th")) == 1:
                result += "<table>" + '\n'.join(table_str[start:i]) + "</table>"
                start = i

        result += "<table>" + '\n'.join(table_str[start:len(table_str)]) + "</table>"

        self.result = result

        dfs = pd.read_html(result)

        # flatten columns, ensuring to store class type information
        for df in dfs:
            class_type = df.columns[0][0]
            df.columns = df.columns.get_level_values(1)
            df.columns.append(pd.Index(["Class Type:"]))
            df["Class Type"] = class_type

        # merge all data into one dataframe
        return pd.concat(dfs)

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

        course_df.columns.append(pd.Index(["Course ID"]))
        class_df.columns.append(pd.Index(["Course ID"]))

        course_df["Course ID"] = course_id
        class_df["Course ID"] = course_id

        return [course_df, class_df]
