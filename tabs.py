import math, sys, os
import pyglet
import pyglet.window.key as pygwink
sys.path.insert(0, os.path.abspath('../lib'))
import cmdArgs

def fri(f): return int(math.floor(f+0.5))
RUN_TEST   = False

class Tabs(pyglet.window.Window):
    def __init__(self):
        self.ww, self.hh  = 1000, 600
        self.n            = [1, 2, 2, 0]
        self.x            = [0, 4, 10, 15]
        self.y            = [0, 3, 9, 15]
        self.w,  self.h   = [0, 0, 0, 0], [0, 0, 0, 0]
        self.w_, self.h_  = [0, 0, 0, 0], [0, 0, 0, 0]
        self.fullScreen   = False
        self.subpixel     = True
        self.argMap       = cmdArgs.parseCmdLine(dbg=1)
        print('Tabs.init() argMap={}'.format(self.argMap), file=DBG_FILE)
#        if 'w' in self.argMap and len(self.argMap['w'])  > 0: self.w            = [int(self.argMap['w'][i]) for i in range(len(self.argMap['w']))]
#        if 'h' in self.argMap and len(self.argMap['h'])  > 0: self.h            = [int(self.argMap['h'][i]) for i in range(len(self.argMap['h']))]
        if 'w' in self.argMap and len(self.argMap['w'])  > 0: self.ww           =  int(self.argMap['w'][0])
        if 'h' in self.argMap and len(self.argMap['h'])  > 0: self.hh           =  int(self.argMap['h'][0])
        if 'n' in self.argMap and len(self.argMap['n'])  > 0: self.n            = [int(self.argMap['n'][i]) for i in range(len(self.argMap['n']))]
        if 'x' in self.argMap and len(self.argMap['x'])  > 0: self.x            = [int(self.argMap['x'][i]) for i in range(len(self.argMap['x']))]
        if 'y' in self.argMap and len(self.argMap['y'])  > 0: self.y            = [int(self.argMap['y'][i]) for i in range(len(self.argMap['y']))]
        if 'S' in self.argMap and len(self.argMap['S']) == 0: self.fullScreen   = True
        if 's' in self.argMap and len(self.argMap['s']) == 0: self.subpixel     = True
        print('[ww]          ww={}'.format(self.ww),         file=DBG_FILE)
        print('[hh]          hh={}'.format(self.hh),         file=DBG_FILE)
        print('[n]            n={}'.format(self.n),          file=DBG_FILE)
        print('[x]            x={}'.format(self.x),          file=DBG_FILE)
        print('[y]            y={}'.format(self.y),          file=DBG_FILE)
        print('[S]   fullScreen={}'.format(self.fullScreen), file=DBG_FILE)
        print('[s]     subpixel={}'.format(self.subpixel),   file=DBG_FILE)
        self._initWindowA()
        super().__init__(screen=self.screens[1], fullscreen=self.fullScreen, resizable=True, visible=False)
        self._initWindowB()
        self.vpn = 0
        self.tci = 0
        self.useOrderedGroup = False
        print('_init() RUN_TEST={} useOrderedGroup={}'.format(RUN_TEST, self.useOrderedGroup), file=DBG_FILE)
        if RUN_TEST: self._initColorLists()
        else: self._initTabs()

    def _initWindowA(self):
        display      = pyglet.canvas.get_display()
        self.screens = display.get_screens()

    def _initWindowB(self):
        self.batch = pyglet.graphics.Batch()
        self.set_size(self.ww, self.hh)
        self.set_visible()
        print('_initWindow() ww={} hh={}'.format(self.ww, self.hh), file=DBG_FILE)

    def dumpGeom(self, reason, i):
        ww, hh, n, x, y, w, h = self.ww, self.hh, self.n[i], self.x[i], self.y[i], self.w[i], self.h[i]
        print('{:25}'.format(reason), file=DBG_FILE)
        print('[{}] ww={:4} hh={:4} n={:3} x={:3} y={:3} w={:7.2f} h={:7.2f}'.format(i, ww, hh, n, x, y, w, h), file=DBG_FILE)
