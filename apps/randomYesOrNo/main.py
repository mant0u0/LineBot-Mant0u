from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

import os
import random

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

# 主要
def random_yes_or_no_main(event, userMessage):
    # 取得重複字元 (陣列：只會使用第 0 個元素 repeated_chars[0] )
    repeated_chars = check_yes_or_no(userMessage)

    # 亂數(0～1)：肯定 1 或否定 0
    randomNum = random.randint(0, 1)

    # 肯定
    if randomNum == 1:
        if random.randrange(0, 2) == 0:
            result_text = repeated_chars[0] + "！"
        else:
            result_text = "問就是" + repeated_chars[0] + "！"
    # 否定
    else:
        # 字串為「有沒有」
        if repeated_chars[0] == "有":
            result_text = "沒" + repeated_chars[0] + "！"
        # 字串為「X不X」、「是不是」、「好不好」、「對不對」...
        else:
            result_text = "不" + repeated_chars[0] + "！"

    # 包裝訊息
    text_message = TextSendMessage(
        text = result_text,
    )
    # 發送訊息
    line_bot_api.reply_message(event.reply_token, text_message)


def random_yes_or_no_main_return(userMessage):
    # 取得重複字元 (陣列：只會使用第 0 個元素 repeated_chars[0] )
    repeated_chars = check_yes_or_no(userMessage)

    # 亂數(0～1)：肯定 1 或否定 0
    randomNum = random.randint(0, 1)

    # 肯定
    if randomNum == 1:
        if random.randrange(0, 2) == 0:
            result_text = repeated_chars[0] + "！"
        else:
            result_text = "問就是" + repeated_chars[0] + "！"
    # 否定
    else:
        # 字串為「有沒有」
        if repeated_chars[0] == "有":
            result_text = "沒" + repeated_chars[0] + "！"
        # 字串為「X不X」、「是不是」、「好不好」、「對不對」...
        else:
            result_text = "不" + repeated_chars[0] + "！"

    # 包裝訊息
    text_message = TextSendMessage(
        text = result_text,
    )
    return text_message


# 判斷是否為「X不X」、「有沒有」句型，並取得重複字元
def check_yes_or_no(userMessage):
    count = userMessage.count("不")
    if count >= 1:
        indices = [i for i, x in enumerate(userMessage) if x == "不"]
        repeated_chars = []
        for index in indices:
            if index > 0 and index < len(userMessage) - 1:
                if userMessage[index - 1] == userMessage[index + 1]:
                    if userMessage[index - 1] not in repeated_chars:
                        repeated_chars.append(userMessage[index - 1])
        return repeated_chars
    elif userMessage.find('有沒有') >= 0:
        repeated_chars = ["有"]
        return repeated_chars
    else:
        return None