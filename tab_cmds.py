#import os, pathlib, sys #, glob
#import inspect, operator #, math
import itertools #, colletions
#from   collections     import Counter
#from   itertools       import accumulate
##from   more_itertools  import consume  # not installed in GitBash's Python
#import pyglet
#import pyglet.font         as pygfont
#import pyglet.image        as pygimg
import pyglet.sprite       as pygsprt
import pyglet.text         as pygtxt
import pyglet.window.key   as pygwink
#import pyglet.window.event as pygwine
#from   pyglet.text     import document, layout
from   tpkg            import utl    as utl
from   tpkg            import kysgs  as kysgs
#from   tpkg            import misc   as misc
#from   tpkg            import evnts  as evnts
from   tpkg.notes      import Notes  as Notes
#from   tpkg.strngs     import Strngs as Strngs
#from   tpkg.chords     import Chords as Chords

P, L, S, C,          T, N, I, K,          M, R, Q, H,          B, A, D, E   = utl.P, utl.L, utl.S, utl.C,    utl.T, utl.N, utl.I, utl.K,    utl.M, utl.R, utl.Q, utl.H,    utl.B, utl.A, utl.D, utl.E
W, X, Y, Z,       NONE,  ist,  fri,         slog,   fmtf,   fmtl,   fmtm    = utl.W, utl.X, utl.Y, utl.Z,    utl.NONE,   utl.ist,   utl.fri,       utl.slog,   utl.fmtf,   utl.fmtl,   utl.fmtm
BGC,  BOLD,  COLOR,     FONT_NAME,  FONT_SIZE, ITALIC,  KERNING,  UNDERLINE = utl.BGC,   utl.BOLD,  utl.COLOR,   utl.FONT_NAME, utl.FONT_SIZE, utl.ITALIC,   utl.KERNING,     utl.UNDERLINE
isAlt, isCtl, isShf,    isAltShf, isCtlAlt, isCtlShf, isCtlAltShf, isNumLck = utl.isAlt, utl.isCtl, utl.isShf,   utl.isCtlAlt,  utl.isAltShf,  utl.isCtlShf, utl.isCtlAltShf, utl.isNumLck

CAT,  CSV,  EVN,  LOG,  PNG,  TXT,  DAT  =     'cat' ,     'csv' ,     'evn',      'log' ,     'png' ,     'txt' ,     'dat'
CATS, CSVS, EVNS, LOGS, PNGS, TEXT, DATA =     'cats',     'csvs',     'evns',     'logs',     'pngs',     'text',     'data'
CAT2, CSV2, EVN2, LOG2, PNG2, TXT2, DAT2 = f'_.{CAT}', f'_.{CSV}', f'_.{EVN}', f'_.{LOG}', f'_.{PNG}', f'_.{TXT}', f'_.{DAT}'
CSV_FILE, EVN_FILE, LOG_FILE, TXT_FILE   = None, None, None, None
BASE_NAME,        BASE_PATH,        PATH = utl.paths()
CSV_PATH  = utl.getFilePath(BASE_NAME, BASE_PATH, fdir=CSVS, fsfx=CSV,  dbg=0)
DAT_PATH  = utl.getFilePath(BASE_NAME, BASE_PATH, fdir=DATA, fsfx=DAT,  dbg=0)
EVN_PATH  = utl.getFilePath(BASE_NAME, BASE_PATH, fdir=EVNS, fsfx=EVN,  dbg=0)
LOG_PATH  = utl.getFilePath(BASE_NAME, BASE_PATH, fdir=LOGS, fsfx=LOG,  dbg=0)
PNG_PATH  = utl.getFilePath(BASE_NAME, BASE_PATH, fdir=PNGS, fsfx=PNG,  dbg=0)
TXT_PATH  = utl.getFilePath(BASE_NAME, BASE_PATH, fdir=TEXT, fsfx=TXT,  dbg=0)

CSV_PATH2 = utl.getFilePath(BASE_NAME, BASE_PATH, fdir=CSVS, fsfx=CSV2, dbg=0)
DAT_PATH2 = utl.getFilePath(BASE_NAME, BASE_PATH, fdir=DATA, fsfx=DAT2, dbg=0)
EVN_PATH2 = utl.getFilePath(BASE_NAME, BASE_PATH, fdir=EVNS, fsfx=EVN2, dbg=0)
LOG_PATH2 = utl.getFilePath(BASE_NAME, BASE_PATH, fdir=LOGS, fsfx=LOG2, dbg=0)
PNG_PATH2 = utl.getFilePath(BASE_NAME, BASE_PATH, fdir=PNGS, fsfx=PNG2, dbg=0)
TXT_PATH2 = utl.getFilePath(BASE_NAME, BASE_PATH, fdir=TEXT, fsfx=TXT2, dbg=0)

