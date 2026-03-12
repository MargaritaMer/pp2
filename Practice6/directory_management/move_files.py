import os
items = os.listdir("project")
for item in items:
    print(item)

files = os.listdir()
for file in files:
    if file.endswith(".py"):
        print(file)


import shutil

os.makedirs("Practice6/project/data/files", exist_ok=True)

if os.path.exists("Practice6/directory_management/test.txt"):
    shutil.copy(
        "Practice6/directory_management/test.txt",
        "Practice6/project/data/files/test.txt"
    )
else:
    print("File not found")
