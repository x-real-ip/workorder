import requests
import time
import sys


def connection_check_url(url, retry_sec):
    """Check connection"""
    attempts = 0
    while attempts < 3:
        try:
            requests.get(url, timeout=5)
            print(f"Connected to {url}")
            break
        except (requests.ConnectionError, requests.Timeout) as exception:
            print(
                f"Can't connect to {url}, try again in {retry_sec} seconds...")
            attempts += 1
            time.sleep(retry_sec)
            if attempts == 3:
                print(f"Can't connect to {url}, script stopped")
                sys.exit()
