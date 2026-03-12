from openai import OpenAI

client = OpenAI (
    base_url="http://127.0.0.1:1234",
    api_key="not_needed"
)

responce = client.chat.completions.create(
    model="text-embedding-qwen3-embedding-8b"
    messages=[
        {"role": "user", "content": ""}
    ]
)