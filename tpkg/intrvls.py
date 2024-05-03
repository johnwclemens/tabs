from tpkg       import utl
from tpkg       import unic
from tpkg       import notes
from tpkg.notes import Notes
from collections import Counter
import math

F, N, S                = unic.F,   unic.N,   unic.S
W, Y, Z, slog, ist     = utl.W,    utl.Y,    utl.Z,    utl.slog,   utl.ist
fmtl, fmtm, fmtf, fmtg = utl.fmtl, utl.fmtm, utl.fmtf, utl.fmtg

SUPERS, MAX_FREQ_IDX, ACCD_TONES = utl.SPRSCRPT_INTS,    utl.MAX_FREQ_IDX,    notes.ACCD_TONES
NT, A4_INDEX, CM_P_M, V_SOUND    = notes.NT,   notes.A4_INDEX,   notes.CM_P_M,   notes.V_SOUND

FLATS, SHRPS  = notes.FLATS, notes.SHRPS
F440s, F432s  = notes.F440s, notes.F432s

# COFS = {'C', 'G', 'D', 'A', 'E', 'B/Cb', 'F#/Gb', 'C#/Db', 'Ab', 'Eb', 'Bb', 'F'}
########################################################################################################################################################################################################
def i2spr(i): # todo fixme still being used by old code that hasn't been retired yet
    if i < 0: return '-' + Z.join( SUPERS[int(digit)] for digit in str(i) if str.isdigit(digit) )
    else:     return       Z.join( SUPERS[int(digit)] for digit in str(i) )

