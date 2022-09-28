#import logging#, shutil#, unicodedata, readline, csv, string
import glob, inspect, itertools, math, os, pathlib, sys
import operator, unicodedata
from collections import OrderedDict as cOd
from itertools   import accumulate
import pyglet
import pyglet.sprite as pygsprt
import pyglet.text as pygtxt
import pyglet.window.event as pygwine
import pyglet.window.key as pygwink
#sys.path.append(os.path.abspath("./lib"))
#print(f'{len(sys.path)=}')
#for _ in sys.path:
#    print(f'{_}')
import chord, util

########################################################################################################################################################################################################
def dumpGlobals():
    util.slog(f'argv      = {util.fmtl(sys.argv, ll=1)}', file=LOG_FILE)
    util.slog(f'PATH      = {PATH}',      file=LOG_FILE)
    util.slog(f'BASE_PATH = {BASE_PATH}', file=LOG_FILE)
    util.slog(f'BASE_NAME = {BASE_NAME}', file=LOG_FILE)
########################################################################################################################################################################################################
Z = ' '   ;    TEST_TEXT = 0
PATH             = pathlib.Path.cwd() / sys.argv[0]
BASE_PATH        = PATH.parent
BASE_NAME        = BASE_PATH.stem
SNAP_DIR         = 'snaps'
SNAP_SFX         = '.png'
LOG_FILE         = None   ;   LF2 = None
P, L, S, C       =  0,  1,  2,  3
T, N, I, K       =  4,  5,  6,  7
R, Q, H, V       =  8,  9, 10, 11
O, A, D          = 12, 13, 14
#                     0         1       2        3       4        5       6        7         8        9      10      11       12       13       14      15
JTEXTS           = ['Page',  'Line',  'Sect',  'Col',  'Tab',  'Note',  'IKey',  'Kord',  '_LLR',  '_LLC', 'Curs', 'View',  '_SNo',  '_SNm',  '_Cpo', '_TNIK']
jTEXTS           = ['pages', 'lines', 'sects', 'cols', 'tabs', 'notes', 'ikeys', 'Kords', 'lrows', 'lcols', 'curs', 'views', 'snos', 'snas', 'capos', 'tniks']
JFMT             = [   1,       2,       2,       3,      4,      4,       4,       4,       2,       3,       1,       1,      2,      2,      3,       4]
TT, NN, II, KK   =  0,  1,  2,  3
C1,  C2          =  0,  1
NORMAL_STYLE, SELECT_STYLE, CURRENT_STYLE, COPY_STYLE = 0, 1, 2, 3
CSR_MODES        = ['MELODY', 'CHORD', 'ARPG']
HARROWS, VARROWS = ['LEFT', 'RIGHT'], ['UP', 'DOWN']
MELODY, CHORD, ARPG   = 0, 1, 2
LEFT, RIGHT, UP, DOWN = 0, 1, 0, 1
# FS_MAX = 90
########################################################################################################################################################################################################
class Test:
    def __init__(self, a, file=None): self._a = a  ;  util.slog(f'<Test_init_:     _a={self._a}>', pfx=1, file=file)
    @property
    def a(self, file=None):           util.slog(f'<Test_prop_a:     _a={self._a}>', pfx=1, file=file)
    @a.setter
    def a(self, a, file=None):        self._a = a  ;  util.slog(f'<Test_set_a:     _a={self._a}>', pfx=1, file=file)
    @a.getter
    def a(self, file=None):           util.slog(f'<Test_get_a:     _a={self._a}>', pfx=1, file=file)  ;  return self._a
    @a.deleter
    def a(self, file=None):           util.slog(f'<Test_del_a: del _a>', pfx=1, file=file)  ;  del self._a
########################################################################################################################################################################################################

class Tabs(pyglet.window.Window):
    def test(self, file=None):
        test = Test(123, file=file)
        self.log(f'init test.a={test.a}')
        test.a = 456
        self.log(f'set  test.a={test.a}')
        del test.a
        self.log(f'del  test.a={test.a}')
        exit()

    def test1(self):
#        x = '\U0001F600 \U0001F603 \U0001F606 \U0001F609'  ;  y = ['\U0001F600', '\U0001F603', '\U0001F606', '\U0001F609'] #        print(f'{x=} y={util.fmtl(y)}')
        self.test_1(0x1D100)
        self.test_1(0x1D600)
#        exit()

    def test_1(self, x):
        for i in range(0x100):
            y = x+i  ;  u = chr(y)  ;  uc = unicodedata.category(u)
            try:                       un = unicodedata.name(u)
            except ValueError:         un = None
            y = f'{i:3} {i:02X} {y:05X} chr({y:05X})'  ;  s = f'{u} ord({u})={ord(u):05X} {uc} {un}'
            print(f'{y} {s}')
#            print(f'{y} {s}', file=LOG_FILE)
            self.log(f'{y} {s}', pfx=0)

    def test2(self):
        self.log(f'os.path.abspath(".")     ={os.path.abspath(".")}')
        self.log(f'os.path.abspath("./")    ={os.path.abspath("./")}')
        self.log(f'os.path.abspath("../")   ={os.path.abspath("../")}')
        self.log(f'os.path.abspath("./Lib") ={os.path.abspath("./Lib")}')
        self.log(f'os.path.abspath("../Lib")={os.path.abspath("../Lib")}')
        self.log( 'sys.path:')
        sys.path.append(os.path.abspath("./Lib"))
#        for p in sys.path:
#            self.log(f'{p}', pfx=0)

    def __init__(self):
        dumpGlobals()
        self.log(f'STFILT:\n{util.fmtl(util.STFILT)}')
        self.log(f'BGN {__class__}')
        self.LOG_ID       = 0
        self.lfSeqPath    = self.getFilePath(seq=1, fdir='logs', fsfx='.log')
#        snapGlobArg       = str(BASE_PATH / SNAP_DIR / BASE_NAME) + '.*' + SNAP_SFX
#        snapGlob          = glob.glob(snapGlobArg)
#        self.log(f'snapGlobArg =  {snapGlobArg}')
#        self.log(f'   snapGlob = { util.fmtl(snapGlob)}')
#        self.deleteGlob(snapGlob, 'SNAP_GLOB')
        self.snapWhy, self.snapType, self.snapReg, self.snapId = '?', '_', 0, 0
        self.catPath      = str(BASE_PATH / 'cats' / BASE_NAME) + '.cat'
        self.catPath      = self.getFilePath(seq=1, fdir='cats', fsfx='.cat')
        self.log(f'catPath={self.catPath}')
        self.settingN     = 0     ;   self.setNvals  = []    ;   self.setNtxt = ''
        self.shiftingTabs = 0     ;   self.shiftSign = 1
        self.inserting    = 0     ;   self.insertStr = ''
        self.jumping      = 0     ;   self.jumpStr   = ''    ;   self.jumpAbs = 0
        self.swapping     = 0     ;   self.swapSrc   = ''    ;   self.swapTrg = ''
        self.idmap        = cOd()
        self.cc           = 0
        self.allSelected  = 0
        self.resyncData   = 0
        self.hArrow, self.vArrow,  self.csrMode                 = RIGHT, UP, CHORD    ;    self.dumpCursorArrows('init()')
        self.tblank, self.tblanki,   self.cursor,  self.data    = None, None, None, []
        self.J1,  self.J2 = [], []
        self.ki           = []
        self.kbk,    self.symb,    self.mods,        self.symbStr, self.modsStr =         0, 0, 0, '', ''
        self.A_CENTER  = 0  ;  self.A_LEFT      = 1  ;  self.A_RIGHT      = 0
        self.X_CENTER  = 1  ;  self.X_LEFT      = 0  ;  self.X_RIGHT      = 0
        self.Y_CENTER  = 1  ;  self.Y_TOP       = 0  ;  self.Y_BOTTOM     = 0  ;  self.Y_BASELINE = 0
        self.AUTO_SAVE = 0  ;  self.CAT         = 0  ;  self.CHECKERED    = 0  ;  self.EVENT_LOG  = 1  ;  self.FULL_SCREEN = 0
        self.GEN_DATA  = 0  ;  self.MULTI_LINE  = 0  ;  self.ORDER_GROUP  = 1  ;  self.RESIZE     = 1  ;  self.RD_STDOUT   = 0
        self.SNAPS     = 1  ;  self.SPRITES     = 0  ;  self.SUBPIX       = 0  ;  self.TEST       = 1  ;  self.VERBOSE     = 0
        self.VIEWS     = 0  ;  self.TRANSPOSE_A = 1  ;  self.DBG_TAB_TEXT = 0  ;  self.BGC        = 1  ;  self.FRET_BOARD  = 0
        self.LL           = 0
        self.SS           = set() if 0 else {0, 1, 2, 3}
        self.ZZ           = set() if 1 else {0, 1}
        self.p0x, self.p0y, self.p0w, self.p0h, self.p0sx, self.p0sy = 0, 0, 0, 0, 0, 0
        nt                = 6
        self.n            = [2, 2, 50, nt]
        self.i            = [1, 1,  1, 1]
        self.dfn          = ''
        ARGS = util.parseCmdLine(file=LOG_FILE)
        self.log(f' argMap={util.fmtm(ARGS)}')
        if 'f' in ARGS and len(ARGS['f'])  > 0: self.dfn =       ARGS['f'][0]
        if 'n' in ARGS and len(ARGS['n'])  > 0: self.n   = [ int(ARGS['n'][i]) for i in range(len(ARGS['n'])) ]
        if 'i' in ARGS and len(ARGS['i'])  > 0: self.i   = [ int(ARGS['i'][i]) for i in range(len(ARGS['i'])) ]
        if 'a' in ARGS and len(ARGS['a']) == 0: self.AUTO_SAVE     =  1
        if 'b' in ARGS and len(ARGS['b']) == 0: self.FRET_BOARD    =  1
        if 'B' in ARGS and len(ARGS['B']) == 0: self.BGC           =  1
        if 'c' in ARGS and len(ARGS['c']) == 0: self.CAT           =  1
        if 'C' in ARGS and len(ARGS['C']) == 0: self.CHECKERED =  1
        if 'd' in ARGS and len(ARGS['d']) == 0: self.DBG_TAB_TEXT  =  1
        if 'e' in ARGS and len(ARGS['e']) == 0: self.EVENT_LOG     =  1
        if 'F' in ARGS and len(ARGS['F']) == 0: self.FULL_SCREEN   =  1
        if 'G' in ARGS and len(ARGS['G']) == 0: self.GEN_DATA      =  1
        if 'g' in ARGS and len(ARGS['g']) == 0: self.ORDER_GROUP   =  1
        if 'M' in ARGS and len(ARGS['M']) == 0: self.MULTI_LINE    =  1
        if 'R' in ARGS and len(ARGS['R']) == 0: self.RESIZE        = 0
        if 'p' in ARGS and len(ARGS['p']) == 0: self.SNAPS         =  1
        if 'x' in ARGS and len(ARGS['x']) == 0: self.SUBPIX        =  1
        if 's' in ARGS and len(ARGS['s']) == 0: self.SPRITES       =  1
        if 't' in ARGS and len(ARGS['t']) == 0: self.TEST          =  1
        if 'v' in ARGS and len(ARGS['v']) == 0: self.VERBOSE       =  1
        if 'V' in ARGS and len(ARGS['V']) == 0: self.VIEWS         =  1
        if 'r' in ARGS and len(ARGS['r']) == 0: self.RD_STDOUT     =  1
        if 'u' in ARGS and len(ARGS['u']) == 0: self.TRANSPOSE_A   =  1
        if 'L' in ARGS and len(ARGS['L']) == 0: self.LL =  1
        if 'S' in ARGS and len(ARGS['S']) >= 0: self.SS = { int(ARGS['S'][i]) for i in range(len(ARGS['S'])) }
        if 'Z' in ARGS and len(ARGS['Z']) >= 0: self.ZZ = { int(ARGS['Z'][i]) for i in range(len(ARGS['Z'])) }
        self.n.insert(S, self.ssl())
        self.i.insert(S, self.ssl())
        self.dumpArgs()
        global LF2   ;   LF2 = LOG_FILE if self.RD_STDOUT else sys.stdout
        if self.TEST: self.test1() # ;  self.quit('EXIT TEST', save=0)
        self.sAlias = 'GUITAR_6_STD'
        self.sobj = util.Strings(LOG_FILE, self.sAlias)
        self.cobj = chord.Chord( LOG_FILE, self.sobj)
        util.Note.setType(util.Note.SHARP)  ;  self.log(f'{util.Note.TYPE=}')
        self.n[S] = self.ssl()
        self._initDataPath()
        if self.CAT: self.cobj.dumpOMAP(str(self.catPath))
        self._initWindowA()
        self.log(f'WxH={self.fmtWxH()}')
        super().__init__(screen=self.screens[1], fullscreen=self.FULL_SCREEN, resizable=True, visible=False)
        self.log(f'WxH={self.fmtWxH()}')
        self._initWindowB()
        self.log(f'WxH={self.fmtWxH()}')
        self.a  = 'center' if self.A_CENTER else 'left' if self.A_LEFT else 'right'  if self.A_RIGHT  else '???'
        self.ax = 'center' if self.X_CENTER else 'left' if self.X_LEFT else 'right'  if self.X_RIGHT  else '???'
        self.ay = 'center' if self.Y_CENTER else 'top'  if self.Y_TOP  else 'bottom' if self.Y_BOTTOM else 'baseline' if self.Y_BASELINE else '???'
        self.dumpAxy()    ;   self.dumpAXY()
        self._reinit()
        self.log(f'END {__class__}')
        self.log(f'{util.INIT}', pfx=0)

    def dumpArgs(self):
        self.log(f'[f]             {self.dfn=}')
        self.log(f'[n]             {self.fmtn()}')
        self.log(f'[i]             {self.fmti()}')
        self.log(f'[a]    {self.AUTO_SAVE=}')
        self.log(f'[b]   {self.FRET_BOARD=}')
        self.log(f'[B]          {self.BGC=}')
        self.log(f'[c]          {self.CAT=}')
        self.log(f'[d] {self.DBG_TAB_TEXT=}')
        self.log(f'[C]    {self.CHECKERED=}')
        self.log(f'[e]    {self.EVENT_LOG=}')
        self.log(f'[F]  {self.FULL_SCREEN=}')
        self.log(f'[G]     {self.GEN_DATA=}')
        self.log(f'[M]   {self.MULTI_LINE=}')
        self.log(f'[g]  {self.ORDER_GROUP=}')
        self.log(f'[p]        {self.SNAPS=}')
        self.log(f'[R]       {self.RESIZE=}')
        self.log(f'[x]       {self.SUBPIX=}')
        self.log(f'[s]      {self.SPRITES=}')
        self.log(f'[t]         {self.TEST=}')
        self.log(f'[v]      {self.VERBOSE=}')
        self.log(f'[V]        {self.VIEWS=}')
        self.log(f'[r]    {self.RD_STDOUT=}')
        self.log(f'[u]  {self.TRANSPOSE_A=}')
        self.log(f'[L]           {self.LL=}')
        self.log(f'[S]           .SS={util.fmtl(self.SS)}')
        self.log(f'[Z]           .ZZ={util.fmtl(self.ZZ)}')

    def _reinit(self):
        self.log('BGN')
        self.pages, self.lines, self.sects, self.cols  = [], [], [], []  ;  self.A = [self.pages, self.lines, self.sects, self.cols]
        self.tabs,  self.notes, self.ikeys, self.kords = [], [], [], []  ;  self.B = [self.tabs,  self.notes, self.ikeys, self.kords]
        self.lrows, self.lcols, self.cursr, self.views = [], [], [], []  ;  self.C = [self.lrows, self.lcols, self.cursr, self.views]
        self.snos,  self.snas,  self.capos             = [], [], []      ;  self.D = [self.snos,  self.snas,  self.capos]
        self.E = [*self.A, *self.B, *self.C, *self.D]
        self.log(f'E={util.fmtl(self.E)}')
        self.resetJ('_reinit')
        self.data = []
        self.cursor,  self.caret, self.cc = None, None, 0
        self.kbk,     self.symb,  self.mods,  self.symbStr, self.modsStr = 0, 0, 0, '', ''
        self.ki = [ 0 for _ in range(len(self.E)) ]   ;   self.log(f'{util.fmtl(self.ki)}')
        self.tblanki, self.tblanks  = 1, [' ', '-']                ;     self.tblank = self.tblanks[self.tblanki]
        self.tblankCol              = self.tblank * self.n[T]      ;  self.tblankRow = self.tblank * (self.n[C] + self.zzl())
        self.dumpBlank()
        self._init()
        self.log('END')

    def _init(self, dbg=1):
        self._initColors()
        self._initData()
        if self.AUTO_SAVE: pyglet.clock.schedule_interval(self.autoSave, 10, how='autoSave timer')
        self._initFonts()
        self._initTextLabels()
        self._initTniks()
        if self.SNAPS: self.regSnap('init', 'INIT')
        if dbg: self.dumpStruct('Init')

    def _initColors(self):
        a = self.SPRITES and not self.BGC  ;  b = self.SPRITES and self.BGC  ;  c = not self.SPRITES and not self.BGC
        P1, P2 = REDS,    REDS     ;  L1, L2 = BLUES,  BLUES   ;  S1, S2 = GRAY0S,  GRAY0S   ;  Z1, Z2 = RED2S, RED2S
        T1, T2 = ORANGES, ORANGE2S ;  N1, N2 = GREENS, GREEN2S ;  I1, I2 = VIOLETS, VIOLET2S ;  K1, K2 = CYANS, CYAN2S
        R1, R2 = CC3S,    CC3S     ;  Q1, Q2 = CC1S,   CC2S    ;  H1, H2 = CC3S,    CC4S     ;  V1, V2 = PINKS, PINKS
        O1, O2 = PINKS,   PINKS    ;  A1, A2 = BLUES,  BLUES   ;  D1, D2 = INDIGOS, INDIGOS
        kP = [P1[ 0], P2[10]] if a else [P1[ 0], P2[10]] if b else [P1[ 0], P2[10]] if c else [P1[10], P2[3]]
        kL = [L1[ 0], L2[10]] if a else [L1[ 0], L2[10]] if b else [L1[ 0], L2[10]] if c else [L1[ 0], L2[10]]
        kS = [S1[ 0], S2[ 0]] if a else [S1[ 0], S2[ 0]] if b else [S1[ 0], S2[ 0]] if c else [S1[ 0], S2[ 0]]
        kC = [Z1[15], Z1[ 7]] if a else [Z1[15], Z1[ 7]] if b else [Z1[15], Z1[ 7]] if c else [Z1[15], Z1[ 7]]
        kT = [T2[13], T2[ 3]] if a else [T1[13], T1[ 3]] if b else [T1[15], T1[ 0]] if c else [T1[15], T1[ 0]]
        kN = [N1[13], N2[ 3]] if a else [N1[13], N2[ 3]] if b else [N1[15], N1[ 0]] if c else [N1[15], N1[ 0]]
        kI = [I2[15], I2[ 0]] if a else [I1[15], I1[ 0]] if b else [I1[15], I1[ 0]] if c else [I1[15], I1[ 0]]
        kK = [K1[13], K2[ 3]] if a else [K1[13], K2[ 3]] if b else [K1[15], K1[ 0]] if c else [K1[15], K1[ 0]]
        kR = [R1[13], R2[ 0]] if a else [R1[13], R2[ 0]] if b else [R1[13], R2[ 0]] if c else [R1[13], R2[ 0]]
        kQ = [Q1[13], Q2[ 0]] if a else [Q1[13], Q2[ 0]] if b else [Q1[13], Q2[ 0]] if c else [Q1[13], Q2[ 0]]
        kH = [H1[ 0], H2[15]] if a else [H1[ 0], H2[15]] if b else [H1[ 0], H2[15]] if c else [H1[ 0], H2[15]]
        kV = [V1[ 0], V2[12]] if a else [V1[ 0], V2[12]] if b else [V1[ 0], V2[12]] if c else [V1[ 0], V2[12]]
        kO = [O1[ 0], O2[10]] if a else [O1[ 0], O2[10]] if b else [O1[ 0], O2[10]] if c else [O1[ 0], O2[10]]
        kA = [A2[ 0], A2[10]] if a else [A2[ 0], A2[10]] if b else [A2[ 0], A2[10]] if c else [A2[ 0], A2[10]]
        kD = [D1[ 0], D2[10]] if a else [D1[ 0], D2[10]] if b else [D1[ 0], D2[10]] if c else [D1[ 0], D2[10]]
        self.k   = [ kP, kL, kS, kC,  kT, kN, kI, kK,  kR, kQ, kH, kV,  kO, kA, kD ]
        [ self.log(f'[{i:2}] {util.fmtl(e, w=3)}') for i, e in enumerate(self.k) ]

    def _initData(self, dbg=1):
        self._initDataPath()
        if self.GEN_DATA: self.genDataFile(self.dataPath1)
        self.readDataFile(self.dataPath1)
        util.copyFile    (self.dataPath1, self.dataPath2)
