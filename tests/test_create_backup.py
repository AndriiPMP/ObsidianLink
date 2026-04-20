import os
import shutil
import uuid

from script.create_backUp import create_backup


def test_create_backup_copies_directory():
    root = os.path.join(os.path.dirname(__file__), "_backup_test_" + uuid.uuid4().hex)
    source = os.path.join(root, "source")
    base = os.path.join(root, "base")

    try:
        os.makedirs(source, exist_ok=True)
        os.makedirs(base, exist_ok=True)
        with open(os.path.join(source, "note.md"), "w", encoding="utf-8") as f:
            f.write("hello")

        backup_path = create_backup(source, base)

        assert backup_path is not None
        assert os.path.isdir(backup_path)
        assert os.path.isfile(os.path.join(backup_path, "note.md"))
        assert os.path.isdir(os.path.join(base, "backups"))
    finally:
        shutil.rmtree(root, ignore_errors=True)
