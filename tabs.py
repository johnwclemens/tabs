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
    def get_field(self, field_name, args, kwargs): # Handle missing key
        try:
            val = super().get_field(field_name, args, kwargs)
        except (KeyError, AttributeError):
            val = None,field_name
        return val
    def format_field(self, value, spec):           # handle invalid formats
        if value is None : return self.missing
        try:
            return super().format_field(value, spec)
        except ValueError:
            if self.badfmt is not None: return self.badfmt
            else: raise
FMTR = MyFormatter()
####################################################################################################################################################################################################
CHECKER_BOARD = 0  ;  EVENT_LOG = 0  ;  FULL_SCREEN = 1  ;  ORDER_GROUP = 1  ;  READ_DATA_FILE = 1  ;  RESIZE = 1  ;  SEQ_LOG_FILES = 1  ;  SUBPIX = 1
VRSN1            = 1  ;  SFX1 = chr(65 + VRSN1)  ;  QQ      = VRSN1  ;  VRSNX1 = f'VRSN1={VRSN1}       QQ={QQ     }  SFX1={SFX1}'
VRSN2            = 0  ;  SFX2 = chr(49 + VRSN2)  ;  SPRITES = VRSN2  ;  VRSNX2 = f'VRSN2={VRSN2}  SPRITES={SPRITES}  SFX2={SFX2}'
VRSN3            = 0  ;  SFX3 = chr(97 + VRSN3)  ;  CCC     = VRSN3  ;  VRSNX3 = f'VRSN3={VRSN3}      CCC={CCC    }  SFX3={SFX3}'
SFX              = f'.{SFX1}.{SFX2}.{SFX3}'
VERBOSE          = 0
PATH             = pathlib.Path(sys.argv[0])
BASE_PATH        = PATH.parent
BASE_NAME        = BASE_PATH.stem
SNAP_DIR         = 'snaps'
SNAP_SFX         = '.png'
LOG_FILE         = None
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
MELODY, CHORD, ARPG   = 0, 1, 2
LEFT, RIGHT, UP, DOWN = 0, 1, 0, 1
CSR_MODES        = ['MELODY', 'CHORD', 'ARPG']
HARROWS, VARROWS = ['LEFT', 'RIGHT'], ['UP', 'DOWN']
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
CC               = [(235, 230,  12, OPACITY[4]), (33, 26, 20, OPACITY[1])]
HUES             = 16
MAX_STACK_DEPTH  = 0  ;  MAX_STACK_FRAME = inspect.stack()
####################################################################################################################################################################################################
def fmtl(l, w=None, u='<', d1='[', d2=']'):
    t = ''
    for i in range(len(l)):
        if w is None:                  t += f'{l[i]} '
        elif type(w) is int  or type(w) is str:           t += f'{l[i]:{u}{w}} '
        elif type(w) is list or type(w) is tuple: t += f'{int(l[i]):{u}{w[i]}} '
    return d1 + t[:-1] + d2
def fmtd(m, w=2, d0=':', d1='[', d2=']'):
    t = ''
    for k, v in m.items():
        if   type(v) is int or type(v) is str:  t += f'{k:>{w}}{d0}{v:<{w}} '
        elif type(v) is list: t += fmtl(v, w)
    return d1 + t.rstrip() + d2
def genColors(cp, nsteps=HUES, dbg=0):
    colors, clen = [], len(cp[0])
    diffs = [cp[1][i] - cp[0][i] for i in range(clen)]
    steps = [diffs[i]/nsteps     for i in range(clen)]
    if dbg: print(f'c1={cp[0]} c2={cp[1]} nsteps={nsteps} diffs={diffs} steps=', end='')  ;  print(f'[{steps[0]:6.1f} {steps[1]:6.1f} {steps[2]:6.1f} {steps[3]:6.1f}]')
    for j in range(nsteps):
        c = tuple([fri(cp[0][i] + j * steps[i]) for i in range(len(cp[0]))])
        if dbg: print(f'c[{j}]={c}')
        colors.append(c)
    if dbg: print(f'colors={cp}')
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
CCS           = genColors(CC)         ;  COLORS.append(CCS)
COLORS        = (INFRA_REDS, REDS, ORANGES, YELLOWS, GRAYS, GREENS, GREEN_BLUES, CYANS, BLUE_GREENS, BLUES, INDIGOS, VIOLETS, ULTRA_VIOLETS)
FONT_SCALE    = 123.42857
FONT_DPIS     = [72, 78, 84, 90, 96, 102, 108, 114, 120]
FONT_NAMES    = ['Times New Roman', 'Lucida Console', 'Courier New', 'Helvetica', 'Arial', 'Century Gothic', 'Bookman Old Style', 'Antique Olive']
FONT_COLORS_S = [PINKS[0], CYANS[0], REDS[0], BLUES[0], YELLOWS[0], GREENS[0], ORANGES[0], VIOLETS[0], REDS[13], YELLOWS[15], GREEN_BLUES[8], ORANGES[12], INDIGOS[8], ULTRA_VIOLETS[9], BLUE_GREENS[8], CC]
FONT_COLORS_L = [PINKS[0], GRAYS[0], BLUES[0], GREENS[0], YELLOWS[0], REDS[0], GRAYS[1], PINKS[8], REDS[10], YELLOWS[15], GRAYS[8], GRAYS[8], INDIGOS[8], GRAYS[9], GRAYS[8], CC]
FONT_COLORS   =  FONT_COLORS_S if SPRITES else FONT_COLORS_L
####################################################################################################################################################################################################
class Tabs(pyglet.window.Window):
    hideST = ['log', 'dumpWBWAW']
    def __init__(self):
        global FULL_SCREEN, SUBPIX, ORDER_GROUP
        snapGlobArg = str(BASE_PATH / SNAP_DIR / BASE_NAME) + SFX + '.*' + SNAP_SFX
        snapGlob    = glob.glob(snapGlobArg)
        self.log(f'(BGN) {__class__}')
        self.log(f'{VRSNX1}')
        self.log(f'{VRSNX2}')
        self.log(f'{VRSNX3}')
        self.dumpGlobalFlags()
        self.log(f'snapGlobArg={snapGlobArg}')
        self.log(f'   snapGlob={snapGlob}')
        self.delGlob(snapGlob, 'SNAP_GLOB')
        self.cobj = misc.Chord(self, LOG_FILE)
        self.n    = []
        self.TNIK = [1, 1, 0, 1]
        nt        = 6 if QQ else 6
        self.log(f'TNIK={(fmtl(self.TNIK))}')
        self.ww, self.hh = 640, 480
        self.n, self.i, self.x, self.y, self.w, self.h, self.g = [1, 3, self.ssc(), 50, nt], [1, 1, 1, 1, nt], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], []
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
#        self.log(f'[N]            N={self.N}')
        self.log(f'[n]            n={fmtl(self.n, FMTN)}')
        self.log(f'[i]            i={fmtl(self.i, FMTN)}')
        self.log(f'[x]            x={fmtl(self.x, FMTN)}')
        self.log(f'[y]            y={fmtl(self.y, FMTN)}')
        self.log(f'[w]           ww={self.ww}')
        self.log(f'[h]           hh={self.hh}')
        self.log(f'[f]  FULL_SCREEN={FULL_SCREEN}')
        self.log(f'[g]  ORDER_GROUP={ORDER_GROUP}')
        self.log(f'[s]       SUBPIX={SUBPIX}')
        self.fontBold, self.fontItalic, self.fontColorIndex, self.fontDpiIndex, self.fontNameIndex, self.fontSize = 0, 0, 0, 4, 0, 48 if FULL_SCREEN else 14
        self.dumpFont()
        if    self.n[T] == 6: self.stringMap = collections.OrderedDict([('E2', 28), ('A2', 33), ('D3', 38), ('G3', 43), ('B3', 47), ('E4', 52)])
        elif  self.n[T] == 7: self.stringMap = collections.OrderedDict([('E2', 28), ('A2', 33), ('D3', 38), ('G3', 43), ('B3', 47), ('E4', 52), ('A4', 57)])
        else:                 self.stringMap = collections.OrderedDict([('E2', 28), ('A2', 33), ('D3', 38), ('G3', 43), ('B3', 47), ('E4', 52)])
        self.stringKeys  = list(self.stringMap.keys())
        self.stringNames = ''.join(reversed([str(k[0]) for k in self.stringKeys]))
        self.stringNumbs = ''.join([str(r+1)  for r in range(self.n[T])])
        self.stringCapo  = ''.join(['0' for _ in range(self.n[T])])
        self.log(f'stringMap   = {fmtd(self.stringMap)}')
        self.log(f'stringKeys  = {fmtl(self.stringKeys) } = {self.stringKeys}')
        self.log(f'stringNames = {fmtl(self.stringNames)} = {self.stringNames}')
        self.log(f'stringNumbs = {fmtl(self.stringNumbs)} = {self.stringNumbs}')
        self.log(f'stringCapo  = {fmtl(self.stringCapo) } = {self.stringCapo}')
        self.strLabel = 'STRING'
        self.cpoLabel = ' CAPO '
        self.log(f'strLabel = {fmtl(self.strLabel)} = {self.strLabel}')
        self.log(f'cpoLabel = {fmtl(self.cpoLabel)} = {self.cpoLabel}')
        self.csrMode, self.hArrow, self.vArrow  = CHORD, RIGHT, UP    ;    self.dumpCursorArrows('init()')
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
        self.log(f'(END) {__class__} {VRSNX1} {VRSNX2} {VRSNX3}')
        self.log(f'{INIT}', ind=0)

    def dumpGlobalFlags(self):
    #    text = 'CHECKER_BOARD={} EVENT_LOG={} FULL_SCREEN={} ORDER_GROUP={} READ_DATA_FILE={} RESIZE={} SEQ_LOG_FILES={} SUBPIX={}'
    #    self.log(text.format(CHECKER_BOARD, EVENT_LOG, FULL_SCREEN, ORDER_GROUP, READ_DATA_FILE, RESIZE, SEQ_LOG_FILES, SUBPIX), ind=0, end='')
        self.log(f'CHECKER_BOARD={CHECKER_BOARD} EVENT_LOG={EVENT_LOG} FULL_SCREEN={FULL_SCREEN} ORDER_GROUP={ORDER_GROUP} READ_DATA_FILE={READ_DATA_FILE} RESIZE={RESIZE} SEQ_LOG_FILES={SEQ_LOG_FILES} SUBPIX={SUBPIX}', ind=0, end='')
        self.log(f' CCC={CCC}', ind=0)

    def _initWindowA(self, dbg=1):
        display      = pyglet.canvas.get_display()
        if dbg: self.log(f'(BGN) {self.fmtWH()}')  ;  self.log(f'display={display}')
        self.screens = display.get_screens()  ;  s = self.screens
        if dbg:
            for i in range(len(s)): self.log(f'screens[{i}] x={s[i].x} y={s[i].y:5} {self.fmtWH(s[i].width, s[i].height)}')
            self.log(f'(END) {self.fmtWH()}')

    def _initWindowB(self, dbg=1):
        self.batch = pyglet.graphics.Batch()
        self._initGroups()
        if dbg: self.log(f'(BGN) {self.fmtWH()}')
        self.set_visible()
        if not FULL_SCREEN: self.set_size(self.ww, self.hh)
        self.ww, self.hh = self.get_size()
        if EVENT_LOG and VERBOSE:
            self.eventLogger = pygwine.WindowEventLogger()
            self.push_handlers(self.eventLogger)
