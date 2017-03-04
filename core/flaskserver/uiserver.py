from flask import Flask, request
import logging
import socket
from threading import Thread
from core.socketsender import Socketsender


log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

class Uiserver(Socketsender):

    def __init__(self, host, port):
        Socketsender.__init__(self, host, port)

        self.app = Flask(__name__)

        self.app.add_url_rule("/setcolor", "setcolor", self.set_color, methods=['POST'])
        self.app.add_url_rule('/', 'index', self.index)
        self.app.add_url_rule('/<path:path>', "static_proxy", self.static_proxy)

        self.last_data = None

    def set_color(self):

        #  make sure only changed data is sent, it's very easy to send the same color over and over
        if request.data != self.last_data:

            request_text = request.data.decode('UTF-8')
            strings = request_text.split(",")

            red = int(float(strings[0]))
            green = int(float(strings[1]))
            blue = int(float(strings[2]))

            self.send_color_change(red, green, blue)

            self.last_data = request.data

        return "Got it"

    def index(self):
        return self.app.send_static_file("index.html")

    def static_proxy(self, path):
        # send_static_file will guess the correct MIME type
        return self.app.send_static_file(path)

    def run(self):
        self.app.run(host="0.0.0.0")
