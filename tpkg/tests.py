import pyglet.sprite     as pygsprt
import pyglet.image      as pygimg
from   pyglet.window.key import symbol_string    as psym
from   pyglet.window.key import modifiers_string as pmod
from   collections       import Counter
from   tpkg              import utl

W, Y, Z, slog, ist     = utl.W,    utl.Y,    utl.Z,    utl.slog,   utl.ist
fmtl, fmtm, fmtf, fmtg = utl.fmtl, utl.fmtm, utl.fmtf, utl.fmtg
SPR                    = pygsprt.Sprite

def test_0(tobj):
    a = 1/0         ;  slog(f'{a=}')
    p = tobj.pages  ;  f = tobj.CSV_FILE
    a = [{'a':1, 'b':"2", 'c':3.00+1/3}]  ;  b = [ f'{p[i].y}' for i in range(len(p)) ]  ;  c = tobj.sobj.stringMap  ;  d = [ tobj.screens ]
    print(tobj.__class__.__name__, 'testA', a, sep=Y, file=f, end=Y)
    print(tobj.__class__.__name__, 'testB', b, sep=Y, file=f, end=Y)
    print(tobj.__class__.__name__, 'testC', c, sep=Y, file=f)
    print(tobj.__class__.__name__, 'testD', d, sep=Y, file=f)
    quit(Z.join(('test00', str(a))))
########################################################################################################################################################################################################
def testSprTxt_0(tobj, path):
    np, nl, ns, nc, nt = tobj.n  ;  r, c = nt*ns*nl, nc
    slog(f'BGN {path=} {r=} {c=}')
#        lbl = tabls[0]
#        tex = batch.get_texture()
#        spr = SPR(tex, x=100, y=100, batch=batch, group=j2g(H), subpixel=SUBPIX)
#        spr.anchor_x, spr.anchor_y = axyWgt(ax, ay)

def testSprTxt_1(tobj, path):
    np, nl, ns, nc, nt = tobj.n  ;  r, c = nt*ns*nl, nc
#        t = tabls[0]  ;  doc = t.document  ;  m = doc.styles  ;  font = pygfont.load(m[FONT_NAME], m[FONT_SIZE])
#        ssPath = snapshot('text img for Sprites', 'SPRTXT')
    slog(f'BGN {path=} {r=} {c=}')
    img = pygimg.load(path)
    ig  = pygimg.ImageGrid(img, r, c)
#        itg = pygimg.TextureGrid(ig)
    ds = ig[0:10]
    for j, d in enumerate(ds):
        slog(f'ds[{j}]=d={d}')
        fname = f'd_{j}.png'
        d.save(fname)
    slog(f'END {path=} {r=} {c=}')

def testSprTxt_2(tobj, path):
    np, nl, ns, nc, nt = tobj.n  ;  r, c = nt*ns*nl, nc
    slog(f'BGN {path=} {r=} {c=}')
    img = pygimg.load(path)
    spr = SPR(img, x=100, y=100, batch=tobj.batch, group=tobj.j2g(tobj.H), subpixel=tobj.SUBPIX)
    spr.anchor_x, spr.anchor_y = tobj.axyWgt(tobj.ax, tobj.ay)
    tobj.sprs.append(spr)

def testSprTxt_3(tobj): # , path):
    np, nl, ns, nc, nt = tobj.n  ;  r, c = 1, nc # nt*ns*nl, nc
    path = utl.getFilePath('testA', tobj.BASE_PATH, tobj.PNGS, tobj.PNG)
    slog(f'BGN {path=} {r=} {c=}')
    pimg = pygimg.load(path)
    ig   = pygimg.ImageGrid(pimg, r, c)
    spr  = tobj.SPR(ig[2], x=300, y=200, batch=tobj.batch, group=tobj.j2g(tobj.H), subpixel=tobj.SUBPIX)
    spr.anchor_x, spr.anchor_y = tobj.axyWgt(tobj.ax, tobj.ay)
    tobj.sprs.append(spr)
    slog(f'END {path=} {r=} {c=}')
    #Install pillow for SVG files
########################################################################################################################################################################################################
def test0(tobj, a=3.14159265359, n=4, q=0):
    slog(f'BGN test0 {a=} {n=} {q=}')
    slog(utl.fmtf(a*1, n))
    slog(utl.fmtf(a*10, n))
    slog(utl.fmtf(a*100, n))
    slog(utl.fmtf(a*1000, n))
    slog(utl.fmtf(a*10000, n))
    slog(utl.fmtf(a*100000, n))
    slog(utl.fmtf(a*1000000, n))
    if   q==2: tExit(tobj, f'test0 {a=} {n=} {q=}', 0)
    elif q==1: tobj.quit(  f'test0 {a=} {n=} {q=}', 0, 0)
    slog(f'END test0 {a=} {n=} {q=}')

