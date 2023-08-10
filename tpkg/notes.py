#import tpkg.utl as utl
from tpkg import utl as utl

M, P         = utl.M, utl.P
F, N, S      = utl.F, utl.N, utl.S
W, Y, Z      = utl.W, utl.Y, utl.Z
slog, fmtf   = utl.slog, utl.fmtf
fmtl, fmtm   = utl.fmtl, utl.fmtm
signed       = utl.signed
ns2signs     = utl.ns2signs
MAX_FREQ_IDX = utl.MAX_FREQ_IDX

def dumpData(csv=0):
    slog(f'BGN D{F} D{N} D{S}')
    dumpTestA(csv)
    dumpNF(csv)
    dumpTestB(csv)
    dumpND(csv)
    dumpKSH(csv)
    dumpKSV(csv)
    slog(f'END D{F} D{N} D{S}')
########################################################################################################################################################################################################
def dumpTestA(csv=0):
    w, d, m, n, file = (0, Z, Y, Y, 3) if csv else ('^5', '[', W, Z, 1)
    t   = Notes.NTONES  ;    s = Notes.SHRP  ;    f = Notes.FLAT  ;  is1 = Notes.IS1  ;  is2 = Notes.IS2  ;  i2v = Notes.I2V  ;  v = 21
    i2n = Notes.I2N     ;  f2s = Notes.F2S   ;  s2f = Notes.S2F   ;  i2f = Notes.I2F  ;  i2s = Notes.I2S  ;  i4v = Notes.I4V  ;  n2i = Notes.N2I
    i4n = Notes.I4N     ;  f4s = Notes.F4S   ;  s4f = Notes.S4F   ;  i4f = Notes.I4F  ;  i4s = Notes.I4S  ;  i6v = Notes.I6V  ;  v2i = Notes.V2I
    slog('BGN')         ;    o = t + 1       ;    p = 0
    slog(f'    {m}{fmtl( list(range(v)), w=w, d=d, s=m)}', p=p, f=file)
    slog(f' F2S{m}{fmtl([ f"{i2n[f][k]}:{f2s[i2n[f][k]]}"  if k in is1 else W for k in range(t) ], w=w, d=d, s=m)}', p=p, f=file)
    slog(f' F4S{m}{fmtl([ f"{i4n[f][k]}:{f4s[i4n[f][k]]}"  if k in is2 else W for k in range(o) ], w=w, d=d, s=m)}', p=p, f=file)
    slog(f' S2F{m}{fmtl([ f"{i2n[s][k]}:{s2f[i2n[s][k]]}"  if k in is1 else W for k in range(t) ], w=w, d=d, s=m)}', p=p, f=file)
    slog(f' S4F{m}{fmtl([ f"{i4n[s][k]}:{s4f[i4n[s][k]]}"  if k in is2 else W for k in range(o) ], w=w, d=d, s=m)}', p=p, f=file)
    slog(f' I2F{m}{fmtl([ f"{k}:{i2f[k]}"                                     for k in range(t) ], w=w, d=d, s=m)}', p=p, f=file)
    slog(f' I4F{m}{fmtl([ f"{k}:{i4f[k]}"                                     for k in range(t) ], w=w, d=d, s=m)}', p=p, f=file)
    slog(f' I2S{m}{fmtl([ f"{k}:{i2s[k]}"                                     for k in range(t) ], w=w, d=d, s=m)}', p=p, f=file)
    slog(f' I4S{m}{fmtl([ f"{k}:{i4s[k]}"                                     for k in range(t) ], w=w, d=d, s=m)}', p=p, f=file)
    slog(f' N2I{m}{fmtl([ f"{k}:{v}"                                     for k,v in n2i.items() ], w=w, d=d, s=m)}', p=p, f=file)
    slog(f'I2NF{m}{fmtl([ f"{k}:{i2n[f][k]}"                                  for k in range(t) ], w=w, d=d, s=m)}', p=p, f=file)
    slog(f'I4NF{m}{fmtl([ f"{k}:{i4n[f][k]}"                                  for k in range(t) ], w=w, d=d, s=m)}', p=p, f=file)
    slog(f'I2NS{m}{fmtl([ f"{k}:{i2n[s][k]}"                                  for k in range(t) ], w=w, d=d, s=m)}', p=p, f=file)
    slog(f'I4NS{m}{fmtl([ f"{k}:{i4n[s][k]}"                                  for k in range(t) ], w=w, d=d, s=m)}', p=p, f=file)
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
    slog(f'I2NF{m}{fmtm(Notes.I2N[-1],  w=q, wv=z, d=d, s=m)}', p=p, f=f)
    slog(f'I4NF{m}{fmtm(Notes.I4N[-1],  w=q, wv=z, d=d, s=m)}', p=p, f=f)
    slog(f'I2NS{m}{fmtm(Notes.I2N[ 1],  w=q, wv=z, d=d, s=m)}', p=p, f=f)
    slog(f'I4NS{m}{fmtm(Notes.I4N[ 1],  w=q, wv=z, d=d, s=m)}', p=p, f=f)
    slog(f' I2V{m}{fmtm(Notes.I2V,      w=x, wv=w, d=d, s=m)}', p=p, f=f)
    slog(f' I4V{m}{fmtm(Notes.I4V,      w=x, wv=w, d=d, s=m)}', p=p, f=f)
    slog(f' I6V{m}{fmtm(Notes.I6V,      w=x, wv=w, d=d, s=m)}', p=p, f=f)
    slog(f' V2I{m}{fmtm(Notes.V2I,      w=u, wv=y, d=d, s=m)}', p=p, f=f)
    slog('END')
