# 洗牌（範例介面）
from linebot import LineBotApi
from linebot.models import *

import os
from apps.common.common import *


line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))

def randomShuffleExample(event):
    # 包裝訊息
    flex_message = FlexSendMessage(
        alt_text='有人在洗牌！',
        contents={
            # JSON 格式貼這邊
            "type": "carousel",
            "contents": [
                {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "image",
                        "size": "full",
                        "aspectMode": "cover",
                        "aspectRatio": "1:1",
                        "gravity": "top",
                        "url": "https://raw.githubusercontent.com/mant0u0/RandomImg/refs/heads/main/transparent_background.png"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
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
                                    "layout": "vertical",
                                    "contents": [],
                                    "width": "100%",
                                    "height": "100%",
                                    "backgroundColor": "#73A7D9",
                                    "cornerRadius": "8px",
                                    "position": "absolute"
                                },
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                    {
                                        "type": "text",
                                        "text": "卡片 1",
                                        "size": "xs",
                                        "color": "#2168a3",
                                        "maxLines": 3,
                                        "wrap": True,
                                        "align": "center",
                                        "weight": "bold",
                                        "lineSpacing": "2px"
                                    }
                                    ],
                                    "width": "100%",
                                    "height": "96%",
                                    "backgroundColor": "#FFFFFF",
                                    "borderWidth": "3px",
                                    "borderColor": "#c0e0ff",
                                    "cornerRadius": "8px",
                                    "position": "absolute",
                                    "paddingAll": "2px",
                                    "alignItems": "center",
                                    "justifyContent": "center"
                                }
                                ],
                                "width": "64px",
                                "height": "88px",
                                "action": {
                                "type": "message",
                                "label": "翻牌：1",
                                "text": "翻牌：1"
                                }
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [],
                                    "width": "100%",
                                    "height": "100%",
                                    "backgroundColor": "#73A7D9",
                                    "cornerRadius": "8px",
                                    "position": "absolute"
                                },
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                    {
                                        "type": "text",
                                        "text": "卡片 2",
                                        "size": "xs",
                                        "color": "#2168a3",
                                        "maxLines": 3,
                                        "wrap": True,
                                        "align": "center",
                                        "weight": "bold",
                                        "lineSpacing": "2px"
                                    }
                                    ],
                                    "width": "100%",
                                    "height": "96%",
                                    "backgroundColor": "#FFFFFF",
                                    "borderWidth": "3px",
                                    "borderColor": "#c0e0ff",
                                    "cornerRadius": "8px",
                                    "position": "absolute",
                                    "paddingAll": "2px",
                                    "alignItems": "center",
                                    "justifyContent": "center"
                                }
                                ],
                                "width": "64px",
                                "height": "88px",
                                "action": {
                                "type": "message",
                                "label": "翻牌：2",
                                "text": "翻牌：2"
                                }
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [],
                                    "width": "100%",
                                    "height": "100%",
                                    "backgroundColor": "#73A7D9",
                                    "cornerRadius": "8px",
                                    "position": "absolute"
                                },
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                    {
                                        "type": "text",
                                        "text": "卡片 3",
                                        "size": "xs",
                                        "color": "#2168a3",
                                        "maxLines": 3,
                                        "wrap": True,
                                        "align": "center",
                                        "weight": "bold",
                                        "lineSpacing": "2px"
                                    }
                                    ],
                                    "width": "100%",
                                    "height": "96%",
                                    "backgroundColor": "#FFFFFF",
                                    "borderWidth": "3px",
                                    "borderColor": "#c0e0ff",
                                    "cornerRadius": "8px",
                                    "position": "absolute",
                                    "paddingAll": "2px",
                                    "alignItems": "center",
                                    "justifyContent": "center"
                                }
                                ],
                                "width": "64px",
                                "height": "88px",
                                "action": {
                                "type": "message",
                                "label": "翻牌：3",
                                "text": "翻牌：3"
                                }
                            }
                            ],
                            "width": "100%",
                            "justifyContent": "center",
                            "spacing": "16px"
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
                                    "layout": "vertical",
                                    "contents": [],
                                    "width": "100%",
                                    "height": "100%",
                                    "backgroundColor": "#73A7D9",
                                    "cornerRadius": "8px",
                                    "position": "absolute"
                                },
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                    {
                                        "type": "text",
                                        "text": "卡片 4",
                                        "size": "xs",
                                        "color": "#2168a3",
                                        "maxLines": 3,
                                        "wrap": True,
                                        "align": "center",
                                        "weight": "bold",
                                        "lineSpacing": "2px"
                                    }
                                    ],
                                    "width": "100%",
                                    "height": "96%",
                                    "backgroundColor": "#FFFFFF",
                                    "borderWidth": "3px",
                                    "borderColor": "#c0e0ff",
                                    "cornerRadius": "8px",
                                    "position": "absolute",
                                    "paddingAll": "2px",
                                    "alignItems": "center",
                                    "justifyContent": "center"
                                }
                                ],
                                "width": "64px",
                                "height": "88px",
                                "action": {
                                "type": "message",
                                "label": "翻牌：1",
                                "text": "翻牌：1"
                                }
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [],
                                    "width": "100%",
                                    "height": "100%",
                                    "backgroundColor": "#4C88C2",
                                    "cornerRadius": "8px",
                                    "position": "absolute"
                                },
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                    {
                                        "type": "image",
                                        "url": "https://raw.githubusercontent.com/mant0u0/RandomImg/refs/heads/main/card.jpg",
                                        "size": "xl",
                                        "aspectRatio": "64:88",
                                        "aspectMode": "cover"
                                    }
                                    ],
                                    "position": "absolute",
                                    "width": "100%",
                                    "height": "96%",
                                    "cornerRadius": "8px"
                                }
                                ],
                                "width": "64px",
                                "height": "88px",
                                "action": {
                                "type": "message",
                                "label": "翻牌：2",
                                "text": "翻牌：2"
                                }
                            }
                            ],
                            "width": "100%",
                            "justifyContent": "center",
                            "spacing": "16px"
                        }
                        ],
                        "width": "100%",
                        "height": "100%",
                        "position": "absolute",
                        "justifyContent": "center",
                        "alignItems": "center",
                        "paddingAll": "12px",
                        "spacing": "8px"
                    }
                    ],
                    "paddingAll": "0px"
                },
                "styles": {
                    "body": {
                    "backgroundColor": "#f2f3f4"
                    }
                }
                }
            ]
        }
    )
    # 發送訊息
    line_bot_api.reply_message(event.reply_token, flex_message)









