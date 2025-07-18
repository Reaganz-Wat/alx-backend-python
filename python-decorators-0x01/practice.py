import time

cache = {}

def memoize(func):
    def wrapper(*args, **kwargs):
        key = (args, tuple(sorted(kwargs)))
        if key in cache:
            print("Picking from cache...")
            return cache[key]
        else:
            print("Making a new network request...")
            results = func(*args, **kwargs)
            cache[key] = results
        return results
    return wrapper

@memoize
def get_user_by_id(user_id):
    return {"ID" :user_id, "School": "ABC University"}

if __name__ == "__main__":
    print(get_user_by_id(2))