########################################################################################################################################################################################################
class DSymb:
    SYMBS = {'X': 'mute', '/': 'slide', '\\': 'bend', '+': 'hammer', '~': 'vibrato', '^': 'tie', '.': 'staccato', '_': 'legato', '%': 'repeat', '|': 'bar', '[': 'groupL', ']': 'groupR'}
########################################################################################################################################################################################################
class Scales:
    MajorIs = [ 0, 2, 4, 5, 7, 9, 11 ]
    @classmethod
    def majIs(cls, i):  return [ (i + j) % Notes.NTONES for j in cls.MajorIs ]
########################################################################################################################################################################################################
class Modes:
    IONIAN, DORIAN, PHRYGIAN, LYDIAN, MIXOLYDIAN, AEOLIAN, LOCRIAN = range(7)
    NAMES = [ 'IONIAN', 'DORIAN', 'PHRYGIAN', 'LYDIAN', 'MIXOLYDIAN', 'AEOLIAN', 'LOCRIAN' ]
    TYPES = [  IONIAN,   DORIAN,   PHRYGIAN,   LYDIAN,   MIXOLYDIAN,   AEOLIAN,   LOCRIAN  ]
########################################################################################################################################################################################################
class Notes__ALT:#0   1. . .. . .2. . .. . .3. . .. . .4. . .. . .5. . .. . .6. . .. . .7. . .. . .8. . .. . .9. . .. . .a. . .. . .b. . .. . .0      #  2    7 9  #
    F2S = {           'Db\u266D':'C#',            'Eb':'D#',                       'Gb':'F#',            'Ab':'G#',            'Bb':'A#'                       } # 1 3  6 8 a # 5/9
    S2F = {           'C#\u266F':'Db',            'D#':'Eb',                       'F#':'Gb',            'G#':'Ab',            'A#':'Bb'                       } # 1 3  6 8 a # 5/9
    F4S = {'C\u266E' :'B#',                                  'Fb':'E' , 'F' :'E#',                                                       'Cb':'B' , 'C`' :'B#' } #0   45     b# 4/9
    S4F = {'B#':'C' ,                                  'E' :'Fb', 'E#':'F' ,                                                       'B' :'Cb', 'B#`':'C'  } #0   45     b# 4/9
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
    I2F = {         0:'C' , 1:f'D{F}', 2:'D' , 3:f'E{F}', 4:'E' ,    5:'F' ,    6:f'G{F}', 7:'G' , 8:f'A{F}', 9:'A' ,10:f'B{F}', 11:'B'    } # ,12:'C' } # 8/12/16
    I2S = {         0:'C' , 1:f'C{S}', 2:'D' , 3:f'D{S}', 4:'E' ,    5:'F' ,    6:f'F{S}', 7:'G' , 8:f'G{S}', 9:'A' ,10:f'A{S}', 11:'B'    } # ,12:'C' } # 8/12/16
    I4F = {         0:'C' , 1:f'D{F}', 2:'D' , 3:f'E{F}', 4:f'F{F}', 5:'F' ,    6:f'G{F}', 7:'G' , 8:f'A{F}', 9:'A' ,10:f'B{F}', 11:f'C{F}'} # ,12:'C' } # 8/12/16
    I4S = { 0:f'B{S}',      1:f'C{S}', 2:'D' , 3:f'D{S}', 4:'E' ,    5:f'E{S}', 6:f'F{S}', 7:'G' , 8:f'G{S}', 9:'A' ,10:f'A{S}', 11:'B'    } # ,12:'C' } # 8/12/16
    I2V = {         0:'R' , 1:'b2',    2:'2' , 3:'m3',    4:'M3',    5:'4' ,    6:'b5',    7:'5' , 8:'#5',    9:'6' ,10:'b7',    11:'7'    } # ,12:'R' } # 8/12/16
    I4V = {         0:'P1', 1:'m2',    2:'M2', 3:'m3',    4:'M3',    5:'P4',    6:'TT',    7:'P5', 8:'m6',    9:'M6',10:'m7',    11:'M7'   } # ,12:'P8'} # 8/12/16
    I6V = {         0:'d2', 1:'A1',    2:'d3', 3:'A2',    4:'d4',    5:'A3',    6:'TT',    7:'d6', 8:'A5',    9:'d7',10:'A6',    11:'d8'   } # ,12:'A7'} # 8/12/16
    V2I = {       'R':0 ,'b2':1,     '2':2, 'm3':3,    'M3':4,     '4':5 ,   'b5':6,     '5':7 ,'#5':8,     '6':9, 'b7':10,     '7':11     } # ,'R`':12 } # 8/12/16
    N2I = {f'B{S}':0, 'C' :0, f'C{S}':1, f'D{F}':1, 'D' :2, f'D{S}':3, f'E{F}':3, 'E' :4, f'F{F}':4, f'E{S}':5, 'F' :5, f'F{S}':6, f'G{F}':6, 'G' :7, f'G{S}':8, f'A{F}':8, 'A' :9, f'A{S}':10, f'B{F}':10, 'B' :11, f'C{F}' :11, f'B{S}`':12, 'C`':12 } #21
    F2S = {            f'D{F}':f'C{S}', f'E{F}':f'D{S}',                       f'G{F}':f'F{S}', f'A{F}':f'G{S}', f'B{F}':f'A{S}'                        } #[ 1 3  6 8 a ]# 5/9
    S2F = {            f'C{S}':f'D{F}', f'D{S}':f'E{F}',                       f'F{S}':f'G{F}', f'G{S}':f'A{F}', f'A{S}':f'B{F}'                        } #[ 1 3  6 8 a ]# 5/9
