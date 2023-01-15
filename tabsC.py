import glob, math, os, pathlib, sys
import operator, inspect, itertools
from itertools      import accumulate
from more_itertools import consume
CODS    = 0
if CODS: from collections import OrderedDict as cOd
import pyglet
import pyglet.sprite as pygsprt
import pyglet.text   as pygtxt
import pyglet.window.event as pygwine
import pyglet.window.key   as pygwink
import chord, util

########################################################################################################################################################################################################
class Tabs(pyglet.window.Window):
####################################################################################################################################################################################################
    def __init__(self):
        ARGS = util.parseCmdLine(file=LOG_FILE)
        dumpGlobals()
        self.log(f'STFILT:\n{util.fmtl(util.STFILT)}')
        self.log(f'BGN {__class__}')
        self.LOG_ID       = 0
        self.lfSeqPath    = self.getFilePath(seq=1, fdir='logs', fsfx='.log')
        self.snapWhy, self.snapType, self.snapReg, self.snapId = '?', '_', 0, 0
#        self.catPath      = str(BASE_PATH / 'cats' / BASE_NAME) + '.cat'
        self.catPath      = self.getFilePath(seq=1, fdir='cats', fsfx='.cat')
        self.log(f'catPath={self.catPath}')
        self.settingN     = 0     ;   self.setNvals  = []    ;   self.setNtxt = ''
        self.shiftingTabs = 0     ;   self.shiftSign = 1
        self.inserting    = 0     ;   self.insertStr = ''
        self.jumping      = 0     ;   self.jumpStr   = ''    ;   self.jumpAbs = 0
        self.swapping     = 0     ;   self.swapSrc   = ''    ;   self.swapTrg = ''
        self.cc           = 0     ;   self.nvis      = 0
        self.allSelected  = 0
        self.resyncData   = 0
        self.newC, self.updC = 0, 0
        self.hArrow, self.vArrow,  self.csrMode           = RIGHT, UP, CHORD   ;   self.dumpCursorArrows('init()')
        self.tblank, self.tblanki, self.cursor, self.data = None, None, None, []
        self.J1,  self.J2 = [], []  ;  self.j1s, self.j2s = [], []
        self.ki           = []
        self.kbk,    self.symb,   self.mods,   self.symbStr,    self.modsStr = 0, 0, 0, '', ''
        self.A_LEFT    = 0  ;  self.A_CENTER    = 1  ;  self.A_RIGHT      = 0
        self.X_LEFT    = 0  ;  self.X_CENTER    = 1  ;  self.X_RIGHT      = 0
        self.Y_TOP     = 0  ;  self.Y_CENTER    = 1  ;  self.Y_BOTTOM     = 0  ;  self.Y_BASELINE = 0  ;  self.RESIZE_FONTS = 1
        self.AUTO_SAVE = 0  ;  self.CAT         = 0  ;  self.CHECKERED    = 0  ;  self.EVENT_LOG  = 0  ;  self.FULL_SCREEN  = 0  ;  self.LONG_TXT = 0
        self.GEN_DATA  = 0  ;  self.MULTI_LINE  = 1  ;  self.ORDER_GROUP  = 1  ;  self.RD_STDOUT  = 0  ;  self.RESIZE       = 1  ;  self.VARROW   = 1
        self.SNAPS     = 1  ;  self.SPRITES     = 0  ;  self.SUBPIX       = 1  ;  self.TEST       = 1  ;  self.VRBY         = 0  ;  self.TIDS     = 0
        self.VIEWS     = 0  ;  self.TRANSPOSE_A = 1  ;  self.DBG_TAB_TEXT = 0  ;  self.BGC        = 0  ;  self.FRET_BOARD   = 0  ;  self.STRETCH  = 0
        self.LL        = 0
        self.SS        = set() if 0 else {0, 1, 2, 3}
        self.ZZ        = set() if 1 else {0} #, 1}
        self.idmap     = cOd() if CODS else {}  ;  self.log(f'{CODS=} {type(self.idmap)=}')
        self.p0x, self.p0y, self.p0w, self.p0h, self.p0sx, self.p0sy = 0, 0, 0, 0, 0, 0
        nt             = 6
        self.n         = [2, 2, 50, nt]
        self.i         = [1, 1,  1, 1]
        self.DATA_FILE_NAME = ''
        self.log(f'argMap={util.fmtm(ARGS)}')
        if 'f' in ARGS and len(ARGS['f'])  > 0: self.DATA_FILE_NAME = ARGS['f'][0]
        if 'n' in ARGS and len(ARGS['n'])  > 0: self.n     = [ int(ARGS['n'][i]) for i in range(len(ARGS['n'])) ]
        if 'i' in ARGS and len(ARGS['i'])  > 0: self.i     = [ int(ARGS['i'][i]) for i in range(len(ARGS['i'])) ]
        if 'a' in ARGS and len(ARGS['a']) == 0: self.AUTO_SAVE      =  1
        if 'b' in ARGS and len(ARGS['b']) == 0: self.FRET_BOARD     =  1
        if 'B' in ARGS and len(ARGS['B']) == 0: self.BGC            =  1
        if 'c' in ARGS and len(ARGS['c']) == 0: self.CAT            =  1
        if 'C' in ARGS and len(ARGS['C']) == 0: self.CHECKERED      =  1
        if 'd' in ARGS and len(ARGS['d']) == 0: self.DBG_TAB_TEXT   =  1
        if 'e' in ARGS and len(ARGS['e']) == 0: self.EVENT_LOG      =  1
        if 'F' in ARGS and len(ARGS['F']) == 0: self.FULL_SCREEN    =  1
        if 'G' in ARGS and len(ARGS['G']) == 0: self.GEN_DATA       =  1
        if 'g' in ARGS and len(ARGS['g']) == 0: self.ORDER_GROUP    =  1
        if 'M' in ARGS and len(ARGS['M']) == 0: self.MULTI_LINE     =  1
        if 'R' in ARGS and len(ARGS['R']) == 0: self.RESIZE         = 0
        if 'p' in ARGS and len(ARGS['p']) == 0: self.SNAPS          =  1
        if 'x' in ARGS and len(ARGS['x']) == 0: self.SUBPIX         =  1
        if 's' in ARGS and len(ARGS['s']) == 0: self.SPRITES        =  1
        if 't' in ARGS and len(ARGS['t']) == 0: self.TEST           =  1
        if 'T' in ARGS and len(ARGS['T']) == 0: self.LONG_TXT       =  1
        if 'V' in ARGS and len(ARGS['V']) == 0: self.VIEWS          =  1
        if 'r' in ARGS and len(ARGS['r']) == 0: self.RD_STDOUT      =  1
        if 'u' in ARGS and len(ARGS['u']) == 0: self.TRANSPOSE_A    =  1
        if 'L' in ARGS and len(ARGS['L']) == 0: self.LL     =  1
        if 'S' in ARGS and len(ARGS['S']) >= 0: self.SS     = { int(ARGS['S'][i]) for i in range(len(ARGS['S'])) }
        if 'Z' in ARGS and len(ARGS['Z']) >= 0: self.ZZ     = { int(ARGS['Z'][i]) for i in range(len(ARGS['Z'])) }
        if 'A' in ARGS: l = len(ARGS['A'])   ;  self.VARROW =  1 if l == 0 else int(ARGS['A'][0]) if l == 1 else 0
        if 'v' in ARGS: l = len(ARGS['v'])   ;  self.VRBY   =  1 if l == 0 else int(ARGS['v'][0]) if l == 1 else 0
        self.n.insert(S, self.ssl())
        self.i.insert(S, 1)
        self.dumpArgs()
        self.vArrow = UP if self.VARROW == 1 else DOWN
        self.fontStyle = NORMAL_STYLE
        self.k         = {}
        self.sAlias = 'GUITAR_6_STD'
        self.sobj = util.Strings(LOG_FILE, self.sAlias)
        self.cobj = chord.Chord( LOG_FILE, self.sobj)
        util.Note.setType(util.Note.FLAT)  ;  self.log(f'{util.Note.TYPE=}')
        self.log(f'Frequency Info')
        self.dumpFreqsHdr()  ;  self.dumpFreqs()  ;  self.dumpFreqs(ref=432)
        self._initDataPath()
        if self.CAT: self.cobj.dumpOMAP(str(self.catPath))
        self._initWindowA()
        self.log(f'WxH={self.fmtWH()}')
        super().__init__(screen=self.screens[0], fullscreen=self.FULL_SCREEN, resizable=True, visible=False)
        self.log(f'WxH={self.fmtWH()}')
        self._initWindowB()
        self.log(f'WxH={self.fmtWH()}')
        self.a  = 'left' if self.A_LEFT else 'center' if self.A_CENTER else 'right'  if self.A_RIGHT  else '???'
        self.ax = 'left' if self.X_LEFT else 'center' if self.X_CENTER else 'right'  if self.X_RIGHT  else '???'
        self.ay = 'top'  if self.Y_TOP  else 'center' if self.Y_CENTER else 'bottom' if self.Y_BOTTOM else 'baseline' if self.Y_BASELINE else '???'
        self.dumpAxy()    ;   self.dumpAXY()
        self._reinit()
        self.log(f'END {__class__}')
        self.log(f'{util.INIT}', pfx=0)
    ####################################################################################################################################################################################################
    def dumpArgs(self):
        self.log(f'[f] {self.DATA_FILE_NAME=}')
        self.log(f'[n]               {self.fmtn()}')
        self.log(f'[i]               {self.fmti()}')
        self.log(f'[a]      {self.AUTO_SAVE=}')
        self.log(f'[b]     {self.FRET_BOARD=}')
        self.log(f'[B]            {self.BGC=}')
        self.log(f'[c]            {self.CAT=}')
        self.log(f'[C]      {self.CHECKERED=}')
        self.log(f'[d]   {self.DBG_TAB_TEXT=}')
        self.log(f'[e]      {self.EVENT_LOG=}')
        self.log(f'[F]    {self.FULL_SCREEN=}')
        self.log(f'[G]       {self.GEN_DATA=}')
        self.log(f'[M]     {self.MULTI_LINE=}')
        self.log(f'[g]    {self.ORDER_GROUP=}')
        self.log(f'[p]          {self.SNAPS=}')
        self.log(f'[R]         {self.RESIZE=}')
        self.log(f'[x]         {self.SUBPIX=}')
        self.log(f'[s]        {self.SPRITES=}')
        self.log(f'[t]           {self.TEST=}')
        self.log(f'[T]       {self.LONG_TXT=}')
        self.log(f'[v]           {self.VRBY=}')
        self.log(f'[V]          {self.VIEWS=}')
        self.log(f'[r]      {self.RD_STDOUT=}')
        self.log(f'[u]    {self.TRANSPOSE_A=}')
        self.log(f'[A]         {self.VARROW=}')
        self.log(f'[L]             {self.LL=}')
        self.log(f'[S]             .SS={util.fmtl(self.SS)}')
        self.log(f'[Z]             .ZZ={util.fmtl(self.ZZ)}')
    ####################################################################################################################################################################################################
    def _reinit(self):
        self.log('BGN')
        self.tpb, self.tpp, self.tpl, self.tps, self.tpc = self.ntp(dbg=1, dbg2=1)
        self.visib = []
        self.pages, self.lines, self.sects, self.colms = [], [], [], []  ;  self.A = [self.pages, self.lines, self.sects, self.colms]
        self.tabls, self.notes, self.ikeys, self.kords = [], [], [], []  ;  self.B = [self.tabls, self.notes, self.ikeys, self.kords]
        self.rowLs, self.qclms, self.hcurs, self.views = [], [], [], []  ;  self.C = [self.rowLs, self.qclms, self.hcurs, self.views]
        self.zclms, self.snums, self.snams, self.capos = [], [], [], []  ;  self.D = [self.zclms, self.snums, self.snams, self.capos]
        self.E    = [*self.A, *self.B, *self.C, *self.D]
        self.log(f'E={util.fmtl(self.E, d1=" [", d2="] ")}')
        self.resetJ('_reinit')
        self.data = []
        self.cursor,  self.caret, self.cc                                = None, None, 0
        self.kbk,     self.symb,  self.mods,  self.symbStr, self.modsStr = 0, 0, 0, '', ''
        self.ki   = [ 0 for _ in range(len(self.E)) ]   ;   self.log(f'{util.fmtl(self.ki)}')
        self.tblanki, self.tblanks  = 1, [' ', '-']                ;     self.tblank = self.tblanks[self.tblanki]
        self.tblankCol              = self.tblank * self.n[T]      ;  self.tblankRow = self.tblank * (self.n[C] + self.zzl())
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
        if self.SNAPS: self.regSnap('init', 'INIT')
    ####################################################################################################################################################################################################
    def _initColors(self):
        k = self.k  ;  a = not self.SPRITES and not self.BGC  ;  b = not self.SPRITES and self.BGC  ;  c =   self.SPRITES and not self.BGC  ;  d = self.SPRITES and self.BGC  ;  i = self.initk
        j = P  ;  k[j] = i(j, BLU,  0, 17, RED, 17, 17) if a else i(j, GRY,  0,  0, GRY,  0,  0) if b else i(j, GRY,  0,  0, GRY,  0,  0) if c else i(j, GRY,  0,  0, GRY,  0,  0) if d else None
        j = L  ;  k[j] = i(j, BLU,  0, 17, RED, 17, 17) if a else i(j, GRY,  0,  0, GRY,  0,  0) if b else i(j, GRY,  0,  0, GRY,  0,  0) if c else i(j, GRY,  0,  0, GRY,  0,  0) if d else None
        j = S  ;  k[j] = i(j, BLU,  0, 17, RED, 17, 17) if a else i(j, GRY,  0,  0, GRY,  0,  0) if b else i(j, GRY,  0,  0, GRY,  0,  0) if c else i(j, GRY,  0,  0, GRY,  0,  0) if d else None
        j = C  ;  k[j] = i(j, BLU,  0, 17, RED, 17, 17) if a else i(j, GRY,  0,  0, GRY,  0,  0) if b else i(j, GRY,  0,  0, GRY,  0,  0) if c else i(j, GRY,  0,  0, GRY,  0,  0) if d else None
        j = T  ;  k[j] = i(j, ORN,  0, 17, ORN, 17, 17) if a else i(j, ORN,  0, 17, ORN, 17, 17) if b else i(j, ORN,  0, 17, ORN, 17, 17) if c else i(j, ORN,  0, 17, ORN, 17, 17) if d else None
        j = N  ;  k[j] = i(j, GRN,  0, 17, GRN, 17, 17) if a else i(j, GRN,  0, 17, GRN, 17, 17) if b else i(j, GRN,  0, 17, GRN, 17, 17) if c else i(j, GRN,  0, 17, GRN, 17, 17) if d else None
        j = I  ;  k[j] = i(j, YLW,  0, 17, YLW, 17, 17) if a else i(j, YLW,  0, 17, YLW, 17, 17) if b else i(j, YLW,  0, 17, YLW, 17, 17) if c else i(j, YLW,  0, 17, YLW, 17, 17) if d else None
        j = K  ;  k[j] = i(j, IND,  0, 17, IND, 17, 17) if a else i(j, IND,  0, 17, IND, 17, 17) if b else i(j, IND,  0, 17, IND, 17, 17) if c else i(j, IND,  0, 17, IND, 17, 17) if d else None
        j = R  ;  k[j] = i(j, BLU,  0, 17, BLU, 17, 17) if a else i(j, BLU,  0, 17, BLU, 17, 17) if b else i(j, BLU,  0,  4, BLU, 17,  4) if c else i(j, BLU,  0, 17, BLU, 17, 17) if d else None
        j = Q  ;  k[j] = i(j, CYA,  0, 17, CYA, 17, 17) if a else i(j, CYA,  0,  0, CYA, 17, 17) if b else i(j, CYA,  0, 17, CYA, 17, 17) if c else i(j, CYA,  0,  0, CYA, 17, 17) if d else None
        j = H  ;  k[j] = i(j, YLW, 17, 11, YLW, 17, 10) if a else i(j, PNK, 17, 10, PNK, 17, 17) if b else i(j, PNK, 17, 17, PNK, 17, 17) if c else i(j, PNK, 17, 17, PNK, 17, 17) if d else None
        j = Z  ;  k[j] = i(j, VLT,  0,  0, VLT, 17, 17) if a else i(j, VLT,  0,  0, VLT, 17, 17) if b else i(j, VLT,  0,  0, VLT, 17, 17) if c else i(j, VLT,  0,  0, VLT, 17, 17) if d else None
        j = U  ;  k[j] = i(j, PNK,  0,  0, PNK, 17, 17) if a else i(j, PNK,  0,  0, PNK, 17, 17) if b else i(j, PNK,  0,  0, PNK, 17, 17) if c else i(j, PNK,  0,  0, PNK, 17, 17) if d else None
        j = A  ;  k[j] = i(j, BLU,  0,  0, BLU, 17, 17) if a else i(j, BLU,  0,  0, BLU, 17, 17) if b else i(j, BLU,  0,  0, BLU, 17, 17) if c else i(j, BLU,  0,  0, BLU, 17, 17) if d else None
        j = D  ;  k[j] = i(j, FSH,  0,  0, FSH, 17, 17) if a else i(j, FSH,  0,  0, FSH, 17, 17) if b else i(j, FSH,  0,  0, FSH, 17, 17) if c else i(j, FSH,  0,  0, FSH, 17, 17) if d else None

    def initk(self, j, key0, rgb0, opc0, key1, rgb1, opc1):
        self.log(f'{j:2}  {JTEXTS[j]:4}  [{key0} {rgb0:2} {opc0:2}] [ {key1} {rgb1:2} {opc1:2}] {util.fmtl(RGB[key0][rgb0][opc0], w="3")} {util.fmtl(RGB[key1][rgb1][opc1], w="3")}', pfx=0)
        return [RGB[key0][rgb0][opc0], RGB[key1][rgb1][opc1]]
    ####################################################################################################################################################################################################
    def _initData(self, dbg=1):
        self._initDataPath()
        if self.GEN_DATA: self.genDataFile(self.dataPath1)
        self.readDataFile(self.dataPath1)
        util.copyFile    (self.dataPath1, self.dataPath2, file=LOG_FILE)
