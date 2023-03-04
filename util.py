"""util.py module.  class list: [DSymb, Notes, Strings, Test]."""
import sys, os, inspect, pathlib
from collections import OrderedDict as cOd

B                = ' '
M                = -7
P                = 7
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
STFILT = ['log', 'tlog', 'fmtl', 'fmtm', 'm12', 'dumpGeom', 'resetJ', 'dumpJs', 'dumpImap', 'dumpSmap', 'dumpCursorArrows', '<listcomp>', 'dumpLimap2', 'dumpTniksPfx', 'dumpTniksSfx', 'fmtXYWH', 'kbkInfo', 'dumpCrs', 'fCrsCrt'] # , 'dumpView', 'dumpLbox', 'dumpRect']
########################################################################################################################################################################################################
def m12(s):         return M12[s] if s in M12 else s
def t2sign(t=None): return ' ' if t is None or t==2 else '+' if t==1 else ''
def js2sign(l):     return [ '-' if k<0  else '+' if k>0 else ' ' for k in l ]

def init(file, oid):
    global LOG_FILE  ;  LOG_FILE = file  ;  global OIDS  ;  OIDS = oid
    slog('BGN')
    slog(f'{B*15}{len(Notes.F2S):3}    F2S', pfx=0)   ;   slog(f'{fmtm(Notes.F2S, w=2, d="")}',  pfx=0)
    slog(f'{B*15}{len(Notes.S2F):3}    S2F', pfx=0)   ;   slog(f'{fmtm(Notes.S2F, w=2, d="")}',  pfx=0)
    slog(f'{B*15}{len(Notes.I2F):3}    I2F', pfx=0)   ;   slog(f'{fmtm(Notes.I2F, w=2, d="")}',  pfx=0)
    slog(f'{B*15}{len(Notes.I2S):3}    I2S', pfx=0)   ;   slog(f'{fmtm(Notes.I2S, w=2, d="")}',  pfx=0)
    slog(f'{B*15}{len(Notes.N2I):3}    N2I', pfx=0)   ;   slog(f'{fmtm(Notes.N2I, w=2, d="")}',  pfx=0)
    slog(f'{B*15}{len(FLATS):3}    FLATS',  pfx=0)
    slog(f'{fmtl(FLATS, w=3, u=">", d="")}',    pfx=0)
    slog(f'{fmtl( [ f"{i + 1:3}" for i in range(Notes.MAX_IDX) ], d="")}', pfx=0)
    slog(f'{fmtl(SHRPS, w=3, u=">", d="")}',    pfx=0)
    slog(f'{B*15}{len(SHRPS):3}    SHRPS',  pfx=0)
    dumpND()
    dumpKS()
    slog('END')

def dumpND():
    slog(f'I  F  S  IV   Notes Table {len(ND)}', pfx=0)
    for i in range(len(ND)):   slog(f'{m12(i)} {fmtl(ND[i], w=2)}', pfx=0)
########################################################################################################################################################################################################
def dumpKS():
    ksd = KSD   ;   t = Notes.NONE   ;   dmpKSDhdr(t)
    items = sorted(ksd.items())
    for k, v in items:
        a, b, c = [], [], []  ;  a2, b2 = [], []
        for i in range(len(v)):
            w = v[i]
            if   i==0: a.append(w[0])  ;  a.append(w[1])  ;  a2.append(f'{w[0]:2} ')  ;  a2.append(f'{m12(w[1])}')  ;  a2 =  ''.join(a2)
            elif i==1: b.append(w[:abs(k)])               ;  b2.append(f'{fmtl(w[:abs(k)], w=2)}')                  ;  b2 = ' '.join(b2)
            else:      c = w
            t = Notes.FLAT if k < 0 else Notes.SHRP if k > 0 else Notes.NONE
        sign = t2sign(t)   ;   nt = Notes.TYPES[t]
        slog(fmtks(sign, k, nt, a[0], a[1], b, c), pfx=0)

def dmpKSDhdr(t):
    l = 2*P+1 if t is Notes.NONE else M if t==Notes.FLAT else P if t==Notes.SHRP else 1  ;   sign = t2sign(t)
    slog(f'KS Type  N  I       Flats/Sharps {B*6} F/S Indices     Key Sig Table {sign}{l}', pfx=0)

