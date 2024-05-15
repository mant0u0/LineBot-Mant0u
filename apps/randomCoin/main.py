# 擲硬幣功能

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

import os
import random
from apps.common.common import *

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

def randomCoinMain(event):

    # 定義硬幣狀態、類型
    coin_status = [
        {
            "text": "正面",
            "id": "1"
        },{
            "text": "反面",
            "id": "0"
        },
    ]
    coin_type = [
        {
            "text": "金幣",
            "id": "G",
        },
        {
            "text": "銀幣",
            "id": "S",
        },
        {
            "text": "銅幣",
            "id": "C",
        },
    ]

    # 亂數決定硬幣狀態、類型、圖片（硬幣正面有不同選轉方向）、閃光效果圖片
    random_status = random.choice(coin_status)
    random_type   = random.choice(coin_type)
    random_img    = str(random.randint(1, 3))
    random_light  = "L" + str(random.randint(0, 3))

    # 結果文字
    result_text = "擲出一枚" + random_type["text"] + random_status["text"] + "！"

    if random_status["text"] == "反面":
        result_coin_img = random_type["id"] + random_status["id"]
    if random_status["text"] == "正面":
        result_coin_img = random_type["id"] + random_status["id"] + random_img


    # flexMessage 容器
    flex_message_contents = []

    # flexMessage 一頁的內容
    pageTemplate = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                # 背景圖片
                {
                    "type": "image",
                    "url": localImg(f"randomCoin/BG0.png"),
                    "size": "full",
                    "aspectMode": "cover",
                    "aspectRatio": "1:1",
                },
                # 硬幣圖片
                {
                    "type": "image",
                    "url": localImg(f"randomCoin/{result_coin_img}.png"),
                    "size": "full",
                    "aspectMode": "cover",
                    "aspectRatio": "1:1",
                    "position": "absolute",
                },
                # 閃光效果
                {
                    "type": "image",
                    "url": localImg(f"randomCoin/{random_light}.png"),
                    "size": "full",
                    "aspectMode": "cover",
                    "aspectRatio": "1:1",
                    "position": "absolute",
                },
                # 底部結果文字的背景
                {
                    "type": "image",
                    "url": localImg(f"randomCoin/BG1.png"),
                    "size": "full",
                    "aspectMode": "cover",
                    "aspectRatio": "1:1",
                    "position": "absolute",
                },
                # 結果文字
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": result_text,
                                            "size": "lg",
                                            "color": "#93563b",
                                            "weight": "bold",
                                            "align": "center"
                                        }
                                    ]
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
            ],
            "paddingAll": "0px",
            "action": {
                "type": "message",
                "label": "action",
                "text": "硬幣"
            },
        }
    }

    # 將 pageTemplate 放入 flex_message_contents 中
    flex_message_contents.append( pageTemplate )

    # 包裝訊息
    flex_message = FlexSendMessage(
        alt_text= '有人擲出硬幣！',
        contents={
            "type": "carousel",
            "contents": flex_message_contents
            }
        )
    
    # 發送訊息
    line_bot_api.reply_message(event.reply_token, flex_message)

