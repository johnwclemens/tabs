from collections import Counter
from tpkg        import utl
from tpkg        import unic
from tpkg.notes  import Notes
from tpkg        import notes

F, N, S          = unic.F, unic.N, unic.S
W, Y, Z          = utl.W, utl.Y, utl.Z
slog, fmtl, fmtm = utl.slog, utl.fmtl, utl.fmtm

# rel = {'EADGBE': {'E2': 4, 'A2': 9, 'D3': 2, 'G3': 7, 'B3': 11, 'E4': 4}}
# off = {'EADGBE': {'E2':24, 'A2':24, 'D3':36, 'G3':36, 'B3': 36, 'E4':48}}
# abs = {'EADGBE': {'E2':28, 'A2':33, 'D3':38, 'G3':43, 'B3': 47, 'E4':52}}

#C_0, C_1, C_2, C_3, C_4, C_5, C_6, C_7, C_8, C_9, C_10 = 'C_0', 'C_1', 'C_2', 'C_3', 'C_4', 'C_5', 'C_6', 'C_7', 'C_8', 'C_9', 'C_10'
#D_0, D_1, D_2, D_3, D_4, D_5, D_6, D_7, D_8, D_9, D_10 = 'D_0', 'D_1', 'D_2', 'D_3', 'D_4', 'D_5', 'D_6', 'D_7', 'D_8', 'D_9', 'D_10'
#E_0, E_1, E_2, E_3, E_4, E_5, E_6, E_7, E_8, E_9, E_10 = 'E_0', 'E_1', 'E_2', 'E_3', 'E_4', 'E_5', 'E_6', 'E_7', 'E_8', 'E_9', 'E_10'
#F_0, F_1, F_2, F_3, F_4, F_5, F_6, F_7, F_8, F_9, F_10 = 'F_0', 'F_1', 'F_2', 'F_3', 'F_4', 'F_5', 'F_6', 'F_7', 'F_8', 'F_9', 'F_10'
#G_0, G_1, G_2, G_3, G_4, G_5, G_6, G_7, G_8, G_9, G_10 = 'G_0', 'G_1', 'G_2', 'G_3', 'G_4', 'G_5', 'G_6', 'G_7', 'G_8', 'G_9', 'G_10'
#A_0, A_1, A_2, A_3, A_4, A_5, A_6, A_7, A_8, A_9, A_10 = 'A_0', 'A_1', 'A_2', 'A_3', 'A_4', 'A_5', 'A_6', 'A_7', 'A_8', 'A_9', 'A_10'
#B_0, B_1, B_2, B_3, B_4, B_5, B_6, B_7, B_8, B_9, B_10 = 'B_0', 'B_1', 'B_2', 'B_3', 'B_4', 'B_5', 'B_6', 'B_7', 'B_8', 'B_9', 'B_10'

C_0, C_1, C_2, C_3, C_4, C_5, C_6, C_7, C_8, C_9, C_10 = 'C 0', 'C 1', 'C 2', 'C 3', 'C 4', 'C 5', 'C 6', 'C 7', 'C 8', 'C 9', 'C 10'
D_0, D_1, D_2, D_3, D_4, D_5, D_6, D_7, D_8, D_9, D_10 = 'D 0', 'D 1', 'D 2', 'D 3', 'D 4', 'D 5', 'D 6', 'D 7', 'D 8', 'D 9', 'D 10'
E_0, E_1, E_2, E_3, E_4, E_5, E_6, E_7, E_8, E_9, E_10 = 'E 0', 'E 1', 'E 2', 'E 3', 'E 4', 'E 5', 'E 6', 'E 7', 'E 8', 'E 9', 'E 10'
F_0, F_1, F_2, F_3, F_4, F_5, F_6, F_7, F_8, F_9, F_10 = 'F 0', 'F 1', 'F 2', 'F 3', 'F 4', 'F 5', 'F 6', 'F 7', 'F 8', 'F 9', 'F 10'
G_0, G_1, G_2, G_3, G_4, G_5, G_6, G_7, G_8, G_9, G_10 = 'G 0', 'G 1', 'G 2', 'G 3', 'G 4', 'G 5', 'G 6', 'G 7', 'G 8', 'G 9', 'G 10'
A_0, A_1, A_2, A_3, A_4, A_5, A_6, A_7, A_8, A_9, A_10 = 'A 0', 'A 1', 'A 2', 'A 3', 'A 4', 'A 5', 'A 6', 'A 7', 'A 8', 'A 9', 'A 10'
B_0, B_1, B_2, B_3, B_4, B_5, B_6, B_7, B_8, B_9, B_10 = 'B 0', 'B 1', 'B 2', 'B 3', 'B 4', 'B 5', 'B 6', 'B 7', 'B 8', 'B 9', 'B 10'

