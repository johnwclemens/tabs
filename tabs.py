import inspect, math, sys, os, glob, pathlib, string, collections#, shutil#, unicodedata, readline, csv
import pyglet
import pyglet.window.key as pygwink
import pyglet.window.event as pygwine
sys.path.insert(0, os.path.abspath('../lib'))
import cmdArgs

class MyFormatter(string.Formatter):
    def __init__(self, missing='???', badfmt='!!!'):
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
CHECKER_BOARD = 0  ;  EVENT_LOG = 1  ;  FULL_SCREEN = 0  ;  ORDER_GROUP = 1  ;  RESIZE = 1  ;  SEQ_LOG_FILES = 1  ;  SUBPIX = 1
VRSN1            = 0  ;  SFX1 = chr(65 + VRSN1)  ;  QQ      = VRSN1  ;  VRSNX1 = 'VRSN1={}       QQ={}  SFX1={}'.format(VRSN1, QQ,      SFX1)
VRSN2            = 1  ;  SFX2 = chr(49 + VRSN2)  ;  SPRITES = VRSN2  ;  VRSNX2 = 'VRSN2={}  SPRITES={}  SFX2={}'.format(VRSN2, SPRITES, SFX2)
VRSN3            = 0  ;  SFX3 = chr(97 + VRSN3)  ;  ZZ      = VRSN3  ;  VRSNX3 = 'VRSN3={}       ZZ={}  SFX3={}'.format(VRSN3, ZZ,      SFX3)
SFX              = f'.{SFX1}.{SFX2}.{SFX3}'
PATH             = pathlib.Path(sys.argv[0])
BASE_PATH        = PATH.parent
BASE_NAME        = BASE_PATH.stem
SNAP_DIR         = 'snaps'
SNAP_SFX         = '.png'
CCC              = 2
FMTN             = (1, 1, 1, 1, 3, 3) # remove?
P, L, S, R, T, N, I, C = 0, 1, 2, 3, 4, 5, 6, 7
Z, COL_L, LINE_L       = ' ', 'Col', 'Line '
SNO_C, SNA_C, CFN_C    = 0, 0, 1
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
FONT_COLORS_S = [BLUES[6], INDIGOS[0], GRAYS[11], GRAYS[11], GREENS[5], ORANGES[0], VIOLETS[0], PINKS[0], GREEN_BLUES[0], INFRA_REDS[0], ULTRA_VIOLETS[0], BLUE_GREENS[0], REDS[0], CC]
FONT_COLORS_L = [BLUES[0], CYANS[0], REDS[0], YELLOWS[0], GREENS[5], INDIGOS[0], VIOLETS[0], PINKS[0], GREEN_BLUES[0], INFRA_REDS[0], ULTRA_VIOLETS[0], BLUE_GREENS[0], REDS[0], CC]
FONT_COLORS   =  FONT_COLORS_S if SPRITES else FONT_COLORS_L
####################################################################################################################################################################################################
class Note(object):
    NUM_SEMI_TONES = 12
    S_TONES = { 0:'C', 1:'C#', 2:'D', 3:'D#', 4:'E', 5:'F', 6:'F#', 7:'G', 8:'G#', 9:'A', 10:'A#', 11:'B' }
    F_TONES = { 0:'C', 1:'Db', 2:'D', 3:'Eb', 4:'E', 5:'F', 6:'Gb', 7:'G', 8:'Ab', 9:'A', 10:'Bb', 11:'B' }
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
        self.name  = self.F_TONES[i % len(self.F_TONES)]
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
        self.log('CHECKER_BOARD={} EVENT_LOG={} FULL_SCREEN={} ORDER_GROUP={} RESIZE={} SEQ_LOG_FILES={} SUBPIX={}'.format(CHECKER_BOARD, EVENT_LOG, FULL_SCREEN, ORDER_GROUP, RESIZE, SEQ_LOG_FILES, SUBPIX))
        self.log('snapGlobArg={}'.format(snapGlobArg))
        self.log('   snapGlob={}'.format(snapGlob))
        self.delGlob(snapGlob, 'SNAP_GLOB')
        self.T, self.N, self.I, self.C = 1, 1, 0, 0
        self.ww, self.hh  = 640, 480
        self.s = [self.T, self.N, self.I, self.C]  ;  self.ss = sum(self.s)  ;  self.log('s={} ss={}'.format(self.s, self.ss))
        self.n, self.i, self.x, self.y, self.w, self.h, self.g = [1, 3, self.ss, 6, 20], [1, 1, 1, 1, 1], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], []
        self.argMap = cmdArgs.parseCmdLine(dbg=1)
        if 'N' in self.argMap and len(self.argMap['N']) == 0: self.N            = 1
        if 'n' in self.argMap and len(self.argMap['n'])  > 0: self.n            = [int(self.argMap['n'][i]) for i in range(len(self.argMap['n']))]
        if 'i' in self.argMap and len(self.argMap['i'])  > 0: self.i            = [int(self.argMap['i'][i]) for i in range(len(self.argMap['i']))]
        if 'x' in self.argMap and len(self.argMap['x'])  > 0: self.x            = [int(self.argMap['x'][i]) for i in range(len(self.argMap['x']))]
        if 'y' in self.argMap and len(self.argMap['y'])  > 0: self.y            = [int(self.argMap['y'][i]) for i in range(len(self.argMap['y']))]
        if 'w' in self.argMap and len(self.argMap['w'])  > 0: self.ww           =  int(self.argMap['w'][0])
        if 'h' in self.argMap and len(self.argMap['h'])  > 0: self.hh           =  int(self.argMap['h'][0])
        if 'f' in self.argMap and len(self.argMap['f']) == 0: FULL_SCREEN       = 1
        if 'g' in self.argMap and len(self.argMap['g']) == 0: ORDER_GROUP       = 1
        if 's' in self.argMap and len(self.argMap['s']) == 0: SUBPIX            = 1
        self.log('[N]            N={}'.format(self.N))
        self.log('[n]            n={}'.format(fmtl(self.n, FMTN)))
        self.log('[i]            i={}'.format(fmtl(self.i, FMTN)))
        self.log('[x]            x={}'.format(fmtl(self.x, FMTN)))
        self.log('[y]            y={}'.format(fmtl(self.y, FMTN)))
        self.log('[w]           ww={}'.format(self.ww))
        self.log('[h]           hh={}'.format(self.hh))
        self.log('[f]  FULL_SCREEN={}'.format(FULL_SCREEN))
        self.log('[g]  ORDER_GROUP={}'.format(ORDER_GROUP))
        self.log('[s]       SUBPIX={}'.format(SUBPIX))
        self.stringMap   = collections.OrderedDict([('E2', 28), ('A2', 33), ('D3', 38), ('G3', 43), ('B3', 47), ('E4', 52)])
        self.stringKeys  = list(self.stringMap.keys())
        self.stringNames = ''.join(reversed([str(k[0]) for k in self.stringKeys]))
        self.stringNumbs = ''.join([str(r+1)  for r in range(self.n[R])])
        self.stringCapo  = ''.join(['0' for _ in range(self.n[R])])
        self.log('stringMap   = {}'.     format(fmtd(self.stringMap)))
        self.log('stringKeys  = {} = {}'.format(fmtl(self.stringKeys),  self.stringKeys))
        self.log('stringNames = {} = {}'.format(fmtl(self.stringNames), self.stringNames))
        self.log('stringNumbs = {} = {}'.format(fmtl(self.stringNumbs), self.stringNumbs))
        self.log('stringCapo  = {} = {}'.format(fmtl(self.stringCapo), self.stringCapo))
        self.fontBold, self.fontItalic, self.fontColorIndex, self.fontDpiIndex, self.fontSize, self.fontNameIndex = 0, 0, 0, 4, 14, 0
        self.dumpFont()
        self._initWindowA()
        super().__init__(screen=self.screens[1], fullscreen=FULL_SCREEN, resizable=True, visible=False)
        self._initWindowB()
        self.data    = []
        self.kbk, self.symb, self.mods, self.symbStr, self.modsStr = 0, 0, 0, '', ''
        self.cc, self.ci, self.SNAP0, self.armSnap, self.tblankCol  = 0, 0, 0, '', ''  ;  self.nblankCol = ''
        self.tblanki, self.tblanks  = 1, [' ', '-']   ;   self.tblank = self.tblanks[self.tblanki]
        self.nblanki, self.nblanks  = 1, [' ', '-']   ;   self.nblank = self.nblanks[self.nblanki]
        self.cursor, self.caret   = None, None
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

    def cpz(self): return self.cpp, self.cpl, self.cps, self.cpr
    def lnl(self): return list(map(len, [self.pages, self.lines, self.sects, self.rows, self.tabs, self.notes]))
    def snl(self): return sum(self.lnl())
    def j(self):   return [i-1 if i else 0 for i in self.i]

    @staticmethod
    def fmtDataDim(d): return '({} x {} x {} x {})'.format(len(d), len(d[0]), len(d[0][0]), len(d[0][0][0]))
    def fmtGeom(self): return '{} {} {} {} {}'.format(fmtl(self.n, FMTN), fmtl(self.lnl()), self.snl(), self.cc, fmtl(self.i, FMTN))
    def ordDict(self, od): self.log('{}'.format(od.items()))
    ####################################################################################################################################################################################################
    def _init(self, dbg=1):
        dataDir  = 'data'  ;  dataSfx = '.dat'  ;  dataPfx = '.{}'.format(self.n[T])
        dataName = BASE_NAME + SFX + dataPfx + dataSfx
        self.dataPath = BASE_PATH / dataDir / dataName
        self.pages,  self.lines,   self.sects, self.rows,  self.tabs  = [], [], [], [], []
        self.labels, self.sprites, self.ucols, self.notes = [], [], [], []
        self.log('(BGN) {}'.format(self.fmtGeom()))
        self.kc  = [GRAYS[7], GRAYS[11]] if CHECKER_BOARD else [GRAYS[7]]  ;  self.kn = [GREENS[1], GREENS[4]] if CHECKER_BOARD else [GREENS[1]]
