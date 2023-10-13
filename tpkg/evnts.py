from   inspect import currentframe as cfrm
import pyglet
#import pyglet.text         as text
#import pyglet.window       as window
##import pyglet.window.event as pygwevnt
##import pyglet.event        as pygevnt
import pyglet.window.key     as pygwink
from   pyglet.window.key import symbol_string    as psym
from   pyglet.window.key import modifiers_string as pmod
from   pyglet.window.key import motion_string    as pmtn
import pyglet.window.mouse   as pygmous
from   tpkg import utl       as utl
from   tpkg import cmds      as cmds
#from   tpkg import tests   as tests

slog, fmtf, fmtl, fmtm         = utl.slog, utl.fmtf, utl.fmtl, utl.fmtm
X, W, Y, Z                     = utl.X, utl.W, utl.Y, utl.Z
TT, NN, II, KK                 = utl.TT, utl.NN, utl.II, utl.KK
MELODY, CHORD, ARPG            = utl.MELODY, utl.CHORD, utl.ARPG
LARROW, RARROW, DARROW, UARROW = utl.LARROW, utl.RARROW, utl.DARROW, utl.UARROW
BOLD, COLOR, ITALIC, FONT_NAME, FONT_SIZE                                = utl.BOLD, utl.COLOR, utl.ITALIC, utl.FONT_NAME, utl.FONT_SIZE
P, L, S, C, T, N, I, K, R, Q, H, M, B, A, D, E                           = utl.P, utl.L, utl.S, utl.C, utl.T, utl.N, utl.I, utl.K, utl.R, utl.Q, utl.H, utl.M, utl.B, utl.A, utl.D, utl.E
isAlt, isCtl, isShf, isAltShf, isCtlAlt, isCtlShf, isCtlAltShf, isNumLck = utl.isAlt, utl.isCtl, utl.isShf, utl.isAltShf, utl.isCtlAlt, utl.isCtlShf, utl.isCtlAltShf, utl.isNumLck

MODS  = 0
FLIST = []

def fn(cf):   return cf.f_code.co_name

def flog(msg, filt=None, fd=4):
    if (filt and filt not in FLIST) or not filt:
        slog(f'{msg} {filt=}', f=fd)
########################################################################################################################################################################################################

class FilteredEventLogger(pyglet.window.event.WindowEventLogger):
    def __init__(self, tobj, fd=None, flst=None):
        super().__init__(fd)
        self.tobj = tobj
        global FLIST   ;   FLIST = flst

    def on_activate(          self):                     flog(Z,                                            filt=fn(cfrm()))
    def on_close(             self):                     flog(Z,                                            filt=fn(cfrm()))
    def on_context_lost(      self):                     flog(Z,                                            filt=fn(cfrm()))
    def on_context_state_lost(self):                     flog(Z,                                            filt=fn(cfrm()))
    def on_deactivate(        self):                     flog(Z,                                            filt=fn(cfrm()))
    def on_draw(              self, **kwargs):           flog(f'{kwargs=}',                                 filt=fn(cfrm()))
    def on_expose(            self):                     flog(Z,                                            filt=fn(cfrm()))
    def on_hide(              self):                     flog(Z,                                            filt=fn(cfrm()))
    def on_key_press(         self, s, m):               flog(f'{s=} {psym(s)} {m=} {pmod(m)}',             filt=fn(cfrm()))
    def on_key_release(       self, s, m):               flog(f'{s=} {psym(s)} {m=} {pmod(m)}',             filt=fn(cfrm()))
    def on_mouse_drag(        self, x, y, dx, dy, b, m): flog(f'{x=} {y=} {dx=} {dy=} {b=} {m=} {pmod(m)}', filt=fn(cfrm()))
    def on_mouse_enter(       self, x, y):               flog(f'{x=} {y=}',                                 filt=fn(cfrm()))
    def on_mouse_leave(       self, x, y):               flog(f'{x=} {y=}',                                 filt=fn(cfrm()))
    def on_mouse_motion(      self, x, y, dx, dy):       flog(f'{x=} {y=} {dx=} {dy=}',                     filt=fn(cfrm()))
    def on_mouse_press(       self, x, y, b, m=0):       flog(f'{x=} {y=} {b=} {m=} {pmod(m)}',             filt=fn(cfrm()))
    def on_mouse_release(     self, x, y, b, m=0):       flog(f'{x=} {y=} {b=} {m=} {pmod(m)}',             filt=fn(cfrm()))
    def on_mouse_scroll(      self, x, y, dx, dy):       flog(f'{x=} {y=} {dx=} {dy=}',                     filt=fn(cfrm()))
    def on_move(              self, x, y):               flog(f'{x=} {y=}',                                 filt=fn(cfrm()))
    def on_resize(            self, w, h):               flog(f'{w=} {h=}',                                 filt=fn(cfrm()))
    def on_show(              self):                     flog(Z,                                            filt=fn(cfrm()))
    def on_text(              self, text):               flog(f'{text=}',                                   filt=fn(cfrm()))
    def on_text_motion(       self, motion):             flog(f'{motion=} {pmtn(motion)}',                  filt=fn(cfrm()))
    def on_text_motion_select(self, motion):             flog(f'{motion=} {pmtn(motion)}',                  filt=fn(cfrm()))

