#!/usr/bin/python3

from phue import Bridge
import sys
import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
DEFAULT_CFG = "cfg.yaml"

if __name__ == "__main__":
    if len(sys.argv) not in [2,3]:
        print("Usage: {} <lightOn>".format(sys.argv[0]))
        sys.exit(-1)
    cfg = yaml.load(open(DEFAULT_CFG, 'r').read(), Loader=Loader)

    b = Bridge(cfg['hue_ip'])
    b.connect()

    room = b.get_group(cfg['group'])

    b.set_light([int(i) for i in room["lights"]], "on", eval(sys.argv[1]))
    if len(sys.argv) > 2:
        b.set_light([int(i) for i in room["lights"]], "hue", eval(sys.argv[2]), transitiontime=1)
