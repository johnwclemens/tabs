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
    if d1 == '': d2 = ''
    if  w is None:  w = 0
    t = ''   ;   s = f'<{len(lst)}' if ll else ''
    for i, l in enumerate(lst):
        if type(l) in (list, tuple, set):
#            d0 = sep + d1 if not i else d1    ;    d3 = d2 + sep
            if type(w) in (list, tuple, set):       t += fmtl(l, w[i], u, d1, d2, sep, ll, z)
            else:                                   t += fmtl(l, w,    u, d1, d2, sep, ll, z)
        else:
            ss = sep if i < len(lst)-1 else ''
            if type(l) is type:                     l = str(l)
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
AUTO_SAVE = 0  ;  CAT = 0  ;  CHECKER_BOARD = 0  ;  EVENT_LOG = 0  ;  FULL_SCREEN = 0  ;  IND = 0  ;  ORDER_GROUP = 1  ;  RESIZE = 1  ;  SEQ_FNAMES = 1  ;  SNAP = 1  ;  SUBPIX = 1  ;  VERBOSE = 0  ;  EXIT = 0
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
LOG_FILE         = None   ;   Z = ' '
FDL              = ' len(data 0 00 000)'
FDT              = 'type(data 0 00 000)'
FMTN             = (2, 2, 2, 3, 1) # p, l, s, c, t remove?
FMTN2            = (1, 2, 2, 2, 2, 2) # generalize for any # of strings
P, L, S, C       =  0,  1,  2,  3
T, N, I, K       =  4,  5,  6,  7
O, A, D          =  8,  9, 10
LLR, LLC         = 11, 12
TT, NN, II, KK   =  0,  1,  2,  3
C1,  C2,  RLC    = 0, 1, 2
JTEXTS           = ['Page',  'Line',  'Sect',  'Col',  'Tab',  'Note',  'IKey',  'Chord',  '_SNo',  '_SNam',  '_Capo',  '_LLR',  '_LLC', '_TNIK']
jTEXTS           = ['pages', 'lines', 'sects', 'cols', 'tabs', 'notes', 'ikeys', 'chords', 'snos', 'snams', 'capos', 'lrows', 'lcols', 'tniks']
JFMT             = [1, 1, 2, 3,  3, 3, 3, 3,  2, 2, 2,  1, 3, 3]
NORMAL_STYLE, CURRENT_STYLE, SELECT_STYLE, COPY_STYLE = 0, 1, 2, 3
INIT             = '###   Init   ###' * 13
QUIT             = '###   Quit   ###' * 13
MELODY, CHORD, ARPG   = 0, 1, 2
LEFT, RIGHT, UP, DOWN = 0, 1, 0, 1
CSR_MODES        = ['MELODY', 'CHORD', 'ARPG']
HARROWS, VARROWS = ['LEFT', 'RIGHT'], ['UP', 'DOWN']
####################################################################################################################################################################################################
OPACITY          = [ 255, 240, 225, 210, 190, 165, 140, 110, 80 ]
GRAY             = [(255, 255, 255, OPACITY[0]), (  0,   0,   0, OPACITY[0])]
PINK             = [(255,  64, 192, OPACITY[0]), ( 57,  16,  16, OPACITY[0])]
INFRA_RED        = [(200, 100,  24, OPACITY[0]), ( 68,  20,  19, OPACITY[0])]
RED              = [(255,  12,  11, OPACITY[0]), ( 88,  15,  12, OPACITY[0])]
ORANGE           = [(255, 128,   0, OPACITY[0]), ( 76,  30,  25, OPACITY[0])]
YELLOW           = [(255, 255,  10, OPACITY[0]), ( 45,  41,  10, OPACITY[0])]
GREEN            = [( 12, 255,  11, OPACITY[0]), ( 21,  54,  10, OPACITY[0])]
GREEN_BLUE       = [( 24, 255,  98, OPACITY[0]), ( 10,  49,  25, OPACITY[0])]
CYAN             = [( 13, 255, 255, OPACITY[0]), ( 16,  64,  64, OPACITY[0])]
BLUE_GREEN       = [( 15, 122, 255, OPACITY[0]), ( 12,  37,  51, OPACITY[0])]
BLUE             = [( 13,  11, 255, OPACITY[0]), ( 19,  11,  64, OPACITY[0])]
INDIGO           = [(255,  22, 255, OPACITY[0]), ( 19,  11,  64, OPACITY[0])]
VIOLET           = [(176,  81, 255, OPACITY[0]), ( 44,  14,  58, OPACITY[0])]
ULTRA_VIOLET     = [(194,  96, 255, OPACITY[3]), ( 50,  19,  61, OPACITY[1])]
CC               = [(155, 155,  10, OPACITY[4]), (200, 200,  10, OPACITY[4])]
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
FONT_SCALE    = 0.8 # 8pts/10pix pts/pux
FONT_DPIS     = [72, 78, 84, 90, 96, 102, 108, 114, 120]
FONT_NAMES    = ['Lucida Console', 'Helvetica', 'Arial', 'Times New Roman', 'Courier New', 'Century Gothic', 'Bookman Old Style', 'Antique Olive']
FONT_COLORS_S = [PINKS[0], CYANS[0], REDS[0], BLUES[0], YELLOWS[0], GREENS[0], ORANGES[0], VIOLETS[0], REDS[13], YELLOWS[15], GREEN_BLUES[8], ORANGES[12], INDIGOS[8], ULTRA_VIOLETS[9], BLUE_GREENS[8], CC]
FONT_COLORS_L = [PINKS[0], GRAYS[0], BLUES[0], GREENS[0], YELLOWS[0], REDS[0], GRAYS[1], PINKS[8], REDS[10], YELLOWS[15], GRAYS[8], GRAYS[8], INDIGOS[8], GRAYS[9], GRAYS[8], CC]
FONT_COLORS   =  FONT_COLORS_S if SPRITES else FONT_COLORS_L
####################################################################################################################################################################################################
class Tabs(pyglet.window.Window):
    hideST  = ['log', 'getImap', 'dumpGeom', 'dumpJ', 'dumpImap', 'dumpSmap', 'dumpCursorArrows', '<listcomp>', 'dumpLimap2', 'dumpData']
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
        self.log(f'snapGlobArg =  {snapGlobArg}')
        self.log(f'   snapGlob = { fmtl(snapGlob)}')
        self.deleteGlob(snapGlob, 'SNAP_GLOB')
        self.catPath = str(BASE_PATH / 'cats' / BASE_NAME) + '.cat'
        self.catPath = self.getFilePath(seq=1, filedir='cats', filesfx='.cat')
        self.log(f'catPath={self.catPath}')
        self.cobj = misc.Chord(self, LOG_FILE)
        misc.Note.setType(misc.Note.SHARP)  ;  self.log(f' Note.TYPE={misc.Note.TYPE}')
        self.shiftingTabs = 0   ;   self.shiftSign = 1
        self.inserting    = 0   ;   self.insertStr = ''
        self.jumping      = 0   ;   self.jumpStr   = ''   ;   self.jumpAbs = 0
        self.swapping     = 0   ;   self.swapSrc   = ''   ;   self.swapTrg = ''
        self.dfn = ''
        nt = 6
        self.ZZ   = [0, 0]
        self.TNIK = [1, 0, 0, 0]   ;   self.ss0 = self.ss()
        self.log(f'TNIK={(fmtl(self.TNIK))}')
        self.ww, self.hh = 640, 480
        self.n, self.i, self.x, self.y, self.w, self.h, self.g = [3, 3, self.ss0, 50, nt], [1, 1, 1, 1, nt], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], []
        self.log(f'argMap={fmtm(ARGS)}')
        if 'f' in ARGS and len(ARGS['f'])  > 0:    self.dfn =      ARGS['f'][0]
        if 'n' in ARGS and len(ARGS['n'])  > 0:    self.n   = [int(ARGS['n'][i]) for i in range(len(ARGS['n']))]
        if 'i' in ARGS and len(ARGS['i'])  > 0:    self.i   = [int(ARGS['i'][i]) for i in range(len(ARGS['i']))]
        if 'x' in ARGS and len(ARGS['x'])  > 0:    self.x   = [int(ARGS['x'][i]) for i in range(len(ARGS['x']))]
        if 'y' in ARGS and len(ARGS['y'])  > 0:    self.y   = [int(ARGS['y'][i]) for i in range(len(ARGS['y']))]
        if 'w' in ARGS and len(ARGS['w'])  > 0:    self.ww  =  int(ARGS['w'][0])
        if 'h' in ARGS and len(ARGS['h'])  > 0:    self.hh  =  int(ARGS['h'][0])
        if 'F' in ARGS and len(ARGS['F']) == 0: FULL_SCREEN =  1
        if 'g' in ARGS and len(ARGS['g']) == 0: ORDER_GROUP =  1
        if 's' in ARGS and len(ARGS['s']) == 0: SUBPIX      =  1
        self.log(f'[f]            f={     self.dfn}')
        self.log(f'[n]            n={fmtl(self.n, FMTN)}')
        self.log(f'[i]            i={fmtl(self.i, FMTN)}')
        self.log(f'[x]            x={fmtl(self.x, FMTN)}')
        self.log(f'[y]            y={fmtl(self.y, FMTN)}')
        self.log(f'[w]            w={fmtl(self.w, FMTN)}')
        self.log(f'[h]            h={fmtl(self.h, FMTN)}')
        self.log(f'[W]           ww={     self.ww}')
        self.log(f'[H]           hh={     self.hh}')
        self.log(f'[F]  FULL_SCREEN={FULL_SCREEN}')
        self.log(f'[g]  ORDER_GROUP={ORDER_GROUP}')
        self.log(f'[s]       SUBPIX={SUBPIX}')
        self.n[S] = self.ss()
        if   self.n[T] == 6: self.stringMap = collections.OrderedDict([('E2', 28), ('A2', 33), ('D3', 38), ('G3', 43), ('B3', 47), ('E4', 52)])
        elif self.n[T] == 7: self.stringMap = collections.OrderedDict([('E2', 28), ('A2', 33), ('D3', 38), ('G3', 43), ('B3', 47), ('E4', 52), ('A4', 57)])
        else:                self.stringMap = collections.OrderedDict([('E2', 28), ('A2', 33), ('D3', 38), ('G3', 43), ('B3', 47), ('E4', 52)])
        self.stringKeys        =  list(self.stringMap.keys())
        self.stringNames       = ''.join(reversed([str(k[0]) for k in       self.stringKeys]))
        self.stringNumbs       = ''.join([str(r+1)           for r in range(self.n[T])])
        self.stringCapo        = ''.join(['0'                for _ in range(self.n[T])])
        self.strLabel          = 'STRING'
        self.cpoLabel          = ' CAPO '
        self.log(f'stringMap   = {fmtm(self.stringMap)}')
        self.log(f'stringKeys  = {fmtl(self.stringKeys)}')
        self.log(f'stringNames =      {self.stringNames}')
        self.log(f'stringNumbs =      {self.stringNumbs}')
        self.log(f'stringCapo  =      {self.stringCapo}')
        self.log(f'strLabel    =      {self.strLabel}')
        self.log(f'cpoLabel    =      {self.cpoLabel}')
        self._initDataPath()
        if CAT: self.cobj.dumpOMAP(str(self.catPath))
        self._initWindowA()
        super().__init__(screen=self.screens[1], fullscreen=FULL_SCREEN, resizable=True, visible=False)
        self._initWindowB()
        self.allSelected    = 0
        self.dataHasChanged = 0
        self.hArrow, self.vArrow,  self.csrMode                                 = RIGHT, UP, CHORD    ;    self.dumpCursorArrows('init()')
        self.tblank, self.tblanki, self.tblankCol,   self.cursor,  self.data    = None, None, None, None, None
        self.J1,     self.J2,      self.cc, self.ci, self.SNAP0,   self.armSnap = None, None, 0, 0, 0, ''
        self.kbk,    self.symb,    self.mods,        self.symbStr, self.modsStr =             0, 0, 0, '', ''
        self._reinit()
        self.log(f'END {__class__} {VRSNX1} {VRSNX2} {VRSNX3}')
        self.log(f'{INIT}', pfx=0)

    def _reinit(self):
        self.log('BGN')
        self.rmap = {}
        self.pages, self.lines, self.sects,  self.cols   = [], [], [], []     ;  self.A = [self.pages, self.lines, self.sects,  self.cols]
        self.tabs,  self.notes, self.ikeys,  self.chords = [], [], [], []     ;  self.B = [self.tabs,  self.notes, self.ikeys,  self.chords]
        self.snos,  self.snas,  self.capos               = [], [], []         ;  self.C = [self.snos,  self.snas,  self.capos]
        self.lrows, self.lcols, self.tniks               = [], [], []         ;  self.D = [self.lrows, self.lcols, self.tniks]
        self.E = [*self.A, *self.B, *self.C, *self.D]
        self.log(f'E={fmtl(self.E)}')
