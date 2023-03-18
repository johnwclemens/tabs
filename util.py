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

def dumpData():
    slog('BGN')
    slog(f'[F2S:      {len(Notes.F2S ):2}] [{fmtm(Notes.F2S,  w=2, d="")}]',  p=0)
    slog(f'[S2F:      {len(Notes.S2F ):2}] [{fmtm(Notes.S2F,  w=2, d="")}]',  p=0)
    slog(f'[F2S2:     {len(Notes.F2S2):2}] [{fmtm(Notes.F2S2, w=2, d="")}]',  p=0)
    slog(f'[S2F2:     {len(Notes.S2F2):2}] [{fmtm(Notes.S2F2, w=2, d="")}]',  p=0)
    slog(f'[I2F:      {len(Notes.I2F ):2}] [{fmtm(Notes.I2F,  w=2, d="")}]',  p=0)
    slog(f'[I2S:      {len(Notes.I2S ):2}] [{fmtm(Notes.I2S,  w=2, d="")}]',  p=0)
    slog(f'[I2F2:     {len(Notes.I2F2):2}] [{fmtm(Notes.I2F2, w=2, d="")}]',  p=0)
    slog(f'[I2S2:     {len(Notes.I2S2):2}] [{fmtm(Notes.I2S2, w=2, d="")}]',  p=0)
    slog(f'[I2V:      {len(Notes.I2V ):2}] [{fmtm(Notes.I2V,  w=2, d="")}]',  p=0)
    slog(f'[V2I:      {len(Notes.V2I ):2}] [{fmtm(Notes.V2I,  w=2, d="")}]',  p=0)
    slog(f'[N2I:      {len(Notes.N2I ):2}] [{fmtm(Notes.N2I,  w=2, d="")}]',  p=0)
    slog(f'[I2N[-1]:  {len(Notes.I2N[-1] ):2}] [{fmtm(Notes.I2N[-1],   w=2, d="")}]',  p=0)
    slog(f'[I2N[ 0]:  {len(Notes.I2N[ 0] ):2}] [{fmtm(Notes.I2N[ 0],   w=2, d="")}]',  p=0)
    slog(f'[I2N[ 1]:  {len(Notes.I2N[ 1] ):2}] [{fmtm(Notes.I2N[ 1],   w=2, d="")}]',  p=0)
    slog(f'[I2N2[-1]: {len(Notes.I2N2[-1] ):2}] [{fmtm(Notes.I2N2[-1],  w=2, d="")}]',  p=0)
    slog(f'[I2N2[ 0]: {len(Notes.I2N2[ 0] ):2}] [{fmtm(Notes.I2N2[ 0],  w=2, d="")}]',  p=0)
    slog(f'[I2N2[ 1]: {len(Notes.I2N2[ 1] ):2}] [{fmtm(Notes.I2N2[ 1],  w=2, d="")}]',  p=0)
    dumpNF()
    dumpND()
    dumpKS()
    slog('END')
########################################################################################################################################################################################################
def dumpNF():
    slog(f'Note Frequency Hz')   ;   msg = f'Piano Note Index{B*43}'
    slog(f'{msg}{fmtl([ i+1 for i in range(88) ], w=5, u="^")}',  p=0)
    slog(f'Index{fmtl([ i+1 for i in range(Notes.MAX_IDX) ], w=5, u="^")}',  p=0)
    dumpFreqs(432)  ;  dumpFreqs(440)
    slog(f'Flats{fmtl(list(FLATS),                           w=5, u="^")}',  p=0)
    slog(f'Shrps{fmtl(list(SHRPS),                           w=5, u="^")}',  p=0)

def dumpND():
    slog(f'I  F  S  IV   Notes Table {len(ND)}', p=0)
    for i in range(len(ND)):   slog(f'{i:x} {fmtl(ND[i], w=2)}', p=0)

def dumpKS():
    dmpKSDhdr()
    keys = sorted(KSD.keys())
    for k in keys:      slog(fmtks(k), p=0)
########################################################################################################################################################################################################
def dumpFreqs(r=440):
    fs = FREQS if r == 440 else FREQS2   ;   g = []   ;   ref = 'A 440' if r == 440 else  'A 432'
    for f in fs:       g.append(f'{f:5.2f}' if f < 100 else f'{f:5.1f}' if f < 1000 else f'{f:5.0f}')
    ' '.join(f'{g}')   ;   slog(f'{ref}{fmtl(g, w=5)} Hz', p=0)
########################################################################################################################################################################################################
def dmpKSDhdr(t=0):
    k = 2*P+1 if t == 0 else M if t == Notes.FLAT else P if t == Notes.SHRP else 1   ;   sign = t2sign(t)
    slog(f'KS Type  N  I   Flats/Sharps Naturals  F/S/N Indices  Ionian Indices   Ionian Note Ordering   Key Sig Table {sign}{k}', p=0)

