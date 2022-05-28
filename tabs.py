#import logging#, shutil#, unicodedata, readline, csv, string
import glob, inspect, itertools, math, os, pathlib, sys
import pyglet
import pyglet.sprite as pygsprt
import pyglet.text as pygtxt
import pyglet.window.event as pygwine
import pyglet.window.key as pygwink
import chord, util

########################################################################################################################################################################################################
def dumpGlobals():
    util.slog(f'argv      = {util.fmtl(sys.argv, ll=1)}', file=LOG_FILE)
    util.slog(f'PATH      = {PATH}', file=LOG_FILE)
    util.slog(f'BASE_PATH = {BASE_PATH}', file=LOG_FILE)
    util.slog(f'BASE_NAME = {BASE_NAME}', file=LOG_FILE)
########################################################################################################################################################################################################
AUTO_SAVE = 0  ;  CAT = 0  ;  EVENT_LOG = 0  ;  IND = 0  ;  RESIZE = 1  ;  SEQ_FNAMES = 1  ;  SNAP = 0  ;  VERBOSE = 0  ;  EXIT = 0
########################################################################################################################################################################################################
PATH             = pathlib.Path.cwd() / sys.argv[0]
BASE_PATH        = PATH.parent
BASE_NAME        = BASE_PATH.stem
SNAP_DIR         = 'snaps'
SNAP_SFX         = '.png'
LOG_FILE         = None   ;   Z = ' '
FDL              = ' len(data 0 00 000)'
FDT              = 'type(data 0 00 000)'
P, L, S, C       =  0,  1,  2,  3
T, N, I, K       =  4,  5,  6,  7
O, A, D          =  8,  9, 10
LR, LC, H        = 11, 12, 13
TT, NN, II, KK   =  0,  1,  2,  3
C1,  C2,  RLC    =  0,  1,  2
JTEXTS           = ['Page',  'Line',  'Sect',  'Col',  'Tab',  'Note',  'IKey',  'Kord',  '_SNo',  '_SNm',  '_Cpo',  '_LLR',  '_LLC', 'Curs', '_TNIK']
jTEXTS           = ['pages', 'lines', 'sects', 'cols', 'tabs', 'notes', 'ikeys', 'Kords', 'snos', 'snas', 'capos', 'lrows', 'lcols', 'curs', 'tniks']
JFMT             = [1, 2, 2, 3,  4, 4, 4, 4,  2, 2, 2,  2, 3, 1, 4]
NORMAL_STYLE, CURRENT_STYLE, SELECT_STYLE, COPY_STYLE = 0, 1, 2, 3
INIT             = '###   Init   ###' * 13
QUIT_BGN         = '###   BGN Quit   ###' * 10
QUIT             = '###   Quit   ###' * 13
QUIT_END         = '###   END Quit   ###' * 10
CSR_MODES        = ['MELODY', 'CHORD', 'ARPG']
HARROWS, VARROWS = ['LEFT', 'RIGHT'], ['UP', 'DOWN']
MELODY, CHORD, ARPG   = 0, 1, 2
LEFT, RIGHT, UP, DOWN = 0, 1, 0, 1
FS_MAX = 50
########################################################################################################################################################################################################
class Test:
    def __init__(self, a, file=None): self._a = a  ;  util.slog(f'<Test_init_:     _a={self._a}>', pfx=1, file=file)
    @property
    def a(self, file=None):       util.slog(f'<Test_prop_a:     _a={self._a}>', pfx=1, file=file)
    @a.setter
    def a(self, a, file=None):    self._a = a  ;  util.slog(f'<Test_set_a:     _a={self._a}>', pfx=1, file=file)
    @a.getter
    def a(self, file=None):       util.slog(f'<Test_get_a:     _a={self._a}>', pfx=1, file=file)  ;  return self._a
    @a.deleter
    def a(self, file=None):       util.slog(f'<Test_del_a: del _a>', pfx=1, file=file)  ;  del self._a
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

    def test2(self):
        self.log(f'os.path.abspath(".")     ={os.path.abspath(".")}')
        self.log(f'os.path.abspath("./")    ={os.path.abspath("./")}')
        self.log(f'os.path.abspath("../")   ={os.path.abspath("../")}')
        self.log(f'os.path.abspath("./Lib") ={os.path.abspath("./Lib")}')
        self.log(f'os.path.abspath("../Lib")={os.path.abspath("../Lib")}')
        self.log( 'sys.path:')
        for p in sys.path:
            self.log(f'{p}', pfx=0)

    def dumpGlobalFlags(self):
        txt1 = f'AUTO_SAVE={AUTO_SAVE} CAT={CAT} EVENT_LOG={EVENT_LOG} IND={IND} '
        txt2 = f'RESIZE={RESIZE} SEQ_FNAMES={SEQ_FNAMES} SNAP+{SNAP} VERBOSE={VERBOSE}'
        self.log(f'{txt1} {txt2}', pfx=0)

    def __init__(self):
        dumpGlobals()
        snapGlobArg = str(BASE_PATH / SNAP_DIR / BASE_NAME) + '.*' + SNAP_SFX
        snapGlob    = glob.glob(snapGlobArg)
        self.log(f'STFILT:\n{util.fmtl(util.STFILT)}')
        self.log(f'BGN {__class__}')
        self.dumpGlobalFlags()
        self.log(f'snapGlobArg =  {snapGlobArg}')
        self.log(f'   snapGlob = { util.fmtl(snapGlob)}')
        self.deleteGlob(snapGlob, 'SNAP_GLOB')
        self.catPath = str(BASE_PATH / 'cats' / BASE_NAME) + '.cat'
        self.catPath = self.getFilePath(seq=1, filedir='cats', filesfx='.cat')
        self.log(f'catPath={self.catPath}')
        self.shiftingTabs = 0   ;   self.shiftSign = 1
        self.inserting    = 0   ;   self.insertStr = ''
        self.jumping      = 0   ;   self.jumpStr   = ''   ;   self.jumpAbs = 0
        self.swapping     = 0   ;   self.swapSrc   = ''   ;   self.swapTrg = ''
        self.dfn = ''
        self.allSelected    = 0
        self.dataHasChanged = 0
        self.hArrow, self.vArrow,  self.csrMode                                 = RIGHT, UP, CHORD    ;    self.dumpCursorArrows('init()')
        self.tblank, self.tblanki, self.tblankCol,   self.cursor,  self.data    = None, None, None, None, []
        self.J1,     self.J2,      self.cc, self.ki, self.SNAP0,   self.armSnap = None, None, 0, 0, 0, ''
        self.kbk,    self.symb,    self.mods,        self.symbStr, self.modsStr =             0, 0, 0, '', ''
        self.CHECKER_BOARD, self.FULL_SCREEN, self.ORDER_GROUP, self.SPRITES, self.SUBPIX  = 0, 0, 0, 0, 0
        self.LL           = 0
        self.SS           = set() if 0 else {0}
        self.ZZ           = set() if 1 else {0, 1}
        nt                = 6
        self.n            = [2, 2, self.ssl(), 50, nt]
        self.i            = [1, 1,     1,       1, nt]
        ARGS = util.parseCmdLine(file=LOG_FILE)
        self.log(f'argMap={util.fmtm(ARGS)}')
        if 'f' in ARGS and len(ARGS['f'])  > 0:    self.dfn =       ARGS['f'][0]
        if 'n' in ARGS and len(ARGS['n'])  > 0:    self.n   = [ int(ARGS['n'][i]) for i in range(len(ARGS['n'])) ]
        if 'i' in ARGS and len(ARGS['i'])  > 0:    self.i   = [ int(ARGS['i'][i]) for i in range(len(ARGS['i'])) ]
        if 'F' in ARGS and len(ARGS['F']) == 0: self.FULL_SCREEN =  1
        if 'g' in ARGS and len(ARGS['g']) == 0: self.ORDER_GROUP =  1
        if 'x' in ARGS and len(ARGS['x']) == 0:      self.SUBPIX =  1
        if 'S' in ARGS and len(ARGS['S']) == 0:     self.SPRITES =  1
        if 'l' in ARGS and len(ARGS['l']) == 0:          self.LL =  1
        if 's' in ARGS and len(ARGS['s']) >= 0:          self.SS = { int(ARGS['s'][i]) for i in range(len(ARGS['s'])) }
        if 'z' in ARGS and len(ARGS['z']) >= 0:          self.ZZ = { int(ARGS['z'][i]) for i in range(len(ARGS['z'])) }
        self.dumpArgs()
        self.sAlias = 'GUITAR_6_STD'
        self.sobj = util.Strings(LOG_FILE, self.sAlias)
        self.cobj = chord.Chord(LOG_FILE, self.sobj)
        util.Note.setType(util.Note.SHARP)  ;  self.log(f' Note.TYPE={util.Note.TYPE}')
        self.n[S] = self.ssl()
        self._initDataPath()
        if CAT: self.cobj.dumpOMAP(str(self.catPath))
        self._initWindowA()
        self.log(f'WxH={self.fmtWxH()}')
        super().__init__(screen=self.screens[1], fullscreen=self.FULL_SCREEN, resizable=True, visible=False)
        self.log(f'WxH={self.fmtWxH()}')
        self._initWindowB()
        self.log(f'WxH={self.fmtWxH()}')
        self._reinit()
        self.log(f'END {__class__}')
        self.log(f'{INIT}', pfx=0)

    def dumpArgs(self):
        self.log(f'[f]            f={          self.dfn}')
        self.log(f'[n]            n={util.fmtl(self.n, util.FMTN)}')
        self.log(f'[i]            i={util.fmtl(self.i, util.FMTN)}')
        self.log(f'[F]  FULL_SCREEN={          self.FULL_SCREEN}')
        self.log(f'[g]  ORDER_GROUP={          self.ORDER_GROUP}')
        self.log(f'[x]       SUBPIX={          self.SUBPIX}')
        self.log(f'[S]      SPRITES={          self.SPRITES}')
        self.log(f'[l]           LL={          self.LL}')
        self.log(f'[s]           SS={util.fmtl(self.SS)}')
        self.log(f'[z]           ZZ={util.fmtl(self.ZZ)}')

    def _reinit(self):
        self.log('BGN')
        self.pages, self.lines, self.sects, self.cols  = [], [], [], []  ;  self.A = [self.pages, self.lines, self.sects, self.cols]
        self.tabs,  self.notes, self.ikeys, self.kords = [], [], [], []  ;  self.B = [self.tabs,  self.notes, self.ikeys, self.kords]
        self.snos,  self.snas,  self.capos             = [], [], []      ;  self.C = [self.snos,  self.snas,  self.capos]
        self.lrows, self.lcols, self.cursr             = [], [], []      ;  self.D = [self.lrows, self.lcols, self.cursr]
        self.E = [*self.A, *self.B, *self.C, *self.D]
        self.log(f'E={util.fmtl(self.E)}')
        self.resetJ('_reinit')
        self.data = []   ;    self.dataHasChanged = 0
        self.cursor,  self.caret   = None, None
        self.kbk,     self.symb, self.mods,  self.symbStr, self.modsStr = 0, 0, 0, '', ''
        self.cc,      self.ki,   self.SNAP0, self.armSnap               = 0, 0, 0, ''
        self.tblanki, self.tblanks  = 1, [' ', '-']                ;     self.tblank = self.tblanks[self.tblanki]
        self.tblankCol              = self.tblank * self.n[T]      ;  self.tblankRow = self.tblank * (self.n[C] + self.zzl())
        self._init()
        self.log('END')

    def _init(self, dbg=0):
        self.ssi = 0
        self._initColors()
        self._initData()
        if AUTO_SAVE: pyglet.clock.schedule_interval(self.autoSave, 10, how='autoSave timer')
        self._initFonts()
        self._initTextLabels()
        self._initTniks()
        if dbg: self.dumpStruct('_init()')

    def _initColors(self):
        KT1, KT2, KT3 = PINKS, BLUES, INDIGOS
        kP  = [    VIOLETS[0],    VIOLETS[12]] if self.CHECKER_BOARD else [   VIOLETS[10]]
        kL  = [     BLUES[12],      BLUES[15]] if self.CHECKER_BOARD else [     BLUES[12]]
        kS  = [     CYANS[12],      CYANS[15]] if self.CHECKER_BOARD else [     CYANS[12]]
        kC  = [      GRAYS[9],      GRAYS[13]] if self.CHECKER_BOARD else [     GRAYS[13]]
        kT  = [    ORANGES[0],     ORANGES[8]] if self.CHECKER_BOARD else [    ORANGES[0]]
        kN  = [     GREENS[0],     GREENS[12]] if self.CHECKER_BOARD else [     GREENS[0]]
        kI  = [    YELLOWS[0],     YELLOWS[8]] if self.CHECKER_BOARD else [    YELLOWS[0]]
        kK  = [      CYANS[0],       CYANS[8]] if self.CHECKER_BOARD else [      CYANS[0]]
        kO  = [       KT1[0],          KT1[8]] if self.CHECKER_BOARD else [        KT1[0]]
        kA  = [       KT2[0],          KT2[8]] if self.CHECKER_BOARD else [        KT2[4]]
        kD  = [       KT1[0],          KT1[8]] if self.CHECKER_BOARD else [        KT1[0]]
        kLR = [      BLUES[0],       BLUES[8]] if self.CHECKER_BOARD else [      BLUES[0]]
        kLC = [      PINKS[0],       PINKS[8]] if self.CHECKER_BOARD else [      PINKS[0]]
        kH  = [      PINKS[0],      YELLOWS[8],       GREENS[0],             REDS[0]]
        self.k   = [ kP, kL, kS, kC,  kT, kN, kI, kK,  kO, kA, kD,  kLR, kLC, kH ]
