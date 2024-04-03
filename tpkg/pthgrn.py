from tpkg       import utl
#from tpkg       import notes
from tpkg.notes import Notes
from tpkg       import intrvls as ivls
import math

W, Y, Z       = utl.W,      utl.Y,     utl.Z
slog, ist     = utl.slog,   utl.ist
fmtf, fmtg    = utl.fmtf,   utl.fmtg
fmtl, fmtm    = utl.fmtl,   utl.fmtm

CM_P_M        = ivls.CM_P_M
V_SOUND       = ivls.V_SOUND
A4_INDEX      = ivls.A4_INDEX
NT            = ivls.NT

F440s, F432s  = ivls.F440s, ivls.F432s
abc2r         = ivls.abc2r
i2spr         = ivls.i2spr
ir            = ivls.ir
fabc          = ivls.fabc
i2nPair       = ivls.i2nPair
r2cents       = ivls.r2cents
k2dCent       = ivls.k2dCent
stackI        = ivls.stackI
stck5ths      = ivls.stck5ths
stck4ths      = ivls.stck4ths
addFmtRs      = ivls.addFmtRs
fmtR0         = ivls.fmtR0
fmtR1         = ivls.fmtR1
fmtR2         = ivls.fmtR2
fmtR3         = ivls.fmtR3
fmtRA         = ivls.fmtRA
fmtRB         = ivls.fmtRB
fdvdr         = ivls.fdvdr
########################################################################################################################################################################################################
#COFSA       = {'C', 'G', 'D',  'A',  'E',  'B',  'F#', 'C#', 'G#', 'D#', 'A#', 'E#', 'B#'}
#COFSB       = {'C', 'F', 'Bb', 'Eb', 'Ab', 'Db', 'Gb', 'Cb', 'Fb', 'Bbb'}
COFMA        = {'C':('F♯', 'G♭'), 'G':('C♯', 'D♭'),  'D':('G♯', 'A♭'), 'A':('D♯', 'E♭'), 'E':('A♯', 'B♭'), 'B':('E♯', 'F'), 'F♯':('B♯', 'C'), 'C♯':('G', 'G'),  'G♯':('D', 'D'),    'D♯':('A', 'A'),    'A♯':('E', 'F♭'),   'E♯':('B', 'C♭'),   'B♯':('F♯', 'G♭')}
COFMB        = {'C':('F♯', 'G♭'), 'F':('B',  'C♭'), 'B♭':('E', 'F♭'), 'E♭':('A', 'A'),  'Ab':('D', 'D'),  'D♭':('G', 'G'),  'G♭':('B♯', 'C'), 'C♭':('E♯', 'F'), 'F♭':('A♯', 'B♭'), 'Bbb':('D♯', 'E♭'), 'Ebb':('G♯', 'A♭'), 'A♭♭':('C♯', 'D♭'), 'D♭♭':('F♯', 'B♭')}
COFM         = COFMA | COFMB
#              0     1     2     3     4     5     6     7     8     9     10    11    12    13    14    15    16    17    18    19    20    21    22    23
#              D     Eb                E     F                 F#    G           Ab    G#          A     Bb                B     C                 C#    D
IVAL_KS     = ['P1', 'm2', 'A1', 'd3', 'M2', 'm3', 'A2', 'd4', 'M3', 'P4', 'A3', 'd5', 'A4', 'd6', 'P5', 'm6', 'A5', 'd7', 'M6', 'm7', 'A6', 'd8', 'M7', 'P8']
CENT_KS     = [   0,  90,  114,  180,  204,  294,  318,  384,  408,  498,  522,  588,  612,  678,  702,  792,  816,  882,  906,  996,  1020, 1086, 1110, 1200]
nimap       = {} # note index to list of abcs (freq ratios) and ckmap (cent key data map)
ckmap       = { ck: {'Count': 0} for ck in CENT_KS } # freq ratio in cents to ival counts and data
ck2ik       = { CENT_KS[i]: k for i, k in enumerate(IVAL_KS) }
#KEYS       = ['Abc', 'Cents', 'Count', 'DCent', 'Freq', 'Idx', 'Ival', 'Note', 'Wavln'] # N/A
K0          = 50
########################################################################################################################################################################################################
def dumpData(csv=0):
    slog(f'BGN {csv=}')
    if csv:  global nimap   ;   nimap = {}
