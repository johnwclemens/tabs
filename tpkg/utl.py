import inspect, math, os, pathlib, sys, glob
from   inspect import currentframe as cfrm
import time
from   functools import wraps
import pyglet
import pyglet.window.key   as pygwink
import pyglet.sprite       as pygsprt
import pyglet.text         as pygtxt
from   tpkg          import unic
#from   tpkg.notes    import Notes
def fn( cf): return cf.f_code.co_name     # stack: func name
def ffn(cf): return cf.f_code.co_filename # stack: func file name

UNICODE       = unic.UNICODE
SPRSCRPT_INTS = { 0: '\u2070', 1: '\u00B9', 2: '\u00B2', 3: '\u00B3', 4: '\u2074', 5: '\u2075', 6: '\u2076', 7: '\u2077', 8: '\u2078', 9: '\u2079' }
ROOT_DIR      = os.getenv('ROOT_DIR', 'test')
BASE_PATH      = pathlib.Path.cwd() / ROOT_DIR
BASE_NAME      = BASE_PATH.stem
P, L, S, C    =  0,  1,  2,  3
T, N, I, K    =  4,  5,  6,  7
M, R, Q, H    =  8,  9, 10, 11
A, B, D, E    = 12, 13, 14, 15
W, X, Y, Z, NONE        = ' ', '\n', ',', '', 'None'
ALT, CTL, SHF, CPL, NML = pygwink.MOD_ALT, pygwink.MOD_CTRL, pygwink.MOD_SHIFT, pygwink.MOD_CAPSLOCK, pygwink.MOD_NUMLOCK
CAT,  CSV,  EVN,  LOG,  PNG,  TXT,  DAT  =     'cat' ,     'csv' ,     'evn',      'log' ,     'png' ,     'txt' ,     'dat'
CATS, CSVS, EVNS, LOGS, PNGS, TEXT, DATA =     'cats',     'csvs',     'evns',     'logs',     'pngs',     'text',     'data'
LBL, SPR              = pygtxt.Label, pygsprt.Sprite
TT, NN, II, KK        =  0,  1,  2,  3
CSR_MODES             = ['MELODY', 'CHORD', 'ARPG']
HARROWS, VARROWS      = ['LARROW', 'RARROW'], ['DARROW', 'UARROW']
MLDY, CHRD, ARPG      =  0, 1, 2
LARROW, RARROW, DARROW, UARROW =  0, 1, 0, 1
NORMAL_STYLE, SELECT_STYLE, CURRENT_STYLE = 0, 1, 2
CSV_FILE, EVN_FILE, LOG_FILE, TXT_FILE = None, None, None, None
BGC, BOLD, COLOR, FONT_NAME, FONT_SIZE, ITALIC, KERNING, UNDERLINE = 'background_color', 'bold', 'color', 'font_name', 'font_size', 'italic', 'kerning', 'underline'
MAX_FREQ_IDX          = 10 * 12 + 1
MAX_STACK_DEPTH       = 0
MAX_STACK_FRAME       = inspect.stack()
INIT, FINI            = 'INIT', 'FIN'
RGB       = {}
#             0   1   2   3   4   5   6    7    8    9   10   11   12   13   14   15   16   17
OPC       = [ 0, 15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165, 170, 195, 210, 225, 240, 255 ]
INIT_BGN  = '###   Init BGN  ###' * 10
INIT_END  = '###   Init END  ###' * 10
QUIT_BGN  = '###   Quit BGN  ###' * 10
QUIT      = '###     Quit    ###' * 10
QUIT_END  = '###   Quit END  ###' * 10
STFILT    = ['log', 'tlog', 'flog', 'fmtl', 'fmtm', 'dumpGeom', 'resetJ', 'dumpJs', 'dumpImap', 'dumpSmap', 'dumpCursorArrows', '<listcomp>', 'dumpLimap2', 'dumpTniksPfx', 'dumpTniksSfx', 'fmtXYWH', 'kbkInfo', 'dumpCrs', 'fCrsCrt'] # , 'dumpView', 'dumpLbox', 'dumpRect']
FONT_NAMES  = [ 'Lucida Console', 'Times New Roman', 'Arial', 'Courier New', 'Blockbusted', 'Fridays', 'Vogue', 'Open 24 Display St' ]
########################################################################################################################################################################################################
def init(cfile, efile, lfile, tfile, f):
    pyglet.font.add_directory('./res/fonts')
    global CSV_FILE, EVN_FILE, LOG_FILE, TXT_FILE   ;   CSV_FILE, EVN_FILE, LOG_FILE, TXT_FILE = cfile, efile, lfile, tfile
    argv   = sys.argv
    argc   = len(argv)
    slog(f'{argc=} {fmtl(argv)=}', f=f)
    for i in range(1, argc): slog(f'argv[{i}]={argv[i]}', f=f)
    ARGS   = parseCmdLine(argv, f=f)
    slog(  f'   ARGS={fmta(ARGS)}', f=f)
    slog(f'{ROOT_DIR=}', f=f)
    return   ARGS