def dumpKSD(ksd, w=2, u='<'):
    keys = sorted(ksd.keys())    ;   d = ''    ;   v = B*24 if Notes.TYPE==Notes.FLAT else ''
    _ = js2sign(keys)   ;   _ = '  '.join(_)   ;   slog(f'{v}{_}')   ;   slog(f'{v}{fmtl(list(map(abs, keys)), w=w, u=u, d=d)}')
    _ = [ f'{    ksd[k][0][0]}'     for k in keys ]                  ;   slog(f'{v}{fmtl(_, w=w, d=d)}')
    _ = [ f'{m12(ksd[k][0][1]):<2}' for k in keys ]                  ;   slog(f'{v}{fmtl(_, w=w, d=d)}')
    f = [ f'{m12(ksd[M][2][f]):<2}' for f in range(len(ksd[M][2])-1, -1, -1) ]
    s = [ f'{m12(ksd[P][2][s]):<2}' for s in range(len(ksd[P][2])) ]         ;  slog(f'{v}{fmtl(f, w=w, d=d)} {B*2} {fmtl(s, w=w, d=d)}')
    f = [ f for f in reversed(ksd[M][1]) ]  ;  s = [ s for s in ksd[P][1] ]  ;  slog(f'{v}{fmtl(f, w=w, d=d)} {B*2} {fmtl(s, w=w, d=d)}')
########################################################################################################################################################################################################
def dumpNic(nic, w=2, dbg=0):
    mc = nic.most_common()   ;   nt = nic.total()
    _ = list(list(zip(*mc)))[0] if mc else []   ;   u = '<'
    if _:
        slog(f'             dict(nic) {fmtl([m12(_) for _ in dict(nic)],               w=w, u=u)}')   if dbg else None
        slog(f'     sorted(dict(nic)) {fmtl([m12(_) for _ in sorted(dict(nic))],       w=w, u=u)}')
        slog(f'           zip(*mc)[0] {fmtl([m12(_) for _ in list(list(zip(*mc)))[0]], w=w, u=u)}')
        slog(f'           zip(*mc)[1] {fmtl(                 list(list(zip(*mc))[1]),  w=w, u=u)}')
        slog(f'      mc[n][1]/nt*100% {fmtl([(100 * n[1]) // nt for n in mc],          w=w)}')
        slog(f'                I2F[n] {fmtl([Notes.I2F[n]       for n in  _ ],         w=w)}')
        slog(f'                I2S[n] {fmtl([Notes.I2S[n]       for n in  _ ],         w=w)}')
########################################################################################################################################################################################################
def calcKS(nic, dbg=0):
    ksd = KSD
    dumpKSD(ksd)
    dumpNic(nic)
    js  = []   ;   t = Notes.TYPE   ;   nt = Notes.TYPES[t]
    ks  = ksd[M][2] if t == Notes.FLAT else ksd[P][2]
    for j in ks:
        if j in nic: js.append(m12(j))
        else:        break
    l   = -len(js) if t==Notes.FLAT else len(js)
    s   = t2sign(t) if js else '?'
    nn  = ksd[l][0][0] if js else '??'
    ni  = ksd[l][0][1]
    ns  = ksd[l][1]
    slog(fmtks( s, l, nt, nn, ni, ns, js)) if dbg else None
    return      s, l, nt, nn, ni, ns, js
########################################################################################################################################################################################################
def fmtks(s, l, nt, nn, ni, ns, js):
    ns = f'[{fmtl(ns, w=2, d="")}]'  ;  js = [ m12(j) for j in js ]  ;  return f'{s}{l} {nt} [{nn:2} {m12(ni)}] {ns:22} [{fmtl(js, d="")}]'