#        self.DF = [0, 0, 0, 0,  0, 0, 0, 0,  0, 0, 0, 0, 0, 0,  0, 0, 0, 0]
        self.initJ('reinit')
        self.data    = []   ;    self.dataHasChanged = 0
        self.cursor,  self.caret   = None, None
        self.kbk,     self.symb, self.mods,  self.symbStr, self.modsStr = 0, 0, 0, '', ''
        self.cc,      self.ci,   self.SNAP0, self.armSnap               = 0, 0, 0, ''
        self.tblanki, self.tblanks  = 1, [' ', '-']                ;     self.tblank = self.tblanks[self.tblanki]
        self.tblankCol              = self.tblank * self.n[T]      ;  self.tblankRow = self.tblank * (self.n[C] + self.zz())
        self._init()
        self.log('END')

    def _init(self, dbg=0):
        self.dumpGeom('BGN')
        self.ssi = 0
        self._initColors()
        self._initData()
        if AUTO_SAVE: pyglet.clock.schedule_interval(self.autoSave, 10, how='autoSave timer')
        self._initTextLabels()
        self._initTniks()
        if self.TNIK[TT] and self.tabs: self.createCursor(self.g[T + 3]) # fix g index
        if dbg: self.dumpStruct('_init()')
        if EXIT: self.quit('EXIT TEST')
        self.dumpGeom('END')

    def _initTniks(self, dbg=1):
        self.dumpJ('init')
        self.dumpXYWH()   ;   self.ss()
        self.smap = {}
        self.createTniks()
        self.cobj.dumpMlimap('init')
        self.dumpXYWH()
        self.dumpJ('init')
        if dbg: self.dumpTniks('new2')

    def _initColors(self):
        self.kp  = [    VIOLETS[0],    VIOLETS[12]] if CHECKER_BOARD else [   VIOLETS[10]]
        self.kl  = [     BLUES[12],      BLUES[15]] if CHECKER_BOARD else [     BLUES[12]]
        self.ks  = [     CYANS[12],      CYANS[15]] if CHECKER_BOARD else [     CYANS[12]]
        self.kc  = [      GRAYS[9],      GRAYS[13]] if CHECKER_BOARD else [     GRAYS[13]]
        self.kt  = [    ORANGES[0],     ORANGES[8]] if CHECKER_BOARD else [    ORANGES[0]]
        self.kn  = [     GREENS[0],     GREENS[12]] if CHECKER_BOARD else [     GREENS[0]]
        self.ki  = [    YELLOWS[0],     YELLOWS[8]] if CHECKER_BOARD else [    YELLOWS[0]]
        self.kk  = [      CYANS[0],       CYANS[8]] if CHECKER_BOARD else [      CYANS[0]]
        self.kt2 = [      PINKS[0],       PINKS[8]] if CHECKER_BOARD else [      PINKS[0]]
        self.kn2 = [      PINKS[0],       PINKS[8]] if CHECKER_BOARD else [      PINKS[4]]
        self.ki2 = [      PINKS[0],       PINKS[8]] if CHECKER_BOARD else [      PINKS[0]]
        self.kk2 = [      PINKS[0],       PINKS[8]] if CHECKER_BOARD else [      PINKS[0]]
        self.klr = [    ORANGES[0],     ORANGES[8]] if CHECKER_BOARD else [    ORANGES[0]]
        self.klc = [      PINKS[0],       PINKS[8]] if CHECKER_BOARD else [      PINKS[0]]
        self.kll = [       REDS[0],        REDS[8]] if CHECKER_BOARD else [       REDS[0]]
        self.k   = [ self.kp, self.kl, self.ks, self.kc, self.kt, self.kn, self.ki, self.kk, self.kt2, self.kn2, self.ki2, self.kk2, self.klr, self.klc, self.kll ]
        [ self.log(f'[{i:2}] {fmtl(*e):3}') for i, e in enumerate(self.k) ]

    def _initData(self, dbg=1):
        self._initDataPath()
        if not self.dataPath1.exists(): self.log(f'dataPath1={self.dataPath1} file does not exist calling createBlankData()')  ;  self.dataPath1.touch()  ;  self.createBlankData()
        else:                           self.readDataFile()
        old = f'{fmtl(self.n)}'
        self.n[P], self.n[L], self.n[C], self.n[T] = self.data2plrc()   ;   self.log(f'reseting from n={old} to n={fmtl(self.n)}')
        self._initTpz()
        self.initBlank()
        if dbg:     self.dumpDataHorz()
        self.data = self.transposeData()
        if dbg:     self.dumpDataVert()
        self.saveDataFile('_initData()', f=2)
#        self.log(f'    assert: size=nt+2*(l*r+l-1) {nt:8,} + {2*(l*r+l-1)} = {size:8,} bytes assert isVert={self.isVert()}')
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
        np, nl, ns, nc, nt = self.n
        self.fs0 = FONT_SCALE * self.hh / (nl * ns * nt)
        self.log(f'fs0=FONT_SCALE*(hh/nl*ns*nt)={FONT_SCALE}*{self.hh}/{nl}*{ns}*{nt}={self.fs0}pt')
        self.fontBold, self.fontItalic, self.fontColorIndex, self.fontDpiIndex, self.fontNameIndex, self.fontSize = 0, 0, 0, 4, 0, self.fs0
        self.dumpFont()
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

    def _initTextLabels(self):
        self.labelTextA, self.labelTextB = [], []
        self.createLabelText()
        self.labelTextC = []  ;  self.labelTextC.append('M')         ;  self.labelTextC.extend(self.labelTextB)
        self.labelTextD = []  ;  self.labelTextD.extend(['R', 'M'])  ;  self.labelTextD.extend(self.labelTextB)
        self.llText = []
        self.llText.append(self.labelTextB)
        self.llText.append(self.labelTextC)
        self.llText.append(self.labelTextD)
        txt = ['    ', '  ', '']  ;  [ self.log(f'llText[{i}]={txt[i]}{fmtl(t)}', pfx=0) for i, t in enumerate(self.llText) ]

    def _initTpz(self, dbg=1):
        np, nl, ns, nc, nt = self.n
        self.tpc =  nt
        self.tps =  nc * self.tpc
        self.tpl =       self.tps
        self.tpp =  nl * self.tpl
        if dbg: self.log(f'tpz={fmtl(self.tpz())}')
    def tpz(self):   return self.tpp, self.tpl, self.tps, self.tpc
    ####################################################################################################################################################################################################
    def ss(self, dbg=0):   s = sum(self.TNIK)  ;    self.log(f'{s} {fmtl(self.TNIK)} {fmtl(self.n)}') if dbg else None   ;   return s   # return 0-4
    def zz(self, dbg=0):   z = sum(self.ZZ)    ;    self.log(f'{z} {fmtl(self.ZZ)} {  fmtl(self.n)}') if dbg else None   ;   return z   # return 0-2
    def dd(self, data=None): data = self.data if data is None else data   ;   return data, data[0], data[0][0], data[0][0][0]
    def dl(self, data=None): data = self.data if data is None else data   ;   return list(map(len,  self.dd(data)))
    def dt(self, data=None): data = self.data if data is None else data   ;   return list(map(type, self.dd(data)))
    def cnts(self):  return self.J2[:]
    def lenA(self):  return [ len(_) for _ in self.A ]
    def lenB(self):  return [ len(_) for _ in self.B ]
    def lenC(self):  return [ len(_) for _ in self.C ]
    def lenD(self):  return [ len(_) for _ in self.D ]
    def lenE(self):  return [ len(_) for _ in self.E ]
    def j(self):     return [ i-1 if i else 0 for i in self.i ]
    def j2(self):    return [ i-1 if i else 0 for j, i in enumerate(self.i)  if j != S ]
    def j3(self):    return [ i-1 if i else 0 for j, i in enumerate(self.i)  if j != S and j != T ]
    def initJ(self, why='init', dbg=1): self.J1    = [ 0 for _ in self.E ]     ;   self.J2     = [ 0 for _ in self.E ]   ;   self.dumpJ(why) if dbg else None
    def setJs(self, j, v):              self.J1[j] = v   ;   self.J2[j] += 1   ;   self.J1[-1] += 1   ;   self.J2[-1] += 1
    ####################################################################################################################################################################################################
    def fmtDD(self, data=None, d='x'): l=list(map(str, self.dl(data)))  ;  return f'({d.join(l)})'
    def fmtdl(self, data=None): data = self.data if data is None else data   ;   return f'{FDL}={self.dl(data)}'
    def fmtdT(self, data=None): data = self.data if data is None else data   ;   return f'{FDT}={self.dt(data)}'
    def fmtWH(self, w=None, h=None, d='x'): (w, h) = (self.ww, self.hh) if not w and not h else (w, h)  ;  return f'({w}{d}{h})'
    def fPos(self):  plct = self.j2()   ;   cc = self.plct2cc(*plct)   ;   cn = self.cc2cn(cc)   ;   return f'{fmtl(plct)} {cc:3} {cn:2}]'
    ####################################################################################################################################################################################################
    def dumpGlobalFlags(self):
        txt1 = f'AUTO_SAVE={AUTO_SAVE} CAT={CAT} CHECKER_BOARD={CHECKER_BOARD} EVENT_LOG={EVENT_LOG} FULL_SCREEN={FULL_SCREEN} IND={IND} '
        txt2 = f'ORDER_GROUP={ORDER_GROUP} RESIZE={RESIZE} SEQ_FNAMES={SEQ_FNAMES} SNAP+{SNAP} SUBPIX={SUBPIX} VERBOSE={VERBOSE}'
        self.log(f'{txt1} {txt2}', pfx=0)

    def dumpDataSlice(self, p, l, c, cc):
        for t in range(self.n[T]):
            ikeys  = self.ikeys[ cc+t].text if self.ikeys  and len(self.ikeys)  > cc+t else ''
            chords = self.chords[cc+t].text if self.chords and len(self.chords) > cc+t else ''
            self.log(f'{self.data[p][l][c]} [{cc+t}] {self.tabs[cc+t].text:2} {self.notes[cc+t].text:2} {ikeys:2} {chords:2}')
    @staticmethod
    def dumpObj( obj,  name, why='', file=None): Tabs.slog(f'{why} {name} ObjId {hex(id(obj))} {type(obj)}', file=file)
    @staticmethod
    def dumpObjs(objs, name, why=''): [Tabs.dumpObj(o, name, why) for o in objs]  # ;   [Tabs.slog(f'{hex(id(o))} type={type(o)}', pfx=0) for o in obj]   ;    Tabs.slog(pfx=0)
    def dumpGeom(self, why1='', why2=''):   e = self.lenE()   ;   self.log(f'{why1} {QQ} {self.zz()} {fmtl(self.ZZ)} {fmtl(self.TNIK)} {self.ss()} {fmtl(self.n)} {fmtl(self.i)} {fmtl(e)} {sum(e[:-1])} {why2}')
    def dumpJ(   self, why):        self.log(f' J1 {fmtl(self.J1, w=JFMT)} {sum(self.J1[:-1]):4} {why}')  ;  self.log(f' J2 {fmtl(self.J2, w=JFMT)} {sum(self.J2[:-1]):4} {why}')
    def dumpNI(  self): self.log(f'    {self.fmtDD()} {self.fmtWH():^11} {fmtl(self.n, w=FMTN, u=">")} {fmtl(self.i, w=FMTN, u=">")}')
    def dumpXY(  self): self.log(f'    {self.fmtDD()} {self.fmtWH():^11} {fmtl(self.x, w="7.2f", u=">")} {fmtl(self.y, w="7.2f", u=">")}')
    def dumpWH(  self): self.log(f'    {self.fmtDD()} {self.fmtWH():^11} {fmtl(self.w, w="7.2f", u=">")} {fmtl(self.h, w="7.2f", u=">")}')
    def dumpXYWH(self): self.dumpNI()  ;  self.dumpXY()  ;  self.dumpWH() # ;  self.log(f'{fmtl(self.x, w="7.2f", u=">")} {fmtl(self.y, w="7.2f", u=">")} {fmtl(self.w, w="7.2f", u=">")} {fmtl(self.h, w="7.2f", u=">")}')
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
        if dbg: self.log(f'BGN {self.fmtDD(self.data)} {self.fmtWH()} {fmtl(self.n)} {(fmtl(self.TNIK))} {fmtl(self.lenE()[:-1])} {sum(self.lenE()[:-1])}')
        if dbg: self.dumpXYWH()
        self.initJ(f'BGN {why}')
        if RESIZE: self.resizeTniks()
        self.dumpJ(f'END {why}')
        self.dumpStruct2(why)
#        self.resizeFonts()
        if not self.cursor and self.tabs and self.TNIK[TT]:  self.createCursor(self.g[T + 3]) # fix g index
        elif   self.cursor:                                  self.resizeCursor()
#        self.snapshot()
#        if dbg: self.dumpStruct(why)
        if dbg: self.setCaption(self.fmtf())
        if dbg: self.log(f'END {self.fmtDD(self.data)} {self.fmtWH()} {fmtl(self.n)} {(fmtl(self.TNIK))} {fmtl(self.lenE()[:-1])} {sum(self.lenE()[:-1])}')
    ####################################################################################################################################################################################################
    def dumpStruct(self, why=''):
        self.log(f'BGN {why}')
#        self.dumpData(why)
        self.dumpTniks(why)
