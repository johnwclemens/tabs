"""util.py module.  class list: [DSymb, Note, Strings, Test]."""
import sys, os, inspect, pathlib
from collections import OrderedDict as cOd

B                = ' '
OIDS             = 0
LOG_FILE         = None
MIN_IVAL_LEN     = 1
MAX_STACK_DEPTH  = 0
MAX_STACK_FRAME  = inspect.stack()
M12              = { 10:'a', 11:'b' }
IVALS            = { 0:'R', 1:'b2', 2:'2', 3:'m3', 4:'M3', 5:'4', 6:'b5', 7:'5', 8:'#5', 9:'6', 10:'b7', 11:'7' }
IVALR            = { 'R':0, 'b2':1, '2':2, 'm3':3, 'M3':4, '4':5, 'b5':6, '5':7, '#5':8, '6':9, 'b7':10, '7':11 }
NTONES           = len(IVALS)
INIT             = '###   Init   ###'     * 13
QUIT_BGN         = '###   BGN Quit   ###' * 10
QUIT             = '###   Quit   ###'     * 13
QUIT_END         = '###   END Quit   ###' * 10
#STFILT = ['log', 'dumpGeom', 'resetJ', 'dumpJs', 'dumpImap', 'dumpSmap', 'dumpCursorArrows', '<listcomp>', 'dumpLimap2', 'dumpTniksPfx', 'dumpTniksSfx']
STFILT = ['log', 'tlog', 'dumpGeom', 'resetJ', 'dumpJs', 'dumpImap', 'dumpSmap', 'dumpCursorArrows', '<listcomp>', 'dumpLimap2', 'dumpTniksPfx', 'dumpTniksSfx', 'fmtXYWH', 'kbkInfo', 'dumpCrs', 'fCrsCrt'] # , 'dumpView', 'dumpLbox', 'dumpRect']
########################################################################################################################################################################################################
def init(file, oid):
    global LOG_FILE  ;  LOG_FILE = file  ;  global OIDS  ;  OIDS = oid
    slog('BGN')
    slog(f'{B*15}{len(Note.F2S):3}    F2S', pfx=0)   ;   slog(f'{fmtm(Note.F2S, w=2, d1="")}',  pfx=0)
    slog(f'{B*15}{len(Note.S2F):3}    S2F', pfx=0)   ;   slog(f'{fmtm(Note.S2F, w=2, d1="")}',  pfx=0)
    slog(f'{B*15}{len(Note.I2F):3}    I2F', pfx=0)   ;   slog(f'{fmtm(Note.I2F, w=2, d1="")}',  pfx=0)
    slog(f'{B*15}{len(Note.I2S):3}    I2S', pfx=0)   ;   slog(f'{fmtm(Note.I2S, w=2, d1="")}',  pfx=0)
    slog(f'{B*15}{len(Note.I2F2):3}    I2F2', pfx=0)   ;   slog(f'{fmtm(Note.I2F2, w=2, d1="")}',  pfx=0)
    slog(f'{B*15}{len(Note.I2S2):3}    I2S2', pfx=0)   ;   slog(f'{fmtm(Note.I2S2, w=2, d1="")}',  pfx=0)
    slog(f'{B*15}{len(Note.N2I):3}    N2I', pfx=0)   ;   slog(f'{fmtm(Note.N2I, w=2, d1="")}',  pfx=0)
    slog(f'{B*15}{len(FLATS):3}    FLATS',  pfx=0)
    slog(f'{fmtl(FLATS, w="3", d1="")}',    pfx=0)
    slog(f'{fmtl( [ f"{i + 1:3}" for i in range(Note.MAX_IDX) ], d1="")}', pfx=0)
    slog(f'{fmtl(SHRPS, w="3", d1="")}',    pfx=0)
    slog(f'{B*15}{len(SHRPS):3}    SHRPS',  pfx=0)
    slog(f'{B*15}{len(KeySig.FO):3}    FO', pfx=0)   ;   slog(f'{fmtm(KeySig.FO, w=2, d1="")}', pfx=0)
    slog(f'{B*15}{len(KeySig.SO):3}    SO', pfx=0)   ;   slog(f'{fmtm(KeySig.SO, w=2, d1="")}', pfx=0)
    slog(f'{B*15}{len(KeySig.KO):3}    KO', pfx=0)   ;   slog(f'{fmtm(KeySig.KO, w=2, d1="")}', pfx=0)
    for i in range(len(Note.I2N)):
        slog(f'{B * 15}{len(Note.I2N[i]):3}    I2N[{Note.TYPES[i]}]', pfx=0)
        slog(f'{fmtm(Note.I2N[i], w=2, d1="")}', pfx=0)
    slog(f'{B*15}{len(KeySig.KS):3}    KS', pfx=0)   ;   slog(f'{fmtm(KeySig.KS, w=2, d2=chr(10), ll=-1)}', pfx=0)
    slog('END')

