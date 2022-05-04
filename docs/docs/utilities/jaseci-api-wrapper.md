---
sidebar_position: 1
---

# Jaseci API Wrapper

Jaseci utilities to simplify and accelerate coding.

`jac_api.py`

```python
import base64
import time
from typing import Union

import requests
from requests import HTTPError

class JacApi:
    def __init__(self, base_url: str,  creds: dict = None):
        self.base_url = base_url.rstrip('/')
        self.session = requests.session()
        if creds:
            self.authenticate(creds)

    def authenticate(self, creds: dict):
        data = self._post('user/token/', creds)
        self.session.headers['Authorization'] = f'Token {data["token"]}'
        return data

    def force_authenticate(self, creds: dict):
        try:
            self.authenticate(creds)
        except HTTPError as e:
            if e.response.status_code == 400 and 'Unable to authenticate with provided credentials' in e.response.text:
                user = {'name': 'API User'}
                user.update(creds)
                self.create_user(user)
                self.authenticate(creds)
            else:
                raise e

    def create_user(self, payload: dict):
        payload['is_activated'] = payload.get('is_activated', True)
        return self._post('user/create/', payload)

    def create_alias(self, name: str, value: str):
        payload = {'name': name, 'value': value}
        return self._post('jac/create_graph', payload)

    def create_graph(self, name: str = None):
        payload = {'name': name or f'Untitled graph {time.time()}'}
        return self._post('jac/create_graph', payload)

    def create_sentinel(self, name: str = None):
        payload = {'name': name or f'Untitled sentinel {time.time()}'}
        return self._post('jac/create_sentinel', payload)

    def delete_graph(self, jid: str):
        payload = {'gph': jid}
        return self._post('jac/delete_graph', payload)

    def delete_sentinel(self, jid: str):
        payload = {'snt': jid}
        return self._post('jac/delete_sentinel', payload)

    def get_graph(self, jid: str, detailed: bool = False, dot: bool = False):
        payload = {'gph': jid, 'detailed': detailed, 'dot': dot}
        return self._post('jac/get_graph', payload)

    def get_jac(self, jid: str):
        payload = {'snt': jid}
        return self._post('jac/get_sentinel', payload)

    def get_node_context(self, jid: str, ctx: list):
        payload = {'nd': jid, ctx: ctx}
        return self._post('jac/get_node_context', payload)

    def get_object(self, jid: str, detailed: bool = False):
        payload = {'obj': jid, 'detailed': detailed}
        return self._post('jac/get_object', payload)

    def list_alias(self):
        return self._post('jac/list_alias')

    def list_graph(self, detailed: bool = False):
        payload = {'detailed': detailed}
        return self._post('jac/list_graph', payload)

    def list_sentinel(self, detailed: bool = False):
        payload = {'detailed': detailed}
        return self._post('jac/list_sentinel', payload)

    def list_walker(self, snt_jid: str, detailed: bool = False):
        payload = {'snt': snt_jid, 'detailed': detailed}
        return self._post('jac/list_walker', payload)

    def load_app(self, name: str, code: str, encoded: bool = False):
        payload = {'name': name, 'code': code, 'encoded': encoded}
        return self._post('jac/load_app', payload)

    def load_application(self, name: str, code: str, encoded: bool = False):
        payload = {'name': name, 'code': code, 'encoded': encoded}
        return self._post('jac/load_application', payload)

    def prime_run(self, name: str, snt_jid: str, nd_jid: str, ctx: dict = None):
        payload = {'name': name, 'snt': snt_jid, 'nd': nd_jid, 'ctx': ctx or {}}
        return self._post('jac/prime_run', payload)

    def prime_walker(self, wlk_jid: str, nd_jid: str, ctx: dict = None):
        payload = {'wlk': wlk_jid, 'nd': nd_jid, 'ctx': ctx or {}}
        return self._post('jac/prime_walker', payload)

    def run(self, name: str, snt_jid: str, nd_jid: str, ctx: dict = None):
        payload = {'name': name, 'snt': snt_jid, 'nd': nd_jid, 'ctx': ctx or {}}
        return self._post('jac/run', payload)

    def run_walker(self, jid: str):
        payload = {'wlk': jid}
        return self._post('jac/run_walker', payload)

    def set_jac(self, snt_jid: str, code: Union[str, bytes], encoded: bool = False):
        payload = {'snt': snt_jid, 'code': code, 'encoded': encoded}
        return self._post('jac/set_jac', payload)

    def set_node_context(self, snt_jid: str, nd_jid: str, ctx: dict = None):
        payload = {'snt': snt_jid, 'nd_jid': nd_jid, 'ctx': ctx or {}}
        return self._post('jac/set_node_context', payload)

    def spawn_walker(self, snt_jid: str, name: str):
        payload = {'snt': snt_jid, 'name': name}
        return self._post('jac/spawn_walker', payload)

    def unspawn(self, wlk_jid: str):
        payload = {'wlk': wlk_jid}
        return self._post('jac/unspawn', payload)

    def _post(self, endpoint: str, payload: dict = None):
        response = self.session.post(f'{self.base_url}/{endpoint}', json=payload)
        if not response.ok:
            response.reason += f' -- {response.text}'
        response.raise_for_status()
        return response.json()
```