from abc import ABC, abstractmethod
import itertools
#import pyglet.text               as pygtxt
from   tpkg        import utl    as utl
from   tpkg        import kysgs  as kysgs
from   tpkg.notes  import Notes  as Notes

P, L, S, C,          T, N, I, K,          M, R, Q, H,          B, A, D, E   = utl.P, utl.L, utl.S, utl.C,    utl.T, utl.N, utl.I, utl.K,    utl.M, utl.R, utl.Q, utl.H,    utl.B, utl.A, utl.D, utl.E
W, X, Y, Z,       NONE,  ist,  fri,         slog,   fmtf,   fmtl,   fmtm    = utl.W, utl.X, utl.Y, utl.Z,    utl.NONE,   utl.ist,   utl.fri,       utl.slog,   utl.fmtf,   utl.fmtl,   utl.fmtm
BGC,  BOLD,  COLOR,     FONT_NAME,  FONT_SIZE, ITALIC,  KERNING,  UNDERLINE = utl.BGC,   utl.BOLD,  utl.COLOR,   utl.FONT_NAME, utl.FONT_SIZE, utl.ITALIC,   utl.KERNING,     utl.UNDERLINE

NORMAL_STYLE, SELECT_STYLE, CURRENT_STYLE = utl.NORMAL_STYLE, utl.SELECT_STYLE, utl.CURRENT_STYLE
CAT,  CSV,  EVN,  LOG,  PNG,  TXT,  DAT   = utl.CAT,  utl.CSV,  utl.EVN,  utl.LOG,  utl.PNG,  utl.TXT,  utl.DAT
CATS, CSVS, EVNS, LOGS, PNGS, TEXT, DATA  = utl.CATS, utl.CSVS, utl.EVNS, utl.LOGS, utl.PNGS, utl.TEXT, utl.DATA 

LBL, SPR              = utl.LBL, utl.SPR
CSR_MODES             = utl.CSR_MODES
HARROWS, VARROWS      = utl.HARROWS, utl.VARROWS
FONT_NAMES            = utl.FONT_NAMES

########################################################################################################################################################################################################

class Cmd(ABC):
    @abstractmethod
    def do(self): pass
    
    @abstractmethod
    def undo(self): pass
########################################################################################################################################################################################################
class TogArrowCmd(Cmd):
    def __init__(self, tobj, how, v, dbg=1):
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
    def __init__(self, tobj, how, dbg=1):
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
class SetFontPrmCmd(Cmd):
    def __init__(self, tobj, n, v, m, dbg=1):
        self.tobj, self.n, self.v, self.m, self.dbg = tobj, n, v, m, dbg

    def do(  self): self._setFontPrm()
    def undo(self): self._setFontPrm()
    
    def _setFontPrm(self):
        tobj, n, v, m, dbg = self.tobj, self.n, self.v, self.m, self.dbg
        if   m == 'clrIdx':      v += getattr(tobj, m)   ;   v %= len(tobj.k)      ;  tobj.log(f'{n=:12} {v=:2} {tobj.clrIdx=:2}')
        elif m == 'fontNameIdx': v += getattr(tobj, m)   ;   v %= len(FONT_NAMES)  ;  tobj.log(f'{n=:12} {v=:2} {tobj.fontNameIdx=:2}')
        setattr(tobj, m, v)
        ts = list(itertools.chain(tobj.A, tobj.B, tobj.C))  ;  lt = len(ts)
        if dbg:         tobj.log(f'{lt=} {m=:12} {n=:12} {fmtf(v, 5)}')
        for j, t in enumerate(ts):
            tobj.setFontPrm2(t, n, v, m, j)
        if dbg:         tobj.log(f'{lt=} {m=:12} {n=:12} {fmtf(v, 5)}')
        tobj.setCaption(tobj.fmtFont())

#    @staticmethod
#    def _setFontPrm2(tobj, ts, n, v, m, j, dbg=1):
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
        tobj.setFontPrm2(tobj.tabls, COLOR, tobj.BGC, 'clrIdx', T)
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
class SetCHVModeCmd(Cmd):
    def __init__(self, tobj, how, c=None, h=None, v=None):
        self.tobj, self.how, self.c, self.h, self.v = tobj, how, c, h, v

    def do(  self): self._setCHVMode()
    def undo(self): self._setCHVMode()

    def _setCHVMode(self):
        tobj, how, c, h, v = self.tobj, self.how, self.c, self.h, self.v
        tobj.dumpCursorArrows(f'BGN {how:7} c={NONE if c is None else c:<4} h={NONE if h is None else h:<4} v={NONE if v is None else v:<4}')
        if c is not None: tobj.csrMode = c
        if h is not None: tobj.hArrow  = h
        if v is not None: tobj.vArrow  = v
        tobj.dumpCursorArrows(f'END {how:7} c={NONE if c is None else c:<4} h={NONE if h is None else h:<4} v={NONE if v is None else v:<4}')
