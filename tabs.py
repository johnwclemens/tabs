import inspect, math, sys, os, glob, pathlib#, shutil#, unicodedata, readline, csv
import pyglet
import pyglet.window.key as pygwink
import pyglet.window.event as pygwine
sys.path.insert(0, os.path.abspath('../lib'))
import cmdArgs
####################################################################################################################################################################################################
CHECKER_BOARD = 0  ;  EVENT_LOG = 1  ;  FULL_SCREEN = 1  ;  ORDER_GROUP = 1  ;  RESIZE = 1  ;  SEQ_LOG_FILES = 1  ;  SUBPIX = 1
VRSN1            = 1  ;  SFX1 = chr(65 + VRSN1)  ;  QQ      = VRSN1  ;  VRSNX1 = 'VRSN1={}       QQ={}  SFX1={}'.format(VRSN1, QQ,      SFX1)
VRSN2            = 0  ;  SFX2 = chr(49 + VRSN2)  ;  SPRITES = VRSN2  ;  VRSNX2 = 'VRSN2={}  SPRITES={}  SFX2={}'.format(VRSN2, SPRITES, SFX2)
VRSN3            = 0  ;  SFX3 = chr(97 + VRSN3)  ;  ZZ      = VRSN3  ;  VRSNX3 = 'VRSN3={}       ZZ={}  SFX3={}'.format(VRSN3, ZZ,      SFX3)
#SFX              = '.' + SFX1 + '.' + SFX2 + '.' + SFX3
#SFX              = '.{}.{}.{}'.format(SFX1, SFX2, SFX3)
SFX              = f'.{SFX1}.{SFX2}.{SFX3}'
PATH             = pathlib.Path(sys.argv[0])
BASE_PATH        = PATH.parent
BASE_NAME        = BASE_PATH.stem
SNAP_DIR         = 'snaps' ;         SNAP_SFX      = '.png'
CCC              = 3
FMTN             = (1, 1, 2, 3, 1, 3)
P, L, R, C       = 0, 1, 2, 3
S, LCOL, LLINE   = ' ', 'Col', 'Line '
INIT             = '###   Init   ###' * 13
QUIT             = '###   Quit   ###' * 13
OPACITY          = [255, 240, 225, 210, 190, 165, 140, 110, 80]
GRAY             = [(255, 255, 255, OPACITY[0]), ( 0,  0,  0, OPACITY[0])]
PINK             = [(255,  64, 192, OPACITY[0]), (57, 16, 16, OPACITY[0])]
INFRA_RED        = [(255,  29,  24, OPACITY[0]), (68, 20, 19, OPACITY[0])]
RED              = [(255,  24,  21, OPACITY[0]), (88, 15, 12, OPACITY[0])]
ORANGE           = [(255, 200,  16, OPACITY[0]), (76, 30, 25, OPACITY[0])]
YELLOW           = [(255, 255,  15, OPACITY[0]), (45, 41, 10, OPACITY[0])]
GREEN            = [( 44, 255,   0, OPACITY[0]), (21, 54, 10, OPACITY[0])]
GREEN_BLUE       = [( 24, 255,  61, OPACITY[0]), (10, 49, 25, OPACITY[0])]
CYAN             = [( 32, 255, 255, OPACITY[0]), (16, 64, 64, OPACITY[0])]
BLUE_GREEN       = [( 25, 181, 255, OPACITY[0]), (12, 37, 51, OPACITY[0])]
BLUE             = [( 35,  26, 255, OPACITY[0]), (19, 11, 64, OPACITY[0])]
INDIGO           = [( 35,  26, 255, OPACITY[0]), (19, 11, 64, OPACITY[0])]
VIOLET           = [(176,  81, 255, OPACITY[0]), (44, 14, 58, OPACITY[0])]
ULTRA_VIOLET     = [(194,  96, 255, OPACITY[3]), (50, 19, 61, OPACITY[1])]
HUES             = 13  ;  MAX_STACK_DEPTH = 0  ;  MAX_STACK_FRAME = inspect.stack()
####################################################################################################################################################################################################
def fmtl(a, w=None, d1='[', d2=']'):
    c = ''
    for i in range(len(a)):
        if w is None: c += '{} '.format(a[i])
        else:         c += '{:{w}} '.format(int(a[i]), w=w[i])
    return d1 + c.rstrip() + d2
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
def fri(f): return int(math.floor(f + 0.5))
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
FONT_SCALE    = 123.42857
FONT_NAMES    = ['Times New Roman', 'Lucida Console', 'Courier New', 'Helvetica', 'Arial', 'Century Gothic', 'Bookman Old Style', 'Antique Olive']
FONT_COLORS   = [REDS[0], YELLOWS[0], GREENS[5], ORANGES[0], BLUES[0], CYANS[0], VIOLETS[0], PINKS[0], GREEN_BLUES[0], INFRA_REDS[0], ULTRA_VIOLETS[0], BLUE_GREENS[0], GRAYS[0], INDIGOS[0]]
FONT_DPIS     = [72, 78, 84, 90, 96, 102, 108, 114, 120]

