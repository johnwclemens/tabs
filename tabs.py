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
def fmtl(lst, w=None, u='<', d1='[', d2=']', sep=' ', ll=0, z=''):
#    Tabs.log(f'{type(lst)}')
    assert type(lst) in (list, tuple, set, frozenset)  #
    if w is None: w = 0
    t = ''   ;   s = f'<{len(lst)}' if ll else ''
    for i, l in enumerate(lst):
        if type(l) in (list, tuple, set):
#            d0 = sep + d1 if not i else d1    ;    d3 = d2 + sep
            if type(w) in (list, tuple, set):       t += fmtl(l, w[i], u, d1, d2, sep, ll, z)
            else:                                   t += fmtl(l, w,    u, d1, d2, sep, ll, z)
        else:
            ss = sep if i < len(lst)-1 else ''
            if type(w) in (list, tuple, set):       t += f'{l:{u}{w[i]}{z}}{ss}'
            else:                                   t += f'{l:{u}{w   }{z}}{ss}'
    return s + d1 + t + d2
def fmtm(m, w=1, d0=':', d1='[', d2=']'):
    t = ''
    for k, v in m.items():
        if   type(v) in (list, tuple, set):         t += f'{k}{d0}'   ;   t += fmtl(v, w)
        elif type(v) in (int, str):                 t += f'{k:>{w}}{d0}{v:<{w}} '
    return d1 + t.rstrip() + d2

def getFilePath(filedir='files', filesfx='.txt', dbg=0):
    sfx = SFX if not ARGS['f'] else ''
    if dbg: Tabs.log(f'BASE_NAME= {BASE_NAME} SFX={SFX}')
    fileName        = BASE_NAME + sfx + filesfx
    filePath        = BASE_PATH / filedir / fileName
    if dbg: Tabs.log(f'fileName  = {fileName} filePath={filePath}')
    return filePath

def dumpGlobals():
    Tabs.log(f'argv      = {fmtl(sys.argv, ll=1)}')
    Tabs.log(f'ARGS      = {fmtm(ARGS)}')
    Tabs.log(f'PATH      = {PATH}')
    Tabs.log(f'BASE_PATH = {BASE_PATH}')
    Tabs.log(f'BASE_NAME = {BASE_NAME}')
    Tabs.log(f'SFX       = {SFX}')
####################################################################################################################################################################################################
ARGS             = cmdArgs.parseCmdLine()
AUTO_SAVE = 1  ;  CHECKER_BOARD = 0  ;  EVENT_LOG = 0  ;  FULL_SCREEN = 1  ;  ORDER_GROUP = 1  ;  RESIZE = 1  ;  SEQ_LOG_FILES = 1  ;  SUBPIX = 1  ;  VERBOSE = 0  ;  CAT = 0
VRSN1            = 1  ;  SFX1 = chr(65 + VRSN1)  ;  QQ      = VRSN1  ;  VRSNX1 = f'VRSN1={VRSN1}       QQ={QQ     }  SFX1={SFX1}'
VRSN2            = 0  ;  SFX2 = chr(49 + VRSN2)  ;  SPRITES = VRSN2  ;  VRSNX2 = f'VRSN2={VRSN2}  SPRITES={SPRITES}  SFX2={SFX2}'
VRSN3            = 2  ;  SFX3 = chr(97 + VRSN3)  ;  CCC     = VRSN3  ;  VRSNX3 = f'VRSN3={VRSN3}      CCC={CCC    }  SFX3={SFX3}'
SFX              = f'.{SFX1}.{SFX2}.{SFX3}' if not ARGS['f'] else ''
PATH             = pathlib.Path.cwd() / sys.argv[0]
BASE_PATH        = PATH.parent
BASE_NAME        = BASE_PATH.stem
SNAP_DIR         = 'snaps'
SNAP_SFX         = '.png'
LOG_FILE         = None
FMTN             = (1, 1, 1, 2, 1, 2, 2) # remove?
FMTN2            = (1, 2, 2, 2, 2, 2) # generalize for any # of strings
P, L, S, C       =  0,  1,  2,  3
T, N, I, K       =  4,  5,  6,  7
O, A, D, E, F, G =  8,  9, 10, 11, 12, 13
LLR, LLC         = 14, 15
TT, NN, II, KK   =  0,  1,  2,  3
Z, COLL, LINL    = ' ', 'Col', 'Line '
C1,  C2,  RLC    = 0, 1, 2
JTEXTS           = ['Page', 'Line', 'Sect', 'Col', 'Tab', 'Note', 'Intv', 'Chord', 'SNo', 'SNa', 'CapA', 'CapB', 'LStr', 'LCap', 'LLR', 'LLC']
NORMAL_STYLE, CURRENT_STYLE, SELECT_STYLE, COPY_STYLE = 0, 1, 2, 3
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
CC               = [(155, 155,  10, OPACITY[4]), (200, 200, 10, OPACITY[4])]
HUES             = 16
MAX_STACK_DEPTH  = 0  ;  MAX_STACK_FRAME = inspect.stack()
####################################################################################################################################################################################################
def genColors(k, nsteps=HUES, dbg=0):
    colors, clen = [], len(k[0])
    diffs = [k[1][i] - k[0][i]  for i in range(clen)]
    steps = [diffs[i]/nsteps    for i in range(clen)]
    if dbg: print(f'c1={k[0]} c2={k[1]} nsteps={nsteps} diffs={diffs} steps=', end='')  ;  print(f'[{steps[0]:6.1f} {steps[1]:6.1f} {steps[2]:6.1f} {steps[3]:6.1f}]')
    for j in range(nsteps):
        c = tuple([fri(k[0][i] + j * steps[i]) for i in range(len(k[0]))])
        if dbg: print(f'c[{j}]={c}')
        colors.append(c)
    if dbg: print(f'colors={k}')
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
#COLORS        = (INFRA_REDS, REDS, ORANGES, YELLOWS, GRAYS, GREENS, GREEN_BLUES, CYANS, BLUE_GREENS, BLUES, INDIGOS, VIOLETS, ULTRA_VIOLETS)
FONT_SCALE    = 123.42857
FONT_DPIS     = [72, 78, 84, 90, 96, 102, 108, 114, 120]
FONT_NAMES    = ['Times New Roman', 'Lucida Console', 'Courier New', 'Helvetica', 'Arial', 'Century Gothic', 'Bookman Old Style', 'Antique Olive']
FONT_COLORS_S = [PINKS[0], CYANS[0], REDS[0], BLUES[0], YELLOWS[0], GREENS[0], ORANGES[0], VIOLETS[0], REDS[13], YELLOWS[15], GREEN_BLUES[8], ORANGES[12], INDIGOS[8], ULTRA_VIOLETS[9], BLUE_GREENS[8], CC]
FONT_COLORS_L = [PINKS[0], GRAYS[0], BLUES[0], GREENS[0], YELLOWS[0], REDS[0], GRAYS[1], PINKS[8], REDS[10], YELLOWS[15], GRAYS[8], GRAYS[8], INDIGOS[8], GRAYS[9], GRAYS[8], CC]
FONT_COLORS   =  FONT_COLORS_S if SPRITES else FONT_COLORS_L
####################################################################################################################################################################################################
class Tabs(pyglet.window.Window):
    hideST2 = ['plct2cc']  #  <listcomp>?
    hideST = ['log', 'dumpData', 'dumpSelectTabs', 'cc2plct', 'cursorCol', 'dumpCursorArrows', 'setCaption', 'dumpWBWAW', 'fmtGeom']
    def __init__(self):
        dumpGlobals()
        global FULL_SCREEN, SUBPIX, ORDER_GROUP
        snapGlobArg = str(BASE_PATH / SNAP_DIR / BASE_NAME) + SFX + '.*' + SNAP_SFX
        snapGlob    = glob.glob(snapGlobArg)
        self.log(f'hideST:\n{fmtl(Tabs.hideST)}')
        self.log(f'BGN {__class__}')
        self.log(f'{VRSNX1}')
        self.log(f'{VRSNX2}')
        self.log(f'{VRSNX3}')
        self.dumpGlobalFlags()
        self.log(f'snapGlobArg={snapGlobArg}')
        self.log(f'   snapGlob={snapGlob}')
        self.deleteGlob(snapGlob, 'SNAP_GLOB')
        self.catPath = str(BASE_PATH / 'cats' / BASE_NAME) + '.cat'
        self.catPath = self.getFilePath(seq=1, filedir='cats', filesfx='.cat')
        self.log(f'catPath={self.catPath}')
        self.cobj = misc.Chord(self, LOG_FILE)
        misc.Note.setType(misc.Note.SHARP)  ;  self.log(f' Note.TYPE={misc.Note.TYPE}')
        self.shiftingTabs = 0  ;   self.shiftSign = 1
        self.inserting = 0     ;   self.insertStr = ''  ;   self.tabCols = set()
        self.jumping = 0       ;   self.jumpStr = ''    ;   self.jumpAbs=0
        self.swapping = 0      ;   self.swapSrc = ''    ;   self.swapTrg=''
        self.dfn = ''
        self.n    = []
        self.TNIK = [1, 1, 0, 1]
        nt        = 6 if QQ else 6
        self.log(f'TNIK={(fmtl(self.TNIK))}')
        self.ww, self.hh = 640, 480
        self.n, self.i, self.x, self.y, self.w, self.h, self.g = [1, 3, self.ssc(), 50, nt], [1, 1, 1, 1, nt], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], []
        self.log(f'argMap={fmtm(ARGS)}')
#        if 'N' in self.argMap and len(self.argMap['N']) == 0: self.N            = 1
        if 'f' in ARGS and len(ARGS['f'])  > 0: self.dfn          =      ARGS['f'][0]
        if 'n' in ARGS and len(ARGS['n'])  > 0: self.n            = [int(ARGS['n'][i]) for i in range(len(ARGS['n']))]
        if 'i' in ARGS and len(ARGS['i'])  > 0: self.i            = [int(ARGS['i'][i]) for i in range(len(ARGS['i']))]
        if 'x' in ARGS and len(ARGS['x'])  > 0: self.x            = [int(ARGS['x'][i]) for i in range(len(ARGS['x']))]
        if 'y' in ARGS and len(ARGS['y'])  > 0: self.y            = [int(ARGS['y'][i]) for i in range(len(ARGS['y']))]
        if 'w' in ARGS and len(ARGS['w'])  > 0: self.ww           =  int(ARGS['w'][0])
        if 'h' in ARGS and len(ARGS['h'])  > 0: self.hh           =  int(ARGS['h'][0])
        if 'F' in ARGS and len(ARGS['F']) == 0: FULL_SCREEN       = 1
        if 'g' in ARGS and len(ARGS['g']) == 0: ORDER_GROUP       = 1
        if 's' in ARGS and len(ARGS['s']) == 0: SUBPIX            = 1
#        self.log(f'[N]            N={self.N}')
        self.log(f'[f]            f={self.dfn}')
        self.log(f'[n]            n={fmtl(self.n, FMTN)}')
        self.log(f'[i]            i={fmtl(self.i, FMTN)}')
        self.log(f'[x]            x={fmtl(self.x, FMTN)}')
        self.log(f'[y]            y={fmtl(self.y, FMTN)}')
        self.log(f'[w]           ww={self.ww}')
        self.log(f'[h]           hh={self.hh}')
        self.log(f'[F]  FULL_SCREEN={FULL_SCREEN}')
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
        self.log(f'stringMap   = {fmtm(self.stringMap)}')
        self.log(f'stringKeys  = {fmtl(self.stringKeys)}')
        self.log(f'stringNames = {self.stringNames}')
        self.log(f'stringNumbs = {self.stringNumbs}')
        self.log(f'stringCapo  = {self.stringCapo}')
        self.strLabel = 'STRING'
        self.cpoLabel = ' CAPO '
        self.log(f'strLabel    = {self.strLabel}')
        self.log(f'cpoLabel    = {self.cpoLabel}')
        self._initDataPath()
        if CAT: self.cobj.dumpOMAP(str(self.catPath))
        else:   self.cobj.dumpOMAP(None)
        self.csrMode, self.hArrow, self.vArrow  = CHORD, RIGHT, UP    ;    self.dumpCursorArrows('init()')
        self._initWindowA()
        super().__init__(screen=self.screens[1], fullscreen=FULL_SCREEN, resizable=True, visible=False)
        self._initWindowB()
        self.dataHasChanged = 0
        self.tblank, self.tblanki, self.tblankCol, self.cursor, self.data = None, None, None, None, None
        self.J1, self.J2, self.cc, self.ci, self.SNAP0, self.armSnap  = None, None, 0, 0, 0, ''
        self.kbk, self.symb, self.mods, self.symbStr, self.modsStr = 0, 0, 0, '', ''
        self._reinit()
        self.log(f'END {__class__} {VRSNX1} {VRSNX2} {VRSNX3}')
        self.log(f'{INIT}', ind=0)

    def _reinit(self):
        self.log('BGN')
        self.pages, self.lines, self.sects,  self.cols                          = [], [], [], []     ;  self.A = [self.pages, self.lines, self.sects,  self.cols]
        self.tabs,  self.notes, self.intvs,  self.chords                        = [], [], [], []     ;  self.B = [self.tabs,  self.notes, self.intvs,  self.chords]
        self.snos,  self.snas,  self.capsA,  self.capsB, self.lstrs, self.lcaps = [],[],[],[],[],[]  ;  self.C = [self.snos,  self.snas,  self.capsA,  self.capsB, self.lstrs, self.lcaps]
        self.lrows, self.lcols, self.labels, self.sprites                       = [], [], [], []     ;  self.D = [self.lrows, self.lcols, self.labels, self.sprites]
        self.E = [*self.A, *self.B, *self.C, *self.D]
        self.log(f'E={fmtl(self.E)}')
        self.DF = [0, 0, 0, 0,  0, 0, 0, 0,  0, 0, 0, 0, 0, 0,  0, 0, 0, 0]
        self.J1, self.J2 = self.initJ('_reinit')
        self.data    = []   ;   self.dataHasChanged = 0
        self.kbk, self.symb, self.mods, self.symbStr, self.modsStr = 0, 0, 0, '', ''
        self.cc, self.ci, self.SNAP0, self.armSnap  = 0, 0, 0, ''
        self.tblanki, self.tblanks  = 1, [' ', '-']   ;   self.tblank = self.tblanks[self.tblanki]
        self.nblanki, self.nblanks  = 1, [' ', '-']   ;   self.nblank = self.nblanks[self.nblanki]
        self.tblankCol = self.tblank * self.n[T]      ;  self.tblankRow = self.nblank * (self.n[C] + CCC)
        self.cursor, self.caret   = None, None
        self._init()
        self.log('END')

    def dumpGlobalFlags(self):
        txt = f'AUTO_SAVE={AUTO_SAVE} CHECKER_BOARD={CHECKER_BOARD} EVENT_LOG={EVENT_LOG} FULL_SCREEN={FULL_SCREEN} ORDER_GROUP={ORDER_GROUP} RESIZE={RESIZE} SEQ_LOG_FILES={SEQ_LOG_FILES} SUBPIX={SUBPIX} VERBOSE={VERBOSE}'
        self.log(f'{txt} CCC={CCC}')

    def _initWindowA(self, dbg=1):
        display      = pyglet.canvas.get_display()
        if dbg: self.log(f'BGN {self.fmtWH()}')  ;  self.log(f'display={display}')
        self.screens = display.get_screens()  ;  s = self.screens
        if dbg:
            for i in range(len(s)): self.log(f'screens[{i}] x={s[i].x} y={s[i].y:5} {self.fmtWH(s[i].width, s[i].height)}')
            self.log(f'END {self.fmtWH()}')

    def _initWindowB(self, dbg=1):
        self.batch = pyglet.graphics.Batch()
        self._initGroups()
        if dbg: self.log(f'BGN {self.fmtWH()}')
        self.set_visible()
        if not FULL_SCREEN: self.set_size(self.ww, self.hh)
        self.ww, self.hh = self.get_size()
        if EVENT_LOG and VERBOSE:
            self.eventLogger = pygwine.WindowEventLogger()
            self.push_handlers(self.eventLogger)
#            self.keyboard = pygwine.key.KeyStateHandler()
#            self.push_handlers(self.keyboard)
        if dbg: self.log(f'END {self.fmtWH()}')

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

    def _initTpz(self, dbg=1):
        np, nl, ns, nc, nt = self.n
        self.tpc =  nt #+ CCC
        self.tps =  nc * self.tpc
        self.tpl =       self.tps
        self.tpp =  nl * self.tpl
        if dbg: self.log(f'tps={fmtl(self.tpz())}')
    ####################################################################################################################################################################################################
    @staticmethod
    def dumpObj( obj,  name, why='', file=None): Tabs.log(f'{why} {name} ObjId {hex(id(obj))} {type(obj)}', file=file)
    @staticmethod
    def dumpObjs(objs, name, why=''): [Tabs.dumpObj(o, name, why) for o in objs]  # ;   [Tabs.log(f'{hex(id(o))} type={type(o)}', ind=0) for o in obj]   ;    Tabs.log(ind=0)
    def dumpWBWAW(self, why, before, what, after, why2=''): self.log(f'{why:<24} {before:>16} {what:^20} {after:<16} {why2}')
    def ss(self,  dbg=0):   s = sum(self.TNIK)  ;                      self.log(f's={s}      TNIK={   fmtl(self.TNIK)} n={fmtl(self.n)}') if dbg else None   ;  return s
    def ssc(self, dbg=0):   s = self.ss()  ;  sc = s if s else 1   ;   self.log(f's={s} sc={sc} TNIK={fmtl(self.TNIK)} n={fmtl(self.n)}') if dbg else None   ;  return sc
    def tpz(self):   return self.tpp, self.tpl, self.tps, self.tpc
    def lens(self):  return self.lenA(), self.lenB(), self.lenC(), self.lenD()
    def lenA(self):  return [len(e) for e in self.A]
    def lenB(self):  return [len(e) for e in self.B]
    def lenC(self):  return [len(e) for e in self.C]
    def lenD(self):  return [len(e) for e in self.D]
    def lenE(self):  return [len(e) for e in self.E]
    def initJ(self, why='init'): self.J1 = [0 for _ in self.E]  ;  self.J2 = [0 for _ in self.E]  ;  self.dumpJ(why)  ;  return self.J1, self.J2
    def dumpJ(self, why):  self.log(f'J1={fmtl(self.J1, ll=1)} {sum(self.J1[:])}> {why}')  ;  self.log(f'J2={fmtl(self.J2, ll=1)} {sum(self.J2[:])}> {why}')
    def updateJs(self, i, v): self.J1[i] = v    ;    self.J2[i] += 1
    def j(self):     return [ i-1 if i else 0 for i in self.i ]
    def j2(self):    return [ i-1 if i else 0 for k, i in enumerate(self.i)  if k != S ]
    def dl(self, data=None):
        if data is None: data = self.data
        return len(data), len(data[0]), len(data[0][0]), len(data[0][0][0])

    def fmtDataDim(self, data=None): return '({} x {} x {} x {})'.format(*self.dl(data))
    def fmtGeom(self): return f'{self.cc} {fmtl(self.i, FMTN)} {fmtl(self.n, FMTN)} {fmtl(self.lenA())} {sum(self.lenA())} {fmtl(self.lenB())} {sum(self.lenB())} {fmtl(self.lenC())} {sum(self.lenC())} {fmtl(self.lenD())} {sum(self.lenD())}'
