from linebot import LineBotApi
from linebot.models import *

import os
import random

# CSV 讀取（Google 端）
import pandas as pd


line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))

# 冷笑話
def badJoke(event):

    # 從Google Sheets下載的CSV檔案的URL
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTU6W8Qj4ONJzVrxZaV0OvIOGuN-ld_lR-SZ5KpqJ3s-O4Po7O3cRiMYFIkbnJ6gHxjGELZhprJU0K_/pub?output=csv"

    # 使用pandas載入CSV文件
    df = pd.read_csv(url)

    # 隨機選取一行
    random_row = df.sample(n=1)

    # 提取隨機選擇的行的第二列數據
    second_column_value = random_row.iloc[0, 1]

    # 列印第二列的值
    # print(second_column_value)

    replyLineMessage = TextSendMessage(str(second_column_value))
    line_bot_api.reply_message(event.reply_token, replyLineMessage)
