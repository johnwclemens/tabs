from abc import ABC, abstractmethod
import inspect, itertools, pathlib
import pyglet
import pyglet.window.key         as pygwink
import pyglet.image              as pygimg
#import pyglet.text               as pygtxt
from   tpkg        import utl
from   tpkg        import kysgs
from   tpkg.notes  import Notes
from   tpkg        import misc

P, L, S, C,          T, N, I, K,          M, R, Q, H,          A, B, D, E   = utl.P, utl.L, utl.S, utl.C,    utl.T, utl.N, utl.I, utl.K,    utl.M, utl.R, utl.Q, utl.H,    utl.A, utl.B, utl.D, utl.E
W, X, Y, Z,       NONE,  ist,  fri,         slog,   fmtf,   fmtl,   fmtm    = utl.W, utl.X, utl.Y, utl.Z,    utl.NONE,   utl.ist,   utl.fri,       utl.slog,   utl.fmtf,   utl.fmtl,   utl.fmtm
BGC,  BOLD,  COLOR,     FONT_NAME,  FONT_SIZE, ITALIC,  KERNING,  UNDERLINE = utl.BGC,   utl.BOLD,  utl.COLOR,   utl.FONT_NAME, utl.FONT_SIZE, utl.ITALIC,   utl.KERNING,     utl.UNDERLINE

NORMAL_STYLE, SELECT_STYLE, CURRENT_STYLE = utl.NORMAL_STYLE, utl.SELECT_STYLE, utl.CURRENT_STYLE
CAT,  CSV,  EVN,  LOG,  PNG,  TXT,  DAT   = utl.CAT,  utl.CSV,  utl.EVN,  utl.LOG,  utl.PNG,  utl.TXT,  utl.DAT
CATS, CSVS, EVNS, LOGS, PNGS, TEXT, DATA  = utl.CATS, utl.CSVS, utl.EVNS, utl.LOGS, utl.PNGS, utl.TEXT, utl.DATA 
BASE_NAME,        BASE_PATH,        PATH  = utl.paths()

MLDY, CHRD, ARPG               = utl.MLDY, utl.CHRD, utl.ARPG
LARROW, RARROW, DARROW, UARROW = utl.LARROW, utl.RARROW, utl.DARROW, utl.UARROW

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
        tobj.newC += 1  ;  why2 = f'New.{tobj.newC}'  ;  why = why2  ;  k = kl[kk]
        page = tobj.createTnik(tobj.pages,   pi, P, x, y, w, h, k, why=why, v=0, dbg=1)
        for line in            tobj.g_createTniks(tobj.lines,  L, page, why=why):
            for sect in        tobj.g_createTniks(tobj.sects,  S, line, why=why):
                for colm in    tobj.g_createTniks(tobj.colms,  C, sect, why=why):
                    for _ in   tobj.g_createTniks(tobj.tabls,  T, colm, why=why): pass
        tobj.dumpTniksSfx(how)
        if tobj.SNAPS >= 2 and dbg: tobj.regSnap(why2, how)
########################################################################################################################################################################################################
class AutoMoveCmd(Cmd):
    def __init__(self, tobj, how, dbg=1):
        self.tobj, self.how, self.dbg = tobj, how, dbg
        
    def do(  self): self._autoMove()
    def undo(self): self._autoMove() # todo fixme
    
    def _autoMove(self):
        tobj, how, dbg = self.tobj, self.how, self.dbg
        tobj.log(f'BGN {tobj.hArrow=} {tobj.vArrow=} {tobj.csrMode=} {how}', pos=1)
        ha = 1 if tobj.hArrow == RARROW else -1
        va = 1 if tobj.vArrow == DARROW else -1
        n, i  = tobj.n[T], tobj.i[T]
        mmDist  = ha * n
        cmDist  = va
        amDist  = mmDist + cmDist
        if dbg:   tobj.dumpCursorArrows(f'{tobj.fmtPos()}     {how} M={mmDist} C={cmDist} A={amDist}')
        if        tobj.csrMode == MLDY:                               cmd = MoveCmd(tobj, how,   mmDist)  ;  cmd.do()
        elif      tobj.csrMode == CHRD:
            if    i==1 and tobj.vArrow==UARROW and tobj.hArrow==RARROW: cmd = MoveCmd(tobj, how,   n*2-1)   ;  cmd.do()
            elif  i==6 and tobj.vArrow==DARROW and tobj.hArrow==LARROW: cmd = MoveCmd(tobj, how, -(n*2-1))  ;  cmd.do()
            else:                                                       cmd = MoveCmd(tobj, how,   cmDist)  ;  cmd.do()
        elif      tobj.csrMode == ARPG:                                 cmd = MoveCmd(tobj, how,   amDist)  ;  cmd.do()
        tobj.log(f'END {tobj.hArrow=} {tobj.vArrow=} {tobj.csrMode=} {how}', pos=1)
