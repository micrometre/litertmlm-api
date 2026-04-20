from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import subprocess
import json
import uuid

app = FastAPI()

@app.post("/v1/chat/completions")
async def chat_proxy(request: Request):
    data = await request.json()
    messages = data.get("messages", [])
    stream = data.get("stream", False)

    # Use litert-lm CLI like helloworld.py
    def generate():
        # Last message is the prompt
        prompt = messages[-1]["content"]
        response_id = f"chatcmpl-{uuid.uuid4()}"
        
        # Build the command like helloworld.py
        cmd = ["litert-lm", "run"]
        cmd.extend(["--from-huggingface-repo", "litert-community/gemma-4-E2B-it-litert-lm", "gemma-4-E2B-it.litertlm"])
        cmd.extend(["--prompt", prompt])
        
        try:
            # Run the command and get output
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300,
            )
            
            if result.returncode == 0:
                response_text = result.stdout.strip()
                # Send the entire response as one chunk
                chunk = {
                    "id": response_id,
                    "object": "chat.completion.chunk",
                    "choices": [{"delta": {"content": response_text}, "index": 0, "finish_reason": "stop"}]
                }
                yield f"data: {json.dumps(chunk)}\n\n"
            
            yield "data: [DONE]\n\n"
            
        except Exception as e:
            # Send error chunk
            chunk = {
                "id": response_id,
                "object": "chat.completion.chunk",
                "choices": [{"delta": {"content": f"Error: {str(e)}"}, "index": 0, "finish_reason": "stop"}]
            }
            yield f"data: {json.dumps(chunk)}\n\n"
            yield "data: [DONE]\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)