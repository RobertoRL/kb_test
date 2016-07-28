import requests


class KillBillHttpClient:

    def __init__(self, host, username, password, api_key, api_secret):
        self.base_url = 'http://' + host + '/1.0/kb'
        self.username = username
        self.password = password
        self.api_key = api_key
        self.api_secret = api_secret

    def __get_api_headers(self):
        headers = {
            'X-Killbill-ApiKey': self.api_key,
            'X-Killbill-ApiSecret': self.api_secret,
        }

        return headers

    def __get_audit_headers(self):
        audit_headers = {'X-Killbill-CreatedBy': 'python-test'}

        return audit_headers

    def __get_kb_session(self):
        session = requests.Session()
        session.auth = (self.username, self.password)
        session.headers.update(self.__get_api_headers())

        return session

    def do_post(self, uri, json):
        with self.__get_kb_session() as http:
            return http.post(self.base_url + uri, json=json, headers=self.__get_audit_headers(), verify=False)

    def do_delete(self, uri):
        with self.__get_kb_session() as http:
            return http.delete(self.base_url + uri, verify=False, headers=self.__get_audit_headers())

    def do_get(self, uri):
        with self.__get_kb_session() as http:
            return http.get(self.base_url + uri, verify=False)