def test1(tobj, amap, mmap, q=0):
    slog(f'{tobj.nlnsnt()=}')
    slog(f'{utl.fmtm(amap)}')
    slog(f'{  amap["LLBL"]}', p=0)
    slog(f'   j(TI)={Y.join(amap["TI"])};')
    slog(f' j(XYWH)={Y.join(amap["XYWH"])};')
    slog(f' j(AXY2)={Y.join(amap["AXY2"])};')
    slog(f' j(LTXA)={Y.join(amap["LTXA"])};')
    slog(f'j(LTXAC)={Y.join(amap["LTXAC"])};')
    slog(f'  j(ADS)={Y.join(amap["ADS"])};')
    slog(f'  j(LDS)={Y.join(amap["LDS"])};')
    slog(f' j(LLBL)={Y.join(amap["LLBL"])};')
    slog(f' {Y.join(amap["LLBL"])}', p=0)
    slog(f'{mmap["JSPR"](2, Y)=}')
    slog(f'{mmap["JLBL"](2, Y)=}')
    slog(f'{mmap["JSPR"](2, Y)}', p=0)
    slog(f'{mmap["JLBL"](2, Y)}', p=0)
    # slog(f'{    tabs.TI=}')
    # slog(f'{  tabs.XYWH=}')
    # slog(f'{  tabs.AXY2=}')
    # slog(f'{   tabs.CWH=}')
    # slog(f'{  tabs.LTXA=}')
    # slog(f'{ tabs.LTXAC=}')
    # slog(f'{   tabs.ADS=}')
    # slog(f'{   tabs.CVA=}')
    # slog(f'{   tabs.LDS=}')
    # slog(f'{  tabs.LLBL=}')
    # slog(f'   j(TI)={Y.join(tabs.TI)};')
    # slog(f' j(XYWH)={Y.join(tabs.XYWH)};')
    # slog(f' j(AXY2)={Y.join(tabs.AXY2)};')
    # slog(f' j(LTXA)={Y.join(tabs.LTXA)};')
    # slog(f'j(LTXAC)={Y.join(tabs.LTXAC)};')
    # slog(f'  j(ADS)={Y.join(tabs.ADS)};')
    # slog(f'  j(LDS)={Y.join(tabs.LDS)};')
    # slog(f' j(LLBL)={Y.join(tabs.LLBL)};')
    # slog(f' {Y.join(tabs.LLBL)}', p=0)
    # slog(f'{tabs.JSPR(2, Y)=}')
    # slog(f'{tabs.JLBL(2, Y)=}')
    # slog(f'{tabs.JSPR(2, Y)}', p=0)
    # slog(f'{tabs.JLBL(2, Y)}', p=0)
    if q:    tExit(tobj, 'test1', 0)
########################################################################################################################################################################################################
def test2(tobj, j=10):
    slog(f'{tobj.ntsl()=}')
    hdrA = '      cc [  tpb  tpp tpl tps tpc] [p l s  c t]'
    hdrB = ' cn   cc [  tpb  tpp tpl tps tpc] [p l s  c t]'
    hdrC = '  cc  cn [  tpb  tpp tpl tps tpc] [p l s  c t]'
    np, nl, ns, nc, nt = tobj.i #  ;   p, l, c = 0, 0, 0
    tobj.dumpTniksPfx(f'BGN {j=} test2', r=0)
    slog(hdrB)
    for p in range(np):
        for l in range(nl):
            for _ in range(ns):
                for c in range(nc):
                    for t in range(nt):
                        cc = tobj.plct2cc(p, l, c, t, dbg=1)
                        cn = tobj.cc2cn(cc)
                        slog(f'{cn:3} {cc:4} {tobj.fntp()} {tobj.fplsct()}')
    slog(hdrB)
    for i in range(len(tobj.tabls) * ns):
        tobj.cc2cn(  i, dbg=1)
    slog(hdrC)
    for i in range(len(tobj.tabls)):
        tobj.cn2cc(  i, dbg=1)
#        slog(hdrB)
#        for i in range(len(tabls)):
#            cn2txt( i, dbg=1)
    slog(hdrA)
    for i in range(len(tobj.tabls) * ns):
        tobj.cc2plct(i, dbg=1)
#        slog(hdrB)
#        for i in range(len(tabls) * ns):
#            plc2cn_(p, l, c, dbg=1)
    tobj.dumpTniksSfx(f'END {j=} test2')
########################################################################################################################################################################################################
def test3(tobj):
    i = tobj.i[0] - 1
    i = (i + 1) % tobj.n[0]
    tobj.i[0] = i + 1
########################################################################################################################################################################################################
def test4(args):
    msg = f'{utl.fmtm(args)=}'
    slog(msg)
    for k, v in args.items():
        slog(f'{k}={utl.fmtl(v, d=Z)} ', p=0, f=-3, e=Z)
    slog(p=0)
