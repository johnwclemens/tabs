import math, sys, os
import pyglet
#import pyglet.window     as pygwin
#import pyglet.text       as pygtxt
import pyglet.window.key as pygwink
sys.path.insert(0, os.path.abspath('../lib'))
import cmdArgs

def fri(f): return int(math.floor(f+0.5))

class Tabs(pyglet.window.Window):
    def __init__(self):
        self.ww, self.hh  = [1000]*2, [600]*2
        self.n            = [8, 8, 6, 8]
        self.x            = [0, 4, 3, 4]
        self.y            = [0, 3, 3, 4]
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
        self.testColorLists = False
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

    def resizeGeom(self):
        self.w = [(self.ww[1]-(self.n[i]+1)*self.x[i])/self.n[i] for i in range(len(self.n))]
        self.h = [(self.hh[1]-(self.n[i]+1)*self.y[i])/self.n[i] for i in range(len(self.n))]
#        ww, hh, n, w, h, x, y = self.getGeom()
#        self.w = [(ww[1]-(n[i]+1)*x[i])/n[i] for i in range(len(n))]
#        self.h = [(hh[1]-(n[i]+1)*y[i])/n[i] for i in range(len(n))]
        return self.ww, self.hh, self.n, self.w, self.h, self.x, self.y

    def getGeom(self):
        return self.ww, self.hh, self.n, self.w, self.h, self.x, self.y

    def dumpGeom(self, reason):
        print('{:32} ww={} hh={} n={} w={} h={} x={} y={}'.format(reason, self.ww, self.hh, self.n, self.w, self.h, self.x, self.y), file=DBG_FILE)

    def _initColorLists(self):
        self.clGroup = self._initGroup(0)
        ww, hh, n, w, h, x, y = self.resizeGeom()
        self.dumpGeom('_initColorLists(dumpGeom)')
        cl = colorLists
        ncl = n[0] #len(cl)
        end = ['\n', ' ']
        [[print('{:2} {:2} {:3} {:3} {:3} {:3}'.format(i, j, cl[i][j][0], cl[i][j][1], cl[i][j][2], cl[i][j][3]), file=DBG_FILE, end=end[0 if j==len(cl[i])-1 else 1]) for j in range(len(cl[i]))] for i in range(ncl)]
        print(file=DBG_FILE)
        self.dumpSprite(None)
        self.colorListSprites = []
        for i in range(ncl):
            nj = n[1] #len(cl[i])
            sprites = []
            for j in range(nj):
                xx, yy = x[1]+(w[1]+x[1])*i, hh[1]-(h[1]+y[1])*(j+1)
                scip = pyglet.image.SolidColorImagePattern(cl[i][j])
                sci = scip.create_image(width=fri(w[1]), height=fri(h[1]))
                spr = self.createSprite('_initColorLists()', sci, self.clGroup, xx, yy, w[1], h[1], i, j)
#                if i == 0: spr.visible = True
#                else:      spr.visible = False
                sprites.append(spr)
            self.colorListSprites.append(sprites)

    def resizeColorLists(self):
        cls = self.colorListSprites
        ncls = len(cls)
        ww, hh, n, w, h, x, y = self.getGeom()
        print('resizeColorLists(BGN) ww={} hh={}'.format(ww, hh), file=DBG_FILE)
        self.dumpSprite(None)
        for i in range(ncls):
            for j in range(len(cls[i])):
                nj = len(cls[i])
#                ww, hh = (W[0]-2*x[1])/ncls, (H[0]-2*y[1])/nj
#                xx, yy = x[1]+i*ww, y[1]+H[0]-hh-j*H[0]/nj
#                ww, hh = (W[1]-2*x[1])/ncls, (H[1]/H[0])*h[1]/nj
#                xx, yy = x[1]+i*ww, H[1]-(hh+y[1])*(j+1)
                xx, yy = x[1]+(w[1]+x[1])*i, hh[1]-(h[1]+y[1])*(j+1)
                cls[i][j].update(x=xx, y=yy, scale_x=ww[1]/ww[0], scale_y=hh[1]/hh[0])
                self.dumpSprite('{:20} {:3} {:3} {:8.2f} {:8.2f} {:8.2f} {:8.2f}'.format('resizeColorLists()', i, j, xx, yy, w[1], h[1]), cls[i][j])

    def createSprite(self, reason, img, grp, x, y, w, h, i, j):
