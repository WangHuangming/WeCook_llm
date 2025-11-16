from typing import List, Dict

DOCUMENTS_DELIMITER = "\n+++++\n"

def augmentation(user_question: str, relevant_chunks: dict) -> list[dict]:
    """
    relevant_chunks: Chroma query 的返回值
    """
    doc_texts = relevant_chunks['documents'][0]

    user_prompt = "Reference Recipes:\n\n"

    for doc_text in doc_texts:
        user_prompt += f"{doc_text}\n"
        user_prompt += DOCUMENTS_DELIMITER

    user_prompt += f"\n### user's request: {user_question}"

    user_message = {"role": "user", "content": user_prompt}

    print('***** Prompt to be sent off to LLM *****')
    print(user_prompt)

    return [user_message]

