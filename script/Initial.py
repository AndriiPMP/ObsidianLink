import os                                                          

target_dir = r"E:\План\IT" #общие переменные которые будут использоваться внутри функций
base_dir = r"E:\План"

def get_file_paths(directory):                                     
     file_paths = [] #тут хранятся пути к файлам                                         
     for root, directories, files in os.walk(directory):            
         for filename in files:                                     
             filepath = os.path.join(root, filename)                
             file_paths.append(filepath)                            
     return file_paths                                               

def format_paths(existing_paths, base_path):
    formated_paths = [] #тут хранится масив путей отформатированных для ссылок в Obsidian
    for path in existing_paths:
        rel_path = os.path.relpath(path, base_path)
        formated_paths.append(rel_path)
    return formated_paths


def get_files_data(file_paths_list):
    files_data = []  #тут хранится библиотека путей файлов и их содержимого

    for path in file_paths_list:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()

            entry = {
                "path": path,
                "content": content
            }
            files_data.append(entry)
        except Exception as e:
            print(f"Не удалось прочитать {path}: {e}")
    return files_data

    