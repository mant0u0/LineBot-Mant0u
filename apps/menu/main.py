# 指令說明選單（主程式）

from linebot import LineBotApi
from linebot.models import *

import json
import os
import random
import datetime
from apps.common.common import *
from apps.common.recordMessage import recordTextMessage, readTextMessage


line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))

# 主要
def mant0u_bot_main(event):
    
    # 取得日期
    today = datetime.datetime.now().strftime("%Y 年 %m 月 %d 日")

    # 取得時間
    now = datetime.datetime.now().strftime("%H:%M")


    random_message = [
        '你好喔！我是饅頭，請問有什麼需要幫忙嗎？',
        '安安，我是饅頭，請問有什麼需要幫忙嗎？',
        '我是饅頭，請問有什麼需要幫忙嗎？',
        '我是饅頭，很高興為你服務，請問有什麼需要幫忙嗎？',
        '你好喔！我是饅頭聊天機器人，有什麼事需要幫忙嗎？',
        '安安，我是饅頭聊天機器人，有什麼事需要幫忙嗎？',
        '今天是 ' + today + '，有什麼事需要幫忙嗎？',
        '現在是 ' + now + '，有什麼事需要幫忙嗎？',
    ]
    
    # 預設功能：指令說明
    quick_reply_list = []
    quick_reply_item = QuickReplyButton( action=MessageAction(label = "● 指令說明", text = "指令說明") )
    quick_reply_list.append( quick_reply_item )

    # 搜尋：讀取前一筆訊息
    try:
        quick_reply_item = QuickReplyButton(
            action=MessageAction(label = "○ 搜尋：" + readTextMessage(event)["message"], text = "搜尋：" + readTextMessage(event)["message"])
        )
        quick_reply_list.append( quick_reply_item )
    except:
        pass

    text_message = TextSendMessage(
        text= random.choice(random_message),
        quick_reply=QuickReply(
            items=quick_reply_list
        )
    )
    line_bot_api.reply_message(event.reply_token, text_message)


def mant0u_bot_instructions(event):
    # 讀取內容 (JSON 檔案)
    filePath = 'apps/menu/textJson/menuContent.json'
    with open(filePath, 'r') as file:
        menu_content = json.load(file)


    # flexMessage 容器
    flex_message_contents = []

    # 將每一頁的內容代入模板 menuPageTemplate(pege) 並放入 flex_message_contents 中
    for pege in menu_content:
        flex_message_contents.append( menuPageTemplate(pege) )

    # 包裝訊息
    flex_message = FlexSendMessage(
        alt_text= '指令說明選單',
        contents={
            "type": "carousel",
            "contents": flex_message_contents
            }
        )
    
    # 發送訊息
    line_bot_api.reply_message(event.reply_token, flex_message)


# 頁面模板
def menuPageTemplate( pege ):

    # 頁面內容（標題 + 按鈕選項）
    pageTemplate_Contents = []

    # 標題 (pageTemplate_Title)
    pageTemplate_Title = [
        {
            "type": "text",
            "text": pege["title"],
            "weight": "bold",
            "size": "lg",
            "color": "#10496d",
            "align": "center"
        }, {
            "type": "text",
            "text": pege["illustrate"],
            "weight": "bold",
            "size": "sm",
            "color": "#10496d99",
            "align": "center",
            "margin": "4px"
        }, {
            "type": "separator",
            "margin": "12px"
        },
    ]
    for i in pageTemplate_Title:
        pageTemplate_Contents.append( i )

    # 按鈕選項 (pageTemplate_Btn)
    for btn in pege["options"]:
        pageTemplate_Btn = [
            # 選項
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": btn["labelText"],
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
                    "text": "？" + btn["actionText"],
                }
            },
            # 分隔線
            {"type": "separator"},
        ]

        for i in pageTemplate_Btn:
            pageTemplate_Contents.append( i )

    # 清除最後一項（分隔線）
    del pageTemplate_Contents[-1]

    # 頁面 (pageTemplate)
    pageTemplate = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
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
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": pageTemplate_Contents,
                    "paddingAll": "12px"
                }
            ],
            "paddingAll": "0px"
        }
    }

    return pageTemplate
        