########################################################################################################################################################################################################
class CsrJumpCmd(Cmd):
    def __init__(self, tobj, how, txt, ab):
        self.tobj, self.how, self.txt, self.ab = tobj, how, txt, ab

    def do(  self): self._csrJump()
    def undo(self): self._csrJump() # todo fixme

    def _csrJump(self):
        tobj, how, txt, ab = self.tobj, self.how, self.txt, self.ab
        cc = tobj.cursorCol()            ;            tobj.jumpAbs = ab
        tobj.log(    f'{how} {txt=} {ab=} {cc=} jt={tobj.jumpAbs} {tobj.fmti()}')
        if not tobj.jumping:                          tobj.jumping = 1
        elif txt.isdecimal():                         tobj.jumpStr += txt
        elif txt == '-' and not tobj.jumpStr:         tobj.jumpStr += txt
        elif txt == W:
            tobj.log(f'{how} {txt=} {ab=} {cc=} jt={tobj.jumpAbs} {tobj.jumpStr=} {tobj.fmti()}')
            jcc  = tobj.n[T] * int(tobj.jumpStr)
            tobj.jumping = 0   ;   tobj.jumpStr = Z
            tobj.move(how, jcc - 1 - ab * cc)
            tobj.log(f'{how} {txt=} {ab=} {cc=} jt={tobj.jumpAbs} {jcc=} moved={jcc - 1 - ab * cc} {tobj.fmti()}')
########################################################################################################################################################################################################
class CopyKordNamesCmd(Cmd):
    def __init__(self, tobj, how, dbg=1):
        self.tobj, self.how, self.dbg = tobj, how, dbg
        
    def do(  self): self._copyKordNames()
    def undo(self): self._copyKordNames() # todo fixme
    
    def _copyKordNames(self):
        tobj, how, dbg = self.tobj, self.how, self.dbg
        nt = tobj.n[T]  ;  cc = tobj.cursorCol()  ;  cn = tobj.cc2cn(cc)  ;  i = 0
        text = set()   ;   t2n = tobj.sobj.tab2nn
        for s in range(nt):
            tt = tobj.tabls[s].text
            if tt and tt != W: 
                txt = t2n(tt if tt else tobj.tblank, s)
                text.add(txt)
        text = list(text)
        for t in text[:-1]:
            if t != tobj.tblank:
                i += 1
                cmd = SelectTabsCmd(tobj, pygwink.MOTION_NEXT_WORD, nt, cn)               ;  cmd.do()
                tobj.on_draw()
                cmd = CopyTabsCmd(  tobj, f'MOTION_COPY={pygwink.MOTION_COPY}')           ;  cmd.do()
                tobj.on_draw()
                cmd = PasteTabsCmd( tobj, f'MOTION_PASTE={pygwink.MOTION_PASTE}', kk=0)   ;  cmd.do()
                tobj.on_draw()
                for j in range(i):
                    cmd = TogKordNamesCmd(tobj, how, hit=0)                               ;  cmd.do()
                    tobj.on_draw()
########################################################################################################################################################################################################
class CopyTabsCmd(Cmd):
    def __init__(self, tobj, how, dbg=1):
        self.tobj, self.how, self.dbg = tobj, how, dbg
        
    def do(  self): self._copyTabs()
    def undo(self): self._copyTabs() # todo fixme
    
    def _copyTabs(self):
        tobj, how, dbg = self.tobj, self.how, self.dbg
        tobj.dumpSmap(f'BGN {how}')  ;  nt = tobj.n[T]  ;  style = NORMAL_STYLE  ;  text = []  ;  tobj.cpyC += 1
        for k in list(tobj.smap.keys()):
            k *= nt
            if tobj.LL:  tobj.setLLStyle(k, style)
            text.append(tobj.setTNIKStyle(k, nt, style))
            if dbg: text.append(W)
        if dbg:         tobj.log(f'{Z.join(text)=}')
        tobj.dumpSmap(f'END {how}')
#        if tobj.SNAPS >= 4:  tobj.regSnap(f'CPY.{tobj.cpyC}', how)
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
class DeleteTabsCmd(Cmd):
    def __init__(self, tobj, how, keep=0, dbg=1):
        self.tobj, self.how, self.keep, self.dbg = tobj, how, keep, dbg
        
    def do(  self): self._deleteTabs()
    def undo(self): self._deleteTabs() # todo fixme
    
    def _deleteTabs(self):
        tobj, how, keep, dbg = self.tobj, self.how, self.keep, self.dbg
        tobj.dumpSmap(f'BGN {how} {keep=}')   ;   style = NORMAL_STYLE   ;   nt = tobj.n[T]   ;   tobj.delC += 1  
        for k, text in tobj.smap.items():
            cn = k   ;   k *= nt
            if dbg:     tobj.log(f'{k=} {cn=} {text=}')
            if tobj.LL: tobj.setLLStyle(k, style)
            tobj.setTNIKStyle(k, nt, style, blank=1)
        if not keep:    tobj.unselectAll(f'deleteTabs({keep=})')
        tobj.dumpSmap(f'END {how} {keep=}')
        if tobj.SNAPS >= 4:  tobj.regSnap(f'DEL.{tobj.delC}', how)
        tobj.rsyncData = 1
