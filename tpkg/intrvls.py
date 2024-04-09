from tpkg       import utl
from tpkg       import unic
from tpkg       import notes
from tpkg.notes import Notes
import math

F, N, S                = unic.F,   unic.N,   unic.S
W, Y, Z, slog, ist     = utl.W,    utl.Y,    utl.Z,    utl.slog,   utl.ist
fmtl, fmtm, fmtf, fmtg = utl.fmtl, utl.fmtm, utl.fmtf, utl.fmtg

SUPERS, MAX_FREQ_IDX, ACCD_TONES = utl.SPRSCRPT_INTS,    utl.MAX_FREQ_IDX,     notes.ACCD_TONES
NT, A4_INDEX, CM_P_M, V_SOUND    = notes.NTONES, notes.A4_INDEX, notes.CM_P_M, notes.V_SOUND

FLATS, SHRPS  = notes.FLATS, notes.SHRPS
F440s, F432s  = notes.F440s, notes.F432s

# COFS = {'C', 'G', 'D', 'A', 'E', 'B/Cb', 'F#/Gb', 'C#/Db', 'Ab', 'Eb', 'Bb', 'F'}
########################################################################################################################################################################################################
def i2spr(i): # todo fixme still being used by old code that hasn't been retired yet
    if i < 0: return '-' + Z.join( SUPERS[int(digit)] for digit in str(i) if str.isdigit(digit) )
    else:     return       Z.join( SUPERS[int(digit)] for digit in str(i) )
########################################################################################################################################################################################################
def dmpData(csv=0):
    slog(f'BGN {csv=}')
    dmpOTS(       rf=440, sss=V_SOUND, csv=csv)
    slog(f'END {csv=}')
########################################################################################################################################################################################################
def fOTS(i, r=440):  f0 = F440s[0] if r == 440 else F432s[0]  ;   return f0 * i
########################################################################################################################################################################################################
def dmpOTS(rf=440, sss=V_SOUND, csv=0):
    slog(f'BGN Overtone Series ({rf=} {sss=} {csv=})')
    ww, dd, mm, nn, ff = ('^6', '[', Y, Y, 3) if csv else ('^6', '[', W, Z, 1)
    rs    = F440s       if rf == 440 else F432s         ;   cs, ds, ns, fs, ws = [], [], [], [], []
    freqs = F440s[:100] if rf == 440 else F432s[:100]   ;   ref = f'440A ' if rf == 440 else f'432A '
    f0    = F440s[0]    ;   w0 = CM_P_M * sss/f0
    for i, freq in enumerate(freqs):
        i += 1          ;    f  = fOTS(i, rf)    ;    w  = w0 / i
        n, n2  = Intonation.f2nPair(f, b=0 if i in (17, 22, 25, 28) else 1) 
        j  = Notes.n2ai(n)
        assert 0 <= j < len(rs),  f'{j=} {len(rs)=}'
        fr, _ = Intonation.norm(f/f0)
        f2 = rs[j]               ;    c = Intonation.r2cents(fr)         ;     d = Intonation.r2cents(f/f2)
        fs.append(fmtf(f, 6))    ;    ns.append(n)            ;     ws.append(fmtf(w, 6))
        cs.append(fmtf(c, 6))    ;    ds.append(fmtg(d, 6 if d >= 0 else 5))
    fs   = mm.join(fs)           ;    ws = mm.join(ws)        ;     ns = fmtl(ns, w=ww, s=mm, d=Z)   ;     cs = fmtl(cs, w=ww, s=mm, d=Z)   ;     ds = fmtl(ds, w=ww, s=mm, d=Z)
    ref += f'{nn}[{nn}'          ;  sfxf = f'{mm}]{mm}Hz'     ;   sfxw = f'{mm}]{mm}cm'              ;   sfxc = f'{mm}]{mm}cents'           ;   sfxd = f'{mm}]{mm}dcents'
    pfxn = f'notes{nn}[{nn}'     ;  pfxc = f'cents{nn}[{nn}'  ;   pfxd = f'dcnts{nn}[{nn}'           ;    sfx = f'{mm}]{nn}'
    slog(f'Index{nn}[{nn}{fmtl(list(range(1, 101)), w=ww, d=Z, s=mm)}{sfx}', p=0, f=ff)
    slog(f'{ref}{fs}{sfxf}',  p=0, f=ff)
    slog(f'{pfxn}{ns}{sfx}',  p=0, f=ff)
    slog(f'{pfxc}{cs}{sfxc}', p=0, f=ff)
    slog(f'{pfxd}{ds}{sfxd}', p=0, f=ff)
    slog(f'{ref}{ws}{sfxw}',  p=0, f=ff)
    slog(f'END Overtone Series ({rf=} {sss=} {csv=})')

