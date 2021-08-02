import inspect, math, sys, os, glob, pathlib, string, collections #, itertools #, shutil#, unicodedata, readline, csv
import pyglet
import pyglet.window.key   as pygwink
import pyglet.window.event as pygwine
sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, os.path.abspath('../lib'))
import misc
import cmdArgs

class MyFormatter(string.Formatter):
    def __init__(self, missing='?????', badfmt='!!!!!'):
        self.missing, self.badfmt = missing, badfmt
    def get_field(self, field_name, args, kwargs): # Handle a key not found
        try:
            val = super().get_field(field_name, args, kwargs)
        except (KeyError, AttributeError):
            val = None,field_name
        return val
    def format_field(self, value, spec):           # handle an invalid format
        if value is None : return self.missing
        try:
            return super().format_field(value, spec)
        except ValueError:
            if self.badfmt is not None: return self.badfmt
            else: raise
FMTR = MyFormatter()
####################################################################################################################################################################################################
CHECKER_BOARD = 0  ;  EVENT_LOG = 1  ;  FULL_SCREEN = 1  ;  ORDER_GROUP = 1  ;  READ_DATA_FILE = 0  ;  RESIZE = 1  ;  SEQ_LOG_FILES = 1  ;  SUBPIX = 1
VRSN1            = 0  ;  SFX1 = chr(65 + VRSN1)  ;  QQ      = VRSN1  ;  VRSNX1 = 'VRSN1={}       QQ={}  SFX1={}'.format(VRSN1, QQ,      SFX1)
VRSN2            = 0  ;  SFX2 = chr(49 + VRSN2)  ;  SPRITES = VRSN2  ;  VRSNX2 = 'VRSN2={}  SPRITES={}  SFX2={}'.format(VRSN2, SPRITES, SFX2)
VRSN3            = 0  ;  SFX3 = chr(97 + VRSN3)  ;  CCC     = VRSN3  ;  VRSNX3 = 'VRSN3={}      CCC={}  SFX3={}'.format(VRSN3, CCC,     SFX3)
SFX              = f'.{SFX1}.{SFX2}.{SFX3}'
PATH             = pathlib.Path(sys.argv[0])
BASE_PATH        = PATH.parent
BASE_NAME        = BASE_PATH.stem
SNAP_DIR         = 'snaps'
SNAP_SFX         = '.png'
FMTN             = (1, 1, 1, 2, 1, 2, 2) # remove?
P, L, S, C       =  0,  1,  2,  3
T, N, I, K       =  4,  5,  6,  7
O, A, D, E, F    =  8,  9, 10, 11, 12
LLR, LLC         = 13, 14
TT, NN, II, KK   =  0,  1,  2,  3
Z, COLL, LINL    = ' ', 'Col', 'Line '
C1,  C2,  RLC    = 0, 1, 2
INIT             = '###   Init   ###' * 13
QUIT             = '###   Quit   ###' * 13
#CURSOR_MODES     = ['MELODY', 'CHORD', 'ARPEGGIO']
DIRECTIONS       = {'UP':-1, 'DOWN':1}
OPACITY          = [255, 240, 225, 210, 190, 165, 140, 110, 80]
GRAY             = [(255, 255, 255, OPACITY[0]), ( 0,  0,  0, OPACITY[0])]
PINK             = [(255,  64, 192, OPACITY[0]), (57, 16, 16, OPACITY[0])]
INFRA_RED        = [(200, 100,  24, OPACITY[0]), (68, 20, 19, OPACITY[0])]
RED              = [(255,  12,  11, OPACITY[0]), (88, 15, 12, OPACITY[0])]
ORANGE           = [(255, 128,   0, OPACITY[0]), (76, 30, 25, OPACITY[0])]
YELLOW           = [(255, 255,  10, OPACITY[0]), (45, 41, 10, OPACITY[0])]
GREEN            = [( 12, 255,  11, OPACITY[0]), (21, 54, 10, OPACITY[0])]
GREEN_BLUE       = [( 24, 255,  98, OPACITY[0]), (10, 49, 25, OPACITY[0])]
CYAN             = [( 13, 255, 255, OPACITY[0]), (16, 64, 64, OPACITY[0])]
BLUE_GREEN       = [( 15, 122, 255, OPACITY[0]), (12, 37, 51, OPACITY[0])]
BLUE             = [( 13,  11, 255, OPACITY[0]), (19, 11, 64, OPACITY[0])]
INDIGO           = [(255,  22, 255, OPACITY[0]), (19, 11, 64, OPACITY[0])]
VIOLET           = [(176,  81, 255, OPACITY[0]), (44, 14, 58, OPACITY[0])]
ULTRA_VIOLET     = [(194,  96, 255, OPACITY[3]), (50, 19, 61, OPACITY[1])]
HUES             = 16
MAX_STACK_DEPTH  = 0  ;  MAX_STACK_FRAME = inspect.stack()
####################################################################################################################################################################################################
def fmtl(a, w=None, u='<', d1='[', d2=']'):
    t = ''
    for i in range(len(a)):
#        if w is None:                  t += '{} '.format(a[i])
#        elif type(w) is int:           t += '{:{}{}} '.format(a[i], u, w)
#        elif type(w) is list or tuple: t += '{:{}{}} '.format(int(a[i]), u, w[i])
        if w is None:                  t += f'{a[i]} '
        elif type(w) is int:           t += f'{a[i]:{u}{w}} '
        elif type(w) is list or tuple: t += f'{int(a[i]):{u}{w[i]}} '
    return d1 + t[:-1] + d2
def fmtd(a, w=2, d0=':', d1='[', d2=']'):
    t = ''
    for k, v in a.items():
        t += '{:>{}}{}{:<{}} '.format(k, w, d0, v, w)
    return d1 + t.rstrip() + d2
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
FONT_DPIS     = [72, 78, 84, 90, 96, 102, 108, 114, 120]
FONT_NAMES    = ['Times New Roman', 'Lucida Console', 'Courier New', 'Helvetica', 'Arial', 'Century Gothic', 'Bookman Old Style', 'Antique Olive']
FONT_COLORS_S = [PINKS[0], CYANS[0], REDS[0], BLUES[0], YELLOWS[0], GREENS[0], ORANGES[0], VIOLETS[0], REDS[13], YELLOWS[15], GREEN_BLUES[8], ORANGES[12], INDIGOS[8], ULTRA_VIOLETS[9], BLUE_GREENS[8], CC]
FONT_COLORS_L = [PINKS[0], GRAYS[0], BLUES[0], GREENS[0], YELLOWS[0], REDS[0], GRAYS[1], PINKS[8], REDS[10], YELLOWS[15], GRAYS[8], GRAYS[8], INDIGOS[8], GRAYS[9], GRAYS[8], CC]
FONT_COLORS   =  FONT_COLORS_S if SPRITES else FONT_COLORS_L
####################################################################################################################################################################################################
class Tabs(pyglet.window.Window):
    def __init__(self):
        global FULL_SCREEN, SUBPIX, ORDER_GROUP
        snapGlobArg = str(BASE_PATH / SNAP_DIR / BASE_NAME) + SFX + '.*' + SNAP_SFX
        snapGlob    = glob.glob(snapGlobArg)
        self.log('(BGN) {}'.format(__class__))
        self.log('{}'.format(VRSNX1))
        self.log('{}'.format(VRSNX2))
        self.log('{}'.format(VRSNX3))
        self.dumpGlobalFlags()
        self.log('snapGlobArg={}'.format(snapGlobArg))
        self.log('   snapGlob={}'.format(snapGlob))
        self.delGlob(snapGlob, 'SNAP_GLOB')
        self.cobj = misc.Chord(self, LOG_FILE)
        self.n = []
        self.TNIK = [1, 0, 0, 1]
        nt     = 6 if QQ else 6
        self.log(f'TNIK={(fmtl(self.TNIK))}')
        self.ww, self.hh  = 640, 480
        self.n, self.i, self.x, self.y, self.w, self.h, self.g = [1, 3, self.ssc(), 10, nt], [1, 1, 1, 1, 3], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], []
        self.argMap = cmdArgs.parseCmdLine(dbg=1)
#        if 'N' in self.argMap and len(self.argMap['N']) == 0: self.N            = 1
        if 'n' in self.argMap and len(self.argMap['n'])  > 0: self.n            = [int(self.argMap['n'][i]) for i in range(len(self.argMap['n']))]
        if 'i' in self.argMap and len(self.argMap['i'])  > 0: self.i            = [int(self.argMap['i'][i]) for i in range(len(self.argMap['i']))]
        if 'x' in self.argMap and len(self.argMap['x'])  > 0: self.x            = [int(self.argMap['x'][i]) for i in range(len(self.argMap['x']))]
        if 'y' in self.argMap and len(self.argMap['y'])  > 0: self.y            = [int(self.argMap['y'][i]) for i in range(len(self.argMap['y']))]
        if 'w' in self.argMap and len(self.argMap['w'])  > 0: self.ww           =  int(self.argMap['w'][0])
        if 'h' in self.argMap and len(self.argMap['h'])  > 0: self.hh           =  int(self.argMap['h'][0])
        if 'f' in self.argMap and len(self.argMap['f']) == 0: FULL_SCREEN       = 1
        if 'g' in self.argMap and len(self.argMap['g']) == 0: ORDER_GROUP       = 1
        if 's' in self.argMap and len(self.argMap['s']) == 0: SUBPIX            = 1
#        self.log('[N]            N={}'.format(self.N))
        self.log('[n]            n={}'.format(fmtl(self.n, FMTN)))
        self.log('[i]            i={}'.format(fmtl(self.i, FMTN)))
        self.log('[x]            x={}'.format(fmtl(self.x, FMTN)))
        self.log('[y]            y={}'.format(fmtl(self.y, FMTN)))
        self.log('[w]           ww={}'.format(self.ww))
        self.log('[h]           hh={}'.format(self.hh))
        self.log('[f]  FULL_SCREEN={}'.format(FULL_SCREEN))
        self.log('[g]  ORDER_GROUP={}'.format(ORDER_GROUP))
        self.log('[s]       SUBPIX={}'.format(SUBPIX))
        self.fontBold, self.fontItalic, self.fontColorIndex, self.fontDpiIndex, self.fontNameIndex, self.fontSize = 0, 0, 0, 4, 0, 24 if FULL_SCREEN else 14
        self.dumpFont()
        if    self.n[T] == 6: self.stringMap = collections.OrderedDict([('E2', 28), ('A2', 33), ('D3', 38), ('G3', 43), ('B3', 47), ('E4', 52)])
        elif  self.n[T] == 7: self.stringMap = collections.OrderedDict([('E2', 28), ('A2', 33), ('D3', 38), ('G3', 43), ('B3', 47), ('E4', 52), ('A4', 57)])
        else:                 self.stringMap = collections.OrderedDict([('E2', 28), ('A2', 33), ('D3', 38), ('G3', 43), ('B3', 47), ('E4', 52)])
        self.stringKeys  = list(self.stringMap.keys())
        self.stringNames = ''.join(reversed([str(k[0]) for k in self.stringKeys]))
        self.stringNumbs = ''.join([str(r+1)  for r in range(self.n[T])])
        self.stringCapo  = ''.join(['0' for _ in range(self.n[T])])
        self.log('stringMap   = {}'.     format(fmtd(self.stringMap)))
        self.log('stringKeys  = {} = {}'.format(fmtl(self.stringKeys),  self.stringKeys))
        self.log('stringNames = {} = {}'.format(fmtl(self.stringNames), self.stringNames))
        self.log('stringNumbs = {} = {}'.format(fmtl(self.stringNumbs), self.stringNumbs))
        self.log('stringCapo  = {} = {}'.format(fmtl(self.stringCapo),  self.stringCapo))
        self.strLabel = 'STRING'
        self.cpoLabel   = ' CAPO '
        self.log('strLabel = {} = {}'.format(fmtl(self.strLabel), self.strLabel))
        self.log('cpoLabel   = {} = {}'.format(fmtl(self.cpoLabel),   self.cpoLabel))
        self.cursorModes = {'MELODY': 0, 'CHORD': 1, 'ARPEGGIO': 2}
        self.cursorMode  = self.cursorModes['MELODY']
