from tpkg       import utl
#from tpkg       import notes
#from tpkg.notes import Notes
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

def abc2r(a, b, c): # assumes a==2 or b==2, probably too specific, move to Pythagorean, rename?
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
    def __init__(self, n='C', rf=440, vs=V_SOUND, csv= 0):
        super().__init__(n=n, rf=rf, vs=vs, csv=csv)
        self.ivalKs = ['P1', 'm2', 'A1', 'd3', 'M2', 'm3', 'A2', 'd4', 'M3', 'P4', 'A3', 'd5', 'A4', 'd6', 'P5', 'm6', 'A5', 'd7', 'M6', 'm7', 'A6', 'd8', 'M7', 'P8']
        self.centKs = [   0,  90,  114,  180,  204,  294,  318,  384,  408,  498,  522,  588,  612,  678,  702,  792,  816,  882,  906,  996,  1020, 1086, 1110, 1200]
        self.set_ck2ikm() # todo this base class method initializes and or sets self.ck2ikm
        self.nimap  = {} # note index to list of abcs (freq ratios) and ckmap (cent key data map)
        self.ckmap  = self.resetCkmap() # freq ratio in cents to ival counts and data
    ####################################################################################################################################################################################################
    def dmpData(self, o, csv=0): # todo fixme
        self.csv = csv
        if   o == 0:
            slog(f'PRT 1 0-12 {self.n} {self.k} {self.csv=}', p=0)
            self.nimap = {}
            for i in range(0, 12):
                k = self.k + (i * 7) % NT
                self.dmpPyth(k)
        elif o == 1:
            slog(f'PRT 2A 7-12 {self.n} {self.k} {self.csv=}', p=0)
            self.nimap = {}
            for i in range(7, 12):
                k = self.k + (i * 7) % NT
                self.dmpPyth(k)
            slog(f'PRT 2B 0-7 {self.n} {self.k} {self.csv=}', p=0)
            for i in range(0, 7):
                k = self.k + (i * 7) % NT
                self.dmpPyth(k)

    def dmpData2(self, o, u=13, o2=0, dbg=0, csv=0): # todo fixme called by Tetractys to call dmpCkMap(), but need to populate ckmap first
        self.csv = csv
        if   o == 0:
            slog(f'PRT 1 0-12 {self.n} {self.k} {self.csv=}', p=0) if dbg else None
            self.nimap = {}
            for i in range(0, 12):
                k = self.k + (i * 7) % NT
                self.dmpPyth(k, u=u, o=o2, dbg=dbg)
        elif o == 1:
            slog(f'PRT 2A 7-12 {self.n} {self.k} {self.csv=}', p=0) if dbg else None
            self.nimap = {}
            for i in range(7, 12):
                k = self.k + (i * 7) % NT
                self.dmpPyth(k, u=u, o=o2, dbg=dbg)
            slog(f'PRT 2B 0-7 {self.n} {self.k} {self.csv=}', p=0) if dbg else None
            for i in range(0, 7):
                k = self.k + (i * 7) % NT
                self.dmpPyth(k, u=u, o=o2, dbg=dbg)
    ####################################################################################################################################################################################################
    @staticmethod
    def abcs(a=7, b=6):
        abc1 = stck5ths(a)
        abc2 = stck4ths(b)
        abc3 = [ stackI(3, 2, 0) ]   ;   abc3.extend(abc1)   ;   abc3.extend(abc2)   ;   abc3.append(stackI(2, 1, 1))
        abc4 = sorted(abc3, key= lambda z: abc2r(z[0], z[1], z[2])[0])
        return [ abc1, abc2, abc3, abc4 ] 

    def k2Abcs(self, k): # todo fixme
        f = self.abcs   ;   i = self.k
        return f(6, 5) if k==i else f(5, 6) if k==i+7 else f(4, 7) if k==i+2  else f(3, 8) if k==i+9 else f(2, 9)  if k==i+4 else f(1, 10) if k==i+11 else f(0, 11) if k==i+6 \
                               else f(7, 4) if k==i+5 else f(8, 3) if k==i+10 else f(9, 2) if k==i+3 else f(10, 1) if k==i+8 else f(11, 0) if k==i+1  else f(12, 0)
    ####################################################################################################################################################################################################
    def fmtNPair(self, k, i, dbg=0): # todo fixme
        n0, _   = self.i2nPair(self.k, s=1)
        n1, n2  = self.i2nPair(k + i, b=0 if i in (4, 6, 11) or k in (self.k + 4, self.k + 6, self.k + 11) else 1, s=1, e=1)   ;   slog(f'{self.k=} {n0=} {n1=} {n2=}') if dbg else None
        if i and i != NT:
            if          n1 == self.COFM[n0][1]:   return n2
            elif n2 and n2 != self.COFM[n0][1]:   n1 += '/' + n2
        slog(f'return {n1=}') if dbg else None
        return n1
    ####################################################################################################################################################################################################
    def dmpPyth(self, k, u=9, o=0, dbg=1):
        x, y = 13, 6     ;   z = x-2   ;   _ = x*W   ;   f0 = self.FREFS[k]   ;   cki = -1
        ww, mm, nn, oo, ff = (f'^{x}', Y, Y, Y, 3) if self.csv else (f'^{x}', W, Z, '|', 1)            ;   w3 = [W, W, W]
        if dbg:
            slog(f'BGN Pythagorean ({k=} {self.rf=} {self.VS=} {self.csv=})', p=0, f=ff)
            ii  = [ f'{i}' for i in range(2 * NT) ]     ;   slog(f'{mm}  k  {mm}{nn} {nn}{fmtl(ii, w=ww, s=mm, d=Z)}', p=0, f=ff)
            self.dmpDataTableLine(x + 1)
        ii, ns, vs, fs, ws = [], [], [], [], []   ;   cs, ds = [], []   ;   r0s, rAs, rBs, r1s, r2s, r3s = [], [], [], [], [], []   ;   abcMap = []
        tmp = self.k2Abcs(k)  ;   abc0 = list(tmp[3])   ;   abc1, abc2, abc3, abc4 = fabc(tmp[0]), fabc(tmp[1]), fabc(tmp[2]), fabc(tmp[3])
        abc1.insert(0, fmtl(w3, w=2, d=Z))              ;   abc2.insert(0, fmtl(w3, w=2, d=Z)) # insert blanks for alignment in log/csv files
        ckm = self.resetCkmap()
        for i, e in enumerate(abc0):
            a, b, c = e[0], e[1], e[2]    ;    r, ca, cb = abc2r(a, b, c)    ;   abc = [ a, ca, b, cb ]   ;    f = r * f0    ;   w = self.w0 / f
            n  = self.fmtNPair(k, i)      ;    c = self.r2cents(r)   ;   d = self.k2dCent(c)   ;   rc = round(c)
            assert rc in self.ck2ikm,  f'{rc=} not in ck2ikm {k=} {i=} {self.k=} {n=} {c=} {r=} {abc=}'   ;   v = self.ck2ikm[rc]   ;   cki += 1
            while self.centKs[cki] < rc:
                r0s.append(_)  ;  r1s.append(_)  ;  r2s.append(_)  ;  r3s.append(_)   ;   rAs.append(_)   ;   rBs.append(_)
                ii.append(_)   ;  cs.append(_)   ;  ds.append(_)   ;  fs.append(_)    ;    ws.append(_)   ;   ns.append(_)   ;    vs.append(_)
                cki += 1    ;  j = len(ii)-1   ;  abc1.insert(j, fmtl(w3, w=2, d=Z))  ;  abc2.insert(j, fmtl(w3, w=2, d=Z))  ;  abc3.insert(j, fmtl(w3, w=2, d=Z))  ;  abc4.insert(j, fmtl(w3, w=2, d=Z))
            ii.append(i)    ;  fs.append(fmtf(f, z))   ;   cs.append(fmtf(c, y-1))   ;  abcMap.append(abc)
            ns.append(n)    ;  ws.append(fmtf(w, z))   ;   ds.append(fmtg(d, y-1))   ;      vs.append(v)
            r0s, rAs, rBs, r1s, r2s, r3s = self.addFmtRs(a, ca, b, cb, rs=[r0s, rAs, rBs, r1s, r2s, r3s], u=y, w=x,     i=i, j=rc)
            if not dbg:   self.upd_ckmap(rc, ckm, n, f, abc, c, i)
        self.nimap[k] = [tmp[2], abcMap, ckm]          ;   sfx = f'{nn}]'   ;   sfxc = f'{nn}]{mm}cents'   ;   sfxf = f'{nn}]{mm}Hz'   ;   sfxw = f'{nn}]{mm}cm'
        while len(abc1) < len(abc3): abc1.append(fmtl(w3, w=2, d=Z)) # append blanks for alignment in log/csv files
        while len(abc2) < len(abc3): abc2.append(fmtl(w3, w=2, d=Z)) # append blanks for alignment in log/csv files
        if dbg:
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
            self.dmpDataTableLine(x + 1)
        self.dmpMaps(k, u, o=o, dbg=dbg)
        slog(f'END Pythagorean ({k=} {self.rf=} {self.VS=} {self.csv=})', p=0, f=ff) if dbg else None
    ####################################################################################################################################################################################################
    def epsilon(self, dbg=0):
        ccents = self.comma()
        ecents = ccents / NT
        if dbg:  slog(f'Epsilon = Comma / 12 = {ccents:10.5f} / 12 = {ecents:10.5f} cents')
        return ecents
        
    def comma(self, dbg=0): # 3**12 / 2**19 = 3¹²/2¹⁹ = 531441 / 524288 = 1.0136432647705078, log2(1.0136432647705078) = 0.019550008653874178, 1200 * log2() = 23.460010384649014
        n, i, iv  = 12, -1, '5'
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
        ecents    = ccents / 12
        if dbg:   slog(f'Epsilon = Comma / 12 = {ccents:10.5f} / 12 = {ecents:10.5f} cents')
        return ccents
    ####################################################################################################################################################################################################
    def fIvals(self, data, i):
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

    def dmpIvals(self, i, ks, cs, ds): # only called by dmpCkMap()
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
    def dmpMaps(self, k, u, o, dbg=1):
        if dbg:
            self.dmpNiMap(  1, k, x=13, upd=1, dbg=dbg)
            self.dmpNiMap(  2, k, x=13, upd=1, dbg=dbg)
            self.dmpNiMap(  3, k, x=13, upd=1, dbg=dbg)
            self.dmpNiMap(  4, k, x=13, upd=1, dbg=dbg)
            self.dmpNiMap(  5, k, x=13, upd=1, dbg=dbg)
            self.dmpCks2Iks(      x=13       )
            self.dmpCkMap(k,      u=u        )
            self.dmpNiMap(  1, k, x=9,  upd=0, dbg=dbg)
            self.dmpNiMap(  2, k, x=9,  upd=0, dbg=dbg)
            self.dmpNiMap(  3, k, x=9,  upd=0, dbg=dbg)
            self.dmpNiMap(  4, k, x=9,  upd=0, dbg=dbg)
            self.dmpNiMap(  5, k, x=9,  upd=0, dbg=dbg)
            self.dmpCks2Iks(      x=9        )
            self.checkIvals(                 )
            self.checkIvals2(                )
        else:
            self.dmpNiMap(  5, k, x=13, upd=1, dbg=dbg)
            self.dmpCkMap(k,      u=u,  o=o,   dbg=dbg)
        self.ckmap = self.resetCkmap() # todo call this once @ end of dmpMaps()
    ####################################################################################################################################################################################################
    def resetCkmap(self): # todo call this once @ end of dmpMaps()
        ckm = {}
        for ck in self.centKs:
            ckm[ck] = {'Count': 0}
        return ckm

    def dmpCks2Iks(self, x=13):
        if not self.csv:
            if   x== 9: slog(f'{7*W}  {fmtm(self.ck2ikm, w=4, wv=2, s=3*W, d=Z)}', p=0)
            elif x==13: slog(f'{9*W}  {fmtm(self.ck2ikm, w=4, wv=2, s=7*W, d=Z)}', p=0)
            else:       slog(f'{5*W}  {fmtm(self.ck2ikm, w=3, wv=2, s="|", d=Z)}', p=0)
            
    def upd_ckmap(self, ck, ckm, n, f, abc, cent, idx): # f = f0 * pa/pb # n if k==ik else W*2
        assert ck in ckm.keys(),  f'{ck=} {ckm.keys()=}'
        ckm[ck]['Count'] = ckm[ck]['Count'] + 1 if 'Count' in ckm[ck] else 1    ;    ckm[ck]['Abc']   = abc
        ckm[ck]['Freq']  = f                      ;   ckm[ck]['Wavln'] = self.w0 / f
        ckm[ck]['Cents'] = cent                   ;   ckm[ck]['DCent'] = self.k2dCent(cent)
        ckm[ck]['Note']  = n
        ckm[ck]['Ival']  = self.ck2ikm[ck]        ;   ckm[ck]['Idx']   = idx
    ####################################################################################################################################################################################################
    def dmpNiMap(self, ni, ik, x, upd=0, dbg=1): # x=13 or x=9
        ww, mm, nn, oo, ff = (f'^{x}', Y, Y, Y, 3) if self.csv else (f'^{x}', W, Z, '|', 1)   ;   pfx = ''   ;   sfx = f'{nn}]'  ;  yy = 6 if x==13 else 4
        f0  = self.FREFS[ik] #  ;   ckmap = {}
        ii = [ f'{i}' for i in range(2 * NT) ]
        if dbg: slog(f'{mm}  k  {mm}{nn} {nn}{fmtl(ii, w=ww, s=mm, d=Z)}', p=0, f=ff) if ni == 1 else None
        if dbg: self.dmpDataTableLine(x + 1) if ni == 1 else None
        for i, (k, v) in enumerate(self.nimap.items()):
            rat0, rat2, rat3, cents = [], [], [], []    ;   cki = -1
            rat1 = [] if x == 13 else None   ;   ratA = [] if x == 9 else None   ;   ratB = [] if x == 9 else None
            for j, e in enumerate(v[1]):
                a, ca, b, cb = e        ;      pa, pb = a ** ca, b ** cb
                n    = self.fmtNPair(k, j)
                pd   = [f'{i:x}', f'{k:2}', f'{n:2}']   ;   pfx = mm.join(pd)    ;   pfx += f'{nn}[{nn}'
                cent = self.r2cents(pa/pb)   ;   rc = round(cent)   ;   centf = f'{cent:{ww}.0f}'   ;   cki += 1   ;   cents.append(centf)
                while self.centKs[cki] < rc:
                    blnk = W*x          ;   cki += 1            ;   cents.append(f'{blnk:{ww}}')
                    rat0.append(blnk)   ;   rat2.append(blnk)   ;   rat3.append(blnk)
                    rat1.append(blnk) if x == 13 else None      ;   ratA.append(blnk) if x == 9 else None   ;   ratB.append(blnk) if x == 9 else None
                if   x == 9:    self.addFmtRs(a, ca, b, cb, rs=[rat0, ratA, ratB, rat2, rat3], u=yy, w=x,     i=i, j=j)
                elif x == 13:   self.addFmtRs(a, ca, b, cb, rs=[rat0,       rat1, rat2, rat3], u=yy, w=x,     i=i, j=j)
                if dbg and upd and ni == 5:
                    self.upd_ckmap(rc, self.ckmap, n if k==ik else W*2, f0*pa/pb, e, cent, j)
            if dbg:
                if   ni == 1:             slog(f'{pfx}{Z.join(fmtl(rat0,  w=ww, s=oo, d=Z))}{sfx}', p=0, f=ff)
                elif ni == 2 and x == 9:  slog(f'{pfx}{Z.join(fmtl(ratA,  w=ww, s=oo, d=Z))}{sfx}', p=0, f=ff)  ;  slog(f'{pfx}{Z.join(fmtl(ratB,  w=ww, s=oo, d=Z))}{sfx}', p=0, f=ff)
                elif ni == 2 and x == 13: slog(f'{pfx}{Z.join(fmtl(rat1,  w=ww, s=oo, d=Z))}{sfx}', p=0, f=ff)
                elif ni == 3:             slog(f'{pfx}{Z.join(fmtl(rat2,  w=ww, s=oo, d=Z))}{sfx}', p=0, f=ff)
                elif ni == 4:             slog(f'{pfx}{Z.join(fmtl(rat3,  w=ww, s=oo, d=Z))}{sfx}', p=0, f=ff)
                elif ni == 5:             slog(f'{pfx}{Z.join(fmtl(cents, w=ww, s=oo, d=Z))}{sfx}', p=0, f=ff)
        if dbg: self.dmpDataTableLine(x + 1)
        if dbg: slog(f'{mm}  k  {mm}{nn} {nn}{fmtl(ii, w=ww, s=mm, d=Z)}', p=0, f=ff) if ni == 5 else None
    ####################################################################################################################################################################################################
    def dmpCkMap(self, k, u=9, o=0, dbg=1):
        y = 4   ;   sk, v = 0, Z    ;   f0 = self.FREFS[k]    ;   blnk = u*W if dbg else 6*W
        mm, nn, oo, ff  = (Y, Y, Y, 3) if self.csv else (W, Z, '|', 1)   ;   ww, w1  = f'^{u}', f'^{u}.1f'
        ns, fs, ws, vs  = [], [], [], []  ;  cs, ds, qs, ks = [], [], [], []  ;   r0s, rAs, rBs, r2s, r3s = [], [], [], [], []  ;  cksf, cksi = [], []
        if dbg:  ckmap = self.ckmap
        else:    ckmap = self.nimap[k][2]
        for i, ck in enumerate(self.centKs):
            ival = self.ck2ikm[ck]    ;    vs.append(ival)
            assert ckmap and ck in ckmap,  f'{k=} {i=} {ival=} {ck=} {ckmap=} {self.ckmap=} {self.nimap[k][2]=} {dbg=}'
            if ckmap[ck]['Count'] > 0:
                assert ival == ckmap[ck]['Ival'],  f'{ival=} {ck=} {ckmap[ck]["Ival"]=}'
                a, ca, b, cb = ckmap[ck]['Abc']   ;    q = self.fdvdr(a, ca, b, cb)
                r0s, rAs, rBs, r2s, r3s = self.addFmtRs(a, ca, b, cb, rs=[r0s, rAs, rBs, r2s, r3s], u=y, w=u if dbg else 6,     i=i, j=ck)
                f, w, n, c, d, k2, i2   = self.getCkMapVal(ckmap, ck, a, ca, b, cb, f0, self.w0)   ;   sk += k2
                cksf.append(f'{c:{w1}}')          ;    cksi.append(int(round(c)))
                fs.append(f'{fmtf(f, u-2)}')      ;      ws.append(f'{fmtf(w, u-2)}')
            else:
                r0s.append(blnk)    ;    rAs.append(blnk)     ;  rBs.append(blnk)  ;   r2s.append(blnk)  ;  r3s.append(blnk)   ;   k2, q = 0, Z
                n, c, d, f, w = blnk, blnk, blnk, blnk, blnk  ;  cksi.append(ck)   ;  cksf.append(blnk)  ;  fs.append(f)       ;   ws.append(w)
            if dbg:   ns.append(n)  ;  ks.append(k2)  ;  cs.append(c)    ;  ds.append(d)      ;   qs.append(q)
            if dbg:   self.dmpIvals(i, cksi, ks, ds)
        if dbg:
            ii = [ f'{i}' for i in range(2 * NT) ]
            slog(f'{mm}  k  {mm}{nn} {nn}{fmtl(ii,          w=ww, s=mm, d=Z)}',      p=0, f=ff)
            self.dmpDataTableLine(u + 1)
            slog(f'{mm}Centk{mm}{nn}[{nn}{fmtl(self.centKs, w=ww, s=oo, d=Z)}{nn}]', p=0, f=ff)
            slog(f'{mm}Itval{mm}{nn}[{nn}{fmtl(vs,          w=ww, s=oo, d=Z)}{nn}]', p=0, f=ff)
            slog(f'{mm}Note {mm}{nn}[{nn}{fmtl(ns,          w=ww, s=oo, d=Z)}{nn}]', p=0, f=ff)
            slog(f'{mm}Cents{mm}{nn}[{nn}{fmtl(cksf,        w=ww, s=oo, d=Z)}{nn}]', p=0, f=ff)
            slog(f'{mm}DCent{mm}{nn}[{nn}{fmtl(ds,          w=ww, s=oo, d=Z)}{nn}]', p=0, f=ff)
            slog(f'{mm}Rati0{mm}{nn}[{nn}{fmtl(r0s,         w=ww, s=oo, d=Z)}{nn}]', p=0, f=ff)
            slog(f'{mm}RatiA{mm}{nn}[{nn}{fmtl(rAs,         w=ww, s=oo, d=Z)}{nn}]', p=0, f=ff)
            slog(f'{mm} A/B {mm}{nn}[{nn}{fmtl(qs,          w=ww, s=oo, d=Z)}{nn}]', p=0, f=ff)
            slog(f'{mm}RatiB{mm}{nn}[{nn}{fmtl(rBs,         w=ww, s=oo, d=Z)}{nn}]', p=0, f=ff)
            slog(f'{mm}Rati2{mm}{nn}[{nn}{fmtl(r2s,         w=ww, s=oo, d=Z)}{nn}]', p=0, f=ff) if u >= 9 else None
            slog(f'{mm}Rati3{mm}{nn}[{nn}{fmtl(r3s,         w=ww, s=oo, d=Z)}{nn}]', p=0, f=ff)
            slog(f'{mm}Freq {mm}{nn}[{nn}{fmtl(fs,          w=ww, s=oo, d=Z)}{nn}]', p=0, f=ff)
            slog(f'{mm}Wavln{mm}{nn}[{nn}{fmtl(ws,          w=ww, s=oo, d=Z)}{nn}]', p=0, f=ff)
            slog(f'{mm}Count{mm}{nn}[{nn}{fmtl(ks,          w=ww, s=oo, d=Z)}{nn}]', p=0, f=ff)
            self.dmpDataTableLine(u + 1)
        elif rAs and rBs:    self.dmpABs(k, rAs, rBs, u) if o == 0 else self.dmpABs(k, rAs, rBs, 6)
    ####################################################################################################################################################################################################
    def dmpABs(self, k, rAs, rBs, u):
        abcs = self.nimap[k][0]    ;   As, Bs = [], []
        for j, abc in enumerate(abcs):
            a, b, c = abc[0], abc[1], abc[2]
            r, ca, cb = abc2r(a, b, c)
            As.append(a ** ca)     ;    Bs.append(b ** cb)
        self.dmp_rABs(k, rAs, rBs, u=u) if u == 6 else self.dmp_rABs(k, As, Bs, u=u)

    def dmp_rABs(self, k, rAs, rBs, u):
        mm, nn, oo, ff  = (Y, Y, Y, 3) if self.csv else (W, Z, '|', -3)
        w1 = f'^{u}'   ;   w2 = f'5'
        ckm = self.nimap[k][2]   ;   ck = 0
        assert ck in ckm,         f'{k=} {ck=} {ckm=}'
        assert ckm[ck]['Count'],  f'{k=} {ck=} {ckm=}'
        n = ckm[ck]['Note']   ;   pfx = 7*W if u==6 else Z
        slog(f'{pfx}{fmtl(rAs, w=w1, s=oo, d=Z)}{pfx}{nn}{n:{w2}}{nn}', p=0, f=ff)
        slog(f'{pfx}{fmtl(rBs, w=w1, s=oo, d=Z)}{pfx}{nn}{n:{w2}}{nn}', p=0, f=ff)
    ####################################################################################################################################################################################################
    def dmpAsBs(self, k, rAs, rBs, u): # print both on same line
        abcs = self.nimap[k][0]    ;   As, Bs = [], []
        for j, abc in enumerate(abcs):
            a, b, c = abc[0], abc[1], abc[2]
            r, ca, cb = abc2r(a, b, c)
            As.append(a ** ca)     ;    Bs.append(b ** cb)
        self.dmp_rArBs(k, As, Bs, rAs, rBs, u=u)        

    def dmp_rArBs(self, k, rA1s, rB1s, rA2s, rB2s, u): # print both on same line
        ckm = self.nimap[k][2]   ;   ck = 0
        assert ck in ckm,         f'{k=} {ck=} {ckm=}'
        assert ckm[ck]['Count'],  f'{k=} {ck=} {ckm=}'
        n = ckm[ck]['Note']
        mm, nn, oo, ff  = (Y, Y, Y, 3) if self.csv else (W, Z, '|', -3)   ;   w1, w2 = f'^{u-1}', '^6'
        slog(f'{fmtl(rA1s, w=w1, s=mm, d=Z)}{nn}{n:{w1}}{nn}{fmtl(rA2s, w=w2, s=mm, d=Z)}', p=0, f=ff)
        slog(f'{fmtl(rB1s, w=w1, s=mm, d=Z)}{nn}{n:{w1}}{nn}{fmtl(rB2s, w=w2, s=mm, d=Z)}', p=0, f=ff)
    ####################################################################################################################################################################################################
    def getCkMapVal(self, ckmap, ck, a, ca, b, cb, f0, w0): # fixme sometimes ?
        f = ckmap[ck]['Freq']    ;   assert round(f, 9) == round(f0 * a**ca / b**cb, 9),    f'{ck=} {f=} {f0=} r={a**ca/b**cb} {f0*a**ca/b**cb=} {a=} {ca=} {b=} {cb=}'
        w = ckmap[ck]['Wavln']   ;   assert w == w0 / f,                f'{w=} {w0=} {f=}'
        n = ckmap[ck]['Note']
        i = ckmap[ck]['Idx']
        k = ckmap[ck]['Count']
        c = ckmap[ck]['Cents']   ;   assert c == self.r2cents(a**ca/b**cb),  f'{c=} {self.r2cents(a**ca/b**cb)=}'
        d = ckmap[ck]['DCent']   ;   assert d == self.k2dCent(c),            f'{d=} {self.k2dCent(c)=}'    ;    d = round(d, 2)
        return f, w, n, c, d, k, i

    def checkIvals(self):
        mm, nn, oo, ff  = (Y, Y, Y, 3) if self.csv else (W, Z, '|', 1)
        slog(f'BGN checkIvals() {self.csv=}', p=0, f=ff)
        msgs, ws = [], [7, 8, 7, 7, 7, 5, 4, 4, 3]
        keys = list(list(self.ckmap.values())[0].keys())
        slog(f'Jdx{mm} {nn}{nn}CK{mm}  {mm}{fmtl(keys, w=ws, s=mm, d=Z)}', p=0, f=ff)
        for i, (ck, cv) in enumerate(self.ckmap.items()):
            msg = f'{i:2}{nn}[{mm}{ck:4}{nn}:{mm}[{mm}'
            for k, v in cv.items():
                msg += f'{fmtf(v, 7)}{mm}' if k in ("Cents", "Freq", "Wavln") else f'{fmtg(v, 6)}{mm}' if k=="DCent" else f'{fmtl(v, s=W):11}{mm}' if k=="Abc" else f'{v:2}{mm}' if k in ("Count", "Idx") else f'{v:5}{mm}' if k=="Note" else f'{v:3}{mm}' if k=="Ival" else f'{v:6}{mm}'
            msg += f']{nn}]'   ;   msgs.append(msg)
        msgs = '\n'.join(msgs)
        slog(f'{msgs}', p=0, f=ff)
        slog(f'END checkIvals() {self.csv=}', p=0, f=ff)
    ########################################################################################################################################################################################################
    def checkIvals2(self):
        self.dmpCkmap()
        keys = list(self.ckmap.keys())
        for k in keys:
            if self.ckmap[k]["Count"] > 0: self.checkIvals2A(k)

    def checkIvals2A(self, key):
        mm, nn, oo, ff  = (Y, Y, Y, 3) if self.csv else (W, Z, '|', 1)  ;  x = 13  ;   ww = f'^{x}.9f'  ;  vv = f'7.3f'  ;  uu = f'^{x}'
        rs = []   ;   blnk = x*W   ;   fk = 'Freq'
        fv = self.ckmap[key][fk]
        for i, (ck, cv) in enumerate(self.ckmap.items()):
            for k2, v2 in cv.items():
                if k2 == fk:
                    v  = cv[fk] / fv
                    rs.append(f'{v:{ww}}')
                    break
            else:
                rs.append(blnk)
            if rs and i==len(self.ckmap)-1:   slog(f'{fv:{vv}}{fmtl(rs, w=uu, s=oo)}', p=0, f=ff)
    ########################################################################################################################################################################################################
    def dmpCkmap(self):
        ks = []   ;   x = 13   ;   w = f'^{x}'   ;   o = '|'
        for k, v in self.ckmap.items():
            ks.append(f'{k:3} {v["Count"]}')
        slog(f'{7*W}{fmtl(ks, w=w, s=o)}', p=0)

    def dmpDataTableLine(self, w=10, n=24):
        c = '-'   ;   nn, mm, t = (Y, Y, Y) if self.csv else (Z, W, '|')
        col = f'{c * (w-1)}'
        cols = t.join([ col for _ in range(n) ])
        slog(f'{mm}     {mm}{nn} {nn}{cols}', p=0, f=3 if self.csv else 1)

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
'''
                                                                                                   1                                                                                                     [1] 1
                                                                                              2         3                                                                                                [1 2 3] 3
                                                                                         4         6         9                                                                                           [1 2 3 4 6 9] 6
                                                                                    8        12        18        27                                                                                      [1 2 3 4 6 8 9 12 18 27] 10
                                                                              16        24        36        54        81                                                                                 [1 2 3 4 6 8 9 12 16 18 24 27 36 54 81] 15
                                                                         32        48        72        108       162       243                                                                           [1 2 3 4 6 8 9 12 16 18 24 27 32 36 48 54 72 81 108 162 243] 21
                                                                    64        96        144       216       324       486       729                                                                      [1 2 3 4 6 8 9 12 16 18 24 27 32 36 48 54 64 72 81 96 108 144 162 216 243 324 486 729] 28
                                                               128       192       288       432       648       972      1458      2187                                                                 [1 2 3 4 6 8 9 12 16 18 24 27 32 36 48 54 64 72 81 96 108 128 144 162 192 216 243 288 324 432 486 648 729 972 1458 2187] 36
                                                          256       384       576       864      1296      1944      2916      4374      6561                                                            [1 2 3 4 6 8 9 12 16 18 24 27 32 36 48 54 64 72 81 96 108 128 144 162 192 216 243 256 288 324 384 432 486 576 648 729 864 972 1296 1458 1944 2187 2916 4374 6561] 45
                                                     512       768      1152      1728      2592      3888      5832      8748      13122     19683                                                      [1 2 3 4 6 8 9 12 16 18 24 27 32 36 48 54 64 72 81 96 108 128 144 162 192 216 243 256 288 324 384 432 486 512 576 648 729 768 864 972 1152 1296 1458 1728 1944 2187 2592 2916 3888 4374 5832 6561 8748 13122 19683] 55
                                               1024      1536      2304      3456      5184      7776      11664     17496     26244     39366     59049                                                 [1 2 3 4 6 8 9 12 16 18 24 27 32 36 48 54 64 72 81 96 108 128 144 162 192 216 243 256 288 324 384 432 486 512 576 648 729 768 864 972 1024 1152 1296 1458 1536 1728 1944 2187 2304 2592 2916 3456 3888 4374 5184 5832 6561 7776 8748 11664 13122 17496 19683 26244 39366 59049] 66
                                          2048      3072      4608      6912      10368     15552     23328     34992     52488     78732    118098    177147                                            [1 2 3 4 6 8 9 12 16 18 24 27 32 36 48 54 64 72 81 96 108 128 144 162 192 216 243 256 288 324 384 432 486 512 576 648 729 768 864 972 1024 1152 1296 1458 1536 1728 1944 2048 2187 2304 2592 2916 3072 3456 3888 4374 4608 5184 5832 6561 6912 7776 8748 10368 11664 13122 15552 17496 19683 23328 26244 34992 39366 52488 59049 78732 118098 177147] 78
                                     4096      6144      9216      13824     20736     31104     46656     69984    104976    157464    236196    354294    531441                                       [1 2 3 4 6 8 9 12 16 18 24 27 32 36 48 54 64 72 81 96 108 128 144 162 192 216 243 256 288 324 384 432 486 512 576 648 729 768 864 972 1024 1152 1296 1458 1536 1728 1944 2048 2187 2304 2592 2916 3072 3456 3888 4096 4374 4608 5184 5832 6144 6561 6912 7776 8748 9216 10368 11664 13122 13824 15552 17496 19683 20736 23328 26244 31104 34992 39366 46656 52488 59049 69984 78732 104976 118098 157464 177147 236196 354294 531441] 91
                                8192      12288     18432     27648     41472     62208     93312    139968    209952    314928    472392    708588    1062882   1594323                                 [1 2 3 4 6 8 9 12 16 18 24 27 32 36 48 54 64 72 81 96 108 128 144 162 192 216 243 256 288 324 384 432 486 512 576 648 729 768 864 972 1024 1152 1296 1458 1536 1728 1944 2048 2187 2304 2592 2916 3072 3456 3888 4096 4374 4608 5184 5832 6144 6561 6912 7776 8192 8748 9216 10368 11664 12288 13122 13824 15552 17496 18432 19683 20736 23328 26244 27648 31104 34992 39366 41472 46656 52488 59049 62208 69984 78732 93312 104976 118098 139968 157464 177147 209952 236196 314928 354294 472392 531441 708588 1062882 1594323] 105
                           16384     24576     36864     55296     82944    124416    186624    279936    419904    629856    944784    1417176   2125764   3188646   4782969                            [1 2 3 4 6 8 9 12 16 18 24 27 32 36 48 54 64 72 81 96 108 128 144 162 192 216 243 256 288 324 384 432 486 512 576 648 729 768 864 972 1024 1152 1296 1458 1536 1728 1944 2048 2187 2304 2592 2916 3072 3456 3888 4096 4374 4608 5184 5832 6144 6561 6912 7776 8192 8748 9216 10368 11664 12288 13122 13824 15552 16384 17496 18432 19683 20736 23328 24576 26244 27648 31104 34992 36864 39366 41472 46656 52488 55296 59049 62208 69984 78732 82944 93312 104976 118098 124416 139968 157464 177147 186624 209952 236196 279936 314928 354294 419904 472392 531441 629856 708588 944784 1062882 1417176 1594323 2125764 3188646 4782969] 120
                      32768     49152     73728    110592    165888    248832    373248    559872    839808    1259712   1889568   2834352   4251528   6377292   9565938  14348907                       [1 2 3 4 6 8 9 12 16 18 24 27 32 36 48 54 64 72 81 96 108 128 144 162 192 216 243 256 288 324 384 432 486 512 576 648 729 768 864 972 1024 1152 1296 1458 1536 1728 1944 2048 2187 2304 2592 2916 3072 3456 3888 4096 4374 4608 5184 5832 6144 6561 6912 7776 8192 8748 9216 10368 11664 12288 13122 13824 15552 16384 17496 18432 19683 20736 23328 24576 26244 27648 31104 32768 34992 36864 39366 41472 46656 49152 52488 55296 59049 62208 69984 73728 78732 82944 93312 104976 110592 118098 124416 139968 157464 165888 177147 186624 209952 236196 248832 279936 314928 354294 373248 419904 472392 531441 559872 629856 708588 839808 944784 1062882 1259712 1417176 1594323 1889568 2125764 2834352 3188646 4251528 4782969 6377292 9565938 14348907] 136
                 65536     98304    147456    221184    331776    497664    746496    1119744   1679616   2519424   3779136   5668704   8503056  12754584  19131876  28697814  43046721                  [1 2 3 4 6 8 9 12 16 18 24 27 32 36 48 54 64 72 81 96 108 128 144 162 192 216 243 256 288 324 384 432 486 512 576 648 729 768 864 972 1024 1152 1296 1458 1536 1728 1944 2048 2187 2304 2592 2916 3072 3456 3888 4096 4374 4608 5184 5832 6144 6561 6912 7776 8192 8748 9216 10368 11664 12288 13122 13824 15552 16384 17496 18432 19683 20736 23328 24576 26244 27648 31104 32768 34992 36864 39366 41472 46656 49152 52488 55296 59049 62208 65536 69984 73728 78732 82944 93312 98304 104976 110592 118098 124416 139968 147456 157464 165888 177147 186624 209952 221184 236196 248832 279936 314928 331776 354294 373248 419904 472392 497664 531441 559872 629856 708588 746496 839808 944784 1062882 1119744 1259712 1417176 1594323 1679616 1889568 2125764 2519424 2834352 3188646 3779136 4251528 4782969 5668704 6377292 8503056 9565938 12754584 14348907 19131876 28697814 43046721] 153
           131072    196608    294912    442368    663552    995328    1492992   2239488   3359232   5038848   7558272  11337408  17006112  25509168  38263752  57395628  86093442  129140163            [1 2 3 4 6 8 9 12 16 18 24 27 32 36 48 54 64 72 81 96 108 128 144 162 192 216 243 256 288 324 384 432 486 512 576 648 729 768 864 972 1024 1152 1296 1458 1536 1728 1944 2048 2187 2304 2592 2916 3072 3456 3888 4096 4374 4608 5184 5832 6144 6561 6912 7776 8192 8748 9216 10368 11664 12288 13122 13824 15552 16384 17496 18432 19683 20736 23328 24576 26244 27648 31104 32768 34992 36864 39366 41472 46656 49152 52488 55296 59049 62208 65536 69984 73728 78732 82944 93312 98304 104976 110592 118098 124416 131072 139968 147456 157464 165888 177147 186624 196608 209952 221184 236196 248832 279936 294912 314928 331776 354294 373248 419904 442368 472392 497664 531441 559872 629856 663552 708588 746496 839808 944784 995328 1062882 1119744 1259712 1417176 1492992 1594323 1679616 1889568 2125764 2239488 2519424 2834352 3188646 3359232 3779136 4251528 4782969 5038848 5668704 6377292 7558272 8503056 9565938 11337408 12754584 14348907 17006112 19131876 25509168 28697814 38263752 43046721 57395628 86093442 129140163] 171
      262144    393216    589824    884736    1327104   1990656   2985984   4478976   6718464  10077696  15116544  22674816  34012224  51018336  76527504  114791256 172186884 258280326 387420489       [1 2 3 4 6 8 9 12 16 18 24 27 32 36 48 54 64 72 81 96 108 128 144 162 192 216 243 256 288 324 384 432 486 512 576 648 729 768 864 972 1024 1152 1296 1458 1536 1728 1944 2048 2187 2304 2592 2916 3072 3456 3888 4096 4374 4608 5184 5832 6144 6561 6912 7776 8192 8748 9216 10368 11664 12288 13122 13824 15552 16384 17496 18432 19683 20736 23328 24576 26244 27648 31104 32768 34992 36864 39366 41472 46656 49152 52488 55296 59049 62208 65536 69984 73728 78732 82944 93312 98304 104976 110592 118098 124416 131072 139968 147456 157464 165888 177147 186624 196608 209952 221184 236196 248832 262144 279936 294912 314928 331776 354294 373248 393216 419904 442368 472392 497664 531441 559872 589824 629856 663552 708588 746496 839808 884736 944784 995328 1062882 1119744 1259712 1327104 1417176 1492992 1594323 1679616 1889568 1990656 2125764 2239488 2519424 2834352 2985984 3188646 3359232 3779136 4251528 4478976 4782969 5038848 5668704 6377292 6718464 7558272 8503056 9565938 10077696 11337408 12754584 14348907 15116544 17006112 19131876 22674816 25509168 28697814 34012224 38263752 43046721 51018336 57395628 76527504 86093442 114791256 129140163 172186884 258280326 387420489] 190
 524288    786432    1179648   1769472   2654208   3981312   5971968   8957952  13436928  20155392  30233088  45349632  68024448  102036672 153055008 229582512 344373768 516560652 774840978 1162261467 [1 2 3 4 6 8 9 12 16 18 24 27 32 36 48 54 64 72 81 96 108 128 144 162 192 216 243 256 288 324 384 432 486 512 576 648 729 768 864 972 1024 1152 1296 1458 1536 1728 1944 2048 2187 2304 2592 2916 3072 3456 3888 4096 4374 4608 5184 5832 6144 6561 6912 7776 8192 8748 9216 10368 11664 12288 13122 13824 15552 16384 17496 18432 19683 20736 23328 24576 26244 27648 31104 32768 34992 36864 39366 41472 46656 49152 52488 55296 59049 62208 65536 69984 73728 78732 82944 93312 98304 104976 110592 118098 124416 131072 139968 147456 157464 165888 177147 186624 196608 209952 221184 236196 248832 262144 279936 294912 314928 331776 354294 373248 393216 419904 442368 472392 497664 524288 531441 559872 589824 629856 663552 708588 746496 786432 839808 884736 944784 995328 1062882 1119744 1179648 1259712 1327104 1417176 1492992 1594323 1679616 1769472 1889568 1990656 2125764 2239488 2519424 2654208 2834352 2985984 3188646 3359232 3779136 3981312 4251528 4478976 4782969 5038848 5668704 5971968 6377292 6718464 7558272 8503056 8957952 9565938 10077696 11337408 12754584 13436928 14348907 15116544 17006112 19131876 20155392 22674816 25509168 28697814 30233088 34012224 38263752 43046721 45349632 51018336 57395628 68024448 76527504 86093442 102036672 114791256 129140163 153055008 172186884 229582512 258280326 344373768 387420489 516560652 774840978 1162261467] 210
      1      |      3      |      9      |     27      |     81      |     243     |     729     |    2187     |    6561     |    19683    |    59049    |   177147    |      2      D♭   
      1      |      2      |      8      |     16      |     64      |     128     |     512     |    2048     |    4096     |    16384    |    32768    |   131072    |      1      D♭   
      1      |      3      |      9      |     27      |     81      |     243     |     729     |    2187     |    6561     |    19683    |    59049    |      4      |      2      A♭   
      1      |      2      |      8      |     16      |     64      |     128     |     512     |    2048     |    4096     |    16384    |    32768    |      3      |      1      A♭   
      1      |      3      |      9      |     27      |     81      |     243     |     729     |    2187     |    6561     |    19683    |      4      |     16      |      2      E♭   
      1      |      2      |      8      |     16      |     64      |     128     |     512     |    2048     |    4096     |    16384    |      3      |      9      |      1      E♭   
      1      |      3      |      9      |     27      |     81      |     243     |     729     |    2187     |    6561     |      4      |     16      |     32      |      2      B♭   
      1      |      2      |      8      |     16      |     64      |     128     |     512     |    2048     |    4096     |      3      |      9      |     27      |      1      B♭   
      1      |      3      |      9      |     27      |     81      |     243     |     729     |    2187     |      4      |     16      |     32      |     128     |      2      F    
      1      |      2      |      8      |     16      |     64      |     128     |     512     |    2048     |      3      |      9      |     27      |     81      |      1      F    
      1      |      3      |      9      |     27      |     81      |     243     |     729     |      4      |     16      |     32      |     128     |     256     |      2      C    
      1      |      2      |      8      |     16      |     64      |     128     |     512     |      3      |      9      |     27      |     81      |     243     |      1      C    
      1      |      3      |      9      |     27      |     81      |     243     |      4      |     16      |     32      |     128     |     256     |    1024     |      2      G    
      1      |      2      |      8      |     16      |     64      |     128     |      3      |      9      |     27      |     81      |     243     |     729     |      1      G    
      1      |      3      |      9      |     27      |     81      |      4      |     16      |     32      |     128     |     256     |    1024     |    4096     |      2      D    
      1      |      2      |      8      |     16      |     64      |      3      |      9      |     27      |     81      |     243     |     729     |    2187     |      1      D    
      1      |      3      |      9      |     27      |      4      |     16      |     32      |     128     |     256     |    1024     |    4096     |    8192     |      2      A    
      1      |      2      |      8      |     16      |      3      |      9      |     27      |     81      |     243     |     729     |    2187     |    6561     |      1      A    
      1      |      3      |      9      |      4      |     16      |     32      |     128     |     256     |    1024     |    4096     |    8192     |    32768    |      2      E    
      1      |      2      |      8      |      3      |      9      |     27      |     81      |     243     |     729     |    2187     |    6561     |    19683    |      1      E    
      1      |      3      |      4      |     16      |     32      |     128     |     256     |    1024     |    4096     |    8192     |    32768    |    65536    |      2      B    
      1      |      2      |      3      |      9      |     27      |     81      |     243     |     729     |    2187     |    6561     |    19683    |    59049    |      1      B    
      1      |      4      |     16      |     32      |     128     |     256     |    1024     |    4096     |    8192     |    32768    |    65536    |   262144    |      2      F♯   
      1      |      3      |      9      |     27      |     81      |     243     |     729     |    2187     |    6561     |    19683    |    59049    |   177147    |      1      F♯   
         0:P1| 90:m2|114:A1|180:d3|204:M2|294:m3|318:A2|384:d4|408:M3|498:P4|522:A3|588:d5|612:A4|678:d6|702:P5|792:m6|816:A5|882:d7|906:M6|996:m7|1020:A6|1086:d8|1110:M7|1200:P8
         1   |      | 2187 |      |  9   |      |19683 |      |  81  |      |177147|      | 729  |      |  3   |      | 6561 |      |  27  |      |59049 |      | 243  |  2          D♭   
         1   |      | 2048 |      |  8   |      |16384 |      |  64  |      |131072|      | 512  |      |  2   |      | 4096 |      |  16  |      |32768 |      | 128  |  1          D♭   
         1   |      | 2187 |      |  9   |      |19683 |      |  81  |  4   |      |      | 729  |      |  3   |      | 6561 |      |  27  |      |59049 |      | 243  |  2          A♭   
         1   |      | 2048 |      |  8   |      |16384 |      |  64  |  3   |      |      | 512  |      |  2   |      | 4096 |      |  16  |      |32768 |      | 128  |  1          A♭   
         1   |      | 2187 |      |  9   |      |19683 |      |  81  |  4   |      |      | 729  |      |  3   |      | 6561 |      |  27  |  16  |      |      | 243  |  2          E♭   
         1   |      | 2048 |      |  8   |      |16384 |      |  64  |  3   |      |      | 512  |      |  2   |      | 4096 |      |  16  |  9   |      |      | 128  |  1          E♭   
         1   |      | 2187 |      |  9   |  32  |      |      |  81  |  4   |      |      | 729  |      |  3   |      | 6561 |      |  27  |  16  |      |      | 243  |  2          B♭   
         1   |      | 2048 |      |  8   |  27  |      |      |  64  |  3   |      |      | 512  |      |  2   |      | 4096 |      |  16  |  9   |      |      | 128  |  1          B♭   
         1   |      | 2187 |      |  9   |  32  |      |      |  81  |  4   |      |      | 729  |      |  3   | 128  |      |      |  27  |  16  |      |      | 243  |  2          F    
         1   |      | 2048 |      |  8   |  27  |      |      |  64  |  3   |      |      | 512  |      |  2   |  81  |      |      |  16  |  9   |      |      | 128  |  1          F    
         1   | 256  |      |      |  9   |  32  |      |      |  81  |  4   |      |      | 729  |      |  3   | 128  |      |      |  27  |  16  |      |      | 243  |  2          C    
         1   | 243  |      |      |  8   |  27  |      |      |  64  |  3   |      |      | 512  |      |  2   |  81  |      |      |  16  |  9   |      |      | 128  |  1          C    
         1   | 256  |      |      |  9   |  32  |      |      |  81  |  4   |      | 1024 |      |      |  3   | 128  |      |      |  27  |  16  |      |      | 243  |  2          G    
         1   | 243  |      |      |  8   |  27  |      |      |  64  |  3   |      | 729  |      |      |  2   |  81  |      |      |  16  |  9   |      |      | 128  |  1          G    
         1   | 256  |      |      |  9   |  32  |      |      |  81  |  4   |      | 1024 |      |      |  3   | 128  |      |      |  27  |  16  |      | 4096 |      |  2          D    
         1   | 243  |      |      |  8   |  27  |      |      |  64  |  3   |      | 729  |      |      |  2   |  81  |      |      |  16  |  9   |      | 2187 |      |  1          D    
         1   | 256  |      |      |  9   |  32  |      | 8192 |      |  4   |      | 1024 |      |      |  3   | 128  |      |      |  27  |  16  |      | 4096 |      |  2          A    
         1   | 243  |      |      |  8   |  27  |      | 6561 |      |  3   |      | 729  |      |      |  2   |  81  |      |      |  16  |  9   |      | 2187 |      |  1          A    
         1   | 256  |      |      |  9   |  32  |      | 8192 |      |  4   |      | 1024 |      |      |  3   | 128  |      |32768 |      |  16  |      | 4096 |      |  2          E    
         1   | 243  |      |      |  8   |  27  |      | 6561 |      |  3   |      | 729  |      |      |  2   |  81  |      |19683 |      |  9   |      | 2187 |      |  1          E    
         1   | 256  |      |65536 |      |  32  |      | 8192 |      |  4   |      | 1024 |      |      |  3   | 128  |      |32768 |      |  16  |      | 4096 |      |  2          B    
         1   | 243  |      |59049 |      |  27  |      | 6561 |      |  3   |      | 729  |      |      |  2   |  81  |      |19683 |      |  9   |      | 2187 |      |  1          B    
         1   | 256  |      |65536 |      |  32  |      | 8192 |      |  4   |      | 1024 |      |262144|      | 128  |      |32768 |      |  16  |      | 4096 |      |  2          F♯   
         1   | 243  |      |59049 |      |  27  |      | 6561 |      |  3   |      | 729  |      |177147|      |  81  |      |19683 |      |  9   |      | 2187 |      |  1          F♯   
                                                                                                   1                                                                                                     [1] 1
                                                                                              2         3                                                                                                [1 2 3] 3
                                                                                         4         6         9                                                                                           [1 2 3 4 6 9] 6
                                                                                    8        12        18        27                                                                                      [1 2 3 4 6 8 9 12 18 27] 10
                                                                              16        24        36        54        81                                                                                 [1 2 3 4 6 8 9 12 16 18 24 27 36 54 81] 15
                                                                         32        48        72        108       162       243                                                                           [1 2 3 4 6 8 9 12 16 18 24 27 32 36 48 54 72 81 108 162 243] 21
                                                                    64        96        144       216       324       486       729                                                                      [1 2 3 4 6 8 9 12 16 18 24 27 32 36 48 54 64 72 81 96 108 144 162 216 243 324 486 729] 28
                                                               128       192       288       432       648       972      1458      2187                                                                 [1 2 3 4 6 8 9 12 16 18 24 27 32 36 48 54 64 72 81 96 108 128 144 162 192 216 243 288 324 432 486 648 729 972 1458 2187] 36
                                                          256       384       576       864      1296      1944      2916      4374      6561                                                            [1 2 3 4 6 8 9 12 16 18 24 27 32 36 48 54 64 72 81 96 108 128 144 162 192 216 243 256 288 324 384 432 486 576 648 729 864 972 1296 1458 1944 2187 2916 4374 6561] 45
                                                     512       768      1152      1728      2592      3888      5832      8748      3280      9841                                                       [1 2 3 4 6 8 9 12 16 18 24 27 32 36 48 54 64 72 81 96 108 128 144 162 192 216 243 256 288 324 384 432 486 512 576 648 729 768 864 972 1152 1296 1458 1728 1944 2187 2592 2916 3280 3888 4374 5832 6561 8748 9841] 55
                                               1024      1536      2304      3456      5184      7776      2916      4374      1640      4920      7381                                                  [1 2 3 4 6 8 9 12 16 18 24 27 32 36 48 54 64 72 81 96 108 128 144 162 192 216 243 256 288 324 384 432 486 512 576 648 729 768 864 972 1024 1152 1296 1458 1536 1640 1728 1944 2187 2304 2592 2916 3280 3456 3888 4374 4920 5184 5832 6561 7381 7776 8748 9841] 64
                                          2048      3072      4608      6912      2592      3888      1458      2187       820      2460      3690      5535                                             [1 2 3 4 6 8 9 12 16 18 24 27 32 36 48 54 64 72 81 96 108 128 144 162 192 216 243 256 288 324 384 432 486 512 576 648 729 768 820 864 972 1024 1152 1296 1458 1536 1640 1728 1944 2048 2187 2304 2460 2592 2916 3072 3280 3456 3690 3888 4374 4608 4920 5184 5535 5832 6561 6912 7381 7776 8748 9841] 72
                                     4096      6144      9216      3456      1296      1944       729      1093       410      1230      1845      2767      8303                                        [1 2 3 4 6 8 9 12 16 18 24 27 32 36 48 54 64 72 81 96 108 128 144 162 192 216 243 256 288 324 384 410 432 486 512 576 648 729 768 820 864 972 1024 1093 1152 1230 1296 1458 1536 1640 1728 1845 1944 2048 2187 2304 2460 2592 2767 2916 3072 3280 3456 3690 3888 4096 4374 4608 4920 5184 5535 5832 6144 6561 6912 7381 7776 8303 8748 9216 9841] 81
                                8192      3072      4608      1728       648       972       364       546       205       615       922      1383      4151      6227                                   [1 2 3 4 6 8 9 12 16 18 24 27 32 36 48 54 64 72 81 96 108 128 144 162 192 205 216 243 256 288 324 364 384 410 432 486 512 546 576 615 648 729 768 820 864 922 972 1024 1093 1152 1230 1296 1383 1458 1536 1640 1728 1845 1944 2048 2187 2304 2460 2592 2767 2916 3072 3280 3456 3690 3888 4096 4151 4374 4608 4920 5184 5535 5832 6144 6227 6561 6912 7381 7776 8192 8303 8748 9216 9841] 90
                           4096      1536      2304       864       324       486       182       273       102       307       461       691      2075      3113      9341                              [1 2 3 4 6 8 9 12 16 18 24 27 32 36 48 54 64 72 81 96 102 108 128 144 162 182 192 205 216 243 256 273 288 307 324 364 384 410 432 461 486 512 546 576 615 648 691 729 768 820 864 922 972 1024 1093 1152 1230 1296 1383 1458 1536 1640 1728 1845 1944 2048 2075 2187 2304 2460 2592 2767 2916 3072 3113 3280 3456 3690 3888 4096 4151 4374 4608 4920 5184 5535 5832 6144 6227 6561 6912 7381 7776 8192 8303 8748 9216 9341 9841] 99
                      2048       768      1152       432       162       243       91        136       51        153       230       345      1037      1556      4670      7006                         [1 2 3 4 6 8 9 12 16 18 24 27 32 36 48 51 54 64 72 81 91 96 102 108 128 136 144 153 162 182 192 205 216 230 243 256 273 288 307 324 345 364 384 410 432 461 486 512 546 576 615 648 691 729 768 820 864 922 972 1024 1037 1093 1152 1230 1296 1383 1458 1536 1556 1640 1728 1845 1944 2048 2075 2187 2304 2460 2592 2767 2916 3072 3113 3280 3456 3690 3888 4096 4151 4374 4608 4670 4920 5184 5535 5832 6144 6227 6561 6912 7006 7381 7776 8192 8303 8748 9216 9341 9841] 109
                 1024       384       576       216       81        121       45        68        25        76        115       172       518       778      2335      3503      5254                    [1 2 3 4 6 8 9 12 16 18 24 25 27 32 36 45 48 51 54 64 68 72 76 81 91 96 102 108 115 121 128 136 144 153 162 172 182 192 205 216 230 243 256 273 288 307 324 345 364 384 410 432 461 486 512 518 546 576 615 648 691 729 768 778 820 864 922 972 1024 1037 1093 1152 1230 1296 1383 1458 1536 1556 1640 1728 1845 1944 2048 2075 2187 2304 2335 2460 2592 2767 2916 3072 3113 3280 3456 3503 3690 3888 4096 4151 4374 4608 4670 4920 5184 5254 5535 5832 6144 6227 6561 6912 7006 7381 7776 8192 8303 8748 9216 9341 9841] 121
             512       192       288       108       40        60       2916       34       3280       38        57        86        259       389      1167      1751      2627      7882               [1 2 3 4 6 8 9 12 16 18 24 25 27 32 34 36 38 40 45 48 51 54 57 60 64 68 72 76 81 86 91 96 102 108 115 121 128 136 144 153 162 172 182 192 205 216 230 243 256 259 273 288 307 324 345 364 384 389 410 432 461 486 512 518 546 576 615 648 691 729 768 778 820 864 922 972 1024 1037 1093 1152 1167 1230 1296 1383 1458 1536 1556 1640 1728 1751 1845 1944 2048 2075 2187 2304 2335 2460 2592 2627 2767 2916 3072 3113 3280 3456 3503 3690 3888 4096 4151 4374 4608 4670 4920 5184 5254 5535 5832 6144 6227 6561 6912 7006 7381 7776 7882 8192 8303 8748 9216 9341 9841] 133
        256       96        144       54       2592       30       1458      4374      1640      4920       28        43        129       194       583       875      1313      3941      5911          [1 2 3 4 6 8 9 12 16 18 24 25 27 28 30 32 34 36 38 40 43 45 48 51 54 57 60 64 68 72 76 81 86 91 96 102 108 115 121 128 129 136 144 153 162 172 182 192 194 205 216 230 243 256 259 273 288 307 324 345 364 384 389 410 432 461 486 512 518 546 576 583 615 648 691 729 768 778 820 864 875 922 972 1024 1037 1093 1152 1167 1230 1296 1313 1383 1458 1536 1556 1640 1728 1751 1845 1944 2048 2075 2187 2304 2335 2460 2592 2627 2767 2916 3072 3113 3280 3456 3503 3690 3888 3941 4096 4151 4374 4608 4670 4920 5184 5254 5535 5832 5911 6144 6227 6561 6912 7006 7381 7776 7882 8192 8303 8748 9216 9341 9841] 143
   128       48        72        27       1296      3888       729      2187       820      2460      3690      2767       64        97        291       437       656      1970      2955      8867     [1 2 3 4 6 8 9 12 16 18 24 25 27 28 30 32 34 36 38 40 43 45 48 51 54 57 60 64 68 72 76 81 86 91 96 97 102 108 115 121 128 129 136 144 153 162 172 182 192 194 205 216 230 243 256 259 273 288 291 307 324 345 364 384 389 410 432 437 461 486 512 518 546 576 583 615 648 656 691 729 768 778 820 864 875 922 972 1024 1037 1093 1152 1167 1230 1296 1313 1383 1458 1536 1556 1640 1728 1751 1845 1944 1970 2048 2075 2187 2304 2335 2460 2592 2627 2767 2916 2955 3072 3113 3280 3456 3503 3690 3888 3941 4096 4151 4374 4608 4670 4920 5184 5254 5535 5832 5911 6144 6227 6561 6912 7006 7381 7776 7882 8192 8303 8748 8867 9216 9341 9841] 150
'''