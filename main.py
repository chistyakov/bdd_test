#!/usr/bin/env python

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler

class FullNameProviderHTTPServer(object):
    SERVER_NAME = ''
    PORT_NUMBER = 8080
    def __init__(self):
        self.httpd = HTTPServer((self.SERVER_NAME, self.PORT_NUMBER),
            FullNameProviderRequestHandler)
        self.users_list = []

    def start(self):
        self.httpd.serve_forever()

    def stop(self):
        self.httpd.shutdown()

    def add_user(self, user):
        self.users_list.append(user)


class FullNameProviderRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        return


def main():
    try:
        server = FullNameProviderHTTPServer()
        server.start()
    except KeyboardInterrupt:
        pass
    server.stop()


if __name__ == "__main__":
    main()