#    def fmtGeom(self): return '{} {} {} {} {} {} {} {} {} {} {}'.format(self.cc, fmtl(self.i, FMTN), fmtl(self.n, FMTN), fmtl(self.lenA()), sum(self.lenA()), fmtl(self.lenB()), sum(self.lenB()), fmtl(self.lenC()), sum(self.lenC()), fmtl(self.lenD()), sum(self.lenD()))
    def ordDict(self, od): self.log(f'{od.items()}')

    def ids(self):
        if SPRITES: return sum(self.J2[:4]), sum(self.J2[4:16]) # sum(self.J2[4:8]) + sum(self.J2[8:14]) + sum(self.J2[14:16])
        else:       return self.J2[-2],      sum(self.J2[:16])  # sum(self.J2[:4]) + sum(self.J2[4:8]) + sum(self.J2[8:14]) + sum(self.J2[14:16])
    def cnts(self): return self.J2[:16]
    ####################################################################################################################################################################################################
    def _initDataPath(self):
        dataDir  = 'data'  ;  dataSfx = '.dat'  ;  dataPfx = f'.{self.n[C]}'
        baseName  = self.dfn if self.dfn else BASE_NAME + SFX + dataPfx + dataSfx
        dataName0 = baseName + '.jnc'
        dataName1 = baseName
        dataName2 = baseName + '.bck'
        self.dataPath0 = BASE_PATH / dataDir / dataName0
        self.dataPath1 = BASE_PATH / dataDir / dataName1
        self.dataPath2 = BASE_PATH / dataDir / dataName2
#        self.log(f'BGN {self.fmtGeom()}', ind=0)
        self.log(f'dataName0 = {dataName0}')
        self.log(f'dataName1 = {dataName1}')
        self.log(f'dataName2 = {dataName2}')
        self.log(f'dataPath0 = {self.dataPath0}')
        self.log(f'dataPath1 = {self.dataPath1}')
        self.log(f'dataPath2 = {self.dataPath2}')

    def _init(self, dbg=0):
        self.ssi = 0
        self._initTpz()
        self._initDataPath()
        self.kp  = [    VIOLETS[0],    VIOLETS[12]] if CHECKER_BOARD else [   VIOLETS[10]]
        self.kl  = [     BLUES[12],      BLUES[15]] if CHECKER_BOARD else [     BLUES[12]]
        self.ks  = [     CYANS[12],      CYANS[15]] if CHECKER_BOARD else [     CYANS[12]]
        self.kc  = [      GRAYS[9],      GRAYS[13]] if CHECKER_BOARD else [     GRAYS[13]]
        self.kt  = [    ORANGES[0],     ORANGES[8]] if CHECKER_BOARD else [    ORANGES[0]]
        self.kn  = [     GREENS[0],     GREENS[12]] if CHECKER_BOARD else [     GREENS[0]]
        self.ki  = [      CYANS[0],       CYANS[8]] if CHECKER_BOARD else [      CYANS[0]]
        self.kk  = [      CYANS[0],       CYANS[8]] if CHECKER_BOARD else [      CYANS[0]]
        self.kt2 = [    YELLOWS[0],     YELLOWS[8]] if CHECKER_BOARD else [    YELLOWS[0]]
        self.kn2 = [GREEN_BLUES[0], GREEN_BLUES[8]] if CHECKER_BOARD else [GREEN_BLUES[4]]
        self.ki2 = [      CYANS[0],       CYANS[8]] if CHECKER_BOARD else [      CYANS[0]]
        self.kk2 = [      BLUES[0],       BLUES[8]] if CHECKER_BOARD else [      BLUES[0]]
        self.klr = [    ORANGES[0],     ORANGES[8]] if CHECKER_BOARD else [    ORANGES[0]]
        self.klc = [      PINKS[0],       PINKS[8]] if CHECKER_BOARD else [      PINKS[0]]
        self.kll = [       REDS[0],        REDS[8]] if CHECKER_BOARD else [       REDS[0]]
        self.k   = [self.kp, self.kl, self.ks, self.kc, self.kt, self.kn, self.ki, self.kk, self.klc, self.klr, self.kll]
        [ self.log(f'[{i:2}] {fmtl(*e):3}') for i, e in enumerate(self.k) ]
        self.readDataFile()
        if AUTO_SAVE: pyglet.clock.schedule_interval(self.autoSave, 10, how='autoSave timer')
        self.labelTextA, self.labelTextB = [], []
        self.createLabelText()
        self.labelTextC = []  ;  self.labelTextC.append('M')         ;  self.labelTextC.extend(self.labelTextB)
        self.labelTextD = []  ;  self.labelTextD.extend(['R', 'M'])  ;  self.labelTextD.extend(self.labelTextB)
        self.llText = []
        self.llText.append(self.labelTextB)
        self.llText.append(self.labelTextC)
        self.llText.append(self.labelTextD)
        txt = ['    ', '  ', '']  ;  [ self.log(f'llText[{i}]={txt[i]}{fmtl(t)}', ind=0) for i, t in enumerate(self.llText) ]
        txt = 'BGN Create '  ;  txt += 'Sprites' if SPRITES else 'Labels'
        self.dumpJ(txt)
        self.ssc()
        self.smap = {}  ;  self.skeys = []
        self.createSprites() if SPRITES else  self.createLabels()
        self.dumpJ('after createSprites()' if SPRITES else 'after createLabels()')
        self.dumpLabels('new2')
        self.dumpJ('after new2')
        self.createCursor(self.g[T + 3]) # fix
        if dbg: self.dumpStruct('_init()')
        self.log(f'END {self.fmtGeom()}', ind=0)
    ####################################################################################################################################################################################################
    def autoSave(self, dt, how, dbg=0):
        if dbg: self.log(f'dt={dt:7.4f} {how} dataHasChanged={self.dataHasChanged}')
        if AUTO_SAVE and self.dataHasChanged: self.saveDataFile(how=how)   ;   self.dataHasChanged = 0

    def on_draw(self, dbg=0):
        self.clear()
        self.batch.draw()
        if self.armSnap:
            if dbg: self.log(f'armSnap={self.armSnap}')
            self.snapshot(self.armSnap)  ;  self.armSnap = ''

    def on_resize(self, width, height):
        super().on_resize(width, height)
        self.ww, self.hh = width, height
#        if not RESIZE: return
        self.log(f'BGN {self.fmtWH()} {self.fmtDataDim(self.data)}')
        self.log(f'TNIK={(fmtl(self.TNIK))}')   ;   why = 'resize'
        self.dumpJ(f'BGN {why}')
        self.J1, self.J2 = self.initJ(why)
        if RESIZE: self.resizeSprites() if SPRITES else self.resizeLabels()
        self.dumpJ(f'END {why}')
        if VERBOSE: self.dumpStruct2(why)
        self.resizeFonts()
        self.resizeCursor()
#        self.snapshot()
        self.dumpStruct(why)
        self.setCaption(self.fmtf())
        self.log(f'END {self.fmtWH()} {self.fmtDataDim(self.data)}')
    ####################################################################################################################################################################################################
    def dumpStruct(self, why=''):
        self.log(f'BGN {why}')
#        self.dumpData(why)
        if SPRITES: self.dumpSprites()
        self.dumpLabels(why)
#        self.dumpTabs(why)
#        self.dumpCols(why)
        self.log(f'END {why}')

    def dumpStruct2(self, why=''):
        self.log(f'BGN {why}')
        self.dumpFont(why)
        self.dumpGlobalFlags()
        self.log(f'{self.fmtGeom()}', ind=0)
        self.log(f'{self.fmtDataDim(self.data)} {self.fmtDataDim(self.data)}')
        self.cobj.dumpMLimap(why)
        self.log(f'END {why}')
    ####################################################################################################################################################################################################
    def saveDataFile(self, how, f=0, dbg=1):
        if dbg:   self.log(f'{how} f={f}')
        if not f and AUTO_SAVE: dataPath = self.dataPath0
        else:                   dataPath = self.dataPath1 if f == 1 else self.dataPath2
        with open(dataPath, 'w') as DATA_FILE:
            self._saveDataFile(how, DATA_FILE)

    def _saveDataFile(self, how, file, dbg=1):
        if dbg: self.log(f'{how}')
        self.log(f'{file.name:40}', ind=0)
        np, nl, nc, nr = self.dl()  # ;  nc += CCC
        data = self.transposeData(self.data) if self.isVert() else self.data
        for p in range(np):
            if dbg: self.log(f'writing {p+1}{self.ordSfx(p+1)} page', ind=0)
            for l in range(nl):
                if dbg: self.log(f'writing {l+1}{self.ordSfx(l+1)} line', ind=0)  # if dbg  else  self.log(ind=0)  if  l  else  None
                for r in range(nr):
                    text = ''
                    for c in range(nc):
                        text += data[p][l][r][c]
                    if dbg: self.log(f'writing {r+1}{self.ordSfx(r+1)} string {text}', ind=0)  # if dbg  else  self.log(text, ind=0)
                    file.write(f'{text}\n')
                if l+1 < nl: file.write('\n')
    ####################################################################################################################################################################################################
    def createBlankData(self):
        self.log('Creating tab data using parameters {} {} {} {} {}'.format(*self.n))
        np, nl, ns, nc, nr = self.n  ;  nc += CCC
        self.data = [[[self.tblankRow for _ in range(nr)] for _ in range(nl)] for _ in range(np)]
        self.dumpDataVert() if self.isVert() else self.dumpDataHorz()
        self.data = self.transposeData()
        self.dumpDataVert() if self.isVert() else self.dumpDataHorz()

    def readDataFile(self, dbg=1):  #  empty file bug
        np, nl, ns, nc, nr = self.n
        if not self.dataPath1.exists(): self.log(f'nl nc nr = {nl} {nc} {nr} dataPath1={self.dataPath1} file does not exist calling createBlankData()')  ;  self.dataPath1.touch()  ;  self.createBlankData()  ;  return
        if dbg: self.log(f'nl={nl} nr={nr} nc={nc} dataPath1={self.dataPath1}')
        with open(str(self.dataPath1), 'r') as DATA_FILE:
            DATA_FILE.seek(0, 2)  ;  size = DATA_FILE.tell()  ;  DATA_FILE.seek(0, 0)
            self.log(f'BGN {DATA_FILE.name:40} {size:8,} bytes = {size/1024:4,.0f} KB')
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
        self.log(f'read     {l:2} Lines with {l*c:6,} Cols on {l*r:4,} Strings {nt:8,} Tabs, vert={vert} blankCol({len(self.tblankCol)})={self.tblankCol}')
        if dbg:     self.dumpDataVert() if vert else self.dumpDataHorz()
        self.data = self.transposeData()
        vert      = self.isVert()
        if dbg:     self.dumpDataVert() if vert else self.dumpDataHorz()
        self.saveDataFile('readDataFile()', f=2)
        self.log(f'assert: size=nt+2*(l*r+l-1) {nt:8,} + {2*(l*r+l-1)} = {size:8,} bytes assert isVert={vert}')
#        assert size == nt + 2 * (l * r + l - 1)  ;  assert vert
        self.log(f'END {DATA_FILE.name:40} {size:8,} bytes = {size/1024:4,.0f} KB')

    def isVert(self, data=None, dbg=1):
        if data is None: data = self.data
        if dbg: self.log(f'BGN type(data data[0] data[00] data[000])={type(data)} {type(data[0])} {type(data[0][0])} {type(data[0][0][0])}')
        assert type(data) is list and type(data[0]) is list and type(data[0][0]) is list and type(data[0][0][0]) is str
        vert = 1 if len(data[0][0]) > len(data[0][0][0]) else 0
        if dbg: self.log(f'END len(data data[0] data[00] data[000])={len(data)} {len(data[0])} {len(data[0][0])} {len(data[0][0][0])} return vert={vert}')
        return vert

    def OLD_isVert(self, data=None, dbg=1):
        if data is None: data = self.data
        vert = 1
        if dbg: self.log(f'BGN type(data 0 00 000)={type(data)} {type(data[0])} {type(data[0][0])} {type(data[0][0][0])}')
        assert type(data) is list and type(data[0]) is list and type(data[0][0]) is list and type(data[0][0][0]) is str
        for p in range(len(data)):
            assert len(data[p]) == len(data[0])
            for l in range(len(data[p])):
                assert len(data[p][l]) == len(data[p][0])
                for c in range(len(data[p][l])):
                    assert len(data[p][l][c]) == len(data[p][l][0])
                if len(data[p][l]) < len(data[p][l][0]): vert = 0  ;  break
        if dbg: self.log(f'END len(data 0 00 000)={len(data)} {len(data[0])} {len(data[0][0])} {len(data[0][0][0])} return vdf={vert}')
        return vert
    ####################################################################################################################################################################################################
