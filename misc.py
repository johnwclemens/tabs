import sys, os, collections
sys.path.insert(0, os.path.abspath('.'))
import tabs

VERBOSE = 0 # tabs.VERBOSE
M12           = { 10:'a', 11:'b' }
INTERVALS     = { 0:'R', 1:'b2', 2:'2', 3:'m3', 4:'M3', 5:'4', 6:'b5', 7:'5', 8:'#5', 9:'6', 10:'b7', 11:'7' }
INTERVAL_RANK = { 'R':0, 'b2':1, '2':2, 'm3':3, 'M3':4, '4':5, 'b5':6, '5':7, '#5':8, '6':9, 'b7':10, '7':11 }
NTONES        = len(INTERVALS)

####################################################################################################################################################################################################
class Note(object):
    FLAT, SHARP = 0, 1
    TYPE        = FLAT
    TYPES       = ['FLAT', 'SHARP']
    F2S         = {'Db':'C#', 'Eb':'D#', 'Gb':'F#', 'Ab':'G#', 'Bb':'A#'}
    S2F         = {'C#':'Db', 'D#':'Eb', 'F#':'Gb', 'G#':'Ab', 'A#':'Bb'}
    FLATS       = { 0:'C', 1:'Db', 2:'D', 3:'Eb', 4:'E', 5:'F', 6:'Gb', 7:'G', 8:'Ab', 9:'A', 10:'Bb', 11:'B' }
    SHARPS      = { 0:'C', 1:'C#', 2:'D', 3:'D#', 4:'E', 5:'F', 6:'F#', 7:'G', 8:'G#', 9:'A', 10:'A#', 11:'B' }
    TONES       = [FLATS, SHARPS]
    INDICES = { 'C0': 0, 'C#0': 1, 'Db0': 1, 'D0': 2, 'D#0': 3, 'Eb0': 3, 'E0': 4, 'F0': 5, 'F#0': 6, 'Gb0': 6, 'G0': 7, 'G#0': 8, 'Ab0': 8, 'A0': 9, 'A#0':10, 'Bb0':10, 'B0':11,
                'C1':12, 'C#1':13, 'Db1':13, 'D1':14, 'D#1':15, 'Eb1':15, 'E1':16, 'F1':17, 'F#1':18, 'Gb1':18, 'G1':19, 'G#1':20, 'Ab1':20, 'A1':21, 'A#1':22, 'Bb1':22, 'B1':23,
                'C2':24, 'C#2':25, 'Db2':25, 'D2':26, 'D#2':27, 'Eb2':27, 'E2':28, 'F2':29, 'F#2':30, 'Gb2':30, 'G2':31, 'G#2':32, 'Ab2':32, 'A2':33, 'A#2':34, 'Bb2':34, 'B2':35,
                'C3':36, 'C#3':37, 'Db3':37, 'D3':38, 'D#3':39, 'Eb3':39, 'E3':40, 'F3':41, 'F#3':42, 'Gb3':42, 'G3':43, 'G#3':44, 'Ab3':44, 'A3':45, 'A#3':46, 'Bb3':46, 'B3':47,
                'C4':48, 'C#4':49, 'Db4':49, 'D4':50, 'D#4':51, 'Eb4':51, 'E4':52, 'F4':53, 'F#4':54, 'Gb4':54, 'G4':55, 'G#4':56, 'Ab4':56, 'A4':57, 'A#4':58, 'Bb4':58, 'B4':59,
                'C5':60, 'C#5':61, 'Db5':61, 'D5':62, 'D#5':63, 'Eb5':63, 'E5':64, 'F5':65, 'F#5':66, 'Gb5':66, 'G5':67, 'G#5':68, 'Ab5':68, 'A5':69, 'A#5':70, 'Bb5':70, 'B5':71,
                'C6':72, 'C#6':73, 'Db6':73, 'D6':74, 'D#6':75, 'Eb6':75, 'E6':76, 'F6':77, 'F#6':78, 'Gb6':78, 'G6':79, 'G#6':80, 'Ab6':80, 'A6':81, 'A#6':82, 'Bb6':82, 'B6':83,
                'C7':84, 'C#7':85, 'Db7':85, 'D7':86, 'D#7':87, 'Eb7':87, 'E7':88, 'F7':89, 'F#7':90, 'Gb7':90, 'G7':91, 'G#7':92, 'Ab7':92, 'A7':93, 'A#7':94, 'Bb7':94, 'B7':95,
                'C8':96 } # For simplicity omit double flats and double sharps and other redundant enharmonic note names e.g. Abb, C##, Cb, B#, Fb, E# etc...
    NAMES   = [ k for k in INDICES.keys() if k[1] is not 'b' ]

    @staticmethod
    def setType(t): Note.TYPE = t

    @staticmethod
    def getName(i):
        name = Note.TONES[Note.TYPE][i % NTONES]
        return name

    @staticmethod
    def getFreq(index): return 440 * pow(pow(2, 1/NTONES), index - Note.INDICES)

####################################################################################################################################################################################################
class DSymb(object):
    SYMBS = {'X': 'mute', '/': 'slide', '\\': 'bend', '+': 'hammer', '~': 'vibrato', '^': 'tie', '.': 'staccato', '_': 'legato', '%': 'repeat', '|': 'bar', '[': 'groupL', ']': 'groupR'}
####################################################################################################################################################################################################

