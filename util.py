"""util.py module.  class list: [DSymb, Notes, Strings, Test]."""
import sys, os, inspect, pathlib
from collections import Counter
from collections import OrderedDict as cOd

B                = ' '
M                = -7
P                = 7
OIDS             = 0
LOG_FILE         = None
MIN_IVAL_LEN     = 1
MAX_STACK_DEPTH  = 0
MAX_STACK_FRAME  = inspect.stack()
INIT             = '###   Init   ###'     * 13
QUIT_BGN         = '###   BGN Quit   ###' * 10
QUIT             = '###   Quit   ###'     * 13
QUIT_END         = '###   END Quit   ###' * 10
#STFILT = ['log', 'dumpGeom', 'resetJ', 'dumpJs', 'dumpImap', 'dumpSmap', 'dumpCursorArrows', '<listcomp>', 'dumpLimap2', 'dumpTniksPfx', 'dumpTniksSfx']
STFILT = ['log', 'tlog', 'fmtl', 'fmtm', 'dumpGeom', 'resetJ', 'dumpJs', 'dumpImap', 'dumpSmap', 'dumpCursorArrows', '<listcomp>', 'dumpLimap2', 'dumpTniksPfx', 'dumpTniksSfx', 'fmtXYWH', 'kbkInfo', 'dumpCrs', 'fCrsCrt'] # , 'dumpView', 'dumpLbox', 'dumpRect']
########################################################################################################################################################################################################
def t2sign(t=0):    return ' ' if not t else '+' if t==1 else ''
def js2sign(l):     return [ '-' if k<0 else '+' if k>0  else ' ' for k in l ]

def init(file, oid):
    global LOG_FILE  ;  LOG_FILE = file  ;  global OIDS  ;  OIDS = oid
    dumpData()

def dumpData(w=2, d='', p=0):
    slog('BGN')     ;  x = f'{w}x'  ;  u = f'>{w}'  ;  y = f'<{w}x'  ;  z = f'<{w}'  ;  q = f'>{w}x'
    slog(f'[F2S:     {len(Notes.F2S):2}] [{fmtm(Notes.F2S, w=w,       d=d)}]', p=p)
    slog(f'[S2F:     {len(Notes.S2F):2}] [{fmtm(Notes.S2F, w=w,       d=d)}]', p=p)
    slog(f'[F3S:     {len(Notes.F3S):2}] [{fmtm(Notes.F3S, w=u, wv=z, d=d)}]', p=p)
    slog(f'[S3F:     {len(Notes.S3F):2}] [{fmtm(Notes.S3F, w=u, wv=z, d=d)}]', p=p)
    slog(f'[I2F:     {len(Notes.I2F):2}] [{fmtm(Notes.I2F, w=x, wv=w, d=d)}]', p=p)
    slog(f'[I2S:     {len(Notes.I2S):2}] [{fmtm(Notes.I2S, w=x, wv=w, d=d)}]', p=p)
    slog(f'[I3F:     {len(Notes.I3F):2}] [{fmtm(Notes.I3F, w=x, wv=w, d=d)}]', p=p)
    slog(f'[I3S:     {len(Notes.I3S):2}] [{fmtm(Notes.I3S, w=x, wv=w, d=d)}]', p=p)
    slog(f'[I2N[-1]: {len(Notes.I2N[-1] ):2}] [{fmtm(Notes.I2N[-1], w=q, wv=z, d=d)}]', p=p)
    slog(f'[I2N[ 1]: {len(Notes.I2N[ 1] ):2}] [{fmtm(Notes.I2N[ 1], w=q, wv=z, d=d)}]', p=p)
    slog(f'[I3N[-1]: {len(Notes.I3N[-1] ):2}] [{fmtm(Notes.I3N[-1], w=q, wv=z, d=d)}]', p=p)
    slog(f'[I3N[ 1]: {len(Notes.I3N[ 1] ):2}] [{fmtm(Notes.I3N[ 1], w=q, wv=z, d=d)}]', p=p)
    slog(f'[I2V:     {len(Notes.I2V ):2}] [{fmtm(Notes.I2V, w=x, wv=w, d=d)}]', p=p)
    slog(f'[V2I:     {len(Notes.V2I ):2}] [{fmtm(Notes.V2I, w=u, wv=y, d=d)}]', p=p)
    slog(f'[N2I:     {len(Notes.N2I ):2}] [{fmtm(Notes.N2I, w=u, wv=y, d=d)}]', p=p)
    dumpNF()
    dumpND()
    dumpKSH()
    dumpKSV()
    slog('END')
