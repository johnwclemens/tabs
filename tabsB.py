import sys, pathlib, itertools # os
import pyglet
import pyglet.window.event as pygwine
import pyglet.window.key as pygwink
import pyglet.text.caret as pygcrt
#import pyglet.text.layout as pyglbox
from  pyglet.text.layout import IncrementalTextLayout as pyglbox
#sys.path.insert(0, os.path.abspath("./lib"))
#print(f'{len(sys.path)=}')
#for _ in sys.path:
#    print(f'{_}')
import util

Z                = ' '
PATH             = pathlib.Path.cwd() / sys.argv[0]
BASE_PATH        = PATH.parent
BASE_NAME        = BASE_PATH.stem
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

def fsize(w, h, l, c, file):
    fsy = h/l  ;  fsx = 1.4 * w/c
    fs = round(min(fsx, fsy) * 14 / 18)
    util.slog(f'{fs=} {w=} {h=} {c=} {l=} {fsx=} {fsy=}', file=file)
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
        self.x, self.y, self.w, self.h = 0, 0, 0, 0
        self.mx, self.my = 1, 1
        self.kbk, self.symb, self.mods, self.symbStr, self.modsStr = 0, 0, 0, '', ''
        self._initArgs()
        self._initWindowA()
        self.log(f'WxH={self.fmtWxH()}')
        super().__init__(screen=self.screens[self.fsi], fullscreen=self.FULL_SCREEN, resizable=True, visible=False)
        self.log(f'WxH={self.fmtWxH()}')
        self._initWindowB()
        self.log(f'WxH={self.fmtWxH()}')
#        self.n.insert(S, self.ssl())
        self.tblanki, self.tblanks  = 1, [' ', '-']
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
            self.keyboard = pygwine.key.KeyStateHandler()
            self.push_handlers(self.keyboard)
        if dbg: self.log(f'END {self.fmtWxH()}')
    ####################################################################################################################################################################################################
    def _initGroups(self):    #     [P, L, C  T,  N, I, K, V   R, Q, H,  O, A, D]
        self.g = []   ;   self.go = [1, 2, 3, 5,  5, 5, 5, 4,  5, 5, 6,  5, 5, 5]
        self.log(f'gn={util.fmtl(self.go)}')
        for i in range(1+max(self.go)):
            p = None if self.ORDER_GROUP or i==0 else self.g[i-1]
            self.g.append(self._initGroup(i, p))
            self.log(f'({i}) g={self.g[i]} pg={self.g[i].parent}')
    def _initGroup(self, order=0, parent=None): return pyglet.graphics.OrderedGroup(order, parent) if self.ORDER_GROUP else pyglet.graphics.Group(parent)
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
    @staticmethod
    def isShift(mods):        return mods & pygwink.MOD_SHIFT
    @staticmethod
    def isCtrl(mods):         return mods & pygwink.MOD_CTRL
    @staticmethod
    def isAlt(mods):          return mods & pygwink.MOD_ALT
    @staticmethod
    def isCtrlShift(mods):    return mods & pygwink.MOD_CTRL and mods & pygwink.MOD_SHIFT
    @staticmethod
    def isAltShift(mods):     return mods & pygwink.MOD_ALT  and mods & pygwink.MOD_SHIFT
    @staticmethod
    def isCtrlAlt(mods):      return mods & pygwink.MOD_CTRL and mods & pygwink.MOD_ALT
    @staticmethod
    def isCtrlAltShift(mods): return mods & pygwink.MOD_CTRL and mods & pygwink.MOD_ALT and mods & pygwink.MOD_SHIFT
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
    def on_text(self, text):
        self.log(f'{text=} {self.focus.caret.mark=} {self.focus.caret.position=}')
        if self.focus:
            self.focus.caret.on_text(text)

    def on_text_motion(self, motion, dbg=1):
        self.kbk = motion
        self.log(f'{self.focus.caret.mark=} {self.focus.caret.position=}')
        if dbg: self.log(f'BGN {self.fmtKbkEvnt()} motion={motion}')
        if self.focus:
            self.focus.caret.on_text_motion(motion)   ;   return
        if   self.isCtrlAltShift(self.mods):                 msg =             f'@&^({             motion})'   ;   self.log(msg) #  ;   self.exit(msg)
        elif self.isCtrlAlt(self.mods):                      msg =             f'@& ({             motion})'   ;   self.log(msg) #  ;   self.exit(msg)
