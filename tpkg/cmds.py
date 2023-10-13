from abc import ABC, abstractmethod
import itertools
import pyglet.text               as pygtxt
from   tpkg        import utl    as utl
from   tpkg        import kysgs  as kysgs
from   tpkg.notes  import Notes  as Notes

P, L, S, C,          T, N, I, K,          M, R, Q, H,          B, A, D, E   = utl.P, utl.L, utl.S, utl.C,    utl.T, utl.N, utl.I, utl.K,    utl.M, utl.R, utl.Q, utl.H,    utl.B, utl.A, utl.D, utl.E
W, X, Y, Z,       NONE,  ist,  fri,         slog,   fmtf,   fmtl,   fmtm    = utl.W, utl.X, utl.Y, utl.Z,    utl.NONE,   utl.ist,   utl.fri,       utl.slog,   utl.fmtf,   utl.fmtl,   utl.fmtm
BGC,  BOLD,  COLOR,     FONT_NAME,  FONT_SIZE, ITALIC,  KERNING,  UNDERLINE = utl.BGC,   utl.BOLD,  utl.COLOR,   utl.FONT_NAME, utl.FONT_SIZE, utl.ITALIC,   utl.KERNING,     utl.UNDERLINE

CAT,  CSV,  EVN,  LOG,  PNG,  TXT,  DAT  =     'cat' ,     'csv' ,     'evn',      'log' ,     'png' ,     'txt' ,     'dat'
CATS, CSVS, EVNS, LOGS, PNGS, TEXT, DATA =     'cats',     'csvs',     'evns',     'logs',     'pngs',     'text',     'data'
HARROWS, VARROWS      = ['LARROW', 'RARROW'], ['DARROW', 'UARROW']
FONT_NAMES            = utl.FONT_NAMES
LBL                   = pygtxt.Label

########################################################################################################################################################################################################

class Cmd(ABC):
    @abstractmethod
    def do(self): pass
    
    @abstractmethod
    def undo(self): pass
########################################################################################################################################################################################################
class TogArrowCmd(Cmd):
    def __init__(self, tobj, how, v, dbg):
        self.tobj, self.how, self.v, self.dbg = tobj, how, v, dbg

    def do(  self): self._togArrow()
    def undo(self): self._togArrow()
    
    def _togArrow(self):
        tobj, how, v, dbg = self.tobj, self.how, self.v, self.dbg
        if dbg: tobj.log(f'BGN {how} {v=} {tobj.hArrow=} = {HARROWS[tobj.hArrow]=} {tobj.vArrow=} = {VARROWS[tobj.vArrow]=}')
        if v:   tobj.vArrow  = (tobj.vArrow + 1) % len(VARROWS)
        else:   tobj.hArrow  = (tobj.hArrow + 1) % len(HARROWS)
        if dbg: tobj.log(f'END {how} {v=} {tobj.hArrow=} = {HARROWS[tobj.hArrow]=} {tobj.vArrow=} = {VARROWS[tobj.vArrow]=}')
########################################################################################################################################################################################################
class TogBlankCmd(Cmd):
    def __init__(self, tobj, how, a):
        self.tobj, self.how, self.a = tobj, how, a
    
    def do(  self):                  self._togBlank()
    def undo(self): self.a *= -1  ;  self._togBlank()
    
    def _togBlank(self):
        tobj, how, a = self.tobj, self.how, self.a
        prevBlank    =  tobj.tblank
        tobj.log(f'BGN {how} {prevBlank=}')
        tobj.tblanki = (tobj.tblanki + a) % len(tobj.tblanks)
        tobj.tblank  =  tobj.tblanks[tobj.tblanki]
        tobj.swapSrc, tobj.swapTrg, tobj.swapping = prevBlank, tobj.tblank, 2
        tobj.swapTab(how, '\r')
        tobj.swapSrc, tobj.swapTrg = Z, Z
        tobj.log(f'END {how} {tobj.tblank=}')