#   def dumpTabData(self, data=None, why='', lc=1, ll=1, i=0):
#        if data is None: data = self.data
#        self.log(f'BGN {why}')
#        self.dumpDataVert(data, lc, ll, i) if self.isVert(data) else self.dumpDataHorz(data, lc, ll, i)
#        transposeData = self.transposeData(data, why='Internal')
#        self.dumpDataVert(transposeData, lc, ll, i) if self.isVer(transposeData) else self.dumpDataHorz(transposeData, lc, ll, i)
#        self.log(f'END {why}')

    def dumpDataHorz(self, data=None, lc=1, ll=1, i=0):
        if data is None: data = self.data
        self.log(f'BGN lc={lc} ll={ll} i={i} {self.fmtDataDim(data)}')
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
        self.log(f'END lc={lc} ll={ll} i={i} {self.fmtDataDim(data)}')

    def dumpDataVert(self, data=None, lc=1, ll=1, i=0):
        if data is None: data = self.data
        self.log(f'BGN lc={lc} ll={ll} i={i} {self.fmtDataDim(data)}')
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
        self.log(f'END lc={lc} ll={ll} i={i} {self.fmtDataDim(data)}')
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
        if dbg: self.log(f'BGN {why} {self.fmtDataDim(data)}')
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
        if dbg: self.log(f'END {why} {self.fmtDataDim(transposed)}')
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
        self.log(f'texts={fmtl(texts)}', ind=0)
        self.dumpLabelText(texts)
    ####################################################################################################################################################################################################
    def geom(self, p=None, j=0, init=0, nn=0, dbg=0):
        mx, my = -1, -1                                      ;  iw, ih =  self.w[j], self.h[j]
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
    def toggleTabs(self, how, tnik):
        self.log(f'BGN {how} tnik={tnik} TNIK={fmtl(self.TNIK)} n={fmtl(self.n)} lenA={self.lenA()} lenB={self.lenB()}')
        if not self.TNIK[tnik] and not self.B[tnik]: self.showTabs(tnik)
        else:                                        self.hideTabs(tnik)
        self.TNIK[tnik] = not self.TNIK[tnik]   ;    self.n[S] = self.ssc()
        self.log(f'calling on_resize() tnik={tnik} TNIK={fmtl(self.TNIK)} n={fmtl(self.n)} lenA={self.lenA()} lenB={self.lenB()}')
        self.on_resize(self.ww, self.hh)
        self.log(f'END {how} tnik={tnik} TNIK={fmtl(self.TNIK)} n={fmtl(self.n)} lenA={self.lenA()} lenB={self.lenB()}')

    def hideTabs(self, tnik, dbg=VERBOSE):
        tabs = self.B[tnik]   # ;   cols = self.cols   ;  sects = self.sects   ;   llcs = self.lcols
        ttype = 'Tab' if tnik == TT  else 'Note' if tnik == NN else 'Chord' if tnik == KK else '???'  ;  t, c, s, r = 0, 0, 0, 0
        np, nl, ns, nc, nt = self.n
        ns2 = nl * ns
        nc2 = nc * ns2
        _tnik = tnik if tnik < 2 else 2
        self.log(f'BGN np={np} nl={nl} ns={ns} nc={nc} nt={nt} ns2={ns2} nc2={nc2} len({ttype})={len(tabs)}')
        for l in range(nl-1, -1, -1):
            for q in range(CCC-1, -1, -1):
                self.hideLabel(self.lcols, q + l * (nc + CCC), 'LLC', dbg=dbg)
        for s in range(ns2-1, ns2-nl-1, -1):
            self.hideLabel(self.sects, s, 'Sect', dbg=dbg)
        for c in range(nc2-1, nc2-(len(self.cols)//nl)-1, -1):
            self.hideLabel(self.cols, c, 'Col', dbg=dbg)
        for t in range(len(tabs)-1, -1, -1):
            self.hideLabel(tabs, t, ttype, dbg=dbg)
        if CCC and tnik == TT:
            for l in range(nl-1, -1, -1):
                if CCC > C2:
                    for z in range(nt-1, -1, -1):
                        self.hideLabel(self.snos, z + l * nt, 'SNo', dbg=dbg)
                if CCC > C1:
                    for z in range(nt-1, -1, -1):
                        self.hideLabel(self.capsA, z + l * nt, 'Cap1', dbg=dbg)
        elif CCC and tnik == NN:
            for l in range(nl-1, -1, -1):
                if CCC > C2:
                    for z in range(nt-1, -1, -1):
                        self.hideLabel(self.snas, z + l * nt, 'SNa', dbg=dbg)
                if CCC > C1:
                    for z in range(nt-1, -1, -1):
                        self.hideLabel(self.capsB, z + l * nt, 'Cap2', dbg=dbg)
        elif CCC and tnik == KK:
            for l in range(nl-1, -1, -1):
                if CCC > C2:
                    for z in range(nt-1, -1, -1):
                        self.hideLabel(self.lstrs, z + l * nt, 'LStr', dbg=dbg)
                if CCC > C1:
                    for z in range(nt-1, -1, -1):
                        self.hideLabel(self.lcaps, z + l * nt, 'LCap', dbg=dbg)
        self.snapshot(f'hideTabs() t={t+1} c={c+1} s={s+1} len({ttype})={len(tabs)}')
        self.log(f'END t={t+1} c={c+1} s={s+1} len({ttype})={len(tabs)}')

    def showTabs(self, tnik, dbg=0):
        np, nl, ns, nc, nt = self.n           ;  tabs = self.B[tnik]
        _nt = nl * nc * nt  ;  _nc = nl * nc  ;  _ns = nl    ;   _tnik = tnik + len(self.B)
        ks  = self.ks       ;   kc = self.kc  ;  chordName = ''
        k = [self.kt, self.kn, self.ki, self.kk]
        ttype = 'Tab' if tnik == TT  else 'Note' if tnik == NN else 'Chord' if tnik == KK else '???'  ;  t, c, s = 0, 0, 0
        self.log(f'BGN _nt={_nt} _nc={_nc} _ns={_ns} len({ttype})={len(tabs)}')
        for s in range(_ns):
            self.showLabel(s, p=self.sects, j=S, g=self.g[S], k=ks)
        for c in range(_nc):
            self.showLabel(c, p=self.cols,  j=C,  g=self.g[C], k=kc)
        for t in range(_nt):
            tt = t % nt
            p, l, cc = t // _nt, t // (nc * nt), (t // nt) % nc
            if dbg: self.log(f'{p} {l} {cc} {tt}', ind=0, end=' ')
            tab = self.data[p][l][cc][tt]
            note = self.getNoteName(tt, tab) if self.isFret(tab) else self.nblank
            if not t:   chordName = self.cobj.getChordName(p, l, cc)  # call only once per column or tpc
            chord = chordName[tt] if len(chordName) > tt else self.nblank
            text  = tab if tnik == TT else note if tnik == NN else chord if tnik == KK else '???'
            self.showLabel(tt, p=tabs, j=_tnik, g=self.g[T], t=text, k=k[tnik])
        self.snapshot(f'showTabs() t={t+1} c={c+1} s={s+1} len({ttype})={len(tabs)}')
        self.log(f'END s={s} c={c} t={t} len({ttype})={len(tabs)}')
    ####################################################################################################################################################################################################
    def toggleRLCols(self, how):
        global CCC  ;  old = CCC  ;  CCC = (CCC + 1) % 3
        self.log(f'BGN {how} old CCC={old} new CCC={CCC} lenC={self.lenC()} QQ={QQ}')
        show = 1 if (CCC == 1 and (not self.lenC()[0] or not self.lenC()[1])) or (CCC == 2 and (not self.lenC()[2])) else 0
        if show: self.showRLCols()
        else:    self.hideRLCols()
        self.log(f'      lenE={self.lenE()}')
        self.on_resize(self.ww, self.hh)
        self.log(f'END {how} lenE={self.lenE()}')

    def showRLCols(self, dbg=VERBOSE):
        self.dumpJ('showRLCols()')
        self.log(f'lenE={self.lenE()}')
        np, nl, ns, nc, nt = self.n   ;   l, s, c, t = 0, 0, 0, 0   ;   v = 1
        tt, nn, kkk = self.TNIK[TT], self.TNIK[NN], self.TNIK[KK]
        kt2, kn2, kk2 = self.kt2, self.kn2, self.kk2   ;   kc = self.kc   ;   kk, kl = kc, kt2
        self.log(f'BGN nl={nl} ns={ns} nc={nc} nt={nt} QQ={QQ}')
        for l in range(nl):
            for s in range(ns):
                c = CCC - 1     ;   self.log(f'CCC={CCC} l={l} s={s} c={c}')
                self.J1[C] = c  ;   j = C  ;  why = 'new Col'
                if SPRITES: self.createSprite(j=j, p=self.cols, x=0, y=0, w=self.w[C], h=self.h[C], kk=self.cci(c, kc), g=self.g[C], why=why, kl=kc, v=v, dbg=dbg)
                else:       self.createLabel( j=j, p=self.cols, x=0, y=0, w=0,         h=0,         kk=self.cci(c, kc), g=self.g[C], why=why, kl=kc,      dbg=dbg)
                for t in range(nt):
                    text = '???'  ;  plist = []
                    if   tt and s == 0:
                        if   c == C1:  text = self.stringNumbs[t]   ;  plist = self.snos   ;  kl = kt2  ;  kk = self.cci(t, kl)  ;  j = O  ;  why = 'new SNo'
                        elif c == C2:  text = self.stringCapo[t]    ;  plist = self.capsA  ;  kl = kt2  ;  kk = self.cci(t, kl)  ;  j = D  ;  why = 'new Cap1'
                        else: msg = f'ERROR Unexpected else c={c}'  ;  self.log(msg)  ;  self.quit(msg)
                        self.createLabel(j=j, p=plist, x=0, y=0, w=0, h=0, kk=kk, g=self.g[T], why=why, t=text, kl=kl, dbg=dbg)
                    elif nn and (s == 1 or (s == 0 and not tt)):
                        if   c == C1:  text = self.stringNames[t]   ;  plist = self.snas   ;  kl = kn2  ;  kk = self.cci(t, kl)  ;  j = A  ;  why = 'new SNa'
                        elif c == C2:  text = self.stringCapo[t]    ;  plist = self.capsB  ;  kl = kn2  ;  kk = self.cci(t, kl)  ;  j = E  ;  why = 'new Cap2'
                        else: msg = f'ERROR Unexpected else c={c}'  ;  self.log(msg)  ;  self.quit(msg)
                        self.createLabel(j=N, p=plist, x=0, y=0, w=0, h=0, kk=kk, g=self.g[T], why=why, t=text, kl=kl, dbg=dbg)
                    elif kkk and (s == 2 or (s == 1 and (not tt or not nn)) or (s == 0 and (not tt and not nn))):
                        if   c == C1: text = self.strLabel[t]       ;  plist = self.lstrs  ;  kl = kk2  ;  kk = self.cci(t, kl)  ;  j = F  ;  why = 'new LStr'
                        elif c == C2: text = self.cpoLabel[t]       ;  plist = self.lcaps  ;  kl = kk2  ;  kk = self.cci(t, kl)  ;  j = G  ;  why = 'new LCap'
                        else: msg = f'ERROR Unexpected else c={c}'  ;  self.log(msg)  ;  self.quit(msg)
                        self.createLabel(j=K, p=plist, x=0, y=0, w=0, h=0, kk=kk, g=self.g[T], why=why, t=text, kl=kl, dbg=dbg)
                    else: msg = f'ERROR Unexpected else s={s}'  ;  self.log(msg)  ;  self.quit(msg)
        self.snapshot(f'showRLCols() l={l} s={s} c={c} t={t}')
        self.log('END')

    def hideRLCols(self, dbg=VERBOSE):
        np, nl, ns, nc, nt = self.n   ;   cols = self.cols   ;   nc = len(cols)   ;   l, s, c = 0, 0, 0   ;  sno, sna, cap1, cap2, lstr, lcap = 0, 0, 0, 0, 0, 0
        ccc = 2 # if CCC else 1
        self.log(f'BGN nl={nl} ns={ns} nc={nc} nt={nt} ccc={ccc}')
        for c in range(nc-1, nc - (ccc * ns * nl) - 1, -1):
            self.hideLabel(cols, c,   t='Col', dbg=dbg)
        snos, capsA, snas, capsB, lstrs, lcaps = self.snos, self.capsA, self.snas, self.capsB, self.lstrs, self.lcaps
        for sno in range(len(snos)):
            self.hideLabel(snos, sno, t='SNo')
        for cap1 in range(len(capsA)):
            self.hideLabel(capsA, cap1, t='Cap1')
        for sna in range(len(snas)):
            self.hideLabel(snas, sna, t='SNa')
        for cap2 in range(len(capsB)):
            self.hideLabel(capsB, cap2, t='Cap2')
        for lstr in range(len(lstrs)):
            self.hideLabel(lstrs, lstr, t='LStr')
        for lcap in range(len(lcaps)):
            self.hideLabel(lcaps, lcap, t='LCap')
        self.snapshot(f'hideRLCols() l={l} s={s} c={c}  sno={sno} sna={sna} cap1={cap1} cap2={cap2} lstr={lstr} lcap={lcap}')
        self.log(f'END l={l} s={s} c={c}')
    ####################################################################################################################################################################################################
    def toggleLLRows(self, how):
        global QQ  ;  old = QQ  ;  QQ = not QQ  ;  self.log(f'{how} old QQ={old} new QQ={QQ} CCC={CCC}')  ;  self.log(f'llText={fmtl(self.llText[CCC])}')
        if QQ and not self.lrows: self.showLLRows()
        else:                      self.hideLLRows()
        self.on_resize(self.ww, self.hh)

    def showLLRows(self, dbg=0):
        l = 0
        for l in range(len(self.lines)):
            self.createLLRow(self.lines[l], l)
        if dbg: self.snapshot(f'showLLRows() l={l}')

    def hideLLRows(self, dbg=0): #        self.quit('FILTER')
        nr = len(self.lrows)    ;  nc = len(self.lcols)  ;  cc, rr = 0, 0   ;   assert not nc % nr
        nc = nc // nr  #  normalize
        for rr in range(nr):
            self.hideLabel(self.lrows, rr, 'LLR')
            for cc in range(nc):
                self.hideLabel(self.lcols, cc + rr * nc, 'LLC')
        if dbg: self.snapshot(f'hideLLRows() nr={nr} nc={nc} rr={rr} cc={cc}')
    ####################################################################################################################################################################################################
    def createLLRow(self, p, pi, dbg=1, dbg2=1):
        klr = self.klr  ;  klc = self.klc  ;  kkr = self.cci(pi, klr)   ;   nn = self.n[T] * self.ss() + 1
        nr, ir, xr, yr, wr, hr, gr, mx, my = self.geom(p=p, j=S, nn=nn, dbg=0)
        if SPRITES: xr += wr/2  ;  yr += hr/2
        self.J1[LLR] = pi   ;   nn = self.n[C]
        row = self.createLabel(LLR, self.lrows, xr, yr, wr, hr, kkr, gr, why=f'new ', kl=klr, dbg=dbg)
        nc, ic, xc, yc, wc, hc, gc, mx, my = self.geom(p=row, j=C, nn=nn, dbg=0)   ;  sc = nc * pi
#        if dbg: self.log(f'nn={nn} nc={nc} pi={pi} sc={sc} len(lcols)={len(self.lcols)}')
        if SPRITES: xc += wc/2
        for c in range(nc):
            kkc = self.cci(pi, klc)
            j = LLC   ;   sc += 1   ;   self.J1[j] = c
            text = self.llText[CCC]
            txt = text[c] if text and len(text) >= c else ''
            self.createLabel(j, self.lcols, xc + c*wc, yc, wc, hc, kkc, gc, why=f'new ', t=txt, kl=klc, dbg=dbg)
#            self.createLabel(f'{Z*(c+1)}{sc}' if self.DF[LLC] and not c else text[c], LLC, self.lcols, xc + c*wc, yc, wc, hc, kkc, gc, why=f'new LC {sc}', kl=klc, dbg=dbg)
#            if not CCC and c == 0:  self.hideLabel(self.lcols, sc-1, f'Hide LLC {sc}')
#            if CCC == 1 and c == 1: self.hideLabel(self.lcols, sc-1, f'Hide LLC {sc}')
        if dbg2: self.log(f'pi={pi:3} px={p.x:7.2f} py={p.y:7.2f} pw={p.width:7.2f} ph={p.height:7.2f}', ind=0)
        if dbg2: self.log(f'nr={nr:3} xr={xr:7.2f} yr={yr:7.2f} wr={wr:7.2f} hr={hr:7.2f}', ind=0)
        if dbg2: self.log(f'nc={nc:3} xc={xc:7.2f} yc={yc:7.2f} wc={wc:7.2f} hc={hc:7.2f}', ind=0)
        if   type(p) is pyglet.text.Label:    p.y -= hr/2  ;  p.height -= hr  # ;                      self.log(f'p.y -= hr/2, p.h -= hr: p.y = {p.y:7.2f} p.h = {p.height:7.2f}', ind=0)
        elif type(p) is pyglet.sprite.Sprite: my = (p.height - hr)/self.h[L]  ;   p.scale_y = my  # ;  self.log(f'p.y -= hr, my = (p.h-hr)/h[L]: h[L]={self.h[L]} my={my:7.5f} p.y={p.y:7.2f} p.h={p.height:7.2f}', ind=0)
        return p

    def resizeLLRow(self, p, pi, dbg=1, dbg2=1):
        nn = self.n[T] * self.ss() + 1
        nr, ir, xr, yr, wr, hr, gr, mxr, myr = self.geom(p=p, j=S, nn=nn, dbg=0)
        if SPRITES: xr += wr/2  ;  yr += hr/2
        self.J1[LLR] = 0   ;   self.J2[LLR] += 1   ;   nn = self.n[C]
        row = self.lrows[pi]    ;    row.width = wr  ;   row.height = hr  ;   row.x = xr  ;   row.y = yr
        if dbg: self.dumpLabel(row, *self.ids(), *self.cnts(), why=f'mod LLR {pi+1}')
        nc, ic, xc, yc, wc, hc, gc, mxc, myc = self.geom(p=row, j=C, nn=nn, dbg=0)   ;   sc = nc * pi
#        if dbg2: self.log(f'nn={nn} nc={nc} pi={pi} sc={sc} len(lcols)={len(self.lcols)}')
        if SPRITES: xc += wc/2
        for c in range(nc):
            j = LLC   ;   self.J1[j] = c   ;   self.J2[j] += 1
#            if dbg: self.log(f'sc={sc} c={c} len(lcols)={len(self.lcols)} n={fmtl(self.n)}')
            col = self.lcols[sc]
            col.text = self.llText[CCC][c]   ;   sc += 1
            col.width = wc   ;   col.height = hc  ;   col.x = xc + c * wc  ;  col.y = yc
            if dbg: self.dumpLabel(col, *self.ids(), *self.cnts(), why=f'mod LLC {sc}')
        if dbg2: self.log(f'nc={nc} pi={pi} sc={sc} len(lcols)={len(self.lcols)}')
        if dbg2: self.log(f'row.y={row.y:7.2f} yr={yr:7.2f} pi={pi} hr={hr:7.2f}', ind=0)
        if dbg2: self.log(f'pi={pi:3} px={p.x:7.2f} py={p.y:7.2f} pw={p.width:7.2f} ph={p.height:7.2f}', ind=0)
        if dbg2: self.log(f'nr={nr:3} xr={xr:7.2f} yr={yr:7.2f} wr={wr:7.2f} hr={hr:7.2f}', ind=0)
        if dbg2: self.log(f'nc={nc:3} xc={xc:7.2f} yc={yc:7.2f} wc={wc:7.2f} hc={hc:7.2f}', ind=0)
        if   type(p) is pyglet.text.Label:    p.y -= hr/2  ;  p.height -= hr  # ;                               self.log(f'p.y -= hr/2, p.h -= hr: p.y = {p.y:7.2f} p.h = {p.height:7.2f}', ind=0)
        elif type(p) is pyglet.sprite.Sprite: my = (p.height - hr)/self.h[L]  ;   p.scale_y = my  # ;  self.log(f'p.y -= hr, my = (p.h-hr)/h[L]: h[L]={self.h[L]} my={my:7.5f} p.y={p.y:7.2f} p.h={p.height:7.2f}', ind=0)
        if dbg2: self.log(f'p.y -= hr/2, p.height -= hr: p.y = {p.y:7.2f} p.h = {p.height:7.2f}', ind=0)
        return p
    ####################################################################################################################################################################################################
    def createLabels(self, dbg=1, dbg2=0):
        self.log(f'BGN {self.fmtGeom()}', ind=0)
        if dbg: self.dumpLabel()
        for p, page in                  enumerate(self.g_createLabels(None, P, self.pages, dbg=dbg, dbg2=dbg2)):
            for l, line in              enumerate(self.g_createLabels(page, L, self.lines, dbg=dbg, dbg2=dbg2)):
                for s, sect in          enumerate(self.g_createLabels(line, S, self.sects, dbg=dbg, dbg2=dbg2)):
                    for c, col in       enumerate(self.g_createLabels(sect, C, self.cols,  dbg=dbg, dbg2=dbg2)):
                        for t, lbl in   enumerate(self.g_createLabels2(col)):
                            if dbg > 1: self.log(f'lbl.y={lbl.y}')
        if dbg: self.dumpLabel()
        self.log(f'END {self.fmtGeom()}', ind=0)

    def g_createLabels(self, p, j, lablist, dbg=1, dbg2=0):
        n, i, x, y, w, h, g, mx, my = self.geom(p=p, j=j, init=1, dbg=dbg2)  ;  x2 = x  ;  y2 = y  ;    kl = self.k[j]
        for m in range(n):
            if   j == C: x2 = x + m * w
            elif p:      y2 = y - m * h
            self.J1[j] = m
            lbl = self.createLabel(j=j, p=lablist, x=x2, y=y2, w=w, h=h, kk=self.cci(j, kl), g=g, why='new ', kl=kl, dbg=dbg)
            if QQ and j == L: self.createLLRow(lbl, m)
            yield lbl
    ####################################################################################################################################################################################################
    def g_createLabels2(self, col, dbg=1, dbg2=0):
        p, l, s, c = self.J1[P], self.J1[L], self.J1[S], self.J1[C]   ;  tt, nn, kkk = self.TNIK[TT], self.TNIK[NN], self.TNIK[KK]   ;   chunks = []
        nt, it, xt, yt, wt, ht, gt, mx, my = self.geom(p=col, j=T, init=1, dbg=dbg2)   ;   kt, kn, kk = self.kt, self.kn, self.kk    ;   kt2, kn2, kk2 = self.kt2, self.kn2, self.kk2
        for t in range(nt):
            why = 'new '
            if   tt and s == 0:
                if   CCC     and c == C1:  tab = self.stringNumbs[t] ;  plist = self.snos   ;  kl = kt2  ;  k = self.cci(t, kl)  ;  j = O
                elif CCC > 1 and c == C2:  tab = self.stringCapo[t]  ;  plist = self.capsA  ;  kl = kt2  ;  k = self.cci(t, kl)  ;  j = D
                else:               tab = self.data[p][l][c-CCC][t]  ;  plist = self.tabs   ;  kl = kt   ;  k = self.cci(t, kl)  ;  j = T
                if self.isNBTab(tab):     self.tabCols.add(self.plc2cn(p, l, c))
                self.createLabel(j, plist,  xt, yt - t*ht, wt, ht, k, gt, why=why, t=tab, kl=kl, dbg=dbg)  ;  yield tab
            elif nn and (s == 1 or (s == 0 and not tt)):
                if   CCC     and c == C1: note = self.stringNames[t] ;  plist = self.snas   ;  kl = kn2  ;  k = self.cci(t, kl)  ;  j = A
                elif CCC > 1 and c == C2: note = self.stringCapo[t]  ;  plist = self.capsB  ;  kl = kn2  ;  k = self.cci(t, kl)  ;  j = E
                else:               tab = self.data[p][l][c-CCC][t]  ;  plist = self.notes  ;  kl = kn   ;  k = self.cci(t, kl)  ;  j = N  ;  note = self.getNoteName(t, tab) if self.isFret(tab) else self.nblank
                self.createLabel(j, plist,  xt, yt - t*ht, wt, ht, k, gt, why=why, t=note, kl=kl, dbg=dbg) ;  yield note
            elif kkk and (s == 2 or (s == 1 and (not tt or not nn)) or (s == 0 and (not tt and not nn))):
                if   CCC     and c == C1: chord = self.strLabel[t]   ;  plist = self.lstrs  ;  kl = kk2  ;  k = self.cci(t, kl)  ;  j = F
                elif CCC > 1 and c == C2: chord = self.cpoLabel[t]   ;  plist = self.lcaps  ;  kl = kk2  ;  k = self.cci(t, kl)  ;  j = G
                else:
                    if not t: chordName, chunks = self.cobj.getChordName(p, l, c-CCC)
                    chord = chunks[t] if len(chunks) > t else self.nblank   ;   j = K
                    plist = self.chords  ;  kl = kk   ;   k = self.cci(t, kl)
                self.createLabel(j, plist,  xt, yt - t*ht, wt, ht, k, gt, why=why, t=chord, kl=kl, dbg=dbg)  ;  yield chord
            else: self.log(f'ERROR Not Handled s={s} tt={tt} nn={nn} kk={kkk}')  ;  yield None
    ####################################################################################################################################################################################################
    def createSprites(self, dbg=1, dbg2=0):
        self.log(f'BGN {self.fmtGeom()}', ind=0)  ;  v = 0
        if dbg: self.dumpLabel()  ;  self.dumpSprite()
        for p, (page, v) in             enumerate(self.g_createSprites(None, P, self.pages, v, dbg=dbg, dbg2=dbg2)):
            for l, (line, _) in         enumerate(self.g_createSprites(page, L, self.lines, v, dbg=dbg, dbg2=dbg2)):
                for s, (sect, _) in     enumerate(self.g_createSprites(line, S, self.sects, v, dbg=dbg, dbg2=dbg2)):
                    for c, (col, _) in  enumerate(self.g_createSprites(sect, C, self.cols,  v, dbg=dbg, dbg2=dbg2)):
                        for t, lbl in   enumerate(self.g_createLabels2(col)):
                            if dbg > 1: self.log(f'lbl.y={lbl.y}')
        if dbg: self.dumpSprite()  ;  self.dumpLabel()
        self.log(f'END {self.fmtGeom()}', ind=0)

    def g_createSprites(self, p, j, sprlist, v, dbg=1, dbg2=0):
        n, i, x, y, w, h, g, mx, my = self.geom(p=p, j=j, init=1, dbg=dbg2)  ;  x2 = x  ;  y2 = y  ;  kl=self.k[j]
        for m in range(n):
            if   j == C:     x2 = x + m * w
            elif p:          y2 = y - m * h
            self.J1[j] = m
            if   j == P:    v=1 if self.J2[j] == self.i[P] else 0
            spr = self.createSprite(j, sprlist, x2, y2, w, h, self.cci(j, kl), g, why=f'new ', kl=kl, v=v, dbg=dbg)
            if QQ and j == L: self.createLLRow(spr, m)
            yield spr, v
    ####################################################################################################################################################################################################
    def resizeLabels(self, dbg=VERBOSE):
        self.log(f'BGN {self.fmtGeom()}', ind=0)
        if dbg: self.dumpLabel()
        for p, page in                  enumerate(self.g_resizeLabels(None, P, self.pages, why=JTEXTS[P])):
            for l, line in              enumerate(self.g_resizeLabels(page, L, self.lines, why=JTEXTS[L])):
                for s, sect in          enumerate(self.g_resizeLabels(line, S, self.sects, why=JTEXTS[S])):
                    for c, col in       enumerate(self.g_resizeLabels(sect, C, self.cols,  why=JTEXTS[C])):
                        for t, lbl in   enumerate(self.g_resizeLabels2(col)):
                            if dbg > 1: self.log(f'lbl.y={lbl.y}')
        if dbg: self.dumpLabel()
        self.log(f'END {self.fmtGeom()}', ind=0)

    def g_resizeLabels(self, p, j, lablist, why, dbg=VERBOSE, dbg2=0):
        n, i, x, y, w, h, g, mx, my = self.geom(p=p, j=j, dbg=dbg2)  ;  x2 = x  ;  y2 = y
        for m in range(n):
            if   j == C: x2 = x + m * w
            elif p:      y2 = y - m * h
            assert(len(lablist))
            lbl = lablist[self.J2[j]]  ;  lbl.x = x2  ;  lbl.y = y2  ;  lbl.width = w  ;  lbl.height = h
            self.J1[j] = m
            self.J2[j] += 1
            if dbg: self.dumpLabel(lbl, *self.ids(), *self.cnts(), why=f'mod{why}{self.J2[j]}')
            if QQ and j == L: self.resizeLLRow(lbl, m)
            yield lbl
    ####################################################################################################################################################################################################
    def g_resizeLabels2(self, col, dbg=VERBOSE, dbg2=0):
        n, i, x, y, w, h, g, mx, my = self.geom(p=col, j=T, dbg=dbg2)  ;  lbl = None
        p,       l,    s,    c       = self.J1[P], self.J1[L], self.J1[S], self.J1[C]
        st,     sn,   si,   sk       = self.J2[T], self.J2[N], self.J2[I], self.J2[K]
        ssno, ssna, scap1, scap2, slstr, slcap = self.J2[O], self.J2[A], self.J2[D], self.J2[E], self.J2[F], self.J2[G]
        tt, nn, kk = self.TNIK[TT], self.TNIK[NN], self.TNIK[KK]
        for t in range(n):##            self.log(f 'tt={tt} nn={nn} kk={kk} TNIK={fmtl(self.TNIK)}  p={p} l={l} s={s} c={c}  st={st} sn={sn} si={si} sk={sk}', ind=0)
            why = 'mod '
            if   tt and s == 0:
                if   CCC     and c == C1:   tab = self.snos[ssno]     ;   ssno += 1  ;  why += f'SNo {ssno}'
                elif CCC > 1 and c == C2:   tab = self.capsA[scap1]   ;  scap1 += 1  ;  why += f'Cap1 {scap1}'
                else:                       tab = self.tabs[st]       ;     st += 1  ;  why += f'Tab {st}'
                tab.width = w    ;   tab.height = h   ;   tab.x = x   ;  tab.y = y - t * h  ;  lbl = tab
                self.J1[T] = t   ;  self.J2[T] = st   ;  self.J2[O] = ssno  ;  self.J2[D] = scap1
                if dbg:   self.dumpLabel(  lbl, *self.ids(), *self.cnts(), why=why)
            elif nn and (s == 1 and tt or (s == 0 and not tt)):
                if   CCC     and c == C1:  note = self.snas[ssna]     ;  ssna += 1  ;  why += f'SNam {ssna}'
                elif CCC > 1 and c == C2:  note = self.capsB[scap2]   ; scap2 += 1  ;  why += f'Cap2 {scap2}'
                else:                      note = self.notes[sn]      ;    sn += 1  ;  why += f'Note {sn}'
                note.width = w   ;  note.height = h   ;   note.x = x  ;    note.y = y - t * h  ;  lbl = note
                self.J1[N] = t   ;  self.J2[N] = sn   ;  self.J2[A] = ssna  ;  self.J2[E] = scap2
                if dbg:   self.dumpLabel( lbl, *self.ids(), *self.cnts(), why=why)
            elif kk and ((s == 2 and  tt and nn) or (s == 1 and tt or nn) or (s == 0 and not tt and not nn)):
                if   CCC     and c == C1: chord = self.lstrs[slstr]  ;  slstr += 1  ;  why += f'LStr {slstr}'
                elif CCC > 1 and c == C2: chord = self.lcaps[slcap]  ;  slcap += 1  ;  why += f'LCap {slcap}'
                else:                     chord = self.chords[sk]    ;     sk += 1  ;  why += f'Chord {sk}'
                chord.width = w  ;  chord.height = h  ;  chord.x = x  ;  chord.y = y - t * h  ;  lbl = chord
                self.J1[K] = t   ;  self.J2[K] = sk   ;  self.J2[F] = slstr  ;  self.J2[G] = slcap
                if dbg:   self.dumpLabel(lbl, *self.ids(), *self.cnts(), why=why)
            elif s == 0: self.log(f's={s} TNIK={self.TNIK} n={n} plsct {p} {l} {s} {c} {t}')
            else: e = f'Error: Not Handled s={s} tt={tt} nn={nn} kk={kk}'   ;  self.log(f'{e}')  ;  self.quit(e)
            yield lbl
    ####################################################################################################################################################################################################
    def resizeSprites(self, dbg=VERBOSE):
        self.log(f'BGN {self.fmtGeom()}', ind=0)
        if dbg: self.dumpSprite()
        for p, page in                enumerate(self.g_resizeSprites(None, P, self.pages, why=JTEXTS[P])):
            for l, line in            enumerate(self.g_resizeSprites(page, L, self.lines, why=JTEXTS[L])):
                for s, sect in        enumerate(self.g_resizeSprites(line, S, self.sects, why=JTEXTS[S])):
                    for c, col in     enumerate(self.g_resizeSprites(sect, C, self.cols,  why=JTEXTS[C])):
                        for t, lbl in enumerate(self.g_resizeLabels2(col)):
                            if dbg > 1: self.log(f'lbl.y={lbl.y}')
        if dbg: self.dumpLabel()  ;  self.dumpSprite()
        self.log(f'END {self.fmtGeom()}', ind=0)

    def g_resizeSprites(self, p, j, sprlist, why, dbg=VERBOSE, dbg2=0):
        nn = self.n[j] if QQ else 0
        n, i, x, y, w, h, g, mx, my = self.geom(p=p, j=j, nn=nn, dbg=dbg2)  ;  x2 = x  ;  y2 = y
        for m in range(n):
            if   j == C: x2 = x + m * w
            elif p:      y2 = y - m * h
            spr = sprlist[self.J2[j]]
            spr.update(x=x2, y=y2, scale_x=mx, scale_y=my)
            self.J1[j] = m
            self.J2[j] += 1
            if dbg: self.dumpSprite(spr, *self.ids(), *self.cnts(), why = f'mod{why}{self.J2[j]}')
            if QQ and j == L: self.resizeLLRow(spr, m)
            yield spr
    ####################################################################################################################################################################################################
    def createCursor(self, g):
        self.cc = self.cursorCol()
        c = self.tabs[self.cc]
        w, h = c.width, c.height
        x, y = c.x - w/2, c.y - h/2
        self.log(f'c={self.cc} x={x:6.1f} y={y:6.1f} w={w:6.1f} h={h:6.1f} i={fmtl(self.i, FMTN)}')
        self.J2[-2] += 1
        self.dumpSprite()
        self.cursor = self.createSprite(-1, None, x, y, w, h, 8, g, why='cursor', kl=CCS, v=1, dbg=1)
        if QQ: self.setLLStyle(self.cc, CURRENT_STYLE)

    def setLLStyle(self, cc, style, dbg=0):
        p, l, c, t = self.cc2plct(cc)  ;  nc = self.n[C]
        bold, italic, color = 0, 0, self.klc[0]
        if   style == NORMAL_STYLE: color = self.klc[0]  ;  bold = 0  ;  italic = 0
        elif style == CURRENT_STYLE: color = CCS[8]      ;  bold = 0  ;  italic = 0
        elif style == SELECT_STYLE:  color = CCS[0]      ;  bold = 1  ;  italic = 1
        elif style == COPY_STYLE:    color = REDS[1]     ;  bold = 1  ;  italic = 1
        self.lcols[c + l * nc].color  = color
        self.lcols[c + l * nc].bold   = bold
        self.lcols[c + l * nc].italic = italic
        if dbg: self.log(f'cc={cc} p={p} l={l} c={c} t={t} style={style} bold={bold} italic={italic} color={color}')

    def resizeCursor(self):
        cc = self.cursorCol()
        c = self.tabs[cc]
        w, h = c.width, c.height
        x, y = c.x - w/2, c.y - h/2
        self.log(f'c={cc} x={x:6.1f} y={y:6.1f} w={w:6.1f} h={h:6.1f} i={fmtl(self.i, FMTN)}')
        self.cursor.update(x=x, y=y, scale_x=w/self.w[T], scale_y=h/self.h[T])
    ####################################################################################################################################################################################################
    def createSprite(self, j, p, x, y, w, h, kk, g, why, kl=None, v=0, dbg=0):
        self.J2[j] += 1   ;   why += JTEXTS[j] + f' {self.J2[j]}' if j >= 0 else ''
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

    def createLabel(self, j, p, x, y, w, h, kk, g, why, t='', kl=None, m=0, dbg=0):
        j1, j2 = self.J1, self.J2   ;   mp = 1 - CCC + len(p) % (self.n[C] + CCC)
        j2[j] += 1   ;   why += JTEXTS[j] + f' {j2[j]}'
        a, ax, ay = 'center', 'center', 'center' # left center right  # bottom baseline center top
        b = self.batch
        o, k, d, ii, n, s = self.fontParams()
        d = FONT_DPIS[d]
        n = FONT_NAMES[n]
        k = FONT_COLORS[kk % len(FONT_COLORS)] if kl is None else kl[kk]
        if m: t = [ t[:i] + '\n' + t[i:] for i in range(len(t), 0, -1) ]
        if j == LLC and not mp % 10: k = self.kll[0] #  ((len(p) - CCC + 1) % 10): k = self.kll[0]
        if len(p) > j2[j]:   self.log(f'ERROR Label Exists? len(p)={len(p)} j={j} j1={fmtl(j1)} j2={fmtl(j2)}')   # ;  self.quit('ERROR Unexpected if')
        lbl = pyglet.text.Label(t, font_name=n, font_size=s, bold=o, italic=ii, color=k, x=x, y=y, width=w, height=h, anchor_x=ax, anchor_y=ay, align=a, dpi=d, batch=b, group=g, multiline=m)
        self.labels.append(lbl)    ;    p.append(lbl)   # ;   self.log(f'Creating new j={j} j1={j1} len(p)={len(p)}')
        if dbg: self.dumpLabel(lbl, *self.ids(), *self.cnts(), why)
        return lbl
    ####################################################################################################################################################################################################
    def showLabel(self, i, p, j, g, t=None, k=None, v=1, dbg=VERBOSE):
        self.J1[j] = i  ;  self.J2[j] += 1
        why = 'show '
        if SPRITES and j < T: self.createSprite(j=j, p=p, x=0, y=0, w=self.w[j], h=self.h[j], kk=self.cci(i, k), g=g, why=why, kl=k, v=v, dbg=dbg)
        else:                 self.createLabel( j=j, p=p, x=0, y=0, w=0,         h=0,         kk=self.cci(i, k), g=g, why=why, t=t, kl=k, dbg=dbg)

    def hideLabel(self, p, j, t='???', dbg=1): #        c = self.E[j][n]
        c = p[j]    ;    ha = hasattr(c, 'text')
        x, y, w, h = c.x, c.y, c.width, c.height
        text = c.text if ha else '??'
        if type(c) is pyglet.sprite.Sprite: c.update(x=0, y=0, scale_x=0, scale_y=0)
        else:                               c.x, c.y, c.width, c.height = 0, 0, 0, 0
        if dbg: self.log(f'{t:5} {j+1:3} {hex(id(c))} {text:6} {x:7.2f} {y:7.2f} {w:7.2f} {h:7.2f} {c.text:6} {c.x:7.2f} {c.y:7.2f} {c.width:7.2f} {c.height:7.2f}', ind=0)
    ####################################################################################################################################################################################################
    def dumpSprites(self, why=''):
        self.log(f'BGN {self.fmtGeom()} {why}', ind=0)
        self.dumpSprite()
        np, nl, ns, nc, nt = self.n    ;    i, sp, sl, ss, sc = 0, 0, 0, 0, 0
        for p in range(np):
            sp += 1                 ; self.dumpSprite(self.sprites[i], *self.ids(), *self.cnts(), why=f'{why} Page {sp}') ; i += 1
            for l in range(nl):
                sl += 1             ; self.dumpSprite(self.sprites[i], *self.ids(), *self.cnts(), why=f'{why} Line {sl}') ; i += 1
                for s in range(ns):
                    ss += 1         ; self.dumpSprite(self.sprites[i], *self.ids(), *self.cnts(), why=f'{why} Sect {ss}') ; i += 1
                    for c in range(nc):
                        sc += 1     ; self.dumpSprite(self.sprites[i], *self.ids(), *self.cnts(), why=f'{why} Col {sc}' ) ; i += 1
        self.dumpSprite()
        self.log(f'END {self.fmtGeom()} {why}',ind=0)

    def dumpTabs(self, why='', dbg=VERBOSE):
        self.log('BGN')
        if dbg: self.log(f'BGN {self.fmtGeom()} {why}', ind=0)
        st, sn, sk = 0, 0, 0   ;   np, nl, ns, nc, nt = self.n   # ;   nc += CCC
        self.dumpLabel()
        for p in range(np):
            for l in range(nl):
                for s in range(ns):
                    for c in range(nc):
                        for t in range(nt):
                            if   s == 0:  self.dumpLabel(self.tabs[st],   *self.ids(), *self.cnts(), why=f'{why} Tab {st}')    ;  st += 1
                            elif s == 1:  self.dumpLabel(self.notes[sn],  *self.ids(), *self.cnts(), why=f'{why} Note {sn}')   ;  sn += 1
                            elif s == 2:  self.dumpLabel(self.chords[sk], *self.ids(), *self.cnts(), why=f'{why} Chord {sk}')  ;  sk += 1
        self.dumpLabel()
        if dbg: self.log(f'END {self.fmtGeom()} {why}', ind=0)
        self.log('END')

    def dumpCols(self, why='', dbg=VERBOSE):
        self.log('BGN')
        if dbg: self.log(f'BGN {self.fmtGeom()} {why}', ind=0)
        self.dumpLabel()
        for i in range(len(self.cols)):
            if SPRITES: self.dumpSprite(self.cols[i], *self.ids(), *self.cnts(), why=f'{why} Col {i+1}')
            else:       self.dumpLabel( self.cols[i], *self.ids(), *self.cnts(), why=f'{why} Col {i+1}')
        self.dumpLabel()
        if dbg: self.log(f'END {self.fmtGeom()} {why}', ind=0)
        self.log('END')

    def dumpLabels(self, why='', dbg=VERBOSE):
        self.initJ(why)
        np, nl, ns, nc, nt = self.n  ;  nc += CCC
        i, sp, sl, ss, sc, st, sn, si, sk = 0, 0, 0, 0, 0, 0, 0, 0, 0   ;   sqr, sqc = 0, 0
        self.log(f'BGN plsct={np} {nl} {ns} {nc} {nt}')
        if dbg: self.log(f'BGN {self.fmtGeom()} {why}', ind=0)
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
                                if   s == 0:  st += 1  ;  self.dumpLabel(self.labels[i], *self.ids(), *self.cnts(), why=f'{why} Tab {st}')    ;  i += 1
                                elif s == 1:  sn += 1  ;  self.dumpLabel(self.labels[i], *self.ids(), *self.cnts(), why=f'{why} Note {sn}' )  ;  i += 1
                                elif s == 2:  sk += 1  ;  self.dumpLabel(self.labels[i], *self.ids(), *self.cnts(), why=f'{why} Chord {sk}')  ;  i += 1
        else:
            for p in range(np):
                sp += 1                                ;   self.J1[P] = sp  ;  self.J2[P] += 1  ;  self.dumpLabel(self.labels[i], *self.ids(), *self.cnts(), why=f'{why} Page {sp}')   ;  i += 1
                for l in range(nl):
                    sl += 1                            ;   self.J1[L] = sl  ;  self.J2[L] += 1  ;  self.dumpLabel(self.labels[i], *self.ids(), *self.cnts(), why=f'{why} Line {sl}')   ;  i += 1
                    for q in range(QQ):
                        sqr += 1                       ; self.J1[LLR] = sqr ; self.J2[LLR] += 1 ;  self.dumpLabel(self.labels[i], *self.ids(), *self.cnts(), why=f'{why} LLR {sqr}')   ;  i += 1
                        for c in range(nc):
                            sqc += 1                   ; self.J1[LLC] = sqc ; self.J2[LLC] += 1 ;  self.dumpLabel(self.labels[i], *self.ids(), *self.cnts(), why=f'{why} LLC {sqc}')   ;  i += 1
                    for s in range(ns):
                        ss += 1                        ;   self.J1[S] = ss  ;  self.J2[S] += 1  ;  self.dumpLabel(self.labels[i], *self.ids(), *self.cnts(), why=f'{why} Sect {ss}')   ;  i += 1
                        for c in range(nc):
                            sc += 1                    ;   self.J1[C] = sc  ;  self.J2[C] += 1  ;  self.dumpLabel(self.labels[i], *self.ids(), *self.cnts(), why=f'{why} Col {sc}')    ;  i += 1
                            for t in range(nt):
                                if   s == 0:  st += 1  ;   self.J1[T] = st  ;  self.J2[T] += 1  ;  self.dumpLabel(self.labels[i], *self.ids(), *self.cnts(), why=f'{why} Tab {st}')    ;  i += 1
                                elif s == 1:  sn += 1  ;   self.J1[N] = sn  ;  self.J2[N] += 1  ;  self.dumpLabel(self.labels[i], *self.ids(), *self.cnts(), why=f'{why} Note {sn}')   ;  i += 1
                                elif s == 2:  sk += 1  ;   self.J1[K] = sk  ;  self.J2[K] += 1  ;  self.dumpLabel(self.labels[i], *self.ids(), *self.cnts(), why=f'{why} Chord {sk}')  ;  i += 1
        self.dumpLabel()  ;  self.dumpJ(why)
        if dbg: self.log(f'END {self.fmtGeom()} {why}', ind=0)
        self.log(f'END plsct={np} {nl} {ns} {nc} {nt}')
    ####################################################################################################################################################################################################
    def dumpSprite(self, b=None, sid=-1, lid=-1, p=-1, l=-1, s=-1, c=-1, t=-1, n=-1, i=-1, k=-1, o=-1, a=-1, d=-1, e=-1, f=-1, g=-1, r=-1, z=-1, why=''):
        if b is None: self.log(f' sid  lid p  l  s   c   t   n   i   k   z    x       y       w       h        v     identity   mx    my   red grn blu opc   why          group       parent', ind=0); return
        ff = '{:4} {:4} {} {:2} {:2} {:3} {:3} {:3} {:3} {:3} {:3} {:7.2f} {:7.2f} {:7.2f} {:7.2f}     {:1} {:13} {:5.3f} {:5.3f} {:3} {:3} {:3} {:3} {:12} {} {}'
        kk, oo, v, gg, pg    =    b.color, b.opacity, b.visible, b.group, b.group.parent   ;   ID = hex(id(b))   ;   z += r   ;   i += o + a + d + e + f + g
        x, y, w, h, iax, iay, m, mx, my, rot    =    b.x, b.y, b.width, b.height, b.image.anchor_x, b.image.anchor_y, b.scale, b.scale_x, b.scale_y, b.rotation
        fs = ff.format(sid, lid, p, l, s, c, t, n, i, k, z, x, y, w, h, v, ID, mx, my, kk[0], kk[1], kk[2], oo, why, gg, pg)
        self.log(fs, ind=0)
        assert(type(b) == pyglet.sprite.Sprite)

    def dumpLabel(self, b=None, sid=-1, lid=-1, p=-1, l=-1, s=-1, c=-1, t=-1, n=-1, i=-1, k=-1, o=-1, a=-1, d=-1, e=-1, f=-1, g=-1, r=-1, z=-1, why=''):
        if b is None: self.log(f' sid  lid p  l  s   c   t   n   i   k   z    x       y       w       h    text      identity  siz dpi b i red grn blu opc   why', ind=0) ; return
        x, y, w, h, fn, dd, zz, kk, bb, ii, tx    =    b.x, b.y, b.width, b.height, b.font_name, b.dpi, b.font_size, b.color, b.bold, b.italic, b.text  ;  ID = hex(id(b))   ;   z += r   ;   i += o + a + d + e + f + g
        ff = '{:4} {:4} {} {:2} {:2} {:3} {:3} {:3} {:3} {:3} {:3} {:7.2f} {:7.2f} {:7.2f} {:7.2f} {:6} {:13} {:2} {:3} {:1} {:1} {:3} {:3} {:3} {:3} {} '
        fs = ff.format(sid, lid, p, l, s, c, t, n, i, k, z, x, y, w, h, tx, ID, zz, dd, bb, ii, kk[0], kk[1], kk[2], kk[3], why)
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
#        if SPRITES: self._setFontParam(self.sprites, n, v, m)
#            if QQ:  self._setFontParam(self.lrows, n, v, m) ; self._setFontParam(self.lcols, n, v, m)
#            if CCC: self._setFontParam(self.snos, n, v, m)  ; self._setFontParam(self.snas, n, v, m) ; self._setFontParam(self.capsA, n, v, m) ; self._setFontParam(self.capsB, n, v, m) ; self._setFontParam(self.lstrs, n, v, m) ; self._setFontParam(self.lcaps, n, v, m)
#            self._setFontParam(self.tabs,   n, v, m)
#            self._setFontParam(self.notes,  n, v, m)
#            self._setFontParam(self.chords, n, v, m)
        self._setFontParam(self.labels, n, v, m)
        self.setCaption(self.fmtf())

    @staticmethod
    def _setFontParam(p, n, v, m):
        for j in range(len(p)):
            setattr(p[j], n, FONT_NAMES[v] if m == 'fontNameIndex' else FONT_COLORS[v] if m == 'fontColorIndex' else FONT_DPIS[v] if m == 'fontDpiIndex' else v)
    ####################################################################################################################################################################################################
    def cursorCol(self): return self.plct2cc(*self.j2())
    def normalizeCC(self, cc): return (cc // self.tpc) * self.tpc

    def plct2cc(self, p, l, c, t, dbg=0):
        tpp, tpl, tps, tpc = self.tpz()
        cc = p * tpp + l * tpl + c * tpc + t
        lenT = len(self.tabs)   ;   ccm = cc % lenT
        if dbg: self.log(f'plct2cc({p} {l} {c} {t}) {tpp} {tpl} {tpc} ({p*tpp} +{l*tpl} +{c*tpc} +{t}) % {lenT} return {ccm}')
        return ccm

    def cc2plct(self, cc, dbg=0):
        tpp, tpl, tps, tpc = self.tpz()
        p =  cc // tpp
        l = (cc - p * tpp) // tpl
        c = (cc - p * tpp - l * tpl) // tpc
        t =  cc - p * tpp - l * tpl - c * tpc
        p = p % self.n[P]
        if dbg: self.log(f'cc2plct({cc}) return {p} {l} {c} {t}')
        return p, l, c, t

    def cn2cc(self, cn):       return cn * self.tpc
#    def cn2plct(self, cn):
    def cc2cn(self, cc):       return cc // self.tpc                                                ;  # ;  self.log(f'({cc}) cc // tpc return {cn}')  ;  return cn
    def plc2cn(self, p, l, c): return (p *  self.tpp // self.tpc) + (l * self.tpl // self.tpc) + c  ;  # ;  self.log(f'({p} {l} {c}) return {cn}')     ;  return cn

    def cn2txt(self, cn):  #  usefull? re-name cn2tabtxt()
        cc = self.cn2cc(cn)
        p, l, c, t = self.cc2plct(cc)
        txt = self.data[p][l][c]
        self.log(f'cn={cn} cc={cc} plct={p} {l} {c} txt={txt}')

    def setCaption(self, msg, dbg=0):
        if dbg: self.log(f'{msg}')
        self.set_caption(msg)
    ####################################################################################################################################################################################################
    def on_mouse_release(self, x, y, button, modifiers, dbg=1):
        np, nl, ns, nc, nt = self.n    ;  nc += CCC   ;   file = None
        y0 = y   ;   y = self.hh - y   ;   n = nl * ns * nt + ns * QQ   ;  m = int(ns*nt) + QQ
        w = self.ww/nc       ;  h = self.hh/n         ;   d = int(y/h) - QQ
        l = int(d/m)         ;  c  = int(x/w) - CCC   ;   t = d - (l * m)  ;  p = 0
        if dbg: self.log(f'BGN button={button} modifiers={modifiers} txt={self.tabs[self.cc].text}', file=file)
        if dbg: self.log(f'x={x} y0={y0:4} w={w:6.2f} h={h:6.2f}')
        if dbg: self.log(f'y={y:4} n={n} m={m} d={d}')
        if dbg: self.log(f'before plct {p} {l} {c} {t}')
        self.moveTo(f'MOUSE RELEASE', p, l, c, t)
        if dbg: self.log(f'after  plct {fmtl(self.j2(), d1="", d2="")}')
    ####################################################################################################################################################################################################
    def kbkEvntTxt(self): return f'{self.kbk:8} {self.symb:8} {self.symbStr:14} {self.mods:2} {self.modsStr:16}'
    ####################################################################################################################################################################################################
    def on_key_press(self, symb, mods, dbg=0): # avoid these
        self.symb, self.mods, self.symbStr, self.modsStr = symb, mods, pygwink.symbol_string(symb), pygwink.modifiers_string(mods)
        self.kbk = self.symbStr  ;  kbk = self.kbk
        if dbg: self.log(f'BGN {self.kbkEvntTxt()}')
        if   kbk == 'A' and self.isCtrlShift(mods):    self.toggleArrow(     '@ ^ A', v=1)
        elif kbk == 'A' and self.isCtrl(     mods):    self.toggleArrow(     '@   A', v=0)
        elif kbk == 'B' and self.isCtrlShift(mods):    self.toggleBlank(     '@ ^ B')
        elif kbk == 'B' and self.isCtrl(     mods):    self.toggleBlank(     '@   B')
        elif kbk == 'C' and self.isCtrlShift(mods):    self.copyTabs(        '@ ^ C')
        elif kbk == 'C' and self.isCtrl(     mods):    self.copyTabs(        '@   C')
        elif kbk == 'D' and self.isCtrlShift(mods):    self.deleteTabs(      '@ ^ D')
        elif kbk == 'D' and self.isCtrl(     mods):    self.deleteTabs(      '@   D')
        elif kbk == 'E' and self.isCtrlShift(mods):    self.eraseTabs(       '@ ^ E')
        elif kbk == 'E' and self.isCtrl(     mods):    self.eraseTabs(       '@   E')
        elif kbk == 'F' and self.isCtrlShift(mods):    self.toggleFullScreen('@ ^ F')
        elif kbk == 'F' and self.isCtrl(     mods):    self.toggleFlatSharp( '@   F')
        elif kbk == 'G' and self.isCtrlShift(mods):    self.move2LastTab(    '@ ^ G', page=1)
        elif kbk == 'G' and self.isCtrl(     mods):    self.move2LastTab(    '@   G', page=0)
        elif kbk == 'H' and self.isCtrlShift(mods):    self.move2FirstTab(   '@ ^ H', page=1)
        elif kbk == 'H' and self.isCtrl(     mods):    self.move2FirstTab(   '@   H', page=0)
        elif kbk == 'I' and self.isCtrlShift(mods):    self.insertSpace(     '@ ^ I')
        elif kbk == 'I' and self.isCtrl(     mods):    self.insertSpace(     '@   I')
        elif kbk == 'J' and self.isCtrlShift(mods):    self.jump(            '@ ^ J', a=1)
        elif kbk == 'J' and self.isCtrl(     mods):    self.jump(            '@   J', a=0)
        elif kbk == 'K' and self.isCtrlShift(mods):    self.toggleTabs(      '@ ^ K', KK)
        elif kbk == 'K' and self.isCtrl(     mods):    self.toggleTabs(      '@   K', KK)
        elif kbk == 'L' and self.isCtrlShift(mods):    self.toggleLLRows(    '@ ^ L')
        elif kbk == 'L' and self.isCtrl(     mods):    self.toggleLLRows(    '@   L')
        elif kbk == 'M' and self.isCtrlShift(mods):    self.toggleRLCols(    '@ ^ M')
        elif kbk == 'M' and self.isCtrl(     mods):    self.toggleRLCols(    '@   M')
        elif kbk == 'N' and self.isCtrlShift(mods):    self.toggleTabs(      '@ ^ N', NN)
        elif kbk == 'N' and self.isCtrl(     mods):    self.toggleTabs(      '@   N', NN)
        elif kbk == 'O' and self.isCtrlShift(mods):    self.toggleCursorMode('@ ^ O')
        elif kbk == 'O' and self.isCtrl(     mods):    self.toggleCursorMode('@   O')
        elif kbk == 'Q' and self.isCtrlShift(mods):    self.quit(            '@ ^ Q', code=1)
        elif kbk == 'Q' and self.isCtrl(     mods):    self.quit(            '@   Q', code=0)
        elif kbk == 'R' and self.isCtrlShift(mods):    self.toggleChordNames('@ ^ R', every=1)
        elif kbk == 'R' and self.isCtrl(     mods):    self.toggleChordNames('@   R', rev=0)
        elif kbk == 'S' and self.isCtrlShift(mods):    self.shiftTabs(       '@ ^ S')
#        elif kbk == 'S' and self.isCtrl(     mods):    self.saveDataFile(    '@   S')
        elif kbk == 'S' and self.isCtrl(     mods):    self.swapTab(         '@   S', txt='')
        elif kbk == 'T' and self.isCtrlShift(mods):    self.toggleTabs(      '@ ^ T', TT)
        elif kbk == 'T' and self.isCtrl(     mods):    self.toggleTabs(      '@   T', TT)
        elif kbk == 'U' and self.isCtrlShift(mods):    self.resetTabs(       '@ ^ U')
        elif kbk == 'U' and self.isCtrl(     mods):    self.resetTabs(       '@   U')
#        elif kbk == 'V' and self.isCtrlAlt(  mods):    self.pasteTabs(       '@ & V', hc=0, kk=1)
        elif kbk == 'V' and self.isCtrlShift(mods):    self.pasteTabs(       '@ ^ V', kk=1)
        elif kbk == 'V' and self.isCtrl(     mods):    self.pasteTabs(       '@   V', kk=0)
        elif kbk == 'W' and self.isCtrlShift(mods):    self.swapTabs(        '@ & W')
        elif kbk == 'W' and self.isCtrl(     mods):    self.swapTabs(        '@ & W')
        elif kbk == 'X' and self.isCtrlShift(mods):    self.cutTabs(         '@ ^ X')
        elif kbk == 'X' and self.isCtrl(     mods):    self.cutTabs(         '@   X')
        elif kbk == 'SPACE' and not self.isParsing():  self.autoMove(        'SPACE')
        elif kbk == 'ESCAPE':                          self.unselectAll(     'ESCAPE')
        elif kbk == 'TAB'       and self.isCtrl(mods): self.setCHVMode(      '@ TAB',       MELODY, LEFT)
        elif kbk == 'TAB':                             self.setCHVMode(      '  TAB',       MELODY, RIGHT)
        elif kbk == 'ENTER'     and self.isCtrl(mods): self.setCHVMode(      '@ ENTER',     CHORD,       v=DOWN)
        elif kbk == 'ENTER':                           self.setCHVMode(      '  ENTER',     CHORD,       v=UP)
#        elif kbk == 'SLASH'     and self.isCtrl(mods): self.setTab(          '@ SLASH', '/')
#        elif kbk == 'SLASH':                           self.setTab(          '  SLASH', '/')
#        elif kbk == 'BACKSLASH' and self.isCtrl(mods): self.setTab(          '@ BACKSLASH', '\\')
#        elif kbk == 'BACKSLASH':                       self.setTab(          '  BACKSLASH', '\\')
#        elif kbk == 'SLASH'     and self.isCtrl(mods): self.setCHVMode(      '@ SLASH',     ARPG,   LEFT,  DOWN)
#        elif kbk == 'SLASH':                           self.setCHVMode(      '  SLASH',     ARPG,   RIGHT, UP)
#        elif kbk == 'BACKSLASH' and self.isCtrl(mods): self.setCHVMode(      '@ BACKSLASH', ARPG,   LEFT,  UP)
#        elif kbk == 'BACKSLASH':                       self.setCHVMode(      '  BACKSLASH', ARPG,   RIGHT, DOWN)
    ####################################################################################################################################################################################################
        elif kbk == 'B' and self.isAltShift(mods):     self.setFontParam('bold',   not self.fontBold,                               'fontBold')
        elif kbk == 'B' and self.isAlt(     mods):     self.setFontParam('bold',   not self.fontBold,                               'fontBold')
        elif kbk == 'C' and self.isAltShift(mods):     self.setFontParam('color',     (self.fontColorIndex + 1) % len(FONT_COLORS), 'fontColorIndex')
        elif kbk == 'C' and self.isAlt(     mods):     self.setFontParam('color',     (self.fontColorIndex - 1) % len(FONT_COLORS), 'fontColorIndex')
        elif kbk == 'D' and self.isAltShift(mods):     self.setFontParam('dpi',       (self.fontDpiIndex   + 1) % len(FONT_DPIS),   'fontDpiIndex')
        elif kbk == 'D' and self.isAlt(     mods):     self.setFontParam('dpi',       (self.fontDpiIndex   - 1) % len(FONT_DPIS),   'fontDpiIndex')
        elif kbk == 'I' and self.isAltShift(mods):     self.setFontParam('italic', not self.fontItalic,                             'fontItalic')
        elif kbk == 'I' and self.isAlt(     mods):     self.setFontParam('italic', not self.fontItalic,                             'fontItalic')
        elif kbk == 'N' and self.isAltShift(mods):     self.setFontParam('font_name', (self.fontNameIndex + 1)  % len(FONT_NAMES),  'fontNameIndex')
        elif kbk == 'N' and self.isAlt(     mods):     self.setFontParam('font_name', (self.fontNameIndex - 1)  % len(FONT_NAMES),  'fontNameIndex')
        elif kbk == 'S' and self.isAltShift(mods):     self.setFontParam('font_size', (self.fontSize      + 1)  % 52,               'fontSize')
        elif kbk == 'S' and self.isAlt(     mods):     self.setFontParam('font_size', (self.fontSize      - 1)  % 52,               'fontSize')
        elif dbg:   self.log(f'Unexpected {self.kbkEvntTxt()}')
        if dbg: self.log(f'END {self.kbkEvntTxt()}')
    ####################################################################################################################################################################################################
    def on_key_release(self, symb, mods, dbg=0):
        self.symb, self.mods, self.symbStr, self.modsStr = symb, mods, pygwink.symbol_string(symb), pygwink.modifiers_string(mods)
        self.kbk = self.symbStr  # ;  kbk = self.kbk   ;   why='on_key_release'
        if dbg: self.log(f'{self.kbkEvntTxt()}')
    ####################################################################################################################################################################################################
    def on_text(self, text, dbg=0): # use for entering strings not for motion
        self.kbk = text
        if dbg: self.log(f'BGN {self.kbkEvntTxt()} swapping={self.swapping}')
        if   self.shiftingTabs:                              self.shiftTabs(  'on_text', text)
        elif self.jumping:                                   self.jump(       'on_text', text, self.jumpAbs)
        elif self.inserting:                                 self.insertSpace('on_text', text)
        elif self.swapping:                                  self.swapTab(    'on_text', text)
        elif self.isTab(self.kbk):                           self.setTab(     'on_text', self.kbk)
        elif self.kbk == '$' and self.isShift(self.mods):    self.snapshot()
        if dbg: self.log(f'END {self.kbkEvntTxt()} swapping={self.swapping}')
    ####################################################################################################################################################################################################
    def on_text_motion(self, motion, dbg=0): # use for motion not strings
        self.kbk = motion   ;   p, l, s, c, t = self.j()  ;  np, nl, ns, nc, nt = self.n
        if dbg: self.log(f'BGN {self.kbkEvntTxt()}')
        if   self.isCtrlAltShift(self.mods):                 self.log(f'ALT CTRL SHIFT ({         motion})')
        elif self.isCtrlAlt(self.mods):
            if   motion == 1:                                self.unselectTabs(f'ALT CTRL LEFT ({ motion})',  nt)
            elif motion == 2:                                self.unselectTabs(f'ALT CTRL RIGHT ({motion})', -nt)
            else:                                            self.log(         f'ALT CTRL ({      motion})')
        elif self.isAltShift(self.mods):                     self.log(         f'ALT SHIFT ({     motion})')
        elif self.isCtrlShift(self.mods):                    self.log(         f'CTRL SHIFT ({    motion})')
        elif self.isShift(self.mods):                        self.log(         f'SHIFT ({         motion})')
        elif self.isAlt(self.mods):
            if   motion == pygwink.MOTION_UP:                self.moveUp(      f'ALT UP ({        motion})')
            elif motion == pygwink.MOTION_DOWN:              self.moveDown(    f'ALT DOWN ({      motion})')
            elif motion == pygwink.MOTION_LEFT:              self.moveLeft(    f'ALT LEFT ({      motion})')
            elif motion == pygwink.MOTION_RIGHT:             self.moveRight(   f'ALT RIGHT ({     motion})')
            elif motion == pygwink.MOTION_BEGINNING_OF_LINE: self.move(        f'ALT HOME ({      motion})', -nt *  c)
            elif motion == pygwink.MOTION_END_OF_LINE:       self.move(        f'ALT END ({       motion})',  nt * (nc - self.i[C]))
            elif motion == pygwink.MOTION_PREVIOUS_PAGE:     self.moveTo(      f'ALT PAGE UP ({   motion})', p, 0,    c, 0)     # move up   to top    tab on top    line
            elif motion == pygwink.MOTION_NEXT_PAGE:         self.moveTo(      f'ALT PAGE DOWN ({ motion})', p, nl-1, c, nt-1)  # move down to bottom tab on bottom line
            else:                                            self.log(         f'ALT ({           motion})')
        elif self.isCtrl(self.mods):
            if   motion == pygwink.MOTION_PREVIOUS_WORD:     self.selectTabs(  f'CTRL LEFT ({     motion})', -nt)
            elif motion == pygwink.MOTION_NEXT_WORD:         self.selectTabs(  f'CTRL RIGHT ({    motion})',  nt)
#            elif motion == pygwink.MOTION_BEGINNING_OF_LINE: self.quit('CTRL + MOTION_BEGINNING_OF_LINE')
#            elif motion == pygwink.MOTION_END_OF_LINE:       self.quit('CTRL + MOTION_END_OF_LINE')
            elif motion == pygwink.MOTION_BEGINNING_OF_FILE: self.log(         f'CTRL + MOTION_BEGINNING_OF_FILE={pygwink.MOTION_BEGINNING_OF_FILE}=CTRL HOME')
            elif motion == pygwink.MOTION_END_OF_FILE:       self.log(         f'CTRL + MOTION_END_OF_FILE={pygwink.MOTION_END_OF_FILE}=CTRL END')
            else:                                            self.log(         f'CTRL ({          motion})')
        if self.mods == 0:
            if   motion == pygwink.MOTION_UP:                self.move(        f' UP ({           motion})', -1)
            elif motion == pygwink.MOTION_DOWN:              self.move(        f' DOWN ({         motion})',  1)
            elif motion == pygwink.MOTION_LEFT:              self.move(        f' LEFT ({         motion})', -nt)
            elif motion == pygwink.MOTION_RIGHT:             self.move(        f' RIGHT ({        motion})',  nt)
#            elif motion == pygwink.MOTION_PREVIOUS_WORD:     self.quit(f 'MOTION_PREVIOUS_WORD={pygwink.MOTION_PREVIOUS_WORD}')
#            elif motion == pygwink.MOTION_NEXT_WORD:         self.quit(f 'MOTION_NEXT_WORD={pygwink.MOTION_NEXT_WORD}')
            elif motion == pygwink.MOTION_BEGINNING_OF_LINE: self.move(        f' HOME ({         motion})', -nt *  c)
            elif motion == pygwink.MOTION_END_OF_LINE:       self.move(        f' END ({          motion})',  nt * (nc - self.i[C]))
            elif motion == pygwink.MOTION_PREVIOUS_PAGE:     self.moveUp(      f' PAGE UP ({      motion})')  # move up   to top    of line, wrap down to bottom of prev line
            elif motion == pygwink.MOTION_NEXT_PAGE:         self.moveDown(    f' PAGE DOWN ({    motion})')  # move down to bottom tab on same line, wrap to next line
#            elif motion == pygwink.MOTION_PREVIOUS_PAGE:     self.move(        f' PAGE UP ({      motion})', -nt *  nc)  # move up   one line to same tab
#            elif motion == pygwink.MOTION_NEXT_PAGE:         self.move(        f' PAGE DOWN ({    motion})',  nt *  nc)  # move down one line to same tab
#            elif motion == pygwink.MOTION_BEGINNING_OF_FILE: self.quit(f 'MOTION_BEGINNING_OF_FILE={pygwink.MOTION_BEGINNING_OF_FILE}')
#            elif motion == pygwink.MOTION_END_OF_FILE:       self.quit(f 'MOTION_END_OF_FILE={pygwink.MOTION_END_OF_FILE}')
            elif motion == pygwink.MOTION_BACKSPACE:         self.setTab(      f'BACKSPACE ({     motion})', self.tblank, rev=1)
            elif motion == pygwink.MOTION_DELETE:            self.setTab(      f'DELETE ({        motion})', self.tblank)
            else:                                            self.log(         f'({               motion}) ???')
        if dbg: self.log(f'END {self.kbkEvntTxt()}')
    ####################################################################################################################################################################################################
    def move2LastTab(self, how, page=0):
        if page: i = len(self.tabs) - 1
        else: i = self.i[L] * self.tpl - 1
        while not self.isFret(self.tabs[i].text): i -= 1
        p, l, c, t = self.cc2plct(i)
        self.moveTo(how, p, l, c, t)
        self.log(f'{how} plct {p} {l} {c} {t}')
    def move2FirstTab(self, how, page=0):
        if page: i = 0
        else: i = self.j()[L] * self.tpl - 1
        while not self.isFret(self.tabs[i].text): i += 1
        p, l, c, t = self.cc2plct(i)
        self.moveTo(how, p, l, c, t)
        self.log(f'{how} plct {p} {l} {c} {t}')

    def moveDown(self, how, dbg=1):
        p, l, s, c, t = self.j()  ;  nt = self.n[T] - 1
        if dbg: self.log(f'BGN {how} plct {p} {l} {c} {t}')
        if t < nt: self.moveTo(how, p, l,   c, nt)      # move down to bottom of      line
        else:      self.moveTo(how, p, l+1, c, 0)       # move down to top    of next line, wrap up to first line
        if dbg: self.log(f'END {how} plct {fmtl(self.j2(), d1="", d2="")}')
    def moveUp(self, how, dbg=1):
        p, l, s, c, t = self.j()  ;  nt = self.n[T] - 1
        if dbg: self.log(f'BGN {how} plct {p} {l} {c} {t}')
        if t:      self.moveTo(how, p, l,    c, 0)      # move up   to top    of      line,    wrap to bottom line
        else:      self.moveTo(how, p, l-1,  c, nt)     # move up   to bottom of prev line
        if dbg: self.log(f'END {how} plct {fmtl(self.j2(), d1="", d2="")}')
    def moveRight(self, how, dbg=1):
        p, l, s, c, t = self.j()  ;  nc = self.n[C] - 1
        if dbg: self.log(f'BGN {how} plct {p} {l} {c} {t}')
        if c < nc: self.moveTo(how, p, l,  nc, t)       # move right to end of line
        else:      self.moveTo(how, p, l+1, 0, t)       # wrap left & down (up) to bgn of next (top) line
        if dbg: self.log(f'END {how} plct {fmtl(self.j2(), d1="", d2="")}')
    def moveLeft(self, how, dbg=1):
        p, l, s, c, t = self.j()  ;  nc = self.n[C] - 1
        if dbg: self.log(f'BGN {how} plct {p} {l} {c} {t}')
        if c:      self.moveTo(how, p, l,   0,  t)      # move left  to bgn of line
        else:      self.moveTo(how, p, l-1, nc, t)      # wrap right & up (down) to end of prev (bottom) line
        if dbg: self.log(f'END {how} plct {fmtl(self.j2(), d1="", d2="")}')

    def moveCursor(self, ss=0):
        self.setLLStyle(self.cc, SELECT_STYLE if ss else NORMAL_STYLE)
        self.cc = self.cursorCol()
        tab = self.tabs[self.cc]
        x = tab.x - tab.width/2   ;   y = tab.y - tab.height/2
        self.cursor.update(x=x, y=y)
        self.setLLStyle(self.cc, CURRENT_STYLE)

#        if not self.SNAP0: t = self.tabs[self.cc]  ;  self.snapshot(f'pre-move() k={k:4} kk={self.cc:3} {fmtl(self.i, FMTN)} text={t.text} {t.x:6.2f} {t.y:6.2f}')  ;  self.SNAP0 = 1
#        self.armSnap = f'move() k={k:4} kk={kk:4} {fmtl(self.i, FMTN)} text={self.tabs[self.cc].text} {x:6.2f} {y:6.2f}'
    def moveTo(self, how, p, l, c, t, ss=0, dbg=1):
        if dbg:    self.log(f'BGN {how} plct {fmtl(self.j2(), d1="", d2="")} cc={self.cursorCol()}')
        self._moveTo(p, l, c, t)
        self.moveCursor(ss)
        if dbg:    self.log(f'END {how} plct {fmtl(self.j2(), d1="", d2="")} cc={self.cc}')

    def move(self, how, k, ss=0, dbg=1):   #  text={self.tabs[self.cc].text} {x:6.2f} {y:6.2f}') # , file=sys.stdout)
        if dbg:    self.log(f'BGN {how} plct {fmtl(self.j2(), d1="", d2="")} cc={self.cursorCol()} k={k}')
        if k:
            p,  l,  c,  t = self.j2()
            self._moveTo(p, l, c, t, n=k)
            self.moveCursor(ss)
        if dbg:    self.log(f'END {how} plct {fmtl(self.j2(), d1="", d2="")} cc={self.cursorCol()} k={k}')

    def _moveTo(self, p, l, c, t, n=0, dbg=1):
        if dbg: self.log(f'BGN n={n} plct {p} {l} {c} {t}')
        np, nl, ns, nc, nt = self.n
        t2        =       n  + t
        c2        = t2 // nt + c
        l2        = c2 // nc + l
        p2        = l2 // nl + p
        self.i[T] = t2  % nt + 1
        self.i[C] = c2  % nc + 1
        self.i[L] = l2  % nl + 1
        self.i[P] = p2  % np + 1
        if dbg: self.log(f'END n={n} plct {p} {l} {c} {t} p2l2c2t2 {p2} {l2} {c2} {t2}')

    def autoMove(self, how, dbg=1):
        self.log(f'BGN {how}')
        ha = 1 if self.hArrow else -1
        va = 1 if self.vArrow else -1
        nt, it = self.n[T], self.i[T]
        mmDist = ha * nt
        cmDist = va
        amDist = mmDist + cmDist
        if dbg: self.dumpCursorArrows(f'{how} M={mmDist} C={cmDist} A={amDist}')
        if      self.csrMode == MELODY:                                     self.move(how, mmDist)
        elif    self.csrMode == CHORD:
            if   it == 1 and self.vArrow  == UP   and self.hArrow == RIGHT: self.move(how,   nt*2-1)
            elif it == 6 and self.vArrow  == DOWN and self.hArrow == RIGHT: self.move(how, -(nt*2-1))
            else:                                                           self.move(how, cmDist)
        elif    self.csrMode == ARPG:                                       self.move(how, amDist)
        self.log(f'END {how}')

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
    def jump(self, how, txt='0', a=0):
        cc = self.cursorCol()   ;   self.jumpAbs = a
        self.log(f'{how} txt={txt} a={a} cc={cc} jt={self.jumpAbs} {fmtl(self.i)}')
        if not self.jumping:                  self.jumping = 1
        elif txt.isdecimal():                 self.jumpStr += txt
        elif txt == '-' and not self.jumpStr: self.jumpStr += txt
        elif txt == ' ':
            self.log(f'{how} txt={txt} a={a} cc={cc} jt={self.jumpAbs} jumpStr={self.jumpStr} {fmtl(self.i)}')
            jcc = self.n[T] * int(self.jumpStr)
            self.jumping = 0   ;    self.jumpStr = ''
            self.move(how, jcc - 1 - a * cc)
            self.log(f'{how} txt={txt} a={a} cc={cc} jt={self.jumpAbs} jcc={jcc} moved={jcc - 1 - a * cc} {fmtl(self.i)}')
    ####################################################################################################################################################################################################
    def dumpSelectTabs(self, why): self.log(f'{why} {fmtl(self.skeys, ll=1)} {fmtl(list(self.smap.values()))}')

    def unselectAll(self, how, dbg=VERBOSE):
        for i in range(len(self.skeys)-1, -1, -1):
            k = self.skeys[i]
            if dbg: self.log(f'{how} i={i} k={k}')
            self.unselectTabs(how, m=0, k=k)

    def unselectTabs(self, how, m, k=None, dbg=VERBOSE):
        cc = self.cursorCol()   ;   nt = self.n[T]
        if k is None: k = self.normalizeCC(cc)
        self.setLLStyle(cc, NORMAL_STYLE)
        if dbg: self.dumpSelectTabs(f'BGN {how} m={m} cc={cc} k={k} cn={self.cc2cn(cc) + 1}')
        for t in range(nt):
            tab   = self.tabs  [k + t]  ;    tab.color = self.kt[0]
            note  = self.notes [k + t]  ;   note.color = self.kn[0]
            chord = self.chords[k + t]  ;  chord.color = self.kk[0]
        if k in self.skeys: self.skeys.remove(k)    ;    self.smap.pop(k)  #  crashes
        elif dbg:           self.log(f'key={k} not found in skeys={fmtl(self.skeys)}')
        if m:   self.move(how, m)
        if dbg: self.dumpSelectTabs(f'END {how} m={m} cc={cc} k={k} cn={self.cc2cn(cc) + 1}')

    def selectTabs(self, how, m=0, cc=None):
        if cc is None: cc = self.cursorCol()
        nt = self.n[T]  ;  text = ''
        k = self.normalizeCC(cc)
        if k in self.smap: self.log(f'k={k} already in smap returning')   ;   return
        self.dumpSelectTabs(f'BGN {how} m={m} cc={cc} k={k} cn={self.cc2cn(cc) + 1}')
        self.skeys.append(k)   # ;   self.sset.add(k)
        for t in range(nt):
            tab   = self.tabs  [k + t]  ;    tab.color = CCS[0]
            note  = self.notes [k + t]  ;   note.color = CCS[0]
            chord = self.chords[k + t]  ;  chord.color = CCS[0]
            text += tab.text
        self.smap[k] = text
        self.move(how, m, ss=1)
        self.dumpSelectTabs(f'END {how} m={m} cc={cc} k={k} cn={self.cc2cn(cc) + 1}')

    def copyTabs(self, how, dbg=VERBOSE):
        self.dumpSelectTabs(f'BGN {how}')   ;   nt = self.n[T]  ;   text = ''
        for k in self.skeys:
            self.setLLStyle(k, NORMAL_STYLE)
            for t in range(nt):
                tab    = self.tabs  [k + t]  ;    tab.color = self.k[T][0]
                note   = self.notes [k + t]  ;   note.color = self.k[N][0]
                chord  = self.chords[k + t]  ;  chord.color = self.k[K][0]
                if dbg: text += tab.text
            if dbg: text += ' '
        if dbg: self.log(f'text={text}')
        self.dumpSelectTabs(f'END {how}')
    ####################################################################################################################################################################################################
    def cutTabs(self, how): self.log('BGN Cut = Copy + Delete')  ;  self.copyTabs(how)  ;  self.log('Cut = Copy + Delete')  ;  self.deleteTabs(how, cut=1)  ;  self.log('END Cut = Copy + Delete')
    ####################################################################################################################################################################################################
    def deleteTabs(self, how, cut=0, dbg=VERBOSE):
        self.dumpSelectTabs(f'BGN {how} cut={cut}')   ;   nt = self.n[T]
        for i, (k,v) in enumerate(self.smap.items()):
            if dbg: self.log(f'i={i} k={k} v={v}')
            self.setLLStyle(k, NORMAL_STYLE)
            for t in range(nt):
                p, l, c, r = self.cc2plct(k + t, dbg=0)
                self.tabs  [k + t].color = self.k[T][0]
                self.notes [k + t].color = self.k[N][0]
                self.chords[k + t].color = self.k[K][0]
                self.setDTNK(self.tblank, k + t, p, l, c, t, uk=1 if t == nt - 1 else 0)  # call with uk=1 only once per column or tpc
        if not cut: self.unselectAll('deleteTabs()')
        self.dumpSelectTabs(f'END {how} cut={cut}')
        self.dataHasChanged = 1

    def pasteTabs(self, how, kk=0, dbg=VERBOSE):
        cc = self.cursorCol()   ;  nt = self.n[T]
        ntc = self.normalizeCC(cc)   ;  kt = 0
        smap, skeys = self.smap, self.skeys
        p, l, s, c, r = self.j()
        self.dumpSelectTabs(f'BGN {how} kk={kk} cc={cc} ntc={ntc} cn={self.cc2cn(cc) + 1} plcr {p} {l} {c} {r}')
        for i, (k, v) in enumerate(smap.items()):
            text = v
            if not i: dk = 0
            elif kk:  dk = i * nt
            else:     dk = skeys[i] - skeys[0]
            if dbg: self.log(f'i={i} k={k} v={v} text={text} kk={kk} dk={dk}')
            for t in range(nt):
                kt = (ntc + dk + t) % self.tpp
                p, l, c, r = self.cc2plct(kt, dbg=0)
                self.setDTNK(text[t], kt, p, l, c, t, uk=1 if t == nt - 1 else 0)  # call with uk=1 only once per column or tpc
            if dbg: self.log(f'smap[{k}]={text} kt={kt} kk={kk} dk={dk}')
#        if not hc: self.unselectAll('pasteTabs()')
#        elif dbg:  self.log(f'holding a copy of smap and skeys')
#        self.dumpSelectTabs(f'END {how} hc={hc} kk={kk} cc={cc} ntc={ntc} cn={self.cc2cn(cc) + 1}')
        self.dumpSelectTabs(f'END {how} kk={kk} cc={cc} ntc={ntc} cn={self.cc2cn(cc) + 1} plcr {p} {l} {c} {r}')
        self.dataHasChanged = 1

    def swapTabs(self, how):
        nk = len(self.skeys)   ;   nk2 = nk // 2
        for i in range(nk2):
            k1 = self.skeys[i]
            k2 = self.skeys[nk - 1 - i]
            text1 = self.smap[k1]
            text2 = self.smap[k2]
            self.smap[k1] = text2
            self.smap[k2] = text1
        self.pasteTabs(how)

    def insertSpace(self, how, txt='0', dbg=1): # need to update tabCols?
        cc = self.cursorCol()   ;   c0 = self.cc2cn(cc)
        if not self.inserting: self.inserting = 1
        elif txt.isdecimal():  self.insertStr += txt
        elif txt == ' ':
            self.inserting = 0
            width = int(self.insertStr)
            tcs = sorted(self.tabCols)
            tcs.append(self.n[C] * self.n[L] - 1)
            tcs = [t + 1 for t in tcs]
            if dbg: self.log(f'{how} Searching for space to insert {width} cols starting at col {c0}')
            self.log(f'{fmtl(tcs, ll=1)} insertSpace', ind=0)
            found, c1, c2 = 0, 0, None   ;   self.insertStr = ''
            for c2 in tcs:
                if dbg: self.log(f'w c0 c1 c2 = {width} {c0} {c1} {c2}')
                if c2 > c0 + width and c2 > c1 + width: found = 1  ;  break
                c1 = c2
            if not found: self.log(f'{how} starting at col {c0} No room to insert {width} cols before end of page at col {tcs[-1]+1}')  ;   return
            self.log(f'{how} starting at col {c0} Found a gap {width} cols wide between cols {c1} and {c2}')
            self.log(f'select cols {c0} ... {c1}, cut cols, move ({width} - {c1} + {c0})={width-c1+c0} cols, paste cols')
            [ self.selectTabs(how, self.tpc) for _ in range(c1 - c0) ]
            self.cutTabs(how)
            self.move(how, (width - c1 + c0) * self.tpc)
            self.pasteTabs(how)

    def shiftTabs(self, how, nf=0):
        self.dumpSelectTabs(f'BGN {how} shiftingTabs={self.shiftingTabs} nf={nf}')
        if not self.shiftingTabs:
            self.shiftingTabs = 1
            for i, (k,v) in enumerate(self.smap.items()):
                self.setLLStyle(k, NORMAL_STYLE)
        elif nf == '-': self.shiftSign = -1
        elif self.isFret(nf):
            self.shiftingTabs = 0   ;   nt = self.n[T]
            for i, (k,v) in enumerate(self.smap.items()):
                p, l, c, r = self.cc2plct(k, dbg=0)
                self.log(f'i={i} k={k} v={v} text={self.smap[k]}')
                for t in range(nt):
                    text = self.smap[k][t]    ;    kt = k + t    ;    fn = 0   ;   ntones = misc.Note.NTONES * 2
                    if self.isFret(text):
                        fn = self.afn(str((self.getFretNum(text) + self.shiftSign * self.getFretNum(nf)) % ntones))  ;  self.log(f'i={i} t={t} text={text} nf={nf} fn={fn}')
                    if fn and self.isFret(fn):  self.setDTNK(fn, kt, p, l, c, t) # uk=0 for each nt tabs
                self.setChord(p, l, c, 0) # do what uk=1 does, once
            self.shiftSign = 1
            self.dataHasChanged = 1
            self.unselectAll('shiftTabs()')
        self.dumpSelectTabs(f'END {how} shiftingTabs={self.shiftingTabs} nf={nf}')

    def swapTab(self, how, txt='', data=None, dbg=0):  # e.g. c => 12 not same # chars asserts
        self.log(f'BGN {how} txt={txt} swapping={self.swapping} swapSrc={self.swapSrc} swapTrg={self.swapTrg}')
        if data is None: data = self.data
        if not self.swapping: self.swapping = 1
        elif txt.isalnum():
            if   self.swapping == 1:   self.swapSrc += txt  ;   self.log(f'{how} swapping={self.swapping} swapSrc={self.swapSrc} swapTrg={self.swapTrg}')
            elif self.swapping == 2:   self.swapTrg += txt  ;   self.log(f'{how} swapping={self.swapping} swapSrc={self.swapSrc} swapTrg={self.swapTrg}')
        elif txt == ' ':
            self.log(f'{how} swapping={self.swapping} swapSrc={self.swapSrc} swapTrg={self.swapTrg}')
            if   self.swapping == 1 and not self.swapTrg: self.swapping = 2   ;   self.log(f'waiting swapSrc={self.swapSrc} swapTrg={self.swapTrg}')   ;   return
            elif self.swapping == 2 and     self.swapTrg: self.swapping = 0   ;   self.log(f'ready   swapSrc={self.swapSrc} swapTrg={self.swapTrg}')
            self.log('set go')
            np, nl, ns, nc, nr = self.n  ;  nc += CCC
            for i in range(len(self.tabs)):
                self.tabs[i].text   = self.tabs[i].text.replace(self.swapSrc, self.swapTrg)
                self.notes[i].text  = self.notes[i].text.replace(self.swapSrc, self.swapTrg)
                self.chords[i].text = self.chords[i].text.replace(self.swapSrc, self.swapTrg)
            for p in range(np):
                for l in range(nl):
                    for c in range(nc):
                        if dbg: self.log(f'before data[{p}][{l}][{c}]={data[p][l][c]}')
                        data[p][l][c] = data[p][l][c].replace(self.swapSrc, self.swapTrg)
                        if dbg: self.log(f'after  data[{p}][{l}][{c}]={data[p][l][c]}')
            self.dataHasChanged = 1
        self.log(f'END {how} {txt} swapping={self.swapping} swapSrc={self.swapSrc} swapTrg={self.swapTrg}')
    ####################################################################################################################################################################################################
    def setTab(self, how, text, rev=0, dbg=1):  # VERBOSE):
        self.log(f'BGN {how} text={text} rev={rev} {fmtl(self.i, FMTN)}')
        if rev: self.reverseArrow()    ;    self.autoMove(how)
        cc = self.cursorCol()          ;    p, l, s, c, t = self.j()
        prev = self.data[p][l][c][t]   ;    pf = self.isFret(prev)   ;   tf = self.isFret(text)
        self.setDTNK(text, cc, p, l, c, t, uk=1 if pf or tf else 0)
        if rev: self.reverseArrow()
        else:   self.autoMove(how)
        if dbg: self.snapshot()
        self.log(f'END {how} text={text} rev={rev} {fmtl(self.i, FMTN)}')
        self.dataHasChanged = 1

    def setDTNK(self, text, cc, p, l, c, t, uk=0, dbg=1):  # VERBOSE):  # what was previous data value
        if dbg: self.log(f'BGN text={text} cc={cc} plct {p} {l} {c} {t} uk={uk}')
        self.setData(text, p, l, c, t)
        if self.TNIK[TT]:        self.setTab2( text, cc)
        if self.TNIK[NN]:        self.setNote( text, cc, t)
        if self.TNIK[KK] and uk: self.setChord(p, l, c, t)
        if dbg: self.log(f'END text={text} cc={cc} plct {p} {l} {c} {t} uk={uk}')
    ####################################################################################################################################################################################################
    def setData(self, text, p, l, c, r, dbg=VERBOSE):
        prev = self.data[p][l][c]
        self.data[p][l][c] = prev[0:r] + text + prev[r+1:]
        if dbg: self.dumpWBWAW(f'({text} {p} {l} {c} {r})', prev, f'<data[{p}][{l}][{c}]>', self.data[p][l][c])
        cn = self.plc2cn(p, l, c)
        if self.isNBTab(text): self.tabCols.add(cn)   ;   self.log(f'adding cn={cn}')
        else:
            for t in self.data[p][l][c]:
                if self.isNBTab(t):       return
            self.tabCols.discard(cn)  ;   self.log(f'removing cn={cn}')

    def setTab2(self, txt, cc, dbg=VERBOSE):
        prev = self.tabs[cc].text
        self.tabs[cc].text = txt
        if dbg: self.dumpWBWAW(f'({txt} cc={cc})', prev, f'<tabs[{cc}].text>', self.tabs[cc].text)

    def setNote(self, txt, cc, r, dbg=VERBOSE):
        prev = self.notes[cc].text
        self.notes[cc].text = self.getNoteName(r, txt) if self.isFret(txt) else self.nblank
        if dbg: self.dumpWBWAW(f'({txt} cc={cc} r={r})', prev, f'<notes[{cc}].text>', self.notes[cc].text)

    def setChord(self, p, l, c, t, dbg=VERBOSE, dbg2=0):
        cc = self.plct2cc(p, l, c, 0)    ;    nt = self.n[T]    ;    name = ''    ;    i = 0
        if dbg: self.log(f'BGN plct {p} {l} {c} {t} cc={cc}')
        chordName, chunks = self.cobj.getChordName(p, l, c)
        if dbg: self.log(f'    plct {p} {l} {c} {t} cc={cc} chordName=<{chordName:<}> chunks={fmtl(chunks)}')
        self.setChordName(chordName, chunks, cc)
        if dbg2:
            for i in range(nt):
                name += self.chords[cc + i].text
            self.log(f'chords[{cc}-{cc+i}].text={name} chordName=<{chordName:<}> chunks={fmtl(chunks)}')
        elif dbg: self.log(f'END plct {p} {l} {c} {t} cc={cc} chordName={chordName}')

    def setChordName(self, name, chunks, cc, dbg=0):  # VERBOSE):
        txt = ''   ;   old = ''   ;   nt = self.n[T]   ;   cc = self.normalizeCC(cc)
        for i in range(nt):
            old += self.chords[cc + i].text
            if chunks and len(chunks) > i: self.chords[cc + i].text = chunks[i]
            else:                          self.chords[cc + i].text = self.nblank
            txt += self.chords[cc + i].text
        if dbg: self.log(f'BGN name=<{name}> chunks={fmtl(chunks)} chords[{cc}-{cc + nt - 1}].text=<{old}>{len(old)}')
        if dbg: self.log(f'END name=<{name}> chunks={fmtl(chunks)} chords[{cc}-{cc + nt - 1}].text=<{txt}>{len(txt)}')
    ####################################################################################################################################################################################################
    @staticmethod
    def getFretNum(tab, dbg=0):
        fretNum = None
        if   '0' <= tab <= '9': fretNum = int(tab)
        elif 'a' <= tab <= 'o': fretNum = int(ord(tab) - 87)
        if dbg: Tabs.log(f'tab={tab} fretNum={fretNum}')
        return fretNum

    def getNoteIndex(self, r, fn, dbg=0):
        row = self.n[T] - r - 1    # Reverse and zero base the string numbering: str[1 ... numStrings] => s[(numStrings - 1) ... 0]
        k = self.stringKeys[row]
        i = self.stringMap[k] + fn
        if dbg: self.log(f'r={r} fretNum={fn} row={row} k={k} i={i} stringMap={fmtm(self.stringMap)}')
        return i

    def getNoteName(self, row, tab, dbg=0):
        fretNum = self.getFretNum(tab)
        index   = self.getNoteIndex(row, fretNum)
        name    = misc.Note.getName(index)
        if dbg: self.log(f'row={row} tab={tab} fretNum={fretNum} index={index} name={name}')
        return name # if self.isFret(tab) else self.nblank
    ####################################################################################################################################################################################################
    def toggleFlatSharp(self, how, dbg=1):  #  page line col tab or select
        tt1 =  misc.Note.TYPE    ;    tt2 = (misc.Note.TYPE + 1) % 2    ;    misc.Note.setType(tt2)    ;   i1 = -1
        self.log(f'BGN {how} type={tt1}={misc.Note.TYPES[tt1]} => type={tt2}={misc.Note.TYPES[tt2]}')
        for i, n in enumerate(self.notes):
            if len(n.text) > 1:
                p, l, c, t = self.cc2plct(i)   ;   old = n.text    ;    i2 = self.plc2cn(p, l, c)
                if   n.text in misc.Note.F2S: n.text = misc.Note.F2S[n.text]
                elif n.text in misc.Note.S2F: n.text = misc.Note.S2F[n.text]
                if dbg: self.log(f'notes[{i:3}] {old} => {n.text} plct {p} {l} {c} {t} i1={i1} i2={i2}')
                if i1 != i2:       self.setChord(p, l, c, t)    ;    i1 = i2
        self.log(f'END {how} type={tt1}={misc.Note.TYPES[tt1]} => type={tt2}={misc.Note.TYPES[tt2]}')

    def keySignature(self): pass
    def scales(self):       pass
    ####################################################################################################################################################################################################
    def toggleChordNames(self, how, every=0, rev=0, dbg=1):
        if self.skeys and not every:
            if dbg: self.dumpSelectTabs(f'BGN {how} every={every} rev={rev} skeys={fmtl(self.skeys)}')
            [ self.toggleChordName(how, self.cc2cn(k), rev) for k in self.skeys ]
        else:
            cc = self.cursorCol()    ;    cn = self.cc2cn(cc)    ;    mk = list(self.cobj.mlimap.keys())
            if dbg: self.dumpSelectTabs(f'BGN {how} every={every} rev={rev} cc={cc} cn={cn} mk={fmtl(mk)}')
            if not every: self.toggleChordName(how, cn, rev)
            else:         self.toggleMatchingChordNames(how, cn, rev)
        if dbg: self.dumpSelectTabs(f'END {how} every={every} rev={rev}     ')

    def toggleMatchingChordNames(self, how, cn='', rev=0, dbg=0, dbg2=0):
        mli = self.cobj.mlimap   ;   iks, others = [], []   ;   mk = list(self.cobj.mlimap.keys())
        if cn not in mli: self.log(f'no mli key for cn={cn}') if dbg else None   ;   return
        rank = [ u[4] for u in mli[cn] ]
        [ iks.append(''.join(u[0])) for u in mli[cn] ]
        if dbg: self.log(f'BGN cn={cn} rank={rank} mk={fmtl(mk)} iks={fmtl(iks)}')
        matches, ranks = self.imapKeys2matches(iks, rank)
        if matches:
            for i in matches:
                if i in mk:
                    v = mli[i]   ;   self.log(f'selectig tabs i={i}')
                    self.selectTabs(how, 0, i * len(self.stringNumbs))
                    if dbg2: [ self.log(f'i={i} {"".join(u[0]):16} {fmtl(u[1]):18} {u[2]:12} {fmtl(u[3]):18} {u[4]}') for u in v ]
                    self.toggleChordName(how, i, rev)
        if dbg: self.log(f'END cn={cn} rank={rank} mk={fmtl(mk)} iks={fmtl(iks)}')

    def imapKeys2matches(self, iks, rank, dbg=0):
        if dbg: self.log(f'BGN rank={rank} iks={fmtl(iks)}')
        mli = self.cobj.mlimap   ;   matches = set()   ;   ranks = []   ;   msg = ''
        for k, v in mli.items():
            _rank = []           ;   match = 0         ;   r = 0
            for u in v:
                jk = ''.join(u[0])
                for ik in iks:
                    if jk == ik:     matches.add(k)    ;   _rank.append(u[4])   ;   match = 1   ;    break
            if match:
                if _rank and _rank == rank: ranks.append(_rank)
                else:
                    if dbg: msg = f' pre spin _rank={_rank} '
                    for r in range(len(rank)):
                        mli[k] = self.cobj.rotateList(mli[k])
                        _rank = [ a[4] for a in mli[k] ]
                        if _rank == rank: break
                    if dbg: self.log(f'{msg} post spin _rank={_rank} r={r+1}')
                    ranks.append(_rank)
        if dbg: self.log(f'END rank={rank} matches={fmtl(matches)} ranks={fmtl(ranks)}')
        return list(matches), ranks

    def toggleChordName(self, how, key, rev=0, dbg=1):
        if dbg: self.dumpSelectTabs(f'BGN {how} rev={rev} key={key}       ')
        chordName, chunks = self.cobj.toggleChordName(key, rev)
        cc = self.cn2cc(key)
        if chordName and chunks: self.setChordName(chordName, chunks, cc)
        elif dbg: self.log(f'selected key={key} at cc={cc} is not a chord')
        if dbg: self.dumpSelectTabs(f'END {how} rev={rev} key={key} cc={cc:3}')
    ####################################################################################################################################################################################################
    def toggleCursorMode(self, how):
        self.log(f'BGN {how} csrMode={self.csrMode}={CSR_MODES[self.csrMode]}')
        self.csrMode  = (self.csrMode + 1) % len(CSR_MODES)
        self.log(f'END {how} csrMode={self.csrMode}={CSR_MODES[self.csrMode]}')

    def toggleArrow(self, how, v=0, dbg=0):
        if dbg: self.log(f'BGN {how} v={v} hArrow={self.hArrow}={HARROWS[self.hArrow]} vArrow={self.vArrow}={VARROWS[self.vArrow]}')
        if v: self.vArrow  = (self.vArrow + 1) % len(VARROWS)
        else: self.hArrow  = (self.hArrow + 1) % len(HARROWS)
        if dbg: self.log(f'END {how} v={v} hArrow={self.hArrow}={HARROWS[self.hArrow]} vArrow={self.vArrow}={VARROWS[self.vArrow]}')
    ####################################################################################################################################################################################################
    def toggleFullScreen(self, how):
        global FULL_SCREEN
        FULL_SCREEN =  not  FULL_SCREEN
        self.set_fullscreen(FULL_SCREEN)
        self.log(f'{how} FULL_SCREEN={FULL_SCREEN}')

    def toggleBlank(self, how):
        prevBlank    =  self.tblank
        self.log(f'BGN {how}')
        self.tblanki = (self.tblanki + 1) % len(self.tblanks)
        self.tblank  =  self.tblanks[self.tblanki]
        self.swapTab(how, prevBlank, self.tblank)
        self.log(f'END {how}')
    ####################################################################################################################################################################################################
    def dumpCursorArrows(self, how): cm, ha, va = self.csrMode, self.hArrow, self.vArrow  ;   self.log(f'{how} csrMode={cm}={CSR_MODES[cm]:6} hArrow={ha}={HARROWS[ha]:5} vArrow={va}={VARROWS[va]:4}')
    def reverseArrow(self, dbg=1):
        if dbg: self.dumpCursorArrows('reverseArrow()')
        if self.csrMode == MELODY or self.csrMode == ARPG: self.toggleArrow('reverseArrow() MELODY or ARPG', v=0)
        if self.csrMode == CHORD  or self.csrMode == ARPG: self.toggleArrow('reverseArrow() CHORD or ARPG',  v=1)
        if dbg: self.dumpCursorArrows('reverseArrow()')

    def setCHVMode(self, how, c=None, h=None, v=None):
        self.dumpCursorArrows(f'BGN {how} c={c} h={h} v={v}')
        if c is not None: self.csrMode = c
        if h is not None: self.hArrow  = h
        if v is not None: self.vArrow  = v
        self.dumpCursorArrows(f'END {how} c={c} h={h} v={v}')
    ####################################################################################################################################################################################################
    def eraseTabs(self, how): # , reset=0):
        np, nl, ns, nc, nt = self.n  ;  nc += CCC
        self.log(f'BGN {how} np={np} nl={nl} ns={ns} nc={nc} nt={nt}')
        for i in range(len(self.tabs)):
            self.tabs  [i].text = self.tblank
            self.notes [i].text = self.nblank
            self.chords[i].text = self.nblank
        for p in range(np):
            for l in range(nl):
                for c in range(nc):
                    self.data[p][l][c] = self.tblankCol
        self.log(f'END {how} np={np} nl={nl} ns={ns} nc={nc} nt={nt}')
        self.dataHasChanged = 1

    def reset(self, how):
        self.log(f'{self.fmtGeom()} BGN {how} before cleanup()')
        self.cleanup()
        self.log(f'{self.fmtGeom()} after cleanup / before _reinit()')
        self._reinit()
        self.log(f'{self.fmtGeom()} END {how} after _reinit()')

    def cleanup(self):
        if QQ: self.deleteList(self.lrows)   ;   self.deleteList(self.lcols)
        self.deleteList(self.sprites)
        self.deleteList(self.labels)
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
    def isShift(mods):        return mods & pygwink.MOD_SHIFT
    @staticmethod
    def isCtrl(mods):         return mods & pygwink.MOD_CTRL
    @staticmethod
    def isAlt(mods):          return mods & pygwink.MOD_ALT
    @staticmethod
    def isCtrlShift(mods):    return mods & pygwink.MOD_CTRL and mods & pygwink.MOD_SHIFT
    @staticmethod
    def isAltShift(mods):     return mods & pygwink.MOD_ALT  and mods  & pygwink.MOD_SHIFT
    @staticmethod
    def isCtrlAlt(mods):      return mods & pygwink.MOD_CTRL and mods & pygwink.MOD_ALT
    @staticmethod
    def isCtrlAltShift(mods): return mods & pygwink.MOD_CTRL and mods & pygwink.MOD_ALT and mods & pygwink.MOD_SHIFT
    @staticmethod
    def isFret(text):         return 1 if '0'<=text<='9'      or 'a'<=text<='o'    else 0
#    def isBTab(self, text):   return 1 if text == self.tblank else 0
    @staticmethod
    def isNBTab(text):        return 1 if                        Tabs.isFret(text) or text in misc.DSymb.SYMBS else 0
    def isTab(self, text):    return 1 if text == self.tblank or Tabs.isFret(text) or text in misc.DSymb.SYMBS else 0
    def isParsing(self):      return 1 if self.inserting or self.jumping or self.shiftingTabs or self.swapping else 0
    @staticmethod
    def afn(fn): return fn if len(fn) == 1 and '0' <= fn <= '9' else chr(ord(fn[1]) - ord('0') + ord('a')) if len(fn) == 2 and fn[0] == '1' else None
#        Tabs.log(f'fn={fn} ', end='')
#        [ Tabs.log(f'ord({r})={ord(r)} ', ind=0, end='') for r in fn ]  ;  Tabs.log('', ind=0)
#        if   len(fn) == 1 and '0' <= fn <= '9': return fn
#        elif len(fn) == 2 and fn[0] == '1':     return chr(ord(fn[1]) - ord('0') + ord('a')) # 48 + 97)
#        else: Tabs.log('ERROR: ')  ;  assert 0
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
    def deleteGlob(g, why=''):
        Tabs.log(f'deleting {len(g)} file globs why={why}')
        for f in g:
            Tabs.log(f'{f}')
            os.system(f'del {f}')

    @staticmethod
    def getFilePath(seq=0, filedir='files', filesfx='.txt'):
        if seq:
            subDir     = '/' + SFX.lstrip('.')
            filedir    = filedir + subDir
            Tabs.log(f'SFX          = {SFX}')
            Tabs.log(f'subdir       = {subDir}')
            Tabs.log(f'filedir      = {filedir}')
            Tabs.log(f'filesfx      = {filesfx}')
            pathlib.Path(filedir).mkdir(parents=True, exist_ok=True)
            fileGlobArg = str(BASE_PATH / filedir / BASE_NAME) + SFX + '.*' + filesfx
            fileGlob    = glob.glob(fileGlobArg)
            Tabs.log(f'fileGlobArg  = {fileGlobArg}')
            Tabs.log('fileGlob:')
            seq        = 1 + Tabs.getFileSeqNum(fileGlob, filesfx)
            filesfx    = f'.{seq}{filesfx}'
            Tabs.log(f'{fmtl(fileGlob)}', ind=0)
            Tabs.log(f'seq num      = {seq} filesfx={filesfx}')
        return getFilePath(filedir=filedir, filesfx=filesfx)

    @staticmethod
    def getFileSeqNum(fgs, sfx, dbg=1):
        i = -1
        if len(fgs):
            ids = []
            for s in fgs:
                if s.endswith(sfx):
                    s = s[:-len(sfx)]
                    j = s.rfind('.')
                    s = s[j+1:]
                    i = int(s)
                    ids.append(i)
            if dbg: Tabs.log(f'ids={ids}')
            i = max(ids)
        return i

    @staticmethod
    def log(msg='', ind=1, file=None, flush=False, sep=',', end='\n'):
        if file is None: file = LOG_FILE
        ss = inspect.stack(0)   ;   si = ss[1]
        if   si.function in Tabs.hideST2: si = ss[3]
        elif si.function in Tabs.hideST:  si = ss[2]
        p = pathlib.Path(si.filename)  ;  n = p.name  ;  l = si.lineno  ;  f = si.function  ;  t = ''
        if   ind == 1: print(f'{Tabs.stackDepth()-4:2} {l:5} {n:7} {t} {f:>20} ', file=file, end='')
        elif ind == 2: print(f'{Tabs.indent():20} {l:5} {n:7} {t} {f:>20} ', file=file, end='')
        print(f'{msg}', file=file, flush=flush, sep=sep, end=end)
#        print(f'{msg}', file=file, flush=flush, sep=sep, end=end) if ind else print(f'{msg}', file=file, flush=flush, sep=sep, end=end)
#        if file != LOG_FILE: Tabs.log(msg, ind, flush=False, sep=',', end=end)
    ####################################################################################################################################################################################################
    def quit(self, why='', code=1, dbg=0):
        self.log(f'BGN {why} code={code}')
        if       code and AUTO_SAVE: self.saveDataFile(why, f=0)
        elif not code:               self.saveDataFile(why, f=1)
        self.cobj.dumpMLimap(why)
        self.cobj.dumpInstanceCat(why)
        self.dumpJ('quit()')
        self.cleanupCat(1 if code != 2 else 0)
        self.log(QUIT, ind=0)
        if dbg: self.dumpStruct('quit ' + why)
        if code != 2: self.snapshot()
        self.log(QUIT, ind=0)
        if dbg:
            self.dumpStack(inspect.stack())
            self.log(QUIT, ind=0)
            self.dumpStack(MAX_STACK_FRAME)
        self.dumpGlobalFlags()
        self.cleanupLog()
        exit()

    def cleanupCat(self, dump=1):
        self.log(f'BGN dump={dump}')
        if   dump and CAT: self.cobj.dumpOMAP(str(self.catPath), merge=1)
        elif dump:         self.cobj.dumpOMAP(None, merge=1)
        if CAT:
            cfp = self.getFilePath(seq=0, filedir='cats', filesfx='.cat')
            self.log(f' ***  copy {self.catPath} {cfp}  ***')
            os.system(f'copy {self.catPath} {cfp}')
        self.log(f'END dump={dump}')

    def cleanupLog(self):
        self.log(f'SEQ_LOG_FILES={SEQ_LOG_FILES}')
        logPath = None
        if SEQ_LOG_FILES:
            logPath = self.getFilePath(seq=SEQ_LOG_FILES, filedir='logs', filesfx='.log')
            self.log(f'LOG_PATH     = {LOG_PATH}')
            self.log(f'logPath      = {logPath}')
            self.log(f' *** copy {LOG_PATH} {logPath} ***')
        self.log(f'closing {LOG_FILE.name}')
        LOG_FILE.close()
        if SEQ_LOG_FILES and logPath: os.system(f'copy {LOG_PATH} {logPath}')
    ####################################################################################################################################################################################################
    @staticmethod
    def deleteList(l):
#        j = 0
#        while j < len(l): t = l[j];  t.delete();  del l[j]
        for ll in l:
            ll.delete()   ;   del ll
    @staticmethod
    def deleteMap(m):
        for k, v in m.items():
            v.delete()   ;   del v
########################################################################################################################################################################################################
if __name__ == '__main__':
    LOG_PATH = getFilePath(filedir='logs', filesfx='.log')
    with open(str(LOG_PATH), 'w') as LOG_FILE:
        Tabs.log(f'LOG_PATH={LOG_PATH} LOG_FILE={LOG_FILE}')
        Tabs()
        ret     = pyglet.app.run()
        Tabs.log(f'pyglet.app.run() returned {ret}, Exiting main')
