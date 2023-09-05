from tpkg.notes import Notes as Notes

########################################################################################################################################################################################################
class DSymb:
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

# Stuff todo
# A: autosave
# B:
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
# Q:
# R: row labels, rootless chords
# S: scales, sound, sprites, stdout
# T: text styles, transpose
# U: undo/redo, unicode
# V: views, visible
# W: window
# X:
# Y:
# Z:
