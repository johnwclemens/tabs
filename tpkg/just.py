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
########################################################################################################################################################################################################
C  [     1     |     0     |    -1     ]
D  [    -2     |    -1     |     0     |     1     |     2     ]
C A[     5     |     1     |    1/5    ]
D B[    1/9    |    1/3    |     1     |     3     |     9     ]
         0           1           2           3           4           5           6           7           8           9          10          11          12          13          14     
r0s[ 0.5555556 | 1.6666667 |     5     |    15     |    45     | 0.1111111 | 0.3333333 |     1     |     3     |     9     | 0.0222222 | 0.0666667 | 0.2000000 | 0.6000000 | 1.8000000 ]
r1s[    5/9    |    5/3    |    5/1    |    5*3    |    5*9    |    1/9    |    1/3    |    1/1    |    1*3    |    1*9    |   1/45    |   1/15    |    1/5    |    3/5    |    9/5    ]
r2s[    5/3^2  |    5/3    |    5/1    |    5*3    |    5*3^2  |    1/3^2  |    1/3    |    1/1    |    1*3    |    1*3^2  | 1/(5*3^2) |  1/(5*3)  |    1/5    |    3/5    |  3^2/5    ]
r3s[   5¹/3²   |   5¹/3¹   |   5¹/3⁰   |   5¹*3¹   |   5¹*3²   |   5⁰/3²   |   5⁰/3¹   |   5⁰/3⁰   |   5⁰*3¹   |   5⁰*3²   | 1/(5¹*3²) | 1/(5¹*3¹) |   3⁰/5¹   |   3¹/5¹   |   3²/5¹   ]
0 0: 5^ 1 * 3^-2 =  0.5556 * 2^ 1 = 1.11111 : n=D 
0 1: 5^ 1 * 3^-1 =  1.6667 * 2^ 0 = 1.66667 : n=A 
0 2: 5^ 1 * 3^ 0 =  5.0000 * 2^-2 = 1.25000 : n=E 
0 3: 5^ 1 * 3^ 1 = 15.0000 * 2^-3 = 1.87500 : n=B 
0 4: 5^ 1 * 3^ 2 = 45.0000 * 2^-5 = 1.40625 : n=F♯
1 0: 5^ 0 * 3^-2 =  0.1111 * 2^ 4 = 1.77778 : n=B♭
1 1: 5^ 0 * 3^-1 =  0.3333 * 2^ 2 = 1.33333 : n=F 
1 2: 5^ 0 * 3^ 0 =  1.0000 * 2^ 0 = 1.00000 : n=C 
1 3: 5^ 0 * 3^ 1 =  3.0000 * 2^-1 = 1.50000 : n=G 
1 4: 5^ 0 * 3^ 2 =  9.0000 * 2^-3 = 1.12500 : n=D 
2 0: 5^-1 * 3^-2 =  0.0222 * 2^ 6 = 1.42222 : n=G♭
2 1: 5^-1 * 3^-1 =  0.0667 * 2^ 4 = 1.06667 : n=D♭
2 2: 5^-1 * 3^ 0 =  0.2000 * 2^ 3 = 1.60000 : n=A♭
2 3: 5^-1 * 3^ 1 =  0.6000 * 2^ 1 = 1.20000 : n=E♭
2 4: 5^-1 * 3^ 2 =  1.8000 * 2^ 0 = 1.80000 : n=B♭
r0s[ 1.1111111 | 1.6666667 | 1.2500000 | 1.8750000 | 1.4062500 | 1.7777778 | 1.3333333 |     1     | 1.5000000 | 1.1250000 | 1.4222222 | 1.0666667 | 1.6000000 | 1.2000000 | 1.8000000 ]
r1s[   10/9    |    5/3    |    5/4    |   15/8    |   45/32   |   16/9    |    4/3    |    1/1    |    3/2    |    9/8    |   64/45   |   16/15   |    8/5    |    6/5    |    9/5    ]
r2s[  2*5/3^2  |    5/3    |   5*1/4   |   5*3/8   | 5*3^2/32  | 16*1/3^2  |   4*1/3   |    1/1    |   1*3/2   |  1*3^2/8  |64/(5*3^2) | 16/(5*3)  |   8*1/5   |   2*3/5   |  3^2/5    ]
r3s[  2*5¹/3²  |   5¹/3¹   |  5¹*3⁰/4  |  5¹*3¹/8  | 5¹*3²/32  | 16*5⁰/3²  |  4*5⁰/3¹  |   5⁰/3⁰   |  5⁰*3¹/2  |  5⁰*3²/8  |64/(5¹*3²) |16/(5¹*3¹) |  8*3⁰/5¹  |  2*3¹/5¹  |   3²/5¹   ]
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

