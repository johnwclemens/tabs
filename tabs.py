import math, sys, os
import unicodedata
import pyglet
import pyglet.window.key as pygwink
import pyglet.window.event as pygwine

sys.path.insert(0, os.path.abspath('../lib'))
import cmdArgs

class Tabs(pyglet.window.Window):
    def __init__(self):
        self.fontNameIndex, self.fontColorIndex, self.fontSizeIndex, self.fontDpiIndex = 7, 0, 6, 3
        global FULL_SCREEN, SUBPIX, ORDER_GROUP, RUN_TEST
        self.ww, self.hh  = 640, 480
        if RUN_TEST: self.n, self.i, self.x, self.y, self.w, self.h, self.o, self.g = [12, 12, 0, 0], [0, 0, 0, 0], [4, 0, 0, 0], [0, 3, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [1, 1, 0, 0], []
        else:        self.n, self.i, self.x, self.y, self.w, self.h, self.o, self.g =  [3, 3, 6, 30], [0, 0, 0, 0], [0, 4, 0, 0], [0, 4, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [2, 0, 0, 3], []
        self.argMap = cmdArgs.parseCmdLine(dbg=1)
        print('_init(BGN) argMap={}'.format(self.argMap), file=DBG_FILE)
        if 'n' in self.argMap and len(self.argMap['n'])  > 0: self.n            = [int(self.argMap['n'][i]) for i in range(len(self.argMap['n']))]
        if 'x' in self.argMap and len(self.argMap['x'])  > 0: self.x            = [int(self.argMap['x'][i]) for i in range(len(self.argMap['x']))]
        if 'y' in self.argMap and len(self.argMap['y'])  > 0: self.y            = [int(self.argMap['y'][i]) for i in range(len(self.argMap['y']))]
        if 'w' in self.argMap and len(self.argMap['w'])  > 0: self.ww           =  int(self.argMap['w'][0])
        if 'h' in self.argMap and len(self.argMap['h'])  > 0: self.hh           =  int(self.argMap['h'][0])
        if 'o' in self.argMap and len(self.argMap['o'])  > 0: self.o            = [int(self.argMap['o'][i]) for i in range(len(self.argMap['o']))]
        if 'i' in self.argMap and len(self.argMap['i'])  > 0: self.i            = [int(self.argMap['i'][i]) for i in range(len(self.argMap['i']))]
        if 'f' in self.argMap and len(self.argMap['f']) == 0: FULL_SCREEN       = True
        if 'g' in self.argMap and len(self.argMap['g']) == 0: ORDER_GROUP       = True
        if 's' in self.argMap and len(self.argMap['s']) == 0: SUBPIX            = True
        if 't' in self.argMap and len(self.argMap['t']) == 0: RUN_TEST          = True
        print('[n]            n={}'.format(self.n),          file=DBG_FILE)
        print('[x]            x={}'.format(self.x),          file=DBG_FILE)
        print('[y]            y={}'.format(self.y),          file=DBG_FILE)
        print('[w]           ww={}'.format(self.ww),         file=DBG_FILE)
        print('[h]           hh={}'.format(self.hh),         file=DBG_FILE)
        print('[o]            o={}'.format(self.o),          file=DBG_FILE)
        print('[i]            i={}'.format(self.i),          file=DBG_FILE)
        print('[f]  FULL_SCREEN={}'.format(FULL_SCREEN),     file=DBG_FILE)
        print('[g]  ORDER_GROUP={}'.format(ORDER_GROUP),     file=DBG_FILE)
        print('[s]       SUBPIX={}'.format(SUBPIX),          file=DBG_FILE)
        print('[t]     RUN_TEST={}'.format(RUN_TEST),        file=DBG_FILE)
        self._initWindowA()
        super().__init__(screen=self.screens[1], fullscreen=FULL_SCREEN, resizable=True, visible=False)
        self._initWindowB()
        self.symbol, self.modifiers, self.symbolStr, self.modsStr = 0, 0, '', ''
        self._init() if not RUN_TEST else self._initTestColorLists()
        print('_init(END)'.format(), file=DBG_FILE)

    def _initWindowA(self):
        display      = pyglet.canvas.get_display()
        self.screens = display.get_screens()

    def _initWindowB(self):
        self.batch = pyglet.graphics.Batch()
        self._initGroups()
        print('_initWindowB(BGN) {}x{}'.format(self.ww, self.hh), file=DBG_FILE)
        self.set_visible()
        self.set_size(self.ww, self.hh)
        self.ww, self.hh = self.get_size()
        self.eventLogger = pygwine.WindowEventLogger()
        self.push_handlers(self.eventLogger)
#        print('_initWindowB(END) {}x{}'.format(self.ww, self.hh), file=DBG_FILE)

    def _initGroups(self):
        for i in range(len(self.n)+3):
            pg = None if ORDER_GROUP or i==0 else self.g[i-1]
            self.g.append(self._initGroup(i, pg))
            print('_initGroups({}) g={} pg={}'.format(i, self.g[i], self.g[i].parent), file=DBG_FILE)

    @staticmethod
    def _initGroup(order=0, parent=None):
        return pyglet.graphics.OrderedGroup(order, parent) if ORDER_GROUP else pyglet.graphics.Group(parent)
#        if ORDER_GROUP: return pyglet.graphics.OrderedGroup(order, parent)
#        else:           return pyglet.graphics.Group(parent)

    def _initTestColorLists(self):
#        self.clGroup = self._initGroup(0)
        self.colorLists = []
        n1, i1, x1, y1, w1, h1, o1, g1 = self.geom(0, 0, 0, self.ww, self.hh, '_initTestColorLists(0)', init=True, dump=0)
        n2, i2, x2, y2, w2, h2, o2, g2 = self.geom(1, 0, 0, self.ww, self.hh, '_initTestColorLists(1)', init=True, dump=0)
        for i in (P, L): self.dumpGeom(i, '_initTestColorLists() i={}'.format(i))
        c = COLORS
#        end = ['\n', ' '];        [[print('{:2} {:2} {:3} {:3} {:3} {:3}'.format(i, j, c[i][j][0], c[i][j][1], c[i][j][2], c[i][j][3]), file=DBG_FILE, end=end[0 if j==n2-1 else 1]) for j in range(n2)] for i in range(n1)]
        self.dumpSprite('')
        for i in range(n1):
            sprites = []
            for j in range(n2):
                xx, yy = x1+(w1+x1)*i, self.hh-(h2+y2)*(j+1)
                spr = self.createSprite('_initTestColorLists()', g1, c[i][j], xx, yy, w1, h2, i, j, v=True)
                sprites.append(spr)
            self.colorLists.append(sprites)
#        print('_initTestColorLists(End)', file=DBG_FILE)

    def resizeTestColorLists(self):
        cls = self.colorLists
        ww, hh = self.ww, self.hh
        n1, i1, x1, y1, w1, h1, o1, g1, mx, my = self.geom(0, 0, 0, ww, hh, 'resizeTestColorLists(0)', init=False, dump=0)
        n2, i2, x2, y2, w2, h2, o2, g2, mx, my = self.geom(1, 0, 0, ww, hh, 'resizeTestColorLists(1)', init=False, dump=0)
        for i in range(n1):
            for j in range(n2):
                xx, yy = x1+(w1+x1)*i, hh-(h2+y2)*(j+1)
                cls[i][j].update(x=xx, y=yy, scale_x=w1/self.w[P], scale_y=h2/self.h[L])
                self.dumpSprite('{:20} {:3} {:3} {:7.2f} {:7.2f} {:7.2f} {:7.2f}'.format('resizeTestColorLists()', i, j, xx, yy, w1, h2), cls[i][j])
        print('resizeTestColorLists(END) ww={} x={} w={:7.2f} x+w={:7.2f} ww-x-w={:7.2f} : y={} hh={} h={:7.2f} y+h={:7.2f} hh-y-h={:7.2f}'.format(ww, x1, w1, x1+w1, ww-x1-w1, hh, y2, h2, y2+h2, hh-y2-h2), file=DBG_FILE)

    def geom(self, j, px, py, pw, ph, reason='', init=False, dump=3):
        n, i, x, y, w, h, o , g = self.n[j], self.i[j], self.x[j], self.y[j], self.w[j], self.h[j], self.o[j], self.g[j]
        if   j==C: n+=CCC
        if   o==0: w, h =  pw-2*x,        (ph-y*(n+1))/n
        elif o==1: w, h = (pw-x*(n+1))/n, (ph-y*(n+1))/n
        elif o==2: w, h =  pw-2*x,         ph-2*y
        elif o==3: w, h = (pw-x*(n+1))/n,  ph-2*y
        if init: self.w[j], self.h[j] = w, h
        if o!=3: x += px #; y = py+ph-y
        if dump==1 or dump==3: self.dumpGeom(j, reason)
        if dump==2 or dump==3: self.dumpSprite('')
#        print('geom({}) px={:7.2f} py={:7.2f} pw={:7.2f} ph={:7.2f}  =>  n={:3} x={:4} y={:4} w={:7.2f} h={:7.2f} o={}'.format(j, px, py, pw, ph, n, x, y, w, h, o), file=DBG_FILE)
        if init: return n, i, x, y, w, h, o, g
        else:    return n, i, x, y, w, h, o, g, w/self.w[j], h/self.h[j]

    def dumpGeom(self, j, reason=''):
        n, i, x, y, w, h, o , g = self.n[j], self.i[j], self.x[j], self.y[j], self.w[j], self.h[j], self.o[j], self.g[j]
        print('{:25} j={} n={:3} i={:4} x={:3} y={:3} w={:7.2f} h={:7.2f} o={} g={}'.format(reason, j, n, i, x, y, w, h, o, g), file=DBG_FILE)

    def createSprite(self, reason, grp, cc, x, y, w, h, i, j, v=None):#        img.anchor_x, img.anchor_y = fri(w/2), fri(h/2)
        scip = pyglet.image.SolidColorImagePattern(cc)
        img = scip.create_image(width=fri(w), height=fri(h))
        spr = pyglet.sprite.Sprite(img, x, y, batch=self.batch, group=grp, subpixel=SUBPIX)
        spr.visible = v if v is not None else True if i==P else False
        spr.color = cc[:3]
        spr.opacity = cc[3]
        if DBG: self.dumpSprite('{:20} {:3} {:3} {:7.2f} {:7.2f} {:7.2f} {:7.2f} {:4} {:4} {} {}'.format(reason, i, j, x, y, w, h, img.anchor_x, img.anchor_y, spr.group, spr.group.parent), spr)
        return spr

    @staticmethod
    def dumpSprite(reason, s=None):
        if s is None: print('    x       y       w       h    iax  iay    m      mx     my     rot   opacity    color    visible     reason         i   j      x       y       w       h    iax  iay', file=DBG_FILE); return
        f = '{:7.2f} {:7.2f} {:7.2f} {:7.2f} {:4} {:4} {:6.3f} {:6.3f} {:6.3f} {:7.2f}  {:4}  ({:3}, {:3}, {:3})  {:1}'
        c = s.color
        fs = f.format(s.x, s.y, s.width, s.height, s.image.anchor_x, s.image.anchor_y, s.scale, s.scale_x, s.scale_y, s.rotation, s.opacity, c[0], c[1], c[2], s.visible)
        print('{} {}'.format(fs, reason), file=DBG_FILE)
        assert(type(s) == pyglet.sprite.Sprite)

    def _init(self):
        self.pages, self.lines, self.rows, self.cols, self.labels = [], [], [], [], []
        self._initPages()
        self._initLabels(self.g[C+1])
        self._initData(  self.g[C+2])
        self._initCursor(self.g[C+3])
        if CARET: self._initCaret()
        self.dumpFont('_init()')
        self.dumpStruct('_init(END)')

    def _initData(self, g):
        self.data = []
        self.texts = []
        self.STRING_NUMS  = ['1', '2', '3', '4', '5', '6']
        self.stringNames  = ['E', 'B', 'G', 'D', 'A', 'E']
        self.capoFretNums = ['0', '0', '0', '0', '0', '0']
        print('STRING_NUMS={}'.format(self.STRING_NUMS),   file=DBG_FILE)
        print('stringNames={}'.format(self.stringNames),   file=DBG_FILE)
        print('capoFretNums={}'.format(self.capoFretNums), file=DBG_FILE)
        data = ['-', '-', '-', '-', '-', '-']
        self.data    = [data]*(self.n[C]+CCC)
        self.data[0] = self.STRING_NUMS
        self.data[1] = self.stringNames
        self.data[2] = self.capoFretNums
        cc = self.cursorCol()
        for c in range(len(self.data)):
            for s in range(len(self.data[c])):
                self.texts.append(self._initText(self.data[c][s], cc+c+s*(self.n[C]+CCC), g))
        self.dumpData()
        print('data={}'.format(self.data), file=DBG_FILE)

    def dumpData(self, reason=''):
        print('dumpData({}):'.format(reason), file=DBG_FILE)
        for c in self.data:
            for s in c:
                print('{}'.format(s), file=DBG_FILE, end='')
            print(file=DBG_FILE)

    def printData(self):
        pass

    def _initCaret(self):
        doc = pyglet.text.document.FormattedDocument()
        w, h, b, g = self.cols[0].width, self.cols[0].height, self.batch, self.g[C+3]
        layout = pyglet.text.layout.IncrementalTextLayout(document=doc, width=w, height=h, batch=b, group=g)
        self.caret = pyglet.text.caret.Caret(layout, batch=self.batch, color=(200, 255, 200))

    def _initPages(self):
        cc = [REDS[0], REDS[2], REDS[4], REDS[6], REDS[8], REDS[10]]
        n, i, x, y, w, h, o, g = self.geom(P, self.x[P], self.y[P], self.ww, self.hh, reason='', init=True, dump=0)
        for p in range(n):
            page = self.createSprite('_initPages', g, cc[p%len(cc)], x, y, w, h, p, 0)
            self.pages.append(page)
            if self.n[P+1] > 0: lines = self._initLines(page)
        return self.pages

    def _initLines(self, spr):
        cc = [CYANS[0], CYANS[5]]
        n, i, x, y, w, h, o, g = self.geom(L, spr.x, spr.y, spr.width, spr.height, reason='', init=True, dump=0)
        for l in range(n):
            yy = spr.y+spr.height-(h+y)*(l+1)
            line   = self.createSprite('_initLines', g, cc[l%len(cc)], x, yy, w, h, l, 0, v=True if len(self.pages)==1 else False)
            self.lines.append(line)
            if self.n[L+1] > 0: rows = self._initRows(line)
#            self._initLineLabels(spr, self.g[C+1])
        return self.lines

    def _initLabels(self, g):
        labels, n = ['R', 'M', '@'], self.n[C]
        [labels.append('{}'.format(c)) for c in range(1, n+1)]
        self.labels.append(self._initText(labels, 0, g))

    def _initLabels_NEW(self, spr, g):
        cc = [ORANGES[0], ORANGES[5]]
        n, i, x, y, w, h, o, gg = self.geom(R, spr.x, spr.y, spr.width, spr.height, reason='', init=True, dump=0)
        yy = spr.y+spr.height-(h+y)
        row = self.createSprite('_initLineLabels', g, cc[0], x, yy, w, h, 0, 0, v=True if len(self.pages)==1 else False)
        labels, n = ['R', 'M', '@'], self.n[C]
        [labels.append('{}'.format(c)) for c in range(1, n+1)]
        self.labels.append(self._initText(labels, 0, g))

    def _initRows(self, spr):
        cc = [YELLOWS[0], YELLOWS[5]]
        n, i, x, y, w, h, o, g = self.geom(R, spr.x, spr.y, spr.width, spr.height, reason='', init=True, dump=0)
        for r in range(n):
            yy = spr.y+spr.height-(h+y)*(r+1)
            row   = self.createSprite('_initRows', g, cc[r%len(cc)], x, yy, w, h, r, 0, v=True if len(self.pages)==1 else False)
            self.rows.append(row)
            if self.n[R+1] > 0: cols = self._initCols(row)
        return self.rows

    def _initCols(self, spr):
#        a, b = 6, 3; cc = [GREENS[a], GREENS[b]] if len(self.rows)%2 else [GREENS[b], GREENS[a]]
        a, b = 11, 8; cc = [GRAYS[a], GRAYS[b]] if len(self.rows)%2 else [GRAYS[b], GRAYS[a]]
        (n, i, x, y, w, h, o, g), s = self.geom(C, spr.x, spr.y, spr.width, spr.height, reason='', init=True, dump=0), len(cc)
        for c in range(n):
            xx, yy = spr.x+x+(w+x)*c, spr.y+spr.height-(h+y)
            col   = self.createSprite('_initCols', g, cc[c%s], xx, yy, w, h, c, 0, v=True if len(self.pages)==1 else False)
            self.cols.append(col)
        return self.cols

    def cursorCol(self):
        p, l, r, c = self.i[P], self.i[L], self.i[R], self.i[C]
        cpr = self.n[C] + CCC
        cpl = self.n[R]*cpr
        cpp = self.n[L]*cpl
        col = p*cpp + l*cpl + (r+1)*cpr + c + CCC
        print('cursorCol() cpp={} cpl={} cpr={}   p={} l={} r={} c={}   col=(p*cpp={} + l*cpl={} + (r+1)*cpr={} + c={} + CCC={})=col={}'.format(cpp, cpl, cpr, p, l, r, c, p*cpp, l*cpl, (r+1)*cpr, c, CCC, col), file=DBG_FILE)
        return col

    def _initCursor(self, g):
        c = self.cursorCol()
        x, y, w, h = self.cols[c].x, self.cols[c].y, self.cols[c].width, self.cols[c].height
        self.cursor = self.createSprite('cursor', g, CC, x, y, w, h, 0, 0, v=True)
        print('_initCursor()   c={:4} x={:6.1f} y={:6.1f} w={:4} h={:4} i[C]={}'.format(c, x, y, w, h, self.i[C]), file=DBG_FILE)

    def _initText(self, text, c, g, b=None):
        if b is None: b = self.batch
        print('_initText(BGN)  c={:4}  txt:'.format(c), file=DBG_FILE, end='')
        w, h, txt = self.cols[c].width, self.cols[c].height, []
        fc, dpi, fs, fn = self.fontInfo()
        for t in text: print('{}'.format(t), file=DBG_FILE, end='')
        print(file=DBG_FILE)
        for i in range(len(text)):
            x, y = self.cols[c+i].x+w/2, self.cols[c+i].y+h/2
            txt.append(pyglet.text.Label(text[i], font_name=fn, font_size=fs, color=fc, x=x, y=y, anchor_x='center', anchor_y='center', align='center', dpi=dpi, batch=b, group=g))
            print('_initText( {:2} ) c={:4} x={:6.1f} y={:6.1f} w={:4} h={:4}'.format(text[i], c, x, y, w, h), file=DBG_FILE)
        return txt

    def on_resize(self, width, height):
        super().on_resize(width, height)
        self.ww, self.hh = width, height
        if RUN_TEST: self.resizeColorLists(); return
        for i in range(len(self.n)): self.dumpGeom(i, 'on_resize({}x{})'.format(self.ww, self.hh))
        self.resizePages()
        self.resizeLabels()
        self.resizeData()
        self.resizeCursor()
        if CARET: self.resizeCaret()
        self.dumpFont('_init()')
        self.dumpStruct('on_resize()')
        self.updateCaption()

    def resizeLabels(self):
        for c in range(len(self.labels)):
            self.resizeText(self.labels[c], c)

    def resizeData(self):
        cc = self.n[C]+CCC
        for c in range(len(self.texts)):
            self.resizeText(self.texts[c], (c%self.n[R]+1)*cc+c//self.n[R])

    def resizeText(self, text, c):
        for i in range(len(text)):
            w, h = self.cols[c+i].width, self.cols[c+i].height
            x, y = self.cols[c+i].x+w/2, self.cols[c+i].y+h/2
            text[i].x, text[i].y, text[i].width, text[i].height = x, y, w, h
            print('resizeText({:4}) c={:4} x={:6.1f} y={:6.1f} w={:6.1f} h={:6.1f}'.format(text[i].text, c, x, y, w, h), file=DBG_FILE)

    def resizeCursor(self):
        c = self.cursorCol()
        x, y, w, h = self.cols[c].x, self.cols[c].y, self.cols[c].width, self.cols[c].height
        self.cursor.update(x=x, y=y, scale_x=self.cols[c].scale_x, scale_y=self.cols[c].scale_y)
        print('resizeCursor()   c={:4} x={:6.1f} y={:6.1f} w={:6.2f} h={:6.2f} i[C]={}'.format(c, x, y, w, h, self.i[C]), file=DBG_FILE)

    def resizeCaret(self):
        pass

    def resizePages(self):
        n, i, x, y, w, h, o, g, mx, my = self.geom(P, self.x[P], self.y[P], self.ww, self.hh, reason='', init=False, dump=0)
        for p in range(n):
            self.pages[p].update(x=x, y=y, scale_x=mx, scale_y=my)
            if DBG: self.dumpSprite('{:20} {:3} {:3} {:7.2f} {:7.2f} {:7.2f} {:7.2f}'.format('on_resize Pages', p, 0, x, y, w, h), self.pages[p])
            if self.n[P+1] > 0: self.resizeLines(self.pages[p], p)

    def resizeLines(self, spr, pn):
        n, i, x, y, w, h, o, g, mx, my = self.geom(L, spr.x, spr.y, spr.width, spr.height, reason='', init=False, dump=0)
        for l in range(n):
            yy = spr.y+spr.height-(h+y)*(l+1)
            self.lines[l+pn*n].update(x=x, y=yy, scale_x=mx, scale_y=my)
            if DBG: self.dumpSprite('{:20} {:3} {:3} {:7.2f} {:7.2f} {:7.2f} {:7.2f}'.format('on_resize Lines', l, 0, x, yy, w, h), self.lines[l+pn*n])
            if self.n[L+1] > 0: self.resizeRows(self.lines[l+pn*n], l+pn*n)

    def resizeRows(self, spr, ln):
        n, i, x, y, w, h, o, g, mx, my = self.geom(R, spr.x, spr.y, spr.width, spr.height, reason='', init=False, dump=0)
        for r in range(n):
            yy = spr.y+spr.height-(h+y)*(r+1)
            self.rows[r+ln*n].update(x=x, y=yy, scale_x=mx, scale_y=my)
            if DBG: self.dumpSprite('{:20} {:3} {:3} {:7.2f} {:7.2f} {:7.2f} {:7.2f}'.format('on_resize Rows', r, 0, x, yy, w, h), self.rows[r+ln*n])
            if self.n[R+1] > 0: self.resizeCols(self.rows[r+ln*n], r+ln*n)

    def resizeCols(self, spr, rn):
        n, i, x, y, w, h, o, g, mx, my = self.geom(C, spr.x, spr.y, spr.width, spr.height, reason='', init=False, dump=0)
        for c in range(n):
            xx, yy = spr.x+x+(w+x)*c, spr.y+spr.height-(h+y)
            self.cols[c+rn*n].update(x=xx, y=yy, scale_x=mx, scale_y=my)
            if DBG: self.dumpSprite('{:20} {:3} {:3} {:7.2f} {:7.2f} {:7.2f} {:7.2f}'.format('on_resize Cols', c, 0, xx, yy, w, h), self.cols[c+rn*n])

    def dumpStruct(self, reason=''):
        print('dumpStruct({})\n    {}:Pages {}:LinesPerPage {}:Lines {}:RowsPerLine {}:Rows {}:ColsPerRow {}:Cols'.format(reason, len(self.pages), self.n[L], len(self.lines), self.n[R], len(self.rows), self.n[C], len(self.cols)), file=DBG_FILE)
        for i in range(len(self.n)):
            self.dumpGeom(i)
#            self.dumpGeom(i, 'dumpStruct({})'.format(reason))

    def dumpFont(self, reason=''):
        fc, dpi, fs, fn = self.fontInfo(); pix = FONT_SCALE*fs/dpi
        print('dumpFont({}) {} {}DPI {}pt {} ({:6.3f}*{}pt/{}DPI)={:6.3f}pixels'.format(reason, fc, dpi, fs, fn, FONT_SCALE, fs, dpi, pix), file=DBG_FILE)

    def on_draw(self):
        self.clear()
        self.batch.draw()

    def kbpEvntTxt(self):
        return 'symbol={:5}={:12} modifiers={}={:26}'.format(self.symbol, self.symbolStr, self.modifiers, self.modsStr)

    def on_key_press(self, symbol, modifiers):
        self.symbol,    self.modifiers = symbol, modifiers
        self.symbolStr, self.modsStr   = pygwink.symbol_string(symbol), pygwink.modifiers_string(modifiers)
        symb,            mods          = self.symbolStr, self.modifiers
        print('on_key_press(BGN)   {}'.format(self.kbpEvntTxt()), file=DBG_FILE)
        if   self.isTab(symb):                      self.addTab()
        elif symb == 'Escape':                      self.quit('on_key_press({})'.format(symb))
        if   self.isCtrl(mods):
            if   symb == '$':                        pyglet.image.get_buffer_manager().get_color_buffer().save('screenshot.png')
            if   symb == 'Q' and self.isShift(mods): self.quit('on_key_press({})'.format(symb))
            elif symb == 'Q':                        self.quit('on_key_press({})'.format(symb))
            if   symb == 'C' and self.isShift(mods): self.updateFontColor( 1)
            elif symb == 'C':                        self.updateFontColor(-1)
            if   symb == 'D' and self.isShift(mods): self.updateFontDpi(   1)
            elif symb == 'D':                        self.updateFontDpi(  -1)
            if   symb == 'N' and self.isShift(mods): self.updateFontName(  1)
            elif symb == 'N':                        self.updateFontName( -1)
            if   symb == 'S' and self.isShift(mods): self.updateFontSize(  1)
            elif symb == 'S':                        self.updateFontSize( -1)

    def on_text(self, text):
        print('on_text(BGN)        {} text={}'.format(self.kbpEvntTxt(), text), file=DBG_FILE)
        if self.isTab(text):                         self.addTab()

    @staticmethod
    def isCtrl(mods):        return mods & pygwink.MOD_CTRL
    @staticmethod
    def isShift(mods):       return mods & pygwink.MOD_SHIFT
    @staticmethod
    def isAlt(mods):         return mods & pygwink.MOD_ALT
#    @staticmethod
#    def isCtrlShift(mods):   return (mods & pygwink.MOD_CTRL) and (mods & pygwink.MOD_SHIFT)

    @staticmethod
    def isTab(text):
        return True if text == '-' or Tabs.isFret(text) else False

    @staticmethod
    def isFret(text):
        return True if '0' <= text <= '9' or 'a' <= text <= 'o' else False

    def addTab(self):
        print('addTab() {}'.format(self.kbpEvntTxt()), file=DBG_FILE)
        self._initText([self.symbolStr], self.i[C], self.g[C+2], self.batch)

    def updateFontColor(self, ii):
        i = (self.fontColorIndex + ii) % len(FONT_COLORS)
        print('updateFontColor({:2}) {} FONT_COLORS[{}]={}'.format(ii, self.kbpEvntTxt(), i, FONT_COLORS[i]), file=DBG_FILE)
        for j in range(len(self.texts)):
            for k in range(len(self.texts[j])):
                self.texts[j][k].color = FONT_COLORS[i]
        self.fontColorIndex = i

    def updateFontDpi(self, ii):
        i = (self.fontDpiIndex + ii) % len(FONT_DPIS)
        print('updateFontDpi() ERROR: Cannot set dpi - Create a new instance?', file=DBG_FILE)
        print('updateFontDpi(  {:2}) {} FONT_DPIS[{}]={}'.format(ii, self.kbpEvntTxt(), i, FONT_DPIS[i]), file=DBG_FILE)
#        for j in range(len(self.texts)):
#            for k in range(len(self.texts[j])):
#                self.texts[j][k].dpi = FONT_DPIS[i]
#        self.fontDpiIndex = i

    def updateFontName(self, ii):
        i = (self.fontNameIndex + ii) % len(FONT_NAMES)
        print('updateFontName( {:2}) {} FONT_NAMES[{}]={}'.format(ii, self.kbpEvntTxt(), i, FONT_NAMES[i]), file=DBG_FILE)
        for j in range(len(self.texts)):
            for k in range(len(self.texts[j])):
                self.texts[j][k].font_name = FONT_NAMES[i]
        self.fontNameIndex = i

    def updateFontSize(self, ii):
        i = (self.fontSizeIndex + ii) % len(FONT_SIZES)
        print('updateFontSize( {:2}) {} FONT_SIZES[{}]={}'.format(ii, self.kbpEvntTxt(), i, FONT_SIZES[i]), file=DBG_FILE)
        for j in range(len(self.texts)):
            for k in range(len(self.texts[j])):
                self.texts[j][k].font_size = FONT_SIZES[i]
        self.fontSizeIndex = i

    def on_text_motion(self, motion):
        print('on_text_motion()    {} motion={}'.format(self.kbpEvntTxt(), motion), file=DBG_FILE)
        if self.modifiers == 0:
            if   motion==pygwink.MOTION_LEFT:          self.move(-1)
            elif motion==pygwink.MOTION_RIGHT:         self.move(1)
            elif motion==pygwink.MOTION_UP:            self.move(-self.n[C]-CCC)
            elif motion==pygwink.MOTION_DOWN:          self.move(self.n[C]+CCC)
            elif motion==pygwink.MOTION_PREVIOUS_PAGE: self.prevPage(self.i[P], motion)
            elif motion==pygwink.MOTION_NEXT_PAGE:     self.nextPage(self.i[P], motion)
            else:                                      print('on_text_motion() motion={} ???'.format(motion), file=DBG_FILE)
            self.updateCaption()

    def move(self, c):
        cc = self.cursorCol()
        k = cc + c
        print('move({}) i[C]={} cc={} k={}'.format(c, self.i[C], cc, k), file=DBG_FILE)
        x, y = self.cols[k].x, self.cols[k].y
        self.cursor.update(x=x, y=y)
        self.i[C] += c

    def fontInfo(self):
        return FONT_COLORS[self.fontColorIndex], FONT_DPIS[self.fontDpiIndex], FONT_SIZES[self.fontSizeIndex], FONT_NAMES[self.fontNameIndex]

    def updateCaption(self):
        fc, fd, fs, fn = self.fontInfo()
        text = '{}dpi {}pt {} {},{},{},{}'.format(fd, fs, fn, fc[0], fc[1], fc[2], fc[3])
        print('updateCaption() {}'.format(text), file=DBG_FILE)
        self.set_caption(text)

    def nextPage(self, i, motion):
        self.pages[i].visible = False
        self.updatePage(i+1, 'nextPage() {}=MOTION_NEXT_PAGE   '.format(motion))

    def prevPage(self, i, motion):
        self.pages[i].visible = False
        self.updatePage(i-1, 'prevPage() {}=MOTION_PREVIOUS_PAGE'.format(motion))

    def updatePage(self, i, reason):
        i = i % self.n[P]
        self.pages[i].visible = True
        print('{} i[{}]={}'.format(reason, P, i), file=DBG_FILE)
        self.i[P] = i

    def on_mouse_release(self, x, y, button, modifiers):  # pyglet.window.mouse.MIDDLE #pyglet.window.mouse.LEFT #pyglet.window.mouse.RIGHT
        w, h = self.ww/self.n[C], self.hh/(self.n[R]*self.n[L])
        y = self.hh-y
        c, r = int(x/w), int(y/h)
        self.i[C] = r*(self.n[C]+2)+c
        j = self.i[C]
        self.cursor.update(self.cols[j].x, self.cols[j].y)
        print('on_mouse_release({}x{}) x={:4} y={:4} w={} h={} c={:4} r={:4} j={}'.format(self.ww, self.hh, x, y, w, h, c, r, j), file=DBG_FILE)

    def toggleColorLists(self, motion):
        if not RUN_TEST: print('toggleColorLists(WARNING) Nothing To Toggle RUN_TEST={} motion={}'.format(RUN_TEST, motion), file=DBG_FILE); return
        cls = self.colorLists
        i = self.i[P]
        print('toggleColorLists() i={}'.format(i), file=DBG_FILE)
        if motion==pygwink.MOTION_LEFT:
            for j in range(len(cls[i])): cls[i][j].visible = False
            i -= 1
            i = i%len(COLORS)
            for j in range(len(cls[i])): cls[i][j].visible = True
            print('toggleColorLists() MOTION_LEFT={} i[P]={} len(cls)={}'.format(motion, i, len(cls)), file=DBG_FILE)
        elif motion==pygwink.MOTION_RIGHT:
            for j in range(len(cls[i])): cls[i][j].visible = False
            i += 1
            i = i%len(COLORS)
            for j in range(len(cls[i])): cls[i][j].visible = True
            print('toggleColorLists() MOTION_RIGHT={} i[P]={} len(cls)={}'.format(motion, i, len(cls)), file=DBG_FILE)
        self.i[P] = i

    def quit(self, reason=''):
        self.dumpStruct('quit() '+reason)
        print('quit() {}\nQuiting'.format(reason), file=DBG_FILE)
        exit()

    def _initTextTest(self, n):
        self._initText(['C', 'C#', 'Db', 'D', 'D#', 'Eb', 'E', ' ',  ' ',  'F', 'F#', 'Gb', 'G', 'G#', 'Ab', 'A', 'A#', 'Bb', 'B', ' ' , ' ' ],                            0*n, self.g[C+2], self.batch)
        self._initText(['C', 'C#', 'Db', 'D', 'D#', 'Eb', 'E', 'E#', 'Fb', 'F', 'F#', 'Gb', 'G', 'G#', 'Ab', 'A', 'A#', 'Bb', 'B', 'B#', 'Cb'],                            1*n, self.g[C+2], self.batch)
        self._initText(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'],                 2*n, self.g[C+2], self.batch)
        self._initText(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25'], 3*n, self.g[C+2], self.batch)
        self._initText(['~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '[', ']', '<', '>', '/', '?', ',', '.', '=', '_', '+', ' ', '|', '{', '}', '-', '\\'],      4*n, self.g[C+2], self.batch)
        ucnFlat, ucnNatural, ucnSharp = unicodedata.name('\u066D'), unicodedata.name('\u166E'), unicodedata.name('\u266F')
#        ucFlat,  ucNatural,  ucSharp  = unicodedata.lookup(ucnFlat), unicodedata.lookup(ucnNatural), unicodedata.lookup(ucnSharp)
#        ucFlat,  ucNatural,  ucSharp  = unicodedata.lookup('MUSIC FLAT SIGN'), unicodedata.lookup('MUSIC NATURAL SIGN'), unicodedata.lookup('MUSIC SHARP SIGN')
        print('    ucnFlat={}'.format(ucnFlat),     file=DBG_FILE)
        print(' ucnNatural={}'.format(ucnNatural),  file=DBG_FILE)
        print('   ucnSharp={}'.format(ucnSharp),    file=DBG_FILE)
#        print('     ucFlat={}'.format(ucFlat),      file=DBG_FILE)
#        print('  ucNatural={}'.format(ucNatural),   file=DBG_FILE)
#        print('    ucSharp={}'.format(ucSharp),     file=DBG_FILE)
#        self._initText([ucFlat],     4*n, self.g[C+2], self.batch)
#        self._initText([ucNatural],  5*n, self.g[C+2], self.batch)
#        self._initText([ucSharp],    6*n, self.g[C+2], self.batch)
#        self._initText([' ', ' ', ' ', ' ', '{#x266D}'], (255, 0, 0, 255), 3*n, self.g[C+2], self.batch) # Unicode seems to require a Document?
#        self._initText([' ', ' ', ' ', ' ', '{#x266F}'], (255, 0, 0, 255), 4*n, self.g[C+2], self.batch)

if __name__=='__main__':
    RUN_TEST = False;  CARET = False;  ORDER_GROUP = True;  SUBPIX = False;  FULL_SCREEN = False;  DBG = False
    SFX          = 'TEST' if RUN_TEST else ''
    DBG_FILE     = open(sys.argv[0] + SFX + ".log.txt", 'w')
    DATA_FILE    = open(sys.argv[0] + SFX + ".dat.txt", 'w')
    P, L, R, C   = 0, 1, 2, 3
    OPACITY      = [255, 240, 225, 210, 190, 165, 140, 110, 80]
    GRAY         = [(255, 255, 255, OPACITY[0]), ( 0,  0,  0, OPACITY[0])]
    PINK         = [(255,  64, 192, OPACITY[1]), (57, 16, 16, OPACITY[1])]
    INFRA_RED    = [(255,  29,  24, OPACITY[5]), (68, 20, 19, OPACITY[5])]
    RED          = [(255,  24,  21, OPACITY[2]), (72, 15, 12, OPACITY[2])]
    ORANGE       = [(255, 128,  32, OPACITY[1]), (76, 30, 25, OPACITY[0])]
    YELLOW       = [(255, 255,  15, OPACITY[0]), (45, 41, 10, OPACITY[0])]
    GREEN        = [( 44, 255,   0, OPACITY[1]), (21, 54, 10, OPACITY[1])]
    GREEN_BLUE   = [( 24, 255,  61, OPACITY[5]), (10, 49, 25, OPACITY[3])]
    CYAN         = [( 32, 255, 255, OPACITY[1]), (16, 64, 64, OPACITY[2])]
    BLUE_GREEN   = [( 25, 181, 255, OPACITY[2]), (12, 37, 51, OPACITY[2])]
    BLUE         = [( 35,  26, 255, OPACITY[7]), (19, 11, 64, OPACITY[7])]
    ULTRA_VIOLET = [(176,  81, 255, OPACITY[7]), (44, 14, 58, OPACITY[5])]
    VIOLET       = [(194,  96, 255, OPACITY[5]), (50, 19, 61, OPACITY[4])]
    HUES         = 13
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
    FONT_SIZES  = [6, 8, 9, 10, 11, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36]
    FONT_COLORS = [REDS[0], GREENS[0], BLUES[0], YELLOWS[0], ORANGES[0], GREEN_BLUES[0], CYANS[0], BLUE_GREENS[0], PINKS[0], INFRA_REDS[0], VIOLETS[0], ULTRA_VIOLETS[0], GRAYS[0]]
    FONT_DPIS    = [75, 80, 90, 96, 100, 108, 116, 124]
    tabs        = Tabs()
    pyglet.app.run()
#        cc = GREENS[-1::-1]+GREENS