def fmtl(lst, w=None, u='>', d1='[', d2=']', sep=' ', ll=None, z=''):
    if lst is None: return 'None'
    lts = (list, tuple, set, frozenset)  ;  dts = (int, float, str)
    assert type(lst) in lts, f'{type(lst)=} {lts=}'
    if d1=='':   d2 = ''
    w = w if w else ''   ;   t = ''
    sl = '-' if ll is not None and ll<0 else ' ' if ll is not None and ll>=0 else ''
    s = f'{sl}{len(lst)}' if ll is not None else ''
    for i, l in enumerate(lst):
        if type(l) in lts:
            if type(w) in lts:               t += fmtl(l, w[i], u, d1, d2, sep, ll, z)
            else:                            t += fmtl(l, w,    u, d1, d2, sep, ll, z)
        else:
            ss = sep if i < len(lst)-1 else ''
            if   type(l) is type:            l =  str(l)
            elif l is None:                  l =  'None'
            if   type(w) in lts:             t += f'{l:{u}{w[i]}{z}}{ss}'
            elif type(l) in dts:             t += f'{l:{u}{w   }{z}}{ss}'
            else:                            t += f'{l}{ss}'
#            else:                             msg = f'ERROR l={l} is type {type(l)}'   ;   slog(msg)   ;   raise SystemExit(msg)
    return s + d1 + t + d2

def fmtm(m, w=1, d0=':', d1='[', d2=']', ll=None):
    if d1=='':   d2 = ''
    t = ''   ;   u = '>'
    for k, v in m.items():
        if   type(v) in (list, tuple, set):         t += f'{d1}{k:{u}{w}}{d0}{fmtl(v, w, ll=k if ll==-1 else ll)}{d2} '
        elif type(v) in (int, str):                 t += f'{d1}{k:{u}{w}}{d0}{v:{u}{w}}{d2} '
    return d1 + t.rstrip() + d2

def ev(obj):          return f'{eval(f"{obj!r}")}'
def fColor(c, d=1): (d1, d2) = ("[", "]") if d else ("", "")  ;  return f'{fmtl(c, w="3", d1=d1, d2=d2):17}'

def ordSfx(n):
    m = n % 10
    if   m == 1 and n != 11: return 'st'
    elif m == 2 and n != 12: return 'nd'
    elif m == 3 and n != 13: return 'rd'
    else:                    return 'th'
########################################################################################################################################################################################################
def stackDepth(sfs):
    global MAX_STACK_DEPTH, MAX_STACK_FRAME
    for i, sf in enumerate(sfs):
        j = len(sfs) - (i + 1)
        if j > MAX_STACK_DEPTH: MAX_STACK_DEPTH = j;  MAX_STACK_FRAME = sfs
    return len(sfs)

def fmtSD(sd): return f'{sd:{sd}}'

def dumpStack(sfs):
    for i, sf in enumerate(sfs):
        fp = pathlib.Path(sf.filename)  ;   n = fp.stem  ;  l = sf.lineno  ;  f = sf.function  ;  c = sf.code_context[0].strip() if sf.code_context else ''  ;  j = len(sfs) - (i + 1)
        slog(f'{j:2} {n:9} {l:5} {f:20} {c}')
    slog(f'MAX_STACK_DEPTH={MAX_STACK_DEPTH:2}')
########################################################################################################################################################################################################
def slog(msg='', pfx=1, file=1, flush=False, sep=',', end='\n'):
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
        msg  = msg.replace('self.', '.')
        msg  = msg.replace('util.', '.')
        msg  = msg.replace('"', '')
        msg  = msg.replace("'", '')
        fp   = pathlib.Path(sf.f_code.co_filename)
        pl   = 18 if pfx == 1 else 8
        pfx  = f'{sf.f_lineno:4} {fp.stem:5} ' if pfx == 1 else ''
        msg  = f'{pfx}{sf.f_code.co_name:{pl}} ' + msg
    so = 0
    if   file == 0:  file = sys.stdout
    elif file == 1:  file = LOG_FILE
    elif file == 2:  file = LOG_FILE  ;  so = 1
    print(f'{msg}', flush=flush, sep=sep, end=end, file=file)
    print(f'{msg}', flush=flush, sep=sep, end=end, file=None) if so else None
