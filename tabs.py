import fractions
import os, sys, glob, inspect, pathlib, itertools # os
import pyglet
import pyglet.window.event as wine # pygwine
import pyglet.window.key   as wink # pygwink
import pyglet.text.caret   as pygcrt
from  pyglet.text.layout import IncrementalTextLayout as pyglbox
#import pyglet.text.layout as pyglbox
#sys.path.insert(0, os.path.abspath("./lib"))
#print(f'{len(sys.path)=}')
#for _ in sys.path:
#    print(f'{_}')
import chord, util

Z                = ' '
PATH             = pathlib.Path.cwd() / sys.argv[0]
BASE_PATH        = PATH.parent
BASE_NAME        = BASE_PATH.stem
SNAP_DIR         = 'snaps'
SNAP_SFX         = '.png'
LOG_FILE         = None
FDL              = ' len(data 0 00 000)'
FDT              = 'type(data 0 00 000)'
P, L, S, T       =  0,  1,  2,  3
N, I, K, V       =  4,  5,  6,  7
R, C, H          =  8,  9, 10
O, A, D          = 11, 12, 13
#                #     0        1        2        3       4       5        6       7         8        9      10       11       12       13      14
JTEXTS           = ['Page',  'Line',  'Strg',  'Tab',  'Note',  'IKey',  'Kord', 'View',  '_LLR',  '_LLC', 'Curs',  '_SNo',  '_SNm',  '_Cpo', '_TNIK']
JFMT             = [   2,       3,       2,       4,      4,       4,       4,      1,       1,       3,      1,       2,       2,       3,       4  ]
TT, NN, II, KK   =  0,  1,  2,  3
LEFT, RIGHT      = -1, 1
UP,   DOWN       = -1, 1
H_ARWS           = {-1:'LEFT', 1:'RIGHT'}
V_ARWS           = {-1:'UP'  , 1:'DOWN' }
C_MODES          = ['MELODY', 'CHORD', 'ARPG']
MELODY, CHORD, ARPG   = 0, 1, 2
IMPLA            = 0
FORWARD          = (wink.MOTION_RIGHT, wink.MOTION_BEGINNING_OF_LINE) # , wink.MOTION_NEXT_WORD,     wink.MOTION_NEXT_PAGE,     wink.DELETE)
BACKWARD         = (wink.MOTION_LEFT,  wink.MOTION_END_OF_LINE)       # , wink.MOTION_PREVIOUS_WORD, wink.MOTION_PREVIOUS_PAGE, wink.BACKSPACE)
UPWARD           = (wink.MOTION_UP,    wink.MOTION_BEGINNING_OF_FILE) # , wink.MOTION_PREVIOUS_WORD, wink.MOTION_PREVIOUS_PAGE)
DOWNWARD         = (wink.MOTION_DOWN,  wink.MOTION_END_OF_FILE)       #  , wink.MOTION_NEXT_WORD,    wink.MOTION_NEXT_PAGE)

def fsize(s, t, w, h, file, xx=1.5, yy=1.):
    fsx = xx * w/t  ;  fsy = yy * h/s
    fs = round(fsx + fsy)
    fs2 = fs * 0.3  # 7/18) # 14/18*1/2
    util.slog(f'{s=} {t=} {w=} {h=} {fsx=:3.2f} {fsy=:3.2f} {fs=:3.2f} {fs2=:3.2f}', file=file)
    return fs2

def fmark(m): return f'{m:<4}' if m is not None else 'None'
def fmtXYWH(x, y, w, h):             return f'({x} {y} {w} {h})'

