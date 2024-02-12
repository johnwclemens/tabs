from collections import Counter
from tpkg        import utl
from tpkg        import unic
from tpkg.notes  import Notes
from tpkg        import notes

F, N, S          = unic.F, unic.N, unic.S
W, Y, Z          = utl.W, utl.Y, utl.Z
slog, fmtl, fmtm = utl.slog, utl.fmtl, utl.fmtm

# aliasR = {'EADGBE': {'E2': 4, 'A2': 9, 'D3': 2, 'G3': 7, 'B3': 11, 'E4': 4}}
# aliasO = {'EADGBE': {'E2':24, 'A2':24, 'D3':36, 'G3':36, 'B3': 36, 'E4':48}}
# aliasA = {'EADGBE': {'E2':28, 'A2':33, 'D3':38, 'G3':43, 'B3': 47, 'E4':52}}

C0, C1, C2, C3, C4, C5, C6, C7, C8, C9, C10 = f'C0', f'C1', f'C2', f'C3', f'C4', f'C5', f'C6', f'C7', f'C8', f'C9', f'C10'
D0, D1, D2, D3, D4, D5, D6, D7, D8, D9, D10 = f'D0', f'D1', f'D2', f'D3', f'D4', f'D5', f'D6', f'D7', f'D8', f'D9', f'D10'
E0, E1, E2, E3, E4, E5, E6, E7, E8, E9, E10 = f'E0', f'E1', f'E2', f'E3', f'E4', f'E5', f'E6', f'E7', f'E8', f'E9', f'E10'
F0, F1, F2, F3, F4, F5, F6, F7, F8, F9, F10 = f'F0', f'F1', f'F2', f'F3', f'F4', f'F5', f'F6', f'F7', f'F8', f'F9', f'F10'
G0, G1, G2, G3, G4, G5, G6, G7, G8, G9, G10 = f'G0', f'G1', f'G2', f'G3', f'G4', f'G5', f'G6', f'G7', f'G8', f'G9', f'G10'
A0, A1, A2, A3, A4, A5, A6, A7, A8, A9, A10 = f'A0', f'A1', f'A2', f'A3', f'A4', f'A5', f'A6', f'A7', f'A8', f'A9', f'A10'
B0, B1, B2, B3, B4, B5, B6, B7, B8, B9, B10 = f'B0', f'B1', f'B2', f'B3', f'B4', f'B5', f'B6', f'B7', f'B8', f'B9', f'B10'

Cs0, Cs1, Cs2, Cs3, Cs4, Cs5, Cs6, Cs7, Cs8, Cs9, Cs10 = f'C♯0', f'C♯1', f'C♯2', f'C♯3', f'C♯4', f'C♯5', f'C♯6', f'C♯7', f'C♯8', f'C♯9', f'C♯10'
Ds0, Ds1, Ds2, Ds3, Ds4, Ds5, Ds6, Ds7, Ds8, Ds9, Ds10 = f'D♯0', f'D♯1', f'D♯2', f'D♯3', f'D♯4', f'D♯5', f'D♯6', f'D♯7', f'D♯8', f'D♯9', f'D♯10'
Es0, Es1, Es2, Es3, Es4, Es5, Es6, Es7, Es8, Es9, Es10 = f'E♯0', f'E♯1', f'E♯2', f'E♯3', f'E♯4', f'E♯5', f'E♯6', f'E♯7', f'E♯8', f'E♯9', f'E♯10'
Fs0, Fs1, Fs2, Fs3, Fs4, Fs5, Fs6, Fs7, Fs8, Fs9, Fs10 = f'F♯0', f'F♯1', f'F♯2', f'F♯3', f'F♯4', f'F♯5', f'F♯6', f'F♯7', f'F♯8', f'F♯9', f'F♯10'
Gs0, Gs1, Gs2, Gs3, Gs4, Gs5, Gs6, Gs7, Gs8, Gs9, Gs10 = f'G♯0', f'G♯1', f'G♯2', f'G♯3', f'G♯4', f'G♯5', f'G♯6', f'G♯7', f'G♯8', f'G♯9', f'G♯10'
As0, As1, As2, As3, As4, As5, As6, As7, As8, As9, As10 = f'A♯0', f'A♯1', f'A♯2', f'A♯3', f'A♯4', f'A♯5', f'A♯6', f'A♯7', f'A♯8', f'A♯9', f'A♯10'
Bs0, Bs1, Bs2, Bs3, Bs4, Bs5, Bs6, Bs7, Bs8, Bs9, Bs10 = f'B♯0', f'B♯1', f'B♯2', f'B♯3', f'B♯4', f'B♯5', f'B♯6', f'B♯7', f'B♯8', f'B♯9', f'B♯10'