#        self.dumpTabs(why)
#        self.dumpCols(why)
        self.log(f'END {why}')

    def dumpStruct2(self, why=''):
        self.dumpGeom('BGN')
        self.log(f'tpz={fmtl(self.tpz())}')
        self.dumpFont(why)
        self.dumpGlobalFlags()
        self.dumpGeom('   ')
        self.log(f'    {self.fmtDD(self.data)} {self.fmtWH():^11}')
        self.cobj.dumpMlimap(why)
        self.dumpGeom('END')
    ####################################################################################################################################################################################################
    def saveDataFile(self, how, f=0, dbg=1):
        if dbg:   self.log(f'{how} f={f}')
        if not f and AUTO_SAVE: dataPath = self.dataPath0
        else:                   dataPath = self.dataPath1 if f == 1 else self.dataPath2
        with open(dataPath, 'w') as DATA_FILE:
            self.log(f'{DATA_FILE.name:40}', pfx=0)
            np, nl, nc, nr = self.dl()
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
                        DATA_FILE.write(f'{text}\n')
                    if l < nl: DATA_FILE.write('\n')
    ####################################################################################################################################################################################################
    def createBlankData(self):
        self.log('Creating tab data using parameters {} {} {} {} {}'.format(*self.n))
        np, nl, ns, nc, nr = self.n  ;  nc += self.zz()
        self.data = [ [ [ self.tblankRow for _ in range(nr) ] for _ in range(nl) ] for _ in range(np) ]

    def data2plrc(self, data=None, dbg=1):
        data = self.data if data is None else data   ;   dl = self.dl(data)
        plrc = dl if self.isVert() else dl[0], dl[1], dl[3], dl[2]
        self.log(f'dl={fmtl(dl)} plrc={fmtl(plrc)}') if dbg else None   ;   return plrc

    def readDataFile(self, dbg=1):
        np, nl, ns, nc, nr = self.n
        self.log(f'BGN {fmtl(self.n)} dataPath1={self.dataPath1}')
        with open(str(self.dataPath1), 'r') as DATA_FILE:
            DATA_FILE.seek(0, 2)    ;   size = DATA_FILE.tell()   ;   DATA_FILE.seek(0, 0)   ;   self.log(f'    {DATA_FILE.name:40} {size:8,} bytes = {size/1024:6,.1f} KB')
            pages, lines, rows, cols = [], [], [], []   ;   sp, sl, sr, sc = 0, 0, 0, 0   ;   txt = 'cols'
            if dbg: self.log(f' p  l  r   c  sp sl  sr   sc  <{txt:10}>                      lp ll  lr   lc', pfx=0)
            for cols in DATA_FILE:
                cols = cols.strip()  ;   msg = f'<{cols}>'   ;   lc = len(cols)
                p = sp % np  ;  l = sl % nl  ;  r = sr % nr  ;    c = sc % nc
                if cols:                rows.append(cols)    ;   sr += 1   ;    sc += lc    ;   msg2 = '  rows.append(cols) '
                else:
                    if not (sr % nr):  lines.append(rows)    ;   sl += 1   ;    rows = []   ;   msg2 = ' lines.append(rows) '
                    if not (sl % nl):  pages.append(lines)   ;   sp += 1   ;   lines = []   ;   msg2 = ' pages.append(lines)'
                if dbg: self.log(f' {p}  {l} {r:2} {c:3}   {sp} {sl:2} {sr:3} {sc:4}  {msg:12} {msg2}  {len(pages)} {len(lines):2} {len(rows):3} {len(cols):4}', pfx=0)
            self.data = pages
        nt   = sp * sl * sc * sr
        self.log(f'    read {sp:1} Pages {sl:2} Lines {sl*sc:6,} Cols {sl*sr:4,} Strings {nt:8,} Tabs, isVert={self.isVert()}')
#        self.log(f'    assert: size=nt+2*(l*r+l-1) {nt:8,} + {2*(l*r+l-1)} = {size:8,} bytes assert isVert={self.isVert()}')
        self.log(f'END {DATA_FILE.name:40} {size:8,} bytes = {size/1024:6,.1f} KB')

    def initBlank(self):
        self.tblankCol = self.tblank * self.tpc   ;   data = self.data    ;   dl = self.dl(data)
        for p in range(dl[0]):
            for l in range(dl[1]):
                for c in range(dl[2]):
                    for b in self.tblanks:
                        if b != self.tblank: data[p][l][c] = data[p][l][c].replace(b, self.tblank)
        self.log(f'tblank={self.tblank} blankCol={self.tblankCol}')

    def isVert(self, data=None, dbg=1):
        dl, dt = self.dl(data), self.dt(data)
        if dbg: self.log(f'BGN {FDT}={fmtl(dt)}')
        assert dt[0] is list and dt[1] is list and dt[2] is list and dt[3] is str
        self.checkData(data)
        vert = 1 if dl[-2] > dl[-1] else 0
        if dbg: self.log(f'END {FDL}={fmtl(dl)} vert={vert}')
        return vert

    def checkData(self, data=None):
        dl, dt = self.dl(data), self.dt(data)   ;   data = self.data if data is None else data
        for p in range(dl[0]):
            assert len(data[p]) == dl[1]
            for l in range(len(data[p])):
                assert len(data[p][l]) == dl[2]
                for c in range(len(data[p][l])):
                    assert len(data[p][l][c]) == dl[3]
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
#            if ll:  plt = f'{JTEXTS[P]} {p+1}'  ;  plab = f'{plt:{i+1}}'  ;  self.log(f'{Z*i}{plab}', pfx=0)
            for l in range(len(data[p])):
                if ll:  llt = f'{JTEXTS[P]} {p+1}'  ;  llab = f'{llt:{i+1}} '  ;  self.log(f'{Z*i}{llab}', pfx=0, end='')   ;   self.log(f'{JTEXTS[L]} {l+1}', pfx=0)
#                if ll:  llt = f'{JTEXTS[L]} {l+1}'  ;  llab = f'{llt:{i+1}}'  ;  self.log(f'{Z*i}{llab}', pfx=0)
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
        w = max(len(data[0][0][0]), len(JTEXTS[P]) + 2, len(JTEXTS[L]) + 2)   ;   txt = Z * i + JTEXTS[C] + Z if i >= 0 else JTEXTS[C]
        self.log(f'BGN {self.fmtDD(data)} lc={lc} ll={ll} i={i} w={w} txt={txt}')
        for p in range(len(data)):
            if ll: self.log(f'{JTEXTS[P]} {p+1}', pfx=0)  ;  self.log(f'{txt:{3}}', pfx=0, end='')  ;  txt2 = [ f'{JTEXTS[L]} {l+1}' for l in range(len(data[0])) ]  ;  self.log(f'{fmtl(txt2, w=w, d1="", d2="")}', pfx=0)
            for c in range(len(data[p][0])):
                pfx = f'{c+1:3} ' if i >= 0 and lc else ''   ;   self.log(f'{pfx}{Z*i}', pfx=0, end='')
                for l in range(len(data[p])):
                    self.log(f'{data[p][l][c]}', pfx=0, end=Z)
                self.log(pfx=0)
        self.log(f'END {self.fmtDD(data)} lc={lc} ll={ll} i={i}')
    ####################################################################################################################################################################################################
    def dumDataLabels(self, data=None, i=0, sep='%'):
        pp = '  '  ;  qq = ' @'   ;   zz = self.zz()
        p = pp[:] if zz > 1 else pp[:1] if zz else ''
        q = qq[:] if zz > 1 else qq[:1] if zz else ''
        if data is None: data = self.data
        n = len(data[0]) - zz   ;   a = ' ' * i if i else ''  ;  b = sep * n  ;  r = sep * 3
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
    def geom(self, p=None, j=0, init=0, nn=0, dbg=1):
        n, i, x, y, w, h, g = self.n[j], self.i[j], self.x[j], self.y[j], self.w[j], self.h[j], self.g[j]
        mx, my = -1, -1   ;   msg  =  ''  ;   iw, ih  =  w, h
        if   n == 0:            n  =  1   ;      msg  =  f'WARN j={j} setting n=0 -> n=1 -> n=0'
        if   nn:                n  =  nn
        if   j == C:            n +=  self.zz()
        if   p is None:         w  =  self.ww - 2*x           ;  h  =  self.hh  - 2*y
        elif j == C:            w  = (p.width - x*(n + 1))/n  ;  h  =  p.height - 2*y
        else:                   w  =  p.width - 2*x           ;  h  = (p.height - y*(n + 1))/n
        if SPRITES:
            if   p is None:     x  =  0                       ;  y  =  0
            elif j == S and nn: x  =  p.x                     ;  y  =  p.y + p.height - h/2
            elif j == C and nn: x  =  p.x + w/2               ;  y  =  p.y + p.height - h
            elif j == T:        x  =  p.x + w/2               ;  y  =  p.y + p.height - h/2
            else:               x  =  p.x                     ;  y  =  p.y + p.height - h
        else:
            if   p is None:     x  =  w/2                     ;  y  =  h/2
            elif j == C:        x  =  w/2                     ;  y  =  p.y
            elif j == T:        x  =  p.x                     ;  y  =  p.y + p.height/2 - h/2
            else:               x  =  w/2                     ;  y  =  p.y + p.height/2 - h/2
        if init:                self.w[j] = w                 ;  self.h[j] = h  # if not nn and init:
        elif iw and ih:         mx =  w/iw                    ;  my =  h/ih
        if   msg:               n = 0                         ;  self.log(msg, pfx=0)
        if   dbg: self._dumpGeom(j, n, i, x, y, w, h, mx, my, iw, ih, nn, p)
        return n, i, x, y, w, h, g, mx, my
    ####################################################################################################################################################################################################
    def _dumpGeom(self, j, n, i, x, y, w, h, mx, my, iw, ih, nn, p):
        px, py, pw, ph = None, None, None, None   ;   file = sys.stdout # if 0 else None
        if p: px, py, pw, ph = p.x, p.y, p.width, p.height
        if p: self.log(FMTR.format(f'  {j}  {n:3} {i:4}   {x:7.2f} {y:7.2f} {w:7.2f} {h:7.2f} {mx:6.3f} {my:6.3f}  {iw:7.2f} {ih:7.2f} {nn:3} {JTEXTS[j]:6} {px:7.2f} {py:7.2f} {pw:7.2f} {ph:7.2f}'), pfx=0, file=file)
        else: self.log(FMTR.format(f'  {j}  {n:3} {i:4}   {x:7.2f} {y:7.2f} {w:7.2f} {h:7.2f} {mx:6.3f} {my:6.3f}  {iw:7.2f} {ih:7.2f} {nn:3} {JTEXTS[j]:6}'), pfx=0, file=file)
#        self.log(f'  {j}  {n:3} {i:4}   {x:7.2f} {y:7.2f} {w:7.2f} {h:7.2f} {mx:6.3f} {my:6.3f}  {iw:7.2f} {ih:7.2f} {nn:3} {JTEXTS[j]} {px:7.2f} {py:7.2f} {pw:7.2f} {ph:7.2f}', pfx=0, file=sys.stdout)
    ####################################################################################################################################################################################################
    def z1(self): return self.ZZ[0] and   self.J1[C] == C1
    def z2(self): return self.ZZ[1] and ((self.J1[C] == C1 and not self.ZZ[0]) or (self.J1[C] == C2 and self.ZZ[0]))
    ####################################################################################################################################################################################################
    def hideLabel(self, p, j, t='', dbg=1):
        c = p[j]    ;    ha = hasattr(c, 'text')
        x, y, w, h = c.x, c.y, c.width, c.height
        text = c.text if ha else ''
        if   type(c) == pyglet.sprite.Sprite: c.update(x=0, y=0, scale_x=0, scale_y=0)
        elif type(c) == pyglet.text.Label:    c.x, c.y, c.width, c.height = 0, 0, 0, 0
        if dbg: self.log(f'{t:5} {j+1:3} {hex(id(c))} {text:6} {x:7.2f} {y:7.2f} {w:7.2f} {h:7.2f} {c.x:7.2f} {c.y:7.2f} {c.width:7.2f} {c.height:7.2f}', pfx=0)
    ####################################################################################################################################################################################################
    def toggleTnik(self, tnik, why=''):
        self.dumpGeom('BFR', why)
        self.TNIK[tnik] = int(not self.TNIK[tnik])   ;    self.n[S] = self.ss()
        self.dumpGeom('AFT', why)

    def toggleQQ(self, why=''):
        self.dumpGeom('BFR', why)
        global QQ  ;  QQ = int(not QQ)
        self.dumpGeom('AFT', why)

    def toggleZZ(self, zz, why=''):
        self.dumpGeom('BFR', why)
        self.ZZ[zz] = int(not self.ZZ[zz])
        self.dumpGeom('AFT', why)
    ####################################################################################################################################################################################################
    def toggleLLRows(self, how, dbg=0):
        self.toggleQQ()
        msg2 = f'{how} QQ={QQ}'
        self.dumpGeom('BGN', f'    {msg2}')
        if dbg: self.log(f'    llText={fmtl(self.llText[self.zz()])}')
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
            self.hideLabel(self.lrows, rr, JTEXTS[LLR])
            for cc in range(nc):
                self.hideLabel(self.lcols, cc + rr * nc, JTEXTS[LLC])
        if SNAP and dbg: self.snapshot(f'hideLLRows() {fmtl(self.TNIK)} {msg}')
        self.dumpGeom('END', msg)
    ####################################################################################################################################################################################################
