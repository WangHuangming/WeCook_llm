import os
from dotenv import load_dotenv
from ollama import Client

load_dotenv()

ollama_client = Client(host=os.environ.get("OLLAMA_HOST", "http://localhost:11434"))


def generation(prompt_messages: list[dict[str, str]]) -> str:
    # Convert the messages to Ollama format
    messages = [
        {"role": msg["role"], "content": msg["content"]} for msg in prompt_messages
    ]

    response = ollama_client.chat(
        model=os.environ.get("CHAT_COMPLETION_MODEL", "deepseek-r1"),
        messages=messages,
        options={
            "temperature": 0,
            "top_k":20
        },
    )

    return response["message"]["content"]