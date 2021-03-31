import inspect, math, sys, os, glob, pathlib#, shutil#, unicodedata
import pyglet
import pyglet.window.key as pygwink
import pyglet.window.event as pygwine
sys.path.insert(0, os.path.abspath('../lib'))
import cmdArgs

class Tabs(pyglet.window.Window):
    def __init__(self):
        global FULL_SCREEN, SUBPIX, ORDER_GROUP
        SNAP_GLOB_ARG = str(BASE_PATH / SNAP_DIR / BASE_NAME) + SFX + '.*' + SNAP_SFX
        FILE_GLOB     = glob.glob(SNAP_GLOB_ARG)
        self.log('(BGN) VRSN={} VRSNX=({}) {}'.format(VRSN, VRSNX, Tabs))
        self.log('globPathArg={}'.format(SNAP_GLOB_ARG))
        for _F in FILE_GLOB:
            self.log('{}  {}'.format(os.path.basename(_F), _F), ind=0)
            pathlib.Path(_F).unlink()
        self.ww, self.hh  = 640, 480
        self.n, self.i, self.x, self.y, self.w, self.h, self.o, self.g = [12, 12, 0, 0], [0, 0, 0, 0], [4, 0, 0, 0], [0, 3, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [1, 1, 0, 0], []
        self.argMap = cmdArgs.parseCmdLine(dbg=1)
        if 'n' in self.argMap and len(self.argMap['n'])  > 0: self.n            = [int(self.argMap['n'][i]) for i in range(len(self.argMap['n']))]
        if 'i' in self.argMap and len(self.argMap['i'])  > 0: self.i            = [int(self.argMap['i'][i]) for i in range(len(self.argMap['i']))]
        if 'x' in self.argMap and len(self.argMap['x'])  > 0: self.x            = [int(self.argMap['x'][i]) for i in range(len(self.argMap['x']))]
        if 'y' in self.argMap and len(self.argMap['y'])  > 0: self.y            = [int(self.argMap['y'][i]) for i in range(len(self.argMap['y']))]
        if 'w' in self.argMap and len(self.argMap['w'])  > 0: self.ww           =  int(self.argMap['w'][0])
        if 'h' in self.argMap and len(self.argMap['h'])  > 0: self.hh           =  int(self.argMap['h'][0])
        if 'o' in self.argMap and len(self.argMap['o'])  > 0: self.o            = [int(self.argMap['o'][i]) for i in range(len(self.argMap['o']))]
        if 'f' in self.argMap and len(self.argMap['f']) == 0: FULL_SCREEN       = 1
        if 'g' in self.argMap and len(self.argMap['g']) == 0: ORDER_GROUP       = 1
        if 's' in self.argMap and len(self.argMap['s']) == 0: SUBPIX            = 1
#        if 't' in self.argMap and len(self.argMap['t']) == 0: TEST              = 1
        self.log('[n]            n={}'.format(self.n))
        self.log('[i]            i={}'.format(self.i))
        self.log('[x]            x={}'.format(self.x))
        self.log('[y]            y={}'.format(self.y))
        self.log('[w]           ww={}'.format(self.ww))
        self.log('[h]           hh={}'.format(self.hh))
        self.log('[o]            o={}'.format(self.o))
        self.log('[f]  FULL_SCREEN={}'.format(FULL_SCREEN))
        self.log('[g]  ORDER_GROUP={}'.format(ORDER_GROUP))
        self.log('[s]       SUBPIX={}'.format(SUBPIX))
#        self.log('[t]         TEST={}'.format(TEST))
        if len(self.n) == K: self.n.append(self.n[C] + CCC)  ;  self.log('[n] +=n[C]+CCC n={}'.format(self.n))
        self._initWindowA()
        super().__init__(screen=self.screens[1], fullscreen=FULL_SCREEN, resizable=True, visible=False)
        self._initWindowB()
        self.symb, self.symbStr, self.mods, self.modsStr, self.kbk = 0, '', 0, '', 0
        self.ci = 0
        self.cursor, self.caret = None, None
        self.data, self.sprites, self.blankCol = [], [], ''
        self._initTestColors()
        self.log('(END) VRSN={} VRSNX=({}) {}'.format(VRSN, VRSNX, Tabs))
        text = '\n' + '###   __init__   ###' * 18 + '\n'
        self.log(text, ind=0)

    def _initWindowA(self, dbg=1):
        if dbg: self.log('(BGN) wxh={}x{}'.format(self.ww, self.hh))
        display      = pyglet.canvas.get_display()
        self.screens = display.get_screens()
        if dbg: self.log('(END) display={} screens={}'.format(display, self.screens))

    def _initWindowB(self, dbg=1):
        self.batch = pyglet.graphics.Batch()
        self._initGroups()
        if dbg: self.log('(BGN) wxh={}x{}'.format(self.ww, self.hh))
        self.set_visible()
        if not FULL_SCREEN: self.set_size(self.ww, self.hh)
        self.ww, self.hh = self.get_size()
        self.eventLogger = pygwine.WindowEventLogger()
        self.push_handlers(self.eventLogger)
        if dbg: self.log('(END) wxh={}x{}'.format(self.ww, self.hh))
########################################################################################################################################################################################################
    def _initGroups(self):
        for i in range(len(self.n)+3):
            p = None if ORDER_GROUP or i==0 else self.g[i-1]
            self.g.append(self._initGroup(i, p))
            self.log('({}) g={} pg={}'.format(i, self.g[i], self.g[i].parent))

    @staticmethod
    def _initGroup(order=0, parent=None):
        return pyglet.graphics.OrderedGroup(order, parent) if ORDER_GROUP else pyglet.graphics.Group(parent)
#        if ORDER_GROUP: return pyglet.graphics.OrderedGroup(order, parent)
#        else:           return pyglet.graphics.Group(parent)

#    def geom_NEW(self, j, p, why='', init=False, dbg=0):
    def geom(self, j, px, py, pw, ph, why='', init=False, dump=3, dbg=0):
        nq = self.n[Q]
        n, i, x, y, w, h, o , g = self.n[j], self.i[j], self.x[j], self.y[j], self.w[j], self.h[j], self.o[j], self.g[j]
        if   nq and j == Q: n = self.n[R] + 1
        elif nq and j == R: n += 1
        elif j == C: n += CCC
        if   o == 0: w, h =  pw - x*2,          (ph - y*(n + 1))/n
        elif o == 1: w, h = (pw - x*(n + 1))/n, (ph - y*(n + 1))/n
        elif o == 2: w, h =  pw - x*2,           ph - y*2
        elif o == 3: w, h = (pw - x*(n + 1))/n,  ph - y*2
        if init: self.w[j], self.h[j] = w, h
        if o != 3: x += px #; y = py+ph-y
        if dump == 2 or dump == 3: self.dumpSprite()
        if dump == 1 or dump == 3: self.dumpGeom(j, why)
        if dbg: self.log('geom({}) px={:7.2f} py={:7.2f} pw={:7.2f} ph={:7.2f}  =>  n={:3} x={:4} y={:4} w={:7.2f} h={:7.2f} o={}'.format(j, px, py, pw, ph, n, x, y, w, h, o))
        if nq and j == Q: n = nq
        if init: return n, i, x, y, w, h, o, g
        else:    return n, i, x, y, w, h, o, g, w/self.w[j], h/self.h[j]

    def dumpGeom(self, j, why=''):
        n, i, x, y, w, h, o , g = self.n[j], self.i[j], self.x[j], self.y[j], self.w[j], self.h[j], self.o[j], self.g[j]
        self.log('{:25} j={} n={:3} i={:4} x={:3} y={:3} w={:7.2f} h={:7.2f} o={} g={}'.format(why, j, n, i, x, y, w, h, o, g))

    def _initTestColors(self):
#        self.clGroup = self._initGroup(0)
        self.colorLists = []
        n1, i1, x1, y1, w1, h1, o1, g1 = self.geom(0, 0, 0, self.ww, self.hh, '_initTestColors(0)', init=True, dump=0)
        n2, i2, x2, y2, w2, h2, o2, g2 = self.geom(1, 0, 0, self.ww, self.hh, '_initTestColors(1)', init=True, dump=0)
        for i in (P, L): self.dumpGeom(i, '_initTestColors() i={}'.format(i))
        c = COLORS
#        self.dumpSprite()
        for i in range(n1):
            sprites = []
            for j in range(n2):
                xx, yy = x1+(w1+x1)*i, self.hh-(h2+y2)*(j+1)
                self.createSprite(sprites, g1, c[i][j], xx, yy, w1, h2, i, j, v=True)
            self.colorLists.append(sprites)

    def resizeTestColors(self):
        cls = self.colorLists
        ww, hh = self.ww, self.hh
        n1, i1, x1, y1, w1, h1, o1, g1, mx, my = self.geom(0, 0, 0, ww, hh, 'resizeTestColors(0)', init=False, dump=0)
        n2, i2, x2, y2, w2, h2, o2, g2, mx, my = self.geom(1, 0, 0, ww, hh, 'resizeTestColors(1)', init=False, dump=0)
        for i in range(n1):
            for j in range(n2):
                xx, yy = x1+(w1+x1)*i, hh-(h2+y2)*(j+1)
                cls[i][j].update(x=xx, y=yy, scale_x=w1/self.w[P], scale_y=h2/self.h[L])
                self.dumpSprite(cls[i][j], i*n2+j, '{:20} {:3} {:3} {:7.2f} {:7.2f} {:7.2f} {:7.2f}'.format('resizeTestColors()', i, j, xx, yy, w1, h2))
        self.log('(END) ww={} x={} w={:7.2f} x+w={:7.2f} ww-x-w={:7.2f} : y={} hh={} h={:7.2f} y+h={:7.2f} hh-y-h={:7.2f}'.format(ww, x1, w1, x1+w1, ww-x1-w1, hh, y2, h2, y2+h2, hh-y2-h2))

    def createSprite(self, ps, grp, cc, x, y, w, h, i, j=0, v=None):
        scip = pyglet.image.SolidColorImagePattern(cc)
        img = scip.create_image(width=fri(w), height=fri(h))
        spr = pyglet.sprite.Sprite(img, x, y, batch=self.batch, group=grp, subpixel=SUBPIX)
        spr.visible = v if v else True if i == P else False
        spr.color, spr.opacity = cc[:3], cc[3]
        self.sprites.append(spr)
        if ps is not None: ps.append(spr)
########################################################################################################################################################################################################
    def resizeSprites(self, dbg=0):
        n = self.n
        self.log('(BGN) n={}'.format(n))
        if dbg: self.dumpSprite()
        i, sp, sl, sq, sr, sc = 0, 0, 0, 0, 0, 0
        np, ip, xp, yp, wp, hp, op, gp, mxp, myp = self.geom(P, self.x[P], self.y[P], self.ww, self.hh, why='', init=False, dump=0)
        for p in range(np):
            page = self.pages[sp]   ;            page.update(x=xp, y=yp, scale_x=mxp, scale_y=myp)   ;  sp += 1
            if dbg: self.dumpSprite(self.sprites[i], i + 1, '{:2} {:2} {:2} {:3} {:5} {:16}'.format(sp, sl, sq, sr, sc, 'resizePages'))                 ; i += 1
            nl, il, xl, yl, wl, hl, ol, gl, mxl, myl = self.geom(L, page.x, page.y, page.width, page.height, why='', init=False, dump=0)
            for l in range(nl):
                yyl = page.y + page.height - (hl + yl) * (l + 1)
                line = self.lines[sl]   ;        line.update(x=xl, y=yyl, scale_x=mxl, scale_y=myl)  ;  sl += 1
                if dbg: self.dumpSprite(self.sprites[i], i + 1, '{:2} {:2} {:2} {:3} {:5} {:16}'.format(sp, sl, sq, sr, sc, 'resizeLines'))             ;  i += 1
                if n[Q]:
                    nq, iq, xq, yq, wq, hq, oq, gq, mxq, myq = self.geom(Q, line.x, line.y, line.width, line.height, why='', init=False, dump=0)
                    for q in range(nq):
                        yyq = line.y + line.height - (hq + yq) * (q + 1)
                        qrow = self.qrows[sq] ;  qrow.update(x=xq, y=yyq, scale_x=mxq, scale_y=myq)  ;  sq += 1
                        if dbg: self.dumpSprite(self.sprites[i], i + 1, '{:2} {:2} {:2} {:3} {:5} {:16}'.format(sp, sl, sq, sr, sc, 'resizeQRows'))     ;  i += 1
                        nc, ic, xc, yc, wc, hc, oc, gc, mxc, myc = self.geom(C, qrow.x, qrow.y, qrow.width, qrow.height, why='', init=False, dump=0)
                        for c in range(nc):
                            xxc, yyc = qrow.x + xc + (wc + xc) * c, qrow.y + qrow.height - (hc + yc)
                            self.cols[sc].update(x=xxc, y=yyc, scale_x=mxc, scale_y=myc)             ;  sc += 1
                            if dbg: self.dumpSprite(self.sprites[i], i + 1, '{:2} {:2} {:2} {:3} {:5} {:16}'.format(sp, sl, sq, sr, sc, 'resizeCols'))  ;  i += 1
                nr, ir, xr, yr, wr, hr, o, gr, mxr, myr = self.geom(R, line.x, line.y, line.width, line.height, why='', init=False, dump=0)
                rr = 1 if n[Q] else 0
                for r in range(rr, nr):
                    yyr = line.y + line.height - (hr + yr) * (r + 1)
                    row = self.rows[sr]   ;       row.update(x=xr, y=yyr, scale_x=mxr, scale_y=myr)   ;  sr += 1
                    if dbg: self.dumpSprite(self.sprites[i], i + 1, '{:2} {:2} {:2} {:3} {:5} {:16}'.format(sp, sl, sq, sr, sc, 'resizeRows'))         ;  i += 1
                    nc, ic, xc, yc, wc, hc, oc, gc, mxc, myc = self.geom(C, row.x, row.y, row.width, row.height, why='', init=False, dump=0)
                    for c in range(nc):
                        xxc, yyc = row.x + xc + (wc + xc) * c, row.y + row.height - (hc + yc)
                        self.cols[sc].update(x=xxc, y=yyc, scale_x=mxc, scale_y=myc)                  ;  sc += 1
                        if dbg: self.dumpSprite(self.sprites[i], i + 1, '{:2} {:2} {:2} {:3} {:5} {:16}'.format(sp, sl, sq, sr, sc, 'resizeCols'))     ;  i += 1
        if dbg: self.dumpSprite()
        self.log('(END) n={}'.format(n))
########################################################################################################################################################################################################
    def dumpSprites(self, why=''):
        n = self.n
        self.log('(BGN) n={} {}'.format(n, why))
        self.dumpSprite()
        i, sp, sl, sq, sr, sc = 0, 0, 0, 0, 0, 0
        for p in range(n[P]):
            sp += 1  ;                     self.dumpSprite(self.sprites[i], i + 1, '{:2} {:2} {:2} {:3} {:4}  {:16}'.format(sp, sl, sq, sr, sc, why))  ;  i += 1
            for l in range(n[L]):
                sl += 1  ;                 self.dumpSprite(self.sprites[i], i + 1, '{:2} {:2} {:2} {:3} {:4}  {:16}'.format(sp, sl, sq, sr, sc, why))  ;  i += 1
                for q in range(n[Q]):
                    sq += 1  ;             self.dumpSprite(self.sprites[i], i + 1, '{:2} {:2} {:2} {:3} {:4}  {:16}'.format(sp, sl, sq, sr, sc, why))  ;  i += 1
                    for c in range(n[K]):
                        sc += 1  ;         self.dumpSprite(self.sprites[i], i + 1, '{:2} {:2} {:2} {:3} {:4}  {:16}'.format(sp, sl, sq, sr, sc, why))  ;  i += 1
                for r in range(n[R]):
                    sr += 1  ;             self.dumpSprite(self.sprites[i], i + 1, '{:2} {:2} {:2} {:3} {:4}  {:16}'.format(sp, sl, sq, sr, sc, why))  ;  i += 1
                    for c in range(n[K]):
                        c += 1  ;          self.dumpSprite(self.sprites[i], i + 1, '{:2} {:2} {:2} {:3} {:4}  {:16}'.format(sp, sl, sq, sr, sc, why))  ;  i += 1
        self.dumpSprite()
        self.log('(END) n={} {}'.format(n, why))

    def dumpSprite(self, s=None, c=-1, why=''):
        if s is None: self.log(' sid   p  l  q   r  col     why               x      xc        y      yc        w       h    iax  iay    m      mx     my     rot   red green blue opc vsb    group       parent', ind=0); return
        f = '{:5} {:16} {:7.2f} {:7.2f}  {:7.2f} {:7.2f}  {:7.2f} {:7.2f} {:4} {:4} {:6.3f} {:6.3f} {:6.3f} {:7.2f}  {:3}  {:3}  {:3}  {:3}  {:1}  {} {}'
        k, o, v, g, p = s.color, s.opacity, s.visible, s.group, s.group.parent
        xc, yc = s.x + s.width / 2, s.y + s.height / 2
        fs = f.format(c, why, s.x, xc, s.y, yc, s.width, s.height, s.image.anchor_x, s.image.anchor_y, s.scale, s.scale_x, s.scale_y, s.rotation, k[0], k[1], k[2], o, v, g, p)
        self.log('{}'.format(fs), ind=0)
        assert (type(s) == pyglet.sprite.Sprite)

    def toggleColorLists(self, motion):
        cls = self.colorLists
        i = self.i[P]
        self.log('i={}'.format(i))
        if motion == pygwink.MOTION_LEFT:
            for j in range(len(cls[i])): cls[i][j].visible = False
            i -= 1
            i = i % len(COLORS)
            for j in range(len(cls[i])): cls[i][j].visible = True
            self.log('MOTION_LEFT={} i[P]={} len(cls)={}'.format(motion, i, len(cls)))
        elif motion == pygwink.MOTION_RIGHT:
            for j in range(len(cls[i])): cls[i][j].visible = False
            i += 1
            i = i % len(COLORS)
            for j in range(len(cls[i])): cls[i][j].visible = True
            self.log('MOTION_RIGHT={} i[P]={} len(cls)={}'.format(motion, i, len(cls)))
        self.i[P] = i
########################################################################################################################################################################################################
    def on_resize(self, width, height):
        super().on_resize(width, height)
        self.ww, self.hh = width, height
        self.resizeTestColors()

    def on_draw(self):
        self.clear()
        self.batch.draw()

    def on_key_press(self, symb, mods):
        self.symb, self.mods, self.symbStr, self.modsStr = symb, mods, pygwink.symbol_string(symb), pygwink.modifiers_string(mods)
        self.kbk = self.symbStr  ;  kbk = self.kbk
        self.log('(BGN) {}'.format(self.kpEvntTxt()))
        if                  self.isTab(kbk):                          self.addTab(kbk, 'on_key_press')
        elif kbk == 'Q' and self.isCtrl(mods) and self.isShift(mods): self.quit('keyPress({})'.format(kbk))
        elif kbk == 'Q' and self.isCtrl(mods):                        self.quit('keyPress({})'.format(kbk))
        elif kbk == 'F' and self.isCtrl(mods) and self.isShift(mods): self.toggleFullScreen()
        elif kbk == 'F' and self.isCtrl(mods):                        self.toggleFullScreen()
#        self.updateCaption()
        self.log('(END) {}'.format(self.kpEvntTxt()))

    def on_text(self, text):
        self.kbk = text
        self.log('(BGN) {}'.format( self.kpEvntTxt()))
        if self.kbk=='$' and self.isShift(self.mods): self.snapshot()
#        self.updateCaption()
        self.log('(END) {}'.format( self.kpEvntTxt()))

    def on_text_motion(self, motion, dbg=0):
        self.kbk = motion
        if dbg: self.log('(BGN) {}'.format(self.kpEvntTxt()))
        if self.mods == 0:
            if   motion == pygwink.MOTION_LEFT:          self.move(-1)
            elif motion == pygwink.MOTION_RIGHT:         self.move( 1)
            elif motion == pygwink.MOTION_UP:            self.move(-self.n[K])
            elif motion == pygwink.MOTION_DOWN:          self.move( self.n[K])
            elif motion == pygwink.HOME:                 pass
            elif motion == pygwink.END:                  pass
#            elif motion==pygwink.MOTION_PREVIOUS_PAGE: self.move() # prevPage(self.i[P], motion)
#            elif motion==pygwink.MOTION_NEXT_PAGE:     self.move() # nextPage(self.i[P], motion)
            else:                                      self.log('on_text_motion() motion={} ???'.format(motion))
#            self.updateCaption()
        if dbg: self.log('(END) {}'.format(self.kpEvntTxt()))
########################################################################################################################################################################################################
    def snapshot(self):
        self.log('SFX={} SNAP_DIR={} SNAP_SFX={} BASE_NAME={} BASE_PATH={}'.format(SFX, SNAP_DIR, SNAP_SFX, BASE_NAME, BASE_PATH))
        SNAP_ID   = '.{}'.format(self.ssi)
        SNAP_NAME = BASE_NAME + SFX + SNAP_ID + SNAP_SFX
        SNAP_PATH = BASE_PATH / SNAP_DIR / SNAP_NAME
        pyglet.image.get_buffer_manager().get_color_buffer().save('{}'.format(SNAP_PATH))
        self.log('SNAP_ID={} SNAP_NAME={} SNAP_PATH={}'.format(SNAP_ID, SNAP_NAME, SNAP_PATH))
        self.ssi += 1

    def dumpStack(self, si):
        for i, e in enumerate(si):
            fp = pathlib.Path(e.filename)  ;            n = fp.stem  ;            l = e.lineno  ;            f = e.function  ;            c = e.code_context[0].strip()  ;            j = len(si) - (i + 1)
            self.log('{:2} {:9} {:5} {:20} {}'.format(j, n, l, f, c))
        self.log('MAX_STACK_DEPTH={:2}'.format(MAX_STACK_DEPTH))

    def indent(self): d = self.stackDepth() - 4;  return '{:{w}}'.format(d, w=d)

    @staticmethod
    def stackDepth():
        global MAX_STACK_DEPTH, MAX_STACK_FRAME
        si = inspect.stack()
        for i, e in enumerate(si):
            j = len(si) - (i + 1)
            if j > MAX_STACK_DEPTH: MAX_STACK_DEPTH = j;  MAX_STACK_FRAME = si
        return len(si)

    def log(self, msg='', ind=1, file=None, flush=False, sep=',', end='\n'):
        if not file: file = LOG_FILE
        si = inspect.stack(0)[1]
        p = pathlib.Path(si.filename)  ;        n = p.name  ;        l = si.lineno  ;        f = si.function  ;        t = ''
        if f == 'self.log': si = inspect.stack(0)[2];  p = pathlib.Path(si.filename);  n = p.name;  l = si.lineno;  f = si.function;  t = ''
        if ind: print('{:20} {:7} {:6} {} {:>20} '.format(self.indent(), l, n, t, f), file=file, end='')
        print('{}'.format(msg), file=file, flush=flush, sep=sep, end=end) if ind else print('{}'.format(msg), file=file, flush=flush, sep=sep, end=end)
        if file != LOG_FILE: self.log(msg, ind)
########################################################################################################################################################################################################
    def quit(self, why=''):
        self.log('(BGN)')
        text = '\n' + '###   Quit   ###' * 13 + '\n'
        self.log(text)
        self.dumpTest('quit() ' + why)
        self.snapshot()
        self.log(text)
        self.dumpStack(inspect.stack())
        self.log(text)
        self.dumpStack(MAX_STACK_FRAME)
        self.log('(END) closing LOG_FILE={}'.format(LOG_FILE.name))
        if not LOG_FILE.closed: LOG_FILE.close()
        exit()
########################################################################################################################################################################################################
if __name__ == '__main__':
    CARET = 0  ;  ORDER_GROUP = 1;  FULL_SCREEN = 0  ;  VRSN = 0  ;  SUBPIX = VRSN
    SFX           = '.' + chr(65 + VRSN)     ;  VRSNX =     'SUBPIX = VRSN'
    PATH          = pathlib.Path(sys.argv[0])
    BASE_PATH     = PATH.parent
    BASE_NAME     = BASE_PATH.stem
    LOG_DIR       = 'logs'  ;         LOG_SFX       = '.log'
    LOG_NAME      = BASE_NAME + SFX + LOG_SFX
    LOG_PATH      = BASE_PATH / LOG_DIR / LOG_NAME
    SNAP_DIR      = 'snaps' ;         SNAP_SFX      = '.png'
    P, L, Q, R, C, K = 0, 1, 2, 3, 4, 5
    OPACITY       = [255, 240, 225, 210, 190, 165, 140, 110, 80]
    GRAY          = [(255, 255, 255, OPACITY[0]), ( 0,  0,  0, OPACITY[0])]
    PINK          = [(255,  64, 192, OPACITY[0]), (57, 16, 16, OPACITY[0])]
    INFRA_RED     = [(255,  29,  24, OPACITY[0]), (68, 20, 19, OPACITY[0])]
    RED           = [(255,  24,  21, OPACITY[0]), (88, 15, 12, OPACITY[0])]
    ORANGE        = [(255, 200,  16, OPACITY[0]), (76, 30, 25, OPACITY[0])]
    YELLOW        = [(255, 255,  15, OPACITY[0]), (45, 41, 10, OPACITY[0])]
    GREEN         = [( 44, 255,   0, OPACITY[0]), (21, 54, 10, OPACITY[0])]
    GREEN_BLUE    = [( 24, 255,  61, OPACITY[0]), (10, 49, 25, OPACITY[0])]
    CYAN          = [( 32, 255, 255, OPACITY[0]), (16, 64, 64, OPACITY[0])]
    BLUE_GREEN    = [( 25, 181, 255, OPACITY[0]), (12, 37, 51, OPACITY[0])]
    BLUE          = [( 35,  26, 255, OPACITY[0]), (19, 11, 64, OPACITY[0])]
    INDIGO        = [( 35,  26, 255, OPACITY[0]), (19, 11, 64, OPACITY[0])]
    VIOLET        = [(176,  81, 255, OPACITY[0]), (44, 14, 58, OPACITY[0])]
    ULTRA_VIOLET  = [(194,  96, 255, OPACITY[3]), (50, 19, 61, OPACITY[1])]
    HUES          = 13  ;  MAX_STACK_DEPTH = 0  ;  MAX_STACK_FRAME = inspect.stack()
########################################################################################################################################################################################################
    def fri(f): return int(math.floor(f+0.5))
    def genColors(cp, nsteps=HUES, dbg=0):
        colors, clen = [], len(cp[0])
        diffs = [cp[1][i] - cp[0][i] for i in range(clen)]
        steps = [diffs[i]/nsteps     for i in range(clen)]
        if dbg: print('c1={} c2={} nsteps={} diffs={} steps='.format(cp[0], cp[1], nsteps, diffs), end='')  ;  print('[{:6.1f} {:6.1f} {:6.1f} {:6.1f}]'.format(steps[0], steps[1], steps[2], steps[3]))
        for j in range(nsteps):
            c = tuple([fri(cp[0][i] + j * steps[i]) for i in range(len(cp[0]))])
            if dbg: print('c[{}]={}'.format(j, c))
            colors.append(c)
        if dbg: print('colors={}'.format(cp))
        return colors

    GRAYS         = genColors(GRAY)
    PINKS         = genColors(PINK)
    INFRA_REDS    = genColors(INFRA_RED)
    REDS          = genColors(RED)
    ORANGES       = genColors(ORANGE)
    YELLOWS       = genColors(YELLOW)
    GREENS        = genColors(GREEN)
    GREEN_BLUES   = genColors(GREEN_BLUE)
    CYANS         = genColors(CYAN)
    BLUE_GREENS   = genColors(BLUE_GREEN)
    BLUES         = genColors(BLUE)
    INDIGOS       = genColors(INDIGO)
    VIOLETS       = genColors(VIOLET)
    ULTRA_VIOLETS = genColors(ULTRA_VIOLET)
    COLORS        = (INFRA_REDS, REDS, ORANGES, YELLOWS, GRAYS, GREENS, GREEN_BLUES, CYANS, BLUE_GREENS, BLUES, INDIGOS, VIOLETS, ULTRA_VIOLETS)
    CC            = (255, 190, 12, 176)
    CCC           = 3
    with open(str(LOG_PATH), 'w') as LOG_FILE:
        tabs          = Tabs()
        pyglet.app.run()