class Tabs(pyglet.window.Window):
    def __init__(self):
        global FULL_SCREEN, SUBPIX, ORDER_GROUP
        SNAP_GLOB_ARG = str(BASE_PATH / SNAP_DIR / BASE_NAME) + SFX + '.*' + SNAP_SFX
        SNAP_GLOB     = glob.glob(SNAP_GLOB_ARG)
        self.log('(BGN) {}'.format(__class__))
        self.log('{}'.format(VRSNX1))
        self.log('{}'.format(VRSNX2))
        self.log('{}'.format(VRSNX3))
        self.log('CHECKER_BOARD={} EVENT_LOG={} FULL_SCREEN={} ORDER_GROUP={} RESIZE={} SEQ_LOG_FILES={} SUBPIX={}'.format(CHECKER_BOARD, EVENT_LOG, FULL_SCREEN, ORDER_GROUP, RESIZE, SEQ_LOG_FILES, SUBPIX))
        self.log('SNAP_GLOB_ARG={}'.format(SNAP_GLOB_ARG))
        self.log('    SNAP_GLOB={}'.format(SNAP_GLOB))
        self.delGlob(SNAP_GLOB, 'SNAP_GLOB')
        self.ww, self.hh  = 640, 480
        self.n, self.i, self.x, self.y, self.w, self.h, self.g = [1, 3, 6, 20], [1, 3, 2, 1], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], []
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
        self.log('[n]            n={}'.format(fmtl(self.n, FMTN)))
        self.log('[i]            i={}'.format(fmtl(self.i, FMTN)))
        self.log('[x]            x={}'.format(fmtl(self.x)))
        self.log('[y]            y={}'.format(fmtl(self.y)))
        self.log('[w]           ww={}'.format(self.ww))
        self.log('[h]           hh={}'.format(self.hh))
        self.log('[f]  FULL_SCREEN={}'.format(FULL_SCREEN))
        self.log('[g]  ORDER_GROUP={}'.format(ORDER_GROUP))
        self.log('[s]       SUBPIX={}'.format(SUBPIX))
        self.fontBold, self.fontItalic, self.fontColorIndex, self.fontDpiIndex, self.fontSize, self.fontNameIndex = 0, 0, 0, 4, 14, 0
        self.dumpFont()
        self._initWindowA()
        super().__init__(screen=self.screens[1], fullscreen=FULL_SCREEN, resizable=True, visible=False)
        self._initWindowB()
        self.symb, self.symbStr, self.mods, self.modsStr, self.kbk = 0, '', 0, '', 0
        self.cc, self.ci, self.SNAP0, self.armSnap = 0, 0, 0, ''
        self.blankCol = ''
        self.cursor, self.caret = None, None
        self.data = []
        self._init()
        self.log('(END) {} {} {}'.format(__class__, VRSNX1, VRSNX2))
        self.log('{}'.format(INIT), ind=0)

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
        self.cpr =  self.n[C] + CCC
        self.cpl = (self.n[R] + QQ) * self.cpr
        self.cpp =  self.n[L] * self.cpl
        if dbg: self.log('cps={}'.format(fmtl(self.cps())))

    def cps(self): return self.cpp, self.cpl, self.cpr
    def lnl(self): return list(map(len, [self.pages, self.lines, self.rows, self.cols, self.qrows, self.ucols]))
    def snl(self): return sum(self.lnl())
#    def szs(self): return self.lnl().append(len(self.acols))
    def j(self):   return [ i-1 if i else 0 for i in self.i ]