########################################################################################################################################################################################################
class TogCsrModeCmd(Cmd):
    def __init__(self, tobj, how, a):
        self.tobj, self.how, self.a = tobj, how, a

    def do(  self): self._togCsrMode()
    def undo(self): self._togCsrMode()
        
    def _togCsrMode(self):
        tobj, how, a = self.tobj, self.how, self.a
        c = tobj.csrMode  ;  h = tobj.hArrow  ;  v = tobj.vArrow
        tobj.dumpCursorArrows(f'BGN {how} {a=} {c=} {h=} {v=}')
        tobj.csrMode = (tobj.csrMode + a) % len(CSR_MODES)
        tobj.dumpCursorArrows(f'END {how} {a=} {c=} {h=} {v=}')
########################################################################################################################################################################################################
class CsrJumpCmd(Cmd):
    def __init__(self, tobj, how, txt, abso):
        self.tobj, self.how, self.txt, self.abso = tobj, how, txt, abso

    def do(  self): self._csrJump()
    def undo(self): self._csrJump()

    def _csrJump(self):
        tobj, how, txt, abso = self.tobj, self.how, self.txt, self.abso
        cc = tobj.cursorCol()            ;            tobj.jumpAbs = abso
        tobj.log(    f'{how} {txt=} {abso=} {cc=} jt={tobj.jumpAbs} {tobj.fmti()}')
        if not tobj.jumping:                          tobj.jumping = 1
        elif txt.isdecimal():                         tobj.jumpStr += txt
        elif txt == '-' and not tobj.jumpStr:         tobj.jumpStr += txt
        elif txt == W:
            tobj.log(f'{how} {txt=} {abso=} {cc=} jt={tobj.jumpAbs} {tobj.jumpStr=} {tobj.fmti()}')
            jcc  = tobj.n[T] * int(tobj.jumpStr)
            tobj.jumping = 0   ;   tobj.jumpStr = Z
            tobj.move(how, jcc - 1 - abso * cc)
            tobj.log(f'{how} {txt=} {abso=} {cc=} jt={tobj.jumpAbs} {jcc=} moved={jcc - 1 - abso * cc} {tobj.fmti()}')
########################################################################################################################################################################################################
class ShiftTabsCmd(Cmd):
    def __init__(self, tobj, how, nf=0):
        self.tobj, self.how, self.nf = tobj, how, nf

    def do(  self): self._shiftTabs()
    def undo(self): self._shiftTabs()

    def _shiftTabs(self):
        tobj, how, nf = self.tobj, self.how, self.nf
        tobj.dumpSmap(f'BGN {how} {tobj.shiftingTabs=} {nf=}')
        if not tobj.shiftingTabs:
            tobj.shiftingTabs = 1
            for k, v in tobj.smap.items():
                tobj.setLLStyle(k, NORMAL_STYLE) if tobj.LL else None
            tobj.setCaption('Enter nf: number of frets to shift +/- int')
        elif nf == '-': tobj.shiftSign = -1
        elif tobj.sobj.isFret(nf):
            tobj.shiftingTabs = 0     ;   nt = tobj.n[T]
            for cn, v in tobj.smap.items():
                cc = tobj.cn2cc(cn)   ;   p, l, c, r = tobj.cc2plct(cc, dbg=0)
                tobj.log(f'{cc=} {cn=} {v=} text={v}')
                for t in range(nt):
                    text = v[t]    ;    kt = cc + t    ;    fn = 0   ;   ntones = Notes.NTONES * 2
                    if tobj.sobj.isFret(text):
                        fn = tobj.afn(str((tobj.sobj.tab2fn(text) + tobj.shiftSign * tobj.sobj.tab2fn(nf)) % ntones))  ;  tobj.log(f'{cc=} {cn=} {t=} {text=} {nf=} {fn=} {tobj.shiftSign=}')
                    if fn and tobj.sobj.isFret(fn):  tobj.setDTNIK(fn, kt, p, l, c, t, kk=1 if t==nt-1 else 0)
            tobj.shiftSign = 1
            tobj.rsyncData = 1
            tobj.unselectAll('shiftTabs()')
        tobj.dumpSmap(f'END {how} {tobj.shiftingTabs=} {nf=} {tobj.shiftSign=}')
