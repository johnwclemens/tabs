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

def dumpData(csv=0):
    slog(f'BGN {csv=}')
    dumpTestA(  csv)
    dumpNF(     csv)
    dumpTestB(  csv)
    dumpND(     csv)
    dmpOTS(     csv=csv, vs=V_SOUND)
    dmpPyth(    csv=csv, vs=V_SOUND)
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
    I6V = { 0:'d2', 1:'A1', 2:'d3', 3:'A2', 4:'d4', 5:'A3', 6:'d5', 7:'A4', 8:'d6', 9:'A5', 10:'d7', 11:'A6', 12:'d8'} # ,13:'A7'} # 8/12/16 TT d2 A1 
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
    hdrs       = ['I', 'F', 'S', 'IV', 'mM', 'dA']
    hdrs       = f'{m.join([ f"{h:{w}}" for h in hdrs ])}'
    slog(f'{hdrs}', p=0, f=f)
    for i, (k, v) in enumerate(ND.items()):
        slog(f'{i:x}{m}{fmtl(v, w=w, d=d, s=m)}', p=0, f=f)
#    for i in range(len(ND)):   slog(f'{i:x}{m}{fmtl(ND[i], w=w, d=d, s=m)}', p=0, f=f)
    slog('END')
########################################################################################################################################################################################################
ND = initND()

FLATS  = [ f'{v}{n}' for n in range(Notes.NTONES - 1) for v in Notes.I2F.values() ][:MAX_FREQ_IDX]
SHRPS  = [ f'{v}{n}' for n in range(Notes.NTONES - 1) for v in Notes.I2S.values() ][:MAX_FREQ_IDX]
#FLATS = [ f'{v}{n}' for n in range(Notes.NTONES - 1) for v in Notes.I4F.values() ][:MAX_FREQ_IDX]
#SHRPS = [ f'{v}{n}' for n in range(Notes.NTONES - 1) for v in Notes.I4S.values() ][:MAX_FREQ_IDX]

def reduce(a, b, c):
    n = a ** c * b ** -c
    for i in range(c):
        if   a > b:
            while n > 2:
                n /= 2
        elif a < b:
            while n < 1:
                n *= 2
    return n
        
def f440(i):         return 440 * (2 ** (1/Notes.NTONES)) ** (i - A4_INDEX)
def f432(i):         return 432 * (2 ** (1/Notes.NTONES)) ** (i - A4_INDEX)
def fOTS(i, r=440):  f0 = F440s[0] if r == 440 else F432s[0]  ;  return f0 * i
def fPyth(a, b, c):  return reduce(a, b, c)
def Piano(c, d=1):   (d, d2) = ("[", "]") if d else (Z, Z)    ;  return f'{utl.NONE:^17}' if c is None else f'{fmtl(c, w=3, d=d, d2=d2):17}'

F440s  = [ f440(i)  for i in range(MAX_FREQ_IDX) ]
F432s  = [ f432(i)  for i in range(MAX_FREQ_IDX) ]
FOTSs  = [ fOTS(i)  for i in range(1, 33) ]
FPythA = [ fPyth(3, 2, i) for i in range(0, 7) ]
FPythB = [ fPyth(2, 3, i) for i in range(1, 7) ]
FPyths = FPythA   ;   FPyths.extend(FPythB)
FPyths = sorted(FPyths)
########################################################################################################################################################################################################
def dumpNF(csv=0):
    w, d, m, n, f = (Z, Z, Y, Y, 3) if csv else ('^5', '[', W, Z, 1)
    slog('BGN Note Frequencies in Hertz, Wavelengths in cm')  ;  nm = MAX_FREQ_IDX   ;   p, q = -8, 88+1   ;   g, h = 0, nm
    slog(f'Piano{n}{fmtl(list(range(p, q)),          w=w, d=d, s=m)}', p=0, f=f)
    slog(f'Index{n}{fmtl(list(range(g, h)),          w=w, d=d, s=m)}', p=0, f=f)
    dumpFreqs(432, csv)    ;    dumpFreqs(440, csv)
    dmpWaveLs(432, csv)    ;    dmpWaveLs(440, csv)
    slog(f'Flats{n}{fmtl(list(FLATS),                w=w, d=d, s=m)}', p=0, f=f)
    slog(f'Shrps{n}{fmtl(list(SHRPS),                w=w, d=d, s=m)}', p=0, f=f)
    slog('END')

def dumpFreqs(r=440, csv=0):
    m, f = (Y, 3) if csv else (W, 1)
    freqs = F440s if r == 440 else F432s   ;    ref = '440A' if r == 440 else '432A'   ;   fs = []
    for freq in freqs:
        ft = fmtf(freq, 5)
        fs.append(f'{ft}')
    fs = m.join(fs)  ;  ref += m if csv else ' ['  ;  sfx = Z if csv else '] Hz'
    slog(f'{ref}{fs}{sfx}', p=0, f=f)

def dmpWaveLs(r=440, csv=0, vs=V_SOUND):
    m, f = (Y, 3) if csv else (W, 1)
    freqs = F440s if r == 440 else F432s   ;    ref = '440A' if r == 440 else '432A'   ;   ws = []
    for freq in freqs:
        w = CM_P_M * vs/freq
        wt = fmtf(w, 5)
        ws.append(f'{wt}')
    ws = m.join(ws)  ;  ref += m if csv else ' ['  ;  sfx = Z if csv else '] cm'
    slog(f'{ref}{ws}{sfx}', p=0, f=f)
