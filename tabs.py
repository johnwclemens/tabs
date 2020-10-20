import math, sys, os
import pyglet
#import pyglet.window     as pygwin
#import pyglet.text       as pygtxt
import pyglet.window.key as pygwink
sys.path.insert(0, os.path.abspath('C:/Python36/my/lib'))
import cmdArgs

def fri(f): return int(math.floor(f+0.5))

class Tabs(pyglet.window.Window):
    def __init__(self):
        self._ww, self._wh = 1000, 600
        self.ww, self.wh = self._ww, self._wh
        self.nPages          = 1
        self.linesPerPage    = 3
        self.rowsPerLine     = 6
        self.colsPerRow      = 1
        self.m               = 12
        self.n               = 12
        self.fullScreen      = False
        self.subpixel        = False
        self.argMap          = cmdArgs.parseCmdLine(dbg=1)
        print('Tabs.init() argMap={}'.format(self.argMap), file=DBG_FILE)
        if 'p' in self.argMap and len(self.argMap['p'])  > 0: self.nPages       = int(self.argMap['p'][0])
        if 'l' in self.argMap and len(self.argMap['l'])  > 0: self.linesPerPage = int(self.argMap['l'][0])
        if 'r' in self.argMap and len(self.argMap['r'])  > 0: self.rowsPerLine  = int(self.argMap['r'][0])
        if 'c' in self.argMap and len(self.argMap['c'])  > 0: self.colsPerRow   = int(self.argMap['c'][0])
        if 'w' in self.argMap and len(self.argMap['w'])  > 0: self.ww           = int(self.argMap['w'][0])
        if 'h' in self.argMap and len(self.argMap['h'])  > 0: self.wh           = int(self.argMap['h'][0])
        if 'm' in self.argMap and len(self.argMap['m'])  > 0: self.m            = int(self.argMap['m'][0])
        if 'n' in self.argMap and len(self.argMap['n'])  > 0: self.n            = int(self.argMap['n'][0])
        if 'F' in self.argMap and len(self.argMap['F']) == 0: self.fullScreen   = True
        if 'f' in self.argMap and len(self.argMap['f']) == 0: self.subpixel     = True
        print('[p]         nPages={}'.format(self.nPages),       file=DBG_FILE)
        print('[l]   linesPerPage={}'.format(self.linesPerPage), file=DBG_FILE)
        print('[r]    rowsPerLine={}'.format(self.rowsPerLine),  file=DBG_FILE)
        print('[c]     colsPerRow={}'.format(self.colsPerRow),   file=DBG_FILE)
        print('[w]             ww={}'.format(self.ww),           file=DBG_FILE)
        print('[h]             wh={}'.format(self.wh),           file=DBG_FILE)
        print('[m]              m={}'.format(self.m),            file=DBG_FILE)
        print('[n]              n={}'.format(self.n),            file=DBG_FILE)
        print('[F]     fullScreen={}'.format(self.fullScreen),   file=DBG_FILE)
        print('[f]       subpixel={}'.format(self.subpixel),     file=DBG_FILE)
        self._initWindowA()
        super().__init__(screen=self.screens[1], fullscreen=self.fullScreen, resizable=True, visible=False)
        self._initWindowB()
        self.testColorLists = False
        if self.testColorLists: self._initColorLists()
        self._initTabs()

    def _initWindowA(self):
        display      = pyglet.canvas.get_display()
        self.screens = display.get_screens()

    def _initWindowB(self):
        self.batch = pyglet.graphics.Batch()
        self.group = [pyglet.graphics.Group(g) for g in range(4)]
        self.set_size(self.ww, self.wh)
        self.set_visible()
        print('_initWindow() ww={} wh={}'.format(self.ww, self.wh), file=DBG_FILE)

    def _initTabs(self):
        print('_initTabs(BGN) nPages={} linesPerPage={} rowsPerLine={} colsPerRow={}'.format(self.nPages, self.linesPerPage, self.rowsPerLine, self.colsPerRow), file=DBG_FILE)
        self.pages, self.lines, self.rows, self.cols = [], [], [], []
        self.cpn = 0
        self.tci = 0
#        self.tabsGroup = pyglet.graphics.Group()
        self._initPages(0, 0, self.ww, self.wh)
        print('_initTabs(END) nPages={} linesPerPage={} rowsPerLine={} colsPerRow={}'.format(self.nPages, self.linesPerPage, self.rowsPerLine, self.colsPerRow), file=DBG_FILE)

    def _initPages(self, xx, yy, ww, hh, ii=6, jj=6):
