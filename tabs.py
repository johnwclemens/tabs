import operator, os, sys
import collections, itertools, queue
from   collections     import Counter
from   itertools       import accumulate
from   more_itertools  import consume  # not installed in GitBash's Python
import pyglet
import pyglet.font            as pygfont
import pyglet.image           as pygimg
import pyglet.window.event    as pygwine
from   pyglet.text     import document, layout
from   tpkg            import utl
from   tpkg            import kysgs
from   tpkg            import misc
from   tpkg            import evnts
from   tpkg            import notes
from   tpkg.notes      import Notes
from   tpkg.strngs     import Strngs
from   tpkg.chords     import Chords
from   tpkg            import cmds
from   tpkg            import unic

F = unic.F
P, L, S, C,          T, N, I, K,          M, R, Q, H,          A, B, D, E   = utl.P, utl.L, utl.S, utl.C,    utl.T, utl.N, utl.I, utl.K,    utl.M, utl.R, utl.Q, utl.H,    utl.A, utl.B, utl.D, utl.E
W, X, Y, Z,       NONE,  ist,  fri,    slog,   fmtf,   fmtl,   fmtm,   fmta = utl.W, utl.X, utl.Y, utl.Z,    utl.NONE,   utl.ist,   utl.fri,     utl.slog,    utl.fmtf, utl.fmtl, utl.fmtm, utl.fmta
BGC,  BOLD,  COLOR,     FONT_NAME,  FONT_SIZE, ITALIC,  KERNING,  UNDERLINE = utl.BGC,   utl.BOLD,  utl.COLOR,   utl.FONT_NAME, utl.FONT_SIZE, utl.ITALIC,    utl.KERNING,      utl.UNDERLINE
isAlt, isCtl, isShf,    isAltShf, isCtlAlt, isCtlShf, isCtlAltShf, isNumLck = utl.isAlt, utl.isCtl, utl.isShf,   utl.isCtlAlt,  utl.isAltShf,  utl.isCtlShf,  utl.isCtlAltShf,  utl.isNumLck

CAT,  CSV,  EVN,  LOG,  PNG,  TXT,  DAT   =  utl.CAT,    utl.CSV,    utl.EVN,    utl.LOG,    utl.PNG,    utl.TXT,    utl.DAT
CATS, CSVS, EVNS, LOGS, PNGS, TEXT, DATA  =  utl.CATS,   utl.CSVS,   utl.EVNS,   utl.LOGS,   utl.PNGS,   utl.TEXT,   utl.DATA 
CAT2, CSV2, EVN2, LOG2, PNG2, TXT2, DAT2  = f'_.{CAT}', f'_.{CSV}', f'_.{EVN}', f'_.{LOG}', f'_.{PNG}', f'_.{TXT}', f'_.{DAT}'
CSV_FILE, EVN_FILE, LOG_FILE, TXT_FILE    = None, None, None, None
BASE_NAME,        BASE_PATH,        PATH  = utl.paths()
CSV_PATH  = utl.getFilePath(BASE_NAME, BASE_PATH, fdir=CSVS, fsfx=CSV,  dbg=0)
DAT_PATH  = utl.getFilePath(BASE_NAME, BASE_PATH, fdir=DATA, fsfx=DAT,  dbg=0)
EVN_PATH  = utl.getFilePath(BASE_NAME, BASE_PATH, fdir=EVNS, fsfx=EVN,  dbg=0)
LOG_PATH  = utl.getFilePath(BASE_NAME, BASE_PATH, fdir=LOGS, fsfx=LOG,  dbg=0)
PNG_PATH  = utl.getFilePath(BASE_NAME, BASE_PATH, fdir=PNGS, fsfx=PNG,  dbg=0)
TXT_PATH  = utl.getFilePath(BASE_NAME, BASE_PATH, fdir=TEXT, fsfx=TXT,  dbg=0)

CSV_PATH2 = utl.getFilePath(BASE_NAME, BASE_PATH, fdir=CSVS, fsfx=CSV2, dbg=0)
DAT_PATH2 = utl.getFilePath(BASE_NAME, BASE_PATH, fdir=DATA, fsfx=DAT2, dbg=0)
EVN_PATH2 = utl.getFilePath(BASE_NAME, BASE_PATH, fdir=EVNS, fsfx=EVN2, dbg=0)
LOG_PATH2 = utl.getFilePath(BASE_NAME, BASE_PATH, fdir=LOGS, fsfx=LOG2, dbg=0)
PNG_PATH2 = utl.getFilePath(BASE_NAME, BASE_PATH, fdir=PNGS, fsfx=PNG2, dbg=0)
TXT_PATH2 = utl.getFilePath(BASE_NAME, BASE_PATH, fdir=TEXT, fsfx=TXT2, dbg=0)

MULTILINE, WRAP_LINES = 'multiline', 'wrap_lines'    ;  LEFT, CENTER, RIGHT, BOTTOM, BASELINE, TOP = 'left', 'center', 'right', 'bottom', 'baseline', 'top'
ALIGN, INDENT, LEAD, LNSP, STRH, TAB_STOPS, WRAP     = 'align', 'indent', 'leading', 'line_spacing', 'stretch', 'tab_stops', 'wrap'
MARGIN_LEFT, MARGIN_RIGHT, MARGIN_TOP, MARGIN_BOTTOM = 'margin_left', 'margin_right', 'margin_top', 'margin_bottom'
TI        = ['tnik', '  i ']
XYWH      = ['   X   ', '   Y   ', '   W   ', '   H   ']
AXY2      = ['x', 'y', 'AnchX', 'AnchY']
CWH       = ['CntWd', 'CntHt']
ACVA      = ['a', 'v']
ADS       = ['Ascnt', 'Dscnt', 'As+Ds']
LTXA      = list(itertools.chain(TI, XYWH, AXY2))
LTXAC     = list(itertools.chain(TI, XYWH, AXY2, CWH))
LDS       = ['FnSz', 'Lead', 'LnSp', 'TablText', ' ForegroundColor ', ' BackgroundColor ', 'B', 'I', 'S', 'M', 'W', 'w', 'FontName']
LLBL      = list(itertools.chain(LTXAC, ADS, ACVA, LDS))
########################################################################################################################################################################################################
TT, NN, II, KK        = utl.TT, utl.NN, utl.II, utl.KK
MLDY, CHRD, ARPG      = utl.MLDY, utl.CHRD, utl.ARPG
LARROW, RARROW        = utl.LARROW, utl.RARROW
DARROW, UARROW        = utl.DARROW, utl.UARROW
LBL, SPR              = utl.LBL, utl.SPR
RGB                   = utl.RGB
C1,  C2               =  0,  1
CSR_MODES             = utl.CSR_MODES
HARROWS, VARROWS      = utl.HARROWS, utl.VARROWS
NORMAL_STYLE, SELECT_STYLE, CURRENT_STYLE = utl.NORMAL_STYLE, utl.SELECT_STYLE, utl.CURRENT_STYLE
########################################################################################################################################################################################################
FIN     = [1, 1, 1, 2, 1]
#           0        1        2        3           4        5        6        7           8        9        10       11          12       13       14       15          16
JTEXTS  = ['Page',  'Line',  'Sect',  'Colm',     'Tabl',  'Note',  'IKey',  'Kord',     'MVie',  'RowL',  'QClm',  'HCrs',     'ANam',  'BNum',  'DCpo',  'EClm',     'TNIK']
JTEXTS2 = ['Page',  'Line',  'Sect',  'Kolm',     'Tabl',  'Note',  'IKey',  'Kord',     'MVie',  'RowL',  'QKlm',  'HCrs',     'ANam',  'BNum',  'DCpo',  'EClm',     'TNIK']
jTEXTS  = ['pages', 'lines', 'sects', 'colms',    'tabls', 'notes', 'ikeys', 'Kords',    'mvies', 'rowls', 'qklms', 'hcsrs',    'anams', 'bnums', 'dcpos', 'eclms',    'tniks']
JFMT    = [ 1,       2,       2,       3,          4,       4,       4,       4,          1,       2,       3,       1,          2,       2,       2,       2,          4]
#JFMT   = [ 2,       3,       3,       6,          6,       6,       6,       6,          1,       3,       5,       1,          3,       3,       3,       4,          7]
########################################################################################################################################################################################################
PNT_PER_PIX =  7/9  # 14pts/18pix
FONT_DPIS   = [ 72, 78, 84, 90, 96, 102, 108, 114, 120 ]
FONT_NAMES  = utl.FONT_NAMES
########################################################################################################################################################################################################
class Tabs(pyglet.window.Window):
########################################################################################################################################################################################################
    def __str__(self):  return f'{self.__class__.__name__}' # {fmtm(ARGS)}'
    def __repr__(self): return f'{self.__class__.__name__}' # {self.width=} {self.height=} {fmtm(ARGS)}'
    ####################################################################################################################################################################################################
    def __init__(self):
        self.LOG_ID = 0                ;   self.log(f'{self.LOG_ID=}')
        self.log(f'BGN {__class__}')   ;   dumpGlobals()
        self.log(f'STFILT:\n{fmtl(utl.STFILT)}')
        utl.timerA()
        utl.timerA(1)
        utl.timerA(1, 2)
        utl.timerA(1, 2, 3)
        utl.timerA(a=1)
        utl.timerA(a=1, b=2)
        utl.timerA(a=1, b=2, c=3)
        utl.timerA(1, 2, c=3)
        utl.timerA(1, b=2, c=3)
        self.fNameLogId, self.LOG_ID = utl.getFileSeqName(   BASE_NAME, BASE_PATH, fdir=LOGS, fsfx=LOG)  ;  self.log(f'{self.LOG_ID=} {self.fNameLogId}')
        self.seqNumCatPath           = utl.getFilePath(self.fNameLogId, BASE_PATH, fdir=CATS, fsfx=CAT)  ;  self.log(f'{self.seqNumCatPath=}')
        self.seqNumCsvPath           = utl.getFilePath(self.fNameLogId, BASE_PATH, fdir=CSVS, fsfx=CSV)  ;  self.log(f'{self.seqNumCsvPath=}')
        self.seqNumLogPath           = utl.getFilePath(self.fNameLogId, BASE_PATH, fdir=LOGS, fsfx=LOG)  ;  self.log(f'{self.seqNumLogPath=}')
        self.seqNumTxtPath           = utl.getFilePath(self.fNameLogId, BASE_PATH, fdir=TEXT, fsfx=TXT)  ;  self.log(f'{self.seqNumTxtPath=}')
        self.addingZ       = 0   ;   self.nvis      = 0    ;   self.DRAW_BGC     = 0
        self.inserting     = 0   ;   self.insertStr = Z    ;   self.prevEvntText = Z
        self.jumping       = 0   ;   self.jumpStr   = Z    ;   self.jumpAbs      = 0
        self.quitting      = 0   ;   self.allTabSel = 0    ;   self.rsyncData    = 0
        self.settingN      = 0   ;   self.setNvals  = []   ;   self.setNtxt      = Z
        self.shifting      = 0   ;   self.shiftSign = 1    ;   self.cc           = 0
        self.swapping      = 0   ;   self.swapSrc   = Z    ;   self.swapTrg      = Z
        self.newC          = 0   ;   self.updC      = 0    ;   self.addC         = 0
        self.hidC          = 0   ;   self.cpyC      = 0    ;   self.pstC         = 0
        self.shwC          = 0   ;   self.snpC      = 0    ;   self.delC         = 0
        self.sprs          = []  ;   self.undoStack = []   ;   self.idmap        = {}
        self.ki            = []  ;   self.ks        = [ W, 0, Notes.NTRL, 'C', 0, [], [] ]
        self.snapReqQ      = queue.SimpleQueue()
        self.J1,       self.J2,      self.j1s,     self.j2s    = [], [], [], []
        self.hArrow,   self.vArrow,  self.csrMode, self.tids   = RARROW, UARROW, CHRD, set()   ;   self.dumpCursorArrows('init()')
        self.tblank,   self.tblanki, self.cursor,  self.data   = None, None, None, []
        self.viewX,    self.viewY,   self.viewW,   self.viewH  = 0, 0, self.width, self.height
        self.viewX0,   self.viewY0,  self.viewW0,  self.viewH0 = 0, 0, self.width, self.height
        self.p0x, self.p0y, self.p0w, self.p0h, self.p0sx, self.p0sy = 0, 0, 0, 0, 0, 0
        pyglet.options['audio'] = ('xaudio2', 'directsound', 'openal', 'pulse', 'silent') # todo add some sound
        ################################################################################################################################################################################################
        self.AUTO_SAVE = 0  ;  self.BGC     = 0  ;  self.CAT     = 0  ;  self.CHECKERED = 0  ;  self.DEC_DATA = 0  ;  self.DSP_J_LEV = 4  ;  self.DBG_TABT  = 0
        self.EVENT_LOG = 0  ;  self.EXIT    = 0  ;  self.FRT_BRD = 0  ;  self.FULL_SCRN = 0  ;  self.GEN_DATA = 0  ;  self.LONG_TXT  = 1  ;  self.MULTILINE = 1
        self.OIDS      = 0  ;  self.ORD_GRP = 1  ;  self.RESIZE  = 1  ;  self.SNAPS     = 0  ;  self.SPRITES  = 0  ;  self.STRETCH   = 0  ;  self.SUBPIX    = 1
        self.TEST      = 0  ;  self.VARROW  = 1  ;  self.VERBY   = 0
        ################################################################################################################################################################################################
        self.AXYV      = [0, 0, 0, 0]   ;   self._initAaxyv()
        self.ROOT_DIR  = 'test'         ;   self.FILE_NAME = BASE_NAME
        self.LL        = 0
        self.SS        = set(range(4))  # set() if 0 else {0, 1, 2, 3}
        self.ZZ        = [] # set()          # set() if 1 else {0} #, 1}
        ################################################################################################################################################################################################
        self.TUNING    = None # guitar 6 std 'EADGBE'
        self.n         = [1, 1, 10, 6]
        self.i         = [1, 1,  1, 6]
        self.VIEW      = []
        ################################################################################################################################################################################################
        self.parseArgs()
        self._initAaxyv()
        ################################################################################################################################################################################################
        self.n0        = []            ;   self.n0.extend(self.n)  ;  self.i0 = []   ;   self.i0.extend(self.i)
        self.n.insert(S, self.ssl())   ;   self.i.insert(S, 1)     ;  self.dumpArgs(f=2)
        self.normi()                   ;   self.h = self.resetH()
        self.LOG_GFN   = self.geomFileName(self.FILE_NAME, LOG)    ;  self.log(f'{self.LOG_GFN=}')
        self.CSV_GFN   = self.geomFileName(self.FILE_NAME, CSV)    ;  self.log(f'{self.CSV_GFN=}')
        self.DAT_GFN   = self.geomFileName(self.FILE_NAME, DAT)    ;  self.log(f'{self.DAT_GFN=}')
        self.TXT_GFN   = self.geomFileName(self.FILE_NAME, TXT)    ;  self.log(f'{self.TXT_GFN=}')
        self.vArrow    = UARROW if self.VARROW == 1 else DARROW
        self.fontStyle = NORMAL_STYLE
        self.k         = {}
        ################################################################################################################################################################################################
        self.sobj      = Strngs(self.TUNING)
        self.cobj      = Chords(self, self.sobj)
        ################################################################################################################################################################################################
        self._initDataPath()
        self._initWindowA()
        self.log(f'WxH={self.fmtWH()}')
        super().__init__(screen=self.screens[self.screenIdx], fullscreen=self.FULL_SCRN, resizable=True, visible=False)
        self.log(f'WxH={self.fmtWH()}')
        self._initWindowB()
        self.log(f'WxH={self.fmtWH()}')
        self._reinit()
        self.log(utl.INIT, p=0)
        self.log(f'END {__class__}')
    ####################################################################################################################################################################################################
    def resetH(self): self.h = [ 0 for _ in self.i ]   ;   return self.h

    def _initAaxyv(self, why=Z, dmp=1):
        self._initAa(self.AXYV[0]) # -1, 0, 1
        self._initAx(self.AXYV[1]) # -1, 0, 1
        self._initAy(self.AXYV[2]) # -1, 0, 1, 2
        self._initAv(self.AXYV[3]) # -1, 0, 1
        if dmp:   self.dumpAXYV(why)
    ####################################################################################################################################################################################################
    def _initAa(self, a):
        self.A_LEFT = 1        if a==-1 else 0  ;  self.A_CENTER = 1  if a==0  else 0  ;  self.A_RIGHT  = 1 if a==1 else 0
        self.aa     = LEFT     if self.A_LEFT  else CENTER if self.A_CENTER else RIGHT if self.A_RIGHT else '??'

    def _initAx(self, x):
        self.X_LEFT = 1        if x==-1 else 0  ;  self.X_CENTER = 1  if x==0  else 0  ;  self.X_RIGHT  = 1 if x==1 else 0
        self.ax     = LEFT     if self.X_LEFT  else CENTER if self.X_CENTER else RIGHT if self.X_RIGHT else '??'

    def _initAy(self, y):
        self.Y_BOTTOM = 1      if y==-1 else 0  ;  self.Y_CENTER = 1  if y==0  else 0  ;  self.Y_TOP    = 1 if y==1 else 0  ;  self.Y_BASELINE = 1 if y==2 else 0
        self.ay       = BOTTOM if self.Y_BOTTOM else CENTER if self.Y_CENTER else TOP  if self.Y_TOP   else BASELINE if self.Y_BASELINE else '??'

    def _initAv(self, v):
        self.V_BOTTOM = 1      if v==-1 else 0  ;  self.V_CENTER = 1  if v==0  else 0  ;  self.V_TOP    = 1 if v==1 else 0
        self.av       = BOTTOM if self.V_BOTTOM else CENTER if self.V_CENTER else TOP  if self.V_TOP   else '??'
    ####################################################################################################################################################################################################
    def normi(self, dbg=1):
        if dbg: self.log(f'before {self.fmti()} {self.fmtn()}')
        i, n = self.i, self.n   ;   self.i = [ i[j] if i[j] <= n[j] else n[j] for j in range(len(i)) ]
        if dbg: self.log(f'after  {self.fmti()} {self.fmtn()}')

    def fileNamePfx(self, ext): return 'E' if ext==TXT else 'D' if ext==DAT else 'C' if ext==CAT else 'B' if self.LL else 'A'

    def geomFileName(self, base, ext, dbg=1):
        n0  = []     ;  n0.extend(self.n0)   ;   n0.insert(S, '_')
        n   = n0        if ext==DAT else self.n
        lbl = self.fileNamePfx(ext)
        n1  = [Z.join([lbl, base])]
        n1.extend([ str(i) for i in n ])
        axay = f'{self.ftAx(self.ax)}{self.ftAy(self.ay)}'
        aaav = f'{self.ftAa(self.aa)}{self.ftAv(self.av)}' if not self.SPRITES else Z
        if ext == DAT:   n2 = []
        else:            n2 = ['_', axay]    ;   n2.extend(['_', aaav])  if aaav else None
        n2.extend(['.', ext])
        n1  = '.'.join(n1)
        n2  =   Z.join(n2)
        _   =   Z.join([n1, n2])
        self.log(f'{9*W}{_}') if dbg else None
        return _
    ####################################################################################################################################################################################################
    def parseArgs(self):
        self.log(f'argMap={fmta(ARGS)}')
        if 'a' in ARGS  and len(ARGS['a']) == 0: self.AUTO_SAVE  =  1
        if 'A' in ARGS: l = len(ARGS['A'])   ;   self.VARROW     =  1 if l == 0 else int(ARGS['A'][0]) if l == 1 else 0
        if 'b' in ARGS  and len(ARGS['b']) == 0: self.FRT_BRD    =  1
        if 'B' in ARGS  and len(ARGS['B']) == 0: self.BGC        =  1
        if 'c' in ARGS  and len(ARGS['c']) == 0: self.CAT        =  1
        if 'C' in ARGS  and len(ARGS['C']) == 0: self.CHECKERED  =  1
        if 'd' in ARGS  and len(ARGS['d']) == 0: self.DEC_DATA   =  1 
        if 'D' in ARGS  and len(ARGS['D'])  > 0: self.DBG_TABT   =   int(ARGS['D'][0])
        if 'e' in ARGS  and len(ARGS['e']) == 0: self.EVENT_LOG  =  1
        if 'e' in ARGS  and len(ARGS['e'])  > 0: self.EVENT_LOG  =   int(ARGS['e'][0])
        if 'f' in ARGS  and len(ARGS['f'])  > 0: self.FILE_NAME  =       ARGS['f'][0]
        if 'F' in ARGS  and len(ARGS['F']) == 0: self.FULL_SCRN  =  1
        if 'g' in ARGS  and len(ARGS['g']) == 0: self.ORD_GRP    =  1
        if 'G' in ARGS  and len(ARGS['G']) == 0: self.GEN_DATA   =  1
        if 'i' in ARGS  and len(ARGS['i'])  > 0: self.i          = [ int(ARGS['i'][i]) for i in range(len(ARGS['i'])) ]
        if 'j' in ARGS  and len(ARGS['j'])  > 0: self.DRAW_BGC   =   int(ARGS['j'][0])
        if 'J' in ARGS  and len(ARGS['J'])  > 0: self.DSP_J_LEV  =   int(ARGS['J'][0])
        if 'l' in ARGS  and len(ARGS['l']) == 0: self.LONG_TXT   =  1
        if 'L' in ARGS  and len(ARGS['L']) == 0: self.LL         =  1
        if 'M' in ARGS  and len(ARGS['M']) == 0: self.MULTILINE  =  1
        if 'n' in ARGS  and len(ARGS['n'])  > 0: self.n          = [ int(ARGS['n'][i]) for i in range(len(ARGS['n'])) ]
        if 'o' in ARGS  and len(ARGS['o']) == 0: self.OIDS       =  1
        if 'p' in ARGS  and len(ARGS['p'])  > 0: self.SNAPS      =   int(ARGS['p'][0])
        if 'r' in ARGS  and len(ARGS['r'])  > 0: self.ROOT_DIR   =       ARGS['r'][0] 
        if 'R' in ARGS  and len(ARGS['R']) == 0: self.RESIZE     =  0
        if 's' in ARGS  and len(ARGS['s']) == 0: self.SPRITES    =  1
        if 'S' in ARGS  and len(ARGS['S']) >= 0: self.SS         = { int(ARGS['S'][i]) for i in range(len(ARGS['S'])) }
        if 't' in ARGS: l = len(ARGS['t'])   ;   self.TEST       =  1 if l == 0 else int(ARGS['t'][0]) if l == 1 else 0
        if 'T' in ARGS  and len(ARGS['T'])  > 0: self.TUNING     = [ ARGS['T'][i] for i in range(len(ARGS['T'])) ]
        if 'u' in ARGS  and len(ARGS['u']) == 0: self.SUBPIX     =  1
        if 'v' in ARGS: l = len(ARGS['v'])   ;   self.VERBY      =  1 if l == 0 else int(ARGS['v'][0]) if l == 1 else 0
        if 'V' in ARGS  and len(ARGS['V'])  > 0: self.VIEW       = [ int(ARGS['V'][i]) for i in range(len(ARGS['V'])) ]
        if 'w' in ARGS  and len(ARGS['w'])  > 0: self.AXYV       = [ int(ARGS['w'][i]) for i in range(len(ARGS['w'])) ]
        if 'x' in ARGS  and len(ARGS['x'])  > 0: self.EXIT       =   int(ARGS['x'][0]) # == 0: self.EXIT       =  1
        if 'Z' in ARGS  and len(ARGS['Z']) >= 0: self.ZZ         = [ int(ARGS['Z'][i]) for i in range(len(ARGS['Z'])) ]
        
    def dumpArgs(self, f=1):
        self.log(f'[a]      {self.AUTO_SAVE=}', f=f)
        self.log(f'[A]         {self.VARROW=}', f=f)
        self.log(f'[b]        {self.FRT_BRD=}', f=f)
        self.log(f'[B]            {self.BGC=}', f=f)
        self.log(f'[c]            {self.CAT=}', f=f)
        self.log(f'[C]      {self.CHECKERED=}', f=f)
        self.log(f'[d]       {self.DEC_DATA=}', f=f)
        self.log(f'[D]       {self.DBG_TABT=}', f=f)
        self.log(f'[e]      {self.EVENT_LOG=}', f=f)
        self.log(f'[f]      {self.FILE_NAME=}', f=f)
        self.log(f'[F]      {self.FULL_SCRN=}', f=f)
        self.log(f'[g]        {self.ORD_GRP=}', f=f)
        self.log(f'[G]       {self.GEN_DATA=}', f=f)
        self.log(f'[i]              .{self.fmti()}', f=f)
        self.log(f'[J]      {self.DSP_J_LEV=}', f=f)
        self.log(f'[l]       {self.LONG_TXT=}', f=f)
        self.log(f'[L]             {self.LL=}', f=f)
        self.log(f'[M]      {self.MULTILINE=}', f=f)
        self.log(f'[n]              .{self.fmtn()}', f=f)
        self.log(f'[o]           {self.OIDS=}', f=f)
        self.log(f'[p]          {self.SNAPS=}', f=f)
        self.log(f'[r]       {self.ROOT_DIR=}', f=f)
        self.log(f'[R]         {self.RESIZE=}', f=f)
        self.log(f'[s]        {self.SPRITES=}', f=f)
        self.log(f'[S]             .SS={fmtl(self.SS)}', f=f)
        self.log(f'[t]           {self.TEST=}', f=f)
        self.log(f'[T]         .TUNING={fmtl(self.TUNING)}', f=f)
        self.log(f'[u]         {self.SUBPIX=}', f=f)
        self.log(f'[v]          {self.VERBY=}', f=f)
        self.log(f'[V]           {self.VIEW=}', f=f)
        self.log(f'[w]           .AXYV={fmtl(self.AXYV)}', f=f)
        self.log(f'[x]           {self.EXIT=}', f=f)
        self.log(f'[Z]             .ZZ={fmtl(self.ZZ)}', f=f)
    ####################################################################################################################################################################################################
    def reinit( self):   self._reinit()
    def _reinit(self):
        self.log('BGN')
        self.tpb, self.tpp, self.tpl, self.tps, self.tpc = self.ntp(dbg=1, dbg2=1)
        self.tpb2, self.tpp2, self.tpl2, self.tpc2       = self.ntp2()
        self.data  = []   ;   self.visib = []    ;    self.nic = Counter()
        self.pages, self.lines, self.sects, self.colms = [], [], [], []  ;  self.A  = [self.pages, self.lines, self.sects, self.colms]
        self.tabls, self.notes, self.ikeys, self.kords = [], [], [], []  ;  self.B  = [self.tabls, self.notes, self.ikeys, self.kords]
        self.views, self.rowLs, self.qclms, self.hcurs = [], [], [], []  ;  self.C  = [self.views, self.rowLs, self.qclms, self.hcurs]
        self.anams, self.bnums, self.capos, self.zclms = [], [], [], []  ;  self.D  = [self.anams, self.bnums, self.capos, self.zclms]
        self.E     = [*self.A, *self.B, *self.C, *self.D]         ;   self.log(f'E={fmtl(self.E, d=" [", d2="] ")}')
        self.resetJ('_reinit')
        self.cc, self.cursor, self.caret = 0, None, None
        self.ki    = [ 0 for _ in range(len(self.E)) ]            ;   self.log(fmtl(self.ki))
        self.tblanki, self.tblanks = 0, [W, '-', '.', '`', '~']   ;   self.tblank    = self.tblanks[self.tblanki]
        self.tblankCol             = self.tblank * self.n[T]      ;   self.tblankRow = self.tblank * self.n[C] #(self.n[C] + self.zzlen())
        self.dumpBlanks()
        self._init()
        self.log('END', pos=1)

    def _init(self):
        self.log(f'{fmtl(FONT_NAMES, s=Y)=}')
        utl.initColors(self.k, self.SPRITES, self.BGC, self.initk)
        self._initData()
        if self.AUTO_SAVE: pyglet.clock.schedule_interval(self.autoSave, 10, how='autoSave timer')
        self._initFonts()
        self._initTextLabels()
        self._initTniks()
    ####################################################################################################################################################################################################
    @utl.dbg0
    def initk(self, j, key0, rgb0, opc0, key1, rgb1, opc1):
        self.log(f'{j:2}  {JTEXTS[j]:4}  [{key0} {rgb0:2} {opc0:2}] [ {key1} {rgb1:2} {opc1:2}] {fmtl(RGB[key0][rgb0][opc0], w=3)} {fmtl(RGB[key1][rgb1][opc1], w=3)}', p=0)
        return [RGB[key0][rgb0][opc0], RGB[key1][rgb1][opc1]]
    ####################################################################################################################################################################################################
    def _initData(self):
        self._initDataPath()
        self.genDataFile( self.dataPath1) if self.GEN_DATA or not self.dataPath1.exists() else None
        self.readDataFile(self.dataPath1)
        utl.copyFile(     self.dataPath1, self.dataPath2)
        utl.copyFile(     self.dataPath1, self.dataPath3)
        old       =  self.fmtn(Z)
        self.n[P] =  self.dl()[0]
        self.log(self.fmtdl())
        self.log(f'Updating n[P]  {old=} {self.fmtn()}')
        self.tpb, self.tpp, self.tpl, self.tps, self.tpc = self.ntp(dbg=1, dbg2=1)
        self.tpb2, self.tpp2, self.tpl2, self.tpc2       = self.ntp2()

    def _initDataPath(self):
        name0 = self.DAT_GFN + '.asv'
        name1 = self.DAT_GFN
        name2 = self.DAT_GFN
        name3 = self.FILE_NAME + '.' + DAT
        self.dataPath0 = BASE_PATH / DATA / name0
        self.dataPath1 = BASE_PATH /        name1
        self.dataPath2 = BASE_PATH / DATA / name2
        self.dataPath3 = BASE_PATH / DATA / name3
        self.log(f'{name0=}')
        self.log(f'{name1=}')
        self.log(f'{name2=}')
        self.log(f'{name3=}')
        self.log(f'{self.dataPath0=}', p=0)
        self.log(f'{self.dataPath1=}', p=0)
        self.log(f'{self.dataPath2=}', p=0)
        self.log(f'{self.dataPath3=}', p=0)

    def makeSubDirs(self, path):
        if not path.parent.exists():
            self.log(f'WARN Invalid Data File Path {path.parent=} -> mkdir', f=2)
            path.parent.mkdir(parents=True, exist_ok=True)
            if not path.parent.exists():    msg = f'ERROR mkdir failed on {path.parent=}'  ;  self.log(msg)  ;  cmd = cmds.QuitCmd(self, msg)  ;  cmd.do()
            if not path.exists():           path.touch()
    ####################################################################################################################################################################################################
    def _initWindowA(self, dbg=1):
        display        = pyglet.canvas.get_display()
        if dbg: self.log(f'BGN {self.fmtWH()}')  ;  self.log(f'{display=}')
        self.screenIdx = 0
        self.screens   = display.get_screens()   ;  screens = self.screens
        for i, s in enumerate(screens):
            if i > 0 and s.height > screens[i-1].height: self.screenIdx = i
            self.log(f'screens[{i}] {s.x=} {s.y:5} {self.fmtWH(s.width, s.height)}')
        self.log(f'END {self.fmtWH()} {self.screenIdx=}')
    ####################################################################################################################################################################################################
    def splitH( self, p, n, dbg=1):
        if   ist(p, LBL):
            p.x, p.width,   self.p0x, self.p0w = self.splitHL(p.x, p.width, n)
            if dbg:         self.log(f'{p.x=:.2f} {p.width=:.2f} {n=} {self.p0x=:.2f} {self.p0w=:.2f}')
        elif ist(p, SPR):
            p.x, p.scale_x, self.p0x, self.p0w = self.splitHS(p.x, p.width, n, p.image.width)
            if dbg:         self.log(f'{p.x=:.2f} {p.scale_x=:.4f} {n=} {self.p0x=:.2f} {self.p0w=:.2f} {self.p0sx=:.4f}')
        return p
    
    def splitHL(self, x, w, n):
        x0 = x                     ;   w0  = w
        w2 = w/n                   ;   w  -= w2
        x  = w2 + w2/2 + w/2       ;   x2  = w2
        self.log(f'{x0=:6.2f} {w0=:6.2f} {n=} {x=:6.2f} {w=:6.2f} {x2=:6.2f} {w2=:6.2f}')
        return x, w, x2, w2
    
    def splitHS(self, x, w, n, s):
        x0 = x                     ;   w0  = w     ;   s0 = s
        w2 = w/n                   ;   w  -= w2    ;   s  = w/s0
        x  = w2 + w2/2 + w/2       ;   x2  = w2
        self.log(f'{x0=:6.2f} {w0=:6.2f} {s0=:6.4f} {n=} {x=:6.2f} {w=:6.2f} {s=:6.4f} {x2=:6.2f} {w2=:6.2f}')
        return x, s, x2, w2
    ####################################################################################################################################################################################################
    def setView(self, i=0):
        self.viewX,  self.viewY,  self.viewW,  self.viewH  =     0,          0,      self.width, self.height
        self.viewX0, self.viewY0, self.viewW0, self.viewH0 = self.viewX, self.viewY, self.viewW, self.viewH if i else None
