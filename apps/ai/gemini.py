import requests
import os
import base64

from apps.common.common import *

gemini_key = os.getenv("GEMINI_KEY", None)

def gemini(userMessage):
    if gemini_key is None:
        return "尚未設定 GEMINI_KEY 環境變數"

    API_KEY = str(gemini_key)

    url = f'https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={API_KEY}'

    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [
            {
                "parts": [{"text": userMessage}]
            }
        ],
        "safetySettings": [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_ONLY_HIGH"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_ONLY_HIGH"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_ONLY_HIGH"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_ONLY_HIGH"
            }
        ]
    }
    response = requests.post(url, headers=headers, json=data)


    if response.status_code == 200:
        reply = response.json()
        try:
            returnText = reply['candidates'][0]['content']['parts'][0]['text']
            print(returnText)
        except:
            returnText = ""
            print(returnText)
    else:
        returnText = "Gemini API 請求失敗"

    return returnText


def geminiPrompt(userMessage, prompt):
    if gemini_key is None:
        return "尚未設定 GEMINI_KEY 環境變數"
    API_KEY = str(gemini_key)

    url = f'https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={API_KEY}'

    # prompt = [
    #     {
    #         "Q":"今天天氣如何",
    #         "A":"晴天",
    #     },
    # ]

    data_contents = []
    # 製作問答範本
    for item in prompt:
        # 範本問題
        data_contents.append({
            "role": "user", "parts": [{"text": item["Q"]}],
        })
        # 範本回答
        data_contents.append({
            "role": "model", "parts": [{"text": item["A"]}],
        })
    
    # 問題
    data_contents.append({
        "role": "user", "parts": [{"text": userMessage}],
    })

    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": data_contents,
        "safetySettings": [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_ONLY_HIGH"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_ONLY_HIGH"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_ONLY_HIGH"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_ONLY_HIGH"
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)


    if response.status_code == 200:
        reply = response.json()
        try:
            returnText = reply['candidates'][0]['content']['parts'][0]['text']
            print(returnText)
        except:
            returnText = ""
            print(returnText)
    else:
        returnText = "Gemini API 請求失敗"

    return returnText

def geminiVision(userMessage, event):
    if gemini_key is None:
        return "尚未設定 GEMINI_KEY 環境變數"
    API_KEY = str(gemini_key)
    url = f'https://generativelanguage.googleapis.com/v1/models/gemini-pro-vision:generateContent?key={API_KEY}'

    # 取得訊息來源 ID
    source_id = getMessageSourceID(event)   

    try:
        # 讀取本地文件並轉換為Base64字符串
        with open(f"/tmp/{source_id}.jpg", "rb") as image_file:
            image_base64_bytes = base64.b64encode(image_file.read())
            image_base64_string = image_base64_bytes.decode('utf-8')

        headers = {'Content-Type': 'application/json'}
        data = {
            "contents": [
                {
                    "parts": [{
                        "text": userMessage
                    }, {
                        "inline_data": {
                            "mime_type": "image/jpeg",
                            "data": image_base64_string
                        }
                    }]
                },
            ],
            "safetySettings": [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_ONLY_HIGH"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_ONLY_HIGH"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_ONLY_HIGH"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_ONLY_HIGH"
                }
            ]

        }

        response = requests.post(url, headers=headers, json=data)

        returnText = response.json()
        returnText = returnText['candidates'][0]['content']['parts'][0]['text']

        return returnText[1:]
    
    except:
        return "目前沒有上傳任何圖片～"