#        img.anchor_x, img.anchor_y = fri(w/2), fri(h/2)
        s = pyglet.sprite.Sprite(img, x, y, batch=self.batch, group=grp, subpixel=self.subpixel)
#        s.opacity = self.getOpacity(255, i, ni)
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
        self._lines = []
#        if not self.useOrderedGroup: self.rootGroup = pyglet.graphics.Group()
        self._initPages()
#       self.printStruct('_initTabs()')
        print('_initTabs(END) nPages={} linesPerPage={} rowsPerLine={} colsPerRow={}'.format(self.n[0], self.n[1], self.n[2], self.n[3]), file=DBG_FILE)

    def _initPages(self):
        self.pageColors  = [BLUES[i] for i in range(len(BLUES))]
        self.pageGroup   = self._initGroup(0)
        ww, hh, n, w, h, x, y = self.resizeGeom()
#        self.dumpGeom('_initPages')
#        self.dumpSprite(None)
        for p in range(n[0]):
            ww, hh = w[0], h[0]
            xx, yy = x[0], y[0]
#            x, y = p*w, H[1]-h-j*H[1]/n[0]
            scip   = pyglet.image.SolidColorImagePattern(self.pageColors[p%n[0]])
            img    = scip.create_image(width=fri(ww), height=fri(hh))
#            page = self.createSprite('_initPages', img, self.pageGroup, xx, yy, ww, hh, p, n[0])
#            self.pages.append(page)
#            if p  != self.vpn:     page.visible = False
            lines  = self._initLines()
#            self.pages.append(lines)
        return self.pages


    def _initLines(self):
        self.lineColors  = [REDS[i] for i in range(len(REDS))]
        self.lineGroup   = self._initGroup(1)
        W, H, n, w, h, x, y = self.getGeom()
        self.dumpGeom('_initLines')
        self.dumpSprite(None)
        lines = []
        for l in range(n[1]):
#            x, y   = xx+ii, yy+jj*(l+1)+l*h
#            w, h = W[1]-2*self.x[1], (H[1]-(n[1]+1)*self.y[1])/n[1]
#            x, y = self.x[1], (l+1)*h[1]/n[1] # H[1]-h-(l+1)*H[1]/n[1]
#            w, h = self.w[1], self.h[1]/n[1]
#            x, y = self.x[1], H[1] - (l+1)*h - self.y[1] # H[1]-h-l*H[1]/n[1]
            ww, hh = w[1], h[1]/n[1]
            xx, yy = x[1], H[0] - (l+1)*hh - (l+1)*y[1]
            xx, yy = x[1], H[0] - (l+1)*(hh + y[1])
            scip   = pyglet.image.SolidColorImagePattern(self.lineColors[l%n[1]])
            img    = scip.create_image(width=fri(ww), height=fri(hh))
            line = self.createSprite('_initLines', img, self.lineGroup, xx, yy, ww, hh, l, 0)
            self.lines.append(line)
            if l  != self.vpn:     line.visible = False
##            rows   = self._initRows(x, y, w, h, p, l)
#            lines.append(rows)
#        self.lines.append(lines)
        return lines
#        if p == self.vpn:
#            for l in range(lpp):
#                self._lines.append(self.lines[l])

    def _initRows(self, xx, yy, ww, hh, p=-1, l=-1, ii=4, jj=4):
        if self.useOrderedGroup: self.rowGroup = pyglet.graphics.OrderedGroup(2)
        else:                    self.rowGroup = pyglet.graphics.Group(self.lineGroup)
        self.rowColors = [VIOLETS[i] for i in range(len(VIOLETS))]
        rpl, c = self.rowsPerLine, 0
        w, h = ww-2*ii, (hh-(rpl+1)*jj)/rpl
        rows = []
        for r in range(rpl):
            x, y   = xx+ii, yy+jj*(r+1)+r*h
            scip   = pyglet.image.SolidColorImagePattern(self.rowColors[r%rpl])
            sci    = scip.create_image(width=fri(w), height=fri(h))
            row    = pyglet.sprite.Sprite(img=sci, x=x, y=y, batch=self.batch, group=self.rowGroup, subpixel=self.subpixel)
            self.rows.append(row)
            if p  != self.vpn:    row.visible = False
            cols   = self._initCols(x, y, w, h, p, l, r)
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
            x, y   = xx+ii+c*w, yy+jj
            scip   = pyglet.image.SolidColorImagePattern(self.colColors[c%8])
            sci    = scip.create_image(width=fri(w), height=fri(h))
            col    = pyglet.sprite.Sprite(img=sci, x=x, y=y, batch=self.batch, group=self.colGroup, subpixel=self.subpixel)
            self.cols.append(col)
            if p  != self.vpn:     col.visible = False
