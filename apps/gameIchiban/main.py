# 擲硬幣功能

from linebot import LineBotApi
from linebot.models import *

import os
import random
from apps.common.common import *
from apps.common.database import *

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))

def gameIchibanSet(event):

    source_id = getMessageSourceID(event)   # 取得訊息來源 ID
    file_path = 'gameIchiban'  # 選擇存取的檔案路徑

    # 獎項
    game_award = [
        "S", "A", "A", "A", "B",
        "B", "B", "C", "C", "C",
        "D", "D", "D", "D", "D",
        "E", "E", "E", "E", "E",
        "F", "F", "F", "F", "F",
    ]
    # 獎項洗牌
    random.shuffle(game_award)

    # 狀態
    game_state = [
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
    ]

    record_data = {
        "award": game_award,
        "state": game_state
    }
    # 寫入 JSON 檔案
    write_database_combined(file_path, source_id, record_data)

    game_text = "一番賞準備完成"
    game_img = "Q.png"

    # text_message = TextSendMessage(text="一番賞準備完成")
    # line_bot_api.reply_message(event.reply_token, text_message)

    # 取得結果畫面、顯示畫面
    pageTemplate_r = pageTemplate_result(game_text, game_img, record_data)
    pageTemplate_m = pageTemplate_menu(record_data)
    not_pressed_index = random.randint(1, 25)
    flexMessage_reply(event, pageTemplate_r, pageTemplate_m, not_pressed_index)
    return

def gameIchibanPlay(event, userMessage):

    # 整理文字
    userMessage = userMessage.replace('一番賞：', '')

    source_id = getMessageSourceID(event)   # 取得訊息來源 ID
    file_path = 'gameIchiban'  # 選擇存取的檔案路徑
    
    # 讀取檔案
    try:
        record_data = read_database_combined(file_path, source_id)
        game_state = record_data["state"] # 狀態
        game_award = record_data["award"] # 獎項

        # 字串需要為數字
        if userMessage.isdigit():
            user_index = int(userMessage) - 1
            # 數字判斷：需要符合 1~ 25
            if user_index >= 0 and user_index <= 25:
                game_start = True
            else:
                game_start = False

            # 符合數字條件：遊戲啟動
            if game_start:
                # 狀態為 0：表示還沒被按過
                if game_state[user_index] == 0:
                    game_state[ user_index ] = 1               # 更新狀態為 1
                    game_result = game_award[ user_index ]  # 取得獎項

                    if game_result == "S":
                        game_text = f"撕開 { str(user_index + 1) } 號，恭喜獲得 {game_result} 賞"
                        game_img = game_result + ".png"
                    else:
                        game_text = f"撕開 { str(user_index + 1) } 號，結果為 {game_result} 賞"
                        game_img = game_result + ".png"

                    # 紀錄更新
                    record_data = {
                        "award": game_award,
                        "state": game_state
                    }
                    # 寫入 JSON 檔案
                    write_database_combined(file_path, source_id, record_data)

                    # 取得未被按下的索引
                    not_pressed_index = get_not_pressed_index(game_state) + 1

                    # 取得結果畫面、顯示畫面
                    pageTemplate_r = pageTemplate_result(game_text, game_img, record_data)
                    pageTemplate_m = pageTemplate_menu(record_data)
                    flexMessage_reply(event, pageTemplate_r, pageTemplate_m, not_pressed_index)
                    return
                # 狀態為 1：表示已被按過
                else:
                    game_text = "這張紙已經被撕過了！請選別的！"
                    text_message = TextSendMessage(text= game_text )
                    line_bot_api.reply_message(event.reply_token, text_message)
                    return
            # 未符合數字條件
            else:
                game_text = "我們沒有那張紙！"
                text_message = TextSendMessage(text= game_text )
                line_bot_api.reply_message(event.reply_token, text_message)
                return
        else:
            game_text = "我們沒有那張紙！"
            text_message = TextSendMessage(text= game_text )
            line_bot_api.reply_message(event.reply_token, text_message)
            return
    except:
        game_text = "目前沒有任何一番賞～"
        text_message = TextSendMessage(text= game_text )
        line_bot_api.reply_message(event.reply_token, text_message)
        return


# 讀取
# def gameIchibanRead(event):
#     source_id = getMessageSourceID(event)   # 取得訊息來源 ID
#     file_path = 'gameIchiban'  # 選擇存取的檔案路徑
    
#     loaded_data = read_database_combined(file_path, source_id)  # 讀取檔案

#     text_message = TextSendMessage(text= str(loaded_data) ) # 印出結果
#     line_bot_api.reply_message(event.reply_token, text_message)



def get_not_pressed_index(list):

    # 檢查 list 是否所有元素都為 1
    if all(val == 1 for val in list):
        # 都為 1 時，回傳 -1
        random_index = -1
    
    else:
        # 收集不為 1 的元素索引
        indices = [i for i, val in enumerate(list) if val != 1]

        # 從索引列表中隨機選擇一個索引
        random_index = random.choice(indices)

    return random_index