#    dmpPyth(k=54, rf=440, sss=V_SOUND, csv=csv) # Gb/F#
#    dmpPyth(k=61, rf=440, sss=V_SOUND, csv=csv) # Db/C#
#    dmpPyth(k=56, rf=440, sss=V_SOUND, csv=csv) # Ab/G#
#    dmpPyth(k=51, rf=440, sss=V_SOUND, csv=csv) # Eb
#    dmpPyth(k=58, rf=440, sss=V_SOUND, csv=csv) # Bb 
#    dmpPyth(k=53, rf=440, sss=V_SOUND, csv=csv) # F
#    dmpPyth(k=60, rf=440, sss=V_SOUND, csv=csv) # C
#    dmpPyth(k=55, rf=440, sss=V_SOUND, csv=csv) # G
#    dmpPyth(k=50, rf=440, sss=V_SOUND, csv=csv) # D
#    dmpPyth(k=57, rf=440, sss=V_SOUND, csv=csv) # A
#    dmpPyth(k=52, rf=440, sss=V_SOUND, csv=csv) # E
#    dmpPyth(k=59, rf=440, sss=V_SOUND, csv=csv) # B
#    dmpPyth(k=54, rf=440, sss=V_SOUND, csv=csv) # F#/Gb
#    dmpPyth(k=61, rf=440, sss=V_SOUND, csv=csv) # C#/Db
#    dmpPyth(k=56, rf=440, sss=V_SOUND, csv=csv) # G#/Ab
#    dmpPyth(k=50, rf=440, sss=V_SOUND, csv=csv) # D
#    dmpPyth(k=55, rf=440, sss=V_SOUND, csv=csv) # G
#    dmpPyth(k=60, rf=440, sss=V_SOUND, csv=csv) # C
#    dmpPyth(k=53, rf=440, sss=V_SOUND, csv=csv) # F
#    dmpPyth(k=58, rf=440, sss=V_SOUND, csv=csv) # Bb 
#    dmpPyth(k=51, rf=440, sss=V_SOUND, csv=csv) # Eb
##   dmpPyth(k=62, rf=440, sss=V_SOUND, csv=csv) # D octave
#    if not csv:  testStacks()
#    dmpPyth(k=50, rf=440, ss=V_SOUND, csv=csv) # D
#    dmpPyth(k=62, rf=440, ss=V_SOUND, csv=csv) # D octave
    dmpData('D', csv)
    slog(f'END {csv=}')
########################################################################################################################################################################################################
def dmpData(n='C', csv=0):
    k0 = Notes.N2I[n] + 48
    for i in range(7, 12):
        k = k0 + (i * 7) % NT
        dmpPyth(k, k0=k0, rf=440, sss=V_SOUND, csv=csv)
    for i in range(0, 7):
        k = k0 + (i * 7) % NT
        dmpPyth(k, k0=k0, rf=440, sss=V_SOUND, csv=csv)
########################################################################################################################################################################################################
def epsilon(dbg=0):
    ccents = comma()
    ecents = ccents / NT
    if dbg:  slog(f'Epsilon = Comma / 12 = {ccents:10.5f} / 12 = {ecents:10.5f} cents')
    return ecents
    
def comma(dbg=0): # 3**12 / 2**19 = 3¹²/2¹⁹ = 531441 / 524288 = 1.0136432647705078, log2(1.0136432647705078) = 0.019550008653874178, 1200 * log2() = 23.460010384649014
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
def abcs(a=7, b=6):
    abc1 = stck5ths(a)
    abc2 = stck4ths(b)
    abc3 = [ stackI(3, 2, 0) ]   ;   abc3.extend(abc1)   ;   abc3.extend(abc2)   ;   abc3.append(stackI(2, 1, 1))
    abc4 = sorted(abc3, key= lambda z: abc2r(z[0], z[1], z[2])[0])
    return [ abc1, abc2, abc3, abc4 ] 