class Chord(object):
    MIN_CHORD_LEN = 3
    def __init__(self, tobj, logfile):
        self.tobj    = tobj
        self.logFile = logfile
        self.limap, self.mlimap, self.umap, self.cycles = [], {}, {}, {}
        self.catmap, self.catmap2 = {}, {}
        self.cat1, self.cat2, self.cat3 = set(), set(), dict()

    def log(self, msg='', ind=1, pos=0, file=None, flush=False, sep=',', end='\n'):
        if file is None: file=self.logFile
        self.tobj.log(msg=msg, ind=ind, pos=pos, file=file, flush=flush, sep=sep, end=end)
    ####################################################################################################################################################################################################
    def getChordName(self, p, l, c, kk=1, why='', dbg=10):
        cn = self.tobj.plc2cn(p, l, c)   ;   self.limap = []
        ikeys, ivals, notes, name, chunks, rank = [], [], [], '', [], -1
        mask, _notes, ixs = self._getIndices(p, l, c)   ;   _imap, vkeys = None, []
        for k in range(len(ixs)):
            _ivals = []   ;   chunks = []
            for j in range(len(ixs)):
                if ixs[j] >= ixs[k]: i =           (ixs[j] - ixs[k])  % NTONES
                else:                i = (NTONES - (ixs[k] - ixs[j])) % NTONES
                _ivals.append(i)
            vkey = ''.join([ f'{v:x}' for v in _ivals ])
            if vkey not in vkeys:
                _ikeys = [ INTERVALS[i] for i in _ivals ]
                if dbg: self._dumpData(rank, _ikeys, _ivals, _notes, mask, 0)
                _imap = collections.OrderedDict(sorted(dict(zip(_ikeys, _notes)).items(), key=lambda t: INTERVAL_RANK[t[0]]))
                ikeys = list(_imap.keys())   ;   notes = list(_imap.values())   ;   ivals = [ INTERVAL_RANK[k] for k in ikeys ]
                ikey = ' '.join([ k for k in ikeys ])
                if ikey in self.OMAP:
                    chunks.append(_imap['R'])
                    [ chunks.append(n) for n in self.OMAP[ikey][2] if n ]
                    name = ''.join(chunks)      ;     rank = self.OMAP[ikey][0]
                    assert ivals == self.OMAP[ikey][1]
                elif kk and len(_imap) >= Chord.MIN_CHORD_LEN:
                    self.log(f'{why} ADDING ikey={ikey} ivals={tabs.fmtl(ivals)} to OMAP')
                    self.umap[ikey] = (rank, ivals, [])    ;   assert 0
                if not kk:  ikeys = _ikeys   ;   notes = _notes   ;   ivals = _ivals
                if dbg: self._dumpData(rank, ikeys, ivals, notes, mask, 1)
                imap  = [ ikeys, ivals, notes, name, chunks, rank ]
                vkeys.append(vkey)   ;   self.limap.append(imap)
                if dbg: self.log(f'{rank:2} <{ikey}> {tabs.fmtl(ikeys)} <{vkey}> {tabs.fmtl(vkeys)} {" ".join(notes):12} {tabs.fmtl(ivals, z="x")} {name:12} {"".join(chunks)}')
        if self.limap:
            self.limap.sort(key=lambda m: m[-1])
            if dbg > 1: self.dumpLimap(self.limap, cn)
            self.mlimap[cn] = self.limap
            return self.limap[0]
        return [ ikeys, ivals, notes, name, chunks, rank ]

    def _getIndices(self, p, l, c, dbg=1, dbg2=0):
        strNumbs   = self.tobj.stringNumbs
        strKeys    = self.tobj.stringKeys
        strNames   = self.tobj.stringNames
        _tabs      = self.tobj.data[p][l][c]
        strIndices = [ Note.INDICES[k] for k in strKeys ]
        mask, indices, notes = [], [], []  ;  nt = len(_tabs)
        for t in range(nt-1, -1, -1):
            if tabs.Tabs.isFret(_tabs[t]):
                fn    = self.tobj.tab2fn(_tabs[t])
                index = self.tobj.fn2ni(fn, t)
                note  = self.tobj.tab2nn(_tabs[t], t)
                if index: indices.append(index)
                if note :   notes.append(note)   ;   mask.append(1)
                else: mask.append(0)
            else: mask.append(0)
        if notes:
            mask0 = [1] * self.tobj.n[tabs.T]
            if dbg2: self.dumpData(strNumbs,   mask0, 'strNumbs', r=1)
            if dbg2: self.dumpData(strKeys,    mask0, 'strKeys')
            if dbg2: self.dumpData(strIndices, mask0, 'strIndices')
            if dbg2: self.dumpData(strNames,   mask0, 'strNames', r=1)
            if dbg:  self.dumpData(_tabs,      mask0, 'Tabs',     r=1)
            if dbg:  self.dumpData(indices,    mask,  'Note Indices')
#            if dbg:  self.dumpData(notes,      mask,  'Notes')
        return mask, notes, indices
    ####################################################################################################################################################################################################
    def _dumpData(self, rank, ikeys, ivals, notes, mask, a):
        ikey = ' '.join(ikeys)   ;   ival = ''.join([ f'{v:x}' for v in ivals ])   ;   note = ' '.join(notes)  # ;   r = f'{rank:2}'
        if a: self.dumpData(ikeys, mask, f'{rank:2} ikeys {ikey}')   ;   self.dumpData(ivals, mask, f'{rank:2} ivals {ival}')   ;   self.dumpData(notes, mask, f'{rank:2} Notes {note}')
        else: self.dumpData(notes, mask, f'{rank:2} Notes {note}')   ;   self.dumpData(ivals, mask, f'{rank:2} ivals {ival}')   ;   self.dumpData(ikeys, mask, f'{rank:2} ikeys {ikey}')

    def dumpData(self, data, mask, why, w=5, u='<', r=0):
        if r:     data = data[::-1]  ;  mask = mask[::-1]
        j = 0   ;   dt = type(data)  ;  self.log(f'{why:26} [ ', end='')
        if dt is list or dt is str:
            for i in range(len(mask)):
                if   mask[i] and j < len(data): self.log('{:{}{}} '.format(data[j], u, w), ind=0, end='')  ;  j += 1
                elif mask[i]:                   self.log('{:{}{}} '.format(' ',     u, w), ind=0, end='')
                else:                           self.log('{:{}{}} '.format('~',     u, w), ind=0, end='')
        elif dt is collections.OrderedDict:
            w2 = 2  ;   i = 0
            for k,v in data.items():
                while not mask[i]: self.log('{:{}{}} '.format('-', u, w),    ind=0, end='')  ;  i += 1
                self.log('{:>{}}{}{:<{}} '.       format(k, w2, ':', v, w2), ind=0, end='')  ;  i += 1
            while i < len(mask): self.log('{:{}{}} '.  format('-', u, w),    ind=0, end='')  ;  i += 1
        else: self.log(f'type={dt} ', ind=0, end='')
        self.log(']',                 ind=0)
    ####################################################################################################################################################################################################
    def dumpMlimap(self, why=''):
        self.log(f'{why}')
        for k, v in self.mlimap.items():
            self.dumpLimap(v, k)
        for k, v in self.mlimap.items():
            self.dumpLimap1(v, k)
        for k, v in self.mlimap.items():
            self.dumpLimap2(v, k)
        for k, v in self.mlimap.items():
            self.dumpLimap3(v, k)

    def dumpLimap(self, limap, key):
        [ self.dumpImap(im, f'{key:2}') for im in limap ]

    def dumpLimap1(self, limap, key):
        self.log(f'{key:2}', ind=0, end=' ')
        for m in limap:
            keys = f'{tabs.fmtl(m[0], w=2, d1=None)}'
            self.log(f'{m[3]:12} {keys:17}', ind=0, end=' ')
        self.log(ind=0)

    def dumpLimap2(self, limap, key):
        self.log(f'{key:2}', ind=0, end='')
        [ self.log(f'{m[-1]:2} {m[3]:12} {tabs.fmtl(m[1], d1=None, z="x"):11} ', ind=0, end='') for m in limap ]
        self.log(ind=0)

    def dumpLimap3(self, limap, key):
        self.log(f'{key:2}', ind=0, end=' ')   ;   msg1, msg2 = '', ''
        for m in limap:
            msg1 += f'|{tabs.fmtl(m[1], d1=None, z="x"):11}'
        msg1 += '|'
        for m in limap:
            msg2 += f'|{tabs.fmtl(m[0], d1=None, w=2):17}'
