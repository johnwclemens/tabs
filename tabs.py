import math, sys, os
import pyglet
import pyglet.window.key as pygwink
sys.path.insert(0, os.path.abspath('../lib'))
import cmdArgs

def fri(f): return int(math.floor(f+0.5))
RUN_TEST = False;  ORDER_GROUP = True;  SUBPIX = True;  FULL_SCREEN = False

class Tabs(pyglet.window.Window):
    def __init__(self):
        global FULL_SCREEN, SUBPIX, ORDER_GROUP, RUN_TEST
        self.ww, self.hh  = 1000, 600
        if RUN_TEST: self.n, self.x, self.y, self.w, self.h, self.o, self.g = [1, 12, 0, 0], [4, 0, 0, 0], [0, 3, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [1, 1, 0, 0], []
        else:        self.n, self.x, self.y, self.w, self.h, self.o, self.g = [1, 2, 2, 0],  [0, 4, 6, 8], [0, 3, 5, 7], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], []
        self.argMap = cmdArgs.parseCmdLine(dbg=1)
        print('Tabs.init() argMap={}'.format(self.argMap), file=DBG_FILE)
        if 'n' in self.argMap and len(self.argMap['n'])  > 0: self.n            = [int(self.argMap['n'][i]) for i in range(len(self.argMap['n']))]
        if 'x' in self.argMap and len(self.argMap['x'])  > 0: self.x            = [int(self.argMap['x'][i]) for i in range(len(self.argMap['x']))]
        if 'y' in self.argMap and len(self.argMap['y'])  > 0: self.y            = [int(self.argMap['y'][i]) for i in range(len(self.argMap['y']))]
        if 'w' in self.argMap and len(self.argMap['w'])  > 0: self.ww           =  int(self.argMap['w'][0])
        if 'h' in self.argMap and len(self.argMap['h'])  > 0: self.hh           =  int(self.argMap['h'][0])
        if 'o' in self.argMap and len(self.argMap['o'])  > 0: self.o            = [int(self.argMap['o'][i]) for i in range(len(self.argMap['o']))]
        if 'S' in self.argMap and len(self.argMap['S']) == 0: FULL_SCREEN       = True
        if 's' in self.argMap and len(self.argMap['s']) == 0: SUBPIX            = True
        if 'o' in self.argMap and len(self.argMap['o']) == 0: ORDER_GROUP       = True
        if 't' in self.argMap and len(self.argMap['t']) == 0: RUN_TEST          = True
        print('[n]            n={}'.format(self.n),          file=DBG_FILE)
        print('[x]            x={}'.format(self.x),          file=DBG_FILE)
        print('[y]            y={}'.format(self.y),          file=DBG_FILE)
        print('[w]           ww={}'.format(self.ww),         file=DBG_FILE)
        print('[h]           hh={}'.format(self.hh),         file=DBG_FILE)
        print('[o]            o={}'.format(self.o),          file=DBG_FILE)
        print('[S]  FULL_SCREEN={}'.format(FULL_SCREEN),     file=DBG_FILE)
        print('[s]       SUBPIX={}'.format(SUBPIX),          file=DBG_FILE)
        print('[g]  ORDER_GROUP={}'.format(ORDER_GROUP),     file=DBG_FILE)
        print('[t]     RUN_TEST={}'.format(RUN_TEST),        file=DBG_FILE)
        self._initWindowA()
        super().__init__(screen=self.screens[1], fullscreen=FULL_SCREEN, resizable=True, visible=False)
        self._initWindowB()
        self.vpn = 0
        self.tci = 0
        if RUN_TEST: self._initColorLists()
        else:        self._initTabs()

    def _initWindowA(self):
        display      = pyglet.canvas.get_display()
        self.screens = display.get_screens()

    def _initWindowB(self):
        self.batch = pyglet.graphics.Batch()
        self._initGroups()
        self.set_size(self.ww, self.hh)
        self.set_visible()
        print('_initWindowB() ww={} hh={}'.format(self.ww, self.hh), file=DBG_FILE)

    def _initGroups(self):
        for i in range(len(self.n)):
            self.g.append(self._initGroup(i))

    @staticmethod
    def _initGroup(order=0, parent=None):
        if ORDER_GROUP: return pyglet.graphics.OrderedGroup(order, parent)
        else:           return pyglet.graphics.Group(parent)

    def _initTabs(self):
        self._initPages()

    def _initColorLists(self):
        self.clGroup = self._initGroup(0)
        n1, x1, y1, w1, h1, o1, g1, self.colorLists = self.geom(0, 0, 0, self.ww, self.hh, reason=None, init=True)
        n2, x2, y2, w2, h2, o2, g2, self.colorLists = self.geom(1, 0, 0, self.ww, self.hh, reason=None, init=True)
        for i in (P, L): self.dumpGeom(i, '_initColorLists() i={}'.format(i))
        c = COLOR[2] #:n1]
