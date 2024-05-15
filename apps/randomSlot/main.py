# 亂數產生

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

import os
import random
from apps.common.common import *

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))


def randomSlotMain(event):
    slot_layout = slot_reset_layout()  # 版面重置
    connected_elements = slot_check_connections(slot_layout)  # 檢查連線

    # 強制連線
    if random.random() > 0.6:
        slot_item = ["1", "1", "1", "1", "1", "1", "1", "2", "2",
                     "2", "2", "2", "3", "3", "3", "3", "4", "4", "7", "7"]
        slot_force_connection(
            slot_layout, random.choice(slot_item))  # 強制連線函數
        connected_elements = slot_check_connections(slot_layout)  # 檢查連線

    # 版面列印
    slotContents = slot_contents_print(slot_layout, connected_elements)

    # flexMessage 容器
    flex_message_contents = []

    # flexMessage 一頁的內容
    pageTemplate = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": slotContents,
            "paddingAll": "0px",
            "action": {
                "type": "message",
                "label": "action",
                "text": "拉霸"
            },
        }
    }


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



# slot 版面列印
def slot_contents_print(slot_layout, connected_elements):
    slotContents = []
    # 背景
    slotBg = {
        "type": "image",
        "url": localImg(f"randomSlot/bg/1.png"),
        "size": "full",
        "aspectMode": "cover",
        "aspectRatio": "1:1",
    }
    slotContents.append(slotBg)

    # 項目
    for col in range(3):
        for row in range(3):
            slotItem = {
                "type": "image",
                "url": localImg("randomSlot/"+str(col)+str(row)+"/"+str(slot_layout[col][row])+".png"),
                "size": "full",
                "aspectMode": "cover",
                "aspectRatio": "1:1",
                "position": "absolute",
            }
            slotContents.append(slotItem)

    # 文字
    if len(connected_elements) == 0:
        slotTextContents = [
            {
                "type": "text",
                "text": " 沒有任何連線～",
                "size": "lg",
                "color": "#93563b",
                "weight": "bold",
                "flex": 0,
            }
        ]
    else:
        slotTextContents = [
            {
                "type": "icon",
                "size": "xxl",
                "url": localImg("randomSlot/icon/"+str(connected_elements[0])+".png"),
                "offsetTop": "8px",
            },
            {
                "type": "text",
                "text": " 出現連線了！",
                "size": "lg",
                "color": "#93563b",
                "weight": "bold",
                "flex": 0,
            }
        ]
    slotText = {
        "type": "box",
        "layout": "horizontal",
        "contents": [
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "box",
                        "layout": "baseline",
                        "contents": slotTextContents,
                        "justifyContent": "center",
                    }
                ],
                "spacing": "xs"
            }
        ],
        "position": "absolute",
        "offsetBottom": "0px",
        "offsetStart": "0px",
        "offsetEnd": "0px",
        "paddingAll": "20px"
    }
    slotContents.append(slotText)

    return slotContents


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

