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
    if csv:
        global PythMap1  ;  PythMap1 = {}
        global PythMap2  ;  PythMap2 = { e: {'Count': 0} for e in CENTKEYS }
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
#    dmpPythMap2(   csv=csv)
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
            i2, c2, d2, n2, f2, w2, p2, q2, r2, s2, v2 = blnk, blnk, blnk, blnk, blnk, blnk, blnk, blnk, blnk, blnk, blnk     ;   cki += 1
            ii.append(i2)  ;  cs.append(c2)  ;  ds.append(d2)  ;  ns.append(n2)  ;  fs.append(f2)  ;  ws.append(w2)  ;  ps.append(p2)   ;   qs.append(q2)  ;  rs.append(r2)  ;  ss.append(s2)  ;  vs.append(v2)
            jj = len(ii)-1 ; abc1.insert(jj, fmtl([W, W, W], w=2, d=Z))  ;  abc2.insert(jj, fmtl([W, W, W], w=2, d=Z))  ;  abc3.insert(jj, fmtl([W, W, W], w=2, d=Z))  ;  abc4.insert(jj, fmtl([W, W, W], w=2, d=Z))
        ii.append(i)             ;   fs.append(fmtf(f, z))     ;   ps.append(p)      ;   rs.append(fmtf(r, z))     ;   cs.append(fmtf(c, y-1))   ;   rrs.append(rr)
        ns.append(n)             ;   ws.append(fmtf(w, z))     ;   qs.append(q)      ;   ss.append(s)              ;   ds.append(fmtg(d, y-1))   ;    vs.append(v)
    ii     = fmtl(ii, w=ww, s=oo, d=Z)   ;   fs = fmtl(fs, w=ww, s=oo, d=Z)   ;   cs = fmtl(cs, w=ww, s=oo, d=Z)   ;   ps  = fmtl(ps, w=ww, s=oo, d=Z)   ;   rs = fmtl(rs, w=ww, s=oo, d=Z)
    ns     = fmtl(ns, w=ww, s=oo, d=Z)   ;   ws = fmtl(ws, w=ww, s=oo, d=Z)   ;   ds = fmtl(ds, w=ww, s=oo, d=Z)   ;   qs  = fmtl(qs, w=ww, s=oo, d=Z)   ;   ss = fmtl(ss, w=ww, s=oo, d=Z)   ;   vs = fmtl(vs, w=ww, s=oo, d=Z)
    abc1   = fmtl(abc1, w=ww, s=oo, d=Z) ; abc2 = fmtl(abc2, w=ww, s=oo, d=Z) ; abc3 = fmtl(abc3, w=ww, s=oo, d=Z) ;  abc4 = fmtl(abc4, w=ww, s=oo, d=Z)
    pfxi   = f'{mm}Index{mm}{nn}[{nn}'  ;  pfxr = f'{mm}Ratio{mm}{nn}[{nn}'  ;  pfx1 = f'{mm} ABC1{mm}{nn}[{nn}'  ;  pfxf = f'{mm}Freq {mm}{nn}[{nn}'
    pfxn   = f'{mm}Note {mm}{nn}[{nn}'  ;  pfxp = f'{mm}Rati1{mm}{nn}[{nn}'  ;  pfx2 = f'{mm} ABC2{mm}{nn}[{nn}'  ;  pfxw = f'{mm}Wavln{mm}{nn}[{nn}'    
    pfxc   = f'{mm}Cents{mm}{nn}[{nn}'  ;  pfxq = f'{mm}Rati2{mm}{nn}[{nn}'  ;  pfx3 = f'{mm} ABC3{mm}{nn}[{nn}'  ;  pfxv = f'{mm}Intrv{mm}{nn}[{nn}'
    pfxd   = f'{mm}dCent{mm}{nn}[{nn}'  ;  pfxs = f'{mm}Rati3{mm}{nn}[{nn}'  ;  pfx4 = f'{mm} ABC4{mm}{nn}[{nn}'
    sfx    = f'{nn}]'            ;  sfxc = f'{nn}]{mm}cents'   ;  sfxf = f'{nn}]{mm}Hz'      ;  sfxw = f'{nn}]{mm}cm'
    PythMap1[k] = rrs # fixme this is not a very useful data, key should store all other data values as well
    slog(f'{pfxi}{ii}{sfx}',  p=0, f=ff)
    slog(f'{pfxn}{ns}{sfx}',  p=0, f=ff)
    slog(f'{pfxv}{vs}{sfx}',  p=0, f=ff)
    slog(f'{pfxr}{rs}{sfx}',  p=0, f=ff)
    slog(f'{pfxp}{ps}{sfx}',  p=0, f=ff)
    slog(f'{pfxq}{qs}{sfx}',  p=0, f=ff)
    slog(f'{pfxs}{ss}{sfx}',  p=0, f=ff)
    slog(f'{pfxc}{cs}{sfxc}', p=0, f=ff)
    slog(f'{pfxd}{ds}{sfxc}', p=0, f=ff)
    slog(f'{pfxf}{fs}{sfxf}', p=0, f=ff)
    slog(f'{pfxw}{ws}{sfxw}', p=0, f=ff)
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
    dmpPythMap2(         csv=csv)
