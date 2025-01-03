# 撲克牌（範例介面）

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

import os

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

def randomPokerExample(event):
    # 包裝訊息
    flex_message = FlexSendMessage(
        alt_text='有人在抽牌！',
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
                            # 第一頁的內容 (pageTemplate_contents)

                            # 背景 (pageTemplate_BG)
                            {
                                "type": "image",
                                "url": "https://raw.githubusercontent.com/mant0u0/RandomImg/main/poker/BG.png",
                                "size": "full",
                                "aspectMode": "cover",
                                "aspectRatio": "1:1",
                                "gravity": "top"
                            },
                            # 文字 (pageTemplate_text)
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                            {
                                                "type": "text",
                                                "text": "♥2 ♠A",
                                                "size": "lg",
                                                "weight": "bold",
                                                "color": "#208148",
                                                "align": "center"
                                            }
                                        ],
                                        "paddingAll": "20px"
                                    }
                                ],
                                "position": "absolute",
                                "width": "100%",
                                "height": "100%",
                                "justifyContent": "flex-end"
                            },

                            # 撲克牌 
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "image",
                                        "url": "https://raw.githubusercontent.com/mant0u0/RandomImg/main/poker/H2.png",
                                        "size": "180px"
                                    }
                                ],
                                "position": "absolute",
                                "paddingAll": "20px",
                                "width": "100%",
                                # 撲克牌位置
                                "offsetStart": "-70px"
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "image",
                                        "url": "https://raw.githubusercontent.com/mant0u0/RandomImg/main/poker/SA.png",
                                        "size": "180px"
                                    }
                                ],
                                "position": "absolute",
                                "paddingAll": "20px",
                                "width": "100%",
                                # 撲克牌位置
                                "offsetStart": "-50px"
                            },

                        ],
                        "paddingAll": "0px",
                        "action": {
                            "type": "message",
                            "label": "action",
                            "text": "撲克牌：1" ,
                        },
                    }
                },

            ]
            }
    )
    # 發送訊息
    line_bot_api.reply_message(event.reply_token, flex_message)