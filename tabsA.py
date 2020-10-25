import math, sys, os
import pyglet
#import pyglet.window     as pygwin
#import pyglet.text       as pygtxt
#import pyglet.window.key as pygwink
sys.path.insert(0, os.path.abspath('C:/Python36/my/lib'))
import cmdArgs

def fri(f): return int(math.floor(f+0.5))

class Tabs(pyglet.window.Window):
    def __init__(self):
        self._ww, self._wh = 1000, 600
        self.ww, self.wh = self._ww, self._wh
        self.nPages          = 3
        self.linesPerPage    = 4
        self.rowsPerLine     = 6
        self.colsPerRow      = 20
        self.fullScreen      = False
        self.argMap          = cmdArgs.parseCmdLine(dbg=1)
        print('Tabs.init() argMap={}'.format(self.argMap), file=DBG_FILE)
        if 'p' in self.argMap and len(self.argMap['p'])  > 0: self.nPages       = int(self.argMap['p'][0])
        if 'l' in self.argMap and len(self.argMap['l'])  > 0: self.linesPerPage = int(self.argMap['l'][0])
        if 'r' in self.argMap and len(self.argMap['r'])  > 0: self.rowsPerLine  = int(self.argMap['r'][0])
        if 'c' in self.argMap and len(self.argMap['c'])  > 0: self.colsPerRow   = int(self.argMap['c'][0])
        if 'w' in self.argMap and len(self.argMap['w'])  > 0: self.ww           = int(self.argMap['w'][0])
        if 'h' in self.argMap and len(self.argMap['h'])  > 0: self.wh           = int(self.argMap['h'][0])
        if 'F' in self.argMap and len(self.argMap['F']) == 0: self.fullScreen   = True
        print('[p]         nPages={}'.format(self.nPages),       file=DBG_FILE)
        print('[l]   linesPerPage={}'.format(self.linesPerPage), file=DBG_FILE)
        print('[r]    rowsPerLine={}'.format(self.rowsPerLine),  file=DBG_FILE)
        print('[c]     colsPerRow={}'.format(self.colsPerRow),   file=DBG_FILE)
        print('[w]             ww={}'.format(self.ww),           file=DBG_FILE)
        print('[h]             wh={}'.format(self.wh),           file=DBG_FILE)
        print('[F]     fullScreen={}'.format(self.fullScreen),   file=DBG_FILE)
        self._initWindowA()
        super().__init__(screen=self.screens[1], fullscreen=self.fullScreen, resizable=True, visible=False)
        self._initWindowB()
        self._initTabs(opq=True)

    def _initWindowA(self):
        display      = pyglet.canvas.get_display()
        self.screens = display.get_screens()

    def _initWindowB(self):
        self.COLORS = [(240, 37, 27, 255), (36, 30, 240, 255), (33, 240, 34, 255), (244, 240, 12, 255)]
        self.batch  = pyglet.graphics.Batch()
        self.group = [pyglet.graphics.Group(g) for g in range(2)]
        self.set_size(self.ww, self.wh)
        self.set_visible()
        print('_initWindow() ww={} wh={}'.format(self.ww, self.wh), file=DBG_FILE)

    def on_draw(self):
        self.clear()
        self.batch.draw()

    def _initTabs(self, opq=True):
        print('_initTabs(BGN) nPages={} linesPerPage={} rowsPerLine={} colsPerRow={}'.format(self.nPages, self.linesPerPage, self.rowsPerLine, self.colsPerRow), file=DBG_FILE)
#        self.pages = [[[[pyglet.shapes.Rectangle(c*w, wh-h-m*wh/lpp-r*h, w, h, color=COLORS[(c+r) % 2], batch=self.batch) for c in range(cpr)] for r in range(rpl)] for m in range(lpp)] for p in range(np)]
#        self.lines = [self.pages[p][m] for m in range(lpp) for p in range(np)]
#        self.rows  = [self.pages[p][m][r] for r in range(rpl) for m in range(lpp) for p in range(np)]
#        self.cols  = [self.pages[p][m][r][c] for c in range(cpr) for r in range(rpl) for m in range(lpp) for p in range(np)]
        self.lines, self.rows, self.cols = [], [], []
        self._initPages(opq)
