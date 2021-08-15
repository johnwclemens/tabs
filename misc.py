import sys, os, collections
sys.path.insert(0, os.path.abspath('.'))
import tabs

VERBOSE = tabs.VERBOSE

class Note(object):
    NUM_SEMI_TONES = 12
    SHARP_TONES    = { 0:'C', 1:'C#', 2:'D', 3:'D#', 4:'E', 5:'F', 6:'F#', 7:'G', 8:'G#', 9:'A', 10:'A#', 11:'B' }
    FLAT_TONES     = { 0:'C', 1:'Db', 2:'D', 3:'Eb', 4:'E', 5:'F', 6:'Gb', 7:'G', 8:'Ab', 9:'A', 10:'Bb', 11:'B' }
    INDICES = { 'C0': 0, 'C#0': 1, 'Db0': 1, 'D0': 2, 'D#0': 3, 'Eb0': 3, 'E0': 4, 'F0': 5, 'F#0': 6, 'Gb0': 6, 'G0': 7, 'G#0': 8, 'Ab0': 8, 'A0': 9, 'A#0':10, 'Bb0':10, 'B0':11,
                'C1':12, 'C#1':13, 'Db1':13, 'D1':14, 'D#1':15, 'Eb1':15, 'E1':16, 'F1':17, 'F#1':18, 'Gb1':18, 'G1':19, 'G#1':20, 'Ab1':20, 'A1':21, 'A#1':22, 'Bb1':22, 'B1':23,
                'C2':24, 'C#2':25, 'Db2':25, 'D2':26, 'D#2':27, 'Eb2':27, 'E2':28, 'F2':29, 'F#2':30, 'Gb2':30, 'G2':31, 'G#2':32, 'Ab2':32, 'A2':33, 'A#2':34, 'Bb2':34, 'B2':35,
                'C3':36, 'C#3':37, 'Db3':37, 'D3':38, 'D#3':39, 'Eb3':39, 'E3':40, 'F3':41, 'F#3':42, 'Gb3':42, 'G3':43, 'G#3':44, 'Ab3':44, 'A3':45, 'A#3':46, 'Bb3':46, 'B3':47,
                'C4':48, 'C#4':49, 'Db4':49, 'D4':50, 'D#4':51, 'Eb4':51, 'E4':52, 'F4':53, 'F#4':54, 'Gb4':54, 'G4':55, 'G#4':56, 'Ab4':56, 'A4':57, 'A#4':58, 'Bb4':58, 'B4':59,
                'C5':60, 'C#5':61, 'Db5':61, 'D5':62, 'D#5':63, 'Eb5':63, 'E5':64, 'F5':65, 'F#5':66, 'Gb5':66, 'G5':67, 'G#5':68, 'Ab5':68, 'A5':69, 'A#5':70, 'Bb5':70, 'B5':71,
                'C6':72, 'C#6':73, 'Db6':73, 'D6':74, 'D#6':75, 'Eb6':75, 'E6':76, 'F6':77, 'F#6':78, 'Gb6':78, 'G6':79, 'G#6':80, 'Ab6':80, 'A6':81, 'A#6':82, 'Bb6':82, 'B6':83,
                'C7':84, 'C#7':85, 'Db7':85, 'D7':86, 'D#7':87, 'Eb7':87, 'E7':88, 'F7':89, 'F#7':90, 'Gb7':90, 'G7':91, 'G#7':92, 'Ab7':92, 'A7':93, 'A#7':94, 'Bb7':94, 'B7':95,
                'C8':96 } # For simplicity omit double flats and double sharps and other redundant enharmonic note names e.g. Abb, C##, Cb, B#, Fb, E# etc...
    def __init__(self, i, ks=None):
        self.index = i
        self.ks    = ks
        self.name  = self.FLAT_TONES[i % len(self.FLAT_TONES)]