#        nt = self.n[T]   ;   ntl = nt * j1l  #        nl, il, xl, yl, wl, hl, gl, mx, my = self.geom(p=p, j=L)
#        if   type(p) is pyglet.text.Label:    p.y -= hl/2   ;   p.height *= ntl / (ntl + 1) / j1l   ;   self.log(f'ntl={ntl:2} jil={j1l} p.y = {p.y:7.2f} p.h = {p.height:7.2f}', pfx=0)
#        elif type(p) is pyglet.sprite.Sprite: my = (p.height - hl)/self.h[L]   ;   p.scale_y = my   ;   self.log(f'ntl={ntl:2} h[L]={self.h[L]} my={my:7.5f} p.y={p.y:7.2f} p.h={p.height:7.2f}', pfx=0)
#        p = self.createTnik(self.lines, L, xl, yl, wl, hl, gl, klk, kl=kll, why='new ', dbg=dbg)
#            self.createTnik(f'{Z*(c+1)}{sc}' if self.DF[LLC] and not c else text[c], LLC, self.lcols, xc + c*wc, yc, wc, hc, gc, kkc, kl=klc, why=f'new LC {sc}', dbg=dbg)
#            if not self.zz() and c == 0:  self.hideLabel(self.lcols, sc-1, f'Hide LLC {sc}')  #            if self.zz() == 1 and c == 1: self.hideLabel(self.lcols, sc-1, f'Hide LLC {sc}')
#        if   type(p) is pyglet.text.Label:    p.y -= hr/2   ;   p.height *= ntl / (ntl + 1) / j1l   ;   self.log(f'ntl={ntl:2} p.y = {p.y:7.2f} p.h = {p.height:7.2f}', pfx=0)
#        elif type(p) is pyglet.sprite.Sprite: my = (p.height - hr)/self.h[L]   ;   p.scale_y = my   ;   self.log(f'ntl={ntl:2} h[L]={self.h[L]} my={my:7.5f} p.y={p.y:7.2f} p.h={p.height:7.2f}', pfx=0)
    def createLLRow(self, p, pi, dbg=1, dbg2=0, dbg3=0):
        klr = self.klr  ;  klc = self.klc  ;  kkr = self.cci(pi, klr) #        kll = self.kl   ;   klk = self.cci(pi, kll)
        nn1 = 1 + self.n[T] * self.ss() * self.i[L]
        nr, ir, xr, yr, wr, hr, gr, mx, my = self.geom(p=p, j=S, nn=nn1, dbg=dbg2)
        if SPRITES: yr += hr/2
        self.J1[LLR] = pi   ;   nn2 = self.n[C]
        row = self.createTnik(self.lrows, pi, LLR, xr, yr, wr, hr, gr, kkr, kl=klr, dbg=dbg)
        nc, ic, xc, yc, wc, hc, gc, mx, my = self.geom(p=row, j=C, nn=nn2, dbg=dbg2)   ;  sc = nc * pi
        if SPRITES: xc += wc/2
        for c in range(nc):
            kkc = self.cci(pi, klc)
            sc += 1   ;   self.J1[LLC] = c
            text = self.llText[self.zz()]
            txt = text[c] if text and len(text) >= c else ''
            self.createTnik(self.lcols, c, LLC, xc + c*wc, yc, wc, hc, gc, kkc, kl=klc, t=txt, dbg=dbg)
        if dbg3: self.log(f'pi={pi:3} px={p.x:7.2f} py={p.y:7.2f} pw={p.width:7.2f} ph={p.height:7.2f} nn1={nn1} nn2={nn2}', pfx=0)
        if dbg3: self.log(f'nr={nr:3} xr={xr:7.2f} yr={yr:7.2f} wr={wr:7.2f} hr={hr:7.2f} row.y={row.y:7.2f} row.h={row.height:7.2f}', pfx=0)
        if dbg3: self.log(f'nc={nc:3} xc={xc:7.2f} yc={yc:7.2f} wc={wc:7.2f} hc={hc:7.2f} sc={sc}', pfx=0)
        if   type(p) is pyglet.text.Label:    p.y, p.height = self.squeeze(p.y, p.height, 1 + self.n[T]*self.ss()*self.i[L])   ;   self.log(f'nn1={nn1:2} nn2={nn2:2} p.y = {p.y:7.2f} p.h = {p.height:7.2f}', pfx=0) if dbg3 else None
        elif type(p) is pyglet.sprite.Sprite: my = (p.height - hr)/self.h[L]   ;   p.scale_y = my    ;   self.log(f'nn1={nn1:2} nn2={nn2:2} h[L]={self.h[L]} my={my:7.5f} p.y={p.y:7.2f} p.h={p.height:7.2f}', pfx=0) if dbg3 else None
        return p

    def resizeLLRow(self, p, pi, dbg=1, dbg2=0, dbg3=0):
        nn1 = 1 + self.n[T] * self.ss() * self.i[L]
        nr, ir, xr, yr, wr, hr, gr, mxr, myr = self.geom(p=p, j=S, nn=nn1, dbg=dbg2)
        if SPRITES:yr += hr/2
        self.J1[LLR] = 0   ;   self.J2[LLR] += 1   ;   nn2 = self.n[C]
        row = self.lrows[pi]    ;    row.width = wr  ;   row.height = hr  ;   row.x = xr  ;   row.y = yr
        if dbg: self.dumpTnik(row, *self.cnts(), why=f'mod LLR {pi+1}')
        nc, ic, xc, yc, wc, hc, gc, mxc, myc = self.geom(p=row, j=C, nn=nn2, dbg=dbg2)   ;   sc = nc * pi
        if SPRITES: xc += wc/2
        for c in range(nc):
            self.J1[LLC] = c   ;   self.J2[LLC] += 1   ;   zz = self.zz()   ;   lcs = self.lcols   ;   lc = len(lcs)   ;   klc = self.klc   ;   kk = self.cci(sc, klc)
            if sc >= lc: self.createTnik(lcs, sc, LLC, 0, 0, 0, 0, self.g[C], kk, klc)  ;  msg = f'ERROR Missing zz={zz} row={pi+1} c={c} sc={sc} lc={lc}'  ;  self.log(msg) # ;  self.quit(msg)
            col = self.lcols[sc]
            col.text = self.llText[zz][c]        ;   sc += 1
            col.width = wc   ;   col.height = hc  ;   col.x = xc + c * wc  ;  col.y = yc
            if dbg: self.dumpTnik(col, *self.cnts(), why=f'mod {JTEXTS[LLC]} {sc}')
        if dbg3: self.log(f'pi={pi:3} px={p.x:7.2f} py={p.y:7.2f} pw={p.width:7.2f} ph={p.height:7.2f} nn1={nn1} nn2={nn2}', pfx=0)
        if dbg3: self.log(f'nr={nr:3} xr={xr:7.2f} yr={yr:7.2f} wr={wr:7.2f} hr={hr:7.2f} row.y={row.y:7.2f} row.h={row.height:7.2f}', pfx=0)
        if dbg3: self.log(f'nc={nc:3} xc={xc:7.2f} yc={yc:7.2f} wc={wc:7.2f} hc={hc:7.2f} sc={sc}', pfx=0)
        if   type(p) is pyglet.text.Label:    p.y, p.height = self.squeeze(p.y, p.height, 1 + self.n[T]*self.ss()*self.i[L])   ;   self.log(f'nn1={nn1:2} nn2={nn2:2} p.y = {p.y:7.2f} p.h = {p.height:7.2f}', pfx=0) if dbg3 else None
        elif type(p) is pyglet.sprite.Sprite: my = (p.height - hr)/self.h[L]   ;   p.scale_y = my   ;      self.log(f'nn1={nn1:2} nn2={nn2} h[L]={self.h[L]} my={my:7.5f} p.y={p.y:7.2f} p.h={p.height:7.2f}', pfx=0) if dbg3 else None
        return p