#        [ self.log(f'[{i:2}] {util.fmtl(*e):3}') for i, e in enumerate(self.k) ]
        for i, e in enumerate(self.k):
            self.log(f'[{i:2}] {util.fmtl(e, w=(3, 3, 3, 3))}')

    def _initData(self, dbg=1):
        self._initDataPath()
        if not self.dataPath1.exists(): self.log(f'dataPath1={self.dataPath1} file does not exist calling initBlankFileData()')  ;  self.dataPath1.touch()  ;  self.initBlankFileData()
        else:                           self.readDataFile()
        old = f'{util.fmtl(self.n)}'    ;    self.n[P], self.n[L], self.n[C], self.n[T] = self.data2plrc()   ;   self.log(f'reseting from n={old} to n={util.fmtl(self.n)}')
        self._initTpz()
        self.syncBlanks()
        if dbg: self.transposeDataDump()
        if EXIT: self.quit('EXIT TEST')
        self.saveDataFile('_initData()', f=2)

    def _initDataPath(self):
        dataDir  = 'data'  ;  dataSfx = '.dat'  ;  dataPfx = f'.{self.n[C]}'
        baseName  = self.dfn if self.dfn else BASE_NAME + dataPfx + dataSfx
        dataName0 = baseName + '.asv'
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

    def _initTniks(self, dbg=0, dbg2=0):
        self.ssl()
        self.smap = {}
        self.createTniks()
        if dbg: self.cobj.dumpMlimap('init')
        if dbg2: self.dumpTniks('New')
    ####################################################################################################################################################################################################
    def _initWindowA(self, dbg=1):
        display      = pyglet.canvas.get_display()
        if dbg: self.log(f'BGN {self.fmtWxH()}')  ;  self.log(f'display={display}')
        self.screens = display.get_screens()  ;  s = self.screens
        if dbg:
            for i in range(len(s)): self.log(f'screens[{i}] x={s[i].x} y={s[i].y:5} {self.fmtWxH(s[i].width, s[i].height)}')
            self.log(f'END {self.fmtWxH()}')

    def _initFonts(self):
        np, nl, ns, nc, nt = self.n  ;  nc += self.zzl()
        n = nl * nt * ns if ns else nl * nt
        pix = self.height / n
        fs = self.pix2fontsize(pix)
        self.fontBold, self.fontItalic, self.fontColorIndex, self.fontDpiIndex, self.fontNameIndex, self.fontSize = 0, 0, 0, 4, 0, fs
        self.log(f'pix=height/n={self.height}/{n}={pix} nl={nl} ns={ns} nt={nt} FONT_SCALE={FONT_SCALE} fs=pix*FONT_SCALE={fs:5.2f}pt')
        self.dumpFont()

    def _initWindowB(self, dbg=1):
        if dbg: self.log(f'BGN {self.fmtWxH()}')
        self.batch = pyglet.graphics.Batch()
        self._initGroups()
        self.set_visible()
        self.log(f'get_size={self.get_size()}')
        if EVENT_LOG and VERBOSE:
            self.eventLogger = pygwine.WindowEventLogger()
            self.push_handlers(self.eventLogger)
