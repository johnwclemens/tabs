import glob, math, os, pathlib, sys
import operator, inspect, itertools
from itertools      import accumulate
from more_itertools import consume
CODS    = 0
if CODS: from collections import OrderedDict as cOd
from          collections import Counter
import pyglet
import pyglet.font         as pygfont
import pyglet.sprite       as pygsprt
import pyglet.text         as pygtxt
import pyglet.window.event as pygwine
import pyglet.window.key   as pygwink
import util, chord
#from util import KeySig    as KS
from util import Notes     as Notes
from util import slog      as slog
from util import olog      as olog
from util import fmtl      as fmtl
from util import fmtm      as fmtm

W, Y, Z               = ' ', ',', ''
P, L, S, C            =  0,  1,  2,  3
T, N, I, K            =  4,  5,  6,  7
R, Q, H, M            =  8,  9, 10, 11
B, A, D, E            = 12, 13, 14, 15
ARGS = util.parseCmdLine()

########################################################################################################################################################################################################
class Tabs(pyglet.window.Window):
####################################################################################################################################################################################################
    def __init__(self):
        self.LOG_ID = 1                ;   self.log(f'{self.LOG_ID=}')
        self.log(f'BGN {__class__}')   ;   dumpGlobals()
        self.log(f'STFILT:\n{fmtl(util.STFILT)}')          ;   self.snapWhy, self.snapType, self.snapReg, self.snapId = '?', '_', 0, 0
        self.fNameLid      = self.getFileSeqName(fdir=LOGS, fsfx=LOG)
        self.seqNumLogPath = util.getFilePath(self.fNameLid, BASE_PATH, fdir=LOGS, fsfx=LOG)   ;   self.log(f'{self.seqNumLogPath=}')
        self.seqNumCsvPath = util.getFilePath(self.fNameLid, BASE_PATH, fdir=CSVS, fsfx=CSV)   ;   self.log(f'{self.seqNumCsvPath=}')
        self.seqNumCatPath = util.getFilePath(self.fNameLid, BASE_PATH, fdir=CATS, fsfx=CAT)   ;   self.log(f'{self.seqNumCatPath=}')
        self.settingN      = 0   ;   self.setNvals  = []   ;   self.setNtxt  = Z
        self.shiftingTabs  = 0   ;   self.shiftSign = 1    ;   self.quitting = 0
        self.inserting     = 0   ;   self.insertStr = Z
        self.jumping       = 0   ;   self.jumpStr   = Z    ;   self.jumpAbs  = 0
        self.swapping      = 0   ;   self.swapSrc   = Z    ;   self.swapTrg  = Z
        self.newC          = 0   ;   self.updC      = 0
        self.cc            = 0   ;   self.nvis      = 0    ;   self.kbk      = 0
        self.allTabSel     = 0   ;   self.rsyncData = 0    ;   self.sprs     = []
        self.ki            = []  ;   self.ks        = [ W, 0, Notes.NONE, 'C', 0, [], [] ]
        self.symbStr,  self.modsStr,  self.symb,    self.mods    = Z, Z, 0, 0
        self.J1,       self.J2,       self.j1s,     self.j2s     = [], [], [], []
        self.hArrow,   self.vArrow,   self.csrMode, self.tids    = RARROW, UARROW, CHORD, set()   ;   self.dumpCursorArrows('init()')
        self.tblank,   self.tblanki,  self.cursor,  self.data    = None, None, None, []
        self.XYVA      = [0, 0, 0, 0]
        self.AX        = self.XYVA[0]
        self.AY        = self.XYVA[1]
        self.VA        = self.XYVA[2]
        self.AA        = self.XYVA[3]
        self.A_LEFT    = 1  if self.AA==-1 else 0  ;  self.A_CENTER = 1  if self.AA==0  else 0  ;  self.A_RIGHT  = 1 if self.AA==1 else 0
        self.X_LEFT    = 1  if self.AX==-1 else 0  ;  self.X_CENTER = 1  if self.AX==0  else 0  ;  self.X_RIGHT  = 1 if self.AX==1 else 0
        self.Y_BOTTOM  = 1  if self.AY==-1 else 0  ;  self.Y_CENTER = 1  if self.AY==0  else 0  ;  self.Y_TOP    = 1 if self.AY==1 else 0  ;  self.Y_BASELINE = 1 if self.AY==2 else 0
        self.V_BOTTOM  = 1  if self.VA==-1 else 0  ;  self.V_CENTER = 1  if self.VA==0  else 0  ;  self.V_TOP    = 1 if self.VA==1 else 0
        self.AUTO_SAVE = 0  ;  self.BGC       = 0  ;  self.CAT      = 1  ;  self.CHECKERED = 0  ;  self.CURSOR   = 1
        self.DBG_TABT  = 0  ;  self.EVENT_LOG = 0  ;  self.FRT_BRD  = 0  ;  self.FULL_SCRN = 0  ;  self.GEN_DATA = 0
        self.LONG_TXT  = 1  ;  self.MULTILINE = 1  ;  self.OIDS     = 0  ;  self.ORD_GRP   = 1  ;  self.PIDX     = 0
        self.RESIZE    = 1  ;  self.SNAPS     = 1  ;  self.SPRITES  = 1  ;  self.STRETCH   = 0  ;  self.SUBPIX   = 1
        self.TEST      = 0  ;  self.TEST_EXIT = 0  ;  self.VARROW   = 1  ;  self.VIEWS     = 0  ;  self.VRBY     = 0
        self.LL        = 0
        self.SS        = set(range(4))  # set() if 0 else {0, 1, 2, 3}
        self.ZZ        = set()          # set() if 1 else {0} #, 1}
        self.idmap     = cOd() if CODS else {}  ;  self.log(f'{CODS=} {type(self.idmap)=}')
        self.p0x, self.p0y, self.p0w, self.p0h, self.p0sx, self.p0sy = 0, 0, 0, 0, 0, 0
        self.n         = [1, 1, 10, 6]
        self.i         = [1, 1,  1, 6]
        self.log(f'argMap={fmtm(ARGS)}')   ;    self.FILE_NAME  = BASE_NAME
        ####################################################################################################################################################################################################
        if 'a' in ARGS and len(ARGS['a']) == 0: self.AUTO_SAVE  =  1
        if 'A' in ARGS: l = len(ARGS['A'])   ;  self.VARROW     =  1 if l == 0 else int(ARGS['A'][0]) if l == 1 else 0
        if 'b' in ARGS and len(ARGS['b']) == 0: self.FRT_BRD    =  1
        if 'B' in ARGS and len(ARGS['B']) == 0: self.BGC        =  1
        if 'c' in ARGS and len(ARGS['c']) == 0: self.CAT        =  1
        if 'C' in ARGS and len(ARGS['C']) == 0: self.CHECKERED  =  1
        if 'd' in ARGS and len(ARGS['d'])  > 0: self.DBG_TABT   =  ARGS['d'][0]
        if 'e' in ARGS and len(ARGS['e']) == 0: self.EVENT_LOG  =  1
        if 'f' in ARGS and len(ARGS['f'])  > 0: self.FILE_NAME  =  ARGS['f'][0]
        if 'F' in ARGS and len(ARGS['F']) == 0: self.FULL_SCRN  =  1
        if 'g' in ARGS and len(ARGS['g']) == 0: self.ORD_GRP    =  1
        if 'G' in ARGS and len(ARGS['G']) == 0: self.GEN_DATA   =  1
        if 'i' in ARGS and len(ARGS['i'])  > 0: self.i          = [ int(ARGS['i'][i]) for i in range(len(ARGS['i'])) ]
        if 'I' in ARGS and len(ARGS['I']) == 0: self.PIDX       =  1
        if 'L' in ARGS and len(ARGS['L']) == 0: self.LL         =  1
        if 'M' in ARGS and len(ARGS['M']) == 0: self.MULTILINE  =  1
        if 'n' in ARGS and len(ARGS['n'])  > 0: self.n          = [ int(ARGS['n'][i]) for i in range(len(ARGS['n'])) ]
        if 'o' in ARGS and len(ARGS['o']) == 0: self.OIDS       =  1
        if 'p' in ARGS and len(ARGS['p']) == 0: self.SNAPS      =  1
        if 'q' in ARGS and len(ARGS['q']) == 0: self.TEST_EXIT  =  1
        if 'R' in ARGS and len(ARGS['R']) == 0: self.RESIZE     = 0
        if 's' in ARGS and len(ARGS['s']) == 0: self.SPRITES    =  1
        if 'S' in ARGS and len(ARGS['S']) >= 0: self.SS         = { int(ARGS['S'][i]) for i in range(len(ARGS['S'])) }
        if 't' in ARGS and len(ARGS['t']) == 0: self.TEST       =  1
        if 'T' in ARGS and len(ARGS['T']) == 0: self.LONG_TXT   =  1
        if 'u' in ARGS and len(ARGS['u']) == 0: self.SUBPIX     =  1
        if 'v' in ARGS: l = len(ARGS['v'])   ;  self.VRBY       =  1 if l == 0 else int(ARGS['v'][0]) if l == 1 else 0
        if 'V' in ARGS and len(ARGS['V']) == 0: self.VIEWS      =  1
        if 'w' in ARGS and len(ARGS['w'])  > 0: self.XYVA       = [ int(ARGS['w'][i]) for i in range(len(ARGS['w'])) ]
        if 'Z' in ARGS and len(ARGS['Z']) >= 0: self.ZZ         = { int(ARGS['Z'][i]) for i in range(len(ARGS['Z'])) }
        self.AX        = self.XYVA[0]
        self.AY        = self.XYVA[1]
        self.VA        = self.XYVA[2]
        self.AA        = self.XYVA[3]
        self.A_LEFT    = 1  if self.AA==-1 else 0  ;  self.A_CENTER = 1  if self.AA==0  else 0  ;  self.A_RIGHT  = 1 if self.AA==1 else 0
        self.X_LEFT    = 1  if self.AX==-1 else 0  ;  self.X_CENTER = 1  if self.AX==0  else 0  ;  self.X_RIGHT  = 1 if self.AX==1 else 0
        self.Y_BOTTOM  = 1  if self.AY==-1 else 0  ;  self.Y_CENTER = 1  if self.AY==0  else 0  ;  self.Y_TOP    = 1 if self.AY==1 else 0  ;  self.Y_BASELINE = 1 if self.AY==2 else 0
        self.V_BOTTOM  = 1  if self.VA==-1 else 0  ;  self.V_CENTER = 1  if self.VA==0  else 0  ;  self.V_TOP    = 1 if self.VA==1 else 0
        ####################################################################################################################################################################################################
        self.n0        = list(self.n)        ;  self.i0         =  list(self.i)
        self.n.insert(S, self.ssl())         ;  self.i.insert(S, 1)         ;  self.dumpArgs(f=2)
        self.LOG_GFN   = self.geomFileName(LOG, self.FILE_NAME)             ;  self.log(f'{self.LOG_GFN=}')
        self.CSV_GFN   = self.geomFileName(CSV, self.FILE_NAME)             ;  self.log(f'{self.CSV_GFN=}')
        self.DAT_GFN   = self.geomFileName(DAT, self.FILE_NAME, n=self.n0)  ;  self.log(f'{self.DAT_GFN=} {self.n0=}')
        self.vArrow    = UARROW if self.VARROW == 1 else DARROW
        self.fontStyle = NORMAL_STYLE
        self.sAlias    = 'GUITAR_6_STD'
        self.k         = {}
        ####################################################################################################################################################################################################
        self.sobj      = util.Strings(self.sAlias)
        self.cobj      = chord.Chord(self, self.sobj)
        ####################################################################################################################################################################################################
        self._initDataPath()
        self._initWindowA()
        self.log(f'WxH={self.fmtWH()}')
        super().__init__(screen=self.screens[self.screenIdx], fullscreen=self.FULL_SCRN, resizable=True, visible=False)
        self.log(f'WxH={self.fmtWH()}')
        self._initWindowB()
        self.log(f'WxH={self.fmtWH()}')
        self.aa = LEFT   if self.A_LEFT   else CENTER if self.A_CENTER else RIGHT if self.A_RIGHT else '???'
        self.ax = LEFT   if self.X_LEFT   else CENTER if self.X_CENTER else RIGHT if self.X_RIGHT else '???'
        self.ay = BOTTOM if self.Y_BOTTOM else CENTER if self.Y_CENTER else TOP   if self.Y_TOP   else BASELINE if self.Y_BASELINE else '???'
        self.va = BOTTOM if self.V_BOTTOM else CENTER if self.V_CENTER else TOP   if self.V_TOP   else '???'
        self.dumpAXY()
        self._reinit()
        self.log(util.INIT, p=0)
        self.log(f'END {__class__}')
    ####################################################################################################################################################################################################
    def __str__(self):  return f'{ARGS}'
    def __repr__(self): return f'{self.__class__.__name__} {self.width=} {self.height=} {ARGS=}'
    ####################################################################################################################################################################################################
    def geomFileName(self, ext, base=None, n=None):
        n = self.n if n is None else n  ;  _ = [base] if base is not None else [BASE_NAME]  ;  _.extend([ str(i) for i in n ])  ;  _.append(ext)  ;  return '.'.join(_) # base.p.l.c.t.ext

    def dumpArgs(self, f=1):
        self.log(f'[a]      {self.AUTO_SAVE=}', f=f)
        self.log(f'[A]         {self.VARROW=}', f=f)
        self.log(f'[b]        {self.FRT_BRD=}', f=f)
        self.log(f'[B]            {self.BGC=}', f=f)
        self.log(f'[c]            {self.CAT=}', f=f)
        self.log(f'[C]      {self.CHECKERED=}', f=f)
        self.log(f'[d]       {self.DBG_TABT=}', f=f)
        self.log(f'[e]      {self.EVENT_LOG=}', f=f)
        self.log(f'[f]      {self.FILE_NAME=}', f=f)
        self.log(f'[F]      {self.FULL_SCRN=}', f=f)
        self.log(f'[g]        {self.ORD_GRP=}', f=f)
        self.log(f'[G]       {self.GEN_DATA=}', f=f)
        self.log(f'[i]               {self.fmti()}', f=f)
        self.log(f'[I]           {self.PIDX=}', f=f)
        self.log(f'[L]             {self.LL=}', f=f)
        self.log(f'[M]      {self.MULTILINE=}', f=f)
        self.log(f'[n]               {self.fmtn()}', f=f)
        self.log(f'[o]           {self.OIDS=}', f=f)
        self.log(f'[p]          {self.SNAPS=}', f=f)
        self.log(f'[q]      {self.TEST_EXIT=}', f=f)
        self.log(f'[R]         {self.RESIZE=}', f=f)
        self.log(f'[s]        {self.SPRITES=}', f=f)
        self.log(f'[S]             .SS={fmtl(self.SS)}', f=f)
        self.log(f'[t]           {self.TEST=}', f=f)
        self.log(f'[T]       {self.LONG_TXT=}', f=f)
        self.log(f'[u]         {self.SUBPIX=}', f=f)
        self.log(f'[v]           {self.VRBY=}', f=f)
        self.log(f'[V]          {self.VIEWS=}', f=f)
        self.log(f'[w]           {self.XYVA=}', f=f)
        self.log(f'[Z]             .ZZ={fmtl(self.ZZ)}', f=f)
    ####################################################################################################################################################################################################
    def _reinit(self):
        self.log('BGN')
        self.tpb, self.tpp, self.tpl, self.tps, self.tpc = self.ntp(dbg=1, dbg2=1)
        self.data  = []   ;   self.visib = []    ;    self.nic = Counter()
        self.pages, self.lines, self.sects, self.colms = [], [], [], []  ;  self.A = [self.pages, self.lines, self.sects, self.colms]
        self.tabls, self.notes, self.ikeys, self.kords = [], [], [], []  ;  self.B = [self.tabls, self.notes, self.ikeys, self.kords]
        self.rowLs, self.qclms, self.hcurs, self.views = [], [], [], []  ;  self.C = [self.rowLs, self.qclms, self.hcurs, self.views]
        self.zclms, self.snums, self.snams, self.capos = [], [], [], []  ;  self.D = [self.zclms, self.snums, self.snams, self.capos]
        self.E     = [*self.A, *self.B, *self.C, *self.D]       ;     self.log(f'E={fmtl(self.E, d=" [", d2="] ")}')
        self.resetJ('_reinit')
        self.cc,   self.kbk,  self.cursor,  self.caret   = 0, 0, None, None
        self.symb, self.mods, self.symbStr, self.modsStr = 0, 0, Z, Z
        self.ki    = [ 0 for _ in range(len(self.E)) ]           ;    self.log(fmtl(self.ki))
        self.tblanki, self.tblanks  = 1, [W, '-']                ;    self.tblank    = self.tblanks[self.tblanki]
        self.tblankCol              = self.tblank * self.n[T]    ;    self.tblankRow = self.tblank * (self.n[C] + self.zzl())
        self.dumpBlanks()
        self._init()
        self.log('END', pos=1)

    def _init(self):
        self._initColors()
        self._initData()
        if self.AUTO_SAVE: pyglet.clock.schedule_interval(self.autoSave, 10, how='autoSave timer')
        self._initFonts()
        self._initTextLabels()
        self._initTniks()
        if self.SNAPS: self.regSnap('init', 'Init')
    ####################################################################################################################################################################################################
    def _initColors(self): # j = M = 11
        KP1, KP2 = VLT, VLT  ;  KL1, KL2 = RED, RED  ;  KS1, KS2 = CYA, CYA  ;  KC1, KC2 = RST, RST
        KT1, KT2 = ORG, ORG  ;  KN1, KN2 = GRN, GRN  ;  KI1, KI2 = YLW, YLW  ;  KK1, KK2 = IND, IND
        KR1, KR2 = BLU, BLU  ;  KQ1, KQ2 = GRY, GRY  ;  KH1, KH2 = YLW, YLW  ;  KM1, KM2 = GRN, GRN
        KB1, KB2 = PNK, PNK  ;  KA1, KA2 = BLU, BLU  ;  KD1, KD2 = FSH, FSH  ;  KE1, KE2 = VLT, VLT
        k = self.k  ;  a = not self.SPRITES and not self.BGC  ;  b = not self.SPRITES and self.BGC  ;  c =   self.SPRITES and not self.BGC  ;  d = self.SPRITES and self.BGC  ;  i = self.initk
        j = P  ;  k[j] = i(j, KP1, 17, 17, KP2,  3, 17) if a else i(j, KP1,  3, 17, KP2, 17, 17) if b else i(j, KP1,  3, 17, KP2, 17, 17) if c else i(j, KP1,  3, 17, KP2, 17, 17) if d else None
        j = L  ;  k[j] = i(j, KL1, 17, 15, KL2,  3, 15) if a else i(j, KL1,  3, 15, KL2, 17, 15) if b else i(j, KL1,  3, 15, KL2, 17, 15) if c else i(j, KL1,  3, 15, KL2, 17, 15) if d else None
        j = S  ;  k[j] = i(j, KS1, 17, 15, KS2,  3, 15) if a else i(j, KS1,  3, 15, KS2, 17, 15) if b else i(j, KS1,  3, 15, KS2, 17, 15) if c else i(j, KS1,  3, 15, KS2, 17, 15) if d else None
        j = C  ;  k[j] = i(j, KC1, 17, 15, KC2,  3, 15) if a else i(j, KC1,  3, 15, KC2, 17, 15) if b else i(j, KC1,  3, 15, KC2, 17, 15) if c else i(j, KC1,  3, 15, KC2, 17, 15) if d else None
        j = T  ;  k[j] = i(j, KT1,  3, 13, KT2, 17, 13) if a else i(j, KT1,  3, 13, KT2, 17, 13) if b else i(j, KT1,  0, 13, KT2, 17, 13) if c else i(j, KT1,  3, 13, KT2, 17, 13) if d else None
        j = N  ;  k[j] = i(j, KN1,  3, 13, KN2, 17, 13) if a else i(j, KN1,  3, 13, KN2, 17, 13) if b else i(j, KN1,  3, 13, KN2, 17, 13) if c else i(j, KN1,  3, 13, KN2, 17, 13) if d else None
        j = I  ;  k[j] = i(j, KI1,  3, 13, KI2, 17, 13) if a else i(j, KI1,  3, 13, KI2, 17, 13) if b else i(j, KI1,  3, 13, KI2, 17, 13) if c else i(j, KI1,  3, 13, KI2, 17, 13) if d else None
        j = K  ;  k[j] = i(j, KK1,  3, 13, KK2, 17, 13) if a else i(j, KK1,  3, 13, KK2, 17, 13) if b else i(j, KK1,  3, 13, KK2, 17, 13) if c else i(j, KK1,  3, 13, KK2, 17, 13) if d else None
        j = R  ;  k[j] = i(j, KR1, 17, 17, KR2, 17, 17) if a else i(j, KR1, 17, 17, KR2, 17, 17) if b else i(j, KR1, 17, 17, KR2, 17, 17) if c else i(j, KR1, 17, 17, KR2, 17, 17) if d else None
        j = Q  ;  k[j] = i(j, KQ1,  3, 10, KQ2, 17, 10) if a else i(j, KQ1,  3, 10, KQ2, 17, 10) if b else i(j, KQ1,  3, 10, KQ2, 17, 10) if c else i(j, KQ1,  3, 10, KQ2, 17, 10) if d else None
        j = H  ;  k[j] = i(j, KH1, 17, 11, KH2, 17, 10) if a else i(j, KH1, 14, 10, KH2, 14, 10) if b else i(j, KH1, 15, 13, KH2, 15, 13) if c else i(j, KH1, 14, 11, KH2, 14, 10) if d else None
        j = M  ;  k[j] = i(j, KM1, 17, 11, KM2, 17, 10) if a else i(j, KM1, 17, 10, KM2, 17, 17) if b else i(j, KM1, 17, 17, KM2, 17, 17) if c else i(j, KM1, 17, 17, KM2, 17, 17) if d else None
        j = B  ;  k[j] = i(j, KB1,  0,  0, KB2, 17, 17) if a else i(j, KB1,  0,  0, KB2, 17, 17) if b else i(j, KB1,  0,  0, KB2, 17, 17) if c else i(j, KB1,  0,  0, KB2, 17, 17) if d else None
        j = A  ;  k[j] = i(j, KA1,  0,  0, KA2, 17, 17) if a else i(j, KA1,  0,  0, KA2, 17, 17) if b else i(j, KA1,  0,  0, KA2, 17, 17) if c else i(j, KA1,  0,  0, KA2, 17, 17) if d else None
        j = D  ;  k[j] = i(j, KD1,  0,  0, KD2, 17, 17) if a else i(j, KD1,  0,  0, KD2, 17, 17) if b else i(j, KD1,  0,  0, KD2, 17, 17) if c else i(j, KD1,  0,  0, KD2, 17, 17) if d else None
        j = E  ;  k[j] = i(j, KE1,  0,  0, KE2, 17, 17) if a else i(j, KE1,  0,  0, KE2, 17, 17) if b else i(j, KE1,  0,  0, KE2, 17, 17) if c else i(j, KE1,  0,  0, KE2, 17, 17) if d else None

    def initk(self, j, key0, rgb0, opc0, key1, rgb1, opc1):
        self.log(f'{j:2}  {JTEXTS[j]:4}  [{key0} {rgb0:2} {opc0:2}] [ {key1} {rgb1:2} {opc1:2}] {fmtl(RGB[key0][rgb0][opc0], w=3)} {fmtl(RGB[key1][rgb1][opc1], w=3)}', p=0)
        return [RGB[key0][rgb0][opc0], RGB[key1][rgb1][opc1]]
    ####################################################################################################################################################################################################
    def _initData(self, dbg=1):
        self._initDataPath()
        if self.GEN_DATA or not self.dataPath1.exists():  self.genDataFile(self.dataPath1)
        self.readDataFile(self.dataPath1)
        util.copyFile(    self.dataPath1, self.dataPath2)
        self.data = self.transposeData(dump=1 if dbg else 0)
        old       = self.fmtn(Z)
        self.n[P] = self.dl()[0]
        self.log(self.fmtdl())
        self.log(f'Updating n[P] {old=} {self.fmtn()}')
        self.tpb, self.tpp, self.tpl, self.tps, self.tpc = self.ntp(dbg=1, dbg2=1)

    def _initDataPath(self):
        dataDir   = DATA
        dataName0 = self.DAT_GFN + '.asv'
        dataName1 = self.DAT_GFN
        dataName2 = self.DAT_GFN + '.bck'
        self.dataPath0 = BASE_PATH / dataDir / dataName0
        self.dataPath1 = BASE_PATH / dataDir / dataName1
        self.dataPath2 = BASE_PATH / dataDir / dataName2
        self.makeSubDirs(self.dataPath1)
        self.log(f'{dataName0=}')
        self.log(f'{dataName1=}')
        self.log(f'{dataName2=}')
        self.log(f'{self.dataPath0=}', p=0)
        self.log(f'{self.dataPath1=}', p=0)
        self.log(f'{self.dataPath2=}', p=0)

    def makeSubDirs(self, path):
        if not path.parent.exists():
            self.log(f'WARN Invalid Data File Path {path.parent=} -> mkdir', f=2)
            path.parent.mkdir(parents=True, exist_ok=True)
            if not path.parent.exists():    msg = f'ERROR mkdir failed on {path.parent=}'  ;  self.log(msg)  ;  self.quit(msg)
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

    def _initWindowB(self, dbg=1):
        if dbg: self.log(f'BGN {self.fmtWH()}')
        self.batch = pyglet.graphics.Batch()
        self._initGroups()
        self.set_visible()
        self.log(f'get_size={self.get_size()}')
        if self.EVENT_LOG:
            self.eventLogger = pygwine.WindowEventLogger()
            self.push_handlers(self.eventLogger)
            self.keyboard    = pygwine.key.KeyStateHandler()
            self.push_handlers(self.keyboard)
        if dbg: self.log(f'END {self.fmtWH()}')
    ####################################################################################################################################################################################################
    def _initGroups(self):
        hdrA    = [P, L, S, C,  T, N, I, K,  R, Q, H, M,  B, A, D, E]
        hdrB    = W.join([ f'{t[0]:2}' for t in JTEXTS ])
        self.gn = [1, 2, 3, 4,  5, 5, 5, 5,  6, 7, 8, 0,  6, 6, 6, 6]  ;  self.g = []
        self.log(fmtl(hdrA, w=2))  ;  self.log(f'  {hdrB}')  ;  self.log(fmtl(self.gn, w=2))
        for i in range(1+max(self.gn)):
            p   = None if self.ORD_GRP or i==0 else self.g[i-1]
            self.g.append(self._initGroup(i, p))
            self.log(f'g[{i}]={self.g[i]} p={self.g[i].parent}')
    def _initGroup(self, order=0, parent=None): return pyglet.graphics.OrderedGroup(order, parent) if self.ORD_GRP else pyglet.graphics.Group(parent)
    ####################################################################################################################################################################################################
    def _initTextLabels(self):
        self.labelTextA, self.labelTextB = [], []
        self.createLabelText()
        self.llText = ['M', '0']
        self.llText.extend(self.labelTextB)
        self.log(fmtl(self.llText))
    ####################################################################################################################################################################################################
    def _initTniks(self):
        self.ssl()      ;   self.smap = {}
        self.log(self.fAxy())   ;   self.log(self.fmtAxy())
        [ self.visib.append([]) for _ in range(len(JTEXTS)) ]
        self.createTniks()
        self.ks = util.nic2KS(self.nic)
        self.log( util.fmtKSK(self.ks[util.KSK]), f=2)
        if self.TEST: self.test1(self.TEST_EXIT)
    ####################################################################################################################################################################################################
    def test(self): #        self.olog('test', a, p=1)
        a = 1/0  ;  self.log(f'{a=}')
        p = self.pages  ;  f = CSV_FILE
        a = [{'a':1, 'b':"2", 'c':3.00+1/3}]  ;  b = [ f'{p[i].y}' for i in range(len(p)) ]  ;  c = self.sobj.stringMap  ;  d = [ self.screens ]
        print(self.__class__.__name__, 'testA', a, sep=Y, file=f, end=Y)
        print(self.__class__.__name__, 'testB', b, sep=Y, file=f, end=Y)
        print(self.__class__.__name__, 'testC', c, sep=Y, file=f)
        print(self.__class__.__name__, 'testD', d, sep=Y, file=f)
        self.quit(Z.join(('test', str(a))))

    def exitTest(self, why, e): #        self.dispatch_event('on_close')
        self.log(f'BGN {why} {e}')
        self.dispatch_event('on_key_press', 65507, 2)
        self.dispatch_event('on_key_press', 65505, 3)
        self.dispatch_event('on_key_press',   113, 3)
        self.log(f'END {why} {e}')