#        self.data = self.A_transposeData(dump=dbg) if self.TRANSPOSE_A else self.transposeDataDump() if dbg else self.OLD_transposeData()
        if self.TRANSPOSE_A:    self.data = self.A_transposeData(dump=dbg)
        else:               self.transposeDataDump() if dbg else self.OLD_transposeData()
        old = self.fmtn('')
        self.n[P] = self.dl()[0]
        self.log(f'{self.fmtdl()}')
        self.log(f'Updating n[P] {old=} {self.fmtn()}')
        self._initntp()

    def _initDataPath(self):
        dataDir   = 'data'  ;  dataSfx = '.dat'  ;  dataPfx = f'.{self.n[C]}'
        baseName  = self.dfn if self.dfn else BASE_NAME + dataPfx + dataSfx
        dataName0 = baseName + '.asv'
        dataName1 = baseName
        dataName2 = baseName + '.bck'
        self.dataPath0 = BASE_PATH / dataDir / dataName0
        self.dataPath1 = BASE_PATH / dataDir / dataName1
        self.dataPath2 = BASE_PATH / dataDir / dataName2
        self.log(f'{dataName0=}')
        self.log(f'{dataName1=}')
        self.log(f'{dataName2=}')
        self.log(f'{self.dataPath0=}', pfx=0)
        self.log(f'{self.dataPath1=}', pfx=0)
        self.log(f'{self.dataPath2=}', pfx=0)

    def _initTniks(self, dbg=0, dbg2=0):
        self.ssl()
        self.smap = {}
        self.dumpAxy()  ;  self.dumpAXY()
        self.createTniks()
        if dbg:  self.cobj.dumpMlimap('Init')
        if dbg2: self.dumpTniks('Init')
    ####################################################################################################################################################################################################
    def _initWindowA(self, dbg=1):
        display      = pyglet.canvas.get_display()
        if dbg: self.log(f'BGN {self.fmtWxH()}')  ;  self.log(f'{display=}')
        self.screens = display.get_screens()      ;  s = self.screens
        if dbg:
            for i in range(len(s)): self.log(f'screens[{i}] x={s[i].x} y={s[i].y:5} {self.fmtWxH(s[i].width, s[i].height)}')
            self.log(f'END {self.fmtWxH()}')

    def _initWindowB(self, dbg=1):
        if dbg: self.log(f'BGN {self.fmtWxH()}')
        self.batch = pyglet.graphics.Batch()
        self._initGroups()
        self.set_visible()
        self.log(f'get_size={self.get_size()}')
        if self.EVENT_LOG:
            self.eventLogger = pygwine.WindowEventLogger()
            self.push_handlers(self.eventLogger)
            self.keyboard = pygwine.key.KeyStateHandler()
            self.push_handlers(self.keyboard)
        if dbg: self.log(f'END {self.fmtWxH()}')
    ####################################################################################################################################################################################################
    def _initGroups(self):    #     [P, L, S, C   T, N, I, K   R, Q, H, V,  O, A, D]
        self.g = []   ;   self.gn = [1, 2, 3, 4,  5, 5, 5, 5,  5, 5, 6, 0,  5, 5, 5]
        self.log(f'{util.fmtl(self.gn)}')
        for i in range(1+max(self.gn)):
            p = None if self.ORDER_GROUP or i==0 else self.g[i-1]
            self.g.append(self._initGroup(i, p))
            self.log(f'g[{i}]={self.g[i]} p={self.g[i].parent}')
    def _initGroup(self, order=0, parent=None): return pyglet.graphics.OrderedGroup(order, parent) if self.ORDER_GROUP else pyglet.graphics.Group(parent)
    ####################################################################################################################################################################################################
    def _initTextLabels(self):
        self.labelTextA, self.labelTextB = [], []
        self.createLabelText()
        self.llText = ['M', '0']
        self.llText.extend(self.labelTextB)
        self.log(f'{util.fmtl(self.llText)}')
    ####################################################################################################################################################################################################
    def lenA(self):                   return [ len(_) for _ in self.A ]
    def lenB(self):                   return [ len(_) for _ in self.B ]
    def lenC(self):                   return [ len(_) for _ in self.C ]
    def lenD(self):                   return [ len(_) for _ in self.D ]
    def lenE(self):                   return [ len(_) for _ in self.E ]
    def j(   self):                   return [ i-1 if i else 0 for    i in           self.i ]
    def j2(  self):                   return [ i-1 if i else 0 for j, i in enumerate(self.i)  if j != S ]
    def j2g(     self, j):            return self.g[ self.gn[j] ]
    def setJ(    self, j, n):         self.J1[j] = n    ;   self.J2[j] += 1          ;   self.J1[-1] += 1   ;  self.J2[-1] += 1         ;  return j
    def setJdump(self, j, n, why=''): self.setJ(j, n)   ;   self.dumpTnik(self.E[j][self.J2[j]-1], j, why)  ;  return j
    def resetJ(self, why='', dbg=1):  self.J1 = [ 0 for _ in range(len(self.E)+1) ]  ;   self.J2 = [ 0 for _ in range(len(self.E)+1) ]  ;  self.dumpJs(why) if dbg else None
    ####################################################################################################################################################################################################
    def ssl(self, dbg=0):  l = len(self.SS)   ;   self.log(f'{self.fmtn()} SS={util.fmtl(self.ss2sl())} l={l}') if dbg else None   ;   return l   # return 0-4
    def zzl(self, dbg=0):  l = len(self.ZZ)   ;   self.log(f'{self.fmtn()} ZZ={util.fmtl(self.zz2sl())} l={l}') if dbg else None   ;   return l   # return 0-2
    def ss2sl(self): return sorted(self.SS)
    def zz2sl(self): return sorted(self.ZZ)
    ####################################################################################################################################################################################################
    def dl(  self, data=None, p=0, l=0, c=0):  return list(map(len,                       self.dplc(data, p, l, c)))
    def dt(  self, data=None, p=0, l=0, c=0):  return list(map(type,                      self.dplc(data, p, l, c)))
    def dtA( self, data=None, p=0, l=0, c=0):  return [ str(type(a)).strip('<>') for a in self.dplc(data, p, l, c) ]
    ####################################################################################################################################################################################################
    def dproxy(self, data):                      return data if data is not None else self.data
    def dplc(  self, data=None, p=0, l=0, c=0):
        data = self.dproxy(data)
        if data:
            if p >= len(data):           msg = f'ERROR BAD p index {p=} {l=} {c=} {len(data)=}'        ;  self.log(msg)  ;  self.quit(msg)
            if l >= len(data[p]):        msg = f'ERROR BAD l index {p=} {l=} {c=} {len(data[p])=}'     ;  self.log(msg)  ;  self.quit(msg)
            if c >= len(data[p][l]):     msg = f'ERROR BAD c index {p=} {l=} {c=} {len(data[p][l])=}'  ;  self.log(msg)  ;  self.quit(msg)
            return data, data[p], data[p][l], data[p][l][c]
        else: return []
    ####################################################################################################################################################################################################
    def fmtdl( self, data=None):       return f'{util.fmtl(self.dl(data))}'
    def fmtdt( self, data=None):       return f"[{' '.join([ t.replace('class ', '') for t in self.dtA(data) ])}]"
    def fmtJ1( self, w=None, d=0):            w = w if w is not None else JFMT  ;  d1 = "" if not d else "["  ;  d2 ="" if not d else "]"  ;  return f'{util.fmtl(self.J1,     w=w, d1=d1, d2=d2)}'
    def fmtJ2( self, w=None, d=0):            w = w if w is not None else JFMT  ;  d1 = "" if not d else "["  ;  d2 ="" if not d else "]"  ;  return f'{util.fmtl(self.J2,     w=w, d1=d1, d2=d2)}'
    def fmtLE( self, w=None):                 w = w if w is not None else JFMT  ;  d1 = ""                    ;  d2 =""                    ;  return f'[{util.fmtl(self.lenE(), w=w, d1=d1, d2=d2)} {sum(self.lenE())}]'
    ####################################################################################################################################################################################################
    def fmtn(self, pfx='n=', n=None):         n = n if n is not None else self.n  ;   return f'{pfx}{util.fmtl(n)}'
    def fmti(self, pfx='i='):                 return f'{pfx}{util.fmtl(self.i)}'
#    def fplct(self):                          return f'{util.fmtl(self.j2())}'
    def fmtPos(self):                         plct = self.j2()        ;  cc = self.plct2cc(*plct)   ;  cn = self.cc2cn(cc)       ;  return f'{util.fmtl(plct)} {cc:3} {cn:2}]'
    def fmtDxD(self, data=None,      d='x'):  l = list(map(str, self.dl(data)))               ;   return f'({d.join(l)})'
    def fmtIxI(self,                 d='x'):  l = list(map(str, self.i))   ;   del l[S:S+1]   ;   return f'({d.join(l)})'
    def fmtWxH(self, w=None, h=None, d='x'):  w = w if w is not None else self.width  ;  h = h if h is not None else self.height  ;  return f'({w}{d}{h})'
    def fmtP0(self):                          return f'{self.p0x} {self.p0w} {self.p0sx} {self.p0y} {self.p0h} {self.p0sy}'
    def fmtWxHP0(self):                       return f'{self.fmtWxH()} {self.fmtP0()}'
    def fmtBlnk(self):                        return f'{self.tblankCol=} {self.tblankRow=}'
    def fmtblnk(self):                        return f'{len(self.tblankCol)=} {len(self.tblankRow)=}'
    ####################################################################################################################################################################################################
    def fmtJText(self, j, i=None, why=''):
        jtxt = f'{JTEXTS[j] if 0 <= j < len(JTEXTS) else "???":4}'
        if i != 0 and i >= len(self.E[j]):   msg = f'ERROR {i=} >= {len(self.E[j])=} {j=} {why} {jtxt}'  ;  self.log(msg) # ;  self.quit(msg)
        return f'{i=} {j=} {why} {jtxt} {len(self.E[j])=}'
    ####################################################################################################################################################################################################
    @staticmethod
    def fmtTcolor(t):     k = ' '.join([ f'{k:3}' for k in t.color ])  ;  k += f' {t.opacity:3}'  if type(t) is pygsprt.Sprite else ''  ;   return k
    @staticmethod
    def fmtTfont(t):      return f'{t.dpi:3} {t.bold:1} {t.italic:1} {t.font_name}'
    @staticmethod
    def fmtTfontSize(t):  return F'{t.font_size:3.0f}'
    @staticmethod
    def fmtTsprite(s):    return f'{s.scale_x:5.3f} {s.scale_y:5.3f}'  # b.image.anchor_x, b.image.anchor_y, b.scale,  b.rotation, b.group, b.group.parent
    @staticmethod
    def fmtTvisible(t):   return 'Visible' if t.visible else '      '
    @staticmethod
    def fmtTxywh(t):      return f'{t.x:7.2f} {t.y:7.2f} {t.width:7.2f} {t.height:7.2f}'
    ####################################################################################################################################################################################################
    def dumpAXY(self):  self.log(f'{self.A_LEFT=} {self.A_CENTER=} {self.A_RIGHT=} {self.X_LEFT=} {self.X_CENTER=} {self.X_RIGHT=} {self.Y_TOP=} {self.Y_CENTER=} {self.Y_BOTTOM=} {self.Y_BASELINE=}', pfx=0, so=1)
    def fmtAxy(self):   return f'{self.a} {self.ax} {self.ay}'
    def dumpAxy(self):  self.log(f'{self.a=} {self.ax=} {self.ay=}')
    def dumpWxHp0(self): self.log(f'{self.fmtWxHP0()}')
    def dumpDataSlice(self, p, l, c, cc):
        for t in range(self.n[T]):
            ikeys = self.ikeys[cc+t].text if self.ikeys and len(self.ikeys) > cc+t else ''
            kords = self.kords[cc+t].text if self.kords and len(self.kords) > cc+t else ''
            self.log(f'{self.data[p][l][c]} [{cc+t}] {self.tabs[cc+t].text:2} {self.notes[cc+t].text:2} {ikeys:2} {kords:2}')
    @staticmethod
    def dumpObjs(objs, name, why=''):            [ Tabs.dumpObj(o, name, why) for o in objs ]
    @staticmethod
    def dumpObj( obj,  name, why='', file=None): util.slog(f'{why} {name} ObjId {id(obj):x} {type(obj)}', file=file)
    def dumpJs(  self, why):                     self.log(f'  J1={self.fmtJ1(0, 1)} {why}')   ;   self.log(f'  J2={self.fmtJ2(0, 1)} {why}')   ;   self.log(f'  LE={self.fmtLE(0)} {why}')
    def dumpGeom(self, why1='', why2=''):        self.log(f'{why1:4} {self.fmtDxD()} {self.fmtIxI()} {util.fmtl(self.ss2sl()):9} {self.LL} {util.fmtl(self.zz2sl()):5} {self.fmtn()} {why2}')
    def dumpSmap(self, why, pos=0):              self.log(f'{why} smap={util.fmtm(self.smap)}', pos=pos)
    def dumpBlank(self): self.log(f'{self.fmtblnk()} {self.fmtBlnk()}')
    ####################################################################################################################################################################################################
    def _initntp(self, dbg=1):
        ntp = self.ntp()  ;  self.tpc, self.tpl, self.tpp, self.tpf = ntp
        if dbg: self.log(f'{self.tpc=} {self.tpl=} {self.tpp=} {self.tpf=} ntp={util.fmtl(ntp)}')

    def ntp(self, d2=1, r2=0, dbg=0):
        d = 'dns' if d2 else '   '
        n = list(self.n)     ;   self.log(f'          n={self.fmtn("", n)}') if dbg else None
        if d2:   del n[2]    ;   self.log(f'        {d}={self.fmtn("", n)}') if dbg else None
        n.reverse()          ;   self.log(f'     {d}Rev={self.fmtn("", n)}') if dbg else None
        n = self.accProd(n)  ;   self.log(f' {d}RevProd={util.fmtl(n)}')     if dbg else None
        if r2: n.reverse()   ;   self.log(f'{d}Rev2Prod={self.fmtn("", n)}') if dbg else None
        return n
    @staticmethod
    def accProd(n):              return list(accumulate(n, operator.mul))
    ####################################################################################################################################################################################################
    def dumpStruct(self, why='', dbg=1):
        self.dumpFont(why)
        self.log(f'{self.fmtn()} ntp={util.fmtl(self.ntp())} ntp0={util.fmtl(self.ntp(0))}')
        if dbg:         self.dumpIdMap()
#        if dbg:         self.dumpTniks(why)
#        if dbg:         self.cobj.dumpMlimap(why)
    ####################################################################################################################################################################################################
    def autoSave(self, dt, why, dbg=1):
        if dbg: self.log(f'Every {dt:=7.4f} seconds, {why} {self.resyncData=}')
        if self.resyncData: self.saveDataFile(why, self.dataPath0)   ;  self.resyncData = 0
    ####################################################################################################################################################################################################
    def on_draw(self):
        pyglet.gl.glClearColor(1, 1, 1, 1)
        self.clear()
        self.batch.draw()
        if self.SNAPS and self.snapReg:
            self.snapReg = 0  ;  self.snapshot()
            self.log(f'{self.snapWhy=} {self.snapType=} {self.snapId=}')

    def on_resize(self, width, height, why=''):
        super().on_resize(width, height)   ;   why2 = 'Upd'
        if self.RESIZE: self.resizeTniks(f'{why2}{why}')
        self.dumpAxy()  ;  self.dumpAXY()
#        if dbg and self.SNAPS: self.regSnap(f'{why2}{why}', 'RSIZ')
    ####################################################################################################################################################################################################
    def saveDataFile(self, why, path, dbg=1):
        if dbg:   self.log(f'{why} {path}')
        with open(path, 'w') as DATA_FILE:
            self.log(f'{DATA_FILE.name:40}', pfx=0)
            if    self.isVert(): data = self.A_transposeData() if self.TRANSPOSE_A else self.OLD_transposeData()
            else:                data = self.data
            self.log(f'{self.fmtn()} {self.fmtdl(data)}')
            for p in range(len(data)):
                if dbg: self.log(f'writing {p+1}{util.ordSfx(p+1)} page', pfx=0)
                for l in range(len(data[p])):
                    if dbg: self.log(f'writing {l+1}{util.ordSfx(l+1)} line', pfx=0)  # if dbg  else  self.log(pfx=0)  if  l  else  None
                    for r in range(len(data[p][l])):
                        text = ''
                        for c in range(len(data[p][l][r])):
                            text += data[p][l][r][c]
                        if dbg: self.log(f'writing {r+1}{util.ordSfx(r+1)} string {text}', pfx=0)  # if dbg  else  self.log(text, pfx=0)
                        DATA_FILE.write(f'{text}\n')
                    DATA_FILE.write('\n')  #   if l < nl:
        size = path.stat().st_size   ;   self.log(f'{self.fmtn()} {self.fmtdl()} {size=}')
        return size
    ####################################################################################################################################################################################################
    def genDataFile(self, path):
        self.log(f'{path} {self.fmtn()}')
        np, nl, ns, nc, nr = self.n  ;  nc += self.zzl()
        self.dumpBlank()
        self.data = [ [ [ self.tblankRow for _ in range(nr) ] for _ in range(nl) ] for _ in range(np) ]
        size = self.saveDataFile('Generated Data', path)
        self.log(f'{path} {size=} {len(self.data)=}')
        self.data = []
        return size
   ####################################################################################################################################################################################################
    def readDataFile(self, path, dbg=1):
        nl = self.n[L]   ;   nr = self.n[T]   ;   sp, sl, st, sr = 0, 0, 0, 0
        if dbg:                             self.log(f'BGN {self.fmtn()}')
        if not path.exists():   self.log(f'WARN Invalid Data File Path {path} -> Touch Data File')   ;   path.touch()
        stat = path.stat()  ;   size = stat.st_size
        if size == 0:           self.log(f'WARN Zero Len Data File  {path} -> Generate Data File')   ;   size = self.genDataFile(path)
        if size == 0:           msg = f'ERROR Zero Len Data File {size=}'   ;   self.log(msg)   ;   self.quit(msg)
        with open(path, 'r') as DATA_FILE:
            DATA_FILE.seek(0, 2)      ;     size = DATA_FILE.tell()   ;   DATA_FILE.seek(0, 0)
            self.log(f'{DATA_FILE.name:40} {size:3,} bytes = {size/1024:3,.1f} KB')
            self.log('Raw Data File BGN:')
            data = self.data          ;     lines, rows = [], []      ;   ntabs = 0
            for tabs in DATA_FILE:
                tabs = tabs.strip('\n')
                if tabs:
                    if not ntabs: ntabs = len(tabs)
                    if len(tabs) != ntabs:      msg = f'ERROR BAD tabs len {len(tabs)=} != {ntabs=}'   ;   self.log(msg)   ;   self.quit(msg)
                    rows.append(tabs)       ;   st += len(tabs)       ;     sr += 1
                else:
                    if rows  and not (sr % nr): lines.append(rows)    ;    rows = []   ;   sl += 1
                    if lines and not (sl % nl): data.append(lines)    ;   lines = []   ;   sp += 1
                self.log(f'{tabs}', pfx=0)
            if rows:  lines.append(rows)    ;   sl += 1
            if lines: data.append(lines)    ;   sp += 1
            self.log('Raw Data File END:')
            self.log(f'{self.fmtdl()=} {self.fmtdt()=}')
            self.assertDataFileSize(sl, size)
            npages, nlines, nrows, ntabs = self.dl()
            self.log(f'{sp    } ({sl/nlines:6.3f}) pages = {sl} lines =          {sr} rows =          {st} tabs')
            self.log(f'{npages} ({sl/nlines:6.3f}) pages @  {nlines} lines per page, @ {nrows} rows per line, @ {ntabs} tabs per row')
            self.dumpDataFile(data)
