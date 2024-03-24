from tpkg       import utl
from tpkg       import unic
from tpkg       import notes
from tpkg.notes import Notes
import math

F, N, S       = unic.F,     unic.N,    unic.S
W, Y, Z       = utl.W,      utl.Y,     utl.Z
slog, ist     = utl.slog,   utl.ist
fmtf, fmtg    = utl.fmtf,   utl.fmtg
fmtl, fmtm    = utl.fmtl,   utl.fmtm

SUPERS        = utl.SPRSCRPT_INTS
MAX_FREQ_IDX  = utl.MAX_FREQ_IDX
ACCD_TONES    = notes.ACCD_TONES
CM_P_M        = notes.CM_P_M
V_SOUND       = notes.V_SOUND
A4_INDEX      = notes.A4_INDEX
NT           = Notes.NTONES
FLATS, SHRPS  = notes.FLATS, notes.SHRPS
F440s, F432s  = notes.F440s, notes.F432s

def i2spr(i):
    if i < 0: return '-' + Z.join(SUPERS[int(digit)] for digit in str(i))
    else:     return       Z.join(SUPERS[int(digit)] for digit in str(i))
########################################################################################################################################################################################################
def ir(n):           return int(round(n))
def r2cents(r):      return math.log2(r) * NT * 100
def cents2r(c):      return 2 ** (c/(100 * NT)) # N/A
def stck5ths(n):     return [ stackI(3, 2, i) for i in range(1, n+1) ]
def stck4ths(n):     return [ stackI(2, 3, i) for i in range(1, n+1) ]
def stackI(a, b, c): return [ a, b, c ]
########################################################################################################################################################################################################
def reduce(n):
    if n > 1:
        while n > 2:
            n /= 2
    elif n < 1:
        while n < 1:
            n *= 2
    return n

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
def abc2r(a, b, c):
    pa0, pb0 = a ** c, b ** c
    r0       = pa0 / pb0
    j        = foldF(r0)
    ca       = c + j if j > 0 else c #  ;   aa = [ a for _ in range(ca) ]
    cb       = c - j if j < 0 else c #  ;   bb = [ b for _ in range(cb) ]
    pa, pb   = a ** ca, b ** cb
    r        = pa / pb   ;   assert r == r0 * (2 ** j),  f'{r=} {r0=} {j=}'
    return r, ca, cb
########################################################################################################################################################################################################
def f2nPair(f, rf=440, b=None, s=0, e=0):
    ni = NT * math.log2(f / rf) # fixme
    i  = round(A4_INDEX + ni)
    return i2nPair(i, b, s, e)
    
def i2nPair(i, b=None, s=0, e=0):
    m = Z    ;    n = FLATS[i] if b == 1 else SHRPS[i]
    if s:                       n = n[:-1].strip()
    if e == 1 and len(n) > 1:
        m = FLATS[i] if not b else SHRPS[i]   ;   m = m[:-1].strip() if s else m
    return n, m
########################################################################################################################################################################################################
def testStacks(n=100, dbg=0):
    i5s, f5s = test5ths(n, -1)  ;   w = '10.5f'
    i4s, f4s = test4ths(n, -1)
    for i, k in enumerate(i5s.keys()):
        if k in i4s and i4s[k][0] > 0:
            if dbg:    slog(  f'{i+1:3} of {n:4} 5ths={k:4} {i5s[k][0]} {fmtl(i5s[k][1], w=w)} also in 4ths={i4s[k][0]} {fmtl(i4s[k][1], w=w)}')
        else: slog(f'{i+1:3} of {n:4} 5ths={k:4} {i5s[k][0]} {fmtl(i5s[k][1], w=w)}') if dbg else None
    for i, k in enumerate(i4s.keys()):
        if k in i5s and i5s[k][0] > 0:
            if dbg:    slog(  f'{i+1:3} of {n:4} 4ths={k:4} {i4s[k][0]} {fmtl(i4s[k][1], w=w)} also in 5ths={i5s[k][0]} {fmtl(i5s[k][1], w=w)}')
        else: slog(f'{i+1:3} of {n:4} 4ths={k:4} {i4s[k][0]} {fmtl(i4s[k][1], w=w)}') if dbg else None

def test5ths(n, i, dbg=0):
    mi, mf = {}, {}   ;   w = '10.5f'
    for m in range(1, n+1):
        s5s       = stck5ths(m)
        a, b, c   = s5s[i]
        r, ca, cb = abc2r(a, b, c)
        pa, pb    = a**ca, b**cb   ;   p = pa/pb
        cents     = r2cents(p)
        kf, ki    = cents, ir(cents)
        if ki in mi:      slog(f'{ki=:4} {mi[ki][0]=} {fmtl(mi[ki][1], w=w)=} {kf=:{w}}')
        if ki not in mi:  mi[ki] = [1, [kf]] 
        else:             mi[ki][0] += 1     ;   mi[ki][1].append(kf)
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
        kf, ki    = cents, ir(cents)
        if ki in mi:      slog(f'{ki=:4} {mi[ki][0]=} {fmtl(mi[ki][1], w=w)=} {kf=:{w}}')
        if ki not in mi:  mi[ki] = [1, [kf]] 
        else:             mi[ki][0] += 1     ;   mi[ki][1].append(kf)
        mf[kf]    = 1 if kf not in mf else mf[kf] + 1
        if dbg: slog(f'{m} {fmtl(s4s)}', p=0)
        if dbg: slog(f'abc = {m} 4ths = [{i}] = {fmtl(s4s[i])} {ca=} {cb=} {r=} {cents:4.0f} cents', p=0)
    ks = list(mi.keys())                     ;   slog(f'4ths {fmtl(ks, w=4)}', p=0)
    ks = sorted(ks, key= lambda x: int(x))   ;   slog(f'sort {fmtl(ks, w=4)}', p=0)
    return mi, mf
########################################################################################################################################################################################################
def dumpData(csv=0):
    slog(f'BGN {csv=}')
    if csv:  global PythMap1   ;   PythMap1 = {}
    dmpOTS(       rf=440, sss=V_SOUND, csv=csv)
#    dmpPyth(k=51, rf=440, sss=V_SOUND, csv=csv) # Eb
#    dmpPyth(k=58, rf=440, sss=V_SOUND, csv=csv) # Bb 
#    dmpPyth(k=53, rf=440, sss=V_SOUND, csv=csv) # F
#    dmpPyth(k=60, rf=440, sss=V_SOUND, csv=csv) # C
#    dmpPyth(k=55, rf=440, sss=V_SOUND, csv=csv) # G
    dmpPyth(k=50, rf=440, sss=V_SOUND, csv=csv) # D
    dmpPyth(k=57, rf=440, sss=V_SOUND, csv=csv) # A
    dmpPyth(k=52, rf=440, sss=V_SOUND, csv=csv) # E
    dmpPyth(k=59, rf=440, sss=V_SOUND, csv=csv) # B
    dmpPyth(k=54, rf=440, sss=V_SOUND, csv=csv) # F#/Gb
    dmpPyth(k=61, rf=440, sss=V_SOUND, csv=csv) # C#/Db
    dmpPyth(k=56, rf=440, sss=V_SOUND, csv=csv) # G#/Ab
#    dmpPyth(k=50, rf=440, sss=V_SOUND, csv=csv) # D
    dmpPyth(k=55, rf=440, sss=V_SOUND, csv=csv) # G
    dmpPyth(k=60, rf=440, sss=V_SOUND, csv=csv) # C
    dmpPyth(k=53, rf=440, sss=V_SOUND, csv=csv) # F
    dmpPyth(k=58, rf=440, sss=V_SOUND, csv=csv) # Bb 
    dmpPyth(k=51, rf=440, sss=V_SOUND, csv=csv) # Eb
##   dmpPyth(k=62, rf=440, sss=V_SOUND, csv=csv) # D octave
#    if not csv:  testStacks()
#    dmpPyth(k=50, rf=440, ss=V_SOUND, csv=csv) # D
#    dmpPyth(k=62, rf=440, ss=V_SOUND, csv=csv) # D octave
    slog(f'END {csv=}')
########################################################################################################################################################################################################
def fOTS(i, r=440):  f0 = F440s[0] if r == 440 else F432s[0]  ;   return f0 * i
FOTSs  = [ fOTS(i)  for i in range(1, 33) ]
########################################################################################################################################################################################################
def dmpOTS(rf=440, sss=V_SOUND, csv=0):
    slog(f'BGN Overtone Series ({rf=} {sss=} {csv=})')
    ww, dd, mm, nn, ff = ('^6', '[', Y, Y, 3) if csv else ('^6', '[', W, Z, 1)
    rs    = F440s       if rf == 440 else F432s         ;   cs, ds, ns, fs, ws = [], [], [], [], []
    freqs = F440s[:100] if rf == 440 else F432s[:100]   ;   ref = f'440A ' if rf == 440 else f'432A '
    f0    = F440s[0]    ;   w0 = CM_P_M * sss/f0
    for i, freq in enumerate(freqs):
        i += 1          ;    f  = fOTS(i, rf)    ;    w  = w0 / i
        n, n2  = f2nPair(f, b=0 if i in (17, 22, 25, 28) else 1) 
        j  = Notes.n2ai(n)
        assert 0 <= j < len(rs),  f'{j=} {len(rs)=}'
        fr = reduce(f/f0)
        f2 = rs[j]               ;    c = r2cents(fr)     ;    d = r2cents(f/f2)
        fs.append(fmtf(f, 6))    ;    ns.append(n)        ;    ws.append(fmtf(w, 6))
        cs.append(fmtf(c, 6))    ;    ds.append(fmtg(d, 6 if d >= 0 else 5))
    fs   = mm.join(fs)           ;    ws = mm.join(ws)    ;    ns = fmtl(ns, w=ww, s=mm, d=Z)      ;     cs = fmtl(cs, w=ww, s=mm, d=Z)   ;   ds = fmtl(ds, w=ww, s=mm, d=Z)
    ref += f'{nn}[{nn}'          ;  sfxf = f'{mm}]{mm}Hz'  ;   sfxw = f'{mm}]{mm}cm'         ;     sfxc = f'{mm}]{mm}cents'   ;   sfxd = f'{mm}]{mm}dcents'
    pfxn = f'notes{nn}[{nn}'     ;  pfxc = f'cents{nn}[{nn}'   ;   pfxd = f'dcnts{nn}[{nn}'        ;    sfx = f'{mm}]{nn}'
    slog(f'Index{nn}[{nn}{fmtl(list(range(1, 101)), w=ww, d=Z, s=mm)}{sfx}', p=0, f=ff)
    slog(f'{ref}{fs}{sfxf}', p=0, f=ff)
    slog(f'{pfxn}{ns}{sfx}', p=0, f=ff)
    slog(f'{pfxc}{cs}{sfxc}', p=0, f=ff)
    slog(f'{pfxd}{ds}{sfxd}', p=0, f=ff)
    slog(f'{ref}{ws}{sfxw}', p=0, f=ff)
    slog(f'END Overtone Series ({rf=} {sss=} {csv=})')

########################################################################################################################################################################################################
PythMap1   = {} # note index to ABCs (freq ratios)
#              0     1     2     3     4     5     6     7     8     9     10    11    12    13    14    15    16    17    18    19    20    21    22    23
#              D     Eb                E     F                 F#    G           Ab    G#          A     Bb                B     C                 C#    D
INTRVLKEYS = ['P1', 'm2', 'A1', 'd3', 'M2', 'm3', 'A2', 'd4', 'M3', 'P4', 'A3', 'd5', 'A4', 'd6', 'P5', 'm6', 'A5', 'd7', 'M6', 'm7', 'A6', 'd8', 'M7', 'P8']
CENTKEYS   = [   0,  90,  114,  180,  204,  294,  318,  384,  408,  498,  522,  588,  612,  678,  702,  792,  816,  882,  906,  996,  1020, 1086, 1110, 1200]
PythMap2   = { e: {'Count': 0} for e in CENTKEYS } # freq ratio in cents to counts
PythMap3   = { CENTKEYS[i]: k for i, k in enumerate(INTRVLKEYS) }
PM2KEYS    = ['ABCs', 'Cents', 'Count', 'DCents', 'Freq', 'Index', 'Intrv', 'Note', 'Wavlen']
########################################################################################################################################################################################################
def pythEpsln(dbg=0):
    ccents = pythComma()
    ecents = ccents / NT
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
def fPyth(a=7, b=6):
    abc1 = stck5ths(a)
    abc2 = stck4ths(b)
    abc3 = [ stackI(3, 2, 0) ]   ;   abc3.extend(abc1)   ;   abc3.extend(abc2)   ;   abc3.append(stackI(2, 1, 1))
    abc4 = sorted(abc3, key= lambda z: abc2r(z[0], z[1], z[2])[0])
    return [ abc1, abc2, abc3, abc4 ] 

def fabc(abc):
    return [ fmtl(e, w=2, d=Z) for e in abc ]
########################################################################################################################################################################################################
def dmpPyth(k=50, rf=440, sss=V_SOUND, csv=0):
    x, y = 13, 6     ;   z = x-2
    ww, mm, nn, oo, ff = (f'^{x}', Y, Y, Y, 3) if csv else (f'^{x}', W, Z, '|', 1)
    slog(f'BGN Pythagorean ({k=} {rf=} {sss=} {csv=})', f=ff)
    ii = [ f'{i}' for i in range(2 * NT) ]
    slog(f'{mm}  k  {mm}{nn} {nn}{fmtl(ii, w=ww, s=mm, d=Z)}', p=0, f=ff)
    dmpDataTableLine(x + 1, csv=csv)
    f0 = F440s[k] if rf==440 else F432s[k]      ;     w0 = CM_P_M * sss
    ii, ns, fs, ws = [], [], [], []   ;   cs, ds = [], []   ;   vs = []   ;   ps, qs = [], []   ;   rs, ss = [], []   ;   nns, rrs = [], []
    abcs = k2PythAbcs(k)         ;   abc0 = list(abcs[3])   ;  cki = -1   ;   blnk = f'{W*x}'
    abc1, abc2, abc3, abc4 = fabc(abcs[0]), fabc(abcs[1]), fabc(abcs[2]), fabc(abcs[3])
    for i, e in enumerate(abc0):
        a, b, c   = e[0], e[1], e[2]
        r, ca, cb = abc2r(a, b, c)
        rr = [ a, ca, b, cb ]
        f  = r * f0              ;    w = w0 / f
        pa = a ** ca             ;   pb = b ** cb              ;   p = f'{pa:>{y}}/{pb:<{y}}'
        qa = f'{a}^{ca}'         ;   qb = f'{b}^{cb}'          ;   q = f'{qa:>{y}}/{qb:<{y}}'
        sa = f'{a}{i2spr(ca)}'   ;   sb = f'{b}{i2spr(cb)}'    ;   s = f'{sa:>{y}}/{sb:<{y}}'
        n, n2 = i2nPair(k + i, b=0 if i in (4, 6, 11) or k in (54, 56, 61) else 1, s=1, e=1)
        if n2 and i and i != NT and i != 6:    n += '/' + n2
        c  = r2cents(r)          ;   d = c - i * 100 if i != 0 else 0.0 # fixme
        rc   = round(c)          ;   v = PythMap3[rc]          ;   cki += 1
        while CENTKEYS[cki] < rc:
            i2, c2, d2, n2, f2, w2, p2, q2, r2, s2, v2 = blnk, blnk, blnk, blnk, blnk, blnk, blnk, blnk, blnk, blnk, blnk    ;    cki += 1
            ii.append(i2)  ;  cs.append(c2)  ;  ds.append(d2)  ;  ns.append(n2)  ;  fs.append(f2)  ;  ws.append(w2)  ;  ps.append(p2)   ;   qs.append(q2)  ;  rs.append(r2)  ;  ss.append(s2)  ;  vs.append(v2)
            jj = len(ii)-1 ; abc1.insert(jj, fmtl([W, W, W], w=2, d=Z))  ;  abc2.insert(jj, fmtl([W, W, W], w=2, d=Z))  ;  abc3.insert(jj, fmtl([W, W, W], w=2, d=Z))  ;  abc4.insert(jj, fmtl([W, W, W], w=2, d=Z))
        ii.append(i)       ;   fs.append(fmtf(f, z))     ;     ps.append(p)      ;   rs.append(fmtf(r, z))     ;   cs.append(fmtf(c, y-1))   ;   rrs.append(rr)
        ns.append(n)       ;   ws.append(fmtf(w, z))     ;     qs.append(q)      ;   ss.append(s)              ;   ds.append(fmtg(d, y-1))   ;    vs.append(v)
    ii     = fmtl(ii,   w=ww, s=oo, d=Z)  ;    fs = fmtl(fs,   w=ww, s=oo, d=Z)  ;    cs = fmtl(cs,   w=ww, s=oo, d=Z)  ;   ps  = fmtl(ps,   w=ww, s=oo, d=Z)  ;  rs = fmtl(rs, w=ww, s=oo, d=Z)
    ns     = fmtl(ns,   w=ww, s=oo, d=Z)  ;    ws = fmtl(ws,   w=ww, s=oo, d=Z)  ;    ds = fmtl(ds,   w=ww, s=oo, d=Z)  ;   qs  = fmtl(qs,   w=ww, s=oo, d=Z)  ;  ss = fmtl(ss, w=ww, s=oo, d=Z)  ;  vs = fmtl(vs, w=ww, s=oo, d=Z)
    abc1   = fmtl(abc1, w=ww, s=oo, d=Z)  ;  abc2 = fmtl(abc2, w=ww, s=oo, d=Z)  ;  abc3 = fmtl(abc3, w=ww, s=oo, d=Z)  ;  abc4 = fmtl(abc4, w=ww, s=oo, d=Z)
    pfxi   = f'{mm}Index{mm}{nn}[{nn}'    ;  pfxr = f'{mm}Ratio{mm}{nn}[{nn}'    ;  pfx1 = f'{mm} ABC1{mm}{nn}[{nn}'    ;  pfxf = f'{mm}Freq {mm}{nn}[{nn}'
    pfxn   = f'{mm}Note {mm}{nn}[{nn}'    ;  pfxp = f'{mm}Rati1{mm}{nn}[{nn}'    ;  pfx2 = f'{mm} ABC2{mm}{nn}[{nn}'    ;  pfxw = f'{mm}Wavln{mm}{nn}[{nn}'    
    pfxc   = f'{mm}Cents{mm}{nn}[{nn}'    ;  pfxq = f'{mm}Rati2{mm}{nn}[{nn}'    ;  pfx3 = f'{mm} ABC3{mm}{nn}[{nn}'    ;  pfxv = f'{mm}Intrv{mm}{nn}[{nn}'
    pfxd   = f'{mm}dCent{mm}{nn}[{nn}'    ;  pfxs = f'{mm}Rati3{mm}{nn}[{nn}'    ;  pfx4 = f'{mm} ABC4{mm}{nn}[{nn}'
    sfx    = f'{nn}]'   ;   sfxc = f'{nn}]{mm}cents'   ;  sfxf = f'{nn}]{mm}Hz'  ;  sfxw = f'{nn}]{mm}cm'
    PythMap1[k] = rrs # fixme this is not a very useful data, key should store all other data values as well
    slog(f'{pfxi}{ii}{sfx}',   p=0, f=ff)
    slog(f'{pfxn}{ns}{sfx}',   p=0, f=ff)
    slog(f'{pfxv}{vs}{sfx}',   p=0, f=ff)
    slog(f'{pfxr}{rs}{sfx}',   p=0, f=ff)
    slog(f'{pfxp}{ps}{sfx}',   p=0, f=ff)
    slog(f'{pfxq}{qs}{sfx}',   p=0, f=ff)
    slog(f'{pfxs}{ss}{sfx}',   p=0, f=ff)
    slog(f'{pfxc}{cs}{sfxc}',  p=0, f=ff)
    slog(f'{pfxd}{ds}{sfxc}',  p=0, f=ff)
    slog(f'{pfxf}{fs}{sfxf}',  p=0, f=ff)
    slog(f'{pfxw}{ws}{sfxw}',  p=0, f=ff)
    slog(f'{pfx1}{abc1}{sfx}', p=0, f=ff)
    slog(f'{pfx2}{abc2}{sfx}', p=0, f=ff)
    slog(f'{pfx3}{abc3}{sfx}', p=0, f=ff)
    slog(f'{pfx4}{abc4}{sfx}', p=0, f=ff)
    dmpDataTableLine(x + 1, csv=csv)
    dmpPythMaps(k,     csv)
    slog(f'END Pythagorean ({k=} {rf=} {sss=} {csv=})', f=ff)
########################################################################################################################################################################################################
def k2PythAbcs(k=50):
    f = fPyth
    return f(6, 5) if k==50 or k== 62 else f(5, 6) if k==57 else f(4, 7) if k==52 else f(3, 8) if k==59 else f(2, 9)  if k==54 else f(1, 10) if k==61 else f(0, 11) if k==56 \
                                      else f(7, 4) if k==55 else f(8, 3) if k==60 else f(9, 2) if k==53 else f(10, 1) if k==58 else f(11, 0) if k==51 else f(12, 0)
