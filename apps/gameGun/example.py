# 手槍（範例介面）

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

import os

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

def gameGunExample(event):
    # 包裝訊息
    flex_message = FlexSendMessage(
        alt_text='手槍 6 發裝子彈！',
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
                        "url": "https://raw.githubusercontent.com/mant0u0/RandomImg/main/gun/ready.png",
                        "size": "full",
                        "aspectRatio": "1:1",
                        "aspectMode": "cover"
                    },
                    # 剩下...的文字
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "剩下 6 發",
                                "color": "#ffffff",
                                "align": "center",
                                "size": "xs"
                            }
                        ],
                        "position": "absolute",
                        "cornerRadius": "20px",
                        "backgroundColor": "#22af9e",
                        "paddingAll": "4px",
                        "paddingStart": "8px",
                        "paddingEnd": "8px",
                        "offsetTop": "20px",
                        "maxWidth": "100px",
                        "offsetStart": "20px"
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
                            "color": "#10665a",
                            "text": "手槍 6 發裝子彈！"
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
                        "text": "開槍"
                    },
                }
                }

            ]
        }
    )
    # 發送訊息
    line_bot_api.reply_message(event.reply_token, flex_message)