#        self.data = self.A_transposeData(dump=dbg) if self.TRANSPOSE_A else self.transposeDataDump() if dbg else self.OLD_transposeData()
        if self.TRANSPOSE_A:    self.data = self.A_transposeData(dump=dbg)
        else:               self.transposeDataDump() if dbg else self.OLD_transposeData()
        old = self.fmtn('')
        self.n[P] = self.dl()[0]
        self.log(f'{self.fmtdl()}')
        self.log(f'Updating n[P] {old=} {self.fmtn()}')
        self.tpb, self.tpp, self.tpl, self.tps, self.tpc = self.ntp(dbg=1, dbg2=1)

    def _initDataPath(self):
        dataDir   = 'data'  ;  dataSfx = '.dat'  ;  dataPfx = f'.{self.n[C]}'
        baseName  = self.DATA_FILE_NAME if self.DATA_FILE_NAME else BASE_NAME + dataPfx + dataSfx
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

    def _initTniks(self):
        self.ssl()      ;   self.smap = {}
        self.dumpAxy()  ;   self.dumpAXY()
        [ self.visib.append(list()) for _ in range(len(JTEXTS)) ]
        self.createTniks()
        if self.TEST:     self.test()  ;  self.test2()
    ####################################################################################################################################################################################################
    def _initWindowA(self, dbg=1):
        display      = pyglet.canvas.get_display()
        if dbg: self.log(f'BGN {self.fmtWH()}')  ;  self.log(f'{display=}')
        self.screens = display.get_screens()     ;  s = self.screens
        if dbg:
            for i in range(len(s)): self.log(f'screens[{i}] x={s[i].x} y={s[i].y:5} {self.fmtWH(s[i].width, s[i].height)}')
            self.log(f'END {self.fmtWH()}')

    def _initWindowB(self, dbg=1):
        if dbg: self.log(f'BGN {self.fmtWH()}')
        self.batch = pyglet.graphics.Batch()
        self._initGroups()
        self.set_visible()
        self.log(f'get_size={self.get_size()}')
        if self.EVENT_LOG:
            self.eventLogger = pygwine.WindowEventLogger()
            self.push_handlers(self.eventLogger)
            self.keyboard = pygwine.key.KeyStateHandler()
            self.push_handlers(self.keyboard)
        if dbg: self.log(f'END {self.fmtWH()}')
    ####################################################################################################################################################################################################
    def _initGroups(self):
        hdrA    = [P, L, S, C,  T, N, I, K,  R, Q, H, V,  Z, U, A, D]
        hdrB    = ' '.join([ f'{t[0]:2}' for t in JTEXTS ])
        self.gn = [1, 2, 3, 4,  5, 5, 5, 5,  5, 5, 6, 0,  5, 5, 5, 5]  ;  self.g = []
        self.log(f'{util.fmtl(hdrA, w="2")}')  ;  self.log(f'  {hdrB}')  ;  self.log(f'{util.fmtl(self.gn, w="2")}')
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
    def test(self, j=10):
        self.log(f'{self.ntsl()=}')
        hdrA = '      cc [  tpb  tpp tpl tps tpc] [p l s  c t]'
        hdrB = ' cn   cc [  tpb  tpp tpl tps tpc] [p l s  c t]'
        hdrC = '  cc  cn [  tpb  tpp tpl tps tpc] [p l s  c t]'
        np, nl, ns, nc, nt = self.i #  ;   p, l, c = 0, 0, 0
        self.dumpTniksPfx(f'BGN {j=} test', r=0)
        self.log(hdrB)
        for p in range(np):
            for l in range(nl):
                for s in range(ns):
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
    
    def test2(self):
        c  = util.KeySig(None, 0, 0)
        a  = util.KeySig('A')
        fs = util.KeySig('F#')
        eb = util.KeySig('Eb')
        self.test2Log(c)
        self.test2Log(a)
        self.test2Log(eb)
        self.test2Log(fs)
        ds = util.KeySig('D#')
        self.test2Log(ds)
        bs = util.KeySig('B#')
        self.test2Log(bs)

    def test2Log(self, k):
        self.log(f'{k.__repr__()}')
        self.log(f'{k.__str__()} {k.name=} {k.nflats=} {k.nshrps=}')
        b = f' {k.NFLATS[k.name]} FLATS {k.FLATS[ k.name]}' if k.name in k.NFLATS and len(k.NFLATS) else ''
        s = f' {k.NSHRPS[k.name]} SHRPS {k.SHRPS[ k.name]}' if k.name in k.NSHRPS and len(k.NSHRPS) else ''
        self.log(f'{k.name}:{b}{s}')
    def OLD__test2Log(self, k):
        self.log(f'{k=} {k.name=} {k.nflats=} {k.nshrps=}')
        b = f' {k.NFLATS[k.name]} FLATS {k.FLATS[ k.name]}' if k.name in k.NFLATS and len(k.NFLATS) else ''
        s = f' {k.NSHRPS[k.name]} SHRPS {k.SHRPS[ k.name]}' if k.name in k.NSHRPS and len(k.NSHRPS) else ''
        self.log(f'{k.name}:{b}{s}')
    ####################################################################################################################################################################################################
    def lenA(self):                   return [ len(_) for _ in self.A ]
    def lenB(self):                   return [ len(_) for _ in self.B ]
    def lenC(self):                   return [ len(_) for _ in self.C ]
    def lenD(self):                   return [ len(_) for _ in self.D ]
    def lenE(self):                   return [ len(_) for _ in self.E ]
    def j(   self):                   return [ i-1 if i else 0 for    i in           self.i ]
    def j2(  self):                   return [ i-1 if i else 0 for j, i in enumerate(self.i)  if j != S ]
    def j2g( self, j):                return self.g[ self.gn[j] ]
    def resetJ(self, why='', dbg=1): self.J1 = [ 0 for _ in range(len(self.E)+1) ]  ;   self.J2 = [ 0 for _ in range(len(self.E)+1) ]  ;  self.nvis = 0  ;  self.dumpJs(why) if dbg else None
    def setJ(self, j, n, v=None):
        v = self.isV() if v is None else v    ;   self.J1[j] = n  ;  self.J2[j] += 1  ;  self.J1[-1] += 1  ;  self.J2[-1] += 1
        self.nvis += 1 if v else 0            ;   self.visib[j].append(v)
    def setJdump(self, j, n, v=None, why=''): i = self.J2[j]  ;  self.setJ(j, n, v)  ;  self.dumpTnik(self.E[j][i], j, why)  ;  return j
    ####################################################################################################################################################################################################
    def ssl(self, dbg=0):  l = len(self.SS)   ;   self.log(f'{self.fmtn()} SS={util.fmtl(self.ss2sl())} {l=}') if dbg else None   ;   return l   # return 0-4
    def zzl(self, dbg=0):  l = len(self.ZZ)   ;   self.log(f'{self.fmtn()} ZZ={util.fmtl(self.zz2sl())} {l=}') if dbg else None   ;   return l   # return 0-2
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
    def fplc(  self, p=None, l=None,         c=None):         j = self.j()  ;  p = j[P] if p is None else p  ;  l = j[L] if l is None else l  ;  c = j[C] if c is None else c  ;                                                                    return f'[{p+1} {l+1}   {c+1:2}]'
    def fplct( self, p=None, l=None,         c=None, t=None): j = self.j()  ;  p = j[P] if p is None else p  ;  l = j[L] if l is None else l  ;  c = j[C] if c is None else c  ;  t = j[T] if t is None else t  ;                                   return f'[{p+1} {l+1}   {c+1:2} {t+1}]'
    def fplsc( self, p=None, l=None, s=None, c=None):         j = self.j()  ;  p = j[P] if p is None else p  ;  l = j[L] if l is None else l  ;  s = j[S] if s is None else s  ;  c = j[C] if c is None else c  ;                                   return f'[{p+1} {l+1} {s+1} {c+1:2}]'
    def fplsct(self, p=None, l=None, s=None, c=None, t=None): j = self.j()  ;  p = j[P] if p is None else p  ;  l = j[L] if l is None else l  ;  s = j[S] if s is None else s  ;  c = j[C] if c is None else c  ;  t = j[T] if t is None else t  ;  return f'[{p+1} {l+1} {s+1} {c+1:2} {t+1}]'
    ####################################################################################################################################################################################################
    def jsum(  self, a=1):          return [ _ + a if self.J2[j] and j < len(self.J1)-1 else _ if j == len(self.J1)-1 else 0 for j, _ in enumerate(self.J1) ]
    def fmtdl( self, data=None):    return f'{util.fmtl(self.dl(data))}'
    def fmtdt( self, data=None):    return f"[{' '.join([ t.replace('class ', '') for t in self.dtA(data) ])}]"
    def fmtJ1( self, w=None, d=0):  w = w if w is not None else JFMT  ;  d1 = "" if not d else "["  ;  d2 ="" if not d else "]"  ;  return     f'{util.fmtl(self.jsum(), w=w, d1=d1, d2="")} {self.fnvis()}{d2}'
    def fmtJ2( self, w=None, d=0):  w = w if w is not None else JFMT  ;  d1 = "" if not d else "["  ;  d2 ="" if not d else "]"  ;  return     f'{util.fmtl(self.J2,     w=w, d1=d1, d2="")} {self.fnvis()}{d2}'
    def fmtLE( self, w=None, d=1):  w = w if w is not None else JFMT  ;  d1 = "" if not d else "["  ;  d2 ="" if not d else "]"  ;  return f'{d1}{util.fmtl(self.lenE(), w=w, d1="", d2="")} {sum(self.lenE()[:-1]):4} {self.fnvis()}{d2}'
    ####################################################################################################################################################################################################
    def fmtPos(self):                         cc = self.plct2cc(*self.j2())  ;  cn = self.cc2cn(cc)  ;  return f'{util.fmtl(self.i, w=FIN)} {cc+1:3} {cn+1:2}]'
    def fmtn(  self, pfx='n=', n=None):       n = n if n is not None else self.n   ;   return f'{pfx}{util.fmtl(n)}'
    def fmti(  self, pfx='i='):               return f'{pfx}{util.fmtl(self.i)}'
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
    def fmtJText(j, why=''):   jtxt = f'{JTEXTS[j]}' if 0 <= j < len(JTEXTS) else f'?{j:2}?'   ;   return f'{j=} {why} {jtxt}'
    ####################################################################################################################################################################################################
    @staticmethod
    def ffont(t):    return f'{t.dpi:3} {t.bold:1} {t.italic:1} {t.font_name}'
    @staticmethod
    def ftcolor(t, d=1): (d1, d2) = ("[", "]") if d else ("", "")  ;  k = ' '.join([ f'{k:3}' for k in t.color[:3] ])  ;  k += f' {t.opacity:3}'  ;  return f'{d1}{k}{d2}'
    @staticmethod
    def ftfntsiz(t): return F'{t.font_size:3.0f}'
    @staticmethod
    def ftMxy(t):    return f'{t.scale:5.3f} {t.scale_x:5.3f} {t.scale_y:5.3f}'
    @staticmethod
    def ftvis(t):    return 'V' if t.visible else 'I'
    @staticmethod
    def ftxywh(t):   return Tabs.fxywh(t.x, t.y, t.width, t.height)
    @staticmethod
    def fiax(t):     return f'{t.image.anchor_x:4}'
    @staticmethod
    def fiay(t):     return f'{t.image.anchor_y:4}'
    @staticmethod
    def fgrp(t):     return f'{t.group}'
    @staticmethod
    def fgrpp(t):    return f'{t.group.parent}'
    ####################################################################################################################################################################################################
    @staticmethod
    def fxywh(x, y, w, h): return f'{x:7.2f} {y:7.2f} {w:7.2f} {h:7.2f}'
    ####################################################################################################################################################################################################
    def fmtAxy(self):    return f'{self.a} {self.ax} {self.ay}'
    def fAxy(self):      return f'{self.ftAx(self.a)} {self.ftAx(self.ax)} {self.ftAy(self.ay)}'
    @staticmethod
    def fcva(t):         a = t.content_valign   ;    return 'T' if a == 'top'    else 'C' if a == 'center' else 'B' if a == 'bottom' else '???'
    @staticmethod
    def ftAy(a):         return 'N' if a == 'baseline' else 'T' if a == 'top'    else 'C' if a == 'center' else 'B' if a == 'bottom' else '???'
    @staticmethod
    def ftAx(a):         return 'L' if a == 'left'     else 'C' if a == 'center' else 'R' if a == 'right'  else '???'
    def fss2sl(self):    s2s = self.ss2sl()  ;  ss = ' '.join([str(s2s[i]) if i < len(s2s) else ' ' for i in range(4)])  ;  return f'({ss:7})'
    def fzz2sl(self):    z2z = self.zz2sl()  ;  zz = ' '.join([str(z2z[i]) if i < len(z2z) else ' ' for i in range(2)])  ;  return f'({zz:3})'
    ####################################################################################################################################################################################################
    def dumpAxy(self):   self.log(f'{self.a=} {self.ax=} {self.ay=}')
    def dumpAXY(self):
        self.log(f'{self.A_LEFT=} {self.A_CENTER=} {self.A_RIGHT=}')
        self.log(f'{self.X_LEFT=} {self.X_CENTER=} {self.X_RIGHT=}')
        self.log(f'{self.Y_TOP=}  {self.Y_CENTER=} {self.Y_BOTTOM=} {self.Y_BASELINE=}')
    def dumpWxHp0(self): self.log(f'{self.fmtWHP0()}')
    def dumpDataSlice(self, p, l, c, cc):
        for t in range(self.n[T]):
            ikeys = self.ikeys[cc+t].text if self.ikeys and len(self.ikeys) > cc+t else ''
            kords = self.kords[cc+t].text if self.kords and len(self.kords) > cc+t else ''
            self.log(f'{self.data[p][l][c]} [{cc+t}] {self.tabls[cc+t].text:2} {self.notes[cc+t].text:2} {ikeys:2} {kords:2}')
