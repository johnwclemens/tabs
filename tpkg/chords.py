#from collections import OrderedDict as cOd
#sys.path.append(os.path.abspath("./lib"))
#print(f'{len(sys.path)=}')
#for _ in sys.path:
#    print(f'{_}')
from   collections import Counter
from   tpkg        import utl   as utl
from   tpkg.notes  import Notes as Notes

NTONES           = Notes.NTONES
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
        vkeys, self.limap, imap, _imap, nnt     = [], [], [], None, NTONES
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
        strNumbs   = self.sobj.stringNumbs
        strKeys    = self.sobj.stringKeys
        strNames   = self.sobj.stringNames
        _tabs      = data[p][l][c]
        strIndices = [ Notes.index(k, 1) for k in strKeys ]
        mask, indices, notes = [], [], []  ;  nt = len(_tabs)
        for t in range(nt-1, -1, -1):
            if self.sobj.isFret(_tabs[t]):
                fn    = self.sobj.tab2fn(_tabs[t])
                index = self.sobj.fn2ni(fn, t)
                note  = self.sobj.tab2nn(_tabs[t], t, nic)
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
        r = [0]   ;   ntones = NTONES
        for i in range(1, len(a)):
            b = a[i+1] if i + 1 < len(a) else ntones   ;   r.append(b - a[i] + r[i-1])
