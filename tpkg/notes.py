from tpkg import utl
from tpkg import unic
#from tpkg import strngs

F, N, S       = unic.F,     unic.N,    unic.S
W, Y, Z       = utl.W,      utl.Y,     utl.Z
slog, ist     = utl.slog,   utl.ist
fmtf, fmtg    = utl.fmtf,   utl.fmtg
fmtl, fmtm    = utl.fmtl,   utl.fmtm
signed, filtA = utl.signed, utl.filtA
#ns2signs      = utl.ns2signs

MAX_FREQ_IDX  = utl.MAX_FREQ_IDX
ACCD_TONES    = ['b', '#', '♭', '♮', '♯']
CM_P_M        = 100 # cm per m, cemtimeters per meter
V_SOUND       = 345 # m/s in dry air @ about 73 deg F
A4_INDEX      = 57  # 440 Hz A Note Index
'''
P1  d2  m2  A1  d3  M2  m3  A2  d4  M3  P4  A3  d5  A4  d6  P5  m6  A5  d7  M6  m7  A6  d8  M7  A7  P8

P1  m2  M2  m3  M3  P4  A4  P5  m6  M6  m7  M7  P8
d2  A1  d3  A2  d4  A3  d5  d6  A5  d7  A6  d8  A7  

P1  C   d2  D♭♭
m2  D♭  A1  C♯
M2  D   d3  E♭♭
m3  E♭  A2  D♯
M3  E   d4  F♭
P4  F   A3  E♯
A4  F♯  d5  G♭
P5  G   d6  A♭♭
m6  A♭  A5  G♯
M6  A   d7  B♭♭
m7  B♭  A6  A♯
M7  B   d8  C♭
P8  C   A7  B♯
'''
########################################################################################################################################################################################################
class Notes:#0      1       2       3       4       5       6       7       8       9        a        b           0       #[  2    7 9  ]#
    I2F = { 0:'C' , 1:'D♭', 2:'D' , 3:'E♭', 4:'E' , 5:'F' , 6:'G♭', 7:'G' , 8:'A♭', 9:'A' , 10:'B♭', 11:'B' } # ,12:'C' } # 8/12/16
    I2S = { 0:'C' , 1:'C♯', 2:'D' , 3:'D♯', 4:'E' , 5:'F' , 6:'F♯', 7:'G' , 8:'G♯', 9:'A' , 10:'A♯', 11:'B' } # ,12:'C' } # 8/12/16
    I4F = { 0:'C' , 1:'D♭', 2:'D' , 3:'E♭', 4:'F♭', 5:'F' , 6:'G♭', 7:'G' , 8:'A♭', 9:'A' , 10:'B♭', 11:'C♭'} # ,12:'C' } # 8/12/16 C♭ F♭
    I4S = { 0:'B♯', 1:'C♯', 2:'D' , 3:'D♯', 4:'E' , 5:'E♯', 6:'F♯', 7:'G' , 8:'G♯', 9:'A' , 10:'A♯', 11:'B' } # ,12:'C' } # 8/12/16 B♯ E♯
#    I2V = { 0:'R',  1:'♭2', 2:'2',  3:'♭3', 4:'3',  5:'4',  6:'TT', 7:'5',  8:'♭6', 9:'6',  10:'♭7', 11:'7', 12:'R' } # 8/12/16 ♭5 ♯5
    I4V = { 0:'P1', 1:'m2', 2:'M2', 3:'m3', 4:'M3', 5:'P4', 6:'A4', 7:'P5', 8:'m6', 9:'M6', 10:'m7', 11:'M7', 12:'P8'} # 8/12/16 TT m6
#    I6V = { 0:'d2', 1:'A1', 2:'d3', 3:'A2', 4:'d4', 5:'A3', 6:'d5', 7:'d6', 8:'A5', 9:'d7', 10:'A6', 11:'d8', 12:'A7'} # 8/12/16 TT d2 A1
    I2V = { 0:'R' , 1:'♭2', 2:'2' , 3:'m3', 4:'M3', 5:'4' , 6:'♭5', 7:'5' , 8:'♯5', 9:'6' , 10:'♭7', 11:'7' }  # 8/12/16 ♭5 ♯5
