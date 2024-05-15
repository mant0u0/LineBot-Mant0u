import requests
import json
import os

openai_api_key = os.getenv("OPENAI_API_KEY")

def openai(userMessage):
    if openai_api_key is None:
        returnText = "尚未設定 OPENAI_API_KEY 環境變數"
        return returnText
    else:
        API_KEY = str(openai_api_key)

        response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers={
                'Authorization': 'Bearer ' + API_KEY
            },
            json={
                'model': 'gpt-3.5-turbo',
                "messages": [
                    {
                        "role": "user",
                        "content": userMessage,
                    }
                ],
            }
        )

        if response.status_code == 200:
            reply = response.json()
            returnText = reply["choices"][0]["message"]["content"]
        else:
            returnText = "Openai API 請求失敗"

        return returnText
