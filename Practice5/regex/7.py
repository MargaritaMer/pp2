import re

string = ["aa","A_b","abbb","Aa_abbb","abbb_bbb","Abb"]

def to_camel(self):
    return self.group(1).upper()

for s in string:
    result = re.sub("_(.)", to_camel, s)
    print(result)