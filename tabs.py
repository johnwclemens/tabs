import math, sys, os
import unicodedata
import pyglet
import pyglet.window.key as pygwink
import pyglet.window.event as pygwine

sys.path.insert(0, os.path.abspath('../lib'))
import cmdArgs

class Tabs(pyglet.window.Window):
    def __init__(self):
        self.fontNameIndex, self.fontColorIndex, self.fontSizeIndex, self.fontDpiIndex = 7, 0, len(FONT_SIZES)//2, len(FONT_DPIS)//2
        global FULL_SCREEN, SUBPIX, ORDER_GROUP, RUN_TEST
        self.ww, self.hh  = 1000, 600
        if RUN_TEST: self.n, self.x, self.y, self.w, self.h, self.o, self.g, self.i = [12, 12, 0, 0], [4, 0, 0, 0], [0, 3, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [1, 1, 0, 0], [], [0, 0, 0, 0]
        else:        self.n, self.x, self.y, self.w, self.h, self.o, self.g, self.i = [3, 3, 6, 40],  [0, 4, 0, 0], [0, 4, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [2, 0, 0, 3], [], [0, 0, 0, 0]
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
        self.eventLogger = pygwine.WindowEventLogger()
        self.push_handlers(self.eventLogger)
#        print('_initWindowB(END) {}x{}'.format(self.ww, self.hh), file=DBG_FILE)

    def _initGroups(self):
        for i in range(len(self.n)+3):
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
        c = COLORS
#        end = ['\n', ' '];        [[print('{:2} {:2} {:3} {:3} {:3} {:3}'.format(i, j, c[i][j][0], c[i][j][1], c[i][j][2], c[i][j][3]), file=DBG_FILE, end=end[0 if j==n2-1 else 1]) for j in range(n2)] for i in range(n1)]
        self.dumpSprite('')
        for i in range(n1):
            sprites = []
            for j in range(n2):
                xx, yy = x1+(w1+x1)*i, self.hh-(h2+y2)*(j+1)
                spr = self.createSprite('_initColorLists()', g1, c[i][j], xx, yy, w1, h2, i, j, v=True, no=0) #n[0], o=255)
                sprites.append(spr)
            self.colorLists.append(sprites)
#        print('_initColorLists(End)', file=DBG_FILE)

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
#        print('geom({}) px={:7.2f} py={:7.2f} pw={:7.2f} ph={:7.2f}  =>  n={:3} x={:4} y={:4} w={:7.2f} h={:7.2f} o={}'.format(i, px, py, pw, ph, n, x, y, w, h, o), file=DBG_FILE)
        if init: return n, x, y, w, h, o, g
        else:    return n, x, y, w, h, o, g, w/self.w[i], h/self.h[i]

    def dumpGeom(self, i, reason=''):
        n, x, y, w, h, g, o = self.n[i], self.x[i], self.y[i], self.w[i], self.h[i], self.g[i], self.o[i]
        print('{:25} i={} n={:3} x={:3} y={:3} w={:7.2f} h={:7.2f} o={} g={}'.format(reason, i, n, x, y, w, h, o, g), file=DBG_FILE)

    def createSprite(self, reason, grp, cc, x, y, w, h, i, j, v=None, no=0, o=255):#        img.anchor_x, img.anchor_y = fri(w/2), fri(h/2)
        scip = pyglet.image.SolidColorImagePattern(cc)
        img = scip.create_image(width=fri(w), height=fri(h))
        spr = pyglet.sprite.Sprite(img, x, y, batch=self.batch, group=grp, subpixel=SUBPIX)
        spr.visible = v if v is not None else True if i==P else False
        spr.color = cc[:3]
        spr.opacity = cc[-1]
        if DBG: self.dumpSprite('{:20} {:3} {:3} {:7.2f} {:7.2f} {:7.2f} {:7.2f} {:4} {:4} {} {}'.format(reason, i, j, x, y, w, h, img.anchor_x, img.anchor_y, spr.group, spr.group.parent), spr)
        return spr

    @staticmethod
    def dumpSprite(reason, s=None):
        if s is None: print('    x       y       w       h    iax  iay    m      mx     my     rot   opacity    color    visible     reason         i   j      x       y       w       h    iax  iay', file=DBG_FILE); return
        f = '{:7.2f} {:7.2f} {:7.2f} {:7.2f} {:4} {:4} {:6.3f} {:6.3f} {:6.3f} {:7.2f}  {:4}  ({:3}, {:3}, {:3})  {:1}'
        c = s.color
        fs = f.format(s.x, s.y, s.width, s.height, s.image.anchor_x, s.image.anchor_y, s.scale, s.scale_x, s.scale_y, s.rotation, s.opacity, c[0], c[1], c[2], s.visible)
        print('{} {}'.format(fs, reason), file=DBG_FILE)
        assert(type(s) == pyglet.sprite.Sprite)

    def _initTabs(self):
        self.pages, self.lines, self.rows, self.cols, self.texts = [], [], [], [], []
        self.dumpSprite('')
        c, n = self.i[C], self.n[C]
        self._initPages()
#        self._initTextTest(n)
        self._initCursor(self.cols, c, self.g[C+1])
#        self._initCaret()
        self.printStructInfo('_initTabs(END)')

    def _initTextTest(self, n):
        self._initText(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'], self.cols, 0, self.g[C+2], self.batch)
        self._initText(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25'], self.cols, n, self.g[C+2], self.batch)
        self._initText(['~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '[', ']', '<', '>', '/', '?', ',', '.', '=', '_', '+', ' ', '|', '{', '}', '-', '\\'], self.cols, 2*n, self.g[C+2], self.batch)
        ucnFlat, ucnNatural, ucnSharp = unicodedata.name('\u066D'), unicodedata.name('\u166E'), unicodedata.name('\u366F')
        ucnAsterisk = 'ASTERISK'
        ucAsterisk = unicodedata.lookup(ucnAsterisk)
#        ucFlat,  ucNatural,  ucSharp  = unicodedata.lookup(ucnFlat), unicodedata.lookup(ucnNatural), unicodedata.lookup(ucnSharp)
#        ucFlat,  ucNatural,  ucSharp  = unicodedata.lookup('MUSIC FLAT SIGN'), unicodedata.lookup('MUSIC NATURAL SIGN'), unicodedata.lookup('MUSIC SHARP SIGN')
        print('ucnAsterisk={}'.format(ucnAsterisk), file=DBG_FILE)
        print('    ucnFlat={}'.format(ucnFlat), file=DBG_FILE)
        print(' ucnNatural={}'.format(ucnNatural), file=DBG_FILE)
        print('   ucnSharp={}'.format(ucnSharp), file=DBG_FILE)
        print(' ucAsterisk={}'.format(ucAsterisk), file=DBG_FILE)
#        print('     ucFlat={}'.format(ucFlat),      file=DBG_FILE)
#        print('  ucNatural={}'.format(ucNatural),   file=DBG_FILE)
#        print('    ucSharp={}'.format(ucSharp),     file=DBG_FILE)
        self._initText([ucAsterisk], self.cols, 3*n, self.g[C+2], self.batch)
#        self._initText([ucFlat],     self.cols, 4*n, self.g[C+2], self.batch)
#        self._initText([ucNatural],  self.cols, 5*n, self.g[C+2], self.batch)
#        self._initText([ucSharp],    self.cols, 6*n, self.g[C+2], self.batch)
#        self._initText([' ', ' ', ' ', ' ', 'Copywrite{#x266D}'], (255, 0, 0, 255), self.cols, 3*n, self.g[C+2], self.batch) # Unicode seems to require a Document?
#        self._initText([' ', ' ', ' ', ' ', 'Copywrite{#x266F}'], (255, 0, 0, 255), self.cols, 4*n, self.g[C+2], self.batch)

    def _initCaret(self):
        doc = pyglet.text.document.UnformattedDocument()
        w, h, b, g = self.cols[0].width, self.cols[0].height, self.batch, self.g[C+3]
        layout = pyglet.text.layout.IncrementalTextLayout(document=doc, width=w, height=h, batch=b, group=g)
        self.caret = pyglet.text.caret.Caret(layout, batch=self.batch, color=(200, 255, 200))

    def _initCursor(self, cols, c, g):
        self.i[C] = c
        x, y, w, h = cols[c].x, cols[c].y, cols[c].width, cols[c].height
        self.cursor = self.createSprite('cursor', g, CC, x, y, w, h, 0, 0, v=True)
        print('_initCursor() c={:4} x={:6.1f} y={:6.1f} w={:4} h={:4}'.format(c, x, y, w, h), file=DBG_FILE)

    def _initText(self, text, cols, c, g, b):
        w,  h,  t   = cols[c].width, cols[c].height, []
        fc, dpi, fs, fn = self.fontInfo()
        print('_initText( {} ) c={:4}'.format(text, c), file=DBG_FILE)
        for i in range(len(text)):
#            dpi = FONT_DPIS[i%len(FONT_DPIS)]
            x, y = cols[c+i].x, cols[c+i].y
            t.append(pyglet.text.Label(text[i], font_name=fn, font_size=fs, color=fc, x=x+w/2, y=y+h/2, anchor_x='center', anchor_y='center', align='center', dpi=dpi, batch=b, group=g))
            print('_initText( {} ) c={:4} x={:6.1f} y={:6.1f} w={:4} h={:4}'.format(text[i], c, x, y, w, h), file=DBG_FILE)
        self.texts.append(t)

    def _initPages(self):
        cc = [REDS[0], REDS[2], REDS[4], REDS[6], REDS[8], REDS[10]]
        n, x, y, w, h, o, g = self.geom(P, self.x[P], self.y[P], self.ww, self.hh, reason='', init=True, dump=0)
        for p in range(n):
            page = self.createSprite('_initPages', g, cc[p%len(cc)], x, y, w, h, p, 0)
            self.pages.append(page)
            if self.n[P+1] > 0: lines = self._initLines(page)
        return self.pages

    def _initLines(self, spr):
        cc = [CYANS[0], CYANS[5]]
        n, x, y, w, h, o, g = self.geom(L, spr.x, spr.y, spr.width, spr.height, reason='', init=True, dump=0)
        for l in range(n):
            yy = spr.y+spr.height-(h+y)*(l+1)
            line   = self.createSprite('_initLines', g, cc[l%len(cc)], x, yy, w, h, l, 0, v=True if len(self.pages)==1 else False)
            self.lines.append(line)
            if self.n[L+1] > 0: rows = self._initRows(line)
        return self.lines

    def _initRows(self, spr):
        cc = [YELLOWS[0], YELLOWS[5]]
        n, x, y, w, h, o, g = self.geom(R, spr.x, spr.y, spr.width, spr.height, reason='', init=True, dump=0)
        for r in range(n):
            yy = spr.y+spr.height-(h+y)*(r+1)
            row   = self.createSprite('_initRows', g, cc[r%len(cc)], x, yy, w, h, r, 0, v=True if len(self.pages)==1 else False)
            self.rows.append(row)
            if self.n[R+1] > 0: cols = self._initCols(row)
        return self.rows

    def _initCols(self, spr):
#        a, b = 6, 3; cc = [GREENS[a], GREENS[b]] if len(self.rows)%2 else [GREENS[b], GREENS[a]]
        a, b = 11, 8; cc = [GRAYS[a], GRAYS[b]] if len(self.rows)%2 else [GRAYS[b], GRAYS[a]]
        (n, x, y, w, h, o, g), s = self.geom(C, spr.x, spr.y, spr.width, spr.height, reason='', init=True, dump=0), len(cc)
        for c in range(n):
            xx, yy = spr.x+x+(w+x)*c, spr.y+spr.height-(h+y)
            col   = self.createSprite('_initCols', g, cc[c%s], xx, yy, w, h, c, 0, v=True if len(self.pages)==1 else False)
            self.cols.append(col)
        return self.cols

    def on_resize(self, width, height):
        super().on_resize(width, height)
        self.ww, self.hh = width, height
        if RUN_TEST: self.resizeColorLists(); return
#        if DBG: self.dumpSprite('')
        for i in range(len(self.n)): self.dumpGeom(i, 'on_resize({}x{})'.format(self.ww, self.hh))
        c = self.i[C]
        self.resizePages()
        for j in range(len(self.texts)):
            self.resizeText(self.texts[j], self.cols, c)
            c += self.n[C]
        self.resizeCursor(self.cols, c)
        self.updateCaption()

    def resizeCursor(self, cols, c):
        x, y, w, h = cols[c].x, cols[c].y, cols[c].width, cols[c].height
        self.cursor.update(x=x, y=y, scale_x=cols[c].scale_x, scale_y=cols[c].scale_y)
        print('resizeCursor() c={:4} x={:6.1f} y={:6.1f} w={:4} h={:4}'.format(c, x, y, w, h), file=DBG_FILE)

    @staticmethod
    def resizeText(text, cols, c):
        w, h = cols[c].width, cols[c].height
        for i in range(len(text)):
#            text[i].layout #dpi = FONT_DPIS[i%len(FONT_DPIS)]
            x, y = cols[c+i].x, cols[c+i].y
            text[i].x, text[i].y = x+w/2, y+h/2
            print('resizeText( {} ) c={:4} x={:6.1f} y={:6.1f} w={:4} h={:4}'.format(text[i].text, c, x, y, w, h), file=DBG_FILE)

    def resizePages(self):
        n, x, y, w, h, o, g, mx, my = self.geom(P, self.x[P], self.y[P], self.ww, self.hh, reason='', init=False, dump=0)
        for p in range(n):
            self.pages[p].update(x=x, y=y, scale_x=mx, scale_y=my)
            if DBG: self.dumpSprite('{:20} {:3} {:3} {:7.2f} {:7.2f} {:7.2f} {:7.2f}'.format('on_resize Pages', p, 0, x, y, w, h), self.pages[p])
            if self.n[P+1] > 0: self.resizeLines(self.pages[p], p)

    def resizeLines(self, spr, pn):
        n, x, y, w, h, o, g, mx, my = self.geom(L, spr.x, spr.y, spr.width, spr.height, reason='', init=False, dump=0)
        for l in range(n):
            yy = spr.y+spr.height-(h+y)*(l+1)
            self.lines[l+pn*n].update(x=x, y=yy, scale_x=mx, scale_y=my)
            if DBG: self.dumpSprite('{:20} {:3} {:3} {:7.2f} {:7.2f} {:7.2f} {:7.2f}'.format('on_resize Lines', l, 0, x, yy, w, h), self.lines[l+pn*n])
            if self.n[L+1] > 0: self.resizeRows(self.lines[l+pn*n], l+pn*n)

    def resizeRows(self, spr, ln):
        n, x, y, w, h, o, g, mx, my = self.geom(R, spr.x, spr.y, spr.width, spr.height, reason='', init=False, dump=0)
        for r in range(n):
            yy = spr.y+spr.height-(h+y)*(r+1)
            self.rows[r+ln*n].update(x=x, y=yy, scale_x=mx, scale_y=my)
            if DBG: self.dumpSprite('{:20} {:3} {:3} {:7.2f} {:7.2f} {:7.2f} {:7.2f}'.format('on_resize Rows', r, 0, x, yy, w, h), self.rows[r+ln*n])
            if self.n[R+1] > 0: self.resizeCols(self.rows[r+ln*n], r+ln*n)

    def resizeCols(self, spr, rn):
        n, x, y, w, h, o, g, mx, my = self.geom(C, spr.x, spr.y, spr.width, spr.height, reason='', init=False, dump=0)
        for c in range(n):
            xx, yy = spr.x+x+(w+x)*c, spr.y+spr.height-(h+y)
            self.cols[c+rn*n].update(x=xx, y=yy, scale_x=mx, scale_y=my)
            if DBG: self.dumpSprite('{:20} {:3} {:3} {:7.2f} {:7.2f} {:7.2f} {:7.2f}'.format('on_resize Cols', c, 0, xx, yy, w, h), self.cols[c+rn*n])

    def printStructInfo(self, reason=''):
        print('{} len(pages)={} len(lines)={} len(rows)={} len(cols)={}'.format(reason, len(self.pages), len(self.lines), len(self.rows), len(self.cols)), file=DBG_FILE)

    def on_draw(self):
        self.clear()
        self.batch.draw()

    def on_key_press(self, symbol, modifiers):
        self.symbol, self.modifiers = symbol, modifiers
        symStr, modStr = pygwink.symbol_string(symbol), pygwink.modifiers_string(modifiers)
        print('on_key_press() {:5} {:12} {} {:12}'.format(symbol, symStr, modifiers, modStr), file=DBG_FILE)
#        print('on_key_press() symbol={} modifiers={}'.format(symbol, modifiers), file=DBG_FILE)

    def on_text(self, text):
        mods = self.modifiers
        print('on_text() text={}'.format(text), file=DBG_FILE)
        if   'A' <= text <= 'G' and mods & pygwink.MOD_SHIFT: self._initText([text], self.cols, self.i[C], self.g[C+2], self.batch)
        elif text == '$': pyglet.image.get_buffer_manager().get_color_buffer().save('screenshot.png')
        elif text == 'c' and mods & pygwink.MOD_CTRL: self.nextFontColor(self.fontColorIndex, text)
        elif text == 'C' and mods & pygwink.MOD_CTRL: self.prevFontColor(self.fontColorIndex, text)
        elif text == 'd': self.nextFontDpi(self.fontDpiIndex, text)
        elif text == 'D': self.prevFontDpi(self.fontDpiIndex, text)
        else:             print('on_text() text={} ???'.format(text), file=DBG_FILE)
        self.updateCaption()

    def nextFontColor(self, i, text):
        self.updateFontColor(i+1, 'nextFontColor() {}=c'.format(text))

    def prevFontColor(self, i, text):
        self.updateFontColor(i-1, 'prevFontColor() {}=c'.format(text))

    def updateFontColor(self, i, reason):
        i = i % len(FONT_COLORS)
        print('{} FONT_COLORS[{}]={}'.format(reason, i, FONT_COLORS[i]), file=DBG_FILE)
        for j in range(len(self.texts)):
            for k in range(len(self.texts[j])):
                self.texts[j][k].color = FONT_COLORS[i]
        self.fontColorIndex = i

    def nextFontDpi(self, i, text):
        self.updateFontDpi(i+1, 'nextFontDpi() {}=d   '.format(text))

    def prevFontDpi(self, i, text):
        self.updateFontDpi(i-1, 'prevFontDpi() {}=D   '.format(text))

    def updateFontDpi(self, i, reason):
        i = i % len(FONT_DPIS)
        print('{} FONT_DPIS[{}]={}'.format(reason, i, FONT_DPIS[i]), file=DBG_FILE)
        for j in range(len(self.texts)):
            for k in range(len(self.texts[j])):
                self.texts[j][k].dpi = FONT_DPIS[i]
        self.fontDpiIndex = i

    def on_text_motion(self, motion):
        print('on_text_motion(BGN) motion={}'.format(motion), file=DBG_FILE)
        if self.modifiers == 0:
            if motion==pygwink.MOTION_RIGHT:             self.moveRight()
#            if   motion == pygwink.MOTION_LEFT:          self.prevFontName(self.fontNameIndex, motion)
#            elif motion == pygwink.MOTION_RIGHT:         self.nextFontName(self.fontNameIndex, motion)
#            elif motion == pygwink.MOTION_DOWN:          self.prevFontSize(self.fontSizeIndex, motion)
#            elif motion == pygwink.MOTION_UP:            self.nextFontSize(self.fontSizeIndex, motion)
#            elif motion == pygwink.MOTION_PREVIOUS_PAGE: self.prevPage(    self.i[P],          motion)
#            elif motion == pygwink.MOTION_NEXT_PAGE:     self.nextPage(    self.i[P],          motion)
            else:                                        print('on_text_motion() motion={} ???'.format(motion), file=DBG_FILE)
            self.updateCaption()

    def moveRight(self):
        cols, c = self.cols, self.i[C]+1
        x, y, w, h = cols[c].x, cols[c].y, cols[c].width, cols[c].height
        self.cursor.update(x=x, y=y, scale_x=cols[c].scale_x, scale_y=cols[c].scale_y)
        self.i[C] = c

    def fontInfo(self):
        return FONT_COLORS[self.fontColorIndex], FONT_DPIS[self.fontDpiIndex], FONT_SIZES[self.fontSizeIndex], FONT_NAMES[self.fontNameIndex]

    def updateCaption(self):
#        for fi in self.fontInfo():
#            text += 'updateCaption() fi={}'.format(fi)
#        self.set_caption('{} {}dpi {}pt {}'.format(fc, fd, fs, fn))
        print('{}'.format(i) for i in range(len(self.fontInfo())))
#        fc, fd, fs, fn = self.fontInfo()
#        self.set_caption('{} {}dpi {}pt {}'.format(fc, fd, fs, fn))

    def nextFontName(self, i, motion):
        self.updateFontName(i+1, 'nextFontName() {}=MOTION_RIGHT'.format(motion))

    def prevFontName(self, i, motion):
        self.updateFontName(i-1, 'prevFontName() {}=MOTION_LEFT '.format(motion))

    def updateFontName(self, i, reason):
        i = i % len(FONT_NAMES)
        print('{} FONT_NAMES[{}]={}'.format(reason, i, FONT_NAMES[i]), file=DBG_FILE)
        for j in range(len(self.texts)):
            for k in range(len(self.texts[j])):
                self.texts[j][k].font_name = FONT_NAMES[i]
        self.fontNameIndex = i

    def nextFontSize(self, i, motion):
        self.updateFontSize(i+1, 'nextFontSize() {}=MOTION_UP   '.format(motion))

    def prevFontSize(self, i, motion):
        self.updateFontSize(i-1, 'prevFontSize() {}=MOTION_DOWN '.format(motion))

    def updateFontSize(self, i, reason):
        i = i % len(FONT_SIZES)
        print('{} FONT_SIZES[{}]={}'.format(reason, i, FONT_SIZES[i]), file=DBG_FILE)
        for j in range(len(self.texts)):
            for k in range(len(self.texts[j])):
                self.texts[j][k].font_size = FONT_SIZES[i]
        self.fontSizeIndex = i

    def nextPage(self, i, motion):
        self.pages[i].visible = False
        self.updatePage(i+1, 'nextPage() {}=MOTION_NEXT_PAGE   '.format(motion))

    def prevPage(self, i, motion):
        self.pages[i].visible = False
        self.updatePage(i-1, 'prevPage() {}=MOTION_PREVIOUS_PAGE'.format(motion))

    def updatePage(self, i, reason):
        i = i % self.n[P]
        self.pages[i].visible = True
        print('{} i[{}]={}'.format(reason, P, i), file=DBG_FILE)
        self.i[P] = i

    def on_mouse_release(self, x, y, button, modifiers):  # pyglet.window.mouse.MIDDLE #pyglet.window.mouse.LEFT #pyglet.window.mouse.RIGHT
        w, h = self.ww/self.n[C], self.hh/(self.n[R]*self.n[L])
        y = self.hh-y
        c, r = int(x/w), int(y/h)
        self.i[C] = r*self.n[C]+c
        j = self.i[C]
        self.cursor.update(self.cols[j].x, self.cols[j].y)
        print('on_mouse_release({}x{}) x={:4} y={:4} w={} h={} c={:4} r={:4} j={}'.format(self.ww, self.hh, x, y, w, h, c, r, j), file=DBG_FILE)

    def toggleColorLists(self, motion):
        if not RUN_TEST: print('toggleColorLists(WARNING) Nothing To Toggle RUN_TEST={} motion={}'.format(RUN_TEST, motion), file=DBG_FILE); return
        cls = self.colorLists
        i = self.i[P]
        print('toggleColorLists() i={}'.format(i), file=DBG_FILE)
        if motion==pygwink.MOTION_LEFT:
            for j in range(len(cls[i])): cls[i][j].visible = False
            i -= 1
            i = i%len(COLORS)
            for j in range(len(cls[i])): cls[i][j].visible = True
            print('toggleColorLists() MOTION_LEFT={} i[P]={} len(cls)={}'.format(motion, i, len(cls)), file=DBG_FILE)
        elif motion==pygwink.MOTION_RIGHT:
            for j in range(len(cls[i])): cls[i][j].visible = False
            i += 1
            i = i%len(COLORS)
            for j in range(len(cls[i])): cls[i][j].visible = True
            print('toggleColorLists() MOTION_RIGHT={} i[P]={} len(cls)={}'.format(motion, i, len(cls)), file=DBG_FILE)
        self.i[P] = i

if __name__=='__main__':
    def fri(f): return int(math.floor(f+0.5))
    RUN_TEST = False;  ORDER_GROUP = True;  SUBPIX = False;  FULL_SCREEN = False;  DBG = False
    SFX          = 'TEST' if RUN_TEST else ''
    DBG_FILE     = open(sys.argv[0] + SFX + ".log.txt", 'w')
    P, L, R, C   = 0, 1, 2, 3
    OPACITY      = [255, 240, 225, 210, 190, 165, 140, 110, 80]
    GRAY         = [(255, 255, 255, OPACITY[0]), ( 0,  0,  0, OPACITY[0])]
    PINK         = [(255,  64, 192, OPACITY[1]), (57, 16, 16, OPACITY[1])]
    INFRA_RED    = [(255,  29,  24, OPACITY[5]), (68, 20, 19, OPACITY[5])]
    RED          = [(255,  24,  21, OPACITY[2]), (72, 15, 12, OPACITY[2])]
    ORANGE       = [(255, 128,  32, OPACITY[1]), (76, 30, 25, OPACITY[0])]
    YELLOW       = [(255, 255,  15, OPACITY[0]), (45, 41, 10, OPACITY[0])]
    GREEN        = [( 44, 255,   0, OPACITY[1]), (21, 54, 10, OPACITY[1])]
    GREEN_BLUE   = [( 24, 255,  61, OPACITY[5]), (10, 49, 25, OPACITY[3])]
    CYAN         = [( 32, 255, 255, OPACITY[1]), (16, 64, 64, OPACITY[2])]
    BLUE_GREEN   = [( 25, 181, 255, OPACITY[2]), (12, 37, 51, OPACITY[2])]
    BLUE         = [( 35,  26, 255, OPACITY[7]), (19, 11, 64, OPACITY[7])]
    ULTRA_VIOLET = [(176,  81, 255, OPACITY[7]), (44, 14, 58, OPACITY[5])]
    VIOLET       = [(194,  96, 255, OPACITY[5]), (50, 19, 61, OPACITY[4])]
    HUES         = 13
    def genColors(cp, nsteps=HUES):
        colors, clen = [], len(cp[0])
        diffs = [cp[1][i] - cp[0][i] for i in range(clen)]
        steps = [diffs[i]/nsteps     for i in range(clen)]
        if DBG: print('genColors(), c1={} c2={} nsteps={} diffs={} steps={}'.format(cp[0], cp[1], nsteps, diffs, steps), file=DBG_FILE)
        for j in range(nsteps):
            c = tuple([fri(cp[0][i]+j*steps[i]) for i in range(len(cp[0]))])
            if DBG: print('genColors() c[{}]={}'.format(j, c), file=DBG_FILE)
            colors.append(c)
        if DBG: print('genColors() colors={}'.format(cp), file=DBG_FILE)
        return colors
    GRAYS       = genColors(GRAY)
    PINKS       = genColors(PINK)
    INFRA_REDS  = genColors(INFRA_RED)
    REDS        = genColors(RED)
    ORANGES     = genColors(ORANGE)
    YELLOWS     = genColors(YELLOW)
    GREENS      = genColors(GREEN)
    GREEN_BLUES = genColors(GREEN_BLUE)
    CYANS       = genColors(CYAN)
    BLUE_GREENS = genColors(BLUE_GREEN)
    BLUES       = genColors(BLUE)
    ULTRA_VIOLETS = genColors(ULTRA_VIOLET)
    VIOLETS     = genColors(VIOLET)
    COLORS      = (PINKS, INFRA_REDS, REDS, ORANGES, YELLOWS, GRAYS, GREENS, GREEN_BLUES, CYANS, BLUE_GREENS, BLUES, VIOLETS, ULTRA_VIOLETS)
    CC          = (255, 190, 12, 176)
    FONT_NAMES  = ['Times New Roman', 'Lucida Console', 'Courier New', 'Helvetica', 'Arial', 'Century Gothic', 'Bookman Old Style', 'Antique Olive']
    FONT_SIZES  = [6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36]
    FONT_COLORS = [REDS[0], GREENS[0], BLUES[0], YELLOWS[0], ORANGES[0], GREEN_BLUES[0], CYANS[0], BLUE_GREENS[0], PINKS[0], INFRA_REDS[0], VIOLETS[0], ULTRA_VIOLETS[0], GRAYS[0]]
    FONT_DPIS    = [75, 80, 90, 96, 100, 108, 116]
    tabs        = Tabs()
    pyglet.app.run()
#        cc = GREENS[-1::-1]+GREENS
