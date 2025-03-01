import requests
import json
import os

API_KEY = os.getenv("GROQ_API_KEY")

def groqWhisper(fileName):

    # API 端點
    url = 'https://api.groq.com/openai/v1/audio/transcriptions'

    # 設定 headers
    headers = {
        'Authorization': f'bearer {API_KEY}'
    }

    # 準備檔案和其他參數
    files = {
        'file': (fileName, open(fileName, 'rb'))
    }

    data = {
        'model': 'whisper-large-v3-turbo',
        'temperature': 0,
        'response_format': 'json',
        'language': 'zh'
    }

    # 發送請求
    try:
        response = requests.post(
            url,
            headers=headers,
            files=files,
            data=data
        )
        
        # 檢查回應
        response.raise_for_status()
        result = response.json()
        print(result)
    except requests.exceptions.RequestException as e:
        print(f"發生錯誤: {e}")
    finally:
        # 確保檔案被關閉
        files['file'][1].close()


    return str(result['text'])