Df0, Df1, Df2, Df3, Df4, Df5, Df6, Df7, Df8, Df9, Df10 = f'D♭0', f'D♭1', f'D♭2', f'D♭3', f'D♭4', f'D♭5', f'D♭6', f'D♭7', f'D♭8', f'D♭9', f'D♭10'
Ef0, Ef1, Ef2, Ef3, Ef4, Ef5, Ef6, Ef7, Ef8, Ef9, Ef10 = f'E♭0', f'E♭1', f'E♭2', f'E♭3', f'E♭4', f'E♭5', f'E♭6', f'E♭7', f'E♭8', f'E♭9', f'E♭10'
Ff0, Ff1, Ff2, Ff3, Ff4, Ff5, Ff6, Ff7, Ff8, Ff9, Ff10 = f'F♭0', f'F♭1', f'F♭2', f'F♭3', f'F♭4', f'F♭5', f'F♭6', f'F♭7', f'F♭8', f'F♭9', f'F♭10'
Gf0, Gf1, Gf2, Gf3, Gf4, Gf5, Gf6, Gf7, Gf8, Gf9, Gf10 = f'G♭0', f'G♭1', f'G♭2', f'G♭3', f'G♭4', f'G♭5', f'G♭6', f'G♭7', f'G♭8', f'G♭9', f'G♭10'
Af0, Af1, Af2, Af3, Af4, Af5, Af6, Af7, Af8, Af9, Af10 = f'A♭0', f'A♭1', f'A♭2', f'A♭3', f'A♭4', f'A♭5', f'A♭6', f'A♭7', f'A♭8', f'A♭9', f'A♭10'
Bf0, Bf1, Bf2, Bf3, Bf4, Bf5, Bf6, Bf7, Bf8, Bf9, Bf10 = f'B♭0', f'B♭1', f'B♭2', f'B♭3', f'B♭4', f'B♭5', f'B♭6', f'B♭7', f'B♭8', f'B♭9', f'B♭10'
Cf0, Cf1, Cf2, Cf3, Cf4, Cf5, Cf6, Cf7, Cf8, Cf9, Cf10 = f'C♭0', f'C♭1', f'C♭2', f'C♭3', f'C♭4', f'C♭5', f'C♭6', f'C♭7', f'C♭8', f'C♭9', f'C♭10'