#    def testSprTxt_0(self, path):
#        np, nl, ns, nc, nt = self.n  ;  r, c = nt*ns*nl, nc
#        self.log(f'BGN {path=} {r=} {c=}')
#        lbl = self.tabls[0]
#        tex = self.batch.get_texture()
#        spr = SPR(tex, x=100, y=100, batch=self.batch, group=self.j2g(H), subpixel=self.SUBPIX)
#        spr.anchor_x, spr.anchor_y = self.axyWgt(self.ax, self.ay)

    def testSprTxt_1(self, path):
        np, nl, ns, nc, nt = self.n  ;  r, c = nt*ns*nl, nc
#        t = self.tabls[0]  ;  doc = t.document  ;  m = doc.styles  ;  font = pygfont.load(m[FONT_NAME], m[FONT_SIZE])
#        ssPath = self.snapshot('text img for Sprites', 'SPRTXT')
        self.log(f'BGN {path=} {r=} {c=}')
        img = pyglet.image.load(path)
        ig = pyglet.image.ImageGrid(img, r, c)
        itg = pyglet.image.TextureGrid(ig)
        self.log(f'{img=}')
        self.log(f' {ig=}')
        self.log(f'{itg=}')
        ds = ig[0:10]
        for j, d in enumerate(ds):
            self.log(f'ds[{j}]=d={d}')
            fname = f'd_{j}.png'
            d.save(fname)
        self.log(f'END {path=} {r=} {c=}')

    def testSprTxt_2(self, path):
        np, nl, ns, nc, nt = self.n  ;  r, c = nt*ns*nl, nc
        self.log(f'BGN {path=} {r=} {c=}')
        img = pyglet.image.load(path)
        spr = SPR(img, x=100, y=100, batch=self.batch, group=self.j2g(H), subpixel=self.SUBPIX)
        spr.anchor_x, spr.anchor_y = self.axyWgt(self.ax, self.ay)
        self.sprs.append(spr)

    def testSprTxt_3(self): # , path):
        np, nl, ns, nc, nt = self.n  ;  r, c = 1, nc # nt*ns*nl, nc
        path = util.getFilePath('testA', BASE_PATH, PNGS, PNG)
        self.log(f'BGN {path=} {r=} {c=}')
        pimg = pyglet.image.load(path)
        ig = pyglet.image.ImageGrid(pimg, r, c)
        spr = SPR(ig[2], x=300, y=200, batch=self.batch, group=self.j2g(H), subpixel=self.SUBPIX)
        spr.anchor_x, spr.anchor_y = self.axyWgt(self.ax, self.ay)
        self.sprs.append(spr)
        self.log(f'END {path=} {r=} {c=}')
        #Install pillow for SVG files

    def test1(self, q=0):
        self.log(f'{    TI=}')
        self.log(f'{  XYWH=}')
        self.log(f'{  AXY2=}')
        self.log(f'{  WHVA=}')
        self.log(f'{  LTXX=}')
        self.log(f'{LTXXCA=}')
        self.log(f'{   ADN=}')
        self.log(f'{   LDS=}')
        self.log(f'{  LLBL=}')
        self.log(f'{  LLBL}', p=0)
        self.log(f'J{Y.join(   TI)=}')
        self.log(f'J{Y.join(  XYWH)=}')
        self.log(f'J{Y.join(  AXY2)=}')
        self.log(f'J{Y.join(  LTXX)=}')
        self.log(f'J{Y.join(LTXXCA)=}')
        self.log(f'J{Y.join(  ADN)=}')
        self.log(f'J{Y.join(  LDS)=}')
        self.log(f'J{Y.join( LLBL)=}')
        self.log(f' {Y.join( LLBL)}', p=0)
        self.log(f'{JSPR(2, Y)=}')
        self.log(f'{JLBL(2, Y)=}')
        self.log(f'{JSPR(2, Y)}', p=0)
        self.log(f'{JLBL(2, Y)}', p=0)
        if q:    self.exitTest('test1', 0)
####################################################################################################################################################################################################
    def testA(self, j=10):
        self.log(f'{self.ntsl()=}')
        hdrA = '      cc [  tpb  tpp tpl tps tpc] [p l s  c t]'
        hdrB = ' cn   cc [  tpb  tpp tpl tps tpc] [p l s  c t]'
        hdrC = '  cc  cn [  tpb  tpp tpl tps tpc] [p l s  c t]'
        np, nl, ns, nc, nt = self.i #  ;   p, l, c = 0, 0, 0
        self.dumpTniksPfx(f'BGN {j=} test', r=0)
        self.log(hdrB)
        for p in range(np):
            for l in range(nl):
                for _ in range(ns):
                    for c in range(nc):
                        for t in range(nt):
                            cc = self.plct2cc(p, l, c, t, dbg=1)
                            cn = self.cc2cn(cc)
                            self.log(f'{cn:3} {cc:4} {self.fntp()} {self.fplsct()}')
        self.log(hdrB)
        for i in range(len(self.tabls) * ns):
            self.cc2cn(  i, dbg=1)
        self.log(hdrC)
        for i in range(len(self.tabls)):
            self.cn2cc(  i, dbg=1)
        self.log(hdrB)
        for i in range(len(self.tabls)):
            self.cn2txt( i, dbg=1)
        self.log(hdrA)
        for i in range(len(self.tabls) * ns):
            self.cc2plct(i, dbg=1)
#        self.log(hdrB)
#        for i in range(len(self.tabls) * ns):
#            self.plc2cn_(p, l, c, dbg=1)
        self.dumpTniksSfx(f'END {j=} test')
    ####################################################################################################################################################################################################
    def lenA(self):                   return [ len(_) for _ in self.A ]
    def lenB(self):                   return [ len(_) for _ in self.B ]
    def lenC(self):                   return [ len(_) for _ in self.C ]
    def lenD(self):                   return [ len(_) for _ in self.D ]
    def lenE(self):                   return [ len(_) for _ in self.E ]
    ####################################################################################################################################################################################################
    def j(   self):                   return [ i-1 if i else 0 for    i in           self.i ]
    def j2(  self):                   return [ i-1 if i else 0 for j, i in enumerate(self.i)  if j != S ]
    def j2g( self, j):                return self.g[ self.gn[j] ]
    def resetJ(self, why=Z, dbg=1): self.J1 = [ 0 for _ in range(len(self.E)+1) ]  ;   self.J2 = [ 0 for _ in range(len(self.E)+1) ]  ;  self.nvis = 0  ;  self.dumpJs(why) if dbg else None
    def setJ(self, j, n, v=None):
        v = self.isV() if v is None else v    ;   self.J1[j] = n  ;  self.J2[j] += 1  ;  self.J1[-1] += 1  ;  self.J2[-1] += 1
        self.nvis += 1 if v else 0            ;   self.visib[j].append(v)
    def setJdump(self, j, n, v=None, why=Z): i = self.J2[j]  ;  self.setJ(j, n, v)  ;  self.dumpTnik(self.E[j][i], j, why)  ;  return j
    ####################################################################################################################################################################################################
    def ssl(self, dbg=0):  l = len(self.SS)   ;   self.log(f'{self.fmtn()} SS={fmtl(self.ss2sl())} {l=}') if dbg else None   ;   return l   # return 0-4
    def zzl(self, dbg=0):  l = len(self.ZZ)   ;   self.log(f'{self.fmtn()} ZZ={fmtl(self.zz2sl())} {l=}') if dbg else None   ;   return l   # return 0-2
    def ss2sl(self): return sorted(self.SS)
    def zz2sl(self): return sorted(self.ZZ)
    ####################################################################################################################################################################################################
    def fss2sl(self):    s2s = self.ss2sl()  ;  ss = W.join([str(s2s[i]) if i < len(s2s) else W for i in range(4)])  ;  return f'({ss:7})'
    def fzz2sl(self):    z2z = self.zz2sl()  ;  zz = W.join([str(z2z[i]) if i < len(z2z) else W for i in range(2)])  ;  return f'({zz:3})'
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
        return []
    ####################################################################################################################################################################################################
    def fplc(  self, p=None, l=None,         c=None):         j = self.j()  ;  p = j[P] if p is None else p  ;  l = j[L] if l is None else l  ;  c = j[C] if c is None else c  ;                                                                    return f'[{p+1} {l+1}   {c+1:2}]'
    def fplct( self, p=None, l=None,         c=None, t=None): j = self.j()  ;  p = j[P] if p is None else p  ;  l = j[L] if l is None else l  ;  c = j[C] if c is None else c  ;  t = j[T] if t is None else t  ;                                   return f'[{p+1} {l+1}   {c+1:2} {t+1}]'
    def fplsc( self, p=None, l=None, s=None, c=None):         j = self.j()  ;  p = j[P] if p is None else p  ;  l = j[L] if l is None else l  ;  s = j[S] if s is None else s  ;  c = j[C] if c is None else c  ;                                   return f'[{p+1} {l+1} {s+1} {c+1:2}]'
    def fplsct(self, p=None, l=None, s=None, c=None, t=None): j = self.j()  ;  p = j[P] if p is None else p  ;  l = j[L] if l is None else l  ;  s = j[S] if s is None else s  ;  c = j[C] if c is None else c  ;  t = j[T] if t is None else t  ;  return f'[{p+1} {l+1} {s+1} {c+1:2} {t+1}]'
    ####################################################################################################################################################################################################
    def jsum(  self, a=1):          return [ _ + a if self.J2[j] and j < len(self.J1)-1 else _ if j == len(self.J1)-1 else 0 for j, _ in enumerate(self.J1) ]
    def fmtdl( self, data=None):    return f'{fmtl(self.dl(data))}'
    def fmtdt( self, data=None):    return f"[{W.join([ t.replace('class ', Z) for t in self.dtA(data) ])}]"
    def fmtJ1( self, w=None, d=0):  w = w if w is not None else JFMT  ;  d = Z if not d else "["  ;  d2 =Z if not d else "]"  ;  return    f'{fmtl(self.jsum(), w=w, d=d, d2=Z)} {self.fnvis()}{d2}'
    def fmtJ2( self, w=None, d=0):  w = w if w is not None else JFMT  ;  d = Z if not d else "["  ;  d2 =Z if not d else "]"  ;  return    f'{fmtl(self.J2,     w=w, d=d, d2=Z)} {self.fnvis()}{d2}'
    def fmtLE( self, w=None, d=1):  w = w if w is not None else JFMT  ;  d = Z if not d else "["  ;  d2 =Z if not d else "]"  ;  return f'{d}{fmtl(self.lenE(), w=w, d=Z, d2=Z)} {sum(self.lenE()[:-1]):4} {self.fnvis()}{d2}'
    ####################################################################################################################################################################################################
    def fmtPos(self):                         cc = self.plct2cc(*self.j2())  ;  nc = self.normalizeCC(cc)  ;  cn = self.cc2cn(cc)  ;  return f'{fmtl(self.i, w=FIN)} {cc+1:3} {nc:3} {cn+1:2}]'
    def fmtn(  self, pfx='n=', n=None):       n = n if n is not None else self.n   ;   return f'{pfx}{fmtl(n)}'
    def fmti(  self, pfx='i='):               return f'{pfx}{fmtl(self.i)}'
    def fmtD(  self, data=None,      d='x'):  l = list(map(str, self.dl(data)))               ;   return f'({d.join(l):^10})'
    def fmtI(  self,                 d='x'):  l = list(map(str, self.i))   ;   del l[S:S+1]   ;   return f'({d.join(l):^10})'
    def fmtWH( self, w=None, h=None, d='x'):
        if w is None: w = self.width  if self.width  is not None else -1
        if h is None: h = self.height if self.height is not None else -1
        return f'({w if w is None else w:4}{d}{h if h is None else h:<4})'
    def fmtP0(self):                          return f'{self.p0x} {self.p0w} {self.p0sx} {self.p0y} {self.p0h} {self.p0sy}'
    def fmtWHP0(self):                        return f'{self.fmtWH()} {self.fmtP0()}'
    ####################################################################################################################################################################################################
    @staticmethod
    def fmtJText(j, why=Z):   jtxt = JTEXTS[j] if 0<=j<len(JTEXTS) else f'?{j:2}?'   ;   return f'{j=} {why} {jtxt}'
    ####################################################################################################################################################################################################
    @staticmethod
    def ffont(t):     return f'{t.dpi:3} {t.bold:1} {t.italic:1} {t.font_name:21}'
    ####################################################################################################################################################################################################
    @staticmethod
    def ftcolor(t):  k = W.join([ f'{k:3}' for k in t.color[:3] ])  ;  k += f' {t.opacity:3}'  ;  return f'[{k}]'
    @staticmethod
    def fFntSz(t):    return f'{t.font_size:4.0f}'
    @staticmethod
    def ftMxy(t):     return f'{t.scale:5.3f} {t.scale_x:5.3f} {t.scale_y:5.3f}'
    @staticmethod
    def ftvis(t):     return 'V' if t.visible else 'I'
    @staticmethod
    def ftxywh(t, s=W):         return Tabs.fxywh(t.x, t.y, t.width, t.height, s=s)
    ####################################################################################################################################################################################################
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
    def dumpAXY(self, dbg=1):                    d = '\n' if dbg else Z  ;  self.log(f'{self.fAxy(d=d, dbg=dbg)}{d}{self.fmtAxy(d=d, dbg=dbg)}{d}{self.fAxyf(dbg=dbg)}', p=0)
    def fmtAxy( self, d=W, dbg=0): (a,b) = ('ax=', 'ay=') if dbg else (Z, Z)  ;  return f'{a}{self.ax}{d}{b}{self.ay}'
    def fAxy(   self, d=W, dbg=0): (a,b) = ('ax=', 'ay=') if dbg else (Z, Z)  ;  return f'{a}{self.ftAx(self.ax)}{d}{b}{self.ftAy(self.ay)}'
    def fAxyf(self, dbg=0):        s = '\n' if dbg else Z  ;  return W.join([f'{self.A_LEFT}', f'{self.A_CENTER}', f'{self.A_RIGHT}{s}', f'{self.X_LEFT}', f'{self.X_CENTER}', f'{self.X_RIGHT}{s}', f'{self.Y_BOTTOM}', f'{self.Y_CENTER}', f'{self.Y_TOP}', f'{self.Y_BASELINE}{s}', f'{self.V_BOTTOM}', f'{self.V_CENTER}', f'{self.V_TOP}'])
    @staticmethod
    def ftAx(a):  return 'L' if a == LEFT   else 'C' if a == CENTER else 'R' if a == RIGHT else '???'
    @staticmethod
    def ftAy(a):  return 'B' if a == BOTTOM else 'C' if a == CENTER else 'T' if a == TOP   else 'N' if a == BASELINE else '???'
    @staticmethod
    def fcva(a):  return 'B' if a == BOTTOM else 'C' if a == CENTER else 'T' if a == TOP   else '???'
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
    def dumpJs(  self, why, w=None, d=1): b = W*12 if self.OIDS else Z  ;  self.log(f'{b}J1{self.fmtJ1(w, d)} {why}')   ;   self.log(f'{b}J2{self.fmtJ2(w, d)} {why}')   ;   self.log(f'{b}LE{self.fmtLE(w)} {why}')
    def dumpGeom(self, why=Z, why2=Z):    b = W*12 if self.OIDS else Z  ;  self.log(f'{b}{why:3}[{self.fmtWH()}{self.fmtD()}{self.fmtI()} {self.fss2sl()} {self.LL} {self.fzz2sl()} {len(self.idmap):4} {self.fnvis()}] {why2}')
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
        self.log(f'tpb tpp tpl tps tpc={fmtl(n)}')  if dbg else None
        return n
    def fntp(  self, dbg=0, dbg2=0):   return fmtl(self.ntp(dbg=dbg, dbg2=dbg2), w=FNTP)
    ####################################################################################################################################################################################################
    @staticmethod
    def accProd(n): return list(accumulate(n, operator.mul))
    ####################################################################################################################################################################################################
    def dumpStruct(self, why=Z, csv=0, dbg=0, dbg2=0):
        self.log(f'{self.fmtn()} BGN ntp={self.fntp(dbg=dbg, dbg2=dbg2)} {self.fmtI()}', pos=1)
        if dbg:      self.dumpArgs(f=2)
        util.dumpNic(self.nic)
        util.dumpData()
        self.dumpFont(why)
        self.dumpVisible()
        self.dumpIdmKeys() if dbg and self.VRBY else None
        self.dumpVisible2()
        if dbg2:     self.dumpTniksA(f'{why}A')
        if dbg2:     self.dumpTniksB(f'{why}B')
        if dbg2:     self.dumpTniksC(f'{why}C')
        if dbg2:     self.dumpTniksD(f'{why}D')
        if dbg2:      self.dumpTniksE()
        if dbg2:      self.dumpTniksF()
        if csv:      self.dumpTnikCsvs(f'CSVs {int(self.PIDX)}') #  ;   self.PIDX = not self.PIDX   ;   self.dumpTnikCsvs(f'CSVs {int(self.PIDX)}')
        if dbg2:     self.cobj.dumpMlimap('MLim') if self.VRBY else None
        self.log(f'{self.fmtn()} END ntp={self.fntp(dbg=dbg, dbg2=dbg2)} {self.fmtI()}', pos=1)
    ####################################################################################################################################################################################################
    def autoSave(self, dt, why, dbg=1):
        if dbg: self.log(f'Every {dt:=7.4f} seconds, {why} {self.rsyncData=}')
        if self.rsyncData: self.saveDataFile(why, self.dataPath0)   ;  self.rsyncData = 0
    ####################################################################################################################################################################################################
    def on_draw(self):
        pyglet.gl.glClearColor(0, 0, 0, 0) # (1, 1, 1, 1) # (R, G, B, A)
        self.clear()
        self.batch.draw()
        if self.SNAPS and self.snapReg:
            self.snapReg = 0       ;    path = self.snapshot()
            self.log(f'{self.snapWhy=} {self.snapType=} {self.snapId=}\n{path=}', pos=1)
#            if self.TEST:    self.testSprTxt(path) # path

    def on_resize(self, width, height, dbg=1):
        super().on_resize(width, height)
        if self.RESIZE: self.resizeTniks(dbg)

#    def on_close(self):
#        self.log('????', f=3)
    ####################################################################################################################################################################################################
    def saveDataFile(self, why, path, dbg=1):
        if dbg:   self.log(f'{why} {path}')
        with open(path, 'w', encoding='utf-8') as DATA_FILE:
            self.log(f'{DATA_FILE.name:40}', p=0)
            data = self.transposeData(dump=1 if dbg else 0) if self.isVert() else self.data
            self.log(f'{self.fmtn()} {self.fmtdl(data)}')
            for p, page in enumerate(data):
                if dbg: self.log(f'writing {p+1}{util.ordSfx(p+1)} page', p=0)
                for l, line in enumerate(page):
                    if dbg: self.log(f'writing {l+1}{util.ordSfx(l+1)} line', p=0)  # if dbg  else  self.log(p=0)  if  l  else  None
                    for r, row in enumerate(line):
                        text = []
                        for c, col in enumerate(row):
                            text.append(col)
#            for p in range(len(data)):
#                if dbg: self.log(f'writing {p+1}{util.ordSfx(p+1)} page', p=0)
#                for l in range(len(data[p])):
#                    if dbg: self.log(f'writing {l+1}{util.ordSfx(l+1)} line', p=0)  # if dbg  else  self.log(p=0)  if  l  else  None
#                    for r in range(len(data[p][l])):
#                        text = []
#                        for c in range(len(data[p][l][r])):
#                            text.append(data[p][l][r][c])
                        text = Z.join(text)
                        if dbg: self.log(f'writing {r+1}{util.ordSfx(r+1)} string {text}', p=0)  # if dbg  else  self.log(text, p=0)
                        DATA_FILE.write(f'{text}\n')
                    DATA_FILE.write('\n')  #   if l < nl:
        size = path.stat().st_size   ;   self.log(f'{self.fmtn()} {self.fmtdl()} {size=}')
        return size
    ####################################################################################################################################################################################################
    def genDataFile(self, path):
        self.log(f'{path} {self.fmtn()}')
        np, nl, ns, nc, nr = self.n  ;  nc += self.zzl()
        self.dumpBlanks()
        self.data = [ [ [ self.tblankRow for _ in range(nr) ] for _ in range(nl) ] for _ in range(np) ]
        size      = self.saveDataFile('Generated Data', path)
        self.log(f'{path} {size=} {len(self.data)=}')
        self.data = []
        return size
   ####################################################################################################################################################################################################
    def readDataFile(self, path, dbg=1):
        nl = self.n[L]      ;   nr = self.n[T]   ;   sp, sl, st, sr = 0, 0, 0, 0
        if dbg:                 self.log(f'BGN {self.fmtn()}')
        if not path.exists():   path = util.getFilePath(self.DAT_GFN, BASE_PATH, fdir=DATA, fsfx=Z)
        stat = path.stat()  ;   size = stat.st_size
        if size == 0:           self.log(f'WARN Zero Len Data File  {path} -> Generate Data File')   ;   size = self.genDataFile(path)
        if size == 0:            msg =  f'ERROR Zero Len Data File {size=}'    ;   self.log(msg)     ;   self.quit(msg)
        with open(path, 'r', encoding='utf-8') as DATA_FILE:
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
                    if rows  and not sr % nr:   lines.append(rows)    ;    rows = []   ;   sl += 1
                    if lines and not sl % nl:   data.append(lines)    ;   lines = []   ;   sp += 1
                self.log(tabs, p=0)
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
        nt    = self.n[C]  ;  nr = self.n[T]  ;  crlf = 2
        dsize = nlines * nr * nt              ;  self.log(f'{dsize=:3,} = {nlines=:3,} *     {nr=:2} *   {nt=}')
        crlfs = nlines * (nr + 1) * crlf      ;  self.log(f'{crlfs=:3,} = {nlines=:3,} * {(nr+1)=:2} * {crlf=}')
        size  =  dsize + crlfs                ;  self.log(f' {size=:3,} =  {dsize=:3,} +  {crlfs=:3,}   {ref=}')
        assert size == ref,     f'{size=:4,} == {ref=:4,}'

    def dumpDataFile(self, data=None):
        data = self.dproxy(data)
        d0, d1, d2, d3 = self.dl()
        self.log(f'BGN {d0} pages, {d1} lines per page, {d2} rows per line, {d3} tabs per line')
        for n0, dn0 in enumerate(data):
            for n1, dn1 in enumerate(dn0):
                self.log(f'{fmtl(dn1, d=Z)}', p=0)