########################################################################################################################################################################################################
class EraseTabsCmd(Cmd):
    def __init__(self, tobj, how): #, reset=0
        self.tobj, self.how = tobj, how
        
    def do(  self): self._eraseTabs()
    def undo(self): self._eraseTabs() # todo fixme
    
    def _eraseTabs(self):
        tobj, how = self.tobj, self.how
        np, nl, ns, nc, nt = tobj.n   ;  nz = 0 #  ;   nz = tobj.zzlen()  ;  nc += nz
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
            if not tobj.sobj.isFret(tobj.tabls[i].text):   continue
            p, l, s, c, t = tobj.cc2plsct(i, dbg=1)    ;   break
        tobj.moveToB(how, p, l, s, c, t, dbg=dbg)
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
            if not tobj.sobj.isFret(tobj.tabls[i].text):   continue
            p, l, s, c, t = tobj.cc2plsct(i, dbg=1)    ;   break
        tobj.moveToB(how, p, l, s, c, t, dbg=dbg)
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
        if tobj.cursor: cmd = MoveCursorCmd(tobj, how, ss)     ;  cmd.do()
        if dbg:         tobj.log(f'END {how} {n=}', pos=1)
########################################################################################################################################################################################################
class MoveCursorCmd(Cmd):
    def __init__(self, tobj, how, ss=0, dbg=1):
        self.tobj, self.how, self.ss, self.dbg = tobj, how, ss, dbg
        
    def do(  self): self._moveCursor()
    def undo(self): self._moveCursor() # todo fixme
    
    def _moveCursor(self):
        tobj, how, ss, dbg = self.tobj, self.how, self.ss, self.dbg
        if dbg:           tobj.log(f'BGN {ss=} {tobj.cc=}', pos=1)
        if tobj.LL:       tobj.setLLStyle(tobj.cc, SELECT_STYLE if ss else NORMAL_STYLE)
        cmd = UpdateCursorCmd(tobj, how, dbg=dbg)         ;  cmd.do()
        if tobj.LL:       tobj.setLLStyle(tobj.cc, CURRENT_STYLE)
        if dbg:           tobj.log(f'END {ss=} {tobj.cc=}', pos=1)
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
        cmd = MoveCursorCmd(tobj, how, ss)       ;  cmd.do()
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
class NextPageCmd(Cmd):
    def __init__(self, tobj, how, dbg=1):
        self.tobj, self.how, self.dbg = tobj, how, dbg
        
    def do(  self): self._nextPage()
    def undo(self): self._nextPage() # todo fixme
    
    def _nextPage(self):
        tobj, how, dbg = self.tobj, self.how, self.dbg
        p, l, c, t = tobj.j2()   ;   n = tobj.n[P] - 1
        if dbg: tobj.log(f'BGN {how} {tobj.fmti()}', pos=1)
        cmd = MoveToCmd(tobj, how, p+1 if p<n else 0, l, c, t)     ;  cmd.do()
#        self.flipPage(how, 1, dbg=1)
        if dbg: tobj.log(f'END {how} {tobj.fmti()}', pos=1)
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
        p, l, s, c, t = tobj.j()    ;   tobj.pstC += 1
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
        if tobj.SNAPS >= 4:  tobj.regSnap(f'PST.{tobj.pstC}', how)
        tobj.rsyncData = 1
########################################################################################################################################################################################################
#class PlayCmd(Cmd):
#    def __init__(self, tobj):
#        self.tobj = tobj
        
#    def do(self):   self._play()
#    def undo(self): self._play()
    