########################################################################################################################################################################################################
def dmpPyth(k, k0=50, rf=440, sss=V_SOUND, csv=0):
    x, y = 13, 6     ;   z = x-2   ;   _ = x*W   ;   f0 = F440s[k] if rf==440 else F432s[k]   ;   w0 = CM_P_M * sss   ;   cki = -1
    ww, mm, nn, oo, ff = (f'^{x}', Y, Y, Y, 3) if csv else (f'^{x}', W, Z, '|', 1)            ;   w3 = [W, W, W]
    slog(f'BGN Pythagorean ({k=} {rf=} {sss=} {csv=})', f=ff)
    ii  = [ f'{i}' for i in range(2 * NT) ]         ;   slog(f'{mm}  k  {mm}{nn} {nn}{fmtl(ii, w=ww, s=mm, d=Z)}', p=0, f=ff)
    dmpDataTableLine(x + 1, csv=csv)
    ii, ns, vs, fs, ws = [], [], [], [], []   ;   cs, ds = [], []   ;   r0s, r1s, r2s, r3s = [], [], [], []   ;   abcMap = []
    tmp = k2Abcs(k)  ;   abc0 = list(tmp[3])        ;   abc1, abc2, abc3, abc4 = fabc(tmp[0]), fabc(tmp[1]), fabc(tmp[2]), fabc(tmp[3])
    abc1.insert(0, fmtl(w3, w=2, d=Z))              ;   abc2.insert(0, fmtl(w3, w=2, d=Z)) # insert blanks for alignment in log/csv files
    for i, e in enumerate(abc0):
        a, b, c = e[0], e[1], e[2]    ;    r, ca, cb = abc2r(a, b, c)    ;   abc = [ a, ca, b, cb ]   ;    f = r * f0    ;   w = w0 / f
        r0 = fmtR0(a, ca, b, cb, f'{ww}.{z-2}f')    ;   r1 = fmtR1(a, ca, b, cb, y)   ;    r2 = fmtR2(a, ca, b, cb, y)   ;   r3 = fmtR3(a, ca, b, cb, y)
        n  = fmtNPair(k, i, k0)   ;   c = r2cents(r)    ;   d = k2dCent(c)   ;    rc = round(c)   ;   assert rc in ck2ik,  f'{rc=} not in ck2ik {k=} {i=} {k0=} {n=} {c=} {r=} {abc=}'   ;   v = ck2ik[rc]    ;   cki += 1
        while CENT_KS[cki] < rc:
            ii.append(_)  ;  cs.append(_)  ;  ds.append(_)  ;  fs.append(_)  ;  ws.append(_)  ;  ns.append(_)  ;  vs.append(_)  ;  r0s.append(_)  ;  r1s.append(_)  ;  r2s.append(_)  ;  r3s.append(_)
            cki += 1  ;  j = len(ii)-1   ;  abc1.insert(j, fmtl(w3, w=2, d=Z))  ;  abc2.insert(j, fmtl(w3, w=2, d=Z))  ;  abc3.insert(j, fmtl(w3, w=2, d=Z))  ;  abc4.insert(j, fmtl(w3, w=2, d=Z))
        ii.append(i)  ;  fs.append(fmtf(f, z))   ;  r1s.append(r1)   ;   r0s.append(r0)  ;   cs.append(fmtf(c, y-1))   ;   abcMap.append(abc)
        ns.append(n)  ;  ws.append(fmtf(w, z))   ;  r2s.append(r2)   ;   r3s.append(r3)  ;   ds.append(fmtg(d, y-1))   ;       vs.append(v)
    nimap[k] = [abcMap, ckmap]   ;   sfx = f'{nn}]'   ;   sfxc = f'{nn}]{mm}cents'   ;   sfxf = f'{nn}]{mm}Hz'   ;   sfxw = f'{nn}]{mm}cm'
    while len(abc1) < len(abc3): abc1.append(fmtl(w3, w=2, d=Z)) # append blanks for alignment in log/csv files
    while len(abc2) < len(abc3): abc2.append(fmtl(w3, w=2, d=Z)) # append blanks for alignment in log/csv files
    slog(f'{mm}Index{mm}{nn}[{nn}{fmtl(ii,   w=ww, s=oo, d=Z)}{sfx}',  p=0, f=ff)
    slog(f'{mm}Note {mm}{nn}[{nn}{fmtl(ns,   w=ww, s=oo, d=Z)}{sfx}',  p=0, f=ff)
    slog(f'{mm}Itval{mm}{nn}[{nn}{fmtl(vs,   w=ww, s=oo, d=Z)}{sfx}',  p=0, f=ff)
    slog(f'{mm}Ratio{mm}{nn}[{nn}{fmtl(r0s,  w=ww, s=oo, d=Z)}{sfx}',  p=0, f=ff)
    slog(f'{mm}Rati1{mm}{nn}[{nn}{fmtl(r1s,  w=ww, s=oo, d=Z)}{sfx}',  p=0, f=ff)
    slog(f'{mm}Rati2{mm}{nn}[{nn}{fmtl(r2s,  w=ww, s=oo, d=Z)}{sfx}',  p=0, f=ff)
    slog(f'{mm}Rati3{mm}{nn}[{nn}{fmtl(r3s,  w=ww, s=oo, d=Z)}{sfx}',  p=0, f=ff)
    slog(f'{mm}Cents{mm}{nn}[{nn}{fmtl(cs,   w=ww, s=oo, d=Z)}{sfxc}', p=0, f=ff)
    slog(f'{mm}DCent{mm}{nn}[{nn}{fmtl(ds,   w=ww, s=oo, d=Z)}{sfxc}', p=0, f=ff)
    slog(f'{mm}Freq {mm}{nn}[{nn}{fmtl(fs,   w=ww, s=oo, d=Z)}{sfxf}', p=0, f=ff)
    slog(f'{mm}Wavln{mm}{nn}[{nn}{fmtl(ws,   w=ww, s=oo, d=Z)}{sfxw}', p=0, f=ff)
    slog(f'{mm} ABC1{mm}{nn}[{nn}{fmtl(abc1, w=ww, s=oo, d=Z)}{sfx}',  p=0, f=ff)
    slog(f'{mm} ABC2{mm}{nn}[{nn}{fmtl(abc2, w=ww, s=oo, d=Z)}{sfx}',  p=0, f=ff)
    slog(f'{mm} ABC3{mm}{nn}[{nn}{fmtl(abc3, w=ww, s=oo, d=Z)}{sfx}',  p=0, f=ff)
    slog(f'{mm} ABC4{mm}{nn}[{nn}{fmtl(abc4, w=ww, s=oo, d=Z)}{sfx}',  p=0, f=ff)
    dmpDataTableLine(x + 1, csv=csv)
    dmpMaps(k, k0, csv)
    slog(f'END Pythagorean ({k=} {rf=} {sss=} {csv=})', f=ff)
