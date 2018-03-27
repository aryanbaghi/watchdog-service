import requests
from dbwrapper.base import Status 
from .base import BasePlugin
from .exceptions import InvalidMethod


class Method:
    GET = 'get'
    POST = 'post'
    DELETE = 'delete'
    PUT = 'put'

    method_map = {
        GET: requests.get,
        POST: requests.post,
        DELETE: requests.delete,
        PUT: requests.put,
    }

class HTTP(BasePlugin):
    def __init__(self, service_id,
                url, expected_code,
                method, payload=None,
                headers=None):
        try:
            Method.method_map[method]
        except KeyError:
            raise InvalidMethod

        self.url = url
        self.expected_code = expected_code
        self.method = method
        self.payload = payload
        self.headers = headers

        super(HTTP, self).__init__(service_id)

    def run(self):

        payload = self.payload
        headers = self.headers
        if callable(self.payload):
            payload = self.payload()
        if callable(self.headers):
            headers = self.headers()

        try:
            response = Method.method_map[self.method](
                self.url,
                data=payload,
                headers=headers,
            )

            if response.status_code == self.expected_code:
                return Status.UP
        except:
            return Status.DOWN