#            self.log(f'    {nlines} lines, {nrows=} rows per line, {ntabs} tabs per row')

    def assertDataFileSize(self, nlines, ref):
        nt  = self.n[C]  ;  nr = self.n[T]  ;  crlf = 2
        dsize = nlines * nr * nt            ;  self.log(f'{dsize=:3,} = {nlines=:3,} *     {nr=:2} *   {nt=}')
        crlfs = nlines * (nr + 1) * crlf    ;  self.log(f'{crlfs=:3,} = {nlines=:3,} * {(nr+1)=:2} * {crlf=}')
        size  =  dsize + crlfs              ;  self.log(f' {size=:3,} =  {dsize=:3,} +  {crlfs=:3,}   {ref=}')
        assert size == ref, f'{size=:4,} == {ref=:4,}'

    def dumpDataFile(self, data=None):
        data = self.dproxy(data)
        d0, d1, d2, d3 = self.dl()
        self.log(f'BGN {d0} pages, {d1} lines per page, {d2} rows per line, {d3} tabs per line')
        for n0 in range(len(data)):
            for n1 in range(len(data[n0])):
                self.log(f'{util.fmtl(data[n0][n1], d1="")}', pfx=0)
            self.log(pfx=0)
        self.log(f'END {d0} pages, {d1} lines per page, {d2} rows per line, {d3} tabs per line')
    ####################################################################################################################################################################################################
    def isVert(self, data=None, dbg=1):
        dl, dt = self.dl(data), self.dt(data)
        if dbg: self.log(f'BGN dl={self.fmtdl()} dt={self.fmtdt()}')
        assert dt[0] is list and dt[1] is list and dt[2] is list and dt[3] is str, f'{dl=} {dt=}'
        vert = 1 if dl[2] > dl[3] else 0
        self.checkData(vert=vert, data=None)
        self.log(f'{util.fmtl(self.dplc()[0])}', pfx=0)
        if dbg: self.log(f'END dl={self.fmtdl()} dt={self.fmtdt()} {vert=}')
        return vert

    def checkData(self, vert, data=None):
        data = self.dproxy(data)   ;   dl = self.dl(data)
        for p in range(dl[0]):
            assert len(data[p]) == dl[1], f'{len(data[p])=} {dl=} {vert=}'
            for l in range(len(data[p])):
                assert len(data[p][l]) == dl[2], f'{len(data[p][l])=} {dl=} {vert=}'
                for c in range(len(data[p][l])):
                    assert len(data[p][l][c]) == dl[3], f'{len(data[p][l])=} {dl=} {vert=}'
    ####################################################################################################################################################################################################
    def transposeDataDump(self, data=None, why='External', dbg=1):
        self.dumpDataVert(data) if self.isVert(data) else self.dumpDataHorz(data)
        self.data = self.OLD_transposeData(data, why, dbg)
        self.dumpDataVert(data) if self.isVert(data) else self.dumpDataHorz(data)

    def OLD_transposeData(self, data=None, why='External', dbg=1):
        data = self.dproxy(data)
        Xdata, msg1, msg2 = [], [], []
        self.log(f'BGN {self.fmtDxD(data)} {why}')
        self.log(f'{self.fmtdl()} {self.fmtdt()}')
        self.log(f'dl={self.fmtdl(data)} dt={self.fmtdt(data)}') if dbg else None
        for p, page in enumerate(data):
            Xpage = []
            for l, line in enumerate(page):
                if dbg: msg1.append(f'{util.fmtl( line, d1="")}')
                Xline = list(map(''.join, itertools.zip_longest(*line, fillvalue=' ')))
                if dbg: msg2.append(f'{util.fmtl(Xline, d1="")}')
                Xpage.append(Xline)
            Xdata.append(Xpage)
        if dbg: [ self.log(m, pfx=0) for m in msg1 ]   ;   self.log(pfx=0)
        if dbg: [ self.log(m, pfx=0) for m in msg2 ]
        self.log(f'END {self.fmtDxD(Xdata)} {why}')
        return Xdata

    def A_transposeData(self, data=None, dump=0, dbg=1):
        data = self.dproxy(data)
        self.log(f'BGN {self.fmtDxD(data)} {dump=}')
        if dump:        self.dumpDataVert(data) if self.isVert(data) else self.dumpDataHorz(data)
        Xdata, msg1, msg2 = [], [], []
        self.log(f'dl={self.fmtdl()} dt={self.fmtdt()}')
        self.log(f'dl={self.fmtdl(data)} dt={self.fmtdt(data)}') if dbg else None
        for p, page in enumerate(data):
            Xpage = []
            for l, line in enumerate(page):
                if dbg: msg1.append(f'{util.fmtl( line, d1="")}')
                Xline = list(map(''.join, itertools.zip_longest(*line, fillvalue=' ')))
                if dbg: msg2.append(f'{util.fmtl(Xline, d1="")}')
                Xpage.append(Xline)
            Xdata.append(Xpage)
        if dbg: [ self.log(m, pfx=0) for m in msg1 ]   ;   self.log(pfx=0)
        if dbg: [ self.log(m, pfx=0) for m in msg2 ]
        self.dumpDataVert(Xdata) if self.isVert(Xdata) else self.dumpDataHorz(Xdata)
        self.log(f'END {self.fmtDxD(Xdata)} {dump=}')
        return Xdata
    ####################################################################################################################################################################################################
    def dumpDataHorz(self, data=None, lc=1, ll=1, i=0):
        data = data or self.data
        self.log(f'BGN {self.fmtDxD(data)} {lc=} {ll=} {i=}')
        for p in range(len(data)):
#            if ll:  plt = f'{JTEXTS[P]} {p+1}'  ;  plab = f'{plt:{i+1}}'  ;  self.log(f'{Z*i}{plab}', pfx=0)
            for l in range(len(data[p])):
                if ll:  llt = f'{JTEXTS[P]} {p+1}'  ;  llab = f'{llt:{i+1}} '  ;  self.log(f'{Z*i}{llab}', pfx=0, end='')   ;   self.log(f'{JTEXTS[L]} {l+1}', pfx=0)
#                if ll:  llt = f'{JTEXTS[L]} {l+1}'  ;  llab = f'{llt:{i+1}}'  ;  self.log(f'{Z*i}{llab}', pfx=0)
                if lc:  self.dumpDataLabels(data[p][l], i=i, sep=Z)
                for r in range(len(data[p][l])):
                    self.log(f'{Z*i}', pfx=0, end='')
                    for c in range(len(data[p][l][r])):
                        self.log(f'{data[p][l][r][c]}', pfx=0, end='')
                    self.log(pfx=0)
                self.log(pfx=0)
        self.log(f'END {self.fmtDxD(data)} {lc=} {ll=} {i=}')

    def dumpDataVert(self, data=None, lc=1, ll=1, i=0):
        data = data or self.data
        w = max(len(data[0][0][0]), len(JTEXTS[P]) + 2, len(JTEXTS[L]) + 2)   ;   txt = Z * i + JTEXTS[C] + Z if i >= 0 else JTEXTS[C]
        self.log(f'BGN {self.fmtDxD(data)} {lc=} {ll=} {i=} {w=} {txt=}')
        for p in range(len(data)):
            if ll: self.log(f'{JTEXTS[P]} {p+1}', pfx=0)  ;  self.log(f'{txt:{3}}', pfx=0, end='')  ;  txt2 = [ f'{JTEXTS[L]} {l+1}' for l in range(len(data[0])) ]  ;  self.log(f'{util.fmtl(txt2, w=w, d1="")}', pfx=0)
            for c in range(len(data[p][0])):
                pfx = f'{c+1:3} ' if i >= 0 and lc else ''   ;   self.log(f'{pfx}{Z*i}', pfx=0, end='')
                for l in range(len(data[p])):
                    self.log(f'{data[p][l][c]}', pfx=0, end=Z)
                self.log(pfx=0)
        self.log(f'END {self.fmtDxD(data)} {lc=} {ll=} {i=}')
    ####################################################################################################################################################################################################
    def dumpDataLabels(self, data=None, i=0, sep='%'):
        pp = '  '  ;  qq = ' @'   ;   lz = self.zzl()
        p = pp[:] if lz > 1 else pp[:1] if lz else ''
        q = qq[:] if lz > 1 else qq[:1] if lz else ''
        data = data or self.data
        n = len(data[0]) - lz   ;   a = ' ' * i if i else ''  ;  b = sep * n  ;  r = sep * 3
        if n >= 100:   self.log(   f'{a}{p}', pfx=0, end='')  ;  [  self.log(f'{c//100}'   if c>=100 else ' ', pfx=0, end='') for c in range(1, n+1) ]  ;  self.log(pfx=0)
        if n >= 10:    self.log(   f'{a}{p}', pfx=0, end='')  ;  [  self.log(f'{c//10%10}' if c>=10  else ' ', pfx=0, end='') for c in range(1, n+1) ]  ;  self.log(pfx=0)
        self.log(                  f'{a}{q}', pfx=0, end='')  ;  [  self.log(f'{c%10}',                        pfx=0, end='') for c in range(1, n+1) ]  ;  self.log(pfx=0)
        if sep != '':  self.log(f'{a}{r}{b}', pfx=0)
    ####################################################################################################################################################################################################
    def createLabelText(self):
        self.labelTextA.extend(f'{j}' for j in range(1, self.n[C] + 1))
        self.labelTextB.extend(f'{j%10}' if j % 10 else f'{j // 10 % 10}' for j in range(1, self.n[C] + 1))
        self.log(f'labelTextA={util.fmtl(self.labelTextA)}', pfx=0)
        self.log(f'labelTextB={util.fmtl(self.labelTextB)}', pfx=0)
        texts = list(zip(self.labelTextA, self.labelTextB))
        self.log(f'texts={util.fmtl(texts)}', pfx=0)
        self.dumpLabelText(texts)

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
    ####################################################################################################################################################################################################
    def toggleTTs(self, how, tt):
        msg2 = f'{how} {tt=}'
        self.dumpGeom(f'BGN', f'     {msg2}')
        if   tt not in self.SS and not self.B[tt]: msg = 'ADD'    ;   self.addTTs( how, tt)
        elif tt     in self.SS:                    msg = 'HIDE'   ;   self.hideTTs(how, tt)
        else:                                      msg = 'SKIP'   ;   self.dumpGeom('   ', f'{msg} {msg2}')   ;   self.toggleTT(tt)
        self.on_resize(self.width, self.height, why='S')
        self.dumpGeom('END', f'{msg} {msg2}')

    def toggleLLs(self, how, dbg=1):
        self.toggleLL()
        msg2 = f'{how} {self.LL=}'
        self.dumpGeom('BGN', f'     {msg2}')
        if dbg: self.log(f'    llText={util.fmtl(self.llText[1-self.zzl():])}')
        if self.LL and not self.lrows: msg = 'ADD'    ;   self.addLLs( how)
        else:                          msg = 'HIDE'   ;   self.hideLLs(how)
        self.on_resize(self.width, self.height)
        self.dumpGeom('END', f'{msg} {msg2}')

    def toggleZZs(self, how, zz):
        ii = 0 if not zz else 2
        msg2 = f'{how} {zz=}'
        self.dumpGeom('BGN', f'     {msg2}')
        if   zz not in self.ZZ and not self.D[ii]: msg = 'ADD'    ;   self.NEW__addZZs(how, zz)
        elif zz     in self.ZZ:                    msg = 'HIDE'   ;   self.hideZZs(how, zz)
        else:                                      msg = 'SKIP'   ;   self.dumpGeom('   ', f'{msg} {msg2}')   ;   self.toggleZZ(zz)
        self.on_resize(self.width, self.height)
        self.dumpGeom('END', f'{msg} {msg2}')
    ####################################################################################################################################################################################################
    def toggleZZ(self, zz, why=''):
        self.dumpGeom('BFR', why)
        self.ZZ.add(zz) if zz not in self.ZZ else self.ZZ.remove(zz)
        n = self.n[C] + self.zzl()
        self.dumpGeom('AFT', why)
        return n

    def toggleTT(self, tt, why=''):
        self.dumpGeom('BFR', why)
        self.SS.add(tt) if tt not in self.SS else self.SS.remove(tt)
        self.n[S] = self.ssl()
        self.dumpGeom('AFT', why)

    def toggleLL(self, why=''):
        self.dumpGeom('BFR', why)
        self.LL = int(not self.LL)
        self.dumpGeom('AFT', why)
    ####################################################################################################################################################################################################
    def hideTTs(self, how, ii, dbg=1):
        why = f'HIDE {how} {ii=}'  ;  why2 = 'Ref'
        np, nl, ns, nc, nt = self.n   ;   nc += self.zzl()
        self.dumpTniksPfx(why)
        for p in range(np):
            self.setJdump(P, p, why2)
            for l in range(nl):
                self.setJdump(L, l, why2)
                for s, s2 in   enumerate(self.ss2sl()):
                    if s2 != ii:         self.setJdump(S, s2, why2)
                    else:                self.hideTnik(self.sects,   p*nl + l,            S, dbg=dbg)
                    for c in range(nc):
                        if s2 != ii:     self.setJdump(C, c,why2)
                        else:            self.hideTnik(self.cols,   (p*nl + l)*nc + c,    C, dbg=dbg)
                        for t in range(nt):
                            tlist, j  =  self.tnikInfo(p, l, s2, c)
                            if s2 != ii: self.setJdump(j, t, why2)
                            else:        self.hideTnik(tlist, ((p*nl + l)*nc + c)*nt + t, j, dbg=dbg)
        if ii == TT:                     self.hideTnik(self.cursr,                     0, H, dbg=dbg)
        self.dumpTniksSfx(why)
        self.toggleTT(ii)

    def hideLLs(self, how):
        msg = f'HIDE {how}'
        nr = len(self.lrows)                    ;  nc = len(self.lcols)
        assert not nc % nr, f'{nc=} {nr=}'      ;  nc = nc // nr  #  normalize
        self.dumpTniksPfx(msg)
        for r in range(nr):
            self.hideTnik(self.lrows, r, R)
            for c in range(nc):
                self.hideTnik(self.lcols, c + r*nc, Q)
        self.dumpTniksSfx(msg)
    ####################################################################################################################################################################################################
    def addZZs(self, how, ii):
        why = f'ADD {how} {ii=}'  ;  why2 = 'Ref'
        self.toggleZZ(ii)
        np, nl, ns, nc, nt = self.n   ;   zz = self.zz2sl()
        self.dumpTniksPfx(why)
        for p in range(np):
            self.setJdump(P, p, why2)
            for l in range(nl):
                self.setJdump(L, l, why2)
                for s, s2 in enumerate(self.ss2sl()):
                    self.setJdump(S, s2, why2)
                    for c in zz:
                        if   c == ii:   self.addZZ(p, l, s, c, c)
                        else:           self.OLD__refZZ(p, l, s, c, c)
                    for c in range(nc): self.OLD__refZZ(p, l, s, c)
        self.dumpTniksSfx(why)

    def NEW__addZZs(self, how, ii):
        why = f'ADD {how} {ii=}'      ;   why1, why2 = 'Ref1', 'Ref2'
        np, nl, ns, nc, nt = self.n   ;   zz = self.zz2sl()
        n = self.toggleZZ(ii)
        self.dumpTniksPfx(why)
        for v, view in enumerate(self.views):
            self.dumpTnik(view, V, why1)
            self.splitH(view, n)
            self.dumpTnik(view, V, why2)
            for p in range(np):
                self.setJdump(P, p, why2)
                for l in range(nl):
                    self.setJdump(L, l, why2)
                    for s, s2 in enumerate(self.ss2sl()):
                        self.setJdump(S, s2, why2)
                        for c in zz:
                            if c == ii:     self.addZZ(p, l, s, c, c)
                            else:           self.OLD__refZZ(p, l, s, c, c)
                        for c in range(nc): self.OLD__refZZ(p, l, s, c)
        self.dumpTniksSfx(why)
    ####################################################################################################################################################################################################
    def addZZ(self, p, l, s, c, ii):
        np, nl, ns, nc, nt = self.n    ;   zzl = self.zzl()   ;   nc += zzl
        z1 = self.z1(c)   ;   z2 = self.z2(c)
        self.log(f'ii={ii} j={C} {JTEXTS[C]:4} nc={nc}      ltl={len(self.cols)} plsc =[{p} {l} {s} {c}  ] J1={self.fmtJ1(0, 1)} J2={self.fmtJ2(0, 1)} z1={z1} z2={z2}', so=1)
        for col in self.g_createTniks(None, C, self.sects[s], ii=ii):
            c2 = c + nc*(s + ns*(l + nl*p))
            self.cols.insert(c2, col)
            if self.LL and self.isV(C) and not s:
                n, _, x, y, w, h = self.geom(C, self.lrows[l], 1)
                lrCol = self.addLL(None, c, x, y, w, h)
                self.lcols.insert(c2, lrCol)
#                msg = f'WARN not tested'   ;   self.log(msg)   ;   self.quit(msg)
            p, l, c, t = self.j2plct()
            tlist, j, kk, txt = self.tnikInfo(p, l, s, c, t)
            self.log(f'ii={ii} j={j} {JTEXTS[j]:4} nc={nc} c2={c2} ltl={len(tlist)} plsc =[{p} {l} {s} {c}  ] J1={self.fmtJ1(0, 1)} J2={self.fmtJ2(0, 1)} z1={z1} z2={z2}', so=1)
            for t, _ in enumerate(self.g_createTniks(self.tabs, T, col, ii=s)):
                self.log(f'ii={ii} j={j} {JTEXTS[j]:4} nc={nc} c2={c2} ltl={len(tlist)} plsct=[{p} {l} {s} {c} {t}] J1={self.fmtJ1(0, 1)} J2={self.fmtJ2(0, 1)} z1={z1} z2={z2}', so=1)

    def OLD__refZZ(self, p, l, s, c, zz=None):
        np, nl, ns, nc, nt = self.n   ;   why = 'Ref'
        self.setJdump(C, c, why)
#            self.setJ(C, c3)
#            self.dumpTnik(self.cols[c3], C, why2)
        tlist, j = self.tnikInfo(p, l, s, c) #s, zz)
        self.log(f'zz={zz} j={C} {JTEXTS[C]:4} nc={nc}       ltl={len(tlist)} plsc =[{p} {l} {s} {c}  ] J1={self.fmtJ1(0, 1)} J2={self.fmtJ2(0, 1)} z1={self.z1(c)} z2={self.z2(c)}', so=1)
        for t in range(nt):
            t2 = t + nt*(c + nc*(s + ns*(l + nl*p))) if j <= K else t
#                self.setJdump(j2, t, why2)
            self.setJ(j, t2)
            self.dumpTnik(tlist[t2], j, why)
            self.log(f'zz={zz} j={j} {JTEXTS[j]:4} nc={nc} t2={t2} ltl={len(tlist)} plsct=[{p} {l} {s} {c} {t}] J1={self.fmtJ1(0, 1)} J2={self.fmtJ2(0, 1)}', so=1)
    ####################################################################################################################################################################################################
    def OLD__hideZZs(self, how, ii, dbg=1):
        why = f'HIDE {how} ii={ii}'  ;   why2 = 'Ref'  # ;  c2, t2 = 0, 0
        self.toggleZZ(ii)
        np, nl, ns, nc, nt = self.n   ;    nc += self.zzl()   ;   ns = self.ssl()
        self.dumpTniksPfx(why)
        for p in range(np):
            self.setJdump(P, p, why2)
            for l in range(nl):
                self.setJdump(L, l, why2)
                for s, s2 in enumerate(self.ss2sl()):
                    self.setJdump(S, s2, why2)
                    for c in range(nc):
                        if c in self.ZZ:
                            tlist, j = self.OLD__tnikInfo(s2, c)   ;   z1 = self.z1()   ;   z2 = self.z2()
                            c2 = ((p * nl + l) * ns + s) * nc + c
                            self.log(f'  ii={ii} s={s} s2={s2} c={c} c2={c2} z1={z1} z2={z2} J1={self.fmtJ1()} J2={self.fmtJ2()}')
                            self.hideTnik(self.cols, c2, C, dbg=dbg)
                            for t in range(nt):
                                self.hideTnik(tlist, self.J1[j], j, dbg=dbg)
                        else:
                            tlist, j = self.OLD__tnikInfo(s2, c)   ;   z1 = self.z1()   ;   z2 = self.z2()
                            self.log(f'  ii={ii} s={s} s2={s2} c={c}     z1={z1} z2={z2} J1={self.fmtJ1()} J2={self.fmtJ2()}')
                            self.setJdump(C, c, why2)
                            for t in range(nt):
