#!/usr/bin/env python3
"""
Minimal helloworld example for LiteRT-LM using the CLI directly.

This demonstrates basic usage of LiteRT language models without requiring
an API server or additional Python packages.
"""

import subprocess
import sys


def run_litert_model(prompt: str, model_reference: str = None):
    """
    Run a LiteRT-LM model with a single prompt.
    
    Args:
        prompt: The prompt to send to the model
        model_reference: Model ID or path. If None, will download from HuggingFace
    
    Returns:
        The model's response text
    """
    
    # Build the command
    cmd = ["litert-lm", "run"]
    
    # Add model reference or use a default from HuggingFace
    if model_reference:
        cmd.append(model_reference)
    else:
        # Use Gemma 4B model from HuggingFace
        cmd.extend(["--from-huggingface-repo", "litert-community/gemma-4-E2B-it-litert-lm", "gemma-4-E2B-it.litertlm"])
    
    # Add the prompt
    cmd.extend(["--prompt", prompt])
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300,  # 5 minute timeout
        )
        
        if result.returncode != 0:
            print(f"Error running litert-lm: {result.stderr}")
            return None
        
        return result.stdout.strip()
    
    except FileNotFoundError:
        print("Error: litert-lm command not found!")
        print("Make sure litert-lm is installed and in your PATH")
        return None
    except subprocess.TimeoutExpired:
        print("Error: Model inference timed out")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def main():
    """
    Simple helloworld example.
    
    Usage:
        python helloworld.py                    # Uses default model from HuggingFace
        python helloworld.py my-model           # Uses a local model
        python helloworld.py ./model.litertlm   # Uses a local model file
    """
    
    # Get model reference from command line or use default
    model_ref = sys.argv[1] if len(sys.argv) > 1 else None
    
    # The prompt
    prompt = "Say 'Hello, World!'"
    
    print(f"Prompt: {prompt}")
    print("Running litert-lm inference...")
    print()
    
    response = run_litert_model(prompt, model_ref)
    
    if response:
        print(f"Response:\n{response}")
        return 0
    else:
        return 1


if __name__ == "__main__":
    exit(main())
