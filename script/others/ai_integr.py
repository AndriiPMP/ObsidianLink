from openai import OpenAI
from files_info import get_folder_paths, get_files_sort_content
import json
import os

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

payload = {
    "task": """Analyze the contents and subject of the sort, then from the entire
            list of folders provided, select the exact directory
            in which the file should be located. Once you've selected the correct
            directory, copy it into your answer, word for word, character for character.""",
    "folders": get_folder_paths(),
    "sort": get_files_sort_content(),
}

def generate_text(prompt: str) -> str:
     
    prompt = json.dumps()

    responce = client.chat.completions.create(
        model="qwen/qwen3.5-9b",  
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return responce.choices[0].message.content