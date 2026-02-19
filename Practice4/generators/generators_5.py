def zero(a):
    for i in range(a, -1, -1):
        yield i
        

a = int(input())
print(list(zero(a)))

