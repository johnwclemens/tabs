#from collections import OrderedDict as cOd
#sys.path.append(os.path.abspath("./lib"))
#print(f'{len(sys.path)=}')
#for _ in sys.path:
#    print(f'{_}')
from   collections import Counter
from   tpkg        import utl
from   tpkg.notes  import Notes
from   tpkg        import cdata

NT               = Notes.NT
W, Y, Z          = utl.W, utl.Y, utl.Z
slog, fmtl, fmtm = utl.slog, utl.fmtl, utl.fmtm
ist              = utl.ist
FMTN             = (1, 1, 2, 2, 2, 2, 2)

class Chords:
    MIN_IVAL_LEN  = 1
    MIN_CHORD_LEN = 3
    def __init__(self, tobj, sobj):
        self.tobj                 = tobj
        self.sobj                 = sobj
        self.chordCounter         = Counter()
        self.limap,  self.mlimap  = [], {}
        self.umap,   self.cycles  = {}, {}
        self.catmap, self.catmap2 = {}, {}
        self.cat1,   self.cat2    = set(), set()
        self.cat3                 = {}
        self.OMAP                 = cdata.OMAP
        
    @staticmethod
    def checkOmap(o):
        assert     ist(o,      tuple),  slog(f'ERROR: Invalid type, expected tuple {type(o)=}')
        assert     ist(o[0],     int),  slog(f'ERROR: Invalid type, expected int   {type(o[0])=}')
        assert     ist(o[1],    list),  slog(f'ERROR: Invalid type, expected list  {type(o[1])=}')
        assert     ist(o[2],    list),  slog(f'ERROR: Invalid type, expected list  {type(o[2])=}')
        for i in range(len(o[1])):
            assert ist(o[1][i],  int),  slog(f'ERROR: Invalid type, expected int   {type(o[1][i])=}')
        for i in range(len(o[2])):
            assert ist(o[2][i],  str),  slog(f'ERROR: Invalid type, expected str   {type(o[2][i])=}')
        return tuple(o[2])
    ####################################################################################################################################################################################################
    def getChordName(self, data, nic, cn, p, l, c, dbg=0):
        ikeys, ivals, notes, name, chunks, rank = [], [], [], Z, [], -1
        vkeys, self.limap, imap, _imap, nnt     = [], [], [], None, NT
        mask,          notes,         js        = self._getIndices(data, nic, p, l, c)   ;   omap = self.OMAP
        for k, jk in enumerate(js):
            ivals = [ ((ji-jk) if ji >= jk else (nnt+(ji-jk))) % nnt for ji in js ]
            vkey  = Z.join([ f'{v:x}' for v in ivals ])   ;   chunks = []   ;   rank = -1
            if vkey not in vkeys:
                ikeys        = [ Notes.I2V[i] for i in ivals ]
                if dbg:        self._dumpData(rank, ikeys, ivals, notes, mask, 0)
                _imap        = dict(sorted(dict(zip(ikeys, notes)).items(), key=lambda t: Notes.V2I[t[0]]))
                _ikeys       = list(_imap.keys())   ;     _ivals = [ Notes.V2I[k] for k in _ikeys ]   ;   _notes = list(_imap.values())   ;   leni = len(_imap)
                ikey         = W.join(_ikeys)
                if ikey in omap:
                    root     = _imap['R']           ;     chunks.append(root)
                    chnks    = self.checkOmap(omap[ikey])
                    chnks   = [ n for n in chnks if n ]
                    chunks.extend(chnks)
                    if root != notes[0]:                  nsfx = f'/{notes[0]}'  ;  chunks.append(nsfx)
                    name     = Z.join(chunks)       ;     rank = omap[ikey][0]
                    assert _ivals == omap[ikey][1],       slog(f'Error _ivals != omap[ikey][1], {_ivals=} {omap[ikey][1]=}')
                elif len(_imap) >= self.MIN_CHORD_LEN:    self.add2uMap(leni, ikey, rank, ivals)
                elif len(_imap) >= self.MIN_IVAL_LEN:     slog(f'{leni=} is Not a Chord {ikey=:21} v={fmtl(sorted(ivals))}')
                if dbg:                  self._dumpData(rank, _ikeys, _ivals, _notes, mask, 1)
                imap         = [ ikeys, ivals, notes, name, chunks, rank ]
                vkeys.append(vkey)   ;   self.limap.append(imap)
                if dbg: slog(f'{rank:2} {Z.join(ikeys):12} {Z.join(f"{i:x}" for i in ivals):6} {Z.join(notes):12} {name:12} {Z.join(chunks):12} {Z.join(_ikeys):12} {Z.join(f"{i:x}" for i in _ivals):6} {Z.join(_notes):12}')
                if dbg: slog(f'{rank:2} {fmtl(ikeys):19} {fmtl(ivals, w="x")} {W.join(notes):12} {name:12} {Z.join(chunks)} {fmtl(_ikeys)} {fmtl(_ivals, w="x")} {W.join(_notes):12}') #fix me
        if  self.limap:
            self.limap.sort(key=lambda m: m[-1])   ;   imi = 0
            if dbg > 1: self.dumpLimap(self.limap, cn, imi)
            self.mlimap[cn]  = [ self.limap, imi ]
            return               self.limap[imi]
        return     imap # [ ikeys, ivals, notes, name, chunks, rank ]
    ####################################################################################################################################################################################################
    def add2uMap(self, li, ikey, rank, ivals, dbg=0):
        kc = self.chordCounter
        kc[ikey]    += 1
        if kc[ikey] != 1:  slog(f'return already counted {ikey=:17} {kc=}') if dbg else None    ;    return
        if dbg:            slog(f'{li=} Adding {ikey=} v={fmtl(sorted(ivals))} to umap')
        self.umap[ikey] = (rank, ivals, [])
        self.dumpUmap() if dbg else None
    ####################################################################################################################################################################################################
    def _getIndices(self, data, nic, p, l, c, dbg=0):
        strNumbs   = self.sobj.numbs
        strKeys    = self.sobj.keys
        strNames   = self.sobj.names
        _tabs      = data[p][l][c]
        strIndices = [ Notes.n2i(k, 1) for k in strKeys ]
        mask, indices, notes = [], [], []  ;  nt = len(_tabs)
        for t in range(nt-1, -1, -1):
            if self.sobj.isFret(_tabs[t]):
                fn    = self.sobj.tab2fn(_tabs[t])
                index = self.sobj.fn2ni(fn, t)
                note  = self.sobj.tab2nn(_tabs[t], t, nic=nic)
                if index: indices.append(index)
                if note :   notes.append(note)   ;   mask.append(1)
                else:        mask.append(0)
            else:            mask.append(0)
        if notes:
            mask0 = [1] * self.sobj.nStrings()
            if dbg: self.dumpData(strNumbs,   mask0, 'strNumbs', r=1)
            if dbg: self.dumpData(strKeys,    mask0, 'strKeys')
            if dbg: self.dumpData(strIndices, mask0, 'strIndices')
            if dbg: self.dumpData(strNames,   mask0, 'strNames', r=1)
            if dbg: self.dumpData(_tabs,      mask0, 'Tabs',     r=1)
            if dbg: self.dumpData(indices,    mask,  'Note Indices')
            if dbg: self.dumpData(notes,      mask,  'Notes')
        return mask, notes, indices
    ####################################################################################################################################################################################################
    def _dumpData(self, rank, ikeys, ivals, notes, mask, a):
        ikey = W.join(ikeys)   ;   ival = Z.join([ f'{v:x}' for v in ivals ])   ;   note = W.join(notes)  # ;   r = f'{rank:2}'
        if a: self.dumpData(ikeys, mask, f'{rank:2} ikeys {ikey}')   ;   self.dumpData(ivals, mask, f'{rank:2} ivals {ival}')   ;   self.dumpData(notes, mask, f'{rank:2} Notes {note}')
        else: self.dumpData(notes, mask, f'{rank:2} Notes {note}')   ;   self.dumpData(ivals, mask, f'{rank:2} ivals {ival}')   ;   self.dumpData(ikeys, mask, f'{rank:2} ikeys {ikey}')

    @staticmethod
    def dumpData(data, mask, why, w=5, u='<', r=0):
        if r:     data = data[::-1]  ;  mask = mask[::-1]
        j = 0   ;   dt = type(data)  ;  slog(f'{why:26} [ ', e=Z)
        if dt is list or dt is str:
            for m in mask:
                if   m and j < len(data): slog(f'{data[j]:{u}{w}} ', p=0, e=Z)  ;  j += 1
                elif m:                   slog(f'{W:{u}{w}} ',       p=0, e=Z)
                else:         _ = '~'  ;  slog(f'{_:{u}{w}} ',       p=0, e=Z)
        elif dt is dict:
            w2 = 2  ;   i = 0
            for k,v in data.items():
                while not mask[i]: _ = '-'   ;   slog(f'{_:{u}{w}} ', p=0, e=Z)  ;  i += 1
                slog(f'{k:>{w2}}:{v:<{w2}} ',                         p=0, e=Z)  ;  i += 1
            while i < len(mask):   _ = '-'   ;   slog(f'{_:{u}{w}} ', p=0, e=Z)  ;  i += 1
        else: slog(f'type={dt} ', p=0, e=Z)
        slog(']',                 p=0)
    ####################################################################################################################################################################################################
    def dumpMlimap(self, why=Z, dbg=0):
        mli = self.mlimap
        slog(f'{why} <dumpLimap > {len(mli)} {fmtl(list(mli.keys()))}') if dbg else None   ;   [ self.dumpLimap( v[0], k, v[1]) for k,v in mli.items() ]
        slog(f'{why} <dumpLimap1> {len(mli)} {fmtl(list(mli.keys()))}') if dbg else None   ;   [ self.dumpLimap1(v[0], k, v[1]) for k,v in mli.items() ]
        slog(f'{why} <dumpLimap2> {len(mli)} {fmtl(list(mli.keys()))}') if dbg else None   ;   [ self.dumpLimap2(v[0], k, v[1]) for k,v in mli.items() ]
        slog(f'{why} <dumpLimap3> {len(mli)} {fmtl(list(mli.keys()))}') if dbg else None   ;   [ self.dumpLimap3(v[0], k, v[1]) for k,v in mli.items() ]

    def dumpLimap(self, limap, key, imi=-1):
        [ self.dumpImap(im, f'{key:3} {imi}') for im in limap ]

    @staticmethod
    def dumpLimap1(limap, key, imi=-1):
        slog(f'{key:3} {imi}', p=0, e=W)
        for m in limap:
            slog(f'{Z.join(m[3]):12} {Z.join(m[0]):12}', p=0, e=W)
        slog(p=0)

    @staticmethod
    def dumpLimap2(limap, key, imi=-1):
        slog(f'{key:3} {imi}', p=0, e=W)
        [ slog(f'{m[3]:12} {Z.join(f"{i:x}" for i in m[1]):6}', p=0, e=Z) for m in limap ]
        slog(p=0)

    @staticmethod
    def dumpLimap3(limap, key, imi=-1):
        slog(f'{key:3} {imi}', p=0, e=W)   ;   msg1, msg2 = [], []
        for m in limap:
            msg1.append(f'{Z.join(f"{i:x}" for i in m[1]):6} ')
            msg2.append(f'{Z.join(m[0]):12} ')
        slog(f'{Z.join(msg1):44}{Z.join(msg2)}', p=0)

    @staticmethod
    def dumpImap(imap, why=Z, f=0):
        if imap and len(imap) == 6: ikeys, ivals, notes, name, chunks, rank = imap[0], imap[1], imap[2], imap[3], imap[4], imap[5]
        else:                       ikeys, ivals, notes, name, chunks, rank =      [],      [],      [],       Z,      [],      -1
        ikeys2         = list(sorted(dict.fromkeys(ikeys), key=lambda t: Notes.V2I[t]))
        nmap           = dict(sorted(dict(zip(ivals, notes)).items()))
        ivals2, notes2 = list(nmap.keys()), list(nmap.values())
        slog(f'{why}{rank:2} {name:12} {Z.join(chunks):12} {Z.join(ikeys):12} {Z.join(f"{i:x}" for i in ivals):6} {Z.join(notes):12} {Z.join(ikeys2):12} {Z.join(f"{i:x}" for i in ivals2):6} {Z.join(notes2):12}', p=1, f=f)
        slog(f'{why}{rank:2} {name:12} {fmtl(chunks, w=2):19} {fmtl(sorted(ikeys, key=lambda t: Notes.V2I[t]), w=FMTN):18} {fmtl(ivals, w="x"):13} {fmtl(notes, w=2):19}', p=1)
    ####################################################################################################################################################################################################
    def rotateMLimap(self, cn):
        a = self.mlimap[cn]
        a = a[-1:] + a[:-1]
        self.mlimap[cn] = a
        return a