#            self.keyboard = pygwine.key.KeyStateHandler()
#            self.push_handlers(self.keyboard)
        if dbg: self.log(f'(END) {self.fmtWH()}')

    def fmtWH(self, w=None, h=None, d1='(', d2=')'):
        (w, h) = (self.ww, self.hh) if not w and not h else (w, h)
        return f'{d1}{w} x {h}{d2}'
    ####################################################################################################################################################################################################
    def _initGroups(self):
        for i in range(len(self.n)+3):
            p = None if ORDER_GROUP or i==0 else self.g[i-1]
            self.g.append(self._initGroup(i, p))
            self.log(f'({i}) g={self.g[i]} pg={self.g[i].parent}')

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
        if dbg: self.log(f'tps={fmtl(self.tpz())}')

    def dumpObj( self, obj, name, why=''): self.log(f'{why} Obj {name} {hex(id(obj))}')
    def dumpObjs(self, obj, name, why=''): self.log(f'{why} Obj {name} ')   ;    [self.log(f'{hex(id(o))} type={type(o)}', ind=0) for o in obj]   ;    self.log(ind=0)
    def ss(self):    s = sum(self.TNIK)  ;                      self.log(f's={s}      TNIK={   fmtl(self.TNIK)} n={fmtl(self.n)}')  ;  return s
    def ssc(self):   s = self.ss()  ;  sc = s if s else 1   ;   self.log(f's={s} sc={sc} TNIK={fmtl(self.TNIK)} n={fmtl(self.n)}')  ;  return sc
    def tpz(self):   return self.tpp, self.tpl, self.tps, self.tpc
    def lens(self):  return self.lenA(), self.lenB(), self.lenC(), self.lenD()
    def lenA(self):  return [len(e) for e in self.A]
    def lenB(self):  return [len(e) for e in self.B]
    def lenC(self):  return [len(e) for e in self.C]
    def lenD(self):  return [len(e) for e in self.D]
    def lenE(self):  return [len(e) for e in self.E]
    def initJ(self): self.J1 = [0 for _ in self.E]  ;  self.J2 = [0 for _ in self.E]  ;  self.dumpJ('initJ()')  ;  return self.J1, self.J2
    def dumpJ(self, why):
        if VERBOSE: self.log(f'J1({len(self.J1)}))={self.J1} {why}')  ;  self.log(f'J2({len(self.J2)}))={self.J2} {why}')
    def updateJs(self, i, v): self.J1[i] = v    ;    self.J2[i] += 1
    def j(self):     return [i-1 if i else 0 for i in self.i]
    def dl(self, data=None):
        if data is None: data = self.data
        return len(data), len(data[0]), len(data[0][0]), len(data[0][0][0])

    def fmtDataDim(self, data=None): return '({} x {} x {} x {})'.format(*self.dl(data))
    def fmtGeom(self): return f'{self.cc} {fmtl(self.i, FMTN)} {fmtl(self.n, FMTN)} {fmtl(self.lenA())} {sum(self.lenA())} {fmtl(self.lenB())} {sum(self.lenB())} {fmtl(self.lenC())} {sum(self.lenC())} {fmtl(self.lenD())} {sum(self.lenD())}'
#    def fmtGeom(self): return '{} {} {} {} {} {} {} {} {} {} {}'.format(self.cc, fmtl(self.i, FMTN), fmtl(self.n, FMTN), fmtl(self.lenA()), sum(self.lenA()), fmtl(self.lenB()), sum(self.lenB()), fmtl(self.lenC()), sum(self.lenC()), fmtl(self.lenD()), sum(self.lenD()))
    def ordDict(self, od): self.log(f'{od.items()}')

    def ids(self):
        if SPRITES: return sum(self.J2[:4]), sum(self.J2[4:8])
        else:       return 0,                sum(self.J2[:4]) + sum(self.J2[4:8])
    def cnts(self): return self.J2[:8]  # self.log(f'J2({len(self.J2)}))={self.J2}')
    ####################################################################################################################################################################################################
    def _init(self, dbg=1):
        dataDir  = 'data'  ;  dataSfx = '.dat'  ;  dataPfx = f'.{self.n[C]}'
        dataName = BASE_NAME + SFX + dataPfx + dataSfx
        self.dataPath = BASE_PATH / dataDir / dataName
        self.log(f'(BGN) {self.fmtGeom()}', ind=0)
        self.kp  = [VIOLETS[0], VIOLETS[12]] if CHECKER_BOARD else [VIOLETS[10]]
        self.kl  = [  BLUES[12],  BLUES[15]] if CHECKER_BOARD else [BLUES[12]]
        self.ks  = [   CYANS[12],   CYANS[15]] if CHECKER_BOARD else [CYANS[12]]
        self.kc  = [GRAYS[9],    GRAYS[13]] if CHECKER_BOARD else [GRAYS[13]]
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
        self.labelTextC = []  ;  self.labelTextC.append('M')         ;  self.labelTextC.extend(self.labelTextB)
        self.labelTextD = []  ;  self.labelTextD.extend(['R', 'M'])  ;  self.labelTextD.extend(self.labelTextB)
        self.llText = []
        self.llText.append(self.labelTextB)
        self.llText.append(self.labelTextC)
        self.llText.append(self.labelTextD)
        self.log(f'textC={self.labelTextC}')
        self.log(f'textD={self.labelTextD}')
        self.dumpJ('(BGN) createSprites() / createLabels()')
        self.ssc()
        self.smap = {}  ;  self.skeys = []
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
        self.log(f'(BGN) {self.fmtWH()} {self.fmtDataDim(self.data)}')
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
        self.log(f'(END) {self.fmtWH()} {self.fmtDataDim(self.data)}')
    ####################################################################################################################################################################################################
    def dumpStruct(self, why=''):
        self.log(f'(BGN) {why}')
#        self.dumpData(why)
#        if SPRITES: self.dumpSprites()
#        self.dumpLabels(why)
#        self.dumpTabs(why)
        self.dumpStruct2()
        self.log(f'(END) {why}')

    def dumpStruct2(self, why=''):
        self.log(f'(BGN) {why}')
        self.dumpFont(why)
        self.dumpGlobalFlags()
        self.log(f'{self.fmtGeom()}', ind=0)
        self.log(f'{self.fmtDataDim(self.data)} {self.fmtDataDim(self.data)}')
        self.log(f'(END) {why}')
    ####################################################################################################################################################################################################
    def writeDataFile(self):
        self.log(f'(BGN) {self.fmtDataDim(self.data)}')
        data = self.transposeData(self.data) if self.isVert() else self.data
        with open(str(self.dataPath), 'w') as DATA_FILE:
            np, nl, nc, nr = self.dl()  ;  nc += CCC
            for p in range(np):
                self.log(f'writing {p+1}{self.ordSfx(p+1)} page')
                for l in range(nl):
                    self.log(f'writing {l+1}{self.ordSfx(l+1)} line')
                    for r in range(nr):
                        text = ''
                        for c in range(nc):
                            text += data[p][l][r][c]
                        self.log(f'writing {r+1}{self.ordSfx(r+1)} string {text}')
                        text += '\n'
                        DATA_FILE.write(text)
                    if l+1 < nl: DATA_FILE.write('\n')
        self.log(f'(END) {self.fmtDataDim(self.data)}')
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
        if dbg: self.log(f'nl={nl} nr={nr} nc={nc}')
        with open(str(self.dataPath), 'r') as DATA_FILE:
            DATA_FILE.seek(0, 2)  ;  size = DATA_FILE.tell()  ;  DATA_FILE.seek(0, 0)
            self.log(f'(BGN) {DATA_FILE.name:40} {size:8,} bytes = {size/1024:4,.0f} KB')
            strings = []  ;  lines = []
            l, r, c = 1, 0, 0
            while l <= nl:
                s = DATA_FILE.readline().strip('\n')
                if len(s): strings.append(s)  ;  r += 1  ;  c = len(s)
                else:
                    lines.append(strings)
                    strings=[]
                    self.log(f'read    {l:2}{self.ordSfx(l)} Line with {c:6,} Cols on {r:4,} Strings {c*r:8,} Tabs')
                    if l == nl: break
                    r = 0
                    l += 1
                if c:  self.log(f'l={l} r={r} c={c}: {s}')
            self.data.append(lines)
        nt   = l * c * r
        self.tblankCol = self.tblank * r
        vert = self.isVert()
        self.log(f'read     {l:2} Lines with {l*c:6,} Cols on {l*r:4,} Strings {nt:8,} Tabs, vdf={vert} blankCol({len(self.tblankCol)})={self.tblankCol}')
        if dbg: self.dumpDataHorz()
        self.data = self.transposeData()
        vert      = self.isVert()
        if dbg: self.dumpDataVert()
        self.log(f'assert: size=nt+2*(l*r+l-1) {nt:8,} + {2*(l*r+l-1)} = {size:8,} bytes assert isVert={vert}')
