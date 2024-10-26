from tpkg       import utl
#from tpkg       import notes
from tpkg.notes import Notes
from tpkg       import intrvls as ivls
import math

W,    Y,    Z,    slog,   ist = utl.W,    utl.Y,    utl.Z,    utl.slog,   utl.ist
fmtl,   fmtm,    fmtf,   fmtg = utl.fmtl, utl.fmtm, utl.fmtf, utl.fmtg
NT, A4_INDEX, CM_P_M, V_SOUND = ivls.NT, ivls.A4_INDEX, ivls.CM_P_M, ivls.V_SOUND
N2I, F2S, I2F, I4V, I6V, I4V_I6V, nextN, prevN = Notes.N2I, Notes.F2S, Notes.I2F, Notes.I4V, Notes.I6V, Notes.I4V_I6V, Notes.nextN, Notes.prevN
########################################################################################################################################################################################################
########################################################################################################################################################################################################

class Pthgrn(ivls.Intonation):
    def __str__(self):  return f'{self.__class__.__name__}'
    def __repr__(self): return f'{self.__class__.__name__}'

    def __init__(self, n='C', rf=440, ss=V_SOUND, csv=0):
        super().__init__(n=n, rf=rf, ss=ss, csv=csv)
#        self.ivalKs = ['P1',  'm2', 'M2', 'm3', 'M3', 'P4', 'A4', 'P5',  'm6', 'M6',  'm7', 'M7', 'P8']
#        self.centKs = [  0,    90,  204,  294,   408,  498,  612,  702,   792,  906,   996, 1110, 1200]
#        self.ivalKs = ['P1',  'm2', 'M2', 'm3', 'M3', 'P4', 'd5', 'A4', 'P5',  'm6', 'M6',  'm7', 'M7', 'P8']
#        self.centKs = [  0,    90,  204,  294,   408,  498,  588,  612,  702,   792,  906,   996, 1110, 1200]
#        self.ivalKs = ['P1',  'm2', 'A1', 'd3', 'M2', 'm3', 'A2', 'd4', 'M3', 'P4',  'A3', 'd5', 'A4', 'd6',  'P5',  'm6', 'A5', 'd7', 'M6',  'm7', 'A6', 'd8', 'M7', 'P8']
#        self.centKs = [  0,    90,  114,  180,  204,  294,  318,  384,   408,  498,   522,  588,  612,  678,   702,   792,  816,  882,  906,   996,  1020, 1086, 1110, 1200]
#        self.ivalKs = ['P1',  'm2', 'A1', 'd3', 'M2', 'm3', 'A2', 'd4', 'M3', 'P4',  'A3', 'd5', 'A4', 'd6',  'P5',  'm6', 'A5', 'd7', 'M6',  'm7', 'A6', 'd8', 'M7', '???', 'P8']
#        self.centKs = [  0,    90,  114,  180,  204,  294,  318,  384,   408,  498,   522,  588,  612,  678,   702,   792,  816,  882,  906,   996,  1020, 1086, 1110, 1177, 1200]
#                     [  0     1      2     3     4     5     6      7      8     9     10    11    12    13     14     15    16    17    18     19    20    21    22     23    24]
#        self.ivalKs = ['P1',  'd2', 'm2',  'A1', 'd3', 'M2', 'm3', 'A2', 'd4',  'M3',  'P4', 'A3', 'd5', 'A4', 'd6',  'P5',  'm6', 'A5', 'd7', 'M6',  'm7', 'A6', 'd8', 'M7', 'P8']
#        self.centKs = [  0,    23,   90,   114,  180,  204,  294,  318,  384,   408,   498,   522,  588,  612,  678,   702,   792,  816,  882,  906,   996,  1020, 1086, 1110, 1200]
        self.ivalKs = ['P1',  'd2', 'm2',  'A1', 'd3', 'M2', 'm3', 'A2', 'd4',  'M3',  'P4', 'A3', 'd5', 'A4', 'd6',  'P5',  'm6', 'A5', 'd7', 'M6',  'm7', 'A6', 'd8', 'M7', 'A7', 'P8']
        self.centKs = [  0,    23,   90,   114,  180,  204,  294,  318,  384,   408,   498,   522,  588,  612,  678,   702,   792,  816,  882,  906,   996,  1020, 1086, 1110, 1177, 1200]
