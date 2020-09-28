import sys, os
sys.path.insert(0, os.path.abspath('C:/Python36/my/lib'))
sys.path.insert(0, os.path.abspath('C:/Python36/my/lib/pyglet'))
import pyglet
import pyglet.window     as pygwin
# import pyglet.window.key as pygwink
import cmdArgs

class Tabs(pygwin.Window):
    def __init__(self):
        self.nPages          = 3
        self.linesPerPage    = 4
        self.rowsPerLine     = 6
        self.colsPerRow      = 100
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
        print('_initWindow() ww={} wh={}'.format(self.ww, self.wh), file=DBG_FILE)

    def _initTabs(self):
        print('_initTabs(BGN) nPages={} linesPerPage={} rowsPerLine={} colsPerRow={}'.format(self.nPages, self.linesPerPage, self.rowsPerLine, self.colsPerRow), file=DBG_FILE)
        w, h, wh = self.ww/self.colsPerRow, self.wh/(self.rowsPerLine * self.linesPerPage), self.wh
        lpp = self.linesPerPage
        self.pages, self.lines, self.rows, self.cols = [], [], [], []
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
        self._verify()
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
                    for c in range(self.colsPerRow):
                        self.pages[0][p][m][r][c].position = (c*w, wh-h-m*wh/lpp-r*h)
                        self.pages[0][p][m][r][c].width,     self.pages[0][p][m][r][c].height = w, h
                        self.pages[0][p][m][r][c].color    = COLORS[(c+r) % 2 + 2]
                    print('p={} m={} r={} wh={} h={:5.1f} m*wh/lpp={:6.1f} wh-h-m*wh/lpp-r*h={:6.1f}'.format(p, m, r, wh, h, m*wh/lpp, wh-h-m*wh/lpp-r*h), file=DBG_FILE)
                self.pages[0][p][m][0][0].color = (127, 121, 16)
        self._verify()
        print('on_resize(END) ww={} wh={}\n'.format(self.ww, self.wh), file=DBG_FILE)

    def _verify(self):
        tmp = [len(e) for e in (self.pages, self.pages[0],  self.lines, self.lines[0], self.rows, self.rows[0], self.cols, self.cols[0])]
        d = dict(zip(['pages', 'pages[0]', 'lines', 'lines[0]', 'rows', 'rows[0]', 'cols', 'cols[0]'], tmp))
        print('_verify(BGN) {}'.format(d), file=DBG_FILE)
        print("_verify() d[pages[0]]={}=nPages={} d[lines[0]]={}=linesPerPage={} d[rows[0]]={}=rowsPerLine={} d[cols[0]]={}=colsPerRow={}".
              format(d['pages[0]'], self.nPages, d['lines[0]'], self.linesPerPage, d['rows[0]'], self.rowsPerLine, d['cols[0]'], self.colsPerRow), file=DBG_FILE)
        assert(d['pages[0]']   == self.nPages);      assert(d['lines[0]'] == self.linesPerPage)
        assert(d['rows[0]'] == self.rowsPerLine); assert(d['cols[0]']  == self.colsPerRow)
        for p in range(self.nPages):
            for m in range(self.linesPerPage):
                for r in range(self.rowsPerLine):
                    q = self.pages[0][p][m][r][0]
                    print('p={} m={} r={} position=({:5.1f}, {:5.1f}) w={:5.1f} h={:5.1f}'.format(p, m, r, q.x, q.y, q.width, q.height), file=DBG_FILE)
        print('_verify(BGN) {}'.format(d), file=DBG_FILE)
#        if self.cols[0][0] == self.rows[0][0][0]:

    def on_draw(self):  #        super().clear()
        self.clear()
        self.batch.draw()

if __name__ == '__main__':
    DBG_FILE = open(sys.argv[0] + ".log.txt", 'w')
    COLORS = [(0, 0, 0), (66, 60, 144), (97, 31, 93), (41, 90, 111)]
    tabs = Tabs()
    pyglet.app.run()