########################################################################################################################################################################################################
class SwapTabCmd(Cmd):
    def __init__(self, tobj, how, txt=Z, data=None, dbg=0, dbg2=0):
        self.tobj, self.how, self.txt, self.data, self.dbg, self.dbg2 = tobj, how, txt, data, dbg, dbg2
        
    def do(  self): self._swapTab()
    def undo(self): self._swapTab()
    
    def _swapTab(self):  # e.g. c => 12 not same # chars asserts
        tobj, how, txt, data, dbg, dbg2 = self.tobj, self.how, self.txt, self.data, self.dbg, self.dbg2
        src, trg = tobj.swapSrc, tobj.swapTrg
        data = data or tobj.data
        if not tobj.swapping: tobj.swapping = 1
        elif txt.isalnum() or txt in tobj.tblanks:
            if   tobj.swapping == 1:   src += txt;   tobj.log(f'    {how} {txt=} {tobj.swapping=} {src=} {trg=}') # optimize str concat?
            elif tobj.swapping == 2:   trg += txt;   tobj.log(f'    {how} {txt=} {tobj.swapping=} {src=} {trg=}') # optimize str concat?
            tobj.swapSrc, tobj.swapTrg = src, trg
        elif txt == '\r':
            tobj.log(f'    {how} {tobj.swapping=} {src=} {trg=}')
            if   tobj.swapping == 1 and not trg: tobj.swapping = 2;   tobj.log(f'{how} waiting {src=} {trg=}') if dbg else None   ;   return
            if   tobj.swapping == 2 and trg:     tobj.swapping = 0;   tobj.log(f'{how} BGN     {src=} {trg=}') if dbg else None
            np, nl, ns, nc, nt = tobj.n    ;     nc += tobj.zzl()
            cc0 = tobj.cursorCol()         ;     p0, l0, c0, t0 = tobj.cc2plct(cc0)   ;   tobj.log(f'BFR {cc0=} {p0=} {l0=} {c0=} {t0=}')
            blanks = tobj.tblanks          ;     blank = 1 if src in blanks and trg in blanks else 0
            if blank:
                for t in tobj.tabls:   t.text = trg if t.text==src else t.text
                for n in tobj.notes:   n.text = trg if n.text==src else n.text
                for i in tobj.ikeys:   i.text = trg if i.text==src else i.text
                for k in tobj.kords:   k.text = trg if k.text==src else k.text
            for p in range(np):
                for l in range(nl):
                    for c in range(nc):
                        text = data[p][l][c]
                        for t in range(nt):
                            if text[t] == src:
                                if dbg2: tobj.log(f'Before data{tobj.fplc(p, l, c)}={text}')
                                if blank and trg != tobj.tblank:
                                    text[t] = trg
                                cc = tobj.plct2cc(p, l, c, t)   ;   tobj.setDTNIK(trg, cc, p, l, c, t, kk=1)
                                if dbg2: tobj.log(f'After  data{tobj.fplc(p, l, c)}={text}')
            tobj.swapSrc, tobj.swapTrg = Z, Z
            tobj.log(f'{how} END     {src=} {trg=}') if dbg else None
#                if dbg2: self.dumpTniks('SWAP')
#                self.moveTo(how, p0, l0, c0, t0)  ;  cc = self.cursorCol()  ;  self.log(f'AFT {cc0=} {p0=} {l0=} {c0=} {t0=} {cc=}')
            if tobj.SNAPS: tobj.regSnap(f'{how}', 'SWAP')
            tobj.rsyncData = 1
########################################################################################################################################################################################################
class TogLLsCmd(Cmd):
    def __init__(self, tobj, how, dbg=1):
        self.tobj, self.how, self.dbg = tobj, how, dbg

    def do(  self): self._togLLs()
    def undo(self): self._togLLs()
    
    def _togLLs(self):
        tobj, how, dbg = self.tobj, self.how, self.dbg
        tobj.flipLL()
        msg2 = f'{how} {tobj.LL=}'
        tobj.dumpGeom('BGN', f'     {msg2}')
        if dbg: tobj.log(f'    llText={fmtl(tobj.llText[1-tobj.zzl():])}')
        if tobj.LL and not tobj.rowLs: msg = 'ADD'    ;   tobj.addLLs( how)
        else:                          msg = 'HIDE'   ;   tobj.hideLLs(how)
        tobj.on_resize(tobj.width, tobj.height)
        tobj.dumpGeom('END', f'{msg} {msg2}')
########################################################################################################################################################################################################
class TogTTsCmd(Cmd):
    def __init__(self, tobj, how, tt):
        self.tobj, self.how, self.tt = tobj, how, tt

    def do(  self): self._togTTs()
    def undo(self): self._togTTs()

    def _togTTs(self):
        tobj, how, tt = self.tobj, self.how, self.tt
        msg2 = f'{how} {tt=}'
        tobj.dumpGeom('BGN', f'     {msg2}')
        if   tt not in tobj.SS and not tobj.B[tt]: msg = 'ADD'    ;   tobj.addTTs( how, tt)
        elif tt     in tobj.SS:                    msg = 'HIDE'   ;   tobj.hideTTs(how, tt)
        else:                                      msg = 'SKIP'   ;   tobj.dumpGeom(W*3, f'{msg} {msg2}')   ;   tobj.flipTT(tt)
        tobj.on_resize(tobj.width, tobj.height)
        tobj.dumpGeom('END', f'{msg} {msg2}')
########################################################################################################################################################################################################
class TogSelectAllCmd(Cmd):
    def __init__(self, tobj, how):
        self.tobj, self.how = tobj, how

    def do(  self): self._togSelectAll()
    def undo(self): self._togSelectAll()
        
    def _togSelectAll(self):
        tobj, how = self.tobj, self.how
        tobj.dumpSmap(f'BGN {how} {tobj.allTabSel=}')
        if   tobj.allTabSel:       tobj.unselectAll(how)   ;   tobj.allTabSel = 0
        else:                      tobj.selectAll(how)     ;   tobj.allTabSel = 1
        tobj.dumpSmap(f'END {how} {tobj.allTabSel=}')