########################################################################################################################################################################################################
def getFilePath(baseName, basePath, fdir='files', fsfx='.txt', dbg=1):
    if dbg: slog(f'{baseName =:12} {basePath = }', file=2)
    fileName      = baseName + fsfx
    filePath      = basePath / fdir / fileName
    if dbg: slog(f'{fileName =:12} {filePath = }', file=2)
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
    key = ''
    vals = []
    largs = len(sys.argv)
    if dbg: slog(f'argv={fmtl(sys.argv[1:])}')  ;  slog(f'{sys.argv[0]}', pfx=0)
    for j in range(1, largs):
        argv = sys.argv[j]
        if len(argv) > 2 and argv[0] == '-' and argv[1] == '-':
            if argv[2].isalpha():
                vals = []
                key = argv[2:]
                options[key] = vals
                if dbg: slog(f'{j:2} long    {argv:2} {key} {fmtl(vals)}', end=' ')
            else:
                slog(f'{j:2} ERROR long    {argv:2} {key} {fmtl(vals)}', end=' ')
        elif len(argv) > 1 and argv[0] == '-':
            if argv[1].isalpha() or argv[1] == '?':
                vals = []
                if len(argv) == 2:
                    key = argv[1:]
                    if dbg: slog(f'{j:2} short   {argv:2} {key} {fmtl(vals)}', end=' ')
                    options[key] = vals
                elif len(argv) > 2:
                    for i in range(1, len(argv)):
                        key = argv[i]
                        if dbg: slog(f'{j:2} short   {argv:2} {key} {fmtl(vals)}', end=' ')
                        options[key] = vals
            elif argv[1].isdigit():
                vals.append(argv)
                options[key] = vals
                if dbg: slog(f'{j:2} neg arg {argv:2} {key} {fmtl(vals)}', end=' ')
            else:
                vals.append(argv)
                options[key] = vals
                if dbg: slog(f'{j:2} ??? arg {argv:2} {key} {fmtl(vals)}', end=' ')
        else:
            vals.append(argv)
            options[key] = vals
            if dbg: slog(f'{j:2} arg     {argv:2} {key} {fmtl(vals)}', end=' ')
        if dbg: slog(pfx=0)
    if dbg: slog(f'options={fmtm(options)}')
    return options
########################################################################################################################################################################################################
class DSymb(object):
    SYMBS = {'X': 'mute', '/': 'slide', '\\': 'bend', '+': 'hammer', '~': 'vibrato', '^': 'tie', '.': 'staccato', '_': 'legato', '%': 'repeat', '|': 'bar', '[': 'groupL', ']': 'groupR'}
########################################################################################################################################################################################################
class Note(object):
    FLAT, SHRP = 0, 1
    TYPE       = FLAT
    TYPES      = ['FLAT', 'SHRP']
#    FS2N       = {'Cb':'B', 'B#':'C', 'Fb':'E', 'E#':'F'}
#    N2FS       = {'B':'Cb', 'C':'B#', 'E':'Fb', 'F':'E#'}
#    S2F2        = {           'C#':'Db', 'D#':'Eb',                       'F#':'Gb', 'G#':'Ab', 'A#':'Bb'}
#    F2S2        = {           'Db':'C#', 'Eb':'D#',                       'Gb':'F#', 'Ab':'G#', 'Bb':'A#'}
    S2F        = {'B#':'C' , 'C#':'Db', 'D#':'Eb', 'E' :'Fb', 'E#':'F' , 'F#':'Gb', 'G#':'Ab', 'A#':'Bb', 'B':'Cb' }
    F2S        = {'C' :'B#', 'Db':'C#', 'Eb':'D#', 'Fb':'E' , 'F' :'E#', 'Gb':'F#', 'Ab':'G#', 'Bb':'A#', 'Cb':'B' }

