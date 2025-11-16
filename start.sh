#!/bin/bash

ollama serve &
OLLAMA_PID=$!

sleep 10

ollama pull llama3.1

echo "Ollama is running with PID: $OLLAMA_PID"
wait $OLLAMA_PID