########################################################################################################################################################################################################
def k2Abcs(k=50):
    f = abcs
    return f(6, 5) if k==50 or k== 62 else f(5, 6) if k==57 else f(4, 7) if k==52 else f(3, 8) if k==59 else f(2, 9)  if k==54 else f(1, 10) if k==61 else f(0, 11) if k==56 \
                                      else f(7, 4) if k==55 else f(8, 3) if k==60 else f(9, 2) if k==53 else f(10, 1) if k==58 else f(11, 0) if k==51 else f(12, 0)
#   return f(7, 6) if k==50 or k== 62 else f(6, 7) if k==57 else f(5, 8) if k==52 else f(4, 9)  if k==59 else f(3, 10) if k==54 else f(2, 11) if k==61 else f(1, 12) if k==56 \
#                                     else f(8, 5) if k==55 else f(9, 4) if k==60 else f(10, 3) if k==53 else f(11, 2) if k==58 else f(12, 1) if k==51 else f(13, 0)
########################################################################################################################################################################################################
def fmtNPair(k, i, k0, dbg=0):
    n0, _   = i2nPair(k0, s=1)
    n1, n2  = i2nPair(k + i, b=0 if i in (4, 6, 11) or k in (K0 + 4, K0 + 6, K0 + 11) else 1, s=1, e=1)   ;   slog(f'{K0=} {n0=} {n1=} {n2=}') if dbg else None
    if i and i != NT:
#        if   n1 == 'A♭':          slog(f'{n1=} == A♭, {n0=} {_=} return {n2=}') if dbg else None   ;   return n2
#        elif n2 and n2 != 'A♭':   slog(f'{n2=} != A♭, {n0=} {_=} {n1=}')        if dbg else None   ;   n1 += '/' + n2
        if          n1 == COFM[n0][1]:   return n2
        elif n2 and n2 != COFM[n0][1]:   n1 += '/' + n2
#        if   (k + i) % NT == (K0 + 6) % NT and len(n)  == 2 and n[1]  == '♭': return n2
#        elif (k + i) % NT != (K0 + 6) % NT and len(n2) == 2 and n2[1] == '♭': n += '/' + n2
#        if n2: n += '/' + n2
    slog(f'return {n1=}') if dbg else None
    return n1
########################################################################################################################################################################################################
def dmpMaps(k, k0, csv):
    dmpNiMap(  1, k, x=13, upd=1, k0=k0, csv=csv)
    dmpNiMap(  2, k, x=13, upd=1, k0=k0, csv=csv)
    dmpNiMap(  3, k, x=13, upd=1, k0=k0, csv=csv)
    dmpNiMap(  4, k, x=13, upd=1, k0=k0, csv=csv)
    dmpNiMap(  5, k, x=13, upd=1, k0=k0, csv=csv)
    dmpCks2Iks(      x=13,               csv=csv)
    dmpCkMap(k,                          csv=csv)
    dmpNiMap(  1, k, x=9,  upd=0, k0=k0, csv=csv)
    dmpNiMap(  2, k, x=9,  upd=0, k0=k0, csv=csv)
    dmpNiMap(  3, k, x=9,  upd=0, k0=k0, csv=csv)
    dmpNiMap(  4, k, x=9,  upd=0, k0=k0, csv=csv)
    dmpNiMap(  5, k, x=9,  upd=0, k0=k0, csv=csv)
    dmpCks2Iks(      x=9,                csv=csv)
    checkIvals(                          csv=csv)
