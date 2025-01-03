# 亂數產生

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

import os
import random
from apps.common.common import *
from apps.randomSlot.template import *


line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))


def random_slot_main(event):
    slot_layout = slot_reset_layout()  # 版面重置
    connected_elements = slot_check_connections(slot_layout)  # 檢查連線

    # 強制連線
    if random.random() > 0.6:
        slot_item = ["1", "1", "1", "1", "1", "1", "1", "2", "2",
                     "2", "2", "2", "3", "3", "3", "3", "4", "4", "7", "7"]
        slot_force_connection(
            slot_layout, random.choice(slot_item))  # 強制連線函數
        connected_elements = slot_check_connections(slot_layout)  # 檢查連線

    # flexMessage 容器
    flex_message_contents = []

    # flexMessage 一頁的內容
    pageTemplate = random_slot_page_template(slot_layout, connected_elements)

    # 將內容放入 flex_message_contents 中
    flex_message_contents.append(pageTemplate)

    # 包裝訊息
    flex_message = FlexSendMessage(
        alt_text= '拉霸機轉動！',
        contents={
            "type": "carousel",
            "contents": flex_message_contents
            }
        )
    # 發送訊息
    line_bot_api.reply_message(event.reply_token, flex_message)





# slot 檢查連線
def slot_check_connections(layout):
    connected_elements = []
    # 檢查水平連線
    for row in layout:
        if row[0] == row[1] == row[2]:
            connected_elements.append(row[0])
    # 檢查垂直連線
    for col in range(3):
        if layout[0][col] == layout[1][col] == layout[2][col]:
            connected_elements.append(layout[0][col])
    # 檢查對角線連線
    if layout[0][0] == layout[1][1] == layout[2][2]:
        connected_elements.append(layout[0][0])
    if layout[0][2] == layout[1][1] == layout[2][0]:
        connected_elements.append(layout[0][2])

    return connected_elements


# slot 版面重置
def slot_reset_layout():
    slot_item = ["0", "1", "2", "3", "4", "7"]
    slot_layout_random = [
        [
            random.choice(slot_item),
            random.choice(slot_item),
            random.choice(slot_item)
        ],
        [
            random.choice(slot_item),
            random.choice(slot_item),
            random.choice(slot_item)
        ],
        [
            random.choice(slot_item),
            random.choice(slot_item),
            random.choice(slot_item)
        ],
    ]
    return slot_layout_random


# slot 強制連線（item：要連線的元素）
def slot_force_connection(slot_layout, item):
    random_connections = random.randint(1, 5)
    if random_connections == 1:
        slot_layout[0][0] = slot_layout[0][1] = slot_layout[0][2] = item
    elif random_connections == 2:
        slot_layout[1][0] = slot_layout[1][1] = slot_layout[1][2] = item
    elif random_connections == 3:
        slot_layout[2][0] = slot_layout[2][1] = slot_layout[2][2] = item
    elif random_connections == 4:
        slot_layout[0][0] = slot_layout[1][1] = slot_layout[2][2] = item
    elif random_connections == 5:
        slot_layout[2][0] = slot_layout[1][1] = slot_layout[0][2] = item