#            self.keyboard = pygwine.key.KeyStateHandler()
#            self.push_handlers(self.keyboard)
        if dbg: self.log(f'END {self.fmtWxH()}')
    ####################################################################################################################################################################################################
    def _initGroups(self):
        self.g = []   ;   self.gn = [0, 1, 2, 3,  4, 4, 4, 4,  4, 4, 4,  4, 4, 5]
        for i in range(len(self.n)+3):
            p = None if self.ORDER_GROUP or i==0 else self.g[i-1]
            self.g.append(self._initGroup(i, p))
            self.log(f'({i}) g={self.g[i]} pg={self.g[i].parent}')
    def _initGroup(self, order=0, parent=None): return pyglet.graphics.OrderedGroup(order, parent) if self.ORDER_GROUP else pyglet.graphics.Group(parent)
    ####################################################################################################################################################################################################
    def _initTextLabels(self):
        self.labelTextA, self.labelTextB = [], []
        self.createLabelText()
        self.labelTextC = []  ;  self.labelTextC.append('M')         ;  self.labelTextC.extend(self.labelTextB)
        self.labelTextD = []  ;  self.labelTextD.extend(['R', 'M'])  ;  self.labelTextD.extend(self.labelTextB)
        self.llText = []
        self.llText.append(self.labelTextB)
        self.llText.append(self.labelTextC)
        self.llText.append(self.labelTextD)
        txt = ['    ', '  ', '']  ;  [ self.log(f'llText[{i}]={txt[i]}{util.fmtl(t)}', pfx=0) for i, t in enumerate(self.llText) ]

    def _initTpz(self, dbg=1):
        np, nl, ns, nc, nt = self.n
        self.tpc =  nt
        self.tps =  nc * self.tpc
        self.tpl =       self.tps
        self.tpp =  nl * self.tpl
        if dbg: self.log(f'tpz={util.fmtl(self.tpz())}')
    def tpz(self):   return self.tpp, self.tpl, self.tps, self.tpc
    ####################################################################################################################################################################################################
    def dl(  self, data=None): return list(map(len,  self.dplc(data)))
    def dt(  self, data=None): return list(map(type, self.dplc(data)))
    def dplc(self, data=None, p=0, l=0, c=0): data = data or self.data   ;   return data, data[p], data[p][l], data[p][l][c]
    def cnts(self):    return self.J2[:]
    def lenA(self):    return [ len(_) for _ in self.A ]
    def lenB(self):    return [ len(_) for _ in self.B ]
    def lenC(self):    return [ len(_) for _ in self.C ]
    def lenD(self):    return [ len(_) for _ in self.D ]
    def lenE(self):    return [ len(_) for _ in self.E ]
    def j(   self):    return [ i-1 if i else 0 for i in self.i ]
    def j2(  self):    return [ i-1 if i else 0 for j, i in enumerate(self.i)  if j != S ]
    def isV( self):    return 1 if self.J2[P] == self.i[P] else 0
    def j2g( self, j): return self.g[ self.gn[j] ]
    def setJ(    self, j, n):         self.J1[j] = n   ;  self.J2[j] += 1  ;  self.J1[-1] += 1  ;  self.J2[-1] += 1  ;  return j
    def setJdump(self, j, n, why=''): self.setJ(j, n)  ;  self.dumpTnik(self.E[j][self.J2[j]-1], j, why)  ;  return j
    def resetJ(self, why='', dbg=1): self.J1 = [ 0 for _ in range(len(self.E)+1) ]  ;  self.J2 = [ 0 for _ in range(len(self.E)+1) ]  ;  self.dumpJs(why) if dbg else None
    ####################################################################################################################################################################################################
    def ssl(self, dbg=0): l = len(self.SS)   ;   self.log(f'n={util.fmtl(self.n)} SS={util.fmtl(self.ss2sl())} l={l}') if dbg else None   ;   return l   # return 0-4
    def zzl(self, dbg=0): l = len(self.ZZ)   ;   self.log(f'n={util.fmtl(self.n)} ZZ={util.fmtl(self.zz2sl())} l={l}') if dbg else None   ;   return l   # return 0-2
    def ss2sl(self): return sorted(self.SS)
    def zz2sl(self): return sorted(self.ZZ)
    ####################################################################################################################################################################################################
    @staticmethod
    def fmtTcolor(t): k = ' '.join([ f'{k:3}' for k in t.color ])  ;  k += f' {t.opacity:3}'  if type(t) is pygsprt.Sprite else ''  ;   return k
    @staticmethod
    def fmtTfont(t):     return f'{t.dpi:3} {t.bold:1} {t.italic:1} {t.font_name}'
    @staticmethod
    def fmtTfontSize(t): return F'{t.font_size:2.0f}'
    @staticmethod
    def fmtTsprite(s):   return f'{s.scale_x:5.3f} {s.scale_y:5.3f}'  # b.image.anchor_x, b.image.anchor_y, b.scale,  b.rotation, b.group, b.group.parent
    @staticmethod
    def fmtTvisible(t):  return 'Vz' if t.visible else '  '
    @staticmethod
    def fmtTxywh(t):     return f'{t.x:7.2f} {t.y:7.2f} {t.width:7.2f} {t.height:7.2f}'
    ####################################################################################################################################################################################################
    def fmtdl( self, data=None): return f'{FDL}={util.fmtl(self.dl(data))}'
    def fmtdt( self, data=None): return f'{FDT}={util.fmtl(self.dt(data))}'
    def fmtJ1( self, w=None, d=0): w = w if w is not None else JFMT  ;  d1 = "" if not d else "["  ;  d2 ="" if not d else "]"  ;  return f'{util.fmtl(self.J1,     w=w, d1=d1, d2=d2)}'
    def fmtJ2( self, w=None, d=0): w = w if w is not None else JFMT  ;  d1 = "" if not d else "["  ;  d2 ="" if not d else "]"  ;  return f'{util.fmtl(self.J2,     w=w, d1=d1, d2=d2)}'
    def fmtLE( self, w=None, d=0): w = w if w is not None else JFMT  ;  d1 = "" if not d else "["  ;  d2 ="" if not d else "]"  ;  return f'{util.fmtl(self.lenE(), w=w, d1=d1, d2=d2)} {sum(self.lenE())}'
    def fPos(  self):  plct = self.j2()   ;   cc = self.plct2cc(*plct)   ;   cn = self.cc2cn(cc)   ;   return f'{util.fmtl(plct)} {cc:3} {cn:2}]'
    def fmtDxD(self, data=None,      d='x'): l = list(map(str, self.dl(data)))               ;   return f'({d.join(l)})'
    def fmtIxI(self, d='x'):                 l = list(map(str, self.i))   ;   del l[S:S+1]   ;   return f'({d.join(l)})'
    def fmtWxH(self, w=None, h=None, d='x'): w = w if w is not None else self.width  ;  h = h if h is not None else self.height  ;  return f'({w}{d}{h})'
    def fWxH_DxD(self):                      return f'{self.fmtDxD()} {self.fmtWxH()}'
    ####################################################################################################################################################################################################
    def dumpDataRead( self, p, l, s, t, sp, sl, ss, st, lp, ll, ls, lt, msg, msg2): self.log(f' {p}  {l} {s:2} {t:3}   {sp} {sl:2} {ss:3} {st:4}  {msg:12} {msg2}  {lp} {ll:2} {ls:3} {lt:4}', pfx=0)
    def dumpDataSlice(self, p, l, c, cc):
        for t in range(self.n[T]):
            ikeys = self.ikeys[cc+t].text if self.ikeys and len(self.ikeys) > cc+t else ''
            kords = self.kords[cc+t].text if self.kords and len(self.kords) > cc+t else ''
            self.log(f'{self.data[p][l][c]} [{cc+t}] {self.tabs[cc+t].text:2} {self.notes[cc+t].text:2} {ikeys:2} {kords:2}')
    @staticmethod
    def dumpObjs(objs, name, why=''): [ Tabs.dumpObj(o, name, why) for o in objs ]
    @staticmethod
    def dumpObj( obj,  name, why='', file=None): util.slog(f'{why} {name} ObjId {id(obj):x} {type(obj)}', file=file)
    def dumpJs(  self, why): self.log(f'  J1 {self.fmtJ1(0)} {why}')  ;  self.log(f'  J2 {self.fmtJ2(0)} {why}')  ;  self.log(f'  LE {self.fmtLE(0)} {why}')
    def dumpGeom(self, why1='', why2=''): self.log(f'{why1} {self.fmtDxD()} {self.fmtIxI()} {util.fmtl(self.ss2sl()):9} {self.LL} {util.fmtl(self.zz2sl()):5} J2={self.fmtJ2(0, 1)} {why2}')
    def dumpSmap(self, why, pos=0): self.log(f'{why} smap={util.fmtm(self.smap)}', pos=pos)
    ####################################################################################################################################################################################################
    def dumpStruct(self, why='', dbg=0, dbg2=1):
        self.dumpGeom(f'BGN {why} {self.fmtWxH()}')
        self.dumpFont(why)
        self.log(f'tpz={util.fmtl(self.tpz())}')
        self.dumpGlobalFlags()
        if not dbg2:     self.dumpJs(why)
        if dbg2:         self.dumpTniks(why)
        if dbg2 and dbg: self.dumpGeom(f'END {why} {self.fmtWxH()}')
        if dbg:          self.cobj.dumpMlimap(why)
        if dbg:          self.dumpGeom(f'END {why} {self.fmtWxH()}')
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

    def on_resize(self, width, height, why='', dbg=0):
        super().on_resize(width, height)   ;   why2 = 'Upd'
        if RESIZE: self.resizeTniks(f'{why2}{why}')
    ####################################################################################################################################################################################################
    def saveDataFile(self, how, f=0, dbg=1):
        if dbg:   self.log(f'{how} f={f}')
        if not f and AUTO_SAVE: dataPath = self.dataPath0
        else:                   dataPath = self.dataPath1 if f == 1 else self.dataPath2
        with open(dataPath, 'w') as DATA_FILE:
            self.log(f'{DATA_FILE.name:40}', pfx=0)
            np, nl, nc, nr = self.dl()
            data = self.transposeData() # if self.isVert() else self.data
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
    def readDataFile(self, dbg=1):
        np, nl, ns, nt = self.n[P], self.n[L], self.n[T], self.n[C]
        self.log(f'BGN {util.fmtl(self.n)} dataPath1={self.dataPath1}')
        with open(str(self.dataPath1), 'r') as DATA_FILE:
            DATA_FILE.seek(0, 2)    ;   size = DATA_FILE.tell()   ;   DATA_FILE.seek(0, 0)
            self.log(f'    {DATA_FILE.name:40} {size:8,} bytes = {size/1024:6,.1f} KB')
            if not size: self.log(f'WARN ZERO File Size size={size} call initBlankFileData()')   ;   return self.initBlankFileData()
            lines, strs = [], []   ;   sp, sl, ss, st = 0, 0, 0, 0   ;   txt = 'tabs'   ;   data = self.data
            if dbg: self.log(f' p  l  s   t  sp sl  ss   st  <{txt:10}>                      lp ll  ls   lt', pfx=0)
            for tabs in DATA_FILE:
                tabs = tabs.strip()    ;    msg = f'<{tabs}>'    ;  lt = len(tabs)
                p = sp % np  ;   l = sl % nl   ;   s = ss % ns   ;   t = st % nt
                if tabs:                strs.append(tabs)        ;  ss += 1  ;   st += lt   ;  self.dumpDataRead(p, l, s, t, sp, sl, ss, st, len(data), len(lines), len(strs), len(tabs), msg, '  strs.add(tabs) ')
                else:
                    if not (ss % ns):  lines.append(strs)        ;  sl += 1  ;   strs = []  ;  self.dumpDataRead(p, l, s, t, sp, sl, ss, st, len(data), len(lines), len(strs), len(tabs), msg, ' lines.add(strs) ')
                    if not (sl % nl):  data.append(lines)        ;  sp += 1  ;  lines = []  ;  self.dumpDataRead(p, l, s, t, sp, sl, ss, st, len(data), len(lines), len(strs), len(tabs), msg, ' pages.add(lines)')
            if dbg: self.log(f' p  l  s   t  sp sl  ss   st  <{txt:10}>                      lp ll  ls   lt', pfx=0)
        self.log(f'    read {sp} pages {sl} lines @ {nl} lines/page {ss} strs @ {ns} strs/line {st} tabs @ {nt} tabs/str {sp+sl+ss+st} objs')
        self.log(f'END {DATA_FILE.name:40} {size:8,} bytes = {size/1024:6,.1f} KB')

    def initBlankFileData(self):
        self.log('Creating tab data using parameters {} {} {} {} {}'.format(*self.n))
        np, nl, ns, nc, nr = self.n  ;  nc += self.zzl()
        self.data = [ [ [ self.tblankRow for _ in range(nr) ] for _ in range(nl) ] for _ in range(np) ]
    ####################################################################################################################################################################################################
    def isVert(self, data=None, dbg=1):
        dl, dt = self.dl(data), self.dt(data)
        if dbg: self.log(f'BGN {self.fmtdl()}')
        if dbg: self.log(f'    {self.fmtdt()}')
        assert dt[0] is list and dt[1] is list and dt[2] is list and dt[3] is str
        self.checkData(data)
        vert = 1 if dl[-2] > dl[-1] else 0
        if dbg: self.log(f'END {self.fmtdl()} vert={vert}')
        return vert

    def checkData(self, data=None):
        data = data or self.data   ;   dl = self.dl(data)
        for p in range(dl[0]):
            assert len(data[p]) == dl[1]
            for l in range(len(data[p])):
                assert len(data[p][l]) == dl[2]
                for c in range(len(data[p][l])):
                    assert len(data[p][l][c]) == dl[3]
    ####################################################################################################################################################################################################
    def transposeDataDump(self, data=None, why='External', pfx=0, dbg=1):
        self.dumpDataHorz(data)
        self.data = self.transposeData(data, why, pfx, dbg)
        self.dumpDataVert(data)

    def transposeData(self, data=None, why='External', pfx=0, dbg=1):
        data = data or self.data
        Xdata, msg1, msg2 = [], [], []
        self.log(f'BGN {self.fmtDxD(data)} {why}')
        self.log(f'dl={util.fmtl(self.dl(data))} dt={util.fmtl(self.dt(data))}') if dbg else None
        for p, page in enumerate(data):
            Xpage = []
            for l, line in enumerate(page):
                if dbg: _ = f'BFR {p} {l}' if pfx else ''   ;   msg1.append(f'{_}{util.fmtl( line, d1="")}')
                Xline = list(map(''.join, itertools.zip_longest(*line, fillvalue=' ')))
                if dbg: _ = f'BFR {p} {l}' if pfx else ''   ;   msg2.append(f'{_}{util.fmtl(Xline, d1="")}')
                Xpage.append(Xline)
            Xdata.append(Xpage)
        if dbg: [ self.log(m, pfx=0) for m in msg1 ]   ;   self.log(pfx=0)
        if dbg: [ self.log(m, pfx=0) for m in msg2 ]
        self.log(f'END {self.fmtDxD(Xdata)} {why}')
        return Xdata
    ####################################################################################################################################################################################################
    def dumpDataHorz(self, data=None, lc=1, ll=1, i=0):
        data = data or self.data
        self.log(f'BGN {self.fmtDxD(data)} lc={lc} ll={ll} i={i}')
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
        self.log(f'END {self.fmtDxD(data)} lc={lc} ll={ll} i={i}')

    def dumpDataVert(self, data=None, lc=1, ll=1, i=0):
        data = data or self.data
        w = max(len(data[0][0][0]), len(JTEXTS[P]) + 2, len(JTEXTS[L]) + 2)   ;   txt = Z * i + JTEXTS[C] + Z if i >= 0 else JTEXTS[C]
        self.log(f'BGN {self.fmtDxD(data)} lc={lc} ll={ll} i={i} w={w} txt={txt}')
        for p in range(len(data)):
            if ll: self.log(f'{JTEXTS[P]} {p+1}', pfx=0)  ;  self.log(f'{txt:{3}}', pfx=0, end='')  ;  txt2 = [ f'{JTEXTS[L]} {l+1}' for l in range(len(data[0])) ]  ;  self.log(f'{util.fmtl(txt2, w=w, d1="")}', pfx=0)
            for c in range(len(data[p][0])):
                pfx = f'{c+1:3} ' if i >= 0 and lc else ''   ;   self.log(f'{pfx}{Z*i}', pfx=0, end='')
                for l in range(len(data[p])):
                    self.log(f'{data[p][l][c]}', pfx=0, end=Z)
                self.log(pfx=0)
        self.log(f'END {self.fmtDxD(data)} lc={lc} ll={ll} i={i}')
    ####################################################################################################################################################################################################
    def dumDataLabels(self, data=None, i=0, sep='%'):
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
    def imap2ikey(self, tobj, imap, i, j, dbg=0):
        imap0 = imap[0][::-1] if imap and len(imap) else []   ;   ff = self.sobj.isFret(tobj)
        if imap0 and len(imap0) > i:                 ikey = tobj if j > K else imap0[i] if ff else self.tblank    ;   i += 1 if ff else 0
        else:                                        ikey = tobj if j > K else self.tblank
        if dbg: self.log(f'ikey={ikey}')
        return ikey

    def imap2Chord(self, tobj, imap, i, j, dbg=0):
        chunks = imap[4]  if (imap and len(imap) > 4) else []
        chordName  = tobj if j > K else chunks[i] if len(chunks) > i else self.tblank
        if dbg: self.log(f'chordName={chordName}')
        return chordName
    ####################################################################################################################################################################################################
    def toggleTTs(self, how, tt):
        msg2 = f'{how} tt={tt}'
        self.dumpGeom(f'BGN', f'     {msg2}')
        if   tt not in self.SS and not self.B[tt]: msg = 'ADD'    ;   self.addTTs( how, tt)
        elif tt     in self.SS:                    msg = 'HIDE'   ;   self.hideTTs(how, tt)
        else:                                      msg = 'SKIP'   ;   self.dumpGeom('   ', f'{msg} {msg2}')   ;   self.toggleTT(tt)
        self.on_resize(self.width, self.height, why='S', dbg=1)
        self.dumpGeom('END', f'{msg} {msg2}')

    def toggleZZs(self, how, zz):
        ii = 0 if not zz else 2
        msg2 = f'{how} zz={zz}'
        self.dumpGeom('BGN', f'     {msg2}')
        if   zz not in self.ZZ and not self.C[ii]: msg = 'ADD'    ;   self.addZZs( how, zz)
        elif zz     in self.ZZ:                    msg = 'HIDE'   ;   self.hideZZs(how, zz)
        else:                                      msg = 'SKIP'   ;   self.dumpGeom('   ', f'{msg} {msg2}')   ;   self.toggleZZ(zz)
        self.on_resize(self.width, self.height, dbg=1)
        self.dumpGeom('END', f'{msg} {msg2}')

    def toggleLLs(self, how, dbg=0):
        self.toggleLL()
        msg2 = f'{how} LL={self.LL}'
        self.dumpGeom('BGN', f'     {msg2}')
        if dbg: self.log(f'    llText={util.fmtl(self.llText[self.zzl()])}')
        if self.LL and not self.lrows: msg = 'ADD'    ;   self.addLLs( how)
        else:                     msg = 'HIDE'   ;   self.hideLLs(how)
        self.on_resize(self.width, self.height, dbg=1)
        self.dumpGeom('END', f'{msg} {msg2}')
    ####################################################################################################################################################################################################
    def toggleTT(self, tt, why=''):
        self.dumpGeom('BFR', why)
        self.SS.add(tt) if tt not in self.SS else self.SS.remove(tt)
        self.n[S] = self.ssl()
        self.dumpGeom('AFT', why)

    def toggleLL(self, why=''):
        self.dumpGeom('BFR', why)
        self.LL = int(not self.LL)
        self.dumpGeom('AFT', why)

    def toggleZZ(self, zz, why=''):
        self.dumpGeom('BFR', why)
        self.ZZ.add(zz) if zz not in self.ZZ else self.ZZ.remove(zz)
        self.dumpGeom('AFT', why)
    ####################################################################################################################################################################################################
    def hideTTs(self, how, i, dbg=1):
        why = f'HIDE {how} i={i}'  ;  why2 = 'Ref'
        np, nl, ns, nc, nt = self.n   ;   nc += self.zzl()
        self.dumpTniksPfx(why)
        for p in range(np):
            self.setJdump(P, p, why2)
            for l in range(nl):
                self.setJdump(L, l, why2)
                for s, s2 in  enumerate(self.ss2sl()):
                    z, j              = self.tnikInfo(s2)
                    if s2 != i:         self.setJdump(S, s2, why2)
                    else:               self.hideTnik(self.sects,   p*nl + l,                 S, dbg=dbg)
                    for c in range(nc):
                        if s2 != i:     self.setJdump(C, c,why2)
                        else:           self.hideTnik(self.cols,   (p*nl + l)*nc + c,         C, dbg=dbg)
                        for t in range(nt):
                            if s2 != i: self.setJdump(j, t, why2)
                            else:       self.hideTnik(         z, ((p*nl + l)*nc + c)*nt + t, j, dbg=dbg)
        if i == TT:                     self.hideTnik(self.cursr,                          0, H, dbg=dbg)
        self.dumpTniksSfx(why)
        self.toggleTT(i)
        if SNAP: self.snapshot(f'hideTTs() {why}')

    def hideZZs(self, how, i, dbg=1):
        why = f'HIDE {how} i={i}'  ;  why2 = 'Ref' # ;  c2, t2 = 0, 0
        np, nl, ns, nc, nt = self.n  ;  nc += self.zzl()  ;  ns = self.ssl()
        self.dumpTniksPfx(why)
        for p in range(np):
            self.setJdump(P, p, why2)
            for l in range(nl):
                self.setJdump(L, l, why2)
                for s, s2 in enumerate(self.ss2sl()):
                    self.setJdump(S, s2, why2)
                    for c in range(nc):
                        if c != i:     self.setJdump(C, c, why2)
                        else:          c2 = ((p*nl + l)*ns + s)*nc + c   ;   self.hideTnik(self.cols, c2, C, dbg=dbg)
                        for t in range(nt):
                            z, j           = self.tnikInfo(s2)