########################################################################################################################################################################################################

def fxy(x, y):    return f'({x:4}, {y:4})'
def fbm(b, m):    return f'{b=} {m} {pmod(m):42}'
def ft(t):        return f'{t=}'
def ftm(motion):  return f'{motion:6} {motion:#06x} {W*16} {MODS} {pmod(MODS):42}'
def fsm(s, m):    return f'{s:6} {s:#06x} {psym(s):16} {m} {pmod(m):42}'

########################################################################################################################################################################################################
def on_close(tobj, dbg=1):
    if dbg: slog('calling tobj.close()')
    tobj.close()
    return True

def on_draw(tobj, **kwargs):
    if   tobj.drwBGC % 3 == 0:     pyglet.gl.glClearColor(0.0, 0.0, 0.0, 0.0)
    elif tobj.drwBGC % 3 == 1:     pyglet.gl.glClearColor(0.5, 0.5, 0.5, 0.5)
    elif tobj.drwBGC % 3 == 2:     pyglet.gl.glClearColor(1.0, 1.0, 1.0, 1.0)
    tobj.clear()
    tobj.batch.draw()
    if  tobj.snapReg and (tobj.SNAPS or tobj.snapType == utl.INIT):
        tobj.snapReg = 0
        _ = fmtm(kwargs) if kwargs else Z
        snapPath = tobj.snapshot(f'on_draw({_})')
        slog(f'{tobj.snapWhy=} {tobj.snapType=} {tobj.snapId=}\n{snapPath=}', f=-2)
#    else: slog(f'{kwargs=}') if kwargs else slog()
#        if tobj.TEST:   tests.testSprTxt_0(snapPath)
########################################################################################################################################################################################################
def on_key_press(tobj, symb, mods, dbg=1):
    assert tobj
    retv  = True
    global MODS      ;     MODS = mods
    fontBold, fontItalic = tobj.fontBold, tobj.fontItalic
    hcurs = tobj.hcurs
    tkb   = tobj.keyboard
    kd    = tkb.data if tkb else None
    kbk   = psym(symb)   ;   m = MODS
    if dbg:    slog(f'BGN {fsm(symb, mods)} kd={fmtm(kd)}')
    if   kbk == 'A' and isCtlShf(kd, m):     cmd = cmds.TogArrowCmd(tobj, '@^A', v=1)         ;  cmd.do()
    elif kbk == 'A' and isCtl(   kd, m):     cmd = cmds.TogArrowCmd(tobj, '@ A', v=0)         ;  cmd.do()
    elif kbk == 'B' and isCtlShf(kd, m):     cmd = cmds.TogBlankCmd(tobj, '@^B', -1)          ;  cmd.do()
    elif kbk == 'B' and isCtl(   kd, m):     cmd = cmds.TogBlankCmd(tobj, '@ B',  1)          ;  cmd.do()
    elif kbk == 'C' and isCtlShf(kd, m):     tobj.copyTabs(     '@^C')
    elif kbk == 'C' and isCtl(   kd, m):     tobj.copyTabs(     '@ C')
    elif kbk == 'D' and isCtlShf(kd, m):     tobj.deleteTabs(   '@^D')
    elif kbk == 'D' and isCtl(   kd, m):     tobj.deleteTabs(   '@ D')
    elif kbk == 'E' and isCtlShf(kd, m):     tobj.eraseTabs(    '@^E')
