"""util.py module.  class list: []."""
import sys, inspect, pathlib
from collections import OrderedDict as cOd

IND = 0
MIN_IVAL_LEN    = 1
MAX_STACK_DEPTH = 0
MAX_STACK_FRAME = inspect.stack()
FMTN            = (1, 2, 2, 2, 3, 1)    # p, l, s, c, t remove?
FMTN2           = (1, 1, 2, 2, 2, 2, 2) # generalize for any # of strings
M12             = { 10:'a', 11:'b' }
INTERVALS       = { 0:'R', 1:'b2', 2:'2', 3:'m3', 4:'M3', 5:'4', 6:'b5', 7:'5', 8:'#5', 9:'6', 10:'b7', 11:'7' }
INTERVAL_RANK   = { 'R':0, 'b2':1, '2':2, 'm3':3, 'M3':4, '4':5, 'b5':6, '5':7, '#5':8, '6':9, 'b7':10, '7':11 }
NTONES          = len(INTERVALS)
STFILT = ['log', 'dumpGeom', 'resetJ', 'dumpJs', 'dumpImap', 'dumpSmap', 'dumpCursorArrows', '<listcomp>', 'dumpLimap2', 'dumpTniksPfx', 'dumpTniksSfx']
########################################################################################################################################################################################################
def getFilePath(baseName, basePath, filedir='files', filesfx='.txt', dbg=0):
    if dbg: slog(f'baseName= {baseName} basePath={basePath}')
    fileName        = baseName + filesfx
    filePath        = basePath / filedir / fileName
    if dbg: slog(f'fileName  = {fileName} filePath={filePath}')
    return filePath
########################################################################################################################################################################################################
def fmtl(lst, w=None, u='>', d1='[', d2=']', sep=' ', ll=0, z=''):
    assert type(lst) in (list, tuple, set, frozenset)
    if d1 == '': d2 = ''
    w = w if w else ''
    t = ''   ;   s = f'<{len(lst)}' if ll else ''
    for i, l in enumerate(lst):
        if type(l) in (list, tuple, set):
#            d0 = sep + d1 if not i else d1    ;    d3 = d2 + sep
            if type(w) in (list, tuple, set):       t += fmtl(l, w[i], u, d1, d2, sep, ll, z)
            else:                                   t += fmtl(l, w,    u, d1, d2, sep, ll, z)
        else:
            ss = sep if i < len(lst)-1 else ''
            if   type(l) is type:                   l = str(l)
            elif l is None:                         l = 'None'
            if   type(w) in (list, tuple, set):     t += f'{l:{u}{w[i]}{z}}{ss}'
            elif type(l) is int:                    t += f'{l:{u}{w   }{z}}{ss}'
            elif type(l) is float:                  t += f'{l:{u}{w   }{z}}{ss}'
            elif type(l) is str:                    t += f'{l:{u}{w   }{z}}{ss}'
            else:                                   msg = f'ERROR l={l} is type {type(l)}'   ;   slog(msg)   ;   raise SystemExit(msg)
    return s + d1 + t + d2

def fmtm(m, w=1, d0=':', d1='[', d2=']'):
    t = ''
    for k, v in m.items():
        if   type(v) in (list, tuple, set):         t += f'{k}{d0}'   ;   t += fmtl(v, w)
        elif type(v) in (int, str):                 t += f'{k:>{w}}{d0}{v:<{w}} '
    return d1 + t.rstrip() + d2
########################################################################################################################################################################################################
def stackDepth(sfs):
    global MAX_STACK_DEPTH, MAX_STACK_FRAME
    for i, sf in enumerate(sfs):
        j = len(sfs) - (i + 1)
        if j > MAX_STACK_DEPTH: MAX_STACK_DEPTH = j;  MAX_STACK_FRAME = sfs
    return len(sfs)

def fmtSD(sd): return f'{sd:{sd}}'

def dumpStack(sfs, file=None):
    for i, sf in enumerate(sfs):
        fp = pathlib.Path(sf.filename)  ;   n = fp.stem  ;  l = sf.lineno  ;  f = sf.function  ;  c = sf.code_context[0].strip() if sf.code_context else ''  ;  j = len(sfs) - (i + 1)
        slog(f'{j:2} {n:9} {l:5} {f:20} {c}', file=file)
    slog(f'MAX_STACK_DEPTH={MAX_STACK_DEPTH:2}', file=file)
