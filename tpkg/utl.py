import glob, inspect, math, os, pathlib, sys
import pyglet.window.key   as pygwink

ROOT_DIR  = "test"
PATH      = pathlib.Path.cwd() / sys.argv[0]
BASE_PATH = PATH.parent / ROOT_DIR
BASE_NAME = BASE_PATH.stem
UNICODE   = 1
F         = f'{0x266D :c}' if UNICODE else 'b' # Flat
N         = f'{0x266E :c}' if UNICODE else '!' # Natural
S         = f'{0x266F :c}' if UNICODE else '#' # Sharp
T         = f'{0x1d11a:c}' # (Treble) Staff
W, Y, Z          = ' ', ',', ''
M, P             = -7, 7
MAX_FREQ_IDX     = 10 * 12 + 1
MAX_STACK_DEPTH  = 0
MAX_STACK_FRAME  = inspect.stack()
CSV_FILE, LOG_FILE, TXT_FILE = None, None, None
INIT      = '###   Init   ###'    * 13
QUIT_BGN  = '###   Quit BGN  ###' * 10
QUIT      = '###   Quit      ###' * 10
QUIT_END  = '###   Quit END  ###' * 10
STFILT = ['log', 'tlog', 'fmtl', 'fmtm', 'dumpGeom', 'resetJ', 'dumpJs', 'dumpImap', 'dumpSmap', 'dumpCursorArrows', '<listcomp>', 'dumpLimap2', 'dumpTniksPfx', 'dumpTniksSfx', 'fmtXYWH', 'kbkInfo', 'dumpCrs', 'fCrsCrt'] # , 'dumpView', 'dumpLbox', 'dumpRect']
########################################################################################################################################################################################################
def init(cfile, lfile, tfile, f):
    global CSV_FILE, LOG_FILE, TXT_FILE   ;   CSV_FILE, LOG_FILE, TXT_FILE = cfile, lfile, tfile
    argv   = sys.argv
    argc   = len(argv)
    slog(f'{argc=} {argv=}', f=f)
    for i in range(1, argc): slog(f'argv[{i}]={argv[i]}', f=f)
    ARGS   = parseCmdLine(argv, f=f)
    global   ROOT_DIR   ;   ROOT_DIR = ARGS['f'][0] if 'f' in ARGS and len(ARGS['f']) > 0 else ROOT_DIR
    slog(f'{     ARGS=}', f=f)
    slog(f'{ ROOT_DIR=}', f=f)
    return   ARGS

def paths():      return BASE_NAME, BASE_PATH, PATH
########################################################################################################################################################################################################
def fri(f):       return int(math.floor(f + 0.5))
def signed(n):    return f' {n}' if n==0 else f'{n:+}'
def ns2signs(ns): return [ '-' if n<0 else '+' if n>0  else W for n in ns ]
def fColor(c, d=1): (d, d2) = ("[", "]") if d else (Z, Z)  ;  return f'{"None":^17}' if c is None else f'{fmtl(c, w=3, d=d, d2=d2):17}'
########################################################################################################################################################################################################
def isAlt(mods):          return mods & pygwink.MOD_ALT
def isCtrl(mods):         return mods & pygwink.MOD_CTRL
def isShift(mods):        return mods & pygwink.MOD_SHIFT
def isCtrlShift(mods):    return mods & pygwink.MOD_CTRL and mods & pygwink.MOD_SHIFT
def isAltShift(mods):     return mods & pygwink.MOD_ALT  and mods & pygwink.MOD_SHIFT
def isCtrlAlt(mods):      return mods & pygwink.MOD_CTRL and mods & pygwink.MOD_ALT
def isCtrlAltShift(mods): return mods & pygwink.MOD_CTRL and mods & pygwink.MOD_ALT and mods & pygwink.MOD_SHIFT
def isNumLock(mods):      return mods & pygwink.MOD_NUMLOCK
def isCapsLock(mods):     return mods & pygwink.MOD_CAPSLOCK
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
    if rev: tmp0 = a[-1 ]   ;   tmp1 = a[:-1]   ;   a = tmp1   ;   a.insert(0, tmp0)
    else:   tmp0 = a[0]     ;   tmp1 = a[1:]    ;   a = tmp1   ;   a.append(tmp0)
    return a
