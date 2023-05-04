import json
import base64
import hashlib
import hmac
import requests
from urllib.parse import urlencode, quote_plus, unquote_plus
from datetime import datetime

from translatedsearch import settings


class SummonAPI:
    def __init__(self):
        self.host = settings.SUMMON_API_HOST
        self.path = '/2.0.0/search'
        self.default_params = {'s.hl': 'false', 's.ho': 'false', 's.light': 'true', 's.ps': '50'}

    def merge_default_params(self, params):
        params2 = self.default_params
        params2.update(params)
        return params2
    
    def search(self, params):
        params = urlencode(self.merge_default_params(params), doseq=True, quote_via=quote_plus)

        headers = self.build_headers(params)
        url = 'http://{}{}?{}'.format(self.host, self.path, params)
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text

    def build_headers(self, query):
        accept = 'application/json'
        date = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
        query_string = unquote_plus('&'.join(sorted(query.split('&'))))
        id_string = "\n".join([accept, date, self.host, self.path, query_string]) + "\n"
        auth_string = self.build_auth_string(id_string)
        return {'Accept': accept,
                'x-summon-date': date,
                'Host': self.host,
                'Authorization': auth_string}

    def build_auth_string(self, id_string):
        key = bytes(settings.SUMMON_API_KEY, 'UTF-8')
        message = bytes(id_string, 'UTF-8')
        hashed_code = hmac.new(key,
                               message,
                               hashlib.sha1).digest()
        digest = base64.encodebytes(hashed_code).decode('UTF-8')
        auth_string = 'Summon {};{}'.format(settings.SUMMON_ACCESS_ID, digest)
        return auth_string.replace('\n', '')
