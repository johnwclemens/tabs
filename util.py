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
#def t2sign(t=None): return ' ' if t is None or t==2 else '+' if t==1 else ''
def t2sign(t=0):    return ' ' if not t else '+' if t==1 else ''
def js2sign(l):     return [ '-' if k<0  else '+' if k>0 else ' ' for k in l ]

def init(file, oid):
    global LOG_FILE  ;  LOG_FILE = file  ;  global OIDS  ;  OIDS = oid
    dumpData()

def dumpData():
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
    t    = Notes.NONE   ;   dmpKSDhdr(t)
    keys = sorted(KSD.keys())
    for k in keys:      slog(fmtks(k), pfx=0)

def dmpKSDhdr(t):
    k = 2*P+1 if t == Notes.NONE else M if t == Notes.FLAT else P if t == Notes.SHRP else 1  ;   sign = t2sign(t)
    slog(f'KS Type  N  I   Flats/Sharps Naturals  F/S/N Indices  Ionian Indices   Ionian Note Ordering   Key Sig Table {sign}{k}', pfx=0)

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
def nic2KS(nic, dbg=0):
    dumpKSD(KSD)     ;     dumpNic(nic)
    iz  = []   ;   t = Notes.TYPE   ;   nt = Notes.TYPES[t]
    ks  = KSD[M][KIS]    if t == Notes.FLAT else KSD[P][KIS]
    for i in ks:
        if i in nic:     iz.append(m12(i))
        else:            break
    k   = -len(iz)       if t == Notes.FLAT else len(iz)
    s   = t2sign(t)      if iz else '?'
    n   = KSD[k][KIM][1] if iz else '??'
    i   = KSD[k][KIM][0]
    ns  = KSD[k][KMS]
    slog(fmtks(k))       if dbg else None
    return  s, k, nt, n, i, ns, js(i)
########################################################################################################################################################################################################
def fmtks(k):
#    t   = 1 if k > 0 else 0 if k < 0 else 2    ;   nt = Notes.TYPES[t]
    t   = -1 if k < 0 else 1 if k > 0 else 0    ;   nt = Notes.TYPES[t]
    s   = t2sign(t)     ;   im = KSD[k][KIM]   ;    i = im[0]      ;    m = im[1]
    iz  = KSD[k][KIS]   ;   jz = KSD[k][KJS]   ;   ms = KSD[k][KMS]
    ns  = [ Notes.name(j, t, 1 if abs(k) >= 5 else 0) for j in jz ]
    iz  = [ m12(i) for i in iz ]
    jz  = [ m12(j) for j in jz ]
    return f'{s}{k} {nt} [{m:2} {m12(i)}] {fmtl(ms, w=2)} {fmtl(iz)} {fmtl(jz)} {fmtl(ns, w=2)}'

def fmtl(lst, w=None, u=None, d='[', d2=']', sep=' ', ll=None, z=''):
    if lst is None: return 'None'
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
#            else:                             msg = f'ERROR l={l} is type {type(l)}'   ;   slog(msg)   ;   raise SystemExit(msg)
    return s + d + t + d2

def fmtm(m, w=1, d0=':', d='[', d2=']', ll=None):
    if d=='':   d2 = ''
    t = ''   ;   u = '>'
    for k, v in m.items():
        if   type(v) in (list, tuple, set):  t += f'{d}{k:{u}{w}}{d0}{fmtl(v, w, ll=k if ll==-1 else ll)}{d2} '
        elif type(v) in (int, str):          t += f'{d}{k:{u}{w}}{d0}{v:{u}{w}}{d2} '
    return d + t.rstrip() + d2

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
def slog(msg='', pfx=1, file=1, flush=False, sep=',', end='\n'):
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
    key     = ''
    vals    = []
    largs   = len(sys.argv)
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
#    FLAT, SHRP, NONE = 0, 1, 2
    FLAT, NONE, SHRP = -1, 0,      1   # -1 ~= 2
    TYPES            = [ 'NONE', 'SHRP', 'FLAT' ] # 0=NONE, 1=SHRP, 2=FLAT=-1
