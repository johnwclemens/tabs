import sys, os, collections
sys.path.insert(0, os.path.abspath('.'))
import tabs

VERBOSE = 0 # tabs.VERBOSE
NO5 = 'x'
AUG = '+'
NO3 = 'y'

class Note(object):
    count       = 0
    FLAT, SHARP = 0, 1
    TYPE        = FLAT
    TYPES       = ['FLAT', 'SHARP']
    NTONES      = 12
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

    def __init__(self, i):
        assert i < 0
        self.index = i
        self.name  = self.TONES[Note.TYPE][i % self.NTONES]
        Note.count += 1
        tabs.Tabs.dumpObj(obj=self, name=f'{self.name} Note', why=f'count={Note.count}')
    @staticmethod
    def setType(t): Note.TYPE = t

    @staticmethod
    def getName(i):
        name = Note.TONES[Note.TYPE][i % Note.NTONES]
        return name

    @staticmethod
    def getFreq(index): return 440 * pow(pow(2, 1/Note.NTONES), index - Note.INDICES)

####################################################################################################################################################################################################
class DSymb(object):
    SYMBS = {'X': 'mute', '/': 'slide', '\\': 'bend', '+': 'hammer', '~': 'vibrato', '^': 'tie', '.': 'staccato', '_': 'legato', '%': 'repeat', '|': 'bar', '[': 'groupL', ']': 'groupR'}
####################################################################################################################################################################################################

class Chord(object):
    INTERVALS     = { 0:'R', 1:'b2', 2:'2', 3:'m3', 4:'M3', 5:'4', 6:'b5', 7:'5', 8:'#5', 9:'6', 10:'b7', 11:'7' }
    INTERVAL_RANK = { 'R':0, 'b2':1, '2':2, 'm3':3, 'M3':4, '4':5, 'b5':6, '5':7, '#5':8, '6':9, 'b7':10, '7':11 }
    _count        = 0
    def __init__(self, tobj, logfile):
        self.tobj    = tobj
        self.logFile = logfile
        self.limap, self.limap1, self.limap2 = [], [], []
        self.mlimap, self.mimEmpty, self.mimPart, self.mimFull = {}, {}, {}, {}
        self.catmap, self.catmap2 = {}, {}
        self.cat1, self.cat2, self.cat3 = set(), set(), dict()
        Chord._count += 1
        self.log(f'ChordNameMap len={len(self.chordNameMap)}')
#        tabs.Tabs.dumpObj(obj=self, name=f'ChordNameMap<{len(self.chordNameMap)}>', why=f'count={Chord._count}', file={logfile})

    def log(self, msg='', ind=1, file=None, flush=False, sep=',', end='\n'):
        if file is None: file=self.logFile
        tabs.Tabs.log(msg=msg, ind=ind, file=file, flush=flush, sep=sep, end=end)

    def updateImap(self, im, name, chunks, dbg=0, dbg2=0):
        intervals = list(im.keys())    ;   notes = list(im.values())     # ;   order = len(self.tobj.stringNumbs)  # ;   omapK = []
        imap = [intervals, notes, name, chunks]  ;   d1, d2 = '<', '>'   ;   chordName = ''
        if name:
            omapK = ' '.join(intervals)
            if omapK in Chord.OMAP:
                order = Chord.OMAP[omapK][0]
                if dbg: self.log(f'omapk={omapK} intervals={tabs.fmtl(intervals)} order={order}')
                self.limap1.insert(order, imap)  ;   self.dumpImap(imap, f'insert(imap) {order}')
