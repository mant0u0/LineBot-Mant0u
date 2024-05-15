# 日本神社抽籤
from linebot import LineBotApi
from linebot.models import *

import os
import random

from apps.ai.gemini import gemini, geminiPrompt
# from apps.ai.openai import openai
from apps.common.common import *

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))

def randomOkamikujiMain(event, userMessage):

    # 取得抽籤結果
    result, result_text, result_num, result_color = getOkamikujiResult()
    
    # 取得抽籤圖片
    result_img_url = localImg(f"randomOkamikuji/item-{str(result_num)}.jpg")
    result_bg_img_url = localImg(f"randomOkamikuji/bg-{str(result_num)}.jpg")

    # flexMessage 容器
    flex_message_contents = []
    # 快速回覆清單
    quick_reply_list = [
        QuickReplyButton(
            action=MessageAction(label='再抽一次', text='抽籤'),
        )
    ]


    # 一般模式：只顯示抽籤結果
    if userMessage == "抽籤":

        # 抽籤結果：將 pageTemplate 放入 flex_message_contents 中
        pageTemplate = pageTemplate_result(result_img_url, result_text, result_color)
        flex_message_contents.append( pageTemplate )
    
    #  AI 模式：顯示抽籤結果、運勢分析
    if userMessage.find('抽籤：') == 0:


        quick_reply_item = QuickReplyButton(
            action=MessageAction(label='再問一次', text=userMessage),
        )
        quick_reply_list.append( quick_reply_item )

        # 整理文字、取得運勢分析
        userMessage = userMessage.replace('抽籤：', '')
        result_fortune = getOkamikujiFortune(result, userMessage)

        # 抽籤結果：將 pageTemplate 放入 flex_message_contents 中
        pageTemplate = pageTemplate_result(result_img_url, result_text, result_color)
        flex_message_contents.append( pageTemplate )

        # 運勢分析結果：將 pageTemplate 放入 flex_message_contents 中
        pageTemplate = pageTemplate_fortune(userMessage, result, result_bg_img_url, result_fortune, result_color )
        flex_message_contents.append( pageTemplate )



    # 當 flex_message_contents 有內容，回傳訊息
    if flex_message_contents != []:
        # 包裝訊息
        flex_message = FlexSendMessage(
            alt_text= '有人抽籤囉！',
            contents={
                "type": "carousel",
                "contents": flex_message_contents
                },
            quick_reply=QuickReply(
                items=quick_reply_list
            )
        )
        
        # 發送訊息
        line_bot_api.reply_message(event.reply_token, flex_message)
        return


# 抽籤結果
def getOkamikujiResult():
    # 取得隨機點數
    result_num = random.randint(1, 7)
    
    # 顯示文字
    if result_num == 1:
        result_text = "抽籤結果：大吉！？"
        result = "大吉"
        result_color = "#10496d"
    elif result_num == 2:
        result_text = "抽籤結果：中吉！！"
        result = "中吉"
        result_color = "#10496d"
    elif result_num == 3:
        result_text = "抽籤結果：小吉！"
        result = "小吉"
        result_color = "#10496d"
    elif result_num == 4:
        result_text = "抽籤結果：吉。"
        result = "吉"
        result_color = "#10496d"
    elif result_num == 5:
        result_text = "抽籤結果：末吉。"
        result = "末吉"
        result_color = "#10496d"
    elif result_num == 6:
        result_text = "抽籤結果：凶！"
        result = "凶"
        result_color = "#353535"
    elif result_num == 7:
        result_text = "抽籤結果：大凶！？"
        result = "大凶"
        result_color = "#353535"

    return result, result_text, result_num, result_color

# 抽籤運勢分析
def getOkamikujiFortune(result, userMessage):

    # gemini
    # askText = f"請模擬日本神社抽籤，根據「{result}」的結果，產生關於「{userMessage}」運勢分析。（限用 20~50 個字）"
    # result_fortune = gemini(askText)

    inputText = f"{result}：{userMessage}"
    prompt = [
        {
            "Q":"大吉：我的戀愛運勢",
            "A":"你的戀愛運勢極佳，各方面均將獲得成功和幸福，可能遇到命中注定的愛情，感情更會更穩固，享受這段美好時光！",
        },
        {
            "Q":"凶：投資股市",
            "A":"投資股市方面可能會遇到挑戰和波動，建議謹慎行事，避免冒險，保持穩健的態度，做好風險控制和資金管理。",
        },
        {
            "Q":"大凶：明天的考試",
            "A":"明天的考試可能會遇到困難和挑戰，建議你積極準備，保持冷靜，專注於考試內容，盡力而為。",
        },
        {
            "Q":"末吉：下周的比賽",
            "A":"下周的比賽可能會有些許波折，但也會有一些幸運之處。請確保充分準備，保持冷靜和專注，並尋求幫助或建議以克服任何挑戰。",
        },  
        {
            "Q":"吉：大樂透",
            "A":"吉兆預示著一些幸運和機會，儘管中獎並非必然，但你可能會遇到一些好運氣。但仍然要理智地玩，不要投入過多金錢。",
        },  
        {
            "Q":"小吉：工作",
            "A":"工作上可能會遇到一些小挑戰，但也會有一些機會和好運。保持積極的態度，努力克服困難，並善用任何出現的機會。",
        },  
        {
            "Q":"大吉：台積電",
            "A":"非常好的兆頭，未來台積電將會取得成功，股票價值可能會上升。如果你是投資者，這是一個好的時機持有或增加投資。",
        },  
        {
            "Q":"凶：房地產",
            "A":"房地產方面可能會面臨挑戰和困難。可能出現市場波動或其他不利因素，導致投資或交易受阻。",
        },

    ]
    result_fortune = geminiPrompt(inputText, prompt)

    return result_fortune

# 抽籤結果 pageTemplate
def pageTemplate_result(result_img_url, result_text, result_color):
    pageTemplate = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "image",
                    "url": result_img_url,
                    "size": "full",
                    "aspectMode": "cover",
                    "aspectRatio": "1:1",
                    "gravity": "center"
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
                                            "text": result_text,
                                            "size": "lg",
                                            "color": result_color,
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
                "text": "抽籤"
            },
        }
    }

    return pageTemplate

# 運勢分析結果 pageTemplate
def pageTemplate_fortune(userMessage, result, result_bg_img_url, result_fortune, result_color ):
    pageTemplate = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "image",
                    "url": result_bg_img_url,
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
                            "text": f"【{userMessage}：{result}】",
                            "color": result_color,
                            "wrap": True,
                            "size": "md",
                            "weight": "bold",
                            "lineSpacing": "4px",
                            "align": "center"
                        },
                        {
                            "type": "text",
                            "text": result_fortune,
                            "color": result_color,
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