def stck5ths(n):     return [ stackI(3, 2, i) for i in range(1, n+1) ]
def stck4ths(n):     return [ stackI(2, 3, i) for i in range(1, n+1) ]
def stackI(a, b, c): return [ a, b, c ]
def fabc(abc):       return [ fmtl(e, w=2, d=Z) for e in abc ]
########################################################################################################################################################################################################
########################################################################################################################################################################################################
class Intonation(object):
    def __init__(self, n='C', rf=440, ss=V_SOUND, csv=0):
        self.rf     = rf
        self.ss     = ss
        self.csv    = csv
        self.i      = Notes.N2I[n] + 48
        self.j      = 0
        self.k      = 0
        self.m      = n
        self.n      = Z
        self.o      = Z
        self.centKs = []
        self.ivalKs = []
        self.ck2ikm = {} # self.set_ck2ikm()
        self.nimap  = {}
        self.ckmap  = {} # self.reset_ckmap()
        self.COFMA  = {'C':('F♯', 'G♭'), 'G':('C♯', 'D♭'),  'D':('G♯', 'A♭'), 'A':('D♯', 'E♭'), 'E':('A♯', 'B♭'), 'B':('E♯', 'F'), 'F♯':('B♯', 'C'), 'C♯':('G', 'G'),  'G♯':('D', 'D'),    'D♯':('A', 'A'),    'A♯':('E', 'F♭'),   'E♯':('B', 'C♭'),   'B♯':('F♯', 'G♭')}
        self.COFMB  = {'C':('F♯', 'G♭'), 'F':('B',  'C♭'), 'B♭':('E', 'F♭'), 'E♭':('A', 'A'),  'Ab':('D', 'D'),  'D♭':('G', 'G'),  'G♭':('B♯', 'C'), 'C♭':('E♯', 'F'), 'F♭':('A♯', 'B♭'), 'B♭♭':('D♯', 'E♭'), 'E♭♭':('G♯', 'A♭'), 'A♭♭':('C♯', 'D♭'), 'D♭♭':('F♯', 'B♭')}
        self.COFM   = self.COFMA | self.COFMB
        self.FREFS  = F440s if self.rf == 440 else F432s
        self.w0     = CM_P_M * self.ss
        self.f0     = self.FREFS[self.i]
    ####################################################################################################################################################################################################
    def reset_ckmap(self):  return { ck:{'Count':0} for ck in list(self.centKs) } # todo call this once @ end of dmpMaps()
    def set_ck2ikm(self):   self.ck2ikm = { self.centKs[i]: k for i, k in enumerate(self.ivalKs) }   ;   return self.ck2ikm # todo this base class method initializes and or sets self.ck2ikm
    ####################################################################################################################################################################################################
    @staticmethod
    def i2spr(i):
        if i < 0: return '-' + Z.join( SUPERS[int(digit)] for digit in str(i) if str.isdigit(digit) )
        else:     return       Z.join( SUPERS[int(digit)] for digit in str(i) )

    @staticmethod
    def r2cents(r): return math.log2(r) * NT * 100

    @staticmethod
    def i2dCent(k):
        return k  if   0<=k<50  else k-100 if  50<=k<150 else k-200 if 150<=k<250 else k-300  if 250<=k<350  else k-400  if  350<=k<450  else k-500  if  450<=k<550   else k-600 if 550<=k<650 else \
            k-700 if 650<=k<750 else k-800 if 750<=k<850 else k-900 if 850<=k<950 else k-1000 if 950<=k<1050 else k-1100 if 1050<=k<1150 else k-1200 if 1150<=k<=1200 else None
    ####################################################################################################################################################################################################
    def abc2r(self, a, b, c): # assumes a==2 or b==2, probably too specific, Pythagorean only, rename?
        pa0, pb0 = a ** c, b ** c
        r0       = pa0 / pb0
        r, j     = self.norm(r0)   ;   assert r == r0 * (2 ** j),  f'{r=} {r0=} {j=}'
        ca       = c + j if j > 0 else c
        cb       = c - j if j < 0 else c
        return r, ca, cb

    def abcs(self, a=7, b=6): # todo generalize m2bc ?
        abc1 = stck5ths(a)
        abc2 = stck4ths(b)
        abc3 = [ stackI(3, 2, 0) ]   ;   abc3.extend(abc1)   ;   abc3.extend(abc2)   ;   abc3.append(stackI(2, 1, 1))
        abc4 = sorted(abc3, key= lambda z: self.abc2r(z[0], z[1], z[2])[0])
        return [ abc1, abc2, abc3, abc4 ] 

    def i2Abcs(self): # todo generalize m2bc ? use the mod operator ? exploring the last else
        f = self.abcs   ;   i = self.i   ;   j = self.j
        return f(6, 5) if j==i   else f(5, 6) if j==i+7 else f(4, 7) if j==i+2  else f(3, 8) if j==i+9 else f(2, 9)  if j==i+4 else f(1, 10) if j==i+11 else \
            f(0, 11)   if j==i+6 else f(7, 4) if j==i+5 else f(8, 3) if j==i+10 else f(9, 2) if j==i+3 else f(10, 1) if j==i+8 else f(11, 0) if j==i+1  else f(13, 13)
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
    def fmtNPair(self, k, i, j=1, d=0, dbg=0): # set j=k or j=self.j ?
        n0, _   = self.i2nPair(self.i, s=1)   ;   d = '/' if d==1 else W if d==0 else d   ;   j = k if j else self.j
        n1, n2  = self.i2nPair(k + i, b=0 if i in (4, 6, 11) or j in (self.i + 4, self.i + 6, self.i + 11) else 1, s=1, e=1)   ;   slog(f'{self.i=} {n0=} {n1=} {n2=}') if dbg else None
        if i and i != NT:
            if          n1 == self.COFM[n0][1]:   return n2
            elif n2 and n2 != self.COFM[n0][1]:   n1 += d + n2
        slog(f'return {n1=}') if dbg else None
        return n1

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
    def setup(self, o, csv=0):
        self.csv = csv
        x = 0
        if   o == 0:
            self.nimap = {}
            slog(    f'P1  0-{NT}+{x} {self.i=:2} {self.j=:2} {self.k=:2} {self.m=:2} {self.n=:2} {self.o=:2} {self.csv=}',        p=0)
            for i in range(0, NT + x):
                self.j = self.i + (i * 7) % (NT + x)
                slog(f'P1  0-{NT}+{x} {self.i=:2} {self.j=:2} {self.k=:2} {self.m=:2} {self.n=:2} {self.o=:2} {self.csv=} : {i=}', p=0)
                self._setup()
        elif o == 1:
            self.nimap = {}
            slog(    f'P2A 7-{NT}+{x} {self.i=:2} {self.j=:2} {self.k=:2} {self.m=:2} {self.n=:2} {self.o=:2} {self.csv=}',        p=0)
            for i in range(7, NT + x):
                self.j = self.i + (i * 7) % (NT + x)
                slog(f'P2A 7-{NT}+{x} {self.i=:2} {self.j=:2} {self.k=:2} {self.m=:2} {self.n=:2} {self.o=:2} {self.csv=} : {i=}', p=0)
                self._setup()
            slog(    f'P2B 0-7{x=:1}  {self.i=:2} {self.j=:2} {self.k=:2} {self.m=:2} {self.n=:2} {self.o=:2} {self.csv=}',        p=0)
            for i in range(0, 7):
                self.j = self.i + (i * 7) % (NT + x)
                slog(f'P2B 0-7{x=:1}  {self.i=:2} {self.j=:2} {self.k=:2} {self.m=:2} {self.n=:2} {self.o=:2} {self.csv=} : {i=}', p=0)
                self._setup()

    def setup2(self, o, o2, u=13, dbg=0, csv=0):
        self.csv = csv
        x = 0
        if   o == 0:
            self.nimap = {}
            slog(    f'P1  0-{NT}+{x} {self.i=:2} {self.j=:2} {self.k=:2} {self.m=:2} {self.n=:2} {self.o=:2} {self.csv=} : {o2=} {u=}', p=0) if dbg else None
            for i in range(0, NT):
                self.j = self.i + (i * 7) % (NT + x)
                slog(f'P1  0-{NT}+{x} {self.i=:2} {self.j=:2} {self.k=:2} {self.m=:2} {self.n=:2} {self.o=:2} {self.csv=} : {i=}',       p=0) if dbg else None
                self._setup(u=u, o=o2, dbg=dbg)
        elif o == 1:
            self.nimap = {}
            slog(    f'P2A 7-{NT}+{x} {self.i=:2} {self.j=:2} {self.k=:2} {self.m=:2} {self.n=:2} {self.o=:2} {self.csv=} : {o2=} {u=}', p=0) if dbg else None
            for i in range(7, NT):
                self.j = self.i + (i * 7) % (NT + x)
                slog(f'P2A 7-{NT}+{x} {self.i=:2} {self.j=:2} {self.k=:2} {self.m=:2} {self.n=:2} {self.o=:2} {self.csv=} : {i=}',       p=0) if dbg else None
                self._setup(u=u, o=o2, dbg=dbg)
            slog(    f'P2B 0-7{x=:1}  {self.i=:2} {self.j=:2} {self.k=:2} {self.m=:2} {self.n=:2} {self.o=:2} {self.csv=} : {o2=} {u=}', p=0) if dbg else None
            for i in range(0, 7):
                self.j = self.i + (i * 7) % (NT + x)
                slog(f'P2B 0-7{x=:1}  {self.i=:2} {self.j=:2} {self.k=:2} {self.m=:2} {self.n=:2} {self.o=:2} {self.csv=} : {i=}',       p=0) if dbg else None
                self._setup(u=u, o=o2, dbg=dbg)
    ####################################################################################################################################################################################################
    def dmpNiMap( self, ni, x, upd=0, dbg=1): pass
    def dmpCkMap( self, u=9, o=0, dbg=1):     pass

    def dmpCkMap2(self):
        ks = []   ;   x = 8   ;   w = f'^{x}'   ;   o = '|'
        for k, v in self.ckmap.items():
            ks.append(f'{k:4} {v["Count"]:2}')
        slog(f'{fmtl(ks, w=w, s=o)}', p=0)

    def updCkMap(self, ck, ckm, n, f, abc, cent, idx): # f = f0 * pa/pb # n if k==ik else W*2 # todo move to base class, but abc arg and key is an issue
        assert ck in ckm.keys(),  f'{ck=} {ckm.keys()=}'
        ckm[ck]['Count'] = ckm[ck]['Count'] + 1 if 'Count' in ckm[ck] else 1
        ckm[ck]['Freq']  = f                     ;   ckm[ck]['Wavln'] = self.w0 / f
        ckm[ck]['Cents'] = cent                  ;   ckm[ck]['DCent'] = self.i2dCent(cent)
        ckm[ck]['Note']  = n                     ;   ckm[ck]['Abcd']  = abc
        ckm[ck]['Ival']  = self.ck2ikm[ck]       ;   ckm[ck]['Index'] = idx
    ####################################################################################################################################################################################################
    def dmpIndices(self, pfx=Z, w=0):
        mm, ff = (Y, 3) if self.csv else(W, 1)   ;   ww = f'^{w}'   ;   n = len(self.centKs)
        ii     = [ f'{i}' for i in range(n) ]    ;   slog(f'{pfx}{fmtl(ii, w=ww, s=mm, d=Z)}', p=0, f=ff)
    ####################################################################################################################################################################################################
    def _setup(self, u=9, o=0, dbg=1):
        x = 13  ;  mm, nn, oo, ff = (Y, Y, Y, 3) if self.csv else (W, Z, '|', 1)  ;  cki, ww, y, z, _, f0, w3 = -1, f'^{x}', 6, x-2, x*W, self.FREFS[self.j], [W, W, W]  ;  pfx = f'{mm}  k  {mm}{nn} {nn}'
        self.k = 0  ;  self.o = Z  ;  self.n = Notes.i2n()[self.j % NT]
        if dbg: slog(f'BGN {self.__str__()} {self.i=:2} {self.j=:2} {self.k=:2} {self.m=:2} {self.n=:2} {self.o=:2} {u=} {o=} {self.csv=} {dbg=}', p=0, f=ff)  ;  self.dmpIndices(pfx, x)  ;  self.dmpDataTableLine(x+1)
        cs, ds, ii, ns, vs, fs, ws = [], [], [], [], [], [], []   ;   r0s, rAs, rBs, r1s, r2s, r3s = [], [], [], [], [], []   ;   abcdMap = []  ;  ckm = self.reset_ckmap()
        tmp = self.i2Abcs()  ;  abc0 = list(tmp[3])  ;  abc1, abc2, abc3, abc4 = fabc(tmp[0]), fabc(tmp[1]), fabc(tmp[2]), fabc(tmp[3])  ;  abc1.insert(0, fmtl(w3, w=2, d=Z))  ;  abc2.insert(0, fmtl(w3, w=2, d=Z)) # insert blanks to align log/csv file
        for i, e in enumerate(abc0):
            a, b, c = e[0], e[1], e[2]  ;  r, ca, cb = self.abc2r(a, b, c)  ;  abcd = [a, ca, b, cb]  ;  f = r * f0  ;  w = self.w0 / f  ;  n = self.fmtNPair(self.j, i)  ;  cki += 1
            c = self.r2cents(r)  ;  d = self.i2dCent(c)  ;  rc = round(c)  ;  assert rc in self.ck2ikm,  f'{rc=} not in ck2ikm {self.i=} {i=} {self.j=} {n=} {c=} {r=} {abcd=} {fmtm(self.ck2ikm, d=Z)}' # ;  v = self.ck2ikm[cki]
            while cki < len(self.centKs) and self.centKs[cki] < rc:
                v = self.ck2ikm[self.centKs[cki]]  ;  vs.append(v) # ;  c = self.centKs[cki]  ;  vs.append(v)  ;  cs.append(c)  ;  ds.append(d)
                ii.append(_)  ;  cs.append(_)  ;  ds.append(_)  ;  fs.append(_)  ;  ws.append(_)  ;  ns.append(_)  ;  r0s.append(_)  ;  rAs.append(_)  ;  rBs.append(_)  ;  r1s.append(_)  ;  r2s.append(_)  ;  r3s.append(_)
                cki += 1  ;  j = len(ii)-1  ;  abc1.insert(j, fmtl(w3, w=2, d=Z))  ;  abc2.insert(j, fmtl(w3, w=2, d=Z))  ;  abc3.insert(j, fmtl(w3, w=2, d=Z))  ;  abc4.insert(j, fmtl(w3, w=2, d=Z))