#    def _play(self): # todo finish impl
#        tobj = self.tobj
        
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
class QuitCmd(Cmd):
    def __init__(self, tobj, why=Z, err=1, save=1, dbg=1):
        self.tobj, self.why, self.err, self.save, self.dbg = tobj, why, err, save, dbg

    def do(  self): return self._quit()
    def undo(self): self._quit()
    
    def _quit(self):
        tobj, why, err, save, dbg = self.tobj, self.why, self.err, self.save, self.dbg  
        retv = True
        hdr1 = tobj.fTnikHdr(1)    ;    hdr0 = tobj.fTnikHdr(0)   ;   tobj.log(hdr1, p=0, f=2)  ;  tobj.log(hdr0,     p=0, f=2)   ;   errStr = f'Error={err}'
        tobj.log(f'BGN {why} {errStr} {save=} {tobj.quitting=}', f=2)                           ;  tobj.log(utl.QUIT, p=0, f=2)   ;   msg    = 'Recursion Error'
        tobj.log(utl.QUIT_BGN, p=0, f=2)    ;    utl.dumpStack(inspect.stack())                 ;  tobj.log(utl.QUIT, p=0, f=2)
        if tobj.quitting:        msg += f' {tobj.quitting=} Exiting'  ;  tobj.log(msg, f=2)     ;  tobj.close() #  ;   return True
        tobj.dumpTniksSfx(why)        ;     tobj.quitting += 1
        if not err:
            utl.dumpStack(utl.MAX_STACK_FRAME)
            if dbg:  tobj.dumpStruct(why, dbg=dbg)
            if save: cmd = SaveDataFileCmd(tobj, why, tobj.dataPath1)    ;  cmd.do()
            if dbg:  tobj.transposeData(dmp=dbg)
            if dbg:  tobj.cobj.dumpMlimap(why)
        if tobj.SNAPS:  tobj.snpC += 1  ;  cmd = SnapshotCmd(tobj, tobj.snpC, utl.FINI, f'quit {err} {save=}')     ;  cmd.do()
        tobj.log(f'END {why} {errStr} {save=} {tobj.quitting=}', f=2)       ;   tobj.log(utl.QUIT_END, p=0, f=2)
        tobj.cleanupFiles()
        tobj.log(f'END {why} {errStr} {save=} {tobj.quitting=}', f=0)       ;   tobj.log(utl.QUIT_END, p=0, f=0)
        tobj.log('Calling close()', e=Y, f=2)
        tobj.close()
        if tobj.TEST:
            if   tobj.EXIT == 0: retv = False  ;  tobj.log(f'{tobj.EXIT=} returning {retv=}')
            elif tobj.EXIT == 1: retv = True   ;  tobj.log(f'{tobj.EXIT=} returning {retv=}')
            elif tobj.EXIT == 2:                  tobj.log(f'{tobj.EXIT=} Calling pyglet.app.exit()')  ;   pyglet.app.exit()
            else:                                 tobj.log(f'{tobj.EXIT=} Calling exit()')             ;   exit()
        else:                                     tobj.log(f'{tobj.EXIT=} returning {retv=}')
        return retv
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
        tobj.reinit()
        tobj.dumpGeom('END', f'{how} after reinit()')
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
class SaveDataFileCmd(Cmd):
    def __init__(self, tobj, how, path, dbg=1):
        self.tobj, self.how, self.path, self.dbg = tobj, how, path, dbg
        
    def do(  self): return self._saveDataFile()
    def undo(self): self._saveDataFile()
    
    def _saveDataFile(self):
        tobj, how, path, dbg = self.tobj, self.how, self.path, self.dbg
        if dbg:   tobj.log(f'BGN {how} {path}')
        with open(path, 'w', encoding='utf-8') as DATA_FILE:
            tobj.log(f'{DATA_FILE.name:40}', p=0)
            commentStr = '#' * tobj.n[C]   ;   commentRow = f'{commentStr}{X}'
            DATA_FILE.write(commentRow) if tobj.DEC_DATA else None
            data = tobj.transposeData(dmp=dbg) # if self.isVert() else self.data
            tobj.log(f'{tobj.fmtn()} {tobj.fmtdl(data)}')
            for p, page in enumerate(data):
                if dbg: tobj.log(f'writing {p+1}{utl.ordSfx(p + 1)}   Page', p=0)
                for l, line in enumerate(page):
                    if dbg: tobj.log(f'writing {l+1}{utl.ordSfx(l+1)}   Line', p=0)  # if dbg  else  self.log(p=0)  if  l  else  None
                    for r, row in enumerate(line):
                        text = []
                        for c, col in enumerate(row):
                            text.append(col)
                        text = Z.join(text)
                        if dbg: tobj.log(f'writing {r+1}{utl.ordSfx(r+1)} String {text}', p=0)  # if dbg  else  self.log(text, p=0)
                        DATA_FILE.write(f'{text}{X}')
                    DATA_FILE.write(commentRow) if tobj.DEC_DATA else DATA_FILE.write(X)  #   if l < nl:
                DATA_FILE.write(commentRow) if tobj.DEC_DATA else DATA_FILE.write(X)
        size = path.stat().st_size   ;   tobj.log(f'{tobj.fmtn()} {tobj.fmtdl()} {size=}')
        if dbg:   tobj.log(f'END {how} {path}')
        return size
