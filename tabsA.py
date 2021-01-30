import math, sys, os
import unicodedata
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
        else:    self.n, self.i, self.x, self.y, self.w, self.h, self.o, self.g =  [1, 2, 6, 20], [0, 0, 0, 0], [0, 4, 0, 0], [0, 4, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [2, 0, 0, 3], []
        self.argMap = cmdArgs.parseCmdLine(dbg=1)
        print('__init__(BGN) argMap={}'.format(self.argMap), file=DBG_FILE)
        if 'n' in self.argMap and len(self.argMap['n'])  > 0: self.n            = [int(self.argMap['n'][i]) for i in range(len(self.argMap['n']))]
        if 'x' in self.argMap and len(self.argMap['x'])  > 0: self.x            = [int(self.argMap['x'][i]) for i in range(len(self.argMap['x']))]
        if 'y' in self.argMap and len(self.argMap['y'])  > 0: self.y            = [int(self.argMap['y'][i]) for i in range(len(self.argMap['y']))]
        if 'w' in self.argMap and len(self.argMap['w'])  > 0: self.ww           =  int(self.argMap['w'][0])
        if 'h' in self.argMap and len(self.argMap['h'])  > 0: self.hh           =  int(self.argMap['h'][0])
        if 'o' in self.argMap and len(self.argMap['o'])  > 0: self.o            = [int(self.argMap['o'][i]) for i in range(len(self.argMap['o']))]
        if 'i' in self.argMap and len(self.argMap['i'])  > 0: self.i            = [int(self.argMap['i'][i]) for i in range(len(self.argMap['i']))]
        if 'f' in self.argMap and len(self.argMap['f']) == 0: FULL_SCREEN       = 1
        if 'g' in self.argMap and len(self.argMap['g']) == 0: ORDER_GROUP       = 1
        if 's' in self.argMap and len(self.argMap['s']) == 0: SUBPIX            = 1
        if 't' in self.argMap and len(self.argMap['t']) == 0: TEST              = 1
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
        print('[t]         TEST={}'.format(TEST),            file=DBG_FILE)
        self.fontBold, self.fontItalic = 1, 1
        self.fontNameIndex, self.fontColorIndex, self.fontSizeIndex, self.fontDpiIndex = 0, 0, len(FONT_SIZES)//3, 3
        self._initWindowA()
        super().__init__(screen=self.screens[1], fullscreen=FULL_SCREEN, resizable=True, visible=False)
        self._initWindowB()
        self.symb, self.symbStr, self.mods, self.modsStr, self.kbk = 0, '', 0, '', 0
        self.sprites = []
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
                spr = self.createSprite('_initTestColors()', g1, c[i][j], xx, yy, w1, h2, i, j, v=True, dbg=1)
                sprites.append(spr)
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

    def geom(self, j, px, py, pw, ph, why='', init=False, dump=3, dbg=0):
        n, i, x, y, w, h, o , g = self.n[j], self.i[j], self.x[j], self.y[j], self.w[j], self.h[j], self.o[j], self.g[j]
#        n = n+1 if j==R else n+CCC if j==C else n
        if   j==R: n += 1
        elif j==C: n += CCC
        if   o==0: w, h =  pw-2*x,        (ph-y*(n+1))/n
        elif o==1: w, h = (pw-x*(n+1))/n, (ph-y*(n+1))/n
        elif o==2: w, h =  pw-2*x,         ph-2*y
        elif o==3: w, h = (pw-x*(n+1))/n,  ph-2*y
        if init: self.w[j], self.h[j] = w, h
        if o!=3: x += px #; y = py+ph-y
        if dump==2 or dump==3: self.dumpSprite()
#        if dbg and init: print('#################################################################################################################################################################################', file=DBG_FILE)
        if dump==1 or dump==3: self.dumpGeom(j, why)
        if dbg: print('geom({}) px={:7.2f} py={:7.2f} pw={:7.2f} ph={:7.2f}  =>  n={:3} x={:4} y={:4} w={:7.2f} h={:7.2f} o={}'.format(j, px, py, pw, ph, n, x, y, w, h, o), file=DBG_FILE)
        if init: return n, i, x, y, w, h, o, g
        else:    return n, i, x, y, w, h, o, g, w/self.w[j], h/self.h[j]

    def cursorCol(self, dbg=1):
        p, l, r, c = self.i[P], self.i[L], self.i[R], self.i[C]
        cpr = self.n[C] + CCC
        cpl = self.n[R]*cpr
        cpp = self.n[L]*cpl
        col = p*cpp + l*cpl + (r+1)*cpr + c + CCC
        if dbg: print('cursorCol() cpp={} cpl={} cpr={}   p={} l={} r={} c={}   col=(p*cpp={} + l*cpl={} + (r+1)*cpr={} + c={} + CCC={})=col={}'.format(cpp, cpl, cpr, p, l, r, c, p*cpp, l*cpl, (r+1)*cpr, c, CCC, col), file=DBG_FILE)
        return col

    def createSprite(self, why, grp, cc, x, y, w, h, i, j, v=None, dbg=0):#        img.anchor_x, img.anchor_y = fri(w/2), fri(h/2)
        scip = pyglet.image.SolidColorImagePattern(cc)
        img = scip.create_image(width=fri(w), height=fri(h))
        spr = pyglet.sprite.Sprite(img, x, y, batch=self.batch, group=grp, subpixel=SUBPIX)
        spr.visible = v if v is not None else True if i==P else False
        spr.color, spr.opacity = cc[:3], cc[3]
        if DBG or dbg: self.dumpSprite(spr, len(self.sprites), '{:16} {:3} {:3} {:7.2f} {:7.2f} {:7.2f} {:7.2f} {:4} {:4} {} {}'.format(why, i, j, x, y, w, h, img.anchor_x, img.anchor_y, spr.group, spr.group.parent))
        self.sprites.append(spr)
        return spr

    def _init(self):
        self.pages, self.lines, self.rows, self.cols, self.labelRows, self.labelsText = [], [], [], [], [], []
        self._initPages()
        self._initLabelsText(self.g[C+1])
        self._initData(  self.g[C+2])
        self._initCursor(self.g[C+3])
        if CARET: self._initCaret()
        self.dumpStruct('_init')

    def _initLabelsText(self, g):
        labels, n = ['R', 'M', '='], self.n[C]
        [labels.append('{}'.format(c)) for c in range(1, n+1)]
        self.dumpTextList(labels, '_initLabelsText(BGN)) labels')
        self.labelsText.append(self._initText(labels, 0, g, dbg=1))
        self.dumpTextList(labels, '_initLabelsText(END)) labels')

    def _initData(self, g):
        cc, self.data, self.texts = self.cursorCol()-CCC, [], []
        self.STRING_NUMS, self.stringNames, self.capoFretNums  = ['1', '2', '3', '4', '5', '6'], ['E', 'B', 'G', 'D', 'A', 'E'], ['0', '0', '0', '0', '0', '0']
        print('_initData() STRING_NUMS={} stringNames={} capoFretNums={}'.format(self.STRING_NUMS, self.stringNames, self.capoFretNums), file=DBG_FILE)
        col = ['-' for _ in range(len(self.STRING_NUMS))]
        for i in range(self.n[C] + CCC): self.data.append(col)
#        self.data    = [['=' for _ in range(len(self.STRING_NUMS))]] * (self.n[C] + CCC)
        self.data[0], self.data[1], self.data[2] = self.STRING_NUMS, self.stringNames, self.capoFretNums
        for c in range(len(self.data)):
            tmp = []
            for s in range(len(self.data[c])):
#                self.texts.append(self._initText(self.data[c][s], cc+c+s*(self.n[C]+CCC), g, dbg=1))
                tmp.append(self._initText(self.data[c][s], cc+c+s*(self.n[C]+CCC), g, dbg=1))
            self.texts.append(tmp)
        self.dumpTexts()
        print('data={}'.format(self.data), file=DBG_FILE)

    def _initText(self, text, c, g, b=None, dbg=0):
        if b is None: b = self.batch
        w, h, txt, a = self.cols[c].width-2, self.cols[c].height-2, [], 'center'
        k, d, s, n, o, j = self.fontInfo()
#        for t in text: print('{}'.format(t), file=DBG_FILE, end='') ; print(file=DBG_FILE)
        if DBG: print('_initText(BGN) text={} c={:3} w={:4} h={:4} fc={} dpi={} fs={} fn={} fb={} fi={}'.format(text, c, w, h, k, d, s, n, o, j), file=DBG_FILE)
        for i in range(len(text)):
            x, y, = self.cols[c+i].x+w/2, self.cols[c+i].y+h/2
            tmp = pyglet.text.Label(text[i], font_name=n, font_size=s, bold=o, italic=j, color=k, x=x, y=y, width=w, height=h, anchor_x=a, anchor_y=a, align=a, dpi=d, batch=b, group=g)
            txt.append(tmp)
            if DBG or dbg: print('_initText() c={:3} x={:6.1f} y={:6.1f} w={:4} h={:4} text[{:3}]={:3}'.format(c, x, y, w, h, i, text[i]), file=DBG_FILE)
        if DBG: print('_initText(END)'.format(), file=DBG_FILE)
        return txt

    def _initPages(self):
        cc = [REDS[0], REDS[2], REDS[4], REDS[6], REDS[8], REDS[10]]
        n, i, x, y, w, h, o, g = self.geom(P, self.x[P], self.y[P], self.ww, self.hh, why='', init=True, dump=0)
        for p in range(n):
            self.dumpSprite()
            page = self.createSprite('_initPages', g, cc[p%len(cc)], x, y, w, h, p, 0, dbg=1)
            self.pages.append(page)
            if self.n[P+1] > 0: lines = self._initLines(page)
        return self.pages

    def _initLines(self, spr):
        cc = [CYANS[0], CYANS[5]]
        n, i, x, y, w, h, o, g = self.geom(L, spr.x, spr.y, spr.width, spr.height, why='', init=True, dump=0)
        for l in range(n):
            yy = spr.y+spr.height-(h+y)*(l+1)
            line   = self.createSprite('_initLines', g, cc[l%len(cc)], x, yy, w, h, l, 0, v=True if len(self.pages)==1 else False, dbg=1)
            self.lines.append(line)
            if self.n[L+1] > 0:
                self.labelRows.append(self._initLabelRow(line, self.g[C+1]))
                rows = self._initRows(line)
        return self.lines

    def _initLabelRow(self, spr, g):
        cc = [VIOLETS[0], VIOLETS[5]]
        n, i, x, y, w, h, o, gg = self.geom(R, spr.x, spr.y, spr.width, spr.height, why='', init=True, dump=0, dbg=0)
        yy = spr.y+spr.height-(h+y)
        labelRow = self.createSprite('_initLabelRow', g, cc[0], x, yy, w, h, 0, 0, v=True if len(self.pages)==1 else False, dbg=1)
        if self.n[R+1] > 0: labelCols = self._initCols(labelRow)
        return labelRow

    def _initRows(self, spr):
        cc = [YELLOWS[0], YELLOWS[5]]
        n, i, x, y, w, h, o, g = self.geom(R, spr.x, spr.y, spr.width, spr.height, why='', init=True, dump=0, dbg=0)
        r1 = 1 if VRSN else 0
        r2 = n if VRSN else n
        for r in range(r1, r2):
            yy = spr.y+spr.height-(h+y)*(r+1)
            row   = self.createSprite('_initRows', g, cc[r%len(cc)], x, yy, w, h, r, 0, v=True if len(self.pages)==1 else False, dbg=1)
            self.rows.append(row)
            if self.n[R+1] > 0: cols = self._initCols(row)
        return self.rows

    def _initCols(self, spr):
#        a, b = 6, 3; cc = [GREENS[a], GREENS[b]] if len(self.rows)%2 else [GREENS[b], GREENS[a]]
        a, b = 11, 8; cc = [GRAYS[a], GRAYS[b]] if len(self.rows)%2 else [GRAYS[b], GRAYS[a]]
        (n, i, x, y, w, h, o, g), s = self.geom(C, spr.x, spr.y, spr.width, spr.height, why='', init=True, dump=0), len(cc)
        for c in range(n):
            xx, yy = spr.x+x+(w+x)*c, spr.y+spr.height-(h+y)
            col   = self.createSprite('_initCols', g, cc[c%s], xx, yy, w, h, c, 0, v=True if len(self.pages)==1 else False, dbg=1)
            self.cols.append(col)
        return self.cols

    def _initCaret(self):
        doc = pyglet.text.document.FormattedDocument()
        w, h, b, g = self.cols[0].width, self.cols[0].height, self.batch, self.g[C+3]
        layout = pyglet.text.layout.IncrementalTextLayout(document=doc, width=w, height=h, batch=b, group=g)
        self.caret = pyglet.text.caret.Caret(layout, batch=self.batch, color=(200, 255, 200))

    def _initCursor(self, g):
        c = self.cursorCol()
        x, y, w, h = self.cols[c].x, self.cols[c].y, self.cols[c].width, self.cols[c].height
        self.cursor = self.createSprite('cursor', g, CC, x, y, w, h, 0, 0, v=True)
        print('_initCursor()   c={:4} x={:6.1f} y={:6.1f} w={:4} h={:4} i[C]={}'.format(c, x, y, w, h, self.i[C]), file=DBG_FILE)
########################################################################################################################################################################################################
    def dumpFont(self, why=''):
        fc, dpi, fs, fn, fb, fi = self.fontInfo()
        pix = FONT_SCALE*fs/dpi
        print('dumpFont({}) {} {}DPI {}pt {} ({:6.3f}*{}pt/{}DPI)={:6.3f}pixels'.format(why, fc, dpi, fs, fn, FONT_SCALE, fs, dpi, pix), file=DBG_FILE)

    def dumpGeom(self, j, why=''):
        n, i, x, y, w, h, o , g = self.n[j], self.i[j], self.x[j], self.y[j], self.w[j], self.h[j], self.o[j], self.g[j]
        print('{:25} j={} n={:3} i={:4} x={:3} y={:3} w={:7.2f} h={:7.2f} o={} g={}'.format(why, j, n, i, x, y, w, h, o, g), file=DBG_FILE)

    @staticmethod
    def dumpTextList(text, why=''):
        print('{}[len={}] = [ '.format(why, len(text)), file=DBG_FILE, end='')
        for i in range(len(text)): print('{}'.format(text[i]), file=DBG_FILE, end=' ')
        print(']', file=DBG_FILE)

    def dumpLabels(self, why=''):
        ns, nc = len(self.labelsText), len(self.labelsText[0])
        print('dumpLabels(BGN) {} ({}x{})'.format(why, ns, nc), file=DBG_FILE)
        print('  s   c    x       y       w       h      Font Name      Size DPI Bold Ital  color/opacity    text', file=DBG_FILE)
        for ss in range(ns):
            for cc in range(nc):
                l = self.labelsText[ss][cc]
                x, y, w, h, n, d, s, c, b, i, t = l.x, l.y, l.width, l.height, l.font_name, l.dpi, l.font_size, l.color, l.bold, l.italic, l.text
                print('{:3} {:3} {:7.2f} {:7.2f} {:7.2f} {:7.2f}  {:16}  {:2}  {:3}   {:1}   {:1}  ({:3},{:3},{:3},{:3})  {}'.format(ss, cc, x, y, w, h, n, s, d, b, i, c[0], c[1], c[2], c[3], t), file=DBG_FILE)
        print('dumpLabels(END) {} ({}x{})'.format(why, ns, nc), file=DBG_FILE)

    def dumpTexts(self, why=''):
        nc, ns = len(self.texts), len(self.texts[0])
        print('dumpTexts(BGN) {} ({}x{}):'.format(why, ns, nc), file=DBG_FILE)
        for cc in range(nc):
            for ss in range(ns):
                l = self.texts[cc][ss][0]
                x, y, w, h, n, d, s, c, b, i, t = l.x, l.y, l.width, l.height, l.font_name, l.dpi, l.font_size, l.color, l.bold, l.italic, l.text
                print('{:3} {:3} {:7.2f} {:7.2f} {:7.2f} {:7.2f}  {:16}  {:2}  {:3}   {:1}   {:1}  ({:3},{:3},{:3},{:3})  {}'.format(ss, cc, x, y, w, h, n, s, d, b, i, c[0], c[1], c[2], c[3], t), file=DBG_FILE)
        print('dumpTexts(END) {} ({}x{})'.format(why, ns, nc), file=DBG_FILE)

#    def dumpData_B(self, why=''):
#        nc, ns = len(self.data), len(self.data[0])
#        print('dumpData(BGN) {} ({}x{}):'.format(why, ns, nc), file=DBG_FILE)
#        for c in range(nc):
#            for s in range(ns):
#                d = self.texts[c][s]
#                x, y, w, h, fn, dpi, fs, c, b, i, t = d.x, d.y, d.width, d.height, d.font_name, d.dpi, d.font_size, d.color, d.bold, d.italic, d.text
#                print('{:3} {:3} {:7.2f} {:7.2f} {:7.2f} {:7.2f}  {:16}  {:2}  {:3}   {:1}   {:1}  ({:3},{:3},{:3},{:3})  {}'.format(c, s, x, y, w, h, fn, fs, dpi, b, i, c[0], c[1], c[2], c[3], t), file=DBG_FILE)
#        print('dumpData(END) {} ({}x{}):'.format(why, ns, nc), file=DBG_FILE)

#    def dumpData_A(self, why=''):
#        nc, ns = len(self.data), len(self.data[0])
#        print('dumpData(BGN) {} ({}x{}):'.format(why, ns, nc), file=DBG_FILE)
#        for c in range(len(self.data)):
#            for s in range(len(self.data[c])):
#                print('{}'.format(self.data[c][s]), file=DBG_FILE, end='')
#            print(file=DBG_FILE)
#        print('dumpData(END) {} ({}x{}):'.format(why, ns, nc), file=DBG_FILE)

    def dumpSprites(self, s, why):
#        print('dumpSprites({})'.format(len(s)), file=DBG_FILE)
        for i in range(len(s)): self.dumpSprite(s[i], i, '{} {}'.format(why, i))

    @staticmethod
    def dumpSprite(s=None, k=-1, why=''):
        if s is None: print('  id      x       y       w       h    iax  iay    m      mx     my     rot    color/opacity  vsb why              i   j      x       y       w       h    iax  iay', file=DBG_FILE); return
        f = '{:5} {:7.2f} {:7.2f} {:7.2f} {:7.2f} {:4} {:4} {:6.3f} {:6.3f} {:6.3f} {:7.2f} ({:3},{:3},{:3},{:3}) {:1}'
        c = s.color
        fs = f.format(k, s.x, s.y, s.width, s.height, s.image.anchor_x, s.image.anchor_y, s.scale, s.scale_x, s.scale_y, s.rotation, c[0], c[1], c[2], s.opacity, s.visible)
        print('{} {}'.format(fs, why), file=DBG_FILE)
        assert(type(s) == pyglet.sprite.Sprite)

    def dumpSpriteCount(self, why=''):
        np, nl, nr, nc, nlr = map(len, [self.pages, self.lines, self.rows, self.cols, self.labelRows])
        sc = 'np={} lpp={} nl={} rpl={} nr={} cpr={} nc={} lrpl={} nlr={}'
        fs = sc.format(np, self.n[L], nl, self.n[R], nr, self.n[C], nc, 1, nlr)
        print('dumpSpriteCount({}) {}'.format(why, fs), file=DBG_FILE)
        print('dumpSpriteCount({}) np={}   +   nl={}   +   nr={}   +    nc={}   +    nlr={} = ns={}'.format(why, np, nl, nr, nc, nlr, np + nl + nr + nc + nlr), file=DBG_FILE)

    def dumpStruct(self, why=''):
        data = [self.pages, self.lines, self.labelRows, self.rows, self.cols]# ; why = 'dumpStruct(why)
        self.dumpFont(why)
        self.dumpSpriteCount(why)
        self.dumpSprite()
        for i in range(len(data)):
#            self.dumpGeom(i, '{}'.format(why))
            self.dumpSprites(data[i], '{} {}'.format(why, i))
        self.dumpLabels(why)
        self.dumpTexts(why)

    def dumpTest(self, why=''):
        self.dumpFont('{}'.format(why))
        self.dumpSprite()
        for i in range(len(self.colorLists)): self.dumpSprites(self.colorLists[i], why)
########################################################################################################################################################################################################
    def on_resize(self, width, height):
        super().on_resize(width, height)
        self.ww, self.hh = width, height
        if TEST: self.resizeTestColors()
        return
#        for i in range(len(self.n)): self.dumpGeom(i, 'on_resize({}x{})'.format(self.ww, self.hh))
        self.resizePages()
        self.resizeLabels()
#        self.resizeData()
        self.resizeCursor()
        if CARET: self.resizeCaret()
        self.dumpFont('_init()')
        self.dumpStruct('on_resize()')
        self.updateCaption()

    def resizeLabels(self):
        for c in range(len(self.labelsText)):
            self.resizeText(self.labelsText[c], c)

    def resizeData(self):
        cc = self.n[C]+CCC
        for c in range(len(self.texts)):
            self.resizeText(self.texts[c], (c%self.n[R])*cc+c//self.n[R])

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
        n, i, x, y, w, h, o, g, mx, my = self.geom(P, self.x[P], self.y[P], self.ww, self.hh, why='', init=False, dump=0)
        for p in range(n):
            self.pages[p].update(x=x, y=y, scale_x=mx, scale_y=my)
            if DBG: self.dumpSprite(self.pages[p], p*n, '{:20} {:3} {:3} {:7.2f} {:7.2f} {:7.2f} {:7.2f}'.format('on_resize Pages', p, 0, x, y, w, h))
            if self.n[P+1] > 0: self.resizeLines(self.pages[p], p)

    def resizeLines(self, spr, pn):
        n, i, x, y, w, h, o, g, mx, my = self.geom(L, spr.x, spr.y, spr.width, spr.height, why='', init=False, dump=0)
        for l in range(n):
            yy = spr.y+spr.height-(h+y)*(l+1)
            self.lines[l+pn*n].update(x=x, y=yy, scale_x=mx, scale_y=my)
            if DBG: self.dumpSprite(self.lines[l+pn*n], pn, '{:20} {:3} {:3} {:7.2f} {:7.2f} {:7.2f} {:7.2f}'.format('on_resize Lines', l, 0, x, yy, w, h))
            if self.n[L+1] > 0:
                self.resizeLabelRow(self.lines[l+pn*n], l+pn*n)
                self.resizeRows(self.lines[l+pn*n], l+pn*n)

    def resizeLabelRow(self, spr, ln):
        n, i, x, y, w, h, o, g, mx, my = self.geom(R, spr.x, spr.y, spr.width, spr.height, why='', init=False, dump=0)
        yy = spr.y+spr.height-(h+y)
        self.labelRows[ln].update(x=x, y=yy, scale_x=mx, scale_y=my)
        if DBG: self.dumpSprite(self.rows[ln], ln, '{:20} {:3} {:3} {:7.2f} {:7.2f} {:7.2f} {:7.2f}'.format('on_resize LabelRow', 0, 0, x, yy, w, h))
        if self.n[R+1] > 0: self.resizeCols(self.labelRows[ln], ln)

    def resizeRows(self, spr, ln):
        n, i, x, y, w, h, o, g, mx, my = self.geom(R, spr.x, spr.y, spr.width, spr.height, why='', init=False, dump=0)
        r1 = 1 if VRSN else 0
        r2 = n if VRSN else n
        n -= 1
        for r in range(r1, r2):
#            print('ln={} n={} r={}'.format(ln, n, r), file=DBG_FILE)
            yy = spr.y+spr.height-(h+y)*(r+1)
            self.rows[(r-1)+ln*n].update(x=x, y=yy, scale_x=mx, scale_y=my)
            if DBG: self.dumpSprite(self.rows[r+ln*n], ln, '{:20} {:3} {:3} {:7.2f} {:7.2f} {:7.2f} {:7.2f}'.format('on_resize Rows', r, 0, x, yy, w, h))
            if self.n[R+1] > 0: self.resizeCols(self.rows[(r-1)+ln*n], (r-1)+ln*n)

    def resizeCols(self, spr, rn):
        n, i, x, y, w, h, o, g, mx, my = self.geom(C, spr.x, spr.y, spr.width, spr.height, why='', init=False, dump=0)
        for c in range(n):
            xx, yy = spr.x+x+(w+x)*c, spr.y+spr.height-(h+y)
            self.cols[c+rn*n].update(x=xx, y=yy, scale_x=mx, scale_y=my)
            if DBG: self.dumpSprite(self.cols[c+rn*n], rn, '{:20} {:3} {:3} {:7.2f} {:7.2f} {:7.2f} {:7.2f}'.format('on_resize Cols', c, 0, xx, yy, w, h))
########################################################################################################################################################################################################
    def on_draw(self):
        self.clear()
        self.batch.draw()

    def kpEvntTxt(self):
        return 'kbk={:6} symb={:6} symbStr={:12} mods={} modsStr={:26}'.format(self.kbk, self.symb, self.symbStr, self.mods, self.modsStr)

    def on_key_press(self, symb, mods):
        self.symb, self.mods, self.symbStr, self.modsStr = symb, mods, pygwink.symbol_string(symb), pygwink.modifiers_string(mods)
        self.kbk = self.symbStr ; kbk = self.kbk
        print('on_key_press(BGN)     {}'.format(self.kpEvntTxt()), file=DBG_FILE)
        if                  self.isTab(kbk):                          self.addTab(kbk)
        elif kbk == 'Q' and self.isCtrl(mods) and self.isShift(mods): self.quit('on_key_press({})'.format(kbk))
        elif kbk == 'Q' and self.isCtrl(mods):                        self.quit('on_key_press({})'.format(kbk))
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
        self.updateCaption()

    def on_text(self, text):
        self.kbk = text
        print('on_text(BGN)          {}'.format( self.kpEvntTxt()), file=DBG_FILE)
        if self.isTab(self.kbk):                 self.addTab(self.kbk)
        if self.kbk=='$' and self.isShift(self.mods): pyglet.image.get_buffer_manager().get_color_buffer().save(sys.argv[0]+SFX+'.snap.png')
#        self.updateCaption()

    def on_text_motion(self, motion):
        self.kbk = motion
        print('on_text_motion(BGN)   {}'.format(self.kpEvntTxt()), file=DBG_FILE)
        if self.mods == 0:
            if   motion==pygwink.MOTION_LEFT:          self.move(-1)
            elif motion==pygwink.MOTION_RIGHT:         self.move(1)
            elif motion==pygwink.MOTION_UP:            self.move(-self.n[C]-CCC)
            elif motion==pygwink.MOTION_DOWN:          self.move(self.n[C]+CCC)
#            elif motion==pygwink.MOTION_PREVIOUS_PAGE: self.move() # prevPage(self.i[P], motion)
#            elif motion==pygwink.MOTION_NEXT_PAGE:     self.move() # nextPage(self.i[P], motion)
            else:                                      print('on_text_motion() motion={} ???'.format(motion), file=DBG_FILE)
#            self.updateCaption()
########################################################################################################################################################################################################
    def addTab(self, kbk):
        print('addTab()              {}'.format(self.kpEvntTxt()), file=DBG_FILE)
        cc = self.cursorCol()
        self.updateData([kbk], cc)#self.cursorCol())
        self.updateTexts([kbk], cc)#self.cursorCol())

    def updateData(self, text, c): # fix bug - why all cols data affected for a given string?
        cs, cc = c//(self.n[C]+CCC)-1, c % (self.n[C]+CCC)
        self.dumpData('updateData(BGN) c={} text={} cc={} cs={}'.format(c, text, cc, cs))
        self.data[cc][cs] = text[0]
#        self.data[cc][cs] = ''.join([text[t] for t in range(len(text))])
        print('updateData() data[{}][{}]={}'.format(cc, cs, self.data[cc][cs]), file=DBG_FILE)
        self.dumpData('updateData(END) c={} text={} cc={} cs={}'.format(c, text, cc, cs))

    def updateTexts(self, text, c):
        cs, cc = c//(self.n[C]+CCC)-1, c%(self.n[C]+CCC)
        ccc = len(self.STRING_NUMS) * cc + cs
        self.dumpTexts('updateTexts(BGN) c={} text={} cc={} cs={} ccc={}'.format(c, text, cc, cs, ccc))
        self.texts[ccc][0].text = text[0]
        self.dumpTexts('updateTexts(END) c={} text={} cc={} cs={} ccc={}'.format(c, text, cc, cs, ccc))

    def updateFontColor(self, ii):
        self.fontColorIndex = self.updateFontIndex(ii, self.fontColorIndex, FONT_COLORS, 'FONT_COLORS')

    def updateFontDpi(self, ii):
        self.fontDpiIndex = self.updateFontIndex(ii, self.fontDpiIndex, FONT_DPIS, 'FONT_DPIS')

    def updateFontName(self, ii):
        self.fontNameIndex = self.updateFontIndex(ii, self.fontNameIndex, FONT_NAMES, 'FONT_NAMES')

    def updateFontSize(self, ii):
        self.fontSizeIndex = self.updateFontIndex(ii, self.fontSizeIndex, FONT_SIZES, 'FONT_SIZES')

    def updateFontIndex(self, ii, index, prop, name):
        i = (index + ii) % len(prop)
        errMsg = '*ERROR* Dpi Read-Only'
        if name=='FONT_DPIS': i = self.fontDpiIndex ; print('{} {} {}[{}]={} {}'.format(errMsg, self.kpEvntTxt(), name, i, prop[i], errMsg), file=DBG_FILE) ; return self.fontDpiIndex
        print('updateFontIndex({:2})   {} {}[{}]={}'.format(ii, self.kpEvntTxt(), name, i, prop[i]), file=DBG_FILE)
        for j in range(len(self.texts)):
            for k in range(len(self.texts[j])):
                if   name=='FONT_COLORS': self.texts[j][k][0].color     = prop[i]
                elif name=='FONT_NAMES':  self.texts[j][k][0].font_name = prop[i]
                elif name=='FONT_SIZES':  self.texts[j][k][0].font_size = prop[i]
                elif name=='FONT_DPIS':   self.texts[j][k][0].dpi       = prop[i]
        for j in range(len(self.labelsText)):
            for k in range(len(self.labelsText[j])):
                if   name=='FONT_COLORS': self.labelsText[j][k].color     = prop[i]
                elif name=='FONT_NAMES':  self.labelsText[j][k].font_name = prop[i]
                elif name=='FONT_SIZES':  self.labelsText[j][k].font_size = prop[i]
                elif name=='FONT_DPIS':   self.labelsText[j][k].dpi       = prop[i]
        return i

    def toggleFontBold(self):
        print('toggleFontBold() {:1} => {:1}'.format(self.fontBold, not self.fontBold), file=DBG_FILE)
        self.fontBold = not self.fontBold
        for j in range(len(self.texts)):
            for k in range(len(self.texts[j])):
                self.texts[j][k][0].bold = self.fontBold
        for j in range(len(self.labelsText)):
            for k in range(len(self.labelsText[j])):
                self.labelsText[j][k].bold = self.fontBold

    def toggleFontItalic(self):
        print('toggleFontItalic() {:1} => {:1}'.format(self.fontItalic, not self.fontItalic), file=DBG_FILE)
        self.fontItalic = not self.fontItalic
        for j in range(len(self.texts)):
            for k in range(len(self.texts[j])):
                self.texts[j][k][0].italic = self.fontItalic
        for j in range(len(self.labelsText)):
            for k in range(len(self.labelsText[j])):
                self.labelsText[j][k].italic = self.fontItalic

    def move(self, c, dbg=1):
        i, cc = self.i[C], self.cursorCol()
        k = cc + c
        x, y = self.cols[k].x, self.cols[k].y
        self.cursor.update(x=x, y=y)
        self.i[C] += c
        if dbg: print('move({:4}) i[C]={} cc={} => cc={} i[C]={}'.format(c, i, cc, k, self.i[C]), file=DBG_FILE)

    def fontInfo(self):
        return FONT_COLORS[self.fontColorIndex], FONT_DPIS[self.fontDpiIndex], FONT_SIZES[self.fontSizeIndex], FONT_NAMES[self.fontNameIndex], self.fontBold, self.fontItalic

    def updateCaption(self):
        fc, fd, fs, fn, fb, fi = self.fontInfo()
        text = '{}dpi {}pt {} {},{},{},{}'.format(fd, fs, fn, fc[0], fc[1], fc[2], fc[3])
        print('updateCaption() {}'.format(text), file=DBG_FILE)
        self.set_caption(text)

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

    def on_mouse_release(self, x, y, button, modifiers):  # pyglet.window.mouse.MIDDLE #pyglet.window.mouse.LEFT #pyglet.window.mouse.RIGHT
        nc, nr = self.n[C] + CCC, self.n[R] * self.n[L]
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
########################################################################################################################################################################################################
    @staticmethod
    def isCtrl(mods):        return mods&pygwink.MOD_CTRL

    @staticmethod
    def isShift(mods):       return mods&pygwink.MOD_SHIFT

    @staticmethod
    def isAlt(mods):         return mods&pygwink.MOD_ALT

#    @staticmethod
#    def isCtrlShift(mods):   return (mods & pygwink.MOD_CTRL) and (mods & pygwink.MOD_SHIFT)

    @staticmethod
    def isTab(text):
        return True if text=='-' or Tabs.isFret(text) else False

    @staticmethod
    def isFret(text):
        return True if '0'<=text<='9' or 'a'<=text<='o' else False

    def quit(self, why=''):
        self.dumpStruct('quit() ' + why) if not TEST else self.dumpTest('quit() ' + why)
        print('quit() {}\nQuiting'.format(why), file=DBG_FILE)
        exit()
'''
    def _initTextTest_FOO(self, n):
        self._initText_A(['C', 'C#', 'Db', 'D', 'D#', 'Eb', 'E', ' ',  ' ',  'F', 'F#', 'Gb', 'G', 'G#', 'Ab', 'A', 'A#', 'Bb', 'B', ' ' , ' ' ],                            0*n, self.g[C+2], self.batch)
        self._initText_A(['C', 'C#', 'Db', 'D', 'D#', 'Eb', 'E', 'E#', 'Fb', 'F', 'F#', 'Gb', 'G', 'G#', 'Ab', 'A', 'A#', 'Bb', 'B', 'B#', 'Cb'],                            1*n, self.g[C+2], self.batch)
        self._initText_A(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'],                 2*n, self.g[C+2], self.batch)
        self._initText_A(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25'], 3*n, self.g[C+2], self.batch)
        self._initText_A(['~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '[', ']', '<', '>', '/', '?', ',', '.', '=', '_', '+', ' ', '|', '{', '}', '-', '\\'],      4*n, self.g[C+2], self.batch)
        ucnFlat, ucnNatural, ucnSharp = unicodedata.name('\u066D'), unicodedata.name('\u166E'), unicodedata.name('\u266F')
#        ucFlat,  ucNatural,  ucSharp  = unicodedata.lookup(ucnFlat), unicodedata.lookup(ucnNatural), unicodedata.lookup(ucnSharp)
#        ucFlat,  ucNatural,  ucSharp  = unicodedata.lookup('MUSIC FLAT SIGN'), unicodedata.lookup('MUSIC NATURAL SIGN'), unicodedata.lookup('MUSIC SHARP SIGN')
        print('    ucnFlat={}'.format(ucnFlat),     file=DBG_FILE)
        print(' ucnNatural={}'.format(ucnNatural),  file=DBG_FILE)
        print('   ucnSharp={}'.format(ucnSharp),    file=DBG_FILE)
#        print('     ucFlat={}'.format(ucFlat),      file=DBG_FILE)
#        print('  ucNatural={}'.format(ucNatural),   file=DBG_FILE)
#        print('    ucSharp={}'.format(ucSharp),     file=DBG_FILE)
#        self._initText_A([ucFlat],     4*n, self.g[C+2], self.batch)
#        self._initText_A([ucNatural],  5*n, self.g[C+2], self.batch)
#        self._initText_A([ucSharp],    6*n, self.g[C+2], self.batch)
#        self._initText_A([' ', ' ', ' ', ' ', '{#x266D}'], (255, 0, 0, 255), 3*n, self.g[C+2], self.batch) # Unicode seems to require a Document?
#        self._initText_A([' ', ' ', ' ', ' ', '{#x266F}'], (255, 0, 0, 255), 4*n, self.g[C+2], self.batch)
'''
########################################################################################################################################################################################################
if __name__=='__main__':
    TEST = 0 ;  CARET = 0 ;  ORDER_GROUP = 1 ;  SUBPIX = 1 ;  FULL_SCREEN = 0 ;  VRSN = 1 ; DBG = 0
    SFX          = 'TEST' if TEST else '{}'.format(VRSN)
    DBG_FILE     = open(sys.argv[0] + SFX + ".log.txt", 'w')
    DATA_FILE    = open(sys.argv[0] + SFX + ".dat.txt", 'w')
    P, L, R, C   = 0, 1, 2, 3
    OPACITY      = [255, 240, 225, 210, 190, 165, 140, 110, 80]
    GRAY         = [(255, 255, 255, OPACITY[0]), ( 0,  0,  0, OPACITY[0])]
    PINK         = [(255,  64, 192, OPACITY[0]), (57, 16, 16, OPACITY[0])]
    INFRA_RED    = [(255,  29,  24, OPACITY[0]), (68, 20, 19, OPACITY[0])]
    RED          = [(255,  24,  21, OPACITY[0]), (82, 15, 12, OPACITY[0])]
    ORANGE       = [(255, 128,  32, OPACITY[0]), (76, 30, 25, OPACITY[0])]
    YELLOW       = [(255, 255,  15, OPACITY[0]), (45, 41, 10, OPACITY[0])]
    GREEN        = [( 44, 255,   0, OPACITY[0]), (21, 54, 10, OPACITY[0])]
    GREEN_BLUE   = [( 24, 255,  61, OPACITY[0]), (10, 49, 25, OPACITY[0])]
    CYAN         = [( 32, 255, 255, OPACITY[0]), (16, 64, 64, OPACITY[0])]
    BLUE_GREEN   = [( 25, 181, 255, OPACITY[0]), (12, 37, 51, OPACITY[0])]
    BLUE         = [( 35,  26, 255, OPACITY[0]), (19, 11, 64, OPACITY[0])]
    ULTRA_VIOLET = [(176,  81, 255, OPACITY[0]), (44, 14, 58, OPACITY[0])]
    VIOLET       = [(194,  96, 255, OPACITY[3]), (50, 19, 61, OPACITY[1])]
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
    FONT_SIZES  = [4, 5, 6, 8, 9, 10, 11, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52]
    FONT_COLORS = [REDS[0], GREENS[0], BLUES[0], YELLOWS[0], ORANGES[0], GREEN_BLUES[0], CYANS[0], BLUE_GREENS[0], PINKS[0], INFRA_REDS[0], VIOLETS[0], ULTRA_VIOLETS[0], GRAYS[0]]
    FONT_DPIS    = [75, 80, 90, 96, 100, 108, 116, 124]
    tabs        = Tabs()
    pyglet.app.run()
#        cc = GREENS[-1::-1]+GREENS