#            if   motion == 1:                                self.unselectTabs(f'@& LEFT ({        motion})',  nc
#            elif motion == 2:                                self.unselectTabs(f'@& RIGHT ({       motion})', -nc)
        elif self.isAltShift(self.mods):                     msg =             f' &^({             motion})'   ;   self.log(msg) #  ;   self.exit(msg)
        elif self.isCtrlShift(self.mods):                    msg =             f'@^ ({             motion})'   ;   self.log(msg) #  ;   self.exit(msg)
        elif self.isShift(self.mods):
            msg =             f'^ ({              motion})'   ;   self.log(msg) #  ;   self.exit(msg)
            if   motion == pygwink.MOTION_UP:                self.move(f' UP    ({motion})', motion)
            elif motion == pygwink.MOTION_DOWN:              self.move(f' DOWN  ({motion})', motion)
            elif motion == pygwink.MOTION_LEFT:              self.move(f' LEFT  ({motion})', motion)
            elif motion == pygwink.MOTION_RIGHT:             self.move(f' RIGHT ({motion})', motion)
        elif self.isAlt(self.mods):                          msg =             f' & ({             motion})'   ;   self.log(msg) #  ;   self.exit(msg)
#            if   motion == pygwink.MOTION_UP:                self.moveUp(      f' & UP ({          motion})')
#            elif motion == pygwink.MOTION_DOWN:              self.moveDown(    f' & DOWN ({        motion})')
#            elif motion == pygwink.MOTION_LEFT:              self.moveLeft(    f' & LEFT ({        motion})')
#            elif motion == pygwink.MOTION_RIGHT:             self.moveRight(   f' & RIGHT ({       motion})')
        elif self.isCtrl(self.mods):
#            if   motion == pygwink.MOTION_PREVIOUS_WORD:     self.selectTabs(  f'@  LEFT ({        motion})', -nc)
#            elif motion == pygwink.MOTION_NEXT_WORD:         self.selectTabs(  f'@  RIGHT ({       motion})',  nc)
            if   motion == pygwink.MOTION_BEGINNING_OF_LINE: msg = f'@  MOTION_BEGINNING_OF_LINE({ motion})'   ;   self.log(msg) #  ;   self.exit(msg) # N/A
            elif motion == pygwink.MOTION_END_OF_LINE:       msg = f'@  MOTION_END_OF_LINE ({      motion})'   ;   self.log(msg) #  ;   self.exit(msg) # N/A
            elif motion == pygwink.MOTION_BEGINNING_OF_FILE: msg = f'@  MOTION_BEGINNING_OF_FILE ({motion})'   ;   self.log(msg) #  ;   self.exit(msg) # CTRL HOME
            elif motion == pygwink.MOTION_END_OF_FILE:       msg = f'@  MOTION_END_OF_FILE ({      motion})'   ;   self.log(msg) #  ;   self.exit(msg) # CTRL END
            else:                                            msg =             f'CTRL ({           motion})'   ;   self.log(msg) #  ;   self.exit(msg)
        elif self.mods == 0:
            if   motion == pygwink.MOTION_UP:                self.move(f' UP    ({motion})', motion)
            elif motion == pygwink.MOTION_DOWN:              self.move(f' DOWN  ({motion})', motion)
            elif motion == pygwink.MOTION_LEFT:              self.move(f' LEFT  ({motion})', motion)
            elif motion == pygwink.MOTION_RIGHT:             self.move(f' RIGHT ({motion})', motion)
            if   motion == pygwink.MOTION_PREVIOUS_WORD:     msg = f'MOTION_PREVIOUS_WORD ({       motion})'   ;   self.log(msg) #  ;   self.exit(msg)
            elif motion == pygwink.MOTION_NEXT_WORD:         msg = f'MOTION_NEXT_WORD ({           motion})'   ;   self.log(msg) #  ;   self.exit(msg)
            else:                                            msg =                             f'({motion})'   ;   self.log(msg) #  ;   self.exit(msg)

    def on_text_motion_select(self, motion):
        msg = f'({motion})'   ;   self.log(msg)
        if self.focus:
            self.focus.caret.on_text_motion_select(motion)   ;   return
        if   motion == pygwink.MOTION_UP:                self.move(f' UP    ({motion})', motion)
        elif motion == pygwink.MOTION_DOWN:              self.move(f' DOWN  ({motion})', motion)
        elif motion == pygwink.MOTION_LEFT:              self.move(f' LEFT  ({motion})', motion)
        elif motion == pygwink.MOTION_RIGHT:             self.move(f' RIGHT ({motion})', motion)
    ####################################################################################################################################################################################################
    def move(self, how='RIGHT', motion=pygwink.MOTION_DOWN, dbg=1):
        if dbg: self.log(f'{how} {motion}')
        for i, v in enumerate(self.views):
            if dbg: self.log(f' Old {v.caret.line=} {v.caret.position=} {v.caret.mark=}')