########################################################################################################################################################################################################
class Go2FirstTabCmd(Cmd):
    def __init__(self, tobj, how, page=0, dbg=1):
        self.tobj, self.how, self.page, self.dbg = tobj, how, page, dbg
        
    def do(  self): self._move2FirstTab()
    def undo(self): self._move2FirstTab() # todo fixme
    
    def _move2FirstTab(self):
        tobj, how, page, dbg = self.tobj, self.how, self.page, self.dbg
        np, nl, ns, nc, nt = tobj.n    ;   p, l, s, c, t = tobj.j()  ;  i = p
        n = p * nl + l     ;   tp = nc * nt
        if page: tp *= nl  ;  n //= nl
        if dbg:    tobj.log(f'BGN {how} {page=} {tobj.fplct()} {i=:4} {n=} {tp=:3} {tp*n=:4} for({tp*n:4}, {tp*(n+1):4}, 1)', pos=1)
        for i in range(tp*n, tp*(n+1), 1):
            if not tobj.sobj.isFret(tobj.tabls[i].text): continue
            p, l, c, t = tobj.cc2plct(i, dbg=1)  ;  break
        tobj.moveTo(how, p, l, c, t, dbg=dbg)
        if dbg:    tobj.log(f'END {how} {page=} {tobj.fplct()} {i=:4} {n=} {tp=:3} {tp*n=:4} for({tp*n:4}, {tp*(n+1):4}, 1)', pos=1)
########################################################################################################################################################################################################
class Go2LastTabCmd(Cmd):
    def __init__(self, tobj, how, page=0, dbg=1):
        self.tobj, self.how, self.page, self.dbg = tobj, how, page, dbg  

    def do(  self): self._move2LastTab()
    def undo(self): self._move2LastTab() # todo fixme
    
    def _move2LastTab(self):
        tobj, how, page, dbg = self.tobj, self.how, self.page, self.dbg
        np, nl, ns, nc, nt = tobj.n    ;   p, l, s, c, t = tobj.j()  ;  i = p
        n = p * nl + l     ;   tp = nc * nt
        if page: tp *= nl  ;  n //= nl
        if dbg:    tobj.log(f'BGN {how} {page=} {tobj.fplct()} {i=:4} {n=} {tp=:3} {tp*n=:4} for({tp*(n+1)-1:4}, {tp*n-1:4}, -1)', pos=1)
        for i in range(tp*(n+1)-1, tp*n-1, -1):
            if not tobj.sobj.isFret(tobj.tabls[i].text): continue
            p, l, c, t = tobj.cc2plct(i, dbg=1)  ;  break
        tobj.moveTo(how, p, l, c, t, dbg=dbg)
        if dbg:    tobj.log(f'END {how} {page=} {tobj.fplct()} {i=:4} {n=} {tp=:3} {tp*n=:4} for({tp*(n+1)-1:4}, {tp*n-1:4}, -1)', pos=1)

########################################################################################################################################################################################################
class InsertSpaceCmd(Cmd):
    def __init__(self, tobj, how, txt='0', dbg=1):
        self.tobj, self.how, self.txt, self.dbg = tobj, how, txt, dbg
        
    def do(  self): self._insertSpace()
    def undo(self): self._insertSpace() # todo fixme
    
    def _insertSpace(self):
        tobj, how, txt, dbg = self.tobj, self.how, self.txt, self.dbg
        cc = tobj.cursorCol()   ;  c0 = tobj.cc2cn(cc)
        if not tobj.inserting:
            tobj.inserting = 1  ;  tobj.setCaption('Enter nc: number of cols to indent int')
        elif txt.isdecimal():
            tobj.insertStr += txt
        elif txt in (W, '\r'):
            tobj.inserting = 0
            width = int(tobj.insertStr)
            tcs   = sorted(tobj.cobj.mlimap)
            tcs.append(tobj.n[C] * tobj.n[L] - 1)
            tcs   = [ t + 1 for t in tcs ]
            if dbg: tobj.log(f'BGN {how} Searching for space to insert {width} cols starting at colm {c0}')
            tobj.log(f'{fmtl(tcs, ll=1)} insertSpace', p=0)
            found, c1, c2 = 0, 0, None   ;   tobj.insertStr = Z
            for c2 in tcs:
                if dbg: tobj.log(f'w c0 c1 c2 = {width} {c0} {c1} {c2}')
                if c2 > c0 + width and c2 > c1 + width: found = 1  ;  break
                c1 = c2
            if not found: tobj.log(f'{how} starting at colm {c0} No room to insert {width} cols before end of page at colm {tcs[-1]+1}')  ;   return
            tobj.log(f'{how} starting at colm {c0} Found a gap {width} cols wide between cols {c1} and {c2}')
            tobj.log(f'select cols {c0} ... {c1}, cut cols, move ({width} - {c1} + {c0})={width-c1+c0} cols, paste cols')
            [ tobj.selectTabs(how, m=tobj.tpc) for _ in range(c1 - c0) ]
            tobj.cutTabs(how)
            tobj.move(how, (width - c1 + c0) * tobj.tpc)
            tobj.pasteTabs(how)
            tobj.unselectAll(how)