def fmtl(lst, w=None, u=None, d='[', d2=']', sep=' ', ll=None, z=''):
    if lst is None: return 'None'
    lts = (list, tuple, set, frozenset)  ;  dtn = (int, float)  ;  dts = (str,)
    assert type(lst) in lts, f'{type(lst)=} {lts=}'
    if d=='':   d2 = ''
    w = w if w else ''   ;   t = ''
    sl = '-' if ll is not None and ll<0 else '+' if ll is not None and ll>=0 else ''
    s = f'{sl}{len(lst)}' if ll is not None else ''
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
#            else:                             msg = f'ERROR l={l} is type {type(l)}'   ;   slog(msg)   ;   raise SystemExit(msg)
    return s + d + t + d2

def fmtm(m, w=1, d0=':', d='[', d2=']', ll=None):
    if d=='':   d2 = ''
    t = ''   ;   u = '>'
    for k, v in m.items():
        if   type(v) in (list, tuple, set):         t += f'{d}{k:{u}{w}}{d0}{fmtl(v, w, ll=k if ll==-1 else ll)}{d2} '
        elif type(v) in (int, str):                 t += f'{d}{k:{u}{w}}{d0}{v:{u}{w}}{d2} '
    return d + t.rstrip() + d2

def ev(obj):          return f'{eval(f"{obj!r}")}'
def fColor(c, d=1): (d, d2) = ("[", "]") if d else ("", "")  ;  return f'{fmtl(c, w=3, d=d, d2=d2):17}'

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
    msg = filtText( msg)
#    msg = filtText2(msg)
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
    print(f'{msg}', flush=flush, sep=sep, end=end, file=file)
    print(f'{msg}', flush=flush, sep=sep, end=end, file=None) if so else None

def filtText(text):
    text = text.replace('"', '')
    text = text.replace("'", '')
    text = text.replace('self', '')
    text = text.replace('util', '')
    text = text.replace('fmtl', '')
    text = text.replace('fmtm', '')
    text = text.replace('m12', '')
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

class Notes(object):
    FLAT, SHRP, NONE = 0, 1, 2
    TYPE       = FLAT
    TYPES      = ['FLAT', 'SHRP', 'NONE']
    S2F        = {            'C#':'Db', 'D#':'Eb',                       'F#':'Gb', 'G#':'Ab', 'A#':'Bb'           }
    F2S        = {            'Db':'C#', 'Eb':'D#',                       'Gb':'F#', 'Ab':'G#', 'Bb':'A#'           }
    S2F2       = { 'B#':'C' ,                       'E' :'Fb', 'E#':'F' ,                                  'B':'Cb' }
    F2S2       = { 'C' :'B#',                       'Fb':'E' , 'F' :'E#',                                  'Cb':'B' }
    I2F        = {         0:'C' , 1:'Db', 2:'D' , 3:'Eb', 4:'E' ,                5:'F' , 6:'Gb', 7:'G' , 8:'Ab', 9:'A' , 10:'Bb', 11:'B'  }
    I2S        = {         0:'C' , 1:'C#', 2:'D' , 3:'D#', 4:'E' ,                5:'F' , 6:'F#', 7:'G' , 8:'G#', 9:'A' , 10:'A#', 11:'B'  }
    I2F2       = {         0:'C' , 1:'Db', 2:'D' , 3:'Eb',         4:'Fb',        5:'F' , 6:'Gb', 7:'G' , 8:'Ab', 9:'A' , 10:'Bb',        11:'Cb' }
    I2S2       = { 0:'B#',         1:'C#', 2:'D' , 3:'D#', 4:'E' ,         5:'E#',         6:'F#', 7:'G' , 8:'G#', 9:'A' , 10:'A#', 11:'B'  }
    I2V        = { 0: 'R', 1: 'b2', 2: '2', 3: 'm3', 4: 'M3', 5: '4', 6: 'b5', 7: '5', 8: '#5', 9: '6', 10: 'b7', 11: '7' }
    N2I        = { 'B#':0, 'C' :0, 'C#':1, 'Db':1, 'D' :2, 'D#':3, 'Eb':3, 'E' :4, 'Fb':4, 'E#':5, 'F' :5, 'F#':6, 'Gb':6, 'G' :7, 'G#':8, 'Ab':8, 'A' :9, 'A#':10, 'Bb':10, 'B' :11, 'Cb' :11 }
    MAX_IDX    = 10 * NTONES + 1
    I2N        = [I2F,  I2S]
    I2N2       = [I2F2, I2S2]

    @staticmethod
    def setType(t): Notes.TYPE = t

    @staticmethod
    def index(n, o=0):
        name = n[:len(n)-1] if o else n
        i = Notes.N2I[name]
        return i

    @staticmethod
    def nextIndex(i, d):
        return (i + d) % NTONES

    @staticmethod
    def name(i, t=None, n2=0):
        t = t if t is not None else Notes.TYPE
        name = Notes.I2N2[t][i % NTONES] if n2 else Notes.I2N[t][i % NTONES]
        return name

    @staticmethod
    def nextName(n, iv, o=0):
        i = Notes.index(n, o)
        j = IVALR[iv]
        k = Notes.nextIndex(i, j)
        m = Notes.name(k)
        return m