#            v.caret.line     += 1 if motion == pygwink.MOTION_DOWN  else -1 if motion == pygwink.MOTION_UP   else 0
#            v.caret.position += 1 if motion == pygwink.MOTION_RIGHT else -1 if motion == pygwink.MOTION_LEFT else 0
#            if   pygwink.MOTION_RIGHT: v.caret.mark = v.caret.position + 1
#            elif pygwink.MOTION_LEFT:  v.caret.position -= 2  ;  v.caret.mark = v.caret.position - 1
            if dbg: self.log(f' New {v.caret.line=} {v.caret.position=} {v.caret.mark=}')
        if dbg: self.log(f'END {how} {motion}')

    def fmtKbkEvnt(self): return f'<{self.kbk:8}> <{self.symb:8}> <{self.symbStr:16}> <{self.mods:2}> <{self.modsStr:16}>'
    ####################################################################################################################################################################################################
    def on_key_press(self, symb, mods, dbg=1, trc=1):
        self.symb, self.mods, self.symbStr, self.modsStr = symb, mods, pygwink.symbol_string(symb), pygwink.modifiers_string(mods)
        self.kbk = self.symbStr  ;  kbk = self.kbk   ;   bgn = 'BGN ' if trc else ''   ;   end = 'END ' if trc else ''
        if   dbg: self.log(f'{bgn}{self.fmtKbkEvnt()}')
        if   kbk == 'TAB':
            if   self.isShift(mods):             direction = -1
            else:                                direction = 1
            if   self.focus in self.views:       i = self.views.index(self.focus)
            else:                                i = 0   ;   direction = 0
            self.set_focus(self.views[(i + direction) % len(self.views)])
        elif kbk == 'S'   and self.isCtrl(mods): self.saveDataFile('@S', self.dataPath1)
        elif kbk == 'ESCAPE':                    self.log(f'{kbk=} Exiting')   ;   pyglet.app.exit()
        if   dbg: self.log(f'{end}{self.fmtKbkEvnt()}')
    ####################################################################################################################################################################################################
    def set_focus(self, focus):
        if focus is self.focus:      return
        if self.focus:
            self.focus.caret.visible = False
            self.focus.caret.mark    = self.focus.caret.position = 0
        self.focus = focus
        if self.focus:
            self.focus.caret.visible = True
    ####################################################################################################################################################################################################
    def dumpViews(self, views=None):
        views = views if views is not None else self.views
        if not views:  self.log(f'No Views {len(views)}')  ;  return
        for i, v in enumerate(views):
            self.dumpView(v, f'[{i}] ')

    def dumpRect(self, r, pfx=''):   self.log(f' Rect{pfx}{fmtXYWH(r.x, r.y, r.width, r.height)}')
    def dumpView(self, v, pfx=''):   self.log(f' View{pfx}{fmtXYWH(v.x, v.y, v.w, v.h)})');  self.dumpLbox(v.lbox, pfx)  ;  self.dumpRect(v.rect, pfx)
    def dumpLbox(self, l, pfx=''):
        self.log(f' Lbox{pfx}{fmtXYWH(l.x, l.y, l.width, l.height)} cw={l.content_width} ch={l.content_height} cva={l.content_valign}')
    ####################################################################################################################################################################################################
    def resizeViews(self, views=None):
        views = views if views is not None else self.views
        if not views:  self.log(f'No Views {len(views)}')  ;  return
        for i, v in enumerate(views):
            self.resizeView(v)

    def resizeRect(self, r):   r.width *= self.mx          ;  r.height *= self.my
    def resizeView(self, v):   v.w = round(v.w * self.mx)  ;  v.h = round(v.h * self.my)  ;  self.resizeLbox(v.lbox)  ;  self.resizeRect(v.rect)
    def resizeLbox(self, l):
        l.width = round(l.width * self.mx)  ;  l.height = round(l.height * self.my)  ;  d = l.document
        fs = d.get_style('font_size', 0)   ;   fs *= self.my
        d.set_style(0, len(d.text), dict(font_size=fs))
    ####################################################################################################################################################################################################
    def on_resize(self, width, height):
        self.dumpDataHorz()
        self.mx = width / self.w   ;  self.my = height / self.h
        self.log(f'BGN {self.fmtWxH()} {self.fmtDxD()} {self.fmtdl()} {self.fmtn()}')
        self.log(   f' {self.width=:4} {self.height=:4} {self.w=:4} {self.h=:4} {self.mx=:5.3f} {self.my=:5.3f}')
        self.w = width   ;   self.h = height
        super().on_resize(width, height)
        self.dumpViews()
        self.resizeViews()
        self.dumpViews()
        self.log(   f' {self.width=:4} {self.height=:4} {self.w=:4} {self.h=:4} {self.mx=:5.3f} {self.my=:5.3f}')
        self.log(f'END {self.fmtWxH()} {self.fmtDxD()} {self.fmtdl()} {self.fmtn()}')
    ####################################################################################################################################################################################################
    def initViews(self, dbg=1): # Bravura Text
        self.w, self.h = self.width, self.height   ;   text = ''
        x, y, w, h     = self.x, self.y, self.w, self.h
        np, nl, nt, nc     = self.n
        for p in range(np):
            for l in range(nl):
                tx = ''  # {font_name ' + f'{name}' + '}{font_size ' + f'{size}' + '}'
                for t in range(nt):
                    txt    = f'{self.data[p][l][t]}'
                    text  += f'{tx}{txt}\n'
                v  = View(text, x, y, w, h, nt, nc, self.batch)
                self.log(f'{fmtXYWH(v.x, v.y, v. w, v.h)}')
                self.views.append(v)
        if dbg: self.dumpViews()
    ####################################################################################################################################################################################################
    @staticmethod
    def log(msg='', pfx=1,  file=None, flush=False, sep=',', end='\n'):
        file = LOG_FILE  if file is None else file    ;   util.slog(msg, pfx, file, flush, sep, end)
    def exit(self, why=''): self.log(f'Exit {why}')   ;   pyglet.app.exit()

