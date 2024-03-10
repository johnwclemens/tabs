from tpkg import utl
from tpkg import unic
#from tpkg import strngs
import math

F, N, S       = unic.F,     unic.N,    unic.S
W, Y, Z       = utl.W,      utl.Y,     utl.Z
slog, ist     = utl.slog,   utl.ist
fmtf, fmtg    = utl.fmtf,   utl.fmtg
fmtl, fmtm    = utl.fmtl,   utl.fmtm
signed, filtA = utl.signed, utl.filtA
ns2signs      = utl.ns2signs

MAX_FREQ_IDX  = utl.MAX_FREQ_IDX
ACCD_TONES    = ['b', '#', '♭', '♮', '♯']
CM_P_M        = 100 # cm per m, cemtimeters per meter
V_SOUND       = 345 # m/s in dry air @ about 73 deg F
A4_INDEX      = 57
SUPERS        = utl.SPRSCRPT_INTS

def dumpData(csv=0):
    slog(f'BGN {csv=}')
    dumpTestA(  csv)
    dumpNF(     csv)
    dumpTestB(  csv)
    dumpND(     csv)
    dmpOTS(       rf=440, sss=V_SOUND, csv=csv)
    dmpPyth(k=51, rf=440, sss=V_SOUND, csv=csv) # Eb
    dmpPyth(k=58, rf=440, sss=V_SOUND, csv=csv) # Bb 
    dmpPyth(k=53, rf=440, sss=V_SOUND, csv=csv) # F
    dmpPyth(k=60, rf=440, sss=V_SOUND, csv=csv) # C
    dmpPyth(k=55, rf=440, sss=V_SOUND, csv=csv) # G
    dmpPyth(k=50, rf=440, sss=V_SOUND, csv=csv) # D
#    dmpPyth(k=62, rf=440, sss=V_SOUND, csv=csv) # D octave
    dmpPyth(k=57, rf=440, sss=V_SOUND, csv=csv) # A
    dmpPyth(k=52, rf=440, sss=V_SOUND, csv=csv) # E
    dmpPyth(k=59, rf=440, sss=V_SOUND, csv=csv) # B
    dmpPyth(k=54, rf=440, sss=V_SOUND, csv=csv) # F#/Gb
    dmpPyth(k=61, rf=440, sss=V_SOUND, csv=csv) # C#/Db
    dmpPyth(k=56, rf=440, sss=V_SOUND, csv=csv) # G#/Ab
    dmpPythMap1(1, csv)
    dmpPythMap1(2, csv)
    dmpPythMap1(3, csv)
    dmpPythMap1(4, csv)
    dmpPythMap1(5, csv)
    if not csv:  testStacks()
#    fPyth(7, 6, csv)
    dmpPythMap2(  csv)
#    dmpPyth(k=50, rf=440, ss=V_SOUND, csv=csv) # D
#    dmpPyth(k=62, rf=440, ss=V_SOUND, csv=csv) # D octave
    slog(f'END {csv=}')
########################################################################################################################################################################################################
def dumpTestA(csv=0):
    w, d, m, n, f = (0, Z, Y, Y, 3) if csv else (2, '[', W, Z, 1)   ;   p = 0   ;   v = 21
    x = f'{w}x'  ;  u = f'>{w}'  ;  y = f'<{w}x'  ;  z = f'<{w}'    ;   q = f'>{w}x'
    slog('BGN')  ;  w = 0 if csv else '^7'
    slog(f'    {m}{fmtl(list(range(v)), w=w,       d=d, s=m)}', p=p, f=f)
    slog(f'ACCD{m}{fmtl([F, N, S], w=w, d=d, s=m)}',            p=p, f=f)
    slog(f' F2S{m}{fmtm(Notes.F2S,      w=w,       d=d, s=m)}', p=p, f=f)   ;   w = 0 if csv else 2
    slog(f' F4S{m}{fmtm(Notes.F4S,      w=u, wv=z, d=d, s=m)}', p=p, f=f)
    slog(f' S2F{m}{fmtm(Notes.S2F,      w=w,       d=d, s=m)}', p=p, f=f)
    slog(f' S4F{m}{fmtm(Notes.S4F,      w=u, wv=z, d=d, s=m)}', p=p, f=f)
    slog(f' I2F{m}{fmtm(Notes.I2F,      w=x, wv=w, d=d, s=m)}', p=p, f=f)
    slog(f' I4F{m}{fmtm(Notes.I4F,      w=x, wv=w, d=d, s=m)}', p=p, f=f)
    slog(f' I2S{m}{fmtm(Notes.I2S,      w=x, wv=w, d=d, s=m)}', p=p, f=f)
    slog(f' I4S{m}{fmtm(Notes.I4S,      w=x, wv=w, d=d, s=m)}', p=p, f=f)
    slog(f' N2I{m}{fmtm(Notes.N2I,      w=u, wv=y, d=d, s=m)}', p=p, f=f)
    slog(f'I2NF{m}{fmtm(Notes.i2n(1),   w=q, wv=z, d=d, s=m)}', p=p, f=f)
    slog(f'I4NF{m}{fmtm(Notes.i4n(1),   w=q, wv=z, d=d, s=m)}', p=p, f=f)
    slog(f'I2NS{m}{fmtm(Notes.i2n(-1),  w=q, wv=z, d=d, s=m)}', p=p, f=f)
    slog(f'I4NS{m}{fmtm(Notes.i4n(-1),  w=q, wv=z, d=d, s=m)}', p=p, f=f)
    slog(f' I2V{m}{fmtm(Notes.I2V,      w=x, wv=w, d=d, s=m)}', p=p, f=f)
    slog(f' I4V{m}{fmtm(Notes.I4V,      w=x, wv=w, d=d, s=m)}', p=p, f=f)
    slog(f' I6V{m}{fmtm(Notes.I6V,      w=x, wv=w, d=d, s=m)}', p=p, f=f)
    slog(f' V2I{m}{fmtm(Notes.V2I,      w=u, wv=y, d=d, s=m)}', p=p, f=f)
    slog('END')

