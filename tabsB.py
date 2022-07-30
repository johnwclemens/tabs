import fractions
import os, sys, glob, inspect, pathlib, itertools # os
import pyglet
import pyglet.window.event as pygwine
import pyglet.window.key as pygwink
import pyglet.text.caret as pygcrt
from  pyglet.text.layout import IncrementalTextLayout as pyglbox
#import pyglet.text.layout as pyglbox
#sys.path.insert(0, os.path.abspath("./lib"))
#print(f'{len(sys.path)=}')
#for _ in sys.path:
#    print(f'{_}')
import util

Z                = ' '
PATH             = pathlib.Path.cwd() / sys.argv[0]
BASE_PATH        = PATH.parent
BASE_NAME        = BASE_PATH.stem
SNAP_DIR         = 'snaps'
SNAP_SFX         = '.png'
LOG_FILE         = None
FDL              = ' len(data 0 00 000)'
FDT              = 'type(data 0 00 000)'
#P, L, C, T       =  0,  1,  2,  3
#N, I, K          =  4,  5,  6
#R, Q, H, V       =  7,  8,  9, 10
#O, A, D          = 11, 12, 13
P, L, C, T       =  0,  1,  2,  3
N, I, K, V       =  4,  5,  6,  7
R, Q, H          =  8,  9, 10
O, A, D          = 11, 12, 13
#P, L, S, C       =  0,  1,  2,  3
#T, N, I, K       =  4,  5,  6,  7
#R, Q, H, V       =  8,  9, 10, 11
#O, A, D          = 12, 13, 14
JTEXTS           = ['Page',  'Line',  'Sect',  'Col',  'Tab',  'Note',  'IKey',  'Kord',  '_LLR',  '_LLC', 'Curs', 'View',  '_SNo',  '_SNm',  '_Cpo', '_TNIK']
JFMT             = [   1,       2,       2,       3,      4,      4,       4,       4,       2,       3,       1,       1,      2,      2,      3,       4]
CSR_MODES        = ['MELODY', 'CHORD', 'ARPG']
HARROWS, VARROWS = ['LEFT', 'RIGHT'], ['UP', 'DOWN']
MELODY, CHORD, ARPG   = 0, 1, 2
LEFT, RIGHT, UP, DOWN = 0, 1, 0, 1

def fsize(c, s, w, h, file, xx=1.5, yy=1.):
    fsx = xx * w/c  ;  fsy = yy * h/s
    fs = round((fsx + fsy) * 7/18) # 14/18*1/2
    util.slog(f'{c=} {s=} {w=} {h=} {fsx=:3.2f} {fsy=:3.2f} {fs=:3.2f}', file=file)
    return fs

def fmtXYWH(x, y, w, h):             return f'({x} {y} {w} {h})'

