# Wrapper for requests.

import requests

def get(url):
    while True:
        try:
            res = requests.get(url)
            return res
        except BaseException as e:
            c = input("Requests ended with error: \"%s\". Try again [y/N]? " % str(e))
            if c.lower() == 'y':
                continue
