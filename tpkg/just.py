from tpkg       import utl
#from tpkg       import notes
from tpkg.notes import Notes
from tpkg       import intrvls as ivls

W, Y, Z       = utl.W,      utl.Y,     utl.Z
slog, ist     = utl.slog,   utl.ist
fmtf, fmtg    = utl.fmtf,   utl.fmtg
fmtl, fmtm    = utl.fmtl,   utl.fmtm

CM_P_M        = ivls.CM_P_M
V_SOUND       = ivls.V_SOUND
A4_INDEX      = ivls.A4_INDEX
NT            = ivls.NT

F440s, F432s  = ivls.F440s, ivls.F432s
i2spr         = ivls.i2spr
i2nPair       = ivls.i2nPair
#addFmtRs      = ivls.addFmtRs

'''
     3^-2    3^-1  3^0 3^1 3^2
5^1  5/3^2   5/3   5/1 3*5 3^2*5^2
5^0  1/3^2   1/3   1/1 1*3 1*3^2
5^-1 1/5*3^2 1/5*3 1/5 3/5 3^2/5

     1/9  1/3   1   3   9
 5   5/9  5/3   5  15  45 
 1   1/9  1/3   1   3   9
1/5  1/45 1/15 1/5 3/5 9/5

     1/9   1/3   1   3   9
 5   10/9  5/3  5/4 15/8 45/32
 1   16/9  4/3   1   3/2  9/8
1/5 64/45 16/15 8/5  6/5  9/5

C  [     1     |     0     |    -1     ]
D  [    -2     |    -1     |     0     |     1     |     2     ]
C A[     5     |     1     |    1/5    ]
D B[    1/9    |    1/3    |     1     |     3     |     9     ]
         0           1           2           3           4           5           6           7           8           9          10          11          12          13          14     
r0s[ 0.5555556 | 1.666667  |     5     |    15     |    45     | 0.1111111 | 0.3333333 |     1     |     3     |     9     |0.02222222 |0.06666667 |    0.2    |    0.6    |    1.8    ]
r1s[    5/9    |    5/3    |    5/1    |    5*3    |    5*9    |    1/9    |    1/3    |    1/1    |    1*3    |    1*9    |   1/45    |   1/15    |    1/5    |    3/5    |    9/5    ]
r2s[  5^1/3^2  |  5^1/3^1  |  5^1*3^0  |  5^1*3^1  |  5^1*3^2  |  5^0/3^2  |  5^0/3^1  |  5^0*3^0  |  5^0*3^1  |  5^0*3^2  |1/(5^1*3^2)|1/(5^1*3^1)|  3^0/5^1  |  3^1/5^1  |  3^2/5^1  ]
r3s[   5¹/3²   |   5¹/3¹   |   5¹*3⁰   |   5¹*3¹   |   5¹*3²   |   5⁰/3²   |   5⁰/3¹   |   5⁰*3⁰   |   5⁰*3¹   |   5⁰*3²   | 1/(5¹*3²) | 1/(5¹*3¹) |   3⁰/5¹   |   3¹/5¹   |   3²/5¹   ]

r0s[ 1.111111  | 1.666667  |   1.25    |   1.875   |  1.40625  | 1.777778  | 1.333333  |     1     |    1.5    |   1.125   | 1.422222  | 1.066667  |    1.6    |    1.2    |    1.8    ]
r1s[   10/9    |    5/3    |    5/4    |   15/8    |   45/32   |   16/9    |    4/3    |    1/1    |    3/2    |    9/8    |   64/45   |   16/15   |    8/5    |    6/5    |    9/5    ]
'''
A, B = 5, 3
C    = [  1,  0, -1 ]
D    = [ -2, -1,  0, 1, 2 ]
R1   = [ A**C[0] * B**D[0], A**C[0] * B**D[1], A**C[0] * B**D[2], A**C[0] * B**D[3], A**C[0] * B**D[4] ]
R2   = [ A**C[1] * B**D[0], A**C[1] * B**D[1], A**C[1] * B**D[2], A**C[1] * B**D[3], A**C[1] * B**D[4] ]
R3   = [ A**C[2] * B**D[0], A**C[2] * B**D[1], A**C[2] * B**D[2], A**C[2] * B**D[3], A**C[2] * B**D[4] ]
CRS  = [ R1, R2, R3 ]
########################################################################################################################################################################################################
#def fmtR0(a, ca, b, cb, w):       pa = float(a ** ca)  ;  pb = float(b ** abs(cb)) if cb < 0 else float(b ** cb)   ;  return f'{pa/pb:{w}}' if cb < 0 else f'{pa*pb:{w}}'
def fmtR0(a, ca, b, cb, w, k=0):
    pa = a ** ca  ;  pb = b ** abs(cb)   ;   p = 2 ** k
    v = p*pa/pb if cb < 0 else p*pa*pb #  ;   u = f'^{w}.{w-4}f' if ist(v, float) else f'^{w}'
    return f'{v:^{w}.{w-4}}' if ist(v, float) else f'{v:^{w}}' # if cb < 0 else f'{v:{u}}'