#                                self.setJdump(j, t, why2)
                                self.setJ(j, t + c * nt)
                                self.dumpTnik(tlist[t + c * nt], j, why2)
        self.dumpTniksSfx(why)
    ####################################################################################################################################################################################################
    def addTTs(self, how, ii):
        why = f'ADD {how} {ii=}'  ;  why2 = 'Ref'
        self.toggleTT(ii)
        np, nl, ns, nc, nt = self.n   ;   nc += self.zzl()
        self.dumpTniksPfx(why)
        for p in range(np):
            self.setJdump(P, p, why2)
            for l in range(nl):
                self.setJdump(L, l, why2)
                for s in self.ss2sl():
                    if s == ii:
                        for sect in      self.g_createTniks(self.sects, S, self.lines[l], ii=ii):
                            for col in   self.g_createTniks(self.cols,  C, sect):
                                for _ in self.g_createTniks(self.tabs,  T, col, ii=ii):
                                    pass
                    else:
                        self.setJdump(S, s, why2)
                        for c in range(nc):
                            self.setJdump(C,  c, why2)
                            for t in range(nt):
                                tlist, j = self.tnikInfo(p, l, s, c, why=why2)
                                self.setJ(j, t)
                                self.dumpTnik(tlist[t], j, why2)
        self.dumpTniksSfx(why)
        if self.tabs and not self.cursor: self.createCursor()

    def addLLs(self, how):
        why = f'ADD {how}'  ;  why2 = 'Ref'
        np, nl = self.n[P], self.n[L]
        self.dumpTniksPfx(why)
        for p in range(np):
            self.setJdump(P, p, why2)
            if self.isV(P):
                for l in range(nl):
                    i = p * nl + l
                    self.setJdump(L, l, why2)
                    self.createLL(self.lines[i], i)
        self.dumpTniksPfx(why)
    ####################################################################################################################################################################################################
    def addLL(self, tlist, c, x, y, w, h, dbg=1):
        l = self.zzl()  ;  kk = NORMAL_STYLE  ;  kl = self.llcolor(c, Q)  # kl = self.k[Q]
        z = 1 if self.FRET_BOARD else 2
        text = self.llText[z-l:]
        txt = text[c]
        return self.createTnik(tlist, c, Q, x + c * w, y, w, h, kk=kk, kl=kl, v=1, t=txt, dbg=dbg)

    def addPage(self, how, dbg=1):
        self.log(f'BGN {how}')
        np, nl, ns, nr, nc = self.n   ;   nc += self.zzl()
        self.n[P] += 1   ;   kl = self.k[P]
        self.log(f'{self.fmtn()}')   ;   self.dumpBlank()
        data = [ [ self.tblankRow for _ in range(nc) ] for _ in range(nl) ]
        self.data = self.A_transposeData(dump=dbg) if self.TRANSPOSE_A else self.OLD_transposeData()
        self.data.append(data)
        self.data = self.A_transposeData(dump=dbg) if self.TRANSPOSE_A else self.OLD_transposeData()
        self.dumpTniksPfx(how)
        if self.VIEWS:
            if      not   self.views:    msg = f'ERROR Empty views {self.n=} {self.zzl()}'   ;   self.log(msg)   ;   self.quit(msg)
            self.dumpTnik(self.views[0], V, 'RefP')
        n, ii, x, y, w, h =    self.geom(V, n=1, i=1, dbg=1)
        page = self.createTnik(self.pages,    len(self.pages), P, x, y, w, h, self.cci(P, 0, kl), kl=kl, dbg=1)
        for line in            self.g_createTniks(self.lines,  L, page):
            for sect in        self.g_createTniks(self.sects,  S, line):
                for col in     self.g_createTniks(self.cols,   C, sect):
                    for _ in   self.g_createTniks(self.tabs,   T, col):
                        pass
        self.dumpTniksSfx(how)
        self.log(f'END {how}')
    ####################################################################################################################################################################################################
    def splitH( self, p, n, dbg=1):
        if   type(p) is pygtxt.Label:
            p.x,  p.width,  self.p0x, self.p0w = self.splitHL(p.x, p.width, n)
            if dbg:       self.log(f'{p.x=:.2f} {p.width=:.2f} {n=} {self.p0x=:.2f} {self.p0w=:.2f}')
        elif type(p) is pygsprt.Sprite:
            p.x, p.scale_x, self.p0x, self.p0w = self.splitHS(p.x, p.width, n, p.image.width)
            if dbg:   self.log(f'{p.x=:.2f} {p.scale_x=:.4f} {n=} {self.p0x=:.2f} {self.p0w=:.2f} {self.p0sx=:.4f}')

    def splitHL(self, x, w, n):
        x0 = x                     ;   w0 = w
        w2 = w/n                   ;   w -= w2
        x = w2 + w2/2 + w/2        ;   x2 = w2
        self.log(f'{x0=:6.2f} {w0=:6.2f} {n=} {x=:6.2f} {w=:6.2f} {x2=:6.2f} {w2=:6.2f}')
        return x, w, x2, w2

    def splitHS(self, x, w, n, s):
        x0 = x      ;   w0 = w     ;   s0 = s
        w2 = w/n    ;   w -= w2    ;   s  = w/s0
        x = w2 + w2/2 + w/2        ;   x2 = w2
        self.log(f'{x0=:6.2f} {w0=:6.2f} {s0=:6.4f} {n=} {x=:6.2f} {w=:6.2f} {s=:6.4f} {x2=:6.2f} {w2=:6.2f}')
        return x, s, x2, w2
    ####################################################################################################################################################################################################
    def splitV(self, p, a, dbg=0):
        if   type(p) is pygtxt.Label:   p.y, p.height, g     = self.splitV1(p.y, p.height, a)                  ;  self.log(f'{p.y=:6.2f} {p.height=:6.2f} {a=} {g=:6.2f}', file=LF2) if dbg else None
        elif type(p) is pygsprt.Sprite: p.y, h, g, p.scale_y = self.splitV2(p.y, p.height, a, p.image.height)  ;  self.log(f'{p.y=:6.2f} {p.scale_y=:6.4f} {a=} {h=:6.2f}', file=LF2) if dbg else None

    def splitV1(self, y, h, a, dbg=1):
        self.log(f'{y=:6.2f} {h=:6.2f} {a=}', end=' ', file=LF2) if dbg else None
        c = h/a  ;  h -= c  ;  y -= c/2 ;  self.log(f'{y=:6.2f} {h=:6.2f} {a=} {c=:6.2f}', pfx=0, file=LF2) if dbg else None  ;  return y, h, c

    def splitV2(self, y, h, a, g, dbg=1):
        self.log(f'{y=:6.2f} {h=:6.2f} {a=} {g=:6.4f}', end=' ', file=LF2) if dbg else None
        c = h/a  ;  h -= c  ;  g = h/g  ;  self.log(f'{y=:6.2f} {h=:6.2f} {a=} {c=:6.2f} {g=:6.4f}', pfx=0, file=LF2)  if dbg else None  ;  return y, h, c, g