#        end = ['\n', ' '];        [[print('{:2} {:2} {:3} {:3} {:3} {:3}'.format(i, j, c[i][j][0], c[i][j][1], c[i][j][2], c[i][j][3]), file=DBG_FILE, end=end[0 if j==n2-1 else 1]) for j in range(n2)] for i in range(n1)]
        self.dumpSprite(None)
        for i in range(n1):
            sprites = []
            for j in range(n2):
                xx, yy = x1+(w1+x1)*i, self.hh-(h2+y2)*(j+1)
                spr = self.createSprite('_initColorLists()', self.clGroup, c, n1, xx, yy, w1, h2, i, j, v=True, no=0) #n[0], o=255)
                sprites.append(spr)
            self.colorLists.append(sprites)

    def resizeColorLists(self):
        cls = self.colorLists
        ww, hh = self.ww, self.hh
        n1, x1, y1, w1, h1, o1, g1, mx, my = self.geom(0, 0, 0, ww, hh, 'resizeColorLists() i=0', init=False)
        n2, x2, y2, w2, h2, o2, g2, mx, my = self.geom(1, 0, 0, ww, hh, 'resizeColorLists() i=1', init=False)
        for i in range(n1):
            for j in range(n2):
                xx, yy = x1+(w1+x1)*i, hh-(h2+y2)*(j+1)
                cls[i][j].update(x=xx, y=yy, scale_x=w1/self.w[P], scale_y=h2/self.h[L])
                self.dumpSprite('{:20} {:3} {:3} {:7.2f} {:7.2f} {:7.2f} {:7.2f}'.format('resizeColorLists()', i, j, xx, yy, w1, h2), cls[i][j])
        print('resizeColorLists(END) ww={} x={} w={:7.2f} x+w={:7.2f} ww-x-w={:7.2f} : y={} hh={} h={:7.2f} y+h={:7.2f} hh-y-h={:7.2f}'.format(ww, x1, w1, x1+w1, ww-x1-w1, hh, y2, h2, y2+h2, hh-y2-h2), file=DBG_FILE)

    def geom(self, i, px, py, pw, ph, reason=None, init=False):
        n, x, y, w, h, o, g = self.n[i], self.x[i], self.y[i], self.w[i], self.h[i], self.o[i], self.g[i]
        if   o==0: w, h =  pw-2*x,        (ph-y*(n+1))/n
        elif o==1: w, h = (pw-x*(n+1))/n, (ph-y*(n+1))/n
        if init: self.w[i], self.h[i] = w, h
        x += px; y += py
        if reason is not None:
            self.dumpGeom(i, reason)
            self.dumpSprite(None)
        mx, my = w/self.w[i], h/self.h[i]
        if init: return n, x, y, w, h, o, g, []
        else:    return n, x, y, w, h, o, g, mx, my

#    def inlay(self):

    def createSprite(self, reason, grp, clr, n, x, y, w, h, i, j, v=None, no=0, o=255):#        img.anchor_x, img.anchor_y = fri(w/2), fri(h/2)
        scip = pyglet.image.SolidColorImagePattern(clr[i%n])
        img = scip.create_image(width=fri(w), height=fri(h))
        spr = pyglet.sprite.Sprite(img, x, y, batch=self.batch, group=grp, subpixel=SUBPIX)
        spr.visible = v if v is not None else True if i==0 else False
        spr.opacity = self.getOpacity(o, j, no)
        self.dumpSprite('{:20} {:3} {:3} {:7.2f} {:7.2f} {:7.2f} {:7.2f} {:4} {:4}'.format(reason, i, j, x, y, w, h, img.anchor_x, img.anchor_y), spr)
        return spr

    def _initPages(self):
        clr  = [YELLOWS[i] for i in range(len(YELLOWS))]
        n, x, y, w, h, o, g, self.pages = self.geom(P, 0, 0, self.ww, self.hh, '_initPages(BGN)', init=True)
        for p in range(n):
            page   = self.createSprite('_initPages', g, clr, n, x, y, w, h, p, 0)
            self.pages.append(page)
            if self.n[L] > 0: lines = self._initLines(page)
        return self.pages

    def _initLines(self, spr):
        clr  = [REDS[i] for i in range(len(REDS))]
        n, x, y, w, h, o, g, self.lines = self.geom(L, spr.x, spr.y, spr.width, spr.height, '_initLines(BGN)', init=True)
        for l in range(n):
            yy = spr.height-(h+y)*(l+1)
            line   = self.createSprite('_initLines', g, clr, n, x, yy, w, h, l, 0, v=True if len(self.pages)==1 else False)
            self.lines.append(line)
            if self.n[R] > 0: rows = self._initRows(line)
        return self.lines

    def _initRows(self, spr):
        clr = [BLUES[i] for i in range(len(BLUES))]
        n, x, y, w, h, o, g, self.rows = self.geom(R, spr.x, spr.y, spr.width, spr.height, '_initRows(BGN)', init=True)
        for r in range(n):
            if y < h: yy = spr.height-(h+y)*(r+1)
            else:     yy = spr.y+spr.height-(self.y[R]+h)*(r+1)