MULTILINE, WRAP_LINES = 'multiline', 'wrap_lines'    ;  LEFT, CENTER, RIGHT, BOTTOM, BASELINE, TOP = 'left', 'center', 'right', 'bottom', 'baseline', 'top'
ALIGN, INDENT, LEAD, LNSP, STRH, TAB_STOPS, WRAP     = 'align', 'indent', 'leading', 'line_spacing', 'stretch', 'tab_stops', 'wrap'
MARGIN_LEFT, MARGIN_RIGHT, MARGIN_TOP, MARGIN_BOTTOM = 'margin_left', 'margin_right', 'margin_top', 'margin_bottom'
TI        = ['tnik', '  i ']
XYWH      = ['   X   ', '   Y   ', '   W   ', '   H   ']
AXY2      = ['x', 'y', 'AnchX', 'AnchY']
CWH       = ['CntWd', 'CntHt']
CVA       = ['v', 'a']
ADS       = ['Ascnt', 'Dscnt', 'As+Ds']
LTXA      = list(itertools.chain(TI, XYWH, AXY2))
LTXAC     = list(itertools.chain(TI, XYWH, AXY2, CWH))
LDS       = ['FnSz', 'Lead', 'LnSp', 'TablText', ' ForegroundColor ', ' BackgroundColor ', 'B', 'I', 'S', 'M', 'W', 'w', 'FontName']
LLBL      = list(itertools.chain(LTXAC, ADS, CVA, LDS))
########################################################################################################################################################################################################
TT, NN, II, KK                 = utl.TT, utl.NN, utl.II, utl.KK
MELODY, CHORD, ARPG            = utl.MELODY, utl.CHORD, utl.ARPG
LARROW, RARROW, DARROW, UARROW = utl.LARROW, utl.RARROW, utl.DARROW, utl.UARROW
LBL                   = pygtxt.Label
SPR                   = pygsprt.Sprite
RGB                   = utl.RGB
C1,  C2               =  0,  1
CSR_MODES             = ['MELODY', 'CHORD', 'ARPG']
HARROWS, VARROWS      = ['LARROW', 'RARROW'], ['DARROW', 'UARROW']
NORMAL_STYLE, SELECT_STYLE, CURRENT_STYLE = 0, 1, 2
########################################################################################################################################################################################################
FIN     = [1, 1, 1, 2, 1]
FNTP    = [5, 4, 3, 3, 3]
#           0        1        2        3           4        5        6        7           8        9        10       11          12       13       14       15          16
JTEXTS  = ['Page',  'Line',  'Sect',  'Colm',     'Tabl',  'Note',  'IKey',  'Kord',     'MVie',  'RowL',  'QClm',  'HCrs',     'BNum',  'ANam',  'DCpo',  'EClm',     'TNIK']
JTEXTS2 = ['Page',  'Line',  'Sect',  'Kolm',     'Tabl',  'Note',  'IKey',  'Kord',     'MVie',  'RowL',  'QKlm',  'HCrs',     'BNum',  'ANam',  'DCpo',  'EClm',     'TNIK']
jTEXTS  = ['pages', 'lines', 'sects', 'colms',    'tabls', 'notes', 'ikeys', 'Kords',    'mvies', 'rowls', 'qklms', 'hcsrs',    'bnums', 'anams', 'dcpos', 'eclms',    'tniks']
JFMT    = [ 1,       2,       2,       3,          4,       4,       4,       4,          1,       2,       3,       1,          2,       2,       2,       2,          4]
#JFMT   = [ 2,       3,       3,       6,          6,       6,       6,       6,          1,       3,       5,       1,          3,       3,       3,       4,          7]
PNT_PER_PIX =  7/9  # 14pts/18pix
FONT_DPIS   = [ 72, 78, 84, 90, 96, 102, 108, 114, 120 ]
FONT_NAMES  = [ 'Lucida Console', 'Times New Roman', 'Arial', 'Courier New', 'Helvetica', 'Century Gothic', 'Bookman Old Style', 'Antique Olive' ]


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
    if   kbk == 'A' and isCtlShf(kd, m):     tobj.flipArrow(    '@^A', v=1)
    elif kbk == 'A' and isCtl(   kd, m):     tobj.flipArrow(    '@ A', v=0)
    elif kbk == 'B' and isCtlShf(kd, m):     tobj.flipBlank(    '@^B')
    elif kbk == 'B' and isCtl(   kd, m):     tobj.flipBlank(    '@ B')
    elif kbk == 'C' and isCtlShf(kd, m):     tobj.copyTabs(     '@^C')
    elif kbk == 'C' and isCtl(   kd, m):     tobj.copyTabs(     '@ C')
    elif kbk == 'D' and isCtlShf(kd, m):     tobj.deleteTabs(   '@^D')
    elif kbk == 'D' and isCtl(   kd, m):     tobj.deleteTabs(   '@ D')
    elif kbk == 'E' and isCtlShf(kd, m):     tobj.eraseTabs(    '@^E')
    elif kbk == 'E' and isCtl(   kd, m):     tobj.eraseTabs(    '@ E')
    elif kbk == 'F' and isCtlShf(kd, m):     tobj.flipFullScrn( '@^F') # FULL_SCREEN
    elif kbk == 'F' and isCtl(   kd, m):     tobj.flipFlatShrp( '@ F') # FLAT_SHARP
    elif kbk == 'G' and isCtlShf(kd, m):     tobj.move2LastTab( '@^G', page=1)
    elif kbk == 'G' and isCtl(   kd, m):     tobj.move2LastTab( '@ G', page=0)
    elif kbk == 'H' and isCtlShf(kd, m):     tobj.move2FirstTab('@^H', page=1)
    elif kbk == 'H' and isCtl(   kd, m):     tobj.move2FirstTab('@ H', page=0)
    elif kbk == 'I' and isCtlShf(kd, m):     tobj.insertSpace(  '@^I')
    elif kbk == 'I' and isCtl(   kd, m):     tobj.flipTTs(      '@ I', II)
    elif kbk == 'J' and isCtlShf(kd, m):     tobj.jump(         '@^J', a=1)
    elif kbk == 'J' and isCtl(   kd, m):     tobj.jump(         '@ J', a=0)
    elif kbk == 'K' and isCtlShf(kd, m):     tobj.flipTTs(      '@^K', KK)
    elif kbk == 'K' and isCtl(   kd, m):     tobj.flipTTs(      '@ K', KK)
    elif kbk == 'L' and isCtlShf(kd, m):     tobj.flipLLs(      '@^L')
    elif kbk == 'L' and isCtl(   kd, m):     tobj.flipLLs(      '@ L')
    elif kbk == 'N' and isCtlShf(kd, m):     tobj.flipTTs(      '@^N', NN)
    elif kbk == 'N' and isCtl(   kd, m):     tobj.flipTTs(      '@ N', NN)
    elif kbk == 'O' and isCtlShf(kd, m):     tobj.flipCrsrMode( '@^O', -1)
    elif kbk == 'O' and isCtl(   kd, m):     tobj.flipCrsrMode( '@ O', 1)
    elif kbk == 'P' and isCtlShf(kd, m):     tobj.addPage(      '@^P', ins=0)
    elif kbk == 'P' and isCtl(   kd, m):     tobj.addPage(      '@ P', ins=None)
    elif kbk == 'R' and isCtlShf(kd, m):     tobj.flipKordNames('@^R', hit=1)
    elif kbk == 'R' and isCtl(   kd, m):     tobj.flipKordNames('@ R', hit=0)
    elif kbk == 'S' and isCtlShf(kd, m):     tobj.shiftTabs(    '@^S')
#   elif kbk == 'S' and isCtl(   kd, m):     tobj.saveDataFile( '@ S', self.dataPath1)
    elif kbk == 'S' and isCtl(   kd, m):     tobj.swapTab(      '@ S', txt=Z)
    elif kbk == 'T' and isCtlShf(kd, m):     tobj.flipTTs(      '@^T', TT)
    elif kbk == 'T' and isCtl(   kd, m):     tobj.flipTTs(      '@ T', TT)
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
    elif kbk == 'TAB' and isCtl(kd, m):      tobj.setCHVMode(   '@ TAB',      MELODY, LARROW)
    elif kbk == 'TAB':                       tobj.setCHVMode(   '  TAB',      MELODY, RARROW)
