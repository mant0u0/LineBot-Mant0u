# 扭蛋機 AI

from linebot import LineBotApi
from linebot.models import *

import os
from apps.common.common import *
from apps.ai.gemini import geminiPrompt
from apps.randomGashapon.main import *


line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))


def randomGashaponAi(event, userMessage):
    userMessage = userMessage.replace('扭蛋：', '')
    userMessage = userMessage.replace('扭蛋機：', '')
    
    Q_limit = "（最多產生8組文字）"
    userMessage = userMessage + Q_limit

    try:
        prompt = [
            {   
                "Q":"請問我晚餐要吃什麼？" + Q_limit, 
                "A":"義大利麵、蛋包飯、肉燥飯、火雞肉飯、炒飯"
            },
            {   
                "Q":"早餐" + Q_limit, 
                "A":"吐司、煎蛋、蛋餅、饅頭、燒餅、包子"
            },
            {   
                "Q":"讀書要讀哪一科" + Q_limit, 
                "A":"國文、英文、數學、化學、生物、地理、歷史、公民"
            },
            {   
                "Q":"出去玩" + Q_limit, 
                "A":"公園、爬山、博物館、美術館、圖書館、水族館、百貨公司"
            },
            {   
                "Q":"高雄哪裡玩" + Q_limit, 
                "A":"駁二、高雄巨蛋、蓮池潭、西子灣、美術館、新崛江、義大世界"
            },
            {   
                "Q":"穿什麼顏色" + Q_limit, 
                "A":"藍色、粉紅色、白色、黑色、黃色、紅色"
            },
            {   
                "Q":"幾點出門" + Q_limit, 
                "A":"早上6點、早上7點、早上8點、早上9點、早上10點"
            },
            {   
                "Q":"蛋餅" + Q_limit, 
                "A":"原味、火腿、肉鬆、蔬菜、起司、玉米、沙拉蛋、雞肉"
            },
            {   
                "Q":"吐司" + Q_limit, 
                "A":"草莓、香蕉、蜂蜜、巧克力、香草、紅豆、蔓越莓、蒜香"
            },
            {   
                "Q":"饅頭口味" + Q_limit, 
                "A":"白饅頭、鮮奶饅頭、黑糖饅頭、南瓜饅頭、抹茶饅頭"
            },
            {   
                "Q":"下列要哪一個：全罩式、半罩式、無罩式" + Q_limit,  
                "A":"全罩式、半罩式、無罩式"
            },
            {   
                "Q":"我要怎麼前往" + Q_limit,  
                "A":"走路、捷運、公車、火車、機車、開車"
            },
        ]
        return_text = geminiPrompt(userMessage, prompt)
        randomGashaponAddCheck(event, return_text)

    except:
        text_message = TextSendMessage(text= "扭蛋暫時無法產生，請稍後再嘗試～" ) # 印出結果
        line_bot_api.reply_message(event.reply_token, text_message)