########################################################################################################################################################################################################
class SelectTabsCmd(Cmd):
    def __init__(self, tobj, how, m=0, cn=None, dbg=1, dbg2=1):
        self.tobj, self.how, self.m, self.cn, self.dbg, self.dbg2 = tobj, how, m, cn, dbg, dbg2
        
    def do(  self): self._selectTabs()
    def undo(self): self._selectTabs()
    
    def _selectTabs(self):
        tobj, how, m, cn, dbg, dbg2 = self.tobj, self.how, self.m, self.cn, self.dbg, self.dbg2
        cc            = tobj.cursorCol()  ;  old = cn
        p, l, s, c, t = tobj.cc2plsct(cc)
        if cn is None:      cn = tobj.cc2cn(cc) # self.plc2cn_(p, l, c)
        nt = tobj.n[T]  ;   k  = cn * nt   ;   style = SELECT_STYLE
        tobj.log(f'{m=} {old=} {cc=} {cn=} {nt} {k=} {tobj.fplsct(p, l, s, c, t)}')
        if cn in tobj.smap: tobj.log(f'RETURN: {cn=} already in smap={fmtm(tobj.smap)}') if dbg2 else None   ;   return
        if dbg:             tobj.dumpSmap(f'BGN {how} {m=} {cn=} {cc=} {k=}')
        text              = tobj.setTNIKStyle(k, nt, style)
        tobj.smap[cn]     = text
        if m:               cmd = MoveCmd(tobj, how, m, ss=1)     ;  cmd.do()
        if dbg:             tobj.dumpSmap(f'END {how} {m=} {cn=} {cc=} {k=}')
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
class SetFontArgCmd(Cmd):
    def __init__(self, tobj, how, n, v, m, dbg=1):
        self.tobj, self.how, self.n, self.v, self.m, self.dbg = tobj, how, n, v, m, dbg

    def do(  self): self._setFontArg()
    def undo(self): self._setFontArg()
    
    def _setFontArg(self):
        tobj, how, n, v, m, dbg = self.tobj, self.how, self.n, self.v, self.m, self.dbg
        if   m == 'clrIdx':      v += getattr(tobj, m)   ;   v %= len(tobj.k)      ;  tobj.log(f'{how} {n=:12} {v=:2} {tobj.clrIdx=:2}')
        elif m == 'fontNameIdx': v += getattr(tobj, m)   ;   v %= len(FONT_NAMES)  ;  tobj.log(f'{how} {n=:12} {v=:2} {tobj.fontNameIdx=:2}')
        setattr(tobj, m, v)
        ts = list(itertools.chain(tobj.A, tobj.B, tobj.C))  ;  lt = len(ts)
        if dbg:         tobj.log(f'{how} {lt=} {m=:12} {n=:12} {fmtf(v, 5)}')
        for j, t in enumerate(ts):
            tobj.setFontArg2(t, n, v, m, j)
        if dbg:         tobj.log(f'{how} {lt=} {m=:12} {n=:12} {fmtf(v, 5)}')
        tobj.setCaption(tobj.fmtFont())
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
class SetTabCmd(Cmd):
    def __init__(self, tobj, how, text, m=0, rev=0, dbg=1):
        self.tobj, self.how, self.text, self.m, self.rev, self.dbg = tobj, how, text, m, rev, dbg
        
    def do(  self): self._setTab()
    def undo(self): self._setTab()
    
    def _setTab(self):
        tobj, how, text, m, rev, dbg = self.tobj, self.how, self.text, self.m, self.rev, self.dbg
        bsp = 1 if m == pygwink.MOTION_BACKSPACE else 0
        if rev: tobj.reverseArrow(bsp)   ;   cmd = AutoMoveCmd(tobj, how)   ;  cmd.do()
        old   = tobj.cursorCol()   ;   msg = Z
        p, l, s, c, t = tobj.j()
        cc    = tobj.plct2cc(p, l, c, t)   ;   cc2 = cc
        tobj.log(f'BGN {how} {rev=} {old=:3} {cc=:3} {text=} {p=} {l=} {s=} {c=} {t=}', pos=1, f=2)
        assert 0 <= p < tobj.n[P] and 0 <= l < tobj.n[L] and 0 <= s < tobj.n[S] and 0 <= c < tobj.n[C] and 0 <= t < tobj.n[T],  f'{tobj.n=} {p=} {l=} {s=} {c=} {t=}'
        data  = tobj.data[p][l][c][t]
        tobj.log(f'    {how} {rev=} {old=:3} {cc=:3}{msg} {text=} {data=} ', pos=1)
        tobj.setDTNIK(text, cc2, p, l, c, t, kk=1)
        p, l, c, t = tobj.j2()   ;   data = tobj.data[p][l][c][t]
        tobj.log(f'END {how} {text=} {data=} {rev=} {old=:3} {cc=:3}{msg}', pos=1)
        if rev: tobj.reverseArrow(bsp)
        else:   cmd = AutoMoveCmd(tobj, how)   ;  cmd.do()
        if dbg and tobj.SNAPS >= 5:
            stype = f'TXT.{text}' if tobj.sobj.isFret(text) else 'SYM' if text in misc.DSymb.SYMBS else 'UNK'
            tobj.regSnap(stype, how)
        tobj.rsyncData = 1
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
class SnapshotCmd(Cmd):
    def __init__(self, tobj, sid, typ=Z, why=Z, dbg=1, dbg2=1): #fixme 11/18/23
        self.tobj, self.sid, self.typ, self.why, self.dbg, self.dbg2 = tobj, sid, typ, why, dbg, dbg2
        
    def do(  self): return self._snapshot()
    def undo(self): self._snapshot()
    
    def _snapshot(self):
        tobj, sid, typ, why, dbg, dbg2 = self.tobj, self.sid, self.typ, self.why, self.dbg, self.dbg2
        logId     = tobj.LOG_ID
        snapName  = f'{BASE_NAME}.{logId}.{sid}.{typ}.{PNG}'
        snapPath  = pathlib.Path(BASE_PATH / PNGS / snapName)
        if dbg:  tobj.log(f'{BASE_NAME=} {logId=} {sid=} {typ=} {PNG=}')
        if dbg:  tobj.log(f'{tobj.fNameLogId=} {snapName=} {why}')
        if dbg:  tobj.log(f'{snapPath}', p=2)
        pygimg.get_buffer_manager().get_color_buffer().save(f'{snapPath}')
        if dbg2: tobj.log(f'{snapName=} {why}', f=2)
        snapName0 = f'{BASE_NAME}.{PNG}'
        snapName2 = tobj.geomFileName(BASE_NAME, PNG)
        snapPath0 = BASE_PATH / PNGS / snapName0
        snapPath2 = BASE_PATH / snapName2
        utl.copyFile(snapPath, snapPath0)
        utl.copyFile(snapPath, snapPath2)
        if dbg:  tobj.log(f'{BASE_NAME=} {tobj.fmtn(Z)}')
        if dbg:  tobj.log(f'{snapName0=} {why}')
        if dbg:  tobj.log(f'{snapName2=} {why}')
        if dbg:  tobj.log(f'{snapPath0=}', p=2)
        if dbg:  tobj.log(f'{snapPath2=}', p=2)
        tobj.dumpTnikCsvs(snapPath)
        return snapPath
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
            np, nl, ns, nc, nt = tobj.n  #  ;     nc += tobj.zzlen()
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
            if tobj.SNAPS >= 2: tobj.regSnap('SWP', how)
            tobj.rsyncData = 1
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
class TogBGCCmd(Cmd):
    def __init__(self, tobj, how):
        self.tobj, self.how = tobj, how

    def do(  self): self._togBGC()
    def undo(self): self._togBGC()

    def _togBGC(self):
        tobj, how = self.tobj, self.how
        tobj.log(f'{how} {tobj.BGC=}') if how else None
        tobj.BGC = (1 + tobj.BGC) % 2
        tobj.setFontArg2(tobj.tabls, COLOR, tobj.BGC, 'clrIdx', T)
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
        tniks, j, _, _ = tobj.tnikInfo(0, 0, s, 0, 0, why=how)
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
        mli = tobj.cobj.mlimap   ;   mks = list(mli.keys())   ;   cn2 = -1
        if cn not in mks: msg = f'ERROR: {cn=} not in {fmtl(mks)=}'   ;   tobj.log(msg)   ;   cmd = QuitCmd(tobj, msg)   ;  cmd.do()
        ivals =  [ u[1] for u in mli[cn][0] ]
        msg   =  [ fmtl(v, w="x") for v in ivals ]
        if dbg: tobj.log(f'BGN {how} mks={fmtl(mks)} cn={cn:2} ivals={fmtl(msg, d=Z)}')
        hits = self._ivalhits(tobj, ivals, how)
        for cn2 in hits:
            if cn2 not in tobj.smap: cmd = SelectTabsCmd(tobj, how, m=0, cn=cn2)     ;  cmd.do()
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
        if tobj.SNAPS >= 6:      tobj.regSnap(f'KRD{imi}', how)
        elif dbg: tobj.log(f'    {how} {cn=} {cc=} is NOT a chord')
        if dbg2:  tobj.cobj.dumpImap(limap[imi], why=f'{cn:2}')