#    def setView(self, nx, ny):
#        self.updView(nx, ny)
#        self.viewX0, self.viewY0, self.viewW0, self.viewH0 = self.viewX, self.viewY, self.viewW, self.viewH

#    def updView(self, nx=0, ny=0, n=None):
#        nc = self.n[C]     + nx
#        n  = self.nlnsnt() if n is None else n
#        nt = n + ny
#        if nt <= 0:  self.log(f'{nt=} {nx=} {ny=} {n=} {nc=} ERROR set nt=1')   ;   nt = self.n[T] * self.n[S]
#        x  = self.width  * nx/nc
#        y  = self.height * ny/nt # if ny<=1 else self.height/nt
#        self.viewX,  self.viewY,  self.viewW,  self.viewH  = x, self.height/2, self.width-x, self.height-y
##        self.viewX,  self.viewY,  self.viewW,  self.viewH  = x, y if ny<=1 else y/2, self.width-x, self.height-y
#        self.log(f'{nx=} {ny=} {n=} {nc=} {nt=} {self.viewX=:.2f} {self.viewY=:.2f} {self.viewW=:.2f} {self.viewH=:.2f}')
    ####################################################################################################################################################################################################
    def _initWindowB(self, dbg=1):
        if dbg: self.log(f'BGN {self.fmtWH()}')
        self.batch = pyglet.graphics.Batch()
        self._initGroups()
        self.set_visible()
        self.log(f'get_size={self.get_size()}')
        self.setView(i=1) # len(self.ZZ), self.LL)
        self.keyboard = None
        if self.EVENT_LOG:
            if self.EVENT_LOG == 1:   self.eventLogger = pyglet.window.event.WindowEventLogger(EVN_FILE)
            else: # 'on_draw', 'on_move', 'on_text', 'on_key_pressed', 'on_key_released', 'on_mouse_scroll', 'on_mouse_motion', 'on_text_motion'
#                flist = ['on_draw']
#                flist = ['on_draw', 'on_move']
                flist = ['on_draw', 'on_move', 'on_mouse_motion']
                self.log(f'{fmtl(flist)} {EVN_FILE=}', f=-3)   ;   self.log(f'{fmtl(flist)} {EVN_FILE=}', f=4)
                from tpkg.evnts import FilteredEventLogger as FELogger
                self.eventLogger = FELogger(self, EVN_FILE, flist)
            self.keyboard        = pygwine.key.KeyStateHandler()
            self.push_handlers(self.eventLogger, self.keyboard)
        if dbg: self.log(f'END {self.fmtWH()}')
    ####################################################################################################################################################################################################
    def _initGroups(self):
        hdrB           =    W.join([ f'{t[0]:2}' for t in JTEXTS ])
        hdrA           =           [P,  L,  S,  C,    T,  N,  I,  K,     M,  R,  Q,  H,     B,  A,  D,  E]
        if len(self.ZZ): self.gn = [1,  2,  3,  4,    7,  8,  9, 10,     0,  5,  6, 15,    11, 12, 13, 14]   ;   self.g = []
        else:            self.gn = [0,  1,  2,  3,    6,  7,  8,  9,    15,  4,  5, 14,    10, 11, 12, 13]   ;   self.g = []
        self.log(fmtl(hdrA, w=2))    ;    self.log(f'  {hdrB}')    ;    self.log(fmtl(self.gn, w=2))
        for i in range(1 + max(self.gn)):
            p   = None if self.ORD_GRP or i==0 else self.g[i-1]
            self.g.append(self._initGroup(i, p))
            self.log(f'g[{i}]={self.g[i]} p={self.g[i].parent}')

    def _initGroup(self, order=0, parent=None): return pyglet.graphics.Group(order, parent) if self.ORD_GRP else pyglet.graphics.Group(parent)
    ####################################################################################################################################################################################################
    def _initTextLabels(self):
        self.labelTextA, self.labelTextB = [], []
        self.createLabelText()
        self.llText = self.labelTextB
#        self.llText = ['M', '0']
#        self.llText.extend(self.labelTextB)
        self.log(fmtl(self.llText))
    ####################################################################################################################################################################################################
    def _initTniks(self):
        self.ssl()   ;   self.smap = {}
        [ self.visib.append([]) for _ in range(len(JTEXTS)) ]
        self.createTniks()
        self.ks = kysgs.nic2KS(self.nic)
        self.log( kysgs.fmtKSK(self.ks[kysgs.KSK]), f=2)
        if self.TEST == 1:
            from tpkg import tests
            attrs = {'TI':TI, 'XYWH':XYWH, 'AXY2':AXY2, 'CWH':CWH, 'LTXA':LTXA, 'LTXAC':LTXAC, 'ADS':ADS, 'ACVA':ACVA, 'LDS':LDS, 'LLBL':LLBL}
            mthds = {'JSPR':JSPR, 'JLBL':JLBL}
            tests.test1(self, attrs, mthds)
            tests.test4(ARGS)
#            tests.test0(self,  0.314159265359, 4)
#            tests.test0(self,  0.314159265359, 5, self.EXIT)
    ####################################################################################################################################################################################################
    def lenA(self):                   return [ len(_) for _ in self.A ]
    def lenB(self):                   return [ len(_) for _ in self.B ]
    def lenC(self):                   return [ len(_) for _ in self.C ]
    def lenD(self):                   return [ len(_) for _ in self.D ]
    def lenE(self):                   return [ len(_) for _ in self.E ]
    ####################################################################################################################################################################################################
    def isJV(self, j=0, dbg=0): # fixme all the other values > k?
        if   P <= j <= K and self.J1[P] == self.j()[P]: v = 1
#        if   P <= j <= K and self.J2[P] == self.i[P]:   v = 1
        elif j in (M, R, Q, H, B, A, D, E):             v = 1
        else:                                           v = 0
        if dbg:  why = f'{v=}'  ;  self.log(f'{self.fmtJText(j, why)} {self.J2[j]=} {self.i[j]=} {self.fmti()} {v=}', f=0)
        return v
    ####################################################################################################################################################################################################
    def resetJ(self, why=Z, dbg=1): self.J1 = [ 0 for _ in range(len(self.E)+1) ]  ;  self.J2 = [ 0 for _ in range(len(self.E)+1) ]  ;  self.nvis = 0  ;  self.dumpJs(why) if dbg else None

#   def setJ(self, j, n, v=None, dbg=0):
#       self.log(f'{j=} {n=} {v=}') if dbg else None
#       self.J1[j] = n  ;  self.J2[j] += 1  ;   self.J1[-1] += 1  ;  self.J2[-1] += 1

    def setJ(self, j, n, v=None):
        v = self.isJV(j) if v is None else v
        self.J1[j] = n  ;  self.J2[j] += 1  ;   self.J1[-1] += 1  ;  self.J2[-1] += 1
        self.nvis  += 1 if v else 0
        assert ist(v, int),  f'{type(v)=} {v=}'
        self.visib[j].append(v)

    def setJdump(self, j, n, v=None, why=Z):
        i = self.J2[j]   ;  self.setJ(j, n, v)
        assert 0 <= j < len(self.E),     f'{j=} out of range {i=} {n=} {v=} {why=}'
        assert 0 <= i < len(self.E[j]),  f'{i=} out of range {j=} {n=} {v=} {why=} {len(self.E[j])=} {self.fjlen()} {self.fmtJ1(1)} {self.fmtJ2(1)}'
        self.dumpTnik(self.E[j][i], j, why)  ;   return j
    ####################################################################################################################################################################################################
    def hh( self):                   return [ i-1 if i else 0 for    i in           self.h ]
    def j(  self):                   return [ i-1 if i else 0 for    i in           self.i ]
    def j2( self):                   return [ i-1 if i else 0 for j, i in enumerate(self.i)  if j != S ]
    def j2g(self, j):                return self.g[ self.gn[j] ]
    ####################################################################################################################################################################################################
    def ssl(self, dbg=0):  l = len(self.SS)  ;   self.log(f'{self.fmtn()} SS={fmtl(self.ss2sl())} {l=}') if dbg else None   ;   return l   # return 0-4
    def zzl(self, dbg=0):  l = len(self.ZZ)  ;   self.log(f'{self.fmtn()} ZZ={fmtl(self.ZZ)} {l=}')      if dbg else None   ;   return l   # return 0-2
    def ss2sl(self): return sorted(self.SS)
    ####################################################################################################################################################################################################
    def fss2sl(self):    s2s = self.ss2sl()  ;   ss = W.join([str(s2s[i]) if i < len(s2s) else W for i in range(4)])  ;  return f'({ss:7})'
    def fzz(   self):    z2z = self.ZZ       ;   zz = W.join([str(z2z[i]) if i < len(z2z) else W for i in range(2)])  ;  return f'({zz:3})'
    ####################################################################################################################################################################################################
    def dl(    self, data=None, p=0, l=0, c=0):  return list(map(len,                       self.dplc(data, p, l, c)))
    def dt(    self, data=None, p=0, l=0, c=0):  return list(map(type,                      self.dplc(data, p, l, c)))
    def dtA(   self, data=None, p=0, l=0, c=0):  return [ str(type(a)).strip('<>') for a in self.dplc(data, p, l, c) ]
    ####################################################################################################################################################################################################
    def dproxy(self, data):                    return data if data is not None else self.data
    def dplc(  self, data=None, p=0, l=0, c=0):
        data = self.dproxy(data)
        if data:
            if p >= len(data):           msg = f'ERROR BAD p index {p=} {l=} {c=} {len(data)=}'        ;  self.log(msg)  ;  cmd = cmds.QuitCmd(self, msg)  ;  cmd.do()
            if l >= len(data[p]):        msg = f'ERROR BAD l index {p=} {l=} {c=} {len(data[p])=}'     ;  self.log(msg)  ;  cmd = cmds.QuitCmd(self, msg)  ;  cmd.do()
            if c >= len(data[p][l]):     msg = f'ERROR BAD c index {p=} {l=} {c=} {len(data[p][l])=}'  ;  self.log(msg)  ;  cmd = cmds.QuitCmd(self, msg)  ;  cmd.do()
            return data, data[p], data[p][l], data[p][l][c]
        return []
    ####################################################################################################################################################################################################
#    def fplc(  self): i = self.i  ;  p, l,    c    = i[P], i[L],       i[C]        ;  return f'[{p} {l}   {c:2}]'
#    def fplct( self): i = self.i  ;  p, l,    c, t = i[P], i[L],       i[C], i[T]  ;  return f'[{p} {l}   {c:2} {t}]'
#    def fplsc( self): i = self.i  ;  p, l, s, c    = i[P], i[L], i[S], i[C]        ;  return f'[{p} {l} {s} {c:2}]'
#    def fplsct(self): i = self.i  ;  p, l, s, c, t = i[P], i[L], i[S], i[C], i[T]  ;  return f'[{p} {l} {s} {c:2} {t}]'
    @staticmethod
    def fplc(  p, l,    c):      return f'[{p} {l}   {c:2}]'
    @staticmethod
    def fplct( p, l,    c, t):   return f'[{p} {l}   {c:2} {t}]'
    @staticmethod
    def fplsc( p, l, s, c):      return f'[{p} {l} {s} {c:2}]'
    @staticmethod
    def fplsct(p, l, s, c, t):   return f'[{p} {l} {s} {c:2} {t}]'
    ####################################################################################################################################################################################################