########################################################################################################################################################################################################
def dumpNF():
    slog(f'Note Frequencies in Hertz')   ;   msg = f'Piano Note Index{B*43}'  ;  nm = Notes.MAX_IDX
    slog(f'{msg}{fmtl([ i+1 for i in range(88) ], w="^5")}', p=0)
    slog(f'Index{fmtl([ i+1 for i in range(nm) ], w="^5")}', p=0)
    dumpFreqs(432)  ;  dumpFreqs(440)
    slog(f'Flats{fmtl(list(FLATS),                w="^5")}', p=0)
    slog(f'Shrps{fmtl(list(SHRPS),                w="^5")}', p=0)

def dumpFreqs(r=440):
    fs = FREQS if r == 440 else FREQS2   ;   g = []   ;   ref = 'A 440' if r == 440 else  'A 432'
    for f in fs:       g.append(f'{f:5.2f}' if f < 100 else f'{f:5.1f}' if f < 1000 else f'{f:5.0f}')
    ' '.join(f'{g}')   ;   slog(f'{ref}{fmtl(g, w=5)} Hz', p=0)
########################################################################################################################################################################################################
def dumpND():
    slog(f'I  F  S  IV   Notes Table {len(ND)}', p=0)
    for i in range(len(ND)):   slog(f'{i:x} {fmtl(ND[i], w=2)}', p=0)
########################################################################################################################################################################################################
def dumpKSV(ksd=None, p=0):
    dmpKSVHdr()   ;   ksd = KSD if ksd is None else ksd
    keys = sorted(ksd.keys())
    for k in keys:    slog(fmtKSK(k), p=p)

def dmpKSVHdr(t=0):
    k = 2*P+1 if t == 0 else M if t == Notes.FLAT else P if t == Notes.SHRP else 1   ;   sign = t2sign(t)
    slog(f'KS Type  N  I   Flats/Sharps Naturals  F/S/N Indices  Ionian Indices   Ionian Note Ordering   Key Sig Table {sign}{k}', p=0)

def dumpKSH(ksd=None, p=0, v=0, w=2, u='<', d=''):
    flats = 'Flats'     ;    shrps = 'Sharps'  ;   slog(f'{flats:^20} KS {shrps:^20}', p=p)     ;  v = B*v if v and Notes.TYPE==Notes.FLAT else ''
    ksd = KSD if ksd is None else ksd          ;   keys = sorted(ksd.keys())  ;  w = f'{u}{w}'  ;  x = f'{w}x'
    _ = js2sign(keys)   ;   _ = '  '.join(_)   ;   slog(f'{v}{_}', p=p)       ;  slog(f'{v}{fmtl(list(map(abs, keys)), w=w, d=d)}', p=p)
    _ = [ ksd[k][0][0]    for k in keys ]      ;   slog(f'{v}{fmtl(_, w=x, d=d)}', p=p)
    _ = [ ksd[k][0][1]    for k in keys ]      ;   slog(f'{v}{fmtl(_, w=w, d=d)}', p=p)
    f = [ ksd[M][2][f]    for f in range(len(ksd[M][2])-1, -1, -1) ]
    s = [ ksd[P][2][s]    for s in range(len(ksd[P][2]))           ]          ;  slog(f'{v}{fmtl(f, w=w, d=d)}    {fmtl(s, w=w, d=d)}', p=p)
    f = [ f for f in reversed(ksd[M][1]) ]  ;  s = [ s for s in ksd[P][1] ]   ;  slog(f'{v}{fmtl(f, w=x, d=d)}    {fmtl(s, w=x, d=d)}', p=p)
########################################################################################################################################################################################################
def nic2KS(nic, dbg=0):
    dumpKSV()   ;   dumpKSH()   ;   dumpNic(nic)
    iz  = []          ;     t  = Notes.TYPE   ;   nt = Notes.TYPES[t]
    ks  = KSD[M][KIS]    if t == Notes.FLAT else KSD[P][KIS]
    for i in ks:
        if i in nic:     iz.append(f'{i:x}')
        else:            break
    k   = -len(iz)       if t == Notes.FLAT else len(iz)
    s   = t2sign(t)      if iz else '?'
    n   = KSD[k][KIM][1] if iz else '??'
    i   = KSD[k][KIM][0]
    ns  = KSD[k][KMS]
    slog(fmtKSK(k))      if dbg else None
    return s, k, nt, n, i, ns, Scales.majIs(i)

def dumpNic(nic): #fix me
    slog(f'{fmtl([ f"{i:x}:{Notes.I2F[i]:2}:{nic[i]}" for i in nic.keys() ])}')
    slog(f'{fmtl([ f"{i:x}:{Notes.I2S[i]:2}:{nic[i]}" for i in nic.keys() ])}')
    slog(f'{fmtl([ f"{i:x}:{Notes.I2F[i]:2}:{nic[i]}" if i in nic and nic[i] > 0 else None for i in KSD[M][KIS] ])}')
    slog(f'{fmtl([ f"{i:x}:{Notes.I2F[i]:2}:{nic[i]}" if i in nic and nic[i] > 0 else None for i in KSD[P][KIS] ])}')
