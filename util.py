"""util.py module.  class list: [DSymb, Note, Strings, Test]."""
import sys, os, inspect, pathlib
from collections import OrderedDict as cOd

B                = ' '
PASS, FAIL, DFLT = 'PASS', 'FAIL', 'DFLT'
OIDS             = 0
LOG_FILE         = None
MIN_IVAL_LEN     = 1
MAX_STACK_DEPTH  = 0
MAX_STACK_FRAME  = inspect.stack()
M12              = { 10:'a', 11:'b' }
INTERVALS        = { 0:'R', 1:'b2', 2:'2', 3:'m3', 4:'M3', 5:'4', 6:'b5', 7:'5', 8:'#5', 9:'6', 10:'b7', 11:'7' }
INTERVAL_RANK    = { 'R':0, 'b2':1, '2':2, 'm3':3, 'M3':4, '4':5, 'b5':6, '5':7, '#5':8, '6':9, 'b7':10, '7':11 }
NTONES           = len(INTERVALS)
INIT             = '###   Init   ###'     * 13
QUIT_BGN         = '###   BGN Quit   ###' * 10
QUIT             = '###   Quit   ###'     * 13
QUIT_END         = '###   END Quit   ###' * 10
#STFILT = ['log', 'dumpGeom', 'resetJ', 'dumpJs', 'dumpImap', 'dumpSmap', 'dumpCursorArrows', '<listcomp>', 'dumpLimap2', 'dumpTniksPfx', 'dumpTniksSfx']
STFILT = ['log', 'tlog', 'dumpGeom', 'resetJ', 'dumpJs', 'dumpImap', 'dumpSmap', 'dumpCursorArrows', '<listcomp>', 'dumpLimap2', 'dumpTniksPfx', 'dumpTniksSfx', 'fmtXYWH', 'kbkInfo', 'dumpCrs', 'fCrsCrt'] # , 'dumpView', 'dumpLbox', 'dumpRect']
########################################################################################################################################################################################################
def init(file, oid):  global LOG_FILE  ;  LOG_FILE = file  ;  global OIDS  ;  OIDS = oid