#        for n0 in range(len(data)):
#            for n1 in range(len(data[n0])):
#                self.log(f'{fmtl(data[n0][n1], d=Z)}', p=0)
            self.log(p=0)
        self.log(f'END {d0} pages, {d1} lines per page, {d2} rows per line, {d3} tabs per line')
    ####################################################################################################################################################################################################
    def isVert(self, data=None, dbg=1):
        dl, dt = self.dl(data), self.dt(data)
        if dbg: self.log(f'BGN dl={self.fmtdl()} dt={self.fmtdt()}')
        assert dt[0] is list and dt[1] is list and dt[2] is list and dt[3] is str,   f'{dl=} {dt=}'
        vert   = 1 if dl[2] > dl[3] else 0
        self.checkData(vert=vert, data=None)
        self.log(fmtl(self.dplc()[0]), p=0)
        if dbg: self.log(f'END dl={self.fmtdl()} dt={self.fmtdt()} {vert=}')
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

    def transposeData(self, data=None, dump=0, dbg=1):
        data = self.dproxy(data)
        self.log(f'BGN {self.fmtD(data)} {dump=}')
        if dump > 1:    self.dumpDataVert(data) if self.isVert(data) else self.dumpDataHorz(data)
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
        if dump > 0:  self.dumpDataVert(tpose) if self.isVert(tpose) else self.dumpDataHorz(tpose)
        self.log(f'END {self.fmtD(tpose)} {dump=}')
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
        self.log(                  f'{a}{q}', p=0, e=Z)  ;  [  self.log(f'{c%10}',                      p=0, e=Z) for c in range(1, n+1) ]  ;  self.log(p=0)
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
    def flipTTs(self, how, tt):
        msg2 = f'{how} {tt=}'
        self.dumpGeom('BGN', f'     {msg2}')
        if   tt not in self.SS and not self.B[tt]: msg = 'ADD'    ;   self.addTTs( how, tt)
        elif tt     in self.SS:                    msg = 'HIDE'   ;   self.hideTTs(how, tt)
        else:                                      msg = 'SKIP'   ;   self.dumpGeom(W*3, f'{msg} {msg2}')   ;   self.flipTT(tt)
        self.on_resize(self.width, self.height)
        self.dumpGeom('END', f'{msg} {msg2}')

    def flipLLs(self, how, dbg=1):
        self.flipLL()
        msg2 = f'{how} {self.LL=}'
        self.dumpGeom('BGN', f'     {msg2}')
        if dbg: self.log(f'    llText={fmtl(self.llText[1-self.zzl():])}')
        if self.LL and not self.rowLs: msg = 'ADD'    ;   self.addLLs( how)
        else:                          msg = 'HIDE'   ;   self.hideLLs(how)
        self.on_resize(self.width, self.height)
        self.dumpGeom('END', f'{msg} {msg2}')

    def flipZZs(self, how, zz):
        ii   = 0 if not zz else 2
        msg2 = f'{how} {zz=}'
        self.dumpGeom('BGN', f'     {msg2}')
        if   zz not in self.ZZ and not self.D[ii]: msg = 'ADD'    ;   self.addZZs(how, zz)
        elif zz     in self.ZZ:                    msg = 'HIDE'   ;   self.hideZZs(how, zz)
        else:                                      msg = 'SKIP'   ;   self.dumpGeom(W*3, f'{msg} {msg2}')   ;   self.flipZZ(zz)
        self.on_resize(self.width, self.height)
        self.dumpGeom('END', f'{msg} {msg2}')
    ####################################################################################################################################################################################################
    def flipZZ(self, zz, why=Z):
        self.dumpGeom('BFR', why)
        self.ZZ.add(zz) if zz not in self.ZZ else self.ZZ.remove(zz)
        n = self.n[C] + self.zzl()
        self.dumpGeom('AFT', why)
        return n

    def flipTT(self, tt, why=Z):
        self.dumpGeom('BFR', why)
        self.SS.add(tt) if tt not in self.SS else self.SS.remove(tt)
        self.n[S] = self.ssl()
        self.dumpGeom('AFT', why)

    def flipLL(self, why=Z):
        self.dumpGeom('BFR', why)
        self.LL = int(not self.LL)
        self.dumpGeom('AFT', why)
    ####################################################################################################################################################################################################
    def hideTTs(self, how, ii, dbg=1):
        why = f'HIDE {how} {ii=}'  ;  why2 = 'Ref'
        np, nl, ns, nc, nt = self.n   ;   nc += self.zzl()
        self.dumpTniksPfx(why)
        for p in range(np):
            self.setJdump(P, p, why=why2) # p
            for l in range(nl):
                self.setJdump(L, l, why=why2) # l
                for _, s in   enumerate( self.ss2sl()):
                    if s != ii:          self.setJdump(S, s, why=why2)
                    else:                self.hideTnik(self.sects,   p*nl + l,            S, dbg=dbg)
                    for c in range(nc):
                        if s != ii:      self.setJdump(C, c, why=why2)
                        else:            self.hideTnik(self.colms,   (p*nl + l)*nc + c,   C, dbg=dbg)
                        for t in range(nt):
                            tlist, j, _, _  =  self.tnikInfo(p, l, s, c)
                            if s != ii:  self.setJdump(j, t, why=why2)
                            else:        self.hideTnik(tlist, ((p*nl + l)*nc + c)*nt + t, j, dbg=dbg)
        if ii == TT:                     self.hideTnik(self.hcurs,                     0, H, dbg=dbg)
        self.dumpTniksSfx(why)
        self.flipTT(ii)

    def hideLLs(self, how):
        msg = f'HIDE {how}'
        nr  = len(self.rowLs)                  ;  nc = len(self.qclms)
        assert not (nc % nr),  f'{nc=} {nr=}'  ;  nc = nc // nr  #  normalize
        self.dumpTniksPfx(msg)
        for r in range(nr):
            self.hideTnik(self.rowLs, r, R)
            for c in range(nc):
                self.hideTnik(self.qclms, c + r*nc, Q)
        self.dumpTniksSfx(msg)
    ####################################################################################################################################################################################################
    def NEW__addZZs(self, how, ii):
        why = f'ADD {how} {ii=}'      ;   why1, why2 = 'Ref1', 'Ref2'
        np, nl, ns, nc, nt = self.n   ;   zz = self.zz2sl() # call after flipZ???
        n = self.flipZZ(ii)
        self.dumpTniksPfx(why)
        for v, view in enumerate(self.views):
            self.dumpTnik(view, M, why=why1)
            self.splitH(view, n)
            self.dumpTnik(view, M, why=why2)
            for p in range(np):
                self.setJdump(P, p, why=why2) # p
                for l in range(nl):
                    self.setJdump(L, l, why=why2) # l
                    for s, s2 in enumerate(self.ss2sl()):
                        self.setJdump(S, s2, why=why2) # s2
                        for c in zz:
                            if c == ii:     self.addZZ(p, l, s, c, why)
                            else:           self.refZZ(p, l, s, c)
                        for c in range(nc): self.refZZ(p, l, s, c)
        self.dumpTniksSfx(why)
    def addZZs(self, how, ii, dbg=0):
        if dbg: self.log(f'{ii=} {how}')
        np, nl, ns, nc, nt = self.n
        for p in range(np):
            self.pages[p] = self.splitH(self.pages[p], self.n[C] + self.zzl() + 1)
            self.dumpTnik(self.pages[p], P, 'Ref')
        if self.RESIZE:   self.resizeTniks(dbg=1)
        self.flipZZ(ii)  # zz = self.zz2sl()   ;   nc += len(zz)
    def OLD__addZZs(self, how, ii, dbg=0):
        why = 'Add'   ;   self.log(f'{why} {ii=} {how}') if dbg else None # ;  why1 = f'{why} {how} {ii=}'  ;  why2 = 'Ref'
        np, nl, ns, nc, nt = self.n
        self.flipZZ(ii) #        zz = self.zz2sl()   ;   nc += len(zz)
#        self.dumpTniksPfx(why1)
        for p in range(np): #            self.setJdump(P, p, why=why2)
            self.pages[p] = self.splitH(self.pages[p], self.n[C] + self.zzl())
        if self.RESIZE:     self.resizeTniks(dbg=1)
#            if self.isV() and 0:
#                for l in range(nl): #                    self.setJdump(L, l, why=why2)
#                    self.g_resizeTniks(self.lines, L, None, why=why2, dbg=1)
#                    for s in range(self.ssl()): #                        self.setJdump(S, s, why=why2)
#                        s += l * ns
#                        self.createZZs(self.sects[s], s, why, dbg=1)
#                        for c in range(nc): self.refZZ(p, l, s, c)
#                        for c in self.zz2sl():
#                            if   c == ii:      self.addZZ(p, l, s, c, why)
#                            else:              self.refZZ(p, l, s, c)
#        self.dumpTniksSfx(why1)
    ####################################################################################################################################################################################################
    def addZZ(self, p, l, s, c, why):
        np, nl, ns, nc, nt = self.n   ;   z1 = self.z1(c)   ;   z2 = self.z2(c)
        for zc in self.g_createTniks(self.zclms, E, self.sects[s], ii=c, why=why):
            c2 = c + nc*(s + ns*(l + nl*p))
            self.log(f'j={C} {JTEXTS[C]:4} {c=} {c2=}  lc={len(self.zclms)} plsc ={self.fplsc(p, l, s, c)} J1={self.fmtJ1(0, 1)} J2={self.fmtJ2(0, 1)} {z1=} {z2=}', f=0)
            for t, _ in enumerate(self.g_createTniks(self.snums, T, zc, why=why)):
                tlist, j, kk, txt = self.tnikInfo(*self.J1plsct(), z=1)
                self.log(f'{t=} {j=} {JTEXTS[j]:4} {c=} {c2=} ltl={len(tlist)} plsct={self.fplsct(p, l, s, c, t)} J1={self.fmtJ1(0, 1)} J2={self.fmtJ2(0, 1)} {z1=} {z2=}', f=0)

    def refZZ(self, p, l, s, c, zz=None):
        np, nl, ns, nc, nt = self.n   ;   why = 'Ref'
        self.setJdump(C, c, why=why)
#            self.setJ(C, c3)
#            self.dumpTnik(self.colms[c3], C, why2)
        tlist, j, _, _ = self.tnikInfo(p, l, s, c, zz)
        self.log(f'{zz=} j={C} {JTEXTS[C]:4} {nc=}       ltl={len(tlist)} plsc =[{self.fplsc(p, l, s, c)} J1={self.fmtJ1(0, 1)} J2={self.fmtJ2(0, 1)} z1={self.z1(c)} z2={self.z2(c)}', f=0)
        for t in range(nt):
            t2 = t + nt*(c + nc*(s + ns*(l + nl*p))) if j <= K else t
#                self.setJdump(j2, t, why=why2)
            self.setJ(j, t2)
            self.dumpTnik(tlist[t2], j, why)
            self.log(f'{zz=} {j=} {JTEXTS[j]:4} {nc=} {t2=} ltl={len(tlist)} plsct={self.fplsct(p, l, s, c, t)} J1={self.fmtJ1(0, 1)} J2={self.fmtJ2(0, 1)}', f=0)
    ####################################################################################################################################################################################################
    def hideZZs(self, how, ii, dbg=1):
        why = f'HIDE {how} ii={ii}'   ;   why2 = 'Ref'  # ;  c2, t2 = 0, 0
        self.flipZZ(ii)
        np, nl, ns, nc, nt = self.n   ;    nc += self.zzl()   ;   ns = self.ssl()
        self.dumpTniksPfx(why)
        for p in range(np):
            self.setJdump(P, p, why=why2)
            for l in range(nl):
                self.setJdump(L, l, why=why2)
                for s, s2 in enumerate(self.ss2sl()):
                    self.setJdump(S, s2, why=why2)
                    for c in range(nc):
                        if c in self.ZZ:
                            tlist, j = self.OLD__tnikInfo(s2, c)   ;   z1 = self.z1()   ;   z2 = self.z2()
                            c2 = ((p * nl + l) * ns + s) * nc + c
                            self.log(f'  ii={ii} s={s} s2={s2} c={c} c2={c2} z1={z1} z2={z2} J1={self.fmtJ1()} J2={self.fmtJ2()}')
                            self.hideTnik(self.colms, c2, C, dbg=dbg)
                            for t in range(nt):
                                self.hideTnik(tlist, self.J1[j], j, dbg=dbg)
                        else:
                            tlist, j = self.OLD__tnikInfo(s2, c)   ;   z1 = self.z1()   ;   z2 = self.z2()
                            self.log(f'  ii={ii} s={s} s2={s2} c={c}     z1={z1} z2={z2} J1={self.fmtJ1()} J2={self.fmtJ2()}')
                            self.setJdump(C, c, why=why2) #  c
                            for t in range(nt):
#                                self.setJdump(j, t, why=why2)
                                self.setJ(j, t + c * nt)
                                self.dumpTnik(tlist[t + c * nt], j, why=why2)
        self.dumpTniksSfx(why)
    ####################################################################################################################################################################################################
    def addTTs(self, how, ii):
        why = f'ADD {how} {ii=}'  ;  why2 = 'Ref'
        self.flipTT(ii)
        np, nl, ns, nc, nt = self.n   ;   nc += self.zzl()
        self.dumpTniksPfx(why)
        for p in range(np):
            self.setJdump(P, p, why=why2)
            for l in range(nl):
                self.setJdump(L, l, why=why2)   ;   ss = self.ss2sl()
                for s, so in enumerate(ss):
                    if so == ii:
                        for sect in      self.g_createTniks(self.sects, S, self.lines[l], ii=s):
                            for colm in  self.g_createTniks(self.colms, C, sect):
                                for _ in self.g_createTniks(self.tabls, T, colm): #, v=1 if p == self.j()[P] else 0): # , ii=s):
                                    pass
                    else:
                        self.setJdump(S, s, why=why2)
                        for c in range(nc):
                            self.setJdump(C, c, why=why2)
                            for t in range(nt):
                                tlist, j, _, _ = self.tnikInfo(p, l, s, c, why=why2)
                                self.setJ(j, t)
                                self.dumpTnik(tlist[t], j, why=why2)
        self.dumpTniksSfx(why)
        if self.CURSOR and self.tabls and not self.cursor: self.createCursor(why)

    def addLLs(self, how):
        why = f'ADD {how}'  ;  why2 = 'Ref'
        np, nl = self.n[P], self.n[L]
        self.dumpTniksPfx(why)
        for p in range(np):
            self.setJdump(P, p, why=why2)
            if self.isV():
                for l in range(nl):
                    i = l + p*nl
                    self.setJdump(L, l, why=why2)
                    self.createLLs(self.lines[i], i, why)  ;  break
        self.dumpTniksSfx(why)
    ####################################################################################################################################################################################################
    def addPage(self, how, ins=None, dbg=1):
        np, nl, ns, nc, nt = self.n   ;   how = f'{how} {ins=}'
        self.dumpBlanks() # self.j()[P]
#        if ins is not None: self.flipPage(how)
        if ins is not None: self.flipVisible(how, self.j()[P])
        self.n[P] += 1   ;   kl = self.k[P]
        data      = [ [ self.tblankRow for _ in range(nt) ] for _ in range(nl) ]
        self.data = self.transposeData(dump=1 if dbg else 0)
        self.data.append(data) if ins is None else self.data.insert(ins, data)
        self.data = self.transposeData(dump=1 if dbg else 0)
        if ins is None: self.dumpTniksPfx(how, r=0)   ;   pi = len(self.pages)
        else:           self.dumpTniksPfx(how, r=1)   ;   pi = self.J1[P]
        self.J1[L], self.J1[S], self.J1[C], self.J1[T] = 0, 0, 0, 0
        n, ii, x, y, w, h =    self.geom(M, n=1, i=1, dbg=1)   ;   kk = self.cci(P, 0, kl)
        self.newC += 1  ;  why2 = f'New{self.newC}'  ;  why = why2
        page = self.createTnik(self.pages,   pi, P, x, y, w, h, kk, kl, why=why, v=0, dbg=1)
        for line in            self.g_createTniks(self.lines,  L, page, why=why):
            for sect in        self.g_createTniks(self.sects,  S, line, why=why):
                for colm in    self.g_createTniks(self.colms,  C, sect, why=why):
                    for _ in   self.g_createTniks(self.tabls,  T, colm, why=why): pass
        self.dumpTniksSfx(how)
        if self.SNAPS and dbg: self.regSnap(how, why2)
    ####################################################################################################################################################################################################
    def splitH( self, p, n, dbg=1):
        if   util.isi(p, LBL):
            p.x, p.width,   self.p0x, self.p0w = self.splitHL(p.x, p.width, n)
            if dbg:         self.log(f'{p.x=:.2f} {p.width=:.2f} {n=} {self.p0x=:.2f} {self.p0w=:.2f}')
        elif util.isi(p, SPR):
            p.x, p.scale_x, self.p0x, self.p0w = self.splitHS(p.x, p.width, n, p.image.width)
            if dbg:         self.log(f'{p.x=:.2f} {p.scale_x=:.4f} {n=} {self.p0x=:.2f} {self.p0w=:.2f} {self.p0sx=:.4f}')
        return p

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
        if util.isi(p, LBL): p.y, p.height, g     = self.splitV1(p.y, p.height, a)                  ;  self.log(f'{p.y=:6.2f} {p.height=:6.2f} {a=} {g=:6.2f}', f=0)  if dbg else None  ;   return p
        if util.isi(p, SPR): p.y, h, g, p.scale_y = self.splitV2(p.y, p.height, a, p.image.height)  ;  self.log(f'{p.y=:6.2f} {p.scale_y=:6.4f} {a=} {h=:6.2f}', f=0) if dbg else None  ;   return p
        self.log(f'ERROR {type(p)=} is not in (SPR, LBL) {p=} {a=}', f=0)  if dbg else None   ;   return None

    def splitV1(self, y, h, a, dbg=1):
        self.log(f'{y=:6.2f} {h=:6.2f} {a=}', e=W, f=0) if dbg else None
        c = h/a  ;  h -= c  ;  y -= c/2 ;  self.log(f'{y=:6.2f} {h=:6.2f} {a=} {c=:6.2f}', p=0, f=0) if dbg else None  ;  return y, h, c

    def splitV2(self, y, h, a, g, dbg=1):
        self.log(f'{y=:6.2f} {h=:6.2f} {a=} {g=:6.4f}', e=W, f=0) if dbg else None
        c = h/a  ;  h -= c  ;  g = h/g  ;  self.log(f'{y=:6.2f} {h=:6.2f} {a=} {c=:6.2f} {g=:6.4f}', p=0, f=0)  if dbg else None  ;  return y, h, c, g

#            if self.LL and self.isV() and not s:
#                n, _, x, y, w, h = self.geom2(C, self.rowLs[l], 1)
#                lrCol = self.createLL(None, l, c, x, y, w, h, why)
#                self.qclms.insert(c2, lrCol)
#                msg = f'WARN not tested'   ;   self.log(msg)   ;   self.quit(msg)
#    def sprite2LabelPos(self, x, y, w, h, dbg=0): x0 = x  ;  y0 = y  ;  x += w/2  ;  y -= h/2  ;  self.log(f'{x0=:6.2f} {y0=:6.2f}, {w/2=:6.2f} {-h/2=:6.2f}, {x=:6.2f} {y=:6.2f} {self.p0x=:6.2f} {self.p0y=:6.2f}', so=1) if dbg else None  ;  return x, y
####################################################################################################################################################################################################
    def isV(self, j=0, dbg=0):
        if   j <= K and self.J1[P] == self.j()[P]:   v = 1
        elif j in (H, Q):                            v = 1
        else:                                        v = 0
        if dbg:  why = f'{v=}'  ;  self.log(f'{self.fmtJText(j, why)} {self.J2[j]=} {self.i[j]=} {self.fmti()} {v=}', f=0)
        return v
    ####################################################################################################################################################################################################
    def z1(self, c=None):  return None if c is None else C1 if C1 in self.ZZ and c == C1 else C2 if C2 in self.ZZ and c == C1 else None
    def z2(self, c=None):  return None if c is None else C2 if C2 in self.ZZ and c == C2 else None
    @staticmethod
    def lens2n(ls):        return [ len(i) if util.isi(i, str) else i for i in ls ]
    ####################################################################################################################################################################################################
    def tnikInfo(self, p, l, s, c, t=None, z=0, why=Z, dbg=0):
        tlist, j, k, txt = None, -1, None, None   ;   z1, z2 = None, None
        if z: z1, z2 = self.z1(c), self.z2(c)
        exp1 = z1 == C1   ;  exp2 = C2 in (z1, z2)
        p, l, s, c, t = self.lens2n([p, l, s, c, t])
        msg1 = f'plsct={self.fplsct(p, l, s, c, t)} {z1=} {z2=} {exp1=} {exp2=} {txt=} {why}'
        msg2 = f'ERROR Invalid sect {s=}:'
        msg3 = f'ERROR Invalid tabl {t=}:'
        if t is None:
            if   s == TT:  tlist, j = (self.snums, B) if exp1 else (self.capos, D) if exp2 else (self.tabls, T)
            elif s == NN:  tlist, j = (self.snams, A) if exp1 else (self.capos, D) if exp2 else (self.notes, N)
            elif s == II:  tlist, j = (self.snums, B) if exp1 else (self.capos, D) if exp2 else (self.ikeys, I)
            elif s == KK:  tlist, j = (self.snams, A) if exp1 else (self.capos, D) if exp2 else (self.kords, K)
            else:   msg = f'{msg2} {msg1}'   ;    self.log(msg)   ;   self.quit(msg) # f'{self.fmtJText(j, why=why)}'
            if dbg: msg =        f'{msg1}'   ;    self.log(msg, f=0) # self.fmtJText(j, why=why)
            return  tlist, j, None, None
        if 0 <= t < self.n[T]:
            kT, kN, kI, kK = self.k[T], self.k[N], self.k[I], self.k[K]   ;   kO, kA, kD = self.k[B], self.k[A], self.k[D]
            tab = self.data[p][l][c][t]  # if C1 != z1 != C2 and C2 != z2 else Z
            if   s == TT:  tlist, j, k, txt = (self.snums, B, kO, self.sobj.stringNumbs[t]) if exp1 else (self.capos, D, kD, self.sobj.stringCapo[t]) if exp2 else (self.tabls, T, kT, tab)
            elif s == NN:  tlist, j, k, txt = (self.snams, A, kA, self.sobj.stringNames[t]) if exp1 else (self.capos, D, kD, self.sobj.stringCapo[t]) if exp2 else (self.notes, N, kN, tab)
            elif s == II:  tlist, j, k, txt = (self.snums, B, kO, self.sobj.stringNumbs[t]) if exp1 else (self.capos, D, kD, self.sobj.stringCapo[t]) if exp2 else (self.ikeys, I, kI, tab)
            elif s == KK:  tlist, j, k, txt = (self.snams, A, kA, self.sobj.stringNames[t]) if exp1 else (self.capos, D, kD, self.sobj.stringCapo[t]) if exp2 else (self.kords, K, kK, tab)
            else:   msg = f'{msg2} {msg1}'  ;   self.log(msg)   ;   self.quit(msg) # self.fmtJText(j, t, why)
            if dbg: msg =        f'{msg1}'  ;   self.log(msg, f=0) # self.fmtJText(j, t, why)
            return  tlist, j, k, txt
        msg = f'{msg3} {msg1}'   ;    self.log(msg)   ;   self.quit(msg) # self.fmtJText(j, t, why)
    ####################################################################################################################################################################################################
    def geom(self, j, p=None, n=None, i=None, dbg=1):
        assert 0 <= j <= len(JTEXTS),  f'{j=} {len(JTEXTS)=}'  ;  ww, hh = self.width, self.height
        n = n  if n is not None else self.n[j]   ;   c = (C, Q, E)  ;  s = (L, S, R, T)
        if n == 0:    n = 1    ;     self.log(f'ERROR n=0 setting {n=}')
        i               = i if i is not None else self.i[j]
        a, b            = self.axWgt(self.ax), self.ayWgt(self.ay)
        px, py, pw, ph  = (a*ww, b*hh, ww, hh) if p is None else (p.x, p.y, p.width, p.height)
        if   j in c:  w = pw/n             ;  h = ph
        elif j == P:  w = pw               ;  h = ph
        else:         w = pw               ;  h = ph/n
        if   j in s:  x = px - a*pw + a*w  ;  y = py + (1-b)*ph - (1-b)*h
        elif j in c:  x = a*w              ;  y = py + b*ph - b*h
        else:         x = px - a*pw + a*w  ;  y = py + b*ph - b*h
        if dbg and self.VRBY >= 2:
            msg  = f'{j=:2} {JTEXTS[j]:4} {n=:2} {self.fxywh(x, y, w, h)}'
            msg2 = f' : {self.ftxywh(p)}' if p else f' : {self.fxywh(0, 0, 0, 0)}'
            msg += msg2 if p else W * len(msg2)
            self.log(f'{msg} {self.fmtJ1(0, 1)} {self.fmtJ2(0, 1)}', p=0, f=0)
        return n, i, x, y, w, h
    ####################################################################################################################################################################################################
    def imap2ikey(self, tobj, imap, i, j, dbg=0):
        imap0 = imap[0][::-1] if imap and len(imap) else []
        ff = self.sobj.isFret(tobj)
        if imap0 and len(imap0) > i:  ikey = tobj if j > K else imap0[i] if ff else self.tblank   # ;   i += 1 if ff else 0
        else:                         ikey = tobj if j > K else self.tblank
        if dbg: self.log(f'{ikey=}')
        return ikey

    def imap2Chord(self, tobj, imap, i, j, dbg=1):
        chunks    = imap[4]  if (imap and len(imap) > 4) else []
        chordName = tobj     if j > K else chunks[i] if len(chunks) > i else self.tblank
        if dbg and chunks:   self.log(f'{chordName=} chunks={fmtl(chunks)} imap={fmtl(imap)}')
        return chordName
    ####################################################################################################################################################################################################
    def ntsl(self): n = 1 + self.n[T] * self.ssl() * self.i[L]   ;   return n
    ####################################################################################################################################################################################################
    def createZZs(self, p, s, why, dbg=1):
        n = self.n[C] + self.zzl()
        kz = self.k[E]   ;  kk = self.cci(E, s, kz) if self.CHECKERED else 0
        nz, iz, xz, yz, wz, hz = self.geom(E, p, n, s, dbg=dbg)
        zclm = self.createTnik(self.zclms, s, E, xz, yz, wz, hz, kk, kz, why, v=1, dbg=dbg)
        if s in (0, 2):
            nu, iu, xu, yu, wu, hu = self.geom(B, zclm, self.n[T], self.i[L], dbg=dbg)
            for u in range(nu):
                self.createZZ(s, u, xu, yu, wu, hu, why)
        if s in (1, 3):
            na, ia, xa, ya, wa, ha = self.geom(A, zclm, self.n[T], self.i[L], dbg=dbg)
            for a in range(na):
                self.createZZ(s, a, xa, ya, wa, ha, why)
        p = self.splitH(p, n, dbg)
        self.dumpTnik(p, S, why=why)
        return p

    def createZZ(self, s, i, x, y, w, h, why, dbg=1):
        self.log(f'ntp={self.fntp(1, 1)}')
        cc = i + s * self.ntp()[0]   ;   kk = NORMAL_STYLE
        p, l, c, t = self.cc2plct(cc)
        tlist, j, ki, txt = self.tnikInfo(p, l, s, c, t, z=1)
        tnik = self.createTnik(tlist, cc, j, x, y-i*h, w, h, kk, ki, why, t=txt, v=1, dbg=dbg)
        return tnik

    def resizeZZs(self, pt, why, dbg=1):
        n    = self.n[C] + self.zzl()
        nz, iz, xz, yz, wz, hz = self.geom(E, pt, n, self.i[S], dbg=dbg)
        zclm = self.resizeTnik(self.zclms, self.J2[E], E, xz, yz, wz, hz, why, dbg=dbg)
        nu, iu, xu, yu, wu, hu = self.geom(B, zclm, self.n[T], self.i[L], dbg=dbg)
        for u in range(nu):
            self.resizeTnik(self.snums, self.J2[B], B, xu, yu-u*hu, wu, hu, why, dbg=dbg)
        pt   = self.splitH(pt, n, dbg=dbg)
        return pt
    ####################################################################################################################################################################################################
    def createLLs(self, pt, pi, why, dbg=1, dbg2=1):
        n    = self.ntsl()   ;   kl = self.k[R]   ;   kk = self.cci(R, pi, kl) if self.CHECKERED else 0
        nr, ir, xr, yr, wr, hr = self.geom(R, pt, n, self.i[L], dbg=dbg2) #  ;   xr0 = xr
        txt = self.dbgTabTxt(R, pi)
        lrow = self.createTnik(self.rowLs, pi, R, xr, yr, wr, hr, kk, kl, why, t=txt, v=1, dbg=dbg)
        nc, ic, xc, yc, wc, hc = self.geom(Q, lrow, self.n[C], self.i[C], dbg=dbg2) #  ;   xc0 = xc
        for c in range(nc):
            self.createLL(self.qclms, pi, c, xc, yc, wc, hc, why)
        pt   = self.splitV(pt, n, dbg=dbg2)
        self.dumpTnik(pt, L, why=why)
        return pt

    def createLL(self, tlist, l, c, x, y, w, h, why, dbg=1):
        cc   = c + self.n[C] * l
        kl   = self.llcolor(cc, Q)
        zl   = self.zzl()  ;  kk = NORMAL_STYLE
        z    = 1 if self.FRT_BRD else 2
        text = self.llText[z-zl:]
        txt  = text[c]
        ll   = self.createTnik(tlist, cc, Q, x + c*w, y, w, h, kk, kl, why, t=txt, v=1, dbg=dbg)
        self.setLLStyle(cc, kk)
        return ll

    def resizeLLs(self, pt, why, dbg=1, dbg2=1):
        n    = self.ntsl()
        nr, ir, xr, yr, wr, hr = self.geom(R, pt, n, self.i[L], dbg=dbg2)  # ;    xr0 = xr
        lrow = self.resizeTnik(self.rowLs, self.J2[R], R, xr, yr, wr, hr, why, dbg=dbg)
        nc, ic, xc, yc, wc, hc = self.geom(Q, lrow, self.n[C], self.i[C], dbg=dbg2)  # ;    xc0 = xc
        for c in range(nc):
            self.resizeTnik(self.qclms, self.J2[Q], Q, xc + c*wc, yc, wc, hc, why, dbg=dbg)
        pt   = self.splitV(pt, n, dbg=dbg2)
        return pt
    ####################################################################################################################################################################################################
    def createTniks(self, dbg=1):
        self.newC += 1  ;  why2 = f'New{self.newC}'  ;  why = why2
        self.dumpTniksPfx(why)
        for page in              self.g_createTniks(self.pages, P, None, why=why): # pass
            for line in          self.g_createTniks(self.lines, L, page, why=why): # pass
                for sect in      self.g_createTniks(self.sects, S, line, why=why): # pass
                    for colm in  self.g_createTniks(self.colms, C, sect, why=why): # pass
                        for _ in self.g_createTniks(self.tabls, T, colm, why=why): pass
        self.dumpTniksSfx(why)
        if self.CURSOR and self.tabls and not self.cursor:  self.createCursor(why)   ;  self.dumpHdrs()
        if dbg:         self.dumpStruct(why2, csv=1)
    ####################################################################################################################################################################################################
    def g_createTniks(self, tlist, j, pt, ii=None, why=Z, dbg=1, dbg2=1): # {0x2588:c}{0x2591:c}{0x2592:c}{0x2593:c}
        n = 1 if ii is not None else None
        n, _, x, y, w, h = self.geom(j, pt, n, ii, dbg=dbg2)   ;   t = Z  ;  kl = self.k[j]  ;  tl2 = tlist   ;   p, l, c, _ = self.J1plct()
        n                = n if ii is None else 1              ;  x2 = x  ;  y2 = y  ;  j2 = j  ;  i3 = 0     ;   js = (P, L, S, C, R, Q)
        for i in range(n):
            if self.DBG_TABT and j in js:   t = self.dbgTabTxt(j, i)
            i2 = i if ii is None else ii
            if   j == P:                    v = 1 if i == self.j()[P] else 0   ;   self.log(f'j==P: {i=} {v=} {self.j()[P]=} {self.i[P]=}', f=0)
            else:                           v = int(self.pages[self.J1[P]].visible)
            if   j in (C, E):              x2 = x + i2 * w #  ;   j2 = len(self.J2) if ii is not None else j
            else:
                if   j != P:               y2 = y - i2 * h
                if   j == S:                _ = self.ss2sl()[i2] if self.ss2sl() else 0  ;  self.SS.add(_)
                elif j >= T:
                    s                         = self.ss2sl()[self.J1[S]]
                    tl2, j2, kl, to           = self.tnikInfo(p, l, s, c, i2, why=why)
                    if   s == TT:           t = to
                    elif s == NN:           t = to if j2 > K else self.sobj.tab2nn(to, i2, self.nic) if self.sobj.isFret(to) else self.tblank
                    elif s in (II, KK):
                        m = self.getImap(p, l, c)
                        if   s == II:       t = self.imap2ikey( to, m, i3, j2)  ;  i3 += 1 if t != self.tblank else 0
                        elif s == KK:       t = self.imap2Chord(to, m, i2, j2)
            kk = self.cci(j2, i2, kl) if self.CHECKERED else 0
            yield self.createTnik(tl2, i2, j2, x2, y2, w, h, kk, kl, why=why, t=t, v=v, dbg=dbg)

    def axyWgt(self, x, y, dbg=0): u, v = self.axWgt(x), self.ayWgt(y)  ;  self.log(f'{x=:6} {y=:6} {u=:4.2f} {v=:4.2f}') if dbg else None  ;  return u, v
    @staticmethod
    def axWgt(x): return 0.0 if x==LEFT   else 0.5 if x==CENTER else 1.0 if x==RIGHT else -1.0
    @staticmethod
    def ayWgt(y): return 0.0 if y==BOTTOM else 0.5 if y==CENTER else 1.0 if y==TOP   else -1.0

    def createSprite(self, tlist, i, j, x, y, w, h, kk, kl, why=Z, t=Z, v=0, g=None, dbg=0):
        path = util.getFilePath('_2_150', BASE_PATH, PNGS, PNG)
        self.setJ(j, i, v)   ;   k = kl[kk]
        if dbg:    self.log(f'{j=} {JTEXTS[j]} {i=} {t=} [{x} {y} {w} {h}] {g=} {kk=} {util.fmtl(kl)} {why}\n{path=}')
        img = pyglet.image.load(path)
        wx, wy = self.axyWgt(self.ax, self.ay)
        img.anchor_x, img.anchor_y = int(wx*w), int(wy*h)
        tnik = SPR(img, x=x, y=y, batch=self.batch, group=self.j2g(j), subpixel=self.SUBPIX)
        tnik.color, tnik.opacity = k[:3], k[3]
        tnik.anchor_x, tnik.anchor_y = wx*w, wy*h
        assert int(tnik.anchor_x)==img.anchor_x,  f'{int(tnik.anchor_x)=} != {img.anchor_x=}'
        assert int(tnik.anchor_y)==img.anchor_y,  f'{int(tnik.anchor_y)=} != {img.anchor_y=}'
        tnik.visible = v        ;  self.visib[j].append(v)
