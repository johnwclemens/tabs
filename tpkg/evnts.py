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
    if  tobj.SNAPS and tobj.snapReg:
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
    hc    = tobj.hcurs
    tkb   = tobj.keyboard
    kd    = tkb.data if tkb else None
    kbk   = psym(symb)   ;   m = MODS
    dp    = tobj.dataPath1
    if dbg:    slog(f'BGN {fsm(symb, mods)} kd={fmtm(kd)}')
    if   kbk == 'A' and isCtlShf(kd, m):      cmd = cmds.TogArrowCmd(     tobj, '@^A', v=1)          ;  cmd.do()
    elif kbk == 'A' and isCtl(   kd, m):      cmd = cmds.TogArrowCmd(     tobj, '@ A', v=0)          ;  cmd.do()
    elif kbk == 'B' and isCtlShf(kd, m):      cmd = cmds.TogBlankCmd(     tobj, '@^B', -1)           ;  cmd.do()
    elif kbk == 'B' and isCtl(   kd, m):      cmd = cmds.TogBlankCmd(     tobj, '@ B',  1)           ;  cmd.do()
    elif kbk == 'C' and isCtlShf(kd, m):      cmd = cmds.CopyTabsCmd(     tobj, '@^C')               ;  cmd.do() # todo fixme also fires MOTION_COPY
    elif kbk == 'C' and isCtl(   kd, m):      cmd = cmds.CopyTabsCmd(     tobj, '@ C')               ;  cmd.do() # todo fixme also fires MOTION_COPY
    elif kbk == 'D' and isCtlShf(kd, m):      cmd = cmds.DeleteTabsCmd(   tobj, '@^D')               ;  cmd.do()
    elif kbk == 'D' and isCtl(   kd, m):      cmd = cmds.DeleteTabsCmd(   tobj, '@ D')               ;  cmd.do()
    elif kbk == 'E' and isCtlShf(kd, m):      cmd = cmds.EraseTabsCmd(    tobj, '@^E')               ;  cmd.do()
    elif kbk == 'E' and isCtl(   kd, m):      cmd = cmds.EraseTabsCmd(    tobj, '@ E')               ;  cmd.do()
    elif kbk == 'F' and isCtlShf(kd, m):      cmd = cmds.TogFullScrnCmd(  tobj, '@^F')               ;  cmd.do()
    elif kbk == 'F' and isCtl(   kd, m):      cmd = cmds.TogFlatShrpCmd(  tobj, '@ F')               ;  cmd.do()
    elif kbk == 'G' and isCtlShf(kd, m):      cmd = cmds.Go2FirstTabCmd(  tobj, '@^G', page=1)       ;  cmd.do()
    elif kbk == 'G' and isCtl(   kd, m):      cmd = cmds.Go2FirstTabCmd(  tobj, '@ G', page=0)       ;  cmd.do()
    elif kbk == 'H' and isCtlShf(kd, m):      cmd = cmds.Go2LastTabCmd(   tobj, '@^H', page=1)       ;  cmd.do()
    elif kbk == 'H' and isCtl(   kd, m):      cmd = cmds.Go2LastTabCmd(   tobj, '@ H', page=0)       ;  cmd.do()
    elif kbk == 'I' and isCtlShf(kd, m):      cmd = cmds.InsertSpaceCmd(  tobj, '@^I')               ;  cmd.do() #
    elif kbk == 'I' and isCtl(   kd, m):      cmd = cmds.TogTTsCmd(       tobj, '@ I', II)           ;  cmd.do() #
    elif kbk == 'J' and isCtlShf(kd, m):      cmd = cmds.CsrJumpCmd(      tobj, '@^J', txt='0', abso=1)  ;  cmd.do()
    elif kbk == 'J' and isCtl(   kd, m):      cmd = cmds.CsrJumpCmd(      tobj, '@ J', txt='0', abso=0)  ;  cmd.do()
    elif kbk == 'K' and isCtlShf(kd, m):      cmd = cmds.TogTTsCmd(       tobj, '@^K', KK)           ;  cmd.do()
    elif kbk == 'K' and isCtl(   kd, m):      cmd = cmds.TogTTsCmd(       tobj, '@ K', KK)           ;  cmd.do()
    elif kbk == 'L' and isCtlShf(kd, m):      cmd = cmds.TogLLsCmd(       tobj, '@^L')               ;  cmd.do()
    elif kbk == 'L' and isCtl(   kd, m):      cmd = cmds.TogLLsCmd(       tobj, '@ L')               ;  cmd.do()
    elif kbk == 'M' and isCtlShf(kd, m):      tobj.flipZZs(      '@^M', 1)
    elif kbk == 'M' and isCtl(   kd, m):      tobj.flipZZs(      '@ M', 0)
    elif kbk == 'N' and isCtlShf(kd, m):      cmd = cmds.TogTTsCmd(       tobj, '@^N', NN)           ;  cmd.do()
    elif kbk == 'N' and isCtl(   kd, m):      cmd = cmds.TogTTsCmd(       tobj, '@ N', NN)           ;  cmd.do()
    elif kbk == 'O' and isCtlShf(kd, m):      cmd = cmds.TogCsrModeCmd(   tobj, '@^O', -1)           ;  cmd.do()
    elif kbk == 'O' and isCtl(   kd, m):      cmd = cmds.TogCsrModeCmd(   tobj, '@ O',  1)           ;  cmd.do()
    elif kbk == 'P' and isCtlShf(kd, m):      cmd = cmds.AddPageCmd(      tobj, '@^P', ins=0)        ;  cmd.do()
    elif kbk == 'P' and isCtl(   kd, m):      cmd = cmds.AddPageCmd(      tobj, '@ P', ins=None)     ;  cmd.do()
    elif kbk == 'Q' and isCtlShf(kd, m):      retv = tobj.quit(  '@^Q', error=0, save=0)
    elif kbk == 'Q' and isCtl(   kd, m):      retv = tobj.quit(  '@ Q', error=0, save=1)
    elif kbk == 'R' and isCtlShf(kd, m):      cmd = cmds.TogKordNamesCmd( tobj, '@^R', hit=1)        ;  cmd.do()
    elif kbk == 'R' and isCtl(   kd, m):      cmd = cmds.TogKordNamesCmd( tobj, '@ R', hit=0)        ;  cmd.do()
    elif kbk == 'S' and isCtlShf(kd, m):      cmd = cmds.SaveDataFileCmd( tobj, '@^S', dp)           ;  cmd.do()
    elif kbk == 'S' and isCtl(   kd, m):      cmd = cmds.SaveDataFileCmd( tobj, '@ S', dp)           ;  cmd.do()
    elif kbk == 'T' and isCtlShf(kd, m):      cmd = cmds.TogTTsCmd(       tobj, '@^T', TT)           ;  cmd.do()
    elif kbk == 'T' and isCtl(   kd, m):      cmd = cmds.TogTTsCmd(       tobj, '@ T', TT)           ;  cmd.do()
    elif kbk == 'U' and isCtlShf(kd, m):      cmd = cmds.ResetCmd(        tobj, '@^U')               ;  cmd.do()
    elif kbk == 'U' and isCtl(   kd, m):      cmd = cmds.ResetCmd(        tobj, '@ U')               ;  cmd.do()
