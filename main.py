import sys
from typing import List, Dict

from core.augmentation import augmentation
from core.generation import generation
from core.system_prompt import get_system_message
from database import query_recipe_collection

conversation_history: List[Dict[str, str]] = [get_system_message()]

def main_loop():
    print("Welcome to the Recipe Assistant! Type 'exit' to quit.\n")

    while True:
        question = input("Your question: ").strip()
        if question.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        results = query_recipe_collection(question, n_results=3)
        print(results)
        relevant_chunks = results

        current_prompt = augmentation(question, relevant_chunks)

        full_prompt = conversation_history + current_prompt

        raw_answer = generation(full_prompt)
        # refined_answer=refine_answer_remove_cot(raw_answer)
        conversation_history.extend(current_prompt)
        conversation_history.append({"role": "assistant", "content": raw_answer})

        print('***** Answer from LLM *****')
        print(raw_answer)

        # if 'Sorry, I could not fix the record with data references.' not in refined_answer:
        #     print('For more details, please refer to the following documents:')
        #     for chunk in relevant_chunks:
        #         print(chunk['document'])

if __name__ == "__main__":
    main_loop()