#                            if c != i: self.setJdump(j, t, why2)
                            if not (c % nc):
#                                self.log(f'p={p} l={l} s={s} c={c} t={t}  s2={s2} c2={c2} t2={t2}  _={c2//(ns*nc)} lz={len(z)} j={j} {JTEXTS[j]} {self.J1[j]} {self.J2[j]}')
                                self.hideTnik(z, self.J2[j], j, dbg=dbg)
        self.dumpTniksSfx(why)
        self.toggleZZ(i)

    def hideLLs(self, how):
        msg = f'HIDE {how}'
        nr = len(self.lrows)    ;  nc = len(self.lcols)
        assert not nc % nr      ;  nc = nc // nr  #  normalize
        self.dumpTniksPfx(msg)
        for r in range(nr):
            self.hideTnik(self.lrows, r, LR)
            for c in range(nc):
                self.hideTnik(self.lcols, c + r*nc, LC)
        self.dumpTniksPfx(msg)
    ####################################################################################################################################################################################################
    def addTTs(self, how, i):
        why = f'ADD {how} i={i}'  ;  why2 = 'Ref'
        self.toggleTT(i)
        np, nl, ns, nc, nt = self.n   ;   nc += self.zzl()
        self.dumpTniksPfx(why)
        for p in range(np):
            self.setJdump(P, p, why2)
            for l in range(nl):
                self.setJdump(L, l, why2)
                for s in self.ss2sl():
                    if s != i:
                        self.setJdump(S,  s, why2)   ;  z, j2 = self.tnikInfo(s)
                        for c in range(nc):
                            self.setJdump(C,  c, why2)
                            for t in range(nt):
                                self.setJdump(j2, t, why2)
                    else:
                        for _, sect in      enumerate(self.g_createTniks(self.sects, S, self.lines[l], ii=i)):
                            for _, col in   enumerate(self.g_createTniks(self.cols,  C, sect)):
                                for _, _ in enumerate(self.g_createTniks(self.tabs,  T, col, ii=i)):
                                    pass
        self.dumpTniksSfx(why)
        if self.tabs and not self.cursor: self.createCursor()

    def addZZs(self, how, i):
        why = f'ADD {how} i={i}'  ;  why2 = 'Ref'
        self.toggleZZ(i)
        np, nl, ns, nc, nt = self.n   ;   nc += self.zzl()
        self.dumpTniksPfx(why)
        for p in range(np):
            self.setJdump(P, p, why2)
            for l in range(nl):
                self.setJdump(L, l, why2)
                for s, s2 in     enumerate(self.ss2sl()):
                    self.setJdump(S, s2, why2)
                    for c, c2 in enumerate(self.g_createTniks(self.cols,     C, self.sects[s2], ii=i)):
                        if self.LL and self.isV() and not s:
                            n, _, x, y, w, h, = self.geom(C, self.lrows[l], 1)
                            lrCol = self.addLL(None, c, n, x, y, w, h)
                            ii = l * nc + i
                            self.log(f'ii={ii} l={l} i={i} nc={nc} LE={self.fmtLE()}')
                            self.lcols.insert(ii, lrCol)
                        for _ in           self.g_createTniks(self.tabs,     T,      c2,       ii=s2):
                            pass
        self.dumpTniksSfx(why)

    def addLLs(self, how):
        why = f'ADD {how}'  ;  why2 = 'Ref'
        np, nl = self.n[P], self.n[L]
        self.dumpTniksPfx(why)
        for p in range(np):
            self.setJdump(P, p, why2)
            for l in range(nl):
                i = p * nl + l
                self.setJdump(L, l, why2)
                if self.isV():          self.createLL(self.lines[i], i)
        self.dumpTniksPfx(why)
    ####################################################################################################################################################################################################
    def addLL(self, tlist, c, x, y, w, h, dbg=1):
        kl   = self.k[LC]   ;   kk  = self.cci(c, kl)
        text = self.llText[self.zzl()]
        txt  = text[c]
        return self.createTnik(tlist, c, LC, x+c*w, y, w, h, kk, kl=kl, t=txt, dbg=dbg)

    def addPage(self, how):
        self.log(f'BGN {how}')
        np, nl, ns, nc, nr = self.n  ;  nc += self.zzl()
        self.n[P] += 1
        self.log(f'n={util.fmtl(self.n)}')
        data = [ [ self.tblankRow for _ in range(nr) ] for _ in range(nl) ]
        self.data = self.transposeData()
        self.data.append(data)
        self.transposeDataDump()
        n, ii, x, y, w, h = self.geom(P)   ;   kl = self.k[P]
        self.dumpTniksPfx(how)
        page = self.createTnik(self.pages,    len(self.pages), P, x, y, w, h, self.cci(0, kl), kl=kl, dbg=1)
        for line in            self.g_createTniks(self.lines,  L, page):
            for sect in        self.g_createTniks(self.sects,  S, line):
                for col in     self.g_createTniks(self.cols,   C, sect):
                    for _ in   self.g_createTniks(self.tabs,   T, col):
                        pass
        self.dumpTniksPfx(how)
        self.log(f'END {how}')
    ####################################################################################################################################################################################################
    def createLL(self, p, pi, dbg=1, dbg2=1):
        klr = self.k[LR]  ;  kkr = self.cci(pi, klr)
        a = 1 + self.n[T] * self.ssl() * self.i[L]
        nr, ir, xr, yr, wr, hr = self.geom(S, p, n=a, dbg=dbg2)
        if   type(p) is pygsprt.Sprite:    xr, yr = self.sprite2LabelPos(xr,    yr, wr, hr)
        lrow = self.createTnik(self.lrows, pi, LR, xr, yr, wr, hr, kkr, kl=klr, dbg=dbg)
        nc, ic, xc, yc, wc, hc = self.geom(C, lrow,   dbg=dbg2)
        if   type(p) is pygsprt.Sprite:    xc, _  = self.sprite2LabelPos(xc-xr, yc, wc, hc)
        for c in range(nc):
            self.addLL(self.lcols, c, nc, xc, yc, wc, hc)
        self.squeeze (p, a, dbg=dbg)
        self.dumpTnik(p, L, why='Upd')
        return p

    def resizeLL(self, p, pi, dbg=1):
        a = 1 + self.n[T] * self.ssl() * self.i[L]
        nr, ir, xr, yr, wr, hr = self.geom(S, p, n=a, dbg=dbg)
        if   type(p) is pygsprt.Sprite:    xr, yr = self.sprite2LabelPos(xr,    yr, wr, hr)
        lrow = self.resizeTnik(self.lrows, self.J2[LR], LR, xr, yr, wr, hr)
        nc, ic, xc, yc, wc, hc = self.geom(C, lrow,   dbg=dbg)   ;   sc = nc * pi
        if   type(p) is pygsprt.Sprite:    xc, _  = self.sprite2LabelPos(xc-xr, yc, wc, hc)
        for c in range(nc):
            klc = self.k[LC]  ;   kk = self.cci(sc, klc)
            nz = self.zzl()   ;  lcs = self.lcols   ;   lc = len(lcs)
            if sc >= lc: self.createTnik(lcs, sc, LC, 0, 0, 0, 0, kk, klc, dbg=1)  ;  msg = f'ERROR Missing nz={nz} lrow={pi+1} c={c} sc={sc} lc={lc}'  ;  self.log(msg)  ;  self.quit(msg)
            self.resizeTnik(lcs, self.J2[LC], LC, xc+c*wc, yc, wc, hc)
        self.squeeze(p, a, dbg=dbg)
        return p
    ####################################################################################################################################################################################################
    def sprite2LabelPos(self, x, y, w, h): x += w/2  ;  y -= h/2  ;  self.log(f'x={x:6.2f} y={y:6.2f}')  ;  return x, y
    def squeeze(self, p, a, dbg=0):
        if   type(p) is pygtxt.Label:   p.y, p.height, g     = self.squeezeA(p.y, p.height, a)                  ;  self.log(f'p.y={p.y:6.2f} p.h={       p.height:6.2f} a={a} g={g:6.2f}') if dbg else None
        elif type(p) is pygsprt.Sprite: p.y, h, g, p.scale_y = self.squeezeB(p.y, p.height, a, p.image.height)  ;  self.log(f'p.y={p.y:6.2f} p.scale_y={p.scale_y:6.4f} a={a} h={h:6.2f}') if dbg else None
    def squeezeA(self, y, h, a):    self.log(f'y={y:6.2f} h={h:6.2f} a={a}', end=' ')             ;  c = h/a  ;  h -= c  ;  y -= c/2            ;  self.log(f'y={y:6.2f} h={h:6.2f} a={a} c={c:6.2f}', pfx=0)  ;  return y, h, c
    def squeezeB(self, y, h, a, g): self.log(f'y={y:6.2f} h={h:6.2f} a={a} g={g:6.4f}', end=' ')  ;  c = h/a  ;  h -= c  ;  y -= c  ;  g = h/g  ;  self.log(f'y={y:6.2f} h={h:6.2f} a={a} c={c:6.2f} g={g:6.4f}', pfx=0)  ;  return y, h, c, g
    def z1(self): nc = self.n[C] + self.zzl()  ;  return 1 if C1 in self.ZZ and (self.J1[C] % nc) == C1 else 0
    def z2(self): nc = self.n[C] + self.zzl()  ;  return 1 if C2 in self.ZZ and (self.J1[C] % nc) == C2 else 0