#    def sprite2LabelPos(self, x, y, w, h, dbg=0): x0 = x  ;  y0 = y  ;  x += w/2  ;  y -= h/2  ;  self.log(f'{x0=:6.2f} {y0=:6.2f}, {w/2=:6.2f} {-h/2=:6.2f}, {x=:6.2f} {y=:6.2f} {self.p0x=:6.2f} {self.p0y=:6.2f}', file=LF2) if dbg else None  ;  return x, y
    ####################################################################################################################################################################################################
    def idmapkey(self, j):    return f'{JTEXTS[j]:4} {self.J2[j]:4}'
    def dumpIdMap(self):
        self.log(' Key  Cnt       ', pfx=0)
        for k, v in self.idmap.items():
            tid, t = v[0], v[1]
            if   type(t) is pygsprt.Sprite: msg = f'visible' if t.visible else '       '
            elif type(t) is pygtxt.Label:   msg = f'{t.font_size:3} {t.text}'
            else:                    msg = f'ERROR not a TNIK {type(t)=}'
            self.log(f'{k:9} {tid:x} {t.x:7.2f} {t.y:7.2f} {t.width:7.2f} {t.height:7.2f} {msg}', pfx=0)
    ####################################################################################################################################################################################################
    def isV( self, j, dbg=0):
        v = 1 if self.J2[P] == self.i[P] else 0
        if dbg: self.log(f'{self.fmtJText(j, why="isV()")} {self.J2[P]=} {self.i[P]=} {self.J2[j]=} i[]={self.fmtIxI()} v={v}', file=LF2)
        return v
    def j2plct(self, p=None, l=None, c=None, t=None):
        np, nl, ns, nc, nt = self.n   ;   n = 0
        if p is None: p = self.J1[P]
        if l is None: l = self.J1[L]
        if c is None: c = self.J1[C]
        if t is None: t = self.J1[T]
        t2 = n + t
        c2 = t2 // nt + c
        l2 = c2 // nc + l
        p2 = l2 // nl + p
        return p2 % np, l2 % nl, c2 % nc, t2 % nt
    ####################################################################################################################################################################################################
    def z1(self, c=None):    return None if c is None else C1 if C1 in self.ZZ and c == C1 else C2 if C2 in self.ZZ and c == C1 else None
    def z2(self, c=None):    return None if c is None else C2 if C2 in self.ZZ and c == C2 else None
    ####################################################################################################################################################################################################
    def tnikInfo(self, p, l, s, c, t=None, why='', dbg=0):
        tlist, j, k, txt = None, -1, None, None   ;   z1, z2 = self.z1(c), self.z2(c)
        exp1 = z1 == C1   ;  exp2 = z1 == C2 or z2 == C2
        msg1 = f'plsct=[{p} {l} {s} {c} {t}] {z1=} {z2=} {exp1=} {exp2=} {txt=} {why}'
        msg2 = f'ERROR {s=} is Invalid:'
        msg3 = f'ERROR {t=} is Invalid:'
        if t is None:
            if   s == TT:  tlist, j = (self.snos, O) if exp1 else (self.capos, D) if exp2 else (self.tabs,  T)
            elif s == NN:  tlist, j = (self.snas, A) if exp1 else (self.capos, D) if exp2 else (self.notes, N)
            elif s == II:  tlist, j = (self.snos, O) if exp1 else (self.capos, D) if exp2 else (self.ikeys, I)
            elif s == KK:  tlist, j = (self.snas, A) if exp1 else (self.capos, D) if exp2 else (self.kords, K)
            else:   msg = f'{msg2} {msg1}'   ;    self.log(msg)   ;   self.quit(msg) # f'{self.fmtJText(j, why=why)}'
            if dbg: msg =        f'{msg1}'   ;    self.log(msg, so=1) # self.fmtJText(j, why=why)
            return  tlist, j
        elif 0 <= t < self.n[T]:
            kT, kN, kI, kK = self.k[T], self.k[N], self.k[I], self.k[K]   ;   kO, kA, kD = self.k[O], self.k[A], self.k[D]
            tab = self.data[p][l][c][t]  # if C1 != z1 != C2 and C2 != z2 else ''
            if   s == TT:  tlist, j, k, txt = (self.snos, O, kO, self.sobj.stringNumbs[t]) if exp1 else (self.capos, D, kD, self.sobj.stringCapo[t]) if exp2 else (self.tabs,  T, kT, tab)
            elif s == NN:  tlist, j, k, txt = (self.snas, A, kA, self.sobj.stringNames[t]) if exp1 else (self.capos, D, kD, self.sobj.stringCapo[t]) if exp2 else (self.notes, N, kN, tab)
            elif s == II:  tlist, j, k, txt = (self.snos, O, kO, self.sobj.stringNumbs[t]) if exp1 else (self.capos, D, kD, self.sobj.stringCapo[t]) if exp2 else (self.ikeys, I, kI, tab)
            elif s == KK:  tlist, j, k, txt = (self.snas, A, kA, self.sobj.stringNames[t]) if exp1 else (self.capos, D, kD, self.sobj.stringCapo[t]) if exp2 else (self.kords, K, kK, tab)
            else:   msg = f'{msg2} {msg1}'   ;    self.log(msg)   ;   self.quit(msg) # self.fmtJText(j, t, why)
            if dbg: msg =        f'{msg1}'   ;    self.log(msg, so=1) # self.fmtJText(j, t, why)
            return  tlist, j, k, txt
        else:       msg = f'{msg3} {msg1}'   ;    self.log(msg)   ;   self.quit(msg) # self.fmtJText(j, t, why)
    ####################################################################################################################################################################################################
    def geom(self, j, p=None, n=None, i=None, dbg=0):
        if j is None or 0 > j >= len(JTEXTS): msg = f'ERROR j is BAD {j=} {len(JTEXTS)=} {n=} {i=} {type(p)=}'  ;  self.log(msg)  ;  self.quit(msg)
        n = n if n is not None else self.n[j]  #  ;  n += self.zzl() if j == C else 0
        i = i if i is not None else self.i[j]
        if   p is None:        w  =  self.width - self.p0w  ;  h  =  self.height
        elif j == C or j == Q: w  =  p.width/n              ;  h  =  p.height
        else:                  w  =  p.width                ;  h  =  p.height/n   if j != P else p.height
        if self.SPRITES:
            if   p is None: x  =  0                         ;  y  =  self.height - h
            elif j == Q:    x  =  p.x + w/2                 ;  y  =  p.y + p.height - h/2
            elif j == T:    x  =  p.x + w/2                 ;  y  =  p.y + p.height - h/2
            else:           x  =  p.x                       ;  y  =  p.y + p.height - h
        else:
            if   p is None: x  =  w/2                       ;  y  =  self.height - h/2
            elif j == Q:    x  =  w/2                       ;  y  =  p.y
            elif j == C:    x  =  w/2                       ;  y  =  p.y
            elif j == T:    x  =  p.x                       ;  y  =  p.y + p.height/2 - h/2
            else:           x  =  w/2                       ;  y  =  p.y + p.height/2 - h/2
        if dbg:
            msg  = f'{j=:2} {JTEXTS[j]:4} {n=:2} {x:7.2f} {y:7.2f} {w:7.2f} {h:7.2f}'
            (px, py, pw, ph) = (p.x, p.y, p.width, p.height) if p else (0.0, 0.0, 0.0, 0.0)
            msg2 = f' : {px:7.2f} {py:7.2f} {pw:7.2f} {ph:7.2f}'  ;  msg += msg2 if p else " " * len(msg2)
            self.log(f'{msg} {self.fmtJ1(0, 1)} {self.fmtJ2(0, 1)}', pfx=0, file=LF2)
        return n, i, x, y, w, h
    ####################################################################################################################################################################################################
    def imap2ikey(self, tobj, imap, i, j, dbg=0):
        imap0 = imap[0][::-1] if imap and len(imap) else []
        ff = self.sobj.isFret(tobj)
        if imap0 and len(imap0) > i:                ikey = tobj if j > K else imap0[i] if ff else self.tblank   # ;   i += 1 if ff else 0
        else:                                       ikey = tobj if j > K else self.tblank
        if dbg: self.log(f'{ikey=}')
        return ikey

    def imap2Chord(self, tobj, imap, i, j, dbg=0):
        chunks = imap[4]  if (imap and len(imap) > 4) else []
        chordName  = tobj if j > K else chunks[i] if len(chunks) > i else self.tblank
        if dbg: self.log(f'{chordName=}')
        return chordName
    ####################################################################################################################################################################################################
    def createLL(self, p, pi, dbg=1, dbg2=1):
        klr = self.k[R]   ;   kkr = self.cci(R, pi, klr) if self.CHECKERED else 0
        n = 1 + self.n[T] * self.ssl() * self.i[L]
        nr, ir, xr, yr, wr, hr = self.geom(R, p, n, self.i[L], dbg=dbg2) #  ;   xr0 = xr
        lrow = self.createTnik(self.lrows, pi, R, xr, yr, wr, hr, kkr, kl=klr, dbg=dbg)
        nc, ic, xc, yc, wc, hc = self.geom(Q, lrow, self.n[C], self.i[C], dbg=dbg2) #  ;   xc0 = xc
        for c in range(nc):
            self.addLL(self.lcols, c, xc, yc, wc, hc)
        self.splitV(p, n, dbg=dbg2)
        self.dumpTnik(p, L, why='Upd')
        return p

    def resizeLL(self, p, dbg=1, dbg2=1):
        n = 1 + self.n[T] * self.ssl() * self.i[L]
        nr, ir, xr, yr, wr, hr = self.geom(R, p, n, self.i[L], dbg=dbg2)  # ;    xr0 = xr
        lrow = self.resizeTnik(self.lrows, self.J2[R], R, xr, yr, wr, hr, dbg=dbg)
        nc, ic, xc, yc, wc, hc = self.geom(Q, lrow, self.n[C], self.i[C], dbg=dbg2)  # ;    xc0 = xc
        for c in range(nc):
            self.resizeTnik(self.lcols, self.J2[Q], Q, xc + c * wc, yc, wc, hc, v=1, dbg=dbg)
        self.splitV(p, n, dbg=dbg2)
        return p
    ####################################################################################################################################################################################################
    def createTniks(self):
        self.dumpTniksPfx()   ;   view = None
        if self.VIEWS:
            _, _, x, y, w, h = self.geom(V, n=1, i=1, dbg=0)  #  0, self.height, self.width, self.height
            view = self.createTnik(self.views, 0, V, x, y, w, h, why="New", v=1, dbg=1)
        for page in              self.g_createTniks(self.pages, P, view): # pass
            for line in          self.g_createTniks(self.lines, L, page): # pass
                for sect in      self.g_createTniks(self.sects, S, line): # pass
                    for col in   self.g_createTniks(self.cols,  C, sect): # pass
                        for _ in self.g_createTniks(self.tabs,  T, col):   pass
        if self.tabs: self.createCursor()
        self.dumpTniksSfx()
    ####################################################################################################################################################################################################
    def g_createTniks(self, tlist, j, pt, ii=-1, why='New', dbg=1, dbg2=1):
        n, _, x, y, w, h = self.geom(j, pt, dbg=dbg2)
        kl = self.k[j]     ;   tlist2 = tlist   ;   j2 = j   ;   i2 = 0   ;   x2 = x   ;   y2 = y  ;  text = ''
        n = 1 if ii >= 0 and (j == S or j == C) else n
        p, l, c, _ = self.j2plct()              ;   np, nl = self.dl()[0], self.dl()[1]
        for i in range(n):
            if self.DBG_TAB_TEXT:                      dlm = '\n' if j == C else ''  ;  text = f'{JTEXTS[j][0]}{dlm}{self.lenE()[-1]}'
            if   j == C:                                x2 = x + i * w
            else:
                if   j != P:                            y2 = y - i * h
                if   j == L and self.J2[L] >= np * nl: msg = f'WARN MAX Line {self.J2[L]=} >= {np=} * {nl=}'     ;  self.log(msg)  ;  self.quit(msg)  # yield None
                if   j == S:                             _ = self.ss2sl()[i] if ii < 0 else ii  ;  self.SS.add(_)
                elif j >= T:
                    s = self.ss2sl()[self.J1[S]] if ii  <  0 else ii
                    imap = self.getImap(p, l, c)  if s >= II else []
                    tlist2, j2, kl, tobj = self.tnikInfo(p, l, s, c, i, why)
                    if   s == TT:                     text = tobj
                    elif s == NN:                     text = tobj if j2 > K else self.sobj.tab2nn(tobj, i) if self.sobj.isFret(tobj) else self.tblank
                    elif s == II:                     text = self.imap2ikey( tobj, imap, i2, j2)   ;   i2 += 1 if text != self.tblank else 0
                    elif s == KK:                     text = self.imap2Chord(tobj, imap, i,  j2)
            k = self.cci(j2, i, kl) if self.CHECKERED else 0
            tnik = self.createTnik(tlist2, i if ii < 0 else ii, j2, x2, y2, w, h, k, kl=kl, t=text, dbg=dbg)
            yield tnik
    ####################################################################################################################################################################################################
    def createTnik(self, tlist, i, j, x, y, w, h, kk=0, kl=None, why='New', t='', v=None, g=None, dbg=0):
        if j is not None: self.setJ(j, i)
        o, k2, d, ii, n, s = self.fontParams()   ;   b = self.batch   ;   k0 = 0
        k = kl[kk]   if kl is not None else FONT_COLORS[(k2 + k0) % len(FONT_COLORS)]
        v = v        if  v is not None else self.isV(j)
        g = g        if  g is not None else self.j2g(j)
        if j == H or (self.SPRITES and (j < T or j == R)):
            scip  = pyglet.image.SolidColorImagePattern(k)
            img   = scip.create_image(width=fri(w), height=fri(h))
            tnik  = pygsprt.Sprite(img, x, y, batch=b, group=g, subpixel=self.SUBPIX)
            tnik.color, tnik.opacity = k[:3], k[3]   ;   tnik.visible = v
        else:
            s         = v * self.calcFontSize(t, w, h, j)
            d, n      = FONT_DPIS[d], FONT_NAMES[n]   ;   ml = self.MULTI_LINE
            a, ax, ay = self.a, self.ax, self.ay  # left center right  # bottom baseline center top
            tnik = pygtxt.Label(t, font_name=n, font_size=s, bold=o, stretch=1, italic=ii, color=k, x=x, y=y, width=w, height=h, anchor_x=ax, anchor_y=ay, align=a, dpi=d, batch=b, group=g, multiline=ml)
            if T <= j <= K:
                d = tnik.document  ;  d.set_style(0, len(d.text), {'color': self.k[j][1], 'background_color': self.k[j][0]})
                for i, c in enumerate(d.text):
                    if self.isEHC(c):
                        d.set_style(i, i+1, {'baseline': h/3, 'font_size': 0.5*s, 'color': (255, 0, 0, 255)})
        if    tlist is not None:     tlist.append(tnik)
        else:                        msg = f'WARN tlist is None cant add tnik: {self.fmtJText(j, i, why)}'  ;  self.log(msg)
        if dbg: key = self.idmapkey(j)  ;  self.idmap[key] = (id(tnik), tnik)  ;  self.dumpTnik(tnik, j, why)
        if self.LL and j == L and v: tnik = self.createLL(tnik, i)
        return tnik
    ####################################################################################################################################################################################################
    @staticmethod
    def isEHC(c): return 1 if c == '#' or c == 'b' else 0
    def llcolor(self, i, j, dbg=0):
        c = self.n[C]  ;   n = 1
        mp = i % c + n
        msg = f'{i=} {j=} {c=} {i%c=} {n=} {mp=}=i%c+n {mp%10=}' if dbg else ''
        if j == Q and not mp % 10 and i:
            self.log(  f'if   {msg} {self.k[R]=}') if dbg else None   ;   return self.k[R]
        else: self.log(f'else {msg} {self.k[j]=}') if dbg else None   ;   return self.k[j]

    def hideTnik(self, tlist, i, j, dbg=0): # AssertionError: When the parameters 'multiline' and 'wrap_lines' are True,the parameter 'width' must be a number.
        c = tlist[i]    ;    ha = hasattr(c, 'text')
        if   type(c) is pygtxt.Label:   c.x, c.y, c.width, c.height = 0, 0, 1, 0  # Zero width not allowed
        elif type(c) is pygsprt.Sprite: c.update(x=0, y=0, scale_x=0, scale_y=0)
        self.setJ(j, i)
        if dbg: self.dumpTnik(c, j, 'Hide')
        if dbg > 1:    text = c.text if ha else ''  ;  self.log(f'{self.fmtJText(j, i+1)} {id(c):x} {text:6} {c.x:7.2f} {c.y:7.2f} {c.width:7.2f} {c.height:7.2f}  J1={self.fmtJ1(0, 1)} J2={self.fmtJ2(0, 1)}', pfx=0)
    ####################################################################################################################################################################################################
    def resizeTniks(self, why=''):
        self.dumpTniksPfx(why)   ;   view = None
        if self.VIEWS:
            _, _, x, y, w, h = self.geom(V, n=1, i=1, dbg=0)
            if not self.views:    msg = f'ERROR Empty views {self.n=} {self.zzl()}';   self.log(msg);   self.quit(msg)
            view = self.resizeTnik(self.views, 0, V, x, y, w, h, why="Upd", v=1, dbg=1)
        for page in                self.g_resizeTniks(self.pages, P, view):
            for line in            self.g_resizeTniks(self.lines, L, page):
                for sect in        self.g_resizeTniks(self.sects, S, line): # pass
                    for col in     self.g_resizeTniks(self.cols,  C, sect): # pass
                        for _ in   self.g_resizeTniks(self.tabs,  T, col):  pass
        if self.RESIZE and self.cursor: self.resizeCursor()
        self.dumpTniksSfx(why)
    ####################################################################################################################################################################################################
    def g_resizeTniks(self, tlist, j, pt=None, why='Upd', dbg=1, dbg2=1):
        if not self.n[j]:     msg = f'ERROR {self.fmtJText(j, why=why)} SKIP {self.n[j]=}'   ;   self.log(msg)   ;   self.quit(msg)
        n, _, x, y, w, h = self.geom(j, pt, dbg=dbg2)
        x2 = x  ;  y2 = y  ;  j2 = j  ;  tlist2 = tlist
        p, l, c, t = self.j2plct()    ;  lp, ll = self.dl()[0], self.dl()[1]
        for i in range(n):
            if   j == C:                x2 = x + i * w
            else:
                if   j != P:            y2 = y - i * h
                if   j == L and self.J2[L] >= lp * ll: msg = f'WARN MAX Line {self.J2[L]=} >= {lp=} * {ll=}'     ;   self.log(msg)  ;  yield None
                elif j >= T:
                    s = self.ss2sl()[self.J1[S] % self.ssl()]
                    tlist2, j2 = self.tnikInfo(p, l, s, c, why=why)
            tnik = self.resizeTnik(tlist2, self.J2[j2], j2, x2, y2, w, h, dbg=dbg)
            yield tnik
    ####################################################################################################################################################################################################
    def resizeTnik(self, tlist, i, j, x, y, w, h, why='Upd', v=None, dbg=1):
        if not tlist:         msg = f'ERROR tlist is Empty {      self.fmtJText(j, i, why)}'  ;  self.log(msg)  ;  self.quit(msg)
        elif i >= len(tlist): msg = f'ERROR {i=} >={len(tlist)=} {self.fmtJText(j, i, why)}'  ;  self.log(msg)  ;  self.quit(msg)
        if j is not None:     self.setJ(j, i)
        tnik = tlist[i]
        v = v      if v is not None else self.isV(j)
        if   type(tnik) is pygtxt.Label:        fs = v * self.calcFontSize(tnik.text, w, h, j)  ;   tnik.x, tnik.y, tnik.width, tnik.height, tnik.font_size = x, y, w, h, fs
        elif type(tnik) is pygsprt.Sprite:  mx, my = w/tnik.image.width, h/tnik.image.height    ;   tnik.update(x=x, y=y, scale_x=mx, scale_y=my)   ;   tnik.visible = v
        if self.LL and j == L and v:          tnik = self.resizeLL(tnik)
        self.dumpTnik(tnik, j, why) if dbg else None
        return tnik
    ####################################################################################################################################################################################################
    def dumpTniksPfx(self, why=''):
        self.dumpWxHp0()
        self.dumpGeom('BGN', why)
        self.resetJ(why)
        self.dumpTnik()

    def dumpTniksSfx(self, why=''):
        self.dumpTnik()
        self.dumpJs(why) if self.J1 and self.J2 else self.log(f'WARN No Js {len(self.J1)=} {len(self.J2)=}')
        self.dumpGeom('END', why)
        self.dumpWxHp0()
    ####################################################################################################################################################################################################
    def dumpTniks2(self):
        np, nl, nc, nt = self.lenE()[P], self.lenE()[L], self.lenE()[C], self.lenE()[T]
        for p in range(np):
            j = P  ;  t = self.pages[p]  ;  self.log(f'{JTEXTS[j]:4} {t.x:7.2f} {t.y:7.2f} {t.width:7.2f} {t.height:7.2f} {self.fmtJ1()} {self.fmtJ2()}')
        for l in range(nl):
            j = L  ;  t = self.lines[l]  ;  self.log(f'{JTEXTS[j]:4} {t.x:7.2f} {t.y:7.2f} {t.width:7.2f} {t.height:7.2f}')
        for c in range(nc):
            j = C  ;  t  = self.cols[c]  ;  self.log(f'{JTEXTS[j]:4} {t.x:7.2f} {t.y:7.2f} {t.width:7.2f} {t.height:7.2f}')
        for t in range(nt):
            j = T  ;  t  = self.tabs[t]  ;  self.log(f'{JTEXTS[j]:4} {t.x:7.2f} {t.y:7.2f} {t.width:7.2f} {t.height:7.2f}')
        for r in range(nl):
            j = R  ;  t = self.lrows[r]  ;  self.log(f'{JTEXTS[j]:4} {t.x:7.2f} {t.y:7.2f} {t.width:7.2f} {t.height:7.2f}')
        for q in range(nc):
            j = Q  ;  t  = self.cols[q]  ;  self.log(f'{JTEXTS[j]:4} {t.x:7.2f} {t.y:7.2f} {t.width:7.2f} {t.height:7.2f}')
    ####################################################################################################################################################################################################
    def dumpTniks(self, why=''):
        np, nl, ns, nc, nt = self.n   ;   ns = self.ssl()   ;   (nr, nq) = (nl, nc) if self.LL else (0, 0)
        sp, sl, ss, sc = 0, 0, 0, 0   ;   st, sn, si, sk = 0, 0, 0, 0   ;   so, sa, sd = 0, 0, 0   ;   sr, sq = 0, 0   ;   i = 0
        self.dumpTniksPfx(why)
        if  self.VIEWS:
            if       not       self.views:    msg = f'ERROR Empty views {self.n=} {self.zzl()}';   self.log(msg);   self.quit(msg)
            for v in range(len(self.views)):
                self.dumpTnik( self.views[v], V, why)
        for p in range(np):
            j = P                         ;  z = sp  ;  self.setJ(j, z)  ;  self.dumpTnik(self.pages[z], j, why)  ;  i += 1  ;  sp += 1
            if self.isV(j):
                for r in range(nr):
                    j = R                 ;  z = sr  ;  self.setJ(j, z)  ;  self.dumpTnik(self.lrows[z], j, why)  ;  i += 1  ;  sr += 1
                    for q in range(nq):
                        j = Q             ;  z = sq  ;  self.setJ(j, z)  ;  self.dumpTnik(self.lcols[z], j, why)  ;  i += 1  ;  sq += 1
            for l in range(nl):
                lp, ll = self.dl()[0], self.dl()[1]
                if sl >= lp * ll:   msg = f'WARN MAX Line {sl=} >= {lp=} * {ll=}'  ;  self.log(msg)  ;  return
                j = L                     ;  z = sl  ;  self.setJ(j, z)  ;  self.dumpTnik(self.lines[z], j, why)  ;  i += 1  ;  sl += 1
                for s in (self.ss2sl()):
                    j = S                 ;  z = ss  ;  self.setJ(j, z)  ;  self.dumpTnik(self.sects[z], j, why)  ;  i += 1  ;  ss += 1
                    for c in range(nc):
                        j = C             ;  z = sc  ;  self.setJ(j, z)  ;  self.dumpTnik(self.cols[ z], j, why)  ;  i += 1  ;  sc += 1
                        for t in range(nt):
                            tlist, j = self.tnikInfo(p, l, s, c, why=why)  #  if z < len(tlist) else self.log(f'ERROR {self.fmtJText(j, t, why)} {z=} > {len(tlist)=}')
                            if   s == TT: z = so if j == O else sd if j == D else st  ;  self.setJ(j, z)  ;  self.dumpTnik(tlist[z], j, why)  ;  i += 1  ;  so += 1 if j == O else 0  ;  sd += 1 if j == D else 0  ;  st += 1 if j == T else 0
                            elif s == NN: z = sa if j == A else sd if j == D else sn  ;  self.setJ(j, z)  ;  self.dumpTnik(tlist[z], j, why)  ;  i += 1  ;  sa += 1 if j == A else 0  ;  sd += 1 if j == D else 0  ;  sn += 1 if j == N else 0
                            elif s == II: z = so if j == O else sd if j == D else si  ;  self.setJ(j, z)  ;  self.dumpTnik(tlist[z], j, why)  ;  i += 1  ;  so += 1 if j == O else 0  ;  sd += 1 if j == D else 0  ;  si += 1 if j == I else 0
                            elif s == KK: z = sa if j == A else sd if j == D else sk  ;  self.setJ(j, z)  ;  self.dumpTnik(tlist[z], j, why)  ;  i += 1  ;  sa += 1 if j == A else 0  ;  sd += 1 if j == D else 0  ;  sk += 1 if j == K else 0
                            else: msg = f'ERROR {i} {self.fmtn()} {np} {nl} {ns} {nc} {nt}, {p} {l} {s} {c} {t} {self.fmtLE(0)}'   ;   self.log(msg)  ;   self.quit(msg)
        self.dumpTniksSfx(why)
    ####################################################################################################################################################################################################
    def dumpTnik(self, t=None, j=None, why=''):
        if   t is None: self.dumpSprite()   ;   self.dumpLabel()
        elif j is None: msg = f'ERROR BAD j {j=}'   ;   self.log(msg)   ;   self.quit(msg)
        if   type(t) is pygtxt.Label:    self.dumpLabel( t, j, why)
        elif type(t) is pygsprt.Sprite:  self.dumpSprite(t, j, why)

    def dumpSprite(self, t=None, j=None, why=''):
        if t is None: self.log(f'P  L  S   C    T    N    I    K  R   Q H V No Nm  Cp  Tid     X       Y       W       H   why  Name  Cnt Visible G Red Grn Blu Opc  Mx    My', pfx=0); return
        J2  = self.fmtJ2()   ;   xywh = self.fmtTxywh(t)   ;   g = self.gn[j]   ;   color = self.fmtTcolor(t)   ;   v = self.fmtTvisible(t)   ;   sprt = self.fmtTsprite(t)
        key = self.idmapkey(j)   ;   assert key == f'{JTEXTS[j]:4} {self.J2[j]:4}', f'{key=} {JTEXTS[j]:4} {self.J2[j]:4}' # ID = self.idmap[key][0] {ID:x}
        self.log(f'{J2} {xywh} {why:4} {key} {v:7} {g} {color} {sprt}', pfx=0)

    def dumpLabel( self, t=None, j=None, why=''):
        if t is None: self.log(f'P  L  S   C    T    N    I    K  R   Q H V No Nm  Cp  Tid     X       Y       W       H   why  Name  Cnt Txt Siz G Red Grn Blu Opc Dpi B I  Font Name', pfx=0)  ;  return
        J2  = self.fmtJ2()  ;  xywh = self.fmtTxywh(t)  ;  g = self.gn[j]  ;  color = self.fmtTcolor(t)  ;  font = self.fmtTfont(t)  ;  fs = self.fmtTfontSize(t) # ID = self.idmap[key][0] {ID:x}
        cw, ch, ca = t.content_width, t.content_height, t.content_valign   ;    axy = self.fmtAxy()
        d = t.document  ;  bgcs = d.get_style('background_color')  ;  bgc = util.fmtl(bgcs)
        key = self.idmapkey(j)   ;   assert key == f'{JTEXTS[j]:4} {self.J2[j]:4}', f'{key=} {JTEXTS[j]:4} {self.J2[j]:4}'
        self.log(f'{J2} {xywh} {why:4} {key} {t.text:3} {fs:3} {g} {color} {font} {cw:2} {ch:2} {ca} {axy} {bgc}', pfx=0)
    ####################################################################################################################################################################################################
    def createCursor(self, dbg=1, dbg2=0):
        x, y, w, h, c = self.cc2xywh()
        if w == 0 or h == 0: msg = f'ERROR DIV by ZERO {w=} {h=}'   ;   self.log(msg)   ;   self.quit(msg)
        self.cursor = self.createTnik(self.cursr, 0, H, x, y, w, h, kk=0, kl=self.k[H], v=1, dbg=dbg)
        if dbg2: self.dumpCursr('NEW', x, y, w, h, c)
        self.setLLStyle(self.cc, CURRENT_STYLE)

    def resizeCursor(self, dbg=1, dbg2=0):
        x, y, w, h, c = self.cc2xywh()
        self.resizeTnik(self.cursr, 0, H, x, y, w, h, v=1, dbg=dbg)
        if dbg2: self.dumpCursr('UPD', x, y, w, h, c)

    def moveCursor(self, ss=0, dbg=1):
        self.setLLStyle(self.cc, SELECT_STYLE if ss else NORMAL_STYLE)
        self.resizeCursor(dbg=dbg)
        self.setLLStyle(self.cc, CURRENT_STYLE)
    ####################################################################################################################################################################################################
    def cc2xywh(self, dbg=1):
        cc = self.cursorCol()
        t  = self.tabs[cc]
        cw, ch, ca = t.content_width, t.content_height, t.content_valign
        if dbg: self.log(f'{cc=} {t.x=:6.2f} {t.y=:6.2f} {t.width=:6.2f} {t.height=:6.2f} {t.text=} {cw=} {ch=} {ca}', so=1)
        w, h = t.width, t.height
        x, y = t.x - w/2, t.y - h/2
        return x, y, w, h, cc

    def cursorCol(self): self.cc = self.plct2cc(*self.j2())  ;  return self.cc
    def normalizeCC(self, cc): return (cc // self.tpc) * self.tpc

    def plct2cc(self, p, l, c, t, dbg=0):
        cc = p * self.tpp + l * self.tpl + c * self.tpc + t   ;   lenT = len(self.tabs)   ;   ccm = cc % lenT if lenT else -1
        if dbg: self.log(f'plct2cc({p} {l} {c} {t}) {self.tpp} {self.tpl} {self.tpc} ({p*self.tpp} +{l*self.tpl} +{c*self.tpc} +{t}) % {lenT} return {ccm}')
        return ccm

    def cc2plct(self, cc, dbg=0):
        tpc, tpl, tpp, _ = self.ntp()
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

    def calcFontSize(self, t, w, h, j=T, dbg=0):
        if j == C: scale = 1.5
        else:      scale = 1.25
        pix = min(scale * w, h)
        fs = self.pix2fontsize(pix)
        if dbg: self.log(f'{j=} {JTEXTS[j]:4} {t=} {w=:6.2f} {h=:6.2f} {pix=:6.2f}=min({scale=:.1f}*w, h) {fs=:6.2f}')
        return int(fs)

    def _initFonts(self):
        np, nl, ns, nc, nt = self.n  ;  nc += self.zzl()
        n = nl * nt * ns if ns else nl * nt  ;  n += self.LL * nl
        w = self.width / nc  ;  h = self.height / n
        fs = self.calcFontSize(' ', w, h, j=T, dbg=1)
        self.fontBold, self.fontItalic, self.fontColorIndex, self.fontDpiIndex, self.fontNameIndex, self.fontSize = 0, 0, 0, 4, 0, fs
        self.log(f'{w=:6.3f}={self.width =}/({nc})                   {FONT_SCALE=:5.3f} fs=w*FONT_SCALE={fs:6.3f}pt')
        self.log(f'{h=:6.3f}={self.height=}/({nl=} * {ns=} * {nt=})  {FONT_SCALE=:5.3f} fs=h*FONT_SCALE={fs:6.3f}pt')
        self.dumpFont()

    def fontParams(self):    return self.fontBold, self.fontColorIndex, self.fontDpiIndex, self.fontItalic, self.fontNameIndex, self.fontSize

    def fmtf1(self, dbg=0):
        fb, fc, fd, fi, fn, fs = self.fontParams()
        text = f'{FONT_DPIS[fd]}dpi {fs:5.2f}pt {FONT_NAMES[fn]} {fc}:{FONT_COLORS[fc]}'
        if dbg: self.log(f'{text}')
        return text
    def fmtf2(self, dbg=0):
        fb, fc, fd, fi, fn, fs = self.fontParams()
        text = f'{fs} {FONT_DPIS[fd]} {fb} {fi} '
        if dbg: self.log(f'{text}')
        return text

    def dumpFont(self, why=''):
        b, k, dpi, i, n, s = self.fontParams()
        pix = s / FONT_SCALE
        self.log(f'{dpi}:{FONT_DPIS[dpi]}dpi {s:6.3f}pt {n}:{FONT_NAMES[n]} {k}:{FONT_COLORS[k]} {s:6.3f}pt = {FONT_SCALE:5.3f}(pt/pix) * {pix:6.3f}pixels {why}')

    def setFontParam(self, n, v, m, dbg=1):
        setattr(self, m, v)
        if dbg: self.log(f'{n=:12}  {v=:4}  {m=}')
        for i in range(len(self.E)):
            self._setFontParam(self.E[i], n, v, m)
#        self.on_resize(self.width, self.height, dbg=1)
#        self.setCaption(self.fmtf1())

    @staticmethod
    def _setFontParam(p, n, v, m, dbg=1):
        for i in range(len(p)):
            k = len(p[i].color)
            msg = f'{FONT_NAMES[v]=}' if m == "fontNameIndex" else f'{FONT_COLORS[v][:k]=}' if m == "fontColorIndex" else f'{v=}' # f'{FONT_DPIS[v]=}' if m == "fontDpiIndex" else f'{v=}'
            if dbg and not i % 10: util.slog(f'{i:4}  {n:12}  {v:4}  {msg}')
            setattr(p[i], n, FONT_NAMES[v] if m == 'fontNameIndex' else FONT_COLORS[v][:k] if m == 'fontColorIndex' else v) # FONT_DPIS[v] if m == 'fontDpiIndex' else v)
    @staticmethod
    def pix2fontsize(pix): return pix * FONT_SCALE # ( ) % FS_MAX
    ####################################################################################################################################################################################################
    def on_mouse_release(self, x, y, button, modifiers, dbg=1):
        np, nl, ns, nc, nt = self.n   ;   nz = self.zzl()    ;  nc += nz   ;   ll = self.LL   ;   file = None
        y0 = y   ;   y = self.height - y   ;   n = nl * ns * nt + ns * ll   ;   m = int(ns * nt) + ll
        w = self.width/nc       ;  h = self.height/n         ;   d = int(y/h) - ll
        l = int(d/m)            ;  c = int(x/w) - nz         ;   t = d - (l * m)  ;  p = 0
        if dbg: self.log(f'BGN button={button} modifiers={modifiers} txt={self.tabs[self.cc].text}', file=file)
        if dbg: self.log(f'{x=} {y0=:4} {w=:6.2f} {h=:6.2f}')
        if dbg: self.log(f'{y=:4} {n=} {m=} {ll=} {d=}')
        if dbg: self.log(f'{self.fmtPos()}     before')
        self.moveTo(f'MOUSE RELEASE', p, l, c, t)
        if dbg: self.log(f'{self.fmtPos()}     after')
    ####################################################################################################################################################################################################
    def kbkEvntTxt(self): return f'<{self.kbk:8}> <{self.symb:8}> <{self.symbStr:16}> <{self.mods:2}> <{self.modsStr:16}>'
    ####################################################################################################################################################################################################
    def on_key_press(self, symb, mods, dbg=0): # avoid these
        self.symb, self.mods, self.symbStr, self.modsStr = symb, mods, pygwink.symbol_string(symb), pygwink.modifiers_string(mods)
        self.kbk = self.symbStr  ;  kbk = self.kbk
        if   dbg: self.log(f'BGN {self.kbkEvntTxt()}')
        if   kbk == 'A' and self.isCtrlShift(mods):    self.toggleArrow(     '@^A', v=1)
        elif kbk == 'A' and self.isCtrl(     mods):    self.toggleArrow(     '@ A', v=0)
        elif kbk == 'B' and self.isCtrlShift(mods):    self.toggleBlank(     '@^B')
        elif kbk == 'B' and self.isCtrl(     mods):    self.toggleBlank(     '@ B')
        elif kbk == 'C' and self.isCtrlShift(mods):    self.copyTabs(        '@^C')
        elif kbk == 'C' and self.isCtrl(     mods):    self.copyTabs(        '@ C')
        elif kbk == 'D' and self.isCtrlShift(mods):    self.deleteTabs(      '@^D')
        elif kbk == 'D' and self.isCtrl(     mods):    self.deleteTabs(      '@ D')
        elif kbk == 'E' and self.isCtrlShift(mods):    self.eraseTabs(       '@^E')
#        elif kbk == 'E' and self.isCtrl(     mods):    self.eraseTabs(       '@ E')
        elif kbk == 'F' and self.isCtrlShift(mods):    self.toggleFullScreen('@^F')
        elif kbk == 'F' and self.isCtrl(     mods):    self.toggleFlatSharp( '@ F')
        elif kbk == 'G' and self.isCtrlShift(mods):    self.move2LastTab(    '@^G', page=1)
        elif kbk == 'G' and self.isCtrl(     mods):    self.move2LastTab(    '@ G', page=0)
        elif kbk == 'H' and self.isCtrlShift(mods):    self.move2FirstTab(   '@^H', page=1)
        elif kbk == 'H' and self.isCtrl(     mods):    self.move2FirstTab(   '@ H', page=0)
        elif kbk == 'I' and self.isCtrlShift(mods):    self.insertSpace(     '@^I')
        elif kbk == 'I' and self.isCtrl(     mods):    self.toggleTTs(       '@ I', II)
        elif kbk == 'J' and self.isCtrlShift(mods):    self.jump(            '@^J', a=1)
        elif kbk == 'J' and self.isCtrl(     mods):    self.jump(            '@ J', a=0)
        elif kbk == 'K' and self.isCtrlShift(mods):    self.toggleTTs(       '@^K', KK)
        elif kbk == 'K' and self.isCtrl(     mods):    self.toggleTTs(       '@ K', KK)
        elif kbk == 'L' and self.isCtrlShift(mods):    self.toggleLLs(       '@^L')
        elif kbk == 'L' and self.isCtrl(     mods):    self.toggleLLs(       '@ L')
        elif kbk == 'M' and self.isCtrlShift(mods):    self.toggleZZs(       '@^M', 1)
        elif kbk == 'M' and self.isCtrl(     mods):    self.toggleZZs(       '@ M', 0)
        elif kbk == 'N' and self.isCtrlShift(mods):    self.toggleTTs(       '@^N', NN)
        elif kbk == 'N' and self.isCtrl(     mods):    self.toggleTTs(       '@ N', NN)
        elif kbk == 'O' and self.isCtrlShift(mods):    self.toggleCursorMode('@^O')
        elif kbk == 'O' and self.isCtrl(     mods):    self.toggleCursorMode('@ O')
#        elif kbk == 'P' and self.isCtrlShift(mods):    self.cobj.togglePage( '@^P')
        elif kbk == 'P' and self.isCtrl(     mods):    self.addPage(         '@ P')
        elif kbk == 'Q' and self.isCtrlShift(mods):    self.quit(            '@^Q', error=0, save=0)
        elif kbk == 'Q' and self.isCtrl(     mods):    self.quit(            '@ Q', error=0, save=1)
        elif kbk == 'R' and self.isCtrlShift(mods):    self.toggleChordNames('@^R', hit=1)
        elif kbk == 'R' and self.isCtrl(     mods):    self.toggleChordNames('@ R', hit=0)
        elif kbk == 'S' and self.isCtrlShift(mods):    self.shiftTabs(       '@^S')
#        elif kbk == 'S' and self.isCtrl(     mods):    self.saveDataFile(    '@ S', self.dataPath1)
        elif kbk == 'S' and self.isCtrl(     mods):    self.swapTab(         '@ S', txt='')
        elif kbk == 'T' and self.isCtrlShift(mods):    self.toggleTTs(       '@^T', TT)
        elif kbk == 'T' and self.isCtrl(     mods):    self.toggleTTs(       '@ T', TT)
        elif kbk == 'U' and self.isCtrlShift(mods):    self.reset(           '@^U')
        elif kbk == 'U' and self.isCtrl(     mods):    self.reset(           '@ U')
#        elif kbk == 'V' and self.isCtrlAlt(  mods):    self.pasteTabs(       '@&V', hc=0, kk=1)
        elif kbk == 'V' and self.isCtrlShift(mods):    self.pasteTabs(       '@^V', kk=1)
        elif kbk == 'V' and self.isCtrl(     mods):    self.pasteTabs(       '@ V', kk=0)
        elif kbk == 'W' and self.isCtrlShift(mods):    self.swapCols(        '@^W')
        elif kbk == 'W' and self.isCtrl(     mods):    self.swapCols(        '@ W')
        elif kbk == 'X' and self.isCtrlShift(mods):    self.cutTabs(         '@^X')
        elif kbk == 'X' and self.isCtrl(     mods):    self.cutTabs(         '@ X')
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
        elif kbk == 'A' and self.isAltShift(mods):     self.setn_cmd(    '&^ A', txt='')
        elif kbk == 'A' and self.isAlt(     mods):     self.setn_cmd(    '& A', txt='')
    ####################################################################################################################################################################################################
        elif kbk == 'B' and self.isAltShift(mods):     self.setFontParam('bold',   not self.fontBold,                               'fontBold')
        elif kbk == 'B' and self.isAlt(     mods):     self.setFontParam('bold',   not self.fontBold,                               'fontBold')
        elif kbk == 'C' and self.isAltShift(mods):     self.setFontParam('color',     (self.fontColorIndex + 1) % len(FONT_COLORS), 'fontColorIndex')
        elif kbk == 'C' and self.isAlt(     mods):     self.setFontParam('color',     (self.fontColorIndex - 1) % len(FONT_COLORS), 'fontColorIndex')
#        elif kbk == 'D' and self.isAltShift(mods):     self.setFontParam('dpi',       (self.fontDpiIndex   + 1) % len(FONT_DPIS),   'fontDpiIndex')
#        elif kbk == 'D' and self.isAlt(     mods):     self.setFontParam('dpi',       (self.fontDpiIndex   - 1) % len(FONT_DPIS),   'fontDpiIndex')
        elif kbk == 'I' and self.isAltShift(mods):     self.setFontParam('italic', not self.fontItalic,                             'fontItalic')
        elif kbk == 'I' and self.isAlt(     mods):     self.setFontParam('italic', not self.fontItalic,                             'fontItalic')
        elif kbk == 'N' and self.isAltShift(mods):     self.setFontParam('font_name', (self.fontNameIndex + 1)  % len(FONT_NAMES),  'fontNameIndex')
        elif kbk == 'N' and self.isAlt(     mods):     self.setFontParam('font_name', (self.fontNameIndex - 1)  % len(FONT_NAMES),  'fontNameIndex')
        elif kbk == 'S' and self.isAltShift(mods):     self.setFontParam('font_size',  self.fontSize      + 1,                      'fontSize') # )  % FS_MAX
        elif kbk == 'S' and self.isAlt(     mods):     self.setFontParam('font_size',  max(self.fontSize-1, 1),                     'fontSize') # )  % FS_MAX
    ####################################################################################################################################################################################################
        if not self.isParsing():
            if   kbk == 'ENTER' and self.isCtrl(mods): self.setCHVMode(  '@  ENTER',     CHORD,       v=DOWN)
            elif kbk == 'ENTER':                       self.setCHVMode(  '   ENTER',     CHORD,       v=UP)
            elif kbk == 'SPACE':                       self.autoMove(    '   SPACE')
        elif dbg: self.log(f'Unexpected {self.kbkEvntTxt()}')
        if   dbg: self.log(       f'END {self.kbkEvntTxt()}')
    ####################################################################################################################################################################################################
    def on_key_release(self, symb, mods, dbg=0):
        self.symb, self.mods, self.symbStr, self.modsStr = symb, mods, pygwink.symbol_string(symb), pygwink.modifiers_string(mods)
        self.kbk = self.symbStr
        if dbg: self.log(f'{self.kbkEvntTxt()}')
    ####################################################################################################################################################################################################
    def on_text(self, text, dbg=0): # use for entering strings not for motion
        self.kbk = text
        if dbg: self.log(f'BGN {self.kbkEvntTxt()} swapping={self.swapping}')
        if   self.shiftingTabs:                              self.shiftTabs(  'onTxt', text)
        elif self.jumping:                                   self.jump(       'onTxt', text, self.jumpAbs)
        elif self.inserting:                                 self.insertSpace('onTxt', text)
        elif self.settingN:                                  self.setn_cmd(   'onTxt', text)
        elif self.swapping:                                  self.swapTab(    'onTxt', text)
        elif self.isTab(self.kbk):                           self.setTab(     'onTxt', self.kbk)
        elif self.kbk == '$' and self.isShift(self.mods):    self.snapshot(f'{text}', 'SNAP')
        if dbg: self.log(f'END {self.kbkEvntTxt()} swapping={self.swapping}')
    ####################################################################################################################################################################################################
    def on_text_motion(self, motion, dbg=1): # use for motion not strings
        self.kbk = motion   ;   p, l, s, c, t = self.j()  ;  np, nl, ns, nc, nt = self.n
        if dbg: self.log(f'BGN {self.kbkEvntTxt()} motion={motion}')
        if   self.isCtrlAltShift(self.mods):                 msg =             f'@&^({             motion})'   ;   self.log(msg)   ;   self.quit(msg)
        elif self.isCtrlAlt(self.mods):
            if   motion == 1:                                self.unselectTabs(f'@& LEFT ({        motion})',  nt)
            elif motion == 2:                                self.unselectTabs(f'@& RIGHT ({       motion})', -nt)
            else:                                            msg =             f'@& ({             motion})'   ;   self.log(msg)   ;   self.quit(msg)
        elif self.isAltShift(self.mods):                     msg =             f' &^({             motion})'   ;   self.log(msg)   ;   self.quit(msg)
        elif self.isCtrlShift(self.mods):                    msg =             f'@^ ({             motion})'   ;   self.log(msg)   ;   self.quit(msg)
        elif self.isShift(self.mods):                        msg =             f'^ ({              motion})'   ;   self.log(msg)   ;   self.quit(msg)
        elif self.isAlt(self.mods):
            if   motion == pygwink.MOTION_UP:                self.moveUp(      f' & UP ({          motion})')
            elif motion == pygwink.MOTION_DOWN:              self.moveDown(    f' & DOWN ({        motion})')
            elif motion == pygwink.MOTION_LEFT:              self.moveLeft(    f' & LEFT ({        motion})')
            elif motion == pygwink.MOTION_RIGHT:             self.moveRight(   f' & RIGHT ({       motion})')
            elif motion == pygwink.MOTION_BEGINNING_OF_LINE: self.move(        f' & HOME ({        motion})', -nt *  c)
            elif motion == pygwink.MOTION_END_OF_LINE:       self.move(        f' & END ({         motion})',  nt * (nc - self.i[C]))
            elif motion == pygwink.MOTION_PREVIOUS_PAGE:     self.prevPage(    f' & PAGE UP ({     motion})')
            elif motion == pygwink.MOTION_NEXT_PAGE:         self.nextPage(    f' & PAGE DOWN ({   motion})')
            else:                                            msg =             f' & ({             motion})'   ;   self.log(msg)   ;   self.quit(msg)
        elif self.isCtrl(self.mods):
            if   motion == pygwink.MOTION_PREVIOUS_WORD:     self.selectTabs(  f'@  LEFT ({        motion})', -nt)
            elif motion == pygwink.MOTION_NEXT_WORD:         self.selectTabs(  f'@  RIGHT ({       motion})',  nt)
            elif motion == pygwink.MOTION_BEGINNING_OF_LINE: msg = f'@  MOTION_BEGINNING_OF_LINE({ motion})'   ;   self.log(msg)   ;   self.quit(msg) # N/A
            elif motion == pygwink.MOTION_END_OF_LINE:       msg = f'@  MOTION_END_OF_LINE ({      motion})'   ;   self.log(msg)   ;   self.quit(msg) # N/A
            elif motion == pygwink.MOTION_BEGINNING_OF_FILE: msg = f'@  MOTION_BEGINNING_OF_FILE ({motion})'   ;   self.log(msg)   ;   self.quit(msg) # CTRL HOME
            elif motion == pygwink.MOTION_END_OF_FILE:       msg = f'@  MOTION_END_OF_FILE ({      motion})'   ;   self.log(msg)   ;   self.quit(msg) # CTRL END
            else:                                            msg =             f'CTRL ({           motion})'   ;   self.log(msg)   ;   self.quit(msg)
        elif self.mods == 0:
            if   motion == pygwink.MOTION_UP:                self.move(        f' UP ({            motion})', -1)
            elif motion == pygwink.MOTION_DOWN:              self.move(        f' DOWN ({          motion})',  1)
            elif motion == pygwink.MOTION_LEFT:              self.move(        f' LEFT ({          motion})', -nt)
            elif motion == pygwink.MOTION_RIGHT:             self.move(        f' RIGHT ({         motion})',  nt)
            elif motion == pygwink.MOTION_PREVIOUS_WORD:     msg = f'MOTION_PREVIOUS_WORD ({       motion})'   ;   self.log(msg)   ;   self.quit(msg)
            elif motion == pygwink.MOTION_NEXT_WORD:         msg = f'MOTION_NEXT_WORD ({           motion})'   ;   self.log(msg)   ;   self.quit(msg)
            elif motion == pygwink.MOTION_BEGINNING_OF_LINE: self.move(        f' HOME ({          motion})', -nt *  c)
            elif motion == pygwink.MOTION_END_OF_LINE:       self.move(        f' END ({           motion})',  nt * (nc - self.i[C]))
            elif motion == pygwink.MOTION_PREVIOUS_PAGE:     self.moveUp(      f' PAGE UP ({       motion})')  # move up   to top    of line, wrap down to bottom of prev line
            elif motion == pygwink.MOTION_NEXT_PAGE:         self.moveDown(    f' PAGE DOWN ({     motion})')  # move down to bottom tab on same line, wrap to next line
            elif motion == pygwink.MOTION_BEGINNING_OF_FILE: msg = f'MOTION_BEGINNING_OF_FILE ({   motion})'   ;   self.log(msg)   ;   self.quit(msg)
            elif motion == pygwink.MOTION_END_OF_FILE:       msg = f'MOTION_END_OF_FILE ({         motion})'   ;   self.log(msg)   ;   self.quit(msg)
            elif motion == pygwink.MOTION_BACKSPACE:         self.setTab(      f'BACKSPACE ({      motion})', self.tblank, rev=1)
            elif motion == pygwink.MOTION_DELETE:            self.setTab(      f'DELETE ({         motion})', self.tblank)
            else:                                            msg =             f'({                motion})'   ;   self.log(msg)   ;   self.quit(msg)
        if dbg: self.log(f'END {self.kbkEvntTxt()} motion={motion}')
#        1353 tabs.py       on_text_motion BGN <   65363> <   65363> <RIGHT           > <16> <MOD_NUMLOCK     > motion=65363
#        1353 tabs.py       on_text_motion BGN <   65363> <   65363> <RIGHT           > < 8> <MOD_CAPSLOCK    > motion=65363
    def on_style_text(self, start, end, attributes): msg = f'{start=} {end=} {util.fmtm(attributes)}'  ;  self.log(msg)  ;  self.quit(msg)
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
    def isAltShift(mods):     return mods & pygwink.MOD_ALT and mods & pygwink.MOD_SHIFT
    @staticmethod
    def isCtrlAlt(mods):      return mods & pygwink.MOD_CTRL and mods & pygwink.MOD_ALT
    @staticmethod
    def isCtrlAltShift(mods): return mods & pygwink.MOD_CTRL and mods & pygwink.MOD_ALT and mods & pygwink.MOD_SHIFT
    def isBTab(self, text):   return 1 if text in self.tblanks else 0
#    def isNBTab(text):        return 1 if                        self.sobj.isFret(text) or text in util.DSymb.SYMBS else 0
    def isTab(self, text):    return 1 if text == self.tblank or self.sobj.isFret(text) or text in util.DSymb.SYMBS else 0
    def isParsing(self):      return 1 if self.inserting or self.jumping or self.settingN or self.shiftingTabs or self.swapping else 0
    @staticmethod
    def afn(fn): return fn if len(fn) == 1 and '0' <= fn <= '9' else chr(ord(fn[1]) - ord('0') + ord('a')) if len(fn) == 2 and fn[0] == '1' else None
    ####################################################################################################################################################################################################
    def move2LastTab(self, how, page=0):
        if page: i = len(self.tabs) - 1
        else: i = self.i[L] * self.tpl - 1
        while not self.sobj.isFret(self.tabs[i].text): i -= 1
        p, l, c, t = self.cc2plct(i)
        self.moveTo(how, p, l, c, t)
        self.log(f'     {how}', pos=1)
    def move2FirstTab(self, how, page=0):
        if page: i = 0
        else: i = self.j()[L] * self.tpl - 1
        while not self.sobj.isFret(self.tabs[i].text): i += 1
        p, l, c, t = self.cc2plct(i)
        self.moveTo(how, p, l, c, t)
        self.log(f'     {how}', pos=1)
    ####################################################################################################################################################################################################
    def prevPage(self, how, dbg=1):
        p, l, c, t = self.j2()
        if dbg: self.log(f'BGN {how} i={self.fmti()}', pos=1)
        self.moveTo(how, p-1, l, c, t)
        self.on_resize(self.width, self.height)
        if dbg: self.log(f'END {how} i={self.fmti()}', pos=1)

    def nextPage(self, how, dbg=1):
        p, l, c, t = self.j2()
        if dbg: self.log(f'BGN {how} i={self.fmti()}', pos=1)
        self.moveTo(how, p+1, l, c, t)
        self.on_resize(self.width, self.height)
        if dbg: self.log(f'END {how} i={self.fmti()}', pos=1)
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

    def move(self, how, k, ss=0, dbg=1):   #  text={self.tabs[self.cc].text} {x:6.2f} {y:6.2f}')
        if dbg:    self.log(f'BGN k={k} {how}', pos=1)
        if k:
            p, l, c, t = self.j2()
            self._moveTo(p, l, c, t, n=k)
            if self.cursor: self.moveCursor(ss)
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
        if dbg: self.dumpCursorArrows(f'{self.fmtPos()}     {how} M={mmDist} C={cmDist} A={amDist}')
        if      self.csrMode == MELODY:                                     self.move(how, mmDist)
        elif    self.csrMode == CHORD:
            if   it == 1 and self.vArrow  == UP   and self.hArrow == RIGHT: self.move(how,   nt*2-1)
            elif it == 6 and self.vArrow  == DOWN and self.hArrow == RIGHT: self.move(how, -(nt*2-1))
            else:                                                           self.move(how, cmDist)
        elif    self.csrMode == ARPG:                                       self.move(how, amDist)
        self.log(f'END {how}', pos=1)
    ####################################################################################################################################################################################################
    def jump(self, how, txt='0', a=0):
        cc = self.cursorCol()   ;   self.jumpAbs = a
        self.log(f'{how} {txt=} {a=} {cc=} jt={self.jumpAbs} {self.fmti()}')
        if not self.jumping:                  self.jumping = 1
        elif txt.isdecimal():                 self.jumpStr += txt
        elif txt == '-' and not self.jumpStr: self.jumpStr += txt
        elif txt == ' ':
            self.log(f'{how} {txt=} {a=} {cc=} jt={self.jumpAbs} {self.jumpStr=} {self.fmti()}')
            jcc = self.n[T] * int(self.jumpStr)
            self.jumping = 0   ;    self.jumpStr = ''
            self.move(how, jcc - 1 - a * cc)
            self.log(f'{how} {txt=} {a=} {cc=} jt={self.jumpAbs} {jcc=} moved={jcc - 1 - a * cc} {self.fmti()}')
    ####################################################################################################################################################################################################
    def setTab(self, how, text, rev=0, dbg=1):
        if rev: self.reverseArrow()   ;    self.autoMove(how)
        p, l, c, t = self.j2()   ;   data = self.data[p][l][c][t]   ;   cc = self.plct2cc(p, l, c, t)  # ;   isDataFret = util.isFret(data)   ;   isTextFret = util.isFret(text)
        self.log(f'BGN {how} {text=} {data=} {rev=}', pos=1)
        self.setDTNIK(text, cc, p, l, c, t, kk=1) # if isDataFret or isTextFret else 0)
        p, l, c, t = self.j2()   ;   data = self.data[p][l][c][t]
        self.log(f'END {how}={text=} {data=} {rev=}', pos=1)
        if rev: self.reverseArrow()
        else:   self.autoMove(how)
        if dbg and self.SNAPS:
            stype = f'TXT_{text}' if self.sobj.isFret(text) else 'SYMB' if text in util.DSymb.SYMBS else 'UNKN'
            self.regSnap(f'{how}', stype)
        self.resyncData = 1

    def setDTNIK(self, text, cc, p, l, c, t, kk=0, pos=0, dbg=1):
        if dbg: self.log(f'BGN {kk=}    {text=}', pos=pos)
        self.setData(text, p, l, c, t)
        imap = self.getImap(p, l, c)
        if TT in self.SS: self.setTab2( text, cc)
        if NN in self.SS: self.setNote( text, cc, t)
        if II in self.SS: self.setIkey( imap, p, l, c)
        if KK in self.SS: self.setChord(imap, p, l, c) if kk else None
        if dbg: self.log(f'END {kk=}    {text=} {len(imap)=}', pos=pos)
    ####################################################################################################################################################################################################
    def setData(self, text, p, l, c, t, pos=0, dbg=1):
        data = self.data[p][l][c]
        if dbg: self.log(f'BGN {t=} {text=} {data=}', pos=pos)
        self.data[p][l][c] = data[0:t] + text + data[t+1:]
        data = self.data[p][l][c]
        if dbg: self.log(f'END {t=} {text=} {data=}', pos=pos)

    def setTab2(self, text, cc, pos=0, dbg=0):
        if dbg: self.log(f'BGN         {text=} tabs[{cc}]={self.tabs[cc].text}', pos=pos)
        self.tabs[cc].text = text
        if dbg: self.log(f'END         {text=} tabs[{cc}]={self.tabs[cc].text}', pos=pos)

    def setNote(self, text, cc, t, pos=0, dbg=0):
        if dbg: self.log(f'BGN     {t=} {text=} notes[{cc}]={self.notes[cc].text}', pos=pos)
        self.notes[cc].text = self.sobj.tab2nn(text, t) if self.sobj.isFret(text) else self.tblank
        if dbg: self.log(f'END     {t=} {text=} notes[{cc}]={self.notes[cc].text}', pos=pos)
    ####################################################################################################################################################################################################
    def getImap(self, p=None, l=None, c=None, dbg=0, dbg2=0):
        dl = self.dl()
        p2, l2, c2, t2 = self.j2plct(p, l, c)  ##
        cn = self.plc2cn(p, l, c)      ;    key = cn   ;   mli = self.cobj.mlimap
        msg1  = f'plc=[{p} {l} {c}] plsct=[{p2} {l2} {c2} {t2}]'   ;   msg2 = f'dl={self.fmtdl()} {cn=} {key=} keys={util.fmtl(list(mli.keys()))}'
        if dbg:           self.log(f'{msg1} {msg2}')
        if p >= dl[0] or l >= dl[1] or c >= dl[2]:  msg = f'ERROR Indexing {msg1} >= {msg2}'   ;   self.log(msg)   ;   self.quit(msg)
        imap  = self.cobj.getChordName(self.data, cn, p, l, c)
        if dbg2 and imap: self.cobj.dumpImap(imap)
        return imap
    ####################################################################################################################################################################################################
    def setIkey(self, imap, p, l, c, pos=0, dbg=0):
        cc = self.plct2cc(p, l, c, 0)
        ikeys = imap[0] if imap else []
        if dbg: self.log(f'BGN ikeys={util.fmtl(ikeys)} {len(imap)=}', pos=pos)
        self.setIkeyText(ikeys, cc, p, l, c)
        if dbg: self.log(f'END ikeys={util.fmtl(ikeys)} {len(imap)=}', pos=pos)

    def setIkeyText(self, text, cc, p, l, c, pos=0, dbg=1, dbg2=0):
        nt  = self.n[T]  ;  cc = self.normalizeCC(cc)   ;   data = self.data[p][l][c]   ;   text = text[::-1]
        txt = self.objs2Text(self.ikeys, cc, nt, I)     ;   sobj = self.sobj  ;  blank = self.tblank  ;  j = 0
        if dbg:  self.log(f'BGN [{cc:2}-{cc+nt-1:2}] text={util.fmtl(text)} {data=} ikeys=<{txt}>{len(txt)}', pos=pos)
        for i in range(nt):
            if text and len(text) > j: ifd = sobj.isFret(data[i])  ;  self.ikeys[cc+i].text = text[j] if ifd else blank  ;  j += 1 if ifd else 0
            else:                                                     self.ikeys[cc+i].text = blank
        txt = self.objs2Text(self.ikeys, cc, nt, I)
        if dbg:  self.log(f'END [{cc:2}-{cc+nt-1:2}] text={util.fmtl(text)} {data=} ikeys=<{txt}>{len(txt)}', pos=pos)
        if dbg2: self.dumpDataSlice(p, l, c, cc)
    ####################################################################################################################################################################################################
    def setChord(self, imap, p, l, c, pos=0, dbg=0):
        cc = self.plct2cc(p, l, c, 0)
        name = imap[3] if imap and len(imap) > 3 else ''  ;   chunks = imap[4] if imap and len(imap) > 4 else []
        if dbg: self.log(f'BGN {name=} chunks={util.fmtl(chunks)} {len(imap)=}', pos=pos)
        self.setChordName(cc, name, chunks) # if name and chunks else self.log(f'WARN Not A Chord {cc=} {name=} {chunks=}', pos=pos)
        if dbg: self.log(f'END {name=} chunks={util.fmtl(chunks)} {len(imap)=}', pos=pos)

    def setChordName(self, cc, name, chunks, pos=0, dbg=1):
        nt = self.n[T]   ;   cc = self.normalizeCC(cc)   ;   kords = self.kords
        txt = self.objs2Text(kords, cc, nt, K)
        if dbg: self.log(f'BGN [{cc:2}-{cc+nt-1:2}] {name=} chunks={util.fmtl(chunks)} chords=<{txt}>{len(txt)}', pos=pos)
        for i in range(nt):
            if chunks and len(chunks) > i: self.kords[cc + i].text = chunks[i]
            else:                          self.kords[cc + i].text = self.tblank
        txt = self.objs2Text(kords, cc, nt, K)
        if dbg: self.log(f'END [{cc:2}-{cc+nt-1:2}] {name=} chunks={util.fmtl(chunks)} chords=<{txt}>{len(txt)}', pos=pos)
    @staticmethod
    def objs2Text(obs, cc, nt, j, dbg=0):
        texts = [ obs[cc + t].text for t in range(nt) ]   ;   text = ''.join(texts)
        if dbg: util.slog(f'{jTEXTS[j]}[{cc}-{cc+nt-1}].text={util.fmtl(texts)}=<{text}>')
        return text
    ####################################################################################################################################################################################################
    def toggleSelectAll(self, how):
        self.dumpSmap(f'BGN {how} {self.allSelected=}')
        if   self.allSelected: self.unselectAll(how)   ;   self.allSelected = 0
        else:                  self.selectAll(how)     ;   self.allSelected = 1
        self.dumpSmap(f'END {how} {self.allSelected=}')

    def selectAll(self, how, dbg=0):
        mli = self.cobj.mlimap
        if dbg: self.dumpSmap(f'BGN {how}')
        for k in mli:
            if k not in self.smap: self.selectTabs(how, cn=k, dbg=1)
        if dbg: self.dumpSmap(f'END {how}')

    def unselectAll(self, how, dbg=0):
        for i in range(len(self.smap)-1, -1, -1):
            cn = list(self.smap.keys())[i]
            if dbg: self.dumpSmap(f'{how} {i=} {cn=}')
            self.unselectTabs(how, m=0, cn=cn)
    ####################################################################################################################################################################################################
    def setLLStyle(self, cc, style, dbg=1):
        if not self.LL or not self.lcols: self.log(f'SKIP {self.LL=} {len(self.lcols)=}') if dbg else None   ;   return
        p, l, c, t = self.cc2plct(cc)             ;  nc = self.n[C]
        bold, italic, color = 0, 0, self.k[Q][0]  ;   i = c + l * nc if self.lcols else 0
        if   style == NORMAL_STYLE:    bold = 0;  italic = 0
        elif style == CURRENT_STYLE:   bold = 1;  italic = 1
        elif style == SELECT_STYLE:    bold = 1;  italic = 1
        else: msg = f'ERROR Invalid style @ [{p} {l} {c} {t}] {i=} {style=}';  self.log(msg);  self.quit(msg)
        bc = 'background_color'  ;  fc = 'color'
        (bs, fs) = (0, 1) if style == NORMAL_STYLE else (1, 0)
        d = self.lcols[i].document  ;  d.set_style(0, len(d.text), {fc: self.llcolor(i, Q)[fs], bc: self.llcolor(i, Q)[bs]})
        self.lcols[i].bold   = bold
        self.lcols[i].italic = italic
        if dbg: self.log(f'{self.fmtPos()}     {i=} = {c=} + {l=} * {nc=} {style=} {bold=} {italic=} {color=} {cc=}')
    ####################################################################################################################################################################################################
    def setTNIKStyle(self, k, nt, style, text='', blank=0):
        for t in range(k, k + nt):
            bgc = 'background_color' ;  fgc = 'color'  ;  uls, ulv = 'underline', (255, 0, 0, 255)
            (bgs, fgs) = (0, 1) if style == NORMAL_STYLE else (1, 0)
            kt, kn, ki, kk = self.k[T], self.k[N], self.k[I], self.k[K]
            tabs, notes, ikeys, kords = self.tabs, self.notes, self.ikeys, self.kords
            if tabs:  d =  tabs[t].document  ;  d.set_style(0, len(d.text), {fgc: kt[fgs], bgc: kt[bgs], uls: ulv})  ;  text += tabs[t].text
            if notes: d = notes[t].document  ;  d.set_style(0, len(d.text), {fgc: kn[fgs], bgc: kn[bgs], uls: ulv})
            if ikeys: d = ikeys[t].document  ;  d.set_style(0, len(d.text), {fgc: ki[fgs], bgc: ki[bgs], uls: ulv})
            if kords: d = kords[t].document  ;  d.set_style(0, len(d.text), {fgc: kk[fgs], bgc: kk[bgs], uls: ulv})
            if blank: p, l, c, r = self.cc2plct(t)  ;  self.setDTNIK(self.tblank, t, p, l, c, t - k, kk=1 if t == k + nt - 1 else 0)
        return text
    ####################################################################################################################################################################################################
    def selectTabs(self, how, m=0, cn=None, dbg=1, dbg2=1):
        if cn is None: cc = self.cc   ;   cn = self.cc2cn(cc)
        else:          cc = self.cn2cc(cn)
        nt = self.n[T]  ;  k = cn * nt   ;   style = SELECT_STYLE
        if cn in self.smap: self.log(f'RETURN: {cn=} already in smap={util.fmtm(self.smap)}') if dbg2 else None   ;   return
        if dbg: self.dumpSmap(f'BGN {how} {m=} {cn=} {cc=} {k=}')
        text = self.setTNIKStyle(k, nt, style)
        self.smap[cn] = text
        if m: self.move(how, m, ss=1)
        if dbg: self.dumpSmap(f'END {how} {m=} {cn=} {cc=} {k=}')
    ####################################################################################################################################################################################################
    def unselectTabs(self, how, m, cn=None, dbg=0):
        if cn is None: cc = self.cc   ;   cn = self.cc2cn(cc)
        else:          cc = self.cn2cc(cn)
        nt = self.n[T]   ;   k = cn * nt   ;   style = NORMAL_STYLE
        self.setLLStyle(cc, style)
        if dbg: self.dumpSmap(f'BGN {how} {m=} {cn=} {cc=} {k=}')
        self.setTNIKStyle(k, nt, style)
        if cn in self.smap: self.smap.pop(cn)
        elif dbg:           self.log(f'{cn=} not found in smap={util.fmtm(self.smap)}')
        if m:   self.move(how, m)
        if dbg: self.dumpSmap(f'END {how} {m=} {cn=} {cc=} {k=}')
    ####################################################################################################################################################################################################
    def copyTabs(self, how, dbg=1):
        self.dumpSmap(f'BGN {how}')   ;   nt = self.n[T]   ;   style = NORMAL_STYLE   ;   text = ''
        for k in list(self.smap.keys()):
            k *= nt
            self.setLLStyle(k, style)
            text += self.setTNIKStyle(k, nt, style)
            if dbg: text += ' '
        if dbg: self.log(f'{text=}')
        self.dumpSmap(f'END {how}')
        if self.SNAPS: self.regSnap(f'{how}', 'COPY')
    ####################################################################################################################################################################################################
    def cutTabs(self, how): self.log('BGN Cut = Copy + Delete')  ;  self.copyTabs(how)  ;  self.log('Cut = Copy + Delete')  ;  self.deleteTabs(how, keep=1)  ;  self.log('END Cut = Copy + Delete')
    ####################################################################################################################################################################################################
    def deleteTabs(self, how, keep=0, dbg=1):
        self.dumpSmap(f'BGN {how} {keep=}')   ;   style = NORMAL_STYLE   ;   nt = self.n[T]
        for k, text in self.smap.items():
            cn = k   ;   k *= nt
            if dbg: self.log(f'{k=} {cn=} {text=}')
            self.setLLStyle(k, style)
            self.setTNIKStyle(k, nt, style, blank=1)
        if not keep: self.unselectAll(f'deleteTabs({keep=})')
        self.dumpSmap(f'END {how} {keep=}')
        if self.SNAPS: self.regSnap(f'{how}', 'DEL')
        self.resyncData = 1

    def pasteTabs(self, how, kk=0, dbg=1):
        cc = self.cursorCol()        ;  nt = self.n[T]
        ntc = self.normalizeCC(cc)   ;  kt = 0
        p, l, s, c, r = self.j()
        self.dumpSmap(f'BGN {how} {kk=} {cc=} {ntc=} cn={self.cc2cn(cc)} plcr=[{p} {l} {c} {r}]')
        for i, (k, text) in enumerate(self.smap.items()):
            if not i: dk = 0
            elif kk:  dk = i * nt
            else:     dk = (list(self.smap.keys())[i] - list(self.smap.keys())[0]) * nt
            if dbg: self.log(f'{i=} {k=} {text=} {kk=} {dk=}')
            for t in range(nt):
                kt = (ntc + dk + t) % self.tpp
                p, l, c, r = self.cc2plct(kt)
                self.setDTNIK(text[t], kt, p, l, c, t, kk=1 if t==nt-1 else 0)
            if dbg: self.log(f'smap[{k}]={text=} {kt=} {kk=} {dk=}')
#        if not hc: self.unselectAll('pasteTabs()')
#        elif dbg:  self.log(f'holding a copy of smap')
#        self.dumpSmap(f'END {how} {hc=} {kk=} {cc=} {ntc=} cn={self.cc2cn(cc) + 1}')
        self.dumpSmap(f'END {how} {kk=} {cc=} {ntc=} cn={self.cc2cn(cc)} plcr=[{p} {l} {c} {r}]')
        if self.SNAPS: self.regSnap(f'{how}', 'PAST')
        self.resyncData = 1
    ####################################################################################################################################################################################################
    def swapCols(self, how):
        nk = len(self.smap)   ;   nk2 = nk // 2
        self.dumpSmap(f'BGN {nk=} {nk2=}')
        for i in range(nk2):
            k1 = list(self.smap.keys())[i]
            k2 = list(self.smap.keys())[nk - 1 - i]
            text1 = self.smap[k1]
            text2 = self.smap[k2]
            self.smap[k1] = text2
            self.smap[k2] = text1
        self.dumpSmap(f'    {nk=} {nk2=}')
        self.pasteTabs(how)
        self.dumpSmap(f'END {nk=} {nk2=}')

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
            self.log(f'{util.fmtl(tcs, ll=1)} insertSpace', pfx=0)
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
        self.dumpSmap(f'BGN {how} {self.shiftingTabs=} {nf=}')
        if not self.shiftingTabs:
            self.shiftingTabs = 1
            for k, v in self.smap.items():
                self.setLLStyle(k, NORMAL_STYLE)
            self.setCaption('Enter nf: number of frets to shift +/- int')
        elif nf == '-': self.shiftSign = -1
        elif self.sobj.isFret(nf):
            self.shiftingTabs = 0   ;   nt = self.n[T]
            for cn, v in self.smap.items():
                cc = self.cn2cc(cn)   ;   p, l, c, r = self.cc2plct(cc, dbg=0)
                self.log(f'{cc=} {cn=} {v=} text={self.smap[cn]}')
                for t in range(nt):
                    text = self.smap[cn][t]    ;    kt = cc + t    ;    fn = 0   ;   ntones = util.NTONES * 2
                    if self.sobj.isFret(text):
                        fn = self.afn(str((self.tab2fn(text) + self.shiftSign * self.tab2fn(nf)) % ntones))  ;  self.log(f'{cc=} {cn=} {t=} {text=} {nf=} {fn=} {self.shiftSign=}')
                    if fn and self.sobj.isFret(fn):  self.setDTNIK(fn, kt, p, l, c, t, kk=1 if t==nt-1 else 0)
            self.shiftSign = 1
            self.resyncData = 1
            self.unselectAll('shiftTabs()')
        self.dumpSmap(f'END {how} {self.shiftingTabs=} {nf=} {self.shiftSign=}')

    def swapTab(self, how, txt='', data=None, dbg=0, dbg2=1):  # e.g. c => 12 not same # chars asserts
        src, trg = self.swapSrc, self.swapTrg
        data = data or self.data
        if not self.swapping: self.swapping = 1
        elif txt.isalnum():
            if   self.swapping == 1:   src += txt   ;   self.log(f'    {how} {txt=} {self.swapping=} {src=} {trg=}')
            elif self.swapping == 2:   trg += txt   ;   self.log(f'    {how} {txt=} {self.swapping=} {src=} {trg=}')
            self.swapSrc, self.swapTrg = src, trg
        elif txt == '\r':
            self.log(f'    {how} {self.swapping=} {src=} {trg=}')
            if   self.swapping == 1 and not trg: self.swapping = 2   ;   self.log(f'{how} waiting {src=} {trg=}') if dbg else None   ;   return
            elif self.swapping == 2 and     trg: self.swapping = 0   ;   self.log(f'{how} BGN     {src=} {trg=}') if dbg else None
            np, nl, ns, nc, nt = self.n   ;   nc += self.zzl()
            cc0 = self.cursorCol()  ;  p0, l0, c0, t0 = self.cc2plct(cc0)  ;  self.log(f'BFR {cc0=} {p0=} {l0=} {c0=} {t0=}')
            blanks = self.tblanks  ;  blank = 1 if src in blanks and trg in blanks else 0
            if blank:
                for i in range(len(self.tabs)):
                    if self.tabs  and  self.tabs[i].text == src:  self.tabs[i].text = trg
                    if self.notes and self.notes[i].text == src: self.notes[i].text = trg
                    if self.ikeys and self.ikeys[i].text == src: self.ikeys[i].text = trg
                    if self.kords and self.kords[i].text == src: self.kords[i].text = trg
            else:
                for p in range(np):
                    for l in range(nl):
                        for c in range(nc):
                            text = data[p][l][c]
                            for t in range(nt):
                                if text[t] == src:
                                    if dbg2: self.log(f'Before data[{p} {l} {c}]={text}')
                                    cc = self.plct2cc(p, l, c, t)  ;  self.setDTNIK(trg, cc, p, l, c, t, kk=1)
                                    if dbg2: self.log(f'After  data[{p} {l} {c}]={text}')
            self.swapSrc, self.swapTrg = '', ''
            self.log(f'{how} END     {src=} {trg=}') if dbg else None
            if dbg2: self.dumpTniks('SWAP')
#            self.moveTo(how, p0, l0, c0, t0)  ;  cc = self.cursorCol()  ;  self.log(f'AFT {cc0=} {p0=} {l0=} {c0=} {t0=} {cc=}')
            if self.SNAPS: self.regSnap(f'{how}', 'SWAP')
            self.resyncData = 1

    def setn_cmd(self, how, txt='', dbg=1):
        if not self.settingN: self.settingN = 1   ;  self.setNtxt = '' ;  self.log(f'BGN {how} {txt=} {self.settingN=} {self.setNvals=}') if dbg else None
        elif txt.isdecimal(): self.setNtxt += txt                      ;  self.log(f'Concat {txt=} {self.settingN=} {self.setNvals=}') if dbg else None
        elif txt == ' ':      self.setNvals.append(int(self.setNtxt))  ;  self.log(f'Append {txt=} {self.settingN=} {self.setNvals=}') if dbg else None   ;  self.setNtxt = ''
        elif txt == 'Q':      self.settingN = 0  ;  self.log(f'Cancel {txt=} {self.settingN=} {self.setNvals=}') if dbg else None
        elif txt == '\r':
            self.settingN = 0   ;   old = self.n
            self.setNvals.append(int(self.setNtxt))
            if len(self.setNvals) == 4:
                self.n[:2] = self.setNvals[:2]   ;  self.n[3:] = self.setNvals[2:]
            self.log(f'Setting {old=} {self.n=}')
            self.log(f'END {how} {txt=} {self.settingN=} {self.setNvals=}')
    ####################################################################################################################################################################################################
    def toggleFlatSharp(self, how, dbg=1):  #  page line col tab or select
        tt1 =  util.Note.TYPE    ;    tt2 = (util.Note.TYPE + 1) % 2    ;    util.Note.setType(tt2)    ;   i1 = -1
        self.log(f'BGN {how} type={tt1}={util.Note.TYPES[tt1]} => type={tt2}={util.Note.TYPES[tt2]}')
        for i, note in enumerate(self.notes):
            if len(note.text) > 1:
                p, l, c, t = self.cc2plct(i)   ;   old = note.text    ;    i2 = self.plc2cn(p, l, c)
                if   note.text in util.Note.F2S: note.text = util.Note.F2S[note.text]
                elif note.text in util.Note.S2F: note.text = util.Note.S2F[note.text]
                if dbg: self.log(f'notes[{i:3}] {old} => {note.text} {i1=} {i2=}')
                if self.kords and i1 != i2:   imap = self.getImap(p, l, c)   ;   self.setChord(imap, p, l, c, t)    ;    i1 = i2
        self.log(f'END {how} type={tt1}={util.Note.TYPES[tt1]} => type={tt2}={util.Note.TYPES[tt2]}')
    ####################################################################################################################################################################################################
    def toggleChordNames(self, how, hit=0, dbg=1):
        cc = self.cc    ;    cn = self.cc2cn(cc)
        mks = list(self.cobj.mlimap.keys())   ;   sks = list(self.smap.keys())
        if sks and not hit:
            if dbg: self.dumpSmap(f'BGN {how} mks={util.fmtl(mks)} {cn=:2} {hit=} sks={util.fmtl(sks)}')
            [ self.toggleChordName(how, k) for k in sks ]
        else:
            if dbg: self.dumpSmap(f'BGN {how} mks={util.fmtl(mks)} {cn=:2} {hit=} sks={util.fmtl(sks)}')
            if hit: self.toggleChordNameHits(how, cn)
            else:   self.toggleChordName(    how, cn)
        if dbg:     self.dumpSmap(f'END {how} mks={util.fmtl(mks)} {cn=:2} {hit=} sks={util.fmtl(sks)}')

    def toggleChordNameHits(self, how, cn, dbg=1):
        mli = self.cobj.mlimap   ;   mks = list(mli.keys())
        if cn not in mli: self.log(f'RETURN: no mli key for {cn=}') if dbg else None   ;   return
        ivals =  [ u[1] for u in mli[cn][0] ]
        msg   =  [ util.fmtl(v, z="x") for v in ivals ]
        if dbg: self.log(f'BGN {how} mks={util.fmtl(mks)} cn={cn:2} ivals={util.fmtl(msg, d1="")}')
        hits = self.ivalhits(ivals, how)
        for cn in hits:
            if cn not in self.smap: self.selectTabs(how, m=0, cn=cn)
            self.toggleChordName(how, cn)
        if dbg: self.log(f'END {how} mks={util.fmtl(mks)} cn={cn:2} ivals={util.fmtl(msg, d1="")}')

    def ivalhits(self, ivals, how, dbg=1):
        mli = self.cobj.mlimap   ;   mks = list(mli.keys())   ;   hits = set()
        for cn, lim in mli.items():
            for im in lim[0]:
                if cn in hits: break
                for iv in ivals:
                    iv1 = self.cobj.fsort(iv)   ;   iv2 = self.cobj.fsort(im[1])
                    if iv1 == iv2:     hits.add(cn)  ;   break
        if dbg: self.log(f'    {how} mks={util.fmtl(mks)} hits={util.fmtl(hits)}')
        return list(hits)

    def toggleChordName(self, how, cn, dbg=1, dbg2=1):
        cc = self.cn2cc(cn)   ;   mli = self.cobj.mlimap
        p, l, c, t = self.cc2plct(cc)    ;   msg = ''
        if not self.ikeys and not self.kords: msg +=  'RETURN: Both ikeys and chords are Empty - '
        if cn not in mli:                     msg += f'RETURN: {cn=} Not Found milap.keys={util.fmtl(list(mli.keys()))}'
        if msg: self.log(msg)   ;   return
        limap = mli[cn][0]      ;   imi = mli[cn][1]
        imi = (imi + 1) % len(limap)
        mli[cn][1] = imi
        ikeys, ivals, notes, chordName, chunks, rank = limap[imi]
        if self.ikeys and ikeys:                self.setIkeyText(ikeys, cc, p, l, c)
        if self.kords and chordName and chunks: self.setChordName(cc, chordName, chunks)
        elif dbg: self.log(f'    {how} {cn=} {cc=} is NOT a chord')
        if dbg2:  self.cobj.dumpImap(limap[imi], why=f'{cn:2}')
        assert imi == limap[imi][-1], f'{imi=} {limap[imi][-1]=}'
    ####################################################################################################################################################################################################
    def toggleCursorMode(self, how):
        self.log(f'BGN {how} {self.csrMode=} = {CSR_MODES[self.csrMode]=}')
        self.csrMode  = (self.csrMode + 1) % len(CSR_MODES)
        self.log(f'END {how} {self.csrMode=} = {CSR_MODES[self.csrMode]=}')

    def toggleArrow(self, how, v=0, dbg=0):
        if dbg: self.log(f'BGN {how} {v=} {self.hArrow=} = {HARROWS[self.hArrow]=} {self.vArrow=} = {VARROWS[self.vArrow]=}')
        if v: self.vArrow  = (self.vArrow + 1) % len(VARROWS)
        else: self.hArrow  = (self.hArrow + 1) % len(HARROWS)
        if dbg: self.log(f'END {how} {v=} {self.hArrow=} = {HARROWS[self.hArrow]=} {self.vArrow=} = {VARROWS[self.vArrow]=}')
    ####################################################################################################################################################################################################
    def toggleFullScreen(self, how):
        self.FULL_SCREEN =  not  self.FULL_SCREEN
        self.set_fullscreen(self.FULL_SCREEN)
        self.log(f'{how} {self.FULL_SCREEN}=')

    def toggleBlank(self, how):
        prevBlank    =  self.tblank
        self.log(f'BGN {how} {prevBlank=}')
        self.tblanki = (self.tblanki + 1) % len(self.tblanks)
        self.tblank  =  self.tblanks[self.tblanki]
        self.swapSrc, self.swapTrg, self.swapping = prevBlank, self.tblank, 2
        self.swapTab(how, '\r')
        self.swapSrc, self.swapTrg = '', ''
        self.log(f'END {how} {self.tblank=}')
    ####################################################################################################################################################################################################
    def dumpCursorArrows(self, how): cm, ha, va = self.csrMode, self.hArrow, self.vArrow  ;   self.log(f'{how} csrMode={cm}={CSR_MODES[cm]:6} hArrow={ha}={HARROWS[ha]:5} vArrow={va}={VARROWS[va]:4}')
    def reverseArrow(self, dbg=1):
        if dbg: self.dumpCursorArrows('reverseArrow()')
        if self.csrMode == MELODY or self.csrMode == ARPG: self.toggleArrow('reverseArrow() MELODY or ARPG', v=0)
        if self.csrMode == CHORD  or self.csrMode == ARPG: self.toggleArrow('reverseArrow() CHORD or ARPG',  v=1)
        if dbg: self.dumpCursorArrows('reverseArrow()')

    def setCHVMode(self, how, c=None, h=None, v=None):
        self.dumpCursorArrows(f'BGN {how} {c=} {h=} {v=}')
        if c is not None: self.csrMode = c
        if h is not None: self.hArrow  = h
        if v is not None: self.vArrow  = v
        self.dumpCursorArrows(f'END {how} {c=} {h=} {v=}')
    ####################################################################################################################################################################################################
    def eraseTabs(self, how): # , reset=0):
        np, nl, ns, nc, nt = self.n   ;   nz = self.zzl()  ;  nc += nz
        self.log(f'BGN {how} {np=} {nl=} {ns=} {nc=} {nt=}')
        self.dumpBlank()
        for i in range(len(self.tabs)):
            self.tabs [i].text = self.tblank
        for i in range(len(self.notes)):
            self.notes[i].text = self.tblank
        for i in range(len(self.ikeys)):
            self.ikeys[i].text = self.tblank
        for i in range(len(self.kords)):
            self.kords[i].text = self.tblank
        for p in range(np):
            for l in range(nl):
                for c in range(nz, nc):
                    self.data[p][l][c-nz] = self.tblankCol
        self.log(f'END {how} {np=} {nl=} {ns=} {nc=} {nt=}')
        self.resyncData = 1

    def reset(self, how):
        self.dumpGeom('BGN', f'{how} before cleanup()')
        self.cleanup()
        self.dumpGeom('   ', f'{how} after cleanup() / before reinit()')
        self._reinit()
        self.dumpGeom('END', f'{how} after reinit()')
    ####################################################################################################################################################################################################
    def cci(self, j, k, kl, dbg=0):
        if k == 0:  self.ki[j] = (self.ki[j] + 1) % len(kl)
        kk   = (k + self.ki[j]) % len(kl)
        if dbg: self.log(f'.ki={util.fmtl(self.ki[:10])} {j=} {k=} kl={util.fmtl(kl)} {self.ki[j]=} {kk=}')
        return kk
    ####################################################################################################################################################################################################
    def regSnap(self, why, typ, dbg=1):
        self.snapWhy  = why
        self.snapType = typ
        self.snapReg  = 1
        if dbg: self.log(f'{self.snapWhy=} {self.snapType=} {self.snapReg=} {self.snapId=}')

    def snapshot(self, why='', typ='', dbg=0, dbg2=1):
        WHY       =  f'{why}' if why else self.snapWhy
        TYPE      = f'.{typ}' if typ else f'.{self.snapType}'
        SNAP_ID   = f'.{self.snapId}'
        LOG_ID    = f'.{self.LOG_ID}' if self.LOG_ID else ''
        if dbg:     self.log(f'{LOG_ID=} {TYPE=} {SNAP_ID=} {WHY}')
        if dbg:     self.log(f'{SNAP_DIR=} {BASE_NAME=} {SNAP_ID=} {SNAP_SFX=}')
        SNAP_NAME = BASE_NAME + LOG_ID + TYPE + SNAP_ID + SNAP_SFX
        SNAP_PATH = BASE_PATH / SNAP_DIR / SNAP_NAME
        if dbg:     self.log(f'{SNAP_PATH=}', pfx=0)
        pyglet.image.get_buffer_manager().get_color_buffer().save(f'{SNAP_PATH}')
        if dbg2:    self.log(f'{SNAP_NAME=} {WHY}', so=1)
        self.snapId += 1
    ####################################################################################################################################################################################################
    def deleteGlob(self, g, why=''):
        self.log(f'deleting {len(g)} files from glob {why=}')
        for f in g:
            self.log(f'{f}')
            os.system(f'del {f}')

    def getFilePath(self, seq=0, fdir='files', fsfx='.txt'):
        if seq and not self.LOG_ID:
            fdir      += '/'
            self.log(f'{fdir=} {fsfx=}')
            pathlib.Path(fdir).mkdir(parents=True, exist_ok=True)
            fGlobArg   = str(BASE_PATH / fdir / BASE_NAME) + '.*' + fsfx
            fGlob      = glob.glob(fGlobArg)
            self.log(f'{fGlobArg=}')
            self.LOG_ID = 1 + self.getFileSeqNum(fGlob, fsfx)
            fsfx          = f'.{self.LOG_ID}{fsfx}'
            self.log(f'fGlob={util.fmtl(fGlob)}', pfx=0)
            self.log(f'{fsfx=}')
        return util.getFilePath(BASE_NAME, BASE_PATH, fdir=fdir, fsfx=fsfx)

    def getFileSeqNum(self, files, sfx, dbg=1, dbg2=1):
        i = -1
        if len(files):
            if dbg2: self.log(f'{sfx=} files={util.fmtl(files)}')
            ids =  [ self.sid(s, sfx) for s in files if s.endswith(sfx) ]
            if dbg:  self.log(f'ids={util.fmtl(ids)}')
            i = max(ids)
        return i
    @staticmethod
    def sid(s, sfx): s = s[:-len(sfx)]   ;   j = s.rfind('.')   ;   return int(s[j+1:])
    ####################################################################################################################################################################################################
    def log(self, msg='', pfx=1, pos=0, file=None, flush=False, sep=',', end='\n', so=0):
        if   file is None: file = LOG_FILE
        if   pos: msg = f'{self.fmtPos()}' + f' {msg}' # if msg else
        util.slog(msg, pfx, file, flush, sep, end, so)
    ####################################################################################################################################################################################################
    def quit(self, why='', error=1, save=1, dbg=1): #, dbg2=1):
        util.dumpStack(inspect.stack(), file=LOG_FILE)    ;   self.log(util.QUIT_BGN,     pfx=0)
        self.dumpTniksSfx(why)
        if not error:      util.dumpStack(util.MAX_STACK_FRAME, file=LOG_FILE)
        self.log(f'BGN {why} {error=} {save=}')           ;   self.log(util.QUIT_BGN, pfx=0)
        self.dumpArgs()
        if not error:
#            if   dbg:  self.dumpStruct(why)
            if save:   self.saveDataFile(why, self.dataPath1)
            if   dbg:  self.A_transposeData(dump=dbg) if self.TRANSPOSE_A else self.OLD_transposeData()
            if   dbg:  self.cobj.dumpMlimap(why)
        if self.SNAPS: self.snapshot(f'quit {error=} {save=}', 'QUIT')
        self.log(f'END {why} {error=} {save=}')           ;   self.log(util.QUIT_END, pfx=0)
        self.cleanupLog()
        self.close()
        pyglet.app.exit()
    ####################################################################################################################################################################################################
    def cleanupCat(self, dump=1):
        self.log(f'BGN {dump=}')
        if   dump and self.CAT: self.cobj.dumpOMAP(str(self.catPath), merge=1)
        elif dump:              self.cobj.dumpOMAP(None, merge=1)
        if self.CAT:
            cfp = self.getFilePath(seq=0, fdir='cats', fsfx='.cat')
            util.copyFile(self.catPath, cfp, file=LOG_FILE)
        self.log(f'END {dump=}')

    def cleanupLog(self):
        self.log(f'Copying {LOG_FILE.name} to {self.lfSeqPath}')
        util.copyFile(LOG_PATH, self.lfSeqPath, LOG_FILE)
        self.log(f'closing {LOG_FILE.name}', flush=True)
        LOG_FILE.close()

########################################################################################################################################################################################################
#                    0   1   2   3   4   5   6   7    8    9    10   11   12   13   14   15   16   17
OPACITY          = [ 0, 15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165, 170, 195, 210, 225, 240, 255 ]
CC3              = [(250, 65,  190, OPACITY[10]), (127,  30,  90, OPACITY[10])]
CC4              = [(255, 127, 255, OPACITY[10]), (150,  75,  12, OPACITY[10])]
CC1              = [( 13,  15, 255, OPACITY[10]), (250,  220, 27, OPACITY[10])]
CC2              = [(255, 127,   0, OPACITY[ 9]), ( 127,  58,  0, OPACITY[ 9])]
GRAY             = [(255, 255, 255, OPACITY[17]), (  0,   0,   0, OPACITY[17])]
PINK             = [(255,  64, 192, OPACITY[17]), ( 57,  16,  16, OPACITY[17])]
INFRA_RED        = [(200, 100,  24, OPACITY[17]), ( 68,  20,  19, OPACITY[17])]
RED              = [(255,   0,   0, OPACITY[17]), ( 50,   0,   0, OPACITY[17])]
ORANGE           = [(255, 127,   0, OPACITY[17]), ( 50,  25,   0, OPACITY[17])]
YELLOW           = [(255, 255,   0, OPACITY[17]), ( 45,  45,   0, OPACITY[17])]
GREEN            = [(  0, 255,   0, OPACITY[17]), (  0,  54,   0, OPACITY[17])]
GREEN0           = [(180, 255, 180, OPACITY[17]), ( 64, 100,  64, OPACITY[17])]
GREEN_BLUE       = [( 24, 255,  98, OPACITY[17]), ( 10,  49,  25, OPACITY[17])]
CYAN             = [( 13, 255, 255, OPACITY[17]), ( 16,  64,  64, OPACITY[17])]
BLUE_GREEN       = [(  0,  64, 255, OPACITY[17]), (  0,  32, 127, OPACITY[17])]
BLUE             = [(  0,   0, 255, OPACITY[17]), (  0,   0,  64, OPACITY[17])]
INDIGO           = [(255,  22, 255, OPACITY[17]), ( 19,  11,  64, OPACITY[17])]
VIOLET           = [(176,   0, 255, OPACITY[17]), (100,   0, 127, OPACITY[17])]
ULTRA_VIOLET     = [(194,  96, 255, OPACITY[17]), ( 50,  19,  61, OPACITY[17])]
GRAY0            = [(  0,   0,   0, OPACITY[ 0]), (  0,   0,   0, OPACITY[ 0])]
GRAY2            = [(255, 255, 255, OPACITY[10]), (  0,   0,   0, OPACITY[10])]
PINK2            = [(255,  64, 192, OPACITY[ 3]), ( 57,  16,  28, OPACITY[ 3])]
RED2             = [(255,   0,   0, OPACITY[ 3]), ( 50,   0,   0, OPACITY[ 3])]
ORANGE2          = [(255, 127,   0, OPACITY[10]), ( 50,  25,   0, OPACITY[10])]
YELLOW2          = [(255, 255,   0, OPACITY[15]), ( 45,  45,   0, OPACITY[15])]
GREEN2           = [(  0, 255,   0, OPACITY[10]), (  0,  54,   0, OPACITY[10])]
CYAN2            = [(  0, 255, 255, OPACITY[10]), (  0,  44,  44, OPACITY[10])]
BLUE2            = [(  0,   0, 255, OPACITY[10]), (  0,   0,  64, OPACITY[10])]
VIOLET2          = [(176,  81, 255, OPACITY[10]), ( 44,  14,  58, OPACITY[10])]
########################################################################################################################################################################################################
def genColors(k, nsteps=16, dbg=1):
    colors, clen = [], len(k[0])
    diffs = [ k[1][i] - k[0][i]  for i in range(clen) ]
    steps = [ diffs[i]/nsteps    for i in range(clen) ]
    if dbg: util.slog(f'c1={k[0]} c2={k[1]} nsteps={nsteps} diffs={diffs} steps=', end='')  ;  util.slog(f'[{steps[0]:6.1f} {steps[1]:6.1f} {steps[2]:6.1f} {steps[3]:6.1f}]')
    for j in range(nsteps):
        c = tuple([ fri(k[0][i] + j * steps[i]) for i in range(len(k[0])) ])
        if dbg: util.slog(f'c[{j}]={c}')
        colors.append(c)
    if dbg: util.slog(f'colors={k}')
    return colors
def fri(f): return int(math.floor(f + 0.5))
########################################################################################################################################################################################################
COLORS        = []
GRAYS         = genColors(GRAY)          ;  COLORS.append(GRAYS)
PINKS         = genColors(PINK)          ;  COLORS.append(PINKS)
INFRA_REDS    = genColors(INFRA_RED)     ;  COLORS.append(INFRA_REDS)
REDS          = genColors(RED)           ;  COLORS.append(REDS)
ORANGES       = genColors(ORANGE)        ;  COLORS.append(ORANGES)
YELLOWS       = genColors(YELLOW)        ;  COLORS.append(YELLOWS)
GREENS        = genColors(GREEN)         ;  COLORS.append(GREENS)
GREEN_BLUES   = genColors(GREEN_BLUE)    ;  COLORS.append(GREEN_BLUES)
CYANS         = genColors(CYAN)          ;  COLORS.append(CYANS)
BLUE_GREENS   = genColors(BLUE_GREEN)    ;  COLORS.append(BLUE_GREENS)
BLUES         = genColors(BLUE)          ;  COLORS.append(BLUES)
INDIGOS       = genColors(INDIGO)        ;  COLORS.append(INDIGOS)
VIOLETS       = genColors(VIOLET)        ;  COLORS.append(VIOLETS)
ULTRA_VIOLETS = genColors(ULTRA_VIOLET)  ;  COLORS.append(ULTRA_VIOLETS)
CC1S          = genColors(CC1)           ;  COLORS.append(CC1S)
CC2S          = genColors(CC2)           ;  COLORS.append(CC2S)
CC3S          = genColors(CC3)           ;  COLORS.append(CC3S)
CC4S          = genColors(CC4)           ;  COLORS.append(CC4S)
GRAY0S        = genColors(GRAY0)         ;  COLORS.append(GRAY0S)
GRAY2S        = genColors(GRAY2)         ;  COLORS.append(GRAY2S)
PINK2S        = genColors(PINK2)         ;  COLORS.append(PINK2S)
RED2S         = genColors(RED2)          ;  COLORS.append(RED2S)
ORANGE2S      = genColors(ORANGE2)       ;  COLORS.append(ORANGE2S)
YELLOW2S      = genColors(YELLOW2)       ;  COLORS.append(YELLOW2S)
GREEN2S       = genColors(GREEN2)        ;  COLORS.append(GREEN2S)
CYAN2S        = genColors(CYAN2)         ;  COLORS.append(CYAN2S)
BLUE2S        = genColors(BLUE2)         ;  COLORS.append(BLUE2S)
VIOLET2S      = genColors(VIOLET2)       ;  COLORS.append(VIOLET2S)
GREEN0S       = genColors(GREEN0)        ;  COLORS.append(GREEN0S)
FONT_SCALE    =  14/18  # 14pts/18pix
FONT_DPIS     = [72, 78, 84, 90, 96, 102, 108, 114, 120]
FONT_NAMES    = ['Lucida Console', 'Helvetica', 'Arial', 'Times New Roman', 'Courier New', 'Century Gothic', 'Bookman Old Style', 'Antique Olive']
FONT_COLORS_S = [PINKS[0], CYANS[0], REDS[0], BLUES[0], YELLOWS[0], GREENS[0], ORANGES[0], VIOLETS[0], REDS[13], YELLOWS[15], GREEN_BLUES[8], ORANGES[12], INDIGOS[8], ULTRA_VIOLETS[9], BLUE_GREENS[8], GRAYS[8]]
FONT_COLORS_L = [PINKS[0], GRAYS[0], BLUES[0], GREENS[0], YELLOWS[0], REDS[0], GRAYS[1], PINKS[8], REDS[10], YELLOWS[15], GRAYS[8], GRAYS[8], INDIGOS[8], GRAYS[9], GRAYS[8], GRAYS[8]]
FONT_COLORS   =  FONT_COLORS_S # if self.SPRITES else FONT_COLORS_L
########################################################################################################################################################################################################

if __name__ == '__main__':
    prevPath = util.getFilePath(BASE_NAME, BASE_PATH, fdir='logs', fsfx='.blog')
    LOG_PATH = util.getFilePath(BASE_NAME, BASE_PATH, fdir='logs', fsfx='.log')
    if LOG_PATH.exists(): util.copyFile(LOG_PATH, prevPath, LOG_FILE)
    with open(   str(LOG_PATH), 'w', encoding='utf-8')  as  LOG_FILE:
        util.slog(f'{LOG_PATH=}',      file=LOG_FILE)
        util.slog(f'{LOG_FILE.name=}', file=LOG_FILE)
        _   = Tabs()
        ret = pyglet.app.run()
        print(f'{ret=}')