##            omapK = ' '.join(intervals)
##            if omapK in Chord.OMAP:
##                order = Chord.OMAP[omapK]
##            if dbg: self.log(f'omapk={omapK} intervals={tabs.fmtl(intervals)} order={order}')
##            self.limap1.insert(order, imap)  ;   self.dumpImap(imap, f'insert(imap) {order}')
#            self.log(f'OMAP {type(Chord.OMAP)}  RANK {type(Chord.INTERVAL_RANK)}  omapK {type(omapK)} OMK {type(Chord.OMAP.keys())}')  #       self.log(f'value {type(Chord.OMAP[omapK])}')
#            for i in intervals:
#                omapK.append(Chord.INTERVAL_RANK[i])
#            omapK = tuple(omapK)
#            if omapK in Chord.OMAP:
#                order = Chord.OMAP[omapK]
#                if dbg: self.log(f'omapk={omapK} intervals={tabs.fmtl(intervals)} order={order}')
#            self.limap1.insert(order, imap)             ;  self.dumpImap(imap, f'insert(imap) {order}') #     self.log(f'limap1 insert {order} {tabs.fmtl(imap)}')
#            if not order: self.limap1.insert(0, imap)   ;  self.dumpImap(imap, 'insert(imap)  ') #  self.log(f'limap1 insert {order} {tabs.fmtl(imap):2}')
#            else:         self.limap1.append(imap)      ;  self.dumpImap(imap, 'append(imap)  ') #  self.log(f'limap1 add      {tabs.fmtl(imap):2}')
        else:             self.limap2.append(imap)     # ;   self.log(f'limap2 add      {tabs.fmtl(imap)}')
        if dbg2:
            for i, m in enumerate(self.limap1):
                self.log(tabs.FMTR.format(f'  limap1 [{i+1}] [ <{m[2]:<6}> {tabs.fmtl(m[0], 2, "<", d1, d2):17} {tabs.fmtl(m[1], 2, "<", d1, d2):17} ]'))
            for i, m in enumerate(self.limap2):
                self.log(tabs.FMTR.format(f'  limap2 [{i+1}] [ <{m[2]:<6}> {tabs.fmtl(m[0], 2, "<", d1, d2):17} {tabs.fmtl(m[1], 2, "<", d1, d2):17} ]'))
        if   self.limap1 and self.limap1[0]: chordName = self.limap1[0][2]  ;  chunks = self.limap1[0][3]
        elif self.limap2 and self.limap2[0]: chordName = self.limap2[0][2]  ;  chunks = self.limap2[0][3]
        return chordName, chunks

    def getChordName(self, p, l, c, dbg=0, dbg2=0):
        cc = c + l * self.tobj.n[tabs.C]
#        if dbg: self.log(f'p l c cc = {p} {l} {c} {cc} mlimap.keys={tabs.fmtl(list(self.mlimap.keys()))}:')
#        if dbg: self.dumpMLimap('Get Chord Name')
        self.limap, chunks, ims = [], [], set()   ;   chordName = ''
        imapKeys, imapNotes                     = None, None   ;   d1, d2 = '<', '>'
        mask, notes, indices                    = self.getNotesIndices(p, l, c)
        for i in range(len(indices)):
            intervals                           = self.getIntervals(indices,  i,     mask)
            imap, imapKeys, imapNotes, chordKey = self.getImapKeys(intervals, notes)
            imk = tuple(imapKeys)
            if dbg: self.log(f'imk={tabs.fmtl(imk)} ims={tabs.fmtl(ims)}')
            if imk not in ims:
                ims.add(imk)
                chordName, chunks               = self._getChordName(imap)
                if dbg and chordName: self.log(f'Inner Chord  [ <{chordName:<6}> {tabs.fmtl(imapKeys, 2, "<", d1, d2):17} {tabs.fmtl(imapNotes, 2, "<", d1, d2):17} ] {tabs.fmtl(chunks)}')
                chordName, chunks               = self.updateImap(imap, chordName, chunks)
        self.limap.extend(self.limap1)      ;     self.limap.extend(self.limap2)
        if chordName:
            if dbg: self.log(f'Outer Chord  [ <{chordName:<6}> {tabs.fmtl(imapKeys, 2, "<", d1, d2):17} {tabs.fmtl(imapNotes, 2, "<", d1, d2):17} ] {tabs.fmtl(chunks)}')
            self.mlimap[cc]                     = self.limap
            if self.limap2:    self.mimPart[cc] = self.limap
            else:              self.mimFull[cc] = self.limap
            self.add2cat(self.limap, cc)
        elif self.limap2:     self.mimEmpty[cc] = self.limap2   ;   self.dumpLimap(self.limap2, cc)
        if dbg2:
            for i, m in enumerate(self.limap):
                self.log(tabs.FMTR.format(f'limap0 {i+1} [ <{m[2]:<9}>  {tabs.fmtl(m[0], 2, "<", d1, d2):17} {tabs.fmtl(m[1], 2, "<", d1, d2):17} ] {tabs.fmtl(m[3])}'))
        self.limap1, self.limap2 = [], []
        return chordName, chunks

    def add2cat(self, limap, cc, why=''):
        self.dumpLimap(limap, cc, why)
        outer = []   ;   keys, ivals = [], []
        for i in limap:
            inner = []
            for j in i[0]:
                inner.append(self.INTERVAL_RANK[j])
            tmp = tuple(inner)
            outer.append(tmp)
            self.cat2.add(tmp)
            k = len(inner)
            if k not in self.cat3:     self.cat3[k] = set()   ;   self.cat3[k].add(tmp)
            else:                      self.cat3[k].add(tmp)
            if tmp not in self.catmap: self.catmap[tmp] = [i[0], i[1]]
            keys.append(tmp)   ;   ivals.append(i[0])
        for k in keys:
            self.catmap2[k] = [sorted(keys), sorted(ivals, key=lambda b: [self.INTERVAL_RANK[c] for c in b])]
        outer = sorted(outer, key=lambda a: [z for z in a])
        self.cat1.add(tuple(outer))