########################################################################################################################################################################################################
class SwapColsCmd(Cmd):
    def __init__(self, tobj, how):
        self.tobj, self.how = tobj, how
        
    def do(  self): self._swapCols()
    def undo(self): self._swapCols() # todo fixme
    
    def _swapCols(self):
        tobj, how = self.tobj, self.how
        nk = len(tobj.smap)   ;   nk2 = nk // 2
        tobj.dumpSmap(f'BGN {nk=} {nk2=}')
        for i in range(nk2):
            k1 = list(tobj.smap.keys())[i]
            k2 = list(tobj.smap.keys())[nk - 1 - i]
            text1 = tobj.smap[k1]
            text2 = tobj.smap[k2]
            tobj.smap[k1] = text2
            tobj.smap[k2] = text1
        tobj.dumpSmap(f'    {nk=} {nk2=}')
        tobj.pasteTabs(how)
        tobj.dumpSmap(f'END {nk=} {nk2=}')
########################################################################################################################################################################################################
class AddPageCmd(Cmd):
    def __init__(self, tobj, how, ins=None, dbg=1):
        self.tobj, self.how, self.ins, self.dbg = tobj, how, ins, dbg
        
    def do(  self): self._addPage()
    def undo(self): self._addPage() # todo fixme
    
    def _addPage(self):
        tobj, how, ins, dbg = self.tobj, self.how, self.ins, self.dbg
        np, nl, ns, nc, nt = tobj.n   ;   how = f'{how} {ins=}'
        tobj.dumpBlanks() # tobj.j()[P]
#        if ins is not None: tobj.flipPage(how)
        if ins is not None: tobj.flipVisible(how=how)
        tobj.n[P] += 1   ;   kl = tobj.k[P]
        data      = [ [ tobj.tblankRow for _ in range(nt) ] for _ in range(nl) ]
        tobj.data = tobj.transposeData(dmp=dbg)
        tobj.data.append(data) if ins is None else tobj.data.insert(ins, data)
        tobj.data = tobj.transposeData(dmp=dbg)
        if ins is None: tobj.dumpTniksPfx(how, r=0)   ;   pi = len(tobj.pages)
        else:           tobj.dumpTniksPfx(how, r=1)   ;   pi = tobj.J1[P]
        tobj.J1[L], tobj.J1[S], tobj.J1[C], tobj.J1[T] = 0, 0, 0, 0
        n, ii, x, y, w, h =    tobj.geom(M, n=1, i=1, dbg=1)   ;   kk = tobj.cci(P, 0, kl) if tobj.CHECKERED else 0
        tobj.newC += 1  ;  why2 = f'New{tobj.newC}'  ;  why = why2  ;  k = kl[kk]
        page = tobj.createTnik(tobj.pages,   pi, P, x, y, w, h, k, why=why, v=0, dbg=1)
        for line in            tobj.g_createTniks(tobj.lines,  L, page, why=why):
            for sect in        tobj.g_createTniks(tobj.sects,  S, line, why=why):
                for colm in    tobj.g_createTniks(tobj.colms,  C, sect, why=why):
                    for _ in   tobj.g_createTniks(tobj.tabls,  T, colm, why=why): pass
        tobj.dumpTniksSfx(how)
        if tobj.SNAPS and dbg: tobj.regSnap(how, why2)
########################################################################################################################################################################################################
class EraseTabsCmd(Cmd):
    def __init__(self, tobj, how): #, reset=0
        self.tobj, self.how = tobj, how
        
    def do(  self): self._eraseTabs()
    def undo(self): self._eraseTabs() # todo fixme
    
    def _eraseTabs(self):
        tobj, how = self.tobj, self.how
        np, nl, ns, nc, nt = tobj.n   ;   nz = tobj.zzl()  ;  nc += nz
        tobj.log(f'BGN {how} {np=} {nl=} {ns=} {nc=} {nt=}')
        tobj.nic.clear()
        tobj.dumpBlanks()
        for t in tobj.tabls:
            t.text = tobj.tblank
        for n in tobj.notes:
            n.text = tobj.tblank
        for i in tobj.ikeys:
            i.text = tobj.tblank
        for k in tobj.kords:
            k.text = tobj.tblank
        for p in range(np):
            for l in range(nl):
                for c in range(nz, nc):
                    tobj.data[p][l][c-nz] = tobj.tblankCol
        tobj.log(f'END {how} {np=} {nl=} {ns=} {nc=} {nt=}')
        tobj.rsyncData = 1
########################################################################################################################################################################################################
class ResetCmd(Cmd):
    def __init__(self, tobj, how):
        self.tobj, self.how = tobj, how
        
    def do(  self): self._reset()
    def undo(self): self._reset() # todo fixme
    
    def _reset(self):
        tobj, how = self.tobj, self.how
        tobj.dumpGeom('BGN', f'{how} before cleanup()')
        tobj.cleanup()
        tobj.dumpGeom('   ', f'{how} after cleanup() / before reinit()')
        tobj._reinit()            # todo fixme
        tobj.dumpGeom('END', f'{how} after reinit()')