#   elif kbk == 'SLASH'     and isCtl(mods): tobj.setCHVMode(  '@ SLASH',     ARPG,   LARROW, DARROW)
#   elif kbk == 'SLASH':                     tobj.setCHVMode(  '  SLASH',     ARPG,   RARROW, UARROW)
#   elif kbk == 'BACKSLASH' and isCtl(mods): tobj.setCHVMode(  '@ BACKSLASH', ARPG,   LARROW, UARROW)
#   elif kbk == 'BACKSLASH':                 tobj.setCHVMode(  '  BACKSLASH', ARPG,   RARROW, DARROW)

    ####################################################################################################################################################################################################
    elif kbk == 'A' and isAltShf(kd, m):     tobj.flipBGC(      '&^A')
    elif kbk == 'A' and isAlt(   kd, m):     tobj.flipBGC(      '& A')
    elif kbk == 'D' and isAltShf(kd, m):     tobj.flipDrwBGC(   '&^D', -1)
    elif kbk == 'D' and isAlt(   kd, m):     tobj.flipDrwBGC(   '& D',  1)
    elif kbk == 'N' and isAltShf(kd, m):     tobj.setn_cmd(     '&^N', txt=Z)
    elif kbk == 'N' and isAlt(   kd, m):     tobj.setn_cmd(     '& N', txt=Z)
    elif kbk == 'P' and isAltShf(kd, m):     tobj.flipPage(     '&^P', -1)
    elif kbk == 'P' and isAlt(   kd, m):     tobj.flipPage(     '& P',  1)
    elif kbk == 'R' and isAltShf(kd, m):     tobj.rotateSprite( '&^R', hcurs[0], -1)
    elif kbk == 'R' and isAlt(   kd, m):     tobj.rotateSprite( '& R', hcurs[0],  1)
    elif kbk == 'V' and isAltShf(kd, m):     tobj.flipVisible(  '&^V', dbg=1)
    elif kbk == 'V' and isAlt(kd, m):        tobj.flipVisible(  '& V', dbg=1)

    ####################################################################################################################################################################################################
    elif kbk == 'B' and isAltShf(kd, m):     tobj.setFontParam(BOLD,      not fontBold,   'fontBold')
    elif kbk == 'B' and isAlt(   kd, m):     tobj.setFontParam(BOLD,      not fontBold,   'fontBold')
    elif kbk == 'C' and isAltShf(kd, m):     tobj.setFontParam(COLOR,        -1,          'clrIdx')
    elif kbk == 'C' and isAlt(   kd, m):     tobj.setFontParam(COLOR,         1,          'clrIdx')
    elif kbk == 'I' and isAltShf(kd, m):     tobj.setFontParam(ITALIC,    not fontItalic, 'fontItalic')
    elif kbk == 'I' and isAlt(   kd, m):     tobj.setFontParam(ITALIC,    not fontItalic, 'fontItalic')
    elif kbk == 'M' and isAltShf(kd, m):     tobj.setFontParam(FONT_NAME,    -1,          'fontNameIdx')
    elif kbk == 'M' and isAlt(   kd, m):     tobj.setFontParam(FONT_NAME,     1,          'fontNameIdx')
    elif kbk == 'S' and isAltShf(kd, m):     tobj.setFontParam(FONT_SIZE,     33 / 32,    'fontSize')
    elif kbk == 'S' and isAlt(   kd, m):     tobj.setFontParam(FONT_SIZE,     32 / 33,    'fontSize')

    else:  retv = False   ;   slog(f'UNH {fsm(symb, mods)} kd={fmtm(kd)}') if dbg else None
    ####################################################################################################################################################################################################
    if  not  tobj.isParsing():
        if   kbk == 'ENTER' and isCtl(kd, m):     tobj.setCHVMode(  '@  ENTER',     CHORD,  v=DARROW)
        elif kbk == 'ENTER':                      tobj.setCHVMode(  '   ENTER',     CHORD,  v=UARROW)
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
#        elif motion == k.MOTION_NEXT_PAGE:         msg = f'@ MOTION_NEXT_PAGE(         {motion})'   ;   slog(msg)   ;   retv = False
        elif motion == k.MOTION_NEXT_PAGE:         cmd = cmds.TogPageCmd(tobj,     '@  MOTION_NEXT_PAGE', motion)        ;  cmd.do()     
        elif motion == k.MOTION_DELETE:            cmd = cmds.DeleteTabsCmd(tobj, f'@ D MOTION_DELETE({motion})')        ;  cmd.do()
        elif motion == k.MOTION_COPY:              cmd = cmds.CopyTabsCmd(tobj,   f'@ C MOTION_COPY(  {motion})')        ;  cmd.do() # todo fixme also fires '@ C'
        elif motion == k.MOTION_PASTE:             cmd = cmds.PasteTabsCmd(tobj,  f'@ V MOTION_PASTE( {motion})', kk=0)  ;  cmd.do() # todo fixme also fires '@ V'
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
        elif motion == k.MOTION_NEXT_PAGE:         tobj.moveDown(    f' PAGE DOWN(     {motion})')  # go down to bottom tab on same line, wrap to next line
        elif motion == k.MOTION_COPY:              msg =             f' MOTION_COPY(   {motion})'   ;   slog(msg)   ;   retv = False
        elif motion == k.MOTION_DELETE:            tobj.setTab(      f'DELETE(         {motion})', tobj.tblank)
        elif motion == k.MOTION_BACKSPACE:         tobj.setTab(      f'BACKSPACE(      {motion})', tobj.tblank, rev=1)
        elif motion == k.MOTION_PREVIOUS_WORD:     msg = f'MOTION_PREVIOUS_WORD(       {motion})'   ;   slog(msg)   ;   retv = False # tobj.quit(msg) # N/A
        elif motion == k.MOTION_NEXT_WORD:         msg = f'MOTION_NEXT_WORD(           {motion})'   ;   slog(msg)   ;   retv = False # tobj.quit(msg) # N/A
        elif motion == k.MOTION_BEGINNING_OF_FILE: msg = f'MOTION_BEGINNING_OF_FILE(   {motion})'   ;   slog(msg)   ;   retv = False # tobj.quit(msg) # N/A
        elif motion == k.MOTION_END_OF_FILE:       msg = f'MOTION_END_OF_FILE(         {motion})'   ;   slog(msg)   ;   retv = False # tobj.quit(msg) # N/A
#       else:                                      msg =             f'UNH(            {motion})'   ;   slog(msg)   ;   retv = False  ;  tobj.quit(msg)
    if dbg: slog(f'END {ftm(motion)} {retv=}')
    return retv

def flipArrow(self, how, v=0, dbg=0):
    if dbg: self.log(f'BGN {how} {v=} {self.hArrow=} = {HARROWS[self.hArrow]=} {self.vArrow=} = {VARROWS[self.vArrow]=}')
    if v:   self.vArrow  = (self.vArrow + 1) % len(VARROWS)
    else:   self.hArrow  = (self.hArrow + 1) % len(HARROWS)
    if dbg: self.log(f'END {how} {v=} {self.hArrow=} = {HARROWS[self.hArrow]=} {self.vArrow=} = {VARROWS[self.vArrow]=}')
########################################################################################################################################################################################################
def flipBlank(self, how):
    prevBlank    =  self.tblank
    self.log(f'BGN {how} {prevBlank=}')
    self.tblanki = (self.tblanki + 1) % len(self.tblanks)
    self.tblank  =  self.tblanks[self.tblanki]
    self.swapSrc, self.swapTrg, self.swapping = prevBlank, self.tblank, 2
    self.swapTab(how, '\r')
    self.swapSrc, self.swapTrg = Z, Z
    self.log(f'END {how} {self.tblank=}')
    ####################################################################################################################################################################################################
def flipFlatShrp(self, how, dbg=0):  #  page line colm tab or select
    t1 = Notes.TYPE    ;    t2 =  Notes.TYPE * -1      ;     Notes.TYPE = t2
    self.log(  f'BGN {how} {t1=} {Notes.TYPES[t1]} => {t2=} {Notes.TYPES[t2]}')
    s = self.ss2sl()[0]  ;  np, nl, ns, nc, nt = self.i
    tniks, j, _, tobj = self.tnikInfo(0, 0, s, 0, 0, why=how)
    for i in range(len(tniks)):
        text = Z  ;   sn = i % nt
        if   self.notes: text = self.notes[i].text
        elif self.kords and self.tabls:
            tabtxt = self.tabls[i].text
            text   = self.sobj.tab2nn(tabtxt, sn) if self.sobj.isFret(tabtxt) else self.tblank
        if text in Notes.N2I and (Notes.N2I[text] not in Notes.IS0):
            cc = i * ns    ;   old = text
            p, l, c, t = self.cc2plct(cc)   ;   cn = self.cc2cn(cc)
            if   text in Notes.F2S:  text = Notes.F2S[text]
            elif text in Notes.S2F:  text = Notes.S2F[text]
            self.notes[i].text     = text
            self.log(  f'{old:2} -> {text:2} = ')
            if dbg: self.log(f'{sn=} {cn=:2} {cc=:4} {i=:4} {old:2} => {text:2} {self.notes[i].text=:2} {self.fplct(p, l, c, t)}')
            if self.kords:
                imap = self.getImap(p, l, c, dbg2=1)
                self.setChord(imap, i, pos=1, dbg=1)
    kysgs.dumpNic(dict(self.nic))
    self.log(kysgs.fmtKSK(self.ks[kysgs.KSK]), f=2)
    self.log(  f'END {how} {t1=} {Notes.TYPES[t1]} => {t2=} {Notes.TYPES[t2]}')
########################################################################################################################################################################################################
def flipFullScrn(self, how):
    self.FULL_SCRN = not self.FULL_SCRN
    self.set_fullscreen( self.FULL_SCRN)
    self.log(   f'{how} {self.FULL_SCRN}=')
########################################################################################################################################################################################################
def flipPage(self, how, a=1, dbg=1):
    if dbg: self.log(f'BGN {how} {a=} {self.i[P]=}')
    self.flipVisible(how=how)
#   self.i[P] = (self.i[P] + a) % self.n[P]
    self.i[P] = (self.j()[P] + a) % self.n[P] + 1
    if dbg: self.log(f'    {how} {a=} {self.i[P]=}')
    self.flipVisible(how=how)
    self.dumpVisible() # ;   self.dumpVisible2()
    self.setCaption(f'{utl.ROOT_DIR}/{DATA}/{self.FILE_NAME}.{DAT} page {self.i[P]}')
    if dbg: self.log(f'END {how} {a=} {self.i[P]=}')
