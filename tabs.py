import inspect, math, sys, os, glob, pathlib#, shutil#, unicodedata
import pyglet
import pyglet.window.key as pygwink
import pyglet.window.event as pygwine
sys.path.insert(0, os.path.abspath('../lib'))
import cmdArgs

class Tabs(pyglet.window.Window):
    def __init__(self):
        self.log('(BGN) {}'.format(Tabs))
        global FULL_SCREEN, SUBPIX, ORDER_GROUP, TEST
        self.ww, self.hh  = 640, 480
        if TEST: self.n, self.i, self.x, self.y, self.w, self.h, self.o, self.g = [12, 12, 0, 0], [0, 0, 0, 0], [4, 0, 0, 0], [0, 3, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [1, 1, 0, 0], []
#        else:    self.n, self.i, self.x, self.y, self.w, self.h, self.o, self.g = [1, 4, VRSN, 6, 80], [0, 0, VRSN, 0, 0], [0, 4, 0, 0, 0], [0, 4, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [2, 0, 0, 0, 3], []
        else:    self.n, self.i, self.x, self.y, self.w, self.h, self.o, self.g = [1, 4, 1, 6, 40], [0, 0, 1, 0, 0], [0, 4, 0, 0, 0], [0, 4, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [2, 0, 0, 0, 3], []
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
        self.log('[n]            n={}'.format(self.n))
        self.log('[i]            i={}'.format(self.i))
        self.log('[x]            x={}'.format(self.x))
        self.log('[y]            y={}'.format(self.y))
        self.log('[w]           ww={}'.format(self.ww))
        self.log('[h]           hh={}'.format(self.hh))
        self.log('[o]            o={}'.format(self.o))
        self.log('[f]  FULL_SCREEN={}'.format(FULL_SCREEN))
        self.log('[g]  ORDER_GROUP={}'.format(ORDER_GROUP))
        self.log('[s]       SUBPIX={}'.format(SUBPIX))
        self.log('[t]         TEST={}'.format(TEST))
        if len(self.n) == K: self.n.append(self.n[C] + CCC)  ;  self.log('[n] +=n[C]+CCC n={}'.format(self.n))
        self.fontBold, self.fontItalic, self.fontColorIndex, self.fontDpiIndex, self.fontSize, self.fontNameIndex = 0, 0, 0, 4, 10, 0
        self.dumpFont()
        self._initWindowA()
        super().__init__(screen=self.screens[1], fullscreen=FULL_SCREEN, resizable=True, visible=False)
        self._initWindowB()
        self.symb, self.symbStr, self.mods, self.modsStr, self.kbk = 0, '', 0, '', 0
        self.ci = 0
        self.cursor, self.caret = None, None
        self.data, self.sprites, self.blankCol = [], [], ''
        self._init() if not TEST else self._initTestColors()
        self.log('(END)')

    def _initWindowA(self, dbg=1):
        if dbg: self.log('(BGN) wxh={}x{}'.format(self.ww, self.hh))
        display      = pyglet.canvas.get_display()
        self.screens = display.get_screens()
        if dbg: self.log('(END) display={} screens={}'.format(display, self.screens))

    def _initWindowB(self, dbg=1):
        self.batch = pyglet.graphics.Batch()
        self._initGroups()
        if dbg: self.log('(BGN) wxh={}x{}'.format(self.ww, self.hh))
        self.set_visible()
        if not FULL_SCREEN: self.set_size(self.ww, self.hh)
        self.ww, self.hh = self.get_size()
        self.eventLogger = pygwine.WindowEventLogger()
        self.push_handlers(self.eventLogger)
        if dbg: self.log('(END) wxh={}x{}'.format(self.ww, self.hh))
########################################################################################################################################################################################################
    def _initTestColors(self):
#        self.clGroup = self._initGroup(0)
        self.colorLists = []
        n1, i1, x1, y1, w1, h1, o1, g1 = self.geom(0, 0, 0, self.ww, self.hh, '_initTestColors(0)', init=True, dump=0)
        n2, i2, x2, y2, w2, h2, o2, g2 = self.geom(1, 0, 0, self.ww, self.hh, '_initTestColors(1)', init=True, dump=0)
        for i in (P, L): self.dumpGeom(i, '_initTestColors() i={}'.format(i))
        c = COLORS
#        end = ['\n', ' '];        [[self.log('{:2} {:2} {:3} {:3} {:3} {:3}'.format(i, j, c[i][j][0], c[i][j][1], c[i][j][2], c[i][j][3]), end=end[0 if j==n2-1 else 1]) for j in range(n2)] for i in range(n1)]
        self.dumpSprite()
        for i in range(n1):
            sprites = []
            for j in range(n2):
                xx, yy = x1+(w1+x1)*i, self.hh-(h2+y2)*(j+1)
                self.createSprite('_initTestColors()', sprites, g1, c[i][j], xx, yy, w1, h2, i, j, v=True, dbg=1)
            self.colorLists.append(sprites)

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
        self.log('(END) ww={} x={} w={:7.2f} x+w={:7.2f} ww-x-w={:7.2f} : y={} hh={} h={:7.2f} y+h={:7.2f} hh-y-h={:7.2f}'.format(ww, x1, w1, x1+w1, ww-x1-w1, hh, y2, h2, y2+h2, hh-y2-h2))
########################################################################################################################################################################################################
    def _initGroups(self):
        for i in range(len(self.n)+3):
            p = None if ORDER_GROUP or i==0 else self.g[i-1]
            self.g.append(self._initGroup(i, p))
            self.log('({}) g={} pg={}'.format(i, self.g[i], self.g[i].parent))

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
        if dbg: self.log('geom({}) px={:7.2f} py={:7.2f} pw={:7.2f} ph={:7.2f}  =>  n={:3} x={:4} y={:4} w={:7.2f} h={:7.2f} o={}'.format(j, px, py, pw, ph, n, x, y, w, h, o))
        if nq and j == Q: n = nq
#        elif nq and j == R: n = self.n[R]
        if init: return n, i, x, y, w, h, o, g
        else:    return n, i, x, y, w, h, o, g, w/self.w[j], h/self.h[j]

    def dumpGeom(self, j, why=''):
        n, i, x, y, w, h, o , g = self.n[j], self.i[j], self.x[j], self.y[j], self.w[j], self.h[j], self.o[j], self.g[j]
        self.log('{:25} j={} n={:3} i={:4} x={:3} y={:3} w={:7.2f} h={:7.2f} o={} g={}'.format(why, j, n, i, x, y, w, h, o, g))
########################################################################################################################################################################################################
    def _init(self, dbg=1):
        self.log('(BGN) n={} i={}'.format(self.n, self.i))
        self.kp = [REDS[0], REDS[2], REDS[4], REDS[6], REDS[8], REDS[10]]  ;  self.kl = [GREENS[0], GREENS[2]]  ;  self.kq = [CYANS[0], CYANS[5]]  ;  self.kr = [YELLOWS[0], YELLOWS[3]]  ;  self.kc = [GRAYS[11], GRAYS[7]]
        self.ssi  = 0
        self.cpr  =  self.n[K]
        self.cpl  = (self.n[R] + self.n[Q]) * self.cpr
        self.cpp  =  self.n[L] * self.cpl
        self.tabs, self.pages, self.lines, self.qrows, self.rows, self.cols = [], [], [], [], [], []
        self.readDataFile()
        self.createSprites()
        if self.n[Q]: self.labels, self.labelTextA, self.labelTextB = [], ['R', 'M', '@'], ['R', 'M', '@']  ;  self.createLabels(self.g[C+1])
        self.createTabs(  self.g[C+2])
        self.createCursor(self.g[C+3])
        if dbg: self.dumpStruct('_init')
        self.log('(END) n={} i={}'.format(self.n, self.i))
########################################################################################################################################################################################################
    def readDataFile(self, dbg=1):
        DATA_DIR = 'data'  ;          DATA_SFX = '.dat'  ;  DATA_PFX = '.{}'.format(self.n[C])
        DATA_NAME = BASE_NAME + SFX + DATA_PFX + DATA_SFX
        DATA_PATH = BASE_PATH / DATA_DIR / DATA_NAME
        DATA_FILE = open(str(DATA_PATH), 'r')
        DATA_FILE.seek(0, 2)  ;  size = DATA_FILE.tell()  ;  DATA_FILE.seek(0, 0)
        self.log('(BGN) name={} size={:8,} bytes={:4,.0f} KB'.format(DATA_FILE.name, size, size/1024))
        self.data, strings = [], []  ;  nl, ns, nc = 0, 0, 0
        self.log('reading {}{} line'.format(nl + 1, self.ordSfx(nl + 1)))
        while 1:
            string = DATA_FILE.readline().strip()  ;  ns = len(strings)  ;  nc = len(strings[0]) if ns else 0
            if len(string) == 0:
                if ns: self.data.append(strings)  ;  nl += 1  ;  self.log('read    {:2}{} line with {:6,} cols on {:4,} strings {:8,} tabs'.format(nl, self.ordSfx(nl), nc, ns, nc*ns))  ;  strings=[]  ;  continue
                else: break
            strings.append(string)
            if dbg: self.log('{}'.format(string), ind=0)
        nl = len(self.data)  ;  ns = len(self.data[0])  ;  nc = len(self.data[0][0])  ;  nt = nl*nc*ns
        vdf = self.isVertDataFrmt(self.data)  ;  self.blankCol = '-' * ns
        self.log('read     {:2} lines with {:6,} cols on {:4,} strings {:8,} tabs, vdf={} blankCol({})={}'.format(nl, nl*nc, nl*ns, nt, vdf, len(self.blankCol), self.blankCol))
        if dbg: self.dumpDataA(self.data)
        self.data = self.transpose(self.data)
        vdf = self.isVertDataFrmt(self.data)
        if dbg: self.dumpDataA(self.data)
        self.log('(assert) size == nt + 2*(nl*ns+nl-1): {:8,} == {:8,} + {}'.format(size, nt, 2*(nl*ns+nl-1)))  ;  assert size == nt + 2*(nl*ns+nl-1)  ;  assert vdf
        self.log('(END) name={} size={:8,} bytes={:4,.0f} KB'.format(DATA_FILE.name, size, size/1024))

    def isVertDataFrmt(self, d, dbg=0):
        vdf = 0
        if dbg: self.log('(BGN) type(d)={} type(d[0])={} type(d[0][0])'.format(type(d), type(d[0]), type(d[0][0])))
        assert type(d) is list and type(d[0]) is list and type(d[0][0]) is str
        if type(d) is list and type(d[0]) is list and type(d[0][0]) is str:
            s0 = d[0][0]  ;  ev = ''
            if dbg: self.log('s0=d[0]: len(s0)={} s0={}'.format(len(s0), s0))
            if not s0.isdecimal():
                if dbg: self.log('s0={} is not a decimal'.format(s0))
            else:
                for i in range(len(s0)): ev = ev + str(i + 1)
                if dbg: self.log('ev={}'.format(ev))
                if s0 == ev:
                    if dbg: self.log('s0={} == ev={}'.format(s0, ev))
                    s1 = d[0][1]
                    if dbg: self.log('s1=d[1]: len(s1)={} s1={}'.format(len(s1), s1))
                    if s1.isalpha():
                        for i in range(len(s1)):
                            if s1[i] not in ('A', 'B', 'C', 'D', 'E', 'F', 'G'):
                                if dbg: self.log('s1[i]={} is not a Note Name'.format(i, s1[i]))
                                break
                        else:
                            vdf = 1
                            if dbg: self.log('s1={} is a String Tuning'.format(s1))
        if dbg: self.log('(END) type(d)={} type(d[0])={} type(d[0][0]) return VDF={}'.format(type(d), type(d[0]), type(d[0][0]), vdf))
        return vdf

    def dumpData(self, why='', lc=1, ll=1):
        self.log('(BGN) {}'.format(why))
        self.dumpDataA(self.data, lc, ll)
        transpose = self.transpose(self.data, why='Internal')
        self.dumpDataA(transpose, lc, ll)
        self.log('(END) {}'.format(why))

    def dumpDataA(self, data, lc=1, ll=1, il=0):
        s=' '
        vdf = self.isVertDataFrmt(data)
        self.log('(BGN) vdf={} lc={} ll={} il={} {}'.format(vdf, lc, ll, il, self.dumpDataDim(data)))
        for i in range(len(data)):
            if ll:             llt = 'Line {}'.format(i + 1)  ;  llab = '{:{}}'.format(llt, il + 1)  ;  self.log('{}'.format(llab), ind=0)
            if not vdf and lc: self.dumpDataLabels(data[i], i=il, sep=s)
            for j in range(len(data[i])):
                self.log('{:<{}}'.format(j + 1, il), ind=0, end='') if il and vdf else self.log('{}'.format(' ' * il), ind=0, end='')
                for k in range(len(data[i][j])):
                    self.log('{}'.format(data[i][j][k]), ind=0, end='')
                self.log(' {}'.format(j + 1), ind=0) if not il and vdf and lc else self.log(ind=0)
            self.log(ind=0)
        self.log('(END) vdf={} lc={} ll={} il={} {}'.format(vdf, lc, ll, il, self.dumpDataDim(data)))

    @staticmethod
    def dumpDataDim(d): return '({} x {} x {})={:8,} tabs'.format(len(d), len(d[0]), len(d[0][0]), len(d)*len(d[0])*len(d[0][0]))

    def dumpDataLabels(self, data, i=0, sep='^'):
        n = len(data[0])-CCC    ;  a = ' ' * i if i else ''   ;  b = sep * n  ;  p = '   '  ;  q = '  @'  ;  r = sep * 3
        if n >= 100:      self.log('{}{}'.format(a, p), ind=0, end='')  ;  [  self.log('{}'.format(c//100   if c>=100 else ' '), ind=0, end='') for c in range(1, n+1) ]  ;  self.log(ind=0)
        if n >= 10:       self.log('{}{}'.format(a, p), ind=0, end='')  ;  [  self.log('{}'.format(c//10%10 if c>=10  else ' '), ind=0, end='') for c in range(1, n+1) ]  ;  self.log(ind=0)
        self.log(                  '{}{}'.format(a, q), ind=0, end='')  ;  [  self.log('{}'.format(c%10),                        ind=0, end='') for c in range(1, n+1) ]  ;  self.log(ind=0)
        if sep != '':   self.log('{}{}{}'.format(a, r, b), ind=0)

    def transpose(self, data, why='External', dbg=1):
        if dbg: self.log('(BGN) {} {}'.format(why, self.dumpDataDim(data)))
        t = []
        for l in range(len(data)):
            tmp = []
            for c in range(len(data[l][0])):
                a = []  ;  s = ''  ;  tt = None
                for r in range(len(data[l])):
                    tt = type(data[l][r])
                    if   tt is str:  s += data[l][r][c]
                    elif tt is list: a.append(data[l][r][c])
                tmp.append(s) if tt is str else t.append(a)
            t.append(tmp)
        if dbg: self.log('(END) {} {}'.format(why, self.dumpDataDim(t)))
        return t
########################################################################################################################################################################################################
    def createSprites(self, dbg=0):
        self.log('(BGN) n={}'.format(self.n))
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
        self.log('(END) n={}'.format(self.n))

    def createSprite(self, why, ps, grp, cc, x, y, w, h, i, j=0, v=None, dbg=0):
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
        self.log('(BGN) n={}'.format(n))
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
        self.log('(END) n={}'.format(n))
########################################################################################################################################################################################################
    def dumpSprites(self, why=''):
        n = self.n
        self.log('(BGN) n={} {}'.format(n, why))
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
        self.log('(END) n={} {}'.format(n, why))

    def dumpSprite(self, s=None, c=-1, why=''):
        if s is None: self.log(' sid   p  l  q   r  col     why               x      xc        y      yc        w       h    iax  iay    m      mx     my     rot   red green blue opc vsb    group       parent', ind=0); return
        f = '{:5} {:16} {:7.2f} {:7.2f}  {:7.2f} {:7.2f}  {:7.2f} {:7.2f} {:4} {:4} {:6.3f} {:6.3f} {:6.3f} {:7.2f}  {:3}  {:3}  {:3}  {:3}  {:1}  {} {}'
        k, o, v, g, p = s.color, s.opacity, s.visible, s.group, s.group.parent
        xc, yc = s.x + s.width/2, s.y + s.height/2
        fs = f.format(c, why, s.x, xc, s.y, yc, s.width, s.height, s.image.anchor_x, s.image.anchor_y, s.scale, s.scale_x, s.scale_y, s.rotation, k[0], k[1], k[2], o, v, g, p)
        self.log('{}'.format(fs), ind=0)
        assert(type(s) == pyglet.sprite.Sprite)
########################################################################################################################################################################################################
    def createCursor(self, g):
        c = self.cursorCol()
        x, y, w, h = self.cols[c].x, self.cols[c].y, self.cols[c].width, self.cols[c].height
        self.dumpSprite()
        self.cursor = self.createSprite('cursor', None, g, CC, x, y, w, h, 0, 0, v=True)
        self.dumpSprite(self.cursor, why='{:2} {:2} {:2} {:3} {:4}  {:16}'.format(-1, -1, -1, -1, -1, 'createCursor'))
        self.log('   c={:4} x={:6.1f} y={:6.1f} w={:4} h={:4} i={}'.format(c, x, y, w, h, self.i))

    def resizeCursor(self):
        c = self.cursorCol()
        x, y, w, h = self.cols[c].x, self.cols[c].y, self.cols[c].width, self.cols[c].height
        self.cursor.update(x=x, y=y, scale_x=self.cols[c].scale_x, scale_y=self.cols[c].scale_y)
        self.log('   c={:4} x={:6.1f} y={:6.1f} w={:6.2f} h={:6.2f} i={}'.format(c, x, y, w, h, self.i))

    def cursorCol(self, dbg=1):
        p, l, _, r, c = self.i#  ;  q = self.n[Q]*(l+1)
        cpp, cpl, cpr = self.cps()
        cc = p*cpp + l*cpl + r*cpr + c
        if dbg: self.log(' cc = ({}*{} + {}*{} + {}*{} + {}) = ({} + {} + {} + {}) = {}'.format(p, cpp, l, cpl, r, cpr, c, p*cpp, l*cpl, r*cpr, c, cc))
        return cc

    def minSize(self):
        cc = self.cursorCol()  ;  w = self.cols[cc].width  ;  h = self.cols[cc].height  ;  m = min(w, h)
        self.log('cc={:3} w={:5.1f} h={:5.1f} m={:5.1f}'.format(cc, w, h, m))
        return m

    def resizeFonts(self):
        ms = self.minSize()  ;  slope, off = 0.6, -1
        fs = ms * slope + off  ;  formula = '(fs = ms*slope+off)'
        self.log('{}w x {}h {} ms={:4.1f} slope={} off={} fs={:4.1f}={:2}'.format(self.ww, self.hh, formula, ms, slope, off, fs, fri(fs)))
        self.setFontParam('font_size', fs, 'fontSize')
#        self.setFontSize(fs)

    def dumpLabelText(self, t, why='', dbg=1):
        self.log('{} len(t)={} len(t[0])={}'.format(why, len(t), len(t[0])))
        for j in range(len(t)):
            self.log('{:^3}'.format(t[j][0]), ind=0, end=' ')
        self.log(ind=0)
        for i in range(3): self.log('{:3} '.format(' '), ind=0, end='')
        for k in range(len(t)//10):
            for i in range(9): self.log('{:^3} '.format(' '), ind=0, end='')
            self.log(' {} '.format('^'), ind=0, end=' ')
        self.log(ind=0)
        for j in range(len(t)):
            self.log('{:^3}'.format(t[j][1]), ind=0, end=' ')
        self.log(ind=0)
        if dbg:
            for i in range(len(t)):
                self.log('{:5}'.format(i - 2), ind=0, end=' ')
                self.log(' {:>5}'.format(t[i][0]), ind=0, end=' ')
                d = ' ' if (i - 2) % 10 else '>'
                self.log('{}{:>5}'.format(d, t[i][1]), ind=0, end=' ')
                self.log(ind=0)

    @staticmethod
    def deleteList(l):
        j = 0
        while j < len(l): t = l[j];  t.delete();  del l[j]
########################################################################################################################################################################################################
    def createLabels(self, g, dbg=1):
        if dbg: self.log('(BGN) n={} len(labels)={}'.format(self.n, len(self.labels)))
        self.labelTextA.extend('{}'.format(j) for j in range(1, self.n[C] + 1))
        self.labelTextB.extend('{}'.format(j % 10 if j % 10 else j // 10 % 10) for j in range(1, self.n[C] + 1))
        texts = list(zip(self.labelTextA, self.labelTextB))
        self.dumpLabelText(texts)
#        self.deleteList(self.labels)
        for q in range(len(self.qrows)):
            if dbg: self.dumpLabel()
            for c in range(len(self.labelTextB)):
                qc = c + q*self.cpl
                tc = c + q*self.cpr
                k  = 1 if c == 2 or (c - 2) % 10 else 2
                l = self.createLabel(self.labels, self.labelTextB[c], qc, k, g)
                if dbg: self.dumpLabel(l, tc, q, qc, 'createLabels')
        if dbg: self.dumpLabel()
        if dbg: self.log('(END) n={} len(labels)={}'.format(self.n, len(self.labels)))

    def createLabel(self, l, text, c, kk, g, m=False):
        w, h, ac, ab, b = self.cols[c].width, self.cols[c].height, 'center', 'center', self.batch
        o, k, d, j, n, s = self.fontParams()
        d = FONT_DPIS[d]
        n = FONT_NAMES[n]
        k = FONT_COLORS[k + kk]
        x, y, = self.cols[c].x + w/2, self.cols[c].y + h/2
        if m:
            for i in range(len(text), 0, -1): text = text[:i] + '\n' + text[i:]
        label = pyglet.text.Label(text, font_name=n, font_size=s, bold=o, italic=j, color=k, x=x, y=y, width=w, height=h, anchor_x=ac, anchor_y=ab, align=ac, dpi=d, batch=b, group=g, multiline=m)
        l.append(label)
        return label

    def createTabs(self, g, dbg=0):
        n = self.n  ;  nt = len(self.tabs)
        self.log('(BGN) n={} nt={}'.format(n, nt))
#        self.deleteList(self.tabs)
#        if dbg: self.dumpData(why='createTabs')
#        if dbg: self.dumpTab()
        for l in range(n[L]):
            for c in range(n[K]):
                if c < len(self.data[l]): col = self.data[l][c]
                else:                     col = self.blankCol  ;  self.data[l].append(col)
#                self.log('{} {} {}'.format(l, c, self.data[l][c]))
                for r in range(n[R]):
                    rc = c + (r + n[Q])*self.cpr + l * self.cpl
                    tc = c + r*self.cpr
#                    if dbg: self.log('() l={} r={:2} c={:3} rc={:4} tc={:4} cc={:4}'.format(l, r, c, rc, tc, cc), end=' ')
                    t = self.createTab(self.tabs, col[r], rc, g)
                    if dbg: self.dumpTab(t, tc, r, rc, 'createTabs')
        if dbg: self.dumpTab()
        if dbg: self.dumpTabs(why='createTabs')
        self.log('(END) n={} nt={}'.format(n, nt))

    def createTab(self, t, text, c, g):
        w, h, ac, ab, b = self.cols[c].width, self.cols[c].height, 'center', 'center', self.batch
        o, k, d, j, n, s = self.fontParams()
        n = FONT_NAMES[n]
        k = FONT_COLORS[k]
        d = FONT_DPIS[d]
        x, y, = self.cols[c].x + w/2, self.cols[c].y + h/2
        tab = pyglet.text.Label(text, font_name=n, font_size=s, bold=o, italic=j, color=k, x=x, y=y, width=w, height=h, anchor_x=ac, anchor_y=ab, align=ac, dpi=d, batch=b, group=g)
        t.append(tab)
        return tab
########################################################################################################################################################################################################
    def resizeLabels(self, dbg=0):
        cpp, cpl, cpr = self.cps()
        lnl = self.lnl()
        self.log('(BGN) lnl={} cpp={} cpl={} cpr={}'.format(lnl, cpp, cpl, cpr))
        for l in range(self.n[L]):
            for c in range(cpr):
                self.resizeLabel(self.labels[c + l*cpr], c + l*cpl)
        if dbg: self.dumpLabels('resizeLabels')
        self.log('(END) lnl={} cpp={} cpl={} cpr={}'.format(lnl, cpp, cpl, cpr))

    def resizeLabel(self, l, c):
        w, h = self.cols[c].width, self.cols[c].height
        x, y = self.cols[c].x + w/2, self.cols[c].y + h/2
        l.x, l.y, l.width, l.height = x, y, w, h

    def resizeTabs(self, dbg=0):
        n = self.n  ;  i = 0
        self.log('(BGN) n={} cps={}'.format(n, self.cps()))
        for l in range(n[L]):
            for c in range(n[K]):
                for r in range(n[R]):
                    t = c + (r + n[Q]) * self.cpr + l * self.cpl
                    self.resizeTab(self.tabs[i], t)
                    i += 1
        if dbg: self.dumpTabs('resizeTabs')
        self.log('(END) n={} cps={}'.format(n, self.cps()))

    def resizeTab(self, t, c):
        w, h = self.cols[c].width, self.cols[c].height
        x, y = self.cols[c].x + w/2, self.cols[c].y + h/2
        t.x, t.y,t.width, t.height = x, y, w, h
########################################################################################################################################################################################################
    def dumpLabels(self, why='', dbg=0):
        cpp, cpl, cpr = self.cps()
        nq = len(self.qrows)
        if dbg: self.log('(BGN) nq={} {}'.format(nq, why))
        self.dumpLabel()
        for q in range(nq):
            for c in range(cpr):
                self.dumpLabel(self.labels[c+q*cpr], c+q*cpr, q, c+q*cpl, why)
        self.dumpLabel()
        if dbg: self.log('(END) nq={} {})'.format(nq, why))

    def dumpLabel(self, l=None, lid=-1, q=-1, c=-1, why=''):
        if l is None: self.log('lid  q   c  text     x       y       w       h      font name      size dpi bold ital red green blue opc  why', ind=0) ; return
        x, y, w, h, n, d, s, k, b, i, t = l.x, l.y, l.width, l.height, l.font_name, l.dpi, l.font_size, l.color, l.bold, l.italic, l.text
        self.log('{:3} {:2} {:4}  {:3} {:7.2f} {:7.2f} {:7.2f} {:7.2f}  {:16}  {:2}  {:3}   {:1}    {:1}  {:3}  {:3}  {:3}  {:3}  {}'.format(lid, q, c, t, x, y, w, h, n, s, d, b, i, k[0], k[1], k[2], k[3], why), ind=0)

    def dumpTabs(self, why='', dbg=0):
        n = self.n  ;  i = 0  ;  why = '{:16}'.format(why)
        if dbg: self.log('(BGN) n={} {}'.format(n, why))
        self.dumpTab()
        for l in range(n[L]):
            for c in range(n[K]):
                for r in range(n[R]):
                    rc = c + (r + n[Q])*self.cpr
                    why2 = ' {:5} {:4} {:2} {:3} {:3} {:1}'.format(i, c, r, rc, len(self.data[l]), len(self.data[l][c]))
                    self.dumpTab(self.tabs[i], i, r, rc, why + why2)
                    i += 1
        self.dumpTab()
        if dbg: self.log('(END) n={} {}'.format(n, why))

    def dumpTab(self, t=None, tid=-1, r=-1, c=-1, why=''):
        if t is None: self.log('tid  r   c  text     x       y       w       h      font name      size dpi bold ital red green blue opc  why                 i    c   r  rc  ', ind=0) ; return
        x, y, w, h, n, d, s, k, b, i, tt = t.x, t.y, t.width, t.height, t.font_name, t.dpi, t.font_size, t.color, t.bold, t.italic, t.text
        self.log('{:3} {:2} {:4}  {:3} {:7.2f} {:7.2f} {:7.2f} {:7.2f}  {:16}  {:2}  {:3}   {:1}    {:1}  {:3}  {:3}  {:3}  {:3}  {}'.format(tid, r, c, tt, x, y, w, h, n, s, d, b, i, k[0], k[1], k[2], k[3], why), ind=0)
########################################################################################################################################################################################################
    def dumpTest(self, why=''):
        self.dumpFont('{}'.format(why))
        self.dumpSprite()
#        for i in range(len(self.colorLists)):
#            self.dumpSprites(self.colorLists[i], why)

    def dumpStruct(self, why=''):
        self.log('(BGN) {}'.format(why))
        self.dumpSprites(why)
        self.dumpLabels(why)
        self.dumpData(why=why)
        self.dumpTabs(why)
        self.dumpFont(why)
        self.dumpNums(why)
        self.cursorCol(dbg=1)
        self.log('(END) {}'.format(why))
########################################################################################################################################################################################################
    def dumpNums(self, why=''):
        n = self.n  ;  i = self.i  ;  lnl = self.lnl()  ;  cps = self.cps()
        self.log('{} n={}  i={} lnl={}  cps={}'.format(why, n, i, lnl, cps))
#######################################################################################################################################################################################################
    def on_resize(self, width, height):
        super().on_resize(width, height)
        self.ww, self.hh = width, height
        if TEST: self.resizeTestColors()  ;  return
        self.log('(BGN) {:4}w x {:4}h'.format(self.ww, self.hh))
        self.resizeSprites()
        self.resizeFonts()
        if self.n[Q]: self.resizeLabels()
        self.resizeTabs()
        self.resizeCursor()
        self.snapshot()
#        self.dumpStruct('on_resize()')
#        self.updateCaption()
        self.log('(END) {:4} x {:4}'.format(self.ww, self.hh))
########################################################################################################################################################################################################
    def on_draw(self):
        self.clear()
        self.batch.draw()

    def kpEvntTxt(self):
        return 'kbk={:8} symb={:8} symbStr={:14} mods={:2} modsStr={:28}'.format(self.kbk, self.symb, self.symbStr, self.mods, self.modsStr)

    def on_key_press(self, symb, mods):
        self.symb, self.mods, self.symbStr, self.modsStr = symb, mods, pygwink.symbol_string(symb), pygwink.modifiers_string(mods)
        self.kbk = self.symbStr  ;  kbk = self.kbk
        self.log('(BGN) {}'.format(self.kpEvntTxt()))
        if                  self.isTab(kbk):                          self.addTab(kbk, 'on_key_press')
        elif kbk == 'Q' and self.isCtrl(mods) and self.isShift(mods): self.quit('keyPress({})'.format(kbk))
        elif kbk == 'Q' and self.isCtrl(mods):                        self.quit('keyPress({})'.format(kbk))
        elif kbk == 'B' and self.isCtrl(mods) and self.isShift(mods): self.setFontParam('bold',   not self.fontBold,   'fontBold')
        elif kbk == 'B' and self.isCtrl(mods):                        self.setFontParam('bold',   not self.fontBold,   'fontBold')
        elif kbk == 'I' and self.isCtrl(mods) and self.isShift(mods): self.setFontParam('italic', not self.fontItalic, 'fontItalic')
        elif kbk == 'I' and self.isCtrl(mods):                        self.setFontParam('italic', not self.fontItalic, 'fontItalic')
        elif kbk == 'S' and self.isCtrl(mods) and self.isShift(mods): self.setFontParam('font_size', (self.fontSize + 1)       % 52,               'fontSize')
        elif kbk == 'S' and self.isCtrl(mods):                        self.setFontParam('font_size', (self.fontSize - 1)       % 52,               'fontSize')
        elif kbk == 'D' and self.isCtrl(mods) and self.isShift(mods): self.setFontParam('dpi',       (self.fontDpiIndex + 1)   % len(FONT_DPIS),   'fontDpiIndex')
        elif kbk == 'D' and self.isCtrl(mods):                        self.setFontParam('dpi',       (self.fontDpiIndex - 1)   % len(FONT_DPIS),   'fontDpiIndex')
        elif kbk == 'N' and self.isCtrl(mods) and self.isShift(mods): self.setFontParam('font_name', (self.fontNameIndex + 1)  % len(FONT_NAMES),  'fontNameIndex')
        elif kbk == 'N' and self.isCtrl(mods):                        self.setFontParam('font_name', (self.fontNameIndex - 1)  % len(FONT_NAMES),  'fontNameIndex')
        elif kbk == 'C' and self.isCtrl(mods) and self.isShift(mods): self.setFontParam('color',     (self.fontColorIndex + 1) % len(FONT_COLORS), 'fontColorIndex')
        elif kbk == 'C' and self.isCtrl(mods):                        self.setFontParam('color',     (self.fontColorIndex + 1) % len(FONT_COLORS), 'fontColorIndex')
        elif kbk == 'F' and self.isCtrl(mods) and self.isShift(mods): self.toggleFullScreen()
        elif kbk == 'F' and self.isCtrl(mods):                        self.toggleFullScreen()
#        self.updateCaption()
        self.log('(END) {}'.format(self.kpEvntTxt()))

    def on_text(self, text):
        self.kbk = text
        self.log('(BGN) {}'.format( self.kpEvntTxt()))
        if self.isTab(self.kbk):                 self.addTab(self.kbk, 'on_text')
        if self.kbk=='$' and self.isShift(self.mods): self.snapshot()
#        self.updateCaption()
        self.log('(END) {}'.format( self.kpEvntTxt()))

    def on_text_motion(self, motion, dbg=0):
        self.kbk = motion
        if dbg: self.log('(BGN) {}'.format(self.kpEvntTxt()))
        if self.mods == 0:
            if   motion == pygwink.MOTION_LEFT:          self.move(-1)
            elif motion == pygwink.MOTION_RIGHT:         self.move( 1)
            elif motion == pygwink.MOTION_UP:            self.move(-self.n[K])
            elif motion == pygwink.MOTION_DOWN:          self.move( self.n[K])
            elif motion == pygwink.HOME:                 pass
            elif motion == pygwink.END:                  pass
#            elif motion==pygwink.MOTION_PREVIOUS_PAGE: self.move() # prevPage(self.i[P], motion)
#            elif motion==pygwink.MOTION_NEXT_PAGE:     self.move() # nextPage(self.i[P], motion)
            else:                                      self.log('on_text_motion() motion={} ???'.format(motion))
#            self.updateCaption()
        if dbg: self.log('(END) {}'.format(self.kpEvntTxt()))
########################################################################################################################################################################################################
    def move(self, c, dbg=1):
        n, i, cc = self.n, self.i, self.cursorCol()  ;  k = cc + c
        if dbg: self.log('(BGN) c={} n={} i={} cc={} k={}'.format(c, n, i, cc, k), file=sys.stdout)
        self.updateI(c)
        kk = k % self.cpp# + k // self.cpp
        self.cursor.update(x=self.cols[kk].x, y=self.cols[kk].y)
        if dbg: self.log('(END) c={} n={} i={} kk={} cc={}'.format(c, n, i, kk, self.cursorCol()), file=sys.stdout)

    def updateI(self, c, dbg=1):
        n, i = self.n, self.i  ;  cpp, cpl, cpr = self.cps()
        if dbg: self.log('(BGN) c={} n={} i={} cps={}'.format(c, n, i, self.cps()), file=sys.stdout)
        sc        = i[C] + c
        self.i[C] = sc %  n[K]
        sr        = sc // cpr + i[R]
        self.i[R] = sr %  n[R]
        sl        = sr // n[R] + i[L]
        self.i[L] = sl %  n[L]
        sp        = sl // n[L] + i[P]
        self.i[P] = sp %  n[P]
#        self.i[C] = sp // n[P] + self.i[C]
        if dbg: self.log('(END) c={} n={} i={} sc={} sr={} sl={} sp={}'.format(c, n, i, sc, sr, sl, sp), file=sys.stdout)
    '''
    def nextPage(self, i, motion):
        self.pages[i].visible = False
        self.updatePage(i+1, '{}=MOTION_NEXT_PAGE   '.format(motion))

    def prevPage(self, i, motion):
        self.pages[i].visible = False
        self.updatePage(i-1, '{}=MOTION_PREVIOUS_PAGE'.format(motion))

    def updatePage(self, i, why):
        i = i % self.n[P]
        self.pages[i].visible = True
        self.log('{} i[{}]={}'.format(why, P, i))
        self.i[P] = i
    '''
########################################################################################################################################################################################################
    def addTab(self, kbk, why=''):
        cc = self.cursorCol()
        self.log('(BGN) {} : cc={} i={} {}'.format(self.kpEvntTxt(), cc, self.i, why), file=sys.stdout)
        self.updateData(kbk, cc)
        self.updateTab( kbk, cc)
        self.snapshot()
        self.log('(END) {} : cc={} i={} {}'.format(self.kpEvntTxt(), cc, self.i, why), file=sys.stdout)

    def on_mouse_release(self, x, y, button, modifiers):  # pyglet.window.mouse.MIDDLE #pyglet.window.mouse.LEFT #pyglet.window.mouse.RIGHT
        n = self.n      ;  np, nl, nq, nr, nc, nk = n
#        i = self.i  ;  ip, il, iq, ir, ic     = i
        cc = self.cursorCol()  ;  cpp, cpl, cpr = self.cps()
        w = self.ww/nk  ;  h = self.hh/((nr + nq)*nl)   ;  y = self.hh - y
        c = int(x/w)    ;  r = int(y/h)
        k = self.i[P]*cpp + self.i[L]*cpl + self.i[R]*cpr + self.i[C]
        self.log('(BGN) b={} m={} n={} x={:4} y={:4} w={:6.2f} h={:6.2f} i={} c={:4} r={:4} k={:4} cc={:4}'.format(button, modifiers, n, x, y, w, h, self.i, c, r, k, cc))
        self.i[C] = c   ;   self.i[L] = r//(nq + nr)  ;  self.i[R] = r % (nq + nr)
        k = self.i[P]*cpp + self.i[L]*cpl + self.i[R]*cpr + self.i[C]
        self.cursor.update(self.cols[k].x, self.cols[k].y)
        cc = self.cursorCol(dbg=0)
        self.log('(END) b={} m={} n={} x={:4} y={:4} w={:6.2f} h={:6.2f} i={} c={:4} r={:4} k={:4} cc={:4}'.format(button, modifiers, n, x, y, w, h, self.i, c, r, k, cc))

    def updateData(self, text, cc, dbg=1):
        p, l, q, r, c = self.i
        t = self.data[l][c]
        if dbg: self.dumpData(why='updateData(BGN) text={} cc={} i={} t={} data[l][c]={}'.format(text, cc, self.i, t, self.data[l][c]))
        self.data[l][c] = t[0:r] + text + t[r+1:]
        if dbg: self.dumpData(why='updateData(END) text={} cc={} i={} t={} data[l][c]={}'.format(text, cc, self.i, t, self.data[l][c]))

    def updateTab(self, text, cc, dbg=1):
        self.log('(BGN) text={} cc={} tabs[cc].text={}'.format(text, cc, self.tabs[cc].text), file=sys.stdout)
        self.tabs[cc].text = text
        if dbg: self.tabs[cc].color = FONT_COLORS[self.fontColorIndex + 1]
        self.log('(END) text={} cc={} tabs[cc].text={}'.format(text, cc, self.tabs[cc].text), file=sys.stdout)

    def updateCaption(self):
        fb, fc, fd, fi, fn, fs = self.fontParams()
        text = '{}dpi {}pt {} {}'.format(fd, fs, fn, fc)
        self.log('{}'.format(text))
        self.set_caption(text)
########################################################################################################################################################################################################
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
########################################################################################################################################################################################################
    def fontParams(self):    return self.fontBold, self.fontColorIndex, self.fontDpiIndex, self.fontItalic, self.fontNameIndex, self.fontSize

    def dumpFont(self, why=''):
        b, c, dpi, i, n, s = self.fontParams()
        pix = FONT_SCALE * s / dpi
        self.log('({}) {} {}DPI {}pt {} ({:6.3f}*{}pt/{}DPI)={:6.3f}pixels'.format(why, c, dpi, s, n, FONT_SCALE, s, dpi, pix))

    def setFontParam(self, n, v, m):
        setattr(self, m, v)
        self.log('n={} v={:.1f} m={}'.format(n, v, m))
        for j in range(len(self.tabs)):
            setattr(self.tabs[j],       n, FONT_NAMES[v] if m == 'fontNameIndex' else FONT_COLORS[v] if m == 'fontColorIndex' else FONT_DPIS[v] if m == 'fontDpiIndex' else v)
        if self.n[Q]:
            for j in range(len(self.labels)):
                setattr(self.labels[j], n, FONT_NAMES[v] if m == 'fontNameIndex' else FONT_COLORS[v] if m == 'fontColorIndex' else FONT_DPIS[v] if m == 'fontDpiIndex' else v)
########################################################################################################################################################################################################
    def toggleFullScreen(self):
        global FULL_SCREEN
        FULL_SCREEN = not FULL_SCREEN
        self.set_fullscreen(FULL_SCREEN)
        self.log('FULL_SCREEN={}'.format(FULL_SCREEN))

    def toggleColorLists(self, motion):
        if not TEST: self.log('(WARNING) Nothing To Toggle TEST={} motion={}'.format(TEST, motion)) ; return
        cls = self.colorLists
        i = self.i[P]
        self.log('i={}'.format(i))
        if motion==pygwink.MOTION_LEFT:
            for j in range(len(cls[i])): cls[i][j].visible = False
            i -= 1
            i = i % len(COLORS)
            for j in range(len(cls[i])): cls[i][j].visible = True
            self.log('MOTION_LEFT={} i[P]={} len(cls)={}'.format(motion, i, len(cls)))
        elif motion==pygwink.MOTION_RIGHT:
            for j in range(len(cls[i])): cls[i][j].visible = False
            i += 1
            i = i % len(COLORS)
            for j in range(len(cls[i])): cls[i][j].visible = True
            self.log('MOTION_RIGHT={} i[P]={} len(cls)={}'.format(motion, i, len(cls)))
        self.i[P] = i
########################################################################################################################################################################################################
    @staticmethod
    def isCtrl(mods):        return mods&pygwink.MOD_CTRL
    @staticmethod
    def isShift(mods):       return mods&pygwink.MOD_SHIFT
    @staticmethod
    def isAlt(mods):         return mods&pygwink.MOD_ALT
    @staticmethod
    def isTab(text):         return True if text=='-' or Tabs.isFret(text)   else False
    @staticmethod
    def isFret(text):        return True if '0'<=text<='9' or 'a'<=text<='o' else False

    def snapshot(self):
        SNAP_DIR      = 'snaps'  ;                                           SNAP_SFX = '.png'
        SNAP_GLOB_ARG = str(BASE_PATH / SNAP_DIR / BASE_NAME) + SFX + '.*' + SNAP_SFX
        self.log('SFX={} SNAP_DIR={} SNAP_SFX={} BASE_NAME={} BASE_PATH={}'.format(SFX, SNAP_DIR, SNAP_SFX, BASE_NAME, BASE_PATH))
        self.log('globPathArg={}'.format(SNAP_GLOB_ARG))
        FILE_GLOB     = glob.glob(SNAP_GLOB_ARG)
        for _F in FILE_GLOB:
            self.log('{}  {}'.format(os.path.basename(_F), _F), ind=0)
            pathlib.Path(_F).unlink()
        SNAP_ID   = '.{}'.format(self.ssi)
        SNAP_NAME = BASE_NAME + SFX + SNAP_ID + SNAP_SFX
        SNAP_PATH = BASE_PATH / SNAP_DIR / SNAP_NAME
        pyglet.image.get_buffer_manager().get_color_buffer().save('{}'.format(SNAP_PATH))
        self.log('SNAP_ID={} SNAP_NAME={} SNAP_PATH={}'.format(SNAP_ID, SNAP_NAME, SNAP_PATH))
        self.ssi += 1

    def dumpStack(self, si):
        for i, e in enumerate(si):
            fp = pathlib.Path(e.filename)  ;            n = fp.stem  ;            l = e.lineno  ;            f = e.function  ;            c = e.code_context[0].strip()  ;            j = len(si) - (i + 1)
            self.log('{:2} {:9} {:5} {:20} {}'.format(j, n, l, f, c))
        self.log('MAX_STACK_DEPTH={:2}'.format(MAX_STACK_DEPTH))

    def indent(self): d = self.stackDepth() - 4;  return '{:{w}}'.format(d, w=d)

    @staticmethod
    def stackDepth():
        global MAX_STACK_DEPTH, MAX_STACK_FRAME
        si = inspect.stack()
        for i, e in enumerate(si):
            j = len(si) - (i + 1)
            if j > MAX_STACK_DEPTH: MAX_STACK_DEPTH = j;  MAX_STACK_FRAME = si
        return len(si)

    def log(self, msg='', ind=1, file=None, flush=False, sep=',', end='\n'):
        if not file: file = LOG_FILE
        si = inspect.stack(0)[1]
        p = pathlib.Path(si.filename)  ;        n = p.name  ;        l = si.lineno  ;        f = si.function  ;        t = ''
        if f == 'self.log': si = inspect.stack(0)[2];  p = pathlib.Path(si.filename);  n = p.name;  l = si.lineno;  f = si.function;  t = ''
        if ind: print('{:20} {:7} {:6} {} {:>20} '.format(self.indent(), l, n, t, f), file=file, end='')
        print('{}'.format(msg), file=file, flush=flush, sep=sep, end=end) if ind else print('{}'.format(msg), file=file, flush=flush, sep=sep, end=end)
        if file != LOG_FILE: self.log(msg, ind)
    ########################################################################################################################################################################################################
    def quit(self, why=''):
        self.log('(BGN)')
        text = '\n' + '###   Quit   ###' * 13 + '\n'
        self.log(text)
        self.dumpStruct('quit ' + why) if not TEST else self.dumpTest('quit() ' + why)
        self.snapshot()
        self.log(text)
        self.dumpStack(inspect.stack())
        self.log(text)
        self.dumpStack(MAX_STACK_FRAME)
        self.log('(END) closing LOG_FILE={}'.format(LOG_FILE.name))
        LOG_FILE.close()
        exit()
########################################################################################################################################################################################################
if __name__ == '__main__':
    TEST = 0  ;  CARET = 0  ;  ORDER_GROUP = 1  ;  SUBPIX = 1  ;  FULL_SCREEN = 0  ;  VRSN = 0
    SFX           = '.TEST' if TEST else '.' + chr(65 + VRSN)
    PATH          = pathlib.Path(sys.argv[0])
    BASE_PATH     = PATH.parent
    BASE_NAME     = BASE_PATH.stem
    LOG_DIR       = 'logs'  ;         LOG_SFX       = '.log'
    LOG_NAME      = BASE_NAME + SFX + LOG_SFX
    LOG_PATH      = BASE_PATH / LOG_DIR / LOG_NAME
    P, L, Q, R, C, K = 0, 1, 2, 3, 4, 5
    OPACITY       = [255, 240, 225, 210, 190, 165, 140, 110, 80]
    GRAY          = [(255, 255, 255, OPACITY[0]), ( 0,  0,  0, OPACITY[0])]
    PINK          = [(255,  64, 192, OPACITY[0]), (57, 16, 16, OPACITY[0])]
    INFRA_RED     = [(255,  29,  24, OPACITY[0]), (68, 20, 19, OPACITY[0])]
    RED           = [(255,  24,  21, OPACITY[0]), (88, 15, 12, OPACITY[0])]
    ORANGE        = [(255, 128,  32, OPACITY[0]), (76, 30, 25, OPACITY[0])]
    YELLOW        = [(255, 255,  15, OPACITY[0]), (45, 41, 10, OPACITY[0])]
    GREEN         = [( 44, 255,   0, OPACITY[0]), (21, 54, 10, OPACITY[0])]
    GREEN_BLUE    = [( 24, 255,  61, OPACITY[0]), (10, 49, 25, OPACITY[0])]
    CYAN          = [( 32, 255, 255, OPACITY[0]), (16, 64, 64, OPACITY[0])]
    BLUE_GREEN    = [( 25, 181, 255, OPACITY[0]), (12, 37, 51, OPACITY[0])]
    BLUE          = [( 35,  26, 255, OPACITY[0]), (19, 11, 64, OPACITY[0])]
    INDIGO        = [( 35,  26, 255, OPACITY[0]), (19, 11, 64, OPACITY[0])]
    VIOLET        = [(176,  81, 255, OPACITY[0]), (44, 14, 58, OPACITY[0])]
    ULTRA_VIOLET  = [(194,  96, 255, OPACITY[3]), (50, 19, 61, OPACITY[1])]
    HUES          = 13  ;  MAX_STACK_DEPTH = 0  ;  MAX_STACK_FRAME = inspect.stack()
    def fri(f): return int(math.floor(f+0.5))
########################################################################################################################################################################################################
    def genColors(cp, nsteps=HUES, dbg=0):
        colors, clen = [], len(cp[0])
        diffs = [cp[1][i] - cp[0][i] for i in range(clen)]
        steps = [diffs[i]/nsteps     for i in range(clen)]
        if dbg: print('c1={} c2={} nsteps={} diffs={} steps='.format(cp[0], cp[1], nsteps, diffs), end='')  ;  print('[{:6.1f} {:6.1f} {:6.1f} {:6.1f}]'.format(steps[0], steps[1], steps[2], steps[3]))
        for j in range(nsteps):
            c = tuple([fri(cp[0][i] + j * steps[i]) for i in range(len(cp[0]))])
            if dbg: print('c[{}]={}'.format(j, c))
            colors.append(c)
        if dbg: print('colors={}'.format(cp))
        return colors

    GRAYS         = genColors(GRAY)
    PINKS         = genColors(PINK)
    INFRA_REDS    = genColors(INFRA_RED)
    REDS          = genColors(RED)
    ORANGES       = genColors(ORANGE)
    YELLOWS       = genColors(YELLOW)
    GREENS        = genColors(GREEN)
    GREEN_BLUES   = genColors(GREEN_BLUE)
    CYANS         = genColors(CYAN)
    BLUE_GREENS   = genColors(BLUE_GREEN)
    BLUES         = genColors(BLUE)
    INDIGOS       = genColors(INDIGO)
    VIOLETS       = genColors(VIOLET)
    ULTRA_VIOLETS = genColors(ULTRA_VIOLET)
    COLORS        = (INFRA_REDS, REDS, ORANGES, YELLOWS, GRAYS, GREENS, GREEN_BLUES, CYANS, BLUE_GREENS, BLUES, INDIGOS, VIOLETS, ULTRA_VIOLETS)
    CC            = (255, 190, 12, 176)
    CCC           = 3
    FONT_SCALE    = 123.42857
    FONT_NAMES    = ['Times New Roman', 'Lucida Console', 'Courier New', 'Helvetica', 'Arial', 'Century Gothic', 'Bookman Old Style', 'Antique Olive']
    FONT_COLORS   = [GREENS[0], BLUES[0], CYANS[0], ORANGES[0], REDS[0], INDIGOS[0], VIOLETS[0], PINKS[0], INFRA_REDS[0], YELLOWS[0], GREEN_BLUES[0], ULTRA_VIOLETS[0], BLUE_GREENS[0], GRAYS[0]]
    FONT_DPIS     = [72, 78, 84, 90, 96, 102, 108, 114, 120]
    with open(str(LOG_PATH), 'w') as LOG_FILE:
        tabs          = Tabs()
        pyglet.app.run()
