def div(a):
    for i in range(1,a+1):
        if i%3==0 and i%4==0:
            yield i
a = int(input())
print(list(div(a)))