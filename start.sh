#!/bin/bash

echo "starting Ollama..."
ollama serve &
OLLAMA_PID=$!

sleep 10

echo "pulling Llama model..."
ollama pull llama3.1

echo "Ollama is running"

echo "starting FastAPI..."
uvicorn main:app --host 0.0.0.0 --port 8000

echo "stopping Ollama..."
kill $OLLAMA_PID