########################################################################################################################################################################################################
class Tetractys:
    def __init__(self, pythgrn):
        self.pythgrn = pythgrn   ;   self.bot = 24   ;   self.top = 10000   ;   self.k = {}
        self.a, self.b, self.c = [], [], [[1]]
        self.d, self.e = [], []   ;   self.d2, self.e2 = [], []
        for i in range(20):
            self.a.append(i)   ;   u, v = [], []
            for j in range(i+1):
                u.append(j)
                if i > 0:   v.append(2*self.c[i-1][j] if j < i else 3*self.c[i-1][i-1])
            self.b.append(u)
            self.c.append(v) if v else None
        slog(f'Tetractys: {self.bot=} {self.top=} a, b, c =  d, e =  d2, e2 =', p=0, f=-3)
        slog(f'{fmtl(self.a, w=5)}', p=0, f=-3)
        slog(f'{fmtl(self.b, w=5)}', p=0, f=-3)
        slog(f'{fmtl(self.c, w=5)}', p=0, f=-3)
        
    def dmpData(self):
        self.sort()
        self.pythgrn.dmpData2(u=9, dbg=0)
        self.octdiv()
        
    def sort(self):
        for v in self.c:
            s = f'{fmtl(v, w="^9", d=Z)}'
            for w in v:
                self.d.append(w)
            self.e = sorted(self.d)
            slog(f'{s:^200} {fmtl(self.e)} {len(self.e)}', p=0, f=-3)
        
    def octdiv(self):
        self.k = Counter()
        for i, v in enumerate(self.c):
            for k, w in enumerate(v):
                while w > self.top:
                    assert ist(w, int),  f'{w=} {ist(w, int)=} {i=} {k=} {v=} {self.k=}'
                    w //= 2   ;   assert ist(w, int),  f'{w=} {ist(w, int)=} {i=} {k=} {v=} {self.k=}'
                if w not in self.d2:  self.d2.append(w)
                else:
                    if not w % 2: w = self.foldB(w, 1)
                    else:         w = self.foldB(w, 1)
                v[k] = w
            s = f'{fmtl(v, w="^9", d=Z)}'
            self.e2 = sorted(self.d2)
            slog(f'{s:^200} {fmtl(self.e2)} {len(self.e2)}', p=0, f=-3)
            
    def foldA(self, n, m):
        n = self.base(n)
        while n in self.d2 and self.k[f'{n}'] >= m:
            if n*2 >= self.top:   n = self.foldA(n, m+1)   ;   break
            n *= 2
        if n not in self.d2: self.d2.append(n)
        self.k[f'{n}'] += 1
        return n
        
    def foldB(self, n, m):
        n0 = n   ;   n //= 2
        while self.k[f'{n}'] >= m:
            if n//2 <= self.bot:
                n = n0   ;   n = self.foldB(n, m+1)   ;   break
            n //= 2
        if n not in self.d2: self.d2.append(n)
        self.k[f'{n}'] += 1
        return n

    def base(self, n):
        while n > self.bot and n in self.d2:
            n //= 2
        return n
########################################################################################################################################################################################################
def tExit(tobj, why, e): #        dispatch_event('on_close')
    slog(f'BGN {why} {e}')
    sym, mod = 65507, 2   ;   slog(f'on_key_press   {sym} {mod} {psym(sym)} {pmod(mod)}')   ;   tobj.dispatch_event('on_key_press',   sym, mod)
    sym, mod = 65505, 3   ;   slog(f'on_key_press   {sym} {mod} {psym(sym)} {pmod(mod)}')   ;   tobj.dispatch_event('on_key_press',   sym, mod)
    sym, mod =   113, 3   ;   slog(f'on_key_press   {sym} {mod} {psym(sym)} {pmod(mod)}')   ;   tobj.dispatch_event('on_key_press',   sym, mod)
    sym, mod =   113, 3   ;   slog(f'on_key_release {sym} {mod} {psym(sym)} {pmod(mod)}')   ;   tobj.dispatch_event('on_key_release', sym, mod)
    sym, mod = 65505, 3   ;   slog(f'on_key_release {sym} {mod} {psym(sym)} {pmod(mod)}')   ;   tobj.dispatch_event('on_key_release', sym, mod)
    sym, mod = 65507, 2   ;   slog(f'on_key_release {sym} {mod} {psym(sym)} {pmod(mod)}')   ;   tobj.dispatch_event('on_key_release', sym, mod)
    slog(f'END {why} {e}')

