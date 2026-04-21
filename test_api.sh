#!/bin/bash

# Test script for LiteRT-LM API
# This script sends a POST request to the chat completions endpoint

API_URL="http://127.0.0.1:8000/v1/chat/completions"

echo "Testing LiteRT-LM API..."
echo "URL: $API_URL"
echo

# Send a simple chat completion request
curl -X POST "$API_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemma-4-E2B-it",
    "messages": [
      {
        "role": "user",
        "content": "can you write a python function that prints hello world "
      }
    ],
    "stream": true,
    "temperature": 0.7,
    "max_tokens": 100
  }'

echo
echo "Test completed."