def dumpKSD(ksd, w=2, u='<'):
#   keys = sorted(ksd.keys())  ;  w = f'{u}{w}'  ;  x = f'{w}x'  ;  d = ''  ;  v = B*24 if Notes.TYPE==Notes.FLAT else ''
#   keys = sorted(ksd.keys())  ;  w = f'{u}{w}'  ;  x = f'{w}x'  ;  v = B*24 if Notes.TYPE==Notes.FLAT else ''  ;  d = ''
    keys = sorted(ksd.keys())  ;  v = B*24 if Notes.TYPE==Notes.FLAT else ''  ;  w = f'{u}{w}'  ;  x = f'{w}x'  ;  d = ''
#   keys = sorted(ksd.keys())  ;  v = B*24 if Notes.TYPE==Notes.FLAT else ''  ;  d = ''  ;  w = f'{u}{w}'  ;  x = f'{w}x'
#   keys = sorted(ksd.keys())  ;  d = ''  ;  w = f'{u}{w}'  ;  x = f'{w}x'  ;  v = B*24 if Notes.TYPE==Notes.FLAT else ''
#   keys = sorted(ksd.keys())  ;  d = ''  ;  v = B*24 if Notes.TYPE==Notes.FLAT else ''  ;  w = f'{u}{w}'  ;  x = f'{w}x'
    _ = js2sign(keys)   ;   _ = '  '.join(_)   ;   slog(f'{v}{_}')   ;   slog(f'{v}{fmtl(list(map(abs, keys)), w=w, d=d)}')
    _ = [ ksd[k][0][0]    for k in keys ]      ;   slog(f'{v}{fmtl(_, w=x, d=d)}')
    _ = [ ksd[k][0][1]    for k in keys ]      ;   slog(f'{v}{fmtl(_, w=w, d=d)}')
    f = [ ksd[M][2][f]    for f in range(len(ksd[M][2])-1, -1, -1) ]
    s = [ ksd[P][2][s]    for s in range(len(ksd[P][2]))           ]         ;  slog(f'{v}{fmtl(f, w=w, d=d)} {B*2} {fmtl(s, w=w, d=d)}')
    f = [ f for f in reversed(ksd[M][1]) ]  ;  s = [ s for s in ksd[P][1] ]  ;  slog(f'{v}{fmtl(f, w=x, d=d)} {B*2} {fmtl(s, w=x, d=d)}')
########################################################################################################################################################################################################
def nic2KS(nic, dbg=0):
    dumpKSD(KSD)   ;   dumpNic(nic)
    iz  = []       ;   t = Notes.TYPE   ;   nt = Notes.TYPES[t]
    ks  = KSD[M][KIS]    if t == Notes.FLAT else KSD[P][KIS]
    for i in ks:
        if i in nic:     iz.append(f'{i:x}')
        else:            break
    k   = -len(iz)       if t == Notes.FLAT else len(iz)
    s   = t2sign(t)      if iz else '?'
    n   = KSD[k][KIM][1] if iz else '??'
    i   = KSD[k][KIM][0]
    ns  = KSD[k][KMS]
    slog(fmtks(k))       if dbg else None
    return  s, k, nt, n, i, ns, Scales.majIs(i)

def dumpNic(nic):
    slog(f'{fmtl([ f"{i:x}:{Notes.I2F[i]:2}:{c:2}" for i, c in nic.items() ])} {fmtl([ f"{i:x}:{Notes.I2S[i]}:{c}" for i, c in nic.items() ])}')
    slog(f'{fmtl([ f"{i:x}:{Notes.I2S[i]:2}:{c:2}" for i, c in nic.items() ])}')
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
        slog(fmtks(k), p=0)
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

#            if     j  == 11:     updNotes(j, 'Cb', 'B', Notes.TYPE, 0)
#            if     j  ==  5:     updNotes(j, 'F', 'E#', Notes.TYPE, 0)
#            elif   j  ==  4:     updNotes(j, 'Fb', 'E', Notes.TYPE, 0)
#            elif   j  ==  0:     updNotes(j, 'C', 'B#', Notes.TYPE, 0)
    def tab2nn(self, tab, s, nic=None, dbg=1):
        fn  = self.tab2fn(tab)
        i   = self.fn2ni(fn, s)   ;   nict = ''
        j   = i % Notes.NTONES
        if nic is not None:  nic[j] += 1  ;  nict = f'nic[{j:x}]={nic[j]} '  ;  slog(f'adding {nict}', f=0) if nic[j]==1 else None
        else:                nic     = Counter()
        name = Notes.name(i)
        if dbg or nict: slog(f'tab={tab} s={s} fn={fn} i={i:2} j={j:x} name={name:2} {nict}{fmtm(nic)}')
        return name
