from core.augmentation import augmentation
from core.generation import generation
from core.system_prompt import get_system_message
from database import query_recipe_collection

conversation_history: list[dict[str, str]] = [get_system_message()]

def main_workflow():
    question = ""

    results = query_recipe_collection(question, n_results=3)
    print(results)
    relevant_chunks = results

    current_prompt = augmentation(question, relevant_chunks)

    full_prompt = conversation_history + current_prompt

    raw_answer = generation(full_prompt)
    # refined_answer=refine_answer_remove_cot(raw_answer)

    print('***** Answer from LLM *****')
    print(raw_answer)

if __name__ == "__main__":
    main_workflow()