import re
pattern = r"ab{2,3}"
string = ["aa","ab","abbb","aaabbb","abbbbbb","abb"]

for s in string:
    if re.fullmatch(pattern,s):
        print(f"{s} -> match")
    else:
        print(f"{s} -> no match")