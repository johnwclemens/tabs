import sys, os
import pyglet
import pyglet.window     as pygwin
#import pyglet.text       as pygtxt
#import pyglet.window.key as pygwink
sys.path.insert(0, os.path.abspath('C:/Python36/my/lib'))
import cmdArgs

class Tabs(pygwin.Window):
    def __init__(self):
        self.nPages          = 3
        self.linesPerPage    = 4
        self.rowsPerLine     = 6
        self.colsPerRow      = 10
        self.ww              = 1000
        self.wh              = 600
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
        self._initWindow()
        self._initTabs()

    def _initWindow(self):
        display      = pyglet.canvas.get_display()
        self.screens = display.get_screens()
        super().__init__(screen=self.screens[1], fullscreen=self.fullScreen, resizable=True, visible=False)
        self.batch   = pyglet.graphics.Batch()
        self.set_size(self.ww, self.wh)
        self.set_visible()
#        asteroid = pyglet.image.load('asteroid.png')
#        sprite = pyglet.sprite.Sprite(img=asteroid, batch=self.batch)
#        self.label = pyglet.text.Label(text='A', font_name='Times New Roman', font_size=14, color=(63, 200, 233), x=100, y=50)  # , batch=self.batch)
#        self.label = pyglet.text.Label('ABC', font_name='Lucida Console', font_size=16, x=100, y=50, width=10, height=10, anchor_x='center', anchor_y='center', batch=self.batch)
        print('_initWindow() ww={} wh={}'.format(self.ww, self.wh), file=DBG_FILE)

    def on_draw(self):
        self.clear()
#        self.label.draw()
        self.batch.draw()

    def _initTabs(self):
        print('_initTabs(BGN) nPages={} linesPerPage={} rowsPerLine={} colsPerRow={}'.format(self.nPages, self.linesPerPage, self.rowsPerLine, self.colsPerRow), file=DBG_FILE)
        w, h, wh = self.ww/self.colsPerRow, self.wh/(self.rowsPerLine * self.linesPerPage), self.wh
        np, lpp, rpl, cpr = self.nPages, self.linesPerPage, self.rowsPerLine, self.colsPerRow
        self.pages = [[[pyglet.shapes.Rectangle(0, wh-h-m*wh/lpp-r*h, w, h, color=COLORS[r % 2], batch=self.batch) for r in range(rpl)] for m in range(lpp)] for p in range(np)]
        self.pages = [[[[pyglet.shapes.Rectangle(c*w, wh-h-m*wh/lpp-r*h, w, h, color=COLORS[(c+r) % 2], batch=self.batch) for c in range(cpr)] for r in range(rpl)] for m in range(lpp)] for p in range(np)]
        self.lines = [self.pages[p][m] for m in range(lpp) for p in range(np)]
        self.rows  = [self.pages[p][m][r] for r in range(rpl) for m in range(lpp) for p in range(np)]
        self.cols  = [self.pages[p][m][r][c] for c in range(cpr) for r in range(rpl) for m in range(lpp) for p in range(np)]
#        self.labels = [[[[pyglet.text.Label('Ab', font_name='Lucida Console', font_size=16, x=c*w, y=wh-h-m*wh/lpp-r*h, width=w, height=h, align='right', batch=self.batch)
#                          for c in range(cpr)] for r in range(rpl)] for m in range(lpp)] for p in range(np)]
        '''
        self.lines, self.rows, self.cols = [], [], []
        pages = []
        for p in range(self.nPages):
            lines = []
            for m in range(self.linesPerPage):
                rows = []
                for r in range(self.rowsPerLine):
                    cols = []
                    for c in range(self.colsPerRow):
                        cols.append(pyglet.shapes.Rectangle(c*w, wh-h-m*wh/lpp-r*h, w, h, color=COLORS[(c+r) % 2], batch=self.batch))
                    print('p={} m={} r={} wh={} h={:5.1f} m*wh/lpp={:6.1f} wh-h-m*wh/lpp-r*h={:6.1f}'.format(p, m, r, wh, h, m*wh/lpp, wh-h-m*wh/lpp-r*h), file=DBG_FILE)
                    self.cols.append(cols)
                    rows.append(cols)
                self.cols[0][0].color = (127, 121, 16)
                self.rows.append(rows)
                lines.append(rows)
            self.lines.append(lines)
            pages.append(lines)
        self.pages.append(pages)
        '''
#        self._verify()
        print('_initTabs(END) nPages={} linesPerPage={} rowsPerLine={} colsPerRow={}'.format(self.nPages, self.linesPerPage, self.rowsPerLine, self.colsPerRow), file=DBG_FILE)

    def on_resize(self, width, height):
        super().on_resize(width, height)
        self.ww, self.wh  = width, height
        print('on_resize(BGN) ww={} wh={}'.format(self.ww, self.wh), file=DBG_FILE)
        w, h, wh = self.ww/self.colsPerRow, self.wh/(self.rowsPerLine*self.linesPerPage), self.wh
        lpp = self.linesPerPage
        for p in range(self.nPages):
            for m in range(self.linesPerPage):
                for r in range(self.rowsPerLine):
#                    self.pages[p][m][r].position = (0, wh-h-m*wh/lpp-r*h)
#                    self.pages[p][m][r].width, self.pages[p][m][r].height = w, h
#                    self.pages[p][m][r].color    = COLORS[(r) % 2 + 2]
#                    self.pages[p][m][r].opacity  = 127
                    for c in range(self.colsPerRow):
                        self.pages[p][m][r][c].position = (c*w, wh-h-m*wh/lpp-r*h)
                        self.pages[p][m][r][c].width, self.pages[p][m][r][c].height = w, h
                        self.pages[p][m][r][c].color    = COLORS[(c+r) % 2 + 2]
#                        self.labels[p][m][r][c].x,     self.labels[p][m][r][c].y      = c*w, wh-h-m*wh/lpp-r*h
#                        self.labels[p][m][r][c].width, self.labels[p][m][r][c].height = w,   h
#                        print('{},{},{},{},{:6.1f},{:6.1f},{:6.1f},{:6.1f}'.format(p, m, r, c, self.labels[p][m][r][c].x, self.labels[p][m][r][c].y, self.labels[p][m][r][c].width, self.labels[p][m][r][c].height), file=DBG_FILE, end=' ')
                    print(file=DBG_FILE)
#                    print('p={} m={} r={} wh={} h={:5.1f} m*wh/lpp={:6.1f} wh-h-m*wh/lpp-r*h={:6.1f}'.format(p, m, r, wh, h, m*wh/lpp, wh-h-m*wh/lpp-r*h), file=DBG_FILE)
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
                    q = self.lines[m][r][c]
                    print('lines: m={} r={} c={} position=({:5.1f}, {:5.1f}) w={:5.1f} h={:5.1f}'.format(m, r, c, q.x, q.y, q.width, q.height), file=DBG_FILE)
        print('printStruct() len(rows)={} cpr={}'.format(len(self.rows), cpr), file=DBG_FILE)
        for r in range(len(self.rows)):
            for c in range(cpr):
                q = self.rows[r][c]
                print('rows: r={} c={} position=({:5.1f}, {:5.1f}) w={:5.1f} h={:5.1f}'.format(r, c, q.x, q.y, q.width, q.height), file=DBG_FILE)
        print('printStruct() len(cols)={}'.format(len(self.cols)), file=DBG_FILE)
        for c in range(len(self.cols)):
            q = self.cols[c]
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
