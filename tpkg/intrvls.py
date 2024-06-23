from tpkg       import utl
from tpkg       import unic
from tpkg       import notes
from tpkg.notes import Notes
from collections import Counter
import math

F,    N,    S,    E,    X   = unic.F,   unic.N,   unic.S,   unic.E,   unic.X
W,    Y,    Z,    slog, ist = utl.W,    utl.Y,    utl.Z,    utl.slog, utl.ist
fmtl, fmtm, fmtf, fmtg      = utl.fmtl, utl.fmtm, utl.fmtf, utl.fmtg

NONE, SUPERS,   MAX_FREQ_IDX, ACCD_TONES = utl.NONE, utl.SPRSCRPT_INTS, utl.MAX_FREQ_IDX, notes.ACCD_TONES
NT,   A4_INDEX, CM_P_M,       V_SOUND    = notes.NT, notes.A4_INDEX,    notes.CM_P_M,     notes.V_SOUND

FLATS, SHRPS  = notes.FLATS, notes.SHRPS
F440s, F432s  = notes.F440s, notes.F432s
#        0    1    2     3     4     5     6     7     8     9      10     11     12
#COFS = ['C', 'G', 'D',  'A',  'E',  'B',  'F♯', 'C♯', 'G♯', 'D♯',  'A♯',  'E#',  'B#']
#COFF = ['C', 'F', 'B♭', 'E♭', 'A♭', 'D♭', 'G♭', 'C♭', 'F♭', 'B♭♭', 'E♭♭', 'A♭♭', 'D♭♭', 'G♭♭', 'C♭♭', 'F♭♭', 'B♭♭♭']
########################################################################################################################################################################################################
'''
#       -28      -27      -26      -25      -24     -23       -22      0       +22      +23      +24      +25      +26      +27      +28
#       -21      -20      -19      -18      -17     -16       -15      0       +15      +16      +17      +18      +19      +20      +21
#       -14      -13      -12      -11      -10      -9       -8       0       +8       +9       +10      +11      +12      +13      +14
#       -7       -6       -5       -4       -3       -2       -1       0       +1       +2       +3       +4       +5       +6       +7
COF = ['C♭♭♭♭', 'G♭♭♭♭', 'D♭♭♭♭', 'A♭♭♭♭', 'E♭♭♭♭', 'B♭♭♭♭', 'F♭♭♭',
       'C♭♭♭',  'G♭♭♭',  'D♭♭♭',  'A♭♭♭',  'E♭♭♭',  'B♭♭♭',  'F♭♭',
       'C♭♭',   'G♭♭',   'D♭♭',   'A♭♭',   'E♭♭',   'B♭♭',   'F♭',
       'C♭',    'G♭',    'D♭',    'A♭',    'E♭',    'B♭',    'F',     'C',    'G',     'D',     'A',     'E',     'B',     'F♯',    'C♯',
                                                                              'G♯',    'D♯',    'A♯',    'E♯',    'B♯',    'F♯♯',   'C♯♯',
                                                                              'G♯♯',   'D♯♯',   'A♯♯',   'E♯♯',   'B♯♯',   'F♯♯♯',  'C♯♯♯',
                                                                              'G♯♯♯',  'D♯♯♯',  'A♯♯♯',  'E♯♯♯',  'B♯♯♯',  'F♯♯♯♯', 'C♯♯♯♯']
#       -7       -6       -5       -4       -3       -2       -1       0       +1       +2       +3       +4       +5       +6       +7
#       -14      -13      -12      -11      -10      -9       -8       0       +8       +9       +10      +11      +12      +13      +14
#       -21      -20      -19      -18      -17     -16       -15      0       +15      +16      +17      +18      +19      +20      +21
#       -28      -27      -26      -25      -24     -23       -22      0       +22      +23      +24      +25      +26      +27      +28
########################################################################################################################################################################################################
#       -28      -27      -26      -25      -24      -23      -22     -21     -20     -19     -18     -17    -16      -15      0     +15    +16    +17    +18    +19    +20     +21     +22     +23     +24     +25     +26     +27      +28
#       -14      -13      -12      -11      -10      -9       -8      -7      -6      -5      -4      -3      -2      -1       0     +1     +2     +3     +4     +5     +6      +7      +8      +9      +10     +11     +12     +13      +14
C2F = ['C♭♭♭♭', 'G♭♭♭♭', 'D♭♭♭♭', 'A♭♭♭♭', 'E♭♭♭♭', 'B♭♭♭♭', 'F♭♭♭', 'C♭♭♭', 'G♭♭♭', 'D♭♭♭', 'A♭♭♭', 'E♭♭♭', 'B♭♭♭', 'F♭♭',
       'C♭♭',   'G♭♭',   'D♭♭',   'A♭♭',   'E♭♭',   'B♭♭',   'F♭',   'C♭',   'G♭',   'D♭',   'A♭',   'E♭',   'B♭',   'F',    'C',   'G',   'D',   'A',   'E',   'B',   'F♯',   'C♯',   'G♯',   'D♯',   'A♯',   'E♯',   'B♯',   'F♯♯',   'C♯♯',
                                                                                                                                    'G♯♯', 'D♯♯', 'A♯♯', 'E♯♯', 'B♯♯', 'F♯♯♯', 'C♯♯♯', 'G♯♯♯', 'D♯♯♯', 'A♯♯♯', 'E♯♯♯', 'B♯♯♯', 'F♯♯♯♯', 'C♯♯♯♯']
#       -14      -13      -12      -11      -10      -9       -8      -7      -6      -5      -4      -3      -2      -1       0     +1     +2     +3     +4     +5     +6      +7      +8      +9      +10     +11     +12     +13      +14
#       -28      -27      -26      -25      -24      -23      -22     -21     -20     -19     -18     -17     -16     -15      0     +15    +16    +17    +18    +19    +20     +21     +22     +23     +24     +25     +26     +27      +28
########################################################################################################################################################################################################
#       -28     -27     -26     -25     -24     -23     -22    -21    -20    -19    -18    -17    -16    -15   -14   -13   -12   -11   -10   -9    -8   -7   -6   -5   -4   -3   -2   -1   0  +1  +2  +3  +4  +5  +6   +7   +8   +9   +10  +11  +12  +13   +14   +15   +16   +17   +18   +19   +20    +21    +22    +23    +24    +25    +26    +27     +28
C3F = ['C♭♭♭♭','G♭♭♭♭','D♭♭♭♭','A♭♭♭♭','E♭♭♭♭','B♭♭♭♭','F♭♭♭','C♭♭♭','G♭♭♭','D♭♭♭','A♭♭♭','E♭♭♭','B♭♭♭','F♭♭','C♭♭','G♭♭','D♭♭','A♭♭','E♭♭','B♭♭','F♭','C♭','G♭','D♭','A♭','E♭','B♭','F','C','G','D','A','E','B','F♯','C♯','G♯','D♯','A♯','E♯','B♯','F♯♯','C♯♯','G♯♯','D♯♯','A♯♯','E♯♯','B♯♯','F♯♯♯','C♯♯♯','G♯♯♯','D♯♯♯','A♯♯♯','E♯♯♯','B♯♯♯','F♯♯♯♯','C♯♯♯♯']

C4F = ['Cbbbb', 'Gbbbb', 'Dbbbb', 'Abbbb', 'Ebbbb', 'Bbbbb', 'Fbbb', 'Cbbb', 'Gbbb', 'Dbbb', 'Abbb', 'Ebbb', 'Bbbb', 'Fbb', 'Cbb', 'Gbb', 'Dbb', 'Abb', 'Ebb', 'Bbb', 'Fb', 'Cb', 'Gb', 'Db', 'Ab', 'Eb', 'Bb', 'F', 'C', 'G', 'D', 'A', 'E', 'B', 'F#', 'C#', 'G#', 'D#', 'A#', 'E#', 'B#', 'F##', 'C##', 'G##', 'D##', 'A##', 'E##', 'B##', 'F###', 'C###', 'G###', 'D###', 'A###', 'E###', 'B###', 'F####', 'C####']
########################################################################################################################################################################################################
#       -28      -27      -26      -25      -24      -23      -22     -21     -20     -19     -18     -17     -16     -15    -14    -13    -12    -11    -10    -9     -8    -7    -6    -5    -4    -3    -2    -1   0
C2F = ['Cbbbb', 'Gbbbb', 'Dbbbb', 'Abbbb', 'Ebbbb', 'Bbbbb', 'Fbbb', 'Cbbb', 'Gbbb', 'Dbbb', 'Abbb', 'Ebbb', 'Bbbb', 'Fbb', 'Cbb', 'Gbb', 'Dbb', 'Abb', 'Ebb', 'Bbb', 'Fb', 'Cb', 'Gb', 'Db', 'Ab', 'Eb', 'Bb', 'F', 'C', 
       'C####', 'F####', 'B###',  'E###',  'A###',  'D###',  'G###', 'C###', 'F###', 'B##',  'E##',  'A##',  'D##',  'G##', 'C##', 'F##', 'B#',  'E#',  'A#',  'D#',  'G#', 'C#', 'F#', 'B',  'E',  'A',  'D',  'G' ]
#       +1       +2       +3       +4       +5       +6       +7      +8      +9      +10     +11     +12     +13     +14    +15    +16    +17    +18    +19    +20    +21   +22   +23   +24   +25   +26   +27   +28

#        0   +1   +2    +3    +4    +5    +6    +7    +8    +9     +10    +11    +12    +13    +14    +15    +16     +17     +18     +19     +20     +21     +22     +23      +24      +25     +26      +27      +28
C3F = ['C', 'F', 'Bb', 'Eb', 'Ab', 'Db', 'Gb', 'Cb', 'Fb', 'Bbb', 'Ebb', 'Abb', 'Dbb', 'Gbb', 'Cbb', 'Fbb', 'Bbbb', 'Ebbb', 'Abbb', 'Dbbb', 'Gbbb', 'Cbbb', 'Fbbb', 'Bbbbb', 'Ebbbb', 'Abbbb','Cbbbb', 'Dbbbb', 'Gbbbb',   
            'G', 'D',  'A',  'E',  'B',  'F#', 'C#', 'G#', 'D#',  'A#',  'E#',  'B#',  'F##', 'C##', 'G##', 'D##',  'A##',  'E##',  'B##',  'F###', 'C###', 'G###', 'D###',  'A###',  'E###', 'B###',  'F####', 'C####']
#            -1   -2    -3    -4    -5    -6    -7    -8    -9     -10    -11    -12    -13    -14    -15    -16     -17     -18     -19     -20     -21     -22     -23      -24      -25     -26      -27      -28

C4F = ['Cbbbb', 'Gbbbb', 'Dbbbb', 'Abbbb', 'Ebbbb', 'Bbbbb', 'Fbbb', 'Cbbb', 'Gbbb', 'Dbbb', 'Abbb', 'Ebbb', 'Bbbb', 'Fbb', 'Cbb', 'Gbb', 'Dbb', 'Abb', 'Ebb', 'Bbb', 'Fb', 'Cb', 'Gb', 'Db', 'Ab', 'Eb', 'Bb', 'F', 'C', 
       'G', 'D', 'A', 'E', 'B', 'F#', 'C#', 'G#', 'D#', 'A#', 'E#', 'B#', 'F##', 'C##', 'G##', 'D##', 'A##', 'E##', 'B##', 'F###', 'C###', 'G###', 'D###', 'A###', 'E###', 'B###', 'F####', 'C####']
#       +1   +2   +3   +4   +5   +6    +7    +8    +9   +10  +11  +12  +13   +14   +15   +16   +17   +18   +19   +20    +21    +22    +23    +24    +25    +26    +27     +28
#       +28  +27  +26  +25  +24  +23   +22   +21   +20   +19   +18   +17   +16    +15    +14    +13    +12    +11    +10    +9      +8      +7      +6      +5      +4      +3      +2       +1

#                    -28      -27      -26      -25      -24      -23      -22     -21     -20     -19     -18     -17    -16      -15      0     +15    +16    +17    +18    +19    +20     +21     +22     +23     +24     +25     +26     +27      +28
#                    -14      -13      -12      -11      -10      -9       -8      -7      -6      -5      -4      -3      -2      -1       0     +1     +2     +3     +4     +5     +6      +7      +8      +9      +10     +11     +12     +13      +14
#        self.COF = ['C♭♭♭♭', 'G♭♭♭♭', 'D♭♭♭♭', 'A♭♭♭♭', 'E♭♭♭♭', 'B♭♭♭♭', 'F♭♭♭', 'C♭♭♭', 'G♭♭♭', 'D♭♭♭', 'A♭♭♭', 'E♭♭♭', 'B♭♭♭', 'F♭♭',
#                    'C♭♭',   'G♭♭',   'D♭♭',   'A♭♭',   'E♭♭',   'B♭♭',   'F♭',   'C♭',   'G♭',   'D♭',   'A♭',   'E♭',   'B♭',   'F',    'C',   'G',   'D',   'A',   'E',   'B',   'F♯',   'C♯',   'G♯',   'D♯',   'A♯',   'E♯',   'B♯',   'F♯♯',   'C♯♯',
#                                                                                                                                                 'G♯♯', 'D♯♯', 'A♯♯', 'E♯♯', 'B♯♯', 'F♯♯♯', 'C♯♯♯', 'G♯♯♯', 'D♯♯♯', 'A♯♯♯', 'E♯♯♯', 'B♯♯♯', 'F♯♯♯♯', 'C♯♯♯♯']
#                    -14      -13      -12      -11      -10      -9       -8      -7      -6      -5      -4      -3      -2      -1       0     +1     +2     +3     +4     +5     +6      +7      +8      +9      +10     +11     +12     +13      +14
#                    -28      -27      -26      -25      -24      -23      -22     -21     -20     -19     -18     -17     -16     -15      0     +15    +16    +17    +18    +19    +20     +21     +22     +23     +24     +25     +26     +27      +28
'''
########################################################################################################################################################################################################
########################################################################################################################################################################################################
class Intonation:
    ic   = 0
