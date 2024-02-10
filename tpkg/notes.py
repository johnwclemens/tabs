from tpkg import utl  as utl
from tpkg import unic as unic

F, N, S          = unic.F, unic.N, unic.S
W, Y, Z          = utl.W, utl.Y, utl.Z
slog, ist        = utl.slog, utl.ist
fmtf, fmtl, fmtm = utl.fmtf, utl.fmtl, utl.fmtm
signed           = utl.signed
ns2signs         = utl.ns2signs
MAX_FREQ_IDX     = utl.MAX_FREQ_IDX

def dumpData(csv=0):
    slog(f'BGN {csv=}')
    dumpTestB(csv)
    dumpNF(csv)
    dumpTestA(csv)
    dumpND(csv)
    slog(f'END {csv=}')
########################################################################################################################################################################################################
def dumpTestA(csv=0):
    w, d, m, n, file = (0, Z, Y, Y, 3) if csv else ('^5', '[', W, Z, 1)
    t   = Notes.NTONES  ;    s = Notes.SHRP  ;    f = Notes.FLAT  ;  is1 = Notes.IS1  ;  is2 = Notes.IS2  ;  i2v = Notes.I2V  ;  v = 21
    i2n = Notes.i2n     ;  f2s = Notes.F2S   ;  s2f = Notes.S2F   ;  i2f = Notes.I2F  ;  i2s = Notes.I2S  ;  i4v = Notes.I4V  ;  n2i = Notes.N2I
    i4n = Notes.i4n     ;  f4s = Notes.F4S   ;  s4f = Notes.S4F   ;  i4f = Notes.I4F  ;  i4s = Notes.I4S  ;  i6v = Notes.I6V  ;  v2i = Notes.V2I
    slog('BGN')         ;    o = t + 1       ;    p = 0
    slog(f'    {m}{fmtl( list(range(v)), w=w, d=d, s=m)}', p=p, f=file)
    slog(f' F2S{m}{fmtl([ f"{i2n(f)[k]}:{f2s[i2n(f)[k]]}" if k in is1 else W for k in range(t) ], w=w, d=d, s=m)}', p=p, f=file)
    slog(f' F4S{m}{fmtl([ f"{i4n(f)[k]}:{f4s[i4n(f)[k]]}" if k in is2 else W for k in range(o) ], w=w, d=d, s=m)}', p=p, f=file)
    slog(f' S2F{m}{fmtl([ f"{i2n(s)[k]}:{s2f[i2n(s)[k]]}" if k in is1 else W for k in range(t) ], w=w, d=d, s=m)}', p=p, f=file)
    slog(f' S4F{m}{fmtl([ f"{i4n(s)[k]}:{s4f[i4n(s)[k]]}" if k in is2 else W for k in range(o) ], w=w, d=d, s=m)}', p=p, f=file)
    slog(f' I2F{m}{fmtl([ f"{k}:{i2f[k]}"                                     for k in range(t) ], w=w, d=d, s=m)}', p=p, f=file)
    slog(f' I4F{m}{fmtl([ f"{k}:{i4f[k]}"                                     for k in range(t) ], w=w, d=d, s=m)}', p=p, f=file)
    slog(f' I2S{m}{fmtl([ f"{k}:{i2s[k]}"                                     for k in range(t) ], w=w, d=d, s=m)}', p=p, f=file)
    slog(f' I4S{m}{fmtl([ f"{k}:{i4s[k]}"                                     for k in range(t) ], w=w, d=d, s=m)}', p=p, f=file)
    slog(f' N2I{m}{fmtl([ f"{k}:{v}"                                     for k,v in n2i.items() ], w=w, d=d, s=m)}', p=p, f=file)
    slog(f'I2NF{m}{fmtl([ f"{k}:{i2n(f)[k]}"                                  for k in range(t) ], w=w, d=d, s=m)}', p=p, f=file)
    slog(f'I4NF{m}{fmtl([ f"{k}:{i4n(f)[k]}"                                  for k in range(t) ], w=w, d=d, s=m)}', p=p, f=file)
    slog(f'I2NS{m}{fmtl([ f"{k}:{i2n(s)[k]}"                                  for k in range(t) ], w=w, d=d, s=m)}', p=p, f=file)
    slog(f'I4NS{m}{fmtl([ f"{k}:{i4n(s)[k]}"                                  for k in range(t) ], w=w, d=d, s=m)}', p=p, f=file)
    slog(f' I2V{m}{fmtl([ f"{k}:{v}"                                     for k,v in i2v.items() ], w=w, d=d, s=m)}', p=p, f=file)
    slog(f' I4V{m}{fmtl([ f"{k}:{v}"                                     for k,v in i4v.items() ], w=w, d=d, s=m)}', p=p, f=file)
    slog(f' I6V{m}{fmtl([ f"{k}:{v}"                                     for k,v in i6v.items() ], w=w, d=d, s=m)}', p=p, f=file)
    slog(f' V2I{m}{fmtl([ f"{k}:{v}"                                     for k,v in v2i.items() ], w=w, d=d, s=m)}', p=p, f=file)
    slog('END')