########################################################################################################################################################################################################
def OLD__timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        bgn    = time.time()
        result = func(*args, **kwargs)
        end    = time.time()
        if args and kwargs: slog(f'{end-bgn:.6f} seconds {func.__name__}({fmtl(args)}, {fmtm(kwargs)}) = {result}')
        elif kwargs:        slog(f'{end-bgn:.6f} seconds {func.__name__}({fmtm(kwargs)}) = {result}')
        elif args:          slog(f'{end-bgn:.6f} seconds {func.__name__}({fmtl(args)}) = {result}')
        else:               slog(f'{end-bgn:.6f} seconds {func.__name__}() = {result}')
        return result
    return wrapper

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        bgn    = time.time()
        result = func(*args, **kwargs)
        end    = time.time()
        if   args and len(args) > 1 and kwargs: slog(f'{end-bgn:.6f} seconds {func.__name__}({fmtl(args, d=Z, s=Y)},{fmtm(kwargs, d=Z, s=Y)}) = {result}')
        elif args and len(args) > 1:            slog(f'{end-bgn:.6f} seconds {func.__name__}({fmtl(args, d=Z, s=Y)}) = {result}')
        elif args and kwargs:                   slog(f'{end-bgn:.6f} seconds {func.__name__}({args[0]},{fmtm(kwargs, d=Z, s=Y)}) = {result}')
        elif args:                              slog(f'{end-bgn:.6f} seconds {func.__name__}({args[0]}) = {result}')
        elif kwargs:                            slog(f'{end-bgn:.6f} seconds {func.__name__}({fmtm(kwargs, d=Z, s=Y)}) = {result}')
        else:                                   slog(f'{end-bgn:.6f} seconds {func.__name__}() = {result}')
        return result
    return wrapper

@timer
def timerA(a=1, b=2, c=3):
    return a + b + c
