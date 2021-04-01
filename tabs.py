import inspect, math, sys, os, glob, pathlib#, shutil#, unicodedata
import pyglet
import pyglet.window.key as pygwink
import pyglet.window.event as pygwine
sys.path.insert(0, os.path.abspath('../lib'))
import cmdArgs
####################################################################################################################################################################################################
CARET = 0  ;  EVENT_LOG = 1  ;  FULL_SCREEN = 0  ;  ORDER_GROUP = 1  ;  RESIZE = 1  ;  SUBPIX = 1
QQ    = 1  ;  SPRITES   = 1
VRSN  = 0
QQ            = VRSN  ;  VRSNX = 'QQ={} VRSN={}'.format(QQ, VRSN)
#SPRITES       = VRSN  ;  VRSNX = 'VRSN={} SPRITES={}'.format(VRSN, SPRITES)
SFX           = '.' + chr(65 + VRSN)
PATH          = pathlib.Path(sys.argv[0])
BASE_PATH     = PATH.parent
BASE_NAME     = BASE_PATH.stem
LOG_DIR       = 'logs'  ;         LOG_SFX       = '.log'
LOG_NAME      = BASE_NAME + SFX + LOG_SFX
LOG_PATH      = BASE_PATH / LOG_DIR / LOG_NAME
SNAP_DIR      = 'snaps' ;         SNAP_SFX      = '.png'
P, L, R, C, Q, U = 0, 1, 2, 3, 4, 5
S, LCOL, LLINE = ' ', 'Col', 'Line '
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
####################################################################################################################################################################################################
def fmtl(a, w=3, d1='[', d2=']'):
    c = ''
    for i in range(len(a)): c += '{:{w}} '.format(int(a[i]), w=w)
    return d1 + c + d2
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
####################################################################################################################################################################################################
COLORS        = []
GRAYS         = genColors(GRAY)       ;  COLORS.append(GRAYS)
PINKS         = genColors(PINK)       ;  COLORS.append(PINKS)
INFRA_REDS    = genColors(INFRA_RED)  ;  COLORS.append(INFRA_REDS)
REDS          = genColors(RED)        ;  COLORS.append(REDS)
ORANGES       = genColors(ORANGE)     ;  COLORS.append(ORANGES)
YELLOWS       = genColors(YELLOW)     ;  COLORS.append(YELLOWS)
GREENS        = genColors(GREEN)      ;  COLORS.append(GREENS)
GREEN_BLUES   = genColors(GREEN_BLUE) ;  COLORS.append(GREEN_BLUES)
CYANS         = genColors(CYAN)       ;  COLORS.append(CYANS)
BLUE_GREENS   = genColors(BLUE_GREEN) ;  COLORS.append(BLUE_GREENS)
BLUES         = genColors(BLUE)       ;  COLORS.append(BLUES)
INDIGOS       = genColors(INDIGO)     ;  COLORS.append(INDIGOS)
VIOLETS       = genColors(VIOLET)     ;  COLORS.append(VIOLETS)
ULTRA_VIOLETS = genColors(ULTRA_VIOLET)  ;  COLORS.append(ULTRA_VIOLETS)
COLORS        = (INFRA_REDS, REDS, ORANGES, YELLOWS, GRAYS, GREENS, GREEN_BLUES, CYANS, BLUE_GREENS, BLUES, INDIGOS, VIOLETS, ULTRA_VIOLETS)
CC            = (255, 190, 12, 176)
CCC           = 3
FONT_SCALE    = 123.42857
FONT_NAMES    = ['Times New Roman', 'Lucida Console', 'Courier New', 'Helvetica', 'Arial', 'Century Gothic', 'Bookman Old Style', 'Antique Olive']
FONT_COLORS   = [REDS[0], GREENS[0], GREEN_BLUES[5], BLUES[0], CYANS[0], ORANGES[0], REDS[0], INDIGOS[0], VIOLETS[0], PINKS[0], INFRA_REDS[0], YELLOWS[0], ULTRA_VIOLETS[0], BLUE_GREENS[0], GRAYS[0]]
FONT_DPIS     = [72, 78, 84, 90, 96, 102, 108, 114, 120]

class Tabs(pyglet.window.Window):
    def __init__(self):
        global FULL_SCREEN, SUBPIX, ORDER_GROUP
        SNAP_GLOB_ARG = str(BASE_PATH / SNAP_DIR / BASE_NAME) + SFX + '.*' + SNAP_SFX
        FILE_GLOB     = glob.glob(SNAP_GLOB_ARG)
        self.log('(BGN) {} {}'.format(__class__, VRSNX))
        self.log('QQ={} SPRITES={}'.format(QQ, SPRITES))
        self.log('CARET={} EVENT_LOG={} FULL_SCREEN={} ORDER_GROUP={} RESIZE={} SUBPIX={}'.format(CARET, EVENT_LOG, FULL_SCREEN, ORDER_GROUP, RESIZE, SUBPIX))
        self.log('{}'.format(SNAP_GLOB_ARG))
        for _F in FILE_GLOB:
            self.log('{}'.format(_F))
            pathlib.Path(_F).unlink()
        self.ww, self.hh  = 640, 480
        self.n, self.i, self.x, self.y, self.w, self.h, self.g = [1, 3, 6, 20, QQ, 20], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], []
        self.argMap = cmdArgs.parseCmdLine(dbg=1)
        if 'n' in self.argMap and len(self.argMap['n'])  > 0: self.n            = [int(self.argMap['n'][i]) for i in range(len(self.argMap['n']))]
        if 'i' in self.argMap and len(self.argMap['i'])  > 0: self.i            = [int(self.argMap['i'][i]) for i in range(len(self.argMap['i']))]
        if 'x' in self.argMap and len(self.argMap['x'])  > 0: self.x            = [int(self.argMap['x'][i]) for i in range(len(self.argMap['x']))]
        if 'y' in self.argMap and len(self.argMap['y'])  > 0: self.y            = [int(self.argMap['y'][i]) for i in range(len(self.argMap['y']))]
        if 'w' in self.argMap and len(self.argMap['w'])  > 0: self.ww           =  int(self.argMap['w'][0])
        if 'h' in self.argMap and len(self.argMap['h'])  > 0: self.hh           =  int(self.argMap['h'][0])
        if 'f' in self.argMap and len(self.argMap['f']) == 0: FULL_SCREEN       = 1
        if 'g' in self.argMap and len(self.argMap['g']) == 0: ORDER_GROUP       = 1
        if 's' in self.argMap and len(self.argMap['s']) == 0: SUBPIX            = 1
        self.log('[n]            n={}'.format(fmtl(self.n)))
        self.log('[i]            i={}'.format(fmtl(self.i)))
        self.log('[x]            x={}'.format(fmtl(self.x)))
        self.log('[y]            y={}'.format(fmtl(self.y)))
        self.log('[w]           ww={}'.format(self.ww))
        self.log('[h]           hh={}'.format(self.hh))
        self.log('[f]  FULL_SCREEN={}'.format(FULL_SCREEN))
        self.log('[g]  ORDER_GROUP={}'.format(ORDER_GROUP))
        self.log('[s]       SUBPIX={}'.format(SUBPIX))
