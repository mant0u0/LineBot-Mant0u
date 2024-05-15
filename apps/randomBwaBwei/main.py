# 擲筊
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

import os
import random

from apps.common.common import *
from apps.ai.gemini import gemini
# from apps.ai.openai import openai

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))


def randomBwaBweiMain(event, userMessage):

    # 讀取
    source_id = getMessageSourceID(event)   # 取得訊息來源 ID
    file_path = 'randomBwaBwei'   # 選擇存取的檔案路徑
    loaded_data = read_json(file_path, source_id)  # 讀取檔案
    try:
        loaded_data["combo"] = loaded_data["combo"] + 1
    except:
        loaded_data = {"combo": 0}

    # 取得擲筊結果
    result_data = getBwaBweiResult(loaded_data["combo"])
    
    # 紀錄結果
    if result_data["state"] == "聖筊":
        write_json(file_path, source_id, loaded_data)    # 寫入 JSON 檔案
    else:
        loaded_data = {"combo": 0}
        write_json(file_path, source_id, loaded_data)    # 寫入 JSON 檔案


    # 取得擲筊圖片
    result_img_url      = localImg(f"randomBwaBwei/{result_data['num']}-{str(random.randint(1, 2))}.png")
    result_bg_img_url   = localImg(f"randomBwaBwei/BG.jpg")
    result_icon_img_url = localImg(f"randomBwaBwei/icon-{result_data['icon']}.png")


    # flexMessage 容器
    flex_message_contents = []

    # 一般模式：只顯示擲筊結果
    if userMessage == "擲筊":
        bwaBwei_model = "default"

        # 擲筊結果：將 pageTemplate 放入 flex_message_contents 中
        pageTemplate = pageTemplate_result(result_img_url, result_data)
        flex_message_contents.append( pageTemplate )


    
    #  AI 模式：顯示擲筊結果、運勢分析
    if userMessage.find('擲筊：') == 0:
        bwaBwei_model = "ai"

        # 紀錄動作指令
        bwaBwei_action_text = userMessage

        # 整理文字、取得運勢分析
        userMessage = userMessage.replace('擲筊：', '')
        result_fortune = getOkamikujiFortune(result_data["illustrate"], userMessage)

        # 擲筊結果：將 pageTemplate 放入 flex_message_contents 中
        pageTemplate = pageTemplate_result(result_img_url, result_data)
        flex_message_contents.append( pageTemplate )

        # 運勢分析結果：將 pageTemplate 放入 flex_message_contents 中
        pageTemplate = pageTemplate_fortune( result_bg_img_url, result_icon_img_url, result_fortune )
        flex_message_contents.append( pageTemplate )

    # 當 flex_message_contents 有內容，回傳訊息
    if flex_message_contents != []:
        if bwaBwei_model == "default":
            # 包裝訊息
            flex_message = FlexSendMessage(
                alt_text= '有人擲筊囉！',
                contents={
                    "type": "carousel",
                    "contents": flex_message_contents
                    },
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=MessageAction(label = "再擲一次", text = "擲筊")
                        ),
                    ]
                )
            )
            
        elif bwaBwei_model == "ai":
            # 包裝訊息
            flex_message = FlexSendMessage(
                alt_text= '有人擲筊囉！',
                contents={
                    "type": "carousel",
                    "contents": flex_message_contents
                    },
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=MessageAction(label = "再擲一次", text = "擲筊")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label = "再問一次", text = bwaBwei_action_text)
                        )
                    ]
                )
            )


        # 發送訊息
        line_bot_api.reply_message(event.reply_token, flex_message)
        return


# 擲筊結果
def getBwaBweiResult(combo):
    # 取得隨機點數
    result_list = ["聖筊", "聖筊", "聖筊", "無筊", "笑筊"]
    result = random.choice(result_list)

    if result == "聖筊":
        if combo <= 1:
            result_data = {
                "state": "聖筊",
                "num": "01",
                "text": "聖筊！",
                "illustrate": "允許、同意或順利",
                "icon": "O"
            }
        elif combo == 2:
            result_data = {
                "state": "聖筊",
                "num": "01",
                "text": f"連續第 {str(combo)} 次聖筊！",
                "illustrate": "允許、同意或順利",
                "icon": "O"
            }
        elif combo >=3 :
            result_data = {
                "state": "聖筊",
                "num": "01",
                "text": f"連續第 {str(combo)} 次聖筊！",
                "illustrate": "非常允許、同意或表示非常順利",
                "icon": "O"
            }

    if result == "無筊":
        result_data = {
            "state": "無筊",
            "num": "11",
            "text": "無筊！",
            "illustrate": "否定、憤怒或不宜行事",
            "icon": "X"
        }
    if result == "笑筊":
        result_data = {
            "state": "笑筊",
            "num": "00",
            "text": "笑筊！",
            "illustrate": "不解、狀況不明",
            "icon": "T"
        }

    return result_data


# 擲筊運勢分析
def getOkamikujiFortune(result_illustrate, userMessage):
    
    # openai
    # askText = f"請扮演神明說話，針對「{userMessage}」表示「{result}」。（請在 20~50 字以內，用古文的方式回覆）"
    # result_fortune = openai(askText)

    # gemini
    askText = f"請扮演神明說話，針對「{userMessage}」表示「{result_illustrate}」。（請在 20~50 字以內，使用白話與古文穿插回覆）"
    result_fortune = gemini(askText)

    return result_fortune

# 擲筊結果 pageTemplate
def pageTemplate_result(result_img_url, result_data):
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
                                            "text": result_data["text"],
                                            "size": "lg",
                                            "color": "#c93a38",
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
                "text": "擲筊"
            },
        }
    }

    return pageTemplate

# 運勢分析結果 pageTemplate
def pageTemplate_fortune( result_bg_img_url, result_icon_img_url, result_fortune ):
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
                            "type": "image",
                            "url": result_icon_img_url,
                            "size": "xxs",
                        },
                        {
                            "type": "text",
                            "text": result_fortune,
                            "color": "#c93a38",
                            "wrap": True,
                            "size": "md",
                            "weight": "bold",
                            "lineSpacing": "8px",
                            "margin": "lg",
                        },
                        {
                            "type": "text",
                            "text": "　",
                            "wrap": True,
                            "size": "md",
                            "weight": "bold",
                            "lineSpacing": "8px",
                            "margin": "md",
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