########################################################################################################################################################################################################
FLATS   = [ f'{k}{n}' for n in range(11) for k in Notes.N2I.keys() if len(k) == 1 or len(k) > 1 and k[1] != '#' ][:Notes.MAX_IDX]
SHRPS   = [ f'{k}{n}' for n in range(11) for k in Notes.N2I.keys() if len(k) == 1 or len(k) > 1 and k[1] != 'b' ][:Notes.MAX_IDX]

def FREQ( index): return 440 * pow(pow(2, 1/NTONES), index - 57)
def FREQ2(index): return 432 * pow(pow(2, 1/NTONES), index - 57)

FREQS   = [ FREQ( i) for i in range(Notes.MAX_IDX) ]
FREQS2  = [ FREQ2(i) for i in range(Notes.MAX_IDX) ]

def initND():
    return { i:[ Notes.I2F[i], Notes.I2S[i], Notes.I2V[i] ] for i in range(NTONES) }
ND    = initND()

########################################################################################################################################################################################################

#class KeySig(object):
#    KSD = {}
#    KSD = initKSD(KSD, t=0)
#    KSD = initKSD(KSD)
#    KSD = initKSD(KSD, t=1)

def initKSD(m, t=None):
    ln = []  ;  li = []  ;  ln2 = []  ;  li2 = []
    if   t is None: i1 = 0  ;  i2 = 0   ;  d = 0  ;  j1 =  1  ;  j2 =  0
    elif t:         i1 = 7  ;  i2 = 6   ;  d = 7  ;  j1 =  1  ;  j2 =  7
    else:           i1 = 5  ;  i2 = 10  ;  d = 5  ;  j1 = -1  ;  j2 = -7
    dmpKSDhdr(t)
    for k in range(0 if t is None else 1 if t else -1, j1+j2, j1):
        n1 = Notes.name(i1, t=t, n2=1)
        n2 = Notes.name(i2, t=t, n2=1) if t is not None else None
        lni = [n1, i1]
        if abs(k) >= 1:   ln.append(n2)  ;  li.append(i2)  ;  ln2 = list(ln)  ;  li2 = list(li)
        m[k] = [ lni, ln2, li2 ]
        _ = [ f'{m12(i)}' for i in li ]
        sign = t2sign(t)   ;   t = 2 if t is None else t
        nt = Notes.TYPES[t]
        slog(fmtks(sign, k, nt, n1, i1, ln, _), pfx=0)
        i1 = Notes.nextIndex(i1, d)
        i2 = Notes.nextIndex(i2, d) if t is not None else None
    return m
########################################################################################################################################################################################################
KSD = {}
KSD = initKSD(KSD, t=0)
KSD = initKSD(KSD)
KSD = initKSD(KSD, t=1)

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

    def tab2nn(self, tab, s, nic=None, dbg=0):
        fn   = self.tab2fn(tab)
        i    = self.fn2ni(fn, s)
        j    = i % NTONES
        if nic is not None:  nic[j] += 1  ;  nics = f'nic[{m12(j)}]={nic[j]}'
        else:                                nics = ''
        name = Notes.name(i)
        if dbg: slog(f'tab={tab} s={s} fn={fn} i={i:2} name={name:2} {nics}')
        return name # if dbg or nics

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