#        self.cols.append(cols)
        return cols
#        rows.append(cols)

    def on_resize(self, width, height):
        super().on_resize(width, height)
        self.ww[1], self.hh[1] = width, height
        ww, hh, n, w, h, x, y = self.resizeGeom()
#        if self.testColorLists: self.resizeColorLists()
        return
#        ppf, lpp, rpl, cpr = self.pagesPerFile, self.linesPerPage, self.rowsPerLine, self.colsPerRow
#        np, nl, nr, nc = len(self.pages), len(self.lines), len(self.rows), len(self.cols)
        mx, my = ww[1]/ww[0], hh[1]/hh[0]
        lpp = n[1]
        print('on_resize(BGN) ww={} hh={} mx={:5.2f} my={:5.2f} w={} h={}'.format(ww, hh, mx, my, w, h), file=DBG_FILE)
        for p in range(n[0]):
            self.pages[p].update(x=self.pages[p].x*mx, y=self.pages[p].y*my, scale_x=mx, scale_y=my)
        for l in range(n[1]):
            ii, jj = 6, 6
            w, h = ww-2*ii, (hh-(lpp+1)*jj)/lpp
#            self.lines[l].update(x=ii, y=jj*(l+1)+(l%lpp)*h, scale_x=mx, scale_y=my)
#            self.lines[l].update(x=self.lines[l].x*mx, y=self.lines[l].y*my, scale_x=mx, scale_y=my)
            self.lines[l].update(scale_x=mx, scale_y=my)
        print('on_resize() yspan = {} * ({:1.1f} + {:1.1f}) + {:1.1f} = ({} * {:1.1f}) + ({} * {:1.1f}) = {:1.1f} + {:1.1f} = {:5.1f}'.
              format(lpp, self.lines[0].y, self.lines[0].height, self.lines[0].y, lpp, self.lines[0].height, lpp + 1, self.lines[0].y, lpp * self.lines[0].height, (lpp+1) * self.lines[0].y, self.lines[0].y + lpp*(self.lines[0].y + self.lines[0].height)), file=DBG_FILE)
        for r in range(n[2]):
            self.rows[r].update(x=self.rows[r].x*mx, y=self.rows[r].y*my, scale_x=mx, scale_y=my)
        for c in range(n[3]):
            self.cols[c].update(x=self.cols[c].x*mx, y=self.cols[c].y*my, scale_x=mx, scale_y=my)

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
    VIOLET   = [(255, 64, 192, 255), (64, 16, 16, 255)]
    RED      = [(255, 32, 32, 255), (64, 16, 16, 255)]
    ORANGE   = [(255, 128, 32, 255), (64, 16, 16, 255)]
    YELLOW   = [(255, 255, 64, 255), (64, 64, 16, 255)]
    GREEN    = [(64, 255, 32, 255), (16, 64, 16, 255)]
    CYAN     = [(32, 255, 255, 255), (16, 64, 64, 255)]
    BLUE     = [(32, 64, 255, 255), (16, 16, 64, 255)]
    PURPLE   = [(208, 96, 255, 255), (64, 16, 64, 255)]
    FOO      = [(255, 192, 64, 255), (64, 64, 32, 255)]
    REDS     = genColors(RED)
    GREENS   = genColors(GREEN)
    BLUES    = genColors(BLUE)
    YELLOWS  = genColors(YELLOW)
    CYANS    = genColors(CYAN)
    VIOLETS  = genColors(VIOLET)
    ORANGES  = genColors(ORANGE)
    PURPLES  = genColors(PURPLE)
    FOOS     = genColors(FOO)
    colorLists = (VIOLETS, REDS, ORANGES, YELLOWS, GREENS, CYANS, BLUES, PURPLES)
#    colorLists = (ORANGES,)
    tabs = Tabs()
    pyglet.app.run()
