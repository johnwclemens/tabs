from tpkg       import utl
#from tpkg       import notes
from tpkg.notes import Notes
from tpkg       import intrvls as ivls
import math

W,  Y,  Z,  slog,  ist = utl.W,    utl.Y,    utl.Z,    utl.slog,   utl.ist
fmtl, fmtm, fmtf, fmtg = utl.fmtl, utl.fmtm, utl.fmtf, utl.fmtg

NT, A4_INDEX, CM_P_M, V_SOUND = ivls.NT, ivls.A4_INDEX, ivls.CM_P_M, ivls.V_SOUND

#fmtR0, fmtR1, fmtR2, fmtR3, fmtRA, fmtRB, fdvdr, addFmtRs = ivls.fmtR0, ivls.fmtR1, ivls.fmtR2, ivls.fmtR3, ivls.fmtRA, ivls.fmtRB, ivls.fdvdr, ivls.addFmtRs
########################################################################################################################################################################################################
########################################################################################################################################################################################################
def stck5ths(n):     return [ stackI(3, 2, i) for i in range(1, n+1) ]
def stck4ths(n):     return [ stackI(2, 3, i) for i in range(1, n+1) ]
def stackI(a, b, c): return [ a, b, c ]
def fabc(abc):       return [ fmtl(e, w=2, d=Z) for e in abc ]

def abc2r(a, b, c): # assumes a==2 or b==2, probably too specific, Pythagorean only, rename?
    pa0, pb0 = a ** c, b ** c
    r0       = pa0 / pb0
    r, j     = ivls.Intonation.norm(r0)   ;   assert r == r0 * (2 ** j),  f'{r=} {r0=} {j=}'
    ca       = c + j if j > 0 else c
    cb       = c - j if j < 0 else c
#    pa, pb   = a ** ca, b ** cb
#    r        = pa / pb   ;   assert r == r0 * (2 ** j),  f'{r=} {r0=} {j=}'
    return r, ca, cb

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
        cents     = ivls.Intonation.r2cents(p)
        kf, ki    = cents, round(cents)
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
        cents     = ivls.Intonation.r2cents(p)
        kf, ki    = cents, round(cents)
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
########################################################################################################################################################################################################
class Pthgrn(ivls.Intonation):
    def __init__(self, n='C', rf=440, ss=V_SOUND, csv=0):
        super().__init__(n=n, rf=rf, ss=ss, csv=csv)
        self.ivalKs = ['P1', 'm2', 'A1', 'd3', 'M2', 'm3', 'A2', 'd4', 'M3', 'P4', 'A3', 'd5', 'A4', 'd6', 'P5', 'm6', 'A5', 'd7', 'M6', 'm7', 'A6', 'd8', 'M7', 'P8']
