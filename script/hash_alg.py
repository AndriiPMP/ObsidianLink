import hashlib


def generate_hash_filepath(formated_path):
    hash_object = hashlib.md5(formated_path.encode('utf-8'))
    return int(hash_object.hexdigest()[:8], 16) % (10*9) # Переделываем хеш в цифровое значение