#            else: slog(f'{cki=} welse: {self.centKs[cki]=} < {rc=}, {fmtl(self.centKs)=}') if dbg else None
            v = self.ck2ikm[rc]  ;  vs.append(v)  ;  ii.append(i)  ;  fs.append(fmtf(f, z))  ;  ws.append(fmtf(w, z))  ;  cs.append(fmtf(c, z-4))  ;  ds.append(fmtg(d, z-4))  ;  abcdMap.append(abcd)  ;  ns.append(n)
            r0s, rAs, rBs, r1s, r2s, r3s = self.addFmtRs(a, ca, b, cb, rs=[r0s, rAs, rBs, r1s, r2s, r3s], u=y, w=x,     i=i, j=rc)
            if not dbg:   self.updCkMap(rc, ckm, n, f, abcd, c, i)
        self.nimap[self.j] = [ckm, tmp[2], abcdMap]   ;   sfx = f'{nn}]'   ;   sfxc = f'{nn}]{mm}cents'   ;   sfxf = f'{nn}]{mm}Hz'   ;   sfxw = f'{nn}]{mm}cm'   ;   cks = self.centKs
        while len(abc1) < len(abc3): abc1.append(fmtl(w3, w=2, d=Z)) # append blanks for alignment in log/csv files
        while len(abc2) < len(abc3): abc2.append(fmtl(w3, w=2, d=Z)) # append blanks for alignment in log/csv files
        if dbg:
            slog(f'{mm}CentK{mm}{nn}[{nn}{fmtl(cks,  w=ww, s=oo, d=Z)}{sfxc}', p=0, f=ff)
            slog(f'{mm}Itval{mm}{nn}[{nn}{fmtl(vs,   w=ww, s=oo, d=Z)}{sfx}',  p=0, f=ff)
            slog(f'{mm}Note {mm}{nn}[{nn}{fmtl(ns,   w=ww, s=oo, d=Z)}{sfx}',  p=0, f=ff)
            slog(f'{mm}Ratio{mm}{nn}[{nn}{fmtl(r0s,  w=ww, s=oo, d=Z)}{sfx}',  p=0, f=ff)
            slog(f'{mm}Rati1{mm}{nn}[{nn}{fmtl(r1s,  w=ww, s=oo, d=Z)}{sfx}',  p=0, f=ff)
            slog(f'{mm}Rati2{mm}{nn}[{nn}{fmtl(r2s,  w=ww, s=oo, d=Z)}{sfx}',  p=0, f=ff)
            slog(f'{mm}Rati3{mm}{nn}[{nn}{fmtl(r3s,  w=ww, s=oo, d=Z)}{sfx}',  p=0, f=ff)
            slog(f'{mm}Freq {mm}{nn}[{nn}{fmtl(fs,   w=ww, s=oo, d=Z)}{sfxf}', p=0, f=ff)
            slog(f'{mm}Wavln{mm}{nn}[{nn}{fmtl(ws,   w=ww, s=oo, d=Z)}{sfxw}', p=0, f=ff)
            slog(f'{mm}Index{mm}{nn}[{nn}{fmtl(ii,   w=ww, s=oo, d=Z)}{sfx}',  p=0, f=ff)
            slog(f'{mm} ABC1{mm}{nn}[{nn}{fmtl(abc1, w=ww, s=oo, d=Z)}{sfx}',  p=0, f=ff)
            slog(f'{mm} ABC2{mm}{nn}[{nn}{fmtl(abc2, w=ww, s=oo, d=Z)}{sfx}',  p=0, f=ff)
            slog(f'{mm} ABC3{mm}{nn}[{nn}{fmtl(abc3, w=ww, s=oo, d=Z)}{sfx}',  p=0, f=ff)
            slog(f'{mm} ABC4{mm}{nn}[{nn}{fmtl(abc4, w=ww, s=oo, d=Z)}{sfx}',  p=0, f=ff)
            slog(f'{mm}Cents{mm}{nn}[{nn}{fmtl(cs,   w=ww, s=oo, d=Z)}{sfxc}', p=0, f=ff)
            slog(f'{mm}DCent{mm}{nn}[{nn}{fmtl(ds,   w=ww, s=oo, d=Z)}{sfxc}', p=0, f=ff)    ;   self.dmpDataTableLine(x+1)
        self.dmpMaps(u, o=o, dbg=dbg)  ;  slog(f'END {self.__str__()} {self.i=:2} {self.j=:2} {self.k=:2} {self.m=:2} {self.n=:2} {self.o=:2} {u=} {o=} {self.csv=} {dbg=}', p=0, f=ff) if dbg else None
    ####################################################################################################################################################################################################
    def dmpMaps(self, u, o, dbg=1): # todo generalize m2bc, but needs dmpNiMap() and dmpCkMap() also ?
        if dbg:
            self.dmpNiMap(0, x=13, upd=1, dbg=dbg)
            self.dmpNiMap(1, x=13, upd=1, dbg=dbg)
            self.dmpNiMap(2, x=13, upd=1, dbg=dbg)
            self.dmpNiMap(3, x=13, upd=1, dbg=dbg)
            self.dmpNiMap(4, x=13, upd=1, dbg=dbg)
            self.dmpCk2Ik(   x=13                )
            self.dmpCkMap(   u=u,         dbg=dbg)
            self.dmpNiMap(0, x=9,  upd=0, dbg=dbg)
            self.dmpNiMap(1, x=9,  upd=0, dbg=dbg)
            self.dmpNiMap(2, x=9,  upd=0, dbg=dbg)
            self.dmpNiMap(3, x=9,  upd=0, dbg=dbg)
            self.dmpNiMap(4, x=9,  upd=0, dbg=dbg)
            self.dmpCk2Ik(   x=9                 )
            self.chckIvls(                       )
            self.chckIvl2(                       )
        else:
            assert u == 12 or u == 13, f'{u=} {self.i=} {self.j=} {self.k=} {self.m=} {o=} {dbg=} {self.csv=}'
            self.dmpNiMap(  4, x=13, upd=1, dbg=dbg)
            self.dmpCkMap(     u=u,  o=o,   dbg=dbg)
        self.ckmap = self.reset_ckmap() # todo call this once @ end of dmpMaps()
    ####################################################################################################################################################################################################
    def dmpCk2Ik(self, x=13): # todo move to base class
        mm, oo, f1, f2 = (Y, Y, 3, 3) if self.csv else (W, '|', 1, -3)   ;   pfx = f'{9*W}' if x == 9 else f'{11*W}' if x == 13 else Z
        if   x ==  9: slog(f'{pfx}{fmtm(self.ck2ikm, w=4, wv=2, s=3*W, d=Z)}', p=0, f=f1) if not self.csv else None
        elif x == 13: slog(f'{pfx}{fmtm(self.ck2ikm, w=4, wv=2, s=7*W, d=Z)}', p=0, f=f1) if not self.csv else None
        else:         slog(f'{pfx}{fmtm(self.ck2ikm, w=4, wv=2, s=oo,  d=Z)}', p=0, f=f2)
    ####################################################################################################################################################################################################
    def chckIvls(self):
        mm, nn, oo, ff  = (Y, Y, Y, 3) if self.csv else (W, Z, '|', 1)
        slog(f'BGN chckIvls() {self.csv=}', p=0, f=ff)
        msgs, ws = [], [3, 7, 7, 7, 6, 5, 10, 4, 3]
        keys = list(list(self.ckmap.values())[0].keys())   ;   keys[0] = 'Knt'   ;   keys[-1] = 'Idx'
        slog(f'Jdx{mm} {nn}{nn}CK{mm}  {mm}{fmtl(keys, u="^", w=ws, s=mm, d=Z)}', p=0, f=ff)
        for i, (ck, cv) in enumerate(self.ckmap.items()):
            msg = f'{i:2}{nn}[{mm}{ck:4}{nn}:{mm}[{mm}'
            for k, v in cv.items():
                msg += f'{fmtf(v, 7)}{mm}' if k in ("Cents", "Freq", "Wavln") else f'{fmtg(v, 6)}{mm}' if k=="DCent" else f'{fmtl(v, s=W):11}{mm}' if k=="Abcd" else f'{v:2}{mm}' if k in ("Count", "Index") else f'{v:5}{mm}' if k=="Note" else f'{v:3}{mm}' if k=="Ival" else f'{v:6}{mm}'
            msg += f']{nn}]'   ;   msgs.append(msg)
        msgs = '\n'.join(msgs)
        slog(f'{msgs}', p=0, f=ff)
        slog(f'END chckIvls() {self.csv=}', p=0, f=ff)

    def chckIvl2(self, cm=0):
        ff = 3 if self.csv else -3
        if cm:    self.dmpCkMap2()
        cntr = Counter()
        keys = list(self.ckmap.keys())
        for k in keys:
            if self.ckmap[k]["Count"] > 0: self.chckIvl2A(k, cntr)
        sl = cntr.most_common()   ;   m, n = 0, 0
        for e in sl:
            n += e[1]   ;   m += 1
        slog(f'{n=} {m=} {fmtl(sl)}', p=0, f=ff)
        slog(f'{fmtm(cntr)}', p=0, f=ff)

    def chckIvl2A(self, key, cntr):
        mm, nn, oo, ff  = (Y, Y, Y, 3) if self.csv else (W, Z, '|', -3)  ;  x = 8  ;  uu = f'{x}'  ;   ww = f'{x}.3f'
        cs = []   ;   blnk = x*W   ;   cmk = 'Cents'
        cmv  = self.ckmap[key][cmk]
        for i, (ck, cv) in enumerate(self.ckmap.items()):
            for k2, v2 in cv.items():
                if k2 == cmk:
                    v  = abs(cv[cmk] - cmv)
                    cntr[f'{v:{ww}}'] += 1
                    cs.append(f'{v:{ww}}')
                    break
            else:
                cs.append(blnk)
            if cs and i==len(self.ckmap)-1:   slog(f'{fmtl(cs, w=uu, s=oo)}', p=0, f=ff)
    ########################################################################################################################################################################################################
    def dmpDataTableLine(self, w=10):
        c = '-'   ;   nn, mm, t = (Y, Y, Y) if self.csv else (Z, W, '|')
        col = f'{c * (w-1)}'   ;   n = len(self.centKs)
        cols = t.join([ col for _ in range(n) ])
        slog(f'{mm}     {mm}{nn} {nn}{cols}', p=0, f=3 if self.csv else 1)
    ####################################################################################################################################################################################################
    def addFmtRs(self, a, ca, b, cb, rs, u=4, w=9, k=None, i=None, j=None):
        assert rs and ist(rs, list),  f'{rs=} {type(rs)=} {a=} {ca} {b} {cb} {u=} {w=}'   ;   lr = len(rs)
        r0s, r2s, r3s = rs[0], rs[-2], rs[-1]          ;   r1s, rAs, rBs = None, None, None
        if   lr == 2:   rAs, rBs      = rs[0], rs[1]
        elif lr == 4:   r1s           = rs[1]
        elif lr == 5:   rAs, rBs      = rs[1], rs[2]
        elif lr == 6:   rAs, rBs, r1s = rs[1], rs[2], rs[3]
        r0s.append(self.fmtR0(a, ca, b, cb, w, k, i, j))
        rAs.append(self.fmtRA(a, ca, w))                 if lr == 2 or lr == 5 or lr == 6 else None
        rBs.append(self.fmtRB(b, cb, w))                 if lr == 2 or lr == 5 or lr == 6 else None
        r1s.append(self.fmtR1(a, ca, b, cb, u, k, i, j)) if lr == 4            or lr == 6 else None
        r2s.append(self.fmtR2(a, ca, b, cb, u, k, i, j)) # if u >= 9 else None
        r3s.append(self.fmtR3(a, ca, b, cb, u, k, i, j))
        if   lr == 2:   return      rAs, rBs
        elif lr == 4:   return r0s,           r1s, r2s, r3s
        elif lr == 5:   return r0s, rAs, rBs,      r2s, r3s
        elif lr == 6:   return r0s, rAs, rBs, r1s, r2s, r3s
    ####################################################################################################################################################################################################
    @staticmethod
    def fmtR0(a, ca, b, cb, w, k, i=None, j=None):
        pa = a ** ca   ;   pb = b ** cb   ;   p = 2 ** k if k else 1   ;   dbg = 0
        pfx = f'{i:4} {j:4} ' if i is not None and j is not None else Z
        if k is None:     v = pa/pb       ;   k = utl.NONE
        else:             v = p*pa*pb
        if w >= 9:        ret = f'{v:^{w}.{w-4}f}' if ist(v, float) else f'{v:^{w}}'
        else:             ret = f'{v:^{w}.{w-2}f}' if ist(v, float) else f'{v:^{w}}'
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
class OTS(Intonation):
    def __init__(self, n='C', rf=440, ss=V_SOUND, csv=0):
        super().__init__(n=n, rf=rf, ss=ss, csv=csv)
        self.ivalKs = ['P1', 'm2', 'm2', 'M2', 'M2', 'm3', 'm3', 'M3', 'M3', 'P4', 'A3', 'd5', 'A4', 'd6', 'P5', 'm6', 'm6', 'M6', 'M6', 'm7', 'm7', 'M7', 'M7', 'P8']
        self.centKs = [   0,  90,  112,  182,  204,  294,  316,  384,  386,  498,  522,  590,  610,  678,  702,  792,  814,  884,  906,  996,  1018, 1088, 1110, 1200]
        self.set_ck2ikm() # todo this base class method initializes and or sets self.ck2ikm
        
    def dmpData(self, csv=0): # todo fixme 
        self.csv = csv
        slog(f'BGN {self.i=:2} {self.m=:2} {self.rf=} {self.ss=} {self.csv=}', p=0)
