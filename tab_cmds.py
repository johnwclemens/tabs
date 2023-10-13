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
    elif kbk == 'F' and isCtlShf(kd, m):     tobj.flipFullScrn( '@^F') # FULL_SCREEN
    elif kbk == 'F' and isCtl(   kd, m):     tobj.flipFlatShrp( '@ F') # FLAT_SHARP
    elif kbk == 'J' and isCtlShf(kd, m):     tobj.jump(         '@^J', a=1)
    elif kbk == 'J' and isCtl(   kd, m):     tobj.jump(         '@ J', a=0)
    elif kbk == 'L' and isCtlShf(kd, m):     tobj.flipLLs(      '@^L')
    elif kbk == 'L' and isCtl(   kd, m):     tobj.flipLLs(      '@ L')
    elif kbk == 'O' and isCtlShf(kd, m):     tobj.flipCrsrMode( '@^O', -1)
    elif kbk == 'O' and isCtl(   kd, m):     tobj.flipCrsrMode( '@ O', 1)
    elif kbk == 'R' and isCtlShf(kd, m):     tobj.flipKordNames('@^R', hit=1)
    elif kbk == 'R' and isCtl(   kd, m):     tobj.flipKordNames('@ R', hit=0)
    elif kbk == 'S' and isCtlShf(kd, m):     tobj.shiftTabs(    '@^S')
#   elif kbk == 'S' and isCtl(   kd, m):     tobj.saveDataFile( '@ S', self.dataPath1)
    elif kbk == 'S' and isCtl(   kd, m):     tobj.swapTab(      '@ S', txt=Z)

    elif kbk == 'TAB' and isCtl(kd, m):      tobj.setCHVMode(   '@ TAB',       MELODY, LARROW)
    elif kbk == 'TAB':                       tobj.setCHVMode(   '  TAB',       MELODY, RARROW)
#   elif kbk == 'SLASH'     and isCtl(mods):  tobj.setCHVMode(  '@ SLASH',     ARPG,   LARROW, DARROW)
#   elif kbk == 'SLASH':                      tobj.setCHVMode(  '  SLASH',     ARPG,   RARROW, UARROW)
#   elif kbk == 'BACKSLASH' and isCtl(mods):  tobj.setCHVMode(  '@ BACKSLASH', ARPG,   LARROW, UARROW)
#   elif kbk == 'BACKSLASH':                  tobj.setCHVMode(  '  BACKSLASH', ARPG,   RARROW, DARROW)

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
