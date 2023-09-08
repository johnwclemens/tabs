from inspect import currentframe as cfrm
import pyglet
#import pyglet.text         as text
#import pyglet.window       as window
##import pyglet.window.event as pygwevnt
##import pyglet.event        as pygevnt
import pyglet.window.key   as pygwink
from pyglet.window.key import symbol_string    as psyms
from pyglet.window.key import modifiers_string as pmods
from pyglet.window.key import motion_string    as pmtns
import pyglet.window.mouse as pygmous
from   tpkg import utl     as utl

slog, fmtf, fmtl, fmtm         = utl.slog, utl.fmtf, utl.fmtl, utl.fmtm
W, Y, Z                        = utl.W, utl.Y, utl.Z
TT, NN, II, KK                 = utl.TT, utl.NN, utl.II, utl.KK
MELODY, CHORD, ARPG            = utl.MELODY, utl.CHORD, utl.ARPG
LARROW, RARROW, DARROW, UARROW = utl.LARROW, utl.RARROW, utl.DARROW, utl.UARROW
BOLD, COLOR, ITALIC, FONT_NAME, FONT_SIZE                                = utl.BOLD, utl.COLOR, utl.ITALIC, utl.FONT_NAME, utl.FONT_SIZE
P, L, S, C, T, N, I, K, R, Q, H, M, B, A, D, E                           = utl.P, utl.L, utl.S, utl.C, utl.T, utl.N, utl.I, utl.K, utl.R, utl.Q, utl.H, utl.M, utl.B, utl.A, utl.D, utl.E
isAlt, isCtl, isShf, isAltShf, isCtlAlt, isCtlShf, isCtlAltShf, isNumLck = utl.isAlt, utl.isCtl, utl.isCtlAlt, utl.isShf, utl.isAltShf, utl.isCtlShf, utl.isCtlAltShf, utl.isNumLck

MODS  = 0
FLIST = []

def flog(msg, fd=None, filt=None):
    if (filt and filt not in FLIST) or not filt:
        slog(f'{msg} {filt=}', f=fd)

#def fMov(x, y):              return f'{x=} {y=}'
def fTxt(   text):           return f'{text=}'
def fTxtMtn(motion):         return f'{motion=}'
def fKbk(   symb, mods):     return f'{symb=}={psyms(symb)} {mods=}={pmods(mods)}'
def fMmov(x, y, dx, dy):     return f'{x=} {y=} {dx=} {dy=}'
def fMclk(x, y, bttn, mods): return f'{x=} {y=} {bttn=} {mods=}={pmods(mods)}'
def fn(cf):                  return cf.f_code.co_name

########################################################################################################################################################################################################

class FilteredEventLogger(pyglet.window.event.WindowEventLogger):
    def __init__(self, tobj, fd=None, flst=None):
        super().__init__(fd)
        self.tobj = tobj
        global FLIST   ;   FLIST = flst

    def on_draw(self, **kwargs):
        flog(f'{kwargs=}', filt=fn(cfrm()))

    def on_move(self, x, y):
        flog(f'{x=} {y=}', filt=fn(cfrm()))

    def on_mouse_motion(self, x, y, dx, dy):
        flog(f'{x=} {y=} {dx=} {dy=}', filt=fn(cfrm()))

    def on_mouse_scroll(self, x, y, dx, dy):
        flog(f'{x=} {y=} {dx=} {dy=}', filt=fn(cfrm()))

    def on_mouse_press(self, x, y, bttn, mods=0):
        flog(f'{x=} {y=} {bttn=} {mods=}', filt=fn(cfrm()))

    def on_mouse_release(self, x, y, bttn, mods=0):
        flog(f'{x=} {y=} {bttn=} {mods=}', filt=fn(cfrm()))

    def on_key_press(self, symb, mods):
        flog(f'{symb=} {psyms(symb)} {mods=} {pmods(mods)}', filt=fn(cfrm()))