#        assert imi == limap[imi][-1],   f'{imi=} {limap[imi][-1]=}'
########################################################################################################################################################################################################
class TogLLsCmd(Cmd):
    def __init__(self, tobj, how, dbg=1):
        self.tobj, self.how, self.dbg = tobj, how, dbg

    def do(  self): self._togLLs()
    def undo(self): self._togLLs()
    
    def _togLLs(self):
        tobj, how, dbg = self.tobj, self.how, self.dbg
        if not tobj.LL: msg = 'ADD'
        else:           msg = 'HID'
        tobj.dumpGeom('BGN', f'{how} {msg}')
        tobj.togLL(f'{how} {msg}')
        if dbg: tobj.log(f'    llText={fmtl(tobj.llText)}')
        if tobj.LL: tobj.addLLs( how)
        else:       tobj.hideLLs(how)
        if   tobj.SNAPS >= 3:      tobj.regSnap(f'{msg}', how)
        tobj.on_resize(tobj.width, tobj.height)
        tobj.dumpGeom('END', f'{how} {msg}')
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
class TogTTsCmd(Cmd):
    def __init__(self, tobj, how, tt):
        self.tobj, self.how, self.tt = tobj, how, tt

    def do(  self): self._togTTs()
    def undo(self): self._togTTs()

    def _togTTs(self):
        tobj, how, tt = self.tobj, self.how, self.tt
        msg2 = f'{how} {tt=}'
        tobj.dumpGeom('BGN', f'     {msg2}')
        if   tt not in tobj.SS:      msg = 'ADD'    ;    sectName = tobj.addTTs( how, tt)
        else:                        msg = 'HID'    ;    sectName = tobj.hideTTs(how, tt)
        if   tobj.SNAPS >= 3:      tobj.regSnap(f'{msg}{sectName}', how)
        tobj.on_resize(tobj.width, tobj.height)
        tobj.dumpGeom('END', f'{msg} {msg2}')
