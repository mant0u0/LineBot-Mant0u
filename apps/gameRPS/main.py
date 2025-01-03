# 猜拳
from linebot import LineBotApi
from linebot.models import *

import os

from apps.common.common import *
from apps.common.database import *

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))


def gameRPSMain(event):
    flex_message_contents = []

    pageTemplate = pageTemplate_menu()

    flex_message_contents.append(pageTemplate)

    # 包裝訊息
    flex_message = FlexSendMessage(
        alt_text= "有人準備猜拳！",
        contents={
            # JSON 格式貼這邊
            "type": "carousel",
            "contents": flex_message_contents
        },
        quick_reply=QuickReply(
            items=[
                QuickReplyButton(
                    action=PostbackAction(label="剪刀", data="猜拳：剪刀")
                ),
                QuickReplyButton(
                    action=PostbackAction(label="石頭", data="猜拳：石頭")
                ),
                QuickReplyButton(
                    action=PostbackAction(label="布", data="猜拳：布")
                ),
            ]
        )
    )
    
    # 發送訊息
    line_bot_api.reply_message(event.reply_token, flex_message)


def gameRPSPlay(event, userPostback):
    # 整理文字
    punch = userPostback.replace('猜拳：', '')

    source_id = getMessageSourceID(event)   # 取得訊息來源 ID
    file_path = 'gameRPS'  # 選擇存取的檔案路徑

    # 取得使用者名稱
    userId, userName = getUserName(event)

    # 遊戲階段 game_stage
    game_stage = 0
    try:
        # 讀取檔案
        record_data = read_database_combined(file_path, source_id)

        if record_data["id"] != "":
            game_stage = 2
        else:
            game_stage = 1
    except:
        game_stage = 1

    # 遊戲階段 1 : 玩家 1 出拳 - 等待
    if game_stage == 1:
        if userName == "玩家": userName = "玩家 1"
        # 取得紀錄：第一位玩家的名字、ID、拳
        record_data = {
            "name": userName,
            "id": userId,
            "punch": punch,
        }
        # 寫入 JSON 檔案
        write_database_combined(file_path, source_id, record_data)
        

        text_message = TextSendMessage(
            text= f"{userName} 準備好了！", 
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        action=PostbackAction(label="剪刀", data="猜拳：剪刀")
                    ),
                    QuickReplyButton(
                        action=PostbackAction(label="石頭", data="猜拳：石頭")
                    ),
                    QuickReplyButton(
                        action=PostbackAction(label="布", data="猜拳：布")
                    ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, text_message)
        return
    
    # 遊戲階段 2 : 玩家 2 出拳 - 顯示結果
    elif game_stage == 2:
        if userName == "玩家": userName = "玩家 2"
        player_1 = record_data
        player_2 = {
            "name": userName,
            "id": userId,
            "punch": punch,
        }

        if player_1["punch"] == player_2["punch"]:
            game_text = "平手！"

        elif player_1["punch"] == "剪刀":
            if player_2["punch"] == "布":
                game_text = f"{player_1['name']} 獲勝！"
            elif player_2["punch"] == "石頭":
                game_text = f"{player_2['name']}  獲勝！"

        elif player_1["punch"] == "石頭":
            if player_2["punch"] == "剪刀":
                game_text = f"{player_1['name']}  獲勝！"
            elif player_2["punch"] == "布":
                game_text = f"{player_2['name']}  獲勝！"

        elif player_1["punch"] == "布":
            if player_2["punch"] == "石頭":
                game_text = f"{player_1['name']}  獲勝！"
            elif player_2["punch"] == "剪刀":
                game_text = f"{player_2['name']}  獲勝！"

        # 移除資料
        remove_database_combined(file_path, source_id)

        flex_message_contents = []
        pageTemplate_r = pageTemplate_result(player_1, player_2, game_text)
        pageTemplate_m = pageTemplate_menu()
        flex_message_contents.append(pageTemplate_r)
        flex_message_contents.append(pageTemplate_m)

        # 包裝訊息
        flex_message = FlexSendMessage(
            alt_text= "有人準備猜拳！",
            contents={
                # JSON 格式貼這邊
                "type": "carousel",
                "contents": flex_message_contents
            },
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        action=PostbackAction(label="剪刀", data="猜拳：剪刀")
                    ),
                    QuickReplyButton(
                        action=PostbackAction(label="石頭", data="猜拳：石頭")
                    ),
                    QuickReplyButton(
                        action=PostbackAction(label="布", data="猜拳：布")
                    ),
                ]
            )
        )
        
        # 發送訊息
        line_bot_api.reply_message(event.reply_token, flex_message)
        return

