from collections import Counter
from tpkg        import utl
from tpkg        import unic
from tpkg.notes  import Notes
from tpkg        import notes

F, N, S          = unic.F, unic.N, unic.S
W, Y, Z          = utl.W, utl.Y, utl.Z
slog, fmtl, fmtm = utl.slog, utl.fmtl, utl.fmtm

E2, A2, D3, G3, B3, E4 = f'E2', f'A2', f'D3', f'G3', f'B3', f'E4' 
C4, F4                 = f'C4', f'F4'

class Strngs:
    aliases_ = {f'EADGBE':             dict([(f'E2',    28), (f'A2',    33), (f'D3',    38), (f'G3',    43), (f'B3',    47), (f'E4',    52)]),
                f'guitar':             dict([(f'E2',    28), (f'A2',    33), (f'D3',    38), (f'G3',    43), (f'B3',    47), (f'E4',    52)]),
                f'english':            dict([(f'C2',    24), (f'E2',    28), (f'G3',    31), (f'C3',    36), (f'E3',    40), (f'G4',    43)]),
                f'drop_D':             dict([(f'D2',    26), (f'A2',    33), (f'D3',    38), (f'G3',    43), (f'B3',    47), (f'E4',    52)]),
                f'DADEAD':             dict([(f'D2',    26), (f'A2',    33), (f'D3',    38), (f'E3',    40), (f'A3',    45), (f'D4',    50)]),
                f'DAEAC{S}E':          dict([(f'D2',    26), (f'A2',    33), (f'E3',    40), (f'A3',    45), (f'C{S}4', 49), (f'E4',    52)]),
                f'DADGBE':             dict([(f'D2',    26), (f'A2',    33), (f'D3',    38), (f'G3',    43), (f'B3',    47), (f'E4',    52)]),
                f'DADGAD':             dict([(f'D2',    26), (f'A2',    33), (f'D3',    38), (f'G3',    40), (f'A3',    45), (f'D4',    50)]),
                f'guitar_6_4ths':      dict([(f'E2',    28), (f'A2',    33), (f'D3',    38), (f'G3',    43), (f'C4',    48), (f'F4',    53)]),
                f'E{F}ADGBE':          dict([(f'E{F}2', 27), (f'A2',    33), (f'D3',    38), (f'G3',    43), (f'B3',    47), (f'E4',    52)]),
                f'EBE{F}G{F}BE{F}':    dict([(f'E2',    28), (f'B2',    35), (f'E{F}3', 39), (f'G{F}3', 42), (f'B3',    47), (f'E{F}4', 51)]),
                f'E{F}BE{F}G{F}BE{F}': dict([(f'E{F}2', 27), (f'B2',    35), (f'E{F}3', 39), (f'G{F}3', 42), (f'B3',    47), (f'E{F}4', 51)]),
    ####################################################################################################################################################################################################
                f'guitar_7_4ths':      dict([(f'E2',    28), (f'A{F}2', 32), (f'C3',    36), (f'E3',    40), (f'A{F}3', 44), (f'C4',    48), (f'E4',    52)]),
                f'EA{F}CEA{F}CE':      dict([(f'E2',    28), (f'A{F}2', 32), (f'C3',    36), (f'E3',    40), (f'A{F}3', 44), (f'C4',    48), (f'E4',    52)]),
                f'guitar_7':           dict([(f'B1',    23), (f'E2',    28), (f'A2',    33), (f'D3',    38), (f'G3',    43), (f'B3',    47), (f'E4',    52)]),
                f'DGBDGBD':            dict([(f'D2',    26), (f'G2',    31), (f'B2',    35), (f'D3',    38), (f'G3',    43), (f'B3',    47), (f'D4',    50)]),
                f'guitar_russian':     dict([(f'D2',    26), (f'G2',    31), (f'B2',    35), (f'D3',    38), (f'G3',    43), (f'B3',    47), (f'D4',    50)]),
                f'guitar_7_drop_C':    dict([(f'C2',    24), (f'E2',    28), (f'A2',    33), (f'D3',    38), (f'G3',    43), (f'B3',    47), (f'E4',    52)]),
                f'guitar_7_drop_B':    dict([(f'B1',    23), (f'E2',    28), (f'A2',    33), (f'D3',    38), (f'G3',    43), (f'B3',    47), (f'E4',    52)]),
                f'guitar_7_drop_A':    dict([(f'A1',    21), (f'E2',    28), (f'A2',    33), (f'D3',    38), (f'G3',    43), (f'B3',    47), (f'E4',    52)]),
                f'CEADGBE':            dict([(f'C2',    24), (f'E2',    28), (f'A2',    33), (f'D3',    38), (f'G3',    43), (f'B3',    47), (f'E4',    52)]),
                f'BEADGBE':            dict([(f'B1',    23), (f'E2',    28), (f'A2',    33), (f'D3',    38), (f'G3',    43), (f'B3',    47), (f'E4',    52)]),
                f'AEADGBE':            dict([(f'A1',    21), (f'E2',    28), (f'A2',    33), (f'D3',    38), (f'G3',    43), (f'B3',    47), (f'E4',    52)])
              } # todo fixme this can easily have typos/incorrect values for the indices - refactor/simplify - revisit keys/aliases