#        kb = [self.kc[0]]  ;  self.kp  = kb  ;  self.kl = kb  ;  self.ks = kb  ;  self.kq = kb  ;  self.kr = kb
        self.ssi = 0
        self._initCps()
        self.readTabs()
        if QQ:
            self.labelTextA, self.labelTextB = ['R', 'M'], ['R', 'M']
            self.labelTextA.extend('{}'.format(j) for j in range(1, self.n[T] + 1))
            self.labelTextB.extend('{}'.format(j % 10 if j % 10 else j // 10 % 10) for j in range(1, self.n[T] + 1))
            texts = list(zip(self.labelTextA, self.labelTextB))
            self.dumpLabelText(texts)
        self.createSprites() if SPRITES else  self.createLabels()
        self.createCursor(self.g[T + 3])
        if dbg: self.dumpStruct('_init')
        self.log('(END) {}'.format(self.fmtGeom()))
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
#        self.dumpTabs(why)
#        self.dumpACols(why)
        self.dumpFont(why)
        u, lab, spr  = list(map(len, [self.ucols, self.labels, self.sprites]))
        self.log('len() u={} lab={} spr={}'.format(u, lab, spr))
        self.log('(END) {}'.format(why))
    ####################################################################################################################################################################################################
    def writeTabs(self):
        self.log('(BGN) {}'.format(self.fmtDataDim(self.data)))
        data = self.transpose(self.data)
        with open(str(self.dataPath), 'w') as DATA_FILE:
            np, nl, ns, nr, nc = self.n  ;  nc += CCC
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
    def readTabs(self, dbg=1):
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
                    self.log('read    {:2}{} line with {:6,} cols on {:4,} strings {:8,} tabs'.format(l, self.ordSfx(l), c, r, c*r))
                    if l == nl: break
                    r = 0
                    l += 1
                if c:  self.log('l={} r={} c={}: {}'.format(l, r, c, s))
            self.data.append(lines)
        nt   = l * c * r
        self.tblankCol = self.tblank * r
        vert = self.isVert()
        self.log('read     {:2} lines with {:6,} cols on {:4,} strings {:8,} tabs, vdf={} blankCol({})={}'.format(l, l*c, l*r, nt, vert, len(self.tblankCol), self.tblankCol))
        if dbg: self.dumpTabsHorz()
        self.data = self.transpose()
        vert      = self.isVert()
        if dbg: self.dumpTabsVert()
        self.log('assert: size=nt+2*(l*r+l-1) {:8,} + {} = {:8,} bytes'.format(nt, 2 * (l * r + l - 1), size))  ;  assert size == nt + 2 * (l * r + l - 1)  ;  assert vert
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
#        self.dumpTabsVert(data, lc, ll, i) if self.isVert(data) else self.dumpTabsHorz(data, lc, ll, i)
#        transpose = self.transpose(data, why='Internal')
#        self.dumpTabsVert(transpose, lc, ll, i) if self.isVer(transpose) else self.dumpTabsHorz(transpose, lc, ll, i)
#        self.log('(END) {}'.format(why))

    def dumpTabsHorz(self, data=None, lc=1, ll=1, i=0):
        if data is None: data = self.data
        self.log('(BGN) lc={} ll={} i={} {}'.format(lc, ll, i, self.fmtDataDim(data)))
        for p in range(len(data)):
            for l in range(len(data[p])):
                if ll:  llt = 'Line {}'.format(l + 1)  ;  llab = '{:{}}'.format(llt, i + 1)  ;  self.log('{}{}'.format(Z * i, llab), ind=0)
                if lc:  self.dumpTabLabels(data[p][l], i=i, sep=Z)
                for r in range(len(data[p][l])):
                    self.log('{}'.format(Z * i), ind=0, end='')
                    for c in range(len(data[p][l][r])):
                        self.log('{}'.format(data[p][l][r][c]), ind=0, end='')
                    self.log(ind=0)
                self.log(ind=0)
        self.log('(END) lc={} ll={} i={} {}'.format(lc, ll, i, self.fmtDataDim(data)))

    def dumpTabsVert(self, data=None, lc=1, ll=1, i=0):
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
    def dumpTabLabels(self, data=None, i=0, sep='%'):
        if data is None: data = self.data
        n = len(data[0])-CCC    ;  a = ' ' * i if i else ''   ;  b = sep * n  ;  p = '  '  ;  q = ' @'  ;  r = sep * 3
        if n >= 100:      self.log('{}{}'.format(a, p), ind=0, end='')  ;  [  self.log('{}'.format(c//100   if c>=100 else ' '), ind=0, end='') for c in range(1, n+1) ]  ;  self.log(ind=0)
        if n >= 10:       self.log('{}{}'.format(a, p), ind=0, end='')  ;  [  self.log('{}'.format(c//10%10 if c>=10  else ' '), ind=0, end='') for c in range(1, n+1) ]  ;  self.log(ind=0)
        self.log(                  '{}{}'.format(a, q), ind=0, end='')  ;  [  self.log('{}'.format(c%10),                        ind=0, end='') for c in range(1, n+1) ]  ;  self.log(ind=0)
        if sep != '':   self.log('{}{}{}'.format(a, r, b), ind=0)

    def transpose(self, data=None, why=' External  ', dbg=1):
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
    def geom_OLD(self, p=None, j=0, s=0, init=0, dbg=1):
        mx, my = None, None
        n, i, x, y, w, h, g = self.n[j], self.i[j], self.x[j], self.y[j], self.w[j], self.h[j], self.g[j]
        if   j == R and not s: n += QQ
        elif j == T:           n += CCC
        if not p:      w, h =  self.ww - x*2, self.hh - y*2
        elif j == T:   w, h = (p.width - x*(n + 1))/n,  p.height - y*2
        else:          w, h =  p.width - x*2,          (p.height - y*(n + 1))/n
        if j != T:     x += p.x if p else self.x[P]
        if init:       self.w[j], self.h[j] = w, h
        else:          mx, my = w/self.w[j], h/self.h[j]
        if dbg:        self.dumpGeom(j, n, i, x, y, w, h, mx, my, init)
        return n, i, x, y, w, h, g, mx, my
    ####################################################################################################################################################################################################
    def geom(self, p=None, j=0, s=0, init=0, dbg=1):
        mx, my = None, None
        n, i, x, y, w, h, g = self.n[j], self.i[j], self.x[j], self.y[j], self.w[j], self.h[j], self.g[j]
        if   j == T:           n += CCC
        if not p:              w =  self.ww - x*2           ;  h =  self.hh - y*2
        elif j == T:           w = (p.width - x*(n + 1))/n  ;  h =  p.height - y*2
        else:                  w =  p.width - x*2           ;  h = (p.height - y*(n + 1))/n
        if SPRITES:
            if j == T:         x += w/2                     ;  y += p.y + p.height/2
            elif p:                                            y += p.y + p.height
        else:
            if not p:          x += w/2                     ;  y += h/2
            elif j == T:       x -= w/2                     ;  y += p.y - h/2 + p.height/2
            else:              x += w/2                     ;  y += p.y + h/2 + p.height/2
        if init:               self.w[j] = w                ;  self.h[j] = h
        else:                  mx = w/self.w[j]             ;  my = h/self.h[j]
        if dbg:                self.dumpGeom(j, n, i, x, y, w, h, mx, my, init)
        return n, i, x, y, w, h, g, mx, my
    def dumpGeom(self, j, n, i, x, y, w, h, mx, my, init):
        iz = fmtl(self.lnl(), FMTN) if init else fmtl(self.i, FMTN)
        self.log(ind=0)
        self.log(FMTR.format('j={} n={:3} i={:4} x={:5.1f} y={:5.1f} w={:7.2f} h={:7.2f} mx={:5.3f} my={:5.3f} {}', j, n, i, x, y, w, h, mx, my, iz))
    ####################################################################################################################################################################################################
    def createLabels(self, dbg=1, dbg2=1):
        self.log('(BGN) {}'.format(self.fmtGeom()))
        np, ip, xp, yp, wp, hp, gp, mx, my = self.geom(None, P, init=1, dbg=dbg2)
        if dbg: self.dumpLabel()
        for p in range(np):
            page = self.createLabel('Page', self.pages, xp, yp, wp, hp, P, gp, why='create Page', dbg=dbg)
            nl, il, xl, yl, wl, hl, gl, mx, my = self.geom(page, L, init=1, dbg=dbg2)
            for l in range(nl):
                yl2 = yl - hl*(l + 1)  ;              line = self.createLabel('Line', self.lines, xl, yl2, wl, hl, L, gl, why='create Line', dbg=dbg)
                ns, iz, xs, ys, ws, hs, gs, mx, my = self.geom(line, S, init=1, dbg=dbg2)
                for s in range(ns):
                    ys2 = ys - hs*(s + 1)  ;          sect = self.createLabel('Sect', self.sects, xs, ys2, ws, hs, S, gs, why='create Sect', dbg=dbg)
                    nr, ir, xr, yr, wr, hr, gr, mx, my = self.geom(sect, R, s=s, init=1, dbg=dbg2)
                    for r in range(nr):
                        yr2 = yr - hr*(r + 1)  ;       row = self.createLabel( 'Row', self.rows,  xr, yr2, wr, hr, R, gr, why= 'create Row', dbg=dbg)
                        nc, ic, xc, yc, wc, hc, gc, mx, my = self.geom(row, T, init=1, dbg=dbg2)
                        for c in range(nc):
                            xc2 = xc + wc*(c + 1)
                            if   s == 0:
                                if QQ and r == 0: cc = -T  ;  tab = self.labelTextB[c]        ;  tabs = self.ucols
                                elif c == SNO_C:  cc = -T  ;  tab = self.stringNumbs[r-QQ]    ;  tabs = self.tabs
                                elif c == CFN_C:  cc = -T  ;  tab = self.stringCapo[r-QQ]     ;  tabs = self.tabs
                                else:             cc =  T  ;  tab = self.data[p][l][c][r-QQ]  ;  tabs = self.tabs
                                self.createLabel(tab, tabs, xc2, yc, wc, hc, cc, gc, why='create Tab', dbg=dbg)
                            elif s == 1:
                                if   c == SNA_C:  cc = -N  ;  note = self.stringNames[r]
                                elif c == CFN_C:  cc = -N  ;  note = self.stringCapo[r]
                                else:             cc =  N  ;  tab = self.data[p][l][c][r]  ;  note = self.getNote(r, tab).name if self.isFret(tab) else self.nblank
                                self.createLabel(note, self.notes, xc2, yc, wc, hc, cc, gc, why='create Note', dbg=dbg)
        if dbg: self.dumpLabel()
        self.log('(END) {}'.format(self.fmtGeom()))
    def createLabels_OLD(self, dbg=1, dbg2=0):
        self.log('(BGN) {}'.format(self.fmtGeom()))
        np, ip, xp, yp, wp, hp, gp, mx, my = self.geom(None, P, init=1, dbg=dbg2)
        if dbg: self.dumpLabel()
        for p in range(np):
            xp2 = xp + wp/2      ;      yp2 = yp + hp/2
            page = self.createLabel('Page', self.pages, xp2, yp2, wp, hp, P, gp, why='create Page', dbg=dbg)
            nl, il, xl, yl, wl, hl, gl, mx, my = self.geom(page, L, init=1, dbg=dbg2)
            for l in range(nl):
                yl2 = page.y + page.height/2 - (yl + hl)*(l + 1) + hl/2
                line = self.createLabel('Line', self.lines, xl, yl2, wl, hl, L, gl, why='create Line', dbg=dbg)
                ns, iz, xs, ys, ws, hs, gs, mx, my = self.geom(line, S, init=1, dbg=dbg2)
                for s in range(ns):
                    ys2 = line.y + line.height/2 - (ys + hs)*(s + 1) + hs/2
                    sect = self.createLabel('Sect', self.sects, xs, ys2, ws, hs, S, gs, why='create Sect', dbg=dbg)
                    nr, ir, xr, yr, wr, hr, gr, mx, my = self.geom(sect, R, s=s, init=1, dbg=dbg2)
                    for r in range(nr):
                        yr2 = sect.y + sect.height/2 - (yr + hr)*(r + 1) + hr/2
                        row = self.createLabel('Row', self.rows, xr, yr2, wr, hr, R, gr, why='create Row', dbg=dbg)
                        nc, ic, xc, yc, wc, hc, gc, mx, my = self.geom(row, T, init=1, dbg=dbg2)
                        for c in range(nc):
                            xc2 = row.x - row.width/2 + (xc + wc)*c + wc/2   ;  yc2 = row.y + row.height - (yc + hc)
                            if   s == 0:
                                if QQ and r == 0: cc = -T  ;  tab = self.labelTextB[c]        ;  tabs = self.ucols
                                elif c == SNO_C:  cc = -T  ;  tab = self.stringNumbs[r-QQ]    ;  tabs = self.tabs
                                elif c == CFN_C:  cc = -T  ;  tab = self.stringCapo[r-QQ]     ;  tabs = self.tabs
                                else:             cc =  T  ;  tab = self.data[p][l][c][r-QQ]  ;  tabs = self.tabs
                                self.createLabel(tab, tabs, xc2, yc2, wc, hc, cc, gc, why='create Tab', dbg=dbg)
                            elif s == 1:
                                if   c == SNA_C: cc = -N  ;  note = self.stringNames[r]
                                elif c == CFN_C: cc = -N  ;  note = self.stringCapo[r]
                                else:            cc = N   ;  tab = self.data[p][l][c][r]  ;  note = self.getNote(r, tab).name if self.isFret(tab) else self.nblank
                                self.createLabel(note, self.notes, xc2, yc2, wc, hc, cc, gc, why='create Note', dbg=dbg)
        if dbg: self.dumpLabel()
        self.log('(END) {}'.format(self.fmtGeom()))

    def createSprites(self, dbg=1, dbg2=1):
        self.log('(BGN) {}'.format(self.fmtGeom()))
        np, ip, xp, yp, wp, hp, gp, mx, my = self.geom(None, P, init=1, dbg=dbg2)
        if dbg: self.dumpSprite()
        for p in range(np):
            v = not p
            page = self.createSprite(self.pages, xp, yp, wp, hp, P, gp, why='create Page', v=v, dbg=dbg)
            nl, il, xl, yl, wl, hl, gl, mx, my = self.geom(page, L, init=1, dbg=dbg2)
            for l in range(nl):
                yl2 = yl - hl*(l + 1)
#                yl2 = page.y + page.height - (yl + hl)*(l + 1)
                line = self.createSprite(self.lines, xl, yl2, wl, hl, L, gl, why='create Line', v=v, dbg=dbg)
                ns, iz, xs, ys, ws, hs, gs, mx, my = self.geom(line, S, init=1, dbg=dbg2)
                for s in range(ns):
                    ys2 = ys - hs*(s + 1)
#                    ys2 = line.y + line.height - (ys + hs)*(s + 1)
                    sect = self.createSprite(self.sects, xs, ys2, ws, hs, S, gs, why='create Sect', v=v, dbg=dbg)
                    nr, ir, xr, yr, wr, hr, gr, mx, my = self.geom(sect, R, s=s, init=1, dbg=dbg2)
                    for r in range(nr):
                        yr2 = yr - hr*(r + 1)
#                        yr2 = sect.y + sect.height - (yr + hr)*(r + 1)
                        row = self.createSprite(self.rows, xr, yr2, wr, hr, R, gr, why='create Row',  v=v, dbg=dbg)
                        nc, ic, xc, yc, wc, hc, gc, mx, my = self.geom(row, T, init=1, dbg=dbg2)
                        if dbg: self.dumpSprite()          ;  self.dumpLabel()
                        for c in range(nc):
                            xc2 = xc + wc*c         # ;   wc2 = wc - wc/10  ;  hc2 = hc - hc/10
#                            xc2 = row.x + (xc + wc)*(c + 1) - wc/2   ;  yc2 = yc + row.y + row.height - hc/2
                            if   s == 0:
                                if QQ and r == 0: cc = -T  ;  tab = self.labelTextB[c]        ;  tabs = self.ucols
                                elif c == SNO_C:  cc = -T  ;  tab = self.stringNumbs[r-QQ]    ;  tabs = self.tabs
                                elif c == CFN_C:  cc = -T  ;  tab = self.stringCapo[r-QQ]     ;  tabs = self.tabs
                                else:             cc =  T  ;  tab = self.data[p][l][c][r-QQ]  ;  tabs = self.tabs
                                self.createLabel(tab, tabs, xc2, yc, wc, hc, cc, gc, why='create Tab', dbg=dbg)
                            elif s == 1:
                                if   c == SNA_C: cc = -N  ;  note = self.stringNames[r]
                                elif c == CFN_C: cc = -N  ;  note = self.stringCapo[r]
                                else:            cc = N   ;  tab = self.data[p][l][c][r]  ;  note = self.getNote(r, tab).name if self.isFret(tab) else self.nblank
                                self.createLabel(note, self.notes, xc2, yc, wc, hc, cc, gc, why='create Note', dbg=dbg)
                        if dbg: self.dumpLabel()  ;  self.dumpSprite()
        self.log('(END) {}'.format(self.fmtGeom()))

    ####################################################################################################################################################################################################
    def createSprite(self, p, x, y, w, h, kk, g, why, v=0, dbg=0):
        o, k, d, j, n, s = self.fontParams()
        k = FONT_COLORS[k + kk]
        scip = pyglet.image.SolidColorImagePattern(k)
        img = scip.create_image(width=fri(w), height=fri(h))
        s = pyglet.sprite.Sprite(img, x, y, batch=self.batch, group=g, subpixel=SUBPIX)
        s.visible = v
        s.color, s.opacity = k[:3], k[3]
        self.sprites.append(s)
        if p is not None:      p.append(s)
        if dbg: self.dumpSprite(s, len(self.sprites), *self.lnl(), why)
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
        if dbg: self.dumpLabel(ll, len(self.labels), *self.lnl(), why=why)
        return ll
    ####################################################################################################################################################################################################
    def resizeSprites(self, dbg=1):
        self.log('(BGN) {}'.format(self.fmtGeom()))
        if dbg: self.dumpSprite()
        i, j, sp, sl, ss, sr, sc, sn, su = 0, 0, 0, 0, 0, 0, 0, 0, 0
        np, ip, xp, yp, wp, hp, gp, mxp, myp = self.geom(None, P, dbg=dbg)
        for p in range(np):
            page = self.pages[sp]                                                                 ;  page.update(x=xp, y=yp, scale_x=mxp, scale_y=myp)  ;  sp += 1  ;  i += 1
            if dbg: self.dumpSprite(self.sprites[i-1], i, sp, ss, sl, sr, sc, sn, 'resize Page')
            nl, il, xl, yl, wl, hl, gl, mxl, myl = self.geom(page, L, dbg=dbg)
            for l in range (nl):
                line = self.lines[sl]          ;  yl2 = yl - hl*(l + 1)  ;  line.update(x=xl, y=yl2, scale_x=mxl, scale_y=myl)  ;  sl += 1  ;  i += 1
#                line = self.lines[sl]          ;  yl2 = page.y + page.height - (yl + hl)*(l + 1)  ;  line.update(x=xl, y=yl2, scale_x=mxl, scale_y=myl)  ;  sl += 1  ;  i += 1
                if dbg: self.dumpSprite(self.sprites[i-1], i, sp, sl, ss, sr, sc, sn, 'resize Line')
                ns, iz, xs, ys, ws, hs, gs, mxs, mys = self.geom(line, S, dbg=dbg)
                for s in range(ns):
                    sect = self.sects[ss]      ;  ys2 = ys - hs*(s + 1)  ;  sect.update(x=xs, y=ys2, scale_x=mxs, scale_y=mys)  ;  ss += 1  ;  i += 1
#                    sect = self.sects[ss]      ;  ys2 = line.y + line.height - (ys + hs)*(s + 1)  ;  sect.update(x=xs, y=ys2, scale_x=mxs, scale_y=mys)  ;  ss += 1  ;  i += 1
                    if dbg: self.dumpSprite(self.sprites[i-1], i, sp, sl, ss, sr, sc, sn, 'resize Sect')
                    nr, ir, xr, yr, wr, hr, gr, mxr, myr = self.geom(sect, R, s=s, dbg=dbg)
                    for r in range(nr):
                        row = self.rows[sr]     ;  yr2 = yr - hr*(r + 1)
#                        row = self.rows[sr]     ;  yr2 = sect.y + sect.height - (yr + hr)*(r + 1)
                        row.update(x=xr, y=yr2, scale_x=mxr, scale_y=myr)
                        sr += 1  ;  i += 1
                        if dbg: self.dumpSprite(self.sprites[i-1], i, sp, sl, ss, sr, sc, sn, 'resize Row')
                        nc, ic, xc, yc, wc, hc, gc, mxc, myc = self.geom(row, T, dbg=dbg)
                        for c in range(nc):
                            if s == 0:
                                if QQ and r == 0: cols = self.ucols[su]  ;  su += 1
                                else:             cols = self.tabs[sc]   ;  sc += 1
                                col = cols  ;  col.width = wc  ;  col.height = hc  ;  col.x = xc + wc*c  ;  col.y = yc  ;  j += 1
#                                col = cols  ;  col.width = wc  ;  col.height = hc  ;  col.x = row.x + (xc + wc)*c + xc + wc/2  ;  col.y = row.y + row.height - yc - hc/2  ;  j += 1
                                if dbg: self.dumpLabel(col, j, sp, sl, ss, sr, sc, sn, 'resize Tab')
                            elif s == 1:
                                note = self.notes[sn]
                                note.width = wc  ;  note.height = hc  ;  note.x = xc + wc*c  ;  note.y = yc  ;  sn += 1  ;  j += 1
#                                note.width = wc  ;  note.height = hc  ;  note.x = row.x + (xc + wc)*(c + 1) - wc/2  ;  note.y = row.y + row.height - yc - hc/2  ;  sn += 1  ;  j += 1
                                if dbg: self.dumpLabel(note, j, sp, sl, ss, sr, sc, sn, 'resize Note')
        if dbg: self.dumpSprite()
        self.log('(END) {}'.format(self.fmtGeom()))

    def resizeLabels(self, dbg=1):
        self.log('(BGN) {}'.format(self.fmtGeom()))
        i, sp, sl, sr, ss, sc, sn, su = 0, 0, 0, 0, 0, 0, 0, 0
        np, ip, xp, yp, wp, hp, gp, mxp, myp = self.geom(None, P, dbg=dbg)
        for p in range(np):
            page = self.pages[sp];                page.width = wp  ;  page.height = hp  ;  page.x = xp + wp/2  ;  page.y = yp + hp/2  ;  sp += 1  ;  i += 1
            if dbg: self.dumpLabel(page, i, sp, sl, ss, sr, sc, sn, 'resize Page')
            nl, il, xl, yl, wl, hl, gl, mxl, myl = self.geom(page, L, dbg=dbg)
            for l in range(nl):
#                yl2 = yl - hl*(l + 1)  ;              line = self.createLabel('Line', self.lines, xl, yl2, wl, hl, L, gl, why='create Line', dbg=dbg)
                line = self.lines[sl];            line.width = wl  ;  line.height = hl  ;  line.x = xl  ;  line.y = yl - hl*(l + 1)  ;  line.y -= page.height/2;  sl += 1  ;  i += 1
#                line = self.lines[sl];            line.width = wl  ;  line.height = hl  ;  line.x = xl  ;  line.y = page.y + page.height/2 - (yl + hl)*(l + 1) + hl/2  ;  sl += 1  ;  i += 1
                if dbg: self.dumpLabel(line, i, sp, sl, ss, sr, sc, sn, 'resize Line')
                ns, iz, xs, ys, ws, hs, gs, mxs, mys = self.geom(line, S, dbg=dbg)
                for s in range(ns):
                    sect = self.sects[ss];        sect.width = ws  ;  sect.height = hs  ;  sect.x = xs  ;  sect.y = ys - hs*(s + 1)  ;  ss += 1  ;  i += 1
#                    sect = self.sects[ss];        sect.width = ws  ;  sect.height = hs  ;  sect.x = xs  ;  sect.y = line.y + line.height/2 - (ys + hs)*(s + 1) + hs/2  ;  ss += 1  ;  i += 1
                    if dbg: self.dumpLabel(sect, i, sp, sl, ss, sr, sc, sn, 'resize Sect')
                    nr, ir, xr, yr, wr, hr, gr, mxr, myr = self.geom(sect, R, s=s, dbg=dbg)
                    for r in range(nr):
                        row = self.rows[sr];       row.width = wr  ;   row.height = hr  ;   row.x = xr  ;   row.y = yr - hr*(r + 1)  ;  sr += 1  ;  i += 1
#                        row = self.rows[sr];       row.width = wr  ;   row.height = hr  ;   row.x = xr  ;   row.y = sect.y + sect.height/2 - (yr + hr)*(r + 1) + hr/2  ;  sr += 1  ;  i += 1
                        if dbg: self.dumpLabel(row, i, sp, sl, ss, sr, sc, sn, 'resize Row')
                        nc, ic, xc, yc, wc, hc, gc, mxc, myc = self.geom(row, T, dbg=dbg)
                        for c in range(nc):
                            if s == 0:
                                if QQ and r == 0: col = self.ucols[su]  ;  su += 1
                                else:             col = self.tabs[sc]   ;  sc += 1
#                                xc2 = xc + wc*(c + 1)
                                col.width = wc  ;   col.height = hc  ;   col.x = xc + wc*(c + 1)  ;  col.y = yc  ;  i += 1
#                                col.width = wc  ;   col.height = hc  ;   col.x = row.x - row.width/2 + (xc + wc)*c + wc/2  ;  col.y = row.y + row.height - (yc + hc)  ;  i += 1
                                if dbg: self.dumpLabel(col, i, sp, sl, ss, sr, sc, sn, 'resize Tab')
                            elif s == 1:
                                note = self.notes[sn]
                                note.width = wc  ;  note.height = hc  ;  note.x = xc + wc*(c + 1)  ;  note.y = yc  ;  sn += 1  ;  i += 1
#                                note.width = wc  ;  note.height = hc  ;  note.x = row.x - row.width/2 + (xc + wc)*c + wc/2  ;  note.y = row.y + row.height - (yc + hc)  ;  sn += 1  ;  i += 1
                                if dbg: self.dumpLabel(note, i, sp, sl, ss, sr, sc, sn, 'resize Note')
        if dbg: self.dumpLabels('resize')
        self.log('(END) {}'.format(self.fmtGeom()))
    ####################################################################################################################################################################################################
    def dumpSprites(self, why=''):
        self.log('(BGN) {} {}'.format(self.fmtGeom(), why))
        np, nl, ns, nr, nc = self.n
        self.dumpSprite()
        i, sp, sl, ss, sr, sc, sn, su = 0, 0, 0, 0, 0, 0, 0, 0
        for p in range(np):
            sp += 1                 ; self.dumpSprite(self.sprites[i], i+1, sp, sl, ss, sr, sc, sn, 'Page') ; i += 1
            for l in range(nl):
                sl += 1             ; self.dumpSprite(self.sprites[i], i+1, sp, sl, ss, sr, sc, sn, 'Line') ; i += 1
                for s in range(ns):
                    ss += 1         ; self.dumpSprite(self.sprites[i], i+1, sp, sl, ss, sr, sc, sn, 'Sect') ; i += 1
                    for r in range(nr):
                        sr += 1     ; self.dumpSprite(self.sprites[i], i+1, sp, sl, ss, sr, sc, sn, 'Row' ) ; i += 1
        self.dumpSprite()
        self.log('(END) {} {}'.format(self.fmtGeom(), why))

    def dumpUCols(self, why='', dbg=1):
        if dbg: self.log('(BGN) {} {})'.format(self.fmtGeom(), why))
        np, nl, ns, nr, nc = self.n  ;  nc += CCC
        nu = QQ * nc
        i, sp, sl, ss, sr, sc, su = 0, 0, 0, 0, 0, 0, 0
        self.dumpLabel(idt='uid')
        for p in range(np):
            sp += 1
            for l in range(nl):
                sl += 1
                for s in range(ns):
                    ss += 1
                    for u in range(nu):
                        if s == 0:
                            su += 1  ;  self.dumpLabel(self.ucols[i], i+1, sp, sl, ss, sr, su, why=why)  ;  i += 1
        self.dumpLabel(idt='uid')
        if dbg: self.log('(END) {} {})'.format(self.fmtGeom(), why))

    def dumpTabs(self, why='', dbg=1):
        if dbg: self.log('(BGN) {} {})'.format(self.fmtGeom(), why))
        np, nl, ns, nr, nc = self.n  ;  nc += CCC
        i, sp, sl, ss, sr, sc, su = 0, 0, 0, 0, 0, 0, 0
        self.dumpLabel(idt='cid')
        for p in range(np):
            sp += 1
            for l in range(nl):
                sl += 1
                for s in range(ns):
                    ss += 1
                    for r in range(nr):
                        sr += 1
                        for c in range(nc):
                            if s == 0:
                                sc += 1  ;  self.dumpLabel(self.tabs[i],  i+1, sp, sl, ss, sr, c+1, why=why)  ;  i += 1
        self.dumpLabel(idt='cid')
        if dbg: self.log('(END) {} {})'.format(self.fmtGeom(), why))

    def dumpLabels(self, why='', dbg=1):
        np, nl, ns, nr, nc = self.n  ;  nc += CCC
        i, sp, sl, ss, sr, su, sc, sn = 0, 0, 0, 0, 0, 0, 0, 0
        if dbg: self.log('(BGN) {} {}'.format(self.fmtGeom(), why))
        self.dumpLabel()
        if SPRITES:
            for p in range(np):
                sp += 1
                for l in range(nl):
                    sl += 1
                    for s in range(ns):
                        ss += 1
                        for r in range(nr):
                            sr += 1
                            for c in range(nc):
                                if s == 0:
                                    if QQ and r == 0: su += 1
                                    else:             sc += 1
                                    self.dumpLabel(self.labels[i], i+1, sp, sl, ss, sr, sc, sn, '{} Col'.format(why))   ;  i += 1
        else:
            for p in range(np):
                sp += 1           ; self.dumpLabel(self.labels[i], i+1, sp, sl, ss, sr, sc, sn, '{} Page'.format(why))  ;  i += 1
                for l in range(nl):
                    sl += 1       ; self.dumpLabel(self.labels[i], i+1, sp, sl, ss, sr, sc, sn, '{} Line'.format(why))  ;  i += 1
                    for s in range(ns):
                        ss += 1   ; self.dumpLabel(self.labels[i], i+1, sp, sl, ss, sr, sc, sn, '{} Sect'.format(why))  ;  i += 1
                        for r in range(nr):
                            sr+=1 ; self.dumpLabel(self.labels[i], i+1, sp, sl, ss, sr, sc, sn, '{} Row'.format(why))   ;  i += 1
                            for c in range(nc):
                                if s == 0:
                                    if QQ and r == 0: su += 1
                                    else:             sc += 1
                                    self.dumpLabel(self.labels[i], i+1, sp, sl, ss, sr, sc, sn, '{} Col'.format(why))   ;  i += 1
        self.dumpLabel()
        if dbg: self.log('(END) {} {})'.format(self.fmtGeom(), why))
    ####################################################################################################################################################################################################
    def dumpSprite(self, z=None, sid=-1, p=-1, l=-1, s=-1, r=-1, c=-1, n=-1, why=''):
        if z is None: self.log('sid  p  l  s  r   c   n    xc      yc       w       h       x       y    iax  iay    m      mx     my     rot   red grn blu opc v       why            group       parent', ind=0); return
        f = '{:4} {} {:2} {:2} {:2} {:3} {:3} {:7.2f} {:7.2f} {:7.2f} {:7.2f} {:7.2f} {:7.2f} {:4} {:4} {:6.3f} {:6.3f} {:6.3f} {:7.2f}  {:3} {:3} {:3} {:3} {:1} {:16} {} {}'
        k, o, v, g, pg = z.color, z.opacity, z.visible, z.group, z.group.parent
        xc, yc = z.x + z.width/2, z.y + z.height/2
        fs = f.format(sid, p, l, s, r, c, n, xc, yc, z.width, z.height, z.x, z.y, z.image.anchor_x, z.image.anchor_y, z.scale, z.scale_x, z.scale_y, z.rotation, k[0], k[1], k[2], o, v, why, g, pg)
        self.log(fs, ind=0)
        assert(type(z) == pyglet.sprite.Sprite)

    def dumpLabel(self, a=None, lid=-1, p=-1, l=-1, s=-1, r=-1, c=-1, n=-1, why='', idt='lid'):
        if a is None: self.log('{:4} p  l  s  r   c   n     x       y       w       h   text   font name     siz dpi bld itl red grn blu opc  why'.format(idt), ind=0) ; return
        x, y, w, h, fn, d, z, k, b, i, t = a.x, a.y, a.width, a.height, a.font_name, a.dpi, a.font_size, a.color, a.bold, a.italic, a.text
        f = '{:4} {} {:2} {:2} {:2} {:3} {:3} {:7.2f} {:7.2f} {:7.2f} {:7.2f} {:4} {:16} {:2} {:3}  {:1}   {:1}  {:3} {:3} {:3} {:3}  {}'
        fs = f.format(lid, p, l, s, r, c, n, x, y, w, h, t, fn, z, d, b, i, k[0], k[1], k[2], k[3], why)
        self.log(fs, ind=0)
    ####################################################################################################################################################################################################
    def resizeFonts(self):
        ms = self.minSize()  ;  slope, off = 0.6, -1
        fs = fri(ms * slope + off)  ;  formula = '(fs = ms*slope+off)'
        self.log('{} {} ms={:4.1f} slope={} off={} fs={:4.1f}={:2}'.format(self.fmtWH(), formula, ms, slope, off, fs, fri(fs)))
        self.setFontParam('font_size', fs, 'fontSize')

    def minSize(self):
        w = self.tabs[0].width  ;  h = self.tabs[0].height  ;  m = min(w, h)
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
            if QQ: self._setFontParam(self.ucols, n, v, m)
            self._setFontParam(self.tabs, n, v, m)
        else: self._setFontParam(self.labels, n, v, m)

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
        elif kbk == 'N' and self.isCtrl(mods) and self.isShift(mods): self.toggleNotes()
        elif kbk == 'N' and self.isCtrl(mods):                        self.toggleNotes()
        elif kbk == 'Q' and self.isCtrl(mods) and self.isShift(mods): self.quit(        'keyPress({})'.format(kbk))
        elif kbk == 'Q' and self.isCtrl(mods):                        self.quit(        'keyPress({})'.format(kbk))
        elif kbk == 'S' and self.isCtrl(mods) and self.isShift(mods): self.writeTabs()
        elif kbk == 'S' and self.isCtrl(mods):                        self.writeTabs()
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

    def _initCps(self, dbg=1):
        np, nl, ns, nr, nc = self.n  ##;  nr += QQ
        self.cpr =  nc + CCC
        self.cps =  nr * self.cpr
        self.cpl =       self.cps
        self.cpp =  nl * self.cpl
        if dbg: self.log('cpz={}'.format(fmtl(self.cpz())))

    def cursorCol(self, dbg=1): #calc
        p, l, s, r, c = self.j()  #;  r += QQ
        cpp, cpl, cps, cpr = self.cpz()
        cc = p*cpp + l*cpl + s*cps + r*cpr + c
        cc = cc % len(self.tabs)
        if dbg: self.log('p={} l={} s={} r={} c={}'.format(p, l, s, r, c))
        if dbg: self.log('cpp={} cpl={} cps={} cpr={}'.format(cpp, cpl, cps, cpr))
        if dbg: self.log('cc={}=({} * {} + {} * {} + {} * {} + {} * {} + {})'.format(cc, p, cpp, l, cpl, s, cps, r, cpr, c))
        return cc
    ####################################################################################################################################################################################################
    def on_mouse_release(self, x, y, button, modifiers):
        np, nl, ns, nr, nc = self.n  ;  nc += CCC       ;  nr += QQ
        w  = self.ww/nc     ;  h  = self.hh/(nl*ns*nr)  ;  y0 = y          ;  y = self.hh - y
        c  = int(x/w)       ;  r0 = int(y/h) - QQ       ;  d0 = int(ns*nr)
        l = int(r0/d0)      ;   r = int(r0 % d0)        ;   s = int(r/d0)  ;  p = 0
        kk = int(c + r*self.cpr + s*self.cps + l*self.cpl + p*self.cpp)
        self.log('(BGN) x={} y0={:4} y={:4} w={:6.2f} h={:6.2f} c={:4} r0={:4} d0={}'.format(x, y0, y, w, h, c, r0, d0), file=sys.stdout)
        self.log('p={} l={} s={} r={} c={} kk={}'.format(p, l, s, r, c, kk))
        self.log('tabs[kk].txt={}'.format(self.tabs[kk].text), file=sys.stdout)
        k  = kk - self.cc
        self.log('      {:4} {:4} {:4} {} b={} m={} txt={}'.format(k, kk, self.cc, fmtl(self.i, FMTN), button, modifiers, self.tabs[self.cc].text), file=sys.stdout)
        self.move(k)
        self.log('(END) {:4} {:4} {:4} {} b={} m={} txt={}'.format(k, kk, self.cc, fmtl(self.i, FMTN), button, modifiers, self.tabs[self.cc].text), file=sys.stdout)

    def move(self, k, dbg=1): #calc
        np, nl, ns, nr, nc = self.n  ;  nc += CCC   ##;  nr += QQ
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
        np, nl, ns, nr, nc = self.n  ;  nc += CCC  ##;  nr += QQ
        p, l, s,  r, c = self.j()
        jc = c + k
        if dbg: self.log('(BGN) {:4}      {:4} {} nc={}'.format(k, self.cc, fmtl(self.i, FMTN), nc), file=sys.stdout)
        self.i[T] = jc %  nc + 1
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
    def addTab(self, text, why='', dbg=1):
        self.log('(BGN) {} {} {}'.format(self.kpEvntTxt(), fmtl(self.i, FMTN), why))
        self.updateData(text)
        self.updateTab(text)
        self.updateNote(text)
        if dbg: self.snapshot()
        self.log('(END) {} {} {}'.format(self.kpEvntTxt(), fmtl(self.i, FMTN), why))

    def updateData(self, text, data=None, dbg=0):
        if data is None: data = self.data
        p, l, s, r, c = self.j()
        t = data[p][l][c]
        self.log('(BGN) data[{}][{}][{}]={}'.format(p, l, c, self.data[p][l][c]))
        self.data[p][l][c] = t[0:r] + text + t[r+1:]
        if dbg: self.dumpTabs(why='updateData text={} i={} data[p][l][c]={}'.format(text, self.i, data[p][l][c]))
        self.log('(END) data[{}][{}][{}]={}'.format(p, l, c, self.data[p][l][c]))

    def updateTab(self, text, dbg=1):
        cc = self.cursorCol()
        self.log('(BGN) tabs[{}].text={}'.format(cc, self.tabs[cc].text))
        self.tabs[cc].text = text
        if dbg: self.tabs[cc].color = FONT_COLORS[self.fontColorIndex + 4]
        self.log('(BGN) tabs[{}].text={}'.format(cc, self.tabs[cc].text))

    def updateNote(self, text, dbg=1):
        p, l, s, r, c = self.j()
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

    def toggleNotes(self): old = self.N  ;  self.N = not self.N  ;  self.log(FMTR.format('toggling N from {} to {}', old, self.N))
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
    def erase(self, reset=1):
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
            self.log('reset={}'.format(reset))
            self.setStringNumbs()
            self.setStringNames()
            self.setCapo()
        self.log('(END) np={} nl={} nr={} nc={}'.format(np, nl, nr, nc))

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
        row = self.n[R] - r - 1    # Reverse and zero base the string numbering: str[1 ... numStrings] => s[(numStrings - 1) ... 0]
        if dbg: self.log('r={} fretNum={} row={} stringMap={}'.format(r, fn, row, fmtd(self.stringMap)))
        k = self.stringKeys[row]
        i = self.stringMap[k] + fn # calculate the fretted note index using the sorted map
        if dbg: self.log('r={} fretNum={} row={} k={} i={}'.format(r, fn, row, k, i))
        return i

    def getNote(self, row, tab, dbg=1):
        fretNum = self.getFretNum(tab)
        note = Note(self.getNoteIndex(row, fretNum))
        if dbg: self.log('row={} tab={} fretNum={} note.name={} note.index={}'.format(row, tab, fretNum, note.name, note.index))
        return note
    ####################################################################################################################################################################################################
    def cci(self, c, cc):
        if c == 0: self.ci = (self.ci + 1) % len(cc)
        k = (c + self.ci) % len(cc)  ;  self.log('c={} cc={} ci={} k={}'.format(c, cc, self.ci, k))
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
        Tabs.log('BGN Logging Open LOG_PATH={}'.format(LOG_PATH))
        Tabs.log('creating Tabs instance'.format())
        tabsObj     = Tabs()
        Tabs.log('tabs={}'.format(tabsObj))
        Tabs.log('invoking pyglet.app.run()'.format())
        ret = pyglet.app.run()
        Tabs.log('pyglet.app.run() return={}'.format(ret))
#        except(AssertionError, ValueError) as EX:
        Tabs.log('END Logging Close LOG_PATH={}'.format(LOG_PATH))