#    I4V = { 0:'P1', 1:'m2', 2:'M2', 3:'m3', 4:'M3', 5:'P4', 6:'A4', 7:'P5', 8:'m6', 9:'M6', 10:'m7', 11:'M7'}  # 8/12/16 TT m6
    I6V = { 0:'d2', 1:'A1', 2:'d3', 3:'A2', 4:'d4', 5:'P4', 6:'d5', 7:'d6', 8:'A5', 9:'d7', 10:'A6', 11:'d8'}  # 8/12/16 TT d2 A1
    V2I = { 'R':0 , '♭2':1, '2':2 , 'm3':3, 'M3':4, '4' :5, '♭5':6, '5':7 , '♯5':8, '6' :9, '♭7':10, '7' :11} # ,'R`':12} # 8/12/16 ♭5 ♯5
#    V2I = { 'R':0 , '♭2':1, '2':2,  '♭3':3, '3':4,  '4':5,  'TT':6, '5':7 , '♭6':8, '6' :9, '♭7':10, '7':11, 'O':12 } # ,'R`':12} # 8/12/16 ♭5 ♯5
    V4I = { 'P1':0, 'm2':1, 'M2':2, 'm3':3, 'M3':4, 'P4':5, 'A4':6, 'P5':7 , 'm6':8, 'M6' :9, 'm7':10, 'M7':11, 'P8':12 } # ,'R`':12} # 8/12/16 ♭5 ♯5
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
    NT                 = len(V2I)

    I4V_I6V = {}
    for i in range(13):
        if i in I4V:
            I4V_I6V[2*i] = I4V[i]
        if i in I6V:
            I4V_I6V[2*i + 1] = I6V[i]

    @staticmethod
    def nextN(n, i=1):
        m = n[0]  ;  o = ord(m)
        if i == 1:   return m
        match o:
            case 65 | 66 | 67 | 68 | 69 | 70:  mm = chr(o+1) # A B C D E F
            case 71:                           mm = chr(65)  # G
            case   _: mm = '??'
        if i>2:
            return Notes.nextN(mm, i-1)
        else:    return mm

    @staticmethod
    def prevN(n): #todo N/A not used ?
        match n[0]:
            case 'A': _ = 'G'
            case 'B': _ = 'A'
            case 'C': _ = 'B'
            case 'D': _ = 'C'
            case 'E': _ = 'D'
            case 'F': _ = 'E'
            case 'G': _ = 'F'
            case _:   _ = '??'
        return _

    @classmethod
    def i2n(cls, t=None):           return cls.I2S if t is None or t==cls.SHRP or t==cls.NTRL else cls.I2F
    @classmethod
    def i4n(cls, t=None):           return cls.I4S if t is None or t==cls.SHRP or t==cls.NTRL else cls.I4F
    @classmethod
    def n2i(cls, n, o=0):           n = n[:-1] if o else n    ;   assert n in cls.N2I,  f'{n=} {cls.N2I=}'     ;   return cls.N2I[n]
    @classmethod
    def n2ai(cls, m):               n = m[:-1].strip()        ;   assert n in cls.N2I,  f'{n=} {cls.N2I=}'     ;   return cls.n2ipo(filtA(m))
    @classmethod
    def n2ipo(cls, n):              o = int(n[-1]) * cls.NT   ;   n = n[:-1]   ;   return cls.N2I[n] + o
    @classmethod
    def nextName(cls, n, iv, o=0):  i = cls.n2i(n, o)   ;   j = cls.V4I[iv]   ;   k = cls.nextIndex(i, j)   ;   return cls.name(k, 0) # todo fixme N/A not used?
    @classmethod
    def nextIndex(cls, i, d=1):     return (i+d) % cls.NT # todo fixme N/A not used?
    @classmethod
    def name(cls, i, t=None, n2=0):
        j = i % cls.NT   ;   t = 2 if t==-1 else t
#       t =     cls.TYPE if t is None else t
        t = t           if t is not None else cls.TYPE
        assert             t is not None  and ist(t, int),     f'{t=} {type(t)=}'
        assert  cls.i2n()    is not None  and t in cls.i2n(),  f'{t=} {cls.i2n()=}'
        assert  cls.i2n()[t] is not None,                   f'{t=} {cls.i2n()[t]=}'
        return  cls.i2n(t)[j]  if n2  else cls.i4n(t)[j]
########################################################################################################################################################################################################

NT        = Notes.NT
########################################################################################################################################################################################################
def f440(i):         return float(440 * (2 ** (1/NT)) ** (i - A4_INDEX))
def f432(i):         return float(432 * (2 ** (1/NT)) ** (i - A4_INDEX))
#def fOTS(i, r=440):  f0 = F440s[0] if r == 440 else F432s[0]  ;   return f0 * i
def Piano(c, d=1):   (d, d2) = ("[", "]") if d else (Z, Z)    ;   return f'{utl.NONE:^17}' if c is None else f'{fmtl(c, w=3, d=d, d2=d2):17}'

