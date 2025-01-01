import time
from functools import wraps

import requests


def retry_request(retry_count: int = 5, delay: int = 3):
    def request_decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            last_response = None
            for _ in range(retry_count):
                try:
                    response = func(*args, **kwargs)
                    if response.status_code in (502, 503):
                        last_response = response
                        time.sleep(delay)
                        continue
                    else:
                        return response

                except requests.exceptions.ConnectionError:
                    pass
            return last_response

        return wrapper

    return request_decorator
