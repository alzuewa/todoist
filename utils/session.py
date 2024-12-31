from typing import Optional

import requests
from requests import Session
from requests.auth import AuthBase

from utils.logger import logger


class BearerAuth(AuthBase):

    def __init__(self, token):
        self.token = token

    def __call__(self, request):
        request.headers["Authorization"] = f"Bearer {self.token}"
        return request


class ApiSession(Session):

    def __init__(self, base_url, auth: Optional[BearerAuth] = None):
        super().__init__()
        self.base_url = base_url
        if auth:
            self.auth = auth
        self.headers = {'Content-Type': 'application/json'}

    @logger
    def request(self, endpoint_path: str, method: str, **kwargs) -> requests.Response:
        url = f'{self.base_url}{endpoint_path}'
        if self.auth:
            return super().request(url=url, method=method, auth=self.auth, headers=self.headers, **kwargs)
        else:
            return super().request(url=url, method=method, headers=self.headers, **kwargs)

    def get(self, endpoint_path: str, **kwargs) -> requests.Response:
        return self.request(endpoint_path, method='GET', **kwargs)

    def post(self, endpoint_path: str, **kwargs) -> requests.Response:
        return self.request(endpoint_path, method='POST', **kwargs)

    def put(self, endpoint_path: str, **kwargs) -> requests.Response:
        return self.request(endpoint_path, method='PUT', **kwargs)

    def patch(self, endpoint_path: str, **kwargs) -> requests.Response:
        return self.request(endpoint_path, method='PATCH', **kwargs)

    def delete(self, endpoint_path: str, **kwargs) -> requests.Response:
        return self.request(endpoint_path, method='DELETE', **kwargs)
