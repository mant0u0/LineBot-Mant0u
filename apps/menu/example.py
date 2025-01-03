# 指令說明選單（範例介面）

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

import os
from apps.common.common import *

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

def menuExample(event):
    # 包裝訊息
    flex_message = FlexSendMessage(
        alt_text='選單',
        contents={
            # JSON 格式貼這邊
            "type": "carousel",
            "contents": [
                #第一頁
                {
                    "type": "bubble",
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "image",
                                "url": localImg("banner/mant0u.png"),
                                "size": "100%",
                                "aspectMode": "fit",
                                "margin": "0px",
                                "position": "relative",
                                "aspectRatio": "1000:280"
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    # 標題
                                    {
                                        "type": "text",
                                        "text": "功能選單",
                                        "weight": "bold",
                                        "size": "lg",
                                        "color": "#10496d",
                                        "align": "center"
                                    }, {
                                        "type": "text",
                                        "text": "第一頁",
                                        "weight": "bold",
                                        "size": "sm",
                                        "color": "#10496d99",
                                        "align": "center",
                                        "margin": "4px"
                                    }, {
                                        "type": "separator",
                                        "margin": "12px"
                                    },

                                    # 選項
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                            {
                                                "type": "text",
                                                "text": "選項 1",
                                                "weight": "bold",
                                                "color": "#10496d"
                                            }
                                        ],
                                        "paddingAll": "12px",
                                        "justifyContent": "center",
                                        "alignItems": "center",
                                        "action": {
                                            "type": "message",
                                            "label": "action",
                                            "text": "訊息 1",
                                        }
                                    },
                                    # 分隔線
                                    {"type": "separator"},
                                    # 選項
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                            {
                                                "type": "text",
                                                "text": "選項 2",
                                                "weight": "bold",
                                                "color": "#10496d"
                                            }
                                        ],
                                        "paddingAll": "12px",
                                        "justifyContent": "center",
                                        "alignItems": "center",
                                        "action": {
                                            "type": "message",
                                            "label": "action",
                                            "text": "訊息 2",
                                        }
                                    },
                                    # 分隔線
                                    {"type": "separator"},
                                ],
                                "paddingAll": "12px"
                            }
                        ],
                        "paddingAll": "0px"
                    }
                },
                
                #第二頁
                {
                    "type": "bubble",
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "image",
                                "url": localImg("banner/mant0u.png"),
                                "size": "100%",
                                "aspectMode": "fit",
                                "margin": "0px",
                                "position": "relative",
                                "aspectRatio": "1000:280"
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    # 標題
                                    {
                                        "type": "text",
                                        "text": "功能選單",
                                        "weight": "bold",
                                        "size": "lg",
                                        "color": "#10496d",
                                        "align": "center"
                                    }, {
                                        "type": "text",
                                        "text": "第二頁",
                                        "weight": "bold",
                                        "size": "sm",
                                        "color": "#10496d99",
                                        "align": "center",
                                        "margin": "4px"
                                    }, {
                                        "type": "separator",
                                        "margin": "12px"
                                    },

                                    # 選項
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                            {
                                                "type": "text",
                                                "text": "選項 1",
                                                "weight": "bold",
                                                "color": "#10496d"
                                            }
                                        ],
                                        "paddingAll": "12px",
                                        "justifyContent": "center",
                                        "alignItems": "center",
                                        "action": {
                                            "type": "message",
                                            "label": "action",
                                            "text": "訊息 1",
                                        }
                                    },
                                    # 分隔線
                                    {"type": "separator"},
                                    # 選項
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                            {
                                                "type": "text",
                                                "text": "選項 2",
                                                "weight": "bold",
                                                "color": "#10496d"
                                            }
                                        ],
                                        "paddingAll": "12px",
                                        "justifyContent": "center",
                                        "alignItems": "center",
                                        "action": {
                                            "type": "message",
                                            "label": "action",
                                            "text": "訊息 2",
                                        }
                                    },
                                    # 分隔線
                                    {"type": "separator"},
                                ],
                                "paddingAll": "12px"
                            }
                        ],
                        "paddingAll": "0px"
                    }
                },
                      
            ]
            }
        )
    # 發送訊息
    line_bot_api.reply_message(event.reply_token, flex_message)

