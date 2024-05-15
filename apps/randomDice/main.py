# 骰子

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

import os
import random
import re
from apps.common.common import *

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))


# 骰子種類定義
dice_type_define = {
    "D": {
        "name": "D",
        "point": 6
    },
    "D4": {
        "name": "D4",
        "point": 4
    },
    "D6": {
        "name": "D6",
        "point": 6
    },
    "D8": {
        "name": "D8",
        "point": 8
    },
    "D10": {
        "name": "D10",
        "point": 10
    },
    "D12": {
        "name": "D12",
        "point": 12
    },
    "D20":  {
        "name": "D20",
        "point": 20
    },
}


# 骰子主程式
def randomDiceMain(event, userMessage):

    # 紀錄動作指令
    dice_action_text = userMessage

    if userMessage == '一個骰子' or userMessage == '一顆骰子' or userMessage == '骰子':
        userMessage = '骰子：1'
    elif userMessage == '兩個骰子' or userMessage == '兩顆骰子' or userMessage == '二個骰子'or userMessage == '二顆骰子':
        userMessage = '骰子：2'
    elif userMessage == '三個骰子' or userMessage == '三顆骰子':
        userMessage = '骰子：3'
    elif userMessage == '四個骰子' or userMessage == '四顆骰子':
        userMessage = '骰子：4'
    elif userMessage == '五個骰子' or userMessage == '五顆骰子':
        userMessage = '骰子：5'

    if userMessage.find('骰子：') == 0:
        # 整理文字
        userMessage = userMessage.replace('骰子：', '')

        # 取得骰子種類清單、骰子模式、錯誤訊息
        dice_list, dice_model, dice_message = get_dice_list(userMessage)

        if dice_model != "error" or dice_model == "null":
            # 取得骰子點數結果
            dice_result = get_dice_result(dice_list)
            # 顯示模式判斷
            if dice_model == "default":
                # 取得結果畫面、顯示畫面
                pageTemplate = pageTemplate_result(dice_list, dice_result, dice_action_text)
                flexMessage_reply(event, pageTemplate, dice_action_text)
                return
            elif dice_model == "advanced":
                # 取得結果畫面、顯示畫面
                pageTemplate = pageTemplate_result(dice_list, dice_result, dice_action_text)
                flexMessage_reply(event, pageTemplate, dice_action_text)
                return
            elif dice_model == "excess":
                result_text = f"各別點數：{str(dice_result)[1:-1]}\n\n骰子數量：{len(dice_result)} 顆\n\n點數總計：{sum(dice_result)} 點"
                # 包裝訊息、發送訊息
                text_message = TextSendMessage(text= result_text )
                line_bot_api.reply_message(event.reply_token, text_message)
                return
        else:
            # 包裝訊息、發送訊息
            text_message = TextSendMessage(text= dice_message )
            line_bot_api.reply_message(event.reply_token, text_message)
            return



# 取得骰子種類清單
def get_dice_list(userMessage):

    dice_list = []    # 骰子種類清單
    dice_model = ""   # 骰子顯示模式
    dice_message = "" # 骰子訊息

    # 輸入 1~10 數值：使用預設骰子 (D)，數值值表示骰子數
    if userMessage.isdigit():
        for i in range(int(userMessage)):
            dice_list.append("D")
        
        if int(userMessage)>= 1 and int(userMessage)<= 10:
            dice_model = "default"  # 一般模式 (六面體骰子)
        elif int(userMessage)> 10:
            dice_model = "excess"   # 過量模式
        elif int(userMessage)== 0:
            dice_model = "null"     # 沒有任何骰子
            dice_message = "沒有擲出任何骰子！"

        return dice_list, dice_model, dice_message

    # 輸入指定熟子種類：建立骰子種類清單，如：["D12", "D4", "D6", "D4"...]
    else:
        userMessage = userMessage.upper()                   # 將英文全部轉為大寫
        dice_list = re.split(r'[；，、;, ]', userMessage)   # 字串分割
        dice_list = [x for x in dice_list if x.strip()]     # 去除空白元素
        dice_list = ["D6" if x == "D" else x for x in dice_list]  # 將 D 全取代為 D6 骰子

        # 檢查語法是否正確
        dice_list, dice_message, dice_model = check_dice_list(dice_list)

        # 判斷模式
        if dice_model != "error" :
            if len(dice_list)>= 1 and len(dice_list)<= 10:
                dice_model = "advanced"  # 進階模式 (D20 骰子)
            elif len(dice_list)> 10:
                dice_model = "excess"    # 過量模式
            elif len(dice_list)== 0:
                dice_model = "null"      # 沒有任何骰子
                dice_message = "沒有擲出任何骰子！"


        return dice_list, dice_model, dice_message


