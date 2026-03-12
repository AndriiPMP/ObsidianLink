import hashlib
from files_info import format_paths


def generate_hash_filepath(formated_path):
    hash_object = hashlib.md5(formated_path.encode('utf-8'))
    return int(hash_object.hexdigest()[:8], 16) % (10*9)