#        self.log(f'{why}', end='')
#        for o in outer:
#            self.log(f'{tabs.fmtl(o, z="x", d2="] ")}', ind=0, end='',  file=self.logFile)
#        self.log(ind=0)

    def toggleChordName(self, rev=0, dbg=0):
        p, l, s, c, t = self.tobj.j()
        cc = c + l * self.tobj.n[tabs.C]
        if dbg: self.log(f'p l c cc = {p} {l} {c} {cc} rev={rev}')
        if cc in self.mlimap.keys():
            limap = self.mlimap[cc]
            if dbg: self.dumpLimap(limap, cc, why=f'before p l c cc = {p} {l} {c} {cc} rev={rev}')
            if rev: tmp0 = limap[-1]  ;   tmp1 = limap[:-1]  ;   limap  = tmp1   ;   limap.insert(0, tmp0)
            else:   tmp0 = limap[0]   ;   tmp1 = limap[1:]   ;   limap  = tmp1   ;   limap.append(tmp0)
            self.mlimap[cc] = limap
            if dbg: self.dumpLimap(limap, cc, why=f'after  p l c cc = {p} {l} {c} {cc} rev={rev}')
            return limap[0][2], limap[0][3]
        else: self.log(f'ERROR: cc={cc} not map key {tabs.fmtl(list(self.mlimap.keys()))}')
   ####################################################################################################################################################################################################
    def getNotesIndices(self, p, l, c, dbg=VERBOSE, dbg2=0):
        strNumbs   = self.tobj.stringNumbs
        strKeys    = self.tobj.stringKeys
        strNames   = self.tobj.stringNames
        _tabs      = self.tobj.data[p][l][c]
        strIndices = [Note.INDICES[k] for k in strKeys]
        notes = []  ;  nt = len(_tabs)  ;   mask = []
        if dbg2: self.log(f'p l c = {p} {l} {c} text={_tabs}')
        for t in range(nt):
            if tabs.Tabs.isFret(_tabs[t]): mask.insert(0, 1)  ;  note = self.tobj.getNoteName(t, _tabs[t])  ;  notes.insert(0, note)
            else:                          mask.insert(0, 0)
        indices = []
        for t in range(nt):
            index = self.tobj.getNoteIndex(t, self.tobj.getFretNum(_tabs[t])) if tabs.Tabs.isFret(_tabs[t]) else 0
#            index = int(self.tobj.getNote(t, _tabs[t]).index) if tabs.Tabs.isFret(_tabs[t]) else 0
            if index: indices.insert(0, index)
        if notes:
            mask0 = [1] * self.tobj.n[tabs.T]
            if dbg2: self.dumpData(strNumbs,   mask0, 'strNumbs', r=1)
            if dbg2: self.dumpData(strKeys,    mask0, 'strKeys')
            if dbg2: self.dumpData(strIndices, mask0, 'strIndices')
            if dbg2: self.dumpData(strNames,   mask0, 'strNames', r=1)
            if dbg:  self.dumpData(_tabs,      mask0, 'Tabs',     r=1)
            if dbg:  self.dumpData(notes,      mask,  'Notes')
            if dbg2: self.dumpData(indices,    mask,  'Indices')
        return mask, notes, indices

    def getIntervals(self, indices, j, mask, order=1, dbg=VERBOSE):
        deltas = []   ;   nst = Note.NTONES
        for i in indices:
            if i - indices[j] >= 0:
                if order: deltas.append((i - indices[j]) % nst)
                else:     deltas.insert(0, (i - indices[j]) % nst)
            else:
                d = (indices[j] - i) % nst
                delta = nst - d
                if delta == nst: delta = 0
                if order: deltas.append(delta)
                else:     deltas.insert(0, delta)
        intervals = []
        for d in deltas:
            intervals.append(self.INTERVALS[d])
        if dbg: self.dumpData(deltas,    mask, 'Deltas')
        if dbg: self.dumpData(intervals, mask, 'Intervals')