#   elif kbk == 'E' and isCtl(   kd, m):     tobj.eraseTabs(    '@ E')
    elif kbk == 'F' and isCtlShf(kd, m):     cmd = cmds.TogFullScrnCmd(tobj, '@^F')           ;  cmd.do()
    elif kbk == 'F' and isCtl(   kd, m):     cmd = cmds.TogFlatShrpCmd(tobj, '@ F')           ;  cmd.do()
    elif kbk == 'G' and isCtlShf(kd, m):     tobj.move2LastTab( '@^G', page=1)
    elif kbk == 'G' and isCtl(   kd, m):     tobj.move2LastTab( '@ G', page=0)
    elif kbk == 'H' and isCtlShf(kd, m):     tobj.move2FirstTab('@^H', page=1)
    elif kbk == 'H' and isCtl(   kd, m):     tobj.move2FirstTab('@ H', page=0)
    elif kbk == 'I' and isCtlShf(kd, m):     tobj.insertSpace(  '@^I')
    elif kbk == 'I' and isCtl(   kd, m):     cmd = cmds.TogTTsCmd(tobj, '@ I', II)            ;  cmd.do()
    elif kbk == 'J' and isCtlShf(kd, m):     cmd = cmds.CsrJumpCmd(tobj, '@^J', txt='0', abso=1)  ;  cmd.do()
    elif kbk == 'J' and isCtl(   kd, m):     cmd = cmds.CsrJumpCmd(tobj, '@ J', txt='0', abso=0)  ;  cmd.do()
    elif kbk == 'K' and isCtlShf(kd, m):     cmd = cmds.TogTTsCmd(tobj, '@^K', KK)            ;  cmd.do()
    elif kbk == 'K' and isCtl(   kd, m):     cmd = cmds.TogTTsCmd(tobj, '@ K', KK)            ;  cmd.do()
    elif kbk == 'L' and isCtlShf(kd, m):     cmd = cmds.TogLLsCmd(tobj, '@^L')                ;  cmd.do()
    elif kbk == 'L' and isCtl(   kd, m):     cmd = cmds.TogLLsCmd(tobj, '@ L')                ;  cmd.do()
    elif kbk == 'M' and isCtlShf(kd, m):     tobj.flipZZs(      '@^M', 1)
    elif kbk == 'M' and isCtl(   kd, m):     tobj.flipZZs(      '@ M', 0)
    elif kbk == 'N' and isCtlShf(kd, m):     cmd = cmds.TogTTsCmd(tobj, '@^N', NN)            ;  cmd.do()
    elif kbk == 'N' and isCtl(   kd, m):     cmd = cmds.TogTTsCmd(tobj, '@ N', NN)            ;  cmd.do()
    elif kbk == 'O' and isCtlShf(kd, m):     cmd = cmds.TogCsrModeCmd(tobj, '@^O', -1)        ;  cmd.do()
    elif kbk == 'O' and isCtl(   kd, m):     cmd = cmds.TogCsrModeCmd(tobj, '@ O',  1)        ;  cmd.do()
    elif kbk == 'P' and isCtlShf(kd, m):     tobj.addPage(      '@^P', ins=0)
    elif kbk == 'P' and isCtl(   kd, m):     tobj.addPage(      '@ P', ins=None)
    elif kbk == 'Q' and isCtlShf(kd, m):     retv = tobj.quit(  '@^Q', error=0, save=0)
    elif kbk == 'Q' and isCtl(   kd, m):     retv = tobj.quit(  '@ Q', error=0, save=1)
    elif kbk == 'R' and isCtlShf(kd, m):     cmd = cmds.TogKordNamesCmd(tobj, '@ R', hit=1)   ;  cmd.do()
    elif kbk == 'R' and isCtl(   kd, m):     cmd = cmds.TogKordNamesCmd(tobj, '@ R', hit=0)   ;  cmd.do()
    elif kbk == 'S' and isCtlShf(kd, m):     cmd = cmds.ShiftTabsCmd(tobj, '@^S')             ;  cmd.do()
#   elif kbk == 'S' and isCtl(   kd, m):     tobj.saveDataFile( '@ S', self.dataPath1)
    elif kbk == 'S' and isCtl(   kd, m):     cmd = cmds.SwapTabCmd(tobj, '@ S', txt=Z)        ;  cmd.do()
    elif kbk == 'T' and isCtlShf(kd, m):     cmd = cmds.TogTTsCmd(tobj, '@^T', TT)            ;  cmd.do()
    elif kbk == 'T' and isCtl(   kd, m):     cmd = cmds.TogTTsCmd(tobj, '@ T', TT)            ;  cmd.do()
    elif kbk == 'U' and isCtlShf(kd, m):     tobj.reset(        '@^U')
    elif kbk == 'U' and isCtl(   kd, m):     tobj.reset(        '@ U')
