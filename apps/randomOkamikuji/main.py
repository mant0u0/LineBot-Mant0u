# 日本神社抽籤
from linebot import LineBotApi
from linebot.models import *

import os
import random

from apps.ai.gemini import gemini_ai
from apps.common.common import *
from apps.randomOkamikuji.template import *


line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))

def random_okamikuji_main(event, userMessage):

    # 抽籤結果對照表
    okamikuji_result_table = [
        {
            "result_name": "大吉",
            "page_text": "抽籤結果：大吉！？",
            "first_page_img_url": localImg(f"randomOkamikuji/item-1.jpg"),
            "fortune_page_img_url": localImg(f"randomOkamikuji/bg-1.jpg"),
            "color": "#10496d",
        },
        {
            "result_name": "中吉",
            "page_text": "抽籤結果：中吉！！",
            "first_page_img_url": localImg(f"randomOkamikuji/item-2.jpg"),
            "fortune_page_img_url": localImg(f"randomOkamikuji/bg-2.jpg"),
            "color": "#10496d",
        },
        {
            "result_name": "小吉",
            "page_text": "抽籤結果：小吉！",
            "first_page_img_url": localImg(f"randomOkamikuji/item-3.jpg"),
            "fortune_page_img_url": localImg(f"randomOkamikuji/bg-3.jpg"),
            "color": "#10496d",
        },
        {
            "result_name": "吉",
            "page_text": "抽籤結果：吉。",
            "first_page_img_url": localImg(f"randomOkamikuji/item-4.jpg"),
            "fortune_page_img_url": localImg(f"randomOkamikuji/bg-4.jpg"),
            "color": "#10496d",
        },
        {
            "result_name": "末吉",
            "page_text": "抽籤結果：末吉。",
            "first_page_img_url": localImg(f"randomOkamikuji/item-5.jpg"),
            "fortune_page_img_url": localImg(f"randomOkamikuji/bg-5.jpg"),
            "color": "#10496d",
        },
        {
            "result_name": "凶",
            "page_text": "抽籤結果：凶！",
            "first_page_img_url": localImg(f"randomOkamikuji/item-6.jpg"),
            "fortune_page_img_url": localImg(f"randomOkamikuji/bg-6.jpg"),
            "color": "#353535",
        },
        {
            "result_name": "大凶",
            "page_text": "抽籤結果：大凶！？",
            "first_page_img_url": localImg(f"randomOkamikuji/item-7.jpg"),
            "fortune_page_img_url": localImg(f"randomOkamikuji/bg-7.jpg"),
            "color": "#353535",
        }
    ]

    # 取得抽籤結果
    okamikuji_result = random.choice(okamikuji_result_table)

    # 一般模式：只顯示抽籤結果
    if userMessage == "抽籤":

        # flexMessage 容器
        flex_message_contents = []

        # 抽籤結果：將 pageTemplate 放入 flex_message_contents 中
        pageTemplate = random_okamikuji_first_page_template(okamikuji_result)
        flex_message_contents.append( pageTemplate )
    
        # 隨機產生下一句話
        sentence_1 = random_sentence()
        sentence_2 = random_sentence()
        sentence_3 = random_sentence()

        # 包裝訊息
        flex_message = FlexSendMessage(
            alt_text= '有人抽籤囉！',
            contents={
                "type": "carousel",
                "contents": flex_message_contents
            },
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton( action=MessageAction(label="● 再抽一次", text="抽籤") ),
                    QuickReplyButton( action=MessageAction(label="○ " + sentence_1, text='抽籤：'+ sentence_1) ),
                    QuickReplyButton( action=MessageAction(label="○ " + sentence_2, text='抽籤：'+ sentence_2) ),
                    QuickReplyButton( action=MessageAction(label="○ " + sentence_3, text='抽籤：'+ sentence_3) ),
                ]
            )
        )
        
        # 發送訊息
        line_bot_api.reply_message(event.reply_token, flex_message)

    #  AI 模式：顯示抽籤結果、運勢分析
    if userMessage.find('抽籤：') == 0:

        # flexMessage 容器
        flex_message_contents = []

        # 整理文字、取得運勢分析
        userMessage = userMessage.replace('抽籤：', '')
        okamikuji_fortune = get_okamikuji_fortune( okamikuji_result["result_name"], userMessage )

        # 抽籤結果：將 pageTemplate 放入 flex_message_contents 中
        pageTemplate = random_okamikuji_first_page_template( okamikuji_result )
        flex_message_contents.append( pageTemplate )

        # 運勢分析結果：將 pageTemplate 放入 flex_message_contents 中
        pageTemplate = random_okamikuji_fortune_page_template( okamikuji_result, okamikuji_fortune, userMessage )
        flex_message_contents.append( pageTemplate )

        # 隨機產生下一句話
        sentence_1 = random_sentence()
        sentence_2 = random_sentence()
        sentence_3 = random_sentence()

        # 包裝訊息
        flex_message = FlexSendMessage(
            alt_text= '有人抽籤囉！',
            contents={
                "type": "carousel",
                "contents": flex_message_contents
            },
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton( action=MessageAction(label="● 再問一次", text= "抽籤：" + userMessage) ),
                    QuickReplyButton( action=MessageAction(label="● 再抽一次", text="抽籤") ),
                    QuickReplyButton( action=MessageAction(label="○ " + sentence_1, text='抽籤：'+ sentence_1) ),
                    QuickReplyButton( action=MessageAction(label="○ " + sentence_2, text='抽籤：'+ sentence_2) ),
                    QuickReplyButton( action=MessageAction(label="○ " + sentence_3, text='抽籤：'+ sentence_3) ),
                    QuickReplyButton( action=MessageAction(label="改塔羅牌 ➜", text='塔羅牌：'+ userMessage) ),
                    QuickReplyButton( action=MessageAction(label="改用擲筊 ➜", text='擲筊：'+ userMessage) ),
                ]
            )
        )
        
        # 發送訊息
        line_bot_api.reply_message(event.reply_token, flex_message)
        return

