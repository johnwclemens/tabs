import sys, os
sys.path.insert(0, os.path.abspath('C:/Python36/my/lib'))
sys.path.insert(0, os.path.abspath('C:/Python36/my/lib/pyglet'))
import pyglet
import pyglet.window     as pygwin
# import pyglet.window.key as pygwink
import cmdArgs

class Tabs(pygwin.Window):
    def __init__(self):
        self.nPages          = 1
        self.linesPerPage    = 4
        self.rowsPerLine     = 6
        self.colsPerRow      = 100
        self.ww              = 1000
        self.wh              = 600
        self.fullScreen      = True
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
#        self.set_size(self.ww, self.wh)
        self.set_visible()
        print('_initWindow() ww={} wh={}'.format(self.ww, self.wh), file=DBG_FILE)

    def _initTabs(self):
        print('_initTabs(BGN) nPages={} linesPerPage={} rowsPerLine={} colsPerRow={}'.format(self.nPages, self.linesPerPage, self.rowsPerLine, self.colsPerRow), file=DBG_FILE)
        w, h, wh = self.ww/self.colsPerRow, self.wh/(self.rowsPerLine*self.linesPerPage), self.wh
        lpp = self.linesPerPage
        self.pages, self.lines, self.rows, self.cols = [], [], [], []
        for p in range(self.nPages):
            lines = []
            for m in range(self.linesPerPage):
                rows = []
                for r in range(self.rowsPerLine):
                    cols = []
                    for c in range(self.colsPerRow):
                        cols.append(pyglet.shapes.Rectangle(c*w, wh-h-m*wh/lpp-r*h, w, h, color=COLORS[(c+r) % 2], batch=self.batch))
#                        print('c={:3} w={:6.1f} c*w={:6.1f} wh={} h={:5.1f} r={} m={} p={} m*wh/lpp={:6.1f} wh-h-m*wh/lpp-r*h={:6.1f}'.format(c, w, c*w, wh, h, r, m, p, m*wh/lpp, wh-h-m*wh/lpp-r*h), file=DBG_FILE)
                    print('wh={} h={:5.1f} r={} m={} p={} m*wh/lpp={:6.1f} wh-h-m*wh/lpp-r*h={:6.1f}'.format(wh, h, r, m, p, m*wh/lpp, wh-h-m*wh/lpp-r*h), file=DBG_FILE)
                    self.cols.append(cols)
#                    print('_initTabs() r={} m={} p={}'.format(r, m, p), file=DBG_FILE)
                    rows.append(cols)
                self.rows.append(rows)
                lines.append(rows)
            self.lines.append(lines)
            self.pages.append(lines)
        print('_initTabs(END) len(pages={}) len(lines={}) len(rows={}) len(cols={})\n'.format(len(self.pages), len(self.lines), len(self.rows), len(self.cols)), file=DBG_FILE)

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
                        self.cols[r][c].position = (c*w, wh-h-m*wh/lpp-r*h)
                        self.cols[r][c].width, self.cols[r][c].height = w, h
#                        print('c={:3} w={:6.1f} c*w={:6.1f} wh={} h={:5.1f} r={} m={} p={} m*wh/lpp={:6.1f} wh-h-m*wh/lpp-r*h={:6.1f}'.format(c, w, c*w, wh, h, r, m, p, m*wh/lpp, wh-h-m*wh/lpp-r*h), file=DBG_FILE)
                    print('wh={} h={:5.1f} r={} m={} p={} m*wh/lpp={:6.1f} wh-h-m*wh/lpp-r*h={:6.1f}'.format(wh, h, r, m, p, m * wh / lpp, wh - h - m * wh / lpp - r * h), file=DBG_FILE)
#                print('on_resize() ww={} wh={} r={} m={} p={}'.format(self.ww, self.wh, r, m, p), file=DBG_FILE)
        print('on_resize(END) ww={} wh={}/n'.format(self.ww, self.wh), file=DBG_FILE)

    def on_draw(self):
#        super().clear()
        self.clear()
        self.batch.draw()

if __name__ == '__main__':
    DBG_FILE = open(sys.argv[0] + ".log.txt", 'w')
    COLORS = [(0, 0, 0), (66, 60, 144)]
    tabs = Tabs()
    pyglet.app.run()

#        cpl, rpl = self.colsPerLine, self.rowsPerLine
#            self.lines.append([[pyglet.shapes.Rectangle(c*w, wh-h-r*h, w, h, color=COLORS[(c+r) % 2], batch=self.batch) for c in range(cpl)] for r in range(rpl)])
#            pages.append(lines)
#        self.pages.append(pages)