F440s  = [ f440(i)  for i in range(MAX_FREQ_IDX) ]
F432s  = [ f432(i)  for i in range(MAX_FREQ_IDX) ]
########################################################################################################################################################################################################
FLATS  = [ f'{v}{n}' for n in range(NT - 1) for v in Notes.I2F.values() ][:MAX_FREQ_IDX]
SHRPS  = [ f'{v}{n}' for n in range(NT - 1) for v in Notes.I2S.values() ][:MAX_FREQ_IDX]
#FLATS = [ f'{v}{n}' for n in range(NT - 1) for v in Notes.I4F.values() ][:MAX_FREQ_IDX]
#SHRPS = [ f'{v}{n}' for n in range(NT - 1) for v in Notes.I4S.values() ][:MAX_FREQ_IDX]

def dumpData(csv=0):
    slog(f'BGN {csv=}')
    dumpTestA(  csv)
    dumpTestB(  csv)
    dumpND(     csv)
    dumpNF(     csv)
    slog(f'END {csv=}')
########################################################################################################################################################################################################
def dumpTestA(csv=0):
    w, d, m, n, f = (2, Z, Y, Y, 3) if csv else (2, Z, W, Z, 1)   ;   p = 0   ;   v = 21
    x = f'{w}x'  ;  u = f'>{w}'  ;  y = f'<{w}x'  ;  z = f'<{w}'    ;   q = f'>{w}x'
    slog('BGN')  ;  w = 0 if csv else '^7'
    slog(f'    {m}[{m}{fmtl(list(range(v)), w=w,       d=d, s=m)}{m}]', p=p, f=f)
    slog(f'ACCD{m}[{m}{fmtl([F, N, S],      w=w,       d=d, s=m)}{m}]', p=p, f=f)
    slog(f' F2S{m}[{m}{fmtm(Notes.F2S,      w=w,       d=d, s=m)}{m}]', p=p, f=f)   ;   w = 0 if csv else 2
    slog(f' F4S{m}[{m}{fmtm(Notes.F4S,      w=u, wv=z, d=d, s=m)}{m}]', p=p, f=f)
    slog(f' S2F{m}[{m}{fmtm(Notes.S2F,      w=w,       d=d, s=m)}{m}]', p=p, f=f)
    slog(f' S4F{m}[{m}{fmtm(Notes.S4F,      w=u, wv=z, d=d, s=m)}{m}]', p=p, f=f)
    slog(f' I2F{m}[{m}{fmtm(Notes.I2F,      w=x, wv=w, d=d, s=m)}{m}]', p=p, f=f)
    slog(f' I4F{m}[{m}{fmtm(Notes.I4F,      w=x, wv=w, d=d, s=m)}{m}]', p=p, f=f)
    slog(f' I2S{m}[{m}{fmtm(Notes.I2S,      w=x, wv=w, d=d, s=m)}{m}]', p=p, f=f)
    slog(f' I4S{m}[{m}{fmtm(Notes.I4S,      w=x, wv=w, d=d, s=m)}{m}]', p=p, f=f)
    slog(f' N2I{m}[{m}{fmtm(Notes.N2I,      w=u, wv=y, d=d, s=m)}{m}]', p=p, f=f)
    slog(f'I2NF{m}[{m}{fmtm(Notes.i2n(1),   w=q, wv=z, d=d, s=m)}{m}]', p=p, f=f)
    slog(f'I4NF{m}[{m}{fmtm(Notes.i4n(1),   w=q, wv=z, d=d, s=m)}{m}]', p=p, f=f)
    slog(f'I2NS{m}[{m}{fmtm(Notes.i2n(-1),  w=q, wv=z, d=d, s=m)}{m}]', p=p, f=f)
    slog(f'I4NS{m}[{m}{fmtm(Notes.i4n(-1),  w=q, wv=z, d=d, s=m)}{m}]', p=p, f=f)
    slog(f' I2V{m}[{m}{fmtm(Notes.I2V,      w=x, wv=w, d=d, s=m)}{m}]', p=p, f=f)
    slog(f' I4V{m}[{m}{fmtm(Notes.I4V,      w=x, wv=w, d=d, s=m)}{m}]', p=p, f=f)
    slog(f' I6V{m}[{m}{fmtm(Notes.I6V,      w=x, wv=w, d=d, s=m)}{m}]', p=p, f=f)
    slog(f' V2I{m}[{m}{fmtm(Notes.V2I,      w=u, wv=y, d=d, s=m)}{m}]', p=p, f=f)
    slog('END')