def menuDetailExample(event):
    # 包裝訊息
    flex_message = FlexSendMessage(
        alt_text='指令說明',
        contents={
            # JSON 格式貼這邊
            "type": "carousel",
            "contents": [
                #第一頁
                {
                    "type": "bubble",
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "image",
                                "url": localImg("banner/mant0u.png"),
                                "size": "100%",
                                "aspectMode": "fit",
                                "margin": "0px",
                                "position": "relative",
                                "aspectRatio": "1000:280"
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    # H1 標題
                                    {
                                        "text": "H1 標題",
                                        "type": "text",
                                        "size": "xl",
                                        "color": "#10496d",
                                        "weight": "bold"
                                    },
                                    # H2 標題
                                    {
                                        "text": "H2 標題",
                                        "type": "text",
                                        "size": "md",
                                        "color": "#10496d",
                                        "weight": "bold",
                                        "margin": "8px"
                                    },
                                    # p 文字
                                    {
                                        "type": "text",
                                        "margin": "8px",
                                        "size": "sm",
                                        "wrap": True,
                                        "weight": "bold",
                                        "lineSpacing": "4px",
                                        "color": "#10496d"+"99",
                                        "contents": [
                                            {
                                                "type": "span",
                                                "text": "一般文字一般文字一般文字一般文字一般文字一般文字一般文字一般文字一般文字一般文字"
                                            },
                                            {
                                                "type": "span",
                                                "text": "重點",
                                                "color": "#eb4846",
                                                "decoration": "underline"
                                            },
                                            {
                                                "type": "span",
                                                "text": "一般文字一般文字一般文字一般文字一般文字一般文字一般文字一般文字一般文字一般文字"
                                            },
                                        ],
                                    },
                                    # H2 標題
                                    {
                                        "text": "H2 標題 - 第二段",
                                        "type": "text",
                                        "size": "md",
                                        "color": "#10496d",
                                        "weight": "bold",
                                        "margin": "8px"
                                    },
                                    # p 文字
                                    {
                                        "type": "text",
                                        "margin": "8px",
                                        "size": "sm",
                                        "wrap": True,
                                        "weight": "bold",
                                        "lineSpacing": "4px",
                                        "color": "#10496d"+"99",
                                        "contents": [
                                            {
                                                "type": "span",
                                                "text": "一般文字第二段一般文字第二段一般文字一般文字一般文字一般文字一般文字一般文字一般文字一般文字"
                                            },
                                        ],
                                    },
                                ],
                                "paddingAll": "12px"
                            }
                        ],
                        "paddingAll": "0px"
                    }
                },
                
                #第二頁
                {
                    "type": "bubble",
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "image",
                                "url": localImg("banner/mant0u.png"),
                                "size": "100%",
                                "aspectMode": "fit",
                                "margin": "0px",
                                "position": "relative",
                                "aspectRatio": "1000:280"
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    # H1 標題
                                    {
                                        "text": "H1 標題",
                                        "type": "text",
                                        "size": "xl",
                                        "color": "#10496d",
                                        "weight": "bold"
                                    },
                                    # H2 標題
                                    {
                                        "text": "H2 標題",
                                        "type": "text",
                                        "size": "md",
                                        "color": "#10496d",
                                        "weight": "bold",
                                        "margin": "8px"
                                    },
                                    # p 文字
                                    {
                                        "type": "text",
                                        "margin": "8px",
                                        "size": "sm",
                                        "wrap": True,
                                        "weight": "bold",
                                        "lineSpacing": "4px",
                                        "color": "#10496d"+"99",
                                        "contents": [
                                            {
                                                "type": "span",
                                                "text": "一般文字一般文字一般文字一般文字一般文字一般文字一般文字一般文字一般文字一般文字"
                                            },
                                            {
                                                "type": "span",
                                                "text": "重點",
                                                "color": "#eb4846",
                                                "decoration": "underline"
                                            },
                                            {
                                                "type": "span",
                                                "text": "一般文字一般文字一般文字一般文字一般文字一般文字一般文字一般文字一般文字一般文字"
                                            },
                                        ],
                                    },
                                    
                                ],
                                "paddingAll": "12px"
                            }
                        ],
                        "paddingAll": "0px"
                    }
                },
                
            ]
        },
        quick_reply=QuickReply(
            items=[
                QuickReplyButton(
                    action=MessageAction(label="問天氣", text="饅頭：今天天氣如何？")
                ),
                QuickReplyButton(
                    action=MessageAction(label="問運勢", text="饅頭：今天運勢如何？")
                ),
                QuickReplyButton(
                    action=MessageAction(label="更多指令 ➜", text="指令說明")
                ),
            ]
        ),
    )
    # 發送訊息
    line_bot_api.reply_message(event.reply_token, flex_message)