# 取得點數
def get_dice_result(dice_list):
    # 骰子點數結果
    dice_result = []
    
    for i in dice_list:
        # 取得骰子點數
        dice_points = random.randint(1, dice_type_define[i]["point"])
        dice_result.append(dice_points)
    return dice_result


# 檢查指令
def check_dice_list(dice_list):
    
    final_dice_list = [] # 骰子種類清單（數量轉換） 
    dice_model = ""      # 骰子顯示模式
    dice_message = ""    # 骰子訊息
    
    # 骰子指令：
    # ["2D6","D10"] -> ["D6","D6","D10"]
    # ["X2D6","D10"] -> 骰子數量錯誤
    # ["2D6","DX10"] -> 骰子類型錯誤

    # 將字串轉為骰子的數量與種類
    for dice in dice_list:
        if "D" in dice:
            dice_num, dice_type = dice.split("D")

            # 判斷骰子數量：轉為整數後確認是否正確，如果 dice_num 是空字串，則設置為 1。
            try:
                dice_num = int(dice_num) if dice_num else 1
            except Exception:
                # print("骰子數量設定錯誤")
                dice_message = "數量設定錯誤！"
                dice_model = "error"
                break

            # 判斷骰子類型
            try:
                dice_type = "D" + dice_type
                dice_type = dice_type_define[dice_type]["name"]
            except Exception:
                # print("骰子類型設定錯誤")
                dice_message = "類型設定錯誤！"
                dice_model = "error"
                break

            final_dice_list.extend([dice_type] * dice_num)
        
        else:
            # final_dice_list.append(dice)
            dice_message = "沒有這種骰子！"
            dice_model = "error"
            break


        

    return final_dice_list, dice_message, dice_model


