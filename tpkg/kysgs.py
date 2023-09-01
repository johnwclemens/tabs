from tpkg       import utl    as utl
from tpkg.notes import Notes  as Notes
from tpkg.misc  import Scales as Scales
from tpkg       import unic   as unic

name, NTONES     = Notes.name, Notes.NTONES
FLAT, NTRL, SHRP = Notes.FLAT, Notes.NTRL, Notes.SHRP
F4S, S4F         = Notes.F4S,  Notes.S4F
nextIndex        = Notes.nextIndex
slog, fmtl       = utl.slog, utl.fmtl
ist, signed      = utl.ist,  utl.signed
W, X, Y, Z       = utl.W,    utl.X,    utl.Y,   utl.Z
F, N, S          = unic.F, unic.N, unic.S

KSD     = {}
KIM, KIS, KMS, KJS, KNS        = range(5)
KSK, KST, KSN, KSI, KSMS, KSSI = range(6)
M, P    = -7, 7
FD, PFX = -2, 1

def init(f):
    global KSD, FD   ;   FD = f
    slog('BGN', f=FD)
    dmpKSVHdr(csv=0, t=-1)
    dmpKSVHdr(csv=1, t=-1)
    KSD = initKSD(KSD, t=-1)
    KSD = initKSD(KSD, t= 1)
    dmpKSVHdr(t= 1)
#    dumpKSH(  csv)
    dumpData(csv=0)
    dumpData(csv=1)
    slog('END', f=FD)

def initKSD(ks, t):
#    slog('BGN', f=FD)
    assert t==FLAT or t==SHRP and ist(t, int),  f'{t=} {type(t)=}'
    if     t==FLAT:  i = 0  ;  j = 6   ;  s = M
    else:            i = 0  ;  j = 10  ;  s = P
    iz1 = [ (j + k*s) % NTONES for k in range(1, 1+abs(s)) ]
    ms1 = [ name(j, t)         for j in iz1 ]
    iz2 = list(iz1)          ;       ms2  =  list(ms1)
    slog(f'{t=} {i=} {j=} {s=} {fmtl(iz2)=} {fmtl(ms2)=}', p=PFX, f=FD)   ;   j += t
    for  k in range(0, t + s, t):
        ak = abs(k)
        m  =   name(i, t, 1 if ak > 5 or ak==0 else 0)
        n  =   name(j, t, 1 if ak > 5 or ak==0 else 0)
        if ak >= 1:   ms2[ak-1] = n  ;  iz2[ak-1] = j   ;  ms = list(ms2)  ;  iz = list(iz2)
        else:                                              ms = list(ms2)  ;  iz = list(iz2)
        jz = Scales.majIs(i)    ;    im  = [i, m]   ;   ns = []
        for j in jz: #        ns = [ name(j, t, 1 if ak >= 5 else 0) for j in jz ]
            a = name(j, t=t, n2=0 if ak > 5 else 1)
            if   ak > 5:
                if   a=='C' : a = f'B{S}'
                elif a=='F' : a = f'E{S}'
            #     if   a in F4S.keys():
            #         a = F4S[a]
            #     elif a in S4F.keys(): # ==f'B{S}':
            #         a = S4F[a]
            ns.append(a)
        ks[k]  =  [ im, iz, ms, jz, ns ]
        slog(fmtKSK(k, csv=0), p=PFX, f=FD)
        slog(fmtKSK(k, csv=1), p=0,   f=3)
        i  =   nextIndex(i, s)
        j  =   nextIndex(j, s)
#    slog('END', f=FD)
    return ks
########################################################################################################################################################################################################
def dumpData(csv=0):
    slog(f'BGN', f=FD)
    dumpKSH(csv)
    dumpKSV(csv)
    slog(f'END', f=FD)
########################################################################################################################################################################################################
def dumpKSV(csv=0):
    f = 3 if csv else FD
    dmpKSVHdr(csv)
    keys = sorted(KSD.keys())
    for k in keys:    slog(fmtKSK(k, csv), p=0 if csv else PFX, f=f)

def dmpKSVHdr(csv=0, t=0):
    c, d, m, n, o, f = (Z, Z, Y, Z, Z, 3)  if csv else ('^20', '^13', W, W, W*2, FD)
    k = 2*P+1 if t == 0 else M if t == Notes.FLAT else P if t == Notes.SHRP else 1
#    fsn, fsi, ii, ino, kst = 'Flats/Shrps Naturals', 'F/S/N Indices', 'Ionian Indices', 'Ionian Note Ordering', f'Key Sig Table {signed(k)}'
    fsn, fsi, ii, ino, kst = 'Key Sigature Ordered', 'F/S/N Indices', 'Ionian Indexing', 'Ionian Note Ordering', f'Key Sig Table {signed(k)}'
    hdrs = ['KS', 'Type', 'N ', f'{n}I', f'{n}{fsn:{c}}', f'{o}{fsi:{d}}', f'{o}{ii:{d}}', f'{n}{ino:{c}}', f'{n}{kst}']
    hdrs = m.join(hdrs)    ;    slog(hdrs, p=PFX, f=FD)
########################################################################################################################################################################################################
def fmtKSK(k, csv=0):
#   w, d, n = (2, '[', Y) if csv else (2, '[', W)  ;  ak = abs(k)
    n = Y if csv else W   ;   w, d = 2, '['     ;    ak = abs(k)
    t   = FLAT if k < 0 else SHRP if k > 0 else NTRL    ;   ntype = Notes.TYPES[t]
    s   = signed(k)       ;  im = KSD[k][KIM]   ;    i = im[0]    ;    m = im[1]
    iz  = KSD[k][KIS]     ;  jz = KSD[k][KJS]   ;   ms = KSD[k][KMS]
