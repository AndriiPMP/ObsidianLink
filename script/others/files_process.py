import os
from dotenv import load_dotenv 

load_dotenv()


def get_file_paths():   

    target_dir = os.getenv("TARGET_DIR")

    file_paths = []                      

    for root, directories, files in os.walk(target_dir):   

        for filename in files:                                     
            filepath = os.path.join(root, filename)                
            file_paths.append(filepath)        

    return file_paths  


def format_paths(existing_paths, base_dir):

    formated_paths = [] 

    for path in existing_paths:
        rel_path = os.path.relpath(path, base_dir)
        formated_paths.append(rel_path)

    return formated_paths

def get_files_content(paths):

    contents=[]

    for path in paths:
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            contents.append(content)

        except Exception as e:
            print(f"Не удалось прочитать {path}: {e}")

    return contents

def get_files_data():

    base_dir = os.getenv("BASE_DIR")

    file_paths = get_file_paths()

    formated_paths = format_paths(file_paths, base_dir)
    
    contents = get_files_content(file_paths)

    return [
        {"path": p, "formated_path": fp, "content": c}
        for p, fp, c in zip(file_paths, formated_paths, contents)     
    ]



    