########################################################################################################################################################################################################
def initKSD(ks, t):
    if     t == -1:   i = 0  ;  j = 6   ;  s = M
    else:             i = 0  ;  j = 10  ;  s = P
    iz1 = [ (j + k * s) % Notes.NTONES for k in range(1, 1+abs(s)) ]
    ms1 = [ Notes.name(j, t)           for j in iz1 ]
    iz2 = list(iz1)          ;         ms2 = list(ms1)
    slog(f'{t=} {i=} {j=} {s=} {fmtl(iz2)=} {fmtl(ms2)=}', p=0)   ;   j += t
    for  k in range(0, t + s, t):
        ak = abs(k)
        m  =   Notes.name(i, t, 1 if ak >= 5 else 0)
        n  =   Notes.name(j, t, 1 if ak >= 5 else 0)
        if ak >= 1:   ms2[ak-1] = n  ;  iz2[ak-1] = j   ;  ms = list(ms2)  ;  iz = list(iz2)
        else:                                              ms = list(ms2)  ;  iz = list(iz2)
        jz = Scales.majIs(i)    ;    im  = [i, m]
        ns = [ Notes.name(j, t, 1 if ak >= 5 else 0) for j in jz ]
        ks[k]  =  [ im, iz, ms, jz, ns ]
        slog(fmtKSK(k), p=0)
        i  =   Notes.nextIndex(i, s)
        j  =   Notes.nextIndex(j, s)
    return ks
########################################################################################################################################################################################################

class DSymb(object):
    SYMBS = {'X': 'mute', '/': 'slide', '\\': 'bend', '+': 'hammer', '~': 'vibrato', '^': 'tie', '.': 'staccato', '_': 'legato', '%': 'repeat', '|': 'bar', '[': 'groupL', ']': 'groupR'}
########################################################################################################################################################################################################

class Scales(object):
    MajorIs = [ 0, 2, 4, 5, 7, 9, 11 ]
    @classmethod
    def majIs(cls, i):  return [ (i + j) % Notes.NTONES for j in cls.MajorIs ]

########################################################################################################################################################################################################

class Modes(object):
    IONIAN, DORIAN, PHRYGIAN, LYDIAN, MIXOLYDIAN, AEOLIAN, LOCRIAN = range(7)
    NAMES = [ 'IONIAN', 'DORIAN', 'PHRYGIAN', 'LYDIAN', 'MIXOLYDIAN', 'AEOLIAN', 'LOCRIAN' ]
    TYPES = [  IONIAN,   DORIAN,   PHRYGIAN,   LYDIAN,   MIXOLYDIAN,   AEOLIAN,   LOCRIAN  ]

########################################################################################################################################################################################################

class Strings(object):
    aliases = {'GUITAR_6_STD':    cOd([('E2', 28), ('A2' , 33), ('D3', 38), ('G3', 43), ('B3' , 47), ('E4', 52)]),
               'GUITAR_6_DROP_D': cOd([('D2', 26), ('A2' , 33), ('D3', 38), ('G3', 43), ('B3' , 47), ('E4', 52)]),
               'GUITAR_7_STD':    cOd([('E2', 28), ('Ab2', 32), ('C3', 36), ('E3', 40), ('Ab3', 44), ('C4', 48), ('E4', 52)])
              }
    def __init__(self, alias=None):
        if alias is None: alias = 'GUITAR_6_STD'
        self.stringMap          = self.aliases[alias]
        self.stringKeys         = list(self.stringMap.keys())
        self.stringNames        = ''.join(reversed([ str(k[0])  for k in            self.stringKeys ]))
        self.stringNumbs        = ''.join(         [ str(r + 1) for r in range(len(self.stringKeys)) ])
        self.stringCapo         = ''.join(         [ '0'        for _ in range(len(self.stringKeys)) ])
        self.strLabel           = 'STRING'
        self.cpoLabel           = ' CAPO '
        slog( f'stringMap   = {fmtm(self.stringMap)}')
        slog( f'stringKeys  = {fmtl(self.stringKeys)}')
        slog( f'stringNames =      {self.stringNames}')
        slog( f'stringNumbs =      {self.stringNumbs}')
        slog( f'stringCapo  =      {self.stringCapo}')
        slog( f'strLabel    =      {self.strLabel}')
        slog( f'cpoLabel    =      {self.cpoLabel}')

    @staticmethod
    def tab2fn(t, dbg=0): fn = int(t) if '0'<=t<='9' else int(ord(t)-87) if 'a'<=t<='o' else None  ;  slog(f'tab={t} fretNum={fn}') if dbg else None  ;  return fn
    @staticmethod
    def isFret(t):      return   1    if '0'<=t<='9'          or            'a'<=t<='o' else 0

    def nStrings(self): return len(self.stringNames)

    def fn2ni(self, fn, s, dbg=0):
        strNum = self.nStrings() - s - 1   # Reverse and zero base the string numbering: str[1 ... numStrings] => s[(numStrings - 1) ... 0]
        k      = self.stringKeys[strNum]
        i      = self.stringMap[k] + fn
        if dbg: slog(f'fn={fn} s={s} strNum={strNum} k={k} i={i} stringMap={fmtm(self.stringMap)}')
        return i

    def tab2nn(self, tab, s, nic=None, dbg=1):
        fn  = self.tab2fn(tab)
        i   = self.fn2ni(fn, s)   ;   nict = ''
        j   = i % Notes.NTONES
        if  nic is None:    nic = Counter()
        else:
            nic[j]    += 1
            if nic[j] == 1:
                if j in (0, 4, 5, 11):
                    ks = nic2KS(nic)  ;  k = ks[KSK]  ;  slog(f'{fmtKSK(k)}', f=2)
                    if     j  == 11:     updNotes(j, 'Cb', 'B', Notes.TYPE, 0)
                    if     j  ==  5:     updNotes(j, 'F', 'E#', Notes.TYPE, 0)
                    elif   j  ==  4:     updNotes(j, 'Fb', 'E', Notes.TYPE, 0)
                    elif   j  ==  0:     updNotes(j, 'C', 'B#', Notes.TYPE, 0)
                nict = f'nic[{j:x}]={nic[j]} '        ;  slog(f'adding {nict}', f=2)
        name = Notes.name(i)
        if dbg and nict:    slog(f'tab={tab} fn={fn:2} s={s} i={i:2} j={j:x} name={name:2} {nict}{fmtm(nic, w="x")}', f=2)
        return name