#    def z1(self): nc = self.n[C] + self.zzl()  ;  return 1 if (C1 in self.ZZ and (self.J1[C] % nc) == C1)   or    (C2 in self.ZZ and (self.J1[C] % nc) == C2) else 0
#    def z2(self): nc = self.n[C] + self.zzl()  ;  return 1 if (C2 in self.ZZ and (self.J1[C] % nc) == C2) and not (C1 in self.ZZ and (self.J1[C] % nc) == C1) else 0
    ####################################################################################################################################################################################################
    def createTniks(self):
        self.dumpTniksPfx()
        for page in              self.g_createTniks(self.pages, P, None):
            for line in          self.g_createTniks(self.lines, L, page):
                for sect in      self.g_createTniks(self.sects, S, line):
                    for col in   self.g_createTniks(self.cols,  C, sect):
                        for _ in self.g_createTniks(self.tabs,  T, col):
                            pass
        self.dumpTniksSfx()
        if self.tabs: self.createCursor()
    ####################################################################################################################################################################################################
    def g_createTniks(self, tlist, j, pt, ii=-1, dbg=1, dbg2=0):
        if j < 0 or j > T: msg = f'ERROR Invalid j={j}'              ;  self.log(msg)   ;   self.quit(msg)
        if not self.n[j]:  msg = f'WARN SKIP n[{j}]={self.n[j]}'     ;  self.log(msg)   ;   return
        p, l, s, c = self.J1[P], self.J1[L], self.J1[S], self.J1[C]  ;  kl = self.k[j]  ;  nz = self.zzl()  ;  text = ''
        imap = self.getImap(p, l, c - nz) if j == T and not self.z1() and not self.z2() else []
        n, _, x, y, w, h = self.geom(j, pt, dbg=dbg2)
        x2 = x  ;  y2 = y  ;  j2 = j  ;  tlist2 = tlist
        n = 1 if ii >= 0 and (j == S or j == C) else n
        for i in range(n):
            k = self.cci(i, kl)
            if   j2 == S:                            y2 = y - i * h  ;  sss = self.ss2sl()[i] if ii < 0 else ii  ;  self.SS.add(sss)  ;  k = self.cci(j, kl)
            elif j2 == C:                            x2 = x + i * w  ;  zzz = self.zz2sl()[i] if ii < 0 and i < nz else ii  ;  self.ZZ.add(zzz) if i < nz else None
            elif j2 >= T:
                y2 = y - i * h  ;  text = ''
                sss = self.ss2sl()[self.J1[S]] if ii < 0 else ii
                tlist2, j2, kl, tobj = self.tnikInfo(sss, i)
                if   sss == TT:                      text = tobj
                elif sss == NN:                      text = tobj if j2 > K else self.sobj.tab2nn(tobj, i) if self.sobj.isFret(tobj) else self.tblank
                elif sss == II:                      text = self.imap2ikey( tobj, imap, i, j2)
                elif sss == KK:                      text = self.imap2Chord(tobj, imap, i, j2)
            elif pt:                                 y2 = y - i * h
            yield self.createTnik(tlist2, i if ii < 0 else ii, j2, x2, y2, w, h, k, kl=kl, t=text, dbg=dbg)
    ####################################################################################################################################################################################################
    def createTnik(self, tlist, i, j, x, y, w, h, kk=0, kl=None, why='New', t='', v=None, g=None, ml=0, dbg=0):
        o, k, d, ii, n, s = self.fontParams()   ;   b = self.batch   ;   k2 = 0
        k = kl[kk] or FONT_COLORS[(k + k2) % len(FONT_COLORS)]
        v = v if v is not None else self.isV()
        g = g if g is not None else self.j2g(j)
        if (self.SPRITES and j < T) or j == H:
            scip = pyglet.image.SolidColorImagePattern(k)
            img  = scip.create_image(width=fri(w), height=fri(h))
            tnik = pygsprt.Sprite(img, x, y, batch=b, group=g, subpixel=self.SUBPIX)
            tnik.color, tnik.opacity = k[:3], k[3]   ;   tnik.visible = v
        else:
            s   *= v
            d, n = FONT_DPIS[d], FONT_NAMES[n]   ;   a, ax, ay = 'center', 'center', 'center' # left center right  # bottom baseline center top
            nz   = self.zzl()   ;   nc = self.n[C] + nz
            mp = len(tlist) % nc + 1 - nz if j == LC and tlist else 0
            if j == LC and not mp % 10 and i:   k = self.k[LR][0]
            if ml:                              t = [ t[:m] + '\n' + t[m:] for m in range(len(t), 0, -1) ]
            tnik = pygtxt.Label(t, font_name=n, font_size=s, bold=o, italic=ii, color=k, x=x, y=y, width=w, height=h, anchor_x=ax, anchor_y=ay, align=a, dpi=d, batch=b, group=g, multiline=ml)
        if tlist is not None:      tlist.append(tnik)
        self.setJ(j, i)       ;    self.dumpTnik(tnik, j, why) if dbg else None
        if self.LL and j == L and v:    tnik = self.createLL(tnik, i)
        return tnik
    ####################################################################################################################################################################################################
    def hideTnik(self, tlist, i, j, dbg=0):
        c = tlist[i]    ;    ha = hasattr(c, 'text')
        if   type(c) == pygtxt.Label:   c.x, c.y, c.width, c.height = 0, 0, 0, 0
        elif type(c) == pygsprt.Sprite: c.update(x=0, y=0, scale_x=0, scale_y=0)
        self.setJ(j, i)
        if dbg: self.dumpTnik(c, j, 'Hide')
        if dbg > 1:    text = c.text if ha else ''  ;  self.log(f'{JTEXTS[j]:4} {i+1:3} {id(c):x} {text:6} {c.x:7.2f} {c.y:7.2f} {c.width:7.2f} {c.height:7.2f}  J1={self.fmtJ1(0, 1)} J2={self.fmtJ2(0, 1)}', pfx=0)
    ####################################################################################################################################################################################################
    def resizeTniks(self, why=''):
        self.dumpTniksPfx(why)
        for page in              self.g_resizeTniks(self.pages, P):
            for line in          self.g_resizeTniks(self.lines, L, page):
                for sect in      self.g_resizeTniks(self.sects, S, line):
                    for col in   self.g_resizeTniks(self.cols,  C, sect):
                        for _ in self.g_resizeTniks(self.tabs,  T, col):
                            pass
        self.dumpTniksSfx(why)
        if self.cursor: self.resizeCursor()
    ####################################################################################################################################################################################################
    def g_resizeTniks(self, tlist, j, pt=None, dbg=1, dbg2=0):
        if not self.n[j]: msg = f'WARN SKIP n[{j}]={self.n[j]}'   ;   self.log(msg)   ;   return
        n, _, x, y, w, h = self.geom(j, pt, dbg=dbg2)
        x2 = x  ;  y2 = y  ;  j2 = j  ;  tlist2 = tlist # ;  sss = -1
        for i in range(n):
            if   j2 == S:                 y2 = y - i * h   ;  # i2 += 1 # ;  self.log(f'Updt j={j} {JTEXTS[j]} J1[S]={self.J1[S]} J2[S]={self.J2[S]} zz={zz} ss={util.fmtl(ss)} n={n} n2={n2} i2={i2-1}', pfx=0)
            elif j2 == C:                 x2 = x + i * w
            elif j2 >= T:
                y2 = y - i * h
                sss = self.ss2sl()[self.J1[S] % self.ssl()]
                tlist2, j2 = self.tnikInfo(sss)
            elif pt:                      y2 = y - i * h
#            if i == 0 or j == T: ss2sl = self.ss2sl() ; zz2sl = self.zz2sl() ;  self.log(f'Updt j={j} {j2} {JTEXTS[j]} n={n} sss={sss} ss2sl={util.fmtl(ss2sl)} zz2sl={util.fmtl(zz2sl)} J1={util.fmtl(self.J1[:D+1])} J2={util.fmtl(self.J2[:D+1])}', pfx=0)
            yield self.resizeTnik(tlist2, self.J2[j2], j2, x2, y2, w, h, dbg=dbg)
    ####################################################################################################################################################################################################
    def resizeTnik(self, tlist, i, j, x, y, w, h, why='Upd', dbg=0):
        if not tlist:         msg = f'ERROR tlist is Empty i={      i      } j={j} {JTEXTS[j]} {why}'  ;  self.log(msg)  ;  self.quit(msg)
        elif i >= len(tlist): msg = f'ERROR i={i} >= len(tlist)={len(tlist)} j={j} {JTEXTS[j]} {why}'  ;  self.log(msg)  ;  self.quit(msg)
        tnik = tlist[i]
        v = self.isV()
        if   type(tnik) is pygtxt.Label:    fs = v * self.pix2fontsize(h)   ;   tnik.x, tnik.y, tnik.width, tnik.height, tnik.font_size = x, y, w, h, fs
        elif type(tnik) is pygsprt.Sprite:  mx, my = w/tnik.image.width, h/tnik.image.height   ;   tnik.update(x=x, y=y, scale_x=mx, scale_y=my)
        if self.LL and j == L and v:     tnik = self.resizeLL(tnik, i)
