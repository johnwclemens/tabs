from tpkg       import utl
#from tpkg       import notes
from tpkg.notes import Notes
from tpkg       import intrvls as ivls
import math

W,    Y,    Z,    slog,   ist = utl.W,    utl.Y,    utl.Z,    utl.slog,   utl.ist
fmtl,   fmtm,    fmtf,   fmtg = utl.fmtl, utl.fmtm, utl.fmtf, utl.fmtg
NT, A4_INDEX, CM_P_M, V_SOUND = ivls.NT, ivls.A4_INDEX, ivls.CM_P_M, ivls.V_SOUND
N2I,          F2S             = Notes.N2I, Notes.F2S
########################################################################################################################################################################################################
########################################################################################################################################################################################################

class Pthgrn(ivls.Intonation):
    def __str__(self):  return f'{self.__class__.__name__}'
    def __repr__(self): return f'{self.__class__.__name__}'
    
    def __init__(self, n='C', rf=440, ss=V_SOUND, csv=0):
        super().__init__(n=n, rf=rf, ss=ss, csv=csv)
#        self.ivalKs = ['P1', 'm2', 'A1', 'd3', 'M2', 'm3', 'A2', 'd4', 'M3', 'P4', 'A3', 'd5', 'A4', 'd6', 'P5', 'm6', 'A5', 'd7', 'M6', 'm7', 'A6', 'd8', 'M7', 'P8']
#        self.centKs = [  0,   90,  114,  180,  204,  294,  318,  384,  408,  498,  522,  588,  612,  678,  702,  792,  816,  882,  906,  996,  1020, 1086, 1110, 1200]
#                     [  0    1     2     3     4     5     6     7     8     9    10    11    12    13    14    15    16    17    18    19     20    21    22    23    24    25    26    27 ]
        self.ivalKs = ['P1', 'LA', 'm2', 'A1', 'd3', 'M2', 'm3', 'A2', 'd4', 'M3', 'LC', 'P4', 'A3', 'd5', 'A4', 'd6', 'P5', 'LD', 'm6', 'A5', 'd7', 'M6', 'm7', 'A6', 'd8', 'M7', 'LB', 'P8']
        self.centKs = [   0,   23,  90,  114,  180,  204,  294,  318,  384,  408,  475,  498,  522,  588,  612,  678,  702,  725,  792,  816,  882,  906,  996,  1020, 1086, 1110, 1177, 1200]
        self.set_ck2ikm() # todo this base class method initializes and or sets self.ck2ikm
        self.ckmap  = self.reset_ckmap() # freq ratio in cents to ival counts and data
    ####################################################################################################################################################################################################
    ####################################################################################################################################################################################################
    def HIDE__setup(self, o, csv=0):
        self.csv = csv
        if   o == 0:
            x = 0
            slog(f'PRT 1 0-NT+{x=}, {self.i=:2} {self.m=:2} {self.csv=}', p=0)
            self.nimap = {}
            for i in range(0, NT + x):
                self.j = self.i + (i * 7) % (NT + x)
                slog(f'PRT 1 0-({NT}+{x}), {i=} {self.j=} {self.i=:2} {self.m=:2} {self.csv=}', p=0)
                self._setup()
    ####################################################################################################################################################################################################
    def epsilon(self, dbg=0): # todo generalize m2bc ?
        ccents = self.comma()
        ecents = ccents / NT
        if dbg:  slog(f'Epsilon = Comma / {NT} = {ccents:10.5f} / {NT} = {ecents:10.5f} cents')
        return ecents
        
    def comma(self, dbg=0): # todo generalize m2bc ?
        n, i, iv  = NT, -1, '5' # 3**12 / 2**19 = 3¹²/2¹⁹ = 531441 / 524288 = 1.0136432647705078, log2(1.0136432647705078) = 0.019550008653874178, 1200 * log2() = 23.460010384649014
        s5s       = ivls.stck5ths(n)
        a, b, c   = s5s[i]
        r, ca, cb = self.abc2r(a, b, c)
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
        pfx, pfx2 = Z, f'{mm}  k  {mm}{nn} {nn}'   ;   sfx = f'{nn}]'   ;   f0 = self.FREFS[self.j] #  ;   w2 = '7.2f'
        if dbg and ni==0:  self.dmpIndices(pfx2, x)   ;   self.dmpDataTableLine(x+1)
        for i, (kk, v) in enumerate(self.nimap.items()):
            rat0, rat2, rat3, cents, cfnts = [], [], [], [], []    ;    cki = -1   ;   self.k = kk
            rat1 = [] if x==13 or x==6 or x==7 else None    ;   ratA = [] if x == 9 else None   ;   ratB = [] if x == 9 else None
            for j, e in enumerate(v[2]):