#    TYPES      = ['FLAT', 'SHRP', 'NONE']
    TYPE       = FLAT
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
    I2N        = [I2F,  I2S,  I2F]
    I2N2       = [I2F2, I2S2, I2F2]

    @staticmethod
    def setType(t): Notes.TYPE = t

    @staticmethod
    def index(n, o=0):
        name = n[:len(n)-1] if o else n
        i    = Notes.N2I[name]
        return i

    @staticmethod
    def nextIndex(i, d):
        return  (i + d) % NTONES

    @staticmethod
    def OLD__name(i, t=None, n2=0):
        t    = 0 if t == 2 else t if t is not None else Notes.TYPE
        name = Notes.I2N2[t][i % NTONES]   if n2   else Notes.I2N[t][i % NTONES]
        return name

    @staticmethod
    def name(i, t=0, n2=0):
        t    = t if t else Notes.TYPE
        name = Notes.I2N2[t][i % NTONES]   if n2   else Notes.I2N[t][i % NTONES]
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
ND = initND()
########################################################################################################################################################################################################
def OLD__initKSD(ks, t=None):
    NT = NTONES
    if   not t: # is None:
        i = 0   ;   i2 = 10  ;    d = 5   ;   j1 =  1  ;   j2 =  0  ;  li0 = [ (i2+1+j*d) % NT for j in range(0,    7,   j1) ]  ;  ln0 = [ Notes.name(j, t) for j in li0 ]
    elif t:
        i = 7   ;   i2 = 6   ;    d = 7   ;   j1 =  1  ;   j2 =  7  ;  li0 = [ (10+j*d)   % NT for j in range(1,  j1+j2, j1) ]  ;  ln0 = [ Notes.name(j, t) for j in li0 ]
    else:
        i = 5   ;   i2 = 10  ;    d = 5   ;   j1 = -1  ;   j2 = -7  ;  li0 = [ (i+1+j*d) % NT for j in range(1, -j1-j2, 1)  ]  ;  ln0 = [ Notes.name(j, t) for j in li0 ]
    li  = list(li0)   ;   ln = list(ln0)
    for k in range(0 if t is None else 1 if t else -1, j1+j2, j1):
        m  = Notes.name(i, t, 1)
        n  = Notes.name(i2, t, 1)
        im = [i, m]      ;    ak = abs(k)
        if ak >= 1:   ln[ak-1] = n  ;  li[ak-1] = i2   ;  ms = list(ln)  ;  iz = list(li)
        else:                                             ms = list(ln)  ;  iz = list(li)
        jz = js(i)
        ns = [ Notes.name(n, t, 1 if ak >= 5 else 0) for n in jz ]
        ks[k] = [ im, iz, ms, jz, ns ]
        slog(fmtks(k), pfx=0)
        i  = Notes.nextIndex(i, d)
        i2 = Notes.nextIndex(i2, d)
    return ks

def OLD_2_initKSD(ks, t=0):
    NT = NTONES
    if   t < 0:
        i = 5   ;   i2 = 10  ;    d = 5   ;   j1 = -1  ;   j2 = -7  ;  li0 = [ (i+1+j*d) % NT for j in range(1, -j1-j2, 1)  ]  ;  ln0 = [ Notes.name(j, t) for j in li0 ]
    elif t > 0:
        i = 7   ;   i2 = 6   ;    d = 7   ;   j1 =  1  ;   j2 =  7  ;  li0 = [ (10+j*d)   % NT for j in range(1,  j1+j2, j1) ]  ;  ln0 = [ Notes.name(j, t) for j in li0 ]
    else:
        i = 0   ;   i2 = 10  ;    d = 5   ;   j1 =  1  ;   j2 =  0  ;  li0 = [ (i2+1+j*d) % NT for j in range(0,    7,   j1) ]  ;  ln0 = [ Notes.name(j, t) for j in li0 ]
    li  = list(li0)   ;   ln = list(ln0)
    for k in range(0 if not t else t, j1+j2, j1):
        m  = Notes.name(i, t, 1)
        n  = Notes.name(i2, t, 1)
        im = [i, m]      ;    ak = abs(k)
        if ak >= 1:   ln[ak-1] = n  ;  li[ak-1] = i2   ;  ms = list(ln)  ;  iz = list(li)
        else:                                             ms = list(ln)  ;  iz = list(li)
        jz = js(i)
        ns = [ Notes.name(n, t, 1 if ak >= 5 else 0) for n in jz ]
        ks[k] = [ im, iz, ms, jz, ns ]
        slog(fmtks(k), pfx=0)
        i  = Notes.nextIndex(i, d)
        i2 = Notes.nextIndex(i2, d)
    return ks