#        self.checkTnik(tnik, i, j)
        if    tlist is not None:   tlist.append(tnik)
        key = self.idmapkey(j)  ;  self.idmap[key] = (tnik, j, i)   ;   self.dumpTnik(tnik, j, why) if dbg else None
        return tnik
    ####################################################################################################################################################################################################
    def createTnik(self, tlist, i, j, x, y, w, h, kk, kl, why=Z, t=Z, v=0, g=None, dbg=0):
        if i is None or j is None: lt = len(tlist) if tlist is not None else None  ;  msg = f'ERROR i or j is None {i=} {j=} {lt=} {t=} {why}'  ;  self.log(msg)  ;  self.quit(msg)
        self.setJ(j, i, v)
        o, k2, d, ii, n, s = self.fontParams()   ;   b = self.batch   ;   k = kl[kk]
        g = g           if g is not None else self.j2g(j)
        if j == H or (self.SPRITES and (j < T or j == R)):
            scip = pyglet.image.SolidColorImagePattern(k)
            img  = scip.create_image(width=fri(w), height=fri(h))
            wx, wy = self.axyWgt(self.ax, self.ay)
            img.anchor_x, img.anchor_y = int(wx*w), int(wy*h)
            tnik = SPR(img, x, y, batch=b, group=g, subpixel=self.SUBPIX)
            tnik.color, tnik.opacity = k[:3], k[3]
            tnik.anchor_x, tnik.anchor_y = wx*w, wy*h
            assert int(tnik.anchor_x)==img.anchor_x,  f'{int(tnik.anchor_x)=} != {img.anchor_x=}'
            assert int(tnik.anchor_y)==img.anchor_y,  f'{int(tnik.anchor_y)=} != {img.anchor_y=}'
        else:
            s = self.calcFontSize(j)       ;   aa, ax, ay, va = self.aa, self.ax, self.ay, self.va  # left center right  # bottom baseline center top
            z = 1 if self.STRETCH else 0   ;        d, n = FONT_DPIS[d], FONT_NAMES[n]   ;   ml = self.MULTILINE
            tnik = LBL(t, font_name=n, font_size=s, bold=o, italic=ii, stretch=z, color=k, x=x, y=y, width=w, height=h, anchor_x=ax, anchor_y=ay, align=aa, multiline=ml, dpi=d, batch=b, group=g)
            tnik.content_valign = self.va
            if   T <= j <= K:      self._setTNIKStyle(tnik, self.k[j], NORMAL_STYLE)
            elif j == Q:           self._setTNIKStyle(tnik, self.k[j] if (i+1) % 10 else self.k[R], NORMAL_STYLE)
        tnik.visible = v        ;  self.visib[j].append(v)
        self.checkTnik(tnik, i, j)
        if    tlist is not None:   tlist.append(tnik)
        key = self.idmapkey(j)  ;  self.idmap[key] = (tnik, j, i)   ;   self.dumpTnik(tnik, j, why) if dbg else None
        if self.LL and j == L:
            if not self.rowLs or len(self.rowLs) < self.n[L]: tnik = self.createLLs(tnik, i, why)
            else:                                             tnik = self.splitV(tnik, self.ntsl(), dbg=dbg)
        if self.ZZ and j == P:                                tnik = self.splitH(tnik, self.n[C] + self.zzl())
        if self.ZZ and j == S and v:                          tnik = self.createZZs(tnik, i, why)
        return tnik
    ####################################################################################################################################################################################################
    def checkTnik(self, t, i, j, dbg=0):
        ntvH = 'Name  Tid V'  ;  ptxtH = W*8  ;  axy2H = self.axy2H()  ;  whvaH, adnH, dsH, ftxtH = Z, Z, Z, Z  ;  whva, adn, s = Z, Z, Z  ;  m, fnt = None, None
        if util.isi(t, LBL):  whvaH = f'{self.whvaH()}'  ;  dsH = f'{self.docStyleH()}'  ;  adnH = W.join(ADN)  ;  ptxtH, ftxtH = ' PrtlText', ' FullText'
        self.log(f'{ntvH}{ptxtH} {axy2H} {whvaH} {adnH} {dsH}{ftxtH}', p=0, f=0)  if j==P or (j==T and i==0) else None
        ptxt, ftxt = Z, Z  ;  js = JTEXTS[j]   ;   v = 'V' if t.visible else 'I'
        ax,   ay   =  self.ax, self.ay  ;   tax, tay =  t.anchor_x, t.anchor_y
        ancX, ancY = f'{int(t.width * self.axWgt(self.ax)):4}', f'{int(t.height * self.ayWgt(self.ay)):4}'
        if util.isi(t, LBL):
            d    = t.document  ;  m = d.styles  ;  wrap = 'char'  ;  aa = self.aa  ;  taa = m[ALIGN]  ;  ml = self.MULTILINE  ;  tml = int(t.multiline)
            assert tax == ax,  f'{tax=} != {ax=}'  ;  assert tay == ay,  f'{tay=} != {ay=}'  ;  assert taa == aa,  f'{taa=} != {aa=}'  ;  assert tml == ml,  f'{tml=} != {ml=}'
            d.set_paragraph_style(0, len(d.text), {LNSP:None, LEAD:0, WRAP:wrap, WRAP_LINES:True})
            fnt  = d.get_font()    ;   asc, dsc = fnt.ascent, fnt.descent   ;   net = asc - dsc   ;   ptxt, ftxt = f'{self.fpTxt(t)}', self.ffTxt(t)
            whva = self.fCtnt(t)   ;   adn = W.join([f'{asc:4}', f'{dsc:4}', f'{net:4}'])   ;   s = self.fDocStyle(m, W, t)
        self.log(f'{js} {i+1:4} {v} {ptxt}{self.fAxy()} {ancX} {ancY} {whva} {adn} {s} {ftxt}', p=0, f=0)
        if util.isi(t, LBL) and dbg and m and FONT_NAME in m:    fnt2 = pygfont.load(m[FONT_NAME], m[FONT_SIZE])    ;    assert fnt == fnt2,  f'{fnt=} != {fnt2=}'

    def dbgTabTxt(self, j, i):
        dt = self.DBG_TABT  ;  d = '\n' if j==C else Z  ;  k = f'{i+1:03}' if j==C else f'{i+1}'  ;  k = d.join(k)  ;  s, t = JTEXTS[j], JTEXTS2[j]  ;  l = len(t)
        if dt==1:  a = 4 if j==C else j+2   ;   b = f'{0x2588:c}'                        ;  return       d.join(b*a)
        if dt==2:  a = 3 if j==C else 4     ;   e = d.join([ s[_] for _ in range(a) ])   ;  return f'{e}{d}{i+1}'
        if dt==3:  a = 3 if j==C else j+1   ;   e = d.join([ t[_] for _ in range(a) ])   ;  return f'{e}{d}{k}'
        e = d.join([ t[_] for _ in range(l) ])
        e = f'{e}{d}{k}'
        e = e*4 if j==P else e
        return e
    @staticmethod
    def fDocStyle(m, d, t):
        lnsp = 'None' if m[LNSP] is None else f'{m[LNSP]:4}'   ;  clr = util.fColor(m[COLOR])  ;  bgc = util.fColor(m[BGC] if BGC in m else None)  ;  ml = int(t.multiline) if t else '?'
        return d.join([f'{m[FONT_SIZE]:4}', f'{m[LEAD]:4}', lnsp, clr,                 bgc,           f'{m[BOLD]}', f'{m[ITALIC]}', f'{m[STRH]}', f'{ml}', f'{int(m[WRAP_LINES])}', f'{m[WRAP][0]}', f'{m[FONT_NAME]:21}'])
    @staticmethod
    def docStyleH(d=W): return d.join(['FnSz', 'Lead', 'LnSp', ' ForegroundColor ', ' BackgroundColor ', 'B',          'I',            'S',         'M',          'W',                 'w',          'FontName             '])

    def hideTnik(self, tlist, i, j, dbg=0): # AssertionError: When the parameters 'multiline' and 'wrap_lines' are True,the parameter 'width' must be a number.
        c = tlist[i]      ;     ha = hasattr(c, 'text')
        if   util.isi(c, LBL):  c.x, c.y, c.width, c.height = 0, 0, 1, 0  # Zero width not allowed
        elif util.isi(c, SPR):  c.update(x=0, y=0, scale_x=0, scale_y=0)
        self.setJ(j, i)
        if dbg:         self.dumpTnik(c, j, 'Hide')
        if dbg > 1:     text = c.text if ha else Z  ;  self.log(f'{self.fmtJText(j)} {i=} {id(c):x} {text:6} {self.ftxywh(c)}  J1={self.fmtJ1(0, 1)} J2={self.fmtJ2(0, 1)}', p=0)
    ####################################################################################################################################################################################################
    def resizeTniks(self, dbg=1):
        self.updC += 1  ;  why = f'Upd{self.updC}'
        self.dumpTniksPfx(why)
        for page in              self.g_resizeTniks(self.pages, P, None, why=why): # pass
            for line in          self.g_resizeTniks(self.lines, L, page, why=why): # pass
                for sect in      self.g_resizeTniks(self.sects, S, line, why=why): # pass
                    for colm in  self.g_resizeTniks(self.colms, C, sect, why=why): # pass
                        for _ in self.g_resizeTniks(self.tabls, T, colm, why=why): pass
        self.dumpTniksSfx(why)
        if self.CURSOR and self.cursor: self.resizeCursor(why, self.cc)   ;   self.dumpHdrs()
        if dbg:   self.dumpStruct(why)
    ####################################################################################################################################################################################################
    def g_resizeTniks(self, tlist, j, pt=None, why=Z, dbg=1, dbg2=1):
        if not self.n[j]:     msg = f'ERROR {self.fmtJText(j, why)} SKIP {self.n[j]=}'   ;   self.log(msg) #  ;   self.quit(msg)
        n, _, x, y, w, h = self.geom(j, pt, dbg=dbg2)
        x2 = x  ;  y2 = y  ;  j2 = j  ;  tlist2 = tlist
        p, l, c, t = self.J1plct()    ;  lp, ll = self.dl()[0], self.dl()[1]
        for i in range(n):
            if   j in (C, E):   x2 = x + i * w
            else:
                if    j == P:   v = int(self.pages[self.J1[P]].visible)  ;  self.log(f'j==P: {i=} {v=} {self.j()[P]=} {self.i[P]=}', f=0)
                else:           y2 = y - i * h
                if    j == L and self.J2[L] >= lp * ll: msg = f'WARN MAX Line {self.J2[L]=} >= {lp=} * {ll=}'  ;   self.log(msg)  ;  self.quit(msg)
                elif  j >= T:
                    s = self.ss2sl()[self.J1[S] % self.ssl()]
                    tlist2, j2, _, _ = self.tnikInfo(p, l, s, c, why=why)
            yield self.resizeTnik(tlist2, self.J2[j2], j2, x2, y2, w, h, why=why, dbg=dbg)
    ####################################################################################################################################################################################################
    def resizeTnik(self, tlist, i, j, x, y, w, h, why=Z, dbg=1): # self._setTNIKStyle(tnik, self.k[j], self.BGC)
        if   not  tlist:        msg = f'ERROR tlist is Empty {      self.fmtJText(j, why)}'  ;  self.log(msg)  ;  self.quit(msg)
        elif i >= len(tlist):   msg = f'ERROR {i=} >={len(tlist)=} {self.fmtJText(j, why)}'  ;  self.log(msg)  ;  self.quit(msg)
        tnik    = tlist[i]   ;    v = tnik.visible
        self.log(f'{H=} {j=} {i=} {self.J2[H]=}') if dbg and j == H  else None
        self.setJ(j, i, v) if j != H or (j == H and self.J2[H] == 0) else None
        if   util.isi(tnik, SPR):
            mx, my = w/tnik.image.width, h/tnik.image.height
            tnik.update(x=x, y=y, scale_x=mx, scale_y=my)
        elif util.isi(tnik, LBL):
            tnik.font_size = self.calcFontSize(j)
            tnik.x, tnik.y, tnik.width, tnik.height = x, y, w, h
            self.checkTnik(tnik, i, j)
        if  self.LL and j == L:
            if v: tnik = self.resizeLLs(tnik, why)
            else: tnik = self.splitV(tnik, self.ntsl(), dbg=dbg)
        self.dumpTnik(tnik, j, why) if dbg else None
        return tnik
    ####################################################################################################################################################################################################
    def p2Js(self, p):
        np, nl, ns, nc, nt = self.n
        l, s, c, t = p*nl, p*nl, p*nl*nc, p*nl*nc*nt
        j1 = [p%np,l%nl,s%ns,c%nc,t%nt,t%nt,t%nt,t%nt,0,0,0,0,0,0,0,0,0]
        j2 = [p,   l,   s,   c,   t,   t,   t,   t,   0,0,0,0,0,0,0,0,0]
        self.log(f'{fmtl(j1)=} {fmtl(j2)=}')
        return j1, j2

    def flipVisible(self, why=None, p=None, dbg=0):
        why = 'TVis' if why is None else why   ;   np, nl, ns, nc, nt = self.n   ;   i = 0   ;   text = None
        pid = f' {id(self.pages[p]):11x}' if self.OIDS else Z   ;   page = self.pages[p]
        self.dumpTniksPfx(why)
        self.J1, self.J2 = self.p2Js(p % np)
        self.log(f'BGN {why} {p=} {pid} pages[{p}].v={int(self.pages[p].visible)} {self.fmti()} {self.fmtn()} {self.fVis()}')
        page.visible                                               = not page.visible   ;  self.setJdump(P, p, why=why)
        for l in range(nl):
            line = self.lines[self.J2[L]]          ;  line.visible = not line.visible   ;  self.setJdump(L, l, why=why)  ;  vl = []
            for s0, s in enumerate(self.ss2sl()):
                sect = self.sects[self.J2[S]]      ;  sect.visible = not sect.visible   ;  self.setJdump(S, s0, why=why)
                for c in range(nc):
                    colm = self.colms[self.J2[C]]  ;  colm.visible = not colm.visible   ;  self.setJdump(C, c, why=why)
                    for t in range(nt):
                        imap = self.getImap(p, l, c) if s >= II else []
                        tlist, j, kl, tobj = self.tnikInfo(p, l, s, c, t, why=why)
                        if   s == TT: text = tobj
                        elif s == NN: text = tobj if j > K else self.sobj.tab2nn(tobj, t, self.nic) if self.sobj.isFret(tobj) else self.tblank
                        elif s == II: text = self.imap2ikey( tobj, imap, i, j)     ;   i += 1 if text != self.tblank else 0
                        elif s == KK: text = self.imap2Chord(tobj, imap, t, j)
                        j2 = self.J2[j]  ;  tnik = tlist[j2]  ;  tnik.visible = not tnik.visible  ;  v = int(tnik.visible)
                        self.setJdump(j, t, why=why)   ;   oid = f' {id(tnik):11x}' if self.OIDS else Z
                        if dbg:       self.log(f'{v=} {j2=:3} {s0} plsct={self.fplsct(p, l, s, c, t)} {text=:4} {oid} {self.J2[j]}', f=0)
                        if dbg:       vl.append(f'{v}')
                if dbg:               vl.append(W)
            if dbg:                   self.log(f'{Z.join(vl)}', p=0)
        self.dumpTniksSfx(why)
        self.log(f'END {why} {p=} {pid} pages[{p}].v={int(self.pages[p].visible)} {self.fmti()} {self.fmtn()} {self.fVis()}')
    ####################################################################################################################################################################################################
    def dumpTniksPfx(self, why=Z, h=1, r=1):
        if r:        self.resetJ(why)   ;   self.clearVisib()
        self.dumpGeom('BGN', why)
        if not r:    self.dumpJs(why, w=None)  if self.J1 and self.J2 else self.quit(f'ERROR No Js {len(self.J1)=} {len(self.J2)=}')
        if h: self.dumpHdrs()

    def dumpTniksSfx(self, why=Z, h=1):
        if h: self.dumpHdrs()
        self.dumpJs(why, w=None)               if self.J1 and self.J2 else self.quit(f'ERROR No Js {len(self.J1)=} {len(self.J2)=}')
        self.dumpGeom('END', why)

    def dumpHdrs(self): hdr1 = self.fTnikHdr(0)   ;   hdr0 = self.fTnikHdr(1)   ;   self.log(hdr1, p=0)   ;   self.log(hdr0, p=0)
    ####################################################################################################################################################################################################
    def fTnikHdr(self, spr=0):
        tid = ' TId  Identity  ' if self.OIDS else ' Tid'  ;    wnc = ' Why  Name  Cnt'  ;  rot_txt = ' Rotated ' if spr else 'PrtlText '
        gv  = 'G V'     ;     jts = self.fjtxt()   ;   xywh = W.join(XYWH)           ;   whva = self.whvaH()   ;   axy2 = self.axy2H()
        cnc = ' CC  NC CN'   ;   rgb = ' Red Grn Blu Opc' if self.LONG_TXT else Z    ;   rgbM = (' M     Mx    My  ' if spr else rgb) if self.LONG_TXT else Z
        sfx = ('x y AncX AncY Grp             pGrp'     if spr     else     f' {axy2} {whva} {W.join(ADN)} FnSz dpi B I FontName')  if self.LONG_TXT else Z
        ft  = f'{W*13}FullText' if self.LONG_TXT and not spr and self.DBG_TABT else Z
        return f'{tid} {wnc} {rot_txt}{gv} {jts} {xywh} {cnc} {rgb} {rgbM} {sfx}{ft}'
    @staticmethod
    def axy2H(d=W):  return d.join(AXY2)
    @staticmethod
    def whvaH(d=W): return d.join(WHVA)
    @staticmethod
    def fjtxt():    return W.join(f'{jtxt[0]:>{JFMT[i]}}' for i, jtxt in enumerate(JTEXTS)) + ' Vis' # optimize str concat?
    def clearVisib(self):               consume(v.clear() for v in self.visib)

    def dumpTnik(self, t=None, j=None, why=Z):
        if   t is None: self.log(self.fTnikHdr(), p=0)      ;  return # hack
        if   j is None:                                        msg = f'{why} ERROR BAD j {j=}'             ;  self.log(msg)  ;  self.quit(msg)
        elif not util.isi(t, LBL) and not util.isi(t, SPR):    msg = f'{why} ERROR Bad t type {type(t)=}'  ;  self.log(msg)  ;  self.quit(msg)
        j1 = self.J1   ;   p, l, c, t2 = j1[P], j1[L], j1[C], j1[T]   ;   fc, bc, rot_txt, sfx = Z, Z, Z, Z
        foid = self.foid(t, j, why)   ;    gv = f'{self.gn[j]} {self.ftvis(t)}'   ;   fj2 = self.fmtJ2()   ;   xywh = self.ftxywh(t)
        cc = self.plct2cc(p, l, c, t2)   ;   cnc = f'{cc+1:3} {self.normalizeCC(cc):3} {self.cc2cn(cc)+1:2}' if j >= T else W*10
        if   util.isi(t, LBL):  rot_txt = self.fpTxt(t)  ;  fc = self.getDocColor(t, 0)  ;  bc = self.getDocColor(t, 1)   ;  sfx = f' {self.fLbl(t)}' if self.LONG_TXT else Z
        elif util.isi(t, SPR):  rot_txt = self.frot(t)   ;  fc = self.ftcolor(t)         ;  bc = self.ftMxy(t)            ;  sfx = f' {self.fSpr(t)}' if self.LONG_TXT else Z
        colors = f' {fc}{bc}' if self.LONG_TXT else Z
        self.log(f'{foid} {rot_txt}{gv} {fj2} {xywh} {cnc}{colors}{sfx}', p=0)

    def OLD__dumpTnik(self, t=None, j=None, why=Z):
        if   t is None: self.log(self.fTnikHdr(), p=0)      ;  return # hack
        if   j is None:                                        msg = f'{why} ERROR BAD j {j=}'             ;  self.log(msg)  ;  self.quit(msg)
        elif not util.isi(t, LBL) and not util.isi(t, SPR):    msg = f'{why} ERROR Bad t type {type(t)=}'  ;  self.log(msg)  ;  self.quit(msg)
        j1 = self.J1  ;  p, l, c, t2 = j1[P], j1[L], j1[C], j1[T]   ;   fc, bc, msg2, msg5 = Z, Z, Z, Z  ;  g = self.gn[j]
        xywh = self.ftxywh(t)   ;  cc = self.plct2cc(p, l, c, t2)   ;   cnc = f'{cc+1:3} {self.normalizeCC(cc):3} {self.cc2cn(cc)+1:2}' if j >= T else W*10
        if   util.isi(t, LBL): fc = self.getDocColor(t, 0)  ;  bc = self.getDocColor(t, 1)   ;  msg2 = self.fpTxt(t)  ;  msg5 = f' {self.fLbl(t)}' if self.LONG_TXT else Z
        elif util.isi(t, SPR): fc = self.ftcolor(t)         ;  bc = self.ftMxy(t)            ;  msg2 = self.frot(t)   ;  msg5 = f' {self.fSpr(t)}' if self.LONG_TXT else Z
        msg1 = self.foid(t, j, why)   ;   msg3 = self.ftvis(t)   ;   msg4 = f' {fc}{bc}' if self.LONG_TXT else Z
        self.log(f'{msg1} {msg2}{g} {msg3} {self.fmtJ2()} {xywh} {cnc}{msg4}{msg5}', p=0)
    ####################################################################################################################################################################################################
    def idmapkey(self, j):  return f'{JTEXTS[j]}{self.J2[j]}'
    def dumpIdmKeys(self):  self.log(fmtl(list(self.idmap.keys()), ll=1))
    def fSpr(self, t, d=W): return f'{self.fAxy()}{d}{self.fiax(t)}{d}{self.fiay(t)}{d}{self.fgrp(t)}{d}{self.fgrpp(t)}'
    def fLbl(self, t, d=W):
        dtxt = f'{d}{self.ffTxt(t)}' if self.DBG_TABT and len(t.text.replace('\n', Z)) > 8 else Z  ;  td = t.document
        ancX, ancY = f'{int(t.width * self.axWgt(self.ax)):4}', f'{int(t.height * self.ayWgt(self.ay)):4}'
        fnt  = td.get_font()    ;   asc  = fnt.ascent   ;   dsc = fnt.descent   ;   net = asc - dsc
        adn  =  d.join([f'{asc:4}', f'{dsc:4}', f'{net:4}'])
        return f'{self.fAxy()}{d}{ancX}{d}{ancY}{d}{self.fCtnt(t)}{d}{adn}{d}{self.fFntSz(t)}{d}{self.ffont(t)}{dtxt}'
    @staticmethod
    def frot(t):            return f'{t.rotation:8.3f} '
    def fnvis(self):        return f'{self.nvis:3}'
    @staticmethod
    def ffTxt(t):           return t.text.replace('\n', Z)
    @staticmethod
    def fpTxt(t): a = t.text.replace('\n', Z)  ;  b = a[:8]  ;  b += '+' if len(a) > 8 else W  ;  return f'{b:9}'
    def fCtnt(self, t, d=W):       return f'{t.content_width:4}{d}{t.content_height:4}{d}{self.fcva(t.content_valign)}{d}{self.ftAx(self.aa)}'
    def getDocColor(self, t, c=1): return util.fColor(self._getDocColor(t, c))
    @staticmethod
    def _getDocColor(t, c=1):      s = BGC if c else COLOR    ;  return t.document.get_style(s)
    def foid(self, t, j, why):  i, n = self.J2[-1], int(self.idmapkey(j)[4:])  ;  oid = f' {id(t):11x}' if self.OIDS else Z  ;  return f'{i:4}{oid} {why:5} {JTEXTS[j]} {n:4}'
    ####################################################################################################################################################################################################
    def dumpTniksA(self, why=Z):
        self.dumpTniksPfx(why)
        for v in self.idmap.values():
            self.setJdump(v[1], v[2], why=why)
        self.dumpTniksSfx(why)

    def dumpTniksB(self, why=Z):
        tpb, tpp, tpl, tps, tpc = self.ntp(dbg=1, dbg2=1)
        np, nl, ns, nc, nt = self.n
        self.dumpTniksPfx(why)
        for p in range(np):
            self.setJdump(P, p, why=why)
            for l in range(nl):
                self.setJdump(L, l, why=why)
                if self.LL and self.J2[P] == self.i[P]: # self.isV() self.E[R][l]:
                    self.setJdump(R, l, why=why)
                    for q in range(nc):  self.setJdump(Q, q, why=why)
                for s, s2 in enumerate(self.ss2sl()):
                    self.setJdump(S, s, why=why)
                    for c in range(nc):
                        self.setJdump(C, c, why=why)
                        for t in range(nt):
                            _, j, k, txt = self.tnikInfo(p, l, s2, c, t, why=why)
                            self.setJdump(j, t + c*tpc + l*tpl + p*tpp, why=why)
        self.setJdump(H, 0, why=why)
        self.dumpTniksSfx(why)
    ####################################################################################################################################################################################################
    def dumpTniksC(self, why=Z):
        self.dumpTniksPfx(why)
        consume(consume(self.setJdump(j, i % self.n[j], why=why) for i in range(len(self.E[j]))) for j in range(len(self.E)))
        self.dumpTniksSfx(why)

    def dumpTniksD(self, why=Z):
        ep, el, es, ec, et, en, ei, ek = self.lenE()[:K+1]   ;   np, nl, ns, nc, nt = self.n
        self.dumpTniksPfx(why)
        if self.LL and self.rowLs and self.qclms:
            for r in range(nl):    self.setJdump(R, r % self.n[L], v=int(self.rowLs[r].visible), why=why)
            for q in range(nl*nc): self.setJdump(Q, q % self.n[C], v=int(self.qclms[q].visible), why=why)
        for p in range(ep):        self.setJdump(P, p % self.n[P], v=int(self.pages[p].visible), why=why)
        for l in range(el):        self.setJdump(L, l % self.n[L], v=int(self.lines[l].visible), why=why)
        for s in range(es):        self.setJdump(S, s % self.n[S], v=int(self.sects[s].visible), why=why)
        for c in range(ec):        self.setJdump(C, c % self.n[C], v=int(self.colms[c].visible), why=why)
        for t in range(et):        self.setJdump(T, t % self.n[T], v=int(self.tabls[t].visible), why=why)
        for n in range(en):        self.setJdump(N, n % self.n[T], v=int(self.notes[n].visible), why=why)
        for i in range(ei):        self.setJdump(I, i % self.n[T], v=int(self.ikeys[i].visible), why=why)
        for k in range(ek):        self.setJdump(K, k % self.n[T], v=int(self.kords[k].visible), why=why)
        self.setJdump(H, 0, v=int(self.hcurs[0].visible), why=why)
        self.dumpTniksSfx(why)
    ####################################################################################################################################################################################################
    def dumpTniksE(self):
        self.log(Y.join(LTXX), p=0, f=3)
        for i, t in enumerate(self.pages):               d = t.document  ;  m = d.styles  ;  s = self.fDocStyle(m, Y, t)  ;  self.log(self.t2csv(t, P, i, Y, s), p=0, f=3)
        for i, t in enumerate(self.lines):               d = t.document  ;  m = d.styles  ;  s = self.fDocStyle(m, Y, t)  ;  self.log(self.t2csv(t, L, i, Y, s), p=0, f=3)
        for i, t in enumerate(self.sects):               d = t.document  ;  m = d.styles  ;  s = self.fDocStyle(m, Y, t)  ;  self.log(self.t2csv(t, S, i, Y, s), p=0, f=3)
        for i, t in enumerate(self.colms):               d = t.document  ;  m = d.styles  ;  s = self.fDocStyle(m, Y, t)  ;  self.log(self.t2csv(t, C, i, Y, s), p=0, f=3)
        for i, t in enumerate(self.tabls):               d = t.document  ;  m = d.styles  ;  s = self.fDocStyle(m, Y, t)  ;  self.log(self.t2csv(t, T, i, Y, s), p=0, f=3)

    def dumpTniksF(self):
        self.log(Y.join(LTXX), p=0, f=3)  ;  a = self.A  ;  b = self.B
        for i in range(len(self.pages)): t = a[0][i]  ;  d = t.document  ;  m = d.styles  ;  s = self.fDocStyle(m, Y, t)  ;  self.log(self.t2csv(t, P, i, Y, s), p=0, f=3)
        for i in range(len(self.lines)): t = a[1][i]  ;  d = t.document  ;  m = d.styles  ;  s = self.fDocStyle(m, Y, t)  ;  self.log(self.t2csv(t, L, i, Y, s), p=0, f=3)
        for i in range(len(self.sects)): t = a[2][i]  ;  d = t.document  ;  m = d.styles  ;  s = self.fDocStyle(m, Y, t)  ;  self.log(self.t2csv(t, S, i, Y, s), p=0, f=3)
        for i in range(len(self.colms)): t = a[3][i]  ;  d = t.document  ;  m = d.styles  ;  s = self.fDocStyle(m, Y, t)  ;  self.log(self.t2csv(t, C, i, Y, s), p=0, f=3)
        for i in range(len(self.tabls)): t = b[0][i]  ;  d = t.document  ;  m = d.styles  ;  s = self.fDocStyle(m, Y, t)  ;  self.log(self.t2csv(t, T, i, Y, s), p=0, f=3)
    ####################################################################################################################################################################################################
    @staticmethod
    def a2csv(a):        return fmtl(a, w=7, u="^", d=Z, s=Y)
    def args2csv(self):  return f'{W*4},  n ,{self.a2csv(self.n0)}', f'{W*4},  i ,{self.a2csv(self.i0)}', f'{W*4},  s ,{self.a2csv(self.ss2sl())}'
    def csvHdr(self, j, n):
        if   util.isi(self.E[j][0], LBL): return JLBL(n, Y)
        elif util.isi(self.E[j][0], SPR): return JSPR(n, Y)

    def t2csv(self, tnik, j, i, d=W, ds=Z): #, e=Y, dbg=0): # self.log(f'E[{j=}][{i=}]={self.E[j][i]} =? {tnik=}') if dbg else None
        assert tnik == self.E[j][i],  f'{tnik=} != {self.E[j][i]=}'
        self.tids.add(id(tnik))  ;   xywh = self.ftxywh(tnik, s=d)   ;   ii = f'{i+1:4}'  ;  w = tnik.width  ;  h = tnik.height
        axy = self.fAxy(d)       ;   ancX, ancY = f'{int(w*self.axWgt(self.ax)):4}', f'{int(h*self.ayWgt(self.ay)):4}'
        if   util.isi(tnik, LBL):
            td  = tnik.document  ;  fnt = td.get_font()     ;  asc, dsc = fnt.ascent, fnt.descent  ;  net = asc - dsc
            adn = d.join([f'{asc:4}', f'{dsc:4}', f'{net:4}'])  ;  ctnt = self.fCtnt(tnik, d)
            return d.join([JTEXTS[j], ii, xywh, axy, ancX, ancY, ctnt, adn, ds])
        elif util.isi(tnik, SPR):
            return d.join([JTEXTS[j], ii, xywh, axy, ancX, ancY])
    ####################################################################################################################################################################################################
    def dumpTnikCsvs(self, why):
        self.dumpTniksPfx(why)
        self.log(f'{fmtl(self.args2csv(), d=Z, s=Y)}', p=0, f=3)
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
        self.dumpTniksSfx(why)
    ####################################################################################################################################################################################################
    def dumpTnikCsv(self, t, j, i): # j in (P, C, T)
        if not i and j not in (L, S):   h = self.csvHdr(j, n=1)  ;  self.log(f'{h}', p=0, f=3)