########################################################################################################################################################################################################
########################################################################################################################################################################################################

class Intonation(object):
    def __init__(self, n='C'):
        self.VS     = V_SOUND
        self.centKs = []
        self.ivalKs = []
        self.ck2ikm = {} # self.setCk2ikm()
        self.n      = n
        self.k      = Notes.N2I[n] + 48
#        self.r0s, self.r2s, self.r3s = [], [], []
#        self.r1s, self.rAs, self.rBs = [], [], []
    ####################################################################################################################################################################################################
    def setCk2ikm(self):   self.ck2ikm = { self.centKs[i]: k for i, k in enumerate(self.ivalKs) }   ;   return self.ck2ikm # todo this base class method initializes and or sets self.ck2ikm
    ####################################################################################################################################################################################################
    @staticmethod
    def i2spr(i):
        if i < 0: return '-' + Z.join( SUPERS[int(digit)] for digit in str(i) if str.isdigit(digit) )
        else:     return       Z.join( SUPERS[int(digit)] for digit in str(i) )

    @staticmethod
    def r2cents(r):      return math.log2(r) * NT * 100

    @staticmethod
    def k2dCent(k):
        return k if 0 <= k < 50 else k-100 if 50<=k<150 else k-200 if 150<=k<250 else k-300 if 250<=k<350 else k-400 if 350<=k<450 else k-500 if 450<=k<550 else k-600 if 550<=k<650 else k-700 if 650<=k<750 else k-800 if 750<=k<850 else k-900 if 850<=k<950 else k-1000 if 950<=k<1050 else k-1100 if 1050<=k<1150 else k-1200 if 1150 <= k <= 1200 else None
    ####################################################################################################################################################################################################
    @staticmethod
    def norm(n):
        i = 0
        if n > 1:
            while n > 2:
                n /= 2  ;  i -= 1
        elif n < 1:
            while n < 1:
                n *= 2  ;  i += 1
        return n, i
    ####################################################################################################################################################################################################
    @staticmethod
    def f2nPair(f, rf=440, b=None, s=0, e=0):
        ni = NT * math.log2(f / rf) # fixme
        i  = round(A4_INDEX + ni)
        return Intonation.i2nPair(i, b, s, e)
    
    @staticmethod
    def i2nPair(i, b=None, s=0, e=0):
        m = Z    ;    n = FLATS[i] if b == 1 else SHRPS[i]
        if s:         n = n[:-1].strip()
        if e == 1 and len(n) > 1:
            m = FLATS[i] if not b else SHRPS[i]   ;   m = m[:-1].strip() if s else m
        return n, m
    ####################################################################################################################################################################################################
    def addFmtRs(self, a, ca, b, cb, rs, u=4, w=9, k=None, i=None, j=None):
        assert rs and ist(rs, list),  f'{rs=} {type(rs)=} {a=} {ca} {b} {cb} {u=} {w=}'   ;   lr = len(rs)
        r0s, r2s, r3s = rs[0], rs[-2], rs[-1]          ;   r1s, rAs, rBs = None, None, None
        if   lr == 4:       r1s      = rs[1]           ;   r1s.append(self.fmtR1(a, ca, b, cb, u, k, i, j))
        elif lr == 5:       rAs, rBs = rs[1], rs[2]    ;   rAs.append(self.fmtRA(a, ca, w))    ;    rBs.append(self.fmtRB(b, cb, w)) # if ist(b**cb, int) else w3))
        r0s.append(self.fmtR0(a, ca, b, cb, w, k, i, j))
        r2s.append(self.fmtR2(a, ca, b, cb, u, k, i, j)) # if u >= 9 else None
        r3s.append(self.fmtR3(a, ca, b, cb, u, k, i, j))
        if   lr == 4:   return r0s, r1s,      r2s, r3s
        elif lr == 5:   return r0s, rAs, rBs, r2s, r3s
    ####################################################################################################################################################################################################
    @staticmethod
    def fmtR0(a, ca, b, cb, w, k, i=None, j=None):
        pa = a ** ca   ;   pb = b ** cb   ;   p = 2 ** k if k else 1   ;   dbg = 0
        pfx = f'{i:4} {j:4} ' if i is not None and j is not None else Z
        if k is None:     v = pa/pb       ;   k = utl.NONE
        else:             v = p*pa*pb
        ret = f'{v:^{w}.{w-4}f}' if ist(v, float) else f'{v:^{w}}'
        slog(f'{pfx}{k:4} {p:4} : {a:2} {ca:2} {b:2} {cb:2} {ret=}') if dbg else None  ;  return ret
    ####################################################################################################################################################################################################
    @staticmethod
    def fmtR1(a, ca, b, cb, w, k, i=None, j=None):
        pa = a ** abs(ca)  ;  pb = b ** abs(cb)  ;  p = 2 ** abs(k) if k else 1  ;  papbi = f'{p}/{pa*pb}'  ;  ret = Z  ;  dbg = 0
        pfx = f'{i:4} {j:4} ' if i is not None and j is not None else Z
        if   k is None:
            ret = f'{pa:>{w}}/{pb:<{w}}'   ;   k = utl.NONE
        elif k == 0:
            ret = f'{pa:>{w}}*{pb:<{w}}' if ca >= 0 < cb else f'{pa:>{w}}/{pb:<{w}}' if ca >= 0 >= cb else f'{pb:>{w}}/{pa:<{w}}' if ca < 0 <= cb else f'{papbi:^{2*w+1}}' if ca < 0 > cb else f'?#?#?'
        elif k > 0:
            pa = pa * p if ca >= 0 <= cb or ca >= 0 > cb else pa  ;  pb = pb * p if ca < 0 <= cb else pb
            ret = f'{pa:>{w}}*{pb:<{w}}' if ca >= 0 < cb else f'{pa:>{w}}/{pb:<{w}}' if ca >= 0 >= cb else f'{pb:>{w}}/{pa:<{w}}' if ca < 0 <= cb else f'{papbi:^{2*w+1}}' if ca < 0 > cb else f'?#?#?'
        elif k < 0:
            if   ca >= 0:  ret = f'{pa*pb:>{w}}/{p:<{w}}'  ;  ret = f'{ret:^{2*w+1}}'
        slog(f'{pfx}{k:4} {p:4} : {a:2} {ca:2} {b:2} {cb:2} {ret=}') if dbg else None  ;  return ret
    ####################################################################################################################################################################################################
    @staticmethod
    def fmtR2(a, ca, b, cb, w, k, i=None, j=None):
        qa = '1' if ca == 0 else f'{a}' if ca == 1 else f'{a}' if ca == -1 else f'{a}^{abs(ca)}'
        qb = '1' if cb == 0 else f'{b}' if cb == 1 else f'{b}' if cb == -1 else f'{b}^{abs(cb)}' 
        p = 2 ** abs(k) if k is not None else 1  ;  qaqbi = f'{p}/({qa}*{qb})'  ;  ret = Z  ;  dbg = 0
        pfx = f'{i:4} {j:4} ' if i is not None and j is not None else Z
        if   k is None:
            qa  = f'{a}^{ca}'   ;    qb = f'{b}^{cb}'
            ret = f'{qa:>{w}}/{qb:<{w}}'   ;   k = utl.NONE
        elif k == 0:
            ret = f'{qa:>{w}}*{qb:<{w}}' if ca >= 0 < cb else f'{qa:>{w}}/{qb:<{w}}' if ca >= 0 >= cb else f'{qb:>{w}}/{qa:<{w}}' if ca < 0 <= cb else f'{qaqbi:^{2*w+1}}' if ca < 0 > cb else f'?#?#?'
        elif k > 0:
            qa = f'{p}*{qa}' if ca >= 0 <= cb or ca >= 0 > cb else qa  ;  qb = f'{p}*{qb}' if ca < 0 <= cb else qb
            ret = f'{qa:>}*{qb:<}' if ca >= 0 < cb else f'{qa:>}/{qb:<}' if ca >= 0 >= cb else f'{qb:>}/{qa:<}' if ca < 0 <= cb else f'{qaqbi}' if ca < 0 > cb else f'?#?#?'  ;  ret = f'{ret:^{2*w+1}}'
        elif k < 0:
            if   ca >= 0:  ret = f'{qa:>}*{qb}/{p:<}'  ;  ret = f'{ret:^{2*w+1}}'
        slog(f'{pfx}{k:4} {p:2} : {a:2} {ca:2} {b:2} {cb:2} {ret=}') if dbg else None  ;  return ret
    ####################################################################################################################################################################################################
    @staticmethod
    def fmtR3(a, ca, b, cb, w, k, i=None, j=None):
        p = 2 ** abs(k) if k is not None else 1  ;  sa = f'{a}{i2spr(abs(ca))}'  ;  sb = f'{b}{i2spr(abs(cb))}'  ;  sasbi = f'1/({sa}*{sb})'  ;  ret = Z  ;  dbg = 0
        pfx = f'{i:4} {j:4} ' if i is not None and j is not None else Z
        if   k is None:
            ret = f'{sa:>{w}}/{sb:<{w}}'   ;   k = utl.NONE
        elif not k:
            ret = f'{sa:>{w}}*{sb:<{w}}' if ca >= 0 < cb else f'{sa:>{w}}/{sb:<{w}}' if ca >= 0 >= cb else f'{sb:>{w}}/{sa:<{w}}' if ca < 0 <= cb else f'{sasbi:^{2*w+1}}' if ca < 0 > cb else f'?#?#?'
        elif k > 0:
            sa = f'{p}*{sa}' if ca >= 0 <= cb or ca >= 0 > cb else sa  ;  sb = f'{p}*{sb}' if ca < 0 <= cb else sb  ;  sasbi = f'{p}/({sa}*{sb})'
            ret = f'{sa:>}*{sb:<}' if ca >= 0 <= cb else f'{sa:>}/{sb:<}' if ca >= 0 > cb else f'{sb:>}/{sa:<}' if ca < 0 <= cb else f'{sasbi}' if ca < 0 > cb else f'?#?#?'  ;  ret = f'{ret:^{2*w+1}}'
        elif k < 0:
            if   ca >= 0:  ret = f'{sa:>}*{sb}/{p:<}'  ;  ret = f'{ret:^{2*w+1}}'
        slog(f'{pfx}{k:4} {p:2} : {a:2} {ca:2} {b:2} {cb:2} {ret=}') if dbg else None  ;  return ret
    ####################################################################################################################################################################################################
    @staticmethod
    def fmtRA(a, ca, w=Z):        pa     =   a ** ca                               ;  return f'{pa:^{w}}' if ist(pa, int) else f'{pa:^{w}.{w-4}f}'
    @staticmethod
    def fmtRB(b, cb, w=Z):        pb     =   b ** cb                               ;  return f'{pb:^{w}}' if ist(pb, int) else f'{pb:^{w}.{w-4}f}'

    def fdvdr(self, a, ca, b, cb):      n = max(len(self.fmtRA(a, ca)), len(self.fmtRB(b, cb)))    ;  return n * '/'
