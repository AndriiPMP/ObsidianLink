
def process_file(task:dict):
    file_path = task.get("path")
    content = task.get("content")        

    print(f"[PROCESSING] {file_path}")
    print(f"[PROCESSING] {content}")