def dumpTestB(csv=0):
    w, d, m, n, file = (0, Z, Y, Y, 3) if csv else ('^5', '[', W, Z, 1)
    t   = Notes.NTONES  ;    s = Notes.SHRP  ;    f = Notes.FLAT  ;  is1 = Notes.IS1  ;  is2 = Notes.IS2  ;  i2v = Notes.I2V  ;    v = 21
    i2n = Notes.i2n     ;  f2s = Notes.F2S   ;  s2f = Notes.S2F   ;  i2f = Notes.I2F  ;  i2s = Notes.I2S  ;  i4v = Notes.I4V  ;  n2i = Notes.N2I
    i4n = Notes.i4n     ;  f4s = Notes.F4S   ;  s4f = Notes.S4F   ;  i4f = Notes.I4F  ;  i4s = Notes.I4S  ;  i6v = Notes.I6V  ;  v2i = Notes.V2I
    slog('BGN')         ;    o = t + 1       ;    p = 0
    slog(f'    {m}{fmtl( list(range(v)), w=w, d=d, s=m)}',    p=p, f=file)
    slog(f'ACCD{m}{fmtl([F, N, S], w=w, d=d, s=m)}',          p=p, f=file)
    slog(f' F2S{m}{fmtl([ f"{i2n(f)[k]}:{f2s[i2n(f)[k]]}" if k in is1 else W for k in range(t) ], w=w, d=d, s=m)}', p=p, f=file)
    slog(f' F4S{m}{fmtl([ f"{i4n(f)[k]}:{f4s[i4n(f)[k]]}" if k in is2 else W for k in range(o) ], w=w, d=d, s=m)}', p=p, f=file)
    slog(f' S2F{m}{fmtl([ f"{i2n(s)[k]}:{s2f[i2n(s)[k]]}" if k in is1 else W for k in range(t) ], w=w, d=d, s=m)}', p=p, f=file)
    slog(f' S4F{m}{fmtl([ f"{i4n(s)[k]}:{s4f[i4n(s)[k]]}" if k in is2 else W for k in range(o) ], w=w, d=d, s=m)}', p=p, f=file)
    slog(f' I2F{m}{fmtl([ f"{k}:{i2f[k]}"                                    for k in range(t) ], w=w, d=d, s=m)}', p=p, f=file)
    slog(f' I4F{m}{fmtl([ f"{k}:{i4f[k]}"                                    for k in range(t) ], w=w, d=d, s=m)}', p=p, f=file)
    slog(f' I2S{m}{fmtl([ f"{k}:{i2s[k]}"                                    for k in range(t) ], w=w, d=d, s=m)}', p=p, f=file)
    slog(f' I4S{m}{fmtl([ f"{k}:{i4s[k]}"                                    for k in range(t) ], w=w, d=d, s=m)}', p=p, f=file)
    slog(f' N2I{m}{fmtl([ f"{k}:{v}"                                    for k,v in n2i.items() ], w=w, d=d, s=m)}', p=p, f=file)
    slog(f'I2NF{m}{fmtl([ f"{k}:{i2n(f)[k]}"                                 for k in range(t) ], w=w, d=d, s=m)}', p=p, f=file)
    slog(f'I4NF{m}{fmtl([ f"{k}:{i4n(f)[k]}"                                 for k in range(t) ], w=w, d=d, s=m)}', p=p, f=file)
    slog(f'I2NS{m}{fmtl([ f"{k}:{i2n(s)[k]}"                                 for k in range(t) ], w=w, d=d, s=m)}', p=p, f=file)
    slog(f'I4NS{m}{fmtl([ f"{k}:{i4n(s)[k]}"                                 for k in range(t) ], w=w, d=d, s=m)}', p=p, f=file)
    slog(f' I2V{m}{fmtl([ f"{k}:{v}"                                    for k,v in i2v.items() ], w=w, d=d, s=m)}', p=p, f=file)
    slog(f' I4V{m}{fmtl([ f"{k}:{v}"                                    for k,v in i4v.items() ], w=w, d=d, s=m)}', p=p, f=file)
    slog(f' I6V{m}{fmtl([ f"{k}:{v}"                                    for k,v in i6v.items() ], w=w, d=d, s=m)}', p=p, f=file)
    slog(f' V2I{m}{fmtl([ f"{k}:{v}"                                    for k,v in v2i.items() ], w=w, d=d, s=m)}', p=p, f=file)
    slog('END')
########################################################################################################################################################################################################
class Notes(object):#1       2       3       4       5       6       7       8       9        a        b           0       #[  2    7 9  ]#
    I2F = { 0:'C' , 1:'D♭', 2:'D' , 3:'E♭', 4:'E' , 5:'F' , 6:'G♭', 7:'G' , 8:'A♭', 9:'A' , 10:'B♭', 11:'B' } # ,12:'C' } # 8/12/16 
    I2S = { 0:'C' , 1:'C♯', 2:'D' , 3:'D♯', 4:'E' , 5:'F' , 6:'F♯', 7:'G' , 8:'G♯', 9:'A' , 10:'A♯', 11:'B' } # ,12:'C' } # 8/12/16
    I4F = { 0:'C' , 1:'D♭', 2:'D' , 3:'E♭', 4:'F♭', 5:'F' , 6:'G♭', 7:'G' , 8:'A♭', 9:'A' , 10:'B♭', 11:'C♭'} # ,12:'C' } # 8/12/16 C♭ F♭
    I4S = { 0:'B♯', 1:'C♯', 2:'D' , 3:'D♯', 4:'E' , 5:'E♯', 6:'F♯', 7:'G' , 8:'G♯', 9:'A' , 10:'A♯', 11:'B' } # ,12:'C' } # 8/12/16 B♯ E♯
    I2V = { 0:'R' , 1:'♭2', 2:'2' , 3:'m3', 4:'M3', 5:'4' , 6:'♭5', 7:'5' , 8:'♯5', 9:'6' , 10:'♭7', 11:'7' } # ,12:'R' } # 8/12/16 ♭5 ♯5
    I4V = { 0:'P1', 1:'m2', 2:'M2', 3:'m3', 4:'M3', 5:'P4', 6:'TT', 7:'P5', 8:'m6', 9:'M6', 10:'m7', 11:'M7'} # ,12:'P8'} # 8/12/16 TT m6
    I6V = { 0:'d2', 1:'A1', 2:'d3', 3:'A2', 4:'d4', 5:'A3', 6:'A4', 7:'d6', 8:'A5', 9:'d7', 10:'A6', 11:'d8'} # ,13:'A7'} # 8/12/16 TT d2 A1 
    V2I = { 'R':0 , '♭2':1, '2':2 , 'm3':3, 'M3':4, '4' :5, '♭5':6, '5':7 , '♯5':8, '6' :9, '♭7':10, '7' :11} # ,'R`':12} # 8/12/16 ♭5 ♯5
    N2I = {'B♯':0 , 'C' :0,'C♯':1 , 'D♭':1, 'D' :2, 'D♯':3, 'E♭':3, 'E':4 , 'F♭':4, 'E♯':5, 'F' :5,  'F♯':6, 'G♭':6, 'G' :7, 'G♯':8, 'A♭':8, 'A' :9, 'A♯':10, 'B♭':10, 'B' :11, 'C♭' :11, 'B♯`':12, 'C`':12 } #21 B# C♭ E# F♭
    F2S = {            'D♭':'C♯', 'E♭':'D♯',                       'G♭':'F♯', 'A♭':'G♯', 'B♭':'A♯'           } #[ 1 3  6 8 a ]# 5/9 D♭->C♯
    S2F = {            'C♯':'D♭', 'D♯':'E♭',                       'F♯':'G♭', 'G♯':'A♭', 'A♯':'B♭'           } #[ 1 3  6 8 a ]# 5/9 C♯->D♭
