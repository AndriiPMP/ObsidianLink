import pytest
from script.hash_alg import generate_hash_filepath

def test_generate_hash_filepath():
    result = generate_hash_filepath(r"E:\План\IT\АИ инженерия\$100 миллионов — цена обучения GPT-4.md")
    assert isinstance(result, int)
    assert 0 <= result < 90
    assert generate_hash_filepath(r"E:\План\IT\АИ инженерия\$100 миллионов — цена обучения GPT-4.md") == generate_hash_filepath(r"E:\План\IT\АИ инженерия\$100 миллионов — цена обучения GPT-4.md")
    result1 = generate_hash_filepath(r"E:\План\IT\АИ инженерия\5-10x эффективность вместо замены программиста.md")
    result2 = generate_hash_filepath(r"E:\План\IT\АИ инженерия\99 языков и автоматический перевод.md")
    assert isinstance(result1, int)
    assert isinstance(result2, int)