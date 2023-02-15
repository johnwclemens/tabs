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
    S2F        = {           'C#':'Db', 'D#':'Eb',                       'F#':'Gb', 'G#':'Ab', 'A#':'Bb'}
    F2S        = {           'Db':'C#', 'Eb':'D#',                       'Gb':'F#', 'Ab':'G#', 'Bb':'A#'}
#   S2F2       = {'B#':'C' , 'C#':'Db', 'D#':'Eb',            'E#':'F' , 'F#':'Gb', 'G#':'Ab', 'A#':'Bb'}
#   F2S2       = {           'Db':'C#', 'Eb':'D#', 'Fb':'E' ,            'Gb':'F#', 'Ab':'G#', 'Bb':'A#', 'Cb':'B'  }

    I2F      = {         0:'C' , 1:'Db', 2:'D' , 3:'Eb', 4:'E' ,                 5:'F' , 6:'Gb', 7:'G' , 8:'Ab', 9:'A' , 10:'Bb', 11:'B'  }
    I2S      = {         0:'C' , 1:'C#', 2:'D' , 3:'D#', 4:'E' ,                 5:'F' , 6:'F#', 7:'G' , 8:'G#', 9:'A' , 10:'A#', 11:'B'  }
    I2F2     = {         0:'C' , 1:'Db', 2:'D' , 3:'Eb',         4:'Fb',         5:'F' , 6:'Gb', 7:'G' , 8:'Ab', 9:'A' , 10:'Bb',        11:'Cb' }
    I2S2     = { 0:'B#',         1:'C#', 2:'D' , 3:'D#', 4:'E' ,         5:'E#',         6:'F#', 7:'G' , 8:'G#', 9:'A' , 10:'A#', 11:'B'  }

#   N2I = {         'C' :0, 'C#':1, 'Db':1, 'D': 2, 'D#':3, 'Eb':3, 'E' :4,                 'F' :5, 'F#':6, 'Gb':6, 'G' :7, 'G#':8, 'Ab':8, 'A' :9, 'A#':10, 'Bb':10, 'B' :11 }
    N2I = { 'B#':0, 'C' :0, 'C#':1, 'Db':1, 'D' :2, 'D#':3, 'Eb':3, 'E' :4, 'Fb':4, 'E#':5, 'F' :5, 'F#':6, 'Gb':6, 'G' :7, 'G#':8, 'Ab':8, 'A' :9, 'A#':10, 'Bb':10, 'B' :11, 'Cb' : 11 }
    MAX_IDX = 10 * NTONES + 1
    I2N  = [I2F,  I2S]
    I2N2 = [I2F2, I2S2]
