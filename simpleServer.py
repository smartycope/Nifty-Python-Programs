from http.server import BaseHTTPRequestHandler, HTTPServer
import time, json, threading
from io import BytesIO


# from flask import Flask
#
# app = Flask(__name__)
#
# @app.route("/")
# def hello():
    # return "Hello, World!"
#
#
#
#
#
serverIP = '70.167.220.168'
myIP = '205.185.99.26'
serverLocal = '192.168.1.168'
bkeys = 'bkeys.org'
#
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
#
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hello, world!')
#
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(b'This is POST request. ')
        response.write(b'Received: ')
        response.write(body)
        self.wfile.write(response.getvalue())
#
#
httpd = HTTPServer(('localhost', 8080), SimpleHTTPRequestHandler)
httpd.serve_forever()
#