#        self.pageGroup  = pyglet.graphics.Group(self.tabsGroup)
        self.pageGroup  = pyglet.graphics.OrderedGroup(0)
        self.pageColors = [BLUES[0], PURPLES[0], CYANS[0], VIOLETS[0]]
        w, h = ww, hh
        for p in range(self.nPages):
            x, y = xx, yy
            scip = pyglet.image.SolidColorImagePattern(self.pageColors[p])
            sci  = scip.create_image(width=fri(w), height=fri(h))
            page = pyglet.sprite.Sprite(img=sci, x=x, y=y, batch=self.batch, group=self.pageGroup, subpixel=self.subpixel)
            self.pages.append(page)
            if p  != self.cpn:     page.visible = False
            w, h   = page.width,   page.height
            xm, ym = page.scale_x, page.scale_y
            print('_initPages() {:2}            x={:6.1f} y={:6.1f} w={:4} h={:4} xm={:5.3f} ym={:5.3f} ww={:4} hh={:4} ii={} jj={} v={} c={}'.format(p, x, y, w, h, xm, ym, ww, hh, ii, jj, page.visible, self.pageColors[p]), file=DBG_FILE)
            lines = self._initLines(x, y, w, h, p)
        self.pages.append(lines)

    def _initLines(self, xx, yy, ww, hh, p, ii=4, jj=4):
#        self.lineGroup = pyglet.graphics.Group(self.pageGroup)
        self.lineGroup = pyglet.graphics.OrderedGroup(1)
        self.lineColors = [GREENS[i] for i in range(len(GREENS))] # if i%2]
        lpp = self.linesPerPage
        w, h = ww-2*ii, (hh-(lpp+1)*jj)/lpp
        lines = []
        for l in range(lpp):
            x, y = xx+ii, yy+jj*(l+1)+l*h
            scip = pyglet.image.SolidColorImagePattern(self.lineColors[l])
            sci = scip.create_image(width=fri(w), height=fri(h))
            line = pyglet.sprite.Sprite(img=sci, x=x, y=y, batch=self.batch, group=self.lineGroup, subpixel=self.subpixel)
            self.lines.append(line)
            if p != self.cpn:      line.visible = False
            w, h = line.width,   line.height
            xm, ym = line.scale_x, line.scale_y
            print('_initLines() {:2} {:2}         x={:6.1f} y={:6.1f} w={:4} h={:4} xm={:5.3f} ym={:5.3f} ww={:4} hh={:4} ii={} jj={} v={} c={}'.format(p, l, x, y, w, h, xm, ym, ww, hh, ii, jj, line.visible, self.lineColors[l]), file=DBG_FILE)
            rows = self._initRows(x, y, w, h, p, l)
            lines.append(rows)
        self.lines.append(lines)
        return lines

    def _initRows(self, xx, yy, ww, hh, p, l, ii=2, jj=2):
#        return []
#        self.rowGroup = pyglet.graphics.Group(self.lineGroup)
        self.rowGroup = pyglet.graphics.OrderedGroup(2)
        self.rowColors = [REDS[i] for i in range(len(REDS))]
        lpp, rpl = self.linesPerPage, self.rowsPerLine
        w, h = ww-2*ii, (hh-(rpl+1)*jj)/rpl
        rows = []
        for r in range(rpl):
            x, y = xx+ii, yy+jj*(r+1)+r*h
            scip = pyglet.image.SolidColorImagePattern(self.rowColors[r%rpl])
            sci = scip.create_image(width=fri(w), height=fri(h))
            row = pyglet.sprite.Sprite(img=sci, x=x, y=y, batch=self.batch, group=self.rowGroup, subpixel=self.subpixel)
            self.rows.append(row)
            if p != self.cpn:   row.visible = False
            w, h = row.width, row.height
            xm, ym = row.scale_x, row.scale_y
            print('_initRows()  {:2} {:2} {:2}      x={:6.1f} y={:6.1f} w={:4} h={:4} xm={:5.3f} ym={:5.3f} ww={:4} hh={:4} ii={} jj={} v={} c={}'.format(p, l, r, x, y, w, h, xm, ym, ww, hh, ii, jj, row.visible, row.color), file=DBG_FILE)
            cols = self._initCols(x, y, w, h, p, l, r)
            rows.append(cols)
        self.rows.append(rows)
        return rows
#        lines.append(rows)

    def _initCols(self, xx, yy, ww, hh, p, l, r, ii=2, jj=2):
        return []
#        self.colGroup = pyglet.graphics.Group(self.rowGroup)
        self.colGroup = pyglet.graphics.OrderedGroup(3)
        self.colColors = [ORANGES[i] for i in range(len(ORANGES))]
        lpp, rpl, cpr = self.linesPerPage, self.rowsPerLine, self.colsPerRow
        w, h = (ww-self.m)/cpr, (wh/lpp - self.n)/rpl