#        [print('[{}] ww={:4} hh={:4} n={:3} x={:3} y={:3} w={:7.2f} h={:7.2f}'.format(i, ww[i%2], hh[i%2], n[i], x[i], y[i], w[i], h[i]), file=DBG_FILE) for i in range(len(n)) if n[i] > 0]
#        print('{:25} ww={} hh={} n={} x={} y={} w={} h={}'.format(reason, self.ww, self.hh, self.n, self.x, self.y, self.w, self.h), file=DBG_FILE)

    def resizeGeom(self, reason, i, g, init=True, dg=True, ds=True):
        ww, hh, n, x, y = self.ww, self.hh, self.n[i], self.x[i], self.y[i]
        if g == 0:
            self.w[i] = (ww -     2*x)
            self.h[i] = (hh -     2*y)
        elif g == 1:
            self.w[i] = (ww -     2*x)
            self.h[i] = (hh - (n+1)*y)/n
        elif g == 2:
            self.w[i] = (ww - (n+1)*x)/n if n != 0 else 100
            self.h[i] = (hh - (n+1)*y)/n if n != 0 else 100
        if init: self.w_[i], self.h_[i] = self.w[i], self.h[i]
        if dg: self.dumpGeom(reason, i)
        if ds: self.dumpSprite(None)
        return ww, hh, n, x, y, self.w[i], self.h[i], self.w_[i], self.h_[i]

    def _initColorLists(self):
        self.clGroup = self._initGroup(0)
        ww, hh, n1, x1, y1, w1, h1, w_1, h_1 = self.resizeGeom('_initColorLists(BGN)', 0, 2, init=True, ds=False)
        ww, hh, n2, x2, y2, w2, h2, w_2, h_2 = self.resizeGeom('_initColorLists(BGN)', 1, 2, init=True, ds=False)
        c = COLOR[:n1]
        end = ['\n', ' ']
        [[print('{:2} {:2} {:3} {:3} {:3} {:3}'.format(i, j, c[i][j][0], c[i][j][1], c[i][j][2], c[i][j][3]), file=DBG_FILE, end=end[0 if j==n2-1 else 1]) for j in range(n2)] for i in range(n1)]
        self.dumpSprite(None)
        self.colorListSprites = []
        for i in range(n1):
            sprites = []
            for j in range(n2):
                xx, yy = x1+(w1+x1)*i, hh-(h2+y2)*(j+1)
                scip = pyglet.image.SolidColorImagePattern(c[i][j])
                sci = scip.create_image(width=fri(w1), height=fri(h2))
                spr = self.createSprite('_initColorLists()', sci, self.clGroup, xx, yy, w1, h2, i, j, v=True, no=0) #n[0], o=255)
                sprites.append(spr)
            self.colorListSprites.append(sprites)

    def resizeColorLists(self):
        cls = self.colorListSprites
        ww, hh, n1, x1, y1, w1, h1, w_1, h_1 = self.resizeGeom('resizeColorLists(BGN)', 0, 2, init=False)
        ww, hh, n2, x2, y2, w2, h2, w_2, h_2 = self.resizeGeom('resizeColorLists(BGN)', 1, 2, init=False)
        for i in range(n1):
            for j in range(n2):
                xx, yy = x1+(w1+x1)*i, hh-(h2+y2)*(j+1)
                cls[i][j].update(x=xx, y=yy, scale_x=w1/w_1, scale_y=h2/h_2)
                self.dumpSprite('{:20} {:3} {:3} {:8.2f} {:8.2f} {:8.2f} {:8.2f}'.format('resizeColorLists()', i, j, xx, yy, w1, h2), cls[i][j])
        print('resizeColorLists(END) ww={} x={} w={:7.2f} x+w={:7.2f} ww-x-w={:7.2f} : y={} hh={} h={:7.2f} y+h={:7.2f} hh-y-h={:7.2f}'.format(ww, x1, w1, x1+w1, ww-x1-w1, hh, y2, h2, y2+h2, hh-y2-h2), file=DBG_FILE)

    def createSprite(self, reason, img, grp, x, y, w, h, i, j, v=None, no=0, o=255):
#        img.anchor_x, img.anchor_y = fri(w/2), fri(h/2)
        s = pyglet.sprite.Sprite(img, x, y, batch=self.batch, group=grp, subpixel=self.subpixel)
        s.visible = v if v is not None else True if i==0 else False
        s.opacity = self.getOpacity(o, j, no)