#   elif kbk == 'V' and isCtlAlt(kd, m):      cmd = cmds.PasteTabsCmd(    tobj, '@&V', hc=0, kk=1)   ;  cmd.do()
    elif kbk == 'V' and isCtlShf(kd, m):      cmd = cmds.PasteTabsCmd(    tobj, '@^V', kk=1)         ;  cmd.do() # todo fixme also fires MOTION_PASTE
    elif kbk == 'V' and isCtl(   kd, m):      cmd = cmds.PasteTabsCmd(    tobj, '@ V', kk=0)         ;  cmd.do() # todo fixme also fires MOTION_PASTE
    elif kbk == 'W' and isCtlShf(kd, m):      cmd = cmds.SwapColsCmd(     tobj, '@^W')               ;  cmd.do()
    elif kbk == 'W' and isCtl(   kd, m):      cmd = cmds.SwapColsCmd(     tobj, '@ W')               ;  cmd.do()
    elif kbk == 'X' and isCtlShf(kd, m):      cmd = cmds.CutTabsCmd(      tobj, '@^X')               ;  cmd.do()
    elif kbk == 'X' and isCtl(   kd, m):      cmd = cmds.CutTabsCmd(      tobj, '@ X')               ;  cmd.do()
    ####################################################################################################################################################################################################
    elif kbk == 'A' and isAltShf(kd, m):      cmd = cmds.TogBGCCmd(       tobj, '&^A')               ;  cmd.do()
    elif kbk == 'A' and isAlt(   kd, m):      cmd = cmds.TogBGCCmd(       tobj, '& A')               ;  cmd.do()
    elif kbk == 'D' and isAltShf(kd, m):      cmd = cmds.TogDrwBGCCmd(    tobj, '&^D', -1)           ;  cmd.do()
    elif kbk == 'D' and isAlt(   kd, m):      cmd = cmds.TogDrwBGCCmd(    tobj, '& D',  1)           ;  cmd.do()
    elif kbk == 'N' and isAltShf(kd, m):      cmd = cmds.SetNCmd(         tobj, '&^N', txt=Z)        ;  cmd.do()
    elif kbk == 'N' and isAlt(   kd, m):      cmd = cmds.SetNCmd(         tobj, '& N', txt=Z)        ;  cmd.do()
    elif kbk == 'P' and isAltShf(kd, m):      cmd = cmds.TogPageCmd(      tobj, '&^P', -1)           ;  cmd.do()
    elif kbk == 'P' and isAlt   (kd, m):      cmd = cmds.TogPageCmd(      tobj, '& P',  1)           ;  cmd.do()
    elif kbk == 'R' and isAltShf(kd, m):      cmd = cmds.RotSprCmd(       tobj, '&^R', hc[0], -1)    ;  cmd.do()
    elif kbk == 'R' and isAlt(   kd, m):      cmd = cmds.RotSprCmd(       tobj, '& R', hc[0],  1)    ;  cmd.do()
    elif kbk == 'S' and isAltShf(kd, m):      cmd = cmds.SwapTabCmd(      tobj, '@ S', txt=Z)        ;  cmd.do() #
    elif kbk == 'S' and isAlt(kd, m):         cmd = cmds.ShiftTabsCmd(    tobj, '@^S')               ;  cmd.do() #
    elif kbk == 'V' and isAltShf(kd, m):      cmd = cmds.TogVisibleCmd(   tobj, '&^V')               ;  cmd.do()
    elif kbk == 'V' and isAlt(kd, m):         cmd = cmds.TogVisibleCmd(   tobj, '& V')               ;  cmd.do() 
    elif kbk == 'Z' and isAltShf(kd, m):      tobj.RESIZE = not tobj.RESIZE   ;  tobj.resizeTniks(dbg=1)
    elif kbk == 'Z' and isAlt(   kd, m):                                         tobj.resizeTniks(dbg=1)
    ####################################################################################################################################################################################################
    elif kbk == 'B' and isAltShf(kd, m):      cmd = cmds.SetFontPrmCmd(   tobj, BOLD,      not fontBold,   'fontBold')     ;  cmd.do()
    elif kbk == 'B' and isAlt(   kd, m):      cmd = cmds.SetFontPrmCmd(   tobj, BOLD,      not fontBold,   'fontBold')     ;  cmd.do()
    elif kbk == 'C' and isAltShf(kd, m):      cmd = cmds.SetFontPrmCmd(   tobj, COLOR,        -1,          'clrIdx')       ;  cmd.do()
    elif kbk == 'C' and isAlt(   kd, m):      cmd = cmds.SetFontPrmCmd(   tobj, COLOR,         1,          'clrIdx')       ;  cmd.do()
    elif kbk == 'I' and isAltShf(kd, m):      cmd = cmds.SetFontPrmCmd(   tobj, ITALIC,    not fontItalic, 'fontItalic')   ;  cmd.do()
    elif kbk == 'I' and isAlt(   kd, m):      cmd = cmds.SetFontPrmCmd(   tobj, ITALIC,    not fontItalic, 'fontItalic')   ;  cmd.do()
    elif kbk == 'M' and isAltShf(kd, m):      cmd = cmds.SetFontPrmCmd(   tobj, FONT_NAME,    -1,          'fontNameIdx')  ;  cmd.do()
    elif kbk == 'M' and isAlt(   kd, m):      cmd = cmds.SetFontPrmCmd(   tobj, FONT_NAME,     1,          'fontNameIdx')  ;  cmd.do()
    elif kbk == 'Y' and isAltShf(kd, m):      cmd = cmds.SetFontPrmCmd(   tobj, FONT_SIZE,     33 / 32,    'fontSize')     ;  cmd.do()
    elif kbk == 'Y' and isAlt(   kd, m):      cmd = cmds.SetFontPrmCmd(   tobj, FONT_SIZE,     32 / 33,    'fontSize')     ;  cmd.do()
    ####################################################################################################################################################################################################
