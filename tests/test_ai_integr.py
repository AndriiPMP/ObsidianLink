from script.others.ai_integr import generate_embedding

def test_generaye_embedding():
    test_text = "Это тестовый текст для генерации эмбеддинга"

    result = generate_embedding(test_text)

    assert isinstance(result, list)
    assert len(result) > 0 
    for num in result:
        assert isinstance(num, float)