#        if not i and j not in (L, S):   np, nl, ns, nc, nt = self.n  ;  n = np*nl*ns  ;  h = self.csvHdr(j, n)  ;  self.log(f'{h}', p=0, f=3)
        self.log(self.fmtTnikCsv(t, j, i), p=0, f=3)
    def fmtTnikCsv(self, t, j, i):
        s = {}
        if   util.isi(t, LBL):   d = t.document  ;  m = d.styles  ;  s = self.fDocStyle(m, Y, t)
#        elif util.isi(t, SPR):   z = Y.join([W * len(_) for _ in LTXX])
        return self.t2csv(t, j, i, Y, s)
    ####################################################################################################################################################################################################
    def createCursor(self, why, dbg=1):
        x, y, w, h, c = self.cc2xywh()
        kk = 0  ;  kl = self.k[H]
        if w == 0 or h == 0: msg = f'ERROR DIV by ZERO {w=} {h=}'   ;   self.log(msg)   ;   self.quit(msg)
        self.cursor   = self.createSprite(self.hcurs, 0, H, x, y, w, h, kk, kl, why, v=1, dbg=dbg)
#        self.cursor   = self.createTnik(self.hcurs, 0, H, x, y, w, h, kk, kl, why, v=1, dbg=dbg)
        if self.LL:     self.setLLStyle(self.cc, CURRENT_STYLE)

    def resizeCursor(self, why, why2, dbg=1):
        x, y, w, h, c = self.cc2xywh()
        self.resizeTnik(self.hcurs, 0, H, x, y, w, h, why, dbg=dbg)
        if dbg and self.SNAPS: self.regSnap(why, f'Upd{why2}')

    def moveCursor(self, ss=0, why=Z, dbg=1):
        if dbg:           self.log(f'BGN {ss=} {self.cc=}', pos=1)
        if self.LL:       self.setLLStyle(self.cc, SELECT_STYLE if ss else NORMAL_STYLE)
        self.resizeCursor(why, why2=self.cc, dbg=dbg)
        if self.LL:       self.setLLStyle(self.cc, CURRENT_STYLE)
        if dbg:           self.log(f'END {ss=} {self.cc=}', pos=1)
    ####################################################################################################################################################################################################
    def cc2xywh(self, dbg=1):
        tpb, tpp, tpl, tps, tpc = self.ntp()   ;   lenT = len(self.tabls)
        old   = self.cursorCol()  ;  cc = old % lenT
        self.log(f'{tpp=} {old=} {lenT=} {cc=} old % lenT', f=0)
        if cc < 0 or cc >= lenT:  msg = f'Invalid index {cc=} {tpp=} {old=} {lenT=}'  ;  self.log(msg)  ;  self.quit(msg)
#       assert 0 <= cc < lenT,          f'Invalid index {cc=} {lenT=}'
        else:
            t     = self.tabls[cc]
            if dbg: self.log(f'{cc=:4} {old=:4} {self.fntp()} {self.ftxywh(t)} {t.text=} {self.fCtnt(t)}', f=0) # i={Notes.index(self.sobj.tab2nn(t, cc % lenT))}
            w, h = t.width if t.width is not None else t.height , t.height
            return t.x, t.y, w, h, cc
    ####################################################################################################################################################################################################
    def plc2cn(self, p, l, c, dbg=1):
        tpb, tpp, tpl, tps, tpc = self.ntp()  ;  ns = self.n[S]
        cn = p*tpp//tpc + l*tpl//tpc//ns + c
#        cc = p*tpp + l*tpl//ns + c*tpc
        if dbg: self.log(f'{cn:4} {self.cn2cc(cn):4} {self.fntp()} plc={self.fplc(p, l, c)} ({p*tpp=:4} +{l*tpl=:3} +{c*tpc=:3})', f=0)
        return cn
#        return ( p *self.tpp//self.tpc) + (l *self.tpl//self.tpc) + c//self.tpc

    def plct2cc(self, p, l, c, t, dbg=0):
        tpb, tpp, tpl, tps, tpc = self.ntp()  ;  ns = self.n[S]
        if ns == 0: cc = p*tpp     + l*tpl     + c*tpc + t
        else:       cc = p*tpp//ns + l*tpl//ns + c*tpc + t
#       cc = p*tpp + l*tpl + s*tps + c*tpc + t
        if dbg: self.log(f'    {cc:4} {self.fntp()} {self.fplct(p, l, c, t)} ({p*tpp:4} +{l*tpl:3} +{tps:3} +{c*tpc:3} +{t})', f=0)
        return cc

    def cursorCol(  self,     dbg=1):   cc = self.plct2cc(*self.j2(), dbg=dbg)   ;  self.log( f'{cc=:3} {util.fmtl(self.j2())}', f=0) if dbg else None  ;  self.cc = cc  ;  return self.cc
    def normalizeCC(self, cc, dbg=0):  tpc = self.tpc  ;  old = cc  ;  cc = cc//tpc*tpc  ;  self.log(f'{old=:4} {cc=:4} {tpc=}', f=0) if dbg else None  ;  return cc
    def cc2cn(      self, cc, dbg=0):  tpc = self.tpc  ;  cn = cc//tpc  ;  self.log(f'{cn:3} {cc:4}//{tpc=} {cc//tpc=}', f=0) if dbg else None  ;  return  cn
    def cn2cc(      self, cn, dbg=0):  tpc = self.tpc  ;  cc = cn *tpc  ;  self.log(f'{cc:4} {cn:3} *{tpc=} {cn *tpc=}', f=0) if dbg else None  ;  return  cc
    def cn2txt(self, cn, dbg=0):  #  usefull? re-name f cn2tabtxt()
        cc         = self.cn2cc(cn)
        p, l, c, t = self.cc2plct(cc)
        txt        = self.data[p][l][c]
        self.log(f' {cn:3} {cc:4} {self.fntp()} {self.fplc(p, l, c)} txt={txt}') if dbg else None
    ####################################################################################################################################################################################################
    def cc2plct(self, cc, dbg=0): #todo
        tpb, tpp, tpl, tps, tpc = self.ntp()
        np, nl, ns, nc, nt = self.n
        t =    cc      % nt
        c =    cc//tpc % nc
#       s =    cc//tps % ns
        l = ns*cc//tpl % nl
        p = ns*cc//tpp % np
        if dbg: self.log(f'{cc:4} {self.fntp()} {self.fplct(p, l, c, t)}')
        return p, l, c, t
    ####################################################################################################################################################################################################
    def J1plct(self, p=None, l=None, c=None, t=None, dbg=0): #        return p2 % np, l2 % nl, c2 % nc, t2 % nt
        np, nl, ns, nc, nt = self.n   ;   n = 0 #  ;   b = 0
        if p is None:    p = self.J1[P]
        if l is None:    l = self.J1[L]
        if c is None:    c = self.J1[C]
        if t is None:    t = self.J1[T]
        t2 = n + t
        c2 = t2 // nt + c
        l2 = c2 // nc + l
        p2 = l2 // nl + p
#        b2 = p2 // np + b
#        rb = b2
        rp = p2 % np
        rl = l2 % nl
        rc = c2 % nc
        rt = t2 % nt
        if dbg: self.log(f'plct={self.fplct(p, l, c, t)} plct2={self.fplct(p2, l2, c2, t2)} rplct={rp, rl, rc, rt}')
        return rp, rl, rc, rt # todo
    def J1plsct(self, p=None, l=None, s=None, c=None, t=None, dbg=0):
        np, nl, ns, nc, nt = self.n   ;   n = 0
        if p is None:    p = self.J1[P]
        if l is None:    l = self.J1[L]
        if s is None:    s = self.J1[S]
        if c is None:    c = self.J1[C]
        if t is None:    t = self.J1[T]
        t2 = n + t
        c2 = t2 // nt + c
        s2 = c2 // nc + s
        l2 = s2 // ns + l
        p2 = s2 // nl + p
        rp = p2 % np
        rl = l2 % nl
        rs = s2 % ns
        rc = c2 % nc
        rt = t2 % nt
        if dbg: self.log(f'plsct={self.fplsct(p, l, s, c, t)} plsct2={self.fplsct(p2, l2, s2, c2, t2)} rplsct={rp, rl, rs, rc, rt}')
        return rp, rl, rs, rc, rt # todo
    ####################################################################################################################################################################################################
    def setCaption(self, msg, dbg=1):
        if dbg: self.log(msg)
        self.set_caption(msg)
    ####################################################################################################################################################################################################
    def calcFontSize(self, j=T, dbg=0):
        np, nl, ns, nc, nt = self.n   ;   h = self.height   ;   g = (L, S)
        pix  =  h if j==P else h/nl if j==L else h/(nl*ns) if j==S else h/(nl*ns*nt) # if j==C else h/nt
        fs   =  self.pix2fontsize(pix)
        if j in g:  fs *= 0.8
        if j == P:  fs *= 0.4
        if dbg: self.log(f'{j=} {JTEXTS[j]:4} {h=:6.2f} {pix=:6.2f} {fs=:6.2f}')
        return int(fs)

    def _initFonts(self):
        np, nl, ns, nc, nt = self.n            ;  nc += self.zzl()
        n  = nl * nt * ns if ns else nl * nt   ;   n += self.LL * nl
        w  = self.width / nc  ;  h = self.height / n
        fs = self.calcFontSize(j=T, dbg=1)
        self.fontBold, self.fontItalic, self.clrIdx, self.fontDpiIndex, self.fontNameIdx, self.fontSize = 0, 0, 0, 4, 0, fs
        self.log(f'{w=:6.3f}={self.width =}/({nc})                 {Z}{FONT_SCALE=:5.3f} fs=w*FONT_SCALE={fs:6.3f}pt', f=2)
        self.log(f'{h=:6.3f}={self.height=}/({nl=} * {ns=} * {nt=}){W}{FONT_SCALE=:5.3f} fs=h*FONT_SCALE={fs:6.3f}pt', f=2)
        self.dumpFont()

    def fmtFont(self, dbg=0):
        fb, fc, fd, fi, fn, fs = self.fontParams()
        text = f'{FONT_DPIS[fd]}dpi {fs:5.2f}pt {FONT_NAMES[fn]} {fc}'
        if dbg: self.log(text)
        return text

    def dumpFont(self, why=Z):
        b, k, dpi, i, n, s = self.fontParams()
        pix = s / FONT_SCALE   ;   fcs = Z # f'{fmtl( [k])}'
        self.log(f'{dpi}:{FONT_DPIS[dpi]}dpi {s:6.3f}pt {n}:{FONT_NAMES[n]} {k}:{fcs} {s:6.3f}pt = {FONT_SCALE:5.3f}(pt/pix) * {pix:6.3f}pixels {why}', f=2)

    def setFontParam(self, n, v, m, dbg=1): # if m == 'clrIdx': self.fontStyle = NORMAL_STYLE if self.fontStyle == SELECT_STYLE else SELECT_STYLE
        setattr(self, m, v)
        t = self.B  ;  lt = len(t)
        if dbg:                self.log( f'      {n:12}  {v:4}  {lt=}  {m}')
        for i in range(1):
            if dbg:            self.log(f'{i:4}  {n:12}  {v:4}  {lt=}  {m}') #  and self.VRBY
            self._setFontParam(self.B[i], n, v, m)
        self.setCaption(self.fmtFont())

    def _setFontParam(self, p, n, v, m, dbg=1):
        k = 3  ;  fb = 0 # if self.fontStyle == NORMAL_STYLE else 1
        for i, pi in enumerate(p):
            if   m == 'clrIdx':      k = len(pi.color)  ;  msg = f'{self.k[v][fb][:k]=}'
            elif m == 'fontNameIdx':                         msg = f'{FONT_NAMES[v]=}'
            else:                                            msg = f'{v=}'
            if dbg:
                j = 1 if self.VRBY else 10
                if not i % j:         self.log(f'{i=:4}  {n=:8}  {v=:2}  {m=:12}  {fb=}  {k=} {fmtl(pi.color, w=3)} {fmtl(p[i].document.get_style(n), w=3)} {msg}', p=0, f=2)
            if   m == 'clrIdx':       self._setTNIKStyle(p[i], self.k[v], self.fontStyle)
            elif m == 'fontNameIdx':  setattr(p[i], n, FONT_NAMES[v])
            else:                     setattr(p[i], n, v)
    @staticmethod
    def pix2fontsize(pix): return pix * FONT_SCALE # ( ) % FS_MAX
    def fontParams(self):  return self.fontBold, self.clrIdx, self.fontDpiIndex, self.fontItalic, self.fontNameIdx, self.fontSize
    ####################################################################################################################################################################################################
    def modDiv(self, n, j, dbg=1):
        if   j == P: tp = self.tpp//self.n[S]  ;  tp2 = len(self.tabls)//self.n[P]
        else:        tp = self.tpl//self.n[S]  ;  tp2 = len(self.tabls)//(self.n[P] * self.n[L])
        assert   tp == tp2,    f'{tp=} {tp2=}'
        if dbg:  self.log(f'{n=} {tp=} {tp2=} {n//tp=} {n%tp=}')
        return tp, n//tp, n % tp
    ####################################################################################################################################################################################################
    def setTab(self, how, text, rev=0, dbg=1): # if isDataFret or isTextFret else 0)
        if rev: self.reverseArrow()   ;    self.autoMove(how)
        old  = self.cursorCol()   ;   msg = Z
        p, l, c, t = self.j2()
        cc   = self.plct2cc(p, l, c, t)   ;   cc2 = cc
        self.log(f'BGN {how} {text=} {rev=} {old=:3} {cc=:3} {p=} {l=} {c=} {t=}', pos=1, f=2)
        data = self.data[p][l][c][t]
        if cc2 >= self.tpp:
            tp, dtp, mtp = self.modDiv(cc, P)   ;   cc2 = tp + mtp   ;   msg = f' {tp=:3} {dtp=} {mtp=} {cc2=:3}'
        if cc2 >= self.tpl:
            tp, dtp, mtp = self.modDiv(cc, L)   ;   cc2 = tp + mtp   ;   msg = f' {tp=:3} {dtp=} {mtp=} {cc2=:3}'
        self.log(f'    {how} {text=} {data=} {rev=} {old=:3} {cc=:3}{msg}', pos=1)
        self.setDTNIK(text, cc2, p, l, c, t, kk=1)
        p, l, c, t = self.j2()   ;   data = self.data[p][l][c][t]
        self.log(f'END {how} {text=} {data=} {rev=} {old=:3} {cc=:3}{msg}', pos=1)
        if rev: self.reverseArrow()
        else:   self.autoMove(how)
        if dbg and self.SNAPS:
            stype = f'TXT_{text}' if self.sobj.isFret(text) else 'SYMB' if text in util.DSymb.SYMBS else 'UNKN'
            self.regSnap(f'{how}', stype)
        self.rsyncData = 1

    def setDTNIK(self, text, cc, p, l, c, t, kk=0, pos=1, dbg=1):
        if dbg:  self.log(f'BGN {kk=}    {text=}', pos=pos)
        self.setData(text, p, l, c, t)
        imap   = self.getImap(p, l, c)
        if TT in self.SS: self.setTab2( text, cc)
        if NN in self.SS: self.setNote( text, cc, t)
        if II in self.SS: self.setIkey( imap, p, l, c)
        if KK in self.SS: self.setChord(imap, cc, pos=1, dbg=1) if kk else None
        if dbg:  self.log(f'END {kk=}    {text=} {len(imap)=}', pos=pos)
    ####################################################################################################################################################################################################
    def setData(self, text, p, l, c, t, pos=0, dbg=1):
        data =  self.data[p][l][c]
        if dbg: self.log(f'BGN {t=} {text=} {data=}', pos=pos)
        self.data[p][l][c] = data[0:t] + text + data[t+1:]
        data =  self.data[p][l][c]
        if dbg: self.log(f'END {t=} {text=} {data=}', pos=pos)

    def setTab2(self, text, cc, pos=0, dbg=0):
        if dbg: self.log(f'BGN         {text=} tabs[{cc}]={self.tabls[cc].text}', pos=pos)
        self.tabls[cc].text = text
        if dbg: self.log(f'END         {text=} tabs[{cc}]={self.tabls[cc].text}', pos=pos)

    def setNote(self, text, cc, t, pos=1, dbg=1): #fix me
        old   = self.notes[cc].text
        if dbg: self.log(f'BGN     {t=} {text=} notes[{cc}]={old}', pos=pos)
        if dbg: self.log(util.fmtKSK(self.ks[util.KSK]))
        ntext = self.sobj.tab2nn(text, t, self.nic) if self.sobj.isFret(text) else self.tblank
        if old in Notes.N2I:
            i  =  Notes.N2I[old]
            if  self.nic[i] <= 1:  del self.nic[i]
            else:                      self.nic[i] -= 1
            util.dumpNic(self.nic)
        self.notes[cc].text = ntext
        if dbg: self.log(f'END     {t=} {text=} notes[{cc}]={self.notes[cc].text}', pos=pos)
