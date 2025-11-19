from datamodel.Ingredient import Ingredient

BLOCK_DELIMITER = "\n+++++++"
CHUNK_DELIMITER = "\n-------"


def augmentation(user_question: str, relevant_chunks: dict, ingredients: list[Ingredient]) -> list[dict[str,str]]:
    doc_texts = relevant_chunks['documents'][0]

    user_prompt = "Reference Recipes:"

    for doc_text in doc_texts:
        user_prompt += f"\n{doc_text}"
        user_prompt += CHUNK_DELIMITER
    user_prompt += BLOCK_DELIMITER

    user_prompt += "\nIngredients:"
    for ingredient in ingredients:
        user_prompt += f"\n{ingredient.name} {ingredient.weightInGrams}g"

    user_prompt += BLOCK_DELIMITER
    user_prompt += f"\n### user's request: {user_question}"

    user_message = {"role": "user", "content": user_prompt}

    print('***** Prompt to be sent off to LLM *****')
    print(user_prompt)

    return [user_message]