####################################################################################################################################################################################################
class Chord(object):
    INTERVALS =     { 0:'R', 1:'b2', 2:'2', 3:'m3', 4:'M3', 5:'4', 6:'b5', 7:'5', 8:'a5', 9:'6', 10:'b7', 11:'7' }
    INTERVAL_RANK = { 'R':0, 'b2':1, '2':2, 'm3':3, 'M3':4, '4':5, 'b5':6, '5':7, 'a5':8, '6':9, 'b7':10, '7':11, }

    def __init__(self, tobj, logfile):
        self.tobj    = tobj
        self.logFile = logfile
        self.limap, self.limap1, self.limap2 = [], [], []
        self.mlimap  = {}
        self.chordNames = self.initChordNames()

    @staticmethod
    def getChordKey(keys):  return ' '.join(keys)

    def updateImap(self, imap, name, dbg=0):
        intervals = list(imap.keys())   ;   notes = list(imap.values())
        imap = [intervals, notes, name]   ;   d1, d2 = '<', '>'  ;  why ='limap'
        if name and name != ' ':  self.limap1.append(imap)
        else:                     self.limap2.append(imap)
        if dbg:
            for i, m in enumerate(self.limap1):
                tabs.Tabs.log(tabs.FMTR.format(f'{why:8}1 {i+1}  [ <{m[2]:<6}> {tabs.fmtl(m[0], 2, "<", d1, d2):17} {tabs.fmtl(m[1], 2, "<", d1, d2):17} ]'), file=self.logFile)
            for i, m in enumerate(self.limap2):
                tabs.Tabs.log(tabs.FMTR.format(f'{why:8}2 {i+1}  [ <{m[2]:<6}> {tabs.fmtl(m[0], 2, "<", d1, d2):17} {tabs.fmtl(m[1], 2, "<", d1, d2):17} ]'), file=self.logFile)
        if   self.limap1 and self.limap1[0]: return self.limap1[0][2]
        elif self.limap2 and self.limap2[0]: return self.limap2[0][2]

    def getChordName(self, p, l, c, dbg=VERBOSE):
        cc = self.tobj.plct2cc(p, l, c, 0)
        if dbg: tabs.Tabs.log(f'p={p} l={l} c={c} cc={cc}')
