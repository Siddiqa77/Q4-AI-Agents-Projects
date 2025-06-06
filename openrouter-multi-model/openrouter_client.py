import httpx
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

async def fetch_model_response(model_name, prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",
    }
    payload = {
        "model": model_name,
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
    except httpx.HTTPStatusError as e:
        return f"❌ HTTP error from `{model_name}`: {e.response.status_code}\n{e.response.text}"
    except Exception as e:
        return f"❌ Unexpected error from `{model_name}`: {str(e)}"


