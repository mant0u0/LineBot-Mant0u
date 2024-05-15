# 亂數產生

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

import os
import random
import re
from apps.common.common import *

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))



def randomNumberMain(event, userMessage):

    if userMessage == "亂數":
        userMessage = "亂數：0 ~ 100"

    if userMessage.find('亂數：') == 0:

        # 整理字串：去除前面關鍵字，只保留數字
        userMessage = userMessage.replace('亂數：', '')

        # 取得亂數區間 random_range 陣列
        random_range = re.findall(r'\b\d+\b', userMessage)
        random_range = getRandomRange(random_range)

        # 取得亂數 random_number
        random_number = getRandomNumber(random_range)

        # 數字位數分割（ 例如："123" -> ["1","2","3"] ）
        message_content_num = []
        for number in str(random_number):
            item = {
                "type": "image",
                "url": localImg("randomNumber/"+str(number)+".png"),
            }
            message_content_num.append(item)

        # 隨機顏色
        random_bg = random.randint(1, 7)
        random_color_list = ["", "#8c2937", "#934b27", "#91592a", "#2d6c3d", "#2e635e", "#294363", "#3c3b7c"]
        random_color = random_color_list[random_bg]

        # 訊息排版微調
        if len(str(random_number)) < 3:
            padding = "60px"
            offsetTop = "10%"
        if len(str(random_number)) == 3:
            padding = "40px"
            offsetTop = "15%"
        if len(str(random_number)) >= 4:
            padding = "20px"
            offsetTop = "20%"

        # 數字區間方塊寬度修正
        numBoxTextLen = len(str(random_range[0]) + str(random_range[1]))
        numBoxMaxWidth = numBoxTextLen * 3 + 18
        if numBoxTextLen > 10:
            numBoxMaxWidth = numBoxTextLen * 3.2 + 18

        # flexMessage 容器
        flex_message_contents = []

        # flexMessage 一頁的內容
        pageTemplate = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "image",
                        "url": localImg("randomNumber/BG"+str(random_bg)+".png"),
                        "size": "full",
                        "aspectMode": "cover",
                        "aspectRatio": "1:1",
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
                                        "type": "box",
                                        "layout": "baseline",
                                        "contents": [
                                            {
                                                "type": "text",
                                                "text": str(random_range[0]),
                                                "align": "center",
                                                "weight": "bold",
                                                "color": random_color,
                                                "flex": 0,
                                                "size": "md"
                                            },
                                            {
                                                "type": "icon",
                                                "url": localImg("randomNumber/ARROW"+str(random_bg)+".png"),
                                                "margin": "4px",
                                                "size": "xxs"
                                            },
                                            {
                                                "type": "text",
                                                "text": str(random_range[1]),
                                                "align": "center",
                                                "weight": "bold",
                                                "color": random_color,
                                                "flex": 0,
                                                "size": "md",
                                                "margin": "4px"
                                            }
                                        ],
                                        "backgroundColor": "#ffffff",
                                        "cornerRadius": "100px",
                                        "paddingAll": "4px",
                                        "paddingStart": "16px",
                                        "paddingEnd": "16px",
                                        "maxWidth": str(numBoxMaxWidth) + "%",
                                        "justifyContent": "center"
                                    },
                                    {
                                        "type": "box",
                                        "layout": "horizontal",
                                        "contents": message_content_num,
                                        "width": "100%",
                                        "paddingStart": padding,
                                        "paddingEnd": padding,
                                        "paddingTop": "20px"
                                    }
                                ],
                                "alignItems": "center",
                                "position": "absolute",
                                "width": "100%",
                                "offsetTop": offsetTop
                            }
                        ],
                        "position": "absolute",
                        "width": "100%",
                        "height": "100%",
                        "justifyContent": "center",
                        "alignItems": "center"
                    },
                    {
                        "type": "image",
                        "url": localImg("randomNumber/BASE"+str(random_bg)+".png"),
                        "size": "full",
                        "aspectMode": "cover",
                        "aspectRatio": "1:1",
                        "position": "absolute",
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
                                        "layout": "horizontal",
                                        "contents": [
                                            {
                                                "type": "text",
                                                "text": str(random_number)+" !",
                                                "size": "lg",
                                                "color": random_color,
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
                    "text": "亂數："+str(random_range[0]) + " ~ " + str(random_range[1])
                },
            }
        }
        
        # 將內容放入 flex_message_contents 中
        flex_message_contents.append(pageTemplate)

        # 包裝訊息
        flex_message = FlexSendMessage(
            alt_text= '新的亂數產生了！',
            contents={
                "type": "carousel",
                "contents": flex_message_contents
                }
            )
        
        # 發送訊息
        line_bot_api.reply_message(event.reply_token, flex_message)
        return


# 取得亂數區間
def getRandomRange(list):
    # 判斷亂數區間上下限
    # 只設定上限，例如："98" -> ["0","98"]
    if len(list) == 1:
        list = [0, int(list[0])]
        return list

    # 設定上限與下限，例如："30～50" -> ["30","50"]
    elif len(list) == 2:
        if int(list[0]) < int(list[1]):
            list = [int(list[0]), int(list[1])]
        if int(list[0]) > int(list[1]):
            list = [int(list[1]), int(list[0])]
        if int(list[0]) == int(list[1]):
            list = [int(list[0]), int(list[1])]
        return list


# 取得亂數
def getRandomNumber(list):
    random_number = random.randint(list[0], list[1])
    return random_number

