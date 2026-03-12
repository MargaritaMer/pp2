names = ["Tom","Anna","Bob"]
age = [17, 18, 16]

for index, name in enumerate(names):
    print (index, name)

for name,ag in zip(names,age):
    print (name,ag)

x = "10"
print("Type",type(x))

x = int(x)
print("Type",type(x))