#def fmtR1(a, ca, b, cb, w):
#    pa = a ** abs(ca) if ca < 0 else a ** ca  ;  pb = b ** abs(cb) if cb < 0 else b ** cb  ;  papbi = f'1/({pa}*{pb})'
#    return f'{pa:>{w}}*{pb:<{w}}' if ca >= 0 <= cb else f'{pa:>{w}}/{pb:<{w}}' if ca >= 0 > cb else f'{pb:>{w}}/{pa:<{w}}' if ca < 0 <= cb else f'{papbi:^{2*w+1}}' if ca < 0 > cb else f'?#?#?'

#def fmtR2(a, ca, b, cb, w):
#    qa = f'{a}^{abs(ca)}' if ca < 0 else f'{a}^{ca}'  ;  qb = f'{b}^{abs(cb)}' if cb < 0 else f'{b}^{cb}'  ;  qaqbi = f'1/({qa}*{qb})'
#    return f'{qa:>{w}}*{qb:<{w}}' if ca >= 0 <= cb else f'{qa:>{w}}/{qb:<{w}}' if ca >= 0 > cb else f'{qb:>{w}}/{qa:<{w}}' if ca < 0 <= cb else f'{qaqbi:^{2*w+1}}' if ca < 0 > cb else f'?#?#?'

#def fmtR3(a, ca, b, cb, w):
#    sa = f'{a}{i2spr(abs(ca))}' if ca < 0 else f'{a}{i2spr(ca)}'  ;  sb = f'{b}{i2spr(abs(cb))}' if cb < 0 else f'{b}{i2spr(cb)}'  ;  sasbi = f'1/({sa}*{sb})'
#    return f'{sa:>{w}}*{sb:<{w}}' if ca >= 0 <= cb else f'{sa:>{w}}/{sb:<{w}}' if ca >= 0 > cb else f'{sb:>{w}}/{sa:<{w}}' if ca < 0 <= cb else f'{sasbi:^{2*w+1}}' if ca < 0 > cb else f'?#?#?'
########################################################################################################################################################################################################
def fmtR0(a, ca, b, cb, w, k=0):
    pa = a ** ca  ;  pb = b ** abs(cb)  ;  p = 2 ** k
    v = p*pa/pb if cb < 0 else p*pa*pb
    return f'{v:^{w}.{w-4}f}' if ist(v, float) else f'{v:^{w}}'
########################################################################################################################################################################################################
def fmtR1(a, ca, b, cb, w, k, i, j):
    pa = a ** abs(ca)  ;  pb = b ** abs(cb)  ;  l = 2 ** abs(k)  ;  papbi = f'{l}/{pa*pb}'  ;  ret = Z  ;  dbg = 0
    if k == 0:
        ret = f'{pa:>{w}}*{pb:<{w}}' if ca >= 0 < cb else f'{pa:>{w}}/{pb:<{w}}' if ca >= 0 >= cb else f'{pb:>{w}}/{pa:<{w}}' if ca < 0 <= cb else f'{papbi:^{2*w+1}}' if ca < 0 > cb else f'?#?#?'
    elif k > 0:
        pa = pa * l if ca >= 0 <= cb or ca >= 0 > cb else pa  ;  pb = pb * l if ca < 0 <= cb else pb
        ret = f'{pa:>{w}}*{pb:<{w}}' if ca >= 0 < cb else f'{pa:>{w}}/{pb:<{w}}' if ca >= 0 >= cb else f'{pb:>{w}}/{pa:<{w}}' if ca < 0 <= cb else f'{papbi:^{2*w+1}}' if ca < 0 > cb else f'?#?#?'
    elif k < 0:
        if   ca >= 0:  ret = f'{pa*pb:>{w}}/{l:<{w}}'  ;  ret = f'{ret:^{2*w+1}}'
    slog(f'{i} {j} {k:2} {l:2} {a} {ca:2} {b} {cb:2} {ret=}') if dbg else None  ;  return ret