#                     [  0    1     2     3     4     5     6     7     8     9    10    11    12    13    14    15    16    17    18    19     20    21    22    23 ]
        self.centKs = [  0,   90,  114,  180,  204,  294,  318,  384,  408,  498,  522,  588,  612,  678,  702,  792,  816,  882,  906,  996,  1020, 1086, 1110, 1200]
        self.set_ck2ikm() # todo this base class method initializes and or sets self.ck2ikm
        self.ckmap  = self.reset_ckmap() # freq ratio in cents to ival counts and data
    ####################################################################################################################################################################################################
    ####################################################################################################################################################################################################
    @staticmethod
    def abcs(a=7, b=6): # todo generalize m2bc ?
        abc1 = stck5ths(a)
        abc2 = stck4ths(b)
        abc3 = [ stackI(3, 2, 0) ]   ;   abc3.extend(abc1)   ;   abc3.extend(abc2)   ;   abc3.append(stackI(2, 1, 1))
        abc4 = sorted(abc3, key= lambda z: abc2r(z[0], z[1], z[2])[0])
        return [ abc1, abc2, abc3, abc4 ] 

    def i2Abcs(self): # todo generalize m2bc ?
        f = self.abcs   ;   i = self.i   ;   j = self.j
        return f(6, 5) if j==i else f(5, 6) if j==i+7 else f(4, 7) if j==i+2  else f(3, 8) if j==i+9 else f(2, 9)  if j==i+4 else f(1, 10) if j==i+11 else f(0, 11) if j==i+6 \
                               else f(7, 4) if j==i+5 else f(8, 3) if j==i+10 else f(9, 2) if j==i+3 else f(10, 1) if j==i+8 else f(11, 0) if j==i+1  else f(12, 0)
    ####################################################################################################################################################################################################
    def fmtNPair(self, k, i, dbg=0): # todo generalize m2bc ? fixme
        n0, _   = self.i2nPair(self.i, s=1)
        n1, n2  = self.i2nPair(k + i, b=0 if i in (4, 6, 11) or k in (self.i + 4, self.i + 6, self.i + 11) else 1, s=1, e=1)   ;   slog(f'{self.i=} {n0=} {n1=} {n2=}') if dbg else None
        if i and i != NT:
            if          n1 == self.COFM[n0][1]:   return n2
            elif n2 and n2 != self.COFM[n0][1]:   n1 += '/' + n2
        slog(f'return {n1=}') if dbg else None
        return n1
    ####################################################################################################################################################################################################
    def _setup(self, u=9, o=0, dbg=1): # todo generalize m2bc ?
        x = 13  ;  mm, nn, oo, ff = (Y, Y, Y, 3) if self.csv else (W, Z, '|', 1)  ;  cki, ww, y, z, _, f0, w3 = -1, f'^{x}', 6, x-2, x*W, self.FREFS[self.j], [W, W, W]  ;  pfx = f'{mm}  k  {mm}{nn} {nn}'  ;  self.k = 0  ;  self.o = Z  ;  self.n = Notes.i2n()[self.j % NT]
        if dbg: slog(f'BGN Pythagorean {self.i=:2} {self.j=:2} {self.k=:2} {self.m=:2} {self.n=:2} {self.o=:2} {u=} {o=} {self.csv=} {dbg=}', p=0, f=ff)  ;  ii = [ f'{i}' for i in range(2 * NT) ]  ;  slog(f'{pfx}{fmtl(ii, w=ww, s=mm, d=Z)}', p=0, f=ff)  ;  self.dmpDataTableLine(x + 1)
        cs, ds, ii, ns, vs, fs, ws = [], [], [], [], [], [], []   ;   r0s, rAs, rBs, r1s, r2s, r3s = [], [], [], [], [], []   ;   abcdMap = []  ;  ckm = self.reset_ckmap()
        tmp = self.i2Abcs()  ;  abc0 = list(tmp[3])  ;  abc1, abc2, abc3, abc4 = fabc(tmp[0]), fabc(tmp[1]), fabc(tmp[2]), fabc(tmp[3])  ;  abc1.insert(0, fmtl(w3, w=2, d=Z))  ;  abc2.insert(0, fmtl(w3, w=2, d=Z)) # insert blanks to align log/csv file
        for i, e in enumerate(abc0):
            a, b, c = e[0], e[1], e[2]  ;  r, ca, cb = abc2r(a, b, c)  ;  abcd = [a, ca, b, cb]  ;  f = r * f0  ;  w = self.w0 / f  ;  n = self.fmtNPair(self.j, i)  ;  cki += 1
            c = self.r2cents(r)  ;  d = self.i2dCent(c)  ;  rc = round(c)  ;  assert rc in self.ck2ikm,  f'{rc=} not in ck2ikm {self.i=:2} {i=} {self.j=} {n=} {c=} {r=} {abcd=}'  ;  v = self.ck2ikm[rc]
            while self.centKs[cki] < rc:
                ii.append(_)  ;  cs.append(_)  ;  ds.append(_)  ;  fs.append(_)  ;  ws.append(_) ;  ns.append(_)  ;  vs.append(_)  ;  r0s.append(_)  ;  rAs.append(_)  ;  rBs.append(_)  ;  r1s.append(_)  ;  r2s.append(_)  ;  r3s.append(_)
                cki += 1  ;  j = len(ii)-1  ;  abc1.insert(j, fmtl(w3, w=2, d=Z))  ;  abc2.insert(j, fmtl(w3, w=2, d=Z))  ;  abc3.insert(j, fmtl(w3, w=2, d=Z))  ;  abc4.insert(j, fmtl(w3, w=2, d=Z))
            ii.append(i)  ;  fs.append(fmtf(f, z))  ;  ws.append(fmtf(w, z))  ;  cs.append(fmtf(c, z-4))  ;  ds.append(fmtg(d, z-4))  ;  abcdMap.append(abcd)  ;  ns.append(n)  ;  vs.append(v)
            r0s, rAs, rBs, r1s, r2s, r3s = self.addFmtRs(a, ca, b, cb, rs=[r0s, rAs, rBs, r1s, r2s, r3s], u=y, w=x,     i=i, j=rc)
            if not dbg:   self.upd_ckmap(rc, ckm, n, f, abcd, c, i)
        self.nimap[self.j] = [ckm, tmp[2], abcdMap]   ;   sfx = f'{nn}]'   ;   sfxc = f'{nn}]{mm}cents'   ;   sfxf = f'{nn}]{mm}Hz'   ;   sfxw = f'{nn}]{mm}cm'   ;   cks = self.centKs
        while len(abc1) < len(abc3): abc1.append(fmtl(w3, w=2, d=Z)) # append blanks for alignment in log/csv files
        while len(abc2) < len(abc3): abc2.append(fmtl(w3, w=2, d=Z)) # append blanks for alignment in log/csv files
        if dbg:
            slog(f'{mm}CentK{mm}{nn}[{nn}{fmtl(cks,  w=ww, s=oo, d=Z)}{sfxc}', p=0, f=ff)
            slog(f'{mm}Note {mm}{nn}[{nn}{fmtl(ns,   w=ww, s=oo, d=Z)}{sfx}',  p=0, f=ff)
            slog(f'{mm}Itval{mm}{nn}[{nn}{fmtl(vs,   w=ww, s=oo, d=Z)}{sfx}',  p=0, f=ff)
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
            slog(f'{mm}DCent{mm}{nn}[{nn}{fmtl(ds,   w=ww, s=oo, d=Z)}{sfxc}', p=0, f=ff)    ;   self.dmpDataTableLine(x + 1)
        self.dmpMaps(u, o=o, dbg=dbg)  ;  slog(f'END Pythagorean {self.i=:2} {self.j=:2} {self.k=:2} {self.m=:2} {self.n=:2} {self.o=:2} {u=} {o=} {self.csv=} {dbg=}', p=0, f=ff) if dbg else None
    ####################################################################################################################################################################################################
    def epsilon(self, dbg=0): # todo generalize m2bc ?
        ccents = self.comma()
        ecents = ccents / NT
        if dbg:  slog(f'Epsilon = Comma / {NT} = {ccents:10.5f} / {NT} = {ecents:10.5f} cents')
        return ecents
        
    def comma(self, dbg=0): # todo generalize m2bc ?
        n, i, iv  = NT, -1, '5' # 3**12 / 2**19 = 3¹²/2¹⁹ = 531441 / 524288 = 1.0136432647705078, log2(1.0136432647705078) = 0.019550008653874178, 1200 * log2() = 23.460010384649014
        s5s       = stck5ths(n)
        a, b, c   = s5s[i]
        r, ca, cb = abc2r(a, b, c)
        if dbg:   slog(f'{n} 5ths, s5s     = {fmtl(s5s)}')
        if dbg:   slog(f'{n} 5ths, s5s[{i}] = {fmtl(s5s[i])} {ca=} {cb=} {r=:10.8}')
        assert [a, b, c] == [3, 2, n],  f'{a=} {b=} {c=} {[3, 2, n]}'
        pa, pb    = a ** ca, b ** cb
        cratio    = pa / pb
        q         = f'{a}{self.i2spr(ca)}/{b}{self.i2spr(cb)}'
        ccents    = self.r2cents(cratio)
        if dbg:   slog(f'Comma = {pa:6}/{pb:<6} = {a}**{ca}/{b}**{cb} = {q:6} = {cratio:10.8f} = {ccents:10.5f} cents')
        ecents    = ccents / NT
        if dbg:   slog(f'Epsilon = Comma / {NT} = {ccents:10.5f} / {NT} = {ecents:10.5f} cents')
        return ccents
    ####################################################################################################################################################################################################
    def dmpNiMap(self, ni, x, upd=0, dbg=1): # x=13 or x=9 #todo generalize m2bc ?
        mm, nn, oo, ff = (Y, Y, Y, 3) if self.csv else (W, Z, '|', 1)  ;  ww, _ = f'^{x}', W*x  ;    yy = 6 if x==13 else 4
        ii = [ f'{i}' for i in range(2 * NT) ]   ;   pfx, pfx2 = Z, f'{mm}  k  {mm}{nn} {nn}'   ;   sfx = f'{nn}]'   ;   f0 = self.FREFS[self.j] #  ;   w2 = '7.2f'
        if dbg:   slog(f'{pfx2}{fmtl(ii, w=ww, s=mm, d=Z)}', p=0, f=ff) if ni == 0 else None    ;   self.dmpDataTableLine(x + 1) if ni==0 else None
        for i, (kk, v) in enumerate(self.nimap.items()):
            rat0, rat2, rat3, cents, cfnts = [], [], [], [], []    ;    cki = -1 #  ;   self.k = kk
            rat1 = [] if x==13 or x==6 or x==7 else None    ;   ratA = [] if x == 9 else None   ;   ratB = [] if x == 9 else None
            for j, e in enumerate(v[2]):
                n    = self.fmtNPair(kk, j)   ;   a, ca, b, cb = e   ;  pa, pb = a ** ca, b ** cb   ;  pd = [f'{i:x}', f'{kk:2}', f'{n:2}'] if dbg else [f'{i:x}', f'{kk:2}  ']
                pfx  = f'{mm.join(pd)}{nn}[{nn}' if dbg else pfx     ;     sfx = f' {nn}{n:2}' if not dbg else sfx
                cent = self.r2cents(pa/pb)    ;   rc = round(cent)   ;    cki += 1
                if dbg and upd and ni == 4:   self.upd_ckmap(rc, self.ckmap, n if kk==self.j else W*2, f0*pa/pb, e, cent, j)
                while  self.centKs[cki] < rc:
                    rat0.append(_)   ;  rat2.append(_)   ;   rat3.append(_)    ;    cki += 1    ;  cents.append(_) #  ;   cfnts.append(_)
                    rat1.append(_) if x==13 else None    ;   ratA.append(_) if x==9 else None   ;   ratB.append(_) if x==9 else None
                cents.append(rc) #  ;   cfnts.append(f'{cent:{w2}}')
                if   x==9:          self.addFmtRs(a, ca, b, cb, rs=[rat0, ratA, ratB, rat2, rat3], u=yy, w=x,     i=i, j=j)
                elif x==13:         self.addFmtRs(a, ca, b, cb, rs=[rat0,       rat1, rat2, rat3], u=yy, w=x,     i=i, j=j)
                elif x==6 or x==7:  self.addFmtRs(a, ca, b, cb, rs=[rat0,       rat1, rat2, rat3], u=yy, w=x,     i=i, j=j)
            if dbg:
                if   ni==0:           slog(f'{pfx}{Z.join(fmtl(rat0,  w=ww, s=oo, d=Z))}{sfx}',  p=0, f=ff)
                elif ni==1 and x==9:  slog(f'{pfx}{Z.join(fmtl(ratA,  w=ww, s=oo, d=Z))}{sfx}',  p=0, f=ff)  ;  slog(f'{pfx}{Z.join(fmtl(ratB, w=ww, s=oo, d=Z))}{sfx}', p=0, f=ff)
                elif ni==1 and x==13: slog(f'{pfx}{Z.join(fmtl(rat1,  w=ww, s=oo, d=Z))}{sfx}',  p=0, f=ff)
                elif ni==2:           slog(f'{pfx}{Z.join(fmtl(rat2,  w=ww, s=oo, d=Z))}{sfx}',  p=0, f=ff)
                elif ni==3:           slog(f'{pfx}{Z.join(fmtl(rat3,  w=ww, s=oo, d=Z))}{sfx}',  p=0, f=ff)
                elif ni==4:           slog(f'{pfx}{Z.join(fmtl(cents, w=ww, s=oo, d=Z))}{sfx}',  p=0, f=ff)
            elif ni==0:               slog(f'{pfx}{Z.join(fmtl(rat0,  w=ww, s=oo, d=Z))}{sfx}',  p=0, f=ff if self.csv else -3)
            elif ni==5:               slog(f'{pfx}{Z.join(fmtl(cents, w=ww, s=oo, d=Z))}{sfx}',  p=0, f=ff if self.csv else -3)
        if dbg: self.dmpDataTableLine(x + 1)   ;   slog(f'{pfx2}{fmtl(ii, w=ww, s=mm, d=Z)}',    p=0, f=ff) if ni == 4 else None
    ####################################################################################################################################################################################################
    def dmpCkMap(self, u=9, o=0, dbg=1): # todo generalize m2bc ?
        mm, nn, oo, ff = (Y, Y, Y, 3) if self.csv else (W, Z, '|', 1)  ;  f0, sk, v, ww, y = self.FREFS[self.j], 0, Z, f'^{u}', 4  ;  _ = u*W if dbg else 7*W  ;  cks = self.centKs if dbg else None
        ns, fs, ws, vs = [], [], [], []  ;  cs, ds, d2s, qs, ks, cksi = [], [], [], [], [], []  ;  r0s, rAs, rBs, r2s, r3s = [], [], [], [], []  ;  ckmap = self.ckmap if dbg else self.nimap[self.j][0]
        sfx = f'{nn}]'   ;   sfxc = f'{nn}]{mm}cents'   ;   sfxf = f'{nn}]{mm}Hz'   ;   sfxw = f'{nn}]{mm}cm'
        for i, ck in enumerate(self.centKs):
            ival = self.ck2ikm[ck]    ;    vs.append(ival)    ;   assert ckmap and ck in ckmap,  f'{self.j=} {i=} {ival=} {ck=} {ckmap=} {self.ckmap=} {self.nimap[self.j][0]=} {dbg=}'
            if ckmap[ck]['Count'] > 0:
                assert ival == ckmap[ck]['Ival'],  f'{ival=} {ck=} {ckmap[ck]["Ival"]=}'    ;   a, ca, b, cb = ckmap[ck]['Abcd']   ;   q = self.fdvdr(a, ca, b, cb)
                r0s, rAs, rBs, r2s, r3s = self.addFmtRs(a, ca, b, cb, rs=[r0s, rAs, rBs, r2s, r3s], u=y, w=u if dbg else 7,     i=i, j=ck)
                f, w, n, c, d, k, i2   = self.getCkMapVal(ckmap, ck, a, ca, b, cb, f0, self.w0)   ;   sk += k   ;   self.k = Notes.N2I[n[:2]] + 48 if n in Notes.N2I else self.k  ;  self.o = n[:2] if n in Notes.N2I else self.o
                cksi.append(int(round(c)))  ;  cs.append(f'{fmtf(c, u-4)}')   ; ds.append(f'{fmtf(d, u-4)}') ; fs.append(f'{fmtf(f, u-2)}') ; ws.append(f'{fmtf(w, u-2)}')
            else: n, d, k, q = _, _, 0, Z  ;  cksi.append(ck) ; cs.append(_) ; ds.append(_) ; fs.append(_) ; ws.append(_) ; r0s.append(_) ; rAs.append(_) ; rBs.append(_) ; r2s.append(_) ; r3s.append(_)
            if dbg:   ns.append(n)  ;  d2s.append(d)  ;  ks.append(k)  ;  qs.append(q)  ;  self.dmpIvals(i, cksi, ks, d2s)
        if dbg:
            ii = [ f'{i}' for i in range(2 * NT) ]
            slog(f'{mm}  k  {mm}{nn} {nn}{fmtl(ii,  w=ww, s=mm, d=Z)}',       p=0, f=ff)  ;  self.dmpDataTableLine(u + 1)
            slog(f'{mm}Centk{mm}{nn}[{nn}{fmtl(cks, w=ww, s=oo, d=Z)}{sfxc}', p=0, f=ff)
            slog(f'{mm}Itval{mm}{nn}[{nn}{fmtl(vs,  w=ww, s=oo, d=Z)}{sfx}',  p=0, f=ff)
            slog(f'{mm}Note {mm}{nn}[{nn}{fmtl(ns,  w=ww, s=oo, d=Z)}{sfx}',  p=0, f=ff)
            slog(f'{mm}Rati0{mm}{nn}[{nn}{fmtl(r0s, w=ww, s=oo, d=Z)}{sfx}',  p=0, f=ff)
            slog(f'{mm}RatiA{mm}{nn}[{nn}{fmtl(rAs, w=ww, s=oo, d=Z)}{sfx}',  p=0, f=ff)
            slog(f'{mm} A/B {mm}{nn}[{nn}{fmtl(qs,  w=ww, s=oo, d=Z)}{sfx}',  p=0, f=ff)
            slog(f'{mm}RatiB{mm}{nn}[{nn}{fmtl(rBs, w=ww, s=oo, d=Z)}{sfx}',  p=0, f=ff)
            slog(f'{mm}Rati2{mm}{nn}[{nn}{fmtl(r2s, w=ww, s=oo, d=Z)}{sfx}',  p=0, f=ff) if u >= 9 else None
            slog(f'{mm}Rati3{mm}{nn}[{nn}{fmtl(r3s, w=ww, s=oo, d=Z)}{sfx}',  p=0, f=ff)
            slog(f'{mm}Freq {mm}{nn}[{nn}{fmtl(fs,  w=ww, s=oo, d=Z)}{sfxf}', p=0, f=ff)
            slog(f'{mm}Wavln{mm}{nn}[{nn}{fmtl(ws,  w=ww, s=oo, d=Z)}{sfxw}', p=0, f=ff)
            slog(f'{mm}Cents{mm}{nn}[{nn}{fmtl(cs,  w=ww, s=oo, d=Z)}{sfxc}', p=0, f=ff)
            slog(f'{mm}DCent{mm}{nn}[{nn}{fmtl(ds,  w=ww, s=oo, d=Z)}{sfxc}', p=0, f=ff)
            slog(f'{mm}Count{mm}{nn}[{nn}{fmtl(ks,  w=ww, s=oo, d=Z)}{sfx}',  p=0, f=ff)  ;  self.dmpDataTableLine(u + 1)
        elif rAs and rBs:    self.dmpABs(rAs, rBs, o)
    ####################################################################################################################################################################################################
    def dmpABs(self, rAs, rBs, o):
        abcs = self.nimap[self.j][1]    ;   aa, bb = [], []
        for j, abc in enumerate(abcs):
            a, b, c = abc[0], abc[1], abc[2]
            r, ca, cb = abc2r(a, b, c)
            aa.append(a ** ca)     ;    bb.append(b ** cb)
        self.dmp_rABs(rAs, rBs, o) if o == 1 else self.dmp_rABs(aa, bb, o)

    def dmp_rABs(self, rAs, rBs, o):
        mm, nn, oo, ff  = (Y, Y, Y, 3) if self.csv else (W, Z, '|', -3)
        ckm  = self.nimap[self.j][0]   ;   n = ckm[0]['Note']   ;   pfx = Z   ;   u = 7
        if not o:
            _ = W*u
            for i, ck in enumerate(self.centKs):
                if ck in ckm and ckm[ck]['Count'] < 1:
                    rAs.insert(i, _)   ;   rBs.insert(i, _)
        ww = f'^{u}'   ;   sfx = W
        slog(f'{pfx}{fmtl(rAs, w=ww, s=oo, d=Z)}{sfx}{nn}{n:2}', p=0, f=ff)
        slog(f'{pfx}{fmtl(rBs, w=ww, s=oo, d=Z)}{sfx}{nn}{n:2}', p=0, f=ff)
    ####################################################################################################################################################################################################
    def dmpAsBs(self, rAs, rBs, u): # print both on same line
        abcs = self.nimap[self.j][1]    ;   As, Bs = [], []
        for j, abc in enumerate(abcs):
            a, b, c = abc[0], abc[1], abc[2]
            r, ca, cb = abc2r(a, b, c)
            As.append(a ** ca)     ;    Bs.append(b ** cb)
        self.dmp_rArBs(As, Bs, rAs, rBs, u=u)        

    def dmp_rArBs(self, rA1s, rB1s, rA2s, rB2s, u): # print both on same line
        ckm = self.nimap[self.j][0]   ;   ck = 0
        assert ck in ckm,         f'{self.j=} {ck=} {ckm=}'
        assert ckm[ck]['Count'],  f'{self.j=} {ck=} {ckm=}'
        n = ckm[ck]['Note']
        mm, nn, oo, ff  = (Y, Y, Y, 3) if self.csv else (W, Z, '|', -3)   ;   w1, w2 = f'^{u-1}', '^6'
        slog(f'{fmtl(rA1s, w=w1, s=mm, d=Z)}{nn}{n:{w1}}{nn}{fmtl(rA2s, w=w2, s=mm, d=Z)}', p=0, f=ff)
        slog(f'{fmtl(rB1s, w=w1, s=mm, d=Z)}{nn}{n:{w1}}{nn}{fmtl(rB2s, w=w2, s=mm, d=Z)}', p=0, f=ff)
    ####################################################################################################################################################################################################
    def getCkMapVal(self, ckmap, ck, a, ca, b, cb, f0, w0): # todo move to base class, but abc args and key are issues  # fixme sometimes asserts key ?
        f = ckmap[ck]['Freq']    ;   assert round(f, 10) == round(f0 * a**ca / b**cb, 10),    f'{ck=} {f=} {f0=} r={a**ca/b**cb} {f0*a**ca/b**cb=} {a=} {ca=} {b=} {cb=}'
        w = ckmap[ck]['Wavln']   ;   assert w == w0 / f,                f'{w=} {w0=} {f=}'
        n = ckmap[ck]['Note']
        i = ckmap[ck]['Index']
        k = ckmap[ck]['Count']
        c = ckmap[ck]['Cents']   ;   assert c == self.r2cents(a**ca/b**cb),  f'{c=} {self.r2cents(a**ca/b**cb)=}'
        d = ckmap[ck]['DCent']   ;   assert d == self.i2dCent(c),            f'{d=} {self.i2dCent(c)=}'    ;    d = round(d, 2)
        return f, w, n, c, d, k, i # todo assume callers do not want ckmap[ck]['Abcd'] value returned
    ####################################################################################################################################################################################################
    def fIvals(self, data, i): # todo move to base class
        mm, nn = (Y, Y) if self.csv else (W, Z)   ;   fd = []
        for j, d in enumerate(data): # j j*100 i Iv  c     k       d       e       c`   Iv  c     k       d       e       c`
            if   j==0:  fd.append(f'{d:x}')                  # j
            elif j==1:  fd.append(f'{d:4}')                  # j*100
            elif j==6:  fd.append(f'{d:7.3f}') if utl.ist(d, float) else fd.append(W*7) # d
            elif j==8:  fd.append(f'*{mm}{d:2}   ')          # c`
            elif j==12: fd.append(f'{d:7.3f}') if utl.ist(d, float) else fd.append(W*7) if i!=0 and i!=len(self.ck2ikm)-1 else fd.append(W*7) # d
            elif j==14: fd.append(f'*{mm}{d:2}')             # c`
            elif j in (5, 11): fd.append(f'@{mm}{d:4}{mm}:') # k k
            elif j in (7, 13): fd.append(f'={mm}{d:5.3f}')   # e e
            elif j in (2, 3, 4, 9, 10): fd.append(f'{d:2}')  # i Iv c Iv c
        return fd

    def dmpIvals(self, i, ks, cs, ds): # todo move to base class, but epsilon is an issue
        mm, nn, oo, ff = (Y, Y, Y, 3) if self.csv else (W, Z, '|', 1)   ;   m = -1
        eps, j     = self.epsilon(), math.floor(i/2)
        hdrA, hdrB1, hdrB2 = ['j', 'j*100', 'i'], ['Iv', f' c{mm} ', f'  k {mm} ', f'   d   {mm} ', f' e   {mm} ', f' c`  '], ['Iv', f' c{mm} ', f'  k {mm} ', f'   d   {mm} ', f' e   {mm} ', f' c`']
        hdrs       = hdrA   ;   hdrs.extend(hdrB1)   ;   hdrs.extend(hdrB2)
        if   i == 0:
            slog(f'{fmtl(hdrs, s=mm, d=Z)}', p=0, f=ff)
            data     = [j, j*100, i, self.ck2ikm[ks[i]], cs[i], ks[i], ds[i], eps, 0, 'd2', 0, 24, W*6, eps, cs[i]]
            fd       = self.fIvals(data, i)    ;    slog(f'{fmtl(fd, s=mm, d=Z)}', p=0, f=ff)
        elif not i % 2:
            u, v = (self.ck2ikm[ks[i+m]], self.ck2ikm[ks[i]])
            if  j < 6 and j % 2 or j > 6 and not j % 2:
                data = [j, j*100, i, u, cs[i+m], ks[i+m], ds[i+m], eps, cs[i], v, cs[i], ks[i], ds[i], eps, cs[i+m]]
                fd   = self.fIvals(data, i)    ;    slog(f'{fmtl(fd, s=mm, d=Z)}', p=0, f=ff)
            else:
                data = [j, j*100, i, v, cs[i], ks[i], ds[i], eps, cs[i+m], u, cs[i+m], ks[i+m], ds[i+m], eps, cs[i]]
                fd   = self.fIvals(data, i)    ;    slog(f'{fmtl(fd, s=mm, d=Z)}', p=0, f=ff)
        elif i == len(self.ck2ikm)-1:
            data     = [j+1, (j+1)*100, i+1, self.ck2ikm[ks[i]], cs[i], ks[i], ds[i], eps, 0, 'A7', 0, 1178, W*6, eps, cs[i]]
            fd       = self.fIvals(data, i)    ;    slog(f'{fmtl(fd, s=mm, d=Z)}', p=0, f=ff)
    ####################################################################################################################################################################################################
    def upd_ckmap(self, ck, ckm, n, f, abc, cent, idx): # f = f0 * pa/pb # n if k==ik else W*2 # todo move to base class, but abc arg and key is an issue
        assert ck in ckm.keys(),  f'{ck=} {ckm.keys()=}'
        ckm[ck]['Count'] = ckm[ck]['Count'] + 1 if 'Count' in ckm[ck] else 1
        ckm[ck]['Freq']  = f                      ;   ckm[ck]['Wavln'] = self.w0 / f
        ckm[ck]['Cents'] = cent                   ;   ckm[ck]['DCent'] = self.i2dCent(cent)
        ckm[ck]['Note']  = n                      ;   ckm[ck]['Abcd']  = abc
        ckm[ck]['Ival']  = self.ck2ikm[ck]        ;   ckm[ck]['Index'] = idx

