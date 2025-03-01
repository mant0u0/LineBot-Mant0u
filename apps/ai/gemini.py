import requests
import json
import os
import base64

from apps.common.common import *

gemini_key = os.getenv("GEMINI_KEY")

# 一般 AI
def gemini(userMessage):
    if gemini_key is None:
        returnText = "尚未設定 GEMINI_KEY 環境變數"
        return returnText
    else:
        API_KEY = str(gemini_key)

        url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}'

        headers = {'Content-Type': 'application/json'}
        data = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {
                        "text": userMessage
                    }
                ]
            }
        ],
        "systemInstruction": {
            "role": "user",
            "parts": [
                {
                    "text": "使用「正體中文(台灣)」回覆"
                }
            ]
        },
        "generationConfig": {
            "temperature": 1,
            "topK": 40,
            "topP": 0.95,
            "maxOutputTokens": 8192,
            "responseMimeType": "text/plain"
        }
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
            print(response)
            returnText = "Gemini API 請求失敗"

        return returnText

# 可以設定 system_prompt 與 record_prompt
def gemini_ai( user_prompt, system_prompt = "使用「正體中文(台灣)」回覆" , record_prompt = [] ):
    if gemini_key is None:
        returnText = "尚未設定 GEMINI_KEY 環境變數"
        return returnText
    else:
        API_KEY = str(gemini_key)
        url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}'

        # prompt
        data_contents = []
        
        # 對話紀錄 prompt
        for item in record_prompt:
            # record_prompt = [
            #     {
            #         "user": "使用者說的話 1",
            #         "model": "AI 模型要回的話 1",
            #     },
            #     {
            #         "user": "使用者說的話 2",
            #         "model": "AI 模型要回的話 2",
            #     },
            # ]

            # 範本問題
            data_contents.append({
                "role": "user", "parts": [{"text": item["user"]}],
            })
            # 範本回答
            data_contents.append({
                "role": "model", "parts": [{"text": item["model"]}],
            })
        
        # 使用者 prompt
        data_contents.append({
            "role": "user", "parts": [{"text": user_prompt}],
        })

        data = {
            "contents" : data_contents,
            "systemInstruction": {
                "role": "user",
                "parts": [
                    {
                        "text": system_prompt
                    }
                ]
            },
            "generationConfig": {
                "temperature": 1,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 8192,
                "responseMimeType": "text/plain"
            }
        }


        headers = {'Content-Type': 'application/json'}
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
            print(response)
            returnText = "Gemini API 請求失敗"

        return returnText
    


def geminiVision(userMessage, event):
    if gemini_key is None:
        returnText = "尚未設定 GEMINI_KEY 環境變數"
        return returnText
    else:
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