#        flog(f'{symb=} {mods=} {pygwink.symbol_string(symb)} {pygwink.modifiers_string(mods)}', filt=fn(cfrm()))

    def on_key_release(self, symb, mods):
        flog(f'{symb=} {psyms(symb)} {mods=} {pmods(mods)}', filt=fn(cfrm()))
#        flog(f'{symb=} {mods=} {pygwink.symbol_string(symb)} {pygwink.modifiers_string(mods)}', filt=fn(cfrm()))

    def on_text(self, text):
        flog(f'{text=}', filt=fn(cfrm()))

    def on_text_motion(self, motion):
        flog(f'{motion=} {pmtns(motion)}', filt=fn(cfrm()))

########################################################################################################################################################################################################
########################################################################################################################################################################################################

def on_move(x, y):
    slog(f'{x=} {y=} retv=True')    ;    return True

def on_mouse_release(tobj, x, y, bttn, mods=0, dbg=1):
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
        if dbg:   slog(f'END {x=:4} {y0=:4} {y=:4} {ww=:6.2f} {hh=:6.2f}',      f=f)
        return True
    else: return False

def on_mouse_scroll(x, y, dx, dy):
    slog(f'{x=} {y=} {dx=} {dy=} retv=True')    ;    return True

def on_text(tobj, text, dbg=1):
    retv = True
    if dbg: slog(f'BGN {fTxt(text)} swapping={tobj.swapping}')
    if      tobj.shiftingTabs:                tobj.shiftTabs(  'onTxt', text)
    elif    tobj.jumping:                     tobj.jump(       'onTxt', text, tobj.jumpAbs)
    elif    tobj.inserting:                   tobj.insertSpace('onTxt', text)
    elif    tobj.settingN:                    tobj.setn_cmd(   'onTxt', text)
    elif    tobj.swapping:                    tobj.swapTab(    'onTxt', text)
    elif    tobj.isTab(text):                 tobj.setTab(     'onTxt', text)
    elif    text == '$' and isShf(tobj.mods): tobj.snapshot(f'{text}', 'SNAP')
    else:   slog(f'UNH {fTxt(text)} Unhandled - return 0', f=-2) if dbg else None   ;   retv = False
    if dbg: slog(f'END {fTxt(text)} swapping={tobj.swapping} {retv=}')
    return retv