#        if cc in self.mlimap: tabs.Tabs.log(f'ERROR: Unexpected key cc={cc} exists')   ;   return ''
        self.limap= []  ;  chordName = ''
        imapKeys, imapNotes   = None, None   ;   d1, d2 = '<', '>'
        mask, notes, indices  = self.getNotesIndices(p, l, c)
        for i in range(len(indices)):
            intervals                           = self.getIntervals(indices, i, mask)
            imap, imapKeys, imapNotes, chordKey = self.getImapKeys(intervals, notes, mask)
            chordName = self._getChordName_B(imap)
            if dbg and chordName: tabs.Tabs.log(f'Inner Chord  [ <{chordName:<6}> {tabs.fmtl(imapKeys, 2, "<", d1, d2):17} {tabs.fmtl(imapNotes, 2, "<", d1, d2):17} ]', file=self.logFile)
            chordName                           = self.updateImap(imap, chordName)
        if chordName:
            if dbg: tabs.Tabs.log(f'Outer Chord  [ <{chordName:<6}> {tabs.fmtl(imapKeys, 2, "<", d1, d2):17} {tabs.fmtl(imapNotes, 2, "<", d1, d2):17} ]', file=self.logFile)
            self.mlimap[cc] = self.limap
        if dbg: tabs.Tabs.log(f'p={p} l={l} c={c} cc={cc}', file=self.logFile)
        self.limap.extend(self.limap1)  ;  self.limap1 = []
        self.limap.extend(self.limap2)  ;  self.limap2 = []
        if dbg:
            for i, m in enumerate(self.limap):
                tabs.Tabs.log(tabs.FMTR.format(f'limap   0 {i+1}  [ <{m[2]:<6}> {tabs.fmtl(m[0], 2, "<", d1, d2):17} {tabs.fmtl(m[1], 2, "<", d1, d2):17} ]'), file=self.logFile)
        return chordName

    def toggleChordName(self, rev=0):
        p, l, s, c, t = self.tobj.j()
        cc = c + l * self.tobj.n[tabs.C]
        if cc in self.mlimap.keys():
            limap = self.mlimap[cc]
            self.dumpLimap(limap, why=f'before len={len(limap)} p={p} l={l} c={c} cc={cc} rev={rev}')
            if rev: tmp0 = limap[-1]  ;   tmp1 = limap[:-1]  ;   limap  = tmp1   ;   limap.insert(0, tmp0)
            else:   tmp0 = limap[0]   ;   tmp1 = limap[1:]   ;   limap  = tmp1   ;   limap.append(tmp0)
            self.mlimap[cc] = limap
            self.dumpLimap(limap, why=f'after  len={len(limap)} p={p} l={l} c={c} cc={cc} rev={rev}')
            return limap[0][2]
   ####################################################################################################################################################################################################
    def getNotesIndices(self, p, l, c, dbg=VERBOSE, dbg2=0):
        mask = [1] * self.tobj.n[tabs.T]
        strNumbs   = self.tobj.stringNumbs
        strKeys    = self.tobj.stringKeys
        strNames   = self.tobj.stringNames
        _tabs      = self.tobj.data[p][l][c]
        strIndices = [Note.INDICES[k] for k in strKeys]
        notes = []  ;  nt = len(_tabs)  ;   mask2 = []
        if dbg2: tabs.Tabs.log(f'p={p} l={l} c={c} text={_tabs}', file=self.logFile)
        for t in range(nt):
            if tabs.Tabs.isFret(_tabs[t]): mask2.insert(0, 1)  ;  note = self.tobj.getNote(t, _tabs[t]).name  ;  notes.insert(0, note)
            else:                          mask2.insert(0, 0)
        indices = []
        for t in range(nt):
            index = int(self.tobj.getNote(t, _tabs[t]).index) if tabs.Tabs.isFret(_tabs[t]) else 0
            if index: indices.insert(0, index)
        if notes:
            if dbg2: self.dumpData(strNumbs,    mask, 'strNumbs', r=1)
            if dbg:  self.dumpData(strKeys,     mask, 'strKeys')
            if dbg:  self.dumpData(strIndices,  mask, 'strIndices')
            if dbg2: self.dumpData(strNames,    mask, 'strNames', r=1)
            if dbg:  self.dumpData(_tabs,       mask, 'Tabs',     r=1)
            if dbg:  self.dumpData(notes,      mask2, 'Notes')
            if dbg:  self.dumpData(indices,    mask2, 'Indices')
        return mask2, notes, indices

    def getIntervals(self, indices, j, mask, order=1, dbg=VERBOSE):
        deltas = []  ;  nst = Note.NUM_SEMI_TONES
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
        return intervals

    def getImapKeys(self, intervals, notes, mask, dbg=VERBOSE, dbg2=0):
        imap = collections.OrderedDict(sorted(dict(zip(intervals, notes)).items(), key=lambda t: self.INTERVAL_RANK[t[0]]))
        imapKeys  = list(imap.keys())
        imapNotes = list(imap.values())
        chordKey  = self.getChordKey(imapNotes)
        if dbg:  self.dumpData(imap,      mask, 'imap')
        if dbg2: self.dumpData(imapKeys,  mask, 'imapKeys')
        if dbg2: self.dumpData(imapNotes, mask, 'mapNotes')
