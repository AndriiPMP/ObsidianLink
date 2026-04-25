from script.others.create_backUp import create_backup
from script.others.ai_integr import generate_text
from script.others.files_process import move_file_by_model

def sort_files():
    
    create_backup()

    generate_text()

    move_file_by_model()