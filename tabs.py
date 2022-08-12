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
HARROWS          = {-1:'LEFT', 1:'RIGHT'}
VARROWS          = {-1:'UP'  , 1:'DOWN' }
CSR_MODES        = ['MELODY', 'CHORD', 'ARPG']
MELODY, CHORD, ARPG   = 0, 1, 2
IMPLA           = 0

def fsize(c, s, w, h, file, xx=1.5, yy=1.):
    fsx = xx * w/c  ;  fsy = yy * h/s
    fs = round(fsx + fsy)
    fs2 = fs * 0.3  # 7/18) # 14/18*1/2
    util.slog(f'{c=} {s=} {w=} {h=} {fsx=:3.2f} {fsy=:3.2f} {fs=:3.2f} {fs2=:3.2f}', file=file)
    return fs2

def fmtXYWH(x, y, w, h):             return f'({x} {y} {w} {h})'

class Tabs(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        self.log(f'init {args=} {kwargs=}')
        self.data        = []
        self.views       = []
        self.batch       = pyglet.graphics.Batch()
        self.group       = pyglet.graphics.OrderedGroup(0)
        self.n           = [1, 1, 50, 6]
        self.snapWhy, self.snapType, self.snapReg, self.snapId = '?', '_', 0, 0
        self.LOG_ID      = 0
        self.lfSeqPath   = self.getFilePath(seq=1, fdir='logs', fsfx='.log')
        self.mx, self.my = 1, 1
        self.x,  self.y,  self.w,  self.h     = 0, 0, 0, 0
        self.symb,    self.mods,    self.motn = 0, 0, 0
        self.symbStr, self.modsStr, self.motnStr, self.kbkTxt = None, None, None, None
        self.hArrow, self.vArrow,  self.csrMode               = RIGHT, DOWN, MELODY    ;    self.dumpCursorArrows('init()')
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
        self.dmpBlnk()
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
#        self._initGroups()
        self.set_visible()
        self.log(f'get_size={self.fmtWxH(self.get_size())}')
        self.kbks = wink.KeyStateHandler()
        self.push_handlers(self.kbks)
        if self.EVENT_LOG: # and self.VERBOSE:
            self.eventLogger = wine.WindowEventLogger()
            self.push_handlers(self.eventLogger)
        if dbg: self.log(f'END {self.fmtWxH()}')
    ####################################################################################################################################################################################################
#    def _initGroups(self):    #     [P, L, C  T,  N, I, K, V   R, Q, H,  O, A, D]
#        self.g = []   ;   self.go = [1, 2, 3, 5,  5, 5, 5, 4,  5, 5, 6,  5, 5, 5]
#        self.log(f'gn={util.fmtl(self.go)}')
#        for i in range(1+max(self.go)):
#            p = None if self.ORDER_GROUP or i==0 else self.g[i-1]
#            self.g.append(self._initGroup(i, p))
#            self.log(f'({i}) g={self.g[i]} pg={self.g[i].parent}')
#    def _initGroup(self, order=0, parent=None): return pyglet.graphics.OrderedGroup(order, parent) if self.ORDER_GROUP else pyglet.graphics.Group(parent)
    ####################################################################################################################################################################################################
    def _initArgs(self):
        self.dfn         = 'test.0.dat'
        self.n           = [1, 1, 6, 50]
        self.v           = set() if 0 else {0}
        self.EVENT_LOG = 0  ;  self.FULL_SCREEN = 0  ;  self.GEN_DATA = 0  ;  self.ORDER_GROUP = 1  ;  self.SNAPS = 0  ;  self.VERBOSE = 0
        ARGS             = util.parseCmdLine(file=LOG_FILE)
        self.log(f'argMap={util.fmtm(ARGS)}')
        if 'a' in ARGS and len(ARGS['a']) == 0: global IMPLA ; IMPLA =  1
        if 'e' in ARGS and len(ARGS['e']) == 0: self.EVENT_LOG       =  1
        if 'f' in ARGS and len(ARGS['f']) >  0: self.dfn             = ARGS['f'][0]
        if 'F' in ARGS and len(ARGS['F']) == 0: self.FULL_SCREEN     =  1
        if 'G' in ARGS and len(ARGS['G']) == 0: self.GEN_DATA        =  1
        if 'g' in ARGS and len(ARGS['g']) == 0: self.ORDER_GROUP     =  0
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
    def fmtBlnk(self):                         return f'{self.blankCol=} {self.blankRow=}'
    def fmtblnk(self):                         return f'{len(self.blankCol)=} {len(self.blankRow)=}'
    def dmpBlnk(self):                         self.log(f'{self.fmtblnk()} {self.fmtBlnk()}')
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
        self.dmpBlnk()
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
                self.log(f'{util.fmtl(data[p][l], d1="")}', pfx=0)
            self.log(pfx=0)
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
        self.log(f'BGN {why} {self.csrMode=} = {CSR_MODES[self.csrMode]=}')
        self.csrMode  = (self.csrMode + 1) % len(CSR_MODES)
        self.log(f'END {why} {self.csrMode=} = {CSR_MODES[self.csrMode]=}')

    def toggleArrow(self, why, v, dbg=1):
        if dbg and     v: self.log(f'BGN {why} {v=} {self.vArrow=:2} = {VARROWS[self.vArrow]=}')
        if dbg and not v: self.log(f'BGN {why} {v=} {self.hArrow=:2} = {HARROWS[self.hArrow]=}')
        if v: self.vArrow *= -1
        else: self.hArrow *= -1
        if dbg and     v: self.log(f'BGN {why} {v=} {self.vArrow=:2} = {VARROWS[self.vArrow]=}')
        if dbg and not v: self.log(f'BGN {why} {v=} {self.hArrow=:2} = {HARROWS[self.hArrow]=}')
    ####################################################################################################################################################################################################
    def OLD_dumpCursorArrows(self, why):
        cm, ha, va = self.csrMode, self.hArrow, self.vArrow
        self.log(f'{why} csrMode={cm}={CSR_MODES[cm]:6} hArrow={ha}={HARROWS[ha]:5} vArrow={va}={VARROWS[va]:4}')
    def dumpCursorArrows(self, why): self.log(f'{why}')
    def reverseArrow(self, dbg=1):
        if dbg: self.dumpCursorArrows('reverseArrow()')
        if self.csrMode == MELODY or self.csrMode == ARPG: self.toggleArrow('reverseArrow() MELODY or ARPG', v=0)
        if self.csrMode == CHORD  or self.csrMode == ARPG: self.toggleArrow('reverseArrow() CHORD or ARPG',  v=1)
        if dbg: self.dumpCursorArrows('reverseArrow()')

    def setCHVMode(self, why, c=None, h=None, v=None):
        self.dumpCursorArrows(f'BGN {why} {c=} {h=} {v=}')
        if c is not None: self.csrMode = c
        if h is not None: self.hArrow  = h
        if v is not None: self.vArrow  = v
        self.dumpCursorArrows(f'END {why} {c=} {h=} {v=}')
    ####################################################################################################################################################################################################
    def fCrsCrt(self, dbg=0): return self.fmtCrs(dbg), self.fmtCrt(dbg)
    def fmtCrs( self, dbg=0): return self.getTabsView().fmtCrs(dbg=dbg)
    def fmtCrt( self, dbg=0): return self.fmtCrtA(dbg), self.fmtCrtB(dbg)
    def fmtCrtA(self, dbg=0): o = f'{id(self.focus.caret):x} '         if dbg else ''  ;  return f'{o}{self.focus.caret.position}:{self.focus.caret.mark}'
    def fmtCrtB(self, dbg=0): o = f'{id(self.getTabsView().caret):x} ' if dbg else ''  ;  return f'{o}{self.getTabsView().caret.position}:{self.getTabsView().caret.mark}'
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
#        if IMPLA: return 1 if self.sobj.isFret(text) or text in util.DSymb.SYMBS else 0
#        else:           return 1 if self.sobj.isFret(text) or text in util.DSymb.SYMBS or text == Z else 0
    ####################################################################################################################################################################################################
    def getTabsView(self): return self.views[0]
    def normCrt(self, caret):
        self.log(f'BGN line={caret.line} pos={caret.position}')
        line = caret.line
        pos  = caret.position
        mark = caret.mark
        while pos > self.n[T]:
            pos  -= line * self.n[T]
            mark -= line * self.n[T]
            line += 1
        caret.position = pos
        caret.mark = mark
        caret.line = line
        self.log(f'END line={caret.line} pos={caret.position}')

#        s = caret.line  ;  t = caret.position - s * self.dl()[T]  ;  return s, t
    def plst2cc(self, p, l, s, t): np, nl, ns, nt = self.dl()  ;  return p*np + l*nl + s*ns + t
    def plst(self, dbg=1):
        v = self.getTabsView()  ;  nt = self.dl()[T]
        s = v.caret.line  ;  t = v.caret.position % (nt + 1)
        msg = f'{s=} {t=} {v.caret.position} {nt}'
        self.log(f'{msg} {self.fCrsCrt()}') if dbg else None
        return 0, 0, s, t
    ####################################################################################################################################################################################################
    def kbkInfo(self, symb=None, mods=None, text=None, motn=None):
        p, l, s, t = self.plst()  ;  self.log(f'{s=} {t=}')
        msg = self.getTabsView().fmtCrs()  ;  kbks = self.kbks
        self.log(f'{msg} {util.fmtl([ f"{k:x}" for k in kbks if kbks[k] ])} : {util.fmtl([ wink.symbol_string(k) for k in kbks if kbks[k] ])}')
        if symb:  self.symb,   self.symbStr = symb, wink.symbol_string(symb)
        if mods:  self.mods,   self.modsStr = mods, wink.modifiers_string(mods)
        if motn:  self.motn,   self.motnStr = motn, wink.motion_string(motn)
        if text:               self.kbkTxt  = text
        return self.symbStr, self.modsStr #, self.motnStr
    ####################################################################################################################################################################################################
    def on_draw(self, dbg=1):
        pyglet.gl.glClearColor(1, 1, 1, 1)
        self.clear()
        self.batch.draw()
        if self.snapReg: self.snapReg = 0  ;  self.snapshot()  ;  self.log(f'{self.snapWhy=} {self.snapType=} {self.snapId=}') if dbg else None
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
    def on_key_press(self, symb, mods):
        symbStr, modsStr = self.kbkInfo(symb, mods)  ;  msg = f'{symb=} {symbStr=} {mods=} {modsStr=}'
        if   symb == wink.ESCAPE:              msg += ' Quit'     ;    self.log(msg)  ;  self.quit(msg, 0)
        elif symb == wink.S and self.isCtrl(): self.saveDataFile('@S', self.dataPath1)
        elif symb == wink.INSERT:              msg += 'INSERT'    ;    self.log(msg)
        elif symb == wink.TAB:
            if   self.isShift():               direction = -1
            else:                              direction = 1
            if   self.focus in self.views:     i = self.views.index(self.focus)
            else:                              direction = 0      ;    i = 0
            self.setFocus(self.views[(i + direction) % len(self.views)])

    def on_key_release(self, symb, mods, dbg=1):
        self.kbkInfo(symb, mods)
    ####################################################################################################################################################################################################
    def on_text_motion(self, m, dbg=1):
        self.kbkInfo(motn=m)  ;  t = f'{m:x}'
        self.log(f'BGN {t} {self.fCrsCrt()}')
        if self.focus:
            self.log(f'otm<{t}> {self.fCrsCrt()}')
            self.focus.caret.on_text_motion(m) # ;  self.autoMove(msg)
            self.log(f'otm<{t}> {self.fCrsCrt()}')
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
#            if   m == wink.MOTION_PREVIOUS_WORD:     msg = f'MOTION_PREVIOUS_WORD {t}'  ;   self.log(msg) #  ;   self.quit(msg)
#            elif m == wink.MOTION_NEXT_WORD:         msg = f'MOTION_NEXT_WORD {t}'      ;   self.log(msg) #  ;   self.quit(msg)
            else:                                    msg =    f'??? {t}'   ;   self.log(msg) #  ;   self.quit(msg)
        else:                                        msg =    f'??? {t}'   ;   self.log(msg) #  ;   self.quit(msg)
        if self.SNAPS: self.regSnap(msg, 'OTM')
        if self.focus: self.log(f'END {t} {self.fCrsCrt()}')
    ####################################################################################################################################################################################################
    def on_text_motion_select(self, ms, dbg=1):
        self.kbkInfo(motn=ms)
        if self.focus: self.log(f'BGN fc={self.fCrsCrt()} {ms=:x}') # ;  self.focus.caret.on_text_motion_select(ms)
        if   ms == wink.MOTION_UP:                msg = f'UP    {ms:x}'  ;  self.move(msg, ms)
        elif ms == wink.MOTION_DOWN:              msg = f'DOWN  {ms:x}'  ;  self.move(msg, ms)
        elif ms == wink.MOTION_LEFT:              msg = f'LEFT  {ms:x}'  ;  self.move(msg, ms)
        elif ms == wink.MOTION_RIGHT:             msg = f'RIGHT {ms:x}'  ;  self.move(msg, ms)
        else:                                     msg = f'???   {ms:x}'  ;  self.log( msg)
        if self.focus: self.log(f'END fc={self.fCrsCrt()} {ms=:x}')  ;  self.focus.caret.on_text_motion_select(ms)
        self.quit(f'ERROR UNHANDLED {msg}')
    ####################################################################################################################################################################################################
    def on_text(self, s, dbg=1):
        self.kbkInfo(text=s)  ;  t = f'<{s}>'
        if   self.focus:    self.log(f'BGN {t} {self.fCrsCrt()}')
        if self.isShift():
            if   s == '$':  msg = f'^${t} snapshot'            ;   self.log(msg, so=1)  ;  self.snapshot(     msg, 'SNP')
            elif s == 'S':  msg = f'^S{t} saveDataFile'        ;   self.log(msg, so=1)  ;  self.saveDataFile( msg, self.dataPath1)
            elif s == 'T':  msg = f'^T{t} toggleCsrMode'       ;   self.log(msg, so=1)  ;  self.toggleCsrMode(msg)
            elif s == 'V':  msg = f'^V{t} toggleArrow(1)'      ;   self.log(msg, so=1)  ;  self.toggleArrow(  msg, v=1)
        elif self.isTab(s): msg =   f'{t} setTab'              ;   self.log(msg, so=1)  ;  self.setTab(       msg, s)
#        elif self.isTab(s):                                                                  self.setTab(f'<{t}>', t)
#        elif IMPLA and t == Z: msg = f'<{t}> fcTextMotn'   ;   self.log(msg, so=1)  ;  self.fcTextMotn(   msg)
        elif s == 'v':      msg = f'v{t} toggleArrow(0)'       ;   self.log(msg, so=1)  ;  self.toggleArrow(  msg, v=0)
        if   self.focus:    self.log(f'END {t} {self.fCrsCrt()}')
    ####################################################################################################################################################################################################
    def setFocus(self, focus, dbg=0):
        if dbg: self.log(f'BGN {id(focus)=} {id(self.focus)=}')
        if focus is self.focus:        self.log(f'{id(focus)=} is {id(self.focus)=}') if dbg else None  ;  return
        if self.focus:
            self.focus.caret.visible = False
            self.focus.caret.mark    = self.focus.caret.position = 0
            self.log(f'{self.focus.caret.visible=} {self.focus.caret.position=} {self.focus.caret.mark=}')
        self.focus = focus
        if self.focus:                 self.focus.caret.visible = True  ;  self.log(f'{self.focus.caret.visible=}') if dbg else None
        if dbg: self.log(f'END {id(focus)=} {id(self.focus)=}')
    ####################################################################################################################################################################################################
    def fcTextMotn(self, msg, dbg=1):
        m = self.getTextMotn(msg)  ;  msg2 = f'on_text_motion<{m:x}>'  ;  msg3 = 'autoMove'
        self.log(f'Before {msg2} {self.fCrsCrt()}')
        self.focus.caret.on_text_motion(m)
        self.log(f'After {msg2} Before {msg3} {self.fCrsCrt()}')
        self.move(msg, m)
#        self.autoMove(msg)
        self.log(f'After  {msg3} {self.fCrsCrt()}')
        if dbg: self.regSnap(msg, 'SPC')

    def getTextMotn(self, msg):
        m = None  ;  msg += f'{self.csrMode=} {self.hArrow=} {self.vArrow=}'
        if   self.csrMode == MELODY and self.hArrow == RIGHT: m = wink.MOTION_RIGHT
        elif self.csrMode == MELODY and self.hArrow == LEFT:  m = wink.MOTION_LEFT
        elif self.csrMode == CHORD  and self.vArrow == DOWN:  m = wink.MOTION_DOWN
        elif self.csrMode == CHORD  and self.vArrow == UP:    m = wink.MOTION_UP
        elif self.csrMode == ARPG   and self.hArrow == RIGHT: m = wink.MOTION_RIGHT
        else: msg = f'ERROR {msg} {m=:x}'  ;  self.log(msg)  ;  self.quit(msg)
        self.log(f'{msg} return {m=:x}')
        return m
    ####################################################################################################################################################################################################
    def OLD__autoMove(self, why):  # FIX ME
        self.log(f'BGN {why}')
        #        va = 1 if self.vArrow else -1
        #        ha = 1 if self.hArrow else -1
        nt, it = self.n[T], 6  # self.i[T]
        mmDist = wink.MOTION_RIGHT if self.hArrow else wink.MOTION_LEFT  # ha * nt
        cmDist = wink.MOTION_UP if self.vArrow else wink.MOTION_DOWN  # va
        amDist = mmDist + cmDist
        self.dumpCursorArrows(f'{why} M={mmDist} C={cmDist} A={amDist}')
        if self.csrMode == MELODY:                                     self.move(why, mmDist)
        elif self.csrMode == CHORD:
            if it == 1 and self.vArrow == UP and self.hArrow == RIGHT: self.move(why, nt * 2 - 1)
            elif it == 6 and self.vArrow == DOWN and self.hArrow == RIGHT: self.move(why, -(nt * 2 - 1))
            else:                                                           self.move(why, cmDist)
        elif self.csrMode == ARPG:                                       self.move(why, amDist)
        self.log(f'END {why}')
    def autoMove_2(self, why):
        self.log(f'BGN {why} {self.fCrsCrt()}')
#        nt, it = self.n[T], 3 # self.i[T]
        mmDir = wink.MOTION_RIGHT if self.hArrow else wink.MOTION_LEFT
        cmDir = wink.MOTION_DOWN  if self.vArrow else wink.MOTION_UP
#        amDir = mmDir + cmDir
#        self.dumpCursorArrows(f'{why} M={mmDir:x} C={cmDir:x}') # A={amDist:x}')
        if   self.csrMode == MELODY:  self.move(why, mmDir)
        elif self.csrMode == CHORD:   self.move(why, cmDir)
#            if   it == 1 and self.vArrow  == UP   and self.hArrow == RIGHT: self.move(why, mmDir)
#            elif it == 6 and self.vArrow  == DOWN and self.hArrow == RIGHT: self.move(why, mmDir)
#            else:                                                           self.move(why, cmDir)
#        elif    self.csrMode == ARPG:                                       self.move(why, amDir)
        self.log(f'END {why} {self.fCrsCrt()}')
    ####################################################################################################################################################################################################
    def move(self, why, m, dbg=1):
        if dbg: self.log(f'BGN {why} {m:x} {self.fCrsCrt()}')
        for i, v in enumerate(self.views):
            s, t = v.caret.line, v.caret.position
            dm   = v.caret.mark - v.caret.position if v.caret.mark is not None else 1
            if dbg: self.log(f'v[{i}] {s=} {t=} {dm=} before {m=:x} {self.fCrsCrt()}')
#            s += self.vArrow if self.csrMode == CHORD  else 0
#            t += self.hArrow if self.csrMode == MELODY else 0
            v.setCrs(s, t, dm)
            if dbg: v.dumpCrs(f'v[{i}] {s=} {t=} {dm=} after  {m=:x} {self.fCrsCrt()}')
        if dbg: self.log(f'END {why} {m:x} {self.fCrsCrt()}')
    ####################################################################################################################################################################################################
    def setTab(self, why, text, dbg=1): # if isDataFret or isTextFret else 0)
        msg = f'{why} <{text}>'  ;     self.log(f'BGN {msg} {self.fCrsCrt()}')
        if text == Z: self.fcTextMotn(msg)  ;  return  # if not IMPLA and text == Z
        p, l, s, t  = self.plst()        ;    data = self.data[p][l][s][t]   ;   cc = self.plst2cc(p, l, s, t)
        if dbg: self.log(f'Before {msg} <{data}> {cc=} plst={p} {l} {s} {t}')
        self.setDTNIK(text, cc, p, l, s, t, kk=1)
        p, l, s, t  = self.plst()        ;    data = self.data[p][l][s][t]
        if dbg: self.log(f'After {msg} <{data}> {cc=} plst={p} {l} {s} {t}')
        if self.focus:
            self.log(f'Before on_text<{text}> {self.fCrsCrt()}')
            self.focus.caret.on_text(text)
            self.log(f'After  on_text<{text}> {self.fCrsCrt()}')
            if   self.csrMode == CHORD:  s += self.vArrow
            elif self.csrMode == MELODY: t += 1
            self.getTabsView().setCrs(s, t, 1)
        TYP = f'TXT_{text}' if self.sobj.isFret(text) else 'SMB' if text in util.DSymb.SYMBS  else 'UNK'
        if self.SNAPS: self.regSnap(f'{msg}', TYP)
        self.log(f'END {msg} {self.fCrsCrt()}')
#        self.resyncData = 1
    ####################################################################################################################################################################################################
    def setDTNIK(self, text, cc, p, l, s, t, kk=0, dbg=1):
        if dbg: self.log(f'{cc=} {kk=}    {text=}')
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
        if dbg: self.log(f'{t=} {text=} {data=}')

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
#        self.log(f'V{pfx}{fmtXYWH(v.x, v.y, v.w, v.h)})')
        v.dumpCrs(f'V{pfx}{fmtXYWH(v.x, v.y, v.w, v.h)}) ')
#        self.log(f'V{pfx}{v.caret.line=} {v.caret.position=} {v.caret.mark=} {v.lbox.selection_start=} {v.lbox.selection_end=}', pfx=0)
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

    def resizeRect(self, r):   r.width *= self.mx          ;  r.height *= self.my
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
        self.w, self.h = self.width, self.height   ;   text = ''
        x, y, w, h     = self.x, self.y, self.w, self.h
        np, nl, nc, nt     = self.n
        for p in range(np):
            for l in range(nl):
                tx = ''
                for c in range(nc):
                    txt    = f'{self.data[p][l][c]}'
                    text  += f'{tx}{txt}\n'
                v  = View(text, x, y, w, h, nt, nc, self.batch, LOG_FILE)
                self.log(f'{fmtXYWH(v.x, v.y, v. w, v.h)}')
                self.views.append(v)
        if dbg: self.dumpViews()
    ####################################################################################################################################################################################################
    def regSnap(self, why, typ, dbg=1):
        self.snapWhy = why
        self.snapType = typ
        self.snapReg = 1
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
        self.log(f'Exit {why} {error=} {save=}')
        util.dumpStack(inspect.stack(), file=LOG_FILE)    ;   self.log(util.QUIT_BGN, pfx=0)
        util.dumpStack(util.MAX_STACK_FRAME, file=LOG_FILE)
        self.log(f'BGN {why} {error=} {save=}')           ;   self.log(util.QUIT,     pfx=0)
        self.dumpArgs()
        if      save:  self.saveDataFile(why, self.dataPath1)
        if not error and dbg: self.log('Clean Run')
        self.snapshot(f'quit {error=} {save=}', 'QUIT')
        self.log(f'END {why} {error=} {save=}')           ;   self.log(util.QUIT_END, pfx=0)
        self.cleanupLog()
        pyglet.app.exit()

########################################################################################################################################################################################################
class View(object): # self.document.set_paragraph_style(0, len(self.document.text), dict(align='center', wrap=True))
    def __init__(self, text, x, y, w, h, c, s, b, file):
        self.file = file
        gA = pyglet.graphics.OrderedGroup(order=1)
        gB = pyglet.graphics.OrderedGroup(order=2)
        fn = 'Lucida Console'  ;  dpi = 96  ;  foo = fractions.Fraction(4, 3)
        fs = fsize(c, s, w, h, file=file, xx=1.33)
        rgb1 = [255, 200, 20, 255]   ;   rgb2 = [0, 0, 0]   ;   rgb3 = [200, 20, 220]
        self.x, self.y, self.w, self.h = x, y, w, h  ;  dx, dy = 2, 2  ;  dw, dh = 2*dx, 2*dy  ;  x2, y2, w2, h2 = x+dx, y+dy, w-dw, h-dh
        self.doc        = pyglet.text.decode_text(text)     ;   util.slog(f'{text=}', file=file, pfx=0)
        self.doc.set_style(0, len(self.doc.text), dict(font_size=fs, font_name=fn, color=rgb1))
        self.rect       = pyglet.shapes.Rectangle(x2, y2, w2, h2, rgb2, batch=b, group=gA)
        self.lbox       = pyglbox(self.doc, w2, h2, multiline=True, dpi=dpi, batch=b, group=gB, wrap_lines=True)
        self.lbox.position = x2, y2
        self.caret      = pygcrt.Caret(self.lbox, color=rgb3)
        util.slog(f'{c=} {s=} {foo=}', file=file)
#        self.setCrs(2, 0)
        self.setCrs(2, 0, 1)

    def setCrs(self, s, t, dm=None):
        self.dumpCrs(f'BGN {s=} {t=} {dm=}     ')
        self.caret.position = t   ;  self.caret.line = s  ;  dm = dm if dm is not None else 1  ;  self.caret.mark = self.caret.position + dm
        self.lbox.set_selection(self.caret.position, self.caret.mark) # if dm is not None else self.caret.position
#        self.lbox.set_selection(t, t + dm)  ;  self.caret.position = t  ;  self.caret.mark = t + dm  ;  self.caret.line = s
        self.dumpCrs(f'END {s=} {t=} {dm=}     ')

    def dumpCrs(self, why, dbg=0): util.slog(f'{self.fmtCrs(why, dbg)}', file=self.file)

    def fmtCrs(self, why='', dbg=0):
        o = f'{id(self.lbox):x} ' if dbg else ''  ;  o2 = f' {id(self.caret):x}' if dbg else ''
        return f'{why}{o}sel={self.lbox.selection_start}:{self.lbox.selection_end} crt={self.caret.line} {self.caret.position}:{self.caret.mark}{o2}'

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