#        assert size == nt + 2 * (l * r + l - 1)  ;  assert vert
        self.log(f'(END) {DATA_FILE.name:40} {size:8,} bytes = {size/1024:4,.0f} KB')

    def isVert(self, data=None, dbg=1):
        if data is None: data = self.data
        vert = 1
        if dbg: self.log(f'(BGN) type(data 0 00 000)={type(data)} {type(data[0])} {type(data[0][0])} {type(data[0][0][0])}')
        assert type(data) is list and type(data[0]) is list and type(data[0][0]) is list and type(data[0][0][0]) is str
        for p in range(len(data)):
            assert len(data[p]) == len(data[0])
            for l in range(len(data[p])):
                assert len(data[p][l]) == len(data[p][0])
                for c in range(len(data[p][l])):
                    assert len(data[p][l][c]) == len(data[p][l][0])
                if len(data[p][l]) < len(data[p][l][0]): vert = 0  ;  break
        if dbg: self.log(f'(BGN) len(data 0 00 000)={len(data)} {len(data[0])} {len(data[0][0])} {len(data[0][0][0])} return vdf={vert}')
        return vert
    ####################################################################################################################################################################################################
#   def dumpTabData(self, data=None, why='', lc=1, ll=1, i=0):
#        if data is None: data = self.data
#        self.log(f'(BGN) {why}')
#        self.dumpDataVert(data, lc, ll, i) if self.isVert(data) else self.dumpDataHorz(data, lc, ll, i)
#        transposeData = self.transposeData(data, why='Internal')
#        self.dumpDataVert(transposeData, lc, ll, i) if self.isVer(transposeData) else self.dumpDataHorz(transposeData, lc, ll, i)
#        self.log(f'(END) {why}')

    def dumpDataHorz(self, data=None, lc=1, ll=1, i=0):
        if data is None: data = self.data
        self.log(f'(BGN) lc={lc} ll={ll} i={i} {self.fmtDataDim(data)}')
        for p in range(len(data)):
            for l in range(len(data[p])):
                if ll:  llt = f'Line {l+1}'  ;  llab = f'{llt:{i+1}}'  ;  self.log(f'{Z*i}{llab}', ind=0)
                if lc:  self.dumDataLabels(data[p][l], i=i, sep=Z)
                for r in range(len(data[p][l])):
                    self.log(f'{Z*i}', ind=0, end='')
                    for c in range(len(data[p][l][r])):
                        self.log(f'{data[p][l][r][c]}', ind=0, end='')
                    self.log(ind=0)
                self.log(ind=0)
        self.log(f'(END) lc={lc} ll={ll} i={i} {self.fmtDataDim(data)}')

    def dumpDataVert(self, data=None, lc=1, ll=1, i=0):
        if data is None: data = self.data
        self.log(f'(BGN) lc={lc} ll={ll} i={i} {self.fmtDataDim(data)}')
        if ll:
            t0 = Z * i + COLL + Z       if        i >= 0 else COLL
            self.log(t0, ind=0, end='') if lc and i >= 0 else self.log(Z * i, ind=0, end='')
            w = max(len(data[0][0][0]), len(LINL) + 1)
            for p in range(len(data)):
                for l in range(len(data[0])):
                    t = f'{LINL}{l+1}'
                    self.log(f'{t:{w}}', ind=0, end=Z)
                self.log(ind=0) #            self.log(t0, ind=0)         if lc and i < 0 else self.log(ind=0)
        for p in range(len(data)):
            for c in range(len(data[p][0])):
                self.log(f'{Z*i}{c+1:3} ', ind=0, end='') if i >= 0 and lc else self.log(f'{Z*i}', ind=0, end='')
                for l in range(len(data[p])):
                    self.log(f'{data[p][l][c]}', ind=0, end=Z)
                self.log(ind=0) #            self.log(f'{c+1:3} ',        ind=0)           if i <  0 and c else self.log(ind=0)
        self.log(f'(END) lc={lc} ll={ll} i={i} {self.fmtDataDim(data)}')
    ####################################################################################################################################################################################################
    def dumDataLabels(self, data=None, i=0, sep='%'):
        pp = '  '  ;  qq = ' @'
        p = pp[:] if CCC > 1 else pp[:1] if CCC else ''
        q = qq[:] if CCC > 1 else qq[:1] if CCC else ''
        if data is None: data = self.data
        n = len(data[0])-CCC    ;  a = ' ' * i if i else ''   ;  b = sep * n  ;  r = sep * 3
        if n >= 100:   self.log(   f'{a}{p}', ind=0, end='')  ;  [  self.log(f'{c//100}'   if c>=100 else ' ', ind=0, end='') for c in range(1, n+1) ]  ;  self.log(ind=0)
        if n >= 10:    self.log(   f'{a}{p}', ind=0, end='')  ;  [  self.log(f'{c//10%10}' if c>=10  else ' ', ind=0, end='') for c in range(1, n+1) ]  ;  self.log(ind=0)
        self.log(                  f'{a}{q}', ind=0, end='')  ;  [  self.log(f'{c%10}',                        ind=0, end='') for c in range(1, n+1) ]  ;  self.log(ind=0)
        if sep != '':  self.log(f'{a}{r}{b}', ind=0)

    def transposeData(self, data=None, why=' External  ', dbg=1):
        if data is None: data = self.data
        if dbg: self.log(f'(BGN) {why} {self.fmtDataDim(data)}')
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
        if dbg: self.log(f'(END) {why} {self.fmtDataDim(transposed)}')
        return transposed

    def dumpLabelText(self, t, d='%', why='', dbg=1):
        self.log(f'{why} len(t)={len(t)} len(t[0])={len(t[0])}')
        for j in range(len(t)):
            self.log(f'{t[j][0]:^3}', ind=0, end=' ')
        self.log(ind=0)
        for k in range(len(t)//10):
            for i in range(9): self.log(f'{" ":^3}', ind=0, end=' ')
            self.log(f' {d} ', ind=0, end=' ')
        self.log(ind=0)
        for j in range(len(t)):
            self.log(f'{t[j][1]:^3}', ind=0, end=' ')
        self.log(ind=0)
        if dbg:
            for i in range(len(t)):
                self.log(f'{i+1:5}', ind=0, end=' ')
                self.log(f' {t[i][0]:>5}', ind=0, end=' ')
                d2 = ' ' if i == 1 or (i + 1) % 10 else d
                self.log(f'{d2}{t[i][1]:>5}', ind=0, end=' ')
                self.log(ind=0)

    def createLabelText(self):
        self.labelTextA.extend(f'{j}' for j in range(1, self.n[C] + 1))
        self.labelTextB.extend(f'{j%10}' if j % 10 else f'{j // 10 % 10}' for j in range(1, self.n[C] + 1))
        self.log(f'labelTextA={fmtl(self.labelTextA)}', ind=0)
        self.log(f'labelTextB={fmtl(self.labelTextB)}', ind=0)
        texts = list(zip(self.labelTextA, self.labelTextB))
        self.log(f'texts={texts}', ind=0)
        self.dumpLabelText(texts)
    ####################################################################################################################################################################################################
    def geom(self, p=None, j=0, init=0, nn=0, dbg=VERBOSE):
        mx, my = -1, -1  ;  iw, ih = self.w[j], self.h[j]
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
#        self.log(FMTR.format('    geom      {}  {:3}  {:4}            {:7.2f} {:7.2f} {:7.2f} {:7.2f} {:5.3f} {:5.3f}  {:7.2f} {:7.2f} {}', j, n, i, x, y, w, h, mx, my, iw, ih, nn), ind=0)
#        self.log(FMTR.format(f'    geom      {j}  {n:3}  {i:4}            {x:7.2f} {y:7.2f} {w:7.2f} {h:7.2f} {mx:5.3f} {my:5.3f}  {iw:7.2f} {ih:7.2f} {nn}'), ind=0)
        self.log(f'    geom      {j}  {n:3}  {i:4}            {x:7.2f} {y:7.2f} {w:7.2f} {h:7.2f} {mx:5.3f} {my:5.3f}  {iw:7.2f} {ih:7.2f} {nn}', ind=0)
    ####################################################################################################################################################################################################
    def toggleTabs(self, tnik):
        self.log(f'(BGN) tnik={tnik} TNIK={fmtl(self.TNIK)} n={fmtl(self.n)} lenA={self.lenA()} lenB={self.lenB()}')
        if not self.TNIK[tnik] and not self.B[tnik]: self.showTabs(tnik)
        else:                                        self.hideTabs(tnik)
        self.TNIK[tnik] = not self.TNIK[tnik]   ;    self.n[S] = self.ss()
        self.log(f'calling on_resize() tnik={tnik} TNIK={fmtl(self.TNIK)} n={fmtl(self.n)} lenA={self.lenA()} lenB={self.lenB()}')
        self.on_resize(self.ww, self.hh)
        self.log(f'(END) tnik={tnik} TNIK={fmtl(self.TNIK)} n={fmtl(self.n)} lenA={self.lenA()} lenB={self.lenB()}')

    def hideTabs(self, tnik, dbg=VERBOSE):
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

    def showRLCols(self, dbg=VERBOSE):
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

    def hideRLCols(self, dbg=VERBOSE):
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
    def createLLRow(self, p, pi, dbg=VERBOSE, dbg2=0):
        nn = self.n[T] * self.ss() + 1  ;  klr = self.klr  ;  klc = self.klc  ;  kkr = self.cci(pi, klr)
        nr, ir, xr, yr, wr, hr, gr, mx, my = self.geom(p=p, j=S, nn=nn, dbg=dbg2)
        if SPRITES: xr += wr/2  ;  yr += hr/2
        self.J1[LLR] = 0
        self.J2[LLR] += 1
        row = self.createLabel(f'LR {pi+1}' if self.DF[LLR] else '', LLR, self.llRows, xr, yr, wr, hr, kkr, gr, why=f'New LR {pi+1}', kl=klr, dbg=dbg)
        nc, ic, xc, yc, wc, hc, gc, mx, my = self.geom(p=row, j=C, nn=self.n[C], dbg=dbg2)   ;  sc = nc * pi
        if dbg: self.log(f'nc={nc} pi={pi} sc={sc} len(llCols)={len(self.llCols)} llText={self.llText}')
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
        if dbg2: self.log(f'pi={pi:3} px={p.x:7.2f} py={p.y:7.2f} pw={p.width:7.2f} ph={p.height:7.2f}', ind=0)
        if dbg2: self.log(f'nr={nr:3} xr={xr:7.2f} yr={yr:7.2f} wr={wr:7.2f} hr={hr:7.2f}', ind=0)
        if dbg2: self.log(f'nc={nc:3} xc={xc:7.2f} yc={yc:7.2f} wc={wc:7.2f} hc={hc:7.2f}', ind=0)
        if   type(p) is pyglet.text.Label:    p.y -= hr/2  ;  p.height -= hr  # ;                      self.log(f'p.y -= hr/2, p.h -= hr: p.y = {p.y:7.2f} p.h = {p.height:7.2f}', ind=0)
        elif type(p) is pyglet.sprite.Sprite: my = (p.height - hr)/self.h[L]  ;   p.scale_y = my  # ;  self.log(f'p.y -= hr, my = (p.h-hr)/h[L]: h[L]={self.h[L]} my={my:7.5f} p.y={p.y:7.2f} p.h={p.height:7.2f}', ind=0)
        return p

    def resizeLLRow(self, p, pi, dbg=VERBOSE, dbg2=0):
        nn = self.n[T] * self.ss() + 1
        nr, ir, xr, yr, wr, hr, gr, mxr, myr = self.geom(p=p, j=S, nn=nn, dbg=dbg2)
        if SPRITES: xr += wr/2  ;  yr += hr/2
        self.J1[LLR] = 0
        self.J2[LLR] += 1
        row = self.llRows[pi]    ;    row.width = wr  ;   row.height = hr  ;   row.x = xr  ;   row.y = yr
        if dbg: self.dumpLabel(row, *self.ids(), *self.cnts(), why=f'resize LR {pi+1}')
        nc, ic, xc, yc, wc, hc, gc, mxc, myc = self.geom(p=row, j=C, dbg=dbg2)   ;  sc = nc * pi
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
        if dbg2: self.log(f'pi={pi:3} px={p.x:7.2f} py={p.y:7.2f} pw={p.width:7.2f} ph={p.height:7.2f}', ind=0)
        if dbg2: self.log(f'nr={nr:3} xr={xr:7.2f} yr={yr:7.2f} wr={wr:7.2f} hr={hr:7.2f}', ind=0)
        if dbg2: self.log(f'nc={nc:3} xc={xc:7.2f} yc={yc:7.2f} wc={wc:7.2f} hc={hc:7.2f}', ind=0)
        if   type(p) is pyglet.text.Label:    p.y -= hr/2  ;  p.height -= hr  # ;                               self.log(f'p.y -= hr/2, p.h -= hr: p.y = {p.y:7.2f} p.h = {p.height:7.2f}', ind=0)
        elif type(p) is pyglet.sprite.Sprite: my = (p.height - hr)/self.h[L]  ;   p.scale_y = my  # ;  self.log(f'p.y -= hr, my = (p.h-hr)/h[L]: h[L]={self.h[L]} my={my:7.5f} p.y={p.y:7.2f} p.h={p.height:7.2f}', ind=0)
        if dbg2: self.log(f'p.y -= hr/2, p.height -= hr: p.y = {p.y:7.2f} p.h = {p.height:7.2f}', ind=0)
        return p
    ####################################################################################################################################################################################################
    def createLabels(self, dbg=VERBOSE, dbg2=0):
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

    def g_createLabels(self, p, j, lablist, why='', dbg=VERBOSE, dbg2=0):
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
    def g_createLabels2(self, col, dbg=VERBOSE, dbg2=0):
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
    def createSprites(self, dbg=VERBOSE, dbg2=0):
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

    def g_createSprites(self, p, j, sprlist, v, why, dbg=VERBOSE, dbg2=0):
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
    def resizeLabels(self, dbg=VERBOSE):
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

    def g_resizeLabels(self, p, j, lablist, why, dbg=VERBOSE, dbg2=0):
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
    def g_resizeLabels2(self, col, dbg=VERBOSE, dbg2=0):
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
    def resizeSprites(self, dbg=VERBOSE):
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

    def g_resizeSprites(self, p, j, sprlist, why, dbg=VERBOSE, dbg2=0):
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
    def showLabel(self, i, p, j, t, g, k=None, v=1, dbg=VERBOSE):
        self.J1[j] = i  ;  self.J2[j] += 1
        why = f'New {t} {self.J2[j]}'
        text = f'{t} {self.J2[j]}' if self.DF[j] else t if j>C else ''
        if SPRITES and j < T: self.createSprite(p=p, x=0, y=0, w=self.w[j], h=self.h[j], kk=self.cci(i, k), g=g, why=why, kl=k, v=v, dbg=dbg)
        else:                 self.createLabel(text, j=j, p=p, x=0, y=0, w=0, h=0, kk=self.cci(i, k), g=g, why=why, kl=k, dbg=dbg)

    def hideLabel(self, p, j, t='???', dbg=VERBOSE): #        c = self.E[j][n]
        c = p[j]    ;    ha = hasattr(c, 'text')
        x, y, w, h = c.x, c.y, c.width, c.height
        text = c.text if ha else '??'
        if SPRITES: c.update(x=0, y=0, scale_x=0, scale_y=0)
        else:       c.x, c.y, c.width, c.height = 0, 0, 0, 0
        if dbg and SPRITES:     self.log(f'{t:5} {j+1:3} {hex(id(c))} {text:6} {x:7.2f} {y:7.2f} {w:7.2f} {h:7.2f} {c.text:6} {c.x:7.2f} {c.y:7.2f} {c.width:7.2f} {c.height:7.2f}', ind=0)
        if dbg and not SPRITES: self.log(f'{t:5} {j+1:3} {hex(id(c))} {text:6} {x:7.2f} {y:7.2f} {w:7.2f} {h:7.2f} {c.text:6} {c.x:7.2f} {c.y:7.2f} {c.width:7.2f} {c.height:7.2f}', ind=0)
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

    def dumpTabs(self, why='', dbg=VERBOSE):
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

    def dumpCols(self, why='', dbg=VERBOSE):
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

    def dumpLabels(self, why='', dbg=VERBOSE):
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
        if z is None: self.log(f' sid  lid p  l  s   c   t   n   i   k    x       y       w       h         id         mx    my   red grn blu opc   why       v     group       parent', ind=0); return
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
        ms = self.minSize()  ;  slope, off = 0.6, 3
        fs = fri(ms * slope + off)  ;  formula = '(fs = ms*slope+off)'
        self.log(f'{self.fmtWH()} {formula} ms={ms:4.1f} slope={slope} off={off} fs={fs:4.1f}={fri(fs):2}')
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
        text = f'{FONT_DPIS[fd]}dpi {fs}pt {FONT_NAMES[fn]} {FONT_COLORS[fc]}'
        self.log(f'{text}')
        return text

    def dumpFont(self, why=''):
        b, k, dpi, i, n, s = self.fontParams()
        pix = FONT_SCALE * s / dpi
#        self.log(f'{why} ki={k} di={dpi}={FONT_DPIS[dpi]}DPI {s}pt ni={n} {FONT_NAMES[n]} {FONT_SCALE}*{m}')
        self.log(f'({why}) {k} {dpi}DPI {s}pt {n} ({FONT_SCALE:6.3f}*{s}pt/{dpi}DPI)={pix:6.3f}pixels')

    def setFontParam(self, n, v, m):
        setattr(self, m, v)
        self.log(f'n={n} v={v:.1f} m={m}')
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
        return f'{self.kbk:8} {self.symb:8} {self.symbStr:14} {self.mods:2} {self.mods:16}'

    def on_key_release(self, symb, mods):
        self.symb, self.mods, self.symbStr, self.modsStr = symb, mods, pygwink.symbol_string(symb), pygwink.modifiers_string(mods)
        self.kbk = self.symbStr  # ;  kbk = self.kbk   ;   why='on_key_release'
        self.log(f'{self.kpEvntTxt()}')

    def on_key_press(self, symb, mods, dbg=0): # avoid these
        self.symb, self.mods, self.symbStr, self.modsStr = symb, mods, pygwink.symbol_string(symb), pygwink.modifiers_string(mods)
        self.kbk = self.symbStr  ;  kbk = self.kbk   ;   why='on_key_press'
        if dbg: self.log(f'(BGN) {self.kpEvntTxt()}')
        if                  self.isTab(kbk):                          self.updateTab(kbk, why)
        elif kbk == 'A' and self.isCtrl(mods) and self.isShift(mods): self.toggleVArrow()
        elif kbk == 'A' and self.isCtrl(mods):                        self.toggleHArrow()
        elif kbk == 'B' and self.isCtrl(mods) and self.isShift(mods): self.toggleBlank()
        elif kbk == 'B' and self.isCtrl(mods):                        self.toggleBlank()
        elif kbk == 'C' and self.isCtrl(mods) and self.isShift(mods): self.copyTabCols()
        elif kbk == 'C' and self.isCtrl(mods):                        self.copyTabCols()
        elif kbk == 'D' and self.isCtrl(mods) and self.isShift(mods): self.deleteTabCols()
        elif kbk == 'D' and self.isCtrl(mods):                        self.deleteTabCols()
        elif kbk == 'E' and self.isCtrl(mods) and self.isShift(mods): self.erase()
        elif kbk == 'E' and self.isCtrl(mods):                        self.erase()
        elif kbk == 'F' and self.isCtrl(mods) and self.isShift(mods): self.toggleFullScreen()
        elif kbk == 'F' and self.isCtrl(mods):                        self.toggleFullScreen()
        elif kbk == 'I' and self.isCtrl(mods) and self.isShift(mods): self.toggleCursorMode(why)
        elif kbk == 'I' and self.isCtrl(mods):                        self.toggleCursorMode(why)
        elif kbk == 'K' and self.isCtrl(mods) and self.isShift(mods): self.toggleTabs(KK)
        elif kbk == 'K' and self.isCtrl(mods):                        self.toggleTabs(KK)
        elif kbk == 'L' and self.isCtrl(mods) and self.isShift(mods): self.toggleLLRows()
        elif kbk == 'L' and self.isCtrl(mods):                        self.toggleLLRows()
        elif kbk == 'M' and self.isCtrl(mods) and self.isShift(mods): self.toggleRLCols()
        elif kbk == 'M' and self.isCtrl(mods):                        self.toggleRLCols()
        elif kbk == 'N' and self.isCtrl(mods) and self.isShift(mods): self.toggleTabs(NN)
        elif kbk == 'N' and self.isCtrl(mods):                        self.toggleTabs(NN)
        elif kbk == 'Q' and self.isCtrl(mods) and self.isShift(mods): self.quit(why)
        elif kbk == 'Q' and self.isCtrl(mods):                        self.quit(why)
        elif kbk == 'R' and self.isCtrl(mods) and self.isShift(mods): self.toggleChordName(rev=1)
        elif kbk == 'R' and self.isCtrl(mods):                        self.toggleChordName(rev=0)
        elif kbk == 'S' and self.isCtrl(mods) and self.isShift(mods): self.writeDataFile()
        elif kbk == 'S' and self.isCtrl(mods):                        self.writeDataFile()
        elif kbk == 'T' and self.isCtrl(mods) and self.isShift(mods): self.toggleTabs(TT)
        elif kbk == 'T' and self.isCtrl(mods):                        self.toggleTabs(TT)
        elif kbk == 'V' and self.isCtrl(mods) and self.isShift(mods): self.pasteTabCols()
        elif kbk == 'V' and self.isCtrl(mods):                        self.pasteTabCols()
        elif kbk == 'X' and self.isCtrl(mods) and self.isShift(mods): self.cutTabCols()
        elif kbk == 'X' and self.isCtrl(mods):                        self.cutTabCols()
        elif kbk == 'SPACE':                                          self.autoMove()
#        elif kbk == 'DELETE':                                         self.updateTab(self.tblank, 'DELETE')
#        elif kbk == 'BACKSPACE':                                      self.updateTab(self.tblank, 'BACKSPACE', backspace=1)
        elif kbk == 'TAB':                                            self.setCHVMode(MELODY, RIGHT, why='')
        elif kbk == 'TAB'       and self.isCtrl(mods):                self.setCHVMode(MELODY, LEFT,  why='TAB')
        elif kbk == 'ENTER':                                          self.setCHVMode(CHORD,  UP,    why='ENTER')
        elif kbk == 'ENTER'     and self.isCtrl(mods):                self.setCHVMode(CHORD,  DOWN,  why='ENTER')
        elif kbk == 'SLASH':                                          self.setCHVMode(ARPG,   RIGHT, UP,   'SLASH')
        elif kbk == 'SLASH'     and self.isCtrl(mods):                self.setCHVMode(ARPG,   LEFT,  DOWN, 'SLASH')
        elif kbk == 'BACKSLASH':                                      self.setCHVMode(ARPG,   RIGHT, DOWN, 'BACKSLASH')
        elif kbk == 'BACKSLASH' and self.isCtrl(mods):                self.setCHVMode(ARPG,   LEFT,  UP,   'BACKSLASH')
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
        else:   self.log(f'Unexpected {self.kpEvntTxt()}')
        if dbg: self.log(f'(END) {self.kpEvntTxt()}')

    def on_text(self, text, dbg=1): # use for entering strings not for motion
        self.kbk = text
        if dbg: self.log(f'(BGN) {self.kpEvntTxt()}')
        if self.isTab(self.kbk):                         self.updateTab(self.kbk, 'on_text')
        if self.kbk=='$' and self.isShift(self.mods):    self.snapshot()
        if dbg: self.log(f'(END) {self.kpEvntTxt()}')

    def on_text_motion(self, motion, dbg=1): # use for motion not strings
        self.kbk = motion   ;   p, l, s, c, t = self.j()  ;  np, nl, ns, nc, nt = self.n
        if dbg: self.log(f'(BGN) {self.kpEvntTxt()}')
        if self.mods == 0:
            if   motion == pygwink.MOTION_UP:                self.move(-1)
            elif motion == pygwink.MOTION_DOWN:              self.move( 1)
            elif motion == pygwink.MOTION_LEFT:              self.move(-nt)
            elif motion == pygwink.MOTION_RIGHT:             self.move( nt)
#            elif motion == pygwink.MOTION_PREVIOUS_WORD:     self.quit(f 'MOTION_PREVIOUS_WORD={pygwink.MOTION_PREVIOUS_WORD}')
#            elif motion == pygwink.MOTION_NEXT_WORD:         self.quit(f 'MOTION_NEXT_WORD={pygwink.MOTION_NEXT_WORD}')
            elif motion == pygwink.MOTION_BEGINNING_OF_LINE: self.move(-nt *  c)
            elif motion == pygwink.MOTION_END_OF_LINE:       self.move( nt * (nc - self.i[C]))
            elif motion == pygwink.MOTION_PREVIOUS_PAGE:     self.move(-nt *  nc)  # move up   one line to same tab
            elif motion == pygwink.MOTION_NEXT_PAGE:         self.move( nt *  nc)  # move down one line to same tab
#            elif motion == pygwink.MOTION_BEGINNING_OF_FILE: self.quit(f 'MOTION_BEGINNING_OF_FILE={pygwink.MOTION_BEGINNING_OF_FILE}')
#            elif motion == pygwink.MOTION_END_OF_FILE:       self.quit(f 'MOTION_END_OF_FILE={pygwink.MOTION_END_OF_FILE}')
            elif motion == pygwink.MOTION_BACKSPACE:         self.updateTab(self.tblank, 'BACKSPACE', rev=1)
            elif motion == pygwink.MOTION_DELETE:            self.updateTab(self.tblank, 'DELETE')
            else:                                            self.log(f'motion={motion} ???')
        elif self.isAlt(self.mods):
            if   motion == pygwink.MOTION_UP:                self.moveUp()
            elif motion == pygwink.MOTION_DOWN:              self.moveDown()
            elif motion == pygwink.MOTION_LEFT:              self.moveLeft()
            elif motion == pygwink.MOTION_RIGHT:             self.moveRight()
            elif motion == pygwink.MOTION_BEGINNING_OF_LINE: self.move(-nt *  c)
            elif motion == pygwink.MOTION_END_OF_LINE:       self.move( nt * (nc - self.i[C]))
            elif motion == pygwink.MOTION_PREVIOUS_PAGE:     self.move(self.cc2(p, 0,    c, 0))     # move up   to top    tab on top    line
            elif motion == pygwink.MOTION_NEXT_PAGE:         self.move(self.cc2(p, nl-1, c, nt-1))  # move down to bottom tab on bottom line
            else:                                            self.log(f'motion={motion} ??? ALT')
        elif self.isCtrl(self.mods):
            if   motion == pygwink.MOTION_PREVIOUS_WORD:     self.selectTabCol(-nt, 'CTRL LEFT')
            elif motion == pygwink.MOTION_NEXT_WORD:         self.selectTabCol( nt, 'CTRL RIGHT')
#            elif motion == pygwink.MOTION_BEGINNING_OF_LINE: self.quit('CTRL + MOTION_BEGINNING_OF_LINE')
#            elif motion == pygwink.MOTION_END_OF_LINE:       self.quit('CTRL + MOTION_END_OF_LINE')
            elif motion == pygwink.MOTION_BEGINNING_OF_FILE: self.log(f'CTRL + MOTION_BEGINNING_OF_FILE={pygwink.MOTION_BEGINNING_OF_FILE}=CTRL HOME')
            elif motion == pygwink.MOTION_END_OF_FILE:       self.log(f'CTRL + MOTION_END_OF_FILE={pygwink.MOTION_END_OF_FILE}=CTRL END')
            else:                                            self.log(f'motion={motion} ??? CTRL')
        if dbg: self.log(f'(END) {self.kpEvntTxt()}')
    ####################################################################################################################################################################################################
    def createCursor(self, g):
        self.cc = self.cursorCol()
        c = self.tabs[self.cc]
        w, h = c.width, c.height
        x, y = c.x - w/2, c.y - h/2
        self.log(f'c={self.cc} x={x:6.1f} y={y:6.1f} w={w:6.1f} h={h:6.1f} i={fmtl(self.i, FMTN)}')
        self.dumpSprite()
        self.cursor = self.createSprite(None, x, y, w, h, 0, g, why='cursor', kl=CCS, v=1, dbg=1)

    def resizeCursor(self):
        cc = self.cursorCol()
        c = self.tabs[cc]
        w, h = c.width, c.height  ;  x, y = c.x - w/2, c.y - h/2
        self.log(f'c={cc} x={x:6.1f} y={y:6.1f} w={w:6.1f} h={h:6.1f} i={fmtl(self.i, FMTN)}')
        self.cursor.update(x=x, y=y, scale_x=w/self.w[T], scale_y=h/self.h[T])

    def cursorCol(self, dbg=VERBOSE):
        p, l, s, c, t = self.j()
        return self.plct2cc(p, l, c, t, dbg)

    def plct2cc(self, p, l, c, t, dbg=VERBOSE):
        tpp, tpl, tps, tpc = self.tpz()
        cc = p * tpp + l * tpl + c * tpc + t
        lenT = len(self.tabs)   ;   ccm = cc % lenT
        if dbg: self.log(f' cc: p={p} l={l} c={c} t={t}', ind=0, end='')
        if dbg: self.log(f' tpp={tpp} tpl={tpl} tpc={tpc}', ind=0, end='')
        if dbg: self.log(f' cc={cc} = ( {p*tpp} + {l*tpl} + {c*tpc} + {t} )', ind=0, end='')
        if dbg : self.log(f' cc = cc % len(tabs) = {cc} % {lenT} = {ccm} = cc', ind=0)
        return ccm

    def cc2plct(self, cc, dbg=VERBOSE):
        tpp, tpl, tps, tpc = self.tpz()
        p =  cc // tpp
        l = (cc - p * tpp) // tpl
        c = (cc - p * tpp - l * tpl) // tpc
        t =  cc - p * tpp - l * tpl - c * tpc
        p = p % self.n[P]
        if dbg: self.log(f'cc={cc} p={p} l={l} c={c} t={t}')
        return p, l, c, t

    def cc2(self, p, l, c, t, dbg=1):
        cc = self.plct2cc(p, l, c, t, dbg)
        return cc - self.cursorCol()
    ####################################################################################################################################################################################################
    def on_mouse_release(self, x, y, button, modifiers, dbg=VERBOSE):
        np, nl, ns, nc, nt = self.n   ;  nc += CCC   ;  nt += QQ        ;  y0 = y
        y = self.hh - y      ;   w = self.ww/nc      ;  h  = self.hh/(nl*ns*nt)
        c  = int(x/w) - CCC  ;  r0 = int(y/h) - QQ   ;  d0 = int(ns*nt)
        l = int(r0/d0)       ;   r = int(r0 % d0)    ;   s = int(r/d0)  ;  p = 0  ;  t = r
        kk = int(p * self.tpp + l * self.tpl + s * self.tps + c * self.tpc + t)
        if dbg: self.log(f'(BGN) x={x} y0={y0:4} w={w:6.2f} h={h:6.2f}', file=sys.stdout)
        if dbg: self.log(f'y={y:4} r0={r0:4} d0={d0} r={r}', file=sys.stdout)
        if dbg: self.log(f'p={p} l={l} s={s} c={c} t={t} kk={kk}', file=sys.stdout)
        if dbg: self.log(f'tabs[kk].txt={self.tabs[kk].text}', file=sys.stdout)
        k  = kk - self.cc
        if dbg: self.log(f'      {k:4} {kk:4} {self.cc:4} {fmtl(self.i, FMTN)} b={button} m={modifiers} txt={self.tabs[self.cc].text}', file=sys.stdout)
        if dbg: self.move(k)
        if dbg: self.log(f'      {k:4} {kk:4} {self.cc:4} {fmtl(self.i, FMTN)} b={button} m={modifiers} txt={self.tabs[self.cc].text}', file=sys.stdout)

    def moveUp(self):
        p, l, s, c, t = self.j()  ; nt = self.n[T] - 1
        if t: self.move(self.cc2(p, l,    c, 0))   # move up   to top    tab on same line
        else: self.move(self.cc2(p, l-1,  c, nt))  # move up   one line to bottom tab
    def moveDown(self):
        p, l, s, c, t = self.j()  ;  nt = self.n[T] - 1
        if t < nt: self.move(self.cc2(p, l,    c, nt))  # move down to bottom tab on same line
        else:      self.move(self.cc2(p, l+1,  c, 0))   # move down one line to top tab
    def moveLeft(self):
        p, l, s, c, t = self.j()  ;  nc = self.n[C] - 1
        if c: self.move(self.cc2(p, l,   0,  t))
        else: self.move(self.cc2(p, l-1, nc, t))
    def moveRight(self):
        p, l, s, c, t = self.j()  ;  nc = self.n[C] - 1
        if c < nc: self.move(self.cc2(p, l,  nc, t))
        else:      self.move(self.cc2(p, l+1, 0, t))

    def move(self, k, dbg=1):
        if dbg: self.log(f'(BGN) {k:4}      {self.cc:4} {fmtl(self.i, FMTN)} text={self.tabs[self.cc].text}', file=sys.stdout)
        if not self.SNAP0: t = self.tabs[self.cc]  ;  self.snapshot(f'pre-move() k={k:4} kk={self.cc:3} {fmtl(self.i, FMTN)} text={t.text} {t.x:6.2f} {t.y:6.2f}')  ;  self.SNAP0 = 1
        self._move(k)
        kk = self.cursorCol()
        t = self.tabs[kk]  ;  x = t.x - t.width/2  ;  y = t.y - t.height/2
        self.cc = kk
        self.cursor.update(x=x, y=y)
        if dbg: self.log(f'(END) {k:4} {kk:4} {self.cc:4} {fmtl(self.i, FMTN)} text={self.tabs[self.cc].text} {x:6.2f} {y:6.2f}', file=sys.stdout)
        self.armSnap = f'move() k={k:4} kk={kk:4} {fmtl(self.i, FMTN)} text={self.tabs[self.cc].text} {x:6.2f} {y:6.2f}'

    def _move(self, k, dbg=1):
        np, nl, ns, nc, nt = self.n
        p,  l,  s,  c,  t = self.j()
        jt = t + k
        if dbg: self.log(f'(BGN) {k:4}      {self.cc:4} {fmtl(self.i, FMTN)} nt={nt}', file=sys.stdout)
        self.i[T] = jt %  nt + 1
        jc   =  c + jt // nt
        self.i[C] = jc %  nc + 1
        jl   =  l + jc // nc
        self.i[L] = jl %  nl + 1
        jp   =  p + jl // nl
        ip0  = self.i[P]
        self.i[P] = jp %  np + 1
        if dbg: self.log(f'(END) {k:4}      {self.cc:4} {fmtl(self.i, FMTN)} ip0={ip0} jp={jp} jl={jl} jc={jc} jt={jt}', file=sys.stdout)

    def autoMove(self, dbg=1):
        self.log('(BGN)')
        ha = 1 if self.hArrow else -1
        va = 1 if self.vArrow else -1
        nt, it = self.n[T], self.i[T]
        mmDist = ha * nt
        cmDist = va
        amDist = mmDist + cmDist
        if dbg: self.dumpCursorArrows(f'M={mmDist} C={cmDist} A={amDist}')
        if      self.csrMode == MELODY:            self.move(mmDist)
        elif    self.csrMode == CHORD:
            if  it == 1 and self.vArrow  == UP and self.hArrow == RIGHT: self.move(nt*2-1)
            else:                                  self.move(cmDist)
        elif    self.csrMode == ARPG:              self.move(amDist)
        self.log('(END)')

    '''
    def nextPage(self, i, motion):
        self.pages[i].visible = False
        self.updatePage(i+1, f'{motion}=MOTION_NEXT_PAGE')

    def prevPage(self, i, motion):
        self.pages[i].visible = False
        self.updatePage(i-1, f'{motion}=MOTION_PREVIOUS_PAGE')

    def updatePage(self, i, why):
        i = i % self.n[P]
        self.pages[i].visible = True
        self.log(f'{why} i[{P}]={i}')
        self.i[P] = i
    '''
    def updateCaption(self, txt): self.set_caption(txt)
    ####################################################################################################################################################################################################
    def selectTabCol(self, m, why='', dbg=1):
        cc = self.cursorCol()  ;  nt = self.n[T]  ;  text = ''
        sc = (cc // nt) * nt
        self.skeys.append(sc)
        self.log(f'(BGN) {why} m={m} cc={cc} sc={sc} skeys<{len(self.skeys)}>={fmtl(self.skeys)}')
        for t in range(nt):
            tab   = self.tabs[sc + t]    ;  old = tab.color  ;  tab.color = CCS[1]
            note  = self.notes[sc + t]   ;                     note.color = CCS[1]
            chord = self.chords[sc + t]  ;                    chord.color = CCS[1]
            if dbg and not t: self.dumpWBWAW(f'cc={cc} sc={sc} t={t}', fmtl(old), f'<tabs[{sc+t}].color>', fmtl(tab.color))
            text += tab.text
        self.smap[sc] = text
        self.move(m)
        self.log(f'(END) {why} m={m} cc={cc} sc={sc} smap<{len(self.smap)}>={fmtd(self.smap)}')

    def copyTabCols(self, dbg=0, dbg2=1):
        self.log(f'(BGN) skeys<{len(self.skeys)}>={self.skeys}')   ;   nt = self.n[T]  ;   text = ''
        for k in range(len(self.skeys)):
            for t in range(nt):
                kv     = self.skeys [k]   ;   kt = kv + t
                tab    = self.tabs  [kt]  ;  old = tab.color  ;  tab.color = self.k[T][0]
                note   = self.notes [kt]  ;                     note.color = self.k[N][0]
                chord  = self.chords[kt]  ;                    chord.color = self.k[K][0]
                if dbg2 and not t: self.dumpWBWAW(f'k={k} t={t} kv={kv} kt={kt}', fmtl(old), f'<tabs[{kt}].color>', fmtl(tab.color))
                if dbg: text += tab.text
            if dbg: text += ' '
        self.log(f'(END) skeys<{len(self.skeys)}>={self.skeys}', end=' ' if dbg else '\n')
        if dbg: self.log(f'text={text}', ind=0)
    ####################################################################################################################################################################################################
    def cutTabCols(self): self.log('(BGN) Cut = Copy + Delete?')  ;  self.copyTabCols()  ;  self.log('Cut = Copy + Delete?')  ;  self.deleteTabCols(cut=1)  ;  self.log('(END) Cut = Copy + Delete?')
    ####################################################################################################################################################################################################
    def deleteTabCols(self, cut=0):
        self.log(f'(BGN) cut={cut} skeys<{len(self.skeys)}>={fmtl(self.skeys)} smap<{len(self.smap)}>={fmtd(self.smap)}')
        nt = self.n[T]
        for i, (k,v) in enumerate(self.smap.items()):
            self.log(f'i={i} k={k} v={v}')
            for t in range(nt):
                p, l, c, r = self.cc2plct(k + t, dbg=0)   ;   kt = k + t
                self.tabs  [kt].color = self.k[T][0]
                self.notes [kt].color = self.k[N][0]
                self.chords[kt].color = self.k[K][0]
                self.updateDTNK(self.tblank, kt, p, l, c, t, uk=1 if t == nt-1 else 0)
        if not cut: self.smap.clear()  ;  self.skeys.clear()
        self.log(f'(END) cut={cut} skeys<{len(self.skeys)}>={fmtl(self.skeys)} smap<{len(self.smap)}>={fmtd(self.smap)}')

    def pasteTabCols(self, dbg=1):
        cc = self.cursorCol()  ;  nt = self.n[T]
        nc = (cc // nt) * nt   ;  sc = 0
        smap, skeys = self.smap, self.skeys
        p, l, s, c, r = self.j()
        self.log(f'(BGN) p={p} l={l} c={c} r={r} cc={cc} nc={nc} skeys<{len(skeys)}>={fmtl(skeys)} smap<{len(smap)}>={fmtd(smap)}')
        for i, (k, v) in enumerate(smap.items()):
            text = smap[k]
            dk = 0 if not i else skeys[i] - skeys[0]
            if dbg: self.log(f'i={i} k={k} v={v} text={text} dk={dk}')
            for t in range(nt):
                sc = (nc + dk + t) % self.tpp
                p, l, c, r = self.cc2plct(sc, dbg=0)
                self.updateDTNK(text[t], sc, p, l, c, t, uk=1 if t == nt-1 else 0)
            if dbg: self.log(f'sm[{k}]={text} sc={sc}')
        self.smap.clear()  ;  self.skeys.clear()
        self.log(f'(END) cc={cc} nc={nc} skeys<{len(skeys)}>={fmtl(skeys)} smap<{len(smap)}>={fmtd(smap)}')

    def updateTab(self, text, why='', rev=0, dbg=1):
        self.log(f'(BGN) text={text} rev={rev} {why} {fmtl(self.i, FMTN)}')
        if rev: self.reverseArrow()    ;    self.autoMove()
        cc = self.cursorCol()          ;    p, l, s, c, t = self.j()
        self.updateDTNK(text, cc, p, l, c, t, uk=1)
        if rev: self.reverseArrow()
        else:   self.autoMove()
        if dbg: self.snapshot()
        self.log(f'(END) text={text} rev={rev} {why} {fmtl(self.i, FMTN)}')
    ####################################################################################################################################################################################################
    def updateDTNK(self, text, cc, p, l, c, t, uk=0, dbg=1):
        if dbg: self.log(f'(BGN) text={text} cc={cc} p={p} l={l} c={c} t={t} uk={uk}')
        self.updateData(text, p, l, c, t)
        if self.TNIK[TT]:        self.updateTab2( text, cc)
        if self.TNIK[NN]:        self.updateNote( text, cc, t)
        if self.TNIK[KK] and uk: self.updateChord(p, l, c, t)
        if dbg: self.log(f'(END) text={text} cc={cc} p={p} l={l} c={c} t={t} uk={uk}')
    ####################################################################################################################################################################################################
    def updateData(self, text, p, l, c, r, dbg=1):
        t = self.data[p][l][c]
        self.data[p][l][c] = t[0:r] + text + t[r+1:]
        if dbg: self.dumpWBWAW(f'({text} {p} {l} {c} {r})', t, f'<data[{p}][{l}][{c}]>', self.data[p][l][c])

    def updateTab2(self, txt, cc, dbg=1):
        oldTxt = self.tabs[cc].text
        self.tabs[cc].text = txt
        if dbg: self.dumpWBWAW(f'({txt} cc={cc})', oldTxt, f'<tabs[{cc}].text>', self.tabs[cc].text)

    def updateNote(self, txt, cc, r, dbg=1):
        oldNote = self.notes[cc].text
        self.notes[cc].text = self.getNote(r, txt).name if self.isFret(txt) else self.nblank
        if dbg: self.dumpWBWAW(f'({txt} cc={cc} r={r})', oldNote, f'<notes[{cc}].text>', self.notes[cc].text)

    def updateChord(self, p, l, c, t, dbg=1, dbg2=1):
        cc = self.plct2cc(p, l, c, 0)    ;    nt = self.n[T]    ;    name = ''    ;    i = 0
        if dbg: self.log(f'(BGN) p={p} l={l} c={c} t={t} cc={cc}')
        chordName = self.cobj.getChordName(p, l, c, dbg=1)
        if dbg2: self.log(f' chordName=<{chordName:<6}>')
        self.updateChordName(chordName, cc)
        if dbg:
            for i in range(nt):
                name += self.chords[cc + i].text
            self.log(f'(END) chords[{cc}-{cc+i}].text={name}')
        else: self.log(f'(END) chordName={chordName}')

    def updateChordName(self, name, cc, dbg=1):
        if dbg: self.log(f'(BGN) name={name} cc={cc}')
        for r in range(self.n[T]):
            self.chords[cc + r].text = name[r] if len(name) > r else ' '
            if dbg: self.log(f'chords[{cc + r}].text={self.chords[cc + r].text}')
        self.log(f'(END) name={name} cc={cc}')

    def dumpWBWAW(self, why, before, what, after, why2=''): self.log(f'{why:<24} {before:>16} {what:^20} {after:<16} {why2}')
    ####################################################################################################################################################################################################
    def dumpCursorArrows(self, why=''): cm, ha, va = self.csrMode, self.hArrow, self.vArrow  ;   self.log(f'csrMode={cm}={CSR_MODES[cm]:6} hArrow={ha}={HARROWS[ha]:5} vArrow={va}={VARROWS[va]:4} {why}')
    def reverseArrow(self, dbg=1):
        if dbg: self.dumpCursorArrows('reverseArrow()')
        if self.csrMode == MELODY or self.csrMode == ARPG: self.toggleHArrow('reverseArrow() MELODY or ARPG')
        if self.csrMode == CHORD  or self.csrMode == ARPG: self.toggleVArrow('reverseArrow() CHORD or ARPG')
        if dbg: self.dumpCursorArrows('reverseArrow()')
    ####################################################################################################################################################################################################
    def toggleChordName(self, rev=0):
        p, l, s, c, r = self.j()
        cc = c + l * self.n[C] # fix
        self.log(f'(BGN) len={len(self.cobj.mlimap[cc])} p={p} l={l} c={c} r={r} cc={cc} rev={rev} {self.cobj.mlimap[cc]}')
        chordName = self.cobj.toggleChordName(rev)
        cc2 = self.cursorCol()
        self.updateChordName(chordName, cc2)
        self.log(f'(END) len={len(self.cobj.mlimap[cc])} p={p} l={l} c={c} r={r} cc={cc} cc2={cc2} rev={rev} {self.cobj.mlimap[cc]}')

    def setCHVMode(self, c=None, h=None, v=None, why=''):
        self.dumpCursorArrows(f'setCHVMode() c={c} h={h} v={v} why={why}')
        if c is not None: self.csrMode = c
        if h is not None: self.hArrow  = h
        if v is not None: self.vArrow  = v
        self.dumpCursorArrows(f'setCHVMode() c={c} h={h} v={v} why={why}')

    def toggleCursorMode(self, why=''):
        self.log(f'(BGN) csrMode={self.csrMode}={CSR_MODES[self.csrMode]} {why}')
        self.csrMode  = (self.csrMode + 1) % len(CSR_MODES)
        self.log(f'(END) csrMode={self.csrMode}={CSR_MODES[self.csrMode]} {why}')

    def toggleHArrow(self, why=''):
        self.log(f'(BGN) hArrow={self.hArrow}={HARROWS[self.hArrow]} {why}')
        self.hArrow  = (self.hArrow + 1) % len(HARROWS)
        self.log(f'(END) hArrow={self.hArrow}={HARROWS[self.hArrow]} {why}')

    def toggleVArrow(self, why=''):
        self.log(f'(BGN) vArrow={self.vArrow}={VARROWS[self.vArrow]} {why}')
        self.vArrow  = (self.vArrow + 1) % len(VARROWS)
        self.log(f'(END) vArrow={self.vArrow}={VARROWS[self.vArrow]} {why}')

    def toggleFullScreen(self):
        global FULL_SCREEN
        FULL_SCREEN =  not  FULL_SCREEN
        self.set_fullscreen(FULL_SCREEN)
        self.log(f'FULL_SCREEN={FULL_SCREEN}')

    def toggleBlank(self):
        prevBlank    =  self.tblank
        self.log('(BGN)')
        self.tblanki = (self.tblanki + 1) % len(self.tblanks)
        self.tblank  =  self.tblanks[self.tblanki]
        self.swapTabs(prevBlank,     self.tblank)
        self.log('(END)')

    def swapTabs(self, src, trg, data=None):
        if data is None: data = self.data
        self.log(f'(BGN) replace({src},{trg})')
        np, nl, ns, nr, nc = self.n  ;  nc += CCC
        for i in range(len(self.tabs)):
            self.tabs[i].text  = self.tabs[i].text.replace(src, trg)
            self.notes[i].text = self.notes[i].text.replace(src, trg)
        for p in range(np):
            for l in range(nl):
                for c in range(nc):
                    self.log(f'before data[{p}][{l}][{c}]={data[p][l][c]}')
                    data[p][l][c] = data[p][l][c].replace(src, trg)
                    self.log(f'after  data[{p}][{l}][{c}]={data[p][l][c]}')
        self.log(f'(END) replace({src},{trg})')
    ####################################################################################################################################################################################################
    def erase(self, reset=0):
        np, nl, ns, nr, nc = self.n  ;  nc += CCC
        self.log(f'(BGN) np={np} nl={nl} ns={ns} nr={nr} nc={nc}')
        for i in range(len(self.tabs)):
            self.tabs  [i].text = self.tblank
            self.notes [i].text = self.nblank
            self.chords[i].text = self.nblank
        for p in range(np):
            for l in range(nl):
                for c in range(nc):
                    self.data[p][l][c] = self.tblankCol
        if reset:
            self.log(f'reset={reset} CCC={CCC}')
            if CCC:     self.setStringNumbs()  ;  self.setStringNames()
            if CCC > 1: self.setCapo()
        self.log(f'(END) np={np} nl={nl} nr={nr} nc={nc}')
    '''
    def setStringNumbs(self):
        np, nl, ns, nr, nc = self.n  ;  nc += CCC  ;  i = C1
        for p in range(np):
            for l in range(nl):
                self.data[p][l][C1] = self.stringNumbs
                self.log(f'p={p} l={l} c={c} data[p][l][c]={self.data[p][l][C1]}')
                for r in range(nr):
                    self.tabs[i].text  = self.stringNumbs[r]
                    self.log(f'({r} {i} {self.tabs[i].text}) ', ind=0, end='')
                    i += nc
                self.log(ind=0)

    def setStringNames(self):
        np, nl, ns, nr, nc = self.n  ;  nc += CCC  ;  i = C1
        for p in range(np):
            for l in range(nl):
                self.data[p][l][C1] = self.stringNames
                self.log(f'p={p} l={l} c={C1} data[p][l]={self.data[p][l][C1]}')
                for r in range(nr):
                    self.notes[i].text = self.stringNames[r]
                    self.log(f'({r} {i} {self.notes[i].text}) ', ind=0, end='')
                    i += nc
                self.log(ind=0)

    def setCapo(self):
        np, nl, ns, nr, nc = self.n  ;  nc += CCC  ;  i = C2
        for p in range(np):
            for l in range(nl):
                self.data[p][l][C2] = self.stringCapo
                self.log(f'p={p} l={l} c={C2} data[p][l]={self.data[p][l][C2]}')
                for r in range(nr):
                    self.tabs[i].text  = self.stringCapo[r]
                    self.notes[i].text = self.stringCapo[r]
                    self.log(f'({r} {i} {self.tabs[i].text} {self.notes[i].text}) ', ind=0, end='')
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
        if dbg: Tabs.log(f'tab={tab} fretNum={fretNum}')
        return fretNum

    def getNoteIndex(self, r, fn, dbg=0):
        row = self.n[T] - r - 1    # Reverse and zero base the string numbering: str[1 ... numStrings] => s[(numStrings - 1) ... 0]
        if dbg: self.log(f'r={r} fretNum={fn} row={row} stringMap={fmtd(self.stringMap)}')
        k = self.stringKeys[row]
        i = self.stringMap[k] + fn
        if dbg: self.log(f'r={r} fretNum={fn} row={row} k={k} i={i}')
        return i

    def getNote(self, row, tab, dbg=0):
        fretNum = self.getFretNum(tab)
        note = misc.Note(self.getNoteIndex(row, fretNum))
        if dbg: self.log(f'row={row} tab={tab} fretNum={fretNum} note.name={note.name} note.index={note.index}')
        return note
    ####################################################################################################################################################################################################
    def cci(self, c, cc, dbg=0):
        if c == 0: self.ci = (self.ci + 1) % len(cc)
        k = (c + self.ci) % len(cc)
        if dbg: self.log(f'c={c} cc={cc} ci={self.ci} k={k}')
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
        if dbg: self.log(f'SFX={SFX} SNAP_DIR={SNAP_DIR} SNAP_SFX={SNAP_SFX} baseName={BASE_NAME} basePath={BASE_PATH}')
        SNAP_ID   = f'.{self.ssi}'
        SNAP_NAME = BASE_NAME + SFX + SNAP_ID + SNAP_SFX
        SNAP_PATH = BASE_PATH / SNAP_DIR / SNAP_NAME
        pyglet.image.get_buffer_manager().get_color_buffer().save(f'{SNAP_PATH}')
        if dbg: self.log(f'SNAP_ID={SNAP_ID} SNAP_NAME={SNAP_NAME,} SNAP_PATH={SNAP_PATH}')
        if dbg2: self.log(f'{SNAP_NAME} {why}', file=sys.stdout)
        self.ssi += 1

    def dumpStack(self, si):
        for i, e in enumerate(si):
            fp = pathlib.Path(e.filename)  ;   n = fp.stem  ;  l = e.lineno  ;  f = e.function  ;  c = e.code_context[0].strip()  ;  j = len(si) - (i + 1)
            self.log(f'{j:2} {n:9} {l:5} {f:20} {c}')
        self.log(f'MAX_STACK_DEPTH={MAX_STACK_DEPTH:2}')

    @staticmethod
    def indent(): d = Tabs.stackDepth() - 4;  return f'{d:{d}}'

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
        Tabs.log(f'deleting {len(g)} file globs why={why}')
        for f in g:
            Tabs.log(f'{f}')
            os.system(f'del {f}')
    @staticmethod
    def getLogPath(seq=0, logdir='logs', logsfx='.log'):
        if seq:
            subDir     = '/' + SFX.lstrip('.')
            logdir     = logdir + subDir
            Tabs.log(f'logdir      = {logdir}')
            pathlib.Path(logdir).mkdir(parents=True, exist_ok=True)
            logGlobArg = str(BASE_PATH / logdir / BASE_NAME) + SFX + '.*' + logsfx
            logGlob    = glob.glob(logGlobArg)
            seq        = 1 + Tabs.getLogId(logGlob, logsfx)
            logsfx     = f'.{seq}{logsfx}'
            Tabs.log(f'logGlobArg  = {logGlobArg}')
            Tabs.log('logGlob:')
            Tabs.log(f'{fmtl(logGlob)}', ind=0)
            Tabs.log(f'seq num     = {seq}')
        logName        = BASE_NAME + SFX + logsfx
        logPath        = BASE_PATH / logdir / logName
        Tabs.log(f'logPath     = {logPath}') if seq else Tabs.log(f'logPath     = {logPath}')
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
            if dbg: Tabs.log(f'ids={ids}')
            i = max(ids)
        return i

    @staticmethod
    def log(msg='', ind=1, file=None, flush=False, sep=',', end='\n'):
        if not file: file = LOG_FILE
        si = inspect.stack(0)[1]
        p = pathlib.Path(si.filename)  ;        n = p.name  ;        l = si.lineno  ;        f = si.function  ;        t = ''
        if f in Tabs.hideST: si = inspect.stack(0)[2];  p = pathlib.Path(si.filename);  n = p.name;  l = si.lineno;  f = si.function;  t = ''
        if ind: print(f'{Tabs.indent():20} {l:5} {n:7} {t} {f:>20} ', file=file, end='')
        print(f'{msg}', file=file, flush=flush, sep=sep, end=end) if ind else print(f'{msg}', file=file, flush=flush, sep=sep, end=end)
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
        self.log(f'SEQ_LOG_FILES = {SEQ_LOG_FILES}')
        logPath = None
        if SEQ_LOG_FILES:
            logPath = self.getLogPath(SEQ_LOG_FILES)
            self.log(f'LOG_PATH    = {LOG_PATH}')
            self.log(f'logPath     = {logPath}')
            self.log(f'copy {LOG_PATH} {logPath}')
        self.log(f'(END) closing LOG_FILE={LOG_FILE.name}')
        LOG_FILE.close()
        if SEQ_LOG_FILES and logPath: os.system(f'copy {LOG_PATH} {logPath}')
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