Cs0, Cs1, Cs2, Cs3, Cs4, Cs5, Cs6, Cs7, Cs8, Cs9, Cs10 = 'C♯0', 'C♯1', 'C♯2', 'C♯3', 'C♯4', 'C♯5', 'C♯6', 'C♯7', 'C♯8', 'C♯9', 'C♯10'
Ds0, Ds1, Ds2, Ds3, Ds4, Ds5, Ds6, Ds7, Ds8, Ds9, Ds10 = 'D♯0', 'D♯1', 'D♯2', 'D♯3', 'D♯4', 'D♯5', 'D♯6', 'D♯7', 'D♯8', 'D♯9', 'D♯10'
Es0, Es1, Es2, Es3, Es4, Es5, Es6, Es7, Es8, Es9, Es10 = 'E♯0', 'E♯1', 'E♯2', 'E♯3', 'E♯4', 'E♯5', 'E♯6', 'E♯7', 'E♯8', 'E♯9', 'E♯10'
Fs0, Fs1, Fs2, Fs3, Fs4, Fs5, Fs6, Fs7, Fs8, Fs9, Fs10 = 'F♯0', 'F♯1', 'F♯2', 'F♯3', 'F♯4', 'F♯5', 'F♯6', 'F♯7', 'F♯8', 'F♯9', 'F♯10'
Gs0, Gs1, Gs2, Gs3, Gs4, Gs5, Gs6, Gs7, Gs8, Gs9, Gs10 = 'G♯0', 'G♯1', 'G♯2', 'G♯3', 'G♯4', 'G♯5', 'G♯6', 'G♯7', 'G♯8', 'G♯9', 'G♯10'
As0, As1, As2, As3, As4, As5, As6, As7, As8, As9, As10 = 'A♯0', 'A♯1', 'A♯2', 'A♯3', 'A♯4', 'A♯5', 'A♯6', 'A♯7', 'A♯8', 'A♯9', 'A♯10'
Bs0, Bs1, Bs2, Bs3, Bs4, Bs5, Bs6, Bs7, Bs8, Bs9, Bs10 = 'B♯0', 'B♯1', 'B♯2', 'B♯3', 'B♯4', 'B♯5', 'B♯6', 'B♯7', 'B♯8', 'B♯9', 'B♯10'

Df0, Df1, Df2, Df3, Df4, Df5, Df6, Df7, Df8, Df9, Df10 = 'D♭0', 'D♭1', 'D♭2', 'D♭3', 'D♭4', 'D♭5', 'D♭6', 'D♭7', 'D♭8', 'D♭9', 'D♭10'
Ef0, Ef1, Ef2, Ef3, Ef4, Ef5, Ef6, Ef7, Ef8, Ef9, Ef10 = 'E♭0', 'E♭1', 'E♭2', 'E♭3', 'E♭4', 'E♭5', 'E♭6', 'E♭7', 'E♭8', 'E♭9', 'E♭10'
Ff0, Ff1, Ff2, Ff3, Ff4, Ff5, Ff6, Ff7, Ff8, Ff9, Ff10 = 'F♭0', 'F♭1', 'F♭2', 'F♭3', 'F♭4', 'F♭5', 'F♭6', 'F♭7', 'F♭8', 'F♭9', 'F♭10'
Gf0, Gf1, Gf2, Gf3, Gf4, Gf5, Gf6, Gf7, Gf8, Gf9, Gf10 = 'G♭0', 'G♭1', 'G♭2', 'G♭3', 'G♭4', 'G♭5', 'G♭6', 'G♭7', 'G♭8', 'G♭9', 'G♭10'
Af0, Af1, Af2, Af3, Af4, Af5, Af6, Af7, Af8, Af9, Af10 = 'A♭0', 'A♭1', 'A♭2', 'A♭3', 'A♭4', 'A♭5', 'A♭6', 'A♭7', 'A♭8', 'A♭9', 'A♭10'
Bf0, Bf1, Bf2, Bf3, Bf4, Bf5, Bf6, Bf7, Bf8, Bf9, Bf10 = 'B♭0', 'B♭1', 'B♭2', 'B♭3', 'B♭4', 'B♭5', 'B♭6', 'B♭7', 'B♭8', 'B♭9', 'B♭10'
Cf0, Cf1, Cf2, Cf3, Cf4, Cf5, Cf6, Cf7, Cf8, Cf9, Cf10 = 'C♭0', 'C♭1', 'C♭2', 'C♭3', 'C♭4', 'C♭5', 'C♭6', 'C♭7', 'C♭8', 'C♭9', 'C♭10'

