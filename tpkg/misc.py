from tpkg.notes import Notes

########################################################################################################################################################################################################
class DSymb:
#    SYMBS = {'X': 'mute', '+': 'hammer', '~': 'vibrato', '^': 'tie', '.': 'staccato', '_': 'legato', '%': 'repeat', '|': 'bar', '[': 'groupL', ']': 'groupR'}
    SYMBS = {'X': 'mute', '/': 'slide', '\\': 'bend', '+': 'hammer', '~': 'vibrato', '^': 'tie', '.': 'staccato', '_': 'legato', '%': 'repeat', '|': 'bar', '[': 'groupL', ']': 'groupR'}
########################################################################################################################################################################################################
class Scales:
    MajorIs = [ 0, 2, 4, 5, 7, 9, 11 ]
    @classmethod
    def majIs(cls, i):  return [ (i + j) % Notes.NTONES for j in cls.MajorIs ]
########################################################################################################################################################################################################
class Modes:
    IONIAN, DORIAN, PHRYGIAN, LYDIAN, MIXOLYDIAN, AEOLIAN, LOCRIAN = range(7)
    NAMES = [ 'IONIAN', 'DORIAN', 'PHRYGIAN', 'LYDIAN', 'MIXOLYDIAN', 'AEOLIAN', 'LOCRIAN' ]
    TYPES = [  IONIAN,   DORIAN,   PHRYGIAN,   LYDIAN,   MIXOLYDIAN,   AEOLIAN,   LOCRIAN  ]
########################################################################################################################################################################################################

#todo list:
# A: autosave
# B: blank tabs
# C: chords, colors, consume
# D: data, display level, docs
# E: events, exit
# F: filters
# G:
# H: harmonics, help
# I: itervals
# J:
# K: keyboard mapping, keysigs
# L: logs
# M: modes
# N: notation
# O:
# P: pages, pytest
# Q: log and quit -> assert
# R: row labels, rootless chords
# S: scales, sound, sprites, stdout
# T: text styles, transpose, tunings
# U: undo/redo, unicode
# V: views, visible
# W: window
# X:
# Y:
# Z:

# Pythagorean Intervals:   abcs -> data map1   cents -> data map2 
# Consider c/t current of total counts AND trim 2 spaces at end of hdr (above verses below)
'''
j j*100 i Iv  c  t     k       d       e       c`   Iv  c t     k       d       e       c`
0    0  0 P1  1/12 @    0 :   0.000 = 1.955 *  0    d2  0/0 @   24 :         = 1.955 *  1
1  100  2 m2  1/ 7 @   90 :  -9.780 = 1.955 *  0    A1  0/5 @  114 :         = 1.955 *  1
2  200  4 M2  1/10 @  204 :   3.910 = 1.955 *  0    d3  0/2 @  180 :         = 1.955 *  1
3  300  6 m3  1/ 9 @  294 :  -5.870 = 1.955 *  0    A2  0/3 @  318 :         = 1.955 *  1
4  400  8 M3  1/ 8 @  408 :   7.820 = 1.955 *  0    d4  0/4 @  384 :         = 1.955 *  1
5  500 10 P4  1/11 @  498 :  -1.960 = 1.955 *  0    A3  0/1 @  522 :         = 1.955 *  1
6  600 12 A4  1/ 6 @  612 :  11.730 = 1.955 *  0    d5  0/6 @  588 :         = 1.955 *  1
7  700 14 P5  1/11 @  702 :   1.960 = 1.955 *  0    d6  0/1 @  678 :         = 1.955 *  1
8  800 16 m6  1/ 8 @  792 :  -7.820 = 1.955 *  0    A5  0/4 @  816 :         = 1.955 *  1
9  900 18 M6  1/ 9 @  906 :   5.870 = 1.955 *  0    d7  0/3 @  882 :         = 1.955 *  1
a 1000 20 m7  1/10 @  996 :  -3.910 = 1.955 *  0    A6  0/2 @ 1020 :         = 1.955 *  1
b 1100 22 M7  1/ 7 @ 1110 :   9.780 = 1.955 *  0    d8  0/5 @ 1086 :         = 1.955 *  1
c 1200 24 P8  1/12 @ 1200 :   0.000 = 1.955 *  0    A7  0/0 @ 1178 :         = 1.955 *  1
'''
# pyglet.options['audio'] = ('xaudio2', 'directsound', 'openal', 'pulse', 'silent')
# source = pyglet.media.load('explosion.wav')

