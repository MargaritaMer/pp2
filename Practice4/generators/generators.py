def sq(a):
    for i in range(1,a):
        yield i**2
a = int(input())
print(list(sq(a)))

