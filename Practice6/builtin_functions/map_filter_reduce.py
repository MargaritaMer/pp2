from functools import reduce

nums = [1,2,3,4,5,6,7,8,9,10]

sq = list(map(lambda x:x**2,nums))
print("Squares",sq)

even = list(filter(lambda x: x%2==0,nums))
print("Even",even)

sum = reduce(lambda x,y: x+y, nums)
print ("Sum",sum)