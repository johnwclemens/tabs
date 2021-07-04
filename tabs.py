import inspect, math, sys, os, glob, pathlib, string, collections, itertools #, shutil#, unicodedata, readline, csv
import pyglet
import pyglet.window.key   as pygwink
import pyglet.window.event as pygwine
sys.path.insert(0, os.path.abspath('../lib'))
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
CHECKER_BOARD = 0  ;  EVENT_LOG = 1  ;  FULL_SCREEN = 0  ;  ORDER_GROUP = 1  ;  READ_DATA_FILE = 1  ;  RESIZE = 1  ;  SEQ_LOG_FILES = 1  ;  SUBPIX = 1
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
O, A, D, B       =  8,  9, 10, 11
TT, NN, II, KK   =  0,  1,  2,  3
Z, COL_L, LINE_L       = ' ', 'Col', 'Line '
SNO_C, SNA_C, CFN_C    = 0, 0, 1
INIT             = '###   Init   ###' * 13
QUIT             = '###   Quit   ###' * 13
OPACITY          = [255, 240, 225, 210, 190, 165, 140, 110, 80]
GRAY             = [(255, 255, 255, OPACITY[0]), ( 0,  0,  0, OPACITY[0])]
PINK             = [(255,  64, 192, OPACITY[0]), (57, 16, 16, OPACITY[0])]
INFRA_RED        = [(255, 129,  24, OPACITY[0]), (68, 20, 19, OPACITY[0])]
RED              = [(255,  19,  21, OPACITY[0]), (88, 15, 12, OPACITY[0])]
ORANGE           = [(255, 200,  16, OPACITY[0]), (76, 30, 25, OPACITY[0])]
YELLOW           = [(255, 255,  15, OPACITY[0]), (45, 41, 10, OPACITY[0])]
GREEN            = [( 21, 255,  19, OPACITY[0]), (21, 54, 10, OPACITY[0])]
GREEN_BLUE       = [( 24, 255,  61, OPACITY[0]), (10, 49, 25, OPACITY[0])]
CYAN             = [( 23, 255, 255, OPACITY[0]), (16, 64, 64, OPACITY[0])]
BLUE_GREEN       = [( 25, 181, 255, OPACITY[0]), (12, 37, 51, OPACITY[0])]
BLUE             = [( 19,  21, 255, OPACITY[0]), (19, 11, 64, OPACITY[0])]
INDIGO           = [(255,  22, 255, OPACITY[0]), (19, 11, 64, OPACITY[0])]
VIOLET           = [(176,  81, 255, OPACITY[0]), (44, 14, 58, OPACITY[0])]
ULTRA_VIOLET     = [(194,  96, 255, OPACITY[3]), (50, 19, 61, OPACITY[1])]
HUES             = 16
MAX_STACK_DEPTH  = 0  ;  MAX_STACK_FRAME = inspect.stack()
####################################################################################################################################################################################################
def fmtl(a, w=None, d1='[', d2=']'):
    t = ''
    for i in range(len(a)):
        if w is None: t += '{} '.format(a[i])
        else:         t += '{:{w}} '.format(int(a[i]), w=w[i])
    return d1 + t.rstrip() + d2
def fmtd(a, d0=':', d1='[', d2=']'):
    t = ''  ;  i = 0
    for k, v in a.items():
        t += '{}{}{} '.        format(k, d0, v)
        i += 1
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
FONT_COLORS_L = [PINKS[0], CYANS[0], REDS[0], BLUES[0], YELLOWS[0], GREENS[0], ORANGES[2], PINKS[8], REDS[10], YELLOWS[15], GREEN_BLUES[8], ORANGES[12], INDIGOS[8], ULTRA_VIOLETS[9], BLUE_GREENS[8], CC]
FONT_COLORS   =  FONT_COLORS_S if SPRITES else FONT_COLORS_L
####################################################################################################################################################################################################
class Note(object):
    NUM_SEMI_TONES = 12
    SHARP_TONES    = { 0:'C', 1:'C#', 2:'D', 3:'D#', 4:'E', 5:'F', 6:'F#', 7:'G', 8:'G#', 9:'A', 10:'A#', 11:'B' }
    FLAT_TONES     = { 0:'C', 1:'Db', 2:'D', 3:'Eb', 4:'E', 5:'F', 6:'Gb', 7:'G', 8:'Ab', 9:'A', 10:'Bb', 11:'B' }
    INDICES = { 'C0': 0, 'C#0': 1, 'Db0': 1, 'D0': 2, 'D#0': 3, 'Eb0': 3, 'E0': 4, 'F0': 5, 'F#0': 6, 'Gb0': 6, 'G0': 7, 'G#0': 8, 'Ab0': 8, 'A0': 9, 'A#0':10, 'Bb0':10, 'B0':11,
                'C1':12, 'C#1':13, 'Db1':13, 'D1':14, 'D#1':15, 'Eb1':15, 'E1':16, 'F1':17, 'F#1':18, 'Gb1':18, 'G1':19, 'G#1':20, 'Ab1':20, 'A1':21, 'A#1':22, 'Bb1':22, 'B1':23,
                'C2':24, 'C#2':25, 'Db2':25, 'D2':26, 'D#2':27, 'Eb2':27, 'E2':28, 'F2':29, 'F#2':30, 'Gb2':30, 'G2':31, 'G#2':32, 'Ab2':32, 'A2':33, 'A#2':34, 'Bb2':34, 'B2':35,
                'C3':36, 'C#3':37, 'Db3':37, 'D3':38, 'D#3':39, 'Eb3':39, 'E3':40, 'F3':41, 'F#3':42, 'Gb3':42, 'G3':43, 'G#3':44, 'Ab3':44, 'A3':45, 'A#3':46, 'Bb3':46, 'B3':47,
                'C4':48, 'C#4':49, 'Db4':49, 'D4':50, 'D#4':51, 'Eb4':51, 'E4':52, 'F4':53, 'F#4':54, 'Gb4':54, 'G4':55, 'G#4':56, 'Ab4':56, 'A4':57, 'A#4':58, 'Bb4':58, 'B4':59,
                'C5':60, 'C#5':61, 'Db5':61, 'D5':62, 'D#5':63, 'Eb5':63, 'E5':64, 'F5':65, 'F#5':66, 'Gb5':66, 'G5':67, 'G#5':68, 'Ab5':68, 'A5':69, 'A#5':70, 'Bb5':70, 'B5':71,
                'C6':72, 'C#6':73, 'Db6':73, 'D6':74, 'D#6':75, 'Eb6':75, 'E6':76, 'F6':77, 'F#6':78, 'Gb6':78, 'G6':79, 'G#6':80, 'Ab6':80, 'A6':81, 'A#6':82, 'Bb6':82, 'B6':83,
                'C7':84, 'C#7':85, 'Db7':85, 'D7':86, 'D#7':87, 'Eb7':87, 'E7':88, 'F7':89, 'F#7':90, 'Gb7':90, 'G7':91, 'G#7':92, 'Ab7':92, 'A7':93, 'A#7':94, 'Bb7':94, 'B7':95,
                'C8':96 } # For simplicity omit double flats and double sharps and other redundant enharmonic note names e.g. Abb, C##, Cb, B#, Fb, E# etc...
    def __init__(self, i, ks=None):
        self.index = i
        self.ks    = ks
        self.name  = self.FLAT_TONES[i % len(self.FLAT_TONES)]
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
        self.n = []
        self.TNIK = [0, 0, 0, 0]
        self.log(f'TNIK={(fmtl(self.TNIK))}')
        self.nc = 6 if QQ else 6
        self.ww, self.hh  = 640, 480
        self.n, self.i, self.x, self.y, self.w, self.h, self.g = [1, 3, self.ssc(), 16, self.nc], [1, 1, 1, 3, 2], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], []
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
        self.log('stringCapo  = {} = {}'.format(fmtl(self.stringCapo), self.stringCapo))
        self._initWindowA()
        super().__init__(screen=self.screens[1], fullscreen=FULL_SCREEN, resizable=True, visible=False)
        self._initWindowB()
        self.pages,   self.lines,   self.sects,     self.cols    = [], [], [], []  ;  self.A = [self.pages,   self.lines,   self.sects,     self.cols]
        self.tabs,    self.notes,   self.intervals, self.chords  = [], [], [], []  ;  self.B = [self.tabs,    self.notes,   self.intervals, self.chords]
        self.snos,    self.snas,    self.capos,     self.blncs   = [], [], [], []  ;  self.C = [self.snos,    self.snas,    self.capos,     self.blncs]
        self.llRows,  self.llCols,  self.labels,    self.sprites = [], [], [], []  ;  self.D = [self.llRows,  self.llCols,  self.sprites,   self.labels]
        self.E = [*self.A, *self.B, *self.C, *self.D]
        self.log(f'E={self.E}')
        self.DF = [0, 0, 1, 1,  0, 0, 0, 0,  0, 0, 0, 0,  0, 0, 0, 0]
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
#    def ss(self):    s0 = sum(self.TNIK)  ;  s = s0 if s0 else 1  ;  txt = 'Forcing to non zero value' if not s0 else ''  ;  self.log(FMTR.format(f's0={s0} sum={s} TNIK={fmtl(self.TNIK)} n={self.n} {txt}'))  ;  return s
    def ss(self):    s = sum(self.TNIK)  ;  self.log(FMTR.format(f's={s} TNIK={fmtl(self.TNIK)} n={fmtl(self.n)}'))  ;  return s
    def ssc(self):   s = self.ss()  ;  sc = s if s else 1   ;   self.log(FMTR.format(f's={s} sc={sc} TNIK={fmtl(self.TNIK)} n={self.n}'))  ;  return sc
    def tpz(self):   return self.tpp, self.tpl, self.tps, self.tpc
    def lens(self):  return self.lenA(), self.lenB(), self.lenC(), self.lenD()
    def lenS(self):  return f'{fmtl(self.lenA())} {fmtl(self.lenB())} {fmtl(self.lenC())} {fmtl(self.lenD())}'
    def lenA(self):  return [len(e) for e in self.A]
    def lenB(self):  return [len(e) for e in self.B]
    def lenC(self):  return [len(e) for e in self.C]
    def lenD(self):  return [len(e) for e in self.D]
    def lenE(self):  return [len(e) for e in self.E]
    def initJ(self): self.J1 = [0 for _ in self.E]  ;  self.J2 = [0 for _ in self.E]  ;  self.dumpJ('initJ()')  ;  return self.J1, self.J2
    def dumpJ(self, why): self.log(f'J1({len(self.J1)}))={self.J1} {why}')  ;  self.log(f'J2({len(self.J2)}))={self.J2} {why}')
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
        self.log('(BGN) {}'.format(self.fmtGeom()))
        self.kp  = [VIOLETS[0], VIOLETS[12]] if CHECKER_BOARD else [VIOLETS[10]]
        self.kl  = [  BLUES[12],  BLUES[15]] if CHECKER_BOARD else [BLUES[12]]
        self.ks  = [   REDS[12],   REDS[15]] if CHECKER_BOARD else [REDS[12]]
        self.kc  = [  GRAYS[12],  GRAYS[15]] if CHECKER_BOARD else [GRAYS[12]]
        self.kt  = [YELLOWS[0], YELLOWS[8]]  if CHECKER_BOARD else [YELLOWS[0]]
        self.kn  = [  CYANS[0],   CYANS[8]]  if CHECKER_BOARD else [CYANS[0]]
        self.ki  = [  CYANS[0],   CYANS[8]]  if CHECKER_BOARD else [CYANS[0]]
        self.kk  = [  PINKS[0],   PINKS[8]]  if CHECKER_BOARD else [PINKS[0]]
        self.klr = [ORANGES[0], ORANGES[8]]  if CHECKER_BOARD else [ORANGES[0]]
        self.klc = [ GREENS[0],  GREENS[8]]  if CHECKER_BOARD else [GREENS[0]]
        self.k   = [self.kp, self.kl, self.ks, self.kc, self.kt, self.kn, self.ki, self.kk, self.klc, self.klr]
        [self.log(f'{fmtl(*e)}') for e in self.k]
        self.ssi = 0
        self._initTpz()
        self.readDataFile() if READ_DATA_FILE else self.createBlankData()
        self.labelTextA, self.labelTextB = ['R', 'M'], ['R', 'M']
        self.createLabelText()
        self.dumpJ('(BGN) createSprites() / createLabels()')
        self.ssc()
        self.createSprites() if SPRITES else  self.createLabels()
        self.dumpJ('(END) createSprites() / createLabels()')
