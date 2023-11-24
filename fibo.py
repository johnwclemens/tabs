import sys, time
from tpkg import utl as utl

fmtm = utl.fmtm
slog = utl.slog
W    = utl.W

parseCmdLine = utl.parseCmdLine
    
@utl.timer
#@utl.memorize
def fibn(n):    # Fibonacci series less than the value n
    a, b = 0, 1
    slog(f'n={n-1}:', e=W) if n > 1 else None
    while a-2 < n:
#        print(f'{n=}:  {a}', end=' ') if not a else None
        slog(f'{a}', p=0, e=W) if a else None
        a, b = b, a+b
    slog(p=0)

@utl.timer
#@utl.memorize
def fibi(i):   # Fibonacci series up to the i'th term
    a, b = 0, 1
    slog(f'i={i-1}:', e=W) if i > 1 else None
    for j in range(i+2): #        print(f'{i=}:  {a}', end=' ') if not a else None
        slog(f'{a}', p=0, e=W) if j else None
        a, b = b, a+b
    slog(p=0)

def OLD__main():
    slog(f'{sys.argv=}')
    args = parseCmdLine(sys.argv, f=-1)
    slog(f'{fmtm(args)=}') #   for i in range(int(sys.argv[1])): fibi(i)  ;  fibn(i)
    for i, (k, v) in enumerate(args.items()):
        if  k == 'i' or k == 'n' or k == 'r':
            v = int(v[0])
            slog(f'{i=} {k=} {v=}')
            fibi(v) if k == 'i' else fibn(v) if k == 'n' else fib(v)

@utl.timer
#@utl.memorize
def fib(n):
    if n==0 or n==1: return n
    else:            return fib(n-1) + fib(n-2)

def main():
    args = sys.argv
    a    = int(args[1])
    slog(f'{a=}')
    bgn = time.time()
    fa  = fib(a)
    end = time.time()
    slog(f'{end-bgn:.6f} seconds fib({a})={fa}')

if __name__ == "__main__":
    main()
