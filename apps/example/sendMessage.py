from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

import os
import json


line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

def textMessageExample(event):
    # 包裝訊息
    text_message = TextSendMessage(text="測試文字")
    # 發送訊息
    line_bot_api.reply_message(event.reply_token, text_message)

def imageMessageExample(event):
    # 包裝訊息
    image_message = ImageSendMessage(
        original_content_url='https://i.imgur.com/pu2S8SA.png',
        preview_image_url='https://i.imgur.com/pu2S8SA.png'
    )
    # 發送訊息
    line_bot_api.reply_message(event.reply_token, image_message)

def audioMessageExample(event):
    #聲音訊息
    audio_message = AudioSendMessage(original_content_url='https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&tl=JA&q=%E6%B8%AC%E8%A9%A6', duration=2000)
    line_bot_api.reply_message(event.reply_token, audio_message)

def flexMessageExample(event):
    # 包裝訊息
    flex_message = FlexSendMessage(
        alt_text='hello',
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
                        "url": "https://scdn.line-apps.com/n/channel_devcenter/img/flexsnapshot/clip/clip1.jpg",
                        "size": "full",
                        "aspectMode": "cover",
                        "aspectRatio": "2:3",
                        "gravity": "top"
                    },
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
                                "text": "Brown's T-shirts",
                                "size": "xl",
                                "color": "#ffffff",
                                "weight": "bold"
                            }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "baseline",
                            "contents": [
                            {
                                "type": "text",
                                "text": "¥35,800",
                                "color": "#ebebeb",
                                "size": "sm",
                                "flex": 0
                            },
                            {
                                "type": "text",
                                "text": "¥75,000",
                                "color": "#ffffffcc",
                                "decoration": "line-through",
                                "gravity": "bottom",
                                "flex": 0,
                                "size": "sm"
                            }
                            ],
                            "spacing": "lg"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                            {
                                "type": "filler"
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "contents": [
                                {
                                    "type": "filler"
                                },
                                {
                                    "type": "icon",
                                    "url": "https://scdn.line-apps.com/n/channel_devcenter/img/flexsnapshot/clip/clip14.png"
                                },
                                {
                                    "type": "text",
                                    "text": "Add to cart",
                                    "color": "#ffffff",
                                    "flex": 0,
                                    "offsetTop": "-2px"
                                },
                                {
                                    "type": "filler"
                                }
                                ],
                                "spacing": "sm"
                            },
                            {
                                "type": "filler"
                            }
                            ],
                            "borderWidth": "1px",
                            "cornerRadius": "4px",
                            "spacing": "sm",
                            "borderColor": "#ffffff",
                            "margin": "xxl",
                            "height": "40px"
                        }
                        ],
                        "position": "absolute",
                        "offsetBottom": "0px",
                        "offsetStart": "0px",
                        "offsetEnd": "0px",
                        "backgroundColor": "#03303Acc",
                        "paddingAll": "20px",
                        "paddingTop": "18px"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "text",
                            "text": "SALE",
                            "color": "#ffffff",
                            "align": "center",
                            "size": "xs",
                            "offsetTop": "3px"
                        }
                        ],
                        "position": "absolute",
                        "cornerRadius": "20px",
                        "offsetTop": "18px",
                        "backgroundColor": "#ff334b",
                        "offsetStart": "18px",
                        "height": "25px",
                        "width": "53px"
                    }
                    ],
                    "paddingAll": "0px"
                }
                },
                {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "image",
                        "url": "https://scdn.line-apps.com/n/channel_devcenter/img/flexsnapshot/clip/clip2.jpg",
                        "size": "full",
                        "aspectMode": "cover",
                        "aspectRatio": "2:3",
                        "gravity": "top"
                    },
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
                                "text": "Cony's T-shirts",
                                "size": "xl",
                                "color": "#ffffff",
                                "weight": "bold"
                            }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "baseline",
                            "contents": [
                            {
                                "type": "text",
                                "text": "¥35,800",
                                "color": "#ebebeb",
                                "size": "sm",
                                "flex": 0
                            },
                            {
                                "type": "text",
                                "text": "¥75,000",
                                "color": "#ffffffcc",
                                "decoration": "line-through",
                                "gravity": "bottom",
                                "flex": 0,
                                "size": "sm"
                            }
                            ],
                            "spacing": "lg"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                            {
                                "type": "filler"
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "contents": [
                                {
                                    "type": "filler"
                                },
                                {
                                    "type": "icon",
                                    "url": "https://scdn.line-apps.com/n/channel_devcenter/img/flexsnapshot/clip/clip14.png"
                                },
                                {
                                    "type": "text",
                                    "text": "Add to cart",
                                    "color": "#ffffff",
                                    "flex": 0,
                                    "offsetTop": "-2px"
                                },
                                {
                                    "type": "filler"
                                }
                                ],
                                "spacing": "sm"
                            },
                            {
                                "type": "filler"
                            }
                            ],
                            "borderWidth": "1px",
                            "cornerRadius": "4px",
                            "spacing": "sm",
                            "borderColor": "#ffffff",
                            "margin": "xxl",
                            "height": "40px"
                        }
                        ],
                        "position": "absolute",
                        "offsetBottom": "0px",
                        "offsetStart": "0px",
                        "offsetEnd": "0px",
                        "backgroundColor": "#9C8E7Ecc",
                        "paddingAll": "20px",
                        "paddingTop": "18px"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "text",
                            "text": "SALE",
                            "color": "#ffffff",
                            "align": "center",
                            "size": "xs",
                            "offsetTop": "3px"
                        }
                        ],
                        "position": "absolute",
                        "cornerRadius": "20px",
                        "offsetTop": "18px",
                        "backgroundColor": "#ff334b",
                        "offsetStart": "18px",
                        "height": "25px",
                        "width": "53px"
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