#        self.mlimap[cn] = (self.mlimap[cn][-1:] + self.mlimap[cn][:-1])

    @staticmethod
    def rotateList(a, rev=0):
        if rev: tmp0 = a[-1 ]   ;   tmp1 = a[:-1]   ;   a = tmp1   ;   a.insert(0, tmp0)
        else:   tmp0 = a[0]     ;   tmp1 = a[1:]    ;   a = tmp1   ;   a.append(tmp0)
        return a

    @staticmethod
    def rotateIndices(a):
        r = [0]   ;   nt = NT
        for i in range(1, len(a)):
            b = a[i+1] if i + 1 < len(a) else nt   ;   r.append(b - a[i] + r[i-1])
#           if    i + 1 < len(a): r.append(abs(a[i+1] - a[i] + r[i-1]) % nt)
#           else:                 r.append(abs(nt     - a[i] + r[i-1]) % nt)
        return r
#    @staticmethod
#    def fsort(ivals): s = set(ivals)   ;   return sorted(s)
    ####################################################################################################################################################################################################
    @staticmethod
    def key2Indices(k): # N/A?
        t = Z   ;   r = []
        for j in k:
            if j != W:   t += j # optimize str concat
            else:        r.append(Notes.V2I[t])  ;  t = Z
        r.append(Notes.V2I[t])
        return r

    @staticmethod
    def mergeMaps(src, trg):
        slog(f'BGN {len(src)=} {len(trg)=}')
        for k, v in src.items():
            trg[k] = v
        slog(f'END {len(src)=} {len(trg)=}')
    ####################################################################################################################################################################################################
    def dumpUmap(self): # optimize str concat?
        if self.umap:
            slog(f'BGN {len(self.OMAP)=} {len(self.umap)=}')
            umapKeys = sorted(self.umap.keys() , key=lambda a: self.umap[a][1])
            for k in umapKeys:
                v = self.umap[k]
                k = "'" + k + "'"
                slog(f'{k:18}: ({v[0]} {fmtl(sorted(v[1])):15})', f=2)
            slog(f'END {len(self.OMAP)=} {len(self.umap)=}')

    def dumpOMAP(self, catpath=None, merge=0):
        slog(f'BGN {len(self.OMAP)=} {len(self.umap)=}')
        if self.umap:           self.dumpUmap()
        if merge and self.umap: self.mergeMaps(self.umap, self.OMAP)
        if catpath:
            with open(str(catpath), 'w', encoding='utf-8') as CAT_FILE:
                self._dumpOMAP(CAT_FILE)
        slog(f'END {len(self.OMAP)=} {len(self.umap)=}')

    def getMapSets(self, omap):
        mapSet   = {}
        for k, v in omap.items():
            v1   = v[1]
            self.checkOmap(omap[k])
            msK  = len(v1)
            if msK not in mapSet: mapSet[msK] = set()
            if v[0] == -1:        v1 = sorted(v1)
            if mapSet:            mapSet[msK].add(tuple(v1))
        return mapSet

    def _dumpOMAP(self, catfile=None, dbg=1):
        file = catfile      if catfile else utl.LOG_FILE    ;   omap, l = self.OMAP, len(self.OMAP)   ;   r, rank = {}, -1   ;   j, mstat, tstat = 0, [], []
        name = catfile.name if catfile else None            ;    mapSet = self.getMapSets(omap)       ;   slog(f'BGN {l=} catfile.{name=}')     ;   msg = 'ERROR: Invalid Rank'
        for msK, msV in mapSet.items():
            tstat.append(0)  ;  count, nord, none = 0, 0, 0  ;      msV = sorted(msV) if msV else None
            for ii in msV:
                keys        = [ Notes.I2V[i] for i in ii ]   ;       j += 1
                keys        = sorted(keys, key=lambda a:   Notes.V2I[a])        ;     keyStr = W.join(keys)
                keyStrFmt   = "'" + keyStr + "'"       ;   v = omap[keyStr]     ;   rankSet  = set()  ;   rankSet.add(v[0])
                count += 1  ;  none += 1 if not v[2] else 0   ;   nord += 1 if v[0] == rank else 0
                v2          = fmtl(v[2], s="','", d="['", d2="']),") if v[2] else f"[{Z},{Z},{Z},{Z}])," if ist(v[2], list) else 'None),'
                slog(                    f'{j:4} {keyStrFmt:18}: ({v[0]}, {fmtl(ii, s=Y, d2="],"):16} {v2:30} # ', p=0, f=2, ft=0)
                if dbg:                   slog(f'{keyStrFmt:18}: ({v[0]}, {fmtl(ii, s=Y, d2="],"):16} {v2:30} # ', p=0, f=file, ft=0, e=Z)
                cycSet      = set()   ;   cycSet.add(tuple(ii))   ;   i2 = list(ii)
                for _ in range(len(ii) - 1):
                    i2      = self.rotateIndices(i2)
                    keys2   = [ Notes.I2V[i] for i in i2 ]
                    keyStr2 = W.join(keys2)   ;   ck = len(i2)    ;   jj = tuple(i2)    ;   cycle = 0   ;    keyStrFmt2 = keyStr2
                    if keyStr2 in omap: rankSet.add(omap[keyStr2][0])
                    if jj in cycSet:
                        if ck not in self.cycles:        self.cycles[ck] = set()
                        self.cycles[ck].add(jj)    ;     cycle = 1
                    cycSet.add(jj)     ;      d = '@' if cycle else '['     ;      d2 = '@' if cycle else ']'
                    if keyStr2 not in omap:   slog('not in OMAP: ', p=0, e=Z, f=file)    ;    r[keyStr2] = (rank, i2, None)
                    if dbg:                   slog(f'{keyStrFmt2:16} {fmtl(i2, w="x", d=d, d2=d2):15} ', p=0, f=file, ft=0, e=Z)
                refSet      = set(range(len(i2)))
                if dbg:
                    if       rankSet == refSet or len(cycSet) != len(refSet) or -1 in rankSet:            slog(p=0, f=file, ft=0)
                    else:    slog(f'\n{msg} {fmtl(refSet, d="<", d2=">")} {fmtl(rankSet, d="<", d2=">")} {fmtl(sorted(cycSet))}', p=0, f=file, ft=0)
            mstat.append([msK, count, nord, none])
        for kk, w in self.cycles.items():
            for c in tuple(sorted(w)):
                keys    = [ Notes.I2V[j] for j in c ]   ;   key = W.join(keys)   ;   v = omap[key]
                slog(f'{kk:2} note cycle {v[0]:2} {fmtl(c, w="x"):13} {key:16} {Z.join(str(v[2])):12} {v[2]}')    # ? Expected type 'Iterable[str]', got 'int' instead ?
        for m in mstat:
            tstat[0]   += m[0]       ;   tstat[1] += m[1]     ;   tstat[2] += m[2]     ;   tstat[3] += m[3]
            slog(f'{m[0]:2} note chords  {tstat[1]:3}  {m[1]:3} valid  {m[2]:3} unordered  {m[3]:3} unnamed')
        lm, lr = len(omap), len(r)   ;   slog(f'{lm=} catfile.{name=} {lr=}')
        slog(f'END grand total {tstat[1]:3} total  {tstat[2]:3} unordered  {tstat[3]:3} unnamed  {len(r)=}')
        return r

    def add2cat(self, limap, cc): # N/A?
        self.dumpLimap(limap, cc)
        outer = []   ;   keys, ivals = [], []
        for i in limap:
            inner = []
            for j in i[0]:
                inner.append(Notes.V2I[j])
            tmp = tuple(inner)
            outer.append(tmp)
            self.cat2.add(tmp)
            k = len(inner)
            if k not in self.cat3:     self.cat3[k] = set()   ;   self.cat3[k].add(tmp)
            else:                      self.cat3[k].add(tmp)
            if tmp not in self.catmap: self.catmap[tmp] = [i[0], i[1]]
            keys.append(tmp)   ;   ivals.append(i[0])
        for k in keys:                 self.catmap2[k] = [ sorted(keys), sorted(ivals, key=lambda b: [Notes.V2I[c] for c in b]) ]
        outer = sorted(outer, key=lambda a: list(a))
        self.cat1.add(tuple(outer))
