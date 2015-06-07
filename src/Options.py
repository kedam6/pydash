"""
Module handling options menu and configuration loading
It handles showing window itself and using configuration of data
"""

__author__ = 'Kedam'

import Tkinter
import tkMessageBox
import ttk
import ConfigParser


# pylint: disable=global-variable-not-assigned
# pylint: disable=global-statement
# Global variables are necessary here, without them I cant save data and load it

class OptionsObject(object):
    """Object containing program config data"""

    def __init__(self):
        self.resolution = 2
        self.musicon = True
        self.musicvolume = 0.2
        self.soundon = True
        self.soundvolume = 1.0
        self.parser = ConfigParser.RawConfigParser()
        self.load()

    def load(self):
        """Loads data from config file, if it fails, save default data to that file"""
        self.parser = ConfigParser.RawConfigParser()
        try:
            with open('config.cfg', 'rb') as configfile:
                self.parser.read('config.cfg')
                self.resolution = self.parser.getint('Config', 'res')
                self.soundon = self.parser.getboolean('Config', 'son')
                self.soundvolume = self.parser.getfloat('Config', 'sv')
                self.musicon = self.parser.getboolean('Config', 'mon')
                self.musicvolume = self.parser.getfloat('Config', 'mv')
        except IOError:
            self.save()

    def save(self):
        """Saved config data to config file"""
        self.parser = ConfigParser.RawConfigParser()
        self.parser.add_section('Config')
        self.parser.set('Config', 'res', str(self.resolution))
        self.parser.set('Config', 'son', str(self.soundon))
        self.parser.set('Config', 'sv', str(self.soundvolume))
        self.parser.set('Config', 'mon', str(self.musicon))
        self.parser.set('Config', 'mv', str(self.musicvolume))
        with open('config.cfg', 'wb') as configfile:
            self.parser.write(configfile)


# All of these are necessary to be global, otherwise whole gui thing doesnt work
# It is necessary for them to stay here, not in object
CONFIG = OptionsObject()
ROOT = None
RESOLUTION_BOX = None
SOUND_ON = None
SOUND_VALUE = None
MUSIC_ON = None
MUSIC_VALUE = None


def ok_callback():
    """Function handling ok button press"""
    global ROOT
    global RESOLUTION_BOX
    global SOUND_ON, SOUND_VALUE, MUSIC_ON, MUSIC_VALUE, CONFIG
    CONFIG.resolution = RESOLUTION_BOX['values'].index(RESOLUTION_BOX.get())
    CONFIG.soundon = SOUND_ON.get()
    CONFIG.musicon = MUSIC_ON.get()
    CONFIG.musicvolume = MUSIC_VALUE.get() / 100.0
    CONFIG.soundvolume = SOUND_VALUE.get() / 100.0
    CONFIG.save()

    tkMessageBox.showinfo("Saved", "Options saved")


def cancel_callback():
    """Function handling cancel button press"""
    ROOT.destroy()


def main():
    """Main function showing options gui"""
    global ROOT
    global RESOLUTION_BOX
    global SOUND_ON, SOUND_VALUE, MUSIC_ON, MUSIC_VALUE

    ROOT = Tkinter.Tk()
    resolutiontext = Tkinter.StringVar()
    SOUND_ON = Tkinter.BooleanVar()
    SOUND_ON.set(CONFIG.soundon)
    MUSIC_ON = Tkinter.BooleanVar()
    MUSIC_ON.set(CONFIG.musicon)
    SOUND_VALUE = Tkinter.IntVar()
    SOUND_VALUE.set(CONFIG.soundvolume * 100)
    MUSIC_VALUE = Tkinter.IntVar()
    MUSIC_VALUE.set(CONFIG.musicvolume * 100)

    top = Tkinter.Frame(ROOT)
    top_sounds = Tkinter.Frame(ROOT)
    top_music = Tkinter.Frame(ROOT)
    bottom = Tkinter.Frame(ROOT)

    top.pack(side=Tkinter.TOP)
    top_sounds.pack(side=Tkinter.TOP)
    top_music.pack(side=Tkinter.TOP)
    bottom.pack(side=Tkinter.BOTTOM, fill=Tkinter.BOTH)

    # Resolution changing
    Tkinter.Label(ROOT, text="Resolution").pack(in_=top, side=Tkinter.TOP)
    RESOLUTION_BOX = ttk.Combobox(top, textvariable=resolutiontext, state='readonly')
    RESOLUTION_BOX['values'] = ('640 x 480', '800 x 600', '1024 x 768')
    RESOLUTION_BOX.current(CONFIG.resolution)
    RESOLUTION_BOX.pack(side=Tkinter.TOP)

    # Sound on
    Tkinter.Label(ROOT, text="Sounds").pack(in_=top_sounds, side=Tkinter.TOP)

    soundcheck = Tkinter.Checkbutton(top_sounds,
                                     text="On",
                                     variable=SOUND_ON,
                                     onvalue=True,
                                     offvalue=False)
    soundcheck.pack(side=Tkinter.LEFT)

    soundslider = Tkinter.Scale(top_sounds,
                                variable=SOUND_VALUE,
                                from_=0,
                                to_=100,
                                tickinterval=100,
                                orient=Tkinter.HORIZONTAL,
                                width=10)
    soundslider.pack(side=Tkinter.LEFT)

    # Music on

    Tkinter.Label(ROOT, text="Music").pack(in_=top_music, side=Tkinter.TOP)

    musiccheck = Tkinter.Checkbutton(top_music,
                                     text="On",
                                     variable=MUSIC_ON,
                                     onvalue=True,
                                     offvalue=False)
    musiccheck.pack(side=Tkinter.LEFT)

    musicslider = Tkinter.Scale(top_music,
                                variable=MUSIC_VALUE,
                                from_=0, to_=100,
                                tickinterval=100,
                                orient=Tkinter.HORIZONTAL,
                                width=10)
    musicslider.pack(side=Tkinter.LEFT)

    ok_button = Tkinter.Button(ROOT,
                               width=10,
                               height=2,
                               text="OK",
                               command=ok_callback)
    cancel_button = Tkinter.Button(ROOT,
                                   width=10,
                                   height=2,
                                   text="Cancel",
                                   command=cancel_callback)
    ok_button.pack(in_=bottom, side=Tkinter.LEFT)
    cancel_button.pack(in_=bottom, side=Tkinter.LEFT)
    ROOT.after(100, ROOT.focus_force)
    ROOT.mainloop()
