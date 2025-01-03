# 撲克牌

from linebot import LineBotApi
from linebot.models import *

import os
import random
from apps.common.common import *

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))



def random_poker_main(event, userMessage):

    # 當輸入「撲克牌」等同於「撲克牌：1」
    if userMessage == "撲克牌":
        userMessage = "撲克牌：1"
    
    # 必須為「撲克牌：num」才會觸發撲克牌
    if userMessage.find('撲克牌：') == 0:
        userMessage = userMessage.replace('撲克牌：', '')

        # 輸入撲克牌數量
        num = int(userMessage)

        # 判斷撲克牌數量 ( 1~54 張)
        if num > 54:
            text_message = TextSendMessage(text="撲克牌不足，無法抽牌！")
            line_bot_api.reply_message(event.reply_token, text_message)
        if num == 0:
            text_message = TextSendMessage(text="我不知道你想抽什麼？")
            line_bot_api.reply_message(event.reply_token, text_message)


        # 建立數列 1~54
        cards = list(range(1, 55))

        # 打亂數列
        random.shuffle(cards)

        # 抽出 num 張牌
        draw_cards = cards[:num]

        # 排序
        draw_cards.sort()

        # 取得卡片名稱與圖片ID
        draw_cards_name, draw_cards_id = get_poker_name(draw_cards)

        # 顯示文字：文字太多省略不寫 
        if len(draw_cards_name) < 6:
            result_text = ' '.join(draw_cards_name)
        else:
            result_text = "撲克牌結果！"


        # 圖片ID：一頁最多顯示 8 張牌，將牌分成 8 張一頁 cards_page
        draw_cards_id_page = [draw_cards_id[i:i+8] for i in range(0, len(draw_cards_id), 8)]

        # flexMessage 容器
        flex_message_contents = []

        # 處理 flexMessage 一頁的內容（背景 + 文字 + 多張牌的圖片）
        for cards_page in draw_cards_id_page:

            # pageTemplate 內容
            pageTemplate_contents = []

            # 背景
            pageTemplate_BG = {
                "type": "image",
                "url": localImg("randomPoker/BG.png"),
                "size": "full",
                "aspectMode": "cover",
                "aspectRatio": "1:1",
                "gravity": "top"
            }

            pageTemplate_contents.append(pageTemplate_BG)

            # 文字
            pageTemplate_text = {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": result_text,
                                "size": "lg",
                                "weight": "bold",
                                "color": "#208148",
                                "align": "center"
                            }
                        ],
                        "paddingAll": "20px"
                    }
                ],
                "position": "absolute",
                "width": "100%",
                "height": "100%",
                "justifyContent": "flex-end"
            }
            pageTemplate_contents.append(pageTemplate_text)

            # 撲克牌：需要計算每一張牌的位置
            offsetMin = -70
            offset = offsetMin / 7 * (len(cards_page) - 1)

            for card_id in cards_page:

                card_img = {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "image",
                            "url": localImg(f"randomPoker/{card_id}.png"),
                            "size": "180px"
                        }
                    ],
                    "position": "absolute",
                    "paddingAll": "20px",
                    "width": "100%",
                    "offsetStart": str(offset) + "px"
                }
                offset = offset + 20
                pageTemplate_contents.append(card_img)

            # flexMessage 一頁的內容
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
                        "text": "撲克牌：" + str(userMessage),
                    },
                }
            }

            # 將 pageTemplate 放入 flex_message_contents 中
            flex_message_contents.append(pageTemplate)

        # 包裝訊息
        flex_message = FlexSendMessage(
            alt_text= '有人在抽撲克牌！',
            contents={
                "type": "carousel",
                "contents": flex_message_contents
                }
            )
        
        # 發送訊息
        line_bot_api.reply_message(event.reply_token, flex_message)





# 取得卡片名稱
def get_poker_name(draw_cards):

    draw_cards_name = []
    draw_cards_id = []

    for card in draw_cards:

        # rank: 牌的數字（除 13 的餘數）
        rank = card % 13
        # suit: 牌的花色（除 13 的商，K 會被整除所以須 -1）
        suit = suit = card // 13
        # suitId: 圖片的 ID
        suitId = ""
        
        # 牌的數字
        if rank == 1:
            rank = "A"
        elif rank == 11:
            rank = "J"
        elif rank == 12:
            rank = "Q"
        elif rank == 0:
            rank = "K"
            suit = suit - 1

        # 牌的花色
        if suit == 0:
            suit = "♣"
            suitId = "C"
        if suit == 1:
            suit = "♦"
            suitId = "D"
        if suit == 2:
            suit = "♥"
            suitId = "H"
        if suit == 3:
            suit = "♠"
            suitId = "S"

        # 卡片名稱
        card_name = f"{suit}{rank}"
        card_id = f"{suitId}{rank}"
        
        # 鬼牌
        if card == 53:
            card_name = "JOKER"
            card_id = "JOKER1"
        if card == 54:
            card_name = "JOKER"
            card_id = "JOKER2"
            
        draw_cards_name.append(card_name)
        draw_cards_id.append(card_id)

    return draw_cards_name, draw_cards_id