#        self.setJdump(j, i, why)
        self.setJ(j, i)         ;   self.dumpTnik(tnik, j, why) if dbg else None
        return tnik
    ####################################################################################################################################################################################################
    def dumpTniksPfx(self, why=''):
        self.dumpGeom('BGN', why)
        self.resetJ(why)
        self.dumpTnik()

    def dumpTniksSfx(self, why=''):
        self.dumpTnik()
        self.dumpJs(why)
        self.dumpGeom('END', why)
    ####################################################################################################################################################################################################
    def dumpTniks(self, why=''):
        np, nl, ns, nc, nt = self.n   ;   ns = self.ssl()   ;   nc += self.zzl()   ;   (nr, nq) = (nl, nc) if self.LL else (0, 0)
        sp, sl, ss, sc = 0, 0, 0, 0   ;   st, sn, si, sk = 0, 0, 0, 0   ;   so, sa, sd = 0, 0, 0   ;   sr, sq = 0, 0   ;   i = 0
        self.dumpTniksPfx(why)
        for p in range(np):
            j = P                         ;  z = sp  ;  self.setJ(j, z)  ;  self.dumpTnik(self.pages[z], j, why)  ;  i += 1  ;  sp += 1
            if self.isV():
                for r in range(nr):
                    j = LR                ;  z = sr  ;  self.setJ(j, z)  ;  self.dumpTnik(self.lrows[z], j, why)  ;  i += 1  ;  sr += 1
                    for q in range(nq):
                        j = LC            ;  z = sq  ;  self.setJ(j, z)  ;  self.dumpTnik(self.lcols[z], j, why)  ;  i += 1  ;  sq += 1
            for l in range(nl):
                j = L                     ;  z = sl  ;  self.setJ(j, z)  ;  self.dumpTnik(self.lines[z], j, why)  ;  i += 1  ;  sl += 1
                for s in (self.ss2sl()):
                    j = S                 ;  z = ss  ;  self.setJ(j, z)  ;  self.dumpTnik(self.sects[z], j, why)  ;  i += 1  ;  ss += 1
                    for c in range(nc):
                        j = C             ;  z = sc  ;  self.setJ(j, z)  ;  self.dumpTnik(self.cols[ z], j, why)  ;  i += 1  ;  sc += 1
                        tlist, j = self.tnikInfo(s)
                        if tlist:
                            for t in range(nt):
                                if   s == TT: z = so if j == O else sd if j == D else st  ;  self.setJ(j, z)  ;  self.dumpTnik(tlist[z], j, why)  ;  i += 1  ;  so += 1 if j == O else 0  ;  sd += 1 if j == D else 0  ;  st += 1 if j == T else 0
                                elif s == NN: z = sa if j == A else sd if j == D else sn  ;  self.setJ(j, z)  ;  self.dumpTnik(tlist[z], j, why)  ;  i += 1  ;  sa += 1 if j == A else 0  ;  sd += 1 if j == D else 0  ;  sn += 1 if j == N else 0
                                elif s == II: z = so if j == O else sd if j == D else si  ;  self.setJ(j, z)  ;  self.dumpTnik(tlist[z], j, why)  ;  i += 1  ;  so += 1 if j == O else 0  ;  sd += 1 if j == D else 0  ;  si += 1 if j == I else 0
                                elif s == KK: z = sa if j == A else sd if j == D else sk  ;  self.setJ(j, z)  ;  self.dumpTnik(tlist[z], j, why)  ;  i += 1  ;  sa += 1 if j == A else 0  ;  sd += 1 if j == D else 0  ;  sk += 1 if j == K else 0
                                else: msg = f'ERROR {i} {util.fmtl(self.n)} {np} {nl} {ns} {nc} {nt}, {p} {l} {s} {c} {t} {self.fmtLE(0)}'   ;   self.log(msg)  ;   self.quit(msg)
        self.dumpTniksSfx(why)
    ####################################################################################################################################################################################################
    def dumpTnik(self, t=None, j=None, why=''):
        if   t is None: self.dumpLabel()   ;   self.dumpSprite() if self.SPRITES else None
        if   type(t) == pygtxt.Label:    self.dumpLabel( t, j, why)
        elif type(t) == pygsprt.Sprite:  self.dumpSprite(t, j, why)

    def dumpSprite(self, t=None, j=None, why=''):
        if t is None: self.log(f'P  L  S   C    T    N    I    K No Nm Cp LR  LC Z  Tid     X       Y       W       H   G why  Name  Cnt V   Identity       Red Grn Blu Opc  Mx    My', pfx=0); return
        J2 = self.fmtJ2()   ;   xywh = self.fmtTxywh(t)   ;   ID = id(t)   ;   g = self.gn[j]   ;   color = self.fmtTcolor(t)   ;   v = self.fmtTvisible(t)   ;   sprt = self.fmtTsprite(t)
        self.log(f'{J2} {xywh} {g} {why:4} {JTEXTS[j]:4} {self.J2[j]:4} {v} {ID:x}     {color} {sprt}', pfx=0)

    def dumpLabel( self, t=None, j=None, why=''):
        if t is None: self.log(f'P  L  S   C    T    N    I    K No Nm Cp LR  LC Z  Tid     X       Y       W       H   G why  Name  Cnt Sz  Identity   Txt Red Grn Blu Opc Dpi B I  Font Name', pfx=0)  ;  return
        J2 = self.fmtJ2()   ;   xywh = self.fmtTxywh(t)   ;   ID = id(t)   ;   g = self.gn[j]   ;   color = self.fmtTcolor(t)   ;   font = self.fmtTfont(t)   ;  fs = self.fmtTfontSize(t)
        self.log(f'{J2} {xywh} {g} {why:4} {JTEXTS[j]:4} {self.J2[j]:4} {fs} {ID:x} {t.text} {color} {font}', pfx=0)
    ####################################################################################################################################################################################################
    def tnikInfo(self, t, i=None, dbg=0):
        tlist, j, k, txt = None, None, None, None  ;  z1, z2 = self.z1(), self.z2()
        if i is None:
            if   t == TT: tlist, j = (self.snos, O) if z1 else (self.capos, D) if z2 else (self.tabs,  T)
            elif t == NN: tlist, j = (self.snas, A) if z1 else (self.capos, D) if z2 else (self.notes, N)
            elif t == II: tlist, j = (self.snos, O) if z1 else (self.capos, D) if z2 else (self.ikeys, I)
            elif t == KK: tlist, j = (self.snas, A) if z1 else (self.capos, D) if z2 else (self.kords, K)
            else:      msg = f't={t} i={i} z1={z1} z2={z2} j={j} txt={txt}'   ;   self.log(msg)   ;   self.quit(msg)
            if dbg: self.log(f't={t} i={i} z1={z1} z2={z2} j={j} txt={txt}')
            return tlist, j
        elif 0 <= i < self.n[T]:
            p, l, s, c = self.J1[P], self.J1[L], self.J1[S], self.J1[C]   ;   nz = self.zzl()   ;   tab = ''
            if dbg: self.log(f't={t} i={i} z1={z1} z2={z2} j={j} txt={txt} plsc {p} {l} {s} {c} zz2sl={self.zz2sl()} J2={self.fmtJ2(0, 1)}')
            if not z1 and not z2: tab = self.data[p][l][c-nz][i]
            kT, kN, kI, kK = self.k[T], self.k[N], self.k[I], self.k[K]   ;   kO, kA, kD, kH = self.k[O], self.k[A], self.k[D], self.k[H]
            if   t == TT: tlist, j, k, txt = (self.snos, O, kO, self.sobj.stringNumbs[i]) if z1 else (self.capos, D, kD, self.sobj.stringCapo[i]) if z2 else (self.tabs,  T, kT, tab)
            elif t == NN: tlist, j, k, txt = (self.snas, A, kA, self.sobj.stringNames[i]) if z1 else (self.capos, D, kD, self.sobj.stringCapo[i]) if z2 else (self.notes, N, kN, tab)
            elif t == II: tlist, j, k, txt = (self.snos, O, kO, self.sobj.stringNumbs[i]) if z1 else (self.capos, D, kD, self.sobj.stringCapo[i]) if z2 else (self.ikeys, I, kI, tab)
            elif t == KK: tlist, j, k, txt = (self.snas, A, kA, self.sobj.stringNames[i]) if z1 else (self.capos, D, kD, self.sobj.stringCapo[i]) if z2 else (self.kords, K, kK, tab)
            else:      msg = f't={t} i={i} z1={z1} z2={z2} j={j} txt={txt} plsc {p} {l} {s} {c} nz={nz}'   ;   self.log(msg)    ;   self.quit(msg)
            return tlist, j, k, txt
        msg = f'ERROR tlist skipped t={t} i={i} z1={z1} z2={z2} j={j} k={k} txt={txt}'   ;   self.log(msg)   ;   self.quit(msg)
    ####################################################################################################################################################################################################
    def geom(self, j=0, p=None, n=None, i=None, dbg=0):
        n = n if n is not None else self.n[j]
        i = i if i is not None else self.i[j]
        if   j == C:            n +=  self.zzl()
        if   p is None:         w  =  self.width             ;  h  =  self.height
        elif j == C:            w  =  p.width/n              ;  h  =  p.height
        else:                   w  =  p.width                ;  h  =  p.height/n
        if self.SPRITES:
            if   p is None:     x  =  0                      ;  y  =  self.height
            elif j == T:        x  =  p.x + w/2              ;  y  =  p.y - h/2
            else:               x  =  p.x                    ;  y  =  p.y
        else:
            if   p is None:     x  =  w/2                    ;  y  =  h/2
            elif j == T:        x  =  p.x                    ;  y  =  p.y + p.height/2 - h/2
            else:               x  =  w/2                    ;  y  =  p.y + p.height/2 - h/2
        if dbg and j <= C: msg = f'{JTEXTS[j]:4} j={j} n={n:2} i={i:2} {x:7.2f} {y:7.2f} {w:7.2f} {h:7.2f}'  ;  msg += f'{p.x:7.2f} {p.y:7.2f} {p.width:7.2f} {p.height:7.2f}' if p else ''  ;  self.log(msg, pfx=0)
        return n, i, x, y, w, h
    ####################################################################################################################################################################################################
    def createCursor(self, dbg=1):
        x, y, w, h, c = self.cc2xywh()
        self.cursor = self.createTnik(self.cursr, 0, H, x, y, w, h, kk=1, kl=self.k[H], v=1, dbg=1)
        if dbg: self.dumpCursr('NEW', x, y, w, h, c)
        if self.LL:  self.setLLStyle(self.cc, CURRENT_STYLE)

    def resizeCursor(self, dbg=1):
        x, y, w, h, c = self.cc2xywh()
        self.resizeTnik(self.cursr, 0, H, x, y, w, h, dbg=1)
        if dbg: self.dumpCursr('UPD', x, y, w, h, c)

    def moveCursor(self, ss=0, dbg=0):
        self.setLLStyle(self.cc, SELECT_STYLE if ss else NORMAL_STYLE)
        self.resizeCursor(dbg=dbg)
        self.setLLStyle(self.cc, CURRENT_STYLE)
    ####################################################################################################################################################################################################
    def dumpCursr(self, why, x, y, w, h, c): self.dumpCxywh(x, y, w, h, c)  ;  self.dumpGeom(why, JTEXTS[H])
    def dumpCxywh(self, x, y, w, h, c): self.log(f'x={x:6.2f} y={y:6.2f} w={w:6.2f} h={h:6.2f} cc={c}')
    def cc2xywh(self, dbg=1): cc = self.cursorCol()  ;  c = self.tabs[cc]  ;  w, h = c.width, c.height  ;  x, y = c.x-w/2, c.y-h/2  ;  self.dumpCxywh(x, y, w, h, cc) if dbg else None  ;  return x, y, w, h, cc

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
    def data2plrc(self, data=None, dbg=1): dl = self.dl(data)  ;  plrc = dl if self.isVert() else dl[0], dl[1], dl[3], dl[2]  ;  self.log(f'dl={util.fmtl(dl)} plrc={util.fmtl(plrc)}') if dbg else None  ;  return plrc

    def cn2txt(self, cn):  #  usefull? re-name cn2tabtxt()
        cc = self.cn2cc(cn)
        p, l, c, t = self.cc2plct(cc)
        txt = self.data[p][l][c]
        self.log(f'cn={cn} cc={cc} plc={p} {l} {c} txt={txt}')
    ####################################################################################################################################################################################################
    def setCaption(self, msg, dbg=1):
        if dbg: self.log(f'{msg}')
        self.set_caption(msg)

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
        b, k, dpi, i, n, s = self.fontParams()   ;   pix = s / FONT_SCALE
        self.log(f'{dpi}:{FONT_DPIS[dpi]}dpi {s:5.2f}pt {n}:{FONT_NAMES[n]} {k}:{FONT_COLORS[k]} {s:5.2f}pt = {FONT_SCALE:5.3f}(pt/pix) * {pix:5.2f}pixels {why}')

    def setFontParam(self, n, v, m, dbg=1):
        setattr(self, m, v)
        if dbg: self.log(f'n={n} m={m} v={v:.1f}')
        for i in range(len(self.E)):
            self._setFontParam(self.E[i], n, v, m)
        self.setCaption(self.fmtf1())

    @staticmethod
    def pix2fontsize(pix): return (pix * FONT_SCALE) % FS_MAX

    @staticmethod
    def _setFontParam(p, n, v, m, dbg=0):
        for i in range(len(p)):
            k = len(p[i].color)
            if m == 'fontSize': v = v % FS_MAX
            if dbg: util.slog(f'n={n} v={v} m={m} {util.fmtl(FONT_COLORS[v])} lk={len(p[i].color)} type(p[{i}])={type(p[i])} type(k)={type(p[i].color)}')
            setattr(p[i], n, FONT_NAMES[v] if m == 'fontNameIndex' else FONT_COLORS[v][:k] if m == 'fontColorIndex' else FONT_DPIS[v] if m == 'fontDpiIndex' else v)
    ####################################################################################################################################################################################################
    def on_mouse_release(self, x, y, button, modifiers, dbg=1):
        np, nl, ns, nc, nt = self.n   ;   nz = self.zzl()    ;  nc += nz   ;   file = None
        y0 = y   ;   y = self.height - y   ;   n = nl * ns * nt + ns * self.LL   ;  m = int(ns*nt) + self.LL
        w = self.width/nc       ;  h = self.height/n         ;   d = int(y/h) - self.LL
        l = int(d/m)         ;  c  = int(x/w) - nz   ;   t = d - (l * m)  ;  p = 0
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
#        elif kbk == 'E' and self.isCtrl(     mods):    self.eraseTabs(       '@   E')
        elif kbk == 'F' and self.isCtrlShift(mods):    self.toggleFullScreen('@ ^ F')
        elif kbk == 'F' and self.isCtrl(     mods):    self.toggleFlatSharp( '@   F')
        elif kbk == 'G' and self.isCtrlShift(mods):    self.move2LastTab(    '@ ^ G', page=1)
        elif kbk == 'G' and self.isCtrl(     mods):    self.move2LastTab(    '@   G', page=0)
        elif kbk == 'H' and self.isCtrlShift(mods):    self.move2FirstTab(   '@ ^ H', page=1)
        elif kbk == 'H' and self.isCtrl(     mods):    self.move2FirstTab(   '@   H', page=0)
        elif kbk == 'I' and self.isCtrlShift(mods):    self.insertSpace(     '@ ^ I')
        elif kbk == 'I' and self.isCtrl(     mods):    self.toggleTTs(      '@   I', II)
        elif kbk == 'J' and self.isCtrlShift(mods):    self.jump(            '@ ^ J', a=1)
        elif kbk == 'J' and self.isCtrl(     mods):    self.jump(            '@   J', a=0)
        elif kbk == 'K' and self.isCtrlShift(mods):    self.toggleTTs(      '@ ^ K', KK)
        elif kbk == 'K' and self.isCtrl(     mods):    self.toggleTTs(      '@   K', KK)
        elif kbk == 'L' and self.isCtrlShift(mods):    self.toggleLLs(     '@ ^ L')
        elif kbk == 'L' and self.isCtrl(     mods):    self.toggleLLs(     '@   L')
        elif kbk == 'M' and self.isCtrlShift(mods):    self.toggleZZs(     '@ ^ M', 1)
        elif kbk == 'M' and self.isCtrl(     mods):    self.toggleZZs(     '@   M', 0)
        elif kbk == 'N' and self.isCtrlShift(mods):    self.toggleTTs(      '@ ^ N', NN)
        elif kbk == 'N' and self.isCtrl(     mods):    self.toggleTTs(      '@   N', NN)
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
        elif kbk == 'T' and self.isCtrlShift(mods):    self.toggleTTs(      '@ ^ T', TT)
        elif kbk == 'T' and self.isCtrl(     mods):    self.toggleTTs(      '@   T', TT)
        elif kbk == 'U' and self.isCtrlShift(mods):    self.reset(       '@ ^ U')
        elif kbk == 'U' and self.isCtrl(     mods):    self.reset(       '@   U')
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
        elif kbk == 'S' and self.isAltShift(mods):     self.setFontParam('font_size', (self.fontSize      + 1)  % FS_MAX,           'fontSize')
        elif kbk == 'S' and self.isAlt(     mods):     self.setFontParam('font_size', (self.fontSize      - 1)  % FS_MAX,           'fontSize')
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
        p, l, s, c, t = self.j()
        if dbg: self.log(f'BGN {how} i={util.fmtl(self.i)}', pos=1)
        self.moveTo(how, p-1, l, c, t)
        self.on_resize(self.width, self.height, dbg=1)
        if dbg: self.log(f'END {how} i={util.fmtl(self.i)}', pos=1)

    def nextPage(self, how, dbg=1):
        p, l, s, c, t = self.j()
        if dbg: self.log(f'BGN {how} i={util.fmtl(self.i)}', pos=1)
        self.moveTo(how, p+1, l, c, t)
        self.on_resize(self.width, self.height, dbg=1)
        if dbg: self.log(f'END {how} i={util.fmtl(self.i)}', pos=1)
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

