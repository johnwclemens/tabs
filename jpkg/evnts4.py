import pyglet
#import pyglet.text         as text
#import pyglet.window       as window
##import pyglet.window.event as pygwevnt
##import pyglet.event        as pygevnt
import pyglet.window.key   as pygwink
#import pyglet.window.mouse as pygmous
from   tpkg import utl     as utl

slog, fmtf                     = utl.slog, utl.fmtf
W, Y, Z                        = utl.W, utl.Y, utl.Z
TT, NN, II, KK                 = utl.TT, utl.NN, utl.II, utl.KK
MELODY, CHORD, ARPG            = utl.MELODY, utl.CHORD, utl.ARPG
LARROW, RARROW, DARROW, UARROW = utl.LARROW, utl.RARROW, utl.DARROW, utl.UARROW
BOLD, COLOR, ITALIC, FONT_NAME, FONT_SIZE                                = utl.BOLD, utl.COLOR, utl.ITALIC, utl.FONT_NAME, utl.FONT_SIZE
P, L, S, C, T, N, I, K, R, Q, H, M, B, A, D, E                           = utl.P, utl.L, utl.S, utl.C, utl.T, utl.N, utl.I, utl.K, utl.R, utl.Q, utl.H, utl.M, utl.B, utl.A, utl.D, utl.E
isAlt, isCtl, isSft, isAltSft, isCtlAlt, isCtlSft, isCtlAltSft, isNumLck = utl.isAlt, utl.isCtl, utl.isCtlAlt, utl.isSft, utl.isAltSft, utl.isCtlSft, utl.isCtlAltSft, utl.isNumLck
########################################################################################################################################################################################################
#        else:                                  slog(f'FILTERED {msg}', f=2)

#flist    = ['on_move', 'on_mouse_motion'] # 'on_draw', 'on_move', 'on_text', 'on_text_motion', 'on_mouse_motion', 'on_mouse_scroll'
#fEvntLog = FilteredEventLogger(flist)
#flog     = fEvntLog.log
########################################################################################################################################################################################################
class FilteredEventLogger(pyglet.window.event.WindowEventLogger):
    def __init__(self, tobj, fd=None, flst=None):
        super().__init__(fd)
        self.tobj = tobj
        self.fd   = fd
        self.flst = flst if flst else []

    def flog(self, msg, filt=None):
        if filt and filt not in self.flst:
            slog(msg, f=self.fd)
        elif not filt:
            slog(msg, f=self.fd)

    def on_move(self, x, y):
        self.flog(f'{x=} {y=}', filt='on_move')

    def on_mouse_motion(self, x, y, dx, dy):
        self.flog(f'{x=} {y=} {dx=} {dy=}', filt='on_mouse_motion')

    def on_mouse_scroll(self, x, y, dx, dy):
        self.flog(f'{x=} {y=} {dx=} {dy=}', filt='on_mouse_scroll')

    def on_mouse_press(self, x, y, bttn, mods=0):
        self.flog(f'{x=} {y=} {bttn=} {mods=}', filt='on_mouse_press')

    def on_mouse_release(self, x, y, bttn, mods=0):
        self.flog(f'{x=} {y=} {bttn=} {mods=}', filt='on_mouse_release')

    def on_key_press(self, symb, mods):
        self.flog(f'{symb=} {mods=} {pygwink.symbol_string(symb)} {pygwink.modifiers_string(mods)}', filt='on_key_press')

    def on_key_release(self, symb, mods):
        self.flog(f'{symb=} {mods=} {pygwink.symbol_string(symb)} {pygwink.modifiers_string(mods)}', filt='on_key_release')

    def on_text(self, text):
        self.flog(f'{text=}', filt='on_text')

    def on_text_motion(self, motion, filt='on_text_motion'):
        self.flog(f'{motion=}')

########################################################################################################################################################################################################
#    def on_move(self, x, y):
#        self.flog(f'{x=} {y=}', filt='on_move')
#        return True

#    def on_mouse_motion(self, x, y, dx, dy):
#        self.flog(f'{x=} {y=} {dx=} {dy=}', filt='on_mouse_motion')
#        return True

#    def on_mouse_scroll(self, x, y, dx, dy):
#        self.flog(f'{x=} {y=} {dx=} {dy=}', filt='on_mouse_scroll')
        # fs = self.tobj.fontSize
        # sf = 33 / 32 if dy > 0 else 32 / 33
        # sfs = sf * fs
        # self.flog(f'{x=} {y=} {dx=} {dy=}, sf * fs = ss, {fmtf(sf, 5)} * {fmtf(fs, 5)} = {fmtf(sfs, 5)}', filt='on_mouse_scroll')
        # self.tobj.setFontParam(FONT_SIZE, sfs, 'fontSize')
        # return True

#    def on_mouse_press(self, x, y, bttn, mods=0):
#        self.flog(f'{x=} {y=} {bttn=} {mods=}', filt='on_mouse_press')

#    def on_mouse_release(self, x, y, bttn, mods=0):
#        self.flog(f'{x=} {y=} {bttn=} {mods=}', filt='on_mouse_release')
        # dbg = 1
        # tobj = self.tobj
        # if bttn==pygmous.LEFT:
        #     hh = tobj.height  ;  ww = tobj.width  ;  tlen = len(tobj.tabls)  ;  ll = tobj.LL    ;  np, nl, ns, nc, nt  = tobj.n
        #     y0 = y            ;   y = hh - y0     ;    nr = nl*(ns*nt + ll)  ;   w = ww/nc      ;  h = hh/nr
        #     cc = tobj.cc      ;   r = int(y/h)    ;     d = int(y/h)  - ll   ;   a = int(d/nr)  ;  b = int(x/w)
        #     p  = tobj.j()[P]  ;   l = a           ;     s = d//nt            ;   c = b          ;  t = (d - l*nr) # % nt
        #     txt = tobj.tabls[cc].text if cc < tlen else Z
        #     if dbg:   self.flog(f'BGN {x=:4} {y0=:4} {y=:4} {w=:6.2f} {h=:6.2f} {ll=} {nc=:2} {nr=:2} {r=:2} {d=:2} {txt=} {bttn=} {mods=}')
        #     if dbg:   self.flog(f'    p={p+1} l={l+1}=(d/nr) s={s+1}=(d//nt) c={c+1}=(x/w) t={t+1}=(d-l*nr)')
        #     if dbg:   self.flog(f'    before MOVE plsct={tobj.fplsct(p, l, s, c, t)}')
        #     p, l, s, c, t = tobj.moveToB('MOUSE RELEASE', p, l, s, c, t)
        #     if dbg:   self.flog(f'    after  MOVE plsct={tobj.fplsct(p, l, s, c, t)}')
        #     if dbg:   self.flog(f'END {x=:4} {y0=:4} {y=:4} {ww=:6.2f} {hh=:6.2f}')
        #     return True
        # else: return False

