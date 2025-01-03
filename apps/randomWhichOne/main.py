from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

import os
import random

from apps.common.common import *

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

# 主要
def random_which_one_main(event, userMessage):

    userMessage = userMessage.replace('哪個：', '')
    userMessage = userMessage.replace('都幾：', '')

    splitList = ['、', '，', '；', ',', '.']

    for item in splitList:
        userMessage = userMessage.replace(item, '、')

    if '、' in userMessage:
        split_result = [s.strip() for s in userMessage.split('、')]
    else:
        split_result = userMessage.split()

    # 當有兩個選項時，啟動迷因按鈕
    if len(split_result) == 2:
        random_which_one_meme_button(event, split_result, userMessage)
    
    else:
        result = str(random.choice(split_result))

        # 包裝訊息
        text_message = TextSendMessage(
            text = result,
            quick_reply = QuickReply(
                items = [
                    QuickReplyButton(
                        action = MessageAction(
                            label = "再問一次", text = "哪個：" + userMessage)
                    ),
                ]
            )
        )
        # 發送訊息
        line_bot_api.reply_message(event.reply_token, text_message)


# 迷因按鈕
def random_which_one_meme_button(event, split_result, userMessage):
    
    result = str(random.choice(split_result))
    before_text_list = ["我覺得是","問就是","感覺是","就選","這個！","隨便啦～", "All in","一律都選"]
    before_text = str(random.choice(before_text_list))
    result_text = f"{before_text} {result}！"
    
    if result == split_result[0]:
        imgUrl = "randomWhichOne/1.png"
    elif result == split_result[1]:
        imgUrl = "randomWhichOne/2.png"

    # 字體大小
    if len(split_result[0]) > 5:
        text_size_1 = "md"
    else:
        text_size_1 = "lg"
    if len(split_result[1]) > 5:
        text_size_2 = "md"
    else:
        text_size_2 = "lg"



    random_event = random.randint(0, 100) 
    if random_event <= 10:
        imgUrl = "randomWhichOne/display.png"
        result_text_list = ["我都不要阿","為什麼要幫你選？","我不知道耶，看你啊"]
        result_text = str(random.choice(result_text_list))
    if random_event >= 90:
        imgUrl = "randomWhichOne/all.png"
        result_text_list = ["我全都要！","小孩子才做選擇！","都可～","隨便～","都可以啊～"]
        result_text = str(random.choice(result_text_list))



    # 包裝訊息
    flex_message = FlexSendMessage(
        alt_text = result,
        contents = {
            "type": "carousel",
            "contents": [
                {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "paddingAll": "0px",
                    "contents": [
                    # 背景圖片
                    {
                        "type": "image",
                        "url": localImg(imgUrl),
                        "aspectRatio": "1:1",
                        "size": "full"
                    },

                    # 結果文字
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "text",
                            "text": result_text,
                            "size": "lg",
                            "color": "#063977",
                            "weight": "bold"
                        }
                        ],
                        "borderWidth": "1px",
                        "position": "absolute",
                        "offsetBottom": "0px",
                        "paddingAll": "20px",
                        "width": "100%",
                        "height": "24%",
                        "justifyContent": "center",
                        "alignItems": "center"
                    },

                    # 左按鈕文字
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "text",
                            "text": split_result[0],
                            "align": "center",
                            "maxLines": 2,
                            "wrap": True,
                            "weight": "bold",
                            "color": "#063977",
                            "size": text_size_1
                        }
                        ],
                        "position": "absolute",
                        "width": "35%",
                        "offsetTop": "13%",
                        "offsetStart": "10%",
                        "height": "52px",
                        "alignItems": "center",
                        "justifyContent": "center"
                    },

                    # 右按鈕文字
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "text",
                            "text": split_result[1],
                            "align": "center",
                            "maxLines": 2,
                            "wrap": True,
                            "weight": "bold",
                            "color": "#063977",
                            "size": text_size_2
                        }
                        ],
                        "position": "absolute",
                        "width": "35%",
                        "offsetTop": "13%",
                        "height": "52px",
                        "alignItems": "center",
                        "justifyContent": "center",
                        "offsetEnd": "10%"
                    }

                    ],

                }
                }
            ]
        },
        quick_reply=QuickReply(
            items=[
                QuickReplyButton(
                    action = MessageAction(
                        label = "再問一次", text = "哪個：" + userMessage)
                ),
            ]
        )
    )
    # 發送訊息
    line_bot_api.reply_message(event.reply_token, flex_message)

