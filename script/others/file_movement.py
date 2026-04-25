import shutil
from pathlib import Path        
from script.others.ai_integr import generate_text   

def move_file_by_model():
    
    model_path = generate_text()

    sort_dir = os.getenv("TARGET_DIR")

    source_path = Path(sort_dir)
    target_dir = Path(model_path)
    target_path = target_dir / source_path.name

    target_path.parent.mkdir(parents=True, exist_ok=True)

    shutil.move(str(source_path), str(target_path))