#   alias=             {'E2': 4, 'A2': 9, 'D3': 2, 'G3': 7, 'B3': 11, 'E4': 4} .
#   alias = {'EADGBE': {'E2':24, 'A2':24, 'D3':36, 'G3':36, 'B3': 36, 'E4':48}}
#                      {'E2':28, 'A2':33, 'D3':38, 'G3':43, 'B3': 47, 'E4':52}
#    @staticmethod
#    def aliases(a):
#        return { e:Notes.n2ai(e) for e in a }

#    alists   = {
#               f'EADGBE': aliases([E2, A2, D3, G3, B3, E4]),
#               f'EADGCF': aliases([E2, A2, D3, G3, C4, F4])
#               }
#    aliases2 = {
#               f'EADGBE': dict([(E2, Notes.n2ai(E2)), (A2, Notes.n2ai(A2)), (D3, Notes.n2ai(D3)), (G3, Notes.n2ai(G3)), (B3, Notes.n2ai(B3)), (E4, Notes.n2ai(E4))]),
#               f'EADGCF': dict([(E2, Notes.n2ai(E2)), (A2, Notes.n2ai(A2)), (D3, Notes.n2ai(D3)), (G3, Notes.n2ai(G3)), (C4, Notes.n2ai(C4)), (F4, Notes.n2ai(F4))])
#               }
        
    def __init__(self, alias=None):
        if alias is None:     alias = 'GUITAR'
#        self.map       =  self.alists[alias]
#        self.keys      = list(self.alists.keys())
#        slog(f'{Notes.n2ipo(E2)} {Notes.n2ipo(A2)} {Notes.n2ipo(D3)} {Notes.n2ipo(G3)} {Notes.n2ipo(B3)} {Notes.n2ipo(E4)}')
#        alias          = self.alias[alias]  # new code prototype
#        slog(f'{alias=} {self.alias=}')     # new code prototype
        self.aliases   = self._initAliases()
        self.map       = self.aliases[alias]
        self.keys      = list(self.map.keys())
        self.names     = Z.join(reversed([ str(k[0])  for k in           self.keys ]))
        self.numbs     = Z.join(         [ str(r + 1) for r in range(len(self.keys)) ])
        self.capo      = Z.join(         [ '0'        for _ in range(len(self.keys)) ])
        self.label     = 'STRING'
        self.labelc    = ' CAPO '
        slog(f'map     = {fmtm(self.map)}')
        slog(f'keys    = {fmtl(self.keys)}')
        slog(f'names   =      {self.names}')
        slog(f'numbs   =      {self.numbs}')
        slog(f'capo    =      {self.capo}')
        slog(f'label   =      {self.label}')
        slog(f'labelc  =      {self.labelc}')

    def _initAliases(self):
        return { f'EADGBE': self._initAlias([E2, A2, D3, G3, B3, E4]),
                 f'EADGCF': self._initAlias([E2, A2, D3, G3, C4, F4])}
    @staticmethod
    def _initAlias(a):
        return { e:Notes.n2ai(e) for e in a }
    
    @staticmethod
    def tab2fn(t, dbg=0): fn = int(t) if '0'<=t<='9' else int(ord(t)-87) if 'a'<=t<='o' else None  ;  slog(f'tab={t} fretNum={fn}') if dbg else W  ;  return fn # todo
    @staticmethod
    def isFret(t):         return  1  if '0'<=t<='9'          or            'a'<=t<='o' else 0

    def nStrings(self):    return len(self.names)

    @staticmethod
    def nn2ni(name):       return notes.index(name, o=1)
        
    def fn2ni(self, fn, s, dbg=0):
