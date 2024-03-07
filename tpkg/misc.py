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

# Pythagorean Interval Name -> ratio or cents
# Pythagorean Map2? table

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
# G) fix - Access to a protected member _reinit of a class - tobj._reinit()
# H) move on_resize() from tabs.py to evnts.py - super.resize
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