#               0   +1   +2    +3    +4    +5    +6    +7    +8    +9    +10   +11   +12   +13    +14   +15   +16    +17    +18    +19    +20    +21     +22    +23    +24    +25     +26    +27    +28    +29    +30     +31     +32      +33     +34
#   COF1    = ['C', 'G', 'D',  'A',  'E',  'B',  'F♯', 'C♯', 'G♯', 'D♯', 'A♯', 'E♯', 'B♯', 'F𝄪',  'C𝄪', 'G𝄪',  'D𝄪',   'A𝄪',  'E𝄪',   'B𝄪',  'F♯𝄪',  'C♯𝄪',  'G♯𝄪', 'D♯𝄪',  'A♯𝄪',  'E♯𝄪',  'B♯𝄪', 'F𝄪𝄪',  'C𝄪𝄪',  'G𝄪𝄪',  'D𝄪𝄪',   'A𝄪𝄪',   'E𝄪𝄪',   'B𝄪𝄪',   'F♯𝄪𝄪']
#   COF2    = [     'F', 'B♭', 'E♭', 'A♭', 'D♭', 'G♭', 'C♭', 'F♭', 'B𝄫', 'E𝄫', 'A𝄫', 'D𝄫', 'G𝄫', 'C𝄫', 'F𝄫', 'B♭𝄫', 'E♭𝄫', 'A♭𝄫', 'D♭𝄫', 'G♭𝄫', 'C♭𝄫', 'F♭𝄫', 'B𝄫𝄫', 'E𝄫𝄫', 'A𝄫𝄫', 'D𝄫𝄫', 'G𝄫𝄫', 'C𝄫𝄫', 'F𝄫𝄫', 'B♭𝄫𝄫', 'E♭𝄫𝄫', 'A♭𝄫𝄫', 'D♭𝄫𝄫', 'G♭𝄫𝄫']
#            0   +1   +2    +3    +4    +5    +6    +7    +8    +9     +10    +11    +12     +13    +14   +15     +16     +17     +18     +19     +20     +21     +22     +23      +24      +25      +26     +27       +28      +29      +30       +31       +32       +33       +34
    COF1 = ['C', 'G', 'D',  'A',  'E',  'B',  'F♯', 'C♯', 'G♯', 'D♯',  'A♯',  'E♯',  'B♯',  'F♯♯', 'C♯♯', 'G♯♯', 'D♯♯',  'A♯♯',  'E♯♯',  'B♯♯',  'F♯♯♯', 'C♯♯♯', 'G♯♯♯', 'D♯♯♯',  'A♯♯♯',  'E♯♯♯',  'B♯♯',  'F♯♯♯♯',  'C♯♯♯♯', 'G♯♯♯♯',  'D♯♯♯♯',  'A♯♯♯♯', 'E♯♯♯♯',  'B♯♯♯♯', 'F♯♯♯♯♯']
    COF2 = [     'F', 'B♭', 'E♭', 'A♭', 'D♭', 'G♭', 'C♭', 'F♭', 'B♭♭', 'E♭♭', 'A♭♭', 'D♭♭', 'G♭♭', 'C♭♭', 'F♭♭', 'B♭♭♭', 'E♭♭♭', 'A♭♭♭', 'D♭♭♭', 'G♭♭♭', 'C♭♭♭', 'F♭♭♭', 'B♭♭♭♭', 'E♭♭♭♭', 'A♭♭♭♭', 'D♭♭♭♭', 'G♭♭♭♭', 'C♭♭♭♭', 'F♭♭♭♭', 'B♭♭♭♭♭', 'E♭♭♭♭♭', 'A♭♭♭♭♭', 'D♭♭♭♭♭', 'G♭𝄫𝄫']