########################################################################################################################################################################################################
class TogFlatShrpCmd(Cmd):
    def __init__(self, tobj, how, dbg):
        self.tobj, self.how, self.dbg = tobj, how, dbg
    
    def do(  self): self._togFlatShrp()
    def undo(self): self._togFlatShrp()
    
    def _togFlatShrp(self):  #  page line colm tab or select
        tobj, how, dbg = self.tobj, self.how, self.dbg
        t1 = Notes.TYPE    ;    t2 =  Notes.TYPE * -1      ;     Notes.TYPE = t2
        tobj.log(  f'BGN {how} {t1=} {Notes.TYPES[t1]} => {t2=} {Notes.TYPES[t2]}')
        s = tobj.ss2sl()[0]  ;  np, nl, ns, nc, nt = tobj.i
        tniks, j, _, _tobj = tobj.tnikInfo(0, 0, s, 0, 0, why=how)
        for i in range(len(tniks)):
            text = Z  ;   sn = i % nt
            if   tobj.notes: text = tobj.notes[i].text
            elif tobj.kords and tobj.tabls:
                tabtxt = tobj.tabls[i].text
                text   = tobj.sobj.tab2nn(tabtxt, sn) if tobj.sobj.isFret(tabtxt) else tobj.tblank
            if text in Notes.N2I and (Notes.N2I[text] not in Notes.IS0):
                cc = i * ns    ;   old = text
                p, l, c, t = tobj.cc2plct(cc)   ;   cn = tobj.cc2cn(cc)
                if   text in Notes.F2S:  text = Notes.F2S[text]
                elif text in Notes.S2F:  text = Notes.S2F[text]
                tobj.notes[i].text     = text
                tobj.log(  f'{old:2} -> {text:2} = ')
                if dbg: tobj.log(f'{sn=} {cn=:2} {cc=:4} {i=:4} {old:2} => {text:2} {tobj.notes[i].text=:2} {tobj.fplct(p, l, c, t)}')
                if tobj.kords:
                    imap = tobj.getImap(p, l, c, dbg2=1)
                    tobj.setChord(imap, i, pos=1, dbg=1)
        kysgs.dumpNic(dict(tobj.nic))
        tobj.log(kysgs.fmtKSK(tobj.ks[kysgs.KSK]), f=2)
        tobj.log(  f'END {how} {t1=} {Notes.TYPES[t1]} => {t2=} {Notes.TYPES[t2]}')
########################################################################################################################################################################################################
class TogFullScrnCmd(Cmd):
    def __init__(self, tobj, how):
        self.tobj, self.how = tobj, how

    def do(  self): self._togFullScrn()
    def undo(self): self._togFullScrn()

    def _togFullScrn(self):
        tobj, how = self.tobj, self.how
        tobj.FULL_SCRN = not tobj.FULL_SCRN
        tobj.set_fullscreen( tobj.FULL_SCRN)
        tobj.log(   f'{how} {tobj.FULL_SCRN}=')
########################################################################################################################################################################################################
class TogPageCmd(Cmd):
    def __init__(self, tobj, how, a):
        self.tobj, self.how, self.a = tobj, how, a

    def do(  self): self._togPage()
    def undo(self): self._togPage()

    def _togPage(self):
        tobj, how, a = self.tobj, self.how, self.a
        tobj.log(f'BGN {how} {a=} {tobj.i[P]=}')
        cmd = TogVisibleCmd(tobj, how)  ;  cmd.do()
        tobj.i[P] = (tobj.j()[P] + a) % tobj.n[P] + 1
        tobj.log(f'    {how} {a=} {tobj.i[P]=}')
        cmd = TogVisibleCmd(tobj, how)  ;  cmd.do()
        tobj.dumpVisible()
        tobj.setCaption(f'{utl.ROOT_DIR}/{DATA}/{tobj.FILE_NAME}.{DAT} page {tobj.i[P]}')
        tobj.log(f'END {how} {a=} {tobj.i[P]=}')