#                     [  0     1      2     3     4     5     6      7      8     9     10    11    12    13     14     15    16    17    18     19    20    21    22     23     24    25    26    27    28     29     30    31    32    33    34     35    36]
#        self.ivalKs = ['P1', 'd2', 'dd3', 'm2', 'A1', 'd3', 'M2', 'AA1', 'dd4', 'm3', 'A2', 'd4', 'M3', 'AA2', 'dd5', 'P4', 'A3', 'AA3', 'd5', 'A4', 'd6', 'P5', 'AA4', 'dd7', 'm6', 'A5', 'd7', 'M6', 'AA5', 'dd8', 'm7', 'A6', 'd8', 'M7', 'AA6', 'A7', 'P8']
#        self.centKs = [   0,   23,   67,   90,  114,  180,  204,   227,   271,  294,  318,  384,  408,   431,   475,   498,  522,  565,  588,  612,  678,  702,   725,   769,   792,  816,  882,  906,  929,   973,  996,  1020, 1086, 1110, 1133,  1177, 1200]
#        self.ivalKs = ['P1', 'd2', 'dd3', 'm2', 'A1', 'd3', 'M2', 'AA1', 'dd4', 'm3', 'A2', 'd4', 'M3', 'AA2', 'dd5', 'P4', 'A3', 'AA3', 'd5', 'A4', '???', 'd6', 'P5', 'AA4', 'dd7', 'm6', 'A5', 'd7', 'M6', 'AA5', 'dd8', 'm7', 'A6', '???', 'd8', 'M7', 'AA6', 'A7', 'P8']
#        self.centKs = [   0,   23,   67,   90,  114,  180,  204,   227,   271,  294,  318,  384,  408,   431,   475,   498,  522,  565,  588,  612,   635,  678,  702,   725,   769,   792,  816,  882,  906,  929,   973,  996,  1020,  1063, 1086, 1110, 1133,  1177, 1200]
#                     [  0     1     2       3     4     5     6       7     8     9      10    11     12     13    14    15     16     17    18    19     20     21     22    23    24     25     26    27    28     29    30     31    32     33     34    35     36    37     38     39    40    41     42     43     44    45    46     47     48    49    50     51     52    54    55]
#        self.ivalKs = ['P1', 'd2', '???', 'dd3', 'm2', 'A1', '???', '???', 'd3', 'M2', 'AA1','???', '???', 'dd4', 'm3', 'A2', '???', '???', 'd4', 'M3', 'AA2', '???', 'dd5', 'P4', 'A3', '???', 'AA3', 'd5', 'A4', '???', '???', 'd6', 'P5', 'AA4', '???', 'dd7', 'm6', 'A5', '???', '???', 'd7', 'M6', 'AA5', '???', 'dd8', 'm7', 'A6', '???', '???', 'd8', 'M7', 'AA6', '???', 'A7', 'P8']
#        self.centKs = [   0,   23,   47,   67,   90,   114,   137,   157,  180,  204,   227,  247,   251,   271,   294,  318,  341,   361,  384,  408,   431,   451,   475,   498,  522,  545,   565,  588,   612,  635,   655,  678,  702,   725,   749,   769,   792,  816,  839,   859,  882,  906,   929,   949,   973,  996,  1020,  1043,  1063,  1086, 1110, 1133,  1153,  1177, 1200]
        self.set_ck2ikm() # todo this base class method initializes and or sets self.ck2ikm
        self.ckmap  = self.reset_ckmap() # freq ratio in cents to ival counts and data
    ####################################################################################################################################################################################################
    ####################################################################################################################################################################################################
    def epsilon(self, dbg=0): # todo generalize m2bc ?
        ccents = self.comma()
        ecents = ccents / NT
        if dbg:  slog(f'Epsilon = Comma / {NT} = {ccents:10.5f} / {NT} = {ecents:10.5f} cents')
        return ecents

    def comma(self, dbg=0): # todo generalize m2bc ?
        n, i, iv     = NT, -1, '5' # 3**12 / 2**19 = 3¹²/2¹⁹ = 531441 / 524288 = 1.0136432647705078, log2(1.0136432647705078) = 0.019550008653874178, 1200 * log2() = 23.460010384649014
        s5s          = self.stck5ths(n, 0)
        a, ca, m, _  = s5s[i]   ;   b = 2
        r, cb        = self.ac2r(a, ca)
        if dbg:      slog(f'{n} 5ths, s5s     = {fmtl(s5s)}')
        if dbg:      slog(f'{n} 5ths, s5s[{i}] = {fmtl(s5s[i])} {ca=} {cb=} {r=:10.8}')
        assert [a, b, ca] == [3, 2, n],  f'{a=} {b=} {ca=} {[3, 2, n]}'
        pa, pb       = a ** abs(ca), b ** abs(cb)
        cratio       = pa / pb
        q            = f'{a}{self.i2spr(ca)}/{b}{self.i2spr(cb)}'
        ccents       = self.r2cents(cratio)
        if dbg:      slog(f'Comma = {pa:6}/{pb:<6} = {a}**{ca}/{b}**{cb} = {q:6} = {cratio:10.8f} = {ccents:10.5f} cents')
        ecents       = ccents / NT
        if dbg:      slog(f'Epsilon = Comma / {NT} = {ccents:10.5f} / {NT} = {ecents:10.5f} cents')
        return ccents
    ####################################################################################################################################################################################################
    def dmpNiMap(self, ni, x, upd=0, dbg=1): # x=13 or x=9 #todo generalize m2bc ?
        mm, nn, oo, ff = (Y, Y, Y, 3) if self.csv else (W, Z, '|', 1)  ;  ww, _ = f'^{x}', W*x  ;    yy = 6 if x==13 else 4
        pfx, pfx2 = Z, f'{mm}  k  {mm}{nn} {nn}'   ;   sfx = f'{nn}]'   ;   f0 = self.FREFS[self.j] #  ;   w2 = '7.2f'
        if dbg and ni==0:  self.dmpIndices(pfx2, x)   ;   self.dmpDataTableLine(x+1)
        for i, (kk, v) in enumerate(self.nimap.items()):
            rat0, rat2, rat3, cents, cfnts = [], [], [], [], []    ;    cki = -1   ;   self.k = kk
            rat1 = [] if x in (6, 7, 13) else None    ;   ratA = [] if x == 9 else None   ;   ratB = [] if x == 9 else None
            for j, e in enumerate(v[2]):
                n    = v[1][0][-1]  ;  a, ca, b, cb = e  ;  pa, pb = a ** abs(ca), b ** abs(cb)  ;  pd = [f'{i:x}', f'{kk:2}', f'{n:2}'] if dbg else [f'{i:x}', f'{kk:2}  ']
                pfx  = f'{mm.join(pd)}{nn}[{nn}' if dbg else pfx     ;     sfx = f' {nn}{n:2}' if not dbg else sfx
                cent = self.r2cents(pa/pb if pa>=pb else pb/pa)    ;   rc = round(cent)   ;    cki += 1
                assert rc in self.ckmap,  f'{rc=} {i=} {kk=} {j=} {n=} {pa=} {pb=} {e=} {rat0[i]} {rat2[i]} {rat3[i]} {fmtl(list(self.ckmap.keys()))}'
                if not dbg and upd and ni == 4:   self.updCkMap(rc, self.ckmap, n if kk==self.j else W*2, f0*pa/pb if pa>=pb else f0*pb/pa, e, cent, j)
                while cki < len(self.centKs) and self.centKs[cki] < rc:
                    rat0.append(_)   ;  rat2.append(_)   ;   rat3.append(_)    ;    cki += 1    ;  cents.append(_) #  ;   cfnts.append(_)
                    rat1.append(_) if x==13 else None    ;   ratA.append(_) if x==9 else None   ;   ratB.append(_) if x==9 else None
                cents.append(rc) #  ;   cfnts.append(f'{cent:{w2}}')
                if   x==9:          self.addFmtRs(a, ca, b, cb, rs=[rat0, ratA, ratB, rat2, rat3], u=yy, w=x,     i=i, j=j)
                elif x==13:         self.addFmtRs(a, ca, b, cb, rs=[rat0,       rat1, rat2, rat3], u=yy, w=x,     i=i, j=j)
                elif x in (6, 7):   self.addFmtRs(a, ca, b, cb, rs=[rat0,       rat1, rat2, rat3], u=yy, w=x,     i=i, j=j)
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
    def dmpCkMap(self, u=9, o=0, dbg=1): #todo generalize m2bc ? #fixme reusing arg o ! # ckmap[498,588,612,702][Note] = F,Gb, F#,G
        mm, nn, oo, ff = (Y, Y, Y, 3) if self.csv else (W, Z, '|', 1)  ;  f0, v, ww, y = self.FREFS[self.j], Z, f'^{u}', 4  ;  _ = u*W if dbg else 7*W  ;  cks = self.centKs if dbg else None
        ns, fs, ws, vs = [], [], [], []   ;   cs, ds, qs, ks, cksi = [], [], [], [], []  ;  r0s, rAs, rBs, r1s, r2s, r3s = [], [], [], [], [], []   ;   f1 = 0
        sfx = f'{nn}]'  ;  sfxc = f'{nn}]{mm}cents'  ;  sfxf = f'{nn}]{mm}Hz'  ;  sfxw = f'{nn}]{mm}cm'  ;  ckmap = self.ckmap if dbg else self.nimap[self.j][0]
        for i, ck in enumerate(self.centKs):
            ival = self.ck2ikm[ck]    ;    vs.append(ival)    ;   assert ckmap and ck in ckmap,  f'{self.j=} {i=} {ival=} {ck=} {ckmap=} {self.ckmap=} {self.nimap[self.j][0]=} {dbg=}'
            if ckmap[ck]['Count'] > 0:
                assert ival == ckmap[ck]['Ival'],  f'{ival=} {ck=} {ckmap[ck]["Ival"]=}'    ;   a, ca, b, cb = ckmap[ck]['Abcd']   ;   q = self.fdvdr(a, ca, b, cb)
                self.addFmtRs(              a, ca, b, cb, rs=[r0s, rAs, rBs, r1s, r2s, r3s], u=y, w=u if dbg else 7,     i=i, j=ck)
                f, w, n, c, d, k, i2         = self.getCkMapVal(ckmap, ck, a, ca, b, cb, f0, self.w0)
                n, m = self.f2nPair(f, b=1, o=0, e=1)   ;   assert m != n,  f'{i=} {ck=} {m=} {n=} {c=} {d=} {k=} {i2=} {f=} {w=}'
                o    = n
                if m:
                    if   m not in self.COFM[self.n]:   n = n + '/' + m
                    elif f1:                           n = m
                    else:                             f1 = 1
                self.k = N2I[n[:2]] + 48 if n in N2I else self.k   ;   self.o = n[:2] if n in Notes.N2I else self.o
                cksi.append(int(round(c)))  ;  cs.append(f'{fmtf(c, u-4)}')   ; ds.append(f'{fmtf(d, u-4)}') ; fs.append(f'{fmtf(f, u-2)}') ; ws.append(f'{fmtf(w, u-2)}')
            else:  n, d, k, q = _, _, 0, Z  ;  cksi.append(ck) ; cs.append(_) ; ds.append(_) ; fs.append(_)  ; ws.append(_) ; r0s.append(_) ; rAs.append(_) ; rBs.append(_) ; r2s.append(_) ; r3s.append(_)
            if dbg:
                ns.append(n)  ;  ks.append(k)  ;  qs.append(q)
                self.dmpIvals(i, cksi, ks)
        if dbg:
            self.dmpIvals2(0)   ;   self.dmpIvals2(1) # (len(self.ck2ikm)-1, cksi, ks)
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
            a, ca  = abc[0], abc[1]     ;   b = 2
            r, cb  = self.ac2r(a, ca)
            pa, pb = a ** abs(ca), b ** abs(cb)
            if pb > pa:   pa, pb = pb, pa
            aa.append(pa)     ;    bb.append(pb)
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
            a, b, ca = abc[0], abc[1], abc[2]
            r, cb = self.ac2r(a, ca)
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
        ca = abs(ca)   ;   cb = abs(cb)
        pa = a ** ca   ;  pb = b ** cb   ;   p = pa/pb if pa > pb else pb/pa if pb/pa else 1/0
        f = ckmap[ck]['Freq']    ;   assert round(f, 10) == round(f0*p, 10),    f'{ck=} {f=} {f0=} p={a**ca/b**cb} {f0*a**ca/b**cb=} {a=} {ca=} {b=} {cb=}' #todo remove round() hack! use Decimal
        w = ckmap[ck]['Wavln']   ;   assert w == w0 / f,                        f'{w=} {w0=} {f=}'
        n = ckmap[ck]['Note']
        i = ckmap[ck]['Index']
        k = ckmap[ck]['Count']
        c = ckmap[ck]['Cents']   ;   assert c == self.r2cents(p),  f'{c=} {self.r2cents(p)=} {p=}'
        d = ckmap[ck]['DCent']   ;   assert d == self.i2dCent(c),  f'{d=} {self.i2dCent(c)=}'    ;    d = round(d, 2)
        return f, w, n, c, d, k, i # todo assume callers do not want ckmap[ck]['Abcd'] value returned
    ####################################################################################################################################################################################################
    def fIvals(self, data, n): # todo move to base class
        mm, nn, zz = (Y, Y, W) if self.csv else (W, Z, Z)   ;   fd = []
        for j, d in enumerate(data): # j j*100 i | Note  Ival  Qty Cent | Note  Ival  Qty CentK   | Note  Ival  Qty CentK   | Note  Ival  Qty CentK
            if   j==0:                fd.append(f'{d:x}{zz} ') # j
            elif j==1:                fd.append(f'{zz}{d:4}{zz} ') # j*100
            elif j==2:                fd.append(f'{d:2}')        # i
            elif j in (3,  6, 9, 12): fd.append(f'|{nn} {self.iv2n(n, d):5}{mm} {d:5}') # Note Iv
            elif j in (4, 7, 10, 13): fd.append(f'{d:2}{zz} ')       # Qty
            elif j in (5, 8, 11, 14): fd.append(f'{d:5}{zz}')        # Cent
        return fd

    def cofi(self, a, b):
        if a > b:                 a, b = b, a
        m = len(self.COF_)//2  ;  return self.COF_[m+a:m+b+1]
