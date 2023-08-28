import glob, inspect, os, pathlib, sys

#LOG_ID       = 0
#LOG,  TXT  =     'log' ,     'txt'
#LOGS, TEXT =     'logs',     'text'
#LOG2, TXT2 = f'_.{LOG}', f'_.{TXT}'
ROOT_DIR  = "../test"
PATH      = pathlib.Path.cwd() / sys.argv[0]
BASE_PATH = PATH.parent / ROOT_DIR
BASE_NAME = BASE_PATH.stem
STFILT    = ['self']
W, Y, Z   = ' ', ',', ''
MAX_STACK_DEPTH    = 0
MAX_STACK_FRAME    = inspect.stack()
LOG_FILE, TXT_FILE = None, None
LOG, LOGS = 'log' , 'logs'   ;   LOG2 = f'_.{LOG}'
TXT, TEXT = 'txt', 'text'    ;   TXT2 = f'_.{TXT}'
########################################################################################################################################################################################################
def isi(o, t):  return isinstance(o, t)

def filtText(text):
    text = text.replace('self', Z)
    return text
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
    tf = 0
    if   f == 0:  f = TXT_FILE
    elif f == 1:  f = LOG_FILE
    elif f == 2:  f = LOG_FILE  ;  tf = 1
    print(t, sep=s, end=e, file=f,        flush=bool(ff))
    print(t, sep=s, end=e, file=TXT_FILE, flush=bool(ff)) if tf else None
########################################################################################################################################################################################################
def fmtl(lst, w=None, u=None, d='[', d2=']', s=W, ll=None): # optimize str concat?
    if   lst is None:   return  'None'
    lts = (list, tuple, set, frozenset)  ;  dtn = (int, float)  ;  dts = (str,)
    assert type(lst) in lts,   f'{type(lst)=} {lts=}'
    if d == Z:    d2 = Z
    w   = w   if w else Z   ;   t = []
    zl  = '-'               if ll is not None and ll<0 else '+' if ll is not None and ll>0 else Z
    z   = f'{zl}{len(lst)}' if ll is not None          else Z
    for i, l in enumerate(lst):
        if type(l) in lts:
            if type(w) in lts:               t.append(fmtl(l, w[i], u, d, d2, s, ll))
            else:                            t.append(fmtl(l, w,    u, d, d2, s, ll))
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
def getFilePath(baseName, basePath, fdir=None, fsfx='txt', dbg=1):
    if dbg: slog(f'{baseName =:12} {basePath = }', f=2)
    fileName   = f'{baseName}.{fsfx}'          if fsfx else baseName
    filePath   =    basePath / fdir / fileName if fdir else basePath / fileName
    if dbg: slog(f'{fileName =:12} {filePath = }', f=2)
    return  filePath

def copyFile(src, trg, dbg=1):
    if not src.exists():   msg = f'ERROR Path Does not Exist {src=}'   ;   print(msg)   ;  raise SystemExit(msg)
    if dbg: slog(f'{src=}')
    if dbg: slog(f'{trg=}')
    cmd  =  f'copy {src} {trg}'
    if dbg: slog(f'{cmd} ###')
    os.system(f'{cmd}')

def cleanupOutFiles(file, fp, snp, f):
    slog(f'Copy {file.name} to {snp}',  ff=1, f=f)
    copyFile(    fp,            snp,   dbg=0)
    slog('Flush & Close Txt File',      ff=1, f=f)
    file.flush()     ;     file.close()
########################################################################################################################################################################################################
def getFileSeqName(baseName, basePath, fdir='logs', fsfx='log', n=1):
    slog(f'{fdir=} / {fsfx=}')
    fGlobArg = f'{(basePath / fdir / baseName)}.*.{fsfx}'
    fGlob    = glob.glob(fGlobArg)
    slog(f'{fGlobArg=}')
    logId    = getFileSeqNum(fGlob, fsfx) + n
    slog(f'{logId=}')
    name     = f'{baseName}.{logId}'
    slog(f'{name=}')
    return  name, logId

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
fNameLid, LOG_ID = getFileSeqName(BASE_NAME, BASE_PATH, fdir=LOGS, fsfx=LOG)   ;   slog(f'{LOG_ID=} {fNameLid}')
seqNumLogPath    = getFilePath(fNameLid, BASE_PATH, fdir=LOGS, fsfx=LOG)       ;   slog(f'{seqNumLogPath=}')
seqNumTxtPath    = getFilePath(fNameLid, BASE_PATH, fdir=TEXT, fsfx=TXT)       ;   slog(f'{seqNumTxtPath=}')
LOG_PATH  = getFilePath(BASE_NAME, BASE_PATH, fdir=LOGS, fsfx=LOG,  dbg=0)
LOG_PATH2 = getFilePath(BASE_NAME, BASE_PATH, fdir=LOGS, fsfx=LOG2, dbg=0)
TXT_PATH  = getFilePath(BASE_NAME, BASE_PATH, fdir=TEXT, fsfx=TXT,  dbg=0)
TXT_PATH2 = getFilePath(BASE_NAME, BASE_PATH, fdir=TEXT, fsfx=TXT2, dbg=0)
if LOG_PATH.exists():
    copyFile(LOG_PATH, LOG_PATH2, dbg=0)
if TXT_PATH.exists():
    copyFile(TXT_PATH, TXT_PATH2, dbg=0)
########################################################################################################################################################################################################
def main():
    global LOG_FILE, TXT_FILE
    with open(str(LOG_PATH), 'w', encoding='utf-8') as LOG_FILE, open(str(TXT_PATH), 'w', encoding='utf-8') as TXT_FILE:
        slog(f'     {PATH=}')
        slog(f'{BASE_PATH=}')
        slog(f'{BASE_NAME=}     :     LOG, LOG2, LOGS = {LOG} {LOG2} {LOGS}')
        slog(f' {LOG_PATH=}')
        slog(f'{LOG_PATH2=}')
        slog(f' {TXT_PATH=}')
        slog(f'{TXT_PATH2=}')
        cleanupOutFiles(TXT_FILE, TXT_PATH, seqNumTxtPath, f=2)
        cleanupOutFiles(LOG_FILE, LOG_PATH, seqNumLogPath, f=1)

if __name__ == '__main__':
    main()