#        self.directions = {'UP': 1, 'DOWN': -1}
        self.direction   = DIRECTIONS['DOWN']
        self._initWindowA()
        super().__init__(screen=self.screens[1], fullscreen=FULL_SCREEN, resizable=True, visible=False)
        self._initWindowB()
        self.pages,   self.lines,   self.sects,     self.cols          = [], [], [], []      ;  self.A = [self.pages,   self.lines,   self.sects,     self.cols]
        self.tabs,    self.notes,   self.intervals, self.chords        = [], [], [], []      ;  self.B = [self.tabs,    self.notes,   self.intervals, self.chords]
        self.snos,    self.snas,    self.capos, self.strls, self.cpols = [], [], [], [], []  ;  self.C = [self.snos,    self.snas,    self.capos,     self.strls, self.cpols]
        self.llRows,  self.llCols,  self.labels,    self.sprites       = [], [], [], []      ;  self.D = [self.llRows,  self.llCols,  self.sprites,   self.labels]
        self.E = [*self.A, *self.B, *self.C, *self.D]
        self.log(f'E={self.E}')
        self.DF = [0, 0, 0, 0,  0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0, 0]
        self.J1, self.J2 = self.initJ()
        self.data    = []
        self.kbk, self.symb, self.mods, self.symbStr, self.modsStr = 0, 0, 0, '', ''
        self.cc, self.ci, self.SNAP0, self.armSnap  = 0, 0, 0, ''
        self.tblanki, self.tblanks  = 1, [' ', '-']   ;   self.tblank = self.tblanks[self.tblanki]
        self.nblanki, self.nblanks  = 1, [' ', '-']   ;   self.nblank = self.nblanks[self.nblanki]
        self.tblankCol = self.tblank * self.n[T]      ;  self.tblankRow = self.nblank * (self.n[C] + CCC)
        self.cursor, self.caret   = None, None
        self._init()
        self.log('(END) {} {} {}'.format(__class__, VRSNX1, VRSNX2))
        self.log('{}'.format(INIT), ind=0)

    def dumpGlobalFlags(self):
        text = 'CHECKER_BOARD={} EVENT_LOG={} FULL_SCREEN={} ORDER_GROUP={} READ_DATA_FILE={} RESIZE={} SEQ_LOG_FILES={} SUBPIX={}'
        self.log(text.format(CHECKER_BOARD, EVENT_LOG, FULL_SCREEN, ORDER_GROUP, READ_DATA_FILE, RESIZE, SEQ_LOG_FILES, SUBPIX), ind=0, end='')
        self.log(' CCC={}'.format(CCC), ind=0)

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

    def _initTpz(self, dbg=1):
        np, nl, ns, nc, nt = self.n
        self.tpc =  nt #+ CCC
        self.tps =  nc * self.tpc
        self.tpl =       self.tps
        self.tpp =  nl * self.tpl
        if dbg: self.log('tps={}'.format(fmtl(self.tpz())))

    def dumpObj( self, obj, name, why=''): self.log(f'{why} Obj {name} {hex(id(obj))}')
    def dumpObjs(self, obj, name, why=''): self.log(f'{why} Obj {name} ')   ;    [self.log(f'{hex(id(o))} type={type(o)}', ind=0) for o in obj]   ;    self.log(ind=0)
    def ss(self):    s = sum(self.TNIK)  ;                      self.log(FMTR.format(f's={s}      TNIK={   fmtl(self.TNIK)} n={fmtl(self.n)}'))  ;  return s
    def ssc(self):   s = self.ss()  ;  sc = s if s else 1   ;   self.log(FMTR.format(f's={s} sc={sc} TNIK={fmtl(self.TNIK)} n={fmtl(self.n)}'))  ;  return sc
    def tpz(self):   return self.tpp, self.tpl, self.tps, self.tpc
    def lens(self):  return self.lenA(), self.lenB(), self.lenC(), self.lenD()
    def lenA(self):  return [len(e) for e in self.A]
    def lenB(self):  return [len(e) for e in self.B]
    def lenC(self):  return [len(e) for e in self.C]
    def lenD(self):  return [len(e) for e in self.D]
    def lenE(self):  return [len(e) for e in self.E]
    def initJ(self): self.J1 = [0 for _ in self.E]  ;  self.J2 = [0 for _ in self.E]  ;  self.dumpJ('initJ()')  ;  return self.J1, self.J2
    def dumpJ(self, why): self.log(f'J1({len(self.J1)}))={self.J1} {why}')  ;  self.log(f'J2({len(self.J2)}))={self.J2} {why}')
    def updateJs(self, i, v): self.J1[i] = v    ;    self.J2[i] += 1
    def j(self):     return [i-1 if i else 0 for i in self.i]
    def dl(self, data=None):
        if data is None: data = self.data
        return len(data), len(data[0]), len(data[0][0]), len(data[0][0][0])

    def fmtDataDim(self, data=None): return '({} x {} x {} x {})'.format(*self.dl(data))
    def fmtGeom(self): return '{} {} {} {} {} {} {} {} {} {} {}'.format(self.cc, fmtl(self.i, FMTN), fmtl(self.n, FMTN), fmtl(self.lenA()), sum(self.lenA()), fmtl(self.lenB()), sum(self.lenB()), fmtl(self.lenC()), sum(self.lenC()), fmtl(self.lenD()), sum(self.lenD()))
    def ordDict(self, od): self.log('{}'.format(od.items()))

    def ids(self):
        if SPRITES: return sum(self.J2[:4]), sum(self.J2[4:8])
        else:       return 0,                sum(self.J2[:4]) + sum(self.J2[4:8])
    def cnts(self): return self.J2[:8]  # self.log(f'J2({len(self.J2)}))={self.J2}')
    ####################################################################################################################################################################################################
    def _init(self, dbg=1):
        dataDir  = 'data'  ;  dataSfx = '.dat'  ;  dataPfx = '.{}'.format(self.n[C])
        dataName = BASE_NAME + SFX + dataPfx + dataSfx
        self.dataPath = BASE_PATH / dataDir / dataName
        self.log(f'(BGN) {self.fmtGeom()}', ind=0)
        self.kp  = [VIOLETS[0], VIOLETS[12]] if CHECKER_BOARD else [VIOLETS[10]]
        self.kl  = [  BLUES[12],  BLUES[15]] if CHECKER_BOARD else [BLUES[12]]
        self.ks  = [   CYANS[12],   CYANS[15]] if CHECKER_BOARD else [CYANS[12]]
        self.kc  = [GRAYS[0],    GRAYS[8]] if CHECKER_BOARD else [GRAYS[0]]
        self.kt  = [ORANGES[0], ORANGES[8]]  if CHECKER_BOARD else [ORANGES[0]]
        self.kn  = [GREENS[0], GREENS[12]]  if CHECKER_BOARD else [GREENS[0]]
        self.ki  = [  CYANS[0],   CYANS[8]]  if CHECKER_BOARD else [CYANS[0]]
        self.kk  = [  CYANS[0],   CYANS[8]]  if CHECKER_BOARD else [CYANS[0]]
        self.kt2 = [YELLOWS[0], YELLOWS[8]]  if CHECKER_BOARD else [YELLOWS[0]]
        self.kn2 = [GREEN_BLUES[0], GREEN_BLUES[8]]  if CHECKER_BOARD else [GREEN_BLUES[4]]
        self.ki2 = [  CYANS[0],   CYANS[8]]  if CHECKER_BOARD else [CYANS[0]]
        self.kk2 = [  BLUES[0],   BLUES[8]]  if CHECKER_BOARD else [BLUES[0]]
        self.klr = [ORANGES[0], ORANGES[8]]  if CHECKER_BOARD else [ORANGES[0]]
        self.klc = [ PINKS[0],  PINKS[8]]  if CHECKER_BOARD else [PINKS[0]]
        self.kll = [ REDS[0],  REDS[8]]  if CHECKER_BOARD else [REDS[0]]
        self.k   = [self.kp, self.kl, self.ks, self.kc, self.kt, self.kn, self.ki, self.kk, self.klc, self.klr, self.kll]
        [self.log(f'{fmtl(*e)}') for e in self.k]
        self.ssi = 0
        self._initTpz()
        self.readDataFile() if READ_DATA_FILE else self.createBlankData()
        self.labelTextA, self.labelTextB = [], []
        self.createLabelText()
        self.labelTextC = []  ;  self.labelTextC.append('M')       ;  self.labelTextC.extend(self.labelTextB)
        self.labelTextD = []  ;  self.labelTextD.extend(['R', 'M'])  ;  self.labelTextD.extend(self.labelTextB)
        self.llText = []
        self.llText.append(self.labelTextB)
        self.llText.append(self.labelTextC)
        self.llText.append(self.labelTextD)
        self.log(f'textC={self.labelTextC}')
        self.log(f'textD={self.labelTextD}')
        self.dumpJ('(BGN) createSprites() / createLabels()')
        self.ssc()
        self.createSprites() if SPRITES else  self.createLabels()
        self.dumpJ('(END) createSprites() / createLabels()')
        self.createCursor(self.g[T + 3]) # fix
        if dbg: self.dumpStruct('_init')
        self.log(f'(END) {self.fmtGeom()}', ind=0)
    ####################################################################################################################################################################################################
    def on_draw(self, dbg=0):
        self.clear()
        self.batch.draw()
        if self.armSnap:
            if dbg: self.log(f'armSnap={self.armSnap}')
            self.snapshot(self.armSnap)  ;  self.armSnap = ''

    def on_resize(self, width, height):
        super().on_resize(width, height)
        self.ww, self.hh = width, height
        if not RESIZE: return
        self.log('(BGN) {} {}'.format(self.fmtWH(), self.fmtDataDim(self.data)))
        self.log(f'TNIK={(fmtl(self.TNIK))}')
        self.dumpJ('(BGN) on_resize()')
        self.J1, self.J2 = self.initJ()
        self.resizeSprites() if SPRITES else self.resizeLabels()
        self.dumpJ('(END) on_resize()')
        self.dumpStruct2('on_resize()')
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
#        if SPRITES: self.dumpSprites()
#        self.dumpLabels(why)
#        self.dumpTabs(why)
        self.dumpStruct2()
        self.log('(END) {}'.format(why))

    def dumpStruct2(self, why=''):
        self.log('(BGN) {}'.format(why))
        self.dumpFont(why)
        self.dumpGlobalFlags()
        self.log(f'{self.fmtGeom()}', ind=0)
        self.log('{} {}'.format(self.fmtWH(), self.fmtDataDim(self.data)))
        self.log('(END) {}'.format(why))
    ####################################################################################################################################################################################################
    def writeDataFile(self):
        self.log('(BGN) {}'.format(self.fmtDataDim(self.data)))
        data = self.transposeData(self.data) if self.isVert() else self.data
        with open(str(self.dataPath), 'w') as DATA_FILE:
            np, nl, nc, nr = self.dl()  ;  nc += CCC
            for p in range(np):
                self.log('writing {}{} page'.format(p+1, self.ordSfx(p+1)))
                for l in range(nl):
                    self.log('writing {}{} line'.format(l+1, self.ordSfx(l+1)))
                    for r in range(nr):
                        text = ''
                        for c in range(nc):
                            text += data[p][l][r][c]
                        self.log('writing {}{} string {}'.format(r+1, self.ordSfx(r+1), text))
                        text += '\n'
                        DATA_FILE.write(text)
                    if l+1 < nl: DATA_FILE.write('\n')
        self.log('(END) {}'.format(self.fmtDataDim(self.data)))
    ####################################################################################################################################################################################################
    def createBlankData(self):
        self.log('Creating tab data using parameters {} {} {} {} {}'.format(*self.n))
        np, nl, ns, nc, nr = self.n  ;  nc += CCC
        self.data = [[[self.tblankRow for _ in range(nr)] for _ in range(nl)] for _ in range(np)]
        self.dumpDataVert() if self.isVert() else self.dumpDataHorz()
        self.data = self.transposeData()
        self.dumpDataVert() if self.isVert() else self.dumpDataHorz()

    def readDataFile(self, dbg=1):
        np, nl, ns, nr, nc = self.n
        if dbg: self.log('nl={} nr={} nc={}'.format(nl, nr, nc))
        with open(str(self.dataPath), 'r') as DATA_FILE:
            DATA_FILE.seek(0, 2)  ;  size = DATA_FILE.tell()  ;  DATA_FILE.seek(0, 0)
            self.log('(BGN) {:40} {:8,} bytes = {:4,.0f} KB'.format(DATA_FILE.name, size, size/1024))
            strings = []  ;  lines = []
            l, r, c = 1, 0, 0
            while l <= nl:
                s = DATA_FILE.readline().strip('\n')
                if len(s): strings.append(s)  ;  r += 1  ;  c = len(s)
                else:
                    lines.append(strings)
                    strings=[]
                    self.log('read    {:2}{} Line with {:6,} Cols on {:4,} Strings {:8,} Tabs'.format(l, self.ordSfx(l), c, r, c*r))
                    if l == nl: break
                    r = 0
                    l += 1
                if c:  self.log('l={} r={} c={}: {}'.format(l, r, c, s))
            self.data.append(lines)
        nt   = l * c * r
        self.tblankCol = self.tblank * r
        vert = self.isVert()
        self.log('read     {:2} Lines with {:6,} Cols on {:4,} Strings {:8,} Tabs, vdf={} blankCol({})={}'.format(l, l*c, l*r, nt, vert, len(self.tblankCol), self.tblankCol))
        if dbg: self.dumpDataHorz()
        self.data = self.transposeData()
        vert      = self.isVert()
        if dbg: self.dumpDataVert()
        self.log('assert: size=nt+2*(l*r+l-1) {:8,} + {} = {:8,} bytes assert isVert={}'.format(nt, 2 * (l * r + l - 1), size, vert))
#        assert size == nt + 2 * (l * r + l - 1)  ;  assert vert
        self.log('(END) {:40} {:8,} bytes = {:4,.0f} KB'.format(DATA_FILE.name, size, size/1024))

    def isVert(self, data=None, dbg=1):
        if data is None: data = self.data
        vert = 1
        if dbg: self.log('(BGN) type(data [0] [0][0] [0][0][0])={} {} {} {}'.format(type(data), type(data[0]), type(data[0][0]), type(data[0][0][0])))
        assert type(data) is list and type(data[0]) is list and type(data[0][0]) is list and type(data[0][0][0]) is str
        for p in range(len(data)):
            assert len(data[p]) == len(data[0])
            for l in range(len(data[p])):
                assert len(data[p][l]) == len(data[p][0])
                for c in range(len(data[p][l])):
                    assert len(data[p][l][c]) == len(data[p][l][0])
                if len(data[p][l]) < len(data[p][l][0]): vert = 0  ;  break
        if dbg: self.log('(END)  len(data [0] [0][0] [0][0][0])={} {} {} {} return vdf={}'.format(len(data), len(data[0]), len(data[0][0]), len(data[0][0][0]), vert))
        return vert
    ####################################################################################################################################################################################################