#    def fplc(  self, p=None, l=None,         c=None):         i = self.i  ;  p = i[P] if p is None else p  ;  l = i[L] if l is None else l  ;                                   c = i[C] if c is None else c  ;                                   return f'[{p} {l}   {c:2}]'
#    def fplct( self, p=None, l=None,         c=None, t=None): i = self.i  ;  p = i[P] if p is None else p  ;  l = i[L] if l is None else l  ;                                   c = i[C] if c is None else c  ;  t = i[T] if t is None else t  ;  return f'[{p} {l}   {c:2} {t}]'
#    def fplsc( self, p=None, l=None, s=None, c=None):         i = self.i  ;  p = i[P] if p is None else p  ;  l = i[L] if l is None else l  ;  s = i[S] if s is None else s  ;  c = i[C] if c is None else c  ;                                   return f'[{p} {l} {s} {c:2}]'
#    def fplsct(self, p=None, l=None, s=None, c=None, t=None): i = self.i  ;  p = i[P] if p is None else p  ;  l = i[L] if l is None else l  ;  s = i[S] if s is None else s  ;  c = i[C] if c is None else c  ;  t = i[T] if t is None else t  ;  return f'[{p} {l} {s} {c:2} {t}]'
#    def fplc(  self, p=None, l=None,         c=None):         i = self.i  ;  p = i[P] if p is None else 1+p  ;  l = i[L] if l is None else 1+l  ;                                     c = i[C] if c is None else 1+c  ;                                     return f'[{p} {l}   {c:2}]'
#    def fplct( self, p=None, l=None,         c=None, t=None): i = self.i  ;  p = i[P] if p is None else 1+p  ;  l = i[L] if l is None else 1+l  ;                                     c = i[C] if c is None else 1+c  ;  t = i[T] if t is None else 1+t  ;  return f'[{p} {l}   {c:2} {t}]'
#    def fplsc( self, p=None, l=None, s=None, c=None):         i = self.i  ;  p = i[P] if p is None else 1+p  ;  l = i[L] if l is None else 1+l  ;  s = i[S] if s is None else 1+s  ;  c = i[C] if c is None else 1+c  ;                                     return f'[{p} {l} {s} {c:2}]'
#    def fplsct(self, p=None, l=None, s=None, c=None, t=None): i = self.i  ;  p = i[P] if p is None else 1+p  ;  l = i[L] if l is None else 1+l  ;  s = i[S] if s is None else 1+s  ;  c = i[C] if c is None else 1+c  ;  t = i[T] if t is None else 1+t  ;  return f'[{p} {l} {s} {c:2} {t}]'
#   def fplc(  self, p=None, l=None,         c=None):         j = self.j()  ;  p = j[P] if p is None else p  ;  l = j[L] if l is None else l  ;                                   c = j[C] if c is None else c  ;                                   return f'[{p+1} {l+1}   {c+1:2}]'
#   def fplct( self, p=None, l=None,         c=None, t=None): j = self.j()  ;  p = j[P] if p is None else p  ;  l = j[L] if l is None else l  ;                                   c = j[C] if c is None else c  ;  t = j[T] if t is None else t  ;  return f'[{p+1} {l+1}   {c+1:2} {t+1}]'
#   def fplsc( self, p=None, l=None, s=None, c=None):         j = self.j()  ;  p = j[P] if p is None else p  ;  l = j[L] if l is None else l  ;  s = j[S] if s is None else s  ;  c = j[C] if c is None else c  ;                                   return f'[{p+1} {l+1} {s+1} {c+1:2}]'
#   def fplsct(self, p=None, l=None, s=None, c=None, t=None): j = self.j()  ;  p = j[P] if p is None else p  ;  l = j[L] if l is None else l  ;  s = j[S] if s is None else s  ;  c = j[C] if c is None else c  ;  t = j[T] if t is None else t  ;  return f'[{p+1} {l+1} {s+1} {c+1:2} {t+1}]'
    ####################################################################################################################################################################################################
    def jsum(  self, a=1):          return [ _ + a if self.J2[j] and j < len(self.J1)-1 else _ if j == len(self.J1)-1 else 0 for j, _ in enumerate(self.J1) ]
    def jlen(self):                 return [ len(e) for e in self.E ]
    def fjlen(self):                return fmtl(self.jlen())
    def fmtdl( self, data=None):    return f'{fmtl(self.dl(data))}'
    def fmtdt( self, data=None):    return f"[{W.join([ t.replace('class ', Z) for t in self.dtA(data) ])}]"
    def fmtJ1( self, w=None, d=1):  w = w if w is not None else JFMT  ;  d = Z if not d else "["  ;  d2 =Z if not d else "]"  ;  return    f'{fmtl(self.jsum(), w=w, d=d, d2=Z)} {self.fnvis()}{d2}'
    def fmtJ2( self, w=None, d=1):  w = w if w is not None else JFMT  ;  d = Z if not d else "["  ;  d2 =Z if not d else "]"  ;  return    f'{fmtl(self.J2,     w=w, d=d, d2=Z)} {self.fnvis()}{d2}'
    def fmtLE( self, w=None, d=1):  w = w if w is not None else JFMT  ;  d = Z if not d else "["  ;  d2 =Z if not d else "]"  ;  return f'{d}{fmtl(self.lenE(), w=w, d=Z, d2=Z)} {sum(self.lenE()[:-1]):4} {self.fnvis()}{d2}'
    ####################################################################################################################################################################################################
    def fmtPos(self):                         cc = self.plct2cc(*self.j2())  ;  nc = self.normalizeCC(cc)  ;  cn = self.cc2cn(cc)  ;  return f'{fmtl(self.i, w=FIN)} {cc+1:3} {nc:3} {cn+1:2}]'
    def fmtn(  self, pfx='n=', n=None):       n = n if n is not None else self.n   ;   return f'{pfx}{fmtl(n)}'
    def fmti(  self, pfx='i='):               return f'{pfx}{fmtl(self.i)}'
    def fmtD(  self, data=None,      d='x'):  l = list(map(str, self.dl(data)))               ;   return f'({d.join(l):^10})'
    def fmtI(  self,                 d='.'):  l = list(map(str, self.i))   ;   del l[S:S+1]   ;   return f'({d.join(l):^10})'
    def fmtWH( self, w=None, h=None, d='x'):
        if w is None: w = self.width  if self.width  is not None else -1
        if h is None: h = self.height if self.height is not None else -1
        return f'({w if w is None else w:4}{d}{h if h is None else h:<4})'
    def fmtP0( self):                         return f'{self.p0x} {self.p0w} {self.p0sx} {self.p0y} {self.p0h} {self.p0sy}'
    def fmtWHP0(self):                        return f'{self.fmtWH()} {self.fmtP0()}'
    ####################################################################################################################################################################################################
    @staticmethod
    def fmtJText(j, why=Z):   jtxt = JTEXTS[j] if 0 <= j < len(JTEXTS) else f'?{j:2}?'   ;   return f'{j=} {why} {jtxt}'
    ####################################################################################################################################################################################################
    @staticmethod
    def ffont(t):     return f'{t.dpi:3} {t.bold:1} {t.italic:1} {t.font_name:14}'
    ####################################################################################################################################################################################################
    @staticmethod
    def ftcolor(t):  k = W.join([ f'{k:3}' for k in t.color[:3] ])  ;  k += f' {t.opacity:3}'  ;  return f'[{k}]'
    @staticmethod
    def fFntSz(t):    return f'{t.font_size:4.0f}'
    @staticmethod
    def ftMxy(t):     return f'{t.scale:5.3f} {t.scale_x:5.3f} {t.scale_y:5.3f}'
    @staticmethod
    def ftvis(t):     return 'V' if t.visible else 'I'
    ####################################################################################################################################################################################################
    @staticmethod
    def ftxywh(t, s=W):         return Tabs.fxywh(t.x, t.y, t.width, t.height, s=s)
    @staticmethod
    def fxywh(x, y, w, h, s=W): return f'{x:7.2f}{s}{y:7.2f}{s}{w:7.2f}{s}{h:7.2f}'
    ####################################################################################################################################################################################################
    @staticmethod
    def fiax(t):      return f'{t.image.anchor_x:4}'
    @staticmethod
    def fiay(t):      return f'{t.image.anchor_y:4}'
    @staticmethod
    def fgrp(t):      return f'{t.group}'
    @staticmethod
    def fgrpp(t):     return f'{t.group.parent}'
    ####################################################################################################################################################################################################
    def setAa(self, a): self._initAa(a)
    def setAx(self, x): self._initAx(x)
    def setAy(self, y): self._initAy(y)
    def setAv(self, v): self._initAv(v)
    ####################################################################################################################################################################################################
    def dumpAXYV(self, why=Z): self.log(X.join([ why, self.fmtAa(), self.fmtAx(), self.fmtAy(), self.fmtAv() ]))
    def fmtAa(   self):        a = W.join([f'{self.A_LEFT}',   f'{self.A_CENTER}', f'{self.A_RIGHT}'])                      ;  a = f'[{a:7}]'  ;  return f'a = {self.ftAa(self.aa)} = {a}'
    def fmtAx(   self):        x = W.join([f'{self.X_LEFT}',   f'{self.X_CENTER}', f'{self.X_RIGHT}'])                      ;  x = f'[{x:7}]'  ;  return f'x = {self.ftAx(self.ax)} = {x}'
    def fmtAy(   self):        y = W.join([f'{self.Y_BOTTOM}', f'{self.Y_CENTER}', f'{self.Y_TOP}', f'{self.Y_BASELINE}'])  ;  y = f'[{y:7}]'  ;  return f'y = {self.ftAy(self.ay)} = {y}'
    def fmtAv(   self):        v = W.join([f'{self.Y_BOTTOM}', f'{self.Y_CENTER}', f'{self.Y_TOP}'])                        ;  v = f'[{v:7}]'  ;  return f'v = {self.ftAv(self.av)} = {v}'
    def fAxy(    self, d=W, dbg=0):   (a,b) = ('ax=', 'ay=') if dbg else (Z, Z)  ;  return f'{a}{self.ftAx(self.ax)}{d}{b}{self.ftAy(self.ay)}'
    @staticmethod
    def ftAa(a):  return 'L' if a == LEFT   else 'C' if a == CENTER else 'R' if a == RIGHT else '??'
    @staticmethod
    def ftAx(a):  return 'L' if a == LEFT   else 'C' if a == CENTER else 'R' if a == RIGHT else '??'
    @staticmethod
    def ftAy(a):  return 'B' if a == BOTTOM else 'C' if a == CENTER else 'T' if a == TOP   else 'N' if a == BASELINE else '??'
    @staticmethod
    def ftAv(a):  return 'B' if a == BOTTOM else 'C' if a == CENTER else 'T' if a == TOP   else '??'
    ####################################################################################################################################################################################################
    def dumpWxHp0(self): self.log(self.fmtWHP0())
    def dumpDataSlice(self, p, l, c, cc):
        for t in range(self.n[T]):
            ikeys = self.ikeys[cc+t].text if self.ikeys and len(self.ikeys) > cc+t else Z
            kords = self.kords[cc+t].text if self.kords and len(self.kords) > cc+t else Z
            self.log(f'{self.data[p][l][c]} [{cc+t}] {self.tabls[cc+t].text:2} {self.notes[cc+t].text:2} {ikeys:2} {kords:2}')
#    @staticmethod
#    def dumpObjs(objs, name, why=Z):            [ Tabs.dumpObj(o, name, why) for o in objs ]
#    @staticmethod
#    def dumpObj( obj,  name, why=Z): slog(f'{why} {name} ObjId {id(obj):x} {type(obj)}')
    ####################################################################################################################################################################################################
    def dumpJs(  self, why, w=None, d=1):
        b = W*10 if self.OIDS else W
        self.log(f'{b}J1{self.fmtJ1(w, d)} {self.fmtAx()} {why}')
        self.log(f'{b}J2{self.fmtJ2(w, d)} {self.fmtAy()} {why}')
        self.log(f'{b}LE{self.fmtLE(w, d)} {self.fmtAv()} {why}')
    def dumpGeom(self, why=Z, why2=Z):
        b = W*10 if self.OIDS else W
        self.log(f'{b}{why:3}[{self.fmtWH()}{self.fmtD()}{self.fmtI()} {self.fss2sl()} {self.LL} {self.fzz()} {len(self.idmap):4} {self.fnvis()}] {self.fmtAa()} {why2}')
    def dumpSmap(self, why, pos=0):       self.log(f'{why} smap={fmtm(self.smap)}', pos=pos)
    ####################################################################################################################################################################################################
    def dumpBlanks(self): self.dmpBlnkHdr()  ;  self.log(f'{self.fmtBlnkCol()}', p=0)  ;  self.log(f'{self.fmtBlnkRow()}', p=0)
    def dmpBlnkHdr(self): self.log(f'{len(self.tblankCol)=} {len(self.tblankRow)=}')
    def fmtBlnkCol(self): return f'{self.tblankCol}'
    def fmtBlnkRow(self): return f'{self.tblankRow}'
    ####################################################################################################################################################################################################
    def ntp(self, dbg=0, dbg2=0):
        n = list(self.n)     ;   self.log(f'{W*9}         n={self.fmtn(Z, n)}') if dbg2 else None
        n.reverse()          ;   self.log(f'{W*9}       Rev={self.fmtn(Z, n)}') if dbg2 else None
        n = self.accProd(n)  ;   self.log(f'{W*9}   nRevPrd={fmtl(n)}')         if dbg2 else None
        n.reverse()          ;   self.log(f'{W*9}nRevPrdRev={fmtl(n)}')         if dbg2 else None
        pfx = 'tpb ' if len(n) == 5 else Z
        self.log(f'{pfx}tpp tpl tps tpc={fmtl(n)}')  if dbg else None
        return n
    def ntp2(self):
        ns = self.n[S] if self.n[S] in range(5) else 1
        if ns <= 0:  self.log(f'{ns=} ERROR set ns=1')    ;    ns = 1
        tpb, tpp, tpl, _, tpc = self.ntp()
        tpb = tpb // ns
        tpp = tpp // ns
        tpl = tpl // ns
        return tpb, tpp, tpl, tpc
    def fntp(  self, dbg=0, dbg2=0):   return fmtl(self.ntp(dbg=dbg, dbg2=dbg2))
    def fntp2( self):                  return fmtl(self.ntp2())
    ####################################################################################################################################################################################################
    @staticmethod
    def accProd(n): return list(accumulate(n, operator.mul))
    ####################################################################################################################################################################################################
    def dumpTniksA(self, why=Z):
        self.dumpTniksPfx(why)
        for v in self.idmap.values():
            self.setJdump(v[1], v[2], v[0].visible, why=why)
        self.dumpTniksSfx(why)

    def dumpTniksB(self, why=Z): # fixme
        np,  nl,  ns,  nc,  nt  = self.n
        self.dumpTniksPfx(why)
        for p in range(np):
            self.setJdump(                             P, p,            self.pages[p           ].visible, why)
            for l in range(nl):
                self.setJdump(                         L, l+p*nl,       self.lines[l+p*nl      ].visible, why)
                if self.LL:
                    self.setJdump(                     R, l+p*nl,       self.rowLs[l+p*nl      ].visible, why)
                    for q in range(nc):  self.setJdump(Q, q+p*nl*nc,    self.qclms[q+p*nl*nc   ].visible, why)
                for s, s2 in enumerate(self.ss2sl()):
                    self.setJdump(                     S, s+p*nl*ns,    self.sects[s+p*nl*ns   ].visible, why)
                    for c in range(nc):
                        self.setJdump(                 C, c+p*nl*ns*nc, self.colms[c+p*nl*ns*nc].visible, why)
                        for t in range(nt):
                            _, j, k, txt  =  self.tnikInfo(p, l, s2, c, t, why=why)
                            self.setJdump(             j, t+p*nl*nc*nt, _[t+p*nl*nc*nt         ].visible, why)
        self.setJdump(H, 0, why=why)
        self.dumpTniksSfx(why)
    ####################################################################################################################################################################################################
    def dumpTniksC(self, why=Z):
        self.dumpTniksPfx(why)   ;   m = [ len(self.C[k]) for k in range(4) ]   ;   n = [ len(self.D[k]) for k in range(4) ]
        it = list(itertools.chain(self.A))   ;   consume(consume(self.setJdump(j  , i % self.n[j], v=int(it[j][i].visible), why=why) for i in range(len(it[j]))) for j in range(len(it)))
        it = list(itertools.chain(self.B))   ;   consume(consume(self.setJdump(j+T, i % self.n[T], v=int(it[j][i].visible), why=why) for i in range(len(it[j]))) for j in range(len(it)))
        it = list(itertools.chain(self.C))   ;   consume(consume(self.setJdump(j+M, i % m[j]     , v=int(it[j][i].visible), why=why) for i in range(len(it[j]))) for j in range(len(it)))
        it = list(itertools.chain(self.D))   ;   consume(consume(self.setJdump(j+A, i % n[j]     , v=int(it[j][i].visible), why=why) for i in range(len(it[j]))) for j in range(len(it)))
        self.dumpTniksSfx(why)

    def dumpTniksD(self, why=Z):
        self.dumpTniksPfx(why)   ;   m = [ len(self.C[k]) for k in range(4) ]   ;   n = [ len(self.D[k]) for k in range(4) ]
        it = list(itertools.chain(self.A))   ;   Tabs.consMe(Tabs.consMe(self.setJdump(j  , i % self.n[j], v=int(it[j][i].visible), why=why) for i in range(len(it[j]))) for j in range(len(it)))
        it = list(itertools.chain(self.B))   ;   Tabs.consMe(Tabs.consMe(self.setJdump(j+T, i % self.n[T], v=int(it[j][i].visible), why=why) for i in range(len(it[j]))) for j in range(len(it)))
        it = list(itertools.chain(self.C))   ;   Tabs.consMe(Tabs.consMe(self.setJdump(j+M, i % m[j]     , v=int(it[j][i].visible), why=why) for i in range(len(it[j]))) for j in range(len(it)))
        it = list(itertools.chain(self.D))   ;   Tabs.consMe(Tabs.consMe(self.setJdump(j+A, i % n[j]     , v=int(it[j][i].visible), why=why) for i in range(len(it[j]))) for j in range(len(it)))
        self.dumpTniksSfx(why)
    @staticmethod
    def consMe(it):  return collections.deque(it, maxlen=0)
    def clearVisib(self):   Tabs.consMe(v.clear() for v in self.visib)
    ####################################################################################################################################################################################################
    def dumpTniksE(self, why=Z):
        ep, el, es, ec, et, en, ei, ek, em, er, eq, eh, eb, ea, ed, ee = self.lenE() #  ;   np, nl, ns, nc, nt = self.n
        self.dumpTniksPfx(why)
#       if self.LL:
#           for p in range(ep):
#               for l in range(nl):    self.setJdump(R, l+p*nl,    v=int(self.rowLs[ l+p*nl  ].visible), why=why)
#               for q in range(nl*nc): self.setJdump(Q, q+p*nl*nc, v=int(self.qclms[q+p*nl*nc].visible), why=why)
        for p in range(ep):            self.setJdump(P, p,         v=int(self.pages[    p    ].visible), why=why)
        for l in range(el):            self.setJdump(L, l,         v=int(self.lines[    l    ].visible), why=why)
        for s in range(es):            self.setJdump(S, s,         v=int(self.sects[    s    ].visible), why=why)
        for c in range(ec):            self.setJdump(C, c,         v=int(self.colms[    c    ].visible), why=why)
        for t in range(et):            self.setJdump(T, t,         v=int(self.tabls[    t    ].visible), why=why)
        for n in range(en):            self.setJdump(N, n,         v=int(self.notes[    n    ].visible), why=why)
        for i in range(ei):            self.setJdump(I, i,         v=int(self.ikeys[    i    ].visible), why=why)
        for k in range(ek):            self.setJdump(K, k,         v=int(self.kords[    k    ].visible), why=why)
        for m in range(em):            self.setJdump(M, m,         v=int(self.views[    m    ].visible), why=why)
        for r in range(er):            self.setJdump(R, r,         v=int(self.rowLs[    r    ].visible), why=why)
        for q in range(eq):            self.setJdump(Q, q,         v=int(self.qclms[    q    ].visible), why=why)
        for h in range(eh):            self.setJdump(H, h,         v=int(self.hcurs[    h    ].visible), why=why)
#       self.setJdump(                               H, 0,         v=int(self.hcurs[    0    ].visible), why=why)
        for a in range(ea):            self.setJdump(A, a,         v=int(self.anams[    a    ].visible), why=why)
        for b in range(eb):            self.setJdump(B, b,         v=int(self.bnums[    b    ].visible), why=why)
        for d in range(ed):            self.setJdump(D, d,         v=int(self.capos[    d    ].visible), why=why)
        for e in range(ee):            self.setJdump(E, e,         v=int(self.zclms[    e    ].visible), why=why)
        self.dumpTniksSfx(why)

    def dumpTniksF(self, why=Z):
        ep, el, es, ec, et, en, ei, ek, em, er, eq, eh, eb, ea, ed, ee = self.lenE() #  ;   np, nl, ns, nc, nt = self.n
        self.dumpTniksPfx(why)
#       if self.LL:
#           for p in range(ep):
#               for l in range(nl):
#                   self.setJdump(                    R, l+p*nl,    v=int(self.rowLs[ l+p*nl  ].visible), why=why)
#                   for q in range(nc): self.setJdump(Q, q+p*nl*nc, v=int(self.qclms[q+p*nl*nc].visible), why=why)
        for p in range(ep):             self.setJdump(P, p,         v=int(self.pages[    p    ].visible), why=why)
        for l in range(el):             self.setJdump(L, l,         v=int(self.lines[    l    ].visible), why=why)
        for s in range(es):             self.setJdump(S, s,         v=int(self.sects[    s    ].visible), why=why)
        for c in range(ec):             self.setJdump(C, c,         v=int(self.colms[    c    ].visible), why=why)
        for t in range(et):             self.setJdump(T, t,         v=int(self.tabls[    t    ].visible), why=why)
        for n in range(en):             self.setJdump(N, n,         v=int(self.notes[    n    ].visible), why=why)
        for i in range(ei):             self.setJdump(I, i,         v=int(self.ikeys[    i    ].visible), why=why)
        for k in range(ek):             self.setJdump(K, k,         v=int(self.kords[    k    ].visible), why=why)
        for m in range(em):             self.setJdump(M, m,         v=int(self.views[    m    ].visible), why=why)
        for r in range(er):             self.setJdump(R, r,         v=int(self.rowLs[    r    ].visible), why=why)
        for q in range(eq):             self.setJdump(Q, q,         v=int(self.qclms[    q    ].visible), why=why)
#       for h in range(eh):             self.setJdump(H, h,         v=int(self.hcurs[    h    ].visible), why=why)
        self.setJdump(                                H, 0,         v=int(self.hcurs[    0    ].visible), why=why)
        for a in range(ea):             self.setJdump(A, a,         v=int(self.anams[    a    ].visible), why=why)
        for b in range(eb):             self.setJdump(B, b,         v=int(self.bnums[    b    ].visible), why=why)
        for d in range(ed):             self.setJdump(D, d,         v=int(self.capos[    d    ].visible), why=why)
        for e in range(ee):             self.setJdump(E, e,         v=int(self.zclms[    e    ].visible), why=why)
        self.dumpTniksSfx(why)
    ####################################################################################################################################################################################################
    def dumpTniksG(self):
        self.log(Y.join(LTXA),  p=0, f=3)
        self.log(Y.join(LTXAC), p=0, f=3)
        for i, t in enumerate(self.pages):               d = t.document  ;  m = d.styles  ;  s = self.fDocStyle(m, Y, t)  ;  self.log(self.t2csv(t, P, i, Y, s), p=0, f=3)
        for i, t in enumerate(self.lines):               d = t.document  ;  m = d.styles  ;  s = self.fDocStyle(m, Y, t)  ;  self.log(self.t2csv(t, L, i, Y, s), p=0, f=3)
        for i, t in enumerate(self.sects):               d = t.document  ;  m = d.styles  ;  s = self.fDocStyle(m, Y, t)  ;  self.log(self.t2csv(t, S, i, Y, s), p=0, f=3)
        for i, t in enumerate(self.colms):               d = t.document  ;  m = d.styles  ;  s = self.fDocStyle(m, Y, t)  ;  self.log(self.t2csv(t, C, i, Y, s), p=0, f=3)
        for i, t in enumerate(self.tabls):               d = t.document  ;  m = d.styles  ;  s = self.fDocStyle(m, Y, t)  ;  self.log(self.t2csv(t, T, i, Y, s), p=0, f=3)
        for i, t in enumerate(self.notes):               d = t.document  ;  m = d.styles  ;  s = self.fDocStyle(m, Y, t)  ;  self.log(self.t2csv(t, N, i, Y, s), p=0, f=3)
        for i, t in enumerate(self.ikeys):               d = t.document  ;  m = d.styles  ;  s = self.fDocStyle(m, Y, t)  ;  self.log(self.t2csv(t, I, i, Y, s), p=0, f=3)
        for i, t in enumerate(self.kords):               d = t.document  ;  m = d.styles  ;  s = self.fDocStyle(m, Y, t)  ;  self.log(self.t2csv(t, K, i, Y, s), p=0, f=3)
        for i, t in enumerate(self.views):               d = t.document  ;  m = d.styles  ;  s = self.fDocStyle(m, Y, t)  ;  self.log(self.t2csv(t, M, i, Y, s), p=0, f=3)
        for i, t in enumerate(self.rowLs):               d = t.document  ;  m = d.styles  ;  s = self.fDocStyle(m, Y, t)  ;  self.log(self.t2csv(t, R, i, Y, s), p=0, f=3)
        for i, t in enumerate(self.qclms):               d = t.document  ;  m = d.styles  ;  s = self.fDocStyle(m, Y, t)  ;  self.log(self.t2csv(t, Q, i, Y, s), p=0, f=3)
#       for i, t in enumerate(self.hcurs):               d = t.document  ;  m = d.styles  ;  s = self.fDocStyle(m, Y, t)  ;  self.log(self.t2csv(t, H, i, Y, s), p=0, f=3)
        for i, t in enumerate(self.anams):               d = t.document  ;  m = d.styles  ;  s = self.fDocStyle(m, Y, t)  ;  self.log(self.t2csv(t, A, i, Y, s), p=0, f=3)
        for i, t in enumerate(self.bnums):               d = t.document  ;  m = d.styles  ;  s = self.fDocStyle(m, Y, t)  ;  self.log(self.t2csv(t, B, i, Y, s), p=0, f=3)
        for i, t in enumerate(self.capos):               d = t.document  ;  m = d.styles  ;  s = self.fDocStyle(m, Y, t)  ;  self.log(self.t2csv(t, D, i, Y, s), p=0, f=3)
        for i, t in enumerate(self.zclms):               d = t.document  ;  m = d.styles  ;  s = self.fDocStyle(m, Y, t)  ;  self.log(self.t2csv(t, E, i, Y, s), p=0, f=3)
#        self.setJdump(H, 0, v=int(self.hcurs[0].visible))

    def dumpTniksH(self):
        self.log(Y.join(LTXA),  p=0, f=3)
        self.log(Y.join(LTXAC), p=0, f=3)  ;  a = self.A  ;  b = self.B  ;  c = self.C    ;  e = self.D
        for i in range(len(self.pages)): t = a[0][i]  ;  d = t.document  ;  m = d.styles  ;  s = self.fDocStyle(m, Y, t)  ;  self.log(self.t2csv(t, P, i, Y, s), p=0, f=3)
        for i in range(len(self.lines)): t = a[1][i]  ;  d = t.document  ;  m = d.styles  ;  s = self.fDocStyle(m, Y, t)  ;  self.log(self.t2csv(t, L, i, Y, s), p=0, f=3)
        for i in range(len(self.sects)): t = a[2][i]  ;  d = t.document  ;  m = d.styles  ;  s = self.fDocStyle(m, Y, t)  ;  self.log(self.t2csv(t, S, i, Y, s), p=0, f=3)
        for i in range(len(self.colms)): t = a[3][i]  ;  d = t.document  ;  m = d.styles  ;  s = self.fDocStyle(m, Y, t)  ;  self.log(self.t2csv(t, C, i, Y, s), p=0, f=3)
        for i in range(len(self.tabls)): t = b[0][i]  ;  d = t.document  ;  m = d.styles  ;  s = self.fDocStyle(m, Y, t)  ;  self.log(self.t2csv(t, T, i, Y, s), p=0, f=3)
        for i in range(len(self.notes)): t = b[1][i]  ;  d = t.document  ;  m = d.styles  ;  s = self.fDocStyle(m, Y, t)  ;  self.log(self.t2csv(t, N, i, Y, s), p=0, f=3)
        for i in range(len(self.ikeys)): t = b[2][i]  ;  d = t.document  ;  m = d.styles  ;  s = self.fDocStyle(m, Y, t)  ;  self.log(self.t2csv(t, I, i, Y, s), p=0, f=3)
        for i in range(len(self.kords)): t = b[3][i]  ;  d = t.document  ;  m = d.styles  ;  s = self.fDocStyle(m, Y, t)  ;  self.log(self.t2csv(t, K, i, Y, s), p=0, f=3)
        for i in range(len(self.views)): t = c[0][i]  ;  d = t.document  ;  m = d.styles  ;  s = self.fDocStyle(m, Y, t)  ;  self.log(self.t2csv(t, M, i, Y, s), p=0, f=3)
        for i in range(len(self.rowLs)): t = c[1][i]  ;  d = t.document  ;  m = d.styles  ;  s = self.fDocStyle(m, Y, t)  ;  self.log(self.t2csv(t, R, i, Y, s), p=0, f=3)
        for i in range(len(self.qclms)): t = c[2][i]  ;  d = t.document  ;  m = d.styles  ;  s = self.fDocStyle(m, Y, t)  ;  self.log(self.t2csv(t, Q, i, Y, s), p=0, f=3)
