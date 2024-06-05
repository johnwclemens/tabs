from   inspect import currentframe as cfrm
import pyglet
import pyglet.window.key     as pygwink
from   pyglet.window.key import symbol_string    as psym
from   pyglet.window.key import modifiers_string as pmod
from   pyglet.window.key import motion_string    as pmtn
import pyglet.window.mouse   as pygmous
from   tpkg import utl
from   tpkg import cmds
#from   tpkg import tests

slog, fmtf, fmtl, fmtm         = utl.slog, utl.fmtf, utl.fmtl, utl.fmtm
X, W, Y, Z                     = utl.X, utl.W, utl.Y, utl.Z
TT, NN, II, KK                 = utl.TT, utl.NN, utl.II, utl.KK
MLDY, CHRD, ARPG               = utl.MLDY, utl.CHRD, utl.ARPG
LARROW, RARROW, DARROW, UARROW = utl.LARROW, utl.RARROW, utl.DARROW, utl.UARROW
BOLD, COLOR, ITALIC, FONT_NAME, FONT_SIZE                                = utl.BOLD, utl.COLOR, utl.ITALIC, utl.FONT_NAME, utl.FONT_SIZE
P, L, S, C, T, N, I, K, R, Q, H, M, A, B, D, E                           = utl.P, utl.L, utl.S, utl.C, utl.T, utl.N, utl.I, utl.K, utl.R, utl.Q, utl.H, utl.M, utl.A, utl.B, utl.D, utl.E
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
    if   tobj.DRAW_BGC % 3 == 0:     pyglet.gl.glClearColor(0.0, 0.0, 0.0, 0.0)
    elif tobj.DRAW_BGC % 3 == 1:     pyglet.gl.glClearColor(0.5, 0.5, 0.5, 0.5)
    elif tobj.DRAW_BGC % 3 == 2:     pyglet.gl.glClearColor(1.0, 1.0, 1.0, 1.0)
    tobj.clear()
    tobj.batch.draw()
    if  tobj.SNAPS and tobj.snapReqQ.qsize():
        _    = fmtm(kwargs) if kwargs else Z
        qlen = tobj.snapReqQ.qsize()
        snapReq  = tobj.snapReqQ.get(False)
        cmd  = cmds.SnapshotCmd(tobj, snapReq[0], snapReq[1], snapReq[2])  ;  snapPath = cmd.do()
        slog(f'{tobj.LOG_ID=:3} sid={snapReq[0]} typ={snapReq[1]} why={snapReq[2]} {qlen=}\n{snapPath}', f=-3)