#        if not self.SNAP0: t = self.tabs[self.cc]  ;  self.snapshot(f'pre-move() k={k:4} kk={self.cc:3} {util.fmtl(self.i, FMTN)} text={t.text} {t.x:6.2f} {t.y:6.2f}')  ;  self.SNAP0 = 1
#        self.armSnap = f'move() k={k:4} kk={kk:4} {util.fmtl(self.i, FMTN)} text={self.tabs[self.cc].text} {x:6.2f} {y:6.2f}'
    ####################################################################################################################################################################################################
    def jump(self, how, txt='0', a=0):
        cc = self.cursorCol()   ;   self.jumpAbs = a
        self.log(f'{how} txt={txt} a={a} cc={cc} jt={self.jumpAbs} {util.fmtl(self.i)}')
        if not self.jumping:                  self.jumping = 1
        elif txt.isdecimal():                 self.jumpStr += txt
        elif txt == '-' and not self.jumpStr: self.jumpStr += txt
        elif txt == ' ':
            self.log(f'{how} txt={txt} a={a} cc={cc} jt={self.jumpAbs} jumpStr={self.jumpStr} {util.fmtl(self.i)}')
            jcc = self.n[T] * int(self.jumpStr)
            self.jumping = 0   ;    self.jumpStr = ''
            self.move(how, jcc - 1 - a * cc)
            self.log(f'{how} txt={txt} a={a} cc={cc} jt={self.jumpAbs} jcc={jcc} moved={jcc - 1 - a * cc} {util.fmtl(self.i)}')
    ####################################################################################################################################################################################################
    def setTab(self, how, text, rev=0, dbg=1):
        if rev: self.reverseArrow()   ;    self.autoMove(how)
        p, l, c, t = self.j2()   ;   data = self.data[p][l][c][t]   ;   cc = self.plct2cc(p, l, c, t)  # ;   isDataFret = util.isFret(data)   ;   isTextFret = util.isFret(text)
        self.log(f'BGN {how} text={text} data={data} rev={rev}', pos=1)
        self.setDTNIK(text, cc, p, l, c, t, kk=1) # if isDataFret or isTextFret else 0)
        p, l, c, t = self.j2()   ;   data = self.data[p][l][c][t]
        self.log(f'END {how} text={text} data={data} rev={rev}', pos=1)
        if rev: self.reverseArrow()
        else:   self.autoMove(how)
        if SNAP and dbg: self.snapshot()
        self.dataHasChanged = 1

    def setDTNIK(self, text, cc, p, l, c, t, kk=0, pos=0, dbg=1):
        if dbg: self.log(f'BGN kk={kk}    text={text}', pos=pos)
        self.setData(text, p, l, c, t)
        imap = self.getImap(p, l, c)
        if TT in self.SS: self.setTab2( text, cc)
        if NN in self.SS: self.setNote( text, cc, t)
        if II in self.SS: self.setIkey( imap, p, l, c)
        if KK in self.SS: self.setChord(imap, p, l, c)
        if dbg: self.log(f'END kk={kk}    text={text} len(imap)={len(imap)}', pos=pos)
    ####################################################################################################################################################################################################
    def setData(self, text, p, l, c, t, pos=0, dbg=1):
        data = self.data[p][l][c]
        if dbg: self.log(f'BGN t={t} text={text} data={data}', pos=pos)
        self.data[p][l][c] = data[0:t] + text + data[t+1:]
        data = self.data[p][l][c]
        if dbg: self.log(f'END t={t} text={text} data={data}', pos=pos)

    def setTab2(self, text, cc, pos=0, dbg=1):
        if dbg: self.log(f'BGN         text={text} tabs[{cc}]={self.tabs[cc].text}', pos=pos)
        self.tabs[cc].text = text
        if dbg: self.log(f'END         text={text} tabs[{cc}]={self.tabs[cc].text}', pos=pos)

    def setNote(self, text, cc, t, pos=0, dbg=1):
        if dbg: self.log(f'BGN     t={t} text={text} notes[{cc}]={self.notes[cc].text}', pos=pos)
        self.notes[cc].text = self.sobj.tab2nn(text, t) if self.sobj.isFret(text) else self.tblank
        if dbg: self.log(f'END     t={t} text={text} notes[{cc}]={self.notes[cc].text}', pos=pos)
    ####################################################################################################################################################################################################
    def getImap(self, p, l, c, dbg=0, dbg2=0):
        cn = self.plc2cn(p, l, c)      ;    key = cn   ;   dl = self.dl()   ;   mli = self.cobj.mlimap
        msg1  = f'plc=[{p} {l} {c}]'   ;   msg2 = f'dl={util.fmtl(dl)} cn={cn} key={key} keys={util.fmtl(list(mli.keys()))}'
        if p >= dl[0] or l >= dl[1] or c >= dl[2]:  msg = f'ERROR Indexing {msg1} >= {msg2}'   ;   self.log(msg)   ;   self.quit(msg)
        if dbg:           self.log(f'{msg1} {msg2}')
        imap  = self.cobj.getChordName(self.data, cn, p, l, c)
        if dbg2 and imap: self.cobj.dumpImap(imap)
        return imap
    ####################################################################################################################################################################################################
    def setIkey(self, imap, p, l, c, pos=0, dbg=0):
        cc = self.plct2cc(p, l, c, 0)
        ikeys = imap[0] if imap else []
        if dbg: self.log(f'BGN ikeys={util.fmtl(ikeys)} len(imap)={len(imap)}', pos=pos)
        self.setIkeyText(ikeys, cc, p, l, c)
        if dbg: self.log(f'END ikeys={util.fmtl(ikeys)} len(imap)={len(imap)}', pos=pos)

    def setIkeyText(self, text, cc, p, l, c, pos=0, dbg=0):
        nt = self.n[T]   ;  cc = self.normalizeCC(cc)   ;   data = self.data[p][l][c]   ;   j = 0   ;   text = text[::-1]
        txt = self.objs2Text(self.ikeys, cc, nt, I)
        if dbg: self.log(f'BGN [{cc:2}-{cc+nt-1:2}] text={util.fmtl(text)} data={data} ikeys=<{txt}>{len(txt)}', pos=pos)
        for i in range(nt):
            if text and len(text) > j: self.ikeys[cc + i].text = text[j] if self.sobj.isFret(data[i]) else self.tblank     ;   j += 1 if self.sobj.isFret(data[i]) else 0
            else:                      self.ikeys[cc + i].text = self.tblank
        txt = self.objs2Text(self.ikeys, cc, nt, I)
        if dbg: self.log(f'END [{cc:2}-{cc+nt-1:2}] text={util.fmtl(text)} data={data} ikeys=<{txt}>{len(txt)}', pos=pos)
        if dbg: self.dumpDataSlice(p, l, c, cc)

    def setChord(self, imap, p, l, c, pos=0, dbg=0):
        cc = self.plct2cc(p, l, c, 0)
        name = imap[3] if imap and len(imap) > 3 else ''  ;   chunks = imap[4] if imap and len(imap) > 4 else []
        if dbg: self.log(f'BGN name={name} chunks={util.fmtl(chunks)} len(imap)={len(imap)}', pos=pos)
        self.setChordName(cc, name, chunks) if name and chunks else self.log(f'WARN Not A Chord cc={cc} name={name} chunks={chunks}', pos=pos)
        if dbg: self.log(f'END name={name} chunks={util.fmtl(chunks)} len(imap)={len(imap)}', pos=pos)

    def setChordName(self, cc, name, chunks, pos=0, dbg=0):
        nt = self.n[T]   ;   cc = self.normalizeCC(cc)   ;   kords = self.kords
        txt = self.objs2Text(kords, cc, nt, K)
        if dbg: self.log(f'BGN [{cc:2}-{cc+nt-1:2}] name={name} chunks={util.fmtl(chunks)} chords=<{txt}>{len(txt)}', pos=pos)
        for i in range(nt):
            if chunks and len(chunks) > i: self.kords[cc + i].text = chunks[i]
            else:                          self.kords[cc + i].text = self.tblank
        txt = self.objs2Text(kords, cc, nt, K)
        if dbg: self.log(f'END [{cc:2}-{cc+nt-1:2}] name={name} chunks={util.fmtl(chunks)} chords=<{txt}>{len(txt)}', pos=pos)
    @staticmethod
    def objs2Text(obs, cc, nt, j, dbg=0):
        texts = [ obs[cc + t].text for t in range(nt) ]   ;   text = ''.join(texts)
        if dbg: util.slog(f'{jTEXTS[j]}[{cc}-{cc+nt-1}].text={util.fmtl(texts)}=<{text}>')
        return text
    ####################################################################################################################################################################################################
    def setLLStyle(self, cc, style, dbg=1):
        p, l, c, t = self.cc2plct(cc)  ;  nc = self.n[C]
        bold, italic, color = 0, 0, self.k[H][0]   ;   i = c + l * nc if self.lcols else 0
        if   style == NORMAL_STYLE:  color = self.k[H][0]  ;  bold = 0  ;  italic = 0
        elif style == CURRENT_STYLE: color = self.k[H][1]  ;  bold = 0  ;  italic = 0
        elif style == SELECT_STYLE:  color = self.k[H][2]  ;  bold = 1  ;  italic = 1
        elif style == COPY_STYLE:    color = self.k[H][3]  ;  bold = 1  ;  italic = 1
        if self.lcols:
            self.lcols[i].color  = color
            self.lcols[i].bold   = bold
            self.lcols[i].italic = italic
        if dbg: self.log(f'{self.fPos()}     i={i} = c={c} + l={l} * nc={nc} style={style} bold={bold} italic={italic} color={color}')

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
        if cn in self.smap: self.log(f'RETURN: cn={cn} already in smap={util.fmtm(self.smap)}') if dbg2 else None   ;   return
        if dbg: self.dumpSmap(f'BGN {how} m={m} cn={cn} cc={cc} k={k}')
        for t in range(nt):
            if self.tabs:  self.tabs [k + t].color = self.k[H][2]
            if self.notes: self.notes[k + t].color = self.k[H][2]
            if self.ikeys: self.ikeys[k + t].color = self.k[H][2]
            if self.kords: self.kords[k + t].color = self.k[H][2]
            if self.tabs:  text += self.tabs  [k + t].text
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
            if self.tabs:  self.tabs [k + t].color = self.k[T][0]
            if self.notes: self.notes[k + t].color = self.k[N][0]
            if self.ikeys: self.ikeys[k + t].color = self.k[I][0]
            if self.kords: self.kords[k + t].color = self.k[K][0]
        if cn in self.smap: self.smap.pop(cn)
        elif dbg:           self.log(f'cn={cn} not found in smap={util.fmtm(self.smap)}')
        if m:   self.move(how, m)
        if dbg: self.dumpSmap(f'END {how} m={m} cn={cn} cc={cc} k={k}')
    ####################################################################################################################################################################################################
    def copyTabs(self, how, dbg=1):
        self.dumpSmap(f'BGN {how}')   ;   nt = self.n[T]  ;   text = ''
        for k in list(self.smap.keys()):
            k *= nt
            self.setLLStyle(k, NORMAL_STYLE)
            for t in range(nt):
                if self.tabs:  self.tabs [k + t].color = self.k[T][0]
                if self.notes: self.notes[k + t].color = self.k[N][0]
                if self.ikeys: self.ikeys[k + t].color = self.k[I][0]
                if self.kords: self.kords[k + t].color = self.k[K][0]
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
                if self.tabs:  self.tabs [k + t].color = self.k[T][0]
                if self.notes: self.notes[k + t].color = self.k[N][0]
                if self.ikeys: self.ikeys[k + t].color = self.k[I][0]
                if self.kords: self.kords[k + t].color = self.k[K][0]
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
        self.dumpSmap(f'BGN {how} shiftingTabs={self.shiftingTabs} nf={nf}')
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
                self.log(f'cc={cc} cn={cn} v={v} text={self.smap[cn]}')
                for t in range(nt):
                    text = self.smap[cn][t]    ;    kt = cc + t    ;    fn = 0   ;   ntones = util.NTONES * 2
                    if self.sobj.isFret(text):
                        fn = self.afn(str((self.tab2fn(text) + self.shiftSign * self.tab2fn(nf)) % ntones))  ;  self.log(f'cc={cc} cn={cn} t={t} text={text} nf={nf} fn={fn} ss={self.shiftSign}')
                    if fn and self.sobj.isFret(fn):  self.setDTNIK(fn, kt, p, l, c, t, kk=1 if t==nt-1 else 0)
            self.shiftSign = 1
            self.dataHasChanged = 1
            self.unselectAll('shiftTabs()')
        self.dumpSmap(f'END {how} shiftingTabs={self.shiftingTabs} nf={nf} ss={self.shiftSign}')

    def syncBlanks(self, data=None):
        self.tblankCol = self.tblank * self.tpc   ;   data = data or self.data    ;   dl = self.dl(data)
        for p in range(dl[0]):
            for l in range(dl[1]):
                for c in range(dl[2]):
                    for b in self.tblanks:
                        if b != self.tblank: data[p][l][c] = data[p][l][c].replace(b, self.tblank)
        self.log(f'tblank={self.tblank} blankCol={self.tblankCol}')

    def swapTab(self, how, txt='', data=None, dbg=0, dbg2=0):  # e.g. c => 12 not same # chars asserts
        src, trg = self.swapSrc, self.swapTrg
        data = data or self.data
        if not self.swapping: self.swapping = 1
        elif txt.isalnum():
            if   self.swapping == 1:   self.swapSrc += txt  # ;   self.log(f'    {how} txt={txt} swapping={self.swapping} swapSrc={self.swapSrc} swapTrg={self.swapTrg}')
            elif self.swapping == 2:   self.swapTrg += txt  # ;   self.log(f'    {how} txt={txt} swapping={self.swapping} swapSrc={self.swapSrc} swapTrg={self.swapTrg}')
        elif txt == '\r':
            self.log(f'    {how} swapping={self.swapping} swapSrc={self.swapSrc} swapTrg={self.swapTrg}')
            if   self.swapping == 1 and not self.swapTrg: self.swapping = 2   ;   self.log(f'{how} waiting swapSrc={self.swapSrc} swapTrg={self.swapTrg}') if dbg else None   ;   return
            elif self.swapping == 2 and     self.swapTrg: self.swapping = 0   ;   self.log(f'{how} BGN     swapSrc={self.swapSrc} swapTrg={self.swapTrg}') if dbg else None
            np, nl, ns, nc, nr = self.n  ;  nc += self.zzl()
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
        tt1 =  util.Note.TYPE    ;    tt2 = (util.Note.TYPE + 1) % 2    ;    util.Note.setType(tt2)    ;   i1 = -1
        self.log(f'BGN {how} type={tt1}={util.Note.TYPES[tt1]} => type={tt2}={util.Note.TYPES[tt2]}')
        for i, n in enumerate(self.notes):
            if len(n.text) > 1:
                p, l, c, t = self.cc2plct(i)   ;   old = n.text    ;    i2 = self.plc2cn(p, l, c)
                if   n.text in util.Note.F2S: n.text = util.Note.F2S[n.text]
                elif n.text in util.Note.S2F: n.text = util.Note.S2F[n.text]
                if dbg: self.log(f'notes[{i:3}] {old} => {n.text} i1={i1} i2={i2}')
                if i1 != i2:   imap = self.getImap(p, l, c)   ;   self.setChord(imap, p, l, c, t)    ;    i1 = i2
        self.log(f'END {how} type={tt1}={util.Note.TYPES[tt1]} => type={tt2}={util.Note.TYPES[tt2]}')
    ####################################################################################################################################################################################################
    def toggleChordNames(self, how, hit=0, dbg=1):
        cc = self.cc    ;    cn = self.cc2cn(cc)
        mks = list(self.cobj.mlimap.keys())   ;   sks = list(self.smap.keys())
        if sks and not hit:
            if dbg: self.dumpSmap(f'BGN {how} mks={util.fmtl(mks)} cn={cn:2} hit={hit} sks={util.fmtl(sks)}')
            [ self.toggleChordName(how, k) for k in sks ]
        else:
            if dbg: self.dumpSmap(f'BGN {how} mks={util.fmtl(mks)} cn={cn:2} hit={hit} sks={util.fmtl(sks)}')
            if hit: self.toggleChordNameHits(how, cn)
            else:   self.toggleChordName(    how, cn)
        if dbg:     self.dumpSmap(f'END {how} mks={util.fmtl(mks)} cn={cn:2} hit={hit} sks={util.fmtl(sks)}')

    def toggleChordNameHits(self, how, cn, dbg=1):
        mli = self.cobj.mlimap   ;   mks = list(mli.keys())
        if cn not in mli: self.log(f'RETURN: no mli key for cn={cn}') if dbg else None   ;   return
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
        if cn not in mli:                     msg += f'RETURN: cn={cn} Not Found milap.keys={util.fmtl(list(mli.keys()))}'
        if msg: self.log(msg)   ;   return
        limap = mli[cn][0]      ;   imi = mli[cn][1]
        imi = (imi + 1) % len(limap)
        mli[cn][1] = imi
        ikeys, ivals, notes, chordName, chunks, rank = limap[imi]
        if self.ikeys and ikeys:                self.setIkeyText(ikeys, cc, p, l, c)
        if self.kords and chordName and chunks: self.setChordName(cc, chordName, chunks)
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
        self.FULL_SCREEN =  not  self.FULL_SCREEN
        self.set_fullscreen(self.FULL_SCREEN)
        self.log(f'{how} FULL_SCREEN={self.FULL_SCREEN}')

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
        np, nl, ns, nc, nt = self.n   ;   nz = self.zzl()  ;  nc += nz
        self.log(f'BGN {how} np={np} nl={nl} ns={ns} nc={nc} nt={nt}')
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
        self.log(f'END {how} np={np} nl={nl} ns={ns} nc={nc} nt={nt}')
        self.dataHasChanged = 1

    def reset(self, how):
        self.dumpGeom('BGN', f'{how} before cleanup()')
        self.cleanup()
        self.dumpGeom('   ', f'{how} after cleanup() / before reinit()')
        self._reinit()
        self.dumpGeom('END', f'{how} after reinit()')
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
    def isBTab(self, text):   return 1 if text in self.tblanks else 0
