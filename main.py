from core.augmentation import augmentation
from core.generation import generation
from core.system_prompt import get_system_message
from core.database import query_recipe_collection
from fastapi import FastAPI
from datamodel.ChatRequest import ChatRequest
from datamodel.ChatResponse import ChatResponse
from datamodel.Ingredient import Ingredient

conversation_history: list[dict[str, str]] = [get_system_message()]

app = FastAPI()

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    question_from_app=request.messages[-1].content
    for m in request.messages[:-1]:
        conversation_history.append({"role":m.role,"content":m.content})
    reply_text = main_workflow(question_from_app,request.ingredients)
    return ChatResponse(reply=reply_text)

def main_workflow(question: str, ingredients: list[Ingredient]):

    results = query_recipe_collection(question, n_results=3)
    # print(f"relevant chunks:{results}")
    relevant_chunks = results

    current_prompt = augmentation(question, relevant_chunks, ingredients)

    full_prompt = conversation_history + current_prompt

    raw_answer = generation(full_prompt)
    # refined_answer=refine_answer_remove_cot(raw_answer)

    print('***** Answer from LLM *****')
    print(raw_answer)
    return raw_answer