def filtA(v, a='_'): return Z.join([ e for e in v if e not in (W, a) ])
def filtB(v, a='_'): return Z.join([ e for e in v if e!=a ])

class Strngs:
    def __init__(self, alias=None, dbg=1):
        if alias is None:  alias = 'EADGBE'
        self.aliases      = self._initAliases()
        if dbg:             self.dumpAliases()
        self.map          = self.aliases[alias]
        self.keys         = list(self.map.keys())
        names             = list(reversed([ str(k[:-1]) for k in           self.keys   ]))
        numbs             =               [ str(r + 1)  for r in range(len(self.keys)) ]
        self.names        = Z.join(names)
        self.names2       = W.join(names) + W
        self.numbs        = Z.join(numbs)
        self.numbs2       = W.join(numbs) + W
        self.capo         = Z.join([ '0' for _ in range(len(self.keys)) ])
        self.label        = 'STRING'
        self.labelc       = ' CAPO '
        slog(f'map        = {fmtm(self.map)}')
        slog(f'keys       = {fmtl(self.keys)}')
        slog(f"names      =     '{Z.join(names)}'")
        slog(f"names2     =     '{self.names2}'")
        slog(f"numbs2     =     '{self.numbs2}'")
        slog(f"names      =     '{self.names}'")
        slog(f"numbs      =     '{self.numbs}'")
        slog(f'capo       =      {self.capo}')
        slog(f'label      =      {self.label}')
        slog(f'labelc     =      {self.labelc}')

    def _initAliases(self):
        return dict([
            (self._initAlias('E A D G B E ',   [E_2, A_2, D_3, G_3, B_3, E_4])),      # guitar 6 std
            (self._initAlias('D A D G B E ',   [D_2, A_2, D_3, G_3, B_3, E_4])),      # guitar 6 drop_d
            (self._initAlias('E A D G C F ',   [E_2, A_2, D_3, G_3, C_4, F_4])),      # guitar 6 4ths
            (self._initAlias('F C G D A E ',   [F_1, C_2, G_2, D_3, A_3, E_4])),      # guitar 6 5ths
            (self._initAlias('A♭E♭B♭F C G ',   [Af1, Ef2, Bf2, F_3, C_4, G_4])),      # guitar 6 5ths
            (self._initAlias('D A D G B E ',   [D_2, A_2, D_3, G_3, B_3, E_4])),      # guitar 6 drop_D 
            (self._initAlias('D A D G A D ',   [D_2, A_2, D_3, G_3, A_3, D_4])),      # guitar 6 dadgad
            (self._initAlias('C E G C E G ',   [C_2, E_2, G_2, C_3, E_3, G_3])),      # guitar 6 english
            (self._initAlias('D A D E A D ',   [D_2, A_2, D_3, E_3, A_3, D_4])),      # guitar 6 dadead
            (self._initAlias('E A C♯G B E ',   [E_2, A_2, Cs3, G_3, B_3, E_4])),      # guitar 6 D=>C#
            (self._initAlias('E♯A♯D♯G♯B♯E♯',   [Es2, As2, Ds3, Gs3, Bs3, Es4])),      # guitar 6 std ♯
            (self._initAlias('E♭A♭D♭G♭B♭E♭',   [Ef2, Af2, Df3, Gf3, Bf3, Ef4])),      # guitar 6 std ♭
            (self._initAlias('E B E♭G♭B E♭',   [E_2, B_2, Ef3, Gf3, B_3, Ef4])),      # guitar 6 andy mckee
            ############################################################################################################################################################################################
            (self._initAlias('B E A D G B E ', [B_1, E_2, A_2, D_3, G_3, B_3, E_4])), # guitar 7 std
            (self._initAlias('B E A D G C F ', [B_1, E_2, A_2, D_3, G_3, C_4, F_4])), # guitar 7 4ths
            (self._initAlias('E G♯C E G♯C E ', [E_2, Gs2, C_3, E_3, Gs3, C_4, E_4])), # guitar 7 3rds
            (self._initAlias('D G B D G B D ', [D_2, G_2, B_2, D_3, G_3, B_3, D_4])), # guitar 7 russian
            ])
    @staticmethod
    def _initAlias(k, v):
        k2 =   filtB(k)