#        w, h = ww/cpr, wh/(rpl*lpp)
        cols = []
        for c in range(self.colsPerRow):
            x, y = 3*self.m+c*w, 3*self.n+wh-h-l*wh/lpp-r*h
            scip = pyglet.image.SolidColorImagePattern(self.colColors[c%8])
            sci  = scip.create_image(width=fri(w), height=fri(h))
            col  = pyglet.sprite.Sprite(img=sci, x=x, y=y, batch=self.batch, group=self.colGroup, subpixel=self.subpixel)
            if p != self.cpn:     col.visible = False
            sw, sh = col.width,   col.height
            xp, yq = col.scale_x, col.scale_y
            cols.append(col)
            if r==0: print('_initCols() {:2} {:2} {:2} {:3} x={:6.1f} y={:6.1f} sw={:4} sh={:4} xp={:5.3f} yq={:5.3f} ww={:4} wh={:4} v={} c={}'.format(p, l, r, c, x, y, sw, sh, xp, yq, ww, wh, col.visible, col.color), file=DBG_FILE)
        self.cols.append(cols)
        return cols
#        rows.append(cols)

    def printStructInfo(self, reason=''):
        print('{} np={} lpp={} rpl={} cpr={} len(pages)={} len(lines)={} len(rows)={} len(cols)={}'
              .format(reason, self.nPages, self.linesPerPage, self.rowsPerLine, self.colsPerRow, len(self.pages), len(self.lines), len(self.rows), len(self.cols)), file=DBG_FILE)

    def printStruct(self, np, lpp, rpl, cpr):
        self.printStructInfo('printStruct(BGN)')
        print('printStruct() np={} lpp={} rpl={} cpr={}'.format(np, lpp, rpl, cpr), file=DBG_FILE)
        for p in range(np):
            for m in range(lpp):
                for r in range(rpl):
                    for c in range(cpr):
                        q = self.pages[p][m][r][c]
                        print('pages: p={} m={} r={} c={} position=({:5.1f}, {:5.1f}) w={:5.1f} h={:5.1f}'.format(p, m, r, c, q.x, q.y, q.width, q.height), file=DBG_FILE)
        print('printStruct() len(pages)={} lpp={} rpl={} cpr={}'.format(len(self.pages), lpp, rpl, cpr), file=DBG_FILE)
        for p in range(len(self.pages)):
            for m in range(lpp):
                for r in range(rpl):
                    for c in range(cpr):
                        q = self.pages[p][m][r][c]
                        print('pages: p={} m={} r={} c={} position=({:5.1f}, {:5.1f}) w={:5.1f} h={:5.1f}'.format(p, m, r, c, q.x, q.y, q.width, q.height), file=DBG_FILE)
        print('printStruct() len(lines)={} rpl={} cpr={}'.format(len(self.lines), rpl, cpr), file=DBG_FILE)
        for m in range(len(self.lines)):
            for r in range(rpl):
                for c in range(cpr):
                    q = self.lines[m][r][c][0]
                    print('lines: m={} r={} c={} position=({:5.1f}, {:5.1f}) w={:5.1f} h={:5.1f}'.format(m, r, c, q.x, q.y, q.width, q.height), file=DBG_FILE)
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
        self.printStruct(1, 1, 1, 1)
        self.printStruct(self.nPages, 1, 1, 1)
        self.printStruct(self.nPages, self.linesPerPage, 1, 1)
        self.printStruct(self.nPages, self.linesPerPage, self.rowsPerLine, 1)
        self.printStruct(self.nPages, self.linesPerPage, self.rowsPerLine, self.colsPerRow)
        struct = (self.pages, self.lines, self.rows, self.cols)
        ln = [len(e) for e in struct]
        sz = [self.size(e) for e in struct]
        d1 = dict(zip(['pages', 'lines', 'rows', 'cols'], ln))
        d2 = dict(zip(['pages', 'lines', 'rows', 'cols'], sz))
        print('_verify() d1={} d2={}'.format(d1, d2), file=DBG_FILE)
        assert(d1['pages'] == self.nPages)
        assert(d1['lines'] == self.nPages * self.linesPerPage)
        assert(d1['rows']  == self.nPages * self.linesPerPage * self.rowsPerLine)
        assert(d1['cols']  == self.nPages * self.linesPerPage * self.rowsPerLine * self.colsPerRow)
        assert(d2['pages'] == self.nPages * self.linesPerPage * self.rowsPerLine * self.colsPerRow)
        assert(d2['lines'] == self.nPages * self.linesPerPage * self.rowsPerLine * self.colsPerRow)
        assert(d2['rows']  == self.nPages * self.linesPerPage * self.rowsPerLine * self.colsPerRow)
        assert(d2['cols']  == self.nPages * self.linesPerPage * self.rowsPerLine * self.colsPerRow)

    def size(self, item):
        if isinstance(item, list): return sum([self.size(i) for i in item])
        return 1

    def on_draw(self):
        self.clear()
        self.batch.draw()

    def on_text(self, text):
        print('on_text() text={}'.format(text), file=DBG_FILE)

    def on_text_motion(self, motion):
        if   motion == pygwink.MOTION_RIGHT:         self.toggleColorLists(motion)
        elif motion == pygwink.MOTION_LEFT:          self.toggleColorLists(motion)
        elif motion == pygwink.MOTION_NEXT_PAGE:     self.setCurrPage(motion)
        elif motion == pygwink.MOTION_PREVIOUS_PAGE: self.setCurrPage(motion)
        else:                                        print('on_text_motion() motion={} ???'.format(motion), file=DBG_FILE)

    def on_resize(self, width, height):
        super().on_resize(width, height)
        return
        self.ww, self.wh  = width, height
        if self.testColorLists: self.resizeColorLists()
        ww, wh = self.ww, self.wh
        print('on_resize(BGN) ww={} wh={}'.format(ww, wh), file=DBG_FILE)
        w, h = ww/self.colsPerRow, wh/(self.rowsPerLine*self.linesPerPage)
        lpp = self.linesPerPage
        for p in range(self.nPages):
            for m in range(self.linesPerPage):
                for r in range(self.rowsPerLine):
                    if type(self.pages[p][m][r]) == pyglet.sprite.Sprite:
                        self.pages[p][m][r].update(x=x, y=y, scale_x=ww/self._ww, scale_y=wh/self._wh)
                    else:
                        for c in range(self.colsPerRow):
                            x, y = c*w, wh-h-m*wh/lpp-r*h
                            self.pages[p][m][r][c].update(x=x, y=y, scale_x=ww/self._ww, scale_y=wh/self._wh)
                            sw, sh = self.pages[p][m][r][c].width, self.pages[p][m][r][c].height
                            xp, yq = self.pages[p][m][r][c].scale_x, self.pages[p][m][r][c].scale_y
                            if r==0: print('on_resize() [{:2}] [{:2}] [{:2}] [{:3}] x={:6.1f} y={:6.1f} sw={:4} sh={:3} xp={:5.3f} yq={:5.3f} ww={} wh={}'.format(p, m, r, c, x, y, sw, sh, xp, yq, ww, wh), file=DBG_FILE)

    def resizeColorLists(self):
        cls = self.colorListSprites
        ncls = len(cls)
        ww, wh = self.ww, self.wh
        print('resizeColorLists(BGN) ww={} wh={}'.format(ww, wh), file=DBG_FILE)
        for i in range(ncls):
            for j in range(len(cls[i])):
                nj = len(cls[i])
                w, h = ww/ncls, wh/nj
                x, y = i*w, wh-h-j*wh/nj
                cls[i][j].update(x=x, y=y, scale_x=ww/self._ww, scale_y=wh/self._wh)

    def _initColorLists(self):
        self.colorListSprites = []
        cl = colorLists
        ncl = len(cl)
        for i in range(ncl):
            sprites = []
            for j in range(len(cl[i])):
                nj = len(cl[i])
                w, h, ww, wh = self.ww/ncl, self.wh/nj, self.ww, self.wh
                x, y = i*w, wh-h-j*wh/nj
                scip = pyglet.image.SolidColorImagePattern(cl[i][j])
                sci = scip.create_image(width=fri(w), height=fri(h))
                spr = pyglet.sprite.Sprite(img=sci, x=x, y=y, batch=self.batch)
