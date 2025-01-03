from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

import os
from apps.common.common import *
from apps.common.database import *

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

# 紀錄群組/個人前一則訊息 
def recordTextMessage(event, userMessage):

    source_id = getMessageSourceID(event)
    file_path = 'recordTextMessage'
    record_data = {
        "id": source_id,
        "message": userMessage,
    }

    if userMessage != '饅頭':
        # 寫入 JSON 檔案
        write_database_temporary(file_path, source_id, record_data)

    # text_message = TextSendMessage(text="寫入成功")
    # line_bot_api.reply_message(event.reply_token, text_message)
    return


# 讀取紀錄
def readTextMessage(event):
    
    source_id = getMessageSourceID(event)
    file_path = 'recordTextMessage'
    
    loaded_data = read_database_temporary(file_path, source_id)    # 讀取檔案

    return loaded_data