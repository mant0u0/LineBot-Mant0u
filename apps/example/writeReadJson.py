from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

import os
import json
from apps.common.common import *
from apps.common.database import *

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))


# 讀取 JSON 範例
def readJsonExample(event):
    
    source_id = getMessageSourceID(event)   # 取得訊息來源 ID
    file_path = 'test'               # 選擇存取的檔案路徑
    
    loaded_data = read_database_temporary(file_path, source_id)  # 讀取檔案
    text_message = TextSendMessage(text= str(loaded_data) ) # 印出結果
    line_bot_api.reply_message(event.reply_token, text_message)


# 寫入 JSON 範例
def writeJsonExample(event, userMessage):

    userMessage = userMessage.replace('寫入：', '')
    
    source_id = getMessageSourceID(event)
    file_path = 'test'
    record_data = {
        "id": source_id,
        "message": userMessage,
    }
    # 寫入 JSON 檔案
    write_database_temporary(file_path, source_id, record_data)

    text_message = TextSendMessage(text="寫入成功")
    line_bot_api.reply_message(event.reply_token, text_message)


# 移除 JSON 資料範例
def removeJsonExample(event):

    source_id = getMessageSourceID(event)
    file_path = 'test'

    remove_database_temporary(file_path, source_id)

    text_message = TextSendMessage(text="移除資料")
    line_bot_api.reply_message(event.reply_token, text_message)