#       strNum = self.nStrings() - s     # Reverse and one  base the string numbering: str[1 ... numStrings] => s[numStrings ... 1]
        strNum = self.nStrings() - s - 1 # Reverse and zero base the string numbering: str[1 ... numStrings] => s[(numStrings - 1) ... 0]
#        assert strNum in range(1, self.nStrings()),  f'{strNum=} not in range(1, {self.nStrings()=} {s=})' # AssertionError: strNum=0 not in range(1, self.nStrings()=6)
        k      = self.keys[strNum] # todo
        assert k is not None and fn is not None,  f'{k=} {strNum=} {s=} {fn=}'
        assert k in self.map,  f'{k=} {strNum=} {s=} {fn=} {self.map=}'
        i      = self.map[k] + fn
        strNum += 1
        if dbg: slog(f'{fn=} {s=} {strNum=} {k=} {i=} map={fmtm(self.map)}')
        return i

#    def tab2ni(self, tab, s):
#        assert tab is not None,  f'{tab=} {s=}'
#        fn  = self.tab2fn(tab)
#        assert fn  is not None,  f'{fn=} {tab=} {s=}'
#        return self.fn2ni(fn, s)

    def tab2nn(self, tab, s, t=None, nic=None, dbg=1, f=-3):
        assert tab is not None,  f'{tab=} {s=} {t=} {nic=}'
        fn  = self.tab2fn(tab)
        assert fn  is not None,  f'{fn=} {tab=} {s=} {t=} {nic=}'
        i   = self.fn2ni(fn, s)   ;   nict = Z
        j   = i % Notes.NTONES
        if   t  is None:                 t = Notes.TYPE
        if  nic is None:               nic = Counter() # dict(key:int, val:int) kysgs.py: 0-11 vals: count
        else:
            nic[j]    += 1
            if nic[j] == 1:
#                if j in (0, 4, 5, 11):
#                    k  = kysgs.KSK
#                    if abs(k) > 5:
                        # if dbg: slog(f'KSK[{k}]={kysgs.fmtKSK(k)}', f=f)
                        # if   j == 11: notes.updNotes(j, f'C{F}', 'B', Notes.TYPE, 0)
                        # if   j ==  5: notes.updNotes(j, 'F', f'E{S}', Notes.TYPE, 0)
                        # elif j ==  4: notes.updNotes(j, f'F{F}', 'E', Notes.TYPE, 0)
                        # elif j ==  0: notes.updNotes(j, 'C', f'B{S}', Notes.TYPE, 0)
#                       if   j == 11: Notes.updNotes(j, 'Cb', 'B',   NotesA.TYPE, 0)
#                       if   j ==  5: Notes.updNotes(j, 'F',  'E#',  NotesA.TYPE, 0)
#                       elif j ==  4: Notes.updNotes(j, 'Fb', 'E',   NotesA.TYPE, 0)
#                       elif j ==  0: Notes.updNotes(j, 'C',  'B#',  NotesA.TYPE, 0)
                if dbg and nict: nict = f'nic[{j:x}]={nic[j]} '  ;   slog(f'adding {nict}', f=f)
        name = Notes.name(i, t, 1) # do not hard code t=1 get note type (sharp/flat)
        if dbg and nict:        slog(f'{tab=} {fn=:2} {s=} {i=:2} {j=:x} {name=:2} {nict}{fmtm(nic, w="x")}', f=f)
        return name