#        v2 = [ filtB(e) for e in v ]
        return  k2, { e:Notes.n2ai(e) for e in v } 
    
    def dumpAliases(self):
        s = self.aliases
#        slog(f'{s}',       p=0)
#        slog(f'{fmtm(s)}', p=0)
        a, f, w = '>', W, 2*7
#        for k, v in s.items():
#            slog(f'{k:{f}{a}{w}}: {fmtm(v, d=Z, s=Y+W)}', p=0)
#        slog(p=0)
        for k, v in s.items():
            k = f'{k:{f}{a}{w}}'   ;   v3 = []
            for k2, v2 in v.items():
                v3.append(f'{v2} {k2}')
            slog(f'{k} :  {fmtl(v3, d=Z, s=Y+2*W)}', p=0)
        
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


#   E  A  D  G  B  E  :  28 E  2   33 A  2   38 D  3   43 G  3   47 B  3   52 E  4
#   D  A  D  G  B  E  :  26 D  2   33 A  2   38 D  3   43 G  3   47 B  3   52 E  4
#   E  A  D  G  C  F  :  28 E  2   33 A  2   38 D  3   43 G  3   48 C  4   53 F  4
#   F  C  G  D  A  E  :  17 F  1   24 C  2   31 G  2   38 D  3   45 A  3   52 E  4
#   A♭ E♭ B♭ F  C  G  :  20 A♭ 1   27 E♭ 2   34 B♭ 2   41 F  3   48 C  4   55 G  4
#   D  A  D  G  A  D  :  26 D  2   33 A  2   38 D  3   43 G  3   45 A  3   50 D  4
#   C  E  G  C  E  G  :  24 C  2   28 E  2   31 G  2   36 C  3   40 E  3   43 G  3
#   D  A  D  E  A  D  :  26 D  2   33 A  2   38 D  3   40 E  3   45 A  3   50 D  4
#   E  A  C♯ G  B  E  :  28 E  2   33 A  2   37 C♯ 3   43 G  3   47 B  3   52 E  4
#   E♯ A♯ D♯ G♯ B♯ E♯ :  29 E♯ 2   34 A♯ 2   39 D♯ 3   44 G♯ 3   36 B♯ 3   53 E♯ 4
#   E♭ A♭ D♭ G♭ B♭ E♭ :  27 E♭ 2   32 A♭ 2   37 D♭ 3   42 G♭ 3   46 B♭ 3   51 E♭ 4
#   E  B  E♭ G♭ B  E♭ :  28 E  2   35 B  2   39 E♭ 3   42 G♭ 3   47 B  3   51 E♭ 4
#B  E  A  D  G  B  E  :  23 B  1   28 E  2   33 A  2   38 D  3   43 G  3   47 B  3   52 E  4
#B  E  A  D  G  C  F  :  23 B  1   28 E  2   33 A  2   38 D  3   43 G  3   48 C  4   53 F  4
#E  G♯ C  E  G♯ C  E  :  28 E  2   32 G♯ 2   36 C  3   40 E  3   44 G♯ 3   48 C  4   52 E  4
#D  G  B  D  G  B  D  :  26 D  2   31 G  2   35 B  2   38 D  3   43 G  3   47 B  3   50 D  4