# 讀取（測試用）
def gameRPSRead(event):
    
    source_id = getMessageSourceID(event)   # 取得訊息來源 ID
    file_path = 'gameRPS'  # 選擇存取的檔案路徑
    
    loaded_data = read_database_combined(file_path, source_id)  # 讀取檔案

    text_message = TextSendMessage(text= str(loaded_data) ) # 印出結果
    line_bot_api.reply_message(event.reply_token, text_message)

# 取得使用者名稱，如果沒有加好友，預設為「玩家」
def getUserName(event):
    userId = event.source.user_id
    try:
        profile = line_bot_api.get_profile(userId)
        profile = json.loads(str(profile))  # 字串轉字典型態
        userName = str(profile['displayName'])
    except:
        userName = '玩家'

    return userId, userName


# 猜拳選單
def pageTemplate_menu():
    pageTemplate_contents = [
        {
            "type": "text",
            "text": "猜拳！",
            "weight": "bold",
            "size": "lg",
            "color": "#a06348",
            "align": "center"
        }, {
            "type": "text",
            "text": "你想要出什麼拳？",
            "weight": "bold",
            "size": "sm",
            "color": "#a0634899",
            "align": "center",
            "margin": "4px"
        }, {
            "type": "separator",
            "margin": "12px"
        }
    ]
    
    btn_list = ["剪刀", "石頭", "布"]

    for i in range(len(btn_list)):
        # 按鈕文字
        btn_item_text = btn_list[i]
        # 按鈕
        btn_item = {
            "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": btn_item_text,
                        "weight": "bold",
                        "color": "#a06348"
                    }
                ],
            "paddingAll": "12px",
            "justifyContent": "center",
            "alignItems": "center",
            "action": {
                "type": "postback",
                "data": "猜拳：" + btn_item_text,
            }
        }
        pageTemplate_contents.append(btn_item)
        # 分隔線
        if i != len(btn_list) - 1:
            pageTemplate_contents.append({"type": "separator"})

    pageTemplate = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "image",
                    "url": localImg("banner/RPS.png"),
                    "size": "100%",
                    "aspectMode": "fit",
                    "margin": "0px",
                    "position": "relative",
                    "aspectRatio": "1000:280"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": pageTemplate_contents,
                    "paddingAll": "12px",
                    "paddingTop": "4px",
                }
            ],
            "paddingAll": "0px"
        }
    }
    
    return pageTemplate


# 猜拳結果
def pageTemplate_result(player_1, player_2, game_text):

    # 結果圖
    result_img = player_1["punch"] + player_2["punch"]
    result_img = result_img.replace('石頭', 'R')
    result_img = result_img.replace('布', 'P')
    result_img = result_img.replace('剪刀', 'S')
    result_img = localImg(f"gameRPS/{result_img}.png")

    # 文字寬度
    player_1_text_width = get_char_width_ratio(player_1["name"]) * 10
    player_2_text_width = get_char_width_ratio(player_2["name"]) * 10

    pageTemplate = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                # 結果圖
                {
                    "type": "image",
                    "url": result_img,
                    "size": "full",
                    "aspectMode": "cover",
                    "aspectRatio": "1:1",
                    "gravity": "center"
                },
                # 玩家 1 名稱
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": player_1["name"],
                            "color": "#ffffff",
                            "align": "center",
                            "size": "xs"
                        }
                    ],
                    "position": "absolute",
                    "cornerRadius": "20px",
                    "backgroundColor": "#ff7550",
                    "paddingAll": "4px",
                    "paddingStart": "8px",
                    "paddingEnd": "8px",
                    "offsetTop": "20px",
                    "width": str(player_1_text_width) + "px" ,
                    "maxWidth": "100px",
                    "offsetStart": "20px"
                },
                # 玩家 2 名稱
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": player_2["name"],
                            "color": "#ffffff",
                            "align": "center",
                            "size": "xs"
                        }
                    ],
                    "position": "absolute",
                    "cornerRadius": "20px",
                    "backgroundColor": "#8ab780",
                    "paddingAll": "4px",
                    "paddingStart": "8px",
                    "paddingEnd": "8px",
                    "offsetTop": "20px",
                    "width": str(player_2_text_width) + "px" ,
                    "maxWidth": "100px",
                    "offsetEnd": "20px"
                },
                # 底部文字
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                    {
                        "type": "text",
                        "size": "lg",
                        "weight": "bold",
                        "align": "center",
                        "color": "#a06348",
                        "text": game_text
                    }
                    ],
                    "position": "absolute",
                    "offsetStart": "0px",
                    "paddingAll": "20px",
                    "offsetBottom": "0px",
                    "offsetEnd": "0px"
                }
            ],
            "paddingAll": "0px",
        }
        }

    return pageTemplate
