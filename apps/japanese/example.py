# 日文單字卡（範例）
from linebot import LineBotApi
from linebot.models import *

import os
import random
import re
import requests
from difflib import SequenceMatcher

from apps.common.common import *

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))

def japaneseWordCardsExample(event):
    # 包裝訊息
    flex_message = FlexSendMessage(
        alt_text='日文單字',
        contents={
            # JSON 格式貼這邊
            "type": "carousel",
            "contents": [
                {
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "url": localImg("banner/mant0u.png"),
                    "size": "full",
                    "aspectRatio": "1000:280",
                    "aspectMode": "cover",
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        # 第一行文字
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "justifyContent": "center",
                            "margin": "4px",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "justifyContent": "flex-end",
                                    "flex": 0,
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "わたし",
                                            "size": "xxs",
                                            "weight": "bold",
                                            "align": "center",
                                            "color": "#19558a",
                                        },
                                        {
                                            "type": "text",
                                            "text": "私",
                                            "size": "xxl",
                                            "weight": "bold",
                                            "align": "center",
                                            "color": "#19558a",
                                        }
                                    ],
                                },
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "justifyContent": "flex-end",
                                    "flex": 0,
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "はです。",
                                            "size": "xxl",
                                            "weight": "bold",
                                            "align": "center",
                                            "color": "#19558a",
                                        }
                                    ],
                                }   
                            ]
                        },

                        # 第二行文字
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "justifyContent": "center",
                            "margin": "4px", 
                            "contents": [
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                {
                                    "type": "text",
                                    "text": "わたし",
                                    "size": "xxs",
                                    "weight": "bold",
                                    "align": "center"
                                },
                                {
                                    "type": "text",
                                    "text": "私",
                                    "size": "xxl",
                                    "weight": "bold",
                                    "align": "center"
                                }
                                ],
                                "justifyContent": "flex-end",
                                "flex": 0
                            }
                            ],
                        }
                    ],
                    "justifyContent": "center"
                }
                }
            
            ]
            }
        )
    # 發送訊息
    line_bot_api.reply_message(event.reply_token, flex_message)