#    dmpPythMap1(5, k, 9, csv=csv) # dupliicates counts
    dmpPythMap3(         csv=csv)
########################################################################################################################################################################################################
def dmpPythMap3(csv=0):
    if not csv:
        slog(f'      {fmtm(PythMap3, w=4, wv=2, s=3*W, d=Z)}', p=0)
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
def fIvals(data, i, csv): # j j*100 i Iv  c     k      d       e       c`   Iv  c     k      d       e       c`
    mm, nn = (Y, Y) if csv else (W, Z)   ;   fd = []   ;   w5, w7 = W*5, W*7
    for j, d in enumerate(data): # elif j in (2, 3, 4): fd.append(f'{d:2}')
        if   j==0:  fd.append(f'{d:x}')           # j
        elif j==1:  fd.append(f'{d:4}')           # j*100
        elif j==2:  fd.append(f'{d:2}')           # i
        elif j==3:  fd.append(f'{d:2}')           # Iv
        elif j==4:  fd.append(f'{d:2}')           # c
        elif j==5:  fd.append(f'@{mm}{d:4}{mm}:') # k
        elif j==6:  fd.append(f'{d:7.3f}')        # d
        elif j==7:  fd.append(f'={mm}{d:5.3f}')   # e
        elif j==8:  fd.append(f'*{mm}{d:2}')      # c`
        elif j==9:  fd.append(f'   {d:2}')        # Iv
        elif j==10: fd.append(f'{d:2}')           # c
        elif j==11: fd.append(f'@{mm}{d:4}{mm}:') # k
        elif j==12: fd.append(f'{d:7.3f}')      if i!=0 and i!=len(PythMap3)-1 else fd.append(f'{w7}{mm}{W}') # d
        elif j==13: fd.append(f'={mm}{d:5.3f}') if i!=0 and i!=len(PythMap3)-1 else fd.append(w5) # e
        elif j==14: fd.append(f'*{mm}{d:2}')      # c`
    return fd
########################################################################################################################################################################################################
def dmpPythIvals(i, ks, cs, ds, csv):
    mm, nn, ff = (Y, Y, 3) if csv else (W, Z, 1)      ;   m = -1
    w4, w5, w6, w7 = W*4, W*5, W*6, W*7
    eps, j     = pythEpsln(), math.floor(i/2)
    hdrA, hdrB = ['j', 'j*100', 'i'], ['Iv', f' c{mm} ', f'  k {mm} ', f'   d   {mm} ', f' e   {mm} ', f' c`  ']
    hdrs       = hdrA   ;   hdrs.extend(hdrB)  ;   hdrs.extend(hdrB)
    if   i == 0:
        slog(f'{fmtl(hdrs, s=mm, d=Z)}', p=0, f=ff)
        data     = [j, j*100, i, PythMap3[ks[i]], cs[i], ks[i], ds[i], eps, 0, 'd2', 0, 24, w6, w6, cs[i]]
        fd       = fIvals(data, i, csv)      ;    slog(f'{fmtl(fd, s=mm, d=Z)}', p=0, f=ff)
    elif not i % 2:
        u, v = (PythMap3[ks[i+m]], PythMap3[ks[i]])
        if  j < 6 and j % 2 or j >= 6 and not j % 2:
            data = [j, j*100, i, u, cs[i+m], ks[i+m], ds[i+m], eps, cs[i], v, cs[i], ks[i], ds[i], eps, cs[i+m]]
            fd   = fIvals(data, i, csv)    ;    slog(f'{fmtl(fd, s=mm, d=Z)}', p=0, f=ff)
        else:
            data = [j, j*100, i, v, cs[i], ks[i], ds[i], eps, cs[i+m], u, cs[i+m], ks[i+m], ds[i+m], eps, cs[i]]
            fd   = fIvals(data, i, csv)    ;    slog(f'{fmtl(fd, s=mm, d=Z)}', p=0, f=ff)
    elif i == len(PythMap3)-1:
        data     = [j+1, (j+1)*100, i+1, PythMap3[ks[i]], cs[i], ks[i], ds[i], eps, 0, 'A7', 0, 1178, w6, w6, cs[i]]
        fd       = fIvals(data, i, csv)      ;    slog(f'{fmtl(fd, s=mm, d=Z)}', p=0, f=ff)
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
def dmpPythMap2(w=9, csv=0): # w=6 or w=9
    global PythMap2
    mm, nn, ff      = (Y, Y, 3) if csv else (W, Z, 1)   ;   x = 4 if w==6 else 5
    ww, w1, w2, w3  = f'^{w}', f'^{w}.1f', f'^{w}.2f', f'^{w}.{x}f'   ;   dbg = 0
    blnk, sc, v     = w*W, 0, Z
    ns, ws          = [], []   ;   cs, ds = [], []  ;   r0s, rAs, rBs, r1s, r2s, r3s = [], [], [], [], [], []  ;  cksf, cksi = [], []  ;  vs = []
    for i, ck in enumerate(CENTKEYS):
        ival = PythMap3[ck] 
        ws.append(ival)
        if PythMap2 and ck in PythMap2 and PythMap2[ck]['Count'] > 0:
            a, ca, b, cb = PythMap2[ck]['ABCs']
            r0s.append(fmtR0(a, ca, b, cb, w3))
            rAs.append(fmtRA(a, ca, ww))
            rBs.append(fmtRB(b, cb, ww))
            v = fdvdr(a, ca, b, cb)
