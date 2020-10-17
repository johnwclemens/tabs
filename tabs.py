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
        self.colorListSprites = []
        self.colorLists = (C_REDS, C_GRNS, C_BLUS, C_YLWS, C_CYNS, C_MAGS, C_ORGS)
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
        self.pages, self.lines, self.rows, self.cols = [], [], [], [], []
        self._initPages(opq)
        print('_initTabs(END) nPages={} linesPerPage={} rowsPerLine={} colsPerRow={}'.format(self.nPages, self.linesPerPage, self.rowsPerLine, self.colsPerRow), file=DBG_FILE)

    def _initPages(self, opq=True):
#        self.PAGE_C = [(248, 20, 225, 255), (248, 40, 35, 255), (48, 60, 255, 255)]
        self.PAGE_C = [C_PRP[i] for i in range(len(C_PRP))]
        ww, wh = self.ww, self.wh
        for p in range(self.nPages):
            x, y = 0, 0
            scip = pyglet.image.SolidColorImagePattern(self.PAGE_C[p])
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
#        self.LINE_C = [(248, 20, 25, 255), (248, 240, 35, 255), (48, 240, 35, 255), (48, 60, 255, 255)]
        self.LINE_C = [C_RED[i] for i in range(len(C_RED)) if i%2]
        w, h, ww, wh = self.ww/self.colsPerRow, self.wh/self.linesPerPage, self.ww, self.wh
        np, lpp, rpl, cpr = self.nPages, self.linesPerPage, self.rowsPerLine, self.colsPerRow
        lines = []
        for m in range(self.linesPerPage):
            x, y = 0, wh-h-m*wh/lpp
            scip = pyglet.image.SolidColorImagePattern(self.LINE_C[m])
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
            print('_initLines() [{:2}] [{:2}]         x={:6.1f} y={:6.1f} sw={:4} sh={:3} xp={:5.3f} yq={:5.3f} ww={} wh={} opacity={} color={}'.format(p, m, x, y, sw, sh, xp, yq, ww, wh, opacity, self.LINE_C[m]), file=DBG_FILE)
        self.lines.append(lines)
        return lines

    def _initRows(self, p, m, o=-1):
        self.ROW_C = []
        w, h, ww, wh = self.ww/self.colsPerRow, self.wh/(self.rowsPerLine*self.linesPerPage), self.ww, self.wh
        np, lpp, rpl, cpr = self.nPages, self.linesPerPage, self.rowsPerLine, self.colsPerRow
        rows = []
        for r in range(self.rowsPerLine):
            x, y = 0, wh-h-m*wh/lpp-r*h
            scip = pyglet.image.SolidColorImagePattern(self.ROW_C[r%rpl])
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
            scip = pyglet.image.SolidColorImagePattern(self.COL_C[(c+r)%2])
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

    def on_resize_OLD(self, width, height):
        super().on_resize(width, height)

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

    def _initColorLists(self):
        cl = self.colorLists
        ncl = len(cl)
        for i in range(ncl):
            sprites = []
            for j in range(len(cl[i])):
                nj = len(cl[i])
                h, ww, wh = self.wh/nj, self.ww, self.wh
                x, y = 0, wh-h-j*wh/nj
                scip = pyglet.image.SolidColorImagePattern(cl[i][j])
                sci = scip.create_image(width=fri(ww), height=fri(h))
                spr = pyglet.sprite.Sprite(img=sci, x=x, y=y, batch=self.batch)
                if i == 0: spr.visible = True
                else:      spr.visible = False
                sprites.append(spr)
                sw, sh = spr.width,   spr.height
                xp, yq = spr.scale_x, spr.scale_y
                print('_initColorLists [{:2}] [{:2}] x={:6.1f} y={:6.1f} sw={:4} sh={:3} xp={:5.3f} yq={:5.3f} ww={} wh={} visible={} cl={}'.format(i, j, x, y, sw, sh, xp, yq, ww, wh, spr.visible, cl[i][j]), file=DBG_FILE)
            self.colorListSprites.append(sprites)

    def toggleColorLists(self, motion):
        cls = self.colorListSprites
        if   motion==pygwink.MOTION_LEFT:
            for j in range(len(cls[self.tci])): cls[self.tci][j].visible = False
            self.tci += 1
            self.tci = self.tci % len(self.colorLists)
            for j in range(len(cls[self.tci])): cls[self.tci][j].visible = True
            print('toggleColorLists() MOTION_LEFT={} tci={} len(cls)={}'.format(motion, self.tci, len(cls)), file=DBG_FILE)
        elif motion==pygwink.MOTION_RIGHT:
            for j in range(len(cls[self.tci])): cls[self.tci][j].visible = False
            self.tci -= 1
            self.tci = self.tci % len(self.colorLists)
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

