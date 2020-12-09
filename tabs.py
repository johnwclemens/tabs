import math, sys, os
import pyglet
import pyglet.window.key as pygwink
sys.path.insert(0, os.path.abspath('../lib'))
import cmdArgs

def fri(f): return int(math.floor(f+0.5))
RUN_TEST = False;  ORDER_GROUP = True;  SUBPIX = True;  FULL_SCREEN = False;  DBG = False

class Tabs(pyglet.window.Window):
    def __init__(self):
        global FULL_SCREEN, SUBPIX, ORDER_GROUP, RUN_TEST
        self.ww, self.hh  = 1000, 600
        if RUN_TEST: self.n, self.x, self.y, self.w, self.h, self.o, self.g, self.i = [9, 12, 0, 0], [4, 0, 0, 0], [0, 3, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [1, 1, 0, 0], [], [0, 0, 0, 0]
        else:        self.n, self.x, self.y, self.w, self.h, self.o, self.g, self.i = [1, 2, 3, 10], [0, 2, 2, 0], [0, 2, 2, 0], [0, 0, 0, 0], [0, 0, 0, 0], [2, 0, 0, 3], [], [0, 0, 0, 13]
        self.argMap = cmdArgs.parseCmdLine(dbg=1)
        print('_init(BGN) argMap={}'.format(self.argMap), file=DBG_FILE)
        if 'n' in self.argMap and len(self.argMap['n'])  > 0: self.n            = [int(self.argMap['n'][i]) for i in range(len(self.argMap['n']))]
        if 'x' in self.argMap and len(self.argMap['x'])  > 0: self.x            = [int(self.argMap['x'][i]) for i in range(len(self.argMap['x']))]
        if 'y' in self.argMap and len(self.argMap['y'])  > 0: self.y            = [int(self.argMap['y'][i]) for i in range(len(self.argMap['y']))]
        if 'w' in self.argMap and len(self.argMap['w'])  > 0: self.ww           =  int(self.argMap['w'][0])
        if 'h' in self.argMap and len(self.argMap['h'])  > 0: self.hh           =  int(self.argMap['h'][0])
        if 'o' in self.argMap and len(self.argMap['o'])  > 0: self.o            = [int(self.argMap['o'][i]) for i in range(len(self.argMap['o']))]
        if 'i' in self.argMap and len(self.argMap['i'])  > 0: self.i            = [int(self.argMap['i'][i]) for i in range(len(self.argMap['i']))]
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
        print('[i]            i={}'.format(self.i),          file=DBG_FILE)
        print('[S]  FULL_SCREEN={}'.format(FULL_SCREEN),     file=DBG_FILE)
        print('[s]       SUBPIX={}'.format(SUBPIX),          file=DBG_FILE)
        print('[g]  ORDER_GROUP={}'.format(ORDER_GROUP),     file=DBG_FILE)
        print('[t]     RUN_TEST={}'.format(RUN_TEST),        file=DBG_FILE)
        self._initWindowA()
        super().__init__(screen=self.screens[1], fullscreen=FULL_SCREEN, resizable=True, visible=False)
        self._initWindowB()
        if RUN_TEST: self._initColorLists()
        else:        self._initTabs()
        print('_init(END)'.format(), file=DBG_FILE)

    def _initWindowA(self):
        display      = pyglet.canvas.get_display()
        self.screens = display.get_screens()

    def _initWindowB(self):
        self.batch = pyglet.graphics.Batch()
        self._initGroups()
        print('_initWindowB(BGN) {}x{}'.format(self.ww, self.hh), file=DBG_FILE)
        self.set_visible()
        self.set_size(self.ww, self.hh)
        self.ww, self.hh = self.get_size()
        print('_initWindowB(END) {}x{}'.format(self.ww, self.hh), file=DBG_FILE)

    def _initGroups(self):
        for i in range(len(self.n)+1):
            pg = None if ORDER_GROUP or i==0 else self.g[i-1]
            self.g.append(self._initGroup(i, pg))
            print('_initGroups({}) g={} pg={}'.format(i, self.g[i], self.g[i].parent), file=DBG_FILE)

    @staticmethod
    def _initGroup(order=0, parent=None):
        if ORDER_GROUP: return pyglet.graphics.OrderedGroup(order, parent)
        else:           return pyglet.graphics.Group(parent)

    def _initColorLists(self):
#        self.clGroup = self._initGroup(0)
        self.colorLists = []
        n1, x1, y1, w1, h1, o1, g1 = self.geom(0, 0, 0, self.ww, self.hh, '_initColorLists(0)', init=True, dump=0)
        n2, x2, y2, w2, h2, o2, g2 = self.geom(1, 0, 0, self.ww, self.hh, '_initColorLists(1)', init=True, dump=0)
        for i in (P, L): self.dumpGeom(i, '_initColorLists() i={}'.format(i))
        c = COLOR
#        end = ['\n', ' '];        [[print('{:2} {:2} {:3} {:3} {:3} {:3}'.format(i, j, c[i][j][0], c[i][j][1], c[i][j][2], c[i][j][3]), file=DBG_FILE, end=end[0 if j==n2-1 else 1]) for j in range(n2)] for i in range(n1)]
        self.dumpSprite('')
        for i in range(n1):
            sprites = []
            for j in range(n2):
                xx, yy = x1+(w1+x1)*i, self.hh-(h2+y2)*(j+1)
                spr = self.createSprite('_initColorLists()', g1, c[i][j], xx, yy, w1, h2, i, j, v=True, no=0) #n[0], o=255)
                sprites.append(spr)
            self.colorLists.append(sprites)
        print('_initColorLists(End)', file=DBG_FILE)

    def resizeColorLists(self):
        cls = self.colorLists
        ww, hh = self.ww, self.hh
        n1, x1, y1, w1, h1, o1, g1, mx, my = self.geom(0, 0, 0, ww, hh, 'resizeColorLists(0)', init=False, dump=0)
        n2, x2, y2, w2, h2, o2, g2, mx, my = self.geom(1, 0, 0, ww, hh, 'resizeColorLists(1)', init=False, dump=0)
        for i in range(n1):
            for j in range(n2):
                xx, yy = x1+(w1+x1)*i, hh-(h2+y2)*(j+1)
                cls[i][j].update(x=xx, y=yy, scale_x=w1/self.w[P], scale_y=h2/self.h[L])
                self.dumpSprite('{:20} {:3} {:3} {:7.2f} {:7.2f} {:7.2f} {:7.2f}'.format('resizeColorLists()', i, j, xx, yy, w1, h2), cls[i][j])
        print('resizeColorLists(END) ww={} x={} w={:7.2f} x+w={:7.2f} ww-x-w={:7.2f} : y={} hh={} h={:7.2f} y+h={:7.2f} hh-y-h={:7.2f}'.format(ww, x1, w1, x1+w1, ww-x1-w1, hh, y2, h2, y2+h2, hh-y2-h2), file=DBG_FILE)

    def on_mouse_release(self, x, y, button, modifiers):  # pyglet.window.mouse.MIDDLE #pyglet.window.mouse.LEFT #pyglet.window.mouse.RIGHT
        w, h = self.ww/self.n[C], self.hh/(self.n[R]*self.n[L])
        y = self.hh-y
        c, r = int(x/w), int(y/h)
        self.i[C] = r*self.n[C]+c
        j = self.i[C]
        self.cursor.update(self.cols[j].x, self.cols[j].y)
        print('on_mouse_release({}x{}) x={:4} y={:4} w={} h={} c={:4} r={:4} j={}'.format(self.ww, self.hh, x, y, w, h, c, r, j), file=DBG_FILE)
        print('on_mouse_release({}x{}) x={:4} y={:4} w={} h={} c={:4} r={:4} j={}'.format(self.ww, self.hh, x, y, w, h, c, r, j))

    def geom(self, i, px, py, pw, ph, reason='', init=False, dump=3):
        n, x, y, w, h, o, g, = self.n[i], self.x[i], self.y[i], self.w[i], self.h[i], self.o[i], self.g[i]
        if   o==0: w, h =  pw-2*x,        (ph-y*(n+1))/n
        elif o==1: w, h = (pw-x*(n+1))/n, (ph-y*(n+1))/n
        elif o==2: w, h = pw-2*x,          ph-2*y
        elif o==3: w, h = (pw-x*(n+1))/n,  ph-2*y
        if init: self.w[i], self.h[i] = w, h
        if o!=3: x += px #; y = py+ph-y
        if dump==1 or dump==3: self.dumpGeom(i, reason)
        if dump==2 or dump==3: self.dumpSprite('')
#        print('{:70} geom() i={} px={} py={} pw={} ph={}  =>  n={} x={} y={} w={} h={} o={}'.format(' ',  i, px, py, pw, ph, n, x, y, w, h, o), file=DBG_FILE)
        if init: return n, x, y, w, h, o, g
        else:    return n, x, y, w, h, o, g, w/self.w[i], h/self.h[i]

    def dumpGeom(self, i, reason=''):
        n, x, y, w, h, g, o = self.n[i], self.x[i], self.y[i], self.w[i], self.h[i], self.g[i], self.o[i]
        print('{:25} i={} n={:3} x={:3} y={:3} w={:7.2f} h={:7.2f} o={} g={}'.format(reason, i, n, x, y, w, h, o, g), file=DBG_FILE)

    def createSprite(self, reason, grp, clr, x, y, w, h, i, j, v=None, no=0, o=255):#        img.anchor_x, img.anchor_y = fri(w/2), fri(h/2)
        scip = pyglet.image.SolidColorImagePattern(clr)
        img = scip.create_image(width=fri(w), height=fri(h))
        spr = pyglet.sprite.Sprite(img, x, y, batch=self.batch, group=grp, subpixel=SUBPIX)
        spr.visible = v if v is not None else True if i==P else False
        spr.opacity = self.getOpacity(o, j, no)
        if DBG: self.dumpSprite('{:20} {:3} {:3} {:7.2f} {:7.2f} {:7.2f} {:7.2f} {:4} {:4} {} {}'.format(reason, i, j, x, y, w, h, img.anchor_x, img.anchor_y, spr.group, spr.group.parent), spr)
        return spr

    def _initTabs(self):
        self.pages, self.lines, self.rows, self.cols = [], [], [], []
        self.dumpSprite('')
        self._initPages()
        j = self.i[C]
        self.cursor = self.createSprite('cursor', self.g[C+1], CC, self.cols[j].x, self.cols[j].y, self.cols[j].width, self.cols[j].height, 0, 0, v=True)
        self.printStructInfo('_initTabs(END)')

    def _initPages(self):
        clr = [YELLOWS[4], YELLOWS[8]]
        n, x, y, w, h, o, g = self.geom(P, self.x[P], self.y[P], self.ww, self.hh, reason='', init=True, dump=1)
        for p in range(n):
            page   = self.createSprite('_initPages', g, clr[p%len(clr)], x, y, w, h, p, 0)
            self.pages.append(page)
            if self.n[P+1] > 0: lines = self._initLines(page)
        return self.pages

    def _initLines(self, spr):
        clr = [REDS[4], REDS[8]]
        n, x, y, w, h, o, g = self.geom(L, spr.x, spr.y, spr.width, spr.height, reason='', init=True, dump=1)
        for l in range(n):
            yy = spr.y+spr.height-(h+y)*(l+1)
            line   = self.createSprite('_initLines', g, clr[l%len(clr)], x, yy, w, h, l, 0, v=True if len(self.pages)==1 else False)
            self.lines.append(line)
            if self.n[L+1] > 0: rows = self._initRows(line)
        return self.lines

    def _initRows(self, spr):
        clr = [BLUES[4], BLUES[8]]
        n, x, y, w, h, o, g = self.geom(R, spr.x, spr.y, spr.width, spr.height, reason='', init=True, dump=1)
        for r in range(n):
            yy = spr.y+spr.height-(h+y)*(r+1)
            row   = self.createSprite('_initRows', g, clr[r%len(clr)], x, yy, w, h, r, 0, v=True if len(self.pages)==1 else False)
            self.rows.append(row)
            if self.n[R+1] > 0: cols = self._initCols(row)
        return self.rows

    def _initCols(self, spr):
        clr = [GREENS[4], GREENS[8]] #        clr = GREENS[-1::-1]+GREENS
        n, x, y, w, h, o, g = self.geom(C, spr.x, spr.y, spr.width, spr.height, reason='', init=True, dump=1)
        for c in range(n):
            xx, yy = spr.x+x+(w+x)*c, spr.y+spr.height-(h+y)
            col   = self.createSprite('_initCols', g, clr[c%len(clr)], xx, yy, w, h, c, 0, v=True if len(self.pages)==1 else False)
            self.cols.append(col)
        return self.cols

    def on_resize(self, width, height):
        super().on_resize(width, height)
        self.ww, self.hh = width, height
        if RUN_TEST: self.resizeColorLists(); return
#        if DBG: self.dumpSprite('')
        for i in range(len(self.n)): self.dumpGeom(i, 'on_resize({}x{})'.format(self.ww, self.hh))
        self.resizePages()
        j = self.i[C]
        self.cursor.update(x=self.cols[j].x, y=self.cols[j].y, scale_x=self.cols[j].scale_x, scale_y=self.cols[j].scale_y)

    def resizePages(self):
        n, x, y, w, h, o, g, mx, my = self.geom(P, self.x[P], self.y[P], self.ww, self.hh, reason='', init=False, dump=0)
        for p in range(n):
            self.pages[p].update(x=x, y=y, scale_x=mx, scale_y=my)
            if DBG: self.dumpSprite('{:20} {:3} {:3} {:7.2f} {:7.2f} {:7.2f} {:7.2f}'.format('on_resize() Pages', p, 0, x, y, w, h), self.pages[p])
            if self.n[P+1] > 0: self.resizeLines(self.pages[p], p)

    def resizeLines(self, spr, pn):
        n, x, y, w, h, o, g, mx, my = self.geom(L, spr.x, spr.y, spr.width, spr.height, reason='', init=False, dump=0)
        for l in range(n):
            yy = spr.y+spr.height-(h+y)*(l+1)
            self.lines[l+pn*n].update(x=x, y=yy, scale_x=mx, scale_y=my)
            if DBG: self.dumpSprite('{:20} {:3} {:3} {:7.2f} {:7.2f} {:7.2f} {:7.2f}'.format('on_resize() Lines', l, 0, x, yy, w, h), self.lines[l+pn*n])
            if self.n[L+1] > 0: self.resizeRows(self.lines[l+pn*n], l+pn*n)

    def resizeRows(self, spr, ln):
        n, x, y, w, h, o, g, mx, my = self.geom(R, spr.x, spr.y, spr.width, spr.height, reason='', init=False, dump=0)
        for r in range(n):
            yy = spr.y+spr.height-(h+y)*(r+1)
            self.rows[r+ln*n].update(x=x, y=yy, scale_x=mx, scale_y=my)
            if DBG: self.dumpSprite('{:20} {:3} {:3} {:7.2f} {:7.2f} {:7.2f} {:7.2f}'.format('on_resize() Rows', r, 0, x, yy, w, h), self.rows[r+ln*n])
            if self.n[R+1] > 0: self.resizeCols(self.rows[r+ln*n], r+ln*n)

    def resizeCols(self, spr, rn):
        n, x, y, w, h, o, g, mx, my = self.geom(C, spr.x, spr.y, spr.width, spr.height, reason='', init=False, dump=0)
        for c in range(n):
            xx, yy = spr.x+x+(w+x)*c, spr.y+spr.height-(h+y)
            self.cols[c+rn*n].update(x=xx, y=yy, scale_x=mx, scale_y=my)
            if 1: self.dumpSprite('{:20} {:3} {:3} {:7.2f} {:7.2f} {:7.2f} {:7.2f}'.format('on_resize() Cols', c, 0, xx, yy, w, h), self.cols[c+rn*n])

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
        print('{} len(pages)={} len(lines)={} len(rows)={} len(cols)={}'.format(reason, len(self.pages), len(self.lines), len(self.rows), len(self.cols)), file=DBG_FILE)

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

    def toggleColorLists(self, motion):
        if not RUN_TEST: print('toggleColorLists(WARNING) Nothing To Toggle RUN_TEST={} motion={}'.format(RUN_TEST, motion), file=DBG_FILE); return
        cls = self.colorLists
        i = self.i[P]
        if   motion==pygwink.MOTION_LEFT:
            for j in range(len(cls[i])): cls[i][j].visible = False
            i -= 1
            i = i % len(COLOR)
            for j in range(len(cls[i])): cls[i][j].visible = True
            print('toggleColorLists() MOTION_LEFT={} i[P]={} len(cls)={}'.format(motion, i, len(cls)), file=DBG_FILE)
        elif motion==pygwink.MOTION_RIGHT:
            for j in range(len(cls[i])): cls[i][j].visible = False
            i += 1
            i = i % len(COLOR)
            for j in range(len(cls[i])): cls[i][j].visible = True
            print('toggleColorLists() MOTION_RIGHT={} i[P]={} len(cls)={}'.format(motion, i, len(cls)), file=DBG_FILE)

    def setCurrPage(self, motion):
        i = self.i[P]
        if motion==pygwink.MOTION_NEXT_PAGE:
            self.pages[self.i[P]].visible = False
            i += 1
            i = i % self.n[P]
            self.pages[self.i[P]].visible = True
            print('setCurrPage() motion={} MOTION_NEXT_PAGE i[P]={}'.format(motion, i), file=DBG_FILE)
        elif motion==pygwink.MOTION_PREVIOUS_PAGE:
            self.pages[self.i[P]].visible = False
            i -= 1
            i = i % self.n[P]
            self.pages[self.i[P]].visible = True
            print('setCurrPage() motion={} MOTION_PREVIOUS_PAGE i[P]={}'.format(motion, i), file=DBG_FILE)
        self.dumpSprite('')
        self.resizePages()

def genColors(cp, nsteps=12):
    colors, clen = [], len(cp[0])
    diffs = [cp[1][i] - cp[0][i] for i in range(clen)]
    steps = [diffs[i]/nsteps   for i in range(clen)]
    if DBG: print('genColors(), c1={} c2={} nsteps={} diffs={} steps={}'.format(cp[0], cp[1], nsteps, diffs, steps), file=DBG_FILE)
    for j in range(nsteps):
        c = tuple([fri(cp[0][i]+j*steps[i]) for i in range(len(cp[0]))])
        if DBG: print('genColors() c[{}]={}'.format(j, c), file=DBG_FILE)
        colors.append(c)
    if DBG: print('genColors() colors={}'.format(cp), file=DBG_FILE)
    return colors

if __name__ == '__main__':
    SFX         = 'TEST' if RUN_TEST else ''
    DBG_FILE    = open(sys.argv[0] + SFX + ".log.txt", 'w')
    P, L, R, C  = 0, 1, 2, 3
    VIOLET      = [(255,  64, 192, 255), (64, 16, 16, 255)]
    RED         = [(255,  32,  32, 255), (64, 16, 16, 255)]
    ORANGE      = [(255, 128,  32, 255), (64, 16, 16, 255)]
    YELLOW      = [(255, 255,  64, 255), (64, 64, 16, 255)]
    GREEN       = [( 32, 255,  32, 255), (16, 64, 16, 255)]
    GREEN_BLUE  = [( 32, 255, 208, 255), (16, 64, 32, 255)]
    CYAN        = [( 32, 255, 255, 255), (16, 64, 64, 255)]
    BLUE_GREEN  = [( 32, 208, 255, 255), (16, 32, 64, 255)]
    BLUE        = [( 32,  64, 255, 255), (16, 16, 64, 255)]
    PURPLE      = [(208,  96, 255, 255), (64, 16, 64, 255)]
    VIOLETS     = genColors(VIOLET)
    REDS        = genColors(RED)
    ORANGES     = genColors(ORANGE)
    YELLOWS     = genColors(YELLOW)
    GREENS      = genColors(GREEN)
    GREEN_BLUES = genColors(GREEN_BLUE)
    CYANS       = genColors(CYAN)
    BLUE_GREENS = genColors(BLUE_GREEN)
    BLUES       = genColors(BLUE)
    PURPLES     = genColors(PURPLE)
    COLOR       = (VIOLETS, REDS, ORANGES, YELLOWS, GREENS, GREEN_BLUES, BLUE_GREENS, BLUES, PURPLES)
    CC          = (192, 98, 39, 200)
    tabs        = Tabs()
    pyglet.app.run()
#    pyglet.image.get_buffer_manager().get_color_buffer().save('screenshot.png')
#        label = pyglet.text.Label('Hello, world', font_name='Times New Roman', font_size=36, x=self.width//2, y=self.height//2, anchor_x='center', anchor_y='center', batch=self.batch)
#        self.cols[0].image = pyglet.image.SolidColorImagePattern((199, 198, 197, 255)).create_image(width=fri(self.cols[0].width), height=fri(self.cols[0].height))