########################################################################################################################################################################################################
########################################################################################################################################################################################################
#def fmtR0(a, ca, b, cb, w):   pa, pb =   float(a ** ca) ,   float(b ** cb)   ;  return f'{pa/pb:^{w}.{w-4}f}'
#def fmtR1(a, ca, b, cb, w):   pa, pb =   a ** ca        ,   b ** cb          ;  return f'{pa:>{w}}/{pb:<{w}}' # if ist(pa, int) else f'{pa:>{w}.{w-4}}/{pb:<{w}.{w-4}f}'
#def fmtRA(a, ca, w=Z):        pa     =   a ** ca                             ;  return f'{pa:^{w}}' if ist(pa, int) else f'{pa:^{w}.{w-4}f}'
#def fmtRB(b, cb, w=Z):        pb     =   b ** cb                             ;  return f'{pb:^{w}}' if ist(pb, int) else f'{pb:^{w}.{w-4}f}'
#def fmtR2(a, ca, b, cb, w):   qa, qb = f'{a}^{ca}'      , f'{b}^{cb}'        ;  return f'{qa:>{w}}/{qb:<{w}}'
#def fmtR3(a, ca, b, cb, w):   sa, sb = f'{a}{i2spr(ca)}', f'{b}{i2spr(cb)}'  ;  return f'{sa:>{w}}/{sb:<{w}}' 
#def fdvdr(a, ca, b, cb):      n = max(len(fmtRA(a, ca)), len(fmtRB(b, cb)))  ;  return n * '/'