########################################################################################################################################################################################################
def flipVisible(self, how=None, dbg=1):  # page 1 pass (1 & 2 & 3 or 2 & 3), page 2 pass (1 & 2 & 3 or 1 & 3), page 3 pass (1 & 2 & 3 or 1 & 2)
    why = 'FVis' if how is None else how       ;  np, nl, ns, nc, nt = self.n
    p, l, s, c  = self.j()[P], 0, 0, 0         ;  vl = []  ;  tpb, tpp, tpl, tps, tpc = self.ntp(dbg=1, dbg2=1)
    self.J1, self.J2 = self.p2Js(p)
    pid = f' {id(self.pages[p]):11x}' if self.OIDS else Z
    assert 0 <= p < len(self.pages), f'{p=} {len(self.pages)=} {self.fmtn()} {self.fmti()} {self.J1} {self.J2}'
    self.log(f'BGN {why} {pid} pages[{p}].v={int(self.pages[p].visible)} {self.fmti()} {self.fmtn()} page{p+1} is visibile {self.fVis()}')
    self.dumpTniksPfx(why, r=0)
    assert 0 <= p < len(self.pages), f'{p=} {len(self.pages)=}'
    page = self.pages[p]              ;  page.visible = not page.visible  ;  self.setJdump(P, p, page.visible, why=why)  ;  vl.append(str(int(page.visible))) if dbg else None
    for l in range(nl):
        line = self.lines[l]          ;  line.visible = not line.visible  ;  self.setJdump(L, l, line.visible, why=why)  ;  vl.append(str(int(line.visible))) if dbg else None
        for s, s2 in enumerate(self.ss2sl()):
            sect = self.sects[s]      ;  sect.visible = not sect.visible  ;  self.setJdump(S, s, sect.visible, why=why)  ;  vl.append(str(int(sect.visible))) if dbg else None
            for c in range(nc):
                colm = self.colms[c]  ;  colm.visible = not colm.visible  ;  self.setJdump(C, c, colm.visible, why=why)  ;  vl.append(str(int(colm.visible))) if dbg else None
                for t in range(nt):
                    tniks, j, k, txt = self.tnikInfo(p, l, s2, c, t, why=why)
                    t2 = t + c*tpc + l*tpl + p*tpp//ns
                    assert t2 < len(tniks),  f'ERROR {t2=} {len(tniks)=}'
                    tnik = tniks[t2]  ;  tnik.visible = not tnik.visible  ;  self.setJdump(j, t2, tnik.visible, why=why)  ;  vl.append(str(int(tnik.visible))) if dbg else None
    self.dumpTniksSfx(why)
    self.log(f'END {why} {pid} pages[{p}].v={int(self.pages[p].visible)} {self.fmti()} {self.fmtn()} page{p+1} is visible {self.fVis()}')
########################################################################################################################################################################################################
def flipKordNames(self, how, hit=0, dbg=1):
    cc = self.cc    ;    cn = self.cc2cn(cc)
    mks = list(self.cobj.mlimap.keys())   ;   sks = list(self.smap.keys())
    if sks and not hit:
        if dbg: self.dumpSmap(f'BGN {how} mks={fmtl(mks)} {cn=:2} {hit=} sks={fmtl(sks)}')
        [ self.flipKordName(how, k) for k in sks ]
    else:
        if dbg: self.dumpSmap(f'BGN {how} mks={fmtl(mks)} {cn=:2} {hit=} sks={fmtl(sks)}')
        if hit: self.flipKordNameHits(how, cn)
        else:   self.flipKordName(    how, cn)
    if dbg:     self.dumpSmap(f'END {how} mks={fmtl(mks)} {cn=:2} {hit=} sks={fmtl(sks)}')

def flipKordNameHits(self, how, cn, dbg=1): # optimize str concat?
    mli = self.cobj.mlimap   ;   mks = list(mli.keys())   ;   cn2 = -1
    if cn not in mks: msg = f'ERROR: {cn=} not in {fmtl(mks)=}'   ;   self.log(msg)   ;   self.quit(msg)
    ivals =  [ u[1] for u in mli[cn][0] ]
    msg   =  [ fmtl(v, w="x") for v in ivals ]
    if dbg: self.log(f'BGN {how} mks={fmtl(mks)} cn={cn:2} ivals={fmtl(msg, d=Z)}')
    hits = self.ivalhits(ivals, how)
    for cn2 in hits:
        if cn2 not in self.smap: self.selectTabs(how, m=0, cn=cn2)
        self.flipKordName(how, cn2)
    if dbg: self.log(f'END {how} mks={fmtl(mks)} cn2={cn2:2} ivals={fmtl(msg, d=Z)}')

def ivalhits(self, ivals, how, dbg=1):
    mli = self.cobj.mlimap    ;   mks = list(mli.keys())   ;   hits = set()
    for cn, lim in mli.items():
        for im in lim[0]:
            if cn in hits: break
            for iv in ivals:
                iv1 = sorted(iv)  ;  iv2 = sorted(im[1])
                if iv1 == iv2:       hits.add(cn)   ;   break
    if dbg: self.log(f'    {how} mks={fmtl(mks)} hits={fmtl(hits)}')
    return list(hits)

def flipKordName(self, how, cn, dbg=1, dbg2=1):
    cc = self.cn2cc(cn)            ;   mli = self.cobj.mlimap
    p, l, c, t = self.cc2plct(cc)  ;   msg = Z
    if not self.ikeys and not self.kords: msg +=  'ERROR: Both ikeys and chords are Empty '
    if cn not in mli:                     msg += f'ERROR: {cn=} not in mks={fmtl(list(mli.keys()))}'
    if msg: self.log(msg)          ;   return
    limap      = mli[cn][0]        ;   imi = mli[cn][1]
    imi        = (imi + 1) % len(limap)
    mli[cn][1] = imi
    ikeys, ivals, notes2, chordName, chunks, rank = limap[imi]
    if self.ikeys and ikeys:                self.setIkeyText(ikeys, cc, p, l, c)
    if self.kords and chordName and chunks: self.setChordName(cc, chordName, chunks)
    elif dbg: self.log(f'    {how} {cn=} {cc=} is NOT a chord')
    if dbg2:  self.cobj.dumpImap(limap[imi], why=f'{cn:2}')
#    assert imi == limap[imi][-1],   f'{imi=} {limap[imi][-1]=}'
########################################################################################################################################################################################################
def setFontParam(self, n, v, m, dbg=1):
    if   m == 'clrIdx':      v += getattr(self, m)   ;   v %= len(self.k)      ;  self.log(f'{n=:12} {v=:2} {self.clrIdx=:2}')
    elif m == 'fontNameIdx': v += getattr(self, m)   ;   v %= len(FONT_NAMES)  ;  self.log(f'{n=:12} {v=:2} {self.fontNameIdx=:2}')
    setattr(self, m, v)
    ts = list(itertools.chain(self.A, self.B, self.C))  ;  lt = len(ts)
    if dbg:         self.log(f'{lt=} {m=:12} {n=:12} {fmtf(v, 5)}')
    for j, t in enumerate(ts):
#            if dbg:     self.log(f'{j=:2} {W*3} {lt=} {m=:12} {n=:12} {v=:2}', p=0) #  and self.VRBY
        self._setFontParam(t, n, v, m, j)
    if dbg:         self.log(f'{lt=} {m=:12} {n=:12} {fmtf(v, 5)}')  # and self.VRBY
    self.setCaption(self.fmtFont())

def _setFontParam(self, ts, n, v, m, j, dbg=1):
    l = 0   ;   fb = 0   ;   fs = 1   ;   msg = Z
    for i, t in enumerate(ts):
        if ist(t, LBL):
            if   m == 'clrIdx':       l = len(t.color)   ;  msg = f'{v=:2} tc={fmtl(t.color, w=3)}  ds={fmtl(t.document.get_style(n), w=3)}  kv={fmtl(self.k[v][fb][:l], w=3)}'
            elif m == 'fontNameIdx':                        msg = f'{v=:2} {FONT_NAMES[v]=}'
            elif m == 'fontSize':    fs = getattr(t, n)  ;  msg = f'{v=:.2f} {fs=:.2f}'
            if dbg and ist(t, LBL) and i==0:            self.log(f'{j=:2} {i=:2}  {l} {fb} {m=:12} {n=:12} {msg}', f=2)
            if   m == 'clrIdx':       self._setTNIKStyle(t, self.k[v], self.fontStyle)
            elif m == 'fontNameIdx':  setattr(t, n, FONT_NAMES[v])
            elif m == 'fontSize':     setattr(t, n, v*fs)
            else:                     setattr(t, n, v)
