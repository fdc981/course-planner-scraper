course-planner-scraper
----------------------

# Dependencies

This program requires a few dependencies as outlined in `requirements.txt`. To install them use

```sh
pip install -r requirements.txt
```

within a [venv](https://docs.python.org/3/library/venv.html) if possible.

# Usage

Scrape and process data:

```sh
python main.py
```

Running tests:

```sh
python -m tests.name_of_test_suite
```

Compile the report for current date (requires `R` and the `rmarkdown` package to be installed):

``` bash
cd results/
R --vanilla <<< "rmarkdown::render('report.rmd')"
```