#    else: slog(f'{kwargs=}') if kwargs else slog()
#        if tobj.TEST:   tests.testSprTxt_0(snapPath)
########################################################################################################################################################################################################
def on_key_press(tobj, symb, mods, dbg=1):
    assert tobj
    retv, retv2  = True, False
    global MODS      ;    MODS = mods
    fontBold, fontItalic = tobj.fontBold, tobj.fontItalic
    k     = psym(symb)   ;   m = MODS
    dp    = tobj.dataPath1
    hc    = tobj.hcurs
    tkb   = tobj.keyboard
    d     = tkb.data if tkb else None
    assert d,  f'{d=} {tkb=}'
    if dbg:           slog(f'BGN {fsm(symb, mods)} {d=}', f=-3)
    if   k == 'P' and isCtlAlt(d, m):      cmd = cmds.PlayCmd(         tobj, '@&P')                  ;  cmd.do()
    elif k == 'S' and isCtlAlt(d, m):      cmd = cmds.SaveDataFileCmd( tobj, '@&S', tobj.dataPath1)  ;  cmd.do()
    ####################################################################################################################################################################################################
    elif k == 'A' and isCtlShf(d, m):      cmd = cmds.TogArrowCmd(     tobj, '@^A', v=1)            ;  cmd.do()
    elif k == 'A' and isCtl(   d, m):      cmd = cmds.TogArrowCmd(     tobj, '@ A', v=0)            ;  cmd.do()
    elif k == 'B' and isCtlShf(d, m):      cmd = cmds.TogBlankCmd(     tobj, '@^B', -1)             ;  cmd.do()
    elif k == 'B' and isCtl(   d, m):      cmd = cmds.TogBlankCmd(     tobj, '@ B',  1)             ;  cmd.do()
    elif k == 'C' and isCtlShf(d, m):      cmd = cmds.CopyTabsCmd(     tobj, '@^C')                 ;  cmd.do() # todo fixme also fires MOTION_COPY
    elif k == 'C' and isCtl(   d, m):      cmd = cmds.CopyTabsCmd(     tobj, '@ C')                 ;  cmd.do() # todo fixme also fires MOTION_COPY
    elif k == 'D' and isCtlShf(d, m):      cmd = cmds.DeleteTabsCmd(   tobj, '@^D')                 ;  cmd.do()
    elif k == 'D' and isCtl(   d, m):      cmd = cmds.DeleteTabsCmd(   tobj, '@ D')                 ;  cmd.do()
    elif k == 'E' and isCtlShf(d, m):      cmd = cmds.EraseTabsCmd(    tobj, '@^E')                 ;  cmd.do()
    elif k == 'E' and isCtl(   d, m):      cmd = cmds.EraseTabsCmd(    tobj, '@ E')                 ;  cmd.do()
    elif k == 'F' and isCtlShf(d, m):      cmd = cmds.TogFlatShrpCmd(  tobj, '@^F')                 ;  cmd.do()
    elif k == 'F' and isCtl(   d, m):      cmd = cmds.TogFlatShrpCmd(  tobj, '@ F')                 ;  cmd.do()
    elif k == 'G' and isCtlShf(d, m):      cmd = cmds.Go2FirstTabCmd(  tobj, '@^G', page=1)         ;  cmd.do()
    elif k == 'G' and isCtl(   d, m):      cmd = cmds.Go2FirstTabCmd(  tobj, '@ G', page=0)         ;  cmd.do()
    elif k == 'H' and isCtlShf(d, m):      cmd = cmds.Go2LastTabCmd(   tobj, '@^H', page=1)         ;  cmd.do()
    elif k == 'H' and isCtl(   d, m):      cmd = cmds.Go2LastTabCmd(   tobj, '@ H', page=0)         ;  cmd.do()
    elif k == 'I' and isCtlShf(d, m):      cmd = cmds.TogTTsCmd(       tobj, '@^I', II)             ;  cmd.do()
    elif k == 'I' and isCtl(   d, m):      cmd = cmds.TogTTsCmd(       tobj, '@ I', II)             ;  cmd.do()
    elif k == 'J' and isCtlShf(d, m):      cmd = cmds.CsrJumpCmd(      tobj, '@^J', txt='0', ab=1)  ;  cmd.do()
    elif k == 'J' and isCtl(   d, m):      cmd = cmds.CsrJumpCmd(      tobj, '@ J', txt='0', ab=0)  ;  cmd.do()
    elif k == 'K' and isCtlShf(d, m):      cmd = cmds.TogTTsCmd(       tobj, '@^K', KK)             ;  cmd.do()
    elif k == 'K' and isCtl(   d, m):      cmd = cmds.TogTTsCmd(       tobj, '@ K', KK)             ;  cmd.do()
    elif k == 'L' and isCtlShf(d, m):      cmd = cmds.TogLLsCmd(       tobj, '@^L')                 ;  cmd.do()
    elif k == 'L' and isCtl(   d, m):      cmd = cmds.TogLLsCmd(       tobj, '@ L')                 ;  cmd.do()
    elif k == 'M' and isCtlShf(d, m):      cmd = cmds.CopyKordNamesCmd(tobj, '@^M')                 ;  cmd.do()
    elif k == 'M' and isCtl(   d, m):      cmd = cmds.CopyKordNamesCmd(tobj, '@ M')                 ;  cmd.do()
    elif k == 'N' and isCtlShf(d, m):      cmd = cmds.TogTTsCmd(       tobj, '@^N', NN)             ;  cmd.do()
    elif k == 'N' and isCtl(   d, m):      cmd = cmds.TogTTsCmd(       tobj, '@ N', NN)             ;  cmd.do()
    elif k == 'O' and isCtlShf(d, m):      cmd = cmds.TogCsrModeCmd(   tobj, '@^O', -1)             ;  cmd.do()
    elif k == 'O' and isCtl(   d, m):      cmd = cmds.TogCsrModeCmd(   tobj, '@ O',  1)             ;  cmd.do()
    elif k == 'P' and isCtlShf(d, m):      cmd = cmds.AddPageCmd(      tobj, '@^P', ins=0)          ;  cmd.do()
    elif k == 'P' and isCtl(   d, m):      cmd = cmds.AddPageCmd(      tobj, '@ P', ins=None)       ;  cmd.do()
    elif k == 'Q' and isCtlShf(d, m):      cmd = cmds.QuitCmd(         tobj, '@^Q', err=0, save=0)  ;  retv2 = cmd.do()
    elif k == 'Q' and isCtl(   d, m):      cmd = cmds.QuitCmd(         tobj, '@ Q', err=0, save=1)  ;  retv2 = cmd.do()
    elif k == 'R' and isCtlShf(d, m):      cmd = cmds.TogKordNamesCmd( tobj, '@^R', hit=1)          ;  cmd.do()
    elif k == 'R' and isCtl(   d, m):      cmd = cmds.TogKordNamesCmd( tobj, '@ R', hit=0)          ;  cmd.do()
    elif k == 'S' and isCtlShf(d, m):      cmd = cmds.SaveDataFileCmd( tobj, '@^S', dp)             ;  cmd.do()
    elif k == 'S' and isCtl(   d, m):      cmd = cmds.SaveDataFileCmd( tobj, '@ S', dp)             ;  cmd.do()
    elif k == 'T' and isCtlShf(d, m):      cmd = cmds.TogTTsCmd(       tobj, '@^T', TT)             ;  cmd.do()
    elif k == 'T' and isCtl(   d, m):      cmd = cmds.TogTTsCmd(       tobj, '@ T', TT)             ;  cmd.do()
    elif k == 'U' and isCtlShf(d, m):      cmd = cmds.ResetCmd(        tobj, '@^U')                 ;  cmd.do()
    elif k == 'U' and isCtl(   d, m):      cmd = cmds.ResetCmd(        tobj, '@ U')                 ;  cmd.do()
    elif k == 'V' and isCtlShf(d, m):      cmd = cmds.PasteTabsCmd(    tobj, '@^V', kk=1)           ;  cmd.do() # todo fixme also fires MOTION_PASTE
    elif k == 'V' and isCtl(   d, m):      cmd = cmds.PasteTabsCmd(    tobj, '@ V', kk=0)           ;  cmd.do() # todo fixme also fires MOTION_PASTE
    elif k == 'W' and isCtlShf(d, m):      cmd = cmds.SwapColsCmd(     tobj, '@^W')                 ;  cmd.do()
    elif k == 'W' and isCtl(   d, m):      cmd = cmds.SwapColsCmd(     tobj, '@ W')                 ;  cmd.do()
    elif k == 'X' and isCtlShf(d, m):      cmd = cmds.CutTabsCmd(      tobj, '@^X')                 ;  cmd.do()
    elif k == 'X' and isCtl(   d, m):      cmd = cmds.CutTabsCmd(      tobj, '@ X')                 ;  cmd.do()
    elif k == 'Y' and isCtlShf(d, m):      cmd = cmds.InsertSpaceCmd(  tobj, '@^Y')                 ;  cmd.do()
    elif k == 'Y' and isCtl(   d, m):      cmd = cmds.InsertSpaceCmd(  tobj, '@ Y')                 ;  cmd.do()
    elif k == 'Z' and isCtlShf(d, m):      cmd = cmds.TogZZsCmd(       tobj, '@^Z', 1)              ;  cmd.do()
    elif k == 'Z' and isCtl(   d, m):      cmd = cmds.TogZZsCmd(       tobj, '@ Z', 0)              ;  cmd.do()
    ####################################################################################################################################################################################################
    elif k == 'D' and isAltShf(d, m):      cmd = cmds.TogDrwBGCCmd(    tobj, '&^D', -1)             ;  cmd.do()
    elif k == 'D' and isAlt(   d, m):      cmd = cmds.TogDrwBGCCmd(    tobj, '& D',  1)             ;  cmd.do()
    elif k == 'E' and isAltShf(d, m):      cmd = cmds.TogBGCCmd(       tobj, '&^E')                 ;  cmd.do()
    elif k == 'E' and isAlt(   d, m):      cmd = cmds.TogBGCCmd(       tobj, '& E')                 ;  cmd.do()
    elif k == 'F' and isAltShf(d, m):      cmd = cmds.TogFullScrnCmd(  tobj, '&^F')                 ;  cmd.do()
    elif k == 'F' and isAlt(   d, m):      cmd = cmds.TogFullScrnCmd(  tobj, '& F')                 ;  cmd.do()
    elif k == 'J' and isAltShf(d, m):      cmd = cmds.TogAXYVCmd(      tobj, '&^J', 0, -1)          ;  cmd.do()
    elif k == 'J' and isAlt(   d, m):      cmd = cmds.TogAXYVCmd(      tobj, '& J', 0,  1)          ;  cmd.do()
    elif k == 'K' and isAltShf(d, m):      cmd = cmds.TogAXYVCmd(      tobj, '&^K', 1, -1)          ;  cmd.do()
    elif k == 'K' and isAlt(   d, m):      cmd = cmds.TogAXYVCmd(      tobj, '& K', 1,  1)          ;  cmd.do()
    elif k == 'L' and isAltShf(d, m):      cmd = cmds.TogAXYVCmd(      tobj, '&^L', 2, -1)          ;  cmd.do()
    elif k == 'L' and isAlt(   d, m):      cmd = cmds.TogAXYVCmd(      tobj, '& L', 2,  1)          ;  cmd.do()
    elif k == 'M' and isAltShf(d, m):      cmd = cmds.TogAXYVCmd(      tobj, '&^M', 3, -1)          ;  cmd.do()
    elif k == 'M' and isAlt(   d, m):      cmd = cmds.TogAXYVCmd(      tobj, '& M', 3,  1)          ;  cmd.do()
    elif k == 'N' and isAltShf(d, m):      cmd = cmds.SetNCmd(         tobj, '&^N', txt=Z)          ;  cmd.do()
    elif k == 'N' and isAlt(   d, m):      cmd = cmds.SetNCmd(         tobj, '& N', txt=Z)          ;  cmd.do()
    elif k == 'P' and isAltShf(d, m):      cmd = cmds.TogPageCmd(      tobj, '&^P', -1)             ;  cmd.do()
    elif k == 'P' and isAlt   (d, m):      cmd = cmds.TogPageCmd(      tobj, '& P',  1)             ;  cmd.do()
    elif k == 'R' and isAltShf(d, m):      cmd = cmds.RotSprCmd(       tobj, '&^R', hc[0], -1)      ;  cmd.do()
    elif k == 'R' and isAlt(   d, m):      cmd = cmds.RotSprCmd(       tobj, '& R', hc[0],  1)      ;  cmd.do()
    elif k == 'S' and isAltShf(d, m):      cmd = cmds.ShiftTabsCmd(    tobj, '&^S')                 ;  cmd.do()
    elif k == 'S' and isAlt(   d, m):      cmd = cmds.ShiftTabsCmd(    tobj, '& S')                 ;  cmd.do()
    elif k == 'V' and isAltShf(d, m):      cmd = cmds.TogVisibleCmd(   tobj, '&^V')                 ;  cmd.do()
    elif k == 'V' and isAlt(   d, m):      cmd = cmds.TogVisibleCmd(   tobj, '& V')                 ;  cmd.do()
    elif k == 'W' and isAltShf(d, m):      cmd = cmds.SwapTabCmd(      tobj, '&^W', txt=Z)          ;  cmd.do()
    elif k == 'W' and isAlt(   d, m):      cmd = cmds.SwapTabCmd(      tobj, '& W', txt=Z)          ;  cmd.do()
    elif k == 'Z' and isAltShf(d, m):      cmd = cmds.UpdateTniksCmd(  tobj, '&^Z', tobj.width, tobj.height)   ;  cmd.do()
    elif k == 'Z' and isAlt(   d, m):      cmd = cmds.UpdateTniksCmd(  tobj, '& Z', tobj.width, tobj.height)   ;  cmd.do()
    ####################################################################################################################################################################################################
    elif k == 'B' and isAltShf(d, m):      cmd = cmds.SetFontArgCmd(   tobj, '&^B', BOLD,      not fontBold,   'fontBold')     ;  cmd.do()
    elif k == 'B' and isAlt(   d, m):      cmd = cmds.SetFontArgCmd(   tobj, '& B', BOLD,      not fontBold,   'fontBold')     ;  cmd.do()
    elif k == 'C' and isAltShf(d, m):      cmd = cmds.SetFontArgCmd(   tobj, '&^C', COLOR,        -1,          'clrIdx')       ;  cmd.do()
    elif k == 'C' and isAlt(   d, m):      cmd = cmds.SetFontArgCmd(   tobj, '& C', COLOR,         1,          'clrIdx')       ;  cmd.do()
    elif k == 'I' and isAltShf(d, m):      cmd = cmds.SetFontArgCmd(   tobj, '&^I', ITALIC,    not fontItalic, 'fontItalic')   ;  cmd.do()
    elif k == 'I' and isAlt(   d, m):      cmd = cmds.SetFontArgCmd(   tobj, '& I', ITALIC,    not fontItalic, 'fontItalic')   ;  cmd.do()
    elif k == 'A' and isAltShf(d, m):      cmd = cmds.SetFontArgCmd(   tobj, '&^A', FONT_NAME,    -1,          'fontNameIdx')  ;  cmd.do()
    elif k == 'A' and isAlt(   d, m):      cmd = cmds.SetFontArgCmd(   tobj, '& A', FONT_NAME,     1,          'fontNameIdx')  ;  cmd.do()
    elif k == 'Y' and isAltShf(d, m):      cmd = cmds.SetFontArgCmd(   tobj, '&^Y', FONT_SIZE,     15 / 16,    'fontSize')     ;  cmd.do()
    elif k == 'Y' and isAlt(   d, m):      cmd = cmds.SetFontArgCmd(   tobj, '& Y', FONT_SIZE,     16 / 15,    'fontSize')     ;  cmd.do()
    ####################################################################################################################################################################################################
