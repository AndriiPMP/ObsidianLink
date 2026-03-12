import os                                                          

target_dir = r"E:\План\IT" # Общие переменные которые будут использоваться внутри функций
base_dir = r"E:\План"

# Функция которая получает полные путя
def get_file_paths(directory):                                     
     file_paths = [] # Тут хранятся пути к файлам                                         
     for root, directories, files in os.walk(directory):            
         for filename in files:                                     
             filepath = os.path.join(root, filename)                
             file_paths.append(filepath)                            
     return file_paths                                               

# Функция которая получает обрезанные путя
def format_paths(existing_paths, base_path):
    formated_paths = [] # Тут хранится масив путей отформатированных для ссылок в Obsidian
    for path in existing_paths:
        rel_path = os.path.relpath(path, base_path)
        formated_paths.append(rel_path)
    return formated_paths

# Функция которая получает содержимое файлов
def get_files_content(file_path_list):
    contents=[]
    for path in file_path_list:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            content.append(content)
        except Exception as e:
            print(f"Не удалось прочитать {path}: {e}")
    return contents

# Функция которая собирает масив
def get_files_data(file_paths_list, formated_path_list, file_content_list):
    files_data = []  # Тут хранится библиотека путей файлов и их содержимого

    for full_path, formated_path, file_content in zip(
        file_paths_list, 
        formated_path_list, 
        file_content_list
        ):
        entry = { # Показываем что мы хотим закинуть в библиотеку
            "path": full_path,
            "formated_path": formated_path,
            "content": file_content
            }
        files_data.append(entry)
    return files_data



    