# 一番賞結果
def pageTemplate_result(game_text, game_img, record_data):

    # 內容
    pageTemplate_contents = []

    # 結果圖
    pageTemplate_background = {
        "type": "image",
        "url": localImg("gameIchiban/"+game_img),
        "size": "full",
        "aspectMode": "cover",
        "aspectRatio": "1:1",
        "gravity": "center"
    }
    pageTemplate_contents.append( pageTemplate_background )

    # 一番賞結果文字
    pageTemplate_bottomText = {
        "type": "box",
        "layout": "horizontal",
        "contents": [
            {
                "type": "text",
                "size": "lg",
                "weight": "bold",
                "align": "center",
                "color": "#262458",
                "text": game_text
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
        }
    }
    # ========================= #
    
    return pageTemplate

# 一番賞選單
def pageTemplate_menu(record_data):

    pageTemplate_menu_contents = []
    
    for y in range(5):
        pageTemplate_menu_row_contents = []
        for x in range(5):
            
            btn_num = (x+1)+(5*y) # 按鈕數字
            if record_data["state"][btn_num - 1] == 0:
                state = "0" 
                btn_text = btn_num # 顯示按鈕數字
                pageTemplate_btn = pageTemplate_menu_btn(state, btn_num)
            elif record_data["state"][btn_num - 1] == 1:
                state = "1" 
                btn_text = record_data["award"][btn_num - 1] # 顯示獎項
                if btn_text != "S":
                    pageTemplate_btn = pageTemplate_menu_btn(state, btn_text)
                else:
                    state = "S" 
                    pageTemplate_btn = pageTemplate_menu_btn(state, btn_text)

            pageTemplate_menu_row_contents.append(pageTemplate_btn)

        pageTemplate_menu_row = {
            "type": "box",
            "layout": "horizontal",
            "contents": pageTemplate_menu_row_contents
        }
        pageTemplate_menu_contents.append(pageTemplate_menu_row)

    # 內容
    pageTemplate_contents = []

    # 底圖
    pageTemplate_background = {
        "type": "image",
        "url": localImg("gameIchiban/BG.png"),
        "size": "full",
        "aspectMode": "cover",
        "aspectRatio": "1:1",
        "gravity": "center"
    }
    pageTemplate_contents.append( pageTemplate_background )

    pageTemplate_title_and_btns = {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "text",
                "text": "剩餘獎項",
                "weight": "bold",
                "size": "lg",
                "color": "#262458"
            },
            {
                "type": "box",
                "layout": "vertical",
                "contents": pageTemplate_menu_contents,
                "paddingTop": "4px"
            }
        ],
        "position": "absolute",
        "offsetBottom": "0px",
        "offsetStart": "0px",
        "offsetEnd": "0px",
        "width": "100%",
        "height": "100%",
        "paddingAll": "8%",
        "alignItems": "center"
    }
    pageTemplate_contents.append( pageTemplate_title_and_btns )

    # ========================= #
    # 第二頁完整的內容
    pageTemplate = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": pageTemplate_contents,
            "paddingAll": "0px",
        }
    }
    # ========================= #
    return pageTemplate

# 一番賞按鈕
def pageTemplate_menu_btn(state, text):

    # 按鈕狀態( 0:未被按下, 1:已被按下, S:大獎已被按下）
    if state == "0":
        btn_color = "#262458"
        btn_backgroundColor = "#efe8ff"

        # 按鈕
        pageTemplate_btn = {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": str(text),
                    "size": "lg",
                    "weight": "bold",
                    "color": btn_color
                }
            ],
            "borderWidth": "2px",
            "borderColor": "#ffffff",
            "width": "44px",
            "height": "44px",
            "justifyContent": "center",
            "alignItems": "center",
            "cornerRadius": "16px",
            "backgroundColor": btn_backgroundColor,
            "action": {
                "type": "message",
                "label": "action",
                "text": "一番賞：" + str(text)
            }
        }
    else:
        if state == "1":
            btn_color = "#ffffff"
            btn_backgroundColor = "#6e9fed"
        elif state == "S":
            btn_color = "#ffffff"
            btn_backgroundColor = "#ED6E7D"

        # 按鈕
        pageTemplate_btn = {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": str(text),
                    "size": "lg",
                    "weight": "bold",
                    "color": btn_color
                }
            ],
            "borderWidth": "2px",
            "borderColor": "#ffffff",
            "width": "44px",
            "height": "44px",
            "justifyContent": "center",
            "alignItems": "center",
            "cornerRadius": "16px",
            "backgroundColor": btn_backgroundColor,
        }

    return pageTemplate_btn

# 包裝訊息，發送訊息
def flexMessage_reply(event, pageTemplate_result, pageTemplate_menu, not_pressed_index):

    # flexMessage 容器
    flex_message_contents = []

    # 將 pageTemplate 放入 flex_message_contents 中
    flex_message_contents.append( pageTemplate_result )
    flex_message_contents.append( pageTemplate_menu )

    # 快速回覆按鈕
    quick_reply_list = []
    if not_pressed_index != -1:
        quick_reply_item = QuickReplyButton(
            action=MessageAction(label = "隨機抽一張", text = f"一番賞：{str(not_pressed_index)}")
        )
        quick_reply_list.append( quick_reply_item )
    quick_reply_item = QuickReplyButton(
        action=MessageAction(label = "重置一番賞", text = "一番賞")
    )
    quick_reply_list.append( quick_reply_item )


    # 包裝訊息
    flex_message = FlexSendMessage(
        alt_text='有人在抽一番賞！',
        contents={
            # JSON 格式貼這邊
            "type": "carousel",
            "contents": flex_message_contents
        },
        quick_reply=QuickReply(
            items= quick_reply_list
        )
    )
    
    # 發送訊息
    line_bot_api.reply_message(event.reply_token, flex_message)