#                -1    -2    -3    -4    -5    -6    -7    -8    -9    -10     -11   -12     -13    -14   -15     -16     -17     -18     -19     -20     -21     -22     -23      -24      -25      -26     -27       -28      -29      -30       -31       -32      -33       -34
#    COF2.reverse()
    COF     = list(COF1)
    COF.extend(reversed(COF2))
    def __init__(self, n='C', rf=440, ss=V_SOUND, csv=0):
        self.rf     = rf
        self.ss     = ss
        self.csv    = csv
        self.i      = Notes.N2I[n] + 48
        self.j      = 0
        self.k      = 0
        self.m      = n
        self.n      = Z
        self.o      = Z
        self.centKs = []
        self.ivalKs = []
        self.ck2ikm = {} # self.set_ck2ikm()
        self.nimap  = {}
        self.ckmap  = {} # self.reset_ckmap()
        self.dmpCOF()
        l           = len(self.COF) - 12
        self.COFM   = { self.COF[i]: (self.COF[(i+6)], self.COF[(i-6)]) for i in range(1+l//2) }
        self.COFM  |= { self.COF[i]: (self.COF[(i+6)], self.COF[(i-6)]) for i in range(-l//2, 0) }
        self.dmpCOFM()
        self.dmpUnis()
        self.FREFS  = F440s if self.rf == 440 else F432s
        self.w0     = CM_P_M * self.ss
        self.f0     = self.FREFS[self.i]

    ####################################################################################################################################################################################################
    def reset_ckmap(self):  return { ck:{'Count':0} for ck in list(self.centKs) } # todo called in _setup() and at end of dmpMaps()
    def set_ck2ikm(self):   self.ck2ikm = { self.centKs[i]: k for i, k in enumerate(self.ivalKs) }   ;   return self.ck2ikm # todo this base class method initializes and or sets self.ck2ikm
    ####################################################################################################################################################################################################
    @classmethod # if cls.ic==0 else None
    def dmpCOF(cls):
        cls.ic += 1
        slog(f'{cls.ic:2}{fmtl(cls.COF)}', p=0)
#                C G D A E B F♯ C♯ G♯ D♯ A♯ E♯ B♯ F𝄪 C𝄪 G𝄪 D𝄪 A𝄪 E𝄪 B𝄪 F♯𝄪 C♯𝄪 G♯𝄪 D♯𝄪 A♯𝄪 E♯𝄪 B♯𝄪 F𝄪𝄪 C𝄪𝄪 G𝄪𝄪 D𝄪𝄪 A𝄪𝄪 E𝄪𝄪 B𝄪𝄪 F♯𝄪𝄪 G♭𝄫𝄫 D♭𝄫𝄫 A♭𝄫𝄫 E♭𝄫𝄫 B♭𝄫𝄫 F𝄫𝄫 C𝄫𝄫 G𝄫𝄫 D𝄫𝄫 A𝄫𝄫 E𝄫𝄫 B𝄫𝄫 F♭𝄫 C♭𝄫 G♭𝄫 D♭𝄫 A♭𝄫 E♭𝄫 B♭𝄫 F𝄫 C𝄫 G𝄫 D𝄫 A𝄫 E𝄫 B𝄫 F♭ C♭ G♭ D♭ A♭ E♭ B♭ F
        slog('   0 1 2 3 4 5 6  7  8  9  10 11 12 13 1415 1617 18 19 20 21  22 23  24  25 26  27 28  29 30 31  32 33 34 -34   -33  -32   -31   -30  -29  -28  -27 -26 -25  -24  -23 -22 -21  -20 -19 -18  -17 -16 -15-14 -13-12 11 -10-9 -8 -7 -6 -5 -4 -3 -2 -1',  p=0)
        slog('   0 1 2 3 4 5 6  7  8  9  10 11 12 13 1415 1617 18 19 20 21  22 23  24  25 26  27 28  29 30 31  32 33 34  35    36   37    38    39   40   41   42  43  44   45   46  47  48   49  50  51   52  53  54 55  56 57 58  59 60 61 62 63 64 65 66 67 68', p=0)
        slog('   0 1 2 3 4 5 6  7  8  9  10 11 12 13 1415 1617 18 19 20 21  22 23  24  25 26  27 28                                                       29   30  31  32   33   34  35  36   37  38  39   40  41  42 43  44 45 46  47 48 49 50 51 52 53 54 55 56', p=0)
        slog('   0 1 2 3 4 5 6  7  8  9  10 11 12 13 1415 1617 18 19 20 21  22 23  24  25 26  27 28                                                      -28  -27 -26 -25  -24  -23 -22 -21  -20 -19 -18  -17 -16 -15-14- 13-12 11 -10-9 -8 -7 -6 -5 -4 -3 -2 -1',  p=0)
#       slog('   C G D A E B F♯ C♯ G♯ D♯ A♯ E♯ B♯ F𝄪 C𝄪 G𝄪 D𝄪 A𝄪 E𝄪 B𝄪 F♯𝄪 C♯𝄪 G♯𝄪 D♯𝄪 A♯𝄪 E♯𝄪 B♯𝄪 F𝄪𝄪 C𝄪𝄪                                                       C𝄫𝄫 G𝄫𝄫 D𝄫𝄫 A𝄫𝄫 E𝄫𝄫 B𝄫𝄫 F♭𝄫 C♭𝄫 G♭𝄫 D♭𝄫 A♭𝄫 E♭𝄫 B♭𝄫 F𝄫 C𝄫 G𝄫 D𝄫 A𝄫 E𝄫 B𝄫 F♭ C♭ G♭ D♭ A♭ E♭ B♭ F',  p=0)
    def dmpUnis(self):
        slog(f'{F}{N}{S}{E}{X}')
        for i in range(16):
            self.dmpUni(0x1d100 + i*16)
    @staticmethod
    def dmpUni(u=0x1d110):
        n = 16
        j = [f'{u:x}-{u+n-1:x}: ']
        for i in range(n):
            j.append(f'{u+i:c}')
        k = W.join(j)
        slog(k, p=0)

    def dmpCOFM(self):
        n   = (len(self.COF)-12)//2
        cof = self.COF[:n+1] + self.COF[-n:]
        slog(f'{len(cof)}{fmtl(cof[:n+1])}{W*52}{fmtl(cof[-n:])}', p=0)
        for i, k in enumerate(cof):
            assert k in self.COFM,  f'{i=} {k=} {n=} {fmtl(cof)} keys={fmtl(list(self.COFM.keys()))}'
            v = self.COFM[k]
            j = i if i <= len(cof)//2 else i - len(cof)
            slog(f'{i:2} {j:3} {k:5} {v}', p=0)
    @staticmethod
    def i2spr(i):
        if i < 0: return '-' + Z.join( SUPERS[int(digit)] for digit in str(i) if str.isdigit(digit) )
        return                 Z.join( SUPERS[int(digit)] for digit in str(i) )

    @staticmethod
    def r2cents(r): return math.log2(r) * NT * 100

    @staticmethod
    def i2dCent(k):
        return k  if   0<=k<50  else k-100 if  50<=k<150 else k-200 if 150<=k<250 else k-300  if 250<=k<350  else k-400  if  350<=k<450  else k-500  if  450<=k<550   else k-600 if 550<=k<650 else \
            k-700 if 650<=k<750 else k-800 if 750<=k<850 else k-900 if 850<=k<950 else k-1000 if 950<=k<1050 else k-1100 if 1050<=k<1150 else k-1200 if 1150<=k<=1200 else None
    ####################################################################################################################################################################################################
    @staticmethod
    def norm(n):
        i = 0
        if n > 1:
            while n > 2:
                n /= 2  ;  i -= 1
        elif n < 1:
            while n < 1:
                n *= 2  ;  i += 1
        return n, i
    ####################################################################################################################################################################################################
    def stck5ths(self, n, i=0, dbg=0):  s = [ self.stackI(3,  k, i+k) for k in range(1, 1+n) ]   ;   slog(f'{i=} {n=}', f=2) if dbg else None   ;   return s
    def stck4ths(self, n, i=0, dbg=0):  s = [ self.stackI(3, -k, i-k) for k in range(1, 1+n) ]   ;   slog(f'{i=} {n=}', f=2) if dbg else None   ;   return s
    def stackI(self, a, b, i):    return [ a, b, self.COF[i], Z ]
    ####################################################################################################################################################################################################
    def ac2r(self, a, c):
        r0   = a ** c
        r, j = self.norm(r0)   ;   assert r == r0 * (2 ** j),  f'{r=} {r0=} {j=}'
        return r, j

    def abcs(self, a, b, i=0, dbg=1): # (n5ths, n4ths, index)
        mm, nn, oo, ff = (Y, Y, Y, 3) if self.csv else (W, Z, '|', 2)
        abc1   = self.stck5ths(a, i, dbg=1)
        abc2   = self.stck4ths(b, i, dbg=1)
        abc3   = [ self.stackI(3, 0, i) ]   ;   abc3.extend(abc1)   ;   abc3.extend(abc2)   ;   abc3.append(self.stackI(2, 1, i))
        abc4   = sorted([(z[0], z[1], z[2], self.ac2r(z[0], z[1])[1]) for z in abc3], key=lambda z: self.ac2r(z[0], z[1])[0])
        abcLst = [abc1, abc2, abc3, abc4]
        if dbg:
            wb = [2, 3, 2, 3]   ;   pfx, sfx = [], []
            for j, abcs in enumerate(abcLst):
                msg = []   ;   pfx.append(f'  abc{j+1} {nn}[{nn}')  ;  sfx.append(f'{nn}]{nn}')
                for k, abc in enumerate(abcs):
                    if k:  msg.append(oo)
                    msg.append(f'{fmtl(abc, w=wb, d=Z, s=mm)}')
                slog(f'{pfx[j]}{Z.join(msg)}{sfx[j]}', p=0, f=ff)
        return abcLst

    def i2Abcs(self, i):
        ff = 3 if self.csv else 2 # q = 2*p+1
        p = 6   ;   q = 13
#        p = 7   ;   q = 15
#        p = 12  ;   q = 25
#        p = 18  ;   q = 37
#        p = 21  ;   q = 43
        if -p <= i <= p:   a = p - i   ;  b = i + p
        else:              a = q       ;  b = q
        slog(f'{i=} {a=} {b=}', f=ff)
        return self.abcs(a, b, i=i)

    def new__i2Abcs(self, i):
        ff = 3 if self.csv else 2
        match i:
            case -7|-6|-5|-4|-3|-2|-1|0|1|2|3|4|5|6|7:   a = 7 - i   ;  b = i + 7
            case _:                                      a = 15      ;  b = 15
        slog(f'{i=} {a=} {b=}', f=ff)
        return self.abcs(a, b, i=i)

    def OLD__i2Abcs(self, i):
        ff = 3 if self.csv else 2
        if   i == -7:  a, b = 14,  0 # Cb
        elif i == -6:  a, b = 13,  1 # Gb
        elif i == -5:  a, b = 12,  2 # Db
        elif i == -4:  a, b = 11,  3 # Ab
        elif i == -3:  a, b = 10,  4 # Eb
        elif i == -2:  a, b =  9,  5 # Bb
        elif i == -1:  a, b =  8,  6 # F
        elif i ==  0:  a, b =  7,  7 # C
        elif i ==  1:  a, b =  6,  8 # G
        elif i ==  2:  a, b =  5,  9 # D
        elif i ==  3:  a, b =  4, 10 # A
        elif i ==  4:  a, b =  3, 11 # E
        elif i ==  5:  a, b =  2, 12 # B
        elif i ==  6:  a, b =  1, 13 # F#
        elif i ==  7:  a, b =  0, 14 # C#
        else:          a, b = 15, 15
        slog(f'{i=} {a=} {b=}', f=ff)
        return self.abcs(a, b, i=i)
    ####################################################################################################################################################################################################
    def fmtNPair(self, i, d=0, dbg=0):
        n0, _   = self.i2nPair(self.i, o=0)   ;   d = '/' if d==1 else W if d==0 else d
        n1, n2  = self.i2nPair(self.k + i, b=0 if i in (4, 6, 11) or self.j in (self.i + 4, self.i + 6, self.i + 11) else 1, o=0, e=1)   ;   slog(f'{self.j=} {i=} {n0=} {n1=} {n2=}') if dbg else None
        if i and i != NT + 1:
            if          n1 == self.COFM[n0][1]:   return n1
            if          n1 == self.COFM[n0][0]:   return n2
            if   n2 and n2 != self.COFM[n0][1]:   n1 += d + n2
        slog(f'return {n1=}') if dbg else None
        return n1

    @staticmethod
    def f2nPair(f, rf=440, b=None, o=0, e=0): # freq, refFreq, index, flat, oct, enharm
        ni = NT * math.log2(f / rf) # fixme
        i  = round(A4_INDEX + ni)
        return Intonation.i2nPair(i, b, o, e)

    @staticmethod
    def i2nPair(i, b=None, o=0, e=0): # index, flat, oct, enharm
        m = Z    ;    n = FLATS[i] if b == 1 else SHRPS[i]
        if not o:     n = n[:-1] # remove the octave number e.g. A4 -> A
        if e == 1 and len(n) > 1:
            m = FLATS[i] if not b else SHRPS[i]   ;   m = m[:-1] if not o else m # remove the octave number e.g. A4 -> A
        return n, m
    ####################################################################################################################################################################################################
    def setup(self, o, csv=0):
        self.csv = csv   ;   pp = 0   ;   x = 0
        if   o == 0:
            self.nimap = {}
            slog(    f'P1  0-{NT}+{x} {self.fim(Z)} {self.csv=}',        p=pp)
            for i in range(0, NT + x):
                self.j = self.i + (i * 7) % (NT + x)
                slog(f'P1  0-{NT}+{x} {self.fim(Z)} {self.csv=} : {i=}', p=pp)
                self._setup(i)
        elif o == 1:
            self.nimap = {}
            slog(    f'P2A 7-{NT}+{x} {self.fim(Z)} {self.csv=}',        p=pp)
            for i in range(7, NT + x):
                self.j = self.i + (i * 7) % (NT + x)
                slog(f'P2A 7-{NT}+{x} {self.fim(Z)} {self.csv=} : {i=}', p=pp)
                self._setup(i)
            slog(    f'P2B 0-7{x=:1}  {self.fim(Z)} {self.csv=}',        p=pp)
            for i in range(0, 7):
                self.j = self.i + (i * 7) % (NT + x)
                slog(f'P2B 0-7{x=:1}  {self.fim(Z)} {self.csv=} : {i=}', p=pp)
                self._setup(i)

    def setup2(self, o, o2, u=13, dbg=0, csv=0):
        self.csv = csv   ;   pp = 0   ;   x = 0
        if   o == 0:
            self.nimap = {}
            slog(    f'P1  0-{NT}+{x} {self.fim(Z)} {self.csv=} : {o2=} {u=}', p=pp) if dbg else None
            for i in range(0, NT):
                self.j = self.i + (i * 7) % (NT + x)
                slog(f'P1  0-{NT}+{x} {self.fim(Z)} {self.csv=} : {i=}',       p=pp) if dbg else None
                self._setup(i, u=u, o=o2, dbg=dbg)
        elif o == 1:
            self.nimap = {}
            slog(    f'P2A 7-{NT}+{x} {self.fim(Z)} {self.csv=} : {o2=} {u=}', p=pp) if dbg else None
            for i in range(7, NT):
                self.j = self.i + (i * 7) % (NT + x)
                slog(f'P2A 7-{NT}+{x} {self.fim(Z)} {self.csv=} : {i=}',       p=pp) if dbg else None
                self._setup(i, u=u, o=o2, dbg=dbg)
            slog(    f'P2B 0-7{x=:1}  {self.fim(Z)} {self.csv=} : {o2=} {u=}', p=pp) if dbg else None
            for i in range(0, 7):
                self.j = self.i + (i * 7) % (NT + x)
                slog(f'P2B 0-7{x=:1}  {self.fim(Z)} {self.csv=} : {i=}',       p=pp) if dbg else None
                self._setup(i, u=u, o=o2, dbg=dbg)
    ####################################################################################################################################################################################################
    def dmpNiMap( self, ni, x, upd=0, dbg=1): pass
    def dmpCkMap( self, u=9, o=0, dbg=1):     pass

    def dmpCkMap2(self):
        ks = []   ;   x = 8   ;   w = f'^{x}'   ;   o = '|'
        for k, v in self.ckmap.items():
            ks.append(f'{k:4} {v["Count"]:2}')
        slog(f'{fmtl(ks, w=w, s=o)}', p=0)

    def updCkMap(self, ck, ckm, n, f, abc, cent, idx): # f = f0 * pa/pb # n if k==ik else W*2
        assert ck in ckm.keys(),  f'{ck=} {ckm.keys()=}'
        ckm[ck]['Count'] = ckm[ck]['Count'] + 1 if 'Count' in ckm[ck] else 1
        ckm[ck]['Freq']  = f                     ;   ckm[ck]['Wavln'] = self.w0 / f
        ckm[ck]['Cents'] = cent                  ;   ckm[ck]['DCent'] = self.i2dCent(cent)
        ckm[ck]['Note']  = n                     ;   ckm[ck]['Abcd']  = abc
        ckm[ck]['Ival']  = self.ck2ikm[ck]       ;   ckm[ck]['Index'] = idx
    ####################################################################################################################################################################################################
    def dmpIndices(self, pfx=Z, w=0):
        mm, ff = (Y, 3) if self.csv else(W, 1)   ;   ww = f'^{w}'   ;   n = len(self.centKs)
        ii     = [ f'{i}' for i in range(n) ]    ;   slog(f'{pfx}{fmtl(ii, w=ww, s=mm, d=Z)}', p=0, f=ff)

    def fim(self, pfx=None):  pfx = str(self) + W if pfx is None else Z   ;   return f'{pfx}[{self.i:2} {self.j:2} {self.k:2} {self.m:2} {self.n:2} {self.o:2}]'
    @staticmethod
    def fabc(abc):                return [ fmtl(e, w=[2,3,2,3], d=Z) for e in abc ]
    ####################################################################################################################################################################################################
    def _setup(self, j, u=9, o=0, dbg=1):
        x = 13  ;  mm, nn, oo, ff = (Y, Y, Y, 3) if self.csv else (W, Z, '|', 1)  ;  cki, ww, y, z, _, f0, w3 = -1, f'^{x}', 6, x-2, x*W, self.FREFS[self.j], [W, W, W]  ;  pfx = f'{mm}  k  {mm}{nn} {nn}'
        self.k = 0   ;   self.o = Z  ;  self.n = Notes.i2n()[self.j % NT]   ;   k = 6 - j if j > 6 else j
        if dbg: slog(f'BGN {self.fim()} {j=} {k=} {u=} {o=} {self.csv=} {dbg=}', p=0, f=ff)  ;  self.dmpIndices(pfx, x)  ;  self.dmpDataTableLine(x+1)
        cs, ds, ii, ns, vs, fs, ws = [], [], [], [], [], [], []   ;   r0s, rAs, rBs, r1s, r2s, r3s = [], [], [], [], [], []   ;   abcdMap = []  ;  ckm = self.ckmap # reset_ckmap()
        tmp = self.i2Abcs(k)  ;  abc0 = list(tmp[-1])  ;  abc1, abc2, abc3, abc4 = self.fabc(tmp[0]), self.fabc(tmp[1]), self.fabc(tmp[2]), self.fabc(tmp[3])  ;  abc1.insert(0, fmtl(w3, w=2, d=Z))  ;  abc2.insert(0, fmtl(w3, w=2, d=Z)) # insert blanks to align log/csv file
        for i, e in enumerate(abc0): # ;  cf = 1 if a==3 else -1  ;  self.k = 48 + (7 * cf) % NT
            a, b, ca, n = e[0], 2, e[1], e[2]  ;  r, cb = self.ac2r(a, ca)  ;  f = r * f0  ;  w = self.w0 / f  ;  cki += 1  ;  abcd = [a, ca, b, cb] if a**abs(ca) >= b**abs(cb) else [b, cb, a, ca]
            c = self.r2cents(r)  ;  d = self.i2dCent(c)  ;  rc = round(c)
            assert rc in self.ck2ikm,  f'{rc=} not in ck2ikm {self.i=} {i=} {self.j=} {c=} {r=} {abcd=} {fmtm(self.ck2ikm, d=Z)} {len(self.ck2ikm)=} {len(self.nimap)=}'
            while cki < len(self.centKs) and self.centKs[cki] < rc:
                ii.append(_)  ;  cs.append(_)  ;  ds.append(_)  ;  fs.append(_)  ;  ws.append(_)  ;  ns.append(_)  ;  r0s.append(_)  ;  rAs.append(_)  ;  rBs.append(_)  ;  r1s.append(_)  ;  r2s.append(_)  ;  r3s.append(_)
                v = self.ck2ikm[self.centKs[cki]]  ;  vs.append(v)  ;  cki += 1  ;  j = len(ii)-1  ;  abc1.insert(j, fmtl(w3, w=2, d=Z))  ;  abc2.insert(j, fmtl(w3, w=2, d=Z))  ;  abc3.insert(j, fmtl(w3, w=2, d=Z))  ;  abc4.insert(j, fmtl(w3, w=2, d=Z))
            v = self.ck2ikm[rc]  ;  ii.append(i)  ;  fs.append(fmtf(f, z))  ;  ws.append(fmtf(w, z))  ;  cs.append(fmtf(c, z-4))  ;  ds.append(fmtg(d, z-4))  ;  ns.append(n)  ;  vs.append(v)  ;  abcdMap.append(abcd)
            r0s, rAs, rBs, r1s, r2s, r3s = self.addFmtRs(a, ca, b, cb, rs=[r0s, rAs, rBs, r1s, r2s, r3s], u=y, w=x,     i=i, j=rc)
            if dbg:   self.updCkMap(rc, ckm, n, f, abcd, c, i)
        self.nimap[self.j] = [ckm, tmp[2], abcdMap]   ;   sfx = f'{nn}]'   ;   sfxc = f'{nn}]{mm}cents'   ;   sfxf = f'{nn}]{mm}Hz'   ;   sfxw = f'{nn}]{mm}cm'   ;   cks = self.centKs
        while len(abc1) < len(abc3): abc1.append(fmtl(w3, w=2, d=Z)) # append blanks for alignment in log/csv files
        while len(abc2) < len(abc3): abc2.append(fmtl(w3, w=2, d=Z)) # append blanks for alignment in log/csv files
        if dbg:
            slog(f'{mm}CentK{mm}{nn}[{nn}{fmtl(cks,  w=ww, s=oo, d=Z)}{sfxc}', p=0, f=ff)
            slog(f'{mm}Itval{mm}{nn}[{nn}{fmtl(vs,   w=ww, s=oo, d=Z)}{sfx}',  p=0, f=ff)
            slog(f'{mm}Note {mm}{nn}[{nn}{fmtl(ns,   w=ww, s=oo, d=Z)}{sfx}',  p=0, f=ff)
            slog(f'{mm}Ratio{mm}{nn}[{nn}{fmtl(r0s,  w=ww, s=oo, d=Z)}{sfx}',  p=0, f=ff)
            slog(f'{mm}Rati1{mm}{nn}[{nn}{fmtl(r1s,  w=ww, s=oo, d=Z)}{sfx}',  p=0, f=ff)
            slog(f'{mm}Rati2{mm}{nn}[{nn}{fmtl(r2s,  w=ww, s=oo, d=Z)}{sfx}',  p=0, f=ff)
            slog(f'{mm}Rati3{mm}{nn}[{nn}{fmtl(r3s,  w=ww, s=oo, d=Z)}{sfx}',  p=0, f=ff)
            slog(f'{mm}Freq {mm}{nn}[{nn}{fmtl(fs,   w=ww, s=oo, d=Z)}{sfxf}', p=0, f=ff)
            slog(f'{mm}Wavln{mm}{nn}[{nn}{fmtl(ws,   w=ww, s=oo, d=Z)}{sfxw}', p=0, f=ff)
            slog(f'{mm}Index{mm}{nn}[{nn}{fmtl(ii,   w=ww, s=oo, d=Z)}{sfx}',  p=0, f=ff)
            slog(f'{mm} ABC1{mm}{nn}[{nn}{fmtl(abc1, w=ww, s=oo, d=Z)}{sfx}',  p=0, f=ff)
            slog(f'{mm} ABC2{mm}{nn}[{nn}{fmtl(abc2, w=ww, s=oo, d=Z)}{sfx}',  p=0, f=ff)
            slog(f'{mm} ABC3{mm}{nn}[{nn}{fmtl(abc3, w=ww, s=oo, d=Z)}{sfx}',  p=0, f=ff)
            slog(f'{mm} ABC4{mm}{nn}[{nn}{fmtl(abc4, w=ww, s=oo, d=Z)}{sfx}',  p=0, f=ff)
            slog(f'{mm}Cents{mm}{nn}[{nn}{fmtl(cs,   w=ww, s=oo, d=Z)}{sfxc}', p=0, f=ff)
            slog(f'{mm}DCent{mm}{nn}[{nn}{fmtl(ds,   w=ww, s=oo, d=Z)}{sfxc}', p=0, f=ff)   ;   self.dmpDataTableLine(x+1)
        self.dmpMaps(u, o=o, dbg=dbg)  ;  slog(f'END {self.fim()} {j=} {k=} {u=} {o=} {self.csv=} {dbg=}', p=0, f=ff) if dbg else None
    ####################################################################################################################################################################################################
    def dmpMaps(self, u, o, dbg=1):
        if dbg:
            self.dmpNiMap(0, x=13, upd=1, dbg=dbg)
            self.dmpNiMap(1, x=13, upd=1, dbg=dbg)
            self.dmpNiMap(2, x=13, upd=1, dbg=dbg)
            self.dmpNiMap(3, x=13, upd=1, dbg=dbg)
            self.dmpNiMap(4, x=13, upd=1, dbg=dbg)
            self.dmpCk2Ik(   x=13                )
            self.dmpCkMap(   u=u,         dbg=dbg)
            self.dmpNiMap(0, x=9,  upd=0, dbg=dbg)
            self.dmpNiMap(1, x=9,  upd=0, dbg=dbg)
            self.dmpNiMap(2, x=9,  upd=0, dbg=dbg)
            self.dmpNiMap(3, x=9,  upd=0, dbg=dbg)
            self.dmpNiMap(4, x=9,  upd=0, dbg=dbg)
            self.dmpCk2Ik(   x=9                 )
            self.chckIvls(                       )
            self.chckIvl2(                       )
        else:
            assert u in (12, 13), f'{u=} {self.fim()} {o=} {dbg=} {self.csv=}'
            self.dmpNiMap(  4, x=13, upd=1, dbg=dbg)
            self.dmpCkMap(     u=u,  o=o,   dbg=dbg)
        self.ckmap = self.reset_ckmap() # fixme call this once @ end of dmpMaps() --> todo wrap in a try:except:finally or a with/as clause:
    ####################################################################################################################################################################################################
    def dmpCk2Ik(self, x=13):
        mm, oo, f1, f2 = (Y, Y, 3, 3) if self.csv else (W, '|', 1, -3)   ;   pfx = f'{9*W}' if x == 9 else f'{11*W}' if x == 13 else Z
        if   x ==  9: slog(f'{pfx}{fmtm(self.ck2ikm, w=4, wv=2, s=3*W, d=Z)}', p=0, f=f1) if not self.csv else None
        elif x == 13: slog(f'{pfx}{fmtm(self.ck2ikm, w=4, wv=2, s=7*W, d=Z)}', p=0, f=f1) if not self.csv else None
        else:         slog(f'{pfx}{fmtm(self.ck2ikm, w=4, wv=2, s=oo,  d=Z)}', p=0, f=f2)
    ####################################################################################################################################################################################################
    '''
Jdx   CK     Knt    Freq    Wavln    Cents    DCent  Note       Abcd       Ival  Idx
 0 [    0: [   3  293.665  117.481  0.00000  +0.000  D      [ 3  0  2   0]  P1    0 ]]
    '''
    def chckIvls(self):
        mm, nn, oo, ff  = (Y, Y, Y, 3) if self.csv else (W, Z, '|', 1)
        slog(f'BGN chckIvls() {self.csv=}', p=0, f=ff)
        msgs, ws = [], [5, 8, 8, 8, 7, 5, 15, 5, 3]   ;   freq, f1 = None, 0
        keys = list(list(self.ckmap.values())[0].keys())   ;   keys[0] = 'Knt'   ;   keys[-1] = 'Idx'
        slog(f'Jdx{mm}{nn} {nn} CK{mm}{mm} {mm}{fmtl(keys, u="^", w=ws, s=mm, d=Z)}', p=0, f=ff)
        for i, (ck, cv) in enumerate(self.ckmap.items()):
            msg = f'{i:2}{mm}{nn}[{mm}{ck:4}{nn}:{mm}[{mm}'
            for k, v in cv.items():
                if   k == "Count":   msg += f' {v:2}{mm}'
                elif k == "Freq":    msg += f' {fmtf(v, 7)}{mm}'  ;  freq = v
                elif k == "Wavln":   msg += f' {fmtf(v, 7)}{mm}'
                elif k == "Cents":   msg += f' {fmtf(v, 7)}{mm}'
                elif k == "DCent":   msg += f' {fmtg(v, 6)}{mm}'
                elif k == "Note":
                    n, m = self.f2nPair(freq, b=1, o=0, e=1)   ;   assert m != n,  f'{i=} {ck=} {m=} {n=}'
                    if m:
                        if   m not in self.COFM[self.n]:   n = n + '/' + m
                        elif f1:                           n = m
                        else:                             f1 = 1
                    msg += f' {n:5}{mm}'
                elif k == "Abcd":    msg += f' {fmtl(v, w=[2, 2, 2, 3] , s=W):13}{mm}'
                elif k == "Ival":    msg += f' {v:3}{mm}'
                elif k == "Index":   msg += f' {v:2}{mm}'
            msg += f']{nn}]'   ;   msgs.append(msg)
        msgs = '\n'.join(msgs)
        slog(f'{msgs}', p=0, f=ff)
        slog(f'END chckIvls() {self.csv=}', p=0, f=ff)

    def chckIvl2(self, cm=0):
        ff = 3 if self.csv else 1
        if cm:    self.dmpCkMap2()
        cntr = Counter()
        keys = list(self.ckmap.keys())
        for k in keys:
            if self.ckmap[k]["Count"] > 0: self.chckIvl2A(k, cntr)
        sl = cntr.most_common()   ;   m, n = 0, 0
        for e in sl:
            n += e[1]   ;   m += 1
        slog(f'{n=} {m=} {fmtl(sl)}', p=0, f=ff)
        slog(f'{fmtm(cntr)}', p=0, f=ff)

    def chckIvl2A(self, key, cntr):
        mm, nn, oo, ff  = (Y, Y, Y, 3) if self.csv else (W, Z, '|', 1)  ;  x = 8  ;  uu = f'{x}'  ;   ww = f'{x}.3f'
        cs = []   ;   blnk = x*W   ;   cmk = 'Cents'
        cmv  = self.ckmap[key][cmk]
        for i, (ck, cv) in enumerate(self.ckmap.items()):
            for k2, v2 in cv.items():
                if k2 == cmk:
                    v  = abs(cv[cmk] - cmv)
                    cntr[f'{v:{ww}}'] += 1
                    cs.append(f'{v:{ww}}')
                    break
            else:
                cs.append(blnk)
            if cs and i==len(self.ckmap)-1:   slog(f'{fmtl(cs, w=uu, s=oo)}', p=0, f=ff)
    ########################################################################################################################################################################################################
    def dmpDataTableLine(self, w=10):
        c = '-'   ;   nn, mm, t = (Y, Y, Y) if self.csv else (Z, W, '|')
        col = f'{c * (w-1)}'   ;   n = len(self.centKs)
        cols = t.join([ col for _ in range(n) ])
        slog(f'{mm}     {mm}{nn} {nn}{cols}', p=0, f=3 if self.csv else 1)
    ####################################################################################################################################################################################################
    def addFmtRs(self, a, ca, b, cb, rs, u=4, w=9, k=None, i=None, j=None):
        assert rs and ist(rs, list),  f'{rs=} {type(rs)=} {a=} {ca} {b} {cb} {u=} {w=}'   ;   lr = len(rs)
        r0s, r2s, r3s = rs[0], rs[-2], rs[-1]          ;   r1s, rAs, rBs = None, None, None
        if   lr == 2:   rAs, rBs      = rs[0], rs[1]
        elif lr == 4:   r1s           = rs[1]
        elif lr == 5:   rAs, rBs      = rs[1], rs[2]
        elif lr == 6:   rAs, rBs, r1s = rs[1], rs[2], rs[3]
        r0s.append(self.fmtR0(a, ca, b, cb, w, k, i, j))
        r2s.append(self.fmtR2(a, ca, b, cb, u, k, i, j)) # if u >= 9 else None
        r3s.append(self.fmtR3(a, ca, b, cb, u, k, i, j))
        r1s.append(self.fmtR1(a, ca, b, cb, u, k, i, j))    if lr in (4, 6)    else None
        self.fmtRABs(a, ca, b, cb, w, rAs, rBs) if lr in (2, 5, 6) else None
#        if   lr == 2:   return      rAs, rBs
#        if   lr == 4:   return r0s,           r1s, r2s, r3s
#        if   lr == 5:   return r0s, rAs, rBs,      r2s, r3s
#        if   lr == 6:   return r0s, rAs, rBs, r1s, r2s, r3s
        return r0s, rAs, rBs, r1s, r2s, r3s
    ####################################################################################################################################################################################################
    def fmtRABs(self, a, ca, b, cb, w, rAs, rBs):
        pa = a ** abs(ca)      ;   pb = b ** abs(cb)  ;   dbg = 0 #  ;   p = 2 ** k if k else 1
        if pb > pa:   a, b = b, a  ;  ca, cb = cb, ca
        rAs.append(self.fmtRA(a, ca, w))
        rBs.append(self.fmtRB(b, cb, w))
        slog(f'{a:2} {ca:2} {b:2} {cb:2}') if dbg else None

    @staticmethod
    def fmtR0(a, ca, b, cb, w, k, i=None, j=None):
        p = 2 ** k if k else 1   ;   dbg = 0
        pfx = f'{i:4} {j:4} ' if i is not None and j is not None else Z
        if k is None:     pa = a ** abs(ca)   ;   pb = b ** abs(cb)   ;   v = pa/pb   if pa >= pb else pb/pa   ;   k = utl.NONE
        else:             pa = a ** ca        ;   pb = b ** cb        ;   v = p*pa*pb
        if w >= 9:        ret = f'{v:^{w}.{w-4}f}' if ist(v, float) else f'{v:^{w}}'
        else:             ret = f'{v:^{w}.{w-2}f}' if ist(v, float) else f'{v:^{w}}'
        slog(f'{pfx}{k:4} {p:4} : {a:2} {ca:2} {b:2} {cb:2} {ret=}') if dbg else None  ;  return ret
    ####################################################################################################################################################################################################
    @staticmethod
    def fmtR1(a, ca, b, cb, w, k, i=None, j=None):
        pa = a ** abs(ca)  ;  pb = b ** abs(cb)  ;  p = 2 ** abs(k) if k else 1  ;  papbi = f'{p}/{pa*pb}'  ;  ret = Z  ;  dbg = 0
        pfx = f'{i:4} {j:4} ' if i is not None and j is not None else Z
        if   k is None:
            k = utl.NONE  ;  ret = f'{pa:>{w}}/{pb:<{w}}' if pa > pb else f'{pb:>{w}}/{pa:<{w}}' if pb > pa else f'{pa:>{w}}/{pb:<{w}}'
        elif k == 0:
            ret = f'{pa:>{w}}*{pb:<{w}}' if ca >= 0 < cb else f'{pa:>{w}}/{pb:<{w}}' if ca >= 0 >= cb else f'{pb:>{w}}/{pa:<{w}}' if ca < 0 <= cb else f'{papbi:^{2*w+1}}' if ca < 0 > cb else '?#?#?'
        elif k > 0:
            pa = pa * p if ca >= 0 <= cb or ca >= 0 > cb else pa  ;  pb = pb * p if ca < 0 <= cb else pb
            ret = f'{pa:>{w}}*{pb:<{w}}' if ca >= 0 < cb else f'{pa:>{w}}/{pb:<{w}}' if ca >= 0 >= cb else f'{pb:>{w}}/{pa:<{w}}' if ca < 0 <= cb else f'{papbi:^{2*w+1}}' if ca < 0 > cb else '?#?#?'
        elif k < 0:
            if   ca >= 0:  ret = f'{pa*pb:>{w}}/{p:<{w}}'  ;  ret = f'{ret:^{2*w+1}}'
        slog(f'{pfx}{k:4} {p:4} : {a:2} {ca:2} {b:2} {cb:2} {ret=}') if dbg else None  ;  return ret
    ####################################################################################################################################################################################################
    @staticmethod
    def fmtR2(a, ca, b, cb, w, k, i=None, j=None):
        qa = '1' if ca == 0 else f'{a}' if ca == 1 else f'{a}' if ca == -1 else f'{a}^{abs(ca)}'
        qb = '1' if cb == 0 else f'{b}' if cb == 1 else f'{b}' if cb == -1 else f'{b}^{abs(cb)}'
        p = 2 ** abs(k) if k is not None else 1  ;  qaqbi = f'{p}/({qa}*{qb})'  ;  ret = Z  ;  dbg = 0
        pfx = f'{i:4} {j:4} ' if i is not None and j is not None else Z
        if   k is None:
            pa = a ** abs(ca)   ;   qa = f'{a}^{abs(ca)}'
            pb = b ** abs(cb)   ;   qb = f'{b}^{abs(cb)}'
            k = utl.NONE  ;  ret = f'{qa:>{w}}/{qb:<{w}}' if pa > pb else f'{qb:>{w}}/{qa:<{w}}' if pb > pa else f'{qa:>{w}}/{qb:<{w}}'
        elif k == 0:
            ret = f'{qa:>{w}}*{qb:<{w}}' if ca >= 0 < cb else f'{qa:>{w}}/{qb:<{w}}' if ca >= 0 >= cb else f'{qb:>{w}}/{qa:<{w}}' if ca < 0 <= cb else f'{qaqbi:^{2*w+1}}' if ca < 0 > cb else '?#?#?'
        elif k > 0:
            qa = f'{p}*{qa}' if ca >= 0 <= cb or ca >= 0 > cb else qa  ;  qb = f'{p}*{qb}' if ca < 0 <= cb else qb
            ret = f'{qa:>}*{qb:<}' if ca >= 0 < cb else f'{qa:>}/{qb:<}' if ca >= 0 >= cb else f'{qb:>}/{qa:<}' if ca < 0 <= cb else f'{qaqbi}' if ca < 0 > cb else '?#?#?'  ;  ret = f'{ret:^{2*w+1}}'
        elif k < 0:
            if   ca >= 0:  ret = f'{qa:>}*{qb}/{p:<}'  ;  ret = f'{ret:^{2*w+1}}'
        slog(f'{pfx}{k:4} {p:2} : {a:2} {ca:2} {b:2} {cb:2} {ret=}') if dbg else None  ;  return ret
    ####################################################################################################################################################################################################
    def fmtR3(self, a, ca, b, cb, w, k, i=None, j=None):
        p = 2 ** abs(k) if k is not None else 1  ;  sa = f'{a}{self.i2spr(abs(ca))}'  ;  sb = f'{b}{self.i2spr(abs(cb))}'  ;  sasbi = f'1/({sa}*{sb})'  ;  ret = Z  ;  dbg = 0
        pfx = f'{i:4} {j:4} ' if i is not None and j is not None else Z   ;   pa = a ** ca   ;   pb = b ** cb
        if   k is None:
            k = utl.NONE  ;  ret = f'{sa:>{w}}/{sb:<{w}}' if pa > pb else f'{sb:>{w}}/{sa:<{w}}' if pb > pa else f'{sa:>{w}}/{sb:<{w}}'
        elif not k:
            ret = f'{sa:>{w}}*{sb:<{w}}' if ca >= 0 < cb else f'{sa:>{w}}/{sb:<{w}}' if ca >= 0 >= cb else f'{sb:>{w}}/{sa:<{w}}' if ca < 0 <= cb else f'{sasbi:^{2*w+1}}' if ca < 0 > cb else '?#?#?'
        elif k > 0:
            sa = f'{p}*{sa}' if ca >= 0 <= cb or ca >= 0 > cb else sa  ;  sb = f'{p}*{sb}' if ca < 0 <= cb else sb  ;  sasbi = f'{p}/({sa}*{sb})'
            ret = f'{sa:>}*{sb:<}' if ca >= 0 <= cb else f'{sa:>}/{sb:<}' if ca >= 0 > cb else f'{sb:>}/{sa:<}' if ca < 0 <= cb else f'{sasbi}' if ca < 0 > cb else '?#?#?'  ;  ret = f'{ret:^{2*w+1}}'
        elif k < 0:
            if   ca >= 0:  ret = f'{sa:>}*{sb}/{p:<}'  ;  ret = f'{ret:^{2*w+1}}'
        slog(f'{pfx}{k:4} {p:2} : {a:2} {ca:2} {b:2} {cb:2} {ret=}') if dbg else None  ;  return ret
    ####################################################################################################################################################################################################
    @staticmethod
    def fmtRA(a, ca, w=Z):
        pa     =   a ** abs(ca)
        if ist(pa, int):   return f'{pa:^{w}}'
        if ist(w,  int):   return f'{pa:^{w}.{w-4}f}'
        return                    f'{pa:^{w}}'
    @staticmethod
    def fmtRB(b, cb, w=Z):
        pb     =   b ** abs(cb)
        if ist(pb, int):   return f'{pb:^{w}}'
        if ist(w,  int):   return f'{pb:^{w}.{w-4}f}'
        return                    f'{pb:^{w}}'

    def fdvdr(self, a, ca, b, cb):      n = max(len(self.fmtRA(a, ca)), len(self.fmtRB(b, cb)))    ;  return n * '/'
########################################################################################################################################################################################################
########################################################################################################################################################################################################
class OTS(Intonation):
    def __init__(self, n='C', rf=440, ss=V_SOUND, csv=0):
        super().__init__(n=n, rf=rf, ss=ss, csv=csv)
        self.ivalKs = ['P1', 'm2', 'm2', 'M2', 'M2', 'm3', 'm3', 'M3', 'M3', 'P4', 'A3', 'd5', 'A4', 'd6', 'P5', 'm6', 'm6', 'M6', 'M6', 'm7', 'm7', 'M7', 'M7', 'P8']
        self.centKs = [   0,  90,  112,  182,  204,  294,  316,  384,  386,  498,  522,  590,  610,  678,  702,  792,  814,  884,  906,  996,  1018, 1088, 1110, 1200]
        self.set_ck2ikm() # todo this base class method initializes and or sets self.ck2ikm

    def dmpData(self, csv=0): # todo fixme
        self.csv = csv
        slog(f'BGN {self.i=:2} {self.m=:2} {self.rf=} {self.ss=} {self.csv=}', p=0)
#        k = Notes.N2I[self.n] + 48 # + 2
        self.dmpOts()
        slog(f'END {self.i=:2} {self.m=:2} {self.rf=} {self.ss=} {self.csv=}', p=0)

    def dmpOts(self):
        slog(f'BGN Overtone Series {self.i=:2} {self.m=:2} {self.csv=}', p=0)
        uu, ww = 3, '^6'   ;   dd, mm, nn, oo, ff = ('[', Y, Y, Y, 3) if self.csv else ('[', W, Z, '|', 1)
        cs, ds, ns, os, fs, ws = [], [], [], [], [], []   ;   ref = '440A' if self.rf == 440 else '432A'   ;   fr = range(1, 256+1)
        f0    = self.FREFS[0]
        for i in fr:
            f = f0 * i             ;      w = self.w0 / f
            n, n2  = self.f2nPair(f, b=0 if i in (17, 22, 25, 28) else 1, o=0)
            o, o2  = self.f2nPair(f, b=0 if i in (17, 22, 25, 28) else 1, o=1)
            fn = self.norm(f/f0)[0]
            c  = self.r2cents(fn)  ;    d = self.i2dCent(c)
            fs.append(fmtf(f, 6))  ;    ws.append(fmtf(w, 6))  ;    ns.append(f'{n:{uu}}')          ;    os.append(f'{o:{uu}}')          ;    cs.append(fmtf(c, 6))           ;  ds.append(fmtg(d, 6 if d >= 0 else 5))
        fs   = mm.join(fs)         ;    ws = mm.join(ws)       ;    ns = fmtl(ns, w=ww, s=mm, d=Z)  ;    os = fmtl(os, w=ww, s=mm, d=Z)  ;    cs = fmtl(cs, w=ww, s=mm, d=Z)  ;  ds = fmtl(ds, w=ww, s=mm, d=Z)
        ref += f'{nn}[{nn}'        ;  sfxf = f'{mm}]{mm}Hz'    ;  sfxw = f'{mm}]{mm}cm'             ;  sfxc = f'{mm}]{mm}cents'          ;  sfxd = f'{mm}]{mm}dcents'
        pfxn = f'notes{nn}[{nn}'   ;  pfxo = f'nOcts{nn}[{nn}' ;  pfxc = f'cents{nn}[{nn}'          ;  pfxd = f'dcnts{nn}[{nn}'          ;   sfx = f'{mm}]{nn}'
        slog(f'Index{nn}[{nn}{fmtl(list(fr), w=ww, d=Z, s=mm)}{sfx}', p=0, f=ff)
        slog(f'f{ref}{fs}{sfxf}',  p=0, f=ff)
        slog(f'{pfxn}{ns}{sfx}',   p=0, f=ff)
        slog(f'{pfxo}{os}{sfx}',   p=0, f=ff)
        slog(f'{pfxc}{cs}{sfxc}',  p=0, f=ff)
        slog(f'{pfxd}{ds}{sfxd}',  p=0, f=ff)
        slog(f'w{ref}{ws}{sfxw}',  p=0, f=ff)
        slog(f'END Overtone Series {self.i=:2} {self.m=:2} {self.csv=}', p=0)
########################################################################################################################################################################################################
########################################################################################################################################################################################################
#def fmtR0_PTH(a, ca, b, cb, w):   pa, pb =   float(a ** ca) ,   float(b ** cb)   ;  return f'{pa/pb:^{w}.{w-4}f}'
#def fmtR1_PTH(a, ca, b, cb, w):   pa, pb =   a ** ca        ,   b ** cb          ;  return f'{pa:>{w}}/{pb:<{w}}' # if ist(pa, int) else f'{pa:>{w}.{w-4}}/{pb:<{w}.{w-4}f}'
#def fmtRA_PTH(a, ca, w=Z):        pa     =   a ** ca                             ;  return f'{pa:^{w}}' if ist(pa, int) else f'{pa:^{w}.{w-4}f}'
#def fmtRB_PTH(b, cb, w=Z):        pb     =   b ** cb                             ;  return f'{pb:^{w}}' if ist(pb, int) else f'{pb:^{w}.{w-4}f}'
#def fmtR2_PTH(a, ca, b, cb, w):   qa, qb = f'{a}^{ca}'      , f'{b}^{cb}'        ;  return f'{qa:>{w}}/{qb:<{w}}'
#def fmtR3_PTH(a, ca, b, cb, w):   sa, sb = f'{a}{i2spr(ca)}', f'{b}{i2spr(cb)}'  ;  return f'{sa:>{w}}/{sb:<{w}}'
#def fdvdr_PTH(a, ca, b, cb):      n = max(len(fmtRA_PTH(a, ca)), len(fmtRB_PTH(b, cb)))  ;  return n * '/'

#def NEW_addFmtRs_PTH(a, ca, b, cb, rs, u=4, w=9):
#    assert rs and ist(rs, list),  f'{rs=} {type(rs)=} {a=} {ca} {b} {cb} {u=} {w=}'   ;   lr = len(rs)
##    r0s, r2s, r3s = [], [], []   ;   r1s = [] if lr == 4 else None   ;   rAs = [] if lr == 5 else None   ;   rBs = [] if lr == 5 else None
#    r0s, r2s, r3s = rs[0], rs[-2], rs[-1] #         ;   r1s, rAs, rBs = None, None, None
#    r1s, rAs, rBs = None,  None,   None
#    if   lr == 4:       r1s      = rs[1]           ;   r1s.append(fmtR1_PTH(a, ca, b, cb, u))
#    elif lr == 5:       rAs, rBs = rs[1], rs[2]    ;   rAs.append(fmtRA_PTH(a, ca, w))    ;    rBs.append(fmtRB_PTH(b, cb, w)) # if ist(b**cb, int) else w3))
#    r0s.append(fmtR0_PTH(a, ca, b, cb, w))
#    r2s.append(fmtR2_PTH(a, ca, b, cb, u)) # if u >= 9 else None
#    r3s.append(fmtR3_PTH(a, ca, b, cb, u))
#    if   lr == 4:   return r0s, r1s,      r2s, r3s
#    elif lr == 5:   return r0s, rAs, rBs, r2s, r3s
########################################################################################################################################################################################################
########################################################################################################################################################################################################
#def addFmtRs(a, ca, b, cb, rs, u=4, w=9, k=None, i=None, j=None):
#    assert rs and ist(rs, list),  f'{rs=} {type(rs)=} {a=} {ca} {b} {cb} {u=} {w=}'   ;   lr = len(rs)
#    r0s, r2s, r3s = rs[0], rs[-2], rs[-1]          ;   r1s, rAs, rBs = None, None, None
#    if   lr == 4:       r1s      = rs[1]           ;   r1s.append(fmtR1(a, ca, b, cb, u, k, i, j))
#    elif lr == 5:       rAs, rBs = rs[1], rs[2]    ;   rAs.append(fmtRA(a, ca, w))    ;    rBs.append(fmtRB(b, cb, w)) # if ist(b**cb, int) else w3))
#    r0s.append(fmtR0(a, ca, b, cb, w, k, i, j))
#    r2s.append(fmtR2(a, ca, b, cb, u, k, i, j)) # if u >= 9 else None
#    r3s.append(fmtR3(a, ca, b, cb, u, k, i, j))
#    if   lr == 4:   return r0s, r1s,      r2s, r3s
#    elif lr == 5:   return r0s, rAs, rBs, r2s, r3s
########################################################################################################################################################################################################
#def fmtR0(a, ca, b, cb, w, k, i=None, j=None):
#    pa = a ** ca   ;   pb = b ** cb   ;   p = 2 ** k if k else 1   ;   dbg = 0
#    pfx = f'{i:4} {j:4} ' if i is not None and j is not None else Z
#    if k is None:     v = pa/pb       ;   k = utl.NONE
#    else:             v = p*pa*pb
#    ret = f'{v:^{w}.{w-4}f}' if ist(v, float) else f'{v:^{w}}'
#    slog(f'{pfx}{k:4} {p:4} : {a:2} {ca:2} {b:2} {cb:2} {ret=}') if dbg else None  ;  return ret
########################################################################################################################################################################################################
#def fmtR1(a, ca, b, cb, w, k, i=None, j=None):
#    pa = a ** abs(ca)  ;  pb = b ** abs(cb)  ;  p = 2 ** abs(k) if k else 1  ;  papbi = f'{p}/{pa*pb}'  ;  ret = Z  ;  dbg = 0
#    pfx = f'{i:4} {j:4} ' if i is not None and j is not None else Z
#    if   k is None:
#        ret = f'{pa:>{w}}/{pb:<{w}}'   ;   k = utl.NONE
#    elif k == 0:
#        ret = f'{pa:>{w}}*{pb:<{w}}' if ca >= 0 < cb else f'{pa:>{w}}/{pb:<{w}}' if ca >= 0 >= cb else f'{pb:>{w}}/{pa:<{w}}' if ca < 0 <= cb else f'{papbi:^{2*w+1}}' if ca < 0 > cb else f'?#?#?'
#    elif k > 0:
#        pa = pa * p if ca >= 0 <= cb or ca >= 0 > cb else pa  ;  pb = pb * p if ca < 0 <= cb else pb
#        ret = f'{pa:>{w}}*{pb:<{w}}' if ca >= 0 < cb else f'{pa:>{w}}/{pb:<{w}}' if ca >= 0 >= cb else f'{pb:>{w}}/{pa:<{w}}' if ca < 0 <= cb else f'{papbi:^{2*w+1}}' if ca < 0 > cb else f'?#?#?'
#    elif k < 0:
#        if   ca >= 0:  ret = f'{pa*pb:>{w}}/{p:<{w}}'  ;  ret = f'{ret:^{2*w+1}}'
#    slog(f'{pfx}{k:4} {p:4} : {a:2} {ca:2} {b:2} {cb:2} {ret=}') if dbg else None  ;  return ret
########################################################################################################################################################################################################
#def fmtR2(a, ca, b, cb, w, k, i=None, j=None):
#    qa = '1' if ca == 0 else f'{a}' if ca == 1 else f'{a}' if ca == -1 else f'{a}^{abs(ca)}'
#    qb = '1' if cb == 0 else f'{b}' if cb == 1 else f'{b}' if cb == -1 else f'{b}^{abs(cb)}'
#    p = 2 ** abs(k) if k is not None else 1  ;  qaqbi = f'{p}/({qa}*{qb})'  ;  ret = Z  ;  dbg = 0
#    pfx = f'{i:4} {j:4} ' if i is not None and j is not None else Z
#    if   k is None:
#        qa  = f'{a}^{ca}'   ;    qb = f'{b}^{cb}'
#        ret = f'{qa:>{w}}/{qb:<{w}}'   ;   k = utl.NONE
#    elif k == 0:
#        ret = f'{qa:>{w}}*{qb:<{w}}' if ca >= 0 < cb else f'{qa:>{w}}/{qb:<{w}}' if ca >= 0 >= cb else f'{qb:>{w}}/{qa:<{w}}' if ca < 0 <= cb else f'{qaqbi:^{2*w+1}}' if ca < 0 > cb else f'?#?#?'
#    elif k > 0:
#        qa = f'{p}*{qa}' if ca >= 0 <= cb or ca >= 0 > cb else qa  ;  qb = f'{p}*{qb}' if ca < 0 <= cb else qb
#        ret = f'{qa:>}*{qb:<}' if ca >= 0 < cb else f'{qa:>}/{qb:<}' if ca >= 0 >= cb else f'{qb:>}/{qa:<}' if ca < 0 <= cb else f'{qaqbi}' if ca < 0 > cb else f'?#?#?'  ;  ret = f'{ret:^{2*w+1}}'
#    elif k < 0:
#        if   ca >= 0:  ret = f'{qa:>}*{qb}/{p:<}'  ;  ret = f'{ret:^{2*w+1}}'
#    slog(f'{pfx}{k:4} {p:2} : {a:2} {ca:2} {b:2} {cb:2} {ret=}') if dbg else None  ;  return ret
########################################################################################################################################################################################################
#def fmtR3(a, ca, b, cb, w, k, i=None, j=None):
#    p = 2 ** abs(k) if k is not None else 1  ;  sa = f'{a}{i2spr(abs(ca))}'  ;  sb = f'{b}{i2spr(abs(cb))}'  ;  sasbi = f'1/({sa}*{sb})'  ;  ret = Z  ;  dbg = 0
#    pfx = f'{i:4} {j:4} ' if i is not None and j is not None else Z
#    if   k is None:
#        ret = f'{sa:>{w}}/{sb:<{w}}'   ;   k = utl.NONE
#    elif not k:
#        ret = f'{sa:>{w}}*{sb:<{w}}' if ca >= 0 < cb else f'{sa:>{w}}/{sb:<{w}}' if ca >= 0 >= cb else f'{sb:>{w}}/{sa:<{w}}' if ca < 0 <= cb else f'{sasbi:^{2*w+1}}' if ca < 0 > cb else f'?#?#?'
#    elif k > 0:
#        sa = f'{p}*{sa}' if ca >= 0 <= cb or ca >= 0 > cb else sa  ;  sb = f'{p}*{sb}' if ca < 0 <= cb else sb  ;  sasbi = f'{p}/({sa}*{sb})'
#        ret = f'{sa:>}*{sb:<}' if ca >= 0 <= cb else f'{sa:>}/{sb:<}' if ca >= 0 > cb else f'{sb:>}/{sa:<}' if ca < 0 <= cb else f'{sasbi}' if ca < 0 > cb else f'?#?#?'  ;  ret = f'{ret:^{2*w+1}}'
#    elif k < 0:
#        if   ca >= 0:  ret = f'{sa:>}*{sb}/{p:<}'  ;  ret = f'{ret:^{2*w+1}}'
#    slog(f'{pfx}{k:4} {p:2} : {a:2} {ca:2} {b:2} {cb:2} {ret=}') if dbg else None  ;  return ret

#def fdvdr(a, ca, b, cb):      n = max(len(fmtRA(a, ca)), len(fmtRB(b, cb)))    ;  return n * '/'
#def fmtRA(a, ca, w=Z):        pa     =   a ** ca                               ;  return f'{pa:^{w}}' if ist(pa, int) else f'{pa:^{w}.{w-4}f}'
#def fmtRB(b, cb, w=Z):        pb     =   b ** cb                               ;  return f'{pb:^{w}}' if ist(pb, int) else f'{pb:^{w}.{w-4}f}'
########################################################################################################################################################################################################
########################################################################################################################################################################################################
#def NEW_addFmtRs_JST(a, ca, b, cb, rs, u=4, w=9, k=None, i=None, j=None):
#    assert rs and ist(rs, list),  f'{rs=} {type(rs)=} {a=} {ca} {b} {cb} {u=} {w=}'   ;   lr = len(rs)
##    r0s, r2s, r3s = [], [], []   ;   r1s = [] if lr == 4 else None   ;   rAs = [] if lr == 5 else None   ;   rBs = [] if lr == 5 else None
#    r0s, r2s, r3s = rs[0], rs[-2], rs[-1] #         ;   r1s, rAs, rBs = None, None, None
#    r1s, rAs, rBs = None,  None,   None
#    if   lr == 4:       r1s      = rs[1]           ;   r1s.append(fmtR1_JST(a, ca, b, cb, u, k, i, j))
#    elif lr == 5:       rAs, rBs = rs[1], rs[2]    ;   rAs.append(fmtRA_JST(a, ca, w))    ;    rBs.append(fmtRB_JST(b, cb, w)) # if ist(b**cb, int) else w3))
#    r0s.append(fmtR0_JST(a, ca, b, cb, w, k))
#    r2s.append(fmtR2_JST(a, ca, b, cb, u, k, i, j)) # if u >= 9 else None
#    r3s.append(fmtR3_JST(a, ca, b, cb, u, k, i, j))
#    if   lr == 4:   return r0s, r1s,      r2s, r3s
#    elif lr == 5:   return r0s, rAs, rBs, r2s, r3s

#def fmtRA_JST(a, ca, w=Z):        pa     =   a ** ca                             ;  return f'{pa:{w}}'
#def fmtRB_JST(b, cb, w=Z):        pb     =   b ** cb                             ;  return f'{pb:{w}}'
#def fdvdr_JST(a, ca, b, cb):      n = max(len(fmtRA_JST(a, ca)), len(fmtRB_JST(b, cb)))  ;  return n * '/'
#def fmtR0_JST(a, ca, b, cb, w, k=0): # w=11
#    pa = a ** ca  ;  pb = b ** abs(cb)  ;  p = 2 ** k if k is not None else 1
#    v = p*pa/pb if cb < 0 else p*pa*pb
#    return f'{v:^{w}.{w-4}f}' if ist(v, float) else f'{v:^{w}}'
########################################################################################################################################################################################################
#def fmtR1_JST(a, ca, b, cb, w, k, i, j):
#    pa = a ** abs(ca)  ;  pb = b ** abs(cb)  ;  l = 2 ** abs(k) if k else None  ;  papbi = f'{l}/{pa*pb}'  ;  ret = Z  ;  dbg = 0
#    if   not k:
#        ret = f'{pa:>{w}}*{pb:<{w}}' if ca >= 0 < cb else f'{pa:>{w}}/{pb:<{w}}' if ca >= 0 >= cb else f'{pb:>{w}}/{pa:<{w}}' if ca < 0 <= cb else f'{papbi:^{2*w+1}}' if ca < 0 > cb else f'?#?#?'
#    elif k > 0:
#        pa = pa * l if ca >= 0 <= cb or ca >= 0 > cb else pa  ;  pb = pb * l if ca < 0 <= cb else pb
#        ret = f'{pa:>{w}}*{pb:<{w}}' if ca >= 0 < cb else f'{pa:>{w}}/{pb:<{w}}' if ca >= 0 >= cb else f'{pb:>{w}}/{pa:<{w}}' if ca < 0 <= cb else f'{papbi:^{2*w+1}}' if ca < 0 > cb else f'?#?#?'
#    elif k < 0:
#        if   ca >= 0:  ret = f'{pa*pb:>{w}}/{l:<{w}}'  ;  ret = f'{ret:^{2*w+1}}'
#    slog(f'{i} {j} {k:2} {l:2} {a} {ca:2} {b} {cb:2} {ret=}') if dbg else None  ;  return ret
########################################################################################################################################################################################################
#def fmtR2_JST(a, ca, b, cb, w, k, i, j):
#    qa = f'1' if ca == 0 else f'{a}' if ca == 1 else f'{a}' if ca == -1 else f'{a}^{abs(ca)}'
#    qb = f'1' if cb == 0 else f'{b}' if cb == 1 else f'{b}' if cb == -1 else f'{b}^{abs(cb)}'
#    l = 2 ** abs(k) if k is not None else 1  ;  qaqbi = f'{l}/({qa}*{qb})'  ;  ret = Z  ;  dbg = 0
#    if   not k:
#        ret = f'{qa:>{w}}*{qb:<{w}}' if ca >= 0 < cb else f'{qa:>{w}}/{qb:<{w}}' if ca >= 0 >= cb else f'{qb:>{w}}/{qa:<{w}}' if ca < 0 <= cb else f'{qaqbi:^{2*w+1}}' if ca < 0 > cb else f'?#?#?'
#    elif k > 0:
#        qa = f'{l}*{qa}' if ca >= 0 <= cb or ca >= 0 > cb else qa  ;  qb = f'{l}*{qb}' if ca < 0 <= cb else qb
#        ret = f'{qa:>}*{qb:<}' if ca >= 0 < cb else f'{qa:>}/{qb:<}' if ca >= 0 >= cb else f'{qb:>}/{qa:<}' if ca < 0 <= cb else f'{qaqbi}' if ca < 0 > cb else f'?#?#?'  ;  ret = f'{ret:^{2*w+1}}'
#    elif k < 0:
#        if   ca >= 0:  ret = f'{qa:>}*{qb}/{l:<}'  ;  ret = f'{ret:^{2*w+1}}'
#    slog(f'{i} {j} {k:2} {l:2} {a} {ca:2} {b} {cb:2} {ret=}') if dbg else None  ;  return ret
########################################################################################################################################################################################################
#def fmtR3_JST(a, ca, b, cb, w, k, i, j):
#    l = 2 ** abs(k) if k is not None else 1  ;  sa = f'{a}{i2spr(abs(ca))}'  ;  sb = f'{b}{i2spr(abs(cb))}'  ;  sasbi = f'1/({sa}*{sb})'  ;  ret = Z  ;  dbg = 0
#    if   not k:
#        ret = f'{sa:>{w}}*{sb:<{w}}' if ca >= 0 < cb else f'{sa:>{w}}/{sb:<{w}}' if ca >= 0 >= cb else f'{sb:>{w}}/{sa:<{w}}' if ca < 0 <= cb else f'{sasbi:^{2*w+1}}' if ca < 0 > cb else f'?#?#?'
#    elif k > 0:
#        sa = f'{l}*{sa}' if ca >= 0 <= cb or ca >= 0 > cb else sa  ;  sb = f'{l}*{sb}' if ca < 0 <= cb else sb  ;  sasbi = f'{l}/({sa}*{sb})'
#        ret = f'{sa:>}*{sb:<}' if ca >= 0 <= cb else f'{sa:>}/{sb:<}' if ca >= 0 > cb else f'{sb:>}/{sa:<}' if ca < 0 <= cb else f'{sasbi}' if ca < 0 > cb else f'?#?#?'  ;  ret = f'{ret:^{2*w+1}}'
#    elif k < 0:
#        if   ca >= 0:  ret = f'{sa:>}*{sb}/{l:<}'  ;  ret = f'{ret:^{2*w+1}}'
#    slog(f'{i} {j} {k:2} {l:2} {a} {ca:2} {b} {cb:2} {ret=}') if dbg else None  ;  return ret
########################################################################################################################################################################################################
#def fmtR0(a, ca, b, cb, w):   pa, pb =   float(a ** ca) ,   float(b ** cb)   ;  return f'{pa/pb:{w}}'
#def fmtR1(a, ca, b, cb, w):   pa, pb =   a ** ca        ,   b ** cb          ;  return f'{pa:>{w}}/{pb:<{w}}'
#def fmtRA(a, ca, w=Z):        pa     =   a ** ca                             ;  return f'{pa:{w}}'
#def fmtRB(b, cb, w=Z):        pb     =   b ** cb                             ;  return f'{pb:{w}}'
#def fmtR2(a, ca, b, cb, w):   qa, qb = f'{a}^{ca}'      , f'{b}^{cb}'        ;  return f'{qa:>{w}}/{qb:<{w}}'
#def fmtR3(a, ca, b, cb, w):   sa, sb = f'{a}{i2spr(ca)}', f'{b}{i2spr(cb)}'  ;  return f'{sa:>{w}}/{sb:<{w}}'
#def fdvdr(a, ca, b, cb):      n = max(len(fmtRA(a, ca)), len(fmtRB(b, cb)))  ;  return n * '/'

#def addFmtRs(r0s, rAs, rBs, r2s, r3s, a, ca, b, cb, w3, ww, u): # u=4 w3='^9.5f' ww='^9'
#    r0s.append(fmtR0(a, ca, b, cb, w3))
#    rAs.append(fmtRA(a, ca, ww if ist(a**ca, int) else w3))
#    rBs.append(fmtRB(b, cb, ww if ist(b**cb, int) else w3))
#    r2s.append(fmtR2(a, ca, b, cb, u)) # if u >= 9 else None
#    r3s.append(fmtR3(a, ca, b, cb, u))
########################################################################################################################################################################################################
########################################################################################################################################################################################################
'''
    k:          0             1             2             3             4             5             6             7             8             9            10            11            12       #  1   2   3   4   5   6   7   8   9   10   11
 0 51: E♭      1/1        2187/2048        9/8       19683/16384      81/64     177147/131072    729/512         3/2        6561/4096       27/16      59049/32768     243/128         2/1      # 2k     19k      .2M          6k      59k
 1 58: B♭      1/1        2187/2048        9/8       19683/16384      81/64          4/3         729/512         3/2        6561/4096       27/16      59049/32768     243/128         2/1      # 2k     19k                   6k      59k
 2 53: F       1/1        2187/2048        9/8       19683/16384      81/64          4/3         729/512         3/2        6561/4096       27/16         16/9         243/128         2/1      # 2k     19k                   6k
 3 60: C       1/1        2187/2048        9/8          32/27         81/64          4/3         729/512         3/2        6561/4096       27/16         16/9         243/128         2/1      # 2k                           6k
 4 55: G       1/1        2187/2048        9/8          32/27         81/64          4/3         729/512         3/2         128/81         27/16         16/9         243/128         2/1      # 2k
 5 50: D       1/1         256/243         9/8          32/27         81/64          4/3         729/512         3/2         128/81         27/16         16/9         243/128         2/1      # 243 9/8 /27 81/ 4/3 512 3/2 /81 27/  /9  243
 6 57: A       1/1         256/243         9/8          32/27         81/64          4/3        1024/729         3/2         128/81         27/16         16/9         243/128         2/1      #                      1k
 7 52: E       1/1         256/243         9/8          32/27         81/64          4/3        1024/729         3/2         128/81         27/16         16/9        4096/2187        2/1      #                      1k                   2k
 8 59: B       1/1         256/243         9/8          32/27       8192/6561        4/3        1024/729         3/2         128/81         27/16         16/9        4096/2187        2/1      #              6k      1k                   2k
 9 54: F♯      1/1         256/243         9/8          32/27       8192/6561        4/3        1024/729         3/2         128/81      32768/19683      16/9        4096/2187        2/1      #              6k      1k         19k       2k
10 61: C♯      1/1         256/243     65536/59049      32/27       8192/6561        4/3        1024/729         3/2         128/81      32768/19683      16/9        4096/2187        2/1      #     59k      6k      1k         19k       2k
11 56: G♯      1/1         256/243     65536/59049      32/27       8192/6561        4/3        1024/729    262144/177147    128/81      32768/19683      16/9        4096/2187        2/1      #     59k      6k      1k .2M     19k       2k
    k:          0             1             2             3             4             5             6             7             8             9            10            11            12       #  1   2   3   4   5   6   7   8   9   10   11
 0 51: E♭       0            114           204           318           408           522           612           702           816           906          1020          1110          1200      # 114     318     522         816     1020
 1 58: B♭       0            114           204           318           408           498           612           702           816           906          1020          1110          1200      # 114     318                 816     1020
 2 53: F        0            114           204           318           408           498           612           702           816           906           996          1110          1200      # 114     318                 816
 3 60: C        0            114           204           294           408           498           612           702           816           906           996          1110          1200      # 114                         816
 4 55: G        0            114           204           294           408           498           612           702           792           906           996          1110          1200      # 114
 5 50: D        0            90            204           294           408           498           612           702           792           906           996          1110          1200      #  90 204 294 408 498 612 702 792 906 996  1110
 6 57: A        0            90            204           294           408           498           588           702           792           906           996          1110          1200      #                     588
 7 52: E        0            90            204           294           408           498           588           702           792           906           996          1086          1200      #                     588                  1086
 8 59: B        0            90            204           294           384           498           588           702           792           906           996          1086          1200      #             384     588                  1086
 9 54: F♯       0            90            204           294           384           498           588           702           792           882           996          1086          1200      #             384     588         882      1086
10 61: C♯       0            90            180           294           384           498           588           702           792           882           996          1086          1200      #     180     384     588         882      1086
11 56: G♯       0            90            180           294           384           498           588           678           792           882           996          1086          1200      #     180     384     588 678     882      1086
    k:          0             1             2             3             4             5             6             7             8             9            10            11            12       #  1   2   3   4   5   6   7   8   9   10   11
'''
