from collections import Counter
from tpkg        import utl    as utl
from tpkg        import unic   as unic
#from tpkg        import notes  as notes
from tpkg.notes  import Notes  as Notes
#from tpkg        import kysgs  as kysgs

F, N, S          = unic.F, unic.N, unic.S
W, Y, Z          = utl.W, utl.Y, utl.Z
slog, fmtl, fmtm = utl.slog, utl.fmtl, utl.fmtm

class Strngs:
    aliases = {'GUITAR_6_STD':    dict([('E2', 28), ('A2' , 33), ('D3', 38), ('G3', 43), ('B3' , 47), ('E4', 52)]),
               'GUITAR_6_DROP_D': dict([('D2', 26), ('A2' , 33), ('D3', 38), ('G3', 43), ('B3' , 47), ('E4', 52)]),
               'GUITAR_7_STD':    dict([('E2', 28), ('Ab2', 32), ('C3', 36), ('E3', 40), ('Ab3', 44), ('C4', 48), ('E4', 52)])
              }
    def __init__(self, alias=None):
        if alias is None: alias = 'GUITAR_6_STD'
        self.stringMap          = self.aliases[alias]
        self.stringKeys         = list(self.stringMap.keys())
        self.stringNames        = Z.join(reversed([ str(k[0])  for k in           self.stringKeys ]))
        self.stringNumbs        = Z.join(         [ str(r + 1) for r in range(len(self.stringKeys)) ])
        self.stringCapo         = Z.join(         [ '0'        for _ in range(len(self.stringKeys)) ])
        self.strLabel           = 'STRING'
        self.cpoLabel           = ' CAPO '
        slog( f'stringMap   = {fmtm(self.stringMap)}')
        slog( f'stringKeys  = {fmtl(self.stringKeys)}')
        slog( f'stringNames =      {self.stringNames}')
        slog( f'stringNumbs =      {self.stringNumbs}')
        slog( f'stringCapo  =      {self.stringCapo}')
        slog( f'strLabel    =      {self.strLabel}')
        slog( f'cpoLabel    =      {self.cpoLabel}')

    @staticmethod
    def tab2fn(t, dbg=0): fn = int(t) if '0'<=t<='9' else int(ord(t)-87) if 'a'<=t<='o' else None  ;  slog(f'tab={t} fretNum={fn}') if dbg else None  ;  return fn
    @staticmethod
    def isFret(t):      return   1    if '0'<=t<='9'          or            'a'<=t<='o' else 0

    def nStrings(self): return len(self.stringNames)

    def fn2ni(self, fn, s, dbg=0):
#        strNum = self.nStrings() - s   # Reverse and one base the string numbering: str[1 ... numStrings] => s[numStrings ... 1]
        strNum = self.nStrings() - s - 1   # Reverse and zero base the string numbering: str[1 ... numStrings] => s[(numStrings - 1) ... 0]
        k      = self.stringKeys[strNum]
        i      = self.stringMap[k] + fn
        strNum += 1
        if dbg: slog(f'{fn=} {s=} {strNum=} {k=} {i=} stringMap={fmtm(self.stringMap)}')
        return i

    def tab2nn(self, tab, s, nic=None, dbg=1, f=-2):
        fn  = self.tab2fn(tab)
        i   = self.fn2ni(fn, s)   ;   nict = Z
        j   = i % Notes.NTONES
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
        name = Notes.name(i, 1, 1)
        if dbg and nict:        slog(f'{tab=} {fn=:2} {s=} {i=:2} {j=:x} {name=:2} {nict}{fmtm(nic, w="x")}', f=f)
        return name