#                if i == 0: spr.visible = True
#                else:      spr.visible = False
                sprites.append(spr)
                sw, sh = spr.width,   spr.height
                xp, yq = spr.scale_x, spr.scale_y
                print('_initColorLists [{:2}] [{:2}] x={:6.1f} y={:6.1f} sw={:4} sh={:3} xp={:5.3f} yq={:5.3f} ww={} wh={} visible={} cl={}'.format(i, j, x, y, sw, sh, xp, yq, ww, wh, spr.visible, cl[i][j]), file=DBG_FILE)
            self.colorListSprites.append(sprites)

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
            self.pages[self.cpn].visible = False
            self.cpn += 1
            self.cpn = self.cpn % self.nPages
            self.pages[self.cpn].visible = True
            print('setCurrPage() motion={} MOTION_NEXT_PAGE cpn={}'.format(motion, self.cpn), file=DBG_FILE)
        elif motion==pygwink.MOTION_PREVIOUS_PAGE:
            self.pages[self.cpn].visible = False
            self.cpn -= 1
            self.cpn = self.cpn % self.nPages
            self.pages[self.cpn].visible = True
            print('setCurrPage() motion={} MOTION_PREVIOUS_PAGE cpn={}'.format(motion, self.cpn), file=DBG_FILE)

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
    FOO      = [(255, 32, 64, 255), (64, 64, 32, 255)]
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
    tabs = Tabs()
    pyglet.app.run()