#               0             1                2             3          4             5                6                7           8
    F4S = { 'C' :f'B{S}',                             f'F{F}':'E' , 'F' :f'E{S}',                                             f'C{F}':'B'  } #,'C``' :'B#' } #[0   45     b]# 4/9
    S4F = { f'B{S}':'C' ,                             'E' :f'F{F}', f'E{S}':'F' ,                                             'B' :f'C{F}' } #,'B#``':'C'  } #[0   45     b]# 4/9
    I2N, I4N           = [None, I2S, I2F],  [None, I4S, I4F]
    IS0,  IS1,  IS2    = [2, 7, 9],  [1, 3, 6, 8, 10],  [0, 4, 5, 11]
    FLAT, NTRL, SHRP   =    -1,      0,      1    # -1 ~= 2
    TYPES              = [ 'NTRL', 'SHRP', 'FLAT' ] # 0=NTRL, 1=SHRP, 2=FLAT=-1
    TYPE, NTONES             = SHRP, len(V2I) # - 1

    @staticmethod
    def index(n, o=0):         name = n[:len(n)-1] if o else n  ;  return Notes.N2I[name]
    @staticmethod
    def nextIndex(i, d=1):     return (i+d) % Notes.NTONES
    @staticmethod
#    def name(i, t, n2):
#        slog(f'{type(Notes)}={Notes} {type(Notes.I2N[t])}={Notes.I2N[t]} {type(Notes.I2N[t][i%Notes.NTONES])}={Notes.I2N[t][i%Notes.NTONES]}')
#        if n2:   return Notes.I4N[t][i % Notes.NTONES]
#        else:    return Notes.I2N[t][i % Notes.NTONES]
#    def name(self, i, t=0, n2=0):   _ = t if t else self.type  ;  return Notes.I4N[_][i % Notes.NTONES] if n2 else Notes.I2N[_][i % Notes.NTONES]
    def name(i, t=0, n2=0):   t = t if t else Notes.TYPE  ;  return Notes.I4N[t][i % Notes.NTONES] if n2 else Notes.I2N[t][i % Notes.NTONES]
    @staticmethod
    def nextName(n, iv, o=0):  i = Notes.index(n, o)  ;  j = Notes.V2I[iv]  ;  k = Notes.nextIndex(i, j)  ;  return Notes.name(k, 0, 0)