#    OLD_INDICES = {#'C' : 0, 'C#' : 1, 'Db' : 1, 'D' : 2, 'D#' : 3, 'Eb' : 3, 'E' : 4, 'F' : 5, 'F#' : 6, 'Gb' : 6, 'G' : 7, 'G#' : 8, 'Ab' : 8, 'A' : 9, 'A#' :10, 'Bb' :10, 'B' :11,
#                'C0': 0, 'C#0': 1, 'Db0': 1, 'D0': 2, 'D#0': 3, 'Eb0': 3, 'E0': 4, 'F0': 5, 'F#0': 6, 'Gb0': 6, 'G0': 7, 'G#0': 8, 'Ab0': 8, 'A0': 9, 'A#0':10, 'Bb0':10, 'B0':11,
#                'C1':12, 'C#1':13, 'Db1':13, 'D1':14, 'D#1':15, 'Eb1':15, 'E1':16, 'F1':17, 'F#1':18, 'Gb1':18, 'G1':19, 'G#1':20, 'Ab1':20, 'A1':21, 'A#1':22, 'Bb1':22, 'B1':23,
#                'C2':24, 'C#2':25, 'Db2':25, 'D2':26, 'D#2':27, 'Eb2':27, 'E2':28, 'F2':29, 'F#2':30, 'Gb2':30, 'G2':31, 'G#2':32, 'Ab2':32, 'A2':33, 'A#2':34, 'Bb2':34, 'B2':35,
#                'C3':36, 'C#3':37, 'Db3':37, 'D3':38, 'D#3':39, 'Eb3':39, 'E3':40, 'F3':41, 'F#3':42, 'Gb3':42, 'G3':43, 'G#3':44, 'Ab3':44, 'A3':45, 'A#3':46, 'Bb3':46, 'B3':47,
#                'C4':48, 'C#4':49, 'Db4':49, 'D4':50, 'D#4':51, 'Eb4':51, 'E4':52, 'F4':53, 'F#4':54, 'Gb4':54, 'G4':55, 'G#4':56, 'Ab4':56, 'A4':57, 'A#4':58, 'Bb4':58, 'B4':59,
#                'C5':60, 'C#5':61, 'Db5':61, 'D5':62, 'D#5':63, 'Eb5':63, 'E5':64, 'F5':65, 'F#5':66, 'Gb5':66, 'G5':67, 'G#5':68, 'Ab5':68, 'A5':69, 'A#5':70, 'Bb5':70, 'B5':71,
#                'C6':72, 'C#6':73, 'Db6':73, 'D6':74, 'D#6':75, 'Eb6':75, 'E6':76, 'F6':77, 'F#6':78, 'Gb6':78, 'G6':79, 'G#6':80, 'Ab6':80, 'A6':81, 'A#6':82, 'Bb6':82, 'B6':83,
#                'C7':84, 'C#7':85, 'Db7':85, 'D7':86, 'D#7':87, 'Eb7':87, 'E7':88, 'F7':89, 'F#7':90, 'Gb7':90, 'G7':91, 'G#7':92, 'Ab7':92, 'A7':93, 'A#7':94, 'Bb7':94, 'B7':95,
#                'C8':96 } # For simplicity omit double flats and double sharps and other redundant enharmonic note names e.g. Abb, C##, Cb, B#, Fb, E# etc...
#                 99    FLATS
# C0 Db0  D0 Eb0  E0  F0 Gb0  G0 Ab0  A0 Bb0  B0  C1 Db1  D1 Eb1  E1  F1 Gb1  G1 Ab1  A1 Bb1  B1  C2 Db2  D2 Eb2  E2  F2 Gb2  G2 Ab2  A2 Bb2  B2  C3 Db3  D3 Eb3  E3  F3 Gb3  G3 Ab3  A3 Bb3  B3  C4 Db4  D4 Eb4  E4  F4 Gb4  G4 Ab4  A4 Bb4  B4  C5 Db5  D5 Eb5  E5  F5 Gb5  G5 Ab5  A5 Bb5  B5  C6 Db6  D6 Eb6  E6  F6 Gb6  G6 Ab6  A6 Bb6  B6  C7 Db7  D7 Eb7  E7  F7 Gb7  G7 Ab7  A7 Bb7  B7  C8 Db8  D8
#  1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19  20  21  22  23  24  25  26  27  28  29  30  31  32  33  34  35  36  37  38  39  40  41  42  43  44  45  46  47  48  49  50  51  52  53  54  55  56  57  58  59  60  61  62  63  64  65  66  67  68  69  70  71  72  73  74  75  76  77  78  79  80  81  82  83  84  85  86  87  88  89  90  91  92  93  94  95  96  97  98  99
# C0 C#0  D0 D#0  E0  F0 F#0  G0 G#0  A0 A#0  B0  C1 C#1  D1 D#1  E1  F1 F#1  G1 G#1  A1 A#1  B1  C2 C#2  D2 D#2  E2  F2 F#2  G2 G#2  A2 A#2  B2  C3 C#3  D3 D#3  E3  F3 F#3  G3 G#3  A3 A#3  B3  C4 C#4  D4 D#4  E4  F4 F#4  G4 G#4  A4 A#4  B4  C5 C#5  D5 D#5  E5  F5 F#5  G5 G#5  A5 A#5  B5  C6 C#6  D6 D#6  E6  F6 F#6  G6 G#6  A6 A#6  B6  C7 C#7  D7 D#7  E7  F7 F#7  G7 G#7  A7 A#7  B7  C8 C#8  D8

    @staticmethod
    def indices(k, o=0):
        key = k[:len(k)-1] if o else k
        i = Note.N2I[key]
        return i

    @staticmethod
    def setType(t): Note.TYPE = t

    @staticmethod
    def getName(i, t=-1):
        t = t if t >= 0 else Note.TYPE
        name = Note.I2N[t][i % NTONES]
        return name

    @staticmethod
    def getName2(i, t=-1):
        t = t if t >= 0 else Note.TYPE
        name = Note.I2N2[t][i % NTONES]
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
#FLATS   =[ f'{k}{n}' for n in range(9) for k in Note.INDICES.keys() if len(k) == 1 or len(k) > 1 and k[1] != '#' ][:Note.MAX_IDX]
#SHRPS   =[ f'{k}{n}' for n in range(9) for k in Note.INDICES.keys() if len(k) == 1 or len(k) > 1 and k[1] != 'b' ][:Note.MAX_IDX]
FLATS   = [ f'{k}{n}' for n in range(11) for k in Note.N2I.keys() if len(k) == 1 or len(k) > 1 and k[1] != '#' ][:Note.MAX_IDX]
SHRPS   = [ f'{k}{n}' for n in range(11) for k in Note.N2I.keys() if len(k) == 1 or len(k) > 1 and k[1] != 'b' ][:Note.MAX_IDX]

