course-planner-scraper
----------------------

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
R --vanilla <<< "rmarkdown::render('report.rmd')
```