#    @staticmethod
#    def dumpObjs(objs, name, why=''):            [ Tabs.dumpObj(o, name, why) for o in objs ]
#    @staticmethod
#    def dumpObj( obj,  name, why='', file=None): util.slog(f'{why} {name} ObjId {id(obj):x} {type(obj)}', file=file)
    def dumpFreqsHdr(self):
        self.log(f'index{util.fmtl([ i for i in range(util.Note.MAX_INDEX) ], w="5")}', pfx=0)
        self.log(f'sharp{util.fmtl(list(util.Note.FNAMES), w="5")}', pfx=0)
        self.log(f' flat{util.fmtl(list(util.Note.SNAMES), w="5")}', pfx=0)
    def dumpFreqs(self, ref=440):
        f = util.FREQS if ref==440 else util.FREQS2
        self.log(f'{ref}A {util.fmtl(f, w="5.0f")}', pfx=0)
    def dumpJs(  self, why, w=None, d=1): b = B*12 if self.TIDS else ''  ;  self.log(f'{b}J1{self.fmtJ1(w, d)} {why}')   ;   self.log(f'{b}J2{self.fmtJ2(w, d)} {why}')   ;   self.log(f'{b}LE{self.fmtLE(w)} {why}')
    def dumpGeom(self, why='', why2=''):  b = B*12 if self.TIDS else ''  ;  self.log(f'{b}{why:3}[{self.fmtWH()}{self.fmtD()}{self.fmtI()} {self.fss2sl()} {self.LL} {self.fzz2sl()} {len(self.idmap):4} {self.fnvis()}] {why2}')
    def dumpSmap(self, why, pos=0):       self.log(f'{why} smap={util.fmtm(self.smap)}', pos=pos)
    ####################################################################################################################################################################################################
    def dumpBlanks(self): self.dmpBlnkHdr()  ;  self.log(f'{self.fmtBlnkCol()}', pfx=0)  ;  self.log(f'{self.fmtBlnkRow()}', pfx=0)
    def dmpBlnkHdr(self): self.log(f'{len(self.tblankCol)=} {len(self.tblankRow)=}')
    def fmtBlnkCol(self): return f'{self.tblankCol}'
    def fmtBlnkRow(self): return f'{self.tblankRow}'
    ####################################################################################################################################################################################################
    def ntp(self, dbg=0, dbg2=0):
        n = list(self.n)     ;   self.log(f'{B*9}         n={self.fmtn("", n)}') if dbg2 else None
        n.reverse()          ;   self.log(f'{B*9}       Rev={self.fmtn("", n)}') if dbg2 else None
        n = self.accProd(n)  ;   self.log(f'{B*9}   nRevPrd={util.fmtl(n)}')     if dbg2 else None
        n.reverse()          ;   self.log(f'{B*9}nRevPrdRev={util.fmtl(n)}')     if dbg2 else None
        self.log(f'tpb tpp tpl tps tpc={util.fmtl(n)}') if dbg else None
        return n
    def fntp(  self, dbg=0, dbg2=0):   return util.fmtl(self.ntp(dbg=dbg, dbg2=dbg2), w=FNTP)
    ####################################################################################################################################################################################################
    @staticmethod
    def accProd(n):              return list(accumulate(n, operator.mul))
    ####################################################################################################################################################################################################
    def dumpStruct(self, why='', dbg=1, dbg2=0):
        self.log(f'{self.fmtn()} BGN ntp={self.fntp(dbg=dbg, dbg2=dbg2)} {self.fmtI()}', pos=1)
        self.dumpFont(why)
        self.dumpVisible()
        self.dumpIdmKeys()
        self.dumpVisible2()
        if dbg:     self.dumpTniksA(f'{why}A')
        if dbg2:    self.dumpTniksB(f'{why}B')
        if dbg2:    self.dumpTniksC(f'{why}C')
        if dbg2:    self.dumpTniksD(f'{why}D')
        if dbg2:    self.cobj.dumpMlimap(f'MLim') if self.VRBY else None
        self.log(f'{self.fmtn()} END ntp={self.fntp(dbg=dbg, dbg2=dbg2)} {self.fmtI()}', pos=1)
    ####################################################################################################################################################################################################
    def autoSave(self, dt, why, dbg=1):
        if dbg: self.log(f'Every {dt:=7.4f} seconds, {why} {self.resyncData=}')
        if self.resyncData: self.saveDataFile(why, self.dataPath0)   ;  self.resyncData = 0
    ####################################################################################################################################################################################################
    def on_draw(self):
        pyglet.gl.glClearColor(0, 0, 0, 0) # (1, 1, 1, 1) # (R, G, B, A)
        self.clear()
        self.batch.draw()
        if self.SNAPS and self.snapReg:
            self.snapReg = 0  ;  self.snapshot()
            self.log(f'{self.snapWhy=} {self.snapType=} {self.snapId=}', pos=1)

    def on_resize(self, width, height, dbg=1):
        super().on_resize(width, height)
#        self.updC += 1   ;   why = f'Upd{self.updC}'
        if self.RESIZE: self.resizeTniks()
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
        self.dumpBlanks()
        self.data = [ [ [ self.tblankRow for _ in range(nr) ] for _ in range(nl) ] for _ in range(np) ]
        size = self.saveDataFile('Generated Data', path)
        self.log(f'{path} {size=} {len(self.data)=}')
        self.data = []
        return size
   ####################################################################################################################################################################################################
    def readDataFile(self, path, dbg=1):
        nl = self.n[L]   ;   nr = self.n[T]   ;   sp, sl, st, sr = 0, 0, 0, 0
        if dbg:                 self.log(f'BGN {self.fmtn()}')
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
        self.log(f'BGN {self.fmtD(data)} {why}')
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
        self.log(f'END {self.fmtD(Xdata)} {why}')
        return Xdata

    def A_transposeData(self, data=None, dump=0, dbg=1):
        data = self.dproxy(data)
        self.log(f'BGN {self.fmtD(data)} {dump=}')
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
        self.log(f'END {self.fmtD(Xdata)} {dump=}')
        return Xdata
    ####################################################################################################################################################################################################
    def dumpDataHorz(self, data=None, lc=1, ll=1, i=0):
        data = data or self.data
        self.log(f'BGN {self.fmtD(data)} {lc=} {ll=} {i=}')
        for p in range(len(data)):
#            if ll:  plt = f'{JTEXTS[P]} {p+1}'  ;  plab = f'{plt:{i+1}}'  ;  self.log(f'{B*i}{plab}', pfx=0)
            for l in range(len(data[p])):
                if ll:  llt = f'{JTEXTS[P]} {p+1}'  ;  llab = f'{llt:{i+1}} '  ;  self.log(f'{B*i}{llab}', pfx=0, end='')   ;   self.log(f'{JTEXTS[L]} {l+1}', pfx=0)
#                if ll:  llt = f'{JTEXTS[L]} {l+1}'  ;  llab = f'{llt:{i+1}}'  ;  self.log(f'{B*i}{llab}', pfx=0)
                if lc:  self.dumpDataLabels(data[p][l], i=i, sep=B)
                for r in range(len(data[p][l])):
                    self.log(f'{B*i}', pfx=0, end='')
                    for c in range(len(data[p][l][r])):
                        self.log(f'{data[p][l][r][c]}', pfx=0, end='')
                    self.log(pfx=0)
                self.log(pfx=0)
        self.log(f'END {self.fmtD(data)} {lc=} {ll=} {i=}')

    def dumpDataVert(self, data=None, lc=1, ll=1, i=0):
        data = data or self.data
        w = max(len(data[0][0][0]), len(JTEXTS[P]) + 2, len(JTEXTS[L]) + 2)   ;   txt = B * i + JTEXTS[C] + B if i >= 0 else JTEXTS[C]
        self.log(f'BGN {self.fmtD(data)} {lc=} {ll=} {i=} {w=} {txt=}')
        for p in range(len(data)):
            if ll: self.log(f'{JTEXTS[P]} {p+1}', pfx=0)  ;  self.log(f'{txt:{3}}', pfx=0, end='')  ;  txt2 = [ f'{JTEXTS[L]} {l+1}' for l in range(len(data[0])) ]  ;  self.log(f'{util.fmtl(txt2, w=w, d1="")}', pfx=0)
            for c in range(len(data[p][0])):
                pfx = f'{c+1:3} ' if i >= 0 and lc else ''   ;   self.log(f'{pfx}{B*i}', pfx=0, end='')
                for l in range(len(data[p])):
                    self.log(f'{data[p][l][c]}', pfx=0, end=B)
                self.log(pfx=0)
        self.log(f'END {self.fmtD(data)} {lc=} {ll=} {i=}')
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
        self.log(f'labelTextA={util.fmtl(self.labelTextA, w="2")}', pfx=0)
        self.log(f'labelTextB={util.fmtl(self.labelTextB, w="2")}', pfx=0)
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
        self.on_resize(self.width, self.height)
        self.dumpGeom('END', f'{msg} {msg2}')

    def toggleLLs(self, how, dbg=1):
        self.toggleLL()
        msg2 = f'{how} {self.LL=}'
        self.dumpGeom('BGN', f'     {msg2}')
        if dbg: self.log(f'    llText={util.fmtl(self.llText[1-self.zzl():])}')
        if self.LL and not self.rowLs: msg = 'ADD'    ;   self.addLLs( how)
        else:                          msg = 'HIDE'   ;   self.hideLLs(how)
        self.on_resize(self.width, self.height)
        self.dumpGeom('END', f'{msg} {msg2}')

    def toggleZZs(self, how, zz):
        ii = 0 if not zz else 2
        msg2 = f'{how} {zz=}'
        self.dumpGeom('BGN', f'     {msg2}')
        if   zz not in self.ZZ and not self.D[ii]: msg = 'ADD'    ;   self.addZZs(how, zz)
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
            self.setJdump(P, p, why=why2) # p
            for l in range(nl):
                self.setJdump(L, l, why=why2) # l
                for _, s in   enumerate(self.ss2sl()):
                    if s != ii:          self.setJdump(S, s, why=why2)
                    else:                self.hideTnik(self.sects,   p*nl + l,            S, dbg=dbg)
                    for c in range(nc):
                        if s != ii:      self.setJdump(C, c, why=why2)
                        else:            self.hideTnik(self.colms,   (p*nl + l)*nc + c,   C, dbg=dbg)
                        for t in range(nt):
                            tlist, j  =  self.tnikInfo(p, l, s, c)
                            if s != ii:  self.setJdump(j, t, why=why2)
                            else:        self.hideTnik(tlist, ((p*nl + l)*nc + c)*nt + t, j, dbg=dbg)
        if ii == TT:                     self.hideTnik(self.hcurs,                     0, H, dbg=dbg)
        self.dumpTniksSfx(why)
        self.toggleTT(ii)

    def hideLLs(self, how):
        msg = f'HIDE {how}'
        nr = len(self.rowLs)                    ;  nc = len(self.qclms)
        assert not (nc % nr), f'{nc=} {nr=}'    ;  nc = nc // nr  #  normalize
        self.dumpTniksPfx(msg)
        for r in range(nr):
            self.hideTnik(self.rowLs, r, R)
            for c in range(nc):
                self.hideTnik(self.qclms, c + r*nc, Q)
        self.dumpTniksSfx(msg)
    ####################################################################################################################################################################################################
    def NEW__addZZs(self, how, ii):
        why = f'ADD {how} {ii=}'      ;   why1, why2 = 'Ref1', 'Ref2'
        np, nl, ns, nc, nt = self.n   ;   zz = self.zz2sl() # call after toggleZ???
        n = self.toggleZZ(ii)
        self.dumpTniksPfx(why)
        for v, view in enumerate(self.views):
            self.dumpTnik(view, V, why=why1)
            self.splitH(view, n)
            self.dumpTnik(view, V, why=why2)
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
        self.resizeTniks(dbg=1)
        self.toggleZZ(ii)  # zz = self.zz2sl()   ;   nc += len(zz)
    def OLD__addZZs(self, how, ii, dbg=0):
        why = 'Add'   ;   self.log(f'{why} {ii=} {how}') if dbg else None # ;  why1 = f'{why} {how} {ii=}'  ;  why2 = 'Ref'
        np, nl, ns, nc, nt = self.n
        self.toggleZZ(ii) #        zz = self.zz2sl()   ;   nc += len(zz)
#        self.dumpTniksPfx(why1)
        for p in range(np): #            self.setJdump(P, p, why=why2)
            self.pages[p] = self.splitH(self.pages[p], self.n[C] + self.zzl())
        self.resizeTniks(dbg=1)
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
        for zc in self.g_createTniks(self.zclms, Z, self.sects[s], ii=c, why=why):
            c2 = c + nc*(s + ns*(l + nl*p))
            self.log(f'j={C} {JTEXTS[C]:4} {c=} {c2=}  lc={len(self.zclms)} plsc ={self.fplsc(p, l, s, c)} J1={self.fmtJ1(0, 1)} J2={self.fmtJ2(0, 1)} {z1=} {z2=}', file=1)
            for t, _ in enumerate(self.g_createTniks(self.snums, T, zc, why=why)):
                tlist, j, kk, txt = self.tnikInfo(*self.J1plsct(), z=1)
                self.log(f'{t=} {j=} {JTEXTS[j]:4} {c=} {c2=} ltl={len(tlist)} plsct={self.fplsct(p, l, s, c, t)} J1={self.fmtJ1(0, 1)} J2={self.fmtJ2(0, 1)} {z1=} {z2=}', file=1)

    def refZZ(self, p, l, s, c, zz=None):
        np, nl, ns, nc, nt = self.n   ;   why = 'Ref'
        self.setJdump(C, c, why=why)
#            self.setJ(C, c3)
#            self.dumpTnik(self.colms[c3], C, why2)
        tlist, j = self.tnikInfo(p, l, s, c, zz)
        self.log(f'{zz=} j={C} {JTEXTS[C]:4} {nc=}       ltl={len(tlist)} plsc =[{self.fplsc(p, l, s, c)} J1={self.fmtJ1(0, 1)} J2={self.fmtJ2(0, 1)} z1={self.z1(c)} z2={self.z2(c)}', file=1)
        for t in range(nt):
            t2 = t + nt*(c + nc*(s + ns*(l + nl*p))) if j <= K else t
#                self.setJdump(j2, t, why=why2)
            self.setJ(j, t2)
            self.dumpTnik(tlist[t2], j, why)
            self.log(f'{zz=} {j=} {JTEXTS[j]:4} {nc=} {t2=} ltl={len(tlist)} plsct={self.fplsct(p, l, s, c, t)} J1={self.fmtJ1(0, 1)} J2={self.fmtJ2(0, 1)}', file=1)
    ####################################################################################################################################################################################################
    def hideZZs(self, how, ii, dbg=1):
        why = f'HIDE {how} ii={ii}'  ;   why2 = 'Ref'  # ;  c2, t2 = 0, 0
        self.toggleZZ(ii)
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
        self.toggleTT(ii)
        np, nl, ns, nc, nt = self.n   ;   nc += self.zzl()
        self.dumpTniksPfx(why)
        for p in range(np):
            self.setJdump(P, p, why=why2)
            for l in range(nl):
                self.setJdump(L, l, why=why2)   ;   ss = self.ss2sl()
                for s in range(len(ss)):
                    if ss[s] == ii:
                        for sect in      self.g_createTniks(self.sects, S, self.lines[l], ii=s):
                            for colm in  self.g_createTniks(self.colms, C, sect):
                                for _ in self.g_createTniks(self.tabls, T, colm): #, v=1 if p == self.j()[P] else 0): # , ii=s):
                                    pass
                    else:
                        self.setJdump(S, s, why=why2)
                        for c in range(nc):
                            self.setJdump(C, c, why=why2)
                            for t in range(nt):
                                tlist, j = self.tnikInfo(p, l, s, c, why=why2)
                                self.setJ(j, t)
                                self.dumpTnik(tlist[t], j, why=why2)
        self.dumpTniksSfx(why)
        if self.tabls and not self.cursor: self.createCursor(why)

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
                    self.createLLs(self.lines[i], i, why)
        self.dumpTniksSfx(why)
    ####################################################################################################################################################################################################
    def addPage(self, how, ins=None, dbg=1):
        np, nl, ns, nc, nt = self.n   ;   how = f'{how} {ins=}'
        self.dumpBlanks() # self.j()[P]
