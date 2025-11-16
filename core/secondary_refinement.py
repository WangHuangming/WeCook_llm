from typing import Dict, List
from core.generation import generation

def refine_answer_remove_cot(raw_llm_output: str) -> str:

    refinement_message = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": (
            "The following is a response that includes your internal reasoning "
            "(chain-of-thought). Please removing all internal thought or step-by-step reasoning, "
            "but keep the content conversational and informative. You can keep a small amount of the conversation."
            "**Title:** **Description:** **Ingredients:** **Steps:** should be kept "
            f"Original response:\n{raw_llm_output}"
        )}
    ]

    refined_output = generation(refinement_message)

    return refined_output