########################################################################################################################################################################################################
# class NotesU(object): #     1          2       3          4          5          6          7       8          9       a          b       0      #[  2    7 9  ]#
#     I2F = {         0:'C' , 1:f'D{F}', 2:'D' , 3:f'E{F}', 4:'E' ,    5:'F' ,    6:f'G{F}', 7:'G' , 8:f'A{F}', 9:'A' ,10:f'B{F}', 11:'B'    } # ,12:'C' } # 8/12/16
#     I2S = {         0:'C' , 1:f'C{S}', 2:'D' , 3:f'D{S}', 4:'E' ,    5:'F' ,    6:f'F{S}', 7:'G' , 8:f'G{S}', 9:'A' ,10:f'A{S}', 11:'B'    } # ,12:'C' } # 8/12/16
#     I4F = {         0:'C' , 1:f'D{F}', 2:'D' , 3:f'E{F}', 4:f'F{F}', 5:'F' ,    6:f'G{F}', 7:'G' , 8:f'A{F}', 9:'A' ,10:f'B{F}', 11:f'C{F}'} # ,12:'C' } # 8/12/16
#     I4S = { 0:f'B{S}',      1:f'C{S}', 2:'D' , 3:f'D{S}', 4:'E' ,    5:f'E{S}', 6:f'F{S}', 7:'G' , 8:f'G{S}', 9:'A' ,10:f'A{S}', 11:'B'    } # ,12:'C' } # 8/12/16
#     I2V = {         0:'R' , 1:'b2',    2:'2' , 3:'m3',    4:'M3',    5:'4' ,    6:'b5',    7:'5' , 8:'#5',    9:'6' ,10:'b7',    11:'7'    } # ,12:'R' } # 8/12/16
# #    I2V = {         0:'R' , 1:f'{F}2',    2:'2' , 3:'m3',    4:'M3',    5:'4' ,    6:f'{F}5',    7:'5' , 8:f'{S}5',    9:'6' ,10:f'{F}7',    11:'7'    } # ,12:'R' } # 8/12/16
#     I4V = {         0:'P1', 1:'m2',    2:'M2', 3:'m3',    4:'M3',    5:'P4',    6:'TT',    7:'P5', 8:'m6',    9:'M6',10:'m7',    11:'M7'   } # ,12:'P8'} # 8/12/16
#     I6V = {         0:'d2', 1:'A1',    2:'d3', 3:'A2',    4:'d4',    5:'A3',    6:'TT',    7:'d6', 8:'A5',    9:'d7',10:'A6',    11:'d8'   } # ,12:'A7'} # 8/12/16
#     V2I = {       'R':0 ,'b2':1,     '2':2, 'm3':3,    'M3':4,     '4':5 ,   'b5':6,     '5':7 ,'#5':8,     '6':9, 'b7':10,     '7':11     } # ,'R`':12 } # 8/12/16
# #    V2I = {       'R':0 ,f'{F}2':1,     '2':2, 'm3':3,    'M3':4,     '4':5 ,   f'{F}5':6,     '5':7 ,f'{S}5':8,     '6':9, f'{F}7':10,     '7':11     } # ,'R`':12 } # 8/12/16
#     N2I = {f'B{S}':0, 'C' :0, f'C{S}':1, f'D{F}':1, 'D' :2, f'D{S}':3, f'E{F}':3, 'E' :4, f'F{F}':4, f'E{S}':5, 'F' :5, f'F{S}':6, f'G{F}':6, 'G' :7, f'G{S}':8, f'A{F}':8, 'A' :9, f'A{S}':10, f'B{F}':10, 'B' :11, f'C{F}' :11, f'B{S}`':12, 'C`':12 } #21
#     F2S = {            f'D{F}':f'C{S}', f'E{F}':f'D{S}',                       f'G{F}':f'F{S}', f'A{F}':f'G{S}', f'B{F}':f'A{S}'                        } #[ 1 3  6 8 a ]# 5/9
#     S2F = {            f'C{S}':f'D{F}', f'D{S}':f'E{F}',                       f'F{S}':f'G{F}', f'G{S}':f'A{F}', f'A{S}':f'B{F}'                        } #[ 1 3  6 8 a ]# 5/9
# #               0             1                2             3          4             5                6                7           8
#     F4S = { 'C' :f'B{S}',                             f'F{F}':'E' , 'F' :f'E{S}',                                             f'C{F}':'B'  } #,'C``' :'B#' } #[0   45     b]# 4/9
#     S4F = { f'B{S}':'C' ,                             'E' :f'F{F}', f'E{S}':'F' ,                                             'B' :f'C{F}' } #,'B#``':'C'  } #[0   45     b]# 4/9
#     I2N, I4N         = [None, I2S, I2F],  [None, I4S, I4F]
    # IS0,  IS1,  IS2  = [2, 7, 9],  [1, 3, 6, 8, 10],  [0, 4, 5, 11]
    # FLAT, NTRL, SHRP =    -1,      0,      1    # -1 ~= 2
    # TYPES            =          [ 'NTRL', 'SHRP', 'FLAT' ] # 0=NTRL, 1=SHRP, 2=FLAT=-1
    # TYPE, NTONES     = SHRP, len(V2I) # - 1

    # @staticmethod
    # def setType(t):           Notes.TYPE = t
    # @staticmethod
    # def index(n, o=0):        name = n[:len(n)-1] if o else n  ;  return Notes.N2I[name]
    # @staticmethod
    # def nextIndex(i, d=1):    return  (i+d) % Notes.NTONES
    # @staticmethod
    # def name(i, t=0, n2=0):   t = t if t else Notes.TYPE  ;  return Notes.I4N[t][i % Notes.NTONES] if n2 else Notes.I2N[t][i % Notes.NTONES]
    # @staticmethod
    # def nextName(n, iv, o=0): i = Notes.index(n, o)  ;  j = Notes.V2I[iv]  ;  k = Notes.nextIndex(i, j)  ;  return Notes.name(k)
