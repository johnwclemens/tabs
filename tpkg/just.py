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
'''
#JTS5_C0 = [ 5, 1, 1/5 ]
#JTS5_R0 = [ 1/9, 1/3, 1, 3, 9 ]
#JTS5_R1 = [ JTS5_C0[0] * JTS5_R0[0], JTS5_C0[0] * JTS5_R0[1], JTS5_C0[0] * JTS5_R0[2], JTS5_C0[0] * JTS5_R0[3], JTS5_C0[0] * JTS5_R0[4] ] # [5/9,  5/3,   5,  15,  45]
#JTS5_R2 = [ JTS5_C0[1] * JTS5_R0[0], JTS5_C0[1] * JTS5_R0[1], JTS5_C0[1] * JTS5_R0[2], JTS5_C0[1] * JTS5_R0[3], JTS5_C0[1] * JTS5_R0[4] ] # [1/9,  1/3,   1,   3,   9]
#JTS5_R3 = [ JTS5_C0[2] * JTS5_R0[0], JTS5_C0[2] * JTS5_R0[1], JTS5_C0[2] * JTS5_R0[2], JTS5_C0[2] * JTS5_R0[3], JTS5_C0[2] * JTS5_R0[4] ] # [1/45, 1/15, 1/5, 3/5, 9/5]
#JTS5    = [ JTS5_R1, JTS5_R2, JTS5_R3 ]
A, B = 5, 3
C    = [  1, 0, -1 ]
D    = [ -2, -1, 0, 1, 2 ]
R1   = [ A**C[0] * B**D[0], A**C[0] * B**D[1], A**C[0] * B**D[2], A**C[0] * B**D[3], A**C[0] * B**D[4] ]
R2   = [ A**C[1] * B**D[0], A**C[1] * B**D[1], A**C[1] * B**D[2], A**C[1] * B**D[3], A**C[1] * B**D[4] ]
R3   = [ A**C[2] * B**D[0], A**C[2] * B**D[1], A**C[2] * B**D[2], A**C[2] * B**D[3], A**C[2] * B**D[4] ]
CRS  = [ R1, R2, R3 ]
########################################################################################################################################################################################################
def fdvdr(a, ca, b, cb):      n = max(len(fmtRA(a, ca)), len(fmtRB(b, cb)))  ;  return n * '/'
def fmtR0(a, ca, b, cb, w):   pa, pb = float(a ** ca), float(b ** abs(cb)) if cb < 0 else float(b ** cb)   ;  return f'{pa/pb:{w}}' if cb < 0 else f'{pa*pb:{w}}'
def fmtR1(a, ca, b, cb, w):
    pa = a ** abs(ca) if ca < 0 else a ** ca  ;  pb = b ** abs(cb) if cb < 0 else b ** cb  ;  papbi = f'1/({pa}*{pb})'
    return f'{pa:>{w}}*{pb:<{w}}' if ca >= 0 <= cb else f'{pa:>{w}}/{pb:<{w}}' if ca >= 0 > cb else f'{pb:>{w}}/{pa:<{w}}' if ca < 0 <= cb else f'{papbi:^{2*w+1}}' if ca < 0 > cb else f'?#?#?'
def fmtRA(a, ca, w=Z):        pa     =   a ** ca                             ;  return f'{pa:{w}}'
def fmtRB(b, cb, w=Z):        pb     =   b ** cb                             ;  return f'{pb:{w}}'
def fmtR2(a, ca, b, cb, w): # qa, qb = f'{a}^{ca}'      , f'{b}^{cb}'        ;  return f'{qa:>{w}}*{qb:<{w}}'
    qa = f'{a}^{abs(ca)}' if ca < 0 else f'{a}^{ca}'  ;  qb = f'{b}^{abs(cb)}' if cb < 0 else f'{b}^{cb}'  ;  qaqbi = f'1/({qa}*{qb})'
    return f'{qa:>{w}}*{qb:<{w}}' if ca >= 0 <= cb else f'{qa:>{w}}/{qb:<{w}}' if ca >= 0 > cb else f'{qb:>{w}}/{qa:<{w}}' if ca < 0 <= cb else f'{qaqbi:^{2*w+1}}' if ca < 0 > cb else f'?#?#?'
def fmtR3(a, ca, b, cb, w): # sa, sb = f'{a}{i2spr(ca)}', f'{b}{i2spr(cb)}'  ;  return f'{sa:>{w}}*{sb:<{w}}' 
    sa = f'{a}{i2spr(abs(ca))}' if ca < 0 else f'{a}{i2spr(ca)}'  ;  sb = f'{b}{i2spr(abs(cb))}' if cb < 0 else f'{b}{i2spr(cb)}'  ;  sasbi = f'1/({sa}*{sb})'
    return f'{sa:>{w}}*{sb:<{w}}' if ca >= 0 <= cb else f'{sa:>{w}}/{sb:<{w}}' if ca >= 0 > cb else f'{sb:>{w}}/{sa:<{w}}' if ca < 0 <= cb else f'{sasbi:^{2*w+1}}' if ca < 0 > cb else f'?#?#?'
def addFmtRs(r0s, r1s, r2s, r3s, a, ca, b, cb, w3, u):
    r0s.append(fmtR0(a, ca, b, cb, w3))
    r1s.append(fmtR1(a, ca, b, cb, u))
#    rAs.append(fmtRA(a, ca, ww if ist(a**ca, int) else w3))
#    rBs.append(fmtRB(b, cb, ww if ist(b**cb, int) else w3))
    r2s.append(fmtR2(a, ca, b, cb, u)) # if u >= 9 else None
    r3s.append(fmtR3(a, ca, b, cb, u))
########################################################################################################################################################################################################
def fmtis(l, v=0):  #  return fmtl([ f'{e}' if ist(e, int) else f'{v**e}' if ist(v**e, int) else f'1/{v**-e}' for e in l ])
    ret = []
    for i, e in enumerate(l):
        if   not v and ist(      e, int):  ret.append(       f'{e}')
        elif     v and ist(v **  e, int):  ret.append(  f'{v ** e}')
        elif     v and ist(v ** -e, int):  ret.append(f'1/{v ** -e}')
        else:                              assert 0,  f'{v=} {i=} {l=} {l[i]=} {e=} {type(e)=} {v**e=} {type(v**e)=} {v**-e=} {type(v**-e)=}'
    return fmtl(ret)
########################################################################################################################################################################################################
def dumpData(csv=0):
    slog(f'BGN {csv=}', p=0)
    dmpData('C', csv=csv)
    slog(f'END {csv=}', p=0)

def dmpData(n='C', csv=0):
    k = Notes.N2I[n] + 48
    dmpJust(k, rf=440, sss=V_SOUND, csv=csv)
    
def dmpJust(k, rf=440, sss=V_SOUND, csv=0):
    slog(f'BGN Just Tone Series ({k=} {rf=} {sss=} {csv=})', p=0)
    r0s, r1s, r2s, r3s = [], [], [], []   ;   a, b = 5, 3
    slog(f'{fmtis(C)}', p=0)
    slog(f'{fmtis(D)}', p=0)
    slog(f'{fmtis(C, A)}', p=0)
    slog(f'{fmtis(D, B)}', p=0)
    for     i, c in enumerate(C):
        for j, d in enumerate(D):
#            if c < 0 < d:
#                tmp = c  ;  c = d  ;  d = abs(tmp)
#                tmp = a  ;  a = b  ;  b = abs(tmp)
            n = fmtNote(k+i, j)
            u = CRS[i][j]
            v, w = ivls.norm(u)
            slog(f'{u:7.4f} {v=:7.5f} : {i=} {j=} {a}^{c:2} {b}^{d:2} {w=:2} {n=:2}', p=0)
    for     c in C:
        for d in D:
#            if c < 0 < d:
#                tmp = c  ;  c = d  ;  d = abs(tmp)
#                tmp = a  ;  a = b  ;  b = abs(tmp)
            addFmtRs(r0s, r1s, r2s, r3s, a, c, b, d, '^9.5f', 4)
    slog(f'{fmtl(r0s)}', p=0)
    slog(f'{fmtl(r1s, w=6)}', p=0)
#    slog(f'{fmtl(rBs, w=6)}', p=0)
    slog(f'{fmtl(r2s)}', p=0)
    slog(f'{fmtl(r3s)}', p=0)
    slog(f'END Just Tone Series ({k=} {rf=} {sss=} {csv=})', p=0)
########################################################################################################################################################################################################
def fmtNote(k, i):
    n1, n2   = i2nPair(k + i, s=1)
    return n1
########################################################################################################################################################################################################
def fJTS(i, r=440):
    f0 = F440s[0] if r==440 else F432s[0]  ;  return f0 * i