#        for i in range(len(self.hcurs)): t = c[3][i]  ;  d = t.document  ;  m = d.styles  ;  s = self.fDocStyle(m, Y, t)  ;  self.log(self.t2csv(t, H, i, Y, s), p=0, f=3)
        for i in range(len(self.anams)): t = e[1][i]  ;  d = t.document  ;  m = d.styles  ;  s = self.fDocStyle(m, Y, t)  ;  self.log(self.t2csv(t, A, i, Y, s), p=0, f=3)
        for i in range(len(self.bnums)): t = e[0][i]  ;  d = t.document  ;  m = d.styles  ;  s = self.fDocStyle(m, Y, t)  ;  self.log(self.t2csv(t, B, i, Y, s), p=0, f=3)
        for i in range(len(self.capos)): t = e[2][i]  ;  d = t.document  ;  m = d.styles  ;  s = self.fDocStyle(m, Y, t)  ;  self.log(self.t2csv(t, D, i, Y, s), p=0, f=3)
        for i in range(len(self.zclms)): t = e[3][i]  ;  d = t.document  ;  m = d.styles  ;  s = self.fDocStyle(m, Y, t)  ;  self.log(self.t2csv(t, E, i, Y, s), p=0, f=3)
#        self.setJdump(H, 0, v=int(self.hcurs[0].visible))
    ####################################################################################################################################################################################################
    def dumpStruct(self, why=Z, dbg=1, dbg2=0):
        self.log(f'{self.fmtn()} BGN ntp={self.fntp()} {self.fntp2()} {self.fmtI()}', pos=1)
        if dbg2:    self.dumpArgs(f=2)
#        kysgs.dumpData()
        kysgs.dumpNic(self.nic)
        self.dumpFont(why)
        self.dumpVisible()
        self.dumpIdmKeys() if dbg and self.VERBY else None
#        self.dumpVisible2()
#        self.dumpTniksB(f'{why}B') if dbg else None
        if dbg2: # todo fixme some dont handle Sprites
            self.dumpTniksA(f'{why}A')
            self.dumpTniksB(f'{why}B')
            self.dumpTniksC(f'{why}C')
            self.dumpTniksD(f'{why}D')
            self.dumpTniksE(f'{why}E')
            self.dumpTniksF(f'{why}F')
            self.dumpTniksG()
            self.dumpTniksH()
        if dbg2:        self.cobj.dumpMlimap('MLim') if self.VERBY else None
        self.log(f'{self.fmtn()} END ntp={self.fntp()} {self.fntp2()} {self.fmtI()}', pos=1)
    ####################################################################################################################################################################################################
    def autoSave(self, dt, how, dbg=1):
        if dbg: self.log(f'Every {dt:=7.4f} seconds, {how} {self.rsyncData=}')
        if self.rsyncData: cmd = cmds.SaveDataFileCmd(self, how, self.dataPath0)   ;  cmd.do()  ;  self.rsyncData = 0
    ####################################################################################################################################################################################################
    def genDataFile(self, path):
        self.log(f'{path} {self.fmtn()}')
        np, nl, ns, nc, nt = self.n # ;  nc += self.zzl()
        self.dumpBlanks()
        self.data = [ [ [ self.tblankRow for _ in range(nt) ] for _ in range(nl) ] for _ in range(np) ]
        self.data = self.transposeData(dmp=1)
        cmd = cmds.SaveDataFileCmd(self, 'Generated Data', path)     ;  size = cmd.do()
        self.log(f'{path} {size=} {self.fmtdl()}')
        self.data = []
        return size
   ####################################################################################################################################################################################################
    def readDataFile(self, path, dbg=1):
        nl = self.n[L]      ;     nr = self.n[T]   ;   sp, sl, sr, st = 0, 0, 0, 0   ;   sx = 0   ;   fd = -3
        if dbg:                 self.log(f'BGN {self.fmtn()}', f=fd)
        if not path.exists():   path = utl.getFilePath(self.DAT_GFN, BASE_PATH, fdir=DATA, fsfx=Z)
        stat = path.stat()  ;   size = stat.st_size
        if size == 0:           self.log(f'WARN Zero Len Data File  {path} -> Generate Data File', f=fd)   ;   size = self.genDataFile(path)
        if size == 0:            msg =  f'ERROR Zero Len Data File {size=}'      ;   self.log(msg, f=fd)   ;   cmd = cmds.QuitCmd(self, msg)  ;  cmd.do()
        with open(path, 'r', encoding='utf-8')  as DATA_FILE:
            DATA_FILE.seek(0, 2)      ;     size = DATA_FILE.tell()   ;   DATA_FILE.seek(0, 0)
            self.log(f'{DATA_FILE.name:40} {size:3,} bytes = {size/1024:3,.1f} KB', f=fd)
            self.log('Raw Data File BGN:', f=fd)
            data = self.data          ;     lines, rows = [], []
            for TABS in DATA_FILE:
                TABS = TABS.rstrip(X)
                if TABS and TABS[0] == '#':   sx += 1
                if TABS and TABS[0] != '#':
                    ntabs = len(TABS)
                    for i in range(ntabs):
                        if  TABS[i] in self.tblanks and TABS[i] != self.tblank:    self.tblank = TABS[i]
                    rows.append(TABS)       ;      st += ntabs           ;     sr += 1
                elif rows  and not sr % nr:        lines.append(rows)    ;    rows = []   ;   sl += 1
                elif lines and not sl % nl:         data.append(lines)   ;   lines = []   ;   sp += 1
                self.log(TABS, p=0, f=fd)
            if rows:  lines.append(rows)    ;   sl += 1
            if lines: data.append(lines)    ;   sp += 1
            self.log('Raw Data File END:', f=fd)
            self.log(f'{self.fmtdl()=} {self.fmtdt()=}', f=fd)
            self.log(f'{sp=} {sl=} {sr=} {st=}', f=fd)
            np, nl, nr, nc = self.dl()
            self.checkDataFile(size, np, nl, nr, nc, sx)
            self.log(f'{sp} ({sl/nl:6.3f}) pages = {sl} lines =          {sr} rows =          {st} cols', f=fd)
            self.log(f'{np} ({sl/nl:6.3f}) pages @ {nl} lines per page, @ {nr} rows per line, @ {nc} cols per row', f=fd)
            self.dumpDataFile(data)
            self.data = self.transposeData(data, dmp=dbg)
        if dbg:         self.log(f'END {self.fmtn()}', f=fd)
   ####################################################################################################################################################################################################
    def checkDataFile(self, ref, p, l, r, c, x):
        x = x - 1 if x else x  ;  y = 2  ;  z = 1 if x else 0  ;  fd = -3  ;  w = p + p * l if not x else x
        msg =           f'{p=} {l=} {r=} {c=} {w=} {x=} {y=} {z=}'
        self.log(f'{ref=} {p=} {l=} {r=} {c=} {w=} {x=} {y=} {z=}', f=fd)
        c0 = c + y if x else 0     ;  self.log(f'{c0=:3} = 0                 = 0', f=fd) if not x else self.log(f'{c0=:3} = c + y = {c} + {y}', f=fd) 
        dl = p * l * r * (c + y)   ;  self.log(f'{dl=:3} = p * l * r * (c+y) = {p} * {l} * {r} * ({z}*{c}+{y})', f=fd)
        cl = w *   (z * c + y)     ;  self.log(f'{cl=:3} = w *       (z*c+y) = {w} * (({z} * {c}) + {y})', f=fd)
        sz = c0 + dl + cl          ;  self.log(f'{sz=:3} = c0 + dl + cl      = {c0} + {dl} + {cl}', f=fd)
        self.log(f'{ref=}', f=fd)
        assert sz == ref,      f'{sz} != {ref=}, {msg}'

    def dumpDataFile(self, data=None):
        data = self.dproxy(data)
        d0, d1, d2, d3 = self.dl()
        self.log(f'BGN {d0} pages, {d1} lines per page, {d2} rows per line, {d3} tabs per line')
        for n0, dn0 in enumerate(data):
            for n1, dn1 in enumerate(dn0):
                self.log(f'{fmtl(dn1, d=Z)}', p=0)
            self.log(p=0)
        self.log(f'END {d0} pages, {d1} lines per page, {d2} rows per line, {d3} tabs per line')
    ####################################################################################################################################################################################################
    def isVert(self, data=None, dbg=1):
        dl, dt = self.dl(data), self.dt(data)
        if dbg:  self.log(f'BGN dl={self.fmtdl()} dt={self.fmtdt()}')
        assert dt[0] is list and dt[1] is list and dt[2] is list and dt[3] is str,   f'{dl=} {dt=}'
        vert   = 1 if dl[2] >= dl[3] else 0
        self.checkData(vert=vert, data=None)
        self.log(fmtl(self.dplc()[0]), p=0)
        if dbg:  self.log(f'END dl={self.fmtdl()} dt={self.fmtdt()} {vert=}')
        return vert

    def checkData(self, vert, data=None):
        data = self.dproxy(data)   ;   dl = self.dl(data)
        for p in range(dl[0]):
            assert len(data[p]) == dl[1],   f'{len(data[p])=} {dl=} {vert=}'
            for l in range(len(data[p])):
                assert len(data[p][l]) == dl[2],   f'{len(data[p][l])=} {dl=} {vert=}'
                for c in range(len(data[p][l])):
                    assert len(data[p][l][c]) == dl[3],   f'{len(data[p][l])=} {dl=} {vert=}'
    ####################################################################################################################################################################################################
#    def transposeDataDump(self, data=None, dbg=1):
#        self.dumpDataVert(data) if self.isVert(data) else self.dumpDataHorz(data)
#        self.data = self.transposeDataA(data, dbg)
#        self.dumpDataVert(data) if self.isVert(data) else self.dumpDataHorz(data)

    def transposeData(self, data=None, dmp=0, dbg=1):
        data = self.dproxy(data)
        self.log(f'BGN {self.fmtD(data)} {dmp=}')
        if dmp > 1:     self.dumpDataVert(data) # if self.isVert(data) else self.dumpDataHorz(data)
        assert self.fmtdl() == self.fmtdl(data),     f'{self.fmtdl()} != {self.fmtdl(data)}'
        assert self.fmtdt() == self.fmtdt(data),     f'{self.fmtdt()} != {self.fmtdt(data)}'
        tpose, msg1, msg2 = [], [], []   ;   self.log(f'dl={self.fmtdl(data)} dt={self.fmtdt(data)}') if dbg else None
        for page in data:
            pageTP = []
            for line in page:
                if dbg:  msg1.append(f'{fmtl(line,   d=Z)}')
                lineTP = list(map(Z.join, itertools.zip_longest(*line, fillvalue=W)))
                if dbg:  msg2.append(f'{fmtl(lineTP, d=Z)}')
                pageTP.append(lineTP)
            tpose.append(pageTP)
        if dbg: [ self.log(m, p=0) for m in msg1 ]   ;   self.log(p=0)
        if dbg: [ self.log(m, p=0) for m in msg2 ]
        if dmp > 0:     self.dumpDataVert(tpose) # if self.isVert(tpose) else self.dumpDataHorz(tpose)
        self.log(f'END {self.fmtD(tpose)} {dmp=}')
        return tpose
    ####################################################################################################################################################################################################
    def dumpDataHorz(self, data=None, lc=1, ll=1, i=0):
        data = data or self.data
        self.log(f'BGN {self.fmtD(data)} {lc=} {ll=} {i=}')
        for p, page in enumerate(data):                       #           #  for p in range(len(data)):
##            if ll:  plt = f'{JTEXTS[P]} {p+1}'  ;  plab = f'{plt:{i+1}}'  ;  self.log(f'{W*i}{plab}', pfx=0)
            for l, line in enumerate(page):                   #           #  for l in range(len(data[p])):
                if ll:  llt = f'{JTEXTS[P]} {p+1}'  ;  llab = f'{llt:{i+1}} '  ;  self.log(f'{W*i}{llab}', p=0, e=Z)   ;   self.log(f'{JTEXTS[L]} {l+1}', p=0)
##                if ll:  llt = f'{JTEXTS[L]} {l+1}'  ;  llab = f'{llt:{i+1}}'  ;  self.log(f'{W*i}{llab}', p=0)
                if lc:  self.dumpDataLabels(line, i=i, sep=W) #           #  if lc:  self.dumpDataLabels(data[p][l], i=i, sep=W)
                for r, row in enumerate(line):                #           #  for r in range(len(         data[p][l])):
                    self.log(W*i, p=0, e=Z)
                    for c, col in enumerate(row):             #           #  for c in range(len(data[p][l][r])):
                        self.log(f'{col}', p=0, e=Z)          #           #      self.log(   f'{data[p][l][r][c]}', p=0, e=Z)
                    self.log(p=0)
                self.log(p=0)
        self.log(f'END {self.fmtD(data)} {lc=} {ll=} {i=}')

    def dumpDataVert(self, data=None, lc=1, ll=1, i=0):
        data = data or self.data   ;   line = []
        w = max(len(data[0][0][0]), len(JTEXTS[P]) + 2, len(JTEXTS[L]) + 2)   ;   txt = W * i + JTEXTS[C] + W if i >= 0 else JTEXTS[C]
        self.log(f'BGN {self.fmtD(data)} {lc=} {ll=} {i=} {w=} {txt=}')
        for p, page in enumerate(data):                       #           #  for p in range(len(data)):
            if ll: self.log(f'{JTEXTS[P]} {p+1}', p=0)  ;  self.log(f'{txt:{3}}', p=0, e=Z)  ;  txt2 = [ f'{JTEXTS[L]} {l+1}' for l, line in enumerate(page) ]  ;  self.log(f'{fmtl(txt2, w=w, d=Z)}', p=0)