#   elif kbk == 'V' and isCtlAlt(kd, m):     tobj.pasteTabs(    '@&V', hc=0, kk=1)
    elif kbk == 'V' and isCtlShf(kd, m):     tobj.pasteTabs(    '@^V', kk=1)
    elif kbk == 'V' and isCtl(   kd, m):     tobj.pasteTabs(    '@ V', kk=0)
    elif kbk == 'W' and isCtlShf(kd, m):     tobj.swapCols(     '@^W')
    elif kbk == 'W' and isCtl(   kd, m):     tobj.swapCols(     '@ W')
    elif kbk == 'X' and isCtlShf(kd, m):     tobj.cutTabs(      '@^X')
    elif kbk == 'X' and isCtl(   kd, m):     tobj.cutTabs(      '@ X')
    ####################################################################################################################################################################################################
    elif kbk == 'ESCAPE':                    tobj.flipSelectAll('ESCAPE')
    elif kbk == 'TAB' and isCtl(kd, m):      cmd = cmds.SetCHVModeCmd(tobj, '@ TAB', MELODY, LARROW)  ;  cmd.do()
    elif kbk == 'TAB':                       cmd = cmds.SetCHVModeCmd(tobj, '  TAB', MELODY, RARROW)  ;  cmd.do()
#   elif kbk == 'SLASH'     and isCtl(mods):  tobj.setTab(      '@ SLASH', '/')
#   elif kbk == 'SLASH':                      tobj.setTab(      '  SLASH', '/')
#   elif kbk == 'BACKSLASH' and isCtl(mods):  tobj.setTab(      '@ BACKSLASH', '\\')
#   elif kbk == 'BACKSLASH':                  tobj.setTab(      '  BACKSLASH', '\\')
#   elif kbk == 'SLASH'     and isCtl(mods):  tobj.setCHVMode(  '@ SLASH',     ARPG,   LARROW, DARROW)
#   elif kbk == 'SLASH':                      tobj.setCHVMode(  '  SLASH',     ARPG,   RARROW, UARROW)
#   elif kbk == 'BACKSLASH' and isCtl(mods):  tobj.setCHVMode(  '@ BACKSLASH', ARPG,   LARROW, UARROW)
#   elif kbk == 'BACKSLASH':                  tobj.setCHVMode(  '  BACKSLASH', ARPG,   RARROW, DARROW)
    elif kbk == 'A' and isAltShf(kd, m):     cmd = cmds.TogBGCCmd(tobj, '&^A')                ;  cmd.do()
    elif kbk == 'A' and isAlt(   kd, m):     cmd = cmds.TogBGCCmd(tobj, '& A')                ;  cmd.do()
    elif kbk == 'D' and isAltShf(kd, m):     cmd = cmds.TogDrwBGCCmd(tobj, '&^D', -1)         ;  cmd.do()
    elif kbk == 'D' and isAlt(   kd, m):     cmd = cmds.TogDrwBGCCmd(tobj, '& D',  1)         ;  cmd.do()
    elif kbk == 'N' and isAltShf(kd, m):     cmd = cmds.SetNCmd(tobj, '&^N', txt=Z)           ;  cmd.do()
    elif kbk == 'N' and isAlt(   kd, m):     cmd = cmds.SetNCmd(tobj, '& N', txt=Z)           ;  cmd.do()
    elif kbk == 'P' and isAltShf(kd, m):     cmd = cmds.TogPageCmd(tobj, '&^P', -1)           ;  cmd.do()
    elif kbk == 'P' and isAlt   (kd, m):     cmd = cmds.TogPageCmd(tobj, '& P',  1)           ;  cmd.do()
    elif kbk == 'R' and isAltShf(kd, m):     cmd = cmds.RotSprCmd(tobj, '&^R', hcurs[0], -1)  ;  cmd.do()
    elif kbk == 'R' and isAlt(   kd, m):     cmd = cmds.RotSprCmd(tobj, '& R', hcurs[0],  1)  ;  cmd.do()
    elif kbk == 'V' and isAltShf(kd, m):     cmd = cmds.TogVisibleCmd(tobj, '&^V')            ;  cmd.do()
    elif kbk == 'V' and isAlt(kd, m):        cmd = cmds.TogVisibleCmd(tobj, '& V')            ;  cmd.do() 
    elif kbk == 'Z' and isAltShf(kd, m):     tobj.RESIZE = not tobj.RESIZE   ;  tobj.resizeTniks(dbg=1)
    elif kbk == 'Z' and isAlt(   kd, m):                                        tobj.resizeTniks(dbg=1)
    ####################################################################################################################################################################################################
    elif kbk == 'B' and isAltShf(kd, m):     cmd = cmds.SetFontPrmCmd(tobj, BOLD,      not fontBold,   'fontBold')     ;  cmd.do()
    elif kbk == 'B' and isAlt(   kd, m):     cmd = cmds.SetFontPrmCmd(tobj, BOLD,      not fontBold,   'fontBold')     ;  cmd.do()
    elif kbk == 'C' and isAltShf(kd, m):     cmd = cmds.SetFontPrmCmd(tobj, COLOR,        -1,          'clrIdx')       ;  cmd.do()
    elif kbk == 'C' and isAlt(   kd, m):     cmd = cmds.SetFontPrmCmd(tobj, COLOR,         1,          'clrIdx')       ;  cmd.do()
    elif kbk == 'I' and isAltShf(kd, m):     cmd = cmds.SetFontPrmCmd(tobj, ITALIC,    not fontItalic, 'fontItalic')   ;  cmd.do()
    elif kbk == 'I' and isAlt(   kd, m):     cmd = cmds.SetFontPrmCmd(tobj, ITALIC,    not fontItalic, 'fontItalic')   ;  cmd.do()
    elif kbk == 'M' and isAltShf(kd, m):     cmd = cmds.SetFontPrmCmd(tobj, FONT_NAME,    -1,          'fontNameIdx')  ;  cmd.do()
    elif kbk == 'M' and isAlt(   kd, m):     cmd = cmds.SetFontPrmCmd(tobj, FONT_NAME,     1,          'fontNameIdx')  ;  cmd.do()
    elif kbk == 'S' and isAltShf(kd, m):     cmd = cmds.SetFontPrmCmd(tobj, FONT_SIZE,     33 / 32,    'fontSize')     ;  cmd.do()
    elif kbk == 'S' and isAlt(   kd, m):     cmd = cmds.SetFontPrmCmd(tobj, FONT_SIZE,     32 / 33,    'fontSize')     ;  cmd.do()