def dumpTestB(csv=0):
    w, d, m, n, f = (0, Z, Y, Y, 3) if csv else (2, '[', W, Z, 1)   ;   p = 0  ;  v = 21
    x = f'{w}x'  ;  u = f'>{w}'  ;  y = f'<{w}x'  ;  z = f'<{w}'    ;   q = f'>{w}x'
    slog('BGN')  ;  w = 0 if csv else '^5'
    slog(f'    {m}{fmtl(list(range(v)), w=w,       d=d, s=m)}', p=p, f=f)
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
########################################################################################################################################################################################################
class Notes__ALT:#0   1. . .. . .2. . .. . .3. . .. . .4. . .. . .5. . .. . .6. . .. . .7. . .. . .8. . .. . .9. . .. . .a. . .. . .b. . .. . .0      #  2    7 9  #
    F2S = {           f'D{F}':f'C{S}',            'Eb':'D#',                       'Gb':'F#',            'Ab':'G#',            'Bb':'A#'                       } # 1 3  6 8 a # 5/9
    S2F = {           f'C{S}':f'D{F}',            'D#':'Eb',                       'F#':'Gb',            'G#':'Ab',            'A#':'Bb'                       } # 1 3  6 8 a # 5/9
    F4S = {'C' :f'B{S}',                                  'Fb':'E' , 'F' :'E#',                                                       'Cb':'B' , 'C`' :'B#' } #0   45     b# 4/9
    S4F = {f'B{S}':'C' ,                                  'E' :'Fb', 'E#':'F' ,                                                       'B' :'Cb', 'B#`':'C'  } #0   45     b# 4/9
#            0. . . 0 . . . 1 . . . 2 . . . 3 . . . 4 . . . 5 . . . 6 . . . 7 . . . 8 . . . 9 . . . a . . . b . . . 0
    V2I = {        'R':0 , 'm2':1, 'M2':2, 'm3':3, 'M3':4, 'P4':5, 'b5':6, 'P5':7, 'm6':8, 'M6':9,'m7':10,'M7':11,'R`':12 } # 8/12/16
    I2V = {        0:'R' , 1:'m2', 2:'M2', 3:'m3', 4:'M3', 5:'P4', 6:'b5', 7:'P5', 8:'m6', 9:'M6',10:'m7',11:'M7',12:'R'  } # 8/12/16
    I2F = {        0:'C' , 1:'Db', 2:'D' , 3:'Eb', 4:'E' , 5:'F' , 6:'Gb', 7:'G' , 8:'Ab', 9:'A' ,10:'Bb',11:'B' ,12:'C'  } # 8/12/16
    I2S = {        0:'C' , 1:'C#', 2:'D' , 3:'D#', 4:'E' , 5:'F' , 6:'F#', 7:'G' , 8:'G#', 9:'A' ,10:'A#',11:'B' ,12:'C'  } # 8/12/16
    I4F = {        0:'C' , 1:'Db', 2:'D' , 3:'Eb', 4:'Fb', 5:'F' , 6:'Gb', 7:'G' , 8:'Ab', 9:'A' ,10:'Bb',11:'Cb',12:'C'  } # 8/12/16
    I4S = { 0:'B#'       , 1:'C#', 2:'D' , 3:'D#', 4:'E' , 5:'E#', 6:'F#', 7:'G' , 8:'G#', 9:'A' ,10:'A#',11:'B' ,12:'B#' } # 8/12/16
#            0. . . 0 . . . 1 . . . 2 . . . 3 . . . 4 . . . 5 . . . 6 . . . 7 . . . 8 . . . 9 . . . a . . . b . . . 0
    N2I = {'B#':0, 'C':0 ,'C#':1, 'Db':1, 'D':2, 'D#':3, 'Eb':3, 'E':4, 'Fb':4, 'E#':5, 'F':5, 'F#':6, 'Gb':6, 'G':7, 'G#':8, 'Ab':8, 'A':9, 'A#':10, 'Bb':10, 'B':11, 'Cb':11, 'B#`':12, 'C`':12 } #21