########################################################################################################################################################################################################
def slog(t=Z, p=1, f=1, s=Y, e='\n', ff=0, ft=1):
    if ft: t = filtText(t)
    if p:
        sf   = inspect.currentframe().f_back
        while sf.f_code.co_name in STFILT: sf = sf.f_back # ;  print(f'sf 2: {sf.f_lineno}, {sf.f_code.co_name}')
        fp   = pathlib.Path(sf.f_code.co_filename)
        pl   = 18 if p == 1 else 8
        p    = f'{sf.f_lineno:4} {fp.stem:5} ' if p == 1 else Z
        t    = f'{p}{sf.f_code.co_name:{pl}} ' + t
    tf, so = 0, 0
    if   f == -2: f = LOG_FILE  ;  tf = 1  ;  so = 1
    elif f == -1: f = sys.stdout
    elif f == 0:  f = TXT_FILE
    elif f == 1:  f = LOG_FILE
    elif f == 2:  f = LOG_FILE  ;  tf = 1
    elif f == 3:  f = CSV_FILE
    elif f == 4:  f = LOG_FILE  ;  so = 1
    print(t, sep=s, end=e, file=f,          flush=bool(ff))
    print(t, sep=s, end=e, file=TXT_FILE,   flush=bool(ff)) if tf else None
    print(t, sep=s, end=e, file=sys.stdout, flush=bool(ff)) if so else None

def olog(o=None, p=1, f=1, s=Y, e='\n', ff=1):
    o = s.join(str(o)) if o is not None else ''
    if p:
        sf   = inspect.currentframe().f_back
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
    text = text.replace('util', Z)
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
def isi(o, t):  return isinstance(o, t)
########################################################################################################################################################################################################
def fmtl(lst, w=None, u=None, d='[', d2=']', s=W, ll=None): # optimize str concat?
    if   lst is None:   return  'None'
    lts = (list, tuple, set, frozenset, zip)  ;  dtn = (int, float)  ;  dts = (str,)
    assert type(lst) in lts,   f'{type(lst)=} {lts=}'
    if d == Z:     d2 = Z
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
            if   isi(l, type):            l =  str(l)
            elif l is None:               l =  'None'
            if   isi(w, lts):             t.append(f'{l:{u}{w[i]}}{ss}')
            elif isi(l, dtn):             t.append(f'{l:{u}{w   }}{ss}')
            elif isi(l, dts):             t.append(f'{l:{u}{w   }}{ss}')
            else:                         t.append(f'{l}{ss}')
    return z + d + Z.join(t) + d2
########################################################################################################################################################################################################
def fmtm(m, w=None, wv=None, u=None, uv=None, d0=':', d='[', d2=']', s=W, ll=None):
    w  = w  if w  is not None else Z   ;  t = []
    wv = wv if wv is not None else w
    if d==Z:   d2 = Z
    u  = Z if u  is None else u
    uv = Z if uv is None else uv
    for i, (k, v) in enumerate(m.items()):
        ss = s if i < len(m) - 1 else Z
        if   type(v) in (list, tuple, set):  t.append(f'{d}{k:{u}{w}}{d0}{fmtl(v, wv, ll=k if ll==-1 else ll)}{d2}{ss}')
        elif type(v) in (int, str):          t.append(f'{d}{k:{u}{w}}{d0}{v:{uv}{wv}}{d2}{ss}')
    return Z.join(t)
########################################################################################################################################################################################################
def fmtf(a, b):
    if b==4: return f'{a:4.2f}' if a < 10 else f'{a:4.1f}' if a < 100 else f'{a:4.0f}'
    if b==5: return f'{a:5.3f}' if a < 10 else f'{a:5.2f}' if a < 100 else f'{a:5.1f}' if a < 1000 else f'{a:5.0f}'
