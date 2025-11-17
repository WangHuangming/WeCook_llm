import os
import chromadb
from chromadb.utils.embedding_functions.ollama_embedding_function import (
    OllamaEmbeddingFunction,
)

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
db_path = os.path.join(project_root, "chroma_db")

ollama_ef = OllamaEmbeddingFunction(
    url="http://localhost:11434",
    model_name="nomic-embed-text:latest",
)

def get_recipe_collection(persist_dir=db_path,collection_name="recipes"):
    client = chromadb.PersistentClient(persist_dir)
    collection = client.get_or_create_collection(
        name=collection_name,
        embedding_function=ollama_ef
    )
    return collection,client


def add_chunks_to_chroma(chunks, persist_dir=db_path, collection_name="recipes"):

    collection, client = get_recipe_collection(persist_dir, collection_name)

    documents = [chunk["chunk_text"] for chunk in chunks]
    embeddings = [chunk["embeddings"] for chunk in chunks]
    ids = [chunk["id"] for chunk in chunks]
    metadatas = [{"title": chunk.get("title"), "date": chunk.get("date")} for chunk in chunks]

    collection.add(
        documents=documents,
        embeddings=embeddings,
        ids=ids,
        metadatas=metadatas
    )
    print("Number of items after add:", collection.count())
    # docs = collection.get(
    #     limit=3,
    #     include=["embeddings", "documents", "metadatas"]
    # )
    # print(docs["embeddings"][0][:10])  # 打印embedding前10个数字
    # print("-------------------")
    # print(docs)
    # print("-------------------")
    print(f"{len(chunks)} chunks added to collection '{collection_name}' and persisted.")

def query_recipe_collection(query_text, n_results=3, persist_dir="./chroma_db", collection_name="recipes"):

    collection, _ = get_recipe_collection(persist_dir, collection_name)
    results = collection.query(query_texts=[query_text], n_results=n_results)
    return results
