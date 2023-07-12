    def flipZZs(self, how, zz):
        ii   = 0 if not zz else 2
        msg2 = f'{how} {zz=}'
        self.dumpGeom('BGN', f'     {msg2}')
        if   zz not in self.ZZ and not self.D[ii]: msg = 'ADD'    ;   self.addZZs(how, zz)
        elif zz     in self.ZZ:                    msg = 'HIDE'   ;   self.hideZZs(how, zz)
        else:                                      msg = 'SKIP'   ;   self.dumpGeom(W*3, f'{msg} {msg2}')   ;   self.flipZZ(zz)
        self.on_resize(self.width, self.height)
        self.dumpGeom('END', f'{msg} {msg2}')

    def flipZZ(self, zz, why=Z):
        self.dumpGeom('BFR', why)
        self.ZZ.add(zz) if zz not in self.ZZ else self.ZZ.remove(zz)
        n = self.n[C] + self.zzl()
        self.dumpGeom('AFT', why)
        return n
    ####################################################################################################################################################################################################
    def NEW__addZZs(self, how, ii):
        why = f'ADD {how} {ii=}'      ;   why1, why2 = 'Ref1', 'Ref2'
        np, nl, ns, nc, nt = self.n   ;   zz = self.zz2sl() # call after flipZ???
        n = self.flipZZ(ii)
        self.dumpTniksPfx(why)
        for v, view in enumerate(self.views):
            self.dumpTnik(view, M, why=why1)
            self.splitH(view, n)
            self.dumpTnik(view, M, why=why2)
            for p in range(np):
                self.setJdump(P, p, why=why2) # p
                for l in range(nl):
                    self.setJdump(L, l, why=why2) # l
                    for s, s2 in enumerate(self.ss2sl()):
                        self.setJdump(S, s2, why=why2) # s2
                        for c in zz:
                            if c == ii:     self.addZZ(p, l, s, c, why)
                            else:           self.refZZ(p, l, s, c)
                        for c in range(nc): self.refZZ(p, l, s, c)
        self.dumpTniksSfx(why)
    def addZZs(self, how, ii, dbg=0):
        if dbg: self.log(f'{ii=} {how}')
        np, nl, ns, nc, nt = self.n
        for p in range(np):
            self.pages[p] = self.splitH(self.pages[p], self.n[C] + self.zzl() + 1)
            self.dumpTnik(self.pages[p], P, 'Ref')
        if self.RESIZE:   self.resizeTniks(dbg=1)
        self.flipZZ(ii)  # zz = self.zz2sl()   ;   nc += len(zz)
    def OLD__addZZs(self, how, ii, dbg=0):
        why = 'Add'   ;   self.log(f'{why} {ii=} {how}') if dbg else None # ;  why1 = f'{why} {how} {ii=}'  ;  why2 = 'Ref'
        np, nl, ns, nc, nt = self.n
        self.flipZZ(ii) #        zz = self.zz2sl()   ;   nc += len(zz)
#        self.dumpTniksPfx(why1)
        for p in range(np): #            self.setJdump(P, p, why=why2)
            self.pages[p] = self.splitH(self.pages[p], self.n[C] + self.zzl())
        if self.RESIZE:     self.resizeTniks(dbg=1)
#            if self.isV() and 0:
#                for l in range(nl): #                    self.setJdump(L, l, why=why2)
#                    self.g_resizeTniks(self.lines, L, None, why=why2, dbg=1)
#                    for s in range(self.ssl()): #                        self.setJdump(S, s, why=why2)
#                        s += l * ns
#                        self.createZZs(self.sects[s], s, why, dbg=1)
#                        for c in range(nc): self.refZZ(p, l, s, c)
#                        for c in self.zz2sl():
#                            if   c == ii:      self.addZZ(p, l, s, c, why)
#                            else:              self.refZZ(p, l, s, c)
#        self.dumpTniksSfx(why1)
    ####################################################################################################################################################################################################
    def addZZ(self, p, l, s, c, why):
        np, nl, ns, nc, nt = self.n   ;   z1 = self.z1(c)   ;   z2 = self.z2(c)
        for zc in self.g_createTniks(self.zclms, E, self.sects[s], ii=c, why=why):
            c2 = c + nc*(s + ns*(l + nl*p))
            self.log(f'j={C} {JTEXTS[C]:4} {c=} {c2=}  lc={len(self.zclms)} plsc ={self.fplsc(p, l, s, c)} J1={self.fmtJ1(0, 1)} J2={self.fmtJ2(0, 1)} {z1=} {z2=}', f=0)
            for t, _ in enumerate(self.g_createTniks(self.snums, T, zc, why=why)):
                tlist, j, kk, txt = self.tnikInfo(*self.J1plsct(), z=1)
                self.log(f'{t=} {j=} {JTEXTS[j]:4} {c=} {c2=} ltl={len(tlist)} plsct={self.fplsct(p, l, s, c, t)} J1={self.fmtJ1(0, 1)} J2={self.fmtJ2(0, 1)} {z1=} {z2=}', f=0)

    def refZZ(self, p, l, s, c, zz=None):
        np, nl, ns, nc, nt = self.n   ;   why = 'Ref'
        self.setJdump(C, c, why=why)
