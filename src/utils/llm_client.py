import os
import requests
from dotenv import load_dotenv, find_dotenv

# Load Environment variables from .env file
load_dotenv(find_dotenv())

def get_llm_responce(context: str, query: str) -> str:

    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENROUTER_API_KEY environment Variable is not set. "
            "Please set it to your OpenRouter API key."
        )

    OPENROUTER_API_BASE = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "your-app-name-or-url",   # optional
        "X-OpenRouter-Title": "Your App Name"     # fixed header
    }

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
        {
            "role": "user",
            "content": query
        }
    ]

    try:
        response = requests.post(
            url=OPENROUTER_API_BASE,
            headers=headers,
            json={
                "model": "openai/gpt-5.2",   # updated model
                "messages": messages,
                "temperature": 0.2,
                "max_tokens": 500
            },
            timeout=60
        )

        response.raise_for_status()
        response_data = response.json()

        if response_data and "choices" in response_data and response_data["choices"]:
            return response_data["choices"][0]["message"]["content"]
        else:
            print(f"No valid response: {response_data}")
            return "No response from LLM."

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        raise ValueError(f"Failed to connect to OpenRouter API: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise ValueError(f"Unexpected error while getting LLM response: {e}")