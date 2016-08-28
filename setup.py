#By default, the installer will be created as dist\Output\setup.exe.
import time
import sys
import os
import pygame
# ModuleFinder can't handle runtime changes to __path__, but win32com uses them
pygamedir = os.path.split(pygame.base.__file__)[0]
os.path.join(pygamedir, pygame.font.get_default_font()),
os.path.join(pygamedir, 'SDL.dll'),
os.path.join(pygamedir, 'SDL_ttf.dll')

try:
    # if this doesn't work, try import modulefinder
    import py2exe.mf as modulefinder
    import win32com
    for p in win32com.__path__[1:]:
        modulefinder.AddPackagePath("win32com", p)
    for extra in ["win32com.shell"]: #,"win32com.mapi"
        __import__(extra)
        m = sys.modules[extra]
        for p in m.__path__[1:]:
            modulefinder.AddPackagePath(extra, p)
except ImportError:
    # no build path setup, no worries.
    pass
from distutils.core import setup
import py2exe
setup(windows=['popStar.py'])