########################################################################################################################################################################################################
def parseCmdLine(argv, dbg=1, f=0):
    options, key, vals, argc = {}, Z, [], len(argv)
    if dbg: slog(f'argv={fmtl(argv[1:])}', p=0, f=f)  ;  slog(argv[0], p=0, f=f)
    for j in range(1, argc):
        arg = argv[j]
        if len(arg) > 2 and arg[0] == '-' and arg[1] == '-':
            if argv[2].isalpha():
                vals = []
                key = arg[2:]
                options[key] = vals
                if dbg: slog(f'{j:2} long    {arg:2} {key} {fmtl(vals)}', f=f, e=W)
            else:
                slog(  f'{j:2} ERROR long    {arg:2} {key} {fmtl(vals)}', f=f, e=W)
        elif len(arg) > 1 and arg[0] == '-':
            if arg[1].isalpha() or arg[1] == '?':
                vals = []
                if len(arg) == 2:
                    key = arg[1:]
                    if dbg: slog(f'{j:2} short   {arg:2} {key} {fmtl(vals)}', p=0, f=f, e=W)
                    options[key] = vals
                elif len(arg) > 2:
                    for i in range(1, len(arg)):
                        key = arg[i]
                        if dbg: slog(f'{j:2} short   {arg:2} {key} {fmtl(vals)}', f=f, e=W)
                        options[key] = vals
            elif arg[1].isdigit():
                vals.append(arg)
                options[key] = vals
                if dbg: slog(f'{j:2} neg arg {arg:2} {key} {fmtl(vals)}', f=f, e=W)
            else:
                vals.append(arg)
                options[key] = vals
                if dbg: slog(f'{j:2} ??? arg {arg:2} {key} {fmtl(vals)}', f=f, e=W)
        else:
            vals.append(arg)
            options[key] = vals
            if dbg: slog(f'{j:2} arg     {arg:2} {key} {fmtl(vals)}', p=0, f=f, e=W)
        if dbg: slog(p=0, f=f)
    if dbg: slog(f'options={fmtm(options)}', f=f)
    return options
########################################################################################################################################################################################################
def getFilePath(baseName, basePath, fdir=None, fsfx='txt', dbg=1, f=-2):
    if dbg: slog(f'{baseName =:12} {basePath = }', f=f)
    fileName   = f'{baseName}.{fsfx}'          if fsfx else baseName
    filePath   =    basePath / fdir / fileName if fdir else basePath / fileName
    if dbg: slog(f'{fileName =:12} {filePath = }', f=f)
    return  filePath

def copyFile(src, trg, dbg=1, f=-2):
    if not src.exists():   msg = f'ERROR Path Does not Exist {src=}'   ;   print(msg)   ;  raise SystemExit(msg)
    if dbg: slog(f'{src=}', f=f)
    if dbg: slog(f'{trg=}', f=f)
    cmd  =  f'copy {src} {trg}'
    if dbg: slog(f'{cmd} ###', f=f)
    os.system(f'{cmd}')

def getFileSeqName(baseName, basePath, fdir='logs', fsfx='log'):
    n = 1
    slog(f'{fdir=} / {fsfx=}')
    fGlobArg = f'{(basePath / fdir / baseName)}.*.{fsfx}'
    fGlob    = glob.glob(fGlobArg)
    slog(f'{fGlobArg=}')
    LOG_ID   = getFileSeqNum(fGlob, fsfx) + n
    slog(f'{LOG_ID=}')
    name     = f'{baseName}.{LOG_ID}'
    slog(f'{name=}')
    return  name, LOG_ID

def getFileSeqNum(files, sfx, dbg=0, dbg2=0):
    i    = 0
    fsfx = f'.{sfx}'
    if len(files):
        if dbg2: slog(f'{sfx=} files={fmtl(files)}')
        ids = [sid(s, fsfx) for s in files if s.endswith(fsfx) and isinstance(sid(s, fsfx), int)]
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