#               n    = self.fmtNPair(kk, j)   ;   a, ca, b, cb = e   ;  pa, pb = a ** ca, b ** cb   ;  pd = [f'{i:x}', f'{kk:2}', f'{n:2}'] if dbg else [f'{i:x}', f'{kk:2}  ']
                n    = self.fmtNPair(j)       ;   a, ca, b, cb = e   ;  pa, pb = a ** ca, b ** cb   ;  pd = [f'{i:x}', f'{kk:2}', f'{n:2}'] if dbg else [f'{i:x}', f'{kk:2}  ']
                pfx  = f'{mm.join(pd)}{nn}[{nn}' if dbg else pfx     ;     sfx = f' {nn}{n:2}' if not dbg else sfx
                cent = self.r2cents(pa/pb)    ;   rc = round(cent)   ;    cki += 1
                if dbg and upd and ni == 4:   self.updCkMap(rc, self.ckmap, n if kk==self.j else W*2, f0*pa/pb, e, cent, j)
                while cki < len(self.centKs) and self.centKs[cki] < rc:
                    rat0.append(_)   ;  rat2.append(_)   ;   rat3.append(_)    ;    cki += 1    ;  cents.append(_) #  ;   cfnts.append(_)
                    rat1.append(_) if x==13 else None    ;   ratA.append(_) if x==9 else None   ;   ratB.append(_) if x==9 else None
                cents.append(rc) #  ;   cfnts.append(f'{cent:{w2}}')
                if   x==9:          self.addFmtRs(a, ca, b, cb, rs=[rat0, ratA, ratB, rat2, rat3], u=yy, w=x,     i=i, j=j)
                elif x==13:         self.addFmtRs(a, ca, b, cb, rs=[rat0,       rat1, rat2, rat3], u=yy, w=x,     i=i, j=j)
                elif x==6 or x==7:  self.addFmtRs(a, ca, b, cb, rs=[rat0,       rat1, rat2, rat3], u=yy, w=x,     i=i, j=j)
            pd = [f'{i:x}', f'{kk:2}', f'{self.fmtNPair(0):2}'] if dbg else [f'{i:x}', f'{kk:2}  ']   ;   pfx = f'{mm.join(pd)}{nn}[{nn}' if dbg else pfx #fixme hack to fix note name in pfx
            if dbg: # pfx was set last at the end of the inner for loop
                if   ni==0:           slog(f'{pfx}{Z.join(fmtl(rat0,  w=ww, s=oo, d=Z))}{sfx}',  p=0, f=ff)
                elif ni==1 and x==9:  slog(f'{pfx}{Z.join(fmtl(ratA,  w=ww, s=oo, d=Z))}{sfx}',  p=0, f=ff)  ;  slog(f'{pfx}{Z.join(fmtl(ratB, w=ww, s=oo, d=Z))}{sfx}', p=0, f=ff)
                elif ni==1 and x==13: slog(f'{pfx}{Z.join(fmtl(rat1,  w=ww, s=oo, d=Z))}{sfx}',  p=0, f=ff)
                elif ni==2:           slog(f'{pfx}{Z.join(fmtl(rat2,  w=ww, s=oo, d=Z))}{sfx}',  p=0, f=ff)
                elif ni==3:           slog(f'{pfx}{Z.join(fmtl(rat3,  w=ww, s=oo, d=Z))}{sfx}',  p=0, f=ff)
                elif ni==4:           slog(f'{pfx}{Z.join(fmtl(cents, w=ww, s=oo, d=Z))}{sfx}',  p=0, f=ff)
            elif ni==0:               slog(f'{pfx}{Z.join(fmtl(rat0,  w=ww, s=oo, d=Z))}{sfx}',  p=0, f=ff if self.csv else -3)
            elif ni==5:               slog(f'{pfx}{Z.join(fmtl(cents, w=ww, s=oo, d=Z))}{sfx}',  p=0, f=ff if self.csv else -3)
        if dbg: self.dmpDataTableLine(x+1)   ;   self.dmpIndices(pfx2, x) if ni == 4 else None
    ####################################################################################################################################################################################################
    def dmpCkMap(self, u=9, o=0, dbg=1): #todo generalize m2bc ? # ckmap[498,588,612,702][Note] = F,Gb,G,Ab
        mm, nn, oo, ff = (Y, Y, Y, 3) if self.csv else (W, Z, '|', 1)  ;  f0, v, ww, y = self.FREFS[self.j], Z, f'^{u}', 4  ;  _ = u*W if dbg else 7*W  ;  cks = self.centKs if dbg else None
        ns, fs, ws, vs = [], [], [], []  ;  cs, ds, d2s, qs, ks, cksi = [], [], [], [], [], []  ;  r0s, rAs, rBs, r2s, r3s = [], [], [], [], []  ;  ckmap = self.ckmap if dbg else self.nimap[self.j][0]
        sfx = f'{nn}]'   ;   sfxc = f'{nn}]{mm}cents'   ;   sfxf = f'{nn}]{mm}Hz'   ;   sfxw = f'{nn}]{mm}cm'   ;   f1 = 0
        for i, ck in enumerate(self.centKs):
            ival = self.ck2ikm[ck]    ;    vs.append(ival)    ;   assert ckmap and ck in ckmap,  f'{self.j=} {i=} {ival=} {ck=} {ckmap=} {self.ckmap=} {self.nimap[self.j][0]=} {dbg=}'
            if ckmap[ck]['Count'] > 0:
                assert ival == ckmap[ck]['Ival'],  f'{ival=} {ck=} {ckmap[ck]["Ival"]=}'    ;   a, ca, b, cb = ckmap[ck]['Abcd']   ;   q = self.fdvdr(a, ca, b, cb)
                r0s, rAs, rBs, r2s, r3s = self.addFmtRs(a, ca, b, cb, rs=[r0s, rAs, rBs, r2s, r3s], u=y, w=u if dbg else 7,     i=i, j=ck)
                f, w, n, c, d, k, i2    = self.getCkMapVal(ckmap, ck, a, ca, b, cb, f0, self.w0)
                n, m = self.f2nPair(f, b=1, o=0, e=1)   ;   assert m != n,  f'{i=} {ck=} {m=} {n=} {c=} {d=} {k=} {i2=} {f=} {w=}'
                if m:
                    if   m not in self.COFM[self.n]:   n = n + '/' + m
                    elif f1:                           n = m
                    else:                             f1 = 1
                self.k = N2I[n[:2]] + 48 if n in N2I else self.k   ;   self.o = n[:2] if n in Notes.N2I else self.o
                cksi.append(int(round(c)))  ;  cs.append(f'{fmtf(c, u-4)}')   ; ds.append(f'{fmtf(d, u-4)}') ; fs.append(f'{fmtf(f, u-2)}') ; ws.append(f'{fmtf(w, u-2)}')
            else:  n, d, k, q = _, _, 0, Z  ;  cksi.append(ck) ; cs.append(_) ; ds.append(_) ; fs.append(_)  ; ws.append(_) ; r0s.append(_) ; rAs.append(_) ; rBs.append(_) ; r2s.append(_) ; r3s.append(_)
            if dbg:   ns.append(n)  ;  d2s.append(d)  ;  ks.append(k)  ;  qs.append(q)  ;  self.dmpIvals(i, cksi, ks, d2s)
        if dbg:
            self.dmpIndices(f'{mm}  k  {mm}{nn} {nn}', u)  ;  self.dmpDataTableLine(u+1)
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
            slog(f'{mm}Count{mm}{nn}[{nn}{fmtl(ks,  w=ww, s=oo, d=Z)}{sfx}',  p=0, f=ff)  ;  self.dmpDataTableLine(u+1)
        elif rAs and rBs:    self.dmpABs(rAs, rBs, o)
    ####################################################################################################################################################################################################
    def dmpABs(self, rAs, rBs, o):
        abcs = self.nimap[self.j][1]    ;   aa, bb = [], []
        for j, abc in enumerate(abcs):
            a, b, c = abc[0], abc[1], abc[2]
            r, ca, cb = self.abc2r(a, b, c)
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
            r, ca, cb = self.abc2r(a, b, c)
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
    def getCkMapVal(self, ckmap, ck, a, ca, b, cb, f0, w0): # todo move to base class, but abc args and key are issues
        f = ckmap[ck]['Freq']    ;   assert round(f, 10) == round(f0 * a**ca / b**cb, 10),    f'{ck=} {f=} {f0=} r={a**ca/b**cb} {f0*a**ca/b**cb=} {a=} {ca=} {b=} {cb=}' #todo remove round() hack! use Decimal
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
#                                    #           <-----------------1---------------->   <-----------------2---------------->   <-----------------3---------------->   <-----------------4---------------->
        for j, d in enumerate(data): # j j*100 i Iv  c     k       d       e       c`   Iv  c     k       d       e       c`   Iv  c     k       d       e       c`   Iv  c     k       d       e       c`
            if   j==0:                 fd.append(f'{d:x}')           # j
            elif j==1:                 fd.append(f'{d:4}')           # j*100
            elif j==2:                 fd.append(f'{d:2} ')          # i
            elif j==6:                 fd.append(f'{d:7.3f}') if utl.ist(d, float) else fd.append(W*7) # d
            elif j in (12, 18, 24):    fd.append(f'{d:7.3f}') if utl.ist(d, float) else fd.append(W*7) if i!=0 and i!=len(self.ck2ikm)-1 else fd.append(W*7) # d d d
            elif j in ( 8, 14, 20):    fd.append(f'*{mm}{d:2}  ')    # c` c` c`
            elif j==26:                fd.append(f'*{mm}{d:2}')      # c`
            elif j in (5, 11, 17, 23): fd.append(f'@{mm}{d:4}{mm}:') # k k k k
            elif j in (7, 13, 19, 25): fd.append(f'={mm}{d:5.3f}')   # e e e e
            elif j in (3,  9, 15, 21): fd.append(f'|  {d:2}')        # Iv Iv Iv Iv
            elif j in (4, 10, 16, 22): fd.append(f'{d:2}')           # c c c c
        return fd

    def dmpIvals(self, h, ks, cs, ds): # todo move to base class, but epsilon is an issue
        mm, nn, oo, ff = (Y, Y, Y, 3) if self.csv else (W, Z, '|', 1)   ;   i, j, k = h-1, h-2, h-3   ;   nh, ni, nj, nk = 0, 0, 0, 0
        eps, l = self.epsilon(), math.floor(h/2)    ;    hdrA = ['j', 'j*100', 'i ']   ;   data = []   ;   m = l - 1 if h > 11 else l
        hdrB1  = ['|  Iv', f' c{mm} ', f'  k {mm} ', f'   d   {mm} ', f' e   {mm} ', f' c` ']
        hdrB2  = ['|  Iv', f' c{mm} ', f'  k {mm} ', f'   d   {mm} ', f' e   {mm} ', f' c`']
        hdrs   = hdrA   ;   hdrs.extend(hdrB1)   ;   hdrs.extend(hdrB1)   ;   hdrs.extend(hdrB1)   ;   hdrs.extend(hdrB2)
        if   h > 0:    nh, ni         = self.ck2ikm[ks[h]], self.ck2ikm[ks[i]]
        elif h > 1:    nh, ni, nj     = self.ck2ikm[ks[h]], self.ck2ikm[ks[i]], self.ck2ikm[ks[j]]
        elif h > 2:    nh, ni, nj, nk = self.ck2ikm[ks[h]], self.ck2ikm[ks[i]], self.ck2ikm[ks[j]], self.ck2ikm[ks[k]]
        if   h == 0:   slog(f'{fmtl(hdrs, s=mm, d=Z)}', p=0, f=ff)
        if   h ==  1:  w, x    = nh, ni      ;  data = [m, m * 100, h, x, cs[i], ks[i], ds[i], eps, cs[h], w, cs[h], ks[h], ds[h], eps, cs[i]]
        elif h ==  3:  w, x    = nh, ni      ;  data = [m, m * 100, h, x, cs[i], ks[i], ds[i], eps, cs[h], w, cs[h], ks[h], ds[h], eps, cs[i]]
        elif h ==  5:  w, x    = nh, ni      ;  data = [m, m * 100, h, w, cs[h], ks[h], ds[h], eps, cs[i], x, cs[i], ks[i], ds[i], eps, cs[h]]
        elif h ==  7:  w, x    = nh, ni      ;  data = [m, m * 100, h, x, cs[i], ks[i], ds[i], eps, cs[h], w, cs[h], ks[h], ds[h], eps, cs[i]]
        elif h ==  9:  w, x    = nh, ni      ;  data = [m, m * 100, h, w, cs[h], ks[h], ds[h], eps, cs[i], x, cs[i], ks[i], ds[i], eps, cs[h]]
        elif h == 12:  w, x, y = nh, ni, nj  ;  data = [m, m * 100, h, x, cs[i], ks[i], ds[i], eps, cs[h], w, cs[h], ks[h], ds[h], eps, cs[i], y, cs[j], ks[j], ds[j], eps, cs[i]]
        elif h == 14:  x, w    = nh, ni      ;  data = [m, m * 100, h, w, cs[h], ks[h], ds[h], eps, cs[i], x, cs[i], ks[i], ds[i], eps, cs[h]]
        elif h == 17:  w, x, y = nh, ni, nj  ;  data = [m, m * 100, h, x, cs[i], ks[i], ds[i], eps, cs[h], y, cs[j], ks[j], ds[j], eps, cs[i], w, cs[h], ks[h], ds[h], eps, cs[i]]
        elif h == 19:  w, x    = nh, ni      ;  data = [m, m * 100, h, x, cs[i], ks[i], ds[i], eps, cs[h], w, cs[h], ks[h], ds[h], eps, cs[i]]
        elif h == 21:  w, x    = nh, ni      ;  data = [m, m * 100, h, w, cs[h], ks[h], ds[h], eps, cs[i], x, cs[i], ks[i], ds[i], eps, cs[h]]
        elif h == 23:  w, x    = nh, ni      ;  data = [m, m * 100, h, x, cs[i], ks[i], ds[i], eps, cs[h], w, cs[h], ks[h], ds[h], eps, cs[i]]
        elif h == 25:  w, x    = nh, ni      ;  data = [m, m * 100, h, w, cs[h], ks[h], ds[h], eps, cs[i], x, cs[i], ks[i], ds[i], eps, cs[h]]
        elif h == 27:  w, x    = nh, ni      ;  data = [m, m * 100, h, w, cs[h], ks[h], ds[h], eps, cs[i], x, cs[i], ks[i], ds[i], eps, cs[h]]