def OLD_3_initKSD(ks, t=0):
    NT = NTONES
    if   t < 0:
        i = 5   ;   j = 10  ;    d = 5   ;   j1 = -1  ;   j2 = -7  ;  li0 = [ (i+1+k*d) % NT for k in range(1, -j1-j2, 1)  ]  ;  ln0 = [ Notes.name(j, t) for j in li0 ]
    elif t > 0:
        i = 7   ;   j = 6   ;    d = 7   ;   j1 =  1  ;   j2 =  7  ;  li0 = [ (10+k*d)   % NT for k in range(1,  j1+j2, j1) ]  ;  ln0 = [ Notes.name(j, t) for j in li0 ]
    else:
        i = 0   ;   j = 10  ;    d = 5   ;   j1 =  1  ;   j2 =  0  ;  li0 = [ (j+1+k*d) % NT for k in range(0,    7,   j1) ]  ;  ln0 = [ Notes.name(j, t) for j in li0 ]
    li  = list(li0)   ;   ln = list(ln0)
    slog(f'{fmtl(li)=} {fmtl(ln)=}')
    for k in range(0 if not t else t, j1+j2, j1):
        m  = Notes.name(i, t, 1)
        n  = Notes.name(j, t, 1)
        im = [i, m]      ;    ak = abs(k)
        if ak >= 1:   ln[ak-1] = n  ;  li[ak-1] = j   ;  ms = list(ln)  ;  iz = list(li)
        else:                                            ms = list(ln)  ;  iz = list(li)
        jz = js(i)
        ns = [ Notes.name(n, t, 1 if ak >= 5 else 0) for n in jz ]
        ks[k] = [ im, iz, ms, jz, ns ]
        slog(fmtks(k), pfx=0)
        i  = Notes.nextIndex(i, d)
        j  = Notes.nextIndex(j, d)
    return ks

def OLD_4_initKSD(ks, t=0):
    NT = NTONES
    if   t < 0: i = 5   ;   j = 10  ;    d = 5   ;   j1 = -1  ;   j2 = -7  ;  li0 = [ (i+1+k*d) % NT for k in range(1, -j1-j2, 1)  ]
    elif t > 0: i = 7   ;   j = 6   ;    d = 7   ;   j1 =  1  ;   j2 =  7  ;  li0 = [ (10+k*d)   % NT for k in range(1,  j1+j2, j1) ]
    else:       i = 0   ;   j = 10  ;    d = 5   ;   j1 =  1  ;   j2 =  0  ;  li0 = [ (j+1+k*d) % NT for k in range(0,    7,   j1) ]
    ln0 = [Notes.name(j, t) for j in li0]
    li  = list(li0)   ;   ln = list(ln0)
    slog(f'{fmtl(li)=} {fmtl(ln)=}')
    for k in range(0 if not t else t, j1+j2, j1):
        m  = Notes.name(i, t, 1)
        n  = Notes.name(j, t, 1)
        im = [i, m]      ;    ak = abs(k)
        if ak >= 1:   ln[ak-1] = n  ;  li[ak-1] = j   ;  ms = list(ln)  ;  iz = list(li)
        else:                                            ms = list(ln)  ;  iz = list(li)
        jz = js(i)
        ns = [ Notes.name(n, t, 1 if ak >= 5 else 0) for n in jz ]
        ks[k] = [ im, iz, ms, jz, ns ]
        slog(fmtks(k), pfx=0)
        i  = Notes.nextIndex(i, d)
        j  = Notes.nextIndex(j, d)
    return ks

def old_5_initKSD(ks, t):
    NT = NTONES #  ;   a = t   ;   b = P + 1
    if   t == -1:  i = 5  ;  j = 10  ;  d = 5  ;  a = -1  ;  b = -7  ;  c =  1
    elif t ==  1:  i = 7  ;  j = 6   ;  d = 7  ;  a =  1  ;  b =  7  ;  c =  3
    else:          i = 0  ;  j = 10  ;  d = 7  ;  a =  1  ;  b =  0  ;  c =  0
    li0 = [ (i+c+k*d) % NT  for k in range(abs(a), abs(a)+P) ]
    ln0 = [Notes.name(j, t) for j in li0]
    li  = list(li0)      ;      ln = list(ln0)
    slog(f'{t=} {a=} {b=} {c=} {fmtl(li)=} {fmtl(ln)=}')
    for k in range(a, a+b, a):
        m  = Notes.name(i, t, 1)
        n  = Notes.name(j, t, 1)
        im = [i, m]      ;    ak = abs(k)
        if ak >= 1:   ln[ak-1] = n  ;  li[ak-1] = j   ;  ms = list(ln)  ;  iz = list(li)
        else:                                            ms = list(ln)  ;  iz = list(li)
        jz = js(i)
        ns = [ Notes.name(n, t, 1 if ak >= 5 else 0) for n in jz ]
        ks[k] = [ im, iz, ms, jz, ns ]
        slog(fmtks(k), pfx=0)
        i  = Notes.nextIndex(i, d)
        j  = Notes.nextIndex(j, d)
    return ks

