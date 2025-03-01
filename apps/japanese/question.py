# 日文問題
from linebot import LineBotApi
from linebot.models import *

import os
import random
import re
import requests

from apps.common.common import *
from apps.ai.gemini import gemini_ai

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))


# 日文問題
def japaneseQuestion(event, userMessage):
    userMessage = userMessage.replace('日文單字：', '')

    try:
        record_prompt = [
            {   
                "user":".世界", 
                "model":"世界|*せかい(sekai)|しんぶん(shinbun)|ほんやく(honyaku)|かんじ(kanji)"
            },
            {   
                "user":".環境", 
                "model":"環境|*かんきょう(kankyou)|かいぎ(kaigi)|てがみ(tegami)|こうじょう(koujou)"
            },
            {   
                "user":".發展", 
                "model":"発展|*はってん(hatten)|ほうほう(houhou)|はっけん(hakken)|ほうちょう(houchou)"
            },
            {   
                "user":".民主", 
                "model":"民主|*みんしゅ(minshu)|きょうわ(kyouwa)|しゅじん(shujin)|ぶんか(bunka)"
            },
            {   
                "user":".饅頭", 
                "model":"饅頭|*まんじゅう(manjuu)|たべもの(tabemono)|やさい(yasai)|くだもの(kudamono)"
            },
            {   
                "user":".下班", 
                "model":"退勤|*たいきん(taikin)|しゅうぎょう(shuugyou)|しごとしゅうりょう(shigoto shuuryou)|はってん(hatten)"
            },
            {   
                "user":".早餐", 
                "model":"朝食|*ちょうしょく(choushoku)|あさごはん(asagohan)|ひるごはん(hirugohan)|ゆうはん(yuuhan)"
            },
            {   
                "user":".蘿蔔", 
                "model":"大根|*だいこん(daikon)|にんじん(ninjin)|ごぼう(gobou)|かぶ(kabu)"
            },
            {   
                "user":".蔚藍檔案", 
                "model":"ブルーアーカイブ|*ブルーアーカイブ(buruu aakaibu)|レッドドキュメント(reddo dokyumento)|イエローファイル(iero fairu)|グリーンレジストリ(guriin rejisutori)"
            },
            {   
                "user":".電腦", 
                "model":"コンピューター|*コンピューター(konpyuutaa)|テレビ(terebi)|スマートフォン(sumaatofon)|タブレット(taburetto)"
            },
            {   
                "user":".鬧鐘", 
                "model":"目覚まし時計|*めざましどけい(mezamashi dokei)|とけい(tokei)|ばんどけい(bandokei)|すいどけい(suidokei)"
            }
        ]

        user_prompt = "."+userMessage
        system_prompt =  "請依照先前格式產生"
        return_text = gemini_ai(user_prompt, system_prompt, record_prompt)
        # print(return_text)

        # 文字分割：題目、答案選項、錯誤選項、錯誤選項、錯誤選項
        question_list = return_text.split("|")

        question_title = userMessage

        question_answer_kanji= question_list[0]
        question_answer_list = [
            question_list[1],
            question_list[2],
            question_list[3],
            question_list[4],
        ]
        # 選項洗牌
        random.shuffle(question_answer_list)

        # LINE 訊息包裝
        flex_message_contents = []
        pageTemplate_Contents = [
            # 主標題
            {
                "type": "text",
                "text": question_title,
                "weight": "bold",
                "wrap": True,
                "size": "lg",
                "color": "#0f6066",
                "align": "center"
            }, 
            # 副標題
            {
                "type": "text",
                "text": "請選擇正確的日文讀音",
                "weight": "bold",
                "size": "sm",
                "color": "#0f606699",
                "align": "center",
                "offsetTop": "4px",
            },
            # 分隔線
            {
                "type": "separator",
                "margin": "12px"
            }
        ]

        for item in question_answer_list:
            
            if item.find('*') >= 0:
                item = item.replace('*', '')
                options_text = item.replace('(', ' (')
                options_text = options_text.replace(')', ') ')
                question_result_text = f"日文單字解答：正確|{options_text}|{question_answer_kanji}"
            else:
                options_text = item.replace('(', ' (')
                options_text = options_text.replace(')', ') ')
                question_result_text = f"日文單字解答：錯誤|{options_text}|{options_text}"

            # 去除羅馬音標
            options_text = re.sub(r'\([^)]*\)', '', item)


            # 按鈕
            btnItem = {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "text",
                    "text": options_text,
                    "weight": "bold",
                    "color": "#0f6066",
                    "wrap": True,
                },
                ],
                "action": {

                    "type": "postback",
                    "label": "action",
                    "data": question_result_text,

                    # "type": "message",
                    # "label": "action",
                    # "text": question_result_text,
                },
                "paddingAll": "12px",
                "justifyContent": "center",
                "alignItems": "center",
            }
            pageTemplate_Contents.append(btnItem)
            
            # 分隔線
            pageTemplate_Contents.append({"type": "separator"})
        
        # 去除最後一個元素(分隔線)
        pageTemplate_Contents = pageTemplate_Contents[:-1]

        # 頁面 (pageTemplate)
        pageTemplate = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    # 橫幅 banner
                    {
                        "type": "image",
                        "url": localImg("banner/japanese.png"),
                        "size": "100%",
                        "aspectMode": "fit",
                        "margin": "0px",
                        "position": "relative",
                        "aspectRatio": "1000:280"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": pageTemplate_Contents,
                        "paddingAll": "12px"
                    }
                ],
                "paddingAll": "0px"
            }
        }
        flex_message_contents.append(pageTemplate)

        # Flex 訊息
        replyLineMessage = FlexSendMessage(
            alt_text= "日文問題！",
            contents={
                "type": "carousel",
                "contents": flex_message_contents,
            }
        )
        
        # 回傳訊息
        line_bot_api.reply_message(event.reply_token, replyLineMessage)
    
    except:
        text_message = TextSendMessage(text= "題目暫時無法產生，請稍後再嘗試～" ) # 印出結果
        line_bot_api.reply_message(event.reply_token, text_message)


