from tpkg       import utl
#from tpkg       import notes
from tpkg.notes import Notes
from tpkg       import intrvls as ivls

W, Y, Z, slog, ist     = utl.W,    utl.Y,    utl.Z,    utl.slog,   utl.ist
fmtl, fmtm, fmtf, fmtg = utl.fmtl, utl.fmtm, utl.fmtf, utl.fmtg

NT, A4_INDEX, CM_P_M, V_SOUND = ivls.NT, ivls.A4_INDEX, ivls.CM_P_M, ivls.V_SOUND

#fmtR0, fmtR1, fmtR2, fmtR3, fmtRA, fmtRB, fdvdr, addFmtRs = ivls.fmtR0, ivls.fmtR1, ivls.fmtR2, ivls.fmtR3, ivls.fmtRA, ivls.fmtRB, ivls.fdvdr, ivls.addFmtRs

'''
     3^-2    3^-1  3^0 3^1 3^2
5^1  5/3^2   5/3   5/1 3*5 3^2*5^2
5^0  1/3^2   1/3   1/1 1*3 1*3^2
5^-1 1/5*3^2 1/5*3 1/5 3/5 3^2/5

     1/9  1/3   1   3   9
 5   5/9  5/3   5  15  45 
 1   1/9  1/3   1   3   9
1/5  1/45 1/15 1/5 3/5 9/5

     1/9   1/3   1   3   9
 5   10/9  5/3  5/4 15/8 45/32
 1   16/9  4/3   1   3/2  9/8
1/5 64/45 16/15 8/5  6/5  9/5
########################################################################################################################################################################################################
BGN Just Intonation Series (k=50 .rf=440 .VS=345 .csv=0)
C  [     1     |     0     |    -1     ]
D  [    -2     |    -1     |     0     |     1     |     2     ]
C A[     5     |     1     |    1/5    ]
D B[    1/9    |    1/3    |     1     |     3     |     9     ]
   [     0           1           2           3           4           5           6           7           8           9          10          11          12          13          14     ]
r0s[  0.55556  |  1.66667  |     5     |    15     |    45     |  0.11111  |  0.33333  |     1     |     3     |     9     |  0.02222  |  0.06667  |  0.20000  |  0.60000  |  1.80000  ]
r1s[    5/9    |    5/3    |    5/1    |    5*3    |    5*9    |    1/9    |    1/3    |    1/1    |    1*3    |    1*9    |   1/45    |   1/15    |    1/5    |    3/5    |    9/5    ]
r2s[    5/3^2  |    5/3    |    5/1    |    5*3    |    5*3^2  |    1/3^2  |    1/3    |    1/1    |    1*3    |    1*3^2  | 1/(5*3^2) |  1/(5*3)  |    1/5    |    3/5    |  3^2/5    ]
r3s[   5¹/3²   |   5¹/3¹   |   5¹/3⁰   |   5¹*3¹   |   5¹*3²   |   5⁰/3²   |   5⁰/3¹   |   5⁰/3⁰   |   5⁰*3¹   |   5⁰*3²   | 1/(5¹*3²) | 1/(5¹*3¹) |   3⁰/5¹   |   3¹/5¹   |   3²/5¹   ]
   [0 0: 5^ 1 * 3^-2 =  0.5556 * 2^ 1 = 1.11111 : D ]
   [0 1: 5^ 1 * 3^-1 =  1.6667 * 2^ 0 = 1.66667 : A ]
   [0 2: 5^ 1 * 3^ 0 =  5.0000 * 2^-2 = 1.25000 : E ]
   [0 3: 5^ 1 * 3^ 1 = 15.0000 * 2^-3 = 1.87500 : B ]
   [0 4: 5^ 1 * 3^ 2 = 45.0000 * 2^-5 = 1.40625 : F♯]
   [1 0: 5^ 0 * 3^-2 =  0.1111 * 2^ 4 = 1.77778 : B♭]
   [1 1: 5^ 0 * 3^-1 =  0.3333 * 2^ 2 = 1.33333 : F ]
   [1 2: 5^ 0 * 3^ 0 =  1.0000 * 2^ 0 = 1.00000 : C ]
   [1 3: 5^ 0 * 3^ 1 =  3.0000 * 2^-1 = 1.50000 : G ]
   [1 4: 5^ 0 * 3^ 2 =  9.0000 * 2^-3 = 1.12500 : D ]
   [2 0: 5^-1 * 3^-2 =  0.0222 * 2^ 6 = 1.42222 : G♭]
   [2 1: 5^-1 * 3^-1 =  0.0667 * 2^ 4 = 1.06667 : D♭ C♯]
   [2 2: 5^-1 * 3^ 0 =  0.2000 * 2^ 3 = 1.60000 : A♭ G♯]
   [2 3: 5^-1 * 3^ 1 =  0.6000 * 2^ 1 = 1.20000 : E♭ D♯]
   [2 4: 5^-1 * 3^ 2 =  1.8000 * 2^ 0 = 1.80000 : A♯ B♭]
notes[     D     |     A     |     E     |     B     |    G♭     |    B♭     |     F     |     C     |     G     |     D     |    G♭     |    D♭     |    A♭     |    E♭     |    B♭     ]
ivals[    M2     |    M6     |    M3     |    M7     |    d5     |    m7     |    P4     |    P1     |    P5     |    M2     |    A4     |    m2     |    m6     |    m3     |    m7     ]
cents[   182.40  |   884.36  |   386.31  |  1088.27  |   590.22  |   996.09  |   498.04  |     0.00  |   701.96  |   203.91  |   609.78  |   111.73  |   813.69  |   315.64  |  1017.60  ]
dcnts[ -17.5963  | -15.6413  | -13.6863  | -11.7313  |  -9.7763  |  -3.9100  |  -1.9550  |   0.0000  |   1.9550  |   3.9100  |   9.7763  |  11.7313  |  13.6863  |  15.6413  |  17.5963  ]
 r0s [ 1.1111111 | 1.6666667 | 1.2500000 | 1.8750000 | 1.4062500 | 1.7777778 | 1.3333333 |     1     | 1.5000000 | 1.1250000 | 1.4222222 | 1.0666667 | 1.6000000 | 1.2000000 | 1.8000000 ]
 r1s [   10/9    |    5/3    |    5/4    |   15/8    |   45/32   |   16/9    |    4/3    |    1/1    |    3/2    |    9/8    |   64/45   |   16/15   |    8/5    |    6/5    |    9/5    ]
 r2s [  2*5/3^2  |    5/3    |   5*1/4   |   5*3/8   | 5*3^2/32  | 16*1/3^2  |   4*1/3   |    1/1    |   1*3/2   |  1*3^2/8  |64/(5*3^2) | 16/(5*3)  |   8*1/5   |   2*3/5   |  3^2/5    ]
 r3s [  2*5¹/3²  |   5¹/3¹   |  5¹*3⁰/4  |  5¹*3¹/8  | 5¹*3²/32  | 16*5⁰/3²  |  4*5⁰/3¹  |   5⁰/3⁰   |  5⁰*3¹/2  |  5⁰*3²/8  |64/(5¹*3²) |16/(5¹*3¹) |  8*3⁰/5¹  |  2*3¹/5¹  |   3²/5¹   ]
freqs[ 290.69507 | 436.04261 | 327.03196 | 490.54793 | 367.91095 | 465.11212 | 348.83409 | 261.62557 | 392.43835 | 294.32876 | 372.08969 | 279.06727 | 418.60090 | 313.95068 | 470.92602 ]
wvlns[ 118.68106 | 79.120708 | 105.49428 | 70.329518 | 93.772691 | 74.175664 | 98.900885 | 131.86785 | 87.911898 | 117.21586 | 92.719580 | 123.62611 | 82.417404 | 109.88987 | 73.259915 ]
END Just Intonation Series (k=50 .rf=440 .VS=345 .csv=0)
BGN Just Intonation Series (k=50 .rf=440 .VS=345 .csv=0)
C  [     1     |     0     |    -1     ]
D  [    -2     |    -1     |     0     |     1     |     2     ]
C A[     5     |     1     |    1/5    ]
D B[    1/9    |    1/3    |     1     |     3     |     9     ]
   [     0           1           2           3           4           5           6           7           8           9          10          11          12          13          14     ]
r0s[  0.55556  |  1.66667  |     5     |    15     |    45     |  0.11111  |  0.33333  |     1     |     3     |     9     |  0.02222  |  0.06667  |  0.20000  |  0.60000  |  1.80000  ]
r1s[    5/9    |    5/3    |    5/1    |    5*3    |    5*9    |    1/9    |    1/3    |    1/1    |    1*3    |    1*9    |   1/45    |   1/15    |    1/5    |    3/5    |    9/5    ]
r2s[    5/3^2  |    5/3    |    5/1    |    5*3    |    5*3^2  |    1/3^2  |    1/3    |    1/1    |    1*3    |    1*3^2  | 1/(5*3^2) |  1/(5*3)  |    1/5    |    3/5    |  3^2/5    ]
r3s[   5¹/3²   |   5¹/3¹   |   5¹/3⁰   |   5¹*3¹   |   5¹*3²   |   5⁰/3²   |   5⁰/3¹   |   5⁰/3⁰   |   5⁰*3¹   |   5⁰*3²   | 1/(5¹*3²) | 1/(5¹*3¹) |   3⁰/5¹   |   3¹/5¹   |   3²/5¹   ]
   [0 1: 5^ 1 * 3^-1 =  1.6667 * 2^ 0 = 1.66667 : A ]
   [0 2: 5^ 1 * 3^ 0 =  5.0000 * 2^-2 = 1.25000 : E ]
   [0 3: 5^ 1 * 3^ 1 = 15.0000 * 2^-3 = 1.87500 : B ]
   [0 4: 5^ 1 * 3^ 2 = 45.0000 * 2^-5 = 1.40625 : F♯]
   [1 1: 5^ 0 * 3^-1 =  0.3333 * 2^ 2 = 1.33333 : F ]
   [1 2: 5^ 0 * 3^ 0 =  1.0000 * 2^ 0 = 1.00000 : C ]
   [1 3: 5^ 0 * 3^ 1 =  3.0000 * 2^-1 = 1.50000 : G ]
   [1 4: 5^ 0 * 3^ 2 =  9.0000 * 2^-3 = 1.12500 : D ]
   [2 1: 5^-1 * 3^-1 =  0.0667 * 2^ 4 = 1.06667 : D♭ C♯]
   [2 2: 5^-1 * 3^ 0 =  0.2000 * 2^ 3 = 1.60000 : A♭ G♯]
   [2 3: 5^-1 * 3^ 1 =  0.6000 * 2^ 1 = 1.20000 : E♭ D♯]
   [2 4: 5^-1 * 3^ 2 =  1.8000 * 2^ 0 = 1.80000 : A♯ B♭]
notes[     A     |     E     |     B     |    G♭     |     F     |     C     |     G     |     D     |    D♭     |    A♭     |    E♭     |    B♭     ]
ivals[    M6     |    M3     |    M7     |    d5     |    P4     |    P1     |    P5     |    M2     |    m2     |    m6     |    m3     |    m7     ]
cents[   884.36  |   386.31  |  1088.27  |   590.22  |   498.04  |     0.00  |   701.96  |   203.91  |   111.73  |   813.69  |   315.64  |  1017.60  ]
dcnts[ -15.6413  | -13.6863  | -11.7313  |  -9.7763  |  -1.9550  |   0.0000  |   1.9550  |   3.9100  |  11.7313  |  13.6863  |  15.6413  |  17.5963  ]
 r0s [ 1.6666667 | 1.2500000 | 1.8750000 | 1.4062500 | 1.3333333 |     1     | 1.5000000 | 1.1250000 | 1.0666667 | 1.6000000 | 1.2000000 | 1.8000000 ]
 r1s [    5/3    |    5/4    |   15/8    |   45/32   |    4/3    |    1/1    |    3/2    |    9/8    |   16/15   |    8/5    |    6/5    |    9/5    ]
 r2s [    5/3    |   5*1/4   |   5*3/8   | 5*3^2/32  |   4*1/3   |    1/1    |   1*3/2   |  1*3^2/8  | 16/(5*3)  |   8*1/5   |   2*3/5   |  3^2/5    ]
 r3s [   5¹/3¹   |  5¹*3⁰/4  |  5¹*3¹/8  | 5¹*3²/32  |  4*5⁰/3¹  |   5⁰/3⁰   |  5⁰*3¹/2  |  5⁰*3²/8  |16/(5¹*3¹) |  8*3⁰/5¹  |  2*3¹/5¹  |   3²/5¹   ]
freqs[ 436.04261 | 327.03196 | 490.54793 | 367.91095 | 348.83409 | 261.62557 | 392.43835 | 294.32876 | 279.06727 | 418.60090 | 313.95068 | 470.92602 ]
wvlns[ 79.120708 | 105.49428 | 70.329518 | 93.772691 | 98.900885 | 131.86785 | 87.911898 | 117.21586 | 123.62611 | 82.417404 | 109.88987 | 73.259915 ]
END Just Intonation Series (k=50 .rf=440 .VS=345 .csv=0)

sorted
cents[     0.00  |   111.73  |   182.40  |   203.91  |   315.64  |   386.31  |   498.04  |   590.22  |   609.78  |   701.96  |   813.69  |   884.36  |   996.09  |  1017.60  |  1088.27  ]
'''
########################################################################################################################################################################################################
A, B = 5, 3
C    = [  1,  0, -1 ]
D    = [ -2, -1,  0, 1, 2 ]
R1   = [ A**C[0] * B**D[0], A**C[0] * B**D[1], A**C[0] * B**D[2], A**C[0] * B**D[3], A**C[0] * B**D[4] ]
R2   = [ A**C[1] * B**D[0], A**C[1] * B**D[1], A**C[1] * B**D[2], A**C[1] * B**D[3], A**C[1] * B**D[4] ]
R3   = [ A**C[2] * B**D[0], A**C[2] * B**D[1], A**C[2] * B**D[2], A**C[2] * B**D[3], A**C[2] * B**D[4] ]
CRS  = [ R1, R2, R3 ]
########################################################################################################################################################################################################
########################################################################################################################################################################################################
class Just(ivls.Intonation):
    def __init__(self, n='C', rf=440, vs=V_SOUND, csv=0):
        super().__init__(n=n, rf=rf, vs=vs, csv=csv)
        self.ivalKs = ['P1', 'm2', 'm2', 'M2', 'M2', 'm3', 'm3', 'M3', 'M3', 'P4', 'A3', 'd5', 'A4', 'd6', 'P5', 'm6', 'm6', 'M6', 'M6', 'm7', 'm7', 'M7', 'M7', 'P8']
        self.centKs = [   0,  90,  112,  182,  204,  294,  316,  384,  386,  498,  522,  590,  610,  678,  702,  792,  814,  884,  906,  996,  1018, 1088, 1110, 1200]
        self.set_ck2ikm() # todo this base class method initializes and or sets self.ck2ikm
    ####################################################################################################################################################################################################
    def dmpData(self, csv=0): # todo fixme 
        self.csv = csv
        slog(f'BGN {self.csv=}', p=0)
        k = self.k
        self.dmpJust(k)
        self.dmpJust(k, st=1)
        for i in range(0, NT):
            k = self.k + (i * 7) % NT
            self.dmpJust(k, st=1)
