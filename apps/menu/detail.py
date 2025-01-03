from linebot import LineBotApi
from linebot.models import *

import os
import re
import json
from apps.common.common import *

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))

# 主要
def menuDetail(event, fileName):

    print(fileName)

    # 讀取內容 (JSON 檔案)
    filePath = 'apps/menu/textJson/detail/'+ fileName +'.json'
    with open(filePath, 'r') as file:
        detailContent = json.load(file)

    text_color = detailContent["text_color"]
    banner_url = detailContent["banner_url"]
    banner_url = localImg(banner_url)

    # flexMessage 容器：放入每一頁的文字
    flex_message_contents = []
    for text_content in detailContent["text_content"]:
        
        # flexMessage 一頁的內容
        pageTemplate = menuPageTemplate(text_color, banner_url, text_content)
        
        # 將 pageTemplate 放入 flex_message_contents 中
        flex_message_contents.append(pageTemplate)

    # 快速回覆
    flex_message_quick_reply = []
    for quick_reply in detailContent["quick_reply"]:
        items = QuickReplyButton(action=MessageAction(label=quick_reply[0], text=quick_reply[1]))
        flex_message_quick_reply.append(items)
    # 快速回覆：「更多指令」按鈕
    flex_message_quick_reply.append( 
        QuickReplyButton(action=MessageAction(label="更多指令 ➜", text="指令說明"))
    )

    
    # 打包
    flex_message_carousel = {
        "type": "carousel",
        "contents": flex_message_contents,
    }

    # 包裝訊息
    flex_message = FlexSendMessage(
        alt_text='指令說明',
        contents= flex_message_carousel,
        quick_reply=QuickReply(
            items=flex_message_quick_reply
        ),
    )
    # 發送訊息
    line_bot_api.reply_message(event.reply_token, flex_message)



# 頁面模板
def menuPageTemplate(text_color, banner_url, text_content):
    # 頁面內容（標題 + 文字）
    pageTemplate_Contents = []
    for item in text_content:
        if item["type"] == "h1":
            pageTemplate_Contents.append(h1_Item(text_color, item["text"]))
        if item["type"] == "h2":
            pageTemplate_Contents.append(h2_Item(text_color, item["text"]))
        if item["type"] == "p":
            pageTemplate_Contents.append(p_Item(text_color, item["text"]))


    # 頁面 (pageTemplate)
    pageTemplate = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "image",
                    "url": banner_url,
                    "aspectMode": "cover",
                    "aspectRatio": "1000:280",
                    "size": "100%"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": pageTemplate_Contents,
                    "paddingAll": "20px",
                    "paddingTop": "16px"
                }
            ],
            "width": "100%",
            "paddingAll": "0px"
        }
    }

    return pageTemplate


# 文字整理
def h1_Item(color, text):
    item = {
        "text": text,
        "type": "text",
        "size": "xl",
        "color": color,
        "weight": "bold"
    }
    return item
def h2_Item(color, text):
    item = {
        "text": text,
        "type": "text",
        "size": "md",
        "color": color,
        "weight": "bold",
        "margin": "8px"
    }
    return item
def p_Item(color, text):
    segments = re.split(r'({{.*?}})', text)
    contents = []

    for segment in segments:
        if segment.startswith('{{') and segment.endswith('}}'):
            contents.append({
                "type": "span",
                "text": segment[2:-2],
                "color": "#eb4846",
                "decoration": "underline"
            })
        else:
            segment = segment.strip()
            if segment:  # 去除空字符串
                contents.append({
                    "type": "span",
                    "text": segment
                })
    item = {
        "type": "text",
        "contents": contents,
        "margin": "8px",
        "size": "sm",
        "wrap": True,
        "weight": "bold",
        "lineSpacing": "4px",
        "color": color+"99",
    }
    return item







