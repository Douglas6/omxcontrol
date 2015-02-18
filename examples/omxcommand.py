#!usr/bin env python

import argparse
from omxcontrol import *

parser = argparse.ArgumentParser()
parser.add_argument("cmd", help="omxplayer command")
parser.add_argument("-u", "--user", dest="user", help="omxplayer user")
parser.add_argument("-n", "--name", dest="name", help="omxplayer D-Bus name")
args = parser.parse_args()

try:
    omx = OmxControl(user=args.user, name=args.name)

    if args.cmd == "1": omx.action(OmxControl.ACTION_DECREASE_SPEED)
    elif args.cmd == "2": omx.action(OmxControl.ACTION_INCREASE_SPEED)
    elif args.cmd == "<": omx.action(OmxControl.ACTION_REWIND)
    elif args.cmd == ">": omx.action(OmxControl.ACTION_FAST_FORWARD)
    elif args.cmd == "z": print(omx.properties())
    elif args.cmd == "j": omx.action(OmxControl.ACTION_PREVIOUS_AUDIO)
    elif args.cmd == "k": omx.action(OmxControl.ACTION_NEXT_AUDIO)
    elif args.cmd == "i": omx.action(OmxControl.ACTION_PREVIOUS_CHAPTER)
    elif args.cmd == "o": omx.action(OmxControl.ACTION_NEXT_CHAPTER)
    elif args.cmd == "n": omx.action(OmxControl.ACTION_PREVIOUS_SUBTITLE)
    elif args.cmd == "m": omx.action(OmxControl.ACTION_NEXT_SUBTITLE)
    elif args.cmd == "s": omx.action(OmxControl.ACTION_TOGGLE_SUBTITLE)
    elif args.cmd == "w": omx.showSubtitles()
    elif args.cmd == "x": omx.hideSubtitles()
    elif args.cmd == "d": omx.action(OmxControl.ACTION_DECREASE_SUBTITLE_DELAY)
    elif args.cmd == "f": omx.action(OmxControl.ACTION_INCREASE_SUBTITLE_DELAY)
    elif args.cmd == "q": omx.quit()
    elif args.cmd == "p": omx.pause()
    elif args.cmd == "-": omx.action(OmxControl.ACTION_DECREASE_VOLUME)
    elif args.cmd == "+" or args.cmd == "=": omx.action(OmxControl.ACTION_INCREASE_VOLUME)
    elif args.cmd == "<<": omx.action(OmxControl.ACTION_SEEK_BACK_SMALL)
    elif args.cmd == ">>": omx.action(OmxControl.ACTION_SEEK_FORWARD_SMALL)
    elif args.cmd == "<<<": omx.action(OmxControl.ACTION_SEEK_BACK_LARGE)
    elif args.cmd == ">>>": omx.action(OmxControl.ACTION_SEEK_FORWARD_LARGE)

except OmxControlError as ex:
    print(ex.message)