########################################################################################################################################################################################################
def dmpCks2Iks(x=13, csv=0):
    if not csv:
        if   x== 9: slog(f'{7*W}  {fmtm(ck2ik, w=4, wv=2, s=3*W, d=Z)}', p=0)
        elif x==13: slog(f'{9*W}  {fmtm(ck2ik, w=4, wv=2, s=7*W, d=Z)}', p=0)
########################################################################################################################################################################################################
def dmpNiMap(ni, ik, x, upd=0, k0=50, rf=440, sss=V_SOUND, csv=0): # x=13 or x=9
    ww, mm, nn, oo, ff = (f'^{x}', Y, Y, Y, 3) if csv else (f'^{x}', W, Z, '|', 1)   ;   pfx = ''   ;   sfx = f'{nn}]'  ;  yy = 6 if x==13 else 4
    f0  = F440s[ik] if rf==440 else F432s[ik]     ;     w0 = CM_P_M * sss   
    ii = [ f'{i}' for i in range(2 * NT) ]
    slog(f'{mm}  k  {mm}{nn} {nn}{fmtl(ii, w=ww, s=mm, d=Z)}', p=0, f=ff) if ni == 1 else None
    dmpDataTableLine(x + 1, csv=csv) if ni == 1 else None
    for i, (k, v) in enumerate(nimap.items()):
        rat0, rat2, rat3, cents = [], [], [], []  ;   cki = -1
        rat1 = [] if x == 13 else None  ;  ratA = [] if x == 9 else None   ;  ratB = [] if x == 9 else None
        for j, e in enumerate(v[0]):
            a, ca, b, cb = e        ;      pa, pb = a ** ca, b ** cb
            n    = fmtNPair(k, j, k0)
            pd   = [f'{i:x}', f'{k:2}', f'{n:2}']   ;   pfx = mm.join(pd)   ;   pfx += f'{nn}[{nn}'
            cent = r2cents(pa/pb)   ;    rc = ir(cent)      ;   cki += 1
            while CENT_KS[cki] < rc:
                blnk = W*x          ;   cki += 1            ;   cents.append(f'{blnk:{ww}}')
                rat0.append(blnk)   ;   rat2.append(blnk)   ;   rat3.append(blnk)
                rat1.append(blnk) if x == 13 else None      ;   ratA.append(blnk) if x == 9 else None   ;   ratB.append(blnk) if x == 9 else None
            r0   = fmtR0(a, ca, b, cb, f'{ww}.5f')          ;   centf = f'{cent:{ww}.0f}'
            r2 = fmtR2(a, ca, b, cb, yy)    ;    r3   = fmtR3(a, ca, b, cb, yy)
            r1 = fmtR1(a, ca, b, cb, yy) if x == 13 else None    ;   rA = fmtRA(a, ca, ww) if x == 9 else None   ;   rB = fmtRB(b, cb, ww) if x == 9 else None
            if upd and ni == 5:
                assert rc in ckmap.keys(),  f'{rc=} {ckmap.keys()=}'     ;     f = f0 * pa/pb
                ckmap[rc]['Count'] = ckmap[rc]['Count'] + 1 if 'Count' in ckmap[rc] else 1    ;    ckmap[rc]['Abc']   = e
                ckmap[rc]['Freq']  = f                      ;   ckmap[rc]['Wavln'] = w0 / f
                ckmap[rc]['Cents'] = cent                   ;   ckmap[rc]['DCent'] = k2dCent(cent)
                ckmap[rc]['Note']  = n if k==ik else W*2
                ckmap[rc]['Ival']  = ck2ik[rc]              ;   ckmap[rc]['Idx']   = j
            rat0.append(r0)   ;   rat2.append(r2)   ;   rat3.append(r3)   ;   cents.append(centf)
            rat1.append(r1) if x == 13 else None    ;   ratA.append(rA) if x == 9 else None   ;   ratB.append(rB) if x == 9 else None
        if   ni == 1:             slog(f'{pfx}{Z.join(fmtl(rat0,  w=ww, s=oo, d=Z))}{sfx}', p=0, f=ff)
        elif ni == 2 and x == 13: slog(f'{pfx}{Z.join(fmtl(rat1,  w=ww, s=oo, d=Z))}{sfx}', p=0, f=ff)
        elif ni == 2 and x == 9:  slog(f'{pfx}{Z.join(fmtl(ratA,  w=ww, s=oo, d=Z))}{sfx}', p=0, f=ff)  ;  slog(f'{pfx}{Z.join(fmtl(ratB,  w=ww, s=oo, d=Z))}{sfx}', p=0, f=ff)
        elif ni == 3:             slog(f'{pfx}{Z.join(fmtl(rat2,  w=ww, s=oo, d=Z))}{sfx}', p=0, f=ff)
        elif ni == 4:             slog(f'{pfx}{Z.join(fmtl(rat3,  w=ww, s=oo, d=Z))}{sfx}', p=0, f=ff)
        elif ni == 5:             slog(f'{pfx}{Z.join(fmtl(cents, w=ww, s=oo, d=Z))}{sfx}', p=0, f=ff)
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
        elif j==12: fd.append(f'{d:7.3f}') if utl.ist(d, float) else fd.append(W*7) if i!=0 and i!=len(ck2ik)-1 else fd.append(W*7) # d
        elif j==14: fd.append(f'*{mm}{d:2}')             # c`
        elif j in (5, 11): fd.append(f'@{mm}{d:4}{mm}:') # k k
        elif j in (7, 13): fd.append(f'={mm}{d:5.3f}')   # e e
        elif j in (2, 3, 4, 9, 10): fd.append(f'{d:2}')  # i Iv c Iv c
    return fd
