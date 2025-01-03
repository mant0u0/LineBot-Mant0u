# 塔羅牌

from linebot import LineBotApi
from linebot.models import *

import os
import json
import random
from apps.common.common import *
from apps.randomTarotCards.template import *
from apps.ai.gemini import gemini

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))


def random_tarot_cards_main(event, userMessage):

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

        input_ai_text = f"請根據塔羅牌{card_name}{card_direction}，依據「{card_illustrate}」牌意解釋關於「{userMessage}」的分析，限用20~50字元來解釋"
        result_text = f"{card_name} - {card_direction}"
        result_text_fortune = gemini(input_ai_text)
        result_img_url = localImg(f"randomTarotCards/{card_direction_en}/{card_name_img}.png")

        if result_text_fortune != "":

            # flexMessage 容器
            flex_message_contents = []

            # 抽籤結果：將 pageTemplate 放入 flex_message_contents 中
            pageTemplate = random_tarotCards_first_page_template(result_img_url, result_text)
            flex_message_contents.append( pageTemplate )

            # 運勢分析結果：將 pageTemplate 放入 flex_message_contents 中
            pageTemplate = random_tarotCards_fortune_page_template( result_text, result_text_fortune, userMessage )
            flex_message_contents.append( pageTemplate )

            # 隨機產生下一句話
            sentence_1 = random_sentence()
            sentence_2 = random_sentence()
            sentence_3 = random_sentence()

            

            # 包裝訊息
            flex_message = FlexSendMessage(
                alt_text= '塔羅牌占卜！',
                contents={
                    "type": "carousel",
                    "contents": flex_message_contents
                },
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton( action=MessageAction(label="● 再問一次", text= "塔羅牌：" + userMessage) ),
                        QuickReplyButton( action=MessageAction(label="○ " + sentence_1, text='塔羅牌：'+ sentence_1) ),
                        QuickReplyButton( action=MessageAction(label="○ " + sentence_2, text='塔羅牌：'+ sentence_2) ),
                        QuickReplyButton( action=MessageAction(label="○ " + sentence_3, text='塔羅牌：'+ sentence_3) ),
                        QuickReplyButton( action=MessageAction(label="改用抽籤 ➜", text='抽籤：'+ userMessage) ),
                        QuickReplyButton( action=MessageAction(label="改用擲筊 ➜", text='擲筊：'+ userMessage) ),
                    ]
                )
            )
            
            # 發送訊息
            line_bot_api.reply_message(event.reply_token, flex_message)
            return