#            self.setJ(C, c3)
#            self.dumpTnik(self.colms[c3], C, why2)
        tlist, j, _, _ = self.tnikInfo(p, l, s, c, zz)
        self.log(f'{zz=} j={C} {JTEXTS[C]:4} {nc=}       ltl={len(tlist)} plsc =[{self.fplsc(p, l, s, c)} J1={self.fmtJ1(0, 1)} J2={self.fmtJ2(0, 1)} z1={self.z1(c)} z2={self.z2(c)}', f=0)
        for t in range(nt):
            t2 = t + nt*(c + nc*(s + ns*(l + nl*p))) if j <= K else t
#                self.setJdump(j2, t, why=why2)
            self.setJ(j, t2)
            self.dumpTnik(tlist[t2], j, why)
            self.log(f'{zz=} {j=} {JTEXTS[j]:4} {nc=} {t2=} ltl={len(tlist)} plsct={self.fplsct(p, l, s, c, t)} J1={self.fmtJ1(0, 1)} J2={self.fmtJ2(0, 1)}', f=0)
    ####################################################################################################################################################################################################
    def hideZZs(self, how, ii, dbg=1):
        why = f'HIDE {how} ii={ii}'   ;   why2 = 'Ref'  # ;  c2, t2 = 0, 0
        self.flipZZ(ii)
        np, nl, ns, nc, nt = self.n   ;    nc += self.zzl()   ;   ns = self.ssl()
        self.dumpTniksPfx(why)
        for p in range(np):
            self.setJdump(P, p, why=why2)
            for l in range(nl):
                self.setJdump(L, l, why=why2)
                for s, s2 in enumerate(self.ss2sl()):
                    self.setJdump(S, s2, why=why2)
                    for c in range(nc):
                        if c in self.ZZ:
                            tlist, j = self.OLD__tnikInfo(s2, c)   ;   z1 = self.z1()   ;   z2 = self.z2()
                            c2 = ((p * nl + l) * ns + s) * nc + c
                            self.log(f'  ii={ii} s={s} s2={s2} c={c} c2={c2} z1={z1} z2={z2} J1={self.fmtJ1()} J2={self.fmtJ2()}')
                            self.hideTnik(self.colms, c2, C, dbg=dbg)
                            for t in range(nt):
                                self.hideTnik(tlist, self.J1[j], j, dbg=dbg)
                        else:
                            tlist, j = self.OLD__tnikInfo(s2, c)   ;   z1 = self.z1()   ;   z2 = self.z2()
                            self.log(f'  ii={ii} s={s} s2={s2} c={c}     z1={z1} z2={z2} J1={self.fmtJ1()} J2={self.fmtJ2()}')
                            self.setJdump(C, c, why=why2) #  c
                            for t in range(nt):