#    elif kbk == 'PAGEUP'   and isCtlShf(kd, m): tobj.log(f'{kbk=} @^PAGEUP')     ;   cmd = cmds.TogPageCmd(tobj, '@^PAGEUP', -1)  ;  cmd.do()
#    elif kbk == 'PAGEUP'   and isCtl(   kd, m): tobj.log(f'{kbk=} @ PAGEUP')     ;   cmd = cmds.TogPageCmd(tobj, '@ PAGEUP',  1)  ;  cmd.do()
#    elif kbk == 'PAGEUP':                       tobj.log(f'{kbk=}   PAGEUP')     ;   tobj.moveUp(    f' PAGEUP')                              # go down to bottom tab on same line, wrap to next line
#    elif kbk == 'PAGEDOWN' and isCtlShf(kd, m): tobj.log(f'{kbk=} @^PAGEDOWN')   ;   cmd = cmds.TogPageCmd(tobj, '@^PAGEDOWN', -1)  ;  cmd.do()
#    elif kbk == 'PAGEDOWN' and isCtl(   kd, m): tobj.log(f'{kbk=} @ PAGEDOWN')   ;   cmd = cmds.TogPageCmd(tobj, '@ PAGEDOWN',  1)  ;  cmd.do()
#    elif kbk == 'PAGEDOWN':                     tobj.log(f'{kbk=}   PAGEDOWN')   ;   tobj.moveDown(    f' PAGEDOWN')                            # go down to bottom tab on same line, wrap to next line
    else:  retv = False   ;   slog(f'UNH {fsm(symb, mods)} kd={fmtm(kd)}') if dbg else None
    ####################################################################################################################################################################################################
    if  not  tobj.isParsing():
        if   kbk == 'ENTER' and isCtl(kd, m):     cmd = cmds.SetCHVModeCmd(tobj, '@ ENTER',     CHORD,  v=DARROW)        ;  cmd.do()
        elif kbk == 'ENTER':                      cmd = cmds.SetCHVModeCmd(tobj, '  ENTER',     CHORD,  v=UARROW)        ;  cmd.do()
        elif kbk == 'SPACE' and tobj.tblank != W: tobj.autoMove(    '   SPACE') # todo
#            elif dbg: self.log(f'Unexpected {self.kbkEvntTxt()} while parsing', f=2)
    if dbg:  slog(f'END {    fsm(symb, mods)} kd={fmtm(kd)}, {retv=}')
    return retv