#        if ins is not None: self.togglePage(how)
        if ins is not None: self.toggleVisible(how, self.j()[P])
        self.n[P] += 1   ;   kl = self.k[P]
        data = [ [ self.tblankRow for _ in range(nt) ] for _ in range(nl) ]
        self.data = self.A_transposeData(dump=dbg) if self.TRANSPOSE_A else self.OLD_transposeData()
        self.data.append(data) if ins is None else self.data.insert(ins, data)
        self.data = self.A_transposeData(dump=dbg) if self.TRANSPOSE_A else self.OLD_transposeData()
        if ins is None: self.dumpTniksPfx(how, r=0)   ;   pi = len(self.pages)
        else:           self.dumpTniksPfx(how, r=1)   ;   pi = self.J1[P]
        self.J1[L], self.J1[S], self.J1[C], self.J1[T] = 0, 0, 0, 0
        n, ii, x, y, w, h =    self.geom(V, n=1, i=1, dbg=1)   ;   kk = self.cci(P, 0, kl)
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
        if   type(p) is LBL:
            p.x,  p.width,  self.p0x, self.p0w = self.splitHL(p.x, p.width, n)
            if dbg:       self.log(f'{p.x=:.2f} {p.width=:.2f} {n=} {self.p0x=:.2f} {self.p0w=:.2f}')
        elif type(p) is SPR:
            p.x, p.scale_x, self.p0x, self.p0w = self.splitHS(p.x, p.width, n, p.image.width)
            if dbg:   self.log(f'{p.x=:.2f} {p.scale_x=:.4f} {n=} {self.p0x=:.2f} {self.p0w=:.2f} {self.p0sx=:.4f}')
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
        if   type(p) is LBL: p.y, p.height, g     = self.splitV1(p.y, p.height, a)                  ;  self.log(f'{p.y=:6.2f} {p.height=:6.2f} {a=} {g=:6.2f}', file=1)  if dbg else None  ;   return p
        elif type(p) is SPR: p.y, h, g, p.scale_y = self.splitV2(p.y, p.height, a, p.image.height)  ;  self.log(f'{p.y=:6.2f} {p.scale_y=:6.4f} {a=} {h=:6.2f}', file=1) if dbg else None  ;   return p

    def splitV1(self, y, h, a, dbg=1):
        self.log(f'{y=:6.2f} {h=:6.2f} {a=}', end=' ', file=0) if dbg else None
        c = h/a  ;  h -= c  ;  y -= c/2 ;  self.log(f'{y=:6.2f} {h=:6.2f} {a=} {c=:6.2f}', pfx=0, file=1) if dbg else None  ;  return y, h, c

    def splitV2(self, y, h, a, g, dbg=1):
        self.log(f'{y=:6.2f} {h=:6.2f} {a=} {g=:6.4f}', end=' ', file=0) if dbg else None
        c = h/a  ;  h -= c  ;  g = h/g  ;  self.log(f'{y=:6.2f} {h=:6.2f} {a=} {c=:6.2f} {g=:6.4f}', pfx=0, file=1)  if dbg else None  ;  return y, h, c, g

#            if self.LL and self.isV() and not s:
#                n, _, x, y, w, h = self.geom2(C, self.rowLs[l], 1)
#                lrCol = self.createLL(None, l, c, x, y, w, h, why)
#                self.qclms.insert(c2, lrCol)
#                msg = f'WARN not tested'   ;   self.log(msg)   ;   self.quit(msg)
#    def sprite2LabelPos(self, x, y, w, h, dbg=0): x0 = x  ;  y0 = y  ;  x += w/2  ;  y -= h/2  ;  self.log(f'{x0=:6.2f} {y0=:6.2f}, {w/2=:6.2f} {-h/2=:6.2f}, {x=:6.2f} {y=:6.2f} {self.p0x=:6.2f} {self.p0y=:6.2f}', so=1) if dbg else None  ;  return x, y
####################################################################################################################################################################################################
    def isV(self, j=0, dbg=0):
        if   j <= K and self.J1[P] == self.j()[P]:   v = 1
        elif j == H or j == R or j == Q:             v = 1
        else:                                        v = 0
        if dbg:  why = f'{v=}'  ;  self.log(f'{self.fmtJText(j, why)} {self.J2[j]=} {self.i[j]=} {self.fmti()} {v=}', file=1)
        return v
    ####################################################################################################################################################################################################
    def z1(self, c=None):    return None if c is None else C1 if C1 in self.ZZ and c == C1 else C2 if C2 in self.ZZ and c == C1 else None
    def z2(self, c=None):    return None if c is None else C2 if C2 in self.ZZ and c == C2 else None
    ####################################################################################################################################################################################################
    def tnikInfo(self, p, l, s, c, t=None, z=0, why='', dbg=0):
        tlist, j, k, txt = None, -1, None, None   ;   z1, z2 = None, None
        if z: z1, z2 = self.z1(c), self.z2(c)
        exp1 = z1 == C1   ;  exp2 = z1 == C2 or z2 == C2
        msg1 = f'plsct={self.fplsct(p, l, s, c, t)} {z1=} {z2=} {exp1=} {exp2=} {txt=} {why}'
        msg2 = f'ERROR {s=} is Invalid:'
        msg3 = f'ERROR {t=} is Invalid:'
        if t is None:
            if   s == TT:  tlist, j = (self.snums, U) if exp1 else (self.capos, D) if exp2 else (self.tabls, T)
            elif s == NN:  tlist, j = (self.snams, A) if exp1 else (self.capos, D) if exp2 else (self.notes, N)
            elif s == II:  tlist, j = (self.snums, U) if exp1 else (self.capos, D) if exp2 else (self.ikeys, I)
            elif s == KK:  tlist, j = (self.snams, A) if exp1 else (self.capos, D) if exp2 else (self.kords, K)
            else:   msg = f'{msg2} {msg1}'   ;    self.log(msg)   ;   self.quit(msg) # f'{self.fmtJText(j, why=why)}'
            if dbg: msg =        f'{msg1}'   ;    self.log(msg, file=1) # self.fmtJText(j, why=why)
            return  tlist, j
        elif 0 <= t < self.n[T]:
            kT, kN, kI, kK = self.k[T], self.k[N], self.k[I], self.k[K]   ;   kO, kA, kD = self.k[U], self.k[A], self.k[D]
            tab = self.data[p][l][c][t]  # if C1 != z1 != C2 and C2 != z2 else ''
            if   s == TT:  tlist, j, k, txt = (self.snums, U, kO, self.sobj.stringNumbs[t]) if exp1 else (self.capos, D, kD, self.sobj.stringCapo[t]) if exp2 else (self.tabls, T, kT, tab)
            elif s == NN:  tlist, j, k, txt = (self.snams, A, kA, self.sobj.stringNames[t]) if exp1 else (self.capos, D, kD, self.sobj.stringCapo[t]) if exp2 else (self.notes, N, kN, tab)
            elif s == II:  tlist, j, k, txt = (self.snums, U, kO, self.sobj.stringNumbs[t]) if exp1 else (self.capos, D, kD, self.sobj.stringCapo[t]) if exp2 else (self.ikeys, I, kI, tab)
            elif s == KK:  tlist, j, k, txt = (self.snams, A, kA, self.sobj.stringNames[t]) if exp1 else (self.capos, D, kD, self.sobj.stringCapo[t]) if exp2 else (self.kords, K, kK, tab)
            else:   msg = f'{msg2} {msg1}'   ;    self.log(msg)   ;   self.quit(msg) # self.fmtJText(j, t, why)
            if dbg: msg =        f'{msg1}'   ;    self.log(msg, file=1) # self.fmtJText(j, t, why)
            return  tlist, j, k, txt
        else:       msg = f'{msg3} {msg1}'   ;    self.log(msg)   ;   self.quit(msg) # self.fmtJText(j, t, why)
    ####################################################################################################################################################################################################
    def geom(self, j, p=None, n=None, i=None, dbg=1):
        assert 0 <= j <= len(JTEXTS), f'{j=} {len(JTEXTS)=}'
        if n is None: n = self.n[j]
#        n += self.zzl() if j == Z or j == R else 0 #!#
        i = i if i is not None else self.i[j]
        if   p is None:        w  =  self.width - self.p0w  ;  h  =  self.height
        elif j == C or j == Q: w  =  p.width/n              ;  h  =  p.height
        elif j == Z:           w  =  p.width/n              ;  h  =  p.height
        else:                  w  =  p.width                ;  h  =  p.height/n   if j != P else p.height
        if self.SPRITES:
            if   p is None:        x  =  self.p0x           ;  y  =  self.height - h
            elif j == T:           x  =  p.x + w/2          ;  y  =  p.y + p.height - h/2
            elif j == Q:           x  =  p.x + w/2          ;  y  =  p.y + p.height - h/2
            elif j == A or j == U: x  =  p.x + w/2          ;  y  =  p.y + p.height - h/2
            elif j == Z:           x  =  p.x                ;  y  =  p.y + p.height - h
            else:                  x  =  p.x                ;  y  =  p.y + p.height - h
        else:
            if   p is None:        x  =  self.p0x + w/2     ;  y  =  self.height - h/2
            elif j == Q:           x  =  w/2                ;  y  =  p.y
            elif j == Z:           x  =  w/2                ;  y  =  p.y
            elif j == C:           x  =  self.p0x + w/2                ;  y  =  p.y
            elif j == T:           x  =  p.x                ;  y  =  p.y + p.height/2 - h/2
            elif j == A or j == U: x  =  p.x                ;  y  =  p.y + p.height/2 - h/2
            else:                  x  =  p.x - p.width/2 + w/2          ;  y  =  p.y + p.height/2 - h/2
        if dbg and self.VRBY >= 2:
            msg  = f'{j=:2} {JTEXTS[j]:4} {n=:2} {self.fxywh(x, y, w, h)}'
            msg2 = f' : {self.ftxywh(p)}' if p else f' : {self.fxywh(0, 0, 0, 0)}'
            msg += msg2 if p else " " * len(msg2)
            self.log(f'{msg} {self.fmtJ1(0, 1)} {self.fmtJ2(0, 1)}', pfx=0, file=1)
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
    def ntsl(self): n = 1 + self.n[T] * self.ssl() * self.i[L]   ;   return n
    ####################################################################################################################################################################################################
    def createZZs(self, p, s, why, dbg=1):
        n = self.n[C] + self.zzl()
        kz = self.k[Z]   ;   kk = self.cci(Z, s, kz) if self.CHECKERED else 0
        nz, iz, xz, yz, wz, hz = self.geom(Z, p, n, s, dbg=dbg)
        zclm = self.createTnik(self.zclms, s, Z, xz, yz, wz, hz, kk, kz, why, v=1, dbg=dbg)
        if s == 0 or s == 2:
            nu, iu, xu, yu, wu, hu = self.geom(U, zclm, self.n[T], self.i[L], dbg=dbg)
            for u in range(nu):
                self.createZZ(s, u, xu, yu, wu, hu, why)
        if s == 1 or s == 3:
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
        n = self.n[C] + self.zzl()
        nz, iz, xz, yz, wz, hz = self.geom(Z, pt, n, self.i[S], dbg=dbg)
        zclm = self.resizeTnik(self.zclms, self.J2[Z], Z, xz, yz, wz, hz, why, dbg=dbg)
        nu, iu, xu, yu, wu, hu = self.geom(U, zclm, self.n[T], self.i[L], dbg=dbg)
        for u in range(nu):
            self.resizeTnik(self.snums, self.J2[U], U, xu, yu-u*hu, wu, hu, why, dbg=dbg)
        pt = self.splitH(pt, n, dbg=dbg)
        return pt

    def createLLs(self, pt, pi, why, dbg=1, dbg2=1):
        n = self.ntsl()   ;   kl = self.k[R]   ;   kk = self.cci(R, pi, kl) if self.CHECKERED else 0
        nr, ir, xr, yr, wr, hr = self.geom(R, pt, n, self.i[L], dbg=dbg2) #  ;   xr0 = xr
        lrow = self.createTnik(self.rowLs, pi, R, xr, yr, wr, hr, kk, kl, why, v=1, dbg=dbg)
        nc, ic, xc, yc, wc, hc = self.geom(Q, lrow, self.n[C], self.i[C], dbg=dbg2) #  ;   xc0 = xc
        for c in range(nc):
            self.createLL(self.qclms, pi, c, xc, yc, wc, hc, why)
        pt = self.splitV(pt, n, dbg=dbg2)
        self.dumpTnik(pt, L, why=why)
        return pt

    def createLL(self, tlist, l, c, x, y, w, h, why, dbg=1):
        cc = c + self.n[C] * l
        kl = self.llcolor(cc, Q)
        zl = self.zzl()  ;  kk = NORMAL_STYLE
        z  = 1 if self.FRET_BOARD else 2
        text = self.llText[z-zl:]
        txt  = text[c]
        ll   = self.createTnik(tlist, cc, Q, x + c*w, y, w, h, kk, kl, why, t=txt, v=1, dbg=dbg)
        self.setLLStyle(cc, kk)
        return ll

    def resizeLLs(self, pt, why, dbg=1, dbg2=1):
        n = self.ntsl()
        nr, ir, xr, yr, wr, hr = self.geom(R, pt, n, self.i[L], dbg=dbg2)  # ;    xr0 = xr
        lrow = self.resizeTnik(self.rowLs, self.J2[R], R, xr, yr, wr, hr, why, dbg=dbg)
        nc, ic, xc, yc, wc, hc = self.geom(Q, lrow, self.n[C], self.i[C], dbg=dbg2)  # ;    xc0 = xc
        for c in range(nc):
            self.resizeTnik(self.qclms, self.J2[Q], Q, xc + c*wc, yc, wc, hc, why, dbg=dbg)
        pt = self.splitV(pt, n, dbg=dbg2)
        return pt
    ####################################################################################################################################################################################################
    def createTniks(self, dbg=1):
        self.newC += 1  ;  why2 = f'New{self.newC}'  ;  why = why2
        self.dumpTniksPfx(why)    ;    view = None #  ;    j = self.j()  ;  p = 0  ;  v = 0
