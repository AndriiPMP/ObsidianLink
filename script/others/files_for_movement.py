import os
from dotenv import load_dotenv


load_dotenv()

TASK = """Analyze the contents and subject of the sort, then from the entire
    list of folders provided, select the exact directory
    in which the file should be located. Once you've selected the correct
    directory, copy it into your answer, word for word, character for character.
    If you think that none of the given paths suits you, just answer this: C:\\Users\\gote2\\Desktop\\План\\Промежуточный материал\\На переработку"""

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

    files_data  = []

    for path in paths:
        
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        files_data.append({
            "path": path,
            "content": content,
        })

    return files_data

def get_sort_files() -> list[str]:

    sort_dir = os.getenv("SORT_DIR")

    if not sort_dir or not os.path.isdir(sort_dir):
        return []

    paths = []
    for root, _, files in os.walk(sort_dir):
        for name in files:
            paths.append(os.path.join(root, name))

    return paths


def build_payloads():
    folders = get_folder_paths()
    payloads = []

    for item in get_files_sort_content():
        payloads.append({
            "path": item["path"],
            "task": TASK,
            "folders": folders,
            "sort": item["content"],
        })

    return payloads