#                                self.setJdump(j, t, why=why2)
                                self.setJ(j, t + c * nt)
                                self.dumpTnik(tlist[t + c * nt], j, why=why2)
        self.dumpTniksSfx(why)
    ####################################################################################################################################################################################################
    def splitH( self, p, n, dbg=1):
        if   util.isi(p, LBL):
            p.x, p.width,   self.p0x, self.p0w = self.splitHL(p.x, p.width, n)
            if dbg:         self.log(f'{p.x=:.2f} {p.width=:.2f} {n=} {self.p0x=:.2f} {self.p0w=:.2f}')
        elif util.isi(p, SPR):
            p.x, p.scale_x, self.p0x, self.p0w = self.splitHS(p.x, p.width, n, p.image.width)
            if dbg:         self.log(f'{p.x=:.2f} {p.scale_x=:.4f} {n=} {self.p0x=:.2f} {self.p0w=:.2f} {self.p0sx=:.4f}')
        return p

    def splitHL(self, x, w, n):
        x0 = x                     ;   w0 = w
        w2 = w/n                   ;   w -= w2
        x = w2 + w2/2 + w/2        ;   x2 = w2
        self.log(f'{x0=:6.2f} {w0=:6.2f} {n=} {x=:6.2f} {w=:6.2f} {x2=:6.2f} {w2=:6.2f}')
        return x, w, x2, w2

    def splitHS(self, x, w, n, s):
        x0 = x      ;   w0 = w     ;   s0 = s
        w2 = w/n    ;   w -= w2    ;   s  = w/s0
        x = w2 + w2/2 + w/2        ;   x2 = w2
        self.log(f'{x0=:6.2f} {w0=:6.2f} {s0=:6.4f} {n=} {x=:6.2f} {w=:6.2f} {s=:6.4f} {x2=:6.2f} {w2=:6.2f}')
        return x, s, x2, w2
    ####################################################################################################################################################################################################
#    def sprite2LabelPos(self, x, y, w, h, dbg=0): x0 = x  ;  y0 = y  ;  x += w/2  ;  y -= h/2  ;  self.log(f'{x0=:6.2f} {y0=:6.2f}, {w/2=:6.2f} {-h/2=:6.2f}, {x=:6.2f} {y=:6.2f} {self.p0x=:6.2f} {self.p0y=:6.2f}', so=1) if dbg else None  ;  return x, y
    ####################################################################################################################################################################################################
    def createZZs(self, p, s, why, dbg=1):
        n = self.n[C] + self.zzl()
        kz = self.k[E]   ;  kk = self.cci(E, s, kz) if self.CHECKERED else 0
        nz, iz, xz, yz, wz, hz = self.geom(E, p, n, s, dbg=dbg)
        zclm = self.createTnik(self.zclms, s, E, xz, yz, wz, hz, kk, kz, why, v=1, dbg=dbg)
        if s in (0, 2):
            nu, iu, xu, yu, wu, hu = self.geom(B, zclm, self.n[T], self.i[L], dbg=dbg)
            for u in range(nu):
                self.createZZ(s, u, xu, yu, wu, hu, why)
        if s in (1, 3):
            na, ia, xa, ya, wa, ha = self.geom(A, zclm, self.n[T], self.i[L], dbg=dbg)
            for a in range(na):
                self.createZZ(s, a, xa, ya, wa, ha, why)
        p = self.splitH(p, n, dbg)
        self.dumpTnik(p, S, why=why)
        return p

    def createZZ(self, s, i, x, y, w, h, why, dbg=1):
        self.log(f'ntp={self.fntp(1, 1)}')
        cc = i + s * self.ntp()[0]   ;   kk = NORMAL_STYLE
        p, l, c, t = self.cc2plct(cc)
        tlist, j, ki, txt = self.tnikInfo(p, l, s, c, t, z=1)
        tnik = self.createTnik(tlist, cc, j, x, y-i*h, w, h, kk, ki, why, t=txt, v=1, dbg=dbg)
        return tnik

    def resizeZZs(self, pt, why, dbg=1):
        n    = self.n[C] + self.zzl()
        nz, iz, xz, yz, wz, hz = self.geom(E, pt, n, self.i[S], dbg=dbg)
        zclm = self.resizeTnik(self.zclms, self.J2[E], E, xz, yz, wz, hz, why, dbg=dbg)
        nu, iu, xu, yu, wu, hu = self.geom(B, zclm, self.n[T], self.i[L], dbg=dbg)
        for u in range(nu):
            self.resizeTnik(self.snums, self.J2[B], B, xu, yu-u*hu, wu, hu, why, dbg=dbg)
        pt   = self.splitH(pt, n, dbg=dbg)
        return pt
    ####################################################################################################################################################################################################
