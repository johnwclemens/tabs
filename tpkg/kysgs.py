from tpkg import utl as utl
#from tpkg import notes as notes
from tpkg.notes import Notes  as Notes
from tpkg.misc  import Scales as Scales

F            = 0
M, P         = utl.M, utl.P
slog         = utl.slog
W, Y, Z      = utl.W, utl.Y, utl.Z
fmtl         = utl.fmtl
signed       = utl.signed

KSD = {}
KIM, KIS, KMS, KJS, KNS        = range(5)
KSK, KST, KSN, KSI, KSMS, KSSI = range(6)

def init(f):
    global KSD, F   ;   F = f
    slog('BGN', f=F)
    dmpKSVHdr(csv=1,   t=-1)
    KSD = initKSD(KSD, t=-1)
    KSD = initKSD(KSD, t= 1)
    dmpKSVHdr(csv=1,   t= 1)
    dumpKSH(  csv=1)
    dumpData()
    slog('END', f=F)

def initKSD(ks, t):
    slog('BGN', f=F)
    nt = Notes.NTONES
    if     t == -1:   i = 0  ;  j = 6   ;  s = M
    else:             i = 0  ;  j = 10  ;  s = P
    iz1 = [ (j + k * s) % nt for k in range(1, 1+abs(s)) ]
    ms1 = [ Notes.name(j, t) for j in iz1 ]
    iz2 = list(iz1)          ;         ms2 = list(ms1)
    slog(f'{t=} {i=} {j=} {s=} {fmtl(iz2)=} {fmtl(ms2)=}', p=0, f=F)   ;   j += t
    for  k in range(0, t + s, t):
        ak = abs(k)
        m  =   Notes.name(i, t, 1 if ak >= 5 else 0)
        n  =   Notes.name(j, t, 1 if ak >= 5 else 0)
        if ak >= 1:   ms2[ak-1] = n  ;  iz2[ak-1] = j   ;  ms = list(ms2)  ;  iz = list(iz2)
        else:                                              ms = list(ms2)  ;  iz = list(iz2)
        jz = Scales.majIs(i)    ;    im  = [i, m]
        ns = [ Notes.name(j, t, 1 if ak >= 5 else 0) for j in jz ]
        ks[k]  =  [ im, iz, ms, jz, ns ]
        slog(fmtKSK(k, csv=1), p=0, f=F)
        i  =   Notes.nextIndex(i, s)
        j  =   Notes.nextIndex(j, s)
    slog('END', f=F)
    return ks
########################################################################################################################################################################################################
def dumpData(csv=0):
    slog(f'BGN', f=F)
    dumpKSH(csv)
    dumpKSV(csv)
    slog(f'END', f=F)
########################################################################################################################################################################################################
def dumpKSV(csv=0):
    f = 3 if csv else F
    dmpKSVHdr(csv)
    keys = sorted(KSD.keys())
    for k in keys:    slog(fmtKSK(k, csv), p=0, f=f)

def dmpKSVHdr(csv=0, t=0):
    c, d, m, n, o, f = (Z, Z, Y, Z, Z, 3)  if csv else ('^20', '^13', W, W, W*2, F)
    k = 2*P+1 if t == 0 else M if t == Notes.FLAT else P if t == Notes.SHRP else 1
    fsn, fsi, ii, ino, kst = 'Flats/Shrps Naturals', 'F/S/N Indices', 'Ionian Indices', 'Ionian Note Ordering', f'Key Sig Table {signed(k)}'
    hdrs = ['KS', 'Type', 'N', f'{n}I', f'{n}{fsn:{c}}', f'{o}{fsi:{d}}', f'{o}{ii:{d}}', f'{n}{ino:{c}}', f'{n}{kst}']
    hdrs = m.join(hdrs)    ;    slog(hdrs, p=0, f=F)
########################################################################################################################################################################################################
def fmtKSK(k, csv=0):
    w, d, n = (0, Z, Y) if csv else (2, '[', W)
#   KSD, KIM, KIS, KJS, KMS = self.KSD, self.KIM, self.KIS, self.KJS, self.KMS
    t   = -1 if k < 0 else 1 if k > 0 else 0    ;   nt = Notes.TYPES[t]
    s   = signed(k)     ;   im = KSD[k][KIM]    ;    i = im[0]      ;    m = im[1]
    iz  = KSD[k][KIS]   ;   jz = KSD[k][KJS]    ;   ms = KSD[k][KMS]