def on_text_motion(tobj, motion, dbg=1):
    assert tobj
    retv = True
    kd = tobj.keyboard.data if tobj.keyboard else None
    k    = pygwink
    p, l, s, c, t = tobj.j()  ;  np, nl, ns, nc, nt = tobj.n
    if dbg: slog(f'BGN {fTxtMtn(motion)}')
    if   isNumLck(kd):                             msg =             f'NUMLOCK(         {motion})'   ;   slog(msg)   ;   pygwink.MOD_NUMLOCK = 0
    if   isCtlAltShf(kd):                          msg =             f'@&^( Unhandled   {motion})'   ;   slog(msg) #  ;   self.quit(msg)
    elif isCtlAlt(kd): # keys[k.MOD_CTRL & k.MOD_ALT]:
        if   motion == 1:                          tobj.unselectTabs(f'@& LEFT(         {motion})',  nt)
        elif motion == 2:                          tobj.unselectTabs(f'@& RIGHT(        {motion})', -nt)
        else:                                      msg =            f'@& UNH( Unhandled {motion})'   ;   slog(msg)   ;   retv = False # self.quit(msg)
    # elif isAltShf(   mods):                         msg =             f' &^(             {motion})'   ;   slog(msg) #  ;   self.quit(msg)
    # elif isCtlShf(   mods):                         msg =             f'@^(              {motion})'   ;   slog(msg) #  ;   self.quit(msg)
    # elif isSft(      mods):                         msg =             f'^ (              {motion})'   ;   slog(msg) #  ;   self.quit(msg)
    if isAlt(kd):
        if   motion == k.MOTION_UP:                tobj.moveUp(      f' & UP(           {motion})')
        elif motion == k.MOTION_DOWN:              tobj.moveDown(    f' & DOWN(         {motion})')
        elif motion == k.MOTION_LEFT:              tobj.moveLeft(    f' & LEFT(         {motion})')
        elif motion == k.MOTION_RIGHT:             tobj.moveRight(   f' & RIGHT(        {motion})')
        elif motion == k.MOTION_BEGINNING_OF_LINE: tobj.move(        f' & HOME(         {motion})', -nt *  c)
        elif motion == k.MOTION_END_OF_LINE:       tobj.move(        f' & END(          {motion})',  nt * (nc - tobj.i[C]))
        elif motion == k.MOTION_PREVIOUS_PAGE:     tobj.prevPage(    f' & PAGE UP(      {motion})')
        elif motion == k.MOTION_NEXT_PAGE:         tobj.nextPage(    f' & PAGE DOWN(    {motion})')
        else:                                      msg =           f' & UNH( Unhandled  {motion})'   ;   slog(msg)   ;   retv = False # tobj.quit(msg)
    elif isCtl(kd):
        if   motion == k.MOTION_NEXT_WORD:         tobj.selectTabs(  f'@  RIGHT(        {motion})',  nt)
        elif motion == k.MOTION_PREVIOUS_WORD:     tobj.selectTabs(  f'@  LEFT(         {motion})', -nt)
        elif motion == k.MOTION_BEGINNING_OF_LINE: msg = f'@  MOTION_BEGINNING_OF_LINE( {motion})'   ;   slog(msg)   ;   tobj.quit(msg) # N/A
        elif motion == k.MOTION_END_OF_LINE:       msg = f'@  MOTION_END_OF_LINE(       {motion})'   ;   slog(msg)   ;   tobj.quit(msg) # N/A
        elif motion == k.MOTION_BEGINNING_OF_FILE: msg = f'@  MOTION_BEGINNING_OF_FILE( {motion})'   ;   slog(msg)   ;   tobj.quit(msg) # CTRL HOME
        elif motion == k.MOTION_END_OF_FILE:       msg = f'@  MOTION_END_OF_FILE(       {motion})'   ;   slog(msg)   ;   tobj.quit(msg) # CTRL END
#           elif motion == pygwink.MOTION_DELETE:            self.deleteTabs( f'@ D MOTION_DELETE({motion})')
#           elif motion == pygwink.MOTION_COPY:              self.copyTabs(   f'@ C MOTION_COPY(  {motion})')
#           elif motion == pygwink.MOTION_PASTE:             self.pasteTabs(  f'@ V MOTION_PASTE( {motion})', kk=0)
        else:                                      msg = f'@  UNH CTRL( Unhandled       {motion}) {fTxtMtn(motion)}'   ;   slog(msg)   ;   retv = False # self.quit(msg)
    else:
        if   motion == k.MOTION_UP:                tobj.move(        f' UP(             {motion})', -1)
        elif motion == k.MOTION_DOWN:              tobj.move(        f' DOWN(           {motion})',  1)
        elif motion == k.MOTION_LEFT:              tobj.move(        f' LEFT(           {motion})', -nt)
        elif motion == k.MOTION_RIGHT:             tobj.move(        f' RIGHT(          {motion})',  nt)
        elif motion == k.MOTION_PREVIOUS_WORD:     msg = f'MOTION_PREVIOUS_WORD(        {motion})'   ;   slog(msg) #  ;   tobj.quit(msg)
        elif motion == k.MOTION_NEXT_WORD:         msg = f'MOTION_NEXT_WORD(            {motion})'   ;   slog(msg) #  ;   tobj.quit(msg)
        elif motion == k.MOTION_BEGINNING_OF_LINE: tobj.move(        f' HOME(           {motion})', -nt *  c)
        elif motion == k.MOTION_END_OF_LINE:       tobj.move(        f' END(            {motion})',  nt * (nc - tobj.i[C]))
        elif motion == k.MOTION_BEGINNING_OF_FILE: msg = f'MOTION_BEGINNING_OF_FILE(    {motion})'   ;   slog(msg) #  ;   tobj.quit(msg)
        elif motion == k.MOTION_END_OF_FILE:       msg = f'MOTION_END_OF_FILE(          {motion})'   ;   slog(msg) #  ;   tobj.quit(msg)
        elif motion == k.MOTION_PREVIOUS_PAGE:     tobj.moveUp(      f' PAGE UP(        {motion})')  # go up   to top    of line, wrap down to bottom of prev line
        elif motion == k.MOTION_NEXT_PAGE:         tobj.moveDown(    f' PAGE DOWN(      {motion})')  # go down to bottom tab on same line, wrap to next line
        elif motion == k.MOTION_DELETE:            tobj.setTab(      f'DELETE(          {motion})', tobj.tblank)
        elif motion == k.MOTION_BACKSPACE:         tobj.setTab(      f'BACKSPACE(       {motion})', tobj.tblank, rev=1)
        else:                                      msg =             f'UNH( Unhandled   {motion})'   ;   slog(msg)   ;   retv = False # tobj.quit(msg)
    if dbg: slog(f'END {fTxtMtn(motion)} {retv=}')
    return retv
