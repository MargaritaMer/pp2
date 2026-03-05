import re

string = ["aa","Ab","AaBbBb","AaBbB","AbbBbbb","abb"]

for s in string:
    result = re.sub(r'(?<!^)([A-Z])', r' \1', s)
    print(result)