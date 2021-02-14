import math, sys, os
#import shutil
#import unicodedata
import pyglet
import pyglet.window.key as pygwink
import pyglet.window.event as pygwine
sys.path.insert(0, os.path.abspath('../lib'))
import cmdArgs

class Tabs(pyglet.window.Window):
    def __init__(self):
        global FULL_SCREEN, SUBPIX, ORDER_GROUP, TEST
        self.ww, self.hh  = 640, 480
        if TEST: self.n, self.i, self.x, self.y, self.w, self.h, self.o, self.g = [12, 12, 0, 0], [0, 0, 0, 0], [4, 0, 0, 0], [0, 3, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [1, 1, 0, 0], []
        else:    self.n, self.i, self.x, self.y, self.w, self.h, self.o, self.g =  [1, 3, VRSN, 6, 20], [0, 0, VRSN, 0, 0], [0, 0, 0, 0, 0], [0, 4, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [2, 0, 0, 0, 3], []
        print('{}'.format(sys.argv[0]), file=DBG_FILE)
        print('{}'.format(os.path.dirname(sys.argv[0])), file=DBG_FILE)
        print('{}'.format(os.path.basename(sys.argv[0])), file=DBG_FILE)
        self.snapPath = '{}/{}'.format(os.path.dirname(sys.argv[0]), SNAP_DIR)
        print('snapPath={}'.format(self.snapPath), file=DBG_FILE)
#        shutil.rmtree(self.snapPath)
        self.argMap = cmdArgs.parseCmdLine(dbg=1)
        print('__init__(BGN) argMap={}'.format(self.argMap), file=DBG_FILE)
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
        print('[n]            n={}'.format(self.n),          file=DBG_FILE)
        print('[i]            i={}'.format(self.i),          file=DBG_FILE)
        print('[x]            x={}'.format(self.x),          file=DBG_FILE)
        print('[y]            y={}'.format(self.y),          file=DBG_FILE)
        print('[w]           ww={}'.format(self.ww),         file=DBG_FILE)
        print('[h]           hh={}'.format(self.hh),         file=DBG_FILE)
        print('[o]            o={}'.format(self.o),          file=DBG_FILE)
        print('[f]  FULL_SCREEN={}'.format(FULL_SCREEN),     file=DBG_FILE)
        print('[g]  ORDER_GROUP={}'.format(ORDER_GROUP),     file=DBG_FILE)
        print('[s]       SUBPIX={}'.format(SUBPIX),          file=DBG_FILE)
        print('[t]         TEST={}'.format(TEST),            file=DBG_FILE)
        if len(self.n) == K: self.n.append(self.n[C] + CCC)  ;  print('[n] +=n[C]+CCC n={}'.format(self.n), file=DBG_FILE)
        self.fontBold, self.fontItalic, self.fontNameIndex, self.fontColorIndex, self.fontSizeIndex, self.fontDpiIndex = 0, 0, 0, 0, len(FONT_SIZES)//3, 3
        self._initWindowA()
        super().__init__(screen=self.screens[1], fullscreen=FULL_SCREEN, resizable=True, visible=False)
        self._initWindowB()
        self.symb, self.symbStr, self.mods, self.modsStr, self.kbk = 0, '', 0, '', 0 ; self.ci = 0
        self.cursor, self.caret = None, None
        self.data, self.sprites = [], []
        self._init() if not TEST else self._initTestColors()
        print('__init__(END)'.format(), file=DBG_FILE)

    def _initWindowA(self):
        display      = pyglet.canvas.get_display()
        self.screens = display.get_screens()

    def _initWindowB(self, dbg=0):
        self.batch = pyglet.graphics.Batch()
        self._initGroups()
        if DBG or dbg: print('_initWindowB(BGN) wxh={}x{}'.format(self.ww, self.hh), file=DBG_FILE)
        self.set_visible()
        if not FULL_SCREEN: self.set_size(self.ww, self.hh)
        self.ww, self.hh = self.get_size()
        self.eventLogger = pygwine.WindowEventLogger()
        self.push_handlers(self.eventLogger)
        if DBG or dbg: print('_initWindowB(END) wxh={}x{}'.format(self.ww, self.hh), file=DBG_FILE)
########################################################################################################################################################################################################
    def _initTestColors(self):
#        self.clGroup = self._initGroup(0)
        self.colorLists = []
        n1, i1, x1, y1, w1, h1, o1, g1 = self.geom(0, 0, 0, self.ww, self.hh, '_initTestColors(0)', init=True, dump=0)
        n2, i2, x2, y2, w2, h2, o2, g2 = self.geom(1, 0, 0, self.ww, self.hh, '_initTestColors(1)', init=True, dump=0)
        for i in (P, L): self.dumpGeom(i, '_initTestColors() i={}'.format(i))
        c = COLORS
#        end = ['\n', ' '];        [[print('{:2} {:2} {:3} {:3} {:3} {:3}'.format(i, j, c[i][j][0], c[i][j][1], c[i][j][2], c[i][j][3]), file=DBG_FILE, end=end[0 if j==n2-1 else 1]) for j in range(n2)] for i in range(n1)]
        self.dumpSprite()
        for i in range(n1):
            sprites = []
            for j in range(n2):
                xx, yy = x1+(w1+x1)*i, self.hh-(h2+y2)*(j+1)
                self.createSprite('_initTestColors()', sprites, g1, c[i][j], xx, yy, w1, h2, i, j, v=True, dbg=1)
            self.colorLists.append(sprites)
#        print('_initTestColorLists(End)', file=DBG_FILE)

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
        print('resizeTestColors(END) ww={} x={} w={:7.2f} x+w={:7.2f} ww-x-w={:7.2f} : y={} hh={} h={:7.2f} y+h={:7.2f} hh-y-h={:7.2f}'.format(ww, x1, w1, x1+w1, ww-x1-w1, hh, y2, h2, y2+h2, hh-y2-h2), file=DBG_FILE)
########################################################################################################################################################################################################
    def _initGroups(self):
        for i in range(len(self.n)+3):
            p = None if ORDER_GROUP or i==0 else self.g[i-1]
            self.g.append(self._initGroup(i, p))
            print('_initGroups({}) g={} pg={}'.format(i, self.g[i], self.g[i].parent), file=DBG_FILE)

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
        if dbg: print('geom({}) px={:7.2f} py={:7.2f} pw={:7.2f} ph={:7.2f}  =>  n={:3} x={:4} y={:4} w={:7.2f} h={:7.2f} o={}'.format(j, px, py, pw, ph, n, x, y, w, h, o), file=DBG_FILE)
        if nq and j == Q: n = nq
#        elif nq and j == R: n = self.n[R]
        if init: return n, i, x, y, w, h, o, g
        else:    return n, i, x, y, w, h, o, g, w/self.w[j], h/self.h[j]

    def dumpGeom(self, j, why=''):
        n, i, x, y, w, h, o , g = self.n[j], self.i[j], self.x[j], self.y[j], self.w[j], self.h[j], self.o[j], self.g[j]
        print('{:25} j={} n={:3} i={:4} x={:3} y={:3} w={:7.2f} h={:7.2f} o={} g={}'.format(why, j, n, i, x, y, w, h, o, g), file=DBG_FILE)
########################################################################################################################################################################################################
    def _init(self):
        self.ssi  = 0
        self.cpr  = self.n[K]
        self.cpq  = self.n[Q]*self.cpr
        self.cpl  = self.n[R]*self.cpr + self.n[Q]*self.cpr
        self.cpp  = self.n[L]*self.cpl
        self.tabs, self.pages, self.lines, self.qrows, self.rows, self.cols = [], [], [], [], [], []
        self.readDataFile()
        self.createSprites()
        if self.n[Q]: self.labels = []  ;  self.createLabels(self.g[C+1])
        self.createTabs(  self.g[C+2])
        self.createCursor(self.g[C+3])
        self.dumpStruct('_init')
########################################################################################################################################################################################################
    def readDataFile(self, dbg=1):
        print('readDataFile(BGN) {}'.format(TAB_FILE.name), file=DBG_FILE)
        lines = []
        while 1:
            line = TAB_FILE.readline().strip()
            if len(line) < 1: break
            lines.append(line)
            if dbg: print('{}'.format(line), file=DBG_FILE)
        if dbg: self.dumpData(d=lines, why='readDataFile(lines) before transpose')
        self.data = self.transpose(lines)
        if dbg: self.dumpData(d=self.data, why='readDataFile(lines) after transpose')
        print('readDataFile(END) {}'.format(TAB_FILE.name), file=DBG_FILE)

    def dumpData(self, d=None, why='', l=1, i=8):
        if d is None: d = self.data
        t = self.transpose(d)
        print('dumpData(BGN) l={} i={} ({} x {}) {}'.format(l, i, len(t), len(t[0]), why), file=DBG_FILE)
        if l: self.printCLabels(d, i=i+1)
        for c in range(len(d)):
            if l: print('{:{w}} '.format(c, w=i), file=DBG_FILE, end='')
            for s in range(len(d[c])):
                print('{}'.format(d[c][s]), file=DBG_FILE, end='')
            print(file=DBG_FILE)
        print('dumpData(   ) l={} i={} ({} x {}) [Transpose] {}'.format(l, i, len(d), len(d[0]), why), file=DBG_FILE)
        if l: self.printCLabels(t, i=i+1)
        for c in range(len(t)):
            if l: print('{:{w}} '.format(c, w=i), file=DBG_FILE, end='')
            for s in range(len(t[c])):
                print('{}'.format(t[c][s]), file=DBG_FILE, end='')
            print(file=DBG_FILE)
        print('dumpData(END) l={} i={} ({} x {}) {}'.format(l, i, len(d), len(d[0]), why), file=DBG_FILE)

    @staticmethod
    def printCLabels(d, i=0):
        a = ' ' * len(d[0])  ;  b = ' ' * i
        print('{}'.format(b), file=DBG_FILE, end='')  ;  [print('{}'.format(c//100),   file=DBG_FILE, end='') for c in range(len(d[0]))]  ;  print(file=DBG_FILE)
        print('{}'.format(b), file=DBG_FILE, end='')  ;  [print('{}'.format(c//10%10), file=DBG_FILE, end='') for c in range(len(d[0]))]  ;  print(file=DBG_FILE)
        print('{}'.format(b), file=DBG_FILE, end='')  ;  [print('{}'.format(c%10),     file=DBG_FILE, end='') for c in range(len(d[0]))]  ;  print(file=DBG_FILE)
        print('{}'.format(b), file=DBG_FILE, end='')  ;   print('{}'.format(a),        file=DBG_FILE)

    @staticmethod
    def transpose(d, dbg=0):
        if dbg: print('transpose(BGN) {}'.format(d), file=DBG_FILE)
        t = []
        for c in range(len(d[0])):
            a = []  ;  s = ''  ;  tt = None
            for r in range(len(d)):
                tt = type(d[r])
                if   tt is str:  s += d[r][c]
                elif tt is list: a.append(d[r][c])
            t.append(s) if tt is str else t.append(a)
            if dbg: print('{} {} {}'.format(s, a, t), file=DBG_FILE)
        if dbg: print('transpose(END) {}'.format(t), file=DBG_FILE)
        return t
########################################################################################################################################################################################################
    def createSprites(self):
        print('createSprites(BGN) n={}'.format(self.n), file=DBG_FILE)
        self.dumpSprite()
        cp, cl, cq, cr, cc = [REDS[0], REDS[2], REDS[4], REDS[6], REDS[8], REDS[10]], [GREENS[0], GREENS[2]], [CYANS[0], CYANS[5]], [YELLOWS[0], YELLOWS[3]], [GRAYS[11], GRAYS[7]]
        np, ip, xp, yp, wp, hp, op, gp = self.geom(P, self.x[P], self.y[P], self.ww, self.hh, why='', init=True, dump=0)
        for p in range(np):
            page = self.createSprite('createPages', self.pages, gp, cp[p%len(cp)], xp, yp, wp, hp, p, 0, dbg=1)
            v = True if len(self.pages)==1 else False
            nl, il, xl, yl, wl, hl, ol, gl = self.geom(L, page.x, page.y, page.width, page.height, why='', init=True, dump=0)
            for l in range(nl):
                yyl = page.y + page.height - (hl+yl)*(l+1)
                line = self.createSprite('createLines', self.lines, gl, cl[l%len(cl)], xl, yyl, wl, hl, l, 0, v=v, dbg=1)
                if self.n[Q]:
                    nq, iq, xq, yq, wq, hq, oq, gq = self.geom(Q, line.x, line.y, line.width, line.height, why='', init=True, dump=0, dbg=0)
                    for q in range(nq):
                        yyq = line.y + line.height - (hq+yq)*(q+1)
                        qrow = self.createSprite('createQRow', self.qrows, gq, cq[0], xq, yyq, wq, hq, 0, 0, v=v, dbg=1)
                        nc, ic, xc, yc, wc, hc, oc, gc = self.geom(C, qrow.x, qrow.y, qrow.width, qrow.height, why='', init=True, dump=0)
                        for c in range(nc):
                            xxc, yyc = qrow.x+xc+(wc+xc)*c, qrow.y+qrow.height-(hc+yc)
                            self.createSprite('createCols', self.cols, gc, cc[self.cci(c, cc)], xxc, yyc, wc, hc, c, 0, v=v, dbg=1)
                nr, ir, xr, yr, wr, hr, o, gr = self.geom(R, line.x, line.y, line.width, line.height, why='', init=True, dump=0, dbg=0)
                rr = 1 if self.n[Q] else 0
                for r in range(rr, nr):
                    yyr = line.y + line.height - (hr+yr)*(r+1)
                    row = self.createSprite('createRows', self.rows, gr, cr[r%len(cr)], xr, yyr, wr, hr, r, 0, v=v, dbg=1)
                    nc, ic, xc, yc, wc, hc, oc, gc = self.geom(C, row.x, row.y, row.width, row.height, why='', init=True, dump=0)
                    for c in range(nc):
                        xxc, yyc = row.x + xc + (wc+xc)*c, row.y + row.height - (hc+yc)
                        self.createSprite('createCols', self.cols, gc, cc[self.cci(c, cc)], xxc, yyc, wc, hc, c, 0, v=v, dbg=1)
        self.dumpSprite()
        print('createSprites(END) n={}'.format(self.n), file=DBG_FILE)

    def createSprite(self, why, ps, grp, cc, x, y, w, h, i, j=0, v=None, dbg=0):
        scip = pyglet.image.SolidColorImagePattern(cc)
        img = scip.create_image(width=fri(w), height=fri(h))
        spr = pyglet.sprite.Sprite(img, x, y, batch=self.batch, group=grp, subpixel=SUBPIX)
        spr.visible = v if v is not None else True if i==P else False
        spr.color, spr.opacity = cc[:3], cc[3]
        self.sprites.append(spr)
        if ps is not None: ps.append(spr)
        if TEST: return
        p, l, q, r, c = self.nl()
        if DBG or dbg: why += ' j={}'.format(j)  ;  self.dumpSprite(spr, len(self.sprites), '{:2} {:2} {:2} {:3} {:5} {:16}'.format(p, l, q, r, c, why))
        return spr
########################################################################################################################################################################################################
    def resizeSprites(self, dbg=1):
        n = self.n
        if dbg: print('resizeSprites(BGN) n={}'.format(n), file=DBG_FILE)
        self.dumpSprite()
        i, sp, sl, sq, sr, sc = 0, 0, 0, 0, 0, 0
        np, ip, xp, yp, wp, hp, op, gp, mxp, myp = self.geom(P, self.x[P], self.y[P], self.ww, self.hh, why='', init=False, dump=0)
        for p in range(np):
            page = self.pages[sp] ; page.update(x=xp, y=yp, scale_x=mxp, scale_y=myp)
            sp += 1 ; self.dumpSprite(self.sprites[i], i+1, '{:2} {:2} {:2} {:3} {:5} {:16}'.format(sp, sl, sq, sr, sc, 'resizePages')) ; i += 1
            nl, il, xl, yl, wl, hl, ol, gl, mxl, myl = self.geom(L, page.x, page.y, page.width, page.height, why='', init=False, dump=0)
            for l in range (nl):
                yyl = page.y + page.height - (hl + yl)*(l + 1)
                line = self.lines[sl] ; line.update(x=xl, y=yyl, scale_x=mxl, scale_y=myl)
                sl += 1 ; self.dumpSprite(self.sprites[i], i+1, '{:2} {:2} {:2} {:3} {:5} {:16}'.format(sp, sl, sq, sr, sc, 'resizeLines')) ; i += 1
                if n[Q]:
                    nq, iq, xq, yq, wq, hq, oq, gq, mxq, myq = self.geom(Q, line.x, line.y, line.width, line.height, why='', init=False, dump=0)
                    for q in range(nq):
                        yyq = line.y + line.height - (hq + yq)*(q + 1)
                        qrow = self.qrows[sq] ; qrow.update(x=xq, y=yyq, scale_x=mxq, scale_y=myq)
                        sq += 1 ; self.dumpSprite(self.sprites[i], i+1, '{:2} {:2} {:2} {:3} {:5} {:16}'.format(sp, sl, sq, sr, sc, 'resizeQRows')) ; i += 1
                        nc, ic, xc, yc, wc, hc, oc, gc, mxc, myc = self.geom(C, qrow.x, qrow.y, qrow.width, qrow.height, why='', init=False, dump=0)
                        for c in range(nc):
                            xxc, yyc = qrow.x + xc + (wc + xc)*c, qrow.y + qrow.height - (hc + yc)
                            self.cols[sc].update(x=xxc, y=yyc, scale_x=mxc, scale_y=myc)
                            sc += 1 ; self.dumpSprite(self.sprites[i], i+1, '{:2} {:2} {:2} {:3} {:5} {:16}'.format(sp, sl, sq, sr, sc, 'resizeCols')) ; i += 1
                nr, ir, xr, yr, wr, hr, o, gr, mxr, myr = self.geom(R, line.x, line.y, line.width, line.height, why='', init=False, dump=0)
                rr = 1 if n[Q] else 0
                for r in range(rr, nr):
                    yyr = line.y + line.height - (hr + yr)*(r + 1)
                    row = self.rows[sr] ; row.update(x=xr, y=yyr, scale_x=mxr, scale_y=myr)
                    sr += 1 ; self.dumpSprite(self.sprites[i], i+1, '{:2} {:2} {:2} {:3} {:5} {:16}'.format(sp, sl, sq, sr, sc, 'resizeRows')) ; i += 1
                    nc, ic, xc, yc, wc, hc, oc, gc, mxc, myc = self.geom(C, row.x, row.y, row.width, row.height, why='', init=False, dump=0)
                    for c in range(nc):
                        xxc, yyc = row.x + xc + (wc + xc)*c, row.y + row.height - (hc + yc)
                        self.cols[sc].update(x=xxc, y=yyc, scale_x=mxc, scale_y=myc)
                        sc += 1 ; self.dumpSprite(self.sprites[i], i+1, '{:2} {:2} {:2} {:3} {:5} {:16}'.format(sp, sl, sq, sr, sc, 'resizeCols')) ; i += 1
        self.dumpSprite()
        if dbg: print('resizeSprites(END) n={}'.format(n), file=DBG_FILE)
########################################################################################################################################################################################################
    def dumpSprites(self, why=''):
        n = self.n
        print('dumpSprites(BGN) n={} {}'.format(n, why), file=DBG_FILE)
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
        print('dumpSprites(END) n={} {}'.format(n, why), file=DBG_FILE)

    @staticmethod
    def dumpSprite(s=None, c=-1, why=''):
        if s is None: print(' sid   p  l  q   r  col     why               x      xc        y      yc        w       h    iax  iay    m      mx     my     rot   red green blue opc vsb    group       parent', file=DBG_FILE); return
        f = '{:5} {:16} {:7.2f} {:7.2f}  {:7.2f} {:7.2f}  {:7.2f} {:7.2f} {:4} {:4} {:6.3f} {:6.3f} {:6.3f} {:7.2f}  {:3}  {:3}  {:3}  {:3}  {:1}  {} {}'
        k, o, v, g, p = s.color, s.opacity, s.visible, s.group, s.group.parent
        xc, yc = s.x + s.width/2, s.y + s.height/2
        fs = f.format(c, why, s.x, xc, s.y, yc, s.width, s.height, s.image.anchor_x, s.image.anchor_y, s.scale, s.scale_x, s.scale_y, s.rotation, k[0], k[1], k[2], o, v, g, p)
        print('{}'.format(fs), file=DBG_FILE)
        assert(type(s) == pyglet.sprite.Sprite)
########################################################################################################################################################################################################
    def createCursor(self, g):
        c = self.cursorCol()
        x, y, w, h = self.cols[c].x, self.cols[c].y, self.cols[c].width, self.cols[c].height
        self.cursor = self.createSprite('cursor', None, g, CC, x, y, w, h, 0, 0, v=True)
        print('createCursor()   c={:4} x={:6.1f} y={:6.1f} w={:4} h={:4} i[C]={}'.format(c, x, y, w, h, self.i[C]), file=DBG_FILE)

    def resizeCursor(self):
        c = self.cursorCol()
        x, y, w, h = self.cols[c].x, self.cols[c].y, self.cols[c].width, self.cols[c].height
        self.cursor.update(x=x, y=y, scale_x=self.cols[c].scale_x, scale_y=self.cols[c].scale_y)
        print('resizeCursor()   c={:4} x={:6.1f} y={:6.1f} w={:6.2f} h={:6.2f} i[C]={}'.format(c, x, y, w, h, self.i[C]), file=DBG_FILE)
########################################################################################################################################################################################################
    def createLabels(self, g, dbg=1):
        lid, text = 0, ['R', 'M', '-']
        [text.append('{}'.format(_)) for _ in range(1, self.n[C] + 1)]
        self.dumpTextList(text, 'createLabels(BGN)) text')
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
        w, h, a, b = self.cols[c].width, self.cols[c].height, 'center', self.batch
        k, d, s, n, o, j = self.fontInfo()
        k = FONT_COLORS[-1]
        x, y, = self.cols[c].x + w/2, self.cols[c].y + h/2
        label = pyglet.text.Label(text, font_name=n, font_size=s, bold=o, italic=j, color=k, x=x, y=y, width=w, height=h, anchor_x=a, anchor_y=a, align=a, dpi=d, batch=b, group=g)
        l.append(label)
        return label

    def createTabs(self, g, dbg=1):
        n = self.n
        if dbg: print('createTabs(BGN) n={}'.format(n), file=DBG_FILE)
        self.dumpData(why='createTabs')
        if dbg: self.dumpTab()
        for l in range(n[L]):
            for c in range(n[K]):
                for r in range(n[R]):
                    rc = c + (r + n[Q])*self.cpr + l * self.cpl
                    tc = c + r*self.cpr
                    cc = c + l*self.cpr
                    print('createTabs() l={} r={:2} c={:3} rc={:4} tc={:4} cc={:4}'.format(l, r, c, rc, tc, cc), file=DBG_FILE, end=' ')
                    t = self.createTab(self.tabs, self.data[cc][r], rc, g)
                    if dbg: self.dumpTab(t, tc, r, rc, 'createTabs')
        self.dumpTabs(why='createTabs')
        if dbg: print('createTabs(END) n={}'.format(n), file=DBG_FILE)

    def createTab(self, t, text, c, g):
        w, h, a, b = self.cols[c].width, self.cols[c].height, 'center', self.batch
        k, d, s, n, o, j = self.fontInfo()
        x, y, = self.cols[c].x + w/2, self.cols[c].y + h/2
        tab = pyglet.text.Label(text, font_name=n, font_size=s, bold=o, italic=j, color=k, x=x, y=y, width=w, height=h, anchor_x=a, anchor_y=a, align=a, dpi=d, batch=b, group=g)
        t.append(tab)
        return tab
########################################################################################################################################################################################################
    def resizeLabels(self):
        cpp, cpl, cpq, cpr = self.cps()
        l = list(self.nl())
        print('resizeLabels(BGN) l={} cpp={} cpl={} cpr={}'.format(l, cpp, cpl, cpq, cpr), file=DBG_FILE)
        for q in range(self.n[Q]):
            for c in range(cpr):
                self.resizeLabel(self.labels[c + q*cpr], c + q*cpl)
        self.dumpLabels('resizeLabels')
        print('resizeLabels(END) l={} cpp={} cpl={} cpr={}'.format(l, cpp, cpl, cpq, cpr), file=DBG_FILE)

    def resizeLabel(self, l, c):
        w, h = self.cols[c].width, self.cols[c].height
        x, y = self.cols[c].x + w/2, self.cols[c].y + h/2
        l.x, l.y, l.width, l.height = x, y, w, h

    def resizeTabs(self, dbg=1):
        n = self.n  ;  i = 0
        print('resizeTabs(BGN) n={} cps={}'.format(n, self.cps()), file=DBG_FILE)
        if dbg: self.dumpLabel()
        for l in range(n[L]):
            for c in range(n[K]):
                for r in range(n[R]):
                    t = c + (r + n[Q]) * self.cpr + l * self.cpl
                    self.resizeTab(self.tabs[i], t)
                    i += 1
        self.dumpTabs('resizeTabs')
        print('resizeTabs(END) n={} cps={}'.format(n, self.cps()), file=DBG_FILE)

    def resizeTab(self, t, c):
        w, h = self.cols[c].width, self.cols[c].height
        x, y = self.cols[c].x + w/2, self.cols[c].y + h/2
        t.x, t.y,t.width, t.height = x, y, w, h
########################################################################################################################################################################################################
    def dumpLabels(self, why='', dbg=1):
        cpp, cpl, cpq, cpr = self.cps()
        nq = len(self.qrows)
        if dbg: print('dumpLabels(BGN) nq={} {}'.format(nq, why), file=DBG_FILE)
        self.dumpLabel()
        for q in range(nq):
            for c in range(cpr):
                self.dumpLabel(self.labels[c+q*cpr], c+q*cpr, q, c+q*cpl, why)
        self.dumpLabel()
        if dbg: print('dumpLabels(END) nq={} {})'.format(nq, why), file=DBG_FILE)

    @staticmethod
    def dumpLabel(l=None, lid=-1, q=-1, c=-1, why=''):
        if l is None: print('lid  q   c  text     x       y       w       h      font name      size dpi bold ital red green blue opc  why', file=DBG_FILE) ; return
        x, y, w, h, n, d, s, k, b, i, t = l.x, l.y, l.width, l.height, l.font_name, l.dpi, l.font_size, l.color, l.bold, l.italic, l.text
        print('{:3} {:2} {:4}  {:3} {:7.2f} {:7.2f} {:7.2f} {:7.2f}  {:16}  {:2}  {:3}   {:1}    {:1}  {:3}  {:3}  {:3}  {:3}  {}'.format(lid, q, c, t, x, y, w, h, n, s, d, b, i, k[0], k[1], k[2], k[3], why), file=DBG_FILE)

    def dumpTabs(self, why='', dbg=1):
        n = self.n  ;  i = 0  ;  why = '{:16}'.format(why)
        if dbg: print('dumpTabs(BGN) n={} {}'.format(n, why), file=DBG_FILE)
        self.dumpTab()
        for c in range(n[K]):
            for r in range(n[R]):
                rc = c + (r + n[Q])*self.cpr
                why2 = ' {:5} {:4} {:2} {:3} {:3} {:1}'.format(i, c, r, rc, len(self.data), len(self.data[c]))
                self.dumpTab(self.tabs[i], i, r, rc, why + why2)
                i += 1
        self.dumpTab()
        if dbg: print('dumpTabs(END) n={} {}'.format(n, why), file=DBG_FILE)

    @staticmethod
    def dumpTab(t=None, tid=-1, r=-1, c=-1, why=''):
        if t is None: print('tid  r   c  text     x       y       w       h      font name      size dpi bold ital red green blue opc  why                 i    c   r  rc  ', file=DBG_FILE) ; return
        x, y, w, h, n, d, s, k, b, i, tt = t.x, t.y, t.width, t.height, t.font_name, t.dpi, t.font_size, t.color, t.bold, t.italic, t.text
        print('{:3} {:2} {:4}  {:3} {:7.2f} {:7.2f} {:7.2f} {:7.2f}  {:16}  {:2}  {:3}   {:1}    {:1}  {:3}  {:3}  {:3}  {:3}  {}'.format(tid, r, c, tt, x, y, w, h, n, s, d, b, i, k[0], k[1], k[2], k[3], why), file=DBG_FILE)
########################################################################################################################################################################################################
    def dumpTest(self, why=''):
        self.dumpFont('{}'.format(why))
        self.dumpSprite()
#        for i in range(len(self.colorLists)):
#            self.dumpSprites(self.colorLists[i], why)

    def dumpStruct(self, why=''):
        print('dumpStruct(BGN) {}'.format(why), file=DBG_FILE)
        self.dumpSprites(why)
        self.dumpLabels(why)
        self.dumpData(why=why)
        self.dumpTabs(why)
        self.dumpFont(why)
        self.dumpNums(why)
        self.cursorCol(dbg=1)
        print('dumpStruct(END) {}'.format(why), file=DBG_FILE)
########################################################################################################################################################################################################
    def dumpNums(self, why=''):
        n = self.n  ;  l = list(self.nl())  ;  c = self.cps()
        print('dumpNums() {} n={}  l={}  c={}'.format(why, n, l, c), file=DBG_FILE)

    @staticmethod
    def dumpTextList(text, why=''):
        print('{}[len={}] = [ '.format(why, len(text)), file=DBG_FILE, end='')
        for i in range(len(text)): print('{}'.format(text[i]), file=DBG_FILE, end=' ')
        print(']', file=DBG_FILE)
########################################################################################################################################################################################################
    def on_resize(self, width, height):
        super().on_resize(width, height)
        self.ww, self.hh = width, height
        if TEST: self.resizeTestColors() ; return
        print('on_resize(BGN) {:4} x {:4}'.format(self.ww, self.hh), file=DBG_FILE) ; return
        self.resizeSprites()
        self.resizeLabels()
        self.resizeTabs()
        self.resizeCursor()
        self.dumpStruct('on_resize()')
#        self.updateCaption()
        print('on_resize(END) {:4} x {:4}'.format(self.ww, self.hh), file=DBG_FILE)
########################################################################################################################################################################################################
    def on_draw(self):
        self.clear()
        self.batch.draw()

    def kpEvntTxt(self):
        return 'kbk={:6} symb={:6} symbStr={:12} mods={} modsStr={:26}'.format(self.kbk, self.symb, self.symbStr, self.mods, self.modsStr)

    def on_key_press(self, symb, mods):
        self.symb, self.mods, self.symbStr, self.modsStr = symb, mods, pygwink.symbol_string(symb), pygwink.modifiers_string(mods)
        self.kbk = self.symbStr  ;  kbk = self.kbk
        print('on_key_press(BGN)     {}'.format(self.kpEvntTxt()), file=DBG_FILE)
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

    def on_text(self, text):
        self.kbk = text
        print('on_text(BGN)          {}'.format( self.kpEvntTxt()), file=DBG_FILE)
        if self.isTab(self.kbk):                 self.addTab(self.kbk, 'on_text')
        if self.kbk=='$' and self.isShift(self.mods): self.snapshot()
#        self.updateCaption()

    def on_text_motion(self, motion):
        self.kbk = motion
        print('on_text_motion(BGN)   {}'.format(self.kpEvntTxt()), file=DBG_FILE)
        if self.mods == 0:
            if   motion==pygwink.MOTION_LEFT:          self.move(-1)
            elif motion==pygwink.MOTION_RIGHT:         self.move( 1)
            elif motion==pygwink.MOTION_UP:            self.move(-self.n[K])
            elif motion==pygwink.MOTION_DOWN:          self.move( self.n[K])
#            elif motion==pygwink.MOTION_PREVIOUS_PAGE: self.move() # prevPage(self.i[P], motion)
#            elif motion==pygwink.MOTION_NEXT_PAGE:     self.move() # nextPage(self.i[P], motion)
            else:                                      print('on_text_motion() motion={} ???'.format(motion), file=DBG_FILE)
#            self.updateCaption()
########################################################################################################################################################################################################
    def move(self, c, dbg=1):
        i, cc = self.i[C], self.cursorCol()
        self.i[C] = (i + c) % self.cpp
        k = (cc + c) % self.cpp
        print(        'move({:4}) i[C]={:3} cc={:3} => i[C]={:3} cc={:3}'.format(c, i, cc, self.i[C], k))
        if dbg: print('move({:4}) i[C]={:3} cc={:3} => i[C]={:3} cc={:3}'.format(c, i, cc, self.i[C], k), file=DBG_FILE)
        self.cursor.update(x=self.cols[k].x, y=self.cols[k].y)

    def nextPage(self, i, motion):
        self.pages[i].visible = False
        self.updatePage(i+1, 'nextPage() {}=MOTION_NEXT_PAGE   '.format(motion))

    def prevPage(self, i, motion):
        self.pages[i].visible = False
        self.updatePage(i-1, 'prevPage() {}=MOTION_PREVIOUS_PAGE'.format(motion))

    def updatePage(self, i, why):
        i = i % self.n[P]
        self.pages[i].visible = True
        print('{} i[{}]={}'.format(why, P, i), file=DBG_FILE)
        self.i[P] = i
########################################################################################################################################################################################################
    def addTab(self, kbk, why=''):
        cc = self.cursorCol()
        print('addTab(BGN)           {} : cc={} {}'.format(self.kpEvntTxt(), cc, why), file=DBG_FILE)
        self.updateData(kbk, cc)
        self.updateTab( kbk, cc)
        self.snapshot()
        print('addTab(END)           {} : cc={} {}'.format(self.kpEvntTxt(), cc, why), file=DBG_FILE)

    def on_mouse_release(self, x, y, button, modifiers):  # pyglet.window.mouse.MIDDLE #pyglet.window.mouse.LEFT #pyglet.window.mouse.RIGHT
        np, nl, nq, nr, nc, nk = self.n  ;  n = self.n
        w, h = self.ww/nk, self.hh/((nr + nq)*nl)
        y = self.hh - y
        c, r  = int(x/w), int(y/h) - nq
        i, cc = self.i[C], self.cursorCol()
        print('on_mouse_release(BGN) b={} m={} n={} x={:4} y={:4} w={:6.2f} h={:6.2f} c={:4} r={:4} i={:4} cc={:4}'.format(button, modifiers, n, x, y, w, h, c, r, i, cc), file=DBG_FILE)
        self.i[C] = r * nk + c
        i = self.i[C] + nq * nk
        self.cursor.update(self.cols[i].x, self.cols[i].y)
        cc = self.cursorCol(dbg=0)
        print('on_mouse_release(END) b={} m={} n={} x={:4} y={:4} w={:6.2f} h={:6.2f} c={:4} r={:4} i={:4} cc={:4}'.format(button, modifiers, n, x, y, w, h, c, r, i, cc), file=DBG_FILE)

    def updateData(self, text, cc):
        c, s = self.cs(cc)
        t = self.data[c]
        self.dumpData(why='updateData(BGN) text={} c={} s={} data[c]={}'.format(text, c, s, self.data[c]))
        self.data[c] = t[0:s] + text + t[s+1:]
        self.dumpData(why='updateData(END) text={} c={} s={} data[c]={}'.format(text, c, s, self.data[c]))

    def updateTab(self, text, cc):
        c, s = self.cs(cc)
        t = c * self.n[R] + s
        print('updateTab(BGN) text={} c={} s={} t={} tabs[t].text={}'.format(text, c, s, t, self.tabs[t].text))  ;  print('updateTab(BGN) text={} c={} s={} t={} tabs[t].text={}'.format(text, c, s, t, self.tabs[t].text), file=DBG_FILE)
        self.tabs[t].text = text  ;  self.tabs[t].color = FONT_COLORS[1]
        print('updateTab(END) text={} c={} s={} t={} tabs[t].text={}'.format(text, c, s, t, self.tabs[t].text))  ;  print('updateTab(END) text={} c={} s={} t={} tabs[t].text={}'.format(text, c, s, t, self.tabs[t].text), file=DBG_FILE)

    def updateCaption(self):
        fc, fd, fs, fn, fb, fi = self.fontInfo()
        text = '{}dpi {}pt {} {},{},{},{}'.format(fd, fs, fn, fc[0], fc[1], fc[2], fc[3])
        print('updateCaption() {}'.format(text), file=DBG_FILE)
        self.set_caption(text)
########################################################################################################################################################################################################
    def cs(self, cc): nk, nr, nq = self.n[K], self.n[R], self.n[Q]  ;  return cc % nk + ((cc//nk)//(nq + nr))*nk, ((cc//nk) - nq*(1 + cc//self.cpl)) % nr
    def cps(self): return self.cpp, self.cpl, self.cpq, self.cpr
    def nl(self):  return map(len, [self.pages, self.lines, self.qrows, self.rows, self.cols])
    def ns(self):  return self.n[P], self.n[L], self.n[Q], self.n[R], self.n[C], self.n[K]

    def cci(self, c, cc):
        if c == 0: self.ci = (self.ci + 1) % len(cc)
        return (c + self.ci) % len(cc)

    def cursorCol(self, dbg=0):
        p, l, q, r, c = self.i
        cpp, cpl, cpq, cpr = self.cps()
        cc = p*cpp + l*cpl + q*cpq + r*cpr + c
        if dbg: print('cursorCol() cc = ({}*{} + {}*{} + {}*{} + {}*{} + {} + {}) = ({} + {} + {} + {} + {}) = {}'.format(p, cpp, l, cpl, q, cpq, r, cpr, c, CCC, p*cpp, l*cpl, q*cpq, r*cpr, c, cc), file=DBG_FILE)
        return cc
########################################################################################################################################################################################################
    def dumpFont(self, why=''):
        fc, dpi, fs, fn, fb, fi = self.fontInfo()
        pix = FONT_SCALE*fs/dpi
        print('dumpFont({}) {} {}DPI {}pt {} ({:6.3f}*{}pt/{}DPI)={:6.3f}pixels'.format(why, fc, dpi, fs, fn, FONT_SCALE, fs, dpi, pix), file=DBG_FILE)

    def fontInfo(self): return FONT_COLORS[self.fontColorIndex], FONT_DPIS[self.fontDpiIndex], FONT_SIZES[self.fontSizeIndex], FONT_NAMES[self.fontNameIndex], self.fontBold, self.fontItalic
    def updateFontColor(self, ii): self.fontColorIndex = self.updateFontIndex(ii, self.fontColorIndex, FONT_COLORS, 'FONT_COLORS')
    def updateFontDpi(  self, ii): self.fontDpiIndex   = self.updateFontIndex(ii, self.fontDpiIndex,   FONT_DPIS,   'FONT_DPIS')
    def updateFontName( self, ii): self.fontNameIndex  = self.updateFontIndex(ii, self.fontNameIndex,  FONT_NAMES,  'FONT_NAMES')
    def updateFontSize( self, ii): self.fontSizeIndex  = self.updateFontIndex(ii, self.fontSizeIndex,  FONT_SIZES,  'FONT_SIZES')

    def updateFontIndex(self, ii, index, prop, name):
        i = (index + ii) % len(prop)
        errMsg = '*ERROR* Dpi Read-Only'
        if name=='FONT_DPIS': i = self.fontDpiIndex ; print('{} {} {}[{}]={} {}'.format(errMsg, self.kpEvntTxt(), name, i, prop[i], errMsg), file=DBG_FILE)  ;  return self.fontDpiIndex
        print('updateFontIndex({:2})   {} {}[{}]={}'.format(ii, self.kpEvntTxt(), name, i, prop[i]), file=DBG_FILE)
        for j in range(len(self.tabs)):
            if   name == 'FONT_COLORS': self.tabs[j].color     = prop[i]
            elif name == 'FONT_NAMES':  self.tabs[j].font_name = prop[i]
            elif name == 'FONT_SIZES':  self.tabs[j].font_size = prop[i]
            elif name == 'FONT_DPIS':   self.tabs[j].dpi       = prop[i]
        if self.n[Q]:
            for j in range(len(self.labels)):
                if   name == 'FONT_COLORS': self.labels[j].color     = prop[i]
                elif name == 'FONT_NAMES':  self.labels[j].font_name = prop[i]
                elif name == 'FONT_SIZES':  self.labels[j].font_size = prop[i]
                elif name == 'FONT_DPIS':   self.labels[j].dpi       = prop[i]
        return i

    def toggleFontBold(self):
        print('toggleFontBold() {:1} => {:1}'.format(self.fontBold, not self.fontBold), file=DBG_FILE)
        self.fontBold = not self.fontBold
        for j in range(len(self.tabs)):
            self.tabs[j].bold = self.fontBold
        if self.n[Q]:
            for j in range(len(self.labels)):
                self.labels[j].bold = self.fontBold

    def toggleFontItalic(self):
        print('toggleFontItalic() {:1} => {:1}'.format(self.fontItalic, not self.fontItalic), file=DBG_FILE)
        self.fontItalic = not self.fontItalic
        for j in range(len(self.tabs)):
            self.tabs[j].italic = self.fontItalic
        if self.n[Q]:
            for j in range(len(self.labels)):
                self.labels[j].italic = self.fontItalic
########################################################################################################################################################################################################
    def on_mouse_release_OLD(self, x, y, button, modifiers):  # pyglet.window.mouse.MIDDLE #pyglet.window.mouse.LEFT #pyglet.window.mouse.RIGHT
        nc, nr = self.n[K], self.n[R] * self.n[L]
        w, h = self.ww/nc, self.hh/nr
        y = self.hh - y
        c, r, i = int(x/w), int(y/h), self.i[C]
        print('on_mouse_release({},{}) BGN nc={} nr={} x={:4} y={:4} w={:6.2f} h={:6.2f} c={:4} r={:4} i={}'.format(button, modifiers, nc, nr, x, y, w, h, c, r, i), file=DBG_FILE)
        self.i[C] = r * nc + c
        j = self.i[C]
        self.cursor.update(self.cols[j].x, self.cols[j].y)
        print('on_mouse_release({},{}) END nc={} nr={} x={:4} y={:4} w={:6.2f} h={:6.2f} c={:4} r={:4} i={}'.format(button, modifiers, nc, nr, x, y, w, h, c, r, j), file=DBG_FILE)

    def toggleColorLists(self, motion):
        if not TEST: print('toggleColorLists(WARNING) Nothing To Toggle TEST={} motion={}'.format(TEST, motion), file=DBG_FILE) ; return
        cls = self.colorLists
        i = self.i[P]
        print('toggleColorLists() i={}'.format(i), file=DBG_FILE)
        if motion==pygwink.MOTION_LEFT:
            for j in range(len(cls[i])): cls[i][j].visible = False
            i -= 1
            i = i % len(COLORS)
            for j in range(len(cls[i])): cls[i][j].visible = True
            print('toggleColorLists() MOTION_LEFT={} i[P]={} len(cls)={}'.format(motion, i, len(cls)), file=DBG_FILE)
        elif motion==pygwink.MOTION_RIGHT:
            for j in range(len(cls[i])): cls[i][j].visible = False
            i += 1
            i = i % len(COLORS)
            for j in range(len(cls[i])): cls[i][j].visible = True
            print('toggleColorLists() MOTION_RIGHT={} i[P]={} len(cls)={}'.format(motion, i, len(cls)), file=DBG_FILE)
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
        name = os.path.basename(sys.argv[0])
        file  = '{}{}.snap.{}.png'.format(name, SFX, self.ssi)
        filePath = '{}/{}'.format(self.snapPath, file)
        print('snapshot() file={} filePath={}'.format(file, filePath), file=DBG_FILE)
        pyglet.image.get_buffer_manager().get_color_buffer().save('{}'.format(filePath))
        self.ssi += 1

    def quit(self, why=''):
        text = '###   Quit   ###' * 13
        print('\n{}\n'.format(text), file=DBG_FILE)
        self.dumpStruct('quit ' + why) if not TEST else self.dumpTest('quit() ' + why)
        print('quit() {}\nExiting'.format(why), file=DBG_FILE)
        self.snapshot()
        exit()
########################################################################################################################################################################################################
if __name__=='__main__':
    TEST = 0  ;  CARET = 0  ;  ORDER_GROUP = 1  ;  SUBPIX = 1  ;  FULL_SCREEN = 0  ;  VRSN = 1  ;  DBG = 0
    SFX           = 'TEST' if TEST else '.{}'.format(VRSN)
    SNAP_DIR     = 'snaps'  ;  DATA_DIR = 'data'
    DBG_FILE      = open(sys.argv[0] + SFX + ".log.txt", 'w')
    TAB_FILE      = open(sys.argv[0] + SFX + ".dat.txt", 'r')
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
    def genColors(cp, nsteps=HUES):
        colors, clen = [], len(cp[0])
        diffs = [cp[1][i] - cp[0][i] for i in range(clen)]
        steps = [diffs[i]/nsteps     for i in range(clen)]
        if DBG: print('genColors(), c1={} c2={} nsteps={} diffs={} steps={}'.format(cp[0], cp[1], nsteps, diffs, steps), file=DBG_FILE)
        for j in range(nsteps):
            c = tuple([fri(cp[0][i]+j*steps[i]) for i in range(len(cp[0]))])
            if DBG: print('genColors() c[{}]={}'.format(j, c), file=DBG_FILE)
            colors.append(c)
        if DBG: print('genColors() colors={}'.format(cp), file=DBG_FILE)
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
#        print('dumpSpriteCount({}) p={} lpp={} l={} qpl={} q={} rpl={} r={} cpr={} c={}'.format(why, p, self.n[L], l, self.n[Q], q, self.n[R], r, self.n[C], c), file=DBG_FILE)
#        print('dumpSpriteCount({}) p={}   +   l={}   +   q={}   +   r={}   +    c={} = {}'.format(why, p, l, q, r, c, p + l + q + r + c), file=DBG_FILE)

    '''
    def col2spr(self, i):
        cpr = self.n[C] + CCC
        cpl = self.n[R]*cpr
        cpp = self.n[L]*cpl
        p = i//cpp
        l = i//cpl
        q = l
        r = i//cpr
        c = i - p - l - q - r
        return p, l, q, r, c

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
########################################################################################################################################################################################################
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
#            print('ln={} n={} r={}'.format(ln, n, r), file=DBG_FILE)
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
    #        print('dumpTexts(BGN) {} ({}x{}):'.format(why, ns, nc), file=DBG_FILE)
    #        for cc in range(nc):
    #            for ss in range(ns):
    #                l = self.texts[cc][ss][0]
    #                x, y, w, h, n, d, s, c, b, i, t = l.x, l.y, l.width, l.height, l.font_name, l.dpi, l.font_size, l.color, l.bold, l.italic, l.text
    #                print('{:3} {:3} {:7.2f} {:7.2f} {:7.2f} {:7.2f}  {:16}  {:2}  {:3}   {:1}   {:1}  ({:3},{:3},{:3},{:3})  {}'.format(ss, cc, x, y, w, h, n, s, d, b, i, c[0], c[1], c[2], c[3], t), file=DBG_FILE)
    #        print('dumpTexts(END) {} ({}x{})'.format(why, ns, nc), file=DBG_FILE)
    ########################################################################################################################################################################################################
    '''
