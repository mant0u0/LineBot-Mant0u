# 日本神社抽籤（範例介面）
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

import os

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

def randomOkamikujiExample(event):
    # 包裝訊息
    flex_message = FlexSendMessage(
        alt_text='有人抽籤囉！',
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
                            # 抽籤結果圖片
                            {
                                "type": "image",
                                "url": "https://raw.githubusercontent.com/mant0u0/RandomImg/main/okamikuji/item-1.jpg",
                                "size": "full",
                                "aspectMode": "cover",
                                "aspectRatio": "1:1",
                                "gravity": "center"
                            },
                            # 抽籤結果文字
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
                                                        "text": "抽籤結果：大吉！？",
                                                        "size": "lg",
                                                        "color": "#10496d",
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
                            "text": "抽籤"
                        },
                    }


                },
                
                # 第二頁、抽籤內容 (pageTemplate)
                {
                    "type": "bubble",
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            # 抽籤運勢分析背景
                            {
                                "type": "image",
                                "url": "https://raw.githubusercontent.com/mant0u0/RandomImg/main/okamikuji/itemBg-1.jpg",
                                "size": "full",
                                "aspectMode": "cover",
                                "aspectRatio": "1:1"
                            },
                            # 抽籤運勢分析文字
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "大吉",
                                        "color": "#10496d",
                                        "wrap": True,
                                        "size": "md",
                                        "weight": "bold",
                                        "lineSpacing": "4px",
                                        "align": "center"
                                    },
                                    {
                                        "type": "text",
                                        "text": "大吉運勢結果說明，大吉運勢結果說明，大吉運勢結果說明，大吉運勢結果說明，大吉運勢結果說明，大吉運勢結果說明，大吉運勢結果說明。",
                                        "color": "#10496d",
                                        "wrap": True,
                                        "size": "md",
                                        "weight": "bold",
                                        "lineSpacing": "4px",
                                        "margin": "lg",
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