__author__ = 'Kedam'

import Tkinter
import tkMessageBox
import ttk


class OptionsObject(object):

    def __init__(self):
        self.resolution = 2
        self.musicon = True
        self.musicvolume = 0.2
        self.soundon = True
        self.soundvolume = 1.0
        self.load()

    def load(self):
        pass

    def save(self):
        pass



config = OptionsObject()
root = None
resolutionbox = None
soundon = None
soundvalue = None
musicon = None
musicvalue = None

def okCallBack():
    global root
    global resolutionbox
    global soundon, soundvalue, musicon, musicvalue, config
    config.resolution = resolutionbox.get()
    tkMessageBox.showinfo("Saved", "Options saved")


def cancelCallBack():
    root.destroy()


def main():
    global root
    global resolutionbox
    global soundon, soundvalue, musicon, musicvalue

    root = Tkinter.Tk()
    resolutiontext = Tkinter.StringVar()
    soundon = Tkinter.IntVar()
    soundon.set(config.soundon)
    musicon = Tkinter.IntVar()
    musicon.set(config.musicon)
    soundvalue = Tkinter.IntVar()
    soundvalue.set(config.soundvolume * 100)
    musicvalue = Tkinter.IntVar()
    musicvalue.set(config.musicvolume * 100)


    top = Tkinter.Frame(root)
    top_sounds = Tkinter.Frame(root)
    top_music = Tkinter.Frame(root)
    bottom = Tkinter.Frame(root)

    top.pack(side=Tkinter.TOP)
    top_sounds.pack(side=Tkinter.TOP)
    top_music.pack(side=Tkinter.TOP)
    bottom.pack(side=Tkinter.BOTTOM, fill=Tkinter.BOTH)

    # Resolution changing
    Tkinter.Label(root, text="Resolution").pack(in_=top, side=Tkinter.TOP)
    resolutionbox = ttk.Combobox(top, textvariable=resolutiontext, state='readonly')
    resolutionbox['values'] = ('640 x 480', '800 x 600', '1024 x 768')
    resolutionbox.current(config.resolution)
    resolutionbox.pack(side=Tkinter.TOP)

    # Sound on
    Tkinter.Label(root, text="Sounds").pack(in_=top_sounds, side=Tkinter.TOP)

    soundcheck = Tkinter.Checkbutton(top_sounds, text="On", variable=soundon, onvalue=True, offvalue=False)
    soundcheck.pack(side=Tkinter.LEFT)

    soundslider = Tkinter.Scale(top_sounds, variable=soundvalue, from_=0, to_=100, tickinterval=100, orient=Tkinter.HORIZONTAL, width=10)
    soundslider.pack(side=Tkinter.LEFT)

    #Music on

    Tkinter.Label(root, text="Music").pack(in_=top_music, side=Tkinter.TOP)

    musiccheck = Tkinter.Checkbutton(top_music, text="On", variable=musicon, onvalue=True, offvalue=False)
    musiccheck.pack(side=Tkinter.LEFT)

    musicslider = Tkinter.Scale(top_music, variable=musicvalue, from_=0, to_=100, tickinterval=100, orient=Tkinter.HORIZONTAL, width=10)
    musicslider.pack(side=Tkinter.LEFT)

    B = Tkinter.Button(root, width=10, height=2, text="OK", command=okCallBack)
    C = Tkinter.Button(root, width=10, height=2, text="Cancel", command=cancelCallBack)
    B.pack(in_=bottom, side=Tkinter.LEFT)
    C.pack(in_=bottom, side=Tkinter.LEFT)
    root.after(100, lambda: root.focus_force())
    root.mainloop()