def initKSD(ks, t):
    NT = NTONES #  ;   a = t   ;   b = P + 1
    if   t == -1:  i = 5  ;  j = 10  ;  s = 5  ;  a = -1  ;  b = a-7  ;  c = -1  ;  d = 1
    elif t ==  1:  i = 7  ;  j = 6   ;  s = 7  ;  a =  1  ;  b = a+7  ;  c =  1  ;  d = 3
    else:          i = 0  ;  j = 5   ;  s = 5  ;  a =  0  ;  b = a-1  ;  c = -1  ;  d = -1
    li0 = [ (i+d+k*s) % NT  for k in range(abs(a), abs(a)+P) ]
    ln0 = [Notes.name(j, t) for j in li0]
    li  = list(li0)       ;      ln = list(ln0)
    slog(f'{t=} {a=} {b=} {c=} {fmtl(li)=} {fmtl(ln)=}')
    for k in range(a, b, c):
        m  = Notes.name(i, t, 1)
        n  = Notes.name(j, t, 1)
        im = [i, m]       ;      ak = abs(k)
        if ak >= 1:   ln[ak-1] = n  ;  li[ak-1] = j   ;  ms = list(ln)  ;  iz = list(li)
        else:                                            ms = list(ln)  ;  iz = list(li)
        jz = js(i)
        ns = [ Notes.name(n, t, 1 if ak >= 5 else 0) for n in jz ]
        ks[k] = [ im, iz, ms, jz, ns ]
        slog(fmtks(k), pfx=0)
        i  = Notes.nextIndex(i, s)
        j  = Notes.nextIndex(j, s)
    return ks

########################################################################################################################################################################################################
def js(i):  return [ (i+j) % NTONES for j in JS ]

JS  = (0, 2, 4, 5, 7, 9, 11)
KIM = 0  ;  KIS = 1  ;  KMS = 2  ;  KJS = 3  ;  KNS = 4
KSD = {}
dmpKSDhdr(0)
KSD = initKSD(KSD, t=-1)
KSD = initKSD(KSD, t= 0)
KSD = initKSD(KSD, t= 1)
dmpKSDhdr(1)
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
        if   nic is None:   nict = ''
        else:
            nic[   j] += 1   ;   nict = f'nic[{m12(j)}]={nic[j]}'
            if nic[j] == 1:      slog(f'adding nic[{j}]={nic[j]}')
            if     j  == 11:     updNks(j, 'Cb', 'B', Notes.FLAT, 1)
            elif   j  ==  5:     updNks(j, 'F', 'E#', Notes.SHRP, 1)
            elif   j  ==  4:     updNks(j, 'Fb', 'E', Notes.FLAT, 1)
            elif   j  ==  0:     updNks(j, 'C', 'B#', Notes.SHRP, 1)
        name = Notes.name(i)
        if dbg or nict: slog(f'tab={tab} s={s} fn={fn} i={i:2} name={name:2} {nict}')
        return name

    @staticmethod
    def isFret(txt):             return 1 if '0' <= txt <= '9'  or 'a' <= txt <= 'o'   else 0
    @staticmethod
    def tab2fn(tab, dbg=0): fn = int(tab) if '0' <= tab <= '9' else int(ord(tab) - 87) if 'a' <= tab <= 'o' else None  ;  slog(f'tab={tab} fretNum={fn}') if dbg else None  ;  return fn
########################################################################################################################################################################################################

def updNks(i, m, n, t, t2):
    if   t  ==  Notes.FLAT:    Notes.I2F[i] = m
    elif t  ==  Notes.SHRP:    Notes.I2S[i] = n
    if   t2 == -1:
        if m in Notes.S2F: del Notes.S2F[m]
        if n in Notes.F2S: del Notes.F2S[n]
    elif t2 ==  1:
        Notes.F2S[n] = m   ;   Notes.S2F[m] = n
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