def fmtl(lst, w=None, u='>', d1='[', d2=']', sep=' ', ll=None, z=''):
    if lst is None: return 'None'
    lts = (list, tuple, set, frozenset)  ;  dts = (int, float, str)
    assert type(lst) in lts, f'{type(lst)=} {lts=}'
    if d1 == ''  :  d2 = ''
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
    t = ''
    for k, v in m.items():
        if   type(v) in (list, tuple, set):         t += f'{d1}{k:{w}}{d0}{fmtl(v, w, ll=KeySig.Ls[k] if ll==-1 else ll)}{d2} '
        elif type(v) in (int, str):                 t += f'{d1}{k:>{w}}{d0}{v:<{w}}{d2} '
    return d1 + t.rstrip() + d2

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
    FLAT, SHARP = 0, 1
    TYPE        = FLAT
    TYPES       = ['FLAT', 'SHARP']
    S2F         = {'C#':'Db', 'D#':'Eb', 'F#':'Gb', 'G#':'Ab', 'A#':'Bb'}
    F2S         = {'Db':'C#', 'Eb':'D#', 'Gb':'F#', 'Ab':'G#', 'Bb':'A#'}
    SHARPS      = { 0:'C', 1:'C#', 2:'D', 3:'D#', 4:'E', 5:'F', 6:'F#', 7:'G', 8:'G#', 9:'A', 10:'A#', 11:'B' }
    FLATS       = { 0:'C', 1:'Db', 2:'D', 3:'Eb', 4:'E', 5:'F', 6:'Gb', 7:'G', 8:'Ab', 9:'A', 10:'Bb', 11:'B' }
    TONES       = [FLATS, SHARPS]
    MAX_INDEX   = 97
    INDICES = { 'C0': 0, 'C#0': 1, 'Db0': 1, 'D0': 2, 'D#0': 3, 'Eb0': 3, 'E0': 4, 'F0': 5, 'F#0': 6, 'Gb0': 6, 'G0': 7, 'G#0': 8, 'Ab0': 8, 'A0': 9, 'A#0':10, 'Bb0':10, 'B0':11,
                'C1':12, 'C#1':13, 'Db1':13, 'D1':14, 'D#1':15, 'Eb1':15, 'E1':16, 'F1':17, 'F#1':18, 'Gb1':18, 'G1':19, 'G#1':20, 'Ab1':20, 'A1':21, 'A#1':22, 'Bb1':22, 'B1':23,
                'C2':24, 'C#2':25, 'Db2':25, 'D2':26, 'D#2':27, 'Eb2':27, 'E2':28, 'F2':29, 'F#2':30, 'Gb2':30, 'G2':31, 'G#2':32, 'Ab2':32, 'A2':33, 'A#2':34, 'Bb2':34, 'B2':35,
                'C3':36, 'C#3':37, 'Db3':37, 'D3':38, 'D#3':39, 'Eb3':39, 'E3':40, 'F3':41, 'F#3':42, 'Gb3':42, 'G3':43, 'G#3':44, 'Ab3':44, 'A3':45, 'A#3':46, 'Bb3':46, 'B3':47,
                'C4':48, 'C#4':49, 'Db4':49, 'D4':50, 'D#4':51, 'Eb4':51, 'E4':52, 'F4':53, 'F#4':54, 'Gb4':54, 'G4':55, 'G#4':56, 'Ab4':56, 'A4':57, 'A#4':58, 'Bb4':58, 'B4':59,
                'C5':60, 'C#5':61, 'Db5':61, 'D5':62, 'D#5':63, 'Eb5':63, 'E5':64, 'F5':65, 'F#5':66, 'Gb5':66, 'G5':67, 'G#5':68, 'Ab5':68, 'A5':69, 'A#5':70, 'Bb5':70, 'B5':71,
                'C6':72, 'C#6':73, 'Db6':73, 'D6':74, 'D#6':75, 'Eb6':75, 'E6':76, 'F6':77, 'F#6':78, 'Gb6':78, 'G6':79, 'G#6':80, 'Ab6':80, 'A6':81, 'A#6':82, 'Bb6':82, 'B6':83,
                'C7':84, 'C#7':85, 'Db7':85, 'D7':86, 'D#7':87, 'Eb7':87, 'E7':88, 'F7':89, 'F#7':90, 'Gb7':90, 'G7':91, 'G#7':92, 'Ab7':92, 'A7':93, 'A#7':94, 'Bb7':94, 'B7':95,
                'C8':96 } # For simplicity omit double flats and double sharps and other redundant enharmonic note names e.g. Abb, C##, Cb, B#, Fb, E# etc...
    SNAMES   = [ k for k in INDICES.keys() if k[1] != '#' ]
    FNAMES   = [ k for k in INDICES.keys() if k[1] != 'b' ]

    @staticmethod
    def setType(t): Note.TYPE = t

    @staticmethod
    def getName(i):
        name = Note.TONES[Note.TYPE][i % NTONES]
        return name