########################################################################################################################################################################################################
def on_key_release(tobj, symb, mods):
    assert tobj
    slog(f'{fKbk(symb, mods)}')

def on_key_press(tobj, symb, mods, dbg=1):
    assert tobj
    retv  = True
    fontBold, fontItalic = tobj.fontBold, tobj.fontItalic
    hcurs = tobj.hcurs
    kd    = tobj.keyboard.data if tobj.keyboard else None   ;   m = mods
    kbk   = psyms(symb)
    if dbg:    slog(f'BGN {fKbk(symb, mods)} kd={fmtm(kd)}')
    if   kbk == 'A' and isCtlShf(kd, m):      tobj.flipArrow('@^A', v=1)
    elif kbk == 'A' and isCtl(   kd, m):      tobj.flipArrow('@ A', v=0)
    elif kbk == 'B' and isCtlShf(kd, m):      tobj.flipBlank(     '@^B')
    elif kbk == 'B' and isCtl(   kd, m):      tobj.flipBlank(     '@ B')
    elif kbk == 'C' and isCtlShf(kd, m):      tobj.copyTabs(      '@^C')
    elif kbk == 'C' and isCtl(   kd, m):      tobj.copyTabs(      '@ C')
    elif kbk == 'D' and isCtlShf(kd, m):      tobj.deleteTabs(    '@^D')
    elif kbk == 'D' and isCtl(   kd, m):      tobj.deleteTabs(    '@ D')
    elif kbk == 'E' and isCtlShf(kd, m):      tobj.eraseTabs(     '@^E')