#        if   type(p) is pyglet.text.Label:    p.y -= hr/2   ;   p.height *= ntl / (ntl + 1) / j1l   ;   self.log(f'ntl={ntl:2} p.y = {p.y:7.2f} p.h = {p.height:7.2f}', pfx=0)
#        elif type(p) is pyglet.sprite.Sprite: my = (p.height - hr)/self.h[L]   ;   p.scale_y = my   ;   self.log(f'ntl={ntl:2} h[L]={self.h[L]} my={my:7.5f} p.y={p.y:7.2f} p.h={p.height:7.2f}', pfx=0)
#        if dbg2: self.log(f'p.y -= hr/2 = {p.y:7.2f}, p.height -= h = {p.height:7.2f}  w={fmtl(self.w)} h={fmtl(self.h)}', pfx=0)
    def squeeze(self, y, h, a):  self.log(f'y={y:6.2f} h={h:6.2f} a={a}', end=' ')  ;  b = h/a  ;  h -= b  ;  y -= b/2  ;  self.log(f' b={b:6.2f} y={y:6.2f} h={h:6.2f}', pfx=0)  ;  return y, h
    ####################################################################################################################################################################################################
    def toggleLRows(self, how, dbg=0):
        self.toggleQQ()
        msg2 = f'{how} QQ={QQ}'
        self.dumpGeom('BGN', f'     {msg2}')
        if dbg: self.log(f'    llText={fmtl(self.llText[self.zz()])}')
        if QQ and not self.lrows: msg = 'SHOW'   ;   self.showLRows(how)
        else:                     msg = 'HIDE'   ;   self.hideLRows(how)
        self.on_resize(self.ww, self.hh, dbg=1)
        self.dumpGeom('END', f'{msg} {msg2}')

    def showLRows(self, how):
        msg = f'SHOW {how}'
        self.dumpGeom('BGN', msg)
        for l, line in enumerate(self.lines):
            self.J1[L] = l
            self.dumpTnik(line, *self.cnts(), why=f'ref {JTEXTS[L]} {1 + self.J1[L]}')
            self.createLLRow(line, l)
        self.dumpGeom('END', msg)

    def createLRow(self, p, pi, dbg=1, dbg2=0):
        klr = self.klr  ;  klc = self.klc  ;  kkr = self.cci(pi, klr)
        nn1 = 1 + self.n[T] * self.ss() * self.i[L]   ;   nn2 = self.n[C]
        nr, ir, xr, yr, wr, hr, gr, mx, my = self.geom(  p, S, init=1, nn=nn1, dbg=dbg2)
        row = self.createTnik(self.lrows, pi, LLR, xr, yr, wr, hr, gr, kkr, kl=klr, dbg=dbg)
        nc, ic, xc, yc, wc, hc, gc, mx, my = self.geom(row, C, init=1, nn=nn2, dbg=dbg2)   ;  sc = nc * pi
        for c in range(nc):
            kkc  = self.cci(pi, klc)   ;   sc += 1
            text = self.llText[self.zz()]
            txt  = text[c] if text and len(text) >= c else ''
            self.createTnik(self.lcols, c, LLC, xc+c*wc, yc, wc, hc, gc, kkc, kl=klc, t=txt, dbg=dbg)
        if   type(p) is pyglet.text.Label:    p.y, p.height = self.squeeze(p.y, p.height, 1 + self.n[T]*self.ss()*self.i[L])   ;   self.log(f'nn1={nn1:2} nn2={nn2:2} p.y = {p.y:7.2f} p.h = {p.height:7.2f}') if dbg else None
        elif type(p) is pyglet.sprite.Sprite: my = (p.height - hr)/self.h[L]   ;   p.scale_y = my    ;   self.log(f'nn1={nn1:2} nn2={nn2:2} h[L]={self.h[L]} my={my:7.5f} p.y={p.y:7.2f} p.h={p.height:7.2f}') if dbg else None
        return p

    def resizeLRow(self, p, pi, dbg=1):
        nn1 = 1 + self.n[T] * self.ss() * self.i[L]   ;   nn2 = self.n[C]
        nr, ir, xr, yr, wr, hr, gr, mxr, myr = self.geom(   p, S, nn=nn1, dbg=dbg)
        lrow = self.resizeTnik(self.lrows, pi, LLR, xr, yr, wr, hr, mxr, myr)
        nc, ic, xc, yc, wc, hc, gc, mxc, myc = self.geom(lrow, C, nn=nn2, dbg=dbg)   ;   sc = nc * pi
        for c in range(nc):
            zz = self.zz()  ;  lcs = self.lcols  ;   lc = len(lcs)       ;  klc = self.klc     ;  kk = self.cci(sc, klc)
            if sc >= lc: self.createTnik(lcs, sc, LLC, 0, 0, 0, 0, self.g[C], kk, klc)  ;  msg = f'ERROR Missing zz={zz} row={pi+1} c={c} sc={sc} lc={lc}'  ;  self.log(msg)  ;  self.quit(msg)
            self.resizeTnik(lcs, c, LLC, xc+c*wc, yc, wc, hc, mxc, myc)
        if   type(p) is pyglet.text.Label:    p.y, p.height = self.squeeze(p.y, p.height, 1 + self.n[T]*self.ss()*self.i[L])   ;   self.log(f'nn1={nn1:2} nn2={nn2:2} p.y = {p.y:7.2f} p.h = {p.height:7.2f}', pfx=0) if dbg else None
        elif type(p) is pyglet.sprite.Sprite: my = (p.height - hr)/self.h[L]   ;   p.scale_y = my   ;      self.log(f'nn1={nn1:2} nn2={nn2} h[L]={self.h[L]} my={my:7.5f} p.y={p.y:7.2f} p.h={p.height:7.2f}', pfx=0) if dbg else None
        return p

    def hideLRows(self, how):
        msg = f'HIDE {how}'
        self.dumpGeom('BGN', msg)
        nr = len(self.lrows)    ;  nc = len(self.lcols)   ;   assert not nc % nr
        nc = nc // nr  #  normalize
        for rr in range(nr):
            self.hideLabel(self.lrows, rr, JTEXTS[LLR])
            for cc in range(nc):
                self.hideLabel(self.lcols, cc + rr * nc, JTEXTS[LLC])
        self.dumpGeom('END', msg)
    ####################################################################################################################################################################################################
    def toggleLCols(self, how, zz):
        ii = 0 if not zz else 2
        msg2 = f'{how} zz={zz}'
        self.dumpGeom('BGN', f'     {msg2}')
        if   not self.ZZ[zz] and not self.C[ii]: msg = 'SHOW'   ;   self.showLCols(how, zz)
        elif     self.ZZ[zz]:                    msg = 'HIDE'   ;   self.hideLCols(how, zz)
        else:                                    msg = 'SKIP'   ;   self.dumpGeom('   ', f'{msg} {msg2}')   ;   self.toggleZZ(zz)
        self.on_resize(self.ww, self.hh, dbg=1)
        self.dumpGeom('END', f'{msg} {msg2}')

    def showLCols(self, how, zz):
        self.J1[L], self.J2[L] = 0, 0
        msg = f'SHOW {how} zz={zz}'
        self.dumpGeom('BGN', msg)
        if 0 not in self.ZZ: msg = f'ERROR ZZ={fmtl(self.ZZ)} is already full'   ;   self.log(msg)   ;   self.quit(msg)
        self.log(f'zz={zz} {fmtl(self.ZZ)}')
        self.toggleZZ(zz)
        self.initJ(msg)
        for l, line in       enumerate(self.lines):
            self.J1[L] = l
            self.dumpTnik(self.lines[l], *self.cnts(), why=f'ref {JTEXTS[L]} {1 + self.J1[L]}')
            for s, sect in   enumerate(self.lenB()):
                if sect:
                    self.J1[S] = s
                    self.dumpTnik(self.sects[s], *self.cnts(), why=f'ref {JTEXTS[S]} {1 + self.J1[S]}')
                    for col in   self.g_createTniksB2(self.sects[s], C, self.cols, init=1, nn=0):
                        for _ in self.g_createTniksC(col):
                            pass
        self.dumpJ(msg)
        self.dumpGeom('END', msg)

    def hideLCols(self, how, zz, dbg=1):
        msg = f'HIDE {how} zz={zz}'
        self.dumpGeom('BGN', msg)
        np, nl, ns, nc, nt = self.n
        for l in range(nl):
            for s, sect in   enumerate(self.TNIK):
                if sect:
                    for c, col in enumerate(self.ZZ):
                        if c == zz: self.hideLabel(self.cols, nc * s + c, 'Col', dbg=dbg)
        for t in range(nt):
            self.hideLabel(self.C[zz], nt, JTEXTS[zz + K - 1], dbg=dbg)
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
        msg = f'SHOW {how} tnik={tnik}'   ;   nl = self.n[L]   ;   init = 0
        self.dumpGeom('BGN', msg)
        if 0 not in self.TNIK: msg = f'ERROR TNIK={fmtl(self.TNIK)} is already full'   ;   self.log(msg)   ;   self.quit(msg)
        self.log(f'tnik={tnik} {fmtl(self.TNIK)}')
        self.toggleTnik(tnik)
        self.initJ(msg)
        for p, page in            enumerate(self.pages):
            self.setJs(P, p)            ;   self.dumpTnik(self.pages[p], *self.cnts(), why=f' ref Page {1 + self.J1[P]:3}')
            for l, line in        enumerate(self.lines[p*nl:p*nl+nl]):
                self.setJs(L, l)        ;   self.dumpTnik(self.lines[p*nl+l], *self.cnts(), why=f' ref Line {1 + self.J1[L]:3}')
                if not line.height: msg = f'WARN Line l={l} height is zero'   ;   self.log(msg)   ;   continue
                for s, sect in    enumerate(self.g_createTniksB1(line, S, self.sects, init=init, tnik=tnik)):
                    for col in              self.g_createTniksA( sect, C, self.cols,  init=init):
                        for _ in            self.g_createTniksC( col, init=init):
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
    def addPage(self, how):
        self.log(f'BGN {how}', pos=1)
        np, nl, ns, nc, nr = self.n  ;  nc += self.zz()
        self.n[P] += 1
        self.log(f'n={fmtl(self.n)}')
        data = [ [ self.tblankRow for _ in range(nr)] for _ in range(nl) ]
        self.data = self.transposeData()
        self.data.append(data)
        self.dumpDataVert() if self.isVert() else self.dumpDataHorz()
        self.data = self.transposeData()
        self.dumpDataVert() if self.isVert() else self.dumpDataHorz()
        n, ii, x, y, w, h, g, mx, my = self.geom(None, P, init=0, nn=1)   ;   kl = self.k[P]
        self.dumpTnik()
        page = self.createTnik(self.pages, len(self.pages), P, x, y, w, h, g, self.cci(0, kl), kl=kl, dbg=1)
        for line in            self.g_createTniksA( page,   L, self.lines, init=0, dbg2=0):
            for sect in        self.g_createTniksB( line,   S, self.sects):
                for col in     self.g_createTniksA( sect,   C, self.cols):
                    for _ in   self.g_createTniksC( col):
                        pass
        self.dumpTnik()
        self.log(f'END {how}', pos=1)
    ####################################################################################################################################################################################################
    def createTniks(self):
        self.dumpGeom('BGN')
        self.dumpTnik()
        for page in              self.g_createTniksA(None, P, self.pages):
            for line in          self.g_createTniksA(page, L, self.lines):
                for sect in      self.g_createTniksB(line, S, self.sects):
                    for col in   self.g_createTniksA(sect, C, self.cols):
                        for _ in self.g_createTniksC(col):
                            pass
        self.dumpTnik()
        self.dumpGeom('END')
    ####################################################################################################################################################################################################
    def g_createTniksA(self, p, j, plist, init=1, nn=0, dbg=1, dbg2=1):
        n, ii, x, y, w, h, g, mx, my = self.geom(p, j, init=init, nn=nn, dbg=dbg2)   ;   kl = self.k[j]   ;  x2 = x   ;   y2 = y
        for i in range(n):  #            if nn and j != L:    self.J2[j] = self.lenE()[j]
            if   j == C:         x2 = x + i * w
            elif p:              y2 = y - i * h
            yield self.createTnik(plist, i, j, x2, y2, w, h, g, self.cci(i, kl), kl=kl, dbg=dbg)

    def g_createTniksB(self, p, j, plist, init=1, nn=0, dbg=1, dbg2=1):
        n, ii, x, y, w, h, g, mx, my = self.geom(p, j, init=init, nn=nn, dbg=dbg2)   ;   kl = self.k[j]  ;   i2 = 0   ;   ns = self.n[S]
        for i, tnik in enumerate(self.TNIK):
            if tnik:
                y2 = y - i2 * h   ;   i2 += 1
                self.log(f'i={i} y2={y2: 6.1f} y={y} h={h} n={n} ns={ns} ss0={self.ss0} ss={self.ss()} init={init} nn={nn} i2={i2} tnik={tnik} p.y={p.y} {p.height}')
                yield self.createTnik(plist, i, j, x, y2, w, h, g, self.cci(j, kl), kl=kl, dbg=dbg)

    def g_createTniksB1(self, p, j, plist, init=1, tnik=0, dbg=1, dbg2=1):
        n, ii, x, y, w, h, g, mx, my = self.geom(p, j, init=init, nn=0, dbg=dbg2)   ;   kl = self.k[j]   ;   ns = self.n[S]
        y2 = y - h
        self.log(          f'    y2={y2: 6.1f} y={y} h={h} n={n} ns={ns} ss0={self.ss0} ss={self.ss()} init={init}           tnik={tnik} p.y={p.y} {p.height}')
        yield self.createTnik(plist, tnik, j, x, y2, w, h, g, self.cci(j, kl), kl=kl, dbg=dbg)

    def g_createTniksB2(self, p, j, plist, init=1, nn=0, dbg=1, dbg2=1, dbg3=1):
        n, ii, x, y, w, h, g, mx, my = self.geom(p, j, init=init, nn=nn, dbg=dbg2)   ;   kl = self.k[j]   ;  x2 = x   ;   k = 0   ;   tpc = self.tpc
        for i, z in enumerate(self.ZZ):
            n  = self.lenC()
            l  =  self.n[L]   ;   s = self.n[S]
            m = l * tpc * s
            if   not z:          self.log(f'i={i} z={z} continue k={k} n={fmtl(n)} l={l} tpc={tpc} s={s} m={m}') if dbg3 else None   ;   continue
            if (k and n[2] < m) or (not k and (n[0] + n[1] <= m)):
                y2 = y - k * h
                if dbg3:         self.log(f'i={i} z={z} create   k={k} n={fmtl(n)} l={l} tpc={tpc} s={s} m={m}')
                yield self.createTnik(plist, k, j, x2, y2, w, h, g, self.cci(j, kl), kl=kl, dbg=dbg)
            elif dbg3:           self.log(f'i={i} z={z} already  k={k} n={fmtl(n)} l={l} tpc={tpc} s={s} m={m}')
            k += 1
    ####################################################################################################################################################################################################
    def g_createTniksC(self, col, init=1, dbg=1, dbg2=0):
        p, l, s, c = self.J1[P], self.J1[L], self.J1[S], self.J1[C]    ;   i2 = 0
        kt, kn, ki, kkk = self.kt, self.kn, self.ki, self.kk           ;   kt2, kn2, ki2, kk2 = self.kt2, self.kn2, self.ki2, self.kk2
        n, ii, x, y, w, h, g, mx, my = self.geom(p=col, j=T, init=init, dbg=dbg2)   ;   zz = self.zz()
        imap = self.getImap(p, l, c-zz) if not self.z1() and not self.z2() else []
        for i in range(n):
            if   s == TT:
                if   self.z1():   tab = self.stringNumbs[i]  ;  plist = self.snos   ;  kl = kt2  ;  k = self.cci(i, kl)  ;  j = O
                elif self.z2():   tab = self.stringCapo[i]   ;  plist = self.capos  ;  kl = kt2  ;  k = self.cci(i, kl)  ;  j = D
                else:       tab = self.data[p][l][c-zz][i]   ;  plist = self.tabs   ;  kl = kt   ;  k = self.cci(i, kl)  ;  j = T
                yield self.createTnik(plist, i, j, x, y-i*h, w, h, g, k, kl=kl, t=tab, dbg=dbg)
            elif s == NN:
                if    self.z1(): note = self.stringNames[i]  ;  plist = self.snas   ;  kl = kn2  ;  k = self.cci(i, kl)  ;  j = A
                elif  self.z2(): note = self.stringCapo[i]   ;  plist = self.capos  ;  kl = kn2  ;  k = self.cci(i, kl)  ;  j = D
                else:       tab = self.data[p][l][c-zz][i]   ;  plist = self.notes  ;  kl = kn   ;  k = self.cci(i, kl)  ;  j = N  ;  note = self.tab2nn(tab, i) if self.isFret(tab) else self.tblank
                yield self.createTnik(plist, i, j, x, y-i*h, w, h, g, k, kl=kl, t=note, dbg=dbg)
            elif s == II:
                if   self.z1():  ikey = self.stringNumbs[i]  ;  plist = self.snos   ;  kl = ki2  ;  k = self.cci(i, kl)  ;  j = O
                elif self.z2():  ikey = self.stringCapo[i]   ;  plist = self.capos  ;  kl = ki2  ;  k = self.cci(i, kl)  ;  j = D
                else:
                    imap0 = imap[0][::-1] if imap and len(imap) else []
                    dd = self.data[p][l][c-zz]   ;     fdd = self.isFret(dd[i])   ;   j = I
                    if imap0 and len(imap0) > i2:     ikey = imap0[i2] if fdd else self.tblank    ;   i2 += 1 if fdd else 0
                    else:                             ikey = self.tblank
                    if dbg2: cc = self.plct2cc(p, l, c, 0)   ;   self.dumpDataSlice(p, l, c, cc)  ;  self.log(f'cc={cc} i={i} i2={i2} imap0={imap0} fdd={fdd} dd={dd} ikey={ikey}')
                    plist = self.ikeys  ;  kl = ki  ;  k = self.cci(i, kl)
                yield self.createTnik(plist, i, j, x, y-i*h, w, h, g, k, kl=kl, t=ikey, dbg=dbg)
            elif s == KK:
                if   self.z1(): chord = self.stringNames[i]  ;  plist = self.snas   ;  kl = kk2  ;  k = self.cci(i, kl)  ;  j = A
                elif self.z2(): chord = self.stringCapo[i]   ;  plist = self.capos  ;  kl = kk2  ;  k = self.cci(i, kl)  ;  j = D
                else:
                    chunks = imap[4]   if (imap and len(imap) > 4) else []
                    chord  = chunks[i] if len(chunks) > i else self.tblank   ;   j = K
                    plist  = self.chords  ;  kl = kkk  ;  k = self.cci(i, kl)
                yield self.createTnik(plist, i, j, x, y-i*h, w, h, g, k, kl=kl, t=chord, dbg=dbg)
            else: msg = f'ERROR: s={s} {fmtl(self.TNIK)}'   ;   self.log(msg)   ;   self.quit(msg)
    ####################################################################################################################################################################################################
    def createTnik(self, plist, i, j, x, y, w, h, g, kk, kl=None, why='', v=None, t='', ml=0, dbg=0):
        o, k, d, i2, n, s = self.fontParams()   ;   b = self.batch   ;   k2 = 0
        k = FONT_COLORS[(k + k2) % len(FONT_COLORS)] if kl is None else kl[kk]
        if v is None: v = 1 if j >= T and self.J2[P] == self.i[P] else 0
        if (SPRITES and j < T) or j < 0:
            scip = pyglet.image.SolidColorImagePattern(k)
            img  = scip.create_image(width=fri(w), height=fri(h))
            tnik = pyglet.sprite.Sprite(img, x, y, batch=b, group=g, subpixel=SUBPIX)
            tnik.color, tnik.opacity = k[:3], k[3]   ;   tnik.visible = v
        else:
            s *= v
            d, n = FONT_DPIS[d], FONT_NAMES[n]   ;   a, ax, ay = 'center', 'center', 'center' # left center right  # bottom baseline center top
            zz   = self.zz()                     ;          mp = len(plist) % (self.n[C] + zz) + 1 - zz if j == LLC else 0
            if j == LLC and not mp % 10:  k = self.kll[0]
            if ml:                        t = [ t[:i] + '\n' + t[i:] for i in range(len(t), 0, -1) ]
            tnik = pyglet.text.Label(t, font_name=n, font_size=s, bold=o, italic=i2, color=k, x=x, y=y, width=w, height=h, anchor_x=ax, anchor_y=ay, align=a, dpi=d, batch=b, group=g, multiline=ml)
        if j >= 0:                        self.J1[j] = i   ;   self.J2[j] += 1   ;   self.J1[-1] += 1   ;   self.J2[-1] += 1
        if not why:                       why = f'new  {JTEXTS[j]} {self.J2[j]:3}'
        if QQ and j == L:                 tnik = self.createLRow(tnik, i)
        self.tniks.append(tnik) if j >= 0 else None       ;   plist.append(tnik) if plist is not None else None
        if dbg:                           self.dumpTnik(tnik, *self.cnts(), why=why)
        return tnik
    ####################################################################################################################################################################################################
    def resizeTniks(self):
        self.dumpGeom('BGN')
        self.dumpTnik()
        for page in              self.g_resizeTniksA(None, P, self.pages):
            for line in          self.g_resizeTniksA(page, L, self.lines):
                for sect in      self.g_resizeTniksB(line, S, self.sects):
                    for col in   self.g_resizeTniksA(sect, C, self.cols):
                        for _ in self.g_resizeTniksC(col):
                            pass
        self.dumpTnik()
        self.dumpGeom('END')
    ####################################################################################################################################################################################################
    def g_resizeTniksA(self, p, j, plist, dbg=1, dbg2=1):
        n, ii, x, y, w, h, g, mx, my = self.geom(p, j, dbg=dbg2)   ;   x2 = x   ;   y2 = y
        if j == C and p is None:
            msg = f'WARN p is None j={j} '   ;   self.log(msg)   ;   yield None
        for i in range(n):
            if   j == C:          x2 = x + i * w
            elif p:               y2 = y - i * h
            tnik = self.resizeTnik(plist, i, j, x2, y2, w, h, mx, my, dbg=dbg)
            yield tnik

    def g_resizeTniksB(self, p, j, plist, dbg=1, dbg2=1):
        n, ii, x, y, w, h, g, mx, my = self.geom(p, j, dbg=dbg2)   ;   i2 = 0   ;   ns = self.n[S]
        for i, tnik in enumerate(self.TNIK):
            if tnik:
                y2 = y - i2 * h   ;   i2 += 1
                self.log(        f'i={i} y2={y2: 6.1f} y={y} h={h} n={n} ns={ns} ss0={self.ss0} ss={self.ss()}             i2={i2} tnik={tnik} p.y={p.y} {p.height}')
                yield self.resizeTnik(plist, i, j, x, y2, w, h, mx, my, dbg=dbg)
    ####################################################################################################################################################################################################
    def g_resizeTniksC(self, col, dbg=1, dbg2=0):
        p,     l,     s,     c       = self.J1[P], self.J1[L], self.J1[S], self.J1[C]   ;   plist = None   ;   j = -1
        n, ii, x, y, w, h, g, mx, my = self.geom(col, T, dbg=dbg2)
        for i in range(n):
            if   s == TT:  (j, plist) = (O, self.snos) if self.z1() else (D, self.capos) if self.z2() else T, self.tabs
            elif s == NN:  (j, plist) = (A, self.snas) if self.z1() else (D, self.capos) if self.z2() else N, self.notes
            elif s == II:  (j, plist) = (O, self.snos) if self.z1() else (D, self.capos) if self.z2() else I, self.ikeys
            elif s == KK:  (j, plist) = (A, self.snas) if self.z1() else (D, self.capos) if self.z2() else K, self.chords
            else:             msg = f'ERROR plist skipped n={n} i={i} j={j} plsc {p} {l} {s} {c} z1={self.z1()} z2={self.z2()}'   ;   self.dumpGeom()    ;   self.quit(msg)
            if plist is None: msg = f'ERROR plist is None n={n} i={i} j={j} plsc {p} {l} {s} {c} z1={self.z1()} z2={self.z2()}'   ;   self.dumpGeom()    ;   self.quit(msg)
            if not plist:     msg = f'ERROR not plist     n={n} i={i} j={j} plsc {p} {l} {s} {c} z1={self.z1()} z2={self.z2()}'   ;   self.dumpGeom()    ;   self.quit(msg)
            yield self.resizeTnik(plist, i, j, x, y-i*h, w, h, mx, my, dbg=dbg)
    ####################################################################################################################################################################################################
    def resizeTnik(self, plist, i, j, x, y, w, h, mx, my, why='', dbg=0):
        if  j  == S and not plist: msg = f'WARN Zero Sections empty plist'   ;   self.log(msg)   ;   return None
        tnik = plist[self.J2[j]] if j  >= 0 else self.cursor
        v = 1 if j >= T and self.J2[P] == self.i[P] else 0
        if j >= T: tnik.font_size = v * self.fs0 * h / self.h[T]
        if   type(tnik) is pyglet.sprite.Sprite: tnik.update(x=x, y=y, scale_x=mx, scale_y=my)
        elif type(tnik) is pyglet.text.Label:    tnik.x, tnik.y, tnik.width, tnik.height = x, y, w, h
        if QQ and j == L:  tnik = self.resizeLRow(tnik, i)
        if j >= 0:         self.J1[j] = i   ;    self.J2[j] += 1   ;      self.J1[-1] += 1      ;    self.J2[-1] += 1
        if not why:        why = f' upd {JTEXTS[j]} {self.J2[j]:3}'
        if dbg:            self.dumpTnik(tnik, *self.cnts(), why=why)
        return tnik
    ####################################################################################################################################################################################################
    def _dumpTniks(self, why=''):
        self.initJ(why)
        np, nl, ns, nc, nt = self.n  ;  nc += self.zz()
        i, sp, sl, ss, sc, st, sn, si, sk = 0, 0, 0, 0, 0, 0, 0, 0, 0   ;   qr, qc = 0, 0
        self.dumpGeom('BGN', f'{why}')
        self.dumpTnik()
        for p in range(np):
            sp += 1                                 ;  self.J1[P]   = sp  ;  self.J2[P]   += 1  ;  self.dumpTnik(self.tniks[i], *self.cnts(), why=f'{why} Page {sp}')  ;  i += 1
            for l in range(nl):
                sl += 1                             ;  self.J1[L]   = sl  ;  self.J2[L]   += 1  ;  self.dumpTnik(self.tniks[i], *self.cnts(), why=f'{why} Line {sl}')  ;  i += 1
                for q in range(QQ):
                    qr += 1                         ;  self.J1[LLR] = qr  ;  self.J2[LLR] += 1  ;  self.dumpTnik(self.tniks[i], *self.cnts(), why=f'{why} LLR {qr}')   ;  i += 1
                    for c in range(nc):
                        qc += 1                     ;  self.J1[LLC] = qc  ;  self.J2[LLC] += 1  ;  self.dumpTnik(self.tniks[i], *self.cnts(), why=f'{why} LLC {qc}')   ;  i += 1
                for s in range(ns):
                    ss += 1                         ;  self.J1[S]   = ss  ;  self.J2[S]   += 1  ;  self.dumpTnik(self.tniks[i], *self.cnts(), why=f'{why} Sect {ss}')  ;  i += 1
                    for c in range(nc):
                        sc += 1                     ;  self.J1[C]   = sc  ;  self.J2[C]   += 1  ;  self.dumpTnik(self.tniks[i], *self.cnts(), why=f'{why} Col {sc}')   ;  i += 1
                        for t in range(nt):
                            if   s == TT:  st += 1  ;  self.J1[T]   = st  ;  self.J2[T]   += 1  ;  self.dumpTnik(self.tniks[i], *self.cnts(), why=f'{why} Tab {st}')   ;  i += 1
                            elif s == NN:  sn += 1  ;  self.J1[N]   = sn  ;  self.J2[N]   += 1  ;  self.dumpTnik(self.tniks[i], *self.cnts(), why=f'{why} Note {sn}')  ;  i += 1
                            elif s == II:  si += 1  ;  self.J1[I]   = si  ;  self.J2[I]   += 1  ;  self.dumpTnik(self.tniks[i], *self.cnts(), why=f'{why} IKey {si}')  ;  i += 1
                            elif s == KK:  sk += 1  ;  self.J1[K]   = sk  ;  self.J2[K]   += 1  ;  self.dumpTnik(self.tniks[i], *self.cnts(), why=f'{why} Chord {sk}') ;  i += 1
                            else: self.log(f'ERROR {i} {fmtl(self.n)} {fmtl(self.TNIK)} {p}/{np} {l}/{nl} {s}/{ns} {c}/{nc} {t}/{nt} {fmtl(self.lenE())}')
        self.dumpTnik()   ;   self.dumpJ(why)
        self.dumpGeom('END', why)
        self.log(f'END plsct {np} {nl} {ns} {nc} {nt}')

    def _dumpSprites(self, why=''):
        self.initJ(why)
        self.dumpGeom('BGN', why)
        np, nl, ns, nc, nt = self.n    ;    i, sp, sl, ss, sc = 0, 0, 0, 0, 0
        self.log(f'BGN plsct {np} {nl} {ns} {nc} {nt}')
        self.dumpTnik()
        for p in range(np):
            sp += 1                   ;   self.J1[P] = sp  ;  self.J2[P] += 1  ;  self.dumpTnik(self.tniks[i], *self.cnts(), why=f'{why} Page {sp}') ; i += 1
            for l in range(nl):
                sl += 1               ;   self.J1[L] = sl  ;  self.J2[L] += 1  ;  self.dumpTnik(self.tniks[i], *self.cnts(), why=f'{why} Line {sl}') ; i += 1
                for s in range(ns):
                    ss += 1           ;   self.J1[S] = ss  ;  self.J2[S] += 1  ;  self.dumpTnik(self.tniks[i], *self.cnts(), why=f'{why} Sect {ss}') ; i += 1
                    for c in range(nc):
                        sc += 1       ;   self.J1[C] = sc  ;  self.J2[C] += 1  ;  self.dumpTnik(self.tniks[i], *self.cnts(), why=f'{why} Col {sc}')  ; i += 1
        self.dumpTnik()             ;   self.dumpJ(why)
        self.log(f'END plsct {np} {nl} {ns} {nc} {nt}')
        self.dumpGeom('END', why)

    def _dumpLabels(self, why='', dbg=0):
        self.initJ(why)
        np, nl, ns, nc, nt = self.n  ;  nc += self.zz()
        i, sp, sl, ss, sc, st, sn, si, sk = 0, 0, 0, 0, 0, 0, 0, 0, 0   ;   qr, qc = 0, 0
        self.dumpGeom('BGN', f'{why}')
        self.dumpTnik()
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
                                if   s == 0:  st += 1  ;  self.J1[T] = st  ;  self.J2[T] += 1  ;  self.dumpTnik(self.tniks[i], *self.cnts(), why=f'{why} Tab {st}')    ;  i += 1
                                elif s == 1:  sn += 1  ;  self.J1[N] = sn  ;  self.J2[N] += 1  ;  self.dumpTnik(self.tniks[i], *self.cnts(), why=f'{why} Note {sn}')   ;  i += 1
                                elif s == 2:  si += 1  ;  self.J1[I] = si  ;  self.J2[I] += 1  ;  self.dumpTnik(self.tniks[i], *self.cnts(), why=f'{why} IKey {si}')   ;  i += 1
                                elif s == 3:  sk += 1  ;  self.J1[K] = sk  ;  self.J2[K] += 1  ;  self.dumpTnik(self.tniks[i], *self.cnts(), why=f'{why} Chord {sk}')  ;  i += 1
        else:
            for p in range(np):
                sp += 1                                ;   self.J1[P] = sp  ;  self.J2[P] += 1  ;  self.dumpTnik(self.tniks[i], *self.cnts(), why=f'{why} Page {sp}')   ;  i += 1
                for l in range(nl):
                    sl += 1                            ;   self.J1[L] = sl  ;  self.J2[L] += 1  ;  self.dumpTnik(self.tniks[i], *self.cnts(), why=f'{why} Line {sl}')   ;  i += 1
                    for q in range(QQ):
                        qr += 1                        ;  self.J1[LLR] = qr ;  self.J2[LLR] += 1 ;  self.dumpTnik(self.tniks[i], *self.cnts(), why=f'{why} LLR {qr}')   ;  i += 1
                        for c in range(nc):
                            qc += 1                    ; self.J1[LLC] = qc  ;  self.J2[LLC] += 1 ;  self.dumpTnik(self.tniks[i], *self.cnts(), why=f'{why} LLC {qc}')   ;  i += 1
                    for s in range(ns):
                        ss += 1                        ;   self.J1[S] = ss  ;  self.J2[S] += 1  ;  self.dumpTnik(self.tniks[i], *self.cnts(), why=f'{why} Sect {ss}')   ;  i += 1
                        for c in range(nc):
                            sc += 1                    ;   self.J1[C] = sc  ;  self.J2[C] += 1  ;  self.dumpTnik(self.tniks[i], *self.cnts(), why=f'{why} Col {sc}')    ;  i += 1
                            for t in range(nt):
                                if   s == TT:  st += 1  ;   self.J1[T] = st  ;  self.J2[T] += 1  ;  self.dumpTnik(self.tniks[i], *self.cnts(), why=f'{why} Tab {st}')    ;  i += 1
                                elif s == NN:  sn += 1  ;   self.J1[N] = sn  ;  self.J2[N] += 1  ;  self.dumpTnik(self.tniks[i], *self.cnts(), why=f'{why} Note {sn}')   ;  i += 1
                                elif s == II:  si += 1  ;   self.J1[I] = si  ;  self.J2[I] += 1  ;  self.dumpTnik(self.tniks[i], *self.cnts(), why=f'{why} IKey {si}')   ;  i += 1
                                elif s == KK:  sk += 1  ;   self.J1[K] = sk  ;  self.J2[K] += 1  ;  self.dumpTnik(self.tniks[i], *self.cnts(), why=f'{why} Chord {sk}')  ;  i += 1
                                else: self.log(f'ERROR {i} {fmtl(self.n)} {fmtl(self.TNIK)} {p}/{np} {l}/{nl} {s}/{ns} {c}/{nc} {t}/{nt} {fmtl(self.lenE())}')
        self.dumpTnik()   ;   self.dumpJ(why)
        if dbg: self.dumpGeom('END', why)
        self.log(f'END plsct {np} {nl} {ns} {nc} {nt}')

    def _dumpTabs(self, why='', dbg=VERBOSE):
        self.initJ(why)
        if dbg: self.dumpGeom('BGN', why)
        i, st, sn, si, sk = 0, 0, 0, 0, 0   ;   np, nl, ns, nc, nt = self.n   # ;   nc += self.zz()
        self.dumpTnik()
        for p in range(np):
            for l in range(nl):
                for s in range(ns):
                    for c in range(nc):
                        for t in range(nt):
                            if   s == TT and self.TNIK[TT]:  st += 1  ;  self.J1[T] = st  ;  self.J2[T] += 1  ;  self.dumpTnik(self.tabs[st-1],   *self.cnts(), why=f'{why} Tab {st}')    ;  i += 1
                            elif s == NN and self.TNIK[NN]:  sn += 1  ;  self.J1[N] = sn  ;  self.J2[N] += 1  ;  self.dumpTnik(self.notes[sn-1],  *self.cnts(), why=f'{why} Note {sn}')   ;  i += 1
                            elif s == II and self.TNIK[II]:  si += 1  ;  self.J1[I] = si  ;  self.J2[I] += 1  ;  self.dumpTnik(self.ikeys[si-1],  *self.cnts(), why=f'{why} IKey {si}')   ;  i += 1
                            elif s == KK and self.TNIK[KK]:  sk += 1  ;  self.J1[K] = sk  ;  self.J2[K] += 1  ;  self.dumpTnik(self.chords[sk-1], *self.cnts(), why=f'{why} Chord {sk}')  ;  i += 1
        self.dumpTnik()   ;   self.dumpJ(why)
        if dbg: self.dumpGeom('END', why)

    def _dumpCols(self, why='', dbg=VERBOSE):
        self.initJ(why)
        if dbg: self.dumpGeom('BGN', why)
        self.dumpTnik()
        for i in range(len(self.cols)):
            self.J1[C] = i  ;  self.J2[C] += 1  ;  self.dumpTnik(self.cols[i], *self.cnts(), why=f'{why} Col {i+1}')
        self.dumpTnik()   ;   self.dumpJ(why)
        if dbg: self.dumpGeom('END', why)
    ####################################################################################################################################################################################################
    def dumpTnik(  self, b=None, p=-1, l=-1, s=-1, c=-1, t=-1, n=-1, i=-1, k=-1, o=-1, a=-1, d=-1, r=-1, z=-1, tid=-1, why=''):
        if   b is None: self.dumpLabel()   ;   self.dumpSprite() if SPRITES else None
        elif type(b) == pyglet.sprite.Sprite:  self.dumpSprite(b, p=p, l=l, s=s, c=c, t=t, n=n, i=i, k=k, o=o, a=a, d=d, r=r, z=z, tid=tid, why=why)
        elif type(b) == pyglet.text.Label:     self.dumpLabel( b, p=p, l=l, s=s, c=c, t=t, n=n, i=i, k=k, o=o, a=a, d=d, r=r, z=z, tid=tid, why=why)

    def dumpSprite(self, b=None, p=-1, l=-1, s=-1, c=-1, t=-1, n=-1, i=-1, k=-1, o=-1, a=-1, d=-1, r=-1, z=-1, tid=-1, why=''):
        if b is None: self.log(f' Tid P  L  S   C   T   N   I   K   z    x       y       w       h        v     identity   mx    my   red grn blu opc   why          group       parent', pfx=0); return
        ff = '{:4} {} {:2} {:2} {:3} {:3} {:3} {:3} {:3} {:3} {:7.2f} {:7.2f} {:7.2f} {:7.2f}     {:1} {:13} {:5.3f} {:5.3f} {:3} {:3} {:3} {:3} {:12} {} {}'
        kk, oo, v, gg, pg    =    b.color, b.opacity, b.visible, b.group, b.group.parent   ;   ID = hex(id(b))   ;   z += r + o + a + d
        x, y, w, h, iax, iay, m, mx, my, rot    =    b.x, b.y, b.width, b.height, b.image.anchor_x, b.image.anchor_y, b.scale, b.scale_x, b.scale_y, b.rotation
        fs = ff.format(tid, p, l, s, c, t, n, i, k, z, x, y, w, h, v, ID, mx, my, kk[0], kk[1], kk[2], oo, why, gg, pg)
        self.log(fs, pfx=0)
        assert(type(b) == pyglet.sprite.Sprite)

    def dumpLabel( self, b=None, p=-1, l=-1, s=-1, c=-1, t=-1, n=-1, i=-1, k=-1, o=-1, a=-1, d=-1, r=-1, z=-1, tid=-1, why=''):
        if b is None: self.log(f' Tid P  L  S   C   T   N   I   K   z    x       y       w       h    text      identity  siz dpi b i red grn blu opc   why', pfx=0) ; return
        x, y, w, h, fn, dd, zz, kk, bb, ii, tx    =    b.x, b.y, b.width, b.height, b.font_name, b.dpi, b.font_size, b.color, b.bold, b.italic, b.text  ;  ID = hex(id(b))   ;   z += r + o + a + d
        ff = '{:4} {} {:2} {:2} {:3} {:3} {:3} {:3} {:3} {:3} {:7.2f} {:7.2f} {:7.2f} {:7.2f} {:6} {:13} {:2.0f} {:3} {:1} {:1} {:3} {:3} {:3} {:3} {} {}'
        fs = ff.format(tid, p, l, s, c, t, n, i, k, z, x, y, w, h, tx, ID, zz, dd, bb, ii, kk[0], kk[1], kk[2], kk[3], why, fn)
        self.log(fs, pfx=0)
    ####################################################################################################################################################################################################
    def createCursor(self, g, dbg=1):
        cc = self.cursorCol()
        c = self.tabs[cc]
        w, h = c.width, c.height
        x, y = c.x - w/2, c.y - h/2
        msg = f'cc={cc} ltabs={len(self.tabs)} x={x:6.2f} y={y:6.2f} w={w:6.2f} h={h:6.2f} wT={self.w[T]:6.2f} hT={self.h[T]:6.2f}'
        if dbg:
            self.log(msg, pos=1)
            self.dumpXYWH()
            self.dumpGeom('NEW', 'CURS')
        self.J2[-2] += 1
        self.cursor = self.createTnik(None, -1, -1, x, y, w, h, g, 8, kl=CCS, why='new Cursor 0', v=1, dbg=1)
        if QQ: self.setLLStyle(self.cc, CURRENT_STYLE)

    def resizeCursor(self, dbg=1):
        cc = self.cursorCol()   ;   c = self.tabs[cc]
        w, h = c.width,   c.height
        x, y = c.x - w/2, c.y - h/2
        msg = f'cc={cc} ltabs={len(self.tabs)} x={x:6.2f} y={y:6.2f} w={w:6.2f} h={h:6.2f} wT={self.w[T]:6.2f} hT={self.h[T]:6.2f}'
        if self.w[T] and self.h[T]:   mx, my = w/self.w[T], h/self.h[T]
        else:                         mx, my,    self.w[T],   self.h[T] = 1, 1, w, h   ;   msg = 'WARN Div By Zero ' + msg   ;   self.log(msg)  # ;   self.quit(msg)
        if dbg:
            self.log(msg, pos=1)
            self.dumpXYWH()
            self.dumpGeom('RSZ', 'CURS')
        self.resizeTnik([], -1, -1, x, y, w, h, mx, my, why='mod Cursor 0', dbg=dbg)
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
    def setCaption(self, msg, dbg=1):
        if dbg: self.log(f'{msg}')
        self.set_caption(msg)

    def resizeFonts(self, dbg = 1):
        ms = self.minSize()  ;  slope, off = 0.6, 3
        fs = fri(ms * slope + off)  ;  formula = '(fs = ms*slope+off)'
        if dbg: self.log(f'{self.fmtWH()} {formula} ms={ms:4.1f} slope={slope} off={off} fs={fs:4.1f}={fri(fs):2}')
        self.setFontParam('font_size', fs, 'fontSize')

    def minSize(self, dbg=1):
        b = self.B   ;   tabs = []
        if dbg: self.log(f'len(b)={len(b)} lenB={fmtl(self.lenB())}')
        for i in range(len(b)):
            if b[i] and b[i][0].width and b[i][0].height: tabs = b[i]