#        if self.VIEWS: # _, _, x, y, w, h = self.geom2(V, n=1, i=1, dbg=1)  ;  kk = 0  ;  kl = self.k[V] # view = self.createTnik(self.views, 0, V, x, y, w, h, kk, kl, why=why, dbg=1)
        for page in              self.g_createTniks(self.pages, P, view, why=why): # pass
            for line in          self.g_createTniks(self.lines, L, page, why=why): # pass
                for sect in      self.g_createTniks(self.sects, S, line, why=why): # pass
                    for colm in  self.g_createTniks(self.colms, C, sect, why=why): # pass
                        for _ in self.g_createTniks(self.tabls, T, colm, why=why): pass
        if self.tabls:  self.createCursor(why)
        self.dumpTniksSfx(why)
        if dbg:         self.dumpStruct(why2)
    ####################################################################################################################################################################################################
    def g_createTniks(self, tlist, j, pt, ii=None, why='', dbg=1, dbg2=1):
        n = 1 if ii is not None else None
        n, _, x, y, w, h = self.geom(j, pt, n, ii, dbg=dbg2)   ;   text = ''   ;    kl = self.k[j]    ;  tlist2 = tlist   ;   p, l, c, _ = self.J1plct()
        n                = n if ii is None else 1       ;   j2 = j   ;   i3 = 0   ;   x2 = x   ;   y2 = y
        for i in range(n):
            if self.DBG_TAB_TEXT:                      dlm = '\n' if j == C else ''  ;  text = f'{JTEXTS[j][0]}{dlm}{self.lenE()[-1]}'
            i2 = i if ii is None else ii
            if   j == P:                                 v = 1 if i == self.j()[P] else 0   ;   self.log(f'j==P: {i=} {v=} {self.j()[P]=} {self.i[P]=}')
            else:                                        v = int(self.pages[self.J1[P]].visible)
            if   j == C or j == Z:                      x2 = x + i2 * w #  ;   j2 = len(self.J2) if ii is not None else j
            else:
                if   j != P:                            y2 = y - i2 * h
                if   j == S:                             _ = self.ss2sl()[i2]  ;  self.SS.add(_)
                elif j >= T:
                    s                    = self.ss2sl()[self.J1[S]]
                    tlist2, j2, kl, tobj = self.tnikInfo(p, l, s, c, i2, why=why)
                    if   s == TT:                     text = tobj
                    elif s == NN:                     text = tobj if j2 > K else self.sobj.tab2nn(tobj, i2) if self.sobj.isFret(tobj) else self.tblank
                    elif s >= II:
                        if   s == II:  imap = self.getImap(p, l, c)  ;  text = self.imap2ikey( tobj, imap, i3, j2)  ;  i3 += 1 if text != self.tblank else 0
                        elif s == KK:  imap = self.getImap(p, l, c)  ;  text = self.imap2Chord(tobj, imap, i2, j2)
            kk = self.cci(j2, i2, kl) if self.CHECKERED else 0
            yield self.createTnik(tlist2, i2, j2, x2, y2, w, h, kk, kl, why=why, t=text, v=v, dbg=dbg)
    ####################################################################################################################################################################################################
    def createTnik(self, tlist, i, j, x, y, w, h, kk, kl, why='', t='', v=0, g=None, dbg=0):
        if i is None or j is None: lt = len(tlist) if tlist is not None else None  ;  msg = f'ERROR i or j is None {i=} {j=} {lt=} {t=} {why}'  ;  self.log(msg)  ;  self.quit(msg)
        assert type(v) is int, f'{v=} {type(v)=} is not int' # v = int(v)
        self.setJ(j, i, v)
        o, k2, d, ii, n, s = self.fontParams()   ;   b = self.batch   ;   k = kl[kk]
        g = g           if g is not None else self.j2g(j)
        if j == H or (self.SPRITES and (j < T or j == R)):
            scip  = pyglet.image.SolidColorImagePattern(k)
            img   = scip.create_image(width=fri(w), height=fri(h))
            tnik  = SPR(img, x, y, batch=b, group=g, subpixel=self.SUBPIX)
            tnik.color, tnik.opacity = k[:3], k[3]
        else:
            s         = self.calcFontSize(t, w, h, j) # * v if self.RESIZE_FONTS else 1
            z         = 1 if self.STRETCH else 0
            d, n      = FONT_DPIS[d], FONT_NAMES[n]   ;   ml = self.MULTI_LINE
            a, ax, ay = self.a, self.ax, self.ay  # left center right  # bottom baseline center top
            tnik = LBL(t, font_name=n, font_size=s, bold=o, stretch=z, italic=ii, color=k, x=x, y=y, width=w, height=h, anchor_x=ax, anchor_y=ay, align=a, dpi=d, batch=b, group=g, multiline=ml)
            if   T <= j <= K:  self._setTNIKStyle(tnik, self.k[j], NORMAL_STYLE)
            elif j == Q:       self._setTNIKStyle(tnik, self.k[j] if (i+1) % 10 else self.k[R], NORMAL_STYLE)
        tnik.visible = v   ;   self.visib[j].append(v)
        if    tlist is not None:       tlist.append(tnik)
        key = self.idmapkey(j)    ;    self.idmap[key] = (tnik, j, i)   ;   self.dumpTnik(tnik, j, why) if dbg else None
        if self.LL and j == L:
            if not self.rowLs or len(self.rowLs) < self.n[L]: tnik = self.createLLs(tnik, i, why)
            else:                                             tnik = self.splitV(tnik, self.ntsl(), dbg=dbg)
        if self.ZZ and j == P:
            tnik = self.splitH(tnik, self.n[C] + self.zzl())
        if self.ZZ and j == S and v:
            tnik = self.createZZs(tnik, i, why)
        return tnik
    ####################################################################################################################################################################################################
    def hideTnik(self, tlist, i, j, dbg=0): # AssertionError: When the parameters 'multiline' and 'wrap_lines' are True,the parameter 'width' must be a number.
        c = tlist[i]    ;    ha = hasattr(c, 'text')
        if   type(c) is LBL: c.x, c.y, c.width, c.height = 0, 0, 1, 0  # Zero width not allowed
        elif type(c) is SPR: c.update(x=0, y=0, scale_x=0, scale_y=0)
        self.setJ(j, i)
        if dbg: self.dumpTnik(c, j, 'Hide')
        if dbg > 1:    text = c.text if ha else ''  ;  self.log(f'{self.fmtJText(j)} {i=} {id(c):x} {text:6} {self.ftxywh(c)}  J1={self.fmtJ1(0, 1)} J2={self.fmtJ2(0, 1)}', pfx=0)
    ####################################################################################################################################################################################################
    def resizeTniks(self, dbg=1):
        self.updC += 1  ;  why2 = f'Upd{self.updC}'  ;  why = why2
        self.dumpTniksPfx(why)   ;   view = None
#        if self.VIEWS:
#            _, _, x, y, w, h = self.geom2(V, n=1, i=1, dbg=0)
#            if not self.views:    msg = f'ERROR Empty views {self.n=} {self.zzl()}';   self.log(msg);   self.quit(msg)
#            view = self.resizeTnik(self.views, 0, V, x, y, w, h, dbg=1)
        for i, page in enumerate(self.g_resizeTniks(self.pages, P, view, why=why)): # pass
            for line in          self.g_resizeTniks(self.lines, L, page, why=why): # pass
                for sect in      self.g_resizeTniks(self.sects, S, line, why=why): # pass
                    for colm in  self.g_resizeTniks(self.colms, C, sect, why=why): # pass
                        for _ in self.g_resizeTniks(self.tabls, T, colm, why=why): pass
        if self.RESIZE and self.cursor: self.resizeCursor(why, self.cc)
        self.dumpTniksSfx(why)
        if dbg:         self.dumpStruct(why2)
    ####################################################################################################################################################################################################
    def g_resizeTniks(self, tlist, j, pt=None, why='', dbg=1, dbg2=1):
        if not self.n[j]:     msg = f'ERROR {self.fmtJText(j, why)} SKIP {self.n[j]=}'   ;   self.log(msg)   ;   self.quit(msg)
        n, _, x, y, w, h = self.geom(j, pt, dbg=dbg2)
        x2 = x  ;  y2 = y  ;  j2 = j  ;  tlist2 = tlist
        p, l, c, t = self.J1plct()    ;  lp, ll = self.dl()[0], self.dl()[1]
        for i in range(n):
            if   j == C or j == Z:       x2 = x + i * w
            else:
                if    j != P:            y2 = y - i * h
                else: v = int(self.pages[self.J1[P]].visible)  ;  self.log(f'j==P: {i=} {v=} {self.j()[P]=} {self.i[P]=}')
                if    j == L and self.J2[L] >= lp * ll: msg = f'WARN MAX Line {self.J2[L]=} >= {lp=} * {ll=}'  ;   self.log(msg)  ;  self.quit(msg)
                elif  j >= T:
                    s = self.ss2sl()[self.J1[S] % self.ssl()]
                    tlist2, j2 = self.tnikInfo(p, l, s, c, why=why)
            tnik = self.resizeTnik(tlist2, self.J2[j2], j2, x2, y2, w, h, why=why, dbg=dbg)
            yield tnik
    ####################################################################################################################################################################################################
    def resizeTnik(self, tlist, i, j, x, y, w, h, why='', dbg=1):
        if not tlist:          msg = f'ERROR tlist is Empty {      self.fmtJText(j, why)}'  ;  self.log(msg)  ;  self.quit(msg)
        elif i >=  len(tlist): msg = f'ERROR {i=} >={len(tlist)=} {self.fmtJText(j, why)}'  ;  self.log(msg)  ;  self.quit(msg)
        tnik = tlist[i]   ;   v = tnik.visible
        self.log(f'{H=} {j=} {i=} {self.J2[H]=}') if dbg and j == H  else None
        self.setJ(j, i, v) if j != H or (j == H and self.J2[H] == 0) else None
        if   type(tnik) is LBL: fs = self.calcFontSize(tnik.text, w, h, j)   ;   fs *= v if self.RESIZE_FONTS else 1  ;   tnik.x, tnik.y, tnik.width, tnik.height, tnik.font_size = x, y, w, h, fs
        elif type(tnik) is SPR: mx, my = w/tnik.image.width, h/tnik.image.height    ;   tnik.update(x=x, y=y, scale_x=mx, scale_y=my)
        if self.LL and j == L:
            if v: tnik = self.resizeLLs(tnik, why)
            else: tnik = self.splitV(tnik, self.ntsl(), dbg=dbg)
#        if self.ZZ and j == S:
#            tnik = self.resizeZZs(tnik, why)
        self.dumpTnik(tnik, j, why) if dbg else None
        return tnik
    def p2Js(self, p): np, nl, ns, nc, nt = self.n  ;  l, s, c, t = p*nl, p*nl, p*nl*nc, p*nl*nc*nt  ;  j1 = [p%np,l%nl,s%ns,c%nc,t%nt,t%nt,t%nt,t%nt,0,0,0,0,0,0,0,0,0]  ;  j2 = [p, l, s, c, t, t, t, t, 0,0,0,0,0,0,0,0,0]  ;  self.log(f'{util.fmtl(j1)=} {util.fmtl(j2)=}')  ;  return j1, j2
    ####################################################################################################################################################################################################
    def toggleVisible(self, why=None, p=None, dbg=1):
        why = 'TVis' if why is None else why   ;   np, nl, ns, nc, nt = self.n   ;   i = 0   ;   text = None
        lines, sects, colms, tabs = self.lines, self.sects, self.colms, self.tabls
        pid = f' {id(self.pages[p]):11x}' if self.TIDS else ''
        self.dumpTniksPfx(why)
        self.J1, self.J2 = self.p2Js(p%np)
        self.log(f'BGN {why} {p=} {pid} pages[{p}].v={int(self.pages[p].visible)} {self.fmti()} {self.fmtn()} {self.fVis()}')
        self.pages[p].visible = not self.pages[p].visible                         ;  self.setJdump(P, p, why=why)
        for l in range(nl):
            line = lines[self.J2[L]]          ;  line.visible = not line.visible  ;  self.setJdump(L, l, why=why) ; vl = []
            for s0, s in enumerate(self.ss2sl()):
                sect = sects[self.J2[S]]      ;  sect.visible = not sect.visible  ;  self.setJdump(S, s0, why=why)
                for c in range(nc):
                    colm = colms[self.J2[C]]  ;  colm.visible = not colm.visible  ;  self.setJdump(C, c, why=why)
                    for t in range(nt):
                        imap = self.getImap(p, l, c) if s >= II else []
                        tlist, j, kl, tobj = self.tnikInfo(p, l, s, c, t, why=why)
                        if   s == TT: text = tobj
                        elif s == NN: text = tobj if j > K else self.sobj.tab2nn(tobj, t) if self.sobj.isFret(tobj) else self.tblank
                        elif s == II: text = self.imap2ikey( tobj, imap, i, j)   ;   i += 1 if text != self.tblank else 0
                        elif s == KK: text = self.imap2Chord(tobj, imap, t, j)
                        j2 = self.J2[j]  ;  tnik = tlist[j2]
                        tnik.visible = not tnik.visible  ;  v = int(tnik.visible)  ;  self.setJdump(j, t, why=why)
                        oid = f' {id(tnik):11x}' if self.TIDS else ''
                        if dbg:       self.log(f'{v=} {j2=:3} {s0} plsct={self.fplsct(p, l, s, c, t)} {text=:4} {oid} {self.J2[j]}', file=1)
                        if dbg:       vl.append(f'{v}')
                if dbg:               vl.append(' ')
            if dbg:                   self.log(f'{"".join(vl)}', pfx=0)
        self.dumpTniksSfx(why)
        self.log(f'END {why} {p=} {pid} pages[{p}].v={int(self.pages[p].visible)} {self.fmti()} {self.fmtn()} {self.fVis()}')
    ####################################################################################################################################################################################################
    def dumpTniksPfx(self, why='', h=1, r=1):
        if r:        self.resetJ(why)   ;   self.clearVisib()
        self.dumpGeom('BGN', why)
        if not r:    self.dumpJs(why, w=None)  if self.J1 and self.J2 else self.quit(f'ERROR No Js {len(self.J1)=} {len(self.J2)=}')
        if h: self.dumpHdrs()

    def dumpTniksSfx(self, why='', h=1):
        if h: self.dumpHdrs()
        self.dumpJs(why, w=None)               if self.J1 and self.J2 else self.quit(f'ERROR No Js {len(self.J1)=} {len(self.J2)=}')
        self.dumpGeom('END', why)

    def dumpHdrs(self): hdr1 = self.fTnikHdr(1)   ;   hdr0 = self.fTnikHdr(0)   ;   self.log(f'{hdr1}', pfx=0)   ;   self.log(f'{hdr0}', pfx=0)
    ####################################################################################################################################################################################################
    def fTnikHdr(self, spr=0):
        tid  = ' TId  Identity  ' if self.TIDS else ' Tid'  ;  wnc = ' Why  Name  Cnt'  ; rtsgv = 'Rotated G V'       if spr else 'Txt fSz G V'
        xywh = '    X       Y       W       H  '            ;  rgb = ' Red Grn Blu Opc'  if self.LONG_TXT else ''
        sfx  = (' Iax  Iay      Grp        pGrp' if spr else 'cw  ch v a x y dpi B I Font Name') if self.LONG_TXT else ''
        rgbM = (' M     Mx    My  ' if spr else rgb) if self.LONG_TXT else ''
        return f'{tid} {wnc} {rtsgv} {self.fjtxt()} {xywh} {rgb} {rgbM} {sfx}'
    @staticmethod
    def fjtxt(): return ' '.join(f'{jtxt[0]:>{JFMT[i]}}' for i, jtxt in enumerate(JTEXTS)) + ' Vis'
    def clearVisib(self):             consume(v.clear() for v in self.visib)

    def dumpTnik(self, t=None, j=None, why=''):
        if   t is None: self.log(f'{self.fTnikHdr()}', pfx=0)   ;   return
        if   j is None:                                 msg = f'ERROR BAD j {j=}'          ;  self.log(msg)  ;  self.quit(msg)
        elif type(t) is not LBL and type(t) is not SPR: msg = f'ERROR Bad type {type(t)}'  ;  self.log(msg)  ;  self.quit(msg)
        xywh = self.ftxywh(t)   ;   g = self.gn[j]   ;   fc, bc = '', ''    ;   msg2, msg5 = '', ''
        if   type(t) is LBL: fc = self.getDocColor(t, 0)  ;  bc = self.getDocColor(t, 1)   ;  msg2 = self.fTxFs(t)  ;  msg5 = self.fLbl(t) if self.LONG_TXT else ''
        elif type(t) is SPR: fc = self.ftcolor(t)         ;  bc = self.ftMxy(t)            ;  msg2 = self.frot(t)   ;  msg5 = self.fSpr(t) if self.LONG_TXT else ''
        else: msg = f'ERROR BAD type(t) {why} {j=} {type(t)=}'   ;   self.log(msg)   ;   self.quit(msg)
        msg1 = self.fid(t, j, why)   ;   msg3 = f'{self.ftvis(t)}'   ;   msg4 = f'{fc} {bc}' if self.LONG_TXT else ''
        self.log(f'{msg1} {msg2} {g} {msg3} {self.fmtJ2()} {xywh} {msg4} {msg5}', pfx=0)
    ####################################################################################################################################################################################################
    def idmapkey(self, j): return f'{JTEXTS[j]}{self.J2[j]}'
    def dumpIdmKeys(self): self.log(f'{util.fmtl(list(self.idmap.keys()), ll=1)}')
    def fSpr(self, t):     return f'{self.fiax(t)} {self.fiay(t)} {self.fgrp(t)} {self.fgrpp(t)}'
    def fLbl(self, t):     return f'{self.fCtnt(t)} {self.fAxy()} {self.ffont(t)}'
    @staticmethod
    def frot(t):           return f'{t.rotation:7.2f}'
    def fnvis(self):       return f'{self.nvis:3}'
    @staticmethod
    def fTxFs(t):          return f'{t.text:>3} {t.font_size:3}'
    def fCtnt(self, t):    return f'{t.content_width:2} {t.content_height:3} {self.fcva(t)}'
    def getDocColor(self, t, c=1): return util.fColor(self._getDocColor(t, c))
    @staticmethod
    def _getDocColor(t, c=1): s = 'background_color' if c else 'color'  ;  return t.document.get_style(s)
    def fid(self, t, j, why): i, n = self.J2[-1], int(self.idmapkey(j)[4:])  ;  oid = f' {id(t):11x}' if self.TIDS else ''  ;  return f'{i:4}{oid} {why:5} {JTEXTS[j]} {n:4}'
    ####################################################################################################################################################################################################
    def dumpTniksA(self, why=''):
        self.dumpTniksPfx(why)
        for v in self.idmap.values():
            self.setJdump(v[1], v[2], why=why)
        self.dumpTniksSfx(why)

    def dumpTniksB(self, why=''):
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
    def dumpTniksC(self, why=''):
        self.dumpTniksPfx(why)
        consume(consume(self.setJdump(j, i % self.n[j], why=why) for i in range(len(self.E[j]))) for j in range(len(self.E)))
        self.dumpTniksSfx(why)

    def dumpTniksD(self, why=''):
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
    def createCursor(self, why, dbg=1):
        x, y, w, h, c = self.cc2xywh()
        kk = 0  ;  kl = self.k[H]
        if w == 0 or h == 0: msg = f'ERROR DIV by ZERO {w=} {h=}'   ;   self.log(msg)   ;   self.quit(msg)
        self.cursor   = self.createTnik(self.hcurs, 0, H, x, y, w, h, kk, kl, why, v=1, dbg=dbg)
        if self.LL:     self.setLLStyle(self.cc, CURRENT_STYLE)

    def resizeCursor(self, why, why2, dbg=1):
        x, y, w, h, c = self.cc2xywh()
        self.resizeTnik(self.hcurs, 0, H, x, y, w, h, why, dbg=dbg)
        if dbg and self.SNAPS: self.regSnap(f'{why}', f'RSZC_{why2}')

    def moveCursor(self, ss=0, why='', dbg=1):
        if dbg:           self.log(f'BGN {ss=} {self.cc=}', pos=1)
        if self.LL:       self.setLLStyle(self.cc, SELECT_STYLE if ss else NORMAL_STYLE)
        self.resizeCursor(why, why2=self.cc, dbg=dbg)
        if self.LL:       self.setLLStyle(self.cc, CURRENT_STYLE)
        if dbg:           self.log(f'END {ss=} {self.cc=}', pos=1)
    ####################################################################################################################################################################################################
    def cc2xywh(self, dbg=1):
        tpb, tpp, tpl, tps, tpc = self.ntp()
        cc = self.cursorCol()   ;   old = cc
        if cc >= tpp: cc = cc % tpp # + tpl
        if cc >= tpl: cc = cc % tpl + tps
        t = self.tabls[cc]
        cw, ch, ca = t.content_width, t.content_height, t.content_valign
        if dbg: self.log(f'{cc=:4} {old=:4} {self.fntp()} {self.ftxywh(t)} {t.text=} {cw=} {ch=} {ca}', file=1)
        w, h = t.width, t.height
        x, y = t.x - w/2, t.y - h/2
        return x, y, w, h, cc
    ####################################################################################################################################################################################################
    def plc2cn(self, p, l, c, dbg=0):
        tpb, tpp, tpl, tps, tpc = self.ntp()  ;  ns = self.n[S]
        cn = p*tpp//tpc + l*tpl//tpc//ns + c