#   elif kbk == 'E' and isCtl(   kd, m):      tobj.eraseTabs(     '@ E')
    elif kbk == 'F' and isCtlShf(kd, m):      tobj.flipFullScreen('@^F')
    elif kbk == 'F' and isCtl(   kd, m):      tobj.flipFlatSharp( '@ F')
    elif kbk == 'G' and isCtlShf(kd, m):      tobj.move2LastTab(  '@^G', page=1)
    elif kbk == 'G' and isCtl(   kd, m):      tobj.move2LastTab(  '@ G', page=0)
    elif kbk == 'H' and isCtlShf(kd, m):      tobj.move2FirstTab( '@^H', page=1)
    elif kbk == 'H' and isCtl(   kd, m):      tobj.move2FirstTab( '@ H', page=0)
    elif kbk == 'I' and isCtlShf(kd, m):      tobj.insertSpace(   '@^I')
    elif kbk == 'I' and isCtl(   kd, m):      tobj.flipTTs(       '@ I', II)
    elif kbk == 'J' and isCtlShf(kd, m):      tobj.jump(          '@^J', a=1)
    elif kbk == 'J' and isCtl(   kd, m):      tobj.jump(          '@ J', a=0)
    elif kbk == 'K' and isCtlShf(kd, m):      tobj.flipTTs(       '@^K', KK)
    elif kbk == 'K' and isCtl(   kd, m):      tobj.flipTTs(       '@ K', KK)
    elif kbk == 'L' and isCtlShf(kd, m):      tobj.flipLLs(       '@^L')
    elif kbk == 'L' and isCtl(   kd, m):      tobj.flipLLs(       '@ L')
    elif kbk == 'M' and isCtlShf(kd, m):      tobj.flipZZs(       '@^M', 1)
    elif kbk == 'M' and isCtl(   kd, m):      tobj.flipZZs(       '@ M', 0)
    elif kbk == 'N' and isCtlShf(kd, m):      tobj.flipTTs(       '@^N', NN)
    elif kbk == 'N' and isCtl(   kd, m):      tobj.flipTTs(       '@ N', NN)
    elif kbk == 'O' and isCtlShf(kd, m):      tobj.flipCursorMode('@^O', -1)
    elif kbk == 'O' and isCtl(   kd, m):      tobj.flipCursorMode('@ O', 1)
    elif kbk == 'P' and isCtlShf(kd, m):      tobj.addPage(       '@^P', ins=0)
    elif kbk == 'P' and isCtl(   kd, m):      tobj.addPage(       '@ P', ins=None)
    elif kbk == 'Q' and isCtlShf(kd, m):      retv = tobj.quit(   '@^Q', error=0, save=0)
    elif kbk == 'Q' and isCtl(   kd, m):      retv = tobj.quit(   '@ Q', error=0, save=1)
    elif kbk == 'R' and isCtlShf(kd, m):      tobj.flipChordNames('@^R', hit=1)
    elif kbk == 'R' and isCtl(   kd, m):      tobj.flipChordNames('@ R', hit=0)
    elif kbk == 'S' and isCtlShf(kd, m):      tobj.shiftTabs(     '@^S')
#   elif kbk == 'S' and isCtl(   kd, m):      tobj.saveDataFile(  '@ S', self.dataPath1)
    elif kbk == 'S' and isCtl(   kd, m):      tobj.swapTab(       '@ S', txt=Z)
    elif kbk == 'T' and isCtlShf(kd, m):      tobj.flipTTs(       '@^T', TT)
    elif kbk == 'T' and isCtl(   kd, m):      tobj.flipTTs(       '@ T', TT)
    elif kbk == 'U' and isCtlShf(kd, m):      tobj.reset(         '@^U')
    elif kbk == 'U' and isCtl(   kd, m):      tobj.reset(         '@ U')
#   elif kbk == 'V' and isCtlAlt(kd, m):      tobj.pasteTabs(     '@&V', hc=0, kk=1)
    elif kbk == 'V' and isCtlShf(kd, m):      tobj.pasteTabs(     '@^V', kk=1)
    elif kbk == 'V' and isCtl(   kd, m):      tobj.pasteTabs(     '@ V', kk=0)
    elif kbk == 'W' and isCtlShf(kd, m):      tobj.swapCols(      '@^W')
    elif kbk == 'W' and isCtl(   kd, m):      tobj.swapCols(      '@ W')
    elif kbk == 'X' and isCtlShf(kd, m):      tobj.cutTabs(       '@^X')
    elif kbk == 'X' and isCtl(   kd, m):      tobj.cutTabs(       '@ X')
    ####################################################################################################################################################################################################
    elif kbk == 'ESCAPE':                     tobj.flipSelectAll( 'ESCAPE')
    elif kbk == 'TAB' and isCtl(kd, m):       tobj.setCHVMode(    '@ TAB',       MELODY, LARROW)
    elif kbk == 'TAB':                        tobj.setCHVMode(    '  TAB',       MELODY, RARROW)
