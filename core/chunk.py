import json
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def json_object_chunking(json_path: str,output_dir:str):
    """Chunk by json object"""
    if not os.path.exists(json_path):
        print(f"Document not found: {json_path}")
        return
    print(f"Processing: {json_path}")

    with open(json_path, "r", encoding="utf-8") as f:
        recipes = json.load(f)

    document_name = Path(json_path).stem
    output_folder = os.path.join(output_dir, document_name)
    Path(output_folder).mkdir(parents=True, exist_ok=True)

    # Clear existing chunks
    if os.path.exists(output_folder):
        for file in os.listdir(output_folder):
            if file.endswith('.json'):
                os.remove(os.path.join(output_folder, file))

    count=0
    for r in recipes:
        chunk_text = (
            f"Title: {r['title']}\n"
            f"Description: {r.get('description', '')}\n"
            f"Ingredients: {r.get('ingredients', '')}\n"
            f"Steps: {r.get('steps', '')}"
        )

        r["chunk_text"]=chunk_text
        chunk_id = r.get("id", "unknown")
        
        safe_filename = f"{document_name}-{chunk_id}.json"

        chunk_file_path = os.path.join(output_folder, safe_filename)

        with open(chunk_file_path, "w", encoding="utf-8") as out_f:
            json.dump(r, out_f, ensure_ascii=False, indent=4)
        count=count+1

    print(f"Processed: {json_path} and created {count} chunks")

if __name__ == "__main__":

    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    document_to_process = os.path.join(project_root, "raw_data", "recipe_v2.json")
    output_dir = os.path.join(project_root, "chunks")

    if os.path.exists(document_to_process):
        json_object_chunking(document_to_process, output_dir)
    else:
        print(f"File not found: {document_to_process}")


