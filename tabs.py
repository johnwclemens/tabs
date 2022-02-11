import inspect, math, sys, os, glob, pathlib, string, collections  #, itertools #, shutil#, unicodedata, readline, csv
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
    assert type(lst) in (list, tuple, set, frozenset)
    if d1 is None: d1, d2 = '', ''
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
    if dbg: Tabs.slog(f'BASE_NAME= {BASE_NAME} SFX={SFX}')
    fileName        = BASE_NAME + sfx + filesfx
    filePath        = BASE_PATH / filedir / fileName
    if dbg: Tabs.slog(f'fileName  = {fileName} filePath={filePath}')
    return filePath

def dumpGlobals():
    Tabs.slog(f'argv      = {fmtl(sys.argv, ll=1)}')
    Tabs.slog(f'ARGS      = {fmtm(ARGS)}')
    Tabs.slog(f'PATH      = {PATH}')
    Tabs.slog(f'BASE_PATH = {BASE_PATH}')
    Tabs.slog(f'BASE_NAME = {BASE_NAME}')
    Tabs.slog(f'SFX       = {SFX}')
####################################################################################################################################################################################################
ARGS             = cmdArgs.parseCmdLine()        ;  DBG0, DBG1, DBG2, DBG3, DBG4, DBG5, DBG6, DBG7, DBG8, DBG9 = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9   ;  DBG = DBG0
AUTO_SAVE = 1  ;  CAT = 0  ;  CHECKER_BOARD = 0  ;  EVENT_LOG = 0  ;  FULL_SCREEN = 1  ;  IND = 0  ;  ORDER_GROUP = 1  ;  RESIZE = 1  ;  SEQ_FNAMES = 1  ;  SNAP = 1  ;  SUBPIX = 1  ;  VERBOSE = 0  ;  EXIT = 0
VRSN1            = 0  ;  SFX1 = chr(65 + VRSN1)  ;  QQ      = VRSN1  ;  VRSNX1 = f'VRSN1={VRSN1}       QQ={QQ     }  SFX1={SFX1}'
VRSN2            = 0  ;  SFX2 = chr(49 + VRSN2)  ;  SPRITES = VRSN2  ;  VRSNX2 = f'VRSN2={VRSN2}  SPRITES={SPRITES}  SFX2={SFX2}'
VRSN3            = 0  ;  SFX3 = chr(97 + VRSN3)  ;  CCC     = VRSN3  ;  VRSNX3 = f'VRSN3={VRSN3}      CCC={CCC    }  SFX3={SFX3}'
####################################################################################################################################################################################################
SFX              = f'.{SFX1}.{SFX2}.{SFX3}' if not ARGS['f'] else ''
PATH             = pathlib.Path.cwd() / sys.argv[0]
BASE_PATH        = PATH.parent
BASE_NAME        = BASE_PATH.stem
SNAP_DIR         = 'snaps'
SNAP_SFX         = '.png'
LOG_FILE         = None
FMTN             = (1, 1, 1, 3, 1) # p, l, s, c, t remove?
FMTN2            = (1, 2, 2, 2, 2, 2) # generalize for any # of strings
P, L, S, C       =  0,  1,  2,  3
T, N, I, K       =  4,  5,  6,  7
O, A, D, E, F, G =  8,  9, 10, 11, 12, 13
LLR, LLC         = 14, 15
TT, NN, II, KK   =  0,  1,  2,  3
Z, COLL, LINL    = ' ', 'Col', 'Line '
C1,  C2,  RLC    = 0, 1, 2
JTEXTS           = ['Page',  'Line',  'Sect',  'Col',  'Tab',  'Note',  'IKey',  'Chord',  'SNo',  'SNa',  'CapA',  'CapB',  'LStr',  'LCap',  'LLR',  'LLC']
jTEXTS           = ['pages', 'lines', 'sects', 'cols', 'tabs', 'notes', 'ikeys', 'chords', 'snos', 'snas', 'capsA', 'capsB', 'lstrs', 'lcaps', 'lrows', 'lcols']
JFMT             = [1, 1, 2, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1]
NORMAL_STYLE, CURRENT_STYLE, SELECT_STYLE, COPY_STYLE = 0, 1, 2, 3
INIT             = '###   Init   ###' * 13
QUIT             = '###   Quit   ###' * 13
MELODY, CHORD, ARPG   = 0, 1, 2
LEFT, RIGHT, UP, DOWN = 0, 1, 0, 1
CSR_MODES        = ['MELODY', 'CHORD', 'ARPG']
HARROWS, VARROWS = ['LEFT', 'RIGHT'], ['UP', 'DOWN']
####################################################################################################################################################################################################
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
    hideST  = ['log', 'getImap', 'dumpGeom', 'dumpWH', 'dumpJ', 'dumpImap', 'dumpSmap', 'dumpCursorArrows', '<listcomp>', 'dumpLimap2', 'dumpData']
    def __init__(self):
        dumpGlobals()
        global FULL_SCREEN, ORDER_GROUP, SUBPIX
        snapGlobArg = str(BASE_PATH / SNAP_DIR / BASE_NAME) + SFX + '.*' + SNAP_SFX
        snapGlob    = glob.glob(snapGlobArg)
        self.log(f'hideST:\n{fmtl(Tabs.hideST)}')  # ;   self.log(f'hideST2:\n{fmtl(Tabs.hideST2)}')
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
        self.inserting = 0     ;   self.insertStr = ''
        self.jumping = 0       ;   self.jumpStr = ''    ;   self.jumpAbs=0
        self.swapping = 0      ;   self.swapSrc = ''    ;   self.swapTrg=''
        self.dfn = ''
        self.n    = []
        self.TNIK = [1, 0, 0, 0]
        nt = 6
#        nt        = 6 if QQ else 6
        self.log(f'TNIK={(fmtl(self.TNIK))}')
        self.ww, self.hh = 640, 480
        self.n, self.i, self.x, self.y, self.w, self.h, self.g = [1, 3, self.ss(), 50, nt], [1, 1, 1, 1, nt], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], []
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
        self.n[S] = self.ss()
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
        self.allSelected = 0
        self._initDataPath()
#        self.cobj.dumpOMAP(str(self.catPath))
        if CAT: self.cobj.dumpOMAP(str(self.catPath))
#        else:   self.cobj.dumpOMAP(None)
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
        self.log(f'{INIT}', pfx=0)

    def _reinit(self):
        self.log('BGN')
        self.rmap = {}
        self.tniks = []
        self.pages, self.lines, self.sects,  self.cols                          = [], [], [], []     ;  self.A = [self.pages, self.lines, self.sects,  self.cols]
        self.tabs,  self.notes, self.ikeys,  self.chords                        = [], [], [], []     ;  self.B = [self.tabs,  self.notes, self.ikeys,  self.chords]
        self.snos,  self.capsA, self.snas,   self.capsB, self.lstrs, self.lcaps = [],[],[],[],[],[]  ;  self.C = [self.snos,  self.capsA,  self.snas,  self.capsB, self.lstrs, self.lcaps]
        self.lrows, self.lcols, self.labels, self.sprites                       = [], [], [], []     ;  self.D = [self.lrows, self.lcols, self.labels, self.sprites]
        self.E = [*self.A, *self.B, *self.C, *self.D]
        self.log(f'E={fmtl(self.E)}')
        self.DF = [0, 0, 0, 0,  0, 0, 0, 0,  0, 0, 0, 0, 0, 0,  0, 0, 0, 0]
        self.initJ('reinit')
        self.data    = []   ;   self.dataHasChanged = 0
        self.kbk, self.symb, self.mods, self.symbStr, self.modsStr = 0, 0, 0, '', ''
        self.cc, self.ci, self.SNAP0, self.armSnap  = 0, 0, 0, ''
        self.tblanki, self.tblanks  = 1, [' ', '-']   ;   self.tblank = self.tblanks[self.tblanki]
#        self.nblanki, self.nblanks  = 1, [' ', '-']   ;   self.nblank = self.nblanks[self.nblanki]
        self.tblankCol = self.tblank * self.n[T]      ;  self.tblankRow = self.tblank * (self.n[C] + CCC)
        self.cursor, self.caret   = None, None
        self._init()
        self.log('END')

    def _init(self, dbg=0):
        self.dumpGeom('BGN')
        self.ssi = 0
        self._initTpz()
        self._initDataPath()
        self.kp  = [    VIOLETS[0],    VIOLETS[12]] if CHECKER_BOARD else [   VIOLETS[10]]
        self.kl  = [     BLUES[12],      BLUES[15]] if CHECKER_BOARD else [     BLUES[12]]
        self.ks  = [     CYANS[12],      CYANS[15]] if CHECKER_BOARD else [     CYANS[12]]
        self.kc  = [      GRAYS[9],      GRAYS[13]] if CHECKER_BOARD else [     GRAYS[13]]
        self.kt  = [    ORANGES[0],     ORANGES[8]] if CHECKER_BOARD else [    ORANGES[0]]
        self.kn  = [     GREENS[0],     GREENS[12]] if CHECKER_BOARD else [     GREENS[0]]
        self.ki  = [    YELLOWS[0],     YELLOWS[8]] if CHECKER_BOARD else [    YELLOWS[0]]
        self.kk  = [      CYANS[0],       CYANS[8]] if CHECKER_BOARD else [      CYANS[0]]
        self.kt2 = [    YELLOWS[0],     YELLOWS[8]] if CHECKER_BOARD else [    YELLOWS[0]]
        self.kn2 = [GREEN_BLUES[0], GREEN_BLUES[8]] if CHECKER_BOARD else [GREEN_BLUES[4]]
        self.ki2 = [      CYANS[0],       CYANS[8]] if CHECKER_BOARD else [      CYANS[0]]
        self.kk2 = [      BLUES[0],       BLUES[8]] if CHECKER_BOARD else [      BLUES[0]]
        self.klr = [    ORANGES[0],     ORANGES[8]] if CHECKER_BOARD else [    ORANGES[0]]
        self.klc = [      PINKS[0],       PINKS[8]] if CHECKER_BOARD else [      PINKS[0]]
        self.kll = [       REDS[0],        REDS[8]] if CHECKER_BOARD else [       REDS[0]]
        self.k   = [ self.kp, self.kl, self.ks, self.kc, self.kt, self.kn, self.ki, self.kk, self.klc, self.klr, self.kll ]
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
        txt = ['    ', '  ', '']  ;  [ self.log(f'llText[{i}]={txt[i]}{fmtl(t)}', pfx=0) for i, t in enumerate(self.llText) ]
        self.dumpJ('init')
        self.dumpWH()   ;  self.ss()
        self.smap = {}
        self.createTNIKs()
        self.cobj.dumpMlimap('init')
        self.dumpWH()
        self.dumpJ('init')
        if dbg: self.dumpLabels('new2')
        if self.TNIK[TT] and self.tabs: self.createCursor(self.g[T + 3]) # fix g index
        if dbg: self.dumpStruct('_init()')
#        self.testslice()
        if EXIT: self.quit('EXIT TEST')
        self.dumpGeom('END')
    ####################################################################################################################################################################################################
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
        self.log(f'dataName0 = {dataName0}')
        self.log(f'dataName1 = {dataName1}')
        self.log(f'dataName2 = {dataName2}')
        self.log(f'dataPath0 = {self.dataPath0}')
        self.log(f'dataPath1 = {self.dataPath1}')
        self.log(f'dataPath2 = {self.dataPath2}')

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
    def tpz(self):   return self.tpp, self.tpl, self.tps, self.tpc
    ####################################################################################################################################################################################################
    def ss(self, dbg=0):   s = sum(self.TNIK)  ;    self.log(f'{s} {fmtl(self.TNIK)} {fmtl(self.n)}') if dbg else None   ;   return s   # return 0-4
    def dl(self, data=None): data = self.data if data is None else data  ;  return len(data), len(data[0]), len(data[0][0]), len(data[0][0][0])
    def lenA(self):  return [ len(_) for _ in self.A ]
    def lenB(self):  return [ len(_) for _ in self.B ]
    def lenC(self):  return [ len(_) for _ in self.C ]
    def lenD(self):  return [ len(_) for _ in self.D ]
    def lenE(self):  return [ len(_) for _ in self.E ]
    def initJ(self, why='init'): self.J1 = [ 0 for _ in self.E ]   ;   self.J2 = [ 0 for _ in self.E ]   ;   self.dumpJ(why)   ;   return self.J1, self.J2
#    def updateJs(self, i, v): self.J1[i] = v    ;    self.J2[i] += 1 # not used?
    def j(self):     return [ i-1 if i else 0 for i in self.i ]
    def j2(self):    return [ i-1 if i else 0 for j, i in enumerate(self.i)  if j != S ]
    def j3(self):    return [ i-1 if i else 0 for j, i in enumerate(self.i)  if j != S and j != T ]
    def ids(self):
        if SPRITES: return sum(self.J2[:4]), sum(self.J2[4:16]) # sum(self.J2[4:8]) + sum(self.J2[8:14]) + sum(self.J2[14:16])
        else:       return self.J2[-2],      sum(self.J2[:16])  # sum(self.J2[:4]) + sum(self.J2[4:8]) + sum(self.J2[8:14]) + sum(self.J2[14:16])
    def cnts(self): return self.J2[:16]
    ####################################################################################################################################################################################################
    def fmtDD(self, data=None, d='x'): l=list(map(str, self.dl(data)))  ;  return f'({d.join(l)})'
    def fmtWH(self, w=None, h=None, d='x'): (w, h) = (self.ww, self.hh) if not w and not h else (w, h)  ;  return f'({d.join([str(w), str(h)])})'
    def fPos(self):  plct = self.j2()   ;   cc = self.plct2cc(*plct)   ;   cn = self.cc2cn(cc)   ;   return f'{fmtl(plct)} {cc:2} {cn}]'
    ####################################################################################################################################################################################################
    def dumpGlobalFlags(self):
        txt1 = f'AUTO_SAVE={AUTO_SAVE} CAT={CAT} CHECKER_BOARD={CHECKER_BOARD} EVENT_LOG={EVENT_LOG} FULL_SCREEN={FULL_SCREEN} IND={IND} '
        txt2 = f'ORDER_GROUP={ORDER_GROUP} RESIZE={RESIZE} SEQ_FNAMES={SEQ_FNAMES} SNAP+{SNAP} SUBPIX={SUBPIX} VERBOSE={VERBOSE}'
        self.log(f'{txt1} {txt2} CCC={CCC}', pfx=0)

    def dumpDataSlice(self, p, l, c, cc):
        for t in range(self.n[T]):
            ikeys  = self.ikeys[ cc+t].text if self.ikeys  and len(self.ikeys)  > cc+t else ''
            chords = self.chords[cc+t].text if self.chords and len(self.chords) > cc+t else ''
            self.log(f'{self.data[p][l][c]} [{cc+t}] {self.tabs[cc+t].text:2} {self.notes[cc+t].text:2} {ikeys:2} {chords:2}')
    @staticmethod
    def dumpObj( obj,  name, why='', file=None): Tabs.slog(f'{why} {name} ObjId {hex(id(obj))} {type(obj)}', file=file)
    @staticmethod
    def dumpObjs(objs, name, why=''): [Tabs.dumpObj(o, name, why) for o in objs]  # ;   [Tabs.slog(f'{hex(id(o))} type={type(o)}', pfx=0) for o in obj]   ;    Tabs.slog(pfx=0)
    def dumpGeom(self, why1='', why2=''):   e = self.lenE()[:-2]   ;   self.log(f'{why1} {QQ} {CCC} {self.ss()} {fmtl(self.TNIK)} {fmtl(self.n)} {fmtl(e)} {sum(e)} {why2}')
    def dumpJ(self, why):         self.log(f'J1 {fmtl(self.J1, w=JFMT)} {sum(self.J1[:]):4} {why}')  ;  self.log(f'J2 {fmtl(self.J2, w=JFMT)} {sum(self.J2[:]):4} {why}')
    def dumpWH(self): self.log(f'{self.fmtWH()} {fmtl(self.w, w="7.2f", u=">")} {fmtl(self.h, w="7.2f", u=">")}')
    ####################################################################################################################################################################################################
    def autoSave(self, dt, how, dbg=0):
        if dbg: self.log(f'dt={dt:7.4f} {how} dataHasChanged={self.dataHasChanged}')
        if AUTO_SAVE and self.dataHasChanged: self.saveDataFile(how=how)   ;   self.dataHasChanged = 0

    def on_draw(self, dbg=0):
        self.clear()
        self.batch.draw()
        if SNAP and self.armSnap:
            if dbg: self.log(f'armSnap={self.armSnap}')
            self.snapshot(self.armSnap)  ;  self.armSnap = ''

    def on_resize(self, width, height, dbg=0):
        super().on_resize(width, height)
        self.ww, self.hh = width, height   ;   why = 'resize'
        if dbg: self.log(f'BGN {self.fmtWH()} {self.fmtDD(self.data)} {fmtl(self.n)} {(fmtl(self.TNIK))} {fmtl(self.lenE()[:-2])} {sum(self.lenE()[:-2])}')
        if dbg: self.dumpWH()
        self.initJ(f'BGN {why}')
        if RESIZE: self.resizeTNIKs()
        self.dumpJ(f'END {why}')
        self.dumpStruct2(why)
        self.resizeFonts()
        if not self.cursor and self.tabs and self.TNIK[TT]:  self.createCursor(self.g[T + 3]) # fix g index
        elif   self.cursor:                                  self.resizeCursor()
#        self.snapshot()
#        if dbg: self.dumpStruct(why)
        if dbg: self.setCaption(self.fmtf())
        if dbg: self.log(f'END {self.fmtWH()} {self.fmtDD(self.data)} {fmtl(self.n)} {(fmtl(self.TNIK))} {fmtl(self.lenE()[:-2])} {sum(self.lenE()[:-2])}')
    ####################################################################################################################################################################################################
    def dumpStruct(self, why=''):
        self.log(f'BGN {why}')
#        self.dumpData(why)
        self.dumpTNIK(why)
        self.dumpLabels(why)
        self.dumpTabs(why)
        self.dumpCols(why)
        self.log(f'END {why}')

    def dumpStruct2(self, why=''):
        self.dumpGeom('BGN')
        self.dumpFont(why)
        self.dumpGlobalFlags()
        self.dumpGeom('   ')
        self.log(f'{self.fmtWH()} {self.fmtDD(self.data)}')
        self.cobj.dumpMlimap(why)
        self.dumpGeom('END')
    ####################################################################################################################################################################################################
    def saveDataFile(self, how, f=0, dbg=0):
        if dbg:   self.log(f'{how} f={f}')
        if not f and AUTO_SAVE: dataPath = self.dataPath0
        else:                   dataPath = self.dataPath1 if f == 1 else self.dataPath2
        with open(dataPath, 'w') as DATA_FILE:
            self._saveDataFile(how, DATA_FILE)

    def _saveDataFile(self, how, file, dbg=0):
        if dbg: self.log(f'{how}')
        self.log(f'{file.name:40}', pfx=0)
        np, nl, nc, nr = self.dl()  # ;  nc += CCC
        data = self.transposeData(self.data) if self.isVert() else self.data
        for p in range(np):
            if dbg: self.log(f'writing {p+1}{self.ordSfx(p+1)} page', pfx=0)
            for l in range(nl):
                if dbg: self.log(f'writing {l+1}{self.ordSfx(l+1)} line', pfx=0)  # if dbg  else  self.log(pfx=0)  if  l  else  None
                for r in range(nr):
                    text = ''
                    for c in range(nc):
                        text += data[p][l][r][c]
                    if dbg: self.log(f'writing {r+1}{self.ordSfx(r+1)} string {text}', pfx=0)  # if dbg  else  self.log(text, pfx=0)
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
                    lines.append(strings)   ;   strings = []
                    self.log(f'read    {l:2}{self.ordSfx(l)} Line with {c:6,} Cols on {r:4,} Strings {c*r:8,} Tabs')
                    if l == nl: break
                    r = 0   ;   l += 1
                if c:  self.log(f'l={l} r={r} c={c}: {s}')
            self.data.append(lines)
        self.initBlank()
        nt   = l * c * r
        vert = self.isVert()
        self.log(f'read     {l:2} Lines with {l*c:6,} Cols on {l*r:4,} Strings {nt:8,} Tabs, vert={vert}')
        if dbg:     self.dumpDataVert() if vert else self.dumpDataHorz()
        self.data = self.transposeData()
        vert      = self.isVert()
        if dbg:     self.dumpDataVert() if vert else self.dumpDataHorz()
        self.saveDataFile('readDataFile()', f=2)
        self.log(f'assert: size=nt+2*(l*r+l-1) {nt:8,} + {2*(l*r+l-1)} = {size:8,} bytes assert isVert={vert}')