#            pages.append(lines)
#        self.pages.append(pages)
#        self._verify()
        print('_initTabs(END) nPages={} linesPerPage={} rowsPerLine={} colsPerRow={}'.format(self.nPages, self.linesPerPage, self.rowsPerLine, self.colsPerRow), file=DBG_FILE)

    def _initPages(self, opq=True):
        self.pages = []
        for p in range(self.nPages):
            lines = self._initLines(p, opq)
            self.pages.append(lines)

    def _initLines(self, p, opq=True):
        lines = []
        for m in range(self.linesPerPage):
            rows = self._initRows(p, m, opq)
            lines.append(rows)
        self.lines.append(lines)
        return lines

    def _initRows(self, p, m, opq=True):
        w, h, ww, wh = self.ww/self.colsPerRow, self.wh/(self.rowsPerLine*self.linesPerPage), self.ww, self.wh
        np, lpp, rpl, cpr = self.nPages, self.linesPerPage, self.rowsPerLine, self.colsPerRow
        rows = []
        for r in range(self.rowsPerLine):
            x, y = 0, wh-h-m*wh/lpp-r*h
            scip = pyglet.image.SolidColorImagePattern(self.COLORS[2] if (r/2)%2 else self.COLORS[3])
            sci = scip.create_image(width=fri(ww), height=fri(h))
            row = pyglet.sprite.Sprite(img=sci, x=x, y=y, batch=self.batch, group=self.group[0], subpixel=False)
            rows.append(row)
            if opq: opacity = 255
            else:   opacity = fri(255*(rpl-1-r)/(rpl-1))
            row.opacity = opacity
            sw, sh = row.width, row.height
            xp, yq = row.scale_x, row.scale_y
            if r==0: print('_initTabs() [{:2}] [{:2}] [{:2}]       x={:6.1f} y={:6.1f} sw={:4} sh={:3} xp={:5.3f} yq={:5.3f} ww={} wh={} color={} opacity={}'.format(p, m, r, x, y, sw, sh, xp, yq, ww, wh, row.color, opacity), file=DBG_FILE)
            cols = self._initCols(p, m, r)
            rows.append(cols)
        self.rows.append(rows)
        return rows
#        lines.append(rows)

    def _initCols(self, p, m, r, opq=True):
        w, h, ww, wh = self.ww/self.colsPerRow, self.wh/(self.rowsPerLine*self.linesPerPage), self.ww, self.wh
        np, lpp, rpl, cpr = self.nPages, self.linesPerPage, self.rowsPerLine, self.colsPerRow
        cols = []
        for c in range(self.colsPerRow):
            x, y = c*w, wh-h-m*wh/lpp-r*h
            scip = pyglet.image.SolidColorImagePattern(self.COLORS[(c+r)%2])
            sci  = scip.create_image(width=fri(w), height=fri(h))
            col  = pyglet.sprite.Sprite(img=sci, x=x, y=y, batch=self.batch, group=self.group[1], subpixel=False)
            if opq: opacity = 1
            else:   opacity = fri(255*(cpr-1-c)/(cpr-1))
            col.opacity     = opacity
            sw, sh = col.width,   col.height
            xp, yq = col.scale_x, col.scale_y
            cols.append(col)
            if r==0: print('_initTabs() [{:2}] [{:2}] [{:2}] [{:3}] x={:6.1f} y={:6.1f} sw={:4} sh={:3} xp={:5.3f} yq={:5.3f} ww={} wh={} color={} opacity={}'.format(p, m, r, c, x, y, sw, sh, xp, yq, ww, wh, col.color, opacity), file=DBG_FILE)
        self.cols.append(cols)
        return cols