########################################################################################################################################################################################################
class Notes2(object): #0   :1         :2         :3         :4         :5         :6         :7         :8         :9         :a         :b     #  2    7 9  #
    F2S = {            'Db':'C#',            'Eb':'D#',                       'Gb':'F#',            'Ab':'G#',            'Bb':'A#'            } # 1 3  6 8 a # 5/9
    S2F = {            'C#':'Db',            'D#':'Eb',                       'F#':'Gb',            'G#':'Ab',            'A#':'Bb'            } # 1 3  6 8 a # 5/9
    F3S = { 'C' :'B#',                                  'Fb':'E' , 'F' :'E#',                                                        'Cb':'B'  } #0   45     b# 4/9
    S3F = { 'B#':'C' ,                                  'E' :'Fb', 'E#':'F' ,                                                        'B' :'Cb' } #0   45     b# 4/9
    V2I = {  'R':0,      'm2':1,  'M2':2,    'm3':3,    'M3':4,    'P4':5,    'b5':6,    'P5':7,    'm6':8,    'M6':9,    'm7':10,   'M7':11   } # 8/12/16
    I2V = {   0:'R',      1:'m2',  2:'M2',   3:'m3',    4:'M3',     5:'P4',    6:'b5',    7:'P5',    8:'m6',    9:'M6',    10:'m7',   11:'M7'  } # 8/12/16
#               :0   :0      :1      :2      :3      :4      :4      :5      :5      :6      :7      :8      :9       :a       :b     :b
    I2F = {         0:'C' , 1:'Db', 2:'D' , 3:'Eb', 4:'E' ,                 5:'F' , 6:'Gb', 7:'G' , 8:'Ab', 9:'A' , 10:'Bb', 11:'B'       } # 8/12/16
    I2S = {         0:'C' , 1:'C#', 2:'D' , 3:'D#', 4:'E' ,                 5:'F' , 6:'F#', 7:'G' , 8:'G#', 9:'A' , 10:'A#', 11:'B'       } # 8/12/16
    I3F = {         0:'C' , 1:'Db', 2:'D' , 3:'Eb',         4:'Fb',         5:'F' , 6:'Gb', 7:'G' , 8:'Ab', 9:'A' , 10:'Bb',        11:'Cb' } # 8/12/16
    I3S = { 0:'B#',         1:'C#', 2:'D' , 3:'D#', 4:'E' ,         5:'E#',         6:'F#', 7:'G' , 8:'G#', 9:'A' , 10:'A#', 11:'B'         } # 8/12/16
    N2I = { 'B#':0, 'C':0, 'C#':1, 'Db':1, 'D':2, 'D#':3, 'Eb':3, 'E':4, 'Fb':4, 'E#':5, 'F':5, 'F#':6, 'Gb':6, 'G':7, 'G#':8, 'Ab':8, 'A':9, 'A#':10, 'Bb':10, 'B':11, 'Cb' :11 } #21