#    def m(self):   return [ n for n in self.n ]

    @staticmethod
    def fmtDataDim(d): return '({} x {} x {})={:8,} tabs'.format(len(d), len(d[0]), len(d[0][0]), len(d)*len(d[0])*len(d[0][0]))
    def fmtGeom(self): return '{} {} {} {} {}'.format(fmtl(self.n, FMTN), fmtl(self.lnl()), self.snl(), self.cc, fmtl(self.i, FMTN))
    ####################################################################################################################################################################################################
    def _init(self, dbg=1):
        self.pages, self.lines, self.rows, self.cols  = [], [], [], []
        self.qrows, self.ucols, self.acols            = [], [], []
        self.data, self.labels, self.sprites          = [], [], []
        self.log('(BGN) {}'.format(self.fmtGeom()))
        self.kc  = [GRAYS[7], GRAYS[11]] if CHECKER_BOARD else [GRAYS[7]]
        kb = [self.kc[0]]  ;  self.kp  = kb  ;  self.kl = kb  ;  self.kq = kb  ;  self.kr = kb  ;  self.ku = kb
        self.ssi = 0
        self._initCps()
        self.readDataFile()
        if QQ:
            self.labelTextA, self.labelTextB = ['R', 'M', '@'], ['R', 'M', '@']
            self.labelTextA.extend('{}'.format(j) for j in range(1, self.n[C] + 1))
            self.labelTextB.extend('{}'.format(j % 10 if j % 10 else j // 10 % 10) for j in range(1, self.n[C] + 1))
            texts = list(zip(self.labelTextA, self.labelTextB))
            self.dumpLabelText(texts)
        self.createSprites() if SPRITES else  self.createLabels()
        self.createCursor(self.g[C+3])
        if dbg: self.dumpStruct('_init')
        self.log('(END) {}'.format(self.fmtGeom()))
    ####################################################################################################################################################################################################
    def on_resize(self, width, height):
        super().on_resize(width, height)
        self.ww, self.hh = width, height
        if not RESIZE: return
        self.log('(BGN) {} {}'.format(self.fmtWH(), self.fmtDataDim(self.data)))
        self.resizeSprites() if SPRITES else self.resizeLabels()
        self.resizeFonts()
        self.resizeCursor()
#        self.snapshot()
#        self.dumpStruct('on_resize()')
        self.updateCaption(self.fmtf())
        self.log('(END) {} {}'.format(self.fmtWH(), self.fmtDataDim(self.data)))
    ####################################################################################################################################################################################################
    def dumpStruct(self, why=''):
        self.log('(BGN) {}'.format(why))
#        self.dumpData(why)
        if SPRITES: self.dumpSprites()
        self.dumpLabels(why)
        self.dumpUCols(why)
        self.dumpCols(why)
        self.dumpACols(why)
        self.dumpFont(why)
        self.log('(END) {}'.format(why))
    ####################################################################################################################################################################################################
    def readDataFile(self, dbg=1):
        nl, nr, nc = self.n[L], self.n[R], self.n[C]
        DATA_DIR  = 'data'    ;                  DATA_SFX = '.dat'  ;  DATA_PFX = '.{}'.format(nc)  ;  nc += CCC
        DATA_NAME = BASE_NAME + SFX + DATA_PFX + DATA_SFX
        DATA_PATH = BASE_PATH / DATA_DIR / DATA_NAME
        if dbg: self.log('nl={} nr={} nc={}'.format(nl, nr, nc))
        with open(str(DATA_PATH), 'r') as DATA_FILE:
            DATA_FILE.seek(0, 2)  ;  size = DATA_FILE.tell()            ;  DATA_FILE.seek(0, 0)
            self.log('(BGN) {:40} {:8,} bytes = {:4,.0f} KB'.format(DATA_FILE.name, size, size/1024))
            strings = []
#            for l in range(1, nl+1):
#                for r in range(1, nr+1):
            l, r, c = 1, 0, 0
            while l <= nl:
                s = DATA_FILE.readline().strip()
#                c = len(s)
                if len(s): strings.append(s)  ;  r += 1  ;  c = len(s)
                else:
                    self.data.append(strings)
                    strings=[]
                    self.log('read    {:2}{} line with {:6,} cols on {:4,} strings {:8,} tabs'.format(l, self.ordSfx(l), c, r, c*r))
                    if l == nl: break
                    r = 0
                    l += 1
#                    if r == 1: self.log('reading {:2}{} line'.format(l, self.ordSfx(l)))
#                    self.log('reading            {:2}{} string'.format(r, self.ordSfx(r)))
                if c:  self.log('l={} r={} c={}: {}'.format(l, r, c, s))
#        nl = len(self.data)  ;  nr = len(self.data[0])  ;  nc = len(self.data[0][0])o
        nt = l*c*r
        vdf = self.isVertDataFrmt(self.data)  ;  self.blankCol = '-' * r
        self.log('read     {:2} lines with {:6,} cols on {:4,} strings {:8,} tabs, vdf={} blankCol({})={}'.format(l, l*c, l*r, nt, vdf, len(self.blankCol), self.blankCol))
        if dbg: self.dumpDataH(self.data)
        self.data = self.transpose(self.data)
        vdf       = self.isVertDataFrmt(self.data)
        if dbg: self.dumpDataV(self.data)
        self.log('assert: size=nt+2*(l*r+l-1) {:8,} + {} = {:8,} bytes'.format(nt, 2 * (l * r + l - 1), size))  ;  assert size == nt + 2 * (l * r + l - 1)  ;  assert vdf
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
    def geom(self, p=None, j=0, init=0, dbg=1):
        mx, my = None, None
        n, i, x, y, w, h, g = self.n[j], self.i[j], self.x[j], self.y[j], self.w[j], self.h[j], self.g[j]
        if   j == R:   n += QQ
        elif j == C:   n += CCC
        if p:
            if j == C: w, h = (p.width - x*(n + 1))/n,  p.height - y*2
            else:      w, h =  p.width - x*2,          (p.height - y*(n + 1))/n
        else:          w, h =  self.ww - x*2, self.hh - y*2
        if j != C:     x += p.x if p else self.x[P]
        if init:       self.w[j], self.h[j] = w, h
        else:          mx, my = w/self.w[j], h/self.h[j]
        if dbg:        self.dumpGeom(j, mx, my)
        return n, i, x, y, w, h, g, mx, my

    def dumpGeom(self, j, mx, my): self.log('j={} n={:3} i={:4} x={:3} y={:3} w={:7.2f} h={:7.2f} g={} mx={} my={}'.format(j, self.n[j], self.i[j], self.x[j], self.y[j], self.w[j], self.h[j], self.g[j], mx, my))
    ####################################################################################################################################################################################################
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
    ####################################################################################################################################################################################################
    def createSprites(self, dbg=1):
        self.log('(BGN) {}'.format(self.fmtGeom()))
        cp, cl, cr, cc, cq, cu = self.kp, self.kl, self.kr, self.kc, self.kq, self.ku
        np, ip, xp, yp, wp, hp, gp, mx, my = self.geom(None, P, init=1)
        if dbg: self.dumpSprite()
        for p in range(np):
            v = not p
            page = self.createSprite(self.pages, xp, yp, wp, hp, cp[p % len(cp)], gp, why='create Page', v=v, dbg=dbg)
            nl, il, xl, yl, wl, hl, gl, mx, my = self.geom(page, L, init=1)
            for l in range(nl):
                yl2 = page.y + page.height - (yl + hl)*(l + 1)
                line = self.createSprite(self.lines, xl, yl2, wl, hl, cl[l % len(cl)], gl, why='create Line', v=v, dbg=dbg)
                if QQ:
                    nq, iq, xq, yq, wq, hq, gq, mx, my = self.geom(line, R, init=1)
                    yq2 = line.y + line.height - (yq + hq)
                    qrow = self.createSprite(self.qrows, xq, yq2, wq, hq, cq[0], gq, why='create QRow', v=v, dbg=dbg)
                    nu, iu, xu, yu, wu, hu, gu, mx, my = self.geom(qrow, C, init=1)
                    if dbg: self.dumpSprite()  ;  self.dumpLabel()
                    for u in range(nu):
                        if ZZ: xu2 = qrow.x + (xu + wu)*(u + 1) - wu/2  ;  yu2 = qrow.y + qrow.height - (yu + hu) + hu/2
                        else:  xu2 = qrow.x + u*(xu + wu) + wu/2        ;  yu2 = yu + qrow.y + qrow.height - hu/2
#                            self.log('xu2={} xu3={} yu2={} yu3={}'.format(int(xu2), int(xu3), int(yu2), int(yu3)), file=sys.stdout)
                        self.createLabel(self.labelTextB[u], self.ucols, xu2, yu2, wu, hu, self.cci(u, cu), gu, why='create UCol', dbg=dbg)
                    if dbg: self.dumpLabel()  ;  self.dumpSprite()
                nr, ir, xr, yr, wr, hr, gr, mx, my = self.geom(line, R, init=1)
                for r in range(QQ, nr):
                    yr2 = line.y + line.height - (yr + hr)*(r + 1)
                    row = self.createSprite(self.rows, xr, yr2, wr, hr, cr[r % len(cr)], gr, why='create Row',  v=v, dbg=dbg)
                    nc, ic, xc, yc, wc, hc, gc, mx, my = self.geom(row, C, init=1)
                    if dbg: self.dumpSprite()         ;  self.dumpLabel()
                    for c in range(nc):
                        if ZZ: xc2 = row.x + (xc + wc)*(c + 1) - wc/2  ;  yc2 = row.y + row.height - (yc + hc) + hc/2
                        else:  xc2 = xc + row.x + c*(xc + wc) + wc/2   ;  yc2 = yc + row.y + row.height - hc/2
#                        self.log('xc2={} xc3={} yc2={} yc3={}'.format(int(xc2), int(xc3), int(yc2), int(yc3)), file=sys.stdout)
                        self.createLabel(self.data[l][c][r-QQ], self.cols, xc2, yc2, wc, hc, self.cci(c, cc), gc, why='create Col', dbg=dbg)
                    if dbg: self.dumpLabel()  ;  self.dumpSprite()
        self.log('(END) {}'.format(self.fmtGeom()))

    def createLabels(self, dbg=1):
        self.log('(BGN) {}'.format(self.fmtGeom()))
        np, ip, xp, yp, wp, hp, gp, mx, my = self.geom(None, P, init=1)
        if dbg: self.dumpLabel()
        for p in range(np):
            xp2 = xp + wp/2  ;          yp2 = yp + hp/2
            page = self.createLabel('Page', self.pages, xp2, yp2, wp, hp, P, gp, why='create Page', dbg=dbg)
            nl, il, xl, yl, wl, hl, gl, mx, my = self.geom(page, L, init=1)
            for l in range(nl):
                yl2 = page.y + page.height/2 - (yl + hl)*(l + 1) + hl/2
                line = self.createLabel('Line', self.lines, xl, yl2, wl, hl, L, gl, 'create Line', dbg=dbg)
                if QQ:
                    nq, iq, xq, yq, wq, hq, gq, mx, my = self.geom(line, R, init=1)
                    yq2 = line.y + line.height/2 - (yq + hq) + hq/2
                    qrow = self.createLabel('QRow', self.qrows, xq, yq2, wq, hq, C+1, gq, 'create QRow', dbg=dbg)
                    nu, iu, xu, yu, wu, hu, gu, mx, my = self.geom(qrow, C, init=1)
                    for u in range(nu):
                        xu2 = qrow.x - qrow.width/2 + (xu + wu)*u + wu/2  ;   yu2 = qrow.y + qrow.height - (yu + hu)
                        self.createLabel(self.labelTextB[u], self.ucols, xu2, yu2, wu, hu, self.cci(u, self.ku), gu, 'create UCol')
                nr, ir, xr, yr, wr, hr, gr, mx, my = self.geom(line, R, init=1)
                for r in range(QQ, nr):
                    yr2 = line.y + line.height/2 - (yr + hr)*(r + 1) + hr/2
                    row = self.createLabel('Row', self.rows, xr, yr2, wr, hr, R, gr, 'create Row', dbg=dbg)
                    nc, ic, xc, yc, wc, hc, gc, mx, my = self.geom(row, C, init=1)
                    for c in range(nc):
                        xc2 = row.x - row.width/2 + (xc + wc)*c + wc/2  ;       yc2 = row.y + row.height - (yc + hc)
                        self.createLabel(self.data[l][c][r-QQ], self.cols, xc2, yc2, wc, hc, self.cci(c, self.kc), gc, 'create Col', dbg=dbg)
        if dbg: self.dumpLabel()
        self.log('(END) {}'.format(self.fmtGeom()))
    ####################################################################################################################################################################################################
    def createSprite(self, p, x, y, w, h, cc, grp, why, v=0, dbg=0):
        scip = pyglet.image.SolidColorImagePattern(cc)
        img = scip.create_image(width=fri(w), height=fri(h))
        s = pyglet.sprite.Sprite(img, x, y, batch=self.batch, group=grp, subpixel=SUBPIX)
        s.visible = v
        s.color, s.opacity = cc[:3], cc[3]
        self.sprites.append(s)
        if p is not None:      p.append(s)
        if dbg: self.dumpSprite(s, len(self.sprites), *self.lnl(), why=why)
        return s

    def createLabel(self, text, p, x, y, w, h, kk, g, why, m=0, dbg=0):
        a, ax, ay = 'center', 'center', 'center' # left center right  # bottom baseline center top
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
        if p == self.cols or p == self.ucols: self.acols.append(ll)
        if dbg: self.dumpLabel(ll, len(self.labels), *self.lnl(), why=why)
        return ll
    ####################################################################################################################################################################################################
    def resizeSprites(self, dbg=0):
        self.log('(BGN) {}'.format(self.fmtGeom()))
        if dbg: self.dumpSprite()
        i, sp, sl, sr, sc, sq, su = 0, 0, 0, 0, 0, 0, 0
        np, ip, xp, yp, wp, hp, gp, mxp, myp = self.geom(None, P)
        for p in range(np):
            page = self.pages[sp]                                                                 ;  page.update(x=xp, y=yp, scale_x=mxp, scale_y=myp)  ;  sp += 1  ;  i += 1
            if dbg: self.dumpSprite(self.sprites[i-1], i, sp, sl, sr, sc, sq, su, 'resize Page')
            nl, il, xl, yl, wl, hl, gl, mxl, myl = self.geom(page, L)
            for l in range (nl):
                line = self.lines[sl]          ;  yl2 = page.y + page.height - (yl + hl)*(l + 1)  ;  line.update(x=xl, y=yl2, scale_x=mxl, scale_y=myl)  ;  sl += 1  ;  i += 1
                if dbg: self.dumpSprite(self.sprites[i-1], i, sp, sl, sr, sc, sq, su, 'resize Line')
                if QQ:
                    nq, iq, xq, yq, wq, hq, gq, mxq, myq = self.geom(line, R)
                    qrow = self.qrows[sq]  ;  yq2 = line.y + line.height - (yq + hq)  ;  qrow.update(x=xq, y=yq2, scale_x=mxq, scale_y=myq)  ;  sq += 1  ;  i += 1
                    if dbg: self.dumpSprite(self.sprites[i-1], i, sp, sl, sr, sc, sq, su, 'resize QRow')
                    nu, iu, xu, yu, wu, hu, gu, mxu, myu = self.geom(qrow, C)
                    for u in range(nu):
                        ucol = self.ucols[su]  ;  ucol.width = wu  ;  ucol.height = hu  ;  ucol.x = qrow.x + (xu + wu)*u + xu + wu/2  ;  ucol.y = qrow.y + qrow.height - yu - hu/2  ;  su += 1  ;  i += 1
                        if dbg: self.dumpLabel(ucol, su, sp, sl, sr, sc, sq, su, why='resize UCol')
                nr, ir, xr, yr, wr, hr, gr, mxr, myr = self.geom(line, R, dbg=1)
                for r in range(QQ, nr):
                    row = self.rows[sr]        ;  yr2 = line.y + line.height - (yr + hr)*(r + 1)  ;   row.update(x=xr, y=yr2, scale_x=mxr, scale_y=myr)  ;  sr += 1  ;  i += 1
                    if dbg: self.dumpSprite(self.sprites[i-1], i, sp, sl, sr, sc, sq, su, 'resize Row')
                    nc, ic, xc, yc, wc, hc, gc, mxc, myc = self.geom(row, C, dbg=1)
                    for c in range(nc):
                        col = self.cols[sc]  ;  col.width = wc  ;  col.height = hc  ;  col.x = row.x + (xc + wc)*c + xc + wc/2  ;  col.y = row.y + row.height - yc - hc/2  ;  sc += 1  ;  i += 1
                        if dbg: self.dumpLabel(col, sc, sp, sl, sr, sc, sq, su, 'resize Col')
        if dbg: self.dumpSprite()
        self.log('(END) {}'.format(self.fmtGeom()))

    def resizeLabels(self, dbg=0):
        self.log('(BGN) {}'.format(self.fmtGeom()))
        i, sp, sl, sr, sc, sq, su = 0, 0, 0, 0, 0, 0, 0
        np, ip, xp, yp, wp, hp, gp, mxp, myp = self.geom(None, P)
        for p in range(np):
            page = self.pages[sp]                  ;  page.width = wp  ;  page.height = hp  ;  page.x = xp + wp/2  ;  page.y = yp + hp/2  ;  sp += 1  ;  i += 1
            if dbg: self.dumpLabel(page, i-1, sp, sl, sr, sc, sq, su, 'resize page')
            nl, il, xl, yl, wl, hl, gl, mxl, myl = self.geom(page, L)
            for l in range(nl):
                line = self.lines[sl]              ;  line.width = wl  ;  line.height = hl  ;  line.x = xl  ;  line.y = page.y + page.height/2 - (yl + hl)*(l + 1) + hl/2  ;  sl += 1  ;  i += 1
                if dbg: self.dumpLabel(line, i-1, sp, sl, sr, sc, sq, su, 'resize line')
                if QQ:
                    nq, iq, xq, yq, wq, hq, gq, mxq, myq = self.geom(line, R)
                    qrow = self.qrows[sq]      ;  qrow.width = wq  ;  qrow.height = hq  ;  qrow.x = xq  ;  qrow.y = line.y + line.height/2 - (yq + hq) + hq/2  ;  sq += 1  ;  i += 1
                    if dbg: self.dumpLabel(qrow, i-1, sp, sl, sr, sc, sq, su, 'resize QRow')
                    nu, iu, xu, yu, wu, hu, gu, mxu, myu = self.geom(qrow, C)
                    for u in range(nu):
                        ucol = self.ucols[su]  ;  ucol.width = wu  ;  ucol.height = hu  ;  ucol.x = qrow.x - qrow.width/2 + (xu + wu)*u + wu/2  ;  ucol.y = qrow.y + qrow.height - (yu + hu)  ;  su += 1  ;  i += 1
                        if dbg: self.dumpLabel(ucol, i-1, sp, sl, sr, sc, sq, su, 'resize UCol')
                nr, ir, xr, yr, wr, hr, gr, mxr, myr = self.geom(line, R, dbg=1)
                for r in range(QQ, nr):
                    row = self.rows[sr]            ;   row.width = wr  ;   row.height = hr  ;   row.x = xr  ;   row.y = line.y + line.height/2 - (yr + hr)*(r + 1) + hr/2  ;  sr += 1  ;  i += 1
                    if dbg: self.dumpLabel(row, i-1, sp, sl, sr, sc, sq, su, 'resize Row')
                    nc, ic, xc, yc, wc, hc, gc, mxc, myc = self.geom(row, C, dbg=1)
                    for c in range(nc):
                        col = self.cols[sc]        ;   col.width = wc  ;   col.height = hc  ;   col.x = row.x - row.width/2 + (xc + wc)*c + wc/2  ;  col.y = row.y + row.height - (yc + hc)  ;  sc += 1  ;  i += 1
                        if dbg: self.dumpLabel(col, i-1, sp, sl, sr, sc, sq, su, 'resize Col')
        if dbg: self.dumpLabels('resize')
        self.log('(END) {}'.format(self.fmtGeom()))
    ####################################################################################################################################################################################################
    def dumpSprites(self, why=''):
        self.log('(BGN) {} {}'.format(self.fmtGeom(), why))
        np, nl, nr, nc = self.n
        self.dumpSprite()
        i, sp, sl, sr, sc, sq, su = 0, 0, 0, 0, 0, 0, 0
        for p in range(np):
            sp += 1             ; self.dumpSprite(self.sprites[i], i+1, sp, sl, sr, sc, sq, su, 'Page') ; i += 1
            for l in range(nl):
                sl += 1         ; self.dumpSprite(self.sprites[i], i+1, sp, sl, sr, sc, sq, su, 'Line') ; i += 1
                if QQ: sq += 1  ; self.dumpSprite(self.sprites[i], i+1, sp, sl, sr, sc, sq, su, 'QRow') ; i += 1
                for r in range(nr):
                    sr += 1     ; self.dumpSprite(self.sprites[i], i+1, sp, sl, sr, sc, sq, su, 'Row') ; i += 1
        self.dumpSprite()
        self.log('(END) {} {}'.format(self.fmtGeom(), why))

    def dumpUCols(self, why='', dbg=1):
        if dbg: self.log('(BGN) {} {})'.format(self.fmtGeom(), why))
        np, nl, nr, nc = self.n  ;  nc += CCC
        nu = QQ * nc
        i, sp, sl, sr, sc, sq, su = 0, 0, 0, 0, 0, 0, 0
        self.dumpLabel(idt='uid')
        for p in range(np):
            sp += 1
            for l in range(nl):
                sl += 1
                for u in range(nu):
                    su += 1  ;  self.dumpLabel(self.ucols[i], i+1, sp, sl, sr, sc, sq, u+1, why=why)  ;  i += 1
        self.dumpLabel(idt='uid')
        if dbg: self.log('(END) {} {})'.format(self.fmtGeom(), why))

    def dumpCols(self, why='', dbg=1):
        if dbg: self.log('(BGN) {} {})'.format(self.fmtGeom(), why))
        np, nl, nr, nc = self.n  ;  nc += CCC
        i, sp, sl, sr, sc, sq, su = 0, 0, 0, 0, 0, 0, 0
        self.dumpLabel(idt='cid')
        for p in range(np):
            sp += 1
            for l in range(nl):
                sl += 1
                for r in range(nr):
                    sr += 1
                    for c in range(nc):
                        sc += 1  ;  self.dumpLabel(self.cols[i],  i+1, sp, sl, sr, c+1, sq, su, why=why)  ;  i += 1
        self.dumpLabel(idt='cid')
        if dbg: self.log('(END) {} {})'.format(self.fmtGeom(), why))

    def dumpACols(self, why='', dbg=1):
        if dbg: self.log('(BGN) {} {})'.format(self.fmtGeom(), why))
        np, nl, nr, nc = self.n  ;  nc += CCC
        nu = QQ * nc
        i, sp, sl, sr, sc, sq, su = 0, 0, 0, 0, 0, 0, 0
        self.dumpLabel(idt='aid')
        for p in range(np):
            sp += 1
            for l in range(nl):
                sl += 1
                for u in range(nu):
                    su += 1  ;  self.dumpLabel(self.acols[i], i+1, sp, sl, sr, sc, sq, su, why=why)  ;  i += 1
                for r in range(nr):
                    sr += 1
                    for c in range(nc):
                        sc += 1  ;  self.dumpLabel(self.acols[i],  i+1, sp, sl, sr, sc, sq, su, why=why)  ;  i += 1
        self.dumpLabel(idt='aid')
        if dbg: self.log('(END) {} {})'.format(self.fmtGeom(), why))

    def dumpLabels(self, why='', dbg=1):
        np, nl, nr, nc = self.n  ;  nc += CCC
        nu = QQ * nc
        i, sp, sl, sr, sc, sq, su = 0, 0, 0, 0, 0, 0, 0
        if dbg: self.log('(BGN) {} {}'.format(self.fmtGeom(), why))
        self.dumpLabel()
        if SPRITES:
            for p in range(np):
                sp += 1
                for l in range(nl):
                    sl += 1
                    for u in range(nu):
                        su += 1  ;  self.dumpLabel(self.labels[i], i+1, sp, sl, sr, sc, sq, su, '{} UCol'.format(why))  ;  i += 1
                    for r in range(nr):
                        sr += 1
                        for c in range(nc):
                            sc += 1  ;  self.dumpLabel(self.labels[i], i+1, sp, sl, sr, sc, sq, su, '{} Col'.format(why))   ;  i += 1
        else:
            for p in range(np):
                sp += 1              ;  self.dumpLabel(self.labels[i], i+1, sp, sl, sr, sc, sq, su, '{} Page'.format(why))  ;  i += 1
                for l in range(nl):
                    sl += 1          ;  self.dumpLabel(self.labels[i], i+1, sp, sl, sr, sc, sq, su, '{} Line'.format(why))  ;  i += 1
                    for u in range(nu):
                        su += 1  ;  self.dumpLabel(self.labels[i], i+1, sp, sl, sr, sc, sq, su, '{} UCol'.format(why))  ;  i += 1
                    for r in range(nr):
                        sr += 1      ;  self.dumpLabel(self.labels[i], i+1, sp, sl, sr, sc, sq, su, '{} Row'.format(why))   ;  i += 1
                        for c in range(nc):
                            sc += 1  ;  self.dumpLabel(self.labels[i], i+1, sp, sl, sr, sc, sq, su, '{} Col'.format(why))   ;  i += 1
        self.dumpLabel()
        if dbg: self.log('(END) {} {})'.format(self.fmtGeom(), why))
    ####################################################################################################################################################################################################
    def dumpSprite(self, s=None, sid=-1, p=-1, l=-1, r=-1, c=-1, q=-1, u=-1, why=''):
        if s is None: self.log('sid  p  l  r   c  q   u    xc      yc       w       h       x       y    iax  iay    m      mx     my     rot   red grn blu opc v       why            group       parent', ind=0); return
        f = '{:4} {} {:2} {:2} {:3} {:2} {:3} {:7.2f} {:7.2f} {:7.2f} {:7.2f} {:7.2f} {:7.2f} {:4} {:4} {:6.3f} {:6.3f} {:6.3f} {:7.2f}  {:3} {:3} {:3} {:3} {:1} {:16} {} {}'
        k, o, v, g, pg = s.color, s.opacity, s.visible, s.group, s.group.parent
        xc, yc = s.x + s.width/2, s.y + s.height/2
        fs = f.format(sid, p, l, r, c, q, u, xc, yc, s.width, s.height, s.x, s.y, s.image.anchor_x, s.image.anchor_y, s.scale, s.scale_x, s.scale_y, s.rotation, k[0], k[1], k[2], o, v, why, g, pg)
        self.log(fs, ind=0)
        assert(type(s) == pyglet.sprite.Sprite)

    def dumpLabel(self, a=None, lid=-1, p=-1, l=-1, r=-1, c=-1, q=-1, u=-1, why='', idt='lid'):
        if a is None: self.log('{:4} p  l  r   c  q   u     x       y       w       h   text   font name     siz dpi bld itl red grn blu opc  why'.format(idt), ind=0) ; return
        x, y, w, h, n, d, s, k, b, i, t = a.x, a.y, a.width, a.height, a.font_name, a.dpi, a.font_size, a.color, a.bold, a.italic, a.text
        f = '{:4} {} {:2} {:2} {:3} {:2} {:3} {:7.2f} {:7.2f} {:7.2f} {:7.2f} {:4} {:16} {:2} {:3}  {:1}   {:1}  {:3} {:3} {:3} {:3}  {}'
        fs = f.format(lid, p, l, r, c, q, u, x, y, w, h, t, n, s, d, b, i, k[0], k[1], k[2], k[3], why)
        self.log(fs, ind=0)
    ####################################################################################################################################################################################################
    def resizeFonts(self):
        ms = self.minSize()  ;  slope, off = 0.6, -1
        fs = fri(ms * slope + off)  ;  formula = '(fs = ms*slope+off)'
        self.log('{} {} ms={:4.1f} slope={} off={} fs={:4.1f}={:2}'.format(self.fmtWH(), formula, ms, slope, off, fs, fri(fs)))
        self.setFontParam('font_size', fs, 'fontSize')

    def minSize(self):
        w = self.cols[0].width  ;  h = self.cols[0].height  ;  m = min(w, h)
        self.log('ww={:5.1f} h={:5.1f} m={:5.1f}'.format(w, h, m))
        return m

    def fontParams(self):    return self.fontBold, self.fontColorIndex, self.fontDpiIndex, self.fontItalic, self.fontNameIndex, self.fontSize
    def fmtf(self):
        fb, fc, fd, fi, fn, fs = self.fontParams()
        text = '{}dpi {}pt {} {}'.format(FONT_DPIS[fd], fs, FONT_NAMES[fn], FONT_COLORS[fc])
        self.log('{}'.format(text))
        return text

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
        if len(self.armSnap): self.snapshot(self.armSnap)  ;  self.armSnap = ''

    def kpEvntTxt(self):
        return '{:8} {:8}     {:14} {:2} {:16}'.format(self.kbk, self.symb, self.symbStr, self.mods, self.modsStr)

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
    def createCursor(self, g):
        cc = self.cursorCol()
        c = self.acols[cc]
        w, h = c.width, c.height  ;  x, y = c.x - w/2, c.y - h/2
        self.log('col[{}]: x={:6.1f} y={:6.1f} w={:6.1f} h={:6.1f} i={}'.format(self.i[C]-1, x, y, w, h, fmtl(self.i, FMTN)))
        self.dumpSprite()
        self.cursor = self.createSprite(None, x, y, w, h, CC, g, why='cursor', v=1, dbg=1)

    def resizeCursor(self):
        cc = self.cursorCol()
        c = self.acols[cc]
        w, h = c.width, c.height  ;  x, y = c.x - w/2, c.y - h/2
        self.log('col[{}]: x={:6.1f} y={:6.1f} w={:6.1f} h={:6.1f} i={}'.format(self.i[C]-1, x, y, w, h, fmtl(self.i, FMTN)))
        self.cursor.update(x=x, y=y, scale_x=w/self.w[C], scale_y=h/self.h[C])

    def cursorCol(self): #calc
        p, l, r, c = self.j()
        cpp, cpl, cpr = self.cps()
        return p*cpp + l*cpl + r*cpr + c
    ####################################################################################################################################################################################################
    def on_mouse_release(self, x, y, button, modifiers):
        np, nl, nr, nc = self.n    ;  nc += CCC
        nr += QQ
        w = self.ww/nc      ;  h = self.hh/(nl * nr)   ;  y0 = y  ;  y = self.hh - y
        c = int(x/w)        ;  r = int(y/h)            ;             kk = c + r * nc
        self.log('(BGN) x={} y0={:4} y={:4} w={:6.2f} h={:6.2f} c={:4} r={:4} txt={}'.format(x, y0, y, w, h, c, r, self.acols[kk].text), file=sys.stdout)
        kk = c + r * nc
        k  = kk - self.cc
        self.log('      {:4} {:4} {:4} {} b={} m={} txt={}'.format(k, kk, self.cc, fmtl(self.i, FMTN), button, modifiers, self.acols[self.cc].text), file=sys.stdout)
        self.move(k)
        self.log('(END) {:4} {:4} {:4} {} b={} m={} txt={}'.format(k, kk, self.cc, fmtl(self.i, FMTN), button, modifiers, self.acols[self.cc].text), file=sys.stdout)

    def move(self, k, dbg=1): #calc
        np, nl, nr, nc = self.n    ;  nc += CCC
        nr += QQ
        if dbg: self.log('(BGN) {:4}      {:4} {} {}'.format(k, self.cc, fmtl(self.i, FMTN), self.acols[self.cc].text), file=sys.stdout)
        if not self.SNAP0: t = self.acols[self.cc]  ;  self.snapshot('pre-move() k={:4} kk={:3} {} txt={} {:6.2f} {:6.2f}'.format(k, self.cc, fmtl(self.i, FMTN), t.text, t.x, t.y))  ;  self.SNAP0 = 1
        self._move(k)
        jp, jl, jr, jc = self.j()
        kk = jc + jr * nc + jl * nr * nc + jp * nl * nr * nc
        t = self.acols[kk]  ;  x = t.x - t.width/2  ;  y = t.y - t.height/2
        self.cc = kk
        self.cursor.update(x=x, y=y)
        if dbg: self.log('(END) {:4} {:4} {:4} {} {} {:6.2f} {:6.2f}'.format(k, kk, self.cc, fmtl(self.i, FMTN), self.acols[self.cc].text, x, y), file=sys.stdout)
        self.armSnap = 'move() k={:4} kk={:4} {} txt={} {:6.2f} {:6.2f}'.format(k, kk, fmtl(self.i, FMTN), self.acols[self.cc].text, x, y)

    def _move(self, k, dbg=1):
        np, nl, nr, nc = self.n
        nr += QQ
        p, l, r, c = self.j()
        nc += CCC
        jc = c + k
        if dbg: self.log('(BGN) {:4}      {:4} {} nc={}'.format(k, self.cc, fmtl(self.i, FMTN), nc), file=sys.stdout)
        self.i[C] = jc %  nc + 1
        jr   =  r + jc // nc
        self.i[R] = jr %  nr + 1
        jl   =  l + jr // nr
        self.i[L] = jl %  nl + 1
        jp   =  p + jl // nl
        ip0  = self.i[P]
        self.i[P] = jp %  np + 1
        if dbg: self.log('(END) {:4}      {:4} {} ip0={} jp={} jl={} jr={} jc={}'.format(k, self.cc, fmtl(self.i, FMTN), ip0, jp, jl, jr, jc), file=sys.stdout)
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
        self.log('(BGN) {} {} {}'.format(self.kpEvntTxt(), fmtl(self.i, FMTN), why), file=sys.stdout)
        self.updateData(kbk)
        self.updateTab( kbk)
#        self.snapshot()
        self.log('(END) {} {} {}'.format(self.kpEvntTxt(), fmtl(self.i, FMTN), why), file=sys.stdout)

    def updateData(self, text, dbg=0):
        p, l, r, c = self.j()
        t = self.data[l][c]
        self.log('(BGN) text={} {} data[l][c]={}'.format(text, fmtl(self.i, FMTN), self.data[l][c]), file=sys.stdout)
        self.data[l][c] = t[0:r] + text + t[r+1:]
        if dbg: self.dumpData(why='updateData text={} i={} data[l][c]={}'.format(text, self.i, self.data[l][c]))
        self.log('(END) text={} {} data[l][c]={}'.format(text, fmtl(self.i, FMTN), self.data[l][c]), file=sys.stdout)

    def updateTab(self, text, dbg=1):
        cc = self.cursorCol()
        self.log('(BGN) text={} cols[{}].text={}'.format(text, cc, self.acols[cc].text), file=sys.stdout)
        self.acols[cc].text = text
        if dbg: self.acols[cc].color = FONT_COLORS[self.fontColorIndex + 4]
        self.log('(END) text={} cols[{}].text={}'.format(text, cc,  self.acols[cc].text), file=sys.stdout)

    def updateCaption(self, txt):
        self.set_caption(txt)
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
    def snapshot(self, why='', dbg=0):
        if dbg: self.log('SFX={} SNAP_DIR={} SNAP_SFX={} BASE_NAME={} BASE_PATH={}'.format(SFX, SNAP_DIR, SNAP_SFX, BASE_NAME, BASE_PATH))
        SNAP_ID   = '.{}'.format(self.ssi)
        SNAP_NAME = BASE_NAME + SFX + SNAP_ID + SNAP_SFX
        SNAP_PATH = BASE_PATH / SNAP_DIR / SNAP_NAME
        pyglet.image.get_buffer_manager().get_color_buffer().save('{}'.format(SNAP_PATH))
        if dbg: self.log('SNAP_ID={} SNAP_NAME={} SNAP_PATH={}'.format(SNAP_ID, SNAP_NAME, SNAP_PATH))
        self.log('{} {}'.format(SNAP_NAME, why), file=sys.stdout)
        self.ssi += 1

    def dumpStack(self, si):
        for i, e in enumerate(si):
            fp = pathlib.Path(e.filename)  ;            n = fp.stem  ;            l = e.lineno  ;            f = e.function  ;            c = e.code_context[0].strip()  ;            j = len(si) - (i + 1)
            self.log('{:2} {:9} {:5} {:20} {}'.format(j, n, l, f, c))
        self.log('MAX_STACK_DEPTH={:2}'.format(MAX_STACK_DEPTH))

    @staticmethod
    def indent(): d = Tabs.stackDepth() - 4;  return '{:{w}}'.format(d, w=d)

    @staticmethod
    def stackDepth():
        global MAX_STACK_DEPTH, MAX_STACK_FRAME
        si = inspect.stack()
        for i, e in enumerate(si):
            j = len(si) - (i + 1)
            if j > MAX_STACK_DEPTH: MAX_STACK_DEPTH = j;  MAX_STACK_FRAME = si
        return len(si)

    @staticmethod
    def delGlob(g, why=''):
        print('deleting {} file globs why={}'.format(len(g), why))
        for f in g:
            Tabs.log('{}'.format(f))
            os.system('del {}'.format(f))
    @staticmethod
    def getLogPath(seq=0, logdir='logs', logsfx='.log'):
        if seq:
            subDir     = '/' + SFX.lstrip('.')
            logdir     = logdir + subDir
            Tabs.log('logdir      = {}'.format(logdir))
            pathlib.Path(logdir).mkdir(parents=True, exist_ok=True)
            logGlobArg = str(BASE_PATH / logdir / BASE_NAME) + SFX + '.*' + logsfx
            logGlob    = glob.glob(logGlobArg)
            seq        = 1 + Tabs.getLogId(logGlob, logsfx)
            logsfx     = '.{}{}'.format(seq, logsfx)
            Tabs.log('logGlobArg  = {}'.format(logGlobArg))
            Tabs.log('logGlob:')
            Tabs.log('{}'.format(fmtl(logGlob)), ind=0)
            Tabs.log('seq num     = {}'.format(seq))
        logName        = BASE_NAME + SFX + logsfx
        logPath        = BASE_PATH / logdir / logName
        Tabs.log('logPath     = {}'.format(logPath)) if seq else print('logPath     = {}'.format(logPath))
        return logPath

    @staticmethod
    def getLogId(s, sfx, dbg=0):
        i = -1
        if len(s):
            ids = []
            for ss in s:
                if ss.endswith(sfx):
                    ss = ss[:-len(sfx)]
                    j = ss.rfind('.')
                    ss = ss[j+1:]
                    i = int(ss)
                    ids.append(i)
            if dbg: tabs.log('ids={}'.format(ids))
            i = max(ids)
        return i

    @staticmethod
    def log(msg='', ind=1, file=None, flush=False, sep=',', end='\n'):
        if not file: file = LOG_FILE
        si = inspect.stack(0)[1]
        p = pathlib.Path(si.filename)  ;        n = p.name  ;        l = si.lineno  ;        f = si.function  ;        t = ''
        if f == 'log': si = inspect.stack(0)[2];  p = pathlib.Path(si.filename);  n = p.name;  l = si.lineno;  f = si.function;  t = ''
        if ind: print('{:20} {:5} {:7} {} {:>20} '.format(Tabs.indent(), l, n, t, f), file=file, end='')
        print('{}'.format(msg), file=file, flush=flush, sep=sep, end=end) if ind else print('{}'.format(msg), file=file, flush=flush, sep=sep, end=end)
        if file != LOG_FILE: Tabs.log(msg, ind)
    ####################################################################################################################################################################################################
    def quit(self, why=''):
        self.log('(BGN)')
        self.log(QUIT, ind=0)
        self.dumpStruct('quit ' + why)
#        self.snapshot()
        self.log(QUIT, ind=0)
        self.dumpStack(inspect.stack())
        self.log(QUIT, ind=0)
        self.dumpStack(MAX_STACK_FRAME)
        self.log('SEQ_LOG_FILES = {}'.format(SEQ_LOG_FILES))
        logPath = None
        if SEQ_LOG_FILES:
            logPath = self.getLogPath(SEQ_LOG_FILES)
            self.log('LOG_PATH    = {}'.format(LOG_PATH))
            self.log('logPath     = {}'.format(logPath))
            self.log('copy {} {}'.format(LOG_PATH, logPath))
        self.log('(END) closing LOG_FILE={}'.format(LOG_FILE.name))
        LOG_FILE.close()
        if SEQ_LOG_FILES and logPath: os.system('copy {} {}'.format(LOG_PATH, logPath))
        exit()
    ####################################################################################################################################################################################################
    @staticmethod
    def deleteList(l): # Not Used?
        j = 0
        while j < len(l): t = l[j];  t.delete();  del l[j]
########################################################################################################################################################################################################
if __name__ == '__main__':
    LOG_PATH = Tabs.getLogPath()
    with open(str(LOG_PATH), 'w') as LOG_FILE:
        Tabs.log('BGN Logging LOG_PATH={}'.format(LOG_PATH))
        Tabs.log('creating Tabs instance'.format())
        tabs     = Tabs()
        tabs.log('tabs={}'.format(tabs))
        tabs.log('invoking pyglet.app.run()'.format())
        ret = pyglet.app.run()
        tabs.log('pyglet.app.run() return={}'.format(ret))
        tabs.log('END Logging LOG_PATH={}'.format(LOG_PATH))
