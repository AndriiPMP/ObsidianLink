from openai import OpenAI

client = OpenAI (
    base_url="http://127.0.0.1:1234/v1", 
    api_key="not_needed"
)

def generate_embedding(text):

    responce = client.embeddings.create( 

        model="text-embedding-qwen3-embedding-8b",

        input=text
    )
    
    return responce.data[0].embedding


def generate_text(prompt: str) -> str:

    responce = client.chat.completions.create(
        model="qwen/qwen3.5-9b",  
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return responce.choices[0].message.content