class Notes(object):#0     :1         :3         :4         :5         :6         :8        :a         :b       #  2    7 9  #
    TKS0, TKS1, TKS2 = [2, 7, 9], [1, 3, 6, 8, 10], [0, 4, 5, 11]
    F2S = {            'Db':'C#', 'Eb':'D#',                       'Gb':'F#', 'Ab':'G#', 'Bb':'A#'           } # 1 3  6 8 a # 5/9
    S2F = {            'C#':'Db', 'D#':'Eb',                       'F#':'Gb', 'G#':'Ab', 'A#':'Bb'           } # 1 3  6 8 a # 5/9
    F3S = { 'C' :'B#',                       'Fb':'E' , 'F' :'E#',                                 'Cb':'B'  } #0   45     b# 4/9
    S3F = { 'B#':'C' ,                       'E' :'Fb', 'E#':'F' ,                                  'B':'Cb' } #0   45     b# 4/9
#   V2I = {  'R':0,      'm2':1,  'M2':2,    'm3':3,    'M3':4,    'P4':5,    'b5':6,    'P5':7,    'm6':8,    'M6':9,    'm7':10,   'M7':11   } # 8/12/16
#   I2V = {   0:'R',      1:'m2',  2:'M2',   3:'m3',    4:'M3',     5:'P4',    6:'b5',    7:'P5',    8:'m6',    9:'M6',    10:'m7',   11:'M7'  } # 8/12/16
    V2I = { 'R':0,          'b2':1, '2':2,  'm3':3, 'M3':4,         '4':5,          'b5':6, '5':7,  '#5':8, '6':9,  'b7':10, '7':11         } # 8/12/16
    I2V = { 0:'R',          1:'b2', 2:'2',  3:'m3', 4:'M3',         5:'4',          6:'b5', 7:'5',  8:'#5', 9:'6',  10:'b7', 11:'7'         } # 8/12/16
    I2F = {         0:'C' , 1:'Db', 2:'D' , 3:'Eb', 4:'E' ,                 5:'F' , 6:'Gb', 7:'G' , 8:'Ab', 9:'A' , 10:'Bb', 11:'B'         } # 8/12/16
    I2S = {         0:'C' , 1:'C#', 2:'D' , 3:'D#', 4:'E' ,                 5:'F' , 6:'F#', 7:'G' , 8:'G#', 9:'A' , 10:'A#', 11:'B'         } # 8/12/16
    I3F = {         0:'C' , 1:'Db', 2:'D' , 3:'Eb',         4:'Fb',         5:'F' , 6:'Gb', 7:'G' , 8:'Ab', 9:'A' , 10:'Bb',        11:'Cb' } # 8/12/16
    I3S = { 0:'B#',         1:'C#', 2:'D' , 3:'D#', 4:'E' ,         5:'E#',         6:'F#', 7:'G' , 8:'G#', 9:'A' , 10:'A#', 11:'B'         } # 8/12/16
    N2I = { 'B#':0, 'C':0, 'C#':1, 'Db':1, 'D':2, 'D#':3, 'Eb':3, 'E':4, 'Fb':4, 'E#':5, 'F':5, 'F#':6, 'Gb':6, 'G':7, 'G#':8, 'Ab':8, 'A':9, 'A#':10, 'Bb':10, 'B':11, 'Cb' :11 } #21