#    I2F        = {         0:'C' , 1:'Db', 2:'D' , 3:'Eb', 4:'E' ,                 5:'F' , 6:'Gb', 7:'G' , 8:'Ab', 9:'A' , 10:'Bb', 11:'B'  }
#    I2S        = {         0:'C' , 1:'C#', 2:'D' , 3:'D#', 4:'E' ,                 5:'F' , 6:'F#', 7:'G' , 8:'G#', 9:'A' , 10:'A#', 11:'B'  }
    I2F2       = {         0:'C' , 1:'Db', 2:'D' , 3:'Eb',         4:'Fb',         5:'F' , 6:'Gb', 7:'G' , 8:'Ab', 9:'A' , 10:'Bb',        11:'Cb' }
    I2S2       = { 0:'B#',         1:'C#', 2:'D' , 3:'D#', 4:'E' ,         5:'E#',         6:'F#', 7:'G' , 8:'G#', 9:'A' , 10:'A#', 11:'B'  }
    I2F        = {         0:'C' , 1:'Db', 2:'D' , 3:'Eb',         4:'Fb',         5:'F' , 6:'Gb', 7:'G' , 8:'Ab', 9:'A' , 10:'Bb',        11:'Cb' }
    I2S        = { 0:'B#',         1:'C#', 2:'D' , 3:'D#', 4:'E' ,         5:'E#',         6:'F#', 7:'G' , 8:'G#', 9:'A' , 10:'A#', 11:'B'  }

    N2I = { 'B#':0, 'C' :0, 'C#':1, 'Db':1, 'D' :2, 'D#':3, 'Eb':3, 'E' :4, 'Fb':4, 'E#':5, 'F' :5, 'F#':6, 'Gb':6, 'G' :7, 'G#':8, 'Ab':8, 'A' :9, 'A#':10, 'Bb':10, 'B' :11, 'Cb' :11 }
    MAX_IDX    = 10 * NTONES + 1
    I2N        = [I2F,  I2S]
    I2N2       = [I2F2, I2S2]

    @staticmethod
    def indices(k, o=0):
        key = k[:len(k)-1] if o else k
        i = Note.N2I[key]
        return i

    @staticmethod
    def setType(t): Note.TYPE = t

    @staticmethod
    def getName(i, t=-1, n2=0):
        t = t if t >= 0 else Note.TYPE
        name = Note.I2N2[t][i % NTONES] if n2 else Note.I2N[t][i % NTONES]
        return name

    @staticmethod
    def noteIv(n, iv, o=0):
        i = Note.indices(n, o)
        j = IVALR[iv]
        k = Note.indexI(i, j)
        m = Note.getName(k)
        return m

    @staticmethod
    def indexI(i, d):
        return (i + d) % NTONES
########################################################################################################################################################################################################
FLATS   = [ f'{k}{n}' for n in range(11) for k in Note.N2I.keys() if len(k) == 1 or len(k) > 1 and k[1] != '#' ][:Note.MAX_IDX]
SHRPS   = [ f'{k}{n}' for n in range(11) for k in Note.N2I.keys() if len(k) == 1 or len(k) > 1 and k[1] != 'b' ][:Note.MAX_IDX]

def FREQ( index): return 440 * pow(pow(2, 1/NTONES), index - 57)
def FREQ2(index): return 432 * pow(pow(2, 1/NTONES), index - 57)

FREQS   = [ FREQ( i) for i in range(Note.MAX_IDX) ]
FREQS2  = [ FREQ2(i) for i in range(Note.MAX_IDX) ]

def initKS(j=-7, m='Bb', iv='4', t=0):
    _ = {}  ;  k = 7
    for i in range(j, j+k, 1):
        _[m] = i
        n = Note.noteIv(m, iv)
        p = Note.indices(n, 0) % NTONES
        q = Note.getName(p, t=t, n2=1)
#        if m in Note.FS2N:
#            a = Note.FS2N[m]
#            _[a] = i
        slog(f'{i:2} {m:3} {iv:2} {n:3} {p:2} {q:3} {Note.TYPES[t]}')
        m = q
    return _
########################################################################################################################################################################################################