#   elif kbk == 'LEFT'   and isCtlShf(kd, m): cmd = cmds.TogPageCmd(      tobj, '@ ^LEFT', -1)           ;  cmd.do()
#   elif kbk == 'LEFT'   and isCtl(   kd, m): cmd = cmds.TogPageCmd(      tobj, '@  LEFT',  1)           ;  cmd.do()
#   elif kbk == 'LEFT':                       cmd = cmds.MoveUpCmd(       tobj, '   LEFT')               ;  cmd.do() # go up   to top    of line, wrap down to bottom of prev line
#   elif kbk == 'RIGHT'  and isCtlShf(kd, m): cmd = cmds.TogPageCmd(      tobj, '@ ^RIGHT', -1)          ;  cmd.do()
#   elif kbk == 'RIGHT'  and isCtl(   kd, m): cmd = cmds.TogPageCmd(      tobj, '@  RIGHT',  1)          ;  cmd.do()
#   elif kbk == 'RIGHT':                      cmd = cmds.MoveDownCmd(     tobj, '   RIGHT')              ;  cmd.do() # go down to bottom tab on same line, wrap to next line
    elif kbk == 'ESCAPE':                     cmd = cmds.TogSelectAllCmd( tobj, '   ESCAPE')             ;  cmd.do()
    elif kbk == 'TAB'  and isCtl(kd, m):      cmd = cmds.SetCHVModeCmd(   tobj, '@  TAB', MELODY, LARROW)                 ;  cmd.do()
    elif kbk == 'TAB':                        cmd = cmds.SetCHVModeCmd(   tobj, '   TAB', MELODY, RARROW)                 ;  cmd.do()
    elif kbk == 'SLASH'     and isCtl(kd, m): cmd = cmds.SetCHVModeCmd(   tobj, '@  SLASH',     ARPG, RARROW, UARROW)     ;  cmd.do()
    elif kbk == 'SLASH'     and isAlt(kd, m): cmd = cmds.SetCHVModeCmd(   tobj, ' & SLASH',     ARPG, LARROW, DARROW)     ;  cmd.do()
    elif kbk == 'BACKSLASH' and isCtl(kd, m): cmd = cmds.SetCHVModeCmd(   tobj, '@  BACKSLASH', ARPG, RARROW, DARROW)     ;  cmd.do()
    elif kbk == 'BACKSLASH' and isAlt(kd, m): cmd = cmds.SetCHVModeCmd(   tobj, ' & BACKSLASH', ARPG, LARROW, UARROW)     ;  cmd.do()
    ####################################################################################################################################################################################################
    else:  retv = False   ;   slog(f'UNH {fsm(symb, mods)} kd={fmtm(kd)}') if dbg else None
    ####################################################################################################################################################################################################
    if  not  tobj.isParsing():
        if   kbk == 'ENTER' and isCtl(kd, m):     cmd = cmds.SetCHVModeCmd(tobj, '@ ENTER', CHORD, v=DARROW)  ;  cmd.do()
        elif kbk == 'ENTER':                      cmd = cmds.SetCHVModeCmd(tobj, '  ENTER', CHORD, v=UARROW)  ;  cmd.do()
        elif kbk == 'SPACE' and tobj.tblank != W: cmd = cmds.AutoMoveCmd(  tobj, '  SPACE')                   ;  cmd.do() # todo
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
    retv  = True
    tkb   = tobj.keyboard
    kd    = tkb.data if tkb else None
    if dbg: slog(f'BGN {ft(text)} swapping={ tobj.swapping}')
    if      tobj.inserting:                  cmd = cmds.InsertSpaceCmd(tobj, 'onTxt', text)                ;  cmd.do()
    elif    tobj.jumping:                    cmd = cmds.CsrJumpCmd(    tobj, 'onTxt', text, tobj.jumpAbs)  ;  cmd.do()
    elif    tobj.settingN:                   cmd = cmds.SetNCmd(       tobj, 'onTxt', text)                ;  cmd.do()
    elif    tobj.shifting:                   cmd = cmds.ShiftTabsCmd(  tobj, 'onTxt', text)                ;  cmd.do()
    elif    tobj.swapping:                   cmd = cmds.SwapTabCmd(    tobj, 'onTxt', text)                ;  cmd.do()
    elif    tobj.isTab(text):                cmd = cmds.SetTabCmd(     tobj, 'onTxt', text)                ;  cmd.do()
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
    tb = tobj.tblank  ;   c2 = nc - tobj.i[C]
    if dbg: slog(f'BGN {ftm(motion)}')
    if   isNumLck(kd, m):                          msg =                            f'NUMLOCK(     {motion})'             ;  slog(msg)   ;   k.MOD_NUMLOCK = 0
    if   isCtlAltShf(kd, m):                       msg =                            f'@&^(         {motion})'             ;  slog(msg)   ;   retv = False # self.quit(msg)
    elif isCtlAlt(kd, m):
        if   motion == k.MOTION_NEXT_WORD:         cmd = cmds.UnselectTabsCmd(tobj, f'@& RIGHT(    {motion})',  nt)       ;  cmd.do()
        elif motion == k.MOTION_PREVIOUS_WORD:     cmd = cmds.UnselectTabsCmd(tobj, f'@& LEFT(     {motion})', -nt)       ;  cmd.do()
        else:                                      msg =                            f'@& UNH(      {motion})'             ;  slog(msg)   ;   retv = False # self.quit(msg)
    elif isAltShf(kd, m):                          msg =                            f' &^(         {motion})'             ;  slog(msg)   ;   retv = False # self.quit(msg)
    elif isCtlShf(kd, m):                          msg =                            f'@ ^(         {motion})'             ;  slog(msg)   ;   retv = False # self.quit(msg)
    elif isShf(kd, m):                             msg =                            f'  ^(         {motion})'             ;  slog(msg)   ;   retv = False # self.quit(msg)
    elif isCtl(kd, m):
        if   motion == k.MOTION_UP:                msg =                            f'@  UP  (     {motion})'             ;  slog(msg)   ;   retv = False
        elif motion == k.MOTION_RIGHT:             msg =                            f'@  RIGHT(    {motion})'             ;  slog(msg)   ;   retv = False
        elif motion == k.MOTION_DOWN:              msg =                            f'@  DOWN(     {motion})'             ;  slog(msg)   ;   retv = False
        elif motion == k.MOTION_LEFT:              msg =                            f'@  LEFT(     {motion})'             ;  slog(msg)   ;   retv = False
        elif motion == k.MOTION_NEXT_PAGE:         cmd = cmds.TogPageCmd(     tobj, f'@  PAGEDOWN( {motion})',  1)        ;  cmd.do()     
        elif motion == k.MOTION_PREVIOUS_PAGE:     cmd = cmds.TogPageCmd(     tobj, f'@  PAGEUP(   {motion})', -1)        ;  cmd.do() # ;   slog(msg)   ;   retv = False # tobj.quit(msg) # N/A
        elif motion == k.MOTION_BACKSPACE:         cmd = cmds.DeleteTabsCmd(  tobj, f'@  BACKSPACE({motion})')            ;  cmd.do() # todo fixme
        elif motion == k.MOTION_DELETE:            cmd = cmds.DeleteTabsCmd(  tobj, f'@  DELETE(   {motion})')            ;  cmd.do()
        elif motion == k.MOTION_NEXT_WORD:         cmd = cmds.SelectTabsCmd(  tobj, f'@  RIGHT(    {motion})',  nt)       ;  cmd.do()
        elif motion == k.MOTION_PREVIOUS_WORD:     cmd = cmds.SelectTabsCmd(  tobj, f'@  LEFT(     {motion})', -nt)       ;  cmd.do()
        elif motion == k.MOTION_BEGINNING_OF_LINE: msg =                            f'@  HOME(     {motion})'             ;  slog(msg)   ;   retv = False # tobj.quit(msg) # N/A
        elif motion == k.MOTION_END_OF_LINE:       msg =                            f'@  END(      {motion})'             ;  slog(msg)   ;   retv = False # tobj.quit(msg) # N/A
        elif motion == k.MOTION_BEGINNING_OF_FILE: msg =                            f'@  BGN_FILE( {motion})'             ;  slog(msg)   ;   retv = False # tobj.quit(msg) # CTRL HOME
        elif motion == k.MOTION_END_OF_FILE:       msg =                            f'@  END_FILE( {motion})'             ;  slog(msg)   ;   retv = False # tobj.quit(msg) # CTRL END
        elif motion == k.MOTION_COPY:              cmd = cmds.CopyTabsCmd(    tobj, f'@  COPY(     {motion})')            ;  cmd.do() # todo fixme also fires '@ C'
        elif motion == k.MOTION_PASTE:             cmd = cmds.PasteTabsCmd(   tobj, f'@  PASTE(    {motion})', kk=0)      ;  cmd.do() # todo fixme also fires '@ V'
        else:                                      msg =                            f'@  UNH CTRL( {motion})'             ;  slog(msg)   ;   retv = False # self.quit(msg)
    elif isAlt(kd, m):
        if   motion == k.MOTION_UP:                cmd = cmds.MoveUpCmd(      tobj, f' & UP(       {motion})')            ;  cmd.do()
        elif motion == k.MOTION_RIGHT:             cmd = cmds.MoveRightCmd(   tobj, f' & RIGHT(    {motion})')            ;  cmd.do()
        elif motion == k.MOTION_DOWN:              cmd = cmds.MoveUpCmd(      tobj, f' & DOWN(     {motion})')            ;  cmd.do()
        elif motion == k.MOTION_LEFT:              cmd = cmds.MoveLeftCmd(    tobj, f' & LEFT(     {motion})')            ;  cmd.do()
        elif motion == k.MOTION_NEXT_PAGE:         cmd = cmds.NextPageCmd(    tobj, f' & PAGEDOWN( {motion})')            ;  cmd.do()
        elif motion == k.MOTION_PREVIOUS_PAGE:     cmd = cmds.PrevPageCmd(    tobj, f' & PAGEUP(   {motion})')            ;  cmd.do()
        elif motion == k.MOTION_BACKSPACE:         cmd = cmds.DeleteTabsCmd(  tobj, f' & BACKSPACE({motion})')            ;  cmd.do() # todo fixme
        elif motion == k.MOTION_DELETE:            cmd = cmds.DeleteTabsCmd(  tobj, f' & DELETE(   {motion})')            ;  cmd.do()
        elif motion == k.MOTION_NEXT_WORD:         msg =                            f' & NEXT WORD({motion})'             ;  slog(msg)   ;   retv = False # tobj.quit(msg) # N/A
        elif motion == k.MOTION_PREVIOUS_WORD:     msg =                            f' & PREV WORD({motion})'             ;  slog(msg)   ;   retv = False # tobj.quit(msg) # N/A
        elif motion == k.MOTION_BEGINNING_OF_LINE: cmd = cmds.MoveCmd(        tobj, f' & HOME(     {motion})', -nt*c)     ;  cmd.do()
        elif motion == k.MOTION_END_OF_LINE:       cmd = cmds.MoveCmd(        tobj, f' & END(      {motion})',  nt*c2)    ;  cmd.do()
        elif motion == k.MOTION_BEGINNING_OF_FILE: msg =                            f' & BGN FILE( {motion})'             ;  slog(msg)   ;   retv = False # tobj.quit(msg) # N/A
        elif motion == k.MOTION_END_OF_FILE:       msg =                            f' & END FILE( {motion})'             ;  slog(msg)   ;   retv = False # tobj.quit(msg) # N/A
        elif motion == k.MOTION_COPY:              msg =                            f' & COPY(     {motion})'             ;  slog(msg)   ;   retv = False
        elif motion == k.MOTION_PASTE:             msg =                            f' & PASTE(    {motion})'             ;  slog(msg)   ;   retv = False
        else:                                      msg =                            f' & UNH(      {motion})'             ;  slog(msg)   ;   retv = False # tobj.quit(msg)
    else:
        if   motion == k.MOTION_UP:                cmd = cmds.MoveCmd(        tobj, f'   UP(       {motion})', -1)        ;  cmd.do()
        elif motion == k.MOTION_RIGHT:             cmd = cmds.MoveCmd(        tobj, f'   RIGHT(    {motion})',  nt)       ;  cmd.do()
        elif motion == k.MOTION_DOWN:              cmd = cmds.MoveCmd(        tobj, f'   DOWN(     {motion})',  1)        ;  cmd.do()
        elif motion == k.MOTION_LEFT:              cmd = cmds.MoveCmd(        tobj, f'   LEFT(     {motion})', -nt)       ;  cmd.do()
        elif motion == k.MOTION_NEXT_PAGE:         cmd = cmds.MoveDownCmd(    tobj, f'   PAGEDOWN( {motion})')            ;  cmd.do() # go down to bottom tab on same line, wrap to next line
        elif motion == k.MOTION_PREVIOUS_PAGE:     cmd = cmds.MoveUpCmd(      tobj, f'   PAGEUP(   {motion})')            ;  cmd.do() # go up   to top    of line, wrap down to bottom of prev line
        elif motion == k.MOTION_BACKSPACE:         cmd = cmds.SetTabCmd(      tobj, f'   BACKSPACE({motion})', tb, rev=1) ;  cmd.do()
        elif motion == k.MOTION_DELETE:            cmd = cmds.SetTabCmd(      tobj, f'   DELETE(   {motion})', tb)        ;  cmd.do()
        elif motion == k.MOTION_NEXT_WORD:         msg =                            f'   NEXT WORD({motion})'             ;  slog(msg)   ;   retv = False # tobj.quit(msg) # N/A
        elif motion == k.MOTION_PREVIOUS_WORD:     msg =                            f'   PREV WORD({motion})'             ;  slog(msg)   ;   retv = False # tobj.quit(msg) # N/A
        elif motion == k.MOTION_BEGINNING_OF_LINE: cmd = cmds.MoveCmd(        tobj, f'   HOME(     {motion})', -nt*c)     ;  cmd.do()
        elif motion == k.MOTION_END_OF_LINE:       cmd = cmds.MoveCmd(        tobj, f'   END(      {motion})',  nt*c2)    ;  cmd.do()
        elif motion == k.MOTION_BEGINNING_OF_FILE: msg =                            f'   BGN FILE( {motion})'             ;  slog(msg)   ;   retv = False # tobj.quit(msg) # N/A
        elif motion == k.MOTION_END_OF_FILE:       msg =                            f'   END FILE( {motion})'             ;  slog(msg)   ;   retv = False # tobj.quit(msg) # N/A
        elif motion == k.MOTION_COPY:              msg =                            f'   COPY(     {motion})'             ;  slog(msg)   ;   retv = False
        elif motion == k.MOTION_PASTE:             msg =                            f'   PASTE(    {motion})'             ;  slog(msg)   ;   retv = False
        else:                                      msg =                            f'   UNH(      {motion})'             ;  slog(msg)   ;   retv = False # ;  tobj.quit(msg)
    if dbg: slog(f'END {ftm(motion)} {retv=}')
    return retv
########################################################################################################################################################################################################
