import requests
import json
from zhconv import convert # 簡轉繁

# 簡轉繁
def zhconvert(text):
    convertText = convert(text, 'zh-hant') 
    return convertText

# 繁化姬 API （簡轉繁用語）
def zhconvert_API(text):

    api_endpoint = "https://api.zhconvert.org/convert"
    params = {
        "text": text,
        "converter": "Taiwan"
    }
    response = requests.post(api_endpoint, json=params)
    if response.status_code == 200:
        data = response.json()
        convertText = data.get("data", {}).get("text")

    return convertText
