#!/usr/bin/env python
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from collections import OrderedDict
import json
from urlparse import urlparse, parse_qs



class FullNameProviderHTTPServer(HTTPServer):
    def __init__(self, *args, **kwargs):
        HTTPServer.__init__(self, *args, **kwargs)
        self.users_list = []

    def add_user(self, user):
        self.users_list.append(user)

    def find_user_by_id(self, user_id):
        try:
            return (u for u in self.users_list if u['id'] == user_id).next()
        except StopIteration:
            raise UserNotFoundExcpetion("user with id {0} was not found".format(user_id))

    def drop_user_by_id(self, user_id):
        try:
            user = self.find_user_by_id(user_id)
            self.users_list.remove(user)
        except UserNotFoundExcpetion:
            pass

    def drop_all_users(self):
        self.users_list = []


class UserNotFoundExcpetion(Exception):
    pass

class CannotGetUserId(Exception):
    pass


class FullNameProviderRequestHandler(BaseHTTPRequestHandler):
    SUPPORTED_HEADER = 'application/json'
    error_content_type = SUPPORTED_HEADER
    error_message_format = '{"Error code": %(code)d, "Message": "%(message)s", "Error code explanation": "%(explain)s"}'
    def do_GET(self):
        if not self.is_content_type_supported():
            self.send_error(415)
            return
        try:
            self.send_full_name_json()
        except UserNotFoundExcpetion:
            self.send_error(404)
        except CannotGetUserId:
            self.send_error(400)
        return

    def send_full_name_json(self):
        user_id = self._get_user_id()
        user_full_name_data = self._get_user_full_name_data(user_id)
        self.send_response(200)
        self.send_header('Content-Type', self.SUPPORTED_HEADER)
        self.end_headers()
        self.wfile.write(json.dumps(user_full_name_data))

    def _get_user_id(self):
        try:
            return int(extract_query_param_from_url_path(self.path, 'id'))
        except (KeyError, ValueError):
            raise CannotGetUserId("can not extract user id from URL {0}".format(self.path))

    def _get_user_full_name_data(self, user_id):
        user = self.server.find_user_by_id(user_id)
        return get_ordered_subdict(user, 'name', 'surname', 'patronymic')

    def is_content_type_supported(self):
        upper_headers = {key.upper(): self.headers[key].upper() for key in self.headers}
        return self.SUPPORTED_HEADER.upper() in upper_headers.get('CONTENT-TYPE', self.SUPPORTED_HEADER.upper())


def extract_query_param_from_url_path(url, param_name):
    query_string = urlparse(url).query
    query_dict = parse_qs(query_string)
    return query_dict[param_name][0]



def get_ordered_subdict(D, *key_names_to_get):
    subset = OrderedDict([(name, D.get(name, '')) for name in key_names_to_get])
    return subset


def main():
    try:
        SERVER_NAME = ''
        PORT_NUMBER = 8080
        httpd = FullNameProviderHTTPServer((SERVER_NAME, PORT_NUMBER),
            FullNameProviderRequestHandler)
        test_user_data = {
                'id': 1,
                'name': 'Alexander',
                'surname': 'Chistyakov',
                'patronymic': 'Olegovich'
            }
        httpd.add_user(test_user_data)
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.shutdown()


if __name__ == "__main__":
    main()