#   N2I     = { 'B#':0, 'C' :0, 'C#':1, 'Db':1, 'D' :2, 'D#':3, 'Eb':3, 'E' :4, 'Fb':4, 'E#':5, 'F' :5, 'F#':6, 'Gb':6, 'G' :7, 'G#':8, 'Ab':8, 'A' :9, 'A#':10, 'Bb':10, 'B' :11, 'Cb' :11 } #21
    FLAT, NONE, SHRP =    -1,      0,      1    # -1 ~= 2
    TYPES            =          [ 'NONE', 'SHRP', 'FLAT' ] # 0=NONE, 1=SHRP, 2=FLAT=-1
    TYPE = FLAT   ;   NTONES = len(I2V)   ;   MAX_IDX = 10 * NTONES + 1
    I2N  = [None, I2S, I2F]   ;   I3N = [None, I3S, I3F]
    @staticmethod
    def setType(t): Notes.TYPE = t
    @staticmethod
    def index(n, o=0):
        name = n[:len(n)-1] if o else n
        i    = Notes.N2I[name]
        return i
    @staticmethod
    def nextIndex(i, d):
        return  (i + d) % Notes.NTONES
    @staticmethod
    def name(i, t=0, n2=0):
        t    = t if t else Notes.TYPE
        name = Notes.I3N[t][i % Notes.NTONES]   if n2   else Notes.I2N[t][i % Notes.NTONES]
        return name
    @staticmethod
    def nextName(n, iv, o=0):
        i = Notes.index(n, o)
        j = Notes.V2I[iv]
        k = Notes.nextIndex(i, j)
        m = Notes.name(k)
        return m

    @staticmethod
    def genCsvFile(why, path, dbg=1):
        if dbg:   slog(f'{why} {path}')
        with open(path, 'w') as CSV_FILE:
            n   = Notes.NTONES  ;    s = Notes.SHRP  ;    f = Notes.FLAT
            i2n = Notes.I2N     ;  f2s = Notes.F2S   ;  s2f = Notes.S2F  ;  tks1 = Notes.TKS1  ;   i2f = Notes.I2F  ;  i2s = Notes.I2S  ;  n2i = Notes.N2I
            i3n = Notes.I3N     ;  f3s = Notes.F3S   ;  s3f = Notes.S3F  ;  tks2 = Notes.TKS2  ;   i3f = Notes.I3F  ;  i3s = Notes.I3S
            slog(f'{CSV_FILE.name:40}', p=0)
            csv = f' ,{  fmtl([ r for r in range(21) ], d="", s=",")}'  ;  CSV_FILE.write(f'{csv}\n')
            csv = f'F2S,{fmtl([ f"{i2n[f][k]}:{f2s[i2n[f][k]]}"  if k in tks1 else B for k in range(n) ], d="", s=",")}'  ;  CSV_FILE.write(f'{csv}\n')
            csv = f'F3S,{fmtl([ f"{i3n[f][k]}:{f3s[i3n[f][k]]}"  if k in tks2 else B for k in range(n) ], d="", s=",")}'  ;  CSV_FILE.write(f'{csv}\n')
            csv = f'S2F,{fmtl([ f"{i2n[s][k]}:{s2f[i2n[s][k]]}"  if k in tks1 else B for k in range(n) ], d="", s=",")}'  ;  CSV_FILE.write(f'{csv}\n')
            csv = f'S3F,{fmtl([ f"{i3n[s][k]}:{s3f[i3n[s][k]]}"  if k in tks2 else B for k in range(n) ], d="", s=",")}'  ;  CSV_FILE.write(f'{csv}\n')
            csv = f'I2F,{fmtl([ f"{k}:{i2f[k]}" for k in range(n) ], d="", s=",")}'  ;  CSV_FILE.write(f'{csv}\n')
            csv = f'I3F,{fmtl([ f"{k}:{i3f[k]}" for k in range(n) ], d="", s=",")}'  ;  CSV_FILE.write(f'{csv}\n')
            csv = f'I2S,{fmtl([ f"{k}:{i2s[k]}" for k in range(n) ], d="", s=",")}'  ;  CSV_FILE.write(f'{csv}\n')
            csv = f'I3S,{fmtl([ f"{k}:{i3s[k]}" for k in range(n) ], d="", s=",")}'  ;  CSV_FILE.write(f'{csv}\n')
#            csv = f'N2I,{fmtl([ f"{i2n[f][k]}:{n2i[i2n[f][k]]}" for k in range(n) ], d="", s=",")}'  ;  CSV_FILE.write(f'{csv}\n')
            csv = f'N2I,{fmtl([ f"{k}:{v}" for k,v in n2i.items() ], d="", s=",")}'  ;  CSV_FILE.write(f'{csv}\n')
        size = path.stat().st_size   ;   slog(f'{size=}')
        return size
########################################################################################################################################################################################################
def updNotes(i, m, n, t, d=0):
    if   t  ==  Notes.FLAT:    Notes.I2F[i] = m
    elif t  ==  Notes.SHRP:    Notes.I2S[i] = n
    if   d:
        if m in Notes.S2F: del Notes.S2F[m]
        if n in Notes.F2S: del Notes.F2S[n]
    else:
        Notes.F2S[n] = m   ;   Notes.S2F[m] = n
########################################################################################################################################################################################################
def initND():
    return { i:[ Notes.I2F[i], Notes.I2S[i], Notes.I2V[i] ] for i in range(Notes.NTONES) }
ND = initND()
########################################################################################################################################################################################################
FLATS  = [ f'{v}{n}' for n in range(11) for v in Notes.I3F.values() ][:Notes.MAX_IDX]
SHRPS  = [ f'{v}{n}' for n in range(11) for v in Notes.I3S.values() ][:Notes.MAX_IDX]

def FREQ( index): return 440 * pow(pow(2, 1/Notes.NTONES), index - 57)
def FREQ2(index): return 432 * pow(pow(2, 1/Notes.NTONES), index - 57)

