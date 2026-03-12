import os                                                          

target_dir = r"E:\План\IT" # Общие переменные которые будут использоваться внутри функций
base_dir = r"E:\План"

# Функция которая получает полные путя
def get_file_paths():    
     file_paths = [] # Тут хранятся пути к файлам                                         
     for root, directories, files in os.walk(target_dir):            
         for filename in files:                                     
             filepath = os.path.join(root, filename)                
             file_paths.append(filepath)                            
     return file_paths                                               

# Функция которая получает обрезанные путя
def format_paths(existing_paths, base_dir):
    existing_paths = get_file_paths()

    formated_paths = [] # Тут хранится масив путей отформатированных для ссылок в Obsidian
    for path in existing_paths:
        rel_path = os.path.relpath(path, base_dir)
        formated_paths.append(rel_path)
    return formated_paths

# Функция которая получает содержимое файлов
def get_files_content():
    contents=[]
    for path in get_file_paths():
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            contents.append(content)
        except Exception as e:
            print(f"Не удалось прочитать {path}: {e}")
    return contents

# Функция которая собирает масив
def get_files_data():
      file_paths = get_file_paths()
      formated_paths = format_paths()
      contents = get_files_content()

      return [
          {"path": p, "formated_path": fp, "content": c}
          for p, fp, c in zip(file_paths, formated_paths, contents)     
      ]



    