#        for i in range(7, NT):
#            k = self.k + (i * 7) % NT
#            self.dmpJust(k)
#        for i in range(0, 7):
#            k = self.k + (i * 7) % NT
#            self.dmpJust(k)
        slog(f'END {self.csv=}', p=0)
    ####################################################################################################################################################################################################
    def fmtNPair(self, k, i, s=0, dbg=0): # todo fixme
        n0, _   = self.i2nPair(self.k, s=1)   ;   s = '/' if s else W
        n1, n2  = self.i2nPair(k + i, b=0 if i in (4, 6, 11) or k in (self.k + 4, self.k + 6, self.k + 11) else 1, s=1, e=1)   ;   slog(f'{self.k=} {n0=} {n1=} {n2=}') if dbg else None
        if i and i != NT:
            if          n1 == self.COFM[n0][1]:   return n2
            elif n2 and n2 != self.COFM[n0][1]:   n1 += s + n2
        slog(f'return {n1=}') if dbg else None
        return n1

    def fmtNote(self, k, i, b=1):
        n1, n2   = self.i2nPair(k + i, b=b, s=1)
        return n1

    def fmtIs(self, l, v=0, w=11):
        oo = Y if self.csv else '|'    ;    ret = []
        for i, e in enumerate(l):
            if   not v and ist(      e, int):  _ =         e    ;  ret.append(f'{_:^{w}}')
            elif     v and ist(v **  e, int):  _ =      v**e    ;  ret.append(f'{_:^{w}}')
            elif     v and ist(v ** -e, int):  _ = f'1/{v**-e}' ;  ret.append(f'{_:^{w}}')
            else:                              assert 0,  f'{v=} {i=} {l=} {l[i]=} {e=} {type(e)=} {v**e=} {type(v**e)=} {v**-e=} {type(v**-e)=}'
        return fmtl(ret, s=oo, d=Z) # W.join(fmtl(ret))
    
    def fmtIRs(self, a, b):
        mm, nn, oo, ff = (Y, Y, Y, 3) if self.csv else (W, Z, '|', 1)   ;   d1, d2 = '[', ']'   ;   x, y, z = 11, 9, 5   ;   w = f'^{x}'
        r0s, r1s, r2s, r3s = [], [], [], []
        slog(f'{nn}C {nn} {nn}{d1}{nn}{self.fmtIs(C,    w=x)}{nn}{d2}', p=0, f=ff)
        slog(f'{nn}D {nn} {nn}{d1}{nn}{self.fmtIs(D,    w=x)}{nn}{d2}', p=0, f=ff)
        slog(f'{nn}C {nn}A{nn}{d1}{nn}{self.fmtIs(C, A, w=x)}{nn}{d2}', p=0, f=ff)
        slog(f'{nn}D {nn}B{nn}{d1}{nn}{self.fmtIs(D, B, w=x)}{nn}{d2}', p=0, f=ff)
        ii = [ f'{i}' for i in range(len(C) * len(D)) ]
        slog(f'{nn}   {nn}{nn}{d1}{nn}{fmtl(ii,  w=w, s=mm, d=Z)}{nn}{d2}', p=0, f=ff)
        for     i, c in enumerate(C):
            for j, d in enumerate(D):
                self.addFmtRs(a, c, b, d, rs=[r0s, r1s, r2s, r3s], u=z,     k=0, i=i, j=j)
        slog(f'{nn}r0s{nn}{nn}{d1}{nn}{fmtl(r0s, w=w, s=oo, d=Z)}{nn}{d2}', p=0, f=ff)
        slog(f'{nn}r1s{nn}{nn}{d1}{nn}{fmtl(r1s, w=w, s=oo, d=Z)}{nn}{d2}', p=0, f=ff)
        slog(f'{nn}r2s{nn}{nn}{d1}{nn}{fmtl(r2s, w=w, s=oo, d=Z)}{nn}{d2}', p=0, f=ff)
        slog(f'{nn}r3s{nn}{nn}{d1}{nn}{fmtl(r3s, w=w, s=oo, d=Z)}{nn}{d2}', p=0, f=ff)
    ####################################################################################################################################################################################################
    def dmpJust(self, k, st=0, dbg=1):
        f0 = self.FREFS[k]  ;  M3 = Notes.V2I['M3']   ;   a, b = 5, 3   ;   k += 2 # todo fixme note freq hack
        mm, nn, oo, ff = (Y, Y, Y, 3) if self.csv else (W, Z, '|', 1)   ;   d1, d2 = '[', ']'   ;   x, y, z = 11, 9, 5   ;   w = f'^{x}'
        slog(f'BGN Just Intonation Series ({k=} {self.rf=} {self.VS=} {self.csv=})', p=0, f=ff)
        self.fmtIRs(a, b)
        for     i, c in enumerate(C):
            kk = k - i * M3
            for j, d in enumerate(D):
                n = self.fmtNPair(kk, (j*7)%NT)
                if st == 1 and j == 0:    slog(f'{st=} Filter1 {n=:2} {k=:2} {kk=:2} @ j=0 {i=}', p=0) if dbg else None   ;   continue
                u = CRS[i][j]
                v, p = self.norm(u)
                slog(f'   {nn}{d1}{nn}{i}{nn} {j}{nn}:{nn} {a}^{c:2} {nn}*{nn} {b}^{d:2} {nn}={nn} {u:7.4f} {nn}*{nn} 2^{p:2} {nn}={nn} {v:7.5f} {nn}:{nn} {n:2}{nn}{d2}', p=0, f=ff)
        r0s, r1s, r2s, r3s = [], [], [], []   ;   cents, dcnts, ivals, notes = [], [], [], []   ;   freqs, wvlns = [], []
        for     i, c in enumerate(C):
            kk = k - i * M3
            for j, d in enumerate(D):
                n = self.fmtNote(kk, (j*7)%NT)
                if st == 1 and j == 0:    slog(f'{st=} Filter2 {n=:2} {k=:2} {kk=:2} @ j=0 {i=}', p=0) if dbg else None   ;   continue
                notes.append(n)
                u = CRS[i][j]
                v, p = self.norm(u)
                self.addFmtRs(a, c, b, d, rs=[r0s, r1s, r2s, r3s], u=z, w=x, k=p, i=i, j=j)
                freq = f0 * v              ;   freqs.append(fmtf(freq, x-2))
                wvln = self.w0 / freq      ;   wvlns.append(fmtf(wvln, x-2))
                cent = self.r2cents(v)     ;   cents.append(f'{cent:7.2f}')
                dcnt = self.k2dCent(cent)  ;   dcnts.append(f'{dcnt:7.4f}')
                rc   = round(cent)
                assert rc in self.ck2ikm,  f'{rc=} not in ck2ik {k=} {i=} {j=} {n=} {cent=} {dcnt=} {rc=}'
                ival = self.ck2ikm[rc]     ;   ivals.append(ival)
        slog(f'{nn}notes{nn}{nn}{d1}{nn}{fmtl(notes, w=w, s=oo, d=Z)}{nn}{d2}', p=0, f=ff)
        slog(f'{nn}ivals{nn}{nn}{d1}{nn}{fmtl(ivals, w=w, s=oo, d=Z)}{nn}{d2}', p=0, f=ff)
        slog(f'{nn}cents{nn}{nn}{d1}{nn}{fmtl(cents, w=w, s=oo, d=Z)}{nn}{d2}', p=0, f=ff)
        slog(f'{nn}dcnts{nn}{nn}{d1}{nn}{fmtl(dcnts, w=w, s=oo, d=Z)}{nn}{d2}', p=0, f=ff)
        slog(f'{nn} r0s {nn}{nn}{d1}{nn}{fmtl(r0s,   w=w, s=oo, d=Z)}{nn}{d2}', p=0, f=ff)
        slog(f'{nn} r1s {nn}{nn}{d1}{nn}{fmtl(r1s,   w=w, s=oo, d=Z)}{nn}{d2}', p=0, f=ff)
        slog(f'{nn} r2s {nn}{nn}{d1}{nn}{fmtl(r2s,   w=w, s=oo, d=Z)}{nn}{d2}', p=0, f=ff)
        slog(f'{nn} r3s {nn}{nn}{d1}{nn}{fmtl(r3s,   w=w, s=oo, d=Z)}{nn}{d2}', p=0, f=ff)
        slog(f'{nn}freqs{nn}{nn}{d1}{nn}{fmtl(freqs, w=w, s=oo, d=Z)}{nn}{d2}', p=0, f=ff)
        slog(f'{nn}wvlns{nn}{nn}{d1}{nn}{fmtl(wvlns, w=w, s=oo, d=Z)}{nn}{d2}', p=0, f=ff)
        slog(f'END Just Intonation Series ({k=} {self.rf=} {self.VS=} {self.csv=})', p=0, f=ff)