#               0          1          2          3         4           5          6          7         8
    F4S = { 'C' :'B♯',                       'F♭':'E' , 'F' :'E♯',                                 'C♭':'B'  } #,'C' :'B♯' } #[0   45     b]# 4/9
    S4F = { 'B♯':'C' ,                       'E' :'F♭', 'E♯':'F' ,                                 'B' :'C♭' } #,'B#':'C'  } #[0   45     b]# 4/9
    IS0,  IS1,  IS2    = [2, 7, 9], [1, 3, 6, 8, 10], [0, 4, 5, 11]
    FLAT, NTRL, SHRP   =  -1,   0,   1  # -1 ~= 2
    TYPES              = [ 'NTRL', 'SHRP', 'FLAT' ] # 0=NTRL, 1=SHRP, 2=FLAT=-1
    TYPE               = SHRP
    NTONES             = len(V2I)
    
    @classmethod
    def i2n(cls, t=None):           return cls.I2S if t is None or t==cls.SHRP or t==cls.NTRL else cls.I2F
    @classmethod
    def i4n(cls, t=None):           return cls.I4S if t is None or t==cls.SHRP or t==cls.NTRL else cls.I4F
    @classmethod
    def n2i(cls, n, o=0):           n = n[:-1] if o else n   ;   assert n in cls.N2I,  f'{n=} {cls.N2I=}'     ;   return cls.N2I[n]
    @classmethod
    def n2ai(cls, m):               n = m[:-1].strip()       ;   assert n in cls.N2I,  f'{n=} {cls.N2I=}'     ;   return cls.n2ipo(filtA(m))
    @classmethod
    def n2ipo(cls, n):              o = int(n[-1]) * cls.NTONES   ;   n = n[:-1]   ;   return cls.N2I[n] + o 
    @classmethod
    def nextName(cls, n, iv, o=0):  i = cls.n2i(n, o)   ;   j = cls.V2I[iv]   ;   k = cls.nextIndex(i, j)   ;   return cls.name(k, 0)
    @classmethod
    def nextIndex(cls, i, d=1):     return (i+d) % cls.NTONES
    @classmethod
    def name(cls, i, t=None, n2=1):
        j = i % cls.NTONES   ;   t = 2 if t==-1 else t
#       t =     cls.TYPE if t is None else t
        t = t        if t is not None else cls.TYPE
        assert     t      is not None and  ist(t, int),     f'{t=} {type(t)=}'
        assert  cls.i2n() is not None and  t in cls.i2n(),  f'{t=} {cls.i2n()=}'
        assert  cls.i2n()[t] is not None,                   f'{t=} {cls.i2n()[t]=}'
        return  cls.i2n(t)[j]  if n2  else cls.i4n(t)[j]
########################################################################################################################################################################################################
def updNotes(i, m, n, t, d=0):
    if   t  ==  Notes.FLAT:    Notes.I2F[i] = m
    elif t  ==  Notes.SHRP:    Notes.I2S[i] = n
    if   d:
        if m in Notes.S2F: del Notes.S2F[m]
        if n in Notes.F2S: del Notes.F2S[n]
    else:
        Notes.F2S[n] = m   ;   Notes.S2F[m] = n
########################################################################################################################################################################################################
def initND():    return { i: [ Notes.I2F[i], Notes.I2S[i], Notes.I2V[i], Notes.I4V[i], Notes.I6V[i] ] for i in range(Notes.NTONES) }

def dumpND(csv=0):
    slog('BGN')
    w, d, m, f = (0, Z, Y, 3) if csv else (2, '[', W, 1)
    hdrs       = ['I', '♭', '♯', 'IV', 'mM', 'dA']
    hdrs       = f'{m.join([ f"{h:{w}}" for h in hdrs ])}'
    slog(f'{hdrs}', p=0, f=f)
    for i, (k, v) in enumerate(ND.items()):
        slog(f'{i:x}{m}{fmtl(v, w=w, d=d, s=m)}', p=0, f=f)
#    for i in range(len(ND)):   slog(f'{i:x}{m}{fmtl(ND[i], w=w, d=d, s=m)}', p=0, f=f)
    slog('END')

ND = initND()
########################################################################################################################################################################################################
FLATS  = [ f'{v}{n}' for n in range(Notes.NTONES - 1) for v in Notes.I2F.values() ][:MAX_FREQ_IDX]
SHRPS  = [ f'{v}{n}' for n in range(Notes.NTONES - 1) for v in Notes.I2S.values() ][:MAX_FREQ_IDX]
#FLATS = [ f'{v}{n}' for n in range(Notes.NTONES - 1) for v in Notes.I4F.values() ][:MAX_FREQ_IDX]
#SHRPS = [ f'{v}{n}' for n in range(Notes.NTONES - 1) for v in Notes.I4S.values() ][:MAX_FREQ_IDX]
########################################################################################################################################################################################################
def dumpNF(csv=0):
    slog('BGN 12 Tone Equal Tempored (Hz, cm)')
    w, m, s, f = (Z, Y, Y, 3) if csv else ('^5', W, Z, 1)
    nm = MAX_FREQ_IDX      ;    p, q = -8, 88+1   ;   g, h = 0, nm
    pfxp, pfxi, pfxf, pfxs =   'Piano[',  'Index[',  'Flats[',  'Shrps['
    sfxp, sfxi, sfxf, sfxs = '] Piano', '] Index', '] Flats', '] Shrps'
    slog(f'{pfxp}{s}{fmtl(list(range(p, q)), w=w, s=m, d=Z)}{s}{sfxp}', p=0, f=f)
    slog(f'{pfxi}{s}{fmtl(list(range(g, h)), w=w, s=m, d=Z)}{s}{sfxi}', p=0, f=f)
    dumpFreqs(432, csv=csv)    ;    dumpFreqs(440, csv=csv)
    dmpWaveLs(432, csv=csv)    ;    dmpWaveLs(440, csv=csv)
    slog(f'{pfxf}{s}{fmtl(list(FLATS),       w=w, s=m, d=Z)}{s}{sfxf}', p=0, f=f)
    slog(f'{pfxs}{s}{fmtl(list(SHRPS),       w=w, s=m, d=Z)}{s}{sfxs}', p=0, f=f)
    slog('END 12 Tone Equal Tempored (Hz, cm)')

