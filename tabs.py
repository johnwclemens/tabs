import math, sys, os
import pyglet
import pyglet.window.key as pygwink
sys.path.insert(0, os.path.abspath('../lib'))
import cmdArgs

def fri(f): return int(math.floor(f+0.5))

class Tabs(pyglet.window.Window):
    def __init__(self):
        self.ww, self.hh  = [1000]*2, [600]*2
        self.n            = [9, 8, 6, 8]
        self.x            = [10, 10, 4, 4]
        self.y            = [10, 10, 3, 3]
        self.fullScreen   = False
        self.subpixel     = True
        self.argMap       = cmdArgs.parseCmdLine(dbg=1)
        print('Tabs.init() argMap={}'.format(self.argMap), file=DBG_FILE)
        if 'w' in self.argMap and len(self.argMap['w'])  > 0: self.w            = [int(self.argMap['w'][i]) for i in range(len(self.argMap['w']))]
        if 'h' in self.argMap and len(self.argMap['h'])  > 0: self.h            = [int(self.argMap['h'][i]) for i in range(len(self.argMap['h']))]
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
        self.testColorLists = True
        print('_init() testColorLists={} useOrderedGroup={}'.format(self.testColorLists, self.useOrderedGroup), file=DBG_FILE)
        if self.testColorLists: self._initColorLists()
        else: self._initTabs()

    def _initWindowA(self):
        display      = pyglet.canvas.get_display()
        self.screens = display.get_screens()

    def _initWindowB(self):
        self.batch = pyglet.graphics.Batch()
        self.set_size(self.ww[1], self.hh[1])
        self.set_visible()
        print('_initWindow() ww={} hh={}'.format(self.ww, self.hh), file=DBG_FILE)

    def dumpGeom(self, reason):
        print('{:32} ww={} hh={} n={} w={} h={} x={} y={}'.format(reason, self.ww, self.hh, self.n, self.w, self.h, self.x, self.y), file=DBG_FILE)

    def resizeGeomA(self):
        self.w = [(self.ww[1]-                      2*self.x[i]) for i in range(len(self.n))]
        self.h = [(self.hh[1]-                      2*self.y[i]) for i in range(len(self.n))]
        return self.ww, self.hh, self.n, self.w, self.h, self.x, self.y

    def resizeGeomB(self):
        self.w = [(self.ww[1]-                      2*self.x[i]) for i in range(len(self.n))]
        self.h = [(self.hh[1]-(self.n[i]+1)*self.y[i])/self.n[i] for i in range(len(self.n))]
        return self.ww, self.hh, self.n, self.w, self.h, self.x, self.y

    def resizeGeomC(self):
        self.w = [(self.ww[1]-(self.n[i]+1)*self.x[i])/self.n[i] for i in range(len(self.n))]
        self.h = [(self.hh[1]-(self.n[i]+1)*self.y[i])/self.n[i] for i in range(len(self.n))]
        return self.ww, self.hh, self.n, self.w, self.h, self.x, self.y

    def _initColorLists(self):
        self.clGroup = self._initGroup(0)
        ww, hh, n, w, h, x, y = self.resizeGeomC()
        self.w_, self.h_ = w, h
        c = COLOR[:n[0]]
        self.dumpGeom('_initColorLists(dumpGeom)')
        end = ['\n', ' ']
        [[print('{:2} {:2} {:3} {:3} {:3} {:3}'.format(i, j, c[i][j][0], c[i][j][1], c[i][j][2], c[i][j][3]), file=DBG_FILE, end=end[0 if j==n[1]-1 else 1]) for j in range(n[1])] for i in range(n[0])]
        print(file=DBG_FILE)
        self.dumpSprite(None)
        self.colorListSprites = []
        for i in range(n[0]):
            sprites = []
            for j in range(n[1]):
                xx, yy = x[1]+(w[0]+x[1])*i, hh[1]-(h[1]+y[1])*(j+1)
                scip = pyglet.image.SolidColorImagePattern(c[i][j])
                sci = scip.create_image(width=fri(w[0]), height=fri(h[1]))
                spr = self.createSprite('_initColorLists()', sci, self.clGroup, xx, yy, w[0], h[1], i, j, v=True, no=0) #n[0], o=255)
                sprites.append(spr)
            self.colorListSprites.append(sprites)

    def resizeColorLists(self):
        cls = self.colorListSprites
