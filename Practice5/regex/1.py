import re
pattern = r"ab*"
test_strings = ["a", "ab", "abb", "abbbbb", "ac", "ba"]

for s in test_strings:
    if re.fullmatch(pattern, s):
        print(f"{s} → match")
    else:
        print(f"{s} → no match")