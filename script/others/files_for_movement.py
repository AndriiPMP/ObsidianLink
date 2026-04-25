import os
from dotenv import load_dotenv


load_dotenv()

def get_folder_paths():
    
    target_dir = os.getenv("SORT_DIR")

    folder_paths = []

    for root, directories, files in os.walk(target_dir):

        for directory in directories:
            folder_path = os.path.join(root, directory)
            folder_paths.append(folder_path)

    return folder_paths

def get_files_sort_content():

    paths = get_sort_files()

    contents = []

    for path in paths:
        
        try:
            with open(path, "r", encoding="utf-8") as f:
                    contents.append(f.read())
        except Exception as e:
            print(f"Не удалось прочитать {path}: {e}")

    return contents

def get_sort_files() -> list[str]:

    sort_dir = os.getenv("SORT_DIR")

    if not sort_dir or not os.path.isdir(sort_dir):
        return []

    paths = []
    for root, _, files in os.walk(sort_dir):
        for name in files:
            paths.append(os.path.join(root, name))

    return paths