########################################################################################################################################################################################################
class Notes(object): #      1          2       3          4          5          6          7       8          9       a          b       0      #[  2    7 9  ]#
    I2F = {         0:'C' , 1:f'D{F}', 2:'D' , 3:f'E{F}', 4:'E' ,    5:'F' ,    6:f'G{F}', 7:'G' , 8:f'A{F}', 9:'A' , 10:f'B{F}', 11:'B'    } # ,12:'C' } # 8/12/16 
    I2S = {         0:'C' , 1:f'C{S}', 2:'D' , 3:f'D{S}', 4:'E' ,    5:'F' ,    6:f'F{S}', 7:'G' , 8:f'G{S}', 9:'A' , 10:f'A{S}', 11:'B'    } # ,12:'C' } # 8/12/16
    I4F = {         0:'C' , 1:f'D{F}', 2:'D' , 3:f'E{F}', 4:f'F{F}', 5:'F' ,    6:f'G{F}', 7:'G' , 8:f'A{F}', 9:'A' , 10:f'B{F}', 11:f'C{F}'} # ,12:'C' } # 8/12/16 Cb Fb
    I4S = { 0:f'B{S}',      1:f'C{S}', 2:'D' , 3:f'D{S}', 4:'E' ,    5:f'E{S}', 6:f'F{S}', 7:'G' , 8:f'G{S}', 9:'A' , 10:f'A{S}', 11:'B'    } # ,12:'C' } # 8/12/16 B# E#
    I2V = {         0:'R' , 1:'b2',    2:'2' , 3:'m3',    4:'M3',    5:'4' ,    6:'b5',    7:'5' , 8:'#5',    9:'6' , 10:'b7',    11:'7'    } # ,12:'R' } # 8/12/16 b5 #5
    I4V = {         0:'P1', 1:'m2',    2:'M2', 3:'m3',    4:'M3',    5:'P4',    6:'TT',    7:'P5', 8:'m6',    9:'M6', 10:'m7',    11:'M7'   } # ,12:'P8'} # 8/12/16 TT m6
    I6V = {         0:'d2', 1:'A1',    2:'d3', 3:'A2',    4:'d4',    5:'A3',    6:'TT',    7:'d6', 8:'A5',    9:'d7', 10:'A6',    11:'d8'   } # ,12:'A7'} # 8/12/16 TT d2 A1 
    V2I = {       'R':0 ,'b2':1,     '2':2, 'm3':3,    'M3':4,     '4':5 ,   'b5':6,     '5':7 ,'#5':8,     '6':9,  'b7':10,     '7':11     } # ,'R`':12} # 8/12/16 b5 #5
    N2I = {f'B{S}':0, 'C' :0, f'C{S}':1, f'D{F}':1, 'D' :2, f'D{S}':3, f'E{F}':3, 'E' :4, f'F{F}':4, f'E{S}':5, 'F' :5, f'F{S}':6, f'G{F}':6, 'G' :7, f'G{S}':8, f'A{F}':8, 'A' :9, f'A{S}':10, f'B{F}':10, 'B' :11, f'C{F}' :11, f'B{S}`':12, 'C`':12 } #21 B# Cb E# Fb
    F2S = {            f'D{F}':f'C{S}', f'E{F}':f'D{S}',                       f'G{F}':f'F{S}', f'A{F}':f'G{S}', f'B{F}':f'A{S}'                        } #[ 1 3  6 8 a ]# 5/9 Db->C#
    S2F = {            f'C{S}':f'D{F}', f'D{S}':f'E{F}',                       f'F{S}':f'G{F}', f'G{S}':f'A{F}', f'A{S}':f'B{F}'                        } #[ 1 3  6 8 a ]# 5/9 C#->Db
#               0             1                2             3          4             5                6                7            8
    F4S = { 'C' :f'B{S}',                             f'F{F}':'E' , 'F' :f'E{S}',                                             f'C{F}':'B'  } #,'C``' :'B#' } #[0   45     b]# 4/9
    S4F = { f'B{S}':'C' ,                             'E' :f'F{F}', f'E{S}':'F' ,                                             'B' :f'C{F}' } #,'B#``':'C'  } #[0   45     b]# 4/9
    IS0,  IS1,  IS2    = [2, 7, 9], [1, 3, 6, 8, 10], [0, 4, 5, 11]
    FLAT, NTRL, SHRP   =  -1,   0,   1  # -1 ~= 2
    TYPES              = [ 'NTRL', 'SHRP', 'FLAT' ] # 0=NTRL, 1=SHRP, 2=FLAT=-1
    TYPE               = SHRP
    NTONES             = len(V2I)

    @classmethod
    def i2n(cls, t=None): return cls.I2S if t is None or t==cls.SHRP or t==cls.NTRL else cls.I2F
    @classmethod
    def i4n(cls, t=None): return cls.I4S if t is None or t==cls.SHRP or t==cls.NTRL else cls.I4F
    @classmethod
    def index(cls, n, o=0):         name = n[:len(n)-1] if o else n   ;   assert name in cls.N2I,  f'{name=} {cls.N2I=}'   ;   return cls.N2I[name]
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
    @classmethod
    def nextName(cls, n, iv, o=0):  i = cls.index(n, o)  ;  j = cls.V2I[iv]  ;  k = cls.nextIndex(i, j)  ;  return cls.name(k, 0)
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
    w, d, m, f = (0, Z, Y, 3) if csv else (2, '[', W, 1)
    hdrs       = ['I', 'F', 'S', 'IV', 'mM', 'dA']
    hdrs       = f'{m.join([ f"{h:{w}}" for h in hdrs ])}'
    slog(f'{hdrs}', p=0, f=f)
    for i, (k, v) in enumerate(ND.items()):
        slog(f'{i:x}{m}{fmtl(v, w=w, d=d, s=m)}', p=0, f=f)