########################################################################################################################################################################################################
def flipDrwBGC(self, how, a):
    self.drwBGC += a
    self.log(f'{how} {self.drwBGC=}')
########################################################################################################################################################################################################
def flipBGC(self, how=Z):
    self.log(f'{how} {self.BGC=}') if how else None
    self.BGC = (1 + self.BGC) % 2
    self.setFontParam2(self.tabls, COLOR, self.BGC, 'clrIdx', T)
########################################################################################################################################################################################################
def setn_cmd(self, how, txt=Z, dbg=1): # optimize str concat?
    if not self.settingN: self.settingN = 1   ;  self.setNtxt = Z  ;  self.log(f'BGN {how} {txt=} {self.settingN=} {self.setNvals=}') if dbg else None
    elif txt.isdecimal(): self.setNtxt += txt                      ;  self.log(   f'Concat {txt=} {self.settingN=} {self.setNvals=}') if dbg else None
    elif txt ==  W:       self.setNvals.append(int(self.setNtxt))  ;  self.log(   f'Append {txt=} {self.settingN=} {self.setNvals=}') if dbg else None  ;  self.setNtxt = Z
    elif txt == 'Q':      self.settingN = 0                        ;  self.log(   f'Cancel {txt=} {self.settingN=} {self.setNvals=}') if dbg else None
    elif txt == '\r':
        self.settingN = 0   ;   old = self.n
        self.setNvals.append(int(self.setNtxt))
        if len(self.setNvals) == 4:
            self.n[:2] = self.setNvals[:2]   ;   self.n[3:] = self.setNvals[2:]
        self.log(f'Setting {old=} {self.n=}')
        self.log(f'END {how} {txt=} {self.settingN=} {self.setNvals=}')
########################################################################################################################################################################################################
def rotateSprite(self, how, spr, cw=1):
    old = spr.rotation
    spr.rotation =  (spr.rotation + cw * 10) % 360
    self.log(f'{how} {cw=} {old=} {spr.rotation=}', f=2)
########################################################################################################################################################################################################
def setCHVMode(self, how, c=None, h=None, v=None):
    self.dumpCursorArrows(f'BGN {how} {c=} {h=} {v=}')
    if c is not None: self.csrMode = c
    if h is not None: self.hArrow  = h
    if v is not None: self.vArrow  = v
    self.dumpCursorArrows(f'END {how} {c=} {h=} {v=}')
########################################################################################################################################################################################################
def flipCrsrMode(self, how, a=1):
    c = self.csrMode  ;  h = self.hArrow  ;  v = self.vArrow
    self.dumpCursorArrows(f'BGN {how} {a=} {c=} {h=} {v=}')
    c = (c + a) % len(CSR_MODES)
    self.dumpCursorArrows(f'END {how} {a=} {c=} {h=} {v=}')
########################################################################################################################################################################################################
def jump(self, how, txt='0', a=0):
    cc = self.cursorCol()                 ;    self.jumpAbs = a
    self.log(    f'{how} {txt=} {a=} {cc=} jt={self.jumpAbs} {self.fmti()}')
    if not self.jumping:                       self.jumping = 1
    elif txt.isdecimal():                      self.jumpStr += txt
    elif txt == '-' and not self.jumpStr:      self.jumpStr += txt
    elif txt == W:
        self.log(f'{how} {txt=} {a=} {cc=} jt={self.jumpAbs} {self.jumpStr=} {self.fmti()}')
        jcc  = self.n[T] * int(self.jumpStr)
        self.jumping = 0   ;   self.jumpStr = Z
        self.move(how, jcc - 1 - a * cc)
        self.log(f'{how} {txt=} {a=} {cc=} jt={self.jumpAbs} {jcc=} moved={jcc - 1 - a * cc} {self.fmti()}')
########################################################################################################################################################################################################
def shiftTabs(self, how, nf=0):
    self.dumpSmap(f'BGN {how} {self.shiftingTabs=} {nf=}')
    if not self.shiftingTabs:
        self.shiftingTabs = 1
        for k, v in self.smap.items():
            self.setLLStyle(k, NORMAL_STYLE) if self.LL else None
        self.setCaption('Enter nf: number of frets to shift +/- int')
    elif nf == '-': self.shiftSign = -1
    elif self.sobj.isFret(nf):
        self.shiftingTabs = 0     ;   nt = self.n[T]
        for cn, v in self.smap.items():
            cc = self.cn2cc(cn)   ;   p, l, c, r = self.cc2plct(cc, dbg=0)
            self.log(f'{cc=} {cn=} {v=} text={v}')
            for t in range(nt):
                text = v[t]    ;    kt = cc + t    ;    fn = 0   ;   ntones = Notes.NTONES * 2
                if self.sobj.isFret(text):
                    fn = self.afn(str((self.sobj.tab2fn(text) + self.shiftSign * self.sobj.tab2fn(nf)) % ntones))  ;  self.log(f'{cc=} {cn=} {t=} {text=} {nf=} {fn=} {self.shiftSign=}')
                if fn and self.sobj.isFret(fn):  self.setDTNIK(fn, kt, p, l, c, t, kk=1 if t==nt-1 else 0)
        self.shiftSign = 1
        self.rsyncData = 1
        self.unselectAll('shiftTabs()')
    self.dumpSmap(f'END {how} {self.shiftingTabs=} {nf=} {self.shiftSign=}')
########################################################################################################################################################################################################
def swapTab(self, how, txt=Z, data=None, dbg=0, dbg2=0):  # e.g. c => 12 not same # chars asserts
    src, trg = self.swapSrc, self.swapTrg
    data = data or self.data
    if not self.swapping: self.swapping = 1
    elif txt.isalnum() or txt in self.tblanks:
        if   self.swapping == 1:   src += txt;   self.log(f'    {how} {txt=} {self.swapping=} {src=} {trg=}') # optimize str concat?
        elif self.swapping == 2:   trg += txt;   self.log(f'    {how} {txt=} {self.swapping=} {src=} {trg=}') # optimize str concat?
        self.swapSrc, self.swapTrg = src, trg
    elif txt == '\r':
        self.log(f'    {how} {self.swapping=} {src=} {trg=}')
        if   self.swapping == 1 and not trg: self.swapping = 2;   self.log(f'{how} waiting {src=} {trg=}') if dbg else None   ;   return
        if   self.swapping == 2 and trg:     self.swapping = 0;   self.log(f'{how} BGN     {src=} {trg=}') if dbg else None
        np, nl, ns, nc, nt = self.n    ;     nc += self.zzl()
        cc0 = self.cursorCol()         ;     p0, l0, c0, t0 = self.cc2plct(cc0)   ;   self.log(f'BFR {cc0=} {p0=} {l0=} {c0=} {t0=}')
        blanks = self.tblanks          ;     blank = 1 if src in blanks and trg in blanks else 0
        if blank:
            for t in self.tabls:   t.text = trg if t.text==src else t.text
            for n in self.notes:   n.text = trg if n.text==src else n.text
            for i in self.ikeys:   i.text = trg if i.text==src else i.text
            for k in self.kords:   k.text = trg if k.text==src else k.text
        for p in range(np):
            for l in range(nl):
                for c in range(nc):
                    text = data[p][l][c]
                    for t in range(nt):
                        if text[t] == src:
                            if dbg2: self.log(f'Before data{self.fplc(p, l, c)}={text}')
                            if blank and trg != self.tblank:
                                text[t] = trg
                            cc = self.plct2cc(p, l, c, t)   ;   self.setDTNIK(trg, cc, p, l, c, t, kk=1)
                            if dbg2: self.log(f'After  data{self.fplc(p, l, c)}={text}')
        self.swapSrc, self.swapTrg = Z, Z
        self.log(f'{how} END     {src=} {trg=}') if dbg else None
#                if dbg2: self.dumpTniks('SWAP')
#                self.moveTo(how, p0, l0, c0, t0)  ;  cc = self.cursorCol()  ;  self.log(f'AFT {cc0=} {p0=} {l0=} {c0=} {t0=} {cc=}')
        if self.SNAPS: self.regSnap(f'{how}', 'SWAP')
        self.rsyncData = 1