#        assert size == nt + 2 * (l * r + l - 1)  ;  assert vert
        self.log(f'END {DATA_FILE.name:40} {size:8,} bytes = {size/1024:4,.0f} KB')

    def initBlank(self):
        self.tblankCol = self.tblank * self.tpc   ;   data = self.data
        for p in range(len(data)):
            for l in range(len(data[0])):
                for c in range(len(data[0][0])):
                    for b in self.tblanks:
                        if b != self.tblank: data[p][l][c] = data[p][l][c].replace(b, self.tblank)
        self.log(f'tblank={self.tblank} blankCol={self.tblankCol}')

    def isVert(self, data=None, dbg=0):
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
        self.log(f'BGN {self.fmtDD(data)} lc={lc} ll={ll} i={i}')
        for p in range(len(data)):
            for l in range(len(data[p])):
                if ll:  llt = f'Line {l+1}'  ;  llab = f'{llt:{i+1}}'  ;  self.log(f'{Z*i}{llab}', pfx=0)
                if lc:  self.dumDataLabels(data[p][l], i=i, sep=Z)
                for r in range(len(data[p][l])):
                    self.log(f'{Z*i}', pfx=0, end='')
                    for c in range(len(data[p][l][r])):
                        self.log(f'{data[p][l][r][c]}', pfx=0, end='')
                    self.log(pfx=0)
                self.log(pfx=0)
        self.log(f'END {self.fmtDD(data)} lc={lc} ll={ll} i={i}')

    def dumpDataVert(self, data=None, lc=1, ll=1, i=0):
        if data is None: data = self.data
        self.log(f'BGN {self.fmtDD(data)} lc={lc} ll={ll} i={i}')
        if ll:
            t0 = Z * i + COLL + Z       if        i >= 0 else COLL
            self.log(t0, pfx=0, end='') if lc and i >= 0 else self.log(Z * i, pfx=0, end='')
            w = max(len(data[0][0][0]), len(LINL) + 1)
            for p in range(len(data)):
                for l in range(len(data[0])):
                    t = f'{LINL}{l+1}'
                    self.log(f'{t:{w}}', pfx=0, end=Z)
                self.log(pfx=0) #            self.log(t0, pfx=0)         if lc and i < 0 else self.log(pfx=0)
        for p in range(len(data)):
            for c in range(len(data[p][0])):
                self.log(f'{Z*i}{c+1:3} ', pfx=0, end='') if i >= 0 and lc else self.log(f'{Z*i}', pfx=0, end='')
                for l in range(len(data[p])):
                    self.log(f'{data[p][l][c]}', pfx=0, end=Z)
                self.log(pfx=0) #            self.log(f'{c+1:3} ',        pfx=0)           if i <  0 and c else self.log(pfx=0)
        self.log(f'END {self.fmtDD(data)} lc={lc} ll={ll} i={i}')
    ####################################################################################################################################################################################################
    def dumDataLabels(self, data=None, i=0, sep='%'):
        pp = '  '  ;  qq = ' @'
        p = pp[:] if CCC > 1 else pp[:1] if CCC else ''
        q = qq[:] if CCC > 1 else qq[:1] if CCC else ''
        if data is None: data = self.data
        n = len(data[0])-CCC    ;  a = ' ' * i if i else ''   ;  b = sep * n  ;  r = sep * 3
        if n >= 100:   self.log(   f'{a}{p}', pfx=0, end='')  ;  [  self.log(f'{c//100}'   if c>=100 else ' ', pfx=0, end='') for c in range(1, n+1) ]  ;  self.log(pfx=0)
        if n >= 10:    self.log(   f'{a}{p}', pfx=0, end='')  ;  [  self.log(f'{c//10%10}' if c>=10  else ' ', pfx=0, end='') for c in range(1, n+1) ]  ;  self.log(pfx=0)
        self.log(                  f'{a}{q}', pfx=0, end='')  ;  [  self.log(f'{c%10}',                        pfx=0, end='') for c in range(1, n+1) ]  ;  self.log(pfx=0)
        if sep != '':  self.log(f'{a}{r}{b}', pfx=0)

    def transposeData(self, data=None, why='External', dbg=1):
        if data is None: data = self.data
        if dbg: self.log(f'BGN {self.fmtDD(data)} {why}')
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
        if dbg: self.log(f'END {self.fmtDD(transposed)} {why}')
        return transposed

    def dumpLabelText(self, t, d='%', why='', dbg=0):
        self.log(f'{why} len(t)={len(t)} len(t[0])={len(t[0])}')
        for j in range(len(t)):
            self.log(f'{t[j][0]:^3}', pfx=0, end=' ')
        self.log(pfx=0)
        for k in range(len(t)//10):
            for i in range(9): self.log(f'{" ":^3}', pfx=0, end=' ')
            self.log(f' {d} ', pfx=0, end=' ')
        self.log(pfx=0)
        for j in range(len(t)):
            self.log(f'{t[j][1]:^3}', pfx=0, end=' ')
        self.log(pfx=0)
        if dbg:
            for i in range(len(t)):
                self.log(f'{i+1:5}', pfx=0, end=' ')
                self.log(f' {t[i][0]:>5}', pfx=0, end=' ')
                d2 = ' ' if i == 1 or (i + 1) % 10 else d
                self.log(f'{d2}{t[i][1]:>5}', pfx=0, end=' ')
                self.log(pfx=0)

    def createLabelText(self):
        self.labelTextA.extend(f'{j}' for j in range(1, self.n[C] + 1))
        self.labelTextB.extend(f'{j%10}' if j % 10 else f'{j // 10 % 10}' for j in range(1, self.n[C] + 1))
        self.log(f'labelTextA={fmtl(self.labelTextA)}', pfx=0)
        self.log(f'labelTextB={fmtl(self.labelTextB)}', pfx=0)
        texts = list(zip(self.labelTextA, self.labelTextB))
        self.log(f'texts={fmtl(texts)}', pfx=0)
        self.dumpLabelText(texts)
    ####################################################################################################################################################################################################
    def showLabel(self, i, p, j, g, t='', k=None, v=1, dbg=0):
        why = 'show '   ;   self.J1[j] = i
        if   SPRITES and j < T: self.createSprite(p=p, j=j, x=0, y=0, w=self.w[j], h=self.h[j], kk=self.cci(i, k), g=g, why=why,      kl=k, v=v, dbg=dbg)
        else:                   self.createLabel( p=p, j=j, x=0, y=0, w=0,         h=0,         kk=self.cci(i, k), g=g, why=why, t=t, kl=k,      dbg=dbg)

    def hideLabels(self, p, t, r1, r2=0, r3=1, dbg=1):
        for j in range(r1, r2, r3):
            text = p[j].text if not SPRITES else ''
            if len(p) > j: self.log(f'{j+1:3} {r2:3} {r3:3} hide {text}', pfx=0) if dbg else None   ;   self.hideLabel(p, j, t)
            else:          self.quit(f'ERROR index j={j+1} >= len(p)={len(p)} t={t} r1,2,3={r1} {r2} {r3}')

    def hideLabel(self, p, j, t='', dbg=1):
        c = p[j]    ;    ha = hasattr(c, 'text')
        x, y, w, h = c.x, c.y, c.width, c.height
        text = c.text if ha else ''
        if   type(c) == pyglet.sprite.Sprite: c.update(x=0, y=0, scale_x=0, scale_y=0)
        elif type(c) == pyglet.text.Label:    c.x, c.y, c.width, c.height = 0, 0, 0, 0
        if dbg: self.log(f'{t:5} {j+1:3} {hex(id(c))} {text:6} {x:7.2f} {y:7.2f} {w:7.2f} {h:7.2f} {c.x:7.2f} {c.y:7.2f} {c.width:7.2f} {c.height:7.2f}', pfx=0)
    ####################################################################################################################################################################################################
    def OLD_1_hideTabs(self, tnik):
        tabs = self.B[tnik]  ;  stnik = self.ss()   ;   msg = f'HIDE tnik={tnik}'
        ttype = 'Tab' if tnik == TT  else 'Note' if tnik == NN else 'Chord' if tnik == KK else '???'
        np, nl, ns, nc, nt = self.n
        ns2 = nl * stnik     ;    ns3 = ns2 - nl
        nc2 = nc * ns2       ;    nc3 = nc2 - nc2 // nl
        self.dumpGeom('BGN', msg)
#        for s in range(ns2-1, ns2-nl-1, -1):
#            self.hideLabel(self.sects, s, 'Sect', dbg=dbg)
#        for c in range(nc2-1, nc2-(len(self.cols)//nl)-1, -1):
#            self.hideLabel(self.cols, c, 'Col', dbg=dbg)
#        for t in range(len(tabs)-1, -1, -1):
#            self.hideLabel(tabs, t, ttype, dbg=dbg)
        if stnik <= 0:  msg = f'ERROR hideTabs() TNIK={fmtl(self.TNIK)} stnik={stnik}'   ;   self.log(msg)   ;   self.quit(msg)
        self.log(f'ns2,ns3={ns2} {ns3} nc2,nc3={nc2} {nc3}')
        self.hideLabels(self.sects, 'Sect',      ns2-1, ns3-1, -1)
        self.hideLabels(self.cols,  'Col',       nc2-1, nc3-1, -1)
        self.hideLabels(     tabs,  ttype, len(tabs)-1,    -1, -1)
        self.log(f'len(sect,col)={len(self.sects)} {len(self.cols)} lenA,B={fmtl(self.lenA())} {fmtl(self.lenB())}')
        if CCC:
            for l in range(nl-1, -1, -1):
                if CCC > C2:
                    if   tnik == KK: self.hideLabels(self.lcaps, 'LCap', (l+1)*nt-1, l*nt-1, -1)
                    elif tnik == NN: self.hideLabels(self.capsB, 'CapB', (l+1)*nt-1, l*nt-1, -1)
                    elif tnik == TT: self.hideLabels(self.capsA, 'CapA', (l+1)*nt-1, l*nt-1, -1)
                if CCC > C1:
                    if   tnik == KK: self.hideLabels(self.lstrs, 'LStr', (l+1)*nt-1, l*nt-1, -1)
                    elif tnik == NN: self.hideLabels(self.snas,   'SNa', (l+1)*nt-1, l*nt-1, -1)
                    elif tnik == TT: self.hideLabels(self.snos,   'SNo', (l+1)*nt-1, l*nt-1, -1)
        """
        if CCC and tnik == TT:
            for l in range(nl-1, -1, -1):
                if CCC > C2:
                    for z in range(nt-1, -1, -1):
                        self.hideLabel(self.capsA, z + l * nt, 'CapA')
                if CCC > C1:
                    for z in range(nt-1, -1, -1):
                        self.hideLabel(self.snos,  z + l * nt, 'SNo')
        elif CCC and tnik == NN:
            for l in range(nl-1, -1, -1):
                if CCC > C2:
                    for z in range(nt-1, -1, -1):
                        self.hideLabel(self.capsB, z + l * nt, 'CapB')
                if CCC > C1:
                    for z in range(nt-1, -1, -1):
                        self.hideLabel(self.snas,  z + l * nt, 'SNa')
        elif CCC and tnik == KK:
            for l in range(nl-1, -1, -1):
                if CCC > C2:
                    for z in range(nt-1, -1, -1):
                        self.hideLabel(self.lcaps, z + l * nt, 'LCap')
                if CCC > C1:
                    for z in range(nt-1, -1, -1):
                        self.hideLabel(self.lstrs, z + l * nt, 'LStr')
        """
        if SNAP: self.snapshot(f'hideTabs() {fmtl(self.TNIK)} {msg}')
        self.dumpGeom('END', msg)

    def OLD_1_showTabs(self, tnik, dbg=1, dbg2=0):
        np, nl, ns, nc, nt = self.n           ;  tabs = self.B[tnik]
        nt2 = nl * nc * nt  ;  nc2 = nl * nc  ;  ns2 = nl    ;   tnikB = tnik + len(self.B)   ;   chunks = []
        ks  = self.ks       ;   kc = self.kc  ;   msg = f'SHOW tnik={tnik}'
        k = [self.kt, self.kn, self.ki, self.kk]
        ttype = 'Tab' if tnik == TT  else 'Note' if tnik == NN else 'Chord' if tnik == KK else '???'  # ;  t, c, s = 0, 0, 0
        self.dumpGeom('BGN', msg)
        if dbg2: self.log(f'ns2={ns2} nt2={nt2} nc2={nc2} len({ttype})={len(tabs)}')
        for s in range(ns2):
            self.showLabel(s, p=self.sects, j=S, g=self.g[S], k=ks, dbg=dbg)
        for c in range(nc2):
            self.showLabel(c, p=self.cols,  j=C,  g=self.g[C], k=kc, dbg=dbg)
        for t in range(nt2):
            tt, p, l, cc = t % nt, t // nt2, t // (nc * nt), (t // nt) % nc
            tab = self.data[p][l][cc][tt]
            note = self.tab2nn(tab, tt) if self.isFret(tab) else self.tblank
            if t % nt == 0:   chordName, chunks = self.cobj.getChordName(p, l, cc)  # call only once per column or tpc
            chord = chunks[tt] if len(chunks) > tt else self.tblank
            text  = tab if tnik == TT else note if tnik == NN else chord if tnik == KK else '???'
            if dbg2: self.log(f'({t} {tt} {p} {l} {cc} {text:2} {tab} {note:2} {chord:2}) ', pfx=0, end='')
            self.showLabel(tt, p=tabs, j=tnikB, g=self.g[T], t=text, k=k[tnik], dbg=dbg)
#        if SNAP and dbg: self.snapshot(f'showTabs() {fmtl(self.TNIK)} {msg}')
        self.dumpGeom('END', msg)
    ####################################################################################################################################################################################################
    def hideRLCols(self, dbg=1):
#        np, nl, ns, nc, nt = self.n   ;   cols = self.cols   ;   nc = len(cols)   ;   l, s, c = 0, 0, 0   ;  sno, sna, capA, capB, lstr, lcap = 0, 0, 0, 0, 0, 0
#        cc = 2 # if CCC else 1
        snos, snas, capsA, capsB, lstrs, lcaps = self.snos, self.snas, self.capsA, self.capsB, self.lstrs, self.lcaps   ;   cols = self.cols
        cc = 2 if CCC else 1   ;   np, nl, ns, nc, nt = self.n   ;   nc = len(cols)   ;   nc2 = nc - (cc * ns * nl)   ;   msg = 'HIDE '
        self.dumpGeom('BGN', msg)
        """
        for c in range(nc-1, nc - (cc * ns * nl) - 1, -1):
            self.hideLabel(cols, c,   t='Col', dbg=dbg)
        for sno  in range(len(snos)-1, -1, -1):
            self.hideLabel(   snos,  sno,  t='SNo')
        for capA  in range(len(capsA)-1, -1, -1):
            self.hideLabel(   capsA,  capA,  t='CapA')
        for sna  in range(len(snas)-1, -1, -1):
            self.hideLabel(   snas,  sna,  t='SNa')
        for capB  in range(len(capsB)-1, -1, -1):
            self.hideLabel(   capsB,  capB,  t='CapB')
        for lstr  in range(len(lstrs)-1, -1, -1):
            self.hideLabel(   lstrs,  lstr,  t='LStr')
        for lcap  in range(len(lcaps)-1, -1, -1):
            self.hideLabel(   lcaps,  lcap,  t='LCap')
        """
        self.hideLabels(cols,  'Col',          nc-1, nc2-1, -1)
        self.hideLabels(snos,  'SNo',  len(snos) -1,    -1, -1)
        self.hideLabels(capsA, 'CapA', len(capsA)-1,    -1, -1)
        self.hideLabels(snas,  'SNa',  len(snas) -1,    -1, -1)
        self.hideLabels(capsB, 'CapB', len(capsB)-1,    -1, -1)
        self.hideLabels(lstrs, 'LStr', len(lstrs)-1,    -1, -1)
        self.hideLabels(lcaps, 'LCap', len(lcaps)-1,    -1, -1)
        if SNAP and dbg: self.snapshot(f'hideRLCols() QQ={QQ} CCC={CCC}') # l={l} s={s} c={c}  sno={sno} sna={sna} capA={capA} capB={capB} lstr={lstr} lcap={lcap}')
        self.dumpGeom('END', msg)

    def toggleRLCols(self, how):
        global CCC  ;  CCC = (CCC + 1) % 3
        msg2 = f'{how} CCC={CCC}'
        self.dumpGeom('BGN', f'     {msg2}')
        show = 1 if (CCC == 1 and (not self.lenC()[0] or not self.lenC()[1])) or (CCC == 2 and (not self.lenC()[2])) else 0
        if show: msg = 'SHOW '   ;   self.showRLCols(how)
        else:    msg = 'HIDE '   ;   self.hideRLCols()
        self.on_resize(self.ww, self.hh, dbg=1)
        self.dumpGeom('END', f'{msg} {msg2}')

    def COPY_toggleTabs(self, how, tnik):
        msg2 = f'{how} tnik={tnik}'
        self.dumpGeom(f'BGN', f'     {msg2}')
        if   not self.TNIK[tnik] and not self.B[tnik]: msg = 'SHOW'   ;   self.showTabs(how, tnik)
        elif     self.TNIK[tnik]:                      msg = 'HIDE'   ;   self.hideTabs(how, tnik)
        else:                                          msg = 'SKIP'   ;   self.dumpGeom('   ', f'{msg} {msg2}')   ;   self.toggleTnik(tnik)
        self.on_resize(self.ww, self.hh, dbg=1)
        self.dumpGeom('END', f'{msg} {msg2}')
    def OLD__showRLCols(self, dbg=1):
        why, text, plist = 'show ', '???', []
        np, nl, ns, nc, nt = self.n   ;   v = 1   ;   msg = 'SHOW '  # ;   l, s, c, t = 0, 0, 0, 0
        tt, nn, ii, kkk = self.TNIK
        kt2, kn2, kk2 = self.kt2, self.kn2, self.kk2   ;   kc = self.kc   ;   kk, kl = kc, kt2
        self.dumpGeom('BGN', msg)
        for l in range(nl):
            for s in range(ns):
                c = CCC - 1   ;   self.J1[C] = c  ;   j = C
                if SPRITES:       self.createSprite(p=self.cols,  j=j,   x=0, y=0, w=self.w[C], h=self.h[C], kk=self.cci(c, kc), g=self.g[C], why=why, kl=kc, v=v, dbg=dbg)
                else:             self.createLabel( p=self.cols,  j=j,   x=0, y=0, w=0,         h=0,         kk=self.cci(c, kc), g=self.g[C], why=why, kl=kc,      dbg=dbg)
                if QQ and not s:  self.createLabel( p=self.lcols, j=LLC, x=0, y=0, w=0,         h=0,         kk=self.cci(c, kc), g=self.g[C], why=why, kl=kc,      dbg=dbg)
                for t in range(nt):
                    if   tt and s == 0:
                        if   c == C1:  text = self.stringNumbs[t]   ;  plist = self.snos   ;  kl = kt2  ;  kk = self.cci(t, kl)  ;  j = O
                        elif c == C2:  text = self.stringCapo[t]    ;  plist = self.capsA  ;  kl = kt2  ;  kk = self.cci(t, kl)  ;  j = D
                        self.createLabel(p=plist, j=j, x=0, y=0, w=0, h=0, kk=kk, g=self.g[T], why=why, t=text, kl=kl, dbg=dbg)
                    elif nn and (s == 1 or (s == 0 and not tt)):
                        if   c == C1:  text = self.stringNames[t]   ;  plist = self.snas   ;  kl = kn2  ;  kk = self.cci(t, kl)  ;  j = A
                        elif c == C2:  text = self.stringCapo[t]    ;  plist = self.capsB  ;  kl = kn2  ;  kk = self.cci(t, kl)  ;  j = E
                        self.createLabel(p=plist, j=j, x=0, y=0, w=0, h=0, kk=kk, g=self.g[T], why=why, t=text, kl=kl, dbg=dbg)
                    elif kkk and (s == 2 or (s == 1 and (not tt or not nn)) or (s == 0 and (not tt and not nn))):
                        if   c == C1: text = self.strLabel[t]       ;  plist = self.lstrs  ;  kl = kk2  ;  kk = self.cci(t, kl)  ;  j = F
                        elif c == C2: text = self.cpoLabel[t]       ;  plist = self.lcaps  ;  kl = kk2  ;  kk = self.cci(t, kl)  ;  j = G
                        self.createLabel(p=plist, j=j, x=0, y=0, w=0, h=0, kk=kk, g=self.g[T], why=why, t=text, kl=kl, dbg=dbg)
        if SNAP and dbg: self.snapshot(f'showRLCols() {fmtl(self.TNIK)} {msg}')
        self.dumpGeom('END', msg)

    def COPY__showTabs(self, how, tnik):
        self.J1[L], self.J2[L] = 0, 0
        msg = f'SHOW {how} tnik={tnik}'
        self.dumpGeom('BGN', msg)
        if 0 not in self.TNIK: msg = f'ERROR TNIK={fmtl(self.TNIK)} is already full'   ;   self.log(msg)   ;   self.quit(msg)
        self.log(f'tnik={tnik} {fmtl(self.TNIK)}')
        self.toggleTnik(tnik)
        self.initJ(msg)
        for l, line in       enumerate(self.lines):
            self.J1[L] = l
            for s, sect in   enumerate(self.g_createLabelsA(line, S, self.sects, nn=1)):
                self.J1[S] = tnik
                for col in   self.g_createLabelsA(sect, C, self.cols,  nn=self.n[C]):
                    for _ in self.g_createLabelsC(col):
                        pass
        self.dumpJ(msg)
        self.dumpGeom('END', msg)

    def showRLCols(self, how):
        self.J1[L], self.J2[L] = 0, 0
        msg = f'SHOW {how} CCC={CCC}'
        self.dumpGeom('BGN', msg)
        for l, line in       enumerate(self.lines):
            self.J1[L] = l
            for s, sect in   enumerate(self.sects):
                self.J1[S] = self.TNIK[s % len(self.TNIK)]
                for col in   self.g_createLabelsA(sect, C, self.cols):
                    for _ in self.g_createLabelsC(col):
                        pass
    ####################################################################################################################################################################################################
    def toggleTnik(self, tnik, why=''):
        self.dumpGeom('BFR', why)
        self.TNIK[tnik] = int(not self.TNIK[tnik])   ;    self.n[S] = self.ss()
        self.dumpGeom('AFT', why)
    ####################################################################################################################################################################################################
    def toggleLLRows(self, how, dbg=0):
        global QQ  ;  QQ = int(not QQ)
        msg2 = f'{how} QQ={QQ}'
        self.dumpGeom('BGN', f'    {msg2}')
        if dbg: self.log(f'    llText={fmtl(self.llText[CCC])}')
        if QQ and not self.lrows: msg = 'SHOW'   ;   self.showLLRows()
        else:                     msg = 'HIDE'   ;   self.hideLLRows()
        self.on_resize(self.ww, self.hh, dbg=1)
        self.dumpGeom('END', f'{msg} {msg2}')

    def showLLRows(self, dbg=0):
        l = 0   ;   msg = 'SHOW '
        self.dumpGeom('BGN', msg)
        for l in range(len(self.lines)):
            self.createLLRow(self.lines[l], l)
        if SNAP and dbg: self.snapshot(f'showLLRows() l={l} {fmtl(self.TNIK)} {msg}')
        self.dumpGeom('END', msg)

    def hideLLRows(self, dbg=0):
        nr = len(self.lrows)    ;  nc = len(self.lcols)   ;   msg = 'HIDE '   ;   assert not nc % nr
        nc = nc // nr  #  normalize
        self.dumpGeom('BGN', msg)
        for rr in range(nr):
            self.hideLabel(self.lrows, rr, 'LLR')
            for cc in range(nc):
                self.hideLabel(self.lcols, cc + rr * nc, 'LLC')
        if SNAP and dbg: self.snapshot(f'hideLLRows() {fmtl(self.TNIK)} {msg}')
        self.dumpGeom('END', msg)
    ####################################################################################################################################################################################################
#        nt = self.n[T]   ;   ntl = nt * j1l  #        nl, il, xl, yl, wl, hl, gl, mx, my = self.geom(p=p, j=L)
#        if   type(p) is pyglet.text.Label:    p.y -= hl/2   ;   p.height *= ntl / (ntl + 1) / j1l   ;   self.log(f'ntl={ntl:2} jil={j1l} p.y = {p.y:7.2f} p.h = {p.height:7.2f}', pfx=0)
#        elif type(p) is pyglet.sprite.Sprite: my = (p.height - hl)/self.h[L]   ;   p.scale_y = my   ;   self.log(f'ntl={ntl:2} h[L]={self.h[L]} my={my:7.5f} p.y={p.y:7.2f} p.h={p.height:7.2f}', pfx=0)
#        p = self.createLabel(self.lines, L, xl, yl, wl, hl, klk, gl, why='new ', kl=kll, dbg=dbg)
#            self.createLabel(f'{Z*(c+1)}{sc}' if self.DF[LLC] and not c else text[c], LLC, self.lcols, xc + c*wc, yc, wc, hc, kkc, gc, why=f'new LC {sc}', kl=klc, dbg=dbg)
#            if not CCC and c == 0:  self.hideLabel(self.lcols, sc-1, f'Hide LLC {sc}')  #            if CCC == 1 and c == 1: self.hideLabel(self.lcols, sc-1, f'Hide LLC {sc}')
#        if   type(p) is pyglet.text.Label:    p.y -= hr/2   ;   p.height *= ntl / (ntl + 1) / j1l   ;   self.log(f'ntl={ntl:2} p.y = {p.y:7.2f} p.h = {p.height:7.2f}', pfx=0)
#        elif type(p) is pyglet.sprite.Sprite: my = (p.height - hr)/self.h[L]   ;   p.scale_y = my   ;   self.log(f'ntl={ntl:2} h[L]={self.h[L]} my={my:7.5f} p.y={p.y:7.2f} p.h={p.height:7.2f}', pfx=0)
    def createLLRow(self, p, pi, dbg=1, dbg2=0):
        klr = self.klr  ;  klc = self.klc  ;  kkr = self.cci(pi, klr) #        kll = self.kl   ;   klk = self.cci(pi, kll)
        nn1 = 1 + self.n[T] * self.ss() * self.i[L]
        nr, ir, xr, yr, wr, hr, gr, mx, my = self.geom(p=p, j=S, nn=nn1, dbg=dbg2)
        if SPRITES: xr += wr/2  ;  yr += hr/2
        self.J1[LLR] = pi   ;   nn2 = self.n[C]
        row = self.createLabel(self.lrows, LLR, xr, yr, wr, hr, kkr, gr, why='new ', kl=klr, dbg=dbg)
        nc, ic, xc, yc, wc, hc, gc, mx, my = self.geom(p=row, j=C, nn=nn2, dbg=dbg2)   ;  sc = nc * pi
        if SPRITES: xc += wc/2
        for c in range(nc):
            kkc = self.cci(pi, klc)
            sc += 1   ;   self.J1[LLC] = c
            text = self.llText[CCC] # index?
            txt = text[c] if text and len(text) >= c else ''
            self.createLabel(self.lcols, LLC, xc + c*wc, yc, wc, hc, kkc, gc, why='new ', t=txt, kl=klc, dbg=dbg)
        if dbg: self.log(f'pi={pi:3} px={p.x:7.2f} py={p.y:7.2f} pw={p.width:7.2f} ph={p.height:7.2f} nn1={nn1} nn2={nn2}', pfx=0)
        if dbg: self.log(f'nr={nr:3} xr={xr:7.2f} yr={yr:7.2f} wr={wr:7.2f} hr={hr:7.2f} row.y={row.y:7.2f} row.h={row.height:7.2f}', pfx=0)
        if dbg: self.log(f'nc={nc:3} xc={xc:7.2f} yc={yc:7.2f} wc={wc:7.2f} hc={hc:7.2f} sc={sc}', pfx=0)
        if   type(p) is pyglet.text.Label:    p.y, p.height = self.squeeze(p.y, p.height, 1 + self.n[T]*self.ss()*self.i[L])   ;   self.log(f'nn1={nn1:2} nn2={nn2:2} p.y = {p.y:7.2f} p.h = {p.height:7.2f}', pfx=0) if dbg else None
        elif type(p) is pyglet.sprite.Sprite: my = (p.height - hr)/self.h[L]   ;   p.scale_y = my    ;   self.log(f'nn1={nn1:2} nn2={nn2:2} h[L]={self.h[L]} my={my:7.5f} p.y={p.y:7.2f} p.h={p.height:7.2f}', pfx=0) if dbg else None
        return p

    def resizeLLRow(self, p, pi, dbg=0, dbg2=0):
        nn1 = 1 + self.n[T] * self.ss() * self.i[L]
        nr, ir, xr, yr, wr, hr, gr, mxr, myr = self.geom(p=p, j=S, nn=nn1, dbg=dbg2)
        if SPRITES: xr += wr/2  ;  yr += hr/2
        self.J1[LLR] = 0   ;   self.J2[LLR] += 1   ;   nn2 = self.n[C]
        row = self.lrows[pi]    ;    row.width = wr  ;   row.height = hr  ;   row.x = xr  ;   row.y = yr
        if dbg: self.dumpTNIK(row, *self.ids(), *self.cnts(), why=f'mod LLR {pi+1}')
        nc, ic, xc, yc, wc, hc, gc, mxc, myc = self.geom(p=row, j=C, nn=nn2, dbg=dbg2)   ;   sc = nc * pi
        if SPRITES: xc += wc/2
        for c in range(nc):
            self.J1[LLC] = c   ;   self.J2[LLC] += 1
            if sc >= len(self.lcols):   self.showLabel(sc, self.lcols, LLC, g=self.g[C], k=self.klc)  ;   self.log(f'ERROR need to add label CCC={CCC} row={pi+1} c={c} sc={sc} len={len(self.lcols)}')
            col = self.lcols[sc]
            col.text = self.llText[CCC][c]        ;   sc += 1
            col.width = wc   ;   col.height = hc  ;   col.x = xc + c * wc  ;  col.y = yc
            if dbg: self.dumpTNIK(col, *self.ids(), *self.cnts(), why=f'mod LLC {sc}')
        if dbg: self.log(f'pi={pi:3} px={p.x:7.2f} py={p.y:7.2f} pw={p.width:7.2f} ph={p.height:7.2f} nn1={nn1} nn2={nn2}', pfx=0)
        if dbg: self.log(f'nr={nr:3} xr={xr:7.2f} yr={yr:7.2f} wr={wr:7.2f} hr={hr:7.2f} row.y={row.y:7.2f} row.h={row.height:7.2f}', pfx=0)
        if dbg: self.log(f'nc={nc:3} xc={xc:7.2f} yc={yc:7.2f} wc={wc:7.2f} hc={hc:7.2f} sc={sc}', pfx=0)
        if   type(p) is pyglet.text.Label:    p.y, p.height = self.squeeze(p.y, p.height, 1 + self.n[T]*self.ss()*self.i[L])   ;   self.log(f'nn1={nn1:2} nn2={nn2:2} p.y = {p.y:7.2f} p.h = {p.height:7.2f}', pfx=0) if dbg else None
        elif type(p) is pyglet.sprite.Sprite: my = (p.height - hr)/self.h[L]   ;   p.scale_y = my   ;      self.log(f'nn1={nn1:2} nn2={nn2} h[L]={self.h[L]} my={my:7.5f} p.y={p.y:7.2f} p.h={p.height:7.2f}', pfx=0) if dbg else None
        return p
#        if   type(p) is pyglet.text.Label:    p.y -= hr/2   ;   p.height *= ntl / (ntl + 1) / j1l   ;   self.log(f'ntl={ntl:2} p.y = {p.y:7.2f} p.h = {p.height:7.2f}', pfx=0)
#        elif type(p) is pyglet.sprite.Sprite: my = (p.height - hr)/self.h[L]   ;   p.scale_y = my   ;   self.log(f'ntl={ntl:2} h[L]={self.h[L]} my={my:7.5f} p.y={p.y:7.2f} p.h={p.height:7.2f}', pfx=0)
#        if dbg2: self.log(f'p.y -= hr/2 = {p.y:7.2f}, p.height -= h = {p.height:7.2f}  w={fmtl(self.w)} h={fmtl(self.h)}', pfx=0)
    def squeeze(self, y, h, a):  self.log(f'y={y:6.2f} h={h:6.2f} a={a}', end=' ')  ;  b = h/a  ;  h -= b  ;  y -= b/2  ;  self.log(f' b={b:6.2f} y={y:6.2f} h={h:6.2f}', pfx=0)  ;  return y, h
    ####################################################################################################################################################################################################
    def toggleTabs(self, how, tnik):
        msg2 = f'{how} tnik={tnik}'
        self.dumpGeom(f'BGN', f'     {msg2}')
        if   not self.TNIK[tnik] and not self.B[tnik]: msg = 'SHOW'   ;   self.showTabs(how, tnik)
        elif     self.TNIK[tnik]:                      msg = 'HIDE'   ;   self.hideTabs(how, tnik)
        else:                                          msg = 'SKIP'   ;   self.dumpGeom('   ', f'{msg} {msg2}')   ;   self.toggleTnik(tnik)
        self.on_resize(self.ww, self.hh, dbg=1)
        self.dumpGeom('END', f'{msg} {msg2}')
    ####################################################################################################################################################################################################
    def showTabs(self, how, tnik):
        self.J1[L], self.J2[L] = 0, 0
        msg = f'SHOW {how} tnik={tnik}'
        self.dumpGeom('BGN', msg)
        if 0 not in self.TNIK: msg = f'ERROR TNIK={fmtl(self.TNIK)} is already full'   ;   self.log(msg)   ;   self.quit(msg)
        self.log(f'tnik={tnik} {fmtl(self.TNIK)}')
        self.toggleTnik(tnik)
        self.initJ(msg)
        for l, line in       enumerate(self.lines):
            self.J1[L] = l
            for s, sect in   enumerate(self.g_createTNIKsA(line, S, self.sects, nn=1)):
                self.J1[S] = tnik
                for col in   self.g_createTNIKsA(sect, C, self.cols,  nn=self.n[C]):
                    for _ in self.g_createTNIKsC(col):
                        pass
        self.dumpJ(msg)
        self.dumpGeom('END', msg)

    def hideTabs(self, how, tnik):
        msg = f'HIDE {how} tnik={tnik}'
        ttype = 'Tab' if tnik == TT  else 'Note' if tnik == NN else 'Ikey' if tnik == II else 'Chord' if tnik == KK else '???'
        np, nl, ns, nc, nt = self.n
        self.dumpGeom('BGN', msg)
        for l in range(nl):
            s = self.ss() * (l + 1) - 1
            self.hideLabel(self.sects, s, 'Sect', dbg=1)
            for c in range(nc):
                self.hideLabel(self.cols, nc * s + c, 'Col', dbg=1)
        for t in range(len(self.B[tnik])):
            self.hideLabel(self.B[tnik], t, ttype)
        self.toggleTnik(tnik)
        if SNAP: self.snapshot(f'hideTabs() {fmtl(self.TNIK)} {msg}')
        self.dumpGeom('END', msg)
    ####################################################################################################################################################################################################
    def geom(self, p=None, j=0, init=0, nn=0, dbg=0):
        mx, my = -1, -1  ;   msg = ''  ;  iw, ih =  self.w[j], self.h[j]
        n, i, x, y, w, h, g = self.n[j], self.i[j], self.x[j], self.y[j], self.w[j], self.h[j], self.g[j]
        if   n == 0:            n = 1   ;  msg  = f'WARN j={j} setting n=0 -> n=1 -> n=0'
        if   nn:                n = nn
        elif j == C:            n += CCC     #    if   j >= T:            n += QQ
        if   p is None:         w =  self.ww - x*2           ;  h =  self.hh  - y*2
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
        if init:                self.w[j] = w                ;  self.h[j] = h  # if not nn and init:
        elif iw and ih:         mx = w/iw                    ;  my = h/ih
        if   msg:               n = 0                        ;  self.log(msg, pfx=0)
        if   dbg: self._dumpGeom(j, n, i, x, y, w, h, mx, my, iw, ih, nn, p)
        return n, i, x, y, w, h, g, mx, my
    ####################################################################################################################################################################################################
    def _dumpGeom(self, j, n, i, x, y, w, h, mx, my, iw, ih, nn, p):
        px, py, pw, ph = None, None, None, None
        if p: px, py, pw, ph = p.x, p.y, p.width, p.height
        if p: self.log(FMTR.format(f'  {j}  {n:3} {i:4}   {x:7.2f} {y:7.2f} {w:7.2f} {h:7.2f} {mx:6.3f} {my:6.3f}  {iw:7.2f} {ih:7.2f} {nn:3} {JTEXTS[j]:6} {px:7.2f} {py:7.2f} {pw:7.2f} {ph:7.2f}'), pfx=0, file=sys.stdout)
        else: self.log(FMTR.format(f'  {j}  {n:3} {i:4}   {x:7.2f} {y:7.2f} {w:7.2f} {h:7.2f} {mx:6.3f} {my:6.3f}  {iw:7.2f} {ih:7.2f} {nn:3} {JTEXTS[j]:6}'), pfx=0, file=sys.stdout)
#        self.log(f'  {j}  {n:3} {i:4}   {x:7.2f} {y:7.2f} {w:7.2f} {h:7.2f} {mx:6.3f} {my:6.3f}  {iw:7.2f} {ih:7.2f} {nn:3} {JTEXTS[j]} {px:7.2f} {py:7.2f} {pw:7.2f} {ph:7.2f}', pfx=0, file=sys.stdout)
    ####################################################################################################################################################################################################
    def createTNIKs(self):
        self.dumpGeom('BGN')
        self.dumpTNIK()
        for page in              self.g_createTNIKsA(None, P, self.pages):
            for line in          self.g_createTNIKsA(page, L, self.lines):
                for sect in      self.g_createTNIKsB(line, S, self.sects):
                    for col in   self.g_createTNIKsA(sect, C, self.cols):
                        for _ in self.g_createTNIKsC(col):
                            pass
        self.dumpTNIK()
        self.dumpGeom('END')
    ####################################################################################################################################################################################################
    def g_createTNIKsA(self, p, j, plist, nn=0, dbg=1, dbg2=0):
        n, i, x, y, w, h, g, mx, my = self.geom(p=p, j=j, init=1, nn=nn, dbg=dbg2)   ;   kl = self.k[j]   ;  x2 = x  ;  y2 = y   ;   v = 0
        for i in range(n):
            if   j == C:       x2 = x + i * w
            elif p:            y2 = y - i * h
            self.J1[j] = i
            if   j == P:       v=1 if self.J2[P] == self.i[P] else 0
            if nn and j != L:  self.J2[j] = len(self.E[j])
            tnik = self.createTNIK(plist, j, x2, y2, w, h, self.cci(j, kl), g, why='new ', kl=kl, v=v, dbg=dbg)
#            if SPRITES: tnik = self.createSprite(plist, j, x2, y2, w, h, self.cci(j, kl), g, why='new ', kl=kl, v=v, dbg=dbg)
#            else:       tnik = self.createLabel( plist, j, x2, y2, w, h, self.cci(j, kl), g, why='new ', kl=kl,      dbg=dbg)
            if QQ and j == L:  self.createLLRow(tnik, i)
            yield tnik

    def g_createTNIKsB(self, p, j, plist, nn=0, dbg=1, dbg2=0):
        n, i, x, y, w, h, g, mx, my = self.geom(p=p, j=j, init=1, nn=nn, dbg=dbg2)   ;   kl = self.k[j]   ;  x2 = x   ;   i2 = 0
        self.log(f'{fmtl(self.TNIK)} n={fmtl(self.n)} j={j} nn={nn} n={n}')
        for i, t in enumerate(self.TNIK):
            if t: y2 = y - i2 * h   ;   i2 += 1
            else: continue
            self.log(f'i={i} i2={i2} t={t} J1={fmtl(self.J1)} J2={fmtl(self.J2)}')
            self.J1[j] = i   ;   self.J2[j] = len(self.E[j])   ;   v=1 if self.J2[P] == self.i[P] else 0
            tnik = self.createTNIK(plist, j, x2, y2, w, h, self.cci(j, kl), g, why='new ', kl=kl, v=v, dbg=dbg)
#            if SPRITES: tnik = self.createSprite(plist, j, x2, y2, w, h, self.cci(j, kl), g, why='new ', kl=kl, v=v, dbg=dbg)
#            else:       tnik = self.createLabel( plist, j, x2, y2, w, h, self.cci(j, kl), g, why='new ', kl=kl, dbg=dbg)
            yield tnik
    ####################################################################################################################################################################################################
    def g_createTNIKsC(self, col, dbg=1, dbg2=0):
        p, l, s, c = self.J1[P], self.J1[L], self.J1[S], self.J1[C]    ;   t2 = 0   ;   stnik = self.ss()
        kt, kn, ki, kkk = self.kt, self.kn, self.ki, self.kk           ;   kt2, kn2, ki2, kk2 = self.kt2, self.kn2, self.ki2, self.kk2
        n, i, x, y, w, h, g, mx, my = self.geom(p=col, j=T, init=1, dbg=dbg2)
        imap = self.getImap(p, l, c, s)
        for t in range(n):
            why = 'new '
            if   s == TT: # and self.TNIK[TT]:
                if   CCC     and c == C1:   tab = self.stringNumbs[t]  ;  plist = self.snos   ;  kl = kt2  ;  k = self.cci(t, kl)  ;  j = O
                elif CCC > 1 and c == C2:   tab = self.stringCapo[t]   ;  plist = self.capsA  ;  kl = kt2  ;  k = self.cci(t, kl)  ;  j = D
                else:               tab = self.data[p][l][c-CCC][t]    ;  plist = self.tabs   ;  kl = kt   ;  k = self.cci(t, kl)  ;  j = T
                self.createTNIK(plist, j, x, y - t*h, w, h, k, g, why=why, t=tab,  kl=kl, dbg=dbg)  ;  yield tab
            elif s == NN: # and self.TNIK[NN]:
                if   CCC     and c == C1:  note = self.stringNames[t]  ;  plist = self.snas   ;  kl = kn2  ;  k = self.cci(t, kl)  ;  j = A
                elif CCC > 1 and c == C2:  note = self.stringCapo[t]   ;  plist = self.capsB  ;  kl = kn2  ;  k = self.cci(t, kl)  ;  j = E
                else:               tab = self.data[p][l][c-CCC][t]    ;  plist = self.notes  ;  kl = kn   ;  k = self.cci(t, kl)  ;  j = N  ;  note = self.tab2nn(tab, t) if self.isFret(tab) else self.tblank
                self.createTNIK(plist, j, x, y - t*h, w, h, k, g, why=why, t=note, kl=kl, dbg=dbg)  ;  yield note
            elif s == II: # and self.TNIK[II]:
                if   CCC     and c == C1:  ikey = self.strLabel[t]     ;  plist = self.lstrs  ;  kl = kk2  ;  k = self.cci(t, kl)  ;  j = F
                elif CCC > 1 and c == C2:  ikey = self.cpoLabel[t]     ;  plist = self.lcaps  ;  kl = kk2  ;  k = self.cci(t, kl)  ;  j = G
                else:
                    imap0 = imap[0][::-1] if imap and len(imap) else []
                    dd = self.data[p][l][c]   ;   fdd = self.isFret(dd[t])   ;   j = I
                    if imap0 and len(imap0) > t2: ikey = imap0[t2] if fdd else self.tblank    ;   t2 += 1 if fdd else 0
                    else:                         ikey = self.tblank
                    if dbg2: cc = self.plct2cc(p, l, c, 0)   ;   self.dumpDataSlice(p, l, c, cc)  ;  self.log(f'cc={cc} t={t} t2={t2} imap0={imap0} fdd={fdd} dd={dd} ikey={ikey}')
                    plist = self.ikeys  ;  kl = ki  ;  k = self.cci(t, kl)
                self.createTNIK(plist, j, x, y - (n-1-t)*h, w, h, k, g, why=why, t=ikey, kl=ki, dbg=dbg)   ;  yield ikey
            elif s == KK: # and self.TNIK[KK]:
                if   CCC     and c == C1: chord = self.strLabel[t]     ;  plist = self.lstrs  ;  kl = kk2  ;  k = self.cci(t, kl)  ;  j = F
                elif CCC > 1 and c == C2: chord = self.cpoLabel[t]     ;  plist = self.lcaps  ;  kl = kk2  ;  k = self.cci(t, kl)  ;  j = G
                else:
                    chunks = imap[4] if (imap and len(imap) > 4) else []
                    chord = chunks[t] if len(chunks) > t else self.tblank   ;   j = K
                    plist = self.chords ;  kl = kkk ;  k = self.cci(t, kl)
                self.createTNIK(plist, j, x, y - t*h, w, h, k, g, why=why, t=chord, kl=kl, dbg=dbg) ;  yield chord
            elif not stnik and not s: self.log(f'WARN skip s={s} {fmtl(self.TNIK)} stnik={stnik}') if dbg2 else None
    ####################################################################################################################################################################################################
    def resizeTNIKs(self):
        self.dumpGeom('BGN')
        self.dumpTNIK()
        for page in              self.g_resizeTNIKsA(None, P, self.pages, why=JTEXTS[P]):
            for line in          self.g_resizeTNIKsA(page, L, self.lines, why=JTEXTS[L]):
                for sect in      self.g_resizeTNIKsB(line, S, self.sects, why=JTEXTS[S]):
                    for col in   self.g_resizeTNIKsA(sect, C, self.cols,  why=JTEXTS[C]):
                        for _ in self.g_resizeTNIKsC(col):
                            pass
        self.dumpTNIK()
        self.dumpGeom('END')
    ####################################################################################################################################################################################################
    def g_resizeTNIKsA(self, p, j, plist, why, dbg=1, dbg2=0):
        n, i, x, y, w, h, g, mx, my = self.geom(p=p, j=j, dbg=dbg2)   ;   x2 = x   ;   y2 = y
        for tt in range(n):
            if   j == C:          x2 = x + tt * w
            elif p:               y2 = y - tt * h
            assert(len(plist))
            tnik = plist[self.J2[j]]
            if SPRITES or j < 0:  tnik.update(x=x2, y=y2, scale_x=mx, scale_y=my)
            else:                 tnik.x = x2  ;  tnik.y = y2  ;  tnik.width = w  ;  tnik.height = h
            self.J1[j] = tt   ;   self.J2[j] += 1
#            if   dbg and SPRITES: self.dumpSprite(tnik, *self.ids(), *self.cnts(), why=f'mod {why} {self.J2[j]}')
#            elif dbg:             self.dumpLabel( tnik, *self.ids(), *self.cnts(), why=f'mod {why} {self.J2[j]}')
            if dbg:               self.dumpTNIK(tnik, *self.ids(), *self.cnts(), why=f'mod {why} {self.J2[j]}')
            if QQ and j == L:     self.resizeLLRow(tnik, tt)
            yield tnik

    def g_resizeTNIKsB(self, p, j, plist, why, dbg=1, dbg2=0):
        n, i, x, y, w, h, g, mx, my = self.geom(p=p, j=j, dbg=dbg2)   ;   x2 = x   ;   i2 = 0
        for i, t in enumerate(self.TNIK):
            if t: y2 = y - i2 * h   ;   i2 += 1
            else: continue
            assert(len(plist))
            tnik = plist[self.J2[j]]
            if j < 0 or (SPRITES and j < T):  tnik.update(x=x2, y=y2, scale_x=mx, scale_y=my)
            else:                             tnik.x = x2  ;  tnik.y = y2  ;  tnik.width = w  ;  tnik.height = h
            self.J1[j] = i   ;    self.J2[j] += 1
            if dbg:               self.dumpTNIK(tnik, *self.ids(), *self.cnts(), why=f'mod {why} {self.J2[j]}')
#            if   dbg and SPRITES: self.dumpSprite(tnik, *self.ids(), *self.cnts(), why=f'mod {why} {self.J2[j]}')
#            elif dbg:             self.dumpLabel( tnik, *self.ids(), *self.cnts(), why=f'mod {why} {self.J2[j]}')
            yield tnik
    ####################################################################################################################################################################################################
    def g_resizeTNIKsC(self, col, dbg=1, dbg2=0):
        tab, note, ikey, chord = None, None, None, None   ;   stnik = self.ss()
        p,       l,    s,    c      = self.J1[P], self.J1[L], self.J1[S], self.J1[C]
        st,     sn,   si,   sk      = self.J2[T], self.J2[N], self.J2[I], self.J2[K]
        ssno, ssna, scapA, scapB, slstr, slcap =  self.J2[O], self.J2[A], self.J2[D], self.J2[E], self.J2[F], self.J2[G]
        n, i, x, y, w, h, g, mx, my = self.geom(p=col, j=T, dbg=dbg2)   ;   lbl = None   ;   why0 = f'{s}'
        for t in range(n):
            why = f'{why0} mod '
            if   s == TT: # and self.TNIK[TT]:
                if   CCC     and c == C1:   tab = self.snos[ssno]     ;   ssno += 1   ;  why += f'SNo {ssno}'
                elif CCC > 1 and c == C2:   tab = self.capsA[scapA]   ;  scapA += 1   ;  why += f'CapA {scapA}'
                elif st < len(self.tabs):   tab = self.tabs[st]       ;     st += 1   ;  why += f'Tab {st}'
                else: msg = f'ERROR indexing {why0} sn={st} len={len(self.tabs)}'   ;   self.dumpGeom(msg)   ;   self.quit(msg)
                tab.width = w    ;   tab.height = h    ;  tab.x = x   ;   tab.y = y - t * h
                self.J1[T] = t   ;   self.J2[T] = st   ;  self.J2[O] = ssno   ;  self.J2[D] = scapA  ;  tnik = tab
                if dbg:              self.dumpTNIK(tnik, *self.ids(), *self.cnts(), why=f'{why} {self.J2[TT]}')
#                if dbg:   self.dumpLabel(tnik, *self.ids(), *self.cnts(), why=why)
            elif s == NN: #  and self.TNIK[NN]:
                if   CCC     and c == C1:  note = self.snas[ssna]     ;   ssna += 1   ;  why += f'SNam {ssna}'
                elif CCC > 1 and c == C2:  note = self.capsB[scapB]   ;  scapB += 1   ;  why += f'CapB {scapB}'
                elif sn < len(self.notes): note = self.notes[sn]      ;     sn += 1   ;  why += f'Note {sn}'
                else: msg = f'ERROR indexing {why0} sn={sn} len={len(self.notes)}'   ;   self.dumpGeom(msg)   ;   self.quit(msg)
                note.width = w   ;  note.height = h    ; note.x = x   ;  note.y = y - t * h  ; tnik = note
                self.J1[N] = t   ;   self.J2[N] = sn   ;  self.J2[A] = ssna   ;  self.J2[E] = scapB
                if dbg:              self.dumpTNIK(tnik, *self.ids(), *self.cnts(), why=f'{why} {self.J2[NN]}')
#                if dbg:   self.dumpLabel(lbl, *self.ids(), *self.cnts(), why=why)
            elif s == II: #  and self.TNIK[II]:
                if   CCC     and c == C1:  ikey = self.lstrs[slstr]   ;  slstr += 1   ;  why += f'LStr {slstr}'
                elif CCC > 1 and c == C2:  ikey = self.lcaps[slcap]   ;  slcap += 1   ;  why += f'LCap {slcap}'
                elif si < len(self.ikeys): ikey = self.ikeys[si]      ;     si += 1   ;  why += f'IKey {si}'
                else: msg = f'ERROR indexing {why0} si={si} len={len(self.ikeys)}'   ;   self.dumpGeom(msg)    ;   self.quit(msg)
                ikey.width = w  ;  ikey.height = h    ;  ikey.x = x  ;  ikey.y = y - t * h  ;  tnik = ikey
                self.J1[I] = t   ;   self.J2[I] = si   ;  self.J2[F] = slstr  ;  self.J2[G] = slcap
#                if dbg:   self.dumpLabel(lbl, *self.ids(), *self.cnts(), why=why)
                if dbg:              self.dumpTNIK(tnik, *self.ids(), *self.cnts(), why=f'{why} {self.J2[II]}')
            elif s == KK: #  and self.TNIK[KK]:
                if   CCC     and c == C1:   chord = self.lstrs[slstr]   ;  slstr += 1   ;  why += f'LStr {slstr}'
                elif CCC > 1 and c == C2:   chord = self.lcaps[slcap]   ;  slcap += 1   ;  why += f'LCap {slcap}'
                elif sk < len(self.chords): chord = self.chords[sk]     ;     sk += 1   ;  why += f'Chord {sk}'
                else: msg = f'ERROR indexing {why0} sk={sk} len={len(self.chords)}'   ;   self.dumpGeom(msg)   ;   self.quit(msg)
                chord.width = w  ; chord.height = h    ; chord.x = x  ; chord.y = y - t * h  ;  tnik = chord
                self.J1[K] = t   ;   self.J2[K] = sk   ;  self.J2[F] = slstr  ;  self.J2[G] = slcap
                if dbg:              self.dumpTNIK(tnik, *self.ids(), *self.cnts(), why=f'{why} {self.J2[KK]}')
#                if dbg:   self.dumpLabel(lbl, *self.ids(), *self.cnts(), why=why)
            else: msg = f'ERROR skip {why0} {fmtl(self.TNIK)} {stnik}'   ;   self.dumpGeom()    ;   self.quit(msg)
            yield lbl
    ####################################################################################################################################################################################################
    def createSprite(self, p, j, x, y, w, h, kk, g, why, kl=None, v=0, dbg=0):
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

    def createTNIK(self, p, j, x, y, w, h, kk, g, why, t='', v=0, kl=None, m=0, dbg=0):
        self.J2[j] += 1   ;   why += JTEXTS[j] + f' {self.J2[j]}' if j >= 0 else ''
        o, k, d, i, n, s = self.fontParams()   ;   b = self.batch   ;   k2 = kk if not SPRITES else 0
        k = FONT_COLORS[(k + k2) % len(FONT_COLORS)] if kl is None else kl[kk]
        if j < 0 or (SPRITES and j < T):
            scip = pyglet.image.SolidColorImagePattern(k)
            img = scip.create_image(width=fri(w), height=fri(h))
            tnik = pyglet.sprite.Sprite(img, x, y, batch=b, group=g, subpixel=SUBPIX)
            tnik.color, tnik.opacity, tnik.visible = k[:3], k[3], v
        else:
            d, n = FONT_DPIS[d], FONT_NAMES[n]   ;   a, ax, ay = 'center', 'center', 'center' # left center right  # bottom baseline center top
            mp = len(p) % (self.n[C] + CCC) + 1 - CCC if j == LLC else 0
            if j == LLC and not mp % 10: k = self.kll[0]
            if m: t = [ t[:i] + '\n' + t[i:] for i in range(len(t), 0, -1) ]
            tnik = pyglet.text.Label(t, font_name=n, font_size=s, bold=o, italic=i, color=k, x=x, y=y, width=w, height=h, anchor_x=ax, anchor_y=ay, align=a, dpi=d, batch=b, group=g, multiline=m)
        self.tniks.append(tnik)   ;   p.append(tnik) if p is not None else None
#        if dbg: self.dumpSprite(tnik, *self.ids(), *self.cnts(), why) if     SPRITES or  j == -1 else None
#        if dbg: self.dumpLabel( tnik, *self.ids(), *self.cnts(), why) if not SPRITES and j != -1 else None
#        if j < 0 or (SPRITES and j < T): self.dumpSprite(tnik, *self.ids(), *self.cnts(), why) if dbg else None
#        else:                            self.dumpLabel( tnik, *self.ids(), *self.cnts(), why) if dbg else None
        if dbg:              self.dumpTNIK(tnik, *self.ids(), *self.cnts(), why=f'{why} {self.J2[j]}')
        return tnik

    def createLabel(self, p, j, x, y, w, h, kk, g, why, t='', kl=None, m=0, dbg=0):
        j1, j2 = self.J1, self.J2   ;   mp = len(p) % (self.n[C] + CCC) + 1 - CCC if j == LLC else 0
        j2[j] += 1   ;   why += JTEXTS[j] + f' {j2[j]}'
        a, ax, ay = 'center', 'center', 'center' # left center right  # bottom baseline center top
        b = self.batch
        o, k, d, ii, n, s = self.fontParams()
        d = FONT_DPIS[d]
        n = FONT_NAMES[n]
        k = FONT_COLORS[kk % len(FONT_COLORS)] if kl is None else kl[kk]
        if m: t = [ t[:i] + '\n' + t[i:] for i in range(len(t), 0, -1) ]
        if j == LLC and not mp % 10: k = self.kll[0]
#        if len(p) > j2[j]:   self.log(f'ERROR Label Exists? len(p)={len(p)} j={j} j2[j]={j2[j]}')   # ;  self.quit('ERROR Unexpected if')
        lbl = pyglet.text.Label(t, font_name=n, font_size=s, bold=o, italic=ii, color=k, x=x, y=y, width=w, height=h, anchor_x=ax, anchor_y=ay, align=a, dpi=d, batch=b, group=g, multiline=m)
        self.labels.append(lbl)    ;    p.append(lbl)
        if dbg: self.dumpTNIK(lbl, *self.ids(), *self.cnts(), why)
        return lbl
    ####################################################################################################################################################################################################
    def dumpSprites(self, why=''):
        self.initJ(why)
        self.dumpGeom('BGN', why)
        np, nl, ns, nc, nt = self.n    ;    i, sp, sl, ss, sc = 0, 0, 0, 0, 0
        self.log(f'BGN plsct {np} {nl} {ns} {nc} {nt}')
        self.dumpTNIK()
        for p in range(np):
            sp += 1                   ;   self.J1[P] = sp  ;  self.J2[P] += 1  ;  self.dumpTNIK(self.sprites[i], *self.ids(), *self.cnts(), why=f'{why} Page {sp}') ; i += 1
            for l in range(nl):
                sl += 1               ;   self.J1[L] = sl  ;  self.J2[L] += 1  ;  self.dumpTNIK(self.sprites[i], *self.ids(), *self.cnts(), why=f'{why} Line {sl}') ; i += 1
                for s in range(ns):
                    ss += 1           ;   self.J1[S] = ss  ;  self.J2[S] += 1  ;  self.dumpTNIK(self.sprites[i], *self.ids(), *self.cnts(), why=f'{why} Sect {ss}') ; i += 1
                    for c in range(nc):
                        sc += 1       ;   self.J1[C] = sc  ;  self.J2[C] += 1  ;  self.dumpTNIK(self.sprites[i], *self.ids(), *self.cnts(), why=f'{why} Col {sc}')  ; i += 1
        self.dumpTNIK()             ;   self.dumpJ(why)
        self.log(f'END plsct {np} {nl} {ns} {nc} {nt}')
        self.dumpGeom('END', why)

    def dumpLabels(self, why='', dbg=0):
        self.initJ(why)
        np, nl, ns, nc, nt = self.n  ;  nc += CCC
        i, sp, sl, ss, sc, st, sn, si, sk = 0, 0, 0, 0, 0, 0, 0, 0, 0   ;   qr, qc = 0, 0
        self.dumpGeom('BGN', f'{why}')
        self.dumpTNIK()
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
                                if   s == 0:  st += 1  ;  self.J1[T] = st  ;  self.J2[T] += 1  ;  self.dumpTNIK(self.labels[i], *self.ids(), *self.cnts(), why=f'{why} Tab {st}')    ;  i += 1
                                elif s == 1:  sn += 1  ;  self.J1[N] = sn  ;  self.J2[N] += 1  ;  self.dumpTNIK(self.labels[i], *self.ids(), *self.cnts(), why=f'{why} Note {sn}')   ;  i += 1
                                elif s == 2:  si += 1  ;  self.J1[I] = si  ;  self.J2[I] += 1  ;  self.dumpTNIK(self.labels[i], *self.ids(), *self.cnts(), why=f'{why} IKey {si}')   ;  i += 1
                                elif s == 3:  sk += 1  ;  self.J1[K] = sk  ;  self.J2[K] += 1  ;  self.dumpTNIK(self.labels[i], *self.ids(), *self.cnts(), why=f'{why} Chord {sk}')  ;  i += 1
        else:
            for p in range(np):
                sp += 1                                ;   self.J1[P] = sp  ;  self.J2[P] += 1  ;  self.dumpTNIK(self.labels[i], *self.ids(), *self.cnts(), why=f'{why} Page {sp}')   ;  i += 1
                for l in range(nl):
                    sl += 1                            ;   self.J1[L] = sl  ;  self.J2[L] += 1  ;  self.dumpTNIK(self.labels[i], *self.ids(), *self.cnts(), why=f'{why} Line {sl}')   ;  i += 1
                    for q in range(QQ):
                        qr += 1                        ;  self.J1[LLR] = qr ;  self.J2[LLR] += 1 ;  self.dumpTNIK(self.labels[i], *self.ids(), *self.cnts(), why=f'{why} LLR {qr}')   ;  i += 1
                        for c in range(nc):
                            qc += 1                    ; self.J1[LLC] = qc  ;  self.J2[LLC] += 1 ;  self.dumpTNIK(self.labels[i], *self.ids(), *self.cnts(), why=f'{why} LLC {qc}')   ;  i += 1
                    for s in range(ns):
                        ss += 1                        ;   self.J1[S] = ss  ;  self.J2[S] += 1  ;  self.dumpTNIK(self.labels[i], *self.ids(), *self.cnts(), why=f'{why} Sect {ss}')   ;  i += 1
                        for c in range(nc):
                            sc += 1                    ;   self.J1[C] = sc  ;  self.J2[C] += 1  ;  self.dumpTNIK(self.labels[i], *self.ids(), *self.cnts(), why=f'{why} Col {sc}')    ;  i += 1
                            for t in range(nt):
                                if   self.tt0(s) == TT:  st += 1  ;   self.J1[T] = st  ;  self.J2[T] += 1  ;  self.dumpTNIK(self.labels[i], *self.ids(), *self.cnts(), why=f'{why} Tab {st}')    ;  i += 1
                                elif self.tt0(s) == NN:  sn += 1  ;   self.J1[N] = sn  ;  self.J2[N] += 1  ;  self.dumpTNIK(self.labels[i], *self.ids(), *self.cnts(), why=f'{why} Note {sn}')   ;  i += 1
                                elif self.tt0(s) == II:  si += 1  ;   self.J1[I] = si  ;  self.J2[I] += 1  ;  self.dumpTNIK(self.labels[i], *self.ids(), *self.cnts(), why=f'{why} IKey {si}')   ;  i += 1
                                elif self.tt0(s) == KK:  sk += 1  ;   self.J1[K] = sk  ;  self.J2[K] += 1  ;  self.dumpTNIK(self.labels[i], *self.ids(), *self.cnts(), why=f'{why} Chord {sk}')  ;  i += 1
                                else: self.log(f'ERROR {i} {fmtl(self.n)} {fmtl(self.TNIK)} {p}/{np} {l}/{nl} {s}/{ns} {c}/{nc} {t}/{nt} {fmtl(self.lenE())}')
        self.dumpTNIK()   ;   self.dumpJ(why)
        if dbg: self.dumpGeom('END', why)
        self.log(f'END plsct {np} {nl} {ns} {nc} {nt}')

    def dumpTabs(self, why='', dbg=VERBOSE):
        self.initJ(why)
        if dbg: self.dumpGeom('BGN', why)
        i, st, sn, si, sk = 0, 0, 0, 0, 0   ;   np, nl, ns, nc, nt = self.n   # ;   nc += CCC
        self.dumpTNIK()
        for p in range(np):
            for l in range(nl):
                for s in range(ns):
                    for c in range(nc):
                        for t in range(nt):
                            if   self.tt0(s) == TT:  st += 1  ;  self.J1[T] = st  ;  self.J2[T] += 1  ;  self.dumpTNIK(self.tabs[st-1],   *self.ids(), *self.cnts(), why=f'{why} Tab {st}')    ;  i += 1
                            elif self.tt0(s) == NN:  sn += 1  ;  self.J1[N] = sn  ;  self.J2[N] += 1  ;  self.dumpTNIK(self.notes[sn-1],  *self.ids(), *self.cnts(), why=f'{why} Note {sn}')   ;  i += 1
                            elif self.tt0(s) == II:  si += 1  ;  self.J1[I] = si  ;  self.J2[I] += 1  ;  self.dumpTNIK(self.ikeys[si-1],  *self.ids(), *self.cnts(), why=f'{why} IKey {si}')   ;  i += 1
                            elif self.tt0(s) == KK:  sk += 1  ;  self.J1[K] = sk  ;  self.J2[K] += 1  ;  self.dumpTNIK(self.chords[sk-1], *self.ids(), *self.cnts(), why=f'{why} Chord {sk}')  ;  i += 1
        self.dumpTNIK()   ;   self.dumpJ(why)
        if dbg: self.dumpGeom('END', why)

    def dumpCols(self, why='', dbg=VERBOSE):
        self.initJ(why)
        if dbg: self.dumpGeom('BGN', why)
        self.dumpTNIK()
        for i in range(len(self.cols)):
            self.J1[C] = i  ;  self.J2[C] += 1  ;  self.dumpTNIK(self.cols[i], *self.ids(), *self.cnts(), why=f'{why} Col {i+1}')
        self.dumpTNIK()   ;   self.dumpJ(why)
        if dbg: self.dumpGeom('END', why)
    ####################################################################################################################################################################################################
    def OLD_1_dumpSprite(self, b=None, sid=-1, lid=-1, p=-1, l=-1, s=-1, c=-1, t=-1, n=-1, i=-1, k=-1, o=-1, a=-1, d=-1, e=-1, f=-1, g=-1, r=-1, z=-1, why=''):
        if b is None: self.log(f' sid  lid p  l  s   c   t   n   i   k   z    x       y       w       h        v     identity   mx    my   red grn blu opc   why          group       parent', pfx=0); return
        ff = '{:4} {:4} {} {:2} {:2} {:3} {:3} {:3} {:3} {:3} {:3} {:7.2f} {:7.2f} {:7.2f} {:7.2f}     {:1} {:13} {:5.3f} {:5.3f} {:3} {:3} {:3} {:3} {:12} {} {}'
        kk, oo, v, gg, pg    =    b.color, b.opacity, b.visible, b.group, b.group.parent   ;   ID = hex(id(b))   ;   z += r   ;   i += o + a + d + e + f + g
        x, y, w, h, iax, iay, m, mx, my, rot    =    b.x, b.y, b.width, b.height, b.image.anchor_x, b.image.anchor_y, b.scale, b.scale_x, b.scale_y, b.rotation
        fs = ff.format(sid, lid, p, l, s, c, t, n, i, k, z, x, y, w, h, v, ID, mx, my, kk[0], kk[1], kk[2], oo, why, gg, pg)
        self.log(fs, pfx=0)
        assert(type(b) == pyglet.sprite.Sprite)

    def dumpSprite(self, b=None, _=-1, tid=-1, p=-1, l=-1, s=-1, c=-1, t=-1, n=-1, i=-1, k=-1, o=-1, a=-1, d=-1, e=-1, f=-1, g=-1, r=-1, z=-1, why=''):
        if b is None: self.log(f' Tid P  L  S   C   T   N   I   K   z    x       y       w       h        v     identity   mx    my   red grn blu opc   why          group       parent', pfx=0); return
        ff = '{:4} {} {:2} {:2} {:3} {:3} {:3} {:3} {:3} {:3} {:7.2f} {:7.2f} {:7.2f} {:7.2f}     {:1} {:13} {:5.3f} {:5.3f} {:3} {:3} {:3} {:3} {:12} {} {}'
        kk, oo, v, gg, pg    =    b.color, b.opacity, b.visible, b.group, b.group.parent   ;   ID = hex(id(b))   ;   z += r   ;   i += o + a + d + e + f + g
        x, y, w, h, iax, iay, m, mx, my, rot    =    b.x, b.y, b.width, b.height, b.image.anchor_x, b.image.anchor_y, b.scale, b.scale_x, b.scale_y, b.rotation
        fs = ff.format(tid, p, l, s, c, t, n, i, k, z, x, y, w, h, v, ID, mx, my, kk[0], kk[1], kk[2], oo, why, gg, pg)
        self.log(fs, pfx=0)
        assert(type(b) == pyglet.sprite.Sprite)

    def dumpTNIK(  self, b=None, _=-1, tid=-1, p=-1, l=-1, s=-1, c=-1, t=-1, n=-1, i=-1, k=-1, o=-1, a=-1, d=-1, e=-1, f=-1, g=-1, r=-1, z=-1, why=''):
        if   type(b) == pyglet.sprite.Sprite: self.dumpSprite(b, _, tid=tid, p=p, l=l, s=s, c=c, t=t, n=n, i=i, k=k, o=o, a=a, d=d, e=e, f=f, g=g, r=r, z=z, why=why)
        elif type(b) == pyglet.text.Label:    self.dumpLabel( b, _, tid=tid, p=p, l=l, s=s, c=c, t=t, n=n, i=i, k=k, o=o, a=a, d=d, e=e, f=f, g=g, r=r, z=z, why=why)
#        msg0 = 'Tid P  L  S   C   T   N   I   K   z    x       y       w       h'
#        msg1 = '        v     identity   mx    my   red grn blu opc   why          group       parent'
#        msg2 = '    text      identity  siz dpi b i red grn blu opc   why'
#        if b is None: self.log(f'{msg0}{msg1}' if SPRITES else f'{msg0}{msg2}', pfx=0)   ;   return
#        f0 = '{:4} {} {:2} {:2} {:3} {:3} {:3} {:3} {:3} {:3} {:7.2f} {:7.2f} {:7.2f} {:7.2f}'
#        f1 = '     {:1} {:13} {:5.3f} {:5.3f} {:3} {:3} {:3} {:3} {:12} {} {}'
#        f2 = ' {:6} {:13} {:2} {:3} {:1} {:1} {:3} {:3} {:3} {:3} {}'


    def dumpLabel( self, b=None, _=-1, tid=-1, p=-1, l=-1, s=-1, c=-1, t=-1, n=-1, i=-1, k=-1, o=-1, a=-1, d=-1, e=-1, f=-1, g=-1, r=-1, z=-1, why=''):
        if b is None: self.log(f' Tid P  L  S   C   T   N   I   K   z    x       y       w       h    text      identity  siz dpi b i red grn blu opc   why', pfx=0) ; return
        x, y, w, h, fn, dd, zz, kk, bb, ii, tx    =    b.x, b.y, b.width, b.height, b.font_name, b.dpi, b.font_size, b.color, b.bold, b.italic, b.text  ;  ID = hex(id(b))   ;   z += r   ;   i += o + a + d + e + f + g
        ff = '{:4} {} {:2} {:2} {:3} {:3} {:3} {:3} {:3} {:3} {:7.2f} {:7.2f} {:7.2f} {:7.2f} {:6} {:13} {:2} {:3} {:1} {:1} {:3} {:3} {:3} {:3} {} '
        fs = ff.format(tid, p, l, s, c, t, n, i, k, z, x, y, w, h, tx, ID, zz, dd, bb, ii, kk[0], kk[1], kk[2], kk[3], why)
        self.log(fs, pfx=0)

    def OLD_1_dumpLabel(self, b=None, sid=-1, lid=-1, p=-1, l=-1, s=-1, c=-1, t=-1, n=-1, i=-1, k=-1, o=-1, a=-1, d=-1, e=-1, f=-1, g=-1, r=-1, z=-1, why=''):
        if b is None: self.log(f' sid  lid p  l  s   c   t   n   i   k   z    x       y       w       h    text      identity  siz dpi b i red grn blu opc   why', pfx=0) ; return
        x, y, w, h, fn, dd, zz, kk, bb, ii, tx    =    b.x, b.y, b.width, b.height, b.font_name, b.dpi, b.font_size, b.color, b.bold, b.italic, b.text  ;  ID = hex(id(b))   ;   z += r   ;   i += o + a + d + e + f + g
        ff = '{:4} {:4} {} {:2} {:2} {:3} {:3} {:3} {:3} {:3} {:3} {:7.2f} {:7.2f} {:7.2f} {:7.2f} {:6} {:13} {:2} {:3} {:1} {:1} {:3} {:3} {:3} {:3} {} '
        fs = ff.format(sid, lid, p, l, s, c, t, n, i, k, z, x, y, w, h, tx, ID, zz, dd, bb, ii, kk[0], kk[1], kk[2], kk[3], why)
        self.log(fs, pfx=0)
    ####################################################################################################################################################################################################
    def createCursor(self, g, dbg=1):
        self.cursorCol()
        if dbg: self.log(f'cc={self.cc} len(tabs)={len(self.tabs)}')
        c = self.tabs[self.cc]
        w, h = c.width, c.height
        x, y = c.x - w/2, c.y - h/2
        if dbg:
            self.log(f'c={self.cc} x={x:6.1f} y={y:6.1f} w={w:6.1f} h={h:6.1f} i={fmtl(self.i, FMTN)}')
            self.dumpWH()
            self.dumpGeom('NEW', 'CURS')
            self.dumpTNIK()
        self.J2[-2] += 1
        self.cursor = self.createTNIK(None, -1, x, y, w, h, 8, g, why='new Cursor', kl=CCS, v=1, dbg=1)
        if QQ: self.setLLStyle(self.cc, CURRENT_STYLE)

    def setLLStyle(self, cc, style, dbg=0):
        p, l, c, t = self.cc2plct(cc)  ;  nc = self.n[C]
        bold, italic, color = 0, 0, self.klc[0]
        if   style == NORMAL_STYLE:  color = self.klc[0]  ;  bold = 0  ;  italic = 0
        elif style == CURRENT_STYLE: color = CCS[8]       ;  bold = 0  ;  italic = 0
        elif style == SELECT_STYLE:  color = CCS[0]       ;  bold = 1  ;  italic = 1
        elif style == COPY_STYLE:    color = REDS[1]      ;  bold = 1  ;  italic = 1
        if self.lcols:
            self.lcols[c + l * nc].color  = color
            self.lcols[c + l * nc].bold   = bold
            self.lcols[c + l * nc].italic = italic
        if dbg: self.log(f'{self.fPos()}     nc={nc} style={style} bold={bold} italic={italic} color={color}')

    def resizeCursor(self, dbg=1):
        cc = self.cursorCol()
        c = self.tabs[cc]
        w, h = c.width, c.height
        x, y = c.x - w/2, c.y - h/2
        if dbg:
            self.log(f'c={cc} x={x:6.1f} y={y:6.1f} w={w:6.1f} h={h:6.1f} i={fmtl(self.i, FMTN)}')
            self.dumpWH()
            self.dumpGeom('RSZ', 'CURS')
        if self.w[T] and self.h[T]: self.cursor.update(x=x, y=y, scale_x=w/self.w[T], scale_y=h/self.h[T])
        else: msg = f'ERROR zero width or height in denom x={x:6.2f} y={y:6.2f} wT={self.w[T]:6.2f} hT={self.h[T]:6.2f}'  ;  self.log(msg)  # ;  self.quit(msg)
    ####################################################################################################################################################################################################
    def setCaption(self, msg, dbg=1):
        if dbg: self.log(f'{msg}')
        self.set_caption(msg)

    def resizeFonts(self, dbg = 1):
        ms = self.minSize()  ;  slope, off = 0.6, 3
        fs = fri(ms * slope + off)  ;  formula = '(fs = ms*slope+off)'
        if dbg: self.log(f'{self.fmtWH()} {formula} ms={ms:4.1f} slope={slope} off={off} fs={fs:4.1f}={fri(fs):2}')
        self.setFontParam('font_size', fs, 'fontSize')

    def minSize(self, dbg=1):
        b = self.B
        if dbg: self.log(f'len(b)={len(b)} lenB={self.lenB()}')
        tabs = b[TT] if b[TT] and b[TT][0].width and b[TT][0].height else b[NN] if b[NN] and b[NN][0].width and b[NN][0].height else b[II] if b[II] and b[II][0].width and b[II][0].height else b[KK] if b[KK] and b[KK][0].width and b[KK][0].height else None
        w = tabs[0].width  if tabs else 20
        h = tabs[0].height if tabs else 20
        m = min(w, h)
        if dbg: self.log(f'w={w:5.1f} h={h:5.1f} m={m:5.1f}')
        return m

    def fontParams(self):    return self.fontBold, self.fontColorIndex, self.fontDpiIndex, self.fontItalic, self.fontNameIndex, self.fontSize
    def fmtf(self, dbg=0):
        fb, fc, fd, fi, fn, fs = self.fontParams()
        text = f'{FONT_DPIS[fd]}dpi {fs}pt {FONT_NAMES[fn]} {fc}:{FONT_COLORS[fc]}'
        if dbg: self.log(f'{text}')
        return text

    def dumpFont(self, why=''):
        b, k, dpi, i, n, s = self.fontParams()
        pix = FONT_SCALE * s / dpi
#        self.log(f'{why} ki={k} di={dpi}={FONT_DPIS[dpi]}DPI {s}pt ni={n} {FONT_NAMES[n]} {FONT_SCALE}*{m}')
        self.log(f'{dpi}:{FONT_DPIS[dpi]}dpi {s}pt {n}:{FONT_NAMES[n]} {k}:{FONT_COLORS[k]} ({FONT_SCALE:4.0f}*{s}pt/{dpi}dpi)={pix:4.0f}pixels {why}')

    def setFontParam(self, n, v, m, dbg=1):
        setattr(self, m, v)
        if dbg: self.log(f'n={n} v={v:.1f} m={m}')
        self._setFontParam(self.tniks, n, v, m)
        self.setCaption(self.fmtf())

    @staticmethod
    def _setFontParam(p, n, v, m):
        for j in range(len(p)):
            setattr(p[j], n, FONT_NAMES[v] if m == 'fontNameIndex' else FONT_COLORS[v] if m == 'fontColorIndex' else FONT_DPIS[v] if m == 'fontDpiIndex' else v)
    ####################################################################################################################################################################################################
    def cursorCol(self): self.cc = self.plct2cc(*self.j2())  ;  return self.cc
    def normalizeCC(self, cc): return (cc // self.tpc) * self.tpc

    def plct2cc(self, p, l, c, t, dbg=0):
        cc = p * self.tpp + l * self.tpl + c * self.tpc + t   ;   lenT = len(self.tabs)   ;   ccm = cc % lenT if lenT else -1
        if dbg: self.log(f'plct2cc({p} {l} {c} {t}) {self.tpp} {self.tpl} {self.tpc} ({p*self.tpp} +{l*self.tpl} +{c*self.tpc} +{t}) % {lenT} return {ccm}')
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
        self.log(f'cn={cn} cc={cc} plc={p} {l} {c} txt={txt}')
    ####################################################################################################################################################################################################
    def on_mouse_release(self, x, y, button, modifiers, dbg=1):
        np, nl, ns, nc, nt = self.n    ;  nc += CCC   ;   file = None
        y0 = y   ;   y = self.hh - y   ;   n = nl * ns * nt + ns * QQ   ;  m = int(ns*nt) + QQ
        w = self.ww/nc       ;  h = self.hh/n         ;   d = int(y/h) - QQ
        l = int(d/m)         ;  c  = int(x/w) - CCC   ;   t = d - (l * m)  ;  p = 0
        if dbg: self.log(f'BGN button={button} modifiers={modifiers} txt={self.tabs[self.cc].text}', file=file)
        if dbg: self.log(f'x={x} y0={y0:4} w={w:6.2f} h={h:6.2f}')
        if dbg: self.log(f'y={y:4} n={n} m={m} d={d}')
        if dbg: self.log(f'{self.fPos()}     before')
        self.moveTo(f'MOUSE RELEASE', p, l, c, t)
        if dbg: self.log(f'{self.fPos()}     after')
    ####################################################################################################################################################################################################
    def kbkEvntTxt(self): return f'{self.kbk:8} {self.symb:8} {self.symbStr:14} {self.mods:2} {self.modsStr:16}'
    ####################################################################################################################################################################################################
    def on_key_press(self, symb, mods, dbg=0): # avoid these
        self.symb, self.mods, self.symbStr, self.modsStr = symb, mods, pygwink.symbol_string(symb), pygwink.modifiers_string(mods)
        self.kbk = self.symbStr  ;  kbk = self.kbk
        if   dbg: self.log(f'BGN {self.kbkEvntTxt()}')
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
        elif kbk == 'I' and self.isCtrl(     mods):    self.toggleTabs(      '@   I', II)
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
        elif kbk == 'P' and self.isCtrlShift(mods):    self.cobj.dumpMlimap( '@ ^ P')
        elif kbk == 'P' and self.isCtrl(     mods):    self.cobj.dumpMlimap( '@   P')
        elif kbk == 'Q' and self.isCtrlShift(mods):    self.quit(            '@ ^ Q', code=1)
        elif kbk == 'Q' and self.isCtrl(     mods):    self.quit(            '@   Q', code=0)
        elif kbk == 'R' and self.isCtrlShift(mods):    self.toggleChordNames('@ ^ R', hit=1)
        elif kbk == 'R' and self.isCtrl(     mods):    self.toggleChordNames('@   R', hit=0)
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
    ####################################################################################################################################################################################################
        elif kbk == 'ESCAPE':                          self.toggleSelectAll( 'ESCAPE')
        elif kbk == 'TAB'       and self.isCtrl(mods): self.setCHVMode(      '@ TAB',       MELODY, LEFT)
        elif kbk == 'TAB':                             self.setCHVMode(      '  TAB',       MELODY, RIGHT)
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
    ####################################################################################################################################################################################################
        if not self.isParsing():
            if   kbk == 'ENTER' and self.isCtrl(mods): self.setCHVMode(      '@ ENTER',     CHORD,       v=DOWN)
            elif kbk == 'ENTER':                       self.setCHVMode(      '  ENTER',     CHORD,       v=UP)
            elif kbk == 'SPACE':                       self.autoMove(        'SPACE')
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
        if   self.shiftingTabs:                              self.shiftTabs(  'onTxt', text)
        elif self.jumping:                                   self.jump(       'onTxt', text, self.jumpAbs)
        elif self.inserting:                                 self.insertSpace('onTxt', text)
        elif self.swapping:                                  self.swapTab(    'onTxt', text)
        elif self.isTab(self.kbk):                           self.setTab(     'onTxt', self.kbk)
        elif self.kbk == '$' and self.isShift(self.mods):    self.snapshot()
        if dbg: self.log(f'END {self.kbkEvntTxt()} swapping={self.swapping}')
    ####################################################################################################################################################################################################
    def on_text_motion(self, motion, dbg=1): # use for motion not strings
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
        self.log(f'     {how}', pos=1)
    def move2FirstTab(self, how, page=0):
        if page: i = 0
        else: i = self.j()[L] * self.tpl - 1
        while not self.isFret(self.tabs[i].text): i += 1
        p, l, c, t = self.cc2plct(i)
        self.moveTo(how, p, l, c, t)
        self.log(f'     {how}', pos=1)
    ####################################################################################################################################################################################################
    def moveDown(self, how, dbg=1):
        p, l, s, c, t = self.j()  ;  nt = self.n[T] - 1
        if dbg: self.log(f'BGN {how}', pos=1)
        if t < nt: self.moveTo(how, p, l,   c, nt)      # move down to bottom of      line
        else:      self.moveTo(how, p, l+1, c, 0)       # move down to top    of next line, wrap up to first line
        if dbg: self.log(f'END {how}', pos=1)
    def moveUp(self, how, dbg=1):
        p, l, s, c, t = self.j()  ;  nt = self.n[T] - 1
        if dbg: self.log(f'BGN {how}', pos=1)
        if t:      self.moveTo(how, p, l,    c, 0)      # move up   to top    of      line,    wrap to bottom line
        else:      self.moveTo(how, p, l-1,  c, nt)     # move up   to bottom of prev line
        if dbg: self.log(f'END {how}', pos=1)
    def moveRight(self, how, dbg=1):
        p, l, s, c, t = self.j()  ;  nc = self.n[C] - 1
        if dbg: self.log(f'BGN {how}', pos=1)
        if c < nc: self.moveTo(how, p, l,  nc, t)       # move right to end of line
        else:      self.moveTo(how, p, l+1, 0, t)       # wrap left & down (up) to bgn of next (top) line
        if dbg: self.log(f'END {how}', pos=1)
    def moveLeft(self, how, dbg=1):
        p, l, s, c, t = self.j()  ;  nc = self.n[C] - 1
        if dbg: self.log(f'BGN {how}', pos=1)
        if c:      self.moveTo(how, p, l,   0,  t)      # move left  to bgn of line
        else:      self.moveTo(how, p, l-1, nc, t)      # wrap right & up (down) to end of prev (bottom) line
        if dbg: self.log(f'END {how}', pos=1)

    def moveCursor(self, ss=0):
        self.setLLStyle(self.cc, SELECT_STYLE if ss else NORMAL_STYLE)
        self.cursorCol()
        if self.tabs and len(self.tabs) > self.cc:
            tab = self.tabs[self.cc]
            x = tab.x - tab.width/2   ;   y = tab.y - tab.height/2
            if self.cursor: self.cursor.update(x=x, y=y)
            self.setLLStyle(self.cc, CURRENT_STYLE)
        else: msg = f'WARN Illegal cursor move request cc={self.cc}'   ;   self.setCaption(msg)   ;   self.log(msg, pos=1)

#        if not self.SNAP0: t = self.tabs[self.cc]  ;  self.snapshot(f'pre-move() k={k:4} kk={self.cc:3} {fmtl(self.i, FMTN)} text={t.text} {t.x:6.2f} {t.y:6.2f}')  ;  self.SNAP0 = 1
#        self.armSnap = f'move() k={k:4} kk={kk:4} {fmtl(self.i, FMTN)} text={self.tabs[self.cc].text} {x:6.2f} {y:6.2f}'
    def moveTo(self, how, p, l, c, t, ss=0, dbg=1):
        if dbg:    self.log(f'BGN {how}', pos=1)
        self._moveTo(p, l, c, t)
        self.moveCursor(ss)
        if dbg:    self.log(f'END {how}', pos=1)

    def move(self, how, k, ss=0, dbg=1):   #  text={self.tabs[self.cc].text} {x:6.2f} {y:6.2f}') # , file=sys.stdout)
        if dbg:    self.log(f'BGN k={k} {how}', pos=1)
        if k:
            p,  l,  c,  t = self.j2()
            self._moveTo(p, l, c, t, n=k)
            self.moveCursor(ss)
        if dbg:    self.log(f'END k={k} {how}', pos=1)

    def _moveTo(self, p, l, c, t, n=0, dbg=1):
        if dbg: self.log(f'BGN n={n}', pos=1)
        np, nl, ns, nc, nt = self.n
        t2        =       n  + t
        c2        = t2 // nt + c
        l2        = c2 // nc + l
        p2        = l2 // nl + p
        self.i[T] = t2  % nt + 1
        self.i[C] = c2  % nc + 1
        self.i[L] = l2  % nl + 1
        self.i[P] = p2  % np + 1
        if dbg: self.log(f'END n={n} plct2=[{p2} {l2} {c2} {t2}]', pos=1)

    def autoMove(self, how, dbg=1):
        self.log(f'BGN {how}', pos=1)
        ha = 1 if self.hArrow else -1
        va = 1 if self.vArrow else -1
        nt, it = self.n[T], self.i[T]
        mmDist = ha * nt
        cmDist = va
        amDist = mmDist + cmDist
        if dbg: self.dumpCursorArrows(f'{self.fPos()}     {how} M={mmDist} C={cmDist} A={amDist}')
        if      self.csrMode == MELODY:                                     self.move(how, mmDist)
        elif    self.csrMode == CHORD:
            if   it == 1 and self.vArrow  == UP   and self.hArrow == RIGHT: self.move(how,   nt*2-1)
            elif it == 6 and self.vArrow  == DOWN and self.hArrow == RIGHT: self.move(how, -(nt*2-1))
            else:                                                           self.move(how, cmDist)
        elif    self.csrMode == ARPG:                                       self.move(how, amDist)
        self.log(f'END {how}', pos=1)

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
    def dumpSmap(self, why, pos=0): self.log(f'{why} smap={fmtm(self.smap)}', pos=pos)

    def toggleSelectAll(self, how):
        self.dumpSmap(f'BGN {how} allSelected={self.allSelected}')
        if   self.allSelected: self.unselectAll(how)   ;   self.allSelected = 0
        else:                  self.selectAll(how)     ;   self.allSelected = 1
        self.dumpSmap(f'END {how} allSelected={self.allSelected}')
    ####################################################################################################################################################################################################
    def selectAll(self, how, dbg=0):
        mli = self.cobj.mlimap
        if dbg: self.dumpSmap(f'BGN {how}')
        for k in mli:
            if k not in self.smap: self.selectTabs(how, cn=k, dbg=1)
        if dbg: self.dumpSmap(f'END {how}')

    def selectTabs(self, how, m=0, cn=None, dbg=0, dbg2=0):
        if cn is None: cc = self.cc   ;   cn = self.cc2cn(cc)
        else:          cc = self.cn2cc(cn)
        nt = self.n[T]  ;  k = cn * nt   ;   text = ''
        if cn in self.smap: self.log(f'RETURN: cn={cn} already in smap={fmtm(self.smap)}') if dbg2 else None   ;   return
        if dbg: self.dumpSmap(f'BGN {how} m={m} cn={cn} cc={cc} k={k}')
        for t in range(nt):
            if self.tabs:   self.tabs  [k + t].color = CCS[0]
            if self.notes:  self.notes [k + t].color = CCS[0]
            if self.ikeys:  self.ikeys [k + t].color = CCS[0]
            if self.chords: self.chords[k + t].color = CCS[0]
            if self.tabs:   text += self.tabs  [k + t].text
        self.smap[cn] = text
        if m: self.move(how, m, ss=1)
        if dbg: self.dumpSmap(f'END {how} m={m} cn={cn} cc={cc} k={k}')
    ####################################################################################################################################################################################################
    def unselectAll(self, how, dbg=0):
        for i in range(len(self.smap)-1, -1, -1):
            cn = list(self.smap.keys())[i]
            if dbg: self.dumpSmap(f'{how} i={i} cn={cn}')
            self.unselectTabs(how, m=0, cn=cn)

    def unselectTabs(self, how, m, cn=None, dbg=0):
        if cn is None: cc = self.cc   ;   cn = self.cc2cn(cc)
        else:          cc = self.cn2cc(cn)
        nt = self.n[T]   ;   k = cn * nt
        self.setLLStyle(cc, NORMAL_STYLE)
        if dbg: self.dumpSmap(f'BGN {how} m={m} cn={cn} cc={cc} k={k}')
        for t in range(nt):
            if self.tabs:   self.tabs  [k + t].color = self.kt[0]
            if self.notes:  self.notes [k + t].color = self.kn[0]
            if self.ikeys:  self.ikeys [k + t].color = self.ki[0]
            if self.chords: self.chords[k + t].color = self.kk[0]
        if cn in self.smap: self.smap.pop(cn)
        elif dbg:           self.log(f'cn={cn} not found in smap={fmtm(self.smap)}')
        if m:   self.move(how, m)
        if dbg: self.dumpSmap(f'END {how} m={m} cn={cn} cc={cc} k={k}')
    ####################################################################################################################################################################################################
    def copyTabs(self, how, dbg=1):
        self.dumpSmap(f'BGN {how}')   ;   nt = self.n[T]  ;   text = ''
        for k in list(self.smap.keys()):
            k *= nt
            self.setLLStyle(k, NORMAL_STYLE)
            for t in range(nt):
                if self.tabs:   self.tabs  [k + t].color = self.k[T][0]
                if self.notes:  self.notes [k + t].color = self.k[N][0]
                if self.ikeys:  self.ikeys [k + t].color = self.k[I][0]
                if self.chords: self.chords[k + t].color = self.k[K][0]
                if dbg: text += self.tabs  [k + t].text
            if dbg: text += ' '
        if dbg: self.log(f'text={text}')
        self.dumpSmap(f'END {how}')
    ####################################################################################################################################################################################################
    def cutTabs(self, how): self.log('BGN Cut = Copy + Delete')  ;  self.copyTabs(how)  ;  self.log('Cut = Copy + Delete')  ;  self.deleteTabs(how, keep=1)  ;  self.log('END Cut = Copy + Delete')
    ####################################################################################################################################################################################################
    def deleteTabs(self, how, keep=0, dbg=1):
        self.dumpSmap(f'BGN {how} keep={keep}')   ;   nt = self.n[T]
        for k, v in self.smap.items():
            cn = k   ;   k *= nt
            if dbg: self.log(f'k={k} cn={cn} v={v}')
            self.setLLStyle(k, NORMAL_STYLE)
            for t in range(nt):
                p, l, c, r  =  self.cc2plct(k + t)
                if self.tabs:   self.tabs  [k + t].color = self.k[T][0]
                if self.notes:  self.notes [k + t].color = self.k[N][0]
                if self.ikeys:  self.ikeys [k + t].color = self.k[I][0]
                if self.chords: self.chords[k + t].color = self.k[K][0]
                self.setDTNIK( self.tblank, k + t, p, l, c, t, kk=1 if t == nt - 1 else 0)  # call with uk=1 only once per column or tpc
        if not keep: self.unselectAll(f'deleteTabs(keep={keep})')
        self.dumpSmap(f'END {how} keep={keep}')
        self.dataHasChanged = 1

    def pasteTabs(self, how, kk=0, dbg=1):
        cc = self.cursorCol()        ;  nt = self.n[T]
        ntc = self.normalizeCC(cc)   ;  kt = 0
        p, l, s, c, r = self.j()
        self.dumpSmap(f'BGN {how} kk={kk} cc={cc} ntc={ntc} cn={self.cc2cn(cc)} plcr {p} {l} {c} {r}')
        for i, (k, v) in enumerate(self.smap.items()):
            text = v
            if not i: dk = 0
            elif kk:  dk = i * nt
            else:     dk = (list(self.smap.keys())[i] - list(self.smap.keys())[0]) * nt
            if dbg: self.log(f'i={i} k={k} v={v} text={text} kk={kk} dk={dk}')
            for t in range(nt):
                kt = (ntc + dk + t) % self.tpp
                p, l, c, r = self.cc2plct(kt)
                self.setDTNIK(text[t], kt, p, l, c, t, kk=1 if t == nt - 1 else 0)  # call with uk=1 only once per column or tpc
            if dbg: self.log(f'smap[{k}]={text} kt={kt} kk={kk} dk={dk}')
#        if not hc: self.unselectAll('pasteTabs()')
#        elif dbg:  self.log(f'holding a copy of smap')
#        self.dumpSmap(f'END {how} hc={hc} kk={kk} cc={cc} ntc={ntc} cn={self.cc2cn(cc) + 1}')
        self.dumpSmap(f'END {how} kk={kk} cc={cc} ntc={ntc} cn={self.cc2cn(cc)} plcr {p} {l} {c} {r}')
        self.dataHasChanged = 1

    def swapTabs(self, how):
        nk = len(self.smap)   ;   nk2 = nk // 2
        self.dumpSmap(f'BGN nk={nk} nk2={nk2}')
        for i in range(nk2):
            k1 = list(self.smap.keys())[i]
            k2 = list(self.smap.keys())[nk - 1 - i]
            text1 = self.smap[k1]
            text2 = self.smap[k2]
            self.smap[k1] = text2
            self.smap[k2] = text1
        self.dumpSmap(f'    nk={nk} nk2={nk2}')
        self.pasteTabs(how)
        self.dumpSmap(f'END nk={nk} nk2={nk2}')

    def insertSpace(self, how, txt='0', dbg=1):
        cc = self.cursorCol()   ;   c0 = self.cc2cn(cc)
        if not self.inserting: self.inserting = 1   ;    self.setCaption('Enter nc: number of cols to indert int')
        elif txt.isdecimal():  self.insertStr += txt
        elif txt == ' ' or txt == '/r':
            self.inserting = 0
            width = int(self.insertStr)
            tcs = sorted(self.cobj.mlimap)
            tcs.append(self.n[C] * self.n[L] - 1)
            tcs = [ t + 1 for t in tcs ]
            if dbg: self.log(f'BGN {how} Searching for space to insert {width} cols starting at col {c0}')
            self.log(f'{fmtl(tcs, ll=1)} insertSpace', pfx=0)
            found, c1, c2 = 0, 0, None   ;   self.insertStr = ''
            for c2 in tcs:
                if dbg: self.log(f'w c0 c1 c2 = {width} {c0} {c1} {c2}')
                if c2 > c0 + width and c2 > c1 + width: found = 1  ;  break
                c1 = c2
            if not found: self.log(f'{how} starting at col {c0} No room to insert {width} cols before end of page at col {tcs[-1]+1}')  ;   return
            self.log(f'{how} starting at col {c0} Found a gap {width} cols wide between cols {c1} and {c2}')
            self.log(f'select cols {c0} ... {c1}, cut cols, move ({width} - {c1} + {c0})={width-c1+c0} cols, paste cols')
            [ self.selectTabs(how, m=self.tpc) for _ in range(c1 - c0) ]
            self.cutTabs(how)
            self.move(how, (width - c1 + c0) * self.tpc)
            self.pasteTabs(how)
            self.unselectAll(how)

    def shiftTabs(self, how, nf=0):
        self.dumpSmap(f'BGN {how} shiftingTabs={self.shiftingTabs} nf={nf}')
        if not self.shiftingTabs:
            self.shiftingTabs = 1
            for k, v in self.smap.items():
                self.setLLStyle(k, NORMAL_STYLE)
            self.setCaption('Enter nf: number of frets to shift +/- int')
        elif nf == '-': self.shiftSign = -1
        elif self.isFret(nf):
            self.shiftingTabs = 0   ;   nt = self.n[T]
            for cn, v in self.smap.items():
                cc = self.cn2cc(cn)   ;   p, l, c, r = self.cc2plct(cc, dbg=0)
                self.log(f'cc={cc} cn={cn} v={v} text={self.smap[cn]}')
                for t in range(nt):
                    text = self.smap[cn][t]    ;    kt = cc + t    ;    fn = 0   ;   ntones = misc.NTONES * 2
                    if self.isFret(text):
                        fn = self.afn(str((self.tab2fn(text) + self.shiftSign * self.tab2fn(nf)) % ntones))  ;  self.log(f'cc={cc} cn={cn} t={t} text={text} nf={nf} fn={fn} ss={self.shiftSign}')
                    if fn and self.isFret(fn):  self.setDTNIK(fn, kt, p, l, c, t) # uk=0 for each nt tabs
                imap = self.getImap(p, l, c, tt=NN)
                self.setChord(imap, p, l, c, 0) # do what uk=1 does, once
            self.shiftSign = 1
            self.dataHasChanged = 1
            self.unselectAll('shiftTabs()')
        self.dumpSmap(f'END {how} shiftingTabs={self.shiftingTabs} nf={nf} ss={self.shiftSign}')

    def swapTab(self, how, txt='', data=None, dbg=0, dbg2=0):  # e.g. c => 12 not same # chars asserts
        src, trg = self.swapSrc, self.swapTrg
        if data is None: data = self.data
        if not self.swapping: self.swapping = 1
        elif txt.isalnum():
            if   self.swapping == 1:   self.swapSrc += txt  # ;   self.log(f'    {how} txt={txt} swapping={self.swapping} swapSrc={self.swapSrc} swapTrg={self.swapTrg}')
            elif self.swapping == 2:   self.swapTrg += txt  # ;   self.log(f'    {how} txt={txt} swapping={self.swapping} swapSrc={self.swapSrc} swapTrg={self.swapTrg}')
        elif txt == '\r':
            self.log(f'    {how} swapping={self.swapping} swapSrc={self.swapSrc} swapTrg={self.swapTrg}')
            if   self.swapping == 1 and not self.swapTrg: self.swapping = 2   ;   self.log(f'{how} waiting swapSrc={self.swapSrc} swapTrg={self.swapTrg}') if dbg else None   ;   return
            elif self.swapping == 2 and     self.swapTrg: self.swapping = 0   ;   self.log(f'{how} BGN     swapSrc={self.swapSrc} swapTrg={self.swapTrg}') if dbg else None
            np, nl, ns, nc, nr = self.n  ;  nc += CCC
            for p in range(np):
                for l in range(nl):
                    for c in range(nc):
                        while src in data[p][l][c]:
                            d = data[p][l][c]
                            t = d.find(src)
                            self.cc = self.plct2cc(p, l, c, t)
                            if dbg2: self.log(f'cc={self.cc} before data[{p}][{l}][{c}]={d}')
                            d = d[:t] + trg + d[t+1:]
                            self.setDTNIK(trg, self.cc, p, l, c, t, kk=1)
                            if dbg2: self.log(f'cc={self.cc} after  data[{p}][{l}][{c}]={d}')
            self.log(f'{how} END     swapSrc={self.swapSrc} swapTrg={self.swapTrg}') if dbg else None
            if dbg2: self.dumpLabels('SWAP')
            self.dataHasChanged = 1
    ####################################################################################################################################################################################################
    def setTab(self, how, text, rev=0, dbg=1):
        if rev: self.reverseArrow()    ;    self.autoMove(how)
        p, l, c, t = self.j2()   ;   data = self.data[p][l][c][t]   ;   isDataFret = self.isFret(data)   ;   isTextFret = self.isFret(text)   ;   cc = self.plct2cc(p, l, c, t)
        self.log(f'BGN {how} text={text} data={data} rev={rev}', pos=1)
        self.setDTNIK(text, cc, p, l, c, t, kk=1 if isDataFret or isTextFret else 0)
        p, l, c, t = self.j2()   ;   data = self.data[p][l][c][t]
        self.log(f'END {how} text={text} data={data} rev={rev}', pos=1)
        if rev: self.reverseArrow()
        else:   self.autoMove(how)
        if SNAP and dbg: self.snapshot()
        self.dataHasChanged = 1

    def setDTNIK(self, text, cc, p, l, c, t, kk=0, pos=0, dbg=0):
        if dbg: self.log(f'BGN kk={kk}    text={text}', pos=pos)
        self.setData(text, p, l, c, t)
        imap1 = self.getImap(p, l, c, tt=II if kk and self.TNIK[II] else TT)
        imap2 = self.getImap(p, l, c, tt=KK if kk and self.TNIK[KK] else TT)
        if self.TNIK[TT]:        self.setTab2( text, cc)
        if self.TNIK[NN]:        self.setNote( text, cc, t)
        if self.TNIK[II] and kk: self.setIkey( imap1, p, l, c)
        if self.TNIK[KK] and kk: self.setChord(imap2, p, l, c)
        if dbg: self.log(f'END kk={kk}    text={text}', pos=pos)
    ####################################################################################################################################################################################################
    def setData(self, text, p, l, c, t, pos=0, dbg=0):
        data = self.data[p][l][c]
        if dbg: self.log(f'BGN t={t} text={text} data={data}', pos=pos)
        self.data[p][l][c] = data[0:t] + text + data[t+1:]
        data = self.data[p][l][c]
        if dbg: self.log(f'END t={t} text={text} data={data}', pos=pos)

    def setTab2(self, text, cc, pos=0, dbg=0):
#        cc = self.plct2cc(*self.j2())
        if dbg: self.log(f'BGN         text={text} tabs[{cc}]={self.tabs[cc].text}', pos=pos)
        self.tabs[cc].text = text
        if dbg: self.log(f'END         text={text} tabs[{cc}]={self.tabs[cc].text}', pos=pos)

    def setNote(self, text, cc, t, pos=0, dbg=0):
#        p, l, c, t = self.j2()   ;   cc = self.plct2cc(p, l, c, t)
        if dbg: self.log(f'BGN     t={t} text={text} notes[{cc}]={self.notes[cc].text}', pos=pos)
        self.notes[cc].text = self.tab2nn(text, t) if self.isFret(text) else self.tblank
        if dbg: self.log(f'END     t={t} text={text} notes[{cc}]={self.notes[cc].text}', pos=pos)

    def getImap(self, p, l, c, tt, dbg=0):
        if tt != II and tt != KK: return []
        cn = self.plc2cn(p, l, c)   ;   key = cn if tt == KK else -cn   ;   why = ' Chord' if tt == KK else ' Ival '   ;   mli = self.cobj.mlimap
        imap = self.cobj.getChordName(p, l, c, kk=1 if tt==KK else 0, why=why)
        if dbg: self.log(f'{why} tt={tt} cn={cn} key={key} keys={fmtl(list(mli.keys()))}')
        if dbg and imap: self.cobj.dumpImap(imap)
        return imap

    def setIkey(self, imap, p, l, c, pos=0, dbg=0):
        ikeys = imap[0]
#        p, l, c, t = self.j2()
        cc = self.plct2cc(p, l, c, 0)  # ;   cn = self.cc2cn(cc)
        if dbg: self.log(f'BGN ikeys={fmtl(ikeys)}', pos=pos)
        self.setIkeyText(ikeys, cc, p, l, c)
        if dbg: self.log(f'END ikeys={fmtl(ikeys)}', pos=pos)

    def setIkeyText(self, text, cc, p, l, c, pos=0, dbg=0):
        nt = self.n[T]   ;  cc = self.normalizeCC(cc)   ;   data = self.data[p][l][c]   ;   j = 0   ;   text = text[::-1]
        txt = self.objs2Text(self.ikeys, cc, nt, I)
        if dbg: self.log(f'BGN [{cc:2}-{cc+nt-1:2}] text={fmtl(text)} data={data} ikeys=<{txt}>{len(txt)}', pos=pos)
        for i in range(nt):
            if text and len(text) > j: self.ikeys[cc + i].text = text[j] if self.isFret(data[i]) else self.tblank     ;   j += 1 if self.isFret(data[i]) else 0
            else:                      self.ikeys[cc + i].text = self.tblank
        txt = self.objs2Text(self.ikeys, cc, nt, I)
        if dbg: self.log(f'END [{cc:2}-{cc+nt-1:2}] text={fmtl(text)} data={data} ikeys=<{txt}>{len(txt)}', pos=pos)
        if dbg: self.dumpDataSlice(p, l, c, cc)

    def setChord(self, imap, p, l, c, pos=0, dbg=0):
#        p, l, c, t = self.j2()
        cc = self.plct2cc(p, l, c, 0)  # ;   cn = self.cc2cn(cc)
        name = imap[3] if imap and len(imap) > 3 else ''  ;   chunks = imap[4] if imap and len(imap) > 4 else []
        if dbg: self.log(f'BGN name={name} chunks={fmtl(chunks)}', pos=pos)
        self.setChordName(cc, name, chunks)
        if dbg: self.log(f'END name={name} chunks={fmtl(chunks)}', pos=pos)

    def setChordName(self, cc, name, chunks, pos=0, dbg=0):
        nt = self.n[T]   ;   cc = self.normalizeCC(cc)   ;   chords = self.chords
        txt = self.objs2Text(chords, cc, nt, K)
        if dbg: self.log(f'BGN [{cc:2}-{cc+nt-1:2}] name={name} chunks={fmtl(chunks)} chords=<{txt}>{len(txt)}', pos=pos)
        for i in range(nt):
            if chunks and len(chunks) > i: self.chords[cc + i].text = chunks[i]
            else:                          self.chords[cc + i].text = self.tblank
        txt = self.objs2Text(chords, cc, nt, K)
        if dbg: self.log(f'END [{cc:2}-{cc+nt-1:2}] name={name} chunks={fmtl(chunks)} chords=<{txt}>{len(txt)}', pos=pos)
    @staticmethod
    def objs2Text(obs, cc, nt, j, dbg=0):
        texts = [ obs[cc + t].text for t in range(nt) ]   ;   text = ''.join(texts)
        if dbg: Tabs.slog(f'{jTEXTS[j]}[{cc}-{cc+nt-1}].text={fmtl(texts)}=<{text}>')
        return text
    ####################################################################################################################################################################################################
    @staticmethod
    def tab2fn(tab, dbg=0): fn = int(tab) if '0' <= tab <= '9' else int(ord(tab) - 87) if 'a' <= tab <= 'o' else None   ;   Tabs.slog(f'tab={tab} fretNum={fn}') if dbg else None   ;   return fn
    def tab2nn(self, tab, s, dbg=0):
        fn   = self.tab2fn(tab)
        i    = self.fn2ni(fn, s)
        name = misc.Note.getName(i)
        if dbg: self.log(f'tab={tab} s={s} fn={fn} i={i} name={name}')
        return name
    def fn2ni(self, fn, s, dbg=0):
        strNum = self.n[T] - s - 1    # Reverse and zero base the string numbering: str[1 ... numStrings] => s[(numStrings - 1) ... 0]
        k = self.stringKeys[strNum]
        i = self.stringMap[k] + fn
        if dbg: self.log(f'fn={fn} s={s} strNum={strNum} k={k} i={i} stringMap={fmtm(self.stringMap)}')
        return i
    ####################################################################################################################################################################################################
    def toggleFlatSharp(self, how, dbg=1):  #  page line col tab or select
        tt1 =  misc.Note.TYPE    ;    tt2 = (misc.Note.TYPE + 1) % 2    ;    misc.Note.setType(tt2)    ;   i1 = -1
        self.log(f'BGN {how} type={tt1}={misc.Note.TYPES[tt1]} => type={tt2}={misc.Note.TYPES[tt2]}')
        for i, n in enumerate(self.notes):
            if len(n.text) > 1:
                p, l, c, t = self.cc2plct(i)   ;   old = n.text    ;    i2 = self.plc2cn(p, l, c)
                if   n.text in misc.Note.F2S: n.text = misc.Note.F2S[n.text]
                elif n.text in misc.Note.S2F: n.text = misc.Note.S2F[n.text]
                if dbg: self.log(f'notes[{i:3}] {old} => {n.text} i1={i1} i2={i2}', pos=1)
                if i1 != i2:   imap = self.getImap(p, l, c, tt=II)   ;   self.setChord(imap, p, l, c, t)    ;    i1 = i2
        self.log(f'END {how} type={tt1}={misc.Note.TYPES[tt1]} => type={tt2}={misc.Note.TYPES[tt2]}')

    def keySignature(self): pass
    def scales(self):       pass
    ####################################################################################################################################################################################################
    def toggleChordNames(self, how, hit=0, dbg=1):
        cc = self.cc    ;    cn = self.cc2cn(cc)
        mks = list(self.cobj.mlimap.keys())   ;   sks = list(self.smap.keys())
        if sks and not hit:
            if dbg: self.dumpSmap(f'BGN {how} mks={fmtl(mks)} cn={cn:2} hit={hit} sks={fmtl(sks)}')
            [ self.toggleChordName(how, k) for k in sks ]
        else:
            if dbg: self.dumpSmap(f'BGN {how} mks={fmtl(mks)} cn={cn:2} hit={hit} sks={fmtl(sks)}')
            if hit: self.toggleChordNameHits(how, cn)
            else:   self.toggleChordName(    how, cn)
        if dbg:     self.dumpSmap(f'END {how} mks={fmtl(mks)} cn={cn:2} hit={hit} sks={fmtl(sks)}')

    def toggleChordNameHits(self, how, cn, dbg=1):
        mli = self.cobj.mlimap   ;   mks = list(mli.keys())
        if cn not in mli: self.log(f'RETURN: no mli key for cn={cn}') if dbg else None   ;   return
        ivals =  [ u[1] for u in mli[cn][0] ]
        msg   =  [ fmtl(v, z="x") for v in ivals ]
        if dbg: self.log(f'BGN {how} mks={fmtl(mks)} cn={cn:2} ivals={fmtl(msg, d1="", d2="")}')
        hits = self.ivalhits(ivals, how)
        for cn in hits:
            if cn not in self.smap: self.selectTabs(how, m=0, cn=cn)
            self.toggleChordName(how, cn)
        if dbg: self.log(f'END {how} mks={fmtl(mks)} cn={cn:2} ivals={fmtl(msg, d1="", d2="")}')

    def ivalhits(self, ivals, how, dbg=1):
        mli = self.cobj.mlimap   ;   mks = list(mli.keys())   ;   hits = set()
        for cn, lim in mli.items():
            for im in lim[0]:
                if cn in hits: break
                for iv in ivals:
                    iv1 = self.cobj.fsort(iv)   ;   iv2 = self.cobj.fsort(im[1])
                    if iv1 == iv2:     hits.add(cn)  ;   break
        if dbg: self.log(f'    {how} mks={fmtl(mks)} hits={fmtl(hits)}')
        return list(hits)

    def toggleChordName(self, how, cn, dbg=1, dbg2=1):
        cc = self.cn2cc(cn)   ;   mli = self.cobj.mlimap
        if cn not in mli: self.log(f'RETURN: cn={cn} Not Found milap.keys={fmtl(list(mli.keys()))}')   ;   return
        limap = mli[cn][0]   ;   imi = mli[cn][1]
        imi = (imi + 1) % len(limap)
        mli[cn][1] = imi
        ikeys, ivals, notes, chordName, chunks, rank = limap[imi]
        if ikeys:                p, l, c, t = self.cc2plct(cc)   ;   self.setIkeyText(ikeys, cc, p, l, c)
        if chordName and chunks: self.setChordName(cc, chordName, chunks)
        elif dbg: self.log(f'    {how} cn={cn} cc={cc} is NOT a chord')
        if dbg2:  self.cobj.dumpImap(limap[imi], why=f'{cn:2}')
        assert imi == limap[imi][-1]
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
        self.log(f'BGN {how} prevBlank={prevBlank}')
        self.tblanki = (self.tblanki + 1) % len(self.tblanks)
        self.tblank  =  self.tblanks[self.tblanki]
        self.swapSrc, self.swapTrg, self.swapping = prevBlank, self.tblank, 2
        self.swapTab(how, '\r')
        self.log(f'END {how} tblank={self.tblank}')
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
        for i in range(len(self.notes)):
            self.notes [i].text = self.tblank
        for i in range(len(self.ikeys)):
            self.ikeys [i].text = self.tblank
        for i in range(len(self.chords)):
            self.chords[i].text = self.tblank
        for p in range(np):
            for l in range(nl):
                for c in range(nc):
                    self.data[p][l][c] = self.tblankCol
        self.log(f'END {how} np={np} nl={nl} ns={ns} nc={nc} nt={nt}')
        self.dataHasChanged = 1

    def reset(self, how):
        self.dumpGeom('BGN', f'{how} before cleanup()')
        self.cleanup()
        self.dumpGeom('   ', f'{how} after cleanup() / before reinit()')
        self._reinit()
        self.dumpGeom('END', f'{how} after reinit()')

    def cleanup(self):
        if QQ: self.deleteList(self.lrows)   ;   self.deleteList(self.lcols)
        self.deleteList(self.sprites)
        self.deleteList(self.labels)
        self.deleteList(self.tniks)
    '''
    def setStringNumbs(self):
        np, nl, ns, nr, nc = self.n  ;  nc += CCC  ;  i = C1
        for p in range(np):
            for l in range(nl):
                self.data[p][l][C1] = self.stringNumbs
                self.log(f'p={p} l={l} c={c} data[p][l][c]={self.data[p][l][C1]}')
                for r in range(nr):
                    self.tabs[i].text  = self.stringNumbs[r]
                    self.log(f'({r} {i} {self.tabs[i].text}) ', pfx=0, end='')
                    i += nc
                self.log(pfx=0)

    def setStringNames(self):
        np, nl, ns, nr, nc = self.n  ;  nc += CCC  ;  i = C1
        for p in range(np):
            for l in range(nl):
                self.data[p][l][C1] = self.stringNames
                self.log(f'p={p} l={l} c={C1} data[p][l]={self.data[p][l][C1]}')
                for r in range(nr):
                    self.notes[i].text = self.stringNames[r]
                    self.log(f'({r} {i} {self.notes[i].text}) ', pfx=0, end='')
                    i += nc
                self.log(pfx=0)

    def setCapo(self):
        np, nl, ns, nr, nc = self.n  ;  nc += CCC  ;  i = C2
        for p in range(np):
            for l in range(nl):
                self.data[p][l][C2] = self.stringCapo
                self.log(f'p={p} l={l} c={C2} data[p][l]={self.data[p][l][C2]}')
                for r in range(nr):
                    self.tabs[i].text  = self.stringCapo[r]
                    self.notes[i].text = self.stringCapo[r]
                    self.log(f'({r} {i} {self.tabs[i].text} {self.notes[i].text}) ', pfx=0, end='')
                    i += nc
                self.log(pfx=0)
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
    def isBTab(self, text):   return 1 if text in self.tblanks else 0
    @staticmethod
    def isNBTab(text):        return 1 if                        Tabs.isFret(text) or text in misc.DSymb.SYMBS else 0
    def isTab(self, text):    return 1 if text == self.tblank or Tabs.isFret(text) or text in misc.DSymb.SYMBS else 0
    def isParsing(self):      return 1 if self.inserting or self.jumping or self.shiftingTabs or self.swapping else 0
    @staticmethod
    def afn(fn): return fn if len(fn) == 1 and '0' <= fn <= '9' else chr(ord(fn[1]) - ord('0') + ord('a')) if len(fn) == 2 and fn[0] == '1' else None
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

    @staticmethod
    def deleteGlob(g, why=''):
        Tabs.slog(f'deleting {len(g)} file globs why={why}')
        for f in g:
            Tabs.slog(f'{f}')
            os.system(f'del {f}')

    @staticmethod
    def getFilePath(seq=0, filedir='files', filesfx='.txt'):
        if seq:
            subDir     = '/' + SFX.lstrip('.')
            filedir    = filedir + subDir
            Tabs.slog(f'SFX          = {SFX}')
            Tabs.slog(f'subdir       = {subDir}')
            Tabs.slog(f'filedir      = {filedir}')
            Tabs.slog(f'filesfx      = {filesfx}')
            pathlib.Path(filedir).mkdir(parents=True, exist_ok=True)
            fileGlobArg = str(BASE_PATH / filedir / BASE_NAME) + SFX + '.*' + filesfx
            fileGlob    = glob.glob(fileGlobArg)
            Tabs.slog(f'fileGlobArg  = {fileGlobArg}')
            Tabs.slog('fileGlob:')
            seq        = 1 + Tabs.getFileSeqNum(fileGlob, filesfx)
            filesfx    = f'.{seq}{filesfx}'
            Tabs.slog(f'{fmtl(fileGlob)}', pfx=0)
            Tabs.slog(f'seq num      = {seq} filesfx={filesfx}')
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
            if dbg: Tabs.slog(f'ids={ids}')
            i = max(ids)
        return i
    ####################################################################################################################################################################################################
    def log(self, msg='', pfx=1, pos=0, file=None, flush=False, sep=',', end='\n'):
        if pos: msg = f'{self.fPos()}' + f' {msg}' # if msg else
        self.slog(msg, pfx, file, flush, sep, end)

    @staticmethod
    def slog(msg='', pfx=1, file=None, flush=False, sep=',', end='\n'):
        if file is None: file = LOG_FILE
        if pfx:
            ss = inspect.stack(0)   ;   i = 1
            while ss[i].function in Tabs.hideST:
                i += 1
            si = ss[i]   ;   sd = Tabs.stackDepth(ss)
            p = pathlib.Path(si.filename)  ;  n = p.name  ;  l = si.lineno  ;  f = si.function
            if IND: print(f'{Tabs.fmtSD(sd):20} {l:5} {n:7} {f:>20} ', file=file, end='')
            else:   print(             f'{sd:2} {l:5} {n:7} {f:>20} ', file=file, end='')
        print(f'{msg}', file=file, flush=flush, sep=sep, end=end)
#        print(f'{msg}', file=file, flush=flush, sep=sep, end=end) if pfx else print(f'{msg}', file=file, flush=flush, sep=sep, end=end)
#        if file != LOG_FILE: Tabs.slog(msg, pfx, flush=False, sep=',', end=end)
    ####################################################################################################################################################################################################
    @staticmethod
    def stackDepth(si):
        global MAX_STACK_DEPTH, MAX_STACK_FRAME
        for i, e in enumerate(si):
            j = len(si) - (i + 1)
            if j > MAX_STACK_DEPTH: MAX_STACK_DEPTH = j;  MAX_STACK_FRAME = si
        return len(si)
    @staticmethod
    def fmtSD(sd): return f'{sd:{sd}}'
    def dumpStack(self, si):
        for i, e in enumerate(si):
            fp = pathlib.Path(e.filename)  ;   n = fp.stem  ;  l = e.lineno  ;  f = e.function  ;  c = e.code_context[0].strip()  ;  j = len(si) - (i + 1)
            self.log(f'{j:2} {n:9} {l:5} {f:20} {c}')
        self.log(f'MAX_STACK_DEPTH={MAX_STACK_DEPTH:2}')
    ####################################################################################################################################################################################################
    def quit(self, why='', code=1, dbg=0):
        self.log(QUIT, pfx=0)
        self.log(f'BGN {why} code={code}')
#        self.dumpDataVert()
#        self.dumpDataHorz()
        self.dumpGeom('    ')
        self.dumpJ('quit')
        if       code and AUTO_SAVE: self.saveDataFile(why, f=0)
        elif not code:               self.saveDataFile(why, f=1)
        self.cobj.dumpMlimap(why)
#        self.cobj.dumpInstanceCat(why)
#        self.cleanupCat(1 if code != 2 else 0)
        if dbg: self.dumpStruct('quit ' + why)
        if SNAP and code != 2: self.snapshot()
        if dbg:
            self.dumpStack(inspect.stack())
            self.log(QUIT, pfx=0)
            self.dumpStack(MAX_STACK_FRAME)
        self.dumpGlobalFlags()
        self.log(f'END {why} code={code}')
        self.log(QUIT, pfx=0)
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
        self.log(f'SEQ_FNAMES={SEQ_FNAMES}')
        logPath = None
        if SEQ_FNAMES:
            logPath = self.getFilePath(seq=SEQ_FNAMES, filedir='logs', filesfx='.log')
            self.log(f'logPath      = {logPath}')
            self.log(f' ### copy {LOG_PATH} {logPath} ###')
        self.log(f'closing {LOG_FILE.name}')
        LOG_FILE.close()
        if SEQ_FNAMES and logPath: os.system(f'copy {LOG_PATH} {logPath}')
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

    def testslice(self):
        a = ['A', 'B', 'C', 'D', 'E']
        self.log(f'a = {fmtl(a, w=2, u=">"):21}')
        b = [ i for i in range(len(a)) ]
        self.log(f'b = {fmtl(b, w=2, u=">"):21}', end=' ')
        self.log(': i for i in range(len(a))', pfx=0)
        c = [ i for i in range(-len(a), 0)]
        self.log(f'c = {fmtl(c, w=2, u=">"):21}', end=' ')
        self.log(': i for i in range(-len(a), 0)', pfx=0)
        self.testslice1(a)
        self.log(pfx=0)
        self.testslice4(a)

    def testslice1(self, a):
        if a is None: a = ['A', 'B', 'C', 'D', 'E']
        self.log(f'a = {fmtl(a, w=2, u=">"):21}')
        b = a[-1:]
        c = a[:-1]
        a = a[-1:] + a[:-1]
        self.log(f'b = {fmtl(b, w=2, u=">"):21} : a[-1:]')
        self.log(f'c = {fmtl(c, w=2, u=">"):21} : a[:-1]')
        self.log(f'a = {fmtl(a, w=2, u=">"):21} : a = b + c = a[-1:] + a[:-1]')

    def testslice2(self, a):
        for k in range(len(a)+1):
            b = a[-1:k:-1]
            self.log(f'b = {fmtl(b, w=2, u=">"):21} : a[-1:{k}:-1]')
        for k in range(len(a)+3):
            b = a[-1:-k:-1]
            self.log(f'b = {fmtl(b, w=2, u=">"):21} : a[-1:{-k}:-1]')
        for k in range(len(a)+1):
            c = a[k:-1]
            self.log(f'c = {fmtl(c, w=2, u=">"):21} : a[{k}:-1]')
        for k in range(len(a)+2):
            c = a[-k:-1]
            self.log(f'c = {fmtl(c, w=2, u=">"):21} : a[-{k}:-1]')

    def testslice3(self, a):
        for k in range(len(a)+1):
            c = a[k:-2]
            self.log(f'c = {fmtl(c, w=2, u=">"):21} : a[{k}:-2]')
        for k in range(len(a)+1):
            c = a[k:-1]
            self.log(f'c = {fmtl(c, w=2, u=">"):21} : a[{k}:-1]')
        for k in range(len(a)+1):
            c = a[k:0]
            self.log(f'c = {fmtl(c, w=2, u=">"):21} : a[{k}:0]')
        for k in range(len(a)+1):
            c = a[k:1]
            self.log(f'c = {fmtl(c, w=2, u=">"):21} : a[{k}:1]')
        for k in range(len(a)+1):
            c = a[k:2]
            self.log(f'c = {fmtl(c, w=2, u=">"):21} : a[{k}:2]')

    def testslice4(self, a):
        for k in         [-2, -1, 1, 2]:
            for j in     range(-len(a)-2, len(a)+1):
                for i in range(-len(a)-2, len(a)+1):
                    c = a[i:j:k]
                    self.log(f'a[ {i:2} {j:2} {k:2} ] = {fmtl(c, w=2, u=">")}')
                self.log(f'a =  {fmtl(a)}   j = {j:2}   k = {k:2}', pfx=0)

    def tt0(self, s):
        tt, nn, ii, kk = self.TNIK
        if   s == 0: return TT if tt else NN if nn else II if ii else KK if kk else -1
        elif s == 1: return NN if nn and tt else II if ii and (not tt or not nn) else KK if kk and (not tt and not nn) or (not tt and not ii) or (not nn and not ii) else -1
        elif s == 2: return II if ii and (tt and nn) else KK if kk and (not tt or not nn or not ii) else -1
        elif s == 3: return KK if kk and (tt and nn and ii) else -1
    def OLD__tt0(self, s):
        tt, nn, ii, kk = self.TNIK
        if   s == 0: return TT if tt else NN if nn else II if ii else KK if kk else -1
        elif s == 1: return NN if nn else II if ii else KK if kk else -1
        elif s == 2: return II if ii else KK if kk else -1
        elif s == 3: return KK if kk else -1
    def tt1(self, s):
        tt, nn, ii, kk = self.TNIK
        if   s == 0: return TT if tt else -1
        elif s == 1: return NN if (nn and tt) or (nn and not tt) else -1
        elif s == 2: return II if (ii and nn and tt) or (ii and (nn or tt)) or (ii and not nn and not tt) else -1
        elif s == 3: return KK if (kk and ii and nn and tt) or (kk and (tt + nn + ii == 2)) or (kk and (tt + nn + ii == 1)) or (kk and not ii and not nn and not tt) else -1
    def tt2(self, s):
        tt, nn, ii, kk = self.TNIK
        if   tt and   s == 0: return TT
        elif nn and ((s == 1 and tt) or (s == 0 and not tt)): return NN
        elif ii and ((s == 2 and tt and nn) or (s == 1 and (tt or nn)) or (s == 0 and not tt and not nn)): return II
        elif kk and ((s == 3 and tt and nn and ii) or (s == 2 and (tt + nn + ii == 2)) or (s == 1 and(tt + nn + ii == 1)) or (s == 0 and (not tt and not nn and not ii))): return KK
        else: return -1
    ####################################################################################################################################################################################################
    def createLabels(self):
        self.dumpGeom('BGN')
        self.dumpTNIK()
        for page in              self.g_createLabelsA(None, P, self.pages):
            for line in          self.g_createLabelsA(page, L, self.lines):
                for sect in      self.g_createLabelsB(line, S, self.sects):
                    for col in   self.g_createLabelsA(sect, C, self.cols):
                        for _ in self.g_createLabelsC(col):
                            pass
        self.dumpTNIK()
        self.dumpGeom('END')
    ####################################################################################################################################################################################################
    def g_createLabelsA(self, p, j, lablist, nn=0, dbg=1, dbg2=0):
        n, i, x, y, w, h, g, mx, my = self.geom(p=p, j=j, init=1, nn=nn, dbg=dbg2)   ;   kl = self.k[j]   ;  x2 = x  ;  y2 = y
        for i in range(n):
            if   j == C: x2 = x + i * w
            elif p:      y2 = y - i * h
            self.J1[j] = i
            if nn and j != L:         self.J2[j] = len(self.E[j])
            lbl = self.createLabel(p=lablist, j=j, x=x2, y=y2, w=w, h=h, kk=self.cci(j, kl), g=g, why='new ', kl=kl, dbg=dbg)
            if QQ and j == L: self.createLLRow(lbl, i)
            yield lbl

    def g_createLabelsB(self, p, j, lablist, nn=0, dbg=1, dbg2=0):
        n, i, x, y, w, h, g, mx, my = self.geom(p=p, j=j, init=1, nn=nn, dbg=dbg2)   ;   kl = self.k[j]   ;  x2 = x   ;   i2 = 0
        self.log(f'{fmtl(self.TNIK)} n={fmtl(self.n)} j={j} nn={nn} n={n}')
        for i, t in enumerate(self.TNIK): # range(len(self.TNIK)):
            if t: y2 = y - i2 * h   ;   i2 += 1
            else: continue
            self.log(f'i={i} i2={i2} t={t} J1={fmtl(self.J1)} J2={fmtl(self.J2)}')
            self.J1[j] = i   ;   self.J2[j] = len(self.E[j])
            lbl = self.createLabel(p=lablist, j=j, x=x2, y=y2, w=w, h=h, kk=self.cci(j, kl), g=g, why='new ', kl=kl, dbg=dbg)
            yield lbl
    ####################################################################################################################################################################################################
    def g_createLabelsC(self, col, dbg=1, dbg2=0):
        p, l, s, c = self.J1[P], self.J1[L], self.J1[S], self.J1[C]    ;   t2 = 0   ;   stnik = self.ss()
        kt, kn, ki, kkk = self.kt, self.kn, self.ki, self.kk           ;   kt2, kn2, ki2, kk2 = self.kt2, self.kn2, self.ki2, self.kk2
        n, i, x, y, w, h, g, mx, my = self.geom(p=col, j=T, init=1, dbg=dbg2)
        imap = self.getImap(p, l, c, s)
        for t in range(n):
            why = 'new '
            if   s == TT: # and self.TNIK[TT]:
                if   CCC     and c == C1:   tab = self.stringNumbs[t]  ;  plist = self.snos   ;  kl = kt2  ;  k = self.cci(t, kl)  ;  j = O
                elif CCC > 1 and c == C2:   tab = self.stringCapo[t]   ;  plist = self.capsA  ;  kl = kt2  ;  k = self.cci(t, kl)  ;  j = D
                else:               tab = self.data[p][l][c-CCC][t]    ;  plist = self.tabs   ;  kl = kt   ;  k = self.cci(t, kl)  ;  j = T
                self.createLabel(plist, j, x, y - t*h, w, h, k, g, why=why, t=tab,  kl=kl, dbg=dbg)  ;  yield tab
            elif s == NN: # and self.TNIK[NN]:
                if   CCC     and c == C1:  note = self.stringNames[t]  ;  plist = self.snas   ;  kl = kn2  ;  k = self.cci(t, kl)  ;  j = A
                elif CCC > 1 and c == C2:  note = self.stringCapo[t]   ;  plist = self.capsB  ;  kl = kn2  ;  k = self.cci(t, kl)  ;  j = E
                else:               tab = self.data[p][l][c-CCC][t]    ;  plist = self.notes  ;  kl = kn   ;  k = self.cci(t, kl)  ;  j = N  ;  note = self.tab2nn(tab, t) if self.isFret(tab) else self.tblank
                self.createLabel(plist, j, x, y - t*h, w, h, k, g, why=why, t=note, kl=kl, dbg=dbg)  ;  yield note
            elif s == II: # and self.TNIK[II]:
                if   CCC     and c == C1:  ikey = self.strLabel[t]     ;  plist = self.lstrs  ;  kl = kk2  ;  k = self.cci(t, kl)  ;  j = F
                elif CCC > 1 and c == C2:  ikey = self.cpoLabel[t]     ;  plist = self.lcaps  ;  kl = kk2  ;  k = self.cci(t, kl)  ;  j = G
                else:
                    imap0 = imap[0][::-1] if imap and len(imap) else []
                    dd = self.data[p][l][c]   ;   fdd = self.isFret(dd[t])   ;   j = I
                    if imap0 and len(imap0) > t2: ikey = imap0[t2] if fdd else self.tblank    ;   t2 += 1 if fdd else 0
                    else:                         ikey = self.tblank
                    if dbg2: cc = self.plct2cc(p, l, c, 0)   ;   self.dumpDataSlice(p, l, c, cc)  ;  self.log(f'cc={cc} t={t} t2={t2} imap0={imap0} fdd={fdd} dd={dd} ikey={ikey}')
                    plist = self.ikeys  ;  kl = ki  ;  k = self.cci(t, kl)
                self.createLabel(plist, j, x, y - (n-1-t)*h, w, h, k, g, why=why, t=ikey, kl=ki, dbg=dbg)   ;  yield ikey
            elif s == KK: # and self.TNIK[KK]:
                if   CCC     and c == C1: chord = self.strLabel[t]     ;  plist = self.lstrs  ;  kl = kk2  ;  k = self.cci(t, kl)  ;  j = F
                elif CCC > 1 and c == C2: chord = self.cpoLabel[t]     ;  plist = self.lcaps  ;  kl = kk2  ;  k = self.cci(t, kl)  ;  j = G
                else:
                    chunks = imap[4] if (imap and len(imap) > 4) else []
                    chord = chunks[t] if len(chunks) > t else self.tblank   ;   j = K
                    plist = self.chords ;  kl = kkk ;  k = self.cci(t, kl)
                self.createLabel(plist, j, x, y - t*h, w, h, k, g, why=why, t=chord, kl=kl, dbg=dbg) ;  yield chord
            elif not stnik and not s: self.log(f'WARN skip s={s} {fmtl(self.TNIK)} stnik={stnik}') if dbg2 else None
#            else: msg = f'ERROR tti={self.tti()} s={s} n={fmtl(self.n)} {fmtl(self.TNIK)} {self.ss()} tt nn kk={int(tt)} {int(nn)} {int(kk)} {fmtl(self.lenE())}'  ;  self.log(msg)  ;  self.quit(msg) #  yield None
    ####################################################################################################################################################################################################
    def createSprites(self, dbg=1):
        self.dumpGeom('BGN')  ;  v = 0
        if dbg: self.dumpTNIK()
        for page, v in             self.g_createSprites(None, P, self.pages, v):
            for line, _ in         self.g_createSprites(page, L, self.lines, v):
                for sect, _ in     self.g_createSprites(line, S, self.sects, v):
                    for col, _ in  self.g_createSprites(sect, C, self.cols,  v):
                        for _ in   self.g_createLabelsC(col):
                            pass
        if dbg: self.dumpTNIK()
        self.dumpGeom('END')

    def g_createSprites(self, p, j, sprlist, v, dbg=1, dbg2=0):
        n, i, x, y, w, h, g, mx, my = self.geom(p=p, j=j, init=1, dbg=dbg2)  ;  x2 = x  ;  y2 = y  ;  kl=self.k[j]
        for tt in range(n):
            if   j == C:     x2 = x + tt * w
            elif p:          y2 = y - tt * h
            self.J1[j] = tt
            if   j == P:    v=1 if self.J2[j] == self.i[P] else 0
            spr = self.createSprite(sprlist, j, x2, y2, w, h, self.cci(j, kl), g, why=f'new ', kl=kl, v=v, dbg=dbg)
            if QQ and j == L: self.createLLRow(spr, tt)
            yield spr, v
    ####################################################################################################################################################################################################
    def resizeLabels(self, dbg=0):
        self.dumpGeom('BGN')
        if dbg: self.dumpTNIK()
        for page in              self.g_resizeLabelsA(None, P, self.pages, why=JTEXTS[P]):
            for line in          self.g_resizeLabelsA(page, L, self.lines, why=JTEXTS[L]):
                for sect in      self.g_resizeLabelsB(line, S, self.sects, why=JTEXTS[S]):
                    for col in   self.g_resizeLabelsA(sect, C, self.cols,  why=JTEXTS[C]):
                        for _ in self.g_resizeLabelsC(col):
                            pass
        if dbg: self.dumpTNIK()
        self.dumpGeom('END')
    ####################################################################################################################################################################################################
    def g_resizeLabelsA(self, p, j, lablist, why, dbg=1, dbg2=0):
        n, i, x, y, w, h, g, mx, my = self.geom(p=p, j=j, dbg=dbg2)   ;   x2 = x   ;   y2 = y
        for tt in range(n):
            if   j == C: x2 = x + tt * w
            elif p:      y2 = y - tt * h
            assert(len(lablist))
            lbl = lablist[self.J2[j]]  ;  lbl.x = x2  ;  lbl.y = y2  ;  lbl.width = w  ;  lbl.height = h
            self.J1[j] = tt   ;   self.J2[j] += 1
            if dbg:           self.dumpTNIK(lbl, *self.ids(), *self.cnts(), why=f'mod {why} {self.J2[j]}')
            if QQ and j == L: self.resizeLLRow(lbl, tt)
            yield lbl

    def g_resizeLabelsB(self, p, j, lablist, why, dbg=1, dbg2=0):
        n, i, x, y, w, h, g, mx, my = self.geom(p=p, j=j, dbg=dbg2)   ;   x2 = x   ;   i2 = 0
        for i, t in enumerate(self.TNIK):
            if t: y2 = y - i2 * h   ;   i2 += 1
            else: continue
            assert(len(lablist))
            lbl = lablist[self.J2[j]]  ;  lbl.x = x2  ;  lbl.y = y2  ;  lbl.width = w  ;  lbl.height = h
            self.J1[j] = i   ;   self.J2[j] += 1
            if dbg:           self.dumpTNIK(lbl, *self.ids(), *self.cnts(), why=f'mod {why} {self.J2[j]}')
            yield lbl
    ####################################################################################################################################################################################################
    def g_resizeLabelsC(self, col, dbg=1, dbg2=0):
        tab, note, ikey, chord = None, None, None, None   ;   stnik = self.ss()
        p,       l,    s,    c      = self.J1[P], self.J1[L], self.J1[S], self.J1[C]
        st,     sn,   si,   sk      = self.J2[T], self.J2[N], self.J2[I], self.J2[K]
        ssno, ssna, scapA, scapB, slstr, slcap =  self.J2[O], self.J2[A], self.J2[D], self.J2[E], self.J2[F], self.J2[G]
        n, i, x, y, w, h, g, mx, my = self.geom(p=col, j=T, dbg=dbg2)   ;   lbl = None   ;   why0 = f'{s}'
        for t in range(n):
            why = f'{why0} mod '
            if   s == TT: # and self.TNIK[TT]:
                if   CCC     and c == C1:   tab = self.snos[ssno]     ;   ssno += 1   ;  why += f'SNo {ssno}'
                elif CCC > 1 and c == C2:   tab = self.capsA[scapA]   ;  scapA += 1   ;  why += f'CapA {scapA}'
                elif st < len(self.tabs):   tab = self.tabs[st]       ;     st += 1   ;  why += f'Tab {st}'
                else: msg = f'ERROR indexing {why0} sn={st} len={len(self.tabs)}'   ;   self.dumpGeom(msg)   ;   self.quit(msg)
                tab.width = w    ;   tab.height = h    ;  tab.x = x   ;   tab.y = y - t * h  ;  lbl = tab
                self.J1[T] = t   ;   self.J2[T] = st   ;  self.J2[O] = ssno   ;  self.J2[D] = scapA
                if dbg:   self.dumpTNIK(lbl, *self.ids(), *self.cnts(), why=why)
            elif s == NN: #  and self.TNIK[NN]:
                if   CCC     and c == C1:  note = self.snas[ssna]     ;   ssna += 1   ;  why += f'SNam {ssna}'
                elif CCC > 1 and c == C2:  note = self.capsB[scapB]   ;  scapB += 1   ;  why += f'CapB {scapB}'
                elif sn < len(self.notes): note = self.notes[sn]      ;     sn += 1   ;  why += f'Note {sn}'
                else: msg = f'ERROR indexing {why0} sn={sn} len={len(self.notes)}'   ;   self.dumpGeom(msg)   ;   self.quit(msg)
                note.width = w   ;  note.height = h    ; note.x = x   ;  note.y = y - t * h  ;  lbl = note
                self.J1[N] = t   ;   self.J2[N] = sn   ;  self.J2[A] = ssna   ;  self.J2[E] = scapB
                if dbg:   self.dumpTNIK(lbl, *self.ids(), *self.cnts(), why=why)
            elif s == II: #  and self.TNIK[II]:
                if   CCC     and c == C1:  ikey = self.lstrs[slstr]   ;  slstr += 1   ;  why += f'LStr {slstr}'
                elif CCC > 1 and c == C2:  ikey = self.lcaps[slcap]   ;  slcap += 1   ;  why += f'LCap {slcap}'
                elif si < len(self.ikeys): ikey = self.ikeys[si]      ;     si += 1   ;  why += f'IKey {si}'
                else: msg = f'ERROR indexing {why0} si={si} len={len(self.ikeys)}'   ;   self.dumpGeom(msg)    ;   self.quit(msg)
                ikey.width = w  ;  ikey.height = h    ;  ikey.x = x  ;  ikey.y = y - t * h  ;  lbl = ikey
                self.J1[I] = t   ;   self.J2[I] = si   ;  self.J2[F] = slstr  ;  self.J2[G] = slcap
                if dbg:   self.dumpTNIK(lbl, *self.ids(), *self.cnts(), why=why)
            elif s == KK: #  and self.TNIK[KK]:
                if   CCC     and c == C1:   chord = self.lstrs[slstr]   ;  slstr += 1   ;  why += f'LStr {slstr}'
                elif CCC > 1 and c == C2:   chord = self.lcaps[slcap]   ;  slcap += 1   ;  why += f'LCap {slcap}'
                elif sk < len(self.chords): chord = self.chords[sk]     ;     sk += 1   ;  why += f'Chord {sk}'
                else: msg = f'ERROR indexing {why0} sk={sk} len={len(self.chords)}'   ;   self.dumpGeom(msg)   ;   self.quit(msg)
                chord.width = w  ; chord.height = h    ; chord.x = x  ; chord.y = y - t * h  ;  lbl = chord
                self.J1[K] = t   ;   self.J2[K] = sk   ;  self.J2[F] = slstr  ;  self.J2[G] = slcap
                if dbg:   self.dumpTNIK(lbl, *self.ids(), *self.cnts(), why=why)
            else: msg = f'ERROR skip {why0} {fmtl(self.TNIK)} {stnik}'   ;   self.dumpGeom()    ;   self.quit(msg)
            yield lbl
    ####################################################################################################################################################################################################
    def resizeSprites(self, dbg=1):
        self.dumpGeom('BGN')
        if dbg: self.dumpTNIK()
        for page in              self.g_resizeSprites(None, P, self.pages, why=JTEXTS[P]):
            for line in          self.g_resizeSprites(page, L, self.lines, why=JTEXTS[L]):
                for sect in      self.g_resizeSprites(line, S, self.sects, why=JTEXTS[S]):
                    for col in   self.g_resizeSprites(sect, C, self.cols,  why=JTEXTS[C]):
                        for _ in self.g_resizeLabelsC(col):
                            pass
        if dbg: self.dumpTNIK()
        self.dumpGeom('END')

    def g_resizeSprites(self, p, j, sprlist, why, dbg=1, dbg2=0):
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

    ########################################################################################################################################################################################################
if __name__ == '__main__':
    backPath = getFilePath(filedir='logs', filesfx='.blog')
#    print(f'backPath={backPath}')
    LOG_PATH = getFilePath(filedir='logs', filesfx='.log')
    if backPath:               os.system(f'copy {LOG_PATH} {backPath}')
    with open(str(LOG_PATH), 'w') as LOG_FILE:
        Tabs.slog(f'LOG_PATH={LOG_PATH} LOG_FILE={LOG_FILE}')
        Tabs()
        ret     = pyglet.app.run()
        Tabs.slog(f'pyglet.app.run() returned {ret}, Exiting main')