########################################################################################################################################################################################################
class TogVisibleCmd(Cmd):
    def __init__(self, tobj, how, dbg=1):
        self.tobj, self.how, self.dbg = tobj, how, dbg
        
    def do(  self): self._togVisible()
    def undo(self): self._togVisible()
    
    def _togVisible(self):
        tobj, how, dbg = self.tobj, self.how, self.dbg
        why = 'FVis' if how is None else how       ;  np, nl, ns, nc, nt = tobj.n
        p, l, s, c  = tobj.j()[P], 0, 0, 0         ;  vl = []  ;  tpb, tpp, tpl, tps, tpc = tobj.ntp(dbg=1, dbg2=1)
        tobj.J1, tobj.J2 = tobj.p2Js(p)
        pid = f' {id(tobj.pages[p]):11x}' if tobj.OIDS else Z
        assert 0 <= p < len(tobj.pages), f'{p=} {len(tobj.pages)=} {tobj.fmtn()} {tobj.fmti()} {tobj.J1} {tobj.J2}'
        tobj.log(f'BGN {why} {pid} pages[{p}].v={int(tobj.pages[p].visible)} {tobj.fmti()} {tobj.fmtn()} page{p+1} is visibile {tobj.fVis()}')
        tobj.dumpTniksPfx(why, r=0)
        assert 0 <= p < len(tobj.pages), f'{p=} {len(tobj.pages)=}'
        page = tobj.pages[p]              ;  page.visible = not page.visible  ;  tobj.setJdump(P, p, page.visible, why=why)  ;  vl.append(str(int(page.visible))) if dbg else None
        for l in range(nl):
            line = tobj.lines[l]          ;  line.visible = not line.visible  ;  tobj.setJdump(L, l, line.visible, why=why)  ;  vl.append(str(int(line.visible))) if dbg else None
            for s, s2 in enumerate(tobj.ss2sl()):
                sect = tobj.sects[s]      ;  sect.visible = not sect.visible  ;  tobj.setJdump(S, s, sect.visible, why=why)  ;  vl.append(str(int(sect.visible))) if dbg else None
                for c in range(nc):
                    colm = tobj.colms[c]  ;  colm.visible = not colm.visible  ;  tobj.setJdump(C, c, colm.visible, why=why)  ;  vl.append(str(int(colm.visible))) if dbg else None
                    for t in range(nt):
                        tniks, j, k, txt = tobj.tnikInfo(p, l, s2, c, t, why=why)
                        t2 = t + c*tpc + l*tpl + p*tpp//ns
                        assert t2 < len(tniks),  f'ERROR {t2=} {len(tniks)=}'
                        tnik = tniks[t2]  ;  tnik.visible = not tnik.visible  ;  tobj.setJdump(j, t2, tnik.visible, why=why)  ;  vl.append(str(int(tnik.visible))) if dbg else None
        tobj.dumpTniksSfx(why)
        tobj.log(f'END {why} {pid} pages[{p}].v={int(tobj.pages[p].visible)} {tobj.fmti()} {tobj.fmtn()} page{p+1} is visible {tobj.fVis()}')
########################################################################################################################################################################################################
class TogKordNamesCmd(Cmd):
    def __init__(self, tobj, how, hit, dbg=1, dbg2=1):
        self.tobj, self.how, self.hit, self.dbg, self.dbg2 = tobj, how, hit, dbg, dbg2

    def do(  self): self._togKordNames()
    def undo(self): self._togKordNames()

    def _togKordNames(self):
        tobj, how, hit, dbg = self.tobj, self.how, self.hit, self.dbg
        cc = tobj.cc    ;    cn = tobj.cc2cn(cc)
        mks = list(tobj.cobj.mlimap.keys())   ;   sks = list(tobj.smap.keys())
        if sks and not hit:
            if dbg: tobj.dumpSmap(f'BGN {how} mks={fmtl(mks)} {cn=:2} {hit=} sks={fmtl(sks)}')
            [ self._togKordName(tobj, how, k) for k in sks ]
        else:
            if dbg: tobj.dumpSmap(f'BGN {how} mks={fmtl(mks)} {cn=:2} {hit=} sks={fmtl(sks)}')
            if hit: self._togKordNameHits(tobj, how, cn)
            else:   self._togKordName(tobj, how, cn)
        if dbg:     tobj.dumpSmap(f'END {how} mks={fmtl(mks)} {cn=:2} {hit=} sks={fmtl(sks)}')
        
    def _togKordNameHits(self, tobj, how, cn, dbg=1):