########################################################################################################################################################################################################
########################################################################################################################################################################################################
#def fmtR0_PTH(a, ca, b, cb, w):   pa, pb =   float(a ** ca) ,   float(b ** cb)   ;  return f'{pa/pb:^{w}.{w-4}f}'
#def fmtR1_PTH(a, ca, b, cb, w):   pa, pb =   a ** ca        ,   b ** cb          ;  return f'{pa:>{w}}/{pb:<{w}}' # if ist(pa, int) else f'{pa:>{w}.{w-4}}/{pb:<{w}.{w-4}f}'
#def fmtRA_PTH(a, ca, w=Z):        pa     =   a ** ca                             ;  return f'{pa:^{w}}' if ist(pa, int) else f'{pa:^{w}.{w-4}f}'
#def fmtRB_PTH(b, cb, w=Z):        pb     =   b ** cb                             ;  return f'{pb:^{w}}' if ist(pb, int) else f'{pb:^{w}.{w-4}f}'
#def fmtR2_PTH(a, ca, b, cb, w):   qa, qb = f'{a}^{ca}'      , f'{b}^{cb}'        ;  return f'{qa:>{w}}/{qb:<{w}}'
#def fmtR3_PTH(a, ca, b, cb, w):   sa, sb = f'{a}{i2spr(ca)}', f'{b}{i2spr(cb)}'  ;  return f'{sa:>{w}}/{sb:<{w}}' 
#def fdvdr_PTH(a, ca, b, cb):      n = max(len(fmtRA_PTH(a, ca)), len(fmtRB_PTH(b, cb)))  ;  return n * '/'