########################################################################################################################################################################################################
def dbg1(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        slog(f'{func.__name__}({args} {kwargs})={result}')
        return result
    return wrapper

def dbg0(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        slog(f'{func.__name__}({args} {kwargs})={result}', p=0, f=-2)
        return result
    return wrapper
########################################################################################################################################################################################################
def memorize(func):
    cache = {}
    @wraps(func)
    def wrapper(*args):
        if args in cache:
            return cache[args]
        result = func(*args)
        cache[args] = result
        return result
    return wrapper

def paths():           return BASE_NAME, BASE_PATH
########################################################################################################################################################################################################
def fri(f):            return int(math.floor(f + 0.5))
def filtA(v, a=W):     return Z.join([ e for e in v if e!=a ])
def signed(n):         return f' {n}' if n==0 else f'{n:+}'
def ns2signs(ns, s=Z): return [ f'-{s}' if n<0 else f'+{s}' if n>0  else f'{W}{s}' for n in ns ]
def fColor(c, d=1):    d = "[" if d else Z  ;  return f'{NONE:^17}' if c is None else f'{fmtl(c, w=3, d=d):17}'
########################################################################################################################################################################################################
def isAlt(      d, m=0): return d[ALT]                       if d and ALT in d                           else m & ALT
def isCtl(      d, m=0): return d[CTL]                       if d and CTL in d                           else m & CTL
def isShf(      d, m=0): return d[SHF]                       if d and SHF in d                           else m & SHF
def isCtlShf(   d, m=0): return d[CTL] and d[SHF]            if d and CTL in d and SHF in d              else m & CTL and m & SHF
def isAltShf(   d, m=0): return d[ALT] and d[SHF]            if d and ALT in d and SHF in d              else m & ALT and m & SHF
def isCtlAlt(   d, m=0): return d[CTL] and d[ALT]            if d and CTL in d and ALT in d              else m & CTL and m & ALT
def isCtlAltShf(d, m=0): return d[CTL] and d[ALT] and d[SHF] if d and CTL in d and ALT in d and SHF in d else m & CTL and m & ALT and m & SHF
def isCapLck(   d, m=0): return d[CPL]                       if d and CPL in d                           else m & CPL
def isNumLck(   d, m=0): return d[NML]                       if d and NML in d                           else m & NML
########################################################################################################################################################################################################
def stackDepth(sfs):
    global     MAX_STACK_DEPTH, MAX_STACK_FRAME
    for i, _ in enumerate(sfs):
        j = len(sfs) - (i + 1)
        if j > MAX_STACK_DEPTH: MAX_STACK_FRAME = sfs  ;  MAX_STACK_DEPTH = j
    return  len(sfs)

def fmtSD(sd): return f'{sd:{sd}}'

def dumpStack(sfs):
    for i, sf in enumerate(sfs):
        fp = pathlib.Path(sf.filename)  ;   n = fp.stem  ;  l = sf.lineno  ;  f = sf.function  ;  c = sf.code_context[0].strip() if sf.code_context else Z  ;  j = len(sfs) - (i + 1)
        slog(f'{j:2} {n:9} {l:5} {f:20} {c}')
    slog(f'MAX_STACK_DEPTH={MAX_STACK_DEPTH:2}')

def rotateList(a, rev=0):
    if rev: tmp0 = a[-1]   ;   tmp1 = a[:-1]   ;   a = tmp1   ;   a.insert(0, tmp0)
    else:   tmp0 = a[0]    ;   tmp1 = a[1:]    ;   a = tmp1   ;   a.append(tmp0)
    return     a
########################################################################################################################################################################################################
def slog(t=Z, p=1, f=1, s=Y, e=X, ff=1, ft=1):   # text, prfx, file, sepr, end, flush, filter
    if t and ft: t = filtText(t)
    if p:
        sf = cfrm().f_back                       # cfrm:  current frame  # sf: stack frame
        while fn(sf) in STFILT:   sf = sf.f_back # fn():  func name
        l = f'#{sf.f_lineno:4} '  if p >= 2 else '#' # set p >= 2 to print line numbers
        fp = pathlib.Path(ffn(sf))               # ffn(): func file name
        s  = f'{fp.stem:5} '
        t  =  f'{l}{s}{fn(sf):18} ' + t          # fn():  func name
    tx, so, cs = 0, 0, 0
    if   f == -3: f = LOG_FILE  ;  tx = 1  ;  so = 1
    elif f == -2: f = TXT_FILE  ;  so = 1
    elif f == -1: f = sys.stdout
    elif f ==  0: f = TXT_FILE
    elif f ==  1: f = LOG_FILE
    elif f ==  2: f = LOG_FILE  ;  tx = 1
    elif f ==  3: f = CSV_FILE
    elif f ==  4: f = EVN_FILE
    else:         f = LOG_FILE  ;  tx = 1  ;  so = 1
    print(t, sep=s, end=e, file=f,          flush=bool(ff))
    print(t, sep=s, end=e, file=TXT_FILE,   flush=bool(ff)) if tx else None
    print(t, sep=s, end=e, file=sys.stdout, flush=bool(ff)) if so else None
    print(t, sep=s, end=e, file=CSV_FILE,   flush=bool(ff)) if cs else None

def olog(o=None, p=1, f=1, s=Y, e=X, ff=1): #, ft=1):
    o = s.join(str(o)) if o is not None else Z
    if p:
        sf   = fn(cfrm())
        while sf.f_code.co_name in STFILT: sf = sf.f_back # ;  print(f'sf 2: {sf.f_lineno}, {sf.f_code.co_name}')
        fp   = pathlib.Path(sf.f_code.co_filename)
        pl   = 18 if p == 1 else 8
        p    = f'{sf.f_lineno:4} {fp.stem:5} ' if p == 1 else Z
        o    = [f'{p}{sf.f_code.co_name:{pl}} ', o]
    tf = 0
    if   f == 0:  f = TXT_FILE
    elif f == 1:  f = LOG_FILE
    elif f == 2:  f = LOG_FILE  ;  tf = 1
    elif f == 3:  f = CSV_FILE
    print(o, sep=s, end=e, file=f,        flush=bool(ff))
    print(o, sep=s, end=e, file=TXT_FILE, flush=bool(ff)) if tf else None
########################################################################################################################################################################################################
def filtText(text):
    text = text.replace('self', Z)
    text = text.replace('cls',  Z)
    text = text.replace('tobj', Z)
    text = text.replace('utl',  Z)
    text = text.replace('fmtl', Z)
    text = text.replace('fmtm', Z)
    return text
########################################################################################################################################################################################################
def ordSfx(n):
    m = n % 10
    if   m == 1 and n != 11: return 'st'
    if   m == 2 and n != 12: return 'nd'
    if   m == 3 and n != 13: return 'rd'
    return 'th'
########################################################################################################################################################################################################
def ist(o, t):  return isinstance(o, t)

def replceDelims(d):
    o = ['[', '{', '<', '(', '|']
    c = [']', '}', '>', ')', Z]
    for i, oo in enumerate(o):
        d = d.replace(oo, c[i])
    return d
########################################################################################################################################################################################################
def fmtl(lst, w=None, u=None, d='[', d2=None, s=W, ll=None): #todo remove negative ll, zl values
    if   lst is None:   return  NONE
    lts = (list, tuple, set, frozenset, zip)  ;  dtn = (int, float)  ;  dts = (str,)
    assert type(lst) in lts,   f'{type(lst)=} {lts=}'
    if d2 is None:    d2 = replceDelims(d)
    w   = w   if w else Z   ;   t = []
    zl  = '-'               if ll is not None and ll<0 else '+' if ll is not None and ll>0 else Z
    z   = f'{zl}{len(lst)}' if ll is not None          else Z
    for i, l in enumerate(lst):
        if type(l) in lts:
            if type(w) in lts:            t.append(fmtl(l, w[i], u, d, d2, s, ll))
            else:                         t.append(fmtl(l, w,    u, d, d2, s, ll))
        else:
            ss = s if i < len(lst)-1 else Z
            u = Z if u is None else u
            if   ist(l, type):            l =  str(l)
            elif l is None:               l =  NONE
            if   ist(w, lts):             t.append(f'{l:{u}{w[i]}}{ss}')
            elif ist(l, dtn):             t.append(f'{l:{u}{w   }}{ss}')
            elif ist(l, dts):             t.append(f'{l:{u}{w   }}{ss}')
            else:                         t.append(f'{l}{ss}')
    return z + d + Z.join(t) + d2
########################################################################################################################################################################################################
def fmtm(m, w=None, wv=None, u=None, uv=None, d0=':', d='{', d2=None, s=W, ll=None):
    if m is None: return NONE
    w  = w  if w  is not None else Z   ;  t = []
    wv = wv if wv is not None else w
    if d2 is None:    d2 = replceDelims(d)
    u  = Z if u  is None else u
    uv = Z if uv is None else uv
    for i, (k, v) in enumerate(m.items()):
        ss = s if i < len(m) - 1 else Z
        if   ist(v, (list, tuple, set)):  t.append(f'{d}{k:{u}{w}}{d0}{fmtl(v, wv, ll=k if ll==-1 else ll)}{d2}{ss}')
        elif ist(v, dict): b,c='{','}' ;  t.append(f'{b}{k:{u}{w}}{d0}{d}{fmtm(v, d=Z)}{d2}{c}{X}')
        elif ist(v, (int, str)):          t.append(f'{d}{k:{u}{w}}{d0}{v:{uv}{wv}}{d2}{ss}')
    return d + Z.join(t) + d2
########################################################################################################################################################################################################
def fmtf(a, b):
    if   b ==  4: return  f'{a:4.2f}'  if a < 10 else  f'{a:4.1f}'  if a < 100 else  f'{a:4.0f}'
    elif b ==  5: return  f'{a:5.3f}'  if a < 10 else  f'{a:5.2f}'  if a < 100 else  f'{a:5.1f}' if a < 1000 else  f'{a:5.0f}'
    elif b ==  6: return  f'{a:6.4f}'  if a < 10 else  f'{a:6.3f}'  if a < 100 else  f'{a:6.2f}' if a < 1000 else  f'{a:6.1f}' if a < 10000 else  f'{a:6.0f}'
    elif b ==  7: return  f'{a:7.5f}'  if a < 10 else  f'{a:7.4f}'  if a < 100 else  f'{a:7.3f}' if a < 1000 else  f'{a:7.2f}' if a < 10000 else  f'{a:7.1f}' if a < 100000 else  f'{a:7.0f}'
    elif b ==  8: return  f'{a:8.6f}'  if a < 10 else  f'{a:8.5f}'  if a < 100 else  f'{a:8.4f}' if a < 1000 else  f'{a:8.3f}' if a < 10000 else  f'{a:8.2f}' if a < 100000 else  f'{a:8.1f}' if a < 1000000 else  f'{a:8.0f}'
    elif b ==  9: return  f'{a:9.7f}'  if a < 10 else  f'{a:9.6f}'  if a < 100 else  f'{a:9.5f}' if a < 1000 else  f'{a:9.4f}' if a < 10000 else  f'{a:9.3f}' if a < 100000 else  f'{a:9.2f}' if a < 1000000 else  f'{a:9.1f}' if a < 10000000 else  f'{a:9.0f}'
    elif b == 10: return f'{a:10.8f}'  if a < 10 else f'{a:10.7f}'  if a < 100 else f'{a:10.6f}' if a < 1000 else f'{a:10.5f}' if a < 10000 else f'{a:10.4f}' if a < 100000 else f'{a:10.3f}' if a < 1000000 else f'{a:10.2f}' if a < 10000000 else f'{a:10.1f}' if a < 100000000 else f'{a:10.0}'
    elif b == 11: return f'{a:11.9f}'  if a < 10 else f'{a:11.8f}'  if a < 100 else f'{a:11.7f}' if a < 1000 else f'{a:11.6f}' if a < 10000 else f'{a:11.5f}' if a < 100000 else f'{a:11.4f}' if a < 1000000 else f'{a:11.3f}' if a < 10000000 else f'{a:11.2f}' if a < 100000000 else f'{a:11.1}' if a < 1000000000 else f'{a:11.0}'
    elif b == 12: return f'{a:12.10f}' if a < 10 else f'{a:12.9f}'  if a < 100 else f'{a:12.8f}' if a < 1000 else f'{a:12.7f}' if a < 10000 else f'{a:12.6f}' if a < 100000 else f'{a:12.5f}' if a < 1000000 else f'{a:12.4f}' if a < 10000000 else f'{a:12.3f}' if a < 100000000 else f'{a:12.2}' if a < 1000000000 else f'{a:12.1}' if a < 10000000000 else f'{a:12.0}'
    elif b == 13: return f'{a:13.11f}' if a < 10 else f'{a:13.10f}' if a < 100 else f'{a:13.9f}' if a < 1000 else f'{a:13.8f}' if a < 10000 else f'{a:13.7f}' if a < 100000 else f'{a:13.6f}' if a < 1000000 else f'{a:13.5f}' if a < 10000000 else f'{a:13.4f}' if a < 100000000 else f'{a:13.3}' if a < 1000000000 else f'{a:13.2}' if a < 10000000000 else f'{a:13.1}' if a < 100000000000 else f'{a:13.0}'

def fmtg(a, b):
    if a < 0: s = '-'   ;   a = abs(a)
    else:     s = '+'
    if   b ==  4: return f'{s}{a:.1f}'  if a < 10 else f'{s}{a:.0f}' if a < 100 else f'{s}{a:.0f}'
    elif b ==  5: return f'{s}{a:.2f}'  if a < 10 else f'{s}{a:.1f}' if a < 100 else f'{s}{a:.0f}' if a < 1000 else f'{s}{a:.0f}'
    elif b ==  6: return f'{s}{a:.3f}'  if a < 10 else f'{s}{a:.2f}' if a < 100 else f'{s}{a:.1f}' if a < 1000 else f'{s}{a:.0f}'
    elif b ==  7: return f'{s}{a:.4f}'  if a < 10 else f'{s}{a:.3f}' if a < 100 else f'{s}{a:.2f}' if a < 1000 else f'{s}{a:.1f}' if a < 10000 else f'{s}{a:.0f}'
    elif b ==  8: return f'{s}{a:.5f}'  if a < 10 else f'{s}{a:.4f}' if a < 100 else f'{s}{a:.3f}' if a < 1000 else f'{s}{a:.2f}' if a < 10000 else f'{s}{a:.1f}' if a < 100000 else f'{s}{a:.0f}'
    elif b ==  9: return f'{s}{a:.6f}'  if a < 10 else f'{s}{a:.5f}' if a < 100 else f'{s}{a:.4f}' if a < 1000 else f'{s}{a:.3f}' if a < 10000 else f'{s}{a:.2f}' if a < 100000 else f'{s}{a:.1f}' if a < 1000000 else f'{s}{a:.0f}'
    elif b == 10: return f'{s}{a:.7f}'  if a < 10 else f'{s}{a:.6f}' if a < 100 else f'{s}{a:.5f}' if a < 1000 else f'{s}{a:.4f}' if a < 10000 else f'{s}{a:.3f}' if a < 100000 else f'{s}{a:.2f}' if a < 1000000 else f'{s}{a:.1f}' if a < 10000000 else f'{s}{a:.0f}'
    elif b == 11: return f'{s}{a:.8f}'  if a < 10 else f'{s}{a:.7f}' if a < 100 else f'{s}{a:.6f}' if a < 1000 else f'{s}{a:.5f}' if a < 10000 else f'{s}{a:.4f}' if a < 100000 else f'{s}{a:.3f}' if a < 1000000 else f'{s}{a:.2f}' if a < 10000000 else f'{s}{a:.1f}' if a < 100000000 else f'{s}{a:.0f}'
    elif b == 12: return f'{s}{a:.9f}'  if a < 10 else f'{s}{a:.8f}' if a < 100 else f'{s}{a:.7f}' if a < 1000 else f'{s}{a:.6f}' if a < 10000 else f'{s}{a:.5f}' if a < 100000 else f'{s}{a:.4f}' if a < 1000000 else f'{s}{a:.3f}' if a < 10000000 else f'{s}{a:.2f}' if a < 100000000 else f'{s}{a:.1f}' if a < 1000000000 else f'{s}{a:.0f}'
    elif b == 13: return f'{s}{a:.10f}' if a < 10 else f'{s}{a:.9f}' if a < 100 else f'{s}{a:.8f}' if a < 1000 else f'{s}{a:.7f}' if a < 10000 else f'{s}{a:.6f}' if a < 100000 else f'{s}{a:.5f}' if a < 1000000 else f'{s}{a:.4f}' if a < 10000000 else f'{s}{a:.3f}' if a < 100000000 else f'{s}{a:.2f}' if a < 1000000000 else f'{s}{a:.1f}' if a < 10000000000 else f'{s}{a:.0f}'
########################################################################################################################################################################################################
def fmta(args):
    t = []
    for k, v in args.items():
        t.append(f'{k}:')
        t.append(f'{fmtl(v, d=Z)} ')
    return Z.join(t)
########################################################################################################################################################################################################
def parseCmdLine(argv, dbg=1, f=0):
    options, key, vals, argc = {}, Z, [], len(argv)
    if dbg: slog(f'argv={fmtl(argv[1:])}', f=f)  ;  slog(argv[0], f=f)
    for j in range(1, argc):
        arg = argv[j]
        if len(arg) > 2 and arg[0] == '-' and arg[1] == '-':
            if argv[2].isalpha():
                vals = []
                key = arg[2:]
                options[key] = vals
                if dbg: slog(f'{j:2} long    {arg:2} {key} {fmtl(vals)}', p=0, f=f, e=W)
            else:
                slog(  f'{j:2} ERROR long    {arg:2} {key} {fmtl(vals)}', f=f, e=W)
        elif len(arg) > 1 and arg[0] == '-':
            if arg[1].isalpha() or arg[1] == '?':
                vals = [] #  ;   cnt = 0
                if len(arg) == 2:
                    key = arg[1:] #  ;   p = 1 if not cnt else 0 # p = 1 if not len(vals) else 0
                    if dbg: slog(f'{j:2} short   {arg:2} {key} {fmtl(vals)}', f=f, e=W)
                    options[key] = vals
                elif len(arg) > 2:
                    for i in range(1, len(arg)):
                        key = arg[i]
                        if dbg: slog(f'{j:2} short   {arg:2} {key} {fmtl(vals)}', p=0, f=f, e=W)
                        options[key] = vals
            elif arg[1].isdigit():
                vals.append(arg)
                options[key] = vals
                if dbg: slog(f'{j:2} neg arg {arg:2} {key} {fmtl(vals)}', p=0, f=f, e=W)
            else:
                vals.append(arg)
                options[key] = vals
                if dbg: slog(f'{j:2} ??? arg {arg:2} {key} {fmtl(vals)}', p=0, f=f, e=W)
        else:
            vals.append(arg)
            options[key] = vals
            if dbg: slog(f'{j:2} arg     {arg:2} {key} {fmtl(vals)}', p=0, f=f, e=W)
        if dbg: slog(p=0, f=f)
    if dbg: slog(f'options={fmta(options)}', f=f)
    return options
########################################################################################################################################################################################################
def dumpRGB(f, dbg=0):
    s = W*7   ;   olen = len(OPC)
    o = [ f' {o}' for o in range(olen) ]
    slog(f'RGB{s}{fmtl(o, w=3,d=Z)}   Diff Span', p=0, f=f)
    vs = {}
    for k, v in RGB.items():
        slog(f'{k}:   ', p=0, f=f, e=Z) if dbg else None   ;   vl = []
        for i in range(olen):
            u  = list(v[i])
            u0 = list(u[i])
            v0 = rotateList(u0, rev=1)
            vl.append(v0)
            vs[k] = vl
        slog(f'{fmtl(vs[k], w=3)}', p=0, f=f, e=Z) if dbg else None
        slog(p=0, f=f) if dbg else None
    slog(f'{"##### zip ####### zip ####"*10}', p=0, f=f) if dbg else None  ;  zs = []
    for k, v in vs.items():
        zs.append(list(zip(*v)))
    for j, z in enumerate(zs):
        for i, y in enumerate(z):
            pfx  = f'{list(vs.keys())[j]}:   ' if not i else f'{W * 7}'   ;   n = olen - 1
            lbl  = 'O=' if i==0 else 'R=' if i==1 else 'G=' if i==2 else 'B=' if i==3 else '?='
            diff = y[n] - y[0]
            span = diff/n
            info = f'{diff:5.1f} {span:4.1f}'
            slog(f'{pfx}{lbl}{fmtl(y, w=3)} {info}', p=0, f=f)
    slog(f'{"##### zip ####### zip ####"*10}', p=0, f=f) if dbg else None

def initRGBs(f, dbg=0):
    aaa, bbb, ccc =  31,  63, 127
    ddd, eee, fff = 176, 208, 255
    if dbg:
        s = W*7  ;  t = f'{s}RGB '
        o = [ f' {o}' for o in range(len(OPC)) ]
        slog(f'RGB{s}{fmtl(o, w=3,d=Z)}{t}Diffs  {t}Steps', p=0, f=f)
    initRGB('FSH', (255, aaa, 255), dbg=dbg)  # 0
    initRGB('PNK', (255, 128, 192), dbg=dbg)  # 1
    initRGB('RED', (255, bbb, bbb), dbg=dbg)  # 2
    initRGB('RST', (255,  96,  10), dbg=dbg)  # 3
    initRGB('ORG', (255, 176, aaa), dbg=dbg)  # 5
    initRGB('PCH', (255, 160, 128), dbg=dbg)  # 4
    initRGB('YLW', (255, 255, bbb), dbg=dbg)  # 6
    initRGB('LIM', (160, 255, aaa), dbg=dbg)  # 7
    initRGB('GRN', (bbb, 255, bbb), dbg=dbg)  # 8
    initRGB('TRQ', (aaa, 255, 192), dbg=dbg)  # 9
    initRGB('CYA', (aaa, 255, 255), dbg=dbg)  # 10
    initRGB('IND', (aaa, 180, 255), dbg=dbg)  # 11
    initRGB('BLU', (bbb, bbb, 255), dbg=dbg)  # 12
    initRGB('VLT', (128, bbb, 255), dbg=dbg)  # 13
    initRGB('GRY', (255, 255, 255), dbg=dbg)  # 14
    initRGB('CL1', (ccc, aaa, 255), dbg=dbg)  # 15
    initRGB('CL2', (255, fff, bbb), dbg=dbg)  # 16
    initRGB('CL3', (255, bbb, eee), dbg=dbg)  # 17
    initRGB('CL4', (aaa, ccc, bbb), dbg=dbg)  # 18
    return RGB.keys()

def initRGB(key, rgb, dv=32, n=None, dbg=0):
    colors = []  ;  lrgb, lopc = len(rgb), len(OPC)  ;  msg, msgR, msgG, msgB = [], [], [], []  ;  n = n + 1 if n is not None else lopc  ;  opc, color = None, None
    diffs  = [ rgb[i] - rgb[i]/dv for i in range(lrgb) ]
    steps  = [ diffs[i]/(n-1)     for i in range(lrgb) ]
    if dbg: msg.append(f'{key:3}:   O=[')
    for j in range(n):
        clrs = []
        if dbg > 2: slog(f'{key:4} {fmtl(rgb, w=3)} {opc=:2} {OPC[opc]:3} {dv=} {n=} {fmtl(diffs, w=".2f")} ', e=Z)  ;  slog(fmtl(steps, w=".2f"), p=0, f=1)
        for opc in range(lopc):
            if dbg: msg.append(f'{OPC[opc]:3} ' if not j else Z)
            color = list([ fri(rgb[i]/dv + j*steps[i]) for i in range(lrgb) ])   ;  color.append(OPC[opc])  ;  clrs.append(tuple(color))
            if dbg > 1:    slog(f'{j:2} {key:4} {fColor(color)}', p=0, e=W)
        if dbg > 1:        slog(p=0)
        if dbg: msgR.append(color[0])   ;   msgG.append(color[1])   ;   msgB.append(color[2])
        colors.append(clrs)
    if dbg:
        msg = Z.join(msg)
        slog( f'{msg[:-1]}] {fmtl(diffs, w="5.1f")} {fmtl(steps, w="4.1f")}', p=0)  ;  msgs = [msgR, msgG, msgB]  ;  rgb = 'RGB'
        for i, msg in enumerate(msgs): slog(f'       {rgb[i]}={fmtl(msg, w=3)}', p=0)
    global RGB  ;  RGB[key] = colors
    return list(RGB.keys())
########################################################################################################################################################################################################
# 0   1    2    3    4    5    6    7    8    9   10   11   12   13   14   15   16   17   18
FSH, PNK, RED, RST, ORG, PCH, YLW, LIM, GRN, TRQ, CYA, IND, BLU, VLT, GRY, CL1, CL2, CL3, CL4 = initRGBs(f=0, dbg=0)
########################################################################################################################################################################################################
def initColors(k, spr, bgc, ik):
    KP1, KP2 = VLT, VLT  ;  KL1, KL2 = FSH, FSH  ;  KS1, KS2 = RED, RED  ;  KC1, KC2 = PNK, PNK  ;  OP1, OP2 =  7, 17  ;  OL1, OL2 = 5, 11  ;  OS1, OS2 = 5, 11  ;  OC1, OC2 =  5, 11
    KT1, KT2 = ORG, ORG  ;  KN1, KN2 = GRN, GRN  ;  KI1, KI2 = YLW, YLW  ;  KK1, KK2 = CYA, CYA  ;  OT1, OT2 = 17, 17 # ;  ON1, ON2 =  0,  0  ;  OI1, OI2 =  0,  0  ;  OK1, OK2 =  0,  0
    KR1, KR2 = BLU, BLU  ;  KQ1, KQ2 = IND, IND  ;  KH1, KH2 = TRQ, TRQ  ;  KM1, KM2 = PCH, PCH  ;  OR1, OR2 = 17, 17  ;  OQ1, OQ2 = 17, 17  ;  OH1, OH2 =  9,  9
    KB1, KB2 = CL3, CL3  ;  KA1, KA2 = CL2, CL2  ;  KD1, KD2 = CL1, CL1  ;  KE1, KE2 = GRY, GRY  ;  OE1, OE2 = 17, 17  ;  aa, zz = 5, 17
    a = not spr and not bgc  ;  b = not spr and bgc  ;  c = spr and not bgc  ;  d = spr and bgc  ;  i = ik
    j = P  ;  k[j] = i(j, KP1, aa, OP1, KP2, zz, OP2) if a else i(j, KP1, 17, 17, KP2, 17, 17) if b else i(j, KP1,  3, 17, KP2, 17, 17) if c else i(j, KP1,  3, 17, KP2, 17, 17) if d else None
    j = L  ;  k[j] = i(j, KL1, aa, OL1, KL2, zz, OL2) if a else i(j, KL1,  3, 15, KL2, 17, 15) if b else i(j, KL1,  3, 15, KL2, 17, 15) if c else i(j, KL1,  3, 15, KL2, 17, 15) if d else None
    j = S  ;  k[j] = i(j, KS1, aa, OS1, KS2, zz, OS2) if a else i(j, KS1,  3, 15, KS2, 17, 15) if b else i(j, KS1,  3, 15, KS2, 17, 15) if c else i(j, KS1,  3, 15, KS2, 17, 15) if d else None
    j = C  ;  k[j] = i(j, KC1, aa, OC1, KC2, zz, OC2) if a else i(j, KC1,  3, 15, KC2, 17, 15) if b else i(j, KC1,  3, 15, KC2, 17, 15) if c else i(j, KC1,  3, 15, KC2, 17, 15) if d else None
    j = T  ;  k[j] = i(j, KT1, aa, OT1, KT2, zz, OT2) if a else i(j, KT1,  0, 17, KT2, 17, 17) if b else i(j, KT1,  0, 17, KT2, 17, 17) if c else i(j, KT1,  0, 17, KT2, 17, 17) if d else None
    j = N  ;  k[j] = i(j, KN1, aa, OT1, KN2, zz, OT2) if a else i(j, KN1,  0, 17, KN2, 17, 17) if b else i(j, KN1,  0, 17, KN2, 17, 17) if c else i(j, KN1,  0, 17, KN2, 17, 17) if d else None
    j = I  ;  k[j] = i(j, KI1, aa, OT1, KI2, zz, OT2) if a else i(j, KI1,  0, 17, KI2, 17, 17) if b else i(j, KI1,  0, 17, KI2, 17, 17) if c else i(j, KI1,  0, 17, KI2, 17, 17) if d else None
    j = K  ;  k[j] = i(j, KK1, aa, OT1, KK2, zz, OT2) if a else i(j, KK1,  0, 17, KK2, 17, 17) if b else i(j, KK1,  0, 17, KK2, 17, 17) if c else i(j, KK1,  0, 17, KK2, 17, 17) if d else None
    j = M  ;  k[j] = i(j, KM1, aa, OE1, KM2, zz, OE2) if a else i(j, KM1, 17, 10, KM2, 17, 17) if b else i(j, KM1, 17, 17, KM2, 17, 17) if c else i(j, KM1, 17, 17, KM2, 17, 17) if d else None
    j = R  ;  k[j] = i(j, KR1, aa, OR1, KR2, zz, OR2) if a else i(j, KR1,  0, 17, KR2, 17, 17) if b else i(j, KR1,  0, 17, KR2, 17, 17) if c else i(j, KR1,  0, 17, KR2, 17, 17) if d else None
    j = Q  ;  k[j] = i(j, KQ1, aa, OQ1, KQ2, zz, OQ2) if a else i(j, KQ1,  0, 17, KQ2, 17, 17) if b else i(j, KQ1,  0, 17, KQ2, 17, 17) if c else i(j, KQ1,  0, 17, KQ2, 17, 10) if d else None
    j = H  ;  k[j] = i(j, KH1, zz, OH1, KH2, aa, OH2) if a else i(j, KH1, 14, 10, KH2, 14, 10) if b else i(j, KH1, 15, 13, KH2, 15, 13) if c else i(j, KH1, 14, 11, KH2, 14, 10) if d else None
    j = A  ;  k[j] = i(j, KA1, aa, OE1, KA2, zz, OE2) if a else i(j, KA1,  0,  0, KA2, 17, 17) if b else i(j, KA1,  0,  0, KA2, 17, 17) if c else i(j, KA1,  0,  0, KA2, 17, 17) if d else None
    j = B  ;  k[j] = i(j, KB1, aa, OE1, KB2, zz, OE2) if a else i(j, KB1,  0,  0, KB2, 17, 17) if b else i(j, KB1,  0,  0, KB2, 17, 17) if c else i(j, KB1,  0,  0, KB2, 17, 17) if d else None
    j = D  ;  k[j] = i(j, KD1, aa, OE1, KD2, zz, OE2) if a else i(j, KD1,  0,  0, KD2, 17, 17) if b else i(j, KD1,  0,  0, KD2, 17, 17) if c else i(j, KD1,  0,  0, KD2, 17, 17) if d else None
    j = E  ;  k[j] = i(j, KE1, aa, OE1, KE2, zz, OE2) if a else i(j, KE1,  0,  0, KE2, 17, 17) if b else i(j, KE1,  0,  0, KE2, 17, 17) if c else i(j, KE1,  0,  0, KE2, 17, 17) if d else None
########################################################################################################################################################################################################
def path2str(po, dbg=0):
    ps = list(po.parts[1:])
    ps.insert(0, po.drive)
    p = '/'.join(ps)
    if dbg:  slog(f'{p}', f=2)
    return p

def getFilePath(baseName, basePath, fdir=None, fsfx='txt', dbg=1, f=-3):
    if dbg: slog(f'{baseName =:12} {path2str(basePath) = }', f=f)
    if dbg: slog(f'{baseName =:12} {basePath = }', f=f)
    fileName   = f'{baseName}.{fsfx}'          if fsfx else baseName
    filePath   =    basePath / fdir / fileName if fdir else basePath / fileName
    if dbg: slog(f'{fileName =:12} {path2str(filePath) = }', f=f)
    if dbg: slog(f'{fileName =:12} {filePath = }', f=f)
    return  filePath

def copyFile(src, trg, dbg=1, f=-3):
    if dbg: slog(f'{path2str(src)=}', f=f)
    if dbg: slog(f'{path2str(trg)=}', f=f)
    if dbg: slog(f'{src=}', f=f)
    if dbg: slog(f'{trg=}', f=f)
    if not src.exists():   msg = f'ERROR Path Does not Exist {src=}'   ;   print(msg)   ;  raise SystemExit(msg)
    cmd  =  f'copy {src} {trg}'   ;   ret = '???'
    if dbg: slog(f'{12*W}{cmd} ###', f=f)
    slog(f'TRY ret = os.system({cmd})', f=f)
    try:
        ret = os.system(cmd)
    except BaseException as e:
        slog(f'ERROR {ret=} {e=}', f=f)
    else:
        slog(f'OK {ret=}', f=f)
    finally:
        slog(f'FINALLY {ret=}', f=f)
    slog(f'os.system {ret=}', f=f)
    return ret
########################################################################################################################################################################################################
def getFileSeqName(baseName, basePath, fdir='logs', fsfx='log'):
    n = 1
    slog(f'    {fdir=} / {fsfx=}')
    fGlobArg = f'{(basePath / fdir / baseName)}.*.{fsfx}' # todo investigate this
#    tmpPath  = f'{basePath}\\{fdir}'
#    fileName = f'{baseName}.*.{fsfx}'
#    fGlobArg = f'{tmpPath}\\{fileName}'
    fGlob    = glob.glob(fGlobArg)
    slog(f'{fGlobArg=}')
    slog(f'{fGlob=}')
    LOG_ID   = getFileSeqNum(fGlob, fsfx) + n
    slog(f'  {LOG_ID=}')
    name     = f'{baseName}.{LOG_ID}'
    slog(f'    {name=}')
    return  name, LOG_ID

def getFileSeqNum(files, sfx, dbg=0, dbg2=0):
    i    = 0
    fsfx = f'.{sfx}'
    if len(files):
        if dbg2: slog(f'{sfx=} files={fmtl(files)}')
        ids = [ sid(s, fsfx) for s in files if s.endswith(fsfx) and isinstance(sid(s, fsfx), int) ]
        if dbg:  slog(f'ids={fmtl(ids)}')
        i   = max(ids) if ids else 0
    return i

def sid(s, sfx):
    s = s[:-len(sfx)]
    j = s.rfind('.')
    i = s[j + 1:]
    return int(i) if isinstance(i, str) and i.isdigit() else None

########################################################################################################################################################################################################
def main():
    getFileSeqName(BASE_NAME, BASE_PATH)
########################################################################################################################################################################################################
if __name__ == '__main__':
    main()