########################################################################################################################################################################################################
def dmpOTS(r=440, csv=0, vs=V_SOUND):
    (ww, d, m, nn, ff) = (Z, Z, Y, Y, 3) if csv else ('^6', '[', W, Z, 1)
    rs    = F440s      if r == 440 else F432s        ;   cs, ns, fs, ws = [], [], [], []
    freqs = F440s[:32] if r == 440 else F432s[:32]   ;   ref = '440A' if r == 440 else '432A'
    f0    = F440s[0]    ;   w0 = CM_P_M * vs/f0
    for i, freq in enumerate(freqs):
        i += 1          ;    f  = fOTS(i, r)    ;    w  = w0 / i
        n  = freq2Note(f, r=r, b=0 if i in (17, 22, 25, 28) else 1) # 
        j  = Notes.n2ai(n)
        assert 0 <= j < len(rs),  f'{j=} {len(rs)=}'
        f2 = rs[j]      ;    c  = 1200 * math.log2(f/f2)
        fs.append(fmtf(f, 6))    ;    ns.append(n)    ;    ws.append(fmtf(w, 6))
        cs.append(fmtg(c, 6 if c >= 0 else 5))
    fs   = m.join(fs)   ;   ws = m.join(ws)   ;   ns = fmtl(ns, w=ww, d=Z)   ;   cs = fmtl(cs, w=ww, d=Z)
    ref += m if csv else ' ['    ;    sfxf = Z if csv else '] Hz'    ;    sfxw = Z if csv else '] cm'
    pfxn = 'note ['     ;   pfxc = 'cents['   ;   sfx = Z if csv else ']'
    slog(f'Index{nn}{fmtl(list(range(1, 33)), w=ww, d=d, s=m)}', p=0, f=ff)
    slog(f'{ref}{fs}{sfxf}', p=0, f=ff)
    slog(f'{pfxn}{ns}{sfx}', p=0, f=ff)
    slog(f'{pfxc}{cs}{sfx}', p=0, f=ff)
    slog(f'{ref}{ws}{sfxw}', p=0, f=ff)

def dmpPyth(r=440, k=50, csv=0, vs=V_SOUND):
    (ww, d, mm, nn, ff) = (Z, Z, Y, Y, 3) if csv else ('^6', '[', W, Z, 1)
    f0 = F440s[k] if r==440 else F432s[k]     ;     w0 = CM_P_M * vs   ;   nt, i4v, i6v = Notes.NTONES, Notes.I4V, Notes.I6V
    ns, vs, rs, cs, fs, ws = [], [], [], [], [], []   ;   x = 6
    slog(f'BGN Pythagorean tuning {r=} {k=} {csv=} {vs=} m/s')
    for i, fr in enumerate(FPyths):
        f = fr * f0     ;     w = w0 / f
#       v  = i4v[i % nt] if i % nt <= 5 else i6v[6] if i % nt == 6 else i6v[7] if i % nt == 7 else i4v[11] if i == 12 else i4v[(i-1) % nt]
#       m = i % nt     ;     v = i4v[m] if m <= 5 else i6v[6] if m == 6 else i6v[7] if m == 7 else i4v[10] if i == 11 else i4v[11] if i == 12 else i4v[(i-1) % nt]
#        m = i % nt     ;     v = i4v[m] if m in range(1, 5) else i6v[m] if m in (6, 7) else i4v[10] if i == 11 else i4v[11] if i == 12 else i4v[(i-1) % nt]
        m = i % nt     ;     v = i4v[m] if m in range(1, 6) else i6v[m] if m in (6, 7) else i4v[(i-1) % nt] if m > 7 else i4v[11] if i == 12 else i4v[0]
        n  = freq2Note(f, r=r, b=0 if i in (4, 7, 12) else 1, s=1)
        c  = 1200 * math.log2(fr)
        ns.append(n)    ;   vs.append(v)      ;   rs.append(fmtf(fr, x))
        fs.append(fmtf(f, x))    ;   ws.append(fmtf(w, x))          ;   cs.append(fmtg(c, x if c >= 0 else x-1))
    ns   = fmtl(ns, w=ww, d=Z)   ;   vs = fmtl(vs, w=ww, d=Z)       ;   cs = fmtl(cs, w=ww, d=Z)
    rs   = fmtl(rs, d=Z)         ;   ws = mm.join(ws)   ;   fs   = fmtl(fs, d=Z)     
    pfxf = 'Freq ['     ;   pfxw = 'Wvlen['   ;   pfxv = 'Intrvl'   ;    sfx = Z if csv else ']'
    pfxr = 'Ratio['     ;   pfxn = 'Note ['   ;   pfxc = 'cents['   ;   sfxf = Z if csv else '] Hz'    ;    sfxw = Z if csv else '] cm'
    slog(f'Index{nn}{fmtl(list(range(1 + nt)), w=ww, d=d, s=mm)}', p=0, f=ff)
    slog(f'{pfxn}{ns}{sfx}',  p=0, f=ff)
    slog(f'{pfxv}{vs}{sfx}',  p=0, f=ff)
    slog(f'{pfxr}{rs}{sfx}',  p=0, f=ff)
    slog(f'{pfxc}{cs}{sfx}',  p=0, f=ff)
    slog(f'{pfxf}{fs}{sfxf}', p=0, f=ff)
    slog(f'{pfxw}{ws}{sfxw}', p=0, f=ff)
    slog(f'END Pythagorean tuning {r=} {k=} {csv=} {vs=} m/s')

def freq2Note(f, r=440, b=1, s=0):
    ni = Notes.NTONES * math.log2(f / r)
    i  = round(A4_INDEX + ni)
    n = FLATS[i] if b==1 else SHRPS[i]
    if s: n = n[:-1].strip()
    return n