########################################################################################################################################################################################################
# class NotesA(object): #     1       2       3       4       5       6       7       8       9       a       b       0      #[  2    7 9  ]#
#     I2F = {         0:'C' , 1:'Db', 2:'D' , 3:'Eb', 4:'E' , 5:'F' , 6:'Gb', 7:'G' , 8:'Ab', 9:'A' ,10:'Bb', 11:'B' } # ,12:'C' } # 8/12/16
#     I2S = {         0:'C' , 1:'C#', 2:'D' , 3:'D#', 4:'E' , 5:'F' , 6:'F#', 7:'G' , 8:'G#', 9:'A' ,10:'A#', 11:'B' } # ,12:'C' } # 8/12/16
#     I4F = {         0:'C' , 1:'Db', 2:'D' , 3:'Eb', 4:'Fb', 5:'F' , 6:'Gb', 7:'G' , 8:'Ab', 9:'A' ,10:'Bb', 11:'Cb'} # ,12:'C' } # 8/12/16
#     I4S = { 0:'B#',         1:'C#', 2:'D' , 3:'D#', 4:'E' , 5:'E#', 6:'F#', 7:'G' , 8:'G#', 9:'A' ,10:'A#', 11:'B' } # ,12:'C' } # 8/12/16
#     I2V = {         0:'R' , 1:'b2', 2:'2' , 3:'m3', 4:'M3', 5:'4' , 6:'b5', 7:'5' , 8:'#5', 9:'6' ,10:'b7', 11:'7' } # ,12:'R' } # 8/12/16
#     I4V = {         0:'P1', 1:'m2', 2:'M2', 3:'m3', 4:'M3', 5:'P4', 6:'TT', 7:'P5', 8:'m6', 9:'M6',10:'m7', 11:'M7'} # ,12:'P8'} # 8/12/16
#     I6V = {         0:'d2', 1:'A1', 2:'d3', 3:'A2', 4:'d4', 5:'A3', 6:'TT', 7:'d6', 8:'A5', 9:'d7',10:'A6', 11:'d8'} # ,12:'A7'} # 8/12/16
#     V2I = {         'R':0 ,'b2':1, '2':2 , 'm3':3, 'M3':4, '4':5 , 'b5':6, '5':7 , '#5':8, '6':9 ,'b7':10,  '7':11 } # ,'R`':12 } # 8/12/16
#     N2I = {'B#':0, 'C' :0, 'C#':1, 'Db':1, 'D' :2, 'D#':3, 'Eb':3, 'E' :4, 'Fb':4, 'E#':5, 'F' :5, 'F#':6, 'Gb':6, 'G' :7, 'G#':8, 'Ab':8, 'A' :9, 'A#':10, 'Bb':10, 'B' :11, 'Cb' :11, 'B#`':12, 'C`':12 } #21
# #              0       0       1       2       3       4       5       6       7       8       9        a       b      0
#     F2S = {            'Db':'C#', 'Eb':'D#',                       'Gb':'F#', 'Ab':'G#', 'Bb':'A#'                        } #[ 1 3  6 8 a ]# 5/9
#     S2F = {            'C#':'Db', 'D#':'Eb',                       'F#':'Gb', 'G#':'Ab', 'A#':'Bb'                        } #[ 1 3  6 8 a ]# 5/9
#     F4S = { 'C' :'B#',                       'Fb':'E' , 'F' :'E#',                                  'Cb':'B' } #,'C``' :'B#' } #[0   45     b]# 4/9
#     S4F = { 'B#':'C' ,                       'E' :'Fb', 'E#':'F' ,                                  'B' :'Cb'} #,'B#``':'C'  } #[0   45     b]# 4/9
    # I2N, I4N         = [None, I2S, I2F],  [None, I4S, I4F]
    # IS0,  IS1,  IS2  = [2, 7, 9],  [1, 3, 6, 8, 10],  [0, 4, 5, 11]
    # FLAT, NTRL, SHRP =    -1,      0,      1    # -1 ~= 2
    # TYPES            =          [ 'NTRL', 'SHRP', 'FLAT' ] # 0=NTRL, 1=SHRP, 2=FLAT=-1
    # TYPE, NTONES     = FLAT, len(V2I) # - 1

    # @staticmethod
    # def setType(t):         NotesA.TYPE = t
    # @staticmethod
    # def index(n, o=0):      name = n[:len(n)-1] if o else n  ;  return NotesA.N2I[name]
    # @staticmethod
    # def nextIndex(i, d=1):  return  (i + d) % NotesA.NTONES
    # @staticmethod
    # def name(i, t=0, n2=0): t = t if t else NotesA.TYPE       ;  return NotesA.I4N[t][i % NotesA.NTONES] if n2 else NotesA.I2N[t][i % NotesA.NTONES]
    # @staticmethod
    # def nextName(n, iv, o=0): i = NotesA.index(n, o)  ;  j = NotesA.V2I[iv]  ;  k = NotesA.nextIndex(i, j)  ;  return NotesA.name(k)
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
def initND():
#    notes = Notes if ntype == Notes else NotesA
#    return { i:[ notes.I2F[i], notes.I2S[i], notes.I2V[i], notes.I4V[i], notes.I6V[i] ] for i in range(notes.NTONES) }
    return {i: [Notes.I2F[i], Notes.I2S[i], Notes.I2V[i], Notes.I4V[i], Notes.I6V[i]] for i in range(Notes.NTONES)}
