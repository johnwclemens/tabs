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
        self.cpn = 0
        self.tci = 0
        self._initColorLists()
#        self._initTabs(opq=True)

    def _initWindowA(self):
        display      = pyglet.canvas.get_display()
        self.screens = display.get_screens()

    def _initWindowB(self):
        self.batch  = pyglet.graphics.Batch()
        self.group = [pyglet.graphics.Group(g) for g in range(2)]
        self.set_size(self.ww, self.wh)
        self.set_visible()
        print('_initWindow() ww={} wh={}'.format(self.ww, self.wh), file=DBG_FILE)

    def _initTabs(self, opq=True):
        print('_initTabs(BGN) nPages={} linesPerPage={} rowsPerLine={} colsPerRow={}'.format(self.nPages, self.linesPerPage, self.rowsPerLine, self.colsPerRow), file=DBG_FILE)
        self.pages, self.lines, self.rows, self.cols = [], [], [], []
        self._initPages(opq)
        print('_initTabs(END) nPages={} linesPerPage={} rowsPerLine={} colsPerRow={}'.format(self.nPages, self.linesPerPage, self.rowsPerLine, self.colsPerRow), file=DBG_FILE)

    def _initPages(self, opq=True):
#        self.pageColors = [(248, 20, 225, 255), (248, 40, 35, 255), (48, 60, 255, 255)]
        self.pageColors = [BLUES[i] for i in range(len(BLUES))]
        ww, wh = self.ww, self.wh
        for p in range(self.nPages):
            x, y = 0, 0
            scip = pyglet.image.SolidColorImagePattern(self.pageColors[p])
            sci = scip.create_image(width=fri(ww), height=fri(wh))
            page = pyglet.sprite.Sprite(img=sci, x=x, y=y, batch=self.batch, subpixel=False)
            self.pages.append(page)
            if opq: opacity = 255
            else:   opacity = fri(255*(self.nPages-1-p)/(self.nPages-1))
            page.opacity = opacity
            if p != self.cpn:      page.visible = False
            sw, sh = page.width,   page.height
            xp, yq = page.scale_x, page.scale_y
            print('_initPages() [{:2}]              x={:6.1f} y={:6.1f} sw={:4} sh={:3} xp={:5.3f} yq={:5.3f} ww={} wh={} opacity={} cpn={}'.format(p, x, y, sw, sh, xp, yq, ww, wh, opacity, self.cpn), file=DBG_FILE)
            lines = self._initLines(p, opq)
#        self.pages.append(lines)

    def _initLines(self, p, opq=True):
#        self.lineColors = [(248, 20, 25, 255), (248, 240, 35, 255), (48, 240, 35, 255), (48, 60, 255, 255)]
        self.lineColors = [GREENS[i] for i in range(len(GREENS)) if i%2]
        w, h, ww, wh = self.ww/self.colsPerRow, self.wh/self.linesPerPage, self.ww, self.wh
        np, lpp, rpl, cpr = self.nPages, self.linesPerPage, self.rowsPerLine, self.colsPerRow
        lines = []
        for m in range(self.linesPerPage):
            x, y = 0, wh-h-m*wh/lpp
            scip = pyglet.image.SolidColorImagePattern(self.lineColors[m])
            sci = scip.create_image(width=fri(ww), height=fri(h))
            line = pyglet.sprite.Sprite(img=sci, x=x, y=y, batch=self.batch, subpixel=False)
            self.lines.append(line)
            if opq: opacity = 255
            else:   opacity = fri(255*(np-1-p)/(self.np-1))
            line.opacity = opacity
            sw, sh = line.width,   line.height
            xp, yq = line.scale_x, line.scale_y