#        rows.append(cols)

    def on_resize(self, width, height):
        super().on_resize(width, height)
        return
        self.ww, self.wh  = width, height
        print('on_resize(BGN) ww={} wh={}'.format(self.ww, self.wh), file=DBG_FILE)
        w, h, ww, wh = self.ww/self.colsPerRow, self.wh/(self.rowsPerLine*self.linesPerPage), self.ww, self.wh
        lpp = self.linesPerPage
        for p in range(self.nPages):
            for m in range(self.linesPerPage):
                for r in range(self.rowsPerLine):
                    x, y = 0, wh-h-m*wh/lpp-r*h
                    if type(self.pages[p][m][r]) == pyglet.sprite.Sprite:
                        self.pages[p][m][r].update(x=x, y=y, scale_x=width/self._ww, scale_y=height/self._wh)
                    else:
                        for c in range(self.colsPerRow):
                            x, y = c*w, wh-h-m*wh/lpp-r*h
                            self.pages[p][m][r][c].update(x=x, y=y, scale_x=width/self._ww, scale_y=height/self._wh)
                            sw, sh = self.pages[p][m][r][c].width,   self.pages[p][m][r][c].height
                            xp, yq = self.pages[p][m][r][c].scale_x, self.pages[p][m][r][c].scale_y
                            opacity = self.pages[p][m][r][c].opacity
                            if r==0: print('on_resize() [{:2}] [{:2}] [{:2}] [{:3}] x={:6.1f} y={:6.1f} sw={:4} sh={:3} xp={:5.3f} yq={:5.3f} ww={} wh={} opacity={}'.format(p, m, r, c, x, y, sw, sh, xp, yq, ww, wh, opacity), file=DBG_FILE)
#                self.pages[p][m][0][0].color = (159+m*32, 100, 16)
#        self._verify()
        print('on_resize(END) ww={} wh={}\n'.format(self.ww, self.wh), file=DBG_FILE)

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

if __name__ == '__main__':
    DBG_FILE = open(sys.argv[0] + ".log.txt", 'w')
    COLORS = [(0, 0, 0), (66, 60, 144), (97, 31, 93), (41, 90, 111)]
    tabs = Tabs()
    pyglet.app.run()