########################################################################################################################################################################################################
class TogAXYVCmd(Cmd):
    def __init__(self, tobj, how, i, j):
        self.tobj, self.how, self.i, self.j = tobj, how, i, j
        
    def do(  self): self._togAXYV()
    def undo(self): self._togAXYV()
    
    def _togAXYV(self):
        tobj, how, i, j = self.tobj, self.how, self.i, self.j
        v  = tobj.aa if i==0 else tobj.ax if i==1 else tobj.ay if i==2 else tobj.av if i==3 else -1
        w  = tobj.ftAa(v) if i==0 else tobj.ftAx(v) if i==1 else tobj.ftAy(v) if i==2 else tobj.ftAv(v) if i==3 else -1 
        d  = tobj.AXYV[i] + 1
        d2 = d + j
        d2 %= 4 if i==2 else 3
        tobj.AXYV[i] = d2 - 1
        v2 = self.setAnchor(tobj, i, how)
        w2 = tobj.ftAa(v2) if i==0 else tobj.ftAa(v2) if i==1 else tobj.ftAy(v2) if i==2 else tobj.ftAv(v2) if i==3 else -1
        i2 = 'A' if i==0 else 'X' if i==1 else 'Y' if i==2 else 'V' if i==3 else '??'
        if   tobj.SNAPS >= 3:      tobj.regSnap(f'AV.{i2}.{w2}', how)
        tobj.log(f'{how} [{i}] [{j}] tobj.AXYV[{i}]={tobj.AXYV[i]:2} : {d} {w:} {v:8} => {d2} {w2} {v2:8}')
        tobj.on_resize(tobj.width, tobj.height)

    @staticmethod    
    def setAnchor(tobj, i, how):
        tobj.setAa(tobj.AXYV[i]) if i==0 else tobj.setAx(tobj.AXYV[i]) if i==1 else tobj.setAy(tobj.AXYV[i]) if i==2 else tobj.setAv(tobj.AXYV[i]) if i==3 else None
        v  = tobj.aa if i==0 else tobj.ax if i==1 else tobj.ay if i==2 else tobj.av if i==3 else -1
        np, nl, ns, nc, nt = tobj.n   ;   k = 'align'
        tobj.dumpTniksPfx(how)
        for p in range(np):
            if   i==0:                 tobj.E[P][p].document.set_style(0, len(tobj.E[P][p].document.text), {k:v})
            elif i==1:                 tobj.E[P][p].anchor_x       = v
            elif i==2:                 tobj.E[P][p].anchor_y       = v
            elif i==3:                 tobj.E[P][p].content_valign = v
            for l in range(nl):
                if   i==0:             tobj.E[L][l].document.set_style(0, len(tobj.E[L][l].document.text), {k: v})
                elif i==1:             tobj.E[L][l].anchor_x       = v
                elif i==2:             tobj.E[L][l].anchor_y       = v
                elif i==3:             tobj.E[L][l].content_valign = v
                for s, s2 in enumerate(tobj.ss2sl()):
                    if   i==0:         tobj.E[S][s].document.set_style(0, len(tobj.E[S][s].document.text), {k: v})
                    elif i==1:         tobj.E[S][s].anchor_x       = v
                    elif i==2:         tobj.E[S][s].anchor_y       = v
                    elif i==3:         tobj.E[S][s].content_valign = v
                    for c in range(nc):
                        if   i==0:     tobj.E[C][c].document.set_style(0, len(tobj.E[C][c].document.text), {k: v})
                        elif i==1:     tobj.E[C][c].anchor_x       = v
                        elif i==2:     tobj.E[C][c].anchor_y       = v
                        elif i==3:     tobj.E[C][c].content_valign = v
                        for t in range(nt):
                            _,j,kk,z = tobj.tnikInfo(p, l, s2, c, t, why=how)   ;   u = t+c*nt
                            if   i==0: tobj.E[j][u].document.set_style(0, len(tobj.E[j][u].document.text), {k: v})
                            elif i==1: tobj.E[j][u].anchor_x       = v
                            elif i==2: tobj.E[j][u].anchor_y       = v
                            elif i==3: tobj.E[j][u].content_valign = v
        tobj.dumpTniksSfx(how)
        return v
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
class TogZZsCmd(Cmd):
    def __init__(self, tobj, how, z):
        self.tobj, self.how, self.z = tobj, how, z
        
    def do(  self): self._togZZs()
    def undo(self): self._togZZs()
    
    def _togZZs(self):
        tobj, how, z = self.tobj, self.how, self.z
        assert z in (0, 1),  f'{z=} {tobj.zz=}'
        msg2 = f'{how} {z=}'
        tobj.dumpGeom('BGN', f'     {msg2}')
        if   z not in tobj.ZZ:     msg = f'ADD.{tobj.addC}'    ;   tobj.addZZs(   z, how) # tobj.addingz = 1
        else:                      msg = f'HID.{tobj.remC}'    ;   tobj.removeZZs(z, how) # tobj.addingz = 0
        if   tobj.SNAPS >= 3:      tobj.regSnap(f'{msg}.{z}', how)
        tobj.on_resize(tobj.width, tobj.height, z=z)
        tobj.dumpGeom('END', f'{msg} {msg2}')