#        if c==0 or r==0 or c==self.nc-1 or r==self.nr-1:
        self.dumpSprite('{:20} {:3} {:3} {:8.2f} {:8.2f} {:8.2f} {:8.2f} {:4} {:4}'.format(reason, i, j, x, y, w, h, img.anchor_x, img.anchor_y), s)
        return s

    def _initGroup(self, order=0, parent=None):
        if self.useOrderedGroup: return pyglet.graphics.OrderedGroup(order, parent)
        else:                    return pyglet.graphics.Group(parent)

    def _initTabs(self):
        print('_initTabs(BGN) nPages={} linesPerPage={} rowsPerLine={} colsPerRow={}'.format(self.n[0], self.n[1], self.n[2], self.n[3]), file=DBG_FILE)
        self.pages, self.lines, self.rows, self.cols = [], [], [], []
#        if not self.useOrderedGroup: self.rootGroup = pyglet.graphics.Group()
        self._initPages()
        print('_initTabs(END) nPages={} linesPerPage={} rowsPerLine={} colsPerRow={}'.format(self.n[0], self.n[1], self.n[2], self.n[3]), file=DBG_FILE)

    def _initPages(self):
        self.pageColors  = [YELLOWS[i] for i in range(len(YELLOWS))]
        i = P
        self.pageGroup   = self._initGroup(i)
        ww, hh, n, x, y, w, h, w_, h_ = self.resizeGeom('_initPages(BGN)', i, 0, init=True)
        for p in range(n):
            scip   = pyglet.image.SolidColorImagePattern(self.pageColors[p%n])
            img    = scip.create_image(width=fri(w), height=fri(h))
            page   = self.createSprite('_initPages', img, self.pageGroup, x, y, w, h, p, 0)
            self.pages.append(page)
            if self.n[L] > 0: lines = self._initLines()
#            self.pages.append(lines)
        return self.pages

    def _initLines(self):
        self.lineColors  = [REDS[i] for i in range(len(REDS))]
        i = L
        self.lineGroup   = self._initGroup(i)
        ww, hh, n, x, y, w, h, w_, h_ = self.resizeGeom('_initLines(BGN)', i, 1, init=True)
        lines = []
        for l in range(n):
            yy = hh-(h+y)*(l+1)
            scip   = pyglet.image.SolidColorImagePattern(self.lineColors[l%n])
            img    = scip.create_image(width=fri(w), height=fri(h))
            line   = self.createSprite('_initLines', img, self.lineGroup, x, yy, w, h, l, 0, v=True if len(self.pages)==1 else False)
            self.lines.append(line)
            if self.n[R] > 0: rows = self._initRows()