def C_GEN(c1, c2, ns=8):
    colors = []
    diffs = [c2[i] - c1[i] for i in range(len(c1))]
    steps = [diffs[i]/ns   for i in range(len(c1))]
    print('C_GEN(), c1={} c2={} ns={} diffs={} steps={}'.format(c1, c2, ns, diffs, steps))
    for j in range(ns):
        c = tuple([fri(c1[i]+j*steps[i]) for i in range(len(c1))])
        print('C_GEN() c[{}]={}'.format(j, c))
        colors.append(c)
    print('C_GEN() colors={}'.format(colors))
    return colors

if __name__ == '__main__':
    DBG_FILE = open(sys.argv[0] + ".log.txt", 'w')
    C_RED = [(255, 32, 64, 255), (240, 0, 0, 255), (224, 0, 0, 255), (208, 0, 0, 255), (192, 0, 0, 255), (176, 0, 0, 255), (160, 64, 32, 255), (144, 64, 32, 255)]
    C_GRN = [(64, 255, 32, 255), (0, 240, 0, 255), (0, 224, 0, 255), (0, 208, 0, 255), (0, 192, 0, 255), (0, 176, 0, 255), (0, 160, 0, 255), (32, 144, 64, 255)]
    C_BLU = [(32, 64, 255, 255), (0, 0, 240, 255), (0, 0, 224, 255), (0, 0, 208, 255), (0, 0, 192, 255), (0, 0, 176, 255), (0, 0, 160, 255), (64, 32, 144, 255)]
    C_YLW = [(255, 255, 64, 255), (240, 240, 0, 255), (224, 224, 0, 255), (208, 208, 0, 255), (192, 192, 0, 255), (176, 176, 0, 255), (160, 160, 0, 255), (144, 144, 32, 255)]
    C_CYN = [(32, 255, 255, 255), (0, 240, 240, 255), (0, 224, 224, 255), (0, 208, 208, 255), (0, 192, 192, 255), (0, 176, 176, 255), (0, 160, 160, 255), (64, 144, 144, 255)]
    C_MAG = [(255, 64, 255, 255), (240, 0, 240, 255), (224, 0, 224, 255), (208, 0, 208, 255), (192, 0, 192, 255), (176, 0, 176, 255), (160, 0, 160, 255), (144, 32, 144, 255)]
    C_ORG = [(228, 96, 128, 255), (240, 0, 240, 255), (224, 0, 224, 255), (208, 0, 208, 255), (192, 0, 192, 255), (176, 0, 176, 255), (160, 0, 160, 255), (144, 64, 0, 255)]
    C_REDS = C_GEN(C_RED[0], C_RED[7])
    C_GRNS = C_GEN(C_GRN[0], C_GRN[7])
    C_BLUS = C_GEN(C_BLU[0], C_BLU[5])
    C_YLWS = C_GEN(C_YLW[0], C_YLW[5])
    C_CYNS = C_GEN(C_CYN[0], C_CYN[5])
    C_MAGS = C_GEN(C_MAG[0], C_MAG[5])
    C_ORGS = C_GEN(C_ORG[0], C_ORG[5])
    tabs = Tabs()
    pyglet.app.run()
