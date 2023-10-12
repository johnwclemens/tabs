import os, pathlib, sys #, glob
import inspect, operator #, math
import collections, itertools
from   collections     import Counter
from   itertools       import accumulate
#from   more_itertools  import consume  # not installed in GitBash's Python
import pyglet
import pyglet.font         as pygfont
import pyglet.image        as pygimg
import pyglet.sprite       as pygsprt
import pyglet.text         as pygtxt
import pyglet.window.event as pygwine
from   pyglet.text     import document, layout
from   tpkg            import utl    as utl
from   tpkg            import kysgs  as kysgs
from   tpkg            import misc   as misc
from   tpkg            import evnts  as evnts
from   tpkg.notes      import Notes  as Notes
from   tpkg.strngs     import Strngs as Strngs
from   tpkg.chords     import Chords as Chords

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
    elif kbk == 'R' and isCtlShf(kd, m):     tobj.flipKordNames('@^R', hit=1)
    elif kbk == 'R' and isCtl(   kd, m):     tobj.flipKordNames('@ R', hit=0)

    elif kbk == 'A' and isAltShf(kd, m):     tobj.flipBGC(      '&^A')
    elif kbk == 'A' and isAlt(   kd, m):     tobj.flipBGC(      '& A')
    elif kbk == 'D' and isAltShf(kd, m):     tobj.flipDrwBGC(   '&^D', -1)
    elif kbk == 'D' and isAlt(   kd, m):     tobj.flipDrwBGC(   '& D',  1)

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

    elif kbk == 'P' and isAltShf(kd, m):     tobj.flipPage(     '&^P', -1)
    elif kbk == 'P' and isAlt(   kd, m):     tobj.flipPage(     '& P',  1)
    elif kbk == 'V' and isAltShf(kd, m):     tobj.flipVisible(  '&^V', dbg=1)
    elif kbk == 'V' and isAlt(kd, m):        tobj.flipVisible(  '& V', dbg=1)
    
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
    ########################################################################################################################################################################################################
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