########################################################################################################################################################################################################
#  99 evnts on_key_press       BGN  65507 0xffe3 LCTRL            2 MOD_CTRL                                   kd=
# 183 evnts on_key_press       UNH  65507 0xffe3 LCTRL            2 MOD_CTRL                                   kd=
# 190 evnts on_key_press       END  65507 0xffe3 LCTRL            2 MOD_CTRL                                   kd=, retv=False
#  99 evnts on_key_press       BGN  65505 0xffe1 LSHIFT           3 MOD_SHIFT|MOD_CTRL                         kd=
# 183 evnts on_key_press       UNH  65505 0xffe1 LSHIFT           3 MOD_SHIFT|MOD_CTRL                         kd=
# 190 evnts on_key_press       END  65505 0xffe1 LSHIFT           3 MOD_SHIFT|MOD_CTRL                         kd=, retv=False
#  99 evnts on_key_press       BGN    113 0x0071 Q                3 MOD_SHIFT|MOD_CTRL                         kd=
# ...
# 190 evnts on_key_press       END    113 0x0071 Q                3 MOD_SHIFT|MOD_CTRL                         kd=, retv=False
########################################################################################################################################################################################################
def on_key_release(tobj, symb, mods, dbg=1):
    assert tobj
    global MODS      ;     MODS = mods
    if dbg: slog(f'    {fsm(symb, mods)}')
    return True
########################################################################################################################################################################################################
def on_mouse_press(tobj, x, y, bttn, mods=0, dbg=1):
    assert tobj
    if dbg: slog(f'UNH {fxy(x, y)}  {fbm(bttn, mods)}')

def on_mouse_release(tobj, x, y, bttn, mods=0, dbg=1):
    global MODS     ;     MODS = mods
    if bttn==pygmous.LEFT:
        hh = tobj.height  ;  ww = tobj.width  ;  tlen = len(tobj.tabls)  ;  ll = tobj.LL    ;  np, nl, ns, nc, nt  = tobj.n
        y0 = y            ;   y = hh - y0     ;    nr = nl*(ns*nt + ll)  ;   w = ww/nc      ;  h = hh/nr
        cc = tobj.cc      ;   r = int(y/h)    ;     d = int(y/h)  - ll   ;   a = int(d/nr)  ;  b = int(x/w)
        p  = tobj.j()[P]  ;   l = a           ;     s = d//nt            ;   c = b          ;  t = (d - l*nr) # % nt
        txt = tobj.tabls[cc].text if cc < tlen else Z   ;   f = -2
        if dbg:   slog(f'BGN {x=:4} {y0=:4} {y=:4} {w=:6.2f} {h=:6.2f} {ll=} {nc=:2} {nr=:2} {r=:2} {d=:2} {txt=} {bttn=} {mods=}', f=f)
        if dbg:   slog(f'    p={p+1} l={l+1}=(d/nr) s={s+1}=(d//nt) c={c+1}=(x/w) t={t+1}=(d-l*nr)', f=f)
        if dbg:   slog(f'    before MOVE plsct={tobj.fplsct(p, l, s, c, t)}',   f=f)
        p, l, s, c, t = tobj.moveToB('MOUSE RELEASE', p, l, s, c, t)
        if dbg:   slog(f'    after  MOVE plsct={tobj.fplsct(p, l, s, c, t)}',   f=f)
        if dbg:   slog(f'END {fxy(x, y)} {y0:4} ({ww:4}x{hh:4})  {fbm(bttn, mods)}', f=f)
        return True
    else: return False

def on_mouse_scroll(tobj, x, y, dx, dy, dbg=1):
    retv = True
    if dbg: slog(f'{fxy(x, y)} {fxy(dx, dy)} {retv=} {tobj}')
    return retv

def on_mouse_motion(tobj, x, y, dx, dy, dbg=1):
    retv = True
    if dbg: slog(f'{fxy(x, y)} {fxy(dx, dy)} {retv=} {tobj}')
    return retv
########################################################################################################################################################################################################
def on_move(tobj, x, y, dbg=1):
    retv = True
    if dbg: slog(f'{fxy(x, y)} {retv=} {tobj}')
    return True