ND = initND()
########################################################################################################################################################################################################
FLATS  = [ f'{v}{n}' for n in range(11) for v in Notes.I4F.values() ][:MAX_FREQ_IDX]
SHRPS  = [ f'{v}{n}' for n in range(11) for v in Notes.I4S.values() ][:MAX_FREQ_IDX]

def FREQ( index): return 440 * pow(pow(2, 1/Notes.NTONES), index - 57)
def FREQ2(index): return 432 * pow(pow(2, 1/Notes.NTONES), index - 57)

FREQS   = [ FREQ( i) for i in range(MAX_FREQ_IDX) ]
FREQS2  = [ FREQ2(i) for i in range(MAX_FREQ_IDX) ]
########################################################################################################################################################################################################
def Piano(c, d=1): (d, d2) = ("[", "]") if d else (Z, Z)  ;  return f'{"None":^17}' if c is None else f'{fmtl(c, w=3, d=d, d2=d2):17}'

def dumpNF(csv=0):
    w, d, m, n, f = (Z, Z, Y, Y, 3) if csv else ('^5', '[', W, Z, 1)
    slog('Note Frequencies in Hertz')  ;  nm = MAX_FREQ_IDX   ;   p, q = -8, 88+1   ;   g, h = 1, nm+1
    slog(f'Piano{n}{fmtl(list(range(p, q)),          w=w, d=d, s=m)}', p=0, f=f)
    slog(f'Index{n}{fmtl(list(range(g, h)),          w=w, d=d, s=m)}', p=0, f=f)
#   slog(f'Piano{n}{fmtl([ i for i in range(p, q) ], w=w, d=d, s=m)}', p=0, f=f)
#   slog(f'Index{n}{fmtl([ i for i in range(g, h) ], w=w, d=d, s=m)}', p=0, f=f)
    dumpFreqs(432, csv)    ;    dumpFreqs(440, csv)
    dumpWaves(432, csv)    ;    dumpWaves(440, csv)
    slog(f'Flats{n}{fmtl(list(FLATS),                w=w, d=d, s=m)}', p=0, f=f)
    slog(f'Shrps{n}{fmtl(list(SHRPS),                w=w, d=d, s=m)}', p=0, f=f)

def dumpFreqs(r=440, csv=0):
    m, f = (Y, 3) if csv else (W, 1)
    freqs = FREQS if r == 440 else FREQS2   ;   ref = '440A' if r == 440 else '432A'   ;   fs = []
    for freq in freqs:
        ft = fmtf(freq, 5)
        fs.append(f'{ft}')
    fs = m.join(fs)  ;  ref += m if csv else ' ['  ;  sfx = Z if csv else '] Hz'
    slog(f'{ref}{fs}{sfx}', p=0, f=f)

