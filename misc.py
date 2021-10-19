import sys, os, collections
sys.path.insert(0, os.path.abspath('.'))
import tabs

VERBOSE = 1 # tabs.VERBOSE
NO5 = 'x'
AUG = '+'
NO3 = 'y'

class Note(object):
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
    MIN_CHORD_LEN = 3
    def __init__(self, tobj, logfile):
        self.tobj    = tobj
        self.logFile = logfile
        self.limap, self.limap1, self.limap2 = [], [], []
        self.mlimap = {}
        self.catmap, self.catmap2 = {}, {}
        self.cat1, self.cat2, self.cat3 = set(), set(), dict()
        self.umap  = {}

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
            else: self.limap1.append(imap)
        else:   self.limap2.append(imap)      # ;   self.log(f'limap2 add      {tabs.fmtl(imap)}')
        if dbg2:
            for i, m in enumerate(self.limap1):
                self.log(tabs.FMTR.format(f'  limap1 [{i+1}] [ <{m[2]:<6}> {tabs.fmtl(m[0], 2, "<", d1, d2):17} {tabs.fmtl(m[1], 2, "<", d1, d2):17} ]'))
            for i, m in enumerate(self.limap2):
                self.log(tabs.FMTR.format(f'  limap2 [{i+1}] [ <{m[2]:<6}> {tabs.fmtl(m[0], 2, "<", d1, d2):17} {tabs.fmtl(m[1], 2, "<", d1, d2):17} ]'))
        if   self.limap1 and self.limap1[0]: chordName = self.limap1[0][2]  ;  chunks = self.limap1[0][3]
        elif self.limap2 and self.limap2[0]: chordName = self.limap2[0][2]  ;  chunks = self.limap2[0][3]
        return chordName, chunks

    def getChordName(self, p, l, c, dbg=1, dbg2=0):
        cc = c + l * self.tobj.n[tabs.C]