########################################################################################################################################################################################################
def fmtR2(a, ca, b, cb, w, k, i, j):
    qa = f'1' if ca == 0 else f'{a}' if ca == 1 else f'{a}' if ca == -1 else f'{a}^{abs(ca)}'
    qb = f'1' if cb == 0 else f'{b}' if cb == 1 else f'{b}' if cb == -1 else f'{b}^{abs(cb)}' 
    l = 2 ** abs(k)  ;  qaqbi = f'{l}/({qa}*{qb})'  ;  ret = Z  ;  dbg = 0
    if k == 0:
        ret = f'{qa:>{w}}*{qb:<{w}}' if ca >= 0 < cb else f'{qa:>{w}}/{qb:<{w}}' if ca >= 0 >= cb else f'{qb:>{w}}/{qa:<{w}}' if ca < 0 <= cb else f'{qaqbi:^{2*w+1}}' if ca < 0 > cb else f'?#?#?'
    elif k > 0:
        qa = f'{l}*{qa}' if ca >= 0 <= cb or ca >= 0 > cb else qa  ;  qb = f'{l}*{qb}' if ca < 0 <= cb else qb
        ret = f'{qa:>}*{qb:<}' if ca >= 0 < cb else f'{qa:>}/{qb:<}' if ca >= 0 >= cb else f'{qb:>}/{qa:<}' if ca < 0 <= cb else f'{qaqbi}' if ca < 0 > cb else f'?#?#?'  ;  ret = f'{ret:^{2*w+1}}'
    elif k < 0:
        if   ca >= 0:  ret = f'{qa:>}*{qb}/{l:<}'  ;  ret = f'{ret:^{2*w+1}}'
    slog(f'{i} {j} {k:2} {l:2} {a} {ca:2} {b} {cb:2} {ret=}') if dbg else None  ;  return ret
########################################################################################################################################################################################################
def fmtR3(a, ca, b, cb, w, k, i, j):
    l = 2 ** abs(k)  ;  sa = f'{a}{i2spr(abs(ca))}'  ;  sb = f'{b}{i2spr(abs(cb))}'  ;  sasbi = f'1/({sa}*{sb})'  ;  ret = Z  ;  dbg = 0
    if   k == 0:
        ret = f'{sa:>{w}}*{sb:<{w}}' if ca >= 0 < cb else f'{sa:>{w}}/{sb:<{w}}' if ca >= 0 >= cb else f'{sb:>{w}}/{sa:<{w}}' if ca < 0 <= cb else f'{sasbi:^{2*w+1}}' if ca < 0 > cb else f'?#?#?'
    elif k > 0:
        sa = f'{l}*{sa}' if ca >= 0 <= cb or ca >= 0 > cb else sa  ;  sb = f'{l}*{sb}' if ca < 0 <= cb else sb  ;  sasbi = f'{l}/({sa}*{sb})'
        ret = f'{sa:>}*{sb:<}' if ca >= 0 <= cb else f'{sa:>}/{sb:<}' if ca >= 0 > cb else f'{sb:>}/{sa:<}' if ca < 0 <= cb else f'{sasbi}' if ca < 0 > cb else f'?#?#?'  ;  ret = f'{ret:^{2*w+1}}'
    elif k < 0:
        if   ca >= 0:  ret = f'{sa:>}*{sb}/{l:<}'  ;  ret = f'{ret:^{2*w+1}}'
    slog(f'{i} {j} {k:2} {l:2} {a} {ca:2} {b} {cb:2} {ret=}') if dbg else None  ;  return ret
########################################################################################################################################################################################################
#def fmtRA(a, ca, w=Z):        pa     =   a ** ca                             ;  return f'{pa:{w}}'
#def fmtRB(b, cb, w=Z):        pb     =   b ** cb                             ;  return f'{pb:{w}}'
#def fdvdr(a, ca, b, cb):      n = max(len(fmtRA(a, ca)), len(fmtRB(b, cb)))  ;  return n * '/'
########################################################################################################################################################################################################
def addFmtRs(i, j, k, r0s, r1s, r2s, r3s, a, ca, b, cb, u=5, w=11):
#   rAs.append(fmtRA(a, ca, ww if ist(a**ca, int) else w3))
#   rBs.append(fmtRB(b, cb, ww if ist(b**cb, int) else w3))
    r0s.append(fmtR0(a, ca, b, cb, w, k))
    r1s.append(fmtR1(a, ca, b, cb, u, k, i, j))
    r2s.append(fmtR2(a, ca, b, cb, u, k, i, j)) if u >= 5 else None
    r3s.append(fmtR3(a, ca, b, cb, u, k, i, j))
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
    dmpData('D', csv=csv)
    slog(f'END {csv=}', p=0)

def dmpData(n='C', csv=0):
    k = Notes.N2I[n] + 48
    dmpJust(k, rf=440, sss=V_SOUND, csv=csv)
########################################################################################################################################################################################################
def dmpJust(k, rf=440, sss=V_SOUND, csv=0):
    mm, nn, oo, ff = (Y, Y, Y, 3) if csv else (W, Z, '|', 1)   ;   x, y, z = 11, 9, 5   ;   w = f'^{x}'  ;  M3 = Notes.V2I['M3']
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
        kk = k - i * M3
        for j, d in enumerate(D):
            n = fmtNote(kk, (j*7)%NT, b=0 if i==0 and j==4 else 1)
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
def fmtNote(k, i, b=1):
    n1, n2   = i2nPair(k + i, b=b, s=1)
    return n1
########################################################################################################################################################################################################
def fJTS(i, r=440):
    f0 = F440s[0] if r==440 else F432s[0]  ;  return f0 * i