#def on_resize(tobj, width, height, dbg=1):
#    super(type(tobj), tobj).on_resize(width, height)
#    if tobj.RESIZE: tobj.resizeTniks(dbg)
#    return True
########################################################################################################################################################################################################
def on_text(tobj, text, dbg=1):
    retv = True
    tkb  = tobj.keyboard
    kd   = tkb.data if tkb else None
    if dbg: slog(f'BGN {ft(text)} swapping={ tobj.swapping}')
    if      tobj.shiftingTabs:               cmd = cmds.ShiftTabsCmd(tobj, 'onTxt', text)                ;  cmd.do()
    elif    tobj.jumping:                    cmd = cmds.CsrJumpCmd(  tobj, 'onTxt', text, tobj.jumpAbs)  ;  cmd.do()
    elif    tobj.inserting:                  tobj.insertSpace('onTxt', text)
    elif    tobj.settingN:                   tobj.setn_cmd(   'onTxt', text)
    elif    tobj.swapping:                   cmd = cmds.SwapTabCmd(  tobj, 'onTxt', text)                ;  cmd.do()
    elif    tobj.isTab(text):                tobj.setTab(     'onTxt', text)
    elif    text == '$' and isShf(kd, MODS): tobj.snapshot(f'{text}', 'SNAP')
    else:   slog(f'UNH {ft(text)}', f=-2) if dbg else None   ;   retv = False
    if dbg: slog(f'END {ft(text)} swapping={ tobj.swapping} {retv=}')
    return retv
########################################################################################################################################################################################################
def on_text_motion(tobj, motion, dbg=1):
    assert tobj
    retv = True
    tkb  = tobj.keyboard
    kd   = tkb.data if tkb else None
    k    = pygwink    ;    m = MODS
    p, l, s, c, t = tobj.j()  ;  np, nl, ns, nc, nt = tobj.n
    if dbg: slog(f'BGN {ftm(motion)}')
    if   isNumLck(kd, m):                          msg =             f'NUMLOCK(        {motion})'   ;   slog(msg)   ;   k.MOD_NUMLOCK = 0
    if   isCtlAltShf(kd, m):                       msg =             f'@&^(            {motion})'   ;   slog(msg)   ;   retv = False # self.quit(msg)
    elif isCtlAlt(kd, m):
        if   motion == 1:                          tobj.unselectTabs(f'@& LEFT(        {motion})',  nt)
        elif motion == 2:                          tobj.unselectTabs(f'@& RIGHT(       {motion})', -nt)
        else:                                      msg =             f'@& UNH(         {motion})'   ;   slog(msg)   ;   retv = False # self.quit(msg)
    elif isAltShf(kd, m):                          msg =             f' &^(            {motion})'   ;   slog(msg)   ;   retv = False # self.quit(msg)
    elif isCtlShf(kd, m):                          msg =             f'@^(             {motion})'   ;   slog(msg)   ;   retv = False # self.quit(msg)
    elif isShf(kd, m):                             msg =             f'^ (             {motion})'   ;   slog(msg)   ;   retv = False # self.quit(msg)
    elif isCtl(kd, m):
        if   motion == k.MOTION_UP:                msg = f'MOTION_UP  ({motion})'   ;    slog(msg)   ;   retv = False
        elif motion == k.MOTION_DOWN:              msg = f'MOTION_DOWN({motion})'   ;    slog(msg)   ;   retv = False
        elif motion == k.MOTION_NEXT_WORD:         tobj.selectTabs(  f'@  RIGHT(       {motion})',  nt)
        elif motion == k.MOTION_PREVIOUS_WORD:     tobj.selectTabs(  f'@  LEFT(        {motion})', -nt)
        elif motion == k.MOTION_BEGINNING_OF_FILE: msg = f'@  MOTION_BEGINNING_OF_FILE({motion} CTRL HOME)'  ;   slog(msg)   ;   retv = False # tobj.quit(msg) # CTRL HOME
        elif motion == k.MOTION_END_OF_FILE:       msg = f'@  MOTION_END_OF_FILE(      {motion} CTRL END)'   ;   slog(msg)   ;   retv = False # tobj.quit(msg) # CTRL END
        elif motion == k.MOTION_BEGINNING_OF_LINE: msg = f'@  MOTION_BEGINNING_OF_LINE({motion})'   ;   slog(msg)   ;   retv = False # tobj.quit(msg) # N/A
        elif motion == k.MOTION_END_OF_LINE:       msg = f'@  MOTION_END_OF_LINE(      {motion})'   ;   slog(msg)   ;   retv = False # tobj.quit(msg) # N/A
        elif motion == k.MOTION_PREVIOUS_PAGE:     msg = f'@  MOTION_PREVIOUS_PAGE(    {motion})'   ;   slog(msg)   ;   retv = False # tobj.quit(msg) # N/A
        elif motion == k.MOTION_NEXT_PAGE:         msg = f'@ MOTION_NEXT_PAGE(         {motion})'   ;   slog(msg)   ;   retv = False
