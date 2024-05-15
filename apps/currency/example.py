# 貨幣換算 訊息範例

from linebot import LineBotApi
from linebot.models import *

import os
from apps.common.common import *

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))

def currencyExample(event):
    # 包裝訊息
    flex_message = FlexSendMessage(
        alt_text='貨幣換算',
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
                    # 頂端 banner
                    {
                        "type": "image",
                        # "url": "https://line-mant0u-bot-vercel.vercel.app/static/images/banner/mant0u.png",
                        "url": localImg("banner/mant0u.png"),
                        "size": "100%",
                        "aspectMode": "fit",
                        "margin": "0px",
                        "position": "relative",
                        "aspectRatio": "1000:280"
                    },
                    # 貨幣換算內容
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            # 標題
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                    {
                                    "type": "text",
                                    "text": "貨幣換算",
                                    "color": "#19558a",
                                    "size": "lg",
                                    "weight": "bold",
                                    "flex": 0
                                    },
                                    {
                                    "type": "text",
                                    "text": "資料來源 Coinbase",
                                    "color": "#19558a66",
                                    "size": "xs",
                                    "weight": "bold",
                                    "margin": "8px",
                                    "gravity": "center",
                                    "align": "end",
                                    "offsetTop": "2px"
                                    }
                                ],
                                "paddingBottom": "6px"
                            },
                            # ============================================ #
                            # 原始貨幣
                            {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                    "type": "text",
                                    "text": "台幣",
                                    "color": "#19558a",
                                    "weight": "bold",
                                    "size": "sm"
                                    }
                                ],
                                "flex": 0
                                },
                                {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                    "type": "text",
                                    "color": "#19558a",
                                    "weight": "bold",
                                    "size": "sm",
                                    "contents": [
                                        {
                                        "type": "span",
                                        "text": "10,000",
                                        "decoration": "line-through",
                                        "color": "#19558a99"
                                        },
                                        {
                                        "type": "span",
                                        "text": " · "
                                        },
                                        {
                                        "type": "span",
                                        "text": "8 折"
                                        }
                                    ]
                                    }
                                ],
                                "alignItems": "flex-end"
                                }
                            ],
                            "paddingBottom": "4px",
                            "paddingTop": "4px"
                            },
                            {
                            "type": "box",
                            "layout": "baseline",
                            "contents": [
                                {
                                "type": "text",
                                "text": "8,000",
                                "color": "#19558a",
                                "weight": "bold",
                                "align": "end",
                                "size": "xl"
                                },
                                {
                                "type": "text",
                                "text": "TWD",
                                "color": "#19558a",
                                "weight": "bold",
                                "align": "end",
                                "size": "md",
                                "flex": 0,
                                "margin": "8px"
                                }
                            ],
                            "backgroundColor": "#e3f2ff",
                            "paddingAll": "12px",
                            "cornerRadius": "12px",
                            "paddingBottom": "4px",
                            "paddingTop": "8px"
                            },
                            {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                "type": "text",
                                "text": "便宜 1,000 台幣！",
                                "color": "#19558a88",
                                "size": "sm",
                                "weight": "bold",
                                "align": "center"
                                }
                            ],
                            "paddingTop": "6px"
                            },
                            # ============================================ #
                            # 向下箭頭
                            {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                "type": "image",
                                # "url": "https://line-mant0u-bot-vercel.vercel.app/static/images/down-arrow.png",
                                "url": localImg("down-arrow.png"),
                                "size": "12px"
                                }
                            ],
                            "alignItems": "center",
                            "paddingTop": "8px"
                            },
                            # ============================================ #
                            # 換算貨幣
                            {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                    "type": "text",
                                    "text": "台幣",
                                    "color": "#19558a",
                                    "weight": "bold",
                                    "size": "sm"
                                    }
                                ],
                                "flex": 0
                                },
                                {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                    "type": "text",
                                    "color": "#19558a",
                                    "weight": "bold",
                                    "size": "sm",
                                    "contents": [
                                        {
                                        "type": "span",
                                        "text": "10,000",
                                        "decoration": "line-through",
                                        "color": "#19558a99"
                                        },
                                        {
                                        "type": "span",
                                        "text": " · "
                                        },
                                        {
                                        "type": "span",
                                        "text": "8 折"
                                        }
                                    ]
                                    }
                                ],
                                "alignItems": "flex-end"
                                }
                            ],
                            "margin": "4px",
                            "paddingTop": "4px",
                            "paddingBottom": "4px"
                            },
                            {
                            "type": "box",
                            "layout": "baseline",
                            "contents": [
                                {
                                "type": "text",
                                "text": "8,000",
                                "color": "#19558a",
                                "weight": "bold",
                                "align": "end",
                                "size": "xl"
                                },
                                {
                                "type": "text",
                                "text": "TWD",
                                "color": "#19558a",
                                "weight": "bold",
                                "align": "end",
                                "size": "md",
                                "flex": 0,
                                "margin": "8px"
                                }
                            ],
                            "backgroundColor": "#e3f2ff",
                            "paddingAll": "12px",
                            "cornerRadius": "12px",
                            "paddingBottom": "4px",
                            "paddingTop": "8px"
                            },
                            {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                "type": "text",
                                "text": "便宜 1,000 台幣！",
                                "color": "#19558a88",
                                "size": "sm",
                                "weight": "bold",
                                "align": "center"
                                }
                            ],
                            "paddingTop": "6px"
                            }
                        ],
                        "paddingAll": "16px",
                        "paddingTop": "8px"
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