#            msg2 += f'|{tabs.fmtl(sorted(m[0], key=lambda t: INTERVAL_RANK[t]), d1=None, w=tabs.FMTN2):16}'
        self.log(f'{msg1:73}{msg2}|', ind=0)
#        msg1 = [ f'{tabs.fmtl(m[1], d1="", d2="", z="x"):13}' for m in limap ]
#        msg2 = [ f'{tabs.fmtl(m[0], d1="", d2="", w=2):19}'   for m in limap ]
#        self.log(f'{tabs.fmtl(msg1):80}{tabs.fmtl(msg2)}', ind=0)
#        msg1 = [ m[1] for m in limap ]
#        msg2 = [ m[0] for m in limap ]
#        self.log(f'{msg1} {msg2}', ind=0)

    def dumpImap(self, imap, why=''):
        ikeys, ivals, inotes, name, chunks, rank = [], [], [], '', [], -1  # ;   ivals2 = ''
        if imap and len(imap) == 6: ikeys, ivals, inotes, name, chunks, rank = imap[0],imap[1], imap[2], imap[3], imap[4], imap[5]
#        if ivals:
#            for i in ivals:
#                ivals2 += f'{i:x}'
        self.log(f'{why}{rank:2} {name:12} {tabs.fmtl(chunks, w=2):19} {tabs.fmtl(ikeys, w=2):19} {tabs.fmtl(ivals, z="x")} {tabs.fmtl(inotes, w=2):19}', ind=0)
#        self.log(f'{why}{rank:2} {name:12} {tabs.fmtl(chunks, w=2):19} {tabs.fmtl(ikeys, w=2):19} {tabs.fmtl(ivals, z="x"):13} {tabs.fmtl(inotes, w=2):19}', ind=0)
#        self.log(f'{why}{rank:2} {name:12} {tabs.fmtl(chunks, w=2):19} {tabs.fmtl(sorted(ikeys, key=lambda t: INTERVAL_RANK[t]), w=tabs.FMTN2):18} {tabs.fmtl(ivals, z="x"):13} {tabs.fmtl(inotes, w=2):19}', ind=0)
    ####################################################################################################################################################################################################
    def rotateMLimap(self, cn):
        a = self.mlimap[cn]
        a = (a[-1:] + a[:-1])
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
       ll = len(a)   ;   r = [0]
       for i in range(1, ll):
           if i + 1 < ll: r.append(a[i+1] - a[i] + r[i-1])
           else :         r.append(NTONES - a[i] + r[i-1])
       return r
    ####################################################################################################################################################################################################
    @staticmethod
    def key2Indices(k):
        r = []  ;  t = ''
        for j in k:
            if j != ' ': t += j
            else:        r.append(INTERVAL_RANK[t])  ;  t = ''
        r.append(INTERVAL_RANK[t])
        return r

    def mergeMaps(self, src, trg):
        self.log(f'BGN len(src) ={len(src)} len(trg)={len(trg)}')
        for k, v in src.items():
            trg[k] = v
        self.log(f'END len(src) ={len(src)} len(trg)={len(trg)}')
    ####################################################################################################################################################################################################
    def dumpUmap(self):
        if self.umap:
            self.log('BGN umap:')
            umapKeys = sorted(self.umap.keys() , key=lambda a: self.umap[a][1])
            for k in umapKeys:
                v = self.umap[k]
                k = '\'' + k + '\''
                self.log(f'{k:19}: ({v[0]}, {tabs.fmtl(v[1], sep=",", d2="],"):15})', ind=0)
            self.log(f'END umap len={len(self.umap)}')

    def dumpOMAP(self, catpath=None, merge=0):
        self.log(f'BGN len(OMAP)={len(self.OMAP)} len(umap)={len(self.umap)}')
        if merge and self.umap: self.mergeMaps(self.umap, self.OMAP)
        r = self._dumpOMAP()
        if catpath:
            with open(str(catpath), 'w') as CAT_FILE:
                self._dumpOMAP(CAT_FILE)
        if r:
            for (k,v) in r.items():
                self.OMAP[k] = v
            self._dumpOMAP()
            if catpath:
                with open(str(catpath), 'w') as CAT_FILE:
                    self._dumpOMAP(CAT_FILE)
        if self.umap: self.dumpUmap()
        self.log(f'END   len(OMAP)={len(self.OMAP)} len(umap)={len(self.umap)}')

    def _dumpOMAP(self, catfile=None, dbg=0):
        file = catfile      if catfile else self.logFile
        name = catfile.name if catfile else None
        omap = self.OMAP
        mapSet = {}   ;   r = {}   ;   rank = -1
        self.log('BGN len(OMAP)={} catfile.name={}'.format(len(omap), name))
        for k, v in omap.items():
            kv = len(v[1])
            if kv not in mapSet: mapSet[kv] = set()
            mapSet[kv].add(tuple(v[1]))
        j, mstat, tstat = 0, [], []  ;  msg = 'ERROR: Invalid Rank'  # ;  q = 0
        for k, sml in mapSet.items():
            sml = sorted(sml)
            tstat.append(0)
            count, nord, none = 0, 0, 0
            for ii in sml:
                keys = [ INTERVALS[i] for i in ii ]
                keyStr    = ' '.join(keys)
                keyStrFmt = '\'' + keyStr + '\''
                v = omap[keyStr]
                rankSet = set()  ;  rankSet.add(v[0])
                if not catfile: count += 1  ;  none += 1 if not v[2] else 0  ;  nord += 1 if v[0] == rank else 0
                v2 = tabs.fmtl(v[2], sep='\',\'', d1='[\'', d2='\']),') if v[2] else '[]),' if type(v[2]) is list else 'None),'
                if dbg: self.log(f'{keyStrFmt:19}: ({v[0]}, {tabs.fmtl(v[1], sep=",", d2="],"):15} {v2:28} # ', ind=0, file=file, end='')
                cycSet =  set()   ;   cycSet.add(tuple(ii))
                for _ in range(len(ii) - 1):
                    ii = self.rotateIndices(ii)
                    keys = [ INTERVALS[i] for i in ii ]
                    keyStr = ' '.join(keys)   ;   ck = len(ii)   ;   jj = tuple(ii)    ;   cycle = 0
                    if keyStr in omap: rankSet.add(omap[keyStr][0])
                    if jj in cycSet:
                        if ck not in self.cycles: self.cycles[ck] = set()
                        self.cycles[ck].add(jj)                                        ;   cycle = 1
                    cycSet.add(jj)    ;     d1 = '@' if cycle else '['    ;    d2 = '@' if cycle else ']'
                    if keyStr not in omap:        self.log(f'Not in map: ', ind=0, end='', file=file)     ;    r[keyStr] = (rank, ii, None)
                    if dbg: self.log(f'{keyStr:16} {tabs.fmtl(ii, z="x", d1=d1, d2=d2):13} ', ind=0, end='', file=file)
                refSet = { _ for _ in range(len(ii)) }
                if dbg:
                    if    rankSet == refSet or len(cycSet) != len(refSet) or -1 in rankSet: self.log(ind=0, file=file)
                    else: self.log(f'\n{msg} {tabs.fmtl(refSet, d1="<", d2=">")} {tabs.fmtl(rankSet, d1="<", d2=">")} {tabs.fmtl(sorted(cycSet))}', ind=0, file=file)  # ;  q = 1
            if not catfile: mstat.append([k, count, nord, none])
        if not catfile:
            for kk, w in self.cycles.items():
                for c in tuple(sorted(w)):
                    keys = [ INTERVALS[j] for j in c ]   ;   key = ' '.join(keys)   ;   v = omap[key]
                    self.log(f'{kk:2} note cycle {v[0]:2} {tabs.fmtl(c, z="x"):13} {key:16} {"".join(v[2]):12} {v[2]}')
            for j in range(len(mstat)):
                self.log(f'{mstat[j][0]:2} note chords  {mstat[j][1]:3} valid  {mstat[j][2]:3} unordered  {mstat[j][3]:3} unnamed')
                tstat[0] += mstat[j][0]   ;   tstat[1] += mstat[j][1]   ;   tstat[2] += mstat[j][2]   ;   tstat[3] += mstat[j][3]
        if catfile: self.log('END len(OMAP)={} catfile.name={} len(r)={}'.format(len(omap), name, len(r)))
        else: self.log(f'END grand total {tstat[1]:3} total  {tstat[2]:3} unordered  {tstat[3]:3} unnamed  len(r)={len(r)}')