# 抽籤運勢分析
def get_okamikuji_fortune(result, userMessage):


    user_prompt = f"{result}：{userMessage}"
    system_prompt =  "模擬日本神社抽籤，請參考先前對話格式回覆，不要重複先前對話內容。"
    record_prompt = [
        {
            "user":"大吉：我的戀愛運勢",
            "model":"你的戀愛運勢極佳，各方面均將獲得成功和幸福，可能遇到命中注定的愛情，感情更會更穩固，享受這段美好時光！",
        },
        {
            "user":"凶：投資股市",
            "model":"投資股市方面可能會遇到挑戰和波動，建議謹慎行事，避免冒險，保持穩健的態度，做好風險控制和資金管理。",
        },
        {
            "user":"大凶：明天的考試",
            "model":"明天的考試可能會遇到困難和挑戰，建議你積極準備，保持冷靜，專注於考試內容，盡力而為。",
        },
        {
            "user":"末吉：下周的比賽",
            "model":"下周的比賽可能會有些許波折，但也會有一些幸運之處。請確保充分準備，保持冷靜和專注，並尋求幫助或建議以克服任何挑戰。",
        },  
        {
            "user":"吉：大樂透",
            "model":"吉兆預示著一些幸運和機會，儘管中獎並非必然，但你可能會遇到一些好運氣。但仍然要理智地玩，不要投入過多金錢。",
        },  
        {
            "user":"小吉：工作",
            "model":"工作上可能會遇到一些小挑戰，但也會有一些機會和好運。保持積極的態度，努力克服困難，並善用任何出現的機會。",
        },  
        {
            "user":"大吉：台積電",
            "model":"非常好的兆頭，未來台積電將會取得成功，股票價值可能會上升。如果你是投資者，這是一個好的時機持有或增加投資。",
        },  
        {
            "user":"凶：房地產",
            "model":"房地產方面可能會面臨挑戰和困難。可能出現市場波動或其他不利因素，導致投資或交易受阻。",
        },

    ]
    result_fortune = gemini_ai(user_prompt, system_prompt, record_prompt)

    return result_fortune


