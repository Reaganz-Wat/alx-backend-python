import time

import requests

def timit(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        results = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time}s to complete")
        return results
    return wrapper

@timit
def getSomethingFromNet(url):
    response = requests.get(url)
    return response.json()

for x in getSomethingFromNet("https://api.escuelajs.co/api/v1/products"):
    print(x)