# 骰子結果
def pageTemplate_result(dice_list, dice_result, dice_action_text):

    # 內容
    pageTemplate_contents = []

    # 主題
    pageTemplate_theme_list = [
        {
            "name":"yellow",
            "color": "#93563b"
        },
        {
            "name":"orange",
            "color": "#a55353"
        },
        {
            "name":"blue",
            "color": "#5360a5"
        },
        {
            "name":"green",
            "color": "#2B9575"
        },
        {
            "name":"red",
            "color": "#bb4747"
        },
        {
            "name":"gray",
            "color": "#6f6f6f"
        },
    ]
    pageTemplate_theme = random.choice(pageTemplate_theme_list)
    
    # 背景圖
    pageTemplate_background = {
        "type": "image",
        "url": localImg(f"randomDice/{pageTemplate_theme['name']}/background.png"),
        "size": "full",
        "aspectRatio": "1:1",
        "aspectMode": "cover"
    }
    pageTemplate_contents.append( pageTemplate_background )

    # 骰子尺寸與位置
    dice_position = [
        {
            "num": 1,
            "size" : "xxl",
            "x": ["0%"],
            "y": ["0%"]
        },
        {
            "num": 2,
            "size" : "xl",
            "x": ["-20%","20%"],
            "y": [  "0%", "0%"]
        },
        {
            "num": 3,
            "size" : "xl",
            "x": [  "0%", "-20%","20%"],
            "y": ["-10%",   "7%", "7%"]
        },
        {
            "num": 4,
            "size" : "lg",
            "x": [ "17%","-17%","-17%","17%"],
            "y": ["-14%","-14%", "14%","14%"]
        },
        {
            "num": 5,
            "size" : "lg",
            "x": ["18%", "-18%","0%","-18%","18%"],
            "y": ["-15%","-15%","0%", "15%","15%"]
        },
        {
            "num": 6,
            "size" : "lg",
            "x": ["-31%",  "0%", "31%","-31%",  "0%", "31%"],
            "y": ["-12%","-12%","-12%", "13%", "13%", "13%"]
        },
        {
            "num": 7,
            "size" : "md",
            "x": ["-28%","0%","28%","-14%","14%","-28%","28%"],
            "y": ["-16%","-16%","-16%","0%","0%","16%","16%"]
        },
        {
            "num": 8,
            "size" : "md",
            "x": ["-28%","0%","28%","-14%","14%","-28%","0%","28%"],
            "y": ["-16%","-16%","-16%","0%","0%","16%","16%","16%"]
        },
        {
            "num": 9,
            "size" : "md",
            "x": ["-26%","0%","26%","-26%","0%","26%","-26%","0%","26%"],
            "y": ["-20%","-20%","-20%","0%","0%","0%","20%","20%","20%"]
        },
        {
            "num": 10,
            "size" : "md",
            "x": ["-27%","0%","27%"  ,"-40%","-13%","13%","40%",  "-27%","0%","27%"],
            "y": ["-15%","-15%","-15%",  "0%","0%","0%","0%",  "15%","15%","15%"]
        },
    ]

    # 骰子
    dice_result_len = len(dice_result)
    dice_result_sum = sum(dice_result)
    for index, dice in enumerate(dice_result):
        dice_point = str(dice)        # 骰子點數
        dice_type  = dice_list[index] # 骰子類型
        pageTemplate_dice = {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "image",
                    "url": localImg(f"randomDice/{pageTemplate_theme['name']}/{dice_type}/{dice_point}.png"),
                    "size": dice_position[dice_result_len-1]["size"] # 骰子尺寸
                }
            ],
            "position": "absolute",
            "width": "100%",
            "height": "75%",
            "justifyContent": "center",
            "alignItems": "center",
            "offsetStart": dice_position[dice_result_len-1]["x"][index], # X 位移
            "offsetTop":   dice_position[dice_result_len-1]["y"][index]  # Y 位移
        }
        pageTemplate_contents.append( pageTemplate_dice )

    # 底部圖片
    pageTemplate_bottom = {
        "type": "image",
        "url": localImg(f"randomDice/{pageTemplate_theme['name']}/bottom.png"),
        "size": "full",
        "aspectRatio": "1:1",
        "aspectMode": "cover",
        "position": "absolute"
    }
    pageTemplate_contents.append( pageTemplate_bottom )

    # 底部文字
    pageTemplate_bottomText = {
        "type": "box",
        "layout": "horizontal",
        "contents": [
            {
                "type": "text",
                "size": "lg",
                "weight": "bold",
                "align": "center",
                "color": pageTemplate_theme['color'],
                "text": "骰子擲出 "+str(dice_result_sum)+" 點"
            }
        ],
        "position": "absolute",
        "offsetStart": "0px",
        "paddingAll": "20px",
        "offsetBottom": "0px",
        "offsetEnd": "0px"
    }
    pageTemplate_contents.append( pageTemplate_bottomText )

    # ========================= #
    
    # 一頁完整的內容
    pageTemplate = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": pageTemplate_contents,
            "paddingAll": "0px",
            "action": {
                "type": "message",
                "label": "action",
                "text": dice_action_text ,
            },
        }
    }

    return pageTemplate


# 包裝訊息，發送訊息
def flexMessage_reply(event, pageTemplate, dice_action_text):

    # flexMessage 容器
    flex_message_contents = []

    # 將 pageTemplate 放入 flex_message_contents 中
    flex_message_contents.append( pageTemplate )

    # 包裝訊息
    flex_message = FlexSendMessage(
        alt_text='有人擲出骰子！',
        contents={
            # JSON 格式貼這邊
            "type": "carousel",
            "contents": flex_message_contents
        },
        quick_reply=QuickReply(
            items=[
                QuickReplyButton(
                    action=MessageAction(label = "再擲一次", text = dice_action_text)
                ),
                QuickReplyButton(
                    action=MessageAction(label = "一顆骰子", text = "一顆骰子")
                ),
                QuickReplyButton(
                    action=MessageAction(label = "兩顆骰子", text = "兩顆骰子")
                ),
                QuickReplyButton(
                    action=MessageAction(label = "三顆骰子", text = "三顆骰子")
                ),
                QuickReplyButton(
                    action=MessageAction(label = "多面骰子", text = "骰子：" + random.choice(["D4","D6","D8","D10","D12","D20"]) )
                ),
            ]
        )
    )
    
    print("[ReplyToken]"+ str(event.reply_token))

    # 發送訊息
    line_bot_api.reply_message(event.reply_token, flex_message)
