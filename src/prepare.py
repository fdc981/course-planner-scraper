import pandas as pd
import datetime
import pathlib
from src.extractor import Extractor

def compile_data(date : str = str(datetime.date.today())):
    """Compile all html data under data/snapshots/*/ to two separate csv files."""
    course_df = pd.DataFrame()
    class_df = pd.DataFrame()

    root = pathlib.Path('.')
    paths = root.glob("data/snapshots/*/%s/" % date)

    htmls = []
    for path in paths:
        for html_path in path.iterdir():
            print("compiling data for:", str(html_path))
            # read html_path
            f = open(str(html_path), 'r')
            subject_area = '/'.split(str(html_path.parent))[-1]

            # extract data
            ex = Extractor(f.read())
            f.close()
            course_details, class_details = ex.compile_df()

            # append to table if not empty
            if not course_details.empty: course_df = course_df.append(course_details)
            if not class_details.empty: class_df = class_df.append(class_details)

    pathlib.Path("data/compiled_data/course_details/").mkdir(parents=True, exist_ok=True)
    pathlib.Path("data/compiled_data/class_details/").mkdir(parents=True, exist_ok=True)

    course_df.to_csv("data/compiled_data/course_details/%s.csv" % date, index=False, na_rep="none")
    class_df.to_csv("data/compiled_data/class_details/%s.csv" % date, index=False)
