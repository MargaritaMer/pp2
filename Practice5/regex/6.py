import re

string = ["aa","A b","abbb","Aa.abbb","abbb,bbb","Abb"]
for s in string:
    result = re.sub("[ ,.]",":",s)
    print(result)