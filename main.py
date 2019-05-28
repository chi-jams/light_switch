#!/usr/bin/python3

from ast import literal_eval
from bottle import jinja2_view, Bottle, request, route, run, static_file
from gevent import monkey; monkey.patch_all()
from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler
from jinja2 import Template
import json
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

    init_vals = {'init_vals':
            {key: bridge.get_group(cfg['group'])['action'][key] for key in
                    ('hue', 'sat', 'bri')}}
    ws.send(json.dumps(init_vals))

    while True:
        try:
            msg = ws.receive()
            cmd_queue.put(msg)

        except WebSocketError as err:
            print("There's an error: {}".format(err))
            break

# Thought this would be able to just be a static directory, but it was being
# weird and dropping the file type so here we are.
@app.route('/formstuff')
def feed_static():
    return static_file('formstuff.js', root='./static/')

# So this is dumb, why do we do this? Basically the Python Philips Hue API takes
# at least 0.1 seconds to make light changes, and can go up to wait times as
# long as a second. Since the set_light function blocks this makes dragging a
# slider be extremely unresponsive. This alleviates that, but it'd be best to
# figure out how to push changes to multiple lights and values in one go. This
# is my lame solution using the library though.
def set_lights(bridge, cmd_queue):
    room = bridge.get_group(cfg['group'])
    print(room)
    last_settings = None
    while True:
        msg = None
        # We only care about the last command
        while not cmd_queue.empty():
            msg = cmd_queue.get()

        if msg and last_settings != msg:
            last_settings = msg
            print(msg)
            # Bold move parsing text and expecting it to just work
            for name, val in literal_eval(msg).items():
                bridge.set_light([int(i) for i in room["lights"]], name, val,
                        transitiontime=1)

if __name__ == '__main__':
    cfg = yaml.load(open(DEFAULT_CFG, 'r').read(), Loader=Loader)
    server = WSGIServer((cfg['server_ip'], cfg['server_port']), app,
        handler_class=WebSocketHandler)
    cmd_queue = Queue()
    bridge = Bridge(cfg['hue_ip'])
    bridge.connect()
    t = Process(target = set_lights, args = (bridge, cmd_queue))

    try:
        t.start()
        server.serve_forever()
    except KeyboardInterrupt:
        t.join()