def dumpTestB(csv=0):
    w, d, m, n, file = ('^5', Z, Y, Y, 3) if csv else ('^5', Z, W, Z, 1)
    t   = NT          ;    s = Notes.SHRP  ;    f = Notes.FLAT  ;  is1 = Notes.IS1  ;  is2 = Notes.IS2  ;  i2v = Notes.I2V  ;    v = 21
    i2n = Notes.i2n   ;  f2s = Notes.F2S   ;  s2f = Notes.S2F   ;  i2f = Notes.I2F  ;  i2s = Notes.I2S  ;  i4v = Notes.I4V  ;  n2i = Notes.N2I
    i4n = Notes.i4n   ;  f4s = Notes.F4S   ;  s4f = Notes.S4F   ;  i4f = Notes.I4F  ;  i4s = Notes.I4S  ;  i6v = Notes.I6V  ;  v2i = Notes.V2I
    slog('BGN')       ;    o = t + 1       ;    p = 0
    slog(f'    {m}[{m}{fmtl( list(range(v)),                                                          w=w, d=d, s=m)}{m}]', p=p, f=file)
    slog(f'ACCD{m}[{m}{fmtl([F, N, S],                                                                w=w, d=d, s=m)}{m}]', p=p, f=file)
    slog(f' F2S{m}[{m}{fmtl([ f"{i2n(f)[k]}:{f2s[i2n(f)[k]]}" if k in is1 else W for k in range(t) ], w=w, d=d, s=m)}{m}]', p=p, f=file)
    slog(f' F4S{m}[{m}{fmtl([ f"{i4n(f)[k]}:{f4s[i4n(f)[k]]}" if k in is2 else W for k in range(o) ], w=w, d=d, s=m)}{m}]', p=p, f=file)
    slog(f' S2F{m}[{m}{fmtl([ f"{i2n(s)[k]}:{s2f[i2n(s)[k]]}" if k in is1 else W for k in range(t) ], w=w, d=d, s=m)}{m}]', p=p, f=file)
    slog(f' S4F{m}[{m}{fmtl([ f"{i4n(s)[k]}:{s4f[i4n(s)[k]]}" if k in is2 else W for k in range(o) ], w=w, d=d, s=m)}{m}]', p=p, f=file)
    slog(f' I2F{m}[{m}{fmtl([ f"{k}:{i2f[k]}"                                    for k in range(t) ], w=w, d=d, s=m)}{m}]', p=p, f=file)
    slog(f' I4F{m}[{m}{fmtl([ f"{k}:{i4f[k]}"                                    for k in range(t) ], w=w, d=d, s=m)}{m}]', p=p, f=file)
    slog(f' I2S{m}[{m}{fmtl([ f"{k}:{i2s[k]}"                                    for k in range(t) ], w=w, d=d, s=m)}{m}]', p=p, f=file)
    slog(f' I4S{m}[{m}{fmtl([ f"{k}:{i4s[k]}"                                    for k in range(t) ], w=w, d=d, s=m)}{m}]', p=p, f=file)
    slog(f' N2I{m}[{m}{fmtl([ f"{k}:{v}"                                    for k,v in n2i.items() ], w=w, d=d, s=m)}{m}]', p=p, f=file)
    slog(f'I2NF{m}[{m}{fmtl([ f"{k}:{i2n(f)[k]}"                                 for k in range(t) ], w=w, d=d, s=m)}{m}]', p=p, f=file)
    slog(f'I4NF{m}[{m}{fmtl([ f"{k}:{i4n(f)[k]}"                                 for k in range(t) ], w=w, d=d, s=m)}{m}]', p=p, f=file)
    slog(f'I2NS{m}[{m}{fmtl([ f"{k}:{i2n(s)[k]}"                                 for k in range(t) ], w=w, d=d, s=m)}{m}]', p=p, f=file)
    slog(f'I4NS{m}[{m}{fmtl([ f"{k}:{i4n(s)[k]}"                                 for k in range(t) ], w=w, d=d, s=m)}{m}]', p=p, f=file)
    slog(f' I2V{m}[{m}{fmtl([ f"{k}:{v}"                                    for k,v in i2v.items() ], w=w, d=d, s=m)}{m}]', p=p, f=file)
    slog(f' I4V{m}[{m}{fmtl([ f"{k}:{v}"                                    for k,v in i4v.items() ], w=w, d=d, s=m)}{m}]', p=p, f=file)
    slog(f' I6V{m}[{m}{fmtl([ f"{k}:{v}"                                    for k,v in i6v.items() ], w=w, d=d, s=m)}{m}]', p=p, f=file)
    slog(f' V2I{m}[{m}{fmtl([ f"{k}:{v}"                                    for k,v in v2i.items() ], w=w, d=d, s=m)}{m}]', p=p, f=file)
    slog('END')