########################################################################################################################################################################################################
def slog(msg='', pfx=1, file=None, flush=False, sep=',', end='\n'):
#    if file is None: file = LOG_FILE
    strip = 1
    if pfx:
        sfs = inspect.stack()          ;  i = 1
        while sfs[i].function in STFILT:  i += 1
        sf = sfs[i]   ;   sd = stackDepth(sfs)
        p = pathlib.Path(sf.filename)  ;  n = p.name  ;  l = sf.lineno  ;  f = sf.function
        if IND: print(f'{fmtSD(sd):20} {l:5} {n:7} {f:>20} ',      file=file, end='')
        else:   print(             f'{sd:2} {l:5} {n:7} {f:>20} ', file=file, end='')
    if strip:
        msg = msg.replace('self.', '.')
        msg = msg.replace('"', '')
        msg = msg.replace("'", '')
    print(f'{msg}', file=file, flush=flush, sep=sep, end=end)
#        print(f'{msg}', file=file, flush=flush, sep=sep, end=end) if pfx else print(f'{msg}', file=file, flush=flush, sep=sep, end=end)
#        if file != LOG_FILE: Tabs.slog(msg, pfx, flush=False, sep=',', end=end)
########################################################################################################################################################################################################
def parseCmdLine(file=None):
    dbg = 1
    options = dict()
    key = ''
    vals = []
    largs = len(sys.argv)
    if dbg: slog(f'argv={fmtl(sys.argv)}', file=file)
    for j in range(1, largs):
        argv = sys.argv[j]
        if len(argv) > 2 and argv[0] == '-' and argv[1] == '-':
            if argv[2].isalpha():
                vals = []
                key = argv[2:]
                options[key] = vals
                if dbg: slog(f'{j:2} long    {argv:2} {key} {fmtl(vals)}', end=' ', file=file)
            else:
                slog(f'{j:2} ERROR long    {argv:2} {key} {fmtl(vals)}', end=' ', file=file)
        elif len(argv) > 1 and argv[0] == '-':
            if argv[1].isalpha() or argv[1] == '?':
                vals = []
                if len(argv) == 2:
                    key = argv[1:]
                    if dbg: slog(f'{j:2} short   {argv:2} {key} {fmtl(vals)}', end=' ', file=file)
                    options[key] = vals
                elif len(argv) > 2:
                    for i in range(1, len(argv)):
                        key = argv[i]
                        if dbg: slog(f'{j:2} short   {argv:2} {key} {fmtl(vals)}', end=' ', file=file)
                        options[key] = vals
            elif argv[1].isdigit():
                vals.append(argv)
                options[key] = vals
                if dbg: slog(f'{j:2} neg arg {argv:2} {key} {fmtl(vals)}', end=' ', file=file)
            else:
                vals.append(argv)
                options[key] = vals
                if dbg: slog(f'{j:2} ??? arg {argv:2} {key} {fmtl(vals)}', end=' ', file=file)
        else:
            vals.append(argv)
            options[key] = vals
            if dbg: slog(f'{j:2} arg     {argv:2} {key} {fmtl(vals)}', end=' ', file=file)
        if dbg: slog(pfx=0, file=file)
    if dbg: slog(f'options={fmtm(options)}', file=file)
    return options
########################################################################################################################################################################################################
class DSymb(object):
    SYMBS = {'X': 'mute', '/': 'slide', '\\': 'bend', '+': 'hammer', '~': 'vibrato', '^': 'tie', '.': 'staccato', '_': 'legato', '%': 'repeat', '|': 'bar', '[': 'groupL', ']': 'groupR'}