#   return f(7, 6) if k==50 or k== 62 else f(6, 7) if k==57 else f(5, 8) if k==52 else f(4, 9)  if k==59 else f(3, 10) if k==54 else f(2, 11) if k==61 else f(1, 12) if k==56 \
#                                     else f(8, 5) if k==55 else f(9, 4) if k==60 else f(10, 3) if k==53 else f(11, 2) if k==58 else f(12, 1) if k==51 else f(13, 0)
########################################################################################################################################################################################################
def k2dCent(k):
    return k if 0 <= k < 50 else k-100 if 50<=k<150 else k-200 if 150<=k<250 else k-300 if 250<=k<350 else k-400 if 350<=k<450 else k-500 if 450<=k<550 else k-600 if 550<=k<650 else k-700 if 650<=k<750 else k-800 if 750<=k<850 else k-900 if 850<=k<950 else k-1000 if 950<=k<1050 else k-1100 if 1050<=k<1150 else k-1200 if 1150 <= k <= 1200 else None
#       return c-100 if 50<=c<150 else c-200 if 150<=c<250 else c-300 if 250<=c<350 else c-400 if 350<=c<450 else c-500 if 450<=c<550 else c-600 if 550<=c<650 else c-700 if 650<=c<750 else c-800 if 750<=c<850 else c-900 if 850<=c<950 else c-1000 if 950<=c<1050 else c-1100 if 1050<=c<1150 else c-1200
########################################################################################################################################################################################################
def dmpPythMaps(k, csv):
#    dmpPythMap1(1, csv=csv)
#    dmpPythMap1(2, csv=csv)
#    dmpPythMap1(3, csv=csv)
#    dmpPythMap1(4, csv=csv)
    dmpPythMap1(5, k,    csv=csv)
    dmpPythMap2(k,       csv=csv)
    dmpPythMap1(5, k, 9, csv=csv) # dupliicates counts
    global PythMap2   ;   PythMap2   = { e: {'Count': 0} for e in CENTKEYS }
    dmpPythMap3(         csv=csv)
########################################################################################################################################################################################################
def dmpPythMap3(csv=0):
    if not csv:
        slog(f'         {fmtm(PythMap3, w=4, wv=2, s=3*W, d=Z)}', p=0)
########################################################################################################################################################################################################
def dmpPythMap1(ni, ik, x=13, csv=0): # x=13 or x=19
    y = 6 # if x==13 else 6 # fixme same value?
    ww, mm, nn, oo, ff = (f'^{x}', Y, Y, Y, 3) if csv else (f'^{x}', W, Z, '|', 1)   ;   pfx = ''   ;   sfx = f'{nn}]'
    ii = [ f'{i}' for i in range(2 * NT) ]
    slog(f'{mm}  k  {mm}{nn} {nn}{fmtl(ii, w=ww, s=mm, d=Z)}', p=0, f=ff) if ni == 1 else None
    dmpDataTableLine(x + 1, csv=csv) if ni == 1 else None
    for i, (k, v) in enumerate(PythMap1.items()):
        rats, qots, exps, exus, cents = [], [], [], [], []   ;   cki = -1
        for j, e in enumerate(v):
            a, ca, b, cb = e
            pa, pb = a ** ca, b ** cb
            n, n2  = i2nPair(j + k, b=0 if j in (4, 6, 11) or k in (54, 56, 61) else 1, s=1, e=1)
            i2     = i if 0 <= i <= 9 else 'a' if i == 10 else 'b' if i == 11 else None
            pd     = [f'{i2:1}', f'{k:2}', f'{n:2}']   ;   pfx = mm.join(pd)   ;   pfx += f'{nn}[{nn}'
            cent   = r2cents(pa/pb)      ;   centR = ir(cent)   ;   cki += 1
            while CENTKEYS[cki] < centR:
                cent2, rat2, qot2, exp2, exu2 = f'{W*x}', f'{W*x}', f'{W*x}', f'{W*x}', f'{W*x}'   ;   cent2f = f'{cent2:{ww}}'   ;   cki += 1
                rats.append(rat2)   ;   qots.append(qot2)   ;   exps.append(exp2)   ;   exus.append(exu2)   ;   cents.append(cent2f)
            rat    = f'{float(pa/pb):{ww}.5f}'
            qot    = f'{pa:{y}}/{pb:<{y}}'
            expA   = f'{a}^{ca}'         ;    expB = f'{b}^{cb}'         ;   exp = f'{expA:>{y}}/{expB:<{y}}'
            exuA   = f'{a}{i2spr(ca)}'   ;    exuB = f'{b}{i2spr(cb)}'   ;   exu = f'{exuA:>{y}}/{exuB:<{y}}'
            if ni == 5:
                assert centR in PythMap2.keys(),  f'{centR=} {PythMap2.keys()=}'
                PythMap2[centR]['Count'] =          PythMap2[centR]['Count'] + 1 if 'Count' in PythMap2[centR] else 1
                PythMap2[centR]['ABCs']  = e    ;   PythMap2[centR]['Cents']  =  cent
                PythMap2[centR]['Note']  = n+n2 if k == ik else '  '
            centf   = f'{cent:{ww}.0f}'
            rats.append(rat)   ;   qots.append(qot)   ;   exps.append(exp)   ;   exus.append(exu)   ;   cents.append(centf)
        ratsf  = Z.join(fmtl(rats,  w=ww, s=oo, d=Z))
        qotsf  = Z.join(fmtl(qots,  w=ww, s=oo, d=Z))
        expsf  = Z.join(fmtl(exps,  w=ww, s=oo, d=Z))
        exusf  = Z.join(fmtl(exus,  w=ww, s=oo, d=Z))
        centsf = Z.join(fmtl(cents, w=ww, s=oo, d=Z))
        if   ni == 1: slog(f'{pfx}{ratsf}{sfx}',  p=0, f=ff)
        elif ni == 2: slog(f'{pfx}{qotsf}{sfx}',  p=0, f=ff)
        elif ni == 3: slog(f'{pfx}{expsf}{sfx}',  p=0, f=ff)
        elif ni == 4: slog(f'{pfx}{exusf}{sfx}',  p=0, f=ff)
        elif ni == 5: slog(f'{pfx}{centsf}{sfx}', p=0, f=ff)
    dmpDataTableLine(x + 1, csv=csv)
    slog(f'{mm}  k  {mm}{nn} {nn}{fmtl(ii, w=ww, s=mm, d=Z)}', p=0, f=ff) if ni == 5 else None
########################################################################################################################################################################################################
def fIvals(data, i, csv):
    mm, nn = (Y, Y) if csv else (W, Z)   ;   fd = []
    for j, d in enumerate(data): # j j*100 i Iv  c     k       d       e       c`   Iv  c     k       d       e       c`
        if   j==0:  fd.append(f'{d:x}')                  # j
        elif j==1:  fd.append(f'{d:4}')                  # j*100
        elif j==6:  fd.append(f'{d:7.3f}') if utl.ist(d, float) else fd.append(W*7) # d
        elif j==8:  fd.append(f'*{mm}{d:2}   ')          # c`
        elif j==12: fd.append(f'{d:7.3f}') if utl.ist(d, float) else fd.append(W*7) if i!=0 and i!=len(PythMap3)-1 else fd.append(W*7) # d
        elif j==14: fd.append(f'*{mm}{d:2}')             # c`
        elif j in (5, 11): fd.append(f'@{mm}{d:4}{mm}:') # k k
        elif j in (7, 13): fd.append(f'={mm}{d:5.3f}')   # e e
        elif j in (2, 3, 4, 9, 10): fd.append(f'{d:2}')  # i Iv c Iv c
    return fd
########################################################################################################################################################################################################
def dmpPythIvals(i, ks, cs, ds, csv):
    mm, nn, oo, ff = (Y, Y, Y, 3) if csv else (W, Z, '|', 1)   ;   m = -1
    eps, j     = pythEpsln(), math.floor(i/2)
    hdrA, hdrB1, hdrB2 = ['j', 'j*100', 'i'], ['Iv', f' c{mm} ', f'  k {mm} ', f'   d   {mm} ', f' e   {mm} ', f' c`  '], ['Iv', f' c{mm} ', f'  k {mm} ', f'   d   {mm} ', f' e   {mm} ', f' c`']
    hdrs       = hdrA   ;   hdrs.extend(hdrB1)   ;   hdrs.extend(hdrB2)
    if   i == 0:
        slog(f'{fmtl(hdrs, s=mm, d=Z)}', p=0, f=ff)
        data     = [j, j*100, i, PythMap3[ks[i]], cs[i], ks[i], ds[i], eps, 0, 'd2', 0, 24, W*6, eps, cs[i]]
        fd       = fIvals(data, i, csv)    ;    slog(f'{fmtl(fd, s=mm, d=Z)}', p=0, f=ff)
    elif not i % 2:
        u, v = (PythMap3[ks[i+m]], PythMap3[ks[i]])
        if  j < 6 and j % 2 or j > 6 and not j % 2:
            data = [j, j*100, i, u, cs[i+m], ks[i+m], ds[i+m], eps, cs[i], v, cs[i], ks[i], ds[i], eps, cs[i+m]]
            fd   = fIvals(data, i, csv)    ;    slog(f'{fmtl(fd, s=mm, d=Z)}', p=0, f=ff)
        else:
            data = [j, j*100, i, v, cs[i], ks[i], ds[i], eps, cs[i+m], u, cs[i+m], ks[i+m], ds[i+m], eps, cs[i]]
            fd   = fIvals(data, i, csv)    ;    slog(f'{fmtl(fd, s=mm, d=Z)}', p=0, f=ff)
    elif i == len(PythMap3)-1:
        data     = [j+1, (j+1)*100, i+1, PythMap3[ks[i]], cs[i], ks[i], ds[i], eps, 0, 'A7', 0, 1178, W*6, eps, cs[i]]
        fd       = fIvals(data, i, csv)    ;    slog(f'{fmtl(fd, s=mm, d=Z)}', p=0, f=ff)
########################################################################################################################################################################################################
def fmtR0(a, ca, b, cb, w):   pa, pb =   float(a ** ca) ,   float(b ** cb)   ;  return f'{pa/pb:{w}}'
#def fmtR1(a, ca, b, cb, w):  pa, pb =   a ** ca        ,   b ** cb          ;  return f'{pa:>}/{pb:<}'
def fmtRA(a, ca, w=Z):        pa     =   a ** ca                             ;  return f'{pa:{w}}'
def fmtRB(b, cb, w=Z):        pb     =   b ** cb                             ;  return f'{pb:{w}}'
def fmtR2(a, ca, b, cb):      qa, qb = f'{a}^{ca}'      , f'{b}^{cb}'        ;  return f'{qa:>}/{qb:<}'
def fmtR3(a, ca, b, cb):      sa, sb = f'{a}{i2spr(ca)}', f'{b}{i2spr(cb)}'  ;  return f'{sa:>}/{sb:<}' 
def fdvdr(a, ca, b, cb):      n = max(len(fmtRA(a, ca)), len(fmtRB(b, cb)))  ;  return n * '/'
########################################################################################################################################################################################################
def dmpDataTableLine(w=10, n=24, csv=0):
    c = '-'   ;   nn, mm, t = (Y, Y, Y) if csv else (Z, W, '|')
    col = f'{c * (w-1)}'
    cols = t.join([ col for _ in range(n) ])
    slog(f'{mm}     {mm}{nn} {nn}{cols}', p=0, f=3 if csv else 1)
########################################################################################################################################################################################################
def dmpPythMap2(k=50, rf=440, sss=V_SOUND, csv=0):
    global PythMap2
    mm, nn, oo, ff  = (Y, Y, Y, 3) if csv else (W, Z, '|', 1)         ;   x, u = 5, 9
    ww, w1, w2, w3  = f'^{u}', f'^{u}.1f', f'^{u}.2f', f'^{u}.{x}f'   ;    dbg = 0
    blnk, sk, v     = u*W, 0, Z       ;  f0 = F440s[k] if rf==440 else F432s[k]   ;   w0 = CM_P_M * sss
    ns, fs, ws, vs  = [], [], [], []  ;  cs, ds, qs, ks = [], [], [], []  ;   r0s, rAs, rBs, r1s, r2s, r3s = [], [], [], [], [], []  ;  cksf, cksi = [], []
    for i, ck in enumerate(CENTKEYS):
        ival = PythMap3[ck] 
        vs.append(ival)
        if PythMap2 and ck in PythMap2 and PythMap2[ck]['Count'] > 0:
            a, ca, b, cb = PythMap2[ck]['ABCs']
            r = a**ca / b**cb
            f = r * f0    ;    w = w0 / f
            r0s.append(fmtR0(a, ca, b, cb, w3))
            rAs.append(fmtRA(a, ca, ww))
            rBs.append(fmtRB(b, cb, ww))
            q = fdvdr(a, ca, b, cb)
#           r1s.append(fmtR1(a, ca, b, cb, ww)) if ck in PythMap2 and PythMap2[ck]['Count'] > 0 else r1s.append(blnk) 
            r2s.append(fmtR2(a, ca, b, cb)) if u >= 9 else None
            r3s.append(fmtR3(a, ca, b, cb))
            n = PythMap2[ck]['Note']
            k = PythMap2[ck]['Count']   ;   sk += k
            c = r2cents(a**ca/b**cb)
            d = k2dCent(c)              ;   d = round(d, 2)
            cksf.append(f'{c:{w1}}')    ;   cksi.append(int(round(c)))
            fs.append(f'{fmtf(f, u-2)}')   ;   ws.append(f'{fmtf(w, u-2)}')
        else:
            r0s.append(blnk)    ;    rAs.append(blnk)     ;  rBs.append(blnk)  ;   r2s.append(blnk)  ;  r3s.append(blnk)   ;   k, q = 0, Z
            n, c, d, f, w = blnk, blnk, blnk, blnk, blnk  ;  cksi.append(ck)   ;  cksf.append(blnk)  ;  fs.append(f)       ;   ws.append(w)
        ns.append(n)  ;  ks.append(k)  ;  cs.append(c)    ;  ds.append(d)      ;   qs.append(q)
        dmpPythIvals(i, cksi, ks, ds, csv)
    ii = [ f'{i}' for i in range(2 * NT) ]
    slog(f'{mm}  k  {mm}{nn} {nn}{fmtl(ii, w=ww, s=mm, d=Z)}', p=0, f=ff)
    dmpDataTableLine(u + 1, csv=csv)
    slog(f'{mm}Centk{mm}{nn}[{nn}{fmtl(CENTKEYS, w=ww, s=oo, d=Z)}{nn}]', p=0, f=ff)
    slog(f'{mm}Intrv{mm}{nn}[{nn}{fmtl(vs,       w=ww, s=oo, d=Z)}{nn}]', p=0, f=ff)
    slog(f'{mm}Note {mm}{nn}[{nn}{fmtl(ns,       w=ww, s=oo, d=Z)}{nn}]', p=0, f=ff)
    slog(f'{mm}Cents{mm}{nn}[{nn}{fmtl(cksf,     w=ww, s=oo, d=Z)}{nn}]', p=0, f=ff)
    slog(f'{mm}dCent{mm}{nn}[{nn}{fmtl(ds,       w=ww, s=oo, d=Z)}{nn}]', p=0, f=ff)
    slog(f'{mm}Rati0{mm}{nn}[{nn}{fmtl(r0s,      w=ww, s=oo, d=Z)}{nn}]', p=0, f=ff)
    slog(f'{mm}RatiA{mm}{nn}[{nn}{fmtl(rAs,      w=ww, s=oo, d=Z)}{nn}]', p=0, f=ff)
    slog(f'{mm} A/B {mm}{nn}[{nn}{fmtl(qs,       w=ww, s=oo, d=Z)}{nn}]', p=0, f=ff)
    slog(f'{mm}RatiB{mm}{nn}[{nn}{fmtl(rBs,      w=ww, s=oo, d=Z)}{nn}]', p=0, f=ff)
#   slog(f'{mm}Rati1{mm}{nn}[{nn}{fmtl(r1s,      w=ww, s=oo, d=Z)}{nn}]', p=0, f=ff)
    slog(f'{mm}Rati2{mm}{nn}[{nn}{fmtl(r2s,      w=ww, s=oo, d=Z)}{nn}]', p=0, f=ff) if u >= 9 else None
    slog(f'{mm}Rati3{mm}{nn}[{nn}{fmtl(r3s,      w=ww, s=oo, d=Z)}{nn}]', p=0, f=ff)
    slog(f'{mm}Freq {mm}{nn}[{nn}{fmtl(fs,       w=ww, s=oo, d=Z)}{nn}]', p=0, f=ff)
    slog(f'{mm}Wavln{mm}{nn}[{nn}{fmtl(ws,       w=ww, s=oo, d=Z)}{nn}]', p=0, f=ff)
    slog(f'{mm}Count{mm}{nn}[{nn}{fmtl(ks,       w=ww, s=oo, d=Z)}{nn}]', p=0, f=ff)
    dmpDataTableLine(u + 1, csv=csv)
    if dbg: slog(f'{len(PythMap1)=} {sk=}', p=0, f=ff)
    PythMap2 = { e: {'Count': 0} for e in CENTKEYS }
