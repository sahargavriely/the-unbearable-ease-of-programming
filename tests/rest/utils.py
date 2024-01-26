import mimetypes

import requests
from requests.compat import urljoin


class Session(requests.Session):

    def __init__(self, base_url='', token=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_url = base_url
        self.token = token or ''

    def _headers(self):
        return {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': mimetypes.types_map['.json'],
        }

    def delete(self, url, **json):
        return self.request('delete', url, data=json)

    def get(self, url, **params):
        return self.request('get', url, data=params)

    def patch(self, url, **json):
        return self.request('patch', url, data=json)

    def post(self, url, **json):
        return self.request('post', url, data=json)

    def put(self, url, **json):
        return self.request('put', url, data=json)

    def request(self, method=None, url=None, data=None, *args, **kwargs):
        method = method.strip().upper() if method else 'GET'
        url = urljoin(self.base_url, url)
        if method == 'GET':
            kwargs['params'] = data
        else:
            kwargs['json'] = data
        response = super().request(method, url, *args, headers=self._headers(),
                                   **kwargs)
        return response