########################################################################################################################################################################################################
def flipLLs(self, how, dbg=1):
    self.flipLL()
    msg2 = f'{how} {self.LL=}'
    self.dumpGeom('BGN', f'     {msg2}')
    if dbg: self.log(f'    llText={fmtl(self.llText[1-self.zzl():])}')
    if self.LL and not self.rowLs: msg = 'ADD'    ;   self.addLLs( how)
    else:                          msg = 'HIDE'   ;   self.hideLLs(how)
    self.on_resize(self.width, self.height)
    self.dumpGeom('END', f'{msg} {msg2}')
########################################################################################################################################################################################################
def flipTTs(self, how, tt):
    msg2 = f'{how} {tt=}'
    self.dumpGeom('BGN', f'     {msg2}')
    if   tt not in self.SS and not self.B[tt]: msg = 'ADD'    ;   self.addTTs( how, tt)
    elif tt     in self.SS:                    msg = 'HIDE'   ;   self.hideTTs(how, tt)
    else:                                      msg = 'SKIP'   ;   self.dumpGeom(W*3, f'{msg} {msg2}')   ;   self.flipTT(tt)
    self.on_resize(self.width, self.height)
    self.dumpGeom('END', f'{msg} {msg2}')
########################################################################################################################################################################################################
def move2LastTab(self, how, page=0, dbg=1):
    np, nl, ns, nc, nt = self.n    ;   p, l, s, c, t = self.j()  ;  i = p
    n = p * nl + l     ;   tp = nc * nt
    if page: tp *= nl  ;  n //= nl
    if dbg:    self.log(f'BGN {how} {page=} {self.fplct()} {i=:4} {n=} {tp=:3} {tp*n=:4} for({tp*(n+1)-1:4}, {tp*n-1:4}, -1)', pos=1)
    for i in range(tp*(n+1)-1, tp*n-1, -1):
        if not self.sobj.isFret(self.tabls[i].text): continue
        p, l, c, t = self.cc2plct(i, dbg=1)  ;  break
    self.moveTo(how, p, l, c, t, dbg=dbg)
    if dbg:    self.log(f'END {how} {page=} {self.fplct()} {i=:4} {n=} {tp=:3} {tp*n=:4} for({tp*(n+1)-1:4}, {tp*n-1:4}, -1)', pos=1)
########################################################################################################################################################################################################
def move2FirstTab(self, how, page=0, dbg=1):
    np, nl, ns, nc, nt = self.n    ;   p, l, s, c, t = self.j()  ;  i = p
    n = p * nl + l     ;   tp = nc * nt
    if page: tp *= nl  ;  n //= nl
    if dbg:    self.log(f'BGN {how} {page=} {self.fplct()} {i=:4} {n=} {tp=:3} {tp*n=:4} for({tp*n:4}, {tp*(n+1):4}, 1)', pos=1)
    for i in range(tp*n, tp*(n+1), 1):
        if not self.sobj.isFret(self.tabls[i].text): continue
        p, l, c, t = self.cc2plct(i, dbg=1)  ;  break
    self.moveTo(how, p, l, c, t, dbg=dbg)
    if dbg:    self.log(f'END {how} {page=} {self.fplct()} {i=:4} {n=} {tp=:3} {tp*n=:4} for({tp*n:4}, {tp*(n+1):4}, 1)', pos=1)
########################################################################################################################################################################################################
def flipSelectAll(self, how):
    self.dumpSmap(f'BGN {how} {self.allTabSel=}')
    if   self.allTabSel:       self.unselectAll(how)   ;   self.allTabSel = 0
    else:                      self.selectAll(how)     ;   self.allTabSel = 1
    self.dumpSmap(f'END {how} {self.allTabSel=}')
########################################################################################################################################################################################################
def insertSpace(self, how, txt='0', dbg=1): # optimize str concat?
    cc = self.cursorCol()   ;   c0 = self.cc2cn(cc)
    if not self.inserting: self.inserting = 1   ;    self.setCaption('Enter nc: number of cols to indent int')
    elif txt.isdecimal():  self.insertStr += txt
    elif txt in (W, '/r'):
        self.inserting = 0
        width = int(self.insertStr)
        tcs   = sorted(self.cobj.mlimap)
        tcs.append(self.n[C] * self.n[L] - 1)
        tcs   = [ t + 1 for t in tcs ]
        if dbg: self.log(f'BGN {how} Searching for space to insert {width} cols starting at colm {c0}')
        self.log(f'{fmtl(tcs, ll=1)} insertSpace', p=0)
        found, c1, c2 = 0, 0, None   ;   self.insertStr = Z
        for c2 in tcs:
            if dbg: self.log(f'w c0 c1 c2 = {width} {c0} {c1} {c2}')
            if c2 > c0 + width and c2 > c1 + width: found = 1  ;  break
            c1 = c2
        if not found: self.log(f'{how} starting at colm {c0} No room to insert {width} cols before end of page at colm {tcs[-1]+1}')  ;   return
        self.log(f'{how} starting at colm {c0} Found a gap {width} cols wide between cols {c1} and {c2}')
        self.log(f'select cols {c0} ... {c1}, cut cols, move ({width} - {c1} + {c0})={width-c1+c0} cols, paste cols')
        [ self.selectTabs(how, m=self.tpc) for _ in range(c1 - c0) ]
        self.cutTabs(how)
        self.move(how, (width - c1 + c0) * self.tpc)
        self.pasteTabs(how)
        self.unselectAll(how)
########################################################################################################################################################################################################
def swapCols(self, how):
    nk = len(self.smap)   ;   nk2 = nk // 2
    self.dumpSmap(f'BGN {nk=} {nk2=}')
    for i in range(nk2):
        k1 = list(self.smap.keys())[i]
        k2 = list(self.smap.keys())[nk - 1 - i]
        text1 = self.smap[k1]
        text2 = self.smap[k2]
        self.smap[k1] = text2
        self.smap[k2] = text1
    self.dumpSmap(f'    {nk=} {nk2=}')
    self.pasteTabs(how)
    self.dumpSmap(f'END {nk=} {nk2=}')
########################################################################################################################################################################################################
def addPage(self, how, ins=None, dbg=1):
    np, nl, ns, nc, nt = self.n   ;   how = f'{how} {ins=}'
    self.dumpBlanks() # self.j()[P]
#        if ins is not None: self.flipPage(how)
    if ins is not None: self.flipVisible(how=how)
    self.n[P] += 1   ;   kl = self.k[P]
    data      = [ [ self.tblankRow for _ in range(nt) ] for _ in range(nl) ]
    self.data = self.transposeData(dmp=dbg)
    self.data.append(data) if ins is None else self.data.insert(ins, data)
    self.data = self.transposeData(dmp=dbg)
    if ins is None: self.dumpTniksPfx(how, r=0)   ;   pi = len(self.pages)
    else:           self.dumpTniksPfx(how, r=1)   ;   pi = self.J1[P]
    self.J1[L], self.J1[S], self.J1[C], self.J1[T] = 0, 0, 0, 0
    n, ii, x, y, w, h =    self.geom(M, n=1, i=1, dbg=1)   ;   kk = self.cci(P, 0, kl) if self.CHECKERED else 0
    self.newC += 1  ;  why2 = f'New{self.newC}'  ;  why = why2  ;  k = kl[kk]
    page = self.createTnik(self.pages,   pi, P, x, y, w, h, k, why=why, v=0, dbg=1)
    for line in            self.g_createTniks(self.lines,  L, page, why=why):
        for sect in        self.g_createTniks(self.sects,  S, line, why=why):
            for colm in    self.g_createTniks(self.colms,  C, sect, why=why):
                for _ in   self.g_createTniks(self.tabls,  T, colm, why=why): pass
    self.dumpTniksSfx(how)
    if self.SNAPS and dbg: self.regSnap(how, why2)