#        if dbg: self.dumpData(list(chordKey), mask, 'chordKey')
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
    def dumpMLimap(self):
        for c, (k,v) in enumerate(self.mlimap.items()):
            tabs.Tabs.log(f'c={c} k={k} v={v}', file=self.logFile)

    def dumpLimap(self, limap, why):
        for imap in limap:
            self.dumpImap(imap, why)

    def dumpImap(self, imap, why):
        intervals = imap[0]  ;  imapNotes = imap[1]   ;   chordName = imap[2]   ;   d1, d2 = '<', '>'
        tabs.Tabs.log(f'{why}  [ <{chordName:<6}> {tabs.fmtl(intervals, 2, "<", d1, d2):17} {tabs.fmtl(imapNotes, 2, "<", d1, d2):17} ]', file=self.logFile)

    def dumpData(self, data, mask, why, w=5, u='<', r=0):
        lf = self.logFile
        if r:     data = data[::-1]  ;  mask = mask[::-1]
        j = 0   ;   dt = type(data)  ;  tabs.Tabs.log(f'{why:21} [ ', end='', file=lf)
        if dt is list or dt is str:
            for i in range(len(mask)):
                if mask[i]: tabs.Tabs.log('{:{}{}} '.format(data[j], u, w), ind=0, end='', file=lf)  ;  j += 1
                else:       tabs.Tabs.log('{:{}{}} '.format('-',     u, w), ind=0, end='', file=lf)
        elif dt is collections.OrderedDict:
            w2 = 2  ;   i = 0
            for k,v in data.items():
                while not mask[i]: tabs.Tabs.log('{:{}{}} '.format('-', u, w),    ind=0, end='', file=lf)  ;  i += 1
                tabs.Tabs.log('{:>{}}{}{:<{}} '.       format(k, w2, ':', v, w2), ind=0, end='', file=lf)  ;  i += 1
            while i < len(mask): tabs.Tabs.log('{:{}{}} '.  format('-', u, w),    ind=0, end='', file=lf)  ;  i += 1
        else: tabs.Tabs.log(f'type={dt} ', ind=0, end='', file=lf)
        tabs.Tabs.log(']',                 ind=0,         file=lf)
    ####################################################################################################################################################################################################
    @staticmethod
    def initChordNames():
         return {'R M3 5'    : '',
                 'R M3 5 7'  : 'M7',
                 'R M3 5 b7' : '7',
                 'R M3 5 6'  : '6',
                 'R m3 5'    : 'm',
                 'R m3 5 7'  : 'mM7',
                 'R m3 5 b7' : 'm7',
                 'R m3 b5'   : 'o',
                 'R m3 b5 b7': '07',
                 'R m3 b5 6' : 'o7',
                 'R M3 a5'   : '+',
                 'R m3 4 a5' : 'm4+',
                 'R 2 4 6'   : '6/9s4'
                 } # how to order/arrange/group?
    ####################################################################################################################################################################################################
    def _getChordName_B(self, imap):
        r = imap['R']
        key = self.getChordKey(imap.keys())
        return f'{r}{self.chordNames[key]}' if key in self.chordNames else ''
    ####################################################################################################################################################################################################
    def _getChordName_A(self, imap):
        r = imap['R']  ;  n = len(imap)
        if   '5' in imap:   return self.parse_5(imap, r, n)
        elif 'b5' in imap:  return self.parse_b5(imap, r, n)
        elif 'a5' in imap:  return self.parse_a5(imap, r, n)
        else:
            if   n == 3:
                if 'm3' in imap:
                    if   'b7' in imap: return f'{r}m7n'
                    elif  '7' in imap: return f'{r}mM7n'
                if 'M3' in imap:
                    if   'b7' in imap: return f'{r}7n'
                    elif  '7' in imap: return f'{r}M7n'
        return ''

    @staticmethod
    def parse_5(imap, r, n):
        if   n == 3:
            if 'm3' in imap: return f'{r}m'
            if 'M3' in imap: return f'{r}'
        elif n == 4:
            if 'm3' in imap:
                if   'b7' in imap: return f'{r}m7'
                elif  '7' in imap: return f'{r}mM7'
            if 'M3' in imap:
                if   'b7' in imap: return f'{r}7'
                elif  '7' in imap: return f'{r}M7'
                elif  '6' in imap: return f'{r}6'

    @staticmethod
    def parse_b5(imap, r, n):
        if   n == 3:
            if 'm3' in imap: return f'{r}o'
        elif n == 4:
            if 'm3' in imap:
                if   'b7' in imap: return f'{r}07'
                elif  '6' in imap: return f'{r}o7'

    @staticmethod
    def parse_a5(imap, r, n):
        if   n == 3:
            if 'M3' in imap: return f'{r}+'