########################################################################################################################################################################################################
class Notes(object):
    F2S     = {            'Db':'C#', 'Eb':'D#',                       'Gb':'F#', 'Ab':'G#', 'Bb':'A#'           } # 5/9
    S2F     = {            'C#':'Db', 'D#':'Eb',                       'F#':'Gb', 'G#':'Ab', 'A#':'Bb'           } # 5/9
    F2S2    = { 'C' :'B#',                       'Fb':'E' , 'F' :'E#',                                  'Cb':'B' } # 4/9
    S2F2    = { 'B#':'C' ,                       'E' :'Fb', 'E#':'F' ,                                  'B':'Cb' } # 4/9
    I2F     = {         0:'C' , 1:'Db', 2:'D' , 3:'Eb', 4:'E' ,                 5:'F' , 6:'Gb', 7:'G' , 8:'Ab', 9:'A' , 10:'Bb', 11:'B'         } # 8/12/16
    I2S     = {         0:'C' , 1:'C#', 2:'D' , 3:'D#', 4:'E' ,                 5:'F' , 6:'F#', 7:'G' , 8:'G#', 9:'A' , 10:'A#', 11:'B'         } # 8/12/16
    I2F2    = {         0:'C' , 1:'Db', 2:'D' , 3:'Eb',         4:'Fb',         5:'F' , 6:'Gb', 7:'G' , 8:'Ab', 9:'A' , 10:'Bb',        11:'Cb' } # 8/12/16
    I2S2    = { 0:'B#',         1:'C#', 2:'D' , 3:'D#', 4:'E' ,         5:'E#',         6:'F#', 7:'G' , 8:'G#', 9:'A' , 10:'A#', 11:'B'         } # 8/12/16
    I2V     = { 0:'R',          1:'b2', 2:'2',  3:'m3', 4:'M3',         5:'4',          6:'b5', 7:'5',  8:'#5', 9:'6',  10:'b7', 11:'7'         } # 8/12/16
    V2I     = { 'R':0,          'b2':1, '2':2,  'm3':3, 'M3':4,         '4':5,          'b5':6, '5':7,  '#5':8, '6':9,  'b7':10, '7':11         } # 8/12/16
    N2I     = { 'B#':0, 'C':0, 'C#':1, 'Db':1, 'D':2, 'D#':3, 'Eb':3, 'E':4, 'Fb':4, 'E#':5, 'F':5, 'F#':6, 'Gb':6, 'G':7, 'G#':8, 'Ab':8, 'A':9, 'A#':10, 'Bb':10, 'B':11, 'Cb' :11 } #21
#   N2I     = { 'B#':0, 'C' :0, 'C#':1, 'Db':1, 'D' :2, 'D#':3, 'Eb':3, 'E' :4, 'Fb':4, 'E#':5, 'F' :5, 'F#':6, 'Gb':6, 'G' :7, 'G#':8, 'Ab':8, 'A' :9, 'A#':10, 'Bb':10, 'B' :11, 'Cb' :11 } #21
    FLAT, NONE, SHRP =    -1,      0,      1    # -1 ~= 2
    TYPES            =          [ 'NONE', 'SHRP', 'FLAT' ] # 0=NONE, 1=SHRP, 2=FLAT=-1
    I2N     = [I2F, I2S, I2F]   ;   I2N2 = [I2F2, I2S2, I2F2]   ;   TYPE = FLAT   ;   NTONES = len(I2V)   ;   MAX_IDX = 10 * NTONES + 1

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
        name = Notes.I2N2[t][i % Notes.NTONES]   if n2   else Notes.I2N[t][i % Notes.NTONES]
        return name

    @staticmethod
    def nextName(n, iv, o=0):
        i = Notes.index(n, o)
        j = Notes.V2I[iv]
        k = Notes.nextIndex(i, j)
        m = Notes.name(k)
        return m
########################################################################################################################################################################################################
def updNotes(i, m, n, t, d):
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
FLATS  = [ f'{v}{n}' for n in range(11) for v in Notes.I2F2.values() ][:Notes.MAX_IDX]
SHRPS  = [ f'{v}{n}' for n in range(11) for v in Notes.I2S2.values() ][:Notes.MAX_IDX]

def FREQ( index): return 440 * pow(pow(2, 1/Notes.NTONES), index - 57)
def FREQ2(index): return 432 * pow(pow(2, 1/Notes.NTONES), index - 57)

