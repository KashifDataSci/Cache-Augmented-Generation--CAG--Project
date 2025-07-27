import os
import httpx 
from dotenv import load_dotenv, find_dotenv

# Load Environment variables from .env file

load_dotenv(find_dotenv())

def get_llm_responce(context: str, query: str) -> str:

    # Use OPENROUTER_API_KEY for OpenRouter

    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENROUTER_API_KEY environment Variable is not set. "
            "Please set it to your OpenRouter API key."
        )

    
    OPENROUTER_API_BASE = "https://openrouter.ai/api/v1/chat/completions"
    
   
    model_name = "mistralai/mistral-7b-instruct" 

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",

        
        "HTTP-Referer": "your-app-name-or-url",
        "X-Title": "Your App Name" 
    }

    # Construct the messages for the chat completion API

    messages = [
        {
            "role": "system",
            "content": (
                "You are an intelligent and precise assistant. "
                "Your primary task is to answer user questions based *solely* on the 'PROVIDED DOCUMENT CONTEXT'. "
                "Read the context carefully before formulating your response. "
                "If the information needed to answer the question is not explicitly available in the provided document, "
                "state clearly that the answer cannot be found in the document. "
                "Do not introduce outside information or make assumptions.\n\n"
                f"PROVIDED DOCUMENT CONTEXT:\n```\n{context}\n```"
            )
        },
        {"role": "user", "content": query}
    ]

    payload = {
        "model": model_name,
        "messages": messages,
        "temperature": 0.2, 
        "max_tokens": 500,  
    }

    try:
        response = httpx.post(OPENROUTER_API_BASE, headers=headers, json=payload, timeout=60)
        response.raise_for_status() 
        response_data = response.json()
        if response_data and "choices" in response_data and response_data["choices"]:
            llm_response_text = response_data["choices"][0]["message"]["content"]
            return llm_response_text
        else:
            print(f"No valid response or choices found: {response_data}")
            return "No response from LLM."

    except httpx.RequestError as e:
        print(f"An HTTP request error occurred: {e}")
        raise ValueError(f"Failed to connect to OpenRouter API: {e}")
    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
        raise ValueError(f"OpenRouter API returned an error: {e.response.status_code} - {e.response.text}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise ValueError(f"An unexpected error occurred while getting LLM response: {e}")