########################################################################################################################################################################################################
def FREQ( index): return 440 * pow(pow(2, 1/NTONES), index - 57)
def FREQ2(index): return 432 * pow(pow(2, 1/NTONES), index - 57)
FREQS   = [ FREQ( i) for i in range(Note.MAX_INDEX) ]
FREQS2  = [ FREQ2(i) for i in range(Note.MAX_INDEX) ]

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
class KeySig(object):
#    S2F = {'B':'Cb', 'F#':'Gb', 'C#':'Db', 'G#':'Ab', 'D#':'Eb', 'A#':'Bb', 'E#':'F', 'B#':'C', 'Fb':'E'}
#    F2S = {'Cb':'B', 'Gb':'F#', 'Db':'C#', 'Ab':'G#', 'Eb':'D#', 'Bb':'A#', 'F':'E#', 'C':'B#', 'E':'Fb'}
    S2F = {'B#':'C' , 'C#':'Db', 'D#':'Eb', 'E' :'Fb', 'E#':'F' , 'F#':'Gb', 'G#':'Ab', 'A#':'Bb', 'B' :'Cb'}
    F2S = {'C' :'B#', 'Db':'C#', 'Eb':'D#', 'Fb':'E' , 'F' :'E#', 'Gb':'F#', 'Ab':'G#', 'Bb':'A#', 'Cb':'B' }
    Ks  = dict()  ;  Ls = dict()
    _ = 'Cb'  ;  Cb = ['Cb', 'Db', 'Eb', 'Fb', 'Gb', 'Ab', 'Bb']  ;  Ks[_] = ['Bb', 'Eb', 'Ab', 'Db', 'Gb', 'Cb', 'Fb']  ;  Ls[_] = -len(Ks[_])
    _ = 'Gb'  ;  Gb = ['Gb', 'Ab', 'Bb', 'Cb', 'Db', 'Eb', 'F' ]  ;  Ks[_] = ['Bb', 'Eb', 'Ab', 'Db', 'Gb', 'Cb']        ;  Ls[_] = -len(Ks[_])
    _ = 'Db'  ;  Db = ['Db', 'Eb', 'F' , 'Gb', 'Ab', 'Bb', 'C' ]  ;  Ks[_] = ['Bb', 'Eb', 'Ab', 'Db', 'Gb']              ;  Ls[_] = -len(Ks[_])
    _ = 'Ab'  ;  Ab = ['Ab', 'Bb', 'C' , 'Db', 'Eb', 'F' , 'G' ]  ;  Ks[_] = ['Bb', 'Eb', 'Ab', 'Db']                    ;  Ls[_] = -len(Ks[_])
    _ = 'Eb'  ;  Eb = ['Eb', 'F' , 'G' , 'Ab', 'Bb', 'C' , 'D' ]  ;  Ks[_] = ['Bb', 'Eb', 'Ab']                          ;  Ls[_] = -len(Ks[_])
    _ = 'Bb'  ;  Bb = ['Bb', 'C' , 'D' , 'Eb', 'F' , 'G' , 'A' ]  ;  Ks[_] = ['Bb', 'Eb']                                ;  Ls[_] = -len(Ks[_])
    _ = 'F'   ;  F  = ['F' , 'G' , 'A' , 'Bb', 'C' , 'D' , 'E' ]  ;  Ks[_] = ['Bb']                                      ;  Ls[_] = -len(Ks[_])
    _ = 'C'   ;  C  = ['C' , 'D' , 'E' , 'F' , 'G' , 'A' , 'B' ]  ;  Ks[_] = []                                          ;  Ls[_] =  len(Ks[_])
    _ = 'G'   ;  G  = ['G' , 'A' , 'B' , 'C' , 'D' , 'E' , 'F#']  ;  Ks[_] = ['F#']                                      ;  Ls[_] =  len(Ks[_])
    _ = 'D'   ;  D  = ['D' , 'E' , 'F#', 'G' , 'A' , 'B' , 'C#']  ;  Ks[_] = ['F#', 'C#']                                ;  Ls[_] =  len(Ks[_])
    _ = 'A'   ;  A  = ['A' , 'B' , 'C#', 'D' , 'E' , 'F#', 'G#']  ;  Ks[_] = ['F#', 'C#', 'G#']                          ;  Ls[_] =  len(Ks[_])
    _ = 'E'   ;  E  = ['E' , 'F#', 'G#', 'A' , 'B' , 'C#', 'D#']  ;  Ks[_] = ['F#', 'C#', 'G#', 'D#']                    ;  Ls[_] =  len(Ks[_])
    _ = 'B'   ;  B  = ['B' , 'C#', 'D#', 'E' , 'F#', 'G#', 'A#']  ;  Ks[_] = ['F#', 'C#', 'G#', 'D#', 'A#']              ;  Ls[_] =  len(Ks[_])
    _ = 'F#'  ;  Fs = ['F#', 'G#', 'A#', 'B' , 'C#', 'D#', 'E#']  ;  Ks[_] = ['F#', 'C#', 'G#', 'D#', 'A#', 'E#']        ;  Ls[_] =  len(Ks[_])
    _ = 'C#'  ;  Cs = ['C#', 'D#', 'E#', 'F#', 'G#', 'A#', 'B#']  ;  Ks[_] = ['F#', 'C#', 'G#', 'D#', 'A#', 'E#', 'B#']  ;  Ls[_] =  len(Ks[_])
    L = len(Ls) // 2
    ########################################################################################################################################################################################################
    def __str__(self):
        k = self.k  ;  ls, ks = '', ''
        if k in self.Ls: ls = f'{self.Ls[k]:2}'
        if k in self.Ks: ks = f'{fmtl(self.Ks[k])}'
        k = B*2 if k is None else k
        return f'{self.r} [{k:2} {ls:2}] {ks:22}'

    def __repr__(self):
        k = self.k   ;   l = self.l
        k = B*2 if k is None else k  ;  l = B*2 if l is None else l
        return f'{k:2} {l:2}'

    def __init__(self, k=None, l=None):
        self.ks = []  ;  self.ks.append(self.fmt(k)) if k else None
        self.ls = []  ;  self.ls.append(self.fmt(l)) if l is not None else None
        self.d, self.k, self.l, self.r = self.info(k, l)
    ########################################################################################################################################################################################################
    def info(self, k=None, l=None):
        if   self.hasNoKL(k, l):                    d = 'has No KL'        ;  k = 'C'          ;  l = self.Ls[k]  ;  r = DFLT
        elif self.hasKL(k, l) and self.isKL(k, l):
            klv = self.klv(k, l)
            if klv[0]:                              d = 'hasKL isKL  klv'  ;  k = klv[1][0]    ;  l = klv[2][0]   ;  r = PASS
            else:                                   d = 'hasKL isKL !klv'  ;  k = klv[1][1]    ;  l = klv[2][1]   ;  r = FAIL
        elif self.hasL(    l) and     self.isL(l):  d =  'hasL  isL'       ;  k = self.l2k(l)  ;  l = self.Ls[k]  ;  r = PASS
        elif self.hasL(    l) and not self.isL(l):  d = f'hasL !isL={l}'   ;                                         r = FAIL # self.k = k  ;  self.l = l
        elif self.hasK(    k) and     self.isK(k):  d =  'hasK  isK'       ;                      l = self.Ls[k]  ;  r = PASS
        elif self.hasK(    k) and not self.isK(k):  d = f'hask !isK={k}'   ;                                         r = FAIL # self.k = k  ;  self.l = l
        else:                                       d = f'ERROR {k=} {l=}' ;                                         r = FAIL # self.k = k  ;  self.l = l
        if     r == FAIL:    self.ks.append(self.fmt(k))   ;   self.ls.append(self.fmt(l))
        return d, k, l, r
    ########################################################################################################################################################################################################
    def tlog(self, i=None):
        if i is not None: i = i + 1
        ii = B*4  if i is None else f'{i:3} '
        kls = [ f'[{self.ks[i] if len(self.ks)>i else B*2} {self.ls[i] if len(self.ls)>i else B*2}]' for i in range(max(len(self.ks), len(self.ls))) ]
        slog(f'{ii}{self.d:15} {fmtl(kls, d1="", sep=""):14} {self!s}', pfx=2, file=1)
        return i
    ########################################################################################################################################################################################################
    def klv(self, k, l):
        kv = 1 if k == self.l2k(l) else 0
        lv = 1 if l == self.Ls[k]  else 0
        v = kv * lv   ;   ks = [k, self.l2k(l)]   ;   ls = [l, self.Ls[k]]
        return v, ks, ls

    def l2k(   self, l, dbg=0):
        for k, v in self.Ls.items():
            if v==l:
                slog(f'{k=} {v=} {l=}') if dbg else None  ;  return k
    ########################################################################################################################################################################################################
    def isK(   self, k):    return 1 if k     in self.Ks                            else 0
    def isL(   self, l):    return 1 if                      -self.L <= l <= self.L else 0
    def isKL(  self, k, l): return 1 if k     in self.Ks and -self.L <= l <= self.L else 0