########################################################################################################################################################################################################
class View(object): # self.document.set_paragraph_style(0, len(self.document.text), dict(align='center', wrap=True))
    def __init__(self, text, x, y, w, h, l, c, b):
        gA = pyglet.graphics.OrderedGroup(order=1)
        gB = pyglet.graphics.OrderedGroup(order=2)
        fs = fsize(w, h, l, c, file=LOG_FILE)  ;  fn = 'Lucida Console'  ;  dpi = 96
        rgb1 = [255, 200, 20, 255]   ;   rgb2 = [0, 0, 0]   ;   rgb3 = [200, 20, 220]
        self.x, self.y, self.w, self.h = x, y, w, h  ;  dx, dy = 2, 2  ;  dw, dh = 2*dx, 2*dy  ;  x2, y2, w2, h2 = x+dx, y+dy, w-dw, h-dh
        self.doc        = pyglet.text.decode_text(text)     ;   util.slog(f'{text=}', file=LOG_FILE, pfx=0)
        self.doc.set_style(0, len(self.doc.text), dict(font_size=fs, font_name=fn, color=rgb1))
        self.rect       = pyglet.shapes.Rectangle(x2, y2, w2, h2, rgb2, batch=b, group=gA)
        self.lbox       = pyglbox(self.doc, w2, h2, multiline=True, dpi=dpi,  batch=b, group=gB, wrap_lines=True)
        self.lbox.position = x2, y2
        self.caret      = pygcrt.Caret(self.lbox, color=rgb3)
        self.caret.position = 0
        self.caret.mark = 1

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