#        if q: self.tobj.quit(msg, code=2)
        return r
    ####################################################################################################################################################################################################
    #    0  1  2  3  4  5  6  7  8   9  10 11 0
    #    R  b2 2  m3 M3 4  b5 5  #5  6  b7 7  R
    #       b9 9  #9    11 #11   b13 13
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
            'R 2 m3'           : (2, [0,2,3],        ['m','2','x']),              # R b2 b7          [0 1 a]       R 6 7            [0 9 b]
            'R 2 M3'           : (2, [0,2,4],        ['2','x']),                  # R 2 b7           [0 2 a]       R #5 b7          [0 8 a]
            'R 2 4'            : (1, [0,2,5],        ['s2','s4','x']),            # R m3 b7          [0 3 a]       R 5 6            [0 7 9]
            'R 2 b5'           : (1, [0,2,6],        ['o','s2']),                 # R M3 b7          [0 4 a]       R b5 #5          [0 6 8]
            'R 2 5'            : (1, [0,2,7],        ['s2']),                     # R 4 b7           [0 5 a]       R 4 5            [0 5 7]
            'R 2 #5'           : (1, [0,2,8],        ['+','s2']),                 # R b5 b7          [0 6 a]       R M3 b5          [0 4 6]
            'R 2 6'            : (0, [0,2,9],        ['6','s2','x']),             # R 5 b7           [0 7 a]       R m3 4           [0 3 5]
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
            'R 5 b7'           : (1, [0,7,10],       ['7','y']),                  # R m3 4           [0 3 5]       R 2 6            [0 2 9]
            'R 5 7'            : (0, [0,7,11],       ['M','7','y']),              # R M3 4           [0 4 5]       R b2 #5          [0 1 8]
            'R #5 6'           : (2, [0,8,9],        ['+','6','y']),              # R b2 M3          [0 1 4]       R m3 7           [0 3 b]
            'R #5 b7'          : (1, [0,8,10],       ['+','7','y']),              # R 2 M3           [0 2 4]       R 2 b7           [0 2 a]
            'R #5 7'           : (0, [0,8,11],       ['M','+','y']),              # R m3 M3          [0 3 4]       R b2 6           [0 1 9]
            'R 6 b7'           : (1, [0,9,10],       ['13','x','y']),             # R b2 m3          [0 1 3]       R 2 7            [0 2 b]
            'R 6 7'            : (0, [0,9,11],       ['M','13','y','x']),         # R 2 m3           [0 2 3]       R b2 b7          [0 1 a]
            'R b7 7'           : (0, [0,10,11],      ['#','13']),                 # R b2 2           [0 1 2]       R b2 7           [0 1 b]
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
            'R m3 M3 5'        : (0, [0,3,4,7],      ['#2']),                     # R b2 M3 6        [0 1 4 9]     R m3 #5 7        [0 3 8 b]     R 4 #5 6         [0 5 8 9]
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
            'R m3 #5 7'        : (1, [0,3,8,11],     ['m','M','+','7']),          # R 4 #5 6         [0 5 8 9]     R m3 M3 5        [0 3 4 7]     R b2 M3 6        [0 1 4 9]
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
            'R M3 #5 7'        : (0, [0,4,8,11],     ['+','M']),                  # R M3 5 #5        [0 4 7 8]     R m3 M3 #5       [0 3 4 8]     R b2 4 6         [0 1 5 9]
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
            'R 4 #5 7'         : (0, [0,5,8,11],     ['+','M','s4']),             # R m3 b5 5        [0 3 6 7]     R m3 M3 6        [0 3 4 9]     R b2 b5 6        [0 1 6 9]
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
            'R 2 4 #5 7'       : (1, [0,2,5,8,11],   ['M','+','7','s2','s4']),    # R m3 b5 6 b7     [0 3 6 9 a]   R m3 b5 5 6      [0 3 6 7 9]   R m3 M3 b5 6     [0 3 4 6 9]   R b2 m3 b5 6     [0 1 3 6 9]
            'R 2 4 6 b7'       : (3, [0,2,5,9,10],   ['13','s2','s4','x']),       # R m3 5 #5 b7     [0 3 7 8 a]   R M3 4 5 6       [0 4 5 7 9]   R b2 m3 4 #5     [0 1 3 5 8]   R 2 M3 5 7       [0 2 4 7 b]
            'R 2 4 6 7'        : (1, [0,2,5,9,11],   ['M','13','s2','s4','x']),   # R m3 5 6 b7      [0 3 7 9 a]   R M3 b5 5 6      [0 4 6 7 9]   R 2 m3 4 #5      [0 2 3 5 8]   R b2 m3 b5 b7    [0 1 3 6 a]
            'R 2 4 b7 7'       : (2, [0,2,5,10,11],  ['#','13','s2','s4']),       # R m3 #5 6 b7     [0 3 8 9 a]   R 4 b5 5 6       [0 5 6 7 9]   R b2 2 M3 5      [0 1 2 4 7]   R b2 m3 b5 7     [0 1 3 6 b]
            'R 2 b5 5 #5'      : (3, [0,2,6,7,8],    ['#4','b6','s2']),           # R M3 4 b5 b7     [0 4 5 6 a]   R b2 2 b5 #5     [0 1 2 6 8]   R b2 4 5 7       [0 1 5 7 b]   R M3 b5 b7 7     [0 4 6 a b]
            'R 2 b5 5 6'       : (3, [0,2,6,7,9],    ['2','#4','6']),             # R M3 4 5 b7      [0 4 5 7 a]   R b2 m3 b5 #5    [0 1 3 6 8]   R 2 4 5 7        [0 2 5 7 b]   R m3 4 6 b7      [0 3 5 9 a]
            'R 2 b5 5 b7'      : (2, [0,2,6,7,10],   ['#','11','s2']),            # R M3 4 #5 b7     [0 4 5 8 a]   R b2 M3 b5 #5    [0 1 4 6 8]   R m3 4 5 7       [0 3 5 7 b]   R 2 M3 #5 6      [0 2 4 8 9]
            'R 2 b5 5 7'       : (2, [0,2,6,7,11],   ['M','','11','s2']),         # R M3 4 6 b7      [0 4 5 9 a]   R b2 4 b5 #5     [0 1 5 6 8]   R M3 4 5 7       [0 4 5 7 b]   R b2 m3 5 #5     [0 1 3 7 8]
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
            'R b5 5 #5 b7'     : (2, [0,6,7,8,10],   ['b','13','#','11','y']),    # R b2 2 M3 b5     [0 1 2 4 6]   R b2 m3 4 7      [0 1 3 5 b]   R 2 M3 b7 7      [0 2 4 a b]   R 2 #5 6 b7      [0 2 8 9 a]
            'R b5 5 #5 7'      : (2, [0,6,7,8,11],   ['M','b','13','#','11','y']), # R b2 2 4 b5      [0 1 2 5 6]   R b2 M3 4 7      [0 1 4 5 b]   R m3 M3 b7 7     [0 3 4 a b]   R b2 5 #5 6      [0 1 7 8 9]
            'R b5 5 6 b7'      : (1, [0,6,7,9,10],   ['13','#','11','y']),        # R b2 m3 M3 b5    [0 1 3 4 6]   R 2 m3 4 7       [0 2 3 5 b]   R b2 m3 6 b7     [0 1 3 9 a]   R 2 #5 6 7       [0 2 8 9 b]
            'R b5 5 6 7'       : (3, [0,6,7,9,11],   ['M','13','#','11','y']),    # R b2 m3 4 b5     [0 1 3 5 6]   R 2 M3 4 7       [0 2 4 5 b]   R 2 m3 6 b7      [0 2 3 9 a]   R b2 5 #5 b7     [0 1 7 8 a]
            'R b5 5 b7 7'      : (2, [0,6,7,10,11],  ['#','13','#','11','y']),    # R b2 M3 4 b5     [0 1 4 5 6]   R m3 M3 4 7      [0 3 4 5 b]   R b2 2 #5 6      [0 1 2 8 9]   R b2 5 #5 7      [0 1 7 8 b]
            'R b5 #5 6 b7'     : (2, [0,6,8,9,10],   ['o','+','13','y']),         # R 2 m3 M3 b5     [0 2 3 4 6]   R b2 2 M3 b7     [0 1 2 4 a]   R b2 m3 6 7      [0 1 3 9 b]   R 2 #5 b7 7      [0 2 8 a b]
            'R b5 #5 6 7'      : (2, [0,6,8,9,11],   ['o','+','13','y']),         # R 2 m3 4 b5      [0 2 3 5 6]   R b2 m3 M3 b7    [0 1 3 4 a]   R 2 m3 6 7       [0 2 3 9 b]   R b2 5 6 b7      [0 1 7 9 a]
            'R b5 #5 b7 7'     : (4, [0,6,8,10,11],  ['o','+','#','13','y']),     # R 2 M3 4 b5      [0 2 4 5 6]   R 2 m3 M3 b7     [0 2 3 4 a]   R b2 2 #5 b7     [0 1 2 8 a]   R b2 5 6 7       [0 1 7 9 b]
            'R b5 6 b7 7'      : (1, [0,6,9,10,11],  ['o','#','13','13','y']),    # R m3 M3 4 b5     [0 3 4 5 6]   R b2 2 m3 6      [0 1 2 3 9]   R b2 2 #5 7      [0 1 2 8 b]   R b2 5 b7 7      [0 1 7 a b]
            'R 5 #5 6 b7'      : (2, [0,7,8,9,10],   ['13','b','13','y']),        # R b2 2 m3 4      [0 1 2 3 5]   R b2 2 M3 7      [0 1 2 4 b]   R b2 m3 b7 7     [0 1 3 a b]   R 2 6 b7 7       [0 2 9 a b]
            'R 5 #5 6 7'       : (0, [0,7,8,9,11],   ['+','13','y']),             # R b2 2 M3 4      [0 1 2 4 5]   R b2 m3 M3 7     [0 1 3 4 b]   R 2 m3 b7 7      [0 2 3 a b]   R b2 #5 6 b7     [0 1 8 9 a]
            'R 5 #5 b7 7'      : (2, [0,7,8,10,11],  ['+','#','13','y']),         # R b2 m3 M3 4     [0 1 3 4 5]   R 2 m3 M3 7      [0 2 3 4 b]   R b2 2 6 b7      [0 1 2 9 a]   R b2 #5 6 7      [0 1 8 9 b]
            'R 5 6 b7 7'       : (2, [0,7,9,10,11],  ['#','13','13','y']),        # R 2 m3 M3 4      [0 2 3 4 5]   R b2 2 m3 b7     [0 1 2 3 a]   R b2 2 6 7       [0 1 2 9 b]   R b2 #5 b7 7     [0 1 8 a b]
            'R #5 6 b7 7'      : (2, [0,8,9,10,11],  ['+','#','13','13','y']),    # R b2 2 m3 M3     [0 1 2 3 4]   R b2 2 m3 7      [0 1 2 3 b]   R b2 2 b7 7      [0 1 2 a b]   R b2 6 b7 7      [0 1 9 a b]
            'R b2 m3 M3 #5 6'  : (5, [0,1,3,4,8,9],  ['+','b2','#2','6']),        # R 2 m3 5 #5 7    [0 2 3 7 8 b] R b2 4 b5 6 b7   [0 1 5 6 9 a] R M3 4 #5 6 7    [0 4 5 8 9 b] R b2 M3 4 5 #5   [0 1 4 5 7 8] R m3 M3 b5 5 7   [0 3 4 6 7 b]
            'R b2 m3 4 b5 b7'  : (3, [0,1,3,5,6,10], ['o','11','b9']),            # R 2 M3 4 6 7     [0 2 4 5 9 b] R 2 m3 5 6 b7    [0 2 3 7 9 a] R b2 4 5 #5 b7   [0 1 5 7 8 a] R M3 b5 5 6 7    [0 4 6 7 9 b] R 2 m3 4 5 #5    [0 2 3 5 7 8]
            'R b2 m3 4 5 #5'   : (5, [0,1,3,5,7,8],  ['m','b2','4','b6']),        # R 2 M3 b5 5 7    [0 2 4 6 7 b] R 2 M3 4 6 b7    [0 2 4 5 9 a] R 2 m3 5 #5 b7   [0 2 3 7 8 a] R b2 4 b5 #5 b7  [0 1 5 6 8 a] R M3 4 5 6 7     [0 4 5 7 9 b]
            'R b2 m3 4 #5 b7'  : (1, [0,1,3,5,8,10], ['m','+','11','b9']),        # R 2 M3 5 6 7     [0 2 4 7 9 b] R 2 4 5 6 b7     [0 2 5 7 9 a] R m3 4 5 #5 b7   [0 3 5 7 8 a] R 2 M3 4 5 6     [0 2 4 5 7 9] R 2 m3 4 5 b7    [0 2 3 5 7 a]
            'R b2 m3 b5 #5 b7' : (3, [0,1,3,6,8,10], ['o','+','b9']),             # R 2 4 5 6 7      [0 2 5 7 9 b] R m3 4 5 6 b7    [0 3 5 7 9 a] R 2 M3 b5 5 6    [0 2 4 6 7 9] R 2 M3 4 5 b7    [0 2 4 5 7 a] R 2 m3 4 #5 b7   [0 2 3 5 8 a]
            'R b2 M3 4 5 #5'   : (4, [0,1,4,5,7,8],  ['b2','4','b6']),            # R m3 M3 b5 5 7   [0 3 4 6 7 b] R b2 m3 M3 #5 6  [0 1 3 4 8 9] R 2 m3 5 #5 7    [0 2 3 7 8 b] R b2 4 b5 6 b7   [0 1 5 6 9 a] R M3 4 #5 6 7    [0 4 5 8 9 b]
            'R b2 4 b5 #5 b7'  : (4, [0,1,5,6,8,10], ['o','+','b9','s4']),        # R M3 4 5 6 7     [0 4 5 7 9 b] R b2 m3 4 5 #5   [0 1 3 5 7 8] R 2 M3 b5 5 7    [0 2 4 6 7 b] R 2 M3 4 6 b7    [0 2 4 5 9 a] R 2 m3 5 #5 b7   [0 2 3 7 8 a]
            'R b2 4 b5 6 b7'   : (2, [0,1,5,6,9,10], ['o','13','b9','s4']),       # R M3 4 #5 6 7    [0 4 5 8 9 b] R b2 M3 4 5 #5   [0 1 4 5 7 8] R m3 M3 b5 5 7   [0 3 4 6 7 b] R b2 m3 M3 #5 6  [0 1 3 4 8 9] R 2 m3 5 #5 7    [0 2 3 7 8 b]
            'R b2 4 5 #5 b7'   : (4, [0,1,5,7,8,10], ['b','13','b9','s4']),       # R M3 b5 5 6 7    [0 4 6 7 9 b] R 2 m3 4 5 #5    [0 2 3 5 7 8] R b2 m3 4 b5 b7  [0 1 3 5 6 a] R 2 M3 4 6 7     [0 2 4 5 9 b] R 2 m3 5 6 b7    [0 2 3 7 9 a]
            'R 2 m3 4 5 #5'    : (5, [0,2,3,5,7,8],  ['m','+','2','4']),          # R b2 m3 4 b5 b7  [0 1 3 5 6 a] R 2 M3 4 6 7     [0 2 4 5 9 b] R 2 m3 5 6 b7    [0 2 3 7 9 a] R b2 4 5 #5 b7   [0 1 5 7 8 a] R M3 b5 5 6 7    [0 4 6 7 9 b]
            'R 2 m3 4 5 b7'    : (0, [0,2,3,5,7,10], ['m','11','9']),             # R b2 m3 4 #5 b7  [0 1 3 5 8 a] R 2 M3 5 6 7     [0 2 4 7 9 b] R 2 4 5 6 b7     [0 2 5 7 9 a] R m3 4 5 #5 b7   [0 3 5 7 8 a] R 2 M3 4 5 6     [0 2 4 5 7 9]
            'R 2 m3 4 #5 b7'   : (1, [0,2,3,5,8,10], ['m','+','11','9']),         # R b2 m3 b5 #5 b7 [0 1 3 6 8 a] R 2 4 5 6 7      [0 2 5 7 9 b] R m3 4 5 6 b7    [0 3 5 7 9 a] R 2 M3 b5 5 6    [0 2 4 6 7 9] R 2 M3 4 5 b7    [0 2 4 5 7 a]
            'R 2 m3 5 #5 b7'   : (3, [0,2,3,7,8,10], ['m','b','13','9']),         # R b2 4 b5 #5 b7  [0 1 5 6 8 a] R M3 4 5 6 7     [0 4 5 7 9 b] R b2 m3 4 5 #5   [0 1 3 5 7 8] R 2 M3 b5 5 7    [0 2 4 6 7 b] R 2 M3 4 6 b7    [0 2 4 5 9 a]
            'R 2 m3 5 #5 7'    : (3, [0,2,3,7,8,11], ['m','M','b','13','9']),     # R b2 4 b5 6 b7   [0 1 5 6 9 a] R M3 4 #5 6 7    [0 4 5 8 9 b] R b2 M3 4 5 #5   [0 1 4 5 7 8] R m3 M3 b5 5 7   [0 3 4 6 7 b] R b2 m3 M3 #5 6  [0 1 3 4 8 9]
            'R 2 m3 5 6 b7'    : (2, [0,2,3,7,9,10], ['m','13','9']),             # R b2 4 5 #5 b7   [0 1 5 7 8 a] R M3 b5 5 6 7    [0 4 6 7 9 b] R 2 m3 4 5 #5    [0 2 3 5 7 8] R b2 m3 4 b5 b7  [0 1 3 5 6 a] R 2 M3 4 6 7     [0 2 4 5 9 b]
            'R 2 M3 4 5 6'     : (5, [0,2,4,5,7,9],  ['2','4','6']),              # R 2 m3 4 5 b7    [0 2 3 5 7 a] R b2 m3 4 #5 b7  [0 1 3 5 8 a] R 2 M3 5 6 7     [0 2 4 7 9 b] R 2 4 5 6 b7     [0 2 5 7 9 a] R m3 4 5 #5 b7   [0 3 5 7 8 a]
            'R 2 M3 4 5 b7'    : (0, [0,2,4,5,7,10], ['11','9']),                 # R 2 m3 4 #5 b7   [0 2 3 5 8 a] R b2 m3 b5 #5 b7 [0 1 3 6 8 a] R 2 4 5 6 7      [0 2 5 7 9 b] R m3 4 5 6 b7    [0 3 5 7 9 a] R 2 M3 b5 5 6    [0 2 4 6 7 9]
            'R 2 M3 4 6 b7'    : (2, [0,2,4,5,9,10], ['13','11','9','x']),        # R 2 m3 5 #5 b7   [0 2 3 7 8 a] R b2 4 b5 #5 b7  [0 1 5 6 8 a] R M3 4 5 6 7     [0 4 5 7 9 b] R b2 m3 4 5 #5   [0 1 3 5 7 8] R 2 M3 b5 5 7    [0 2 4 6 7 b]
            'R 2 M3 4 6 7'     : (0, [0,2,4,5,9,11], ['M','13','11','9','x']),    # R 2 m3 5 6 b7    [0 2 3 7 9 a] R b2 4 5 #5 b7   [0 1 5 7 8 a] R M3 b5 5 6 7    [0 4 6 7 9 b] R 2 m3 4 5 #5    [0 2 3 5 7 8] R b2 m3 4 b5 b7  [0 1 3 5 6 a]
            'R 2 M3 b5 5 6'    : (5, [0,2,4,6,7,9],  ['2','#4','6']),             # R 2 M3 4 5 b7    [0 2 4 5 7 a] R 2 m3 4 #5 b7   [0 2 3 5 8 a] R b2 m3 b5 #5 b7 [0 1 3 6 8 a] R 2 4 5 6 7      [0 2 5 7 9 b] R m3 4 5 6 b7    [0 3 5 7 9 a]
            'R 2 M3 b5 5 7'    : (1, [0,2,4,6,7,11], ['M','#','11','9']),         # R 2 M3 4 6 b7    [0 2 4 5 9 a] R 2 m3 5 #5 b7   [0 2 3 7 8 a] R b2 4 b5 #5 b7  [0 1 5 6 8 a] R M3 4 5 6 7     [0 4 5 7 9 b] R b2 m3 4 5 #5   [0 1 3 5 7 8]
            'R 2 M3 b5 #5 b7'  : (0, [0,2,4,6,8,10], ['+','#','11','9']),         # R 2 M3 b5 #5 b7  @0 2 4 6 8 a@ R 2 M3 b5 #5 b7  @0 2 4 6 8 a@ R 2 M3 b5 #5 b7  @0 2 4 6 8 a@ R 2 M3 b5 #5 b7  @0 2 4 6 8 a@ R 2 M3 b5 #5 b7  @0 2 4 6 8 a@
            'R 2 M3 5 6 7'     : (3, [0,2,4,7,9,11], ['M','13','9']),             # R 2 4 5 6 b7     [0 2 5 7 9 a] R m3 4 5 #5 b7   [0 3 5 7 8 a] R 2 M3 4 5 6     [0 2 4 5 7 9] R 2 m3 4 5 b7    [0 2 3 5 7 a] R b2 m3 4 #5 b7  [0 1 3 5 8 a]
            'R 2 4 5 6 b7'     : (4, [0,2,5,7,9,10], ['13','s2','s4']),           # R m3 4 5 #5 b7   [0 3 5 7 8 a] R 2 M3 4 5 6     [0 2 4 5 7 9] R 2 m3 4 5 b7    [0 2 3 5 7 a] R b2 m3 4 #5 b7  [0 1 3 5 8 a] R 2 M3 5 6 7     [0 2 4 7 9 b]
            'R 2 4 5 6 7'      : (4, [0,2,5,7,9,11], ['M','13','s2','s4']),       # R m3 4 5 6 b7    [0 3 5 7 9 a] R 2 M3 b5 5 6    [0 2 4 6 7 9] R 2 M3 4 5 b7    [0 2 4 5 7 a] R 2 m3 4 #5 b7   [0 2 3 5 8 a] R b2 m3 b5 #5 b7 [0 1 3 6 8 a]
            'R m3 M3 b5 5 7'   : (0, [0,3,4,6,7,11], ['M','#','11','#9']),        # R b2 m3 M3 #5 6  [0 1 3 4 8 9] R 2 m3 5 #5 7    [0 2 3 7 8 b] R b2 4 b5 6 b7   [0 1 5 6 9 a] R M3 4 #5 6 7    [0 4 5 8 9 b] R b2 M3 4 5 #5   [0 1 4 5 7 8]
            'R m3 4 5 #5 b7'   : (2, [0,3,5,7,8,10], ['m','b','13','11']),        # R 2 M3 4 5 6     [0 2 4 5 7 9] R 2 m3 4 5 b7    [0 2 3 5 7 a] R b2 m3 4 #5 b7  [0 1 3 5 8 a] R 2 M3 5 6 7     [0 2 4 7 9 b] R 2 4 5 6 b7     [0 2 5 7 9 a]
            'R m3 4 5 6 b7'    : (2, [0,3,5,7,9,10], ['m','13','11']),            # R 2 M3 b5 5 6    [0 2 4 6 7 9] R 2 M3 4 5 b7    [0 2 4 5 7 a] R 2 m3 4 #5 b7   [0 2 3 5 8 a] R b2 m3 b5 #5 b7 [0 1 3 6 8 a] R 2 4 5 6 7      [0 2 5 7 9 b]
            'R M3 4 5 6 7'     : (0, [0,4,5,7,9,11], ['M','13','11']),            # R b2 m3 4 5 #5   [0 1 3 5 7 8] R 2 M3 b5 5 7    [0 2 4 6 7 b] R 2 M3 4 6 b7    [0 2 4 5 9 a] R 2 m3 5 #5 b7   [0 2 3 7 8 a] R b2 4 b5 #5 b7  [0 1 5 6 8 a]
            'R M3 4 #5 6 7'    : (1, [0,4,5,8,9,11], ['+','M','13','11']),        # R b2 M3 4 5 #5   [0 1 4 5 7 8] R m3 M3 b5 5 7   [0 3 4 6 7 b] R b2 m3 M3 #5 6  [0 1 3 4 8 9] R 2 m3 5 #5 7    [0 2 3 7 8 b] R b2 4 b5 6 b7   [0 1 5 6 9 a]
            'R M3 b5 5 6 7'    : (1, [0,4,6,7,9,11], ['M','13','#','11']),        # R 2 m3 4 5 #5    [0 2 3 5 7 8] R b2 m3 4 b5 b7  [0 1 3 5 6 a] R 2 M3 4 6 7     [0 2 4 5 9 b] R 2 m3 5 6 b7    [0 2 3 7 9 a] R b2 4 5 #5 b7   [0 1 5 7 8 a]
            }
    ####################################################################################################################################################################################################
    #################################
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

    def add2cat(self, limap, cc):
        self.dumpLimap(limap, cc)
        outer = []   ;   keys, ivals = [], []
        for i in limap:
            inner = []
            for j in i[0]:
                inner.append(INTERVAL_RANK[j])
            tmp = tuple(inner)
            outer.append(tmp)
            self.cat2.add(tmp)
            k = len(inner)
            if k not in self.cat3:     self.cat3[k] = set()   ;   self.cat3[k].add(tmp)
            else:                      self.cat3[k].add(tmp)
            if tmp not in self.catmap: self.catmap[tmp] = [i[0], i[1]]
            keys.append(tmp)   ;   ivals.append(i[0])
        for k in keys:
            self.catmap2[k] = [sorted(keys), sorted(ivals, key=lambda b: [INTERVAL_RANK[c] for c in b])]
        outer = sorted(outer, key=lambda a: [z for z in a])
        self.cat1.add(tuple(outer))
