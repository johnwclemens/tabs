from tpkg.notes import Notes as Notes

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
# T: text styles, transpose
# U: undo/redo, unicode
# V: views, visible
# W: window
# X:
# Y:
# Z:

#fixme list:
# A) all pages visible on startup despite all but one set to False
#  1) only create pages as needed - saves memory and layout time - but not so clear how to impl?
#  2) cycle through all the pages - works in sito by side effect = probably not a real solution?
# B) pages in some cases do not display keystrokes interactively!
# C) various tab movements are incorrect
#  1) space/backspace
#  2) top/bottom string automove
# D) fix BACKSPACE - pass motion value as seperate arg to SetTabCmd
# E) how to sort cmds.py classes
