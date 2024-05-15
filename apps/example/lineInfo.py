from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

import os
import json

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

# 取得使用者資訊
def userInfo(event):
    try:
        UserId = event.source.user_id
        profile = line_bot_api.get_profile(UserId)
        profile = json.loads(str(profile))  # 字串轉字典型態
        
        # 使用者名稱
        displayName = profile['displayName']
        result_text = "使用者名稱：" + displayName + "\n"

        # 使用者語言
        language = profile['language']
        result_text = result_text + "使用者名稱：" + language + "\n"

        # 使用者大頭貼
        pictureUrl = profile['pictureUrl']
        result_text = result_text + "使用者大頭貼：" + pictureUrl + "\n"

        # 使用者簡介
        statusMessage = profile['statusMessage']
        result_text = result_text + "使用者簡介：" + statusMessage + "\n"
        
        # 使用者 ID
        userId = profile['userId']
        result_text = result_text + "使用者 ID：" + userId + "\n"

    except:
        result_text = '目前沒有加好友，無法獲取 LINE 名稱。'

    # 包裝訊息
    text_message = TextSendMessage(text=result_text)
    # 發送訊息
    line_bot_api.reply_message(event.reply_token, text_message)


# 取得訊息資訊
def messageInfo(event):

    # 使用者訊息
    userMessage = event.message.text
    result_text = "使用者訊息：" + userMessage + "\n"

    # 訊息來源類型 (user/group)
    userMessageSourceType = event.source.type
    result_text = result_text + "訊息來源類型：" + userMessageSourceType + "\n"

    # 使用者 ID
    userId = event.source.user_id
    result_text = result_text + "使用者 ID：" + userId + "\n"

    # 群組 ID
    if userMessageSourceType == 'group':
        groupId = event.source.group_id
        result_text = result_text + "群組 ID：" + groupId + "\n"

    # 包裝訊息
    text_message = TextSendMessage(text=result_text)
    # 發送訊息
    line_bot_api.reply_message(event.reply_token, text_message)