#        tabs = b[TT] if b[TT] and b[TT][0].width and b[TT][0].height else b[NN] if b[NN] and b[NN][0].width and b[NN][0].height else b[II] if b[II] and b[II][0].width and b[II][0].height else b[KK] if b[KK] and b[KK][0].width and b[KK][0].height else None
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
        b, k, dpi, i, n, s = self.fontParams()   ;   pix = s / FONT_SCALE
#        pix = FONT_SCALE * s / dpi
#        self.log(f'{why} ki={k} di={dpi}={FONT_DPIS[dpi]}DPI {s}pt ni={n} {FONT_NAMES[n]} {FONT_SCALE}*{m}')
#        self.log(f'{dpi}:{FONT_DPIS[dpi]}dpi {s}pt {n}:{FONT_NAMES[n]} {k}:{FONT_COLORS[k]} ({FONT_SCALE:4.0f}*{s}pt/{FONT_DPIS[dpi]}dpi)={pix:4.0f}pixels {why}')
        self.log(f'{dpi}:{FONT_DPIS[dpi]}dpi {s}pt {n}:{FONT_NAMES[n]} {k}:{FONT_COLORS[k]} {s}pt = {FONT_SCALE:5.3f}(pt/pix) * {pix:4.1f}pixels {why}')

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
    def on_mouse_release(self, x, y, button, modifiers, dbg=1):
        np, nl, ns, nc, nt = self.n   ;   zz = self.zz()    ;  nc += zz   ;   file = None
        y0 = y   ;   y = self.hh - y   ;   n = nl * ns * nt + ns * QQ   ;  m = int(ns*nt) + QQ
        w = self.ww/nc       ;  h = self.hh/n         ;   d = int(y/h) - QQ
        l = int(d/m)         ;  c  = int(x/w) - zz   ;   t = d - (l * m)  ;  p = 0
        if dbg: self.log(f'BGN button={button} modifiers={modifiers} txt={self.tabs[self.cc].text}', file=file)
        if dbg: self.log(f'x={x} y0={y0:4} w={w:6.2f} h={h:6.2f}')
        if dbg: self.log(f'y={y:4} n={n} m={m} d={d}')
        if dbg: self.log(f'{self.fPos()}     before')
        self.moveTo(f'MOUSE RELEASE', p, l, c, t)
        if dbg: self.log(f'{self.fPos()}     after')
    ####################################################################################################################################################################################################
    def kbkEvntTxt(self): return f'<{self.kbk:8}> <{self.symb:8}> <{self.symbStr:16}> <{self.mods:2}> <{self.modsStr:16}>'
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
        elif kbk == 'L' and self.isCtrlShift(mods):    self.toggleLRows(     '@ ^ L')
        elif kbk == 'L' and self.isCtrl(     mods):    self.toggleLRows(     '@   L')
        elif kbk == 'M' and self.isCtrlShift(mods):    self.toggleLCols(     '@ ^ M', 1)
        elif kbk == 'M' and self.isCtrl(     mods):    self.toggleLCols(     '@   M', 0)
        elif kbk == 'N' and self.isCtrlShift(mods):    self.toggleTabs(      '@ ^ N', NN)
        elif kbk == 'N' and self.isCtrl(     mods):    self.toggleTabs(      '@   N', NN)
        elif kbk == 'O' and self.isCtrlShift(mods):    self.toggleCursorMode('@ ^ O')
        elif kbk == 'O' and self.isCtrl(     mods):    self.toggleCursorMode('@   O')
