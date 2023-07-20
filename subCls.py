#__all__ = ['tabsC', 'util', 'chord']
#UNICODE     = 1
#import random
F                = f'{0x266D :c}' # Flat
N                = f'{0x266E :c}' # Natural
S                = f'{0x266F :c}' # Sharp

class Note(object):
    def __init__(self, name, accd=0):
        self.name = name
        self.accd = accd
    def query(self):
        a = self.accd
        acd = 'b' if a == -1 else '#' if a == 1 else ''
        return self.name + acd

class UnicodeNote(Note):
    def __init__(self, name, accd=0):
        super().__init__(name, accd)
    def query(self):
        a = self.accd
        acd = f'{F}' if a == -1 else f'{S}' if a == 1 else f'{N}' if a == 0 else ''
        return self.name + acd

if __name__ == '__main__':
    cn = Note('C')
    cu = UnicodeNote('C')
    print(f'{cn.query()}')
    print(f'{cu.query()}')

    csn = Note('C', 1)
    csu = UnicodeNote('C', 1)
    print(f'{csn.query()}')
    print(f'{csu.query()}')

    cnn = Note('C', 0)
    cnu = UnicodeNote('C', 0)
    print(f'{cnn.query()}')
    print(f'{cnu.query()}')

    cbn = Note('C', -1)
    cbu = UnicodeNote('C', -1)
    print(f'{cbn.query()}')
    print(f'{cbu.query()}')