#    for i in range(len(ND)):   slog(f'{i:x}{m}{fmtl(ND[i], w=w, d=d, s=m)}', p=0, f=f)
########################################################################################################################################################################################################
ND = initND()

FLATS  = [ f'{v}{n}' for n in range(Notes.NTONES - 1) for v in Notes.I2F.values() ][:MAX_FREQ_IDX]
SHRPS  = [ f'{v}{n}' for n in range(Notes.NTONES - 1) for v in Notes.I2S.values() ][:MAX_FREQ_IDX]
#FLATS  = [ f'{v}{n}' for n in range(Notes.NTONES - 1) for v in Notes.I4F.values() ][:MAX_FREQ_IDX]
#SHRPS  = [ f'{v}{n}' for n in range(Notes.NTONES - 1) for v in Notes.I4S.values() ][:MAX_FREQ_IDX]

def FREQ1(index): return 440 * pow(pow(2, 1/Notes.NTONES), index - 57)
def FREQ2(index): return 432 * pow(pow(2, 1/Notes.NTONES), index - 57)
def Piano(c, d=1): (d, d2) = ("[", "]") if d else (Z, Z)  ;  return f'{utl.NONE:^17}' if c is None else f'{fmtl(c, w=3, d=d, d2=d2):17}'

FREQ1S = [ FREQ1(i) for i in range(MAX_FREQ_IDX) ]
FREQ2S = [ FREQ2(i) for i in range(MAX_FREQ_IDX) ]
########################################################################################################################################################################################################
def dumpNF(csv=0):
    w, d, m, n, f = (Z, Z, Y, Y, 3) if csv else ('^5', '[', W, Z, 1)
    slog('Note Frequencies in Hertz')  ;  nm = MAX_FREQ_IDX   ;   p, q = -8, 88+1   ;   g, h = 1, nm+1
    slog(f'Piano{n}{fmtl(list(range(p, q)),          w=w, d=d, s=m)}', p=0, f=f)
    slog(f'Index{n}{fmtl(list(range(g, h)),          w=w, d=d, s=m)}', p=0, f=f)
    dumpFreqs(432, csv)    ;    dumpFreqs(440, csv)
    dmpWvLens(432, csv)    ;    dmpWvLens(440, csv)
    slog(f'Flats{n}{fmtl(list(FLATS),                w=w, d=d, s=m)}', p=0, f=f)
    slog(f'Shrps{n}{fmtl(list(SHRPS),                w=w, d=d, s=m)}', p=0, f=f)

def dumpFreqs(r=440, csv=0):
    m, f = (Y, 3) if csv else (W, 1)
    freqs = FREQ1S if r == 440 else FREQ2S   ;    ref = '440A' if r == 440 else '432A'   ;   fs = []
    for freq in freqs:
        ft = fmtf(freq, 5)
        fs.append(f'{ft}')
    fs = m.join(fs)  ;  ref += m if csv else ' ['  ;  sfx = Z if csv else '] Hz'
    slog(f'{ref}{fs}{sfx}', p=0, f=f)
########################################################################################################################################################################################################
def dmpWvLens(r=440, csv=0, v=340):
    m, f = (Y, 3) if csv else (W, 1)         ;   cmpm = 100
    freqs = FREQ1S if r == 440 else FREQ2S   ;    ref = '440A' if r == 440 else '432A'   ;   ws = []
    for freq in freqs:
        w = cmpm * v/freq
        wt = fmtf(w, 5)
        ws.append(f'{wt}')
    ws = m.join(ws)  ;  ref += m if csv else ' ['  ;  sfx = Z if csv else '] cm'
    slog(f'{ref}{ws}{sfx}', p=0, f=f)