########################################################################################################################################################################################################
########################################################################################################################################################################################################
#def fmtR0(a, ca, b, cb, w):       pa = float(a ** ca)  ;  pb = float(b ** abs(cb)) if cb < 0 else float(b ** cb)   ;  return f'{pa/pb:{w}}' if cb < 0 else f'{pa*pb:{w}}'

#def fmtR1(a, ca, b, cb, w):
#    pa = a ** abs(ca) if ca < 0 else a ** ca  ;  pb = b ** abs(cb) if cb < 0 else b ** cb  ;  papbi = f'1/({pa}*{pb})'
#    return f'{pa:>{w}}*{pb:<{w}}' if ca >= 0 <= cb else f'{pa:>{w}}/{pb:<{w}}' if ca >= 0 > cb else f'{pb:>{w}}/{pa:<{w}}' if ca < 0 <= cb else f'{papbi:^{2*w+1}}' if ca < 0 > cb else f'?#?#?'

#def fmtR2(a, ca, b, cb, w):
#    qa = f'{a}^{abs(ca)}' if ca < 0 else f'{a}^{ca}'  ;  qb = f'{b}^{abs(cb)}' if cb < 0 else f'{b}^{cb}'  ;  qaqbi = f'1/({qa}*{qb})'
#    return f'{qa:>{w}}*{qb:<{w}}' if ca >= 0 <= cb else f'{qa:>{w}}/{qb:<{w}}' if ca >= 0 > cb else f'{qb:>{w}}/{qa:<{w}}' if ca < 0 <= cb else f'{qaqbi:^{2*w+1}}' if ca < 0 > cb else f'?#?#?'

