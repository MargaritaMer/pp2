import re

string = ["a_a","ab","ab_bb","aaabbb","abbb_bbb","abb"]
for s in string:           
    result = re.findall("[a-z]+_[a-z]+", s)
    print(result)