########################################################################################################################################################################################################
def dmpIvals(i, ks, cs, ds, csv): # only called by dmpCkMap()
    mm, nn, oo, ff = (Y, Y, Y, 3) if csv else (W, Z, '|', 1)   ;   m = -1
#    slog(f'BGN dmpIvals() {i=} {csv=}')
    eps, j     = epsilon(), math.floor(i/2)
    hdrA, hdrB1, hdrB2 = ['j', 'j*100', 'i'], ['Iv', f' c{mm} ', f'  k {mm} ', f'   d   {mm} ', f' e   {mm} ', f' c`  '], ['Iv', f' c{mm} ', f'  k {mm} ', f'   d   {mm} ', f' e   {mm} ', f' c`']
    hdrs       = hdrA   ;   hdrs.extend(hdrB1)   ;   hdrs.extend(hdrB2)
    if   i == 0:
        slog(f'{fmtl(hdrs, s=mm, d=Z)}', p=0, f=ff)
        data     = [j, j*100, i, ck2ik[ks[i]], cs[i], ks[i], ds[i], eps, 0, 'd2', 0, 24, W*6, eps, cs[i]]
        fd       = fIvals(data, i, csv)    ;    slog(f'{fmtl(fd, s=mm, d=Z)}', p=0, f=ff)
    elif not i % 2:
        u, v = (ck2ik[ks[i+m]], ck2ik[ks[i]])
        if  j < 6 and j % 2 or j > 6 and not j % 2:
            data = [j, j*100, i, u, cs[i+m], ks[i+m], ds[i+m], eps, cs[i], v, cs[i], ks[i], ds[i], eps, cs[i+m]]
            fd   = fIvals(data, i, csv)    ;    slog(f'{fmtl(fd, s=mm, d=Z)}', p=0, f=ff)
        else:
            data = [j, j*100, i, v, cs[i], ks[i], ds[i], eps, cs[i+m], u, cs[i+m], ks[i+m], ds[i+m], eps, cs[i]]
            fd   = fIvals(data, i, csv)    ;    slog(f'{fmtl(fd, s=mm, d=Z)}', p=0, f=ff)
    elif i == len(ck2ik)-1:
        data     = [j+1, (j+1)*100, i+1, ck2ik[ks[i]], cs[i], ks[i], ds[i], eps, 0, 'A7', 0, 1178, W*6, eps, cs[i]]
        fd       = fIvals(data, i, csv)    ;    slog(f'{fmtl(fd, s=mm, d=Z)}', p=0, f=ff)
#    slog(f'END dmpIvals() {i=} {csv=}')
########################################################################################################################################################################################################
#def fmtR0(a, ca, b, cb, w):   pa, pb =   float(a ** ca) ,   float(b ** cb)   ;  return f'{pa/pb:{w}}'
#def fmtR1(a, ca, b, cb, w):   pa, pb =   a ** ca        ,   b ** cb          ;  return f'{pa:>{w}}/{pb:<{w}}'
#def fmtRA(a, ca, w=Z):        pa     =   a ** ca                             ;  return f'{pa:{w}}'
#def fmtRB(b, cb, w=Z):        pb     =   b ** cb                             ;  return f'{pb:{w}}'
#def fmtR2(a, ca, b, cb, w):   qa, qb = f'{a}^{ca}'      , f'{b}^{cb}'        ;  return f'{qa:>{w}}/{qb:<{w}}'
#def fmtR3(a, ca, b, cb, w):   sa, sb = f'{a}{i2spr(ca)}', f'{b}{i2spr(cb)}'  ;  return f'{sa:>{w}}/{sb:<{w}}' 
#def fdvdr(a, ca, b, cb):      n = max(len(fmtRA(a, ca)), len(fmtRB(b, cb)))  ;  return n * '/'
    