#        if len(self.n) == K: self.n.append(self.n[C] + CCC)  ;  self.log('[n] +=n[C]+CCC n={}'.format(fmtl(self.n)))
        self.fontBold, self.fontItalic, self.fontColorIndex, self.fontDpiIndex, self.fontSize, self.fontNameIndex = 0, 0, 0, 4, 14, 0
        self.dumpFont()
        self._initWindowA()
        super().__init__(screen=self.screens[1], fullscreen=FULL_SCREEN, resizable=True, visible=False)
        self._initWindowB()
        self.symb, self.symbStr, self.mods, self.modsStr, self.kbk = 0, '', 0, '', 0
        self.ci = 0
        self.blankCol = ''
        self.cursor, self.caret = None, None
        self.data = []
        self._init()
        self.log('(END) {} {}'.format(__class__, VRSNX))
        text = '\n' + '###   __init__   ###' * 18 + '\n'
        self.log(text, ind=0)

    def _initWindowA(self, dbg=1):
        display      = pyglet.canvas.get_display()
        if dbg: self.log('(BGN) {}'.format(self.fmtWH()))  ;  self.log('display={}'.format(display))
        self.screens = display.get_screens()  ;  s = self.screens
        if dbg:
            for i in range(len(s)): self.log('screens[{}] x={} y={:5} {}'.format(i, s[i].x, s[i].y, self.fmtWH(s[i].width, s[i].height)))
            self.log('(END) {}'.format(self.fmtWH()))

    def _initWindowB(self, dbg=1):
        self.batch = pyglet.graphics.Batch()
        self._initGroups()
        if dbg: self.log('(BGN) {}'.format(self.fmtWH()))
        self.set_visible()
        if not FULL_SCREEN: self.set_size(self.ww, self.hh)
        self.ww, self.hh = self.get_size()
        if EVENT_LOG:
            self.eventLogger = pygwine.WindowEventLogger()
            self.push_handlers(self.eventLogger)
        if dbg: self.log('(END) {}'.format(self.fmtWH()))

    def fmtWH(self, w=None, h=None, d1='(', d2=')'):
        (w, h) = (self.ww, self.hh) if not w and not h else (w, h)
        return '{}{} x {}{}'.format(d1, w, h, d2)
    ####################################################################################################################################################################################################
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

    def _initCps(self, dbg=1):
        self.cpq = self.n[U] + CCC
        self.cpr = self.n[C] + CCC
        self.cpl = self.n[R] * self.cpr + self.n[Q] * self.cpq
        self.cpp = self.n[L] * self.cpl
        if dbg: self.log('cps={}'.format(fmtl(self.cps())))

    def _initRps(self, dbg=1):
        self.rpu = self.n[Q]
        self.rpc = self.n[R]
        self.rpl = self.cpr  * self.rpc + self.cpq * self.rpu
        self.rpp = self.n[L] * self.rpl
        if dbg: self.log('rps={}'.format(fmtl(self.rps())))

    def cps(self): return self.cpp, self.cpl, self.cpr, self.cpq
    def rps(self): return self.rpp, self.rpl, self.rpc, self.rpu
    def lnl(self): return list(map(len, [self.pages, self.lines, self.rows, self.cols, self.qrows, self.ucols]))

    @staticmethod
    def fmtDataDim(d): return '({} x {} x {})={:8,} tabs'.format(len(d), len(d[0]), len(d[0][0]), len(d)*len(d[0])*len(d[0][0]))
    ####################################################################################################################################################################################################
    def cursorCol(self, dbg=0):
        p, l, r, c, q, u = self.i
        cpp, cpl, cpr, cpq = self.cps()
        cc = p*cpp + l*cpl + r*cpr + q*cpq + c
        if dbg:
            self.log('cc={:4}=({}*{:3} + {}*{:3} + {}*{:3} + {:2}*{:3} + {:3})'.format(cc, p, cpp, l, cpl, r, cpr, q, cpq, c))
            self.log('cc={:4}=({:4} + {:4} + {:3} + {:4} + {:3})'.format(cc, p*cpp, l*cpl, r*cpr, q*cpq, c))
        return cc

    def cursorRow(self, dbg=0):
        p, l, r, c, q, u = self.i
        rpp, rpl, rpc, rpu = self.rps()
        cr = p*rpp + l*rpl + r*rpc + q*rpu + r
        if dbg:
            self.log('cr={:4}=({}*{:3} + {}*{:3} + {}*{:3} + {:2}*{:3} + {:3})'.format(cr, p, rpp, l, rpl, r, rpc, q, rpu, r))
            self.log('cr={:4}=({:4} + {:4} + {:3} + {:4} + {:3})'.format(cr, p*rpp, l*rpl, r*rpc, q*rpu, r))
        return cr

    def _init(self, dbg=1):
        self.log('(BGN) n={} i={}'.format(fmtl(self.n), fmtl(self.i)))
        self.pages, self.lines, self.rows, self.cols = [], [], [], []
        self.qrows, self.ucols = [], []
        self.labels = []
        self.data = []
        if SPRITES: self.sprites = []
        self.kc = [GRAYS[11], GRAYS[7]] ; kb = [self.kc[1]]
        self.kp = kb ; self.kl = kb ; self.kq = kb ; self.kr = kb ; self.ku = kb
        self.ssi  = 0
        self._initCps()  ;  self._initRps()
        self.readDataFile()
        if QQ: self.labelTextA, self.labelTextB = ['R', 'M', '@'], ['R', 'M', '@']
        self.createSprites() if SPRITES else  self.createLabels()
        self.createCursor(self.g[C+3])
        if dbg: self.dumpStruct('_init')
        self.log('(END) n={} i={}'.format(fmtl(self.n), fmtl(self.i)))
    ####################################################################################################################################################################################################
    def on_resize(self, width, height):
        super().on_resize(width, height)
        self.ww, self.hh = width, height
        if not RESIZE: return
        self.log('(BGN) {} {}'.format(self.fmtWH(), self.fmtDataDim(self.data)))
        self.resizeSprites() if SPRITES else self.resizeLabels()
        self.resizeFonts()
        self.resizeCursor()
        self.snapshot()
        self.dumpStruct('on_resize()')
#        self.updateCaption()
        self.log('(END) {} {}'.format(self.fmtWH(), self.fmtDataDim(self.data)))
    ####################################################################################################################################################################################################
    def dumpStruct(self, why=''):
        self.log('(BGN) {}'.format(why))
