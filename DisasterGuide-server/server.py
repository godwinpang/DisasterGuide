#!usr/bin/env python3
"""
Base code loosely pulled from https://www.codexpedia.com/python/python-web-server-for-get-and-post-requests/, adapted
for Python 3.
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import post_addlocation
import post_getlocation
import post_getlocationhistory
import get_getallusers
import get_getdisasters
import post_adduser
import post_getuser
import post_help
import post_getwatsoncontext
import post_adddisaster
from database import *
import asyncio
import websockets
from threading import Thread
from uuid import uuid4 as uuid

EARTHQUAKE_THRESHOLD = 7.0  # magnitude from 1 to 10
HURRICANE_THRESHOLD = 3  # Saffir-Simpson Hurricane Wind Scale

def get_content_length(headers):
    for tp in headers._headers:
        variable, value = tp
        if variable == "Content-Length":
            return int(value)

    raise ValueError("Missing Content-Length in header.")


def severity_threshold(type, severity):
    if type == "earthquake":
        return severity >= EARTHQUAKE_THRESHOLD
    elif type == "hurricane":
        return severity >= HURRICANE_THRESHOLD
    else:
        raise NotImplementedError("Natural disaster type " + str(type) + " is not currently supported in determining severity.")


class CustomRequestHandler(BaseHTTPRequestHandler):
    POST_REQUESTS = {
        "/adduser": post_adduser.handler,
        "/getuser": post_getuser.handler,
        "/addlocation": post_addlocation.handler,
        "/getlocation": post_getlocation.handler,
        "/getlocationhistory": post_getlocationhistory.handler,
        "/getallusers": get_getallusers.handler,
        "/help": post_help.handler,
        "/getwatsoncontext": post_getwatsoncontext.handler,
        "/adddisaster": post_adddisaster.handler
    }

    GET_REQUESTS = {
        "/getallusers": get_getallusers.handler,
        "/getdisasters": get_getdisasters.handler
    }

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_HEAD(self):
        self._set_headers()

    def do_GET(self):
        self._set_headers()

        try:
            if self.path == "/getdisasters":
                response = CustomRequestHandler.GET_REQUESTS[self.path](database, severity_threshold)
            else:
                response = CustomRequestHandler.GET_REQUESTS[self.path](database)

        except KeyError as _:
            print("Invalid path " + str(self.path) + " received.")
            response = {"success": False, "failure_reason": "Invalid path " + str(self.path) + "."}

        # send JSON response back to client
        json_response = json.dumps(response)  # string representation
        self.wfile.write(json_response.encode())
        return True

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
            response = CustomRequestHandler.POST_REQUESTS[self.path](database, body_json)

        except KeyError as _:
            print("Invalid path " + str(self.path) + " received.")
            response = {"success": False, "failure_reason": "Invalid path " + str(self.path) + "."}

        # send JSON response back to client
        json_response = json.dumps(response)  # string representation
        self.wfile.write(json_response.encode())
        return True

def run_main_server(server_class=HTTPServer, handler_class=CustomRequestHandler, port=8088):
    server_address = ('0.0.0.0', port)
    httpd = server_class(server_address, handler_class)
    print('Server running at localhost:' + str(port) + '...')
    httpd.serve_forever()

async def get_disaster(websocket, path):
    while(True):
        disaster = await websocket.recv()
        disaster_id = str(uuid())
        database.log_disaster(disaster_id, disaster["type"], disaster["latitude"], disaster["longitude"], disaster["radius"], disaster["severity"])

def start_socket_loop(loop):
    asyncio.set_event_loop(loop)
    socket_server = websockets.serve(get_disaster, 'localhost', 8085)
    loop.run_until_complete(socket_server)
    loop.run_forever()

if __name__ == '__main__':
    database = Database("localhost", 5432, "disasterguide", "postgres", "postgres")
    t = Thread(target=start_socket_loop, args=(asyncio.get_event_loop(),))
    t.start()

    run_main_server()