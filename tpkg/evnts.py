import pyglet
#import pyglet.text         as text
#import pyglet.window       as window
##import pyglet.window.event as pygwevnt
##import pyglet.event        as pygevnt
#import pyglet.window.key   as pygwink
from   tpkg import utl     as utl

slog    = utl.slog
W, Y, Z = utl.W, utl.Y, utl.Z
P, L, S, C, T, N, I, K, R, Q, H, M, B, A, D, E = utl.P, utl.L, utl.S, utl.C, utl.T, utl.N, utl.I, utl.K, utl.R, utl.Q, utl.H, utl.M, utl.B, utl.A, utl.D, utl.E

class FilteredEventLogger(pyglet.window.event.WindowEventLogger):
    def __init__(self, etypes):
        super().__init__()
        self.etypes = etypes

    def log(self, msg, etype=None, f=-2):
        if etype and etype not in self.etypes: slog(msg, f=f)
        elif not etype:                        slog(msg, f=f)
#        else:                                  slog(f'FILTERED {msg}', f=2)

flist    = ['on_move', 'on_mouse_motion'] # 'on_draw', 'on_move', 'on_text', 'on_text_motion', 'on_mouse_motion'
fEvntLog = FilteredEventLogger(flist)
flog     = fEvntLog.log

def on_move(x, y):
    flog(f'{x=} {y=}', etype='on_move')

def on_mouse_motion(x, y, dx, dy):
    flog(f'{x=} {y=} {dx=} {dy=}', etype='on_mouse_motion')

def on_mouse_release(tobj, x, y, button, mods=0, dbg=1):
    hh = tobj.height  ;  ww = tobj.width  ;  tlen = len(tobj.tabls)  ;  ll = tobj.LL    ;  np, nl, ns, nc, nt  = tobj.n
    y0 = y            ;   y = hh - y0     ;    nr = nl*(ns*nt + ll)  ;   w = ww/nc      ;  h = hh/nr
    cc = tobj.cc      ;   r = int(y/h)    ;     d = int(y/h)  - ll   ;   a = int(d/nr)  ;  b = int(x/w)
    p  = tobj.j()[P]  ;   l = a           ;     s = d//nt            ;   c = b          ;  t = (d - l*nr) # % nt
    txt = tobj.tabls[cc].text if cc < tlen else Z   ;   f = -2
    if dbg:   slog(f'BGN {x=:4} {y0=:4} {y=:4} {w=:6.2f} {h=:6.2f} {ll=} {nc=:2} {nr=:2} {r=:2} {d=:2} {txt=} {button=} {mods=}', f=f)
    if dbg:   slog(f'    p={p+1} l={l+1}=(d/nr) s={s+1}=(d//nt) c={c+1}=(x/w) t={t+1}=(d-l*nr)', f=f)
    if dbg:   slog(f'    before MOVE plsct={tobj.fplsct(p, l, s, c, t)}',   f=f)
    p, l, s, c, t = tobj.moveToB('MOUSE RELEASE', p, l, s, c, t)
    if dbg:   slog(f'    after  MOVE plsct={tobj.fplsct(p, l, s, c, t)}',   f=f)
    if dbg:   slog(f'END {x=:4} {y0=:4} {y=:4} {ww=:6.2f} {hh=:6.2f}',      f=f)