#    def on_key_press(self, symb, mods):
#        self.flog(f'{symb=} {mods=} {pygwink.symbol_string(symb)} {pygwink.modifiers_string(mods)}', filt='on_key_press')
    #     retv = True   ;   dbg = 1
    #     tobj = self.tobj
    #     fontBold, fontItalic                             = tobj.fontBold, tobj.fontItalic
    #     tobj.symb, tobj.mods, tobj.symbStr, tobj.modsStr = symb, mods, pygwink.symbol_string(symb), pygwink.modifiers_string(mods)
    #     tobj.kbk = tobj.symbStr   ;   kbk = tobj.kbk   ;   hcurs = tobj.hcurs
    #     if dbg:    self.flog(f'BGN {tobj.kbkEvntTxt()}')
    #     if   kbk == 'A' and isCtlSft(mods):    tobj.flipArrow('@^A', v=1)
    #     elif kbk == 'A' and isCtl(mods):       tobj.flipArrow('@ A', v=0)
    #     elif kbk == 'B' and isCtlSft(mods):    tobj.flipBlank(     '@^B')
    #     elif kbk == 'B' and isCtl(   mods):    tobj.flipBlank(     '@ B')
    #     elif kbk == 'C' and isCtlSft(mods):    tobj.copyTabs(      '@^C')
    #     elif kbk == 'C' and isCtl(   mods):    tobj.copyTabs(      '@ C')
    #     elif kbk == 'D' and isCtlSft(mods):    tobj.deleteTabs(    '@^D')
    #     elif kbk == 'D' and isCtl(   mods):    tobj.deleteTabs(    '@ D')
    #     elif kbk == 'E' and isCtlSft(mods):    tobj.eraseTabs(     '@^E')
    # #   elif kbk == 'E' and isCtl(   mods):    tobj.eraseTabs(     '@ E')
    #     elif kbk == 'F' and isCtlSft(mods):    tobj.flipFullScreen('@^F')
    #     elif kbk == 'F' and isCtl(   mods):    tobj.flipFlatSharp( '@ F')
    #     elif kbk == 'G' and isCtlSft(mods):    tobj.move2LastTab(  '@^G', page=1)
    #     elif kbk == 'G' and isCtl(   mods):    tobj.move2LastTab(  '@ G', page=0)
    #     elif kbk == 'H' and isCtlSft(mods):    tobj.move2FirstTab( '@^H', page=1)
    #     elif kbk == 'H' and isCtl(   mods):    tobj.move2FirstTab( '@ H', page=0)
    #     elif kbk == 'I' and isCtlSft(mods):    tobj.insertSpace(   '@^I')
    #     elif kbk == 'I' and isCtl(   mods):    tobj.flipTTs(       '@ I', II)
    #     elif kbk == 'J' and isCtlSft(mods):    tobj.jump(          '@^J', a=1)
    #     elif kbk == 'J' and isCtl(   mods):    tobj.jump(          '@ J', a=0)
    #     elif kbk == 'K' and isCtlSft(mods):    tobj.flipTTs(       '@^K', KK)
    #     elif kbk == 'K' and isCtl(   mods):    tobj.flipTTs(       '@ K', KK)
    #     elif kbk == 'L' and isCtlSft(mods):    tobj.flipLLs(       '@^L')
    #     elif kbk == 'L' and isCtl(   mods):    tobj.flipLLs(       '@ L')
    #     elif kbk == 'M' and isCtlSft(mods):    tobj.flipZZs(       '@^M', 1)
    #     elif kbk == 'M' and isCtl(   mods):    tobj.flipZZs(       '@ M', 0)
    #     elif kbk == 'N' and isCtlSft(mods):    tobj.flipTTs(       '@^N', NN)
    #     elif kbk == 'N' and isCtl(   mods):    tobj.flipTTs(       '@ N', NN)
    #     elif kbk == 'O' and isCtlSft(mods):    tobj.flipCursorMode('@^O', -1)
    #     elif kbk == 'O' and isCtl(   mods):    tobj.flipCursorMode('@ O', 1)
    #     elif kbk == 'P' and isCtlSft(mods):    tobj.addPage(       '@^P', ins=0)
    #     elif kbk == 'P' and isCtl(   mods):    tobj.addPage(       '@ P', ins=None)
    #     elif kbk == 'Q' and isCtlSft(mods):    retv = tobj.quit(   '@^Q', error=0, save=0)
    #     elif kbk == 'Q' and isCtl(   mods):    retv = tobj.quit(   '@ Q', error=0, save=1)
    #     elif kbk == 'R' and isCtlSft(mods):    tobj.flipChordNames('@^R', hit=1)
    #     elif kbk == 'R' and isCtl(   mods):    tobj.flipChordNames('@ R', hit=0)
    #     elif kbk == 'S' and isCtlSft(mods):    tobj.shiftTabs(     '@^S')
    # #   elif kbk == 'S' and isCtl(   mods):    tobj.saveDataFile(  '@ S', self.dataPath1)
    #     elif kbk == 'S' and isCtl(   mods):    tobj.swapTab(       '@ S', txt=Z)
    #     elif kbk == 'T' and isCtlSft(mods):    tobj.flipTTs(       '@^T', TT)
    #     elif kbk == 'T' and isCtl(   mods):    tobj.flipTTs(       '@ T', TT)
    #     elif kbk == 'U' and isCtlSft(mods):    tobj.reset(         '@^U')
    #     elif kbk == 'U' and isCtl(   mods):    tobj.reset(         '@ U')
    # #   elif kbk == 'V' and isCtlAlt(mods):    tobj.pasteTabs(     '@&V', hc=0, kk=1)
    #     elif kbk == 'V' and isCtlSft(mods):    tobj.pasteTabs(     '@^V', kk=1)
    #     elif kbk == 'V' and isCtl(   mods):    tobj.pasteTabs(     '@ V', kk=0)
    #     elif kbk == 'W' and isCtlSft(mods):    tobj.swapCols(      '@^W')
    #     elif kbk == 'W' and isCtl(   mods):    tobj.swapCols(      '@ W')
    #     elif kbk == 'X' and isCtlSft(mods):    tobj.cutTabs(       '@^X')
    #     elif kbk == 'X' and isCtl(   mods):    tobj.cutTabs(       '@ X')
    #     ####################################################################################################################################################################################################
    #     elif kbk == 'ESCAPE':                    tobj.flipSelectAll( 'ESCAPE')
    #     elif kbk == 'TAB'       and isCtl(mods): tobj.setCHVMode(    '@ TAB',       MELODY, LARROW)
    #     elif kbk == 'TAB':                       tobj.setCHVMode(    '  TAB',       MELODY, RARROW)
    # #   elif kbk == 'SLASH'     and isCtl(mods): tobj.setTab(        '@ SLASH', '/')
    # #   elif kbk == 'SLASH':                     tobj.setTab(        '  SLASH', '/')
    # #   elif kbk == 'BACKSLASH' and isCtl(mods): tobj.setTab(        '@ BACKSLASH', '\\')
    # #   elif kbk == 'BACKSLASH':                 tobj.setTab(        '  BACKSLASH', '\\')
    # #   elif kbk == 'SLASH'     and isCtl(mods): tobj.setCHVMode(    '@ SLASH',     ARPG,   LARROW, DARROW)
    # #   elif kbk == 'SLASH':                     tobj.setCHVMode(    '  SLASH',     ARPG,   RARROW, UARROW)
    # #   elif kbk == 'BACKSLASH' and isCtl(mods): tobj.setCHVMode(    '@ BACKSLASH', ARPG,   LARROW, UARROW)
    # #   elif kbk == 'BACKSLASH':                 tobj.setCHVMode(    '  BACKSLASH', ARPG,   RARROW, DARROW)
    #     elif kbk == 'D' and isAltSft(mods):      tobj.flipBGC(     '&^D')
    #     elif kbk == 'D' and isAlt(   mods):      tobj.flipBGC(     '& D')
    #     elif kbk == 'N' and isAltSft(mods):      tobj.setn_cmd(    '&^N', txt=Z)
    #     elif kbk == 'N' and isAlt(   mods):      tobj.setn_cmd(    '& N', txt=Z)
    #     elif kbk == 'P' and isAltSft(mods):      tobj.flipPage(    '&^P', 1)
    #     elif kbk == 'P' and isAlt(   mods):      tobj.flipPage(    '& P', -1)
    #     elif kbk == 'R' and isAltSft(mods):      tobj.rotateSprite('&^R', hcurs[0], -1)
    #     elif kbk == 'R' and isAlt(   mods):      tobj.rotateSprite('& R', hcurs[0],  1)
    #     elif kbk == 'Z' and isAltSft(mods):      tobj.RESIZE = not tobj.RESIZE   ;  tobj.resizeTniks(dbg=1)
    #     elif kbk == 'Z' and isAlt(   mods):                                         tobj.resizeTniks(dbg=1)
    #     ####################################################################################################################################################################################################
    #     elif kbk == 'B' and isAltSft(mods):      tobj.setFontParam(BOLD,      not fontBold,   'fontBold')
    #     elif kbk == 'B' and isAlt(   mods):      tobj.setFontParam(BOLD,      not fontBold,   'fontBold')
    #     elif kbk == 'C' and isAltSft(mods):      tobj.setFontParam(COLOR,         1,          'clrIdx')
    #     elif kbk == 'C' and isAlt(   mods):      tobj.setFontParam(COLOR,        -1,          'clrIdx')
    #     elif kbk == 'I' and isAltSft(mods):      tobj.setFontParam(ITALIC,    not fontItalic, 'fontItalic')
    #     elif kbk == 'I' and isAlt(   mods):      tobj.setFontParam(ITALIC,    not fontItalic, 'fontItalic')
    #     elif kbk == 'A' and isAltSft(mods):      tobj.setFontParam(FONT_NAME,     1,          'fontNameIdx')
    #     elif kbk == 'A' and isAlt(   mods):      tobj.setFontParam(FONT_NAME,    -1,          'fontNameIdx')
    #     elif kbk == 'S' and isAltSft(mods):      tobj.setFontParam(FONT_SIZE,     33 / 32,    'fontSize')
    #     elif kbk == 'S' and isAlt(   mods):      tobj.setFontParam(FONT_SIZE,     32 / 33,    'fontSize')
    #     else:   self.flog(f'UNH {tobj.kbkEvntTxt()} Unhandled - return 0') if dbg else None   ;   retv = False
    #     ####################################################################################################################################################################################################
    #     if  not  tobj.isParsing():
    #         if   kbk == 'ENTER' and isCtl(mods): tobj.setCHVMode(  '@  ENTER',     CHORD,  v=DARROW)
    #         elif kbk == 'ENTER':                 tobj.setCHVMode(  '   ENTER',     CHORD,  v=UARROW)
    #         elif kbk == 'SPACE':                 tobj.autoMove(    '   SPACE')
    # #            elif dbg: self.log(f'Unexpected {self.kbkEvntTxt()} while parsing', f=2)
    #     if dbg:  self.flog(f'END {tobj.kbkEvntTxt()}')
    #     return retv

