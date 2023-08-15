import pyglet.window.key   as pygwink
import pyglet.sprite       as pygsprt
import pyglet.image        as pygimg

from   tpkg import utl  as utl
#import tabs             as tabs
#from   tabs import Tabs as Tabs

SPR          = pygsprt.Sprite
slog         = utl.slog
#tobj         = None # Tabs
W, Y, Z      = utl.W, utl.Y, utl.Z

def test00(tobj):
    a = 1/0         ;  slog(f'{a=}')
    p = tobj.pages  ;  f = tobj.CSV_FILE
    a = [{'a':1, 'b':"2", 'c':3.00+1/3}]  ;  b = [ f'{p[i].y}' for i in range(len(p)) ]  ;  c = tobj.sobj.stringMap  ;  d = [ tobj.screens ]
    print(tobj.__class__.__name__, 'testA', a, sep=Y, file=f, end=Y)
    print(tobj.__class__.__name__, 'testB', b, sep=Y, file=f, end=Y)
    print(tobj.__class__.__name__, 'testC', c, sep=Y, file=f)
    print(tobj.__class__.__name__, 'testD', d, sep=Y, file=f)
    quit(Z.join(('test00', str(a))))
####################################################################################################################################################################################################
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
####################################################################################################################################################################################################
def test0(tobj, n, q=0):
    a = .314159265359
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
    slog(f'{tobj.ntsl()=}')
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
####################################################################################################################################################################################################
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
####################################################################################################################################################################################################
def tExit(tobj, why, e): #        dispatch_event('on_close')
    slog(f'BGN {why} {e}')
    sym, mod = 65507, 2
    slog(f'on_key_press   {sym} {mod} {pygwink.symbol_string(sym)} {pygwink.modifiers_string(mod)}')   ;   tobj.dispatch_event('on_key_press',   sym, mod)
    sym, mod = 65505, 3
    slog(f'on_key_press   {sym} {mod} {pygwink.symbol_string(sym)} {pygwink.modifiers_string(mod)}')   ;   tobj.dispatch_event('on_key_press',   sym, mod)
    sym, mod = 113, 3
    slog(f'on_key_press   {sym} {mod} {pygwink.symbol_string(sym)} {pygwink.modifiers_string(mod)}')   ;   tobj.dispatch_event('on_key_press',   sym, mod)
    sym, mod = 113, 3
    slog(f'on_key_release {sym} {mod} {pygwink.symbol_string(sym)} {pygwink.modifiers_string(mod)}')   ;   tobj.dispatch_event('on_key_release', sym, mod)
    sym, mod = 65505, 3
    slog(f'on_key_release {sym} {mod} {pygwink.symbol_string(sym)} {pygwink.modifiers_string(mod)}')   ;   tobj.dispatch_event('on_key_release', sym, mod)
    sym, mod = 65507, 2
    slog(f'on_key_release {sym} {mod} {pygwink.symbol_string(sym)} {pygwink.modifiers_string(mod)}')   ;   tobj.dispatch_event('on_key_release', sym, mod)
    slog(f'END {why} {e}')