#        cc = p*tpp + l*tpl//ns + c*tpc
        if dbg: self.log(f'{cn:4} {self.cn2cc(cn):4} {self.fntp()} plc={self.fplc(p, l, c)} ({p*tpp=:4} +{l*tpl=:3} +{c*tpc=:3})')
        return cn
#        return ( p *self.tpp//self.tpc) + (l *self.tpl//self.tpc) + c//self.tpc

    def plct2cc(self, p, l, c, t, dbg=0):
        tpb, tpp, tpl, tps, tpc = self.ntp()  ;  ns = self.n[S]
        cc = p*tpp//ns + l*tpl//ns + c*tpc + t
#        cc = p*tpp + l*tpl + s*tps + c*tpc + t
        if dbg: self.log(f'    {cc:4} {self.fntp()} {self.fplct(p, l, c, t)} ({p*tpp:4} +{l*tpl:3} +{tps:3} +{c*tpc:3} +{t})')
        return cc

    def cursorCol(  self, dbg=0):      cc = self.plct2cc(*self.j2(), dbg=dbg)  ;  self.log( f'{cc=:3} {self.j2()}') if dbg else None  ;  self.cc = cc  ;  return self.cc
    def normalizeCC(self, cc, dbg=0):  tpc = self.tpc  ;  old = cc  ;  cc = cc//tpc * tpc   ;  self.log(f'{old=:4} {cc=:4} {tpc=}')  if dbg else None  ;  return (cc//self.tpc) * self.tpc
    def cc2cn(      self, cc, dbg=0):  tpc = self.tpc  ;  cn = cc//tpc  ;  self.log(f'{cn:3} {cc:4}//{tpc=} {cc//tpc=}') if dbg else None  ;  return  cn
    def cn2cc(      self, cn, dbg=0):  tpc = self.tpc  ;  cc = cn *tpc  ;  self.log(f'{cc:4} {cn:3} *{tpc=} {cn *tpc=}') if dbg else None  ;  return  cc
    def cn2txt(self, cn, dbg=0):  #  usefull? re-name f cn2tabtxt()
        cc = self.cn2cc(cn)
        p, l, c, t = self.cc2plct(cc)
        txt = self.data[p][l][c]
        self.log(f' {cn:3} {cc:4} {self.fntp()} {self.fplc(p, l, c)} txt={txt}') if dbg else None
    ####################################################################################################################################################################################################
    def cc2plct(self, cc, dbg=0):
        tpb, tpp, tpl, tps, tpc = self.ntp()
        np, nl, ns, nc, nt = self.n
        t =    cc      % nt
        c =    cc//tpc % nc
#        s =    cc//tps % ns
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
        return rp, rl, rc, rt
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
        return rp, rl, rs, rc, rt
    ####################################################################################################################################################################################################
    def setCaption(self, msg, dbg=1):
        if dbg: self.log(f'{msg}')
        self.set_caption(msg)
    ####################################################################################################################################################################################################
    def calcFontSize(self, t, w, h, j=4, dbg=0):
        if j == C: scale = 1.5
        else:      scale = 1.25
        pix  = min(scale * w, h)
        fs   =  self.pix2fontsize(pix)
        if dbg: self.log(f'{j=} {JTEXTS[j]:4} {t=} {w=:6.2f} {h=:6.2f} {pix=:6.2f}=min({scale=:.1f}*w, h) {fs=:6.2f}')
        return int(fs)

    def _initFonts(self):
        np, nl, ns, nc, nt = self.n          ;  nc += self.zzl()
        n = nl * nt * ns if ns else nl * nt  ;   n += self.LL * nl
        w = self.width / nc  ;  h = self.height / n
        fs = self.calcFontSize('X', w, h, j=T, dbg=1)
        self.fontBold, self.fontItalic, self.clrIdx, self.fontDpiIndex, self.fontNameIndex, self.fontSize = 0, 0, 0, 4, 0, fs
        self.log(f'{w=:6.3f}={self.width =}/({nc})                   {FONT_SCALE=:5.3f} fs=w*FONT_SCALE={fs:6.3f}pt')
        self.log(f'{h=:6.3f}={self.height=}/({nl=} * {ns=} * {nt=})  {FONT_SCALE=:5.3f} fs=h*FONT_SCALE={fs:6.3f}pt')
        self.dumpFont()

    def fmtFont(self, dbg=0):
        fb, fc, fd, fi, fn, fs = self.fontParams()
        text = f'{FONT_DPIS[fd]}dpi {fs:5.2f}pt {FONT_NAMES[fn]} {fc}'
        if dbg: self.log(f'{text}')
        return text

    def dumpFont(self, why=''):
        b, k, dpi, i, n, s = self.fontParams()
        pix = s / FONT_SCALE   ;   fcs = '' # f'{util.fmtl( [k])}'
        self.log(f'{dpi}:{FONT_DPIS[dpi]}dpi {s:6.3f}pt {n}:{FONT_NAMES[n]} {k}:{fcs} {s:6.3f}pt = {FONT_SCALE:5.3f}(pt/pix) * {pix:6.3f}pixels {why}')

    def setFontParam(self, n, v, m, dbg=1):
        setattr(self, m, v)
        if m == "clrIdx": self.fontStyle = NORMAL_STYLE if self.fontStyle == SELECT_STYLE else SELECT_STYLE
        if dbg:                         self.log( f'      {n:12}  {v:4}  {m}  {len(self.E)=}')
        for i in range(len(self.E)):
            if dbg and self.VRBY:    self.log(f'{i:4}  {n:12}  {v:4}  {m}  {len(self.E)=}')
            self._setFontParam(self.E[i], n, v, m)
        self.setCaption(self.fmtFont())

    def _setFontParam(self, p, n, v, m, dbg=1):
        for i in range(len(p)):
            # k = len(p[i].color) # { [v][:k]=}' if m == "clrIdx" else
            msg = f'{FONT_NAMES[v]=}' if m == "fontNameIndex" else f'{v=}'
            if dbg:
                f = 1 if self.VRBY else 10
                if not i % f:           self.log(f'{i:4}  {n:12}  {v:4}  {msg}')
            if   m == 'clrIdx':         self.setTNIKStyle(i, 1, self.fontStyle)
            else:                       setattr(p[i], n, FONT_NAMES[v] if m == 'fontNameIndex' else v)
    @staticmethod
    def pix2fontsize(pix): return pix * FONT_SCALE # ( ) % FS_MAX
    def fontParams(self):    return self.fontBold, self.clrIdx, self.fontDpiIndex, self.fontItalic, self.fontNameIndex, self.fontSize
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
        old = self.cursorCol()   ;   j2 = self.j2
        p, l, c, t = j2()   ;   data = self.data[p][l][c][t]
        cc  = self.cursorCol()   ;   msg = ''   ;   cc2 = cc
        if cc2 >= self.tpp:
            tp, dtp, mtp = self.modDiv(cc, P)   ;   cc2 = tp + mtp   ;   msg = f' {tp=:3} {dtp=} {mtp=} {cc2=:3}'
        if cc2 >= self.tpl:
            tp, dtp, mtp = self.modDiv(cc, L)   ;   cc2 = tp + mtp   ;   msg = f' {tp=:3} {dtp=} {mtp=} {cc2=:3}'
        self.log(f'BGN {how} {text=} {data=} {rev=} {old=:3} {cc=:3}{msg}', pos=1)
        self.setDTNIK(text, cc2, p, l, c, t, kk=1)
        p, l, c, t = j2()   ;   data = self.data[p][l][c][t]
        self.log(f'END {how} {text=} {data=} {rev=} {old=:3} {cc=:3}{msg}', pos=1)
        if rev: self.reverseArrow()
        else:   self.autoMove(how)
        if dbg and self.SNAPS:
            stype = f'TXT_{text}' if self.sobj.isFret(text) else 'SYMB' if text in util.DSymb.SYMBS else 'UNKN'
            self.regSnap(f'how', stype)
        self.resyncData = 1

    def setDTNIK(self, text, cc, p, l, c, t, kk=0, pos=0, dbg=1):
        if dbg: self.log(f'BGN {kk=}    {text=}', pos=pos)
        self.setData(text, p, l, c, t)
        imap = self.getImap(p, l, c)
        if TT in self.SS: self.setTab2( text, cc)
        if NN in self.SS: self.setNote( text, cc, t)
        if II in self.SS: self.setIkey( imap, p, l, c)
        if KK in self.SS: self.setChord(imap, cc, pos=1, dbg=1) if kk else None
        if dbg: self.log(f'END {kk=}    {text=} {len(imap)=}', pos=pos)
    ####################################################################################################################################################################################################
    def setData(self, text, p, l, c, t, pos=0, dbg=1):
        data = self.data[p][l][c]
        if dbg: self.log(f'BGN {t=} {text=} {data=}', pos=pos)
        self.data[p][l][c] = data[0:t] + text + data[t+1:]
        data = self.data[p][l][c]
        if dbg: self.log(f'END {t=} {text=} {data=}', pos=pos)

    def setTab2(self, text, cc, pos=0, dbg=0):
        if dbg: self.log(f'BGN         {text=} tabs[{cc}]={self.tabls[cc].text}', pos=pos)
        self.tabls[cc].text = text
        if dbg: self.log(f'END         {text=} tabs[{cc}]={self.tabls[cc].text}', pos=pos)

    def setNote(self, text, cc, t, pos=0, dbg=0):
        if dbg: self.log(f'BGN     {t=} {text=} notes[{cc}]={self.notes[cc].text}', pos=pos)
        self.notes[cc].text = self.sobj.tab2nn(text, t) if self.sobj.isFret(text) else self.tblank
        if dbg: self.log(f'END     {t=} {text=} notes[{cc}]={self.notes[cc].text}', pos=pos)
    ####################################################################################################################################################################################################
    def getImap(self, p=None, l=None, c=None, dbg=0, dbg2=0):
        dl = self.dl()
        cn = self.plc2cn(p, l, c)      ;    key = cn   ;   mli = self.cobj.mlimap
        msg1  = f'plc={self.fplc(p, l, c)}'   ;   msg2 = f'dl={self.fmtdl()} {cn=} {key=} keys={util.fmtl(list(mli.keys()))}'
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
    ###############################################################################################*#####################################################################################################
    def setChord(self, imap, cc, pos=0, dbg=0):
#        cc = self.plct2cc(p, l, c, 0)
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
    def on_mouse_release(self, x, y, button, mods, dbg=1):
        np, nl, ns, nc, nt = self.n   ;   nz = self.zzl()    ;  nc += nz    ;   ll = self.LL   ;   ww = self.width   ;   hh = self.height
        y0 = y     ;   y = self.height - y   ;   m = ns * nt + ll    ;   n = nl * m
        w = ww/nc  ;   h = hh/n              ;   d = int(y/h) - ll   ;   tlen = len(self.tabls)
        l = int(d/m)            ;  c = int(x/w) - nz         ;   t = d - (l * m)     ;      p = self.j()[P]
        text = self.tabls[self.cc].text if self.cc < tlen else ''
        if dbg: self.log(f'BGN {x=} {y=:4} {w=:6.2f} {h=:6.2f}', pos=1)
        if dbg: self.log(f'    {button=} {mods=} {self.cc=} {tlen=} {text=}', pos=1, file=2)
        if dbg: self.log(f'    {m=} {n=} {ll=} {nc=} {nz=} {d=}', pos=1)
        if dbg: self.log(f'    {p=}=i[P] {l=}=(d/m) {c=}=(x/w-nz) {t=}=(d-l*m)', pos=1)
        if dbg: self.log(f'    before plct={self.fplct(p, l, c, t)}', pos=1)
        self.moveTo(f'MOUSE RELEASE', p, l, c, t)
        if dbg: self.log(f'    after  plct={self.fplct(p, l, c, t)}', pos=1)
        if dbg: self.log(f'END {x=} {y0=:4} {ww=:6.2f} {hh=:6.2f}', pos=1)
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
        elif kbk == 'O' and self.isCtrlShift(mods):    self.toggleCursorMode('@^O', -1)
        elif kbk == 'O' and self.isCtrl(     mods):    self.toggleCursorMode('@ O', 1)
        elif kbk == 'P' and self.isCtrlShift(mods):    self.addPage(         '@^P', ins=0)
        elif kbk == 'P' and self.isCtrl(     mods):    self.addPage(         '@ P', ins=None)
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
        elif kbk == 'N' and self.isAltShift(mods):     self.setn_cmd(  '&^N', txt='')
        elif kbk == 'N' and self.isAlt(     mods):     self.setn_cmd(  '& N', txt='')
        elif kbk == 'P' and self.isAltShift(mods):     self.togglePage('&^P', 1)
        elif kbk == 'P' and self.isAlt(mods):          self.togglePage('& P', -1)
