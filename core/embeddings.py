import json
import os
import time
from typing import List
from dotenv import load_dotenv
from ollama import Client

load_dotenv()

ollama_client = Client(host=os.environ.get("OLLAMA_HOST", "http://localhost:11434"))

CUSTOM_EMBEDDING_DIM = 768

def gather_chunk_files(document_folders: list[str]) -> list[str]:
    chunk_files = []

    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    chunks_dir = os.path.join(project_root, "chunks")

    for document_folder in document_folders:
        folder_path = os.path.join(chunks_dir, document_folder)
        if os.path.exists(folder_path):
            for file in os.listdir(folder_path):
                if file.endswith(".json"):
                    chunk_files.append(os.path.join(folder_path, file))
    
    return chunk_files


def embeddings(documents_to_process:List[str]):

    chunk_files = gather_chunk_files(documents_to_process)
    for index, chunk_file in enumerate(chunk_files, start=1):
        chunk_data = json.load(open(chunk_file, encoding="utf-8"))

        with open(chunk_file, "w", encoding="utf-8") as c:
            response = ollama_client.embeddings(
                model=os.environ.get("EMBEDDING_MODEL", "nomic-embed-text"),
                prompt=chunk_data["chunk_text"],
                options={
                    "keep_alive": 0
                },
            )

            embedding = response["embedding"]
            print(f"Embedding dimension: {len(embedding)}")

            # if CUSTOM_EMBEDDING_DIM > 0 and len(embedding) > CUSTOM_EMBEDDING_DIM:
            #     embedding = embedding[:CUSTOM_EMBEDDING_DIM]

            chunk_data["embeddings"] = response["embedding"]
            json.dump(chunk_data, c, indent=4, ensure_ascii=False)

        time.sleep(0.1)
        print(f"Processed chunks -> {index}/{len(chunk_files)}")


