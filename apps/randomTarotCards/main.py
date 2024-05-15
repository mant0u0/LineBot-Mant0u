# 塔羅牌

from linebot import LineBotApi
from linebot.models import *

import os
import json
import random
from apps.common.common import *

from apps.ai.gemini import gemini

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))


def randomTarotCardsMain(event, userMessage):

    # 整理文字
    if userMessage == "塔羅牌":
        userMessage = "塔羅牌：我的運勢"
    
    if userMessage.find('塔羅牌：') == 0:
        userMessage = userMessage.replace('塔羅牌：', '')

        # 讀取內容 (JSON 檔案)
        filePath = 'apps/randomTarotCards/tarot_cards.json'
        with open(filePath, 'r') as file:
            data = json.load(file) # 讀取檔案
        
        # 抽一張牌
        tarotCard_result = random.choice(data)
        
        # 卡片名稱
        card_name = tarotCard_result["name"]
        card_name_img = tarotCard_result["img"]
        
        card_direction = random.randint(0, 1)
        if card_direction == 0:
            # 正位
            card_illustrate = tarotCard_result["upright"]
            card_direction = "正位"
            card_direction_en = "upright"
        else:
            # 逆位
            card_illustrate = tarotCard_result["inverse"]
            card_direction = "逆位"
            card_direction_en = "inverse"

        input_ai_text = f"請根據塔羅牌{card_name}{card_direction}，依據「{card_illustrate}」牌意解釋有關「{userMessage}」的分析，限用20~50字元來解釋。"
        result_text = f"{card_name} - {card_direction}"
        result_text_fortune = gemini(input_ai_text)

        # 取得塔羅牌圖片
        result_img_url = localImg(f"randomTarotCards/{card_direction_en}/{card_name_img}.png")

        # flexMessage 容器
        flex_message_contents = []

        # 抽籤結果：將 pageTemplate 放入 flex_message_contents 中
        pageTemplate = pageTemplate_result(result_img_url, result_text)
        flex_message_contents.append( pageTemplate )

        # 運勢分析結果：將 pageTemplate 放入 flex_message_contents 中
        pageTemplate = pageTemplate_fortune( result_text, result_text_fortune )
        flex_message_contents.append( pageTemplate )

        # 包裝訊息
        flex_message = FlexSendMessage(
            alt_text= '塔羅牌占卜！',
            contents={
                "type": "carousel",
                "contents": flex_message_contents
                }
            )
        
        # 發送訊息
        line_bot_api.reply_message(event.reply_token, flex_message)
        return

# 抽籤結果 pageTemplate
def pageTemplate_result(result_img_url, result_text):
    pageTemplate = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                # 背景
                {
                    "type": "image",
                    "url": localImg("randomTarotCards/BG.png"),
                    "size": "full",
                    "aspectMode": "cover",
                    "aspectRatio": "1:1",
                    "gravity": "center"
                },

                # 陰影
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "image",
                        "url": localImg("randomTarotCards/shadow.png"),
                        "size": "3xl"
                    }
                    ],
                    "position": "absolute",
                    "width": "100%",
                    "height": "75%",
                    "justifyContent": "center",
                    "alignItems": "center"
                },

                # 卡片
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "image",
                        "url": result_img_url,
                        "size": "3xl"
                    }
                    ],
                    "position": "absolute",
                    "width": "100%",
                    "height": "75%",
                    "justifyContent": "center",
                    "alignItems": "center"
                },

                # 文字
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
                                            "text": result_text,
                                            "size": "lg",
                                            "color": "#222d53",
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
            # "action": {
            #     "type": "message",
            #     "label": "action",
            #     "text": "塔羅牌"
            # },
        }
    }

    return pageTemplate

# 運勢分析結果 pageTemplate
def pageTemplate_fortune( result_text, result_text_fortune ):
    pageTemplate = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                # 背景
                {
                    "type": "image",
                    "url": localImg("randomTarotCards/BG_text.png"),
                    "size": "full",
                    "aspectMode": "cover",
                    "aspectRatio": "1:1"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": f"✦ {result_text} ✦",
                            "color": "#222d53",
                            "wrap": True,
                            "size": "md",
                            "weight": "bold",
                            "lineSpacing": "4px",
                            "align": "center"
                        },
                        {
                            "type": "text",
                            "text": result_text_fortune,
                            "color": "#222d53",
                            "wrap": True,
                            "size": "md",
                            "weight": "bold",
                            "lineSpacing": "4px",
                            "margin": "lg",
                        }
                    ],
                    "position": "absolute",
                    "width": "100%",
                    "height": "100%",
                    "justifyContent": "center",
                    "alignItems": "center",
                    "paddingAll": "12%"
                }
            ],
            "paddingAll": "0px"
        }
    }

    return pageTemplate