FREQS   = [ FREQ( i) for i in range(Notes.MAX_IDX) ]
FREQS2  = [ FREQ2(i) for i in range(Notes.MAX_IDX) ]
########################################################################################################################################################################################################
def fmtKSK(k):
    t   = -1 if k < 0 else 1 if k > 0 else 0    ;   nt = Notes.TYPES[t]
    s   = t2sign(t)     ;   im = KSD[k][KIM]    ;    i = im[0]      ;    m = im[1]
    iz  = KSD[k][KIS]   ;   jz = KSD[k][KJS]    ;   ms = KSD[k][KMS]
    ns  = [ Notes.name(j, t, 1 if abs(k) >= 5 else 0) for j in jz ]
    iz  = [ f'{i:x}' for i in iz ]
    jz  = [ f'{j:x}' for j in jz ]
    return f'{s}{k} {nt} [{m:2} {i:x}] {fmtl(ms, w=2)} {fmtl(iz)} {fmtl(jz)} {fmtl(ns, w=2)}'
########################################################################################################################################################################################################
def fmtl(lst, w=None, u=None, d='[', d2=']', s=' ', ll=None): # optimize str concat?
    if   lst is None:   return  'None'
    lts = (list, tuple, set, frozenset)  ;  dtn = (int, float)  ;  dts = (str,)
    assert type(lst) in lts, f'{type(lst)=} {lts=}'
    if d == '':    d2 = ''
    w   = w   if w else ''   ;   t = []
    zl  = '-'               if ll is not None and ll<0 else '+' if ll is not None and ll>=0 else ''
    z   = f'{zl}{len(lst)}' if ll is not None          else ''
    for i, l in enumerate(lst):
        if type(l) in lts:
            if type(w) in lts:               t.append(fmtl(l, w[i], u, d, d2, s, ll))
            else:                            t.append(fmtl(l, w,    u, d, d2, s, ll))
        else:
            ss = s if i < len(lst)-1 else ''
            u = '' if u is None else u
            if   type(l) is type:            l =  str(l)
            elif l is None:                  l =  'None'
            if   type(w) in lts:             t.append(f'{l:{u}{w[i]}}{ss}')
            elif type(l) in dtn:             t.append(f'{l:{u}{w   }}{ss}')
            elif type(l) in dts:             t.append(f'{l:{u}{w   }}{ss}')
            else:                            t.append(f'{l}{ss}')
    return z + d + ''.join(t) + d2
########################################################################################################################################################################################################
def fmtm(m, w=None, wv=None, u=None, uv=None, d0=':', d='[', d2=']', s=' ', ll=None):
    w  = w  if w  else ''   ;  t = []
    wv = wv if wv else w
    if d=='':   d2 = ''
    u  = '' if u  is None else u
    uv = '' if uv is None else uv
    for i, (k, v) in enumerate(m.items()):
        ss = s if i < len(m) - 1 else ''
        if   type(v) in (list, tuple, set):  t.append(f'{d}{k:{u}{w}}{d0}{fmtl(v, wv, ll=k if ll==-1 else ll)}{d2}{ss}')
        elif type(v) in (int, str):          t.append(f'{d}{k:{u}{w}}{d0}{v:{uv}{wv}}{d2}{ss}')
    return ''.join(t)
########################################################################################################################################################################################################
def ev(obj):         return f'{eval(f"{obj!r}")}'
def fColor(c, d=1): (d, d2) = ("[", "]") if d else ("", "")  ;  return f'{fmtl(c, w=3, d=d, d2=d2):17}'

def ordSfx(n):
    m = n % 10
    if   m == 1 and n != 11: return 'st'
    elif m == 2 and n != 12: return 'nd'
    elif m == 3 and n != 13: return 'rd'
    else:                    return 'th'
########################################################################################################################################################################################################
def stackDepth(sfs):
    global     MAX_STACK_DEPTH, MAX_STACK_FRAME
    for i, sf in enumerate(sfs):
        j = len(sfs) - (i + 1)
        if j > MAX_STACK_DEPTH: MAX_STACK_FRAME = sfs  ;  MAX_STACK_DEPTH = j
    return  len(sfs)

def fmtSD(sd): return f'{sd:{sd}}'

def dumpStack(sfs):
    for i, sf in enumerate(sfs):
        fp = pathlib.Path(sf.filename)  ;   n = fp.stem  ;  l = sf.lineno  ;  f = sf.function  ;  c = sf.code_context[0].strip() if sf.code_context else ''  ;  j = len(sfs) - (i + 1)
        slog(f'{j:2} {n:9} {l:5} {f:20} {c}')
    slog(f'MAX_STACK_DEPTH={MAX_STACK_DEPTH:2}')
########################################################################################################################################################################################################
def slog(t='', p=1, f=1, s=',', e='\n', ff=False):
    t = filtText(t) #    t = filtText2(t)
    if p:
        sf   = inspect.currentframe().f_back
        while sf.f_code.co_name in STFILT: sf = sf.f_back # ;  print(f'sf 2: {sf.f_lineno}, {sf.f_code.co_name}')
        fp   = pathlib.Path(sf.f_code.co_filename)
        pl   = 18 if p == 1 else 8
        p    = f'{sf.f_lineno:4} {fp.stem:5} ' if p == 1 else ''
        t    = f'{p}{sf.f_code.co_name:{pl}} ' + t
    so = 0
    if   f == 0:  f = sys.stdout
    elif f == 1:  f = LOG_FILE
    elif f == 2:  f = LOG_FILE  ;  so = 1
    print(t, sep=s, end=e, file=f,    flush=ff)
    print(t, sep=s, end=e, file=None, flush=ff) if so else None