#           r1s.append(fmtR1(a, ca, b, cb, ww)) if ck in PythMap2 and PythMap2[ck]['Count'] > 0 else r1s.append(blnk) 
            r2s.append(fmtR2(a, ca, b, cb)) if w >= 9 else None
            r3s.append(fmtR3(a, ca, b, cb))
            n = PythMap2[ck]['Note']
            c = PythMap2[ck]['Count']   ;   sc += c
            f = r2cents(a**ca/b**cb)
            d = k2dCent(f)
            cksf.append(f)    ;   cksi.append(int(round(f)))
        else:
            r0s.append(blnk)    ;    rAs.append(blnk)   ;    rBs.append(blnk)  ;    r2s.append(blnk)  ;  r3s.append(blnk)
            n, f = blnk, blnk   ;    c, d = 0, 0.0      ;   cksi.append(ck)    ;   cksf.append(float(ck))  ;  v = Z
        ns.append(n)  ;  cs.append(c)  ;  ds.append(d)  ;     vs.append(v)
        dmpPythIvals(i, cksi, cs, ds, csv)
    ii = [ f'{i}' for i in range(2 * NT) ]
    slog(f'{mm}  k  {mm}{nn} {nn}{fmtl(ii, w=ww, s=mm, d=Z)}', p=0, f=ff)
    dmpDataTableLine(w + 1, csv=csv)
    slog(f'{mm}Centk{mm}{nn}[{nn}{fmtl(CENTKEYS, w=ww, s=mm, d=Z)}{nn}]', p=0, f=ff)
    slog(f'{mm}Intrv{mm}{nn}[{nn}{fmtl(ws,       w=ww, s=mm, d=Z)}{nn}]', p=0, f=ff)
    slog(f'{mm}Note {mm}{nn}[{nn}{fmtl(ns,       w=ww, s=mm, d=Z)}{nn}]', p=0, f=ff)
    slog(f'{mm}Cents{mm}{nn}[{nn}{fmtl(cksf,     w=w1, s=mm, d=Z)}{nn}]', p=0, f=ff)
    slog(f'{mm}dCent{mm}{nn}[{nn}{fmtl(ds,       w=w2, s=mm, d=Z)}{nn}]', p=0, f=ff)
    slog(f'{mm}Rati0{mm}{nn}[{nn}{fmtl(r0s,      w=ww, s=mm, d=Z)}{nn}]', p=0, f=ff)
    slog(f'{mm}RatiA{mm}{nn}[{nn}{fmtl(rAs,      w=ww, s=mm, d=Z)}{nn}]', p=0, f=ff)
    slog(f'{mm}     {mm}{nn}[{nn}{fmtl(vs,       w=ww, s=mm, d=Z)}{nn}]', p=0, f=ff)
    slog(f'{mm}RatiB{mm}{nn}[{nn}{fmtl(rBs,      w=ww, s=mm, d=Z)}{nn}]', p=0, f=ff)
#   slog(f'{mm}Rati1{mm}{nn}[{nn}{fmtl(r1s,      w=ww, s=mm, d=Z)}{nn}]', p=0, f=ff)
    slog(f'{mm}Rati2{mm}{nn}[{nn}{fmtl(r2s,      w=ww, s=mm, d=Z)}{nn}]', p=0, f=ff) if w >= 9 else None
    slog(f'{mm}Rati3{mm}{nn}[{nn}{fmtl(r3s,      w=ww, s=mm, d=Z)}{nn}]', p=0, f=ff)
    slog(f'{mm}Count{mm}{nn}[{nn}{fmtl(cs,       w=ww, s=mm, d=Z)}{nn}]', p=0, f=ff)
    dmpDataTableLine(w + 1, csv=csv)
    if dbg: slog(f'{len(PythMap1)=} {sc=}', p=0, f=ff)
    PythMap2 = { e: {'Count': 0} for e in CENTKEYS }