#def NEW_addFmtRs_PTH(a, ca, b, cb, rs, u=4, w=9):
#    assert rs and ist(rs, list),  f'{rs=} {type(rs)=} {a=} {ca} {b} {cb} {u=} {w=}'   ;   lr = len(rs)
##    r0s, r2s, r3s = [], [], []   ;   r1s = [] if lr == 4 else None   ;   rAs = [] if lr == 5 else None   ;   rBs = [] if lr == 5 else None
#    r0s, r2s, r3s = rs[0], rs[-2], rs[-1] #         ;   r1s, rAs, rBs = None, None, None
#    r1s, rAs, rBs = None,  None,   None
#    if   lr == 4:       r1s      = rs[1]           ;   r1s.append(fmtR1_PTH(a, ca, b, cb, u))
#    elif lr == 5:       rAs, rBs = rs[1], rs[2]    ;   rAs.append(fmtRA_PTH(a, ca, w))    ;    rBs.append(fmtRB_PTH(b, cb, w)) # if ist(b**cb, int) else w3))
#    r0s.append(fmtR0_PTH(a, ca, b, cb, w))
#    r2s.append(fmtR2_PTH(a, ca, b, cb, u)) # if u >= 9 else None
#    r3s.append(fmtR3_PTH(a, ca, b, cb, u))
#    if   lr == 4:   return r0s, r1s,      r2s, r3s
#    elif lr == 5:   return r0s, rAs, rBs, r2s, r3s
########################################################################################################################################################################################################
########################################################################################################################################################################################################
#def addFmtRs(a, ca, b, cb, rs, u=4, w=9, k=None, i=None, j=None):
#    assert rs and ist(rs, list),  f'{rs=} {type(rs)=} {a=} {ca} {b} {cb} {u=} {w=}'   ;   lr = len(rs)
#    r0s, r2s, r3s = rs[0], rs[-2], rs[-1]          ;   r1s, rAs, rBs = None, None, None
#    if   lr == 4:       r1s      = rs[1]           ;   r1s.append(fmtR1(a, ca, b, cb, u, k, i, j))
#    elif lr == 5:       rAs, rBs = rs[1], rs[2]    ;   rAs.append(fmtRA(a, ca, w))    ;    rBs.append(fmtRB(b, cb, w)) # if ist(b**cb, int) else w3))
#    r0s.append(fmtR0(a, ca, b, cb, w, k, i, j))
#    r2s.append(fmtR2(a, ca, b, cb, u, k, i, j)) # if u >= 9 else None
#    r3s.append(fmtR3(a, ca, b, cb, u, k, i, j))
#    if   lr == 4:   return r0s, r1s,      r2s, r3s
#    elif lr == 5:   return r0s, rAs, rBs, r2s, r3s
########################################################################################################################################################################################################
#def fmtR0(a, ca, b, cb, w, k, i=None, j=None):
#    pa = a ** ca   ;   pb = b ** cb   ;   p = 2 ** k if k else 1   ;   dbg = 0
#    pfx = f'{i:4} {j:4} ' if i is not None and j is not None else Z
#    if k is None:     v = pa/pb       ;   k = utl.NONE
#    else:             v = p*pa*pb
#    ret = f'{v:^{w}.{w-4}f}' if ist(v, float) else f'{v:^{w}}'
#    slog(f'{pfx}{k:4} {p:4} : {a:2} {ca:2} {b:2} {cb:2} {ret=}') if dbg else None  ;  return ret
########################################################################################################################################################################################################
#def fmtR1(a, ca, b, cb, w, k, i=None, j=None):
#    pa = a ** abs(ca)  ;  pb = b ** abs(cb)  ;  p = 2 ** abs(k) if k else 1  ;  papbi = f'{p}/{pa*pb}'  ;  ret = Z  ;  dbg = 0
#    pfx = f'{i:4} {j:4} ' if i is not None and j is not None else Z
#    if   k is None:
#        ret = f'{pa:>{w}}/{pb:<{w}}'   ;   k = utl.NONE
#    elif k == 0:
#        ret = f'{pa:>{w}}*{pb:<{w}}' if ca >= 0 < cb else f'{pa:>{w}}/{pb:<{w}}' if ca >= 0 >= cb else f'{pb:>{w}}/{pa:<{w}}' if ca < 0 <= cb else f'{papbi:^{2*w+1}}' if ca < 0 > cb else f'?#?#?'
#    elif k > 0:
#        pa = pa * p if ca >= 0 <= cb or ca >= 0 > cb else pa  ;  pb = pb * p if ca < 0 <= cb else pb
#        ret = f'{pa:>{w}}*{pb:<{w}}' if ca >= 0 < cb else f'{pa:>{w}}/{pb:<{w}}' if ca >= 0 >= cb else f'{pb:>{w}}/{pa:<{w}}' if ca < 0 <= cb else f'{papbi:^{2*w+1}}' if ca < 0 > cb else f'?#?#?'
#    elif k < 0:
#        if   ca >= 0:  ret = f'{pa*pb:>{w}}/{p:<{w}}'  ;  ret = f'{ret:^{2*w+1}}'
#    slog(f'{pfx}{k:4} {p:4} : {a:2} {ca:2} {b:2} {cb:2} {ret=}') if dbg else None  ;  return ret
########################################################################################################################################################################################################
#def fmtR2(a, ca, b, cb, w, k, i=None, j=None):
#    qa = '1' if ca == 0 else f'{a}' if ca == 1 else f'{a}' if ca == -1 else f'{a}^{abs(ca)}'
#    qb = '1' if cb == 0 else f'{b}' if cb == 1 else f'{b}' if cb == -1 else f'{b}^{abs(cb)}' 
#    p = 2 ** abs(k) if k is not None else 1  ;  qaqbi = f'{p}/({qa}*{qb})'  ;  ret = Z  ;  dbg = 0
#    pfx = f'{i:4} {j:4} ' if i is not None and j is not None else Z
#    if   k is None:
#        qa  = f'{a}^{ca}'   ;    qb = f'{b}^{cb}'
#        ret = f'{qa:>{w}}/{qb:<{w}}'   ;   k = utl.NONE
#    elif k == 0:
#        ret = f'{qa:>{w}}*{qb:<{w}}' if ca >= 0 < cb else f'{qa:>{w}}/{qb:<{w}}' if ca >= 0 >= cb else f'{qb:>{w}}/{qa:<{w}}' if ca < 0 <= cb else f'{qaqbi:^{2*w+1}}' if ca < 0 > cb else f'?#?#?'
#    elif k > 0:
#        qa = f'{p}*{qa}' if ca >= 0 <= cb or ca >= 0 > cb else qa  ;  qb = f'{p}*{qb}' if ca < 0 <= cb else qb
#        ret = f'{qa:>}*{qb:<}' if ca >= 0 < cb else f'{qa:>}/{qb:<}' if ca >= 0 >= cb else f'{qb:>}/{qa:<}' if ca < 0 <= cb else f'{qaqbi}' if ca < 0 > cb else f'?#?#?'  ;  ret = f'{ret:^{2*w+1}}'
#    elif k < 0:
#        if   ca >= 0:  ret = f'{qa:>}*{qb}/{p:<}'  ;  ret = f'{ret:^{2*w+1}}'
#    slog(f'{pfx}{k:4} {p:2} : {a:2} {ca:2} {b:2} {cb:2} {ret=}') if dbg else None  ;  return ret
########################################################################################################################################################################################################
#def fmtR3(a, ca, b, cb, w, k, i=None, j=None):
#    p = 2 ** abs(k) if k is not None else 1  ;  sa = f'{a}{i2spr(abs(ca))}'  ;  sb = f'{b}{i2spr(abs(cb))}'  ;  sasbi = f'1/({sa}*{sb})'  ;  ret = Z  ;  dbg = 0
#    pfx = f'{i:4} {j:4} ' if i is not None and j is not None else Z
#    if   k is None:
#        ret = f'{sa:>{w}}/{sb:<{w}}'   ;   k = utl.NONE
#    elif not k:
#        ret = f'{sa:>{w}}*{sb:<{w}}' if ca >= 0 < cb else f'{sa:>{w}}/{sb:<{w}}' if ca >= 0 >= cb else f'{sb:>{w}}/{sa:<{w}}' if ca < 0 <= cb else f'{sasbi:^{2*w+1}}' if ca < 0 > cb else f'?#?#?'
#    elif k > 0:
#        sa = f'{p}*{sa}' if ca >= 0 <= cb or ca >= 0 > cb else sa  ;  sb = f'{p}*{sb}' if ca < 0 <= cb else sb  ;  sasbi = f'{p}/({sa}*{sb})'
#        ret = f'{sa:>}*{sb:<}' if ca >= 0 <= cb else f'{sa:>}/{sb:<}' if ca >= 0 > cb else f'{sb:>}/{sa:<}' if ca < 0 <= cb else f'{sasbi}' if ca < 0 > cb else f'?#?#?'  ;  ret = f'{ret:^{2*w+1}}'
#    elif k < 0:
#        if   ca >= 0:  ret = f'{sa:>}*{sb}/{p:<}'  ;  ret = f'{ret:^{2*w+1}}'
#    slog(f'{pfx}{k:4} {p:2} : {a:2} {ca:2} {b:2} {cb:2} {ret=}') if dbg else None  ;  return ret

