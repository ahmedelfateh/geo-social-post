import time


def retry(func):
    def retried_func(*args, **kwargs):
        MAX_TRIES = 3
        tries = 0
        while True:
            resp = func(*args, **kwargs)
            if resp.status_code != 200 and tries < MAX_TRIES:
                print("here")
                tries += 1
                time.sleep(5)
                continue
            break
        return resp

    return retried_func