#                util.updNotes(11, 'B', 'Cb', Notes.TYPE, -1)
#                util.updNotes( 5, 'F', 'E#', Notes.TYPE, -1)
#                util.updNotes( 4, 'E', 'Fb', Notes.TYPE, -1)
#                util.updNotes( 0, 'C', 'B#', Notes.TYPE, -1)
    ####################################################################################################################################################################################################
    def getImap(self, p=None, l=None, c=None, dbg=0, dbg2=0):
        dl    = self.dl()
        cn    = self.plc2cn(p, l, c)          ;     key = cn   ;   mli = self.cobj.mlimap
        msg1  = f'plc={self.fplc(p, l, c)}'   ;    msg2 = f'dl={self.fmtdl()} {cn=} {key=} keys={fmtl(list(mli.keys()))}'
        if dbg:        self.log(f'{msg1} {msg2}', f=0)
        if p >= dl[0] or l >= dl[1] or c >= dl[2]:  msg = f'ERROR Indexing {msg1} >= {msg2}'  ;  self.log(msg)  ;  self.quit(msg)
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

    def setIkeyText(self, text, cc, p, l, c, pos=1, dbg=1, dbg2=0):
        nt  = self.n[T]  ;  cc = self.normalizeCC(cc)   ;   data = self.data[p][l][c]   ;   text = text[::-1]
        txt = self.objs2Text(self.ikeys, cc, nt, I)     ;   sobj = self.sobj  ;  blank = self.tblank  ;  j = 0
        if dbg:  self.log(f'BGN [{cc:2}-{cc+nt-1:2}] text={fmtl(text)} {data=} ikeys=<{txt}>{len(txt)}', pos=pos)
        for i in range(nt):
            if text and len(text) > j: ifd = sobj.isFret(data[i])  ;  self.ikeys[cc+i].text = text[j] if ifd else blank  ;  j += 1 if ifd else 0
            else:                                                     self.ikeys[cc+i].text = blank
        txt = self.objs2Text(self.ikeys, cc, nt, I)
        if dbg:  self.log(f'END [{cc:2}-{cc+nt-1:2}] text={fmtl(text)} {data=} ikeys=<{txt}>{len(txt)}', pos=pos)
        if dbg2: self.dumpDataSlice(p, l, c, cc)
    ###############################################################################################*#####################################################################################################
    def setChord(self, imap, cc, pos=1, dbg=0):
#        cc = self.plct2cc(p, l, c, 0)
        name = imap[3] if imap and len(imap) > 3 else Z  ;   chunks = imap[4] if imap and len(imap) > 4 else []
        if dbg: self.log(f'BGN {name=} chunks={fmtl(chunks)} {len(imap)=}', pos=pos)
        self.setChordName(cc, name, chunks) # if name and chunks else self.log(f'WARN Not A Chord {cc=} {name=} {chunks=}', pos=pos)
        if dbg: self.log(f'END {name=} chunks={fmtl(chunks)} {len(imap)=}', pos=pos)

    def setChordName(self, cc, name, chunks, pos=1, dbg=1):
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
        texts = [ obs[cc + t].text for t in range(nt) ]    ;   text = Z.join(texts)
        if dbg: slog(f'{jTEXTS[j]}[{cc}-{cc+nt-1}].text={fmtl(texts)}=<{text}>')
        return text
    ####################################################################################################################################################################################################
    def on_mouse_release(self, x, y, button, mods, dbg=1):
        np, nl, ns, nc, nt = self.n   ;   nz = self.zzl()    ;  nc += nz    ;   ll = self.LL   ;   ww = self.width   ;   hh = self.height
        y0 = y     ;   y = self.height - y   ;   m = ns * nt  + ll   ;      n = nl * m
        w = ww/nc  ;   h = hh/n              ;   d = int(y/h) - ll   ;   tlen = len(self.tabls)
        l = int(d/m)  ;  c = int(x/w) - nz   ;   t = d - (l * m)     ;      p = self.j()[P]
        text = self.tabls[self.cc].text if self.cc < tlen else Z
        if dbg: self.log(f'BGN {x=} {y=:4} {w=:6.2f} {h=:6.2f}', pos=1)
        if dbg: self.log(f'    {button=} {mods=} {self.cc=} {tlen=} {text=}', pos=1, f=2)
        if dbg: self.log(f'    {m=} {n=} {ll=} {nc=} {nz=} {d=}', pos=1)
        if dbg: self.log(f'    {p=}=i[P] {l=}=(d/m) {c=}=(x/w-nz) {t=}=(d-l*m)', pos=1)
        if dbg: self.log(f'    before plct={self.fplct(p, l, c, t)}', pos=1)
        self.moveTo('MOUSE RELEASE', p, l, c, t)
        if dbg: self.log(f'    after  plct={self.fplct(p, l, c, t)}', pos=1)
        if dbg: self.log(f'END {x=} {y0=:4} {ww=:6.2f} {hh=:6.2f}', pos=1)
    ####################################################################################################################################################################################################
    def kbkEvntTxt(self): return f'<{self.kbk=:8}> <{self.symb=:8}> <{self.symbStr=:16}> <{self.mods=:2}> <{self.modsStr=:16}>'
    ####################################################################################################################################################################################################
    def on_key_press(self, symb, mods, dbg=1): # avoid these
        self.symb, self.mods, self.symbStr, self.modsStr = symb, mods, pygwink.symbol_string(symb), pygwink.modifiers_string(mods)
        self.kbk = self.symbStr  ;  kbk = self.kbk
        if   dbg: self.log(f'BGN {self.kbkEvntTxt()}')
        if   kbk == 'A' and self.isCtrlShift(mods):    self.flipArrow(     '@^A', v=1)
        elif kbk == 'A' and self.isCtrl(     mods):    self.flipArrow(     '@ A', v=0)
        elif kbk == 'B' and self.isCtrlShift(mods):    self.flipBlank(     '@^B')
        elif kbk == 'B' and self.isCtrl(     mods):    self.flipBlank(     '@ B')
        elif kbk == 'C' and self.isCtrlShift(mods):    self.copyTabs(      '@^C')
        elif kbk == 'C' and self.isCtrl(     mods):    self.copyTabs(      '@ C')
        elif kbk == 'D' and self.isCtrlShift(mods):    self.deleteTabs(    '@^D')
        elif kbk == 'D' and self.isCtrl(     mods):    self.deleteTabs(    '@ D')
        elif kbk == 'E' and self.isCtrlShift(mods):    self.eraseTabs(     '@^E')
#       elif kbk == 'E' and self.isCtrl(     mods):    self.eraseTabs(     '@ E')
        elif kbk == 'F' and self.isCtrlShift(mods):    self.flipFullScreen('@^F')
        elif kbk == 'F' and self.isCtrl(     mods):    self.flipFlatSharp( '@ F') #  ;   KS.test()
        elif kbk == 'G' and self.isCtrlShift(mods):    self.move2LastTab(  '@^G', page=1)
        elif kbk == 'G' and self.isCtrl(     mods):    self.move2LastTab(  '@ G', page=0)
        elif kbk == 'H' and self.isCtrlShift(mods):    self.move2FirstTab( '@^H', page=1)
        elif kbk == 'H' and self.isCtrl(     mods):    self.move2FirstTab( '@ H', page=0)
        elif kbk == 'I' and self.isCtrlShift(mods):    self.insertSpace(   '@^I')
        elif kbk == 'I' and self.isCtrl(     mods):    self.flipTTs(       '@ I', II)
        elif kbk == 'J' and self.isCtrlShift(mods):    self.jump(          '@^J', a=1)
        elif kbk == 'J' and self.isCtrl(     mods):    self.jump(          '@ J', a=0)
        elif kbk == 'K' and self.isCtrlShift(mods):    self.flipTTs(       '@^K', KK)
        elif kbk == 'K' and self.isCtrl(     mods):    self.flipTTs(       '@ K', KK)
        elif kbk == 'L' and self.isCtrlShift(mods):    self.flipLLs(       '@^L')
        elif kbk == 'L' and self.isCtrl(     mods):    self.flipLLs(       '@ L')
        elif kbk == 'M' and self.isCtrlShift(mods):    self.flipZZs(       '@^M', 1)
        elif kbk == 'M' and self.isCtrl(     mods):    self.flipZZs(       '@ M', 0)
        elif kbk == 'N' and self.isCtrlShift(mods):    self.flipTTs(       '@^N', NN)
        elif kbk == 'N' and self.isCtrl(     mods):    self.flipTTs(       '@ N', NN)
        elif kbk == 'O' and self.isCtrlShift(mods):    self.flipCursorMode('@^O', -1)
        elif kbk == 'O' and self.isCtrl(     mods):    self.flipCursorMode('@ O', 1)
        elif kbk == 'P' and self.isCtrlShift(mods):    self.addPage(       '@^P', ins=0)
        elif kbk == 'P' and self.isCtrl(     mods):    self.addPage(       '@ P', ins=None)
        elif kbk == 'Q' and self.isCtrlShift(mods):    self.quit(          '@^Q', error=0, save=0)
        elif kbk == 'Q' and self.isCtrl(     mods):    self.quit(          '@ Q', error=0, save=1)
        elif kbk == 'R' and self.isCtrlShift(mods):    self.flipChordNames('@^R', hit=1)
        elif kbk == 'R' and self.isCtrl(     mods):    self.flipChordNames('@ R', hit=0)
        elif kbk == 'S' and self.isCtrlShift(mods):    self.shiftTabs(     '@^S')
#       elif kbk == 'S' and self.isCtrl(     mods):    self.saveDataFile(  '@ S', self.dataPath1)
        elif kbk == 'S' and self.isCtrl(     mods):    self.swapTab(       '@ S', txt=Z)
        elif kbk == 'T' and self.isCtrlShift(mods):    self.flipTTs(       '@^T', TT)
        elif kbk == 'T' and self.isCtrl(     mods):    self.flipTTs(       '@ T', TT)
        elif kbk == 'U' and self.isCtrlShift(mods):    self.reset(         '@^U')
        elif kbk == 'U' and self.isCtrl(     mods):    self.reset(         '@ U')
#       elif kbk == 'V' and self.isCtrlAlt(  mods):    self.pasteTabs(     '@&V', hc=0, kk=1)
        elif kbk == 'V' and self.isCtrlShift(mods):    self.pasteTabs(     '@^V', kk=1)
        elif kbk == 'V' and self.isCtrl(     mods):    self.pasteTabs(     '@ V', kk=0)
        elif kbk == 'W' and self.isCtrlShift(mods):    self.swapCols(      '@^W')
        elif kbk == 'W' and self.isCtrl(     mods):    self.swapCols(      '@ W')
        elif kbk == 'X' and self.isCtrlShift(mods):    self.cutTabs(       '@^X')
        elif kbk == 'X' and self.isCtrl(     mods):    self.cutTabs(       '@ X')
    ####################################################################################################################################################################################################
        elif kbk == 'ESCAPE':                          self.flipSelectAll( 'ESCAPE')
        elif kbk == 'TAB'       and self.isCtrl(mods): self.setCHVMode(    '@ TAB',       MELODY, LARROW)
        elif kbk == 'TAB':                             self.setCHVMode(    '  TAB',       MELODY, RARROW)
#       elif kbk == 'SLASH'     and self.isCtrl(mods): self.setTab(        '@ SLASH', '/')
#       elif kbk == 'SLASH':                           self.setTab(        '  SLASH', '/')
#       elif kbk == 'BACKSLASH' and self.isCtrl(mods): self.setTab(        '@ BACKSLASH', '\\')
#       elif kbk == 'BACKSLASH':                       self.setTab(        '  BACKSLASH', '\\')
#       elif kbk == 'SLASH'     and self.isCtrl(mods): self.setCHVMode(    '@ SLASH',     ARPG,   LARROW,  DARROW)
#       elif kbk == 'SLASH':                           self.setCHVMode(    '  SLASH',     ARPG,   RARROW, UARROW)
#       elif kbk == 'BACKSLASH' and self.isCtrl(mods): self.setCHVMode(    '@ BACKSLASH', ARPG,   LARROW,  UARROW)
#       elif kbk == 'BACKSLASH':                       self.setCHVMode(    '  BACKSLASH', ARPG,   RARROW, DARROW)
    ####################################################################################################################################################################################################
        elif kbk == 'D' and self.isAltShift(mods):     self.flipBGC(     '&^D')
        elif kbk == 'D' and self.isAlt(     mods):     self.flipBGC(     '& D')
        elif kbk == 'N' and self.isAltShift(mods):     self.setn_cmd(    '&^N', txt=Z)
        elif kbk == 'N' and self.isAlt(     mods):     self.setn_cmd(    '& N', txt=Z)
        elif kbk == 'P' and self.isAltShift(mods):     self.flipPage(    '&^P', 1)
        elif kbk == 'P' and self.isAlt(     mods):     self.flipPage(    '& P', -1)
        elif kbk == 'R' and self.isAltShift(mods):     self.rotateSprite('&^R', self.hcurs[0], -1)
        elif kbk == 'R' and self.isAlt(     mods):     self.rotateSprite('& R', self.hcurs[0],  1)
        elif kbk == 'Z' and self.isAltShift(mods):     self.RESIZE = not self.RESIZE  ;  self.resizeTniks(dbg=1) # if self.RESIZE else None
        elif kbk == 'Z' and self.isAlt(     mods):                                       self.resizeTniks(dbg=1) # if self.RESIZE else None
####################################################################################################################################################################################################
        elif kbk == 'B' and self.isAltShift(mods):     self.setFontParam(BOLD,      not self.fontBold,                           'fontBold')
        elif kbk == 'B' and self.isAlt(     mods):     self.setFontParam(BOLD,      not self.fontBold,                           'fontBold')
        elif kbk == 'C' and self.isAltShift(mods):     self.setFontParam(COLOR,        (self.clrIdx + 1) % len(self.k),          'clrIdx')
        elif kbk == 'C' and self.isAlt(     mods):     self.setFontParam(COLOR,        (self.clrIdx - 1) % len(self.k),          'clrIdx')
        elif kbk == 'I' and self.isAltShift(mods):     self.setFontParam(ITALIC,    not self.fontItalic,                         'fontItalic')
        elif kbk == 'I' and self.isAlt(     mods):     self.setFontParam(ITALIC,    not self.fontItalic,                         'fontItalic')
        elif kbk == 'A' and self.isAltShift(mods):     self.setFontParam(FONT_NAME,    (self.fontNameIdx + 1) % len(FONT_NAMES), 'fontNameIdx')
        elif kbk == 'A' and self.isAlt(     mods):     self.setFontParam(FONT_NAME,    (self.fontNameIdx - 1) % len(FONT_NAMES), 'fontNameIdx')
        elif kbk == 'S' and self.isAltShift(mods):     self.setFontParam(FONT_SIZE,     self.fontSize    + 1,                    'fontSize') # )  % FS_MAX
        elif kbk == 'S' and self.isAlt(     mods):     self.setFontParam(FONT_SIZE, max(self.fontSize    - 1, 1),                'fontSize') # )  % FS_MAX
        else:   self.log(f'Unexpected {self.kbkEvntTxt()}', f=2)
    ####################################################################################################################################################################################################
        if not self.isParsing():
            if   kbk == 'ENTER' and self.isCtrl(mods): self.setCHVMode(  '@  ENTER',     CHORD,       v=DARROW)
            elif kbk == 'ENTER':                       self.setCHVMode(  '   ENTER',     CHORD,       v=UARROW)
            elif kbk == 'SPACE':                       self.autoMove(    '   SPACE')
#            elif dbg: self.log(f'Unexpected {self.kbkEvntTxt()} while parsing', f=2)
        if   dbg: self.log(       f'END {self.kbkEvntTxt()}')
    ####################################################################################################################################################################################################
    def on_key_release(self, symb, mods, dbg=1):
        self.symb, self.mods, self.symbStr, self.modsStr = symb, mods, pygwink.symbol_string(symb), pygwink.modifiers_string(mods)
        self.kbk = self.symbStr
        if dbg:    self.log(self.kbkEvntTxt())
    ####################################################################################################################################################################################################
    def on_text(self, text, dbg=1): # use for entering strings not for motion
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
        if   self.isNumLock(     self.mods):                 msg =             f'NUMLOCK(         {motion})'   ;   self.log(msg)   ;   pygwink.MOD_NUMLOCK = 0
        if   self.isCtrlAltShift(self.mods):                 msg =             f'@&^(             {motion})'   ;   self.log(msg) #  ;   self.quit(msg)
        elif self.isCtrlAlt(     self.mods):
            if   motion == 1:                                self.unselectTabs(f'@& LEFT (        {motion})',  nt)
            elif motion == 2:                                self.unselectTabs(f'@& RIGHT (       {motion})', -nt)
            else:                                            msg =             f'@& (             {motion})'   ;   self.log(msg) #  ;   self.quit(msg)
        elif self.isAltShift( self.mods):                    msg =             f' &^(             {motion})'   ;   self.log(msg) #  ;   self.quit(msg)
        elif self.isCtrlShift(self.mods):                    msg =             f'@^(              {motion})'   ;   self.log(msg) #  ;   self.quit(msg)
        elif self.isShift(    self.mods):                    msg =             f'^ (              {motion})'   ;   self.log(msg) #  ;   self.quit(msg)
        elif self.isAlt(      self.mods):
            if   motion == pygwink.MOTION_UP:                self.moveUp(      f' & UP (          {motion})')
            elif motion == pygwink.MOTION_DOWN:              self.moveDown(    f' & DOWN (        {motion})')
            elif motion == pygwink.MOTION_LEFT:              self.moveLeft(    f' & LEFT (        {motion})')
            elif motion == pygwink.MOTION_RIGHT:             self.moveRight(   f' & RIGHT (       {motion})')
            elif motion == pygwink.MOTION_BEGINNING_OF_LINE: self.move(        f' & HOME (        {motion})', -nt *  c)
            elif motion == pygwink.MOTION_END_OF_LINE:       self.move(        f' & END (         {motion})',  nt * (nc - self.i[C]))
            elif motion == pygwink.MOTION_PREVIOUS_PAGE:     self.prevPage(    f' & PAGE UP (     {motion})')
            elif motion == pygwink.MOTION_NEXT_PAGE:         self.nextPage(    f' & PAGE DOWN (   {motion})')
            else:                                            msg =             f' & (             {motion})'   ;   self.log(msg)   ;   self.quit(msg)
        elif self.isCtrl(self.mods):
            if   motion == pygwink.MOTION_PREVIOUS_WORD:     self.selectTabs(  f'@  LEFT (        {motion})', -nt)
            elif motion == pygwink.MOTION_NEXT_WORD:         self.selectTabs(  f'@  RIGHT (       {motion})',  nt)
            elif motion == pygwink.MOTION_BEGINNING_OF_LINE: msg = f'@  MOTION_BEGINNING_OF_LINE( {motion})'   ;   self.log(msg)   ;   self.quit(msg) # N/A
            elif motion == pygwink.MOTION_END_OF_LINE:       msg = f'@  MOTION_END_OF_LINE (      {motion})'   ;   self.log(msg)   ;   self.quit(msg) # N/A
            elif motion == pygwink.MOTION_BEGINNING_OF_FILE: msg = f'@  MOTION_BEGINNING_OF_FILE( {motion})'   ;   self.log(msg)   ;   self.quit(msg) # CTRL HOME
            elif motion == pygwink.MOTION_END_OF_FILE:       msg = f'@  MOTION_END_OF_FILE (      {motion})'   ;   self.log(msg)   ;   self.quit(msg) # CTRL END
            else:                                            msg =             f'CTRL (           {motion})'   ;   self.log(msg)   ;   self.quit(msg)
        elif self.mods == 0:
            if   motion == pygwink.MOTION_UP:                self.move(        f' UP (            {motion})', -1)
            elif motion == pygwink.MOTION_DOWN:              self.move(        f' DOWN (          {motion})',  1)
            elif motion == pygwink.MOTION_LEFT:              self.move(        f' LEFT (          {motion})', -nt)
            elif motion == pygwink.MOTION_RIGHT:             self.move(        f' RIGHT (         {motion})',  nt)
            elif motion == pygwink.MOTION_PREVIOUS_WORD:     msg = f'MOTION_PREVIOUS_WORD (       {motion})'   ;   self.log(msg)   ;   self.quit(msg)
            elif motion == pygwink.MOTION_NEXT_WORD:         msg = f'MOTION_NEXT_WORD (           {motion})'   ;   self.log(msg)   ;   self.quit(msg)
            elif motion == pygwink.MOTION_BEGINNING_OF_LINE: self.move(        f' HOME (          {motion})', -nt *  c)
            elif motion == pygwink.MOTION_END_OF_LINE:       self.move(        f' END (           {motion})',  nt * (nc - self.i[C]))
            elif motion == pygwink.MOTION_PREVIOUS_PAGE:     self.moveUp(      f' PAGE UP (       {motion})')  # move up   to top    of line, wrap down to bottom of prev line
            elif motion == pygwink.MOTION_NEXT_PAGE:         self.moveDown(    f' PAGE DOWN (     {motion})')  # move down to bottom tab on same line, wrap to next line
            elif motion == pygwink.MOTION_BEGINNING_OF_FILE: msg = f'MOTION_BEGINNING_OF_FILE (   {motion})'   ;   self.log(msg)   ;   self.quit(msg)
            elif motion == pygwink.MOTION_END_OF_FILE:       msg = f'MOTION_END_OF_FILE (         {motion})'   ;   self.log(msg)   ;   self.quit(msg)
            elif motion == pygwink.MOTION_BACKSPACE:         self.setTab(      f'BACKSPACE (      {motion})', self.tblank, rev=1)
            elif motion == pygwink.MOTION_DELETE:            self.setTab(      f'DELETE (         {motion})', self.tblank)
            else:                                            msg =             f'(                {motion})'   ;   self.log(msg)   ;   self.quit(msg)
        if dbg: self.log(f'END {self.kbkEvntTxt()} motion={motion}')
#        1353 tabs.py       on_text_motion BGN <   65363> <   65363> <RIGHT           > <16> <MOD_NUMLOCK     > motion=65363
#        1353 tabs.py       on_text_motion BGN <   65363> <   65363> <RIGHT           > < 8> <MOD_CAPSLOCK    > motion=65363
    def on_style_text(self, start, end, attributes): msg = f'{start=} {end=} {fmtm(attributes)}'  ;  self.log(msg)  ;  self.quit(msg)
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
    def isAltShift(mods):     return mods & pygwink.MOD_ALT  and mods & pygwink.MOD_SHIFT
    @staticmethod
    def isCtrlAlt(mods):      return mods & pygwink.MOD_CTRL and mods & pygwink.MOD_ALT
    @staticmethod
    def isCtrlAltShift(mods): return mods & pygwink.MOD_CTRL and mods & pygwink.MOD_ALT and mods & pygwink.MOD_SHIFT
    @staticmethod
    def isNumLock(mods):      return mods & pygwink.MOD_NUMLOCK
    @staticmethod
    def isCapsLock(mods):     return mods & pygwink.MOD_CAPSLOCK
    def isBTab(self, text):   return 1 if text in self.tblanks else 0
#    def isNBTab(text):        return 1 if                        self.sobj.isFret(text) or text in util.DSymb.SYMBS else 0
    def isTab(self, text):    return 1 if text == self.tblank or self.sobj.isFret(text) or text in util.DSymb.SYMBS else 0
    def isParsing(self):      return 1 if self.inserting or self.jumping or self.settingN or self.shiftingTabs or self.swapping else 0
#    def isEH(t): return 1 if t == '#' or t == 'b' else 0
    @staticmethod
    def afn(fn): return fn if len(fn) == 1 and '0' <= fn <= '9' else chr(ord(fn[1]) - ord('0') + ord('a')) if len(fn) == 2 and fn[0] == '1' else None
    ####################################################################################################################################################################################################
    def flipBGC(self, how=''):
        self.log(f'{how} {self.BGC=}') if how else None
        self.BGC = (1 + self.BGC) % 2
        self._initColors()
        if self.RESIZE:    self.resizeTniks()

    def move2LastTab(self, how, page=0, dbg=1):
        np, nl, ns, nc, nt = self.n    ;   p, l, s, c, t = self.j()  ;  i = p
        n = p * nl + l     ;   tp = nc * nt
        if page: tp *= nl  ;  n //= nl
        if dbg:    self.log(f'BGN {how} {page=} {self.fplct()} {i=:4} {n=} {tp=:3} {tp*n=:4} for({tp*(n+1)-1:4}, {tp*n-1:4}, -1)', pos=1)
        for i in range(tp*(n+1)-1, tp*n-1, -1):
            if not self.sobj.isFret(self.tabls[i].text): continue
            p, l, c, t = self.cc2plct(i, dbg=1)  ;  break
        self.moveTo(how, p, l, c, t, dbg=dbg)
        if dbg:    self.log(f'END {how} {page=} {self.fplct()} {i=:4} {n=} {tp=:3} {tp*n=:4} for({tp*(n+1)-1:4}, {tp*n-1:4}, -1)', pos=1)
    def move2FirstTab(self, how, page=0, dbg=1):
        np, nl, ns, nc, nt = self.n    ;   p, l, s, c, t = self.j()  ;  i = p
        n = p * nl + l     ;   tp = nc * nt
        if page: tp *= nl  ;  n //= nl
        if dbg:    self.log(f'BGN {how} {page=} {self.fplct()} {i=:4} {n=} {tp=:3} {tp*n=:4} for({tp*n:4}, {tp*(n+1):4}, 1)', pos=1)
        for i in range(tp*n, tp*(n+1), 1):
            if not self.sobj.isFret(self.tabls[i].text): continue
            p, l, c, t = self.cc2plct(i, dbg=1)  ;  break
        self.moveTo(how, p, l, c, t, dbg=dbg)
        if dbg:    self.log(f'END {how} {page=} {self.fplct()} {i=:4} {n=} {tp=:3} {tp*n=:4} for({tp*n:4}, {tp*(n+1):4}, 1)', pos=1)
    ####################################################################################################################################################################################################
    def prevPage(self, how, dbg=1):
        p, l, c, t = self.j2()   ;   n = self.n[P] - 1
        if dbg: self.log(f'BGN {how} {self.fmti()}', pos=1)
        self.moveTo(how, p-1 if p>0 else n, l, c, t)