#        ni, nj = len(cls), len(cls[0])
        ww, hh, n, w, h, x, y = self.resizeGeomC()
        w_, h_ = self.w_, self.h_
        print('resizeColorLists(BGN) ww={} hh={}'.format(ww, hh), file=DBG_FILE)
        self.dumpSprite(None)
        for i in range(n[0]):
            for j in range(n[1]):
                xx, yy = x[1]+(w[0]+x[1])*i, hh[1]-(h[1]+y[1])*(j+1)
                cls[i][j].update(x=xx, y=yy, scale_x=w[0]/w_[0], scale_y=h[0]/h_[0])
                self.dumpSprite('{:20} {:3} {:3} {:8.2f} {:8.2f} {:8.2f} {:8.2f}'.format('resizeColorLists()', i, j, xx, yy, w[0], h[1]), cls[i][j])

    def createSprite(self, reason, img, grp, x, y, w, h, i, j, v=None, no=0, o=255):
#        img.anchor_x, img.anchor_y = fri(w/2), fri(h/2)
        s = pyglet.sprite.Sprite(img, x, y, batch=self.batch, group=grp, subpixel=self.subpixel)
        s.visible = v if v is not None else True if i==0 else False
        s.opacity = self.getOpacity(o, j, no)
#        if c==0 or r==0 or c==self.nc-1 or r==self.nr-1:
        self.dumpSprite('{:20} {:3} {:3} {:8.2f} {:8.2f} {:8.2f} {:8.2f} {:4} {:4}'.format(reason, i, j, x, y, w, h, img.anchor_x, img.anchor_y), s)
        return s

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
        self.pageColors  = [BLUES[i] for i in range(len(BLUES))]
        self.pageGroup   = self._initGroup(0)
        i = P
        ww, hh, n, w, h, x, y = self.resizeGeomA()
        self.w_, self.h_ = self.w, self.h
        self.w_[i], self.h_[i] = w[i], h[i]
        for p in range(n[i]):
            self.dumpGeom('_initPages')
            self.dumpSprite(None)
            scip   = pyglet.image.SolidColorImagePattern(self.pageColors[p%n[i]])
            img    = scip.create_image(width=fri(w[i]), height=fri(h[i]))
            page   = self.createSprite('_initPages', img, self.pageGroup, x[i], y[i], w[i], h[i], p, 0)
            self.pages.append(page)
            lines  = self._initLines()
#            self.pages.append(lines)
        return self.pages

    def _initLines(self):
        self.lineColors  = [REDS[i] for i in range(len(REDS))]
        self.lineGroup   = self._initGroup(1)
        i = L
        ww, hh, n, w, h, x, y = self.resizeGeomB()
        self.w_[i], self.h_[i] = w[i], h[i]
        self.dumpGeom('_initLines')
        self.dumpSprite(None)
        lines = []
        for l in range(n[i]):
            yy = hh[i]-(h[i]+y[i])*(l+1)
            scip   = pyglet.image.SolidColorImagePattern(self.lineColors[l%n[i]])
            img    = scip.create_image(width=fri(w[i]), height=fri(h[i]))
            line   = self.createSprite('_initLines', img, self.lineGroup, x[i], yy, w[i], h[i], l, 0, v=True if len(self.pages)==1 else False)
            self.lines.append(line)
##            rows   = self._initRows(x, y, w, h, p, l)
#            lines.append(rows)
#        self.lines.append(lines)
        return lines

    def on_resize(self, width, height):
        super().on_resize(width, height)
        self.ww[1], self.hh[1] = width, height
        if self.testColorLists: return self.resizeColorLists()
        w_, h_ = self.w_, self.h_
        ww, hh, n, w, h, x, y = self.resizeGeomA()
        mx, my = w[0]/w_[0], h[0]/h_[0]
        print('on_resize(BGN) ww={} hh={} mx={:6.3f} my={:6.3f} w={} h={}'.format(ww, hh, mx, my, w, h), file=DBG_FILE)
        self.dumpSprite(None)
        for p in range(n[0]):
            self.pages[p].update(x=self.pages[p].x*mx, y=self.pages[p].y*my, scale_x=mx, scale_y=my)
            self.dumpSprite('{:20} {:3} {:3} {:8.2f} {:8.2f} {:8.2f} {:8.2f}'.format('on_resize()', p, 0, x[0], y[0], w[0], h[0]), self.pages[p])
        mx, my = w[1]/w_[1], h[1]/h_[1]
        for l in range(n[1]):
            ww, hh, n, w, h, x, y = self.resizeGeomB()
            yy = hh[1]-(h[1]+y[1])*(l+1)
            self.lines[l].update(x=x[1], y=yy, scale_x=mx, scale_y=my)
            self.dumpSprite('{:20} {:3} {:3} {:8.2f} {:8.2f} {:8.2f} {:8.2f}'.format('on_resize()', l, 0, x[1], yy, w[1], h[1]), self.lines[l])