#    def isNoKL(self, k, l): return 1 if k not in self.Ks and -self.L >= l >= self.L else 0
    @staticmethod
    def hasNoKL(k, l): return 1 if k is     None and l is     None else 0
    @staticmethod
    def hasK(   k   ): return 0 if k is None else 1
    @staticmethod
    def hasL(      l): return 0 if l is None else 1
    @staticmethod
    def hasKL(  k, l): return 0 if k is None or l is None else 1
    @staticmethod
    def fmt(a):        return B*2 if a is None else f'{a:2}'
    @classmethod
    def fLs(cls):      return f'{fmtm(cls.Ls)}'
    @classmethod
    def fKs(cls):      return f'{fmtm(cls.Ks, w=2, d2=chr(10), ll=-1)}'
    ########################################################################################################################################################################################################
    def test(self, i=0):
        slog(self.fKs(), pfx=0)
        slog(self.fLs())
        self.test_1A()
        self.test_1B()
        self.test_2A()
        self.test_2B()
        self.test_3A()
        self.test_3B()
#        i = self.test_1(i)
#        i = self.test_2(i)
#        i = self.test_3(i)
#        i = self.test_4(i)
        return i
    ########################################################################################################################################################################################################
    @classmethod
    def test_1A(cls, i=0, j=0):
        l = len(cls.Ls) // 2 + j
        for k in cls.Ls.keys():
            for n in range(-l, l+1, 1):
                ks = KeySig(k=k, l=n)  ;  i = ks.tlog(i)
        return i

    @classmethod
    def test_1B(cls, i=0, j=0):
        l = len(cls.Ls) // 2 + j
        for n in range(l, -l-1, -1):
            for k in cls.Ls.keys():
                ks = KeySig(k=k, l=n)  ;  i = ks.tlog(i)
        return i
    ########################################################################################################################################################################################################
    @classmethod
    def test_2A(cls, i=0):
        for k in cls.Ls.keys():
            ks = KeySig(k=k)  ;  i = ks.tlog(i)
        return i

    @classmethod
    def test_2B(cls, i=0):
        for k in cls.Ls.keys():
            ks = KeySig(k=k)  ;  i = ks.tlog(i)
        return i
    ########################################################################################################################################################################################################
    @classmethod
    def test_3A(cls, i=0, j=0):
        l = len(cls.Ls) // 2 + j
        for n in range(-l, l+1, 1):
            ks = KeySig(l=n)  ;  i = ks.tlog(i)
        return i

    @classmethod
    def test_3B(cls, i=0, j=0):
        l = len(cls.Ls) // 2 + j
        for n in range(l, -l-1, -1):
            ks = KeySig(l=n)  ;  i = ks.tlog(i)
        return i
    ########################################################################################################################################################################################################
    @classmethod
    def test_1(cls, i):
        ks = KeySig('Cb')  ;  i = ks.tlog(i)
        ks = KeySig('Gb')  ;  i = ks.tlog(i)
        ks = KeySig('Db')  ;  i = ks.tlog(i)
        ks = KeySig('Ab')  ;  i = ks.tlog(i)
        ks = KeySig('Eb')  ;  i = ks.tlog(i)
        ks = KeySig('Bb')  ;  i = ks.tlog(i)
        ks = KeySig('F')   ;  i = ks.tlog(i)
        ks = KeySig('C')   ;  i = ks.tlog(i)
        ks = KeySig('G')   ;  i = ks.tlog(i)
        ks = KeySig('D')   ;  i = ks.tlog(i)
        ks = KeySig('A')   ;  i = ks.tlog(i)
        ks = KeySig('E')   ;  i = ks.tlog(i)
        ks = KeySig('B')   ;  i = ks.tlog(i)
        ks = KeySig('F#')  ;  i = ks.tlog(i)
        ks = KeySig('C#')  ;  i = ks.tlog(i)
        return i

    @classmethod
    def test_2(cls, i):
        ks = KeySig('C#')  ;  i = ks.tlog(i)
        ks = KeySig('F#')  ;  i = ks.tlog(i)
        ks = KeySig('B')   ;  i = ks.tlog(i)
        ks = KeySig('E')   ;  i = ks.tlog(i)
        ks = KeySig('A')   ;  i = ks.tlog(i)
        ks = KeySig('D')   ;  i = ks.tlog(i)
        ks = KeySig('G')   ;  i = ks.tlog(i)
        ks = KeySig('C')   ;  i = ks.tlog(i)
        ks = KeySig('F')   ;  i = ks.tlog(i)
        ks = KeySig('Bb')  ;  i = ks.tlog(i)
        ks = KeySig('Eb')  ;  i = ks.tlog(i)
        ks = KeySig('Ab')  ;  i = ks.tlog(i)
        ks = KeySig('Db')  ;  i = ks.tlog(i)
        ks = KeySig('Gb')  ;  i = ks.tlog(i)
        ks = KeySig('Cb')  ;  i = ks.tlog(i)
        return i

    @classmethod
    def test_3(cls, i):
        ks = KeySig('Cb', -7)  ;  i = ks.tlog(i)
        ks = KeySig('Gb', -6)  ;  i = ks.tlog(i)
        ks = KeySig('Db', -5)  ;  i = ks.tlog(i)
        ks = KeySig('Ab', -4)  ;  i = ks.tlog(i)
        ks = KeySig('Eb', -3)  ;  i = ks.tlog(i)
        ks = KeySig('Bb', -2)  ;  i = ks.tlog(i)
        ks = KeySig('F' , -1)  ;  i = ks.tlog(i)
        ks = KeySig('C' ,  0)  ;  i = ks.tlog(i)
        ks = KeySig('G' ,  1)  ;  i = ks.tlog(i)
        ks = KeySig('D' ,  2)  ;  i = ks.tlog(i)
        ks = KeySig('A' ,  3)  ;  i = ks.tlog(i)
        ks = KeySig('E' ,  4)  ;  i = ks.tlog(i)
        ks = KeySig('B' ,  5)  ;  i = ks.tlog(i)
        ks = KeySig('F#',  6)  ;  i = ks.tlog(i)
        ks = KeySig('C#',  7)  ;  i = ks.tlog(i)
        return i

    @classmethod
    def test_4(cls, i):
        ks = KeySig('C#',  7)  ;  i = ks.tlog(i)
        ks = KeySig('F#',  6)  ;  i = ks.tlog(i)
        ks = KeySig('B' ,  5)  ;  i = ks.tlog(i)
        ks = KeySig('E' ,  4)  ;  i = ks.tlog(i)
        ks = KeySig('A' ,  3)  ;  i = ks.tlog(i)
        ks = KeySig('D' ,  2)  ;  i = ks.tlog(i)
        ks = KeySig('G' ,  1)  ;  i = ks.tlog(i)
        ks = KeySig('C' ,  0)  ;  i = ks.tlog(i)
        ks = KeySig('F',  -1)  ;  i = ks.tlog(i)
        ks = KeySig('Bb', -2)  ;  i = ks.tlog(i)
        ks = KeySig('Eb', -3)  ;  i = ks.tlog(i)
        ks = KeySig('Ab', -4)  ;  i = ks.tlog(i)
        ks = KeySig('Db', -5)  ;  i = ks.tlog(i)
        ks = KeySig('Gb', -6)  ;  i = ks.tlog(i)
        ks = KeySig('Cb', -7)  ;  i = ks.tlog(i)
        return i
    @staticmethod
    def test_B(i):
        ks = KeySig(l=0)         ;  i = ks.tlog(i)
        ks = KeySig(l=4)         ;  i = ks.tlog(i)
        ks = KeySig(l=-4)        ;  i = ks.tlog(i)
        ks = KeySig(l=8)         ;  i = ks.tlog(i)
        ks = KeySig(l=-8)        ;  i = ks.tlog(i)
        ks = KeySig('', l=0)     ;  i = ks.tlog(i)
        ks = KeySig('', l=4)     ;  i = ks.tlog(i)
        ks = KeySig('', l=-4)    ;  i = ks.tlog(i)
        ks = KeySig('', l=8)     ;  i = ks.tlog(i)
        ks = KeySig('', l=-8)    ;  i = ks.tlog(i)
        ks = KeySig('C', l=0)    ;  i = ks.tlog(i)
        ks = KeySig('E', l=4)    ;  i = ks.tlog(i)
        ks = KeySig('Ab', l=-4)  ;  i = ks.tlog(i)
        ks = KeySig('D', l=8)    ;  i = ks.tlog(i)
        ks = KeySig('Db', l=-8)  ;  i = ks.tlog(i)
        ks = KeySig('')          ;  i = ks.tlog(i)
        ks = KeySig('E',  4)     ;  i = ks.tlog(i)
        ks = KeySig('Ab', -4)    ;  i = ks.tlog(i)
        ks = KeySig('A',  3)     ;  i = ks.tlog(i)
        ks = KeySig('Z')         ;  i = ks.tlog(i)
        ks = KeySig('Z', 3)      ;  i = ks.tlog(i)
        ks = KeySig('', 3)       ;  i = ks.tlog(i)
        ks = KeySig(3)           ;  i = ks.tlog(i)
        ks = KeySig('')          ;  i = ks.tlog(i)
        ks = KeySig('X')         ;  i = ks.tlog(i)
        ks = KeySig()            ;  i = ks.tlog(i)
        ks = KeySig('D#')        ;  i = ks.tlog(i)
        ks = KeySig('G#')        ;  i = ks.tlog(i)
        return i
    @classmethod
    def test_A(cls, i):
        ks = KeySig('A')         ;  i = ks.tlog(i)
        ks = KeySig('A', None)   ;  i = ks.tlog(i)
        ks = KeySig(None, 3)     ;  i = ks.tlog(i)
        ks = KeySig(l=3)         ;  i = ks.tlog(i)
        ks = KeySig('A', 3)      ;  i = ks.tlog(i)
        ks = KeySig(None, None)  ;  i = ks.tlog(i)
        ks = KeySig('Eb')        ;  i = ks.tlog(i)
        ks = KeySig('Eb', None)  ;  i = ks.tlog(i)
        ks = KeySig(l=-3)        ;  i = ks.tlog(i)
        ks = KeySig('Eb', -3)    ;  i = ks.tlog(i)
        ks = KeySig(k='A')       ;  i = ks.tlog(i)
        ks = KeySig(k='A', l=None)   ;  i = ks.tlog(i)
        ks = KeySig(None, l=-3)      ;  i = ks.tlog(i)
        ks = KeySig(None, l=None)    ;  i = ks.tlog(i)
        ks = KeySig(k=None, l=None)  ;  i = ks.tlog(i)
        return i
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