#       if       h % 2 and (h <= 9 or h >= 17):    fd = self.fIvals(data, h)  ;  slog(f'{fmtl(fd, s=mm, d=Z)}', p=0, f=ff)
#       if       h % 2 and (h < 11 or h > 15):     fd = self.fIvals(data, h)  ;  slog(f'{fmtl(fd, s=mm, d=Z)}', p=0, f=ff)
        if       h % 2 and h not in (11, 13, 15):  fd = self.fIvals(data, h)  ;  slog(f'{fmtl(fd, s=mm, d=Z)}', p=0, f=ff)
        elif not h % 2 and h     in (12, 14):      fd = self.fIvals(data, h)  ;  slog(f'{fmtl(fd, s=mm, d=Z)}', p=0, f=ff)
'''
j j*100 i Iv  c     k       d       e       c`   Iv  c     k       d       e       c`   Iv  c     k       d       e       c`   Iv  c     k       d       e       c`
0    0  1 P1 12 @    0 :   0.000 = 1.955 *  0    LA  0 @   23 :         = 1.955 * 12   
1  100  3 m2  7 @   90 :  -9.780 = 1.955 *  5    A1  5 @  114 :  13.690 = 1.955 *  7   
2  200  5 M2 10 @  204 :   3.910 = 1.955 *  2    d3  2 @  180 : -19.550 = 1.955 * 10   
3  300  7 m3  9 @  294 :  -5.870 = 1.955 *  3    A2  3 @  318 :  17.600 = 1.955 *  9   
4  400  9 M3  8 @  408 :   7.820 = 1.955 *  4    d4  4 @  384 : -15.640 = 1.955 *  8   
5  500 12 P4 11 @  498 :  -1.960 = 1.955 *  1    A3  1 @  522 :  21.510 = 1.955 * 11     0  0 @  475 :         = 1.955 * 11   
6  600 14 d5  6 @  612 :  11.730 = 1.955 *  6    A4  6 @  588 : -11.730 = 1.955 *  6   
7  700 17 P5 11 @  702 :   1.960 = 1.955 *  0     0  1 @  678 : -21.510 = 1.955 * 11    LD  0 @  725 :         = 1.955 * 11   
8  800 19 m6  8 @  792 :  -7.820 = 1.955 *  4    A5  4 @  816 :  15.640 = 1.955 *  8   
9  900 21 M6  9 @  906 :   5.870 = 1.955 *  3    d7  3 @  882 : -17.600 = 1.955 *  9   
a 1000 23 m7 10 @  996 :  -3.910 = 1.955 *  2    A6  2 @ 1020 :  19.550 = 1.955 * 10   
b 1100 25 M7  7 @ 1110 :   9.780 = 1.955 *  5    d8  5 @ 1086 : -13.690 = 1.955 *  7   
c 1200 27 P8 12 @ 1200 :   0.000 = 1.955 *  0    LB  0 @ 1177 :         = 1.955 * 12   
'''
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