########################################################################################################################################################################################################
class CopyTabsCmd(Cmd):
    def __init__(self, tobj, how, dbg=1):
        self.tobj, self.how, self.dbg = tobj, how, dbg
        
    def do(  self): self._copyTabs()
    def undo(self): self._copyTabs() # todo fixme
    
    def _copyTabs(self):
        tobj, how, dbg = self.tobj, self.how, self.dbg
        tobj.dumpSmap(f'BGN {how}')   ;   nt = tobj.n[T]   ;   style = NORMAL_STYLE   ;   text = []
        for k in list(tobj.smap.keys()):
            k *= nt
            if tobj.LL:  tobj.setLLStyle(k, style)
            text.append(tobj.setTNIKStyle(k, nt, style))
            if dbg: text.append(W)
        if dbg:         tobj.log(f'{Z.join(text)=}')
        tobj.dumpSmap(f'END {how}')
        if tobj.SNAPS:  tobj.regSnap(f'{how}', 'COPY')
########################################################################################################################################################################################################
class DeleteTabsCmd(Cmd):
    def __init__(self, tobj, how, keep=0, dbg=1):
        self.tobj, self.how, self.keep, self.dbg = tobj, how, keep, dbg
        
    def do(  self): self._deleteTabs()
    def undo(self): self._deleteTabs() # todo fixme
    
    def _deleteTabs(self):
        tobj, how, keep, dbg = self.tobj, self.how, self.keep, self.dbg
        tobj.dumpSmap(f'BGN {how} {keep=}')   ;   style = NORMAL_STYLE   ;   nt = tobj.n[T]
        for k, text in tobj.smap.items():
            cn = k   ;   k *= nt
            if dbg:     tobj.log(f'{k=} {cn=} {text=}')
            if tobj.LL: tobj.setLLStyle(k, style)
            tobj.setTNIKStyle(k, nt, style, blank=1)
        if not keep:    tobj.unselectAll(f'deleteTabs({keep=})')
        tobj.dumpSmap(f'END {how} {keep=}')
        if tobj.SNAPS:  tobj.regSnap(f'{how}', 'DELT')
        tobj.rsyncData = 1
########################################################################################################################################################################################################
class PasteTabsCmd(Cmd):
    def __init__(self, tobj, how, kk=0, dbg=1):
        self.tobj, self.how, self.kk, self.dbg = tobj, how, kk, dbg
        
    def do(  self): self._pasteTabs()
    def undo(self): self._pasteTabs() # todo fixme
    
    def _pasteTabs(self):
        tobj, how, kk, dbg = self.tobj, self.how, self.kk, self.dbg
        cc = tobj.cursorCol()       ;   nt = tobj.n[T]
        cn = tobj.normalizeCC(cc)   ;   kt = 0
        p, l, s, c, t = tobj.j()
        tobj.dumpSmap(f'BGN {how} {kk=} {cc=} {cn=}={tobj.cc2cn(cc)} plct={tobj.fplct(p, l, c, t)}')
        for i, (k, text) in enumerate(tobj.smap.items()):
            if not i:   dk = 0
            elif kk:    dk = i * nt
            else:       dk = (list(tobj.smap.keys())[i] - list(tobj.smap.keys())[0]) * nt
            if dbg:     tobj.log(f'{i=} {k=} {text=} {kk=} {dk=}')
            for n in range(nt):
                kt         = (cn + dk + n) % tobj.tpp # todo
                p, l, c, t = tobj.cc2plct(kt)
                tobj.setDTNIK(text[n], kt, p, l, c, n, kk=1 if n==nt-1 else 0)
            if dbg:     tobj.log(f'{i=} {k=} {text=} {kk=} {dk=} {kt=}')
        tobj.log(f'clearing {len(tobj.smap)=}')   ;   tobj.smap.clear()
        tobj.dumpSmap(f'END {how} {kk=} {cc=} {cn=}={tobj.cc2cn(cc)} plct={tobj.fplct(p, l, c, t)}')
        if tobj.SNAPS:  tobj.regSnap(f'{how}', 'PAST')
        tobj.rsyncData = 1
########################################################################################################################################################################################################
class CutTabsCmd(Cmd):
    def __init__(self, tobj, how):
        self.tobj, self.how = tobj, how
        
    def do(  self): self._cutTabs()
    def undo(self): self._cutTabs() # todo fixme
    
    def _cutTabs(self):
        tobj, how = self.tobj, self.how
        tobj.log('BGN Cut = Copy + Delete')
        cmd = CopyTabsCmd(tobj, how)            ;  cmd.do()
        tobj.log('Cut = Copy + Delete')
        cmd = DeleteTabsCmd(tobj, how, keep=1)  ;  cmd.do()
        tobj.log('END Cut = Copy + Delete')