#        elif kbk == 'P' and self.isCtrlShift(mods):    self.cobj.togglePage( '@ ^ P')
        elif kbk == 'P' and self.isCtrl(     mods):    self.addPage(         '@   P')
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
        elif kbk == 'W' and self.isCtrlShift(mods):    self.swapCols(        '@ & W')
        elif kbk == 'W' and self.isCtrl(     mods):    self.swapCols(        '@ & W')
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
        if dbg: self.log(f'BGN {self.kbkEvntTxt()} motion={motion}')
        if   self.isCtrlAltShift(self.mods):                 msg =             f'ALT CTRL SHIFT ({   motion})'   ;   self.log(msg)   ;   self.quit(msg)
        elif self.isCtrlAlt(self.mods):
            if   motion == 1:                                self.unselectTabs(f'ALT CTRL LEFT ({    motion})',  nt)
            elif motion == 2:                                self.unselectTabs(f'ALT CTRL RIGHT ({   motion})', -nt)
            else:                                            msg =             f'ALT CTRL ({         motion})'   ;   self.log(msg)   ;   self.quit(msg)
        elif self.isAltShift(self.mods):                     msg =             f'ALT SHIFT ({        motion})'   ;   self.log(msg)   ;   self.quit(msg)
        elif self.isCtrlShift(self.mods):                    msg =             f'CTRL SHIFT ({       motion})'   ;   self.log(msg)   ;   self.quit(msg)
        elif self.isShift(self.mods):                        msg =             f'SHIFT ({            motion})'   ;   self.log(msg)   ;   self.quit(msg)
        elif self.isAlt(self.mods):
            if   motion == pygwink.MOTION_UP:                self.moveUp(      f'ALT UP ({           motion})')
            elif motion == pygwink.MOTION_DOWN:              self.moveDown(    f'ALT DOWN ({         motion})')
            elif motion == pygwink.MOTION_LEFT:              self.moveLeft(    f'ALT LEFT ({         motion})')
            elif motion == pygwink.MOTION_RIGHT:             self.moveRight(   f'ALT RIGHT ({        motion})')
            elif motion == pygwink.MOTION_BEGINNING_OF_LINE: self.move(        f'ALT HOME ({         motion})', -nt *  c)
            elif motion == pygwink.MOTION_END_OF_LINE:       self.move(        f'ALT END ({          motion})',  nt * (nc - self.i[C]))
            elif motion == pygwink.MOTION_PREVIOUS_PAGE:     self.prevPage(    f'ALT PAGE UP ({      motion})')
            elif motion == pygwink.MOTION_NEXT_PAGE:         self.nextPage(    f'ALT PAGE DOWN ({    motion})')
            else:                                            msg =             f'ALT ({              motion})'   ;   self.log(msg)   ;   self.quit(msg)
        elif self.isCtrl(self.mods):
            if   motion == pygwink.MOTION_PREVIOUS_WORD:     self.selectTabs(  f'CTRL LEFT ({        motion})', -nt)
            elif motion == pygwink.MOTION_NEXT_WORD:         self.selectTabs(  f'CTRL RIGHT ({       motion})',  nt)
            elif motion == pygwink.MOTION_BEGINNING_OF_LINE: msg = f'CTRL MOTION_BEGINNING_OF_LINE({ motion})'   ;   self.log(msg)   ;   self.quit(msg) # N/A
            elif motion == pygwink.MOTION_END_OF_LINE:       msg = f'CTRL MOTION_END_OF_LINE ({      motion})'   ;   self.log(msg)   ;   self.quit(msg) # N/A
            elif motion == pygwink.MOTION_BEGINNING_OF_FILE: msg = f'CTRL MOTION_BEGINNING_OF_FILE ({motion})'   ;   self.log(msg)   ;   self.quit(msg) # CTRL HOME
            elif motion == pygwink.MOTION_END_OF_FILE:       msg = f'CTRL MOTION_END_OF_FILE ({      motion})'   ;   self.log(msg)   ;   self.quit(msg) # CTRL END
            else:                                            msg =             f'CTRL ({             motion})'   ;   self.log(msg)   ;   self.quit(msg)
        elif self.mods == 0:
            if   motion == pygwink.MOTION_UP:                self.move(        f' UP ({              motion})', -1)
            elif motion == pygwink.MOTION_DOWN:              self.move(        f' DOWN ({            motion})',  1)
            elif motion == pygwink.MOTION_LEFT:              self.move(        f' LEFT ({            motion})', -nt)
            elif motion == pygwink.MOTION_RIGHT:             self.move(        f' RIGHT ({           motion})',  nt)
            elif motion == pygwink.MOTION_PREVIOUS_WORD:     msg = f'MOTION_PREVIOUS_WORD ({         motion})'   ;   self.log(msg)   ;   self.quit(msg)
            elif motion == pygwink.MOTION_NEXT_WORD:         msg = f'MOTION_NEXT_WORD ({             motion})'   ;   self.log(msg)   ;   self.quit(msg)
            elif motion == pygwink.MOTION_BEGINNING_OF_LINE: self.move(        f' HOME ({            motion})', -nt *  c)
            elif motion == pygwink.MOTION_END_OF_LINE:       self.move(        f' END ({             motion})',  nt * (nc - self.i[C]))
            elif motion == pygwink.MOTION_PREVIOUS_PAGE:     self.moveUp(      f' PAGE UP ({         motion})')  # move up   to top    of line, wrap down to bottom of prev line
            elif motion == pygwink.MOTION_NEXT_PAGE:         self.moveDown(    f' PAGE DOWN ({       motion})')  # move down to bottom tab on same line, wrap to next line
            elif motion == pygwink.MOTION_BEGINNING_OF_FILE: msg = f'MOTION_BEGINNING_OF_FILE ({     motion})'   ;   self.log(msg)   ;   self.quit(msg)
            elif motion == pygwink.MOTION_END_OF_FILE:       msg = f'MOTION_END_OF_FILE ({           motion})'   ;   self.log(msg)   ;   self.quit(msg)
            elif motion == pygwink.MOTION_BACKSPACE:         self.setTab(      f'BACKSPACE ({        motion})', self.tblank, rev=1)
            elif motion == pygwink.MOTION_DELETE:            self.setTab(      f'DELETE ({           motion})', self.tblank)
            else:                                            msg =             f'({                  motion})'   ;   self.log(msg)   ;   self.quit(msg)
        if dbg: self.log(f'END {self.kbkEvntTxt()} motion={motion}')
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
    def prevPage(self, how, dbg=1):
        p, l, s, c, t = self.j()
        if dbg: self.log(f'BGN {how} i={fmtl(self.i)}', pos=1)
        self.moveTo(how, p-1, l, c, t)
        self.on_resize(self.ww, self.hh, dbg=1)
        if dbg: self.log(f'END {how} i={fmtl(self.i)}', pos=1)

    def nextPage(self, how, dbg=1):
        p, l, s, c, t = self.j()
        if dbg: self.log(f'BGN {how} i={fmtl(self.i)}', pos=1)
        self.moveTo(how, p+1, l, c, t)
        self.on_resize(self.ww, self.hh, dbg=1)
        if dbg: self.log(f'END {how} i={fmtl(self.i)}', pos=1)
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
    ####################################################################################################################################################################################################
    def moveTo(self, how, p, l, c, t, ss=0, dbg=1):
        if dbg:    self.log(f'BGN {how}', pos=1)
        self._moveTo(p, l, c, t)
        self.moveCursor(ss)
        if dbg:    self.log(f'END {how}', pos=1)

    def move(self, how, k, ss=0, dbg=1):   #  text={self.tabs[self.cc].text} {x:6.2f} {y:6.2f}') # , file=sys.stdout)
        if dbg:    self.log(f'BGN k={k} {how}', pos=1)
        if k:
            p, l, c, t = self.j2()
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
    ####################################################################################################################################################################################################
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
    def setTab(self, how, text, rev=0, dbg=1):
        if rev: self.reverseArrow()   ;    self.autoMove(how)
        p, l, c, t = self.j2()   ;   data = self.data[p][l][c][t]   ;   cc = self.plct2cc(p, l, c, t)  # ;   isDataFret = self.isFret(data)   ;   isTextFret = self.isFret(text)
        self.log(f'BGN {how} text={text} data={data} rev={rev}', pos=1)
        self.setDTNIK(text, cc, p, l, c, t, kk=1) # if isDataFret or isTextFret else 0)
        p, l, c, t = self.j2()   ;   data = self.data[p][l][c][t]
        self.log(f'END {how} text={text} data={data} rev={rev}', pos=1)
        if rev: self.reverseArrow()
        else:   self.autoMove(how)
        if SNAP and dbg: self.snapshot()
        self.dataHasChanged = 1

    def setDTNIK(self, text, cc, p, l, c, t, kk=0, pos=0, dbg=0):
        if dbg: self.log(f'BGN kk={kk}    text={text}', pos=pos)
        self.setData(text, p, l, c, t)
        imap = self.getImap(p, l, c)
        if self.TNIK[TT]: self.setTab2( text, cc)
        if self.TNIK[NN]: self.setNote( text, cc, t)
        if self.TNIK[II]: self.setIkey( imap, p, l, c)
        if self.TNIK[KK]: self.setChord(imap, p, l, c)
        if dbg: self.log(f'END kk={kk}    text={text} len(imap)={len(imap)}', pos=pos)
    ####################################################################################################################################################################################################
    def setData(self, text, p, l, c, t, pos=0, dbg=0):
        data = self.data[p][l][c]
        if dbg: self.log(f'BGN t={t} text={text} data={data}', pos=pos)
        self.data[p][l][c] = data[0:t] + text + data[t+1:]
        data = self.data[p][l][c]
        if dbg: self.log(f'END t={t} text={text} data={data}', pos=pos)

    def setTab2(self, text, cc, pos=0, dbg=0):
        if dbg: self.log(f'BGN         text={text} tabs[{cc}]={self.tabs[cc].text}', pos=pos)
        self.tabs[cc].text = text
        if dbg: self.log(f'END         text={text} tabs[{cc}]={self.tabs[cc].text}', pos=pos)

    def setNote(self, text, cc, t, pos=0, dbg=0):
        if dbg: self.log(f'BGN     t={t} text={text} notes[{cc}]={self.notes[cc].text}', pos=pos)
        self.notes[cc].text = self.tab2nn(text, t) if self.isFret(text) else self.tblank
        if dbg: self.log(f'END     t={t} text={text} notes[{cc}]={self.notes[cc].text}', pos=pos)

    def getImap(self, p, l, c, dbg=1, dbg2=1):
        cn = self.plc2cn(p, l, c)      ;    key = cn   ;   dl = self.dl()   ;   mli = self.cobj.mlimap
        msg1  = f'plc=[{p} {l} {c}]'   ;   msg2 = f'dl={fmtl(dl)} cn={cn} key={key} keys={fmtl(list(mli.keys()))}'
        if p >= dl[0] or l >= dl[1] or c >= dl[2]:  msg = f'ERROR Indexing {msg1} >= {msg2}'   ;   self.log(msg)   ;   self.quit(msg)
        if dbg:           self.log(f'{msg1} {msg2}')
        imap  = self.cobj.getChordName(p, l, c)
        if dbg2 and imap: self.cobj.dumpImap(imap)
        return imap

    def setIkey(self, imap, p, l, c, pos=0, dbg=0):
        cc = self.plct2cc(p, l, c, 0)
        ikeys = imap[0] if imap else []
        if dbg: self.log(f'BGN ikeys={fmtl(ikeys)} len(imap)={len(imap)}', pos=pos)
        self.setIkeyText(ikeys, cc, p, l, c)
        if dbg: self.log(f'END ikeys={fmtl(ikeys)} len(imap)={len(imap)}', pos=pos)

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
        cc = self.plct2cc(p, l, c, 0)
        name = imap[3] if imap and len(imap) > 3 else ''  ;   chunks = imap[4] if imap and len(imap) > 4 else []
        if dbg: self.log(f'BGN name={name} chunks={fmtl(chunks)} len(imap)={len(imap)}', pos=pos)
        self.setChordName(cc, name, chunks) if name and chunks else None   ;    self.log(f'WARN Not A Chord cc={cc} name={name} chunks={chunks}', pos=pos)
        if dbg: self.log(f'END name={name} chunks={fmtl(chunks)} len(imap)={len(imap)}', pos=pos)

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
    def dumpSmap(self, why, pos=0): self.log(f'{why} smap={fmtm(self.smap)}', pos=pos)

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
                self.setDTNIK( self.tblank, k + t, p, l, c, t, kk=1 if t==nt-1 else 0)
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
                self.setDTNIK(text[t], kt, p, l, c, t, kk=1 if t==nt-1 else 0)
            if dbg: self.log(f'smap[{k}]={text} kt={kt} kk={kk} dk={dk}')
