#!/usr/bin/env python

"""Copyright (c) 2015 Douglas Otwell <https://github.com/Douglas6/omxcontrol.git>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
import dbus
import datetime

class OmxControl:
    ACTION_DECREASE_SPEED = 1
    ACTION_INCREASE_SPEED = 2
    ACTION_REWIND = 3
    ACTION_FAST_FORWARD = 4
    ACTION_SHOW_INFO = 5
    ACTION_PREVIOUS_AUDIO = 6
    ACTION_NEXT_AUDIO = 7
    ACTION_PREVIOUS_CHAPTER = 8
    ACTION_NEXT_CHAPTER = 9
    ACTION_PREVIOUS_SUBTITLE = 10
    ACTION_NEXT_SUBTITLE = 11
    ACTION_TOGGLE_SUBTITLE = 12
    ACTION_DECREASE_SUBTITLE_DELAY = 13
    ACTION_INCREASE_SUBTITLE_DELAY = 14
    ACTION_EXIT = 15
    ACTION_PAUSE = 16
    ACTION_DECREASE_VOLUME = 17
    ACTION_INCREASE_VOLUME = 18
    ACTION_SEEK_BACK_SMALL = 19
    ACTION_SEEK_FORWARD_SMALL = 20
    ACTION_SEEK_BACK_LARGE = 21
    ACTION_SEEK_FORWARD_LARGE = 22
    ACTION_SEEK_RELATIVE = 25
    ACTION_SEEK_ABSOLUTE = 26
    ACTION_STEP = 23
    ACTION_BLANK = 24
    ACTION_MOVE_VIDEO = 27
    ACTION_HIDE_VIDEO = 28
    ACTION_UNHIDE_VIDEO = 29
    ACTION_HIDE_SUBTITLES = 30
    ACTION_SHOW_SUBTITLES = 31

    user = None;
    name = None;
    __iface_root = None;
    __iface_props = None;
    __iface_player = None;

    def __init__(self, user=None, name=None):
        self.user = user if user else os.environ["USER"]
        self.name = name if name else "org.mpris.MediaPlayer2.omxplayer"

        bus_address_filename = "/tmp/omxplayerdbus.{}".format(self.user)
        bus_pid_filename = "/tmp/omxplayerdbus.{}.pid".format(self.user)
        try:
            with open(bus_address_filename, "r") as f:
                bus_address = f.read().rstrip()
            with open(bus_pid_filename, "r") as f:
                bus_pid = f.read().rstrip()
        except IOError:
            raise OmxControlError("Unable to find D-Bus session for user {}. Is omxplayer running under this user?".format(self.user))

        os.environ["DBUS_SESSION_BUS_ADDRESS"] = bus_address
        os.environ["DBUS_SESSION_BUS_PID"] = bus_pid
        session_bus = dbus.SessionBus()
        try:
            omx_object = session_bus.get_object(self.name, 
                    "/org/mpris/MediaPlayer2", 
                    introspect=False)
            self.__iface_root = dbus.Interface(omx_object, "org.mpris.MediaPlayer2")
            self.__iface_props = dbus.Interface(omx_object, "org.freedesktop.DBus.Properties")
            self.__iface_player = dbus.Interface(omx_object, "org.mpris.MediaPlayer2.Player")
        except dbus.exceptions.DBusException as ex:
            raise OmxControlError(message="A D-Bus exception occurred: {}. Is omxplayer running?".format(ex.get_dbus_message()))

    def __assertConnected(self):
        if not self.__iface_root or not self.__iface_props or not self.__iface_player:
            raise OmxControlError(message="OmxControl is not connected")

    """Root interface"""

    def quit(self):
        """Terminate the omsplayer process."""
        self.__assertConnected()
        try: self.__iface_root.Quit()
        except dbus.exceptions.DBusException: pass

    """Properties interface"""

    def canQuit(self):
        """Return whether or not the player can quit."""
        self.__assertConnected()
        try: return bool(self.__iface_props.CanQuit())
        except dbus.exceptions.DBusException: pass

    def fullscreen(self):
        """Return whether or not the player is fullscreen."""
        self.__assertConnected()
        try: return bool(self.__iface_props.Fullscreen())
        except dbus.exceptions.DBusException: pass

    def canSetFullscreen(self):
        """Return whether or not the player can go fullscreen."""
        self.__assertConnected()
        try: return bool(self.__iface_props.CanSetFullscreen())
        except dbus.exceptions.DBusException: pass

    def canRaise(self):
        """Return whether or not the player can be brought to the top of all windows."""
        self.__assertConnected()
        try: return bool(self.__iface_props.CanRaise())
        except dbus.exceptions.DBusException: pass

    def hasTrackList(self):
        """Return whether or not the player has a track list."""
        self.__assertConnected()
        try: return bool(self.__iface_props.HasTrackList())
        except dbus.exceptions.DBusException: pass

    def identity(self):
        """Return the player name."""
        self.__assertConnected()
        try: return str(self.__iface_props.Identity())
        except dbus.exceptions.DBusException: pass

    def supportedUriSchemes(self):
        """Return playable URI formats."""
        self.__assertConnected()
        try: return self.__parseStringArray(self.__iface_props.SupportedUriSchemes())
        except dbus.exceptions.DBusException: pass

    def supportedMimeTypes(self):
        """Return supported MIME types. Note: currently not implemented"""
        self.__assertConnected()
        try: return self.__parseStringArray(self.__iface_props.SupportedMimeTypes())
        except dbus.exceptions.DBusException: pass

    def __parseStringArray(self, arr):
        lst = []
        for itm in arr: lst.append(str(itm))
        return lst

    def canGoNext(self):
        """Return whether or not the player can skip to the next track."""
        self.__assertConnected()
        try: return bool(self.__iface_props.CanGoNext())
        except dbus.exceptions.DBusException: pass

    def canGoPrevious(self):
        """Return whether or not the player can skip to the previous track."""
        self.__assertConnected()
        try: return bool(self.__iface_props.CanGoPrevious())
        except dbus.exceptions.DBusException: pass

    def canSeek(self):
        """Return whether or not the player can seek."""
        self.__assertConnected()
        try: return bool(self.__iface_props.CanSeek())
        except dbus.exceptions.DBusException: pass

    def canControl(self):
        """Return whether or not the player can be controlled."""
        self.__assertConnected()
        try: return bool(self.__iface_props.CanControl())
        except dbus.exceptions.DBusException: pass

    def canPlay(self):
        """Return whether or not the player can play."""
        self.__assertConnected()
        try: return bool(self.__iface_props.CanPlay())
        except dbus.exceptions.DBusException: pass

    def canPause(self):
        """Return whether or not the player can be paused."""
        self.__assertConnected()
        try: return bool(self.__iface_props.CanPause())
        except dbus.exceptions.DBusException: pass

    def playbackStatus(self):
        """Return current state of the player, either 'Paused' or 'Playing'."""
        self.__assertConnected()
        try: return str(self.__iface_props.PlaybackStatus())
        except dbus.exceptions.DBusException: pass

    def volume(self, vol):
        """Set the volume and return the current volume."""
        self.__assertConnected()
        try:
            if vol: 
                return float(self.__iface_props.Volume(dbus.Double(vol)))
            else: 
                return float(self.__iface_props.Volume())
        except dbus.exceptions.DBusException: pass

    def mute(self):
        """Mute the audio stream."""
        self.__assertConnected()
        try: self.__iface_props.Mute()
        except dbus.exceptions.DBusException: pass

    def unmute(self):
        """Unmute the audio stream."""
        self.__assertConnected()
        try: self.__iface_props.Unmute()
        except dbus.exceptions.DBusException: pass

    def position(self):
        """Return the current position of the playing media"""
        self.__assertConnected()
        try:
            micros = self.__iface_props.Position()
            return datetime.timedelta(0, 0, micros)
        except dbus.exceptions.DBusException: pass

    def duration(self):
        """Return the total length of the playing media"""
        self.__assertConnected()
        try:
            micros = self.__iface_props.Duration()
            return datetime.timedelta(0, 0, micros)
        except dbus.exceptions.DBusException: pass

    def minimumRate(self):
        """Return the maximum playback rate of the video."""
        self.__assertConnected()
        try: return float(self.__iface_props.MinimumRate())
        except dbus.exceptions.DBusException: pass

    def maximumRate(self):
        """Return the maximum playback rate of the video."""
        self.__assertConnected()
        try: return float(self.__iface_props.MaximumRate())
        except dbus.exceptions.DBusException: pass

    """ player interface """

    def next(self):
        """Skip to the next chapter."""
        self.__assertConnected()
        try: return self.__iface_player.Next()
        except dbus.exceptions.DBusException: pass
     
    def previous(self):
        """Skip to the previous chapter."""
        self.__assertConnected()
        try: return self.__iface_player.Previous()
        except dbus.exceptions.DBusException: pass
     
    def pause(self):
        """Toggles the play state."""
        self.__assertConnected()
        try: self.__iface_player.Pause()
        except dbus.exceptions.DBusException: pass

    def playPause(self):
        """Same as the pause method."""
        self.__assertConnected()
        try: self.__iface_player.PlayPause()
        except dbus.exceptions.DBusException: pass

    def stop(self):
        """Stop playback."""
        self.__assertConnected()
        try: self.__iface_player.Stop()
        except dbus.exceptions.DBusException: pass

    def seek(self, micros):
        """Perform a relative seek, in microseconds."""
        self.__assertConnected()
        try: return float(self.__iface_player.Seek(dbus.Int64(micros)))
        except dbus.exceptions.DBusException: pass

    def setPosition(self, micros):
        """Seeks to a specific location in the file."""
        self.__assertConnected()
        try:
            self.__iface_player.SetPosition(dbus.ObjectPath("/"), dbus.Int64(micros))
        except dbus.exceptions.DBusException as ex: pass
            
    def listSubtitles(self):
        """Return a list of all known subtitles."""
        self.__assertConnected()
        try:
            items = self.__iface_player.ListSubtitles()
            return self.__parseList(items)
        except dbus.exceptions.DBusException as ex: pass

    def listAudio(self):
        """Return a list of all known audio streams."""
        self.__assertConnected()
        try:
            items = self.__iface_player.ListAudio()
            return self.__parseList(items)
        except dbus.exceptions.DBusException as ex: pass

    def listVideo(self):
        """Return a list of all known video streams."""
        self.__assertConnected()
        try:
            items = self.__iface_player.ListVideo()
            return self.__parseList(items)
        except dbus.exceptions.DBusException as ex: pass

    def __parseList(self, itms):
        """Parse a omxplayer 'list' string into a list of dictionaries."""
        items = []
        for itm in itms:
            parms = itm.split(":")
            item = {}
            item["index"] = int(parms[0])
            item["language"] = parms[1]
            item["name"] = parms[2]
            item["codec"] = parms[3]
            item["active"] = True if parms[4] == u"active" else False 
            items.append(item)
        return items
            
    def selectSubtitle(self, idx):
        """Select the subtitle at a given index."""
        self.__assertConnected()
        try: return bool(self.__iface_player.SelectSubtitle(dbus.Int32(idx)))
        except dbus.exceptions.DBusException as ex: pass

    def selectAudio(self, idx):
        """Select the audio stream at a given index."""
        self.__assertConnected()
        try: return bool(self.__iface_player.SelectAudio(dbus.Int32(idx)))
        except dbus.exceptions.DBusException as ex: pass

    def showSubtitles(self):
        """Turn on subtitles."""
        self.__assertConnected()
        try: self.__iface_player.ShowSubtitles()
        except dbus.exceptions.DBusException as ex: pass

    def hideSubtitles(self):
        """Turn off subtitles."""
        self.__assertConnected()
        try: self.__iface_player.HideSubtitles()
        except dbus.exceptions.DBusException as ex: pass

    def action(self, act):
        """Execute a 'keyboard' command."""
        self.__assertConnected()
        try: self.__iface_player.Action(dbus.Int32(act))
        except dbus.exceptions.DBusException: pass

    def videoPos(self, pos):
        """Set video position."""
        self.__assertConnected()
        pos_str = "{} {} {} {}".format(pos[0], pos[1], pos[2], pos[3])
        try: 
            cur_pos = self.__iface_player.VideoPos(dbus.ObjectPath("/"), dbus.String(pos_str)).split()
            return (int(cur_pos[0]), int(cur_pos[1]), int(cur_pos[2]), int(cur_pos[3]))
        except dbus.exceptions.DBusException: pass

    """Convenience methods"""

    def status(self):
        status = {}
        status["playbackStatus"] = self.playbackStatus()
        status["duration"] = self.duration()
        status["position"] = self.position()

        return status

    def properties(self):
        props = {}
        props["identity"] = self.identity()
        props["playbackStatus"] = self.playbackStatus()
        props["duration"] = self.duration()
        props["position"] = self.position()
        props["canQuit"] = self.canQuit()
        props["fullscreen"] = self.fullscreen()
        props["canSetFullscreen"] = self.canSetFullscreen()
        props["canRaise"] = self.canRaise()
        props["hasTrackList"] = self.hasTrackList()
        props["supportedUriSchemes"] = self.supportedUriSchemes()
        props["supportedMimeTypes"] = self.supportedMimeTypes()
        props["canGoNext"] = self.canGoNext()
        props["canGoPrevious"] = self.canGoPrevious()
        props["canSeek"] = self.canSeek()
        props["canControl"] = self.canControl()
        props["canPlay"] = self.canPlay()
        props["canPause"] = self.canPause()
        props["volume"] = self.volume(None)
        props["minimumRate"] = self.minimumRate()
        props["maximumRate"] = self.maximumRate()

        return props

class OmxControlError(Exception):
    def __init__(self, message=None):
        if message:
            self.message = message

if __name__ == "__main__":
    import pprint
    pp = pprint.PrettyPrinter(indent=4)

    omx = OmxControl()
    props = omx.properties()
    pp.pprint(props)