#   ns  = [ name(j, t, 1) for j in jz ] #    0 4 5 b
    ns  = [ name(j, t, 1 if ak > 5 or ak == 0 else 0) for j in jz ] #    0 4 5 b
    iz  = [ f'{i:x}' for i in iz ]
    jz  = [ f'{j:x}' for j in jz ]
    _ = [s, ntype, f'{m:{w}}', f'{i:x}', fmtl(ms, w=w, d=d, s=n), fmtl(iz, d=d, s=n), fmtl(jz, d=d, s=n), fmtl(ns, w=w, d=d, s=n)]
#    _ = [s, ntype, f'{m:{w}}', f'{i:x}', f'{W}', fmtl(ms, w=w, d=d, s=n), f'{W}', fmtl(iz, d=d, s=n), f'{W}', fmtl(jz, d=d, s=n), f'{W}', fmtl(ns, w=w, d=d, s=n)]
    return n.join(_)

def dumpKSH(csv=0):
#   c, y, fd   = (Z, Z, 3)    if csv else ('^20', W, FD)     ;  u, v = '<', 0   ;   f, k, s = 'Flats', 'N', 'Shrps'  ;  p = 0 if csv else PFX
#   c, y, fd   = (Z, Z, 3)    if csv else ('^20', W, FD)     ;  u, v = '<', 0   ;   f, k, s = '    Flats    ', 'N', '    Shrps    '  ;  p = 0 if csv else PFX
    c, y, fd   = (Z, Z, 3)    if csv else ('^20', W, FD)     ;  u, v = '<', 0   ;   f, k, s = ',F,l,a,t,s,,', 'N', ',S,h,r,p,s,,'  ;  p = 0 if csv else PFX
    w, d, m, n = (0, Z, Y, Y) if csv else (2, '[', W, W*2)   ;     v = W*v if v and Notes.TYPE==Notes.FLAT else Z
    hdrs = [ f'{y}{f:{c}}', f'{k:{w}}', f'{s:{c}}' ]         ;  hdrs = m.join(hdrs)   ;   slog(hdrs, p=p, f=fd)
#   keys = sorted(KSD.keys())  ;  w, x = f'{u}{w}', f'{w}x'  ;     p = 0 if csv else PFX
    keys = sorted(KSD.keys())  ;  w = f'{u}{w}' ;   x = f'{w}x'    ;   p = 0 if csv else PFX
    _  = utl.ns2signs(keys)    ;  _ = n.join(_) ;   slog(f'{v}{y}{_}', p=p, f=fd)    ;   slog(f'{v}{fmtl(list(map(abs, keys)), w=w, d=d, s=m)}', p=p, f=fd)
    _  = [ KSD[k][KIM][KSK]    for k in keys ]  ;   slog(f'{v}{fmtl(_, w=x, d=d, s=m)}', p=p, f=fd)
    _  = [ KSD[k][KIM][KST]    for k in keys ]  ;   slog(f'{v}{fmtl(_, w=w, d=d, s=m)}', p=p, f=fd)    ;   y = Z if csv else W*2
    f  = [ KSD[M][KMS][f]      for f in range(len(KSD[M][KMS])-1, -1, -1) ]  ;  s = [ KSD[P][KMS][s]    for s in range(len(KSD[P][KMS])) ]
    fs = []  ;  fs.extend(f)   ;  fs.append(y)  ;   fs.extend(s)   ;   slog(f'{v}{fmtl(fs, w=w, d=d, s=m)}', p=p, f=fd)
    f  = [ f'{f:x}' for f in reversed(KSD[M][KIS]) ]   ;   s = [ f'{s:x}' for s in KSD[P][KIS] ]
    fs = []  ;  fs.extend(f)   ;  fs.append(y)  ;   fs.extend(s)   ;   slog(f'{v}{fmtl(fs, w=w, d=d, s=m)}', p=p, f=fd)
########################################################################################################################################################################################################
def nic2KS(nic, dbg=0):
    if dbg: dumpKSV()   ;   dumpKSH()   ;   dumpNic(nic)
    iz  = []            ;   t  = Notes.TYPE   ;   nt = Notes.TYPES[t]
    ks  = KSD[M][KIS]    if t == Notes.FLAT else KSD[P][KIS]
    for i in ks:
        if i in nic:     iz.append(f'{i:x}')
        else:            break
    k   = -len(iz)       if t == Notes.FLAT else len(iz)
    n   = KSD[k][KIM][KST] if iz else '??'
    i   = KSD[k][KIM][KSK]
    ns  = KSD[k][KMS]
    if dbg: slog(fmtKSK(k), p=PFX, f=FD)
    if dbg: slog(fmtKSK(k), p=PFX, f=FD)
    return k, nt, n, i, ns, Scales.majIs(i)

def dumpNic(nic): #fix me
    slog(f'{fmtl([ f"{i:x}:{Notes.I2F[i]:2}:{nic[i]}" for i in nic.keys() ], s=Y)}', p=PFX, f=FD)
    slog(f'{fmtl([ f"{i:x}:{Notes.I2S[i]:2}:{nic[i]}" for i in nic.keys() ], s=Y)}', p=PFX, f=FD)
    slog(f'{fmtl([ f"{i:x}:{Notes.I2F[i]:2}:{nic[i]}" if  i in nic and nic[i] > 0 else None for i in KSD[M][KIS] ], s=Y)}', p=PFX, f=FD)
    slog(f'{fmtl([ f"{i:x}:{Notes.I2F[i]:2}:{nic[i]}" if  i in nic and nic[i] > 0 else None for i in KSD[P][KIS] ], s=Y)}', p=PFX, f=FD)
########################################################################################################################################################################################################
