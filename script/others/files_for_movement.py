import os
from dotenv import load_dotenv
import shutil
from pathlib import Path        
from script.others.ai_integr import generate_text   

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

def move_file_by_model():
    model_path = generate_text()

    sort_dir = os.getenv("TARGET_DIR")

    source_path = Path(sort_dir)
    target_dir = Path(model_path)
    target_path = target_dir / source_path.name

    target_path.parent.mkdir(parents=True, exist_ok=True)

    shutil.move(str(source_path), str(target_path))