# 亂數產生

from linebot import LineBotApi, WebhookHandler
from linebot.models import *

import os
import random
import re
from apps.common.common import *
from apps.randomNumber.template import random_number_page_template


line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))


# 亂數
def random_number_main(event, userMessage):

    if userMessage == "亂數":
        userMessage = "亂數：0 ~ 100"

    if userMessage.find('亂數：') == 0:

        # 整理字串：去除前面關鍵字，只保留數字
        userMessage = userMessage.replace('亂數：', '')

        # 取得亂數區間 random_range 陣列
        random_range = re.findall(r'\b\d+\b', userMessage)

        # 取得亂數最小值、最大值
        min_num, max_num = get_random_min_max(random_range)

        # 取得亂數 random_number
        random_number = random.randint(min_num, max_num)

        # flexMessage 容器
        flex_message_contents = []

        # flexMessage 一頁的內容
        pageTemplate = random_number_page_template(random_number, min_num, max_num)
        
        # 將內容放入 flex_message_contents 中
        flex_message_contents.append(pageTemplate)

        # 包裝訊息
        flex_message = FlexSendMessage(
            alt_text= '新的亂數產生了！',
            contents={
                "type": "carousel",
                "contents": flex_message_contents
                }
            )
        
        # 發送訊息
        line_bot_api.reply_message(event.reply_token, flex_message)
        return


# 取得亂數區間
def get_random_min_max(list):
    """
        如果亂數區間只有上限，例如:"98" -> "0","98"
        如果亂數區間有上下限，例如:"30～50" -> "30","50"
        回傳 min 與 max
    """
    
    # 亂數區間只有上限
    if len(list) == 1:
        return 0, int(list[0])

    # 亂數區間有上下限
    elif len(list) == 2:
        if int(list[0]) < int(list[1]):
            return int(list[0]), int(list[1])
        if int(list[0]) > int(list[1]):
            return int(list[1]), int(list[0])
        if int(list[0]) == int(list[1]):
            return int(list[0]), int(list[1])