#def fmtR3(a, ca, b, cb, w):
#    sa = f'{a}{i2spr(abs(ca))}' if ca < 0 else f'{a}{i2spr(ca)}'  ;  sb = f'{b}{i2spr(abs(cb))}' if cb < 0 else f'{b}{i2spr(cb)}'  ;  sasbi = f'1/({sa}*{sb})'
#    return f'{sa:>{w}}*{sb:<{w}}' if ca >= 0 <= cb else f'{sa:>{w}}/{sb:<{w}}' if ca >= 0 > cb else f'{sb:>{w}}/{sa:<{w}}' if ca < 0 <= cb else f'{sasbi:^{2*w+1}}' if ca < 0 > cb else f'?#?#?'
########################################################################################################################################################################################################
########################################################################################################################################################################################################
#def fmtR0(a, ca, b, cb, w, k=0): # w=11
#    pa = a ** ca  ;  pb = b ** abs(cb)  ;  p = 2 ** k if k is not None else 1
#    v = p*pa/pb if cb < 0 else p*pa*pb
#    return f'{v:^{w}.{w-4}f}' if ist(v, float) else f'{v:^{w}}'
########################################################################################################################################################################################################
#def fmtR1(a, ca, b, cb, w, k, i, j):
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
#def fmtR2(a, ca, b, cb, w, k, i, j):
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
#def fmtR3(a, ca, b, cb, w, k, i, j):
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
#def fmtRA(a, ca, w=Z):        pa     =   a ** ca                             ;  return f'{pa:{w}}'
#def fmtRB(b, cb, w=Z):        pb     =   b ** cb                             ;  return f'{pb:{w}}'
#def fdvdr(a, ca, b, cb):      n = max(len(fmtRA(a, ca)), len(fmtRB(b, cb)))  ;  return n * '/'
########################################################################################################################################################################################################
#def NEW_addFmtRs(a, ca, b, cb, rs, u=4, w=9, k=None, i=None, j=None):
#    assert rs and ist(rs, list),  f'{rs=} {type(rs)=} {a=} {ca} {b} {cb} {u=} {w=}'   ;   lr = len(rs)
##    r0s, r2s, r3s = [], [], []   ;   r1s = [] if lr == 4 else None   ;   rAs = [] if lr == 5 else None   ;   rBs = [] if lr == 5 else None
#    r0s, r2s, r3s = rs[0], rs[-2], rs[-1] #         ;   r1s, rAs, rBs = None, None, None
#    r1s, rAs, rBs = None,  None,   None
#    if   lr == 4:       r1s      = rs[1]           ;   r1s.append(fmtR1(a, ca, b, cb, u, k, i, j))
#    elif lr == 5:       rAs, rBs = rs[1], rs[2]    ;   rAs.append(fmtRA(a, ca, w))    ;    rBs.append(fmtRB(b, cb, w)) # if ist(b**cb, int) else w3))
#    r0s.append(fmtR0(a, ca, b, cb, w, k))
#    r2s.append(fmtR2(a, ca, b, cb, u, k, i, j)) # if u >= 9 else None
#    r3s.append(fmtR3(a, ca, b, cb, u, k, i, j))
#    if   lr == 4:   return r0s, r1s,      r2s, r3s
#    elif lr == 5:   return r0s, rAs, rBs, r2s, r3s
    
#def OLD_addFmtRs(i, j, k, r0s, r1s, r2s, r3s, a, ca, b, cb, u=5, w=11): # u=5 w=11
##   rAs.append(fmtRA(a, ca, ww if ist(a**ca, int) else w3))
##   rBs.append(fmtRB(b, cb, ww if ist(b**cb, int) else w3))
#    r0s.append(fmtR0(a, ca, b, cb, w, k))
#    r1s.append(fmtR1(a, ca, b, cb, u, k, i, j))
#    r2s.append(fmtR2(a, ca, b, cb, u, k, i, j)) if u >= 5 else None
#    r3s.append(fmtR3(a, ca, b, cb, u, k, i, j))
########################################################################################################################################################################################################