#def fdvdr(a, ca, b, cb):      n = max(len(fmtRA(a, ca)), len(fmtRB(b, cb)))    ;  return n * '/'
#def fmtRA(a, ca, w=Z):        pa     =   a ** ca                               ;  return f'{pa:^{w}}' if ist(pa, int) else f'{pa:^{w}.{w-4}f}'
#def fmtRB(b, cb, w=Z):        pb     =   b ** cb                               ;  return f'{pb:^{w}}' if ist(pb, int) else f'{pb:^{w}.{w-4}f}'
########################################################################################################################################################################################################
########################################################################################################################################################################################################
#def NEW_addFmtRs_JST(a, ca, b, cb, rs, u=4, w=9, k=None, i=None, j=None):
#    assert rs and ist(rs, list),  f'{rs=} {type(rs)=} {a=} {ca} {b} {cb} {u=} {w=}'   ;   lr = len(rs)
##    r0s, r2s, r3s = [], [], []   ;   r1s = [] if lr == 4 else None   ;   rAs = [] if lr == 5 else None   ;   rBs = [] if lr == 5 else None
#    r0s, r2s, r3s = rs[0], rs[-2], rs[-1] #         ;   r1s, rAs, rBs = None, None, None
#    r1s, rAs, rBs = None,  None,   None
#    if   lr == 4:       r1s      = rs[1]           ;   r1s.append(fmtR1_JST(a, ca, b, cb, u, k, i, j))
#    elif lr == 5:       rAs, rBs = rs[1], rs[2]    ;   rAs.append(fmtRA_JST(a, ca, w))    ;    rBs.append(fmtRB_JST(b, cb, w)) # if ist(b**cb, int) else w3))
#    r0s.append(fmtR0_JST(a, ca, b, cb, w, k))
#    r2s.append(fmtR2_JST(a, ca, b, cb, u, k, i, j)) # if u >= 9 else None
#    r3s.append(fmtR3_JST(a, ca, b, cb, u, k, i, j))
#    if   lr == 4:   return r0s, r1s,      r2s, r3s
#    elif lr == 5:   return r0s, rAs, rBs, r2s, r3s
    
