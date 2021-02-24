import inspect, math, sys, os#, shutil#, unicodedata
import pyglet, pathlib
import pyglet.window.key as pygwink
import pyglet.window.event as pygwine
sys.path.insert(0, os.path.abspath('../lib'))
import cmdArgs

class Tabs(pyglet.window.Window):
    def __init__(self):#        shutil.rmtree(self.snapPath)
        global FULL_SCREEN, SUBPIX, ORDER_GROUP, TEST
        self.ww, self.hh  = 640, 480
        if TEST: self.n, self.i, self.x, self.y, self.w, self.h, self.o, self.g = [12, 12, 0, 0], [0, 0, 0, 0], [4, 0, 0, 0], [0, 3, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [1, 1, 0, 0], []
        else:    self.n, self.i, self.x, self.y, self.w, self.h, self.o, self.g = [1, 3, VRSN, 6, 120], [0, 2, 0, 5, 122], [0, 4, 0, 0, 0], [0, 4, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [2, 0, 0, 0, 3], []
        self.argMap = cmdArgs.parseCmdLine(dbg=1)
        if 'n' in self.argMap and len(self.argMap['n'])  > 0: self.n            = [int(self.argMap['n'][i]) for i in range(len(self.argMap['n']))]
        if 'i' in self.argMap and len(self.argMap['i'])  > 0: self.i            = [int(self.argMap['i'][i]) for i in range(len(self.argMap['i']))]
        if 'x' in self.argMap and len(self.argMap['x'])  > 0: self.x            = [int(self.argMap['x'][i]) for i in range(len(self.argMap['x']))]
        if 'y' in self.argMap and len(self.argMap['y'])  > 0: self.y            = [int(self.argMap['y'][i]) for i in range(len(self.argMap['y']))]
        if 'w' in self.argMap and len(self.argMap['w'])  > 0: self.ww           =  int(self.argMap['w'][0])
        if 'h' in self.argMap and len(self.argMap['h'])  > 0: self.hh           =  int(self.argMap['h'][0])
        if 'o' in self.argMap and len(self.argMap['o'])  > 0: self.o            = [int(self.argMap['o'][i]) for i in range(len(self.argMap['o']))]
        if 'f' in self.argMap and len(self.argMap['f']) == 0: FULL_SCREEN       = 1
        if 'g' in self.argMap and len(self.argMap['g']) == 0: ORDER_GROUP       = 1
        if 's' in self.argMap and len(self.argMap['s']) == 0: SUBPIX            = 1
        if 't' in self.argMap and len(self.argMap['t']) == 0: TEST              = 1
        log('[n]            n={}'.format(self.n))
        log('[i]            i={}'.format(self.i))
        log('[x]            x={}'.format(self.x))
        log('[y]            y={}'.format(self.y))
        log('[w]           ww={}'.format(self.ww))
        log('[h]           hh={}'.format(self.hh))
        log('[o]            o={}'.format(self.o))
        log('[f]  FULL_SCREEN={}'.format(FULL_SCREEN))
        log('[g]  ORDER_GROUP={}'.format(ORDER_GROUP))
        log('[s]       SUBPIX={}'.format(SUBPIX))
        log('[t]         TEST={}'.format(TEST))
        if len(self.n) == K: self.n.append(self.n[C] + CCC)  ;  log('[n] +=n[C]+CCC n={}'.format(self.n))
        self.fontBold, self.fontItalic, self.fontNameIndex, self.fontColorIndex, self.fontSizeIndex, self.fontDpiIndex = 0, 0, 0, 0, len(FONT_SIZES)//3, 3
        self._initWindowA()
        super().__init__(screen=self.screens[1], fullscreen=FULL_SCREEN, resizable=True, visible=False)
        self._initWindowB()
        self.symb, self.symbStr, self.mods, self.modsStr, self.kbk = 0, '', 0, '', 0 ; self.ci = 0
        self.cursor, self.caret = None, None
        self.data, self.sprites = [], []
        self._init() if not TEST else self._initTestColors()
        log('__init__(END)'.format())

    def _initWindowA(self, dbg=1):
        if dbg: log('_initWindowA(BGN) wxh={}x{}'.format(self.ww, self.hh))
        display      = pyglet.canvas.get_display()
        self.screens = display.get_screens()
        if dbg: log('_initWindowA(END) display={} screens={}'.format(display, self.screens))

    def _initWindowB(self, dbg=1):
        self.batch = pyglet.graphics.Batch()
        self._initGroups()
        if dbg: log('_initWindowB(BGN) wxh={}x{}'.format(self.ww, self.hh))
        self.set_visible()
        if not FULL_SCREEN: self.set_size(self.ww, self.hh)
        self.ww, self.hh = self.get_size()
        self.eventLogger = pygwine.WindowEventLogger()
        self.push_handlers(self.eventLogger)
        if dbg: log('_initWindowB(END) wxh={}x{}'.format(self.ww, self.hh))
########################################################################################################################################################################################################
    def _initTestColors(self):
#        self.clGroup = self._initGroup(0)
        self.colorLists = []
        n1, i1, x1, y1, w1, h1, o1, g1 = self.geom(0, 0, 0, self.ww, self.hh, '_initTestColors(0)', init=True, dump=0)
        n2, i2, x2, y2, w2, h2, o2, g2 = self.geom(1, 0, 0, self.ww, self.hh, '_initTestColors(1)', init=True, dump=0)
        for i in (P, L): self.dumpGeom(i, '_initTestColors() i={}'.format(i))
        c = COLORS
#        end = ['\n', ' '];        [[log('{:2} {:2} {:3} {:3} {:3} {:3}'.format(i, j, c[i][j][0], c[i][j][1], c[i][j][2], c[i][j][3]), end=end[0 if j==n2-1 else 1]) for j in range(n2)] for i in range(n1)]
        self.dumpSprite()
        for i in range(n1):
            sprites = []
            for j in range(n2):
                xx, yy = x1+(w1+x1)*i, self.hh-(h2+y2)*(j+1)
                self.createSprite('_initTestColors()', sprites, g1, c[i][j], xx, yy, w1, h2, i, j, v=True, dbg=1)
            self.colorLists.append(sprites)
#        log('_initTestColorLists(End)')

    def resizeTestColors(self):
        cls = self.colorLists
        ww, hh = self.ww, self.hh
        n1, i1, x1, y1, w1, h1, o1, g1, mx, my = self.geom(0, 0, 0, ww, hh, 'resizeTestColors(0)', init=False, dump=0)
        n2, i2, x2, y2, w2, h2, o2, g2, mx, my = self.geom(1, 0, 0, ww, hh, 'resizeTestColors(1)', init=False, dump=0)
        for i in range(n1):
            for j in range(n2):
                xx, yy = x1+(w1+x1)*i, hh-(h2+y2)*(j+1)
                cls[i][j].update(x=xx, y=yy, scale_x=w1/self.w[P], scale_y=h2/self.h[L])
                self.dumpSprite(cls[i][j], i*n2+j, '{:20} {:3} {:3} {:7.2f} {:7.2f} {:7.2f} {:7.2f}'.format('resizeTestColors()', i, j, xx, yy, w1, h2))
        log('resizeTestColors(END) ww={} x={} w={:7.2f} x+w={:7.2f} ww-x-w={:7.2f} : y={} hh={} h={:7.2f} y+h={:7.2f} hh-y-h={:7.2f}'.format(ww, x1, w1, x1+w1, ww-x1-w1, hh, y2, h2, y2+h2, hh-y2-h2))
########################################################################################################################################################################################################
    def _initGroups(self):
        for i in range(len(self.n)+3):
            p = None if ORDER_GROUP or i==0 else self.g[i-1]
            self.g.append(self._initGroup(i, p))
            log('_initGroups({}) g={} pg={}'.format(i, self.g[i], self.g[i].parent))

    @staticmethod
    def _initGroup(order=0, parent=None):
        return pyglet.graphics.OrderedGroup(order, parent) if ORDER_GROUP else pyglet.graphics.Group(parent)
#        if ORDER_GROUP: return pyglet.graphics.OrderedGroup(order, parent)
#        else:           return pyglet.graphics.Group(parent)

    def geom(self, j, px, py, pw, ph, why='', init=False, dump=3, dbg=0):
        nq = self.n[Q]
        n, i, x, y, w, h, o , g = self.n[j], self.i[j], self.x[j], self.y[j], self.w[j], self.h[j], self.o[j], self.g[j]
        if   nq and j == Q: n = self.n[R] + 1
        elif nq and j == R: n += 1
        elif j == C: n += CCC
        if   o == 0: w, h =  pw - x*2,          (ph - y*(n + 1))/n
        elif o == 1: w, h = (pw - x*(n + 1))/n, (ph - y*(n + 1))/n
        elif o == 2: w, h =  pw - x*2,           ph - y*2
        elif o == 3: w, h = (pw - x*(n + 1))/n,  ph - y*2
        if init: self.w[j], self.h[j] = w, h
        if o != 3: x += px #; y = py+ph-y
        if dump == 2 or dump == 3: self.dumpSprite()
        if dump == 1 or dump == 3: self.dumpGeom(j, why)
        if dbg: log('geom({}) px={:7.2f} py={:7.2f} pw={:7.2f} ph={:7.2f}  =>  n={:3} x={:4} y={:4} w={:7.2f} h={:7.2f} o={}'.format(j, px, py, pw, ph, n, x, y, w, h, o))
        if nq and j == Q: n = nq
#        elif nq and j == R: n = self.n[R]
        if init: return n, i, x, y, w, h, o, g
        else:    return n, i, x, y, w, h, o, g, w/self.w[j], h/self.h[j]

    def dumpGeom(self, j, why=''):
        n, i, x, y, w, h, o , g = self.n[j], self.i[j], self.x[j], self.y[j], self.w[j], self.h[j], self.o[j], self.g[j]
        log('{:25} j={} n={:3} i={:4} x={:3} y={:3} w={:7.2f} h={:7.2f} o={} g={}'.format(why, j, n, i, x, y, w, h, o, g))
########################################################################################################################################################################################################
    def _init(self, dbg=1):
        if dbg: log('_init(BGN) n={} i={}'.format(self.n, self.i))
        self.kp = [REDS[0], REDS[2], REDS[4], REDS[6], REDS[8], REDS[10]]  ;  self.kl = [GREENS[0], GREENS[2]]  ;  self.kq = [CYANS[0], CYANS[5]]  ;  self.kr = [YELLOWS[0], YELLOWS[3]]  ;  self.kc = [GRAYS[11], GRAYS[7]]
        self.ssi  = 0
        self.cpr  =  self.n[K]
        self.cpl  = (self.n[R] + self.n[Q]) * self.cpr
        self.cpp  =  self.n[L] * self.cpl
        self.tabs, self.pages, self.lines, self.qrows, self.rows, self.cols = [], [], [], [], [], []
        self.readDataFile()
        self.createSprites()
        if self.n[Q]: self.labels = []  ;  self.createLabels(self.g[C+1])
        self.createTabs(  self.g[C+2])
        self.createCursor(self.g[C+3])
        self.m = self.whMin()
        self.dumpStruct('_init')
        if dbg: log('_init(END) n={} i={}'.format(self.n, self.i))
########################################################################################################################################################################################################
    def readDataFile(self, dbg=1):
        DATA_FILE.seek(0, 2)  ;  size = DATA_FILE.tell()  ;  DATA_FILE.seek(0, 0)
        log('readDataFile(BGN) name={} size={:8,} bytes={:4,.0f} KB'.format(DATA_FILE.name, size, size/1024))
        lines, strings = [], []  ;  nl, ns, nc = 0, 0, 0
        log('reading {}{} line'.format(nl + 1, self.ordSfx(nl + 1)))
        while 1:
            string = DATA_FILE.readline().strip()  ;  ns = len(strings)  ;  nc = len(strings[0]) if ns else 0
            if len(string) == 0:
                if ns: lines.append(strings)  ;  nl += 1  ;  log('read    {:2}{} line with {:6,} cols on {:4,} strings {:8,} tabs'.format(nl, self.ordSfx(nl), nc, ns, nc*ns))  ;  strings=[]  ;  continue
                else: break
            strings.append(string)
            if dbg: log('{}'.format(string), ind=0)
        nl = len(lines)  ;  ns = len(lines[0])  ;  nc = len(lines[0][0])  ;  nt = nl*nc*ns
        log('read     {:2} lines with {:6,} cols on {:4,} strings {:8,} tabs'.format(nl, nl*nc, nl*ns, nt))
#        for l in range(len(lines)):
#            if dbg: self.dumpData(lines[l], why='readDataFile(lines) before transpose')
#            tmp = self.transpose(lines[l])
#            if dbg: self.dumpData(tmp, why='readDataFile(lines) after transpose')
#            self.data.append(tmp)
        if dbg: self.dumpData(lines, why='readDataFile(lines) before transpose')
        self.data = self.transpose(lines)
        if dbg: self.dumpData(self.data, why='readDataFile(lines) after transpose')
        log('readDataFile(assert) size == nt + 2*(nl*ns+nl-1): {:8,} == {:8,} + {}'.format(size, nt, 2*(nl*ns+nl-1)))  ;  assert size == nt + 2*(nl*ns+nl-1)
        log('readDataFile(END) name={} size={:8,} bytes={:4,.0f} KB'.format(DATA_FILE.name, size, size/1024))

    def dumpData(self, data, why='', ll=1, ls=1, li=0):
        log('dumpData(BGN) ll={} ls={} li={} ({} x {} x {})={:8,} tabs {}'.format(ll, ls, li, len(data), len(data[0]), len(data[0][0]), len(data)*len(data[0])*len(data[0][0]), why))
        for l in range(len(data)):
            if ll: self.dumpDataLabels(data[l], l, i=li)
            for c in range(len(data[l])):
                if ls and li: sl = 'String {:2}'.format(c+1)  ;  log('{:{w}} '.format(sl, w=li), ind=0, end='')
                for s in range(len(data[l][c])):
                    log('{}'.format(data[l][c][s]), ind=0, end='')
                log(ind=0)
            log(ind=0)
        t = self.transpose(data)
        log('dumpData(   ) ll={} ls={} li={} ({} x {} x {})={:8,} tabs [Transpose] {}'.format(ll, ls, li, len(t), len(t[0]), len(t[0][0]), len(data)*len(data[0])*len(data[0][0]), why))
        for l in range(len(t)):
            if ll: self.dumpDataLabels(t[l], l, i=li)
            for c in range(len(t[l])):
                if ls and li: log('{:{w}} '.format(c+1, w=li), ind=0, end='')
                for s in range(len(t[l][c])):
                    log('{}'.format(t[l][c][s]), ind=0, end='')
                log(ind=0)
        log(ind=0)
        log('dumpData(END) ll={} ls={} li={} ({} x {} x {})={:8,} tabs {}'.format(ll, ls, li, len(data), len(data[0]), len(data[0][0]), len(data)*len(data[0])*len(data[0][0]), why))

    @staticmethod
    def dumpDataLabels(data, line, i=0):
        n = len(data[0])  ;   a = ' ' * n   ;  b = ' ' * (i+1) if i else ''
        ll = 'Line {}'.format(line + 1)     ;  l = '{:{}}'.format(ll, i+1)
        log('{}'.format(b), ind=0, end='')  ;  [  log('{}'.format(c//100   if c>=100 else ' '), ind=0, end='') for c in range(1, n+1) ]  ;  log(ind=0)
        log('{}'.format(b), ind=0, end='')  ;  [  log('{}'.format(c//10%10 if c>=10  else ' '), ind=0, end='') for c in range(1, n+1) ]  ;  log(ind=0)
        log('{}'.format(b), ind=0, end='')  ;  [  log('{}'.format(c%10),                        ind=0, end='') for c in range(1, n+1) ]  ;  log(ind=0)
        if i: log('{}'.format(l), ind=0, end=''); log('{}'.format(a),                           ind=0)

    def transpose(self, data, dbg=1):
        if dbg: log('transpose(BGN) {}'.format(data))
        t = []
        for l in range(len(data)):
            t.append(self.transpose_OLD(data[l]))
#            for c in range(len(data[l][0])):
#                a = []  ;  s = ''  ;  tt = None
#                for r in range(len(data[l])):
#                    tt = type(data[l][r])
#                    if   tt is str:  s += data[l][r][c]
#                    elif tt is list: a.append(data[l][r][c])
#                t.append(s) if tt is str else t.append(a)
#                if dbg: log('{} {} {}'.format(s, a, t))
        if dbg: log('transpose(END) {}'.format(t))
        return t

    @staticmethod
    def transpose_OLD(data, dbg=0):
        if dbg: log('transpose_OLD(BGN) {}'.format(data))
        t = []
        for c in range(len(data[0])):
            a = []  ;  s = ''  ;  tt = None
            for r in range(len(data)):
                tt = type(data[r])
                if   tt is str:  s += data[r][c]
                elif tt is list: a.append(data[r][c])
            t.append(s) if tt is str else t.append(a)
#            if dbg: log('{} {} {}'.format(s, a, t))
        if dbg: log('transpose_OLD(END) {}'.format(t))
        return t
########################################################################################################################################################################################################
    '''
    def createPages(self):
        cc = [REDS[0], REDS[2], REDS[4], REDS[6], REDS[8], REDS[10]]
        n, i, x, y, w, h, o, g = self.geom(P, self.x[P], self.y[P], self.ww, self.hh, why='', init=True, dump=0)
        for p in range(n):
            page = self.createSprite('createPages', self.pages, g, cc[p%len(cc)], x, y, w, h, p, 0, dbg=1)
            if self.n[P+1] > 0: self.createLines(page)
        return self.pages

    def createLines(self, spr):
        cc = [GREENS[0], GREENS[2]]
        n, i, x, y, w, h, o, g = self.geom(L, spr.x, spr.y, spr.width, spr.height, why='', init=True, dump=0)
        for l in range(n):
            yy = spr.y+spr.height-(h+y)*(l+1)
            line   = self.createSprite('createLines', self.lines, g, cc[l%len(cc)], x, yy, w, h, l, 0, v=True if len(self.pages)==1 else False, dbg=1)
            if self.n[L+1] > 0:
                self.createQRow(line)
                self.createRows(line)

    def createQRow(self, spr):
        cc = [YELLOWS[0], YELLOWS[3]]
        n, i, x, y, w, h, o, g = self.geom(Q, spr.x, spr.y, spr.width, spr.height, why='', init=True, dump=0, dbg=0)
        yy = spr.y+spr.height-(h+y)
        qrow = self.createSprite('createQRow', self.qrows, g, cc[0], x, yy, w, h, 0, 0, v=True if len(self.pages)==1 else False, dbg=1)
        if self.n[R+1] > 0: self.createCols(qrow)

    def createRows(self, spr):
        cc = [CYANS[0], CYANS[5]]
        n, i, x, y, w, h, o, g = self.geom(R, spr.x, spr.y, spr.width, spr.height, why='', init=True, dump=0, dbg=0)
        r1 = 1 if VRSN else 0
        r2 = n if VRSN else n
        for r in range(r1, r2):
            yy = spr.y+spr.height-(h+y)*(r+1)
            row   = self.createSprite('createRows', self.rows, g, cc[r%len(cc)], x, yy, w, h, r, 0, v=True if len(self.pages)==1 else False, dbg=1)
            if self.n[R+1] > 0: self.createCols(row)

    def createCols(self, spr):
        a, b = 11, 8; cc = [GRAYS[a], GRAYS[b]] if len(self.rows)%2 else [GRAYS[b], GRAYS[a]]
        n, i, x, y, w, h, o, g  = self.geom(C, spr.x, spr.y, spr.width, spr.height, why='', init=True, dump=0)
        for c in range(n):
            xx, yy = spr.x+x+(w+x)*c, spr.y+spr.height-(h+y)
            self.createSprite('createCols', self.cols, g, cc[c%len(cc)], xx, yy, w, h, c, 0, v=True if len(self.pages)==1 else False, dbg=1)
    '''
    def createSprites_NEW(self, dbg=1):
        log('createSprites(BGN) n={}'.format(self.n))
        if dbg: self.dumpSprite()
#        self.kp = [REDS[0], REDS[2], REDS[4], REDS[6], REDS[8], REDS[10]]  ;  self.kl = [GREENS[0], GREENS[2]]  ;  self.kq = [CYANS[0], CYANS[5]]  ;  self.kr = [YELLOWS[0], YELLOWS[3]]  ;  self.kc = [GRAYS[11], GRAYS[7]]
#        self.kp, self.kl, self.kq, self.kr, self.kc = [REDS[0], REDS[2], REDS[4], REDS[6], REDS[8], REDS[10]], [GREENS[0], GREENS[2]], [CYANS[0], CYANS[5]], [YELLOWS[0], YELLOWS[3]], [GRAYS[11], GRAYS[7]]
        self.createPages()
        if dbg: self.dumpSprite()
        log('createSprites(END) n={}'.format(self.n))

    def createPages(self, dbg=1):
        np, ip, xp, yp, wp, hp, op, gp = self.geom(P, self.x[P], self.y[P], self.ww, self.hh, why='', init=True, dump=0)
        for p in range(np):
            page = self.createSprite('createPages', self.pages, gp, self.kp[p % len(self.kp)], xp, yp, wp, hp, p, 0, dbg=dbg)
            if self.n[L]: self.createLines(page, v=1 if p == 1 else 0)

    def createLines(self, page, v, dbg=1):
        nl, il, xl, yl, wl, hl, ol, gl = self.geom(L, page.x, page.y, page.width, page.height, why='', init=True, dump=0)
        for l in range(nl):
            yyl = page.y + page.height - (hl + yl) * (l + 1)
            line = self.createSprite('createLines', self.lines, gl, self.kl[l % len(self.kl)], xl, yyl, wl, hl, l, 0, v=v, dbg=dbg)
            if self.n[Q]: self.createQRow(line, v)
            self.createRows(line, v)

    def createQRow(self, line, v, dbg=1):
        nq, iq, xq, yq, wq, hq, oq, gq = self.geom(Q, line.x, line.y, line.width, line.height, why='', init=True, dump=0, dbg=0)
        for q in range(nq):
            yyq = line.y + line.height - (hq + yq) * (q + 1)
            qrow = self.createSprite('createQRow', self.qrows, gq, self.kq[0], xq, yyq, wq, hq, 0, 0, v=v, dbg=dbg)
            if self.n[C]: self.createCols(qrow, v)

    def createRows(self, line, v, dbg=1):
        nr, ir, xr, yr, wr, hr, o, gr = self.geom(R, line.x, line.y, line.width, line.height, why='', init=True, dump=0, dbg=0)
        rr = 1 if self.n[Q] else 0
        for r in range(rr, nr):
            yyr = line.y + line.height - (hr + yr) * (r + 1)
            row = self.createSprite('createRows', self.rows, gr, self.kr[r % len(self.kr)], xr, yyr, wr, hr, r, 0, v=v, dbg=dbg)
            if self.n[C]: self.createCols(row, v)

    def createCols(self, row, v, dbg=1):
        nc, ic, xc, yc, wc, hc, oc, gc = self.geom(C, row.x, row.y, row.width, row.height, why='', init=True, dump=0)
        for c in range(nc):
            xxc, yyc = row.x + xc + (wc + xc) * c, row.y + row.height - (hc + yc)
            self.createSprite('createCols', self.cols, gc, self.kc[self.cci(c, self.kc)], xxc, yyc, wc, hc, c, 0, v=v, dbg=dbg)
########################################################################################################################################################################################################
    def createSprites(self, dbg=1):
        log('createSprites(BGN) n={}'.format(self.n))
        if dbg: self.dumpSprite()
        cp, cl, cq, cr, cc = self.kp, self.kl, self.kq, self.kr, self.kc
#        cp, cl, cq, cr, cc = [REDS[0], REDS[2], REDS[4], REDS[6], REDS[8], REDS[10]], [GREENS[0], GREENS[2]], [CYANS[0], CYANS[5]], [YELLOWS[0], YELLOWS[3]], [GRAYS[11], GRAYS[7]]
        np, ip, xp, yp, wp, hp, op, gp = self.geom(P, self.x[P], self.y[P], self.ww, self.hh, why='', init=True, dump=0)
        for p in range(np):
            page = self.createSprite('createPages', self.pages, gp, cp[p % len(cp)], xp, yp, wp, hp, p, 0, dbg=dbg)
            v = True if len(self.pages) == 1 else False
            nl, il, xl, yl, wl, hl, ol, gl = self.geom(L, page.x, page.y, page.width, page.height, why='', init=True, dump=0)
            for l in range(nl):
                yyl = page.y + page.height - (hl+yl)*(l+1)
                line = self.createSprite('createLines', self.lines, gl, cl[l % len(cl)], xl, yyl, wl, hl, l, 0, v=v, dbg=dbg)
                if self.n[Q]:
                    nq, iq, xq, yq, wq, hq, oq, gq = self.geom(Q, line.x, line.y, line.width, line.height, why='', init=True, dump=0, dbg=0)
                    for q in range(nq):
                        yyq = line.y + line.height - (hq+yq)*(q+1)
                        qrow = self.createSprite('createQRow', self.qrows, gq, cq[0], xq, yyq, wq, hq, 0, 0, v=v, dbg=dbg)
                        nc, ic, xc, yc, wc, hc, oc, gc = self.geom(C, qrow.x, qrow.y, qrow.width, qrow.height, why='', init=True, dump=0)
                        for c in range(nc):
                            xxc, yyc = qrow.x+xc+(wc+xc)*c, qrow.y+qrow.height-(hc+yc)
                            self.createSprite('createCols', self.cols, gc, cc[self.cci(c, cc)], xxc, yyc, wc, hc, c, 0, v=v, dbg=dbg)
                nr, ir, xr, yr, wr, hr, o, gr = self.geom(R, line.x, line.y, line.width, line.height, why='', init=True, dump=0, dbg=0)
                rr = 1 if self.n[Q] else 0
                for r in range(rr, nr):
                    yyr = line.y + line.height - (hr+yr)*(r+1)
                    row = self.createSprite('createRows', self.rows, gr, cr[r % len(cr)], xr, yyr, wr, hr, r, 0, v=v, dbg=dbg)
                    nc, ic, xc, yc, wc, hc, oc, gc = self.geom(C, row.x, row.y, row.width, row.height, why='', init=True, dump=0)
                    for c in range(nc):
                        xxc, yyc = row.x + xc + (wc+xc)*c, row.y + row.height - (hc+yc)
                        self.createSprite('createCols', self.cols, gc, cc[self.cci(c, cc)], xxc, yyc, wc, hc, c, 0, v=v, dbg=dbg)
        if dbg: self.dumpSprite()
        log('createSprites(END) n={}'.format(self.n))

    def createSprite(self, why, ps, grp, cc, x, y, w, h, i, j=0, v=None, dbg=1):
        scip = pyglet.image.SolidColorImagePattern(cc)
        img = scip.create_image(width=fri(w), height=fri(h))
        spr = pyglet.sprite.Sprite(img, x, y, batch=self.batch, group=grp, subpixel=SUBPIX)
        spr.visible = v if v is not None else True if i==P else False
        spr.color, spr.opacity = cc[:3], cc[3]
        self.sprites.append(spr)
        if ps is not None: ps.append(spr)
        if TEST: return
        p, l, q, r, c = self.lnl()
        if dbg: why += ' j={}'.format(j)  ;  self.dumpSprite(spr, len(self.sprites), '{:2} {:2} {:2} {:3} {:5} {:16}'.format(p, l, q, r, c, why))
        return spr
########################################################################################################################################################################################################
    def resizeSprites(self, dbg=0):
        n = self.n
        log('resizeSprites(BGN) n={}'.format(n))
        if dbg: self.dumpSprite()
        i, sp, sl, sq, sr, sc = 0, 0, 0, 0, 0, 0
        np, ip, xp, yp, wp, hp, op, gp, mxp, myp = self.geom(P, self.x[P], self.y[P], self.ww, self.hh, why='', init=False, dump=0)
        for p in range(np):
            page = self.pages[sp]  ;  page.update(x=xp, y=yp, scale_x=mxp, scale_y=myp)  ;  sp += 1
            if dbg: self.dumpSprite(self.sprites[i], i+1, '{:2} {:2} {:2} {:3} {:5} {:16}'.format(sp, sl, sq, sr, sc, 'resizePages')) ; i += 1
            nl, il, xl, yl, wl, hl, ol, gl, mxl, myl = self.geom(L, page.x, page.y, page.width, page.height, why='', init=False, dump=0)
            for l in range (nl):
                yyl = page.y + page.height - (hl + yl)*(l + 1)
                line = self.lines[sl]  ;  line.update(x=xl, y=yyl, scale_x=mxl, scale_y=myl)  ;  sl += 1
                if dbg: self.dumpSprite(self.sprites[i], i+1, '{:2} {:2} {:2} {:3} {:5} {:16}'.format(sp, sl, sq, sr, sc, 'resizeLines')) ; i += 1
                if n[Q]:
                    nq, iq, xq, yq, wq, hq, oq, gq, mxq, myq = self.geom(Q, line.x, line.y, line.width, line.height, why='', init=False, dump=0)
                    for q in range(nq):
                        yyq = line.y + line.height - (hq + yq)*(q + 1)
                        qrow = self.qrows[sq]  ;  qrow.update(x=xq, y=yyq, scale_x=mxq, scale_y=myq)  ;  sq += 1
                        if dbg: self.dumpSprite(self.sprites[i], i+1, '{:2} {:2} {:2} {:3} {:5} {:16}'.format(sp, sl, sq, sr, sc, 'resizeQRows')) ; i += 1
                        nc, ic, xc, yc, wc, hc, oc, gc, mxc, myc = self.geom(C, qrow.x, qrow.y, qrow.width, qrow.height, why='', init=False, dump=0)
                        for c in range(nc):
                            xxc, yyc = qrow.x + xc + (wc + xc)*c, qrow.y + qrow.height - (hc + yc)
                            self.cols[sc].update(x=xxc, y=yyc, scale_x=mxc, scale_y=myc)  ;  sc += 1
                            if dbg: self.dumpSprite(self.sprites[i], i+1, '{:2} {:2} {:2} {:3} {:5} {:16}'.format(sp, sl, sq, sr, sc, 'resizeCols')) ; i += 1
                nr, ir, xr, yr, wr, hr, o, gr, mxr, myr = self.geom(R, line.x, line.y, line.width, line.height, why='', init=False, dump=0)
                rr = 1 if n[Q] else 0
                for r in range(rr, nr):
                    yyr = line.y + line.height - (hr + yr)*(r + 1)
                    row = self.rows[sr]  ;  row.update(x=xr, y=yyr, scale_x=mxr, scale_y=myr)  ;  sr += 1
                    if dbg: self.dumpSprite(self.sprites[i], i+1, '{:2} {:2} {:2} {:3} {:5} {:16}'.format(sp, sl, sq, sr, sc, 'resizeRows')) ; i += 1
                    nc, ic, xc, yc, wc, hc, oc, gc, mxc, myc = self.geom(C, row.x, row.y, row.width, row.height, why='', init=False, dump=0)
                    for c in range(nc):
                        xxc, yyc = row.x + xc + (wc + xc)*c, row.y + row.height - (hc + yc)
                        self.cols[sc].update(x=xxc, y=yyc, scale_x=mxc, scale_y=myc)  ;  sc += 1
                        if dbg: self.dumpSprite(self.sprites[i], i+1, '{:2} {:2} {:2} {:3} {:5} {:16}'.format(sp, sl, sq, sr, sc, 'resizeCols')) ; i += 1
        if dbg: self.dumpSprite()
        log('resizeSprites(END) n={}'.format(n))
########################################################################################################################################################################################################
    def dumpSprites(self, why=''):
        n = self.n
        log('dumpSprites(BGN) n={} {}'.format(n, why))
        self.dumpSprite()
        i, sp, sl, sq, sr, sc = 0, 0, 0, 0, 0, 0
        for p in range(n[P]):
            sp += 1             ; self.dumpSprite(self.sprites[i], i+1, '{:2} {:2} {:2} {:3} {:4}  {:16}'.format(sp, sl, sq, sr, sc, why)) ; i += 1
            for l in range(n[L]):
                sl += 1         ; self.dumpSprite(self.sprites[i], i+1, '{:2} {:2} {:2} {:3} {:4}  {:16}'.format(sp, sl, sq, sr, sc, why)) ; i += 1
                for q in range(n[Q]):
                    sq += 1     ; self.dumpSprite(self.sprites[i], i+1, '{:2} {:2} {:2} {:3} {:4}  {:16}'.format(sp, sl, sq, sr, sc, why)) ; i += 1
                    for c in range(n[K]):
                        sc += 1 ; self.dumpSprite(self.sprites[i], i+1, '{:2} {:2} {:2} {:3} {:4}  {:16}'.format(sp, sl, sq, sr, sc, why)) ; i += 1
                for r in range(n[R]):
                    sr += 1     ; self.dumpSprite(self.sprites[i], i+1, '{:2} {:2} {:2} {:3} {:4}  {:16}'.format(sp, sl, sq, sr, sc, why)) ; i += 1
                    for c in range(n[K]):
                        sc += 1 ; self.dumpSprite(self.sprites[i], i+1, '{:2} {:2} {:2} {:3} {:4}  {:16}'.format(sp, sl, sq, sr, sc, why)) ; i += 1
        self.dumpSprite()
        log('dumpSprites(END) n={} {}'.format(n, why))

    @staticmethod
    def dumpSprite(s=None, c=-1, why=''):
        if s is None: log(' sid   p  l  q   r  col     why               x      xc        y      yc        w       h    iax  iay    m      mx     my     rot   red green blue opc vsb    group       parent', ind=0); return
        f = '{:5} {:16} {:7.2f} {:7.2f}  {:7.2f} {:7.2f}  {:7.2f} {:7.2f} {:4} {:4} {:6.3f} {:6.3f} {:6.3f} {:7.2f}  {:3}  {:3}  {:3}  {:3}  {:1}  {} {}'
        k, o, v, g, p = s.color, s.opacity, s.visible, s.group, s.group.parent
        xc, yc = s.x + s.width/2, s.y + s.height/2
        fs = f.format(c, why, s.x, xc, s.y, yc, s.width, s.height, s.image.anchor_x, s.image.anchor_y, s.scale, s.scale_x, s.scale_y, s.rotation, k[0], k[1], k[2], o, v, g, p)
        log('{}'.format(fs), ind=0)
        assert(type(s) == pyglet.sprite.Sprite)
########################################################################################################################################################################################################
    def createCursor(self, g):
        c = self.cursorCol()
        x, y, w, h = self.cols[c].x, self.cols[c].y, self.cols[c].width, self.cols[c].height
        self.dumpSprite()
        self.cursor = self.createSprite('cursor', None, g, CC, x, y, w, h, 0, 0, v=True)
        log('createCursor()   c={:4} x={:6.1f} y={:6.1f} w={:4} h={:4} i={}'.format(c, x, y, w, h, self.i))

    def resizeCursor(self):
        c = self.cursorCol()
        x, y, w, h = self.cols[c].x, self.cols[c].y, self.cols[c].width, self.cols[c].height
        self.cursor.update(x=x, y=y, scale_x=self.cols[c].scale_x, scale_y=self.cols[c].scale_y)
        log('resizeCursor()   c={:4} x={:6.1f} y={:6.1f} w={:6.2f} h={:6.2f} i={}'.format(c, x, y, w, h, self.i))

    def cursorCol(self, dbg=1):
        p, l, _, r, c = self.i#  ;  q = self.n[Q]*(l+1)
        cpp, cpl, cpr = self.cps()
        cc = p*cpp + l*cpl + r*cpr + c
        if dbg: log('cursorCol() cc = ({}*{} + {}*{} + {}*{} + {}) = ({} + {} + {} + {}) = {}'.format(p, cpp, l, cpl, r, cpr, c, p*cpp, l*cpl, r*cpr, c, cc))
        return cc

    def whMin(self):
        c = self.cursorCol()  ;  w = self.cols[c].width  ;  h = self.cols[c].height  ;  m = min(w, h)
        log('whMin() c={:3} w={:5.1f} h={:5.1f} m={:5.1f}'.format(c, w, h, m))
        return m

    def resizeFonts(self):
        whMin = self.whMin()  ;  m = self.m
        ni = 5 if whMin > m else -5 if whMin < m else 0
        log('resizeFonts() ni={} m={:5.1f} whMin={:5.1f}'.format(ni, m, whMin))
        self.m += ni
        self.updateFontSize(ni)
########################################################################################################################################################################################################
    def createLabels(self, g, dbg=1):
        lid, text = 0, ['R', 'M', '@']
        [text.append('{}'.format(_)) for _ in range(1, self.n[C] + 1)]
        self.dumpTextList(text, 'createLabels(BGN)) text')
        if dbg: log('createLabels() n={} len(labels)={}'.format(self.n, len(self.labels)))
        self.deleteList(self.labels)
        for q in range(len(self.qrows)):
            if dbg: self.dumpLabel()
            for c in range(len(text)):
                qc = c + q*self.cpl
                tc = c + q*self.cpr
                l = self.createLabel(self.labels, text[c], qc, g)
                if dbg: self.dumpLabel(l, tc, q, qc, 'createLabels')
        if dbg: self.dumpLabel()
        self.dumpTextList(text, 'createLabels(END)) text')

    def createLabel(self, l, text, c, g):
        w, h, ac, ab, b, m = self.cols[c].width, self.cols[c].height, 'center', 'center', self.batch, True
        k, d, s, n, o, j = self.fontInfo()
        k = FONT_COLORS[-1]
        x, y, = self.cols[c].x + w/2, self.cols[c].y + h/2
        for i in range(len(text), 0, -1): text = text[:i] + '\n' + text[i:]
        label = pyglet.text.Label(text, font_name=n, font_size=s, bold=o, italic=j, color=k, x=x, y=y, width=w, height=h, anchor_x=ac, anchor_y=ab, align=ac, dpi=d, batch=b, group=g, multiline=m)
        l.append(label)
        return label

    def createTabs(self, g, dbg=1):
        n = self.n  ;  nt = len(self.tabs)
        log('createTabs(BGN) n={} nt={}'.format(n, nt))
        self.deleteList(self.tabs)
#        if dbg: self.dumpTab()
        if dbg: self.dumpData(self.data, why='createTabs')
        for l in range(n[L]):
            for c in range(n[K]):
                cc = c + l * self.cpr
                col = self.data[l][cc] if cc < len(self.data[l]) else BLANK_COL
                for r in range(n[R]):
                    rc = c + (r + n[Q])*self.cpr + l * self.cpl
                    tc = c + r*self.cpr
#                    if dbg: log('createTabs() l={} r={:2} c={:3} rc={:4} tc={:4} cc={:4}'.format(l, r, c, rc, tc, cc), end=' ')
                    t = self.createTab(self.tabs, col[r], rc, g)
                    if dbg: self.dumpTab(t, tc, r, rc, 'createTabs')
        if dbg: self.dumpTabs(why='createTabs')
        log('createTabs(END) n={} nt={}'.format(n, nt))

    def createTab(self, t, text, c, g):
        w, h, ac, ab, b = self.cols[c].width, self.cols[c].height, 'center', 'center', self.batch
        k, d, s, n, o, j = self.fontInfo()
        x, y, = self.cols[c].x + w/2, self.cols[c].y + h/2
        tab = pyglet.text.Label(text, font_name=n, font_size=s, bold=o, italic=j, color=k, x=x, y=y, width=w, height=h, anchor_x=ac, anchor_y=ab, align=ac, dpi=d, batch=b, group=g)
        t.append(tab)
        return tab
########################################################################################################################################################################################################
    def resizeLabels(self, dbg=0):
        cpp, cpl, cpr = self.cps()
        lnl = self.lnl()
        log('resizeLabels(BGN) lnl={} cpp={} cpl={} cpr={}'.format(lnl, cpp, cpl, cpr))
        for l in range(self.n[L]):
            for c in range(cpr):
                self.resizeLabel(self.labels[c + l*cpr], c + l*cpl)
        if dbg: self.dumpLabels('resizeLabels')
        log('resizeLabels(END) lnl={} cpp={} cpl={} cpr={}'.format(lnl, cpp, cpl, cpr))

    def resizeLabel(self, l, c):
        w, h = self.cols[c].width, self.cols[c].height
        x, y = self.cols[c].x + w/2, self.cols[c].y + h/2
        l.x, l.y, l.width, l.height = x, y, w, h

    def resizeTabs(self, dbg=0):
        n = self.n  ;  i = 0
        log('resizeTabs(BGN) n={} cps={}'.format(n, self.cps()))
        for l in range(n[L]):
            for c in range(n[K]):
                for r in range(n[R]):
                    t = c + (r + n[Q]) * self.cpr + l * self.cpl
                    self.resizeTab(self.tabs[i], t)
                    i += 1
        if dbg: self.dumpTabs('resizeTabs')
        log('resizeTabs(END) n={} cps={}'.format(n, self.cps()))

    def resizeTab(self, t, c):
        w, h = self.cols[c].width, self.cols[c].height
        x, y = self.cols[c].x + w/2, self.cols[c].y + h/2
        t.x, t.y,t.width, t.height = x, y, w, h
########################################################################################################################################################################################################
    def dumpLabels(self, why='', dbg=1):
        cpp, cpl, cpr = self.cps()
        nq = len(self.qrows)
        if dbg: log('dumpLabels(BGN) nq={} {}'.format(nq, why))
        self.dumpLabel()
        for q in range(nq):
            for c in range(cpr):
                self.dumpLabel(self.labels[c+q*cpr], c+q*cpr, q, c+q*cpl, why)
        self.dumpLabel()
        if dbg: log('dumpLabels(END) nq={} {})'.format(nq, why))

    @staticmethod
    def dumpLabel(l=None, lid=-1, q=-1, c=-1, why=''):
        if l is None: log('lid  q   c  text     x       y       w       h      font name      size dpi bold ital red green blue opc  why', ind=0) ; return
        x, y, w, h, n, d, s, k, b, i, t = l.x, l.y, l.width, l.height, l.font_name, l.dpi, l.font_size, l.color, l.bold, l.italic, l.text
        log('{:3} {:2} {:4}  {:3} {:7.2f} {:7.2f} {:7.2f} {:7.2f}  {:16}  {:2}  {:3}   {:1}    {:1}  {:3}  {:3}  {:3}  {:3}  {}'.format(lid, q, c, t, x, y, w, h, n, s, d, b, i, k[0], k[1], k[2], k[3], why), ind=0)

    def dumpTabs(self, why='', dbg=1):
        n = self.n  ;  i = 0  ;  why = '{:16}'.format(why)
        if dbg: log('dumpTabs(BGN) n={} {}'.format(n, why))
        self.dumpTab()
        for l in range(n[L]):
            for c in range(n[K]):
                for r in range(n[R]):
                    rc = c + (r + n[Q])*self.cpr
                    why2 = ' {:5} {:4} {:2} {:3} {:3} {:1}'.format(i, c, r, rc, len(self.data[l]), len(self.data[l][c]))
                    self.dumpTab(self.tabs[i], i, r, rc, why + why2)
                    i += 1
        self.dumpTab()
        if dbg: log('dumpTabs(END) n={} {}'.format(n, why))

    @staticmethod
    def dumpTab(t=None, tid=-1, r=-1, c=-1, why=''):
        if t is None: log('tid  r   c  text     x       y       w       h      font name      size dpi bold ital red green blue opc  why                 i    c   r  rc  ', ind=0) ; return
        x, y, w, h, n, d, s, k, b, i, tt = t.x, t.y, t.width, t.height, t.font_name, t.dpi, t.font_size, t.color, t.bold, t.italic, t.text
        log('{:3} {:2} {:4}  {:3} {:7.2f} {:7.2f} {:7.2f} {:7.2f}  {:16}  {:2}  {:3}   {:1}    {:1}  {:3}  {:3}  {:3}  {:3}  {}'.format(tid, r, c, tt, x, y, w, h, n, s, d, b, i, k[0], k[1], k[2], k[3], why), ind=0)
########################################################################################################################################################################################################
    def dumpTest(self, why=''):
        self.dumpFont('{}'.format(why))
        self.dumpSprite()
#        for i in range(len(self.colorLists)):
#            self.dumpSprites(self.colorLists[i], why)

    def dumpStruct(self, why=''):
        log('dumpStruct(BGN) {}'.format(why))
#        self.dumpSprites(why)
#        self.dumpLabels(why)
#        self.dumpData(why=why)
#        self.dumpTabs(why)
        self.dumpFont(why)
        self.dumpNums(why)
        self.cursorCol(dbg=1)
        log('dumpStruct(END) {}'.format(why))
########################################################################################################################################################################################################
    def dumpNums(self, why=''):
        n = self.n  ;  i = self.i  ;  lnl = self.lnl()  ;  cps = self.cps()
        log('dumpNums() {} n={}  i={} lnl={}  cps={}'.format(why, n, i, lnl, cps))

    @staticmethod
    def dumpTextList(text, why=''):
        log('{}[len={}] = [ '.format(why, len(text)), end='')
        for i in range(len(text)): log('{}'.format(text[i]), ind=0, end=' ')
        log(']', ind=0)
########################################################################################################################################################################################################
    def on_resize(self, width, height):
        stackInfo(1)
        super().on_resize(width, height)
        self.ww, self.hh = width, height
        if TEST: self.resizeTestColors()  ;  return
        log('on_resize(BGN) {:4} x {:4}'.format(self.ww, self.hh))
        self.resizeFonts()
        self.resizeSprites()
        if self.n[Q]: self.resizeLabels()
        self.resizeTabs()
        self.resizeCursor()
        self.snapshot()
#        self.dumpStruct('on_resize()')
#        self.updateCaption()
        log('on_resize(END) {:4} x {:4}'.format(self.ww, self.hh))
########################################################################################################################################################################################################
    def on_draw(self):
        self.clear()
        self.batch.draw()

    def kpEvntTxt(self):
        return 'kbk={:6} symb={:6} symbStr={:12} mods={} modsStr={:26}'.format(self.kbk, self.symb, self.symbStr, self.mods, self.modsStr)

    def on_key_press(self, symb, mods):
        self.symb, self.mods, self.symbStr, self.modsStr = symb, mods, pygwink.symbol_string(symb), pygwink.modifiers_string(mods)
        self.kbk = self.symbStr  ;  kbk = self.kbk
        log('on_key_press(BGN)     {}'.format(self.kpEvntTxt()))
        if                  self.isTab(kbk):                          self.addTab(kbk, 'on_key_press')
        elif kbk == 'Q' and self.isCtrl(mods) and self.isShift(mods): self.quit('keyPress({})'.format(kbk))
        elif kbk == 'Q' and self.isCtrl(mods):                        self.quit('keyPress({})'.format(kbk))
        elif kbk == 'C' and self.isCtrl(mods) and self.isShift(mods): self.updateFontColor( 1)
        elif kbk == 'C' and self.isCtrl(mods):                        self.updateFontColor(-1)
        elif kbk == 'D' and self.isCtrl(mods) and self.isShift(mods): self.updateFontDpi(   1)
        elif kbk == 'D' and self.isCtrl(mods):                        self.updateFontDpi(  -1)
        elif kbk == 'N' and self.isCtrl(mods) and self.isShift(mods): self.updateFontName(  1)
        elif kbk == 'N' and self.isCtrl(mods):                        self.updateFontName( -1)
        elif kbk == 'S' and self.isCtrl(mods) and self.isShift(mods): self.updateFontSize(  1)
        elif kbk == 'S' and self.isCtrl(mods):                        self.updateFontSize( -1)
        elif kbk == 'B' and self.isCtrl(mods) and self.isShift(mods): self.toggleFontBold()
        elif kbk == 'B' and self.isCtrl(mods):                        self.toggleFontBold()
        elif kbk == 'I' and self.isCtrl(mods) and self.isShift(mods): self.toggleFontItalic()
        elif kbk == 'I' and self.isCtrl(mods):                        self.toggleFontItalic()
#        self.updateCaption()
        log('on_key_press(END)     {}'.format(self.kpEvntTxt()))

    def on_text(self, text):
        self.kbk = text
        log('on_text(BGN)          {}'.format( self.kpEvntTxt()))
        if self.isTab(self.kbk):                 self.addTab(self.kbk, 'on_text')
        if self.kbk=='$' and self.isShift(self.mods): self.snapshot()
#        self.updateCaption()
        log('on_text(END)          {}'.format( self.kpEvntTxt()))

    def on_text_motion(self, motion):
        self.kbk = motion
        log('on_text_motion(BGN)   {}'.format(self.kpEvntTxt()))
        if self.mods == 0:
            if   motion==pygwink.MOTION_LEFT:          self.move(-1)
            elif motion==pygwink.MOTION_RIGHT:         self.move( 1)
            elif motion==pygwink.MOTION_UP:            self.move(-self.n[K])
            elif motion==pygwink.MOTION_DOWN:          self.move( self.n[K])
#            elif motion==pygwink.MOTION_PREVIOUS_PAGE: self.move() # prevPage(self.i[P], motion)
#            elif motion==pygwink.MOTION_NEXT_PAGE:     self.move() # nextPage(self.i[P], motion)
            else:                                      log('on_text_motion() motion={} ???'.format(motion))
#            self.updateCaption()
        log('on_text_motion(END)   {}'.format(self.kpEvntTxt()))
########################################################################################################################################################################################################
    def move(self, c, dbg=1):
        i, cc = self.i, self.cursorCol()
        self.i[C] = (i[C] + c) % self.cpp
        kk = (cc + c) % self.cpp
        log(        'move({:4}) i={} cc={:3} => i={} cc={:3}'.format(c, i, cc, self.i, kk))
        if dbg: log('move({:4}) i={} cc={:3} => i={} cc={:3}'.format(c, i, cc, self.i, kk))
        self.cursor.update(x=self.cols[kk].x, y=self.cols[kk].y)

    def nextPage(self, i, motion):
        self.pages[i].visible = False
        self.updatePage(i+1, 'nextPage() {}=MOTION_NEXT_PAGE   '.format(motion))

    def prevPage(self, i, motion):
        self.pages[i].visible = False
        self.updatePage(i-1, 'prevPage() {}=MOTION_PREVIOUS_PAGE'.format(motion))

    def updatePage(self, i, why):
        i = i % self.n[P]
        self.pages[i].visible = True
        log('{} i[{}]={}'.format(why, P, i))
        self.i[P] = i
########################################################################################################################################################################################################
    def addTab(self, kbk, why=''):
        cc = self.cursorCol()
        log('addTab(BGN)           {} : cc={} {}'.format(self.kpEvntTxt(), cc, why))
        self.updateData(kbk, cc)
        self.updateTab( kbk, cc)
        self.snapshot()
        log('addTab(END)           {} : cc={} {}'.format(self.kpEvntTxt(), cc, why))

    def on_mouse_release(self, x, y, button, modifiers):  # pyglet.window.mouse.MIDDLE #pyglet.window.mouse.LEFT #pyglet.window.mouse.RIGHT
        stackInfo(1)
        n = self.n  ;  np, nl, nq, nr, nc, nk = n
#        i = self.i  ;  ip, il, iq, ir, ic     = i
        cc = self.cursorCol()  ;  cpp, cpl, cpr = self.cps()
        w = self.ww/nk  ;  h = self.hh/((nr + nq)*nl)   ;  y = self.hh - y
        c = int(x/w)    ;  r = int(y/h)
        k = self.i[P]*cpp + self.i[L]*cpl + self.i[R]*cpr + self.i[C]
        log('on_mouse_release(BGN) b={} m={} n={} x={:4} y={:4} w={:6.2f} h={:6.2f} i={} c={:4} r={:4} k={:4} cc={:4}'.format(button, modifiers, n, x, y, w, h, self.i, c, r, k, cc))
        self.i[C] = c  ;  self.i[L] = r//(nq + nr)  ;  self.i[R] = r % (nq + nr)
        k = self.i[P]*cpp + self.i[L]*cpl + self.i[R]*cpr + self.i[C]
        self.cursor.update(self.cols[k].x, self.cols[k].y)
        cc = self.cursorCol(dbg=0)
        log('on_mouse_release(END) b={} m={} n={} x={:4} y={:4} w={:6.2f} h={:6.2f} i={} c={:4} r={:4} k={:4} cc={:4}'.format(button, modifiers, n, x, y, w, h, self.i, c, r, k, cc))

    def updateData(self, text, cc, dbg=0):
        c, s = self.cs(cc)
        t = self.data[c]
        if dbg: self.dumpData(self.data, why='updateData(BGN) text={} c={} s={} data[c]={}'.format(text, c, s, self.data[c]))
        self.data[c] = t[0:s] + text + t[s+1:]
        if dbg: self.dumpData(self.data, why='updateData(END) text={} c={} s={} data[c]={}'.format(text, c, s, self.data[c]))

    def updateTab(self, text, cc):
        c, s = self.cs(cc)
        t = c * self.n[R] + s
        log('updateTab(BGN) text={} c={} s={} t={} tabs[t].text={}'.format(text, c, s, t, self.tabs[t].text), file=sys.stdout)
        self.tabs[t].text = text  ;  self.tabs[t].color = FONT_COLORS[1]
        log('updateTab(END) text={} c={} s={} t={} tabs[t].text={}'.format(text, c, s, t, self.tabs[t].text), file=sys.stdout)

    def updateCaption(self):
        fc, fd, fs, fn, fb, fi = self.fontInfo()
        text = '{}dpi {}pt {} {},{},{},{}'.format(fd, fs, fn, fc[0], fc[1], fc[2], fc[3])
        log('updateCaption() {}'.format(text))
        self.set_caption(text)
########################################################################################################################################################################################################
    def cs(self, cc): nk, nr, nq = self.n[K], self.n[R], self.n[Q]  ;  return cc % nk + ((cc//nk)//(nq + nr))*nk, ((cc//nk) - nq*(1 + cc//self.cpl)) % nr
    def cps(self): return self.cpp, self.cpl, self.cpr
    def lnl(self): return list(map(len, [self.pages, self.lines, self.qrows, self.rows, self.cols]))

    def cci(self, c, cc):
        if c == 0: self.ci = (self.ci + 1) % len(cc)
        return (c + self.ci) % len(cc)

    @staticmethod
    def ordSfx(n):
        m = n % 10
        if   m == 1 and n != 11: return 'st'
        elif m == 2 and n != 12: return 'nd'
        elif m == 3 and n != 13: return 'rd'
        else:                    return 'th'

    @staticmethod
    def deleteList(l):
        i = 0
        while i < len(l): t = l[i];  t.delete();  del l[i]
########################################################################################################################################################################################################
    def dumpFont(self, why=''):
        fc, dpi, fs, fn, fb, fi = self.fontInfo()
        pix = FONT_SCALE*fs/dpi
        log('dumpFont({}) {} {}DPI {}pt {} ({:6.3f}*{}pt/{}DPI)={:6.3f}pixels'.format(why, fc, dpi, fs, fn, FONT_SCALE, fs, dpi, pix))

    def fontInfo(self): return FONT_COLORS[self.fontColorIndex], FONT_DPIS[self.fontDpiIndex], FONT_SIZES[self.fontSizeIndex], FONT_NAMES[self.fontNameIndex], self.fontBold, self.fontItalic
    def updateFontColor(self, ii): self.fontColorIndex = self.updateFontIndex(ii, self.fontColorIndex, FONT_COLORS, 'FONT_COLORS')
    def updateFontDpi(  self, ii): self.fontDpiIndex   = self.updateFontIndex(ii, self.fontDpiIndex,   FONT_DPIS,   'FONT_DPIS')
    def updateFontName( self, ii): self.fontNameIndex  = self.updateFontIndex(ii, self.fontNameIndex,  FONT_NAMES,  'FONT_NAMES')
    def updateFontSize( self, ii): self.fontSizeIndex  = self.updateFontIndex(ii, self.fontSizeIndex,  FONT_SIZES,  'FONT_SIZES')

    def updateFontIndex(self, ii, index, prop, name):
        i = (index + ii) % len(prop)
        log('updateFontIndex({:2})   {} {}[{}]={}'.format(ii, self.kpEvntTxt(), name, i, prop[i]))
        self.createTabs(self.g[C+1])
        if self.n[Q]: self.createLabels(self.g[C+2])
        return i

    def toggleFontBold(self):
        log('toggleFontBold() {:1} => {:1}'.format(self.fontBold, not self.fontBold))
        self.fontBold = not self.fontBold
        for j in range(len(self.tabs)):
            self.tabs[j].bold = self.fontBold
        if self.n[Q]:
            for j in range(len(self.labels)):
                self.labels[j].bold = self.fontBold

    def toggleFontItalic(self):
        log('toggleFontItalic() {:1} => {:1}'.format(self.fontItalic, not self.fontItalic))
        self.fontItalic = not self.fontItalic
        for j in range(len(self.tabs)):
            self.tabs[j].italic = self.fontItalic
        if self.n[Q]:
            for j in range(len(self.labels)):
                self.labels[j].italic = self.fontItalic
########################################################################################################################################################################################################
    def toggleColorLists(self, motion):
        if not TEST: log('toggleColorLists(WARNING) Nothing To Toggle TEST={} motion={}'.format(TEST, motion)) ; return
        cls = self.colorLists
        i = self.i[P]
        log('toggleColorLists() i={}'.format(i))
        if motion==pygwink.MOTION_LEFT:
            for j in range(len(cls[i])): cls[i][j].visible = False
            i -= 1
            i = i % len(COLORS)
            for j in range(len(cls[i])): cls[i][j].visible = True
            log('toggleColorLists() MOTION_LEFT={} i[P]={} len(cls)={}'.format(motion, i, len(cls)))
        elif motion==pygwink.MOTION_RIGHT:
            for j in range(len(cls[i])): cls[i][j].visible = False
            i += 1
            i = i % len(COLORS)
            for j in range(len(cls[i])): cls[i][j].visible = True
            log('toggleColorLists() MOTION_RIGHT={} i[P]={} len(cls)={}'.format(motion, i, len(cls)))
        self.i[P] = i
########################################################################################################################################################################################################
    @staticmethod
    def isCtrl(mods):        return mods&pygwink.MOD_CTRL
    @staticmethod
    def isShift(mods):       return mods&pygwink.MOD_SHIFT
    @staticmethod
    def isAlt(mods):         return mods&pygwink.MOD_ALT

    @staticmethod
    def isTab(text):
        return True if      text=='-' or Tabs.isFret(text) else False
    @staticmethod
    def isFret(text):
        return True if '0'<=text<='9' or 'a'<=text<='o'    else False

    def snapshot(self):
        SNAP_DIR  = 'snaps'
        SNAP_SFX  = '.png'
        SNAP_ID   = '.{}'.format(self.ssi)
        SNAP_NAME = BASE_NAME + SFX + SNAP_ID + SNAP_SFX
        SNAP_PATH = BASE_PATH / SNAP_DIR / SNAP_NAME
        pyglet.image.get_buffer_manager().get_color_buffer().save('{}'.format(SNAP_PATH))
        log('snapshot() SNAP_PATH={}'.format(SNAP_PATH))
        self.ssi += 1

    def quit(self, why=''):
        text = '###   Quit   ###' * 13
        log('\n{}\n'.format(text))
        self.dumpStruct('quit ' + why) if not TEST else self.dumpTest('quit() ' + why)
        log('quit() {}\nExiting'.format(why))
        self.snapshot()
        stackInfo(1)
        exit()
########################################################################################################################################################################################################
if __name__=='__main__':
    TEST = 0  ;  CARET = 0  ;  ORDER_GROUP = 1  ;  SUBPIX = 1  ;  FULL_SCREEN = 0  ;  VRSN = 1
    SFX           = '.TEST' if TEST else '.' + chr(65 + VRSN)
    PATH          = pathlib.Path(sys.argv[0])
    BASE_PATH     = PATH.parent
    BASE_NAME     = BASE_PATH.stem
    LOG_DIR       = 'logs'  ;         LOG_SFX       = '.log'
    LOG_NAME      = BASE_NAME + SFX + LOG_SFX
    LOG_PATH      = BASE_PATH / LOG_DIR / LOG_NAME
    LOG_FILE      = open(str(LOG_PATH), 'w')
    DATA_DIR      = 'data'  ;         DATA_SFX      = '.dat'
    DATA_NAME     = BASE_NAME + SFX + DATA_SFX
    DATA_PATH     = BASE_PATH / DATA_DIR / DATA_NAME
    DATA_FILE     = open(str(DATA_PATH), 'r')
    P, L, Q, R, C, K = 0, 1, 2, 3, 4, 5
    OPACITY       = [255, 240, 225, 210, 190, 165, 140, 110, 80]
    GRAY          = [(255, 255, 255, OPACITY[0]), ( 0,  0,  0, OPACITY[0])]
    PINK          = [(255,  64, 192, OPACITY[0]), (57, 16, 16, OPACITY[0])]
    INFRA_RED     = [(255,  29,  24, OPACITY[0]), (68, 20, 19, OPACITY[0])]
    RED           = [(255,  24,  21, OPACITY[0]), (82, 15, 12, OPACITY[0])]
    ORANGE        = [(255, 128,  32, OPACITY[0]), (76, 30, 25, OPACITY[0])]
    YELLOW        = [(255, 255,  15, OPACITY[0]), (45, 41, 10, OPACITY[0])]
    GREEN         = [( 44, 255,   0, OPACITY[0]), (21, 54, 10, OPACITY[0])]
    GREEN_BLUE    = [( 24, 255,  61, OPACITY[0]), (10, 49, 25, OPACITY[0])]
    CYAN          = [( 32, 255, 255, OPACITY[0]), (16, 64, 64, OPACITY[0])]
    BLUE_GREEN    = [( 25, 181, 255, OPACITY[0]), (12, 37, 51, OPACITY[0])]
    BLUE          = [( 35,  26, 255, OPACITY[0]), (19, 11, 64, OPACITY[0])]
    ULTRA_VIOLET  = [(176,  81, 255, OPACITY[0]), (44, 14, 58, OPACITY[0])]
    VIOLET        = [(194,  96, 255, OPACITY[3]), (50, 19, 61, OPACITY[1])]
    HUES          = 13
    def fri(f): return int(math.floor(f+0.5))
########################################################################################################################################################################################################
    def stackInfo(c=1):
        si = inspect.stack(c)
        for i, e in enumerate(si):
            log('stackInfo(): {} {:16} {:4} {:16} {} ^{}'.format(i, os.path.basename(e.filename), e.lineno, e.function, e.code_context, stackDepth()))

    def indent(): d = stackDepth() - 4  ;  return '{:{w}}^'.format(d, w=d)
    def stackDepth(): return len(inspect.stack())

    def log(msg='', ind=1, file=LOG_FILE, flush=True, sep=',', end='\n'):
        print('{}{}'.format(indent(), msg), file=file, flush=flush, sep=sep, end=end) if ind else print('{}'.format(msg), file=file, flush=flush, sep=sep, end=end)
        if file != LOG_FILE: log(msg, ind)
########################################################################################################################################################################################################
    def genColors(cp, nsteps=HUES, dbg=0):
        colors, clen = [], len(cp[0])
        diffs = [cp[1][i] - cp[0][i] for i in range(clen)]
        steps = [diffs[i]/nsteps     for i in range(clen)]
        if dbg: log('genColors(), c1={} c2={} nsteps={} diffs={} steps='.format(cp[0], cp[1], nsteps, diffs), end='')  ;  log('[{:6.1f} {:6.1f} {:6.1f} {:6.1f}]'.format(steps[0], steps[1], steps[2], steps[3]))
        for j in range(nsteps):
            c = tuple([fri(cp[0][i] + j * steps[i]) for i in range(len(cp[0]))])
            if dbg: log('genColors() c[{}]={}'.format(j, c))
            colors.append(c)
        if dbg: log('genColors() colors={}'.format(cp))
        return colors
    GRAYS       = genColors(GRAY)
    PINKS       = genColors(PINK)
    INFRA_REDS  = genColors(INFRA_RED)
    REDS        = genColors(RED)
    ORANGES     = genColors(ORANGE)
    YELLOWS     = genColors(YELLOW)
    GREENS      = genColors(GREEN)
    GREEN_BLUES = genColors(GREEN_BLUE)
    CYANS       = genColors(CYAN)
    BLUE_GREENS = genColors(BLUE_GREEN)
    BLUES       = genColors(BLUE)
    ULTRA_VIOLETS = genColors(ULTRA_VIOLET)
    VIOLETS     = genColors(VIOLET)
    COLORS      = (PINKS, INFRA_REDS, REDS, ORANGES, YELLOWS, GRAYS, GREENS, GREEN_BLUES, CYANS, BLUE_GREENS, BLUES, VIOLETS, ULTRA_VIOLETS)
    CC          = (255, 190, 12, 176)
    CCC         = 3
    BLANK_COL   = '------'
    FONT_SCALE  = 123.42857
    FONT_NAMES  = ['Times New Roman', 'Lucida Console', 'Courier New', 'Helvetica', 'Arial', 'Century Gothic', 'Bookman Old Style', 'Antique Olive']
    FONT_SIZES  = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52]
    FONT_COLORS = [REDS[0], GREENS[0], BLUES[0], YELLOWS[0], ORANGES[0], GREEN_BLUES[0], CYANS[0], BLUE_GREENS[0], PINKS[0], INFRA_REDS[0], VIOLETS[0], ULTRA_VIOLETS[0], GRAYS[0]]
    FONT_DPIS    = [75, 80, 90, 96, 100, 108, 116, 124]
    tabs        = Tabs()
    pyglet.app.run()
#        cc = GREENS[-1::-1]+GREENS

#    def dumpSpriteCount(self, why=''):
#        p, l, q, r, c = self.ns()
#        print('dumpSpriteCount({}) p={} lpp={} l={} qpl={} q={} rpl={} r={} cpr={} c={}'.format(why, p, self.n[L], l, self.n[Q], q, self.n[R], r, self.n[C], c))
#        print('dumpSpriteCount({}) p={}   +   l={}   +   q={}   +   r={}   +    c={} = {}'.format(why, p, l, q, r, c, p + l + q + r + c))
    '''
    def resizePages(self, dbg=0):
        n, i, x, y, w, h, o, g, mx, my = self.geom(P, self.x[P], self.y[P], self.ww, self.hh, why='', init=False, dump=0)
        for p in range(n):
            self.pages[p].update(x=x, y=y, scale_x=mx, scale_y=my)
            if DBG or dbg: self.dumpSprite(self.pages[p], p*n, '{:2} {:2} {:2} {:3} {:5} {:16}'.format(ii, pp, ll, qq, rr, cc, 'on_resize Pages'))
            if self.n[P+1] > 0: self.resizeLines(self.pages[p], p, dbg)

    def resizeLines(self, spr, p, q, r, c, dbg=0):
        n, i, x, y, w, h, o, g, mx, my = self.geom(L, spr.x, spr.y, spr.width, spr.height, why='', init=False, dump=0)
        for l in range(n):
            ll, yy = l+p*n, spr.y+spr.height-(h+y)*(l+1)
            self.lines[ll].update(x=x, y=yy, scale_x=mx, scale_y=my)
            if DBG or dbg: self.dumpSprite(self.lines[ll], ll, '{:2} {:2} {:2} {:3} {:5} {:16}'.format(p, ll, q, r, c, 'on_resize Lines'))
            if self.n[L+1] > 0:
                self.resizeQRow(self.lines[ll], p, ll, r, c, dbg)
                self.resizeRows(self.lines[ll], p, ll, r, c, dbg)

    def resizeQRow(self, spr, p, l, r, c, dbg=0):
        n, i, x, y, w, h, o, g, mx, my = self.geom(R, spr.x, spr.y, spr.width, spr.height, why='', init=False, dump=0)
        qq, yy = l, spr.y+spr.height-(h+y)
        self.qrows[l].update(x=x, y=yy, scale_x=mx, scale_y=my)
        if DBG or dbg: self.dumpSprite(self.qrows[qq], qq, '{:2} {:2} {:2} {:3} {:5} {:16}'.format(p, l, qq, r, c, 'on_resize QRow'))
        if self.n[R+1] > 0: self.resizeCols(self.qrows[qq], p, l, qq, r, dbg)

    def resizeRows(self, spr, p, l, q, c, dbg=0):
        n, i, x, y, w, h, o, g, mx, my = self.geom(R, spr.x, spr.y, spr.width, spr.height, why='', init=False, dump=0)
        r1 = 1 if VRSN else 0
        r2 = n if VRSN else n
        n -= 1
        for r in range(r1, r2):
#            print('ln={} n={} r={}'.format(ln, n, r))
            rr, yy = (r-1)+l*n, spr.y+spr.height-(h+y)*(r+1)
            self.rows[rr].update(x=x, y=yy, scale_x=mx, scale_y=my)
            if DBG or dbg: self.dumpSprite(self.rows[rr], rr, '{:2} {:2} {:2} {:3} {:5} {:16}'.format(p, l, q, rr, c, 'on_resize Rows'))
            if self.n[R+1] > 0: self.resizeCols(self.rows[rr], p, l, q, rr, dbg)

    def resizeCols(self, spr, p, l, q, r, dbg=0):
        n, i, x, y, w, h, o, g, mx, my = self.geom(C, spr.x, spr.y, spr.width, spr.height, why='', init=False, dump=0)
        for c in range(n):
            cc, xx, yy = c+r*n, spr.x+x+(w+x)*c, spr.y+spr.height-(h+y)
            self.cols[cc].update(x=xx, y=yy, scale_x=mx, scale_y=my)
            if DBG or dbg: self.dumpSprite(self.cols[cc], cc, '{:2} {:2} {:2} {:3} {:5} {:16}'.format(p, l, q, r, cc, 'on_resize Cols'))
    #    def dumpTexts(self, why=''):
    #        nc, ns = len(self.texts), len(self.texts[0])
    #        print('dumpTexts(BGN) {} ({}x{}):'.format(why, ns, nc))
    #        for cc in range(nc):
    #            for ss in range(ns):
    #                l = self.texts[cc][ss][0]
    #                x, y, w, h, n, d, s, c, b, i, t = l.x, l.y, l.width, l.height, l.font_name, l.dpi, l.font_size, l.color, l.bold, l.italic, l.text
    #                print('{:3} {:3} {:7.2f} {:7.2f} {:7.2f} {:7.2f}  {:16}  {:2}  {:3}   {:1}   {:1}  ({:3},{:3},{:3},{:3})  {}'.format(ss, cc, x, y, w, h, n, s, d, b, i, c[0], c[1], c[2], c[3], t))
    #        print('dumpTexts(END) {} ({}x{})'.format(why, ns, nc))
    ########################################################################################################################################################################################################
    def ns(self):  return self.n[P], self.n[L], self.n[Q], self.n[R], self.n[C], self.n[K]
    '''