def quickReplyExample(event):
    # 包裝訊息
    text_message = TextSendMessage(
        text="快速回覆範例訊息",
        quick_reply=QuickReply(
            items=[
                    QuickReplyButton(
                        action=MessageAction(label='訊息', text='訊息內容'),
                        # image_url='https://storage.googleapis.com/你的icon連結.png'
                    ),
                    QuickReplyButton(
                        action=CameraAction(label='拍照'),
                        # image_url='https://storage.googleapis.com/你的icon連結.png'
                    ),
                    QuickReplyButton(
                        action=CameraRollAction(label='相冊'),
                        # image_url='https://storage.googleapis.com/你的icon連結.png'
                    ),
                    QuickReplyButton(
                        action=LocationAction(label='位置'),
                        # image_url='https://storage.googleapis.com/你的icon連結.png'
                    ),
                    QuickReplyButton(
                        action=PostbackAction(label='Postback', data='action=buy&itemid=123'),
                        # image_url='https://storage.googleapis.com/你的icon連結.png'
                    ),
                    QuickReplyButton(
                        action=DatetimePickerAction(label='選擇時間', data='datetime', mode='datetime'),
                        # image_url='https://storage.googleapis.com/你的icon連結.png'
                    )

            ]
        )
    )
    # 發送訊息
    line_bot_api.reply_message(event.reply_token, text_message)



# 愚人節假轉帳回覆
def foolDayMessage(event, num):
    # 包裝訊息
    flex_message = FlexSendMessage(
        alt_text=f'已將 NT$ {num} 轉帳給您',
        contents={
            "type": "bubble",
            "size": "hecto",
            "hero": {
                "type": "image",
                "url": "https://i.imgur.com/6Q0B4sS.png",
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover",
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "text",
                    "text": "LINE Pay",
                    "size": "lg"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "md",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "text",
                        "text": f'已將 NT$ {num} 轉帳給您',
                        "wrap": True,
                        "color": "#666666",
                        "size": "sm",
                        "flex": 5
                    }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "text",
                        "text": "瞭解更多",
                        "size": "md",
                        "weight": "bold"
                    }
                    ],
                    "paddingAll": "10px",
                    "cornerRadius": "8px",
                    "backgroundColor": "#00000022",
                    "justifyContent": "center",
                    "alignItems": "center",
                    "margin": "lg",
                    "action": {
                    "type": "uri",
                    "label": "action",
                    "uri": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
                    }
                }
                ]
            }
            }
        )
    # 發送訊息
    line_bot_api.reply_message(event.reply_token, flex_message)