def dumpFreqs(rf=440, csv=0):
    m, s, f = (Y, Y, 3) if csv else (W, Z, 1)
    freqs = F440s if rf == 440 else F432s   ;   ref = f'F{rf}A'   ;   fs = []
    for freq in freqs:
        ft = fmtf(freq, 5)
        fs.append(f'{ft}')
    fs = m.join(fs)   ;   pfx = f'{ref}['   ;   sfx = f'] {ref} Hz'
    slog(f'{pfx}{s}{fs}{s}{sfx}', p=0, f=f)

def dmpWaveLs(rf=440, sss=V_SOUND, csv=0):
    m, s, f = (Y, Y, 3) if csv else (W, Z, 1)
    freqs = F440s if rf == 440 else F432s   ;    ref = f'W{rf}A'   ;   ws = []
    for freq in freqs:
        w = CM_P_M * sss/freq
        wt = fmtf(w, 5)
        ws.append(f'{wt}')
    ws = m.join(ws)   ;   pfx = f'{ref}['   ;   sfx = f'] {ref} cm'
    slog(f'{pfx}{s}{ws}{s}{sfx}', p=0, f=f)
########################################################################################################################################################################################################
def dmpOTS(rf=440, sss=V_SOUND, csv=0):
    slog(f'BGN Overtone Series ({rf=} {sss=} {csv=})')
    (ww, d, mm, nn, ff) = (Z, Z, Y, Y, 3) if csv else ('^6', '[', W, Z, 1)
    rs    = F440s      if rf == 440 else F432s        ;   cs, ns, fs, ws = [], [], [], []
    freqs = F440s[:32] if rf == 440 else F432s[:32]   ;   ref = '440A' if rf == 440 else '432A'
    f0    = F440s[0]    ;   w0 = CM_P_M * sss/f0
    for i, freq in enumerate(freqs):
        i += 1          ;    f  = fOTS(i, rf)    ;    w  = w0 / i
        n, n2  = f2nPair(f, b=0 if i in (17, 22, 25, 28) else 1) 
        j  = Notes.n2ai(n)
        assert 0 <= j < len(rs),  f'{j=} {len(rs)=}'
        f2 = rs[j]      ;    c  = r2cents(f/f2)
        fs.append(fmtf(f, 6))    ;    ns.append(n)    ;    ws.append(fmtf(w, 6))
        cs.append(fmtg(c, 6 if c >= 0 else 5))
    fs   = mm.join(fs)  ;   ws = mm.join(ws)   ;   ns = fmtl(ns, w=ww, s=mm, d=Z)   ;   cs = fmtl(cs, w=ww, s=mm, d=Z)
    ref += mm if csv else ' ['    ;    sfxf = Z if csv else '] Hz'    ;    sfxw = Z if csv else '] cm'
    pfxn = 'note ['     ;   pfxc = 'cents['   ;   sfx = Z if csv else ']'
    slog(f'Index{nn}{fmtl(list(range(1, 33)), w=ww, d=d, s=mm)}', p=0, f=ff)
    slog(f'{ref}{fs}{sfxf}', p=0, f=ff)
    slog(f'{pfxn}{ns}{sfx}', p=0, f=ff)
    slog(f'{pfxc}{cs}{sfx}', p=0, f=ff)
    slog(f'{ref}{ws}{sfxw}', p=0, f=ff)
    slog(f'END Overtone Series ({rf=} {sss=} {csv=})')
########################################################################################################################################################################################################
def f440(i):         return float(440 * (2 ** (1/Notes.NTONES)) ** (i - A4_INDEX))
def f432(i):         return float(432 * (2 ** (1/Notes.NTONES)) ** (i - A4_INDEX))
def fOTS(i, r=440):  f0 = F440s[0] if r == 440 else F432s[0]  ;   return f0 * i
def Piano(c, d=1):   (d, d2) = ("[", "]") if d else (Z, Z)    ;   return f'{utl.NONE:^17}' if c is None else f'{fmtl(c, w=3, d=d, d2=d2):17}'

F440s  = [ f440(i)  for i in range(MAX_FREQ_IDX) ]
F432s  = [ f432(i)  for i in range(MAX_FREQ_IDX) ]
FOTSs  = [ fOTS(i)  for i in range(1, 33) ]
########################################################################################################################################################################################################
PythMap1 = {} # note index to freq ratio
PythMap2 = {} # freq ratio in cents to count
########################################################################################################################################################################################################
def r2cents(r):      return Notes.NTONES * 100 * math.log2(r)

def stck5ths(n):     return [ stackI(3, 2, i) for i in range(1, n+1) ]
def stck4ths(n):     return [ stackI(2, 3, i) for i in range(1, n+1) ]
def stackI(a, b, c): return [ a, b, c ]
########################################################################################################################################################################################################
def testStacks(n=100):
    i5s, f5s = test5ths(n, -1)  ;   w = '10.5f'
    i4s, f4s = test4ths(n, -1)
    for i, k in enumerate(i5s.keys()):
        if k in i4s and i4s[k][0] > 0:
            slog(  f'{i+1:3} of {n:4} 5ths={k:4} {i5s[k][0]} {fmtl(i5s[k][1], w=w)} also in 4ths={i4s[k][0]} {fmtl(i4s[k][1], w=w)}')
        else: slog(f'{i+1:3} of {n:4} 5ths={k:4} {i5s[k][0]} {fmtl(i5s[k][1], w=w)}')
    for i, k in enumerate(i4s.keys()):
        if k in i5s and i5s[k][0] > 0:
            slog(  f'{i+1:3} of {n:4} 4ths={k:4} {i4s[k][0]} {fmtl(i4s[k][1], w=w)} also in 5ths={i5s[k][0]} {fmtl(i5s[k][1], w=w)}')
        else: slog(f'{i+1:3} of {n:4} 4ths={k:4} {i4s[k][0]} {fmtl(i4s[k][1], w=w)}')