########################################################################################################################################################################################################
def eraseTabs(self, how): # , reset=0):
    np, nl, ns, nc, nt = self.n   ;   nz = self.zzl()  ;  nc += nz
    self.log(f'BGN {how} {np=} {nl=} {ns=} {nc=} {nt=}')
    self.nic.clear()
    self.dumpBlanks()
    for t in self.tabls:
        t.text = self.tblank
    for n in self.notes:
        n.text = self.tblank
    for i in self.ikeys:
        i.text = self.tblank
    for k in self.kords:
        k.text = self.tblank
    for p in range(np):
        for l in range(nl):
            for c in range(nz, nc):
                self.data[p][l][c-nz] = self.tblankCol
    self.log(f'END {how} {np=} {nl=} {ns=} {nc=} {nt=}')
    self.rsyncData = 1
########################################################################################################################################################################################################
def reset(self, how):
    self.dumpGeom('BGN', f'{how} before cleanup()')
    self.cleanup()
    self.dumpGeom('   ', f'{how} after cleanup() / before reinit()')
    self._reinit()
    self.dumpGeom('END', f'{how} after reinit()')
########################################################################################################################################################################################################
def copyTabs(self, how, dbg=1): # optimize str concat?
    self.dumpSmap(f'BGN {how}')   ;   nt = self.n[T]   ;   style = NORMAL_STYLE   ;   text = []
    for k in list(self.smap.keys()):
        k *= nt
        if self.LL:  self.setLLStyle(k, style)
        text.append(self.setTNIKStyle(k, nt, style))
        if dbg: text.append(W)
    if dbg:         self.log(f'{Z.join(text)=}')
    self.dumpSmap(f'END {how}')
    if self.SNAPS:  self.regSnap(f'{how}', 'COPY')
########################################################################################################################################################################################################
def deleteTabs(self, how, keep=0, dbg=1):
    self.dumpSmap(f'BGN {how} {keep=}')   ;   style = NORMAL_STYLE   ;   nt = self.n[T]
    for k, text in self.smap.items():
        cn = k   ;   k *= nt
        if dbg:     self.log(f'{k=} {cn=} {text=}')
        if self.LL: self.setLLStyle(k, style)
        self.setTNIKStyle(k, nt, style, blank=1)
    if not keep:    self.unselectAll(f'deleteTabs({keep=})')
    self.dumpSmap(f'END {how} {keep=}')
    if self.SNAPS:  self.regSnap(f'{how}', 'DELT')
    self.rsyncData = 1
########################################################################################################################################################################################################
def pasteTabs(self, how, kk=0, dbg=1):
    cc = self.cursorCol()       ;   nt = self.n[T]
    cn = self.normalizeCC(cc)   ;   kt = 0
    p, l, s, c, t = self.j()
    self.dumpSmap(f'BGN {how} {kk=} {cc=} {cn=}={self.cc2cn(cc)} plct={self.fplct(p, l, c, t)}')
    for i, (k, text) in enumerate(self.smap.items()):
        if not i:   dk = 0
        elif kk:    dk = i * nt
        else:       dk = (list(self.smap.keys())[i] - list(self.smap.keys())[0]) * nt
        if dbg:     self.log(f'{i=} {k=} {text=} {kk=} {dk=}')
        for n in range(nt):
            kt         = (cn + dk + n) % self.tpp # todo
            p, l, c, t = self.cc2plct(kt)
            self.setDTNIK(text[n], kt, p, l, c, n, kk=1 if n==nt-1 else 0)
        if dbg:     self.log(f'{i=} {k=} {text=} {kk=} {dk=} {kt=}')
    self.log(f'clearing {len(self.smap)=}')   ;   self.smap.clear()
    self.dumpSmap(f'END {how} {kk=} {cc=} {cn=}={self.cc2cn(cc)} plct={self.fplct(p, l, c, t)}')
    if self.SNAPS:  self.regSnap(f'{how}', 'PAST')
    self.rsyncData = 1
########################################################################################################################################################################################################
def cutTabs(self, how): self.log('BGN Cut = Copy + Delete')  ;  self.copyTabs(how)  ;  self.log('Cut = Copy + Delete')  ;  self.deleteTabs(how, keep=1)  ;  self.log('END Cut = Copy + Delete')
########################################################################################################################################################################################################
def cutTabs(self, how):
    self.log('BGN Cut = Copy + Delete')
    self.copyTabs(how)
    self.log('Cut = Copy + Delete')
    self.deleteTabs(how, keep=1)
    self.log('END Cut = Copy + Delete')
########################################################################################################################################################################################################
def moveUp(self, how, dbg=1):
    p, l, s, c, t = self.j()  ;  n = self.n[T] - 1  ;  m = self.n[L] - 1
    if dbg: self.log(f'BGN {how}', pos=1)
    if t>0: self.moveTo(how, p, l,                 c, 0) # go up   to top    of      line
    else:   self.moveTo(how, p, l-1 if l>0 else m, c, n) # go up   to bottom of prev line, wrap down to bottom of last line
    if dbg: self.log(f'END {how}', pos=1)
########################################################################################################################################################################################################
def moveDown(self, how, dbg=1):
    p, l, s, c, t = self.j()  ;  n = self.n[T] - 1  ;  m = self.n[L] - 1
    if dbg: self.log(f'BGN {how}', pos=1)
    if t<n: self.moveTo(how, p, l,                 c, n) # go down to bottom of      line
    else:   self.moveTo(how, p, l+1 if l<m else 0, c, 0) # go down to top    of next line, wrap up to top of first line
    if dbg: self.log(f'END {how}', pos=1)
########################################################################################################################################################################################################
def moveLeft(self, how, dbg=1):
    p, l, s, c, t = self.j()  ;  n = self.n[C] - 1  ;  m = self.n[L] - 1
    if dbg: self.log(f'BGN {how}', pos=1)
    if c>0: self.moveTo(how, p, l,                 0, t) # go left  to bgn of      line
    else:   self.moveTo(how, p, l-1 if l>0 else m, n, t) # go left  to end of prev line, wrap right to bottom of last line
    if dbg: self.log(f'END {how}', pos=1)                # go right & up to end of prev line, wrap down to bottom of last line
########################################################################################################################################################################################################
def moveRight(self, how, dbg=1):
    p, l, s, c, t = self.j()  ;  n = self.n[C] - 1  ;  m = self.n[L] - 1
    if dbg: self.log(f'BGN {how}', pos=1)
    if c<n: self.moveTo(how, p, l,                 n, t) # go right to end of      line
    else:   self.moveTo(how, p, l+1 if l<m else 0, 0, t) # go right to bgn of next line, wrap left to top of first line
    if dbg: self.log(f'END {how}', pos=1)                # go left & down to bgn of next line, wrap left to top of first line
########################################################################################################################################################################################################
def moveTo(self, how, p, l, c, t, ss=0, dbg=1):
    if dbg:    self.log(f'BGN {how}', pos=1)
    self._moveTo(p, l, c, t)
    self.moveCursor(ss, how)
    if dbg:    self.log(f'END {how}', pos=1)
########################################################################################################################################################################################################
def _moveTo(self, p, l, c, t, n=0, dbg=1): # todo
    if dbg: self.log(f'BGN plct={self.fplct(p, l, c, t)}', pos=1) # {n=}
    np, nl, ns, nc, nt = self.n
    t2        =       n  + t
    c2        = t2 // nt + c
    l2        = c2 // nc + l
    p2        = l2 // nl + p
    self.i[T] = t2  % nt + 1
    self.i[C] = c2  % nc + 1
    self.i[L] = l2  % nl + 1
    self.i[P] = p2  % np + 1
    if dbg: self.log(f'END {n=} {self.fmti()} plct={self.fplct(p, l, c, t)} plct2={self.fplct(p2, l2, c2, t2)}', pos=1)
########################################################################################################################################################################################################
def move(self, how, n, ss=0, dbg=1):
    if dbg:    self.log(f'BGN {how} {n=}', pos=1)
    p, l, c, t = self.j2()
    self._moveTo(p, l, c, t, n=n)
    if self.CURSOR and self.cursor: self.moveCursor(ss, how)
    if dbg:    self.log(f'END {how} {n=}', pos=1)