def FREQ( index): return 440 * pow(pow(2, 1/NTONES), index - 57)
def FREQ2(index): return 432 * pow(pow(2, 1/NTONES), index - 57)

FREQS   = [ FREQ( i) for i in range(Note.MAX_IDX) ]
FREQS2  = [ FREQ2(i) for i in range(Note.MAX_IDX) ]

def OLD__initO():
    _, j, m, iv, iw = [], 7, 'F', '4', 0
    for i in range(-j, j+1, 1):
        t = 0 if i < 0 else 1
        if i==0:   m, iv = 'B', '5'  ;  continue
        n = Note.noteIv(m, iv)
        p = (Note.indices(n, 0) - iw) % NTONES
        q = Note.getName2(p, t=t)
        slog(f'{i:2} {m:3} {iv:2} {n:3} {p:2} {q:3} {Note.TYPES[t]}')
        _.append(q)   ;   m = n
    return _
def OLD__init1(j=7, m='F#', iv='5', t=1):
    _ = []  ;  k = 1 if t else -1  ;  j *= k
    for i in range(k, j+k, k):
        _.append(m)
        n = Note.noteIv(m, iv)
        p = Note.indices(n, 0) % NTONES
        q = Note.getName2(p, t=t)
        slog(f'{i:2} {m:3} {iv:2} {n:3} {p:2} {q:3} {Note.TYPES[t]}')
        m = q
    return _
def OLD__initKS(j=7, m='F#', iv='5', t=1):
    _ = {}  ;  k = 1 if t else -1  ;  j *= k
    for i in range(k, j+k, k):
        _[m] = i
        n = Note.noteIv(m, iv)
        p = Note.indices(n, 0) % NTONES
        q = Note.getName2(p, t=t)
        slog(f'{i:2} {m:3} {iv:2} {n:3} {p:2} {q:3} {Note.TYPES[t]}')
        m = q
    return _
def initKSA(j=7, m='F#', iv='5', t=1):
    _ = {}  ;  k = 1 if t else -1  ;  j *= k
    for i in range(k, j+k, k):
        _[m] = i
        n = Note.noteIv(m, iv)
        p = Note.indices(n, 0) % NTONES
        q = Note.getName2(p, t=t)
        slog(f'{i:2} {m:3} {iv:2} {n:3} {p:2} {q:3} {Note.TYPES[t]}')
        m = q
    return _
def initKS(j=7, m='F#', iv='5', t=1):
    _ = {}  ;  a = 1 if t else -j  ;  b = j+1 if t else 0
    for i in range(a, b):
        _[m] = i
        n = Note.noteIv(m, iv)
        p = Note.indices(n, 0) % NTONES
        q = Note.getName2(p, t=t)
        slog(f'{i:2} {m:3} {iv:2} {n:3} {p:2} {q:3} {Note.TYPES[t]}')
        m = q
    return _
########################################################################################################################################################################################################

class KeySig(object):
    FO  = {'Bb':-7, 'Eb':-6, 'Ab':-5, 'Db':-4, 'Gb':-3, 'Cb':-2, 'Fb':-1}
    SO  = {'F#': 1, 'C#': 2, 'G#': 3, 'D#': 4, 'A#': 5, 'E#': 6, 'B#': 7}
    SO2 = initKS()
    FO2 = initKS(m='Bb', iv='4', t=0)
    KO  = dict(FO)   ;  KO.update(SO)  ;  KS  =  dict()  ;   N = len(FO)
    KO2 = dict(FO2)  ;  KO2.update(SO2)
    for _ in range(-N, N+1, 1):
        O = FO  if _ < 0 else SO    ;   KS[_] = list(O.keys())[:abs(_)]
    slog(f'FO ={fmtm(FO, w=2, d1="")}')  ;  slog(f'FO2={fmtm(FO2, w=2, d1="")}')
    slog(f'SO ={fmtm(SO, w=2, d1="")}')  ;  slog(f'SO2={fmtm(SO2, w=2, d1="")}')
    slog(f'KO ={fmtm(KO, w=2, d1="")}')  ;  slog(f'KO2={fmtm(KO2, w=2, d1="")}')
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

    def tab2nn(self, tab, s, n2=0, dbg=0):
        fn   = self.tab2fn(tab)
        i    = self.fn2ni(fn, s)
        name = Note.getName2(i) if n2 else Note.getName(i)
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