def test5ths(n, i, dbg=0):
    mi, mf = {}, {}   ;   w = '10.5f'
    for m in range(1, n+1):
        s5s       = stck5ths(m)
        a, b, c   = s5s[i]
        r, ca, cb = abc2r(a, b, c)
        pa, pb    = a**ca, b**cb   ;   p = pa/pb
        cents     = r2cents(p)
        kf, ki    = cents, int(round(cents))
        if ki in mi:      slog(f'{ki=:4} {mi[ki][0]=} {fmtl(mi[ki][1], w=w)=} {kf=:{w}}')
        if ki not in mi:  mi[ki] = [1, [kf]] 
        else:             mi[ki][0] += 1   ;   mi[ki][1].append(kf)
        mf[kf]    = 1 if kf not in mf else mf[kf] + 1
        if dbg: slog(f'{m} {fmtl(s5s)}', p=0)
        if dbg: slog(f'abc = {m} 5ths = [{i}] = {fmtl(s5s[i])} {ca=} {cb=} {r=} {cents:4.0f} cents', p=0)
    ks = list(mi.keys())                     ;   slog(f'5ths {fmtl(ks, w=4)}', p=0)
    ks = sorted(ks, key= lambda x: int(x))   ;   slog(f'sort {fmtl(ks, w=4)}', p=0)
    return mi, mf

def test4ths(n, i, dbg=0):
    mi, mf = {}, {}   ;   w = '10.5f'
    for m in range(1, n+1):
        s4s       = stck4ths(m)
        a, b, c   = s4s[i]
        r, ca, cb = abc2r(a, b, c)
        pa, pb    = a**ca, b**cb   ;   p = pa/pb
        cents     = r2cents(p)
        kf, ki    = cents, int(round(cents))
        if ki in mi:      slog(f'{ki=:4} {mi[ki][0]=} {fmtl(mi[ki][1], w=w)=} {kf=:{w}}')
        if ki not in mi:  mi[ki] = [1, [kf]] 
        else:             mi[ki][0] += 1   ;   mi[ki][1].append(kf)
        mf[kf]    = 1 if kf not in mf else mf[kf] + 1
        if dbg: slog(f'{m} {fmtl(s4s)}', p=0)
        if dbg: slog(f'abc = {m} 4ths = [{i}] = {fmtl(s4s[i])} {ca=} {cb=} {r=} {cents:4.0f} cents', p=0)
    ks = list(mi.keys())                     ;   slog(f'4ths {fmtl(ks, w=4)}', p=0)
    ks = sorted(ks, key= lambda x: int(x))   ;   slog(f'sort {fmtl(ks, w=4)}', p=0)
    return mi, mf
########################################################################################################################################################################################################
def pythEpsln(dbg=0): # 3**13 / 2**20 = 3¹³/2²⁰ = 1594323 / 1048576 = 1.5204648971557617 ## 1.0011298906275259 0.0016291673878230113
    ccents = pythComma()
    ecents = ccents / Notes.NTONES
    if dbg:  slog(f'Epsilon = Comma / 12 = {ccents:10.5f} / 12 = {ecents:10.5f} cents')
    return ecents
    
def pythComma(dbg=0): # 3**12 / 2**19 = 3¹²/2¹⁹ = 531441 / 524288 = 1.0136432647705078, log2(1.0136432647705078) = 0.019550008653874178, 1200 * log2() = 23.460010384649014
    n, i, iv  = 12, -1, '5'
    s5s       = stck5ths(n)
    a, b, c   = s5s[i]
    r, ca, cb = abc2r(a, b, c)
    if dbg:   slog(f'{n} 5ths, s5s     = {fmtl(s5s)}')
    if dbg:   slog(f'{n} 5ths, s5s[{i}] = {fmtl(s5s[i])} {ca=} {cb=} {r=:10.8}')
    assert [a, b, c] == [3, 2, n],  f'{a=} {b=} {c=} {[3, 2, n]}'
    pa, pb    = a ** ca, b ** cb
    cratio    = pa / pb
    q         = f'{a}{i2spr(ca)}/{b}{i2spr(cb)}'
    ccents    = r2cents(cratio)
    if dbg:   slog(f'Comma = {pa:6}/{pb:<6} = {a}**{ca}/{b}**{cb} = {q:6} = {cratio:10.8f} = {ccents:10.5f} cents')
    ecents    = ccents / 12
    if dbg:   slog(f'Epsilon = Comma / 12 = {ccents:10.5f} / 12 = {ecents:10.5f} cents')
    return ccents
########################################################################################################################################################################################################
def abc2r(a, b, c):
    pa0, pb0 = a ** c, b ** c
    r0       = pa0 / pb0
    j        = foldF(r0)
    ca       = c + j if j > 0 else c #  ;   aa = [ a for _ in range(ca) ]
    cb       = c - j if j < 0 else c #  ;   bb = [ b for _ in range(cb) ]
    pa, pb   = a ** ca, b ** cb
    r        = pa / pb   ;   assert r == r0 * (2 ** j),  f'{r=} {r0=} {j=}'
    return r, ca, cb

def i2spr(i):
    if i < 0: return '-' + Z.join(SUPERS[int(digit)] for digit in str(i))
    else:     return       Z.join(SUPERS[int(digit)] for digit in str(i))
        
def foldF(n):
    i = 0
    if n > 1:
        while n > 2:
            n /= 2  ;  i -= 1
    elif n < 1:
        while n < 1:
            n *= 2  ;  i += 1
    return i
########################################################################################################################################################################################################
def fPyth(a=7, b=6, csv=0):
    m, n, o, f = (Y, Y, Y, 3) if csv else (W, Z, '|', 1)   ;   d, e = '[', ']'   ;   w = f'^13'
    abc1 = stck5ths(a)
    abc2 = stck4ths(b)
    abc3 = [ stackI(3, 2, 0) ]   ;   abc3.extend(abc1)   ;   abc3.extend(abc2)   ;   abc3.append(stackI(2, 1, 1))
    abc4 = sorted(abc3, key= lambda x: abc2r(x[0], x[1], x[2])[0])    ;   tmp1, tmp2, tmp3, tmp4 = [], [], [], []
    abcR = list(abc4)
    l1, l2, l3, l4 = len(abc1), len(abc2), len(abc3), len(abc4)
    for abc in abc1: s = W.join([str(_) for _ in abc])   ;   t = f'{s:{w}}'   ;   tmp1.append(t)
    for abc in abc2: s = W.join([str(_) for _ in abc])   ;   t = f'{s:{w}}'   ;   tmp2.append(t)
    for abc in abc3: s = W.join([str(_) for _ in abc])   ;   t = f'{s:{w}}'   ;   tmp3.append(t)
    for abc in abc4: s = W.join([str(_) for _ in abc])   ;   t = f'{s:{w}}'   ;   tmp4.append(t)
    idxs = [ f'{i:{w}}' for i, _ in enumerate(abcR) ]    ;      idxs = o.join(idxs)
    abc1, abc2, abc3, abc4 = o.join(tmp1), o.join(tmp2), o.join(tmp3), o.join(tmp4)
    if not csv:  dmpDataTableLine()
    slog(f'      {n}{d}{n}{idxs}{n}{e}{m}',     p=0, f=f)
    slog(f'abc1  {n}{d}{n}{abc1}{n}{e}{m}{l1}', p=0, f=f)
    slog(f'abc2  {n}{d}{n}{abc2}{n}{e}{m}{l2}', p=0, f=f)
    slog(f'abc3  {n}{d}{n}{abc3}{n}{e}{m}{l3}', p=0, f=f)
    slog(f'abc4  {n}{d}{n}{abc4}{n}{e}{m}{l4}', p=0, f=f)
    return abcR
