import sys, pathlib, itertools # os
import pyglet
import pyglet.window.event as pygwine
#import pyglet.window.key as pygwink
#sys.path.insert(0, os.path.abspath("./lib"))
#print(f'{len(sys.path)=}')
#for _ in sys.path:
#    print(f'{_}')
import util

Z                = ' '
PATH             = pathlib.Path.cwd() / sys.argv[0]
BASE_PATH        = PATH.parent
BASE_NAME        = BASE_PATH.stem
FDL              = ' len(data 0 00 000)'
FDT              = 'type(data 0 00 000)'
P, L, S, C       =  0,  1,  2,  3
T, N, I, K       =  4,  5,  6,  7
R, Q, H, V       =  8,  9, 10, 11
O, A, D          = 12, 13, 14
JTEXTS           = ['Page',  'Line',  'Sect',  'Col',  'Tab',  'Note',  'IKey',  'Kord',  '_LLR',  '_LLC', 'Curs', 'View',  '_SNo',  '_SNm',  '_Cpo', '_TNIK']
JFMT             = [   1,       2,       2,       3,      4,      4,       4,       4,       2,       3,       1,       1,      2,      2,      3,       4]

class Tabs(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        util.slog(f'init {args=} {kwargs=}')
        self._initArgs()
        self._initWindowA()
        self.log(f'WxH={self.fmtWxH()}')
        super().__init__(screen=self.screens[1], fullscreen=self.FULL_SCREEN, resizable=True, visible=False)
        self.log(f'WxH={self.fmtWxH()}')
        self._initWindowB()
        self.log(f'WxH={self.fmtWxH()}')
        self.data        = []
        self.views       = []
        self.x, self.y, self.w, self.h = 0, 0, 0, 0
        self.n.insert(S, self.ssl())
        self.tblanki, self.tblanks  = 1, [' ', '-']
        self.tblank      = self.tblanks[self.tblanki]
        self.tblankCol   = self.tblank * self.n[T]
        self.tblankRow   = self.tblank * self.n[C]
        self.dumpBlank()
        self.initData()
        self.initView()
        self.text_cursor = self.get_system_mouse_cursor('text')
        self.focus       = None
        self.set_focus(self.views[0])
    ####################################################################################################################################################################################################
    def _initWindowA(self, dbg=1):
        display      = pyglet.canvas.get_display()
        if dbg: self.log(f'BGN {self.fmtWxH()}')  ;  self.log(f'{display=}')
        self.screens = display.get_screens()      ;  s = self.screens
        if dbg:
            for i in range(len(s)): self.log(f'screens[{i}] x={s[i].x} y={s[i].y:5} {self.fmtWxH(s[i].width, s[i].height)}')
            self.log(f'END {self.fmtWxH()}')

    def _initWindowB(self, dbg=1):
        if dbg: self.log(f'BGN {self.fmtWxH()}')
        self.batch = pyglet.graphics.Batch()
#        self._initGroups()
        self.set_visible()
        self.log(f'get_size={self.get_size()}')
        if self.EVENT_LOG and self.VERBOSE:
            self.eventLogger = pygwine.WindowEventLogger()
            self.push_handlers(self.eventLogger)
            self.keyboard = pygwine.key.KeyStateHandler()
            self.push_handlers(self.keyboard)
        if dbg: self.log(f'END {self.fmtWxH()}')
    ####################################################################################################################################################################################################
    def _initArgs(self):
        self.dfn         = 'test.7.dat'
        self.n           = [1, 1, 50, 6]
        self.SS          = set() if 0 else {0}
        self.FULL_SCREEN = 0   ;   self.EVENT_LOG = 0   ;   self.VERBOSE = 0
        ARGS             = util.parseCmdLine(file=LOG_FILE)
        self.log(f' argMap={util.fmtm(ARGS)}')
        if 'e' in ARGS and len(ARGS['e']) == 0: self.EVENT_LOG     =  1
        if 'f' in ARGS and len(ARGS['f']) >  0: self.dfn = ARGS['f'][0]
        if 'n' in ARGS and len(ARGS['n']) >  0: self.n = [int(ARGS['n'][i]) for i in range(len(ARGS['n']))]
        if 'F' in ARGS and len(ARGS['F']) == 0: self.FULL_SCREEN   =  1
        if 'S' in ARGS and len(ARGS['S']) >= 0: self.SS = {int(ARGS['S'][i]) for i in range(len(ARGS['S']))}
        if 'v' in ARGS and len(ARGS['v']) == 0: self.VERBOSE       =  1
        self.dumpArgs()
    ####################################################################################################################################################################################################
    def dumpArgs(self):
        self.log(f'[e]     {self.EVENT_LOG=}')
        self.log(f'[f]     {self.dfn=}')
        self.log(f'[F]     {self.FULL_SCREEN=}')
        self.log(f'[n]     {self.fmtn()}')
        self.log(f'[S] .SS={util.fmtl(self.SS)}')
        self.log(f'[v]     {self.VERBOSE=}')

    def initData(self):
        self._initDataPath()
        self.readDataFile(self.dataPath1)
        util.copyFile    (self.dataPath1, self.dataPath2)
#        self.data       = self.transposeData(dump=1)

    def fmtDxD(self, data=None,      d='x'):   l = list(map(str, self.dl(data)))       ;    return f'({d.join(l)})'
    def fmtWxH(self, w=None, h=None, d='x'):   w = w if w is not None else self.width  ;  h = h if h is not None else self.height  ;  return f'({w}{d}{h})'
    def ssl(self, dbg=0): l = len(self.SS)  ;  self.log(f'{self.fmtn()} SS={util.fmtl(self.ss2sl())} l={l}') if dbg else None  ;  return l
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
        dataDir   = 'data'  ;  dataSfx = '.dat'  ;  dataPfx = f'.{self.n[C]}'
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
            if    self.isVert(): data = self.transposeData()
            else:                data = self.data
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
        np, nl, ns, nc, nr = self.n
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
        nt  = self.n[C]  ;  nr = self.n[T]  ;  crlf = 2
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
        if dump:        self.dumpDataVert(data) if self.isVert(data) else self.dumpDataHorz(data)
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
        self.dumpDataVert(Xdata) if self.isVert(Xdata) else self.dumpDataHorz(Xdata)
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
        if self.focus:
            self.focus.caret.on_text(text)

    def on_text_motion(self, motion):
        if self.focus:
            self.focus.caret.on_text_motion(motion)

    def on_text_motion_select(self, motion):
        if self.focus:
            self.focus.caret.on_text_motion_select(motion)
    ####################################################################################################################################################################################################
    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.TAB:
            if modifiers & pyglet.window.key.MOD_SHIFT: direction = -1
            else:                                       direction = 1
            if self.focus in self.views:                i = self.views.index(self.focus)
            else:                                       i = 0     ;     direction = 0
            self.set_focus(self.views[(i + direction) % len(self.views)])
        elif symbol == pyglet.window.key.ESCAPE:        pyglet.app.exit()
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
    def on_resize(self, width, height):
        mx = width / self.w   ;  my = height / self.h
        self.log(f'BGN {self.width=:4} {self.height=:4} {self.w=:4} {self.h=:4} {mx=:5.3f} {my=:5.3f}', pfx=0)
        self.w = width   ;   self.h = height
        super().on_resize(width, height)
        if not self.views:  self.log(f'No Views {len(self.views)}')  ;  return
        for i, v in enumerate(self.views):
            l  = v.layout   ;   r  = v.rectangle
            lx, ly, lw, lh = l.x, l.y, l.width, l.height
            rx, ry, rw, rh = r.x, r.y, r.width, r.height
            self.log(f' {lx=} {ly=}  {lw=:4} {lh=:4}  {rx=} {ry=}  {rw=:4} {rh=:4}', pfx=0)
            l.width = int(l.width * mx)  ;  l.height = int(l.height * my)  ;  r.width = int(r.width * mx)  ;  r.height = int(r.height * my)
            lx, ly, lw, lh = l.x, l.y, l.width, l.height
            rx, ry, rw, rh = r.x, r.y, r.width, r.height
            self.log(f' {lx=} {ly=}  {lw=:4} {lh=:4}  {rx=} {ry=}  {rw=:4} {rh=:4}', pfx=0)
        self.log(f'END {self.width=:4} {self.height=:4} {self.w=:4} {self.h=:4} {mx=:5.3f} {my=:5.3f}', pfx=0)
    ####################################################################################################################################################################################################
    def initView(self): # self.dl()[P], self.dl()[L], self.dl()[T]
        self.w, self.h = self.width, self.height   ;   text = ''
        x, y, w, h     = self.x, self.y, self.w, self.h
        np, nl, nt     = self.n[P], self.n[L], self.n[T]
        for p in range(np):
            for l in range(nl):
                tx = '{font_name "Bravura Text"}{font_size 36}'
                for t in range(nt):
                    txt    = f'{self.data[p][l][t]}'
                    text  += f'{tx}{txt}\n'
                v  = View(text, x, y, w, h, nt, self.batch)
                lx, ly, lw, lh =    v.layout.x,    v.layout.y,    v.layout.width,    v.layout.height
                rx, ry, rw, rh = v.rectangle.x, v.rectangle.y, v.rectangle.width, v.rectangle.height
                self.log(f'{lx=} {ly=}  {lw=} {lh=}  {rx=} {ry=}  {rw=} {rh=}')
                self.views.append(v)
    @staticmethod
    def log(msg='', pfx=1,  file=None, flush=False, sep=',', end='\n'):
        file = LOG_FILE  if file is None else file   ;   util.slog(msg, pfx, file, flush, sep, end)

class View: # self.document.set_paragraph_style(0, len(self.document.text), dict(align='center', wrap=True))
    def __init__(self, text, x, y, w, h, l, batch):
        self.x, self.y, self.w, self.h = x, y, w, h
        self.document = pyglet.text.decode_attributed(text)
        self.document.set_style(          0, len(self.document.text), dict(color=(255, 200, 20, 255), font_size=24, font_name='Bravura Text'))
        font = self.document.get_font(0)
        fs   = font.size   ;   fh = font.ascent - font.descent
        font = self.scaleFont(font, h, l)
        fs2  = font.size   ;   fh2 = font.ascent - font.descent
        self.document.set_style(0, len(self.document.text), dict(font_size=font.size))
        util.slog(f'{self.x=} {self.y=} {self.w=} {self.h=} {l=} {fs=} {fh=} fh*l={fh*l} {fs2=:5.2f} {fh2=:5.2f} fh2*l={fh2*l:5.2f}')
        util.slog(f'{text=}', file=LOG_FILE, pfx=0)
        self.layout = pyglet.text.layout.IncrementalTextLayout(self.document, w, h, batch=batch, multiline=True, wrap_lines=True)
        self.layout.position = x, y   ;   o = 0
        self.caret = pyglet.text.caret.Caret(self.layout)
        self.rectangle = pyglet.shapes.Rectangle(x - o, y - o, w + o, h + o, (0, 0, 0), batch)

    @staticmethod
    def scaleFont(font, h, l, dbg=1):
        fs  = font.size
        fh  = font.ascent - font.descent
        fhl = fh * l
        scale = h / fhl
        font.size = fs * scale
        if dbg: util.slog(f'{fs=} {fh=} {h=} {l=} (fh*l)={fhl=} (h/fhl)={scale=:5.3f} (fs*scale)={font.size=:4.1}')
        return font

    def hit_test(self, x, y): return 0 < x - self.layout.x < self.layout.width and 0 < y - self.layout.y < self.layout.height

if __name__ == '__main__':
    LOG_PATH = util.getFilePath(BASE_NAME, BASE_PATH, fdir='logs', fsfx='.log')
    with open(   str(LOG_PATH), 'w')   as   LOG_FILE:
        util.slog(f'{LOG_PATH=}',      file=LOG_FILE)
        util.slog(f'{LOG_FILE.name=}', file=LOG_FILE)
        Tabs()
        pyglet.app.run()