#        if dbg: self.log(f'p l c cc = {p} {l} {c} {cc} mlimap.keys={tabs.fmtl(list(self.mlimap.keys()))}:')
#        if dbg: self.dumpMLimap('Get Chord Name')
        self.limap, chunks, ims = [], [], set()   ;   chordName = ''
        imapKeys, imapNotes                     = None, None   ;   d1, d2 = '<', '>'
        mask, notes, indices                    = self.getNotesIndices(p, l, c)
        for i in range(len(indices)):
            imk = indices[i] % len(self.INTERVALS)
            if imk not in ims:
                ims.add(imk)
                intervals                           = self.getIntervals(indices,  i,     mask)
                imap, imapKeys, imapNotes, chordKey = self.getImapKeys(intervals, notes)
                if dbg: self.log(f'imk={imk} ims={tabs.fmtl(ims)} cc={cc}')
                chordName, chunks               = self._getChordName(imap)
                if dbg and chordName: self.log(f'Inner Chord     [ <{chordName:<6}> {tabs.fmtl(imapKeys, 2, "<", d1, d2):17} {tabs.fmtl(imapNotes, 2, "<", d1, d2):17} ] {tabs.fmtl(chunks)}')
                chordName, chunks               = self.updateImap(imap, chordName, chunks)
        self.limap.extend(self.limap1)      ;     self.limap.extend(self.limap2)
        if chordName:
            if dbg: self.log(f'Outer Chord     [ <{chordName:<6}> {tabs.fmtl(imapKeys, 2, "<", d1, d2):17} {tabs.fmtl(imapNotes, 2, "<", d1, d2):17} ] {tabs.fmtl(chunks)}')
            self.mlimap[cc]                     = self.limap
            self.add2cat(self.limap, cc)
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

    def toggleChordName(self, key, rev=0):
        self.log(f'rev={rev} key={key}')
        if key not in self.mlimap.keys(): self.log(f'key={key} Not Found')   ;   return None, None
        else:
           limap = self.mlimap[key]
           self.dumpLimap(limap, key, why=f'before key={key} rev={rev}')
           if rev: tmp0 = limap[-1]  ;   tmp1 = limap[:-1]  ;   limap  = tmp1   ;   limap.insert(0, tmp0)
           else:   tmp0 = limap[0]   ;   tmp1 = limap[1:]   ;   limap  = tmp1   ;   limap.append(tmp0)
           self.mlimap[key] = limap
           self.dumpLimap(limap, key, why=f'after  key={key} rev={rev}')
           return limap[0][2], limap[0][3]
   ####################################################################################################################################################################################################
    def getNotesIndices(self, p, l, c, dbg=VERBOSE, dbg2=0):
        strNumbs   = self.tobj.stringNumbs
        strKeys    = self.tobj.stringKeys
        strNames   = self.tobj.stringNames
        _tabs      = self.tobj.data[p][l][c]
        strIndices = [ Note.INDICES[k] for k in strKeys ]
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
            if dbg2: self.dumpData(indices,    mask,  'Note Indices')
            if dbg:  self.dumpData(notes,      mask,  'Notes')
        return mask, notes, indices

    def getIntervals(self, indices, j, mask, order=1, dbg=VERBOSE):
        ii = []   ;   nst = Note.NTONES
        for i in indices:
            if i - indices[j] >= 0:
                if order: ii.append((i - indices[j]) % nst)
                else:     ii.insert(0, (i - indices[j]) % nst)
            else:
                d = (indices[j] - i) % nst
                delta = nst - d
                if delta == nst: delta = 0
                if order: ii.append(delta)
                else:     ii.insert(0, delta)
        intervals = []
        for i in ii:
            intervals.append(self.INTERVALS[i])
        if dbg: self.dumpData(ii,    mask, 'Interval Indices')
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
        self.log(f'{why} len={len(self.mlimap)}')        ;   count1, count2 = 0, 0
        for i, (k, v) in enumerate(self.mlimap.items()):
            self.dumpLimap(v, k)
        for i, (k, v) in enumerate(self.mlimap.items()):
            self.log(f'{i+1:3} {k:3}', ind=0, end=' ')
            for j in range(len(v)):
                tmp = f'{tabs.fmtl(v[j][0], w=tabs.FMTN2, d1="", d2="")}'   ;   count1 += 1
                if v[j][2]: count2 += 1
                self.log(f'{v[j][2]:7}|{tmp:16}', ind=0, end='')
            self.log(ind=0)
        if count1: self.log(f'{why} len={len(self.mlimap)} count=({count2} / {count1})={count2/count1:6.4} ')

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
        key = ' '.join(imap.keys())   ;   order = len(self.tobj.stringNumbs) + 1
        chordName, root, name, chunks = '', '', [], []
        if key in self.OMAP:
            name = self.OMAP[key][2]  ;  root = imap['R']
            if dbg: self.log(f'    Found key=<{key}> root={root} name={tabs.fmtl(name)} {type(name)}')
        else:
            if dbg: self.log(f'Not Found key=<{key}> root={root} name={tabs.fmtl(name)} {type(name)}')
            if len(imap) > Chord.MIN_CHORD_LEN:
                ii = self.key2Indices(key)
                self.log(f'adding key {key} with indices {tabs.fmtl(ii)} to OMAP')
                self.umap[key] = (order, ii, [])
        if root:    chunks.append(root)
        if name:   [chunks.append(n) for n in name if n]   ;   chordName = ''.join(chunks[:])
        if dbg:     self.log(f'chordName=<{chordName}> chunks={tabs.fmtl(chunks)}')
        return chordName, chunks
    def key2Indices(self, k):
        r = []  ;  t = ''
        for j in k:
            if j != ' ': t += j
            else:        r.append(self.INTERVAL_RANK[t])  ;  t = ''
        r.append(self.INTERVAL_RANK[t])
        return r
    @staticmethod
    def rotateIndices(a):
        ll = len(a)   ;   r = [0]
        for i in range(1, ll):
            if i + 1 < ll: r.append(a[i+1] - a[i] + r[i-1])
            else :         r.append(Note.NTONES - a[i] + r[i-1])
        return r
    def mergeMaps(self, src, trg):
        self.log(f'BGN len(src)={len(src)} len(trg){len(trg)}')
        for k, v in src.items():
            trg[k] = v
        self.log(f'END len(src)={len(src)} len(trg){len(trg)}')
    ####################################################################################################################################################################################################
    def dumpOMAP(self, catpath=None, merge=0):
        self.log('BGN')
        if merge: self.mergeMaps(self.umap, self.OMAP)
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
        self.log('END')

    def _dumpOMAP(self, catfile=None):
        file = catfile      if catfile else self.logFile
        name = catfile.name if catfile else None
        omap = self.OMAP   ;   setMap = {}   ;   r = {}   ;   order = len(self.tobj.stringNumbs) + 1
        self.log('BGN len(OMAP)={} {}'.format(len(omap), name))
        for k, v in omap.items():
            kv = len(v[1])
            if kv not in setMap: setMap[kv] = set()
            setMap[kv].add(tuple(v[1]))
        j, mstat, tstat = 0, [], []
        for k, sml in setMap.items():
            sml = sorted(sml)
            tstat.append(0)
            count, nord, none = 0, 0, 0
            for ii in sml:
                keys = [ self.INTERVALS[i] for i in ii ]
                keyStr    = ' '.join(keys)
                keyStrFmt = '\'' + keyStr + '\''
                v = omap[keyStr]
                if not catfile:
                    count += 1
                    if not v[2]: none += 1
                    if v[0] >= len(self.tobj.stringNumbs): nord += 1
                v2 = tabs.fmtl(v[2], sep='\',\'', d1='[\'', d2='\']),') if v[2] else '[]' if type(v[2]) is list else 'None),'
                self.log(f'{keyStrFmt:19}: ({v[0]}, {tabs.fmtl(v[1], sep=",", d2="],"):15} {v2:26} # ', ind=0, file=file, end='')
                for _ in range(len(ii)-1):
                    ii = self.rotateIndices(ii)
                    keys = [ self.INTERVALS[i] for i in ii ]
                    keyStr = ' '.join(keys)
                    if keyStr not in omap: self.log(f'Not in Map: ', ind=0, end='', file=file)   ;   r[keyStr] = (order, ii, None)
                    self.log(f'{keyStr:16} {tabs.fmtl(ii, z="x"):13} ', ind=0, end='', file=file)
                self.log(ind=0, file=file)
            if not catfile: mstat.append([k, count, nord, none])
        if not catfile:
            for j in range(len(mstat)):
                self.log(f' {mstat[j][0]} note chords  {mstat[j][1]:3} total  {mstat[j][2]:3} unordered  {mstat[j][3]:3} unnamed')
                tstat[0] += mstat[j][0]   ;   tstat[1] += mstat[j][1]   ;   tstat[2] += mstat[j][2]   ;   tstat[3] += mstat[j][3]
        if catfile: self.log('END len(OMAP)={} {} len(r)={}'.format(len(omap), name, len(r)))
        else: self.log(f'END grand total {tstat[1]:3} total  {tstat[2]:3} unordered  {tstat[3]:3} unnamed  len(r)={len(r)}')
        return r

    ####################################################################################################################################################################################################
    #    0  1  2  3  4  5  6  7  8   9  10 11 0
    #    R  b2 2  m3 M3 4  b5 5  #5  6  b7 7  R
    #       b9 9  #9    11 #11   b13 13
    ####################################################################################################################################################################################################
    OMAP = {
            'R b2 m3'          : (2, [0,1,3],        ['m','b2']),               # R 2 7            [0 2 b]       R 6 b7           [0 9 a]
            'R b2 M3'          : (1, [0,1,4],        ['b2','x']),               # R m3 7           [0 3 b]       R #5 6           [0 8 9]
            'R b2 4'           : (2, [0,1,5],        ['s4','b2','x']),          # R M3 7           [0 4 b]       R 5 #5           [0 7 8]
            'R b2 b5'          : (1, [0,1,6],        ['o','b2','y']),           # R 4 7            [0 5 b]       R b5 5           [0 6 7]
            'R 2 M3'           : (2, [0,2,4],        ['2','x']),                # R 2 b7           [0 2 a]       R #5 b7          [0 8 a]
            'R 2 4'            : (1, [0,2,5],        ['s2','s4','x']),          # R m3 b7          [0 3 a]       R 5 6            [0 7 9]
            'R 2 b5'           : (1, [0,2,6],        ['s2','o']),               # R M3 b7          [0 4 a]       R b5 #5          [0 6 8]
            'R 2 5'            : (1, [0,2,7],        ['s2']),                   # R 4 b7           [0 5 a]       R 4 5            [0 5 7]
            'R 2 #5'           : (1, [0,2,8],        ['s2','+']),               # R b5 b7          [0 6 a]       R M3 b5          [0 4 6]
            'R 2 6'            : (0, [0,2,9],        ['6','s2','x']),           # R 5 b7           [0 7 a]       R m3 4           [0 3 5]
            'R 2 b7'           : (0, [0,2,10],       ['7','s2','x']),           # R #5 b7          [0 8 a]       R 2 M3           [0 2 4]
            'R 2 7'            : (0, [0,2,11],       ['M7','s2','x']),          # R 6 b7           [0 9 a]       R b2 m3          [0 1 3]
            'R m3 4'           : (2, [0,3,5],        ['m','4']),                # R 2 6            [0 2 9]       R 5 b7           [0 7 a]
            'R m3 b5'          : (0, [0,3,6],        ['o']),                    # R m3 6           [0 3 9]       R b5 6           [0 6 9]
            'R m3 5'           : (0, [0,3,7],        ['m']),                    # R M3 6           [0 4 9]       R 4 #5           [0 5 8]
            'R m3 #5'          : (1, [0,3,8],        ['m','+']),                # R 4 6            [0 5 9]       R M3 5           [0 4 7]
            'R m3 6'           : (1, [0,3,9],        ['m6','x']),               # R b5 6           [0 6 9]       R m3 b5          [0 3 6]
            'R m3 b7'          : (0, [0,3,10],       ['m7','x']),               # R 5 6            [0 7 9]       R 2 4            [0 2 5]
            'R m3 7'           : (0, [0,3,11],       ['m','M7','x']),           # R #5 6           [0 8 9]       R b2 M3          [0 1 4]
            'R M3 b5'          : (2, [0,4,6],        ['b5']),                   # R 2 #5           [0 2 8]       R b5 b7          [0 6 a]
            'R M3 5'           : (0, [0,4,7],        ['']),                     # R m3 #5          [0 3 8]       R 4 6            [0 5 9]
            'R M3 #5'          : (0, [0,4,8],        ['+']),                    # R M3 #5          [0 4 8]       R M3 #5          [0 4 8]
            'R M3 6'           : (1, [0,4,9],        ['6','x']),                # R 4 #5           [0 5 8]       R m3 5           [0 3 7]
            'R M3 b7'          : (0, [0,4,10],       ['7','x']),                # R b5 #5          [0 6 8]       R 2 b5           [0 2 6]
            'R M3 7'           : (0, [0,4,11],       ['M7','x']),               # R 5 #5           [0 7 8]       R b2 4           [0 1 5]
            'R 4 5'            : (2, [0,5,7],        ['s4']),                   # R 2 5            [0 2 7]       R 4 b7           [0 5 a]
            'R 4 #5'           : (2, [0,5,8],        ['s4','+']),               # R m3 5           [0 3 7]       R M3 6           [0 4 9]
            'R 4 6'            : (2, [0,5,9],        ['6','s4','x']),           # R M3 5           [0 4 7]       R m3 #5          [0 3 8]
            'R 4 b7'           : (0, [0,5,10],       ['7','s4','x']),           # R 4 5            [0 5 7]       R 2 5            [0 2 7]
            'R 4 7'            : (0, [0,5,11],       ['M7','s4','x']),          # R b5 5           [0 6 7]       R b2 b5          [0 1 6]
            'R b5 5'           : (2, [0,6,7],        ['#4','y']),               # R b2 b5          [0 1 6]       R 4 7            [0 5 b]
            'R b5 #5'          : (2, [0,6,8],        ['o','+','y']),            # R 2 b5           [0 2 6]       R M3 b7          [0 4 a]
            'R b5 6'           : (2, [0,6,9],        ['o7','y']),               # R m3 b5          [0 3 6]       R m3 6           [0 3 9]
            'R b5 b7'          : (0, [0,6,10],       ['07','y']),               # R M3 b5          [0 4 6]       R 2 #5           [0 2 8]
            'R 5 #5'           : (1, [0,7,8],        ['b6','y']),               # R b2 4           [0 1 5]       R M3 7           [0 4 b]
            'R 5 6'            : (2, [0,7,9],        ['6','y']),                # R 2 4            [0 2 5]       R m3 b7          [0 3 a]
            'R 5 b7'           : (1, [0,7,10],       ['7','y']),                # R m3 4           [0 3 5]       R 2 6            [0 2 9]
            'R #5 6'           : (2, [0,8,9],        ['+','6','y']),            # R b2 M3          [0 1 4]       R m3 7           [0 3 b]
            'R #5 b7'          : (1, [0,8,10],       ['7','+','y']),            # R 2 M3           [0 2 4]       R 2 b7           [0 2 a]
            'R 6 b7'           : (1, [0,9,10],       ['13','x','y']),           # R b2 m3          [0 1 3]       R 2 7            [0 2 b]
            'R b2 2 M3'        : (3, [0,1,2,4],      ['b2','2','x']),           # R b2 m3 7        [0 1 3 b]     R 2 b7 7         [0 2 a b]     R #5 6 b7        [0 8 9 a]
            'R b2 2 b5'        : (3, [0,1,2,6],      ['s2','b2','o']),          # R b2 4 7         [0 1 5 b]     R M3 b7 7        [0 4 a b]     R b5 5 #5        [0 6 7 8]
            'R b2 m3 4'        : (3, [0,1,3,5],      ['m','b2','4']),           # R 2 M3 7         [0 2 4 b]     R 2 6 b7         [0 2 9 a]     R 5 #5 b7        [0 7 8 a]
            'R b2 m3 b5'       : (2, [0,1,3,6],      ['o','b2']),               # R 2 4 7          [0 2 5 b]     R m3 6 b7        [0 3 9 a]     R b5 5 6         [0 6 7 9]
            'R b2 m3 5'        : (3, [0,1,3,7],      ['m','b2']),               # R 2 b5 7         [0 2 6 b]     R M3 6 b7        [0 4 9 a]     R 4 b5 #5        [0 5 6 8]
            'R b2 m3 #5'       : (3, [0,1,3,8],      ['m','b2','+']),           # R 2 5 7          [0 2 7 b]     R 4 6 b7         [0 5 9 a]     R M3 4 5         [0 4 5 7]
            'R b2 m3 6'        : (0, [0,1,3,9],      ['m','6','x']),            # R 2 #5 7         [0 2 8 b]     R b5 6 b7        [0 6 9 a]     R m3 M3 b5       [0 3 4 6]
            'R b2 m3 b7'       : (1, [0,1,3,10],     ['m','b9','x']),           # R 2 6 7          [0 2 9 b]     R 5 6 b7         [0 7 9 a]     R 2 m3 4         [0 2 3 5]
            'R b2 m3 7'        : (0, [0,1,3,11],     ['m','b9']),               # R 2 b7 7         [0 2 a b]     R #5 6 b7        [0 8 9 a]     R b2 2 M3        [0 1 2 4]
            'R b2 M3 5'        : (1, [0,1,4,7],      ['b2']),                   # R m3 b5 7        [0 3 6 b]     R m3 #5 6        [0 3 8 9]     R 4 b5 6         [0 5 6 9]
            'R b2 M3 #5'       : (3, [0,1,4,8],      ['+','b2']),               # R m3 5 7         [0 3 7 b]     R M3 #5 6        [0 4 8 9]     R M3 4 #5        [0 4 5 8]
            'R b2 M3 b7'       : (1, [0,1,4,10],     ['b9','x']),               # R m3 6 7         [0 3 9 b]     R b5 #5 6        [0 6 8 9]     R 2 m3 b5        [0 2 3 6]
            'R b2 4 b5'        : (2, [0,1,5,6],      ['s4','o','b2']),          # R M3 4 7         [0 4 5 b]     R b2 5 #5        [0 1 7 8]     R b5 5 7         [0 6 7 b]
            'R b2 4 #5'        : (2, [0,1,5,8],      ['b2','s4','+']),          # R M3 5 7         [0 4 7 b]     R m3 5 #5        [0 3 7 8]     R M3 4 6         [0 4 5 9]
            'R b2 4 b7'        : (1, [0,1,5,10],     ['11','b9','x']),          # R M3 6 7         [0 4 9 b]     R 4 5 #5         [0 5 7 8]     R 2 m3 5         [0 2 3 7]
            'R b2 4 7'         : (0, [0,1,5,11],     ['M','b9','s4']),          # R M3 b7 7        [0 4 a b]     R b5 5 #5        [0 6 7 8]     R b2 2 b5        [0 1 2 6]
            'R b2 b5 5'        : (1, [0,1,6,7],      ['b2','#4','y']),          # R 4 b5 7         [0 5 6 b]     R b2 b5 5        [0 1 6 7]     R 4 b5 7         [0 5 6 b]
            'R b2 b5 #5'       : (3, [0,1,6,8],      ['b2','#4','+']),          # R 4 5 7          [0 5 7 b]     R 2 b5 5         [0 2 6 7]     R M3 4 b7        [0 4 5 a]
            'R b2 5 #5'        : (3, [0,1,7,8],      ['+','b2','y']),           # R b5 5 7         [0 6 7 b]     R b2 4 b5        [0 1 5 6]     R M3 4 7         [0 4 5 b]
            'R b2 5 6'         : (3, [0,1,7,9],      ['b2','6','y']),           # R b5 #5 7        [0 6 8 b]     R 2 4 b5         [0 2 5 6]     R m3 M3 b7       [0 3 4 a]
            'R b2 5 b7'        : (0, [0,1,7,10],     ['b9','y']),               # R b5 6 7         [0 6 9 b]     R m3 4 b5        [0 3 5 6]     R 2 m3 6         [0 2 3 9]
            'R b2 #5 b7'       : (2, [0,1,8,10],     ['b','13','b9','y','x']),  # R 5 6 7          [0 7 9 b]     R 2 M3 4         [0 2 4 5]     R 2 m3 b7        [0 2 3 a]
            'R 2 m3 4'         : (3, [0,2,3,5],      ['m','2','4','x']),        # R b2 m3 b7       [0 1 3 a]     R 2 6 7          [0 2 9 b]     R 5 6 b7         [0 7 9 a]
            'R 2 m3 b5'        : (2, [0,2,3,6],      ['o','2']),                # R b2 M3 b7       [0 1 4 a]     R m3 6 7         [0 3 9 b]     R b5 #5 6        [0 6 8 9]
            'R 2 m3 5'         : (2, [0,2,3,7],      ['m2']),                   # R b2 4 b7        [0 1 5 a]     R M3 6 7         [0 4 9 b]     R 4 5 #5         [0 5 7 8]
            'R 2 m3 6'         : (2, [0,2,3,9],      ['m','2','6','x']),        # R b2 5 b7        [0 1 7 a]     R b5 6 7         [0 6 9 b]     R m3 4 b5        [0 3 5 6]
            'R 2 m3 b7'        : (0, [0,2,3,10],     ['m9','x']),               # R b2 #5 b7       [0 1 8 a]     R 5 6 7          [0 7 9 b]     R 2 M3 4         [0 2 4 5]
            'R 2 M3 4'         : (3, [0,2,4,5],      ['2','4','x']),            # R 2 m3 b7        [0 2 3 a]     R b2 #5 b7       [0 1 8 a]     R 5 6 7          [0 7 9 b]
            'R 2 M3 b5'        : (3, [0,2,4,6],      ['2','#4','x']),           # R 2 M3 b7        [0 2 4 a]     R 2 #5 b7        [0 2 8 a]     R b5 #5 b7       [0 6 8 a]
            'R 2 M3 5'         : (0, [0,2,4,7],      ['2']),                    # R 2 4 b7         [0 2 5 a]     R m3 #5 b7       [0 3 8 a]     R 4 5 6          [0 5 7 9]
            'R 2 M3 #5'        : (2, [0,2,4,8],      ['+','2']),                # R 2 b5 b7        [0 2 6 a]     R M3 #5 b7       [0 4 8 a]     R M3 b5 #5       [0 4 6 8]
            'R 2 M3 6'         : (0, [0,2,4,9],      ['6','9','x']),            # R 2 5 b7         [0 2 7 a]     R 4 #5 b7        [0 5 8 a]     R m3 4 5         [0 3 5 7]
            'R 2 M3 b7'        : (0, [0,2,4,10],     ['9','x']),                # R 2 #5 b7        [0 2 8 a]     R b5 #5 b7       [0 6 8 a]     R 2 M3 b5        [0 2 4 6]
            'R 2 M3 7'         : (0, [0,2,4,11],     ['M9','x']),               # R 2 6 b7         [0 2 9 a]     R 5 #5 b7        [0 7 8 a]     R b2 m3 4        [0 1 3 5]
            'R 2 4 b5'         : (2, [0,2,5,6],      ['s2','s4','o']),          # R m3 M3 b7       [0 3 4 a]     R b2 5 6         [0 1 7 9]     R b5 #5 7        [0 6 8 b]
            'R 2 4 5'          : (3, [0,2,5,7],      ['s2','s4']),              # R m3 4 b7        [0 3 5 a]     R 2 5 6          [0 2 7 9]     R 4 5 b7         [0 5 7 a]
            'R 2 4 #5'         : (2, [0,2,5,8],      ['s2','s4','+']),          # R m3 b5 b7       [0 3 6 a]     R m3 5 6         [0 3 7 9]     R M3 b5 6        [0 4 6 9]
            'R 2 4 6'          : (3, [0,2,5,9],      ['6','9','s4','x']),       # R m3 5 b7        [0 3 7 a]     R M3 5 6         [0 4 7 9]     R m3 4 #5        [0 3 5 8]
            'R 2 4 b7'         : (2, [0,2,5,10],     ['7','s2','s4','x']),      # R m3 #5 b7       [0 3 8 a]     R 4 5 6          [0 5 7 9]     R 2 M3 5         [0 2 4 7]
            'R 2 4 7'          : (1, [0,2,5,11],     ['M7','s2','s4','x']),     # R m3 6 b7        [0 3 9 a]     R b5 5 6         [0 6 7 9]     R b2 m3 b5       [0 1 3 6]
            'R 2 b5 5'         : (2, [0,2,6,7],      ['s2','#4']),              # R M3 4 b7        [0 4 5 a]     R b2 b5 #5       [0 1 6 8]     R 4 5 7          [0 5 7 b]
            'R 2 b5 #5'        : (1, [0,2,6,8],      ['s2','o','+']),           # R M3 b5 b7       [0 4 6 a]     R 2 b5 #5        [0 2 6 8]     R M3 b5 b7       [0 4 6 a]
            'R 2 b5 6'         : (3, [0,2,6,9],      ['s2','o','6']),           # R M3 5 b7        [0 4 7 a]     R m3 b5 #5       [0 3 6 8]     R m3 4 6         [0 3 5 9]
            'R 2 b5 b7'        : (1, [0,2,6,10],     ['s2','07']),              # R M3 #5 b7       [0 4 8 a]     R M3 b5 #5       [0 4 6 8]     R 2 M3 #5        [0 2 4 8]
            'R 2 b5 7'         : (1, [0,2,6,11],     ['s2','07']),              # R M3 6 b7        [0 4 9 a]     R 4 b5 #5        [0 5 6 8]     R b2 m3 5        [0 1 3 7]
            'R 2 5 6'          : (2, [0,2,7,9],      ['6','s2']),               # R 4 5 b7         [0 5 7 a]     R 2 4 5          [0 2 5 7]     R m3 4 b7        [0 3 5 a]
            'R 2 5 b7'         : (1, [0,2,7,10],     ['7','s2']),               # R 4 #5 b7        [0 5 8 a]     R m3 4 5         [0 3 5 7]     R 2 M3 6         [0 2 4 9]
            'R 2 5 7'          : (1, [0,2,7,11],     ['M7','s2']),              # R 4 6 b7         [0 5 9 a]     R M3 4 5         [0 4 5 7]     R b2 m3 #5       [0 1 3 8]
            'R 2 #5 b7'        : (2, [0,2,8,10],     ['7','s2','+']),           # R b5 #5 b7       [0 6 8 a]     R 2 M3 b5        [0 2 4 6]     R 2 M3 b7        [0 2 4 a]
            'R 2 #5 7'         : (3, [0,2,8,11],     ['Mb','13','s2','x']),     # R b5 6 b7        [0 6 9 a]     R m3 M3 b5       [0 3 4 6]     R b2 m3 6        [0 1 3 9]
            'R 2 6 b7'         : (1, [0,2,9,10],     ['13','s2','x']),          # R 5 #5 b7        [0 7 8 a]     R b2 m3 4        [0 1 3 5]     R 2 M3 7         [0 2 4 b]
            'R 2 6 7'          : (2, [0,2,9,11],     ['M','13','s2']),          # R 5 6 b7         [0 7 9 a]     R 2 m3 4         [0 2 3 5]     R b2 m3 b7       [0 1 3 a]
            'R 2 b7 7'         : (2, [0,2,10,11],    ['M','#','13','s2','x']),  # R #5 6 b7        [0 8 9 a]     R b2 2 M3        [0 1 2 4]     R b2 m3 7        [0 1 3 b]
            'R m3 M3 b5'       : (1, [0,3,4,6],      ['#2']),                   # R b2 m3 6        [0 1 3 9]     R 2 #5 7         [0 2 8 b]     R b5 6 b7        [0 6 9 a]
            'R m3 M3 b7'       : (0, [0,3,4,10],     ['#9','x']),               # R b2 5 6         [0 1 7 9]     R b5 #5 7        [0 6 8 b]     R 2 4 b5         [0 2 5 6]
            'R m3 4 b5'        : (3, [0,3,5,6],      ['o','4']),                # R 2 m3 6         [0 2 3 9]     R b2 5 b7        [0 1 7 a]     R b5 6 7         [0 6 9 b]
            'R m3 4 5'         : (3, [0,3,5,7],      ['m4']),                   # R 2 M3 6         [0 2 4 9]     R 2 5 b7         [0 2 7 a]     R 4 #5 b7        [0 5 8 a]
            'R m3 4 #5'        : (2, [0,3,5,8],      ['m4','+']),               # R 2 4 6          [0 2 5 9]     R m3 5 b7        [0 3 7 a]     R M3 5 6         [0 4 7 9]
            'R m3 4 6'         : (1, [0,3,5,9],      ['m6','4','x']),           # R 2 b5 6         [0 2 6 9]     R M3 5 b7        [0 4 7 a]     R m3 b5 #5       [0 3 6 8]
            'R m3 4 b7'        : (0, [0,3,5,10],     ['m','11','x']),           # R 2 5 6          [0 2 7 9]     R 4 5 b7         [0 5 7 a]     R 2 4 5          [0 2 5 7]
            'R m3 b5 #5'       : (2, [0,3,6,8],      ['o','+']),                # R m3 4 6         [0 3 5 9]     R 2 b5 6         [0 2 6 9]     R M3 5 b7        [0 4 7 a]
            'R m3 b5 6'        : (0, [0,3,6,9],      ['o7']),                   # R m3 b5 6        [0 3 6 9]     R m3 b5 6        [0 3 6 9]     R m3 b5 6        [0 3 6 9]
            'R m3 b5 b7'       : (0, [0,3,6,10],     ['07']),                   # R m3 5 6         [0 3 7 9]     R M3 b5 6        [0 4 6 9]     R 2 4 #5         [0 2 5 8]
            'R m3 b5 7'        : (0, [0,3,6,11],     ['o','M7']),               # R m3 #5 6        [0 3 8 9]     R 4 b5 6         [0 5 6 9]     R b2 M3 5        [0 1 4 7]
            'R m3 5 #5'        : (3, [0,3,7,8],      ['m','b6']),               # R M3 4 6         [0 4 5 9]     R b2 4 #5        [0 1 5 8]     R M3 5 7         [0 4 7 b]
            'R m3 5 6'         : (1, [0,3,7,9],      ['m6']),                   # R M3 b5 6        [0 4 6 9]     R 2 4 #5         [0 2 5 8]     R m3 b5 b7       [0 3 6 a]
            'R m3 5 b7'        : (0, [0,3,7,10],     ['m7']),                   # R M3 5 6         [0 4 7 9]     R m3 4 #5        [0 3 5 8]     R 2 4 6          [0 2 5 9]
            'R m3 5 7'         : (0, [0,3,7,11],     ['m','M7']),               # R M3 #5 6        [0 4 8 9]     R M3 4 #5        [0 4 5 8]     R b2 M3 #5       [0 1 4 8]
            'R m3 #5 6'        : (3, [0,3,8,9],      ['m','+','6']),            # R 4 b5 6         [0 5 6 9]     R b2 M3 5        [0 1 4 7]     R m3 b5 7        [0 3 6 b]
            'R m3 #5 b7'       : (1, [0,3,8,10],     ['m','b','13','x']),       # R 4 5 6          [0 5 7 9]     R 2 M3 5         [0 2 4 7]     R 2 4 b7         [0 2 5 a]
            'R m3 6 b7'        : (0, [0,3,9,10],     ['m','13','x']),           # R b5 5 6         [0 6 7 9]     R b2 m3 b5       [0 1 3 6]     R 2 4 7          [0 2 5 b]
            'R m3 6 7'         : (0, [0,3,9,11],     ['m','13','x']),           # R b5 #5 6        [0 6 8 9]     R 2 m3 b5        [0 2 3 6]     R b2 M3 b7       [0 1 4 a]
            'R M3 4 5'         : (0, [0,4,5,7],      ['4']),                    # R b2 m3 #5       [0 1 3 8]     R 2 5 7          [0 2 7 b]     R 4 6 b7         [0 5 9 a]
            'R M3 4 #5'        : (1, [0,4,5,8],      ['+','4']),                # R b2 M3 #5       [0 1 4 8]     R m3 5 7         [0 3 7 b]     R M3 #5 6        [0 4 8 9]
            'R M3 4 6'         : (1, [0,4,5,9],      ['6','4','x']),            # R b2 4 #5        [0 1 5 8]     R M3 5 7         [0 4 7 b]     R m3 5 #5        [0 3 7 8]
            'R M3 4 b7'        : (0, [0,4,5,10],     ['11','x']),               # R b2 b5 #5       [0 1 6 8]     R 4 5 7          [0 5 7 b]     R 2 b5 5         [0 2 6 7]
            'R M3 4 7'         : (0, [0,4,5,11],     ['M','11','x']),           # R b2 5 #5        [0 1 7 8]     R b5 5 7         [0 6 7 b]     R b2 4 b5        [0 1 5 6]
            'R M3 b5 #5'       : (3, [0,4,6,8],      ['#4','+']),               # R 2 M3 #5        [0 2 4 8]     R 2 b5 b7        [0 2 6 a]     R M3 #5 b7       [0 4 8 a]
            'R M3 b5 6'        : (3, [0,4,6,9],      ['b5','6']),               # R 2 4 #5         [0 2 5 8]     R m3 b5 b7       [0 3 6 a]     R m3 5 6         [0 3 7 9]
            'R M3 b5 b7'       : (0, [0,4,6,10],     ['#','11','x']),           # R 2 b5 #5        [0 2 6 8]     R M3 b5 b7       [0 4 6 a]     R 2 b5 #5        [0 2 6 8]
            'R M3 5 6'         : (1, [0,4,7,9],      ['6']),                    # R m3 4 #5        [0 3 5 8]     R 2 4 6          [0 2 5 9]     R m3 5 b7        [0 3 7 a]
            'R M3 5 b7'        : (0, [0,4,7,10],     ['7']),                    # R m3 b5 #5       [0 3 6 8]     R m3 4 6         [0 3 5 9]     R 2 b5 6         [0 2 6 9]
            'R M3 5 7'         : (0, [0,4,7,11],     ['M7']),                   # R m3 5 #5        [0 3 7 8]     R M3 4 6         [0 4 5 9]     R b2 4 #5        [0 1 5 8]
            'R M3 #5 6'        : (2, [0,4,8,9],      ['+','6']),                # R M3 4 #5        [0 4 5 8]     R b2 M3 #5       [0 1 4 8]     R m3 5 7         [0 3 7 b]
            'R M3 #5 b7'       : (0, [0,4,8,10],     ['b','13','x']),           # R M3 b5 #5       [0 4 6 8]     R 2 M3 #5        [0 2 4 8]     R 2 b5 b7        [0 2 6 a]
            'R M3 6 b7'        : (0, [0,4,9,10],     ['13','x']),               # R 4 b5 #5        [0 5 6 8]     R b2 m3 5        [0 1 3 7]     R 2 b5 7         [0 2 6 b]
            'R M3 6 7'         : (1, [0,4,9,11],     ['M','13','x']),           # R 4 5 #5         [0 5 7 8]     R 2 m3 5         [0 2 3 7]     R b2 4 b7        [0 1 5 a]
            'R M3 b7 7'        : (1, [0,4,10,11],    ['7','M','7','x']),        # R b5 5 #5        [0 6 7 8]     R b2 2 b5        [0 1 2 6]     R b2 4 7         [0 1 5 b]
            'R 4 b5 #5'        : (2, [0,5,6,8],      ['s4','o','+']),           # R b2 m3 5        [0 1 3 7]     R 2 b5 7         [0 2 6 b]     R M3 6 b7        [0 4 9 a]
            'R 4 b5 6'         : (2, [0,5,6,9],      ['s4','o','6']),           # R b2 M3 5        [0 1 4 7]     R m3 b5 7        [0 3 6 b]     R m3 #5 6        [0 3 8 9]
            'R 4 b5 7'         : (0, [0,5,6,11],     ['o','11','y']),           # R b2 b5 5        [0 1 6 7]     R 4 b5 7         [0 5 6 b]     R b2 b5 5        [0 1 6 7]
            'R 4 5 #5'         : (3, [0,5,7,8],      ['s4','b6']),              # R 2 m3 5         [0 2 3 7]     R b2 4 b7        [0 1 5 a]     R M3 6 7         [0 4 9 b]
            'R 4 5 6'          : (3, [0,5,7,9],      ['s4','6']),               # R 2 M3 5         [0 2 4 7]     R 2 4 b7         [0 2 5 a]     R m3 #5 b7       [0 3 8 a]
            'R 4 5 b7'         : (1, [0,5,7,10],     ['7','s4']),               # R 2 4 5          [0 2 5 7]     R m3 4 b7        [0 3 5 a]     R 2 5 6          [0 2 7 9]
            'R 4 5 7'          : (1, [0,5,7,11],     ['M7','s4']),              # R 2 b5 5         [0 2 6 7]     R M3 4 b7        [0 4 5 a]     R b2 b5 #5       [0 1 6 8]
            'R 4 #5 b7'        : (2, [0,5,8,10],     ['b','13','s4']),          # R m3 4 5         [0 3 5 7]     R 2 M3 6         [0 2 4 9]     R 2 5 b7         [0 2 7 a]
            'R 4 6 b7'         : (2, [0,5,9,10],     ['13','s4','x']),          # R M3 4 5         [0 4 5 7]     R b2 m3 #5       [0 1 3 8]     R 2 5 7          [0 2 7 b]
            'R b5 5 #5'        : (2, [0,6,7,8],      ['#4','+','y']),           # R b2 2 b5        [0 1 2 6]     R b2 4 7         [0 1 5 b]     R M3 b7 7        [0 4 a b]
            'R b5 5 6'         : (3, [0,6,7,9],      ['#4','6','y']),           # R b2 m3 b5       [0 1 3 6]     R 2 4 7          [0 2 5 b]     R m3 6 b7        [0 3 9 a]
            'R b5 5 7'         : (1, [0,6,7,11],     ['M','#','11','y']),       # R b2 4 b5        [0 1 5 6]     R M3 4 7         [0 4 5 b]     R b2 5 #5        [0 1 7 8]
            'R b5 #5 6'        : (3, [0,6,8,9],      ['o','+','6','y']),        # R 2 m3 b5        [0 2 3 6]     R b2 M3 b7       [0 1 4 a]     R m3 6 7         [0 3 9 b]
            'R b5 #5 b7'       : (1, [0,6,8,10],     ['b','13','#','11','y']),  # R 2 M3 b5        [0 2 4 6]     R 2 M3 b7        [0 2 4 a]     R 2 #5 b7        [0 2 8 a]
            'R b5 #5 7'        : (1, [0,6,8,11],     ['b','13','#','11','y']),  # R 2 4 b5         [0 2 5 6]     R m3 M3 b7       [0 3 4 a]     R b2 5 6         [0 1 7 9]
            'R b5 6 b7'        : (2, [0,6,9,10],     ['13','#','11','y']),      # R m3 M3 b5       [0 3 4 6]     R b2 m3 6        [0 1 3 9]     R 2 #5 7         [0 2 8 b]
            'R b5 6 7'         : (1, [0,6,9,11],     ['M','13','#','11','y']),  # R m3 4 b5        [0 3 5 6]     R 2 m3 6         [0 2 3 9]     R b2 5 b7        [0 1 7 a]
            'R 5 #5 b7'        : (2, [0,7,8,10],     ['b','13','y']),           # R b2 m3 4        [0 1 3 5]     R 2 M3 7         [0 2 4 b]     R 2 6 b7         [0 2 9 a]
            'R 5 6 b7'         : (0, [0,7,9,10],     ['13','y']),               # R 2 m3 4         [0 2 3 5]     R b2 m3 b7       [0 1 3 a]     R 2 6 7          [0 2 9 b]
            'R 5 6 7'          : (1, [0,7,9,11],     ['M','13','y']),           # R 2 M3 4         [0 2 4 5]     R 2 m3 b7        [0 2 3 a]     R b2 #5 b7       [0 1 8 a]
            'R #5 6 b7'        : (1, [0,8,9,10],     ['+','13','y']),           # R b2 2 M3        [0 1 2 4]     R b2 m3 7        [0 1 3 b]     R 2 b7 7         [0 2 a b]
            'R b2 m3 4 5'      : (4, [0,1,3,5,7],    ['m','b2','4']),           # R 2 M3 b5 7      [0 2 4 6 b]   R 2 M3 6 b7      [0 2 4 9 a]   R 2 5 #5 b7      [0 2 7 8 a]   R 4 b5 #5 b7     [0 5 6 8 a]
            'R b2 m3 4 #5'     : (4, [0,1,3,5,8],    ['m','b2','4','+']),       # R 2 M3 5 7       [0 2 4 7 b]   R 2 4 6 b7       [0 2 5 9 a]   R m3 5 #5 b7     [0 3 7 8 a]   R M3 4 5 6       [0 4 5 7 9]
            'R b2 m3 4 6'      : (4, [0,1,3,5,9],    ['m','b2','4','6','x']),   # R 2 M3 #5 7      [0 2 4 8 b]   R 2 b5 6 b7      [0 2 6 9 a]   R M3 5 #5 b7     [0 4 7 8 a]   R m3 M3 b5 #5    [0 3 4 6 8]
            'R b2 m3 4 b7'     : (0, [0,1,3,5,10],   ['m','11','b9','x']),      # R 2 M3 6 7       [0 2 4 9 b]   R 2 5 6 b7       [0 2 7 9 a]   R 4 5 #5 b7      [0 5 7 8 a]   R 2 m3 4 5       [0 2 3 5 7]
            'R b2 m3 b5 #5'    : (4, [0,1,3,6,8],    ['o','+','b2']),           # R 2 4 5 7        [0 2 5 7 b]   R m3 4 6 b7      [0 3 5 9 a]   R 2 b5 5 6       [0 2 6 7 9]   R M3 4 5 b7      [0 4 5 7 a]
            'R b2 m3 b5 b7'    : (2, [0,1,3,6,10],   ['07','b9']),              # R 2 4 6 7        [0 2 5 9 b]   R m3 5 6 b7      [0 3 7 9 a]   R M3 b5 5 6      [0 4 6 7 9]   R 2 m3 4 #5      [0 2 3 5 8]
            'R b2 m3 5 #5'     : (3, [0,1,3,7,8],    ['m','b2','+']),           # R 2 b5 5 7       [0 2 6 7 b]   R M3 4 6 b7      [0 4 5 9 a]   R b2 4 b5 #5     [0 1 5 6 8]   R M3 4 5 7       [0 4 5 7 b]
            'R b2 m3 5 b7'     : (1, [0,1,3,7,10],   ['m','b9']),               # R 2 b5 6 7       [0 2 6 9 b]   R M3 5 6 b7      [0 4 7 9 a]   R m3 4 b5 #5     [0 3 5 6 8]   R 2 m3 4 6       [0 2 3 5 9]
            'R b2 m3 #5 b7'    : (3, [0,1,3,8,10],   ['mb','9','b','13','x']),  # R 2 5 6 7        [0 2 7 9 b]   R 4 5 6 b7       [0 5 7 9 a]   R 2 M3 4 5       [0 2 4 5 7]   R 2 m3 4 b7      [0 2 3 5 a]
            'R b2 M3 b5 6'     : (3, [0,1,4,6,9],    ['b2','b5','6']),          # R m3 4 #5 7      [0 3 5 8 b]   R 2 4 #5 6       [0 2 5 8 9]   R m3 b5 5 b7     [0 3 6 7 a]   R m3 M3 5 6      [0 3 4 7 9]
            'R b2 M3 b5 b7'    : (1, [0,1,4,6,10],   ['m','9','#','11']),       # R m3 4 6 7       [0 3 5 9 b]   R 2 b5 #5 6      [0 2 6 8 9]   R M3 b5 5 b7     [0 4 6 7 a]   R 2 m3 b5 #5     [0 2 3 6 8]
            'R b2 M3 5 6'      : (2, [0,1,4,7,9],    ['b2','6']),               # R m3 b5 #5 7     [0 3 6 8 b]   R m3 4 #5 6      [0 3 5 8 9]   R 2 4 b5 6       [0 2 5 6 9]   R m3 M3 5 b7     [0 3 4 7 a]
            'R b2 M3 5 b7'     : (0, [0,1,4,7,10],   ['b9']),                   # R m3 b5 6 7      [0 3 6 9 b]   R m3 b5 #5 6     [0 3 6 8 9]   R m3 4 b5 6      [0 3 5 6 9]   R 2 m3 b5 6      [0 2 3 6 9]
            'R b2 4 b5 #5'     : (4, [0,1,5,6,8],    ['s4','b2','o','+']),      # R M3 4 5 7       [0 4 5 7 b]   R b2 m3 5 #5     [0 1 3 7 8]   R 2 b5 5 7       [0 2 6 7 b]   R M3 4 6 b7      [0 4 5 9 a]
            'R b2 4 b5 b7'     : (2, [0,1,5,6,10],   ['11','b9','b5','y']),     # R M3 4 6 7       [0 4 5 9 b]   R b2 4 5 #5      [0 1 5 7 8]   R M3 b5 5 7      [0 4 6 7 b]   R 2 m3 5 #5      [0 2 3 7 8]
            'R b2 4 5 #5'      : (4, [0,1,5,7,8],    ['s4','b2','+']),          # R M3 b5 5 7      [0 4 6 7 b]   R 2 m3 5 #5      [0 2 3 7 8]   R b2 4 b5 b7     [0 1 5 6 a]   R M3 4 6 7       [0 4 5 9 b]
            'R b2 4 #5 b7'     : (3, [0,1,5,8,10],   ['b9','s4','+']),          # R M3 5 6 7       [0 4 7 9 b]   R m3 4 5 #5      [0 3 5 7 8]   R 2 M3 4 6       [0 2 4 5 9]   R 2 m3 5 b7      [0 2 3 7 a]
            'R 2 m3 4 5'       : (4, [0,2,3,5,7],    ['m','2','4']),            # R b2 m3 4 b7     [0 1 3 5 a]   R 2 M3 6 7       [0 2 4 9 b]   R 2 5 6 b7       [0 2 7 9 a]   R 4 5 #5 b7      [0 5 7 8 a]
            'R 2 m3 4 #5'      : (4, [0,2,3,5,8],    ['m','2','4','+']),        # R b2 m3 b5 b7    [0 1 3 6 a]   R 2 4 6 7        [0 2 5 9 b]   R m3 5 6 b7      [0 3 7 9 a]   R M3 b5 5 6      [0 4 6 7 9]
            'R 2 m3 4 6'       : (4, [0,2,3,5,9],    ['m','2','4','6','x']),    # R b2 m3 5 b7     [0 1 3 7 a]   R 2 b5 6 7       [0 2 6 9 b]   R M3 5 6 b7      [0 4 7 9 a]   R m3 4 b5 #5     [0 3 5 6 8]
            'R 2 m3 4 b7'      : (0, [0,2,3,5,10],   ['m','11','9']),           # R b2 m3 #5 b7    [0 1 3 8 a]   R 2 5 6 7        [0 2 7 9 b]   R 4 5 6 b7       [0 5 7 9 a]   R 2 M3 4 5       [0 2 4 5 7]
            'R 2 m3 b5 #5'     : (3, [0,2,3,6,8],    ['o','+','2']),            # R b2 M3 b5 b7    [0 1 4 6 a]   R m3 4 6 7       [0 3 5 9 b]   R 2 b5 #5 6      [0 2 6 8 9]   R M3 b5 5 b7     [0 4 6 7 a]
            'R 2 m3 b5 6'      : (3, [0,2,3,6,9],    ['o','2','6']),            # R b2 M3 5 b7     [0 1 4 7 a]   R m3 b5 6 7      [0 3 6 9 b]   R m3 b5 #5 6     [0 3 6 8 9]   R m3 4 b5 6      [0 3 5 6 9]
            'R 2 m3 5 #5'      : (3, [0,2,3,7,8],    ['m','+','2']),            # R b2 4 b5 b7     [0 1 5 6 a]   R M3 4 6 7       [0 4 5 9 b]   R b2 4 5 #5      [0 1 5 7 8]   R M3 b5 5 7      [0 4 6 7 b]
            'R 2 m3 5 b7'      : (0, [0,2,3,7,10],   ['m9']),                   # R b2 4 #5 b7     [0 1 5 8 a]   R M3 5 6 7       [0 4 7 9 b]   R m3 4 5 #5      [0 3 5 7 8]   R 2 M3 4 6       [0 2 4 5 9]
            'R 2 M3 4 5'       : (4, [0,2,4,5,7],    ['2','4']),                # R 2 m3 4 b7      [0 2 3 5 a]   R b2 m3 #5 b7    [0 1 3 8 a]   R 2 5 6 7        [0 2 7 9 b]   R 4 5 6 b7       [0 5 7 9 a]
            'R 2 M3 4 6'       : (2, [0,2,4,5,9],    ['2','4','6','x']),        # R 2 m3 5 b7      [0 2 3 7 a]   R b2 4 #5 b7     [0 1 5 8 a]   R M3 5 6 7       [0 4 7 9 b]   R m3 4 5 #5      [0 3 5 7 8]
            'R 2 M3 b5 6'      : (4, [0,2,4,6,9],    ['2','b5','6']),           # R 2 M3 5 b7      [0 2 4 7 a]   R 2 4 #5 b7      [0 2 5 8 a]   R m3 b5 #5 b7    [0 3 6 8 a]   R m3 4 5 6       [0 3 5 7 9]
            'R 2 M3 b5 7'      : (1, [0,2,4,6,11],   ['M#','11','9']),          # R 2 M3 6 b7      [0 2 4 9 a]   R 2 5 #5 b7      [0 2 7 8 a]   R 4 b5 #5 b7     [0 5 6 8 a]   R b2 m3 4 5      [0 1 3 5 7]
            'R 2 M3 5 6'       : (1, [0,2,4,7,9],    ['2','6']),                # R 2 4 5 b7       [0 2 5 7 a]   R m3 4 #5 b7     [0 3 5 8 a]   R 2 4 5 6        [0 2 5 7 9]   R m3 4 5 b7      [0 3 5 7 a]
            'R 2 M3 5 b7'      : (0, [0,2,4,7,10],   ['9']),                    # R 2 4 #5 b7      [0 2 5 8 a]   R m3 b5 #5 b7    [0 3 6 8 a]   R m3 4 5 6       [0 3 5 7 9]   R 2 M3 b5 6      [0 2 4 6 9]
            'R 2 M3 5 7'       : (0, [0,2,4,7,11],   ['M9']),                   # R 2 4 6 b7       [0 2 5 9 a]   R m3 5 #5 b7     [0 3 7 8 a]   R M3 4 5 6       [0 4 5 7 9]   R b2 m3 4 #5     [0 1 3 5 8]
            'R 2 M3 #5 7'      : (2, [0,2,4,8,11],   ['M','b','13','9','x']),   # R 2 b5 6 b7      [0 2 6 9 a]   R M3 5 #5 b7     [0 4 7 8 a]   R m3 M3 b5 #5    [0 3 4 6 8]   R b2 m3 4 6      [0 1 3 5 9]
            'R 2 M3 6 b7'      : (0, [0,2,4,9,10],   ['13','9','x']),           # R 2 5 #5 b7      [0 2 7 8 a]   R 4 b5 #5 b7     [0 5 6 8 a]   R b2 m3 4 5      [0 1 3 5 7]   R 2 M3 b5 7      [0 2 4 6 b]
            'R 2 M3 6 7'       : (2, [0,2,4,9,11],   ['M','13','9','x']),       # R 2 5 6 b7       [0 2 7 9 a]   R 4 5 #5 b7      [0 5 7 8 a]   R 2 m3 4 5       [0 2 3 5 7]   R b2 m3 4 b7     [0 1 3 5 a]
            'R 2 4 b5 6'       : (3, [0,2,5,6,9],    ['s2','s4','o','6']),      # R m3 M3 5 b7     [0 3 4 7 a]   R b2 M3 5 6      [0 1 4 7 9]   R m3 b5 #5 7     [0 3 6 8 b]   R m3 4 #5 6      [0 3 5 8 9]
            'R 2 4 5 6'        : (2, [0,2,5,7,9],    ['s2','s4','6']),          # R m3 4 5 b7      [0 3 5 7 a]   R 2 M3 5 6       [0 2 4 7 9]   R 2 4 5 b7       [0 2 5 7 a]   R m3 4 #5 b7     [0 3 5 8 a]
            'R 2 4 5 b7'       : (3, [0,2,5,7,10],   ['7','s2','s4']),          # R m3 4 #5 b7     [0 3 5 8 a]   R 2 4 5 6        [0 2 5 7 9]   R m3 4 5 b7      [0 3 5 7 a]   R 2 M3 5 6       [0 2 4 7 9]
            'R 2 4 5 7'        : (2, [0,2,5,7,11],   ['M7','s2','s4']),         # R m3 4 6 b7      [0 3 5 9 a]   R 2 b5 5 6       [0 2 6 7 9]   R M3 4 5 b7      [0 4 5 7 a]   R b2 m3 b5 #5    [0 1 3 6 8]
            'R 2 4 #5 6'       : (4, [0,2,5,8,9],    ['+','s2','s4','6']),      # R m3 b5 5 b7     [0 3 6 7 a]   R m3 M3 5 6      [0 3 4 7 9]   R b2 M3 b5 6     [0 1 4 6 9]   R m3 4 #5 7      [0 3 5 8 b]
            'R 2 4 #5 b7'      : (3, [0,2,5,8,10],   ['11','9','+','y']),       # R m3 b5 #5 b7    [0 3 6 8 a]   R m3 4 5 6       [0 3 5 7 9]   R 2 M3 b5 6      [0 2 4 6 9]   R 2 M3 5 b7      [0 2 4 7 a]
            'R 2 4 6 b7'       : (3, [0,2,5,9,10],   ['13','s2','s4','x']),     # R m3 5 #5 b7     [0 3 7 8 a]   R M3 4 5 6       [0 4 5 7 9]   R b2 m3 4 #5     [0 1 3 5 8]   R 2 M3 5 7       [0 2 4 7 b]
            'R 2 4 6 7'        : (1, [0,2,5,9,11],   ['M','13','s2','s4','x']), # R m3 5 6 b7      [0 3 7 9 a]   R M3 b5 5 6      [0 4 6 7 9]   R 2 m3 4 #5      [0 2 3 5 8]   R b2 m3 b5 b7    [0 1 3 6 a]
            'R 2 b5 5 6'       : (3, [0,2,6,7,9],    ['2','#4','6']),           # R M3 4 5 b7      [0 4 5 7 a]   R b2 m3 b5 #5    [0 1 3 6 8]   R 2 4 5 7        [0 2 5 7 b]   R m3 4 6 b7      [0 3 5 9 a]
            'R 2 b5 5 7'       : (2, [0,2,6,7,11],   ['M#','11','s2']),         # R M3 4 6 b7      [0 4 5 9 a]   R b2 4 b5 #5     [0 1 5 6 8]   R M3 4 5 7       [0 4 5 7 b]   R b2 m3 5 #5     [0 1 3 7 8]
            'R 2 b5 #5 6'      : (4, [0,2,6,8,9],    ['s2','#4','+','6']),      # R M3 b5 5 b7     [0 4 6 7 a]   R 2 m3 b5 #5     [0 2 3 6 8]   R b2 M3 b5 b7    [0 1 4 6 a]   R m3 4 6 7       [0 3 5 9 b]
            'R 2 b5 6 b7'      : (1, [0,2,6,9,10],   ['s2','#','11','13','x']), # R M3 5 #5 b7     [0 4 7 8 a]   R m3 M3 b5 #5    [0 3 4 6 8]   R b2 m3 4 6      [0 1 3 5 9]   R 2 M3 #5 7      [0 2 4 8 b]
            'R 2 b5 6 7'       : (2, [0,2,6,9,11],   ['M','13','s2','o']),      # R M3 5 6 b7      [0 4 7 9 a]   R m3 4 b5 #5     [0 3 5 6 8]   R 2 m3 4 6       [0 2 3 5 9]   R b2 m3 5 b7     [0 1 3 7 a]
            'R 2 5 #5 b7'      : (2, [0,2,7,8,10],   ['b','13','s2']),          # R 4 b5 #5 b7     [0 5 6 8 a]   R b2 m3 4 5      [0 1 3 5 7]   R 2 M3 b5 7      [0 2 4 6 b]   R 2 M3 6 b7      [0 2 4 9 a]
            'R 2 5 6 b7'       : (1, [0,2,7,9,10],   ['13','s2']),              # R 4 5 #5 b7      [0 5 7 8 a]   R 2 m3 4 5       [0 2 3 5 7]   R b2 m3 4 b7     [0 1 3 5 a]   R 2 M3 6 7       [0 2 4 9 b]
            'R 2 5 6 7'        : (2, [0,2,7,9,11],   ['M','13','s2']),          # R 4 5 6 b7       [0 5 7 9 a]   R 2 M3 4 5       [0 2 4 5 7]   R 2 m3 4 b7      [0 2 3 5 a]   R b2 m3 #5 b7    [0 1 3 8 a]
            'R m3 M3 b5 #5'    : (3, [0,3,4,6,8],    ['#2','#4','#5']),         # R b2 m3 4 6      [0 1 3 5 9]   R 2 M3 #5 7      [0 2 4 8 b]   R 2 b5 6 b7      [0 2 6 9 a]   R M3 5 #5 b7     [0 4 7 8 a]
            'R m3 M3 5 6'      : (2, [0,3,4,7,9],    ['#2','6']),               # R b2 M3 b5 6     [0 1 4 6 9]   R m3 4 #5 7      [0 3 5 8 b]   R 2 4 #5 6       [0 2 5 8 9]   R m3 b5 5 b7     [0 3 6 7 a]
            'R m3 M3 5 b7'     : (0, [0,3,4,7,10],   ['#9']),                   # R b2 M3 5 6      [0 1 4 7 9]   R m3 b5 #5 7     [0 3 6 8 b]   R m3 4 #5 6      [0 3 5 8 9]   R 2 4 b5 6       [0 2 5 6 9]
            'R m3 4 b5 #5'     : (3, [0,3,5,6,8],    ['o','4','+']),            # R 2 m3 4 6       [0 2 3 5 9]   R b2 m3 5 b7     [0 1 3 7 a]   R 2 b5 6 7       [0 2 6 9 b]   R M3 5 6 b7      [0 4 7 9 a]
            'R m3 4 b5 6'      : (4, [0,3,5,6,9],    ['o','4','6']),            # R 2 m3 b5 6      [0 2 3 6 9]   R b2 M3 5 b7     [0 1 4 7 a]   R m3 b5 6 7      [0 3 6 9 b]   R m3 b5 #5 6     [0 3 6 8 9]
            'R m3 4 5 #5'      : (4, [0,3,5,7,8],    ['m','4','+']),            # R 2 M3 4 6       [0 2 4 5 9]   R 2 m3 5 b7      [0 2 3 7 a]   R b2 4 #5 b7     [0 1 5 8 a]   R M3 5 6 7       [0 4 7 9 b]
            'R m3 4 5 6'       : (2, [0,3,5,7,9],    ['m','4','6']),            # R 2 M3 b5 6      [0 2 4 6 9]   R 2 M3 5 b7      [0 2 4 7 a]   R 2 4 #5 b7      [0 2 5 8 a]   R m3 b5 #5 b7    [0 3 6 8 a]
            'R m3 4 5 b7'      : (0, [0,3,5,7,10],   ['m','11']),               # R 2 M3 5 6       [0 2 4 7 9]   R 2 4 5 b7       [0 2 5 7 a]   R m3 4 #5 b7     [0 3 5 8 a]   R 2 4 5 6        [0 2 5 7 9]
            'R m3 4 #5 6'      : (4, [0,3,5,8,9],    ['m','4','+','6']),        # R 2 4 b5 6       [0 2 5 6 9]   R m3 M3 5 b7     [0 3 4 7 a]   R b2 M3 5 6      [0 1 4 7 9]   R m3 b5 #5 7     [0 3 6 8 b]
            'R m3 4 #5 b7'     : (4, [0,3,5,8,10],   ['m','11','+']),           # R 2 4 5 6        [0 2 5 7 9]   R m3 4 5 b7      [0 3 5 7 a]   R 2 M3 5 6       [0 2 4 7 9]   R 2 4 5 b7       [0 2 5 7 a]
            'R m3 4 #5 7'      : (1, [0,3,5,8,11],   ['m','b','13','11']),      # R 2 4 #5 6       [0 2 5 8 9]   R m3 b5 5 b7     [0 3 6 7 a]   R m3 M3 5 6      [0 3 4 7 9]   R b2 M3 b5 6     [0 1 4 6 9]
            'R m3 4 6 b7'      : (1, [0,3,5,9,10],   ['m','13','11','x']),      # R 2 b5 5 6       [0 2 6 7 9]   R M3 4 5 b7      [0 4 5 7 a]   R b2 m3 b5 #5    [0 1 3 6 8]   R 2 4 5 7        [0 2 5 7 b]
            'R m3 4 6 7'       : (2, [0,3,5,9,11],   ['mM','13','11','x']),     # R 2 b5 #5 6      [0 2 6 8 9]   R M3 b5 5 b7     [0 4 6 7 a]   R 2 m3 b5 #5     [0 2 3 6 8]   R b2 M3 b5 b7    [0 1 4 6 a]
            'R m3 b5 5 b7'     : (0, [0,3,6,7,10],   ['m','#','11']),           # R m3 M3 5 6      [0 3 4 7 9]   R b2 M3 b5 6     [0 1 4 6 9]   R m3 4 #5 7      [0 3 5 8 b]   R 2 4 #5 6       [0 2 5 8 9]
            'R m3 b5 #5 6'     : (2, [0,3,6,8,9],    ['o','+','6']),            # R m3 4 b5 6      [0 3 5 6 9]   R 2 m3 b5 6      [0 2 3 6 9]   R b2 M3 5 b7     [0 1 4 7 a]   R m3 b5 6 7      [0 3 6 9 b]
            'R m3 b5 #5 b7'    : (1, [0,3,6,8,10],   ['07','+']),               # R m3 4 5 6       [0 3 5 7 9]   R 2 M3 b5 6      [0 2 4 6 9]   R 2 M3 5 b7      [0 2 4 7 a]   R 2 4 #5 b7      [0 2 5 8 a]
            'R m3 b5 #5 7'     : (1, [0,3,6,8,11],   ['m#','11','b','13']),     # R m3 4 #5 6      [0 3 5 8 9]   R 2 4 b5 6       [0 2 5 6 9]   R m3 M3 5 b7     [0 3 4 7 a]   R b2 M3 5 6      [0 1 4 7 9]
            'R m3 b5 6 7'      : (1, [0,3,6,9,11],   ['o','M','13']),           # R m3 b5 #5 6     [0 3 6 8 9]   R m3 4 b5 6      [0 3 5 6 9]   R 2 m3 b5 6      [0 2 3 6 9]   R b2 M3 5 b7     [0 1 4 7 a]
            'R m3 5 #5 b7'     : (1, [0,3,7,8,10],   ['m','b','13']),           # R M3 4 5 6       [0 4 5 7 9]   R b2 m3 4 #5     [0 1 3 5 8]   R 2 M3 5 7       [0 2 4 7 b]   R 2 4 6 b7       [0 2 5 9 a]
            'R m3 5 6 b7'      : (0, [0,3,7,9,10],   ['m','13']),               # R M3 b5 5 6      [0 4 6 7 9]   R 2 m3 4 #5      [0 2 3 5 8]   R b2 m3 b5 b7    [0 1 3 6 a]   R 2 4 6 7        [0 2 5 9 b]
            'R M3 4 5 6'       : (2, [0,4,5,7,9],    ['4','6']),                # R b2 m3 4 #5     [0 1 3 5 8]   R 2 M3 5 7       [0 2 4 7 b]   R 2 4 6 b7       [0 2 5 9 a]   R m3 5 #5 b7     [0 3 7 8 a]
            'R M3 4 5 b7'      : (0, [0,4,5,7,10],   ['11']),                   # R b2 m3 b5 #5    [0 1 3 6 8]   R 2 4 5 7        [0 2 5 7 b]   R m3 4 6 b7      [0 3 5 9 a]   R 2 b5 5 6       [0 2 6 7 9]
            'R M3 4 5 7'       : (1, [0,4,5,7,11],   ['M','11']),               # R b2 m3 5 #5     [0 1 3 7 8]   R 2 b5 5 7       [0 2 6 7 b]   R M3 4 6 b7      [0 4 5 9 a]   R b2 4 b5 #5     [0 1 5 6 8]
            'R M3 4 6 b7'      : (0, [0,4,5,9,10],   ['13','11','x']),          # R b2 4 b5 #5     [0 1 5 6 8]   R M3 4 5 7       [0 4 5 7 b]   R b2 m3 5 #5     [0 1 3 7 8]   R 2 b5 5 7       [0 2 6 7 b]
            'R M3 4 6 7'       : (1, [0,4,5,9,11],   ['M','13','11','x']),      # R b2 4 5 #5      [0 1 5 7 8]   R M3 b5 5 7      [0 4 6 7 b]   R 2 m3 5 #5      [0 2 3 7 8]   R b2 4 b5 b7     [0 1 5 6 a]
            'R M3 b5 5 6'      : (3, [0,4,6,7,9],    ['#4','6']),               # R 2 m3 4 #5      [0 2 3 5 8]   R b2 m3 b5 b7    [0 1 3 6 a]   R 2 4 6 7        [0 2 5 9 b]   R m3 5 6 b7      [0 3 7 9 a]
            'R M3 b5 5 b7'     : (0, [0,4,6,7,10],   ['#','11]']),              # R 2 m3 b5 #5     [0 2 3 6 8]   R b2 M3 b5 b7    [0 1 4 6 a]   R m3 4 6 7       [0 3 5 9 b]   R 2 b5 #5 6      [0 2 6 8 9]
            'R M3 b5 5 7'      : (0, [0,4,6,7,11],   ['M#','11']),              # R 2 m3 5 #5      [0 2 3 7 8]   R b2 4 b5 b7     [0 1 5 6 a]   R M3 4 6 7       [0 4 5 9 b]   R b2 4 5 #5      [0 1 5 7 8]
            'R M3 5 #5 b7'     : (0, [0,4,7,8,10],   ['b','13']),               # R m3 M3 b5 #5    [0 3 4 6 8]   R b2 m3 4 6      [0 1 3 5 9]   R 2 M3 #5 7      [0 2 4 8 b]   R 2 b5 6 b7      [0 2 6 9 a]
            'R M3 5 6 b7'      : (0, [0,4,7,9,10],   ['13']),                   # R m3 4 b5 #5     [0 3 5 6 8]   R 2 m3 4 6       [0 2 3 5 9]   R b2 m3 5 b7     [0 1 3 7 a]   R 2 b5 6 7       [0 2 6 9 b]
            'R M3 5 6 7'       : (1, [0,4,7,9,11],   ['M','13']),               # R m3 4 5 #5      [0 3 5 7 8]   R 2 M3 4 6       [0 2 4 5 9]   R 2 m3 5 b7      [0 2 3 7 a]   R b2 4 #5 b7     [0 1 5 8 a]
            'R 4 b5 #5 b7'     : (3, [0,5,6,8,10],   ['b','13','#11','s4']),    # R b2 m3 4 5      [0 1 3 5 7]   R 2 M3 b5 7      [0 2 4 6 b]   R 2 M3 6 b7      [0 2 4 9 a]   R 2 5 #5 b7      [0 2 7 8 a]
            'R 4 5 #5 b7'      : (3, [0,5,7,8,10],   ['b','13','s4']),          # R 2 m3 4 5       [0 2 3 5 7]   R b2 m3 4 b7     [0 1 3 5 a]   R 2 M3 6 7       [0 2 4 9 b]   R 2 5 6 b7       [0 2 7 9 a]
            'R 4 5 6 b7'       : (1, [0,5,7,9,10],   ['13','s4']),              # R 2 M3 4 5       [0 2 4 5 7]   R 2 m3 4 b7      [0 2 3 5 a]   R b2 m3 #5 b7    [0 1 3 8 a]   R 2 5 6 7        [0 2 7 9 b]
            'R b2 m3 4 b5 b7'  : (3, [0,1,3,5,6,10], ['o','11','b9']),          # R 2 M3 4 6 7     [0 2 4 5 9 b] R 2 m3 5 6 b7    [0 2 3 7 9 a] R b2 4 5 #5 b7   [0 1 5 7 8 a] R M3 b5 5 6 7    [0 4 6 7 9 b] R 2 m3 4 5 #5    [0 2 3 5 7 8]
            'R b2 m3 4 5 #5'   : (5, [0,1,3,5,7,8],  ['m','+','b2','4']),       # R 2 M3 b5 5 7    [0 2 4 6 7 b] R 2 M3 4 6 b7    [0 2 4 5 9 a] R 2 m3 5 #5 b7   [0 2 3 7 8 a] R b2 4 b5 #5 b7  [0 1 5 6 8 a] R M3 4 5 6 7     [0 4 5 7 9 b]
            'R b2 m3 4 #5 b7'  : (1, [0,1,3,5,8,10], ['m','11','b9','+']),      # R 2 M3 5 6 7     [0 2 4 7 9 b] R 2 4 5 6 b7     [0 2 5 7 9 a] R m3 4 5 #5 b7   [0 3 5 7 8 a] R 2 M3 4 5 6     [0 2 4 5 7 9] R 2 m3 4 5 b7    [0 2 3 5 7 a]
            'R b2 m3 b5 #5 b7' : (3, [0,1,3,6,8,10], ['o','b','13','b9']),      # R 2 4 5 6 7      [0 2 5 7 9 b] R m3 4 5 6 b7    [0 3 5 7 9 a] R 2 M3 b5 5 6    [0 2 4 6 7 9] R 2 M3 4 5 b7    [0 2 4 5 7 a] R 2 m3 4 #5 b7   [0 2 3 5 8 a]
            'R b2 4 b5 #5 b7'  : (4, [0,1,5,6,8,10], ['b','13','b','9','s4']),  # R M3 4 5 6 7     [0 4 5 7 9 b] R b2 m3 4 5 #5   [0 1 3 5 7 8] R 2 M3 b5 5 7    [0 2 4 6 7 b] R 2 M3 4 6 b7    [0 2 4 5 9 a] R 2 m3 5 #5 b7   [0 2 3 7 8 a]
            'R b2 4 5 #5 b7'   : (4, [0,1,5,7,8,10], ['b','13','b9','s4']),     # R M3 b5 5 6 7    [0 4 6 7 9 b] R 2 m3 4 5 #5    [0 2 3 5 7 8] R b2 m3 4 b5 b7  [0 1 3 5 6 a] R 2 M3 4 6 7     [0 2 4 5 9 b] R 2 m3 5 6 b7    [0 2 3 7 9 a]
            'R 2 m3 4 5 #5'    : (5, [0,2,3,5,7,8],  ['m','+','2','4']),        # R b2 m3 4 b5 b7  [0 1 3 5 6 a] R 2 M3 4 6 7     [0 2 4 5 9 b] R 2 m3 5 6 b7    [0 2 3 7 9 a] R b2 4 5 #5 b7   [0 1 5 7 8 a] R M3 b5 5 6 7    [0 4 6 7 9 b]
            'R 2 m3 4 5 b7'    : (0, [0,2,3,5,7,10], ['m','11','9']),           # R b2 m3 4 #5 b7  [0 1 3 5 8 a] R 2 M3 5 6 7     [0 2 4 7 9 b] R 2 4 5 6 b7     [0 2 5 7 9 a] R m3 4 5 #5 b7   [0 3 5 7 8 a] R 2 M3 4 5 6     [0 2 4 5 7 9]
            'R 2 m3 4 #5 b7'   : (1, [0,2,3,5,8,10], ['m','11','9','+']),       # R b2 m3 b5 #5 b7 [0 1 3 6 8 a] R 2 4 5 6 7      [0 2 5 7 9 b] R m3 4 5 6 b7    [0 3 5 7 9 a] R 2 M3 b5 5 6    [0 2 4 6 7 9] R 2 M3 4 5 b7    [0 2 4 5 7 a]
            'R 2 m3 5 #5 b7'   : (3, [0,2,3,7,8,10], ['mb','13','9']),          # R b2 4 b5 #5 b7  [0 1 5 6 8 a] R M3 4 5 6 7     [0 4 5 7 9 b] R b2 m3 4 5 #5   [0 1 3 5 7 8] R 2 M3 b5 5 7    [0 2 4 6 7 b] R 2 M3 4 6 b7    [0 2 4 5 9 a]
            'R 2 m3 5 6 b7'    : (2, [0,2,3,7,9,10], ['m','13','9']),           # R b2 4 5 #5 b7   [0 1 5 7 8 a] R M3 b5 5 6 7    [0 4 6 7 9 b] R 2 m3 4 5 #5    [0 2 3 5 7 8] R b2 m3 4 b5 b7  [0 1 3 5 6 a] R 2 M3 4 6 7     [0 2 4 5 9 b]
            'R 2 M3 4 5 6'     : (5, [0,2,4,5,7,9],  ['2','4','6']),            # R 2 m3 4 5 b7    [0 2 3 5 7 a] R b2 m3 4 #5 b7  [0 1 3 5 8 a] R 2 M3 5 6 7     [0 2 4 7 9 b] R 2 4 5 6 b7     [0 2 5 7 9 a] R m3 4 5 #5 b7   [0 3 5 7 8 a]
            'R 2 M3 4 5 b7'    : (0, [0,2,4,5,7,10], ['11','9']),               # R 2 m3 4 #5 b7   [0 2 3 5 8 a] R b2 m3 b5 #5 b7 [0 1 3 6 8 a] R 2 4 5 6 7      [0 2 5 7 9 b] R m3 4 5 6 b7    [0 3 5 7 9 a] R 2 M3 b5 5 6    [0 2 4 6 7 9]
            'R 2 M3 4 6 b7'    : (2, [0,2,4,5,9,10], ['13','11','9','x']),      # R 2 m3 5 #5 b7   [0 2 3 7 8 a] R b2 4 b5 #5 b7  [0 1 5 6 8 a] R M3 4 5 6 7     [0 4 5 7 9 b] R b2 m3 4 5 #5   [0 1 3 5 7 8] R 2 M3 b5 5 7    [0 2 4 6 7 b]
            'R 2 M3 4 6 7'     : (0, [0,2,4,5,9,11], ['M','13','11','9','x']),  # R 2 m3 5 6 b7    [0 2 3 7 9 a] R b2 4 5 #5 b7   [0 1 5 7 8 a] R M3 b5 5 6 7    [0 4 6 7 9 b] R 2 m3 4 5 #5    [0 2 3 5 7 8] R b2 m3 4 b5 b7  [0 1 3 5 6 a]
            'R 2 M3 b5 5 6'    : (5, [0,2,4,6,7,9],  ['2','#4','6']),           # R 2 M3 4 5 b7    [0 2 4 5 7 a] R 2 m3 4 #5 b7   [0 2 3 5 8 a] R b2 m3 b5 #5 b7 [0 1 3 6 8 a] R 2 4 5 6 7      [0 2 5 7 9 b] R m3 4 5 6 b7    [0 3 5 7 9 a]
            'R 2 M3 b5 5 7'    : (1, [0,2,4,6,7,11], ['M#','11','9']),          # R 2 M3 4 6 b7    [0 2 4 5 9 a] R 2 m3 5 #5 b7   [0 2 3 7 8 a] R b2 4 b5 #5 b7  [0 1 5 6 8 a] R M3 4 5 6 7     [0 4 5 7 9 b] R b2 m3 4 5 #5   [0 1 3 5 7 8]
            'R 2 M3 5 6 7'     : (3, [0,2,4,7,9,11], ['M','13','9']),           # R 2 4 5 6 b7     [0 2 5 7 9 a] R m3 4 5 #5 b7   [0 3 5 7 8 a] R 2 M3 4 5 6     [0 2 4 5 7 9] R 2 m3 4 5 b7    [0 2 3 5 7 a] R b2 m3 4 #5 b7  [0 1 3 5 8 a]
            'R 2 4 5 6 b7'     : (4, [0,2,5,7,9,10], ['13','s2','s4']),         # R m3 4 5 #5 b7   [0 3 5 7 8 a] R 2 M3 4 5 6     [0 2 4 5 7 9] R 2 m3 4 5 b7    [0 2 3 5 7 a] R b2 m3 4 #5 b7  [0 1 3 5 8 a] R 2 M3 5 6 7     [0 2 4 7 9 b]
            'R 2 4 5 6 7'      : (4, [0,2,5,7,9,11], ['M','13','s2','s4']),     # R m3 4 5 6 b7    [0 3 5 7 9 a] R 2 M3 b5 5 6    [0 2 4 6 7 9] R 2 M3 4 5 b7    [0 2 4 5 7 a] R 2 m3 4 #5 b7   [0 2 3 5 8 a] R b2 m3 b5 #5 b7 [0 1 3 6 8 a]
            'R m3 4 5 #5 b7'   : (2, [0,3,5,7,8,10], ['mb','13','11']),         # R 2 M3 4 5 6     [0 2 4 5 7 9] R 2 m3 4 5 b7    [0 2 3 5 7 a] R b2 m3 4 #5 b7  [0 1 3 5 8 a] R 2 M3 5 6 7     [0 2 4 7 9 b] R 2 4 5 6 b7     [0 2 5 7 9 a]
            'R m3 4 5 6 b7'    : (2, [0,3,5,7,9,10], ['m','13','11']),          # R 2 M3 b5 5 6    [0 2 4 6 7 9] R 2 M3 4 5 b7    [0 2 4 5 7 a] R 2 m3 4 #5 b7   [0 2 3 5 8 a] R b2 m3 b5 #5 b7 [0 1 3 6 8 a] R 2 4 5 6 7      [0 2 5 7 9 b]
            'R M3 4 5 6 7'     : (0, [0,4,5,7,9,11], ['M','13','11']),          # R b2 m3 4 5 #5   [0 1 3 5 7 8] R 2 M3 b5 5 7    [0 2 4 6 7 b] R 2 M3 4 6 b7    [0 2 4 5 9 a] R 2 m3 5 #5 b7   [0 2 3 7 8 a] R b2 4 b5 #5 b7  [0 1 5 6 8 a]
            'R M3 b5 5 6 7'    : (1, [0,4,6,7,9,11], ['M','13','#','11']),      # R 2 m3 4 5 #5    [0 2 3 5 7 8] R b2 m3 4 b5 b7  [0 1 3 5 6 a] R 2 M3 4 6 7     [0 2 4 5 9 b] R 2 m3 5 6 b7    [0 2 3 7 9 a] R b2 4 5 #5 b7   [0 1 5 7 8 a]
            }
    ####################################################################################################################################################################################################
#seperate M#