#        for r in range(n[2]):
#            self.rows[r].update(x=self.rows[r].x*mx, y=self.rows[r].y*my, scale_x=mx, scale_y=my)
#        for c in range(n[3]):
#            self.cols[c].update(x=self.cols[c].x*mx, y=self.cols[c].y*my, scale_x=mx, scale_y=my)

    def _initRows(self, xx, yy, ww, hh, p=-1, l=-1, ii=4, jj=4):
        if self.useOrderedGroup: self.rowGroup = pyglet.graphics.OrderedGroup(2)
        else:                    self.rowGroup = pyglet.graphics.Group(self.lineGroup)
        self.rowColors = [VIOLETS[i] for i in range(len(VIOLETS))]
        rpl, c = self.rowsPerLine, 0
        w, h = ww-2*ii, (hh-(rpl+1)*jj)/rpl
        rows = []
        for r in range(rpl):
            x, y = xx+ii, yy+jj*(r+1)+r*h
            scip = pyglet.image.SolidColorImagePattern(self.rowColors[r%rpl])
            sci = scip.create_image(width=fri(w), height=fri(h))
            row = pyglet.sprite.Sprite(img=sci, x=x, y=y, batch=self.batch, group=self.rowGroup, subpixel=self.subpixel)
            self.rows.append(row)
            if p!=self.vpn:    row.visible = False
            cols = self._initCols(x, y, w, h, p, l, r)
#            rows.append(cols)
#        self.rows.append(rows)
        return rows
#        lines.append(rows)

    def _initCols(self, xx, yy, ww, hh, p=-1, l=-1, r=-1, ii=2, jj=2):
        if self.useOrderedGroup: self.colGroup = pyglet.graphics.OrderedGroup(3)
        else:                    self.colGroup = pyglet.graphics.Group(self.rowGroup)
        self.colColors = [ORANGES[i] for i in range(len(ORANGES))]
        lpp, rpl, cpr = self.linesPerPage, self.rowsPerLine, self.colsPerRow
        w, h = (ww-2*ii)/cpr, hh-2*jj
        cols = []
        for c in range(self.colsPerRow):
            x, y = xx+ii+c*w, yy+jj
            scip = pyglet.image.SolidColorImagePattern(self.colColors[c%8])
            sci = scip.create_image(width=fri(w), height=fri(h))
            col = pyglet.sprite.Sprite(img=sci, x=x, y=y, batch=self.batch, group=self.colGroup, subpixel=self.subpixel)
            self.cols.append(col)
            if p!=self.vpn:     col.visible = False
#        self.cols.append(cols)
        return cols
#        rows.append(cols)

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
        if not self.testColorLists:
            print('toggleColorLists() motion={} testColorLists={}'.format(motion, self.testColorLists), file=DBG_FILE)
            return
        cls = self.colorListSprites
        if   motion==pygwink.MOTION_LEFT:
            for j in range(len(cls[self.tci])): cls[self.tci][j].visible = False
            self.tci -= 1
            self.tci = self.tci % len(colorLists)
            for j in range(len(cls[self.tci])): cls[self.tci][j].visible = True
            print('toggleColorLists() MOTION_LEFT={} tci={} len(cls)={}'.format(motion, self.tci, len(cls)), file=DBG_FILE)
        elif motion==pygwink.MOTION_RIGHT:
            for j in range(len(cls[self.tci])): cls[self.tci][j].visible = False
            self.tci += 1
            self.tci = self.tci % len(colorLists)
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
    DBG_FILE = open(sys.argv[0] + ".log.txt", 'w')
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
    COLOR = (VIOLETS, REDS, ORANGES, YELLOWS, GREENS, CYANS, BLUES, PURPLES, FOOS)
    tabs = Tabs()
    pyglet.app.run()