#        tobj, how, cn, dbg = self.tobj, self.how, self.cn, self.dbg
        mli = tobj.cobj.mlimap   ;   mks = list(mli.keys())   ;   cn2 = -1
        if cn not in mks: msg = f'ERROR: {cn=} not in {fmtl(mks)=}'   ;   tobj.log(msg)   ;   tobj.quit(msg)
        ivals =  [ u[1] for u in mli[cn][0] ]
        msg   =  [ fmtl(v, w="x") for v in ivals ]
        if dbg: tobj.log(f'BGN {how} mks={fmtl(mks)} cn={cn:2} ivals={fmtl(msg, d=Z)}')
        hits = self._ivalhits(tobj, ivals, how)
        for cn2 in hits:
            if cn2 not in tobj.smap: tobj.selectTabs(how, m=0, cn=cn2)
            self._togKordName(tobj, how, cn2)
        if dbg: tobj.log(f'END {how} mks={fmtl(mks)} cn2={cn2:2} ivals={fmtl(msg, d=Z)}')

    @staticmethod
    def _ivalhits(tobj, ivals, how, dbg=1):
        mli = tobj.cobj.mlimap    ;   mks = list(mli.keys())   ;   hits = set()
        for cn, lim in mli.items():
            for im in lim[0]:
                if cn in hits: break
                for iv in ivals:
                    iv1 = sorted(iv)  ;  iv2 = sorted(im[1])
                    if iv1 == iv2:       hits.add(cn)   ;   break
        if dbg: tobj.log(f'    {how} mks={fmtl(mks)} hits={fmtl(hits)}')
        return list(hits)

    @staticmethod
    def _togKordName(tobj, how, cn, dbg=1, dbg2=1):
#        tobj, how, cn, dbg, dbg2 = self.tobj, self.how, self.cn, self.dbg, self.dbg2
        cc = tobj.cn2cc(cn)            ;   mli = tobj.cobj.mlimap
        p, l, c, t = tobj.cc2plct(cc)  ;   msg = Z
        if not tobj.ikeys and not tobj.kords: msg +=  'ERROR: Both ikeys and chords are Empty '
        if cn not in mli:                     msg += f'ERROR: {cn=} not in mks={fmtl(list(mli.keys()))}'
        if msg: tobj.log(msg)          ;   return
        limap      = mli[cn][0]        ;   imi = mli[cn][1]
        imi        = (imi + 1) % len(limap)
        mli[cn][1] = imi
        ikeys, ivals, notes2, chordName, chunks, rank = limap[imi]
        if tobj.ikeys and ikeys:                tobj.setIkeyText(ikeys, cc, p, l, c)
        if tobj.kords and chordName and chunks: tobj.setChordName(cc, chordName, chunks)
        elif dbg: tobj.log(f'    {how} {cn=} {cc=} is NOT a chord')
        if dbg2:  tobj.cobj.dumpImap(limap[imi], why=f'{cn:2}')
#        assert imi == limap[imi][-1],   f'{imi=} {limap[imi][-1]=}'
########################################################################################################################################################################################################
class SetFontParamCmd(Cmd):
    def __init__(self, tobj, n, v, m, dbg=1):
        self.tobj, self.n, self.v, self.m, self.dbg = tobj, n, v, m, dbg

    def do(  self): self._setFontParam()
    def undo(self): self._setFontParam()
    
    def _setFontParam(self):
        tobj, n, v, m, dbg = self.tobj, self.n, self.v, self.m, self.dbg
        if   m == 'clrIdx':      v += getattr(tobj, m)   ;   v %= len(tobj.k)      ;  tobj.log(f'{n=:12} {v=:2} {tobj.clrIdx=:2}')
        elif m == 'fontNameIdx': v += getattr(tobj, m)   ;   v %= len(FONT_NAMES)  ;  tobj.log(f'{n=:12} {v=:2} {tobj.fontNameIdx=:2}')
        setattr(tobj, m, v)
        ts = list(itertools.chain(tobj.A, tobj.B, tobj.C))  ;  lt = len(ts)
        if dbg:         tobj.log(f'{lt=} {m=:12} {n=:12} {fmtf(v, 5)}')
        for j, t in enumerate(ts):
            tobj.setFontParam2(t, n, v, m, j)
        if dbg:         tobj.log(f'{lt=} {m=:12} {n=:12} {fmtf(v, 5)}')
        tobj.setCaption(tobj.fmtFont())

