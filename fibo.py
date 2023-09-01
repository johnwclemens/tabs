import sys
from tpkg import utl as utl

fmtm = utl.fmtm
slog = utl.slog
W    = utl.W

parseCmdLine = utl.parseCmdLine

def fibn(n):    # Fibonacci series less than the value n
    a, b = 0, 1
    slog(f'n={n-1}:', e=W) if n > 1 else None
    while a-2 < n:
#        print(f'{n=}:  {a}', end=' ') if not a else None
        slog(f'{a}', p=0, e=W) if a else None
        a, b = b, a+b
    slog(p=0)

def fibi(i):   # Fibonacci series up to the i'th term
    a, b = 0, 1
    slog(f'i={i-1}:', e=W) if i > 1 else None
    for j in range(i+2): #        print(f'{i=}:  {a}', end=' ') if not a else None
        slog(f'{a}', p=0, e=W) if j else None
        a, b = b, a+b
    slog(p=0)

def main():
    slog(f'{sys.argv=}')
    args = parseCmdLine(sys.argv, f=-1)
    slog(f'{fmtm(args)=}') #   for i in range(int(sys.argv[1])): fibi(i)  ;  fibn(i)
    for i, (k, v) in enumerate(args.items()):
        if  k == 'i' or k == 'n':
            v = int(v[0])
            slog(f'{i=} {k=} {v=}')
            fibi(v) if k == 'i' else fibn(v)

if __name__ == "__main__":
    main()
