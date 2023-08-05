
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
    c, d, m, n, o, f = (Z, Z, Y, Z, Z, 3) if csv else ('^20', '^13', W, W, W*2, 1)
    k = 2*P+1 if t == 0 else M if t == Notes.FLAT else P if t == Notes.SHRP else 1
    fsn, fsi, ii, ino, kst = 'Flats/Shrps Naturals', 'F/S/N Indices', 'Ionian Indices', 'Ionian Note Ordering', f'Key Sig Table {signed(k)}'
    hdrs = ['KS', 'Type', 'N', f'{n}I', f'{n}{fsn:{c}}', f'{o}{fsi:{d}}', f'{o}{ii:{d}}', f'{n}{ino:{c}}', f'{n}{kst}']
    hdrs = m.join(hdrs)   ;   slog(hdrs, p=0, f=f)

def fmtKSK(k, csv=0):
    w, d, n = (0, Z, Y) if csv else (2, '[', W)
    t   = -1 if k < 0 else 1 if k > 0 else 0    ;   nt = Notes.TYPES[t]
    s   = signed(k)     ;   im = KSD[k][KIM]    ;    i = im[0]      ;    m = im[1]
    iz  = KSD[k][KIS]   ;   jz = KSD[k][KJS]    ;   ms = KSD[k][KMS]
    ns  = [ Notes.name(j, t, 1 if abs(k) >= 5 else 0) for j in jz ]
    iz  = [ f'{i:x}' for i in iz ]
    jz  = [ f'{j:x}' for j in jz ]
    _ = [s, nt, f'{m:{w}}', f'{i:x}', fmtl(ms, w=w, d=d, s=n), fmtl(iz, d=d, s=n), fmtl(jz, d=d, s=n), fmtl(ns, w=w, d=d, s=n)]
    return n.join(_)

def dumpKSH(csv=0):
    c, y, ff   = (Z, Z, 3)    if csv else ('^20', W, 1)     ;  u, v, p = '<', 0, 0   ;   f, k, s = 'Flats', 'N', 'Shrps'
    w, d, m, n = (0, Z, Y, Y) if csv else (2, '[', W, W*2)  ;  v = W*v if v and Notes.TYPE==Notes.FLAT else Z
    hdrs = [ f'{y}{f:{c}}', f'{k:{w}}', f'{s:{c}}' ]        ;  hdrs = m.join(hdrs)   ;   slog(hdrs, p=p, f=ff)
    keys = sorted(KSD.keys())  ;  w = f'{u}{w}' ;   x = f'{w}x'
    _  = ns2signs(keys)  ;   _ = n.join(_)      ;   slog(f'{v}{y}{_}', p=p, f=ff)    ;  slog(f'{v}{fmtl(list(map(abs, keys)), w=w, d=d, s=m)}', p=p, f=ff)
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
    ms1 = [ Notes.name(j, t)           for j in iz1 ]
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