class Tabs(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        self.log(f'init {args=} {kwargs=}')
        self.data        = []
        self.views       = []
        self.batch       = pyglet.graphics.Batch()
        self.group       = pyglet.graphics.OrderedGroup(0)
        self.n           = [1, 1, 6, 20]
        self.i           = [1, 1, 6, 1]
        self.v           = set() if 0 else {0}
#        self.p, self.l, self.s, self.t = 0, 0, 0, 0
        self.snapWhy, self.snapType, self.snapReg, self.snapId = '?', '_', 0, 0
        self.LOG_ID      = 0
        self.lfSeqPath   = self.getFilePath(seq=1, fdir='logs', fsfx='.log')
        self.mx, self.my = 1, 1
        self.x,  self.y,  self.w,  self.h     = 0, 0, 0, 0
        self.symb,    self.mods,    self.motn = 0, 0, 0
        self.symbTxt, self.modsTxt, self.motnTxt, self.kbkTxt = None, None, None, None
        self.hArrow, self.vArrow,  self.csrMode               = RIGHT, DOWN, MELODY    ;    self.dumpCrsArrows('init()')
        self._initArgs()
        self.sAlias = 'GUITAR_6_STD'
        self.sobj = util.Strings(LOG_FILE, self.sAlias)
        self.cobj = chord.Chord( LOG_FILE, self.sobj)
        util.Note.setType(util.Note.SHARP)  ;  self.log(f'{util.Note.TYPE=}')
        self._initWindowA()
        super().__init__(screen=self.screens[self.fsi], fullscreen=self.FULL_SCREEN, resizable=True, visible=False)
        self._initWindowB()
        self.blanki, self.blanks = 0, ['-', ' ']
        self.blank    = self.blanks[self.blanki]
        self.blankCol = self.blank * self.n[S]
        self.blankRow = self.blank * self.n[T]
        self.dmpBlnks()
        self.initData()
        self.initViews()
        self.text_cursor = self.get_system_mouse_cursor('text')
        self.focus       = None
        self.regSnap('init', 'INIT')
        self.setFocus(self.getTabsView())
    ####################################################################################################################################################################################################
    def _initWindowA(self, dbg=1):
        display      = pyglet.canvas.get_display()
        if dbg:      self.log(f'BGN {self.fmtWxH()}')   ;   self.log(f'{display=}')
        self.screens = display.get_screens()  ;  s = self.screens  ;  ri, rv = len(self.screens), 0
        assert display.get_windows() == [], f'ERROR Unexpected {display.get_windows()}'
        for i in range(len(s)):
            w = s[i].width  ;  h = s[i].height
            if w * h > rv:     ri, rv = i, w * h
            self.log(f'screens[{i}] {self.fmtXdY(s[i].x, s[i].y)} {self.fmtWxH(s[i].width, s[i].height)} {ri=} {rv=:,}', pfx=0)
            self.log(f'screens[{i}] {s[i].get_mode()}', pfx=0)
        self.fsi, self.fss = ri, rv   ;   self.log(f'{self.fsi=} {self.fss=:,} {self.fmtWxH(s[ri].width, s[ri].height)}')
        if dbg:      self.log(f'END {self.fmtWxH()}')   ;   self.log(f'{display=}')

    def _initWindowB(self, dbg=1):
        if dbg: self.log(f'BGN {self.fmtWxH()}')
        w = self.display.get_windows()
        for j in range(len(w)): self.log(f'windows[{j}] {self.fmtXdY(w[j].x, w[j].y)} {self.fmtWxH(w[j].width, w[j].height)}')
        self.set_visible()
        self.log(f'get_size={self.fmtWxH(self.get_size())}')
        self.kbks = wink.KeyStateHandler()
        self.push_handlers(self.kbks)
        if self.EVENT_LOG: # and self.VERBOSE:
            self.eventLogger = wine.WindowEventLogger()
            self.push_handlers(self.eventLogger)
        if dbg: self.log(f'END {self.fmtWxH()}')
    ####################################################################################################################################################################################################
    def _initArgs(self):
        self.dfn         = 'test.0.dat'
        self.EVENT_LOG = 0  ;  self.FULL_SCREEN = 0  ;  self.GEN_DATA = 0  ;  self.ORDER_GROUP = 1  ;  self.SNAPS = 0  ;  self.VERBOSE = 0
        ARGS             = util.parseCmdLine(file=LOG_FILE)
        self.log(f'argMap={util.fmtm(ARGS)}')
        if 'a' in ARGS and len(ARGS['a']) == 0: global IMPLA ; IMPLA =  1
        if 'e' in ARGS and len(ARGS['e']) == 0: self.EVENT_LOG       =  1
        if 'f' in ARGS and len(ARGS['f']) >  0: self.dfn             = ARGS['f'][0]
        if 'F' in ARGS and len(ARGS['F']) == 0: self.FULL_SCREEN     =  1
        if 'G' in ARGS and len(ARGS['G']) == 0: self.GEN_DATA        =  1
        if 'g' in ARGS and len(ARGS['g']) == 0: self.ORDER_GROUP     =  0
        if 'm' in ARGS and len(ARGS['m']) == 0: self.csrMode         = ARGS['m'][0]
        if 'n' in ARGS and len(ARGS['n']) >  0: self.n               = [int(ARGS['n'][i]) for i in range(len(ARGS['n']))]
        if 's' in ARGS and len(ARGS['s']) == 0: self.SNAPS           =  1
        if 'v' in ARGS and len(ARGS['v']) >= 0: self.v               = {int(ARGS['v'][i]) for i in range(len(ARGS['v']))}
        if 'V' in ARGS and len(ARGS['V']) == 0: self.VERBOSE         =  1
        self.dumpArgs()
    ####################################################################################################################################################################################################
    def dumpArgs(self):
        self.log(f'[a]        {IMPLA=}')
        self.log(f'[e]   {self.EVENT_LOG=}')
        self.log(f'[f]         {self.dfn=}')
        self.log(f'[F] {self.FULL_SCREEN=}')
        self.log(f'[G]    {self.GEN_DATA=}')
        self.log(f'[g] {self.ORDER_GROUP=}')
        self.log(f'[n]            {self.fmtn()}')
        self.log(f'[s]       {self.SNAPS=}')
        self.log(f'[v]            {self.fmtv()}')
        self.log(f'[V]     {self.VERBOSE=}')

    def fmtDxD( self, data=None,      d='x'):  l = list(map(str, self.dl(data)))       ;  return f'({d.join(l)})'
    def fmtXdY( self, x=None, y=None, d=','):  x = x if x is not None else self.x      ;  y = y if y is not None else self.y       ;  return f'({x:4}{d}{y:4})'
    def fmtWxH( self, w=None, h=None, d='x'):  w = w if w is not None else self.width  ;  h = h if h is not None else self.height  ;  return f'({w}{d}{h})'
#    def fmtBlnk(self):                         return f'{self.blankCol=} {self.blankRow=}'
#    def fmtblnk(self):                         return f'{len(self.blankCol)=} {len(self.blankRow)=}'
    def dmpBlnks(self):                        self.log(f'{self.dumpBlnkCol()} {self.dumpBlnkRow()}')
    def dumpBlnkCol(self):                     self.log(f'.blankCol=<{len(self.blankCol)}> {self.blankCol}')
    def dumpBlnkRow(self):                     self.log(f'.blankRow=<{len(self.blankRow)}> {self.blankRow}')
    def fmtn(self, pfx='n=', n=None):          n = n if n is not None else self.n    ;    return f'{pfx}{util.fmtl(n)}'
    def fmtv(self, pfx='v=', v=None):          v = v if v is not None else self.v    ;    return f'{pfx}{util.fmtl(v)}'
    def dl(  self, data=None, p=0, l=0, s=0):  return list(map(len,                       self.dpls(data, p, l, s)))
    def dt(  self, data=None, p=0, l=0, s=0):  return list(map(type,                      self.dpls(data, p, l, s)))
    def dtA( self, data=None, p=0, l=0, s=0):  return [ str(type(a)).strip('<>') for a in self.dpls(data, p, l, s) ]
    def dproxy(self, data):                    return data if data is not None else self.data
    def dpls(  self, data=None, p=0, l=0, s=0):
        data = self.dproxy(data)
        if p > len(data):           msg = f'ERROR BAD p index {p=} {l=} {s=} {len(data)=}'        ;  self.log(msg)  ;  raise SystemExit(msg)
        if l > len(data[p]):        msg = f'ERROR BAD l index {p=} {l=} {s=} {len(data[p])=}'     ;  self.log(msg)  ;  raise SystemExit(msg)
        if s > len(data[p][l]):     msg = f'ERROR BAD s index {p=} {l=} {s=} {len(data[p][l])=}'  ;  self.log(msg)  ;  raise SystemExit(msg)
        return data, data[p], data[p][l], data[p][l][s]
    ####################################################################################################################################################################################################
    def fmtdl( self, data=None, fdl=0):       txt = FDL if fdl else ''  ;  return f'{txt}{util.fmtl(self.dl(data))}'
    def fmtdt( self, data=None, fdt=0):       txt = FDT if fdt else ''  ;  return txt + f"[{' '.join([ t.replace('class ', '') for t in self.dtA(data) ])}]"
    ####################################################################################################################################################################################################
    def initData(self):
        self._initDataPath()
        if self.GEN_DATA: self.genDataFile(self.dataPath1)
        self.readDataFile(self.dataPath1)
        util.copyFile    (self.dataPath1, self.dataPath2)
#        self.data       = self.transposeData(dump=1)

    def _initDataPath(self):
        dataDir   = 'data'  ;  dataSfx = '.dat'  ;  dataPfx = f'.{self.n[S]}'
        baseName  = self.dfn if self.dfn else BASE_NAME + dataPfx + dataSfx
        dataName0 = baseName + '.asv'
        dataName1 = baseName
        dataName2 = baseName + '.bck'
        self.dataPath0 = BASE_PATH / dataDir / dataName0
        self.dataPath1 = BASE_PATH / dataDir / dataName1
        self.dataPath2 = BASE_PATH / dataDir / dataName2
        self.log(f'{dataName0=}')
        self.log(f'{dataName1=}')
        self.log(f'{dataName2=}')
        self.log(f'{self.dataPath0=}', pfx=0)
        self.log(f'{self.dataPath1=}', pfx=0)
        self.log(f'{self.dataPath2=}', pfx=0)
    ####################################################################################################################################################################################################
    def saveDataFile(self, why, path, dbg=1):
        if dbg:   self.log(f'{why} {path}')
        with open(path, 'w') as DATA_FILE:
            self.log(f'{DATA_FILE.name:40}', pfx=0)
            data = self.data
#            if    self.isVert(): data = self.transposeData()
#            else:                data = self.data
            self.log(f'{self.fmtn()} {self.fmtdl(data)}')
            for p in range(len(data)):
                if dbg: self.log(f'writing {p+1}{util.ordSfx(p+1)} page', pfx=0)
                for l in range(len(data[p])):
                    if dbg: self.log(f'writing {l+1}{util.ordSfx(l+1)} line', pfx=0)
                    for s in range(len(data[p][l])):
                        text = ''
                        for t in range(len(data[p][l][s])):
                            text += data[p][l][s][t]
                        if dbg: self.log(f'writing {s+1}{util.ordSfx(s+1)} string {text}', pfx=0)
                        DATA_FILE.write(f'{text}\n')
                    DATA_FILE.write('\n')
        size = path.stat().st_size   ;   self.log(f'{self.fmtn()} {self.fmtdl()} {size=}')
        return size
    ####################################################################################################################################################################################################
    def genDataFile(self, path):
        self.log(f'{path} {self.fmtn()}')
        np, nl, ns, nt = self.n
        self.dmpBlnks()
        self.data = [ [ [ self.blankRow for _ in range(ns) ] for _ in range(nl) ] for _ in range(np) ]
        size = self.saveDataFile('Generated Data', path)
        self.log(f'{path} {size=} {len(self.data)=}')
        self.data = []
        return size
    ####################################################################################################################################################################################################
    def readDataFile(self, path, dbg=1):
        nl = self.n[L]   ;   ns = self.n[S]   ;   sp, sl, ss, st = 0, 0, 0, 0
        if dbg:                 self.log(f'BGN {self.fmtn()}')
        if not path.exists():   self.log(f'WARN Invalid Data File Path {path} -> Touch Data File')   ;   path.touch()
        stat = path.stat()  ;   size = stat.st_size
        if size == 0:           self.log(f'WARN Zero Len Data File  {path} -> Generate Data File')   ;   size = self.genDataFile(path)
        if size == 0:           msg = f'ERROR Zero Len Data File {size=}'   ;   self.log(msg)   ;   self.quit(msg)
        with open(path, 'r') as DATA_FILE:
            DATA_FILE.seek(0, 2)      ;     size = DATA_FILE.tell()   ;   DATA_FILE.seek(0, 0)
            self.log(f'{DATA_FILE.name:40} {size:3,} bytes = {size/1024:3,.1f} KB')
            self.log('Raw Data File BGN:')
            data = self.data          ;     lines, strings = [], []   ;   ntabs = 0
            for tabs in DATA_FILE:
                tabs = tabs.strip()
                if tabs:
                    if not ntabs:             ntabs  = len(tabs)
                    if len(tabs) != ntabs:      msg  = f'ERROR BAD tabs len {len(tabs)=} != {ntabs=}'   ;   self.log(msg)   ;   self.quit(msg)
                    strings.append(tabs)     ;   st += len(tabs)      ;     ss += 1
                else:
                    if strings and not (ss % ns): lines.append(strings)   ;   strings = []   ;   sl += 1
                    if lines   and not (sl % nl):  data.append(lines)     ;   lines   = []   ;   sp += 1
                self.log(f'{tabs}', pfx=0)
            if strings: lines.append(strings)   ;   sl += 1
            if lines:    data.append(lines)     ;   sp += 1
            self.log('Raw Data File END:')
            self.log(f'{self.fmtdl()=} {self.fmtdt()=}')
            self.checkDataFileSize(sl, size)  ;  self.checkData()
            np, nl, ns, nt = self.n
            self.log(f'{sp} ({sl/nl:6.3f}) pages = {sl} lines =           {ss} strings =           {st} tabs')
            self.log(f'{np} ({sl/nl:6.3f}) pages @ {nl} lines per page, @ {ns} strings per line, @ {nt} tabs per string')
            self.dumpDataFile(data)
    ####################################################################################################################################################################################################
    def checkDataFileSize(self, nlines, ref):
        np, nl, ns, nt = self.dl()          ;  crlf = 2
        dsize = nlines * ns * nt            ;  self.log(f'{dsize=:3,} = {nlines=:3,} *     {ns=:2} *   {nt=}')
        crlfs = nlines * (ns + 1) * crlf    ;  self.log(f'{crlfs=:3,} = {nlines=:3,} * {(ns+1)=:2} * {crlf=}')
        size  =  dsize + crlfs              ;  self.log(f' {size=:3,} =  {dsize=:3,} +  {crlfs=:3,} = {ref=}')
        assert size == ref, f'{size=:4,} == {ref=:4,}'

    def dumpDataFile(self, data=None):
        data = self.dproxy(data)
        np, nl, ns, nt = self.dl()
        self.log(f'BGN {np} pages, {nl} lines per page, {ns} strings per line, {nt} tabs per string')
        for p in range(len(data)):
            for l in range(len(data[p])):
                for s in range(len(data[p][l])):
                    self.log(f'{data[p][l][s]}', pfx=0)
#                self.log(pfx=0)
        self.log(f'END {np} pages, {nl} lines per page, {ns} strings per line, {nt} tabs per string')
    ####################################################################################################################################################################################################
    def isVert(self, data=None, dbg=1):  # N/A
        l, t = self.dl(data), self.dt(data)
        if dbg: self.log(f'BGN {self.fmtdl()=} {self.fmtdt()=}')
        assert t[0] is list and t[1] is list and t[2] is list and t[3] is str, f'{l=} {t=}'
        vert = 1 if l[2] > l[3] else 0
        self.checkData(data=None)
        self.log(f'{util.fmtl(self.dplc()[0])}', pfx=0)
        if dbg: self.log(f'END {self.fmtdl()=} {self.fmtdt()=} {vert=}')
        return vert

    def checkData(self, data=None):
        data = self.dproxy(data)   ;   n = self.dl(data)
        assert n == self.n, f'{self.fmtn(n=n)} .n={self.fmtn("")}'
        np, nl, ns, nt = n
        assert len(data) == np, f'{len(data)=} {np=}'
        for p in range(np):
            assert len(data[p]) == nl, f'{len(data[p])=} {nl=}'
            for l in range(len(data[p])):
                assert len(data[p][l]) == ns, f'{len(data[p][l])=} {ns=}'
                for s in range(len(data[p][l])):
                    assert len(data[p][l][s]) == nt, f'{len(data[p][l][s])=} {nt=}'
    ####################################################################################################################################################################################################
    def transposeData(self, data=None, dump=0, dbg=1):  # N/A
        data = self.dproxy(data)
        self.log(f'BGN {self.fmtDxD(data)} {dump=}')
        if dump:        self.dumpDataVert( data) if self.isVert( data) else self.dumpDataHorz( data)
        Xdata, msg1, msg2 = [], [], []
        self.log(f'{self.fmtdl()} {self.fmtdt()}')
        self.log(f'dl={self.fmtdl(data)} dt={self.fmtdt(data)}') if dbg else None
        for p, page in enumerate(data):
            Xpage = []
            for l, line in enumerate(page):
                if dbg: msg1.append(f'{util.fmtl(line,  d1="")}')
                Xline = list(map(''.join, itertools.zip_longest(*line, fillvalue=' ')))
                if dbg: msg2.append(f'{util.fmtl(Xline, d1="")}')
                Xpage.append(Xline)
            Xdata.append(Xpage)
        if dbg: [self.log(m, pfx=0) for m in msg1];   self.log(pfx=0)
        if dbg: [self.log(m, pfx=0) for m in msg2]
        if dump:        self.dumpDataVert(Xdata) if self.isVert(Xdata) else self.dumpDataHorz(Xdata)
        self.log(f'END {self.fmtDxD(Xdata)} {dump=}')
        return Xdata
    ####################################################################################################################################################################################################
    def dumpDataHorz(self, data=None, lc=1, ll=1, i=0):
        data = data or self.data
        self.log(f'BGN {self.fmtDxD(data)} {lc=} {ll=} {i=}')
        for p in range(len(data)):
            #            if ll:  plt = f'{JTEXTS[P]} {p+1}'  ;  plab = f'{plt:{i+1}}'  ;  self.log(f'{Z*i}{plab}', pfx=0)
            for l in range(len(data[p])):
                if ll:  llt = f'{JTEXTS[P]} {p + 1}';  llab = f'{llt:{i + 1}} ';  self.log(f'{Z * i}{llab}', pfx=0, end='');   self.log(f'{JTEXTS[L]} {l + 1}', pfx=0)
                #                if ll:  llt = f'{JTEXTS[L]} {l+1}'  ;  llab = f'{llt:{i+1}}'  ;  self.log(f'{Z*i}{llab}', pfx=0)
                if lc:  self.dumpDataLabels(data[p][l], i=i, sep=Z)
                for r in range(len(data[p][l])):
                    self.log(f'{Z * i}', pfx=0, end='')
                    for c in range(len(data[p][l][r])):
                        self.log(f'{data[p][l][r][c]}', pfx=0, end='')
                    self.log(pfx=0)
                self.log(pfx=0)
        self.log(f'END {self.fmtDxD(data)} {lc=} {ll=} {i=}')

    def dumpDataVert(self, data=None, lc=1, ll=1, i=0):
        data = data or self.data
        w = max(len(data[0][0][0]), len(JTEXTS[P]) + 2, len(JTEXTS[L]) + 2)  ;   txt = Z * i + JTEXTS[C] + Z if i >= 0 else JTEXTS[C]
        self.log(f'BGN {self.fmtDxD(data)} {lc=} {ll=} {i=} {w=} {txt=}')
        for p in range(len(data)):
            if ll: self.log(f'{JTEXTS[P]} {p + 1}', pfx=0);  self.log(f'{txt:{3}}', pfx=0, end='')  ;  txt2 = [ f'{JTEXTS[L]} {l + 1}' for l in range(len(data[0])) ]  ;  self.log(f'{util.fmtl(txt2, w=w, d1="")}', pfx=0)
            for c in range(len(data[p][0])):
                pfx = f'{c + 1:3} ' if i >= 0 and lc else ''  ;   self.log(f'{pfx}{Z * i}', pfx=0, end='')
                for l in range(len(data[p])):
                    self.log(f'{data[p][l][c]}', pfx=0, end=Z)
                self.log(pfx=0)
        self.log(f'END {self.fmtDxD(data)} {lc=} {ll=} {i=}')
    ####################################################################################################################################################################################################
    def dumpDataLabels(self, data=None, i=0, sep='%'):
        p, q = '', ''
        data = data if data is not None else self.data
        n = len(data[0])   ;   a = ' ' * i if i else ''  ;  b = sep * n  ;  r = sep * 3
        if n >= 100:   self.log(   f'{a}{p}', pfx=0, end='')  ;  [ self.log(f'{c//100}'   if c>=100 else ' ', pfx=0, end='') for c in range(1, n+1) ]  ;  self.log(pfx=0)
        if n >= 10:    self.log(   f'{a}{p}', pfx=0, end='')  ;  [ self.log(f'{c//10%10}' if c>=10  else ' ', pfx=0, end='') for c in range(1, n+1) ]  ;  self.log(pfx=0)
        self.log(                  f'{a}{q}', pfx=0, end='')  ;  [ self.log(f'{c%10}',                        pfx=0, end='') for c in range(1, n+1) ]  ;  self.log(pfx=0)
        if sep != '':  self.log(f'{a}{r}{b}', pfx=0)
    ####################################################################################################################################################################################################
    def toggleBlank(self, why):
        prevBlank    =  self.blank
        self.log(f'BGN {why} {prevBlank=}')
        self.blanki = (self.blanki + 1) % len(self.blanks)
        self.blank  =  self.blanks[self.blanki]
#        self.swapSrc, self.swapTrg, self.swapping = prevBlank, self.blank, 2
#        self.swapTab(why, '\r')
        self.log(f'END {why} {self.blank=}')

    def toggleCsrMode(self, why):
        self.dumpCrsArrows(why)
        self.csrMode  = (self.csrMode + 1) % len(C_MODES)
        self.dumpCrsArrows(why)

    def toggleArrow(self, why, v):
        self.dumpCrsArrows(why)
        if v: self.vArrow *= -1
        else: self.hArrow *= -1
        self.dumpCrsArrows(why)
    ####################################################################################################################################################################################################
    def dumpCrsArrows(self, why): c, h, v = self.csrMode, self.hArrow, self.vArrow  ;  self.log(f'{why} {C_MODES[c]:6} {H_ARWS[h]:5} {V_ARWS[v]:4}')
    def fchv(self): c, h, v = self.csrMode, self.hArrow, self.vArrow  ;  return f'{C_MODES[c][0]} {H_ARWS[h][0]} {V_ARWS[v][0]}'
    def reverseArrow(self, dbg=1):
        if dbg: self.dumpCrsArrows('reverseArrow()')
        if self.csrMode == MELODY or self.csrMode == ARPG: self.toggleArrow('reverseArrow() MELODY or ARPG', v=0)
        if self.csrMode == CHORD  or self.csrMode == ARPG: self.toggleArrow('reverseArrow() CHORD or ARPG',  v=1)
        if dbg: self.dumpCrsArrows('reverseArrow()')

    def setCHVMode(self, why, c=None, h=None, v=None):
        self.dumpCrsArrows(f'BGN {why} {c=} {h=} {v=}')
        if c is not None: self.csrMode = c
        if h is not None: self.hArrow  = h
        if v is not None: self.vArrow  = v
        self.dumpCrsArrows(f'END {why} {c=} {h=} {v=}')
    ####################################################################################################################################################################################################
    def fCrsCrt(self): return self.fmtCrs(), self.fmtCrt()
    def fmtCrs( self): return self.getTabsView().fmtCrs()
    def fmtCrt( self): return self.fmtCrtA(), self.fmtCrtB()
    def fmtCrtA(self): return f'{self.focus.caret.position}:{fmark(self.focus.caret.mark)}'
    def fmtCrtB(self): return f'{self.getTabsView().caret.position}:{fmark(self.getTabsView().caret.mark)}'
    ####################################################################################################################################################################################################
    def isAlt(self):          return 1 if self.kbks[wink.MOD_ALT]   or self.kbks[wink.LALT]   or self.kbks[wink.RALT]   else 0
    def isCtrl(self):         return 1 if self.kbks[wink.MOD_CTRL]  or self.kbks[wink.LCTRL]  or self.kbks[wink.RCTRL]  else 0
    def isShift(self):        return 1 if self.kbks[wink.MOD_SHIFT] or self.kbks[wink.LSHIFT] or self.kbks[wink.RSHIFT] else 0
    def isCtrlShift(self):    return 1 if self.isCtrl() and self.isShift() else 0
    def isAltShift(self):     return 1 if self.isAlt()  and self.isShift() else 0
    def isCtrlAlt(self):      return 1 if self.isCtrl() and self.isAlt()   else 0
    def isCtrlAltShift(self): return 1 if self.isCtrl() and self.isAlt()   and self.isShift() else 0
    ####################################################################################################################################################################################################
#    def isBTab(self, text):   return 1 if text in self.blanks else 0  # text == self.blank
    def isTab(self, text): return 1 if self.sobj.isFret(text) or text in util.DSymb.SYMBS or text == Z else 0
    ####################################################################################################################################################################################################
    def getTabsView(self): return self.views[0]

    def fp(self):    return f'{self.fplst()} {self.fmtCrs()} {self.fchv()}' #  {self.vcp()} {self.docW()} {self.fplst()}
    def fplst(self): p, l = 0, 0,  ;   s, t = self.crt2st(self.getTabsView().caret, dbg=0)  ;  p, l, s, t = self.plstN(p, l, s, t)  ;  return f'{p} {l} {s} {t}'
#    def fplst(self): p, l, s, t = self.plst(dbg=0)  ;  return f'{p} {l} {s} {t:2}'
#    def fplst(self): self.p, self.l, self.s, self.t = self.plst(dbg=0)  ;  return f'{self.p} {self.l} {self.s} {self.t:2}'
    def docW(self):  return self.dl()[T] + 1
    def vcp(self):   return self.getTabsView().caret.position
    def plst2cc(self, p, l, s, t): np, nl, ns, nt = self.dl()  ;  return p*np + l*nl + s*ns + t*nt

    def plstN(self, p, l, s, t):
        np, nl, ns, nt = self.n
        return p % np, l % nl, s % ns, t % (nt+1)

    def plstN_A(self, p, l, s, t, n=0, dbg=0):
        np, nl, ns, nt = self.n
        if dbg: self.log(f'BGN {n=} {p} {l} {s} {t}')
        t2 = n + t
        s2 = t2//nt + s
        l2 = s2//ns + l
        p2 = l2//nl + p
        if dbg: self.log(f'    {n=} {p2} {l2} {s2} {t2}')
        t3 = t2 % nt
        s3 = s2 % ns
        l3 = l2 % nl
        p3 = p2 % np
        if dbg: self.log(f'END {n=} {p3} {l3} {s3} {t3}')
        return p3, l3, s3, t3

    def _move(self, why, m, dbg=1):
        v = self.getTabsView()  ;  np, nl, ns, nt = self.n  ;  mt = f'{m:x}' if m is not None else 'None'
        s = v.caret.line % ns   ;  t = v.caret.position % (nt+1)
        ds = 0   ;  dt = 0
        if   m == wink.MOTION_RIGHT: dt = 1
        elif m == wink.MOTION_LEFT:  dt = -1
        elif m == wink.MOTION_UP:    ds = -1
        elif m == wink.MOTION_DOWN:  ds = 1
        if dbg: self.log(f'{self.fp()} BGN {why} {mt} {s} {ds} {t} {dt}')
        self.moveCrt(s, t, ds, dt)
        if dbg: self.log(f'{self.fp()} END {s} {ds} {t} {dt}')

    def moveCrt(self, s, t, ds, dt):
        self.getTabsView().setCrs(s+ds, t+dt)

    def j(self): return [ i-1 if i else 0 for i in self.i ]
    def m2plst(self, m=None, dbg=1):
        v = self.getTabsView()  ;  ns = self.n[S]     ;  nt = self.n[T]  ;  mt = f'{m:x}' if m is not None else 'None'
        p = 0    ;    l = 0     ;  s = v.caret.line % ns   ;  t = v.caret.position % (nt+1)  ;  s0 = s  ;  t0 = t
        if   t == 0 and s == 0 and m in BACKWARD:  t = nt-1  ;  s = ns-1  ;                 self.log(f's={s0} t={t0} {mt} {s=} {t=}')
        elif s == 0            and m in UPWARD:    t += 1    ;  t = t % nt ;  s = ns-1   ;  self.log(f's={s0} t={t0} {mt} {s=} {t=}')
        elif t == nt           and m in BACKWARD:  t = nt-1  ;                              self.log(f's={s0} t={t0} {mt} {s=} {t=}')
        elif t == nt           and m in FORWARD:   t = 0     ;  s += 1    ;  s = s % ns  ;  self.log(f's={s0} t={t0} {mt} {s=} {t=}')
        if dbg: self.log(f'{self.fp()}')
        return p, l, s, t

    def NEW_2_plst(self, m=None, dbg=1):
        v = self.getTabsView()  ;  ns = self.n[S]     ;  nt = self.n[T]  ;  mt = f'{m:x}' if m is not None else 'None'
        p = 0    ;    l = 0     ;  s = v.caret.line % ns   ;  t = v.caret.position % (nt+1)  ;  s0 = s  ;  t0 = t
        if   t == 0 and s == 0:
            if   m in BACKWARD:  t = nt-1  ;  s = ns-1  ;                 self.log(f's={s0} t={t0} {mt} {s=} {t=}')
            elif m in UPWARD:    t += 1    ;  t = t % nt ;  s = ns-1   ;  self.log(f's={s0} t={t0} {mt} {s=} {t=}')
        elif s == 0:
            if   m in UPWARD:    t += 1    ;  t = t % nt ;  s = ns-1   ;  self.log(f's={s0} t={t0} {mt} {s=} {t=}')
        elif t == nt:
            if   m in BACKWARD:  t = nt-1  ;                              self.log(f's={s0} t={t0} {mt} {s=} {t=}')
            elif m in FORWARD:   t = 0     ;  s += 1    ;  s = s % ns  ;  self.log(f's={s0} t={t0} {mt} {s=} {t=}')
        if dbg: self.log(f'{self.fp()}')
        return p, l, s, t

    def NEW_1_plst(self, m=None, dbg=1):
        v = self.getTabsView()  ;  ns = self.n[S]     ;  nt = self.n[T]  ;  mt = f'{m:x}' if m is not None else 'None'
        p = 0    ;    l = 0     ;  s = v.caret.line % ns   ;  t = v.caret.position % (nt+1)  ;  s0 = s  ;  t0 = t
        if   t == nt:
            if   m in BACKWARD:  t = nt-1  ;                              self.log(f's={s0} t={t0} {mt} {s=} {t=}')
            elif m in FORWARD:   t = 0     ;  s += 1    ;  s = s % ns  ;  self.log(f's={s0} t={t0} {mt} {s=} {t=}')
        elif t == 0 and s == 0:
            if   m in BACKWARD:  t = nt-1  ;  s = ns-1  ;                 self.log(f's={s0} t={t0} {mt} {s=} {t=}')
        if dbg: self.log(f'{self.fp()}')
        return p, l, s, t

    def OLD_plst(self, m=None, dbg=1):
        v = self.getTabsView()  ;  ns = self.n[S]     ;  nt = self.n[T]  ;  mt = f'{m:x}' if m is not None else 'None'
        p = 0    ;    l = 0     ;  s = v.caret.line % ns   ;  t = v.caret.position % (nt+1)  ;  s0 = s  ;  t0 = t
        if   s == 0 and t == 0:
            if   m in BACKWARD:  t = nt-1  ;  s -= 1  ;  s = s % ns  ;  self.log(f's={s0} t={t0} {mt} {s=} {t=}')
            elif m in UPWARD:    s = ns-1  ;  t += 1  ;  t = t % nt  ;  self.log(f's={s0} t={t0} {mt} {s=} {t=}')
        elif s == 0 and t == nt:
            if   m in FORWARD:   t = 0     ;  s -= 1  ;  s = s % ns  ;  self.log(f's={s0} t={t0} {mt} {s=} {t=}')
            elif m in UPWARD:    s = ns-1  ;  t += 1  ;  t = t % nt  ;  self.log(f's={s0} t={t0} {mt} {s=} {t=}')
        elif s == ns and t == 0:
            if   m in BACKWARD:  t = nt-1  ;  s -= 1  ;  s = s % ns  ;  self.log(f's={s0} t={t0} {mt} {s=} {t=}')
            elif m in DOWNWARD:  s = 0     ;  t += 1  ;  t = t % nt  ;  self.log(f's={s0} t={t0} {mt} {s=} {t=}')
        elif s == ns and t == nt:
            if   m in FORWARD:   t = 0     ;  s -= 1  ;  s = s % ns  ;  self.log(f's={s0} t={t0} {mt} {s=} {t=}')
            elif m in DOWNWARD:  s = 0     ;  t += 1  ;  t = t % nt  ;  self.log(f's={s0} t={t0} {mt} {s=} {t=}')
        elif s == 0:
            if   m in UPWARD:    s = ns-1  ;  t += 1  ;  t = t % nt  ;  self.log(f's={s0} t={t0} {mt} {s=} {t=}')
        elif s == ns:
            if   m in DOWNWARD:  s = 0     ;  t += 1  ;  t = t % nt  ;  self.log(f's={s0} t={t0} {mt} {s=} {t=}')
        elif t == 0:
            if   m in BACKWARD:  t = nt-1  ;  s -= 1  ;  s = s % ns  ;  self.log(f's={s0} t={t0} {mt} {s=} {t=}')
        elif t == nt:
            if   m in BACKWARD:  t = nt-1
            elif m in FORWARD:   t = 0     ;  s += 1  ;  s = s % ns  ;  self.log(f's={s0} t={t0} {mt} {s=} {t=}')
#        s += self.hArrow if self.csrMode == ARPG else 0  ;  s = s % self.n[S]
#        if t >= self.dl()[T]: v.caret.line += 1  ;  l += v.caret.line // self.dl()[S]  ;  t = v.caret.position % n  ;  t -= 1 if t == n else 0
        if dbg: self.log(f'{self.fp()}')
        return p, l, s, t
    ####################################################################################################################################################################################################
    def on_draw(self, dbg=1):
        pyglet.gl.glClearColor(1, 1, 1, 1)
        self.clear()
        self.batch.draw()
        if self.snapReg: self.snapReg = 0  ;  self.snapshot()  ;  self.log(f'{self.snapWhy=} {self.snapType=} {self.snapId=}') if dbg else None
    ####################################################################################################################################################################################################
    def setFocus(self, focus, dbg=0):
        if dbg: self.log(f'BGN {id(focus)=} {id(self.focus)=}')
        if focus is self.focus:        self.log(f'{id(focus)=} is {id(self.focus)=}') if dbg else None  ;  return
        if self.focus:
            self.focus.caret.visible = False
            self.focus.caret.mark    = self.focus.caret.position = 0
            self.log(f'{self.focus.caret.visible=} {self.focus.caret.position=} {fmark(self.focus.caret.mark)=}')
        self.focus = focus
        if self.focus:                 self.focus.caret.visible = True  ;  self.log(f'{self.focus.caret.visible=}') if dbg else None
        if dbg: self.log(f'END {id(focus)=} {id(self.focus)=}')
    ####################################################################################################################################################################################################
    def on_mouse_motion(self, x, y, dx, dy):
        for view in self.views:
            if view.hitTest(x, y): self.set_mouse_cursor(self.text_cursor)   ;    break
        else:                      self.set_mouse_cursor(None)

    def on_mouse_press(self, x, y, button, modifiers):
        for view in self.views:
            if view.hitTest(x, y): self.setFocus(view)   ;   break
        else:                      self.setFocus(None)
        if self.focus:             self.focus.caret.on_mouse_press(x, y, button, modifiers)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.focus:
            self.focus.caret.on_mouse_drag(x, y, dx, dy, buttons, modifiers)
    ####################################################################################################################################################################################################
    def OLD_on_text_motion(self, m):
        self.kbkInfo(motn=m)  ;  t = f'{m:x}'
        self.log(f'{self.fp()} BGN {t}')
#        if self.focus and (m == wink.MOTION_RIGHT or m == wink.MOTION_LEFT or m == wink.MOTION_UP or m == wink.MOTION_DOWN):
        if self.focus and (m != wink.MOTION_RIGHT and m != wink.MOTION_LEFT and m != wink.MOTION_UP and m != wink.MOTION_DOWN):
            self.log(f'{self.fp()} otm<{t}>')
            self.focus.caret.on_text_motion(m)
            return pyglet.event.EVENT_HANDLED
#            self.log(f'{self.fp()} otm<{t}>')
        if   self.isCtrlAltShift():            msg = f'@&^??? {t}'   ;   self.log(msg)
        elif self.isCtrlAlt():                 msg =  f'@&??? {t}'   ;   self.log(msg)
#            if   m == 1:                                self.unselectTabs(f' @& LEFT ({            m})',  nc
#            elif m == 2:                                self.unselectTabs(f' @& RIGHT ({           m})', -nc)
        elif self.isAltShift():                msg =  f'&^??? {t}'   ;   self.log(msg)
        elif self.isCtrlShift():               msg =  f'@^??? {t}'   ;   self.log(msg)
        elif self.isShift():
            if   m == wink.MOTION_UP:          msg =   f'^UP    {t}'  ;  self.move(msg, m)
            elif m == wink.MOTION_DOWN:        msg =   f'^DOWN  {t}'  ;  self.move(msg, m)
            elif m == wink.MOTION_LEFT:        msg =   f'^LEFT  {t}'  ;  self.move(msg, m)
            elif m == wink.MOTION_RIGHT:       msg =   f'^RIGHT {t}'  ;  self.move(msg, m)
            else:                              msg =   f'^??? {t}'    ;  self.log(msg)
        elif self.isAlt():                     msg =   f'&??? {t}'    ;  self.log(msg)
#            if   m == wink.MOTION_UP:                self.moveUp(      f' & UP ({          m})')
#            elif m == wink.MOTION_DOWN:              self.moveDown(    f' & DOWN ({        m})')
#            elif m == wink.MOTION_LEFT:              self.moveLeft(    f' & LEFT ({        m})')
#            elif m == wink.MOTION_RIGHT:             self.moveRight(   f' & RIGHT ({       m})')
        elif self.isCtrl():
#            if   m == wink.MOTION_PREVIOUS_WORD:     self.selectTabs(  f'@  LEFT ({        m})', -nc)
#            elif m == wink.MOTION_NEXT_WORD:         self.selectTabs(  f'@  RIGHT ({       m})',  nc)
            if   m == wink.MOTION_BEGINNING_OF_LINE: msg =  f'@BLINE {t}'   ;   self.log(msg) #  ;   self.quit(msg) # N/A
            elif m == wink.MOTION_END_OF_LINE:       msg =  f'@ELINE {t}'   ;   self.log(msg) #  ;   self.quit(msg) # N/A
            elif m == wink.MOTION_BEGINNING_OF_FILE: msg =  f'@BFILE {t}'   ;   self.log(msg) #  ;   self.quit(msg) # CTRL HOME
            elif m == wink.MOTION_END_OF_FILE:       msg =  f'@EFILE {t}'   ;   self.log(msg) #  ;   self.quit(msg) # CTRL END
            else:                                    msg =  f'@??? {t}'     ;   self.log(msg) #  ;   self.quit(msg)
        elif self.mods == 0:
            if   m == wink.MOTION_UP:                msg =    f'UP    {t}'  ;  self.move(msg, m)
            elif m == wink.MOTION_DOWN:              msg =    f'DOWN  {t}'  ;  self.move(msg, m)
            elif m == wink.MOTION_LEFT:              msg =    f'LEFT  {t}'  ;  self.move(msg, m)
            elif m == wink.MOTION_RIGHT:             msg =    f'RIGHT {t}'  ;  self.move(msg, m)
            elif m == wink.MOTION_DELETE:            msg =    f'DELETE    {t}'  ;  self.setTab(msg, self.blank)
            elif m == wink.MOTION_BACKSPACE:         msg =    f'BACKSPACE {t}'  ;  self.setTab(msg, self.blank)
#            elif m == wink.MOTION_BEGINNING_OF_LINE: msg =    f'BLINE {t}' ;  self.log(msg) # ;  self.move(msg, m) # self.fcTextMotn(msg)
#            elif m == wink.MOTION_END_OF_LINE:       msg =    f'ELINE {t}' ;  self.log(msg) # ;  self.moveEOL(msg, m) # self.fcTextMotn(msg, m)
#            if   m == wink.MOTION_PREVIOUS_WORD:     msg = f'MOTION_PREVIOUS_WORD {t}'  ;   self.log(msg) #  ;   self.quit(msg)
#            elif m == wink.MOTION_NEXT_WORD:         msg = f'MOTION_NEXT_WORD {t}'      ;   self.log(msg) #  ;   self.quit(msg)
#            else:                                    msg =    f'??? {t}'   ;   self.log(msg) #  ;   self.quit(msg)
        else:                                        msg =    f'??? {t}'   ;   self.log(msg) #  ;   self.quit(msg)
#        if self.SNAPS: self.regSnap(msg, 'otm')
#        if self.focus: self.log(f'{self.fp()} END {t}')
        return pyglet.event.EVENT_HANDLED
    ####################################################################################################################################################################################################
    def kbkInfo(self, symb=None, mods=None, motn=None, text=None, dbg=1):
        kbks = self.kbks
        msg = f'{self.fp()} {util.fmtl([ f"{k:x}" for k in kbks if kbks[k] ])} : {util.fmtl([ wink.symbol_string(k) for k in kbks if kbks[k] ])}'
        if symb:  self.symb,   self.symbTxt = symb, wink.symbol_string(symb)
        if mods:  self.mods,   self.modsTxt = mods, wink.modifiers_string(mods)
        if motn:  self.motn,   self.motnTxt = motn, wink.motion_string(motn)
        if text:               self.kbkTxt  = text
        if dbg:   self.log(f'{msg} {self.symbTxt} {self.modsTxt} {self.motnTxt} {self.kbkTxt}')
        return self.symbTxt, self.modsTxt, self.motnTxt, self.kbkTxt
    ####################################################################################################################################################################################################
    def on_key_press(self, symb, mods):
#        symbTxt, modsTxt, motnTxt, text = self.kbkInfo(symb, mods)  ;  msg = f'{symbTxt=} {modsTxt=} {motnTxt=} {text=}'  ;  self.log(msg)
        self.kbkInfo(symb, mods)
        if   symb == wink.ESCAPE:              msg = ' Quit'                                ;  self.log(msg)  ;  self.quit(msg, 0)
        elif symb == wink.S and self.isCtrl(): msg = '@s'                                   ;  self.log(msg)  ;  self.saveDataFile('@S', self.dataPath1)
        elif symb == wink.INSERT:              msg = 'INSERT'                               ;  self.log(msg)
        elif symb == wink.PAGEUP:              msg = '  PAGEUP xff55 MOTION_PREVIOUS_PAGE'  ;  self.log(msg)
        elif symb == wink.PAGEDOWN:            msg = 'PAGEDOWN xff56 MOTION_NEXT_PAGE'      ;  self.log(msg)
        elif symb == wink.TAB:
            if   self.isShift():               d = -1
            else:                              d = 1
            if   self.focus in self.views:     i = self.views.index(self.focus)
            else:                              d = 0  ;  i = 0
            self.setFocus(self.views[(i + d) % len(self.views)])

    def on_key_release(self, symb, mods):
        self.kbkInfo(symb, mods)
#        symbTxt, modsTxt, motnTxt, text = self.kbkInfo(symb, mods)  ;  msg = f'{symbTxt=} {modsTxt=} {motnTxt=} {text=}'  ;  self.log(msg)
    ####################################################################################################################################################################################################
    def on_text_motion(self, m, dbg=1):
        _, _, motnTxt, _ = self.kbkInfo(motn=m)
        if self.focus:
            msg = f'{m:x} {motnTxt=}'
            if dbg: self.log(f'BGN {msg}')
            if   m == wink.MOTION_NEXT_PAGE:     msg += f'PAGEDOWN xff55 MOTION_NEXT_PAGE'      ;  self.log(msg)
            elif m == wink.MOTION_PREVIOUS_PAGE: msg += f'  PAGEUP xff55 MOTION_PREVIOUS_PAGE'  ;  self.log(msg)
            self._move(msg, m)
#            s, t = self._on_text_motion(m, dbg)
#            v = self.getTabsView()
#            v.setCrs(s, t, dm=1)
            if dbg: self.log(f'END {msg}')
            return pyglet.event.EVENT_HANDLED

    def _on_text_motion(self, m, dbg=1):
        mt = f'otm<{wink.motion_string(m)}:{m:x}>'
        s0, t0 = self.crt2st(self.focus.caret, dbg)  ;  pos0 = self.focus.caret.position  ;  cc0 = self.plst2cc(0, 0, s0, t0)
        if dbg: self.log(f'{self.fp()} Before {mt} {s0:3} {t0:3} {pos0:3} {cc0:4}')
#        self.focus.caret.on_text_motion(m)
        self._move('otm', m)
        p, l, s, t = self.m2plst(m)  ;  pos = self.focus.caret.position  ;  cc = self.plst2cc(0, 0, s, t)
        if dbg: self.log(f'{self.fp()} After  {mt} {s:3} {t:3} {pos:3} {cc:4}')
#        if s == s0 and t == t0 and pos == pos0:
        return s, t
    ####################################################################################################################################################################################################
    def on_text_motion_select(self, ms, dbg=1):
        _, _, motnTxt, _ = self.kbkInfo(motn=ms)
        if self.focus:
            msg = f'{ms:x} {motnTxt=}'
            if dbg: self.log(f'BGN {msg}')
#            if   ms == wink.MOTION_UP:                msg = f'UP    {ms:x}'  ;  self.move(msg, ms)
            if dbg: ms = f'OTMS<{wink.motion_string(ms)}:{ms:x}>'
            self.log(f'{self.fp()} Before {ms}')
            self.focus.caret.on_text_motion_select(ms)
            self.log(f'{self.fp()} After  {ms}')
            if dbg: self.log(f'END {msg}')
            return pyglet.event.EVENT_HANDLED
    ####################################################################################################################################################################################################
    def on_text(self, text, dbg=1):
        symbTxt, modsTxt, motnTxt, text = self.kbkInfo(text=text)
        if self.focus:
            msg = f'{symbTxt=} {modsTxt=} {motnTxt=} {text=}'  ;  t = f'<{text}>'
            if dbg: self.log(f'BGN {msg}')
            if self.isShift():
                if   text == '$':  msg = f'^${t} snapshot'        ;  self.log(msg, so=1)  ;  self.snapshot(msg, 'SNP')
                elif text == 'S':  msg = f'^S{t} saveDataFile'    ;  self.log(msg, so=1)  ;  self.saveDataFile(msg, self.dataPath1)
                elif text == 'T':  msg = f'^T{t} toggleCsrMode'   ;  self.log(msg, so=1)  ;  self.toggleCsrMode(msg)
                elif text == 'V':  msg = f'^V{t} toggleArrow(1)'  ;  self.log(msg, so=1)  ;  self.toggleArrow(msg, v=1)
            elif self.isTab(text): msg =   f'{t} setTab'                                  ;  self.setTab(msg, text)
#                self.log(f'{self.fp()} Before {t}')
#                self.focus.caret.on_text(text)
#                self.log(f'{self.fp()} After  {t}')
            elif text == 'v':      msg =  f'v{t} toggleArrow(0)'  ;  self.log(msg, so=1)  ;  self.toggleArrow(msg, v=0)
            if dbg: self.log(f'END {msg}')
            return pyglet.event.EVENT_HANDLED
    ####################################################################################################################################################################################################
    def fcTextMotn(self, msg, dbg=1):
        mode = self.csrMode       ;  r = wink.MOTION_RIGHT  ;  l = wink.MOTION_LEFT  ;     m = None
        wms = wink.motion_string  ;  u = wink.MOTION_UP     ;  d = wink.MOTION_DOWN  ;  msg2 = f'move'
        if mode == MELODY or mode == ARPG: m = r if self.hArrow == RIGHT else l  ;  self._fcTextMotn(f'otm<{wms(m)}>', m)
        if mode == CHORD  or mode == ARPG: m = d if self.vArrow == DOWN  else u  ;  self._fcTextMotn(f'otm<{wms(m)}>', m)
        self.log(f'{self.fp()} Before {msg2}')
        self._move(msg, m)
        self.log(f'{self.fp()} After  {msg2}')
        if dbg: self.regSnap(msg, 'SPC')

    def _fcTextMotn(self, msg, m):
        self.log(f'{self.fp()} Before {msg}')
        self.focus.caret.on_text_motion(m)
        self.log(f'{self.fp()} After {msg}')

    def NOT_USED_getTextMotn(self, msg):
        m = None  ;  msg += f' {self.csrMode=} {self.hArrow=} {self.vArrow=}'
        if self.csrMode == MELODY or self.csrMode == ARPG: m = wink.MOTION_RIGHT if self.hArrow == RIGHT else wink.MOTION_LEFT
        if self.csrMode == CHORD  or self.csrMode == ARPG: m = wink.MOTION_DOWN  if self.vArrow == DOWN  else wink.MOTION_UP
        t = wink.motion_string(m)
        self.log(f'{msg} return {t}:{m=:x}')
        return m
    ####################################################################################################################################################################################################
    def move(self, why, m, dbg=1):
        mt = f'{m:x}' if m is not None else ''
        if dbg: self.log(f'{self.fp()} BGN {why} {mt}')
        for i, v in enumerate(self.views):
            if self.focus:
                d = 1 if m != wink.MOTION_END_OF_LINE else -1
#                s0, t0 = self.crt2st(v.caret)  ;  n0 = v.caret.mark
                p, l, s, t = self.m2plst(m)
                v.caret.mark = t + d   ;  n = v.caret.mark
                dn = v.caret.mark - v.caret.position if v.caret.mark is not None else d
                if dbg: self.log( f'{self.fp()} v[{i}] {mt} {d} Before {s=} {t=} {n=} {dn=} ')
                v.setCrs(s, t, dm=dn)
                if dbg: v.dumpCrs(f'{self.fp()} v[{i}] {mt} {d} After  {s=} {t=} {n=} {dn=} ')
        if dbg: self.log(f'{self.fp()} END {why} {mt}')

    def crt2st(self, crt, dbg=1): self.log(f'{crt.line=} {crt.position=}') if dbg else None  ;  return crt.line, crt.position
#        s  = crt.line      ;  t = crt.position  ;  n0 = crt.mark
#        self.i[S] = s+1 ;  self.i[T] = t+1
#        crt.mark = t + d   ;  n = crt.mark
#        dn = crt.mark - crt.position if crt.mark is not None else d
#        return s, t

    def NOT_USED_moveEOL(self, msg='', m=None, dbg=1):
        if dbg: self.log(f'{self.fp()} BGN {msg} {m=}')
        for i, v in enumerate(self.views):
            s  = v.caret.line  ;  t = self.docW()-1
            dm = v.caret.mark - v.caret.position if v.caret.mark is not None else 1
            if dbg: self.log( f'{self.fp()} v[{i}] {s=} {t=} {dm=} before {t}')
            v.setCrs(s, t, dm=dm)
            if dbg: v.dumpCrs(f'{self.fp()} v[{i}] {s=} {t=} {dm=} after  {t}')
        if dbg: self.log(f'{self.fp()} END {msg} {m=}')
    ####################################################################################################################################################################################################
    def setTab(self, why, text, dbg=1):
        msg = f'{why} <{text}>'  ;     self.log(f'{self.fp()} BGN {msg}')
        if text == Z: self.fcTextMotn(msg)  ;  return
        p, l, s, t  = self.m2plst()           ;  data = self.data[p][l][s][t]  ;  cc = self.plst2cc(p, l, s, t)
        if dbg: self.log(f'{self.fp()} Before {msg} <{data}> {cc=}')
        self.setDTNIK(text, cc, p, l, s, t, kk=1)
        p, l, s, t  = self.m2plst()           ;  data = self.data[p][l][s][t]
        if dbg: self.log(f'{self.fp()} After  {msg} <{data}> {cc=}')
        self.log(f'{self.fp()} Before ot<{text}>')
        self.focus.caret.on_text(text)
        self.log(f'{self.fp()} After  ot<{text}>')
        if   self.csrMode == CHORD:  s += self.vArrow
        elif self.csrMode == MELODY: t += self.hArrow
        elif self.csrMode == ARPG:   s += self.vArrow  ;  t += self.hArrow
        self.getTabsView().setCrs(s, t, dm=1)
        TYP = f'TXT_{text}' if self.sobj.isFret(text) else 'SMB' if text in util.DSymb.SYMBS  else 'UNK'
        if self.SNAPS: self.regSnap(f'{msg}', TYP)
        self.log(f'{self.fp()} END {msg}')
#        self.resyncData = 1
    ####################################################################################################################################################################################################
    def setDTNIK(self, text, cc, p, l, s, t, kk=0, dbg=1):
        if dbg: self.log(f'{self.fp()} {text=} {cc=} {kk=}')
        self.setData(text, p, l, s, t)
#        imap = self.getImap(p, l, s)
#        if TT in self.v: self.setTab2( text, cc)
#        if NN in self.v: self.setNote( text, cc, s)
#        if II in self.v: self.setIkey( imap, p, l, s)
#        if KK in self.v: self.setChord(imap, p, l, s)
#        if dbg: self.log(f'END {cc=} {kk=}    {text=}') #{len(imap)=}')
    ####################################################################################################################################################################################################
    def setData(self, text, p, l, s, t, dbg=1):
        data = self.data[p][l][s]
#        if dbg: self.log(f'BGN {t=} {text=} {data=}')
        self.data[p][l][s] = data[0:t] + text + data[t+1:]
        data = self.data[p][l][s]
        if dbg: self.log(f'{self.fp()} {text=} {t=} {data=}')

    def setTab2(self, text, cc, dbg=1):
        if dbg: self.log(f'BGN         {text=} tabs[{cc}]={self.tabs[cc].text}')
        self.tabs[cc].text = text
        if dbg: self.log(f'END         {text=} tabs[{cc}]={self.tabs[cc].text}')

    def setNote(self, text, cc, t, dbg=1):
        if dbg: self.log(f'BGN     {t=} {text=} notes[{cc}]={self.notes[cc].text}')
        self.notes[cc].text = self.sobj.tab2nn(text, t) if self.sobj.isFret(text) else self.blank
        if dbg: self.log(f'END     {t=} {text=} notes[{cc}]={self.notes[cc].text}')
    ####################################################################################################################################################################################################
    def dumpViews(self, views=None):
        views = views if views is not None else self.views
        if not views:  self.log(f'No Views {len(views)}')  ;  return
        for i, v in enumerate(views):
            self.dumpView(v, f'[{i}] ')

    def dumpView(self, v, pfx=''):
        v.dumpCrs(f'V{pfx}{fmtXYWH(v.x, v.y, v.w, v.h)} ')
        self.dumpLbox(v.lbox, pfx)  ;  self.dumpRect(v.rect, pfx)

    def dumpLbox(self, l, pfx=''):
        self.log(f'L{pfx}{fmtXYWH(l.x, l.y, l.width, l.height)} cw={l.content_width} ch={l.content_height} cva={l.content_valign}')
        self.log(f'L{pfx}sel={l.selection_start}:{l.selection_end}')

    def dumpRect(self, r, pfx=''):
        self.log(f'R{pfx}{fmtXYWH(r.x, r.y, r.width, r.height)}')
    ####################################################################################################################################################################################################
    def resizeViews(self, views=None):
        views = views if views is not None else self.views
        if not views:  self.log(f'No Views {len(views)}')  ;  return
        for i, v in enumerate(views):
            self.resizeView(v)

    def resizeView(self, v):
        v.w = round(v.w * self.mx)  ;  v.h = round(v.h * self.my)
        self.resizeLbox(v.lbox)     ;  self.resizeRect(v.rect)

    def resizeLbox(self, l):
        l.width = round(l.width * self.mx)  ;  l.height = round(l.height * self.my)  ;  d = l.document
        fs = d.get_style('font_size', 0)    ;   fs *= self.my
        d.set_style(0, len(d.text), dict(font_size=fs))

    def resizeRect(self, r):   r.width *= self.mx  ;  r.height *= self.my
    ####################################################################################################################################################################################################
    def on_resize(self, width, height):
        self.dumpDataHorz()
        self.mx = width / self.w   ;  self.my = height / self.h
        self.log(f'BGN {self.fmtWxH()} {self.fmtDxD()} {self.fmtdl()} {self.fmtn()}')
        self.log(    f'{self.width=:4} {self.height=:4} {self.w=:4} {self.h=:4} {self.mx=:5.3f} {self.my=:5.3f}')
        self.w = width   ;   self.h = height
        super().on_resize(width, height)
        self.dumpViews()
        self.resizeViews()
        self.dumpViews()
        self.log(    f'{self.width=:4} {self.height=:4} {self.w=:4} {self.h=:4} {self.mx=:5.3f} {self.my=:5.3f}')
        self.log(f'END {self.fmtWxH()} {self.fmtDxD()} {self.fmtdl()} {self.fmtn()}')
    ####################################################################################################################################################################################################
    def initViews(self, dbg=1): # Bravura Text
        self.w, self.h = self.width, self.height   ;   txts = []
        x, y, w, h     = self.x, self.y, self.w, self.h
        np, nl, ns, nt = self.n
        for p in range(np):
            for l in range(nl):
                for s in range(ns):
                    t    = f'{self.data[p][l][s]}\n'
                    txts.append(t)
                    if dbg: self.log(f'{t}', pfx=0)
                v  = View(txts, x, y, w, h, ns, nt, self.batch, LOG_FILE)
                self.log(f'{fmtXYWH(v.x, v.y, v. w, v.h)}')
                self.views.append(v)
        if dbg: self.dumpViews()
    ####################################################################################################################################################################################################
    def regSnap(self, why, typ, dbg=1):
        self.snapWhy  = why
        self.snapType = typ
        self.snapReg  = 1
        if dbg: self.log(f'{self.snapWhy=} {self.snapType=} {self.snapReg=} {self.snapId=}')

    def snapshot(self, why='', typ='', dbg=0, dbg2=1):
        WHY       =  f'{why}' if why else self.snapWhy
        TYPE      = f'.{typ}' if typ else f'.{self.snapType}'
        SNAP_ID   = f'.{self.snapId}'
        LOG_ID    = f'.{self.LOG_ID}' if self.LOG_ID else ''
        if dbg:     self.log(f'{LOG_ID=} {TYPE=} {SNAP_ID=} {WHY}')
        if dbg:     self.log(f'{SNAP_DIR=} {BASE_NAME=} {SNAP_ID=} {SNAP_SFX=}')
        SNAP_NAME = BASE_NAME + LOG_ID + TYPE + SNAP_ID + SNAP_SFX
        SNAP_PATH = BASE_PATH / SNAP_DIR / SNAP_NAME
        if dbg:     self.log(f'{SNAP_PATH=}', pfx=0)
        pyglet.image.get_buffer_manager().get_color_buffer().save(f'{SNAP_PATH}')
        if dbg2:    self.log(f'{SNAP_NAME=} {WHY}', so=1)
        self.snapId += 1
    ####################################################################################################################################################################################################
    def deleteGlob(self, why, g):
        self.log(f'{why} deleting {len(g)} files from glob')
        for f in g:
            self.log(f'{f}')
            os.system(f'del {f}')

    def getFilePath(self, seq=0, fdir='files', fsfx='.txt'):
        if seq and not self.LOG_ID:
            fdir      += '/'
            self.log(f'{fdir=} {fsfx=}')
            pathlib.Path(fdir).mkdir(parents=True, exist_ok=True)
            fGlobArg   = str(BASE_PATH / fdir / BASE_NAME) + '.*' + fsfx
            fGlob      = glob.glob(fGlobArg)
            self.log(f'{fGlobArg=}')
            self.LOG_ID = 1 + self.getFileSeqNum(fGlob, fsfx)
            fsfx          = f'.{self.LOG_ID}{fsfx}'
            self.log(f'fGlob={util.fmtl(fGlob)}', pfx=0)
            self.log(f'{fsfx=}')
        return util.getFilePath(BASE_NAME, BASE_PATH, fdir=fdir, fsfx=fsfx)

    def getFileSeqNum(self, files, sfx, dbg=1, dbg2=1):
        i = -1
        if len(files):
            if dbg2: self.log(f'{sfx=} files={util.fmtl(files)}')
            ids =  [ self.sid(s, sfx) for s in files if s.endswith(sfx) ]
            if dbg:  self.log(f'ids={util.fmtl(ids)}')
            i = max(ids)
        return i
    @staticmethod
    def sid(s, sfx): s = s[:-len(sfx)]   ;   j = s.rfind('.')   ;   return int(s[j+1:])
    ####################################################################################################################################################################################################
    @staticmethod
    def log(msg='', pfx=1,  file=None, flush=False, sep=',', end='\n', so=0):
        file = LOG_FILE  if file is None else file    ;   util.slog(msg, pfx, file, flush, sep, end, so)

    def cleanupLog(self):
        self.log(f'{LOG_FILE.name}')   ;   self.log(f'{self.lfSeqPath}')
        self.log(f'Closing and Copying {LOG_FILE.name} to {self.lfSeqPath}')
        LOG_FILE.close()
        util.copyFile(LOG_PATH, self.lfSeqPath)

    def quit(self, why='', error=1, save=1, dbg=1):
        self.log(util.QUIT_BGN, pfx=0)
        self.log(f'Exit {why} {error=} {save=}')
        util.dumpStack(inspect.stack(), file=LOG_FILE)    ;   self.log(util.QUIT, pfx=0)
        util.dumpStack(util.MAX_STACK_FRAME, file=LOG_FILE)
        self.log(f'BGN {why} {error=} {save=}')           ;   self.log(util.QUIT, pfx=0)
        self.dumpArgs()
        if      save:         self.saveDataFile(why, self.dataPath1)
        if not error and dbg: self.log('Clean Run')
        self.snapshot(f'quit {error=} {save=}', 'QUIT')
        self.log(f'END {why} {error=} {save=}')
        self.log(util.QUIT_END, pfx=0)    ;    self.cleanupLog()
        print('Call pyglet.app.exit()')
        self.close()
        pyglet.app.exit()

########################################################################################################################################################################################################
class View(object): # self.document.set_paragraph_style(0, len(self.document.text), dict(align='center', wrap=True))
    def __init__(self, txts, x, y, w, h, ns, nt, b, file):
        self.file = file
        gA = pyglet.graphics.OrderedGroup(order=1)
        gB = pyglet.graphics.OrderedGroup(order=2)
        fn = 'Lucida Console'  ;  dpi = 96  ;  foo = fractions.Fraction(4, 3)
        fs = fsize(ns, nt, w, h, file=file, xx=1.33)
        rgb1 = [255, 200, 20, 255]   ;   rgb2 = [0, 0, 0]   ;   rgb3 = [200, 20, 220]
        self.x, self.y, self.w, self.h = x, y, w, h  ;  dx, dy = 2, 2  ;  dw, dh = 2*dx, 2*dy  ;  x2, y2, w2, h2 = x+dx, y+dy, w-dw, h-dh
        text = ''.join(txts)
        util.slog(f'{len(text)=}:', file=file)
        util.slog(f'{text}', pfx=0, file=file)
        self.doc        = pyglet.text.decode_text(text)
        self.doc.set_style(0, len(self.doc.text), dict(font_size=fs, font_name=fn, color=rgb1))
        self.rect       = pyglet.shapes.Rectangle(x2, y2, w2, h2, rgb2, batch=b, group=gA)
        self.lbox       = pyglbox(self.doc, w2, h2, multiline=True, dpi=dpi, batch=b, group=gB, wrap_lines=True)
        self.lbox.position = x2, y2
        self.caret      = pygcrt.Caret(self.lbox, color=rgb3)
        lc = self.lbox.get_line_count()
        util.slog(f'{ns=} {nt=} {lc=} {foo=}={foo.numerator/foo.denominator:6.4}', file=file)
#        for t in text:          util.slog(f'<{t}>', pfx=0, file=file)
        util.slog(f'{len(self.doc.text)=}:', file=file)
        util.slog(f'{self.doc.text}', pfx=0, file=file)
        self.setCrs(0, 0, dm=1)

    def setCrs(self, s, t, dm=None):
        self.dumpCrs(f'BGN {s=} {t=} {dm=}     ')
        self.caret.position = t   ;  self.caret.line = s  ;  dm = dm if dm is not None else 1  ;  self.caret.mark = self.caret.position + dm
        self.lbox.set_selection(self.caret.position, self.caret.mark)
        self.dumpCrs(f'END {s=} {t=} {dm=}     ')

    def fmtCrs(self, why=''): return f'{why}{self.caret.position:2}:{fmark(self.caret.mark)} {self.caret.line}'
#        o = f'{id(self.lbox):x} ' if dbg else ''    ;    return f'{why}{o}{self.caret.position:2}:{self.caret.mark:4} {self.caret.line}'
    def dumpCrs(self, why): Tabs.log(f'{self.fmtCrs(why)}', file=self.file)
    def hitTest(self, x, y):  r = self.lbox  ;  return 0 < x - r.x < r.width and 0 < y - r.y < r.height
########################################################################################################################################################################################################

if __name__ == '__main__':
    prevPath = util.getFilePath(BASE_NAME, BASE_PATH, fdir='logs', fsfx='.blog')
    LOG_PATH = util.getFilePath(BASE_NAME, BASE_PATH, fdir='logs', fsfx='.log')
    if LOG_PATH.exists(): util.copyFile(LOG_PATH, prevPath, LOG_FILE)
    with open(   str(LOG_PATH), 'w')   as   LOG_FILE:
        util.slog(f'{LOG_PATH=}',      file=LOG_FILE)
        util.slog(f'{LOG_FILE.name=}', file=LOG_FILE)
        Tabs()
        pyglet.app.run()