#def fmtR1(a, ca, b, cb, w):
#    pa = a ** abs(ca) if ca < 0 else a ** ca  ;  pb = b ** abs(cb) if cb < 0 else b ** cb  ;  papbi = f'1/({pa}*{pb})'
#    return f'{pa:>{w}}*{pb:<{w}}' if ca >= 0 <= cb else f'{pa:>{w}}/{pb:<{w}}' if ca >= 0 > cb else f'{pb:>{w}}/{pa:<{w}}' if ca < 0 <= cb else f'{papbi:^{2*w+1}}' if ca < 0 > cb else f'?#?#?'
def fmtR1(a, ca, b, cb, w, k, i, j):
    pa = a ** abs(ca)  ;  pb = b ** abs(cb)  ;  l = 2 ** abs(k)  ;  papbi = f'{l}/{pa*pb}'
    if k == 0:
        ret = f'{pa:>{w}}*{pb:<{w}}' if ca >= 0 < cb else f'{pa:>{w}}/{pb:<{w}}' if ca >= 0 >= cb else f'{pb:>{w}}/{pa:<{w}}' if ca < 0 <= cb else f'{papbi:^{2*w+1}}' if ca < 0 > cb else f'?#?#?'
        slog(f'{i} {j} {k:2} {l:2} {a} {ca:2} {b} {cb:2} {ret=}')  ;  return ret
    if   k > 0:
        pa = pa * l if ca >= 0 <= cb or ca >= 0 > cb else pa  ;  pb = pb * l if ca < 0 <= cb else pb
        ret = f'{pa:>{w}}*{pb:<{w}}' if ca >= 0 < cb else f'{pa:>{w}}/{pb:<{w}}' if ca >= 0 >= cb else f'{pb:>{w}}/{pa:<{w}}' if ca < 0 <= cb else f'{papbi:^{2*w+1}}' if ca < 0 > cb else f'?#?#?'
        slog(f'{i} {j} {k:2} {l:2} {a} {ca:2} {b} {cb:2} {ret=}')  ;  return ret
    elif k < 0:
        if   ca >= 0:  ret = f'{pa*pb:>{w}}/{l:<{w}}'  ;  slog(f'{i} {j} {k:2} {l:2} {a} {ca:2} {b} {cb:2} {ret=}')  ;  return ret

def fmtR2(a, ca, b, cb, w, k=0):
    qa = f'{a}^{abs(ca)}' if ca < 0 else f'{a}^{ca}'  ;  qb = f'{b}^{abs(cb)}' if cb < 0 else f'{b}^{cb}'  ;  qaqbi = f'1/({qa}*{qb})'
    return f'{qa:>{w}}*{qb:<{w}}' if ca >= 0 <= cb else f'{qa:>{w}}/{qb:<{w}}' if ca >= 0 > cb else f'{qb:>{w}}/{qa:<{w}}' if ca < 0 <= cb else f'{qaqbi:^{2*w+1}}' if ca < 0 > cb else f'?#?#?'

def fmtR3(a, ca, b, cb, w, k=0): 
    sa = f'{a}{i2spr(abs(ca))}' if ca < 0 else f'{a}{i2spr(ca)}'  ;  sb = f'{b}{i2spr(abs(cb))}' if cb < 0 else f'{b}{i2spr(cb)}'  ;  sasbi = f'1/({sa}*{sb})'
    return f'{sa:>{w}}*{sb:<{w}}' if ca >= 0 <= cb else f'{sa:>{w}}/{sb:<{w}}' if ca >= 0 > cb else f'{sb:>{w}}/{sa:<{w}}' if ca < 0 <= cb else f'{sasbi:^{2*w+1}}' if ca < 0 > cb else f'?#?#?'

#def fmtRA(a, ca, w=Z):        pa     =   a ** ca                             ;  return f'{pa:{w}}'
#def fmtRB(b, cb, w=Z):        pb     =   b ** cb                             ;  return f'{pb:{w}}'
#def fdvdr(a, ca, b, cb):      n = max(len(fmtRA(a, ca)), len(fmtRB(b, cb)))  ;  return n * '/'

