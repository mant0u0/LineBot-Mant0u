import requests
import json
import os

API_KEY = os.getenv("GROQ_API_KEY")

def groqAI(userMessage):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "messages": [
            {
                "role": "system",
                "content": 
                " - 請使用「台灣-正體中文」回答我，不要使用「英文」或是「簡體中文」。\n- 請用簡短的對話回答，限制 100 字以內，不使用條列式回覆。"
            },
            {
                "role": "user",
                "content": userMessage
            }
        ],
        "model": "gemma2-9b-it",
        "temperature": 1,
        "max_tokens": 1024,
        "top_p": 1,
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    # print("\n\n")
    # print(response.json()["choices"][0]["message"]["content"])
    # print(response.json())

    return response.json()["choices"][0]["message"]["content"]
