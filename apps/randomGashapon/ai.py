# 扭蛋機 AI

from linebot import LineBotApi
from linebot.models import *

import os
from apps.common.common import *
from apps.ai.gemini import  gemini_ai
from apps.randomGashapon.main import *


line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))


def randomGashaponAi(event, userMessage):
    userMessage = userMessage.replace('扭蛋：', '')
    userMessage = userMessage.replace('扭蛋機：', '')
    
    Q_limit = "（最多產生8組文字）"
    userMessage = userMessage + Q_limit

    try:
        record_prompt = [
            {   
                "user":"請問我晚餐要吃什麼？" + Q_limit, 
                "model":"義大利麵、蛋包飯、肉燥飯、火雞肉飯、炒飯"
            },
            {   
                "user":"早餐" + Q_limit, 
                "model":"吐司、煎蛋、蛋餅、饅頭、燒餅、包子"
            },
            {   
                "user":"讀書要讀哪一科" + Q_limit, 
                "model":"國文、英文、數學、化學、生物、地理、歷史、公民"
            },
            {   
                "user":"出去玩" + Q_limit, 
                "model":"公園、爬山、博物館、美術館、圖書館、水族館、百貨公司"
            },
            {   
                "user":"高雄哪裡玩" + Q_limit, 
                "model":"駁二、高雄巨蛋、蓮池潭、西子灣、美術館、新崛江、義大世界"
            },
            {   
                "user":"穿什麼顏色" + Q_limit, 
                "model":"藍色、粉紅色、白色、黑色、黃色、紅色"
            },
            {   
                "user":"幾點出門" + Q_limit, 
                "model":"早上6點、早上7點、早上8點、早上9點、早上10點"
            },
            {   
                "user":"蛋餅" + Q_limit, 
                "model":"原味、火腿、肉鬆、蔬菜、起司、玉米、沙拉蛋、雞肉"
            },
            {   
                "user":"吐司" + Q_limit, 
                "model":"草莓、香蕉、蜂蜜、巧克力、香草、紅豆、蔓越莓、蒜香"
            },
            {   
                "user":"饅頭口味" + Q_limit, 
                "model":"白饅頭、鮮奶饅頭、黑糖饅頭、南瓜饅頭、抹茶饅頭"
            },
            {   
                "user":"下列要哪一個：全罩式、半罩式、無罩式" + Q_limit,  
                "model":"全罩式、半罩式、無罩式"
            },
            {   
                "user":"我要怎麼前往" + Q_limit,  
                "model":"走路、捷運、公車、火車、機車、開車"
            },
        ]
        user_prompt = userMessage
        system_prompt = "產生相關字詞單字，請依照先前格式產生，最多產生8組文字"
        return_text = gemini_ai(user_prompt, system_prompt, record_prompt)
        randomGashaponAddCheck(event, return_text)

    except:
        text_message = TextSendMessage(text= "扭蛋暫時無法產生，請稍後再嘗試～" ) # 印出結果
        line_bot_api.reply_message(event.reply_token, text_message)