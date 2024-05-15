# 擲筊（範例介面）
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

import os

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

def randomBwaBweiExample(event):
    # 包裝訊息
    flex_message = FlexSendMessage(
        alt_text='有人在擲筊！',
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
                            {
                                "type": "image",
                                "url": "https://raw.githubusercontent.com/mant0u0/RandomImg/main/bwaBwei/00-1.png",
                                "size": "full",
                                "aspectMode": "cover",
                                "aspectRatio": "1:1",
                            },
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
                                                        "text": "無筊！",
                                                        "size": "lg",
                                                        "color": "#c93a38",
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
                            "text": "擲筊"
                        },
                    }
                },




                
                # 第二頁、擲筊內容 (pageTemplate)
                {
                    "type": "bubble",
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "image",
                                "url": "https://raw.githubusercontent.com/mant0u0/RandomImg/main/bwaBwei/BG.jpg",
                                "size": "full",
                                "aspectMode": "cover",
                                "aspectRatio": "1:1"
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "image",
                                        "url": "https://raw.githubusercontent.com/mant0u0/RandomImg/main/bwaBwei/icon-XX.png",
                                        "size": "xxs",
                                    },
                                    {
                                        "type": "text",
                                        "text": "擲筊內容擲筊內容擲筊內容擲筊內容擲筊內容擲筊內容擲筊內容擲筊內容擲筊內容擲筊內容",
                                        "color": "#c93a38",
                                        "wrap": True,
                                        "size": "md",
                                        "weight": "bold",
                                        "lineSpacing": "8px",
                                        "margin": "lg",
                                    },
                                    {
                                        "type": "text",
                                        "text": "　",
                                        "wrap": True,
                                        "size": "md",
                                        "weight": "bold",
                                        "lineSpacing": "8px",
                                        "margin": "md",
                                    }
                                ],
                                "position": "absolute",
                                "width": "100%",
                                "height": "100%",
                                "justifyContent": "center",
                                "alignItems": "center",
                                "paddingAll": "12%"
                            }
                        ],
                        "paddingAll": "0px"
                    }
                }

            ]
            }
    )
    # 發送訊息
    line_bot_api.reply_message(event.reply_token, flex_message)