#    def on_key_release(self, symb, mods):
#        self.flog(f'{symb=} {mods=} {pygwink.symbol_string(symb)} {pygwink.modifiers_string(mods)}', filt='on_key_release')
        # self.tobj.symb, self.tobj.mods, self.tobj.symbStr, self.tobj.modsStr = symb, mods, pygwink.symbol_string(symb), pygwink.modifiers_string(mods)
        # self.tobj.kbk = self.tobj.symbStr
        # self.flog(f'    {self.tobj.kbkEvntTxt()}')
        # return True

#    def on_text(self, text):
#        self.flog(f'{text=}', filt='on_text')
        # retv = True
        # tobj = self.tobj
        # tobj.kbk = text
        # if dbg: self.flog(f'BGN {tobj.kbkEvntTxt()} swapping={tobj.swapping}')
        # if      tobj.shiftingTabs:                       tobj.shiftTabs(  'onTxt', text)
        # elif    tobj.jumping:                            tobj.jump(       'onTxt', text, tobj.jumpAbs)
        # elif    tobj.inserting:                          tobj.insertSpace('onTxt', text)
        # elif    tobj.settingN:                           tobj.setn_cmd(   'onTxt', text)
        # elif    tobj.swapping:                           tobj.swapTab(    'onTxt', text)
        # elif    tobj.isTab(tobj.kbk):                    tobj.setTab(     'onTxt', tobj.kbk)
        # elif    tobj.kbk == '$' and isSft(tobj.mods):    tobj.snapshot(f'{text}', 'SNAP')
        # else:   self.flog(f'UNH {tobj.kbkEvntTxt()} Unhandled - return 0') if dbg else None   ;   retv = False
        # if dbg: self.flog(f'END {tobj.kbkEvntTxt()} swapping={tobj.swapping}')
        # return retv

