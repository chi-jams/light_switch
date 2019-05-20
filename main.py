#!/usr/bin/python3

from ast import literal_eval
from bottle import jinja2_view, Bottle, request, route, run, static_file
from gevent import monkey; monkey.patch_all()
from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler
from jinja2 import Template
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

    room = b.get_group(cfg['group'])
    while True:
        try:
            msg = ws.receive()
            print('I got a thing: {}'.format(msg))
            start = time.time()
            light_settings = literal_eval(msg)
            for setting in light_settings:
                b.set_light([int(i) for i in room["lights"]], setting,
                    light_settings[setting], transitiontime=1)
            end = time.time()
            print("Took {} seconds".format(end - start))
        except WebSocketError:
            print("There's an error")
            break

@app.route('/formstuff')
def feed_static():
    return static_file('formstuff.js', root='./static/')

if __name__ == '__main__':
    cfg = yaml.load(open(DEFAULT_CFG, 'r').read(), Loader=Loader)

    b = Bridge(cfg['hue_ip'])
    b.connect()
    server = WSGIServer((cfg['server_ip'], cfg['server_port']), app,
        handler_class=WebSocketHandler)
    server.serve_forever()