#       ns  = [ Notes.name(j, t, 0)                       for j in jz ] # 2 7 9 1 3 6 8 a
    ns  = [ Notes.name(j, t, 1 if abs(k) >= 5 else 0) for j in jz ] #    0 4 5 b
    iz  = [ f'{i:x}' for i in iz ]
    jz  = [ f'{j:x}' for j in jz ]
    _ = [s, nt, f'{m:{w}}', f'{i:x}', fmtl(ms, w=w, d=d, s=n), fmtl(iz, d=d, s=n), fmtl(jz, d=d, s=n), fmtl(ns, w=w, d=d, s=n)]
    return n.join(_)

def dumpKSH(csv=0):
    c, y, ff   = (Z, Z, 3)    if csv else ('^20', W, F)     ;  u, v, p = '<', 0, 0   ;   f, k, s = 'Flats', 'N', 'Shrps'
    w, d, m, n = (0, Z, Y, Y) if csv else (2, '[', W, W*2)  ;  v = W*v if v and Notes.TYPE==Notes.FLAT else Z
#    KSD, KIM, KIS, KMS, KSK, KST = self.KSD, self.KIM, self.KIS, self.KMS, self.KSK, self.KST
    hdrs = [ f'{y}{f:{c}}', f'{k:{w}}', f'{s:{c}}' ]        ;  hdrs = m.join(hdrs)   ;   slog(hdrs, p=p, f=ff)
    keys = sorted(KSD.keys())  ;  w = f'{u}{w}' ;   x = f'{w}x'
    _  = utl.ns2signs(keys)    ;  _ = n.join(_) ;   slog(f'{v}{y}{_}', p=p, f=ff)    ;   slog(f'{v}{fmtl(list(map(abs, keys)), w=w, d=d, s=m)}', p=p, f=ff)
    _  = [ KSD[k][KIM][KSK]    for k in keys ]  ;   slog(f'{v}{fmtl(_, w=x, d=d, s=m)}', p=p, f=ff)
    _  = [ KSD[k][KIM][KST]    for k in keys ]  ;   slog(f'{v}{fmtl(_, w=w, d=d, s=m)}', p=p, f=ff)   ;  y = Z if csv else W*2
    f  = [ KSD[M][KMS][f]      for f in range(len(KSD[M][KMS])-1, -1, -1) ]  ;  s = [ KSD[P][KMS][s]    for s in range(len(KSD[P][KMS])) ]
    fs = []  ;  fs.extend(f)   ;  fs.append(y)  ;   fs.extend(s)   ;   slog(f'{v}{fmtl(fs, w=w, d=d, s=m)}', p=p, f=ff)
    f  = [ f'{f:x}' for f in reversed(KSD[M][KIS]) ]   ;   s = [ f'{s:x}' for s in KSD[P][KIS] ]
    fs = []  ;  fs.extend(f)   ;  fs.append(y)  ;   fs.extend(s)   ;   slog(f'{v}{fmtl(fs, w=w, d=d, s=m)}', p=p, f=ff)
########################################################################################################################################################################################################
def nic2KS(nic, dbg=0):
#    KSD, KIM, KIS, KMS, KSK, KST = self.KSD, self.KIM, self.KIS, self.KMS, self.KSK, self.KST
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
    if dbg: slog(fmtKSK(k), f=F)
    if dbg: slog(fmtKSK(k), f=F)
    return k, nt, n, i, ns, Scales.majIs(i)

def dumpNic(nic): #fix me
#    KSD, KIS = self.KSD, self.KIS
    slog(f'{fmtl([ f"{i:x}:{Notes.I2F[i]:2}:{nic[i]}" for i in nic.keys() ], s=Y)}', f=F)
    slog(f'{fmtl([ f"{i:x}:{Notes.I2S[i]:2}:{nic[i]}" for i in nic.keys() ], s=Y)}', f=F)
    slog(f'{fmtl([ f"{i:x}:{Notes.I2F[i]:2}:{nic[i]}" if  i in nic and nic[i] > 0 else None for i in KSD[M][KIS] ], s=Y)}', f=F)
    slog(f'{fmtl([ f"{i:x}:{Notes.I2F[i]:2}:{nic[i]}" if  i in nic and nic[i] > 0 else None for i in KSD[P][KIS] ], s=Y)}', f=F)
########################################################################################################################################################################################################
# KSD = {}
# KIM, KIS, KMS, KJS, KNS        = range(5)
# KSK, KST, KSN, KSI, KSMS, KSSI = range(6)
# dmpKSVHdr(csv=1,   t=-1)
# KSD = initKSD(KSD, t=-1)
# KSD = initKSD(KSD, t= 1)
# dmpKSVHdr(csv=1,   t= 1)
# dumpKSH(  csv=1)