########################################################################################################################################################################################################
def dmpPyth(k=50, rf=440, sss=V_SOUND, csv=0):
    slog(f'BGN Pythagorean ({k=} {rf=} {sss=} {csv=})')    ;    x, y = 13, 6   ;   z = x-2   ;  rnd = 1
    ww, mm, nn, oo, ff = (Z, Y, Y, Y, 3) if csv else (f'^{x}', W, Z, '|', 1)   ;   uu = f'^{x}'
    f0 = F440s[k] if rf==440 else F432s[k]     ;     w0 = CM_P_M * sss   ;   nt, i4v, i6v = Notes.NTONES, Notes.I4V, Notes.I6V
    ii, ns, fs, ws = [], [], [], []   ;   cs, ds = [], []   ;   us, vs = [], []   ;   ps, qs = [], []   ;   rs, ss = [], []   ;   nns, rrs = [], []
    abcs = k2fPyths(k, csv, fPyth)
    for i, e in enumerate(abcs):
        a, b, c   = e[0], e[1], e[2]
        r, ca, cb = abc2r(a, b, c)
        rr = [ a, ca, b, cb ]
        f  = r * f0     ;     w = w0 / f      ;   m = i % nt
        u  = 'P2' if a==2 and b==1 else i6v[i] if i == 12 else i6v[m]
        v  = 'P2' if a==2 and b==1 else i4v[m] if i == 12 else i4v[m]
        pa = a ** ca               ;   pb = b ** cb             ;   p = f'{pa:>{y}}/{pb:<{y}}'
        qa = f'{a}^{ca}'           ;   qb = f'{b}^{cb}'         ;   q = f'{qa:>{y}}/{qb:<{y}}'
        sa = f'{a}{i2spr(ca)}'     ;   sb = f'{b}{i2spr(cb)}'   ;   s = f'{sa:>{y}}/{sb:<{y}}'
        n, n2 = i2nPair(k + i, b=0 if i in (4, 6, 11) or k in (54, 56, 61) else 1, s=1, e=1)
        if n2 and i and i != nt and i != 6:    n += '/' + n2
        c  = r2cents(r)            ;   d = c - i * 100 if i != 0 else 0.0 # fixme
        ii.append(i)               ;   fs.append(fmtf(f, z))   ;   ps.append(p)   ;    rs.append(fmtf(r, z))   ;   us.append(u)   ;   cs.append(float(c) if rnd else fmtf(c, x))    ;    rrs.append(rr)
        ns.append(n)               ;   ws.append(fmtf(w, z))   ;   qs.append(q)   ;    ss.append(s)            ;   vs.append(v)   ;   ds.append(float(d) if rnd else fmtg(d, x if d > 0 else x))
    csw, dsw = (f'^{x}.2f', f'^{x}.2f') if rnd else (ww, x-1)
    ii     = fmtl(ii, w=uu, s=oo, d=Z)   ;   fs = fmtl(fs, w=uu, s=oo, d=Z)   ;   cs = fmtl(cs, w=csw, s=oo, d=Z)    ;   us = fmtl(us, w=uu, s=oo, d=Z)   ;    ps  = fmtl(ps, w=ww, s=oo, d=Z)   ;   rs = fmtl(rs, w=uu, s=oo, d=Z)
    ns     = fmtl(ns, w=uu, s=oo, d=Z)   ;   ws = fmtl(ws, w=uu, s=oo, d=Z)   ;   ds = fmtl(ds, w=dsw, s=oo, d=Z)    ;   vs = fmtl(vs, w=uu, s=oo, d=Z)   ;    qs  = fmtl(qs, w=ww, s=oo, d=Z)   ;   ss = fmtl(ss, w=uu, s=oo, d=Z)
    PythMap1[k] = rrs
    pfxr   = f'Ratio {nn}[{nn}'   ;   pfxc = f'Cents {nn}[{nn}'   ;   pfxn = f'Note  {nn}[{nn}'   ;   pfxi = f'Index {nn}[{nn}'
    pfxp   = f'Ratio1{nn}[{nn}'   ;   pfxd = f'dCents{nn}[{nn}'   ;   pfxf = f'Freq  {nn}[{nn}'   ;   pfxv = f'Intrv1{nn}[{nn}'
    pfxq   = f'Ratio2{nn}[{nn}'   ;   pfxs = f'Ratio3{nn}[{nn}'   ;   pfxw = f'Wavlen{nn}[{nn}'   ;   pfxu = f'Intrv2{nn}[{nn}'
    sfx    = f'{nn}]'             ;   sfxc = f'{nn}]{mm}cents'    ;   sfxf = f'{nn}]{mm}Hz'       ;   sfxw = f'{nn}]{mm}cm'    
    slog(f'{pfxi}{ii}{sfx}',  p=0, f=ff)
    slog(f'{pfxn}{ns}{sfx}',  p=0, f=ff)
    slog(f'{pfxv}{vs}{sfx}',  p=0, f=ff)
    slog(f'{pfxu}{us}{sfx}',  p=0, f=ff)
    slog(f'{pfxr}{rs}{sfx}',  p=0, f=ff)
    slog(f'{pfxp}{ps}{sfx}',  p=0, f=ff)
    slog(f'{pfxq}{qs}{sfx}',  p=0, f=ff)
    slog(f'{pfxs}{ss}{sfx}',  p=0, f=ff)
    slog(f'{pfxc}{cs}{sfxc}', p=0, f=ff)
    slog(f'{pfxd}{ds}{sfxc}', p=0, f=ff)
    slog(f'{pfxf}{fs}{sfxf}', p=0, f=ff)
    slog(f'{pfxw}{ws}{sfxw}', p=0, f=ff)
    if not csv:  dmpDataTableLine()
    slog(f'END Pythagorean ({k=} {rf=} {sss=} {csv=})')
########################################################################################################################################################################################################
def k2fPyths(k=50, c=0, f=fPyth):
    return f(6, 5, c) if k==50 or k== 62 else f(5, 6, c) if k==57 else f(4, 7, c) if k==52 else f(3, 8, c) if k==59 else f(2, 9, c)  if k==54 else f(1, 10, c) if k==61 else f(0, 11, c) if k==56 \
                                         else f(7, 4, c) if k==55 else f(8, 3, c) if k==60 else f(9, 2, c) if k==53 else f(10, 1, c) if k==58 else f(11, 0, c) if k==51 else f(12, 0, c)