#            lines.append(rows)
#        self.lines.append(lines)
        return lines

    def _initRows(self, ):
        self.rowColors = [BLUES[i] for i in range(len(BLUES))]
        i = R
        self.rowGroup = self._initGroup(i)
        ww, hh, n, x, y, w, h, w_, h_ = self.resizeGeom('_initRows(BGN)', i, 1, init=True)
        rows = []
        for r in range(n):
            yy = hh-(h+y)*(r+1)
            scip   = pyglet.image.SolidColorImagePattern(self.rowColors[r%n])
            img    = scip.create_image(width=fri(w), height=fri(h))
            row   = self.createSprite('_initRows', img, self.rowGroup, x, yy, w, h, r, 0, v=True if len(self.pages)==1 else False)
            self.rows.append(row)
            if self.n[C] > 0: cols = self._initCols()
        return rows

    def _initCols(self):
        self.colColors = [GREENS[i] for i in range(len(GREENS))]
        i = C
        self.colGroup = self._initGroup(i)
        ww, hh, n, x, y, w, h, w_, h_ = self.resizeGeom('_initCols(BGN)', i, 2, init=True)
        cols = []
        for c in range(n):
            xx, yy = x+(w+x)*c, hh-(h+y)*(c+1)
            scip = pyglet.image.SolidColorImagePattern(self.colColors[c%n])
            img = scip.create_image(width=fri(w), height=fri(h))
            col   = self.createSprite('_initCols', img, self.colGroup, xx, yy, w, h, c, 0, v=True if len(self.pages)==1 else False)
            self.cols.append(col)
        return cols

    def on_resize(self, width, height):
        super().on_resize(width, height)
        self.ww, self.hh = width, height
        if RUN_TEST: self.resizeColorLists(); return
        if len(self.pages) > 0:
            ww, hh, n, x, y, w, h, w_, h_ = self.resizeGeom('on_resize(BGN) Pages', P, 0, init=False)
            mx, my = w/w_, n*h/h_
            for p in range(n):
                self.pages[p].update(x=x, y=y, scale_x=mx, scale_y=my)
                self.dumpSprite('{:20} {:3} {:3} {:8.2f} {:8.2f} {:8.2f} {:8.2f}'.format('on_resize() Pages', p, 0, x, y, w, h), self.pages[p])
        if len(self.lines) > 0:
            ww, hh, n, x, y, w, h, w_, h_ = self.resizeGeom('on_resize(BGN) Lines', L, 1, init=False)
            mx, my = w/w_, h/h_
            for l in range(n):
                yy = hh-(h+y)*(l+1)
                self.lines[l].update(x=x, y=yy, scale_x=mx, scale_y=my)
                self.dumpSprite('{:20} {:3} {:3} {:8.2f} {:8.2f} {:8.2f} {:8.2f}'.format('on_resize() Lines', l, 0, x, yy, w, h), self.lines[l])
        if len(self.rows) > 0:
            ww, hh, n, x, y, w, h, w_, h_ = self.resizeGeom('on_resize(BGN) rows', R, 1, init=False)
            mx, my = w/w_, h/h_
            for r in range(n):
                yy = hh-(h+y)*(r+1)
                self.rows[r].update(x=x, y=yy, scale_x=mx, scale_y=my)
                self.dumpSprite('{:20} {:3} {:3} {:8.2f} {:8.2f} {:8.2f} {:8.2f}'.format('on_resize() Rows', r, 0, x, yy, w, h), self.rows[r])
        if len(self.cols) > 0:
            ww, hh, n, x, y, w, h, w_, h_ = self.resizeGeom('on_resize(BGN) cols', C, 2, init=False)
            mx, my = w/w_, h/h_
            for c in range(n):
                xx, yy = x+(w+x)*c, hh-(h+y)*(c+1)
                self.cols[c].update(x=xx, y=yy, scale_x=mx, scale_y=my)
                self.dumpSprite('{:20} {:3} {:3} {:8.2f} {:8.2f} {:8.2f} {:8.2f}'.format('on_resize() Cols', c, 0, xx, yy, w, h), self.cols[c])

    @staticmethod
    def dumpSprite(reason, s=None):
        if s is None: print('     x        y        w        h    iax  iay    m      mx     my      rot   opacity    color      visible      reason         i   j       x        y        w        h    iax  iay', file=DBG_FILE); return
        f = '{:8.2f} {:8.2f} {:8.2f} {:8.2f} {:4} {:4} {:6.3f} {:6.3f} {:6.3f} {:8.2f}  {:4}  {}  {}'
        fs = f.format(s.x, s.y, s.width, s.height, s.image.anchor_x, s.image.anchor_y, s.scale, s.scale_x, s.scale_y, s.rotation, s.opacity, s.color, s.visible)
        print('{} {}'.format(fs, reason), file=DBG_FILE)
        assert(type(s) == pyglet.sprite.Sprite)

    @staticmethod
    def getOpacity(opacity=255, i=0, ni=0):
        if ni <= 0: return opacity
        else:       return fri(opacity*((i+1) % (ni+1))/ni)

    def printStructInfo(self, reason=''):
        print('{} ppf={} lpp={} rpl={} cpr={} len(pages)={} len(lines)={} len(rows)={} len(cols)={}'
              .format(reason, self.pagesPerFile, self.linesPerPage, self.rowsPerLine, self.colsPerRow, len(self.pages), len(self.lines), len(self.rows), len(self.cols)), file=DBG_FILE)

#    def printStruct(self, reason=''):
#        self.printStructInfo('printStruct(BGN) {}'.format(reason))
#        ppf, lpp, rpl, cpr = len(self.pages), len(self.lines), len(self.rows), len(self.cols)
#        for p in range(ppf):
#            self.printSpriteInfo('pages[{}]'.format(p), self.pages[p])
#        for l in range(lpp):
#            self.printSpriteInfo('lines[{}]'.format(l), self.lines[l])
#        for r in range(rpl):
#            self.printSpriteInfo('rows[{}]'.format(r), self.rows[r])
#        for c in range(cpr):
#            self.printSpriteInfo('cols[{}]'.format(c), self.cols[c])

    def printStruct_OLD(self, np, lpp, rpl, cpr):
        self.printStructInfo('printStruct(BGN)')