#   elif k == 'LEFT'   and isCtlShf(d, m): cmd = cmds.TogPageCmd(      tobj, '@ ^LEFT', -1)         ;  cmd.do()
#   elif k == 'LEFT'   and isCtl(   d, m): cmd = cmds.TogPageCmd(      tobj, '@  LEFT',  1)         ;  cmd.do()
#   elif k == 'LEFT':                      cmd = cmds.MoveUpCmd(       tobj, '   LEFT')             ;  cmd.do() # go up   to top    of line, wrap down to bottom of prev line
#   elif k == 'RIGHT'  and isCtlShf(d, m): cmd = cmds.TogPageCmd(      tobj, '@ ^RIGHT', -1)        ;  cmd.do()
#   elif k == 'RIGHT'  and isCtl(   d, m): cmd = cmds.TogPageCmd(      tobj, '@  RIGHT',  1)        ;  cmd.do()
#   elif k == 'RIGHT':                     cmd = cmds.MoveDownCmd(     tobj, '   RIGHT')            ;  cmd.do() # go down to bottom tab on same line, wrap to next line
    elif k == 'ESCAPE':                    cmd = cmds.TogSelectAllCmd( tobj, '   ESCAPE')           ;  cmd.do()
    elif k == 'TAB'       and isShf(d, m): cmd = cmds.SetCHVModeCmd(   tobj, '  ^TAB',       MLDY, LARROW)             ;  cmd.do()
    elif k == 'TAB':                       cmd = cmds.SetCHVModeCmd(   tobj, '   TAB',       MLDY, RARROW)             ;  cmd.do()
    elif k == 'SLASH'     and isCtl(d, m): cmd = cmds.SetCHVModeCmd(   tobj, '@  SLASH',     ARPG, RARROW, UARROW)     ;  cmd.do()
    elif k == 'SLASH'     and isAlt(d, m): cmd = cmds.SetCHVModeCmd(   tobj, ' & SLASH',     ARPG, LARROW, DARROW)     ;  cmd.do()
    elif k == 'BACKSLASH' and isCtl(d, m): cmd = cmds.SetCHVModeCmd(   tobj, '@  BACKSLASH', ARPG, RARROW, DARROW)     ;  cmd.do()
    elif k == 'BACKSLASH' and isAlt(d, m): cmd = cmds.SetCHVModeCmd(   tobj, ' & BACKSLASH', ARPG, LARROW, UARROW)     ;  cmd.do()
    ####################################################################################################################################################################################################
    else:
        slog(f'UNH          {k=} {retv=} setting retv to False', f=-3) if dbg else None
        retv = False
    ####################################################################################################################################################################################################
    if not retv2:
        retv = retv2
        slog(f'UNH {retv2=} {k=} {retv=} {fsm(symb, mods)} {d=}', f=-3) if dbg else None
    ####################################################################################################################################################################################################
    slog(f'check isParsing {k=} {retv=}', f=-3)
    if  not  tobj.isParsing():
        slog(f'Not isParsing {k=} {retv=}', f=-3)
        if   k == 'ENTER' and isShf(d, m):      cmd = cmds.SetCHVModeCmd(tobj, '  ^ENTER', CHRD, v=DARROW)  ;  tobj.prevEvntText = k  ;  cmd.do()
        elif k == 'ENTER':                      cmd = cmds.SetCHVModeCmd(tobj, '   ENTER', CHRD, v=UARROW)  ;  tobj.prevEvntText = k  ;  cmd.do()
        elif k == 'SPACE' and tobj.tblank != W: cmd = cmds.AutoMoveCmd(  tobj, '   SPACE')                                            ;  cmd.do() # todo