########################################################################################################################################################################################################
def moveCursor(self, ss=0, why=Z, dbg=1):
    if dbg:           self.log(f'BGN {ss=} {self.cc=}', pos=1)
    if self.LL:       self.setLLStyle(self.cc, SELECT_STYLE if ss else NORMAL_STYLE)
    self.resizeCursor(why, dbg=dbg)
    if self.LL:       self.setLLStyle(self.cc, CURRENT_STYLE)
    if dbg:           self.log(f'END {ss=} {self.cc=}', pos=1)
########################################################################################################################################################################################################
def resizeCursor(self, why, dbg=1):
    x, y, w, h, c = self.cc2xywh()
    self.resizeTnik(self.hcurs, 0, H, x, y, w, h, why=why, dbg=dbg)
########################################################################################################################################################################################################
def resizeTnik(self, tlist, i, j, x, y, w, h, why=Z, dbg=0): # self.setTNIKStyle2(tnik, self.k[j], self.BGC)
#        assert 0 <= i < len(tlist),  f'{i=} {len(tlist)=}'
    tnik    = tlist[i]
    self.log(f'{why} {H=} {j=} {i=} {self.J2[H]=}')       if dbg and j == H else None
    if   ist(tnik, SPR):
        mx, my = w/tnik.image.width, h/tnik.image.height
        tnik.update(x=x, y=y, scale_x=mx, scale_y=my)
    elif ist(tnik, LBL):
        tnik.font_size = self.calcFontSize(j)
        tnik.x, tnik.y, tnik.width, tnik.height = x, y, w, h
        self.checkTnik(tnik, i, j)
    self.setJ(j, i, tnik.visible) if j != H or (j == H and self.J2[H] == 0) else None # todo fixme - do we want or need to set v info of the tnik as well?
    self.dumpTnik(tnik, j, why) if dbg else None
    if j == P and tnik.visible:   self.setCaption(f'{utl.ROOT_DIR}/{DATA}/{self.FILE_NAME}.{DAT} page {self.i[P]}')
    return tnik
########################################################################################################################################################################################################
def prevPage(self, how, dbg=1):
    p, l, c, t = self.j2()   ;   n = self.n[P] - 1
    if dbg: self.log(f'BGN {how} {self.fmti()}', pos=1)
    self.moveTo(how, p-1 if p>0 else n, l, c, t)
#        self.flipPage(how, -1, dbg=1)
    if dbg: self.log(f'END {how} {self.fmti()}', pos=1)
########################################################################################################################################################################################################
def nextPage(self, how, dbg=1):
    p, l, c, t = self.j2()   ;   n = self.n[P] - 1
    if dbg: self.log(f'BGN {how} {self.fmti()}', pos=1)
    self.moveTo(how, p+1 if p<n else 0, l, c, t)
#        self.flipPage(how, 1, dbg=1)
    if dbg: self.log(f'END {how} {self.fmti()}', pos=1)
########################################################################################################################################################################################################
def autoMove(self, how, dbg=1):
    self.log(f'BGN {self.hArrow=} {self.vArrow=} {self.csrMode=} {how}', pos=1)
    ha = 1 if self.hArrow == RARROW else -1
    va = 1 if self.vArrow == DARROW else -1
    n, i  = self.n[T], self.i[T]
    mmDist  = ha * n
    cmDist  = va
    amDist  = mmDist + cmDist
    if dbg:   self.dumpCursorArrows(f'{self.fmtPos()}     {how} M={mmDist} C={cmDist} A={amDist}')
    if        self.csrMode == MELODY:                               cmd = cmds.MoveCmd(self, how,   mmDist)  ;  cmd.do()
    elif      self.csrMode == CHORD:
        if    i==1 and self.vArrow==UARROW and self.hArrow==RARROW: cmd = cmds.MoveCmd(self, how,   n*2-1)   ;  cmd.do()
        elif  i==6 and self.vArrow==DARROW and self.hArrow==LARROW: cmd = cmds.MoveCmd(self, how, -(n*2-1))  ;  cmd.do()
        else:                                                       cmd = cmds.MoveCmd(self, how,   cmDist)  ;  cmd.do()
    elif      self.csrMode == ARPG:                                 cmd = cmds.MoveCmd(self, how,   amDist)  ;  cmd.do()
    self.log(f'END {self.hArrow=} {self.vArrow=} {self.csrMode=} {how}', pos=1)
########################################################################################################################################################################################################
def selectTabs(self, how, m=0, cn=None, dbg=1, dbg2=1):
    cc         = self.cursorCol()  ;  old = cn
    p, l, s, c, t = self.cc2plsct(cc)
    if cn is None:      cn = self.cc2cn(cc) # self.plc2cn_(p, l, c)
    nt = self.n[T]  ;   k  = cn * nt   ;   style = SELECT_STYLE
    self.log(f'{m=} {old=} {cc=} {cn=} {nt} {k=} {self.fplsct(p, l, s, c, t)}')
    if cn in self.smap: self.log(f'RETURN: {cn=} already in smap={fmtm(self.smap)}') if dbg2 else None   ;   return
    if dbg:             self.dumpSmap(f'BGN {how} {m=} {cn=} {cc=} {k=}')
    text              = self.setTNIKStyle(k, nt, style)
    self.smap[cn]     = text
    if m:               cmd = cmds.MoveCmd(self, how, m, ss=1)     ;  cmd.do()
    if dbg:             self.dumpSmap(f'END {how} {m=} {cn=} {cc=} {k=}')
########################################################################################################################################################################################################
def unselectTabs(self, how, m, cn=None, dbg=0):
    if cn is None:      cc = self.cc   ;      cn = self.cc2cn(cc)
    else:               cc = self.cn2cc(cn)
    nt = self.n[T]  ;   k = cn * nt    ;   style = NORMAL_STYLE
    if self.LL:         self.setLLStyle(cc, style)
    if dbg:             self.dumpSmap(f'BGN {how} {m=} {cn=} {cc=} {k=}')
    self.setTNIKStyle(k, nt, style)
    if cn in self.smap: self.smap.pop(cn)
    elif dbg:           self.log(f'{cn=} not found in smap={fmtm(self.smap)}')
    if m:               cmd = cmds.MoveCmd(self, how, m)     ;  cmd.do()
    if dbg:             self.dumpSmap(f'END {how} {m=} {cn=} {cc=} {k=}')
########################################################################################################################################################################################################
def saveDataFile(self, why, path, dbg=1):
    if dbg:   self.log(f'BGN {why} {path}')
    with open(path, 'w', encoding='utf-8') as DATA_FILE:
        self.log(f'{DATA_FILE.name:40}', p=0)
        commentStr = '#' * self.n[C]   ;   commentRow = f'{commentStr}{X}'
        DATA_FILE.write(commentRow) if self.DEC_DATA else None
        data = self.transposeData(dmp=dbg) # if self.isVert() else self.data
        self.log(f'{self.fmtn()} {self.fmtdl(data)}')
        for p, page in enumerate(data):
            if dbg: self.log(f'writing {p+1}{utl.ordSfx(p + 1)}   Page', p=0)
            for l, line in enumerate(page):
                if dbg: self.log(f'writing {l+1}{utl.ordSfx(l+1)}   Line', p=0)  # if dbg  else  self.log(p=0)  if  l  else  None
                for r, row in enumerate(line):
                    text = []
                    for c, col in enumerate(row):
                        text.append(col)
                    text = Z.join(text)
                    if dbg: self.log(f'writing {r+1}{utl.ordSfx(r+1)} String {text}', p=0)  # if dbg  else  self.log(text, p=0)
                    DATA_FILE.write(f'{text}{X}')
                DATA_FILE.write(commentRow) if self.DEC_DATA else DATA_FILE.write(X)  #   if l < nl:
            DATA_FILE.write(commentRow) if self.DEC_DATA else DATA_FILE.write(X)
    size = path.stat().st_size   ;   self.log(f'{self.fmtn()} {self.fmtdl()} {size=}')
    if dbg:   self.log(f'END {why} {path}')
    return size
########################################################################################################################################################################################################
