from abc import ABC, abstractmethod
from   tpkg            import utl    as utl
from   tpkg            import kysgs  as kysgs
from   tpkg.notes      import Notes  as Notes

P, L, S, C,          T, N, I, K,          M, R, Q, H,          B, A, D, E   = utl.P, utl.L, utl.S, utl.C,    utl.T, utl.N, utl.I, utl.K,    utl.M, utl.R, utl.Q, utl.H,    utl.B, utl.A, utl.D, utl.E
W, X, Y, Z,       NONE,  ist,  fri,         slog,   fmtf,   fmtl,   fmtm    = utl.W, utl.X, utl.Y, utl.Z,    utl.NONE,   utl.ist,   utl.fri,       utl.slog,   utl.fmtf,   utl.fmtl,   utl.fmtm
CAT,  CSV,  EVN,  LOG,  PNG,  TXT,  DAT  =     'cat' ,     'csv' ,     'evn',      'log' ,     'png' ,     'txt' ,     'dat'
CATS, CSVS, EVNS, LOGS, PNGS, TEXT, DATA =     'cats',     'csvs',     'evns',     'logs',     'pngs',     'text',     'data'
HARROWS, VARROWS      = ['LARROW', 'RARROW'], ['DARROW', 'UARROW']

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