#def addFmtRs(r0s, rAs, rBs, r2s, r3s, a, ca, b, cb, w3, ww, u):
#    r0s.append(fmtR0(a, ca, b, cb, w3))
#    rAs.append(fmtRA(a, ca, ww if ist(a**ca, int) else w3))
#    rBs.append(fmtRB(b, cb, ww if ist(b**cb, int) else w3))
#    r2s.append(fmtR2(a, ca, b, cb, u)) # if u >= 9 else None
#    r3s.append(fmtR3(a, ca, b, cb, u))
########################################################################################################################################################################################################
def dmpDataTableLine(w=10, n=24, csv=0):
    c = '-'   ;   nn, mm, t = (Y, Y, Y) if csv else (Z, W, '|')
    col = f'{c * (w-1)}'
    cols = t.join([ col for _ in range(n) ])
    slog(f'{mm}     {mm}{nn} {nn}{cols}', p=0, f=3 if csv else 1)
########################################################################################################################################################################################################
def dmpCkMap(k=50, rf=440, sss=V_SOUND, csv=0):
    x, y, u = 5, 4, 9   ;   blnk, sk, v = u*W, 0, Z   ;   f0 = F440s[k] if rf==440 else F432s[k]   ;   w0 = CM_P_M * sss   ;  dbg = 1   ;   global ckmap
    mm, nn, oo, ff  = (Y, Y, Y, 3) if csv else (W, Z, '|', 1)             ;   ww, w1, w2, w3  = f'^{u}', f'^{u}.1f', f'^{u}.2f', f'^{u}.{x}f'
    ns, fs, ws, vs  = [], [], [], []  ;  cs, ds, qs, ks = [], [], [], []  ;   r0s, rAs, rBs, r2s, r3s = [], [], [], [], []  ;  cksf, cksi = [], []
    for i, ck in enumerate(CENT_KS):
        ival = ck2ik[ck]    ;    vs.append(ival)   ;   assert ckmap and ck in ckmap,  f'{ck=} {ckmap=}'
        if ckmap[ck]['Count'] > 0:
            assert ival == ckmap[ck]['Ival'],  f'{ival=} {ck=} {ckmap[ck]["Ival"]=}'
            a, ca, b, cb = ckmap[ck]['Abc']   ;    q = fdvdr(a, ca, b, cb)
            addFmtRs(r0s, rAs, rBs, r2s, r3s, a, ca, b, cb, w3, ww, y)
            f, w, n, c, d, k, i2 = getCkMap(ck, a, ca, b, cb, f0, w0)   ;   sk += k
            cksf.append(f'{c:{w1}}')          ;    cksi.append(int(round(c)))
            fs.append(f'{fmtf(f, u-2)}')      ;      ws.append(f'{fmtf(w, u-2)}')
        else:
            r0s.append(blnk)    ;    rAs.append(blnk)     ;  rBs.append(blnk)  ;   r2s.append(blnk)  ;  r3s.append(blnk)   ;   k, q = 0, Z
            n, c, d, f, w = blnk, blnk, blnk, blnk, blnk  ;  cksi.append(ck)   ;  cksf.append(blnk)  ;  fs.append(f)       ;   ws.append(w)
        ns.append(n)  ;  ks.append(k)  ;  cs.append(c)    ;  ds.append(d)      ;   qs.append(q)
        dmpIvals(i, cksi, ks, ds, csv)
    ii = [ f'{i}' for i in range(2 * NT) ]
    if dbg: slog(f'{len(nimap)=} {sk=}', p=0, f=ff)
    slog(f'{mm}  k  {mm}{nn} {nn}{fmtl(ii,      w=ww, s=mm, d=Z)}',      p=0, f=ff)
    dmpDataTableLine(u + 1, csv=csv)
    slog(f'{mm}Centk{mm}{nn}[{nn}{fmtl(CENT_KS, w=ww, s=oo, d=Z)}{nn}]', p=0, f=ff)
    slog(f'{mm}Itval{mm}{nn}[{nn}{fmtl(vs,      w=ww, s=oo, d=Z)}{nn}]', p=0, f=ff)
    slog(f'{mm}Note {mm}{nn}[{nn}{fmtl(ns,      w=ww, s=oo, d=Z)}{nn}]', p=0, f=ff)
    slog(f'{mm}Cents{mm}{nn}[{nn}{fmtl(cksf,    w=ww, s=oo, d=Z)}{nn}]', p=0, f=ff)
    slog(f'{mm}DCent{mm}{nn}[{nn}{fmtl(ds,      w=ww, s=oo, d=Z)}{nn}]', p=0, f=ff)
    slog(f'{mm}Rati0{mm}{nn}[{nn}{fmtl(r0s,     w=ww, s=oo, d=Z)}{nn}]', p=0, f=ff)
    slog(f'{mm}RatiA{mm}{nn}[{nn}{fmtl(rAs,     w=ww, s=oo, d=Z)}{nn}]', p=0, f=ff)
    slog(f'{mm} A/B {mm}{nn}[{nn}{fmtl(qs,      w=ww, s=oo, d=Z)}{nn}]', p=0, f=ff)
    slog(f'{mm}RatiB{mm}{nn}[{nn}{fmtl(rBs,     w=ww, s=oo, d=Z)}{nn}]', p=0, f=ff)
    slog(f'{mm}Rati2{mm}{nn}[{nn}{fmtl(r2s,     w=ww, s=oo, d=Z)}{nn}]', p=0, f=ff) if u >= 9 else None
    slog(f'{mm}Rati3{mm}{nn}[{nn}{fmtl(r3s,     w=ww, s=oo, d=Z)}{nn}]', p=0, f=ff)
    slog(f'{mm}Freq {mm}{nn}[{nn}{fmtl(fs,      w=ww, s=oo, d=Z)}{nn}]', p=0, f=ff)
    slog(f'{mm}Wavln{mm}{nn}[{nn}{fmtl(ws,      w=ww, s=oo, d=Z)}{nn}]', p=0, f=ff)
    slog(f'{mm}Count{mm}{nn}[{nn}{fmtl(ks,      w=ww, s=oo, d=Z)}{nn}]', p=0, f=ff)
    dmpDataTableLine(u + 1, csv=csv)
