# Wrapper for requests.

import requests
import time

def get(url : str, retry_time : int = -1, double_time : bool = False) -> str:
    """Wrapper for requests.get which requests again upon failure.

    retry_time : integer value that determines the retry time in seconds. If negative, then
                 this function will prompt the user whether to retry.

    double_time : if true and retry_time is nonnegative, doubles retry_time after each retry"""
    while True:
        try:
            res = requests.get(url)
            return res
        except BaseException as e:
            if retry_time < 0:
                c = input("Requests ended with error: \"%s\". Try again [y/N]? " % str(e))
                if c.lower() == 'y':
                    print("Continuing...")
                    continue
                else:
                    print("Stopping...")
                    break
            else:
                print("Requests ended with error: \"%s\". Retrying in %d seconds." % (str(e), retry_time))
                time.sleep(retry_time)
                if double_time:
                    retry_time *= 2
                continue