#def fmtRA_JST(a, ca, w=Z):        pa     =   a ** ca                             ;  return f'{pa:{w}}'
#def fmtRB_JST(b, cb, w=Z):        pb     =   b ** cb                             ;  return f'{pb:{w}}'
#def fdvdr_JST(a, ca, b, cb):      n = max(len(fmtRA_JST(a, ca)), len(fmtRB_JST(b, cb)))  ;  return n * '/'
#def fmtR0_JST(a, ca, b, cb, w, k=0): # w=11
#    pa = a ** ca  ;  pb = b ** abs(cb)  ;  p = 2 ** k if k is not None else 1
#    v = p*pa/pb if cb < 0 else p*pa*pb
#    return f'{v:^{w}.{w-4}f}' if ist(v, float) else f'{v:^{w}}'
########################################################################################################################################################################################################
#def fmtR1_JST(a, ca, b, cb, w, k, i, j):
#    pa = a ** abs(ca)  ;  pb = b ** abs(cb)  ;  l = 2 ** abs(k) if k else None  ;  papbi = f'{l}/{pa*pb}'  ;  ret = Z  ;  dbg = 0
#    if   not k:
#        ret = f'{pa:>{w}}*{pb:<{w}}' if ca >= 0 < cb else f'{pa:>{w}}/{pb:<{w}}' if ca >= 0 >= cb else f'{pb:>{w}}/{pa:<{w}}' if ca < 0 <= cb else f'{papbi:^{2*w+1}}' if ca < 0 > cb else f'?#?#?'
#    elif k > 0:
#        pa = pa * l if ca >= 0 <= cb or ca >= 0 > cb else pa  ;  pb = pb * l if ca < 0 <= cb else pb
#        ret = f'{pa:>{w}}*{pb:<{w}}' if ca >= 0 < cb else f'{pa:>{w}}/{pb:<{w}}' if ca >= 0 >= cb else f'{pb:>{w}}/{pa:<{w}}' if ca < 0 <= cb else f'{papbi:^{2*w+1}}' if ca < 0 > cb else f'?#?#?'
#    elif k < 0:
#        if   ca >= 0:  ret = f'{pa*pb:>{w}}/{l:<{w}}'  ;  ret = f'{ret:^{2*w+1}}'
#    slog(f'{i} {j} {k:2} {l:2} {a} {ca:2} {b} {cb:2} {ret=}') if dbg else None  ;  return ret
########################################################################################################################################################################################################
#def fmtR2_JST(a, ca, b, cb, w, k, i, j):
#    qa = f'1' if ca == 0 else f'{a}' if ca == 1 else f'{a}' if ca == -1 else f'{a}^{abs(ca)}'
#    qb = f'1' if cb == 0 else f'{b}' if cb == 1 else f'{b}' if cb == -1 else f'{b}^{abs(cb)}' 
#    l = 2 ** abs(k) if k is not None else 1  ;  qaqbi = f'{l}/({qa}*{qb})'  ;  ret = Z  ;  dbg = 0
#    if   not k:
#        ret = f'{qa:>{w}}*{qb:<{w}}' if ca >= 0 < cb else f'{qa:>{w}}/{qb:<{w}}' if ca >= 0 >= cb else f'{qb:>{w}}/{qa:<{w}}' if ca < 0 <= cb else f'{qaqbi:^{2*w+1}}' if ca < 0 > cb else f'?#?#?'
#    elif k > 0:
#        qa = f'{l}*{qa}' if ca >= 0 <= cb or ca >= 0 > cb else qa  ;  qb = f'{l}*{qb}' if ca < 0 <= cb else qb
#        ret = f'{qa:>}*{qb:<}' if ca >= 0 < cb else f'{qa:>}/{qb:<}' if ca >= 0 >= cb else f'{qb:>}/{qa:<}' if ca < 0 <= cb else f'{qaqbi}' if ca < 0 > cb else f'?#?#?'  ;  ret = f'{ret:^{2*w+1}}'
#    elif k < 0:
#        if   ca >= 0:  ret = f'{qa:>}*{qb}/{l:<}'  ;  ret = f'{ret:^{2*w+1}}'
#    slog(f'{i} {j} {k:2} {l:2} {a} {ca:2} {b} {cb:2} {ret=}') if dbg else None  ;  return ret
########################################################################################################################################################################################################
#def fmtR3_JST(a, ca, b, cb, w, k, i, j):
#    l = 2 ** abs(k) if k is not None else 1  ;  sa = f'{a}{i2spr(abs(ca))}'  ;  sb = f'{b}{i2spr(abs(cb))}'  ;  sasbi = f'1/({sa}*{sb})'  ;  ret = Z  ;  dbg = 0
#    if   not k:
#        ret = f'{sa:>{w}}*{sb:<{w}}' if ca >= 0 < cb else f'{sa:>{w}}/{sb:<{w}}' if ca >= 0 >= cb else f'{sb:>{w}}/{sa:<{w}}' if ca < 0 <= cb else f'{sasbi:^{2*w+1}}' if ca < 0 > cb else f'?#?#?'
#    elif k > 0:
#        sa = f'{l}*{sa}' if ca >= 0 <= cb or ca >= 0 > cb else sa  ;  sb = f'{l}*{sb}' if ca < 0 <= cb else sb  ;  sasbi = f'{l}/({sa}*{sb})'
#        ret = f'{sa:>}*{sb:<}' if ca >= 0 <= cb else f'{sa:>}/{sb:<}' if ca >= 0 > cb else f'{sb:>}/{sa:<}' if ca < 0 <= cb else f'{sasbi}' if ca < 0 > cb else f'?#?#?'  ;  ret = f'{ret:^{2*w+1}}'
#    elif k < 0:
#        if   ca >= 0:  ret = f'{sa:>}*{sb}/{l:<}'  ;  ret = f'{ret:^{2*w+1}}'
#    slog(f'{i} {j} {k:2} {l:2} {a} {ca:2} {b} {cb:2} {ret=}') if dbg else None  ;  return ret
########################################################################################################################################################################################################
#def fmtR0(a, ca, b, cb, w):   pa, pb =   float(a ** ca) ,   float(b ** cb)   ;  return f'{pa/pb:{w}}'
#def fmtR1(a, ca, b, cb, w):   pa, pb =   a ** ca        ,   b ** cb          ;  return f'{pa:>{w}}/{pb:<{w}}'
#def fmtRA(a, ca, w=Z):        pa     =   a ** ca                             ;  return f'{pa:{w}}'
#def fmtRB(b, cb, w=Z):        pb     =   b ** cb                             ;  return f'{pb:{w}}'
#def fmtR2(a, ca, b, cb, w):   qa, qb = f'{a}^{ca}'      , f'{b}^{cb}'        ;  return f'{qa:>{w}}/{qb:<{w}}'
#def fmtR3(a, ca, b, cb, w):   sa, sb = f'{a}{i2spr(ca)}', f'{b}{i2spr(cb)}'  ;  return f'{sa:>{w}}/{sb:<{w}}' 
#def fdvdr(a, ca, b, cb):      n = max(len(fmtRA(a, ca)), len(fmtRB(b, cb)))  ;  return n * '/'
    
#def addFmtRs(r0s, rAs, rBs, r2s, r3s, a, ca, b, cb, w3, ww, u): # u=4 w3='^9.5f' ww='^9'
#    r0s.append(fmtR0(a, ca, b, cb, w3))
#    rAs.append(fmtRA(a, ca, ww if ist(a**ca, int) else w3))
#    rBs.append(fmtRB(b, cb, ww if ist(b**cb, int) else w3))
#    r2s.append(fmtR2(a, ca, b, cb, u)) # if u >= 9 else None
#    r3s.append(fmtR3(a, ca, b, cb, u))
########################################################################################################################################################################################################
########################################################################################################################################################################################################
'''        
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