########################################################################################################################################################################################################    
def getCkMap(ck, a, ca, b, cb, f0, w0): # sometimes
    f = ckmap[ck]['Freq']    ;   assert f == f0 * a**ca / b**cb,    f'{ck=} {f=} {f0=} r={a**ca/b**cb} {f0*a**ca/b**cb=} {a=} {ca=} {b=} {cb=}'
    w = ckmap[ck]['Wavln']   ;   assert w == w0 / f,                f'{w=} {w0=} {f=}'
    n = ckmap[ck]['Note']
    i = ckmap[ck]['Idx']
    k = ckmap[ck]['Count']
    c = ckmap[ck]['Cents']   ;   assert c == r2cents(a**ca/b**cb),  f'{c=} {r2cents(a**ca/b**cb)=}'
    d = ckmap[ck]['DCent']   ;   assert d == k2dCent(c),            f'{d=} {k2dCent(c)=}'    ;    d = round(d, 2)
    return f, w, n, c, d, k, i
########################################################################################################################################################################################################
def checkIvals(csv=0):
    global ckmap
    mm, nn, oo, ff  = (Y, Y, Y, 3) if csv else (W, Z, '|', 1)
    slog(f'BGN checkIvals() {csv=}', p=0, f=ff)
    keys, msgs, ws = [], [], [7, 8, 7, 7, 7, 5, 4, 4, 3]
    for kk, vv in ckmap.items():
        keys = list(vv.keys())
    slog(f'Jdx{mm} {nn}{nn}CK{mm}  {mm}{fmtl(keys, w=ws, s=mm, d=Z)}', p=0, f=ff)
    for i, (k, v) in enumerate(ckmap.items()):
        msg = f'{i:2}{nn}[{mm}{k:4}{nn}:{mm}[{mm}'
        for j, (k2, v2) in enumerate(v.items()):
            msg += f'{fmtf(v2, 7)}{mm}' if k2 in ("Cents", "Freq", "Wavln") else f'{fmtg(v2, 6)}{mm}' if k2=="DCent" else f'{fmtl(v2, s=W):11}{mm}' if k2=="Abc" else f'{v2:2}{mm}' if k2 in ("Count", "Idx") else f'{v2:5}{mm}' if k2=="Note" else f'{v2:3}{mm}' if k2=="Ival" else f'{v2:6}{mm}'
        msg += f']{nn}]'   ;   msgs.append(msg)
    msgs = '\n'.join(msgs)
    slog(f'{msgs}', p=0, f=ff)
    slog(f'END checkIvals() {csv=}', p=0, f=ff)
    ckmap = { e: {'Count': 0} for e in CENT_KS }
