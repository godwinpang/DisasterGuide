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

def normalize_1_to_10(value, min, max):
    return (value - min + 1) / max * 10

EARTHQUAKE_THRESHOLD = normalize_1_to_10(7.0, 1, 10)  # magnitude from 1 to 10
HURRICANE_THRESHOLD = normalize_1_to_10(3, 1, 5)  # Saffir-Simpson Hurricane Wind Scale; 1 to 5
WILDFIRE_THRESHOLD = normalize_1_to_10(3, 1, 4)  # Wildland Urban Interface Hazard Scale; 3D scale from 1 to 4 each dimension
TORNADO_THRESHOLD = normalize_1_to_10(3, 0, 5)  # Fujita scale; 0 to 5

OUTGOING_IP_ADDRESS = "0.0.0.0"
WEB_SOCKET_SERVER_PORT = 8085
BACKEND_SERVER_PORT = 8088
DATABASE_PORT = 5432

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
    elif type == "wildfire":
        return severity >= WILDFIRE_THRESHOLD
    elif type == "tornado":
        return severity >= TORNADO_THRESHOLD
    else:
        print("[ WARNING ] Natural disaster type " + str(type) + " is not currently supported in determining severity.")
        return False


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
            print("[ ERROR ] Invalid path " + str(self.path) + " received.")
            response = {"success": False, "failure_reason": "Invalid path " + str(self.path) + "."}

        # send JSON response back to client
        json_response = json.dumps(response)  # string representation
        self.wfile.write(json_response.encode())
        return True

def run_main_server(server_class=HTTPServer, handler_class=CustomRequestHandler, port=BACKEND_SERVER_PORT):
    server_address = (OUTGOING_IP_ADDRESS, port)
    httpd = server_class(server_address, handler_class)
    print('Server running at localhost:' + str(port) + '...')
    httpd.serve_forever()

async def get_disaster(websocket, path):
    while(True):
        disaster = await websocket.recv()
        disaster_id = str(uuid())
        print(disaster)
        disaster_parsed = json.loads(disaster)
        database.log_disaster(disaster_id, disaster_parsed["type"], disaster_parsed["latitude"], disaster_parsed["longitude"], disaster_parsed["radius"], disaster_parsed["severity"])

def start_socket_loop(loop):
    asyncio.set_event_loop(loop)
    socket_server = websockets.serve(get_disaster, OUTGOING_IP_ADDRESS, WEB_SOCKET_SERVER_PORT)
    loop.run_until_complete(socket_server)
    loop.run_forever()

if __name__ == '__main__':
    database = Database("localhost", DATABASE_PORT, "disasterguide", "postgres", "postgres")
    t = Thread(target=start_socket_loop, args=(asyncio.get_event_loop(),))
    t.start()

    run_main_server()