#        self.createCursor(self.g[T + 3]) # fix
        if dbg: self.dumpStruct('_init')
        self.log('(END) {}'.format(self.fmtGeom()))

    def createLabelText(self):
        self.labelTextA.extend('{}'.format(j) for j in range(1, self.n[C] + 1))
        self.labelTextB.extend('{}'.format(j % 10 if j % 10 else j // 10 % 10) for j in range(1, self.n[C] + 1))
        texts = list(zip(self.labelTextA, self.labelTextB))
        self.dumpLabelText(texts)
    ####################################################################################################################################################################################################
    def on_draw(self):
        self.clear()
        self.batch.draw()
        if len(self.armSnap): self.snapshot(self.armSnap)  ;  self.armSnap = ''

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
#        self.resizeCursor()
        self.snapshot()
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
        self.log(f'{self.lenS()}')
        self.log(f'{self.fmtGeom()}')
        self.log('{} {}'.format(self.fmtWH(), self.fmtDataDim(self.data)))
        self.log('(END) {}'.format(why))
    ####################################################################################################################################################################################################
    def writeDataFile(self):
        self.log('(BGN) {}'.format(self.fmtDataDim(self.data)))
        data = self.transposeData(self.data) if self.isVert() else self.data
        with open(str(self.dataPath), 'w') as DATA_FILE:
            np, nl, nc, nr = self.d()  ;  nc += CCC
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
            t0 = Z * i + COL_L + Z       if        i >= 0 else COL_L
            self.log(t0, ind=0, end='') if lc and i >= 0 else self.log(Z * i, ind=0, end='')
            w = max(len(data[0][0][0]), len(LINE_L) + 1)
            for p in range(len(data)):
                for l in range(len(data[0])):
                    t = '{}{}'.format(LINE_L, l + 1)
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
        for i in range(2): self.log('{:3} '.format(' '), ind=0, end='')
        for k in range(len(t)//10):
            for i in range(9): self.log('{:^3} '.format(' '), ind=0, end='')
            self.log(' {} '.format(d), ind=0, end=' ')
        self.log(ind=0)
        for j in range(len(t)):
            self.log('{:^3}'.format(t[j][1]), ind=0, end=' ')
        self.log(ind=0)
        if dbg:
            for i in range(len(t)):
                self.log('{:5}'.format(i - 1), ind=0, end=' ')
                self.log(' {:>5}'.format(t[i][0]), ind=0, end=' ')
                d2 = ' ' if i == 1 or (i - 1) % 10 else d
                self.log('{}{:>5}'.format(d2, t[i][1]), ind=0, end=' ')
                self.log(ind=0)
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
    def createLLRow(self, p, pi, dbg=1, dbg2=1):
        nn = self.n[T] * self.ss() + 1  ;  klr = self.klr  ;  klc = self.klc  ;  kkr = self.cci(pi, klr)
        nr, ir, xr, yr, wr, hr, gr, mx, my = self.geom(p=p, j=S, nn=nn, dbg=dbg2)
        if SPRITES: xr += wr/2  ;  yr += hr/2
        row = self.createLabel(f'LR {pi+1}' if self.DF[12] else '', self.llRows, xr, yr, wr, hr, kkr, gr, why=f'create LR {pi+1}', kl=klr, dbg=dbg)
        nc, ic, xc, yc, wc, hc, gc, mx, my = self.geom(p=row, j=C, nn=self.n[C], dbg=dbg2)   ;  sc = nc * pi
        self.log(f'nc={nc} pi={pi} sc={sc} len(llCols)={len(self.llCols)}')
        if SPRITES: xc += wc/2
        for c in range(nc):
            sc +=  1  ;  kkc = self.cci(pi, klc)
            self.createLabel(f'{Z*(c+1)}{sc}' if self.DF[13] and not c else self.labelTextB[c], self.llCols, xc + c*wc, yc, wc, hc, kkc, gc, why=f'create LC {sc}', kl=klc, dbg=dbg)
        if dbg2: self.log('pi={:3} px={:7.2f} py={:7.2f} pw={:7.2f} ph={:7.2f}'.format(pi, p.x, p.y, p.width, p.height), ind=0)
        if dbg2: self.log('nr={:3} xr={:7.2f} yr={:7.2f} wr={:7.2f} hr={:7.2f}'.format(nr, xr, yr, wr, hr), ind=0)
        if dbg2: self.log('nc={:3} xc={:7.2f} yc={:7.2f} wc={:7.2f} hc={:7.2f}'.format(nc, xc, yc, wc, hc), ind=0)
        if   type(p) is pyglet.text.Label:    p.y -= hr/2  ;  p.height -= hr  ;                      self.log(f'p.y -= hr/2, p.h -= hr: p.y = {p.y:7.2f} p.h = {p.height:7.2f}', ind=0)
        elif type(p) is pyglet.sprite.Sprite: my = (p.height - hr)/self.h[L]  ;   p.scale_y = my  ;  self.log(f'p.y -= hr, my = (p.h-hr)/h[L]: h[L]={self.h[L]} my={my:7.5f} p.y={p.y:7.2f} p.h={p.height:7.2f}', ind=0)
        return p

    def resizeLLRow(self, p, pi, dbg=1, dbg2=1):
        nn = self.n[T] * self.ss() + 1  ;  i = 0
        nr, ir, xr, yr, wr, hr, gr, mxr, myr = self.geom(p=p, j=S, nn=nn, dbg=dbg2)
        if SPRITES: xr += wr/2  ;  yr += hr/2
        row = self.llRows[pi]  ;       i += 1  ;   row.width = wr  ;   row.height = hr  ;   row.x = xr  ;   row.y = yr
        if dbg: self.dumpLabel(row, *self.ids(), *self.cnts(), why=f'resize LR {pi+1}')
        nc, ic, xc, yc, wc, hc, gc, mxc, myc = self.geom(p=row, j=C, dbg=dbg)   ;  sc = nc * pi
        self.log(f'nc={nc} pi={pi} sc={sc} len(llCols)={len(self.llCols)}')
        if SPRITES: xc += wc/2
        for c in range(nc):
            text = self.llCols[sc]   ;     text.width = wc   ;   text.height = hc  ;   text.x = xc + c * wc  ;  text.y = yc  ;  sc += 1  ;  i += 1
            if dbg: self.dumpLabel(text, *self.ids(), *self.cnts(), why=f'resize LC {sc}')
        if dbg2: self.log(f'row.y={row.y:7.2f} yr={yr:7.2f} pi={pi} hr={hr:7.2f}', ind=0)
        if dbg2: self.log('pi={:3} px={:7.2f} py={:7.2f} pw={:7.2f} ph={:7.2f}'.format(pi, p.x, p.y, p.width, p.height), ind=0)
        if dbg2: self.log('nr={:3} xr={:7.2f} yr={:7.2f} wr={:7.2f} hr={:7.2f}'.format(nr, xr, yr, wr, hr), ind=0)
        if dbg2: self.log('nc={:3} xc={:7.2f} yc={:7.2f} wc={:7.2f} hc={:7.2f}'.format(nc, xc, yc, wc, hc), ind=0)
        if   type(p) is pyglet.text.Label:    p.y -= hr/2  ;  p.height -= hr  ;                               self.log(f'p.y -= hr/2, p.h -= hr: p.y = {p.y:7.2f} p.h = {p.height:7.2f}', ind=0)
        elif type(p) is pyglet.sprite.Sprite: my = (p.height - hr)/self.h[L]  ;   p.scale_y = my  ;  self.log(f'p.y -= hr, my = (p.h-hr)/h[L]: h[L]={self.h[L]} my={my:7.5f} p.y={p.y:7.2f} p.h={p.height:7.2f}', ind=0)
        self.log('p.y -= hr/2, p.height -= hr: p.y = {:7.2f} p.h = {:7.2f}'.format(p.y, p.height), ind=0)
        return p
    ####################################################################################################################################################################################################
    def toggleLLRows(self):
        global QQ  ;  old = QQ  ;  QQ = not QQ  ;  self.log(f'old QQ={old} new QQ={QQ}')
        if QQ and not self.llRows: self.showLLRows()
        else:                       self.hideLLRows()
        self.on_resize(self.ww, self.hh)

    def showLLRows(self):
        for l in range(len(self.lines)):
            self.log(f'l={l}')
            self.createLLRow(self.lines[l], l)

    def hideLLRows(self):
        nr = len(self.llRows)    ;  nc = len(self.llCols)  ;  assert not nc % nr
        nc = nc // nr
        for rr in range(nr):
            r = self.llRows[rr]  ;  rx, ry, rw, rh = r.x, r.y, r.width, r.height
            r.x, r.y, r.width, r.height = 0, 0, 0, 0
            self.log(f' rr={rr:3} nr={nr:3}     before {rx:7.2f} {ry:7.2f} {rw:7.2f} {rh:7.2f}    after {r.x:7.2f} {r.y:7.2f} {r.width:7.2f} {r.height:7.2f}', ind=0)
            for cc in range(nc):
                c = self.llCols[cc + rr * nc]  ;  cx, cy, cw, ch = c.x, c.y, c.width, c.height
                c.x, c.y, c.width, c.height = 0, 0, 0, 0
                self.log(f'     cc={cc:3} nc={nc:3} before {cx:7.2f} {cy:7.2f} {cw:7.2f} {ch:7.2f}    after {c.x:7.2f} {c.y:7.2f} {c.width:7.2f} {c.height:7.2f}', ind=0)
    ####################################################################################################################################################################################################
    def toggleTabs(self):
        self.log(f'(BGN) TNIK={fmtl(self.TNIK)} n={fmtl(self.n)}')
        if self.TNIK[TT] and not self.tabs: self.showTabs()
        else:                                self.showTabs()
        self.log(f'      TNIK={fmtl(self.TNIK)} n={fmtl(self.n)}')
        self.TNIK[TT] = not self.TNIK[TT]
#        self.n[S] = self.ss()
        self.log(f'(END) TNIK={fmtl(self.TNIK)} n={fmtl(self.n)}')
        self.on_resize(self.ww, self.hh)

    def toggleNotes(self):
        self.log(f'(BGN) TNIK={fmtl(self.TNIK)} n={fmtl(self.n)}')
        self.TNIK[NN] = not self.TNIK[NN]
        self.n[S] = self.ss()
        if self.TNIK[NN] and not self.notes: self.showNotes()
        else:                                self.hideNotes()
        self.log(f'(END) TNIK={fmtl(self.TNIK)} n={fmtl(self.n)}')
        self.on_resize(self.ww, self.hh)

    def toggleChords(self):
        self.log(f'(BGN) TNIK={fmtl(self.TNIK)} n={fmtl(self.n)}')
        self.TNIK[KK] = not self.TNIK[KK]
        self.n[S] = self.ss()
        if self.TNIK[KK] and not self.chords: self.showChords()
        else:                                self.hideChords()
        self.log(f'(END) TNIK={fmtl(self.TNIK)} n={fmtl(self.n)}')
        self.on_resize(self.ww, self.hh)
    ####################################################################################################################################################################################################
    def hideTabs(self, dbg=1):
        nl = len(self.lines)  ;  ns = len(self.sects)  ;  nc = len(self.cols)  ;  nt = len(self.tabs)
        self.log(f'(BGN) nl={nl} ns={ns} nc={nc} nt={nt}')
        self.dumpJ('(BGN) hideTabs()')
        for i in range(ns):
            s = self.sects[i]
            if SPRITES: s.update(x=0, y=0, scale_x=0, scale_y=0)
            else:       s.x, s.y, s.w, s.h = 0, 0, 0, 0  # ;  s.text = ''
            self.log(f'sects i={i}')
        for i in range(nc):
            c = self.cols[i]
            if SPRITES: c.update(x=0, y=0, scale_x=0, scale_y=0)
            else:       c.x, c.y, c.w, c.h = 0, 0, 0, 0  # ;  c.text = ''
            self.log(f'cols i={i}')
        for i in range(nt):
            t = self.tabs[i]  ;  x, y, w, h = t.x, t.y, t.width, t.height
            t.x, t.y, t.width, t.height = 0, 0, 0, 0  ;  text = self.tabs[i].text  # ;  n.text = ''
            if dbg: self.log(f'{text} [{x:7.2f} {y:7.2f} {w:7.2f} {h:7.2f}] {t.text:6} [{t.x:7.2f} {t.y:7.2f} {t.width:7.2f} {t.height:7.2f}]')
        self.dumpJ('(END) hideTabs()')
        self.log(f'(END) nl={nl} ns={ns} nc={nc} nt={nt}')

    def hideNotes(self, dbg=1):
        nl = len(self.lines)  ;  ns = len(self.sects)  ;  nc = len(self.cols)  ;  nt = len(self.tabs)
        self.log(f'(BGN) nl={nl} ns={ns} nc={nc} nt={nt}')
        self.dumpJ('(BGN) hideNotes()')
        for i in range(ns):
            s = self.sects[i]
            if SPRITES: s.update(x=0, y=0, scale_x=0, scale_y=0)
            else:       s.x, s.y, s.w, s.h = 0, 0, 0, 0  # ;  s.text = ''
            self.log(f'sects i={i}')
        for i in range(nc):
            c = self.cols[i]
            if SPRITES: c.update(x=0, y=0, scale_x=0, scale_y=0)
            else:       c.x, c.y, c.w, c.h = 0, 0, 0, 0  # ;  c.text = ''
            self.log(f'cols i={i}')
        for i in range(nt):
            n = self.notes[i]  ;  x, y, w, h = n.x, n.y, n.width, n.height
            n.x, n.y, n.width, n.height = 0, 0, 0, 0  ;  text = self.tabs[i].text  # ;  n.text = ''
            if dbg: self.log(f'{text} [{x:7.2f} {y:7.2f} {w:7.2f} {h:7.2f}] {n.text:6} [{n.x:7.2f} {n.y:7.2f} {n.width:7.2f} {n.height:7.2f}]')
        self.dumpJ('(END) hideNotes()')
        self.log(f'(END) nl={nl} ns={ns} nc={nc} nt={nt}')

    def hideChords(self, dbg=1):
        nl = len(self.lines)  ;  ns = len(self.sects)  ;  nc = len(self.cols)  ;  nt = len(self.tabs)
        self.log(f'(BGN) nl={nl} ns={ns} nc={nc} nt={nt}')
        self.dumpJ('(BGN) hideChords()')
        for i in range(ns):
            s = self.sects[i]
            if SPRITES: s.update(x=0, y=0, scale_x=0, scale_y=0)
            else:       s.x, s.y, s.w, s.h = 0, 0, 0, 0  # ;  s.text = ''
            self.log(f'sects i={i}')
        for i in range(nc):
            c = self.cols[i]
            if SPRITES: c.update(x=0, y=0, scale_x=0, scale_y=0)
            else:       c.x, c.y, c.w, c.h = 0, 0, 0, 0  # ;  c.text = ''
            self.log(f'cols i={i}')
        for i in range(nt):
            k = self.chords[i]  ;  x, y, w, h = k.x, k.y, k.width, k.height
            k.x, k.y, k.width, k.height = 0, 0, 0, 0  ;  text = self.tabs[i].text  # ;  n.text = ''
            if dbg: self.log(f'{text} [{x:7.2f} {y:7.2f} {w:7.2f} {h:7.2f}] {k.text:6} [{k.x:7.2f} {k.y:7.2f} {k.width:7.2f} {k.height:7.2f}]')
        self.dumpJ('(END) hideChords()')
        self.log(f'(END) nl={nl} ns={ns} nc={nc} nt={nt}')
    ####################################################################################################################################################################################################
    def showTabs(self, dbg=1):
        np, nl, ns, nc, nt = self.n
        ks = self.ks  ;  kc = self.kc  ;   kt = self.kt  ;  v = 1  ;  tsects = []
        self.log(f'(BGN) TNIK={fmtl(self.TNIK)} nl={nl} ns={ns} nc={nc} nt={nt}')
        self.dumpJ('(BGN) showTabs()')
        for p in range(np):
            for l in range(nl):
                for c in range(nc):
                    for t in range(nt):
                        self.J1[T] = t
                        self.J2[T] += 1
                        why = f'create Tab {self.J2[T]}'
                        self.log(f'{p} {l} {c} {t}', ind=0, end=' ')
                        tab = self.data[p][l][c][t]
                        self.createLabel(tab, p=self.tabs, x=0, y=0, w=0, h=0, kk=self.cci(t, kt), g=self.g[T], why=why, kl=kt, dbg=dbg)

    def showTabs_OLD(self, dbg=1):
        nl, ns, nc = self.J2[L], self.J2[S], self.J2[C]  ;  nc = (nc * nl) // ns  ;  nt = self.n[L] * self.n[S] * self.n[C] * self.n[T]
        ks = self.ks  ;  kc = self.kc  ;   kt = self.kt  ;  v = 1  ;  tsects = []
        self.log(f'(BGN) TNIK={fmtl(self.TNIK)} nl={nl} ns={ns} nc={nc} nt={nt}')
        self.dumpJ('(BGN) showTabs()')   ;  inner = 0
        if not self.TNIK[TT] and self.ss():
            inner = 1
            nt = self.J2[T]
            for s in range(nl):
                self.J1[S] = s + ns # * self.TNIK[TT]
                self.J2[S] += 1
                why  = f'create Sect {self.J2[S]}'
                text = f'Sect {self.J2[S]}' if self.DF[S] else ''
                if SPRITES: self.createSprite(p=tsects, x=0, y=0, w=self.w[S], h=self.h[S], kk=self.cci(s, ks), g=self.g[S], why=why, kl=ks, v=v, dbg=dbg)
                else:       self.createLabel(text, p=tsects, x=0, y=0, w=0, h=0, kk=S, g=self.g[S], why=why, kl=None, dbg=dbg)
            self.dumpObjs(self.sects, 'self.sects', f'merging len={len(self.sects)}')
            self.dumpObjs(     tsects, '   tsects', f'merging len={len(tsects)}')
            self.sects.extend(tsects)
            self.dumpObjs(self.sects, 'self.sects', f'merging len={len(self.sects)}')
            for c in range(nc):
                self.J1[C] = c
                self.J2[C] += 1
                why = f'create C {self.J2[C]}'
                if SPRITES: self.createSprite(p=self.cols, x=0, y=0, w=self.w[C], h=self.h[C], kk=self.cci(c, kc), g=self.g[C], why=why, kl=kc, v=v, dbg=dbg)
                else:       self.createLabel(f'C {self.J2[C]}' if self.DF[C] else '', p=self.cols, x=0, y=0, w=0, h=0, kk=C, g=self.g[C], why=why, kl=None, dbg=dbg)
        self.log(f'tpz={self.tpz()}')
#        for tt in range(nt):
#            t = tt % self.n[T]
#            self.J1[T] = t
#            self.J2[T] += 1
#            why = f'create Tab {self.J2[T]}'
#            if inner: p, l, c = self.J1[P],  self.J1[L],   self.J1[C]
#            else:     p, l, c = tt // (self.n[L] * self.n[C] * self.n[T]), tt // (self.n[C] * self.n[T]), tt // self.n[T]
#            self.log(f'p={p} l={l} c={c} t={t} tt={tt}', ind=0, end=' ')
#            tab = self.data[p][l][c][t]
#            self.createLabel(tab, p=self.tabs, x=0, y=0, w=0, h=0, kk=self.cci(t, kt), g=self.g[T], why=why, kl=kt, dbg=dbg)
        self.dumpJ('(END) showTabs()')
        self.log(f'(END) TNIK={self.TNIK} nl={nl} ns={ns} nc={nc} nt={nt}')

    def showNotes(self, dbg=1):
        nl, ns, nc, nt = self.J2[L], self.J2[S], self.J2[C], self.J2[T]  ;  nc = (nc * nl) // ns
        ks = self.ks  ;  kc = self.kc  ;   kn = self.kn  ;  v = 1  ;  nsects = []
        self.log(f'(BGN) TNIK={self.TNIK} nl={nl} ns={ns} nc={nc} nt={nt}')
        self.dumpJ('(BGN) showNotes()')
        for s in range(nl):
            self.J1[S] = s + ns * self.TNIK[NN]
            self.J2[S] += 1
            why  = f'create Sect {self.J2[S]}'
            text = f'Sect {self.J2[S]}' if self.DF[S] else ''
            if SPRITES: self.createSprite(p=nsects, x=0, y=0, w=self.w[S], h=self.h[S], kk=self.cci(s, ks), g=self.g[S], why=why, kl=ks, v=v, dbg=dbg)
            else:       self.createLabel(text, p=nsects, x=0, y=0, w=0, h=0, kk=S, g=self.g[S], why=why, kl=None, dbg=dbg)
        self.dumpObjs(self.sects, 'self.sects', f'merging len={len(self.sects)}')
        self.dumpObjs(     nsects, '   nsects', f'merging len={len(nsects)}')
        self.sects.extend(nsects)
        self.dumpObjs(self.sects, 'self.sects', f'merging len={len(self.sects)}')
        for c in range(nc):
            self.J1[C] = c
            self.J2[C] += 1
            why = f'create C {self.J2[C]}'
            if SPRITES: self.createSprite(p=self.cols, x=0, y=0, w=self.w[C], h=self.h[C], kk=self.cci(c, kc), g=self.g[C], why=why, kl=kc, v=v, dbg=dbg)
            else:       self.createLabel(f'C {self.J2[C]}' if self.DF[C] else '', p=self.cols, x=0, y=0, w=0, h=0, kk=C, g=self.g[C], why=why, kl=None, dbg=dbg)
        for t in range(nt):
            tt = t % self.n[T]
            self.J1[N] = tt
            self.J2[N] += 1
            text = self.tabs[t].text
            note = self.getNote(t % self.n[T], text).name if self.isFret(text) else self.nblank
            why = f'create Note {self.J2[N]}'
            self.createLabel(note, p=self.notes, x=0, y=0, w=0, h=0, kk=self.cci(t, kn), g=self.g[T], why=why, kl=kn, dbg=dbg)
        self.dumpJ('(END) showNotes()')
        self.log(f'(END) TNIK={self.TNIK} nl={nl} ns={ns} nc={nc} nt={nt}')

    def showChords(self, dbg=1):
        nl, ns, nc, nt = self.J2[L], self.J2[S], self.J2[C], self.J2[T]  ;  nc = (nc * nl) // ns
        ks = self.ks  ;  kc = self.kc  ;  kk = self.kk  ;  v = 1  ;  ksects = []
        self.log(f'(BGN) TNIK={self.TNIK} nl={nl} ns={ns} nc={nc} nt={nt}')
        self.dumpJ('(BGN) showChords()')
        for s in range(nl):
            self.J1[S] = s + ns
            self.J2[S] += 1
            why  = f'create Sect {self.J2[S]}'
            text = f'Sect {self.J2[S]}' if self.DF[S] else ''
            if SPRITES: self.createSprite(p=ksects, x=0, y=0, w=self.w[S], h=self.h[S], kk=self.cci(s, ks), g=self.g[S], why=why, kl=ks, v=v, dbg=dbg)
            else:       self.createLabel(text, p=ksects, x=0, y=0, w=0, h=0, kk=S, g=self.g[S], why=why, kl=None, dbg=dbg)
        self.dumpObjs(self.sects, 'self.sects', f'merging len={len(self.sects)}')
        self.dumpObjs(     ksects, '   ksects', f'merging len={len(ksects)}')
        self.sects.extend(ksects)
        self.dumpObjs(self.sects, 'self.sects', f'merging len={len(self.sects)}')
        for c in range(nc):
            self.J1[C] = c
            self.J2[C] += 1
            why = f'create C {self.J2[C]}'
            if SPRITES: self.createSprite(p=self.cols, x=0, y=0, w=self.w[C], h=self.h[C], kk=self.cci(c, kc), g=self.g[C], why=why, kl=kc, v=v, dbg=dbg)
            else:       self.createLabel(f'C {self.J2[C]}' if self.DF[C] else '', p=self.cols, x=0, y=0, w=0, h=0, kk=C, g=self.g[C], why=why, kl=None, dbg=dbg)
        for t in range(nt):
            tt = t % self.n[T]
            self.J1[K] = tt
            self.J2[K] += 1
            why = f'create Chord {self.J2[K]}'
            chordName = self.getChordName()
            chord = chordName[tt] if len(chordName) > tt else ' '
            self.createLabel(chord, p=self.chords, x=0, y=0, w=0, h=0, kk=self.cci(t, kk), g=self.g[T], why=why, kl=kk, dbg=dbg)
        self.dumpJ('(END) showChords()')
        self.log(f'(END) TNIK={self.TNIK} nl={nl} ns={ns} nc={nc} nt={nt}')
    ####################################################################################################################################################################################################
    def createLabels(self, dbg=1, dbg2=0):
        self.log('(BGN) {}'.format(self.fmtGeom()))
        if dbg: self.dumpLabel()
        for p, page in                  enumerate(self.g_createLabels(None, P, self.pages, why='Page ', dbg=dbg, dbg2=dbg2)):
            for l, line in              enumerate(self.g_createLabels(page, L, self.lines, why='Line ', dbg=dbg, dbg2=dbg2)):
                for s, sect in          enumerate(self.g_createLabels(line, S, self.sects, why='Sect ', dbg=dbg, dbg2=dbg2)):
                    for c, col in       enumerate(self.g_createLabels(sect, C, self.cols,  why='C ',    dbg=dbg, dbg2=dbg2)):
                        for t, lbl in   enumerate(self.g_createLabels2(col)):
                            if dbg > 1: self.log(f'lbl.y={lbl.y}')
        if dbg: self.dumpLabel()
        self.log('(END) {}'.format(self.fmtGeom()))

    def g_createLabels(self, p, j, lablist, why, dbg=1, dbg2=0):
        n, ii, x, y, w, h, g, mx, my = self.geom(p=p, j=j, init=1, dbg=dbg2)  ;  x2 = x  ;  y2 = y
        for m in range(n):
            if   j == C: x2 = x + m * w
            elif p:      y2 = y - m * h
            self.J1[j] = m
            self.J2[j] += 1
            text = f'{why}{self.J2[j]}' if self.DF[j] else ''  ;  why2 = f'create {why}{self.J2[j]}'
            lbl = self.createLabel(text=text, p=lablist, x=x2, y=y2, w=w, h=h, kk=j, g=g, why=why2, kl=None, dbg=dbg)
#            if     lablist: lbl.text = text  ;  lbl.x = x2  ;  lbl.y = y2  ;  lbl.width = w  ;  lbl.height = h  ;  self.dumpLabel(lbl, len(self.sprites), len(self.labels), *self.lenA(), *self.lenB(), why)
#            else:           lbl = self.createLabel(text=text, p=lablist, x=x2, y=y2, w=w, h=h, kk=j, g=g, why=why2, kl=None, dbg=dbg)
            if QQ and j == L: self.createLLRow(lbl, m)
            yield lbl
    ####################################################################################################################################################################################################
    def g_createLabels2(self, col, dbg=1, dbg2=0):
        p, l, s, c = self.J1[P], self.J1[L], self.J1[S], self.J1[C]  ;  cc = (self.n[S] + 1) * self.n[C] * self.n[T]
        nt, it, xt, yt, wt, ht, gt, mx, my = self.geom(p=col, j=T, init=1, dbg=dbg2)  ;  kt, kn, kk = self.kt, self.kn, self.kk
        for t in range(nt):
#            self.log(f't={t} nt={nt} TNIK={self.TNIK} st={self.J2[T]}')
            if   self.TNIK[TT] and s == 0:
                if   CCC     and c == SNO_C:   tab = self.stringNumbs[t]    ;  plist = self.snos   ;  kl = None  ;  k = T                ;  self.J2[O] += 1  ;  why = f'create  SNo {self.J2[O]}'
                elif CCC > 1 and c == CFN_C:   tab = self.stringCapo[t]     ;  plist = self.capos  ;  kl = None  ;  k = T                ;  self.J2[D] += 1  ;  why = f'create Capo {self.J2[D]}'
                else:                          tab = self.data[p][l][c][t]  ;  plist = self.tabs   ;  kl = kt    ;  k = self.cci(t, kl)  ;  self.J2[T] += 1  ;  why = f'create  Tab {self.J2[T]}'
                self.createLabel(tab,   plist,  xt, yt - t*ht, wt, ht, k, gt, why=why, kl=kl, dbg=dbg)  ;  yield tab
            elif self.TNIK[NN] and (s == 0 or (s == 1 and self.J2[N] < cc))  :
                if   CCC     and c == SNA_C:  note = self.stringNames[t]    ;  plist = self.snas   ;  kl = None  ;  k = -N               ;  self.J2[A] += 1  ;  why = f'create SNam {self.J2[A]}'
                elif CCC > 1 and c == CFN_C:  note = self.stringCapo[t]     ;  plist = self.capos  ;  kl = None  ;  k = -N               ;  self.J2[T] += 1  ;  why = f'create Capo {self.J2[T]}'
                else:                          tab = self.data[p][l][c][t]  ;  plist = self.notes  ;  kl = kn    ;  k = self.cci(t, kl)  ;  self.J2[N] += 1  ;  why = f'create Note {self.J2[N]}'  ;  note = self.getNote(t, tab).name if self.isFret(tab) else self.nblank
                self.createLabel(note,  plist,  xt, yt - t*ht, wt, ht, k, gt, why=why, kl=kl, dbg=dbg)  ;  yield note
            elif self.TNIK[KK] and (s == 0 or (s == 1 and self.J2[K] < cc) or (s == 2 and self.J2[K] < cc)):
                if   CCC     and c == SNO_C: chord = ' '                    ;  plist = self.blncs  ;  kl = None  ;  k = -K               ;  self.J2[B] += 1  ;  why = f'create Blncs {self.J2[B]}'
                elif CCC > 1 and c == CFN_C: chord = ' '                    ;  plist = self.blncs  ;  kl = None  ;  k = -K               ;  self.J2[B] += 1  ;  why = f'create Blncs {self.J2[B]}'
                else:                      chordName = self.getChordName()  ;  plist = self.chords ;  kl = kk    ;  k = self.cci(t, kl)  ;  self.J2[K] += 1  ;  why = f'create Chord {self.J2[K]}'  ;  chord = chordName[t] if len(chordName) > t else ' '
                self.createLabel(chord, plist,  xt, yt - t*ht, wt, ht, k, gt, why=why, kl=kl, dbg=dbg)  ;  yield chord
    ####################################################################################################################################################################################################
    def createSprites(self, dbg=1, dbg2=0):
        self.log('(BGN) {}'.format(self.fmtGeom()))  ;  v = 0
        if dbg: self.dumpLabel()  ;  self.dumpSprite()
        for p, (page, v) in             enumerate(self.g_createSprites(None, P, self.pages, v, why=' Page ', dbg=dbg, dbg2=dbg2)):
            for l, (line, _) in         enumerate(self.g_createSprites(page, L, self.lines, v, why=' Line ', dbg=dbg, dbg2=dbg2)):
                for s, (sect, _) in     enumerate(self.g_createSprites(line, S, self.sects, v, why=' Sect ', dbg=dbg, dbg2=dbg2)):
                    for c, (col, _) in  enumerate(self.g_createSprites(sect, C, self.cols,  v, why=' C ',    dbg=dbg, dbg2=dbg2)):
                        for t, lbl in   enumerate(self.g_createLabels2(col)):
                            if dbg > 1: self.log(f'lbl.y={lbl.y}')
        self.log(f'lenS={self.lenS()}')
        if dbg: self.dumpSprite()  ;  self.dumpLabel()
        self.log('(END) {}'.format(self.fmtGeom()))

    def g_createSprites(self, p, j, sprlist, v, why, dbg=1, dbg2=1):
        n, ii, x, y, w, h, g, mx, my = self.geom(p=p, j=j, init=1, dbg=dbg2)  ;  x2 = x  ;  y2 = y  ;  kl=self.k[j]
        for m in range(n):
            if   j == C:     x2 = x + m * w
            elif p:          y2 = y - m * h
            self.J1[j] = m
            self.J2[j] += 1
            if   j == P:    v=1 if self.J2[j] == self.i[P] else 0
            spr = self.createSprite(sprlist, x2, y2, w, h, self.cci(j, kl), g, why=f'create{why}{self.J2[j]}', kl=kl, v=v, dbg=dbg)
            if QQ and j == L: self.createLLRow(spr, m)
            yield spr, v
    ####################################################################################################################################################################################################
    def resizeLabels(self, dbg=1):
        self.log('(BGN) {}'.format(self.fmtGeom()))
        if dbg: self.dumpLabel()
        for p, page in                  enumerate(self.g_resizeLabels(None, P, self.pages, why=f' Page ')):
            for l, line in              enumerate(self.g_resizeLabels(page, L, self.lines, why=f' Line ')):
                for s, sect in          enumerate(self.g_resizeLabels(line, S, self.sects, why=f' Sect ')):
                    for c, col in       enumerate(self.g_resizeLabels(sect, C, self.cols,  why=f' C ')):
                        for t, lbl in   enumerate(self.g_resizeLabels2(col)):
                            if dbg > 1: self.log(f'lbl.y={lbl.y}')
        if dbg: self.dumpLabel()
        self.log('(END) {}'.format(self.fmtGeom()))

    def g_resizeLabels(self, p, j, lablist, why, dbg=1, dbg2=0):
        n, ii, x, y, w, h, g, mx, my = self.geom(p=p, j=j, dbg=dbg2)  ;  x2 = x  ;  y2 = y
        for m in range(n):
            if   j == C: x2 = x + m * w
            elif p:      y2 = y - m * h
            lbl = lablist[self.J2[j]]  ;  lbl.x = x2  ;  lbl.y = y2  ;  lbl.width = w  ;  lbl.height = h
            self.J1[j] = m
            self.J2[j] += 1
            if dbg: self.dumpLabel(lbl, *self.ids(), *self.cnts(), why=f'resize{why}{self.J2[j]}')
            if QQ and j == L: self.resizeLLRow(lbl, m)
            yield lbl
    ####################################################################################################################################################################################################
    def g_resizeLabels2(self, col, dbg=1, dbg2=0): # s, c
        n, ii, x, y, w, h, g, mx, my = self.geom(p=col, j=T, dbg=dbg2)  ;  lbl = None  ;  cc = (self.n[S] + 1) * self.n[C] * self.n[T]
        p,       l,    s,    c = self.J1[P], self.J1[L], self.J1[S], self.J1[C]
        st,     sn,   si,   sk = self.J2[T], self.J2[N], self.J2[I], self.J2[K]
        ssno, ssna, scap, sbln = self.J2[O], self.J2[A], self.J2[D], self.J2[B]
        for t in range(n):
#            self.log(f't={t} n={n} TNIK={self.TNIK} st={st}')
            if   self.TNIK[TT] and s == 0:
                if   CCC     and c == SNO_C:   tab = self.snos[ssno]     ;  ssno += 1  ;    why = f'resize  SNo {ssno}'
                elif CCC > 1 and c == CFN_C:   tab = self.capos[scap]    ;  scap += 1  ;    why = f'resize Capo {scap}'
                else:                          tab = self.tabs[st]       ;    st += 1  ;    why = f'resize  Tab {st}'
                tab.width = w    ;   tab.height = h    ;   tab.x = x     ;  tab.y = y - t * h  ;  lbl = tab
                self.J1[T] = t   ;  self.J2[T] = st    ;  self.J2[O] = ssno  ;  self.J2[D] = scap
                if dbg:   self.dumpLabel(  lbl, *self.ids(), *self.cnts(), why=why)
            elif self.TNIK[NN] and (s == 0 or (s == 1 and self.J2[N] < cc))  :
                if   CCC     and c == SNA_C:  note = self.snas[ssna]     ;  ssna += 1  ;    why = f'resize SNam {ssna}'
                elif CCC > 1 and c == CFN_C:  note = self.capos[scap]    ;  scap += 1  ;    why = f'resize Capo {scap}'
                else:                         note = self.notes[sn]      ;    sn += 1  ;    why = f'resize Note {sn}'
                note.width = w   ;  note.height = h    ;   note.x = x    ;    note.y = y - t * h  ;  lbl = note
                self.J1[N] = t   ;  self.J2[N] = sn  ;  self.J2[A] = ssna  ;  self.J2[D] = scap
                if dbg:   self.dumpLabel( lbl, *self.ids(), *self.cnts(), why=why)
            elif self.TNIK[KK] and (s == 0 or (s == 1 and self.J2[K] < cc) or (s == 2 and self.J2[K] < cc)):
                if   CCC     and c == SNO_C: chord = self.blncs[sbln]    ;  sbln += 1  ;  why = f'resize Blncs {sbln}'
                elif CCC > 1 and c == CFN_C: chord = self.blncs[sbln]    ;  sbln += 1  ;  why = f'resize Blncs {sbln}'
                else:                        chord = self.chords[sk]     ;    sk += 1  ;  why = f'resize Chord {sk}'
                chord.width = w  ;  chord.height = h  ;  chord.x = x  ;  chord.y = y - t * h  ;  lbl = chord
                self.J1[K] = t   ;  self.J2[K] = sk  ;  self.J2[B] = sbln
                if dbg:   self.dumpLabel(lbl, *self.ids(), *self.cnts(), why=why)
            yield lbl
    ####################################################################################################################################################################################################
    def resizeSprites(self, dbg=1):
        self.log('(BGN) {}'.format(self.fmtGeom()))
        if dbg: self.dumpSprite()
        self.log(f'lenS={self.lenS()}')
        for p, page in                enumerate(self.g_resizeSprites(None, P, self.pages, why=f' Page ')):
            for l, line in            enumerate(self.g_resizeSprites(page, L, self.lines, why=f' Line ')):
                for s, sect in        enumerate(self.g_resizeSprites(line, S, self.sects, why=f' Sect ')):
                    for c, col in     enumerate(self.g_resizeSprites(sect, C, self.cols,  why=f' C ')):
                        for t, lbl in enumerate(self.g_resizeLabels2(col)):
                            if dbg > 1: self.log(f'lbl.y={lbl.y}')
        if dbg: self.dumpLabel()  ;  self.dumpSprite()
        self.log('(END) {}'.format(self.fmtGeom()))

    def g_resizeSprites(self, p, j, sprlist, why, dbg=1, dbg2=1):
        nn = self.n[j] if QQ else 0
        n, ii, x, y, w, h, g, mx, my = self.geom(p=p, j=j, nn=nn, dbg=dbg2)  ;  x2 = x  ;  y2 = y
        for m in range(n):
            if   j == C: x2 = x + m * w
            elif p:      y2 = y - m * h
            spr = sprlist[self.J2[j]]
            spr.update(x=x2, y=y2, scale_x=mx, scale_y=my)
            self.J1[j] = m
            self.J2[j] += 1
            if dbg: self.dumpSprite(spr, *self.ids(), *self.cnts(), why = f'resize{why}{self.J2[j]}')
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
        if dbg: self.dumpSprite(spr, len(self.sprites), len(self.labels), *self.lenA(), *self.lenB(), why)
        return spr

    def createLabel(self, text, p, x, y, w, h, kk, g, why, kl=None, m=0, dbg=0):
        a, ax, ay = 'center', 'center', 'center' # left center right  # bottom baseline center top
        b = self.batch
        o, k, d, j, n, s = self.fontParams()
        d = FONT_DPIS[d]
        n = FONT_NAMES[n]
        k = FONT_COLORS[(k + kk) % len(FONT_COLORS)] if kl is None else kl[kk]
        if m:
            for i in range(len(text), 0, -1): text = text[:i] + '\n' + text[i:]
        lbl = pyglet.text.Label(text, font_name=n, font_size=s, bold=o, italic=j, color=k, x=x, y=y, width=w, height=h, anchor_x=ax, anchor_y=ay, align=a, dpi=d, batch=b, group=g, multiline=m)
        self.labels.append(lbl)
        p.append(lbl)
        if dbg: self.dumpLabel(lbl, len(self.sprites), len(self.labels), *self.lenA(), *self.lenB(), why)
        return lbl
    ####################################################################################################################################################################################################
    def dumpSprites(self, why=''):
        self.log('(BGN) {} {}'.format(self.fmtGeom(), why))
        np, nl, ns, nr, nc = self.n
        self.dumpSprite()
        i, sp, sl, ss, sc, st, sn, si, sk = 0, 0, 0, 0, 0, 0, 0, 0, 0
        for p in range(np):
            sp += 1                 ; self.dumpSprite(self.sprites[i], i+1, len(self.labels), sp, sl, ss, sc, st, sn, si, sk, 'Page') ; i += 1
            for l in range(nl):
                sl += 1             ; self.dumpSprite(self.sprites[i], i+1, len(self.labels), sp, sl, ss, sc, st, sn, si, sk, 'Line') ; i += 1
                for s in range(ns):
                    ss += 1         ; self.dumpSprite(self.sprites[i], i+1, len(self.labels), sp, sl, ss, sc, st, sn, si, sk, 'Sect') ; i += 1
                    for c in range(nc):
                        sc += 1     ; self.dumpSprite(self.sprites[i], i+1, len(self.labels), sp, sl, ss, sc, st, sn, si, sk, 'Row' ) ; i += 1
        self.dumpSprite()
        self.log('(END) {} {}'.format(self.fmtGeom(), why))

    def dumpTabs(self, why='', dbg=1):
        if dbg: self.log('(BGN) {} {})'.format(self.fmtGeom(), why))
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
                            if   s == 0:  self.dumpLabel(self.tabs[st],   len(self.sprites), i+1, sp, sl, ss, sc, st, sn, sk, why=why)  ;  st += 1  ;  i += 1
                            elif s == 1:  self.dumpLabel(self.notes[sn],  len(self.sprites), i+1, sp, sl, ss, sc, st, sn, sk, why=why)  ;  sn += 1  ;  i += 1
                            elif s == 2:  self.dumpLabel(self.chords[sk], len(self.sprites), i+1, sp, sl, ss, sc, st, sn, sk, why=why)  ;  sk += 1  ;  i += 1
        self.dumpLabel()
        if dbg: self.log('(END) {} {})'.format(self.fmtGeom(), why))

    def dumpLabels(self, why='', dbg=1):
        np, nl, ns, nc, nt = self.n  #;  nc += CCC
        i, sp, sl, ss, sc, st, sn, si, sk = 0, 0, 0, 0, 0, 0, 0, 0, 0
        if dbg: self.log('(BGN) {} {}'.format(self.fmtGeom(), why))
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
                                if   s == 0:  st += 1  ;  self.dumpLabel(self.labels[i], len(self.sprites), i+1, sp, sl, ss, sc, st, sn, si, sk, '{}   Col'.format(why))   ;  i += 1
                                elif s == 1:  sn += 1  ;  self.dumpLabel(self.labels[i], len(self.sprites), i+1, sp, sl, ss, sc, st, sn, si, sk, '{}  Note'.format(why))   ;  i += 1
                                elif s == 2:  sk += 1  ;  self.dumpLabel(self.labels[i], len(self.sprites), i+1, sp, sl, ss, sc, st, sn, sk, si, '{} Chord'.format(why))   ;  i += 1
        else:
            for p in range(np):
                sp += 1                      ;  self.dumpLabel(self.labels[i], len(self.sprites), i+1, sp, sl, ss, sc, st, sn, si, sk, '{}  Page'.format(why))  ;  i += 1
                for l in range(nl):
                    sl += 1                  ;  self.dumpLabel(self.labels[i], len(self.sprites), i+1, sp, sl, ss, sc, st, sn, si, sk, '{}  Line'.format(why))  ;  i += 1
                    for s in range(ns):
                        ss += 1              ;  self.dumpLabel(self.labels[i], len(self.sprites), i+1, sp, sl, ss, sc, st, sn, si, sk, '{}  Sect'.format(why))  ;  i += 1
                        for c in range(nc):
                            sc += 1          ;  self.dumpLabel(self.labels[i], len(self.sprites), i+1, sp, sl, ss, sc, st, sn, si, sk, '{}   Col'.format(why))   ;  i += 1
                            for t in range(nt):
                                if   s == 0:  st += 1  ;  self.dumpLabel(self.labels[i], len(self.sprites), i+1, sp, sl, ss, sc, st, sn, si, sk, '{}   Tab'.format(why))  ;  i += 1
                                elif s == 1:  sn += 1  ;  self.dumpLabel(self.labels[i], len(self.sprites), i+1, sp, sl, ss, sc, st, sn, si, sk, '{}  Note'.format(why))  ;  i += 1
                                elif s == 2:  sk += 1  ;  self.dumpLabel(self.labels[i], len(self.sprites), i+1, sp, sl, ss, sc, st, sn, si, sk, '{} Chord'.format(why))  ;  i += 1
        self.dumpLabel()
        if dbg: self.log('(END) {} {})'.format(self.fmtGeom(), why))
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
        w = self.tabs[0].width if len(self.tabs) else 20
        h = self.tabs[0].height if len(self.tabs) else 18
        m = min(w, h)
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

    def on_key_press(self, symb, mods):
        self.symb, self.mods, self.symbStr, self.modsStr = symb, mods, pygwink.symbol_string(symb), pygwink.modifiers_string(mods)
        self.kbk = self.symbStr  ;  kbk = self.kbk
        self.log('(BGN) {}'.format(self.kpEvntTxt()))
        if                  self.isTab(kbk):                          self.addTab(kbk,  'on_key_press')
        elif kbk == 'B' and self.isCtrl(mods) and self.isShift(mods): self.toggleBlank()
        elif kbk == 'B' and self.isCtrl(mods):                        self.toggleBlank()
        elif kbk == 'E' and self.isCtrl(mods) and self.isShift(mods): self.erase()
        elif kbk == 'E' and self.isCtrl(mods):                        self.erase()
        elif kbk == 'F' and self.isCtrl(mods) and self.isShift(mods): self.toggleFullScreen()
        elif kbk == 'F' and self.isCtrl(mods):                        self.toggleFullScreen()
        elif kbk == 'K' and self.isCtrl(mods) and self.isShift(mods): self.toggleChords()
        elif kbk == 'K' and self.isCtrl(mods):                        self.toggleChords()
        elif kbk == 'L' and self.isCtrl(mods) and self.isShift(mods): self.toggleLLRows()
        elif kbk == 'L' and self.isCtrl(mods):                        self.toggleLLRows()
        elif kbk == 'N' and self.isCtrl(mods) and self.isShift(mods): self.toggleNotes()
        elif kbk == 'N' and self.isCtrl(mods):                        self.toggleNotes()
        elif kbk == 'Q' and self.isCtrl(mods) and self.isShift(mods): self.quit(        'keyPress({})'.format(kbk))
        elif kbk == 'Q' and self.isCtrl(mods):                        self.quit(        'keyPress({})'.format(kbk))
        elif kbk == 'S' and self.isCtrl(mods) and self.isShift(mods): self.writeDataFile()
        elif kbk == 'S' and self.isCtrl(mods):                        self.writeDataFile()
        elif kbk == 'T' and self.isCtrl(mods) and self.isShift(mods): self.toggleTabs()
        elif kbk == 'T' and self.isCtrl(mods):                        self.toggleTabs()
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
            if   motion == pygwink.MOTION_LEFT:          self.move(-self.tpc)
            elif motion == pygwink.MOTION_RIGHT:         self.move( self.tpc)
            elif motion == pygwink.MOTION_UP:            self.move(-1)
            elif motion == pygwink.MOTION_DOWN:          self.move( 1)
            elif motion == pygwink.HOME:                 pass
            elif motion == pygwink.END:                  pass
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
        if dbg: self.log('  p={}   l={}   s={}   c={}   t={}'.format(p, l, s, c, t))
        if dbg: self.log('tpp={} tpl={} tps={} tpc={}'.format(tpp, tpl, tps, tpc))
        if dbg: self.log(' cc={} = ( {} + {} + {} + {} + {} )'.format(cc, p * tpp, l * tpl, s * tps, c * tpc, t))
        lenT = len(self.tabs)   ;   ccm = cc % lenT
        if dbg : self.log('cc = cc % len(tabs) = {} % {} = {}'.format(cc, lenT, ccm))
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

    def move(self, k, dbg=1): #calc
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
    def addTab(self, text, why='', dbg=1):
        self.log('(BGN) {} {} {}'.format(self.kpEvntTxt(), fmtl(self.i, FMTN), why))
        self.updateData(text)
        self.updateTab(text)
        self.updateNote(text)
        if dbg: self.snapshot()
        self.log('(END) {} {} {}'.format(self.kpEvntTxt(), fmtl(self.i, FMTN), why))

    def updateData(self, text, data=None, dbg=0):
        if data is None: data = self.data
        p, l, s, c, r = self.j()
        t = data[p][l][c]
        self.log('(BGN) data[{}][{}][{}]={}'.format(p, l, c, self.data[p][l][c]))
        self.data[p][l][c] = t[0:r] + text + t[r+1:]
        if dbg: self.dumpTabs(why='updateData text={} i={} data[p][l][c]={}'.format(text, self.i, data[p][l][c]))
        self.log('(END) data[{}][{}][{}]={}'.format(p, l, c, self.data[p][l][c]))

    def updateTab(self, text, dbg=0):
        cc = self.cursorCol()
        self.log('(BGN) tabs[{}].text={}'.format(cc, self.tabs[cc].text))
        self.tabs[cc].text = text
        if dbg: self.tabs[cc].color = FONT_COLORS[self.fontColorIndex + 4]
        self.log('(BGN) tabs[{}].text={}'.format(cc, self.tabs[cc].text))

    def updateNote(self, text, dbg=0):
        p, l, s, c, r = self.j()
        cc = self.cursorCol()
        self.log('(BGN) notes[{}].text={}'.format(cc, self.notes[cc].text))
        self.notes[cc].text = self.getNote(r, text).name if self.isFret(text) else self.nblank
        if dbg: self.notes[cc].color = FONT_COLORS[self.fontColorIndex + 4]
        self.log('(END) notes[{}].text={}'.format(cc, self.notes[cc].text))

    def updateCaption(self, txt):
        self.set_caption(txt)
    ####################################################################################################################################################################################################
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
        np, nl, ns, nr, nc = self.n  ;  nc += CCC  ;  i = SNO_C
        for p in range(np):
            for l in range(nl):
                self.data[p][l][SNO_C] = self.stringNumbs
                self.log('p={} l={} c={} data[p][l][c]={}'.format(p, l, SNO_C, self.data[p][l][SNO_C]))
                for r in range(nr):
                    self.tabs[i].text  = self.stringNumbs[r]
                    self.log('({} {} {}) '.format(r, i, self.tabs[i].text), ind=0, end='')
                    i += nc
                self.log(ind=0)

    def setStringNames(self):
        np, nl, ns, nr, nc = self.n  ;  nc += CCC  ;  i = SNA_C
        for p in range(np):
            for l in range(nl):
                self.data[p][l][SNA_C] = self.stringNames
                self.log('p={} l={} c={} data[p][l]={}'.format(p, l, SNA_C, self.data[p][l][SNA_C]))
                for r in range(nr):
                    self.notes[i].text = self.stringNames[r]
                    self.log('({} {} {}) '.format(r, i, self.notes[i].text), ind=0, end='')
                    i += nc
                self.log(ind=0)

    def setCapo(self):
        np, nl, ns, nr, nc = self.n  ;  nc += CCC  ;  i = CFN_C
        for p in range(np):
            for l in range(nl):
                self.data[p][l][CFN_C] = self.stringCapo
                self.log('p={} l={} c={} data[p][l]={}'.format(p, l, CFN_C, self.data[p][l][CFN_C]))
                for r in range(nr):
                    self.tabs[i].text  = self.stringCapo[r]
                    self.notes[i].text = self.stringCapo[r]
                    self.log('({} {} {} {}) '.format(r, i, self.tabs[i].text, self.notes[i].text), ind=0, end='')
                    i += nc
                self.log(ind=0)
    '''
    ####################################################################################################################################################################################################
    @staticmethod
    def isCtrl(mods):        return mods&pygwink.MOD_CTRL
    @staticmethod
    def isShift(mods):       return mods&pygwink.MOD_SHIFT
    @staticmethod
    def isAlt(mods):         return mods&pygwink.MOD_ALT
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
        note = Note(self.getNoteIndex(row, fretNum))
        if dbg: self.log('row={} tab={} fretNum={} note.name={} note.index={}'.format(row, tab, fretNum, note.name, note.index))
        return note

    def getChordName(self, dbg=0):
        name = 'A#mb13'
        if dbg: self.log('chord={}'.format(name))
        return name
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
    def snapshot(self, why='', dbg=0):
        if dbg: self.log('SFX={} SNAP_DIR={} SNAP_SFX={} baseName={} basePath={}'.format(SFX, SNAP_DIR, SNAP_SFX, BASE_NAME, BASE_PATH))
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
        if file != LOG_FILE: Tabs.log(msg, ind)
    ####################################################################################################################################################################################################
    def quit(self, why='', dbg=0):
        self.log('(BGN)')
        self.dumpJ('quit()')
        self.log(QUIT, ind=0)
        self.dumpStruct('quit ' + why)
#        self.snapshot()
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
def testZip():
    a = [1, 2, 3]  ;  b = [4, 5, 6]
    Tabs.log(f'a={a} b={b}', ind=0)
    c = list(zip(a, b))
    Tabs.log(f'c={c}', ind=0)
    d = list(itertools.chain(*c))
    Tabs.log(f'd=flatten(c)={d}', ind=0)
    e = list(zip(*zip(a, b)))
    Tabs.log(f'e={e}', ind=0)
    f = list(zip(*c))
    Tabs.log(f'f={f}', ind=0)
    aa = [1, 2, 3, 4, 5, 6]
    Tabs.log(f'aa={aa}', ind=0)
    bb = [ [ aa[a+b*len(aa)//2] for a in range(len(aa)//2) ] for b in range(len(aa)//3) ]
    Tabs.log(f'bb={bb}', ind=0)
    cc = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    Tabs.log(f'cc={cc}', ind=0)
    dd = [ [ cc[a+b*len(cc)//3] for a in range(len(cc)//3) ] for b in range(len(cc)//3) ]
    Tabs.log(f'dd={dd}', ind=0)
    ee = list(itertools.chain(list(zip(bb[0], ['a', 'b', 'c'], bb[1]))))
    Tabs.log(f'ee={ee}', ind=0)

#self.sects = list(itertools.chain(list(*zip(self.sects, sects))))
#def ufl(z, a, b):pass
def dist(a, b=0, s=1, e=None):
    c = []
    if not e: e = len(a)
    for j in range(b, e, s):
        c.append(j)
    return c

def testPrecedence():
    Tabs.log('? a == 2 or b == 3 and c == 4 ?')
    a = 2  ;  b = 3  ;  c = 4  ;  Tabs.log(f'a={a} b={b} c={c}')
    Tabs.log('True') if a == 2 or b == 3 and c == 4 else Tabs.log('False')
    a = 1  ;  b = 3  ;  c = 4  ;  Tabs.log(f'a={a} b={b} c={c}')
    Tabs.log('True') if a == 2 or b == 3 and c == 4 else Tabs.log('False')
    a = 2  ;  b = 1  ;  c = 4  ;  Tabs.log(f'a={a} b={b} c={c}')
    Tabs.log('True') if a == 2 or b == 3 and c == 4 else Tabs.log('False')
    a = 2  ;  b = 3  ;  c = 5  ;  Tabs.log(f'a={a} b={b} c={c}')
    Tabs.log('True') if a == 2 or b == 3 and c == 4 else Tabs.log('False')
    a = 1  ;  b = 2  ;  c = 3  ;  Tabs.log(f'a={a} b={b} c={c}')
    Tabs.log('True') if a == 2 or b == 3 and c == 4 else Tabs.log('False')

    Tabs.log('? (a == 2 or b == 3) and c == 4 ?')
    a = 2  ;  b = 3  ;  c = 4  ;  Tabs.log(f'a={a} b={b} c={c}')
    Tabs.log('True') if (a == 2 or b == 3) and c == 4 else Tabs.log('False')
    a = 1  ;  b = 3  ;  c = 4  ;  Tabs.log(f'a={a} b={b} c={c}')
    Tabs.log('True') if (a == 2 or b == 3) and c == 4 else Tabs.log('False')
    a = 2  ;  b = 1  ;  c = 4  ;  Tabs.log(f'a={a} b={b} c={c}')
    Tabs.log('True') if (a == 2 or b == 3) and c == 4 else Tabs.log('False')
    a = 2  ;  b = 3  ;  c = 5  ;  Tabs.log(f'a={a} b={b} c={c}')
    Tabs.log('True') if (a == 2 or b == 3) and c == 4 else Tabs.log('False')
    a = 1  ;  b = 2  ;  c = 3  ;  Tabs.log(f'a={a} b={b} c={c}')
    Tabs.log('True') if (a == 2 or b == 3) and c == 4 else Tabs.log('False')
if __name__ == '__main__':
    LOG_PATH = Tabs.getLogPath()
    with open(str(LOG_PATH), 'w') as LOG_FILE:
        Tabs.log('BGN Logging Open LOG_PATH={}'.format(LOG_PATH))
#        testZip()  ;  exit()
        Tabs.log('creating Tabs instance'.format())
        tabsObj     = Tabs()
        Tabs.log('tabs={}'.format(tabsObj))
        Tabs.log('invoking pyglet.app.run()'.format())
        ret = pyglet.app.run()
        Tabs.log('pyglet.app.run() return={}'.format(ret))
#        except(AssertionError, ValueError) as EX:
        Tabs.log('END Logging Close LOG_PATH={}'.format(LOG_PATH))