#        if not hc: self.unselectAll('pasteTabs()')
#        elif dbg:  self.log(f'holding a copy of smap')
#        self.dumpSmap(f'END {how} hc={hc} kk={kk} cc={cc} ntc={ntc} cn={self.cc2cn(cc) + 1}')
        self.dumpSmap(f'END {how} kk={kk} cc={cc} ntc={ntc} cn={self.cc2cn(cc)} plcr {p} {l} {c} {r}')
        self.dataHasChanged = 1

    def swapCols(self, how):
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
                    if fn and self.isFret(fn):  self.setDTNIK(fn, kt, p, l, c, t, kk=1 if t==nt-1 else 0)
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
            np, nl, ns, nc, nr = self.n  ;  nc += self.zz()
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
            if dbg2: self.dumpTniks('SWAP')
            self.dataHasChanged = 1
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
                if i1 != i2:   imap = self.getImap(p, l, c)   ;   self.setChord(imap, p, l, c, t)    ;    i1 = i2
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
        np, nl, ns, nc, nt = self.n   ;   zz = self.zz()  ;  nc += zz
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
                for c in range(zz, nc):
                    self.data[p][l][c-zz] = self.tblankCol
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
        self.deleteList(self.tniks)
    '''
    def setStringNumbs(self):
        np, nl, ns, nr, nc = self.n  ;  nc += self.zz()  ;  i = C1
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
        np, nl, ns, nr, nc = self.n  ;  nc += self.zz()  ;  i = C1
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
        np, nl, ns, nr, nc = self.n  ;  nc += self.zz()  ;  i = C2
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
    def quit(self, why='', code=0, dbg=0):
        self.log(QUIT, pfx=0)
        self.log(f'BGN {why} code={code}')
#        self.dumpDataVert()
#        self.dumpDataHorz()
        self.dumpGeom('    ')
        self.dumpJ('quit')
        if       code and AUTO_SAVE: self.saveDataFile(why, f=0)
        elif not code:               self.saveDataFile(why, f=1)
        self.dumpXYWH()
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
