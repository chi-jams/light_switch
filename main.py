#!/usr/bin/python3

from ast import literal_eval
from bottle import jinja2_view, Bottle, request, route, run, static_file
from gevent import monkey; monkey.patch_all()
from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler
from jinja2 import Template
from multiprocessing import Process, Queue
from phue import Bridge
import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

import time

DEFAULT_CFG = "cfg.yaml"

app = Bottle()

@app.route('/')
@jinja2_view('index.html', template_lookup=['templates'])
def index():
    return {}

@app.route('/websocket')
def handle_websocket():
    ws = request.environ.get('wsgi.websocket')

    if not ws:
        abort(400, 'Expected a websocket request!')

    while True:
        try:
            msg = ws.receive()
            print('I got a thing: {}'.format(msg))
            cmd_queue.put(msg)

        except WebSocketError:
            print("There's an error")
            break

@app.route('/formstuff')
def feed_static():
    return static_file('formstuff.js', root='./static/')

# So this is dumb, why do we do this? Basically the Python Philips Hue API takes
# at least 0.1 seconds to make light changes, and can go up to wait times as
# long as a second. Since the set_light function blocks this makes dragging a
# slider be extremely unresponsive. This alleviates that, but it'd be best to
# figure out how to push changes to multiple lights and values in one go. This
# is my lame solution using the library though.
def set_lights(cmd_queue):
    b = Bridge(cfg['hue_ip'])
    b.connect()
    room = b.get_group(cfg['group'])
    last_settings = None
    while True:
        msg = None
        # We only care about the last command
        while not cmd_queue.empty():
            msg = cmd_queue.get()

        if msg and last_settings != msg:
            print('Wat: {}'.format(msg))
            last_settings = msg
            # Bold move parsing text and expecting it to just work
            for name, val in literal_eval(msg).items():
                b.set_light([int(i) for i in room["lights"]], name, val,
                        transitiontime=1)

if __name__ == '__main__':
    cfg = yaml.load(open(DEFAULT_CFG, 'r').read(), Loader=Loader)
    server = WSGIServer((cfg['server_ip'], cfg['server_port']), app,
        handler_class=WebSocketHandler)
    cmd_queue = Queue()
    t = Process(target = set_lights, args = (cmd_queue,))

    try:
        t.start()
        server.serve_forever()
    except KeyboardInterrupt:
        t.join()