#        elif dbg: self.log(f'Unexpected {self.kbkEvntTxt()} while not parsing', f=2)
        else: slog(f'Done Not isParsing {k=} {retv=}', f=-3)
    slog(f'{d=} {tkb=}', f=-3)
    if dbg:   slog(f'END {fsm(symb, mods)} {d=}', f=-3)
    slog(f'END processing event {k=} return {retv=}', f=-3)
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
        p  = tobj.j()[P]  ;   l = a           ;     s = d//nt            ;   c = b          ;  t = d - l*nr #) % nt
        txt = tobj.tabls[cc].text if cc < tlen else Z   ;   f = -3
        if dbg:   slog(f'BGN {x=:4} {y0=:4} {y=:4} {w=:6.2f} {h=:6.2f} {ll=} {nc=:2} {nr=:2} {r=:2} {d=:2} {txt=} {bttn=} {mods=}', f=f)
        if dbg:   slog(f'    p={p+1} l={l+1}=(d/nr) s={s+1}=(d//nt) c={c+1}=(x/w) t={t+1}=(d-l*nr)', f=f)
        if dbg:   slog(f'    before MOVE plsct={tobj.fplsct(p, l, s, c, t)}',   f=f)
        p, l, s, c, t = tobj.moveTo('MOUSE RELEASE', p, l, s, c, t)
        if dbg:   slog(f'    after  MOVE plsct={tobj.fplsct(p, l, s, c, t)}',   f=f)
        if dbg:   slog(f'END {fxy(x, y)} {y0:4} ({ww:4}x{hh:4})  {fbm(bttn, mods)}', f=f)
        return True
    return False

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

