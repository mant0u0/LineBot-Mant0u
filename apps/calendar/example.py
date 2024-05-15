from linebot import LineBotApi
from linebot.models import *

import os
from apps.common.common import *

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))

# 日曆範例
def calendarExample(event):
    # 包裝訊息
    flex_message = FlexSendMessage(
        alt_text='日曆',
        contents={
            "type": "carousel",
            "contents": [
                {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    # 背景圖片
                    {
                        "type": "image",
                        "url": localImg("calendar/background.png"),
                        "aspectRatio": "1:1",
                        "size": "full"
                    },
                    # 底部結果文字的背景
                    {
                        "type": "image",
                        "url": localImg("calendar/bottom.png"),
                        "position": "absolute",
                        "size": "full",
                        "aspectRatio": "1:1"
                    },
                    # 結果文字
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "text",
                            "text": "還剩下 5 天",
                            "size": "lg",
                            "color": "#ffffff",
                            "weight": "bold"
                        }
                        ],
                        "borderWidth": "1px",
                        "position": "absolute",
                        "offsetBottom": "0px",
                        "paddingAll": "20px",
                        "width": "100%",
                        "height": "24%",
                        "justifyContent": "center",
                        "alignItems": "center"
                    },
                    # 日期與星期
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "image",
                                "url": localImg("calendar/day/20.png"),
                                "aspectRatio": "350:300"
                            },
                            {
                                "type": "image",
                                "url": localImg("calendar/week/Sunday.png"),
                                "aspectRatio": "280:90"
                            }
                        ],
                        "position": "absolute",
                        "paddingAll": "20px",
                        "width": "100%",
                        "height": "75%",
                        "justifyContent": "center",
                        "alignItems": "center",
                        "offsetTop": "0px"
                    },
                    # 西元 + 月份
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "image",
                            "url": localImg("calendar/year/ad.png"),
                            "aspectRatio": "150:80",
                            "size": "32px"
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                            {
                                "type": "image",
                                "url": localImg("calendar/year/2.png"),
                                "aspectRatio": "68:76",
                                "size": "14px",
                                "flex": 0
                            },
                            {
                                "type": "image",
                                "url": localImg("calendar/year/2.png"),
                                "aspectRatio": "68:76",
                                "size": "14px",
                                "flex": 0
                            },
                            {
                                "type": "image",
                                "url": localImg("calendar/year/2.png"),
                                "aspectRatio": "68:76",
                                "size": "14px",
                                "flex": 0
                            },
                            {
                                "type": "image",
                                "url": localImg("calendar/year/2.png"),
                                "aspectRatio": "68:76",
                                "size": "14px",
                                "flex": 0
                            }
                            ],
                            "margin": "4px",
                            "height": "20px",
                            "width": "40%",
                            "justifyContent": "flex-end"
                        },
                        {
                            "type": "image",
                            "url": localImg("calendar/month/12.png"),
                            "size": "24px",
                            "aspectRatio": "65:130",
                            "margin": "2px"
                        }
                        ],
                        "position": "absolute",
                        "paddingAll": "16px",
                        "width": "100%",
                        "height": "75%",
                        "justifyContent": "flex-start",
                        "alignItems": "flex-end",
                        "offsetTop": "0px"
                    },
                    # 農曆 + 月份
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "image",
                            "url": localImg("calendar/year/tw.png"),
                            "aspectRatio": "150:80",
                            "size": "32px"
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                            {
                                "type": "image",
                                "url": localImg("calendar/year/2.png"),
                                "aspectRatio": "68:76",
                                "size": "14px",
                                "flex": 0
                            },
                            {
                                "type": "image",
                                "url": localImg("calendar/year/2.png"),
                                "aspectRatio": "68:76",
                                "size": "14px",
                                "flex": 0
                            },
                            {
                                "type": "image",
                                "url": localImg("calendar/year/2.png"),
                                "aspectRatio": "68:76",
                                "size": "14px",
                                "flex": 0
                            },
                            {
                                "type": "image",
                                "url": localImg("calendar/year/2.png"),
                                "aspectRatio": "68:76",
                                "size": "14px",
                                "flex": 0
                            }
                            ],
                            "margin": "4px",
                            "height": "20px",
                            "width": "40%",
                            "justifyContent": "flex-start"
                        },
                        {
                            "type": "image",
                            "url": localImg("calendar/zodiac/5.png"),
                            "size": "24px",
                            "margin": "2px",
                            "aspectRatio": "1:1"
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                            {
                                "type": "image",
                                "url": localImg("calendar/lunar_year/1/2.png"),
                                "aspectRatio": "68:76",
                                "size": "14px",
                                "flex": 0
                            },
                            {
                                "type": "image",
                                "url": localImg("calendar/lunar_year/2/1.png"),
                                "aspectRatio": "68:76",
                                "size": "14px",
                                "flex": 0
                            }
                            ],
                            "height": "20px",
                            "width": "20%",
                            "justifyContent": "flex-start",
                            "margin": "2px",
                            "offsetEnd": "2px"
                        },
                        {
                            "type": "image",
                            "size": "24px",
                            "aspectRatio": "65:130",
                            "url": localImg("calendar/lunar_month/3.png"),
                        },
                        {
                            "type": "image",
                            "url": localImg("calendar/lunar_day/12.png"),
                            "size": "24px",
                            "aspectRatio": "65:130"
                        }
                        ],
                        "position": "absolute",
                        "paddingAll": "16px",
                        "width": "100%",
                        "height": "75%",
                        "justifyContent": "flex-start",
                        "alignItems": "flex-start",
                        "offsetTop": "0px"
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

