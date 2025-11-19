#!/bin/bash

# ---- 启动 Ollama 后台 ----
echo "Starting Ollama..."
ollama serve &
OLLAMA_PID=$!

# 可选：等待 Ollama 启动再继续
sleep 10

# ---- 拉取模型（如果已有则很快）----
echo "Pulling Llama model..."
ollama pull llama3.1

echo "Ollama is running with PID: $OLLAMA_PID"

# ---- 启动 FastAPI （主线程）----
echo "Starting FastAPI..."
uvicorn main:app --host 0.0.0.0 --port 8000

# ---- uvicorn 退出时关闭 Ollama ----
echo "Stopping Ollama..."
kill $OLLAMA_PID