########################################################################################################################################################################################################
'''
   k        0         1         2         3         4         5         6         7         8         9        10        11        12        13        14        15        16        17        18        19        20        21        22        23    
        ---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------
 Centk [    0        90        114       180       204       294       318       384       408       498       522       588       612       678       702       792       816       882       906       996      1020      1086      1110      1200   ]
 Intrv [   P1        m2        A1        d3        M2        m3        A2        d4        M3        P4        A3        d5        A4        d6        P5        m6        A5        d7        M6        m7        A6        d8        M7        P8    ]
 Note  [    D       E♭D♯                            E         F                           F♯G♭        G                           G♯A♭                  A       B♭A♯                            B         C                           C♯D♭        D    ]
 Cents [   0.0      90.2                          203.9     294.1                         407.8     498.0                         611.7               702.0     792.2                         905.9     996.1                        1109.8    1200.0  ]
 dCent [   0.0      -9.78                         3.91      -5.87                         7.82      -1.96                         11.73               1.96      -7.82                         5.87      -3.91                         9.78       0.0   ]
 Rati0 [ 1.00000   1.05350                       1.12500   1.18519                       1.26562   1.33333                       1.42383             1.50000   1.58025                       1.68750   1.77778                       1.89844   2.00000 ]
 RatiA [    1        256                            9        32                            81         4                            729                  3        128                           27        16                            243        2    ]
       [    /        ///                            /        //                            //         /                            ///                  /        ///                           //        //                            ///        /    ]
 RatiB [    1        243                            8        27                            64         3                            512                  2        81                            16         9                            128        1    ]
 Rati2 [ 3^0/2^0   2^8/3^5                       3^2/2^3   2^5/3^3                       3^4/2^6   2^2/3^1                       3^6/2^9             3^1/2^1   2^7/3^4                       3^3/2^4   2^4/3^2                       3^5/2^7   2^1/1^1 ]
 Rati3 [  3⁰/2⁰     2⁸/3⁵                         3²/2³     2⁵/3³                         3⁴/2⁶     2²/3¹                         3⁶/2⁹               3¹/2¹     2⁷/3⁴                         3³/2⁴     2⁴/3²                         3⁵/2⁷     2¹/1¹  ]
 Count [    1         1         0         0         1         1         0         0         1         1         0         0         1         0         1         1         0         0         1         1         0         0         1         1    ]
        ---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------
   k        0         1         2         3         4         5         6         7         8         9        10        11        12        13        14        15        16        17        18        19        20        21        22        23    
        ---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------
 Centk [    0        90        114       180       204       294       318       384       408       498       522       588       612       678       702       792       816       882       906       996      1020      1086      1110      1200   ]
 Intrv [   P1        m2        A1        d3        M2        m3        A2        d4        M3        P4        A3        d5        A4        d6        P5        m6        A5        d7        M6        m7        A6        d8        M7        P8    ]
 Note  [    A       B♭A♯                            B         C                           C♯D♭        D                 D♯E♭                            E         F                           G♭F♯        G                           G♯A♭        A    ]
 Cents [   0.0      90.2                          203.9     294.1                         407.8     498.0               588.3     611.7               702.0     792.2                         905.9     996.1                        1109.8    1200.0  ]
 dCent [   0.0      -9.78                         3.91      -5.87                         7.82      -1.96              -11.73     11.73               1.96      -7.82                         5.87      -3.91                         9.78       0.0   ]
 Rati0 [ 1.00000   1.05350                       1.12500   1.18519                       1.26562   1.33333             1.40466   1.42383             1.50000   1.58025                       1.68750   1.77778                       1.89844   2.00000 ]
 RatiA [    1        256                            9        32                            81         4                 1024       729                  3        128                           27        16                            243        2    ]
       [    /        ///                            /        //                            //         /                 ////       ///                  /        ///                           //        //                            ///        /    ]
 RatiB [    1        243                            8        27                            64         3                  729       512                  2        81                            16         9                            128        1    ]
 Rati2 [ 3^0/2^0   2^8/3^5                       3^2/2^3   2^5/3^3                       3^4/2^6   2^2/3^1            2^10/3^6   3^6/2^9             3^1/2^1   2^7/3^4                       3^3/2^4   2^4/3^2                       3^5/2^7   2^1/1^1 ]
 Rati3 [  3⁰/2⁰     2⁸/3⁵                         3²/2³     2⁵/3³                         3⁴/2⁶     2²/3¹              2¹⁰/3⁶     3⁶/2⁹               3¹/2¹     2⁷/3⁴                         3³/2⁴     2⁴/3²                         3⁵/2⁷     2¹/1¹  ]
 Count [    2         2         0         0         2         2         0         0         2         2         0         1         1         0         2         2         0         0         2         2         0         0         2         2    ]
        ---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------
   k        0         1         2         3         4         5         6         7         8         9        10        11        12        13        14        15        16        17        18        19        20        21        22        23    
        ---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------
 Centk [    0        90        114       180       204       294       318       384       408       498       522       588       612       678       702       792       816       882       906       996      1020      1086      1110      1200   ]
 Intrv [   P1        m2        A1        d3        M2        m3        A2        d4        M3        P4        A3        d5        A4        d6        P5        m6        A5        d7        M6        m7        A6        d8        M7        P8    ]
 Note  [    E         F                           G♭F♯        G                           G♯A♭        A                 A♯B♭                            B         C                           D♭C♯        D                 D♯E♭                  E    ]
 Cents [   0.0      90.2                          203.9     294.1                         407.8     498.0               588.3     611.7               702.0     792.2                         905.9     996.1              1086.3    1109.8    1200.0  ]
 dCent [   0.0      -9.78                         3.91      -5.87                         7.82      -1.96              -11.73     11.73               1.96      -7.82                         5.87      -3.91              -13.69     9.78       0.0   ]
 Rati0 [ 1.00000   1.05350                       1.12500   1.18519                       1.26562   1.33333             1.40466   1.42383             1.50000   1.58025                       1.68750   1.77778             1.87289   1.89844   2.00000 ]
 RatiA [    1        256                            9        32                            81         4                 1024       729                  3        128                           27        16                 4096       243        2    ]
       [    /        ///                            /        //                            //         /                 ////       ///                  /        ///                           //        //                 ////       ///        /    ]
 RatiB [    1        243                            8        27                            64         3                  729       512                  2        81                            16         9                 2187       128        1    ]
 Rati2 [ 3^0/2^0   2^8/3^5                       3^2/2^3   2^5/3^3                       3^4/2^6   2^2/3^1            2^10/3^6   3^6/2^9             3^1/2^1   2^7/3^4                       3^3/2^4   2^4/3^2            2^12/3^7   3^5/2^7   2^1/1^1 ]
 Rati3 [  3⁰/2⁰     2⁸/3⁵                         3²/2³     2⁵/3³                         3⁴/2⁶     2²/3¹              2¹⁰/3⁶     3⁶/2⁹               3¹/2¹     2⁷/3⁴                         3³/2⁴     2⁴/3²              2¹²/3⁷     3⁵/2⁷     2¹/1¹  ]
 Count [    3         3         0         0         3         3         0         0         3         3         0         2         1         0         3         3         0         0         3         3         0         1         2         3    ]
        ---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------
   k        0         1         2         3         4         5         6         7         8         9        10        11        12        13        14        15        16        17        18        19        20        21        22        23    
        ---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------
 Centk [    0        90        114       180       204       294       318       384       408       498       522       588       612       678       702       792       816       882       906       996      1020      1086      1110      1200   ]
 Intrv [   P1        m2        A1        d3        M2        m3        A2        d4        M3        P4        A3        d5        A4        d6        P5        m6        A5        d7        M6        m7        A6        d8        M7        P8    ]
 Note  [    B         C                           D♭C♯        D                 D♯E♭                  E                   F                           G♭F♯        G                           A♭G♯        A                 A♯B♭                  B    ]
 Cents [   0.0      90.2                          203.9     294.1               384.4     407.8     498.0               588.3     611.7               702.0     792.2                         905.9     996.1              1086.3    1109.8    1200.0  ]
 dCent [   0.0      -9.78                         3.91      -5.87              -15.64     7.82      -1.96              -11.73     11.73               1.96      -7.82                         5.87      -3.91              -13.69     9.78       0.0   ]
 Rati0 [ 1.00000   1.05350                       1.12500   1.18519             1.24859   1.26562   1.33333             1.40466   1.42383             1.50000   1.58025                       1.68750   1.77778             1.87289   1.89844   2.00000 ]
 RatiA [    1        256                            9        32                 8192       81         4                 1024       729                  3        128                           27        16                 4096       243        2    ]
       [    /        ///                            /        //                 ////       //         /                 ////       ///                  /        ///                           //        //                 ////       ///        /    ]
 RatiB [    1        243                            8        27                 6561       64         3                  729       512                  2        81                            16         9                 2187       128        1    ]
 Rati2 [ 3^0/2^0   2^8/3^5                       3^2/2^3   2^5/3^3            2^13/3^8   3^4/2^6   2^2/3^1            2^10/3^6   3^6/2^9             3^1/2^1   2^7/3^4                       3^3/2^4   2^4/3^2            2^12/3^7   3^5/2^7   2^1/1^1 ]
 Rati3 [  3⁰/2⁰     2⁸/3⁵                         3²/2³     2⁵/3³              2¹³/3⁸     3⁴/2⁶     2²/3¹              2¹⁰/3⁶     3⁶/2⁹               3¹/2¹     2⁷/3⁴                         3³/2⁴     2⁴/3²              2¹²/3⁷     3⁵/2⁷     2¹/1¹  ]
 Count [    4         4         0         0         4         4         0         1         3         4         0         3         1         0         4         4         0         0         4         4         0         2         2         4    ]
        ---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------
   k        0         1         2         3         4         5         6         7         8         9        10        11        12        13        14        15        16        17        18        19        20        21        22        23    
        ---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------
 Centk [    0        90        114       180       204       294       318       384       408       498       522       588       612       678       702       792       816       882       906       996      1020      1086      1110      1200   ]
 Intrv [   P1        m2        A1        d3        M2        m3        A2        d4        M3        P4        A3        d5        A4        d6        P5        m6        A5        d7        M6        m7        A6        d8        M7        P8    ]
 Note  [  F♯G♭        G                           G♯A♭        A                 A♯B♭                  B                   C                           C♯D♭        D                 D♯E♭                  E                   F                 F♯G♭   ]
 Cents [   0.0      90.2                          203.9     294.1               384.4     407.8     498.0               588.3     611.7               702.0     792.2               882.4     905.9     996.1              1086.3    1109.8    1200.0  ]
 dCent [   0.0      -9.78                         3.91      -5.87              -15.64     7.82      -1.96              -11.73     11.73               1.96      -7.82               -17.6     5.87      -3.91              -13.69     9.78       0.0   ]
 Rati0 [ 1.00000   1.05350                       1.12500   1.18519             1.24859   1.26562   1.33333             1.40466   1.42383             1.50000   1.58025             1.66479   1.68750   1.77778             1.87289   1.89844   2.00000 ]
 RatiA [    1        256                            9        32                 8192       81         4                 1024       729                  3        128                32768      27        16                 4096       243        2    ]
       [    /        ///                            /        //                 ////       //         /                 ////       ///                  /        ///                /////      //        //                 ////       ///        /    ]
 RatiB [    1        243                            8        27                 6561       64         3                  729       512                  2        81                 19683      16         9                 2187       128        1    ]
 Rati2 [ 3^0/2^0   2^8/3^5                       3^2/2^3   2^5/3^3            2^13/3^8   3^4/2^6   2^2/3^1            2^10/3^6   3^6/2^9             3^1/2^1   2^7/3^4            2^15/3^9   3^3/2^4   2^4/3^2            2^12/3^7   3^5/2^7   2^1/1^1 ]
 Rati3 [  3⁰/2⁰     2⁸/3⁵                         3²/2³     2⁵/3³              2¹³/3⁸     3⁴/2⁶     2²/3¹              2¹⁰/3⁶     3⁶/2⁹               3¹/2¹     2⁷/3⁴              2¹⁵/3⁹     3³/2⁴     2⁴/3²              2¹²/3⁷     3⁵/2⁷     2¹/1¹  ]
 Count [    5         5         0         0         5         5         0         2         3         5         0         4         1         0         5         5         0         1         4         5         0         3         2         5    ]
        ---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------
   k        0         1         2         3         4         5         6         7         8         9        10        11        12        13        14        15        16        17        18        19        20        21        22        23    
        ---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------
 Centk [    0        90        114       180       204       294       318       384       408       498       522       588       612       678       702       792       816       882       906       996      1020      1086      1110      1200   ]
 Intrv [   P1        m2        A1        d3        M2        m3        A2        d4        M3        P4        A3        d5        A4        d6        P5        m6        A5        d7        M6        m7        A6        d8        M7        P8    ]
 Note  [  C♯D♭        D                 D♯E♭                  E                   F                 F♯G♭                  G                           G♯A♭        A                 A♯B♭                  B                   C                 C♯D♭   ]
 Cents [   0.0      90.2                180.4     203.9     294.1               384.4     407.8     498.0               588.3     611.7               702.0     792.2               882.4     905.9     996.1              1086.3    1109.8    1200.0  ]
 dCent [   0.0      -9.78              -19.55     3.91      -5.87              -15.64     7.82      -1.96              -11.73     11.73               1.96      -7.82               -17.6     5.87      -3.91              -13.69     9.78       0.0   ]
 Rati0 [ 1.00000   1.05350             1.10986   1.12500   1.18519             1.24859   1.26562   1.33333             1.40466   1.42383             1.50000   1.58025             1.66479   1.68750   1.77778             1.87289   1.89844   2.00000 ]
 RatiA [    1        256                65536       9        32                 8192       81         4                 1024       729                  3        128                32768      27        16                 4096       243        2    ]
       [    /        ///                /////       /        //                 ////       //         /                 ////       ///                  /        ///                /////      //        //                 ////       ///        /    ]
 RatiB [    1        243                59049       8        27                 6561       64         3                  729       512                  2        81                 19683      16         9                 2187       128        1    ]
 Rati2 [ 3^0/2^0   2^8/3^5            2^16/3^10  3^2/2^3   2^5/3^3            2^13/3^8   3^4/2^6   2^2/3^1            2^10/3^6   3^6/2^9             3^1/2^1   2^7/3^4            2^15/3^9   3^3/2^4   2^4/3^2            2^12/3^7   3^5/2^7   2^1/1^1 ]
 Rati3 [  3⁰/2⁰     2⁸/3⁵              2¹⁶/3¹⁰    3²/2³     2⁵/3³              2¹³/3⁸     3⁴/2⁶     2²/3¹              2¹⁰/3⁶     3⁶/2⁹               3¹/2¹     2⁷/3⁴              2¹⁵/3⁹     3³/2⁴     2⁴/3²              2¹²/3⁷     3⁵/2⁷     2¹/1¹  ]
 Count [    6         6         0         1         5         6         0         3         3         6         0         5         1         0         6         6         0         2         4         6         0         4         2         6    ]
        ---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------
   k        0         1         2         3         4         5         6         7         8         9        10        11        12        13        14        15        16        17        18        19        20        21        22        23    
        ---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------
 Centk [    0        90        114       180       204       294       318       384       408       498       522       588       612       678       702       792       816       882       906       996      1020      1086      1110      1200   ]
 Intrv [   P1        m2        A1        d3        M2        m3        A2        d4        M3        P4        A3        d5        A4        d6        P5        m6        A5        d7        M6        m7        A6        d8        M7        P8    ]
 Note  [  G♯A♭        A                 A♯B♭                  B                   C                 C♯D♭                  D                 D♯E♭                  E                   F                 F♯G♭                  G                 G♯A♭   ]
 Cents [   0.0      90.2                180.4     203.9     294.1               384.4     407.8     498.0               588.3     611.7     678.5     702.0     792.2               882.4     905.9     996.1              1086.3    1109.8    1200.0  ]
 dCent [   0.0      -9.78              -19.55     3.91      -5.87              -15.64     7.82      -1.96              -11.73     11.73    -21.51     1.96      -7.82               -17.6     5.87      -3.91              -13.69     9.78       0.0   ]
 Rati0 [ 1.00000   1.05350             1.10986   1.12500   1.18519             1.24859   1.26562   1.33333             1.40466   1.42383   1.47981   1.50000   1.58025             1.66479   1.68750   1.77778             1.87289   1.89844   2.00000 ]
 RatiA [    1        256                65536       9        32                 8192       81         4                 1024       729     262144       3        128                32768      27        16                 4096       243        2    ]
       [    /        ///                /////       /        //                 ////       //         /                 ////       ///     //////       /        ///                /////      //        //                 ////       ///        /    ]
 RatiB [    1        243                59049       8        27                 6561       64         3                  729       512     177147       2        81                 19683      16         9                 2187       128        1    ]
 Rati2 [ 3^0/2^0   2^8/3^5            2^16/3^10  3^2/2^3   2^5/3^3            2^13/3^8   3^4/2^6   2^2/3^1            2^10/3^6   3^6/2^9  2^18/3^11  3^1/2^1   2^7/3^4            2^15/3^9   3^3/2^4   2^4/3^2            2^12/3^7   3^5/2^7   2^1/1^1 ]
 Rati3 [  3⁰/2⁰     2⁸/3⁵              2¹⁶/3¹⁰    3²/2³     2⁵/3³              2¹³/3⁸     3⁴/2⁶     2²/3¹              2¹⁰/3⁶     3⁶/2⁹    2¹⁸/3¹¹    3¹/2¹     2⁷/3⁴              2¹⁵/3⁹     3³/2⁴     2⁴/3²              2¹²/3⁷     3⁵/2⁷     2¹/1¹  ]
 Count [    7         7         0         2         5         7         0         4         3         7         0         6         1         1         6         7         0         3         4         7         0         5         2         7    ]
        ---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------
   k        0         1         2         3         4         5         6         7         8         9        10        11        12        13        14        15        16        17        18        19        20        21        22        23    
        ---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------
 Centk [    0        90        114       180       204       294       318       384       408       498       522       588       612       678       702       792       816       882       906       996      1020      1086      1110      1200   ]
 Intrv [   P1        m2        A1        d3        M2        m3        A2        d4        M3        P4        A3        d5        A4        d6        P5        m6        A5        d7        M6        m7        A6        d8        M7        P8    ]
 Note  [    G                 A♭G♯                  A       B♭A♯                            B         C                           C♯D♭                  D       E♭D♯                            E         F                           F♯G♭        G    ]
 Cents [   0.0      90.2      113.7     180.4     203.9     294.1               384.4     407.8     498.0               588.3     611.7     678.5     702.0     792.2               882.4     905.9     996.1              1086.3    1109.8    1200.0  ]
 dCent [   0.0      -9.78     13.69    -19.55     3.91      -5.87              -15.64     7.82      -1.96              -11.73     11.73    -21.51     1.96      -7.82               -17.6     5.87      -3.91              -13.69     9.78       0.0   ]
 Rati0 [ 1.00000   1.05350   1.06787   1.10986   1.12500   1.18519             1.24859   1.26562   1.33333             1.40466   1.42383   1.47981   1.50000   1.58025             1.66479   1.68750   1.77778             1.87289   1.89844   2.00000 ]
 RatiA [    1        256      2187      65536       9        32                 8192       81         4                 1024       729     262144       3        128                32768      27        16                 4096       243        2    ]
       [    /        ///      ////      /////       /        //                 ////       //         /                 ////       ///     //////       /        ///                /////      //        //                 ////       ///        /    ]
 RatiB [    1        243      2048      59049       8        27                 6561       64         3                  729       512     177147       2        81                 19683      16         9                 2187       128        1    ]
 Rati2 [ 3^0/2^0   2^8/3^5  3^7/2^11  2^16/3^10  3^2/2^3   2^5/3^3            2^13/3^8   3^4/2^6   2^2/3^1            2^10/3^6   3^6/2^9  2^18/3^11  3^1/2^1   2^7/3^4            2^15/3^9   3^3/2^4   2^4/3^2            2^12/3^7   3^5/2^7   2^1/1^1 ]
 Rati3 [  3⁰/2⁰     2⁸/3⁵    3⁷/2¹¹    2¹⁶/3¹⁰    3²/2³     2⁵/3³              2¹³/3⁸     3⁴/2⁶     2²/3¹              2¹⁰/3⁶     3⁶/2⁹    2¹⁸/3¹¹    3¹/2¹     2⁷/3⁴              2¹⁵/3⁹     3³/2⁴     2⁴/3²              2¹²/3⁷     3⁵/2⁷     2¹/1¹  ]
 Count [    8         7         1         2         6         8         0         4         4         8         0         6         2         1         7         8         0         3         5         8         0         5         3         8    ]
        ---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------
   k        0         1         2         3         4         5         6         7         8         9        10        11        12        13        14        15        16        17        18        19        20        21        22        23    
        ---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------
 Centk [    0        90        114       180       204       294       318       384       408       498       522       588       612       678       702       792       816       882       906       996      1020      1086      1110      1200   ]
 Intrv [   P1        m2        A1        d3        M2        m3        A2        d4        M3        P4        A3        d5        A4        d6        P5        m6        A5        d7        M6        m7        A6        d8        M7        P8    ]
 Note  [    C                 D♭C♯                  D       E♭D♯                            E         F                           F♯G♭                  G                 A♭G♯                  A       B♭A♯                            B         C    ]
 Cents [   0.0      90.2      113.7     180.4     203.9     294.1               384.4     407.8     498.0               588.3     611.7     678.5     702.0     792.2     815.6     882.4     905.9     996.1              1086.3    1109.8    1200.0  ]
 dCent [   0.0      -9.78     13.69    -19.55     3.91      -5.87              -15.64     7.82      -1.96              -11.73     11.73    -21.51     1.96      -7.82     15.64     -17.6     5.87      -3.91              -13.69     9.78       0.0   ]
 Rati0 [ 1.00000   1.05350   1.06787   1.10986   1.12500   1.18519             1.24859   1.26562   1.33333             1.40466   1.42383   1.47981   1.50000   1.58025   1.60181   1.66479   1.68750   1.77778             1.87289   1.89844   2.00000 ]
 RatiA [    1        256      2187      65536       9        32                 8192       81         4                 1024       729     262144       3        128      6561      32768      27        16                 4096       243        2    ]
       [    /        ///      ////      /////       /        //                 ////       //         /                 ////       ///     //////       /        ///      ////      /////      //        //                 ////       ///        /    ]
 RatiB [    1        243      2048      59049       8        27                 6561       64         3                  729       512     177147       2        81       4096      19683      16         9                 2187       128        1    ]
 Rati2 [ 3^0/2^0   2^8/3^5  3^7/2^11  2^16/3^10  3^2/2^3   2^5/3^3            2^13/3^8   3^4/2^6   2^2/3^1            2^10/3^6   3^6/2^9  2^18/3^11  3^1/2^1   2^7/3^4  3^8/2^12  2^15/3^9   3^3/2^4   2^4/3^2            2^12/3^7   3^5/2^7   2^1/1^1 ]
 Rati3 [  3⁰/2⁰     2⁸/3⁵    3⁷/2¹¹    2¹⁶/3¹⁰    3²/2³     2⁵/3³              2¹³/3⁸     3⁴/2⁶     2²/3¹              2¹⁰/3⁶     3⁶/2⁹    2¹⁸/3¹¹    3¹/2¹     2⁷/3⁴    3⁸/2¹²    2¹⁵/3⁹     3³/2⁴     2⁴/3²              2¹²/3⁷     3⁵/2⁷     2¹/1¹  ]
 Count [    9         7         2         2         7         9         0         4         5         9         0         6         3         1         8         8         1         3         6         9         0         5         4         9    ]
        ---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------
   k        0         1         2         3         4         5         6         7         8         9        10        11        12        13        14        15        16        17        18        19        20        21        22        23    
        ---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------
 Centk [    0        90        114       180       204       294       318       384       408       498       522       588       612       678       702       792       816       882       906       996      1020      1086      1110      1200   ]
 Intrv [   P1        m2        A1        d3        M2        m3        A2        d4        M3        P4        A3        d5        A4        d6        P5        m6        A5        d7        M6        m7        A6        d8        M7        P8    ]
 Note  [    F                 G♭F♯                  G                 A♭G♯                  A       B♭A♯                            B                   C                 D♭C♯                  D       E♭D♯                            E         F    ]
 Cents [   0.0      90.2      113.7     180.4     203.9     294.1     317.6     384.4     407.8     498.0               588.3     611.7     678.5     702.0     792.2     815.6     882.4     905.9     996.1              1086.3    1109.8    1200.0  ]
 dCent [   0.0      -9.78     13.69    -19.55     3.91      -5.87     17.6     -15.64     7.82      -1.96              -11.73     11.73    -21.51     1.96      -7.82     15.64     -17.6     5.87      -3.91              -13.69     9.78       0.0   ]
 Rati0 [ 1.00000   1.05350   1.06787   1.10986   1.12500   1.18519   1.20135   1.24859   1.26562   1.33333             1.40466   1.42383   1.47981   1.50000   1.58025   1.60181   1.66479   1.68750   1.77778             1.87289   1.89844   2.00000 ]
 RatiA [    1        256      2187      65536       9        32       19683     8192       81         4                 1024       729     262144       3        128      6561      32768      27        16                 4096       243        2    ]
       [    /        ///      ////      /////       /        //       /////     ////       //         /                 ////       ///     //////       /        ///      ////      /////      //        //                 ////       ///        /    ]
 RatiB [    1        243      2048      59049       8        27       16384     6561       64         3                  729       512     177147       2        81       4096      19683      16         9                 2187       128        1    ]
 Rati2 [ 3^0/2^0   2^8/3^5  3^7/2^11  2^16/3^10  3^2/2^3   2^5/3^3  3^9/2^14  2^13/3^8   3^4/2^6   2^2/3^1            2^10/3^6   3^6/2^9  2^18/3^11  3^1/2^1   2^7/3^4  3^8/2^12  2^15/3^9   3^3/2^4   2^4/3^2            2^12/3^7   3^5/2^7   2^1/1^1 ]
 Rati3 [  3⁰/2⁰     2⁸/3⁵    3⁷/2¹¹    2¹⁶/3¹⁰    3²/2³     2⁵/3³    3⁹/2¹⁴    2¹³/3⁸     3⁴/2⁶     2²/3¹              2¹⁰/3⁶     3⁶/2⁹    2¹⁸/3¹¹    3¹/2¹     2⁷/3⁴    3⁸/2¹²    2¹⁵/3⁹     3³/2⁴     2⁴/3²              2¹²/3⁷     3⁵/2⁷     2¹/1¹  ]
 Count [   10         7         3         2         8         9         1         4         6        10         0         6         4         1         9         8         2         3         7        10         0         5         5        10    ]
        ---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------
   k        0         1         2         3         4         5         6         7         8         9        10        11        12        13        14        15        16        17        18        19        20        21        22        23    
        ---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------
 Centk [    0        90        114       180       204       294       318       384       408       498       522       588       612       678       702       792       816       882       906       996      1020      1086      1110      1200   ]
 Intrv [   P1        m2        A1        d3        M2        m3        A2        d4        M3        P4        A3        d5        A4        d6        P5        m6        A5        d7        M6        m7        A6        d8        M7        P8    ]
 Note  [  B♭A♯                  B                   C                 D♭C♯                  D       E♭D♯                            E                   F                 G♭F♯                  G                 A♭G♯                  A       B♭A♯   ]
 Cents [   0.0      90.2      113.7     180.4     203.9     294.1     317.6     384.4     407.8     498.0               588.3     611.7     678.5     702.0     792.2     815.6     882.4     905.9     996.1    1019.6    1086.3    1109.8    1200.0  ]
 dCent [   0.0      -9.78     13.69    -19.55     3.91      -5.87     17.6     -15.64     7.82      -1.96              -11.73     11.73    -21.51     1.96      -7.82     15.64     -17.6     5.87      -3.91     19.55    -13.69     9.78       0.0   ]
 Rati0 [ 1.00000   1.05350   1.06787   1.10986   1.12500   1.18519   1.20135   1.24859   1.26562   1.33333             1.40466   1.42383   1.47981   1.50000   1.58025   1.60181   1.66479   1.68750   1.77778   1.80203   1.87289   1.89844   2.00000 ]
 RatiA [    1        256      2187      65536       9        32       19683     8192       81         4                 1024       729     262144       3        128      6561      32768      27        16       59049     4096       243        2    ]
       [    /        ///      ////      /////       /        //       /////     ////       //         /                 ////       ///     //////       /        ///      ////      /////      //        //       /////     ////       ///        /    ]
 RatiB [    1        243      2048      59049       8        27       16384     6561       64         3                  729       512     177147       2        81       4096      19683      16         9       32768     2187       128        1    ]
 Rati2 [ 3^0/2^0   2^8/3^5  3^7/2^11  2^16/3^10  3^2/2^3   2^5/3^3  3^9/2^14  2^13/3^8   3^4/2^6   2^2/3^1            2^10/3^6   3^6/2^9  2^18/3^11  3^1/2^1   2^7/3^4  3^8/2^12  2^15/3^9   3^3/2^4   2^4/3^2  3^10/2^15 2^12/3^7   3^5/2^7   2^1/1^1 ]
 Rati3 [  3⁰/2⁰     2⁸/3⁵    3⁷/2¹¹    2¹⁶/3¹⁰    3²/2³     2⁵/3³    3⁹/2¹⁴    2¹³/3⁸     3⁴/2⁶     2²/3¹              2¹⁰/3⁶     3⁶/2⁹    2¹⁸/3¹¹    3¹/2¹     2⁷/3⁴    3⁸/2¹²    2¹⁵/3⁹     3³/2⁴     2⁴/3²    3¹⁰/2¹⁵   2¹²/3⁷     3⁵/2⁷     2¹/1¹  ]
 Count [   11         7         4         2         9         9         2         4         7        11         0         6         5         1        10         8         3         3         8        10         1         5         6        11    ]
        ---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------
   k        0         1         2         3         4         5         6         7         8         9        10        11        12        13        14        15        16        17        18        19        20        21        22        23    
        ---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------
 Centk [    0        90        114       180       204       294       318       384       408       498       522       588       612       678       702       792       816       882       906       996      1020      1086      1110      1200   ]
 Intrv [   P1        m2        A1        d3        M2        m3        A2        d4        M3        P4        A3        d5        A4        d6        P5        m6        A5        d7        M6        m7        A6        d8        M7        P8    ]
 Note  [  E♭D♯                  E                   F                 G♭F♯                  G                 A♭G♯                  A                 B♭A♯                  B                   C                 D♭C♯                  D       E♭D♯   ]
 Cents [   0.0      90.2      113.7     180.4     203.9     294.1     317.6     384.4     407.8     498.0     521.5     588.3     611.7     678.5     702.0     792.2     815.6     882.4     905.9     996.1    1019.6    1086.3    1109.8    1200.0  ]
 dCent [   0.0      -9.78     13.69    -19.55     3.91      -5.87     17.6     -15.64     7.82      -1.96     21.51    -11.73     11.73    -21.51     1.96      -7.82     15.64     -17.6     5.87      -3.91     19.55    -13.69     9.78       0.0   ]
 Rati0 [ 1.00000   1.05350   1.06787   1.10986   1.12500   1.18519   1.20135   1.24859   1.26562   1.33333   1.35152   1.40466   1.42383   1.47981   1.50000   1.58025   1.60181   1.66479   1.68750   1.77778   1.80203   1.87289   1.89844   2.00000 ]
 RatiA [    1        256      2187      65536       9        32       19683     8192       81         4      177147     1024       729     262144       3        128      6561      32768      27        16       59049     4096       243        2    ]
       [    /        ///      ////      /////       /        //       /////     ////       //         /      //////     ////       ///     //////       /        ///      ////      /////      //        //       /////     ////       ///        /    ]
 RatiB [    1        243      2048      59049       8        27       16384     6561       64         3      131072      729       512     177147       2        81       4096      19683      16         9       32768     2187       128        1    ]
 Rati2 [ 3^0/2^0   2^8/3^5  3^7/2^11  2^16/3^10  3^2/2^3   2^5/3^3  3^9/2^14  2^13/3^8   3^4/2^6   2^2/3^1  3^11/2^17 2^10/3^6   3^6/2^9  2^18/3^11  3^1/2^1   2^7/3^4  3^8/2^12  2^15/3^9   3^3/2^4   2^4/3^2  3^10/2^15 2^12/3^7   3^5/2^7   2^1/1^1 ]
 Rati3 [  3⁰/2⁰     2⁸/3⁵    3⁷/2¹¹    2¹⁶/3¹⁰    3²/2³     2⁵/3³    3⁹/2¹⁴    2¹³/3⁸     3⁴/2⁶     2²/3¹    3¹¹/2¹⁷   2¹⁰/3⁶     3⁶/2⁹    2¹⁸/3¹¹    3¹/2¹     2⁷/3⁴    3⁸/2¹²    2¹⁵/3⁹     3³/2⁴     2⁴/3²    3¹⁰/2¹⁵   2¹²/3⁷     3⁵/2⁷     2¹/1¹  ]
 Count [   12         7         5         2        10         9         3         4         8        11         1         6         6         1        11         8         4         3         9        10         2         5         7        12    ]
        ---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------
         0:P1     90:m2    114:A1    180:d3    204:M2    294:m3    318:A2    384:d4    408:M3    498:P4    522:A3    588:d5    612:A4    678:d6    702:P5    792:m6    816:A5    882:d7    906:M6    996:m7   1020:A6   1086:d8   1110:M7   1200:P8
'''
'''
   k          0             1             2             3             4             5             6             7             8             9            10            11            12            13            14            15            16            17            18            19            20            21            22            23      
        -------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------
 Index [      0      |      1      |             |             |      2      |      3      |             |             |      4      |      5      |             |             |      6      |             |      7      |      8      |             |             |      9      |     10      |             |             |     11      |     12      ]
 Note  [      D      |    E♭/D♯    |             |             |      E      |      F      |             |             |    F♯/G♭    |      G      |             |             |     G♯      |             |      A      |    B♭/A♯    |             |             |      B      |      C      |             |             |    C♯/D♭    |      D      ]
 Intrv [     P1      |     m2      |             |             |     M2      |     m3      |             |             |     M3      |     P4      |             |             |     A4      |             |     P5      |     m6      |             |             |     M6      |     m7      |             |             |     M7      |     P8      ]
 Ratio [ 1.000000000 | 1.053497942 |             |             | 1.125000000 | 1.185185185 |             |             | 1.265625000 | 1.333333333 |             |             | 1.423828125 |             | 1.500000000 | 1.580246914 |             |             | 1.687500000 | 1.777777778 |             |             | 1.898437500 | 2.000000000 ]
 Rati1 [     1/1     |   256/243   |             |             |     9/8     |    32/27    |             |             |    81/64    |     4/3     |             |             |   729/512   |             |     3/2     |   128/81    |             |             |    27/16    |    16/9     |             |             |   243/128   |     2/1     ]
 Rati2 [   3^0/2^0   |   2^8/3^5   |             |             |   3^2/2^3   |   2^5/3^3   |             |             |   3^4/2^6   |   2^2/3^1   |             |             |   3^6/2^9   |             |   3^1/2^1   |   2^7/3^4   |             |             |   3^3/2^4   |   2^4/3^2   |             |             |   3^5/2^7   |   2^1/1^1   ]
 Rati3 [    3⁰/2⁰    |    2⁸/3⁵    |             |             |    3²/2³    |    2⁵/3³    |             |             |    3⁴/2⁶    |    2²/3¹    |             |             |    3⁶/2⁹    |             |    3¹/2¹    |    2⁷/3⁴    |             |             |    3³/2⁴    |    2⁴/3²    |             |             |    3⁵/2⁷    |    2¹/1¹    ]
 Cents [    0.000    |    90.22    |             |             |    203.9    |    294.1    |             |             |    407.8    |    498.0    |             |             |    611.7    |             |    702.0    |    792.2    |             |             |    905.9    |    996.1    |             |             |     1110    |     1200    ] cents
 dCent [    +0.00    |    -9.78    |             |             |    +3.91    |    -5.87    |             |             |    +7.82    |    -1.96    |             |             |    +11.7    |             |    +1.96    |    -7.82    |             |             |    +5.87    |    -3.91    |             |             |    +9.78    |    +0.00    ] cents
 Freq  [ 293.6647679 | 309.3752288 |             |             | 330.3728639 | 348.0471323 |             |             | 371.6694719 | 391.5530239 |             |             | 418.1281559 |             | 440.4971519 | 464.0628431 |             |             | 495.5592959 | 522.0706985 |             |             | 557.5042078 | 587.3295358 ] Hz
 Wavln [ 117.4808958 | 111.5150691 |             |             | 104.4274629 | 99.12450583 |             |             | 92.82441150 | 88.11067185 |             |             | 82.51058800 |             | 78.32059720 | 74.34337937 |             |             | 69.61830862 | 66.08300389 |             |             | 61.88294100 | 58.74044790 ] cm
  ABC1 [   3  2  1   |   3  2  2   |             |             |   3  2  3   |   3  2  4   |             |             |   3  2  5   |   3  2  6   |             |             |             |             |             |             |             ]
  ABC2 [   2  3  1   |   2  3  2   |             |             |   2  3  3   |   2  3  4   |             |             |   2  3  5   |             |             |             |             |             |             |             ]
  ABC3 [   3  2  0   |   3  2  1   |             |             |   3  2  2   |   3  2  3   |             |             |   3  2  4   |   3  2  5   |             |             |   3  2  6   |             |   2  3  1   |   2  3  2   |             |             |   2  3  3   |   2  3  4   |             |             |   2  3  5   |   2  1  1   ]
  ABC4 [   3  2  0   |   2  3  5   |             |             |   3  2  2   |   2  3  3   |             |             |   3  2  4   |   2  3  1   |             |             |   3  2  6   |             |   3  2  1   |   2  3  4   |             |             |   3  2  3   |   2  3  2   |             |             |   3  2  5   |   2  1  1   ]
        -------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------
0 50 D [      0      |     90      |             |             |     204     |     294     |             |             |     408     |     498     |             |             |     612     |             |     702     |     792     |             |             |     906     |     996     |             |             |    1110     |    1200     ]
        -------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------
   k          0             1             2             3             4             5             6             7             8             9            10            11            12            13            14            15            16            17            18            19            20            21            22            23      
        -------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------
 Index [      0      |      1      |             |             |      2      |      3      |             |             |      4      |      5      |             |      6      |             |             |      7      |      8      |             |             |      9      |     10      |             |             |     11      |     12      ]
 Note  [      A      |    B♭/A♯    |             |             |      B      |      C      |             |             |    C♯/D♭    |      D      |             |     D♯      |             |             |      E      |      F      |             |             |    G♭/F♯    |      G      |             |             |    G♯/A♭    |      A      ]
 Intrv [     P1      |     m2      |             |             |     M2      |     m3      |             |             |     M3      |     P4      |             |     d5      |             |             |     P5      |     m6      |             |             |     M6      |     m7      |             |             |     M7      |     P8      ]
 Ratio [ 1.000000000 | 1.053497942 |             |             | 1.125000000 | 1.185185185 |             |             | 1.265625000 | 1.333333333 |             | 1.404663923 |             |             | 1.500000000 | 1.580246914 |             |             | 1.687500000 | 1.777777778 |             |             | 1.898437500 | 2.000000000 ]
 Rati1 [     1/1     |   256/243   |             |             |     9/8     |    32/27    |             |             |    81/64    |     4/3     |             |  1024/729   |             |             |     3/2     |   128/81    |             |             |    27/16    |    16/9     |             |             |   243/128   |     2/1     ]
 Rati2 [   3^0/2^0   |   2^8/3^5   |             |             |   3^2/2^3   |   2^5/3^3   |             |             |   3^4/2^6   |   2^2/3^1   |             |  2^10/3^6   |             |             |   3^1/2^1   |   2^7/3^4   |             |             |   3^3/2^4   |   2^4/3^2   |             |             |   3^5/2^7   |   2^1/1^1   ]
 Rati3 [    3⁰/2⁰    |    2⁸/3⁵    |             |             |    3²/2³    |    2⁵/3³    |             |             |    3⁴/2⁶    |    2²/3¹    |             |   2¹⁰/3⁶    |             |             |    3¹/2¹    |    2⁷/3⁴    |             |             |    3³/2⁴    |    2⁴/3²    |             |             |    3⁵/2⁷    |    2¹/1¹    ]
 Cents [    0.000    |    90.22    |             |             |    203.9    |    294.1    |             |             |    407.8    |    498.0    |             |    588.3    |             |             |    702.0    |    792.2    |             |             |    905.9    |    996.1    |             |             |     1110    |     1200    ] cents
 dCent [    +0.00    |    -9.78    |             |             |    +3.91    |    -5.87    |             |             |    +7.82    |    -1.96    |             |    -11.7    |             |             |    +1.96    |    -7.82    |             |             |    +5.87    |    -3.91    |             |             |    +9.78    |    +0.00    ] cents
 Freq  [ 440.0000000 | 463.5390947 |             |             | 495.0000000 | 521.4814815 |             |             | 556.8750000 | 586.6666667 |             | 618.0521262 |             |             | 660.0000000 | 695.3086420 |             |             | 742.5000000 | 782.2222222 |             |             | 835.3125000 | 880.0000000 ] Hz
 Wavln [ 78.40909091 | 74.42737926 |             |             | 69.69696970 | 66.15767045 |             |             | 61.95286195 | 58.80681818 |             | 55.82053445 |             |             | 52.27272727 | 49.61825284 |             |             | 46.46464646 | 44.10511364 |             |             | 41.30190797 | 39.20454545 ] cm
  ABC1 [   3  2  1   |   3  2  2   |             |             |   3  2  3   |   3  2  4   |             |             |   3  2  5   |             |             |             |             |             |             |             ]
  ABC2 [   2  3  1   |   2  3  2   |             |             |   2  3  3   |   2  3  4   |             |             |   2  3  5   |   2  3  6   |             |             |             |             |             |             |             ]
  ABC3 [   3  2  0   |   3  2  1   |             |             |   3  2  2   |   3  2  3   |             |             |   3  2  4   |   3  2  5   |             |   2  3  1   |             |             |   2  3  2   |   2  3  3   |             |             |   2  3  4   |   2  3  5   |             |             |   2  3  6   |   2  1  1   ]
  ABC4 [   3  2  0   |   2  3  5   |             |             |   3  2  2   |   2  3  3   |             |             |   3  2  4   |   2  3  1   |             |   2  3  6   |             |             |   3  2  1   |   2  3  4   |             |             |   3  2  3   |   2  3  2   |             |             |   3  2  5   |   2  1  1   ]
        -------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------
0 50 D [      0      |     90      |             |             |     204     |     294     |             |             |     408     |     498     |             |             |     612     |             |     702     |     792     |             |             |     906     |     996     |             |             |    1110     |    1200     ]
1 57 A [      0      |     90      |             |             |     204     |     294     |             |             |     408     |     498     |             |     588     |             |             |     702     |     792     |             |             |     906     |     996     |             |             |    1110     |    1200     ]
        -------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------
   k          0             1             2             3             4             5             6             7             8             9            10            11            12            13            14            15            16            17            18            19            20            21            22            23      
        -------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------
 Index [      0      |      1      |             |             |      2      |      3      |             |             |      4      |      5      |             |      6      |             |             |      7      |      8      |             |             |      9      |     10      |             |     11      |             |     12      ]
 Note  [      E      |      F      |             |             |    G♭/F♯    |      G      |             |             |    G♯/A♭    |      A      |             |     A♯      |             |             |      B      |      C      |             |             |    D♭/C♯    |      D      |             |    D♯/E♭    |             |      E      ]
 Intrv [     P1      |     m2      |             |             |     M2      |     m3      |             |             |     M3      |     P4      |             |     d5      |             |             |     P5      |     m6      |             |             |     M6      |     m7      |             |     d8      |             |     P8      ]
 Ratio [ 1.000000000 | 1.053497942 |             |             | 1.125000000 | 1.185185185 |             |             | 1.265625000 | 1.333333333 |             | 1.404663923 |             |             | 1.500000000 | 1.580246914 |             |             | 1.687500000 | 1.777777778 |             | 1.872885231 |             | 2.000000000 ]
 Rati1 [     1/1     |   256/243   |             |             |     9/8     |    32/27    |             |             |    81/64    |     4/3     |             |  1024/729   |             |             |     3/2     |   128/81    |             |             |    27/16    |    16/9     |             |  4096/2187  |             |     2/1     ]
 Rati2 [   3^0/2^0   |   2^8/3^5   |             |             |   3^2/2^3   |   2^5/3^3   |             |             |   3^4/2^6   |   2^2/3^1   |             |  2^10/3^6   |             |             |   3^1/2^1   |   2^7/3^4   |             |             |   3^3/2^4   |   2^4/3^2   |             |  2^12/3^7   |             |   2^1/1^1   ]
 Rati3 [    3⁰/2⁰    |    2⁸/3⁵    |             |             |    3²/2³    |    2⁵/3³    |             |             |    3⁴/2⁶    |    2²/3¹    |             |   2¹⁰/3⁶    |             |             |    3¹/2¹    |    2⁷/3⁴    |             |             |    3³/2⁴    |    2⁴/3²    |             |   2¹²/3⁷    |             |    2¹/1¹    ]
 Cents [    0.000    |    90.22    |             |             |    203.9    |    294.1    |             |             |    407.8    |    498.0    |             |    588.3    |             |             |    702.0    |    792.2    |             |             |    905.9    |    996.1    |             |     1086    |             |     1200    ] cents
 dCent [    +0.00    |    -9.78    |             |             |    +3.91    |    -5.87    |             |             |    +7.82    |    -1.96    |             |    -11.7    |             |             |    +1.96    |    -7.82    |             |             |    +5.87    |    -3.91    |             |    -13.7    |             |    +0.00    ] cents
 Freq  [ 329.6275569 | 347.2619530 |             |             | 370.8310015 | 390.6696971 |             |             | 417.1848767 | 439.5034092 |             | 463.0159373 |             |             | 494.4413354 | 520.8929294 |             |             | 556.2465023 | 586.0045456 |             | 617.3545830 |             | 659.2551138 ] Hz
 Wavln [ 104.6635795 | 99.34863208 |             |             | 93.03429287 | 88.30989518 |             |             | 82.69714921 | 78.49768461 |             | 74.51147406 |             |             | 69.77571965 | 66.23242139 |             |             | 62.02286191 | 58.87326345 |             | 55.88360554 |             | 52.33178974 ] cm
  ABC1 [   3  2  1   |   3  2  2   |             |             |   3  2  3   |   3  2  4   |             |             |             |             |             |             |             |             |             ]
  ABC2 [   2  3  1   |   2  3  2   |             |             |   2  3  3   |   2  3  4   |             |             |   2  3  5   |   2  3  6   |             |   2  3  7   |             |             |             |             |             |             ]
  ABC3 [   3  2  0   |   3  2  1   |             |             |   3  2  2   |   3  2  3   |             |             |   3  2  4   |   2  3  1   |             |   2  3  2   |             |             |   2  3  3   |   2  3  4   |             |             |   2  3  5   |   2  3  6   |             |   2  3  7   |             |   2  1  1   ]
  ABC4 [   3  2  0   |   2  3  5   |             |             |   3  2  2   |   2  3  3   |             |             |   3  2  4   |   2  3  1   |             |   2  3  6   |             |             |   3  2  1   |   2  3  4   |             |             |   3  2  3   |   2  3  2   |             |   2  3  7   |             |   2  1  1   ]
        -------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------
0 50 D [      0      |     90      |             |             |     204     |     294     |             |             |     408     |     498     |             |             |     612     |             |     702     |     792     |             |             |     906     |     996     |             |             |    1110     |    1200     ]
1 57 A [      0      |     90      |             |             |     204     |     294     |             |             |     408     |     498     |             |     588     |             |             |     702     |     792     |             |             |     906     |     996     |             |             |    1110     |    1200     ]
2 52 E [      0      |     90      |             |             |     204     |     294     |             |             |     408     |     498     |             |     588     |             |             |     702     |     792     |             |             |     906     |     996     |             |    1086     |             |    1200     ]
        -------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------
   k          0             1             2             3             4             5             6             7             8             9            10            11            12            13            14            15            16            17            18            19            20            21            22            23      
        -------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------
 Index [      0      |      1      |             |             |      2      |      3      |             |      4      |             |      5      |             |      6      |             |             |      7      |      8      |             |             |      9      |     10      |             |     11      |             |     12      ]
 Note  [      B      |      C      |             |             |    D♭/C♯    |      D      |             |    D♯/E♭    |             |      E      |             |      F      |             |             |    G♭/F♯    |      G      |             |             |    A♭/G♯    |      A      |             |    A♯/B♭    |             |      B      ]
 Intrv [     P1      |     m2      |             |             |     M2      |     m3      |             |     d4      |             |     P4      |             |     d5      |             |             |     P5      |     m6      |             |             |     M6      |     m7      |             |     d8      |             |     P8      ]
 Ratio [ 1.000000000 | 1.053497942 |             |             | 1.125000000 | 1.185185185 |             | 1.248590154 |             | 1.333333333 |             | 1.404663923 |             |             | 1.500000000 | 1.580246914 |             |             | 1.687500000 | 1.777777778 |             | 1.872885231 |             | 2.000000000 ]
 Rati1 [     1/1     |   256/243   |             |             |     9/8     |    32/27    |             |  8192/6561  |             |     4/3     |             |  1024/729   |             |             |     3/2     |   128/81    |             |             |    27/16    |    16/9     |             |  4096/2187  |             |     2/1     ]
 Rati2 [   3^0/2^0   |   2^8/3^5   |             |             |   3^2/2^3   |   2^5/3^3   |             |  2^13/3^8   |             |   2^2/3^1   |             |  2^10/3^6   |             |             |   3^1/2^1   |   2^7/3^4   |             |             |   3^3/2^4   |   2^4/3^2   |             |  2^12/3^7   |             |   2^1/1^1   ]
 Rati3 [    3⁰/2⁰    |    2⁸/3⁵    |             |             |    3²/2³    |    2⁵/3³    |             |   2¹³/3⁸    |             |    2²/3¹    |             |   2¹⁰/3⁶    |             |             |    3¹/2¹    |    2⁷/3⁴    |             |             |    3³/2⁴    |    2⁴/3²    |             |   2¹²/3⁷    |             |    2¹/1¹    ]
 Cents [    0.000    |    90.22    |             |             |    203.9    |    294.1    |             |    384.4    |             |    498.0    |             |    588.3    |             |             |    702.0    |    792.2    |             |             |    905.9    |    996.1    |             |     1086    |             |     1200    ] cents
 dCent [    +0.00    |    -9.78    |             |             |    +3.91    |    -5.87    |             |    -15.6    |             |    -1.96    |             |    -11.7    |             |             |    +1.96    |    -7.82    |             |             |    +5.87    |    -3.91    |             |    -13.7    |             |    +0.00    ] cents
 Freq  [ 493.8833013 | 520.3050417 |             |             | 555.6187139 | 585.3431719 |             | 616.6578271 |             | 658.5110683 |             | 693.7400555 |             |             | 740.8249519 | 780.4575625 |             |             | 833.4280709 | 878.0147578 |             | 924.9867407 |             | 987.7666025 ] Hz
 Wavln [ 69.85455858 | 66.30725678 |             |             | 62.09294096 | 58.93978380 |             | 55.94674791 |             | 52.39091894 |             | 49.73044258 |             |             | 46.56970572 | 44.20483785 |             |             | 41.39529397 | 39.29318920 |             | 37.29783194 |             | 34.92727929 ] cm
  ABC1 [   3  2  1   |   3  2  2   |             |             |   3  2  3   |             |             |             |             |             |             |             |             |             ]
  ABC2 [   2  3  1   |   2  3  2   |             |             |   2  3  3   |   2  3  4   |             |   2  3  5   |             |   2  3  6   |             |   2  3  7   |             |             |   2  3  8   |             |             |             |             ]
  ABC3 [   3  2  0   |   3  2  1   |             |             |   3  2  2   |   3  2  3   |             |   2  3  1   |             |   2  3  2   |             |   2  3  3   |             |             |   2  3  4   |   2  3  5   |             |             |   2  3  6   |   2  3  7   |             |   2  3  8   |             |   2  1  1   ]
  ABC4 [   3  2  0   |   2  3  5   |             |             |   3  2  2   |   2  3  3   |             |   2  3  8   |             |   2  3  1   |             |   2  3  6   |             |             |   3  2  1   |   2  3  4   |             |             |   3  2  3   |   2  3  2   |             |   2  3  7   |             |   2  1  1   ]
        -------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------
0 50 D [      0      |     90      |             |             |     204     |     294     |             |             |     408     |     498     |             |             |     612     |             |     702     |     792     |             |             |     906     |     996     |             |             |    1110     |    1200     ]
1 57 A [      0      |     90      |             |             |     204     |     294     |             |             |     408     |     498     |             |     588     |             |             |     702     |     792     |             |             |     906     |     996     |             |             |    1110     |    1200     ]
2 52 E [      0      |     90      |             |             |     204     |     294     |             |             |     408     |     498     |             |     588     |             |             |     702     |     792     |             |             |     906     |     996     |             |    1086     |             |    1200     ]
3 59 B [      0      |     90      |             |             |     204     |     294     |             |     384     |             |     498     |             |     588     |             |             |     702     |     792     |             |             |     906     |     996     |             |    1086     |             |    1200     ]
        -------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------
   k          0             1             2             3             4             5             6             7             8             9            10            11            12            13            14            15            16            17            18            19            20            21            22            23      
        -------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------
 Index [      0      |      1      |             |             |      2      |      3      |             |      4      |             |      5      |             |      6      |             |             |      7      |      8      |             |      9      |             |     10      |             |     11      |             |     12      ]
 Note  [     F♯      |      G      |             |             |    G♯/A♭    |      A      |             |    A♯/B♭    |             |      B      |             |      C      |             |             |    C♯/D♭    |      D      |             |    D♯/E♭    |             |      E      |             |      F      |             |     F♯      ]
 Intrv [     P1      |     m2      |             |             |     M2      |     m3      |             |     d4      |             |     P4      |             |     d5      |             |             |     P5      |     m6      |             |     d7      |             |     m7      |             |     d8      |             |     P8      ]
 Ratio [ 1.000000000 | 1.053497942 |             |             | 1.125000000 | 1.185185185 |             | 1.248590154 |             | 1.333333333 |             | 1.404663923 |             |             | 1.500000000 | 1.580246914 |             | 1.664786872 |             | 1.777777778 |             | 1.872885231 |             | 2.000000000 ]
 Rati1 [     1/1     |   256/243   |             |             |     9/8     |    32/27    |             |  8192/6561  |             |     4/3     |             |  1024/729   |             |             |     3/2     |   128/81    |             | 32768/19683 |             |    16/9     |             |  4096/2187  |             |     2/1     ]
 Rati2 [   3^0/2^0   |   2^8/3^5   |             |             |   3^2/2^3   |   2^5/3^3   |             |  2^13/3^8   |             |   2^2/3^1   |             |  2^10/3^6   |             |             |   3^1/2^1   |   2^7/3^4   |             |  2^15/3^9   |             |   2^4/3^2   |             |  2^12/3^7   |             |   2^1/1^1   ]
 Rati3 [    3⁰/2⁰    |    2⁸/3⁵    |             |             |    3²/2³    |    2⁵/3³    |             |   2¹³/3⁸    |             |    2²/3¹    |             |   2¹⁰/3⁶    |             |             |    3¹/2¹    |    2⁷/3⁴    |             |   2¹⁵/3⁹    |             |    2⁴/3²    |             |   2¹²/3⁷    |             |    2¹/1¹    ]
 Cents [    0.000    |    90.22    |             |             |    203.9    |    294.1    |             |    384.4    |             |    498.0    |             |    588.3    |             |             |    702.0    |    792.2    |             |    882.4    |             |    996.1    |             |     1086    |             |     1200    ] cents
 dCent [    +0.00    |    -9.78    |             |             |    +3.91    |    -5.87    |             |    -15.6    |             |    -1.96    |             |    -11.7    |             |             |    +1.96    |    -7.82    |             |    -17.6    |             |    -3.91    |             |    -13.7    |             |    +0.00    ] cents
 Freq  [ 369.9944227 | 389.7883630 |             |             | 416.2437256 | 438.5119084 |             | 461.9713932 |             | 493.3258969 |             | 519.7178174 |             |             | 554.9916341 | 584.6825445 |             | 615.9618576 |             | 657.7678626 |             | 692.9570898 |             | 739.9888454 ] Hz
 Wavln [ 93.24464879 | 88.50956897 |             |             | 82.88413226 | 78.67517242 |             | 74.67994882 |             | 69.93348659 |             | 66.38217673 |             |             | 62.16309919 | 59.00637931 |             | 56.00996161 |             | 52.45011494 |             | 49.78663254 |             | 46.62232439 ] cm
  ABC1 [   3  2  1   |   3  2  2   |             |             |             |             |             |             |             |             |             |             |             ]
  ABC2 [   2  3  1   |   2  3  2   |             |             |   2  3  3   |   2  3  4   |             |   2  3  5   |             |   2  3  6   |             |   2  3  7   |             |             |   2  3  8   |   2  3  9   |             |             |             |             ]
  ABC3 [   3  2  0   |   3  2  1   |             |             |   3  2  2   |   2  3  1   |             |   2  3  2   |             |   2  3  3   |             |   2  3  4   |             |             |   2  3  5   |   2  3  6   |             |   2  3  7   |             |   2  3  8   |             |   2  3  9   |             |   2  1  1   ]
  ABC4 [   3  2  0   |   2  3  5   |             |             |   3  2  2   |   2  3  3   |             |   2  3  8   |             |   2  3  1   |             |   2  3  6   |             |             |   3  2  1   |   2  3  4   |             |   2  3  9   |             |   2  3  2   |             |   2  3  7   |             |   2  1  1   ]
        -------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------
0 50 D [      0      |     90      |             |             |     204     |     294     |             |             |     408     |     498     |             |             |     612     |             |     702     |     792     |             |             |     906     |     996     |             |             |    1110     |    1200     ]
1 57 A [      0      |     90      |             |             |     204     |     294     |             |             |     408     |     498     |             |     588     |             |             |     702     |     792     |             |             |     906     |     996     |             |             |    1110     |    1200     ]
2 52 E [      0      |     90      |             |             |     204     |     294     |             |             |     408     |     498     |             |     588     |             |             |     702     |     792     |             |             |     906     |     996     |             |    1086     |             |    1200     ]
3 59 B [      0      |     90      |             |             |     204     |     294     |             |     384     |             |     498     |             |     588     |             |             |     702     |     792     |             |             |     906     |     996     |             |    1086     |             |    1200     ]
4 54 F♯[      0      |     90      |             |             |     204     |     294     |             |     384     |             |     498     |             |     588     |             |             |     702     |     792     |             |     882     |             |     996     |             |    1086     |             |    1200     ]
        -------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------
   k          0             1             2             3             4             5             6             7             8             9            10            11            12            13            14            15            16            17            18            19            20            21            22            23      
        -------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------
 Index [      0      |      1      |             |      2      |             |      3      |             |      4      |             |      5      |             |      6      |             |             |      7      |      8      |             |      9      |             |     10      |             |     11      |             |     12      ]
 Note  [     C♯      |      D      |             |    D♯/E♭    |             |      E      |             |      F      |             |    F♯/G♭    |             |      G      |             |             |    G♯/A♭    |      A      |             |    A♯/B♭    |             |      B      |             |      C      |             |     C♯      ]
 Intrv [     P1      |     m2      |             |     d3      |             |     m3      |             |     d4      |             |     P4      |             |     d5      |             |             |     P5      |     m6      |             |     d7      |             |     m7      |             |     d8      |             |     P8      ]
 Ratio [ 1.000000000 | 1.053497942 |             | 1.109857915 |             | 1.185185185 |             | 1.248590154 |             | 1.333333333 |             | 1.404663923 |             |             | 1.500000000 | 1.580246914 |             | 1.664786872 |             | 1.777777778 |             | 1.872885231 |             | 2.000000000 ]
 Rati1 [     1/1     |   256/243   |             | 65536/59049 |             |    32/27    |             |  8192/6561  |             |     4/3     |             |  1024/729   |             |             |     3/2     |   128/81    |             | 32768/19683 |             |    16/9     |             |  4096/2187  |             |     2/1     ]
 Rati2 [   3^0/2^0   |   2^8/3^5   |             |  2^16/3^10  |             |   2^5/3^3   |             |  2^13/3^8   |             |   2^2/3^1   |             |  2^10/3^6   |             |             |   3^1/2^1   |   2^7/3^4   |             |  2^15/3^9   |             |   2^4/3^2   |             |  2^12/3^7   |             |   2^1/1^1   ]
 Rati3 [    3⁰/2⁰    |    2⁸/3⁵    |             |   2¹⁶/3¹⁰   |             |    2⁵/3³    |             |   2¹³/3⁸    |             |    2²/3¹    |             |   2¹⁰/3⁶    |             |             |    3¹/2¹    |    2⁷/3⁴    |             |   2¹⁵/3⁹    |             |    2⁴/3²    |             |   2¹²/3⁷    |             |    2¹/1¹    ]
 Cents [    0.000    |    90.22    |             |    180.4    |             |    294.1    |             |    384.4    |             |    498.0    |             |    588.3    |             |             |    702.0    |    792.2    |             |    882.4    |             |    996.1    |             |     1086    |             |     1200    ] cents
 dCent [    +0.00    |    -9.78    |             |    -19.6    |             |    -5.87    |             |    -15.6    |             |    -1.96    |             |    -11.7    |             |             |    +1.96    |    -7.82    |             |    -17.6    |             |    -3.91    |             |    -13.7    |             |    +0.00    ] cents
 Freq  [ 554.3652620 | 584.0226628 |             | 615.2666736 |             | 657.0254956 |             | 692.1750078 |             | 739.1536826 |             | 778.6968837 |             |             | 831.5478929 | 876.0339942 |             | 922.9000103 |             | 985.5382435 |             | 1038.262512 |             | 1108.730524 ] Hz
 Wavln [ 62.23333670 | 59.07305007 |             | 56.07324674 |             | 52.50937784 |             | 49.84288599 |             | 46.67500252 |             | 44.30478755 |             |             | 41.48889113 | 39.38203338 |             | 37.38216450 |             | 35.00625189 |             | 33.22859066 |             | 31.11666835 ] cm
  ABC1 [   3  2  1   |             |             |             |             |             |             |             |             |             |             |             ]
  ABC2 [   2  3  1   |   2  3  2   |             |   2  3  3   |             |   2  3  4   |             |   2  3  5   |             |   2  3  6   |             |   2  3  7   |             |             |   2  3  8   |   2  3  9   |             |   2  3 10   |             |             |             ]
  ABC3 [   3  2  0   |   3  2  1   |             |   2  3  1   |             |   2  3  2   |             |   2  3  3   |             |   2  3  4   |             |   2  3  5   |             |             |   2  3  6   |   2  3  7   |             |   2  3  8   |             |   2  3  9   |             |   2  3 10   |             |   2  1  1   ]
  ABC4 [   3  2  0   |   2  3  5   |             |   2  3 10   |             |   2  3  3   |             |   2  3  8   |             |   2  3  1   |             |   2  3  6   |             |             |   3  2  1   |   2  3  4   |             |   2  3  9   |             |   2  3  2   |             |   2  3  7   |             |   2  1  1   ]
        -------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------
0 50 D [      0      |     90      |             |             |     204     |     294     |             |             |     408     |     498     |             |             |     612     |             |     702     |     792     |             |             |     906     |     996     |             |             |    1110     |    1200     ]
1 57 A [      0      |     90      |             |             |     204     |     294     |             |             |     408     |     498     |             |     588     |             |             |     702     |     792     |             |             |     906     |     996     |             |             |    1110     |    1200     ]
2 52 E [      0      |     90      |             |             |     204     |     294     |             |             |     408     |     498     |             |     588     |             |             |     702     |     792     |             |             |     906     |     996     |             |    1086     |             |    1200     ]
3 59 B [      0      |     90      |             |             |     204     |     294     |             |     384     |             |     498     |             |     588     |             |             |     702     |     792     |             |             |     906     |     996     |             |    1086     |             |    1200     ]
4 54 F♯[      0      |     90      |             |             |     204     |     294     |             |     384     |             |     498     |             |     588     |             |             |     702     |     792     |             |     882     |             |     996     |             |    1086     |             |    1200     ]
5 61 C♯[      0      |     90      |             |     180     |             |     294     |             |     384     |             |     498     |             |     588     |             |             |     702     |     792     |             |     882     |             |     996     |             |    1086     |             |    1200     ]
        -------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------
   k          0             1             2             3             4             5             6             7             8             9            10            11            12            13            14            15            16            17            18            19            20            21            22            23      
        -------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------
 Index [      0      |      1      |             |      2      |             |      3      |             |      4      |             |      5      |             |      6      |             |      7      |             |      8      |             |      9      |             |     10      |             |     11      |             |     12      ]
 Note  [     G♯      |      A      |             |    A♯/B♭    |             |      B      |             |      C      |             |    C♯/D♭    |             |      D      |             |    D♯/E♭    |             |      E      |             |      F      |             |    F♯/G♭    |             |      G      |             |     G♯      ]
 Intrv [     P1      |     m2      |             |     d3      |             |     m3      |             |     d4      |             |     P4      |             |     d5      |             |     d6      |             |     m6      |             |     d7      |             |     m7      |             |     d8      |             |     P8      ]
 Ratio [ 1.000000000 | 1.053497942 |             | 1.109857915 |             | 1.185185185 |             | 1.248590154 |             | 1.333333333 |             | 1.404663923 |             | 1.479810553 |             | 1.580246914 |             | 1.664786872 |             | 1.777777778 |             | 1.872885231 |             | 2.000000000 ]
 Rati1 [     1/1     |   256/243   |             | 65536/59049 |             |    32/27    |             |  8192/6561  |             |     4/3     |             |  1024/729   |             |262144/177147|             |   128/81    |             | 32768/19683 |             |    16/9     |             |  4096/2187  |             |     2/1     ]
 Rati2 [   3^0/2^0   |   2^8/3^5   |             |  2^16/3^10  |             |   2^5/3^3   |             |  2^13/3^8   |             |   2^2/3^1   |             |  2^10/3^6   |             |  2^18/3^11  |             |   2^7/3^4   |             |  2^15/3^9   |             |   2^4/3^2   |             |  2^12/3^7   |             |   2^1/1^1   ]
 Rati3 [    3⁰/2⁰    |    2⁸/3⁵    |             |   2¹⁶/3¹⁰   |             |    2⁵/3³    |             |   2¹³/3⁸    |             |    2²/3¹    |             |   2¹⁰/3⁶    |             |   2¹⁸/3¹¹   |             |    2⁷/3⁴    |             |   2¹⁵/3⁹    |             |    2⁴/3²    |             |   2¹²/3⁷    |             |    2¹/1¹    ]
 Cents [    0.000    |    90.22    |             |    180.4    |             |    294.1    |             |    384.4    |             |    498.0    |             |    588.3    |             |    678.5    |             |    792.2    |             |    882.4    |             |    996.1    |             |     1086    |             |     1200    ] cents
 dCent [    +0.00    |    -9.78    |             |    -19.6    |             |    -5.87    |             |    -15.6    |             |    -1.96    |             |    -11.7    |             |    -21.5    |             |    -7.82    |             |    -17.6    |             |    -3.91    |             |    -13.7    |             |    +0.00    ] cents
 Freq  [ 415.3046976 | 437.5226444 |             | 460.9292056 |             | 492.2129749 |             | 518.5453563 |             | 553.7395968 |             | 583.3635258 |             | 614.5722741 |             | 656.2839665 |             | 691.3938084 |             | 738.3194624 |             | 777.8180344 |             | 830.6093952 ] Hz
 Wavln [ 83.07153808 | 78.85306154 |             | 74.84880451 |             | 70.09161026 |             | 66.53227067 |             | 62.30365356 |             | 59.13979615 |             | 56.13660338 |             | 52.56870769 |             | 49.89920300 |             | 46.72774017 |             | 44.35484711 |             | 41.53576904 ] cm
  ABC1 [             |             |             |             |             |             |             |             |             |             |             ]
  ABC2 [   2  3  1   |   2  3  2   |             |   2  3  3   |             |   2  3  4   |             |   2  3  5   |             |   2  3  6   |             |   2  3  7   |             |   2  3  8   |             |   2  3  9   |             |   2  3 10   |             |   2  3 11   |             |             ]
  ABC3 [   3  2  0   |   2  3  1   |             |   2  3  2   |             |   2  3  3   |             |   2  3  4   |             |   2  3  5   |             |   2  3  6   |             |   2  3  7   |             |   2  3  8   |             |   2  3  9   |             |   2  3 10   |             |   2  3 11   |             |   2  1  1   ]
  ABC4 [   3  2  0   |   2  3  5   |             |   2  3 10   |             |   2  3  3   |             |   2  3  8   |             |   2  3  1   |             |   2  3  6   |             |   2  3 11   |             |   2  3  4   |             |   2  3  9   |             |   2  3  2   |             |   2  3  7   |             |   2  1  1   ]
        -------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------
0 50 D [      0      |     90      |             |             |     204     |     294     |             |             |     408     |     498     |             |             |     612     |             |     702     |     792     |             |             |     906     |     996     |             |             |    1110     |    1200     ]
1 57 A [      0      |     90      |             |             |     204     |     294     |             |             |     408     |     498     |             |     588     |             |             |     702     |     792     |             |             |     906     |     996     |             |             |    1110     |    1200     ]
2 52 E [      0      |     90      |             |             |     204     |     294     |             |             |     408     |     498     |             |     588     |             |             |     702     |     792     |             |             |     906     |     996     |             |    1086     |             |    1200     ]
3 59 B [      0      |     90      |             |             |     204     |     294     |             |     384     |             |     498     |             |     588     |             |             |     702     |     792     |             |             |     906     |     996     |             |    1086     |             |    1200     ]
4 54 F♯[      0      |     90      |             |             |     204     |     294     |             |     384     |             |     498     |             |     588     |             |             |     702     |     792     |             |     882     |             |     996     |             |    1086     |             |    1200     ]
5 61 C♯[      0      |     90      |             |     180     |             |     294     |             |     384     |             |     498     |             |     588     |             |             |     702     |     792     |             |     882     |             |     996     |             |    1086     |             |    1200     ]
6 56 G♯[      0      |     90      |             |     180     |             |     294     |             |     384     |             |     498     |             |     588     |             |     678     |             |     792     |             |     882     |             |     996     |             |    1086     |             |    1200     ]
        -------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------
   k          0             1             2             3             4             5             6             7             8             9            10            11            12            13            14            15            16            17            18            19            20            21            22            23      
        -------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------
 Index [      0      |             |      1      |             |      2      |      3      |             |             |      4      |      5      |             |             |      6      |             |      7      |      8      |             |             |      9      |     10      |             |             |     11      |     12      ]
 Note  [      G      |             |    A♭/G♯    |             |      A      |    B♭/A♯    |             |             |      B      |      C      |             |             |     C♯      |             |      D      |    E♭/D♯    |             |             |      E      |      F      |             |             |    F♯/G♭    |      G      ]
 Intrv [     P1      |             |     A1      |             |     M2      |     m3      |             |             |     M3      |     P4      |             |             |     A4      |             |     P5      |     m6      |             |             |     M6      |     m7      |             |             |     M7      |     P8      ]
 Ratio [ 1.000000000 |             | 1.067871094 |             | 1.125000000 | 1.185185185 |             |             | 1.265625000 | 1.333333333 |             |             | 1.423828125 |             | 1.500000000 | 1.580246914 |             |             | 1.687500000 | 1.777777778 |             |             | 1.898437500 | 2.000000000 ]
 Rati1 [     1/1     |             |  2187/2048  |             |     9/8     |    32/27    |             |             |    81/64    |     4/3     |             |             |   729/512   |             |     3/2     |   128/81    |             |             |    27/16    |    16/9     |             |             |   243/128   |     2/1     ]
 Rati2 [   3^0/2^0   |             |   3^7/2^11  |             |   3^2/2^3   |   2^5/3^3   |             |             |   3^4/2^6   |   2^2/3^1   |             |             |   3^6/2^9   |             |   3^1/2^1   |   2^7/3^4   |             |             |   3^3/2^4   |   2^4/3^2   |             |             |   3^5/2^7   |   2^1/1^1   ]
 Rati3 [    3⁰/2⁰    |             |    3⁷/2¹¹   |             |    3²/2³    |    2⁵/3³    |             |             |    3⁴/2⁶    |    2²/3¹    |             |             |    3⁶/2⁹    |             |    3¹/2¹    |    2⁷/3⁴    |             |             |    3³/2⁴    |    2⁴/3²    |             |             |    3⁵/2⁷    |    2¹/1¹    ]
 Cents [    0.000    |             |    113.7    |             |    203.9    |    294.1    |             |             |    407.8    |    498.0    |             |             |    611.7    |             |    702.0    |    792.2    |             |             |    905.9    |    996.1    |             |             |     1110    |     1200    ] cents
 dCent [    +0.00    |             |    +13.7    |             |    +3.91    |    -5.87    |             |             |    +7.82    |    -1.96    |             |             |    +11.7    |             |    +1.96    |    -7.82    |             |             |    +5.87    |    -3.91    |             |             |    +9.78    |    +0.00    ] cents
 Freq  [ 391.9954360 |             | 418.6005950 |             | 440.9948655 | 464.5871834 |             |             | 496.1192237 | 522.6605813 |             |             | 558.1341266 |             | 587.9931540 | 619.4495778 |             |             | 661.4922982 | 696.8807751 |             |             | 744.1788355 | 783.9908720 ] Hz
 Wavln [ 88.01122879 |             | 82.41746528 |             | 78.23220337 | 74.25947429 |             |             | 69.53973633 | 66.00842159 |             |             | 61.81309896 |             | 58.67415253 | 55.69460572 |             |             | 52.15480224 | 49.50631619 |             |             | 46.35982422 | 44.00561439 ] cm
  ABC1 [   3  2  1   |             |   3  2  2   |             |   3  2  3   |   3  2  4   |             |             |   3  2  5   |   3  2  6   |             |             |   3  2  7   |             |             |             |             |             ]
  ABC2 [   2  3  1   |             |   2  3  2   |             |   2  3  3   |   2  3  4   |             |             |             |             |             |             |             |             |             ]
  ABC3 [   3  2  0   |             |   3  2  1   |             |   3  2  2   |   3  2  3   |             |             |   3  2  4   |   3  2  5   |             |             |   3  2  6   |             |   3  2  7   |   2  3  1   |             |             |   2  3  2   |   2  3  3   |             |             |   2  3  4   |   2  1  1   ]
  ABC4 [   3  2  0   |             |   3  2  7   |             |   3  2  2   |   2  3  3   |             |             |   3  2  4   |   2  3  1   |             |             |   3  2  6   |             |   3  2  1   |   2  3  4   |             |             |   3  2  3   |   2  3  2   |             |             |   3  2  5   |   2  1  1   ]
        -------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------
0 50 D [      0      |     90      |             |             |     204     |     294     |             |             |     408     |     498     |             |             |     612     |             |     702     |     792     |             |             |     906     |     996     |             |             |    1110     |    1200     ]
1 57 A [      0      |     90      |             |             |     204     |     294     |             |             |     408     |     498     |             |     588     |             |             |     702     |     792     |             |             |     906     |     996     |             |             |    1110     |    1200     ]
2 52 E [      0      |     90      |             |             |     204     |     294     |             |             |     408     |     498     |             |     588     |             |             |     702     |     792     |             |             |     906     |     996     |             |    1086     |             |    1200     ]
3 59 B [      0      |     90      |             |             |     204     |     294     |             |     384     |             |     498     |             |     588     |             |             |     702     |     792     |             |             |     906     |     996     |             |    1086     |             |    1200     ]
4 54 F♯[      0      |     90      |             |             |     204     |     294     |             |     384     |             |     498     |             |     588     |             |             |     702     |     792     |             |     882     |             |     996     |             |    1086     |             |    1200     ]
5 61 C♯[      0      |     90      |             |     180     |             |     294     |             |     384     |             |     498     |             |     588     |             |             |     702     |     792     |             |     882     |             |     996     |             |    1086     |             |    1200     ]
6 56 G♯[      0      |     90      |             |     180     |             |     294     |             |     384     |             |     498     |             |     588     |             |     678     |             |     792     |             |     882     |             |     996     |             |    1086     |             |    1200     ]
7 55 G [      0      |             |     114     |             |     204     |     294     |             |             |     408     |     498     |             |             |     612     |             |     702     |     792     |             |             |     906     |     996     |             |             |    1110     |    1200     ]
        -------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------
   k          0             1             2             3             4             5             6             7             8             9            10            11            12            13            14            15            16            17            18            19            20            21            22            23      
        -------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------
 Index [      0      |             |      1      |             |      2      |      3      |             |             |      4      |      5      |             |             |      6      |             |      7      |             |      8      |             |      9      |     10      |             |             |     11      |     12      ]
 Note  [      C      |             |    D♭/C♯    |             |      D      |    E♭/D♯    |             |             |      E      |      F      |             |             |     F♯      |             |      G      |             |    A♭/G♯    |             |      A      |    B♭/A♯    |             |             |      B      |      C      ]
 Intrv [     P1      |             |     A1      |             |     M2      |     m3      |             |             |     M3      |     P4      |             |             |     A4      |             |     P5      |             |     A5      |             |     M6      |     m7      |             |             |     M7      |     P8      ]
 Ratio [ 1.000000000 |             | 1.067871094 |             | 1.125000000 | 1.185185185 |             |             | 1.265625000 | 1.333333333 |             |             | 1.423828125 |             | 1.500000000 |             | 1.601806641 |             | 1.687500000 | 1.777777778 |             |             | 1.898437500 | 2.000000000 ]
 Rati1 [     1/1     |             |  2187/2048  |             |     9/8     |    32/27    |             |             |    81/64    |     4/3     |             |             |   729/512   |             |     3/2     |             |  6561/4096  |             |    27/16    |    16/9     |             |             |   243/128   |     2/1     ]
 Rati2 [   3^0/2^0   |             |   3^7/2^11  |             |   3^2/2^3   |   2^5/3^3   |             |             |   3^4/2^6   |   2^2/3^1   |             |             |   3^6/2^9   |             |   3^1/2^1   |             |   3^8/2^12  |             |   3^3/2^4   |   2^4/3^2   |             |             |   3^5/2^7   |   2^1/1^1   ]
 Rati3 [    3⁰/2⁰    |             |    3⁷/2¹¹   |             |    3²/2³    |    2⁵/3³    |             |             |    3⁴/2⁶    |    2²/3¹    |             |             |    3⁶/2⁹    |             |    3¹/2¹    |             |    3⁸/2¹²   |             |    3³/2⁴    |    2⁴/3²    |             |             |    3⁵/2⁷    |    2¹/1¹    ]
 Cents [    0.000    |             |    113.7    |             |    203.9    |    294.1    |             |             |    407.8    |    498.0    |             |             |    611.7    |             |    702.0    |             |    815.6    |             |    905.9    |    996.1    |             |             |     1110    |     1200    ] cents
 dCent [    +0.00    |             |    +13.7    |             |    +3.91    |    -5.87    |             |             |    +7.82    |    -1.96    |             |             |    +11.7    |             |    +1.96    |             |    +15.6    |             |    +5.87    |    -3.91    |             |             |    +9.78    |    +0.00    ] cents
 Freq  [ 523.2511306 |             | 558.7647571 |             | 588.6575219 | 620.1494881 |             |             | 662.2397122 | 697.6681741 |             |             | 745.0196762 |             | 784.8766959 |             | 838.1471357 |             | 882.9862829 | 930.2242322 |             |             | 993.3595683 | 1046.502261 ] Hz
 Wavln [ 65.93392347 |             | 61.74333574 |             | 58.60793197 | 55.63174793 |             |             | 52.09593953 | 49.45044260 |             |             | 46.30750181 |             | 43.95594898 |             | 41.16222383 |             | 39.07195465 | 37.08783195 |             |             | 34.73062635 | 32.96696173 ] cm
  ABC1 [   3  2  1   |             |   3  2  2   |             |   3  2  3   |   3  2  4   |             |             |   3  2  5   |   3  2  6   |             |             |   3  2  7   |             |   3  2  8   |             |             |             |             ]
  ABC2 [   2  3  1   |             |   2  3  2   |             |   2  3  3   |             |             |             |             |             |             |             |             |             ]
  ABC3 [   3  2  0   |             |   3  2  1   |             |   3  2  2   |   3  2  3   |             |             |   3  2  4   |   3  2  5   |             |             |   3  2  6   |             |   3  2  7   |             |   3  2  8   |             |   2  3  1   |   2  3  2   |             |             |   2  3  3   |   2  1  1   ]
  ABC4 [   3  2  0   |             |   3  2  7   |             |   3  2  2   |   2  3  3   |             |             |   3  2  4   |   2  3  1   |             |             |   3  2  6   |             |   3  2  1   |             |   3  2  8   |             |   3  2  3   |   2  3  2   |             |             |   3  2  5   |   2  1  1   ]
        -------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------
0 50 D [      0      |     90      |             |             |     204     |     294     |             |             |     408     |     498     |             |             |     612     |             |     702     |     792     |             |             |     906     |     996     |             |             |    1110     |    1200     ]
1 57 A [      0      |     90      |             |             |     204     |     294     |             |             |     408     |     498     |             |     588     |             |             |     702     |     792     |             |             |     906     |     996     |             |             |    1110     |    1200     ]
2 52 E [      0      |     90      |             |             |     204     |     294     |             |             |     408     |     498     |             |     588     |             |             |     702     |     792     |             |             |     906     |     996     |             |    1086     |             |    1200     ]
3 59 B [      0      |     90      |             |             |     204     |     294     |             |     384     |             |     498     |             |     588     |             |             |     702     |     792     |             |             |     906     |     996     |             |    1086     |             |    1200     ]
4 54 F♯[      0      |     90      |             |             |     204     |     294     |             |     384     |             |     498     |             |     588     |             |             |     702     |     792     |             |     882     |             |     996     |             |    1086     |             |    1200     ]
5 61 C♯[      0      |     90      |             |     180     |             |     294     |             |     384     |             |     498     |             |     588     |             |             |     702     |     792     |             |     882     |             |     996     |             |    1086     |             |    1200     ]
6 56 G♯[      0      |     90      |             |     180     |             |     294     |             |     384     |             |     498     |             |     588     |             |     678     |             |     792     |             |     882     |             |     996     |             |    1086     |             |    1200     ]
7 55 G [      0      |             |     114     |             |     204     |     294     |             |             |     408     |     498     |             |             |     612     |             |     702     |     792     |             |             |     906     |     996     |             |             |    1110     |    1200     ]
8 60 C [      0      |             |     114     |             |     204     |     294     |             |             |     408     |     498     |             |             |     612     |             |     702     |             |     816     |             |     906     |     996     |             |             |    1110     |    1200     ]
        -------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------
   k          0             1             2             3             4             5             6             7             8             9            10            11            12            13            14            15            16            17            18            19            20            21            22            23      
        -------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------
 Index [      0      |             |      1      |             |      2      |             |      3      |             |      4      |      5      |             |             |      6      |             |      7      |             |      8      |             |      9      |     10      |             |             |     11      |     12      ]
 Note  [      F      |             |    G♭/F♯    |             |      G      |             |    A♭/G♯    |             |      A      |    B♭/A♯    |             |             |      B      |             |      C      |             |    D♭/C♯    |             |      D      |    E♭/D♯    |             |             |      E      |      F      ]
 Intrv [     P1      |             |     A1      |             |     M2      |             |     A2      |             |     M3      |     P4      |             |             |     A4      |             |     P5      |             |     A5      |             |     M6      |     m7      |             |             |     M7      |     P8      ]
 Ratio [ 1.000000000 |             | 1.067871094 |             | 1.125000000 |             | 1.201354980 |             | 1.265625000 | 1.333333333 |             |             | 1.423828125 |             | 1.500000000 |             | 1.601806641 |             | 1.687500000 | 1.777777778 |             |             | 1.898437500 | 2.000000000 ]
 Rati1 [     1/1     |             |  2187/2048  |             |     9/8     |             | 19683/16384 |             |    81/64    |     4/3     |             |             |   729/512   |             |     3/2     |             |  6561/4096  |             |    27/16    |    16/9     |             |             |   243/128   |     2/1     ]
 Rati2 [   3^0/2^0   |             |   3^7/2^11  |             |   3^2/2^3   |             |   3^9/2^14  |             |   3^4/2^6   |   2^2/3^1   |             |             |   3^6/2^9   |             |   3^1/2^1   |             |   3^8/2^12  |             |   3^3/2^4   |   2^4/3^2   |             |             |   3^5/2^7   |   2^1/1^1   ]
 Rati3 [    3⁰/2⁰    |             |    3⁷/2¹¹   |             |    3²/2³    |             |    3⁹/2¹⁴   |             |    3⁴/2⁶    |    2²/3¹    |             |             |    3⁶/2⁹    |             |    3¹/2¹    |             |    3⁸/2¹²   |             |    3³/2⁴    |    2⁴/3²    |             |             |    3⁵/2⁷    |    2¹/1¹    ]
 Cents [    0.000    |             |    113.7    |             |    203.9    |             |    317.6    |             |    407.8    |    498.0    |             |             |    611.7    |             |    702.0    |             |    815.6    |             |    905.9    |    996.1    |             |             |     1110    |     1200    ] cents
 dCent [    +0.00    |             |    +13.7    |             |    +3.91    |             |    +17.6    |             |    +7.82    |    -1.96    |             |             |    +11.7    |             |    +1.96    |             |    +15.6    |             |    +5.87    |    -3.91    |             |             |    +9.78    |    +0.00    ] cents
 Freq  [ 349.2282314 |             | 372.9307335 |             | 392.8817604 |             | 419.5470752 |             | 441.9919804 | 465.6376419 |             |             | 497.2409780 |             | 523.8423471 |             | 559.3961002 |             | 589.3226405 | 620.8501892 |             |             | 662.9879706 | 698.4564629 ] Hz
 Wavln [ 98.78926414 |             | 92.51047689 |             | 87.81267924 |             | 82.23153501 |             | 78.05571488 | 74.09194810 |             |             | 69.38285767 |             | 65.85950943 |             | 61.67365126 |             | 58.54178616 | 55.56896108 |             |             | 52.03714325 | 49.39463207 ] cm
  ABC1 [   3  2  1   |             |   3  2  2   |             |   3  2  3   |             |   3  2  4   |             |   3  2  5   |   3  2  6   |             |             |   3  2  7   |             |   3  2  8   |             |   3  2  9   |             |             |             ]
  ABC2 [   2  3  1   |             |   2  3  2   |             |             |             |             |             |             |             |             |             |             ]
  ABC3 [   3  2  0   |             |   3  2  1   |             |   3  2  2   |             |   3  2  3   |             |   3  2  4   |   3  2  5   |             |             |   3  2  6   |             |   3  2  7   |             |   3  2  8   |             |   3  2  9   |   2  3  1   |             |             |   2  3  2   |   2  1  1   ]
  ABC4 [   3  2  0   |             |   3  2  7   |             |   3  2  2   |             |   3  2  9   |             |   3  2  4   |   2  3  1   |             |             |   3  2  6   |             |   3  2  1   |             |   3  2  8   |             |   3  2  3   |   2  3  2   |             |             |   3  2  5   |   2  1  1   ]
        -------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------
0 50 D [      0      |     90      |             |             |     204     |     294     |             |             |     408     |     498     |             |             |     612     |             |     702     |     792     |             |             |     906     |     996     |             |             |    1110     |    1200     ]
1 57 A [      0      |     90      |             |             |     204     |     294     |             |             |     408     |     498     |             |     588     |             |             |     702     |     792     |             |             |     906     |     996     |             |             |    1110     |    1200     ]
2 52 E [      0      |     90      |             |             |     204     |     294     |             |             |     408     |     498     |             |     588     |             |             |     702     |     792     |             |             |     906     |     996     |             |    1086     |             |    1200     ]
3 59 B [      0      |     90      |             |             |     204     |     294     |             |     384     |             |     498     |             |     588     |             |             |     702     |     792     |             |             |     906     |     996     |             |    1086     |             |    1200     ]
4 54 F♯[      0      |     90      |             |             |     204     |     294     |             |     384     |             |     498     |             |     588     |             |             |     702     |     792     |             |     882     |             |     996     |             |    1086     |             |    1200     ]
5 61 C♯[      0      |     90      |             |     180     |             |     294     |             |     384     |             |     498     |             |     588     |             |             |     702     |     792     |             |     882     |             |     996     |             |    1086     |             |    1200     ]
6 56 G♯[      0      |     90      |             |     180     |             |     294     |             |     384     |             |     498     |             |     588     |             |     678     |             |     792     |             |     882     |             |     996     |             |    1086     |             |    1200     ]
7 55 G [      0      |             |     114     |             |     204     |     294     |             |             |     408     |     498     |             |             |     612     |             |     702     |     792     |             |             |     906     |     996     |             |             |    1110     |    1200     ]
8 60 C [      0      |             |     114     |             |     204     |     294     |             |             |     408     |     498     |             |             |     612     |             |     702     |             |     816     |             |     906     |     996     |             |             |    1110     |    1200     ]
9 53 F [      0      |             |     114     |             |     204     |             |     318     |             |     408     |     498     |             |             |     612     |             |     702     |             |     816     |             |     906     |     996     |             |             |    1110     |    1200     ]
        -------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------
   k          0             1             2             3             4             5             6             7             8             9            10            11            12            13            14            15            16            17            18            19            20            21            22            23      
        -------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------
 Index [      0      |             |      1      |             |      2      |             |      3      |             |      4      |      5      |             |             |      6      |             |      7      |             |      8      |             |      9      |             |     10      |             |     11      |     12      ]
 Note  [     B♭      |             |      B      |             |      C      |             |    D♭/C♯    |             |      D      |    E♭/D♯    |             |             |      E      |             |      F      |             |    G♭/F♯    |             |      G      |             |    A♭/G♯    |             |      A      |     B♭      ]
 Intrv [     P1      |             |     A1      |             |     M2      |             |     A2      |             |     M3      |     P4      |             |             |     A4      |             |     P5      |             |     A5      |             |     M6      |             |     A6      |             |     M7      |     P8      ]
 Ratio [ 1.000000000 |             | 1.067871094 |             | 1.125000000 |             | 1.201354980 |             | 1.265625000 | 1.333333333 |             |             | 1.423828125 |             | 1.500000000 |             | 1.601806641 |             | 1.687500000 |             | 1.802032471 |             | 1.898437500 | 2.000000000 ]
 Rati1 [     1/1     |             |  2187/2048  |             |     9/8     |             | 19683/16384 |             |    81/64    |     4/3     |             |             |   729/512   |             |     3/2     |             |  6561/4096  |             |    27/16    |             | 59049/32768 |             |   243/128   |     2/1     ]
 Rati2 [   3^0/2^0   |             |   3^7/2^11  |             |   3^2/2^3   |             |   3^9/2^14  |             |   3^4/2^6   |   2^2/3^1   |             |             |   3^6/2^9   |             |   3^1/2^1   |             |   3^8/2^12  |             |   3^3/2^4   |             |  3^10/2^15  |             |   3^5/2^7   |   2^1/1^1   ]
 Rati3 [    3⁰/2⁰    |             |    3⁷/2¹¹   |             |    3²/2³    |             |    3⁹/2¹⁴   |             |    3⁴/2⁶    |    2²/3¹    |             |             |    3⁶/2⁹    |             |    3¹/2¹    |             |    3⁸/2¹²   |             |    3³/2⁴    |             |   3¹⁰/2¹⁵   |             |    3⁵/2⁷    |    2¹/1¹    ]
 Cents [    0.000    |             |    113.7    |             |    203.9    |             |    317.6    |             |    407.8    |    498.0    |             |             |    611.7    |             |    702.0    |             |    815.6    |             |    905.9    |             |     1020    |             |     1110    |     1200    ] cents
 dCent [    +0.00    |             |    +13.7    |             |    +3.91    |             |    +17.6    |             |    +7.82    |    -1.96    |             |             |    +11.7    |             |    +1.96    |             |    +15.6    |             |    +5.87    |             |    +19.6    |             |    +9.78    |    +0.00    ] cents
 Freq  [ 466.1637615 |             | 497.8028059 |             | 524.4342317 |             | 560.0281566 |             | 589.9885107 | 621.5516820 |             |             | 663.7370745 |             | 699.2456423 |             | 746.7042088 |             | 786.6513476 |             | 840.0422349 |             | 884.9827660 | 932.3275230 ] Hz
 Wavln [ 74.00832679 |             | 69.30455110 |             | 65.78517937 |             | 61.60404543 |             | 58.47571499 | 55.50624509 |             |             | 51.97841333 |             | 49.33888453 |             | 46.20303407 |             | 43.85678625 |             | 41.06936362 |             | 38.98381000 | 37.00416339 ] cm
  ABC1 [   3  2  1   |             |   3  2  2   |             |   3  2  3   |             |   3  2  4   |             |   3  2  5   |   3  2  6   |             |             |   3  2  7   |             |   3  2  8   |             |   3  2  9   |             |   3  2 10   |             |             ]
  ABC2 [   2  3  1   |             |             |             |             |             |             |             |             |             |             |             ]
  ABC3 [   3  2  0   |             |   3  2  1   |             |   3  2  2   |             |   3  2  3   |             |   3  2  4   |   3  2  5   |             |             |   3  2  6   |             |   3  2  7   |             |   3  2  8   |             |   3  2  9   |             |   3  2 10   |             |   2  3  1   |   2  1  1   ]
  ABC4 [   3  2  0   |             |   3  2  7   |             |   3  2  2   |             |   3  2  9   |             |   3  2  4   |   2  3  1   |             |             |   3  2  6   |             |   3  2  1   |             |   3  2  8   |             |   3  2  3   |             |   3  2 10   |             |   3  2  5   |   2  1  1   ]
        -------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------
0 50 D [      0      |     90      |             |             |     204     |     294     |             |             |     408     |     498     |             |             |     612     |             |     702     |     792     |             |             |     906     |     996     |             |             |    1110     |    1200     ]
1 57 A [      0      |     90      |             |             |     204     |     294     |             |             |     408     |     498     |             |     588     |             |             |     702     |     792     |             |             |     906     |     996     |             |             |    1110     |    1200     ]
2 52 E [      0      |     90      |             |             |     204     |     294     |             |             |     408     |     498     |             |     588     |             |             |     702     |     792     |             |             |     906     |     996     |             |    1086     |             |    1200     ]
3 59 B [      0      |     90      |             |             |     204     |     294     |             |     384     |             |     498     |             |     588     |             |             |     702     |     792     |             |             |     906     |     996     |             |    1086     |             |    1200     ]
4 54 F♯[      0      |     90      |             |             |     204     |     294     |             |     384     |             |     498     |             |     588     |             |             |     702     |     792     |             |     882     |             |     996     |             |    1086     |             |    1200     ]
5 61 C♯[      0      |     90      |             |     180     |             |     294     |             |     384     |             |     498     |             |     588     |             |             |     702     |     792     |             |     882     |             |     996     |             |    1086     |             |    1200     ]
6 56 G♯[      0      |     90      |             |     180     |             |     294     |             |     384     |             |     498     |             |     588     |             |     678     |             |     792     |             |     882     |             |     996     |             |    1086     |             |    1200     ]
7 55 G [      0      |             |     114     |             |     204     |     294     |             |             |     408     |     498     |             |             |     612     |             |     702     |     792     |             |             |     906     |     996     |             |             |    1110     |    1200     ]
8 60 C [      0      |             |     114     |             |     204     |     294     |             |             |     408     |     498     |             |             |     612     |             |     702     |             |     816     |             |     906     |     996     |             |             |    1110     |    1200     ]
9 53 F [      0      |             |     114     |             |     204     |             |     318     |             |     408     |     498     |             |             |     612     |             |     702     |             |     816     |             |     906     |     996     |             |             |    1110     |    1200     ]
a 58 B♭[      0      |             |     114     |             |     204     |             |     318     |             |     408     |     498     |             |             |     612     |             |     702     |             |     816     |             |     906     |             |    1020     |             |    1110     |    1200     ]
        -------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------
   k          0             1             2             3             4             5             6             7             8             9            10            11            12            13            14            15            16            17            18            19            20            21            22            23      
        -------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------
 Index [      0      |             |      1      |             |      2      |             |      3      |             |      4      |             |      5      |             |      6      |             |      7      |             |      8      |             |      9      |             |     10      |             |     11      |     12      ]
 Note  [     E♭      |             |      E      |             |      F      |             |    G♭/F♯    |             |      G      |             |    A♭/G♯    |             |      A      |             |    B♭/A♯    |             |      B      |             |      C      |             |    D♭/C♯    |             |      D      |     E♭      ]
 Intrv [     P1      |             |     A1      |             |     M2      |             |     A2      |             |     M3      |             |     A3      |             |     A4      |             |     P5      |             |     A5      |             |     M6      |             |     A6      |             |     M7      |     P8      ]
 Ratio [ 1.000000000 |             | 1.067871094 |             | 1.125000000 |             | 1.201354980 |             | 1.265625000 |             | 1.351524353 |             | 1.423828125 |             | 1.500000000 |             | 1.601806641 |             | 1.687500000 |             | 1.802032471 |             | 1.898437500 | 2.000000000 ]
 Rati1 [     1/1     |             |  2187/2048  |             |     9/8     |             | 19683/16384 |             |    81/64    |             |177147/131072|             |   729/512   |             |     3/2     |             |  6561/4096  |             |    27/16    |             | 59049/32768 |             |   243/128   |     2/1     ]
 Rati2 [   3^0/2^0   |             |   3^7/2^11  |             |   3^2/2^3   |             |   3^9/2^14  |             |   3^4/2^6   |             |  3^11/2^17  |             |   3^6/2^9   |             |   3^1/2^1   |             |   3^8/2^12  |             |   3^3/2^4   |             |  3^10/2^15  |             |   3^5/2^7   |   2^1/1^1   ]
 Rati3 [    3⁰/2⁰    |             |    3⁷/2¹¹   |             |    3²/2³    |             |    3⁹/2¹⁴   |             |    3⁴/2⁶    |             |   3¹¹/2¹⁷   |             |    3⁶/2⁹    |             |    3¹/2¹    |             |    3⁸/2¹²   |             |    3³/2⁴    |             |   3¹⁰/2¹⁵   |             |    3⁵/2⁷    |    2¹/1¹    ]
 Cents [    0.000    |             |    113.7    |             |    203.9    |             |    317.6    |             |    407.8    |             |    521.5    |             |    611.7    |             |    702.0    |             |    815.6    |             |    905.9    |             |     1020    |             |     1110    |     1200    ] cents
 dCent [    +0.00    |             |    +13.7    |             |    +3.91    |             |    +17.6    |             |    +7.82    |             |    +21.5    |             |    +11.7    |             |    +1.96    |             |    +15.6    |             |    +5.87    |             |    +19.6    |             |    +9.78    |    +0.00    ] cents
 Freq  [ 311.1269837 |             | 332.2435124 |             | 350.0178567 |             | 373.7739515 |             | 393.7700888 |             | 420.4956954 |             | 442.9913499 |             | 466.6904756 |             | 498.3652686 |             | 525.0267850 |             | 560.6609272 |             | 590.6551332 | 622.2539674 ] Hz
 Wavln [ 110.8871998 |             | 103.8394994 |             | 98.56639980 |             | 92.30177723 |             | 87.61457760 |             | 82.04602420 |             | 77.87962453 |             | 73.92479985 |             | 69.22633292 |             | 65.71093320 |             | 61.53451815 |             | 58.40971840 | 55.44359989 ] cm
  ABC1 [   3  2  1   |             |   3  2  2   |             |   3  2  3   |             |   3  2  4   |             |   3  2  5   |             |   3  2  6   |             |   3  2  7   |             |   3  2  8   |             |   3  2  9   |             |   3  2 10   |             |   3  2 11   |             ]
  ABC2 [             |             |             |             |             |             |             |             |             |             |             ]
  ABC3 [   3  2  0   |             |   3  2  1   |             |   3  2  2   |             |   3  2  3   |             |   3  2  4   |             |   3  2  5   |             |   3  2  6   |             |   3  2  7   |             |   3  2  8   |             |   3  2  9   |             |   3  2 10   |             |   3  2 11   |   2  1  1   ]
  ABC4 [   3  2  0   |             |   3  2  7   |             |   3  2  2   |             |   3  2  9   |             |   3  2  4   |             |   3  2 11   |             |   3  2  6   |             |   3  2  1   |             |   3  2  8   |             |   3  2  3   |             |   3  2 10   |             |   3  2  5   |   2  1  1   ]
        -------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------
0 50 D [      0      |     90      |             |             |     204     |     294     |             |             |     408     |     498     |             |             |     612     |             |     702     |     792     |             |             |     906     |     996     |             |             |    1110     |    1200     ]
1 57 A [      0      |     90      |             |             |     204     |     294     |             |             |     408     |     498     |             |     588     |             |             |     702     |     792     |             |             |     906     |     996     |             |             |    1110     |    1200     ]
2 52 E [      0      |     90      |             |             |     204     |     294     |             |             |     408     |     498     |             |     588     |             |             |     702     |     792     |             |             |     906     |     996     |             |    1086     |             |    1200     ]
3 59 B [      0      |     90      |             |             |     204     |     294     |             |     384     |             |     498     |             |     588     |             |             |     702     |     792     |             |             |     906     |     996     |             |    1086     |             |    1200     ]
4 54 F♯[      0      |     90      |             |             |     204     |     294     |             |     384     |             |     498     |             |     588     |             |             |     702     |     792     |             |     882     |             |     996     |             |    1086     |             |    1200     ]
5 61 C♯[      0      |     90      |             |     180     |             |     294     |             |     384     |             |     498     |             |     588     |             |             |     702     |     792     |             |     882     |             |     996     |             |    1086     |             |    1200     ]
6 56 G♯[      0      |     90      |             |     180     |             |     294     |             |     384     |             |     498     |             |     588     |             |     678     |             |     792     |             |     882     |             |     996     |             |    1086     |             |    1200     ]
7 55 G [      0      |             |     114     |             |     204     |     294     |             |             |     408     |     498     |             |             |     612     |             |     702     |     792     |             |             |     906     |     996     |             |             |    1110     |    1200     ]
8 60 C [      0      |             |     114     |             |     204     |     294     |             |             |     408     |     498     |             |             |     612     |             |     702     |             |     816     |             |     906     |     996     |             |             |    1110     |    1200     ]
9 53 F [      0      |             |     114     |             |     204     |             |     318     |             |     408     |     498     |             |             |     612     |             |     702     |             |     816     |             |     906     |     996     |             |             |    1110     |    1200     ]
a 58 B♭[      0      |             |     114     |             |     204     |             |     318     |             |     408     |     498     |             |             |     612     |             |     702     |             |     816     |             |     906     |             |    1020     |             |    1110     |    1200     ]
b 51 E♭[      0      |             |     114     |             |     204     |             |     318     |             |     408     |             |     522     |             |     612     |             |     702     |             |     816     |             |     906     |             |    1020     |             |    1110     |    1200     ]
        -------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------
'''
'''        
j j*100 i Iv  c     k       d       e       c`   Iv  c     k       d       e       c`
0    0  0 P1  1 @    0 :   0.000 = 1.955 *  0    d2  0 @   24 :         = 1.955 *  1
1  100  2 m2  1 @   90 :  -9.780 = 1.955 *  0    A1  0 @  114 :         = 1.955 *  1
2  200  4 M2  1 @  204 :   3.910 = 1.955 *  0    d3  0 @  180 :         = 1.955 *  1
3  300  6 m3  1 @  294 :  -5.870 = 1.955 *  0    A2  0 @  318 :         = 1.955 *  1
4  400  8 M3  1 @  408 :   7.820 = 1.955 *  0    d4  0 @  384 :         = 1.955 *  1
5  500 10 P4  1 @  498 :  -1.960 = 1.955 *  0    A3  0 @  522 :         = 1.955 *  1
6  600 12 A4  1 @  612 :  11.730 = 1.955 *  0    d5  0 @  588 :         = 1.955 *  1
7  700 14 P5  1 @  702 :   1.960 = 1.955 *  0    d6  0 @  678 :         = 1.955 *  1
8  800 16 m6  1 @  792 :  -7.820 = 1.955 *  0    A5  0 @  816 :         = 1.955 *  1
9  900 18 M6  1 @  906 :   5.870 = 1.955 *  0    d7  0 @  882 :         = 1.955 *  1
a 1000 20 m7  1 @  996 :  -3.910 = 1.955 *  0    A6  0 @ 1020 :         = 1.955 *  1
b 1100 22 M7  1 @ 1110 :   9.780 = 1.955 *  0    d8  0 @ 1086 :         = 1.955 *  1
c 1200 24 P8  1 @ 1200 :   0.000 = 1.955 *  0    A7  0 @ 1178 :         = 1.955 *  1

j j*100 i Iv  c     k       d       e       c`   Iv  c     k       d       e       c`
0    0  0 P1  2 @    0 :   0.000 = 1.955 *  0    d2  0 @   24 :         = 1.955 *  2
1  100  2 m2  2 @   90 :  -9.780 = 1.955 *  0    A1  0 @  114 :         = 1.955 *  2
2  200  4 M2  2 @  204 :   3.910 = 1.955 *  0    d3  0 @  180 :         = 1.955 *  2
3  300  6 m3  2 @  294 :  -5.870 = 1.955 *  0    A2  0 @  318 :         = 1.955 *  2
4  400  8 M3  2 @  408 :   7.820 = 1.955 *  0    d4  0 @  384 :         = 1.955 *  2
5  500 10 P4  2 @  498 :  -1.960 = 1.955 *  0    A3  0 @  522 :         = 1.955 *  2
6  600 12 A4  1 @  612 :  11.730 = 1.955 *  1    d5  1 @  588 : -11.730 = 1.955 *  1
7  700 14 P5  2 @  702 :   1.960 = 1.955 *  0    d6  0 @  678 :         = 1.955 *  2
8  800 16 m6  2 @  792 :  -7.820 = 1.955 *  0    A5  0 @  816 :         = 1.955 *  2
9  900 18 M6  2 @  906 :   5.870 = 1.955 *  0    d7  0 @  882 :         = 1.955 *  2
a 1000 20 m7  2 @  996 :  -3.910 = 1.955 *  0    A6  0 @ 1020 :         = 1.955 *  2
b 1100 22 M7  2 @ 1110 :   9.780 = 1.955 *  0    d8  0 @ 1086 :         = 1.955 *  2
c 1200 24 P8  2 @ 1200 :   0.000 = 1.955 *  0    A7  0 @ 1178 :         = 1.955 *  2

j j*100 i Iv  c     k       d       e       c`   Iv  c     k       d       e       c`
0    0  0 P1  3 @    0 :   0.000 = 1.955 *  0    d2  0 @   24 :         = 1.955 *  3
1  100  2 m2  3 @   90 :  -9.780 = 1.955 *  0    A1  0 @  114 :         = 1.955 *  3
2  200  4 M2  3 @  204 :   3.910 = 1.955 *  0    d3  0 @  180 :         = 1.955 *  3
3  300  6 m3  3 @  294 :  -5.870 = 1.955 *  0    A2  0 @  318 :         = 1.955 *  3
4  400  8 M3  3 @  408 :   7.820 = 1.955 *  0    d4  0 @  384 :         = 1.955 *  3
5  500 10 P4  3 @  498 :  -1.960 = 1.955 *  0    A3  0 @  522 :         = 1.955 *  3
6  600 12 A4  1 @  612 :  11.730 = 1.955 *  2    d5  2 @  588 : -11.730 = 1.955 *  1
7  700 14 P5  3 @  702 :   1.960 = 1.955 *  0    d6  0 @  678 :         = 1.955 *  3
8  800 16 m6  3 @  792 :  -7.820 = 1.955 *  0    A5  0 @  816 :         = 1.955 *  3
9  900 18 M6  3 @  906 :   5.870 = 1.955 *  0    d7  0 @  882 :         = 1.955 *  3
a 1000 20 m7  3 @  996 :  -3.910 = 1.955 *  0    A6  0 @ 1020 :         = 1.955 *  3
b 1100 22 M7  2 @ 1110 :   9.780 = 1.955 *  1    d8  1 @ 1086 : -13.690 = 1.955 *  2
c 1200 24 P8  3 @ 1200 :   0.000 = 1.955 *  0    A7  0 @ 1178 :         = 1.955 *  3

j j*100 i Iv  c     k       d       e       c`   Iv  c     k       d       e       c`
0    0  0 P1  4 @    0 :   0.000 = 1.955 *  0    d2  0 @   24 :         = 1.955 *  4
1  100  2 m2  4 @   90 :  -9.780 = 1.955 *  0    A1  0 @  114 :         = 1.955 *  4
2  200  4 M2  4 @  204 :   3.910 = 1.955 *  0    d3  0 @  180 :         = 1.955 *  4
3  300  6 m3  4 @  294 :  -5.870 = 1.955 *  0    A2  0 @  318 :         = 1.955 *  4
4  400  8 M3  3 @  408 :   7.820 = 1.955 *  1    d4  1 @  384 : -15.640 = 1.955 *  3
5  500 10 P4  4 @  498 :  -1.960 = 1.955 *  0    A3  0 @  522 :         = 1.955 *  4
6  600 12 A4  1 @  612 :  11.730 = 1.955 *  3    d5  3 @  588 : -11.730 = 1.955 *  1
7  700 14 P5  4 @  702 :   1.960 = 1.955 *  0    d6  0 @  678 :         = 1.955 *  4
8  800 16 m6  4 @  792 :  -7.820 = 1.955 *  0    A5  0 @  816 :         = 1.955 *  4
9  900 18 M6  4 @  906 :   5.870 = 1.955 *  0    d7  0 @  882 :         = 1.955 *  4
a 1000 20 m7  4 @  996 :  -3.910 = 1.955 *  0    A6  0 @ 1020 :         = 1.955 *  4
b 1100 22 M7  2 @ 1110 :   9.780 = 1.955 *  2    d8  2 @ 1086 : -13.690 = 1.955 *  2
c 1200 24 P8  4 @ 1200 :   0.000 = 1.955 *  0    A7  0 @ 1178 :         = 1.955 *  4

j j*100 i Iv  c     k       d       e       c`   Iv  c     k       d       e       c`
0    0  0 P1  5 @    0 :   0.000 = 1.955 *  0    d2  0 @   24 :         = 1.955 *  5
1  100  2 m2  5 @   90 :  -9.780 = 1.955 *  0    A1  0 @  114 :         = 1.955 *  5
2  200  4 M2  5 @  204 :   3.910 = 1.955 *  0    d3  0 @  180 :         = 1.955 *  5
3  300  6 m3  5 @  294 :  -5.870 = 1.955 *  0    A2  0 @  318 :         = 1.955 *  5
4  400  8 M3  3 @  408 :   7.820 = 1.955 *  2    d4  2 @  384 : -15.640 = 1.955 *  3
5  500 10 P4  5 @  498 :  -1.960 = 1.955 *  0    A3  0 @  522 :         = 1.955 *  5
6  600 12 A4  1 @  612 :  11.730 = 1.955 *  4    d5  4 @  588 : -11.730 = 1.955 *  1
7  700 14 P5  5 @  702 :   1.960 = 1.955 *  0    d6  0 @  678 :         = 1.955 *  5
8  800 16 m6  5 @  792 :  -7.820 = 1.955 *  0    A5  0 @  816 :         = 1.955 *  5
9  900 18 M6  4 @  906 :   5.870 = 1.955 *  1    d7  1 @  882 : -17.600 = 1.955 *  4
a 1000 20 m7  5 @  996 :  -3.910 = 1.955 *  0    A6  0 @ 1020 :         = 1.955 *  5
b 1100 22 M7  2 @ 1110 :   9.780 = 1.955 *  3    d8  3 @ 1086 : -13.690 = 1.955 *  2
c 1200 24 P8  5 @ 1200 :   0.000 = 1.955 *  0    A7  0 @ 1178 :         = 1.955 *  5

j j*100 i Iv  c     k       d       e       c`   Iv  c     k       d       e       c`
0    0  0 P1  6 @    0 :   0.000 = 1.955 *  0    d2  0 @   24 :         = 1.955 *  6
1  100  2 m2  6 @   90 :  -9.780 = 1.955 *  0    A1  0 @  114 :         = 1.955 *  6
2  200  4 M2  5 @  204 :   3.910 = 1.955 *  1    d3  1 @  180 : -19.550 = 1.955 *  5
3  300  6 m3  6 @  294 :  -5.870 = 1.955 *  0    A2  0 @  318 :         = 1.955 *  6
4  400  8 M3  3 @  408 :   7.820 = 1.955 *  3    d4  3 @  384 : -15.640 = 1.955 *  3
5  500 10 P4  6 @  498 :  -1.960 = 1.955 *  0    A3  0 @  522 :         = 1.955 *  6
6  600 12 A4  1 @  612 :  11.730 = 1.955 *  5    d5  5 @  588 : -11.730 = 1.955 *  1
7  700 14 P5  6 @  702 :   1.960 = 1.955 *  0    d6  0 @  678 :         = 1.955 *  6
8  800 16 m6  6 @  792 :  -7.820 = 1.955 *  0    A5  0 @  816 :         = 1.955 *  6
9  900 18 M6  4 @  906 :   5.870 = 1.955 *  2    d7  2 @  882 : -17.600 = 1.955 *  4
a 1000 20 m7  6 @  996 :  -3.910 = 1.955 *  0    A6  0 @ 1020 :         = 1.955 *  6
b 1100 22 M7  2 @ 1110 :   9.780 = 1.955 *  4    d8  4 @ 1086 : -13.690 = 1.955 *  2
c 1200 24 P8  6 @ 1200 :   0.000 = 1.955 *  0    A7  0 @ 1178 :         = 1.955 *  6

j j*100 i Iv  c     k       d       e       c`   Iv  c     k       d       e       c`
0    0  0 P1  7 @    0 :   0.000 = 1.955 *  0    d2  0 @   24 :         = 1.955 *  7
1  100  2 m2  7 @   90 :  -9.780 = 1.955 *  0    A1  0 @  114 :         = 1.955 *  7
2  200  4 M2  5 @  204 :   3.910 = 1.955 *  2    d3  2 @  180 : -19.550 = 1.955 *  5
3  300  6 m3  7 @  294 :  -5.870 = 1.955 *  0    A2  0 @  318 :         = 1.955 *  7
4  400  8 M3  3 @  408 :   7.820 = 1.955 *  4    d4  4 @  384 : -15.640 = 1.955 *  3
5  500 10 P4  7 @  498 :  -1.960 = 1.955 *  0    A3  0 @  522 :         = 1.955 *  7
6  600 12 A4  1 @  612 :  11.730 = 1.955 *  6    d5  6 @  588 : -11.730 = 1.955 *  1
7  700 14 P5  6 @  702 :   1.960 = 1.955 *  1    d6  1 @  678 : -21.510 = 1.955 *  6
8  800 16 m6  7 @  792 :  -7.820 = 1.955 *  0    A5  0 @  816 :         = 1.955 *  7
9  900 18 M6  4 @  906 :   5.870 = 1.955 *  3    d7  3 @  882 : -17.600 = 1.955 *  4
a 1000 20 m7  7 @  996 :  -3.910 = 1.955 *  0    A6  0 @ 1020 :         = 1.955 *  7
b 1100 22 M7  2 @ 1110 :   9.780 = 1.955 *  5    d8  5 @ 1086 : -13.690 = 1.955 *  2
c 1200 24 P8  7 @ 1200 :   0.000 = 1.955 *  0    A7  0 @ 1178 :         = 1.955 *  7

j j*100 i Iv  c     k       d       e       c`   Iv  c     k       d       e       c`
0    0  0 P1  8 @    0 :   0.000 = 1.955 *  0    d2  0 @   24 :         = 1.955 *  8
1  100  2 m2  7 @   90 :  -9.780 = 1.955 *  1    A1  1 @  114 :  13.690 = 1.955 *  7
2  200  4 M2  6 @  204 :   3.910 = 1.955 *  2    d3  2 @  180 : -19.550 = 1.955 *  6
3  300  6 m3  8 @  294 :  -5.870 = 1.955 *  0    A2  0 @  318 :         = 1.955 *  8
4  400  8 M3  4 @  408 :   7.820 = 1.955 *  4    d4  4 @  384 : -15.640 = 1.955 *  4
5  500 10 P4  8 @  498 :  -1.960 = 1.955 *  0    A3  0 @  522 :         = 1.955 *  8
6  600 12 A4  2 @  612 :  11.730 = 1.955 *  6    d5  6 @  588 : -11.730 = 1.955 *  2
7  700 14 P5  7 @  702 :   1.960 = 1.955 *  1    d6  1 @  678 : -21.510 = 1.955 *  7
8  800 16 m6  8 @  792 :  -7.820 = 1.955 *  0    A5  0 @  816 :         = 1.955 *  8
9  900 18 M6  5 @  906 :   5.870 = 1.955 *  3    d7  3 @  882 : -17.600 = 1.955 *  5
a 1000 20 m7  8 @  996 :  -3.910 = 1.955 *  0    A6  0 @ 1020 :         = 1.955 *  8
b 1100 22 M7  3 @ 1110 :   9.780 = 1.955 *  5    d8  5 @ 1086 : -13.690 = 1.955 *  3
c 1200 24 P8  8 @ 1200 :   0.000 = 1.955 *  0    A7  0 @ 1178 :         = 1.955 *  8

j j*100 i Iv  c     k       d       e       c`   Iv  c     k       d       e       c`
0    0  0 P1  9 @    0 :   0.000 = 1.955 *  0    d2  0 @   24 :         = 1.955 *  9
1  100  2 m2  7 @   90 :  -9.780 = 1.955 *  2    A1  2 @  114 :  13.690 = 1.955 *  7
2  200  4 M2  7 @  204 :   3.910 = 1.955 *  2    d3  2 @  180 : -19.550 = 1.955 *  7
3  300  6 m3  9 @  294 :  -5.870 = 1.955 *  0    A2  0 @  318 :         = 1.955 *  9
4  400  8 M3  5 @  408 :   7.820 = 1.955 *  4    d4  4 @  384 : -15.640 = 1.955 *  5
5  500 10 P4  9 @  498 :  -1.960 = 1.955 *  0    A3  0 @  522 :         = 1.955 *  9
6  600 12 A4  3 @  612 :  11.730 = 1.955 *  6    d5  6 @  588 : -11.730 = 1.955 *  3
7  700 14 P5  8 @  702 :   1.960 = 1.955 *  1    d6  1 @  678 : -21.510 = 1.955 *  8
8  800 16 m6  8 @  792 :  -7.820 = 1.955 *  1    A5  1 @  816 :  15.640 = 1.955 *  8
9  900 18 M6  6 @  906 :   5.870 = 1.955 *  3    d7  3 @  882 : -17.600 = 1.955 *  6
a 1000 20 m7  9 @  996 :  -3.910 = 1.955 *  0    A6  0 @ 1020 :         = 1.955 *  9
b 1100 22 M7  4 @ 1110 :   9.780 = 1.955 *  5    d8  5 @ 1086 : -13.690 = 1.955 *  4
c 1200 24 P8  9 @ 1200 :   0.000 = 1.955 *  0    A7  0 @ 1178 :         = 1.955 *  9

j j*100 i Iv  c     k       d       e       c`   Iv  c     k       d       e       c`
0    0  0 P1 10 @    0 :   0.000 = 1.955 *  0    d2  0 @   24 :         = 1.955 * 10
1  100  2 m2  7 @   90 :  -9.780 = 1.955 *  3    A1  3 @  114 :  13.690 = 1.955 *  7
2  200  4 M2  8 @  204 :   3.910 = 1.955 *  2    d3  2 @  180 : -19.550 = 1.955 *  8
3  300  6 m3  9 @  294 :  -5.870 = 1.955 *  1    A2  1 @  318 :  17.600 = 1.955 *  9
4  400  8 M3  6 @  408 :   7.820 = 1.955 *  4    d4  4 @  384 : -15.640 = 1.955 *  6
5  500 10 P4 10 @  498 :  -1.960 = 1.955 *  0    A3  0 @  522 :         = 1.955 * 10
6  600 12 A4  4 @  612 :  11.730 = 1.955 *  6    d5  6 @  588 : -11.730 = 1.955 *  4
7  700 14 P5  9 @  702 :   1.960 = 1.955 *  1    d6  1 @  678 : -21.510 = 1.955 *  9
8  800 16 m6  8 @  792 :  -7.820 = 1.955 *  2    A5  2 @  816 :  15.640 = 1.955 *  8
9  900 18 M6  7 @  906 :   5.870 = 1.955 *  3    d7  3 @  882 : -17.600 = 1.955 *  7
a 1000 20 m7 10 @  996 :  -3.910 = 1.955 *  0    A6  0 @ 1020 :         = 1.955 * 10
b 1100 22 M7  5 @ 1110 :   9.780 = 1.955 *  5    d8  5 @ 1086 : -13.690 = 1.955 *  5
c 1200 24 P8 10 @ 1200 :   0.000 = 1.955 *  0    A7  0 @ 1178 :         = 1.955 * 10

j j*100 i Iv  c     k       d       e       c`   Iv  c     k       d       e       c`
0    0  0 P1 11 @    0 :   0.000 = 1.955 *  0    d2  0 @   24 :         = 1.955 * 11
1  100  2 m2  7 @   90 :  -9.780 = 1.955 *  4    A1  4 @  114 :  13.690 = 1.955 *  7
2  200  4 M2  9 @  204 :   3.910 = 1.955 *  2    d3  2 @  180 : -19.550 = 1.955 *  9
3  300  6 m3  9 @  294 :  -5.870 = 1.955 *  2    A2  2 @  318 :  17.600 = 1.955 *  9
4  400  8 M3  7 @  408 :   7.820 = 1.955 *  4    d4  4 @  384 : -15.640 = 1.955 *  7
5  500 10 P4 11 @  498 :  -1.960 = 1.955 *  0    A3  0 @  522 :         = 1.955 * 11
6  600 12 A4  5 @  612 :  11.730 = 1.955 *  6    d5  6 @  588 : -11.730 = 1.955 *  5
7  700 14 P5 10 @  702 :   1.960 = 1.955 *  1    d6  1 @  678 : -21.510 = 1.955 * 10
8  800 16 m6  8 @  792 :  -7.820 = 1.955 *  3    A5  3 @  816 :  15.640 = 1.955 *  8
9  900 18 M6  8 @  906 :   5.870 = 1.955 *  3    d7  3 @  882 : -17.600 = 1.955 *  8
a 1000 20 m7 10 @  996 :  -3.910 = 1.955 *  1    A6  1 @ 1020 :  19.550 = 1.955 * 10
b 1100 22 M7  6 @ 1110 :   9.780 = 1.955 *  5    d8  5 @ 1086 : -13.690 = 1.955 *  6
c 1200 24 P8 11 @ 1200 :   0.000 = 1.955 *  0    A7  0 @ 1178 :         = 1.955 * 11

j j*100 i Iv  c     k       d       e       c`   Iv  c     k       d       e       c`
0    0  0 P1 12 @    0 :   0.000 = 1.955 *  0    d2  0 @   24 :         = 1.955 * 12
1  100  2 m2  7 @   90 :  -9.780 = 1.955 *  5    A1  5 @  114 :  13.690 = 1.955 *  7
2  200  4 M2 10 @  204 :   3.910 = 1.955 *  2    d3  2 @  180 : -19.550 = 1.955 * 10
3  300  6 m3  9 @  294 :  -5.870 = 1.955 *  3    A2  3 @  318 :  17.600 = 1.955 *  9
4  400  8 M3  8 @  408 :   7.820 = 1.955 *  4    d4  4 @  384 : -15.640 = 1.955 *  8
5  500 10 P4 11 @  498 :  -1.960 = 1.955 *  1    A3  1 @  522 :  21.510 = 1.955 * 11
6  600 12 A4  6 @  612 :  11.730 = 1.955 *  6    d5  6 @  588 : -11.730 = 1.955 *  6
7  700 14 P5 11 @  702 :   1.960 = 1.955 *  1    d6  1 @  678 : -21.510 = 1.955 * 11
8  800 16 m6  8 @  792 :  -7.820 = 1.955 *  4    A5  4 @  816 :  15.640 = 1.955 *  8
9  900 18 M6  9 @  906 :   5.870 = 1.955 *  3    d7  3 @  882 : -17.600 = 1.955 *  9
a 1000 20 m7 10 @  996 :  -3.910 = 1.955 *  2    A6  2 @ 1020 :  19.550 = 1.955 * 10
b 1100 22 M7  7 @ 1110 :   9.780 = 1.955 *  5    d8  5 @ 1086 : -13.690 = 1.955 *  7
c 1200 24 P8 12 @ 1200 :   0.000 = 1.955 *  0    A7  0 @ 1178 :         = 1.955 * 12

j j*100 i Iv  c     k       d       e       c`   Iv  c     k       d       e       c`
0|   0| 0|P1|12|@    0 :|  0.000|= 1.955|*  0   |d2| 0|@   24 :|       |= 1.955|* 12
1| 100| 2|m2| 7|@   90 :| -9.780|= 1.955|*  5   |A1| 5|@  114 :| 13.690|= 1.955|*  7
2| 200| 4|M2|10|@  204 :|  3.910|= 1.955|*  2   |d3| 2|@  180 :|-19.550|= 1.955|* 10
3| 300| 6|m3| 9|@  294 :| -5.870|= 1.955|*  3   |A2| 3|@  318 :| 17.600|= 1.955|*  9
4| 400| 8|M3| 8|@  408 :|  7.820|= 1.955|*  4   |d4| 4|@  384 :|-15.640|= 1.955|*  8
5| 500|10|P4|11|@  498 :| -1.960|= 1.955|*  1   |A3| 1|@  522 :| 21.510|= 1.955|* 11
6| 600|12|A4| 6|@  612 :| 11.730|= 1.955|*  6   |d5| 6|@  588 :|-11.730|= 1.955|*  6
7| 700|14|P5|11|@  702 :|  1.960|= 1.955|*  1   |d6| 1|@  678 :|-21.510|= 1.955|* 11
8| 800|16|m6| 8|@  792 :| -7.820|= 1.955|*  4   |A5| 4|@  816 :| 15.640|= 1.955|*  8
9| 900|18|M6| 9|@  906 :|  5.870|= 1.955|*  3   |d7| 3|@  882 :|-17.600|= 1.955|*  9
a|1000|20|m7|10|@  996 :| -3.910|= 1.955|*  2   |A6| 2|@ 1020 :| 19.550|= 1.955|* 10
b|1100|22|M7| 7|@ 1110 :|  9.780|= 1.955|*  5   |d8| 5|@ 1086 :|-13.690|= 1.955|*  7
c|1200|24|P8|12|@ 1200 :|  0.000|= 1.955|*  0   |A7| 0|@ 1178 :|       |= 1.955|* 12

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