#   return fPyth(7, 6, c) if k==50 or k== 62 else fPyth(6, 7, c) if k==57 else fPyth(5, 8, c) if k==52 else fPyth(4, 9, c)  if k==59 else fPyth(3, 10, c) if k==54 else fPyth(2, 11, c) if k==61 else fPyth(1, 12, c) if k==56 \
#                                            else fPyth(8, 5, c) if k==55 else fPyth(9, 4, c) if k==60 else fPyth(10, 3, c) if k==53 else fPyth(11, 2, c) if k==58 else fPyth(12, 1, c) if k==51 else fPyth(13, 0, c)
########################################################################################################################################################################################################
def f2nPair(f, rf=440, b=None, s=0, e=0):
    ni = Notes.NTONES * math.log2(f / rf)
    i  = round(A4_INDEX + ni)
    return i2nPair(i, b, s, e)
    
def i2nPair(i, b=None, s=0, e=0):
    m = Z    ;    n = FLATS[i] if b == 1 else SHRPS[i]
    if s:                       n = n[:-1].strip()
    if e == 1 and len(n) > 1:
        m = FLATS[i] if not b else SHRPS[i]   ;   m = m[:-1].strip() if s else m
    return n, m
########################################################################################################################################################################################################
def k2dCent(k):
        return k-100 if 50<=k<150 else k-200 if 150<=k<250 else k-300 if 250<=k<350 else k-400 if 350<=k<450 else k-500 if 450<=k<550 else k-600 if 550<=k<650 else k-700 if 650<=k<750 else k-800 if 750<=k<850 else k-900 if 850<=k<950 else k-1000 if 950<=k<1050 else k-1100 if 1050<=k<1150 else k-1200
#        return c-100 if 50<=c<150 else c-200 if 150<=c<250 else c-300 if 250<=c<350 else c-400 if 350<=c<450 else c-500 if 450<=c<550 else c-600 if 550<=c<650 else c-700 if 650<=c<750 else c-800 if 750<=c<850 else c-900 if 850<=c<950 else c-1000 if 950<=c<1050 else c-1100 if 1050<=c<1150 else c-1200

def dmpDataTableLine(): slog(f' ' * 6 + f'-' * 14 * 13 + f'-', p=0)
########################################################################################################################################################################################################
def dmpPythMap1(ni, csv=0):
    x, y = 13, 6   ;   ww, mm, nn, oo, dd, ff = (Z, Y, Y, Y, '[', 3) if csv else (f'^{x}', W, Z, '|', Z, 1)   ;   uu = f'^{x}'
    ii = [ f'{i}' for i in range(Notes.NTONES + 1) ]   ;   slog(f'    k    {fmtl(ii, w=ww, s=mm, d=Z)}', p=0) if ni == 1 else None
#    ck = sorted(PythMap2.keys())
    dmpDataTableLine() if not csv and ni == 1 else None
    for i, (k, v) in enumerate(PythMap1.items()):
        n, n2   = i2nPair(k, b=0 if k in (54, 56, 61) else 1, s=1)
        rats, qots, exps, exus, cnts = [], [], [], [], []
        pd = [f'{i:2}', f'{k:2}', f'{n:2}']   ;   pdf = mm.join(pd) 
        for e in v:
            a, ca, b, cb = e
            pa, pb = a ** ca, b ** cb
            rat  = f'{float(pa/pb):{uu}.4f}'
            qot  = f'{pa:{y}}/{pb:<{y}}'
            expA = f'{a}^{ca}'         ;   expB = f'{b}^{cb}'         ;   exp = f'{expA:>{y}}/{expB:<{y}}'
            exuA = f'{a}{i2spr(ca)}'   ;   exuB = f'{b}{i2spr(cb)}'   ;   exu = f'{exuA:>{y}}/{exuB:<{y}}'
            cnt  = r2cents(pa/pb)
            if not csv and ni == 5:    PythMap2[cnt] = PythMap2[cnt] + 1 if cnt in PythMap2.keys() else 1
            cnt  = f'{cnt:{uu}.0f}'
            rats.append(rat)   ;   qots.append(qot)   ;   exps.append(exp)   ;   exus.append(exu)   ;   cnts.append(cnt)
        ratsf = Z.join(fmtl(rats, w=ww, s=oo, d=dd))
        qotsf = Z.join(fmtl(qots, w=ww, s=oo, d=dd))
        expsf = Z.join(fmtl(exps, w=ww, s=oo, d=dd))
        exusf = Z.join(fmtl(exus, w=ww, s=oo, d=dd))
        cntsf = Z.join(fmtl(cnts, w=ww, s=oo, d=dd))
        if   ni == 1: slog(f'{pdf} {ratsf}', p=0, f=ff)
        elif ni == 2: slog(f'{pdf} {qotsf}', p=0, f=ff)
        elif ni == 3: slog(f'{pdf} {expsf}', p=0, f=ff)
        elif ni == 4: slog(f'{pdf} {exusf}', p=0, f=ff)
        elif ni == 5: slog(f'{pdf} {cntsf}', p=0, f=ff)
    if not csv:  dmpDataTableLine()   ;   slog(f'    k    {fmtl(ii, w=ww, s=mm, d=Z)}', p=0) if ni == 5 else None
########################################################################################################################################################################################################
def checkPythIvals(i, j, ks, cs, ds):
    nt, i4v, i6v = Notes.NTONES, Notes.I4V, Notes.I6V
    eps = pythEpsln()
    if i == 0:   slog(f' j j*100 i     c       k        d       e       c`     c       k        d       e       c`')
    if j in i4v:
        u = i4v[j]    ;   v = i6v[j]
        if not i % 2 and i and i != len(ks)-1:
            m = 1 if i % 2 else -1
            slog(f'{j:2} {j*100:4} {i:2} {u}[{cs[i]:2} @ {ks[i]:8.3f}: {ds[i]:7.3f} = {eps:5.3f} * {cs[i+m]:2}]  {v}[{cs[i+m]:2} @ {ks[i+m]:8.3f}: {ds[i+m]:7.3f} = {eps:5.3f} * {cs[i]:2}]')
            assert round(cs[i+m] * eps, 3) == round(ds[i], 3),          f'{cs[i+m]:2} * {eps:5.3f} == {ds[i]:7.3f}'
            assert cs[i+m] * round(eps, 3) + j*100 == round(ks[i], 3),  f'{cs[i+m]:2} * {round(eps, 3):5.3} + 100*{j:2} == {round(ks[i], 3):8.3f}'