#        self.flipPage(how, -1, dbg=1)
        if dbg: self.log(f'END {how} {self.fmti()}', pos=1)

    def nextPage(self, how, dbg=1):
        p, l, c, t = self.j2()   ;   n = self.n[P] - 1
        if dbg: self.log(f'BGN {how} {self.fmti()}', pos=1)
        self.moveTo(how, p+1 if p<n else 0, l, c, t)
#        self.flipPage(how, 1, dbg=1)
        if dbg: self.log(f'END {how} {self.fmti()}', pos=1)
    ####################################################################################################################################################################################################
    def moveUp(self, how, dbg=1):
        p, l, s, c, t = self.j()  ;  n = self.n[T] - 1  ;  m = self.n[L] - 1
        if dbg: self.log(f'BGN {how}', pos=1)
        if t>0: self.moveTo(how, p, l,                 c, 0) # move up   to top    of      line
        else:   self.moveTo(how, p, l-1 if l>0 else m, c, n) # move up   to bottom of prev line, wrap down to bottom of last line
        if dbg: self.log(f'END {how}', pos=1)
    def moveDown(self, how, dbg=1):
        p, l, s, c, t = self.j()  ;  n = self.n[T] - 1  ;  m = self.n[L] - 1
        if dbg: self.log(f'BGN {how}', pos=1)
        if t<n: self.moveTo(how, p, l,                 c, n) # move down to bottom of      line
        else:   self.moveTo(how, p, l+1 if l<m else 0, c, 0) # move down to top    of next line, wrap up to top of first line
        if dbg: self.log(f'END {how}', pos=1)
    def moveLeft(self, how, dbg=1):
        p, l, s, c, t = self.j()  ;  n = self.n[C] - 1  ;  m = self.n[L] - 1
        if dbg: self.log(f'BGN {how}', pos=1)
        if c>0: self.moveTo(how, p, l,                 0, t) # move left  to bgn of      line
        else:   self.moveTo(how, p, l-1 if l>0 else m, n, t) # move left  to end of prev line, wrap right to bottom of last line
        if dbg: self.log(f'END {how}', pos=1)                # move right & up to end of prev line, wrap down to bottom of last line
    def moveRight(self, how, dbg=1):
        p, l, s, c, t = self.j()  ;  n = self.n[C] - 1  ;  m = self.n[L] - 1
        if dbg: self.log(f'BGN {how}', pos=1)
        if c<n: self.moveTo(how, p, l,                 n, t) # move right to end of      line
        else:   self.moveTo(how, p, l+1 if l<m else 0, 0, t) # move right to bgn of next line, wrap left to top of first line
        if dbg: self.log(f'END {how}', pos=1)                # move left & down to bgn of next line, wrap left to top of first line
    ####################################################################################################################################################################################################
    def moveTo(self, how, p, l, c, t, ss=0, dbg=1):
        if dbg:    self.log(f'BGN {how}', pos=1)
        self._moveTo(p, l, c, t)
        self.moveCursor(ss, how)
        if dbg:    self.log(f'END {how}', pos=1)

    def move(self, how, n, ss=0, dbg=1):
        if dbg:    self.log(f'BGN {n=} {how}', pos=1)
        p, l, c, t = self.j2()
        self._moveTo(p, l, c, t, n=n)
        if self.CURSOR and self.cursor: self.moveCursor(ss, how)
        if dbg:    self.log(f'END {n=} {how}', pos=1)

    def _moveTo(self, p, l, c, t, n=0, dbg=1): # todo
        if dbg: self.log(f'BGN {n=} plct={self.fplct(p, l, c, t)}', pos=1)
        np, nl, ns, nc, nt = self.n
        t2        =       n  + t
        c2        = t2 // nt + c
        l2        = c2 // nc + l
        p2        = l2 // nl + p
        self.i[T] = t2  % nt + 1
        self.i[C] = c2  % nc + 1
        self.i[L] = l2  % nl + 1
        self.i[P] = p2  % np + 1
        if dbg: self.log(f'END {n=} {self.fmti()} plct={self.fplct(p, l, c, t)} plct2={self.fplct(p2, l2, c2, t2)}', pos=1)
    ####################################################################################################################################################################################################
    def autoMove(self, how, dbg=1):
        self.log(f'BGN {how}', pos=1)
        ha = 1 if self.hArrow == RARROW else -1
        va = 1 if self.vArrow == DARROW else -1
        n, i  = self.n[T], self.i[T]
        mmDist  = ha * n
        cmDist  = va
        amDist  = mmDist + cmDist
        if dbg:   self.dumpCursorArrows(f'{self.fmtPos()}     {how} M={mmDist} C={cmDist} A={amDist}')
        if        self.csrMode == MELODY:                               self.move(how,   mmDist)
        elif      self.csrMode == CHORD:
            if    i==1 and self.vArrow==UARROW and self.hArrow==RARROW: self.move(how,   n*2-1)
            elif  i==6 and self.vArrow==DARROW and self.hArrow==LARROW: self.move(how, -(n*2-1))
            else:                                                       self.move(how,   cmDist)
        elif      self.csrMode == ARPG:                                 self.move(how,   amDist)
        self.log(f'END {how}', pos=1)
    ####################################################################################################################################################################################################
    def jump(self, how, txt='0', a=0): # optimize str concat?
        cc = self.cursorCol()                 ;    self.jumpAbs = a
        self.log(    f'{how} {txt=} {a=} {cc=} jt={self.jumpAbs} {self.fmti()}')
        if not self.jumping:                       self.jumping = 1
        elif txt.isdecimal():                      self.jumpStr += txt
        elif txt == '-' and not self.jumpStr:      self.jumpStr += txt
        elif txt == W:
            self.log(f'{how} {txt=} {a=} {cc=} jt={self.jumpAbs} {self.jumpStr=} {self.fmti()}')
            jcc  = self.n[T] * int(self.jumpStr)
            self.jumping = 0   ;   self.jumpStr = Z
            self.move(how, jcc - 1 - a * cc)
            self.log(f'{how} {txt=} {a=} {cc=} jt={self.jumpAbs} {jcc=} moved={jcc - 1 - a * cc} {self.fmti()}')
    ####################################################################################################################################################################################################
    def flipSelectAll(self, how):
        self.dumpSmap(f'BGN {how} {self.allTabSel=}')
        if   self.allTabSel:       self.unselectAll(how)   ;   self.allTabSel = 0
        else:                      self.selectAll(how)     ;   self.allTabSel = 1
        self.dumpSmap(f'END {how} {self.allTabSel=}')

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
    def setLLStyle(self, cc, style, dbg=0):
        if not self.LL or not self.qclms: msg = f'SKIP {self.LL=} {len(self.qclms)=}'     ;  self.log(msg)  ;  self.quit(msg)
        p, l, c, t = self.cc2plct(cc)
        bold, italic = 0, 0   ;   np, nl, ns, nc, nt = self.n
        i = c + l * nc if self.qclms else 0
        if   style == NORMAL_STYLE:    bold = 0   ;  italic = 0
        elif style == CURRENT_STYLE:   bold = 1   ;  italic = 1
        elif style == SELECT_STYLE:    bold = 1   ;  italic = 1
        else: msg = f'ERROR Invalid style @ plct={self.fplct(p, l, c, t)} {i=} {style=}'  ;  self.log(msg)  ;  self.quit(msg)
        (bs, fs) = (0, 1) if style == NORMAL_STYLE else (1, 0)
#        d = self.qclms[i].document # #
#        d.set_style(0, len(d.text), {COLOR: self.llcolor(i, Q)[fs], BGC: self.llcolor(i, Q)[bs]}) # #
        self.setTC(self.qclms[i], self.llcolor(i, Q)[fs], self.llcolor(i, Q)[bs])
        self.qclms[i].bold   = bold
        self.qclms[i].italic = italic
        if dbg: self.log(f'     {i=} = {c=} + {l=} * {nc=} * {nt=} {style=} {bold=} {italic=} {cc=}', pos=1)
    ####################################################################################################################################################################################################
    def llcolor(self, i, j, dbg=0):
        nc = self.n[C]  ;   n = 1
        mp = i % nc + n
        msg = f'{i=} {j=} {nc=} {i%nc=} {n=} {mp=}=i%nc+n {mp%10=}' if dbg else Z
        if j == Q and not mp % 10: # and i:
            self.log(  f'if   {msg} {self.k[R]=}') if dbg else None   ;   return self.k[R]
        self.log(f'else {msg} {self.k[j]=}') if dbg else None         ;   return self.k[j]
    ####################################################################################################################################################################################################
    def setTNIKStyle(self, k, nt, style, text=Z, blank=0): # optimize str concat?
        for t in range(k, k + nt):
            msg = f'{t=} {k=} {nt=} {blank=}' #  {text=:{self.n[T]}
            if self.tabls: self._setTNIKStyle(self.tabls[t], self.k[T], style)  ;  text += self.tabls[t].text
            if self.notes: self._setTNIKStyle(self.notes[t], self.k[N], style)
            if self.ikeys: self._setTNIKStyle(self.ikeys[t], self.k[I], style)
            if self.kords: self._setTNIKStyle(self.kords[t], self.k[K], style)
            if blank: p, l, c, r = self.cc2plct(t)  ;  self.setDTNIK(self.tblank, t, p, l, c, t - k, kk=1 if t == k + nt - 1 else 0)
            self.log(f'{msg} {text=:{self.n[T]}}')
#            self.log(f'END {t=} {k=} {nt=} {blank=} {text=}')
        return text

    def _setTNIKStyle(self, tnik, color, style=0): # d =  tnik.document ; d.set_style(0, len(d.text), {COLOR: color[fgs], BGC: color[bgs]})
        (bgs, fgs) = (0, 1)  if style == NORMAL_STYLE else (1, 0)
        if util.isi(tnik, LBL):   self.setTC(tnik, color[fgs], color[bgs])
    @staticmethod
    def setTC(t, fgc, bgc=None):
        cm = {COLOR:fgc}
        if bgc:             cm[BGC] = bgc
        d = t.document  ;  d.set_style(0, len(d.text), cm)
    ####################################################################################################################################################################################################
    def selectTabs(self, how, m=0, cn=None, dbg=1, dbg2=1):
        cc         = self.cursorCol()  ;  old = cn
        p, l, c, t = self.cc2plct(cc)
        if cn is None:      cn = self.cc2cn(cc) # self.plc2cn_(p, l, c)
        nt = self.n[T]  ;   k  = cn * nt   ;   style = SELECT_STYLE
        self.log(f'{m=} {old=} {cc=} {cn=} {nt} {k=} {self.fplct(p, l, c, t)}')
        if cn in self.smap: self.log(f'RETURN: {cn=} already in smap={fmtm(self.smap)}') if dbg2 else None   ;   return
        if dbg:             self.dumpSmap(f'BGN {how} {m=} {cn=} {cc=} {k=}')
        text              = self.setTNIKStyle(k, nt, style)
        self.smap[cn]     = text
        if m:               self.move(how, m, ss=1)
        if dbg:             self.dumpSmap(f'END {how} {m=} {cn=} {cc=} {k=}')
    ####################################################################################################################################################################################################
    def unselectTabs(self, how, m, cn=None, dbg=0):
        if cn is None:      cc = self.cc   ;      cn = self.cc2cn(cc)
        else:               cc = self.cn2cc(cn)
        nt = self.n[T]  ;   k = cn * nt    ;   style = NORMAL_STYLE
        if self.LL:         self.setLLStyle(cc, style)
        if dbg:             self.dumpSmap(f'BGN {how} {m=} {cn=} {cc=} {k=}')
        self.setTNIKStyle(k, nt, style)
        if cn in self.smap: self.smap.pop(cn)
        elif dbg:           self.log(f'{cn=} not found in smap={fmtm(self.smap)}')
        if m:               self.move(how, m)
        if dbg:             self.dumpSmap(f'END {how} {m=} {cn=} {cc=} {k=}')
    ####################################################################################################################################################################################################
    def copyTabs(self, how, dbg=1): # optimize str concat?
        self.dumpSmap(f'BGN {how}')   ;   nt = self.n[T]   ;   style = NORMAL_STYLE   ;   text = []
        for k in list(self.smap.keys()):
            k *= nt
            if self.LL:  self.setLLStyle(k, style)
            text.append(self.setTNIKStyle(k, nt, style))
            if dbg: text.append(W)
        if dbg:         self.log(f'{Z.join(text)=}')
        self.dumpSmap(f'END {how}')
        if self.SNAPS:  self.regSnap(f'{how}', 'COPY')
    ####################################################################################################################################################################################################
    def cutTabs(self, how): self.log('BGN Cut = Copy + Delete')  ;  self.copyTabs(how)  ;  self.log('Cut = Copy + Delete')  ;  self.deleteTabs(how, keep=1)  ;  self.log('END Cut = Copy + Delete')
    ####################################################################################################################################################################################################
    def deleteTabs(self, how, keep=0, dbg=1):
        self.dumpSmap(f'BGN {how} {keep=}')   ;   style = NORMAL_STYLE   ;   nt = self.n[T]
        for k, text in self.smap.items():
            cn = k   ;   k *= nt
            if dbg:     self.log(f'{k=} {cn=} {text=}')
            if self.LL: self.setLLStyle(k, style)
            self.setTNIKStyle(k, nt, style, blank=1)
        if not keep:    self.unselectAll(f'deleteTabs({keep=})')
        self.dumpSmap(f'END {how} {keep=}')
        if self.SNAPS:  self.regSnap(f'{how}', 'DELT')
        self.rsyncData = 1

    def pasteTabs(self, how, kk=0, dbg=1):
        cc = self.cursorCol()       ;   nt = self.n[T]
        cn = self.normalizeCC(cc)   ;   kt = 0
        p, l, s, c, t = self.j()
        self.dumpSmap(f'BGN {how} {kk=} {cc=} {cn=}={self.cc2cn(cc)} plct={self.fplct(p, l, c, t)}')
        for i, (k, text) in enumerate(self.smap.items()):
            if not i:   dk = 0
            elif kk:    dk = i * nt
            else:       dk = (list(self.smap.keys())[i] - list(self.smap.keys())[0]) * nt
            if dbg:     self.log(f'{i=} {k=} {text=} {kk=} {dk=}')
            for n in range(nt):
                kt         = (cn + dk + n) % self.tpp # todo
                p, l, c, t = self.cc2plct(kt)
                self.setDTNIK(text[n], kt, p, l, c, n, kk=1 if n==nt-1 else 0)
            if dbg:     self.log(f'{i=} {k=} {text=} {kk=} {dk=} {kt=}')
        self.log(f'clearing {len(self.smap)=}')   ;   self.smap.clear()
        self.dumpSmap(f'END {how} {kk=} {cc=} {cn=}={self.cc2cn(cc)} plct={self.fplct(p, l, c, t)}')
        if self.SNAPS:  self.regSnap(f'{how}', 'PAST')
        self.rsyncData = 1
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

    def swapTab(self, how, txt=Z, data=None, dbg=0, dbg2=1):  # e.g. c => 12 not same # chars asserts
        src, trg = self.swapSrc, self.swapTrg
        data = data or self.data
        if not self.swapping: self.swapping = 1
        elif txt.isalnum():
            if   self.swapping == 1:   src += txt;   self.log(f'    {how} {txt=} {self.swapping=} {src=} {trg=}') # optimize str concat?
            elif self.swapping == 2:   trg += txt;   self.log(f'    {how} {txt=} {self.swapping=} {src=} {trg=}') # optimize str concat?
            self.swapSrc, self.swapTrg = src, trg
        elif txt == '\r':
            self.log(f'    {how} {self.swapping=} {src=} {trg=}')
            if   self.swapping == 1 and not trg: self.swapping = 2;   self.log(f'{how} waiting {src=} {trg=}') if dbg else None   ;   return
            if   self.swapping == 2 and trg:     self.swapping = 0;   self.log(f'{how} BGN     {src=} {trg=}') if dbg else None
            np, nl, ns, nc, nt = self.n    ;     nc += self.zzl()
            cc0 = self.cursorCol()         ;     p0, l0, c0, t0 = self.cc2plct(cc0)   ;   self.log(f'BFR {cc0=} {p0=} {l0=} {c0=} {t0=}')
            blanks = self.tblanks          ;     blank = 1 if src in blanks and trg in blanks else 0
            if blank:
                for t in self.tabls:   t.text = trg if t.text==src else None
                for n in self.notes:   n.text = trg if n.text==src else None
                for i in self.ikeys:   i.text = trg if i.text==src else None
                for k in self.kords:   k.text = trg if k.text==src else None
#                for i in range(len(self.tabls)):
#                    if self.tabls and self.tabls[i].text == src: self.tabls[i].text = trg
#                    if self.notes and self.notes[i].text == src: self.notes[i].text = trg
#                    if self.ikeys and self.ikeys[i].text == src: self.ikeys[i].text = trg
#                    if self.kords and self.kords[i].text == src: self.kords[i].text = trg
            else:
                for p in range(np):
                    for l in range(nl):
                        for c in range(nc):
                            text = data[p][l][c]
                            for t in range(nt):
                                if text[t] == src:
                                    if dbg2: self.log(f'Before data{self.fplc(p, l, c)}={text}')
                                    cc = self.plct2cc(p, l, c, t)   ;   self.setDTNIK(trg, cc, p, l, c, t, kk=1)
                                    if dbg2: self.log(f'After  data{self.fplc(p, l, c)}={text}')
            self.swapSrc, self.swapTrg = Z, Z
            self.log(f'{how} END     {src=} {trg=}') if dbg else None
#                if dbg2: self.dumpTniks('SWAP')
#                self.moveTo(how, p0, l0, c0, t0)  ;  cc = self.cursorCol()  ;  self.log(f'AFT {cc0=} {p0=} {l0=} {c0=} {t0=} {cc=}')
            if self.SNAPS: self.regSnap(f'{how}', 'SWAP')
            self.rsyncData = 1

    def insertSpace(self, how, txt='0', dbg=1): # optimize str concat?
        cc = self.cursorCol()   ;   c0 = self.cc2cn(cc)
        if not self.inserting: self.inserting = 1   ;    self.setCaption('Enter nc: number of cols to indent int')
        elif txt.isdecimal():  self.insertStr += txt
        elif txt in (W, '/r'):
            self.inserting = 0
            width = int(self.insertStr)
            tcs   = sorted(self.cobj.mlimap)
            tcs.append(self.n[C] * self.n[L] - 1)
            tcs   = [ t + 1 for t in tcs ]
            if dbg: self.log(f'BGN {how} Searching for space to insert {width} cols starting at colm {c0}')
            self.log(f'{fmtl(tcs, ll=1)} insertSpace', p=0)
            found, c1, c2 = 0, 0, None   ;   self.insertStr = Z
            for c2 in tcs:
                if dbg: self.log(f'w c0 c1 c2 = {width} {c0} {c1} {c2}')
                if c2 > c0 + width and c2 > c1 + width: found = 1  ;  break
                c1 = c2
            if not found: self.log(f'{how} starting at colm {c0} No room to insert {width} cols before end of page at colm {tcs[-1]+1}')  ;   return
            self.log(f'{how} starting at colm {c0} Found a gap {width} cols wide between cols {c1} and {c2}')
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
                self.setLLStyle(k, NORMAL_STYLE) if self.LL else None
            self.setCaption('Enter nf: number of frets to shift +/- int')
        elif nf == '-': self.shiftSign = -1
        elif self.sobj.isFret(nf):
            self.shiftingTabs = 0     ;   nt = self.n[T]
            for cn, v in self.smap.items():
                cc = self.cn2cc(cn)   ;   p, l, c, r = self.cc2plct(cc, dbg=0)
                self.log(f'{cc=} {cn=} {v=} text={v}')
                for t in range(nt):
                    text = v[t]    ;    kt = cc + t    ;    fn = 0   ;   ntones = Notes.NTONES * 2
                    if self.sobj.isFret(text):
                        fn = self.afn(str((self.tab2fn(text) + self.shiftSign * self.tab2fn(nf)) % ntones))  ;  self.log(f'{cc=} {cn=} {t=} {text=} {nf=} {fn=} {self.shiftSign=}')
                    if fn and self.sobj.isFret(fn):  self.setDTNIK(fn, kt, p, l, c, t, kk=1 if t==nt-1 else 0)
            self.shiftSign = 1
            self.rsyncData = 1
            self.unselectAll('shiftTabs()')
        self.dumpSmap(f'END {how} {self.shiftingTabs=} {nf=} {self.shiftSign=}')

    def setn_cmd(self, how, txt=Z, dbg=1): # optimize str concat?
        if not self.settingN: self.settingN = 1   ;  self.setNtxt = Z  ;  self.log(f'BGN {how} {txt=} {self.settingN=} {self.setNvals=}') if dbg else None
        elif txt.isdecimal(): self.setNtxt += txt                      ;  self.log(   f'Concat {txt=} {self.settingN=} {self.setNvals=}') if dbg else None
        elif txt ==  W:       self.setNvals.append(int(self.setNtxt))  ;  self.log(   f'Append {txt=} {self.settingN=} {self.setNvals=}') if dbg else None  ;  self.setNtxt = Z
        elif txt == 'Q':      self.settingN = 0                        ;  self.log(   f'Cancel {txt=} {self.settingN=} {self.setNvals=}') if dbg else None
        elif txt == '\r':
            self.settingN = 0   ;   old = self.n
            self.setNvals.append(int(self.setNtxt))
            if len(self.setNvals) == 4:
                self.n[:2] = self.setNvals[:2]   ;   self.n[3:] = self.setNvals[2:]
            self.log(f'Setting {old=} {self.n=}')
            self.log(f'END {how} {txt=} {self.settingN=} {self.setNvals=}')
    ####################################################################################################################################################################################################
    def rotateSprite(self, how, spr, cw=1):
        old = spr.rotation
        spr.rotation =  (spr.rotation + cw * 10) % 360
        self.log(f'{how} {cw=} {old=} {spr.rotation=}', f=2)
    ####################################################################################################################################################################################################
    def flipFlatSharp(self, how, dbg=0):  #  page line colm tab or select
        t1 = Notes.TYPE    ;    t2 =  Notes.TYPE * -1      ;     Notes.setType(t2)
        self.log(  f'BGN {how} {t1=} {Notes.TYPES[t1]} => {t2=} {Notes.TYPES[t2]}')
        s = self.ss2sl()[0]  ;  np, nl, ns, nc, nt = self.i
        tniks, j, _, tobj = self.tnikInfo(0, 0, s, 0, 0, why=how)
        for i in range(len(tniks)):
            text = Z  ;   sn = i % nt
            if   self.notes: text = self.notes[i].text
            elif self.kords and self.tabls:
                tabtxt = self.tabls[i].text
                text   = self.sobj.tab2nn(tabtxt, sn) if self.sobj.isFret(tabtxt) else self.tblank
            if text in Notes.N2I and (Notes.N2I[text] not in Notes.IS0):
                cc = i * ns    ;   old = text
                p, l, c, t = self.cc2plct(cc)   ;   cn = self.cc2cn(cc)
                if   text in Notes.F2S:  text = Notes.F2S[text]
                elif text in Notes.S2F:  text = Notes.S2F[text]
                self.notes[i].text     = text
                self.log(  f'{old:2} -> {text:2} = ')
                if dbg: self.log(f'{sn=} {cn=:2} {cc=:4} {i=:4} {old:2} => {text:2} {self.notes[i].text=:2} {self.fplct(p, l, c, t)}')
                if self.kords:
                    imap = self.getImap(p, l, c, dbg2=1)
                    self.setChord(imap, i, pos=1, dbg=1)
        util.dumpNic(dict(self.nic))
        self.log(util.fmtKSK(self.ks[util.KSK]), f=2)
        self.log(  f'END {how} {t1=} {Notes.TYPES[t1]} => {t2=} {Notes.TYPES[t2]}')
    ####################################################################################################################################################################################################
    def flipChordNames(self, how, hit=0, dbg=1):
        cc = self.cc    ;    cn = self.cc2cn(cc)
        mks = list(self.cobj.mlimap.keys())   ;   sks = list(self.smap.keys())
        if sks and not hit:
            if dbg: self.dumpSmap(f'BGN {how} mks={fmtl(mks)} {cn=:2} {hit=} sks={fmtl(sks)}')
            [ self.flipChordName(how, k) for k in sks ]
        else:
            if dbg: self.dumpSmap(f'BGN {how} mks={fmtl(mks)} {cn=:2} {hit=} sks={fmtl(sks)}')
            if hit: self.flipChordNameHits(how, cn)
            else:   self.flipChordName(    how, cn)
        if dbg:     self.dumpSmap(f'END {how} mks={fmtl(mks)} {cn=:2} {hit=} sks={fmtl(sks)}')

    def flipChordNameHits(self, how, cn, dbg=1): # optimize str concat?
        mli = self.cobj.mlimap   ;   mks = list(mli.keys())   ;   cn2 = -1
        if cn not in mks: msg = f'ERROR: {cn=} not in {fmtl(mks)=}'   ;   self.log(msg)   ;   self.quit(msg)
        ivals =  [ u[1] for u in mli[cn][0] ]
        msg   =  [ fmtl(v, w="x") for v in ivals ]
        if dbg: self.log(f'BGN {how} mks={fmtl(mks)} cn={cn:2} ivals={fmtl(msg, d=Z)}')
        hits = self.ivalhits(ivals, how)
        for cn2 in hits:
            if cn2 not in self.smap: self.selectTabs(how, m=0, cn=cn2)
            self.flipChordName(how, cn2)
        if dbg: self.log(f'END {how} mks={fmtl(mks)} cn2={cn2:2} ivals={fmtl(msg, d=Z)}')

    def ivalhits(self, ivals, how, dbg=1):
        mli = self.cobj.mlimap    ;   mks = list(mli.keys())   ;   hits = set()
        for cn, lim in mli.items():
            for im in lim[0]:
                if cn in hits: break
                for iv in ivals:
                    iv1 = sorted(iv)      ;   iv2 = sorted(im[1])
                    if iv1 == iv2:   hits.add(cn)  ;   break
        if dbg: self.log(f'    {how} mks={fmtl(mks)} hits={fmtl(hits)}')
        return list(hits)

    def flipChordName(self, how, cn, dbg=1, dbg2=1):
        cc = self.cn2cc(cn)            ;   mli = self.cobj.mlimap
        p, l, c, t = self.cc2plct(cc)  ;   msg = Z
        if not self.ikeys and not self.kords: msg +=  'ERROR: Both ikeys and chords are Empty '
        if cn not in mli:                     msg += f'ERROR: {cn=} not in mks={fmtl(list(mli.keys()))}'
        if msg: self.log(msg)          ;   return
        limap      = mli[cn][0]        ;   imi = mli[cn][1]
        imi        = (imi + 1) % len(limap)
        mli[cn][1] = imi
        ikeys, ivals, notes, chordName, chunks, rank = limap[imi]
        if self.ikeys and ikeys:                self.setIkeyText(ikeys, cc, p, l, c)
        if self.kords and chordName and chunks: self.setChordName(cc, chordName, chunks)
        elif dbg: self.log(f'    {how} {cn=} {cc=} is NOT a chord')
        if dbg2:  self.cobj.dumpImap(limap[imi], why=f'{cn:2}')