####################################################################################################################################################################################################
        elif kbk == 'B' and self.isAltShift(mods):     self.setFontParam('bold',      not self.fontBold,                             'fontBold')
        elif kbk == 'B' and self.isAlt(     mods):     self.setFontParam('bold',      not self.fontBold,                             'fontBold')
        elif kbk == 'C' and self.isAltShift(mods):     self.setFontParam('color',        (self.clrIdx + 1) % len(RGB),               'clrIdx')
        elif kbk == 'C' and self.isAlt(     mods):     self.setFontParam('color',        (self.clrIdx - 1) % len(RGB),               'clrIdx')
        elif kbk == 'I' and self.isAltShift(mods):     self.setFontParam('italic',    not self.fontItalic,                           'fontItalic')
        elif kbk == 'I' and self.isAlt(     mods):     self.setFontParam('italic',    not self.fontItalic,                           'fontItalic')
        elif kbk == 'N' and self.isAltShift(mods):     self.setFontParam('font_name',    (self.fontNameIndex + 1) % len(FONT_NAMES), 'fontNameIndex')
        elif kbk == 'N' and self.isAlt(     mods):     self.setFontParam('font_name',    (self.fontNameIndex - 1) % len(FONT_NAMES), 'fontNameIndex')
        elif kbk == 'S' and self.isAltShift(mods):     self.setFontParam('font_size',     self.fontSize      + 1,                    'fontSize') # )  % FS_MAX
        elif kbk == 'S' and self.isAlt(     mods):     self.setFontParam('font_size', max(self.fontSize      - 1, 1),                'fontSize') # )  % FS_MAX
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
    def move2LastTab(self, how, page=0, dbg=1):
        np, nl, ns, nc, nt = self.n    ;  p, l, s, c, t = self.j()  ;  i = p
        n = p * nl + l  ;  tp = nc * nt
        if page: tp *= nl  ;  n //= nl
        if dbg:    self.log(f'BGN {how} {page=} {self.fplct()} {i=:4} {n=} {tp=:3} {tp*n=:4} for({tp*(n+1)-1:4}, {tp*n-1:4}, -1)', pos=1)
        for i in range(tp*(n+1)-1, tp*n-1, -1):
            if not self.sobj.isFret(self.tabls[i].text): continue
            p, l, c, t = self.cc2plct(i, dbg=1)  ;  break
        self.moveTo(how, p, l, c, t, dbg=dbg)
        if dbg:    self.log(f'END {how} {page=} {self.fplct()} {i=:4} {n=} {tp=:3} {tp*n=:4} for({tp*(n+1)-1:4}, {tp*n-1:4}, -1)', pos=1)
    def move2FirstTab(self, how, page=0, dbg=1):
        np, nl, ns, nc, nt = self.n    ;  p, l, s, c, t = self.j()  ;  i = p
        n = p * nl + l  ;  tp = nc * nt
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
#        self.togglePage(how, -1, dbg=1)
        if dbg: self.log(f'END {how} {self.fmti()}', pos=1)

    def nextPage(self, how, dbg=1):
        p, l, c, t = self.j2()   ;   n = self.n[P] - 1
        if dbg: self.log(f'BGN {how} {self.fmti()}', pos=1)
        self.moveTo(how, p+1 if p<n else 0, l, c, t)
#        self.togglePage(how, 1, dbg=1)
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
        if self.cursor: self.moveCursor(ss, how)
        if dbg:    self.log(f'END {n=} {how}', pos=1)

    def _moveTo(self, p, l, c, t, n=0, dbg=1):
        if dbg: self.log(f'BGN {n=} plct={self.fplct(p, l, c, t)}', pos=1)
        np, nl, ns, nc, nt = self.n
        t2        =       n  + t
        c2        = t2 // nt + c
        l2        = c2 // nc + l
        p2        = l2 // nl + p
        self.i[T] = t2  % nt + 1
        self.i[C] = c2  % nc + 1
        self.i[L] = l2  % nl + 1
        self.i[P] = p2 + 1 # % np + 1
        if dbg: self.log(f'END {n=} {self.fmti()} plct={self.fplct(p, l, c, t)} plct2={self.fplct(p2, l2, c2, t2)}', pos=1)
    ####################################################################################################################################################################################################
    def autoMove(self, how, dbg=1):
        self.log(f'BGN {how}', pos=1)
        ha = 1 if self.hArrow == RIGHT else -1
        va = 1 if self.vArrow == DOWN  else -1
        nt, it = self.n[T], self.i[T]
        mmDist = ha * nt
        cmDist = va
        amDist = mmDist + cmDist
        if dbg: self.dumpCursorArrows(f'{self.fmtPos()}     {how} M={mmDist} C={cmDist} A={amDist}')
        if      self.csrMode == MELODY:                                     self.move(how, mmDist)
        elif    self.csrMode == CHORD:
            if   it == 1 and self.vArrow  == UP   and self.hArrow == RIGHT: self.move(how,   nt*2-1)
            elif it == 6 and self.vArrow  == DOWN and self.hArrow == LEFT:  self.move(how, -(nt*2-1))
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
            jcc  = self.n[T] * int(self.jumpStr)
            self.jumping = 0   ;   self.jumpStr = ''
            self.move(how, jcc - 1 - a * cc)
            self.log(f'{how} {txt=} {a=} {cc=} jt={self.jumpAbs} {jcc=} moved={jcc - 1 - a * cc} {self.fmti()}')
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
    def setLLStyle(self, cc, style, dbg=0):
        if not self.LL or not self.qclms: msg = f'SKIP {self.LL=} {len(self.qclms)=}'  ;  self.log(msg)  ;  self.quit(msg)
        p, l, c, t = self.cc2plct(cc)
        bold, italic = 0, 0   ;   np, nl, ns, nc, nt = self.n
        i = c + l * nc if self.qclms else 0
        if   style == NORMAL_STYLE:    bold = 0   ;  italic = 0
        elif style == CURRENT_STYLE:   bold = 1   ;  italic = 1
        elif style == SELECT_STYLE:    bold = 1   ;  italic = 1
        else: msg = f'ERROR Invalid style @ plct={self.fplct(p, l, c, t)} {i=} {style=}';  self.log(msg);  self.quit(msg)
        (bs, fs) = (0, 1) if style == NORMAL_STYLE else (1, 0)
#        bc = 'background_color'  ;  fc = 'color' # #
#        d = self.qclms[i].document # #
#        d.set_style(0, len(d.text), {fc: self.llcolor(i, Q)[fs], bc: self.llcolor(i, Q)[bs]}) # #
        self.setTC(self.qclms[i], self.llcolor(i, Q)[fs], self.llcolor(i, Q)[bs])
        self.qclms[i].bold   = bold
        self.qclms[i].italic = italic
        if dbg: self.log(f'{self.fmtPos()}     {i=} = {c=} + {l=} * {nc=} * {nt=} {style=} {bold=} {italic=} {cc=}')
    ####################################################################################################################################################################################################
    def llcolor(self, i, j, dbg=0):
        nc = self.n[C]  ;   n = 1
        mp = i % nc + n
        msg = f'{i=} {j=} {nc=} {i%nc=} {n=} {mp=}=i%nc+n {mp%10=}' if dbg else ''
        if j == Q and not mp % 10: # and i:
            self.log(  f'if   {msg} {self.k[R]=}') if dbg else None   ;   return self.k[R]
        else: self.log(f'else {msg} {self.k[j]=}') if dbg else None   ;   return self.k[j]
    ####################################################################################################################################################################################################
    def setTNIKStyle(self, k, nt, style, text='', blank=0):
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

    def _setTNIKStyle(self, tnik, color, style=0):
        (bgs, fgs) = (0, 1)  if style == NORMAL_STYLE else (1, 0)
#        d =  tnik.document   ;   d.set_style(0, len(d.text), {'color': color[fgs], 'background_color': color[bgs]}) # #
        self.setTC(tnik, color[fgs], color[bgs])
    @staticmethod
    def setTC(t, fgc, bgc=None): cm = {'color': fgc}  ;  cm |= {'background_color': bgc} if bgc else None  ;  d = t.document  ;  d.set_style(0, len(d.text), cm)
    ####################################################################################################################################################################################################
    def selectTabs(self, how, m=0, cn=None, dbg=1, dbg2=1):
        cc         = self.cursorCol()  ;  old = cn
        p, l, c, t = self.cc2plct(cc)
        if cn is None:      cn = self.cc2cn(cc) # self.plc2cn_(p, l, c)
        nt = self.n[T]  ;   k  = cn * nt   ;   style = SELECT_STYLE
        self.log(f'{m=} {old=} {cc=} {cn=} {nt} {k=} {self.fplct(p, l, c, t)}')
        if cn in self.smap: self.log(f'RETURN: {cn=} already in smap={util.fmtm(self.smap)}') if dbg2 else None   ;   return
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
        elif dbg:           self.log(f'{cn=} not found in smap={util.fmtm(self.smap)}')
        if m:               self.move(how, m)
        if dbg:             self.dumpSmap(f'END {how} {m=} {cn=} {cc=} {k=}')
    ####################################################################################################################################################################################################
    def copyTabs(self, how, dbg=1):
        self.dumpSmap(f'BGN {how}')   ;   nt = self.n[T]   ;   style = NORMAL_STYLE   ;   text = ''
        for k in list(self.smap.keys()):
            k *= nt
            if self.LL:  self.setLLStyle(k, style)
            text += self.setTNIKStyle(k, nt, style)
            if dbg: text += ' '
        if dbg:         self.log(f'{text=}')
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
        if self.SNAPS:  self.regSnap(f'{how}', 'DEL')
        self.resyncData = 1

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
                kt         = (cn + dk + n) % self.tpp
                p, l, c, t = self.cc2plct(kt)
                self.setDTNIK(text[n], kt, p, l, c, n, kk=1 if n==nt-1 else 0)
            if dbg:     self.log(f'{i=} {k=} {text=} {kk=} {dk=} {kt=}')
        self.log(f'clearing {len(self.smap)=}')   ;   self.smap.clear()
        self.dumpSmap(f'END {how} {kk=} {cc=} {cn=}={self.cc2cn(cc)} plct={self.fplct(p, l, c, t)}')
        if self.SNAPS:  self.regSnap(f'{how}', 'PAST')
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

    def swapTab(self, how, txt='', data=None, dbg=0, dbg2=1):  # e.g. c => 12 not same # chars asserts
        src, trg = self.swapSrc, self.swapTrg
        data = data or self.data
        if not self.swapping: self.swapping = 1
        elif txt.isalnum():
            if   self.swapping == 1:   src += txt;   self.log(f'    {how} {txt=} {self.swapping=} {src=} {trg=}')
            elif self.swapping == 2:   trg += txt;   self.log(f'    {how} {txt=} {self.swapping=} {src=} {trg=}')
            self.swapSrc, self.swapTrg = src, trg
        elif txt == '\r':
            self.log(f'    {how} {self.swapping=} {src=} {trg=}')
            if   self.swapping == 1 and not trg: self.swapping = 2;   self.log(f'{how} waiting {src=} {trg=}') if dbg else None   ;   return
            elif self.swapping == 2 and trg:     self.swapping = 0;   self.log(f'{how} BGN     {src=} {trg=}') if dbg else None
            np, nl, ns, nc, nt = self.n    ;     nc += self.zzl()
            cc0 = self.cursorCol()         ;     p0, l0, c0, t0 = self.cc2plct(cc0)   ;   self.log(f'BFR {cc0=} {p0=} {l0=} {c0=} {t0=}')
            blanks = self.tblanks          ;     blank = 1 if src in blanks and trg in blanks else 0
            if blank:
                for i in range(len(self.tabls)):
                    if self.tabls and self.tabls[i].text == src: self.tabls[i].text = trg
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
                                    if dbg2: self.log(f'Before data{self.fplc(p, l, c)}={text}')
                                    cc = self.plct2cc(p, l, c, t)   ;   self.setDTNIK(trg, cc, p, l, c, t, kk=1)
                                    if dbg2: self.log(f'After  data{self.fplc(p, l, c)}={text}')
            self.swapSrc, self.swapTrg = '', ''
            self.log(f'{how} END     {src=} {trg=}') if dbg else None