#    @staticmethod
#    def _setFontParam2(tobj, ts, n, v, m, j, dbg=1):
#        l = 0   ;   fb = 0   ;   fs = 1   ;   msg = Z
#        for i, t in enumerate(ts):
#            if ist(t, LBL):
#                if   m == 'clrIdx':       l = len(t.color)   ;  msg = f'{v=:2} tc={fmtl(t.color, w=3)}  ds={fmtl(t.document.get_style(n), w=3)}  kv={fmtl(tobj.k[v][fb][:l], w=3)}'
#                elif m == 'fontNameIdx':                        msg = f'{v=:2} {FONT_NAMES[v]=}'
#                elif m == 'fontSize':    fs = getattr(t, n)  ;  msg = f'{v=:.2f} {fs=:.2f}'
#                if dbg and ist(t, LBL) and i==0:            tobj.log(f'{j=:2} {i=:2}  {l} {fb} {m=:12} {n=:12} {msg}', f=2)
#                if   m == 'clrIdx':       tobj.setTNIKStyle2(t, tobj.k[v], tobj.fontStyle)
#                elif m == 'fontNameIdx':  setattr(t, n, FONT_NAMES[v])
#                elif m == 'fontSize':     setattr(t, n, v*fs)
#                else:                     setattr(t, n, v)
########################################################################################################################################################################################################
class TogDrwBGCCmd(Cmd):
    def __init__(self, tobj, how, a):
        self.tobj, self.how, self.a = tobj, how, a

    def do(  self): self._togDrwBGC()
    def undo(self): self._togDrwBGC()

    def _togDrwBGC(self):
        tobj, how, a = self.tobj, self.how, self.a
        tobj.drwBGC += a
        tobj.log(f'{how} {tobj.drwBGC=}')
########################################################################################################################################################################################################
class TogBGCCmd(Cmd):
    def __init__(self, tobj, how):
        self.tobj, self.how = tobj, how

    def do(  self): self._togBGC()
    def undo(self): self._togBGC()

    def _togBGC(self):
        tobj, how = self.tobj, self.how
        tobj.log(f'{how} {tobj.BGC=}') if how else None
        tobj.BGC = (1 + tobj.BGC) % 2
        tobj.setFontParam2(tobj.tabls, COLOR, tobj.BGC, 'clrIdx', T)
########################################################################################################################################################################################################
class SetNCmd(Cmd):
    def __init__(self, tobj, how, txt=Z, dbg=1):
        self.tobj, self.how, self.txt, self.dbg = tobj, how, txt, dbg
        
    def do(  self): self._setN()
    def undo(self): self._setN()
    
    def _setN(self):
        tobj, how, txt, dbg = self.tobj, self.how, self.txt, self.dbg
        if not tobj.settingN: tobj.settingN = 1   ;  tobj.setNtxt = Z  ;  tobj.log(f'BGN {how} {txt=} {tobj.settingN=} {tobj.setNvals=}') if dbg else None
        elif txt.isdecimal(): tobj.setNtxt += txt                      ;  tobj.log(   f'Concat {txt=} {tobj.settingN=} {tobj.setNvals=}') if dbg else None
        elif txt ==  W:       tobj.setNvals.append(int(tobj.setNtxt))  ;  tobj.log(   f'Append {txt=} {tobj.settingN=} {tobj.setNvals=}') if dbg else None  ;  tobj.setNtxt = Z
        elif txt == 'Q':      tobj.settingN = 0                        ;  tobj.log(   f'Cancel {txt=} {tobj.settingN=} {tobj.setNvals=}') if dbg else None
        elif txt == '\r':
            tobj.settingN = 0   ;   old = tobj.n
            tobj.setNvals.append(int(tobj.setNtxt))
            if len(tobj.setNvals) == 4:
                tobj.n[:2] = tobj.setNvals[:2]   ;   tobj.n[3:] = tobj.setNvals[2:]
            tobj.log(f'Setting {old=} {tobj.n=}')
            tobj.log(f'END {how} {txt=} {tobj.settingN=} {tobj.setNvals=}')
########################################################################################################################################################################################################
class RotSprCmd(Cmd):
    def __init__(self, tobj, how, spr, cw=1):
        self.tobj, self.how, self.spr, self.cw = tobj, how, spr, cw
    def do(  self): self._rotSpr()
    def undo(self): self._rotSpr()
    
    def _rotSpr(self):
        tobj, how, spr, cw = self.tobj, self.how, self.spr, self.cw
        old = spr.rotation
        spr.rotation =  (spr.rotation + cw * 10) % 360
        tobj.log(f'{how} {cw=} {old=} {spr.rotation=}', f=2)
########################################################################################################################################################################################################