# 日文解答
def japaneseAnswer(event, userMessage):
    userMessage = userMessage.replace('日文單字解答：', '')

    # 取得使用者名稱
    userId, userName = getUserName(event)

    info_list = userMessage.split("|")
    if info_list[0] == "正確":
        img_url = localImg("OO.png")
        
        if info_list[1].find(info_list[2]) == 0:
            ans_text = info_list[1]
        else:
            ans_text = info_list[2]+"、"+info_list[1]

        ans_contents = [
            {
                "type": "text",
                "text": ans_text,
                "weight": "bold",
                "size": "sm",
                "wrap": False,
                "offsetBottom": "1px"
            },
            {
                "type": "text",
                "text": userName + " 答對了！",
                "wrap": True,
                "color": "#8c8c8c",
                "size": "xs",
                "offsetTop": "1px"
            }
        ]

    else:
        img_url = localImg("XX.png")
        ans_text = info_list[1]
        ans_contents = [
            {
                "type": "text",
                "text": ans_text,
                "weight": "bold",
                "size": "sm",
                "wrap": True,
                "offsetBottom": "1px"
            },
            {
                "type": "text",
                "text": userName + " 答錯了！",
                "wrap": True,
                "color": "#8c8c8c",
                "size": "xs",
                "offsetTop": "1px"
            }
        ]

    # 去除羅馬音標、取得聲音訊息
    audio_text = re.sub(r'\([^)]*\)', '', info_list[1])
    audio_url = generate_sound_url(audio_text)
    audio_message = AudioSendMessage(original_content_url=audio_url , duration=2000)

    contentsList = []
    contentsItem = {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "image",
                    "url": img_url,
                    "size": "xxs",
                    "flex": 1,
                    "offsetEnd": "5px"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": ans_contents,
                    "flex": 4
                }
            ],
            "justifyContent": "center",
            "alignItems": "center",
            "paddingAll": "16px",
            "paddingEnd": "20px",
            "action": {
                "type": "message",
                "label": "action",
                "text": ans_text,
            },
            
        },
    }
    contentsList.append(contentsItem)

    # 包裝訊息
    replyLineMessage = FlexSendMessage(
        alt_text='解答！',
        contents={
            "type": "carousel",
            "contents": contentsList,
        }
    )

    if info_list[0] == "正確":
        # 回傳訊息
        line_bot_api.reply_message(event.reply_token, [replyLineMessage, audio_message])
        # line_bot_api.reply_message(event.reply_token, [replyLineMessage])
    else:
        # 回傳訊息
        line_bot_api.reply_message(event.reply_token, [replyLineMessage])


# 取得使用者名稱，如果沒有加好友，預設為「玩家」
def getUserName(event):
    userId = event.source.user_id
    try:
        profile = line_bot_api.get_profile(userId)
        profile = json.loads(str(profile))  # 字串轉字典型態
        userName = str(profile['displayName'])
    except:
        userName = '有人'

    return userId, userName


# 文字轉語音
def generate_sound_url(user_message, language='ja-JP', engine='Google'):
    def get_sound(sound_id):
        response = requests.get(f'https://api.soundoftext.com/sounds/{sound_id}')
        sound_status = response.json()

        if sound_status['status'] == 'Pending':
            print('Sleeping...')
            time.sleep(2)
            return get_sound(sound_id)

        return sound_status['location']

    data = {'engine': engine, 'data': {'voice': language, 'text': user_message}}

    response = requests.post(
        'https://api.soundoftext.com/sounds',
        headers={'Content-Type': 'application/json'},
        json=data
    )
    sound_request = response.json()
    sound_url = get_sound(sound_request['id'])

    return sound_url