FREQS   = [ FREQ( i) for i in range(Notes.MAX_IDX) ]
FREQS2  = [ FREQ2(i) for i in range(Notes.MAX_IDX) ]
########################################################################################################################################################################################################
def fmtks(k):
    t   = -1 if k < 0 else 1 if k > 0 else 0    ;   nt = Notes.TYPES[t]
    s   = t2sign(t)     ;   im = KSD[k][KIM]    ;    i = im[0]      ;    m = im[1]
    iz  = KSD[k][KIS]   ;   jz = KSD[k][KJS]    ;   ms = KSD[k][KMS]
    ns  = [ Notes.name(j, t, 1 if abs(k) >= 5 else 0) for j in jz ]
    iz  = [ f'{i:x}' for i in iz ]
    jz  = [ f'{j:x}' for j in jz ]
    return f'{s}{k} {nt} [{m:2} {i:x}] {fmtl(ms, w=2)} {fmtl(iz)} {fmtl(jz)} {fmtl(ns, w=2)}'
########################################################################################################################################################################################################
def fmtl(lst, w=None, u=None, d='[', d2=']', sep=' ', ll=None, z=''):
    if   lst is None:   return  'None'
    lts = (list, tuple, set, frozenset)  ;  dtn = (int, float)  ;  dts = (str,)
    assert type(lst) in lts, f'{type(lst)=} {lts=}'
    if d == '':    d2 = ''
    w   = w   if w else ''   ;   t = ''
    sl  = '-'               if ll is not None and ll<0 else '+' if ll is not None and ll>=0 else ''
    s   = f'{sl}{len(lst)}' if ll is not None          else ''
    for i, l in enumerate(lst):
        if type(l) in lts:
            if type(w) in lts:               t += fmtl(l, w[i], u, d, d2, sep, ll, z)
            else:                            t += fmtl(l, w,    u, d, d2, sep, ll, z)
        else:
            ss = sep if i < len(lst)-1 else ''
            u = '' if u is None else u
            if   type(l) is type:            l =  str(l)
            elif l is None:                  l =  'None'
            if   type(w) in lts:             t += f'{l:{u}{w[i]}{z}}{ss}'
            elif type(l) in dtn:             t += f'{l:{u}{w   }{z}}{ss}'
            elif type(l) in dts:             t += f'{l:{u}{w   }{z}}{ss}'
            else:                            t += f'{l}{ss}'
    return s + d + t + d2
########################################################################################################################################################################################################
def fmtm(m, w=1, d0=':', d='[', d2=']', ll=None):
    if d=='':   d2 = ''
    t = ''   ;   u = '>'
    for k, v in m.items():
        if   type(v) in (list, tuple, set):  t += f'{d}{k:{u}{w}}{d0}{fmtl(v, w, ll=k if ll==-1 else ll)}{d2} '
        elif type(v) in (int, str):          t += f'{d}{k:{u}{w}}{d0}{v:{u}{w}}{d2} '
    return d + t.rstrip() + d2
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
def OLD__slog(msg='', pfx=1, file=1, flush=False, sep=',', end='\n'):
    msg = filtText( msg) #    msg = filtText2(msg)
    if pfx:
        sf   = inspect.currentframe().f_back
        while sf.f_code.co_name in STFILT: sf = sf.f_back # ;  print(f'sf 2: {sf.f_lineno}, {sf.f_code.co_name}')
#        else:                           print(f'sf:  {sf.f_lineno}, {sf.f_code.co_name}')
#        sfi = inspect.getframeinfo(sf)
#        if sfi.function == 'log':
#            sf = sf.f_back
#            sfi = inspect.getframeinfo(sf)
#        filename  = pathlib.Path(sfi.filename).name
#        msg  = f'{sfi.lineno:5} {filename:7} {sfi.function:>20} ' + msg
        fp   = pathlib.Path(sf.f_code.co_filename)
        pl   = 18 if pfx == 1 else 8
        pfx  = f'{sf.f_lineno:4} {fp.stem:5} ' if pfx == 1 else ''
        msg  = f'{pfx}{sf.f_code.co_name:{pl}} ' + msg
    so = 0
    if   file == 0:  file = sys.stdout
    elif file == 1:  file = LOG_FILE
    elif file == 2:  file = LOG_FILE  ;  so = 1
    print(msg, sep=sep, end=end, file=file, flush=flush)
    print(msg, sep=sep, end=end, file=None, flush=flush) if so else None
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
    if dbg: slog(f'argv={fmtl(sys.argv[1:])}')  ;  slog(f'{sys.argv[0]}', p=0)
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
KIM = 0  ;  KIS = 1  ;  KMS = 2  ;  KJS = 3  ;  KNS = 4
KSD = {}
dmpKSDhdr(-1)
KSD = initKSD(KSD, t=-1)
KSD = initKSD(KSD, t= 1)
dmpKSDhdr( 1)
#class KS(object):
#    def __init__(self):
#        self.KSD = {}
#        dmpKSDhdr(-1)
#        self.KSD = initKSD(self.KSD, t=-1)
#        self.KSD = initKSD(self.KSD, t= 1)
#        dmpKSDhdr( 1)

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
