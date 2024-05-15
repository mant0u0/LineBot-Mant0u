# 骰子（範例介面）

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

import os
from apps.common.common import *

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

def randomDiceExample(event):
    # 包裝訊息
    flex_message = FlexSendMessage(
        alt_text='有人擲出骰子！',
        contents={
            # JSON 格式貼這邊
            "type": "carousel",
            "contents": [

                # 第一頁 (pageTemplate)
                {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    # 背景圖
                    {
                        "type": "image",
                        "url": localImg("randomDice/background.png"),
                        "size": "full",
                        "aspectRatio": "1:1",
                        "aspectMode": "cover"
                    },
                    # 骰子 (最底層)
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "image",
                            "url": localImg("randomDice/1.png"),
                            "size": "xl" # 骰子尺寸
                        }
                        ],
                        "position": "absolute",
                        "width": "100%",
                        "height": "75%",
                        "justifyContent": "center",
                        "alignItems": "center",
                        "offsetStart": "0%", # X 位移
                        "offsetTop": "-10%"  # Y 位移
                    },
                    # 骰子 
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "image",
                            "url": localImg("randomDice/1.png"),
                            "size": "xl"
                        }
                        ],
                        "position": "absolute",
                        "width": "100%",
                        "height": "75%",
                        "justifyContent": "center",
                        "alignItems": "center",
                        "offsetStart": "-20%", 
                        "offsetTop": "7%" 
                    },
                    # 骰子
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "image",
                            "url": localImg("randomDice/1.png"),
                            "size": "xl"
                        }
                        ],
                        "position": "absolute",
                        "width": "100%",
                        "height": "75%",
                        "justifyContent": "center",
                        "alignItems": "center",
                        "offsetStart": "20%",
                        "offsetTop": "7%"
                    },
                    # 底部圖片
                    {
                        "type": "image",
                        "url": localImg("randomDice/bottom.png"),
                        "size": "full",
                        "aspectRatio": "1:1",
                        "aspectMode": "cover",
                        "position": "absolute"
                    },
                    # 底部文字
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                        {
                            "type": "text",
                            "size": "lg",
                            "weight": "bold",
                            "align": "center",
                            "color": "#93563b",
                            "text": "骰子擲出 6 點"
                        }
                        ],
                        "position": "absolute",
                        "offsetStart": "0px",
                        "paddingAll": "20px",
                        "offsetBottom": "0px",
                        "offsetEnd": "0px"
                    }
                    ],
                    "paddingAll": "0px",
                    "action": {
                        "type": "message",
                        "label": "action",
                        "text": "骰子：3" ,
                    },
                }
                }

            ]
        }
    )
    # 發送訊息
    line_bot_api.reply_message(event.reply_token, flex_message)