#  0   +1   +2    +3    +4    +5     +6    +7    +8    +9     +10    +11    +12     +13    +14   +15     +16     +17     +18     +19     +20     +21     +22     +23      +24      +25      +26     +27      +28      +29      +30       +31       +32       +33       +34
#['C', 'G', 'D',  'A',  'E',  'B',  'F♯', 'C♯', 'G♯', 'D♯',  'A♯',  'E♯',  'B♯',  'F♯♯', 'C♯♯', 'G♯♯', 'D♯♯',  'A♯♯',  'E♯♯',  'B♯♯',  'F♯♯♯', 'C♯♯♯', 'G♯♯♯', 'D♯♯♯',  'A♯♯♯',  'E♯♯♯',  'B♯♯♯',  'F♯♯♯♯', 'C♯♯♯♯', 'G♯♯♯♯', 'D♯♯♯♯',  'A♯♯♯♯',  'E♯♯♯♯',  'B♯♯♯♯',  'F♯♯♯♯♯']
#[     'F', 'B♭', 'E♭', 'A♭', 'D♭', 'G♭', 'C♭', 'F♭', 'B♭♭', 'E♭♭', 'A♭♭', 'D♭♭', 'G♭♭', 'C♭♭', 'F♭♭', 'B♭♭♭', 'E♭♭♭', 'A♭♭♭', 'D♭♭♭', 'G♭♭♭', 'C♭♭♭', 'F♭♭♭', 'B♭♭♭♭', 'E♭♭♭♭', 'A♭♭♭♭', 'D♭♭♭♭', 'G♭♭♭♭', 'C♭♭♭♭', 'F♭♭♭♭', 'B♭♭♭♭♭', 'E♭♭♭♭♭', 'A♭♭♭♭♭', 'D♭♭♭♭♭', 'G♭♭♭♭♭']
#      -1    -2    -3    -4    -5    -6    -7    -8    -9     -10    -11   -12     -13    -14   -15     -16     -17     -18     -19     -20     -21     -22     -23      -24      -25      -26     -27       -28      -29      -30       -31       -32       -33       -34
    def NEW__iv2n(self, n, iv):
        m = n[0]
        match iv:
            case 'P1':  nn = nextN(m, 1)  ;  e = '♭' if n in self.cofi( -2,  -6) else '♯'  if n in self.cofi(  6,   6) else Z
            case 'm2':  nn = nextN(m, 2)  ;  e = '♭' if n in self.cofi(  3,  -3) else '♭♭' if n in self.cofi( -4,  -6) else Z
            case 'M2':  nn = nextN(m, 2)  ;  e = '♭' if n in self.cofi( -4,  -6) else '♯'  if n in self.cofi(  4,   6) else Z
            case 'm3':  nn = nextN(m, 3)  ;  e = '♭' if n in self.cofi( -5,   1) else '♭♭' if n in self.cofi( -6,  -6) else Z
            case 'M3':  nn = nextN(m, 3)  ;  e = '♭' if n in self.cofi( -6,  -6) else '♯'  if n in self.cofi(  2,   6) else Z
            case 'P4':  nn = nextN(m, 4)  ;  e = '♭' if n in self.cofi( -1,  -6) else Z
            case 'A4':  nn = nextN(m, 4)  ;  e = '♯' if n in self.cofi(  0,   6) else Z
            case 'P5':  nn = nextN(m, 5)  ;  e = '♭' if n in self.cofi( -3,  -6) else '♯'  if n in self.cofi(  5,   6) else Z
            case 'm6':  nn = nextN(m, 6)  ;  e = '♭' if n in self.cofi(  2,  -4) else '♭♭' if n in self.cofi( -5,  -6) else Z
            case 'M6':  nn = nextN(m, 6)  ;  e = '♭' if n in self.cofi( -5,  -6) else '♯'  if n in self.cofi(  3,   6) else Z
            case 'm7':  nn = nextN(m, 7)  ;  e = '♭' if n in self.cofi(  0,  -6) else Z
            case 'M7':  nn = nextN(m, 7)  ;  e = '♯' if n in self.cofi(  1,   6) else Z
            case 'P8':  nn = nextN(m, 8)  ;  e = '♭' if n in self.cofi( -2,  -6) else '♯'  if n in self.cofi(  6,   6) else Z
            
            case 'd2':  nn = nextN(m, 2)  ;  e = '♯' if n in self.cofi(  7,  12) else '♭♭' if n in self.cofi( -9, -12) else Z
            case 'd3':  nn = nextN(m, 3)  ;  e = '♭' if n in self.cofi( -7, -10) else '♯'  if n in self.cofi(  6,  10) else '♭♭'  if n in self.cofi(-11, -12) else '♯♯'  if n in self.cofi( 11,  12) else Z
            case 'd4':  nn = nextN(m, 4)  ;  e = '♭' if n in self.cofi( -7, -12) else '♯'  if n in self.cofi(  7,   8) else '♯♯'  if n in self.cofi(  9,  12) else Z
            case 'd5':  nn = nextN(m, 5)  ;  e = '♭' if n in self.cofi( -8, -12) else '♯♯' if n in self.cofi(  7,  12) else Z
            case 'd6':  nn = nextN(m, 6)  ;  e = '♭' if n in self.cofi( -7,  -9) else '♯'  if n in self.cofi(  7,  11) else '♭♭' if n in self.cofi(-10, -12) else '♯♯'  if n in self.cofi( 12,  12) else Z
            case 'd7':  nn = nextN(m, 7)  ;  e = '♭' if n in self.cofi( -7, -11) else '♯'  if n in self.cofi(  7,   9) else '♭♭' if n in self.cofi(-12, -12) else '♯♯'  if n in self.cofi( 10,  12) else Z
            case 'd8':  nn = nextN(m, 8)  ;  e = '♭' if n in self.cofi( -7, -12) else '♯'  if n in self.cofi(  7,   7) else '♯♯' if n in self.cofi(  8,  12) else Z
            case 'A1':  nn = nextN(m, 1)  ;  e = '♯' if n in self.cofi( 11,  12) else '♭♭' if n in self.cofi( -7, -10) else '♭♭♭' if n in self.cofi(-11, -12) else Z
            case 'A2':  nn = nextN(m, 2)  ;  e = '♯' if n in self.cofi(  9,  12) else '♭♭' if n in self.cofi( -7, -12) else Z
            case 'A3':  nn = nextN(m, 3)  ;  e = '♭' if n in self.cofi( -7,  -7) else '♯'  if n in self.cofi(  7,  12) else '♭♭' if n in self.cofi( -8, -12) else Z
            case 'A4':  nn = nextN(m, 4)  ;  e = '♯' # ?
            case 'A5':  nn = nextN(m, 5)  ;  e = '♯' if n in self.cofi( 10,  12) else '♭♭' if n in self.cofi( -7, -11) else '♭♭♭' if n in self.cofi(-12, -12) else Z
            case 'A6':  nn = nextN(m, 6)  ;  e = '♯' if n in self.cofi(  8,  12) else '♭♭' if n in self.cofi( -7, -12) else Z
            case 'A7':  nn = nextN(m, 7)  ;  e = '♭' if n in self.cofi( -7,  -8) else '♯'  if n in self.cofi(  7,  12) else '♭♭' if n in self.cofi( -9, -12) else Z
            case _:     nn = nextN(m, 1)  ;  e = '??'
        return nn + e
    
    def iv2n(self, n, iv):
        m = n[0]
        match iv:
            case 'P1':  nn = nextN(m, 1)  ;  e = '♭' if n in self.cofi( -2,  -8) else '♯' if n in self.cofi(  6,  12) else '♭♭' if n in self.cofi( -9, -12) else Z
            case 'm2':  nn = nextN(m, 2)  ;  e = '♭' if n in self.cofi(  3,  -3) else '♯' if n in self.cofi( 11,  12) else '♭♭' if n in self.cofi( -4, -10) else '♭♭♭' if n in self.cofi(-11, -12) else Z
            case 'M2':  nn = nextN(m, 2)  ;  e = '♭' if n in self.cofi( -4, -10) else '♯' if n in self.cofi(  4,  10) else '♭♭' if n in self.cofi(-11, -12) else '♯♯'  if n in self.cofi( 11,  12) else Z
            case 'm3':  nn = nextN(m, 3)  ;  e = '♭' if n in self.cofi( -5,   1) else '♯' if n in self.cofi(  9,  12) else '♭♭' if n in self.cofi( -6, -12) else Z
            case 'M3':  nn = nextN(m, 3)  ;  e = '♭' if n in self.cofi( -6, -12) else '♯' if n in self.cofi(  2,   8) else '♯♯' if n in self.cofi(  9,  12) else Z
            case 'P4':  nn = nextN(m, 4)  ;  e = '♭' if n in self.cofi( -1,  -7) else '♯' if n in self.cofi(  7,  12) else '♭♭' if n in self.cofi( -8, -12) else Z
            case 'A4':  nn = nextN(m, 4)  ;  e = '♭' if n in self.cofi( -8, -12) else '♯' if n in self.cofi(  0,   6) else '♯♯' if n in self.cofi(  7,  12) else Z
            case 'P5':  nn = nextN(m, 5)  ;  e = '♭' if n in self.cofi( -3,  -9) else '♯' if n in self.cofi(  5,  11) else '♭♭' if n in self.cofi(-10, -12) else '♯♯'  if n in self.cofi( 12,  12) else Z
            case 'm6':  nn = nextN(m, 6)  ;  e = '♭' if n in self.cofi(  2,  -4) else '♯' if n in self.cofi( 10,  12) else '♭♭' if n in self.cofi( -5, -11) else '♭♭♭' if n in self.cofi(-12, -12) else Z
            case 'M6':  nn = nextN(m, 6)  ;  e = '♭' if n in self.cofi( -5, -11) else '♯' if n in self.cofi(  3,   9) else '♭♭' if n in self.cofi(-12, -12) else '♯♯'  if n in self.cofi( 10,  12) else Z
            case 'm7':  nn = nextN(m, 7)  ;  e = '♭' if n in self.cofi(  0,  -6) else '♯' if n in self.cofi(  8,  12) else '♭♭' if n in self.cofi( -7, -12) else Z
            case 'M7':  nn = nextN(m, 7)  ;  e = '♭' if n in self.cofi( -7, -12) else '♯' if n in self.cofi(  1,   7) else '♯♯' if n in self.cofi(  8,  12) else Z
            case 'P8':  nn = nextN(m, 8)  ;  e = '♭' if n in self.cofi( -2,  -8) else '♯' if n in self.cofi(  6,  12) else '♭♭' if n in self.cofi( -9, -12) else Z
            case 'd2':  nn = nextN(m, 2)  ;  e = '♭♭'
            case 'd3':  nn = nextN(m, 3)  ;  e = '♭♭'
            case 'd4':  nn = nextN(m, 4)  ;  e = '♭'
            case 'd5':  nn = nextN(m, 5)  ;  e = '♭' # ?
            case 'd6':  nn = nextN(m, 6)  ;  e = '♭♭'
            case 'd7':  nn = nextN(m, 7)  ;  e = '♭♭'
            case 'd8':  nn = nextN(m, 8)  ;  e = '♭'
            case 'A1':  nn = nextN(m, 1)  ;  e = '♯'
            case 'A2':  nn = nextN(m, 2)  ;  e = '♯'
            case 'A3':  nn = nextN(m, 3)  ;  e = '♯'
            case 'A4':  nn = nextN(m, 4)  ;  e = '♯' # ?
            case 'A5':  nn = nextN(m, 5)  ;  e = '♯'
            case 'A6':  nn = nextN(m, 6)  ;  e = '♯'
            case 'A7':  nn = nextN(m, 7)  ;  e = '♯'
            case _:     nn = nextN(m, 1)  ;  e = '??'
        return nn + e

    def dmpIvals(self, h, ks, cs): # todo move to base class, but epsilon is an issue
        mm, nn, oo, ff = (Y, Y, Y, 3) if self.csv else (W, Z, '|', 1)   ;   i, j, k = h-1, h-2, h-3    ;   nns = 1
        l = h//2   ;   hdrA = ['j ', ' j*100 ', ' i ']   ;  data = []   ;   hs = []
        m  = l # l-1 if h>=23 else l # m = l-6 if h>=34 else l-5 if h>=28 else l-4 if h>=22 else l-3 if h>=16 else l-2 if h>=10 else l-1 if h>=4 else l
        hdrB1  = [f'|{mm}Note{mm}  Ival ', ' Qty ', ' Cent ']
        hdrB2  = [f'|{mm}Note{mm}  Ival ', ' Qty ', ' Cent ']
        hdrs   = hdrA   ;   hdrs.extend(hdrB1)   ;   hdrs.extend(hdrB1)   ;   hdrs.extend(hdrB1)   ;   hdrs.extend(hdrB2)
        if   h > 2:   w, x, y, z = self.ck2ikm[ks[h]], self.ck2ikm[ks[i]], self.ck2ikm[ks[j]], self.ck2ikm[ks[k]]
        elif h > 1:   w, x, y, z = self.ck2ikm[ks[h]], self.ck2ikm[ks[i]], self.ck2ikm[ks[j]], None
        elif h > 0:   w, x, y, z = self.ck2ikm[ks[h]], self.ck2ikm[ks[i]], None,               None
        else:         w, x, y, z = self.ck2ikm[ks[h]], None,               None,               None
        if   h == 0:   slog(f'{fmtl(hdrs, s=nn, d=Z)}', p=0, f=ff)
        if nns == 0:
            if   h ==  0: hs.append(h) ; data = [m, m * 100, h, x, cs[i], ks[i]]
            elif h ==  1: hs.append(h) ; data = [m, m * 100, h, x, cs[i], ks[i]]
            elif h ==  2: hs.append(h) ; data = [m, m * 100, h, x, cs[i], ks[i]]
            elif h ==  3: hs.append(h) ; data = [m, m * 100, h, x, cs[i], ks[i]]
            elif h ==  4: hs.append(h) ; data = [m, m * 100, h, x, cs[i], ks[i]]
            elif h ==  5: hs.append(h) ; data = [m, m * 100, h, x, cs[i], ks[i]]
            elif h ==  6: hs.append(h) ; data = [m, m * 100, h, x, cs[i], ks[i]]
            elif h ==  7: hs.append(h) ; data = [m, m * 100, h, x, cs[i], ks[i]]
            elif h ==  8: hs.append(h) ; data = [m, m * 100, h, x, cs[i], ks[i]]
            elif h ==  9: hs.append(h) ; data = [m, m * 100, h, x, cs[i], ks[i]]
            elif h == 10: hs.append(h) ; data = [m, m * 100, h, x, cs[i], ks[i]]
            elif h == 11: hs.append(h) ; data = [m, m * 100, h, x, cs[i], ks[i]]
            elif h == 12: hs.append(h) ; data = [m, m * 100, h, x, cs[i], ks[i]]
        elif nns == 1:
            if   h ==  1: hs.append(h) ; data = [m, m * 100, h, x, cs[i], ks[i], w, cs[h], ks[h]]
            elif h ==  3: hs.append(h) ; data = [m, m * 100, h, x, cs[i], ks[i], w, cs[h], ks[h]]
            elif h ==  5: hs.append(h) ; data = [m, m * 100, h, w, cs[h], ks[h], x, cs[i], ks[i]]
            elif h ==  7: hs.append(h) ; data = [m, m * 100, h, x, cs[i], ks[i], w, cs[h], ks[h]]
            elif h ==  9: hs.append(h) ; data = [m, m * 100, h, w, cs[h], ks[h], x, cs[i], ks[i]]
            elif h == 11: hs.append(h) ; data = [m, m * 100, h, x, cs[i], ks[i], w, cs[h], ks[h]]
            elif h == 13: hs.append(h) ; data = [m, m * 100, h, w, cs[h], ks[h], x, cs[i], ks[i]]
            elif h == 15: hs.append(h) ; data = [m, m * 100, h, w, cs[h], ks[h], x, cs[i], ks[i]]
            elif h == 17: hs.append(h) ; data = [m, m * 100, h, x, cs[i], ks[i], w, cs[h], ks[h]]
            elif h == 19: hs.append(h) ; data = [m, m * 100, h, w, cs[h], ks[h], x, cs[i], ks[i]]
            elif h == 21: hs.append(h) ; data = [m, m * 100, h, x, cs[i], ks[i], w, cs[h], ks[h]]
            elif h == 23: hs.append(h) ; data = [m, m * 100, h, w, cs[h], ks[h], x, cs[i], ks[i]]
            elif h == 25: hs.append(h) ; data = [m, m * 100, h, w, cs[h], ks[h], x, cs[i], ks[i]]
        elif nns == 2:
            if   h ==  1: hs.append(h) ; data = [m, m * 100, h, x, cs[i], ks[i], w, cs[h], ks[h]]
            elif h ==  4: hs.append(h) ; data = [m, m * 100, h, x, cs[i], ks[i], w, cs[h], ks[h], y, cs[j], ks[j]]
            elif h ==  7: hs.append(h) ; data = [m, m * 100, h, x, cs[i], ks[i], y, cs[j], ks[j], w, cs[h], ks[h]]
            elif h == 10: hs.append(h) ; data = [m, m * 100, h, x, cs[i], ks[i], w, cs[h], ks[h], y, cs[j], ks[j]]
            elif h == 13: hs.append(h) ; data = [m, m * 100, h, x, cs[i], ks[i], y, cs[j], ks[j], w, cs[h], ks[h]]
            elif h == 16: hs.append(h) ; data = [m, m * 100, h, x, cs[i], ks[i], w, cs[h], ks[h], y, cs[j], ks[j]]
            elif h == 19: hs.append(h) ; data = [m, m * 100, h, w, cs[h], ks[h], x, cs[i], ks[i], y, cs[j], ks[j]]
            elif h == 22: hs.append(h) ; data = [m, m * 100, h, x, cs[i], ks[i], y, cs[j], ks[j], w, cs[h], ks[h]]
            elif h == 25: hs.append(h) ; data = [m, m * 100, h, x, cs[i], ks[i], w, cs[h], ks[h], y, cs[j], ks[j]]
            elif h == 28: hs.append(h) ; data = [m, m * 100, h, x, cs[i], ks[i], y, cs[j], ks[j], w, cs[h], ks[h]]
            elif h == 31: hs.append(h) ; data = [m, m * 100, h, x, cs[i], ks[i], w, cs[h], ks[h], y, cs[j], ks[j]]
            elif h == 34: hs.append(h) ; data = [m, m * 100, h, x, cs[i], ks[i], y, cs[j], ks[j], w, cs[h], ks[h]]
            elif h == 37: hs.append(h) ; data = [m, m * 100, h, w, cs[h], ks[h], x, cs[i], ks[i]]
        elif nns == 3:
            pass
        if   h in hs:
            fd = self.fIvals(data, self.n)
            slog(f'{fmtl(fd, s=mm, d=Z)}', p=0, f=ff)

    def NEW__dmpIvals(self, h, ks,cs): # todo move to base class, but epsilon is an issue
        mm, nn, oo, ff = (Y, Y, Y, 3) if self.csv else (W, Z, '|', 1)
        hdrA  = ['j', 'j*100', 'i ']   ;   l = math.floor(h/2)  ;  data = []
        hdrB1 = ['| Note  Iv', f'   c{mm} ', f'  k{mm}']
        hdrB2 = ['| Note  Iv', f'   c{mm} ', f'  k{mm}']
        hdrs  = hdrA   ;   hdrs.extend(hdrB1)   ;   hdrs.extend(hdrB1)   ;   hdrs.extend(hdrB1)    ;   hdrs.extend(hdrB2)
        w = self.ck2ikm[ks[h]]  ;   x = self.ck2ikm[ks[h-1]]   ;   y = self.ck2ikm[ks[h-2]]
        if   h == 0:   slog(f'{fmtl(hdrs, s=mm, d=Z)}', p=0, f=ff)
        elif h == 12: data = [l, l * 100, h, w, cs[h], ks[h]]
        elif h == 25: data = [l, l * 100, h, w, cs[h], ks[h], x, cs[h-1], ks[h-1]]
        elif h == 37: data = [l, l * 100, h, w, cs[h], ks[h], x, cs[h-1], ks[h-1], y, cs[h-2], ks[h-2]]
        fd = self.fIvals(data, self.n)
        slog(f'{fmtl(fd, s=mm, d=Z)}', p=0, f=ff)

    def dmpIvals2(self, i): # for j in range(6, -7, -1): for j in range(12, 6, -1): for j in range(-7, -13, -1):
        mm, nn, oo, ff, zz = (Y, Y, Y, 3, W) if self.csv else (W, Z, '|', 1, Z)   ;   m = 12
        ivs  = list(I4V.values())
        if i == 0:  n1s, n2s = reversed(self.COF1[:m+1]), self.COF2[:m]
        else:       n1s, n2s = self.COF1[:m+1], reversed(self.COF2[:m])
        hdr = f'   {zz}{fmtl(ivs, w=5, s=mm, d=Z)}'
        slog(p=0, f=ff)   ;   slog(f'  {hdr}', p=0, f=ff)
        for j, n in enumerate(n1s if i==0 else n2s):
            notes = []
            for k, v in I4V.items():
                note = self.iv2n(n, v)
                notes.append(note)
            if i == 0:        slog(f'{m-j:3}{mm} {fmtl(notes, w=5, d=Z, s=mm)}', p=0, f=ff)
            else:             slog(f'{j-m:3}{mm} {fmtl(notes, w=5, d=Z, s=mm)}', p=0, f=ff)
        for j, n in enumerate(n2s if i==0 else n1s):
            notes = []
            for k, v in I4V.items():
                note = self.iv2n(n, v)
                notes.append(note)
            if i == 0:        slog(f'{-j-1:3}{mm} {fmtl(notes, w=5, d=Z, s=mm)}', p=0, f=ff)
            else:             slog(f'{  j :3}{mm} {fmtl(notes, w=5, d=Z, s=mm)}', p=0, f=ff)
