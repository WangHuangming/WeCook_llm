import json
import os
from core.chunk import json_object_chunking
from core.embeddings import embeddings, gather_chunk_files
from database import add_chunks_to_chroma, query_recipe_collection

def load_chunks_from_files(file_paths: list[str]) -> list[dict]:
    all_chunks = []
    for file_path in file_paths:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                all_chunks.extend(data)
            elif isinstance(data, dict):
                all_chunks.append(data)
    return all_chunks


def data_proceed():

    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    #chunking
    document_to_process = os.path.join(project_root, "raw_data", "recipe_v3.json")
    output_dir = os.path.join(project_root, "chunks")

    if os.path.exists(document_to_process):
        json_object_chunking(document_to_process, output_dir)
    else:
        print(f"File not found: {document_to_process}")

    #embedding
    documents_to_process=[
        "recipe_v3"
    ]
    embeddings(documents_to_process)

    chunk_files = gather_chunk_files(documents_to_process)
    chunks = load_chunks_from_files(chunk_files)
    add_chunks_to_chroma(chunks)

    # question="give me a quick recipe that I added before"
    # results = query_recipe_collection(question, n_results=3)
    # print(results)

data_proceed()