#        print('printStruct() np={} lpp={} rpl={} cpr={}'.format(np, lpp, rpl, cpr), file=DBG_FILE)
        for p in range(np):
            for l in range(lpp):
                for r in range(rpl):
                    for c in range(cpr):
                        q = self.pages[p][l][r][c]
                        print('pages: p={} l={} r={} c={} position=({:5.1f}, {:5.1f}) w={:5.1f} h={:5.1f}'.format(p, l, r, c, q.x, q.y, q.width, q.height), file=DBG_FILE)
        print('printStruct() len(pages)={} lpp={} rpl={} cpr={}'.format(len(self.pages), lpp, rpl, cpr), file=DBG_FILE)
        for p in range(len(self.pages)):
            for l in range(lpp):
                for r in range(rpl):
                    for c in range(cpr):
                        q = self.pages[p][l][r][c]
                        print('pages: p={} l={} r={} c={} position=({:5.1f}, {:5.1f}) w={:5.1f} h={:5.1f}'.format(p, l, r, c, q.x, q.y, q.width, q.height), file=DBG_FILE)
        print('printStruct() len(lines)={} rpl={} cpr={}'.format(len(self.lines), rpl, cpr), file=DBG_FILE)
        for l in range(len(self.lines)):
            for r in range(rpl):
                for c in range(cpr):
                    q = self.lines[l][r][c][0]
                    print('lines: l={} r={} c={} position=({:5.1f}, {:5.1f}) w={:5.1f} h={:5.1f}'.format(l, r, c, q.x, q.y, q.width, q.height), file=DBG_FILE)
        print('printStruct() len(rows)={} cpr={}'.format(len(self.rows), cpr), file=DBG_FILE)
        for r in range(len(self.rows)):
            for c in range(cpr):
                q = self.rows[r][c][0]
                print('rows: r={} c={} position=({:5.1f}, {:5.1f}) w={:5.1f} h={:5.1f}'.format(r, c, q.x, q.y, q.width, q.height), file=DBG_FILE)
        print('printStruct() len(cols)={}'.format(len(self.cols)), file=DBG_FILE)
        for c in range(len(self.cols)):
            q = self.cols[c][0]
            print('cols: c={} position=({:5.1f}, {:5.1f}) w={:5.1f} h={:5.1f}'.format(c, q.x, q.y, q.width, q.height), file=DBG_FILE)
        self.printStructInfo('printStruct(END)')

    def _verify(self):
        self.printStruct_OLD(1, 1, 1, 1)
        self.printStruct_OLD(self.pagesPerFile, 1, 1, 1)
        self.printStruct_OLD(self.pagesPerFile, self.linesPerPage, 1, 1)
        self.printStruct_OLD(self.pagesPerFile, self.linesPerPage, self.rowsPerLine, 1)
        self.printStruct_OLD(self.pagesPerFile, self.linesPerPage, self.rowsPerLine, self.colsPerRow)
        struct = (self.pages, self.lines, self.rows, self.cols)
        ln = [len(e) for e in struct]
        sz = [self.size(e) for e in struct]
        d1 = dict(zip(['pages', 'lines', 'rows', 'cols'], ln))
        d2 = dict(zip(['pages', 'lines', 'rows', 'cols'], sz))
        print('_verify() d1={} d2={}'.format(d1, d2), file=DBG_FILE)
        assert(d1['pages'] == self.pagesPerFile)
        assert(d1['lines'] == self.pagesPerFile * self.linesPerPage)
        assert(d1['rows']  == self.pagesPerFile * self.linesPerPage * self.rowsPerLine)
        assert(d1['cols']  == self.pagesPerFile * self.linesPerPage * self.rowsPerLine * self.colsPerRow)
        assert(d2['pages'] == self.pagesPerFile * self.linesPerPage * self.rowsPerLine * self.colsPerRow)
        assert(d2['lines'] == self.pagesPerFile * self.linesPerPage * self.rowsPerLine * self.colsPerRow)
        assert(d2['rows']  == self.pagesPerFile * self.linesPerPage * self.rowsPerLine * self.colsPerRow)
        assert(d2['cols']  == self.pagesPerFile * self.linesPerPage * self.rowsPerLine * self.colsPerRow)

    def size(self, item):
        if isinstance(item, list): return sum([self.size(i) for i in item])
        return 1

    def on_draw(self):
        self.clear()
        self.batch.draw()

    def on_text(self, text):
        print('on_text() text={}'.format(text), file=DBG_FILE)

    def on_text_motion(self, motion):
        if   motion == pygwink.MOTION_LEFT:          self.toggleColorLists(motion)
        elif motion == pygwink.MOTION_RIGHT:         self.toggleColorLists(motion)
        elif motion == pygwink.MOTION_NEXT_PAGE:     self.setCurrPage(motion)
        elif motion == pygwink.MOTION_PREVIOUS_PAGE: self.setCurrPage(motion)
        else:                                        print('on_text_motion() motion={} ???'.format(motion), file=DBG_FILE)

