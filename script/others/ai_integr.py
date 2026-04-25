from openai import OpenAI
from script.others.files_process import get_folder_paths, get_files_sort_content
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


def generate_text(prompt: str) -> str:

    payload = {
    "task": """Analyze the contents and subject of the sort, then from the entire
            list of folders provided, select the exact directory
            in which the file should be located. Once you've selected the correct
            directory, copy it into your answer, word for word, character for character.""",
    "folders": get_folder_paths(),
    "sort": get_files_sort_content(),
    }
     
    prompt = json.dumps(payload, ensure_ascii=False, indent=2)

    responce = client.chat.completions.create(
        model="qwen/qwen3.5-9b",  
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return responce.choices[0].message.content