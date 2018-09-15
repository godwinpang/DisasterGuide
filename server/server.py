#!usr/bin/env python3
"""
Base code pulled from https://www.codexpedia.com/python/python-web-server-for-get-and-post-requests/, adapted for
Python 3.
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import post_location
import post_help
import json

def get_content_length(headers):
    for tp in headers._headers:
        variable, value = tp
        if variable == "Content-Length":
            return int(value)

    raise ValueError("Missing Content-Length in header.")

class CustomRequestHandler(BaseHTTPRequestHandler):
    POST_REQUESTS = {
        "/location": post_location.execute,
        "/help": post_help.execute
    }

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_HEAD(self):
        self._set_headers()

    def do_GET(self):
        self._set_headers()
        print(self.path)
        self.wfile.write("<html><body><h1>Get Request Received!</h1></body></html>")

    def do_POST(self):
        """
        Handle POST requests to server.
        :return: True if successful
        """
        self._set_headers()
        content_len = get_content_length(self.headers)
        post_body = self.rfile.read(content_len)

        body_json = json.loads(post_body)

        print("JSON received:", body_json)

        try:
            response = CustomRequestHandler.POST_REQUESTS[self.path](body_json)

        except KeyError as _:
            print("Invalid path " + str(self.path) + " received.")
            response = {"success": False, "failureReason": "Invalid path " + str(self.path) + "."}

        # send JSON response back to client
        json_response = json.dumps(response)  # string representation
        self.wfile.write(json_response.encode())
        return True

def run(server_class=HTTPServer, handler_class=CustomRequestHandler, port=8088):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Server running at localhost:' + str(port) + '...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()