#            yy = y+(h+self.y[R])*r
            row   = self.createSprite('_initRows', g, clr, n, x, yy, w, h, r, 0, v=True if len(self.pages)==1 else False)
            self.rows.append(row)
            if self.n[C] > 0: cols = self._initCols(row)
        return self.rows

    def _initCols(self, spr):
        clr = [GREENS[i] for i in range(len(GREENS))]
        n, x, y, w, h, o, g, self.cols = self.geom(C, spr.x, spr.y-spr.height, spr.width, spr.height, '_initCols(BGN)', init=True)
        for c in range(n):
            xx, yy = x+(w+x)*c, spr.height-(h+y)*(c+1)
            col   = self.createSprite('_initCols', g, clr, n, xx, yy, w, h, c, 0, v=True if len(self.pages)==1 else False)
            self.cols.append(col)
        return self.cols

    def on_resize(self, width, height):
        super().on_resize(width, height)
        self.ww, self.hh = width, height
        if RUN_TEST: self.resizeColorLists(); return
        for i in range(2): self.dumpGeom(i, 'on_resize({})'.format(i))
        self.dumpSprite(None)
        self.resizePages()

    def resizePages(self):
#        n, x, y, w, h = self.n[P], self.x[P], self.y[P], self.ww, self.hh
        n, x, y, w, h, o, g, mx, my = self.geom(P, self.x[P], self.y[P], self.ww, self.hh, reason=None, init=False)
#        mx, my = w/self.w[P], h/self.h[P]
        for p in range(n):
            self.pages[p].update(x=x, y=y, scale_x=mx, scale_y=my)
            self.dumpSprite('{:20} {:3} {:3} {:7.2f} {:7.2f} {:7.2f} {:7.2f}'.format('on_resize() Pages', p, 0, x, y, w, h), self.pages[p])
            if self.n[L] > 0: self.resizeLines(self.pages[p])

    def resizeLines(self, spr):
        n, x, y, w, h, o, g, mx, my = self.geom(L, spr.x, spr.y, spr.width, spr.height, reason=None, init=False) #, 'on_resize(BGN) Lines')
#        mx, my = w/self.w[L], h/self.h[L]
        for l in range(n):
            yy = spr.height-(h+y)*(l+1)
            self.lines[l].update(x=x, y=yy, scale_x=mx, scale_y=my)
            self.dumpSprite('{:20} {:3} {:3} {:7.2f} {:7.2f} {:7.2f} {:7.2f}'.format('on_resize() Lines', l, 0, x, yy, w, h), self.lines[l])
            if self.n[R] > 0: self.resizeRows(self.lines[l])

    def resizeRows(self, spr):
        n, x, y, w, h, o, g, mx, my = self.geom(R, spr.x, spr.y, spr.width, spr.height, reason=None, init=False) #, 'on_resize(BGN) Rows')
#        mx, my = w/self.w[R], h/self.h[R]
        for r in range(n):
#            yy = spr.height-(h+y)*(r+1)
            yy = y+(h+self.y[R])*r
            self.rows[r].update(x=x, y=yy, scale_x=mx, scale_y=my)
            self.dumpSprite('{:20} {:3} {:3} {:7.2f} {:7.2f} {:7.2f} {:7.2f}'.format('on_resize() Rows', r, 0, x, yy, w, h), self.rows[r])
            if self.n[C] > 0: self.resizeCols(self.rows[r])

    def resizeCols(self, spr):
        n, x, y, w, h, o, g, mx, my = self.geom(C, spr.x, spr.y, spr.width, spr.height, reason=None, init=False) #, 'on_resize(BGN) Cols')