class KeySig(object):
    FO = initKS()
    SO = initKS(j=1, m='F#', iv='5', t=1)
    KO  = dict(FO)   ;  KO.update(SO)
    KS  =  dict()  ;   N = len(FO)
    for _ in range(-N, N+1, 1):        O = FO  if _ < 0 else SO    ;   KS[_] = list(O.keys())[:abs(_)]
    slog(f'FO ={fmtm(FO, w=2, d1="")}')
    slog(f'SO ={fmtm(SO, w=2, d1="")}')
    slog(f'KO ={fmtm(KO, w=2, d1="")}')
    slog(f'KS ={fmtm(KS, w=2, d1="")}')
    ########################################################################################################################################################################################################
    def __init__(self, k=0):
        self.k  = k
        self.ks = self.KS[self.k]
    def __str__( self):  return f'{self.k:2} {fmtl(self.ks)}'
    def __repr__(self):  return f'KeySig({self.k})'
    ########################################################################################################################################################################################################
    def tlog(self, i=None):
        if i is not None: i = i + 1
        ii = B*4  if i is None else f'{i:3} '
        slog(f'{ii}{ev(self)}')
        return i
    ########################################################################################################################################################################################################
    @classmethod
    def sortKS(cls, e): return sorted(e, key=lambda t: cls.KO[t])
    @classmethod
    def fKS(cls):      return f'{fmtm(cls.KS, w=2, d2=chr(10), ll=-1)}'
    ########################################################################################################################################################################################################
    @classmethod
    def test(cls):
        slog(cls.fKS(), pfx=0)
        cls.default()
        cls.test_1()
    ########################################################################################################################################################################################################
    @classmethod
    def default(cls, i=0):
        ks = KeySig()            ;  i = ks.tlog(i)
        ks = KeySig( 0)          ;  i = ks.tlog(i)
        ks = KeySig( 1)          ;  i = ks.tlog(i)
        ks = KeySig(-1)          ;  i = ks.tlog(i)
        ks = KeySig(k= 0)        ;  i = ks.tlog(i)
        ks = KeySig(k= 1)        ;  i = ks.tlog(i)
        ks = KeySig(k=-1)        ;  i = ks.tlog(i)
        return i
    @classmethod
    def test_1(cls, i=0, j=0):
        l = cls.N + j
        for n in range(-l, l+1, 1):
            ns = KeySig(n)  ;  i = ns.tlog(i)
        return i
########################################################################################################################################################################################################

class Strings(object):
    aliases = {'GUITAR_6_STD':    cOd([('E2', 28), ('A2', 33), ('D3', 38), ('G3', 43), ('B3', 47), ('E4', 52)]),
               'GUITAR_6_DROP_D': cOd([('D2', 26), ('A2', 33), ('D3', 38), ('G3', 43), ('B3', 47), ('E4', 52)]),
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

    def nStrings(self): return len(self.stringNames)

    def fn2ni(self, fn, s, dbg=0):
        strNum = self.nStrings() - s - 1    # Reverse and zero base the string numbering: str[1 ... numStrings] => s[(numStrings - 1) ... 0]
        k      = self.stringKeys[strNum]
        i      = self.stringMap[k] + fn
        if dbg: slog(f'fn={fn} s={s} strNum={strNum} k={k} i={i} stringMap={fmtm(self.stringMap)}')
        return i

    def tab2nn(self, tab, s, dbg=0):
        fn   = self.tab2fn(tab)
        i    = self.fn2ni(fn, s)
        name = Note.getName(i)
        if dbg: slog(f'tab={tab} s={s} fn={fn} i={i} name={name}')
        return name

    @staticmethod
    def isFret(txt):             return 1 if '0' <= txt <= '9'  or 'a' <= txt <= 'o'   else 0
    @staticmethod
    def tab2fn(tab, dbg=0): fn = int(tab) if '0' <= tab <= '9' else int(ord(tab) - 87) if 'a' <= tab <= 'o' else None  ;  slog(f'tab={tab} fretNum={fn}') if dbg else None  ;  return fn
########################################################################################################################################################################################################

class Mode(object):
    NAMES = 'IONIAN', 'DORIAN', 'PHRYGIAN', 'LYDIAN', 'MIXOLYDIAN', 'AEOLIAN', 'LOCRIAN'
    def __init__(self, name='IONIAN', tonic='C', ks=0):
        self.name  = name
        self.tonic = tonic
        self.ks    = ks
#class COFs(object):
#    CO5s = ['C', 'G', 'D' , 'A' , 'E' , 'B' , 'F#', 'C#']
#    CO4s = ['C', 'F', 'Bb', 'Eb', 'Ab', 'Db', 'Gb', 'Cb']
########################################################################################################################################################################################################
class Test:
    def __init__(self, a): self._a = a  ;  slog(f'<Test_init_:     _a={self._a}>', pfx=1)
    @property
    def a(self):                           slog(f'<Test_prop_a:     _a={self._a}>', pfx=1)
    @a.setter
    def a(self, a):        self._a = a  ;  slog(f'<Test_set_a:     _a={self._a}>', pfx=1)
    @a.getter
    def a(self):                           slog(f'<Test_get_a:     _a={self._a}>', pfx=1)  ;  return self._a
    @a.deleter
    def a(self):                           slog(f'<Test_del_a: del _a>', pfx=1)  ;  del self._a
