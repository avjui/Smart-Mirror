# smartmirror.py
# requirements
# requests, feedparser, traceback, Pillow

from Tkinter import *
from PluginManager import pluginmgr

# Intial logger
import Logger as logger

log = logger.Logger(__name__)

# Inital loading plugin instance
plugins = pluginmgr.get_plugins()


class FullscreenWindow:
    def __init__(self):
        self.tk = Tk()
        self.tk.configure(background='black')
        self.topFrame = Frame(self.tk, background='black')
        self.bottomFrame = Frame(self.tk, background='black')
        self.topFrame.pack(side=TOP, fill=BOTH, expand=YES)
        self.bottomFrame.pack(side=BOTTOM, fill=BOTH, expand=YES)
        self.state = False
        self.tk.bind("<Return>", self.toggle_fullscreen)
        self.tk.bind("<Escape>", self.end_fullscreen)

        for key in plugins:
            self.plugin_raw = pluginmgr.get_plugins()[key]
            if self.plugin_raw.load:
                try:
                    self.plugin = self.plugin_raw(self.topFrame)
                    self.plugin.pack(self.plugin_raw.position)
                    log.info('%s Plugin loaded with Version %s' % (self.plugin_raw.name, self.plugin_raw.version))
                except Exception as e:
                    log.error('Load Plugin give Exception:[  %s  ]' % e)

                    self.plugin.pack(side=RIGHT, anchor=N, padx=100, pady=60)

    def toggle_fullscreen(self, event=None):
        self.state = not self.state  # Just toggling the boolean
        self.tk.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.tk.attributes("-fullscreen", False)
        return "break"


if __name__ == '__main__':
    w = FullscreenWindow()
    w.tk.mainloop()