#    pyglet.image.get_buffer_manager().get_color_buffer().save('screenshot.png')

    def toggleColorLists(self, motion):
        if not RUN_TEST:
            print('toggleColorLists(WARNING) Nothing To Toggle RUN_TEST={} motion={}'.format(RUN_TEST, motion), file=DBG_FILE)
            return
        cls = self.colorListSprites
        if   motion==pygwink.MOTION_LEFT:
            for j in range(len(cls[self.tci])): cls[self.tci][j].visible = False
            self.tci -= 1
            self.tci = self.tci % len(COLOR)
            for j in range(len(cls[self.tci])): cls[self.tci][j].visible = True
            print('toggleColorLists() MOTION_LEFT={} tci={} len(cls)={}'.format(motion, self.tci, len(cls)), file=DBG_FILE)
        elif motion==pygwink.MOTION_RIGHT:
            for j in range(len(cls[self.tci])): cls[self.tci][j].visible = False
            self.tci += 1
            self.tci = self.tci % len(COLOR)
            for j in range(len(cls[self.tci])): cls[self.tci][j].visible = True
            print('toggleColorLists() MOTION_RIGHT={} tci={} len(cls)={}'.format(motion, self.tci, len(cls)), file=DBG_FILE)

    def setCurrPage(self, motion):
        if motion==pygwink.MOTION_NEXT_PAGE:
            self.pages[self.vpn].visible = False
            self.vpn += 1
            self.vpn = self.vpn % self.pagesPerFile
            self.pages[self.vpn].visible = True
            print('setCurrPage() motion={} MOTION_NEXT_PAGE cpn={}'.format(motion, self.vpn), file=DBG_FILE)
        elif motion==pygwink.MOTION_PREVIOUS_PAGE:
            self.pages[self.vpn].visible = False
            self.vpn -= 1
            self.vpn = self.vpn % self.pagesPerFile
            self.pages[self.vpn].visible = True
            print('setCurrPage() motion={} MOTION_PREVIOUS_PAGE cpn={}'.format(motion, self.vpn), file=DBG_FILE)

def genColors(colors, ns=8):
    _colors, _len = [], len(colors[0])
    diffs = [colors[1][i] - colors[0][i] for i in range(_len)]
    steps = [diffs[i]/ns   for i in range(_len)]
    print('genColors(), c1={} c2={} ns={} diffs={} steps={}'.format(colors[0], colors[1], ns, diffs, steps))
    for j in range(ns):
        c = tuple([fri(colors[0][i]+j*steps[i]) for i in range(len(colors[0]))])
        print('genColors() c[{}]={}'.format(j, c))
        _colors.append(c)
    print('genColors() colors={}'.format(colors))
    return _colors

if __name__ == '__main__':
    SFX        = 'TEST' if RUN_TEST else ''
    DBG_FILE   = open(sys.argv[0] + SFX + ".log.txt", 'w')
    P, L, R, C = 0, 1, 2, 3
    VIOLET     = [(255, 64, 192, 255), (64, 16, 16, 255)]
    RED        = [(255, 32, 32, 255), (64, 16, 16, 255)]
    ORANGE     = [(255, 128, 32, 255), (64, 16, 16, 255)]
    YELLOW     = [(255, 255, 64, 255), (64, 64, 16, 255)]
    GREEN      = [(64, 255, 32, 255), (16, 64, 16, 255)]
    CYAN       = [(32, 255, 255, 255), (16, 64, 64, 255)]
    BLUE       = [(32, 64, 255, 255), (16, 16, 64, 255)]
    PURPLE     = [(208, 96, 255, 255), (64, 16, 64, 255)]
    FOO        = [(255, 192, 64, 255), (64, 64, 32, 255)]
    REDS       = genColors(RED)
    GREENS     = genColors(GREEN)
    BLUES      = genColors(BLUE)
    YELLOWS    = genColors(YELLOW)
    CYANS      = genColors(CYAN)
    VIOLETS    = genColors(VIOLET)
    ORANGES    = genColors(ORANGE)
    PURPLES    = genColors(PURPLE)
    FOOS       = genColors(FOO)
    COLOR      = (VIOLETS, REDS, ORANGES, YELLOWS, GREENS, CYANS, BLUES, PURPLES, FOOS)
    tabs       = Tabs()
    pyglet.app.run()