#  99 evnts on_key_press       BGN  65507 0xffe3 LCTRL            2 MOD_CTRL                                   kd=
# 183 evnts on_key_press       UNH  65507 0xffe3 LCTRL            2 MOD_CTRL                                   kd=
# 190 evnts on_key_press       END  65507 0xffe3 LCTRL            2 MOD_CTRL                                   kd=, retv=False
#  99 evnts on_key_press       BGN  65505 0xffe1 LSHIFT           3 MOD_SHIFT|MOD_CTRL                         kd=
# 183 evnts on_key_press       UNH  65505 0xffe1 LSHIFT           3 MOD_SHIFT|MOD_CTRL                         kd=
# 190 evnts on_key_press       END  65505 0xffe1 LSHIFT           3 MOD_SHIFT|MOD_CTRL                         kd=, retv=False
#  99 evnts on_key_press       BGN    113 0x0071 Q                3 MOD_SHIFT|MOD_CTRL                         kd=
# ...
# 190 evnts on_key_press       END    113 0x0071 Q                3 MOD_SHIFT|MOD_CTRL                         kd=, retv=False
########################################################################################################################################################################################################
'''
# 159 tests test4              .(args)='{{i:[1 1 1 6]} {n:[1 1 10 6]} {M:[0]} {t:[]} {d:[]} {e:[]} {o:[]} {p:[6]} {S:[0 1 3]} {f:[test]} {w:[0 0 0 0]} {T:[E A D G B E]}}'
i=1 1 1 6 n=1 1 10 6 M=0 t= d= e= o= p=6 S=0 1 3 f=test w=0 0 0 0 T=E A D G B E 

# 175 tests __init__           (.a, w=3)='[  0   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19]'
# 176 tests __init__           (.b, w=3)='[[  0][  0   1][  0   1   2][  0   1   2   3][  0   1   2   3   4][  0   1   2   3   4   5][  0   1   2   3   4   5   6][  0   1   2   3   4   5   6   7][  0   1   2   3   4   5   6   7   8][  0   1   2   3   4   5   6   7   8   9][  0   1   2   3   4   5   6   7   8   9  10][  0   1   2   3   4   5   6   7   8   9  10  11][  0   1   2   3   4   5   6   7   8   9  10  11  12][  0   1   2   3   4   5   6   7   8   9  10  11  12  13][  0   1   2   3   4   5   6   7   8   9  10  11  12  13  14][  0   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15][  0   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16][  0   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17][  0   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18][  0   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19]]'
# 177 tests __init__           (.c, w=3)='[[  1][  2   3][  4   6   9][  8  12  18  27][ 16  24  36  54  81][ 32  48  72 108 162 243][ 64  96 144 216 324 486 729][128 192 288 432 648 972 1458 2187][256 384 576 864 1296 1944 2916 4374 6561][512 768 1152 1728 2592 3888 5832 8748 13122 19683][1024 1536 2304 3456 5184 7776 11664 17496 26244 39366 59049][2048 3072 4608 6912 10368 15552 23328 34992 52488 78732 118098 177147][4096 6144 9216 13824 20736 31104 46656 69984 104976 157464 236196 354294 531441][8192 12288 18432 27648 41472 62208 93312 139968 209952 314928 472392 708588 1062882 1594323][16384 24576 36864 55296 82944 124416 186624 279936 419904 629856 944784 1417176 2125764 3188646 4782969][32768 49152 73728 110592 165888 248832 373248 559872 839808 1259712 1889568 2834352 4251528 6377292 9565938 14348907][65536 98304 147456 221184 331776 497664 746496 1119744 1679616 2519424 3779136 5668704 8503056 12754584 19131876 28697814 43046721][131072 196608 294912 442368 663552 995328 1492992 2239488 3359232 5038848 7558272 11337408 17006112 25509168 38263752 57395628 86093442 129140163][262144 393216 589824 884736 1327104 1990656 2985984 4478976 6718464 10077696 15116544 22674816 34012224 51018336 76527504 114791256 172186884 258280326 387420489][524288 786432 1179648 1769472 2654208 3981312 5971968 8957952 13436928 20155392 30233088 45349632 68024448 102036672 153055008 229582512 344373768 516560652 774840978 1162261467]]'
                                                                                                   1                                                                                                     [1]
                                                                                              2         3                                                                                                [1 2 3]
                                                                                         4         6         9                                                                                           [1 2 3 4 6 9]
                                                                                    8        12        18        27                                                                                      [1 2 3 4 6 8 9 12 18 27]
                                                                              16        24        36        54        81                                                                                 [1 2 3 4 6 8 9 12 16 18 24 27 36 54 81]
                                                                         32        48        72        108       162       243                                                                           [1 2 3 4 6 8 9 12 16 18 24 27 32 36 48 54 72 81 108 162 243]
                                                                    64        96        144       216       324       486       729                                                                      [1 2 3 4 6 8 9 12 16 18 24 27 32 36 48 54 64 72 81 96 108 144 162 216 243 324 486 729]
                                                               128       192       288       432       648       972      1458      2187                                                                 [1 2 3 4 6 8 9 12 16 18 24 27 32 36 48 54 64 72 81 96 108 128 144 162 192 216 243 288 324 432 486 648 729 972 1458 2187]
                                                          256       384       576       864      1296      1944      2916      4374      6561                                                            [1 2 3 4 6 8 9 12 16 18 24 27 32 36 48 54 64 72 81 96 108 128 144 162 192 216 243 256 288 324 384 432 486 576 648 729 864 972 1296 1458 1944 2187 2916 4374 6561]
                                                     512       768      1152      1728      2592      3888      5832      8748      13122     19683                                                      [1 2 3 4 6 8 9 12 16 18 24 27 32 36 48 54 64 72 81 96 108 128 144 162 192 216 243 256 288 324 384 432 486 512 576 648 729 768 864 972 1152 1296 1458 1728 1944 2187 2592 2916 3888 4374 5832 6561 8748 13122 19683]
                                               1024      1536      2304      3456      5184      7776      11664     17496     26244     39366     59049                                                 [1 2 3 4 6 8 9 12 16 18 24 27 32 36 48 54 64 72 81 96 108 128 144 162 192 216 243 256 288 324 384 432 486 512 576 648 729 768 864 972 1024 1152 1296 1458 1536 1728 1944 2187 2304 2592 2916 3456 3888 4374 5184 5832 6561 7776 8748 11664 13122 17496 19683 26244 39366 59049]
                                          2048      3072      4608      6912      10368     15552     23328     34992     52488     78732    118098    177147                                            [1 2 3 4 6 8 9 12 16 18 24 27 32 36 48 54 64 72 81 96 108 128 144 162 192 216 243 256 288 324 384 432 486 512 576 648 729 768 864 972 1024 1152 1296 1458 1536 1728 1944 2048 2187 2304 2592 2916 3072 3456 3888 4374 4608 5184 5832 6561 6912 7776 8748 10368 11664 13122 15552 17496 19683 23328 26244 34992 39366 52488 59049 78732 118098 177147]
                                     4096      6144      9216      13824     20736     31104     46656     69984    104976    157464    236196    354294    531441                                       [1 2 3 4 6 8 9 12 16 18 24 27 32 36 48 54 64 72 81 96 108 128 144 162 192 216 243 256 288 324 384 432 486 512 576 648 729 768 864 972 1024 1152 1296 1458 1536 1728 1944 2048 2187 2304 2592 2916 3072 3456 3888 4096 4374 4608 5184 5832 6144 6561 6912 7776 8748 9216 10368 11664 13122 13824 15552 17496 19683 20736 23328 26244 31104 34992 39366 46656 52488 59049 69984 78732 104976 118098 157464 177147 236196 354294 531441]
                                8192      12288     18432     27648     41472     62208     93312    139968    209952    314928    472392    708588    1062882   1594323                                 [1 2 3 4 6 8 9 12 16 18 24 27 32 36 48 54 64 72 81 96 108 128 144 162 192 216 243 256 288 324 384 432 486 512 576 648 729 768 864 972 1024 1152 1296 1458 1536 1728 1944 2048 2187 2304 2592 2916 3072 3456 3888 4096 4374 4608 5184 5832 6144 6561 6912 7776 8192 8748 9216 10368 11664 12288 13122 13824 15552 17496 18432 19683 20736 23328 26244 27648 31104 34992 39366 41472 46656 52488 59049 62208 69984 78732 93312 104976 118098 139968 157464 177147 209952 236196 314928 354294 472392 531441 708588 1062882 1594323]
                           16384     24576     36864     55296     82944    124416    186624    279936    419904    629856    944784    1417176   2125764   3188646   4782969                            [1 2 3 4 6 8 9 12 16 18 24 27 32 36 48 54 64 72 81 96 108 128 144 162 192 216 243 256 288 324 384 432 486 512 576 648 729 768 864 972 1024 1152 1296 1458 1536 1728 1944 2048 2187 2304 2592 2916 3072 3456 3888 4096 4374 4608 5184 5832 6144 6561 6912 7776 8192 8748 9216 10368 11664 12288 13122 13824 15552 16384 17496 18432 19683 20736 23328 24576 26244 27648 31104 34992 36864 39366 41472 46656 52488 55296 59049 62208 69984 78732 82944 93312 104976 118098 124416 139968 157464 177147 186624 209952 236196 279936 314928 354294 419904 472392 531441 629856 708588 944784 1062882 1417176 1594323 2125764 3188646 4782969]
                      32768     49152     73728    110592    165888    248832    373248    559872    839808    1259712   1889568   2834352   4251528   6377292   9565938  14348907                       [1 2 3 4 6 8 9 12 16 18 24 27 32 36 48 54 64 72 81 96 108 128 144 162 192 216 243 256 288 324 384 432 486 512 576 648 729 768 864 972 1024 1152 1296 1458 1536 1728 1944 2048 2187 2304 2592 2916 3072 3456 3888 4096 4374 4608 5184 5832 6144 6561 6912 7776 8192 8748 9216 10368 11664 12288 13122 13824 15552 16384 17496 18432 19683 20736 23328 24576 26244 27648 31104 32768 34992 36864 39366 41472 46656 49152 52488 55296 59049 62208 69984 73728 78732 82944 93312 104976 110592 118098 124416 139968 157464 165888 177147 186624 209952 236196 248832 279936 314928 354294 373248 419904 472392 531441 559872 629856 708588 839808 944784 1062882 1259712 1417176 1594323 1889568 2125764 2834352 3188646 4251528 4782969 6377292 9565938 14348907]
                 65536     98304    147456    221184    331776    497664    746496    1119744   1679616   2519424   3779136   5668704   8503056  12754584  19131876  28697814  43046721                  [1 2 3 4 6 8 9 12 16 18 24 27 32 36 48 54 64 72 81 96 108 128 144 162 192 216 243 256 288 324 384 432 486 512 576 648 729 768 864 972 1024 1152 1296 1458 1536 1728 1944 2048 2187 2304 2592 2916 3072 3456 3888 4096 4374 4608 5184 5832 6144 6561 6912 7776 8192 8748 9216 10368 11664 12288 13122 13824 15552 16384 17496 18432 19683 20736 23328 24576 26244 27648 31104 32768 34992 36864 39366 41472 46656 49152 52488 55296 59049 62208 65536 69984 73728 78732 82944 93312 98304 104976 110592 118098 124416 139968 147456 157464 165888 177147 186624 209952 221184 236196 248832 279936 314928 331776 354294 373248 419904 472392 497664 531441 559872 629856 708588 746496 839808 944784 1062882 1119744 1259712 1417176 1594323 1679616 1889568 2125764 2519424 2834352 3188646 3779136 4251528 4782969 5668704 6377292 8503056 9565938 12754584 14348907 19131876 28697814 43046721]
           131072    196608    294912    442368    663552    995328    1492992   2239488   3359232   5038848   7558272  11337408  17006112  25509168  38263752  57395628  86093442  129140163            [1 2 3 4 6 8 9 12 16 18 24 27 32 36 48 54 64 72 81 96 108 128 144 162 192 216 243 256 288 324 384 432 486 512 576 648 729 768 864 972 1024 1152 1296 1458 1536 1728 1944 2048 2187 2304 2592 2916 3072 3456 3888 4096 4374 4608 5184 5832 6144 6561 6912 7776 8192 8748 9216 10368 11664 12288 13122 13824 15552 16384 17496 18432 19683 20736 23328 24576 26244 27648 31104 32768 34992 36864 39366 41472 46656 49152 52488 55296 59049 62208 65536 69984 73728 78732 82944 93312 98304 104976 110592 118098 124416 131072 139968 147456 157464 165888 177147 186624 196608 209952 221184 236196 248832 279936 294912 314928 331776 354294 373248 419904 442368 472392 497664 531441 559872 629856 663552 708588 746496 839808 944784 995328 1062882 1119744 1259712 1417176 1492992 1594323 1679616 1889568 2125764 2239488 2519424 2834352 3188646 3359232 3779136 4251528 4782969 5038848 5668704 6377292 7558272 8503056 9565938 11337408 12754584 14348907 17006112 19131876 25509168 28697814 38263752 43046721 57395628 86093442 129140163]
      262144    393216    589824    884736    1327104   1990656   2985984   4478976   6718464  10077696  15116544  22674816  34012224  51018336  76527504  114791256 172186884 258280326 387420489       [1 2 3 4 6 8 9 12 16 18 24 27 32 36 48 54 64 72 81 96 108 128 144 162 192 216 243 256 288 324 384 432 486 512 576 648 729 768 864 972 1024 1152 1296 1458 1536 1728 1944 2048 2187 2304 2592 2916 3072 3456 3888 4096 4374 4608 5184 5832 6144 6561 6912 7776 8192 8748 9216 10368 11664 12288 13122 13824 15552 16384 17496 18432 19683 20736 23328 24576 26244 27648 31104 32768 34992 36864 39366 41472 46656 49152 52488 55296 59049 62208 65536 69984 73728 78732 82944 93312 98304 104976 110592 118098 124416 131072 139968 147456 157464 165888 177147 186624 196608 209952 221184 236196 248832 262144 279936 294912 314928 331776 354294 373248 393216 419904 442368 472392 497664 531441 559872 589824 629856 663552 708588 746496 839808 884736 944784 995328 1062882 1119744 1259712 1327104 1417176 1492992 1594323 1679616 1889568 1990656 2125764 2239488 2519424 2834352 2985984 3188646 3359232 3779136 4251528 4478976 4782969 5038848 5668704 6377292 6718464 7558272 8503056 9565938 10077696 11337408 12754584 14348907 15116544 17006112 19131876 22674816 25509168 28697814 34012224 38263752 43046721 51018336 57395628 76527504 86093442 114791256 129140163 172186884 258280326 387420489]
 524288    786432    1179648   1769472   2654208   3981312   5971968   8957952  13436928  20155392  30233088  45349632  68024448  102036672 153055008 229582512 344373768 516560652 774840978 1162261467 [1 2 3 4 6 8 9 12 16 18 24 27 32 36 48 54 64 72 81 96 108 128 144 162 192 216 243 256 288 324 384 432 486 512 576 648 729 768 864 972 1024 1152 1296 1458 1536 1728 1944 2048 2187 2304 2592 2916 3072 3456 3888 4096 4374 4608 5184 5832 6144 6561 6912 7776 8192 8748 9216 10368 11664 12288 13122 13824 15552 16384 17496 18432 19683 20736 23328 24576 26244 27648 31104 32768 34992 36864 39366 41472 46656 49152 52488 55296 59049 62208 65536 69984 73728 78732 82944 93312 98304 104976 110592 118098 124416 131072 139968 147456 157464 165888 177147 186624 196608 209952 221184 236196 248832 262144 279936 294912 314928 331776 354294 373248 393216 419904 442368 472392 497664 524288 531441 559872 589824 629856 663552 708588 746496 786432 839808 884736 944784 995328 1062882 1119744 1179648 1259712 1327104 1417176 1492992 1594323 1679616 1769472 1889568 1990656 2125764 2239488 2519424 2654208 2834352 2985984 3188646 3359232 3779136 3981312 4251528 4478976 4782969 5038848 5668704 5971968 6377292 6718464 7558272 8503056 8957952 9565938 10077696 11337408 12754584 13436928 14348907 15116544 17006112 19131876 20155392 22674816 25509168 28697814 30233088 34012224 38263752 43046721 45349632 51018336 57395628 68024448 76527504 86093442 102036672 114791256 129140163 153055008 172186884 229582512 258280326 344373768 387420489 516560652 774840978 1162261467]
                                                                                                   1                                                                                                     [1]
                                                                                              2         3                                                                                                [1 2 3]
                                                                                         4         6         9                                                                                           [1 2 3 4 6 9]
                                                                                    8        12        18        27                                                                                      [1 2 3 4 6 8 9 12 18 27]
                                                                              16        24        36        54        81                                                                                 [1 2 3 4 6 8 9 12 16 18 24 27 36 54 81]
                                                                         32        48        72        108       162       243                                                                           [1 2 3 4 6 8 9 12 16 18 24 27 32 36 48 54 72 81 108 162 243]
                                                                    64        96        144       216       324       486       729                                                                      [1 2 3 4 6 8 9 12 16 18 24 27 32 36 48 54 64 72 81 96 108 144 162 216 243 324 486 729]
                                                               128       192       288       432       648       972      1458      2187                                                                 [1 2 3 4 6 8 9 12 16 18 24 27 32 36 48 54 64 72 81 96 108 128 144 162 192 216 243 288 324 432 486 648 729 972 1458 2187]
                                                          256       384       576       864      1296      1944      2916      4374      6561                                                            [1 2 3 4 6 8 9 12 16 18 24 27 32 36 48 54 64 72 81 96 108 128 144 162 192 216 243 256 288 324 384 432 486 576 648 729 864 972 1296 1458 1944 2187 2916 4374 6561]
                                                     512       768      1152      1728      2592      3888      5832      8748      6561      9841                                                       [1 2 3 4 6 8 9 12 16 18 24 27 32 36 48 54 64 72 81 96 108 128 144 162 192 216 243 256 288 324 384 432 486 512 576 648 729 768 864 972 1152 1296 1458 1728 1944 2187 2592 2916 3888 4374 5832 6561 8748 9841]
                                               1024      1536      2304      3456      5184      7776       729      2187      6561      9841      7381                                                  [1 2 3 4 6 8 9 12 16 18 24 27 32 36 48 54 64 72 81 96 108 128 144 162 192 216 243 256 288 324 384 432 486 512 576 648 729 768 864 972 1024 1152 1296 1458 1536 1728 1944 2187 2304 2592 2916 3456 3888 4374 5184 5832 6561 7381 7776 8748 9841]
                                          2048      3072      4608      6912       81        243       729      2187      6561      9841      7381      5535                                             [1 2 3 4 6 8 9 12 16 18 24 27 32 36 48 54 64 72 81 96 108 128 144 162 192 216 243 256 288 324 384 432 486 512 576 648 729 768 864 972 1024 1152 1296 1458 1536 1728 1944 2048 2187 2304 2592 2916 3072 3456 3888 4374 4608 5184 5535 5832 6561 6912 7381 7776 8748 9841]
                                     4096      6144      9216       27        81        243       729      2187      6561      9841      7381      5535      8303                                        [1 2 3 4 6 8 9 12 16 18 24 27 32 36 48 54 64 72 81 96 108 128 144 162 192 216 243 256 288 324 384 432 486 512 576 648 729 768 864 972 1024 1152 1296 1458 1536 1728 1944 2048 2187 2304 2592 2916 3072 3456 3888 4096 4374 4608 5184 5535 5832 6144 6561 6912 7381 7776 8303 8748 9216 9841]
                                8192        3         9        27        81        243       729      2187      6561      9841      7381      5535      8303      6227                                   [1 2 3 4 6 8 9 12 16 18 24 27 32 36 48 54 64 72 81 96 108 128 144 162 192 216 243 256 288 324 384 432 486 512 576 648 729 768 864 972 1024 1152 1296 1458 1536 1728 1944 2048 2187 2304 2592 2916 3072 3456 3888 4096 4374 4608 5184 5535 5832 6144 6227 6561 6912 7381 7776 8192 8303 8748 9216 9841]
                             1         3         9        27        81        243       729      2187      6561      9841      7381      5535      8303      6227      9341                              [1 2 3 4 6 8 9 12 16 18 24 27 32 36 48 54 64 72 81 96 108 128 144 162 192 216 243 256 288 324 384 432 486 512 576 648 729 768 864 972 1024 1152 1296 1458 1536 1728 1944 2048 2187 2304 2592 2916 3072 3456 3888 4096 4374 4608 5184 5535 5832 6144 6227 6561 6912 7381 7776 8192 8303 8748 9216 9341 9841]
                        1         3         9        27        81        243       729      2187      6561      9841      7381      5535      8303      6227      9341      7006                         [1 2 3 4 6 8 9 12 16 18 24 27 32 36 48 54 64 72 81 96 108 128 144 162 192 216 243 256 288 324 384 432 486 512 576 648 729 768 864 972 1024 1152 1296 1458 1536 1728 1944 2048 2187 2304 2592 2916 3072 3456 3888 4096 4374 4608 5184 5535 5832 6144 6227 6561 6912 7006 7381 7776 8192 8303 8748 9216 9341 9841]
                   1         3         9        27        81        243       729      2187      6561      9841      7381      5535      8303      6227      9341      3503      5254                    [1 2 3 4 6 8 9 12 16 18 24 27 32 36 48 54 64 72 81 96 108 128 144 162 192 216 243 256 288 324 384 432 486 512 576 648 729 768 864 972 1024 1152 1296 1458 1536 1728 1944 2048 2187 2304 2592 2916 3072 3456 3888 4096 4374 4608 5184 5254 5535 5832 6144 6227 6561 6912 7006 7381 7776 8192 8303 8748 9216 9341 9841]
              1         3         9        27        81        243       729      2187      6561      9841      7381      5535      8303      6227      9341      3503      2627      7882               [1 2 3 4 6 8 9 12 16 18 24 27 32 36 48 54 64 72 81 96 108 128 144 162 192 216 243 256 288 324 384 432 486 512 576 648 729 768 864 972 1024 1152 1296 1458 1536 1728 1944 2048 2187 2304 2592 2916 3072 3456 3888 4096 4374 4608 5184 5254 5535 5832 6144 6227 6561 6912 7006 7381 7776 7882 8192 8303 8748 9216 9341 9841]
         1         3         9        27        81        243       729      2187      6561      9841      7381      5535      8303      6227      9341      3503      2627      3941      5911          [1 2 3 4 6 8 9 12 16 18 24 27 32 36 48 54 64 72 81 96 108 128 144 162 192 216 243 256 288 324 384 432 486 512 576 648 729 768 864 972 1024 1152 1296 1458 1536 1728 1944 2048 2187 2304 2592 2916 3072 3456 3888 4096 4374 4608 5184 5254 5535 5832 5911 6144 6227 6561 6912 7006 7381 7776 7882 8192 8303 8748 9216 9341 9841]
    1         3         9        27        81        243       729      2187      6561      9841      7381      5535      8303      6227      9341      3503      2627      3941      5911      8867     [1 2 3 4 6 8 9 12 16 18 24 27 32 36 48 54 64 72 81 96 108 128 144 162 192 216 243 256 288 324 384 432 486 512 576 648 729 768 864 972 1024 1152 1296 1458 1536 1728 1944 2048 2187 2304 2592 2916 3072 3456 3888 4096 4374 4608 5184 5254 5535 5832 5911 6144 6227 6561 6912 7006 7381 7776 7882 8192 8303 8748 8867 9216 9341 9841]
'''
########################################################################################################################################################################################################