'''
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
        self._ww, self._wh = 1200, 800
        self.ww, self.wh = self._ww, self._wh
        self.nPages          = 4
        self.linesPerPage    = 3
        self.rowsPerLine     = 6
        self.colsPerRow      = 8
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
        self.cpn = 0
        self.tci = 0
        self.useOrderedGroup = True
        self.testColorLists = False
        print('_init() useOrderedGroup={}'.format(self.useOrderedGroup), file=DBG_FILE)
        if self.testColorLists: self._initColorLists()
        self._initTabs()

    def _initWindowA(self):
        display      = pyglet.canvas.get_display()
        self.screens = display.get_screens()

    def _initWindowB(self):
        self.batch = pyglet.graphics.Batch()
#        self.group = [pyglet.graphics.Group(g) for g in range(4)]
        self.set_size(self.ww, self.wh)
        self.set_visible()
        print('_initWindow() ww={} wh={}'.format(self.ww, self.wh), file=DBG_FILE)

    def _initTabs(self):
        print('_initTabs(BGN) nPages={} linesPerPage={} rowsPerLine={} colsPerRow={}'.format(self.nPages, self.linesPerPage, self.rowsPerLine, self.colsPerRow), file=DBG_FILE)
        self.pages, self.lines, self.rows, self.cols = [], [], [], []
#        if not self.useOrderedGroup: self.rootGroup = pyglet.graphics.Group()
        self._initPages(0, 0, self.ww, self.wh)
        print('_initTabs(END) nPages={} linesPerPage={} rowsPerLine={} colsPerRow={}'.format(self.nPages, self.linesPerPage, self.rowsPerLine, self.colsPerRow), file=DBG_FILE)

    @staticmethod
    def printSpriteInfo(reason, p, l, r, c, x, y, w, h, xm, ym, ww, hh, ii, jj, visible, color):
        formatStr = '{:12} {:2} {:2} {:2} {:3}  x={:6.1f} y={:6.1f} w={:4} h={:4} xm={:5.3f} ym={:5.3f} ww={:4} hh={:4} ii={} jj={} v={} c={}'
        print(formatStr.format(reason, p, l, r, c, x, y, w, h, xm, ym, ww, hh, ii, jj, visible, color), file=DBG_FILE)

    def _initPages(self, xx, yy, ww, hh, ii=0, jj=0):
        if self.useOrderedGroup: self.pageGroup = pyglet.graphics.OrderedGroup(0)
        else:                    self.pageGroup = pyglet.graphics.Group() #self.rootGroup)
        self.pageColors = [BLUES[0], PURPLES[0], CYANS[0], VIOLETS[0]]
        w, h = ww-2*ii, hh-jj
#        w, h = ww, hh
        np, l, r, c = self.nPages, 0, 0, 0
        for p in range(self.nPages):
            x, y   = xx, yy
            scip   = pyglet.image.SolidColorImagePattern(self.pageColors[p%np])
            sci    = scip.create_image(width=fri(w), height=fri(h))
            page   = pyglet.sprite.Sprite(img=sci, x=x, y=y, batch=self.batch, group=self.pageGroup, subpixel=self.subpixel)
            self.pages.append(page)
            if p  != self.cpn:     page.visible = False
            w, h   = page.width,   page.height
            xm, ym = page.scale_x, page.scale_y
            self.printSpriteInfo('_initPages()', p, l, r, c, x, y, w, h, xm, ym, ww, hh, ii, jj, page.visible, self.pageColors[p%np])
            lines  = self._initLines(x, y, w, h, p)
#            self.pages.append(lines)

    def _initLines(self, xx, yy, ww, hh, p, ii=6, jj=6):
        if self.useOrderedGroup: self.lineGroup = pyglet.graphics.OrderedGroup(1)
        else:                    self.lineGroup = pyglet.graphics.Group(self.pageGroup)
        self.lineColors = [GREENS[i] for i in range(len(GREENS))] # if i%2]
        lpp, r, c = self.linesPerPage, 0, 0
        w, h = ww-2*ii, (hh-(lpp+1)*jj)/lpp
        lines = []
        for l in range(lpp):
            x, y   = xx+ii, yy+jj*(l+1)+l*h
            scip   = pyglet.image.SolidColorImagePattern(self.lineColors[l%lpp])
            sci    = scip.create_image(width=fri(w), height=fri(h))
            line   = pyglet.sprite.Sprite(img=sci, x=x, y=y, batch=self.batch, group=self.lineGroup, subpixel=self.subpixel)
            self.lines.append(line)
            if p  != self.cpn:     line.visible = False
            w, h   = line.width,   line.height
            xm, ym = line.scale_x, line.scale_y
            self.printSpriteInfo('_initLines()', p, l, r, c, x, y, w, h, xm, ym, ww, hh, ii, jj, line.visible, self.lineColors[l%lpp])
##            rows   = self._initRows(x, y, w, h, p, l)
#            lines.append(rows)
#        self.lines.append(lines)
        return lines

    def _initRows(self, xx, yy, ww, hh, p, l, ii=4, jj=4):
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
            if p  != self.cpn:    row.visible = False
            w, h   = row.width,   row.height
            xm, ym = row.scale_x, row.scale_y
            self.printSpriteInfo('_initRows()', p, l, r, c, x, y, w, h, xm, ym, ww, hh, ii, jj, row.visible, self.rowColors[r%rpl])
            cols   = self._initCols(x, y, w, h, p, l, r)
#            rows.append(cols)
#        self.rows.append(rows)
        return rows
#        lines.append(rows)

    def _initCols(self, xx, yy, ww, hh, p, l, r, ii=2, jj=2):
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
            if p  != self.cpn:     col.visible = False
            w, h   = col.width,    col.height
            xm, ym = col.scale_x,  col.scale_y
            self.printSpriteInfo('_initCols()', p, l, r, c, x, y, w, h, xm, ym, ww, hh, ii, jj, col.visible, self.colColors[c%8])
#        self.cols.append(cols)
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
        if   motion == pygwink.MOTION_LEFT:          self.toggleColorLists(motion)
        elif motion == pygwink.MOTION_RIGHT:         self.toggleColorLists(motion)
        elif motion == pygwink.MOTION_NEXT_PAGE:     self.setCurrPage(motion)
        elif motion == pygwink.MOTION_PREVIOUS_PAGE: self.setCurrPage(motion)
        else:                                        print('on_text_motion() motion={} ???'.format(motion), file=DBG_FILE)

    def on_resize(self, width, height):
        super().on_resize(width, height)
        self.ww, self.wh  = width, height
        if self.testColorLists: self.resizeColorLists()
#        np, lpp, rpl, cpr = self.nPages, self.linesPerPage, self.rowsPerLine, self.colsPerRow
        np, lpp, rpl, cpr = len(self.pages), len(self.lines), len(self.rows), len(self.cols)
        ww, wh = self.ww, self.wh
        scale_x, scale_y = ww/self._ww, wh/self._wh
        for p in range(np):
            self.pages[p].update(x=self.pages[p].x*scale_x, y=self.pages[p].y*scale_y, scale_x=scale_x, scale_y=scale_y)
        for l in range(lpp):
            self.lines[l].update(x=self.lines[l].x*scale_x, y=self.lines[l].y*scale_y, scale_x=scale_x, scale_y=scale_y)
        for r in range(rpl):
            self.rows[r].update(x=self.rows[r].x*scale_x, y=self.rows[r].y*scale_y, scale_x=scale_x, scale_y=scale_y)
        for c in range(cpr):
            self.cols[c].update(x=self.cols[c].x*scale_x, y=self.cols[c].y*scale_y, scale_x=scale_x, scale_y=scale_y)
        print('on_resize(BGN) ww={} wh={}'.format(ww, wh), file=DBG_FILE)
        w, h = ww/self.colsPerRow, wh/(self.rowsPerLine*self.linesPerPage)
        lpp = self.linesPerPage
        for p in range(self.nPages):
            if type(self.pages[p]) == pyglet.sprite.Sprite:
                self.pages[p].update(x=0, y=0, scale_x=ww/self._ww, scale_y=wh/self._wh)
            else:
                for l in range(self.linesPerPage):
                    if type(self.pages[p][l])==pyglet.sprite.Sprite:
                        self.pages[p][l].update(x=x, y=y, scale_x=ww/self._ww, scale_y=wh/self._wh)
                    else:
                        for r in range(self.rowsPerLine):
                            if type(self.pages[p][l][r]) == pyglet.sprite.Sprite:
                                self.pages[p][l][r].update(x=x, y=y, scale_x=ww/self._ww, scale_y=wh/self._wh)
                            else:
                                for c in range(self.colsPerRow):
                                    x, y = c*w, wh-h-l*wh/lpp-r*h
                                    self.pages[p][l][r][c].update(x=x, y=y, scale_x=ww/self._ww, scale_y=wh/self._wh)
                                    sw, sh = self.pages[p][l][r][c].width, self.pages[p][l][r][c].height
                                    xp, yq = self.pages[p][l][r][c].scale_x, self.pages[p][l][r][c].scale_y
                                    if r==0: print('on_resize() [{:2}] [{:2}] [{:2}] [{:3}] x={:6.1f} y={:6.1f} sw={:4} sh={:3} xp={:5.3f} yq={:5.3f} ww={} wh={}'.format(p, l, r, c, x, y, sw, sh, xp, yq, ww, wh), file=DBG_FILE)
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
'''