#    def on_text_motion(self, motion, filt='on_text_motion'):
#        self.flog(f'{motion=}')
    #     tobj = self.tobj
    #     tobj.kbk = motion   ;   p, l, s, c, t = tobj.j()  ;  np, nl, ns, nc, nt = tobj.n
    #     if dbg: self.flog(f'BGN {tobj.kbkEvntTxt()} motion={motion}')
    #     if   isNumLck(   tobj.mods):                         msg =             f'NUMLOCK(         {motion})'   ;   self.flog(msg)   ;   pygwink.MOD_NUMLOCK = 0
    #     if   isCtlAltSft(tobj.mods):                         msg =             f'@&^(             {motion})'   ;   self.flog(msg) #  ;   self.quit(msg)
    #     elif isCtlAlt(   tobj.mods):
    #         if   motion == 1:                                tobj.unselectTabs(f'@& LEFT(         {motion})',  nt)
    #         elif motion == 2:                                tobj.unselectTabs(f'@& RIGHT(        {motion})', -nt)
    #         else:                                            msg =             f'@& (             {motion})'   ;   self.flog(msg) #  ;   self.quit(msg)
    #     elif isAltSft(   tobj.mods):                         msg =             f' &^(             {motion})'   ;   self.flog(msg) #  ;   self.quit(msg)
    #     elif isCtlSft(   tobj.mods):                         msg =             f'@^(              {motion})'   ;   self.flog(msg) #  ;   self.quit(msg)
    #     elif isSft(      tobj.mods):                         msg =             f'^ (              {motion})'   ;   self.flog(msg) #  ;   self.quit(msg)
    #     elif isAlt(      tobj.mods):
    #         if   motion == pygwink.MOTION_UP:                tobj.moveUp(      f' & UP(           {motion})')
    #         elif motion == pygwink.MOTION_DOWN:              tobj.moveDown(    f' & DOWN(         {motion})')
    #         elif motion == pygwink.MOTION_LEFT:              tobj.moveLeft(    f' & LEFT(         {motion})')
    #         elif motion == pygwink.MOTION_RIGHT:             tobj.moveRight(   f' & RIGHT(        {motion})')
    #         elif motion == pygwink.MOTION_BEGINNING_OF_LINE: tobj.move(        f' & HOME(         {motion})', -nt *  c)
    #         elif motion == pygwink.MOTION_END_OF_LINE:       tobj.move(        f' & END(          {motion})',  nt * (nc - tobj.i[C]))
    #         elif motion == pygwink.MOTION_PREVIOUS_PAGE:     tobj.prevPage(    f' & PAGE UP(      {motion})')
    #         elif motion == pygwink.MOTION_NEXT_PAGE:         tobj.nextPage(    f' & PAGE DOWN(    {motion})')
    #         else:                                            msg =             f' &(              {motion})'   ;   self.flog(msg)   ;   tobj.quit(msg)
    #     elif isCtl(tobj.mods):
    #         if   motion == pygwink.MOTION_NEXT_WORD:         tobj.selectTabs(  f'@  RIGHT(        {motion})',  nt)
    #         elif motion == pygwink.MOTION_PREVIOUS_WORD:     tobj.selectTabs(  f'@  LEFT(         {motion})', -nt)
    #         elif motion == pygwink.MOTION_BEGINNING_OF_LINE: msg = f'@  MOTION_BEGINNING_OF_LINE( {motion})'   ;   self.flog(msg)   ;   tobj.quit(msg) # N/A
    #         elif motion == pygwink.MOTION_END_OF_LINE:       msg = f'@  MOTION_END_OF_LINE(       {motion})'   ;   self.flog(msg)   ;   tobj.quit(msg) # N/A
    #         elif motion == pygwink.MOTION_BEGINNING_OF_FILE: msg = f'@  MOTION_BEGINNING_OF_FILE( {motion})'   ;   self.flog(msg)   ;   tobj.quit(msg) # CTRL HOME
    #         elif motion == pygwink.MOTION_END_OF_FILE:       msg = f'@  MOTION_END_OF_FILE(       {motion})'   ;   self.flog(msg)   ;   tobj.quit(msg) # CTRL END
    # #           elif motion == pygwink.MOTION_DELETE:            self.deleteTabs( f'@ D MOTION_DELETE({motion})')
    # #           elif motion == pygwink.MOTION_COPY:              self.copyTabs(   f'@ C MOTION_COPY(  {motion})')
    # #           elif motion == pygwink.MOTION_PASTE:             self.pasteTabs(  f'@ V MOTION_PASTE( {motion})', kk=0)
    #         else:                                            msg =             f'UNH CTRL(        {motion}) {tobj.kbkEvntTxt()}'   ;   self.flog(msg) #  ;   self.quit(msg)
    #     elif tobj.mods == 0:
    #         if   motion == pygwink.MOTION_UP:                tobj.move(        f' UP(             {motion})', -1)
    #         elif motion == pygwink.MOTION_DOWN:              tobj.move(        f' DOWN(           {motion})',  1)
    #         elif motion == pygwink.MOTION_LEFT:              tobj.move(        f' LEFT(           {motion})', -nt)
    #         elif motion == pygwink.MOTION_RIGHT:             tobj.move(        f' RIGHT(          {motion})',  nt)
    #         elif motion == pygwink.MOTION_PREVIOUS_WORD:     msg = f'MOTION_PREVIOUS_WORD(        {motion})'   ;   self.flog(msg)   ;   tobj.quit(msg)
    #         elif motion == pygwink.MOTION_NEXT_WORD:         msg = f'MOTION_NEXT_WORD(            {motion})'   ;   self.flog(msg)   ;   tobj.quit(msg)
    #         elif motion == pygwink.MOTION_BEGINNING_OF_LINE: tobj.move(        f' HOME(           {motion})', -nt *  c)
    #         elif motion == pygwink.MOTION_END_OF_LINE:       tobj.move(        f' END(            {motion})',  nt * (nc - tobj.i[C]))
    #         elif motion == pygwink.MOTION_BEGINNING_OF_FILE: msg = f'MOTION_BEGINNING_OF_FILE(    {motion})'   ;   self.flog(msg)   ;   tobj.quit(msg)
    #         elif motion == pygwink.MOTION_END_OF_FILE:       msg = f'MOTION_END_OF_FILE(          {motion})'   ;   self.flog(msg)   ;   tobj.quit(msg)
    #         elif motion == pygwink.MOTION_PREVIOUS_PAGE:     tobj.moveUp(      f' PAGE UP(        {motion})')  # go up   to top    of line, wrap down to bottom of prev line
    #         elif motion == pygwink.MOTION_NEXT_PAGE:         tobj.moveDown(    f' PAGE DOWN(      {motion})')  # go down to bottom tab on same line, wrap to next line
    #         elif motion == pygwink.MOTION_DELETE:            tobj.setTab(      f'DELETE(          {motion})', tobj.tblank)
    #         elif motion == pygwink.MOTION_BACKSPACE:         tobj.setTab(      f'BACKSPACE(       {motion})', tobj.tblank, rev=1)
    #         else:                                            msg =             f'(                {motion})'   ;   self.flog(msg)   ;   tobj.quit(msg)
    #     if dbg: self.flog(f'END {tobj.kbkEvntTxt()} motion={motion}')
    #     return True
    ####################################################################################################################################################################################################