########################################################################################################################################################################################################
def updNotes(i, m, n, t, d=0): # N/A
    if   t  ==  Notes.FLAT:    Notes.I2F[i] = m
    elif t  ==  Notes.SHRP:    Notes.I2S[i] = n
    if   d:
        if m in Notes.S2F: del Notes.S2F[m]
        if n in Notes.F2S: del Notes.F2S[n]
    else:
        Notes.F2S[n] = m   ;   Notes.S2F[m] = n
########################################################################################################################################################################################################
def initND():    return { i: [ Notes.I2F[i], Notes.I2S[i], Notes.I2V[i], Notes.I4V[i], Notes.I6V[i] ] for i in range(NT) }

def dumpND(csv=0):
    slog('BGN')
    w, d1, d2, m, n, f = (2, Y, W, Y, Y, 3) if csv else (2, '[', ']', W, Z, 1)
    hdrs       = ['♭ ', '♯ ', 'IV', 'mM', 'dA']
    hdrs       = f'{m.join([ f"{hdrs[i]}" for i in range(len(hdrs)) ])}'
    slog(f'I{d1}{hdrs}{d2}', p=0, f=f)
    for i, (k, v) in enumerate(ND.items()):
        slog(f'{i:x}{d1}{fmtl(v, w=w, d=Z, s=m)}{d2}', p=0, f=f) # fixme using hex format for single char width hack
#    for i in range(len(ND)):   slog(f'{i:x}{m}{fmtl(ND[i], w=w, d=d, s=m)}', p=0, f=f)
    slog('END')

ND = initND()
########################################################################################################################################################################################################
def dumpNF(csv=0):
    slog('BGN 12 Tone Equal Tempored (Hz, cm)')
    w, m, s, f = ('^5', Y, Y, 3) if csv else ('^5', W, Z, 1)
    nm = MAX_FREQ_IDX      ;    p, q = -8, 88+1   ;   g, h = 0, nm
    pfxp, pfxi, pfxf, pfxs =   f'Piano{m}[{m}',  f'Index{m}[{m}',  f'Flats{m}[{m}',  f'Shrps{m}[{m}'
    sfxp, sfxi, sfxf, sfxs = f'{m}]{m}Piano', f'{m}]{m}Index', f'{m}]{m}Flats', f'{m}]{m}Shrps'
    slog(f'{pfxp}{fmtl(list(range(p, q)), w=w, s=m, d=Z)}{sfxp}', p=0, f=f)
    slog(f'{pfxi}{fmtl(list(range(g, h)), w=w, s=m, d=Z)}{sfxi}', p=0, f=f)
    dumpFreqs(432, csv=csv)    ;    dumpFreqs(440, csv=csv)
    dmpWaveLs(432, csv=csv)    ;    dmpWaveLs(440, csv=csv)
    slog(f'{pfxf}{fmtl(list(FLATS),       w=w, s=m, d=Z)}{sfxf}', p=0, f=f)
    slog(f'{pfxs}{fmtl(list(SHRPS),       w=w, s=m, d=Z)}{sfxs}', p=0, f=f)
    slog('END 12 Tone Equal Tempored (Hz, cm)')

def dumpFreqs(rf=440, csv=0):
    m, s, f = (Y, Y, 3) if csv else (W, Z, 1)
    freqs = F440s if rf == 440 else F432s   ;   ref = f'F{rf}A{m}'   ;   fs = []
    for freq in freqs:
        ft = fmtf(freq, 5)
        fs.append(f'{ft}')
    fs = m.join(fs)   ;   pfx = f'{ref}[{m}'   ;   sfx = f'{m}]{m}{ref}Hz'
    slog(f'{pfx}{fs}{sfx}', p=0, f=f)

def dmpWaveLs(rf=440, sss=V_SOUND, csv=0):
    m, s, f = (Y, Y, 3) if csv else (W, Z, 1)
    freqs = F440s if rf == 440 else F432s   ;    ref = f'W{rf}A{m}'   ;   ws = []
    for freq in freqs:
        w = CM_P_M * sss/freq
        wt = fmtf(w, 5)
        ws.append(f'{wt}')
    ws = m.join(ws)   ;   pfx = f'{ref}[{m}'   ;   sfx = f'{m}]{m}{ref}cm'
    slog(f'{pfx}{ws}{sfx}', p=0, f=f)
########################################################################################################################################################################################################