#        mx, my = w/self.w[C], h/self.h[C]
        for c in range(n):
            xx, yy = x+(w+x)*c, spr.height-(h+y)*(c+1)
            self.cols[c].update(x=xx, y=yy, scale_x=mx, scale_y=my)
            self.dumpSprite('{:20} {:3} {:3} {:7.2f} {:7.2f} {:7.2f} {:7.2f}'.format('on_resize() Cols', c, 0, xx, yy, w, h), self.cols[c])

    def dumpGeom(self, i, reason=None):
        ww, hh, n, x, y, w, h, g, o = self.ww, self.hh, self.n[i], self.x[i], self.y[i], self.w[i], self.h[i], self.g[i], self.o[i]
        print('{:25} ww={:4} hh={:4}'.format(reason, ww, hh), file=DBG_FILE, end=' ')
        print('i={} n={:3} x={:3} y={:3} w={:7.2f} h={:7.2f} o={} g={}'.format(i, n, x, y, w, h, o, g), file=DBG_FILE)
#        [print('[{}] ww={:4} hh={:4} n={:3} x={:3} y={:3} w={:7.2f} h={:7.2f}'.format(i, ww[i%2], hh[i%2], n[i], x[i], y[i], w[i], h[i]), file=DBG_FILE) for i in range(len(n)) if n[i] > 0]
#        print('{:25} ww={} hh={} n={} x={} y={} w={} h={}'.format(reason, self.ww, self.hh, self.n, self.x, self.y, self.w, self.h), file=DBG_FILE)

    @staticmethod
    def dumpSprite(reason, s=None):
        if s is None: print('    x       y       w       h    iax  iay    m      mx     my     rot   opacity    color    visible     reason         i   j      x       y       w       h    iax  iay', file=DBG_FILE); return
        f = '{:7.2f} {:7.2f} {:7.2f} {:7.2f} {:4} {:4} {:6.3f} {:6.3f} {:6.3f} {:7.2f}  {:4}  {}  {:1}'
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
        cls = self.colorLists
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

def genColors(cp, nsteps=12):
    colors, clen = [], len(cp[0])
    diffs = [cp[1][i] - cp[0][i] for i in range(clen)]
    steps = [diffs[i]/nsteps   for i in range(clen)]
    print('genColors(), c1={} c2={} nsteps={} diffs={} steps={}'.format(cp[0], cp[1], nsteps, diffs, steps))
    for j in range(nsteps):
        c = tuple([fri(cp[0][i]+j*steps[i]) for i in range(len(cp[0]))])
        print('genColors() c[{}]={}'.format(j, c))
        colors.append(c)
    print('genColors() colors={}'.format(cp))
    return colors

if __name__ == '__main__':
    SFX        = 'TEST' if RUN_TEST else ''
    DBG_FILE   = open(sys.argv[0] + SFX + ".log.txt", 'w')
    P, L, R, C = 0, 1, 2, 3
    VIOLET     = [(255, 64, 192, 255), (64, 16, 16, 255)]
    RED        = [(255, 32, 32, 255), (64, 16, 16, 255)]
    ORANGE     = [(255, 128, 32, 255), (64, 16, 16, 255)]
    YELLOW     = [(255, 255, 64, 255), (64, 64, 16, 255)]
    GREEN      = [(32, 255, 32, 255), (16, 64, 16, 255)]
    GREEN_BLUE = [(32, 255, 208, 255), (16, 64, 32, 255)]
    CYAN       = [(32, 255, 255, 255), (16, 64, 64, 255)]
    BLUE_GREEN = [(32, 208, 255, 255), (16, 32, 64, 255)]
    BLUE       = [(32, 64, 255, 255), (16, 16, 64, 255)]
    PURPLE     = [(208, 96, 255, 255), (64, 16, 64, 255)]
    VIOLETS    = genColors(VIOLET)
    REDS       = genColors(RED)
    ORANGES    = genColors(ORANGE)
    YELLOWS    = genColors(YELLOW)
    GREENS     = genColors(GREEN)
    GREEN_BLUES = genColors(GREEN_BLUE)
    CYANS      = genColors(CYAN)
    BLUE_GREENS = genColors(BLUE_GREEN)
    BLUES      = genColors(BLUE)
    PURPLES    = genColors(PURPLE)
    COLOR      = (VIOLETS, REDS, ORANGES, YELLOWS, GREENS, GREEN_BLUES, BLUE_GREENS, BLUES, PURPLES)
    tabs       = Tabs()
    pyglet.app.run()
