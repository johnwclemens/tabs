def fibn(n):    # Fibonacci series less than the value n
    a, b = 0, 1
    print(f'n={n-1}:', end=' ') if n > 1 else None
    while a-2 < n:
#        print(f'{n=}:  {a}', end=' ') if not a else None
        print(a, end=' ') if a else None
        a, b = b, a+b
    print()

def fibi(i):   # Fibonacci series up to the i'th term
    a, b = 0, 1
    print(f'i={i-1}:', end=' ') if i > 1 else None
    for j in range(i+2):
#        print(f'{i=}:  {a}', end=' ') if not a else None
        print(a, end=' ') if j else None
        a, b = b, a+b
    print()

def main():
    for i in range(int(sys.argv[1])):
        fibi(i)
        fibn(i)

if __name__ == "__main__":
    import sys
    main()