# def on_mouse_motion(x, y, dx, dy):
#     flog(f'{x=} {y=} {dx=} {dy=}', filt='on_mouse_motion', f=-2)
#     return True
#
# def on_mouse_scroll(tobj, x, y, dx, dy):
#     fs = tobj.fontSize
#     sf = 33 / 32 if dy > 0 else 32 / 33
#     sfs = sf * fs
#     flog(f'{x=} {y=} {dx=} {dy=}, sf * fs = ss, {fmtf(sf, 5)} * {fmtf(fs, 5)} = {fmtf(sfs, 5)}', filt='on_mouse_scroll', f=-2)
#     tobj.setFontParam(FONT_SIZE, sfs, 'fontSize')
#     return True
#
# def on_mouse_release(tobj, x, y, bttn, mods=0, dbg=1):
#     if bttn==pygmous.LEFT:
#         hh = tobj.height  ;  ww = tobj.width  ;  tlen = len(tobj.tabls)  ;  ll = tobj.LL    ;  np, nl, ns, nc, nt  = tobj.n
#         y0 = y            ;   y = hh - y0     ;    nr = nl*(ns*nt + ll)  ;   w = ww/nc      ;  h = hh/nr
#         cc = tobj.cc      ;   r = int(y/h)    ;     d = int(y/h)  - ll   ;   a = int(d/nr)  ;  b = int(x/w)
#         p  = tobj.j()[P]  ;   l = a           ;     s = d//nt            ;   c = b          ;  t = (d - l*nr) # % nt
#         txt = tobj.tabls[cc].text if cc < tlen else Z   ;   f = -2
#         if dbg:   slog(f'BGN {x=:4} {y0=:4} {y=:4} {w=:6.2f} {h=:6.2f} {ll=} {nc=:2} {nr=:2} {r=:2} {d=:2} {txt=} {bttn=} {mods=}', f=f)
#         if dbg:   slog(f'    p={p+1} l={l+1}=(d/nr) s={s+1}=(d//nt) c={c+1}=(x/w) t={t+1}=(d-l*nr)', f=f)
#         if dbg:   slog(f'    before MOVE plsct={tobj.fplsct(p, l, s, c, t)}',   f=f)
#         p, l, s, c, t = tobj.moveToB('MOUSE RELEASE', p, l, s, c, t)
#         if dbg:   slog(f'    after  MOVE plsct={tobj.fplsct(p, l, s, c, t)}',   f=f)
#         if dbg:   slog(f'END {x=:4} {y0=:4} {y=:4} {ww=:6.2f} {hh=:6.2f}',      f=f)
#         return True
#     else: return False
#
# def on_key_press(tobj, symb, mods, dbg=1): # avoid these
#     retv = True
#     fontBold, fontItalic                             = tobj.fontBold, tobj.fontItalic
#     tobj.symb, tobj.mods, tobj.symbStr, tobj.modsStr = symb, mods, pygwink.symbol_string(symb), pygwink.modifiers_string(mods)
#     tobj.kbk = tobj.symbStr   ;   kbk = tobj.kbk   ;   hcurs = tobj.hcurs
#     if dbg:    flog(f'BGN {tobj.kbkEvntTxt()}', f=-2)
#     if   kbk == 'A' and isCtlSft(mods):    tobj.flipArrow('@^A', v=1)
#     elif kbk == 'A' and isCtl(mods):       tobj.flipArrow('@ A', v=0)
#     elif kbk == 'B' and isCtlSft(mods):    tobj.flipBlank(     '@^B')
#     elif kbk == 'B' and isCtl(   mods):    tobj.flipBlank(     '@ B')
#     elif kbk == 'C' and isCtlSft(mods):    tobj.copyTabs(      '@^C')
#     elif kbk == 'C' and isCtl(   mods):    tobj.copyTabs(      '@ C')
#     elif kbk == 'D' and isCtlSft(mods):    tobj.deleteTabs(    '@^D')
#     elif kbk == 'D' and isCtl(   mods):    tobj.deleteTabs(    '@ D')
#     elif kbk == 'E' and isCtlSft(mods):    tobj.eraseTabs(     '@^E')
# #   elif kbk == 'E' and isCtl(   mods):    tobj.eraseTabs(     '@ E')
#     elif kbk == 'F' and isCtlSft(mods):    tobj.flipFullScreen('@^F')
#     elif kbk == 'F' and isCtl(   mods):    tobj.flipFlatSharp( '@ F')
#     elif kbk == 'G' and isCtlSft(mods):    tobj.move2LastTab(  '@^G', page=1)
#     elif kbk == 'G' and isCtl(   mods):    tobj.move2LastTab(  '@ G', page=0)
#     elif kbk == 'H' and isCtlSft(mods):    tobj.move2FirstTab( '@^H', page=1)
#     elif kbk == 'H' and isCtl(   mods):    tobj.move2FirstTab( '@ H', page=0)
#     elif kbk == 'I' and isCtlSft(mods):    tobj.insertSpace(   '@^I')
#     elif kbk == 'I' and isCtl(   mods):    tobj.flipTTs(       '@ I', II)
#     elif kbk == 'J' and isCtlSft(mods):    tobj.jump(          '@^J', a=1)
#     elif kbk == 'J' and isCtl(   mods):    tobj.jump(          '@ J', a=0)
#     elif kbk == 'K' and isCtlSft(mods):    tobj.flipTTs(       '@^K', KK)
#     elif kbk == 'K' and isCtl(   mods):    tobj.flipTTs(       '@ K', KK)
#     elif kbk == 'L' and isCtlSft(mods):    tobj.flipLLs(       '@^L')
#     elif kbk == 'L' and isCtl(   mods):    tobj.flipLLs(       '@ L')
#     elif kbk == 'M' and isCtlSft(mods):    tobj.flipZZs(       '@^M', 1)
#     elif kbk == 'M' and isCtl(   mods):    tobj.flipZZs(       '@ M', 0)
#     elif kbk == 'N' and isCtlSft(mods):    tobj.flipTTs(       '@^N', NN)
#     elif kbk == 'N' and isCtl(   mods):    tobj.flipTTs(       '@ N', NN)
#     elif kbk == 'O' and isCtlSft(mods):    tobj.flipCursorMode('@^O', -1)
#     elif kbk == 'O' and isCtl(   mods):    tobj.flipCursorMode('@ O', 1)
#     elif kbk == 'P' and isCtlSft(mods):    tobj.addPage(       '@^P', ins=0)
#     elif kbk == 'P' and isCtl(   mods):    tobj.addPage(       '@ P', ins=None)
#     elif kbk == 'Q' and isCtlSft(mods):    retv = tobj.quit(   '@^Q', error=0, save=0)
#     elif kbk == 'Q' and isCtl(   mods):    retv = tobj.quit(   '@ Q', error=0, save=1)
#     elif kbk == 'R' and isCtlSft(mods):    tobj.flipChordNames('@^R', hit=1)
#     elif kbk == 'R' and isCtl(   mods):    tobj.flipChordNames('@ R', hit=0)
#     elif kbk == 'S' and isCtlSft(mods):    tobj.shiftTabs(     '@^S')
# #   elif kbk == 'S' and isCtl(   mods):    tobj.saveDataFile(  '@ S', self.dataPath1)
#     elif kbk == 'S' and isCtl(   mods):    tobj.swapTab(       '@ S', txt=Z)
#     elif kbk == 'T' and isCtlSft(mods):    tobj.flipTTs(       '@^T', TT)
#     elif kbk == 'T' and isCtl(   mods):    tobj.flipTTs(       '@ T', TT)
#     elif kbk == 'U' and isCtlSft(mods):    tobj.reset(         '@^U')
#     elif kbk == 'U' and isCtl(   mods):    tobj.reset(         '@ U')
# #   elif kbk == 'V' and isCtlAlt(mods):    tobj.pasteTabs(     '@&V', hc=0, kk=1)
#     elif kbk == 'V' and isCtlSft(mods):    tobj.pasteTabs(     '@^V', kk=1)
#     elif kbk == 'V' and isCtl(   mods):    tobj.pasteTabs(     '@ V', kk=0)
#     elif kbk == 'W' and isCtlSft(mods):    tobj.swapCols(      '@^W')
#     elif kbk == 'W' and isCtl(   mods):    tobj.swapCols(      '@ W')
#     elif kbk == 'X' and isCtlSft(mods):    tobj.cutTabs(       '@^X')
#     elif kbk == 'X' and isCtl(   mods):    tobj.cutTabs(       '@ X')
#     ####################################################################################################################################################################################################
#     elif kbk == 'ESCAPE':                    tobj.flipSelectAll( 'ESCAPE')
#     elif kbk == 'TAB'       and isCtl(mods): tobj.setCHVMode(    '@ TAB',       MELODY, LARROW)
#     elif kbk == 'TAB':                       tobj.setCHVMode(    '  TAB',       MELODY, RARROW)
# #   elif kbk == 'SLASH'     and isCtl(mods): tobj.setTab(        '@ SLASH', '/')
# #   elif kbk == 'SLASH':                     tobj.setTab(        '  SLASH', '/')
# #   elif kbk == 'BACKSLASH' and isCtl(mods): tobj.setTab(        '@ BACKSLASH', '\\')
# #   elif kbk == 'BACKSLASH':                 tobj.setTab(        '  BACKSLASH', '\\')
# #   elif kbk == 'SLASH'     and isCtl(mods): tobj.setCHVMode(    '@ SLASH',     ARPG,   LARROW, DARROW)
# #   elif kbk == 'SLASH':                     tobj.setCHVMode(    '  SLASH',     ARPG,   RARROW, UARROW)
# #   elif kbk == 'BACKSLASH' and isCtl(mods): tobj.setCHVMode(    '@ BACKSLASH', ARPG,   LARROW, UARROW)
# #   elif kbk == 'BACKSLASH':                 tobj.setCHVMode(    '  BACKSLASH', ARPG,   RARROW, DARROW)
#     elif kbk == 'D' and isAltSft(mods):      tobj.flipBGC(     '&^D')
#     elif kbk == 'D' and isAlt(   mods):      tobj.flipBGC(     '& D')
#     elif kbk == 'N' and isAltSft(mods):      tobj.setn_cmd(    '&^N', txt=Z)
#     elif kbk == 'N' and isAlt(   mods):      tobj.setn_cmd(    '& N', txt=Z)
#     elif kbk == 'P' and isAltSft(mods):      tobj.flipPage(    '&^P', 1)
#     elif kbk == 'P' and isAlt(   mods):      tobj.flipPage(    '& P', -1)
#     elif kbk == 'R' and isAltSft(mods):      tobj.rotateSprite('&^R', hcurs[0], -1)
#     elif kbk == 'R' and isAlt(   mods):      tobj.rotateSprite('& R', hcurs[0],  1)
#     elif kbk == 'Z' and isAltSft(mods):      tobj.RESIZE = not tobj.RESIZE   ;  tobj.resizeTniks(dbg=1)
#     elif kbk == 'Z' and isAlt(   mods):                                         tobj.resizeTniks(dbg=1)
#     ####################################################################################################################################################################################################
#     elif kbk == 'B' and isAltSft(mods):      tobj.setFontParam(BOLD,      not fontBold,   'fontBold')
#     elif kbk == 'B' and isAlt(   mods):      tobj.setFontParam(BOLD,      not fontBold,   'fontBold')
#     elif kbk == 'C' and isAltSft(mods):      tobj.setFontParam(COLOR,         1,          'clrIdx')
#     elif kbk == 'C' and isAlt(   mods):      tobj.setFontParam(COLOR,        -1,          'clrIdx')
#     elif kbk == 'I' and isAltSft(mods):      tobj.setFontParam(ITALIC,    not fontItalic, 'fontItalic')
#     elif kbk == 'I' and isAlt(   mods):      tobj.setFontParam(ITALIC,    not fontItalic, 'fontItalic')
#     elif kbk == 'A' and isAltSft(mods):      tobj.setFontParam(FONT_NAME,     1,          'fontNameIdx')
#     elif kbk == 'A' and isAlt(   mods):      tobj.setFontParam(FONT_NAME,    -1,          'fontNameIdx')
#     elif kbk == 'S' and isAltSft(mods):      tobj.setFontParam(FONT_SIZE,     33 / 32,    'fontSize')
#     elif kbk == 'S' and isAlt(   mods):      tobj.setFontParam(FONT_SIZE,     32 / 33,    'fontSize')
#     else:   flog(f'UNH {tobj.kbkEvntTxt()} Unhandled - return 0', f=1) if dbg else None   ;   retv = False
#     ####################################################################################################################################################################################################
#     if  not  tobj.isParsing():
#         if   kbk == 'ENTER' and isCtl(mods): tobj.setCHVMode(  '@  ENTER',     CHORD,  v=DARROW)
#         elif kbk == 'ENTER':                 tobj.setCHVMode(  '   ENTER',     CHORD,  v=UARROW)
#         elif kbk == 'SPACE':                 tobj.autoMove(    '   SPACE')
# #            elif dbg: self.log(f'Unexpected {self.kbkEvntTxt()} while parsing', f=2)
#     if dbg:  flog(f'END {tobj.kbkEvntTxt()}', f=-2)
#     return retv
#
# def on_key_release(tobj, symb, mods, dbg=1):
#     tobj.symb, tobj.mods, tobj.symbStr, tobj.modsStr = symb, mods, pygwink.symbol_string(symb), pygwink.modifiers_string(mods)
#     tobj.kbk = tobj.symbStr
#     if dbg:    flog(f'    {tobj.kbkEvntTxt()}', f=-2)
#     return True
#
# def on_text(tobj, text, dbg=1): # use for entering strings not for motion
#     retv = True
#     tobj.kbk = text
#     if dbg: flog(f'BGN {tobj.kbkEvntTxt()} swapping={tobj.swapping}')
#     if      tobj.shiftingTabs:                       tobj.shiftTabs(  'onTxt', text)
#     elif    tobj.jumping:                            tobj.jump(       'onTxt', text, tobj.jumpAbs)
#     elif    tobj.inserting:                          tobj.insertSpace('onTxt', text)
#     elif    tobj.settingN:                           tobj.setn_cmd(   'onTxt', text)
#     elif    tobj.swapping:                           tobj.swapTab(    'onTxt', text)
#     elif    tobj.isTab(tobj.kbk):                    tobj.setTab(     'onTxt', tobj.kbk)
#     elif    tobj.kbk == '$' and isSft(tobj.mods):    tobj.snapshot(f'{text}', 'SNAP')
#     else:   flog(f'UNH {tobj.kbkEvntTxt()} Unhandled - return 0', f=-2) if dbg else None   ;   retv = False
#     if dbg: flog(f'END {tobj.kbkEvntTxt()} swapping={tobj.swapping}')
#     return retv
#
# def on_text_motion(tobj, motion, dbg=1): # use for motion not strings
#     tobj.kbk = motion   ;   p, l, s, c, t = tobj.j()  ;  np, nl, ns, nc, nt = tobj.n
#     if dbg: flog(f'BGN {tobj.kbkEvntTxt()} motion={motion}')
#     if   isNumLck(   tobj.mods):                         msg =             f'NUMLOCK(         {motion})'   ;   flog(msg)   ;   pygwink.MOD_NUMLOCK = 0
#     if   isCtlAltSft(tobj.mods):                         msg =             f'@&^(             {motion})'   ;   flog(msg) #  ;   self.quit(msg)
#     elif isCtlAlt(   tobj.mods):
#         if   motion == 1:                                tobj.unselectTabs(f'@& LEFT(         {motion})',  nt)
#         elif motion == 2:                                tobj.unselectTabs(f'@& RIGHT(        {motion})', -nt)
#         else:                                            msg =             f'@& (             {motion})'   ;   flog(msg) #  ;   self.quit(msg)
#     elif isAltSft(   tobj.mods):                         msg =             f' &^(             {motion})'   ;   flog(msg) #  ;   self.quit(msg)
#     elif isCtlSft(   tobj.mods):                         msg =             f'@^(              {motion})'   ;   flog(msg) #  ;   self.quit(msg)
#     elif isSft(      tobj.mods):                         msg =             f'^ (              {motion})'   ;   flog(msg) #  ;   self.quit(msg)
#     elif isAlt(      tobj.mods):
#         if   motion == pygwink.MOTION_UP:                tobj.moveUp(      f' & UP(           {motion})')
#         elif motion == pygwink.MOTION_DOWN:              tobj.moveDown(    f' & DOWN(         {motion})')
#         elif motion == pygwink.MOTION_LEFT:              tobj.moveLeft(    f' & LEFT(         {motion})')
#         elif motion == pygwink.MOTION_RIGHT:             tobj.moveRight(   f' & RIGHT(        {motion})')
#         elif motion == pygwink.MOTION_BEGINNING_OF_LINE: tobj.move(        f' & HOME(         {motion})', -nt *  c)
#         elif motion == pygwink.MOTION_END_OF_LINE:       tobj.move(        f' & END(          {motion})',  nt * (nc - tobj.i[C]))
#         elif motion == pygwink.MOTION_PREVIOUS_PAGE:     tobj.prevPage(    f' & PAGE UP(      {motion})')
#         elif motion == pygwink.MOTION_NEXT_PAGE:         tobj.nextPage(    f' & PAGE DOWN(    {motion})')
#         else:                                            msg =             f' &(              {motion})'   ;   flog(msg)   ;   tobj.quit(msg)
#     elif isCtl(tobj.mods):
#         if   motion == pygwink.MOTION_NEXT_WORD:         tobj.selectTabs(  f'@  RIGHT(        {motion})',  nt)
#         elif motion == pygwink.MOTION_PREVIOUS_WORD:     tobj.selectTabs(  f'@  LEFT(         {motion})', -nt)
#         elif motion == pygwink.MOTION_BEGINNING_OF_LINE: msg = f'@  MOTION_BEGINNING_OF_LINE( {motion})'   ;   flog(msg)   ;   tobj.quit(msg) # N/A
#         elif motion == pygwink.MOTION_END_OF_LINE:       msg = f'@  MOTION_END_OF_LINE(       {motion})'   ;   flog(msg)   ;   tobj.quit(msg) # N/A
#         elif motion == pygwink.MOTION_BEGINNING_OF_FILE: msg = f'@  MOTION_BEGINNING_OF_FILE( {motion})'   ;   flog(msg)   ;   tobj.quit(msg) # CTRL HOME
#         elif motion == pygwink.MOTION_END_OF_FILE:       msg = f'@  MOTION_END_OF_FILE(       {motion})'   ;   flog(msg)   ;   tobj.quit(msg) # CTRL END
# #           elif motion == pygwink.MOTION_DELETE:            self.deleteTabs( f'@ D MOTION_DELETE({motion})')
# #           elif motion == pygwink.MOTION_COPY:              self.copyTabs(   f'@ C MOTION_COPY(  {motion})')
# #           elif motion == pygwink.MOTION_PASTE:             self.pasteTabs(  f'@ V MOTION_PASTE( {motion})', kk=0)
#         else:                                            msg =             f'UNH CTRL(        {motion}) {tobj.kbkEvntTxt()}'   ;   flog(msg) #  ;   self.quit(msg)
#     elif tobj.mods == 0:
#         if   motion == pygwink.MOTION_UP:                tobj.move(        f' UP(             {motion})', -1)
#         elif motion == pygwink.MOTION_DOWN:              tobj.move(        f' DOWN(           {motion})',  1)
#         elif motion == pygwink.MOTION_LEFT:              tobj.move(        f' LEFT(           {motion})', -nt)
#         elif motion == pygwink.MOTION_RIGHT:             tobj.move(        f' RIGHT(          {motion})',  nt)
#         elif motion == pygwink.MOTION_PREVIOUS_WORD:     msg = f'MOTION_PREVIOUS_WORD(        {motion})'   ;   flog(msg)   ;   tobj.quit(msg)
#         elif motion == pygwink.MOTION_NEXT_WORD:         msg = f'MOTION_NEXT_WORD(            {motion})'   ;   flog(msg)   ;   tobj.quit(msg)
#         elif motion == pygwink.MOTION_BEGINNING_OF_LINE: tobj.move(        f' HOME(           {motion})', -nt *  c)
#         elif motion == pygwink.MOTION_END_OF_LINE:       tobj.move(        f' END(            {motion})',  nt * (nc - tobj.i[C]))
#         elif motion == pygwink.MOTION_BEGINNING_OF_FILE: msg = f'MOTION_BEGINNING_OF_FILE(    {motion})'   ;   flog(msg)   ;   tobj.quit(msg)
#         elif motion == pygwink.MOTION_END_OF_FILE:       msg = f'MOTION_END_OF_FILE(          {motion})'   ;   flog(msg)   ;   tobj.quit(msg)
#         elif motion == pygwink.MOTION_PREVIOUS_PAGE:     tobj.moveUp(      f' PAGE UP(        {motion})')  # go up   to top    of line, wrap down to bottom of prev line
#         elif motion == pygwink.MOTION_NEXT_PAGE:         tobj.moveDown(    f' PAGE DOWN(      {motion})')  # go down to bottom tab on same line, wrap to next line
#         elif motion == pygwink.MOTION_DELETE:            tobj.setTab(      f'DELETE(          {motion})', tobj.tblank)
#         elif motion == pygwink.MOTION_BACKSPACE:         tobj.setTab(      f'BACKSPACE(       {motion})', tobj.tblank, rev=1)
#         else:                                            msg =             f'(                {motion})'   ;   flog(msg)   ;   tobj.quit(msg)
#     if dbg: flog(f'END {tobj.kbkEvntTxt()} motion={motion}')
#     return True

#        1353 tabs.py       on_text_motion BGN <   65363> <   65363> <RIGHT           > <16> <MOD_NUMLOCK     > motion=65363
#        1353 tabs.py       on_text_motion BGN <   65363> <   65363> <RIGHT           > < 8> <MOD_CAPSLOCK    > motion=65363
