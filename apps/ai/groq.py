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
        "model": "llama-3.3-70b-versatile",
        "temperature": 1,
        "max_tokens": 1024,
        "top_p": 1,
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data), timeout=30)
        
        if response.status_code != 200:
            return "抱歉，AI 服務暫時無法使用，請稍後再試。"
        
        response_data = response.json()
        
        if "choices" in response_data and response_data["choices"]:
            return response_data["choices"][0]["message"]["content"]
        else:
            return "抱歉，AI 未能產生回應，請稍後再試。"
            
    except Exception as e:
        return "抱歉，AI 服務發生錯誤，請稍後再試。"

# 進階版 - 可以設定 system_prompt 與 record_prompt
def groqAI_advanced(user_prompt, system_prompt="使用「台灣-正體中文」回答我，不要使用「英文」或是「簡體中文」。請用簡短的對話回答，限制 100 字以內，不使用條列式回覆。", record_prompt=[]):
    if API_KEY is None:
        return "尚未設定 GROQ_API_KEY 環境變數"
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # 建立訊息列表
    messages = []
    
    # 系統 prompt
    messages.append({
        "role": "system",
        "content": system_prompt
    })
    
    # 對話紀錄 prompt
    for item in record_prompt:
        # record_prompt = [
        #     {
        #         "user": "使用者說的話 1",
        #         "assistant": "AI 回應的話 1",  # 可使用 "assistant" 或 "model"
        #     },
        #     {
        #         "user": "使用者說的話 2",
        #         "model": "AI 回應的話 2",  # 可使用 "assistant" 或 "model"
        #     },
        # ]
        
        # 使用者的訊息
        messages.append({
            "role": "user",
            "content": item["user"]
        })
        # AI 的回應（支援 "assistant" 或 "model" 兩種 key）
        ai_response = item.get("assistant") or item.get("model", "")
        messages.append({
            "role": "assistant",
            "content": ai_response
        })
    
    # 當前使用者 prompt
    messages.append({
        "role": "user",
        "content": user_prompt
    })
    
    data = {
        "messages": messages,
        "model": "llama-3.3-70b-versatile",
        "temperature": 1,
        "max_tokens": 1024,
        "top_p": 1,
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data), timeout=30)
        
        if response.status_code != 200:
            return "抱歉，AI 服務暫時無法使用，請稍後再試。"
        
        response_data = response.json()
        
        if "choices" in response_data and response_data["choices"]:
            return response_data["choices"][0]["message"]["content"]
        else:
            return "抱歉，AI 未能產生回應，請稍後再試。"
            
    except Exception as e:
        return "抱歉，AI 服務發生錯誤，請稍後再試。"

