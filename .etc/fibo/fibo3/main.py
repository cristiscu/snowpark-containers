import sys

# n:    0, 1, 2, 3, 4, 5, 6, 7,  8,  9,  10, 11, 12  ...
# f(n): 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144 ...
def f(n):
    if n < 0: return -1
    elif n <= 1: return n
    elif n == 2: return 1
    else: return f(n-1) + f(n-2)

# logs entered data
def f_log(n):
    ret = f(n)
    with open("logs/log.txt", "a") as myfile:
        myfile.write(f"{n}: {ret}\n")
    return ret
   
if __name__ == '__main__':
    while True:
        n = int(input("n: "))
        if n < 0: break
        f_log(n)
        with open("logs/log.txt", "r") as myfile:
            print(myfile.read())