#                if dbg2: self.dumpTniks('SWAP')
#                self.moveTo(how, p0, l0, c0, t0)  ;  cc = self.cursorCol()  ;  self.log(f'AFT {cc0=} {p0=} {l0=} {c0=} {t0=} {cc=}')
            if self.SNAPS: self.regSnap(f'{how}', 'SWAP')
            self.resyncData = 1

    def insertSpace(self, how, txt='0', dbg=1):
        cc = self.cursorCol()   ;   c0 = self.cc2cn(cc)
        if not self.inserting: self.inserting = 1   ;    self.setCaption('Enter nc: number of cols to indent int')
        elif txt.isdecimal():  self.insertStr += txt
        elif txt == ' ' or txt == '/r':
            self.inserting = 0
            width = int(self.insertStr)
            tcs = sorted(self.cobj.mlimap)
            tcs.append(self.n[C] * self.n[L] - 1)
            tcs = [ t + 1 for t in tcs ]
            if dbg: self.log(f'BGN {how} Searching for space to insert {width} cols starting at colm {c0}')
            self.log(f'{util.fmtl(tcs, ll=1)} insertSpace', pfx=0)
            found, c1, c2 = 0, 0, None   ;   self.insertStr = ''
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
            self.shiftingTabs = 0   ;   nt = self.n[T]
            for cn, v in self.smap.items():
                cc = self.cn2cc(cn)   ;   p, l, c, r = self.cc2plct(cc, dbg=0)
                self.log(f'{cc=} {cn=} {v=} text={self.smap[cn]}')
                for t in range(nt):
                    text = self.smap[cn][t]    ;    kt = cc + t    ;    fn = 0   ;   ntones = util.NTONES * 2
                    if self.sobj.isFret(text):
                        fn = self.afn(str((self.tab2fn(text) + self.shiftSign * self.tab2fn(nf)) % ntones))  ;  self.log(f'{cc=} {cn=} {t=} {text=} {nf=} {fn=} {self.shiftSign=}')
                    if fn and self.sobj.isFret(fn):  self.setDTNIK(fn, kt, p, l, c, t, kk=1 if t==nt-1 else 0)
            self.shiftSign  = 1
            self.resyncData = 1
            self.unselectAll('shiftTabs()')
        self.dumpSmap(f'END {how} {self.shiftingTabs=} {nf=} {self.shiftSign=}')

    def setn_cmd(self, how, txt='', dbg=1):
        if not self.settingN: self.settingN = 1   ;  self.setNtxt = '' ;  self.log(f'BGN {how} {txt=} {self.settingN=} {self.setNvals=}') if dbg else None
        elif txt.isdecimal(): self.setNtxt += txt                      ;  self.log(   f'Concat {txt=} {self.settingN=} {self.setNvals=}') if dbg else None
        elif txt == ' ':      self.setNvals.append(int(self.setNtxt))  ;  self.log(   f'Append {txt=} {self.settingN=} {self.setNvals=}') if dbg else None   ;  self.setNtxt = ''
        elif txt == 'Q':      self.settingN = 0  ;  self.log(f'Cancel {txt=} {self.settingN=} {self.setNvals=}') if dbg else None
        elif txt == '\r':
            self.settingN = 0   ;   old = self.n
            self.setNvals.append(int(self.setNtxt))
            if len(self.setNvals) == 4:
                self.n[:2] = self.setNvals[:2]   ;  self.n[3:] = self.setNvals[2:]
            self.log(f'Setting {old=} {self.n=}')
            self.log(f'END {how} {txt=} {self.settingN=} {self.setNvals=}')
    ####################################################################################################################################################################################################
    def toggleFlatSharp(self, how, dbg=1):  #  page line colm tab or select
        t1 = util.Note.TYPE  ;  t2 = (util.Note.TYPE + 1) % 2    ;   util.Note.setType(t2)
        self.log(  f'BGN {how} {t1=} {util.Note.TYPES[t1]} => {t2=} {util.Note.TYPES[t2]}')
        s = self.ss2sl()[0]  ;  np, nl, ns, nc, nt = self.i
        tniks, j, k, tobj = self.tnikInfo(0, 0, s, 0, 0, why=how)
        for i in range(len(tniks)):
            text = ''  ;   sn = i % nt
            if   self.notes: text = self.notes[i].text
            elif self.kords and self.tabls:
                tabtxt = self.tabls[i].text
                text   = self.sobj.tab2nn(tabtxt, sn) if self.sobj.isFret(tabtxt) else self.tblank
            if len(text) > 1:
                cc = i * ns
                p, l, c, t = self.cc2plct(cc)   ;   old = text
                cn = self.cc2cn(cc)
                if   text in util.Note.F2S: text = util.Note.F2S[text]
                elif text in util.Note.S2F: text = util.Note.S2F[text]
                self.notes[i].text = text
                if dbg: self.log(f'{sn=} {cn=} {cc=} {i=} {old} => {text} {self.notes[i].text=} {self.fplct(p, l, c, t)}')
                if self.kords:
                    imap = self.getImap(p, l, c, dbg2=1)
                    self.setChord(imap, i, pos=1, dbg=1)
        self.log(  f'END {how} {t1=} {util.Note.TYPES[t1]} => {t2=} {util.Note.TYPES[t2]}')
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
        if cn not in mks: msg = f'ERROR: {cn=} not in {util.fmtl(mks)=}'   ;   self.log(msg)   ;   self.quit(msg)
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
        if not self.ikeys and not self.kords: msg +=  'ERROR: Both ikeys and chords are Empty '
        if cn not in mli:                     msg += f'ERROR: {cn=} not in mks={util.fmtl(list(mli.keys()))}'
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
    def togglePage(self, how, dp=1, dbg=1):
        pA = self.j()[P] if dbg else None
        self.toggleVisible(how, self.j()[P])
        if dbg: pB = self.j()[P]    ;   self.log(f'{pA=} {pB=}, {self.fmtJ1()}, {self.fmtJ2()}', pfx=0)
        self.dumpVisible()  ;   self.dumpVisible2()
        self.i[P] = ((self.j()[P] + dp) % self.n[P]) + 1
        if dbg: pA = self.j()[P]
        self.toggleVisible(how, self.j()[P])
        if dbg: pB = self.j()[P]    ;   self.log(f'{pA=} {pB=}, {self.fmtJ1()}, {self.fmtJ2()}', pfx=0)
        self.dumpVisible()  ;   self.dumpVisible2()
        if self.SNAPS and dbg:  self.regSnap(how, f'TPag{self.i[P]}')
        self.resizeTniks(dbg)
    ####################################################################################################################################################################################################
    def dumpVisible(self):
        nsum = 0  ;  j = 0  ;  lsum = 0  ;  nmax = 0  ;  a = B*10  ;  b = B*8  ;  c = B*7  ;  d = B*6  ;  e = B*5
        for j in range(len(self.visib) - 1):
            vl = []   ;   n = 0
            for w in self.visib[j]:
                vl.append(str(int(w)))      ;  lsum += 1   ;    n += 1    if w           else 0
            v = ''.join(vl)  ;  l = len(v)  ;  nsum += n   ;  nmax = nsum if nsum > nmax else nmax
            if l:                              self.log(self.fVisible(n, j, l, v), pfx=0)
        v = ''.join([ f'{a if not i else b if i//10 < 1 else c if i//10 < 10 else d if i//10 < 100 else e}{10+i*10}' for i in range(nmax//10) ])
        j += 1   ;  n = nsum  ;  l = lsum   ;  self.log(self.fVisible(n, j, l, v), pfx=0)
    @staticmethod
    def fVisible(n, j, l, v): return f'{n:4}{jTEXTS[j][0]}{l:<4}{v}'
    def dumpVisible2(self):
#        consume(consume(self.log(f'{int(self.E[j][i].visible)}', pfx=0, end=' ') for i in range(len(self.E[j]))) for j in range(len(self.E)))
#        [ [ self.log(f'{int(self.E[j][i].visible)}', pfx=0, end=' ') for i in range(len(self.E[j]))] for j in range(len(self.E)) ]
        for j in range(len(self.E)):
            for i in range(len(self.E[j])):
                self.log(f'{int(self.E[j][i].visible)}', pfx=0, end='')
            if len(self.E[j]): self.log(pfx=0)
    def fVis(self): return f'{util.fmtl([ i + 1 if p.visible else B for i, p in enumerate(self.pages) ])}'
    ####################################################################################################################################################################################################
    def toggleCursorMode(self, how, m):
        self.log(f'BGN {how} {self.csrMode=} = {CSR_MODES[self.csrMode]=}')
        self.csrMode  = (self.csrMode + m) % len(CSR_MODES)
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
    def dumpCursorArrows(self, how): cm, ha, va = self.csrMode, self.hArrow, self.vArrow  ;  self.log(f'{how} csrMode={cm}={CSR_MODES[cm]:6} hArrow={ha}={HARROWS[ha]:5} vArrow={va}={VARROWS[va]:4}')
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
        self.dumpBlanks()
        for i in range(len(self.tabls)):
            self.tabls[i].text = self.tblank
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
        if dbg2:    self.log(f'{SNAP_NAME=} {WHY}', file=2)
        self.snapId += 1
    ####################################################################################################################################################################################################
    def deleteGlob(self, g, why=''):
        self.log(f'deleting {len(g)} files from glob {why=}')
        for f in g:
            self.log(f'{f}')
            os.system(f'del {f}')

    def getFilePath(self, seq=0, fdir='files', fsfx='.txt', dbg=0):
        if seq and not self.LOG_ID:
            fdir      += '/'
            self.log(f'{fdir=} {fsfx=}')
            pathlib.Path(fdir).mkdir(parents=True, exist_ok=True)
            fGlobArg   = str(BASE_PATH / fdir / BASE_NAME) + '.*' + fsfx
            fGlob      = glob.glob(fGlobArg)
            self.log(f'{fGlobArg=}')
            self.LOG_ID = 1 + self.getFileSeqNum(fGlob, fsfx)
            fsfx        = f'.{self.LOG_ID}{fsfx}'
            if dbg:     self.log(f'fGlob={util.fmtl(fGlob)}', pfx=0)
            self.log(f'{fsfx=}')
        return util.getFilePath(BASE_NAME, BASE_PATH, fdir=fdir, fsfx=fsfx, file=LOG_FILE)

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
    def log(self, msg='', pfx=1, pos=0, file=None, flush=False, sep=',', end='\n'):
        so = 0 if file is None or file == 1 else 1
        file = sys.stdout if file == 1 else LOG_FILE
        if   pos: msg = f'{self.fmtPos()} {msg}'
        util.slog(msg, pfx, file, flush, sep, end, so)
    ####################################################################################################################################################################################################
    def quit(self, why='', error=1, save=1, dbg=1): #, dbg2=1):
        hdr1 = self.fTnikHdr(1)   ;   hdr0 = self.fTnikHdr(0)  ;  self.log(f'{hdr1}', pfx=0, file=2)   ;   self.log(f'{hdr0}', pfx=0, file=2)
        self.log(util.QUIT_BGN, pfx=0, file=2)   ;   util.dumpStack(inspect.stack())    ;   self.log(util.QUIT, pfx=0, file=2)
        self.dumpTniksSfx(why)
        if not error:      util.dumpStack(util.MAX_STACK_FRAME, file=LOG_FILE)
        self.log(f'BGN {why} {error=} {save=}', file=2)           ;   self.log(util.QUIT, pfx=0, file=2)
        self.dumpArgs()
        if not error:
            if dbg:  self.dumpStruct(why)
            if save: self.saveDataFile(why, self.dataPath1)
            if dbg:  self.A_transposeData(dump=dbg) if self.TRANSPOSE_A else self.OLD_transposeData()
            if dbg:  self.cobj.dumpMlimap(why)
        if self.SNAPS:                self.snapshot(f'quit {error=} {save=}', 'QUIT')
        self.log(f'END {why} {error=} {save=}', file=2)           ;   self.log(util.QUIT_END, pfx=0, file=2)
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
    ####################################################################################################################################################################################################

# Global Functions BGN
########################################################################################################################################################################################################
def fri(f): return int(math.floor(f + 0.5))
########################################################################################################################################################################################################
def dumpGlobals():
    util.slog(f'BASE_NAME = {BASE_NAME}', file=LOG_FILE)
    util.slog(f'argv      = {util.fmtl(sys.argv, ll=1)}', file=LOG_FILE)
    util.slog(f'PATH      = {PATH}', file=LOG_FILE)
    util.slog(f'BASE_PATH = {BASE_PATH}', file=LOG_FILE)
########################################################################################################################################################################################################
def initRGB(dbg=1):
    if dbg:
        s = f'{B*7}'  ;  t = f'{s}RGB '
        o = [ f' {o}' for o in range(len(OPC)) ]
        util.slog(f'RGB{s}{util.fmtl(o, w="3",d1="")}{t}Diffs  {t}Steps', pfx=0, file=LOG_FILE)
    _initRGB('FSH', (255,   0, 255))  # 0
    _initRGB('PNK', (255, 128, 192))  # 1
    _initRGB('RED', (255,   0,   0))  # 2
    _initRGB('RST', (255,  96,   0))  # 3
    _initRGB('PCH', (255, 160, 128))  # 4
    _initRGB('ORN', (255, 176,   0))  # 5
    _initRGB('YLW', (255, 255,   0))  # 6
    _initRGB('LIM', (160, 255,   0))  # 7
    _initRGB('GRN', (  0, 255,   0))  # 8
    _initRGB('TRQ', (  0, 255, 192))  # 9
    _initRGB('CYA', (  0, 255, 255))  # 10
    _initRGB('IND', (  0, 180, 255))  # 11
    _initRGB('BLU', (  0,   0, 255))  # 12
    _initRGB('VLT', (128,   0, 255))  # 13
    _initRGB('GRY', (255, 255, 255))  # 14
    _initRGB('CL1', ( 13,  15, 255))  # 15
    _initRGB('CL2', (255, 128,   0))  # 16
    _initRGB('CL3', (250, 65,  190))  # 17
    _initRGB('CL4', (255, 128, 255))  # 18
    return RGB.keys()
########################################################################################################################################################################################################
def _initRGB(key, rgb, dv=32, n=None, dbg=2):
    colors = []  ;  lrgb, lopc = len(rgb), len(OPC)  ;  msg, msgR, msgG, msgB = '', [], [], []  ;  n = n + 1 if n is not None else lopc  ;  opc, color = None, None
    diffs  = [ rgb[i] - rgb[i]/dv for i in range(lrgb) ]
    steps  = [ diffs[i]/(n-1)     for i in range(lrgb) ]
    if dbg: msg = f'{key:3}:   O=['
    for j in range(n):
        clrs = []
        if dbg > 2: util.slog(f'{key:4} {util.fmtl(rgb, w="3")} {opc=:2} {OPC[opc]:3} {dv=} {n=} {util.fmtl(diffs, w=".2f")} ', end='', file=LOG_FILE);  util.slog(f'{util.fmtl(steps, w=".2f")}', pfx=0, file=LOG_FILE)
        for opc in range(lopc):
            if dbg: msg += f'{OPC[opc]:3} ' if not j else ''
            color = list([ fri(rgb[i]/dv + j*steps[i]) for i in range(lrgb) ])  ;  color.append(OPC[opc])  ;  clrs.append(tuple(color))
            if   dbg > 1:       util.slog(f'{j:2} {key:4} {util.fColor(color)}', pfx=0, end=' ', file=LOG_FILE)
        util.slog(pfx=0, file=LOG_FILE)
        if dbg: msgR.append(color[0])  ;  msgG.append(color[1])  ;  msgB.append(color[2])
        colors.append(clrs)
    if dbg:
        util.slog( f'{msg[:-1]}] {util.fmtl(diffs, w="5.1f")} {util.fmtl(steps, w="4.1f")}', pfx=0, file=LOG_FILE)  ;  msgs = [msgR, msgG, msgB]  ;  rgb = 'RGB'
        for i, msg in enumerate(msgs): util.slog(f'       {rgb[i]}={util.fmtl(msg, w="3")}', pfx=0, file=LOG_FILE)
    global RGB  ;  RGB[key] = colors
    return list(RGB.keys())
########################################################################################################################################################################################################
# Global Functions END

# Globals BGN
########################################################################################################################################################################################################
PATH      = pathlib.Path.cwd() / sys.argv[0]
BASE_PATH = PATH.parent
BASE_NAME = BASE_PATH.stem
SNAP_DIR  = 'snaps'
SNAP_SFX  = '.png'
LOG_FILE  = None
########################################################################################################################################################################################################
B                     = ' '
FIN                   = [1, 1, 1, 2, 1]
FNTP                  = [5, 4, 3, 3, 3]
LBL                   = pygtxt.Label
SPR                   = pygsprt.Sprite
RGB                   = cOd() if CODS else {}
P, L, S, C            =  0,  1,  2,  3
T, N, I, K            =  4,  5,  6,  7
R, Q, H, V            =  8,  9, 10, 11
Z, U, A, D            = 12, 13, 14, 15
TT, NN, II, KK        =  0,  1,  2,  3
C1,  C2               =  0,  1
CSR_MODES             = ['MELODY', 'CHORD', 'ARPG']
HARROWS, VARROWS      = ['LEFT', 'RIGHT'], ['DOWN', 'UP']
MELODY, CHORD, ARPG   =  0, 1, 2
LEFT, RIGHT, DOWN, UP =  0, 1, 0, 1
NORMAL_STYLE, SELECT_STYLE, CURRENT_STYLE, COPY_STYLE = 0, 1, 2, 3
#           0        1        2        3        4        5        6        7        8        9        10      11       12       13       14       15       16
JTEXTS = ['Page',  'Line',  'Sect',  'Colm',  'Tab ',  'Note',  'IKey',  'Kord',  'RowL',  'QClm',  'HCrs',  'View',  'ZClm',  'UNum',  'ANam',  'DCpo',  'TNIK']
jTEXTS = ['pages', 'lines', 'sects', 'colms', 'tabs ', 'notes', 'ikeys', 'Kords', 'rowls', 'qclms', 'hcsrs', 'views', 'zclms', 'unums', 'anams', 'dcpos', 'tniks']
JFMT   = [  1,       2,       2,       3,       4,       4,       4,       4,       2,       3,       1,       1,       2,       2,       2,       2,       4]
#JFMT   = [  2,       3,       3,       6,       6,       6,       6,       6,       3,       5,       1,       1,       3,       3,       3,       4,       7]
#          0   1   2   3   4   5   6   7    8    9   10   11   12   13   14   15   16   17
OPC    = [ 0, 15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165, 170, 195, 210, 225, 240, 255 ]
FONT_SCALE =  14/18  # 14pts/18pix
FONT_DPIS  = [ 72, 78, 84, 90, 96, 102, 108, 114, 120 ]
FONT_NAMES = [ 'Lucida Console', 'Times New Roman', 'Helvetica', 'Arial', 'Courier New', 'Century Gothic', 'Bookman Old Style', 'Antique Olive' ]
########################################################################################################################################################################################################
# Globals END

# Log and Main BGN
########################################################################################################################################################################################################
prevPath = util.getFilePath(BASE_NAME, BASE_PATH, fdir='logs', fsfx='.blog')
LOG_PATH = util.getFilePath(BASE_NAME, BASE_PATH, fdir='logs', fsfx='.log')
if LOG_PATH.exists():     util.copyFile(LOG_PATH, prevPath, LOG_FILE)
with open(   str(LOG_PATH), 'w', encoding='utf-8')  as      LOG_FILE:
    util.slog(f'{sys.argv[0]}', pfx=0, so=2,           file=LOG_FILE)
    util.slog(f'argv={util.fmtl(sys.argv[1:])}', so=2, file=LOG_FILE)
    # 0   1    2    3    4    5    6    7    8    9   10   11   12   13   14   15   16   17   18
    FSH, PNK, RED, RST, PCH, ORN, YLW, LIM, GRN, TRQ, CYA, IND, BLU, VLT, GRY, CL1, CL2, CL3, CL4 = initRGB()
    def main():
        util.slog(f'{LOG_PATH=}',      file=LOG_FILE)
        util.slog(f'{LOG_FILE.name=}', file=LOG_FILE)
        _ = Tabs()
        ret = pyglet.app.run()
        print(f'{ret=}')
    ########################################################################################################################################################################################################
    if __name__ == '__main__':
        main()
########################################################################################################################################################################################################
# Log and Main END
