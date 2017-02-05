#
# -*- coding: <utf-8> -*-
#

import os
import sys
from Tkinter import Frame

import Logger as logger

'''
Code base on code from http://yannik520.github.io/python_plugin_framework.html
'''

log = logger.Logger(__name__)


class Plugin(object, Frame):
    class __metaclass__(type):
        def __init__(cls, name, bases, attrs):
            if not hasattr(cls, 'plugins'):
                cls.plugins = {}
            else:
                if attrs['__module__'] != 'PluginManager':
                    modul = attrs['__module__'].upper()
                    cls.plugins[modul] = cls

        def get_plugins(cls):
            return cls.plugins


class PluginMgr(object):
    plugin_dirs = {}
    adding = True

    # make the manager class as singleton
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(PluginMgr, cls).__new__(cls, *args, **kwargs)

        return cls._instance

    def __init__(self):

        self.plugin_dirs.update({
            'plugins': False,
        })

    def _load_all(self):
        #TODO: Clean up the code
        for (pdir, loaded) in self.plugin_dirs.iteritems():
            if loaded:
                continue

            for root, dirs, mod in os.walk(pdir):
                sys.path.insert(0, root)
                lookdir = root
                sys.path.insert(0, lookdir)
                for mod in [x[:-3] for x in os.listdir(lookdir) if x.endswith('.py')]:
                    if mod and mod != '__init__':
                        if mod in sys.modules:
                            log.info('Module %s already exists, skip' % mod)
                        else:
                            try:
                                pymod = __import__(mod)
                                self.plugin_dirs[pdir] = True
                                log.info("Plugin Found [Name] %s	[Path] %s" % (mod, pymod.__file__))
                                print mod.upper(), pymod.__file__
                            except ImportError, e:
                                log.error('Loading failed, skip plugin %s/%s Error: %s' % os.path.basename(lookdir), mod, e)

                del (sys.path[0])
                break

    def get_plugins(self):
        """ the return value is dict of name:class pairs """
        self._load_all()
        return Plugin.get_plugins()

pluginmgr = PluginMgr()