#            cmd = tobj.NextPageCmd(tobj, '@  MOTION_NEXT_PAGE', motion)   ;  cmd.do()     
        elif motion == k.MOTION_DELETE:            tobj.deleteTabs(f'@ D MOTION_DELETE({motion})')
        elif motion == k.MOTION_COPY:              tobj.copyTabs(  f'@ C MOTION_COPY(  {motion})')
        elif motion == k.MOTION_PASTE:             tobj.pasteTabs( f'@ V MOTION_PASTE( {motion})', kk=0)
        else:                                      msg = f'@  UNH CTRL(                {motion})'   ;   slog(msg)   ;   retv = False # self.quit(msg)
    elif isAlt(kd, m):
        if   motion == k.MOTION_UP:                tobj.moveUp(      f' & UP(          {motion})')
        elif motion == k.MOTION_DOWN:              tobj.moveDown(    f' & DOWN(        {motion})')
        elif motion == k.MOTION_LEFT:              tobj.moveLeft(    f' & LEFT(        {motion})')
        elif motion == k.MOTION_RIGHT:             tobj.moveRight(   f' & RIGHT(       {motion})')
        elif motion == k.MOTION_BEGINNING_OF_LINE: tobj.move(        f' & HOME(        {motion})', -nt *  c)
        elif motion == k.MOTION_END_OF_LINE:       tobj.move(        f' & END(         {motion})',  nt * (nc - tobj.i[C]))
        elif motion == k.MOTION_PREVIOUS_PAGE:     tobj.prevPage(    f' & PAGE UP(     {motion})')
        elif motion == k.MOTION_NEXT_PAGE:         tobj.nextPage(    f' & PAGE DOWN(   {motion})')
        else:                                      msg =             f' & UNH(         {motion})'   ;   slog(msg)   ;   retv = False # tobj.quit(msg)
    else:
        if   motion == k.MOTION_UP:                tobj.move(        f' UP(            {motion})', -1)
        elif motion == k.MOTION_DOWN:              tobj.move(        f' DOWN(          {motion})',  1)
        elif motion == k.MOTION_LEFT:              tobj.move(        f' LEFT(          {motion})', -nt)
        elif motion == k.MOTION_RIGHT:             tobj.move(        f' RIGHT(         {motion})',  nt)
        elif motion == k.MOTION_BEGINNING_OF_LINE: tobj.move(        f' HOME(          {motion})', -nt *  c)
        elif motion == k.MOTION_END_OF_LINE:       tobj.move(        f' END(           {motion})',  nt * (nc - tobj.i[C]))
        elif motion == k.MOTION_PREVIOUS_PAGE:     tobj.moveUp(      f' PAGE UP(       {motion})')  # go up   to top    of line, wrap down to bottom of prev line
#        elif motion == k.MOTION_NEXT_PAGE:         tobj.moveDown(    f' PAGE DOWN(     {motion})')  # go down to bottom tab on same line, wrap to next line
        elif motion == k.MOTION_NEXT_PAGE:         
            msg = f' MOTION_NEXT_PAGE(     {motion})'  ;   slog(msg)   ;   retv = False
        elif motion == k.MOTION_DELETE:            tobj.setTab(      f'DELETE(         {motion})', tobj.tblank)
        elif motion == k.MOTION_BACKSPACE:         tobj.setTab(      f'BACKSPACE(      {motion})', tobj.tblank, rev=1)
        elif motion == k.MOTION_PREVIOUS_WORD:     msg = f'MOTION_PREVIOUS_WORD(       {motion})'   ;   slog(msg)   ;   retv = False # tobj.quit(msg) # N/A
        elif motion == k.MOTION_NEXT_WORD:         msg = f'MOTION_NEXT_WORD(           {motion})'   ;   slog(msg)   ;   retv = False # tobj.quit(msg) # N/A
        elif motion == k.MOTION_BEGINNING_OF_FILE: msg = f'MOTION_BEGINNING_OF_FILE(   {motion})'   ;   slog(msg)   ;   retv = False # tobj.quit(msg) # N/A
        elif motion == k.MOTION_END_OF_FILE:       msg = f'MOTION_END_OF_FILE(         {motion})'   ;   slog(msg)   ;   retv = False # tobj.quit(msg) # N/A
#        else:                                      msg =             f'UNH(            {motion})'   ;   slog(msg)   ;   retv = False  ;  tobj.quit(msg)
    if dbg: slog(f'END {ftm(motion)} {retv=}')
    return retv
########################################################################################################################################################################################################
