from linebot import LineBotApi, WebhookHandler
from linebot.models import *

import os
import random
from apps.common.common import *
from apps.common.database import *
from apps.randomShuffle.template import *


line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))


# 洗牌
def random_shuffle_main(event, userMessage):
    userMessage = userMessage.replace('洗牌：', '')
    split_text_list = ['、', '，', '；', ',', '.']

    # 整理字串去除標點
    for text in split_text_list:
        userMessage = userMessage.replace(text, '、')

    # 切割
    split_list = [s.strip() for s in userMessage.split('、') if s.strip()]

    # 檢查洗牌的數量是否在允許範圍內
    if len(split_list) < 2:
        text_message = TextSendMessage(text="你洗太少牌囉～")
        line_bot_api.reply_message(event.reply_token, text_message)
        return
    if len(split_list) > 9:
        text_message = TextSendMessage(text="你洗太多牌囉～")
        line_bot_api.reply_message(event.reply_token, text_message)
        return

    shuffle_list = list(split_list)  # 複製一份清單
    random.shuffle(shuffle_list)     # 打亂
    card_state_list = [0] * len(shuffle_list) # 翻牌紀錄

    # 寫入
    source_id = getMessageSourceID(event)   # 取得訊息來源 ID
    file_path = 'randomShuffle'   # 選擇存取的檔案路徑
    write_data = { 
        "split_list": split_list,            # 未打亂的清單
        "shuffle_list": shuffle_list,        # 打亂的清單
        "card_state_list" : card_state_list, # 翻牌紀錄
    }
    write_database_combined(file_path, source_id, write_data)    # 寫入 JSON 檔案

    # 卡片未翻開數量
    card_count = len(shuffle_list)

    # 快速回覆按鈕
    quick_reply_list = random_shuffle_quick_reply_list(write_data, "start")
    
    flex_message_contents = []

    # flexMessage 一頁的內容
    firstPageTemplate = random_shuffle_first_page_template( "牌組已經洗牌！", card_count )
    flex_message_contents.append( firstPageTemplate )

    # 取得翻牌頁面
    pageTemplate = random_shuffle_page_template( write_data )
    flex_message_contents.append( pageTemplate )

    # 包裝訊息 發送訊息
    flex_message = FlexSendMessage(
        alt_text= '牌組已經洗牌！',
        contents={
            "type": "carousel",
            "contents": flex_message_contents
        },
        quick_reply = QuickReply(
            items = quick_reply_list
        )
    )
    line_bot_api.reply_message(event.reply_token, flex_message)


# 顯示翻牌
def random_shuffle_display(event):

    # 讀取
    source_id = getMessageSourceID(event)   # 取得訊息來源 ID
    file_path = 'randomShuffle'   # 選擇存取的檔案路徑
    loaded_data = read_database_combined(file_path, source_id)  # 讀取檔案

    try:
        flex_message_contents = []

        # 判斷是否所有牌都翻開
        if all(value == 1 for value in loaded_data["card_state_list"]):
            # flexMessage 一頁的內容
            firstPageTemplate = random_shuffle_first_page_template( "所有牌都翻開了！", 0 )
            flex_message_contents.append( firstPageTemplate )
        else:
            # 卡片未翻開數量: 計算 card_state_list 內的 0 的數量
            card_count = loaded_data["card_state_list"].count(0)

            # flexMessage 一頁的內容
            firstPageTemplate = random_shuffle_first_page_template( "請點擊抽牌～", card_count )
            flex_message_contents.append( firstPageTemplate )

        # 取得翻牌頁面
        pageTemplate = random_shuffle_page_template( loaded_data )
        flex_message_contents.append( pageTemplate )

        # 包裝訊息 發送訊息
        flex_message = FlexSendMessage(
            alt_text= "有人想抽牌！",
            contents={
                "type": "carousel",
                "contents": flex_message_contents
            },
        )
        line_bot_api.reply_message(event.reply_token, flex_message)


    except:
        # 包裝訊息 發送訊息
        text_message = TextSendMessage(
            text = "沒有設定任何牌組！",
        )
        line_bot_api.reply_message(event.reply_token, text_message)