#fixme list:
# A) all pages visible on startup despite all but one set to False
#  1) only create pages as needed - saves memory and layout time - but not so clear how to impl?
#  2) cycle through all the pages - works in situ by side effect = probably not a real solution?
# B) pages in some cases do not display keystrokes interactively!
# C) various tab movements are incorrect
#  1) space/backspace
#  2) top/bottom string automove
# D) fix BACKSPACE - pass motion value as seperate arg to SetTabCmd
# E) how to sort cmds.py classes - alphabetically?
# F) load more fonts into res/fonts dir (.ttf files)
# G) fix - Access to a protected member _reinit of a class - tobj._reinit()  _DONE
# H) move on_resize() from tabs.py to evnts.py - super.resize  _DONE
# I) cleanup use of negative j values and abs(j) hack
# J) something fishy with x value in createZZs/resizeZZs()
# K) add 1 vs create 2 - how many zclms?  add can share 1 zclm
# L) consider refactor zclm from zzs to tniks
# M) member vars being set confusing e.g. self.ZZ complex state set mid-stream
# N) cmd refactoring really makes it hard to find code re multiple files - also how to sort cmd code
# O) why create page/line/sect for each zz?
# P) maybe do not call resize() unless its visible
# Q) register snap needs a list
# R) revisit sharps & flats & chord names
# S) multiple lines is broke (only displays last line, others are blank)
# T) still issues with tnik.visible and update/resize? (w/h=0, parent, grp num/ord) only set visible on groups?
# U) Log file creation issues for some time now

######################################################################################################################################################

# Diatonic Inervals:
#  0  1   2   3   4   5   6   7   8   9  10   11   12
# P1 m2  M2  m3  M3  P4  TT  P5  m6  M6  m7   M7   P8
# 0 100 200 300 400 500 600 700 800 900 1000 1100 1200

# C Ionian
# P1 M2 M3 P4 P5 M6 M7 P8
# C  D  E  F  G  A  B  C
# D Dorian
# P1 M2 m3 P4 P5 M6 m7 P8
# D  E  F  G  A  B  C  D
# E Phrygian
# P1 m2 m3 P4 P5 m6 m7 P8
# E  F  G  A  B  C  D  E
# F Lydian
# P1 M2 M3 A4 P5 M6 M7 P8
# F  G  A  B  C  D  E  F
# G Mixolydian
# P1 M2 M3 P4 P5 M6 m7 P8
# G  A  B  C  D  E  F  G
# A Aeolian
# P1 M2 m3 P4 P5 m6 m7 P8
# A  B  C  D  E  F  G  A
# B Lydian
# P1 m2 m3 P4 d5 m6 m7 P8
# B  C  D  E  F  G  A  B

# Pythagorean Inetvals:
#  1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19  20  21   22   23   24
# D   Eb  D#   E  E   F   F   Gb  F#  G   G   Ab  G#  A   A   Bb  A#  B   B   C   C    Db   C#   D
# P1  m2  A1  d3  M2  m3  A2  d4  M3  P4  A3  d5  A4  d6  P5  m6  A5  d7  M6  m7  A6   d8   M7   P8
#  0  90 114 180 204 294 318 384 408 498 522 588 612 678 702 792 816 882 906 996 1020 1086 1110 1200
# 12  7   5   2  10   9   3   4   8   11  1   6   6   1   11  8   4   3   9   10   2    5    7   12

#####################################################################################################

# F Pythagorean Inetvals: F
#  1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19  20  21   22   23   24
# F  GbF#         G  AbG#         A  BbA#     B           C  DbC#         D  EbD#           E    F
# P1  m2  A1  d3  M2  m3  A2  d4  M3  P4  A3  d5  A4  d6  P5  m6  A5  d7  M6  m7  A6   d8   M7   P8
#  0  90 114 180 204 294 318 384 408 498 522 588 612 678 702 792 816 882 906 996 1020 1086 1110 1200
# 12  7   5   2  10   9   3   4   8   11  1   6   6   1   11  8   4   3   9   10   2    5    7   12