class Strngs:
    def __init__(self, alias=None):
        if alias is None:     alias = 'EADGBE'
        self.aliases   = self._initAliases()
        self.map       = self.aliases[alias]
        self.keys      = list(self.map.keys())
        self.names     = Z.join(reversed([ str(k[:-1]) for k in           self.keys   ]))
        self.numbs     = Z.join(         [ str(r + 1)  for r in range(len(self.keys)) ])
        self.capo      = Z.join(         [ '0'         for _ in range(len(self.keys)) ])
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
        return dict([
            (self._initAlias('E A D G B E ', [E2,  A2,  D3,  G3,  B3,  E4 ])), # guitar 6 std
            (self._initAlias('D A D G B E ', [D2,  A2,  D3,  G3,  B3,  E4 ])), # guitar 6 drop_d
            (self._initAlias('E A D G C F ', [E2,  A2,  D3,  G3,  C4,  F4 ])), # guitar 6 4ths
            (self._initAlias('F C G D A E ', [F1,  C2,  G2,  D3,  A3,  E4 ])), # guitar 6 5ths
            (self._initAlias('A♭E♭B♭F C G ', [Af1, Ef2, Bf2, F3,  C4,  G4 ])), # guitar 6 5ths
            (self._initAlias('D A D G B E ', [D2,  A2,  D3,  G3,  B3,  E4 ])), # guitar 6 drop_D 
            (self._initAlias('D A D G A D ', [D2,  A2,  D3,  G3,  A3,  D4 ])), # guitar 6 dadgad
            (self._initAlias('C E G C E G ', [C2,  E2,  G2,  C3,  E3,  G3 ])), # guitar 6 english
            (self._initAlias('D A D E A D ', [D2,  A2,  D3,  E3,  A3,  D4 ])), # guitar 6 dadead
            (self._initAlias('E A C♯G B E ', [E2,  A2,  Cs3, G3,  B3,  E4 ])), # guitar 6 D=>C#
            (self._initAlias('E♯A♯D♯G♯B♯E♯', [Es2, As2, Ds3, Gs3, Bs3, Es4])), # guitar 6 std ♯
            (self._initAlias('E♭A♭D♭G♭B♭E♭', [Ef2, Af2, Df3, Gf3, Bf3, Ef4])), # guitar 6 std ♭
            (self._initAlias('E B E♭G♭B E♭', [E2,  B2,  Ef3, Gf3, B3,  Ef4])), # guitar 6 andy mckee
            ############################################################################################################################################################################################
            (self._initAlias('B E A D G B E ', [B1,  E2,  A2,  D3,  G3,  B3,  E4 ])), # guitar 7 std
            (self._initAlias('B E A D G C F ', [B1,  E2,  A2,  D3,  G3,  C4,  F4 ])), # guitar 7 4ths
            (self._initAlias('E G♯C E G♯C E ', [E2,  Gs2, C3,  E4,  Gs3, C4,  E4 ])), # guitar 7 3rds
            (self._initAlias('D G B D G B D ', [D2,  G2,  B2,  D3,  G3,  B3,  D4 ])), # guitar 7 russian
            ])
    @staticmethod
    def _initAlias(k, v):
        k = ''.join([ e for e in k if e!=' ' ])
        return  k, { e:Notes.n2ai(e) for e in v } 
    
    @staticmethod
    def tab2fn(t, dbg=0): fn = int(t) if '0'<=t<='9' else int(ord(t)-87) if 'a'<=t<='o' else None  ;  slog(f'tab={t} fretNum={fn}') if dbg else W  ;  return fn # todo
    @staticmethod
    def isFret(t):         return  1  if '0'<=t<='9'          or            'a'<=t<='o' else 0

    def nStrings(self): #   return len(self.names) # fixme don't count accidentals
        return len([ e for e in self.names if e not in notes.ACCD_TONES ])
        
    @staticmethod
    def nn2ni(name):       return notes.index(name, o=1)
        
    def fn2ni(self, fn, s, dbg=0):
#       strNum = self.nStrings() - s     # Reverse and one  base the string numbering: str[1 ... numStrings] => s[numStrings ... 1]
        strNum = self.nStrings() - s - 1 # Reverse and zero base the string numbering: str[1 ... numStrings] => s[(numStrings - 1) ... 0]
        assert strNum in range(0, self.nStrings()),  f'{strNum=} not in range(1, {self.nStrings()=} {s=})' # AssertionError: strNum=0 not in range(1, self.nStrings()=6)
        assert strNum in range(0, len(self.keys)),   f'{strNum=} not in range(0, {len(self.keys)=} {s=})'
        k      = self.keys[strNum] # todo
        assert k is not None and fn is not None,  f'{k=} {strNum=} {s=} {fn=}'
        assert k in self.map,  f'{k=} {strNum=} {s=} {fn=} {self.map=}'
        i      = self.map[k] + fn
        strNum += 1
        if dbg: slog(f'{fn=} {s=} {strNum=} {k=} {i=} map={fmtm(self.map)}')
        return i

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
