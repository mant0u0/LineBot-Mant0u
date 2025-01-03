# 海盜桶

from linebot import LineBotApi
from linebot.models import *

import os
import random
from apps.common.common import *
from apps.common.database import *

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))

# 海動桶設定
def gamePopUpPirateSet(event):

    source_id = getMessageSourceID(event)   # 取得訊息來源 ID
    file_path = 'gamePopUpPirate'  # 選擇存取的檔案路徑

    # 機關
    game_organ = [
        "1", "0", "0", "0", "0",
        "0", "0", "0", "0", "0",
        "0", "0", "0", "0", "0",
        "0", "0", "0", "0", "0",
        "0", "0", "0", "0", "0",
    ]

    # 機關洗牌
    random.shuffle(game_organ)

    # 狀態
    game_state = [
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
    ]

    record_data = {
        "organ": game_organ,
        "state": game_state
    }
    # 寫入 JSON 檔案
    write_database_combined(file_path, source_id, record_data)

    game_text = "海盜桶準備完成"
    game_img = "set.png"

    # text_message = TextSendMessage(text="海盜桶準備完成")
    # line_bot_api.reply_message(event.reply_token, text_message)

    # 取得結果畫面、顯示畫面
    pageTemplate_r = pageTemplate_result(game_text, game_img, record_data)
    pageTemplate_m = pageTemplate_menu(record_data)
    not_pressed_index = random.randint(1, 25)
    game_result = "0"
    flexMessage_reply(event, pageTemplate_r, pageTemplate_m, not_pressed_index, game_result)
    return

def gamePopUpPiratePlay(event, userMessage):

    # 整理文字
    userMessage = userMessage.replace('海盜桶：', '')

    source_id = getMessageSourceID(event)   # 取得訊息來源 ID
    file_path = 'gamePopUpPirate'  # 選擇存取的檔案路徑
    
    # 讀取檔案
    try:
        record_data = read_database_combined(file_path, source_id)
        game_state = record_data["state"] # 狀態
        game_organ = record_data["organ"] # 機關

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
                    game_state[ user_index ] = 1            # 更新狀態為 1
                    game_result = game_organ[ user_index ]  # 取得機關

                    if game_result == "0": # 海盜桶沒事
                        game_text = f"插入{ str(user_index + 1) }號，沒有任何事發生"
                        
                        count_state = game_state.count(1) # 計算有多少劍被插入
                        
                        # 更換前五次遊玩的圖片（沒插劍、插一支、插兩支...插五支，後面省略）
                        if count_state >= 5: count_state = 5
                        game_img = str(count_state) + ".png"

                        # 紀錄更新
                        record_data = {
                            "organ": game_organ,
                            "state": game_state
                        }
                        # 寫入 JSON 檔案
                        write_database_combined(file_path, source_id, record_data)
                    
                    else: # 海盜桶射出
                        game_text = f"插入{ str(user_index + 1) }號，海盜射出來了！"
                        game_img = "end.png"
                        # 移除資料
                        remove_database_combined(file_path, source_id)


                    # 取得未被按下的索引
                    not_pressed_index = get_not_pressed_index(game_state) + 1

                    # 取得結果畫面、顯示畫面
                    pageTemplate_r = pageTemplate_result(game_text, game_img, record_data)
                    pageTemplate_m = pageTemplate_menu(record_data)
                    flexMessage_reply(event, pageTemplate_r, pageTemplate_m, not_pressed_index, game_result)
                    return
                # 狀態為 1：表示已被按過
                else:
                    game_text = "這個位子被選過了！請選別的！"
                    text_message = TextSendMessage(text= game_text )
                    line_bot_api.reply_message(event.reply_token, text_message)
                    return
            # 未符合數字條件
            else:
                game_text = "沒有這個洞！"
                text_message = TextSendMessage(text= game_text )
                line_bot_api.reply_message(event.reply_token, text_message)
                return
        else:
            game_text = "沒有這個洞！"
            text_message = TextSendMessage(text= game_text )
            line_bot_api.reply_message(event.reply_token, text_message)
            return
    except:
        game_text = "海盜桶還沒被啟動～"
        text_message = TextSendMessage( 
            text= game_text,
            quick_reply=QuickReply(
                items= [
                    QuickReplyButton(
                        action=MessageAction(label = "啟動海盜桶", text = "海盜桶")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label = "如何遊玩？", text = "？海盜桶")
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, text_message)
        return


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

# 海盜桶結果
def pageTemplate_result(game_text, game_img, record_data):

    # 內容
    pageTemplate_contents = []

    # 結果圖
    pageTemplate_background = {
        "type": "image",
        "url": localImg("gamePopUpPirate/"+game_img),
        "size": "full",
        "aspectMode": "cover",
        "aspectRatio": "1:1",
        "gravity": "center"
    }
    pageTemplate_contents.append( pageTemplate_background )

    # 海盜桶結果文字
    pageTemplate_bottomText = {
        "type": "box",
        "layout": "vertical",
        "borderWidth": "1px",
        "position": "absolute",
        "offsetBottom": "0px",
        "paddingAll": "20px",
        "width": "100%",
        "height": "24%",
        "justifyContent": "center",
        "alignItems": "center",
        "contents": [
            {
                "type": "text",
                "text": game_text,
                "size": "lg",
                "color": "#683e32",
                "weight": "bold"
            }
        ],
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

# 海盜桶選單
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
                btn_text = btn_num # 顯示按鈕數字
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
        "url": localImg("gamePopUpPirate/background.png"),
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
                "text": "剩餘插槽",
                "weight": "bold",
                "size": "lg",
                "color": "#683e32"
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

# 海盜桶按鈕
def pageTemplate_menu_btn(state, text):

    # 按鈕狀態( 0:未被按下, 1:已被按下）
    if state == "0":
        btn_color = "#683e32"
        btn_backgroundColor = "#ffede1"

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
                "text": "海盜桶：" + str(text)
            }
        }
    else:
        btn_color = "#e9e2e0"
        btn_backgroundColor = "#fff9f5"

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
def flexMessage_reply(event, pageTemplate_result, pageTemplate_menu, not_pressed_index, game_result):

    # flexMessage 容器
    flex_message_contents = []
    # 快速回覆按鈕
    quick_reply_list = []

    # 將 pageTemplate 放入 flex_message_contents 中
    flex_message_contents.append( pageTemplate_result )
    
    # 判斷是否要顯示按鈕選單
    if game_result != "1":
        flex_message_contents.append( pageTemplate_menu )
        # 快速回覆按鈕
        quick_reply_item = QuickReplyButton(
            action=MessageAction(label = "隨便戳一個", text = f"海盜桶：{str(not_pressed_index)}")
        )
        quick_reply_list.append( quick_reply_item )


    quick_reply_item = QuickReplyButton(
        action=MessageAction(label = "重置海盜桶", text = "海盜桶")
    )
    quick_reply_list.append( quick_reply_item )


    # 包裝訊息
    flex_message = FlexSendMessage(
        alt_text='有人在玩海盜桶！',
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