#            rows = self._initRows(p, m, opq)
#            lines.append(rows)
            print('_initLines() [{:2}] [{:2}]         x={:6.1f} y={:6.1f} sw={:4} sh={:3} xp={:5.3f} yq={:5.3f} ww={} wh={} opacity={} color={}'.format(p, m, x, y, sw, sh, xp, yq, ww, wh, opacity, self.lineColors[m]), file=DBG_FILE)
        self.lines.append(lines)
        return lines

    def _initRows(self, p, m, o=-1):
        self.rowColors = [REDS[i] for i in range(len(REDS)) if i%2]
        w, h, ww, wh = self.ww/self.colsPerRow, self.wh/(self.rowsPerLine*self.linesPerPage), self.ww, self.wh
        np, lpp, rpl, cpr = self.nPages, self.linesPerPage, self.rowsPerLine, self.colsPerRow
        rows = []
        for r in range(self.rowsPerLine):
            x, y = 0, wh-h-m*wh/lpp-r*h
            scip = pyglet.image.SolidColorImagePattern(self.rowColors[r%rpl])
            sci = scip.create_image(width=fri(ww), height=fri(h))
            row = pyglet.sprite.Sprite(img=sci, x=x, y=y, batch=self.batch, group=self.group[0], subpixel=False)
            rows.append(row)
            if o<0: opacity = 255
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
            scip = pyglet.image.SolidColorImagePattern(self.colColors[(c+r)%2])
            sci  = scip.create_image(width=fri(w), height=fri(h))
            col  = pyglet.sprite.Sprite(img=sci, x=x, y=y, batch=self.batch, group=self.group[1], subpixel=False)
            if opq: opacity = 128
            else:   opacity = fri(255*(cpr-1-c)/(cpr-1))
            col.opacity     = opacity
            sw, sh = col.width,   col.height
            xp, yq = col.scale_x, col.scale_y
            cols.append(col)
            if r==0: print('_initTabs() [{:2}] [{:2}] [{:2}] [{:3}] x={:6.1f} y={:6.1f} sw={:4} sh={:3} xp={:5.3f} yq={:5.3f} ww={} wh={} color={} opacity={}'.format(p, m, r, c, x, y, sw, sh, xp, yq, ww, wh, col.color, opacity), file=DBG_FILE)
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

    def on_resize_OLD(self, width, height):
        super().on_resize(width, height)
#        return
        self.ww, self.wh = width, height
        print('on_resize(BGN) ww={} wh={}'.format(self.ww, self.wh), file=DBG_FILE)
        w, h, ww, wh = self.ww/self.colsPerRow, self.wh/(self.rowsPerLine*self.linesPerPage), self.ww, self.wh
        lpp = self.linesPerPage
        for p in range(self.nPages):
            for m in range(self.linesPerPage):
                for r in range(self.rowsPerLine):
                    x, y = 0, wh-h-m*wh/lpp-r*h
                    if type(self.pages[p][m][r])==pyglet.sprite.Sprite:
                        self.pages[p][m][r].update(x=x, y=y, scale_x=width/self._ww, scale_y=height/self._wh)
                    else:
                        for c in range(self.colsPerRow):
                            x, y = c*w, wh-h-m*wh/lpp-r*h
                            self.pages[p][m][r][c].update(x=x, y=y, scale_x=width/self._ww, scale_y=height/self._wh)
                            sw, sh = self.pages[p][m][r][c].width, self.pages[p][m][r][c].height
                            xp, yq = self.pages[p][m][r][c].scale_x, self.pages[p][m][r][c].scale_y
                            opacity = self.pages[p][m][r][c].opacity
                            if r==0: print('on_resize() [{:2}] [{:2}] [{:2}] [{:3}] x={:6.1f} y={:6.1f} sw={:4} sh={:3} xp={:5.3f} yq={:5.3f} ww={} wh={} opacity={}'.format(p, m, r, c, x, y, sw, sh, xp, yq, ww, wh, opacity), file=DBG_FILE)
#                self.pages[p][m][0][0].color = (159+m*32, 100, 16)
#        self._verify()
        print('on_resize(END) ww={} wh={}\n'.format(self.ww, self.wh), file=DBG_FILE)

    def on_resize(self, width, height):
        super().on_resize(width, height)
        self.ww, self.wh  = width, height
        self.resizeColorLists()

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
        elif motion==pygwink.MOTION_PREVIOUS_PAGE:
            self.pages[self.cpn].visible = False
            self.cpn -= 1
            self.cpn = self.cpn % self.nPages
            self.pages[self.cpn].visible = True
        print('setCurrPage() motion={} MOTION_NEXT_PAGE cpn={}'.format(motion, self.cpn), file=DBG_FILE)

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