########################################################################################################################################################################################################
class MoveCursorCmd(Cmd):
    def __init__(self, tobj, ss=0, why=Z, dbg=1):
        self.tobj, self.ss, self.why, self.dbg = tobj, ss, why, dbg
        
    def do(  self): self._moveCursor()
    def undo(self): self._moveCursor() # todo fixme
    
    def _moveCursor(self):
        tobj, ss, why, dbg = self.tobj, self.ss, self.why, self.dbg
        if dbg:           tobj.log(f'BGN {ss=} {tobj.cc=}', pos=1)
        if tobj.LL:       tobj.setLLStyle(tobj.cc, SELECT_STYLE if ss else NORMAL_STYLE)
        cmd = ResizeCursorCmd(tobj, why, dbg=dbg)         ;  cmd.do()
        if tobj.LL:       tobj.setLLStyle(tobj.cc, CURRENT_STYLE)
        if dbg:           tobj.log(f'END {ss=} {tobj.cc=}', pos=1)
########################################################################################################################################################################################################
class ResizeCursorCmd(Cmd):
    def __init__(self, tobj, why, dbg=1):
        self.tobj, self.why, self.dbg = tobj, why, dbg
        
    def do(  self): self._resizeCursor()
    def undo(self): self._resizeCursor() # todo fixme
    
    def _resizeCursor(self):
        tobj, why, dbg = self.tobj, self.why, self.dbg
        x, y, w, h, c = tobj.cc2xywh()
        tobj.resizeTnik(tobj.hcurs, 0, H, x, y, w, h, why=why, dbg=dbg)
########################################################################################################################################################################################################
class MoveToCmd(Cmd):
    def __init__(self, tobj, how, p, l, c, t, ss=0, dbg=1):
        self.tobj, self.how, self.p, self.l, self.c, self.t, self.ss, self.dbg = tobj, how, p, l, c, t, ss, dbg
        
    def do(  self): self._moveTo()
    def undo(self): self._moveTo() # todo fixme
    
    def _moveTo(self):
        tobj, how, p, l, c, t, ss, dbg = self.tobj, self.how, self.p, self.l, self.c, self.t, self.ss, self.dbg
        if dbg:    tobj.log(f'BGN {how}', pos=1)
        cmd = MoveTo2Cmd(tobj, p, l, c, t)       ;  cmd.do()
        cmd = MoveCursorCmd(tobj, ss, how)       ;  cmd.do()
        if dbg:    tobj.log(f'END {how}', pos=1)
########################################################################################################################################################################################################
class MoveTo2Cmd(Cmd):
    def __init__(self, tobj, p, l, c, t, n=0, dbg=1):
        self.tobj, self.p, self.l, self.c, self.t, self.n, self.dbg = tobj, p, l, c, t, n, dbg 

    def do(  self): self._moveto2()
    def undo(self): self._moveto2() # todo fixme
    
    def _moveto2(self): # todo
        tobj, p, l, c, t, n, dbg = self.tobj, self.p, self.l, self.c, self.t, self.n, self.dbg
        if dbg: tobj.log(f'BGN plct={tobj.fplct(p, l, c, t)}', pos=1) # {n=}
        np, nl, ns, nc, nt = tobj.n
        t2        =       n  + t
        c2        = t2 // nt + c
        l2        = c2 // nc + l
        p2        = l2 // nl + p
        tobj.i[T] = t2  % nt + 1
        tobj.i[C] = c2  % nc + 1
        tobj.i[L] = l2  % nl + 1
        tobj.i[P] = p2  % np + 1
        if dbg: tobj.log(f'END {n=} {tobj.fmti()} plct={tobj.fplct(p, l, c, t)} plct2={tobj.fplct(p2, l2, c2, t2)}', pos=1)
########################################################################################################################################################################################################
class MoveCmd(Cmd):
    def __init__(self, tobj, how, n, ss=0, dbg=1):
        self.tobj, self.how, self.n, self.ss, self.dbg = tobj, how, n, ss, dbg
        
    def do(  self): self._move()
    def undo(self): self._move() # todo fixme
    
    def _move(self):
        tobj, how, n, ss, dbg = self.tobj, self.how, self.n, self.ss, self.dbg
        if dbg:    tobj.log(f'BGN {how} {n=}', pos=1)
        p, l, c, t = tobj.j2()
        cmd = MoveTo2Cmd(tobj, p, l, c, t, n=n)     ;  cmd.do()
        if tobj.CURSOR and tobj.cursor: tobj.moveCursor(ss, how)
        if dbg:    tobj.log(f'END {how} {n=}', pos=1)
########################################################################################################################################################################################################
class MoveUpCmd(Cmd):
    def __init__(self, tobj, how, dbg=1):
        self.tobj, self.how, self.dbg = tobj, how, dbg
        
    def do(  self): self._moveUp()
    def undo(self): self._moveUp() # todo fixme
    
    def _moveUp(self):
        tobj, how, dbg = self.tobj, self.how, self.dbg
        p, l, s, c, t = tobj.j()  ;  n = tobj.n[T] - 1  ;  m = tobj.n[L] - 1
        if dbg: tobj.log(f'BGN {how}', pos=1)
        if t>0: cmd = MoveToCmd(tobj, how, p, l,                 c, 0)     ;  cmd.do() # go up   to top    of      line
        else:   cmd = MoveToCmd(tobj, how, p, l-1 if l>0 else m, c, n)     ;  cmd.do() # go up   to bottom of prev line, wrap down to bottom of last line
        if dbg: tobj.log(f'END {how}', pos=1)