def on_resize(tobj, w, h, z, dbg=1):
    assert z in (0, 1, None),  f'{z=}'
    if tobj.RESIZE:
        cmd = cmds.UpdateTniksCmd(tobj, 'on_resize()', w, h, z, dbg)     ;  cmd.do()
    return True
#    super(type(tobj), tobj).on_resize(width, height)
#    if tobj.RESIZE: tobj.resizeTniks(dbg)
#    return True
########################################################################################################################################################################################################
def on_text(tobj, text, dbg=1):
    retv  = True
    tkb   = tobj.keyboard
    kd    = tkb.data if tkb else None
    if   dbg: slog(f'BGN {ft(text)} {tobj.prevEvntText=} {tobj.inserting=} {tobj.jumping=} {tobj.settingN=} {tobj.shifting=} {tobj.swapping=}')
    if      tobj.inserting:                  cmd = cmds.InsertSpaceCmd(tobj,  'onTxt', text)                ;  cmd.do()
    elif    tobj.jumping:                    cmd = cmds.CsrJumpCmd(    tobj,  'onTxt', text, tobj.jumpAbs)  ;  cmd.do()
    elif    tobj.settingN:                   cmd = cmds.SetNCmd(       tobj,  'onTxt', text)                ;  cmd.do()
    elif    tobj.shifting:                   cmd = cmds.ShiftTabsCmd(  tobj,  'onTxt', text)                ;  cmd.do()
    elif    tobj.swapping:                   cmd = cmds.SwapTabCmd(    tobj,  'onTxt', text)                ;  cmd.do()
    elif    tobj.isTab(text):                cmd = cmds.SetTabCmd(     tobj,  'onTxt', text)                ;  cmd.do()
    elif    text=='$' and isShf(kd, MODS): tobj.snpC += 1  ;  cmd = cmds.SnapshotCmd(tobj, tobj.snpC, f'SNP.{tobj.snpC}', text)    ;  cmd.do()
    elif dbg: slog(f'UNH {ft(text)} {tobj.prevEvntText=}', f=-3) if text != '\r' and tobj.prevEvntText != 0xff0d else None   ;   retv = False # 65293
    tobj.prevEvntText = text
    if   dbg: slog(f'END {ft(text)} {tobj.prevEvntText=} {tobj.inserting=} {tobj.jumping=} {tobj.settingN=} {tobj.shifting=} {tobj.swapping=} {retv=}')
    return retv