#        self.log(f'{why}', end='')
#        for o in outer:
#            self.log(f'{tabs.fmtl(o, z="x", d2="] ")}', ind=0, end='',  file=self.logFile)
#        self.log(ind=0)

    def dumpInstanceCat(self, why=''):
        cat1 = sorted(self.cat1)
        cat2 = sorted(self.cat2)
        cat3 = self.cat3
        catmap = self.catmap
        catmap2 = self.catmap2
        self.log(f'{why} cat1 <{len(cat1)}>')
        n = 0
        for c in cat1:
            n += len(c)
            self.log(f'{n:3} {tabs.fmtl(c, z="x")}', ind=0)
        self.log(f'{why} cat2 <{len(cat2)}>')
        self.log(f'{tabs.fmtl(cat2, z="x")}', ind=0)
        for i, c in enumerate(cat2):
            self.log(f'{i+1:3} {tabs.fmtl(c, z="x")}', ind=0)
        self.log(f'{why} cat3 <{len(cat3)}>')
        self.log(f'{tabs.fmtm(cat3)}', ind=0,  file=self.logFile)
        for k in cat3.keys():
            cat3[k] = sorted(tuple(cat3[k]))
            for j, v in enumerate(cat3[k]):
                self.log(f'{j+1:3} {tabs.fmtl(v, z="x")}', ind=0)
        self.log(f'{why} catmap <{len(catmap)}>')
        self.log(f'{tabs.fmtm(catmap)}', ind=0,  file=self.logFile)
        for i, (k,v) in enumerate(catmap.items()):
            self.log(f'{i+1:3} {tabs.fmtl(k, z="x")} {tabs.fmtl(v, w=2)}', ind=0)
        self.log(f'{why} catmap2 <{len(catmap2)}>')
        self.log(f'{tabs.fmtm(catmap2)}', ind=0,  file=self.logFile)
        for k in cat3.keys():
            for i, v in enumerate(cat3[k]):
                self.log(f'{i+1:3} {tabs.fmtl(v, z="x")}', ind=0, end='  ')
                for j, u in enumerate(catmap2[v]):
                    for h, w in enumerate(u):
                        if j:        self.log(f'{"" if h else "  "}{tabs.fmtl(w, w=tabs.FMTN2)}', ind=0, end='')
                        elif w != v: self.log(f'{                   tabs.fmtl(w,        z="x")}', ind=0, end='')
                self.log(ind=0)