#   def dumpTabData(self, data=None, why='', lc=1, ll=1, i=0):
#        if data is None: data = self.data
#        self.log('(BGN) {}'.format(why))
#        self.dumpDataVert(data, lc, ll, i) if self.isVert(data) else self.dumpDataHorz(data, lc, ll, i)
#        transposeData = self.transposeData(data, why='Internal')
#        self.dumpDataVert(transposeData, lc, ll, i) if self.isVer(transposeData) else self.dumpDataHorz(transposeData, lc, ll, i)
#        self.log('(END) {}'.format(why))

    def dumpDataHorz(self, data=None, lc=1, ll=1, i=0):
        if data is None: data = self.data
        self.log('(BGN) lc={} ll={} i={} {}'.format(lc, ll, i, self.fmtDataDim(data)))
        for p in range(len(data)):
            for l in range(len(data[p])):
                if ll:  llt = 'Line {}'.format(l + 1)  ;  llab = '{:{}}'.format(llt, i + 1)  ;  self.log('{}{}'.format(Z * i, llab), ind=0)
                if lc:  self.dumDataLabels(data[p][l], i=i, sep=Z)
                for r in range(len(data[p][l])):
                    self.log('{}'.format(Z * i), ind=0, end='')
                    for c in range(len(data[p][l][r])):
                        self.log('{}'.format(data[p][l][r][c]), ind=0, end='')
                    self.log(ind=0)
                self.log(ind=0)
        self.log('(END) lc={} ll={} i={} {}'.format(lc, ll, i, self.fmtDataDim(data)))

    def dumpDataVert(self, data=None, lc=1, ll=1, i=0):
        if data is None: data = self.data
        self.log('(BGN) lc={} ll={} i={} {}'.format(lc, ll, i, self.fmtDataDim(data)))
        if ll:
            t0 = Z * i + COLL + Z       if        i >= 0 else COLL
            self.log(t0, ind=0, end='') if lc and i >= 0 else self.log(Z * i, ind=0, end='')
            w = max(len(data[0][0][0]), len(LINL) + 1)
            for p in range(len(data)):
                for l in range(len(data[0])):
                    t = '{}{}'.format(LINL, l + 1)
                    self.log('{:{}}'.format(t, w), ind=0, end=Z)
                self.log(ind=0)#            self.log(t0, ind=0)         if lc and i < 0 else self.log(ind=0)
        for p in range(len(data)):
            for c in range(len(data[p][0])):
                self.log('{}{:3} '.format(Z * i, c + 1), ind=0, end='') if i >= 0 and lc else self.log('{}'.format(Z * i), ind=0, end='')
                for l in range(len(data[p])):
                    self.log('{}'.format(data[p][l][c]), ind=0, end=Z)
                self.log(ind=0)##            self.log('{:3} '.format(cc + 1),        ind=0)           if i <  0 and c else self.log(ind=0)
        self.log('(END) lc={} ll={} i={} {}'.format(lc, ll, i, self.fmtDataDim(data)))
    ####################################################################################################################################################################################################
    def dumDataLabels(self, data=None, i=0, sep='%'):
        pp = '  '  ;  qq = ' @'
        p = pp[:] if CCC > 1 else pp[:1] if CCC else ''
        q = qq[:] if CCC > 1 else qq[:1] if CCC else ''
        if data is None: data = self.data
        n = len(data[0])-CCC    ;  a = ' ' * i if i else ''   ;  b = sep * n  ;  r = sep * 3
        if n >= 100:      self.log('{}{}'.format(a, p), ind=0, end='')  ;  [  self.log('{}'.format(c//100   if c>=100 else ' '), ind=0, end='') for c in range(1, n+1) ]  ;  self.log(ind=0)
        if n >= 10:       self.log('{}{}'.format(a, p), ind=0, end='')  ;  [  self.log('{}'.format(c//10%10 if c>=10  else ' '), ind=0, end='') for c in range(1, n+1) ]  ;  self.log(ind=0)
        self.log(                  '{}{}'.format(a, q), ind=0, end='')  ;  [  self.log('{}'.format(c%10),                        ind=0, end='') for c in range(1, n+1) ]  ;  self.log(ind=0)
        if sep != '':   self.log('{}{}{}'.format(a, r, b), ind=0)

    def transposeData(self, data=None, why=' External  ', dbg=1):
        if data is None: data = self.data
        if dbg: self.log('(BGN) {} {}'.format(why, self.fmtDataDim(data)))
        transposed = []
        for p in range(len(data)):
            lines = []
            for l in range(len(data[p])):
                swapped = []
                for c in range(len(data[p][l][0])):
                    a = []  ;  s = ''  ;  tt = None
                    for r in range(len(data[p][l])):
                        tt = type(data[p][l][r])
                        if   tt is str:  s += data[p][l][r][c]
                        elif tt is list: a.append(data[p][l][r][c])
                    swapped.append(s) if tt is str else transposed.append(a)
                lines.append(swapped)
            transposed.append(lines)
        if dbg: self.log('(END) {} {}'.format(why, self.fmtDataDim(transposed)))
        return transposed

    def dumpLabelText(self, t, d='%', why='', dbg=1):
        self.log('{} len(t)={} len(t[0])={}'.format(why, len(t), len(t[0])))
        for j in range(len(t)):
            self.log('{:^3}'.format(t[j][0]), ind=0, end=' ')
        self.log(ind=0)
        for k in range(len(t)//10):
            for i in range(9): self.log('{:^3} '.format(' '), ind=0, end='')
            self.log(' {} '.format(d), ind=0, end=' ')
        self.log(ind=0)
        for j in range(len(t)):
            self.log('{:^3}'.format(t[j][1]), ind=0, end=' ')
        self.log(ind=0)
        if dbg:
            for i in range(len(t)):
                self.log('{:5}'.format(i + 1), ind=0, end=' ')
                self.log(' {:>5}'.format(t[i][0]), ind=0, end=' ')
                d2 = ' ' if i == 1 or (i + 1) % 10 else d
                self.log('{}{:>5}'.format(d2, t[i][1]), ind=0, end=' ')
                self.log(ind=0)

    def createLabelText(self):
        self.labelTextA.extend('{}'.format(j) for j in range(1, self.n[C] + 1))
        self.labelTextB.extend('{}'.format(j % 10 if j % 10 else j // 10 % 10) for j in range(1, self.n[C] + 1))
        self.log(f'labelTextA={fmtl(self.labelTextA)}', ind=0)
        self.log(f'labelTextB={fmtl(self.labelTextB)}', ind=0)
        texts = list(zip(self.labelTextA, self.labelTextB))
        self.log(f'texts={texts}', ind=0)
        self.dumpLabelText(texts)
    ####################################################################################################################################################################################################
    def geom(self, p=None, j=0, init=0, nn=0, dbg=1):
        mx, my = None, None  ;  iw, ih = self.w[j], self.h[j]
        n, i, x, y, w, h, g = self.n[j], self.i[j], self.x[j], self.y[j], self.w[j], self.h[j], self.g[j]
        if nn:                  n = nn
        if   j == C:            n += CCC
        if p is None:           w =  self.ww - x*2           ;  h =  self.hh  - y*2
        elif j == C:            w = (p.width - x*(n + 1))/n  ;  h =  p.height - y*2
        else:                   w =  p.width - x*2           ;  h = (p.height - y*(n + 1))/n
        if SPRITES:
            if p is None:                                       y = 0
            elif j == T:        x += p.x + w/2               ;  y = p.y + p.height - h/2
            else:                                               y = p.y + p.height - h
        else:
            if p is None:       x += w/2                     ;  y = h/2
            elif j == C:        x += w/2                     ;  y = p.y
            elif j == T:        x += p.x                     ;  y = p.y + p.height/2 - h/2
            else:               x += w/2                     ;  y = p.y + p.height/2 - h/2
        if not nn and init:     self.w[j] = w                ;  self.h[j] = h
        elif iw and ih:         mx = w/iw                    ;  my = h/ih
        if dbg:                 self.dumpGeom(j, n, i, x, y, w, h, mx, my, iw, ih, nn)
        return n, i, x, y, w, h, g, mx, my

    def dumpGeom(self, j, n, i, x, y, w, h, mx, my, iw, ih, nn):
        self.log(FMTR.format('    geom      {}  {:3}  {:4}            {:7.2f} {:7.2f} {:7.2f} {:7.2f} {:5.3f} {:5.3f}  {:7.2f} {:7.2f} {}', j, n, i, x, y, w, h, mx, my, iw, ih, nn), ind=0)
    ####################################################################################################################################################################################################
    def toggleTabs(self, tnik):
        self.log(f'(BGN) tnik={tnik} TNIK={fmtl(self.TNIK)} n={fmtl(self.n)} lenA={self.lenA()} lenB={self.lenB()}')
        if not self.TNIK[tnik] and not self.B[tnik]: self.showTabs(tnik)
        else:                                        self.hideTabs(tnik)
        self.TNIK[tnik] = not self.TNIK[tnik]   ;    self.n[S] = self.ss()
        self.log(f'calling on_resize() tnik={tnik} TNIK={fmtl(self.TNIK)} n={fmtl(self.n)} lenA={self.lenA()} lenB={self.lenB()}')
        self.on_resize(self.ww, self.hh)
        self.log(f'(END) tnik={tnik} TNIK={fmtl(self.TNIK)} n={fmtl(self.n)} lenA={self.lenA()} lenB={self.lenB()}')

    def hideTabs(self, tnik, dbg=1):
        tabs = self.B[tnik]   ;   cols = self.cols   ;  sects = self.sects
        ttype = 'Tab' if tnik == TT  else 'Note' if tnik == NN else 'Chord' if tnik == KK else '???'  ;  t, c, s = 0, 0, 0
        np, nl, ns, nc, nt = self.n
        ns2 = nl * ns
        nc2 = nc * ns2
        _tnik = tnik if tnik < 2 else 2
        self.log(f'(BGN) np={np} nl={nl} ns={ns} nc={nc} nt={nt} ns2={ns2} nc2={nc2} len({ttype})={len(tabs)}')
        for s in range(ns2-1, ns2-nl-1, -1):
            self.hideLabel(sects, s, 'Sect', dbg=dbg)
        for c in range(nc2-1, nc2-(len(cols)//nl)-1, -1):
            self.hideLabel(cols, c, 'Col', dbg=dbg)
        for t in range(len(tabs)):
            self.hideLabel(tabs, t, ttype, dbg=dbg)
        self.snapshot(f'hideTabs() t={t+1} c={c+1} s={s+1} len({ttype})={len(tabs)}')
        self.log(f'(END) t={t+1} c={c+1} s={s+1} len({ttype})={len(tabs)}')

    def showTabs(self, tnik):
        np, nl, ns, nc, nt = self.n           ;  tabs = self.B[tnik]
        _nt = nl * nc * nt  ;  _nc = nl * nc  ;  _ns = nl    ;   _tnik = tnik + len(self.B)
        ks  = self.ks       ;   kc = self.kc  ;  chordName = ''
        k = [self.kt, self.kn, self.ki, self.kk]
        ttype = 'Tab' if tnik == TT  else 'Note' if tnik == NN else 'Chord' if tnik == KK else '???'  ;  t, c, s = 0, 0, 0
        self.log(f'(BGN) _nt={_nt} _nc={_nc} _ns={_ns} len({ttype})={len(tabs)}')
        for s in range(_ns):
            self.showLabel(s, p=self.sects, j=S, t='Sect', g=self.g[S], k=ks)
        for c in range(_nc):
            self.showLabel(c, p=self.cols,  j=C, t='C',  g=self.g[C], k=kc)
        for t in range(_nt):
            tt = t % nt
            p, l, cc = t // _nt, t // (nc * nt), (t // nt) % nc
#            self.log(f'{p} {l} {cc} {tt}', ind=0, end=' ')
            tab = self.data[p][l][cc][tt]
            note = self.getNote(tt, tab).name if self.isFret(tab) else self.nblank
            if not t:   chordName = self.cobj.getChordName(p, l, cc)
            chord = chordName[tt] if len(chordName) > tt else ' '
            text  = tab if tnik == TT else note if tnik == NN else chord if tnik == KK else '???'
#            self.createLabel(text, j=_tnik, p=tabs, x=0, y=0, w=0, h=0, kk=self.cci(_t, k[tnik]), g=self.g[T], why=why, kl=k[tnik], dbg=dbg)
            self.showLabel(tt, p=tabs, j=_tnik, t=f'{text}', g=self.g[T], k=k[tnik])
        self.snapshot(f'showTabs() t={t+1} c={c+1} s={s+1} len({ttype})={len(tabs)}')
        self.log(f'(END) s={s} c={c} t={t} len({ttype})={len(tabs)}')
    ####################################################################################################################################################################################################
    def toggleRLCols(self):
        global CCC  ;  old = CCC  ;  CCC = (CCC + 1) % 3
        self.log(f'(BGN) old CCC={old} New CCC={CCC} lenC={self.lenC()} QQ={QQ}')
        show = 1 if (CCC == 1 and (not self.lenC()[0] or not self.lenC()[1])) or (CCC == 2 and (not self.lenC()[2])) else 0
        if show: self.showRLCols()
        else:    self.hideRLCols()
        self.log(f'      lenE={self.lenE()}')
        self.on_resize(self.ww, self.hh)
        self.log(f'(END) lenE={self.lenE()}')

    def showRLCols(self, dbg=1):
        self.dumpJ('showRLCols()')
        self.log(f'lenE={self.lenE()}')
        np, nl, ns, nc, nt = self.n   ;   l, s, c, t = 0, 0, 0, 0   ;   v = 1
        tt, nn, kkk = self.TNIK[TT], self.TNIK[NN], self.TNIK[KK]
        kt2, kn2, kk2 = self.kt2, self.kn2, self.kk2   ;   kc = self.kc   ;   kk, kl = kc, kt2
        self.log(f'(BGN) nl={nl} ns={ns} nc={nc} nt={nt} QQ={QQ}')
        for l in range(nl):
            for s in range(ns):
                c = CCC - 1     ;   self.log(f'CCC={CCC} l={l} s={s} c={c}')
                self.J1[C] = c  ;  self.J2[C] += 1   ;   why = f'New Col {self.J2[C]}'
                if SPRITES: self.createSprite(p=self.cols, x=0, y=0, w=self.w[C], h=self.h[C], kk=self.cci(c, kc), g=self.g[C], why=why, kl=kc, v=v, dbg=dbg)
                else:       self.createLabel(f'C {self.J2[C]}' if self.DF[C] else '',j=C, p=self.cols, x=0, y=0, w=0, h=0, kk=self.cci(c, kc), g=self.g[C], why=why, kl=kc, dbg=dbg)
                for t in range(nt):
                    text = '???'  ;  plist = []
                    if   tt and s == 0:
                        if   c == C1:  text = self.stringNumbs[t]   ;  plist = self.snos   ;  kl = kt2  ;  kk = self.cci(t, kl)  ;  self.J2[O] += 1 ;  why = f'New SNo  {self.J2[O]}'
                        elif c == C2:  text = self.stringCapo[t]    ;  plist = self.capos  ;  kl = kt2  ;  kk = self.cci(t, kl)  ;  self.J2[D] += 1 ;  why = f'New Capo {self.J2[D]}'
                        else: msg = f'ERROR Unexpected else c={c}'  ;  self.log(msg)  ;  self.quit(msg)
                        self.createLabel(text, j=T, p=plist, x=0, y=0, w=0, h=0, kk=kk, g=self.g[T], why=why, kl=kl, dbg=dbg)
                    elif nn and (s == 1 or (s == 0 and not tt)):
                        if   c == C1:  text = self.stringNames[t]   ;  plist = self.snas   ;  kl = kn2  ;  kk = self.cci(t, kl)  ;  self.J2[A] += 1  ;  why = f'New SNa  {self.J2[A]}'
                        elif c == C2:  text = self.stringCapo[t]    ;  plist = self.capos  ;  kl = kn2  ;  kk = self.cci(t, kl)  ;  self.J2[D] += 1  ;  why = f'New Capo {self.J2[D]}'
                        else: msg = f'ERROR Unexpected else c={c}'  ;  self.log(msg)  ;  self.quit(msg)
                        self.createLabel(text, j=N, p=plist, x=0, y=0, w=0, h=0, kk=kk, g=self.g[T], why=why, kl=kl, dbg=dbg)
                    elif kkk and (s == 2 or (s == 1 and (not tt or not nn)) or (s == 0 and (not tt and not nn))):
                        if   c == C1: text = self.strLabel[t]       ;  plist = self.strls  ;  kl = kk2  ;  kk = self.cci(t, kl)  ;  self.J2[E] += 1  ;  why = f'New StrL {self.J2[E]}'
                        elif c == C2: text = self.cpoLabel[t]       ;  plist = self.cpols  ;  kl = kk2  ;  kk = self.cci(t, kl)  ;  self.J2[F] += 1  ;  why = f'New CpoL {self.J2[F]}'
                        else: msg = f'ERROR Unexpected else c={c}'  ;  self.log(msg)  ;  self.quit(msg)
                        self.createLabel(text, j=K, p=plist, x=0, y=0, w=0, h=0, kk=kk, g=self.g[T], why=why, kl=kl, dbg=dbg)
                    else: msg = f'ERROR Unexpected else s={s}'  ;  self.log(msg)  ;  self.quit(msg)
        self.snapshot(f'showRLCols() l={l} s={s} c={c} t={t}')
        self.log('(END)')

    def hideRLCols(self, dbg=1):
        np, nl, ns, nc, nt = self.n   ;   cols = self.cols   ;   nc = len(cols)   ;   l, s, c = 0, 0, 0   ;   sno, sna, cap, strl, cpol = 0, 0, 0, 0, 0
        ccc = 2 # if CCC else 1
        self.log(f'(BGN) nl={nl} ns={ns} nc={nc} nt={nt} ccc={ccc}')
        for c in range(nc-1, nc - (ccc * ns * nl) - 1, -1):
            self.hideLabel(cols, c,   t='Col', dbg=dbg)
        snos, snas, capos, strls, cpols = self.snos, self.snas, self.capos, self.strls, self.cpols
        for sno in range(len(snos)):
            self.hideLabel(snos, sno, t='SNOS')
        for sna in range(len(snas)):
            self.hideLabel(snas, sna, t='SNAS')
        for cap in range(len(capos)):
            self.hideLabel(capos, cap, t='CAPOS')
        for strl in range(len(strls)):
            self.hideLabel(strls, strl, t='STRLS')
        for cpol in range(len(cpols)):
            self.hideLabel(cpols, cpol, t='CPOLS')
        self.snapshot(f'hideRLCols() l={l} s={s} c={c}  sno={sno} sna={sna} cap={cap} strl={strl} cpol={cpol}')
        self.log(f'(END) l={l} s={s} c={c}')
    ####################################################################################################################################################################################################
    def toggleLLRows(self):
        global QQ  ;  old = QQ  ;  QQ = not QQ  ;  self.log(f'old QQ={old} New QQ={QQ} CCC={CCC}')  ;  self.log(f'llText={fmtl(self.llText[CCC])}')
        if QQ and not self.llRows: self.showLLRows()
        else:                      self.hideLLRows()
        self.on_resize(self.ww, self.hh)

    def showLLRows(self):
        l = 0
        for l in range(len(self.lines)):
            self.log(f'l={l}')
            self.createLLRow(self.lines[l], l)
        self.snapshot(f'showLLRows() l={l}')

    def hideLLRows(self):
        nr = len(self.llRows)    ;  nc = len(self.llCols)  ;  cc, rr = 0, 0   ;   assert not nc % nr
        nc = nc // nr
        for rr in range(nr):
            self.hideLabel(self.llRows, rr, 'LLR')
            for cc in range(nc):
                self.hideLabel(self.llCols, cc + rr * nc, 'LLC')
        self.snapshot(f'hideLLRows() nr={nr} nc={nc} rr={rr} cc={cc}')
    ####################################################################################################################################################################################################
    def createLLRow(self, p, pi, dbg=1, dbg2=0):
        nn = self.n[T] * self.ss() + 1  ;  klr = self.klr  ;  klc = self.klc  ;  kkr = self.cci(pi, klr)
        nr, ir, xr, yr, wr, hr, gr, mx, my = self.geom(p=p, j=S, nn=nn, dbg=dbg2)
        if SPRITES: xr += wr/2  ;  yr += hr/2
        self.J1[LLR] = 0
        self.J2[LLR] += 1
        row = self.createLabel(f'LR {pi+1}' if self.DF[LLR] else '', LLR, self.llRows, xr, yr, wr, hr, kkr, gr, why=f'New LR {pi+1}', kl=klr, dbg=dbg)
        nc, ic, xc, yc, wc, hc, gc, mx, my = self.geom(p=row, j=C, nn=self.n[C], dbg=dbg2)   ;  sc = nc * pi
        self.log(f'nc={nc} pi={pi} sc={sc} len(llCols)={len(self.llCols)}')
        if SPRITES: xc += wc/2
        for c in range(nc):
            kkc = self.cci(pi, klc)
            sc += 1
            self.J1[LLC] = c
            self.J2[LLC] += 1
            text = self.llText[0]
            self.createLabel(f'{Z*(c+1)}{sc}' if self.DF[LLC] and not c else text[c], LLC, self.llCols, xc + c*wc, yc, wc, hc, kkc, gc, why=f'New LC {sc}', kl=klc, dbg=dbg)
#            if not CCC and c == 0:  self.hideLabel(self.llCols, sc-1, f'Hide LLC {sc}')
#            if CCC == 1 and c == 1: self.hideLabel(self.llCols, sc-1, f'Hide LLC {sc}')
        if dbg2: self.log('pi={:3} px={:7.2f} py={:7.2f} pw={:7.2f} ph={:7.2f}'.format(pi, p.x, p.y, p.width, p.height), ind=0)
        if dbg2: self.log('nr={:3} xr={:7.2f} yr={:7.2f} wr={:7.2f} hr={:7.2f}'.format(nr, xr, yr, wr, hr), ind=0)
        if dbg2: self.log('nc={:3} xc={:7.2f} yc={:7.2f} wc={:7.2f} hc={:7.2f}'.format(nc, xc, yc, wc, hc), ind=0)
        if   type(p) is pyglet.text.Label:    p.y -= hr/2  ;  p.height -= hr  # ;                      self.log(f'p.y -= hr/2, p.h -= hr: p.y = {p.y:7.2f} p.h = {p.height:7.2f}', ind=0)
        elif type(p) is pyglet.sprite.Sprite: my = (p.height - hr)/self.h[L]  ;   p.scale_y = my  # ;  self.log(f'p.y -= hr, my = (p.h-hr)/h[L]: h[L]={self.h[L]} my={my:7.5f} p.y={p.y:7.2f} p.h={p.height:7.2f}', ind=0)
        return p

    def resizeLLRow(self, p, pi, dbg=1, dbg2=0):
        nn = self.n[T] * self.ss() + 1
        nr, ir, xr, yr, wr, hr, gr, mxr, myr = self.geom(p=p, j=S, nn=nn, dbg=dbg2)
        if SPRITES: xr += wr/2  ;  yr += hr/2
        self.J1[LLR] = 0
        self.J2[LLR] += 1
        row = self.llRows[pi]    ;    row.width = wr  ;   row.height = hr  ;   row.x = xr  ;   row.y = yr
        if dbg: self.dumpLabel(row, *self.ids(), *self.cnts(), why=f'resize LR {pi+1}')
        nc, ic, xc, yc, wc, hc, gc, mxc, myc = self.geom(p=row, j=C, dbg=dbg)   ;  sc = nc * pi
        if dbg2: self.log(f'nc={nc} pi={pi} sc={sc} len(llCols)={len(self.llCols)}')
        if SPRITES: xc += wc/2
        for c in range(nc):
            self.J1[LLC] = c
            self.J2[LLC] += 1
#            if dbg: self.log(f 'sc={sc} c={c} len(llCols)={len(self.llCols)} n={fmtl(self.n)}')
            col = self.llCols[sc]
            col.text = self.llText[CCC][c]
            col.width = wc   ;   col.height = hc  ;   col.x = xc + c * wc  ;  col.y = yc  ;  sc += 1
            if dbg: self.dumpLabel(col, *self.ids(), *self.cnts(), why=f'resize LC {sc}')
        if dbg2: self.log(f'nc={nc} pi={pi} sc={sc} len(llCols)={len(self.llCols)}')
        if dbg2: self.log(f'row.y={row.y:7.2f} yr={yr:7.2f} pi={pi} hr={hr:7.2f}', ind=0)
        if dbg2: self.log('pi={:3} px={:7.2f} py={:7.2f} pw={:7.2f} ph={:7.2f}'.format(pi, p.x, p.y, p.width, p.height), ind=0)
        if dbg2: self.log('nr={:3} xr={:7.2f} yr={:7.2f} wr={:7.2f} hr={:7.2f}'.format(nr, xr, yr, wr, hr), ind=0)
        if dbg2: self.log('nc={:3} xc={:7.2f} yc={:7.2f} wc={:7.2f} hc={:7.2f}'.format(nc, xc, yc, wc, hc), ind=0)
        if   type(p) is pyglet.text.Label:    p.y -= hr/2  ;  p.height -= hr  # ;                               self.log(f'p.y -= hr/2, p.h -= hr: p.y = {p.y:7.2f} p.h = {p.height:7.2f}', ind=0)
        elif type(p) is pyglet.sprite.Sprite: my = (p.height - hr)/self.h[L]  ;   p.scale_y = my  # ;  self.log(f'p.y -= hr, my = (p.h-hr)/h[L]: h[L]={self.h[L]} my={my:7.5f} p.y={p.y:7.2f} p.h={p.height:7.2f}', ind=0)
        if dbg2: self.log('p.y -= hr/2, p.height -= hr: p.y = {:7.2f} p.h = {:7.2f}'.format(p.y, p.height), ind=0)
        return p
    ####################################################################################################################################################################################################
    def createLabels(self, dbg=1, dbg2=0):
        self.log(f'(BGN) {self.fmtGeom()}', ind=0)
        if dbg: self.dumpLabel()
        for p, page in                  enumerate(self.g_createLabels(None, P, self.pages, why='Page ', dbg=dbg, dbg2=dbg2)):
            for l, line in              enumerate(self.g_createLabels(page, L, self.lines, why='Line ', dbg=dbg, dbg2=dbg2)):
                for s, sect in          enumerate(self.g_createLabels(line, S, self.sects, why='Sect ', dbg=dbg, dbg2=dbg2)):
                    for c, col in       enumerate(self.g_createLabels(sect, C, self.cols,  why='C ',    dbg=dbg, dbg2=dbg2)):
                        for t, lbl in   enumerate(self.g_createLabels2(col)):
                            if dbg > 1: self.log(f'lbl.y={lbl.y}')
        if dbg: self.dumpLabel()
        self.log(f'(END) {self.fmtGeom()}', ind=0)

    def g_createLabels(self, p, j, lablist, why='', dbg=1, dbg2=0):
        n, ii, x, y, w, h, g, mx, my = self.geom(p=p, j=j, init=1, dbg=dbg2)  ;  x2 = x  ;  y2 = y  ;    kl = self.k[j]
        for m in range(n):
            if   j == C: x2 = x + m * w
            elif p:      y2 = y - m * h
            self.J1[j] = m  ;  self.J2[j] += 1
            text = f'{why}{self.J2[j]}' if self.DF[j] else ''  ;  why2 = f'New {why}{self.J2[j]}'
            lbl = self.createLabel(text=text, j=j, p=lablist, x=x2, y=y2, w=w, h=h, kk=self.cci(j, kl), g=g, why=why2, kl=kl, dbg=dbg)
            if QQ and j == L: self.createLLRow(lbl, m)
            yield lbl
    ####################################################################################################################################################################################################
    def g_createLabels2(self, col, dbg=1, dbg2=0):
        p, l, s, c = self.J1[P], self.J1[L], self.J1[S], self.J1[C]   ;  tt, nn, kkk = self.TNIK[TT], self.TNIK[NN], self.TNIK[KK]   ;   chordName = ''
        nt, it, xt, yt, wt, ht, gt, mx, my = self.geom(p=col, j=T, init=1, dbg=dbg2)   ;   kt, kn, kk = self.kt, self.kn, self.kk    ;    kt2, kn2, kk2 = self.kt2, self.kn2, self.kk2
        for t in range(nt): #            self.log(f't={t} nt={nt} TNIK={self.TNIK} st={self.J2[T]}') #            self.log(f's={s} tt={tt} nn={nn} kk={kkk}')#        self.log(f'p={p} l={l} s={s} c={c} nt={nt}')
            if   tt and s == 0:
                if   CCC     and c == C1:   tab = self.stringNumbs[t]    ;  plist = self.snos   ;  kl = kt2   ;  k = self.cci(t, kl)  ;  self.J2[O] += 1  ;  why = f'New SNo {self.J2[O]}'
                elif CCC > 1 and c == C2:   tab = self.stringCapo[t]     ;  plist = self.capos  ;  kl = kt2   ;  k = self.cci(t, kl)  ;  self.J2[D] += 1  ;  why = f'New Capo {self.J2[D]}'
                else:                       tab = self.data[p][l][c][t]  ;  plist = self.tabs   ;  kl = kt    ;  k = self.cci(t, kl)  ;  self.J2[T] += 1  ;  why = f'New Tab {self.J2[T]}'
                self.createLabel(tab, T,   plist,  xt, yt - t*ht, wt, ht, k, gt, why=why, kl=kl, dbg=dbg)  ;  yield tab
            elif nn and (s == 1 or (s == 0 and not tt)):
                if   CCC     and c == C1:  note = self.stringNames[t]    ;  plist = self.snas   ;  kl = kn2   ;  k = self.cci(t, kl)  ;  self.J2[A] += 1  ;  why = f'New SNam {self.J2[A]}'
                elif CCC > 1 and c == C2:  note = self.stringCapo[t]     ;  plist = self.capos  ;  kl = kn2   ;  k = self.cci(t, kl)  ;  self.J2[D] += 1  ;  why = f'New Capo {self.J2[D]}'
                else:                       tab = self.data[p][l][c][t]  ;  plist = self.notes  ;  kl = kn    ;  k = self.cci(t, kl)  ;  self.J2[N] += 1  ;  why = f'New Note {self.J2[N]}'  ;  note = self.getNote(t, tab).name if self.isFret(tab) else self.nblank
                self.createLabel(note, N,  plist,  xt, yt - t*ht, wt, ht, k, gt, why=why, kl=kl, dbg=dbg)  ;  yield note
            elif kkk and (s == 2 or (s == 1 and (not tt or not nn)) or (s == 0 and (not tt and not nn))):
                if   CCC     and c == C1: chord = self.strLabel[t]       ;  plist = self.strls   ;  kl = kk2   ;  k = self.cci(t, kl)  ;  self.J2[E] += 1  ;  why = f'New StrL {self.J2[E]}'
                elif CCC > 1 and c == C2: chord = self.cpoLabel[t]       ;  plist = self.cpols   ;  kl = kk2   ;  k = self.cci(t, kl)  ;  self.J2[F] += 1  ;  why = f'New CpoL {self.J2[F]}'
                else:
                    if not t: chordName = self.cobj.getChordName(p, l, c)
                    chord = chordName[t] if len(chordName) > t else ' '
                    plist = self.chords  ;  kl = kk    ;  k = self.cci(t, kl)  ;  self.J2[K] += 1  ;  why = f'New Chord {self.J2[K]}'
                self.createLabel(chord, K, plist,  xt, yt - t*ht, wt, ht, k, gt, why=why, kl=kl, dbg=dbg)  ;  yield chord
            else: self.log(f'ERROR Not Handled s={s} tt={tt} nn={nn} kk={kkk}')  ;  yield None
    ####################################################################################################################################################################################################
    def createSprites(self, dbg=1, dbg2=0):
        self.log(f'(BGN) {self.fmtGeom()}', ind=0)  ;  v = 0
        if dbg: self.dumpLabel()  ;  self.dumpSprite()
        for p, (page, v) in             enumerate(self.g_createSprites(None, P, self.pages, v, why=' Page ', dbg=dbg, dbg2=dbg2)):
            for l, (line, _) in         enumerate(self.g_createSprites(page, L, self.lines, v, why=' Line ', dbg=dbg, dbg2=dbg2)):
                for s, (sect, _) in     enumerate(self.g_createSprites(line, S, self.sects, v, why=' Sect ', dbg=dbg, dbg2=dbg2)):
                    for c, (col, _) in  enumerate(self.g_createSprites(sect, C, self.cols,  v, why=' Col ',  dbg=dbg, dbg2=dbg2)):
                        for t, lbl in   enumerate(self.g_createLabels2(col)):
                            if dbg > 1: self.log(f'lbl.y={lbl.y}')
        if dbg: self.dumpSprite()  ;  self.dumpLabel()
        self.log(f'(END) {self.fmtGeom()}', ind=0)

    def g_createSprites(self, p, j, sprlist, v, why, dbg=1, dbg2=0):
        n, ii, x, y, w, h, g, mx, my = self.geom(p=p, j=j, init=1, dbg=dbg2)  ;  x2 = x  ;  y2 = y  ;  kl=self.k[j]
        for m in range(n):
            if   j == C:     x2 = x + m * w
            elif p:          y2 = y - m * h
            self.J1[j] = m
            self.J2[j] += 1
            if   j == P:    v=1 if self.J2[j] == self.i[P] else 0
            spr = self.createSprite(sprlist, x2, y2, w, h, self.cci(j, kl), g, why=f'New{why}{self.J2[j]}', kl=kl, v=v, dbg=dbg)
            if QQ and j == L: self.createLLRow(spr, m)
            yield spr, v
    ####################################################################################################################################################################################################
    def resizeLabels(self, dbg=1):
        self.log(f'(BGN) {self.fmtGeom()}', ind=0)
        if dbg: self.dumpLabel()
        for p, page in                  enumerate(self.g_resizeLabels(None, P, self.pages, why=f' Page ')):
            for l, line in              enumerate(self.g_resizeLabels(page, L, self.lines, why=f' Line ')):
                for s, sect in          enumerate(self.g_resizeLabels(line, S, self.sects, why=f' Sect ')):
                    for c, col in       enumerate(self.g_resizeLabels(sect, C, self.cols,  why=f' Col ')):
                        for t, lbl in   enumerate(self.g_resizeLabels2(col)):
                            if dbg > 1: self.log(f'lbl.y={lbl.y}')
        if dbg: self.dumpLabel()
        self.log(f'(END) {self.fmtGeom()}', ind=0)

    def g_resizeLabels(self, p, j, lablist, why, dbg=1, dbg2=0):
        n, ii, x, y, w, h, g, mx, my = self.geom(p=p, j=j, dbg=dbg2)  ;  x2 = x  ;  y2 = y
        for m in range(n):
            if   j == C: x2 = x + m * w
            elif p:      y2 = y - m * h
            assert(len(lablist))
            lbl = lablist[self.J2[j]]  ;  lbl.x = x2  ;  lbl.y = y2  ;  lbl.width = w  ;  lbl.height = h
            self.J1[j] = m
            self.J2[j] += 1
            if dbg: self.dumpLabel(lbl, *self.ids(), *self.cnts(), why=f'Mod{why}{self.J2[j]}')
            if QQ and j == L: self.resizeLLRow(lbl, m)
            yield lbl
    ####################################################################################################################################################################################################
    def g_resizeLabels2(self, col, dbg=1, dbg2=0):
        n, ii, x, y, w, h, g, mx, my = self.geom(p=col, j=T, dbg=dbg2)  ;  lbl = None
        p,       l,    s,    c       = self.J1[P], self.J1[L], self.J1[S], self.J1[C]
        st,     sn,   si,   sk       = self.J2[T], self.J2[N], self.J2[I], self.J2[K]
        ssno, ssna, scap, strl, cpol = self.J2[O], self.J2[A], self.J2[D], self.J2[E], self.J2[F]
        tt, nn, kk = self.TNIK[TT], self.TNIK[NN], self.TNIK[KK]    # ;   chordName = ''
        for t in range(n):##            self.log(f 'tt={tt} nn={nn} kk={kk} TNIK={fmtl(self.TNIK)}  p={p} l={l} s={s} c={c}  st={st} sn={sn} si={si} sk={sk}', ind=0)
            if   tt and s == 0:
                if   CCC     and c == C1:   tab = self.snos[ssno]   ;  ssno += 1  ;  why = f'Mod SNo {ssno}'
                elif CCC > 1 and c == C2:   tab = self.capos[scap]  ;  scap += 1  ;  why = f'Mod Capo {scap}'
                else:                       tab = self.tabs[st]     ;    st += 1  ;  why = f'Mod Tab {st}'
                tab.width = w    ;   tab.height = h   ;   tab.x = x   ;  tab.y = y - t * h  ;  lbl = tab
                self.J1[T] = t   ;  self.J2[T] = st   ;  self.J2[O] = ssno  ;  self.J2[D] = scap
                if dbg:   self.dumpLabel(  lbl, *self.ids(), *self.cnts(), why=why)
            elif nn and (s == 1 and tt or (s == 0 and not tt)):
                if   CCC     and c == C1:  note = self.snas[ssna]   ;  ssna += 1  ;  why = f'Mod SNam {ssna}'
                elif CCC > 1 and c == C2:  note = self.capos[scap]  ;  scap += 1  ;  why = f'Mod Capo {scap}'
                else:                      note = self.notes[sn]    ;    sn += 1  ;  why = f'Mod Note {sn}'  # ;   note.text = self.getNote(t, ttab).name if self.isFret(ttab) else self.nblank
                note.width = w   ;  note.height = h   ;   note.x = x  ;    note.y = y - t * h  ;  lbl = note
                self.J1[N] = t   ;  self.J2[N] = sn   ;  self.J2[A] = ssna  ;  self.J2[D] = scap
                if dbg:   self.dumpLabel( lbl, *self.ids(), *self.cnts(), why=why)
            elif kk and ((s == 2 and  tt and nn) or (s == 1 and tt or nn) or (s == 0 and not tt and not nn)):
                if   CCC     and c == C1: chord = self.strls[strl]  ;  strl += 1  ;  why = f'Mod Strls {strl}'
                elif CCC > 1 and c == C2: chord = self.cpols[cpol]  ;  cpol += 1  ;  why = f'Mod Cpols {cpol}'
                else:
                    chord = self.chords[sk]   ;    sk += 1  ;  why = f'Mod Chord {sk}'
#                    if not t:   chordName = self.cobj.getChordName(p, l, c)
#                    chord.text = chordName[t] if len(chordName) > t else ' '
                chord.width = w  ;  chord.height = h  ;  chord.x = x  ;  chord.y = y - t * h  ;  lbl = chord
                self.J1[K] = t   ;  self.J2[K] = sk   ;  self.J2[E] = strl  ;  self.J2[F] = cpol
                if dbg:   self.dumpLabel(lbl, *self.ids(), *self.cnts(), why=why)
            else: e = f'Error: Not Handled s={s} tt={tt} nn={nn} kk={kk}'   ;  self.log(f'{e}')  ;  self.quit(e)
            yield lbl
    ####################################################################################################################################################################################################
    def resizeSprites(self, dbg=1):
        self.log(f'(BGN) {self.fmtGeom()}', ind=0)
        if dbg: self.dumpSprite()
        for p, page in                enumerate(self.g_resizeSprites(None, P, self.pages, why=f' Page ')):
            for l, line in            enumerate(self.g_resizeSprites(page, L, self.lines, why=f' Line ')):
                for s, sect in        enumerate(self.g_resizeSprites(line, S, self.sects, why=f' Sect ')):
                    for c, col in     enumerate(self.g_resizeSprites(sect, C, self.cols,  why=f' C ')):
                        for t, lbl in enumerate(self.g_resizeLabels2(col)):
                            if dbg > 1: self.log(f'lbl.y={lbl.y}')
        if dbg: self.dumpLabel()  ;  self.dumpSprite()
        self.log(f'(END) {self.fmtGeom()}', ind=0)

    def g_resizeSprites(self, p, j, sprlist, why, dbg=1, dbg2=0):
        nn = self.n[j] if QQ else 0
        n, ii, x, y, w, h, g, mx, my = self.geom(p=p, j=j, nn=nn, dbg=dbg2)  ;  x2 = x  ;  y2 = y
        for m in range(n):
            if   j == C: x2 = x + m * w
            elif p:      y2 = y - m * h
            spr = sprlist[self.J2[j]]
            spr.update(x=x2, y=y2, scale_x=mx, scale_y=my)
            self.J1[j] = m
            self.J2[j] += 1
            if dbg: self.dumpSprite(spr, *self.ids(), *self.cnts(), why = f'Mod{why}{self.J2[j]}')
            if QQ and j == L: self.resizeLLRow(spr, m)
            yield spr
    ####################################################################################################################################################################################################
    def createSprite(self, p, x, y, w, h, kk, g, why, kl=None, v=0, dbg=0):
        o, k, d, j, n, s = self.fontParams()
        k = FONT_COLORS[(k + kk) % len(FONT_COLORS)] if kl is None else kl[kk]
        scip = pyglet.image.SolidColorImagePattern(k)
        img = scip.create_image(width=fri(w), height=fri(h))
        spr = pyglet.sprite.Sprite(img, x, y, batch=self.batch, group=g, subpixel=SUBPIX)
        spr.visible = v
        spr.color, spr.opacity = k[:3], k[3]
        self.sprites.append(spr)
        if p is not None:      p.append(spr)
        if dbg: self.dumpSprite(spr, *self.ids(), *self.cnts(), why)
        return spr

    def createLabel(self, text, j, p, x, y, w, h, kk, g, why, kl=None, m=0, dbg=0):
        j1, j2 = self.J1[j], self.J2[j]
        a, ax, ay = 'center', 'center', 'center' # left center right  # bottom baseline center top
        b = self.batch
        o, k, d, ii, n, s = self.fontParams()
        d = FONT_DPIS[d]
        n = FONT_NAMES[n]
        k = FONT_COLORS[kk % len(FONT_COLORS)] if kl is None else kl[kk]
        if j == LLC and not ((len(p) + 1) % 10): k = self.kll[0]
        if m:
            for i in range(len(text), 0, -1): text = text[:i] + '\n' + text[i:]
        if len(p) > j2:
            self.log(f'ERROR Label Exists? j={j} j1={j1} j2={j2} len(p)={len(p)}')   # ;  self.quit('ERROR Unexpected if')
#            lbl = p[j1]
#            self.log(f'Old text={lbl.text} x={lbl.x:7.2f} y={lbl.y:7.2f} w={lbl.width:7.2f} h={lbl.height:7.2f}')
        lbl = pyglet.text.Label(text, font_name=n, font_size=s, bold=o, italic=ii, color=k, x=x, y=y, width=w, height=h, anchor_x=ax, anchor_y=ay, align=a, dpi=d, batch=b, group=g, multiline=m)
        self.labels.append(lbl)    ;    p.append(lbl)   # ;   self.log(f'Creating New j={j} j1={j1} len(p)={len(p)}')
        if dbg: self.dumpLabel(lbl, *self.ids(), *self.cnts(), why)
        return lbl
    ####################################################################################################################################################################################################
    def showLabel(self, i, p, j, t, g, k=None, v=1, dbg=1):
        self.J1[j] = i  ;  self.J2[j] += 1
        why = f'New {t} {self.J2[j]}'
        text = f'{t} {self.J2[j]}' if self.DF[j] else t if j>C else ''
        if SPRITES: self.createSprite(p=p, x=0, y=0, w=self.w[j], h=self.h[j], kk=self.cci(i, k), g=g, why=why, kl=k, v=v, dbg=dbg)
        else:       self.createLabel(text, j=j, p=p, x=0, y=0, w=0, h=0, kk=self.cci(i, k), g=g, why=why, kl=k, dbg=dbg)

    def hideLabel(self, p, j, t='???', dbg=1): #        c = self.E[j][n]
        c = p[j]    ;    ha = hasattr(c, 'text')
        x, y, w, h = c.x, c.y, c.width, c.height
        text = c.text if ha else '??'
        if SPRITES: c.update(x=0, y=0, scale_x=0, scale_y=0)
        else:       c.x, c.y, c.width, c.height = 0, 0, 0, 0
        if dbg:     self.log(f'{t:5} {j+1:3} {hex(id(c))} {text:6} {x:7.2f} {y:7.2f} {w:7.2f} {h:7.2f} {c.text:6} {c.x:7.2f} {c.y:7.2f} {c.width:7.2f} {c.height:7.2f}', ind=0)
    ####################################################################################################################################################################################################
    def dumpSprites(self, why=''):
        self.log(f'(BGN) {self.fmtGeom()} {why}', ind=0)
        np, nl, ns, nr, nc = self.n
        self.dumpSprite()
        i, sp, sl, ss, sc, st, sn, si, sk = 0, 0, 0, 0, 0, 0, 0, 0, 0
        for p in range(np):
            sp += 1                 ; self.dumpSprite(self.sprites[i], *self.ids(), *self.cnts(), why=f'Page {sp}') ; i += 1
            for l in range(nl):
                sl += 1             ; self.dumpSprite(self.sprites[i], *self.ids(), *self.cnts(), why=f'Line {sl}') ; i += 1
                for s in range(ns):
                    ss += 1         ; self.dumpSprite(self.sprites[i], *self.ids(), *self.cnts(), why=f'Sect {ss}') ; i += 1
                    for c in range(nc):
                        sc += 1     ; self.dumpSprite(self.sprites[i], *self.ids(), *self.cnts(), why=f'Col {sc}' ) ; i += 1
        self.dumpSprite()
        self.log(f'(END) {self.fmtGeom()} {why}',ind=0)

    def dumpTabs(self, why='', dbg=1):
        if dbg: self.log(f'(BGN) {self.fmtGeom()} {why}', ind=0)
        np, nl, ns, nc, nt = self.n  #;  nc += CCC
        i, sp, sl, ss, sc, st, sn, sk = 0, 0, 0, 0, 0, 0, 0, 0
        self.dumpLabel()
        for p in range(np):
            sp += 1
            for l in range(nl):
                sl += 1
                for s in range(ns):
                    ss += 1
                    for c in range(nc):
                        sc += 1
                        for t in range(nt):
                            if   s == 0:  self.dumpLabel(self.tabs[st],   *self.ids(), *self.cnts(), why=f'Tab {st} {why}')  ;  st += 1  ;  i += 1
                            elif s == 1:  self.dumpLabel(self.notes[sn],  *self.ids(), *self.cnts(), why=f'Note {sn} {why}')  ;  sn += 1  ;  i += 1
                            elif s == 2:  self.dumpLabel(self.chords[sk], *self.ids(), *self.cnts(), why=f'Chord {sk} {why}')  ;  sk += 1  ;  i += 1
        self.dumpLabel()
        if dbg: self.log(f'(END) {self.fmtGeom()} {why}', ind=0)

    def dumpCols(self, why='', dbg=1):
        if dbg: self.log(f'(BGN) {self.fmtGeom()} {why}', ind=0)
        np, nl, ns, nc, nt = self.n  #;  nc += CCC
        i, sp, sl, ss, sc, st, sn, si, sk = 0, 0, 0, 0, 0, 0, 0, 0, 0
        self.dumpLabel()
        for p in range(np):
            sp += 1
            for l in range(nl):
                sl += 1
                for s in range(ns):
                    ss += 1
                    for c in range(nc):
                        sc += 1
                        if SPRITES: self.dumpSprite(self.cols[i], *self.ids(), *self.cnts(), why=f'Col {sc} {why}')   ;  i += 1
                        else:        self.dumpLabel(self.cols[i], *self.ids(), *self.cnts(), why=f'Col {sc} {why}')   ;  i += 1
        self.dumpLabel()
        if dbg: self.log(f'(END) {self.fmtGeom()} {why}', ind=0)

    def dumpLabels(self, why='', dbg=1):
        np, nl, ns, nc, nt = self.n  #;  nc += CCC
        i, sp, sl, ss, sc, st, sn, si, sk = 0, 0, 0, 0, 0, 0, 0, 0, 0
        if dbg: self.log(f'(BGN) {self.fmtGeom()} {why}', ind=0)
        self.dumpLabel()
        if SPRITES:
            for p in range(np):
                sp += 1
                for l in range(nl):
                    sl += 1
                    for s in range(ns):
                        ss += 1
                        for c in range(nc):
                            sc += 1
                            for t in range(nt):
                                if   s == 0:  st += 1  ;  self.dumpLabel(self.labels[i], *self.ids(), *self.cnts(), why=f'Col {st} {why}')     ;  i += 1
                                elif s == 1:  sn += 1  ;  self.dumpLabel(self.labels[i], *self.ids(), *self.cnts(), why=f'Note {sn} {why}')    ;  i += 1
                                elif s == 2:  sk += 1  ;  self.dumpLabel(self.labels[i], *self.ids(), *self.cnts(), why=f'Chord {sk} {why}')   ;  i += 1
        else:
            for p in range(np):
                sp += 1                      ;  self.dumpLabel(self.labels[i], *self.ids(), *self.cnts(), why=f'Page {sp} {why}')  ;  i += 1
                for l in range(nl):
                    sl += 1                  ;  self.dumpLabel(self.labels[i], *self.ids(), *self.cnts(), why=f'Line {sl} {why}')  ;  i += 1
                    for s in range(ns):
                        ss += 1              ;  self.dumpLabel(self.labels[i], *self.ids(), *self.cnts(), why=f'Sect {ss} {why}')  ;  i += 1
                        for c in range(nc):
                            sc += 1          ;  self.dumpLabel(self.labels[i], *self.ids(), *self.cnts(), why=f'Col {sc} {why}')   ;  i += 1
                            for t in range(nt):
                                if   s == 0:  st += 1  ;  self.dumpLabel(self.labels[i], *self.ids(), *self.cnts(), why=f'Tab {st} {why}')  ;  i += 1
                                elif s == 1:  sn += 1  ;  self.dumpLabel(self.labels[i], *self.ids(), *self.cnts(), why=f'Note {sn} {why}')  ;  i += 1
                                elif s == 2:  sk += 1  ;  self.dumpLabel(self.labels[i], *self.ids(), *self.cnts(), why=f'Chord {sk} {why}')  ;  i += 1
        self.dumpLabel()
        if dbg: self.log(f'(END) {self.fmtGeom()} {why}', ind=0)
    ####################################################################################################################################################################################################
    def dumpSprite(self, z=None, sid=-1, lid=-1, p=-1, l=-1, s=-1, c=-1, t=-1, n=-1, i=-1, k=-1, why=''):
        if z is None: self.log(f' sid  lid p  l  s   c   t   n   i   k    x       y       w       h         id         mx    my   red grn blu opc   why         v   group       parent', ind=0); return
        f = '{:4} {:4} {} {:2} {:2} {:3} {:3} {:3} {:3} {:3} {:7.2f} {:7.2f} {:7.2f} {:7.2f} {} {:5.3f} {:5.3f} {:3} {:3} {:3} {:3} {:12} {:1} {} {}'
        kk, o, v, g, pg    =    z.color, z.opacity, z.visible, z.group, z.group.parent   ;   ID = hex(id(z))
        x, y, w, h, iax, iay, m, mx, my, rot    =    z.x, z.y, z.width, z.height, z.image.anchor_x, z.image.anchor_y, z.scale, z.scale_x, z.scale_y, z.rotation
        fs = f.format(sid, lid, p, l, s, c, t, n, i, k, x, y, w, h, ID, mx, my, kk[0], kk[1], kk[2], o, why, v, g, pg)
        self.log(fs, ind=0)
        assert(type(z) == pyglet.sprite.Sprite)

    def dumpSprite_OLD(self, z=None, sid=-1, lid=-1, p=-1, l=-1, s=-1, c=-1, t=-1, n=-1, i=-1, k=-1, why=''):  #  ;  ID = hex(id(z))
        if z is None: self.log(f' sid  lid p  l  s   c   t   n   i   k    x       y       w       h     iax  iay   m     mx    my     rot  red grn blu opc   why         v   group       parent', ind=0); return
        f = '{:4} {:4} {} {:2} {:2} {:3} {:3} {:3} {:3} {:3} {:7.2f} {:7.2f} {:7.2f} {:7.2f} {:4} {:4} {:5.3f} {:5.3f} {:5.3f} {:7.2f} {:3} {:3} {:3} {:3} {:12} {:1} {} {}'
        kk, o, v, g, pg    =    z.color, z.opacity, z.visible, z.group, z.group.parent
        x, y, w, h, iax, iay, m, mx, my, rot    =    z.x, z.y, z.width, z.height, z.image.anchor_x, z.image.anchor_y, z.scale, z.scale_x, z.scale_y, z.rotation
        fs = f.format(sid, lid, p, l, s, c, t, n, i, k, x, y, w, h, iax, iay, m, mx, my, rot, kk[0], kk[1], kk[2], o, why, v, g, pg)
        self.log(fs, ind=0)
        assert(type(z) == pyglet.sprite.Sprite)

    def dumpLabel(self, a=None, sid=-1, lid=-1, p=-1, l=-1, s=-1, c=-1, t=-1, n=-1, i=-1, k=-1, why=''):
        if a is None: self.log(f' sid  lid p  l  s   c   t   n   i   k    x       y       w       h    text    font name   siz dpi b i red grn blu opc   why', ind=0) ; return
        x, y, w, h, fn, d, z, kk, b, ii, tx    =    a.x, a.y, a.width, a.height, a.font_name, a.dpi, a.font_size, a.color, a.bold, a.italic, a.text  ;  ID = hex(id(a))
        f = '{:4} {:4} {} {:2} {:2} {:3} {:3} {:3} {:3} {:3} {:7.2f} {:7.2f} {:7.2f} {:7.2f} {:6} {:13} {:2} {:3} {:1} {:1} {:3} {:3} {:3} {:3} {} '
        fs = f.format(sid, lid, p, l, s, c, t, n, i, k, x, y, w, h, tx, ID, z, d, b, ii, kk[0], kk[1], kk[2], kk[3], why)
        self.log(fs, ind=0)
    ####################################################################################################################################################################################################
    def resizeFonts(self):
        ms = self.minSize()  ;  slope, off = 0.6, -1
        fs = fri(ms * slope + off)  ;  formula = '(fs = ms*slope+off)'
        self.log('{} {} ms={:4.1f} slope={} off={} fs={:4.1f}={:2}'.format(self.fmtWH(), formula, ms, slope, off, fs, fri(fs)))
        self.setFontParam('font_size', fs, 'fontSize')

    def minSize(self):
        b = self.B
        self.log(f'len(b)={len(b)} lenB={self.lenB()}')
        tabs = b[TT] if b[TT] and b[TT][0].width and b[TT][0].height else b[NN] if b[NN] and b[NN][0].width and b[NN][0].height else b[KK] if b[KK] and b[KK][0].width and b[KK][0].height else None
        w = tabs[0].width  if tabs else 20
        h = tabs[0].height if tabs else 20
        m = min(w, h)
        self.log(f'w={w:5.1f} h={h:5.1f} m={m:5.1f}')
        return m

    def fontParams(self):    return self.fontBold, self.fontColorIndex, self.fontDpiIndex, self.fontItalic, self.fontNameIndex, self.fontSize
    def fmtf(self):
        fb, fc, fd, fi, fn, fs = self.fontParams()
        text = '{}dpi {}pt {} {}'.format(FONT_DPIS[fd], fs, FONT_NAMES[fn], FONT_COLORS[fc])
        self.log('{}'.format(text))
        return text

    def dumpFont(self, why=''):
        b, k, dpi, i, n, s = self.fontParams()
        pix = FONT_SCALE * s / dpi
#        self.log(f'{why} ki={k} di={dpi}={FONT_DPIS[dpi]}DPI {s}pt ni={n} {FONT_NAMES[n]} {FONT_SCALE}*{m}')
        self.log('({}) {} {}DPI {}pt {} ({:6.3f}*{}pt/{}DPI)={:6.3f}pixels'.format(why, k, dpi, s, n, FONT_SCALE, s, dpi, pix))

    def setFontParam(self, n, v, m):
        setattr(self, m, v)
        self.log('n={} v={:.1f} m={}'.format(n, v, m))
        if SPRITES:
            if QQ: self._setFontParam(self.llRows, n, v, m)  ;  self._setFontParam(self.llCols, n, v, m)
            self._setFontParam(self.tabs,   n, v, m)
            self._setFontParam(self.notes,  n, v, m)
            self._setFontParam(self.chords, n, v, m)
        else:      self._setFontParam(self.labels, n, v, m)

    @staticmethod
    def _setFontParam(p, n, v, m):
        for j in range(len(p)):
            setattr(p[j], n, FONT_NAMES[v] if m == 'fontNameIndex' else FONT_COLORS[v] if m == 'fontColorIndex' else FONT_DPIS[v] if m == 'fontDpiIndex' else v)
    ####################################################################################################################################################################################################
    def kpEvntTxt(self):
        return '{:8} {:8}     {:14} {:2} {:16}'.format(self.kbk, self.symb, self.symbStr, self.mods, self.modsStr)

    def on_key_press(self, symb, mods, dbg=0):
        self.symb, self.mods, self.symbStr, self.modsStr = symb, mods, pygwink.symbol_string(symb), pygwink.modifiers_string(mods)
        self.kbk = self.symbStr  ;  kbk = self.kbk
        if dbg: self.log('(BGN) {}'.format(self.kpEvntTxt()))
        if                  self.isTab(kbk):                          self.addTab(kbk,  'on_key_press')
        elif kbk == 'B' and self.isCtrl(mods) and self.isShift(mods): self.toggleBlank()
        elif kbk == 'B' and self.isCtrl(mods):                        self.toggleBlank()
        elif kbk == 'D' and self.isCtrl(mods) and self.isShift(mods): self.toggleDir()
        elif kbk == 'D' and self.isCtrl(mods):                        self.toggleDir()
        elif kbk == 'E' and self.isCtrl(mods) and self.isShift(mods): self.erase()
        elif kbk == 'E' and self.isCtrl(mods):                        self.erase()
        elif kbk == 'F' and self.isCtrl(mods) and self.isShift(mods): self.toggleFullScreen()
        elif kbk == 'F' and self.isCtrl(mods):                        self.toggleFullScreen()
        elif kbk == 'I' and self.isCtrl(mods) and self.isShift(mods): self.toggleCursorMode()
        elif kbk == 'I' and self.isCtrl(mods):                        self.toggleCursorMode()
        elif kbk == 'K' and self.isCtrl(mods) and self.isShift(mods): self.toggleTabs(KK)
        elif kbk == 'K' and self.isCtrl(mods):                        self.toggleTabs(KK)
        elif kbk == 'L' and self.isCtrl(mods) and self.isShift(mods): self.toggleLLRows()
        elif kbk == 'L' and self.isCtrl(mods):                        self.toggleLLRows()
        elif kbk == 'M' and self.isCtrl(mods) and self.isShift(mods): self.toggleRLCols()
        elif kbk == 'M' and self.isCtrl(mods):                        self.toggleRLCols()
        elif kbk == 'N' and self.isCtrl(mods) and self.isShift(mods): self.toggleTabs(NN)
        elif kbk == 'N' and self.isCtrl(mods):                        self.toggleTabs(NN)
        elif kbk == 'Q' and self.isCtrl(mods) and self.isShift(mods): self.quit(        'keyPress({})'.format(kbk))
        elif kbk == 'Q' and self.isCtrl(mods):                        self.quit(        'keyPress({})'.format(kbk))
        elif kbk == 'R' and self.isCtrl(mods) and self.isShift(mods): self.toggleChordName(rev=1)
        elif kbk == 'R' and self.isCtrl(mods):                        self.toggleChordName(rev=0)
        elif kbk == 'S' and self.isCtrl(mods) and self.isShift(mods): self.writeDataFile()
        elif kbk == 'S' and self.isCtrl(mods):                        self.writeDataFile()
        elif kbk == 'T' and self.isCtrl(mods) and self.isShift(mods): self.toggleTabs(TT)
        elif kbk == 'T' and self.isCtrl(mods):                        self.toggleTabs(TT)
    ####################################################################################################################################################################################################
        elif kbk == 'B' and self.isAlt(mods) and self.isShift(mods):  self.setFontParam('bold',   not self.fontBold,   'fontBold')
        elif kbk == 'B' and self.isAlt(mods):                         self.setFontParam('bold',   not self.fontBold,   'fontBold')
        elif kbk == 'I' and self.isAlt(mods) and self.isShift(mods):  self.setFontParam('italic', not self.fontItalic, 'fontItalic')
        elif kbk == 'I' and self.isAlt(mods):                         self.setFontParam('italic', not self.fontItalic, 'fontItalic')
        elif kbk == 'S' and self.isAlt(mods) and self.isShift(mods):  self.setFontParam('font_size', (self.fontSize + 1)       % 52,               'fontSize')
        elif kbk == 'S' and self.isAlt(mods):                         self.setFontParam('font_size', (self.fontSize - 1)       % 52,               'fontSize')
        elif kbk == 'D' and self.isAlt(mods) and self.isShift(mods):  self.setFontParam('dpi',       (self.fontDpiIndex + 1)   % len(FONT_DPIS),   'fontDpiIndex')
        elif kbk == 'D' and self.isAlt(mods):                         self.setFontParam('dpi',       (self.fontDpiIndex - 1)   % len(FONT_DPIS),   'fontDpiIndex')
        elif kbk == 'N' and self.isAlt(mods) and self.isShift(mods):  self.setFontParam('font_name', (self.fontNameIndex + 1)  % len(FONT_NAMES),  'fontNameIndex')
        elif kbk == 'N' and self.isAlt(mods):                         self.setFontParam('font_name', (self.fontNameIndex - 1)  % len(FONT_NAMES),  'fontNameIndex')
        elif kbk == 'C' and self.isAlt(mods) and self.isShift(mods):  self.setFontParam('color',     (self.fontColorIndex + 1) % len(FONT_COLORS), 'fontColorIndex')
        elif kbk == 'C' and self.isAlt(mods):                         self.setFontParam('color',     (self.fontColorIndex - 1) % len(FONT_COLORS), 'fontColorIndex')
#        self.updateCaption()
        if dbg: self.log('(END) {}'.format(self.kpEvntTxt()))

    def on_text(self, text, dbg=0):
        self.kbk = text
        if dbg: self.log('(BGN) {}'.format( self.kpEvntTxt()))
        if self.isTab(self.kbk):                         self.addTab(self.kbk, 'on_text')
        if self.kbk=='$' and self.isShift(self.mods):    self.snapshot()
#        self.updateCaption()
        if dbg: self.log('(END) {}'.format( self.kpEvntTxt()))

    def on_text_motion(self, motion, dbg=1):
        self.kbk = motion
        if dbg: self.log('(BGN) {}'.format(self.kpEvntTxt()))
        if self.mods == 0:
            if   motion == pygwink.MOTION_LEFT:              self.move(-self.tpc)
            elif motion == pygwink.MOTION_RIGHT:             self.move( self.tpc)
            elif motion == pygwink.MOTION_UP:                self.move(-1)
            elif motion == pygwink.MOTION_DOWN:              self.move( 1)
            elif motion == pygwink.MOTION_BEGINNING_OF_LINE: self.move(-self.tpc *  self.j()[C])
            elif motion == pygwink.MOTION_END_OF_LINE:       self.move( self.tpc * (self.n[C] - self.i[C]))
            elif motion == pygwink.MOTION_PREVIOUS_PAGE:     self.move(-self.tpc *  self.n[C]) # Line?
            elif motion == pygwink.MOTION_NEXT_PAGE:         self.move( self.tpc *  self.n[C]) # Line?
#            elif motion==pygwink.MOTION_PREVIOUS_PAGE: self.move() # prevPage(self.i[P], motion)
#            elif motion==pygwink.MOTION_NEXT_PAGE:     self.move() # nextPage(self.i[P], motion)
            else:                                      self.log('on_text_motion() motion={} ???'.format(motion))
#            self.updateCaption()
        if dbg: self.log('(END) {}'.format(self.kpEvntTxt()))
    ####################################################################################################################################################################################################
    def createCursor(self, g):
        self.cc = self.cursorCol()
        c = self.tabs[self.cc]
        w, h = c.width, c.height
        x, y = c.x - w/2, c.y - h/2
        self.log('c={} x={:6.1f} y={:6.1f} w={:6.1f} h={:6.1f} i={}'.format(self.cc, x, y, w, h, fmtl(self.i, FMTN)))
        self.dumpSprite()
        self.cursor = self.createSprite(None, x, y, w, h, -1, g, why='cursor', v=1, dbg=1)

    def resizeCursor(self):
        cc = self.cursorCol()
        c = self.tabs[cc]
        w, h = c.width, c.height  ;  x, y = c.x - w/2, c.y - h/2
        self.log('c={} x={:6.1f} y={:6.1f} w={:6.1f} h={:6.1f} i={}'.format(cc, x, y, w, h, fmtl(self.i, FMTN)))
        self.cursor.update(x=x, y=y, scale_x=w/self.w[T], scale_y=h/self.h[T])

    def cursorCol(self, dbg=1): #calc
        p, l, s, c, t = self.j()
        tpp, tpl, tps, tpc = self.tpz()
        cc = p * tpp + l * tpl + s * tps + c * tpc + t
        if dbg: self.log(f' p={p} l={l} s={s} c={c} t={t}', ind=0, end='')
        if dbg: self.log(f' tpp={tpp} tpl={tpl} tps={tps} tpc={tpc}', ind=0, end='')
        if dbg: self.log(f' cc={cc} = ( {p*tpp} + {l*tpl} + {s*tps} + {c*tpc} + {t} )', ind=0, end='')
        lenT = len(self.tabs)   ;   ccm = cc % lenT
        if dbg : self.log(f' cc = cc % len(tabs) = {cc} % {lenT} = {ccm} = cc', ind=0)
        return ccm
    ####################################################################################################################################################################################################
    def on_mouse_release(self, x, y, button, modifiers):
        np, nl, ns, nc, nt = self.n   ;  nc += CCC   ;  nt += QQ        ;  y0 = y
        y = self.hh - y      ;   w = self.ww/nc      ;  h  = self.hh/(nl*ns*nt)
        c  = int(x/w) - CCC  ;  r0 = int(y/h) - QQ   ;  d0 = int(ns*nt)
        l = int(r0/d0)       ;   r = int(r0 % d0)    ;   s = int(r/d0)  ;  p = 0  ;  t = r
        kk = int(p * self.tpp + l * self.tpl + s * self.tps + c * self.tpc + t)
        self.log(f'(BGN) x={x} y0={y0:4} w={w:6.2f} h={h:6.2f}', file=sys.stdout)
        self.log(f'y={y:4} r0={r0:4} d0={d0} r={r}', file=sys.stdout)
        self.log(f'p={p} l={l} s={s} c={c} t={t} kk={kk}', file=sys.stdout)
        self.log(f'tabs[kk].txt={self.tabs[kk].text}', file=sys.stdout)
        k  = kk - self.cc
        self.log('      {:4} {:4} {:4} {} b={} m={} txt={}'.format(k, kk, self.cc, fmtl(self.i, FMTN), button, modifiers, self.tabs[self.cc].text), file=sys.stdout)
        self.move(k)
        self.log('(END) {:4} {:4} {:4} {} b={} m={} txt={}'.format(k, kk, self.cc, fmtl(self.i, FMTN), button, modifiers, self.tabs[self.cc].text), file=sys.stdout)

    def move(self, k, dbg=1):
        if dbg: self.log('(BGN) {:4}      {:4} {} text={}'.format(k, self.cc, fmtl(self.i, FMTN), self.tabs[self.cc].text), file=sys.stdout)
        if not self.SNAP0: t = self.tabs[self.cc]  ;  self.snapshot('pre-move() k={:4} kk={:3} {} text={} {:6.2f} {:6.2f}'.format(k, self.cc, fmtl(self.i, FMTN), t.text, t.x, t.y))  ;  self.SNAP0 = 1
        self._move(k)
        kk = self.cursorCol()
        t = self.tabs[kk]  ;  x = t.x - t.width/2  ;  y = t.y - t.height/2
        self.cc = kk
        self.cursor.update(x=x, y=y)
        if dbg: self.log('(END) {:4} {:4} {:4} {} text={} {:6.2f} {:6.2f}'.format(k, kk, self.cc, fmtl(self.i, FMTN), self.tabs[self.cc].text, x, y), file=sys.stdout)
        self.armSnap = 'move() k={:4} kk={:4} {} text={} {:6.2f} {:6.2f}'.format(k, kk, fmtl(self.i, FMTN), self.tabs[self.cc].text, x, y)

    def _move(self, k, dbg=1):
        np, nl, ns, nc, nt = self.n
        p,  l,  s,  c,  t = self.j()
        jt = t + k
        if dbg: self.log('(BGN) {:4}      {:4} {} nt={}'.format(k, self.cc, fmtl(self.i, FMTN), nt), file=sys.stdout)
        self.i[T] = jt %  nt + 1
        jc   =  c + jt // nt
        self.i[C] = jc %  nc + 1
        jl   =  l + jc // nc
        self.i[L] = jl %  nl + 1
        jp   =  p + jl // nl
        ip0  = self.i[P]
        self.i[P] = jp %  np + 1
        if dbg: self.log('(END) {:4}      {:4} {} ip0={} jp={} jl={} jc={} jt={}'.format(k, self.cc, fmtl(self.i, FMTN), ip0, jp, jl, jc, jt), file=sys.stdout)

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
    def updateCaption(self, txt):
        self.set_caption(txt)

    def addTab(self, text, why='', dbg=1):
        self.log('(BGN) {} {} {}'.format(self.kpEvntTxt(), fmtl(self.i, FMTN), why))
        cc = self.cursorCol()
        melodyModeDist   = self.n[T]
        chordModeDist    = self.direction
        arpeggioModeDist = melodyModeDist + self.direction
        self.updateData(text)
        if self.TNIK[TT]: self.updateTab(cc, text)
        if self.TNIK[NN]: self.updateNote(cc, text)
        if self.TNIK[KK]: self.updateChord(cc)
        if   self.cursorMode == self.cursorModes['MELODY']:    self.move(melodyModeDist)
        elif self.cursorMode == self.cursorModes['CHORD']:     self.move(chordModeDist)
        elif self.cursorMode == self.cursorModes['ARPEGGIO']:  self.move(arpeggioModeDist)
        if dbg: self.snapshot()
        self.log('(END) {} {} {}'.format(self.kpEvntTxt(), fmtl(self.i, FMTN), why))

    def updateData(self, text, data=None, dbg=0, dbg2=0):
        if data is None: data = self.data
        p, l, s, c, r = self.j()
        t = data[p][l][c]
        if dbg: self.log('(BGN) data[{}][{}][{}]={}'.format(p, l, c, self.data[p][l][c]))
        self.data[p][l][c] = t[0:r] + text + t[r+1:]
        if dbg2: self.dumpTabs(why='updateData text={} i={} data[p][l][c]={}'.format(text, self.i, data[p][l][c]))
        if dbg: self.log('(END) data[{}][{}][{}]={}'.format(p, l, c, self.data[p][l][c]))

    def updateTab(self, cc, txt, dbg=0, dbg2=0):
        if dbg: self.log('(BGN) tabs[{}].text={}'.format(cc, self.tabs[cc].text))
        self.tabs[cc].text = txt
        if dbg2: self.tabs[cc].color = FONT_COLORS[self.fontColorIndex + 4]
        if dbg: self.log('(END) tabs[{}].text={}'.format(cc, self.tabs[cc].text))

    def updateNote(self, cc, txt, dbg=0, dbg2=0):
        p, l, s, c, r = self.j()
        if dbg: self.log('(BGN) notes[{}].text={}'.format(cc, self.notes[cc].text))
        self.notes[cc].text = self.getNote(r, txt).name if self.isFret(txt) else self.nblank
        if dbg2: self.notes[cc].color = FONT_COLORS[self.fontColorIndex + 4]
        if dbg: self.log('(END) notes[{}].text={}'.format(cc, self.notes[cc].text))

    def updateChord(self, cc, dbg=0, dbg2=0):
        p, l, s, c, r = self.j()
        if dbg: self.log('(BGN) chords[{}].text=<{}>'.format(cc, self.chords[cc].text))
        chordName = self.cobj.getChordName(p, l, c)
        if dbg2: self.log(f'cc={cc} p={p} l={l} c={c} r={r} chordName=<{chordName:<6}>')
        self.updateChordName(cc, chordName)
        if dbg: self.log('(END) chords[{}].text=<{}>'.format(cc, self.chords[cc].text))

    def updateChordName(self, cc, name, dbg=0):
        tc = cc - self.j()[T]
        for k in range(self.n[T]):
            self.chords[tc + k].text = name[k] if len(name) > k else ' '
            if dbg:self.log(f'chords[{tc+k}].text={self.chords[tc+k].text}')
    ####################################################################################################################################################################################################
    def toggleChordName(self, rev=0):
        p, l, s, c, r = self.j()
        cc = c + l * self.n[C]
        self.log(f'(BGN) len={len(self.cobj.mlimap[cc])} p={p} l={l} c={c} r={r} cc={cc} rev={rev} {self.cobj.mlimap[cc]}')
        chordName = self.cobj.toggleChordName(rev)
        cc2 = self.cursorCol()
        self.updateChordName(cc2, chordName)
        self.log(f'(END) len={len(self.cobj.mlimap[cc])} p={p} l={l} c={c} r={r} cc={cc} cc2={cc2} rev={rev} {self.cobj.mlimap[cc]}')

    def toggleCursorMode(self):
        self.log(f'(BGN) cursorMode={self.cursorMode}')
        self.cursorMode  = (self.cursorMode + 1) % len(self.cursorModes)
        self.log(f'(END) cursorMode={self.cursorMode}')

    def toggleDir(self):
        self.log(f'(BGN) direction={self.direction}')
        self.direction *= -1
        self.log(f'(END) direction={self.direction}')

    def toggleFullScreen(self):
        global FULL_SCREEN
        FULL_SCREEN =  not  FULL_SCREEN
        self.set_fullscreen(FULL_SCREEN)
        self.log('FULL_SCREEN={}'.format(FULL_SCREEN))

    def toggleBlank(self):
        prevBlank    =  self.tblank
        self.log('(BGN)'.format())
        self.tblanki = (self.tblanki + 1) % len(self.tblanks)
        self.tblank  =  self.tblanks[self.tblanki]
        self.swapTabs(prevBlank,     self.tblank)
        self.log('(END)'.format())

    def swapTabs(self, src, trg, data=None):
        if data is None: data = self.data
        self.log('(BGN) replace({},{})'.format(src, trg))
        np, nl, ns, nr, nc = self.n  ;  nc += CCC
        for i in range(len(self.tabs)):
            self.tabs[i].text  = self.tabs[i].text.replace(src, trg)
            self.notes[i].text = self.notes[i].text.replace(src, trg)
        for p in range(np):
            for l in range(nl):
                for c in range(nc):
                    self.log('before data[{}][{}][{}]={}'.format(p, l, c, data[p][l][c]))
                    data[p][l][c] = data[p][l][c].replace(src, trg)
                    self.log('after  data[{}][{}][{}]={}'.format(p, l, c, data[p][l][c]))
        self.log('(END) replace({},{})'.format(src, trg))
    ####################################################################################################################################################################################################
    def erase(self, reset=0):
        np, nl, ns, nr, nc = self.n  ;  nc += CCC
        self.log('(BGN) np={} nl={} ns={} nr={} nc={}'.format(np, nl, ns, nr, nc))
        for i in range(len(self.tabs)):
            self.tabs[i].text  = self.tblank
            self.notes[i].text = self.tblank
        for p in range(np):
            for l in range(nl):
                for c in range(nc):
                    self.data[p][l][c] = self.tblankCol
        if reset:
            self.log('reset={} CCC={}'.format(reset, CCC))
            if CCC:     self.setStringNumbs()  ;  self.setStringNames()
            if CCC > 1: self.setCapo()
        self.log('(END) np={} nl={} nr={} nc={}'.format(np, nl, nr, nc))
    '''
    def setStringNumbs(self):
        np, nl, ns, nr, nc = self.n  ;  nc += CCC  ;  i = C1
        for p in range(np):
            for l in range(nl):
                self.data[p][l][C1] = self.stringNumbs
                self.log('p={} l={} c={} data[p][l][c]={}'.format(p, l, C1, self.data[p][l][C1]))
                for r in range(nr):
                    self.tabs[i].text  = self.stringNumbs[r]
                    self.log('({} {} {}) '.format(r, i, self.tabs[i].text), ind=0, end='')
                    i += nc
                self.log(ind=0)

    def setStringNames(self):
        np, nl, ns, nr, nc = self.n  ;  nc += CCC  ;  i = C1
        for p in range(np):
            for l in range(nl):
                self.data[p][l][C1] = self.stringNames
                self.log('p={} l={} c={} data[p][l]={}'.format(p, l, C1, self.data[p][l][C1]))
                for r in range(nr):
                    self.notes[i].text = self.stringNames[r]
                    self.log('({} {} {}) '.format(r, i, self.notes[i].text), ind=0, end='')
                    i += nc
                self.log(ind=0)

    def setCapo(self):
        np, nl, ns, nr, nc = self.n  ;  nc += CCC  ;  i = C2
        for p in range(np):
            for l in range(nl):
                self.data[p][l][C2] = self.stringCapo
                self.log('p={} l={} c={} data[p][l]={}'.format(p, l, C2, self.data[p][l][C2]))
                for r in range(nr):
                    self.tabs[i].text  = self.stringCapo[r]
                    self.notes[i].text = self.stringCapo[r]
                    self.log('({} {} {} {}) '.format(r, i, self.tabs[i].text, self.notes[i].text), ind=0, end='')
                    i += nc
                self.log(ind=0)
    '''
    ####################################################################################################################################################################################################
    @staticmethod
    def isCtrl(mods):        return mods & pygwink.MOD_CTRL
    @staticmethod
    def isShift(mods):       return mods & pygwink.MOD_SHIFT
    @staticmethod
    def isAlt(mods):         return mods & pygwink.MOD_ALT
    @staticmethod
    def isFret(text):        return True if '0'<=text<='9'      or 'a'<=text<='o'    else False
    def isTab(self, text):   return True if text == self.tblank or Tabs.isFret(text) else False
    @staticmethod
    def getFretNum(tab, dbg=0):
        fretNum = None
        if   '0' <= tab <= '9': fretNum = int(tab)
        elif 'a' <= tab <= 'o': fretNum = int(ord(tab) - 87)
        if dbg: Tabs.log('tab={} fretNum={}'.format(tab, fretNum))
        return fretNum

    def getNoteIndex(self, r, fn, dbg=0):
        row = self.n[T] - r - 1    # Reverse and zero base the string numbering: str[1 ... numStrings] => s[(numStrings - 1) ... 0]
        if dbg: self.log('r={} fretNum={} row={} stringMap={}'.format(r, fn, row, fmtd(self.stringMap)))
        k = self.stringKeys[row]
        i = self.stringMap[k] + fn
        if dbg: self.log('r={} fretNum={} row={} k={} i={}'.format(r, fn, row, k, i))
        return i

    def getNote(self, row, tab, dbg=0):
        fretNum = self.getFretNum(tab)
        note = misc.Note(self.getNoteIndex(row, fretNum))
        if dbg: self.log('row={} tab={} fretNum={} note.name={} note.index={}'.format(row, tab, fretNum, note.name, note.index))
        return note
    ####################################################################################################################################################################################################
    def cci(self, c, cc, dbg=0):
        if c == 0: self.ci = (self.ci + 1) % len(cc)
        k = (c + self.ci) % len(cc)
        if dbg: self.log('c={} cc={} ci={} k={}'.format(c, cc, self.ci, k))
        return k
    @staticmethod
    def ordSfx(n):
        m = n % 10
        if   m == 1 and n != 11: return 'st'
        elif m == 2 and n != 12: return 'nd'
        elif m == 3 and n != 13: return 'rd'
        else:                    return 'th'
    ####################################################################################################################################################################################################
    def snapshot(self, why='', dbg=0, dbg2=0):
        if dbg: self.log('SFX={} SNAP_DIR={} SNAP_SFX={} baseName={} basePath={}'.format(SFX, SNAP_DIR, SNAP_SFX, BASE_NAME, BASE_PATH))
        SNAP_ID   = '.{}'.format(self.ssi)
        SNAP_NAME = BASE_NAME + SFX + SNAP_ID + SNAP_SFX
        SNAP_PATH = BASE_PATH / SNAP_DIR / SNAP_NAME
        pyglet.image.get_buffer_manager().get_color_buffer().save('{}'.format(SNAP_PATH))
        if dbg: self.log('SNAP_ID={} SNAP_NAME={} SNAP_PATH={}'.format(SNAP_ID, SNAP_NAME, SNAP_PATH))
        if dbg2: self.log('{} {}'.format(SNAP_NAME, why), file=sys.stdout)
        self.ssi += 1

    def dumpStack(self, si):
        for i, e in enumerate(si):
            fp = pathlib.Path(e.filename)  ;            n = fp.stem  ;            l = e.lineno  ;            f = e.function  ;            c = e.code_context[0].strip()  ;            j = len(si) - (i + 1)
            self.log('{:2} {:9} {:5} {:20} {}'.format(j, n, l, f, c))
        self.log('MAX_STACK_DEPTH={:2}'.format(MAX_STACK_DEPTH))

    @staticmethod
    def indent(): d = Tabs.stackDepth() - 4;  return '{:{}}'.format(d, d)

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
            if dbg: Tabs.log('ids={}'.format(ids))
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
        if file != LOG_FILE: Tabs.log(msg, ind, flush=False, sep=',', end=end)
    ####################################################################################################################################################################################################
    def quit(self, why='', dbg=0):
        self.cobj.dumpMLimap()
        self.log('(BGN)')
        self.dumpJ('quit()')
        self.log(QUIT, ind=0)
        self.dumpStruct('quit ' + why)
#        self.dumpLabels('Quit')
        self.snapshot()
        self.log(QUIT, ind=0)
        if dbg:
            self.dumpStack(inspect.stack())
            self.log(QUIT, ind=0)
            self.dumpStack(MAX_STACK_FRAME)
        self.dumpGlobalFlags()
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
        Tabs()
        ret     = pyglet.app.run()
        Tabs.log(f'pyglet.app.run() returned {ret}, Exiting main')
