import re

string = ["aa","Ab","abbb","Aaabbb","abbbbbb","Abb"]
for s in string:
    result = re.findall("a.*b",s)
    print(result)