########################################################################################################################################################################################################
class Note(object):
    FLAT, SHARP = 0, 1
    TYPE        = FLAT
    TYPES       = ['FLAT', 'SHARP']
    F2S         = {'Db':'C#', 'Eb':'D#', 'Gb':'F#', 'Ab':'G#', 'Bb':'A#'}
    S2F         = {'C#':'Db', 'D#':'Eb', 'F#':'Gb', 'G#':'Ab', 'A#':'Bb'}
    FLATS       = { 0:'C', 1:'Db', 2:'D', 3:'Eb', 4:'E', 5:'F', 6:'Gb', 7:'G', 8:'Ab', 9:'A', 10:'Bb', 11:'B' }
    SHARPS      = { 0:'C', 1:'C#', 2:'D', 3:'D#', 4:'E', 5:'F', 6:'F#', 7:'G', 8:'G#', 9:'A', 10:'A#', 11:'B' }
    TONES       = [FLATS, SHARPS]
    INDICES = { 'C0': 0, 'C#0': 1, 'Db0': 1, 'D0': 2, 'D#0': 3, 'Eb0': 3, 'E0': 4, 'F0': 5, 'F#0': 6, 'Gb0': 6, 'G0': 7, 'G#0': 8, 'Ab0': 8, 'A0': 9, 'A#0':10, 'Bb0':10, 'B0':11,
                'C1':12, 'C#1':13, 'Db1':13, 'D1':14, 'D#1':15, 'Eb1':15, 'E1':16, 'F1':17, 'F#1':18, 'Gb1':18, 'G1':19, 'G#1':20, 'Ab1':20, 'A1':21, 'A#1':22, 'Bb1':22, 'B1':23,
                'C2':24, 'C#2':25, 'Db2':25, 'D2':26, 'D#2':27, 'Eb2':27, 'E2':28, 'F2':29, 'F#2':30, 'Gb2':30, 'G2':31, 'G#2':32, 'Ab2':32, 'A2':33, 'A#2':34, 'Bb2':34, 'B2':35,
                'C3':36, 'C#3':37, 'Db3':37, 'D3':38, 'D#3':39, 'Eb3':39, 'E3':40, 'F3':41, 'F#3':42, 'Gb3':42, 'G3':43, 'G#3':44, 'Ab3':44, 'A3':45, 'A#3':46, 'Bb3':46, 'B3':47,
                'C4':48, 'C#4':49, 'Db4':49, 'D4':50, 'D#4':51, 'Eb4':51, 'E4':52, 'F4':53, 'F#4':54, 'Gb4':54, 'G4':55, 'G#4':56, 'Ab4':56, 'A4':57, 'A#4':58, 'Bb4':58, 'B4':59,
                'C5':60, 'C#5':61, 'Db5':61, 'D5':62, 'D#5':63, 'Eb5':63, 'E5':64, 'F5':65, 'F#5':66, 'Gb5':66, 'G5':67, 'G#5':68, 'Ab5':68, 'A5':69, 'A#5':70, 'Bb5':70, 'B5':71,
                'C6':72, 'C#6':73, 'Db6':73, 'D6':74, 'D#6':75, 'Eb6':75, 'E6':76, 'F6':77, 'F#6':78, 'Gb6':78, 'G6':79, 'G#6':80, 'Ab6':80, 'A6':81, 'A#6':82, 'Bb6':82, 'B6':83,
                'C7':84, 'C#7':85, 'Db7':85, 'D7':86, 'D#7':87, 'Eb7':87, 'E7':88, 'F7':89, 'F#7':90, 'Gb7':90, 'G7':91, 'G#7':92, 'Ab7':92, 'A7':93, 'A#7':94, 'Bb7':94, 'B7':95,
                'C8':96 } # For simplicity omit double flats and double sharps and other redundant enharmonic note names e.g. Abb, C##, Cb, B#, Fb, E# etc...
    NAMES   = [ k for k in INDICES.keys() if k[1] != 'b' ]

    @staticmethod
    def setType(t): Note.TYPE = t

    @staticmethod
    def getName(i):
        name = Note.TONES[Note.TYPE][i % NTONES]
        return name

    @staticmethod
    def getFreq(index): return 440 * pow(pow(2, 1/NTONES), index - Note.INDICES)
########################################################################################################################################################################################################
class Strings(object):
    aliases = {'GUITAR_6_STD':    cOd([('E2', 28), ('A2', 33), ('D3', 38), ('G3', 43), ('B3', 47), ('E4', 52)]),
               'GUITAR_6_DROP_D': cOd([('D2', 26), ('A2', 33), ('D3', 38), ('G3', 43), ('B3', 47), ('E4', 52)]),
               'GUITAR_7_STD':    cOd([('E2', 28), ('Ab2', 32), ('C3', 36), ('E3', 40), ('Ab3', 44), ('C4', 48), ('E4', 52)])
              }
    def __init__(self, file=None, alias=None):
        if alias is None: alias = 'GUITAR_6_STD'
        self.stringMap = self.aliases[alias]
        self.stringKeys = list(self.stringMap.keys())
        self.stringNames = ''.join(reversed([ str(k[0])  for k in            self.stringKeys ]))
        self.stringNumbs = ''.join(         [ str(r + 1) for r in range(len(self.stringKeys)) ])
        self.stringCapo = ''.join(          [ '0'        for _ in range(len(self.stringKeys)) ])
        self.strLabel = 'STRING'
        self.cpoLabel = ' CAPO '
        slog(f'stringMap   = {fmtm(self.stringMap)}',  file=file)
        slog(f'stringKeys  = {fmtl(self.stringKeys)}', file=file)
        slog(f'stringNames =      {self.stringNames}', file=file)
        slog(f'stringNumbs =      {self.stringNumbs}', file=file)
        slog(f'stringCapo  =      {self.stringCapo}',  file=file)
        slog(f'strLabel    =      {self.strLabel}',    file=file)
        slog(f'cpoLabel    =      {self.cpoLabel}',    file=file)

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