#        if dbg: self.dumpData(list(ivset), [1]*len(ivset), 'IvSet')
        return intervals

    def getImapKeys(self, intervals, notes, dbg=VERBOSE, dbg2=VERBOSE):
        imap      = collections.OrderedDict(sorted(dict(zip(intervals, notes)).items(), key=lambda t: self.INTERVAL_RANK[t[0]]))
        imapKeys  = list(imap.keys())
        imapNotes = list(imap.values())
        chordKey  = ' '.join(imapNotes)
        mask      = [1] * len(imapKeys)
        if dbg:  self.dumpData(imap,      mask, 'imap')
        if dbg2: self.dumpData(imapKeys,  mask, 'imapKeys')
        if dbg2: self.dumpData(imapNotes, mask, 'imapNotes')
#        if dbg2: self.dumpData(list(chordKey), [1]*len(chordKey), 'chordKey')
        '''
        sdeltas, rdeltas, relimapKeys = [], [], ['R']
        for k in imapKeys:
            sdeltas.append(self.INTERVAL_RANK[k])
            rdeltas.insert(0, self.INTERVAL_RANK[k])
        if dbg: self.dumpData(sdeltas, mask, 'SDeltas')
        if dbg: self.dumpData(rdeltas, mask, 'RDeltas')
        for (i, sd) in enumerate(sdeltas):
            relimapKeys.append(self.INTERVALS[rdeltas[i]])
        if dbg: self.dumpData(relimapKeys, mask, 'RelImapKeys')
        '''
        return imap, imapKeys, imapNotes, chordKey
    ####################################################################################################################################################################################################
    def dumpCat(self, why=''):
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

    def dumpMLimap(self, why=''):
        self._dumpMLimap(self.mlimap,   f'{why} Mlimap')
        self._dumpMLimap(self.mimEmpty, f'{why} Empty')
        self._dumpMLimap(self.mimPart,  f'{why} Part')
        self._dumpMLimap(self.mimFull,  f'{why} Full')

    def _dumpMLimap(self, mlimap, why=''):
        self.log(f'{why} len={len(mlimap)}')        ;   count1, count2 = 0, 0
        for i, (k, v) in enumerate(mlimap.items()):
            self.dumpLimap(v, k)
        for i, (k, v) in enumerate(mlimap.items()):
            self.log(f'{i+1:3} {k:3}', ind=0, end=' ')
            for j in range(len(v)):
                tmp = f'{tabs.fmtl(v[j][0], w=tabs.FMTN2, d1="", d2="")}'   ;   count1 += 1
                if v[j][2]: count2 += 1
                self.log(f'{v[j][2]:7}|{tmp:16}', ind=0, end='')
            self.log(ind=0)
        if count1: self.log(f'{why} len={len(mlimap)} count=({count2} / {count1})={count2/count1:6.4} ')

    def dumpLimap(self, limap, cc, why=''):
        aa, bb = [], []  ;  sl = len(self.tobj.stringNumbs)  ;  lc = [0] * sl  ;  ln = [' ' for _ in range(sl)]  # ;  aa2 = []
        ll = len(limap)   ;   llb = len(limap[0][0])   ;   pos = 53   # ;   lla = len(limap[0])
        for j in range(len(limap[0][1])):
            ln[j]  = limap[0][1][j]
        for i, m in enumerate(limap):
            lc[i] = 1 if m[2] else 'X'
            bb.append(m[0])
            aa.append([Chord.INTERVAL_RANK[j] for j in m[0]])
#        self.log(f'len(ln)={len(ln)} len(lc)={len(lc)} ll={ll}, lla={lla}, llb={llb} aa = {tabs.fmtl(aa, z="x")}', ind=0, file=sys.stdout)
#        for i in range(sl):
#            if i < ll:  aa2.append( [ Chord.INTERVAL_RANK[j] for j in limap[i][0] ] )   # ;   aa2.append( [ ' ' for _ in range(sl - ll) ] )
#            else:                     aa2.append( [ '-' for _ in range(sl - ll) ] )
        self.log(f'{why}{cc+1:3} {tabs.fmtl(lc, d1="", d2="", sep="")} {tabs.fmtl(ln, w=2, d1="", d2="")}', ind=0, end=' ')
        for j in range(len(aa)):
            self.log(f'{tabs.fmtl(aa[j],  z="x",       d1="" if j else "|", d2="|")}', ind=0, end='' if j<len(aa)-1 else tabs.Z*(pos-(2*ll*llb)))