#        assert imi == limap[imi][-1],   f'{imi=} {limap[imi][-1]=}'
    ####################################################################################################################################################################################################
    def flipPage(self, how, dp=1, dbg=1):
        pA = self.j()[P] if dbg else None
        self.flipVisible(how, self.j()[P])
        if dbg: pB = self.j()[P]    ;   self.log(f'{pA=} {pB=}, {self.fmtJ1()}, {self.fmtJ2()}', p=0)
        self.dumpVisible()  ;   self.dumpVisible2()
        self.i[P] = ((self.j()[P] + dp) % self.n[P]) + 1 # todo
        if dbg: pA = self.j()[P]
        self.flipVisible(how, self.j()[P])
        if dbg: pB = self.j()[P]    ;   self.log(f'{pA=} {pB=}, {self.fmtJ1()}, {self.fmtJ2()}', p=0)
        self.dumpVisible()  ;   self.dumpVisible2()
        if self.SNAPS and dbg:  self.regSnap(how, f'FlpP{self.i[P]}')
        if self.RESIZE:         self.resizeTniks(dbg)
    ####################################################################################################################################################################################################
    def dumpVisible(self):
        nsum = 0  ;  j = 0  ;  lsum = 0  ;  nmax = 0  ;  a = W*10  ;  b = W*8  ;  c = W*7  ;  d = W*6  ;  e = W*5
        for j in range(len(self.visib) - 1):
            vl = []   ;   n = 0
            for w in self.visib[j]:
                vl.append(str(int(w)))     ;  lsum += 1   ;    n += 1    if w           else 0
            v = Z.join(vl)  ;  l = len(v)  ;  nsum += n   ;  nmax = nsum if nsum > nmax else nmax
            if l:                              self.log(self.fVisible(n, j, l, v), p=0)
        v = Z.join([ f'{a if not i else b if i//10 < 1 else c if i//10 < 10 else d if i//10 < 100 else e}{10+i*10}' for i in range(nmax//10) ])
        j += 1   ;  n = nsum  ;  l = lsum   ;  self.log(self.fVisible(n, j, l, v), p=0)
    @staticmethod
    def fVisible(n, j, l, v): return f'{n:4}{jTEXTS[j][0]}{l:<4}{v}'
    def dumpVisible2(self):
#        consume(consume(self.log(f'{int(self.E[j][i].visible)}', pfx=0, end=W) for i in range(len(self.E[j]))) for j in range(len(self.E)))
#        [ [ self.log(f'{int(self.E[j][i].visible)}', pfx=0, end=W) for i in range(len(self.E[j]))] for j in range(len(self.E)) ]
#        for j in range(len(self.E)):
#            for i in range(len(self.E[j])):
#                self.log(f'{int(self.E[j][i].visible)}', p=0, e=Z)
        for j, e in enumerate(self.E):
            for e2 in e:
                self.log(f'{int(e2.visible)}', p=0, e=Z)
            if len(e): self.log(p=0)
    def fVis(self): return f'{fmtl([ i + 1 if p.visible else W for i, p in enumerate(self.pages) ])}'
    ####################################################################################################################################################################################################
    def flipCursorMode(self, how, m):
        self.log(f'BGN {how} {self.csrMode=} = {CSR_MODES[self.csrMode]=}')
        self.csrMode  = (self.csrMode + m) % len(CSR_MODES)
        self.log(f'END {how} {self.csrMode=} = {CSR_MODES[self.csrMode]=}')

    def flipArrow(self, how, v=0, dbg=0):
        if dbg: self.log(f'BGN {how} {v=} {self.hArrow=} = {HARROWS[self.hArrow]=} {self.vArrow=} = {VARROWS[self.vArrow]=}')
        if v: self.vArrow  = (self.vArrow + 1) % len(VARROWS)
        else: self.hArrow  = (self.hArrow + 1) % len(HARROWS)
        if dbg: self.log(f'END {how} {v=} {self.hArrow=} = {HARROWS[self.hArrow]=} {self.vArrow=} = {VARROWS[self.vArrow]=}')
    ####################################################################################################################################################################################################
    def flipFullScreen(self, how):
        self.FULL_SCRN = not self.FULL_SCRN
        self.set_fullscreen( self.FULL_SCRN)
        self.log(   f'{how} {self.FULL_SCRN}=')

    def flipBlank(self, how):
        prevBlank    =  self.tblank
        self.log(f'BGN {how} {prevBlank=}')
        self.tblanki = (self.tblanki + 1) % len(self.tblanks)
        self.tblank  =  self.tblanks[self.tblanki]
        self.swapSrc, self.swapTrg, self.swapping = prevBlank, self.tblank, 2
        self.swapTab(how, '\r')
        self.swapSrc, self.swapTrg = Z, Z
        self.log(f'END {how} {self.tblank=}')
    ####################################################################################################################################################################################################
    def dumpCursorArrows(self, how): cm, ha, va = self.csrMode, self.hArrow, self.vArrow  ;  self.log(f'{how} csrMode={cm}={CSR_MODES[cm]:6} hArrow={ha}={HARROWS[ha]:5} vArrow={va}={VARROWS[va]:4}')
    def reverseArrow(self, dbg=1):
        if dbg: self.dumpCursorArrows('reverseArrow()')
        if self.csrMode in (MELODY, ARPG): self.flipArrow('reverseArrow() MELODY or ARPG', v=0)
        if self.csrMode in (CHORD, ARPG):  self.flipArrow('reverseArrow() CHORD or ARPG',  v=1)
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
        self.nic.clear()
        self.dumpBlanks()
        for t in self.tabls:
            t.text = self.tblank
        for n in self.notes:
            n.text = self.tblank
        for i in self.ikeys:
            i.text = self.tblank
        for k in self.kords:
            k.text = self.tblank
        for p in range(np):
            for l in range(nl):
                for c in range(nz, nc):
                    self.data[p][l][c-nz] = self.tblankCol
        self.log(f'END {how} {np=} {nl=} {ns=} {nc=} {nt=}')
        self.rsyncData = 1

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
        if dbg: self.log(f'.ki={fmtl(self.ki[:10])} {j=} {k=} kl={fmtl(kl)} {self.ki[j]=} {kk=}')
        return kk
    ####################################################################################################################################################################################################
    def regSnap(self, why, typ, dbg=1):
        self.snapWhy  = why
        self.snapType = typ
        self.snapReg  = 1
        if dbg: self.log(f'{self.LOG_ID:3} {self.snapId:3} {self.snapType:8} {self.snapWhy}')

    def snapshot(self, why=Z, typ=Z, dbg=1, dbg2=1):
        why       = why if why else self.snapWhy
        typ       = typ if typ else self.snapType
        snapId    = self.snapId    ;    logId     = self.LOG_ID
        snapName  = f'{BASE_NAME}.{logId}.{snapId}.{typ}.{PNG}'
        SnapPath  = BASE_PATH / PNGS / snapName
        if dbg:     self.log(f'{BASE_NAME=} {logId=} {snapId=} {typ=} {PNG=}')
        if dbg:     self.log(f'{self.fNameLid=} {PNGS=} {snapName=} {why}')
        if dbg:     self.log(f'{SnapPath=}', p=2)
        pyglet.image.get_buffer_manager().get_color_buffer().save(f'{SnapPath}')
        if dbg2:    self.log(f'{snapName=} {why}', f=2)
        self.snapId += 1
        return SnapPath
    ####################################################################################################################################################################################################
    def deleteGlob(self, g, why=Z):
        self.log(f'deleting {len(g)} files from glob {why=}')
        for f in g:
            self.log(f)
            os.system(f'del {f}')

    def getFileSeqName(self, fdir='files', fsfx='txt'):
        fdir += '/'
        self.log(f'{fdir=} {fsfx=}')
        pathlib.Path(fdir).mkdir(parents=True, exist_ok=True)
        fGlobArg = f'{(BASE_PATH / fdir / BASE_NAME)}.*.{fsfx}'
        fGlob = glob.glob(fGlobArg)
        self.log(f'{fGlobArg=}')
        self.LOG_ID = 1 + self.getFileSeqNum(fGlob, fsfx)
        return f'{BASE_NAME}.{self.LOG_ID}'

    def getFileSeqNum(self, files, sfx, dbg=0, dbg2=0):
        i = -1  ;  fsfx = f'.{sfx}'
        if len(files):
            if dbg2: self.log(f'{sfx=} files={fmtl(files)}')
            ids =  [ self.sid(s, fsfx) for s in files if s.endswith(fsfx) and util.isi(self.sid(s, fsfx), int) ]
            if dbg:  self.log(f'ids={fmtl(ids)}')
            i = max(ids) if ids else 0
        return i
    @staticmethod
    def sid(s, sfx):
        s = s[:-len(sfx)]
        j = s.rfind('.')
        i = s[j+1:]
        return int(i) if util.isi(i, str) and i.isdigit() else None
    ####################################################################################################################################################################################################
    def log(self, t=Z, p=1, pos=0, f=1, s=Y, e='\n', ff=False):
        if pos:   t = f'{self.fmtPos()} {t}'
        slog(t, p, f, s, e, ff)
    def olog(self, *o, p=1, pos=0, f=1, s=Y, e='\n', ff=False):
        if pos:   pos = f'{self.fmtPos()}'
        olog((pos, o), p, f, s, e, ff)
    ####################################################################################################################################################################################################
    def quit(self, why=Z, error=1, save=1, dbg=1):
        hdr1 = self.fTnikHdr(1)  ;  hdr0 = self.fTnikHdr(0)  ;  self.log(hdr1, p=0, f=2)  ;  self.log(hdr0, p=0, f=2)   ;   err = f'Error={error}'
        self.log(f'BGN {why} {err} {save=} {self.quitting=}', f=2)                  ;   self.log(util.QUIT, p=0, f=2)   ;   msg = 'Recursion Error'
        self.log(util.QUIT_BGN, p=0, f=2)    ;    util.dumpStack(inspect.stack())   ;   self.log(util.QUIT, p=0, f=2)
        if self.quitting:        msg += f' {self.quitting=} Exiting'  ;  self.log(msg, f=2)  ;  self.close()   ;   return
        self.dumpTniksSfx(why)         ;    self.quitting += 1
        if not error:
            util.dumpStack(util.MAX_STACK_FRAME)
            if dbg:  self.dumpStruct(why, csv=1, dbg=dbg)
            if save: self.saveDataFile(why, self.dataPath1)
            if dbg:  self.transposeData(dump=1 if dbg else 0)
            if dbg:  self.cobj.dumpMlimap(why)
        if self.SNAPS:                      self.snapshot(f'quit {error} {save=}', 'QUIT')
        self.log(f'END {why} {err} {save=} {self.quitting=}', f=2)       ;   self.log(util.QUIT_END, p=0, f=2)
        self.cleanupFiles()
#        self.close()
        self.log(f'END {why} {err} {save=} {self.quitting=}', f=0)       ;   self.log(util.QUIT_END, p=0, f=0)
        print('Calling close()', end=Y)
        self.close()
#        print('Calling pyglet.app.exit()', end=Y)
#        pyglet.app.exit()
#        print('Calling exit()')
#        exit()
    ####################################################################################################################################################################################################
    def cleanupFiles(self):
        self.cleanupCsvFile()
        self.cleanupCatFile() if self.cobj.umap else None

    def cleanupCsvFile(self):
        if not CSV_FILE.closed:
            self.log(f'Closing {CSV_FILE.name}', ff=True)
            CSV_FILE.flush()
            CSV_FILE.close()
        csvPath  = util.getFilePath(BASE_NAME,     BASE_PATH, fdir=CSVS, fsfx=CSV)
        csvPath2 = util.getFilePath(self.CSV_GFN,  BASE_PATH, fdir=CSVS, fsfx=Z)
        csvPath3 = util.getFilePath(self.fNameLid, BASE_PATH, fdir=CSVS, fsfx=CSV)
        self.makeSubDirs(csvPath2)
        self.log(f'Copying {CSV_FILE.name} to {csvPath2}', f=2)
        util.copyFile(csvPath, csvPath2)
        self.makeSubDirs(csvPath3)
        self.log(f'Copying {CSV_FILE.name} to {csvPath3}', f=2)
        util.copyFile(csvPath, csvPath3)

    def cleanupCatFile(self):
        CAT_PATH = util.getFilePath(BASE_NAME, BASE_PATH, fdir=CATS, fsfx=CAT)
        pcatPath = util.getFilePath(BASE_NAME, BASE_PATH, fdir=CATS, fsfx=CATP)
        if CAT_PATH.exists():     util.copyFile(CAT_PATH, pcatPath)
        with open(str(CAT_PATH), 'w', encoding='utf-8') as CAT_FILE:
            self.cobj.dumpOMAP( CAT_PATH, merge=1)
            self.log(f'Closing {CAT_FILE.name}', ff=True)
            CAT_FILE.flush()
            CAT_FILE.close()
        catPath  = util.getFilePath(BASE_NAME,     BASE_PATH, fdir=CATS, fsfx=CAT)
        catPath2 = util.getFilePath(self.fNameLid, BASE_PATH, fdir=CATS, fsfx=CAT)
        self.makeSubDirs(catPath2)
        self.log(f'Copying {CAT_FILE.name} to {catPath2}', f=2)
        util.copyFile(catPath, catPath2)
########################################################################################################################################################################################################
# Global Functions BGN
########################################################################################################################################################################################################
def fri(f): return int(math.floor(f + 0.5))
########################################################################################################################################################################################################
def dumpGlobals():
    slog(f'BASE_NAME = {BASE_NAME}', f=2)
    slog(f'argv      = {fmtl(sys.argv, ll=1)}', f=2)
    slog(f'PATH      = {PATH}',      f=2)
    slog(f'BASE_PATH = {BASE_PATH}', f=2)
########################################################################################################################################################################################################
def initRGB(dbg=1):
    if dbg:
        s = W*7  ;  t = f'{s}RGB '
        o = [ f' {o}' for o in range(len(OPC)) ]
        slog(f'RGB{s}{fmtl(o, w=3,d=Z)}{t}Diffs  {t}Steps', p=0, f=2)
    _initRGB('FSH', (255,  10, 255))  # 0
    _initRGB('PNK', (255, 128, 192))  # 1
    _initRGB('RED', (255,  10,  10))  # 2
    _initRGB('RST', (255,  96,  10))  # 3
    _initRGB('PCH', (255, 160, 128))  # 4
    _initRGB('ORG', (255, 176,  10))  # 5
    _initRGB('YLW', (255, 255,  10))  # 6
    _initRGB('LIM', (160, 255,  10))  # 7
    _initRGB('GRN', ( 10, 255,  10))  # 8
    _initRGB('TRQ', ( 10, 255, 192))  # 9
    _initRGB('CYA', ( 10, 255, 255))  # 10
    _initRGB('IND', ( 10, 180, 255))  # 11
    _initRGB('BLU', ( 10,  10, 255))  # 12
    _initRGB('VLT', (128,  10, 255))  # 13
    _initRGB('GRY', (255, 255, 255))  # 14
    _initRGB('CL1', ( 13,  15, 255))  # 15
    _initRGB('CL2', (255, 128,  10))  # 16
    _initRGB('CL3', (250,  65, 190))  # 17
    _initRGB('CL4', (151,  71,  10))  # 18
    return RGB.keys()
########################################################################################################################################################################################################
def _initRGB(key, rgb, dv=32, n=None, dbg=0):
    colors = []  ;  lrgb, lopc = len(rgb), len(OPC)  ;  msg, msgR, msgG, msgB = [], [], [], []  ;  n = n + 1 if n is not None else lopc  ;  opc, color = None, None
    diffs  = [ rgb[i] - rgb[i]/dv for i in range(lrgb) ]
    steps  = [ diffs[i]/(n-1)     for i in range(lrgb) ]
    if dbg: msg.append(f'{key:3}:   O=[')
    for j in range(n):
        clrs = []
        if dbg > 2: slog(f'{key:4} {fmtl(rgb, w=3)} {opc=:2} {OPC[opc]:3} {dv=} {n=} {fmtl(diffs, w=".2f")} ', e=Z);  slog(fmtl(steps, w=".2f"), p=0, f=1)
        for opc in range(lopc):
            if dbg: msg.append(f'{OPC[opc]:3} ' if not j else Z)
            color = list([ fri(rgb[i]/dv + j*steps[i]) for i in range(lrgb) ])  ;  color.append(OPC[opc])  ;  clrs.append(tuple(color))
            if   dbg > 1:       slog(f'{j:2} {key:4} {util.fColor(color)}', p=0, e=W)
        if dbg: slog(p=0)
        if dbg: msgR.append(color[0])  ;  msgG.append(color[1])  ;  msgB.append(color[2])
        colors.append(clrs)
    if dbg:
        msg = Z.join(msg)
        slog( f'{msg[:-1]}] {fmtl(diffs, w="5.1f")} {fmtl(steps, w="4.1f")}', p=0)  ;  msgs = [msgR, msgG, msgB]  ;  rgb = 'RGB'
        for i, msg in enumerate(msgs): slog(f'       {rgb[i]}={fmtl(msg, w=3)}', p=0)
    global RGB  ;  RGB[key] = colors
    return list(RGB.keys())
########################################################################################################################################################################################################
# Global Functions END
#--disable=C0301 --disable=C0304 --disable=C0321 --disable=C0115 --disable=C0116 --disable=R0912 --disable=R0913 --disable=R0914 tabsC.py util.py chord.py
# Globals BGN
########################################################################################################################################################################################################
PATH      = pathlib.Path.cwd() / sys.argv[0]
BASE_PATH = PATH.parent
BASE_NAME = BASE_PATH.stem
CAT,  CSV,  LOG,  PNG,  DAT     = 'cat',  'csv',  'log',  'png',  'dat'
CATS, CSVS, LOGS, PNGS, DATA    = 'cats', 'csvs', 'logs', 'pngs', 'data'
CATP, CSVP, LOGP                = f'_.{CAT}', f'_.{CSV}', f'_.{LOG}'
CSV_FILE, LOG_FILE              = None, None
########################################################################################################################################################################################################
MULTILINE, WRAP_LINES = 'multiline', 'wrap_lines'   ;   LEFT, CENTER, RIGHT, BOTTOM, BASELINE, TOP = 'left', 'center', 'right', 'bottom', 'baseline', 'top'
BGC, BOLD, COLOR, FONT_NAME, FONT_SIZE, ITALIC, KERNING, UNDERLINE = 'background_color', 'bold', 'color', 'font_name', 'font_size', 'italic', 'kerning', 'underline'
ALIGN, INDENT, LEAD, LNSP, STRH, TAB_STOPS, WRAP = 'align', 'indent', 'leading', 'line_spacing', 'stretch', 'tab_stops', 'wrap'
MARGIN_LEFT, MARGIN_RIGHT, MARGIN_TOP, MARGIN_BOTTOM = 'margin_left', 'margin_right', 'margin_top', 'margin_bottom'
TI        = ['tnik', '  i ']
XYWH      = ['    X  ', '    Y  ', '    W  ', '    H  ']
AXY2      = ['x', 'y', 'AncX', 'AncY']
WHVA      = ['CntW', 'CntH', 'v', 'a']
ADN       = ['Ascn', 'Dscn', 'nA-D']
LTXX      = list(itertools.chain(TI, XYWH, AXY2))
LTXXCA    = list(itertools.chain(TI, XYWH, AXY2, WHVA))
LDS       = ['FnSz', 'Lead', 'LnSp', ' ForegroundColor ', ' BackgroundColor ', 'B', 'I', 'S', 'M', 'W', 'w', 'FontName']
LLBL      = list(itertools.chain(LTXXCA, ADN, LDS))
def JLBL(n, d): return (f'{d.join(LLBL)}{d}'*n).removesuffix(d)
def JSPR(n, d): return (f'{d.join(LTXX)}{d}'*n).removesuffix(d)
########################################################################################################################################################################################################
LBL                   = pygtxt.Label
SPR                   = pygsprt.Sprite
RGB                   = cOd() if CODS else {}
TT, NN, II, KK        =  0,  1,  2,  3
C1,  C2               =  0,  1
CSR_MODES             = ['MELODY', 'CHORD', 'ARPG']
HARROWS, VARROWS      = ['LARROW', 'RARROW'], ['DARROW', 'UARROW']
MELODY, CHORD, ARPG   =  0, 1, 2
LARROW, RARROW, DARROW, UARROW =  0, 1, 0, 1
NORMAL_STYLE, SELECT_STYLE, CURRENT_STYLE, COPY_STYLE = 0, 1, 2, 3
########################################################################################################################################################################################################
FIN     = [1, 1, 1, 2, 1]
FNTP    = [5, 4, 3, 3, 3]
#           0        1        2        3        4        5        6        7        8        9        10      11       12       13       14       15       16
JTEXTS  = ['Page',  'Line',  'Sect',  'Colm',  'Tabl',  'Note',  'IKey',  'Kord',  'RowL',  'QClm',  'HCrs',  'View',  'ZClm',  'UNum',  'ANam',  'DCpo',  'TNIK']
JTEXTS2 = ['Pag',   'Lin',   'Sct',   'Clm',   'Tabl',  'Note',  'IKey',  'Kord',  'RowL',  'QClm',  'HCrs',  'View',  'ZClm',  'UNum',  'ANam',  'DCpo',  'TNIK']
jTEXTS  = ['pages', 'lines', 'sects', 'colms', 'tabls', 'notes', 'ikeys', 'Kords', 'rowls', 'qclms', 'hcsrs', 'views', 'zclms', 'unums', 'anams', 'dcpos', 'tniks']
JFMT    = [  1,       2,       2,       3,       4,       4,       4,       4,       2,       3,       1,       1,       2,       2,       2,       2,       4]
#JFMT   = [  2,       3,       3,       6,       6,       6,       6,       6,       3,       5,       1,       1,       3,       3,       3,       4,       7]
#          0   1   2   3   4   5   6   7    8    9   10   11   12   13   14   15   16   17
OPC     = [ 0, 15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165, 170, 195, 210, 225, 240, 255 ]
FONT_SCALE =  14/18  # 14pts/18pix
FONT_DPIS  = [ 72, 78, 84, 90, 96, 102, 108, 114, 120 ]
FONT_NAMES = [ 'Lucida Console', 'Times New Roman', 'Helvetica', 'Arial', 'Courier New', 'Century Gothic', 'Bookman Old Style', 'Antique Olive' ]
########################################################################################################################################################################################################
# Globals END

# Log and Main BGN
########################################################################################################################################################################################################
LOG_PATH = util.getFilePath(BASE_NAME, BASE_PATH, fdir=LOGS, fsfx=LOG)
CSV_PATH = util.getFilePath(BASE_NAME, BASE_PATH, fdir=CSVS, fsfx=CSV)
plogPath = util.getFilePath(BASE_NAME, BASE_PATH, fdir=LOGS, fsfx=LOGP)
pcsvPath = util.getFilePath(BASE_NAME, BASE_PATH, fdir=CSVS, fsfx=CSVP)
if LOG_PATH.exists():     util.copyFile(LOG_PATH, plogPath)
if CSV_PATH.exists():     util.copyFile(CSV_PATH, pcsvPath)
with open(str(LOG_PATH), 'w', encoding='utf-8') as LOG_FILE, open(str(CSV_PATH), 'w', encoding='utf-8') as CSV_FILE:
    util.init(LOG_FILE, CSV_FILE, 0)
    slog(sys.argv[0],   p=0,           f=2)
    slog(f'argv={fmtl(sys.argv[1:])}', f=2)
    # 0   1    2    3    4    5    6    7    8    9   10   11   12   13   14   15   16   17   18
    FSH, PNK, RED, RST, PCH, ORG, YLW, LIM, GRN, TRQ, CYA, IND, BLU, VLT, GRY, CL1, CL2, CL3, CL4 = initRGB()
    def main():
        slog(f'{CSV_PATH=}',  f=2)   ;   slog(f'{CSV_FILE.name=}', f=2)
        slog(f'{LOG_PATH=}',  f=2)   ;   slog(f'{LOG_FILE.name=}', f=2)
        tabs = Tabs()                ;   snlfp    =    tabs.seqNumLogPath
        slog(f'{str(tabs)=}', f=2)   ;   slog(f'{tabs=}', f=2)
        ret = pyglet.app.run()       ;   msg      =    'Close & Copy'
        slog(f'pyglet.app.run(): {ret=}')
        slog(f'{msg} {LOG_FILE.name} to {snlfp}', ff=1)
        util.copyFile(LOG_PATH,          snlfp)
        glfp = util.getFilePath(tabs.LOG_GFN, BASE_PATH, fdir=LOGS, fsfx=Z)    ;    tabs.makeSubDirs(glfp)
        slog(f'{msg} {LOG_FILE.name} to { glfp}', ff=1)
        util.copyFile(LOG_PATH,           glfp)
        LOG_FILE.flush()             ;    LOG_FILE.close()
        print('Thats all folks', flush=True)
    ########################################################################################################################################################################################################
    if __name__ == '__main__':
        main()
########################################################################################################################################################################################################
# Log and Main END