class Tabs(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        util.slog(f'init {args=} {kwargs=}')
        self.data        = []
        self.views       = []
        self.batch       = pyglet.graphics.Batch()
        self.group       = pyglet.graphics.OrderedGroup(0)
        self.n           = [1, 1, 50, 6]
        self.ssi         = 0
        self.lfSeqNum    = 0
        self.lfSeqPath   = self.getFilePath(seq=1, fdir='logs', fsfx='.log')
        self.mx, self.my = 1, 1
        self.x,  self.y,  self.w,  self.h     = 0, 0, 0, 0
        self.symb,    self.mods,    self.motn = 0, 0, 0
        self.symbStr, self.modsStr, self.motnStr, self.kbkTxt = None, None, None, None
        self.hArrow, self.vArrow,  self.csrMode               = RIGHT, DOWN, MELODY    ;    self.dumpCursorArrows('init()')
        self._initArgs()
        self._initWindowA()
        super().__init__(screen=self.screens[self.fsi], fullscreen=self.FULL_SCREEN, resizable=True, visible=False)
        self._initWindowB()
#        self.n.insert(S, self.ssl())
        self.tblanki, self.tblanks  = 0, [' ', '-']
        self.tblank      = self.tblanks[self.tblanki]
        self.tblankCol   = self.tblank * self.n[T]
        self.tblankRow   = self.tblank * self.n[C]
        self.dumpBlank()
        self.initData()
        self.initViews()
        self.text_cursor = self.get_system_mouse_cursor('text')
        self.focus       = None
        self.set_focus(self.views[0])
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
        if self.EVENT_LOG: # and self.VERBOSE:
            self.eventLogger = pygwine.WindowEventLogger()
            self.push_handlers(self.eventLogger)
            self.kbks = pygwink.KeyStateHandler()
            self.push_handlers(self.kbks)
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
        self.dfn         = 'test.7.dat'
        self.n           = [1, 1, 50, 6]
        self.SS          = set() if 0 else {0}
        self.FULL_SCREEN = 0   ;   self.EVENT_LOG = 0   ;   self.ORDER_GROUP = 1   ;   self.VERBOSE = 0
        ARGS             = util.parseCmdLine(file=LOG_FILE)
        self.log(f'argMap={util.fmtm(ARGS)}')
        if 'e' in ARGS and len(ARGS['e']) == 0: self.EVENT_LOG     =  1
        if 'f' in ARGS and len(ARGS['f']) >  0: self.dfn = ARGS['f'][0]
        if 'g' in ARGS and len(ARGS['g']) == 0: self.ORDER_GROUP   =  0
        if 'n' in ARGS and len(ARGS['n']) >  0: self.n = [int(ARGS['n'][i]) for i in range(len(ARGS['n']))]
        if 'F' in ARGS and len(ARGS['F']) == 0: self.FULL_SCREEN   =  1
        if 'S' in ARGS and len(ARGS['S']) >= 0: self.SS = {int(ARGS['S'][i]) for i in range(len(ARGS['S']))}
        if 'v' in ARGS and len(ARGS['v']) == 0: self.VERBOSE       =  1
        self.dumpArgs()
    ####################################################################################################################################################################################################
    def dumpArgs(self):
        self.log(f'[e]   {self.EVENT_LOG=}')
        self.log(f'[f]         {self.dfn=}')
        self.log(f'[F] {self.FULL_SCREEN=}')
        self.log(f'[g] {self.ORDER_GROUP=}')
        self.log(f'[n]            {self.fmtn()}')
        self.log(f'[S]          .SS={util.fmtl(self.SS)}')
        self.log(f'[v]     {self.VERBOSE=}')

    def initData(self):
        self._initDataPath()
        self.readDataFile(self.dataPath1)
        util.copyFile    (self.dataPath1, self.dataPath2)
#        self.data       = self.transposeData(dump=1)

    def fmtDxD( self, data=None,      d='x'):  l = list(map(str, self.dl(data)))       ;    return f'({d.join(l)})'
    def fmtXdY( self, x=None, y=None, d=','):  x = x if x is not None else self.x      ;  y = y if y is not None else self.y       ;  return f'({x:4}{d}{y:4})'
    def fmtWxH( self, w=None, h=None, d='x'):  w = w if w is not None else self.width  ;  h = h if h is not None else self.height  ;  return f'({w}{d}{h})'
    def ssl(self, dbg=0): l = len(self.SS)  ;  self.log(f'{self.fmtn()} SS={util.fmtl(self.ss2sl())} l={l}') if dbg else None      ;  return l
    def fmtBlnk(self):                         return f'{self.tblankCol=} {self.tblankRow=}'
    def fmtblnk(self):                         return f'{len(self.tblankCol)=} {len(self.tblankRow)=}'
    def dumpBlank(self): self.log(f'{self.fmtblnk()} {self.fmtBlnk()}')
    def fmtn(self, pfx='n=', n=None):          n = n if n is not None else self.n    ;    return f'{pfx}{util.fmtl(n)}'
    def dl(  self, data=None, p=0, l=0, c=0):  return list(map(len,                       self.dplc(data, p, l, c)))
    def dt(  self, data=None, p=0, l=0, c=0):  return list(map(type,                      self.dplc(data, p, l, c)))
    def dtA( self, data=None, p=0, l=0, c=0):  return [ str(type(a)).strip('<>') for a in self.dplc(data, p, l, c) ]
    def dproxy(self, data):                    return data if data is not None else self.data
    def dplc(  self, data=None, p=0, l=0, c=0):
        data = self.dproxy(data)
        if p >= len(data):           msg = f'ERROR BAD p index {p=} {l=} {c=} {len(data)=}'        ;  self.log(msg)  ;  raise SystemExit(msg)
        if l >= len(data[p]):        msg = f'ERROR BAD l index {p=} {l=} {c=} {len(data[p])=}'     ;  self.log(msg)  ;  raise SystemExit(msg)
        if c >= len(data[p][l]):     msg = f'ERROR BAD c index {p=} {l=} {c=} {len(data[p][l])=}'  ;  self.log(msg)  ;  raise SystemExit(msg)
        return data, data[p], data[p][l], data[p][l][c]
    ####################################################################################################################################################################################################
    def fmtdl( self, data=None, fdl=0):       txt = FDL if fdl else ''  ;  return f'{txt}{util.fmtl(self.dl(data))}'
    def fmtdt( self, data=None, fdt=0):       txt = FDT if fdt else ''  ;  return txt + f"[{' '.join([ t.replace('class ', '') for t in self.dtA(data) ])}]"
    ####################################################################################################################################################################################################
    def _initDataPath(self):
        dataDir   = 'data'  ;  dataSfx = '.dat'  ;  dataPfx = f'.{self.n[T]}'
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
                    if dbg: self.log(f'writing {l+1}{util.ordSfx(l+1)} line', pfx=0)  # if dbg  else  self.log(pfx=0)  if  l  else  None
                    for r in range(len(data[p][l])):
                        text = ''
                        for c in range(len(data[p][l][r])):
                            text += data[p][l][r][c]
                        if dbg: self.log(f'writing {r+1}{util.ordSfx(r+1)} string {text}', pfx=0)  # if dbg  else  self.log(text, pfx=0)
                        DATA_FILE.write(f'{text}\n')
                    DATA_FILE.write('\n')  #   if l < nl:
        size = path.stat().st_size   ;   self.log(f'{self.fmtn()} {self.fmtdl()} {size=}')
        return size
    ####################################################################################################################################################################################################
    def genDataFile(self, path):
        self.log(f'{path} {self.fmtn()}')
        np, nl, nc, nr = self.n
        self.dumpBlank()
        self.data = [ [ [ self.tblankRow for _ in range(nr) ] for _ in range(nl) ] for _ in range(np) ]
        size = self.saveDataFile('Generated Data', path)
        self.log(f'{path} {size=} {len(self.data)=}')
        self.data = []
        return size
    ####################################################################################################################################################################################################
    def readDataFile(self, path, dbg=1):
        nl = self.n[L]   ;   nr = self.n[T]   ;   sp, sl, st, sr = 0, 0, 0, 0
        if dbg:                             self.log(f'BGN {self.fmtn()}')
        if not path.exists():
            self.log(f'WARN No Data File Exists @ {path} -> Touch Data File')   ;   path.touch()
        stat = path.stat()  ;     size = stat.st_size
        if size == 0:
            self.log(f'WARN Zero Len Data File @ {path} -> Generate Data File')   ;   size = self.genDataFile(path)
        if size == 0:
            msg = f'ERROR Zero Len Data File {size=}'   ;   self.log(msg)   ;   self.quit(msg)
        with open(path, 'r') as DATA_FILE:
            DATA_FILE.seek(0, 2)      ;     size = DATA_FILE.tell()   ;   DATA_FILE.seek(0, 0)
            self.log(f'{DATA_FILE.name:40} {size:3,} bytes = {size/1024:3,.1f} KB')
            self.log('Raw Data File BGN:')
            data = self.data          ;     lines, rows = [], []      ;   ntabs = 0
            for tabs in DATA_FILE:
                tabs = tabs.strip()
                if tabs:
                    if not ntabs: ntabs = len(tabs)
                    if len(tabs) != ntabs:      msg = f'ERROR BAD tabs len {len(tabs)=} != {ntabs=}'   ;   self.log(msg)   ;   self.quit(msg)
                    rows.append(tabs)       ;   st += len(tabs)       ;     sr += 1
                else:
                    if rows  and not (sr % nr): lines.append(rows)    ;    rows = []   ;   sl += 1
                    if lines and not (sl % nl): data.append(lines)    ;   lines = []   ;   sp += 1
                self.log(f'{tabs}', pfx=0)
            if rows:  lines.append(rows)    ;   sl += 1
            if lines: data.append(lines)    ;   sp += 1
            self.log('Raw Data File END:')
            self.log(f'{self.fmtdl()=} {self.fmtdt()=}')
            self.assertDataFileSize(sl, size)
            npages, nlines, nrows, ntabs = self.dl()
            self.log(f'{sp    } ({sl/nlines:6.3f}) pages = {sl} lines =          {sr} rows =          {st} tabs')
            self.log(f'{npages} ({sl/nlines:6.3f}) pages @  {nlines} lines per page, @ {nrows} rows per line, @ {ntabs} tabs per row')
            self.dumpDataFile(data)
    ####################################################################################################################################################################################################
    def assertDataFileSize(self, nlines, ref):
        self.n =  self.dl()          ;  crlf = 2
        np, nl, nr, nt = self.n
        dsize = nlines * nr * nt            ;  self.log(f'{dsize=:3,} = {nlines=:3,} *     {nr=:2} *   {nt=}')
        crlfs = nlines * (nr + 1) * crlf    ;  self.log(f'{crlfs=:3,} = {nlines=:3,} * {(nr+1)=:2} * {crlf=}')
        size  =  dsize + crlfs              ;  self.log(f' {size=:3,} =  {dsize=:3,} +  {crlfs=:3,}   {ref=}')
        assert size == ref, f'{size=:4,} == {ref=:4,}'

    def dumpDataFile(self, data=None):
        data = self.dproxy(data)
        d0, d1, d2, d3 = self.dl()
        self.log(f'BGN {d0} pages, {d1} lines per page, {d2} rows per line, {d3} tabs per line')
        for n0 in range(len(data)):
            for n1 in range(len(data[n0])):
                self.log(f'{util.fmtl(data[n0][n1], d1="")}', pfx=0)
            self.log(pfx=0)
        self.log(f'END {d0} pages, {d1} lines per page, {d2} rows per line, {d3} tabs per line')
    ####################################################################################################################################################################################################
    def isVert(self, data=None, dbg=1):
        dl, dt = self.dl(data), self.dt(data)
        if dbg: self.log(f'BGN {self.fmtdl()=} {self.fmtdt()=}')
        assert dt[0] is list and dt[1] is list and dt[2] is list and dt[3] is str, f'{dl=} {dt=}'
        vert = 1 if dl[2] > dl[3] else 0
        self.checkData(vert=vert, data=None)
        self.log(f'{util.fmtl(self.dplc()[0])}', pfx=0)
        if dbg: self.log(f'END {self.fmtdl()=} {self.fmtdt()=} {vert=}')
        return vert

    def checkData(self, vert, data=None):
        data = self.dproxy(data)   ;   dl = self.dl(data)
        for p in range(dl[0]):
            assert len(data[p]) == dl[1], f'{len(data[p])=} {dl=} {vert=}'
            for l in range(len(data[p])):
                assert len(data[p][l]) == dl[2], f'{len(data[p][l])=} {dl=} {vert=}'
                for c in range(len(data[p][l])):
                    assert len(data[p][l][c]) == dl[3], f'{len(data[p][l])=} {dl=} {vert=}'
    ####################################################################################################################################################################################################
    def transposeData(self, data=None, dump=0, dbg=1):
        data = self.dproxy(data)
        self.log(f'BGN {self.fmtDxD(data)} {dump=}')
        if dump:        self.dumpDataVert( data) if self.isVert( data) else self.dumpDataHorz( data)
        Xdata, msg1, msg2 = [], [], []
        self.log(f'{self.fmtdl()} {self.fmtdt()}')
        self.log(f'dl={self.fmtdl(data)} dt={self.fmtdt(data)}') if dbg else None
        for p, page in enumerate(data):
            Xpage = []
            for l, line in enumerate(page):
                if dbg: msg1.append(f'{util.fmtl(line, d1="")}')
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
    def toggleBlank(self, how):
        prevBlank    =  self.tblank
        self.log(f'BGN {how} {prevBlank=}')
        self.tblanki = (self.tblanki + 1) % len(self.tblanks)
        self.tblank  =  self.tblanks[self.tblanki]
#        self.swapSrc, self.swapTrg, self.swapping = prevBlank, self.tblank, 2
#        self.swapTab(how, '\r')
        self.log(f'END {how} {self.tblank=}')

    def toggleCursorMode(self, how):
        self.log(f'BGN {how} {self.csrMode=} = {CSR_MODES[self.csrMode]=}')
        self.csrMode  = (self.csrMode + 1) % len(CSR_MODES)
        self.log(f'END {how} {self.csrMode=} = {CSR_MODES[self.csrMode]=}')

    def toggleArrow(self, how, v=0, dbg=0):
        if dbg: self.log(f'BGN {how} {v=} {self.hArrow=} = {HARROWS[self.hArrow]=} {self.vArrow=} = {VARROWS[self.vArrow]=}')
        if v: self.vArrow  = (self.vArrow + 1) % len(VARROWS)
        else: self.hArrow  = (self.hArrow + 1) % len(HARROWS)
        if dbg: self.log(f'END {how} {v=} {self.hArrow=} = {HARROWS[self.hArrow]=} {self.vArrow=} = {VARROWS[self.vArrow]=}')
    ####################################################################################################################################################################################################
    def dumpCursorArrows(self, how): cm, ha, va = self.csrMode, self.hArrow, self.vArrow  ;  self.log(f'{how} csrMode={cm}={CSR_MODES[cm]:6} hArrow={ha}={HARROWS[ha]:5} vArrow={va}={VARROWS[va]:4}')
    def reverseArrow(self, dbg=1):
        if dbg: self.dumpCursorArrows('reverseArrow()')
        if self.csrMode == MELODY or self.csrMode == ARPG: self.toggleArrow('reverseArrow() MELODY or ARPG', v=0)
        if self.csrMode == CHORD  or self.csrMode == ARPG: self.toggleArrow('reverseArrow() CHORD or ARPG',  v=1)
        if dbg: self.dumpCursorArrows('reverseArrow()')

    def setCHVMode(self, how, c=None, h=None, v=None):
        self.dumpCursorArrows(f'BGN {how} {c=} {h=} {v=}')
        if c is not None: self.csrMode = c
        if h is not None: self.hArrow  = h
        if v is not None: self.vArrow  = v
        self.dumpCursorArrows(f'END {how} {c=} {h=} {v=}')
    ####################################################################################################################################################################################################
    def isAlt(self):          return 1 if self.kbks[pygwink.MOD_ALT]   or self.kbks[pygwink.LALT]   or self.kbks[pygwink.RALT]   else 0
    def isCtrl(self):         return 1 if self.kbks[pygwink.MOD_CTRL]  or self.kbks[pygwink.LCTRL]  or self.kbks[pygwink.RCTRL]  else 0
    def isShift(self):        return 1 if self.kbks[pygwink.MOD_SHIFT] or self.kbks[pygwink.LSHIFT] or self.kbks[pygwink.RSHIFT] else 0
    def isCtrlShift(self):    return 1 if self.isCtrl() and self.isShift() else 0
    def isAltShift(self):     return 1 if self.isAlt()  and self.isShift() else 0
    def isCtrlAlt(self):      return 1 if self.isCtrl() and self.isAlt()   else 0
    def isCtrlAltShift(self): return 1 if self.isCtrl() and self.isAlt()   and self.isShift() else 0
    ####################################################################################################################################################################################################
    def on_draw(self):
        pyglet.gl.glClearColor(1, 1, 1, 1)
        self.clear()
        self.batch.draw()
    ####################################################################################################################################################################################################
    def on_mouse_motion(self, x, y, dx, dy):
        for view in self.views:
            if view.hit_test(x, y): self.set_mouse_cursor(self.text_cursor)   ;    break
        else:                       self.set_mouse_cursor(None)

    def on_mouse_press(self, x, y, button, modifiers):
        for view in self.views:
            if view.hit_test(x, y): self.set_focus(view)   ;   break
        else:                       self.set_focus(None)
        if self.focus:              self.focus.caret.on_mouse_press(x, y, button, modifiers)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.focus:
            self.focus.caret.on_mouse_drag(x, y, dx, dy, buttons, modifiers)
    ####################################################################################################################################################################################################
    def fmtKbkE(self): return f'{self.symb} {self.symbStr} {self.mods} {self.modsStr} {self.motn} {self.motnStr} {self.kbkTxt}'
    def kbkInfo(self, symb=None, mods=None, text=None, motn=None):
        self.log(f'{util.fmtl([k for k in self.kbks if self.kbks[k]])} : {util.fmtl([pygwink.symbol_string(k) for k in self.kbks if self.kbks[k]])}')
        if symb:  self.symb,   self.symbStr = symb, pygwink.symbol_string(symb)
        if mods:  self.mods,   self.modsStr = mods, pygwink.modifiers_string(mods)
        if motn:  self.motn,   self.motnStr = motn, pygwink.motion_string(motn)
        if text:               self.kbkTxt  = text
#        self.log(f'{self.fmtKbkE()}') # ;  self.log(end='')
#        return self.symbStr, self.modsStr
    ####################################################################################################################################################################################################
    def on_key_press(self, symb, mods):
        symbStr, modsStr  = self.symbStr, self.modsStr
#        self.log(f'{symb} {symbStr} {mods} {modsStr}')
#        self.log(f'{self.fmtKbkE()}')
        self.kbkInfo(symb, mods)
        if   symb == pygwink.ESCAPE: msg = f'{symb=} {symbStr=} {mods=} {modsStr=} Quit'   ;   self.log(msg)   ;   self.quit(msg)
        elif symb == pygwink.S:      self.saveDataFile('@S', self.dataPath1) if self.isCtrl() else None
        elif symb == pygwink.INSERT: self.log(f'INSERT {symb} {symbStr=}')
        elif symb == pygwink.TAB:
            if   self.isShift():           direction = -1
            else:                          direction = 1
            if   self.focus in self.views: i = self.views.index(self.focus)
            else:                          i = 0   ;   direction = 0
            self.set_focus(self.views[(i + direction) % len(self.views)])

    def on_key_release(self, symb, mods, dbg=1):
#        self.log(f'{symb} {mods}')
#        self.log(f'{self.fmtKbkE()}')
        self.kbkInfo(symb, mods)
    ####################################################################################################################################################################################################
    def on_text(self, t, dbg=1):
#        self.log(f'{self.fmtKbkE()}')
        self.kbkInfo(text=t)
        self.log(f'{t=} {self.focus.caret.position=} {self.focus.caret.mark=}')
        if   t == 'S' and self.isShift():      self.saveDataFile(f'@{t=}', self.dataPath1) # if self.isCtrl() else None
        elif t == '$' and self.isShift():      self.snapshot(    f'^{t=}', f'{self.ssi=}')
#        elif t == ' ':                         self.autoMove(     f'{t=}')
        elif t == 'ESCAPE': msg = f'{t=} Quit'   ;  self.log(msg)  ;  self.quit(msg)
        if self.focus:                                   self.focus.caret.on_text(t)
        self.log(f'{t=} {self.focus.caret.position=} {self.focus.caret.mark=}')
    ####################################################################################################################################################################################################
    def on_text_motion(self, m, dbg=1):
        self.kbkInfo(motn=m)
        self.log(f'{self.focus.caret.position=} {self.focus.caret.mark=}')
        if self.focus: self.focus.caret.on_text_motion(m)  ;  self.log(f'focus.caret.on_text_motion {m}') if dbg else '' #  ;   return
        if   self.isCtrlAltShift():            msg =     f'@&^ ??? ({m})'   ;   self.log(msg) #  ;   self.quit(msg)
        elif self.isCtrlAlt():                 msg =     f'@&  ??? ({m})'   ;   self.log(msg) #  ;   self.quit(msg)
#            if   m == 1:                                self.unselectTabs(f' @& LEFT ({            m})',  nc
#            elif m == 2:                                self.unselectTabs(f' @& RIGHT ({           m})', -nc)
        elif self.isAltShift():                msg =     f'&^  ??? ({m})'   ;   self.log(msg) #  ;   self.quit(msg)
        elif self.isCtrlShift():               msg =     f'@^  ??? ({m})'   ;   self.log(msg) #  ;   self.quit(msg)
        elif self.isShift():
            if   m == pygwink.MOTION_UP:                self.move(m, 'UP   ')
            elif m == pygwink.MOTION_DOWN:              self.move(m, 'DOWN ')
            elif m == pygwink.MOTION_LEFT:              self.move(m, 'LEFT ')
            elif m == pygwink.MOTION_RIGHT:             self.move(m, 'RIGHT')
            else:                                       msg =     f'^ ??? ({m})'   ;   self.log(msg) #  ;   self.quit(msg)
        elif self.isAlt():                     msg =     f'& ??? ({m})'   ;   self.log(msg) #  ;   self.quit(msg)
#            if   m == pygwink.MOTION_UP:                self.moveUp(      f' & UP ({          m})')
#            elif m == pygwink.MOTION_DOWN:              self.moveDown(    f' & DOWN ({        m})')
#            elif m == pygwink.MOTION_LEFT:              self.moveLeft(    f' & LEFT ({        m})')
#            elif m == pygwink.MOTION_RIGHT:             self.moveRight(   f' & RIGHT ({       m})')
        elif self.isCtrl():
#            if   m == pygwink.MOTION_PREVIOUS_WORD:     self.selectTabs(  f'@  LEFT ({        m})', -nc)
#            elif m == pygwink.MOTION_NEXT_WORD:         self.selectTabs(  f'@  RIGHT ({       m})',  nc)
            if   m == pygwink.MOTION_BEGINNING_OF_LINE: msg =     f' @  BGN_LINE {m}'   ;   self.log(msg) #  ;   self.quit(msg) # N/A
            elif m == pygwink.MOTION_END_OF_LINE:       msg =     f' @  END_LINE {m}'   ;   self.log(msg) #  ;   self.quit(msg) # N/A
            elif m == pygwink.MOTION_BEGINNING_OF_FILE: msg =     f' @  BGN_FILE {m}'   ;   self.log(msg) #  ;   self.quit(msg) # CTRL HOME
            elif m == pygwink.MOTION_END_OF_FILE:       msg =     f' @  END_FILE {m}'   ;   self.log(msg) #  ;   self.quit(msg) # CTRL END
            else:                                       msg =     f' @ ??? ({      m})'   ;   self.log(msg) #  ;   self.quit(msg)
        elif self.mods == 0:
            if   m == pygwink.MOTION_UP:                self.move(m, 'UP   ')
            elif m == pygwink.MOTION_DOWN:              self.move(m, 'DOWN ')
            elif m == pygwink.MOTION_LEFT:              self.move(m, 'LEFT ')
            elif m == pygwink.MOTION_RIGHT:             self.move(m, 'RIGHT')
#            if   m == pygwink.MOTION_PREVIOUS_WORD:     msg = f'MOTION_PREVIOUS_WORD ({       m})'   ;   self.log(msg) #  ;   self.quit(msg)
#            elif m == pygwink.MOTION_NEXT_WORD:         msg = f'MOTION_NEXT_WORD ({           m})'   ;   self.log(msg) #  ;   self.quit(msg)
            else:                                       msg = f'( ???    {m})'   ;   self.log(msg) #  ;   self.quit(msg)
    ####################################################################################################################################################################################################
    def on_text_motion_select(self, m, dbg=1):
        self.log(f'{self.fmtKbkE()}')
        self.kbkInfo(motn=m)
        if self.focus: self.focus.caret.on_text_motion_select(m)  ;  self.log(f'focus.caret.on_text_motion {m}') if dbg else '' #  ;   return
        if   m == pygwink.MOTION_UP:                self.move(m, 'UP   ')
        elif m == pygwink.MOTION_DOWN:              self.move(m, 'DOWN ')
        elif m == pygwink.MOTION_LEFT:              self.move(m, 'LEFT ')
        elif m == pygwink.MOTION_RIGHT:             self.move(m, 'RIGHT')
        else:                                           msg = f'???   ({m})'   ;   self.log(msg)
    ####################################################################################################################################################################################################
    def move(self, m, how, dbg=1):
        if dbg: self.log(f'BGN {how} {m}')
        for i, v in enumerate(self.views):
            if dbg: self.log(f'Old {v.caret.line=} {v.caret.position=} {v.caret.mark=} {v.lbox.selection_start=} {v.lbox.selection_end=}')
            v.setCursor(v.caret.position)
            if dbg: self.log(f'New {v.caret.line=} {v.caret.position=} {v.caret.mark=} {v.lbox.selection_start=} {v.lbox.selection_end=}')
        if dbg: self.log(f'END {how} {m}')
    ####################################################################################################################################################################################################
    def autoMove(self, how, dbg=1):
        self.log(f'BGN {how}')
        va = 1 if self.vArrow else -1
#        ha = 1 if self.hArrow else -1
        nt, it = self.n[T], 6 # self.i[T]
        mmDist = pygwink.MOTION_RIGHT # ha * nt
        cmDist = va
        amDist = mmDist + cmDist
        if dbg: self.dumpCursorArrows(f'{how} M={mmDist} C={cmDist} A={amDist}')
        if      self.csrMode == MELODY:                                     self.move(mmDist, how)
        elif    self.csrMode == CHORD:
            if   it == 1 and self.vArrow  == UP   and self.hArrow == RIGHT: self.move(  nt*2-1,  how)
            elif it == 6 and self.vArrow  == DOWN and self.hArrow == RIGHT: self.move(-(nt*2-1), how)
            else:                                                           self.move(cmDist, how)
        elif    self.csrMode == ARPG:                                       self.move(amDist, how)
        self.log(f'END {how}')
    ####################################################################################################################################################################################################
    def set_focus(self, focus, dbg=1):
        if focus is self.focus:        self.log(f'{id(focus)=} is {id(self.focus)=}') if dbg else None  ;  return
        if self.focus:
            self.focus.caret.visible = False
            self.focus.caret.mark    = self.focus.caret.position = 0
            if dbg: self.log(f'{self.focus.caret.visible=} {self.focus.caret.position=} {self.focus.caret.mark=}')
        self.focus = focus
        if self.focus:            self.focus.caret.visible = True  ;  self.log(f'{self.focus.caret.visible=}') if dbg else None
    ####################################################################################################################################################################################################
    def dumpViews(self, views=None):
        views = views if views is not None else self.views
        if not views:  self.log(f'No Views {len(views)}')  ;  return
        for i, v in enumerate(views):
            self.dumpView(v, f'[{i}] ')

    def dumpView(self, v, pfx=''):
        self.log(f'V{pfx}{fmtXYWH(v.x, v.y, v.w, v.h)})')
        self.log(f'V{pfx}{v.caret.line=} {v.caret.position=} {v.caret.mark=} {v.lbox.selection_start=} {v.lbox.selection_end=}', pfx=0)
        self.dumpLbox(v.lbox, pfx)  ;  self.dumpRect(v.rect, pfx)

    def dumpLbox(self, l, pfx=''):
        self.log(f'L{pfx}{fmtXYWH(l.x, l.y, l.width, l.height)} cw={l.content_width} ch={l.content_height} cva={l.content_valign}')
        self.log(f'L{pfx}{l.selection_start=} {l.selection_end=}')

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
    def snapshot(self, why='', why2='', dbg=1, dbg2=1):
        if dbg:      self.log(f'{why} {why2}')
        if dbg:      self.log(f'{SNAP_DIR=} {BASE_NAME=} {SNAP_SFX=}')   ;   self.log(f'{BASE_PATH=}', pfx=0)
        lfSeqNum    = f'.{self.lfSeqNum}' if self.lfSeqNum else ''
        SNAP_ID   = f'.{self.ssi}'
        SNAP_NAME = BASE_NAME + lfSeqNum + SNAP_ID + SNAP_SFX
        SNAP_PATH = BASE_PATH / SNAP_DIR / SNAP_NAME
        if dbg:     self.log(f'{SNAP_PATH=}', pfx=0)  ;  self.log(f'{SNAP_ID=:3}  {SNAP_NAME=}')
        pyglet.image.get_buffer_manager().get_color_buffer().save(f'{SNAP_PATH}')
        if dbg2:    self.log(f'{why} {SNAP_NAME=} {why2}', file=sys.stdout)
        self.ssi += 1
    ####################################################################################################################################################################################################
    def deleteGlob(self, g, why=''):
        self.log(f'deleting {len(g)} files from glob {why=}')
        for f in g:
            self.log(f'{f}')
            os.system(f'del {f}')

    def getFilePath(self, seq=0, fdir='files', fsfx='.txt'):
        if seq and not self.lfSeqNum:
            fdir      += '/'
            self.log(f'{fdir=} {fsfx=}')
            pathlib.Path(fdir).mkdir(parents=True, exist_ok=True)
            fGlobArg   = str(BASE_PATH / fdir / BASE_NAME) + '.*' + fsfx
            fGlob      = glob.glob(fGlobArg)
            self.log(f'{fGlobArg=}')
            self.lfSeqNum = 1 + self.getFileSeqNum(fGlob, fsfx)
            fsfx          = f'.{self.lfSeqNum}{fsfx}'
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
    def log(msg='', pfx=1,  file=None, flush=False, sep=',', end='\n'):
        file = LOG_FILE  if file is None else file    ;   util.slog(msg, pfx, file, flush, sep, end)

    def cleanupLog(self):
        self.log(f'Copying {LOG_FILE.name} to {self.lfSeqPath}')
        util.copyFile(LOG_PATH, self.lfSeqPath, LOG_FILE)
        self.log(f'closing {LOG_FILE.name}', flush=True)
        LOG_FILE.close()

    def quit(self, why='', error=1, save=1, dbg=1):
        self.log(f'Exit {why}')
        util.dumpStack(inspect.stack(), file=LOG_FILE)    ;   self.log(util.QUIT_BGN, pfx=0)
        util.dumpStack(util.MAX_STACK_FRAME, file=LOG_FILE)
        self.log(f'BGN {why} {error=} {save=}')           ;   self.log(util.QUIT_BGN, pfx=0)
        self.dumpArgs()
        if      save:  self.saveDataFile(why, self.dataPath1)
        if not error and dbg: self.log('Clean Run')
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
        self.setCursor(0)

    def setCursor(self, i):
        util.slog(f'BGN {self.lbox.selection_start=:3} {self.lbox.selection_end=:3}', file=self.file)
        self.lbox.set_selection(i, i+1)  ;  self.caret.position = i  ;  self.caret.mark = self.lbox.selection_end
        util.slog(f'END {self.lbox.selection_start=:3} {self.lbox.selection_end=:3}', file=self.file)

    def hit_test(self, x, y):  r = self.lbox  ;  return 0 < x - r.x < r.width and 0 < y - r.y < r.height
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
