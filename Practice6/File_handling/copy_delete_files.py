import shutil
import os
shutil.copy("Practice6/File_handling/data.txt", "Practice6/File_handling/file.txt")


if os.path.exists("Practice6/File_handling/file.txt"):
    os.remove("Practice6/File_handling/file.txt")