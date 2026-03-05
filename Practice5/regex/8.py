import re

string = ["aa","Ab","aBBbb","AaBbB","AbbBbbb","abb"]

for s in string:
    result = re.split(r'(?=[A-Z])', s)
    print(result)