########################################################################################################################################################################################################
class MoveDownCmd(Cmd):
    def __init__(self, tobj, how, dbg=1):
        self.tobj, self.how, self.dbg = tobj, how, dbg

    def do(  self): self._moveDown()
    def undo(self): self._moveDown() # todo fixme
    
    def _moveDown(self):
        tobj, how, dbg = self.tobj, self.how, self.dbg
        p, l, s, c, t = tobj.j()  ;  n = tobj.n[T] - 1  ;  m = tobj.n[L] - 1
        if dbg: tobj.log(f'BGN {how}', pos=1)
        if t<n: cmd = MoveToCmd(tobj, how, p, l,                 c, n)     ;  cmd.do() # go down to bottom of      line
        else:   cmd = MoveToCmd(tobj, how, p, l+1 if l<m else 0, c, 0)     ;  cmd.do() # go down to top    of next line, wrap up to top of first line
        if dbg: tobj.log(f'END {how}', pos=1)
########################################################################################################################################################################################################
class MoveLeftCmd(Cmd):
    def __init__(self, tobj, how, dbg=1):
        self.tobj, self.how, self.dbg = tobj, how, dbg
        
    def do(  self): self._moveLeft()
    def undo(self): self._moveLeft() # todo fixme
    
    def _moveLeft(self):
        tobj, how, dbg = self.tobj, self.how, self.dbg
        p, l, s, c, t = tobj.j()  ;  n = tobj.n[C] - 1  ;  m = tobj.n[L] - 1
        if dbg: tobj.log(f'BGN {how}', pos=1)
        if c>0: cmd = MoveToCmd(tobj, how, p, l,                 0, t)     ;  cmd.do() # go left  to bgn of      line
        else:   cmd = MoveToCmd(tobj, how, p, l-1 if l>0 else m, n, t)     ;  cmd.do() # go left  to end of prev line, wrap right to bottom of last line
        if dbg: tobj.log(f'END {how}', pos=1)                # go right & up to end of prev line, wrap down to bottom of last line
########################################################################################################################################################################################################
class MoveRightCmd(Cmd):
    def __init__(self, tobj, how, dbg=1):
        self.tobj, self.how, self.dbg = tobj, how, dbg
        
    def do(  self): self._moveRight()
    def undo(self): self._moveRight() # todo fixme
    
    def _moveRight(self):
        tobj, how, dbg = self.tobj, self.how, self.dbg
        p, l, s, c, t = tobj.j()  ;  n = tobj.n[C] - 1  ;  m = tobj.n[L] - 1
        if dbg: tobj.log(f'BGN {how}', pos=1)
        if c<n: cmd = MoveToCmd(tobj, how, p, l,                 n, t)     ;  cmd.do() # go right to end of      line
        else:   cmd = MoveToCmd(tobj, how, p, l+1 if l<m else 0, 0, t)     ;  cmd.do() # go right to bgn of next line, wrap left to top of first line
        if dbg: tobj.log(f'END {how}', pos=1)                # go left & down to bgn of next line, wrap left to top of first line
 ########################################################################################################################################################################################################
class PrevPageCmd(Cmd):
    def __init__(self, tobj, how, dbg=1):
        self.tobj, self.how, self.dbg = tobj, how, dbg
        
    def do(  self): self._prevPage()
    def undo(self): self._prevPage() # todo fixme
    
    def _prevPage(self):
        tobj, how, dbg = self.tobj, self.how, self.dbg
        p, l, c, t = tobj.j2()   ;   n = tobj.n[P] - 1
        if dbg: tobj.log(f'BGN {how} {tobj.fmti()}', pos=1)
        cmd = MoveToCmd(tobj, how, p-1 if p>0 else n, l, c, t)     ;  cmd.do()
#        self.flipPage(how, -1, dbg=1)
        if dbg: tobj.log(f'END {how} {tobj.fmti()}', pos=1)

 ########################################################################################################################################################################################################
class NextPageCmd(Cmd):
    def __init__(self, tobj, how, dbg=1):
        self.tobj, self.how, self.dbg = tobj, how, dbg
        
    def do(  self): self._nextPage()
    def undo(self): self._nextPage()
    
    def _nextPage(self):
        tobj, how, dbg = self.tobj, self.how, self.dbg
        p, l, c, t = tobj.j2()   ;   n = tobj.n[P] - 1
        if dbg: tobj.log(f'BGN {how} {tobj.fmti()}', pos=1)
        cmd = MoveToCmd(tobj, how, p+1 if p<n else 0, l, c, t)     ;  cmd.do()
#        self.flipPage(how, 1, dbg=1)
        if dbg: tobj.log(f'END {how} {tobj.fmti()}', pos=1)

 ########################################################################################################################################################################################################