#           if    i + 1 < len(a): r.append(abs(a[i+1] - a[i] + r[i-1]) % ntones)
#           else:                 r.append(abs(ntones - a[i] + r[i-1]) % ntones)
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
                slog(f'{k:18}: ({v[0]} {fmtl(sorted(v[1])):15})', p=2)
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
    ####################################################################################################################################################################################################
    #    0  1  2  3  4  5  6  7  8   9  10 11 0
    #    R  b2 2  m3 M3 4  b5 5  #5  6  b7 7  R
    #       b9 9  #9    11 #11   b13 13    15
    ####################################################################################################################################################################################################
    OMAP = {
            'R b2 2'           : (2, [0,1,2],        ['b2','s2','x']),            # R b2 7           [0 1 b]       R b7 7           [0 a b]
            'R b2 m3'          : (2, [0,1,3],        ['m','b2','x']),             # R 2 7            [0 2 b]       R 6 b7           [0 9 a]
            'R b2 M3'          : (1, [0,1,4],        ['b2','x']),                 # R m3 7           [0 3 b]       R #5 6           [0 8 9]
            'R b2 4'           : (2, [0,1,5],        ['b2','s4','x']),            # R M3 7           [0 4 b]       R 5 #5           [0 7 8]
            'R b2 b5'          : (1, [0,1,6],        ['o','b2','y']),             # R 4 7            [0 5 b]       R b5 5           [0 6 7]
            'R b2 5'           : (2, [0,1,7],        ['b2','y']),                 # R b5 7           [0 6 b]       R 4 b5           [0 5 6]
            'R b2 #5'          : (2, [0,1,8],        ['+','b2','y']),             # R 5 7            [0 7 b]       R M3 4           [0 4 5]
            'R b2 6'           : (2, [0,1,9],        ['b2','6','y','x']),         # R #5 7           [0 8 b]       R m3 M3          [0 3 4]
            'R b2 b7'          : (1, [0,1,10],       ['b9','y','x']),             # R 6 7            [0 9 b]       R 2 m3           [0 2 3]
            'R b2 7'           : (1, [0,1,11],       ['M','b9','y','x']),         # R b7 7           [0 a b]       R b2 2           [0 1 2]
            'R 2 m3'           : (0, [0,2,3],        ['m','2','x']),              # R b2 b7          [0 1 a]       R 6 7            [0 9 b]
            'R 2 M3'           : (2, [0,2,4],        ['2','x']),                  # R 2 b7           [0 2 a]       R #5 b7          [0 8 a]
            'R 2 4'            : (1, [0,2,5],        ['s2','s4','x']),            # R m3 b7          [0 3 a]       R 5 6            [0 7 9]
            'R 2 b5'           : (1, [0,2,6],        ['o','s2']),                 # R M3 b7          [0 4 a]       R b5 #5          [0 6 8]
            'R 2 5'            : (1, [0,2,7],        ['s2']),                     # R 4 b7           [0 5 a]       R 4 5            [0 5 7]
            'R 2 #5'           : (1, [0,2,8],        ['+','s2']),                 # R b5 b7          [0 6 a]       R M3 b5          [0 4 6]
            'R 2 6'            : (1, [0,2,9],        ['6','s2','x']),             # R 5 b7           [0 7 a]       R m3 4           [0 3 5]
            'R 2 b7'           : (0, [0,2,10],       ['7','s2','x']),             # R #5 b7          [0 8 a]       R 2 M3           [0 2 4]
            'R 2 7'            : (0, [0,2,11],       ['M','7','s2','x']),         # R 6 b7           [0 9 a]       R b2 m3          [0 1 3]
            'R m3 M3'          : (1, [0,3,4],        ['#2','x']),                 # R b2 6           [0 1 9]       R #5 7           [0 8 b]
            'R m3 4'           : (2, [0,3,5],        ['m','4','x']),              # R 2 6            [0 2 9]       R 5 b7           [0 7 a]
            'R m3 b5'          : (0, [0,3,6],        ['o']),                      # R m3 6           [0 3 9]       R b5 6           [0 6 9]
            'R m3 5'           : (0, [0,3,7],        ['m']),                      # R M3 6           [0 4 9]       R 4 #5           [0 5 8]
            'R m3 #5'          : (1, [0,3,8],        ['m','+']),                  # R 4 6            [0 5 9]       R M3 5           [0 4 7]
            'R m3 6'           : (1, [0,3,9],        ['m','6','x']),              # R b5 6           [0 6 9]       R m3 b5          [0 3 6]
            'R m3 b7'          : (0, [0,3,10],       ['m','7','x']),              # R 5 6            [0 7 9]       R 2 4            [0 2 5]
            'R m3 7'           : (0, [0,3,11],       ['m','M','7','x']),          # R #5 6           [0 8 9]       R b2 M3          [0 1 4]
            'R M3 4'           : (1, [0,4,5],        ['4','x']),                  # R b2 #5          [0 1 8]       R 5 7            [0 7 b]
            'R M3 b5'          : (2, [0,4,6],        ['b5']),                     # R 2 #5           [0 2 8]       R b5 b7          [0 6 a]
            'R M3 5'           : (0, [0,4,7],        ['']),                       # R m3 #5          [0 3 8]       R 4 6            [0 5 9]
            'R M3 #5'          : (0, [0,4,8],        ['+']),                      # R M3 #5          @0 4 8@       R M3 #5          @0 4 8@
            'R M3 6'           : (1, [0,4,9],        ['6','x']),                  # R 4 #5           [0 5 8]       R m3 5           [0 3 7]
            'R M3 b7'          : (0, [0,4,10],       ['7','x']),                  # R b5 #5          [0 6 8]       R 2 b5           [0 2 6]
            'R M3 7'           : (0, [0,4,11],       ['M','7','x']),              # R 5 #5           [0 7 8]       R b2 4           [0 1 5]
            'R 4 b5'           : (1, [0,5,6],        ['o','s4']),                 # R b2 5           [0 1 7]       R b5 7           [0 6 b]
            'R 4 5'            : (2, [0,5,7],        ['s4']),                     # R 2 5            [0 2 7]       R 4 b7           [0 5 a]
            'R 4 #5'           : (2, [0,5,8],        ['+','s4']),                 # R m3 5           [0 3 7]       R M3 6           [0 4 9]
            'R 4 6'            : (2, [0,5,9],        ['6','s4','x']),             # R M3 5           [0 4 7]       R m3 #5          [0 3 8]
            'R 4 b7'           : (0, [0,5,10],       ['7','s4','x']),             # R 4 5            [0 5 7]       R 2 5            [0 2 7]
            'R 4 7'            : (0, [0,5,11],       ['M','7','s4','x']),         # R b5 5           [0 6 7]       R b2 b5          [0 1 6]
            'R b5 5'           : (2, [0,6,7],        ['#4','y']),                 # R b2 b5          [0 1 6]       R 4 7            [0 5 b]
            'R b5 #5'          : (2, [0,6,8],        ['o','+','y']),              # R 2 b5           [0 2 6]       R M3 b7          [0 4 a]
            'R b5 6'           : (2, [0,6,9],        ['o','6','y']),              # R m3 b5          [0 3 6]       R m3 6           [0 3 9]
            'R b5 b7'          : (0, [0,6,10],       ['o','7','y']),              # R M3 b5          [0 4 6]       R 2 #5           [0 2 8]
            'R b5 7'           : (0, [0,6,11],       ['M','o','7','y']),          # R 4 b5           [0 5 6]       R b2 5           [0 1 7]
            'R 5 #5'           : (1, [0,7,8],        ['b6','y']),                 # R b2 4           [0 1 5]       R M3 7           [0 4 b]
            'R 5 6'            : (2, [0,7,9],        ['6','y']),                  # R 2 4            [0 2 5]       R m3 b7          [0 3 a]
            'R 5 b7'           : (0, [0,7,10],       ['7','y']),                  # R m3 4           [0 3 5]       R 2 6            [0 2 9]
            'R 5 7'            : (0, [0,7,11],       ['M','7','y']),              # R M3 4           [0 4 5]       R b2 #5          [0 1 8]
            'R #5 6'           : (2, [0,8,9],        ['+','6','y']),              # R b2 M3          [0 1 4]       R m3 7           [0 3 b]
            'R #5 b7'          : (1, [0,8,10],       ['+','7','y']),              # R 2 M3           [0 2 4]       R 2 b7           [0 2 a]
            'R #5 7'           : (0, [0,8,11],       ['M','+','y']),              # R m3 M3          [0 3 4]       R b2 6           [0 1 9]
            'R 6 b7'           : (1, [0,9,10],       ['13','x','y']),             # R b2 m3          [0 1 3]       R 2 7            [0 2 b]
            'R 6 7'            : (2, [0,9,11],       ['M','13','y','x']),         # R 2 m3           [0 2 3]       R b2 b7          [0 1 a]
            'R b7 7'           : (0, [0,10,11],      ['#','13']),                 # R b2 2           [0 1 2]       R b2 7           [0 1 b]
    ####################################################################################################################################################################################################
            'R b2 2 m3'        : (3, [0,1,2,3],      ['m','b2','2']),             # R b2 2 7         [0 1 2 b]     R b2 b7 7        [0 1 a b]     R 6 b7 7         [0 9 a b]
            'R b2 2 M3'        : (3, [0,1,2,4],      ['b2','2','x']),             # R b2 m3 7        [0 1 3 b]     R 2 b7 7         [0 2 a b]     R #5 6 b7        [0 8 9 a]
            'R b2 2 4'         : (2, [0,1,2,5],      ['b2','s2','s4','x']),       # R b2 M3 7        [0 1 4 b]     R m3 b7 7        [0 3 a b]     R 5 #5 6         [0 7 8 9]
            'R b2 2 b5'        : (3, [0,1,2,6],      ['o','b2','s2']),            # R b2 4 7         [0 1 5 b]     R M3 b7 7        [0 4 a b]     R b5 5 #5        [0 6 7 8]
            'R b2 2 5'         : (2, [0,1,2,7],      ['b2','s2']),                # R b2 b5 7        [0 1 6 b]     R 4 b7 7         [0 5 a b]     R 4 b5 5         [0 5 6 7]
            'R b2 2 #5'        : (3, [0,1,2,8],      ['+','b2','s2']),            # R b2 5 7         [0 1 7 b]     R b5 b7 7        [0 6 a b]     R M3 4 b5        [0 4 5 6]
            'R b2 2 6'         : (3, [0,1,2,9],      ['b2','6','s2']),            # R b2 #5 7        [0 1 8 b]     R 5 b7 7         [0 7 a b]     R m3 M3 4        [0 3 4 5]
            'R b2 2 b7'        : (0, [0,1,2,10],     ['b9','s2']),                # R b2 6 7         [0 1 9 b]     R #5 b7 7        [0 8 a b]     R 2 m3 M3        [0 2 3 4]
            'R b2 2 7'         : (0, [0,1,2,11],     ['M','b9','s2','x']),        # R b2 b7 7        [0 1 a b]     R 6 b7 7         [0 9 a b]     R b2 2 m3        [0 1 2 3]
            'R b2 m3 M3'       : (3, [0,1,3,4],      ['b2','#2','x']),            # R 2 m3 7         [0 2 3 b]     R b2 6 b7        [0 1 9 a]     R #5 6 7         [0 8 9 b]
            'R b2 m3 4'        : (3, [0,1,3,5],      ['m','b2','4']),             # R 2 M3 7         [0 2 4 b]     R 2 6 b7         [0 2 9 a]     R 5 #5 b7        [0 7 8 a]
            'R b2 m3 b5'       : (2, [0,1,3,6],      ['o','b2']),                 # R 2 4 7          [0 2 5 b]     R m3 6 b7        [0 3 9 a]     R b5 5 6         [0 6 7 9]
            'R b2 m3 5'        : (3, [0,1,3,7],      ['m','b2']),                 # R 2 b5 7         [0 2 6 b]     R M3 6 b7        [0 4 9 a]     R 4 b5 #5        [0 5 6 8]
            'R b2 m3 #5'       : (3, [0,1,3,8],      ['m','+','b2']),             # R 2 5 7          [0 2 7 b]     R 4 6 b7         [0 5 9 a]     R M3 4 5         [0 4 5 7]
            'R b2 m3 6'        : (0, [0,1,3,9],      ['m','b2','6','x']),         # R 2 #5 7         [0 2 8 b]     R b5 6 b7        [0 6 9 a]     R m3 M3 b5       [0 3 4 6]
            'R b2 m3 b7'       : (1, [0,1,3,10],     ['m','b9','x']),             # R 2 6 7          [0 2 9 b]     R 5 6 b7         [0 7 9 a]     R 2 m3 4         [0 2 3 5]
            'R b2 m3 7'        : (0, [0,1,3,11],     ['m','M','b9','x']),         # R 2 b7 7         [0 2 a b]     R #5 6 b7        [0 8 9 a]     R b2 2 M3        [0 1 2 4]
            'R b2 M3 4'        : (2, [0,1,4,5],      ['b2','4','x']),             # R m3 M3 7        [0 3 4 b]     R b2 #5 6        [0 1 8 9]     R 5 #5 7         [0 7 8 b]
            'R b2 M3 b5'       : (2, [0,1,4,6],      ['b2','b5']),                # R m3 4 7         [0 3 5 b]     R 2 #5 6         [0 2 8 9]     R b5 5 b7        [0 6 7 a]
            'R b2 M3 5'        : (1, [0,1,4,7],      ['b2']),                     # R m3 b5 7        [0 3 6 b]     R m3 #5 6        [0 3 8 9]     R 4 b5 6         [0 5 6 9]
            'R b2 M3 #5'       : (3, [0,1,4,8],      ['+','b2']),                 # R m3 5 7         [0 3 7 b]     R M3 #5 6        [0 4 8 9]     R M3 4 #5        [0 4 5 8]
            'R b2 M3 6'        : (2, [0,1,4,9],      ['b2','6']),                 # R m3 #5 7        [0 3 8 b]     R 4 #5 6         [0 5 8 9]     R m3 M3 5        [0 3 4 7]
            'R b2 M3 b7'       : (1, [0,1,4,10],     ['b9','x']),                 # R m3 6 7         [0 3 9 b]     R b5 #5 6        [0 6 8 9]     R 2 m3 b5        [0 2 3 6]
            'R b2 M3 7'        : (0, [0,1,4,11],     ['M','b9','x']),             # R m3 b7 7        [0 3 a b]     R 5 #5 6         [0 7 8 9]     R b2 2 4         [0 1 2 5]
            'R b2 4 b5'        : (2, [0,1,5,6],      ['o','b2','s4']),            # R M3 4 7         [0 4 5 b]     R b2 5 #5        [0 1 7 8]     R b5 5 7         [0 6 7 b]
            'R b2 4 5'         : (2, [0,1,5,7],      ['b2','s4']),                # R M3 b5 7        [0 4 6 b]     R 2 5 #5         [0 2 7 8]     R 4 b5 b7        [0 5 6 a]
            'R b2 4 #5'        : (2, [0,1,5,8],      ['+','b2','s4']),            # R M3 5 7         [0 4 7 b]     R m3 5 #5        [0 3 7 8]     R M3 4 6         [0 4 5 9]
            'R b2 4 6'         : (3, [0,1,5,9],      ['b2','6','s4','x']),        # R M3 #5 7        [0 4 8 b]     R M3 5 #5        [0 4 7 8]     R m3 M3 #5       [0 3 4 8]
            'R b2 4 b7'        : (2, [0,1,5,10],     ['b9','s4','x']),            # R M3 6 7         [0 4 9 b]     R 4 5 #5         [0 5 7 8]     R 2 m3 5         [0 2 3 7]
            'R b2 4 7'         : (0, [0,1,5,11],     ['M','b9','s4','x']),        # R M3 b7 7        [0 4 a b]     R b5 5 #5        [0 6 7 8]     R b2 2 b5        [0 1 2 6]
            'R b2 b5 5'        : (1, [0,1,6,7],      ['b2','#4','y']),            # R 4 b5 7         [0 5 6 b]     R b2 b5 5        @0 1 6 7@     R 4 b5 7         @0 5 6 b@
            'R b2 b5 #5'       : (3, [0,1,6,8],      ['o','+','b2','y']),         # R 4 5 7          [0 5 7 b]     R 2 b5 5         [0 2 6 7]     R M3 4 b7        [0 4 5 a]
            'R b2 b5 6'        : (3, [0,1,6,9],      ['o','b2','6','y']),         # R 4 #5 7         [0 5 8 b]     R m3 b5 5        [0 3 6 7]     R m3 M3 6        [0 3 4 9]
            'R b2 b5 b7'       : (1, [0,1,6,10],     ['o','b9','y']),             # R 4 6 7          [0 5 9 b]     R M3 b5 5        [0 4 6 7]     R 2 m3 #5        [0 2 3 8]
            'R b2 b5 7'        : (0, [0,1,6,11],     ['o','M','b9','y']),         # R 4 b7 7         [0 5 a b]     R 4 b5 5         [0 5 6 7]     R b2 2 5         [0 1 2 7]
            'R b2 5 #5'        : (3, [0,1,7,8],      ['+','b2','y']),             # R b5 5 7         [0 6 7 b]     R b2 4 b5        [0 1 5 6]     R M3 4 7         [0 4 5 b]
            'R b2 5 6'         : (3, [0,1,7,9],      ['b2','6','y']),             # R b5 #5 7        [0 6 8 b]     R 2 4 b5         [0 2 5 6]     R m3 M3 b7       [0 3 4 a]
            'R b2 5 b7'        : (0, [0,1,7,10],     ['b9','y']),                 # R b5 6 7         [0 6 9 b]     R m3 4 b5        [0 3 5 6]     R 2 m3 6         [0 2 3 9]
            'R b2 5 7'         : (0, [0,1,7,11],     ['M','b9','y']),             # R b5 b7 7        [0 6 a b]     R M3 4 b5        [0 4 5 6]     R b2 2 #5        [0 1 2 8]
            'R b2 #5 6'        : (3, [0,1,8,9],      ['+','b2','6','y']),         # R 5 #5 7         [0 7 8 b]     R b2 M3 4        [0 1 4 5]     R m3 M3 7        [0 3 4 b]
            'R b2 #5 b7'       : (2, [0,1,8,10],     ['b','13','b9','y','x']),    # R 5 6 7          [0 7 9 b]     R 2 M3 4         [0 2 4 5]     R 2 m3 b7        [0 2 3 a]
            'R b2 #5 7'        : (0, [0,1,8,11],     ['+','M','b9','y']),         # R 5 b7 7         [0 7 a b]     R m3 M3 4        [0 3 4 5]     R b2 2 6         [0 1 2 9]
            'R b2 6 b7'        : (0, [0,1,9,10],     ['13','b9','y','x']),        # R #5 6 7         [0 8 9 b]     R b2 m3 M3       [0 1 3 4]     R 2 m3 7         [0 2 3 b]
            'R b2 6 7'         : (1, [0,1,9,11],     ['M','13','b9','y','x']),    # R #5 b7 7        [0 8 a b]     R 2 m3 M3        [0 2 3 4]     R b2 2 b7        [0 1 2 a]
            'R b2 b7 7'        : (1, [0,1,10,11],    ['#','13','b9','y','x']),    # R 6 b7 7         [0 9 a b]     R b2 2 m3        [0 1 2 3]     R b2 2 7         [0 1 2 b]
            'R 2 m3 M3'        : (3, [0,2,3,4],      ['2','#2','x']),             # R b2 2 b7        [0 1 2 a]     R b2 6 7         [0 1 9 b]     R #5 b7 7        [0 8 a b]
            'R 2 m3 4'         : (3, [0,2,3,5],      ['m','2','4','x']),          # R b2 m3 b7       [0 1 3 a]     R 2 6 7          [0 2 9 b]     R 5 6 b7         [0 7 9 a]
            'R 2 m3 b5'        : (2, [0,2,3,6],      ['o','2']),                  # R b2 M3 b7       [0 1 4 a]     R m3 6 7         [0 3 9 b]     R b5 #5 6        [0 6 8 9]
            'R 2 m3 5'         : (1, [0,2,3,7],      ['m','2']),                  # R b2 4 b7        [0 1 5 a]     R M3 6 7         [0 4 9 b]     R 4 5 #5         [0 5 7 8]
            'R 2 m3 #5'        : (3, [0,2,3,8],      ['m','2','#5']),             # R b2 b5 b7       [0 1 6 a]     R 4 6 7          [0 5 9 b]     R M3 b5 5        [0 4 6 7]
            'R 2 m3 6'         : (2, [0,2,3,9],      ['m','2','6','x']),          # R b2 5 b7        [0 1 7 a]     R b5 6 7         [0 6 9 b]     R m3 4 b5        [0 3 5 6]
            'R 2 m3 b7'        : (0, [0,2,3,10],     ['m','9','x']),              # R b2 #5 b7       [0 1 8 a]     R 5 6 7          [0 7 9 b]     R 2 M3 4         [0 2 4 5]
            'R 2 m3 7'         : (1, [0,2,3,11],     ['m','M','9','x']),          # R b2 6 b7        [0 1 9 a]     R #5 6 7         [0 8 9 b]     R b2 m3 M3       [0 1 3 4]
            'R 2 M3 4'         : (3, [0,2,4,5],      ['2','4','x']),              # R 2 m3 b7        [0 2 3 a]     R b2 #5 b7       [0 1 8 a]     R 5 6 7          [0 7 9 b]
            'R 2 M3 b5'        : (3, [0,2,4,6],      ['2','b5']),                 # R 2 M3 b7        [0 2 4 a]     R 2 #5 b7        [0 2 8 a]     R b5 #5 b7       [0 6 8 a]
            'R 2 M3 5'         : (0, [0,2,4,7],      ['2']),                      # R 2 4 b7         [0 2 5 a]     R m3 #5 b7       [0 3 8 a]     R 4 5 6          [0 5 7 9]
            'R 2 M3 #5'        : (2, [0,2,4,8],      ['+','2']),                  # R 2 b5 b7        [0 2 6 a]     R M3 #5 b7       [0 4 8 a]     R M3 b5 #5       [0 4 6 8]
            'R 2 M3 6'         : (0, [0,2,4,9],      ['2','6','x']),              # R 2 5 b7         [0 2 7 a]     R 4 #5 b7        [0 5 8 a]     R m3 4 5         [0 3 5 7]
            'R 2 M3 b7'        : (0, [0,2,4,10],     ['9','x']),                  # R 2 #5 b7        [0 2 8 a]     R b5 #5 b7       [0 6 8 a]     R 2 M3 b5        [0 2 4 6]
            'R 2 M3 7'         : (0, [0,2,4,11],     ['M','9','x']),              # R 2 6 b7         [0 2 9 a]     R 5 #5 b7        [0 7 8 a]     R b2 m3 4        [0 1 3 5]
            'R 2 4 b5'         : (2, [0,2,5,6],      ['o','s2','s4']),            # R m3 M3 b7       [0 3 4 a]     R b2 5 6         [0 1 7 9]     R b5 #5 7        [0 6 8 b]
            'R 2 4 5'          : (3, [0,2,5,7],      ['s2','s4']),                # R m3 4 b7        [0 3 5 a]     R 2 5 6          [0 2 7 9]     R 4 5 b7         [0 5 7 a]
            'R 2 4 #5'         : (2, [0,2,5,8],      ['+','s2','s4']),            # R m3 b5 b7       [0 3 6 a]     R m3 5 6         [0 3 7 9]     R M3 b5 6        [0 4 6 9]
            'R 2 4 6'          : (3, [0,2,5,9],      ['6','s2','s4','x']),        # R m3 5 b7        [0 3 7 a]     R M3 5 6         [0 4 7 9]     R m3 4 #5        [0 3 5 8]
            'R 2 4 b7'         : (2, [0,2,5,10],     ['7','s2','s4','x']),        # R m3 #5 b7       [0 3 8 a]     R 4 5 6          [0 5 7 9]     R 2 M3 5         [0 2 4 7]
            'R 2 4 7'          : (1, [0,2,5,11],     ['M','7','s2','s4','x']),    # R m3 6 b7        [0 3 9 a]     R b5 5 6         [0 6 7 9]     R b2 m3 b5       [0 1 3 6]
            'R 2 b5 5'         : (2, [0,2,6,7],      ['s2','#4']),                # R M3 4 b7        [0 4 5 a]     R b2 b5 #5       [0 1 6 8]     R 4 5 7          [0 5 7 b]
            'R 2 b5 #5'        : (1, [0,2,6,8],      ['o','+','s2']),             # R M3 b5 b7       [0 4 6 a]     R 2 b5 #5        @0 2 6 8@     R M3 b5 b7       @0 4 6 a@
            'R 2 b5 6'         : (3, [0,2,6,9],      ['o','6','s2']),             # R M3 5 b7        [0 4 7 a]     R m3 b5 #5       [0 3 6 8]     R m3 4 6         [0 3 5 9]
            'R 2 b5 b7'        : (1, [0,2,6,10],     ['0','7','s2']),             # R M3 #5 b7       [0 4 8 a]     R M3 b5 #5       [0 4 6 8]     R 2 M3 #5        [0 2 4 8]
            'R 2 b5 7'         : (1, [0,2,6,11],     ['M','b','13','s2']),        # R M3 6 b7        [0 4 9 a]     R 4 b5 #5        [0 5 6 8]     R b2 m3 5        [0 1 3 7]
            'R 2 5 #5'         : (3, [0,2,7,8],      ['b6','s2']),                # R 4 b5 b7        [0 5 6 a]     R b2 4 5         [0 1 5 7]     R M3 b5 7        [0 4 6 b]
            'R 2 5 6'          : (2, [0,2,7,9],      ['6','s2']),                 # R 4 5 b7         [0 5 7 a]     R 2 4 5          [0 2 5 7]     R m3 4 b7        [0 3 5 a]
            'R 2 5 b7'         : (1, [0,2,7,10],     ['7','s2']),                 # R 4 #5 b7        [0 5 8 a]     R m3 4 5         [0 3 5 7]     R 2 M3 6         [0 2 4 9]
            'R 2 5 7'          : (1, [0,2,7,11],     ['M','7','s2']),             # R 4 6 b7         [0 5 9 a]     R M3 4 5         [0 4 5 7]     R b2 m3 #5       [0 1 3 8]
            'R 2 #5 6'         : (3, [0,2,8,9],      ['+','6','s2']),             # R b5 5 b7        [0 6 7 a]     R b2 M3 b5       [0 1 4 6]     R m3 4 7         [0 3 5 b]
            'R 2 #5 b7'        : (2, [0,2,8,10],     ['b','13','s2','x']),        # R b5 #5 b7       [0 6 8 a]     R 2 M3 b5        [0 2 4 6]     R 2 M3 b7        [0 2 4 a]
            'R 2 #5 7'         : (3, [0,2,8,11],     ['M','b','13','s2','x']),    # R b5 6 b7        [0 6 9 a]     R m3 M3 b5       [0 3 4 6]     R b2 m3 6        [0 1 3 9]
            'R 2 6 b7'         : (1, [0,2,9,10],     ['13','s2','x']),            # R 5 #5 b7        [0 7 8 a]     R b2 m3 4        [0 1 3 5]     R 2 M3 7         [0 2 4 b]
            'R 2 6 7'          : (2, [0,2,9,11],     ['M','13','s2','x']),        # R 5 6 b7         [0 7 9 a]     R 2 m3 4         [0 2 3 5]     R b2 m3 b7       [0 1 3 a]
            'R 2 b7 7'         : (2, [0,2,10,11],    ['#','13','s2','x']),        # R #5 6 b7        [0 8 9 a]     R b2 2 M3        [0 1 2 4]     R b2 m3 7        [0 1 3 b]
            'R m3 M3 4'        : (2, [0,3,4,5],      ['#2','4']),                 # R b2 2 6         [0 1 2 9]     R b2 #5 7        [0 1 8 b]     R 5 b7 7         [0 7 a b]
            'R m3 M3 b5'       : (1, [0,3,4,6],      ['#2','b5']),                # R b2 m3 6        [0 1 3 9]     R 2 #5 7         [0 2 8 b]     R b5 6 b7        [0 6 9 a]
            'R m3 M3 5'        : (1, [0,3,4,7],      ['#2']),                     # R b2 M3 6        [0 1 4 9]     R m3 #5 7        [0 3 8 b]     R 4 #5 6         [0 5 8 9]
            'R m3 M3 #5'       : (2, [0,3,4,8],      ['+','#2']),                 # R b2 4 6         [0 1 5 9]     R M3 #5 7        [0 4 8 b]     R M3 5 #5        [0 4 7 8]
            'R m3 M3 6'        : (2, [0,3,4,9],      ['#2','6','x']),             # R b2 b5 6        [0 1 6 9]     R 4 #5 7         [0 5 8 b]     R m3 b5 5        [0 3 6 7]
            'R m3 M3 b7'       : (0, [0,3,4,10],     ['#9','x']),                 # R b2 5 6         [0 1 7 9]     R b5 #5 7        [0 6 8 b]     R 2 4 b5         [0 2 5 6]
            'R m3 M3 7'        : (0, [0,3,4,11],     ['M','#9','x']),             # R b2 #5 6        [0 1 8 9]     R 5 #5 7         [0 7 8 b]     R b2 M3 4        [0 1 4 5]
            'R m3 4 b5'        : (3, [0,3,5,6],      ['o','4']),                  # R 2 m3 6         [0 2 3 9]     R b2 5 b7        [0 1 7 a]     R b5 6 7         [0 6 9 b]
            'R m3 4 5'         : (3, [0,3,5,7],      ['m','4']),                  # R 2 M3 6         [0 2 4 9]     R 2 5 b7         [0 2 7 a]     R 4 #5 b7        [0 5 8 a]
            'R m3 4 #5'        : (2, [0,3,5,8],      ['m','+','4']),              # R 2 4 6          [0 2 5 9]     R m3 5 b7        [0 3 7 a]     R M3 5 6         [0 4 7 9]
            'R m3 4 6'         : (1, [0,3,5,9],      ['m','4','6','x']),          # R 2 b5 6         [0 2 6 9]     R M3 5 b7        [0 4 7 a]     R m3 b5 #5       [0 3 6 8]
            'R m3 4 b7'        : (0, [0,3,5,10],     ['m','11','x']),             # R 2 5 6          [0 2 7 9]     R 4 5 b7         [0 5 7 a]     R 2 4 5          [0 2 5 7]
            'R m3 4 7'         : (1, [0,3,5,11],     ['m','M','11','x']),         # R 2 #5 6         [0 2 8 9]     R b5 5 b7        [0 6 7 a]     R b2 M3 b5       [0 1 4 6]
            'R m3 b5 5'        : (1, [0,3,6,7],      ['m','#4']),                 # R m3 M3 6        [0 3 4 9]     R b2 b5 6        [0 1 6 9]     R 4 #5 7         [0 5 8 b]
            'R m3 b5 #5'       : (2, [0,3,6,8],      ['o','+']),                  # R m3 4 6         [0 3 5 9]     R 2 b5 6         [0 2 6 9]     R M3 5 b7        [0 4 7 a]
            'R m3 b5 6'        : (0, [0,3,6,9],      ['o','7']),                  # R m3 b5 6        @0 3 6 9@     R m3 b5 6        @0 3 6 9@     R m3 b5 6        @0 3 6 9@
            'R m3 b5 b7'       : (0, [0,3,6,10],     ['0','7']),                  # R m3 5 6         [0 3 7 9]     R M3 b5 6        [0 4 6 9]     R 2 4 #5         [0 2 5 8]
            'R m3 b5 7'        : (0, [0,3,6,11],     ['o','M','7']),              # R m3 #5 6        [0 3 8 9]     R 4 b5 6         [0 5 6 9]     R b2 M3 5        [0 1 4 7]
            'R m3 5 #5'        : (3, [0,3,7,8],      ['m','b6']),                 # R M3 4 6         [0 4 5 9]     R b2 4 #5        [0 1 5 8]     R M3 5 7         [0 4 7 b]
            'R m3 5 6'         : (1, [0,3,7,9],      ['m','6']),                  # R M3 b5 6        [0 4 6 9]     R 2 4 #5         [0 2 5 8]     R m3 b5 b7       [0 3 6 a]
            'R m3 5 b7'        : (0, [0,3,7,10],     ['m','7']),                  # R M3 5 6         [0 4 7 9]     R m3 4 #5        [0 3 5 8]     R 2 4 6          [0 2 5 9]
            'R m3 5 7'         : (0, [0,3,7,11],     ['m','M','7']),              # R M3 #5 6        [0 4 8 9]     R M3 4 #5        [0 4 5 8]     R b2 M3 #5       [0 1 4 8]
            'R m3 #5 6'        : (3, [0,3,8,9],      ['m','+','6']),              # R 4 b5 6         [0 5 6 9]     R b2 M3 5        [0 1 4 7]     R m3 b5 7        [0 3 6 b]
            'R m3 #5 b7'       : (1, [0,3,8,10],     ['m','b','13','x']),         # R 4 5 6          [0 5 7 9]     R 2 M3 5         [0 2 4 7]     R 2 4 b7         [0 2 5 a]
            'R m3 #5 7'        : (0, [0,3,8,11],     ['m','M','+','7']),          # R 4 #5 6         [0 5 8 9]     R m3 M3 5        [0 3 4 7]     R b2 M3 6        [0 1 4 9]
            'R m3 6 b7'        : (0, [0,3,9,10],     ['m','13','x']),             # R b5 5 6         [0 6 7 9]     R b2 m3 b5       [0 1 3 6]     R 2 4 7          [0 2 5 b]
            'R m3 6 7'         : (0, [0,3,9,11],     ['m','M','13','x']),         # R b5 #5 6        [0 6 8 9]     R 2 m3 b5        [0 2 3 6]     R b2 M3 b7       [0 1 4 a]
            'R m3 b7 7'        : (1, [0,3,10,11],    ['m','#','13','x']),         # R 5 #5 6         [0 7 8 9]     R b2 2 4         [0 1 2 5]     R b2 M3 7        [0 1 4 b]
            'R M3 4 b5'        : (2, [0,4,5,6],      ['b5','4']),                 # R b2 2 #5        [0 1 2 8]     R b2 5 7         [0 1 7 b]     R b5 b7 7        [0 6 a b]
            'R M3 4 5'         : (0, [0,4,5,7],      ['4']),                      # R b2 m3 #5       [0 1 3 8]     R 2 5 7          [0 2 7 b]     R 4 6 b7         [0 5 9 a]
            'R M3 4 #5'        : (1, [0,4,5,8],      ['+','4']),                  # R b2 M3 #5       [0 1 4 8]     R m3 5 7         [0 3 7 b]     R M3 #5 6        [0 4 8 9]
            'R M3 4 6'         : (1, [0,4,5,9],      ['4','6','x']),              # R b2 4 #5        [0 1 5 8]     R M3 5 7         [0 4 7 b]     R m3 5 #5        [0 3 7 8]
            'R M3 4 b7'        : (0, [0,4,5,10],     ['11','x']),                 # R b2 b5 #5       [0 1 6 8]     R 4 5 7          [0 5 7 b]     R 2 b5 5         [0 2 6 7]
            'R M3 4 7'         : (0, [0,4,5,11],     ['M','11','x']),             # R b2 5 #5        [0 1 7 8]     R b5 5 7         [0 6 7 b]     R b2 4 b5        [0 1 5 6]
            'R M3 b5 5'        : (2, [0,4,6,7],      ['#4']),                     # R 2 m3 #5        [0 2 3 8]     R b2 b5 b7       [0 1 6 a]     R 4 6 7          [0 5 9 b]
            'R M3 b5 #5'       : (3, [0,4,6,8],      ['+','#4']),                 # R 2 M3 #5        [0 2 4 8]     R 2 b5 b7        [0 2 6 a]     R M3 #5 b7       [0 4 8 a]
            'R M3 b5 6'        : (3, [0,4,6,9],      ['b5','6']),                 # R 2 4 #5         [0 2 5 8]     R m3 b5 b7       [0 3 6 a]     R m3 5 6         [0 3 7 9]
            'R M3 b5 b7'       : (0, [0,4,6,10],     ['#','11','x']),             # R 2 b5 #5        [0 2 6 8]     R M3 b5 b7       @0 4 6 a@     R 2 b5 #5        @0 2 6 8@
            'R M3 b5 7'        : (0, [0,4,6,11],     ['M','7','b5']),             # R 2 5 #5         [0 2 7 8]     R 4 b5 b7        [0 5 6 a]     R b2 4 5         [0 1 5 7]
            'R M3 5 #5'        : (1, [0,4,7,8],      ['b6']),                     # R m3 M3 #5       [0 3 4 8]     R b2 4 6         [0 1 5 9]     R M3 #5 7        [0 4 8 b]
            'R M3 5 6'         : (1, [0,4,7,9],      ['6']),                      # R m3 4 #5        [0 3 5 8]     R 2 4 6          [0 2 5 9]     R m3 5 b7        [0 3 7 a]
            'R M3 5 b7'        : (0, [0,4,7,10],     ['7']),                      # R m3 b5 #5       [0 3 6 8]     R m3 4 6         [0 3 5 9]     R 2 b5 6         [0 2 6 9]
            'R M3 5 7'         : (0, [0,4,7,11],     ['M','7']),                  # R m3 5 #5        [0 3 7 8]     R M3 4 6         [0 4 5 9]     R b2 4 #5        [0 1 5 8]
            'R M3 #5 6'        : (2, [0,4,8,9],      ['+','6']),                  # R M3 4 #5        [0 4 5 8]     R b2 M3 #5       [0 1 4 8]     R m3 5 7         [0 3 7 b]
            'R M3 #5 b7'       : (0, [0,4,8,10],     ['+','7']),                  # R M3 b5 #5       [0 4 6 8]     R 2 M3 #5        [0 2 4 8]     R 2 b5 b7        [0 2 6 a]
            'R M3 #5 7'        : (0, [0,4,8,11],     ['+','M','7']),              # R M3 5 #5        [0 4 7 8]     R m3 M3 #5       [0 3 4 8]     R b2 4 6         [0 1 5 9]
            'R M3 6 b7'        : (0, [0,4,9,10],     ['13','x']),                 # R 4 b5 #5        [0 5 6 8]     R b2 m3 5        [0 1 3 7]     R 2 b5 7         [0 2 6 b]
            'R M3 6 7'         : (0, [0,4,9,11],     ['M','13','x']),             # R 4 5 #5         [0 5 7 8]     R 2 m3 5         [0 2 3 7]     R b2 4 b7        [0 1 5 a]
            'R M3 b7 7'        : (1, [0,4,10,11],    ['#','13','x']),             # R b5 5 #5        [0 6 7 8]     R b2 2 b5        [0 1 2 6]     R b2 4 7         [0 1 5 b]
            'R 4 b5 5'         : (3, [0,5,6,7],      ['#4','s4','y']),            # R b2 2 5         [0 1 2 7]     R b2 b5 7        [0 1 6 b]     R 4 b7 7         [0 5 a b]
            'R 4 b5 #5'        : (2, [0,5,6,8],      ['o','+','s4']),             # R b2 m3 5        [0 1 3 7]     R 2 b5 7         [0 2 6 b]     R M3 6 b7        [0 4 9 a]
            'R 4 b5 6'         : (2, [0,5,6,9],      ['o','6','s4']),             # R b2 M3 5        [0 1 4 7]     R m3 b5 7        [0 3 6 b]     R m3 #5 6        [0 3 8 9]
            'R 4 b5 b7'        : (1, [0,5,6,10],     ['o','7','s4']),             # R b2 4 5         [0 1 5 7]     R M3 b5 7        [0 4 6 b]     R 2 5 #5         [0 2 7 8]
            'R 4 b5 7'         : (0, [0,5,6,11],     ['o','M','7','s4']),         # R b2 b5 5        [0 1 6 7]     R 4 b5 7         @0 5 6 b@     R b2 b5 5        @0 1 6 7@
            'R 4 5 #5'         : (3, [0,5,7,8],      ['b6','s4']),                # R 2 m3 5         [0 2 3 7]     R b2 4 b7        [0 1 5 a]     R M3 6 7         [0 4 9 b]
            'R 4 5 6'          : (3, [0,5,7,9],      ['6','s4']),                 # R 2 M3 5         [0 2 4 7]     R 2 4 b7         [0 2 5 a]     R m3 #5 b7       [0 3 8 a]
            'R 4 5 b7'         : (1, [0,5,7,10],     ['7','s4']),                 # R 2 4 5          [0 2 5 7]     R m3 4 b7        [0 3 5 a]     R 2 5 6          [0 2 7 9]
            'R 4 5 7'          : (1, [0,5,7,11],     ['M','7','s4']),             # R 2 b5 5         [0 2 6 7]     R M3 4 b7        [0 4 5 a]     R b2 b5 #5       [0 1 6 8]
            'R 4 #5 6'         : (3, [0,5,8,9],      ['+','6','s4']),             # R m3 M3 5        [0 3 4 7]     R b2 M3 6        [0 1 4 9]     R m3 #5 7        [0 3 8 b]
            'R 4 #5 b7'        : (2, [0,5,8,10],     ['+','7','s4']),             # R m3 4 5         [0 3 5 7]     R 2 M3 6         [0 2 4 9]     R 2 5 b7         [0 2 7 a]
            'R 4 #5 7'         : (0, [0,5,8,11],     ['+','M','7','s4']),         # R m3 b5 5        [0 3 6 7]     R m3 M3 6        [0 3 4 9]     R b2 b5 6        [0 1 6 9]
            'R 4 6 b7'         : (2, [0,5,9,10],     ['13','s4','x']),            # R M3 4 5         [0 4 5 7]     R b2 m3 #5       [0 1 3 8]     R 2 5 7          [0 2 7 b]
            'R 4 6 7'          : (0, [0,5,9,11],     ['M','13','s4','x']),        # R M3 b5 5        [0 4 6 7]     R 2 m3 #5        [0 2 3 8]     R b2 b5 b7       [0 1 6 a]
            'R 4 b7 7'         : (1, [0,5,10,11],    ['#','13','s4','x']),        # R 4 b5 5         [0 5 6 7]     R b2 2 5         [0 1 2 7]     R b2 b5 7        [0 1 6 b]
            'R b5 5 #5'        : (2, [0,6,7,8],      ['#4','b6','y']),            # R b2 2 b5        [0 1 2 6]     R b2 4 7         [0 1 5 b]     R M3 b7 7        [0 4 a b]
            'R b5 5 6'         : (3, [0,6,7,9],      ['#4','6','y']),             # R b2 m3 b5       [0 1 3 6]     R 2 4 7          [0 2 5 b]     R m3 6 b7        [0 3 9 a]
            'R b5 5 b7'        : (0, [0,6,7,10],     ['#','11','y']),             # R b2 M3 b5       [0 1 4 6]     R m3 4 7         [0 3 5 b]     R 2 #5 6         [0 2 8 9]
            'R b5 5 7'         : (1, [0,6,7,11],     ['M','#','11','y']),         # R b2 4 b5        [0 1 5 6]     R M3 4 7         [0 4 5 b]     R b2 5 #5        [0 1 7 8]
            'R b5 #5 6'        : (3, [0,6,8,9],      ['o','+','6','y']),          # R 2 m3 b5        [0 2 3 6]     R b2 M3 b7       [0 1 4 a]     R m3 6 7         [0 3 9 b]
            'R b5 #5 b7'       : (1, [0,6,8,10],     ['o','+','7','y']),          # R 2 M3 b5        [0 2 4 6]     R 2 M3 b7        [0 2 4 a]     R 2 #5 b7        [0 2 8 a]
            'R b5 #5 7'        : (1, [0,6,8,11],     ['M','o','+','7','y']),      # R 2 4 b5         [0 2 5 6]     R m3 M3 b7       [0 3 4 a]     R b2 5 6         [0 1 7 9]
            'R b5 6 b7'        : (2, [0,6,9,10],     ['o','13','y']),             # R m3 M3 b5       [0 3 4 6]     R b2 m3 6        [0 1 3 9]     R 2 #5 7         [0 2 8 b]
            'R b5 6 7'         : (1, [0,6,9,11],     ['M','o','13','y']),         # R m3 4 b5        [0 3 5 6]     R 2 m3 6         [0 2 3 9]     R b2 5 b7        [0 1 7 a]
            'R b5 b7 7'        : (1, [0,6,10,11],    ['o','#','13']),             # R M3 4 b5        [0 4 5 6]     R b2 2 #5        [0 1 2 8]     R b2 5 7         [0 1 7 b]
            'R 5 #5 6'         : (3, [0,7,8,9],      ['+','6','y','+x']),         # R b2 2 4         [0 1 2 5]     R b2 M3 7        [0 1 4 b]     R m3 b7 7        [0 3 a b]
            'R 5 #5 b7'        : (2, [0,7,8,10],     ['b','13','y']),             # R b2 m3 4        [0 1 3 5]     R 2 M3 7         [0 2 4 b]     R 2 6 b7         [0 2 9 a]
            'R 5 #5 7'         : (1, [0,7,8,11],     ['M','b','13','y']),         # R b2 M3 4        [0 1 4 5]     R m3 M3 7        [0 3 4 b]     R b2 #5 6        [0 1 8 9]
            'R 5 6 b7'         : (0, [0,7,9,10],     ['13','y']),                 # R 2 m3 4         [0 2 3 5]     R b2 m3 b7       [0 1 3 a]     R 2 6 7          [0 2 9 b]
            'R 5 6 7'          : (1, [0,7,9,11],     ['M','13','y']),             # R 2 M3 4         [0 2 4 5]     R 2 m3 b7        [0 2 3 a]     R b2 #5 b7       [0 1 8 a]
            'R 5 b7 7'         : (1, [0,7,10,11],    ['#','13','y']),             # R m3 M3 4        [0 3 4 5]     R b2 2 6         [0 1 2 9]     R b2 #5 7        [0 1 8 b]
            'R #5 6 b7'        : (1, [0,8,9,10],     ['+','13','y']),             # R b2 2 M3        [0 1 2 4]     R b2 m3 7        [0 1 3 b]     R 2 b7 7         [0 2 a b]
            'R #5 6 7'         : (2, [0,8,9,11],     ['+','M','13','y']),         # R b2 m3 M3       [0 1 3 4]     R 2 m3 7         [0 2 3 b]     R b2 6 b7        [0 1 9 a]
            'R #5 b7 7'        : (2, [0,8,10,11],    ['+','#','13','y']),         # R 2 m3 M3        [0 2 3 4]     R b2 2 b7        [0 1 2 a]     R b2 6 7         [0 1 9 b]
            'R 6 b7 7'         : (2, [0,9,10,11],    ['#','13','6','xy']),        # R b2 2 m3        [0 1 2 3]     R b2 2 7         [0 1 2 b]     R b2 b7 7        [0 1 a b]
    ####################################################################################################################################################################################################
            'R b2 2 m3 M3'     : (4, [0,1,2,3,4],    ['b2','2','#2','x']),        # R b2 2 m3 7      [0 1 2 3 b]   R b2 2 b7 7      [0 1 2 a b]   R b2 6 b7 7      [0 1 9 a b]   R #5 6 b7 7      [0 8 9 a b]
            'R b2 2 m3 4'      : (4, [0,1,2,3,5],    ['m','b2','2','4','x']),     # R b2 2 M3 7      [0 1 2 4 b]   R b2 m3 b7 7     [0 1 3 a b]   R 2 6 b7 7       [0 2 9 a b]   R 5 #5 6 b7      [0 7 8 9 a]
            'R b2 2 m3 b5'     : (3, [0,1,2,3,6],    ['o','b2','2']),             # R b2 2 4 7       [0 1 2 5 b]   R b2 M3 b7 7     [0 1 4 a b]   R m3 6 b7 7      [0 3 9 a b]   R b5 5 #5 6      [0 6 7 8 9]
            'R b2 2 m3 5'      : (4, [0,1,2,3,7],    ['m','b2','2']),             # R b2 2 b5 7      [0 1 2 6 b]   R b2 4 b7 7      [0 1 5 a b]   R M3 6 b7 7      [0 4 9 a b]   R 4 b5 5 #5      [0 5 6 7 8]
            'R b2 2 m3 #5'     : (4, [0,1,2,3,8],    ['m','+','b2','2']),         # R b2 2 5 7       [0 1 2 7 b]   R b2 b5 b7 7     [0 1 6 a b]   R 4 6 b7 7       [0 5 9 a b]   R M3 4 b5 5      [0 4 5 6 7]
            'R b2 2 m3 6'      : (4, [0,1,2,3,9],    ['m','b2','2','6','x']),     # R b2 2 #5 7      [0 1 2 8 b]   R b2 5 b7 7      [0 1 7 a b]   R b5 6 b7 7      [0 6 9 a b]   R m3 M3 4 b5     [0 3 4 5 6]
            'R b2 2 m3 b7'     : (0, [0,1,2,3,10],   ['m','b9','x']),             # R b2 2 6 7       [0 1 2 9 b]   R b2 #5 b7 7     [0 1 8 a b]   R 5 6 b7 7       [0 7 9 a b]   R 2 m3 M3 4      [0 2 3 4 5]
            'R b2 2 m3 7'      : (1, [0,1,2,3,11],   ['m','M','b9','9','x']),     # R b2 2 b7 7      [0 1 2 a b]   R b2 6 b7 7      [0 1 9 a b]   R #5 6 b7 7      [0 8 9 a b]   R b2 2 m3 M3     [0 1 2 3 4]
            'R b2 2 M3 4'      : (4, [0,1,2,4,5],    ['b2','s2','s4']),           # R b2 m3 M3 7     [0 1 3 4 b]   R 2 m3 b7 7      [0 2 3 a b]   R b2 #5 6 b7     [0 1 8 9 a]   R 5 #5 6 7       [0 7 8 9 b]
            'R b2 2 M3 b5'     : (4, [0,1,2,4,6],    ['o','b2','2']),             # R b2 m3 4 7      [0 1 3 5 b]   R 2 M3 b7 7      [0 2 4 a b]   R 2 #5 6 b7      [0 2 8 9 a]   R b5 5 #5 b7     [0 6 7 8 a]
            'R b2 2 M3 5'      : (4, [0,1,2,4,7],    ['b2','2']),                 # R b2 m3 b5 7     [0 1 3 6 b]   R 2 4 b7 7       [0 2 5 a b]   R m3 #5 6 b7     [0 3 8 9 a]   R 4 b5 5 6       [0 5 6 7 9]
            'R b2 2 M3 #5'     : (4, [0,1,2,4,8],    ['+','b2','2']),             # R b2 m3 5 7      [0 1 3 7 b]   R 2 b5 b7 7      [0 2 6 a b]   R M3 #5 6 b7     [0 4 8 9 a]   R M3 4 b5 #5     [0 4 5 6 8]
            'R b2 2 M3 6'      : (4, [0,1,2,4,9],    ['b2','2','6']),             # R b2 m3 #5 7     [0 1 3 8 b]   R 2 5 b7 7       [0 2 7 a b]   R 4 #5 6 b7      [0 5 8 9 a]   R m3 M3 4 5      [0 3 4 5 7]
            'R b2 2 M3 b7'     : (0, [0,1,2,4,10],   ['b9','9','x']),             # R b2 m3 6 7      [0 1 3 9 b]   R 2 #5 b7 7      [0 2 8 a b]   R b5 #5 6 b7     [0 6 8 9 a]   R 2 m3 M3 b5     [0 2 3 4 6]
            'R b2 2 M3 7'      : (1, [0,1,2,4,11],   ['M','b9','s2']),            # R b2 m3 b7 7     [0 1 3 a b]   R 2 6 b7 7       [0 2 9 a b]   R 5 #5 6 b7      [0 7 8 9 a]   R b2 2 m3 4      [0 1 2 3 5]
            'R b2 2 4 b5'      : (3, [0,1,2,5,6],    ['o','b2','s2','s4']),       # R b2 M3 4 7      [0 1 4 5 b]   R m3 M3 b7 7     [0 3 4 a b]   R b2 5 #5 6      [0 1 7 8 9]   R b5 5 #5 7      [0 6 7 8 b]
            'R b2 2 4 5'       : (4, [0,1,2,5,7],    ['b2','s2','s4']),           # R b2 M3 b5 7     [0 1 4 6 b]   R m3 4 b7 7      [0 3 5 a b]   R 2 5 #5 6       [0 2 7 8 9]   R 4 b5 5 b7      [0 5 6 7 a]
            'R b2 2 4 #5'      : (2, [0,1,2,5,8],    ['+','b2','s2','s4']),       # R b2 M3 5 7      [0 1 4 7 b]   R m3 b5 b7 7     [0 3 6 a b]   R m3 5 #5 6      [0 3 7 8 9]   R M3 4 b5 6      [0 4 5 6 9]
            'R b2 2 4 6'       : (4, [0,1,2,5,9],    ['b2','6','s2','s4','x']),   # R b2 M3 #5 7     [0 1 4 8 b]   R m3 5 b7 7      [0 3 7 a b]   R M3 5 #5 6      [0 4 7 8 9]   R m3 M3 4 #5     [0 3 4 5 8]
            'R b2 2 4 b7'      : (1, [0,1,2,5,10],   ['b9','s2','s4','x']),       # R b2 M3 6 7      [0 1 4 9 b]   R m3 #5 b7 7     [0 3 8 a b]   R 4 5 #5 6       [0 5 7 8 9]   R 2 m3 M3 5      [0 2 3 4 7]
            'R b2 2 4 7'       : (1, [0,1,2,5,11],   ['b9','s2','s4','x']),       # R b2 M3 b7 7     [0 1 4 a b]   R m3 6 b7 7      [0 3 9 a b]   R b5 5 #5 6      [0 6 7 8 9]   R b2 2 m3 b5     [0 1 2 3 6]
            'R b2 2 b5 5'      : (3, [0,1,2,6,7],    ['b2','#4','s2']),           # R b2 4 b5 7      [0 1 5 6 b]   R M3 4 b7 7      [0 4 5 a b]   R b2 b5 5 #5     [0 1 6 7 8]   R 4 b5 5 7       [0 5 6 7 b]
            'R b2 2 b5 #5'     : (4, [0,1,2,6,8],    ['o','+','b2','s2']),        # R b2 4 5 7       [0 1 5 7 b]   R M3 b5 b7 7     [0 4 6 a b]   R 2 b5 5 #5      [0 2 6 7 8]   R M3 4 b5 b7     [0 4 5 6 a]
            'R b2 2 b5 6'      : (4, [0,1,2,6,9],    ['o','b2','6','s2']),        # R b2 4 #5 7      [0 1 5 8 b]   R M3 5 b7 7      [0 4 7 a b]   R m3 b5 5 #5     [0 3 6 7 8]   R m3 M3 4 6      [0 3 4 5 9]
            'R b2 2 b5 b7'     : (1, [0,1,2,6,10],   ['o','b9','s2']),            # R b2 4 6 7       [0 1 5 9 b]   R M3 #5 b7 7     [0 4 8 a b]   R M3 b5 5 #5     [0 4 6 7 8]   R 2 m3 M3 #5     [0 2 3 4 8]
            'R b2 2 b5 7'      : (3, [0,1,2,6,11],   ['o','M','b9','s2']),        # R b2 4 b7 7      [0 1 5 a b]   R M3 6 b7 7      [0 4 9 a b]   R 4 b5 5 #5      [0 5 6 7 8]   R b2 2 m3 5      [0 1 2 3 7]
            'R b2 2 5 #5'      : (3, [0,1,2,7,8],    ['b2','b6','s2']),           # R b2 b5 5 7      [0 1 6 7 b]   R 4 b5 b7 7      [0 5 6 a b]   R b2 4 b5 5      [0 1 5 6 7]   R M3 4 b5 7      [0 4 5 6 b]
            'R b2 2 5 6'       : (4, [0,1,2,7,9],    ['b2','6','s2']),            # R b2 b5 #5 7     [0 1 6 8 b]   R 4 5 b7 7       [0 5 7 a b]   R 2 4 b5 5       [0 2 5 6 7]   R m3 M3 4 b7     [0 3 4 5 a]
            'R b2 2 5 b7'      : (0, [0,1,2,7,10],   ['b9','s2']),                # R b2 b5 6 7      [0 1 6 9 b]   R 4 #5 b7 7      [0 5 8 a b]   R m3 4 b5 5      [0 3 5 6 7]   R 2 m3 M3 6      [0 2 3 4 9]
            'R b2 2 5 7'       : (0, [0,1,2,7,11],   ['M','b9','s2']),            # R b2 b5 b7 7     [0 1 6 a b]   R 4 6 b7 7       [0 5 9 a b]   R M3 4 b5 5      [0 4 5 6 7]   R b2 2 m3 #5     [0 1 2 3 8]
            'R b2 2 #5 6'      : (4, [0,1,2,8,9],    ['+','b2','6','s2']),        # R b2 5 #5 7      [0 1 7 8 b]   R b5 5 b7 7      [0 6 7 a b]   R b2 M3 4 b5     [0 1 4 5 6]   R m3 M3 4 7      [0 3 4 5 b]
            'R b2 2 #5 b7'     : (0, [0,1,2,8,10],   ['+','b9','s2']),            # R b2 5 6 7       [0 1 7 9 b]   R b5 #5 b7 7     [0 6 8 a b]   R 2 M3 4 b5      [0 2 4 5 6]   R 2 m3 M3 b7     [0 2 3 4 a]
            'R b2 2 #5 7'      : (2, [0,1,2,8,11],   ['+','M','b9','s2']),        # R b2 5 b7 7      [0 1 7 a b]   R b5 6 b7 7      [0 6 9 a b]   R m3 M3 4 b5     [0 3 4 5 6]   R b2 2 m3 6      [0 1 2 3 9]
            'R b2 2 6 b7'      : (3, [0,1,2,9,10],   ['13','b9','s2','x']),       # R b2 #5 6 7      [0 1 8 9 b]   R 5 #5 b7 7      [0 7 8 a b]   R b2 m3 M3 4     [0 1 3 4 5]   R 2 m3 M3 7      [0 2 3 4 b]
            'R b2 2 6 7'       : (1, [0,1,2,9,11],   ['M','13','b9','s2']),       # R b2 #5 b7 7     [0 1 8 a b]   R 5 6 b7 7       [0 7 9 a b]   R 2 m3 M3 4      [0 2 3 4 5]   R b2 2 m3 b7     [0 1 2 3 a]
            'R b2 2 b7 7'      : (0, [0,1,2,10,11],  ['#','13','b9','s2','x']),   # R b2 6 b7 7      [0 1 9 a b]   R #5 6 b7 7      [0 8 9 a b]   R b2 2 m3 M3     [0 1 2 3 4]   R b2 2 m3 7      [0 1 2 3 b]
            'R b2 m3 M3 4'     : (4, [0,1,3,4,5],    ['b2','#2','4','x']),        # R 2 m3 M3 7      [0 2 3 4 b]   R b2 2 6 b7      [0 1 2 9 a]   R b2 #5 6 7      [0 1 8 9 b]   R 5 #5 b7 7      [0 7 8 a b]
            'R b2 m3 M3 b5'    : (4, [0,1,3,4,6],    ['o','b2','#2']),            # R 2 m3 4 7       [0 2 3 5 b]   R b2 m3 6 b7     [0 1 3 9 a]   R 2 #5 6 7       [0 2 8 9 b]   R b5 5 6 b7      [0 6 7 9 a]
            'R b2 m3 M3 5'     : (4, [0,1,3,4,7],    ['b2','#2']),                # R 2 m3 b5 7      [0 2 3 6 b]   R b2 M3 6 b7     [0 1 4 9 a]   R m3 #5 6 7      [0 3 8 9 b]   R 4 b5 #5 6      [0 5 6 8 9]
            'R b2 m3 M3 #5'    : (3, [0,1,3,4,8],    ['+','b2','#2']),            # R 2 m3 5 7       [0 2 3 7 b]   R b2 4 6 b7      [0 1 5 9 a]   R M3 #5 6 7      [0 4 8 9 b]   R M3 4 5 #5      [0 4 5 7 8]
            'R b2 m3 M3 6'     : (4, [0,1,3,4,9],    ['b2','#2','6','x']),        # R 2 m3 #5 7      [0 2 3 8 b]   R b2 b5 6 b7     [0 1 6 9 a]   R 4 #5 6 7       [0 5 8 9 b]   R m3 M3 b5 5     [0 3 4 6 7]
            'R b2 m3 M3 b7'    : (0, [0,1,3,4,10],   ['#9','b9','x']),            # R 2 m3 6 7       [0 2 3 9 b]   R b2 5 6 b7      [0 1 7 9 a]   R b5 #5 6 7      [0 6 8 9 b]   R 2 m3 4 b5      [0 2 3 5 6]
            'R b2 m3 M3 7'     : (3, [0,1,3,4,11],   ['M','#9','b9','x']),        # R 2 m3 b7 7      [0 2 3 a b]   R b2 #5 6 b7     [0 1 8 9 a]   R 5 #5 6 7       [0 7 8 9 b]   R b2 2 M3 4      [0 1 2 4 5]
            'R b2 m3 4 b5'     : (4, [0,1,3,5,6],    ['o','b2','4']),             # R 2 M3 4 7       [0 2 4 5 b]   R 2 m3 6 b7      [0 2 3 9 a]   R b2 5 #5 b7     [0 1 7 8 a]   R b5 5 6 7       [0 6 7 9 b]
            'R b2 m3 4 5'      : (4, [0,1,3,5,7],    ['m','b2','4']),             # R 2 M3 b5 7      [0 2 4 6 b]   R 2 M3 6 b7      [0 2 4 9 a]   R 2 5 #5 b7      [0 2 7 8 a]   R 4 b5 #5 b7     [0 5 6 8 a]
            'R b2 m3 4 #5'     : (4, [0,1,3,5,8],    ['m','+','b2','4']),         # R 2 M3 5 7       [0 2 4 7 b]   R 2 4 6 b7       [0 2 5 9 a]   R m3 5 #5 b7     [0 3 7 8 a]   R M3 4 5 6       [0 4 5 7 9]
            'R b2 m3 4 6'      : (4, [0,1,3,5,9],    ['m','b2','4','6','x']),     # R 2 M3 #5 7      [0 2 4 8 b]   R 2 b5 6 b7      [0 2 6 9 a]   R M3 5 #5 b7     [0 4 7 8 a]   R m3 M3 b5 #5    [0 3 4 6 8]
            'R b2 m3 4 b7'     : (0, [0,1,3,5,10],   ['m','11','b9','x']),        # R 2 M3 6 7       [0 2 4 9 b]   R 2 5 6 b7       [0 2 7 9 a]   R 4 5 #5 b7      [0 5 7 8 a]   R 2 m3 4 5       [0 2 3 5 7]
            'R b2 m3 4 7'      : (3, [0,1,3,5,11],   ['m','M','11','b9','x']),    # R 2 M3 b7 7      [0 2 4 a b]   R 2 #5 6 b7      [0 2 8 9 a]   R b5 5 #5 b7     [0 6 7 8 a]   R b2 2 M3 b5     [0 1 2 4 6]
            'R b2 m3 b5 5'     : (3, [0,1,3,6,7],    ['o','b2']),                 # R 2 4 b5 7       [0 2 5 6 b]   R m3 M3 6 b7     [0 3 4 9 a]   R b2 b5 5 6      [0 1 6 7 9]   R 4 b5 #5 7      [0 5 6 8 b]
            'R b2 m3 b5 #5'    : (4, [0,1,3,6,8],    ['o','+','b2']),             # R 2 4 5 7        [0 2 5 7 b]   R m3 4 6 b7      [0 3 5 9 a]   R 2 b5 5 6       [0 2 6 7 9]   R M3 4 5 b7      [0 4 5 7 a]
            'R b2 m3 b5 6'     : (2, [0,1,3,6,9],    ['o','b2','6']),             # R 2 4 #5 7       [0 2 5 8 b]   R m3 b5 6 b7     [0 3 6 9 a]   R m3 b5 5 6      [0 3 6 7 9]   R m3 M3 b5 6     [0 3 4 6 9]
            'R b2 m3 b5 b7'    : (2, [0,1,3,6,10],   ['0','7','b9']),             # R 2 4 6 7        [0 2 5 9 b]   R m3 5 6 b7      [0 3 7 9 a]   R M3 b5 5 6      [0 4 6 7 9]   R 2 m3 4 #5      [0 2 3 5 8]
            'R b2 m3 b5 7'     : (1, [0,1,3,6,11],   ['o','M','b9']),             # R 2 4 b7 7       [0 2 5 a b]   R m3 #5 6 b7     [0 3 8 9 a]   R 4 b5 5 6       [0 5 6 7 9]   R b2 2 M3 5      [0 1 2 4 7]
            'R b2 m3 5 #5'     : (3, [0,1,3,7,8],    ['m','+','b2']),             # R 2 b5 5 7       [0 2 6 7 b]   R M3 4 6 b7      [0 4 5 9 a]   R b2 4 b5 #5     [0 1 5 6 8]   R M3 4 5 7       [0 4 5 7 b]
            'R b2 m3 5 6'      : (2, [0,1,3,7,9],    ['m','b2','6']),             # R 2 b5 #5 7      [0 2 6 8 b]   R M3 b5 6 b7     [0 4 6 9 a]   R 2 4 b5 #5      [0 2 5 6 8]   R m3 M3 b5 b7    [0 3 4 6 a]
            'R b2 m3 5 b7'     : (1, [0,1,3,7,10],   ['m','b9']),                 # R 2 b5 6 7       [0 2 6 9 b]   R M3 5 6 b7      [0 4 7 9 a]   R m3 4 b5 #5     [0 3 5 6 8]   R 2 m3 4 6       [0 2 3 5 9]
            'R b2 m3 5 7'      : (1, [0,1,3,7,11],   ['m','M','b9']),             # R 2 b5 b7 7      [0 2 6 a b]   R M3 #5 6 b7     [0 4 8 9 a]   R M3 4 b5 #5     [0 4 5 6 8]   R b2 2 M3 #5     [0 1 2 4 8]
            'R b2 m3 #5 6'     : (4, [0,1,3,8,9],    ['m','+','b2','6']),         # R 2 5 #5 7       [0 2 7 8 b]   R 4 b5 6 b7      [0 5 6 9 a]   R b2 M3 4 5      [0 1 4 5 7]   R m3 M3 b5 7     [0 3 4 6 b]
            'R b2 m3 #5 b7'    : (3, [0,1,3,8,10],   ['m','+','b9']),             # R 2 5 6 7        [0 2 7 9 b]   R 4 5 6 b7       [0 5 7 9 a]   R 2 M3 4 5       [0 2 4 5 7]   R 2 m3 4 b7      [0 2 3 5 a]
            'R b2 m3 #5 7'     : (0, [0,1,3,8,11],   ['m','+','M','b9']),         # R 2 5 b7 7       [0 2 7 a b]   R 4 #5 6 b7      [0 5 8 9 a]   R m3 M3 4 5      [0 3 4 5 7]   R b2 2 M3 6      [0 1 2 4 9]
            'R b2 m3 6 b7'     : (0, [0,1,3,9,10],   ['m','13','b9','x']),        # R 2 #5 6 7       [0 2 8 9 b]   R b5 5 6 b7      [0 6 7 9 a]   R b2 m3 M3 b5    [0 1 3 4 6]   R 2 m3 4 7       [0 2 3 5 b]
            'R b2 m3 6 7'      : (3, [0,1,3,9,11],   ['m','M','13','b9','x']),    # R 2 #5 b7 7      [0 2 8 a b]   R b5 #5 6 b7     [0 6 8 9 a]   R 2 m3 M3 b5     [0 2 3 4 6]   R b2 2 M3 b7     [0 1 2 4 a]
            'R b2 m3 b7 7'     : (0, [0,1,3,10,11],  ['m','#','13','b9']),        # R 2 6 b7 7       [0 2 9 a b]   R 5 #5 6 b7      [0 7 8 9 a]   R b2 2 m3 4      [0 1 2 3 5]   R b2 2 M3 7      [0 1 2 4 b]
            'R b2 M3 4 b5'     : (3, [0,1,4,5,6],    ['b2','4','b5']),            # R m3 M3 4 7      [0 3 4 5 b]   R b2 2 #5 6      [0 1 2 8 9]   R b2 5 #5 7      [0 1 7 8 b]   R b5 5 b7 7      [0 6 7 a b]
            'R b2 M3 4 5'      : (3, [0,1,4,5,7],    ['b2','4']),                 # R m3 M3 b5 7     [0 3 4 6 b]   R b2 m3 #5 6     [0 1 3 8 9]   R 2 5 #5 7       [0 2 7 8 b]   R 4 b5 6 b7      [0 5 6 9 a]
            'R b2 M3 4 #5'     : (4, [0,1,4,5,8],    ['+','b2','4']),             # R m3 M3 5 7      [0 3 4 7 b]   R b2 M3 #5 6     [0 1 4 8 9]   R m3 5 #5 7      [0 3 7 8 b]   R M3 4 #5 6      [0 4 5 8 9]
            'R b2 M3 4 6'      : (3, [0,1,4,5,9],    ['b2','4','6','x']),         # R m3 M3 #5 7     [0 3 4 8 b]   R b2 4 #5 6      [0 1 5 8 9]   R M3 5 #5 7      [0 4 7 8 b]   R m3 M3 5 #5     [0 3 4 7 8]
            'R b2 M3 4 b7'     : (0, [0,1,4,5,10],   ['11','b9','x']),            # R m3 M3 6 7      [0 3 4 9 b]   R b2 b5 #5 6     [0 1 6 8 9]   R 4 5 #5 7       [0 5 7 8 b]   R 2 m3 b5 5      [0 2 3 6 7]
            'R b2 M3 4 7'      : (1, [0,1,4,5,11],   ['M','11','b9','x']),        # R m3 M3 b7 7     [0 3 4 a b]   R b2 5 #5 6      [0 1 7 8 9]   R b5 5 #5 7      [0 6 7 8 b]   R b2 2 4 b5      [0 1 2 5 6]
            'R b2 M3 b5 5'     : (3, [0,1,4,6,7],    ['b2','#4']),                # R m3 4 b5 7      [0 3 5 6 b]   R 2 m3 #5 6      [0 2 3 8 9]   R b2 b5 5 b7     [0 1 6 7 a]   R 4 b5 6 7       [0 5 6 9 b]
            'R b2 M3 b5 #5'    : (4, [0,1,4,6,8],    ['+','b2','#4']),            # R m3 4 5 7       [0 3 5 7 b]   R 2 M3 #5 6      [0 2 4 8 9]   R 2 b5 5 b7      [0 2 6 7 a]   R M3 4 #5 b7     [0 4 5 8 a]
            'R b2 M3 b5 6'     : (3, [0,1,4,6,9],    ['b2','b5','6']),            # R m3 4 #5 7      [0 3 5 8 b]   R 2 4 #5 6       [0 2 5 8 9]   R m3 b5 5 b7     [0 3 6 7 a]   R m3 M3 5 6      [0 3 4 7 9]
            'R b2 M3 b5 b7'    : (1, [0,1,4,6,10],   ['#','11','b9']),            # R m3 4 6 7       [0 3 5 9 b]   R 2 b5 #5 6      [0 2 6 8 9]   R M3 b5 5 b7     [0 4 6 7 a]   R 2 m3 b5 #5     [0 2 3 6 8]
            'R b2 M3 b5 7'     : (0, [0,1,4,6,11],   ['#','11','b9','x']),        # R m3 4 b7 7      [0 3 5 a b]   R 2 5 #5 6       [0 2 7 8 9]   R 4 b5 5 b7      [0 5 6 7 a]   R b2 2 4 5       [0 1 2 5 7]
            'R b2 M3 5 #5'     : (2, [0,1,4,7,8],    ['b2','b6']),                # R m3 b5 5 7      [0 3 6 7 b]   R m3 M3 #5 6     [0 3 4 8 9]   R b2 4 b5 6      [0 1 5 6 9]   R M3 4 #5 7      [0 4 5 8 b]
            'R b2 M3 5 6'      : (2, [0,1,4,7,9],    ['b2','6']),                 # R m3 b5 #5 7     [0 3 6 8 b]   R m3 4 #5 6      [0 3 5 8 9]   R 2 4 b5 6       [0 2 5 6 9]   R m3 M3 5 b7     [0 3 4 7 a]
            'R b2 M3 5 b7'     : (0, [0,1,4,7,10],   ['b9']),                     # R m3 b5 6 7      [0 3 6 9 b]   R m3 b5 #5 6     [0 3 6 8 9]   R m3 4 b5 6      [0 3 5 6 9]   R 2 m3 b5 6      [0 2 3 6 9]
            'R b2 M3 5 7'      : (0, [0,1,4,7,11],   ['M','b9']),                 # R m3 b5 b7 7     [0 3 6 a b]   R m3 5 #5 6      [0 3 7 8 9]   R M3 4 b5 6      [0 4 5 6 9]   R b2 2 4 #5      [0 1 2 5 8]
            'R b2 M3 #5 6'     : (3, [0,1,4,8,9],    ['+','b2','6']),             # R m3 5 #5 7      [0 3 7 8 b]   R M3 4 #5 6      [0 4 5 8 9]   R b2 M3 4 #5     [0 1 4 5 8]   R m3 M3 5 7      [0 3 4 7 b]
            'R b2 M3 #5 b7'    : (2, [0,1,4,8,10],   ['+','b9']),                 # R m3 5 6 7       [0 3 7 9 b]   R M3 b5 #5 6     [0 4 6 8 9]   R 2 M3 4 #5      [0 2 4 5 8]   R 2 m3 b5 b7     [0 2 3 6 a]
            'R b2 M3 #5 7'     : (1, [0,1,4,8,11],   ['+','M','b9']),             # R m3 5 b7 7      [0 3 7 a b]   R M3 5 #5 6      [0 4 7 8 9]   R m3 M3 4 #5     [0 3 4 5 8]   R b2 2 4 6       [0 1 2 5 9]
            'R b2 M3 6 b7'     : (0, [0,1,4,9,10],   ['13','b9','x']),            # R m3 #5 6 7      [0 3 8 9 b]   R 4 b5 #5 6      [0 5 6 8 9]   R b2 m3 M3 5     [0 1 3 4 7]   R 2 m3 b5 7      [0 2 3 6 b]
            'R b2 M3 6 7'      : (0, [0,1,4,9,11],   ['M','13','b9','x']),        # R m3 #5 b7 7     [0 3 8 a b]   R 4 5 #5 6       [0 5 7 8 9]   R 2 m3 M3 5      [0 2 3 4 7]   R b2 2 4 b7      [0 1 2 5 a]
            'R b2 M3 b7 7'     : (0, [0,1,4,10,11],  ['#','13','b9','x']),        # R m3 6 b7 7      [0 3 9 a b]   R b5 5 #5 6      [0 6 7 8 9]   R b2 2 m3 b5     [0 1 2 3 6]   R b2 2 4 7       [0 1 2 5 b]
            'R b2 4 b5 5'      : (4, [0,1,5,6,7],    ['b2','#4','s4']),           # R M3 4 b5 7      [0 4 5 6 b]   R b2 2 5 #5      [0 1 2 7 8]   R b2 b5 5 7      [0 1 6 7 b]   R 4 b5 b7 7      [0 5 6 a b]
            'R b2 4 b5 #5'     : (4, [0,1,5,6,8],    ['o','+','b2','s4']),        # R M3 4 5 7       [0 4 5 7 b]   R b2 m3 5 #5     [0 1 3 7 8]   R 2 b5 5 7       [0 2 6 7 b]   R M3 4 6 b7      [0 4 5 9 a]
            'R b2 4 b5 6'      : (4, [0,1,5,6,9],    ['o','b2','6','s4']),        # R M3 4 #5 7      [0 4 5 8 b]   R b2 M3 5 #5     [0 1 4 7 8]   R m3 b5 5 7      [0 3 6 7 b]   R m3 M3 #5 6     [0 3 4 8 9]
            'R b2 4 b5 b7'     : (2, [0,1,5,6,10],   ['o','b9','s4']),            # R M3 4 6 7       [0 4 5 9 b]   R b2 4 5 #5      [0 1 5 7 8]   R M3 b5 5 7      [0 4 6 7 b]   R 2 m3 5 #5      [0 2 3 7 8]
            'R b2 4 b5 7'      : (2, [0,1,5,6,11],   ['o','M','b9','s4']),        # R M3 4 b7 7      [0 4 5 a b]   R b2 b5 5 #5     [0 1 6 7 8]   R 4 b5 5 7       [0 5 6 7 b]   R b2 2 b5 5      [0 1 2 6 7]
            'R b2 4 5 #5'      : (4, [0,1,5,7,8],    ['+','b2','s4']),            # R M3 b5 5 7      [0 4 6 7 b]   R 2 m3 5 #5      [0 2 3 7 8]   R b2 4 b5 b7     [0 1 5 6 a]   R M3 4 6 7       [0 4 5 9 b]
            'R b2 4 5 6'       : (3, [0,1,5,7,9],    ['b2','6','s4']),            # R M3 b5 #5 7     [0 4 6 8 b]   R 2 M3 5 #5      [0 2 4 7 8]   R 2 4 b5 b7      [0 2 5 6 a]   R m3 M3 #5 b7    [0 3 4 8 a]
            'R b2 4 5 b7'      : (2, [0,1,5,7,10],   ['b9','s4']),                # R M3 b5 6 7      [0 4 6 9 b]   R 2 4 5 #5       [0 2 5 7 8]   R m3 4 b5 b7     [0 3 5 6 a]   R 2 m3 5 6       [0 2 3 7 9]
            'R b2 4 5 7'       : (2, [0,1,5,7,11],   ['M','b9','s4']),            # R M3 b5 b7 7     [0 4 6 a b]   R 2 b5 5 #5      [0 2 6 7 8]   R M3 4 b5 b7     [0 4 5 6 a]   R b2 2 b5 #5     [0 1 2 6 8]
            'R b2 4 #5 6'      : (4, [0,1,5,8,9],    ['+','b2','6','s4']),        # R M3 5 #5 7      [0 4 7 8 b]   R m3 M3 5 #5     [0 3 4 7 8]   R b2 M3 4 6      [0 1 4 5 9]   R m3 M3 #5 7     [0 3 4 8 b]
            'R b2 4 #5 b7'     : (3, [0,1,5,8,10],   ['b9','+','s4']),            # R M3 5 6 7       [0 4 7 9 b]   R m3 4 5 #5      [0 3 5 7 8]   R 2 M3 4 6       [0 2 4 5 9]   R 2 m3 5 b7      [0 2 3 7 a]
            'R b2 4 #5 7'      : (1, [0,1,5,8,11],   ['M','+','b9','s4']),        # R M3 5 b7 7      [0 4 7 a b]   R m3 b5 5 #5     [0 3 6 7 8]   R m3 M3 4 6      [0 3 4 5 9]   R b2 2 b5 6      [0 1 2 6 9]
            'R b2 4 6 b7'      : (4, [0,1,5,9,10],   ['13','b9','s4','x']),       # R M3 #5 6 7      [0 4 8 9 b]   R M3 4 5 #5      [0 4 5 7 8]   R b2 m3 M3 #5    [0 1 3 4 8]   R 2 m3 5 7       [0 2 3 7 b]
            'R b2 4 6 7'       : (2, [0,1,5,9,11],   ['M','13','b9','s4','x']),   # R M3 #5 b7 7     [0 4 8 a b]   R M3 b5 5 #5     [0 4 6 7 8]   R 2 m3 M3 #5     [0 2 3 4 8]   R b2 2 b5 b7     [0 1 2 6 a]
            'R b2 4 b7 7'      : (0, [0,1,5,10,11],  ['#','13','b9','s4','x']),   # R M3 6 b7 7      [0 4 9 a b]   R 4 b5 5 #5      [0 5 6 7 8]   R b2 2 m3 5      [0 1 2 3 7]   R b2 2 b5 7      [0 1 2 6 b]
            'R b2 b5 5 #5'     : (4, [0,1,6,7,8],    ['b2','#4','b6','y']),       # R 4 b5 5 7       [0 5 6 7 b]   R b2 2 b5 5      [0 1 2 6 7]   R b2 4 b5 7      [0 1 5 6 b]   R M3 4 b7 7      [0 4 5 a b]
            'R b2 b5 5 6'      : (4, [0,1,6,7,9],    ['b2','#4','6']),            # R 4 b5 #5 7      [0 5 6 8 b]   R b2 m3 b5 5     [0 1 3 6 7]   R 2 4 b5 7       [0 2 5 6 b]   R m3 M3 6 b7     [0 3 4 9 a]
            'R b2 b5 5 b7'     : (2, [0,1,6,7,10],   ['#','11','b9','y']),        # R 4 b5 6 7       [0 5 6 9 b]   R b2 M3 b5 5     [0 1 4 6 7]   R m3 4 b5 7      [0 3 5 6 b]   R 2 m3 #5 6      [0 2 3 8 9]
            'R b2 b5 5 7'      : (2, [0,1,6,7,11],   ['M','#','11','b9','y']),    # R 4 b5 b7 7      [0 5 6 a b]   R b2 4 b5 5      [0 1 5 6 7]   R M3 4 b5 7      [0 4 5 6 b]   R b2 2 5 #5      [0 1 2 7 8]
            'R b2 b5 #5 6'     : (4, [0,1,6,8,9],    ['o','+','b2','6']),         # R 4 5 #5 7       [0 5 7 8 b]   R 2 m3 b5 5      [0 2 3 6 7]   R b2 M3 4 b7     [0 1 4 5 a]   R m3 M3 6 7      [0 3 4 9 b]
            'R b2 b5 #5 b7'    : (2, [0,1,6,8,10],   ['o','+','b9','y']),         # R 4 5 6 7        [0 5 7 9 b]   R 2 M3 b5 5      [0 2 4 6 7]   R 2 M3 4 b7      [0 2 4 5 a]   R 2 m3 #5 b7     [0 2 3 8 a]
            'R b2 b5 #5 7'     : (1, [0,1,6,8,11],   ['o','+','b9','y']),         # R 4 5 b7 7       [0 5 7 a b]   R 2 4 b5 5       [0 2 5 6 7]   R m3 M3 4 b7     [0 3 4 5 a]   R b2 2 5 6       [0 1 2 7 9]
            'R b2 b5 6 b7'     : (2, [0,1,6,9,10],   ['13','b9','b5','y']),       # R 4 #5 6 7       [0 5 8 9 b]   R m3 M3 b5 5     [0 3 4 6 7]   R b2 m3 M3 6     [0 1 3 4 9]   R 2 m3 #5 7      [0 2 3 8 b]
            'R b2 b5 6 7'      : (2, [0,1,6,9,11],   ['M','13','b9','b5']),       # R 4 #5 b7 7      [0 5 8 a b]   R m3 4 b5 5      [0 3 5 6 7]   R 2 m3 M3 6      [0 2 3 4 9]   R b2 2 5 b7      [0 1 2 7 a]
            'R b2 b5 b7 7'     : (1, [0,1,6,10,11],  ['#','13','b9','b5']),       # R 4 6 b7 7       [0 5 9 a b]   R M3 4 b5 5      [0 4 5 6 7]   R b2 2 m3 #5     [0 1 2 3 8]   R b2 2 5 7       [0 1 2 7 b]
            'R b2 5 #5 6'      : (4, [0,1,7,8,9],    ['+','b2','6','y']),         # R b5 5 #5 7      [0 6 7 8 b]   R b2 2 4 b5      [0 1 2 5 6]   R b2 M3 4 7      [0 1 4 5 b]   R m3 M3 b7 7     [0 3 4 a b]
            'R b2 5 #5 b7'     : (1, [0,1,7,8,10],   ['b','13','b9','y']),        # R b5 5 6 7       [0 6 7 9 b]   R b2 m3 4 b5     [0 1 3 5 6]   R 2 M3 4 7       [0 2 4 5 b]   R 2 m3 6 b7      [0 2 3 9 a]
            'R b2 5 #5 7'      : (1, [0,1,7,8,11],   ['M','b','13','b9','y']),    # R b5 5 b7 7      [0 6 7 a b]   R b2 M3 4 b5     [0 1 4 5 6]   R m3 M3 4 7      [0 3 4 5 b]   R b2 2 #5 6      [0 1 2 8 9]
            'R b2 5 6 b7'      : (1, [0,1,7,9,10],   ['13','b9','y']),            # R b5 #5 6 7      [0 6 8 9 b]   R 2 m3 4 b5      [0 2 3 5 6]   R b2 m3 M3 b7    [0 1 3 4 a]   R 2 m3 6 7       [0 2 3 9 b]
            'R b2 5 6 7'       : (1, [0,1,7,9,11],   ['M','13','b9','y']),        # R b5 #5 b7 7     [0 6 8 a b]   R 2 M3 4 b5      [0 2 4 5 6]   R 2 m3 M3 b7     [0 2 3 4 a]   R b2 2 #5 b7     [0 1 2 8 a]
            'R b2 5 b7 7'      : (0, [0,1,7,10,11],  ['#','13','b9','y']),        # R b5 6 b7 7      [0 6 9 a b]   R m3 M3 4 b5     [0 3 4 5 6]   R b2 2 m3 6      [0 1 2 3 9]   R b2 2 #5 7      [0 1 2 8 b]
            'R b2 #5 6 b7'     : (2, [0,1,8,9,10],   ['+','13','b9','y']),        # R 5 #5 6 7       [0 7 8 9 b]   R b2 2 M3 4      [0 1 2 4 5]   R b2 m3 M3 7     [0 1 3 4 b]   R 2 m3 b7 7      [0 2 3 a b]
            'R b2 #5 6 7'      : (0, [0,1,8,9,11],   ['+','M','13','b9','y']),    # R 5 #5 b7 7      [0 7 8 a b]   R b2 m3 M3 4     [0 1 3 4 5]   R 2 m3 M3 7      [0 2 3 4 b]   R b2 2 6 b7      [0 1 2 9 a]
            'R b2 #5 b7 7'     : (3, [0,1,8,10,11],  ['+','#','13','b9','y']),    # R 5 6 b7 7       [0 7 9 a b]   R 2 m3 M3 4      [0 2 3 4 5]   R b2 2 m3 b7     [0 1 2 3 a]   R b2 2 6 7       [0 1 2 9 b]
            'R b2 6 b7 7'      : (3, [0,1,9,10,11],  ['#','13','13','b9','xy']),  # R #5 6 b7 7      [0 8 9 a b]   R b2 2 m3 M3     [0 1 2 3 4]   R b2 2 m3 7      [0 1 2 3 b]   R b2 2 b7 7      [0 1 2 a b]
            'R 2 m3 M3 4'      : (4, [0,2,3,4,5],    ['2','#2','4','x']),         # R b2 2 m3 b7     [0 1 2 3 a]   R b2 2 6 7       [0 1 2 9 b]   R b2 #5 b7 7     [0 1 8 a b]   R 5 6 b7 7       [0 7 9 a b]
            'R 2 m3 M3 b5'     : (4, [0,2,3,4,6],    ['o','2','#2']),             # R b2 2 M3 b7     [0 1 2 4 a]   R b2 m3 6 7      [0 1 3 9 b]   R 2 #5 b7 7      [0 2 8 a b]   R b5 #5 6 b7     [0 6 8 9 a]
            'R 2 m3 M3 5'      : (3, [0,2,3,4,7],    ['2','#2']),                 # R b2 2 4 b7      [0 1 2 5 a]   R b2 M3 6 7      [0 1 4 9 b]   R m3 #5 b7 7     [0 3 8 a b]   R 4 5 #5 6       [0 5 7 8 9]
            'R 2 m3 M3 #5'     : (4, [0,2,3,4,8],    ['+','2','#2']),             # R b2 2 b5 b7     [0 1 2 6 a]   R b2 4 6 7       [0 1 5 9 b]   R M3 #5 b7 7     [0 4 8 a b]   R M3 b5 5 #5     [0 4 6 7 8]
            'R 2 m3 M3 6'      : (4, [0,2,3,4,9],    ['2','#2','6','x']),         # R b2 2 5 b7      [0 1 2 7 a]   R b2 b5 6 7      [0 1 6 9 b]   R 4 #5 b7 7      [0 5 8 a b]   R m3 4 b5 5      [0 3 5 6 7]
            'R 2 m3 M3 b7'     : (2, [0,2,3,4,10],   ['#9','9','x']),             # R b2 2 #5 b7     [0 1 2 8 a]   R b2 5 6 7       [0 1 7 9 b]   R b5 #5 b7 7     [0 6 8 a b]   R 2 M3 4 b5      [0 2 4 5 6]
            'R 2 m3 M3 7'      : (1, [0,2,3,4,11],   ['M','#9','9','x']),         # R b2 2 6 b7      [0 1 2 9 a]   R b2 #5 6 7      [0 1 8 9 b]   R 5 #5 b7 7      [0 7 8 a b]   R b2 m3 M3 4     [0 1 3 4 5]
            'R 2 m3 4 b5'      : (4, [0,2,3,5,6],    ['o','2','4']),              # R b2 m3 M3 b7    [0 1 3 4 a]   R 2 m3 6 7       [0 2 3 9 b]   R b2 5 6 b7      [0 1 7 9 a]   R b5 #5 6 7      [0 6 8 9 b]
            'R 2 m3 4 5'       : (4, [0,2,3,5,7],    ['m','2','4']),              # R b2 m3 4 b7     [0 1 3 5 a]   R 2 M3 6 7       [0 2 4 9 b]   R 2 5 6 b7       [0 2 7 9 a]   R 4 5 #5 b7      [0 5 7 8 a]
            'R 2 m3 4 #5'      : (4, [0,2,3,5,8],    ['m','+','2','4']),          # R b2 m3 b5 b7    [0 1 3 6 a]   R 2 4 6 7        [0 2 5 9 b]   R m3 5 6 b7      [0 3 7 9 a]   R M3 b5 5 6      [0 4 6 7 9]
            'R 2 m3 4 6'       : (4, [0,2,3,5,9],    ['m','2','4','6','x']),      # R b2 m3 5 b7     [0 1 3 7 a]   R 2 b5 6 7       [0 2 6 9 b]   R M3 5 6 b7      [0 4 7 9 a]   R m3 4 b5 #5     [0 3 5 6 8]
            'R 2 m3 4 b7'      : (0, [0,2,3,5,10],   ['m','11','9','x']),         # R b2 m3 #5 b7    [0 1 3 8 a]   R 2 5 6 7        [0 2 7 9 b]   R 4 5 6 b7       [0 5 7 9 a]   R 2 M3 4 5       [0 2 4 5 7]
            'R 2 m3 4 7'       : (2, [0,2,3,5,11],   ['m','M','11','9','x']),     # R b2 m3 6 b7     [0 1 3 9 a]   R 2 #5 6 7       [0 2 8 9 b]   R b5 5 6 b7      [0 6 7 9 a]   R b2 m3 M3 b5    [0 1 3 4 6]
            'R 2 m3 b5 5'      : (3, [0,2,3,6,7],    ['m','2','#4']),             # R b2 M3 4 b7     [0 1 4 5 a]   R m3 M3 6 7      [0 3 4 9 b]   R b2 b5 #5 6     [0 1 6 8 9]   R 4 5 #5 7       [0 5 7 8 b]
            'R 2 m3 b5 #5'     : (3, [0,2,3,6,8],    ['o','+','2']),              # R b2 M3 b5 b7    [0 1 4 6 a]   R m3 4 6 7       [0 3 5 9 b]   R 2 b5 #5 6      [0 2 6 8 9]   R M3 b5 5 b7     [0 4 6 7 a]
            'R 2 m3 b5 6'      : (3, [0,2,3,6,9],    ['o','2','6']),              # R b2 M3 5 b7     [0 1 4 7 a]   R m3 b5 6 7      [0 3 6 9 b]   R m3 b5 #5 6     [0 3 6 8 9]   R m3 4 b5 6      [0 3 5 6 9]
            'R 2 m3 b5 b7'     : (0, [0,2,3,6,10],   ['0','9']),                  # R b2 M3 #5 b7    [0 1 4 8 a]   R m3 5 6 7       [0 3 7 9 b]   R M3 b5 #5 6     [0 4 6 8 9]   R 2 M3 4 #5      [0 2 4 5 8]
            'R 2 m3 b5 7'      : (1, [0,2,3,6,11],   ['o','M','9']),              # R b2 M3 6 b7     [0 1 4 9 a]   R m3 #5 6 7      [0 3 8 9 b]   R 4 b5 #5 6      [0 5 6 8 9]   R b2 m3 M3 5     [0 1 3 4 7]
            'R 2 m3 5 #5'      : (3, [0,2,3,7,8],    ['m','+','2']),              # R b2 4 b5 b7     [0 1 5 6 a]   R M3 4 6 7       [0 4 5 9 b]   R b2 4 5 #5      [0 1 5 7 8]   R M3 b5 5 7      [0 4 6 7 b]
            'R 2 m3 5 6'       : (3, [0,2,3,7,9],    ['m','2','6']),              # R b2 4 5 b7      [0 1 5 7 a]   R M3 b5 6 7      [0 4 6 9 b]   R 2 4 5 #5       [0 2 5 7 8]   R m3 4 b5 b7     [0 3 5 6 a]
            'R 2 m3 5 b7'      : (0, [0,2,3,7,10],   ['m','9']),                  # R b2 4 #5 b7     [0 1 5 8 a]   R M3 5 6 7       [0 4 7 9 b]   R m3 4 5 #5      [0 3 5 7 8]   R 2 M3 4 6       [0 2 4 5 9]
            'R 2 m3 5 7'       : (1, [0,2,3,7,11],   ['m','M','9']),              # R b2 4 6 b7      [0 1 5 9 a]   R M3 #5 6 7      [0 4 8 9 b]   R M3 4 5 #5      [0 4 5 7 8]   R b2 m3 M3 #5    [0 1 3 4 8]
            'R 2 m3 #5 6'      : (4, [0,2,3,8,9],    ['m','+','2','6']),          # R b2 b5 5 b7     [0 1 6 7 a]   R 4 b5 6 7       [0 5 6 9 b]   R b2 M3 b5 5     [0 1 4 6 7]   R m3 4 b5 7      [0 3 5 6 b]
            'R 2 m3 #5 b7'     : (1, [0,2,3,8,10],   ['m','+','9']),              # R b2 b5 #5 b7    [0 1 6 8 a]   R 4 5 6 7        [0 5 7 9 b]   R 2 M3 b5 5      [0 2 4 6 7]   R 2 M3 4 b7      [0 2 4 5 a]
            'R 2 m3 #5 7'      : (0, [0,2,3,8,11],   ['+','M','9','x']),          # R b2 b5 6 b7     [0 1 6 9 a]   R 4 #5 6 7       [0 5 8 9 b]   R m3 M3 b5 5     [0 3 4 6 7]   R b2 m3 M3 6     [0 1 3 4 9]
            'R 2 m3 6 b7'      : (0, [0,2,3,9,10],   ['m','13','9','x']),         # R b2 5 #5 b7     [0 1 7 8 a]   R b5 5 6 7       [0 6 7 9 b]   R b2 m3 4 b5     [0 1 3 5 6]   R 2 M3 4 7       [0 2 4 5 b]
            'R 2 m3 6 7'       : (3, [0,2,3,9,11],   ['m','M','13','9','x']),     # R b2 5 6 b7      [0 1 7 9 a]   R b5 #5 6 7      [0 6 8 9 b]   R 2 m3 4 b5      [0 2 3 5 6]   R b2 m3 M3 b7    [0 1 3 4 a]
            'R 2 m3 b7 7'      : (1, [0,2,3,10,11],  ['m','#','13','9']),         # R b2 #5 6 b7     [0 1 8 9 a]   R 5 #5 6 7       [0 7 8 9 b]   R b2 2 M3 4      [0 1 2 4 5]   R b2 m3 M3 7     [0 1 3 4 b]
            'R 2 M3 4 b5'      : (3, [0,2,4,5,6],    ['b5','2','4']),             # R 2 m3 M3 b7     [0 2 3 4 a]   R b2 2 #5 b7     [0 1 2 8 a]   R b2 5 6 7       [0 1 7 9 b]   R b5 #5 b7 7     [0 6 8 a b]
            'R 2 M3 4 5'       : (4, [0,2,4,5,7],    ['2','4']),                  # R 2 m3 4 b7      [0 2 3 5 a]   R b2 m3 #5 b7    [0 1 3 8 a]   R 2 5 6 7        [0 2 7 9 b]   R 4 5 6 b7       [0 5 7 9 a]
            'R 2 M3 4 #5'      : (3, [0,2,4,5,8],    ['+','2','4']),              # R 2 m3 b5 b7     [0 2 3 6 a]   R b2 M3 #5 b7    [0 1 4 8 a]   R m3 5 6 7       [0 3 7 9 b]   R M3 b5 #5 6     [0 4 6 8 9]
            'R 2 M3 4 6'       : (2, [0,2,4,5,9],    ['2','4','6','x']),          # R 2 m3 5 b7      [0 2 3 7 a]   R b2 4 #5 b7     [0 1 5 8 a]   R M3 5 6 7       [0 4 7 9 b]   R m3 4 5 #5      [0 3 5 7 8]
            'R 2 M3 4 b7'      : (0, [0,2,4,5,10],   ['11','9','x']),             # R 2 m3 #5 b7     [0 2 3 8 a]   R b2 b5 #5 b7    [0 1 6 8 a]   R 4 5 6 7        [0 5 7 9 b]   R 2 M3 b5 5      [0 2 4 6 7]
            'R 2 M3 4 7'       : (2, [0,2,4,5,11],   ['M','11','9','x']),         # R 2 m3 6 b7      [0 2 3 9 a]   R b2 5 #5 b7     [0 1 7 8 a]   R b5 5 6 7       [0 6 7 9 b]   R b2 m3 4 b5     [0 1 3 5 6]
            'R 2 M3 b5 5'      : (4, [0,2,4,6,7],    ['2','#4']),                 # R 2 M3 4 b7      [0 2 4 5 a]   R 2 m3 #5 b7     [0 2 3 8 a]   R b2 b5 #5 b7    [0 1 6 8 a]   R 4 5 6 7        [0 5 7 9 b]
            'R 2 M3 b5 #5'     : (3, [0,2,4,6,8],    ['+','2','#4']),             # R 2 M3 b5 b7     [0 2 4 6 a]   R 2 M3 #5 b7     [0 2 4 8 a]   R 2 b5 #5 b7     [0 2 6 8 a]   R M3 b5 #5 b7    [0 4 6 8 a]
            'R 2 M3 b5 6'      : (4, [0,2,4,6,9],    ['2','b5','6']),             # R 2 M3 5 b7      [0 2 4 7 a]   R 2 4 #5 b7      [0 2 5 8 a]   R m3 b5 #5 b7    [0 3 6 8 a]   R m3 4 5 6       [0 3 5 7 9]
            'R 2 M3 b5 b7'     : (1, [0,2,4,6,10],   ['#','11','9','x']),         # R 2 M3 #5 b7     [0 2 4 8 a]   R 2 b5 #5 b7     [0 2 6 8 a]   R M3 b5 #5 b7    [0 4 6 8 a]   R 2 M3 b5 #5     [0 2 4 6 8]
            'R 2 M3 b5 7'      : (1, [0,2,4,6,11],   ['M','#','11','9']),         # R 2 M3 6 b7      [0 2 4 9 a]   R 2 5 #5 b7      [0 2 7 8 a]   R 4 b5 #5 b7     [0 5 6 8 a]   R b2 m3 4 5      [0 1 3 5 7]
            'R 2 M3 5 #5'      : (2, [0,2,4,7,8],    ['2','b6']),                 # R 2 4 b5 b7      [0 2 5 6 a]   R m3 M3 #5 b7    [0 3 4 8 a]   R b2 4 5 6       [0 1 5 7 9]   R M3 b5 #5 7     [0 4 6 8 b]
            'R 2 M3 5 6'       : (1, [0,2,4,7,9],    ['2','6']),                  # R 2 4 5 b7       [0 2 5 7 a]   R m3 4 #5 b7     [0 3 5 8 a]   R 2 4 5 6        [0 2 5 7 9]   R m3 4 5 b7      [0 3 5 7 a]
            'R 2 M3 5 b7'      : (0, [0,2,4,7,10],   ['9']),                      # R 2 4 #5 b7      [0 2 5 8 a]   R m3 b5 #5 b7    [0 3 6 8 a]   R m3 4 5 6       [0 3 5 7 9]   R 2 M3 b5 6      [0 2 4 6 9]
            'R 2 M3 5 7'       : (0, [0,2,4,7,11],   ['M','9']),                  # R 2 4 6 b7       [0 2 5 9 a]   R m3 5 #5 b7     [0 3 7 8 a]   R M3 4 5 6       [0 4 5 7 9]   R b2 m3 4 #5     [0 1 3 5 8]
            'R 2 M3 #5 6'      : (3, [0,2,4,8,9],    ['+','2','6']),              # R 2 b5 5 b7      [0 2 6 7 a]   R M3 4 #5 b7     [0 4 5 8 a]   R b2 M3 b5 #5    [0 1 4 6 8]   R m3 4 5 7       [0 3 5 7 b]
            'R 2 M3 #5 b7'     : (0, [0,2,4,8,10],   ['+','9']),                  # R 2 b5 #5 b7     [0 2 6 8 a]   R M3 b5 #5 b7    [0 4 6 8 a]   R 2 M3 b5 #5     [0 2 4 6 8]   R 2 M3 b5 b7     [0 2 4 6 a]
            'R 2 M3 #5 7'      : (2, [0,2,4,8,11],   ['M','+','9']),              # R 2 b5 6 b7      [0 2 6 9 a]   R M3 5 #5 b7     [0 4 7 8 a]   R m3 M3 b5 #5    [0 3 4 6 8]   R b2 m3 4 6      [0 1 3 5 9]
            'R 2 M3 6 b7'      : (0, [0,2,4,9,10],   ['13','9','x']),             # R 2 5 #5 b7      [0 2 7 8 a]   R 4 b5 #5 b7     [0 5 6 8 a]   R b2 m3 4 5      [0 1 3 5 7]   R 2 M3 b5 7      [0 2 4 6 b]
            'R 2 M3 6 7'       : (2, [0,2,4,9,11],   ['M','13','9','x']),         # R 2 5 6 b7       [0 2 7 9 a]   R 4 5 #5 b7      [0 5 7 8 a]   R 2 m3 4 5       [0 2 3 5 7]   R b2 m3 4 b7     [0 1 3 5 a]
            'R 2 M3 b7 7'      : (1, [0,2,4,10,11],  ['#','13','9','x']),         # R 2 #5 6 b7      [0 2 8 9 a]   R b5 5 #5 b7     [0 6 7 8 a]   R b2 2 M3 b5     [0 1 2 4 6]   R b2 m3 4 7      [0 1 3 5 b]
            'R 2 4 b5 5'       : (3, [0,2,5,6,7],    ['o','s2','s4']),            # R m3 M3 4 b7     [0 3 4 5 a]   R b2 2 5 6       [0 1 2 7 9]   R b2 b5 #5 7     [0 1 6 8 b]   R 4 5 b7 7       [0 5 7 a b]
            'R 2 4 b5 #5'      : (3, [0,2,5,6,8],    ['o','+','s2','24']),        # R m3 M3 b5 b7    [0 3 4 6 a]   R b2 m3 5 6      [0 1 3 7 9]   R 2 b5 #5 7      [0 2 6 8 b]   R M3 b5 6 b7     [0 4 6 9 a]
            'R 2 4 b5 6'       : (3, [0,2,5,6,9],    ['o','6','s2','s4']),        # R m3 M3 5 b7     [0 3 4 7 a]   R b2 M3 5 6      [0 1 4 7 9]   R m3 b5 #5 7     [0 3 6 8 b]   R m3 4 #5 6      [0 3 5 8 9]
            'R 2 4 b5 b7'      : (4, [0,2,5,6,10],   ['o','7','s2','s4']),        # R m3 M3 #5 b7    [0 3 4 8 a]   R b2 4 5 6       [0 1 5 7 9]   R M3 b5 #5 7     [0 4 6 8 b]   R 2 M3 5 #5      [0 2 4 7 8]
            'R 2 4 b5 7'       : (2, [0,2,5,6,11],   ['o','M','7','s2','s4']),    # R m3 M3 6 b7     [0 3 4 9 a]   R b2 b5 5 6      [0 1 6 7 9]   R 4 b5 #5 7      [0 5 6 8 b]   R b2 m3 b5 5     [0 1 3 6 7]
            'R 2 4 5 #5'       : (4, [0,2,5,7,8],    ['+','s2','s4']),            # R m3 4 b5 b7     [0 3 5 6 a]   R 2 m3 5 6       [0 2 3 7 9]   R b2 4 5 b7      [0 1 5 7 a]   R M3 b5 6 7      [0 4 6 9 b]
            'R 2 4 5 6'        : (2, [0,2,5,7,9],    ['6','s2','s4']),            # R m3 4 5 b7      [0 3 5 7 a]   R 2 M3 5 6       [0 2 4 7 9]   R 2 4 5 b7       [0 2 5 7 a]   R m3 4 #5 b7     [0 3 5 8 a]
            'R 2 4 5 b7'       : (3, [0,2,5,7,10],   ['7','s2','s4']),            # R m3 4 #5 b7     [0 3 5 8 a]   R 2 4 5 6        [0 2 5 7 9]   R m3 4 5 b7      [0 3 5 7 a]   R 2 M3 5 6       [0 2 4 7 9]
            'R 2 4 5 7'        : (2, [0,2,5,7,11],   ['M','7','s2','s4']),        # R m3 4 6 b7      [0 3 5 9 a]   R 2 b5 5 6       [0 2 6 7 9]   R M3 4 5 b7      [0 4 5 7 a]   R b2 m3 b5 #5    [0 1 3 6 8]
            'R 2 4 #5 6'       : (4, [0,2,5,8,9],    ['+','6','s2','s4']),        # R m3 b5 5 b7     [0 3 6 7 a]   R m3 M3 5 6      [0 3 4 7 9]   R b2 M3 b5 6     [0 1 4 6 9]   R m3 4 #5 7      [0 3 5 8 b]
            'R 2 4 #5 b7'      : (3, [0,2,5,8,10],   ['+','7','s2','s4']),        # R m3 b5 #5 b7    [0 3 6 8 a]   R m3 4 5 6       [0 3 5 7 9]   R 2 M3 b5 6      [0 2 4 6 9]   R 2 M3 5 b7      [0 2 4 7 a]
            'R 2 4 #5 7'       : (1, [0,2,5,8,11],   ['+','M','7','s2','s4']),    # R m3 b5 6 b7     [0 3 6 9 a]   R m3 b5 5 6      [0 3 6 7 9]   R m3 M3 b5 6     [0 3 4 6 9]   R b2 m3 b5 6     [0 1 3 6 9]
#           'R 2 4 6 b7'       : (3, [0,2,5,9,10],   ['13','s2','s4','x']),       # R m3 5 #5 b7     [0 3 7 8 a]   R M3 4 5 6       [0 4 5 7 9]   R b2 m3 4 #5     [0 1 3 5 8]   R 2 M3 5 7       [0 2 4 7 b]
            'R 2 4 6 b7'       : (3, [0,2,5,9,10],   ['13','11','9','x','y']),    # R m3 5 #5 b7     [0 3 7 8 a]   R M3 4 5 6       [0 4 5 7 9]   R b2 m3 4 #5     [0 1 3 5 8]   R 2 M3 5 7       [0 2 4 7 b]
            'R 2 4 6 7'        : (1, [0,2,5,9,11],   ['M','13','s2','s4','x']),   # R m3 5 6 b7      [0 3 7 9 a]   R M3 b5 5 6      [0 4 6 7 9]   R 2 m3 4 #5      [0 2 3 5 8]   R b2 m3 b5 b7    [0 1 3 6 a]
            'R 2 4 b7 7'       : (2, [0,2,5,10,11],  ['#','13','s2','s4']),       # R m3 #5 6 b7     [0 3 8 9 a]   R 4 b5 5 6       [0 5 6 7 9]   R b2 2 M3 5      [0 1 2 4 7]   R b2 m3 b5 7     [0 1 3 6 b]
            'R 2 b5 5 #5'      : (3, [0,2,6,7,8],    ['#4','b6','s2']),           # R M3 4 b5 b7     [0 4 5 6 a]   R b2 2 b5 #5     [0 1 2 6 8]   R b2 4 5 7       [0 1 5 7 b]   R M3 b5 b7 7     [0 4 6 a b]
            'R 2 b5 5 6'       : (3, [0,2,6,7,9],    ['2','#4','6']),             # R M3 4 5 b7      [0 4 5 7 a]   R b2 m3 b5 #5    [0 1 3 6 8]   R 2 4 5 7        [0 2 5 7 b]   R m3 4 6 b7      [0 3 5 9 a]
            'R 2 b5 5 b7'      : (2, [0,2,6,7,10],   ['#','11','s2']),            # R M3 4 #5 b7     [0 4 5 8 a]   R b2 M3 b5 #5    [0 1 4 6 8]   R m3 4 5 7       [0 3 5 7 b]   R 2 M3 #5 6      [0 2 4 8 9]
            'R 2 b5 5 7'       : (2, [0,2,6,7,11],   ['M','#','11','s2']),        # R M3 4 6 b7      [0 4 5 9 a]   R b2 4 b5 #5     [0 1 5 6 8]   R M3 4 5 7       [0 4 5 7 b]   R b2 m3 5 #5     [0 1 3 7 8]
            'R 2 b5 #5 6'      : (4, [0,2,6,8,9],    ['o','+','2','6']),          # R M3 b5 5 b7     [0 4 6 7 a]   R 2 m3 b5 #5     [0 2 3 6 8]   R b2 M3 b5 b7    [0 1 4 6 a]   R m3 4 6 7       [0 3 5 9 b]
            'R 2 b5 #5 b7'     : (4, [0,2,6,8,10],   ['o','+','7','s2']),         # R M3 b5 #5 b7    [0 4 6 8 a]   R 2 M3 b5 #5     [0 2 4 6 8]   R 2 M3 b5 b7     [0 2 4 6 a]   R 2 M3 #5 b7     [0 2 4 8 a]
            'R 2 b5 #5 7'      : (4, [0,2,6,8,11],   ['M','o','+','7','s2']),     # R M3 b5 6 b7     [0 4 6 9 a]   R 2 4 b5 #5      [0 2 5 6 8]   R m3 M3 b5 b7    [0 3 4 6 a]   R b2 m3 5 6      [0 1 3 7 9]
            'R 2 b5 6 b7'      : (1, [0,2,6,9,10],   ['o','13','s2']),            # R M3 5 #5 b7     [0 4 7 8 a]   R m3 M3 b5 #5    [0 3 4 6 8]   R b2 m3 4 6      [0 1 3 5 9]   R 2 M3 #5 7      [0 2 4 8 b]
            'R 2 b5 6 7'       : (2, [0,2,6,9,11],   ['M','o','13','9']),         # R M3 5 6 b7      [0 4 7 9 a]   R m3 4 b5 #5     [0 3 5 6 8]   R 2 m3 4 6       [0 2 3 5 9]   R b2 m3 5 b7     [0 1 3 7 a]
            'R 2 b5 b7 7'      : (2, [0,2,6,10,11],  ['o','#','13','s2']),        # R M3 #5 6 b7     [0 4 8 9 a]   R M3 4 b5 #5     [0 4 5 6 8]   R b2 2 M3 #5     [0 1 2 4 8]   R b2 m3 5 7      [0 1 3 7 b]
            'R 2 5 #5 6'       : (3, [0,2,7,8,9],    ['+','6','s2']),             # R 4 b5 5 b7      [0 5 6 7 a]   R b2 2 4 5       [0 1 2 5 7]   R b2 M3 b5 7     [0 1 4 6 b]   R m3 4 b7 7      [0 3 5 a b]
            'R 2 5 #5 b7'      : (2, [0,2,7,8,10],   ['+','b','13','s2']),        # R 4 b5 #5 b7     [0 5 6 8 a]   R b2 m3 4 5      [0 1 3 5 7]   R 2 M3 b5 7      [0 2 4 6 b]   R 2 M3 6 b7      [0 2 4 9 a]
            'R 2 5 #5 7'       : (2, [0,2,7,8,11],   ['M','b','13','s2']),        # R 4 b5 6 b7      [0 5 6 9 a]   R b2 M3 4 5      [0 1 4 5 7]   R m3 M3 b5 7     [0 3 4 6 b]   R b2 m3 #5 6     [0 1 3 8 9]
            'R 2 5 6 b7'       : (1, [0,2,7,9,10],   ['13','s2']),                # R 4 5 #5 b7      [0 5 7 8 a]   R 2 m3 4 5       [0 2 3 5 7]   R b2 m3 4 b7     [0 1 3 5 a]   R 2 M3 6 7       [0 2 4 9 b]
            'R 2 5 6 7'        : (2, [0,2,7,9,11],   ['M','13','s2']),            # R 4 5 6 b7       [0 5 7 9 a]   R 2 M3 4 5       [0 2 4 5 7]   R 2 m3 4 b7      [0 2 3 5 a]   R b2 m3 #5 b7    [0 1 3 8 a]
            'R 2 5 b7 7'       : (1, [0,2,7,10,11],  ['#','13','s2']),            # R 4 #5 6 b7      [0 5 8 9 a]   R m3 M3 4 5      [0 3 4 5 7]   R b2 2 M3 6      [0 1 2 4 9]   R b2 m3 #5 7     [0 1 3 8 b]
            'R 2 #5 6 b7'      : (0, [0,2,8,9,10],   ['+','13','s2']),            # R b5 5 #5 b7     [0 6 7 8 a]   R b2 2 M3 b5     [0 1 2 4 6]   R b2 m3 4 7      [0 1 3 5 b]   R 2 M3 b7 7      [0 2 4 a b]
            'R 2 #5 6 7'       : (3, [0,2,8,9,11],   ['+','M','13','s2']),        # R b5 5 6 b7      [0 6 7 9 a]   R b2 m3 M3 b5    [0 1 3 4 6]   R 2 m3 4 7       [0 2 3 5 b]   R b2 m3 6 b7     [0 1 3 9 a]
            'R 2 #5 b7 7'      : (1, [0,2,8,10,11],  ['+','#','13','s2']),        # R b5 #5 6 b7     [0 6 8 9 a]   R 2 m3 M3 b5     [0 2 3 4 6]   R b2 2 M3 b7     [0 1 2 4 a]   R b2 m3 6 7      [0 1 3 9 b]
            'R 2 6 b7 7'       : (3, [0,2,9,10,11],  ['#','13','13','s2']),       # R 5 #5 6 b7      [0 7 8 9 a]   R b2 2 m3 4      [0 1 2 3 5]   R b2 2 M3 7      [0 1 2 4 b]   R b2 m3 b7 7     [0 1 3 a b]
            'R m3 M3 4 b5'     : (3, [0,3,4,5,6],    ['#2','4','b5']),            # R b2 2 m3 6      [0 1 2 3 9]   R b2 2 #5 7      [0 1 2 8 b]   R b2 5 b7 7      [0 1 7 a b]   R b5 6 b7 7      [0 6 9 a b]
            'R m3 M3 4 5'      : (3, [0,3,4,5,7],    ['#2','4']),                 # R b2 2 M3 6      [0 1 2 4 9]   R b2 m3 #5 7     [0 1 3 8 b]   R 2 5 b7 7       [0 2 7 a b]   R 4 #5 6 b7      [0 5 8 9 a]
            'R m3 M3 4 #5'     : (2, [0,3,4,5,8],    ['+','#2','4']),             # R b2 2 4 6       [0 1 2 5 9]   R b2 M3 #5 7     [0 1 4 8 b]   R m3 5 b7 7      [0 3 7 a b]   R M3 5 #5 6      [0 4 7 8 9]
            'R m3 M3 4 6'      : (2, [0,3,4,5,9],    ['#2','4','6','x']),         # R b2 2 b5 6      [0 1 2 6 9]   R b2 4 #5 7      [0 1 5 8 b]   R M3 5 b7 7      [0 4 7 a b]   R m3 b5 5 #5     [0 3 6 7 8]
            'R m3 M3 4 b7'     : (0, [0,3,4,5,10],   ['11','#9','x']),            # R b2 2 5 6       [0 1 2 7 9]   R b2 b5 #5 7     [0 1 6 8 b]   R 4 5 b7 7       [0 5 7 a b]   R 2 4 b5 5       [0 2 5 6 7]
            'R m3 M3 4 7'      : (0, [0,3,4,5,11],   ['M','11','#9','x']),        # R b2 2 #5 6      [0 1 2 8 9]   R b2 5 #5 7      [0 1 7 8 b]   R b5 5 b7 7      [0 6 7 a b]   R b2 M3 4 b5     [0 1 4 5 6]
            'R m3 M3 b5 5'     : (3, [0,3,4,6,7],    ['#2','#4']),                # R b2 m3 M3 6     [0 1 3 4 9]   R 2 m3 #5 7      [0 2 3 8 b]   R b2 b5 6 b7     [0 1 6 9 a]   R 4 #5 6 7       [0 5 8 9 b]
            'R m3 M3 b5 #5'    : (3, [0,3,4,6,8],    ['o','+','#9']),             # R b2 m3 4 6      [0 1 3 5 9]   R 2 M3 #5 7      [0 2 4 8 b]   R 2 b5 6 b7      [0 2 6 9 a]   R M3 5 #5 b7     [0 4 7 8 a]
            'R m3 M3 b5 6'     : (3, [0,3,4,6,9],    ['#2','b5','6']),            # R b2 m3 b5 6     [0 1 3 6 9]   R 2 4 #5 7       [0 2 5 8 b]   R m3 b5 6 b7     [0 3 6 9 a]   R m3 b5 5 6      [0 3 6 7 9]
            'R m3 M3 b5 b7'    : (1, [0,3,4,6,10],   ['#','11','#9','x']),        # R b2 m3 5 6      [0 1 3 7 9]   R 2 b5 #5 7      [0 2 6 8 b]   R M3 b5 6 b7     [0 4 6 9 a]   R 2 4 b5 #5      [0 2 5 6 8]
            'R m3 M3 b5 7'     : (0, [0,3,4,6,11],   ['o','M','#9']),             # R b2 m3 #5 6     [0 1 3 8 9]   R 2 5 #5 7       [0 2 7 8 b]   R 4 b5 6 b7      [0 5 6 9 a]   R b2 M3 4 5      [0 1 4 5 7]
            'R m3 M3 5 #5'     : (2, [0,3,4,7,8],    ['#2','b6']),                # R b2 M3 4 6      [0 1 4 5 9]   R m3 M3 #5 7     [0 3 4 8 b]   R b2 4 #5 6      [0 1 5 8 9]   R M3 5 #5 7      [0 4 7 8 b]
            'R m3 M3 5 6'      : (2, [0,3,4,7,9],    ['#2','6']),                 # R b2 M3 b5 6     [0 1 4 6 9]   R m3 4 #5 7      [0 3 5 8 b]   R 2 4 #5 6       [0 2 5 8 9]   R m3 b5 5 b7     [0 3 6 7 a]
            'R m3 M3 5 b7'     : (0, [0,3,4,7,10],   ['#9']),                     # R b2 M3 5 6      [0 1 4 7 9]   R m3 b5 #5 7     [0 3 6 8 b]   R m3 4 #5 6      [0 3 5 8 9]   R 2 4 b5 6       [0 2 5 6 9]
            'R m3 M3 5 7'      : (0, [0,3,4,7,11],   ['M','#9']),                 # R b2 M3 #5 6     [0 1 4 8 9]   R m3 5 #5 7      [0 3 7 8 b]   R M3 4 #5 6      [0 4 5 8 9]   R b2 M3 4 #5     [0 1 4 5 8]
            'R m3 M3 #5 6'     : (3, [0,3,4,8,9],    ['+','#2','6']),             # R b2 4 b5 6      [0 1 5 6 9]   R M3 4 #5 7      [0 4 5 8 b]   R b2 M3 5 #5     [0 1 4 7 8]   R m3 b5 5 7      [0 3 6 7 b]
            'R m3 M3 #5 b7'    : (0, [0,3,4,8,10],   ['+','#9']),                 # R b2 4 5 6       [0 1 5 7 9]   R M3 b5 #5 7     [0 4 6 8 b]   R 2 M3 5 #5      [0 2 4 7 8]   R 2 4 b5 b7      [0 2 5 6 a]
            'R m3 M3 #5 7'     : (1, [0,3,4,8,11],   ['+','M','#9']),             # R b2 4 #5 6      [0 1 5 8 9]   R M3 5 #5 7      [0 4 7 8 b]   R m3 M3 5 #5     [0 3 4 7 8]   R b2 M3 4 6      [0 1 4 5 9]
            'R m3 M3 6 b7'     : (0, [0,3,4,9,10],   ['13','#9','x']),            # R b2 b5 5 6      [0 1 6 7 9]   R 4 b5 #5 7      [0 5 6 8 b]   R b2 m3 b5 5     [0 1 3 6 7]   R 2 4 b5 7       [0 2 5 6 b]
            'R m3 M3 6 7'      : (1, [0,3,4,9,11],   ['M','13','#9','x']),        # R b2 b5 #5 6     [0 1 6 8 9]   R 4 5 #5 7       [0 5 7 8 b]   R 2 m3 b5 5      [0 2 3 6 7]   R b2 M3 4 b7     [0 1 4 5 a]
            'R m3 M3 b7 7'     : (0, [0,3,4,10,11],  ['#','13','#9','x']),        # R b2 5 #5 6      [0 1 7 8 9]   R b5 5 #5 7      [0 6 7 8 b]   R b2 2 4 b5      [0 1 2 5 6]   R b2 M3 4 7      [0 1 4 5 b]
            'R m3 4 b5 5'      : (1, [0,3,5,6,7],    ['o','4','5']),              # R 2 m3 M3 6      [0 2 3 4 9]   R b2 2 5 b7      [0 1 2 7 a]   R b2 b5 6 7      [0 1 6 9 b]   R 4 #5 b7 7      [0 5 8 a b]
            'R m3 4 b5 #5'     : (3, [0,3,5,6,8],    ['o','+','4']),              # R 2 m3 4 6       [0 2 3 5 9]   R b2 m3 5 b7     [0 1 3 7 a]   R 2 b5 6 7       [0 2 6 9 b]   R M3 5 6 b7      [0 4 7 9 a]
            'R m3 4 b5 6'      : (4, [0,3,5,6,9],    ['o','4','6']),              # R 2 m3 b5 6      [0 2 3 6 9]   R b2 M3 5 b7     [0 1 4 7 a]   R m3 b5 6 7      [0 3 6 9 b]   R m3 b5 #5 6     [0 3 6 8 9]
            'R m3 4 b5 b7'     : (0, [0,3,5,6,10],   ['o','11']),                 # R 2 m3 5 6       [0 2 3 7 9]   R b2 4 5 b7      [0 1 5 7 a]   R M3 b5 6 7      [0 4 6 9 b]   R 2 4 5 #5       [0 2 5 7 8]
            'R m3 4 b5 7'      : (0, [0,3,5,6,11],   ['o','M','11']),             # R 2 m3 #5 6      [0 2 3 8 9]   R b2 b5 5 b7     [0 1 6 7 a]   R 4 b5 6 7       [0 5 6 9 b]   R b2 M3 b5 5     [0 1 4 6 7]
            'R m3 4 5 #5'      : (4, [0,3,5,7,8],    ['m','+','4']),              # R 2 M3 4 6       [0 2 4 5 9]   R 2 m3 5 b7      [0 2 3 7 a]   R b2 4 #5 b7     [0 1 5 8 a]   R M3 5 6 7       [0 4 7 9 b]
            'R m3 4 5 6'       : (2, [0,3,5,7,9],    ['m','4','6']),              # R 2 M3 b5 6      [0 2 4 6 9]   R 2 M3 5 b7      [0 2 4 7 a]   R 2 4 #5 b7      [0 2 5 8 a]   R m3 b5 #5 b7    [0 3 6 8 a]
            'R m3 4 5 b7'      : (0, [0,3,5,7,10],   ['m','11']),                 # R 2 M3 5 6       [0 2 4 7 9]   R 2 4 5 b7       [0 2 5 7 a]   R m3 4 #5 b7     [0 3 5 8 a]   R 2 4 5 6        [0 2 5 7 9]
            'R m3 4 5 7'       : (1, [0,3,5,7,11],   ['m','M','11']),             # R 2 M3 #5 6      [0 2 4 8 9]   R 2 b5 5 b7      [0 2 6 7 a]   R M3 4 #5 b7     [0 4 5 8 a]   R b2 M3 b5 #5    [0 1 4 6 8]
            'R m3 4 #5 6'      : (4, [0,3,5,8,9],    ['m','+','4','6']),          # R 2 4 b5 6       [0 2 5 6 9]   R m3 M3 5 b7     [0 3 4 7 a]   R b2 M3 5 6      [0 1 4 7 9]   R m3 b5 #5 7     [0 3 6 8 b]
            'R m3 4 #5 b7'     : (4, [0,3,5,8,10],   ['m','+','11']),             # R 2 4 5 6        [0 2 5 7 9]   R m3 4 5 b7      [0 3 5 7 a]   R 2 M3 5 6       [0 2 4 7 9]   R 2 4 5 b7       [0 2 5 7 a]
            'R m3 4 #5 7'      : (1, [0,3,5,8,11],   ['m','M','+','11']),         # R 2 4 #5 6       [0 2 5 8 9]   R m3 b5 5 b7     [0 3 6 7 a]   R m3 M3 5 6      [0 3 4 7 9]   R b2 M3 b5 6     [0 1 4 6 9]
            'R m3 4 6 b7'      : (1, [0,3,5,9,10],   ['m','13','11','x']),        # R 2 b5 5 6       [0 2 6 7 9]   R M3 4 5 b7      [0 4 5 7 a]   R b2 m3 b5 #5    [0 1 3 6 8]   R 2 4 5 7        [0 2 5 7 b]
            'R m3 4 6 7'       : (2, [0,3,5,9,11],   ['m','M','13','11','x']),    # R 2 b5 #5 6      [0 2 6 8 9]   R M3 b5 5 b7     [0 4 6 7 a]   R 2 m3 b5 #5     [0 2 3 6 8]   R b2 M3 b5 b7    [0 1 4 6 a]
            'R m3 4 b7 7'      : (1, [0,3,5,10,11],  ['m','#','13','11','x']),    # R 2 5 #5 6       [0 2 7 8 9]   R 4 b5 5 b7      [0 5 6 7 a]   R b2 2 4 5       [0 1 2 5 7]   R b2 M3 b5 7     [0 1 4 6 b]
            'R m3 b5 5 #5'     : (3, [0,3,6,7,8],    ['m','#4','b6']),            # R m3 M3 4 6      [0 3 4 5 9]   R b2 2 b5 6      [0 1 2 6 9]   R b2 4 #5 7      [0 1 5 8 b]   R M3 5 b7 7      [0 4 7 a b]
            'R m3 b5 5 6'      : (4, [0,3,6,7,9],    ['m','#4','6']),             # R m3 M3 b5 6     [0 3 4 6 9]   R b2 m3 b5 6     [0 1 3 6 9]   R 2 4 #5 7       [0 2 5 8 b]   R m3 b5 6 b7     [0 3 6 9 a]
            'R m3 b5 5 b7'     : (0, [0,3,6,7,10],   ['m','#','11']),             # R m3 M3 5 6      [0 3 4 7 9]   R b2 M3 b5 6     [0 1 4 6 9]   R m3 4 #5 7      [0 3 5 8 b]   R 2 4 #5 6       [0 2 5 8 9]
            'R m3 b5 5 7'      : (1, [0,3,6,7,11],   ['o','M','7']),              # R m3 M3 #5 6     [0 3 4 8 9]   R b2 4 b5 6      [0 1 5 6 9]   R M3 4 #5 7      [0 4 5 8 b]   R b2 M3 5 #5     [0 1 4 7 8]
            'R m3 b5 #5 6'     : (2, [0,3,6,8,9],    ['o','+','6']),              # R m3 4 b5 6      [0 3 5 6 9]   R 2 m3 b5 6      [0 2 3 6 9]   R b2 M3 5 b7     [0 1 4 7 a]   R m3 b5 6 7      [0 3 6 9 b]
            'R m3 b5 #5 b7'    : (1, [0,3,6,8,10],   ['o','+','7']),              # R m3 4 5 6       [0 3 5 7 9]   R 2 M3 b5 6      [0 2 4 6 9]   R 2 M3 5 b7      [0 2 4 7 a]   R 2 4 #5 b7      [0 2 5 8 a]
            'R m3 b5 #5 7'     : (1, [0,3,6,8,11],   ['o','+','M','7']),          # R m3 4 #5 6      [0 3 5 8 9]   R 2 4 b5 6       [0 2 5 6 9]   R m3 M3 5 b7     [0 3 4 7 a]   R b2 M3 5 6      [0 1 4 7 9]
            'R m3 b5 6 b7'     : (0, [0,3,6,9,10],   ['o','13']),                 # R m3 b5 5 6      [0 3 6 7 9]   R m3 M3 b5 6     [0 3 4 6 9]   R b2 m3 b5 6     [0 1 3 6 9]   R 2 4 #5 7       [0 2 5 8 b]
            'R m3 b5 6 7'      : (1, [0,3,6,9,11],   ['o','M','13']),             # R m3 b5 #5 6     [0 3 6 8 9]   R m3 4 b5 6      [0 3 5 6 9]   R 2 m3 b5 6      [0 2 3 6 9]   R b2 M3 5 b7     [0 1 4 7 a]
            'R m3 b5 b7 7'     : (1, [0,3,6,10,11],  ['o','#','13']),             # R m3 5 #5 6      [0 3 7 8 9]   R M3 4 b5 6      [0 4 5 6 9]   R b2 2 4 #5      [0 1 2 5 8]   R b2 M3 5 7      [0 1 4 7 b]
            'R m3 5 #5 6'      : (4, [0,3,7,8,9],    ['m','b6','6']),             # R M3 4 b5 6      [0 4 5 6 9]   R b2 2 4 #5      [0 1 2 5 8]   R b2 M3 5 7      [0 1 4 7 b]   R m3 b5 b7 7     [0 3 6 a b]
            'R m3 5 #5 b7'     : (1, [0,3,7,8,10],   ['m','b','13']),             # R M3 4 5 6       [0 4 5 7 9]   R b2 m3 4 #5     [0 1 3 5 8]   R 2 M3 5 7       [0 2 4 7 b]   R 2 4 6 b7       [0 2 5 9 a]
            'R m3 5 #5 7'      : (1, [0,3,7,8,11],   ['m','M','b','13']),         # R M3 4 #5 6      [0 4 5 8 9]   R b2 M3 4 #5     [0 1 4 5 8]   R m3 M3 5 7      [0 3 4 7 b]   R b2 M3 #5 6     [0 1 4 8 9]
            'R m3 5 6 b7'      : (0, [0,3,7,9,10],   ['m','13']),                 # R M3 b5 5 6      [0 4 6 7 9]   R 2 m3 4 #5      [0 2 3 5 8]   R b2 m3 b5 b7    [0 1 3 6 a]   R 2 4 6 7        [0 2 5 9 b]
            'R m3 5 6 7'       : (1, [0,3,7,9,11],   ['m','M','13']),             # R M3 b5 #5 6     [0 4 6 8 9]   R 2 M3 4 #5      [0 2 4 5 8]   R 2 m3 b5 b7     [0 2 3 6 a]   R b2 M3 #5 b7    [0 1 4 8 a]
            'R m3 5 b7 7'      : (0, [0,3,7,10,11],  ['m','#','13']),             # R M3 5 #5 6      [0 4 7 8 9]   R m3 M3 4 #5     [0 3 4 5 8]   R b2 2 4 6       [0 1 2 5 9]   R b2 M3 #5 7     [0 1 4 8 b]
            'R m3 #5 6 b7'     : (0, [0,3,8,9,10],   ['m','+','13']),             # R 4 b5 5 6       [0 5 6 7 9]   R b2 2 M3 5      [0 1 2 4 7]   R b2 m3 b5 7     [0 1 3 6 b]   R 2 4 b7 7       [0 2 5 a b]
            'R m3 #5 6 7'      : (3, [0,3,8,9,11],   ['m','+','M','13']),         # R 4 b5 #5 6      [0 5 6 8 9]   R b2 m3 M3 5     [0 1 3 4 7]   R 2 m3 b5 7      [0 2 3 6 b]   R b2 M3 6 b7     [0 1 4 9 a]
            'R m3 #5 b7 7'     : (2, [0,3,8,10,11],  ['m','+','#','13']),         # R 4 5 #5 6       [0 5 7 8 9]   R 2 m3 M3 5      [0 2 3 4 7]   R b2 2 4 b7      [0 1 2 5 a]   R b2 M3 6 7      [0 1 4 9 b]
            'R m3 6 b7 7'      : (2, [0,3,9,10,11],  ['m','6','#','13','x']),     # R b5 5 #5 6      [0 6 7 8 9]   R b2 2 m3 b5     [0 1 2 3 6]   R b2 2 4 7       [0 1 2 5 b]   R b2 M3 b7 7     [0 1 4 a b]
            'R M3 4 b5 5'      : (3, [0,4,5,6,7],    ['4','#4']),                 # R b2 2 m3 #5     [0 1 2 3 8]   R b2 2 5 7       [0 1 2 7 b]   R b2 b5 b7 7     [0 1 6 a b]   R 4 6 b7 7       [0 5 9 a b]
            'R M3 4 b5 #5'     : (3, [0,4,5,6,8],    ['o','+','4']),              # R b2 2 M3 #5     [0 1 2 4 8]   R b2 m3 5 7      [0 1 3 7 b]   R 2 b5 b7 7      [0 2 6 a b]   R M3 #5 6 b7     [0 4 8 9 a]
            'R M3 4 b5 6'      : (3, [0,4,5,6,9],    ['4','b5','6']),             # R b2 2 4 #5      [0 1 2 5 8]   R b2 M3 5 7      [0 1 4 7 b]   R m3 b5 b7 7     [0 3 6 a b]   R m3 5 #5 6      [0 3 7 8 9]
            'R M3 4 b5 b7'     : (0, [0,4,5,6,10],   ['11','b5']),                # R b2 2 b5 #5     [0 1 2 6 8]   R b2 4 5 7       [0 1 5 7 b]   R M3 b5 b7 7     [0 4 6 a b]   R 2 b5 5 #5      [0 2 6 7 8]
            'R M3 4 b5 7'      : (0, [0,4,5,6,11],   ['M','11','b5']),            # R b2 2 5 #5      [0 1 2 7 8]   R b2 b5 5 7      [0 1 6 7 b]   R 4 b5 b7 7      [0 5 6 a b]   R b2 4 b5 5      [0 1 5 6 7]
            'R M3 4 5 #5'      : (2, [0,4,5,7,8],    ['4','b6']),                 # R b2 m3 M3 #5    [0 1 3 4 8]   R 2 m3 5 7       [0 2 3 7 b]   R b2 4 6 b7      [0 1 5 9 a]   R M3 #5 6 7      [0 4 8 9 b]
            'R M3 4 5 6'       : (2, [0,4,5,7,9],    ['4','6']),                  # R b2 m3 4 #5     [0 1 3 5 8]   R 2 M3 5 7       [0 2 4 7 b]   R 2 4 6 b7       [0 2 5 9 a]   R m3 5 #5 b7     [0 3 7 8 a]
            'R M3 4 5 b7'      : (0, [0,4,5,7,10],   ['11']),                     # R b2 m3 b5 #5    [0 1 3 6 8]   R 2 4 5 7        [0 2 5 7 b]   R m3 4 6 b7      [0 3 5 9 a]   R 2 b5 5 6       [0 2 6 7 9]
            'R M3 4 5 7'       : (1, [0,4,5,7,11],   ['M','11']),                 # R b2 m3 5 #5     [0 1 3 7 8]   R 2 b5 5 7       [0 2 6 7 b]   R M3 4 6 b7      [0 4 5 9 a]   R b2 4 b5 #5     [0 1 5 6 8]
            'R M3 4 #5 6'      : (2, [0,4,5,8,9],    ['+','4','6']),              # R b2 M3 4 #5     [0 1 4 5 8]   R m3 M3 5 7      [0 3 4 7 b]   R b2 M3 #5 6     [0 1 4 8 9]   R m3 5 #5 7      [0 3 7 8 b]
            'R M3 4 #5 b7'     : (0, [0,4,5,8,10],   ['+','11']),                 # R b2 M3 b5 #5    [0 1 4 6 8]   R m3 4 5 7       [0 3 5 7 b]   R 2 M3 #5 6      [0 2 4 8 9]   R 2 b5 5 b7      [0 2 6 7 a]
            'R M3 4 #5 7'      : (0, [0,4,5,8,11],   ['M','b','13','11']),        # R b2 M3 5 #5     [0 1 4 7 8]   R m3 b5 5 7      [0 3 6 7 b]   R m3 M3 #5 6     [0 3 4 8 9]   R b2 4 b5 6      [0 1 5 6 9]
            'R M3 4 6 b7'      : (0, [0,4,5,9,10],   ['13','11','x']),            # R b2 4 b5 #5     [0 1 5 6 8]   R M3 4 5 7       [0 4 5 7 b]   R b2 m3 5 #5     [0 1 3 7 8]   R 2 b5 5 7       [0 2 6 7 b]
            'R M3 4 6 7'       : (1, [0,4,5,9,11],   ['M','13','11','x']),        # R b2 4 5 #5      [0 1 5 7 8]   R M3 b5 5 7      [0 4 6 7 b]   R 2 m3 5 #5      [0 2 3 7 8]   R b2 4 b5 b7     [0 1 5 6 a]
            'R M3 4 b7 7'      : (0, [0,4,5,10,11],  ['#','13','11','x']),        # R b2 b5 5 #5     [0 1 6 7 8]   R 4 b5 5 7       [0 5 6 7 b]   R b2 2 b5 5      [0 1 2 6 7]   R b2 4 b5 7      [0 1 5 6 b]
            'R M3 b5 5 #5'     : (3, [0,4,6,7,8],    ['#4','b6']),                # R 2 m3 M3 #5     [0 2 3 4 8]   R b2 2 b5 b7     [0 1 2 6 a]   R b2 4 6 7       [0 1 5 9 b]   R M3 #5 b7 7     [0 4 8 a b]
            'R M3 b5 5 6'      : (3, [0,4,6,7,9],    ['#4','6']),                 # R 2 m3 4 #5      [0 2 3 5 8]   R b2 m3 b5 b7    [0 1 3 6 a]   R 2 4 6 7        [0 2 5 9 b]   R m3 5 6 b7      [0 3 7 9 a]
            'R M3 b5 5 b7'     : (0, [0,4,6,7,10],   ['#','11]']),                # R 2 m3 b5 #5     [0 2 3 6 8]   R b2 M3 b5 b7    [0 1 4 6 a]   R m3 4 6 7       [0 3 5 9 b]   R 2 b5 #5 6      [0 2 6 8 9]
            'R M3 b5 5 7'      : (0, [0,4,6,7,11],   ['M','#','11']),             # R 2 m3 5 #5      [0 2 3 7 8]   R b2 4 b5 b7     [0 1 5 6 a]   R M3 4 6 7       [0 4 5 9 b]   R b2 4 5 #5      [0 1 5 7 8]
            'R M3 b5 #5 6'     : (4, [0,4,6,8,9],    ['b5','+','6']),             # R 2 M3 4 #5      [0 2 4 5 8]   R 2 m3 b5 b7     [0 2 3 6 a]   R b2 M3 #5 b7    [0 1 4 8 a]   R m3 5 6 7       [0 3 7 9 b]
            'R M3 b5 #5 b7'    : (2, [0,4,6,8,10],   ['+','#','11']),             # R 2 M3 b5 #5     [0 2 4 6 8]   R 2 M3 b5 b7     [0 2 4 6 a]   R 2 M3 #5 b7     [0 2 4 8 a]   R 2 b5 #5 b7     [0 2 6 8 a]
            'R M3 b5 #5 7'     : (1, [0,4,6,8,11],   ['+','M','#','11']),         # R 2 M3 5 #5      [0 2 4 7 8]   R 2 4 b5 b7      [0 2 5 6 a]   R m3 M3 #5 b7    [0 3 4 8 a]   R b2 4 5 6       [0 1 5 7 9]
            'R M3 b5 6 b7'     : (0, [0,4,6,9,10],   ['13','b5']),                # R 2 4 b5 #5      [0 2 5 6 8]   R m3 M3 b5 b7    [0 3 4 6 a]   R b2 m3 5 6      [0 1 3 7 9]   R 2 b5 #5 7      [0 2 6 8 b]
            'R M3 b5 6 7'      : (1, [0,4,6,9,11],   ['M','13','b5']),            # R 2 4 5 #5       [0 2 5 7 8]   R m3 4 b5 b7     [0 3 5 6 a]   R 2 m3 5 6       [0 2 3 7 9]   R b2 4 5 b7      [0 1 5 7 a]
            'R M3 b5 b7 7'     : (1, [0,4,6,10,11],  ['#','13','#','11']),        # R 2 b5 5 #5      [0 2 6 7 8]   R M3 4 b5 b7     [0 4 5 6 a]   R b2 2 b5 #5     [0 1 2 6 8]   R b2 4 5 7       [0 1 5 7 b]
            'R M3 5 #5 6'      : (3, [0,4,7,8,9],    ['b6','6']),                 # R m3 M3 4 #5     [0 3 4 5 8]   R b2 2 4 6       [0 1 2 5 9]   R b2 M3 #5 7     [0 1 4 8 b]   R m3 5 b7 7      [0 3 7 a b]
            'R M3 5 #5 b7'     : (0, [0,4,7,8,10],   ['b','13']),                 # R m3 M3 b5 #5    [0 3 4 6 8]   R b2 m3 4 6      [0 1 3 5 9]   R 2 M3 #5 7      [0 2 4 8 b]   R 2 b5 6 b7      [0 2 6 9 a]
            'R M3 5 #5 7'      : (0, [0,4,7,8,11],   ['M','b','13']),             # R m3 M3 5 #5     [0 3 4 7 8]   R b2 M3 4 6      [0 1 4 5 9]   R m3 M3 #5 7     [0 3 4 8 b]   R b2 4 #5 6      [0 1 5 8 9]
            'R M3 5 6 b7'      : (0, [0,4,7,9,10],   ['13']),                     # R m3 4 b5 #5     [0 3 5 6 8]   R 2 m3 4 6       [0 2 3 5 9]   R b2 m3 5 b7     [0 1 3 7 a]   R 2 b5 6 7       [0 2 6 9 b]
            'R M3 5 6 7'       : (1, [0,4,7,9,11],   ['M','13']),                 # R m3 4 5 #5      [0 3 5 7 8]   R 2 M3 4 6       [0 2 4 5 9]   R 2 m3 5 b7      [0 2 3 7 a]   R b2 4 #5 b7     [0 1 5 8 a]
            'R M3 5 b7 7'      : (0, [0,4,7,10,11],  ['#','13']),                 # R m3 b5 5 #5     [0 3 6 7 8]   R m3 M3 4 6      [0 3 4 5 9]   R b2 2 b5 6      [0 1 2 6 9]   R b2 4 #5 7      [0 1 5 8 b]
            'R M3 #5 6 b7'     : (0, [0,4,8,9,10],   ['+','13']),                 # R M3 4 b5 #5     [0 4 5 6 8]   R b2 2 M3 #5     [0 1 2 4 8]   R b2 m3 5 7      [0 1 3 7 b]   R 2 b5 b7 7      [0 2 6 a b]
            'R M3 #5 6 7'      : (0, [0,4,8,9,11],   ['+','M','13']),             # R M3 4 5 #5      [0 4 5 7 8]   R b2 m3 M3 #5    [0 1 3 4 8]   R 2 m3 5 7       [0 2 3 7 b]   R b2 4 6 b7      [0 1 5 9 a]
            'R M3 #5 b7 7'     : (0, [0,4,8,10,11],  ['+','#','13']),             # R M3 b5 5 #5     [0 4 6 7 8]   R 2 m3 M3 #5     [0 2 3 4 8]   R b2 2 b5 b7     [0 1 2 6 a]   R b2 4 6 7       [0 1 5 9 b]
            'R M3 6 b7 7'      : (1, [0,4,9,10,11],  ['#','13','13','x']),        # R 4 b5 5 #5      [0 5 6 7 8]   R b2 2 m3 5      [0 1 2 3 7]   R b2 2 b5 7      [0 1 2 6 b]   R b2 4 b7 7      [0 1 5 a b]
            'R 4 b5 5 #5'      : (2, [0,5,6,7,8],    ['#4','b6','s4']),           # R b2 2 m3 5      [0 1 2 3 7]   R b2 2 b5 7      [0 1 2 6 b]   R b2 4 b7 7      [0 1 5 a b]   R M3 6 b7 7      [0 4 9 a b]
            'R 4 b5 5 6'       : (3, [0,5,6,7,9],    ['#4','6','s4']),            # R b2 2 M3 5      [0 1 2 4 7]   R b2 m3 b5 7     [0 1 3 6 b]   R 2 4 b7 7       [0 2 5 a b]   R m3 #5 6 b7     [0 3 8 9 a]
            'R 4 b5 5 b7'      : (2, [0,5,6,7,10],   ['o','#','11','s4']),        # R b2 2 4 5       [0 1 2 5 7]   R b2 M3 b5 7     [0 1 4 6 b]   R m3 4 b7 7      [0 3 5 a b]   R 2 5 #5 6       [0 2 7 8 9]
            'R 4 b5 5 7'       : (1, [0,5,6,7,11],   ['M','#','11','s4']),        # R b2 2 b5 5      [0 1 2 6 7]   R b2 4 b5 7      [0 1 5 6 b]   R M3 4 b7 7      [0 4 5 a b]   R b2 b5 5 #5     [0 1 6 7 8]
            'R 4 b5 #5 6'      : (2, [0,5,6,8,9],    ['o','+','6','s4']),         # R b2 m3 M3 5     [0 1 3 4 7]   R 2 m3 b5 7      [0 2 3 6 b]   R b2 M3 6 b7     [0 1 4 9 a]   R m3 #5 6 7      [0 3 8 9 b]
            'R 4 b5 #5 b7'     : (3, [0,5,6,8,10],   ['o','+','7','s4']),         # R b2 m3 4 5      [0 1 3 5 7]   R 2 M3 b5 7      [0 2 4 6 b]   R 2 M3 6 b7      [0 2 4 9 a]   R 2 5 #5 b7      [0 2 7 8 a]
            'R 4 b5 #5 7'      : (1, [0,5,6,8,11],   ['o','+','M','7','s4']),     # R b2 m3 b5 5     [0 1 3 6 7]   R 2 4 b5 7       [0 2 5 6 b]   R m3 M3 6 b7     [0 3 4 9 a]   R b2 b5 5 6      [0 1 6 7 9]
            'R 4 b5 6 b7'      : (1, [0,5,6,9,10],   ['o','13','s4']),            # R b2 M3 4 5      [0 1 4 5 7]   R m3 M3 b5 7     [0 3 4 6 b]   R b2 m3 #5 6     [0 1 3 8 9]   R 2 5 #5 7       [0 2 7 8 b]
            'R 4 b5 6 7'       : (1, [0,5,6,9,11],   ['o','M','13','s4']),        # R b2 M3 b5 5     [0 1 4 6 7]   R m3 4 b5 7      [0 3 5 6 b]   R 2 m3 #5 6      [0 2 3 8 9]   R b2 b5 5 b7     [0 1 6 7 a]
            'R 4 b5 b7 7'      : (1, [0,5,6,10,11],  ['o','#','13','s4']),        # R b2 4 b5 5      [0 1 5 6 7]   R M3 4 b5 7      [0 4 5 6 b]   R b2 2 5 #5      [0 1 2 7 8]   R b2 b5 5 7      [0 1 6 7 b]
            'R 4 5 #5 6'       : (4, [0,5,7,8,9],    ['b6','6','s4']),            # R 2 m3 M3 5      [0 2 3 4 7]   R b2 2 4 b7      [0 1 2 5 a]   R b2 M3 6 7      [0 1 4 9 b]   R m3 #5 b7 7     [0 3 8 a b]
            'R 4 5 #5 b7'      : (3, [0,5,7,8,10],   ['b','13','s4']),            # R 2 m3 4 5       [0 2 3 5 7]   R b2 m3 4 b7     [0 1 3 5 a]   R 2 M3 6 7       [0 2 4 9 b]   R 2 5 6 b7       [0 2 7 9 a]
            'R 4 5 #5 7'       : (2, [0,5,7,8,11],   ['M','b','13','s4']),        # R 2 m3 b5 5      [0 2 3 6 7]   R b2 M3 4 b7     [0 1 4 5 a]   R m3 M3 6 7      [0 3 4 9 b]   R b2 b5 #5 6     [0 1 6 8 9]
            'R 4 5 6 b7'       : (1, [0,5,7,9,10],   ['13','s4']),                # R 2 M3 4 5       [0 2 4 5 7]   R 2 m3 4 b7      [0 2 3 5 a]   R b2 m3 #5 b7    [0 1 3 8 a]   R 2 5 6 7        [0 2 7 9 b]
            'R 4 5 6 7'        : (3, [0,5,7,9,11],   ['M','13','s4']),            # R 2 M3 b5 5      [0 2 4 6 7]   R 2 M3 4 b7      [0 2 4 5 a]   R 2 m3 #5 b7     [0 2 3 8 a]   R b2 b5 #5 b7    [0 1 6 8 a]
            'R 4 5 b7 7'       : (2, [0,5,7,10,11],  ['#','13','s4']),            # R 2 4 b5 5       [0 2 5 6 7]   R m3 M3 4 b7     [0 3 4 5 a]   R b2 2 5 6       [0 1 2 7 9]   R b2 b5 #5 7     [0 1 6 8 b]
            'R 4 #5 6 b7'      : (2, [0,5,8,9,10],   ['+','13','s4']),            # R m3 M3 4 5      [0 3 4 5 7]   R b2 2 M3 6      [0 1 2 4 9]   R b2 m3 #5 7     [0 1 3 8 b]   R 2 5 b7 7       [0 2 7 a b]
            'R 4 #5 6 7'       : (1, [0,5,8,9,11],   ['+','M','13','s4']),        # R m3 M3 b5 5     [0 3 4 6 7]   R b2 m3 M3 6     [0 1 3 4 9]   R 2 m3 #5 7      [0 2 3 8 b]   R b2 b5 6 b7     [0 1 6 9 a]
            'R 4 #5 b7 7'      : (3, [0,5,8,10,11],  ['+','#','13','s4']),        # R m3 4 b5 5      [0 3 5 6 7]   R 2 m3 M3 6      [0 2 3 4 9]   R b2 2 5 b7      [0 1 2 7 a]   R b2 b5 6 7      [0 1 6 9 b]
            'R 4 6 b7 7'       : (2, [0,5,9,10,11],  ['#','13','13','s4']),       # R M3 4 b5 5      [0 4 5 6 7]   R b2 2 m3 #5     [0 1 2 3 8]   R b2 2 5 7       [0 1 2 7 b]   R b2 b5 b7 7     [0 1 6 a b]
            'R b5 5 #5 6'      : (4, [0,6,7,8,9],    ['#4','b6','6','y']),        # R b2 2 m3 b5     [0 1 2 3 6]   R b2 2 4 7       [0 1 2 5 b]   R b2 M3 b7 7     [0 1 4 a b]   R m3 6 b7 7      [0 3 9 a b]
            'R b5 5 #5 b7'     : (2, [0,6,7,8,10],   ['b13','#11','y']),    # R b2 2 M3 b5     [0 1 2 4 6]   R b2 m3 4 7      [0 1 3 5 b]   R 2 M3 b7 7      [0 2 4 a b]   R 2 #5 6 b7      [0 2 8 9 a]
            'R b5 5 #5 7'      : (2, [0,6,7,8,11],   ['M7','b13','#11','y']),     # R b2 2 4 b5      [0 1 2 5 6]   R b2 M3 4 7      [0 1 4 5 b]   R m3 M3 b7 7     [0 3 4 a b]   R b2 5 #5 6      [0 1 7 8 9]
            'R b5 5 6 b7'      : (1, [0,6,7,9,10],   ['13','#1','y']),        # R b2 m3 M3 b5    [0 1 3 4 6]   R 2 m3 4 7       [0 2 3 5 b]   R b2 m3 6 b7     [0 1 3 9 a]   R 2 #5 6 7       [0 2 8 9 b]
            'R b5 5 6 7'       : (3, [0,6,7,9,11],   ['M','13','#11','y']),    # R b2 m3 4 b5     [0 1 3 5 6]   R 2 M3 4 7       [0 2 4 5 b]   R 2 m3 6 b7      [0 2 3 9 a]   R b2 5 #5 b7     [0 1 7 8 a]
            'R b5 5 b7 7'      : (2, [0,6,7,10,11],  ['7M7','#13','#11','y']),    # R b2 M3 4 b5     [0 1 4 5 6]   R m3 M3 4 7      [0 3 4 5 b]   R b2 2 #5 6      [0 1 2 8 9]   R b2 5 #5 7      [0 1 7 8 b]
            'R b5 #5 6 b7'     : (2, [0,6,8,9,10],   ['+','13','#11','y']),         # R 2 m3 M3 b5     [0 2 3 4 6]   R b2 2 M3 b7     [0 1 2 4 a]   R b2 m3 6 7      [0 1 3 9 b]   R 2 #5 b7 7      [0 2 8 a b]
            'R b5 #5 6 7'      : (2, [0,6,8,9,11],   ['+','b5','M13','y']),         # R 2 m3 4 b5      [0 2 3 5 6]   R b2 m3 M3 b7    [0 1 3 4 a]   R 2 m3 6 7       [0 2 3 9 b]   R b2 5 6 b7      [0 1 7 9 a]
            'R b5 #5 b7 7'     : (4, [0,6,8,10,11],  ['+M7','b13','#11','y']),     # R 2 M3 4 b5      [0 2 4 5 6]   R 2 m3 M3 b7     [0 2 3 4 a]   R b2 2 #5 b7     [0 1 2 8 a]   R b2 5 6 7       [0 1 7 9 b]
            'R b5 6 b7 7'      : (1, [0,6,9,10,11],  ['M7','b5','13','y']),    # R m3 M3 4 b5     [0 3 4 5 6]   R b2 2 m3 6      [0 1 2 3 9]   R b2 2 #5 7      [0 1 2 8 b]   R b2 5 b7 7      [0 1 7 a b]
            'R 5 #5 6 b7'      : (2, [0,7,8,9,10],   ['13','b13','y']),        # R b2 2 m3 4      [0 1 2 3 5]   R b2 2 M3 7      [0 1 2 4 b]   R b2 m3 b7 7     [0 1 3 a b]   R 2 6 b7 7       [0 2 9 a b]
            'R 5 #5 6 7'       : (0, [0,7,8,9,11],   ['M13','b13','y']),             # R b2 2 M3 4      [0 1 2 4 5]   R b2 m3 M3 7     [0 1 3 4 b]   R 2 m3 b7 7      [0 2 3 a b]   R b2 #5 6 b7     [0 1 8 9 a]
            'R 5 #5 b7 7'      : (2, [0,7,8,10,11],  ['M7','b13','y']),         # R b2 m3 M3 4     [0 1 3 4 5]   R 2 m3 M3 7      [0 2 3 4 b]   R b2 2 6 b7      [0 1 2 9 a]   R b2 #5 6 7      [0 1 8 9 b]
            'R 5 6 b7 7'       : (2, [0,7,9,10,11],  ['13','M7','y']),        # R 2 m3 M3 4      [0 2 3 4 5]   R b2 2 m3 b7     [0 1 2 3 a]   R b2 2 6 7       [0 1 2 9 b]   R b2 #5 b7 7     [0 1 8 a b]
            'R #5 6 b7 7'      : (2, [0,8,9,10,11],  ['13','M7','b13','y']),    # R b2 2 m3 M3     [0 1 2 3 4]   R b2 2 m3 7      [0 1 2 3 b]   R b2 2 b7 7      [0 1 2 a b]   R b2 6 b7 7      [0 1 9 a b]
    ####################################################################################################################################################################################################
            'R b2 m3 M3 b5 6'  : (5, [0,1,3,4,6,9],  ['b#2','b5','6']),           # R 2 m3 4 #5 7    [0 2 3 5 8 b] R b2 m3 b5 6 b7  [0 1 3 6 9 a] R 2 4 #5 6 7     [0 2 5 8 9 b] R m3 b5 5 6 b7   [0 3 6 7 9 a] R m3 M3 b5 5 6   [0 3 4 6 7 9]
            'R b2 m3 M3 #5 6'  : (5, [0,1,3,4,8,9],  ['+','b#2','6']),            # R 2 m3 5 #5 7    [0 2 3 7 8 b] R b2 4 b5 6 b7   [0 1 5 6 9 a] R M3 4 #5 6 7    [0 4 5 8 9 b] R b2 M3 4 5 #5   [0 1 4 5 7 8] R m3 M3 b5 5 7   [0 3 4 6 7 b]
            'R b2 m3 4 b5 b7'  : (3, [0,1,3,5,6,10], ['o','11','b9']),            # R 2 M3 4 6 7     [0 2 4 5 9 b] R 2 m3 5 6 b7    [0 2 3 7 9 a] R b2 4 5 #5 b7   [0 1 5 7 8 a] R M3 b5 5 6 7    [0 4 6 7 9 b] R 2 m3 4 5 #5    [0 2 3 5 7 8]
            'R b2 m3 4 5 #5'   : (5, [0,1,3,5,7,8],  ['m','b2','4','b6']),        # R 2 M3 b5 5 7    [0 2 4 6 7 b] R 2 M3 4 6 b7    [0 2 4 5 9 a] R 2 m3 5 #5 b7   [0 2 3 7 8 a] R b2 4 b5 #5 b7  [0 1 5 6 8 a] R M3 4 5 6 7     [0 4 5 7 9 b]
            'R b2 m3 4 #5 b7'  : (1, [0,1,3,5,8,10], ['m','+','11','b9']),        # R 2 M3 5 6 7     [0 2 4 7 9 b] R 2 4 5 6 b7     [0 2 5 7 9 a] R m3 4 5 #5 b7   [0 3 5 7 8 a] R 2 M3 4 5 6     [0 2 4 5 7 9] R 2 m3 4 5 b7    [0 2 3 5 7 a]
            'R b2 m3 b5 #5 b7' : (3, [0,1,3,6,8,10], ['o','+','b9']),             # R 2 4 5 6 7      [0 2 5 7 9 b] R m3 4 5 6 b7    [0 3 5 7 9 a] R 2 M3 b5 5 6    [0 2 4 6 7 9] R 2 M3 4 5 b7    [0 2 4 5 7 a] R 2 m3 4 #5 b7   [0 2 3 5 8 a]
            'R b2 m3 b5 6 b7'  : (2, [0,1,3,6,9,10], ['0','13','b9']),            # R 2 4 #5 6 7     [0 2 5 8 9 b] R m3 b5 5 6 b7   [0 3 6 7 9 a] R m3 M3 b5 5 6   [0 3 4 6 7 9] R b2 m3 M3 b5 6  [0 1 3 4 6 9] R 2 m3 4 #5 7    [0 2 3 5 8 b]
            'R b2 M3 4 5 #5'   : (4, [0,1,4,5,7,8],  ['b2','4','b6']),            # R m3 M3 b5 5 7   [0 3 4 6 7 b] R b2 m3 M3 #5 6  [0 1 3 4 8 9] R 2 m3 5 #5 7    [0 2 3 7 8 b] R b2 4 b5 6 b7   [0 1 5 6 9 a] R M3 4 #5 6 7    [0 4 5 8 9 b]
            'R b2 M3 4 #5 b7'  : (1, [0,1,4,5,8,10], ['+','11','b9']),            # R m3 M3 5 6 7    [0 3 4 7 9 b] R m3 4 5 #5 7    [0 3 5 7 8 b] R 2 M3 4 #5 6    [0 2 4 5 8 9] R 2 m3 b5 5 b7   [0 2 3 6 7 a] R b2 M3 4 #5 b7 [0 1 4 5 8 a]
            'R b2 M3 b5 5 b7'  : (0, [0,1,4,6,7,10], ['#11','b9']),               # R m3 4 b5 6 7    @0 3 5 6 9 b@ R 2 m3 b5 #5 6   @0 2 3 6 8 9@ R b2 M3 b5 5 b7  @0 1 4 6 7 a@ R m3 4 b5 6 7 @0 3 5 6 9 b@ R 2 m3 b5 #5 6 @0 2 3 6 8 9@
            'R b2 M3 b5 #5 6'  : (5, [0,1,4,6,8,9],  ['+','b2','#4','6']),        # R m3 4 5 #5 7    [0 3 5 7 8 b] R 2 M3 4 #5 6    [0 2 4 5 8 9] R 2 m3 b5 5 b7   [0 2 3 6 7 10] R b2 M3 4 #5 b7 [0 1 4 5 8 a] R m3 M3 5 6 7 [0 3 4 7 9 b]
            'R b2 4 b5 #5 b7'  : (4, [0,1,5,6,8,10], ['b#5','b9','s4']),          # R M3 4 5 6 7     [0 4 5 7 9 b] R b2 m3 4 5 #5   [0 1 3 5 7 8] R 2 M3 b5 5 7    [0 2 4 6 7 b] R 2 M3 4 6 b7    [0 2 4 5 9 a] R 2 m3 5 #5 b7   [0 2 3 7 8 a]
            'R b2 4 b5 6 b7'   : (2, [0,1,5,6,9,10], ['b5','13','b9','s4']),      # R M3 4 #5 6 7    [0 4 5 8 9 b] R b2 M3 4 5 #5   [0 1 4 5 7 8] R m3 M3 b5 5 7   [0 3 4 6 7 b] R b2 m3 M3 #5 6  [0 1 3 4 8 9] R 2 m3 5 #5 7    [0 2 3 7 8 b]
            'R b2 4 5 #5 b7'   : (4, [0,1,5,7,8,10], ['b13','b9','s4']),          # R M3 b5 5 6 7    [0 4 6 7 9 b] R 2 m3 4 5 #5    [0 2 3 5 7 8] R b2 m3 4 b5 b7  [0 1 3 5 6 a] R 2 M3 4 6 7     [0 2 4 5 9 b] R 2 m3 5 6 b7    [0 2 3 7 9 a]
            'R 2 m3 4 5 #5'    : (5, [0,2,3,5,7,8],  ['m2','4','b6']),            # R b2 m3 4 b5 b7  [0 1 3 5 6 a] R 2 M3 4 6 7     [0 2 4 5 9 b] R 2 m3 5 6 b7    [0 2 3 7 9 a] R b2 4 5 #5 b7   [0 1 5 7 8 a] R M3 b5 5 6 7    [0 4 6 7 9 b]
            'R 2 m3 4 5 b7'    : (0, [0,2,3,5,7,10], ['m','11','9']),             # R b2 m3 4 #5 b7  [0 1 3 5 8 a] R 2 M3 5 6 7     [0 2 4 7 9 b] R 2 4 5 6 b7     [0 2 5 7 9 a] R m3 4 5 #5 b7   [0 3 5 7 8 a] R 2 M3 4 5 6     [0 2 4 5 7 9]
            'R 2 m3 4 #5 b7'   : (1, [0,2,3,5,8,10], ['m+','11','9']),            # R b2 m3 b5 #5 b7 [0 1 3 6 8 a] R 2 4 5 6 7      [0 2 5 7 9 b] R m3 4 5 6 b7    [0 3 5 7 9 a] R 2 M3 b5 5 6    [0 2 4 6 7 9] R 2 M3 4 5 b7    [0 2 4 5 7 a]
            'R 2 m3 4 #5 7'    : (1, [0,2,3,5,8,11], ['m+','11','9']),            # R b2 m3 b5 6 b7  [0 1 3 6 9 a] R 2 4 #5 6 7     [0 2 5 8 9 b] R m3 b5 5 6 b7   [0 3 6 7 9 a] R m3 M3 b5 5 6   [0 3 4 6 7 9] R b2 m3 M3 b5 6  [0 1 3 4 6 9]
            'R 2 m3 b5 5 b7'   : (0, [0,2,3,6,7,10], ['m9','#11']),               # R b2 M3 4 #5 b7  [0 1 4 5 8 a] R m3 M3 5 6 7    [0 3 4 7 9 b] R m3 4 5 #5 7    [0 3 5 7 8 b] R  2 M3 4 #5 6   [0 2 4 5 8 9] R 2 m3 b5 5 b7 [0 2 3 6 7 a]
            'R 2 m3 b5 #5 6'   : (2, [0,2,3,6,8,9],  ['o+','2','6']),             # R b2 M3 b5 5 b7  @0 1 4 6 7 a@ R m3 4 b5 6 7    @0 3 5 6 9 b@ R 2 m3 b5 #5 6   @0 2 3 6 8 9@ R b2 M3 b5 5 b7  @0 1 4 6 7 a@ R m3 4 b5 6 7 @0 3 5 6 9 b@
            'R 2 m3 5 #5 b7'   : (3, [0,2,3,7,8,10], ['m9','b13']),               # R b2 4 b5 #5 b7  [0 1 5 6 8 a] R M3 4 5 6 7     [0 4 5 7 9 b] R b2 m3 4 5 #5   [0 1 3 5 7 8] R 2 M3 b5 5 7    [0 2 4 6 7 b] R 2 M3 4 6 b7    [0 2 4 5 9 a]
            'R 2 m3 5 #5 7'    : (3, [0,2,3,7,8,11], ['m','M9','b13']),           # R b2 4 b5 6 b7   [0 1 5 6 9 a] R M3 4 #5 6 7    [0 4 5 8 9 b] R b2 M3 4 5 #5   [0 1 4 5 7 8] R m3 M3 b5 5 7   [0 3 4 6 7 b] R b2 m3 M3 #5 6  [0 1 3 4 8 9]
            'R 2 m3 5 6 b7'    : (2, [0,2,3,7,9,10], ['m','13','9']),             # R b2 4 5 #5 b7   [0 1 5 7 8 a] R M3 b5 5 6 7    [0 4 6 7 9 b] R 2 m3 4 5 #5    [0 2 3 5 7 8] R b2 m3 4 b5 b7  [0 1 3 5 6 a] R 2 M3 4 6 7     [0 2 4 5 9 b]
            'R 2 M3 4 5 6'     : (5, [0,2,4,5,7,9],  ['2','4','6']),              # R 2 m3 4 5 b7    [0 2 3 5 7 a] R b2 m3 4 #5 b7  [0 1 3 5 8 a] R 2 M3 5 6 7     [0 2 4 7 9 b] R 2 4 5 6 b7     [0 2 5 7 9 a] R m3 4 5 #5 b7   [0 3 5 7 8 a]
            'R 2 M3 4 #5 6'    : (3, [0,2,4,5,8,9],  ['+','2','4','6']),          # R 2 m3 b5 5 b7   [0 2 3 6 7 a] R b2 M3 4 #5 b7  [0 1 4 5 8 a] R m3 M3 5 6 7    [0 3 4 7 9 b] R b2 M3 b5 #5 6  [0 1 4 6 8 9] R 2 M3 4 #5 6    [0 2 4 5 8 9]
            'R 2 M3 4 5 b7'    : (0, [0,2,4,5,7,10], ['11','9']),                 # R 2 m3 4 #5 b7   [0 2 3 5 8 a] R b2 m3 b5 #5 b7 [0 1 3 6 8 a] R 2 4 5 6 7      [0 2 5 7 9 b] R m3 4 5 6 b7    [0 3 5 7 9 a] R 2 M3 b5 5 6    [0 2 4 6 7 9]
            'R 2 M3 4 6 b7'    : (2, [0,2,4,5,9,10], ['13','11','9','x']),        # R 2 m3 5 #5 b7   [0 2 3 7 8 a] R b2 4 b5 #5 b7  [0 1 5 6 8 a] R M3 4 5 6 7     [0 4 5 7 9 b] R b2 m3 4 5 #5   [0 1 3 5 7 8] R 2 M3 b5 5 7    [0 2 4 6 7 b]
            'R 2 M3 4 6 7'     : (0, [0,2,4,5,9,11], ['M13','11','9','x']),       # R 2 m3 5 6 b7    [0 2 3 7 9 a] R b2 4 5 #5 b7   [0 1 5 7 8 a] R M3 b5 5 6 7    [0 4 6 7 9 b] R 2 m3 4 5 #5    [0 2 3 5 7 8] R b2 m3 4 b5 b7  [0 1 3 5 6 a]
            'R 2 M3 b5 5 6'    : (5, [0,2,4,6,7,9],  ['2','#4','6']),             # R 2 M3 4 5 b7    [0 2 4 5 7 a] R 2 m3 4 #5 b7   [0 2 3 5 8 a] R b2 m3 b5 #5 b7 [0 1 3 6 8 a] R 2 4 5 6 7      [0 2 5 7 9 b] R m3 4 5 6 b7    [0 3 5 7 9 a]
            'R 2 M3 b5 5 7'    : (1, [0,2,4,6,7,11], ['M7','#11','9']),           # R 2 M3 4 6 b7    [0 2 4 5 9 a] R 2 m3 5 #5 b7   [0 2 3 7 8 a] R b2 4 b5 #5 b7  [0 1 5 6 8 a] R M3 4 5 6 7     [0 4 5 7 9 b] R b2 m3 4 5 #5   [0 1 3 5 7 8]
            'R 2 M3 b5 #5 b7'  : (0, [0,2,4,6,8,10], ['b#5','9']),                # R 2 M3 b5 #5 b7  @0 2 4 6 8 a@ R 2 M3 b5 #5 b7  @0 2 4 6 8 a@ R 2 M3 b5 #5 b7  @0 2 4 6 8 a@ R 2 M3 b5 #5 b7  @0 2 4 6 8 a@ R 2 M3 b5 #5 b7  @0 2 4 6 8 a@
            'R 2 M3 5 6 7'     : (3, [0,2,4,7,9,11], ['M','13','9']),             # R 2 4 5 6 b7     [0 2 5 7 9 a] R m3 4 5 #5 b7   [0 3 5 7 8 a] R 2 M3 4 5 6     [0 2 4 5 7 9] R 2 m3 4 5 b7    [0 2 3 5 7 a] R b2 m3 4 #5 b7  [0 1 3 5 8 a]
            'R 2 4 5 6 b7'     : (4, [0,2,5,7,9,10], ['13','s24']),               # R m3 4 5 #5 b7   [0 3 5 7 8 a] R 2 M3 4 5 6     [0 2 4 5 7 9] R 2 m3 4 5 b7    [0 2 3 5 7 a] R b2 m3 4 #5 b7  [0 1 3 5 8 a] R 2 M3 5 6 7     [0 2 4 7 9 b]
            'R 2 4 5 6 7'      : (4, [0,2,5,7,9,11], ['M13','s24']),              # R m3 4 5 6 b7    [0 3 5 7 9 a] R 2 M3 b5 5 6    [0 2 4 6 7 9] R 2 M3 4 5 b7    [0 2 4 5 7 a] R 2 m3 4 #5 b7   [0 2 3 5 8 a] R b2 m3 b5 #5 b7 [0 1 3 6 8 a]
            'R 2 4 #5 6 7'     : (4, [0,2,5,8,9,11], ['+','M13','11','9']),       # R m3 b5 5 6 b7   [0 3 6 7 9 a] R m3 M3 b5 5 6   [0 3 4 6 7 9] R b2 m3 M3 b5 6  [0 1 3 4 6 9] R 2 m3 4 #5 7    [0 2 3 5 8 b] R b2 m3 b5 6 b7  [0 1 3 6 9 a]
            'R m3 M3 b5 5 6'   : (3, [0,3,4,6,7,9],  ['#2','#4','6']),            # R b2 m3 M3 b5 6  [0 1 3 4 6 9] R 2 m3 4 #5 7    [0 2 3 5 8 b] R b2 m3 b5 6 b7  [0 1 3 6 9 a] R 2 4 #5 6 7     [0 2 5 8 9 b] R m3 b5 5 6 b7   [0 3 6 7 9 a]
            'R m3 M3 b5 5 7'   : (0, [0,3,4,6,7,11], ['M','#11','#9']),           # R b2 m3 M3 #5 6  [0 1 3 4 8 9] R 2 m3 5 #5 7    [0 2 3 7 8 b] R b2 4 b5 6 b7   [0 1 5 6 9 a] R M3 4 #5 6 7    [0 4 5 8 9 b] R b2 M3 4 5 #5   [0 1 4 5 7 8]
            'R m3 M3 5 6 7'    : (2, [0,3,4,7,9,11], ['m','M','13','#9']),        # R m3 4 5 #5 7    [0 3 5 7 8 b] R 2 M3 4 #5 6    [0 2 4 5 8 9] R 2 m3 b5 5 b7   [0 2 3 6 7 a] R b2 M3 4 #5 b7  [0 1 4 5 8 a] R m3 M3 5 6 7    [0 3 4 7 9 b]
            'R m3 4 b5 6 7'    : (1, [0,3,5,6,9,11], ['o','M13','11']),           # R 2 m3 b5 #5 6   @0 2 3 6 8 9@ R b2 M3 b5 5 b7  @0 1 4 6 7 a@ R m3 4 b5 6 7    @0 3 5 6 9 b@ R 2 m3 b5 #5 6   @0 2 3 6 8 9@ R b2 M3 b5 5 b7  @0 1 4 6 7 a@
            'R m3 4 5 #5 b7'   : (2, [0,3,5,7,8,10], ['m','b13','11']),           # R 2 M3 4 5 6     [0 2 4 5 7 9] R 2 m3 4 5 b7    [0 2 3 5 7 a] R b2 m3 4 #5 b7  [0 1 3 5 8 a] R 2 M3 5 6 7     [0 2 4 7 9 b] R 2 4 5 6 b7     [0 2 5 7 9 a]
            'R m3 4 5 #5 7'    : (4, [0,3,5,7,8,11], ['+','m','M11']),            # R 2 M3 4 #5 6    [0 2 4 5 8 9] R 2 m3 b5 5 b7   [0 2 3 6 7 a] R b2 M3 4 #5 b7  [0 1 4 5 8 a] R m3 M3 5 6 7    [0 3 4 7 9 b] R b2 M3 b5 #5 6  [0 1 4 6 8 9]
            'R m3 4 5 6 b7'    : (2, [0,3,5,7,9,10], ['m','13','11']),            # R 2 M3 b5 5 6    [0 2 4 6 7 9] R 2 M3 4 5 b7    [0 2 4 5 7 a] R 2 m3 4 #5 b7   [0 2 3 5 8 a] R b2 m3 b5 #5 b7 [0 1 3 6 8 a] R 2 4 5 6 7      [0 2 5 7 9 b]
            'R M3 4 5 6 7'     : (0, [0,4,5,7,9,11], ['M13','11']),               # R b2 m3 4 5 #5   [0 1 3 5 7 8] R 2 M3 b5 5 7    [0 2 4 6 7 b] R 2 M3 4 6 b7    [0 2 4 5 9 a] R 2 m3 5 #5 b7   [0 2 3 7 8 a] R b2 4 b5 #5 b7  [0 1 5 6 8 a]
            'R M3 4 #5 6 7'    : (1, [0,4,5,8,9,11], ['+','M13','11']),           # R b2 M3 4 5 #5   [0 1 4 5 7 8] R m3 M3 b5 5 7   [0 3 4 6 7 b] R b2 m3 M3 #5 6  [0 1 3 4 8 9] R 2 m3 5 #5 7    [0 2 3 7 8 b] R b2 4 b5 6 b7   [0 1 5 6 9 a]
            'R m3 b5 5 6 b7'   : (0, [0,3,6,7,9,10], ['m13','#11']),              # R m3 M3 b5 5 6   [0 3 4 6 7 9] R b2 m3 M3 b5 6  [0 1 3 4 6 9] R 2 m3 4 #5 7    [0 2 3 5 8 b] R b2 m3 b5 6 b7  [0 1 3 6 9 a] R 2 4 #5 6 7     [0 2 5 8 9 b]
            'R M3 b5 5 6 7'    : (1, [0,4,6,7,9,11], ['M13','#11']),              # R 2 m3 4 5 #5    [0 2 3 5 7 8] R b2 m3 4 b5 b7  [0 1 3 5 6 a] R 2 M3 4 6 7     [0 2 4 5 9 b] R 2 m3 5 6 b7    [0 2 3 7 9 a] R b2 4 5 #5 b7   [0 1 5 7 8 a]

            'R b2 2 m3 4 #5'   : (4, [0,1,2,3,5,8],  ['m+','2b2','4']),           # R b2 2 M3 5 7    [0 1 2 4 7 b] R b2 m3 b5 b7 7  [0 1 3 6 a b] R 2 4 6 b7 7     [0 2 5 9 a b] R m3 5 #5 6 b7   [0 3 7 8 9 a] R M3 4 b5 5 6    [0 4 5 6 7 9]
            'R b2 2 M3 5 7'    : (1, [0,1,2,4,7,11], ['M9','b9']),                # R b2 m3 b5 b7 7  [0 1 3 6 a b] R 2 4 6 b7 7     [0 2 5 9 a b] R m3 5 #5 6 b7   [0 3 7 8 9 a] R M3 4 b5 5 6    [0 4 5 6 7 9] R b2 2 m3 4 #5   [0 1 2 3 5 8]
            'R b2 m3 b5 b7 7'  : (3, [0,1,3,6,10,11], ['07','M7','b9']),          # R 2 4 6 b7 7     [0 2 5 9 a b] R m3 5 #5 6 b7   [0 3 7 8 9 a] R M3 4 b5 5 6    [0 4 5 6 7 9] R b2 2 m3 4 #5   [0 1 2 3 5 8] R b2 2 M3 5 7    [0 1 2 4 7 b]
            'R 2 4 6 b7 7'     : (5, [0,2,5,9,10,11], ['7','M13','s24']),         # R m3 5 #5 6 b7   [0 3 7 8 9 a] R M3 4 b5 5 6    [0 4 5 6 7 9] R b2 2 m3 4 #5   [0 1 2 3 5 8] R b2 2 M3 5 7    [0 1 2 4 7 b] R b2 m3 b5 b7 7  [0 1 3 6 a b]
            'R m3 5 #5 6 b7'   : (0, [0,3,7,8,9,10], ['m13','b13']),              # R M3 4 b5 5 6    [0 4 5 6 7 9] R b2 2 m3 4 #5   [0 1 2 3 5 8] R b2 2 M3 5 7    [0 1 2 4 7 b] R b2 m3 b5 b7 7  [0 1 3 6 a b] R 2 4 6 b7 7     [0 2 5 9 a b]
            'R M3 4 b5 5 6'    : (2, [0,4,5,6,7,9],  ['4#4','6']),                # R b2 2 m3 4 #5   [0 1 2 3 5 8] R b2 2 M3 5 7    [0 1 2 4 7 b] R b2 m3 b5 b7 7  [0 1 3 6 a b] R 2 4 6 b7 7     [0 2 5 9 a b] R m3 5 #5 6 b7   [0 3 7 8 9 a]

            'R b2 2 m3 b5 b7'  : (4, [0,1,2,3,6,10], ['07','9b9']),               # R b2 2 4 6 7     [0 1 2 5 9 b] R b2 M3 #5 b7 7  [0 1 4 8 a b] R m3 5 6 b7 7    [0 3 7 9 a b] R M3 b5 5 #5 6   [0 4 6 7 8 9] R 2 m3 M3 4 #5   [0 2 3 4 5 8]
            'R b2 2 4 6 7'     : (2, [0,1,2,5,9,11], ['M13','b9','s24']),         # R b2 M3 #5 b7 7  [0 1 4 8 a b] R m3 5 6 b7 7    [0 3 7 9 a b] R M3 b5 5 #5 6   [0 4 6 7 8 9] R 2 m3 M3 4 #5   [0 2 3 4 5 8] R b2 2 m3 b5 b7  [0 1 2 3 6 a]
            'R b2 M3 #5 b7 7'  : (1, [0,1,4,8,10,11], ['7+','M9']),               # R m3 5 6 b7 7    [0 3 7 9 a b] R M3 b5 5 #5 6   [0 4 6 7 8 9] R 2 m3 M3 4 #5   [0 2 3 4 5 8] R b2 2 m3 b5 b7  [0 1 2 3 6 a] R b2 2 4 6 7     [0 1 2 5 9 b]
            'R 2 m3 M3 4 #5'   : (5, [0,2,3,4,5,8],  ['m+','2#2','4']),           # R b2 2 m3 b5 b7  [0 1 2 3 6 a] R b2 2 4 6 7     [0 1 2 5 9 b] R b2 M3 #5 b7 7  [0 1 4 8 a b] R m3 5 6 b7 7    [0 3 7 9 a b] R M3 b5 5 #5 6   [0 4 6 7 8 9]
            'R m3 5 6 b7 7'    : (0, [0,3,7,9,10,11], ['m7','M13']),              # R M3 b5 5 #5 6   [0 4 6 7 8 9] R 2 m3 M3 4 #5   [0 2 3 4 5 8] R b2 2 m3 b5 b7  [0 1 2 3 6 a] R b2 2 4 6 7     [0 1 2 5 9 b] R b2 M3 #5 b7 7  [0 1 4 8 a b]
            'R M3 b5 5 #5 6'   : (3, [0,4,6,7,8,9],  ['6b6','#4']),               # R 2 m3 M3 4 #5   [0 2 3 4 5 8] R b2 2 m3 b5 b7  [0 1 2 3 6 a] R b2 2 4 6 7     [0 1 2 5 9 b] R b2 M3 #5 b7 7  [0 1 4 8 a b] R m3 5 6 b7 7    [0 3 7 9 a b]

            'R b2 2 b5 5 b7'   : (1, [0,1,2,6,7,10],  ['#11','9b9','y']),         # R b2 4 b5 6 7    [0 1 5 6 9 b] R M3 4 #5 b7 7   [0 4 5 8 a b] R b2 M3 b5 5 #5  [0 1 4 6 7 8] R m3 4 b5 5 7    [0 3 5 6 7 b] R 2 m3 M3 #5 6   [0 2 3 4 8 9]
            'R b2 M3 b5 5 #5'  : (0, [0,1,4,6,7,8],   ['b2','#4','b6']),          # R m3 4 b5 5 7    [0 3 5 6 7 b] R 2 m3 M3 #5 6   [0 2 3 4 8 9] R b2 2 b5 5 b7   [0 1 2 6 7 a] R b2 4 b5 6 7    [0 1 5 6 9 b] R M3 4 #5 b7 7   [0 4 5 8 a b]
            'R b2 4 b5 6 7'    : (2, [0,1,5,6,9,11],  ['13','11','b9','b5']),     # R M3 4 #5 b7 7   [0 4 5 8 a b] R b2 M3 b5 5 #5  [0 1 4 6 7 8] R m3 4 b5 5 7    [0 3 5 6 7 b] R 2 m3 M3 #5 6   [0 2 3 4 8 9] R b2 2 b5 5 b7   [0 1 2 6 7 a]
            'R 2 m3 M3 #5 6'   : (3, [0,2,3,4,8,9],   ['6b6','2#2']),             # R b2 2 b5 5 b7   [0 1 2 6 7 a] R b2 4 b5 6 7    [0 1 5 6 9 b] R M3 4 #5 b7 7   [0 4 5 8 a b] R b2 M3 b5 5 #5  [0 1 4 6 7 8] R m3 4 b5 5 7    [0 3 5 6 7 b]
            'R m3 4 b5 5 7'    : (4, [0,3,5,6,7,11],  ['m','M11','#11']),         # R 2 m3 M3 #5 6   [0 2 3 4 8 9] R b2 2 b5 5 b7   [0 1 2 6 7 a] R b2 4 b5 6 7    [0 1 5 6 9 b] R M3 4 #5 b7 7   [0 4 5 8 a b] R b2 M3 b5 5 #5  [0 1 4 6 7 8]
            'R M3 4 #5 b7 7'   : (5, [0,4,5,8,10,11], ['+','13','M11']),          # R b2 M3 b5 5 #5  [0 1 4 6 7 8] R m3 4 b5 5 7    [0 3 5 6 7 b] R 2 m3 M3 #5 6   [0 2 3 4 8 9] R b2 2 b5 5 b7   [0 1 2 6 7 a] R b2 4 b5 6 7    [0 1 5 6 9 b]

          # 'R b2 m3 4 b5 6'  : (-1, [0,1,3,5,6,9],   ['o','b2','4','6']),        # R 2 M3 4 #5 7    [0 2 4 5 8 b] R 2 m3 b5 6 b7   [0 2 3 6 9 a] R b2 M3 5 #5 b7  [0 1 4 7 8 a] R m3 b5 5 6 7    [0 3 6 7 9 b] R m3 M3 b5 #5 6  [0 3 4 6 8 9]
          # 'R b2 M3 5 #5 b7' : (-1, [0,1,4,7,8,10],  ['b13','b9']),              # R m3 b5 5 6 7    [0 3 6 7 9 b] R m3 M3 b5 #5 6  [0 3 4 6 8 9] R b2 m3 4 b5 6   [0 1 3 5 6 9] R 2 M3 4 #5 7    [0 2 4 5 8 b] R 2 m3 b5 6 b7   [0 2 3 6 9 a]
          # 'R 2 m3 b5 6 b7'  : (-1, [0,2,3,6,9,10],  ['7','o7','9']),            # R b2 M3 5 #5 b7  [0 1 4 7 8 a] R m3 b5 5 6 7    [0 3 6 7 9 b] R m3 M3 b5 #5 6  [0 3 4 6 8 9] R b2 m3 4 b5 6   [0 1 3 5 6 9] R 2 M3 4 #5 7    [0 2 4 5 8 b]
          # 'R 2 M3 4 #5 7'   : (-1, [0,2,4,5,8,11],  ['+','M11','9']),           # R 2 m3 b5 6 b7   [0 2 3 6 9 a] R b2 M3 5 #5 b7  [0 1 4 7 8 a] R m3 b5 5 6 7    [0 3 6 7 9 b] R m3 M3 b5 #5 6  [0 3 4 6 8 9] R b2 m3 4 b5 6   [0 1 3 5 6 9]
          # 'R m3 M3 b5 #5 6' : (-1, [0,3,4,6,8,9],   ['+','b5','#2','6']),       # R b2 m3 4 b5 6   [0 1 3 5 6 9] R 2 M3 4 #5 7    [0 2 4 5 8 b] R 2 m3 b5 6 b7   [0 2 3 6 9 a] R b2 M3 5 #5 b7  [0 1 4 7 8 a] R m3 b5 5 6 7    [0 3 6 7 9 b]
          # 'R m3 b5 5 6 7'   : (-1, [0,3,6,7,9,11],  ['o7','M7','#11']),         # R m3 M3 b5 #5 6  [0 3 4 6 8 9] R b2 m3 4 b5 6   [0 1 3 5 6 9] R 2 M3 4 #5 7    [0 2 4 5 8 b] R 2 m3 b5 6 b7   [0 2 3 6 9 a] R b2 M3 5 #5 b7  [0 1 4 7 8 a]
            }
    ####################################################################################################################################################################################################
    # index 3note 4note 5note 6note #
    #   1     1     1     1     1   #
    #   2     3     4     5     6   #
    #   3     6    10    15    21   #
    #   4    10    20    35    56   #
    #   5    15    35    70   126   #
    #   6    21    56   126   252   #
    #   7    28    84   210   462   #
    #   8    36   120   330         #
    #   9    45   165               #
    #  10    55                     #
    #################################
    # 1-10   55   220   550  1012   #
    ####################################################################################################################################################################################################

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