########################################################################################################################################################################################################
def dmpPythMap2(csv=0):
    ww, uu, mm, ff  = ('^7', '^7.2f', Y, 3) if csv else ('^7', '^7.2f', W, 1)
    nt, i4v, i6v = Notes.NTONES, Notes.I4V, Notes.I6V
    ii, cs, ds, j2s, us, vs, ws = [], [], [], [], [], [], []   ;   j2 = 0
    ks           = sorted(PythMap2.keys())
    for i, k in enumerate(ks):
        j = i % 2
        if j: j2 = math.floor(i/2) + 1
#        if j2 in i4v:        u = i4v[j2]    ;   v = i6v[j2]   ;   us.append(u)   ;   vs.append(v)
        j2s.append(j2)
        c = PythMap2[k]
        d = k2dCent(k) if i != 0 else 0.0
        ii.append(i)
        cs.append(c)
        ds.append(d)
        checkPythIvals(i, j2, ks, cs, ds)
#        ival = i6v[i] if i % 2 and i < len(i6v) else i4v[i] if i < len(i4v) else 'P2'
        ival = i6v[j2] if i % 2 and j2 < len(i6v) else i4v[j2] if j2 < len(i4v) else 'P2'
#        ival = vs[j2] if j2 % 2 and j2 < len(vs) else us[j2] if j2 < len(us) else 'P2'
        ws.append(ival) # if i % 2 else None
    slog(f'Index {fmtl(ii,  w=ww, s=mm, d=Z)}', p=0, f=ff)
    slog(f' J2s  {fmtl(j2s, w=ww, s=mm, d=Z)}', p=0, f=ff)
    slog(f'Intrv {fmtl(ws,  w=ww, s=mm, d=Z)}', p=0, f=ff)
#    slog(f'Intrv {fmtl(us,  w=ww, s=mm, d=Z)}', p=0, f=ff)
#    slog(f'Intr2 {fmtl(vs,  w=ww, s=mm, d=Z)}', p=0, f=ff)
    slog(f'Cents {fmtl(ks,  w=uu, s=mm, d=Z)}', p=0, f=ff)
    slog(f'dCent {fmtl(ds,  w=uu, s=mm, d=Z)}', p=0, f=ff)
    slog(f'Count {fmtl(cs,  w=ww, s=mm, d=Z)}', p=0, f=ff)
########################################################################################################################################################################################################
'''        
    k:          0             1             2             3             4             5             6             7             8             9            10            11            12       #  1   2   3   4   5   6   7   8   9   10   11
 0 51: E♭      1/1        2187/2048        9/8       19683/16384      81/64     177147/131072    729/512         3/2        6561/4096       27/16      59049/32768     243/128         2/1      # 2k     19k      .2M          6k      59k
 1 58: B♭      1/1        2187/2048        9/8       19683/16384      81/64          4/3         729/512         3/2        6561/4096       27/16      59049/32768     243/128         2/1      # 2k     19k                   6k      59k
 2 53: F       1/1        2187/2048        9/8       19683/16384      81/64          4/3         729/512         3/2        6561/4096       27/16         16/9         243/128         2/1      # 2k     19k                   6k
 3 60: C       1/1        2187/2048        9/8          32/27         81/64          4/3         729/512         3/2        6561/4096       27/16         16/9         243/128         2/1      # 2k                           6k
 4 55: G       1/1        2187/2048        9/8          32/27         81/64          4/3         729/512         3/2         128/81         27/16         16/9         243/128         2/1      # 2k
 5 50: D       1/1         256/243         9/8          32/27         81/64          4/3         729/512         3/2         128/81         27/16         16/9         243/128         2/1      # 243 9/8 /27 81/ 4/3 512 3/2 /81 27/  /9  243
 6 57: A       1/1         256/243         9/8          32/27         81/64          4/3        1024/729         3/2         128/81         27/16         16/9         243/128         2/1      #                      1k
 7 52: E       1/1         256/243         9/8          32/27         81/64          4/3        1024/729         3/2         128/81         27/16         16/9        4096/2187        2/1      #                      1k                   2k
 8 59: B       1/1         256/243         9/8          32/27       8192/6561        4/3        1024/729         3/2         128/81         27/16         16/9        4096/2187        2/1      #              6k      1k                   2k
 9 54: F♯      1/1         256/243         9/8          32/27       8192/6561        4/3        1024/729         3/2         128/81      32768/19683      16/9        4096/2187        2/1      #              6k      1k         19k       2k
10 61: C♯      1/1         256/243     65536/59049      32/27       8192/6561        4/3        1024/729         3/2         128/81      32768/19683      16/9        4096/2187        2/1      #     59k      6k      1k         19k       2k
11 56: G♯      1/1         256/243     65536/59049      32/27       8192/6561        4/3        1024/729    262144/177147    128/81      32768/19683      16/9        4096/2187        2/1      #     59k      6k      1k .2M     19k       2k
    k:          0             1             2             3             4             5             6             7             8             9            10            11            12       #  1   2   3   4   5   6   7   8   9   10   11
 0 51: E♭       0            114           204           318           408           522           612           702           816           906          1020          1110          1200      # 114     318     522         816     1020
 1 58: B♭       0            114           204           318           408           498           612           702           816           906          1020          1110          1200      # 114     318                 816     1020
 2 53: F        0            114           204           318           408           498           612           702           816           906           996          1110          1200      # 114     318                 816
 3 60: C        0            114           204           294           408           498           612           702           816           906           996          1110          1200      # 114                         816
 4 55: G        0            114           204           294           408           498           612           702           792           906           996          1110          1200      # 114
 5 50: D        0            90            204           294           408           498           612           702           792           906           996          1110          1200      #  90 204 294 408 498 612 702 792 906 996  1110
 6 57: A        0            90            204           294           408           498           588           702           792           906           996          1110          1200      #                     588
 7 52: E        0            90            204           294           408           498           588           702           792           906           996          1086          1200      #                     588                  1086
 8 59: B        0            90            204           294           384           498           588           702           792           906           996          1086          1200      #             384     588                  1086
 9 54: F♯       0            90            204           294           384           498           588           702           792           882           996          1086          1200      #             384     588         882      1086
10 61: C♯       0            90            180           294           384           498           588           702           792           882           996          1086          1200      #     180     384     588         882      1086
11 56: G♯       0            90            180           294           384           498           588           678           792           882           996          1086          1200      #     180     384     588 678     882      1086
    k:          0             1             2             3             4             5             6             7             8             9            10            11            12       #  1   2   3   4   5   6   7   8   9   10   11
'''