def dumpWaves(r=440, csv=0, v=340):
    m, f = (Y, 3) if csv else (W, 1)       ;   cmpm = 100
    freqs = FREQS if r == 440 else FREQS2   ;   ref = '440A' if r == 440 else '432A'   ;   ws = []
    for freq in freqs:
        w = cmpm * v/freq
        wt = fmtf(w, 5)
        ws.append(f'{wt}')
    ws = m.join(ws)  ;  ref += m if csv else ' ['  ;  sfx = Z if csv else '] cm'
    slog(f'{ref}{ws}{sfx}', p=0, f=f)
########################################################################################################################################################################################################
def dumpND(csv=0):
    w, d, m, f = (0, Z, Y, 3) if csv else (2, '[', W, 1)
    hdrs       = ['I', 'F', 'S', 'IV', 'mM', 'dA']
    hdrs       = f'{m.join([ f"{h:{w}}" for h in hdrs ])}'
    slog(f'{hdrs}', p=0, f=f)
    for i, (k, v) in enumerate(ND.items()):
        slog(f'{i:x}{m}{fmtl(v, w=w, d=d, s=m)}', p=0, f=f)
#    for i in range(len(ND)):   slog(f'{i:x}{m}{fmtl(ND[i], w=w, d=d, s=m)}', p=0, f=f)
########################################################################################################################################################################################################
def dumpKSV(csv=0):
    f = 3 if csv else 1
    dmpKSVHdr(csv)
    keys = sorted(KSD.keys())
    for k in keys:    slog(fmtKSK(k, csv), p=0, f=f)

def dmpKSVHdr(csv=0, t=0):
    c, d, m, n, o, f = (Z, Z, Y, Z, Z, 3)  if csv else ('^20', '^13', W, W, W*2, 1)
    k = 2*P+1 if t == 0 else M if t == Notes.FLAT else P if t == Notes.SHRP else 1
    fsn, fsi, ii, ino, kst = 'Flats/Shrps Naturals', 'F/S/N Indices', 'Ionian Indices', 'Ionian Note Ordering', f'Key Sig Table {signed(k)}'
    hdrs = ['KS', 'Type', 'N', f'{n}I', f'{n}{fsn:{c}}', f'{o}{fsi:{d}}', f'{o}{ii:{d}}', f'{n}{ino:{c}}', f'{n}{kst}']
    hdrs = m.join(hdrs)    ;    slog(hdrs, p=0, f=f)

def fmtKSK(k, csv=0):
    w, d, n = (0, Z, Y) if csv else (2, '[', W)
    t   = -1 if k < 0 else 1 if k > 0 else 0    ;   nt = Notes.TYPES[t]
    s   = signed(k)     ;   im = KSD[k][KIM]    ;    i = im[0]      ;    m = im[1]
    iz  = KSD[k][KIS]   ;   jz = KSD[k][KJS]    ;   ms = KSD[k][KMS]
    ns  = [ Notes.name(j, t, 0) for j in jz ]
#    ns  = [ Notes.name(j, t, 1 if abs(k) >= 5 else 0) for j in jz ]
    iz  = [ f'{i:x}' for i in iz ]
    jz  = [ f'{j:x}' for j in jz ]
    _ = [s, nt, f'{m:{w}}', f'{i:x}', fmtl(ms, w=w, d=d, s=n), fmtl(iz, d=d, s=n), fmtl(jz, d=d, s=n), fmtl(ns, w=w, d=d, s=n)]
    return n.join(_)

def dumpKSH(csv=0):
    c, y, ff   = (Z, Z, 3)    if csv else ('^20', W, 1)     ;  u, v, p = '<', 0, 0   ;   f, k, s = 'Flats', 'N', 'Shrps'
    w, d, m, n = (0, Z, Y, Y) if csv else (2, '[', W, W*2)  ;  v = W*v if v and Notes.TYPE==Notes.FLAT else Z
    hdrs = [ f'{y}{f:{c}}', f'{k:{w}}', f'{s:{c}}' ]        ;  hdrs = m.join(hdrs)   ;   slog(hdrs, p=p, f=ff)
    keys = sorted(KSD.keys())  ;  w = f'{u}{w}' ;   x = f'{w}x'
    _  = utl.ns2signs(keys)    ;  _ = n.join(_) ;   slog(f'{v}{y}{_}', p=p, f=ff)    ;  slog(f'{v}{fmtl(list(map(abs, keys)), w=w, d=d, s=m)}', p=p, f=ff)
    _  = [ KSD[k][KIM][KSK]    for k in keys ]  ;   slog(f'{v}{fmtl(_, w=x, d=d, s=m)}', p=p, f=ff)
    _  = [ KSD[k][KIM][KST]    for k in keys ]  ;   slog(f'{v}{fmtl(_, w=w, d=d, s=m)}', p=p, f=ff)   ;  y = Z if csv else W*2
    f  = [ KSD[M][KMS][f]      for f in range(len(KSD[M][KMS])-1, -1, -1) ]  ;  s = [ KSD[P][KMS][s]    for s in range(len(KSD[P][KMS])) ]
    fs = []  ;  fs.extend(f)   ;  fs.append(y)  ;   fs.extend(s)   ;   slog(f'{v}{fmtl(fs, w=w, d=d, s=m)}', p=p, f=ff)
    f  = [ f'{f:x}' for f in reversed(KSD[M][KIS]) ]   ;   s = [ f'{s:x}' for s in KSD[P][KIS] ]
    fs = []  ;  fs.extend(f)   ;  fs.append(y)  ;   fs.extend(s)   ;   slog(f'{v}{fmtl(fs, w=w, d=d, s=m)}', p=p, f=ff)
