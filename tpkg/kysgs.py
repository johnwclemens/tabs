from tpkg       import utl
from tpkg.notes import Notes
from tpkg.misc  import Scales
from tpkg       import unic

name, NTONES       = Notes.name, Notes.NTONES
TYPE, TYPES        = Notes.TYPE, Notes.TYPES
FLAT, NTRL, SHRP   = Notes.FLAT, Notes.NTRL, Notes.SHRP
I2S, I2F, F4S, S4F = Notes.I2S,  Notes.I2F,  Notes.F4S,  Notes.S4F
nextIndex          = Notes.nextIndex
slog, fmtl         = utl.slog, utl.fmtl
ist, signed        = utl.ist,  utl.signed
W, X, Y, Z         = utl.W,    utl.X,    utl.Y,   utl.Z
F, N, S            = unic.F, unic.N, unic.S

KSD     = {}
KIM, KIS, KMS, KJS, KNS        = range(5)
KSK, KST, KSN, KSI, KSMS, KSSI = range(6)
M, P    = -7, 7
FD, PFX = 2, 0

def init(f):
    global FD   ;   FD = f
    slog('BGN',   f=FD)
    dmpKSVHdr(csv=0,   t=FLAT)
    dmpKSVHdr(csv=1,   t=FLAT)
    initKSD(KSD, t=FLAT)
    initKSD(KSD, t=SHRP)
    dmpKSVHdr(csv=0,   t=SHRP)
    dmpKSVHdr(csv=1,   t=SHRP)
    dumpData( csv=0)
    dumpData( csv=1)
    slog('END',   f=FD)

def initKSD(ksd, t):
    assert t==FLAT or t==SHRP and ist(t, int),  f'{t=} {type(t)=}'
    if     t==FLAT:  i = 0  ;  j = 6   ;  s = M
    else:            i = 0  ;  j = 10  ;  s = P
    iz1 = [ (j + k*s) % NTONES for k in range(1, 1+abs(s)) ]
    ms1 = [ name(j, t)         for j in iz1 ]
    iz2 = list(iz1)          ;       ms2  =  list(ms1)
    slog(f'{t=} {i=} {j=} {s=} {fmtl(iz2)=} {fmtl(ms2)=}', p=PFX, f=FD)   ;   j += t
    for  k in range(0, t + s, t):
        ak =    abs(k)
        m  =   name(i, t, n2=0 if ak > 5 else 1)
        n  =   name(j, t, n2=0 if ak > 5 else 1)
        if ak >= 1:   ms2[ak-1] = n  ;  iz2[ak-1] = j   ;  ms = list(ms2)  ;  iz = list(iz2)
        else:                                              ms = list(ms2)  ;  iz = list(iz2)
        jz = Scales.majIs(i)    ;   im = [i, m] #  ;   ns = []
        ns = [ name(j, t, n2=0 if ak > 5 else 1) for j in jz ]
        ksd[k]  =  [ im, iz, ms, jz, ns ]
        slog(fmtKSK(k, csv=0), p=PFX, f=FD)
        slog(fmtKSK(k, csv=1), p=0,   f=3)
        i  =   nextIndex(i, s)
        j  =   nextIndex(j, s)
    global KSD   ;   KSD = ksd
########################################################################################################################################################################################################
def dumpData(csv=0):
    slog(f'BGN {csv=}', f=FD)
    dumpKSH(csv)
    dumpKSV(csv)
    slog(f'END {csv=}', f=FD)
########################################################################################################################################################################################################
def dumpKSV(csv=0):
    f = 3 if csv else FD
    slog(f'BGN {csv=}', f=FD)
    dmpKSVHdr(csv)
    keys = sorted(KSD.keys())
    for k in keys:    slog(fmtKSK(k, csv), p=0 if csv else PFX, f=f)
    dmpKSVHdr(csv)
    slog(f'END {csv=}', f=FD)

def dmpKSVHdr(csv=0, t=0):
    y, fd = (Y, 3)  if csv else (W, FD)  # ;   n, m = W, W*2
    k = 2*P+1 if t == 0 else M if t == FLAT else P if t == SHRP else 1
    kso, fsi, ini, ino, kst = 'Key Sigature Ordered', 'F/S/N Indices', 'Ionian Note I', 'Ionian Note Ordering', f'Key Sig Table {signed(k)}'
    hdrs = ['KS', 'Type', 'N ', f'I', f' {kso} ', f' {fsi} ', f' {ini} ', f' {ino} ', f'{kst}']
    hdrs = y.join(hdrs)    ;    slog(hdrs, p=PFX, f=fd)