# C Pythagorean Inetvals: C
#  1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19  20  21   22   23   24
# C  DbC#     D      EbD#         E   F       Gb  F#      G  AbG#         A  BbA#           B    C
# P1  m2  A1  d3  M2  m3  A2  d4  M3  P4  A3  d5  A4  d6  P5  m6  A5  d7  M6  m7  A6   d8   M7   P8
#  0  90 114 180 204 294 318 384 408 498 522 588 612 678 702 792 816 882 906 996 1020 1086 1110 1200
# 12  7   5   2  10   9   3   4   8   11  1   6   6   1   11  8   4   3   9   10   2    5    7   12

# G Pythagorean Inetvals: G
#  1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19  20  21   22   23   24
# G  AbG#     A      BbA#         B   C       Db  C#      D  EbD#         E   F       GbF#       G
# P1  m2  A1  d3  M2  m3  A2  d4  M3  P4  A3  d5  A4  d6  P5  m6  A5  d7  M6  m7  A6   d8   M7   P8
#  0  90 114 180 204 294 318 384 408 498 522 588 612 678 702 792 816 882 906 996 1020 1086 1110 1200
# 12  7   5   2  10   9   3   4   8   11  1   6   6   1   11  8   4   3   9   10   2    5    7   12

# D Pythagorean Inetvals: D
#  1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19  20  21   22   23   24
# D  EbD#         E   F          GbF# G       Ab  G#      A  BbA#         B   C            DbC#  D
# P1  m2  A1  d3  M2  m3  A2  d4  M3  P4  A3  d5  A4  d6  P5  m6  A5  d7  M6  m7  A6   d8   M7   P8
#  0  90 114 180 204 294 318 384 408 498 522 588 612 678 702 792 816 882 906 996 1020 1086 1110 1200
# 12  7   5   2  10   9   3   4   8   11  1   6   6   1   11  8   4   3   9   10   2    5    7   12

# A Pythagorean Inetvals: A
#  1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19  20  21   22   23   24
# A  BbA#         B   C      DbC#     D       Eb  D#      E   F      GbF#     G       AbG#       A
# P1  m2  A1  d3  M2  m3  A2  d4  M3  P4  A3  d5  A4  d6  P5  m6  A5  d7  M6  m7  A6   d8   M7   P8
#  0  90 114 180 204 294 318 384 408 498 522 588 612 678 702 792 816 882 906 996 1020 1086 1110 1200
# 12  7   5   2  10   9   3   4   8   11  1   6   6   1   11  8   4   3   9   10   2    5    7   12

# E Pythagorean Inetvals: E
#  1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19  20  21   22   23   24
# E   F      GbF#     G      AbG#     A       Bb  A#  B       C      DbC#     D       EbD#       E
# P1  m2  A1  d3  M2  m3  A2  d4  M3  P4  A3  d5  A4  d6  P5  m6  A5  d7  M6  m7  A6   d8   M7   P8
#  0  90 114 180 204 294 318 384 408 498 522 588 612 678 702 792 816 882 906 996 1020 1086 1110 1200
# 12  7   5   2  10   9   3   4   8   11  1   6   6   1   11  8   4   3   9   10   2    5    7   12

# B Pythagorean Inetvals: B
#  1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19  20  21   22   23   24
# B   C      DbC#     D      EbD#         E   F       Gb  F#  G      AbG#     A       BbA#       B
# P1  m2  A1  d3  M2  m3  A2  d4  M3  P4  A3  d5  A4  d6  P5  m6  A5  d7  M6  m7  A6   d8   M7   P8
#  0  90 114 180 204 294 318 384 408 498 522 588 612 678 702 792 816 882 906 996 1020 1086 1110 1200
# 12  7   5   2  10   9   3   4   8   11  1   6   6   1   11  8   4   3   9   10   2    5    7   12

# F# Pythagorean Inetvals: F#
#  1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19  20  21   22   23   24
# F#  G      AbG#     A      BbA#     B       C      DbC#     D       EbD#        E    F         F#
# P1  m2  A1  d3  M2  m3  A2  d4  M3  P4  A3  d5  A4  d6  P5  m6  A5  d7  M6  m7  A6   d8   M7   P8
#  0  90 114 180 204 294 318 384 408 498 522 588 612 678 702 792 816 882 906 996 1020 1086 1110 1200
# 12  7   5   2  10   9   3   4   8   11  1   6   6   1   11  8   4   3   9   10   2    5    7   12


# D  E  F  G  A  B  C# D
# P1 M2 m3 
#