########################################################################################################################################################################################################
def nic2KS(nic, dbg=0):
    if dbg: dumpKSV()   ;   dumpKSH()   ;   dumpNic(nic)
    iz  = []          ;     t  = Notes.TYPE   ;   nt = Notes.TYPES[t]
    ks  = KSD[M][KIS]    if t == Notes.FLAT else KSD[P][KIS]
    for i in ks:
        if i in nic:     iz.append(f'{i:x}')
        else:            break
    k   = -len(iz)       if t == Notes.FLAT else len(iz)
    n   = KSD[k][KIM][KST] if iz else '??'
    i   = KSD[k][KIM][KSK]
    ns  = KSD[k][KMS]
    slog(fmtKSK(k))      if dbg else None
    return k, nt, n, i, ns, Scales.majIs(i)

def dumpNic(nic): #fix me
    slog(f'{fmtl([ f"{i:x}:{Notes.I2F[i]:2}:{nic[i]}" for i in nic.keys() ], s=Y)}')
    slog(f'{fmtl([ f"{i:x}:{Notes.I2S[i]:2}:{nic[i]}" for i in nic.keys() ], s=Y)}')
    slog(f'{fmtl([ f"{i:x}:{Notes.I2F[i]:2}:{nic[i]}" if  i in nic and nic[i] > 0 else None for i in KSD[M][KIS] ], s=Y)}')
    slog(f'{fmtl([ f"{i:x}:{Notes.I2F[i]:2}:{nic[i]}" if  i in nic and nic[i] > 0 else None for i in KSD[P][KIS] ], s=Y)}')
########################################################################################################################################################################################################
def initKSD(ks, t):
    if     t == -1:   i = 0  ;  j = 6   ;  s = M
    else:             i = 0  ;  j = 10  ;  s = P
    iz1 = [ (j + k * s) % Notes.NTONES for k in range(1, 1+abs(s)) ]
    ms1 = []
    for j in iz1:
        name = Notes.name(j, t, 0)
        ms1.append(name)
#    ms1 = [ Notes.name(j, t)           for j in iz1 ]
    iz2 = list(iz1)          ;         ms2 = list(ms1)
    slog(f'{t=} {i=} {j=} {s=} {fmtl(iz2)=} {fmtl(ms2)=}', p=0)   ;   j += t
    for  k in range(0, t + s, t):
        ak = abs(k)
        m  =   Notes.name(i, t, 1 if ak >= 5 else 0)
        n  =   Notes.name(j, t, 1 if ak >= 5 else 0)
        if ak >= 1:   ms2[ak-1] = n  ;  iz2[ak-1] = j   ;  ms = list(ms2)  ;  iz = list(iz2)
        else:                                              ms = list(ms2)  ;  iz = list(iz2)
        jz = Scales.majIs(i)    ;    im  = [i, m]
        ns = [ Notes.name(j, t, 1 if ak >= 5 else 0) for j in jz ]
        ks[k]  =  [ im, iz, ms, jz, ns ]
        slog(fmtKSK(k, csv=1), p=0)
        i  =   Notes.nextIndex(i, s)
        j  =   Notes.nextIndex(j, s)
    return ks
########################################################################################################################################################################################################
KSD = {}
KIM, KIS, KMS, KJS, KNS        = range(5)
KSK, KST, KSN, KSI, KSMS, KSSI = range(6)
dmpKSVHdr(csv=1,   t=-1)
KSD = initKSD(KSD, t=-1)
KSD = initKSD(KSD, t= 1)
dmpKSVHdr(csv=1,   t= 1)
dumpKSH(  csv=1)