# 執行翻牌
def random_shuffle_flop(event, userMessage):

    flop_number = userMessage.replace('翻牌：', '')
    flop_number = flop_number.replace('抽牌：', '')

    # 判斷是否要全部翻牌
    if flop_number == "全部翻開" or flop_number == "全部翻牌":
        flop_index = -1
        # 讀取
        source_id = getMessageSourceID(event)   # 取得訊息來源 ID
        file_path = 'randomShuffle'   # 選擇存取的檔案路徑
        loaded_data = read_database_combined(file_path, source_id)  # 讀取檔案
        game_state = "end"

        try:
            # 全部翻牌
            for index in range(len(loaded_data["card_state_list"])):
                loaded_data["card_state_list"][index] = 1
            write_database_combined(file_path, source_id, loaded_data)    # 寫入 JSON 檔案
            
            # 快速回覆按鈕
            quick_reply_list = random_shuffle_quick_reply_list(loaded_data, game_state)

            flex_message_contents = []

            # flexMessage 一頁的內容
            firstPageTemplate = random_shuffle_first_page_template( "所有牌都被翻開了！", 0 )
            flex_message_contents.append( firstPageTemplate )

            # 取得翻牌頁面
            pageTemplate = random_shuffle_page_template( loaded_data )
            flex_message_contents.append( pageTemplate )

            # 包裝訊息 發送訊息
            flex_message = FlexSendMessage(
                alt_text= "所有牌都被翻開了！",
                contents={
                    "type": "carousel",
                    "contents": flex_message_contents
                },
                quick_reply = QuickReply(
                    items = quick_reply_list
                )
            )
            line_bot_api.reply_message(event.reply_token, flex_message)

        except:
            # 包裝訊息 發送訊息
            text_message = TextSendMessage(
                text = "沒有設定任何牌組！",
            )
            line_bot_api.reply_message(event.reply_token, text_message)


    # 判斷 flop_number 是否為整數
    if flop_number.isdigit():
        flop_index = int(flop_number) - 1

        # 讀取
        source_id = getMessageSourceID(event)   # 取得訊息來源 ID
        file_path = 'randomShuffle'   # 選擇存取的檔案路徑
        loaded_data = read_database_combined(file_path, source_id)  # 讀取檔案
        game_state = "start"

        if 0 <= flop_index < len(loaded_data["card_state_list"]):
            if loaded_data["card_state_list"][flop_index] == 0:
                loaded_data["card_state_list"][flop_index] = 1
                write_database_combined(file_path, source_id, loaded_data)

                result_text = f"翻開了 {loaded_data['shuffle_list'][flop_index]}"
                
                # 判斷是否已經翻完
                if all(card_state == 1 for card_state in loaded_data["card_state_list"]):
                    # result_text += "\n所有牌都被翻開了！"
                    game_state = "end"

            else:
                flop_index = -1
                result_text = "這張牌已經被翻過了！"
                if game_state == "end":
                    result_text = "所有牌都被翻開了！"

        else:
            result_text = "翻牌號碼超出範圍！"

        try:

            # 卡片未翻開數量: 計算 card_state_list 內的 0 的數量
            card_count = loaded_data["card_state_list"].count(0)

            # 快速回覆按鈕
            quick_reply_list = random_shuffle_quick_reply_list(loaded_data, game_state)

            flex_message_contents = []

            # flexMessage 一頁的內容
            firstPageTemplate = random_shuffle_first_page_template( result_text, card_count )
            flex_message_contents.append( firstPageTemplate )

            # 取得翻牌頁面
            pageTemplate = random_shuffle_page_template( loaded_data , flop_index)
            flex_message_contents.append( pageTemplate )

            # 包裝訊息 發送訊息
            flex_message = FlexSendMessage(
                alt_text= result_text,
                contents={
                    "type": "carousel",
                    "contents": flex_message_contents
                },
                quick_reply = QuickReply(
                    items = quick_reply_list
                )
            )
            line_bot_api.reply_message(event.reply_token, flex_message)

        except:
            # 包裝訊息 發送訊息
            text_message = TextSendMessage(
                text = "沒有設定任何牌組！",
            )
            line_bot_api.reply_message(event.reply_token, text_message)

    else:
        text_message = TextSendMessage(text = "無效的翻牌號碼！")
        line_bot_api.reply_message(event.reply_token, text_message)
        return

# 取得快速回覆按鈕
def random_shuffle_quick_reply_list(loaded_data, game_state):

    # 快速回覆按鈕
    quick_reply_list = []

    # for index, value in enumerate(loaded_data["card_state_list"]):
    #     circle_numbers = ["➀","➁","➂","➃","➄","➅","➆","➇","➈","➉"]
    #     circle_numbers_flop = ["➊","➋","➌","➍","➎","➏","➐","➑","➒","➓"]
    #     if value == 0:
    #         quick_reply_item = QuickReplyButton(action=MessageAction(label = f"{circle_numbers[index]} ？？？", text = f"翻牌：{index+1}"))
    #         quick_reply_list.append(quick_reply_item)
    #     else: 
    #         quick_reply_item = QuickReplyButton(action=PostbackAction(label = f"{circle_numbers_flop[index]} {loaded_data['shuffle_list'][index]}", data = f"翻牌：{loaded_data['shuffle_list'][index]}"))
    #         quick_reply_list.append(quick_reply_item)
    

    if game_state != "end":
        quick_reply_item = QuickReplyButton(action=MessageAction(label = "● 全部翻開", text = "翻牌：全部翻開"))
        quick_reply_list.append(quick_reply_item)

    userMessage_revert = "洗牌：" + "、".join(loaded_data["split_list"])
    quick_reply_item = QuickReplyButton(action=MessageAction(label = "重新洗牌 ➜", text = f"{userMessage_revert}"))
    quick_reply_list.append(quick_reply_item)


    return quick_reply_list