'''
j  j*100  i | Note   Ival  Qty  Cent | Note   Ival  Qty  Cent | Note   Ival  Qty  Cent | Note   Ival  Qty  Cent 
0     0   1 | C      P1     1      0 | D      d2     0     23
1   100   3 | D♭     m2     1     90 | C      A1     0    114
2   200   5 | D      M2     1    204 | E      d3     0    180
3   300   7 | E♭     m3     1    294 | D      A2     0    318
4   400   9 | E      M3     1    408 | F      d4     0    384
5   500  11 | F      P4     1    498 | E      A3     0    522
6   600  13 | F♯     A4     1    612 | G      d5     1    588
7   700  15 | G      P5     1    702 | A      d6     0    678
8   800  17 | A♭     m6     1    792 | G      A5     0    816
9   900  19 | A      M6     1    906 | B      d7     0    882
a  1000  21 | B♭     m7     1    996 | A      A6     0   1020
b  1100  23 | B      M7     1   1110 | C      d8     0   1086
c  1200  25 | C      P8     1   1200 | B      A7     0   1177

     P1    m2    M2    m3    M3    P4    A4    P5    m6    M6    m7    M7    P8   
  6  F♯    G     G♯    A     A♯    B     B♯    C♯    D     D♯    E     E♯    F♯   
  5  B     C     C♯    D     D♯    E     E♯    F♯    G     G♯    A     A♯    B    
  4  E     F     F♯    G     G♯    A     A♯    B     C     C♯    D     D♯    E    
  3  A     B♭    B     C     C♯    D     D♯    E     F     F♯    G     G♯    A    
  2  D     E♭    E     F     F♯    G     G♯    A     B♭    B     C     C♯    D    
  1  G     A♭    A     B♭    B     C     C♯    D     E♭    E     F     F♯    G    
  0  C     D♭    D     E♭    E     F     F♯    G     A♭    A     B♭    B     C    
 -1  F     G♭    G     A♭    A     B♭    B     C     D♭    D     E♭    E     F    
 -2  B♭    C♭    C     D♭    D     E♭    E     F     G♭    G     A♭    A     B♭   
 -3  E♭    F♭    F     G♭    G     A♭    A     B♭    C♭    C     D♭    D     E♭   
 -4  A♭    B♭♭   B♭    C♭    C     D♭    D     E♭    F♭    F     G♭    G     A♭   
 -5  D♭    E♭♭   E♭    F♭    F     G♭    G     A♭    B♭♭   B♭    C♭    C     D♭   
 -6  G♭    A♭♭   A♭    B♭♭   B♭    C♭    C     D♭    E♭♭   E♭    F♭    F     G♭   

     P1    m2    M2    m3    M3    P4    A4    P5    m6    M6    m7    M7    P8   
 -6  G♭    A♭♭   A♭    B♭♭   B♭    C♭    C     D♭    E♭♭   E♭    F♭    F     G♭   
 -5  D♭    E♭♭   E♭    F♭    F     G♭    G     A♭    B♭♭   B♭    C♭    C     D♭   
 -4  A♭    B♭♭   B♭    C♭    C     D♭    D     E♭    F♭    F     G♭    G     A♭   
 -3  E♭    F♭    F     G♭    G     A♭    A     B♭    C♭    C     D♭    D     E♭   
 -2  B♭    C♭    C     D♭    D     E♭    E     F     G♭    G     A♭    A     B♭   
 -1  F     G♭    G     A♭    A     B♭    B     C     D♭    D     E♭    E     F    
  0  C     D♭    D     E♭    E     F     F♯    G     A♭    A     B♭    B     C    
  1  G     A♭    A     B♭    B     C     C♯    D     E♭    E     F     F♯    G    
  2  D     E♭    E     F     F♯    G     G♯    A     B♭    B     C     C♯    D    
  3  A     B♭    B     C     C♯    D     D♯    E     F     F♯    G     G♯    A    
  4  E     F     F♯    G     G♯    A     A♯    B     C     C♯    D     D♯    E    
  5  B     C     C♯    D     D♯    E     E♯    F♯    G     G♯    A     A♯    B    
  6  F♯    G     G♯    A     A♯    B     B♯    C♯    D     D♯    E     E♯    F♯   

j  j*100  i | Note   Ival  Qty  Cent | Note   Ival  Qty  Cent | Note   Ival  Qty  Cent | Note   Ival  Qty  Cent 
0     0   1 | C      P1     1      0 | D♭♭    d2     0     23
1   100   3 | D♭     m2     1     90 | C♯     A1     0    114
2   200   5 | D      M2     1    204 | E♭♭    d3     0    180
3   300   7 | E♭     m3     1    294 | D♯     A2     0    318
4   400   9 | E      M3     1    408 | F♭     d4     0    384
5   500  11 | F      P4     1    498 | E♯     A3     0    522
6   600  13 | F♯     A4     1    612 | G♭     d5     1    588
7   700  15 | G      P5     1    702 | A♭♭    d6     0    678
8   800  17 | A♭     m6     1    792 | G♯     A5     0    816
9   900  19 | A      M6     1    906 | B♭♭    d7     0    882
a  1000  21 | B♭     m7     1    996 | A♯     A6     0   1020
b  1100  23 | B      M7     1   1110 | C♭     d8     0   1086
c  1200  25 | C      P8     1   1200 | B♯     A7     0   1177
   P1    m2    M2    m3    M3    P4    A4    P5    m6    M6    m7    M7    P8   
-7 C♭    D♭♭   D♭    E♭♭   E♭    F♭    F     G♭    A♭♭   A♭    B♭♭   B♭    C♭   
-6 G♭    A♭♭   A♭    B♭♭   B♭    C♭    C     D♭    E♭♭   E♭    F♭    F     G♭   
-5 D♭    E♭♭   E♭    F♭    F     G♭    G     A♭    B♭♭   B♭    C♭    C     D♭   
-4 A♭    B♭♭   B♭    C♭    C     D♭    D     E♭    F♭    F     G♭    G     A♭   
-3 E♭    F♭    F     G♭    G     A♭    A     B♭    C♭    C     D♭    D     E♭   
-2 B♭    C♭    C     D♭    D     E♭    E     F     G♭    G     A♭    A     B♭   
-1 F     G♭    G     A♭    A     B♭    B     C     D♭    D     E♭    E     F    
 0 C     D♭    D     E♭    E     F     F♯    G     A♭    A     B♭    B     C    
 1 G     A♭    A     B♭    B     C     C♯    D     E♭    E     F     F♯    G    
 2 D     E♭    E     F     F♯    G     G♯    A     B♭    B     C     C♯    D    
 3 A     B♭    B     C     C♯    D     D♯    E     F     F♯    G     G♯    A    
 4 E     F     F♯    G     G♯    A     A♯    B     C     C♯    D     D♯    E    
 5 B     C     C♯    D     D♯    E     E♯    F♯    G     G♯    A     A♯    B    
 6 F♯    G     G♯    A     A♯    B     B♯    C♯    D     D♯    E     E♯    F♯   
 7 C♯    D     D♯    E     E♯    F♯    F♯♯   G♯    A     A♯    B     B♯    C♯   

j j*100 i  | Note Iv  c     k       d       e        c`  | Note Iv  c     k       d       e        c`  | Note Iv  c     k       d       e        c`  | Note Iv  c     k       d       e        c`
0    0  1  | D♭   P1   1 @    0 :   0.000 = 1.955 *  0   | ?19? d2   0 @   23 :         = 1.955 *  1  
1  100  3  | D    m2   0 @   90 :         = 1.955 *  1   | D♭   A1   1 @  114 :  13.690 = 1.955 *  0  
2  200  5  | E♭   M2   1 @  204 :   3.910 = 1.955 *  0   | D    d3   0 @  180 :         = 1.955 *  1  
3  300  7  | E    m3   0 @  294 :         = 1.955 *  1   | E♭   A2   1 @  318 :  17.600 = 1.955 *  0  
4  400  9  | F    M3   1 @  408 :   7.820 = 1.955 *  0   | E    d4   0 @  384 :         = 1.955 *  1  
5  500 11  | F♯   P4   1 @  498 :  -1.960 = 1.955 *  1   | G♭   A3   1 @  522 :  21.510 = 1.955 *  1  
6  600 13  | G    A4   1 @  612 :  11.730 = 1.955 *  0   | F♯   d5   0 @  588 :         = 1.955 *  1  
7  700 15  | A♭   P5   1 @  702 :   1.960 = 1.955 *  0   | G    d6   0 @  678 :         = 1.955 *  1  
8  800 17  | A    m6   0 @  792 :         = 1.955 *  1   | A♭   A5   1 @  816 :  15.640 = 1.955 *  0  
9  900 19  | B♭   M6   1 @  906 :   5.870 = 1.955 *  0   | A    d7   0 @  882 :         = 1.955 *  1  
a 1000 21  | B    m7   0 @  996 :         = 1.955 *  1   | B♭   A6   1 @ 1020 :   5.870 = 1.955 *  1  
b 1100 23  | C    M7   1 @ 1110 :   9.780 = 1.955 *  0   | B    d8   0 @ 1086 :         = 1.955 *  1  
c 1200 25  | D♭   P8   1 @ 1200 :   0.000 = 1.955 *  0   | C    A7   0 @ 1177 :         = 1.955 *  1  
########################################################################################################################################################################################################
j j*100 i  |  Iv  c     k       d       e        c`  |  Iv  c     k       d       e        c`  |  Iv  c     k       d       e        c`  |  Iv  c     k       d       e        c`
0    0  1  |  P1  12 @    0 :   0.000 = 1.955 *  6   |  d2   6 @   23 :  23.460 = 1.955 * 12  
1  100  4  |  m2  12 @   90 :  -9.780 = 1.955 * 11   |  A1  11 @  114 :  13.690 = 1.955 * 12   |  dd3  2 @   67 : -33.240 = 1.955 * 12  
2  200  7  |  M2  12 @  204 :   3.910 = 1.955 *  4   |  d3   9 @  180 : -19.550 = 1.955 * 12   |  AA1  4 @  227 :  27.370 = 1.955 * 12  
3  300 10  |  m3  12 @  294 :  -5.870 = 1.955 *  9   |  A2   9 @  318 :  17.600 = 1.955 * 12   |  dd4  4 @  271 : -29.330 = 1.955 * 12  
4  400 13  |  M3  12 @  408 :   7.820 = 1.955 *  2   |  d4  11 @  384 : -15.640 = 1.955 * 12   |  AA2  2 @  431 :  31.280 = 1.955 * 12  
5  500 16  |  P4  12 @  498 :  -1.960 = 1.955 *  7   |  A3   7 @  522 :  21.510 = 1.955 *  6   |  dd5  6 @  475 : -25.420 = 1.955 * 12  
6  600 19  |  d5  12 @  612 :  11.730 = 1.955 * 12   |  A4  12 @  588 : -11.730 = 1.955 * 12   |  AA3  1 @  565 : -35.190 = 1.955 * 12  
7  700 22  |  P5  12 @  702 :   1.960 = 1.955 *  8   |  d6   8 @  678 : -21.510 = 1.955 *  5   |  AA4  5 @  725 :  25.420 = 1.955 * 12  
8  800 25  |  m6  12 @  792 :  -7.820 = 1.955 * 10   |  A5  10 @  816 :  15.640 = 1.955 * 12   |  dd7  3 @  769 : -31.280 = 1.955 * 12  
9  900 28  |  M6  12 @  906 :   5.870 = 1.955 *  3   |  d7  10 @  882 : -17.600 = 1.955 * 12   |  AA5  3 @  929 :  29.330 = 1.955 * 12  
a 1000 31  |  m7  12 @  996 :  -3.910 = 1.955 *  8   |  A6   8 @ 1020 : -27.370 = 1.955 *  5   |  dd8  5 @  973 : -27.370 = 1.955 * 12  
b 1100 34  |  M7  12 @ 1110 :   9.780 = 1.955 *  1   |  d8  12 @ 1086 : -13.690 = 1.955 * 12   |  AA6  1 @ 1133 :  33.240 = 1.955 * 12  
c 1200 36  |  P8  12 @ 1200 :   0.000 = 1.955 *  7   |  A7   7 @ 1177 : -23.460 = 1.955 * 12  

j j*100 i  |  Iv  c     k       d       e        c`  |  Iv  c     k       d       e        c`  |  Iv  c     k       d       e        c`  |  Iv  c     k       d       e        c`
0    0  1  |  P1  12 @    0 :   0.000 = 1.955 *  6   |  d2   6 @   23 :  23.460 = 1.955 * 12  
1  100  4  |  m2  12 @   90 :  -9.780 = 1.955 * 11   |  A1  11 @  114 :  13.690 = 1.955 * 12   |  dd3  2 @   67 : -33.240 = 1.955 * 12  
2  200  7  |  M2  12 @  204 :   3.910 = 1.955 *  4   |  d3   9 @  180 : -19.550 = 1.955 * 12   |  dd4  4 @  227 :  27.370 = 1.955 * 12  
3  300 10  |  m3  12 @  294 :  -5.870 = 1.955 *  9   |  A2   9 @  318 :  17.600 = 1.955 * 12   |  AA2  4 @  271 : -29.330 = 1.955 * 12  
4  400 13  |  M3  12 @  408 :   7.820 = 1.955 *  2   |  d4  11 @  384 : -15.640 = 1.955 * 12   |  AA2  2 @  431 :  31.280 = 1.955 * 12  
5  500 16  |  P4  12 @  498 :  -1.960 = 1.955 *  7   |  A3   7 @  522 :  21.510 = 1.955 *  6   |  dd5  6 @  475 : -25.420 = 1.955 * 12  
6  600 19  |  d5  12 @  612 :  11.730 = 1.955 * 12   |  A4  12 @  588 : -11.730 = 1.955 * 12   |  AA3  1 @  565 : -35.190 = 1.955 * 12  
8  800 22  |  P5  12 @  702 :   1.960 = 1.955 *  8   |  d6   8 @  678 : -21.510 = 1.955 *  5   |  AA4  5 @  725 :  25.420 = 1.955 * 12  
8  800 25  |  m6  12 @  792 :  -7.820 = 1.955 * 10   |  A5  10 @  816 :  15.640 = 1.955 * 12   |  dd7  3 @  769 : -31.280 = 1.955 * 12  
a 1000 28  |  M6  12 @  906 :   5.870 = 1.955 *  3   |  d7  10 @  882 : -17.600 = 1.955 * 12   |  AA5  3 @  929 :  29.330 = 1.955 * 12  
a 1000 31  |  m7  12 @  996 :  -3.910 = 1.955 *  8   |  A6   8 @ 1020 : -27.370 = 1.955 *  5   |  dd8  5 @  973 : -27.370 = 1.955 * 12  
c 1200 34  |  M7  12 @ 1110 :   9.780 = 1.955 *  1   |  d8  12 @ 1086 : -13.690 = 1.955 * 12   |  AA6  1 @ 1133 :  33.240 = 1.955 * 12  
d 1300 36  |  P8  12 @ 1200 :   0.000 = 1.955 *  7   |  A7   7 @ 1177 : -23.460 = 1.955 * 12  

j j*100 i  |  Iv  c     k       d       e        c`  |  Iv  c     k       d       e        c`  |  Iv  c     k       d       e        c`  |  Iv  c     k       d       e        c`
0    0  1  |  P1  12 @    0 :   0.000 = 1.955 *  6   |  d2   6 @   23 :  23.460 = 1.955 * 12  
1  100  4  |  m2  12 @   90 :  -9.780 = 1.955 * 11   |  A1  11 @  114 :  13.690 = 1.955 * 12   |  dd3  2 @   67 : -33.240 = 1.955 * 12  
2  200  7  |  M2  12 @  204 :   3.910 = 1.955 *  4   |  d3   9 @  180 : -19.550 = 1.955 * 12   |  dd4  4 @  227 :  27.370 = 1.955 * 12  
3  300 10  |  m3  12 @  294 :  -5.870 = 1.955 *  9   |  A2   9 @  318 :  17.600 = 1.955 * 12   |  AA2  4 @  271 : -29.330 = 1.955 * 12  
4  400 13  |  M3  12 @  408 :   7.820 = 1.955 *  2   |  d4  11 @  384 : -15.640 = 1.955 * 12   |  AA2  2 @  431 :  31.280 = 1.955 * 12  
5  500 16  |  P4  12 @  498 :  -1.960 = 1.955 *  7   |  A3   7 @  522 :  21.510 = 1.955 *  6   |  dd5  6 @  475 : -25.420 = 1.955 * 12  
6  600 19  |  d5  12 @  612 :  11.730 = 1.955 * 12   |  A4  12 @  588 : -11.730 = 1.955 * 12   |  AA3  1 @  565 : -35.190 = 1.955 * 12  
8  800 22  |  P5  12 @  702 :   1.960 = 1.955 *  8   |  d6   8 @  678 : -21.510 = 1.955 *  5   |  AA4  5 @  725 :  25.420 = 1.955 * 12  
8  800 25  |  m6  12 @  792 :  -7.820 = 1.955 * 10   |  A5  10 @  816 :  15.640 = 1.955 * 12   |  dd7  3 @  769 : -31.280 = 1.955 * 12  
a 1000 28  |  M6  12 @  906 :   5.870 = 1.955 *  3   |  d7  10 @  882 : -17.600 = 1.955 * 12   |  AA5  3 @  929 :  29.330 = 1.955 * 12  
a 1000 31  |  m7  12 @  996 :  -3.910 = 1.955 *  8   |  A6   8 @ 1020 : -27.370 = 1.955 *  5   |  dd8  5 @  973 : -27.370 = 1.955 * 12  
c 1200 34  |  M7  12 @ 1110 :   9.780 = 1.955 *  1   |  d8  12 @ 1086 : -13.690 = 1.955 * 12   |  AA6  1 @ 1133 :  33.240 = 1.955 * 12  
d 1300 36  |  P8  12 @ 1200 :   0.000 = 1.955 *  7   |  A7   7 @ 1177 : -23.460 = 1.955 * 12  

j j*100 i  |  Iv  c     k       d       e        c`  |  Iv  c     k       d       e        c`  |  Iv  c     k       d       e        c`  |  Iv  c     k       d       e        c`
0    0  1  |  P1  12 @    0 :   0.000 = 1.955 *  5   |  d2   5 @   23 :  23.460 = 1.955 * 12  
1  100  4  |  m2  12 @   90 :  -9.780 = 1.955 * 10   |  A1  10 @  114 :  13.690 = 1.955 * 12   |  dd3  1 @   67 : -33.240 = 1.955 * 12  
2  200  7  |  M2  12 @  204 :   3.910 = 1.955 *  3   |  d3   8 @  180 : -19.550 = 1.955 * 12   |  dd4  3 @  227 :  27.370 = 1.955 * 12  
3  300 10  |  m3  12 @  294 :  -5.870 = 1.955 *  8   |  A2   8 @  318 :  17.600 = 1.955 * 12   |  AA2  3 @  271 : -29.330 = 1.955 * 12  
4  400 13  |  M3  12 @  408 :   7.820 = 1.955 *  1   |  d4  10 @  384 : -15.640 = 1.955 * 12   |  AA2  1 @  431 :  31.280 = 1.955 * 12  
5  500 16  |  P4  12 @  498 :  -1.960 = 1.955 *  6   |  A3   6 @  522 :  21.510 = 1.955 *  5   |  dd5  5 @  475 : -25.420 = 1.955 * 12  
6  600 18  |  d5  11 @  612 :  11.730 = 1.955 * 12   |  A4  12 @  588 : -11.730 = 1.955 * 11  
7  700 21  |  P5  12 @  702 :   1.960 = 1.955 *  7   |  d6   7 @  678 : -21.510 = 1.955 *  4   |  AA4  4 @  725 :  25.420 = 1.955 * 12  
8  800 24  |  m6  12 @  792 :  -7.820 = 1.955 *  9   |  A5   9 @  816 :  15.640 = 1.955 * 12   |  dd7  2 @  769 : -31.280 = 1.955 * 12  
9  900 27  |  M6  12 @  906 :   5.870 = 1.955 *  2   |  d7   9 @  882 : -17.600 = 1.955 * 12   |  AA5  2 @  929 :  29.330 = 1.955 * 12  
a 1000 30  |  m7  12 @  996 :  -3.910 = 1.955 *  7   |  A6   7 @ 1020 : -27.370 = 1.955 *  4   |  dd8  4 @  973 : -27.370 = 1.955 * 12  
b 1100 32  |  M7  12 @ 1110 :   9.780 = 1.955 * 11   |  d8  11 @ 1086 : -13.690 = 1.955 * 12  
c 1200 34  |  P8  12 @ 1200 :   0.000 = 1.955 *  6   |  A7   6 @ 1177 : -23.460 = 1.955 * 12  

j j*100 i  |  Iv  c     k       d       e        c`  |  Iv  c     k       d       e        c`  |  Iv  c     k       d       e        c`  |  Iv  c     k       d       e        c`
0    0  1  |  P1  12 @    0 :   0.000 = 1.955 *  4   |  d2   4 @   23 :  23.460 = 1.955 * 12  
1  100  3  |  m2  12 @   90 :  -9.780 = 1.955 *  9   |  A1   9 @  114 :  13.690 = 1.955 * 12  
2  200  6  |  M2  12 @  204 :   3.910 = 1.955 *  2   |  d3   7 @  180 : -19.550 = 1.955 * 12   |  dd4  2 @  227 :  27.370 = 1.955 * 12  
3  300  9  |  m3  12 @  294 :  -5.870 = 1.955 *  7   |  A2   7 @  318 :  17.600 = 1.955 * 12   |  AA2  2 @  271 : -29.330 = 1.955 * 12  
4  400 11  |  M3  12 @  408 :   7.820 = 1.955 *  9   |  d4   9 @  384 : -15.640 = 1.955 * 12  
5  500 14  |  P4  12 @  498 :  -1.960 = 1.955 *  5   |  A3   5 @  522 :  21.510 = 1.955 *  4   |  dd5  4 @  475 : -25.420 = 1.955 * 12  
6  600 16  |  d5  10 @  612 :  11.730 = 1.955 * 11   |  A4  11 @  588 : -11.730 = 1.955 * 10  
7  700 19  |  P5  12 @  702 :   1.960 = 1.955 *  6   |  d6   6 @  678 : -21.510 = 1.955 *  3   |  AA4  3 @  725 :  25.420 = 1.955 * 12  
8  800 22  |  m6  12 @  792 :  -7.820 = 1.955 *  8   |  A5   8 @  816 :  15.640 = 1.955 * 12   |  dd7  1 @  769 : -31.280 = 1.955 * 12  
9  900 25  |  M6  12 @  906 :   5.870 = 1.955 *  1   |  d7   8 @  882 : -17.600 = 1.955 * 12   |  AA5  1 @  929 :  29.330 = 1.955 * 12  
a 1000 28  |  m7  12 @  996 :  -3.910 = 1.955 *  6   |  A6   6 @ 1020 : -27.370 = 1.955 *  3   |  dd8  3 @  973 : -27.370 = 1.955 * 12  
b 1100 30  |  M7  11 @ 1110 :   9.780 = 1.955 * 10   |  d8  10 @ 1086 : -13.690 = 1.955 * 11  
c 1200 32  |  P8  12 @ 1200 :   0.000 = 1.955 *  5   |  A7   5 @ 1177 : -23.460 = 1.955 * 12  

j j*100 i  |  Iv  c     k       d       e        c`  |  Iv  c     k       d       e        c`  |  Iv  c     k       d       e        c`  |  Iv  c     k       d       e        c`
0    0  1  |  P1  12 @    0 :   0.000 = 1.955 *  4   |  d2   4 @   23 :  23.460 = 1.955 * 12  
1  100  3  |  m2  12 @   90 :  -9.780 = 1.955 *  9   |  A1   9 @  114 :  13.690 = 1.955 * 12  
2  200  6  |  M2  12 @  204 :   3.910 = 1.955 *  2   |  d3   7 @  180 : -19.550 = 1.955 * 12   |  dd4  2 @  227 :  27.370 = 1.955 * 12  
3  300  9  |  m3  12 @  294 :  -5.870 = 1.955 *  7   |  A2   7 @  318 :  17.600 = 1.955 * 12   |  AA2  2 @  271 : -29.330 = 1.955 * 12  
4  400 11  |  M3  12 @  408 :   7.820 = 1.955 *  9   |  d4   9 @  384 : -15.640 = 1.955 * 12  
5  500 14  |  P4  12 @  498 :  -1.960 = 1.955 *  5   |  A3   5 @  522 :  21.510 = 1.955 *  4   |  dd5  4 @  475 : -25.420 = 1.955 * 12  
6  600 16  |  d5  10 @  612 :  11.730 = 1.955 * 11   |  A4  11 @  588 : -11.730 = 1.955 * 10  
7  700 19  |  P5  12 @  702 :   1.960 = 1.955 *  6   |  d6   6 @  678 : -21.510 = 1.955 *  3   |  AA4  3 @  725 :  25.420 = 1.955 * 12  
8  800 22  |  m6  12 @  792 :  -7.820 = 1.955 *  8   |  A5   8 @  816 :  15.640 = 1.955 * 12   |  dd7  1 @  769 : -31.280 = 1.955 * 12  
9  900 25  |  M6  12 @  906 :   5.870 = 1.955 *  1   |  d7   8 @  882 : -17.600 = 1.955 * 12   |  AA5  1 @  929 :  29.330 = 1.955 * 12  
b 1100 28  |  m7  12 @  996 :  -3.910 = 1.955 *  6   |  A6   6 @ 1020 : -27.370 = 1.955 *  3   |  dd8  3 @  973 : -27.370 = 1.955 * 12  
c 1200 30  |  M7  11 @ 1110 :   9.780 = 1.955 * 10   |  d8  10 @ 1086 : -13.690 = 1.955 * 11  
d 1300 32  |  P8  12 @ 1200 :   0.000 = 1.955 *  5   |  A7   5 @ 1177 : -23.460 = 1.955 * 12  

j j*100 i  |  Iv  c     k       d       e        c`  |  Iv  c     k       d       e        c`  |  Iv  c     k       d       e        c`  |  Iv  c     k       d       e        c`
0    0  1  |  P1  12 @    0 :   0.000 = 1.955 *  4   |  d2   4 @   23 :  23.460 = 1.955 * 12  
1  100  3  |  m2  12 @   90 :  -9.780 = 1.955 *  9   |  A1   9 @  114 :  13.690 = 1.955 * 12  
2  200  6  |  M2  12 @  204 :   3.910 = 1.955 *  2   |  d3   7 @  180 : -19.550 = 1.955 * 12   |  dd4  2 @  227 :  27.370 = 1.955 * 12  
3  300  9  |  m3  12 @  294 :  -5.870 = 1.955 *  7   |  A2   7 @  318 :  17.600 = 1.955 * 12   |  AA2  2 @  271 : -29.330 = 1.955 * 12  
4  400 11  |  M3  12 @  408 :   7.820 = 1.955 *  9   |  d4   9 @  384 : -15.640 = 1.955 * 12  
5  500 14  |  P4  12 @  498 :  -1.960 = 1.955 *  5   |  A3   5 @  522 :  21.510 = 1.955 *  4   |  dd5  4 @  475 : -25.420 = 1.955 * 12  
6  600 16  |  d5  10 @  612 :  11.730 = 1.955 * 11   |  A4  11 @  588 : -11.730 = 1.955 * 10  
7  700 19  |  P5  12 @  702 :   1.960 = 1.955 *  6   |  d6   6 @  678 : -21.510 = 1.955 *  3   |  AA4  3 @  725 :  25.420 = 1.955 * 12  
9  900 22  |  m6  12 @  792 :  -7.820 = 1.955 *  8   |  A5   8 @  816 :  15.640 = 1.955 * 12   |  dd7  1 @  769 : -31.280 = 1.955 * 12  
a 1000 24  |  M6  12 @  906 :   5.870 = 1.955 *  8   |  d7   8 @  882 : -17.600 = 1.955 * 12  
a 1000 27  |  dd8  3 @  973 : -27.370 = 1.955 * 12   |  m7  12 @  996 :  29.330 = 1.955 *  1   |  AA5  1 @  929 :  29.330 = 1.955 *  3  
b 1100 29  |  d8  10 @ 1086 : -13.690 = 1.955 *  6   |  A6   6 @ 1020 :  19.550 = 1.955 * 10   |  m7  12 @  996 :  -3.910 = 1.955 *  6  
c 1200 31  |  A7   5 @ 1177 : -23.460 = 1.955 * 11   |  M7  11 @ 1110 :   9.780 = 1.955 *  5  

j j*100 i  |  Iv  c     k       d       e        c`  |  Iv  c     k       d       e        c`  |  Iv  c     k       d       e        c`  |  Iv  c     k       d       e        c`
0    0  1  |  P1  12 @    0 :   0.000 = 1.955 *  3   |  d2   3 @   23 :  23.460 = 1.955 * 12  
1  100  3  |  m2  11 @   90 :  -9.780 = 1.955 *  8   |  A1   8 @  114 :  13.690 = 1.955 * 11  
2  200  6  |  M2  12 @  204 :   3.910 = 1.955 *  1   |  d3   6 @  180 : -19.550 = 1.955 * 12   |  dd4  1 @  227 :  27.370 = 1.955 * 12  
3  300  9  |  m3  12 @  294 :  -5.870 = 1.955 *  6   |  A2   6 @  318 :  17.600 = 1.955 * 12   |  AA2  1 @  271 : -29.330 = 1.955 * 12  
4  400 11  |  M3  11 @  408 :   7.820 = 1.955 *  8   |  d4   8 @  384 : -15.640 = 1.955 * 11  
5  500 14  |  P4  12 @  498 :  -1.960 = 1.955 *  4   |  A3   4 @  522 :  21.510 = 1.955 *  3   |  dd5  3 @  475 : -25.420 = 1.955 * 12  
6  600 16  |  d5   9 @  612 :  11.730 = 1.955 * 10   |  A4  10 @  588 : -11.730 = 1.955 *  9  
7  700 19  |  P5  12 @  702 :   1.960 = 1.955 *  5   |  d6   5 @  678 : -21.510 = 1.955 *  2   |  AA4  2 @  725 :  25.420 = 1.955 * 12  
8  800 21  |  m6  12 @  792 :  -7.820 = 1.955 *  7   |  A5   7 @  816 :  15.640 = 1.955 * 12  
9  900 23  |  M6  12 @  906 :   5.870 = 1.955 *  7   |  d7   7 @  882 : -17.600 = 1.955 * 12  
a 1000 26  |  m7  12 @  996 :  -3.910 = 1.955 *  5   |  A6   5 @ 1020 : -27.370 = 1.955 *  2   |  dd8  2 @  973 : -27.370 = 1.955 * 12  
b 1100 28  |  M7  10 @ 1110 :   9.780 = 1.955 *  9   |  d8   9 @ 1086 : -13.690 = 1.955 * 10  
c 1200 30  |  P8  12 @ 1200 :   0.000 = 1.955 *  4   |  A7   4 @ 1177 : -23.460 = 1.955 * 12  
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