#        slog(f'{why}', end=Z)
#        for o in outer:
#            slog(f'{fmtl(o, w="x", d2="] ")}', pfx=0, end=Z)
#        slog(pfx=0)

    def dumpInstanceCat(self, why=Z):
        cat1 = sorted(self.cat1)
        cat2 = sorted(self.cat2)
        cat3 = self.cat3
        catmap = self.catmap
        catmap2 = self.catmap2
        slog(f'{why} cat1 <{len(cat1)}>')
        n = 0
        for c in cat1:
            n += len(c)
            slog(f'{n:3} {fmtl(c, w="x")}', p=0)
        slog(f'{why} cat2 <{len(cat2)}>')
        slog(f'{fmtl(cat2, w="x")}', p=0)
        for i, c in enumerate(cat2):
            slog(f'{i+1:3} {fmtl(c, w="x")}', p=0)
        slog(f'{why} cat3 <{len(cat3)}>')
        slog(f'{fmtm(cat3)}', p=0)
        for k in cat3.keys():
            cat3[k] = sorted(tuple(cat3[k]))
            for j, v in enumerate(cat3[k]):
                slog(f'{j+1:3} {fmtl(v, w="x")}', p=0)
        slog(f'{why} catmap <{len(catmap)}>')
        slog(f'{fmtm(catmap)}', p=0)
        for i, (k,v) in enumerate(catmap.items()):
            slog(f'{i+1:3} {fmtl(k, w="x")} {fmtl(v, w=2)}', p=0)
        slog(f'{why} catmap2 <{len(catmap2)}>')
        slog(f'{fmtm(catmap2)}', p=0)
        for k in cat3.keys():
            for i, v in enumerate(cat3[k]):
                slog(f'{i+1:3} {fmtl(v, w="x")}', p=0, e='  ')
                for j, u in enumerate(catmap2[v]):
                    for h, w in enumerate(u):
                        if j:        slog(f'{Z if h else "  "}{fmtl(w, w=FMTN)}', p=0, e=Z)
                        elif w != v: slog(f'{                  fmtl(w, w="x")}',  p=0, e=Z)
                slog(p=0)