#        self.dumpData(why)
        self.dumpSprites() if SPRITES else self.dumpLabels(why)
        self.dumpFont(why)
        self.cursorCol(1)
        self.cursorRow(1)
        self.log('(END) {}'.format(why))
    ####################################################################################################################################################################################################
    def readDataFile(self, dbg=1):
        DATA_DIR  = 'data'    ;                  DATA_SFX = '.dat'  ;  DATA_PFX = '.{}'.format(self.n[C])
        DATA_NAME = BASE_NAME + SFX + DATA_PFX + DATA_SFX
        DATA_PATH = BASE_PATH / DATA_DIR / DATA_NAME
        DATA_FILE = open(str(DATA_PATH), 'r')
        DATA_FILE.seek(0, 2)  ;  size = DATA_FILE.tell()            ;  DATA_FILE.seek(0, 0)
        self.log('(BGN) {:40} {:8,} bytes = {:4,.0f} KB'.format(DATA_FILE.name, size, size/1024))
        strings = []  ;  nl, ns, nc = 0, 0, 0
        self.log('reading {:2}{} line'.format(nl + 1, self.ordSfx(nl + 1)))
        while 1:
            string = DATA_FILE.readline().strip() ;  ns = len(strings)  ;  nc = len(strings[0]) if ns else 0
            if len(string) == 0:
                if ns: self.data.append(strings) ; nl += 1 ; self.log('read    {:2}{} line with {:6,} cols on {:4,} strings {:8,} tabs'.format(nl, self.ordSfx(nl), nc, ns, nc*ns)) ; strings=[] ; continue
                else: break
            strings.append(string)
            if dbg: self.log('{}'.format(string), ind=0)
        nl = len(self.data)  ;  ns = len(self.data[0])  ;  nc = len(self.data[0][0])  ;  nt = nl*nc*ns
        vdf = self.isVertDataFrmt(self.data)  ;  self.blankCol = '-' * ns
        self.log('read     {:2} lines with {:6,} cols on {:4,} strings {:8,} tabs, vdf={} blankCol({})={}'.format(nl, nl*nc, nl*ns, nt, vdf, len(self.blankCol), self.blankCol))
        if dbg: self.dumpDataH(self.data)
        self.data = self.transpose(self.data)
        vdf       = self.isVertDataFrmt(self.data)
        if dbg: self.dumpDataV(self.data)
        self.log('assert: size=nt+2*(nl*ns+nl-1) {:8,} + {} = {:8,} bytes'.format(nt, 2*(nl*ns+nl-1), size))  ;  assert size == nt + 2 * (nl * ns + nl - 1)  ;  assert vdf
        self.log('(END) {:40} {:8,} bytes = {:4,.0f} KB'.format(DATA_FILE.name, size, size/1024))

    def isVertDataFrmt(self, d, dbg=0):
        vdf = 0
        if dbg: self.log('(BGN) type(d)={} type(d[0])={} type(d[0][0])'.format(type(d), type(d[0]), type(d[0][0])))
        assert type(d) is list and type(d[0]) is list and type(d[0][0]) is str
        if type(d) is list and type(d[0]) is list and type(d[0][0]) is str:
            s0 = d[0][0]  ;  ev = ''
            if dbg: self.log('s0=d[0]: len(s0)={} s0={}'.format(len(s0), s0))
            if not s0.isdecimal():
                if dbg: self.log('s0={} is not a decimal'.format(s0))
            else:
                for i in range(len(s0)): ev = ev + str(i + 1)
                if dbg: self.log('ev={}'.format(ev))
                if s0 == ev:
                    if dbg: self.log('s0={} == ev={}'.format(s0, ev))
                    s1 = d[0][1]
                    if dbg: self.log('s1=d[1]: len(s1)={} s1={}'.format(len(s1), s1))
                    if s1.isalpha():
                        for i in range(len(s1)):
                            if s1[i] not in ('A', 'B', 'C', 'D', 'E', 'F', 'G'):
                                if dbg: self.log('s1[i]={} is not a Note Name'.format(i, s1[i]))
                                break
                        else:
                            vdf = 1
                            if dbg: self.log('s1={} is a String Tuning'.format(s1))
        if dbg: self.log('(END) type(d)={} type(d[0])={} type(d[0][0]) return vdf={}'.format(type(d), type(d[0]), type(d[0][0]), vdf))
        return vdf
    ####################################################################################################################################################################################################
    def dumpData(self, why='', c=1, l=1, i=0):
        self.log('(BGN) {}'.format(why))
        self.dumpDataV(self.data, c, l, i) if self.isVertDataFrmt(self.data) else self.dumpDataH(self.data, c, l, i)
        transpose = self.transpose(self.data, why='Internal')
        self.dumpDataV(transpose, c, l, i) if self.isVertDataFrmt(transpose) else self.dumpDataH(transpose, c, l, i)
        self.log('(END) {}'.format(why))

    def dumpDataH(self, data, c=1, l=1, i=0):
        self.log('(BGN) c={} l={} i={} {}'.format(c, l, i, self.fmtDataDim(data)))
        for ll in range(len(data)):
            if l:  llt = 'Line {}'.format(ll + 1)  ;  llab = '{:{}}'.format(llt, i + 1)  ;  self.log('{}{}'.format(S * i, llab), ind=0)
            if c:  self.dumpDataLabels(data[ll], i=i, sep=S)
            for rr in range(len(data[ll])):
                self.log('{}'.format(S * i), ind=0, end='')
                for cc in range(len(data[ll][rr])):
                    self.log('{}'.format(data[ll][rr][cc]), ind=0, end='')
                self.log(ind=0)
            self.log(ind=0)
        self.log('(END) c={} l={} i={} {}'.format(c, l, i, self.fmtDataDim(data)))

    def dumpDataV(self, data, c=1, l=1, i=0):
        self.log('(BGN) c={} l={} i={} {}'.format(c, l, i, self.fmtDataDim(data)))
        if l:
            t0 = S * i + LCOL + S       if       i >= 0 else LCOL
            self.log(t0, ind=0, end='') if c and i >= 0 else self.log(S * i, ind=0, end='')
            w = max(len(data[0][0]), len(LLINE) + 1)
            for ll in range(len(data)):
                t = '{}{}'.format(LLINE, ll + 1)
                self.log('{:{}}'.format(t, w), ind=0, end=S)
            self.log(ind=0)#            self.log(t0, ind=0)         if c and i < 0 else self.log(ind=0)
        for cc in range(len(data[0])):
            self.log('{}{:3} '.format(S * i, cc + 1), ind=0, end='') if i >= 0 and c else self.log('{}'.format(S * i), ind=0, end='')
            for ll in range(len(data)):
                self.log('{}'.format(data[ll][cc]), ind=0, end=S)
            self.log(ind=0)##            self.log('{:3} '.format(cc + 1),        ind=0)           if i <  0 and c else self.log(ind=0)
        self.log('(END) c={} l={} i={} {}'.format(c, l, i, self.fmtDataDim(data)))
    ####################################################################################################################################################################################################
    def dumpDataLabels(self, data, i=0, sep='%'):
        n = len(data[0])-CCC    ;  a = ' ' * i if i else ''   ;  b = sep * n  ;  p = '   '  ;  q = '  @'  ;  r = sep * 3
        if n >= 100:      self.log('{}{}'.format(a, p), ind=0, end='')  ;  [  self.log('{}'.format(c//100   if c>=100 else ' '), ind=0, end='') for c in range(1, n+1) ]  ;  self.log(ind=0)
        if n >= 10:       self.log('{}{}'.format(a, p), ind=0, end='')  ;  [  self.log('{}'.format(c//10%10 if c>=10  else ' '), ind=0, end='') for c in range(1, n+1) ]  ;  self.log(ind=0)
        self.log(                  '{}{}'.format(a, q), ind=0, end='')  ;  [  self.log('{}'.format(c%10),                        ind=0, end='') for c in range(1, n+1) ]  ;  self.log(ind=0)
        if sep != '':   self.log('{}{}{}'.format(a, r, b), ind=0)

    def transpose(self, data, why=' External  ', dbg=1):
        if dbg: self.log('(BGN) {} {}'.format(why, self.fmtDataDim(data)))
        t = []
        for l in range(len(data)):
            tmp = []
            for c in range(len(data[l][0])):
                a = []  ;  s = ''  ;  tt = None
                for r in range(len(data[l])):
                    tt = type(data[l][r])
                    if   tt is str:  s += data[l][r][c]
                    elif tt is list: a.append(data[l][r][c])
                tmp.append(s) if tt is str else t.append(a)
            t.append(tmp)
        if dbg: self.log('(END) {} {}'.format(why, self.fmtDataDim(t)))
        return t
    ####################################################################################################################################################################################################
    def geom(self, p=None, j=0, init=0, dbg=0):
        nq = QQ  ;   mx, my = None, None
        n, i, x, y, w, h, g = self.n[j], self.i[j], self.x[j], self.y[j], self.w[j], self.h[j], self.g[j]
        if   nq and j == Q:      n = self.n[R] + 1
        elif nq and j == R:      n += 1
        if j == C or j == U:     n += CCC
        if p:
            if j == C or j == U: w, h = (p.width - x*(n + 1))/n,  p.height - y*2
            else:                w, h =  p.width - x*2,          (p.height - y*(n + 1))/n
        else:                    w, h =  self.ww - x*2, self.hh - y*2
        if j != C and j != U:    x += p.x if p else self.x[P]
        if init:                 self.w[j], self.h[j] = w, h
        else:                    mx, my = w/self.w[j], h/self.h[j]
        if nq and j == Q:        n = nq
        if dbg:                  self.dumpGeom(j)
        return n, i, x, y, w, h, g, mx, my

    def dumpGeom(self, j): self.log('j={} n={:3} i={:4} x={:3} y={:3} w={:7.2f} h={:7.2f} g={}'.format(j, self.n[j], self.i[j], self.x[j], self.y[j], self.w[j], self.h[j], self.g[j]))
    ####################################################################################################################################################################################################
    def createSprites(self, dbg=1):
        self.log('(BGN) n={}'.format(fmtl(self.n)))
        if QQ:
            self.labelTextA.extend('{}'.format(j) for j in range(1, self.n[C] + 1))
            self.labelTextB.extend('{}'.format(j % 10 if j % 10 else j // 10 % 10) for j in range(1, self.n[C] + 1))
            texts = list(zip(self.labelTextA, self.labelTextB))
            self.dumpLabelText(texts)
        cp, cl, cr, cc, cq, cu = self.kp, self.kl, self.kr, self.kc, self.kq, self.ku
        np, ip, xp, yp, wp, hp, gp, mx, my = self.geom(None, P, init=1)
        if dbg: self.dumpSprite()
        for p in range(np):
            page = self.createSprite(self.pages, xp, yp, wp, hp, cp[p % len(cp)], gp, why='create Page', v=0, dbg=dbg)
            v = 1 if len(self.pages) == 1 else 0
            nl, il, xl, yl, wl, hl, gl, mx, my = self.geom(page, L, init=1)
            for l in range(nl):
                yyl = page.y + page.height - (hl+yl)*(l+1)
                line = self.createSprite(self.lines, xl, yyl, wl, hl, cl[l % len(cl)], gl, why='create Line', v=v, dbg=dbg)
                if QQ:
                    nq, iq, xq, yq, wq, hq, gq, mx, my = self.geom(line, Q, init=1)
                    for q in range(nq):
                        yyq = line.y + line.height - (hq+yq)*(q+1)
                        qrow = self.createSprite(self.qrows, xq, yyq, wq, hq, cq[0], gq, why='create QRow', v=v, dbg=dbg)
                        nu, iu, xu, yu, wu, hu, gu, mx, my = self.geom(qrow, U, init=1)
                        if dbg: self.dumpSprite()  ;  self.dumpLabel()
                        for u in range(nu):
                            xxu = qrow.x + xu + (wu+xu)*u + wu/2 ;  yyu = qrow.y + qrow.height - (hu+yu) + hu/2
                            self.createLabel(self.labelTextB[u], self.ucols, xxu, yyu, wu, hu, self.cci(u, cu), gu, why='create UCol')
                        if dbg: self.dumpLabel()  ;  self.dumpSprite()
                nr, ir, xr, yr, wr, hr, gr, mx, my = self.geom(line, R, init=1)
                rr = 1 if QQ else 0
                for r in range(rr, nr):
                    yyr = line.y + line.height - (hr+yr)*(r+1)
                    row = self.createSprite(self.rows, xr, yyr, wr, hr, cr[r % len(cr)], gr, why='create Row',  v=v, dbg=dbg)
                    nc, ic, xc, yc, wc, hc, gc, mx, my = self.geom(row, C, init=1)
                    if dbg: self.dumpSprite()         ;  self.dumpLabel()
                    for c in range(nc):
                        xxc = row.x + xc + (wc+xc)*c  ;  yyc = row.y + row.height - (hc+yc)
                        xxc += wc/2                   ;  yyc += hc/2
                        self.createLabel(self.data[l][c][r-rr], self.cols, xxc, yyc, wc, hc, self.cci(c, cc), gc, why='create Col')
                    if dbg: self.dumpLabel()
                    if dbg: self.dumpSprite()
        self.log('(END) n={}'.format(fmtl(self.n)))

    def cci(self, c, cc):
        if c == 0: self.ci = (self.ci + 1) % len(cc)
        return (c + self.ci) % len(cc)

    def dumpLabelText(self, t, d='%', why='', dbg=1):
        self.log('{} len(t)={} len(t[0])={}'.format(why, len(t), len(t[0])))
        for j in range(len(t)):
            self.log('{:^3}'.format(t[j][0]), ind=0, end=' ')
        self.log(ind=0)
        for i in range(3): self.log('{:3} '.format(' '), ind=0, end='')
        for k in range(len(t)//10):
            for i in range(9): self.log('{:^3} '.format(' '), ind=0, end='')
            self.log(' {} '.format(d), ind=0, end=' ')
        self.log(ind=0)
        for j in range(len(t)):
            self.log('{:^3}'.format(t[j][1]), ind=0, end=' ')
        self.log(ind=0)
        if dbg:
            for i in range(len(t)):
                self.log('{:5}'.format(i - 2), ind=0, end=' ')
                self.log(' {:>5}'.format(t[i][0]), ind=0, end=' ')
                d2 = ' ' if i == 2 or (i - 2) % 10 else d
                self.log('{}{:>5}'.format(d2, t[i][1]), ind=0, end=' ')
                self.log(ind=0)

    def createLabels(self, dbg=1):
        self.log('(BGN) n={}'.format(fmtl(self.n)))
        if QQ:
            self.labelTextA.extend('{}'.format(j) for j in range(1, self.n[C] + 1))
            self.labelTextB.extend('{}'.format(j % 10 if j % 10 else j // 10 % 10) for j in range(1, self.n[C] + 1))
            texts = list(zip(self.labelTextA, self.labelTextB))
            self.dumpLabelText(texts)
        np, ip, xp, yp, wp, hp, gp, mx, my = self.geom(None, P, init=1)
        if dbg: self.dumpLabel()
        for p in range(np):
            xp2 = xp + wp/2  ;          yp2 = yp + hp/2
            page = self.createLabel('Page', self.pages, xp2, yp2, wp, hp, P, gp, why='create Page')
            nl, il, xl, yl, wl, hl, gl, mx, my = self.geom(page, L, init=1)
            for l in range(nl):
                yl2 = page.y + page.height/2 - (hl+yl)*(l+1) + hl/2
                line = self.createLabel('Line', self.lines, xl, yl2, wl, hl, L, gl, 'create Line')
                if QQ:
                    nq, iq, xq, yq, wq, hq, gq, mx, my = self.geom(line, Q, init=1)
                    for q in range(nq):
                        yq2 = line.y + line.height/2 - (hq+yq)*(q+1) + hq/2
                        qrow = self.createLabel('QRow', self.qrows, xq, yq2, wq, hq, Q, gq, 'create QRow')
                        nc, ic, xc, yc, wc, hc, gc, mx, my = self.geom(qrow, C, init=1)
                        for c in range(nc):
                            xc2 = qrow.x - qrow.width/2 + (wc+xc)*c + wc/2
                            yc2 = qrow.y + qrow.height  - (hc+yc)
                            self.createLabel(self.labelTextB[c], self.ucols, xc2, yc2, wc, hc, self.cci(c, self.kc), gc, 'create QCol')
                nr, ir, xr, yr, wr, hr, gr, mx, my = self.geom(line, R, init=1)
                rr = 1 if QQ else 0
                for r in range(rr, nr):
                    yr2 = line.y + line.height/2 - (hr+yr)*(r+1) + hr/2
                    row = self.createLabel('Row', self.rows, xr, yr2, wr, hr, R, gr, 'create Row')
                    nc, ic, xc, yc, wc, hc, gc, mx, my = self.geom(row, C, init=1)
                    for c in range(nc):
                        xc2 = row.x - row.width/2 + (wc+xc)*c + wc/2
                        yc2 = row.y + row.height  - (hc+yc)
                        self.createLabel(self.data[l][c][r-rr], self.cols, xc2, yc2, wc, hc, self.cci(c, self.kc), gc, 'create Col')
        self.log('(END) lnl={}'.format(fmtl(self.lnl())))
    ####################################################################################################################################################################################################
    def createSprite(self, p, x, y, w, h, cc, grp, why, v=0, dbg=0): #        s.visible = v if v else True if i==P else False
        scip = pyglet.image.SolidColorImagePattern(cc)
        img = scip.create_image(width=fri(w), height=fri(h))
        s = pyglet.sprite.Sprite(img, x, y, batch=self.batch, group=grp, subpixel=SUBPIX)
        s.visible = v
        s.color, s.opacity = cc[:3], cc[3]
        if SPRITES: self.sprites.append(s)
        p.append(s)
        p, l, r, c, q, u = self.lnl()
        if dbg: self.dumpSprite(s, len(self.sprites), p, l, r, c, q, u, why=why)
        return s

    def createLabel(self, text, p, x, y, w, h, kk, g, why, m=0, z=1):
        a, ax, ay = ('center', 'center', 'center') if not z else ('left', 'center', 'center')
        b = self.batch
        o, k, d, j, n, s = self.fontParams()
        d = FONT_DPIS[d]
        n = FONT_NAMES[n]
        k = FONT_COLORS[k + kk]
        if m:
            for i in range(len(text), 0, -1): text = text[:i] + '\n' + text[i:]
        ll = pyglet.text.Label(text, font_name=n, font_size=s, bold=o, italic=j, color=k, x=x, y=y, width=w, height=h, anchor_x=ax, anchor_y=ay, align=a, dpi=d, batch=b, group=g, multiline=m)
        self.labels.append(ll)
        p.append(ll)
        p, l, r, c, q, u = self.lnl()
        if len(why): self.dumpLabel(ll, len(self.labels), p, l, r, c, q, u, why=why)
        return ll
    ####################################################################################################################################################################################################
    def resizeSprites(self, dbg=1):
        self.log('(BGN) n={}'.format(fmtl(self.n)))
        if dbg: self.dumpSprite()
        i, sp, sl, sr, sc, sq, su = 0, 0, 0, 0, 0, 0, 0
        np, ip, xp, yp, wp, hp, gp, mxp, myp = self.geom(None, P)
        for p in range(np):
            page = self.pages[sp]  ;  page.update(x=xp, y=yp, scale_x=mxp, scale_y=myp)  ;  sp += 1
            if dbg: self.dumpSprite(self.sprites[i], i+1, sp, sl, sr, sc, sq, su, 'resize Page') ; i += 1
            nl, il, xl, yl, wl, hl, gl, mxl, myl = self.geom(page, L)
            for l in range (nl):
                yyl = page.y + page.height - (hl + yl)*(l + 1)
                line = self.lines[sl]  ;  line.update(x=xl, y=yyl, scale_x=mxl, scale_y=myl)  ;  sl += 1
                if dbg: self.dumpSprite(self.sprites[i], i+1, sp, sl, sr, sc, sq, su, 'resize Line') ; i += 1
                if QQ:
                    nq, iq, xq, yq, wq, hq, gq, mxq, myq = self.geom(line, Q)
                    for q in range(nq):
                        yyq = line.y + line.height - (hq + yq)*(q + 1)
                        qrow = self.qrows[sq]  ;  qrow.update(x=xq, y=yyq, scale_x=mxq, scale_y=myq)  ;  sq += 1
                        if dbg: self.dumpSprite(self.sprites[i], i+1, sp, sl, sr, sc, sq, su, 'resize QRow') ; i += 1
                        nu, iu, xu, yu, wu, hu, gu, mxu, myu = self.geom(qrow, U)
                        for u in range(nu):
                            xxu = qrow.x + xu + (wu + xu)*u  ;  yyu = qrow.y + qrow.height - (hu + yu)
                            self.ucols[su].w = wu            ;  self.ucols[su].h = hu
                            self.ucols[su].x = xxu + wu/2    ;  self.ucols[su].y = yyu + hu/2
                            if dbg: self.dumpLabel(self.ucols[su], su, sp, sl, sr, sc, sq, su, why='resize UCol')
                            sc += 1
                nr, ir, xr, yr, wr, hr, gr, mxr, myr = self.geom(line, R)
                rr = 1 if QQ else 0
                for r in range(rr, nr):
                    yyr = line.y + line.height - (hr + yr)*(r + 1)
                    row = self.rows[sr]  ;  row.update(x=xr, y=yyr, scale_x=mxr, scale_y=myr)  ;  sr += 1
                    if dbg: self.dumpSprite(self.sprites[i], i+1, sp, sl, sr, sc, sq, su, 'resize Row') ; i += 1
                    nc, ic, xc, yc, wc, hc, gc, mxc, myc = self.geom(row, C)
                    for c in range(nc):
                        xxc = row.x + xc + (wc + xc)*c  ;  yyc = row.y + row.height - (hc + yc)
                        self.cols[sc].w = wc            ;  self.cols[sc].h = hc
                        self.cols[sc].x = xxc + wc/2    ;  self.cols[sc].y = yyc + hc/2
                        if dbg: self.dumpLabel(self.cols[sc], sc, sp, sl, sr, sc, sq, su, 'resize Col')
                        sc += 1
        if dbg: self.dumpSprite()
        self.log('(END) n={}'.format(fmtl(self.n)))

    def resizeLabels(self, dbg=1):
#        cpp, cpl, cpr, cpq = self.cps()
#        lnl = self.lnl()
#        self.log('(BGN) lnl={} cpp={} cpl={} cpr={} cpq={}'.format(lnl, cpp, cpl, cpr, cpq))
        self.log('(BGN) lnl={} cps={}'.format(self.lnl(), self.cps()))
        i, sp, sl, sr, sc, sq, su = 0, 0, 0, 0, 0, 0, 0
        np, ip, xp, yp, wp, hp, gp, mxp, myp = self.geom(None, P)
        for p in range(np):
            page = self.pages[sp]
            page.width = wp  ;  page.height = hp  ;  page.x = xp + wp/2  ;  page.y = yp + hp/2  ;  sp += 1
            i += 1
            if dbg: self.dumpLabel(page, i, sp, sl, sr, sc, sq, su, 'resize page')
            nl, il, xl, yl, wl, hl, gl, mxl, myl = self.geom(page, L)
            for l in range(nl):
                line = self.lines[sl]
                line.width = wl  ;  line.height = hl  ;  line.x = xl
                line.y = page.y + page.height/2 - (hl+yl)*(l+1) + hl/2  ;  sl += 1
                if dbg: self.dumpLabel(line, i, sp, sl, sr, sc, sq, su, 'resize line')
                i += 1
                if QQ:
                    nq, iq, xq, yq, wq, hq, gq, mxq, myq = self.geom(line, Q)
                    for q in range(nq):
                        qrow = self.qrows[sq]
                        qrow.width = wq  ;  qrow.height = hq  ;  qrow.x = xq
                        qrow.y = line.y + line.height/2 - (hq+yq)*(q+1) + hq/2  ;  sq += 1
                        if dbg: self.dumpLabel(qrow, i, sp, sl, sr, sc, sq, su, 'resize QRow')
                        i += 1
                        nc, ic, xc, yc, wc, hc, gc, mxc, myc = self.geom(qrow, C)
                        for c in range(nc):
                            qcol = self.ucols[sc]
                            qcol.width = wc     ;  qcol.height = hc
                            qcol.x = qrow.x - qrow.width/2 + (wc+xc)*c + wc/2
                            qcol.y = qrow.y + qrow.height  - (hc+yc)             ;  sc += 1
                            if dbg: self.dumpLabel(qcol, i, sp, sl, sr, sc, sq, su, 'resize QCol')
                            i += 1
                nr, ir, xr, yr, wr, hr, gr, mxr, myr = self.geom(line, R)
                rr = 1 if QQ else 0
                for r in range(rr, nr):
                    row = self.rows[sr]
                    row.width = wr  ;  row.height = hr  ;  row.x = xr
                    row.y = line.y + line.height/2 - (hr+yr)*(r+1) + hr/2    ;  sr += 1
                    if dbg: self.dumpLabel(row, i, sp, sl, sr, sc, sq, su, 'resize Row')
                    i += 1
                    nc, ic, xc, yc, wc, hc, gc, mxc, myc = self.geom(row, C)
                    for c in range(nc):
                        col = self.cols[sc]
                        col.width = wc  ;  col.height = hc
                        col.x = row.x - row.width/2 + (wc+xc)*c + wc/2
                        col.y = row.y + row.height  - (hc+yc)             ;  sc += 1
                        if dbg: self.dumpLabel(col, i, sp, sl, sr, sc, sq, su, 'resize Col')
                        i += 1
        if dbg: self.dumpLabels('resize')
        self.log('(END) lnl={} cps={}'.format(self.lnl(), self.cps()))
#        self.log('(END) lnl={} cpp={} cpl={} cpr={} cpq={}'.format(lnl, cpp, cpl, cpr, cpq))
    ####################################################################################################################################################################################################
    def dumpSprites(self, why=''):
        n = self.n
        self.log('(BGN) n={} {}'.format(fmtl(n), why))
        self.dumpSprite()
        i, sp, sl, sr, sc, sq, su = 0, 0, 0, 0, 0, 0, 0
        for p in range(n[P]):
            sp += 1             ; self.dumpSprite(self.sprites[i], i+1, sp, sl, sr, sc, sq, su, 'Page') ; i += 1
            for l in range(n[L]):
                sl += 1         ; self.dumpSprite(self.sprites[i], i+1, sp, sl, sr, sc, sq, su, 'Line') ; i += 1
                for q in range(QQ):
                    sq += 1     ; self.dumpSprite(self.sprites[i], i+1, sp, sl, sr, sc, sq, su, 'QRow') ; i += 1
#                    for c in range(n[K]):
#                        sc += 1 ; self.dumpSprite(self.sprites[i], i+1, '{:2} {:2} {:2} {:3}'.format(sp, sl, sq, sr)) ; i += 1
                for r in range(n[R]):
                    sr += 1     ; self.dumpSprite(self.sprites[i], i+1, sp, sl, sr, sc, sq, su, 'Row') ; i += 1
#                    for c in range(n[K]):
#                        sc += 1 ; self.dumpSprite(self.sprites[i], i+1, '{:2} {:2} {:2} {:3} {:4}  {:16}'.format(sp, sl, sq, sr, sc, why)) ; i += 1
        self.dumpSprite()
        self.log('(END) n={} {}'.format(fmtl(n), why))

    def dumpLabels(self, why='', dbg=0):
        np, nl, nr, nc, nk = self.n
        i, sp, sl, sr, sc, sq, su = 0, 0, 0, 0, 0, 0, 0
        if dbg: self.log('(BGN) n={} {}'.format(self.n, why))
        self.dumpLabel()
        for p in range(np):
            sp += 1              ;  self.dumpLabel(self.labels[i], i+1, sp, sl, sr, sc, sq, su, '{} Page'.format(why))  ;  i += 1
            for l in range(nl):
                sl += 1          ;  self.dumpLabel(self.labels[i], i+1, sp, sl, sr, sc, sq, su, '{} Line'.format(why))  ;  i += 1
                for q in range(QQ):
                    sq += 1      ;  self.dumpLabel(self.labels[i], i+1, sp, sl, sr, sc, sq, su, '{} QRow'.format(why))  ;  i += 1
                    for u in range(nk):
                        su += 1  ;  self.dumpLabel(self.labels[i], i+1, sp, sl, sr, sc, sq, su, '{} QCol'.format(why))  ;  i += 1
                for r in range(nr):
                    sr += 1      ;  self.dumpLabel(self.labels[i], i+1, sp, sl, sr, sc, sq, su, '{} Row'.format(why))  ;  i += 1
                    for c in range(nk):
                        sc += 1  ;  self.dumpLabel(self.labels[i], i+1, sp, sl, sr, sc, sq, su, '{} Col'.format(why))  ;  i += 1
        self.dumpLabel()
        if dbg: self.log('(END) n={} {})'.format(self.n, why))
    ####################################################################################################################################################################################################
    def dumpSprite(self, s=None, sid=-1, p=-1, l=-1, r=-1, c=-1, q=-1, u=-1, why=''):
        if s is None: self.log('sid  p  l  r   c  q   u     x      xc        y      yc        w       h    iax  iay    m      mx     my     rot   red grn blu opc v       why            group       parent', ind=0); return
        f = '{:4} {} {:2} {:2} {:3} {:2} {:3} {:7.2f} {:7.2f}  {:7.2f} {:7.2f}  {:7.2f} {:7.2f} {:4} {:4} {:6.3f} {:6.3f} {:6.3f} {:7.2f}  {:3} {:3} {:3} {:3} {:1} {:16} {} {}'
        k, o, v, g, pg = s.color, s.opacity, s.visible, s.group, s.group.parent
        xc, yc = s.x + s.width/2, s.y + s.height/2
        fs = f.format(sid, p, l, r, c, q, u, s.x, xc, s.y, yc, s.width, s.height, s.image.anchor_x, s.image.anchor_y, s.scale, s.scale_x, s.scale_y, s.rotation, k[0], k[1], k[2], o, v, why, g, pg)
        self.log(fs, ind=0)
        assert(type(s) == pyglet.sprite.Sprite)

    def dumpLabel(self, a=None, lid=-1, p=-1, l=-1, r=-1, c=-1, q=-1, u=-1, why=''):
        if a is None: self.log('lid  p  l  r   c  q   u text       x       y       w       h      font name     siz dpi bld itl red grn blu opc  why', ind=0) ; return
        x, y, w, h, n, d, s, k, b, i, t = a.x, a.y, a.width, a.height, a.font_name, a.dpi, a.font_size, a.color, a.bold, a.italic, a.text
        f = '{:4} {} {:2} {:2} {:3} {:2} {:3} {:6} {:7.2f} {:7.2f} {:7.2f} {:7.2f}  {:16} {:2} {:3}  {:1}   {:1}  {:3} {:3} {:3} {:3}  {}'
        fs = f.format(lid, p, l, r, c, q, u, t, x, y, w, h, n, s, d, b, i, k[0], k[1], k[2], k[3], why)
        self.log(fs, ind=0)
    ####################################################################################################################################################################################################
    def createCursor(self, g):
        cc, cr = self.cursorCol(1), self.cursorRow(1)
        self.log('(BGN) cc={} cr={}'.format(cc, cr))
        tc = self.cols[cc]  ;  tr = self.cols[cr]
        xc, yc, wc, hc = tc.x, tc.y, tc.width, tc.height
        xr, yr, wr, hr = tr.x, tr.y, tr.width, tr.height
        xc -= wc/2  ;  yc += hc/2
        self.log('cc={:4} x={:6.1f} y={:6.1f} w={:6.1f} h={:6.1f} i={}'.format(cc, xc, yc, wc, hc, fmtl(self.i)))
        self.log('cr={:4} x={:6.1f} y={:6.1f} w={:6.1f} h={:6.1f} i={}'.format(cr, xr, yr, wr, hr, fmtl(self.i)))
        self.dumpSprite()
        self.cursor = self.createSprite(self.sprites, xc, yc, wc, hc, CC, g, why='cursor', v=1)
        self.dumpSprite(self.cursor, why='{:2} {:2} {:2} {:3}'.format(-1, -1, -1, -1))
        self.log('(END) cc={} cr={}'.format(cc, cr))

    def resizeCursor(self):
        cc, cr = self.cursorCol(), self.cursorRow()
        self.log('(BGN) cc={} cr={}'.format(cc, cr))
        tc = self.cols[cc]  ;  tr = self.cols[cr]
        xc, yc, wc, hc = tc.x, tc.y, tc.width, tc.height
        xr, yr, wr, hr = tr.x, tr.y, tr.width, tr.height
        self.log('cc={:4} x={:6.1f} y={:6.1f} w={:6.1f} h={:6.1f} i={}'.format(cc, xc, yc, wc, hc, fmtl(self.i)))
        self.log('cr={:4} x={:6.1f} y={:6.1f} w={:6.1f} h={:6.1f} i={}'.format(cr, xr, yr, wr, hr, fmtl(self.i)))
        self.cursor.update(x=xc - wc/2, y=yc + hc/2, scale_x=wc/self.w[C], scale_y=hc/self.h[C])
        self.log('(END) cc={} cr={}'.format(cc, cr))
    ####################################################################################################################################################################################################
    def resizeFonts(self):
        ms = self.minSize()  ;  slope, off = 0.6, -1
        fs = fri(ms * slope + off)  ;  formula = '(fs = ms*slope+off)'
        self.log('{} {} ms={:4.1f} slope={} off={} fs={:4.1f}={:2}'.format(self.fmtWH(), formula, ms, slope, off, fs, fri(fs)))
        self.setFontParam('font_size', fs, 'fontSize')

    def minSize(self):
        cc = self.cursorCol()  ;  cr = self.cursorRow()  ;  w = self.cols[cc].width  ;  h = self.cols[cc].height  ;  m = min(w, h)
        self.log('cc={:4} cr={:4} w={:5.1f} h={:5.1f} m={:5.1f}'.format(cc, cr, w, h, m))
        return m

    def fontParams(self):    return self.fontBold, self.fontColorIndex, self.fontDpiIndex, self.fontItalic, self.fontNameIndex, self.fontSize

    def dumpFont(self, why=''):
        b, c, dpi, i, n, s = self.fontParams()
        pix = FONT_SCALE * s / dpi
        self.log('({}) {} {}DPI {}pt {} ({:6.3f}*{}pt/{}DPI)={:6.3f}pixels'.format(why, c, dpi, s, n, FONT_SCALE, s, dpi, pix))

    def setFontParam(self, n, v, m):
        setattr(self, m, v)
        self.log('n={} v={:.1f} m={}'.format(n, v, m))
        if SPRITES:
            self._setFontParam(self.cols, n, v, m)
            if QQ: self._setFontParam(self.ucols, n, v, m)
        else: self._setFontParam(self.labels, n, v, m)

    @staticmethod
    def _setFontParam(p, n, v, m):
        for j in range(len(p)):
            setattr(p[j], n, FONT_NAMES[v] if m == 'fontNameIndex' else FONT_COLORS[v] if m == 'fontColorIndex' else FONT_DPIS[v] if m == 'fontDpiIndex' else v)
    ####################################################################################################################################################################################################
    def on_draw(self):
        self.clear()
        self.batch.draw()

    def kpEvntTxt(self):
        return '{:8} {:8}     {:14} {:2} {:28}'.format(self.kbk, self.symb, self.symbStr, self.mods, self.modsStr)

    def on_key_press(self, symb, mods):
        self.symb, self.mods, self.symbStr, self.modsStr = symb, mods, pygwink.symbol_string(symb), pygwink.modifiers_string(mods)
        self.kbk = self.symbStr  ;  kbk = self.kbk
        self.log('(BGN) {}'.format(self.kpEvntTxt()))
        if                  self.isTab(kbk):                          self.addTab(kbk,  'on_key_press')
        elif kbk == 'Q' and self.isCtrl(mods) and self.isShift(mods): self.quit(        'keyPress({})'.format(kbk))
        elif kbk == 'Q' and self.isCtrl(mods):                        self.quit(        'keyPress({})'.format(kbk))
        elif kbk == 'B' and self.isCtrl(mods) and self.isShift(mods): self.setFontParam('bold',   not self.fontBold,   'fontBold')
        elif kbk == 'B' and self.isCtrl(mods):                        self.setFontParam('bold',   not self.fontBold,   'fontBold')
        elif kbk == 'I' and self.isCtrl(mods) and self.isShift(mods): self.setFontParam('italic', not self.fontItalic, 'fontItalic')
        elif kbk == 'I' and self.isCtrl(mods):                        self.setFontParam('italic', not self.fontItalic, 'fontItalic')
        elif kbk == 'S' and self.isCtrl(mods) and self.isShift(mods): self.setFontParam('font_size', (self.fontSize + 1)       % 52,               'fontSize')
        elif kbk == 'S' and self.isCtrl(mods):                        self.setFontParam('font_size', (self.fontSize - 1)       % 52,               'fontSize')
        elif kbk == 'D' and self.isCtrl(mods) and self.isShift(mods): self.setFontParam('dpi',       (self.fontDpiIndex + 1)   % len(FONT_DPIS),   'fontDpiIndex')
        elif kbk == 'D' and self.isCtrl(mods):                        self.setFontParam('dpi',       (self.fontDpiIndex - 1)   % len(FONT_DPIS),   'fontDpiIndex')
        elif kbk == 'N' and self.isCtrl(mods) and self.isShift(mods): self.setFontParam('font_name', (self.fontNameIndex + 1)  % len(FONT_NAMES),  'fontNameIndex')
        elif kbk == 'N' and self.isCtrl(mods):                        self.setFontParam('font_name', (self.fontNameIndex - 1)  % len(FONT_NAMES),  'fontNameIndex')
        elif kbk == 'C' and self.isCtrl(mods) and self.isShift(mods): self.setFontParam('color',     (self.fontColorIndex + 1) % len(FONT_COLORS), 'fontColorIndex')
        elif kbk == 'C' and self.isCtrl(mods):                        self.setFontParam('color',     (self.fontColorIndex + 1) % len(FONT_COLORS), 'fontColorIndex')
        elif kbk == 'F' and self.isCtrl(mods) and self.isShift(mods): self.toggleFullScreen()
        elif kbk == 'F' and self.isCtrl(mods):                        self.toggleFullScreen()
#        self.updateCaption()
        self.log('(END) {}'.format(self.kpEvntTxt()))

    def on_text(self, text):
        self.kbk = text
        self.log('(BGN) {}'.format( self.kpEvntTxt()))
        if self.isTab(self.kbk):                         self.addTab(self.kbk, 'on_text')
        if self.kbk=='$' and self.isShift(self.mods):    self.snapshot()
#        self.updateCaption()
        self.log('(END) {}'.format( self.kpEvntTxt()))

    def on_text_motion(self, motion, dbg=0):
        self.kbk = motion
        if dbg: self.log('(BGN) {}'.format(self.kpEvntTxt()))
        if self.mods == 0:
            if   motion == pygwink.MOTION_LEFT:          self.move(-1)
            elif motion == pygwink.MOTION_RIGHT:         self.move( 1)
            elif motion == pygwink.MOTION_UP:            self.move(-self.cpr)
            elif motion == pygwink.MOTION_DOWN:          self.move( self.cpr)
            elif motion == pygwink.HOME:                 pass
            elif motion == pygwink.END:                  pass
#            elif motion==pygwink.MOTION_PREVIOUS_PAGE: self.move() # prevPage(self.i[P], motion)
#            elif motion==pygwink.MOTION_NEXT_PAGE:     self.move() # nextPage(self.i[P], motion)
            else:                                      self.log('on_text_motion() motion={} ???'.format(motion))
#            self.updateCaption()
        if dbg: self.log('(END) {}'.format(self.kpEvntTxt()))
    ####################################################################################################################################################################################################
    def move(self, c, dbg=1):
        n, i, cc, cr = self.n, self.i, self.cursorCol(), self.cursorRow()  ;  k = cc + c
        if dbg: self.log('(BGN) {:4}    {:4}    {:4}    {:4}             i={}'.format(c, k, cc, cr, fmtl(i)), file=sys.stdout)
        self.updateI(c)
        kk = k % self.cpp# + k // self.cpp
        t = self.cols[kk]
        self.cursor.update(x=t.x - t.width/2, y=t.y + t.height/2)
        if dbg: self.log('(END) {:4}    {:4}    {:4}    {:4}             i={}'.format(c, kk, self.cursorCol(), self.cursorRow(), fmtl(i)), file=sys.stdout)

    def updateI(self, c, dbg=1):
        n, i = self.n, self.i  ;  cpp, cpl, cpr, cpq = self.cps()
        if dbg: self.log('(BGN) {:4} cps{} rps{} i={}'.format(c, fmtl(self.cps()), fmtl(self.rps()), fmtl(i)), file=sys.stdout)
        sc        = i[C] + c
        self.i[C] = sc %  cpr
        sr        = sc // cpr + i[R]
        self.i[R] = sr %  n[R]
        sl        = sr // n[R] + i[L]
        self.i[L] = sl %  n[L]
        sp        = sl // n[L] + i[P]
        self.i[P] = sp %  n[P]
#        self.i[C] = sp // n[P] + self.i[C]
        if dbg: self.log('(END) {:4} sc={:4} sr={:4}   sl={:4} sp={:4}   i={}'.format(c, sc, sr, sl, sp, fmtl(i)), file=sys.stdout)
    '''
    def nextPage(self, i, motion):
        self.pages[i].visible = False
        self.updatePage(i+1, '{}=MOTION_NEXT_PAGE   '.format(motion))

    def prevPage(self, i, motion):
        self.pages[i].visible = False
        self.updatePage(i-1, '{}=MOTION_PREVIOUS_PAGE'.format(motion))

    def updatePage(self, i, why):
        i = i % self.n[P]
        self.pages[i].visible = True
        self.log('{} i[{}]={}'.format(why, P, i))
        self.i[P] = i
    '''
    ####################################################################################################################################################################################################
    def addTab(self, kbk, why=''):
        self.log('(BGN) {} i={} {}'.format(self.kpEvntTxt(), fmtl(self.i), why), file=sys.stdout)
        self.updateData(kbk)
        self.updateTab( kbk)
        self.snapshot()
        self.log('(END) {} i={} {}'.format(self.kpEvntTxt(), fmtl(self.i), why), file=sys.stdout)

    def on_mouse_release(self, x, y, button, modifiers):  # pyglet.window.mouse.MIDDLE #pyglet.window.mouse.LEFT #pyglet.window.mouse.RIGHT
        n, i = self.n, self.i  ;  np, nl, nq, nr, nc, nk = n
        cc = self.cursorCol()  ;  cr = self.cursorRow()  ;  cps = self.cps()  ;  cpp, cpl, cpr, cpq = cps
        w = self.ww/nk  ;  h = self.hh/((nr + nq)*nl)   ;  y0 = y  ;  y = self.hh - y
        c = int(x/w)    ;  r = int(y/h)
        k = self.i[P]*cpp + self.i[L]*cpl + self.i[R]*cpr + self.i[C]
        self.log('(BGN) k={:4} cc={} cr={} i={}'.format(k, cc, cr, fmtl(i)))
        self.log('b={} m={} x={:4} y0={:4} y={:4} w={:6.2f} h={:6.2f} c={:4} r={:4}'.format(button, modifiers, x, y0, y, w, h, c, r))
        self.log('cps={} rps={}'.format(self.cps(), self.rps()))
        self.i[C] = c   ;   self.i[L] = r//(nq + nr)  ;  self.i[R] = r % (nq + nr)
        k = self.i[P]*cpp + self.i[L]*cpl + self.i[R]*cpr + self.i[C]
        self.cursor.update(self.cols[k].x, self.cols[k].y)
        cc, cr = self.cursorCol(), self.cursorRow()
        self.log('(END) k={:4} cc={} cr={} i={}'.format(k, cc, cr, fmtl(i)))

    def updateData(self, text, dbg=0):
        cc = self.cursorCol(1)
        p, l, q, r, c = self.i
        t = self.data[l][c]
        self.log('(BGN) text={} cc={} i={} self.data[l][c]={}'.format(text, cc, fmtl(self.i), self.data[l][c]), file=sys.stdout)
        self.data[l][c] = t[0:r] + text + t[r+1:]
        if dbg: self.dumpData(why='updateData text={} cc={} i={} data[l][c]={}'.format(text, cc, self.i, self.data[l][c]))
        self.log('(END) text={} cc={} i={} self.data[l][c]={}'.format(text, cc, fmtl(self.i), self.data[l][c]), file=sys.stdout)

    def updateTab(self, text, dbg=1):
        cr = self.cursorRow(1)
        self.log('(BGN) text={} cr={} tabs[cr].text={}'.format(text, cr, self.cols[cr].text), file=sys.stdout)
        self.cols[cr].text = text
        if dbg: self.cols[cr].color = FONT_COLORS[self.fontColorIndex + 4]
        self.log('(END) text={} cr={} tabs[cr].text={}'.format(text, cr, self.cols[cr].text), file=sys.stdout)

    def updateCaption(self):
        fb, fc, fd, fi, fn, fs = self.fontParams()
        text = '{}dpi {}pt {} {}'.format(fd, fs, fn, fc)
        self.log('{}'.format(text))
        self.set_caption(text)
    ####################################################################################################################################################################################################
    def toggleFullScreen(self):
        global FULL_SCREEN
        FULL_SCREEN =  not  FULL_SCREEN
        self.set_fullscreen(FULL_SCREEN)
        self.log('FULL_SCREEN={}'.format(FULL_SCREEN))
    ####################################################################################################################################################################################################
    @staticmethod
    def isCtrl(mods):        return mods&pygwink.MOD_CTRL
    @staticmethod
    def isShift(mods):       return mods&pygwink.MOD_SHIFT
    @staticmethod
    def isAlt(mods):         return mods&pygwink.MOD_ALT
    @staticmethod
    def isTab(text):         return True if text=='-' or Tabs.isFret(text)   else False
    @staticmethod
    def isFret(text):        return True if '0'<=text<='9' or 'a'<=text<='o' else False
    ####################################################################################################################################################################################################
    @staticmethod
    def ordSfx(n):
        m = n % 10
        if   m == 1 and n != 11: return 'st'
        elif m == 2 and n != 12: return 'nd'
        elif m == 3 and n != 13: return 'rd'
        else:                    return 'th'
    ####################################################################################################################################################################################################
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
        if f == 'log': si = inspect.stack(0)[2];  p = pathlib.Path(si.filename);  n = p.name;  l = si.lineno;  f = si.function;  t = ''
        if ind: print('{:20} {:5} {:7} {} {:>20} '.format(self.indent(), l, n, t, f), file=file, end='')
        print('{}'.format(msg), file=file, flush=flush, sep=sep, end=end) if ind else print('{}'.format(msg), file=file, flush=flush, sep=sep, end=end)
        if file != LOG_FILE: self.log(msg, ind)
    ####################################################################################################################################################################################################
    def quit(self, why=''):
        self.log('(BGN)')
        text = '\n' + '###   Quit   ###' * 13 + '\n'
        self.log(text)
        self.dumpStruct('quit ' + why)
        self.snapshot()
        self.log(text)
        self.dumpStack(inspect.stack())
        self.log(text)
        self.dumpStack(MAX_STACK_FRAME)
        self.log('(END) closing LOG_FILE={}'.format(LOG_FILE.name))
        if not LOG_FILE.closed: LOG_FILE.close()
        exit()
    ####################################################################################################################################################################################################
    @staticmethod
    def deleteList(l): # Not Used
        j = 0
        while j < len(l): t = l[j];  t.delete();  del l[j]
########################################################################################################################################################################################################
if __name__ == '__main__':
    with open(str(LOG_PATH), 'w') as LOG_FILE:
        tabs          = Tabs()
        pyglet.app.run()