#        for j in range(len(aa2)):
#            if j < ll: self.log(f'{tabs.fmtl(aa2[j], z="x", d1="" if j else "|", d2="|")}', ind=0, end='')  #  if j<len(aa2) else '  ')
#            else:      self.log(f'{tabs.fmtl(aa2[j],   d1="" if j else "|", d2="|")}', ind=0, end='') #   if j<len(aa2) else '  ')
        for i in range(len(bb)):
            self.log(f'{tabs.fmtl(bb[i], w=tabs.FMTN2, d1="" if i else "|", d2="|")}', ind=0, end='' if i<len(bb)-1 else "\n")

    def dumpImap(self, imap, why):
        intervals = imap[0]   ;   imapNotes = imap[1]   ;   chordName = imap[2]   ;   chunks = imap[3] ;   d1, d2 = '[', ']'
        self.log(f'{why}  [ [{chordName:6}] {tabs.fmtl(intervals, w=2, d1=d1, d2=d2):17} {tabs.fmtl(imapNotes, w=2, d1=d1, d2=d2):17} ] {tabs.fmtl(chunks)}')

    def dumpData(self, data, mask, why, w=5, u='<', r=0):
        lf = self.logFile
        if r:     data = data[::-1]  ;  mask = mask[::-1]
        j = 0   ;   dt = type(data)  ;  self.log(f'{why:21} [ ', end='', file=lf)
        if dt is list or dt is str:
            for i in range(len(mask)):
                if mask[i]: self.log('{:{}{}} '.format(data[j], u, w), ind=0, end='', file=lf)  ;  j += 1
                else:       self.log('{:{}{}} '.format('-',     u, w), ind=0, end='', file=lf)
        elif dt is collections.OrderedDict:
            w2 = 2  ;   i = 0
            for k,v in data.items():
                while not mask[i]: self.log('{:{}{}} '.format('-', u, w),    ind=0, end='', file=lf)  ;  i += 1
                self.log('{:>{}}{}{:<{}} '.       format(k, w2, ':', v, w2), ind=0, end='', file=lf)  ;  i += 1
            while i < len(mask): self.log('{:{}{}} '.  format('-', u, w),    ind=0, end='', file=lf)  ;  i += 1
        else: self.log(f'type={dt} ', ind=0, end='', file=lf)
        self.log(']',                 ind=0,         file=lf)
    ####################################################################################################################################################################################################
    def _getChordName(self, imap, dbg=0):
        key = ' '.join(imap.keys())
        root, name, chunks = '', [], []
        if key in self.chordNameMap:
            name = self.chordNameMap[key]  ;  root = imap['R']
            if dbg: self.log(f'    Found key=<{key}> root={root} name={tabs.fmtl(name)}')
        elif dbg:   self.log(f'Not Found key=<{key}> root={root} name={tabs.fmtl(name)}')
        if root: chunks.append(root)
        [chunks.append(n) for n in name]
        chordName = ''.join(chunks[:])
        if dbg: self.log(f'chordName=<{chordName}> chunks={tabs.fmtl(chunks)}')
        return chordName, chunks
    ####################################################################################################################################################################################################
    #    0  1  2  3  4  5  6  7  8   9  10 11 0
    #    R  b2 2  m3 M3 4  b5 5  #5  6  b7 7  R
    #       b9 9  #9    11 #11   b13 13
    ####################################################################################################################################################################################################
    chordNameMap = {
        'R m3 b5 #5'    : ['o', f'{AUG}'],
        'R M3 4 6 7'    : ['M', '13', '11', f'{NO5}'],       #  Maj 13 11  No5
        'R m3 4 6 b7'   : ['m', '13', '11', f'{NO5}'],       #  Min 13 11  No5
        'R b2 4 #5 b7'  : ['b9', 's4', f'{AUG}'],            #  b9 sus4 Aug
        'R b2 m3 b5 b7' : ['07', 'b9'],                      #  Min 7 b5 b9
        'R b2 4 b7'     : ['11', 'b9', f'{NO5}'],            #  11 b9  No5
        'R M3 4 6 b7'   : ['13', '11', f'{NO5}'],            #  13 11  No5
        'R 2 5'         : ['s2'],                            #  sus2
        'R 2 #5'        : ['s2', f'{AUG}'],                  #  sus2  Aug
        'R 4 5'         : ['s4'],                            #  sus4
        'R 4 #5'        : ['s4', f'{AUG}'],                  #  sus4  Aug
        'R 2 4'         : ['s2', 's4', f'{NO5}'],            #  sus2sus4  No5
        'R 2 4 5'       : ['s2', 's4'],                      #  sus2sus4
        'R 2 6'         : ['6', 's2', f'{NO5}'],             #  6 sus2  No5
        'R 2 5 6'       : ['6', 's2'],                       #  6 sus2
        'R 2 b5 6'      : ['s2', 'o', '6'],                  #  sus2 6 b5
        'R 4 6'         : ['6', 's4', f'{NO5}'],             #  6 sus4  No5
        'R 4 5 6'       : ['6', 's4'],                       #  6 sus4
        'R 2 4 6'       : ['6', '/9', 's4', f'{NO5}'],       #  6/9 sus4  No5
        'R 2 4 5 6'     : ['6', '/9', 's4'],                 #  6/9 sus4
        'R 2 b7'        : ['7', 's2', f'{NO5}'],             #  7 sus2  No5
        'R 2 #5 b7'     : ['7', 's2', f'{AUG}'],             #  7 sus2  Aug
        'R 2 5 b7'      : ['7', 's2'],                       #  7 sus2
        'R 4 b7'        : ['7', 's4', f'{NO5}'],             #  7 sus4  No5
        'R 4 #5 b7'     : ['7', 's4', f'{AUG}'],             #  7 sus4  Aug
        'R 4 5 b7'      : ['7', 's4'],                       #  7 sus4
        'R 2 4 b7'      : ['7', 's2', 's4', f'{NO5}'],       #  7 sus2sus4  No5
        'R 2 4 5 b7'    : ['7', 's2', 's4'],                 #  7 sus2sus4
        'R 2 6 b7'      : ['13', 's2', f'{NO5}'],            #  13 sus2  No5  # Shadows # ?
        'R 2 5 6 b7'    : ['13', 's2'],                      #  13 sus2       # Shadows # ?
        'R 4 6 b7'      : ['13', 's4', f'{NO5}'],            #  13 sus4  No5
        'R 4 5 6 b7'    : ['13', 's4'],                      #  13 sus4
        'R 2 4 6 b7'    : ['13', 's2', 's4', f'{NO5}'],      #  13 sus2sus4  No5
        'R 2 4 5 6 b7'  : ['13', 's2', 's4'],                #  13 sus2sus4
        'R 2 7'         : ['M7', 's2', f'{NO5}'],            #  Maj 7 sus2  No5
        'R 2 5 7'       : ['M7', 's2'],                      #  Maj 7 sus2
        'R 4 7'         : ['M7', 's4', f'{NO5}'],            #  Maj 7 sus4  No5
        'R 4 5 7'       : ['M7', 's4'],                      #  Maj 7 sus4
        'R 2 4 7'       : ['M7', 's2', 's4', f'{NO5}'],      #  Maj 7 sus2sus4  No5
        'R 2 4 5 7'     : ['M7', 's2', 's4'],                #  Maj 7 sus2sus4
        'R 2 4 6 7'     : ['M', '13', 's2', 's4', f'{NO5}'], #  Maj 13 sus2sus4  No5
        'R 2 4 5 6 7'   : ['M', '13', 's2', 's4'],           #  Maj 13 sus2sus4
        'R M3 5'        : [],                          #  Major
        'R b2 M3 5'     : ['b2'],                      #  b2
        'R 2 M3 5'      : ['2'],                       #  2
        'R M3 4 5'      : ['4'],                       #  4
        'R M3 6'        : ['6', f'{NO5}'],             #  6  No5
        'R M3 5 6'      : ['6'],                       #  6
        'R M3 4 6'      : ['6', '/4', f'{NO5}'],       #  6/4  No5
        'R M3 b7'       : ['7', f'{NO5}'],             #  7  No5
        'R M3 5 b7'     : ['7'],                       #  7
        'R M3 7'        : ['M7', f'{NO5}'],            #  Maj 7  No5
        'R M3 5 7'      : ['M7'],                      #  Maj 7
        'R 2 M3 6'    : ['6', '/9', f'{NO5}'],       #  add 6/9  No5
        'R 2 M3 5 6'  : ['6', '/9'],                 #  add 6/9
        'R 2 M3 7'    : ['M9', f'{NO5}'],            #  Maj 9  No5
        'R 2 M3 5 7'  : ['M9'],                      #  Maj 9
        'R M3 4 7'    : ['M', '11', f'{NO5}'],       #  Maj 11  No5
        'R M3 4 5 7'  : ['M', '11'],                 #  Maj 11
        'R 5 6 7'     : ['M', '13', f'{NO3}'],       #  Maj 13  N03
        'R M3 6 7'    : ['M', '13', f'{NO5}'],       #  Maj 13  No5
        'R M3 5 6 7'  : ['M', '13'],                 #  Maj 13
        'R b2 M3 b7'  : ['b9', f'{NO5}'],            #  b9  No5
        'R b2 M3 5 b7': ['b9'],                      #  b9
        'R 2 M3 b7'   : ['9', f'{NO5}'],             #  9  No5
        'R 2 M3 5 b7' : ['9'],                       #  9
        'R m3 M3 b7'  : ['#9', f'{NO5}'],            #  #9  No5
        'R m3 M3 5 b7': ['#9'],                      #  #9
        'R M3 4 b7'   : ['11', f'{NO5}'],            #  11  No5
        'R M3 4 5 b7' : ['11'],                      #  11
        'R M3 b5 b7'  : ['#', '11', f'{NO5}'],       #  #11  No5
        'R M3 b5 5 b7': ['#', '11]'],                #  #11
        'R 5 6 b7'    : ['13', f'{NO3}'],            #  13  N03
        'R M3 6 b7'   : ['13', f'{NO5}'],            #  13  No5
        'R M3 5 6 b7' : ['13'],                      #  13
        'R M3 #5 b7'  : ['b', '13', f'{NO5}'],       #  b13  No5
        'R M3 5 #5 b7': ['b', '13'],                 #  b13
        'R m3 5'      : ['m'],                       #  Minor
        'R b2 m3 #5'  : ['m', 'b2', f'{AUG}'],       #  Min b2  Aug
        'R 2 m3 5'    : ['m2'],                      #  Min 2
        'R m3 4 5'    : ['m4'],                      #  Min 4
        'R m3 #5'     : ['m', f'{AUG}'],             #  Min  Aug
        'R m3 5 #5'   : ['m', 'b6'],                 #  Min b6
        'R m3 6'      : ['m6', f'{NO5}'],            #  Min 6  No5  # Shadows #  Dim7  No5
        'R m3 5 6'    : ['m6'],                      #  Min 6
        'R m3 4 6'    : ['m6', '/4', f'{NO5}'],      #  Min 6/4  No5
        'R m3 b7'     : ['m7', f'{NO5}'],            #  Min 7  No5
        'R m3 5 b7'   : ['m7'],                      #  Min 7
        'R m3 7'      : ['m', 'M7', f'{NO5}'],       #  Min Maj 7  No5
        'R m3 5 7'    : ['m', 'M7'],                 #  Min Maj 7
        'R b2 m3 b7'  : ['m', 'b9', f'{NO5}'],       #  Min b9  No5
        'R b2 m3 5 b7': ['m', 'b9'],                 #  Min b9
        'R 2 m3 b7'   : ['m9', f'{NO5}'],            #  Min 9  No5
        'R 2 m3 5 b7' : ['m9'],                      #  Min 9
        'R m3 4 b7'   : ['m', '11', f'{NO5}'],       #  Min 11  No5
        'R m3 4 5 b7' : ['m', '11'],                 #  Min 11
        'R m3 6 b7'   : ['m', '13', f'{NO5}'],       #  Min 13  No5
        'R m3 5 6 b7' : ['m', '13'],                 #  Min 13
        'R m3 #5 b7'  : ['m', 'b', '13', f'{NO5}'],  #  Min b13  No5
        'R m3 5 #5 b7': ['m', 'b', '13'],            #  Min b13
        'R m3 b5'     : ['o'],                       #  Dim
        'R b2 m3 b5'  : ['o', 'b2'],                 #  Dim b2
        'R m3 b5 b7'  : ['07'],                      #  Min 7 b5
        'R b5 6'      : ['o7', f'{NO3}'],            #  Dim 7  No3
#        'R m3 6'      : ['o7', f'{NO5}'],            #  Dim 7  No5  # Shadows #  Min 6  No5
        'R m3 b5 6'   : ['o7'],                      #  Dim 7
        'R M3 #5'     : [f'{AUG}'],                  #  Aug
        'R m3 4 #5'   : ['m4', f'{AUG}'],            #  Maj inversion
        'R b2 4 #5'   : ['b2', 's4', f'{AUG}'],      #  Maj inversion
        } # how to order/arrange/group?
    ####################################################################################################################################################################################################
    OMAP2 = {
        'R m3 #5'    :1, 'R M3 5'     :0, 'R 4 6'       :2,                  #  [0 3 8]   [0 4 7]   [0 5 9]
        'R m3 5'     :0, 'R M3 6'     :1, 'R 4 #5'      :2,                  #  [0 3 7]   [0 4 9]   [0 5 8]
        'R b2 4 #5'  :3, 'R m3 5 #5'  :1, 'R M3 4 6'    :2, 'R M3 5 7'  :0,  #  [0 1 5 8] [0 3 7 8] [0 4 5 9] [0 4 7 b]
        'R m3 4 6'   :1, 'R M3 5 b7'  :0, 'R m3 b5 #5'  :2, 'R 2 b5 6'  :3,  #  [0 2 6 9] [0 3 5 9] [0 3 6 8] [0 4 7 a]
        'R 2 4 6'    :2, 'R m3 4 #5'  :3, 'R m3 5 b7'   :0, 'R M3 5 6'  :1,  #  [0 2 5 9] [0 3 5 8] [0 3 7 a] [0 4 7 9]
            }
    OMAP1 = {
        'R m3 #5'    : (1, ['m', f'{AUG}']),            'R M3 5'     : (0, []),                   'R 4 6'       : (2, ['6', 's4', f'{NO5}']),                                      #  [0 3 8]   [0 4 7]   [0 5 9]
        'R m3 5'     : (0, ['m']),                      'R M3 6'     : (1, ['6', f'{NO5}']),      'R 4 #5'      : (2, ['s4', f'{AUG}']),                                           #  [0 3 7]   [0 4 9]   [0 5 8]
        'R b2 4 #5'  : (3, ['b2', 's4', f'{AUG}']),     'R m3 5 #5'  : (1, ['m', 'b6']),          'R M3 4 6'    : (2, ['6', '/4', f'{NO5}']), 'R M3 5 7'  : (0, ['M7']),           #  [0 1 5 8] [0 3 7 8] [0 4 5 9] [0 4 7 b]
        'R m3 4 6'   : (1, ['m6', '/4', f'{NO5}']),     'R M3 5 b7'  : (0, ['7']),                'R m3 b5 #5'  : (2, ['m', 'o', f'{AUG}']),  'R 2 b5 6'  : (3, ['s2', 'o', '6']), #  [0 2 6 9] [0 3 5 9] [0 3 6 8] [0 4 7 a]
        'R 2 4 6'    : (2,['6', '/9', 's4', f'{NO5}']), 'R m3 4 #5'  : (3, ['m4', f'{AUG}']),     'R m3 5 b7'   : (0, ['m7']),                'R M3 5 6'  : (1, ['6']),            #  [0 2 5 9] [0 3 5 8] [0 3 7 a] [0 4 7 9]
            }
    OMAP  = {
        'R M3 5'     : (0, []),                       'R m3 #5'    : (1, ['m', f'{AUG}']),        'R 4 6'       : (2, ['6', 's4', f'{NO5}']),                                                   #  [0 3 8]   [0 4 7]   [0 5 9]
        'R m3 5'     : (0, ['m']),                    'R M3 6'     : (1, ['6', f'{NO5}']),        'R 4 #5'      : (2, ['s4', f'{AUG}']),                                                        #  [0 3 7]   [0 4 9]   [0 5 8]
        'R M3 5 7'   : (0, ['M7']),                   'R m3 5 #5'  : (1, ['m', 'b6']),            'R M3 4 6'    : (2, ['6', '/4', f'{NO5}']),       'R b2 4 #5'  : (3, ['b2', 's4', f'{AUG}']), #  [0 1 5 8] [0 3 7 8] [0 4 5 9] [0 4 7 b]
        'R M3 5 b7'  : (0, ['7']),                    'R m3 4 6'   : (1, ['m6', '/4', f'{NO5}']), 'R m3 b5 #5'  : (2, ['m', 'o', f'{AUG}']),        'R 2 b5 6'   : (3, ['s2', 'o', '6']),       #  [0 2 6 9] [0 3 5 9] [0 3 6 8] [0 4 7 a]
        'R m3 5 b7'  : (0, ['m7']),                   'R M3 5 6'   : (1, ['6']),                  'R 2 4 6'     : (2, ['6', '/9', 's4', f'{NO5}']), 'R m3 4 #5'  : (3, ['m4', f'{AUG}']),       #  [0 2 5 9] [0 3 5 8] [0 3 7 a] [0 4 7 9]
            }