########################################################################################################################################################################################################
def filtText(text):
    text = text.replace('"', '')
    text = text.replace("'", '')
    text = text.replace('self', '')
    text = text.replace('util', '')
    text = text.replace('fmtl', '')
    text = text.replace('fmtm', '')
    return text

def filtText2(text):
    text = text.replace(', w=w', '')
    text = text.replace(', u=u', '')
    text = text.replace(', d=d', '')
    text = text.replace('([ ', '')
    text = text.replace(' ])', '')
    text = text.replace('(_)', '_')
    text = text.replace('(f[_])', 'f[_]')
    text = text.replace('(s[_])', 's[_]')
    return text
########################################################################################################################################################################################################
def getFilePath(baseName, basePath, fdir='files', fsfx='.txt', dbg=1):
    if dbg: slog(f'{baseName =:12} {basePath = }', f=2)
    fileName      = baseName + fsfx
    filePath      = basePath / fdir / fileName
    if dbg: slog(f'{fileName =:12} {filePath = }', f=2)
    return filePath

def copyFile(src, trg):
    if not src.exists(): msg = f'ERROR Path Doesnt Exist {src=}'   ;   slog(msg)   ;  raise SystemExit(msg)
    slog(f'{src=}')
    slog(f'{trg=}')
    cmd = f'copy {src} {trg}'
    slog(f'### {cmd} ###')
    os.system(f'{cmd}')
########################################################################################################################################################################################################
def parseCmdLine(dbg=1):
    options = dict()
    key     = ''
    vals    = []
    largs   = len(sys.argv)
    if dbg: slog(f'argv={fmtl(sys.argv[1:])}')  ;  slog(sys.argv[0], p=0)
    for j in range(1, largs):
        argv = sys.argv[j]
        if len(argv) > 2 and argv[0] == '-' and argv[1] == '-':
            if argv[2].isalpha():
                vals = []
                key = argv[2:]
                options[key] = vals
                if dbg: slog(f'{j:2} long    {argv:2} {key} {fmtl(vals)}', e=' ')
            else:
                slog(f'{j:2} ERROR long    {argv:2} {key} {fmtl(vals)}', e=' ')
        elif len(argv) > 1 and argv[0] == '-':
            if argv[1].isalpha() or argv[1] == '?':
                vals = []
                if len(argv) == 2:
                    key = argv[1:]
                    if dbg: slog(f'{j:2} short   {argv:2} {key} {fmtl(vals)}', e=' ')
                    options[key] = vals
                elif len(argv) > 2:
                    for i in range(1, len(argv)):
                        key = argv[i]
                        if dbg: slog(f'{j:2} short   {argv:2} {key} {fmtl(vals)}', e=' ')
                        options[key] = vals
            elif argv[1].isdigit():
                vals.append(argv)
                options[key] = vals
                if dbg: slog(f'{j:2} neg arg {argv:2} {key} {fmtl(vals)}', e=' ')
            else:
                vals.append(argv)
                options[key] = vals
                if dbg: slog(f'{j:2} ??? arg {argv:2} {key} {fmtl(vals)}', e=' ')
        else:
            vals.append(argv)
            options[key] = vals
            if dbg: slog(f'{j:2} arg     {argv:2} {key} {fmtl(vals)}', e=' ')
        if dbg: slog(p=0)
    if dbg: slog(f'options={fmtm(options)}')
    return options
########################################################################################################################################################################################################
KSD = {}
KIM, KIS, KMS, KJS, KNS             = range(5)
KSS, KSK, KST, KSN, KSI, KSMS, KSSI = range(7)
dmpKSVHdr(-1)
KSD = initKSD(KSD, t=-1)
KSD = initKSD(KSD, t= 1)
dmpKSVHdr( 1)
dumpKSH()

########################################################################################################################################################################################################

class Test:
    def __init__(self, a): self._a = a  ;  slog(f'<Test_init_:     _a={self._a}>', p=1)
    @property
    def a(self):                           slog(f'<Test_prop_a:    _a={self._a}>', p=1)
    @a.setter
    def a(self, a):        self._a = a  ;  slog(f'<Test_set_a:     _a={self._a}>', p=1)
    @a.getter
    def a(self):                           slog(f'<Test_get_a:     _a={self._a}>', p=1)  ;  return self._a
    @a.deleter
    def a(self):                           slog(f'<Test_del_a: del _a>', p=1)  ;  del self._a