#    def isNBTab(text):        return 1 if                        self.sobj.isFret(text) or text in util.DSymb.SYMBS else 0
    def isTab(self, text):    return 1 if text == self.tblank or self.sobj.isFret(text) or text in util.DSymb.SYMBS else 0
    def isParsing(self):      return 1 if self.inserting or self.jumping or self.shiftingTabs or self.swapping else 0
    @staticmethod
    def afn(fn): return fn if len(fn) == 1 and '0' <= fn <= '9' else chr(ord(fn[1]) - ord('0') + ord('a')) if len(fn) == 2 and fn[0] == '1' else None
    ####################################################################################################################################################################################################
    def cci(self, k, kl, dbg=0):
        if k == 0: self.ki = (self.ki + 1) % len(kl)
        kk = (k + self.ki) % len(kl)
        if dbg: self.log(f'k={k} kl={util.fmtl(kl)} ki={self.ki} kk={kk}')
        return kk
    @staticmethod
    def ordSfx(n):
        m = n % 10
        if   m == 1 and n != 11: return 'st'
        elif m == 2 and n != 12: return 'nd'
        elif m == 3 and n != 13: return 'rd'
        else:                    return 'th'
    ####################################################################################################################################################################################################
    def snapshot(self, why='', dbg=0, dbg2=0):
        if dbg: self.log(f'SNAP_DIR={SNAP_DIR} SNAP_SFX={SNAP_SFX} baseName={BASE_NAME} basePath={BASE_PATH}')
        SNAP_ID   = f'.{self.ssi}'
        SNAP_NAME = BASE_NAME + SNAP_ID + SNAP_SFX
        SNAP_PATH = BASE_PATH / SNAP_DIR / SNAP_NAME
        pyglet.image.get_buffer_manager().get_color_buffer().save(f'{SNAP_PATH}')
        if dbg: self.log(f'SNAP_ID={SNAP_ID} SNAP_NAME={SNAP_NAME,} SNAP_PATH={SNAP_PATH}')
        if dbg2: self.log(f'{SNAP_NAME} {why}', file=sys.stdout)
        self.ssi += 1
    @staticmethod
    def deleteGlob(g, why=''):
        util.slog(f'deleting {len(g)} file globs why={why}', file=LOG_FILE)
        for f in g:
            util.slog(f'{f}', file=LOG_FILE)
            os.system(f'del {f}')
    @staticmethod
    def getFilePath(seq=0, filedir='files', filesfx='.txt'):
        if seq:
            subDir     = '/'
            filedir    = filedir + subDir
            util.slog(f'subdir       = {subDir}', file=LOG_FILE)
            util.slog(f'filedir      = {filedir}', file=LOG_FILE)
            util.slog(f'filesfx      = {filesfx}', file=LOG_FILE)
            pathlib.Path(filedir).mkdir(parents=True, exist_ok=True)
            fileGlobArg = str(BASE_PATH / filedir / BASE_NAME) + '.*' + filesfx
            fileGlob    = glob.glob(fileGlobArg)
            util.slog(f'fileGlobArg  = {fileGlobArg}', file=LOG_FILE)
            util.slog('fileGlob:', file=LOG_FILE)
            seq        = 1 + Tabs.getFileSeqNum(fileGlob, filesfx)
            filesfx    = f'.{seq}{filesfx}'
            util.slog(f'{util.fmtl(fileGlob)}', pfx=0, file=LOG_FILE)
            util.slog(f'seq num      = {seq} filesfx={filesfx}', file=LOG_FILE)
        return util.getFilePath(BASE_NAME, BASE_PATH, filedir=filedir, filesfx=filesfx)
    @staticmethod
    def getFileSeqNum(fgs, sfx, dbg=1):
        i = -1
        if len(fgs):
            if dbg: util.slog(f'sfx={sfx} fgs={util.fmtl(fgs)}', file=LOG_FILE)
            ids = []
            for s in fgs:
                if s.endswith(sfx):
                    s = s[:-len(sfx)]
                    j = s.rfind('.')
                    s = s[j+1:]
                    i = int(s)
                    ids.append(i)
            if dbg: util.slog(f'ids={ids}', file=LOG_FILE)
            i = max(ids)
        return i
    ####################################################################################################################################################################################################
    def log(self, msg='', pfx=1, pos=0, file=None, flush=False, sep=',', end='\n'):
        if file is None: file = LOG_FILE
        if pos: msg = f'{self.fPos()}' + f' {msg}' # if msg else
        util.slog(msg, pfx, file, flush, sep, end)
    ####################################################################################################################################################################################################
    def quit(self, why='', code=0, dbg=1, dbg2=1):
        self.log(f'BGN {why} code={code}')        ;   self.log(QUIT_BGN, pfx=0)
        if dbg: util.dumpStack(inspect.stack(), file=LOG_FILE)   ;   self.log(QUIT, pfx=0)   ;   util.dumpStack(util.MAX_STACK_FRAME, file=LOG_FILE)
        self.dumpArgs()
        if dbg: self.dumpStruct('quit')
#        if SNAP and code != 2: self.snapshot()
#        self.cobj.dumpInstanceCat(why)
#        self.cleanupCat(1 if code != 2 else 0)
        if       code and AUTO_SAVE: self.saveDataFile(why, f=0)
        elif not code:               self.saveDataFile(why, f=1)
        if dbg2: self.transposeDataDump()
        if dbg:  self.cobj.dumpMlimap(why)
        self.log(f'END {why} code={code}')        ;   self.log(QUIT_END, pfx=0)
        self.cleanupLog()
        pyglet.app.exit()
    ####################################################################################################################################################################################################
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

########################################################################################################################################################################################################
OPACITY          = [ 255, 240, 225, 210, 190, 165, 140, 110, 80 ]
GRAY             = [(255, 255, 255, OPACITY[0]), (  0,   0,   0, OPACITY[0])]
PINK             = [(255,  64, 192, OPACITY[0]), ( 57,  16,  16, OPACITY[0])]
INFRA_RED        = [(200, 100,  24, OPACITY[0]), ( 68,  20,  19, OPACITY[0])]
RED              = [(255,  12,  11, OPACITY[0]), ( 88,  15,  12, OPACITY[0])]
ORANGE           = [(255, 128,   0, OPACITY[0]), ( 76,  30,  25, OPACITY[0])]
YELLOW           = [(255, 255,  10, OPACITY[0]), (255, 255,  10, OPACITY[8])]
#YELLOW           = [(255, 255,  10, OPACITY[0]), ( 45,  41,  10, OPACITY[0])]
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
########################################################################################################################################################################################################
def genColors(k, nsteps=HUES, dbg=0):
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
FONT_SCALE    = 0.8 # 8pts/10pix pts/pux
FONT_DPIS     = [72, 78, 84, 90, 96, 102, 108, 114, 120]
FONT_NAMES    = ['Lucida Console', 'Helvetica', 'Arial', 'Times New Roman', 'Courier New', 'Century Gothic', 'Bookman Old Style', 'Antique Olive']
FONT_COLORS_S = [PINKS[0], CYANS[0], REDS[0], BLUES[0], YELLOWS[0], GREENS[0], ORANGES[0], VIOLETS[0], REDS[13], YELLOWS[15], GREEN_BLUES[8], ORANGES[12], INDIGOS[8], ULTRA_VIOLETS[9], BLUE_GREENS[8], GRAYS[8]]
FONT_COLORS_L = [PINKS[0], GRAYS[0], BLUES[0], GREENS[0], YELLOWS[0], REDS[0], GRAYS[1], PINKS[8], REDS[10], YELLOWS[15], GRAYS[8], GRAYS[8], INDIGOS[8], GRAYS[9], GRAYS[8], GRAYS[8]]
FONT_COLORS   =  FONT_COLORS_S # if self.SPRITES else FONT_COLORS_L
########################################################################################################################################################################################################

if __name__ == '__main__':
    backPath = util.getFilePath(BASE_NAME, BASE_PATH, filedir='logs', filesfx='.blog')
    LOG_PATH = util.getFilePath(BASE_NAME, BASE_PATH, filedir='logs', filesfx='.log')
    if backPath:               os.system(f'copy {LOG_PATH} {backPath}')
    with open(str(LOG_PATH), 'w') as LOG_FILE:
        util.slog(f'LOG_PATH={LOG_PATH} LOG_FILE={LOG_FILE}', file=LOG_FILE)
        Tabs()
        ret     = pyglet.app.run()
