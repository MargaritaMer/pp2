with open("Practice5/raw.txt", "r", encoding="utf-8") as f:
    text = f.read()
pattern = r"\d+\.\n(.+?)\n([\d, ]+) x ([\d, ]+)\n([\d, ]+)"
import re

matches = re.findall(pattern, text)

for item in matches:
    name = item[0]
    quantity = item[1]
    price = item[2]
    total = item[3]

    print("Название:", name)
    print("Количество:", quantity)
    print("Цена:", price)
    print("Сумма:", total)
    print("-" * 40)