#        k = Notes.N2I[self.n] + 48 # + 2
        self.dmpOts()
        slog(f'END {self.i=:2} {self.m=:2} {self.rf=} {self.ss=} {self.csv=}', p=0)
    
    def dmpOts(self):
        slog(f'BGN Overtone Series {self.i=:2} {self.m=:2} {self.csv=}', p=0)
        ww, dd, mm, nn, ff = ('^6', '[', Y, Y, 3) if self.csv else ('^6', '[', W, Z, 1)
        cs, ds, ns, fs, ws = [], [], [], [], []   ;   ref = f'440A' if self.rf == 440 else f'432A'   ;   fr = range(1, 256+1)
        f0    = self.FREFS[0]
        for i in fr:
            f = f0 * i              ;      w = self.w0 / f
            n, n2  = self.f2nPair(f, b=0 if i in (17, 22, 25, 28) else 1)
            fn = self.norm(f/f0)[0]
            c  = self.r2cents(fn)   ;      d = self.i2dCent(c)
            fs.append(fmtf(f, 6))   ;     ns.append(n)            ;     ws.append(fmtf(w, 6))
            cs.append(fmtf(c, 6))   ;     ds.append(fmtg(d, 6 if d >= 0 else 5))
        fs   = mm.join(fs)          ;     ws = mm.join(ws)        ;     ns = fmtl(ns, w=ww, s=mm, d=Z)   ;     cs = fmtl(cs, w=ww, s=mm, d=Z)   ;     ds = fmtl(ds, w=ww, s=mm, d=Z)
        ref += f'{nn}[{nn}'         ;   sfxf = f'{mm}]{mm}Hz'     ;   sfxw = f'{mm}]{mm}cm'              ;   sfxc = f'{mm}]{mm}cents'           ;   sfxd = f'{mm}]{mm}dcents'
        pfxn = f'notes{nn}[{nn}'    ;   pfxc = f'cents{nn}[{nn}'  ;   pfxd = f'dcnts{nn}[{nn}'           ;    sfx = f'{mm}]{nn}'
        slog(f'Index{nn}[{nn}{fmtl(list(fr), w=ww, d=Z, s=mm)}{sfx}', p=0, f=ff)
        slog(f'f{ref}{fs}{sfxf}',  p=0, f=ff)
        slog(f'{pfxn}{ns}{sfx}',   p=0, f=ff)
        slog(f'{pfxc}{cs}{sfxc}',  p=0, f=ff)
        slog(f'{pfxd}{ds}{sfxd}',  p=0, f=ff)
        slog(f'w{ref}{ws}{sfxw}',  p=0, f=ff)
        slog(f'END Overtone Series {self.i=:2} {self.m=:2} {self.csv=}', p=0)
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
