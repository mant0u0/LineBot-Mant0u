# 翻譯

from linebot import LineBotApi
from linebot.models import *

import os
import googletrans
import requests
from apps.common.common import *

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))

def translateMain(event, userMessage):
    userMessage = userMessage.replace('翻譯：', '')

    # LINE 訊息包裝
    contentsList = []
    btnContentsList = [
        {
            "type": "text",
            "text": "翻譯成什麼語言？",
            "weight": "bold",
            "size": "lg",
            "color": "#1a5887",
            "align": "center"
        }, {
            "type": "text",
            "text": userMessage,
            "weight": "bold",
            "size": "sm",
            "color": "#1a588799",
            "align": "center",
            "margin": "4px"
        }, {
            "type": "separator",
            "margin": "12px"
        }
    ]
    btnList = ["中文", "英文", "日文", "韓文", "注音"]

    for i in range(len(btnList)):
        # 按鈕文字
        language = btnList[i]
        # 按鈕
        btnItem = {
            "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": language,
                            "weight": "bold",
                            "color": "#1a5887"
                        }
                    ],
            "paddingAll": "12px",
            "justifyContent": "center",
            "alignItems": "center",
            "action": {
                "type": "postback",
                "label": "中文",
                "data": "翻譯：" + language + "|||" + userMessage,
                    }
        }
        btnContentsList.append(btnItem)
        # 分隔線
        if i != len(btnList) - 1:
            btnContentsList.append({"type": "separator"})

    contentsItem = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "image",
                    "url": localImg("banner/translate.png"),
                    "size": "100%",
                    "aspectMode": "fit",
                    "margin": "0px",
                    "position": "relative",
                    "aspectRatio": "1000:279"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": btnContentsList,
                    "paddingAll": "12px"
                }
            ],
            "paddingAll": "0px"
        }
    }
    contentsList.append(contentsItem)

    # 包裝訊息
    replyLineMessage = FlexSendMessage(
        alt_text='翻譯！',
        contents={
            "type": "carousel",
            "contents": contentsList,
        },
    )
    # 回傳訊息
    line_bot_api.reply_message(event.reply_token, replyLineMessage)



def translatePostback(event, userPostback):
    postbackText = userPostback.replace('翻譯：', '')
    postbackText = postbackText.split("|||")
    language = postbackText[0]
    inputText = postbackText[1]

    if language == '英文':
        language = 'en'
    if language == '日文':
        language = 'ja'
    if language == '韓文':
        language = 'ko'
    if language == '中文':
        language = 'zh-tw'
    if language == '注音':
        language = 'bopomofo'

    if language != "bopomofo":
        translator = googletrans.Translator()
        resultText = translator.translate(inputText, dest=language).text

    # 注音
    else:
        api_endpoint = "https://api.zhconvert.org/convert"
        converter = "Bopomofo"
        params = {
            "text": inputText,
            "converter": converter
        }
        response = requests.post(api_endpoint, json=params)
        if response.status_code == 200:
            data = response.json()
            resultText = data.get("data", {}).get("text")

    # 台灣化翻譯
    if language == "zh-tw":
        api_endpoint = "https://api.zhconvert.org/convert"
        converter = "Taiwan"
        params = {
            "text": resultText,
            "converter": converter
        }
        response = requests.post(api_endpoint, json=params)
        if response.status_code == 200:
            data = response.json()
            resultText = data.get("data", {}).get("text")
    
    # 包裝訊息、發送訊息
    text_message = TextSendMessage(text=resultText)
    line_bot_api.reply_message(event.reply_token, text_message)