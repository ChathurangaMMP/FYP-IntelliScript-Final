# import os

# files_count = {"folders": 0}

# main_folder = "cbsl-data"
# main_folder_dirs = os.listdir(main_folder)

# for main_dir in main_folder_dirs:
#     if os.path.isdir(f"{main_folder}/{main_dir}"):
#         files_count["folders"] += 1

#     if os.path.isfile(f"{main_folder}/{main_dir}"):
#         file_name, file_extension = os.path.splitext(
#             f"{main_folder}/{main_dir}")

#         if file_extension not in files_count:
#             files_count[file_extension] = 0

#         files_count[file_extension] += 1

import os

pdfs = 0
images = 0
textfiles = 0
docs = 0
excels = 0

for root, dirs, files in os.walk('cbsl-data/'):
    for file in files:
        if file.endswith(".pdf"):
            pdfs += 1
        elif file.endswith(".docx"):
            docs += 1
        elif file.endswith(".xlsx") or file.endswith(".csv") or file.endswith(".xls"):
            excels += 1
        elif file.endswith(".txt"):
            textfiles += 1
        elif file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".png"):
            pdfs += 1
        else:
            print(file)

print(pdfs, images, textfiles, docs, excels)