#            if ll: self.log(f'{JTEXTS[P]} {p+1}', p=0)  ;  self.log(f'{txt:{3}}', p=0, e=Z)  ;  txt2 = [ f'{JTEXTS[L]} {l+1}' for l in range(len(page)) ]  ;  self.log(f'{fmtl(txt2, w=w, d=Z)}', p=0)
#            if ll: self.log(f'{JTEXTS[P]} {p+1}', p=0)  ;  self.log(f'{txt:{3}}', p=0, e=Z)  ;  txt2 = [ f'{JTEXTS[L]} {l+1}' for l in range(len(data[0])) ]  ;  self.log(f'{fmtl(txt2, w=w, d=Z)}', p=0)
            for c, col in enumerate(line):                    #           #  for c in range(len(data[p][0])):
                pfx = f'{c+1:3} ' if i >= 0 and lc else Z   ;   self.log(f'{pfx}{W*i}', p=0, e=Z)
                for l, line in enumerate(page):               #           #  for l in range(len(data[p])):
                    self.log(f'{col}', p=0, e=W)    #           #      self.log(f'{data[p][l][c]}', p=0, e=W)
                self.log(p=0)
        self.log(f'END {self.fmtD(data)} {lc=} {ll=} {i=}')
    ####################################################################################################################################################################################################
    def dumpDataLabels(self, data=None, i=0, sep='%'):
        pp = '  '  ;  qq = ' @'   ;   lz = self.zzl()
        p = pp[:] if lz > 1 else pp[:1] if lz else Z
        q = qq[:] if lz > 1 else qq[:1] if lz else Z
        data = data or self.data
        n = len(data[0]) - lz   ;   a = W * i if i else Z  ;  b = sep * n  ;  r = sep * 3
        if n >= 100:   self.log(   f'{a}{p}', p=0, e=Z)  ;  [  self.log(f'{c//100}'   if c>=100 else W, p=0, e=Z) for c in range(1, n+1) ]  ;  self.log(p=0)
        if n >= 10:    self.log(   f'{a}{p}', p=0, e=Z)  ;  [  self.log(f'{c//10%10}' if c>=10  else W, p=0, e=Z) for c in range(1, n+1) ]  ;  self.log(p=0)
        self.log(                  f'{a}{q}', p=0, e=Z)  ;  [  self.log(f'{c    %10}',                  p=0, e=Z) for c in range(1, n+1) ]  ;  self.log(p=0)
        if sep != Z:   self.log(f'{a}{r}{b}', p=0)
    ####################################################################################################################################################################################################
    def createLabelText(self):
        self.labelTextA.extend(f'{j}' for j in range(1, self.n[C] + 1))
        self.labelTextB.extend(f'{j%10}' if j % 10 else f'{j // 10 % 10}' for j in range(1, self.n[C] + 1))
        self.log(f'labelTextA={fmtl(self.labelTextA, w=2)}', p=0)
        self.log(f'labelTextB={fmtl(self.labelTextB, w=2)}', p=0)
        texts = list(zip(self.labelTextA, self.labelTextB))
        self.log(f'texts={fmtl(texts)}', p=0)
        self.dumpLabelText(texts)

    def dumpLabelText(self, t, d='%', why=Z, dbg=0):
        self.log(f'{why} {len(t)=} {len(t[0])=}')
        for tj in t:     self.log(f'{tj[0]:^3}', p=0, e=W)
        self.log(p=0)
        for _ in range(len(t)//10):
            for i in range(9): self.log(f'{W:^3}', p=0, e=W)
            self.log(f' {d} ', p=0, e=W)
        self.log(p=0)
        for tj in t:     self.log(f'{tj[1]:^3}', p=0, e=W)
        self.log(p=0)
        if dbg:
            for i, ti in enumerate(t):
                self.log(f'{i+1:5}', p=0, e=W)
                self.log(f' {ti[0]:>5}', p=0, e=W)
                d2 = W if i == 1 or (i + 1) % 10 else d
                self.log(f'{d2}{ti[1]:>5}', p=0, e=W)
                self.log(p=0)
    ####################################################################################################################################################################################################
    def togZZ(self, zz, why=Z):
        self.dumpGeom('BFR', why)
        self.ZZ.append(zz) if zz not in self.ZZ else self.ZZ.remove(zz)
        n = self.n[C] # + self.zzl()
        self.dumpGeom('AFT', why)
        return n

    def togLL(self, why=Z):
        self.dumpGeom('BFR', why)
        self.LL = int(not self.LL)
        self.dumpGeom('AFT', why)

    def togTT(self, tt, why=Z):
        self.dumpGeom('BFR', why)
        self.SS.add(tt) if tt not in self.SS else self.SS.remove(tt)
        self.n[S] = self.ssl()
        self.dumpGeom('AFT', why)
    ####################################################################################################################################################################################################
    def addZZs( self, z, how):
        pi = self.J1[S]  ;  zz = self.ZZ  ;  l = len(zz)  ;  az = self.addingZ  ;  why = f'Add{self.addC+1}'  ;   assert(l in (0, 1, 2)),  f'{l=} zz={fmtl(zz)} {z=}'  ;  assert z in (0, 1),  f'{z=}'
        assert z in (0, 1), f'{how} {why} {az=} {z=} zz={fmtl(zz)}'
        self.log(f'BFR {how} {why} {l=} {pi=} {self.addC=} {az=} {z=} zz={fmtl(zz)}')
        if z not in zz:    zz.append(z)     ;     l = len(zz)  ;  self.addC += 1  ;  self.addingZ = 1  ;   assert(l in (1, 2)),  f'{l=} zz={fmtl(zz)} {z=}'
        self.log(f'AFT {how} {why} {l=} {pi=} {self.addC=} {az=} {z=} zz={fmtl(zz)}')
#        self.updView(len(self.ZZ), self.LL * self.n[L])
        self.dumpTniksPfx(why)
        for s, sect in enumerate(self.sects):
            self.setJdump(S, s, sect.visible, 'Ref ')
            self.createZZs(sect, z, why)
        self.dumpTniksSfx(why)

    def createZZs(self, pt, z, why, dbg=1):
        pi = self.J1[S]   ;   zz = self.ZZ  ;  l = len(zz)  ;  az = self.addingZ  ;  assert l in (1, 2),  f'{l=} {zz=} {z=} {pi=}'  ;  assert z in (0, 1),  f'{z=} {zz=} {pi} {l=}'
        np, nl, ns, nc, nt       = self.n
        kz = self.k[E]    ;   kk = self.cci(E, pi, kz) if self.CHECKERED else 0  ;  k = kz[kk]
        _, _, xx, yy, ww, hh     = self.geom(E, None, 1, pi, dbg)
        nic, t2n,  t, yy, hh     = self.nic, self.sobj.tab2nn, '0', pt.y, pt.height
        if   l==1:             e = self.createTnik(self.zclms, pi, E, xx, yy, ww, hh, k, why, v=1, dbg=dbg)
        else:                  e = self.zclms[pi]
        x0 = xx if l==1 else xx - ww/4    ;    x1 = xx if l==1 else xx + ww/4
        if   z==0:
            if   pi in (0, 2):     ii, _, x, y, w, h = self.geom(A, e, nt, self.i[L], dbg)
            else:                  ii, _, x, y, w, h = self.geom(B, e, nt, self.i[L], dbg)
            self.log(f'    @ Z {why} {l=} {pi=} {self.addC=} {az=} {z=} zz={fmtl(zz):5} {ww=:6.2f} {ww/4=:6.2f} {x=:6.2f} {x0=:6.2f} {x1=:6.2f} {w=:6.2f} {ww/l=:6.2f}')
            for i in range(ii):
                if   pi in (0, 2): self.createTnik(self.anams, i, A, x0, y-i*h, ww/l, h, k, why, t2n(t, i, nic=nic), 1, dbg) # Notes.type?
                elif pi in (1, 3): self.createTnik(self.bnums, i, B, x0, y-i*h, ww/l, h, k, why, str(1+i),           1, dbg)
            if l==2:
                for capo in self.capos: capo.x = xx + ww/4  ;  capo.w = ww/l
        elif z==1:
            ii, _, x, y, w, h    = self.geom(D, e, nt, self.i[L], dbg)
            self.log(f'    @ Z {why} {l=} {pi=} {self.addC=} {az=} {z=} zz={fmtl(zz):5} {ww=:6.2f} {ww/4=:6.2f} {x=:6.2f} {x0=:6.2f} {x1=:6.2f} {w=:6.2f} {ww/l=:6.2f}')
            for i in range(ii):    self.createTnik(self.capos, i, D, x1, y-i*h, ww/l, h, k, why, self.sobj.capo[i], 1, dbg)
            if l==2:
                for anam in self.anams: anam.x = xx - ww/4  ;  anam.w = ww/l
                for bnum in self.bnums: bnum.x = xx - ww/4  ;  bnum.w = ww/l
    ####################################################################################################################################################################################################
    def removeZZs(self, z, how, dbg=1):
        pi = self.J1[S]  ;  zz = self.ZZ  ;  l = len(zz)  ;  az = self.addingZ  ;  why = f'Rmv{self.hidC+1}'  ;   assert(l in (0, 1, 2)),  f'{l=} zz={fmtl(zz)} {z=}'  ;  assert z in (0, 1),  f'{z=}'
        np, nl, ns, nc, nt     = self.n
        self.log(f'BFR {how} {why} {l=} {pi=} {self.hidC=} {az=} {z=} zz={fmtl(zz)}')
        zz.remove(z)     ;     l = len(zz)  ;  self.hidC += 1  ;  self.addingZ = 0  ;   assert(l in (0, 1)),  f'{l=} zz={fmtl(zz)} {z=}'
        self.log(f'AFT {how} {why} {l=} {pi=} {self.hidC=} {az=} {z=} zz={fmtl(zz)}')
        zclms, anams, bnums, capos = self.zclms, self.anams, self.bnums, self.capos
#        self.updView(l, self.LL * nl)
        self.dumpTniksPfx(why)
        _, _, xx, yy, ww, hh   = self.geom(E, None, 1, pi, dbg)
        x0 = xx if l==1 else xx - ww/4    ;    x1 = xx if l==1 else xx + ww/4
        if   z==0:
            for s in range(ns):
                if l == 0:                 self.removeTnik(zclms, s, E)
                if not s%2:
                    for a in range(nt):    self.removeTnik(anams, a+s//2*nt, A)
                else:
                    for b in range(nt):    self.removeTnik(bnums, b+s//2*nt, B)
                if capos:
                    t, _, x, y, w, h =     self.geom(D, zclms[s], nt, self.i[L], dbg)
                    for i in range(nt):
                        if capos[i+s*nt].visible: capos[i+s*nt].x = x1  ;  capos[i+s*nt].w = ww/l # self.updateTnik(capos, i, D, x1, y-i%nt*h, ww/l if l else w, h, how, dbg) if capos[i+s*nt].visible else None
        elif z==1:
            for s in range(ns):
                if l == 0:                 self.removeTnik(zclms, s, E)
                for     c in range(nt):    self.removeTnik(capos, c+s*nt, D)
                if anams and bnums:
                    t, _, x, y, w, h =     self.geom(D, zclms[s], nt, self.i[L], dbg) #  ;   p = pi*t   ;   q = (pi+1)*t
                    for i in range(nt): 
                        if anams[i+s//2*nt].visible: anams[i+s//2*nt].x = x0  ;  anams[i+s//2*nt].w = ww/l # self.updateTnik(anams, i, A, x0, y-i%nt*h, ww/l if l else w, h, how, dbg) if anams[i+s//2*nt].visible else None
                    for i in range(nt):
                        if bnums[i+s//2*nt].visible: bnums[i+s//2*nt].x = x0  ;  bnums[i+s//2*nt].w = ww/l # self.updateTnik(bnums, i, B, x0, y-i%nt*h, ww/l if l else w, h, how, dbg) if bnums[i+s//2*nt].visible else None
        self.dumpTniksSfx(why)

    def updateZZs(self, pt, s, z, why, dbg=1, dbg2=1):
        pi = self.J1[S]  ;  zz = self.ZZ  ;  l = len(zz)  ;  az = self.addingZ  ;  assert l in (1, 2),  f'{l=} {zz=} {z=} {pi=}'
#        self.updView(l, self.LL * self.n[L])
        np, nl, ns, nc, nt     = self.n
        _, _, xx, yy, ww, hh   = self.geom(E, None, 1, pi, dbg2)
        p, q,     yy,     hh   = pi//2, pi//2+1, pt.y, pt.height
        e                      = self.updateTnik(self.zclms, pi, E, xx, yy, ww, hh, why, dbg)
        x0 = xx if l==1 else xx - ww/4    ;    x1 = xx if l==1 else xx + ww/4
        if self.anams and self.bnums:
            if   pi in (0, 2):     t, _, x, y, w, h = self.geom(A, e, nt, self.i[L], dbg2)
            else:                  t, _, x, y, w, h = self.geom(B, e, nt, self.i[L], dbg2)
            self.log(f'    @ Z {why} {l=} {pi=} {self.addC=} {az=} {z=} zz={fmtl(zz):5} {ww=:6.2f} {ww/4=:6.2f} {x=:6.2f} {x0=:6.2f} {x1=:6.2f} {w=:6.2f} {ww/l=:6.2f}')
            for i in range(p*t, q*t):
                if   not s % nt:   self.updateTnik(self.anams, i, A, x0, y-i%nt*h, ww/l, h, why, dbg) if self.anams[i].visible else None
                else:              self.updateTnik(self.bnums, i, B, x0, y-i%nt*h, ww/l, h, why, dbg) if self.bnums[i].visible else None
        if self.capos:
            t, _, x, y, w, h =     self.geom(D, e, nt, self.i[L], dbg2)   ;   p = pi*t   ;   q = (pi+1)*t
            self.log(f'    @ Z {why} {l=} {pi=} {self.addC=} {az=} {z=} zz={fmtl(zz):5} {ww=:6.2f} {ww/4=:6.2f} {x=:6.2f} {x0=:6.2f} {x1=:6.2f} {w=:6.2f} {ww/l=:6.2f}')
            for i in range(p, q):
                if self.capos[i].visible:                    self.updateTnik(self.capos, i, D, x1, y-i%nt*h, ww/l, h, why, dbg)
    ####################################################################################################################################################################################################
    def createLLs(self, p, pi, why, dbg=1, dbg2=1):
        np, nl, ns, nc, nt = self.n
        n    = ns * nt # + self.LL
        kl   = self.k[R]               ;   kk = self.cci(R, pi, kl) if self.CHECKERED else 0
        rn, ri, rx, ry, rw, rh = self.geom(R, p, n, self.i[L], dbg=dbg2)
        txt  = self.dbgTabTxt(R, pi)   ;    k = kl[kk]
        v    = 1 if self.j()[P] == pi else 0
        lrow = self.createTnik(self.rowLs, pi, R, rx, ry, rw, rh, k, why=why, t=txt, v=v, dbg=dbg)
        cn, ci, cx, cy, cw, ch = self.geom(Q, lrow, self.n[C], self.i[C], dbg=dbg2)
        for c in range(cn):
            self.createLL(self.qclms, pi, c, cx, cy, cw, ch, v, why)
        return p

    def createLL(self, tlist, l, c, x, y, w, h, v, why, dbg=1):
        cc   = c + self.n[C] * l
        kl   = self.llcolor(cc, Q)  ;  kk = NORMAL_STYLE   ;   k = kl[kk]
        text = self.llText
        txt  = text[c]
        ll   = self.createTnik(tlist, cc, Q, x + c*w, y, w, h, k, why=why, t=txt, v=v, dbg=dbg)
        self.setLLStyle(cc, kk)
        return ll

    def updateLLs(self, p, v, why, dbg=1, dbg2=1):
        np, nl, ns, nc, nt = self.n
        n    = ns * nt # + self.LL
        rn, ri, rx, ry, rw, rh = self.geom(R, p, n, self.i[L], dbg=dbg2)
        lrow = self.updateTnik(self.rowLs, self.J2[R], R, rx, ry, rw, rh, why=why, dbg=dbg)  ;  lrow.visible = v
        cn, ci, cx, cy, cw, ch = self.geom(Q, lrow, self.n[C], self.i[C], dbg=dbg2)
        for c in range(cn):
            qclm = self.updateTnik(self.qclms, self.J2[Q], Q, cx + c*cw, cy, cw, ch, why=why, dbg=dbg)  ;  qclm.visible = v  
        return p
    ####################################################################################################################################################################################################
    def addLLs(self, how):
        why = f'Add'  ;  why2 = f'{how} Add' # 'Ref'
        self.dumpTniksPfx(why2)
        self.setView()
#        self.updView(len(self.ZZ), self.LL * self.n[L])
        pn, pi, px, py, pw, ph = self.geom(P, None, dbg=1)  ;  pi = 0  ;  p = self.pages[pi]
        self.updateTnik(self.pages, pi, P, px, py, pw, ph, why, dbg=1)
        if self.isJV(P):
            ln, li, lx, ly, lw, lh = self.geom(L, p, dbg=1)
            for li in range(ln):
                self.updateTnik(self.lines, li, L, lx, ly, lw, lh, dbg=1)  ;  l = self.lines[li]
                if len(self.rowLs) <= li+1: self.createLLs(l, li, why)
                elif   self.rowLs:          self.updateLLs(l, 1,  why)
        self.dumpTniksSfx(why2)

    def hideLLs(self, how):
        msg = f'{how} Hid'
        self.dumpTniksPfx(msg)
        self.setView()
        for r, rowl in enumerate(self.rowLs): self.removeTnik(self.rowLs, r, R)
        for q, qclm in enumerate(self.qclms): self.removeTnik(self.qclms, q, Q)
        self.dumpTniksSfx(msg)
    ####################################################################################################################################################################################################
#    def sprite2LabelPos(self, x, y, w, h, dbg=0): x0 = x  ;  y0 = y  ;  x += w/2  ;  y -= h/2  ;  self.log(f'{x0=:6.2f} {y0=:6.2f}, {w/2=:6.2f} {-h/2=:6.2f}, {x=:6.2f} {y=:6.2f} {self.p0x=:6.2f} {self.p0y=:6.2f}', so=1) if dbg else None  ;  return x, y
    ####################################################################################################################################################################################################
    def z1(self, c=None):  return None if c is None else C1 if C1 in self.ZZ and c == C1 else C2 if C2 in self.ZZ and c == C1 else None
    def z2(self, c=None):  return None if c is None else C2 if C2 in self.ZZ and c == C2 else None
    @staticmethod
    def lens2n(ls):        return [len(i) if ist(i, str) else i for i in ls]
    ####################################################################################################################################################################################################
    def tnikInfo(self, p, l, s, c, t=None, z=0, why=Z, dbg=0):
        tlist, j, k, txt = None, -1, None, None   ;   z1, z2 = None, None
        if z: z1, z2 = self.z1(c), self.z2(c)
        exp1 = z1 == C1   ;  exp2 = C2 in (z1, z2)
        s %= T # and 0 <= s < self.n[S]
        assert 0 <= p < self.n[P] and 0 <= l < self.n[L] and 0 <= c < self.n[C] and 0 <= t < self.n[T],  f'{self.n=} {self.fplsct(p, l, s, c, t)=}'
        assert s in (TT, NN, II, KK),  f'{s=}' # breaks when n[L] > 1
        msg1 = f'{self.fplsct( p, l, s, c, t)=} {z1=} {z2=} {exp1=} {exp2=} {txt=} {why}'
        msg2 = f'ERROR Invalid sect {s=}:'
        if   t is None:
            if   s == TT:  tlist, j = (self.anams, A) if exp1 else (self.capos, D) if exp2 else (self.tabls, T)
            elif s == NN:  tlist, j = (self.bnums, B) if exp1 else (self.capos, D) if exp2 else (self.notes, N)
            elif s == II:  tlist, j = (self.anams, A) if exp1 else (self.capos, D) if exp2 else (self.ikeys, I)
            elif s == KK:  tlist, j = (self.bnums, B) if exp1 else (self.capos, D) if exp2 else (self.kords, K)
            else:   msg = f'{msg2} {msg1}'   ;    self.log(msg)   ;   cmd = cmds.QuitCmd(self, msg)  ;  cmd.do()
            if dbg: msg =        f'{msg1}'   ;    self.log(msg, f=0)
        else:
            kT, kN, kI, kK = self.k[T], self.k[N], self.k[I], self.k[K]   ;   kO, kA, kD = self.k[B], self.k[A], self.k[D]
            tab = self.data[p][l][c][t] if C1 != z1 != C2 and C2 != z2 else Z
            if   s == TT:  tlist, j, k, txt = (self.anams, A, kA, self.sobj.names[t]) if exp1 else (self.capos, D, kD, self.sobj.capo[t]) if exp2 else (self.tabls, T, kT, tab)
            elif s == NN:  tlist, j, k, txt = (self.bnums, B, kO, self.sobj.numbs[t]) if exp1 else (self.capos, D, kD, self.sobj.capo[t]) if exp2 else (self.notes, N, kN, tab)
            elif s == II:  tlist, j, k, txt = (self.anams, A, kA, self.sobj.names[t]) if exp1 else (self.capos, D, kD, self.sobj.capo[t]) if exp2 else (self.ikeys, I, kI, tab)
            elif s == KK:  tlist, j, k, txt = (self.bnums, B, kO, self.sobj.numbs[t]) if exp1 else (self.capos, D, kD, self.sobj.capo[t]) if exp2 else (self.kords, K, kK, tab)
            if dbg: msg =        f'{msg1}'  ;  self.log(msg, f=0)
        return tlist, j, k, txt
    ####################################################################################################################################################################################################
    def geom(self, j, p=None, n=None, i=None, dbg=0):
        assert j in (P, L, S, C,  T, N, I, K,  M, R, Q, H,  A, B, D, E),  f'{j=}'
        n = n  if n is not None else self.n[j] if j <= T else self.n[T]   ;   c = (C, Q, E)   ;   e = (A, B, D, E, M)   ;   t = (T, N, I, K)
        if j in e:     vx, vy, vw, vh = 0, 0, self.viewX, self.height - self.viewY 
        else:          vx, vy, vw, vh = self.viewX, self.viewY, self.viewW, self.viewH
        np, nl, ns, nc, nt = self.n #  ;   nsnt = ns*nt #  ;   nr = nsnt * nl + self.LL   ;   dn = nr - nsnt
        if   n == 0:     n = 1        ;   self.log(f'ERROR n=0 setting {n=}')
        i                  = i if i is not None else self.i[j] if j <= T else self.i[T]
        a, b               = self.axWgt(self.ax), self.ayWgt(self.ay)   ;   d = 1-b
        px, py, pw, ph     = (a*vw, b*vh if nl==1 else vy, vw, vh) if p is None else (p.x, p.y, p.width, p.height)
        if   j in c:     w = pw/n             ;  h = ph
        elif j == P:     w = pw               ;  h = ph       ;    px += vx # ;  py -= vy
        elif j in t:     w = pw               ;  h = ph/n # - dn*ph/nr
        else:            w = pw               ;  h = ph/n
        if   j in c:     x = vx        + a*w  ;  y = py + b*ph - b*h
        elif j == R:     x = px - a*pw + a*w  ;  y = self.height - h/2 if not self.J1[L] else self.height/2 - h/2
        elif j in t:     x = px - a*pw + a*w  ;  y = py + d*ph - d*h # - dn*ph/nr #  ;   self.log(f'{a=} {b=} {d=:.1f} {dn=} [{vx:7.2f} {vy:7.2f} {vw:7.2f} {vh:7.2f}] {ph:6.2f} {ph/n=:6.2f} [{x:7.2f} {y:7.2f} {w:7.2f} {h:7.2f}] {self.SS=} {self.ZZ=}')
        else:            x = px - a*pw + a*w  ;  y = py + d*ph - d*h
        if dbg and self.VERBY >= 2:
            msg  = f'{j=:2} {JTEXTS[j]:4} {n=:2} {self.fxywh(x, y, w, h)}'
            msg2 = f' : {self.ftxywh(p)}' if p else f' : {self.fxywh(0, 0, 0, 0)}'
            msg += msg2 if p else W * len(msg2)
            self.log(f'{msg} {self.fmtJ1(0, 1)} {self.fmtJ2(0, 1)} {x} {px} {-a*pw} {a*w}', p=0, f=0)
        return n, i, x, y, w, h
    ####################################################################################################################################################################################################
    def dbgTabTxt(self, j, i):
        dt = self.DBG_TABT
        if   dt==0:  return Z
        i2 = (i + 1) % 10 if j==C else i + 1
        d  = X if j==C else Z   ;   k = d.join(f'{i2}')  ;  s, t, u = JTEXTS[j], JTEXTS2[j], jTEXTS[j]
        if   dt==1:  a = 1         ;   b = f'{0x2588:c}'                        ;   return d.join(b*a)
        elif dt==2:  a = j+1       ;   b = f'{0x2588:c}'                        ;   return d.join(b*a)
        elif dt==3:  a = 4         ;   b = f'{0x2588:c}'                        ;   return d.join(b*a)
        elif dt==4:  a = 1         ;   e = d.join([ s[_] for _ in range(a) ])   ;   return d.join([e, k])
        elif dt==5:  a = j+1       ;   e = d.join([ s[_] for _ in range(a) ])   ;   return d.join([e, k])
        elif dt==6:  a = 4         ;   e = d.join([ s[_] for _ in range(a) ])   ;   return d.join([e, k])
        elif dt==7:  a = 1         ;   e = d.join([ t[_] for _ in range(a) ])   ;   return d.join([e, k])
        elif dt==8:  a = j+1       ;   e = d.join([ t[_] for _ in range(a) ])   ;   return d.join([e, k])
        elif dt==9:  a = 4         ;   e = d.join([ t[_] for _ in range(a) ])   ;   return d.join([e, k])
        elif dt==10: a = 1         ;   e = d.join([ u[_] for _ in range(a) ])   ;   return d.join([e, k])
        elif dt==11: a = j+1       ;   e = d.join([ u[_] for _ in range(a) ])   ;   return d.join([e, k])
        elif dt==12: a = 4         ;   e = d.join([ u[_] for _ in range(a) ])   ;   return d.join([e, k])
    ####################################################################################################################################################################################################
    @staticmethod
    def fDocStyle(m, d, t):
        lnsp = NONE if m[LNSP] is None else f'{m[LNSP]:4}'   ;  txt = t.document.text  ;  clr = utl.fColor(m[COLOR])  ;  bgc = utl.fColor(m[BGC] if BGC in m else None)  ;  ml = int(t.multiline) if t else '?'
        return d.join([f'{fmtf(m[FONT_SIZE], 4)}', f'{m[LEAD]:4}', lnsp, f'{txt:8}', clr,                 bgc,           f'{m[BOLD]}', f'{m[ITALIC]}', f'{m[STRH]}', f'{ml}', f'{int(m[WRAP_LINES])}', f'{m[WRAP][0]}', f'{m[FONT_NAME]:21}'])
    @staticmethod
    def docStyleH(d=W):       return d.join(['FnSz', 'Lead', 'LnSp', 'TablText', ' ForegroundColor ', ' BackgroundColor ', 'B',          'I',            'S',         'M',          'W',                 'w',          'FontName             '])
    ####################################################################################################################################################################################################
    def imap2ikey(self, tobj, imap, i, j, dbg=0):
        imap0 = imap[0][::-1] if imap and len(imap) else []
        ff = self.sobj.isFret(tobj)
        assert ist(j, int),  f'{j=} {type(j)=}'
        if imap0 and len(imap0) > i:  ikey = tobj if j > K else imap0[i] if ff else self.tblank
        else:                         ikey = tobj if j > K else self.tblank
        if dbg: self.log(f'{ikey=} {i=} {j=} {ff=} {imap0=}')
        return ikey

    def imap2Chord(self, tobj, imap, i, j, dbg=0):
        chunks    = imap[4]  if (imap and len(imap) > 4) else []
        chordName = tobj     if j > K else chunks[i] if len(chunks) > i else self.tblank
        if dbg and chunks:   self.log(f'{chordName=} chunks={fmtl(chunks)} imap={fmtl(imap)}')
        return chordName
    ####################################################################################################################################################################################################
    def nlnsnt( self):    return self.n[L] * len(self.SS) * self.n[T]
    def axyWgt(self, x, y, dbg=0): u, v = self.axWgt(x), self.ayWgt(y)  ;  self.log(f'{x=:6} {y=:6} {u=:4.2f} {v=:4.2f}') if dbg else None  ;  return u, v
    @staticmethod
    def axWgt(x): return 0.0 if x==LEFT   else 0.5 if x==CENTER else 1.0 if x==RIGHT else -1.0
    @staticmethod
    def ayWgt(y): return 0.0 if y==BOTTOM else 0.5 if y==CENTER else 1.0 if y==TOP   else -1.0
    def fancXY(self, t): return f'{int(t.width * self.axWgt(self.ax)):5}', f'{int(t.height * self.ayWgt(self.ay)):5}'
    ####################################################################################################################################################################################################
    def checkTnik(self, t, i, j, dbg=0, dbg2=0):
        ntvH       = 'Name  Tid V'  ;  axy2H = self.axy2H()  ;  cwhH, acvaH, adsH, dsH, ftxtH = Z, Z, Z, Z, Z  ;  cwh, acva, ads, s = Z, Z, Z, Z  ;  ptxtH, ftxtH = ' PrtTxt', ' FullText'
        if ist(t, LBL):  cwhH = f'{self.cwhH()}'  ;  acvaH = f'{self.acvaH()}'  ;  dsH = f'{self.docStyleH()}'  ;  adsH = W.join(ADS)
        if i==0 and j==0:     self.log(f'{ntvH}{ptxtH} {axy2H} {cwhH} {adsH} {acvaH} {dsH}{ftxtH}', p=0, f=0)  if j==P or (j==T and i==0) else None
        ptxt, ftxt = Z, Z  ;  js = JTEXTS[j]   ;   v = 'V' if t.visible else 'I'
#        ax,     ay = self.ax,    self.ay
#        tax,   tay = t.anchor_x, t.anchor_y
        ancX, ancY = self.fancXY(t)
        if ist(t, LBL):
            d      = t.document  ;  m = d.styles  ;  wrap = 'char' # ;  aa = self.aa  ;  taa = m[ALIGN]  ;  ml = self.MULTILINE  ;  tml = int(t.multiline)
#            assert tax == ax,  f'{tax=} != {ax=} {i=} {j=}'  ;  assert tay == ay,  f'{tay=} != {ay=}'  ;  assert taa == aa,  f'{taa=} != {aa=}'  ;  assert tml == ml,  f'{tml=} != {ml=}'
            d.set_paragraph_style(0, len(d.text), {LNSP:None, LEAD:0, WRAP:wrap, WRAP_LINES:True})
            fnt    = d.get_font()   ;   asc, dsc = fnt.ascent, fnt.descent   ;   sad = asc + abs(dsc)    ;   ptxt, ftxt = f'{self.fpTxt(t)}', self.ffTxt(t) # todo descent value seems to be negative?
            cwh    = self.fcwh(t)   ;   acva = self.acvaH()   ;   ads = self.fads(asc, dsc, sad, W)   ;   s = self.fDocStyle(m, W, t)
            if dbg:
                if m and FONT_NAME in m:
                    fnt2 = pygfont.load(m[FONT_NAME], m[FONT_SIZE])
                    assert fnt.name == fnt2.name,  f'ERROR loading font, {m[FONT_NAME]=} {fnt=} {fnt2=}'
                    assert fnt.size == fnt2.size,  f'ERROR loading font, {m[FONT_SIZE]=} {fnt=} {fnt2=}'
#                   assert fnt == fnt2,            f'ERROR loading font, {fnt=} {fnt2=}'  #todo why does this assert? (stretch mismatch, address)
                else: msg = f'ERROR {FONT_NAME} not in {m=}'    ;    self.log(msg)    ;    cmd = cmds.QuitCmd(self, msg)  ;  cmd.do()
        if dbg2:      self.log(f'{js} {i+1:4} {v} {ptxt}{self.fAxy()} {ancX} {ancY} {cwh} {ads} {acva} {s} {ftxt}', p=0, f=0)
#        if ist(t, LBL) and dbg and m and FONT_NAME in m:    fnt2 = pygfont.load(m[FONT_NAME], m[FONT_SIZE])    ;    assert fnt == fnt2,  f'{fnt=} != {fnt2=}'
    ####################################################################################################################################################################################################
    def ss2sli(self, n):
        s = self.ss2sl()   ;   i, v = None, None
        for i, v in enumerate(s):
            if v==n: return i
        assert 0,  f'{n=} {s=} {i=} {v=}'
#        return None
    @staticmethod
    def sectName(s):
        s1, s2, s3 = '.', s[-2:-1], s[-1]
        return s1 + s3 if s2=='^' else s1 + s3.lower()
    ####################################################################################################################################################################################################
    def hideTTs(self, how, ii, dbg=0):
        ss = self.sectName(how)
        hid2 = f'Hid{ss} {how} {ii=}'  ;  hid = f'Hid{ss}'   ;   upd = 'Upd'   ;   ref = f'Ref{ss}'
        i = self.ss2sli(ii)
        np, nl, ns, nc, nt = self.n
        self.dumpTniksPfx(hid2)
        for p, page in         enumerate(self.g_newUpdTniks(P,                  nw=0, pt=None, why=ref)):
            for l, line in     enumerate(self.g_newUpdTniks(L,                  nw=0, pt=page, why=ref)):
                for s, sect in enumerate(self.g_newUpdTniks(S,                  nw=2, pt=line, why=hid)): # s=ii
                    if s == i:
                        for c, colm in  enumerate(self.g_newUpdTniks(C, m=i*nc, nw=2, pt=sect, why=hid)):
                            for t, _ in enumerate(self.g_newUpdTniks(s+4,       nw=2, pt=colm, why=hid)):  pass # s=ii
        self.dumpTniksSfx(hid2)
        self.togTT(ii)
        self.dumpTniksPfx(hid2)
        for page in                      self.g_newUpdTniks(P,          nw=0, pt=None, why=upd, dbg=1):
            for line in                  self.g_newUpdTniks(L,          nw=0, pt=page, why=upd, dbg=1):
                for s, sect in enumerate(self.g_newUpdTniks(S,          nw=0, pt=line, why=upd, dbg=1)):
                    for colm in          self.g_newUpdTniks(C, m=i*nc,  nw=0, pt=sect, why=upd, dbg=1):
                        for _ in         self.g_newUpdTniks(s+4,        nw=0, pt=colm, why=upd, dbg=1): pass # s=z()[s]
        if ii == TT:                     self.removeTnik(self.hcurs, 0, H, dbg)
        self.dumpTniksSfx(hid2)
        return ss
    ####################################################################################################################################################################################################
    def addTTs(self, how, ii):
        ss = self.sectName(how)
        add2 = f'Add{ss} {how} {ii=}'  ;  add = f'Add{ss}'   ;   upd = 'Upd'   ;   ref = f'Ref{ss}'
        self.togTT(ii)
        i = self.ss2sli(ii)
        np, nl, ns, nc, nt = self.n
        self.dumpTniksPfx(add2)
        for page in                      self.g_newUpdTniks(P,         nw=0, pt=None, why=ref, dbg=1):
            for line in                  self.g_newUpdTniks(L,         nw=0, pt=page, why=ref, dbg=1):
                for s, sect in enumerate(self.g_newUpdTniks(S,         nw=1, pt=line, why=add, dbg=1)):
                    if s == i:
                        for colm in      self.g_newUpdTniks(C, m=i*nc, nw=1, pt=sect, why=add, dbg=1): 
                            for _ in     self.g_newUpdTniks(s+4,       nw=1, pt=colm, why=add, dbg=1): pass # s=z()[i]
        self.dumpTniksSfx(add2)
        self.dumpTniksPfx(add2)
        for page in                      self.g_newUpdTniks(P,         nw=0, pt=None, why=ref, dbg=1):
            for line in                  self.g_newUpdTniks(L,         nw=0, pt=page, why=ref, dbg=1):
                for s, sect in enumerate(self.g_newUpdTniks(S,         nw=0, pt=line, why=upd, dbg=1)):
                    for colm in          self.g_newUpdTniks(C, m=i*nc, nw=0, pt=sect, why=upd, dbg=1):
                        for _ in         self.g_newUpdTniks(s+4,       nw=0, pt=colm, why=upd, dbg=1): pass # s=z()[s]
        if self.tabls and not self.cursor: self.createCursor(add)
        self.dumpTniksSfx(add2)
        return ss
    ####################################################################################################################################################################################################
    def createTniks(self, dbg=1):
        self.newC += 1  ;  why = f'New{self.newC}'  ;  ll = self.LL  ;  view = self.VIEW  ;  np, nl, ns, nc, nt = self.n
        self.dumpTniksPfx(why)
        if   self.DSP_J_LEV == P:
            for _ in                     self.g_createTniks(self.pages, P, None, why=why):  pass
        elif self.DSP_J_LEV == L:
            for page in                  self.g_createTniks(self.pages, P, None, why=why):  # pass
                for _ in                 self.g_createTniks(self.lines, L, page, why=why):  pass
        elif self.DSP_J_LEV == S:
            for page in                  self.g_createTniks(self.pages, P, None, why=why):  # pass
                for l, line in enumerate(self.g_createTniks(self.lines, L, page, why=why)): # pass
                    if ll and not l:     self.createLLs(line, l, why)
                    for _ in             self.g_createTniks(self.sects, S, line, why=why):  pass
        elif self.DSP_J_LEV == C:
            for page in                  self.g_createTniks(self.pages, P, None, why=why):  # pass
                for l, line in enumerate(self.g_createTniks(self.lines, L, page, why=why)): # pass
                    if ll and not l:     self.createLLs(line, l, why)
                    for sect in          self.g_createTniks(self.sects, S, line, why=why):  # pass
                        for _ in         self.g_createTniks(self.colms, C, sect, why=why):  pass
        else:
            for page in                      self.g_newUpdTniks(P,                 nw=1, pt=None, why=why):  # pass
                for l, line in     enumerate(self.g_newUpdTniks(L,                 nw=1, pt=page, why=why)): # pass
                    if ll and not l:         self.createLLs(line, l, why) #                       if v and zz:         self.createZZs(sect, -1, why)
                    for s, sect in enumerate(self.g_newUpdTniks(S,                 nw=1, pt=line, why=why)): # pass s=z()[s],
                        for colm in          self.g_newUpdTniks(C, m=l*ns*nc+s*nc, nw=1, pt=sect, why=why):  # pass m=s*nc
                            for _ in         self.g_newUpdTniks(s+4,               nw=1, pt=colm, why=why): pass # s=l*ns+z()[s],
            self.resetH()
            if view: 
                for z in range(len(view)):
                    self.addZZs(z, why)
        self.dumpTniksSfx(why)
        if self.tabls and not self.cursor:  self.createCursor(why)   ;  self.dumpHdrs()
        if dbg and self.SNAPS >= 1:         self.regSnap('NEW', why)
        if dbg:         self.dumpStruct(why)
    ####################################################################################################################################################################################################
    def g_createTniks(self, tlist, j, pt=None, ii=None, why=Z, dbg=1, dbg2=1):
        n  = 1  if ii is not None else None
        n, _, x, y, w, h = self.geom(j, pt, n, ii, dbg=dbg2)
        n  = n  if ii is not None else 1
        p, l, c, _ = self.J1plct()
        tl2, x2, y2, j2 = tlist, x, y, j
        i3 = 0   ;   t = Z    ;    kl = self.k[j]    ;    js = (P, L, S, C, R, Q)
        for i in range(n):
            if self.DBG_TABT and j in js:    t = self.dbgTabTxt(j, i)
            i2 = i if ii is None else ii  ;  np, nl, ns, nc, nt = self.n
            if   j == S:                     self.SS.add(self.ss2sl()[i2] if self.ss2sl() else 0)
            if   j == P:                     v = 1 if i == self.j()[P] else 0   ;   self.log(f'j==P: {i=} {v=} {self.j()[P]=} {self.i[P]=}', f=0)
            else:                            v = int(self.pages[self.J1[P]].visible) # use parent or page? todo
            if   j == C:                    x2 = x + i2*w # ;  j2 = len(self.J2) if ii is not None else j
            else:
                if   j == P:                y2 = y
                elif j == L:                y2 = y - i2*h - self.LL*i2*h/(ns*nt)
                elif j >= T:
                    s                          = self.ss2sl()[self.J1[S]]
                    tl2, j2, kl, t0            = self.tnikInfo(p, l, s, c, i2, why=why) # todo
                    if   s == TT:            t = t0
                    elif s == NN:            t = t0 if j2 > K else self.sobj.tab2nn(t0, i2, nic=self.nic) if self.sobj.isFret(t0) else self.tblank
                    elif s in (II, KK):
                        m = self.getImap(p, l, c)
                        if   s == II:        t = self.imap2ikey( t0, m, i3, j2)  ;  i3 += 1 if t != self.tblank else 0
                        elif s == KK:        t = self.imap2Chord(t0, m, i2, j2)
                    y2 = y - i2*h
                else:                       y2 = y - i2*h
            k = kl[self.BGC]
            yield self.createTnik(tl2, i2, j2, x2, y2, w, h, k, why=why, t=t, v=v, dbg=dbg)
    ####################################################################################################################################################################################################
    def g_updateTniks(self, tlist, j, pt=None, ii=None, why=Z, dbg=1, dbg2=1):
        if not self.n[j]:     msg = f'ERROR {self.fmtJText(j, why)} SKIP {self.n[j]=}'   ;   self.log(msg) #  ;   cmd = cmds.QuitCmd(self, msg)  ;  cmd.do()
        n  = 1  if ii is not None else None
        n, _, x, y, w, h = self.geom(j, pt, n, dbg=dbg2)
        p, l, c, t = self.J1plct()
        tl2, x2, y2, j2 = tlist, x, y, j
        lp, ll = self.dl()[0], self.dl()[1]
        for i in range(n):
            if   j in (C, E):                   x2 = x + i*w
            else:
                if    j == P:                    v = int(self.pages[self.J1[P]].visible)  ;  self.log(f'j==P: {i=} {v=} {self.j()[P]=} {self.i[P]=}', f=0)
                else:                           y2 = y - i*h
                if    j == L:
                    if self.J2[L] >= lp*ll:     msg = f'WARN MAX Line {self.J2[L]=} >= {lp=} * {ll=}'  ;   self.log(msg)  ;  cmd = cmds.QuitCmd(self, msg)  ;  cmd.do()
                    y2 = y - i*h - self.LL*i*h/(self.n[S]*self.n[T])
                elif  j >= T:
                    s = self.ss2sl()[self.J1[S] % self.ssl()]
                    tl2, j2, _, _ = self.tnikInfo(p, l, s, c, why=why)
            yield self.updateTnik(tl2, self.J2[j2], j2, x2, y2, w, h, why=why, dbg=dbg)
    ####################################################################################################################################################################################################
    def ijSum(self, i, j, dbg=0):
        np, nl, ns, nc, nt = self.n
        p, l, s,  c = self.J1[P], self.J1[L], self.J1[S], self.J1[C]
        t, n, ii, k = self.J1[T], self.J1[N], self.J1[I], self.J1[K]
        if   j==P:               r = i
        elif j==L:               r = i + p*nl
        elif j==S:               r = i + l*ns
        elif j==C:               r = i
        elif j in (T, N, I, K):  r = i + c*nt % (nc*nt)
        else:                    r = -1
        if dbg: slog(f'({r=} {j=} {i=} , {p=} {l=} {s=} {c=} , {t=} {n=} {ii=} {k=} , {p*nl=} {l*ns=} {s*nc=} {c*nt=})', f=0)
        return r 

    def j2tl(self, j):
        assert 0 <= j < 16,            f'{j=}'
        assert len(self.E) > 0,        f'{len(self.E)}'
        assert self.E[j] is not None,  f'{j=} {self.fmtJ1(0, 1)} {self.fmtJ2(0, 1)}'
        return self.E[j]
        #self.pages if j==P else self.lines if j==L else self.sects if j==S else self.colms if j==C else self.tabls if j==T else self.notes if j==N else self.ikeys if j==I# else self.kords if j==K else self.views if j==M else self.rowLs if j==R else self.qclms if j==Q else self.hcurs if j==H else self.anams if j==A else self.bnums if j==B else self.capos if j==C else self.zclms if j==E else []

    def ji2plsct(self, j, i, dbg=1):
        p, l, s, c = self.hh()[P], self.hh()[L], self.hh()[S], self.hh()[C]
        t = self.j()[T] if j >= T else -1
        if   j==P:  p = i   ;   self.h[P] = i+1
        elif j==L:  l = i   ;   self.h[L] = i+1
        elif j==S:  s = i   ;   self.h[S] = i+1
        elif j==C:  c = i   ;   self.h[C] = i+1
        elif j>=T:  t = i   ;   self.h[T] = i+1
        if dbg:     self.log(f'plsct={self.fplsct(*self.h)} {j=} {i=}', p=0, f=0)
        return self.trncPlsct(p, l, s, c, t)
    ####################################################################################################################################################################################################
    def g_newUpdTniks(self, j, m=0, nw=0, pt=None, why=Z, dbg=1, dbg2=1):
        n, k, x, y, w, h   = self.geom(j, pt, n=None, dbg=dbg2)
        np, nl, ns, nc, nt = self.n
        x2, y2, j2, t0     = x, y, j, Z
        tl, hit            = self.j2tl(j2), 0
        i2, tx, kl = (0, Z, self.k[j]) if nw == 1 else (0, None, None)
        js  = (P, L, S, C, R, Q)       if nw == 1 else None
        for i in range(m, m+n):
            if nw == 1 and self.DBG_TABT and j in js:    tx = self.dbgTabTxt(j, i)
            ijs = self.ijSum(i, j2)
            if   j == P:                 v = 1 if i == self.j()[P] else 0   ;   self.log(f'j==P: {i=} {v=} {self.j()[P]=} {self.i[P]=}', f=0)
            else:                        v = int(self.pages[self.J1[P]].visible) # use parent or page? todo
            p, l, s, c, t                  = self.ji2plsct(j, i)
            if len(self.SS) == 0:  self.log(f'{s=} {len(self.SS)=}')   ;   return None
            s                              = self.ss2sl()[s]
            if   j in (C, E):           x2 = x + (i % nc) * w
            else:                       y2 = y - i * h
            if   j == L:                y2 = y2 - self.LL*i*h/(ns*nt)
            elif j >= T:
                tl, j2, kl, t0             = self.tnikInfo(p, l, s, c, i, why=why)  # todo
                if   s == TT:           tx = t0
                elif s == NN:           tx = t0 if j2 > K else self.sobj.tab2nn(t0, i, nic=self.nic) if self.sobj.isFret(t0) else self.tblank
                elif s in (II, KK):
                    im = self.getImap(p, l, c)
                    if   s == II:       tx = self.imap2ikey( t0, im, i2, j2)   ;   i2 += 1 if tx != self.tblank else 0
                    elif s == KK:       tx = self.imap2Chord(t0, im, i,  j2)
            msg = f'{ijs:3} {self.fmtJText(j2)} {j2=} {t0:3} {i=:2} {s=} {self.J2[j2]=:2} {len(tl)=:2} {len(tl)=:2} {self.fjlen()} {self.fmtJ1(1, 1)} {self.fmtJ2(1, 1)} {nw=}'    ;    self.log(f'{msg}', f=0)
#            assert x2 <= self.width  and w <= self.width,   f'{x2=} {w=} {self.width=} {msg}'
#            assert y2 <= self.height and h <= self.height,  f'{y2=} {h=} {self.height} {msg}'
            assert tl == self.E[j2],                        f'{j2=} {tl=} {self.E[j2]=} {msg}'
            assert nw in (0, 1, 2),     f'{msg}'
            if   nw == 0:
                if ijs < len(tl):
                    yield       self.updateTnik(tl, ijs, j2, x2, y2, w, h,     why=why,       v=1, dbg=dbg)
                else:     self.log(f'ERROR {self.ijSum(i, j2, 1)} >= {len(tl)} : {msg}')   ;   assert ijs >= len(tl),  f'{ijs=} {len(tl)=} {j=} {i=}'
            elif nw == 1:
                if   i <= ijs: # ijs >= len(tl):
                    kk = kl[self.BGC]
                    yield       self.createTnik(tl, i,   j2, x2, y2, w, h, kk, why=why, t=tx, v=v, dbg=dbg)
                else:     yield self.updateTnik(tl, ijs, j2, x2, y2, w, h,     why=why,       v=1, dbg=dbg)
            elif nw == 2:
                if ijs < len(tl):
#                    if j != S or (j == S and hit == 0):
#                        if j == S:  hit = 1 
                    yield   self.removeTnik(tl, ijs, j2, why=why, dbg=dbg)
#                    else: self.log(f'{ijs=} {len(tl)=} {j=} {j2=} {i=} {hit=} {self.fjlen()} J1={self.fmtJ1(0, 1)} J2={self.fmtJ2(0, 1)}')
    ####################################################################################################################################################################################################
    def removeTnik(self, tlist, i, j, why=Z, dbg=1): # AssertionError: When the parameters 'multiline' and 'wrap_lines' are True,the parameter 'width' must be a number.
        assert len(tlist) and i < len(tlist),  f'{len(tlist)=} {i=} {j=} {self.fmtJ1(0, 1)=} {self.fmtJ2(0, 1)=}'
        t = tlist[i]        ;     ha = hasattr(t, 'text')
        if j in (T,N,I,K): assert ha,  f'{j=} {i=}'
        t.visible = False   ;      v = int(t.visible)
#        if   ist(t, LBL):  t.width, t.height = 1, 0  # Zero width not allowed
#        elif ist(t, SPR):  t.update(scale_x=0, scale_y=0)
        if dbg:     text = t.text if ha else Z   ;   self.log(f'{self.fmtJText(j)} {i=} {id(t):x} {text:6} {self.ftxywh(t)} {self.fjlen()} J1={self.fmtJ1(0, 1)} J2={self.fmtJ2(0, 1)}', p=0, f=0)
        self.setJdump(j, i, v, why)
        return t

    def createTnik(self, tlst, i, j, x, y, w, h, k, why=Z, t=Z, v=0, dbg=0):
        assert i    is not None and j is not None,  f'ERROR i or j is None {i=} {j=} lt={len(tlst) if tlst is not None else None} {t=} {why}'
        assert tlst is not None and k is not None,  f'ERROR tlst or k is None {tlst=} {k=}'
        assert ist(v, int),  f'ERROR wrong type {type(v)=} {v=}'
        self.setJ(j, i, v) # todo fixme - make it clear we want to set v (visible) on the tnik as well
        o, _, d, ii, n, s = self.fontParams()   ;   b = self.batch   ;   g = self.j2g(j)
        if j == H or (self.SPRITES and (j < T or j == R)):
            scip   = pygimg.SolidColorImagePattern(k)
            img    = scip.create_image(width=fri(w), height=fri(h))
            wx, wy = self.axyWgt(self.ax, self.ay)
            img.anchor_x, img.anchor_y   = int(wx*w), int(wy*h)
            self.log(f'{x=} {y=} {w=} {h=} {img.anchor_x=} {img.anchor_y=} {self.ax=} {self.ay=}')
            tnik                         = SPR(img, x, y, batch=b, group=g, subpixel=self.SUBPIX)
            tnik.color, tnik.opacity     = k[:3], k[3]
            tnik.anchor_x, tnik.anchor_y = wx*w, wy*h
            assert int(tnik.anchor_x)==img.anchor_x,  f'{int(tnik.anchor_x)=} != {img.anchor_x=}'
            assert int(tnik.anchor_y)==img.anchor_y,  f'{int(tnik.anchor_y)=} != {img.anchor_y=}'
        else:
            s = self.calcFontSize(j)       ;   aa, ax, ay = self.aa, self.ax, self.ay  # left center right  # bottom center top (baseline)
            z = 1 if self.STRETCH else 0   ;   d,  n,  ml = FONT_DPIS[d], FONT_NAMES[n], self.MULTILINE
            tnik = LBL(t, font_name=n, font_size=s, bold=o, italic=ii, stretch=z, color=k, x=x, y=y, width=w, height=h, anchor_x=ax, anchor_y=ay, align=aa, multiline=ml, dpi=d, batch=b, group=g)
            tnik.content_valign =  self.av
            if   j == Q:           self.setTNIKStyle2(tnik, self.k[j] if (i+1) % 10 else self.k[R], NORMAL_STYLE)
            else:                  self.setTNIKStyle2(tnik, self.k[j],                              NORMAL_STYLE)
        if j == P and v:           self.setCaption(f'{utl.ROOT_DIR}/{DATA}/{self.FILE_NAME}.{DAT} page {self.i[P]}')
        self.checkTnik(tnik, i, j)
        if    tlst is not None:    tlst.append(tnik)
        key = self.idmapkey(j)  ;  self.idmap[key] = (tnik, j, i)
        tnik.visible =  bool(v)
#        self.visib[j].append(v)
        if    dbg:                 self.dumpTnik(tnik, j, why)
        return tnik
    ####################################################################################################################################################################################################
    def updateTnik(self, tlist, i, j, x, y, w, h, why=Z, v=0, dbg=0):
        assert 0 <= i < len(tlist),  f'{i=} {len(tlist)=} {j=} {x=:.2f} {y=:.2f} {w=:.2f} {h=:.2f} {why} {self.ijSum(i, j)=}'
        tnik   = tlist[i]
        self.log(f'{why} {H=} {j=} {i=} {self.J2[H]=}')       if dbg and j == H else None
        if   ist(tnik, SPR) and tnik.visible:
            mx, my = w/tnik.image.width, h/tnik.image.height
            tnik.update(x=x, y=y, scale_x=mx, scale_y=my)
        elif ist(tnik, LBL) and tnik.visible:
            if w <= 0: w = 1  ;  self.log(f'{j=} {i=} {x=} {y=} {w=} {h=}')
#            assert w > 0,  f'{w=} {tnik.visible=}' # AssertionError: When the parameters 'multiline' and 'wrap_lines' are True, the parameter 'width' must be a number.
            tnik.font_size = self.calcFontSize(j)
            tnik.x, tnik.y, tnik.width, tnik.height = x, y, w, h
            self.checkTnik(tnik, i, j)
        else: assert type(tnik) == SPR or type(tnik) == LBL,  f'{type(tnik)=}'
        self.setJ(j, i, tnik.visible) if j != H or (j == H and self.J2[H] == 0) else None # todo fixme - do we want or need to set v info of the tnik as well?
        self.dumpTnik(tnik, j, why) if dbg else None
        if j == P and tnik.visible:   self.setCaption(f'{utl.ROOT_DIR}/{DATA}/{self.FILE_NAME}.{DAT} page {self.i[P]}')
        tnik.visible =  bool(v)
        return tnik
    ####################################################################################################################################################################################################
    def dumpTniksPfx(self, why=Z, h=1, r=1):
        if r:        self.resetJ(why)   ;   self.clearVisib()
        self.dumpGeom('BGN', why)
        if not r:
            if self.J1 and self.J2: self.dumpJs(why, w=None)
            else:                   cmd = cmds.QuitCmd(self, f'ERROR No Js {len(self.J1)=} {len(self.J2)=}')  ;  cmd.do()
        if h: self.dumpHdrs()

    def dumpTniksSfx(self, why=Z, h=1):
        if h: self.dumpHdrs()
        if self.J1 and self.J2:     self.dumpJs(why, w=None)
        else:                       cmd = cmds.QuitCmd(self, f'ERROR No Js {len(self.J1)=} {len(self.J2)=}')  ;  cmd.do()
        self.dumpGeom('END', why)

    def dumpHdrs(self): hdr1 = self.fTnikHdr(0)   ;   hdr0 = self.fTnikHdr(1)   ;   self.log(hdr1, p=0)   ;   self.log(hdr0, p=0)
    ####################################################################################################################################################################################################
    def fTnikHdr(self, spr=0):
        tid = ' TId  Identity  ' if self.OIDS else ' Tid'  ;    wnc = ' Why  Name  Cnt'  ;  rot_txt = 'Rotate ' if spr else 'PrtTxt '
        gv  = 'G V'     ;     jts = self.fjtxt()   ;   xywh = W.join(XYWH)           ;   cwh = self.cwhH()   ;  acva = self.acvaH()  ;   axy2 = self.axy2H()
        cnc = ' CC  NC CN'   ;   rgb = ' Red Grn Blu Opc' if self.LONG_TXT else Z    ;   rgbM = (' M     Mx    My  ' if spr else rgb)  if self.LONG_TXT else Z
        sfx = ('x y AncX AncY Grp            pGrp'     if spr     else     f' {axy2} {cwh} {W.join(ADS)} {acva} FnSz dpi B I FontName') if self.LONG_TXT else Z
        ft  = f'{W*13}FullText' if self.LONG_TXT and not spr and self.DBG_TABT else Z
        return f'{tid} {wnc} {rot_txt}{gv} {jts} {xywh} {cnc} {rgb} {rgbM} {sfx}{ft}'
    @staticmethod
    def axy2H(d=W):  return d.join(AXY2)
    @staticmethod
    def acvaH(d=W):   return d.join(ACVA)
    @staticmethod
    def cwhH(d=W):   return d.join(CWH)
    ####################################################################################################################################################################################################
    @staticmethod
    def fjtxt():     return W.join(f'{jtxt[0]:>{JFMT[i]}}' for i, jtxt in enumerate(JTEXTS)) + ' Vis' # optimize str concat?

    def dumpTnik(self, t=None, j=None, why=Z):
        if   t is None:    self.log(self.fTnikHdr(), p=0)   ;   return # hack
        if   j is None:                              msg = f'{why} ERROR BAD j {j=}'             ;  self.log(msg)  ;  cmd = cmds.QuitCmd(self, msg)  ;  cmd.do()
        elif not ist(t, LBL) and not ist(t, SPR):    msg = f'{why} ERROR Bad t type {type(t)=}'  ;  self.log(msg)  ;  cmd = cmds.QuitCmd(self, msg)  ;  cmd.do()
        j1   = self.J1   ;   p, l, c, t2 = j1[P], j1[L], j1[C], j1[T]   ;   fc, bc, rot_txt, sfx = Z, Z, Z, Z
        foid = self.foid(t, j, why)   ;    gv = f'{self.gn[j]:x} {self.ftvis(t)}'   ;   fj2 = self.fmtJ2(d=0)   ;   xywh = self.ftxywh(t)
        cc   = self.plct2cc(p, l, c, t2)   ;   cnc = f'{cc+1:3} {self.normalizeCC(cc):3} {self.cc2cn(cc)+1:2}' if j >= T else W*10
        if   ist(t, LBL):  rot_txt = self.fpTxt(t)  ;  fc = self.getDocColor(t, 0)  ;  bc = self.getDocColor(t, 1)   ;  sfx = f' {self.fLbl(t)}' if self.LONG_TXT else Z
        elif ist(t, SPR):  rot_txt = self.frot(t)   ;  fc = self.ftcolor(t)         ;  bc = self.ftMxy(t)            ;  sfx = f' {self.fSpr(t)}' if self.LONG_TXT else Z
        colors = f' {fc}{bc}' if self.LONG_TXT else Z
        self.log(f'{foid} {rot_txt}{gv} {fj2} {xywh} {cnc}{colors}{sfx}', p=0)
    ####################################################################################################################################################################################################
    def on_close(        self):                     return evnts.on_close(        self)
    def on_draw(         self, **kwargs):           return evnts.on_draw(         self, **kwargs)
    def on_key_press(    self, symb, mods):         return evnts.on_key_press(    self, symb, mods)
    def on_key_release(  self, symb, mods):         return evnts.on_key_release(  self, symb, mods)
    def on_mouse_motion( self, x, y, dx, dy):       return evnts.on_mouse_motion( self, x, y, dx, dy)
    def on_mouse_scroll( self, x, y, dx, dy):       return evnts.on_mouse_scroll( self, x, y, dx, dy)
    def on_mouse_release(self, x, y, bttn, mods=0): return evnts.on_mouse_release(self, x, y, bttn, mods)
    def on_move(         self, x, y):               return evnts.on_move(         self, x, y)
    def on_resize(       self, w, h, z=None):       return evnts.on_resize(       self, w, h, z)
    def on_text(         self, text):               return evnts.on_text(         self, text)
    def on_text_motion(  self, motion):             return evnts.on_text_motion(  self, motion)
#        super().on_resize(w, h)
#        assert z in (0, 1, None),  f'{z=}'
#        if self.RESIZE:
#            cmd = cmds.UpdateTniksCmd(self, 'on_resize()', w, h, z, dbg=1)     ;  cmd.do()
#        return True
    ####################################################################################################################################################################################################
    def idmapkey(self, j):  return f'{JTEXTS[j]}{self.J2[j]}'
    def dumpIdmKeys(self):  self.log(fmtl(list(self.idmap.keys()), ll=1))
    def fSpr(self, t, d=W): return f'{self.fAxy()}{d}{self.fiax(t)}{d}{self.fiay(t)}{d}{self.fgrp(t)}{d}{self.fgrpp(t)}'
    def fLbl(self, t, d=W):
        dtxt = f'{d}{self.ffTxt(t)}' if self.DBG_TABT and len(t.text.replace(X, Z)) > 6 else Z  ;  td = t.document
        ancX, ancY = self.fancXY(t)
        fnt  = td.get_font()    ;   asc  = fnt.ascent   ;   dsc = fnt.descent   ;   sad = asc + abs(dsc) # todo descent value seems to be negative?
        ads  =  self.fads(asc, dsc, sad, d)
        return d.join([self.fAxy(), ancX, ancY, self.fcwh(t), ads, self.fAaAv(t), self.fFntSz(t), self.ffont(t), dtxt])
    @staticmethod
    def fads(asc, dsc, sad, d):    return d.join([f'{asc:5}', f'{-dsc if dsc < 0 else dsc:5}', f'{sad:5}']) # todo display a positive value
    @staticmethod
    def frot(t):                   return f'{t.rotation:6.1f} '
    def fnvis(self):               return f'{self.nvis:3}'
    @staticmethod
    def ffTxt(t):                  return t.text.replace(X, Z)
    @staticmethod
    def fpTxt(t): a = t.text.replace(X, Z)  ;  b = a[:6]  ;  b += '+' if len(a) > 6 else W  ;  return f'{b:7}'
    @staticmethod
    def fcwh(       t, d=W):       return f'{fmtf(t.content_width, 5)}{d}{fmtf(t.content_height, 5)}'
    def fAaAv(self, t, d=W):       return f'{self.ftAa(self.aa)}{d}{self.ftAv(t.content_valign)}'
    def fCtnt(self, t, d=W):       return f'{self.fcwh(t)}{d}{self.fAaAv(t)}'
    def getDocColor(self, t, c=1): return utl.fColor(self._getDocColor(t, c))
    @staticmethod
    def _getDocColor(t, c=1):      s = BGC if c else COLOR    ;  return t.document.get_style(s)
    def foid(self, t, j, why):  i, n = self.J2[-1], int(self.idmapkey(j)[4:])  ;  oid = f' {id(t):11x}' if self.OIDS else Z  ;  return f'{i:4}{oid} {why:5} {JTEXTS[j]} {n:4}'
    ####################################################################################################################################################################################################
    @staticmethod
    def a2csv(a, w=7):   return fmtl(a, w=w, u="^", d=Z, s=Y) if ist(a, list) else f'{a:^{w}}'
    def args2csv(self):  return f'{W*4}, -n ,{self.a2csv(self.n0)}', f'{W},{W}, -i  ,{self.a2csv(self.i0, w=5)}', f' -s  ,{self.a2csv(self.ss2sl()[:2], w=1)},{self.a2csv(self.ss2sl()[2:], w=4)} ,{W*4},{W*4},{W*4},{W*8}'
    @staticmethod
    def csvHdr(n): return JLBL(n, Y)
#    def csvHdr(self, j, n): return JLBL(n, Y) if ist(self.E[j][0], LBL) else JSPR(n, Y) # ist(self.E[j][0], SPR)

    def t2csv(self, tnik, j, i, d=W, ds=Z):
        assert tnik == self.E[j][i],  f'{tnik=} != {self.E[j][i]=}'
        self.tids.add(id(tnik))  ;   xywh = self.ftxywh(tnik, s=d)   ;   ii = f'{i+1:4}'
        axy = self.fAxy(d)       ;   ancX, ancY = self.fancXY(tnik)
        if   ist(tnik, LBL):
            td  = tnik.document  ;  fnt = td.get_font()     ;  asc, dsc = fnt.ascent, fnt.descent  ;  sad = asc + abs(dsc) # todo descent value seems to be negative?
            ads = self.fads(asc, dsc, sad, d)  ;  cwh = self.fcwh(tnik, d)  ;  acva = self.fAaAv(tnik, d)
            return d.join([JTEXTS[j], ii, xywh, axy, ancX, ancY, cwh, ads, acva, ds])
        elif ist(tnik, SPR):
            return d.join([JTEXTS[j], ii, xywh, axy, ancX, ancY])
    ####################################################################################################################################################################################################
    def dumpTnikCsvs(self, snapPath):
        name = snapPath.stem if snapPath else Z
        args = self.args2csv()   ;   self.log(f'{fmtl(args, d=Z, s=Y)}{name}', p=0, f=3)
        for j, p in enumerate(self.pages):     self.dumpTnikCsv(p, P, j)
        for j, l in enumerate(self.lines):     self.dumpTnikCsv(l, L, j)
        if self.LL and self.rowLs and self.qclms:
            for j, r in enumerate(self.rowLs): self.dumpTnikCsv(r, R, j)
            for j, q in enumerate(self.qclms): self.dumpTnikCsv(q, Q, j)
        for j, s in enumerate(self.sects):     self.dumpTnikCsv(s, S, j)
        for j, c in enumerate(self.colms):     self.dumpTnikCsv(c, C, j)
        for j, t in enumerate(self.tabls):     self.dumpTnikCsv(t, T, j)
        for j, n in enumerate(self.notes):     self.dumpTnikCsv(n, N, j)
        for j, i in enumerate(self.ikeys):     self.dumpTnikCsv(i, I, j)
        for j, k in enumerate(self.kords):     self.dumpTnikCsv(k, K, j)
        for j, h in enumerate(self.hcurs):     self.dumpTnikCsv(h, H, j)
    ####################################################################################################################################################################################################
    def dumpTnikCsv(self, t, j, i):
        if i == 0 and j == P:    h = self.csvHdr(n=1)   ;   self.log(f'{h}', p=0, f=3)
        self.log(self.fmtTnikCsv(t, j, i), p=0, f=3)
#        if i == 0 and j == H:    h = self.csvHdr(j, n=1)   ;   self.log(f'{h}', p=0, f=3)
    def fmtTnikCsv(self, t, j, i):
        s = {}
        if   ist(t, LBL):   d = t.document  ;  m = d.styles  ;  s = self.fDocStyle(m, Y, t)
#        elif ist(t, SPR):   z = Y.join([W * len(_) for _ in LTXX])
        return self.t2csv(t, j, i, Y, s)
    ####################################################################################################################################################################################################
    def saveDigits__old(self):
        path = utl.getFilePath('_2', BASE_PATH, PNGS, PNG)
        for i in range(self.n[C] * self.n[T], self.n[T]):
#            self.tabls[i]
            bm = pygimg.get_buffer_manager()
            frame = bm.get_color_buffer()
            img = frame.get_image_data()
            with open(path, 'wb', encoding='utf-8') as file:
                file.write(img.get_image_data())

    def saveImg(self, path):
        doc      = document.FormattedDocument()
        doc.text = '0123456789'
        layout.TextLayout(doc)
#        tl.view_x     = tl.get_point_from_position(0)[0]
#        tl.view_width = tl.get_point_from_position(len(doc.text))[0]
        bm        = pygimg.get_buffer_manager()
        frame     = bm.get_color_buffer()
        img       = frame.get_image_data()
        self.log(f'{path=}', f=2)
        with open(path, 'wb', encoding='utf-8') as file:
            file.write(img.get_data())
    ####################################################################################################################################################################################################
    def createSprite(self, tlist, i, j, x, y, w, h, k, why=Z, t=Z, v=0, g=None, dbg=0):
        path = utl.getFilePath('_2', BASE_PATH, PNGS, PNG)
        self.saveImg(path)
        self.setJ(j, i, v)
        if dbg:    self.log(f'{j=} {JTEXTS[j]} {i=} {t=} [{x} {y} {w} {h}] {g=} {utl.fmtl(k)} {why}\n{path=}')
        img = pygimg.load(path)
        wx, wy = self.axyWgt(self.ax, self.ay)
        img.anchor_x, img.anchor_y = int(wx*w), int(wy*h)
        tnik = SPR(img, x=x, y=y, batch=self.batch, group=self.j2g(j), subpixel=self.SUBPIX)
        tnik.color, tnik.opacity = k[:3], k[3]
        tnik.anchor_x, tnik.anchor_y = wx*w, wy*h
        assert int(tnik.anchor_x)==img.anchor_x,  f'{int(tnik.anchor_x)=} != {img.anchor_x=}'
        assert int(tnik.anchor_y)==img.anchor_y,  f'{int(tnik.anchor_y)=} != {img.anchor_y=}'
        assert ist(v, int),  f'{type(v)=} {v=}'
        tnik.visible = bool(v)        ;  self.visib[j].append(v)
#        self.checkTnik(tnik, i, j)
        if    tlist is not None:   tlist.append(tnik)
        key = self.idmapkey(j)  ;  self.idmap[key] = (tnik, j, i)   ;   self.dumpTnik(tnik, j, why) if dbg else None
        return tnik
    ####################################################################################################################################################################################################
    def createCursor(self, why, dbg=1):
        x, y, w, h, c = self.cc2xywh()
        kk = 0  ;  kl = self.k[H]  ;  k = kl[kk]
        assert w != 0 and h != 0,  f'{w=} {h=} {x=} {y=} {c=}' 
#        if w == 0 or h == 0: msg = f'ERROR DIV by ZERO {w=} {h=}'   ;   self.log(msg)   ;   cmd = cmds.QuitCmd(self, msg)  ;  cmd.do()
        if self.TEST == 3:  self.cursor = self.createSprite(self.hcurs, 0, H, x, y, w, h, k, why=why, v=1, dbg=dbg)
        else:               self.cursor = self.createTnik(  self.hcurs, 0, H, x, y, w, h, k, why=why, v=1, dbg=dbg)
        if self.LL:         self.setLLStyle(self.cc, CURRENT_STYLE)
    ####################################################################################################################################################################################################
    def cc2xywh(self, dbg=1):
        tpb, tpp, tpl, tps, tpc = self.ntp()   ;   lenT = len(self.tabls)
        old   = self.cursorCol()   ;   cc = old % lenT
        self.log(f'{tpp=} {old=} {lenT=} {cc=} old % lenT', f=0)
        assert 0 <= cc < lenT,  f'Invalid index {cc=} {tpp=} {old=} {lenT=}'
        t     = self.tabls[cc]
        if dbg: self.log(f'{cc=:4} {old=:4} {self.fntp()} {self.ftxywh(t)} {t.text=} {self.fCtnt(t)}', f=0) # i={Notes.n2i(self.sobj.tab2nn(t, cc % lenT))}
        w, h  = t.width if t.width is not None else t.height , t.height
        assert w != 0 and h != 0,  f'{w=} {h=}'
        return  t.x, t.y, w, h, cc
    ####################################################################################################################################################################################################
    def plc2cn(self, p, l, c, dbg=0):
        tpb, tpp, tpl, tpc = self.ntp2()
        cn = p * tpp//tpc + l * tpl//tpc + c
        self.log(f'{cn=} = {p=} * {tpp=} + {l=} * {tpl=} + {c=} * {tpc=}') if dbg else None
        return cn
    
    def plct2cc(self, p, l, c, t, dbg=0):
        tpb, tpp, tpl, tps, tpc = self.ntp()
#        assert tpp != 0,  f'{self.ntp()=}'
        if tpp <= 0:  self.log(f'{tpp=} plct={self.fplct(p, l, c, t)}')    ;    return 0
        ns = self.n[S] if self.n[S] else 1
        cc = p*tpp//ns + l*tpl//ns + c*tpc + t
        cc = cc % tpp
        if dbg: self.log(f'    {cc:4} {self.fntp()} {self.fplct(p, l, c, t)} ({p*tpp:4} +{l*tpl:3} +{tps:3} +{c*tpc:3} +{t})', f=0)
        return cc

    def cursorCol(  self,     dbg=1):   cc = self.plct2cc(*self.j2(), dbg=dbg)   ;   self.log( f'{cc=:3} {utl.fmtl(self.j2())}', f=0) if dbg else None  ;  self.cc = cc  ;  return self.cc
    def normalizeCC(self, cc, dbg=0):  tpc = self.tpc  ;  old = cc  ;  cc = cc//tpc*tpc  ;  self.log(f'{old=:4} {cc=:4} {tpc=}', f=0) if dbg else None  ;  return cc

    def cc2cn(      self, cc, dbg=0):  nt = self.n[T]  ;  cn = cc//nt   ;  self.log(f'{cn:3} {cc:4}//{nt=} {cc//nt=}', f=0) if dbg else None  ;  return  cn
    def cn2cc(      self, cn, dbg=0):  nt = self.n[T]  ;  cc = cn * nt  ;  self.log(f'{cc:4} {cn:3} *{nt=} {cn *nt=}', f=0) if dbg else None  ;  return  cc

#    def cn2txt(self, cn, dbg=0):  #  usefull? re-name f cn2tabtxt()
#        cc         = self.cn2cc(cn)
#        p, l, c, t = self.cc2plct(cc)
#        txt        = self.data[p][l][c]
#        self.log(f' {cn:3} {cc:4} {self.fntp()} {self.fplc(p, l, c)} txt={txt}') if dbg else None
    ####################################################################################################################################################################################################
    def cc2plct(self, cc, dbg=0): #todo
        tpb, tpp, tpl, tps, tpc = self.ntp()
        np,  nl,  ns,  nc,  nt  = self.n
        t =    cc      % nt
        c =    cc//tpc % nc
        l = ns*cc//tpl % nl
        p = ns*cc//tpp % np
        if dbg: self.log(f'{cc:4} {self.fntp()} {self.fplct(p, l, c, t)}')
        return p, l, c, t

    def cc2plsct(self, cc, dbg=0): #todo
        tpb, tpp, tpl, tps, tpc = self.ntp()
        np,  nl,  ns,  nc,  nt  = self.n
        t =    cc      % nt
        c =    cc//tpc % nc
        s =    cc//tps % ns
        l = ns*cc//tpl % nl
        p = ns*cc//tpp % np
        if dbg: self.log(f'{cc:4} {self.fntp()} {self.fplsct(p, l, s, c, t)}')
        return p, l, s, c, t
    ####################################################################################################################################################################################################
    def J1plct(self, p=None, l=None, c=None, t=None, dbg=0): #        return p2 % np, l2 % nl, c2 % nc, t2 % nt
        np, nl, ns, nc, nt = self.n    ;    n = 0
#        s = self.J1[S]
        if p is None:    p = self.J1[P]
        if l is None:    l = self.J1[L]
        if c is None:    c = self.J1[C]
        if t is None:    t = self.J1[T]
        t2 = n + t
        c2 = t2 // nt + c
#        s2 = c2 // nc + s
#        l2 = s2 // ns + l
        l2 = c2 // nc + l
        p2 = l2 // nl + p
        rp = p2 % np
        rl = l2 % nl
#        rs = s2 % ns
        rc = c2 % nc
        rt = t2 % nt
        if dbg: self.log(f'plct={self.fplct(p, l, c, t)} plct2={self.fplct(p2, l2, c2, t2)} rplct={rp, rl, rc, rt}')
        return rp, rl, rc, rt # todo

    def J1plsct(self, p=None, l=None, s=None, c=None, t=None, dbg=0):
        np, nl, ns, nc, nt = self.n
        if p is None:    p = self.J1[P]
        if l is None:    l = self.J1[L]
        if s is None:    s = self.J1[S]
        if c is None:    c = self.J1[C]
        if t is None:    t = self.J1[T]
        t2 = t  % nt
        c2 = t2 // nt
        s2 = c2 // nc
        l2 = s2 // ns
        p2 = l2 // nl
        rp = p2 % np
        rl = l2 % nl
        rs = s2 % ns
        rc = c2 % nc
        rt = t2 % nt
        if dbg: self.log(f'plsct={self.fplsct(p, l, s, c, t)} plsct2={self.fplsct(p2, l2, s2, c2, t2)} rplsct={rp, rl, rs, rc, rt}')
        return rp, rl, rs, rc, rt # todo
    ####################################################################################################################################################################################################
    def j2plct(self, p=None, l=None, c=None, t=None, dbg=0):
        np, nl, ns, nc, nt = self.n
        p2, l2, c2, t2     = self.J2[P], self.J2[L], self.J2[C], self.J2[T]
        if p is None:    p = p2 % np
        if l is None:    l = l2 % nl
        if c is None:    c = c2 % nc
        if t is None:    t = t2 % nt
        if dbg: self.log(f'plct2={self.fplct(p2, l2, c2, t2)} plct={self.fplct(p, l, c, t)}')
        return p, l, c, t

    def j2plsct(self, p=None, l=None, s=None, c=None, t=None, dbg=0):
        np, nl, ns, nc, nt = self.n
        p2, l2, s2, c2, t2 = self.J2[P], self.J2[L], self.J2[S], self.J2[C], self.J2[T]
        if p is None:    p = p2 % np
        if l is None:    l = l2 % nl
        if s is None:    s = s2 % ns
        if c is None:    c = c2 % nc
        if t is None:    t = t2 % nt
        if dbg: self.log(f'plsct2={self.fplsct(p2, l2, s2, c2, t2)} plsct={self.fplsct(p, l, s, c, t)}')
        return p, l, s, c, t
    ####################################################################################################################################################################################################
    def setCaption(self, msg, dbg=1):
        if dbg: self.log(msg, f=0)
        self.set_caption(msg)
    ####################################################################################################################################################################################################
    def calcFontSize(self, j=T, dbg=0):
        np, nl, ns, nc, nt = self.n   ;   w, h = self.viewW, self.viewH   ;   ll = self.LL
        if j < T: nt = 1
        if j < C: nc = 1
        if j < S: ns = 1
        if j < L: nl = 1
        nr = nl * (ns * nt + ll)
        pw, ph = w/nc, h/nr
        pw /= j+1 if j < C else 1
        pix = min(pw, ph)
        fs   =  self.pix2pnt(pix)
        if dbg: self.log(f'{j=} {JTEXTS[j]:4} {w=:6.2f} {h=:6.2f} {nc=} {nr=} {pw=:6.2f} {ph=:6.2f} {pix=:6.2f} {fs=:6.2f}')
        return fs

    def _initFonts(self):
        np, nl, ns, nc, nt = self.n #           ;  nc += self.zzl()
        n  = nl * nt * ns if ns else nl * nt   ;   n += self.LL * nl
        w  = self.viewW / nc  ;  h = self.viewH / n
        fs = self.calcFontSize(j=T, dbg=1)
        self.fontBold, self.fontItalic, self.clrIdx, self.fontDpiIndex, self.fontNameIdx, self.fontSize = 0, 0, 0, 4, 0, fs
        self.log(f'{w=:6.3f}={self.viewW=:6.1f}/({nc})                 {Z}{PNT_PER_PIX=:6.4f} fs=w*PNT_PER_PIX={fs:6.2f}pt', f=2)
        self.log(f'{h=:6.3f}={self.viewH=:6.1f}/({nl=} * {ns=} * {nt=}){W}{PNT_PER_PIX=:6.4f} fs=h*PNT_PER_PIX={fs:6.2f}pt', f=2)
        self.dumpFont()

    def fmtFont(self, dbg=0):
        fb, fc, fd, fi, fn, fs = self.fontParams()
        text = f'{FONT_DPIS[fd]}dpi {fs:5.2f}pt {FONT_NAMES[fn]} {fc}'
        if dbg: self.log(text)
        return text

    def dumpFont(self, why=Z):
        b, k, dpi, i, n, s = self.fontParams()
        pix = s / PNT_PER_PIX   ;   fcs = Z # f'{fmtl( [k])}'
        self.log(f'{dpi}:{FONT_DPIS[dpi]}dpi {s:6.2f}pt {n}:{FONT_NAMES[n]} {k}:{fcs} {s:6.2f}pt = {PNT_PER_PIX:6.4f}(pt/pix) * {pix:6.2f}pixels {why}', f=-3)

    def setFontArg2(self, ts, n, v, m, j, dbg=1):
        l = 0   ;   fb = 0   ;   fs = 1   ;   msg = Z
        for i, t in enumerate(ts):
            if ist(t, LBL):
                if   m == 'clrIdx':       l = len(t.color)   ;  msg = f'{v=:2} tc={fmtl(t.color, w=3)}  ds={fmtl(t.document.get_style(n), w=3)}  kv={fmtl(self.k[v][fb][:l], w=3)}'
                elif m == 'fontNameIdx':                        msg = f'{v=:2} {FONT_NAMES[v]=}'
                elif m == 'fontSize':    fs = getattr(t, n)  ;  msg = f'{v=:.2f} {fs=:.2f}'
                if dbg and ist(t, LBL) and i==0:            self.log(f'{j=:2} {i=:2}  {l} {fb} {m=:12} {n=:12} {msg}', f=2)
                if   m == 'clrIdx':       self.setTNIKStyle2(t, self.k[v], self.fontStyle)
                elif m == 'fontNameIdx':  setattr(t, n, FONT_NAMES[v])
                elif m == 'fontSize':     setattr(t, n, v*fs)
                else:                     setattr(t, n, v)

    @staticmethod
    def pix2pnt(pix):      return pix * PNT_PER_PIX # ( ) % FS_MAX
    def fontParams(self):  return self.fontBold, self.clrIdx, self.fontDpiIndex, self.fontItalic, self.fontNameIdx, self.fontSize
    ####################################################################################################################################################################################################
    def qdmod(self, n, j, dbg=1):
        if    j == P: tp = self.tpp//self.n[S]  ;  tp2 = len(self.tabls)//self.n[P]
        else:         tp = self.tpl//self.n[S]  ;  tp2 = len(self.tabls)//(self.n[P] * self.n[L])
        assert  tp == tp2,     f'{tp=} != {tp2=}, {n=} {j=}'
        if dbg:       self.log(f'{n=} {j=} {tp=} {tp2=} {n//tp=} {n%tp=}')
        return tp, n//tp, tp % tp
    ####################################################################################################################################################################################################
    def setDTNIK(self, text, cc, p, l, c, t, kk=0, pos=1, dbg=0):
        if dbg:  self.log(f'BGN {kk=}    {text=}', pos=pos)
        self.setData(text, p, l, c, t)
        imap   = self.getImap(p, l, c)
        if TT in self.SS: self.setTab2( text, cc)
        if NN in self.SS: self.setNote( text, cc, t)
        if II in self.SS: self.setIkey( imap, p, l, c)
        if KK in self.SS: self.setChord(imap, cc, pos=1, dbg=1) if kk else None
        if dbg:  self.log(f'END {kk=}    {text=} {len(imap)=}', pos=pos)
    ####################################################################################################################################################################################################
    def setData(self, text, p, l, c, t, pos=0, dbg=0):
        data =  self.data[p][l][c]
        if dbg: self.log(f'BGN {t=} {text=} {data=}', pos=pos)
        self.data[p][l][c] = data[0:t] + text + data[t+1:]
        data =  self.data[p][l][c]
        if dbg: self.log(f'END {t=} {text=} {data=}', pos=pos)

    def setTab2(self, text, cc, pos=0, dbg=0):
        if dbg: self.log(f'BGN         {text=} tabs[{cc}]={self.tabls[cc].text}', pos=pos)
        self.tabls[cc].text = text
        if dbg: self.log(f'END         {text=} tabs[{cc}]={self.tabls[cc].text}', pos=pos)

    def setNote(self, text, cc, t, pos=1, dbg=0): #fix me
        assert cc < len(self.notes),  f'{cc=} {len(self.notes)=} {self.fjlen()}'
        old   = self.notes[cc].text
        if dbg: self.log(f'BGN     {t=} {text=} notes[{cc}]={old}', pos=pos)
        if dbg: self.log(kysgs.fmtKSK(self.ks[kysgs.KSK]))
        ntext = self.sobj.tab2nn(text, t, nic=self.nic) if self.sobj.isFret(text) else self.tblank
        if old in Notes.N2I:
            i  =  Notes.N2I[old]
            if  self.nic[i] <= 1:  del self.nic[i]
            else:                      self.nic[i] -= 1
            kysgs.dumpNic(self.nic)
        self.notes[cc].text = ntext
        if dbg: self.log(f'END     {t=} {text=} notes[{cc}]={self.notes[cc].text}', pos=pos)
#        utl.updNotes(11, 'B', 'Cb', Notes.TYPE, -1)
#        utl.updNotes( 5, 'F', 'E#', Notes.TYPE, -1)
#        utl.updNotes( 4, 'E', 'Fb', Notes.TYPE, -1)
#        utl.updNotes( 0, 'C', 'B#', Notes.TYPE, -1)
    ####################################################################################################################################################################################################
    def getImap(self, p=None, l=None, c=None, dbg=0, dbg2=0):
        dl    = self.dl() #todo
        cn    = self.plc2cn(p, l, c)          ;     key = cn   ;   mli = self.cobj.mlimap
        msg1  = f'plc={self.fplc(p, l, c)}'   ;    msg2 = f'dl={self.fmtdl()} {cn=} {key=} keys={fmtl(list(mli.keys()))}'
        if dbg:        self.log(f'{msg1} {msg2}', f=0)
        if p >= dl[0] or l >= dl[1] or c >= dl[2]:  msg = f'ERROR Indexing {msg1} >= {msg2}'  ;  self.log(msg)  ;  cmd = cmds.QuitCmd(self, msg)  ;  cmd.do() # todo is this correct?
        imap  = self.cobj.getChordName(self.data, None, cn, p, l, c)
        if dbg2 and imap: self.cobj.dumpImap(imap, f=1)
        return imap
    ####################################################################################################################################################################################################
    def setIkey(self, imap, p, l, c, pos=1, dbg=0):
        cc    = self.plct2cc(p, l, c, 0)
        ikeys = imap[0] if imap else []
        if dbg: self.log(f'BGN ikeys={fmtl(ikeys)} {len(imap)=}', pos=pos)
        self.setIkeyText(ikeys, cc, p, l, c)
        if dbg: self.log(f'END ikeys={fmtl(ikeys)} {len(imap)=}', pos=pos)

    def setIkeyText(self, text, cc, p, l, c, pos=1, dbg=0, dbg2=0):
        nt  = self.n[T]  ;  cc = self.normalizeCC(cc)   ;   data = self.data[p][l][c]   ;   text = text[::-1]
        txt = self.objs2Text(self.ikeys, cc, nt, I)     ;   sobj = self.sobj  ;  blank = self.tblank  ;  j = 0
        if dbg:  self.log(f'BGN [{cc:2}-{cc+nt-1:2}] text={fmtl(text)} {data=} ikeys=<{txt}>{len(txt)}', pos=pos)
        for i in range(nt):
            if text and len(text) > j: ifd = sobj.isFret(data[i])  ;  self.ikeys[cc+i].text = text[j] if ifd else blank  ;  j += 1 if ifd else 0
            else:                                                     self.ikeys[cc+i].text = blank
        txt = self.objs2Text(self.ikeys, cc, nt, I)
        if dbg:  self.log(f'END [{cc:2}-{cc+nt-1:2}] text={fmtl(text)} {data=} ikeys=<{txt}>{len(txt)}', pos=pos)
        if dbg2: self.dumpDataSlice(p, l, c, cc)
    ####################################################################################################################################################################################################
    def setChord(self, imap, cc, pos=1, dbg=0):
#        cc = self.plct2cc(p, l, c, 0)
        name = imap[3] if imap and len(imap) > 3 else Z  ;   chunks = imap[4] if imap and len(imap) > 4 else []
        if dbg: self.log(f'BGN {name=} chunks={fmtl(chunks)} {len(imap)=}', pos=pos)
        self.setChordName(cc, name, chunks) # if name and chunks else self.log(f'WARN Not A Chord {cc=} {name=} {chunks=}', pos=pos)
        if dbg: self.log(f'END {name=} chunks={fmtl(chunks)} {len(imap)=}', pos=pos)

    def setChordName(self, cc, name, chunks, pos=1, dbg=0):
        nt  = self.n[T]   ;   cc = self.normalizeCC(cc)   ;   kords = self.kords
        txt = self.objs2Text(kords, cc, nt, K)
        if dbg: self.log(f'BGN [{cc:2}-{cc+nt-1:2}] {name=} chunks={fmtl(chunks)} chords=<{txt}>{len(txt)}', pos=pos)
        for i in range(nt):
            if chunks and len(chunks) > i:  self.kords[cc + i].text = chunks[i]
            else:                           self.kords[cc + i].text = self.tblank
        txt = self.objs2Text(kords, cc, nt, K)
        if dbg: self.log(f'END [{cc:2}-{cc+nt-1:2}] {name=} chunks={fmtl(chunks)} chords=<{txt}>{len(txt)}', pos=pos)
    @staticmethod
    def objs2Text(obs, cc, nt, j, dbg=0):
        assert cc + nt <= len(obs),  f'{cc=} {nt=} {len(obs)=}'
        texts = [ obs[cc + t].text for t in range(nt) ]    ;   text = Z.join(texts)
        if dbg: slog(f'{jTEXTS[j]}[{cc}-{cc+nt-1}].text={fmtl(texts)}=<{text}>')
        return text
    ####################################################################################################################################################################################################
    def on_style_text(   self, start, end, attributes): msg = f'{start=} {end=} {fmtm(attributes)}'  ;  self.log(msg)  ;  cmd = cmds.QuitCmd(self, msg)  ;  cmd.do()
    def isBTab(self, text):   return 1 if text in self.tblanks else 0
#   def isNBTab(text):        return 1 if                        self.sobj.isFret(text) or text in  utl.DSymb.SYMBS else 0
    def isTab(self, text):    return 1 if text == self.tblank or self.sobj.isFret(text) or text in misc.DSymb.SYMBS else 0
    def isParsing(self):      return 1 if self.inserting or self.jumping or self.settingN or self.shifting or self.swapping else 0
#   def isEH(t):              return 1 if t == '#' or t == 'b' else 0
    @staticmethod
    def afn(fn): return fn if len(fn) == 1 and '0' <= fn <= '9' else chr(ord(fn[1]) - ord('0') + ord('a')) if len(fn) == 2 and fn[0] == '1' else None
    ####################################################################################################################################################################################################
    def moveTo(self, how, p, l, s, c, t, ss=0, dbg=1):
        if dbg:    self.log(f'BGN {how}', pos=1)
        p2, l2, s2, c2, t2 = self.moveTo_(p, l, s, c, t)
        if self.cursor: cmd = cmds.MoveCursorCmd(self, ss, how)     ;  cmd.do()
        if dbg:         self.log(f'END {how}', pos=1)
        return p2, l2, s2, c2, t2

    def moveTo_(self, p, l, s, c, t, n=0, dbg=1): # todo
        p2, l2, s2, c2, t2 = self.trncPlsct(p, l, s, c, t+n)
        self.i[T] = t2 + 1
        self.i[C] = c2 + 1
        self.i[S] = s2 + 1
        self.i[L] = l2 + 1
        self.i[P] = p2 + 1
        if dbg: self.log(f'plsct={self.fplsct(p, l, s, c, t)} {n=} plsct2={self.fplsct(p2, l2, s2, c2, t2)} {self.fmti()}', pos=1)
        return p2, l2, s2, c2, t2

    def nrmPlsct(self, p, l, s, c, t): # N/A
        np, nl, ns, nc, nt = self.n
        t0 = int(t/nt)   ;   t2 = t0 % ns
#        c2 = t // nt + c
#        s2 = c // nc + s
        s2 = (s + t0) % ns
        l0 = int(s/ns)   ;   l2 = (l + l0) % nl
#        s2 = s + 1 if t / nt else s
#        l2 = l + 1 if s / ns >= ns else l
#        p2 = p + 1 if l // nl else p
        return p, l2, s2, c, t2

    def trncPlsct(self, p, l, s, c, t):
        np, nl, ns, nc, nt = self.n
        t2 = t % nt
        c2 = c % nc
        s2 = s % ns if ns else 0
        l2 = l % nl
        p2 = p % np
        return p2, l2, s2, c2, t2
    ####################################################################################################################################################################################################
    def selectAll(self, how, dbg=0):
        mli = self.cobj.mlimap
        if dbg: self.dumpSmap(f'BGN {how}')
        for k in mli:
            if k not in self.smap: cmd = cmds.SelectTabsCmd(self, how, cn=k, dbg=1)     ;  cmd.do()
        if dbg: self.dumpSmap(f'END {how}')

    def unselectAll(self, how, dbg=0):
        for i in range(len(self.smap)-1, -1, -1):
            cn = list(self.smap.keys())[i]
            if dbg: self.dumpSmap(f'{how} {i=} {cn=}')
            cmd = cmds.UnselectTabsCmd(self, how, m=0, cn=cn)     ;  cmd.do()
    ####################################################################################################################################################################################################
    def setLLStyle(self, cc, style, dbg=0):
        if not self.LL or not self.qclms: msg = f'SKIP {self.LL=} {len(self.qclms)=}'     ;  self.log(msg)  ;  cmd = cmds.QuitCmd(self, msg)  ;  cmd.do()
        p, l, c, t = self.cc2plct(cc)
        bold, italic = 0, 0   ;   np, nl, ns, nc, nt = self.n
        i = c + l * nc if self.qclms else 0
        if   style == NORMAL_STYLE:    bold = 0   ;  italic = 0
        elif style == CURRENT_STYLE:   bold = 0   ;  italic = 1
        elif style == SELECT_STYLE:    bold = 0   ;  italic = 0
        else: msg = f'ERROR Invalid style @ plct={self.fplct(p, l, c, t)} {i=} {style=}'  ;  self.log(msg)  ;  cmd = cmds.QuitCmd(self, msg)  ;  cmd.do()
        (bs, fs) = (0, 1) if style == NORMAL_STYLE else (1, 0)
        if self.qclms and len(self.qclms) > i:
            self.setFgcBgc(   self.qclms[i], self.llcolor(i, Q)[fs], self.llcolor(i, Q)[bs])
            d = self.qclms[i].document
            d.set_style(0, len(d.text), {COLOR: self.llcolor(i, Q)[fs], BGC: self.llcolor(i, Q)[bs]})
            self.qclms[i].bold   = bold
            self.qclms[i].italic = italic
        if dbg: self.log(f'     {i=} = {c=} + {l=} * {nc=} * {nt=} {style=} {bold=} {italic=} {cc=}', pos=1)
    ####################################################################################################################################################################################################
    def llcolor(self, i, j, dbg=0):
        nc = self.n[C]  ;   n = 1
        mp = i % nc + n
        msg = f'{i=} {j=} {nc=} {i%nc=} {n=} {mp=}=i%nc+n {mp%10=}' if dbg else Z
        if j == Q and not mp % 10: # and i:
            self.log(f'if   {msg} {self.k[R]=}') if dbg else None   ;   return self.k[R]
        self.log(    f'else {msg} {self.k[j]=}') if dbg else None   ;   return self.k[j]
    ####################################################################################################################################################################################################
    def setTNIKStyle(self, k, nt, style, text=Z, blank=0): # optimize str concat?
        for t in range(k, k + nt):
            msg = f'{t=} {k=} {nt=} {blank=}' #  {text=:{self.n[T]}
            if self.tabls: self.setTNIKStyle2(self.tabls[t], self.k[T], style)  ;  text += self.tabls[t].text
            if self.notes: self.setTNIKStyle2(self.notes[t], self.k[N], style)
            if self.ikeys: self.setTNIKStyle2(self.ikeys[t], self.k[I], style)
            if self.kords: self.setTNIKStyle2(self.kords[t], self.k[K], style)
            if blank: p, l, c, r = self.cc2plct(t)  ;  self.setDTNIK(self.tblank, t, p, l, c, t - k, kk=1 if t == k + nt - 1 else 0)
            self.log(f'{msg} {text=:{self.n[T]}}')
#            self.log(f'{t=} {k=} {nt=} {blank=} {text=}')
        return text

    def setTNIKStyle2(self, tnik, color, style=0): # d =  tnik.document ; d.set_style(0, len(d.text), {COLOR: color[fgs], BGC: color[bgs]})
        if ist(tnik, LBL):   (bgs, fgs) = (0, 1)  if style == NORMAL_STYLE or style == CURRENT_STYLE else (1, 0)   ;   self.setFgcBgc(tnik, color[fgs], color[bgs])
#        self.setFgcBgc(tnik, color[1], color[0])
    @staticmethod
    def setFgcBgc(t, fgc, bgc=None):
        cm = {COLOR:fgc}
        if bgc:            cm[BGC] = bgc
        d = t.document  ;  d.set_style(0, len(d.text), cm)
    ####################################################################################################################################################################################################
    def p2Js(self, p):
        np, nl, ns, nc, nt = self.n
        p,  l,  s,  c,  t  = p, p*nl, p*nl*ns, p*nl*ns*nc, p*nl*nc*nt
        j2 = [p,l,s,c,  t,t,t,t,  0,0,0,0,  0,0,0,0,0]
        j1 = [0,0,0,0,  0,0,0,0,  0,0,0,0,  0,0,0,0,0]
        self.log(f'j1={fmtl(j1)} j2={fmtl(j2)}')
        return j1, j2
    ####################################################################################################################################################################################################
    def dumpVisible(self):
        nmax, nsum = 0, 0  ;  a = W*3  ;  b = W*8  ;  c = W*7  ;  d = W*6  ;  e = W*5
        for j, e in enumerate(self.E):
            for k, e2 in enumerate(e):
                nsum += 1
                nmax += 1 if e2 and j==T else 0
                self.log(f'{int(e2.visible)}', p=0, e=Z)
            if len(e): self.log(p=0)
        v = Z.join([ f'{a if not i else b if i//10 < 1 else c if i//10 < 10 else d if i//10 < 100 else e}{10+i*10}' for i in range(nmax//10) ])
        self.log(f'{nsum:<7}{v}', p=0)
#        consume(consume(self.log(f'{int(self.E[j][i].visible)}', pfx=0, end=W) for i in range(len(self.E[j]))) for j in range(len(self.E)))
#        [ [ self.log(f'{int(self.E[j][i].visible)}', pfx=0, end=W) for i in range(len(self.E[j]))] for j in range(len(self.E)) ]
#        for j in range(len(self.E)):
#            for i in range(len(self.E[j])):
#                self.log(f'{int(self.E[j][i].visible)}', p=0, e=Z)
    ####################################################################################################################################################################################################
    @staticmethod
    def fVisible(n, j, l, v): return f'{n:4}{jTEXTS[j][0]}{l:<4} {v}'             # N/A not used??
    def fVis(self): return f'{fmtl([ int(p.visible) for p in self.pages ], s=Z)}' # N/A not used??
    ####################################################################################################################################################################################################
    def dumpCursorArrows(self, how): cm, ha, va = self.csrMode, self.hArrow, self.vArrow  ;  self.log(f'{how} csrMode={cm}={CSR_MODES[cm]:6} hArrow={ha}={HARROWS[ha]:5} vArrow={va}={VARROWS[va]:4}')

    def reverseArrow(self, bsp=0, dbg=1):
        if dbg: self.dumpCursorArrows('reverseArrow()')
        if self.csrMode in (MLDY, ARPG) or bsp: cmd = cmds.TogArrowCmd(self, 'reverseArrow() MELODY or ARPG or bsp', v=0)  ;  cmd.do() # self.flipArrow('reverseArrow() MELODY or ARPG or bsp', v=0)
        if self.csrMode in (CHRD, ARPG):        cmd = cmds.TogArrowCmd(self, 'reverseArrow()  CHORD or ARPG',        v=1)  ;  cmd.do() # self.flipArrow('reverseArrow()  CHORD or ARPG',        v=1)
        if dbg: self.dumpCursorArrows('reverseArrow()')
    ####################################################################################################################################################################################################
    def cci(self, j, k, kl, dbg=0):
        if k == 0:  self.ki[j] = (self.ki[j] + 1) % len(kl)
        kk   = (k + self.ki[j]) % len(kl)
        if dbg: self.log(f'.ki={fmtl(self.ki[:10])} {j=} {k=} kl={fmtl(kl)} {self.ki[j]=} {kk=}')
        return kk
    ####################################################################################################################################################################################################
    def regSnap(self, typ, why, dbg=1):
        self.snpC += 1
        snapReq = [self.snpC, typ, why]
        self.snapReqQ.put(snapReq)
        if dbg: self.log(f'{self.LOG_ID=:3} sid={snapReq[0]} typ={snapReq[1]:6} why={snapReq[2]} Qlen={self.snapReqQ.qsize()}')
    ####################################################################################################################################################################################################
    def deleteGlob(self, g, why=Z):
        self.log(f'deleting {len(g)} files from glob {why=}')
        for f in g:
            self.log(f)
            os.system(f'del {f}')
    ####################################################################################################################################################################################################
    def log(self, t=Z, p=1, pos=0, f=1, s=Y, e=X, ff=False):
        if pos:   t = f'{self.fmtPos()} {t}'
        slog(t, p, f, s, e, ff)

#    def olog(self, *o, p=1, pos=0, f=1, s=Y, e=X, ff=False):
#        if pos:   pos = f'{self.fmtPos()}'
#        olog((pos, o), p, f, s, e, ff)
    ####################################################################################################################################################################################################
    def cleanupFiles(self):
        self.cleanupCsvFile()
        self.cleanupCatFile() if self.cobj.umap else None

    def cleanupCsvFile(self):
        if not CSV_FILE.closed:
            self.log(f'Flush & Close {CSV_FILE.name}', ff=True)
            CSV_FILE.flush()     ;    CSV_FILE.close()
        csvPath  = utl.getFilePath(BASE_NAME,    BASE_PATH, fdir=CSVS, fsfx=CSV)
        csvPath2 = utl.getFilePath(self.CSV_GFN, BASE_PATH, fdir=None, fsfx=Z)
        csvPath3 = self.seqNumCsvPath
        self.log(f'Copying {CSV_FILE.name} to {csvPath2}', f=2)
        utl.copyFile(csvPath, csvPath2)
        self.makeSubDirs(csvPath3)
        self.log(f'Copying {CSV_FILE.name} to {csvPath3}', f=2)
        utl.copyFile(csvPath, csvPath3)

    def cleanupCatFile(self):
        fileName = self.fileNamePfx(CAT) + BASE_NAME
        catPath  = utl.getFilePath(BASE_NAME, BASE_PATH, fdir=CATS, fsfx=CAT)
        catPath1 = utl.getFilePath(fileName,  BASE_PATH, fdir=None, fsfx=CAT)
        catPath2 = utl.getFilePath(BASE_NAME, BASE_PATH, fdir=CATS, fsfx=CAT2)
        if self.CAT:
            with open(str(catPath), 'w', encoding='utf-8') as catFile:
                self.cobj.dumpOMAP(catPath, merge=1)
#                self.log(f'Flush & Close {catFile.name}', ff=True)
#                catFile.flush()     ;     catFile.close()
            catPath3 = self.seqNumCatPath
            self.log(f'Copying {catFile.name} to {catPath3}', f=2)
            utl.copyFile(catPath, catPath3)
        if catPath.exists():     utl.copyFile(catPath, catPath1);    utl.copyFile(catPath, catPath2)
########################################################################################################################################################################################################
# Global Functions BGN
########################################################################################################################################################################################################
def JLBL(n, d): return (f'{d.join(LLBL)}{d}'*n).removesuffix(d)
def JSPR(n, d): return (f'{d.join(LTXA)}{d}'*n).removesuffix(d)
########################################################################################################################################################################################################
def dumpGlobals():
    slog(f'BASE_NAME = {BASE_NAME}', f=2)
    slog(f'argv      = {fmtl(sys.argv, ll=1)}', f=2)
    slog(f'PATH      = {PATH}',      f=2)
    slog(f'BASE_PATH = {BASE_PATH}', f=2)
########################################################################################################################################################################################################
def cleanupOutFiles(file, fp, gfp, sqnp, f):
    slog(f'Copy {file.name} to {sqnp}',  ff=1, f=f)
    utl.copyFile(fp,            sqnp, f=f)
    slog(f'Copy {file.name} to {gfp}',  ff=1, f=f)
    utl.copyFile(fp,            gfp, f=f)
    slog('Flush & Close Txt File',      ff=1, f=f)
    file.flush()     ;     file.close()

def dumpFileInfo(f, fd):    slog(f'{fd=} {f.mode} {f.encoding} {f.name}')
########################################################################################################################################################################################################
# Global Functions END
########################################################################################################################################################################################################
# 0   1    2    3    4    5    6    7    8    9   10   11   12   13   14   15   16   17   18
FSH, PNK, RED, RST, ORG, PCH, YLW, LIM, GRN, TRQ, CYA, IND, BLU, VLT, GRY, CL1, CL2, CL3, CL4 = utl.initRGBs(f=0, dbg=0)
if CSV_PATH.exists():    utl.copyFile(CSV_PATH, CSV_PATH2, f=0)
if DAT_PATH.exists():    utl.copyFile(DAT_PATH, DAT_PATH2, f=0)
if EVN_PATH.exists():    utl.copyFile(EVN_PATH, EVN_PATH2, f=0)
if LOG_PATH.exists():    utl.copyFile(LOG_PATH, LOG_PATH2, f=0)
if PNG_PATH.exists():    utl.copyFile(PNG_PATH, PNG_PATH2, f=0)
if TXT_PATH.exists():    utl.copyFile(TXT_PATH, TXT_PATH2, f=0)
with open(str(LOG_PATH), 'w', encoding='utf-8') as LOG_FILE, open(str(CSV_PATH), 'w', encoding='utf-8') as CSV_FILE, open(str(TXT_PATH), 'w', encoding='utf-8') as TXT_FILE, open(str(EVN_PATH), 'w', encoding='utf-8') as EVN_FILE: # order?
    _    = -3
    ARGS = utl.init(CSV_FILE, EVN_FILE, LOG_FILE, TXT_FILE, f=_)
    notes.dumpData()   ;   notes.dumpData(csv=1)
    kysgs.init(f=2)
    slog(f'BGN {sys.argv[0]}', p=0,    f=_)
    slog(f'argv={fmtl(sys.argv[1:])}', f=_)
    utl.dumpRGB(f=_)
#   def main():
    dumpFileInfo(CSV_FILE, fd=_)
    dumpFileInfo(EVN_FILE, fd=_)
    dumpFileInfo(LOG_FILE, fd=_)
    dumpFileInfo(TXT_FILE, fd=_)
    slog('Constructing Tabs object', f=-3)
    tabs = Tabs()  ;  seqNumLogPath = tabs.seqNumLogPath  ;  seqNumTxtPath = tabs.seqNumTxtPath
    slog(f'{str(tabs)=}', f=_)   ;   slog(f'{tabs=}', f=_)
    slog('Call pyglet.app.run()')
    pyglet.app.run()
    slog('Thats all folks!', ff=1, f=_)
    slog(f'END {sys.argv[0]}',     f=_)
    geomLogPath = utl.getFilePath(tabs.LOG_GFN, BASE_PATH, fdir=None, fsfx=Z)
    geomTxtPath = utl.getFilePath(tabs.TXT_GFN, BASE_PATH, fdir=None, fsfx=Z)
    cleanupOutFiles(TXT_FILE, TXT_PATH, geomTxtPath, seqNumTxtPath, f=_)
    cleanupOutFiles(LOG_FILE, LOG_PATH, geomLogPath, seqNumLogPath, f=-1)
########################################################################################################################################################################################################
#    if __name__ == '__main__':
#        main()
########################################################################################################################################################################################################
#--disable=C0301 --disable=C0304 --disable=C0321 --disable=C0115 --disable=C0116 --disable=R0912 --disable=R0913 --disable=R0914 tabs.py utl.py chord.py
