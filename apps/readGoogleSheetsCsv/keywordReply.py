from linebot import LineBotApi
from linebot.models import *

import os
import random
from apps.common.common import *

# CSV 讀取（Google 端）
import pandas as pd

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))

# 關鍵字回話
def keywordReply(event, userMessage):

    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRZzBqVz_NABb31hG2YA3ApFYyv_Lk4Df0_yxcsFepUB6FD05W4bqQrGdfamRmudsRc_DsoeM-EB1Tk/pub?gid=374932633&single=true&output=csv"
    df = pd.read_csv(url)

    csv_content = []
    grouped = df.groupby('關鍵字')
    for input_val, group in grouped:
        output_vals = group['機器人回覆'].tolist()
        csv_content.append({
            "input": input_val.strip(),
            "output": [output.strip() for output in output_vals]
        })

    for item in csv_content:
        # 當字串中有關鍵字，其關鍵字前後有「空白」字元，會觸發回覆
        # 加上兩邊的空白是為了應對在字串開頭或結尾的情況
        userMessage = userMessage
        userMessage = userMessage.replace('?', ' ')
        userMessage = userMessage.replace('？', ' ')
        userMessage = userMessage.replace('!', ' ')
        userMessage = userMessage.replace('！', ' ')
        userMessage = userMessage.replace(',', ' ')
        userMessage = userMessage.replace('，', ' ')
        userMessage = userMessage.replace('。', ' ')

        userMessage = " " + userMessage + " "
        if (" " + item["input"] + " ") in userMessage:
            # 回覆結果隨機
            output = item["output"]
            output = random.choice(output)
            replyLineMessage = TextSendMessage(str(output))
            line_bot_api.reply_message(event.reply_token, replyLineMessage)

# 關鍵字設定
def keywordSet(event):

    # LINE 訊息包裝
    contentsList = []
    btnContentsList = [
        {
            "type": "text",
            "text": "饅頭機器人關鍵字回覆設定",
            "weight": "bold",
            "size": "lg",
            "color": "#04437c",
            "align": "center"
        }, {
            "type": "separator",
            "margin": "12px"
        }
    ]
    btnList = [
        ["關鍵字設定", "https://forms.gle/zC5jqCSgjvh1Ecj57"],
        ["關鍵字清單", "https://docs.google.com/spreadsheets/d/1DwcOn_pSixdQdEdJlSc1ZaNhF1OTptGsJepIqXTo0Xs/edit#gid=374932633"],
    ]

    for i in range(len(btnList)):
        # 按鈕文字
        text = btnList[i][0]
        url = btnList[i][1]
        # 按鈕
        btnItem = {
            "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": text,
                            "weight": "bold",
                            "color": "#04437c"
                        }
                    ],
            "paddingAll": "12px",
            "justifyContent": "center",
            "alignItems": "center",
            "action": {
                "type": "uri",
                "label": "action",
                "uri": url
                    }
        }
        btnContentsList.append(btnItem)
        # 分隔線
        if i != len(btnList) - 1:
            btnContentsList.append({"type": "separator"})

    contentsItem = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "image",
                    "url": localImg("banner/mantou.png"),
                    "size": "100%",
                    "aspectMode": "fit",
                    "margin": "0px",
                    "position": "relative",
                    "aspectRatio": "1000:279"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": btnContentsList,
                    "paddingAll": "12px"
                }
            ],
            "paddingAll": "0px"
        }
    }
    contentsList.append(contentsItem)

    # 包裝訊息
    replyLineMessage = FlexSendMessage(
        alt_text='機器人後台設定',
        contents={
            "type": "carousel",
            "contents": contentsList,
        }
    )
    # 回傳訊息
    line_bot_api.reply_message(event.reply_token, replyLineMessage)