########################################################################################################################################################################################################
def on_text_motion(tobj, motion, dbg=1):
    assert tobj
    retv = True
    tkb  = tobj.keyboard
    kd   = tkb.data if tkb else None
    k    = pygwink    ;    n = MODS   ;   m = motion
    p, l, s, c, t = tobj.j()  ;  np, nl, ns, nc, nt = tobj.n
    tb = tobj.tblank  ;   c2 = nc - tobj.i[C]
    if dbg: slog(f'BGN {ftm(m)}')
    if   isNumLck(kd, n):                     msg =                            f'NUMLOCK(     {m})'             ;  slog(msg)   ;   k.MOD_NUMLOCK = 0
    if   isCtlAltShf(kd, n):                  msg =                            f'@&^(         {m})'             ;  slog(msg)   ;   retv = False # self.quit(msg)
    elif isCtlAlt(kd, n):
        if   m == k.MOTION_NEXT_WORD:         cmd = cmds.UnselectTabsCmd(tobj, f'@& RIGHT(    {m})',  nt)       ;  cmd.do()
        elif m == k.MOTION_PREVIOUS_WORD:     cmd = cmds.UnselectTabsCmd(tobj, f'@& LEFT(     {m})', -nt)       ;  cmd.do()
        else:                                 msg =                            f'@& UNH(      {m})'             ;  slog(msg)   ;   retv = False # self.quit(msg)
    elif isAltShf(kd, n):                     msg =                            f' &^(         {m})'             ;  slog(msg)   ;   retv = False # self.quit(msg)
    elif isCtlShf(kd, n):                     msg =                            f'@ ^(         {m})'             ;  slog(msg)   ;   retv = False # self.quit(msg)
    elif isShf(kd, n):                        msg =                            f'  ^(         {m})'             ;  slog(msg)   ;   retv = False # self.quit(msg)
    elif isCtl(kd, n):
        if   m == k.MOTION_UP:                msg =                            f'@  UP  (     {m})'             ;  slog(msg)   ;   retv = False
        elif m == k.MOTION_DOWN:              msg =                            f'@  DOWN(     {m})'             ;  slog(msg)   ;   retv = False
        elif m == k.MOTION_RIGHT:             msg =                            f'@  RIGHT(    {m})'             ;  slog(msg)   ;   retv = False
        elif m == k.MOTION_LEFT:              msg =                            f'@  LEFT(     {m})'             ;  slog(msg)   ;   retv = False
        elif m == k.MOTION_NEXT_PAGE:         cmd = cmds.TogPageCmd(     tobj, f'@  PAGEDOWN( {m})',  1)        ;  cmd.do()
        elif m == k.MOTION_PREVIOUS_PAGE:     cmd = cmds.TogPageCmd(     tobj, f'@  PAGEUP(   {m})', -1)        ;  cmd.do() # ;   slog(msg)   ;   retv = False # tobj.quit(msg) # N/A
        elif m == k.MOTION_BACKSPACE:         cmd = cmds.DeleteTabsCmd(  tobj, f'@  BACKSPACE({m})')            ;  cmd.do() # todo fixme
        elif m == k.MOTION_DELETE:            cmd = cmds.DeleteTabsCmd(  tobj, f'@  DELETE(   {m})')            ;  cmd.do()
        elif m == k.MOTION_NEXT_WORD:         cmd = cmds.SelectTabsCmd(  tobj, f'@  RIGHT(    {m})',  nt)       ;  cmd.do()
        elif m == k.MOTION_PREVIOUS_WORD:     cmd = cmds.SelectTabsCmd(  tobj, f'@  LEFT(     {m})', -nt)       ;  cmd.do()
        elif m == k.MOTION_BEGINNING_OF_LINE: msg =                            f'@  HOME(     {m})'             ;  slog(msg)   ;   retv = False # tobj.quit(msg) # N/A
        elif m == k.MOTION_END_OF_LINE:       msg =                            f'@  END(      {m})'             ;  slog(msg)   ;   retv = False # tobj.quit(msg) # N/A
        elif m == k.MOTION_BEGINNING_OF_FILE: msg =                            f'@  BGN_FILE( {m})'             ;  slog(msg)   ;   retv = False # tobj.quit(msg) # CTRL HOME
        elif m == k.MOTION_END_OF_FILE:       msg =                            f'@  END_FILE( {m})'             ;  slog(msg)   ;   retv = False # tobj.quit(msg) # CTRL END
        elif m == k.MOTION_COPY:              cmd = cmds.CopyTabsCmd(    tobj, f'@  COPY(     {m})')            ;  cmd.do() # todo fixme also fires '@ C'
        elif m == k.MOTION_PASTE:             cmd = cmds.PasteTabsCmd(   tobj, f'@  PASTE(    {m})', kk=0)      ;  cmd.do() # todo fixme also fires '@ V'
        else:                                 msg =                            f'@  UNH CTRL( {m})'             ;  slog(msg)   ;   retv = False  ;  cmd = cmds.QuitCmd(tobj, msg)  ;  cmd.do()
    elif isAlt(kd, n):
        if   m == k.MOTION_UP:                cmd = cmds.MoveUpCmd(      tobj, f' & UP(       {m})')            ;  cmd.do()
        elif m == k.MOTION_DOWN:              cmd = cmds.MoveUpCmd(      tobj, f' & DOWN(     {m})')            ;  cmd.do()
        elif m == k.MOTION_RIGHT:             cmd = cmds.MoveRightCmd(   tobj, f' & RIGHT(    {m})')            ;  cmd.do()
        elif m == k.MOTION_LEFT:              cmd = cmds.MoveLeftCmd(    tobj, f' & LEFT(     {m})')            ;  cmd.do()
        elif m == k.MOTION_NEXT_PAGE:         cmd = cmds.NextPageCmd(    tobj, f' & PAGEDOWN( {m})')            ;  cmd.do()
        elif m == k.MOTION_PREVIOUS_PAGE:     cmd = cmds.PrevPageCmd(    tobj, f' & PAGEUP(   {m})')            ;  cmd.do()
        elif m == k.MOTION_BACKSPACE:         cmd = cmds.DeleteTabsCmd(  tobj, f' & BACKSPACE({m})')            ;  cmd.do() # todo fixme
        elif m == k.MOTION_DELETE:            cmd = cmds.DeleteTabsCmd(  tobj, f' & DELETE(   {m})')            ;  cmd.do()
        elif m == k.MOTION_NEXT_WORD:         msg =                            f' & NEXT WORD({m})'             ;  slog(msg)   ;   retv = False # tobj.quit(msg) # N/A
        elif m == k.MOTION_PREVIOUS_WORD:     msg =                            f' & PREV WORD({m})'             ;  slog(msg)   ;   retv = False # tobj.quit(msg) # N/A
        elif m == k.MOTION_BEGINNING_OF_LINE: cmd = cmds.MoveCmd(        tobj, f' & HOME(     {m})', -nt*c)     ;  cmd.do()
        elif m == k.MOTION_END_OF_LINE:       cmd = cmds.MoveCmd(        tobj, f' & END(      {m})',  nt*c2)    ;  cmd.do()
        elif m == k.MOTION_BEGINNING_OF_FILE: msg =                            f' & BGN FILE( {m})'             ;  slog(msg)   ;   retv = False # tobj.quit(msg) # N/A
        elif m == k.MOTION_END_OF_FILE:       msg =                            f' & END FILE( {m})'             ;  slog(msg)   ;   retv = False # tobj.quit(msg) # N/A
        elif m == k.MOTION_COPY:              msg =                            f' & COPY(     {m})'             ;  slog(msg)   ;   retv = False  ;  cmd = cmds.QuitCmd(tobj, msg)  ;  cmd.do()
        elif m == k.MOTION_PASTE:             msg =                            f' & PASTE(    {m})'             ;  slog(msg)   ;   retv = False  ;  cmd = cmds.QuitCmd(tobj, msg)  ;  cmd.do()
        else:                                 msg =                            f' & UNH(      {m})'             ;  slog(msg)   ;   retv = False  ;  cmd = cmds.QuitCmd(tobj, msg)  ;  cmd.do()
    else:
        if   m == k.MOTION_UP:                cmd = cmds.MoveCmd(        tobj, f'   UP(       {m})', -1)        ;  cmd.do()
        elif m == k.MOTION_DOWN:              cmd = cmds.MoveCmd(        tobj, f'   DOWN(     {m})',  1)        ;  cmd.do()
        elif m == k.MOTION_RIGHT:             cmd = cmds.MoveCmd(        tobj, f'   RIGHT(    {m})',  nt)       ;  cmd.do()
        elif m == k.MOTION_LEFT:              cmd = cmds.MoveCmd(        tobj, f'   LEFT(     {m})', -nt)       ;  cmd.do()
        elif m == k.MOTION_NEXT_PAGE:         cmd = cmds.MoveDownCmd(    tobj, f'   PAGEDOWN( {m})')            ;  cmd.do() # go down to bottom tab on same line, wrap to next line
        elif m == k.MOTION_PREVIOUS_PAGE:     cmd = cmds.MoveUpCmd(      tobj, f'   PAGEUP(   {m})')            ;  cmd.do() # go up   to top    of line, wrap down to bottom of prev line
        elif m == k.MOTION_BACKSPACE:         cmd = cmds.SetTabCmd(      tobj, f'   BACKSPACE({m})', tb, m, 1)  ;  cmd.do()
        elif m == k.MOTION_DELETE:            cmd = cmds.SetTabCmd(      tobj, f'   DELETE(   {m})', tb)        ;  cmd.do()
        elif m == k.MOTION_NEXT_WORD:         msg =                            f'   NEXT WORD({m})'             ;  slog(msg)   ;   retv = False # tobj.quit(msg) # N/A
        elif m == k.MOTION_PREVIOUS_WORD:     msg =                            f'   PREV WORD({m})'             ;  slog(msg)   ;   retv = False # tobj.quit(msg) # N/A
        elif m == k.MOTION_BEGINNING_OF_LINE: cmd = cmds.MoveCmd(        tobj, f'   HOME(     {m})', -nt*c)     ;  cmd.do()
        elif m == k.MOTION_END_OF_LINE:       cmd = cmds.MoveCmd(        tobj, f'   END(      {m})',  nt*c2)    ;  cmd.do()
        elif m == k.MOTION_BEGINNING_OF_FILE: msg =                            f'   BGN FILE( {m})'             ;  slog(msg)   ;   retv = False # tobj.quit(msg) # N/A
        elif m == k.MOTION_END_OF_FILE:       msg =                            f'   END FILE( {m})'             ;  slog(msg)   ;   retv = False # tobj.quit(msg) # N/A
        elif m == k.MOTION_COPY:              msg =                            f'   COPY(     {m})'             ;  slog(msg)   ;   retv = False  ;  cmd = cmds.QuitCmd(tobj, msg)  ;  cmd.do()
        elif m == k.MOTION_PASTE:             msg =                            f'   PASTE(    {m})'             ;  slog(msg)   ;   retv = False  ;  cmd = cmds.QuitCmd(tobj, msg)  ;  cmd.do()
        else:                                 msg =                            f'   UNH(      {m})'             ;  slog(msg)   ;   retv = False  ;  cmd = cmds.QuitCmd(tobj, msg)  ;  cmd.do()
    if dbg: slog(f'END {ftm(m)} {retv=}')
    return retv
########################################################################################################################################################################################################