#   elif kbk == 'SLASH'     and isCtl(mods): tobj.setTab(        '@ SLASH', '/')
#   elif kbk == 'SLASH':                     tobj.setTab(        '  SLASH', '/')
#   elif kbk == 'BACKSLASH' and isCtl(mods): tobj.setTab(        '@ BACKSLASH', '\\')
#   elif kbk == 'BACKSLASH':                 tobj.setTab(        '  BACKSLASH', '\\')
#   elif kbk == 'SLASH'     and isCtl(mods): tobj.setCHVMode(    '@ SLASH',     ARPG,   LARROW, DARROW)
#   elif kbk == 'SLASH':                     tobj.setCHVMode(    '  SLASH',     ARPG,   RARROW, UARROW)
#   elif kbk == 'BACKSLASH' and isCtl(mods): tobj.setCHVMode(    '@ BACKSLASH', ARPG,   LARROW, UARROW)
#   elif kbk == 'BACKSLASH':                 tobj.setCHVMode(    '  BACKSLASH', ARPG,   RARROW, DARROW)
    elif kbk == 'D' and isAltShf(kd, m):      tobj.flipBGC(     '&^D')
    elif kbk == 'D' and isAlt(   kd, m):      tobj.flipBGC(     '& D')
    elif kbk == 'N' and isAltShf(kd, m):      tobj.setn_cmd(    '&^N', txt=Z)
    elif kbk == 'N' and isAlt(   kd, m):      tobj.setn_cmd(    '& N', txt=Z)
    elif kbk == 'P' and isAltShf(kd, m):      tobj.flipPage(    '&^P', 1)
    elif kbk == 'P' and isAlt(   kd, m):      tobj.flipPage(    '& P', -1)
    elif kbk == 'R' and isAltShf(kd, m):      tobj.rotateSprite('&^R', hcurs[0], -1)
    elif kbk == 'R' and isAlt(   kd, m):      tobj.rotateSprite('& R', hcurs[0],  1)
    elif kbk == 'Z' and isAltShf(kd, m):      tobj.RESIZE = not tobj.RESIZE   ;  tobj.resizeTniks(dbg=1)
    elif kbk == 'Z' and isAlt(   kd, m):                                         tobj.resizeTniks(dbg=1)
    ####################################################################################################################################################################################################
    elif kbk == 'B' and isAltShf(kd, m):      tobj.setFontParam(BOLD,      not fontBold,   'fontBold')
    elif kbk == 'B' and isAlt(   kd, m):      tobj.setFontParam(BOLD,      not fontBold,   'fontBold')
    elif kbk == 'C' and isAltShf(kd, m):      tobj.setFontParam(COLOR,         1,          'clrIdx')
    elif kbk == 'C' and isAlt(   kd, m):      tobj.setFontParam(COLOR,        -1,          'clrIdx')
    elif kbk == 'I' and isAltShf(kd, m):      tobj.setFontParam(ITALIC,    not fontItalic, 'fontItalic')
    elif kbk == 'I' and isAlt(   kd, m):      tobj.setFontParam(ITALIC,    not fontItalic, 'fontItalic')
    elif kbk == 'A' and isAltShf(kd, m):      tobj.setFontParam(FONT_NAME,     1,          'fontNameIdx')
    elif kbk == 'A' and isAlt(   kd, m):      tobj.setFontParam(FONT_NAME,    -1,          'fontNameIdx')
    elif kbk == 'S' and isAltShf(kd, m):      tobj.setFontParam(FONT_SIZE,     33 / 32,    'fontSize')
    elif kbk == 'S' and isAlt(   kd, m):      tobj.setFontParam(FONT_SIZE,     32 / 33,    'fontSize')
    else:  retv = False   ;   slog(f'UNH {fKbk(symb, mods)} kd={fmtm(kd)} Unhandled') if dbg else None
    ####################################################################################################################################################################################################
    if  not  tobj.isParsing():
        if   kbk == 'ENTER' and isCtl(kd, m): tobj.setCHVMode(  '@  ENTER',     CHORD,  v=DARROW)
        elif kbk == 'ENTER':                  tobj.setCHVMode(  '   ENTER',     CHORD,  v=UARROW)
        elif kbk == 'SPACE':                  tobj.autoMove(    '   SPACE')
#            elif dbg: self.log(f'Unexpected {self.kbkEvntTxt()} while parsing', f=2)
    if dbg:  slog(f'END {fKbk(symb, mods)} kd={fmtm(kd)} {retv=}')
    return retv