#def NEW_addFmtRs(a, ca, b, cb, rs, u=4, w=9):
#    assert rs and ist(rs, list),  f'{rs=} {type(rs)=} {a=} {ca} {b} {cb} {u=} {w=}'   ;   lr = len(rs)
##    r0s, r2s, r3s = [], [], []   ;   r1s = [] if lr == 4 else None   ;   rAs = [] if lr == 5 else None   ;   rBs = [] if lr == 5 else None
#    r0s, r2s, r3s = rs[0], rs[-2], rs[-1] #         ;   r1s, rAs, rBs = None, None, None
#    r1s, rAs, rBs = None,  None,   None
#    if   lr == 4:       r1s      = rs[1]           ;   r1s.append(fmtR1(a, ca, b, cb, u))
#    elif lr == 5:       rAs, rBs = rs[1], rs[2]    ;   rAs.append(fmtRA(a, ca, w))    ;    rBs.append(fmtRB(b, cb, w)) # if ist(b**cb, int) else w3))
#    r0s.append(fmtR0(a, ca, b, cb, w))
#    r2s.append(fmtR2(a, ca, b, cb, u)) # if u >= 9 else None
#    r3s.append(fmtR3(a, ca, b, cb, u))
#    if   lr == 4:   return r0s, r1s,      r2s, r3s
#    elif lr == 5:   return r0s, rAs, rBs, r2s, r3s
    
#def OLD_addFmtRs(r0s, rAs, rBs, r2s, r3s, a, ca, b, cb, u=4, w=9):
#    r0s.append(fmtR0(a, ca, b, cb, w))
#    rAs.append(fmtRA(a, ca, w)) # if ist(a**ca, int) else w3))
#    rBs.append(fmtRB(b, cb, w)) # if ist(b**cb, int) else w3))
#    r2s.append(fmtR2(a, ca, b, cb, u)) # if u >= 9 else None
#    r3s.append(fmtR3(a, ca, b, cb, u))
########################################################################################################################################################################################################
