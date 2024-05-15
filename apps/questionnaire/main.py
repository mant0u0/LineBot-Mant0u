# 問卷（未完成功能）
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

import os
import random
import re

from apps.common.common import *

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))


def questionnaireMain(event, userMessage):
    userMessage = userMessage.replace('題目：', '')
    userMessage = userMessage.replace('問題：', '')

    # 取得使用者名稱
    try:
        UserId = event.source.user_id
        profile = line_bot_api.get_profile(UserId)
        profile = json.loads(str(profile))  # 字串轉字典型態
        userName = str(profile['displayName'])
    except:
        userName = '有人'

    # 文字分割：第一行（題目）、第二行...（選項）
    textList = userMessage.split("\n")

    # LINE 訊息包裝
    flex_message_contents = []
    pageTemplate_Contents = [
        # 副標題
        {
            "type": "text",
            "text": userName + "提出問題！",
            "weight": "bold",
            "size": "sm",
            "color": "#205e0899",
            "align": "center",
            "offsetBottom": "8px",
        },
        # 主標題
        {
            "type": "text",
            "text": str(textList[0]),
            "weight": "bold",
            "wrap": True,
            "size": "lg",
            "color": "#205e08",
            "align": "center"
        }, {
            "type": "separator",
            "margin": "12px"
        }
    ]

    # 移除第一行（題目）
    textList = textList[1:]

    for i in range(len(textList)):
        # 按鈕
        btnItem = {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": str(textList[i]),
                "weight": "bold",
                "color": "#205e08",
                "wrap": True,
            },
            ],
            "action": {
                "type": "message",
                "label": "action",
                "text": str(textList[i]),
            },
            "paddingAll": "12px",
            "justifyContent": "center",
            "alignItems": "center",
        }
        pageTemplate_Contents.append(btnItem)
        # 分隔線
        if i != len(textList) - 1:
            pageTemplate_Contents.append({"type": "separator"})

    # 頁面 (pageTemplate)
    pageTemplate = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                # 橫幅 banner
                {
                    "type": "image",
                    "url": localImg("banner/question.png"),
                    "size": "100%",
                    "aspectMode": "fit",
                    "margin": "0px",
                    "position": "relative",
                    "aspectRatio": "1000:279"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": pageTemplate_Contents,
                    "paddingAll": "12px"
                }
            ],
            "paddingAll": "0px"
        }
    }
    flex_message_contents.append(pageTemplate)

    # 包裝訊息
    replyLineMessage = FlexSendMessage(
        alt_text=userName + "提出問題！",
        contents={
            "type": "carousel",
            "contents": flex_message_contents,
        }
    )
    # 回傳訊息
    line_bot_api.reply_message(event.reply_token, replyLineMessage)