########################################################################################################################################################################################################
def fmtKSK(k, csv=0):
    y = Y if csv else W   ;   w, d = 2, '['     ;    ak = abs(k)
    t   = FLAT if k < 0 else SHRP if k > 0 else NTRL    ;   ntype = TYPES[t]
    s   = signed(k)       ;  im = KSD[k][KIM]   ;    i = im[0]    ;    m = im[1]
    iz  = KSD[k][KIS]     ;  jz = KSD[k][KJS]   ;   ms = KSD[k][KMS]
    ns  = [ name(j, t, 0 if ak > 5 else 1) for j in jz ] #    0 4 5 b
    iz  = [ f'{i:x}' for i in iz ]
    jz  = [ f'{j:x}' for j in jz ]
    _ = [s, ntype, f'{m:{w}}', f'{i:x}', fmtl(ms, w=w, d=d, s=y), fmtl(iz, d=d, s=y), fmtl(jz, d=d, s=y), fmtl(ns, w=w, d=d, s=y)]
    return y.join(_)
########################################################################################################################################################################################################
def dumpKSH(csv=0):
    y = Z if csv else W*2   ;   d, m, n = (Z, Y, Y) if csv else ('[', W, W*2)
    v, fd   = (f'{W}{Y}', 3)    if csv else (W*2, FD)   ;   p = 0 if csv else PFX
    f, k, s = [c for c in 'Flats  '], [c for c in 'N'], [c for c in '  Shrps']
    f = v.join(f)   ;   k = v.join(k)   ;   s = v.join(s)
    hdrs = [ f'{f} ', f'{k} ', f'{s}' ]       ;  hdrs = m.join(hdrs)   ;  _ =  Z if csv else W  ;  slog(f'{_}{hdrs}', p=p, f=fd)
    keys = sorted(KSD.keys())  ;  w = f'<2' ;   x = f'{w}x'
    _  = utl.ns2signs(keys)
    z = v.join(_)   ;   _ = Z if csv else W   ;   slog(f'{_}{z}', p=p, f=fd)
    slog(f'{fmtl(list(map(abs, keys)), w=w, d=d, s=m)}', p=p, f=fd)
    _  = [ KSD[k][KIM][KSK]    for k in keys ]  ;   slog(f'{fmtl(_, w=x, d=d, s=m)}', p=p, f=fd)
    _  = [ KSD[k][KIM][KST]    for k in keys ]  ;   slog(f'{fmtl(_, w=w, d=d, s=m)}', p=p, f=fd)
    f  = [ KSD[M][KMS][f]      for f in range(len(KSD[M][KMS])-1, -1, -1) ]  ;  s = [ KSD[P][KMS][s]    for s in range(len(KSD[P][KMS])) ]
    fs = []  ;  fs.extend(f)   ;  fs.append(y)  ;   fs.extend(s)   ;   slog(f'{fmtl(fs, w=w, d=d, s=m)}', p=p, f=fd)
    f  = [ f'{f:x}' for f in reversed(KSD[M][KIS]) ]   ;   s = [ f'{s:x}' for s in KSD[P][KIS] ]
    fs = []  ;  fs.extend(f)   ;  fs.append(y)  ;   fs.extend(s)   ;   slog(f'{fmtl(fs, w=w, d=d, s=m)}', p=p, f=fd)

def nic2KS(nic, dbg=0):
    if dbg: dumpKSV()   ;   dumpKSH()   ;   dumpNic(nic)
    iz  = []            ;   t  = TYPE   ;   nt = TYPES[t]
    ks  = KSD[M][KIS]    if t == FLAT else KSD[P][KIS]
    for i in ks:
        if i in nic:     iz.append(f'{i:x}')
        else:            break
    k   = -len(iz)       if t == FLAT else len(iz)
    n   = KSD[k][KIM][KST] if iz else '??'
    i   = KSD[k][KIM][KSK]
    ns  = KSD[k][KMS]
    if dbg: slog(fmtKSK(k), p=PFX, f=FD)
    if dbg: slog(fmtKSK(k), p=PFX, f=FD)
    return k, nt, n, i, ns, Scales.majIs(i)

def dumpNic(nic): #fix me
    s = f'{Y}{W}'
    slog(f'{fmtl([ f"{i:x}:{I2F[i]:2}:{nic[i]}" for i in nic.keys() ], s=s)}', p=PFX, f=FD)
    slog(f'{fmtl([ f"{i:x}:{I2S[i]:2}:{nic[i]}" for i in nic.keys() ], s=s)}', p=PFX, f=FD)
    slog(f'{fmtl([ f"{i:x}:{I2F[i]:2}:{nic[i]}" if  i in nic and nic[i] > 0 else " None " for i in KSD[M][KIS] ], s=s)}', p=PFX, f=FD)
    slog(f'{fmtl([ f"{i:x}:{I2F[i]:2}:{nic[i]}" if  i in nic and nic[i] > 0 else " None " for i in KSD[P][KIS] ], s=s)}', p=PFX, f=FD)
########################################################################################################################################################################################################