def addFmtRs(i, j, k, r0s, r1s, r2s, r3s, a, ca, b, cb, u=5, w=11):
#   rAs.append(fmtRA(a, ca, ww if ist(a**ca, int) else w3))
#   rBs.append(fmtRB(b, cb, ww if ist(b**cb, int) else w3))
    r0s.append(fmtR0(a, ca, b, cb, w, k))
    r1s.append(fmtR1(a, ca, b, cb, u, k, i, j))
    r2s.append(fmtR2(a, ca, b, cb, u, k)) if u >= 5 else None
    r3s.append(fmtR3(a, ca, b, cb, u, k))
########################################################################################################################################################################################################
def fmtis(l, v=0, w=11, csv=0):
    mm = Y if csv else '|'    ;    ret = []
    for i, e in enumerate(l):
        if   not v and ist(      e, int):  _ =         e    ;  ret.append(f'{_:^{w}}')
        elif     v and ist(v **  e, int):  _ =      v**e    ;  ret.append(f'{_:^{w}}')
        elif     v and ist(v ** -e, int):  _ = f'1/{v**-e}' ;  ret.append(f'{_:^{w}}')
        else:                              assert 0,  f'{v=} {i=} {l=} {l[i]=} {e=} {type(e)=} {v**e=} {type(v**e)=} {v**-e=} {type(v**-e)=}'
    return fmtl(ret, s=mm) # W.join(fmtl(ret))
########################################################################################################################################################################################################
def dumpData(csv=0):
    slog(f'BGN {csv=}', p=0)
    dmpData('C', csv=csv)
    slog(f'END {csv=}', p=0)

def dmpData(n='C', csv=0):
    k = Notes.N2I[n] + 48
    dmpJust(k, rf=440, sss=V_SOUND, csv=csv)
########################################################################################################################################################################################################
def dmpJust(k, rf=440, sss=V_SOUND, csv=0):
    mm, nn, oo, ff = (Y, Y, Y, 3) if csv else (W, Z, '|', 1)   ;   x, y, z = 11, 9, 5   ;   w = f'^{x}' #  ;   w2 = f'^{x}.{y}'
    slog(f'BGN Just Tone Series ({k=} {rf=} {sss=} {csv=})', p=0, f=ff)
    r0s, r1s, r2s, r3s = [], [], [], []   ;   a, b = 5, 3
    slog(f'C  {fmtis(C,    w=x, csv=csv)}', p=0, f=ff)
    slog(f'D  {fmtis(D,    w=x, csv=csv)}', p=0, f=ff)
    slog(f'C A{fmtis(C, A, w=x, csv=csv)}', p=0, f=ff)
    slog(f'D B{fmtis(D, B, w=x, csv=csv)}', p=0, f=ff)
    ii = [ f'{i}' for i in range(len(C) * len(D)) ]
    slog(f'    {fmtl(ii, w=w, s=mm, d=Z)}', p=0, f=ff)
    for     i, c in enumerate(C):
        for j, d in enumerate(D):
            addFmtRs(i, j, 0, r0s, r1s, r2s, r3s, a, c, b, d, z)
    slog(f'r0s{fmtl(r0s, w=w, s=oo)}', p=0, f=ff)
    slog(f'r1s{fmtl(r1s, w=w, s=oo)}', p=0, f=ff)
    slog(f'r2s{fmtl(r2s, w=w, s=oo)}', p=0, f=ff)
    slog(f'r3s{fmtl(r3s, w=w, s=oo)}', p=0, f=ff)
    for     i, c in enumerate(C):
        for j, d in enumerate(D):
            n = fmtNote(k+i, j)
            u = CRS[i][j]
            v, p = ivls.norm(u)
            slog(f'{i} {j}: {a}^{c:2} * {b}^{d:2} = {u:7.4f} * 2^{p:2} = {v:7.5f} : {n=:2}', p=0, f=ff)
    r0s, r1s, r2s, r3s = [], [], [], []
    for     i, c in enumerate(C):
        for j, d in enumerate(D):
            u = CRS[i][j]
            v, p = ivls.norm(u)
            addFmtRs(i, j, p, r0s, r1s, r2s, r3s, a, c, b, d, z)
    slog(f'r0s{fmtl(r0s, w=w, s=oo)}', p=0, f=ff)
    slog(f'r1s{fmtl(r1s, w=w, s=oo)}', p=0, f=ff)
    slog(f'r2s{fmtl(r2s, w=w, s=oo)}', p=0, f=ff)
    slog(f'r3s{fmtl(r3s, w=w, s=oo)}', p=0, f=ff)
    slog(f'END Just Tone Series ({k=} {rf=} {sss=} {csv=})', p=0, f=ff)
########################################################################################################################################################################################################
def fmtNote(k, i):
    n1, n2   = i2nPair(k + i, s=1)
    return n1
########################################################################################################################################################################################################
def fJTS(i, r=440):
    f0 = F440s[0] if r==440 else F432s[0]  ;  return f0 * i

