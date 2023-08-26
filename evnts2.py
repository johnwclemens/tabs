import pyglet
import pyglet.text         as text
import pyglet.window       as window
#import pyglet.window.event as pygwnev
import pyglet.event        as pygevnt
import pyglet.window.key   as pygwink
from   tpkg import utl     as utl

slog    = utl.slog
W, Y, Z = utl.W, utl.Y, utl.Z

def eventLogger(etypes):
   def decorator(callback):
       def wrapper(*args, **kwargs):
           etype = args[0]
           if etype in etypes:
               slog(f'{args  =}')
               slog(f'{kwargs=}')
               slog(f'{etypes=}')
               slog(f'{etype =}')
           return callback
       return wrapper
   return decorator

