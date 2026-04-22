import os
import shutil
from dotenv import load_dotenv

load_dotenv()

def create_backup():

    target_dir = os.getenv("TARGET_DIR")

    base_dir = os.getenv("BASE_DIR")

    backup_root = os.path.join(base_dir, "backups")

    os.makedirs(backup_root, exist_ok=True)

    source_name = os.path.basename(os.path.normpath(target_dir))

    backup_path = get_backup_path(backup_root, source_name)

    if os.path.isdir(target_dir):
        shutil.copytree(target_dir, backup_path)

    else:
        os.makedirs(backup_path, exist_ok=True)
        shutil.copy2(target_dir, os.path.join(backup_path, os.path.basename(target_dir)))
    


def get_backup_path(backup_root, source_name):

    n = 1
    while True:

        backup_path = os.path.join(backup_root, f"{source_name}_{n}")

        if not os.path.exists(backup_path):
            return backup_path
        n += 1