########################################################################################################################################################################################################
class UnselectTabsCmd(Cmd):
    def __init__(self, tobj, how, m, cn=None, dbg=1):
        self.tobj, self.how, self.m, self.cn, self.dbg = tobj, how, m, cn, dbg
        
    def do(  self): self._unselectTabs()
    def undo(self): self._unselectTabs()
    
    def _unselectTabs(self):
        tobj, how, m, cn, dbg = self.tobj, self.how, self.m, self.cn, self.dbg
        if cn is None:      cc = tobj.cc   ;      cn = tobj.cc2cn(cc)
        else:               cc = tobj.cn2cc(cn)
        nt = tobj.n[T]  ;   k = cn * nt    ;   style = NORMAL_STYLE
        if tobj.LL:         tobj.setLLStyle(cc, style)
        if dbg:             tobj.dumpSmap(f'BGN {how} {m=} {cn=} {cc=} {k=}')
        tobj.setTNIKStyle(k, nt, style)
        if cn in tobj.smap: tobj.smap.pop(cn)
        elif dbg:           tobj.log(f'{cn=} not found in smap={fmtm(tobj.smap)}')
        if m:               cmd = MoveCmd(tobj, how, m)     ;  cmd.do()
        if dbg:             tobj.dumpSmap(f'END {how} {m=} {cn=} {cc=} {k=}')
########################################################################################################################################################################################################
class UpdateCursorCmd(Cmd):
    def __init__(self, tobj, why, dbg=1):
        self.tobj, self.why, self.dbg = tobj, why, dbg
        
    def do(  self): self._updateCursor()
    def undo(self): self._updateCursor() # todo fixme
    
    def _updateCursor(self):
        tobj, why, dbg = self.tobj, self.why, self.dbg
        x, y, w, h, c = tobj.cc2xywh()
        tobj.updateTnik(tobj.hcurs, 0, H, x, y, w, h, why=why, v=1, dbg=dbg)
########################################################################################################################################################################################################
class UpdateTniksCmd(Cmd):
    def __init__(self, tobj, how, w, h, z=None, dbg=1):
        self.tobj, self.how, self.w, self.h, self.z, self.dbg = tobj, how, w, h, z, dbg
        
    def do(  self): self._updateTniks()
    def undo(self): self._updateTniks()
    
    def _updateTniks(self):
        tobj, z, dbg = self.tobj, self.z, self.dbg
        if self.w is not None and self.h is not None:        pyglet.window.Window.on_resize(tobj, self.w, self.h)
        tobj.updC += 1  ;  why = f'Upd{tobj.updC}'  ;  ll = tobj.LL   ;  np, nl, ns, nc, nt = tobj.n
        tobj.updView(len(tobj.ZZ), tobj.LL * tobj.n[L])
        tobj.dumpTniksPfx(why)
        if   tobj.DSP_J_LEV == P:
            for _ in                     tobj.g_updateTniks(tobj.pages, P, None, why=why):  pass
        elif tobj.DSP_J_LEV == L:
            for page in                  tobj.g_updateTniks(tobj.pages, P, None, why=why):  # pass
                for _ in                 tobj.g_updateTniks(tobj.lines, L, page, why=why):  pass
        elif tobj.DSP_J_LEV == S:
            for page in                  tobj.g_updateTniks(tobj.pages, P, None, why=why):  # pass
                for l, line in enumerate(tobj.g_updateTniks(tobj.lines, L, page, why=why)): # pass
                    if ll and not l:     tobj.updateLLs(line, 1, why)
                    for _ in             tobj.g_updateTniks(tobj.sects, S, line, why=why):  pass
        elif tobj.DSP_J_LEV == C:
            for page in                  tobj.g_updateTniks(tobj.pages, P, None, why=why):  # pass
                for l, line in enumerate(tobj.g_updateTniks(tobj.lines, L, page, why=why)): # pass
                    if ll and not l:     tobj.updateLLs(line, 1, why)
                    for sect in          tobj.g_updateTniks(tobj.sects, S, line, why=why):  # pass
                        for _ in         tobj.g_updateTniks(tobj.colms, C, sect, why=why):  pass
        else:
            for page in                      tobj.g_newUpdTniks(P,                 nw=0, pt=None, why=why):  # pass
                for l, line in     enumerate(tobj.g_newUpdTniks(L,                 nw=0, pt=page, why=why)): # pass
                    if ll and l:             tobj.updateLLs(line, 1, why) #                        if zz:               tobj.updateZZs(sect, s, z, why)
                    for s, sect in enumerate(tobj.g_newUpdTniks(S,                 nw=0, pt=line, why=why)): # pass
                        for colm in          tobj.g_newUpdTniks(C, m=l*ns*nc+s*nc, nw=0, pt=sect, why=why):  # pass
                            for _ in         tobj.g_newUpdTniks(T,                 nw=0, pt=colm, why=why):  pass # s=l*ns+zs()[s]
            tobj.resetH()
        tobj.dumpTniksSfx(why)
        if tobj.cursor:                 cmd = UpdateCursorCmd(tobj, why)  ;  cmd.do()   ;   tobj.dumpHdrs()
        if dbg and tobj.SNAPS >= 10:    tobj.regSnap(f'Upd.{tobj.updC}', why)
        if dbg:    tobj.dumpStruct(why) # , dbg=dbg)
########################################################################################################################################################################################################