########################################################################################################################################################################################################
'''        
j,j*100,i,Iv, c, ,  k , ,   d   , , e   , , c`  ,Iv, c, ,  k , ,   d   , , e   , , c`  
0,   0, 0,P1,12,@,   0,:,  0.000,=,1.955,*, 0,   d2, 0,@,  24,:,       , ,     ,*,12
1, 100, 2,m2, 7,@,  90,:, -9.775,=,1.955,*, 5,   A1, 5,@, 114,:, 13.685,=,1.955,*, 7
2, 200, 4,M2,10,@, 204,:,  3.910,=,1.955,*, 2,   d3, 2,@, 180,:,-19.550,=,1.955,*,10
3, 300, 6,m3, 9,@, 294,:, -5.865,=,1.955,*, 3,   A2, 3,@, 318,:, 17.595,=,1.955,*, 9
4, 400, 8,M3, 8,@, 408,:,  7.820,=,1.955,*, 4,   d4, 4,@, 384,:,-15.640,=,1.955,*, 8
5, 500,10,P4,11,@, 498,:, -1.955,=,1.955,*, 1,   A3, 1,@, 522,:, 21.505,=,1.955,*,11
6, 600,12,d5, 6,@, 588,:,-11.730,=,1.955,*, 6,   A4, 6,@, 612,:, 11.730,=,1.955,*, 6
7, 700,14,P5,11,@, 702,:,  1.955,=,1.955,*, 1,   d6, 1,@, 678,:,-21.505,=,1.955,*,11
8, 800,16,m6, 8,@, 792,:, -7.820,=,1.955,*, 4,   A5, 4,@, 816,:, 15.640,=,1.955,*, 8
9, 900,18,M6, 9,@, 906,:,  5.865,=,1.955,*, 3,   d7, 3,@, 882,:,-17.595,=,1.955,*, 9
a,1000,20,m7,10,@, 996,:, -3.910,=,1.955,*, 2,   A6, 2,@,1020,:, 19.550,=,1.955,*,10
b,1100,22,M7, 7,@,1110,:,  9.775,=,1.955,*, 5,   d8, 5,@,1086,:,-13.685,=,1.955,*, 7
c,1200,24,P8,12,@,1200,:,  0.000,=,1.955,*, 0,   A7, 0,@,1178,:,       , ,     ,*,12

j j*100 i Iv  c     k       d       e       c`   Iv  c     k       d       e       c`  
0    0  0 P1 12 @    0 :   0.000 = 1.955 *  0    d2  0 @   24 :                 * 12
1  100  2 m2  7 @   90 :  -9.775 = 1.955 *  5    A1  5 @  114 :  13.685 = 1.955 *  7
2  200  4 M2 10 @  204 :   3.910 = 1.955 *  2    d3  2 @  180 : -19.550 = 1.955 * 10
3  300  6 m3  9 @  294 :  -5.865 = 1.955 *  3    A2  3 @  318 :  17.595 = 1.955 *  9
4  400  8 M3  8 @  408 :   7.820 = 1.955 *  4    d4  4 @  384 : -15.640 = 1.955 *  8
5  500 10 P4 11 @  498 :  -1.955 = 1.955 *  1    A3  1 @  522 :  21.505 = 1.955 * 11
6  600 12 d5  6 @  588 : -11.730 = 1.955 *  6    A4  6 @  612 :  11.730 = 1.955 *  6
7  700 14 P5 11 @  702 :   1.955 = 1.955 *  1    d6  1 @  678 : -21.505 = 1.955 * 11
8  800 16 m6  8 @  792 :  -7.820 = 1.955 *  4    A5  4 @  816 :  15.640 = 1.955 *  8
9  900 18 M6  9 @  906 :   5.865 = 1.955 *  3    d7  3 @  882 : -17.595 = 1.955 *  9
a 1000 20 m7 10 @  996 :  -3.910 = 1.955 *  2    A6  2 @ 1020 :  19.550 = 1.955 * 10
b 1100 22 M7  7 @ 1110 :   9.775 = 1.955 *  5    d8  5 @ 1086 : -13.685 = 1.955 *  7
c 1200 24 P8 12 @ 1200 :   0.000 = 1.955 *  0    A7  0 @ 1178 :                 * 12

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
