import re

string = ["aa","Ab","abbb","Aaabbb","abbbbbb","Abb"]
for s in string:
    result = re.findall("[A-Z][a-z]+",s)
    print(result)