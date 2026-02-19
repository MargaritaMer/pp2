import math
n=int(input())
l=int(input())

s = (n * l * l) / (4 * math.tan(math.pi / n))
print ("area",s)