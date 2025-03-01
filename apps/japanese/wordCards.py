# 日文單字範例
from linebot import LineBotApi
from linebot.models import *

import os
import random
import re
import requests
from urllib.parse import quote

from apps.common.common import *
from apps.ai.gemini import  gemini_ai

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))

# 日文單字卡
def japaneseWordCards(event):

    # 讀取內容 (JSON 檔案)
    filePath = 'apps/japanese/textJson/N5.json'
    with open(filePath, 'r') as file:
        jpwords_content = json.load(file)

    # 隨機取一個日文單字
    random_jpwords = random.choice(jpwords_content)
    # random_jpwords = {
    #     "Kana" : "あいます",
    #     "Kanji" : "会います",
    #     "Phonetic" : "{{会,あ}}います",
    #     "Chinese" : "見面"
    # }
    
    # 整理中文解釋
    if isinstance(random_jpwords["Chinese"], str):
        jpwords_chinese = random_jpwords["Chinese"]
    elif isinstance(random_jpwords["Chinese"], list):
        temp = ""
        for t in random_jpwords["Chinese"]:
            temp = temp + t + "\n"
        temp = temp.rstrip("\n")
        jpwords_chinese = temp
    else:
        jpwords_chinese = str(random_jpwords["Chinese"])

    # 產生日文例句
    jpwords_example_sentences = get_jpwords_example_sentences( random_jpwords["Kanji"] +"。"+ jpwords_chinese )
    
    # 產生日文例句文字排版
    jpwords_example_sentences_template = get_jpwords_example_sentences_template("#0f6066", jpwords_example_sentences)

    # 產生日文單字文字排版
    jpwords_template = get_jpwords_template(random_jpwords)

    # 包裝訊息
    flex_message = FlexSendMessage(
        alt_text= f'日文單字：{random_jpwords["Kanji"]}',
        contents={
            # JSON 格式貼這邊
            "type": "carousel",
            "contents": [
                {
                    "type": "bubble",
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "paddingAll": "0px",
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

                            # 語音按鈕
                            {
                                "type": "image",
                                "url": localImg("sound-btn.png"),
                                "size": "20px",
                                "aspectRatio": "1:1",
                                "aspectMode": "fit",
                                "position": "absolute",
                                "offsetEnd": "16px",
                                "offsetTop": "90px",
                                "action": {
                                    "type": "message",
                                    "text": f"日文語音：{random_jpwords['Kanji']}（{random_jpwords['Kana']}）"
                                },
                            },

                            # 單字類型
                            {
                                "type": "box",
                                "layout": "vertical",
                                "position": "absolute",
                                "width": "100%",
                                "height": "100%",
                                "paddingAll": "12px",
                                "justifyContent": "flex-start",
                                "alignItems": "flex-start",
                                "contents": [
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                        {
                                            "type": "text",
                                            "text": "N5 日文單字",
                                            "size": "xxs",
                                            "weight": "bold",
                                            "color": "#ffffff"
                                        }
                                        ],
                                        "backgroundColor": "#00000099",
                                        "paddingAll": "4px",
                                        "width": "84px",
                                        "cornerRadius": "4px",
                                        "alignItems": "center"
                                    }
                                ],

                            },

                            # 日文單字
                            {
                                "type": "box",
                                "layout": "vertical",
                                "paddingTop": "4px",
                                "paddingStart": "16px",
                                "paddingEnd": "16px",
                                "contents": [
                                    jpwords_template
                                    # row_text,
                                    # row_text,
                                ],
                            },

                            # 中文解釋
                            {
                                "type": "box",
                                "layout": "vertical",
                                "paddingAll": "16px",
                                "paddingTop": "12px",
                                "paddingBottom": "20px",
                                "contents": [
                                    {
                                        "type": "text",
                                        "weight": "bold",
                                        "wrap": True,
                                        "size": "md",
                                        "lineSpacing": "4px",
                                        "color": "#0f606699",
                                        "align": "center",
                                        "text": jpwords_chinese,
                                    },

                                    # 例句標題
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "paddingTop": "12px",
                                        # "paddingBottom": "6px",
                                        "contents": [
                                            {
                                                "type": "text",
                                                "weight": "bold",
                                                "wrap": True,
                                                "size": "md",
                                                "lineSpacing": "4px",
                                                "color": "#0f6066",
                                                "text": "【例句】",
                                            },
                                        ],
                                    },

                                    # 例句 + 語音按鈕
                                    {
                                        "type": "box",
                                        "layout": "horizontal",
                                        "alignItems": "center",
                                        "contents": [
                                            # 例句
                                            {
                                                "type": "box",
                                                "layout": "vertical",
                                                "contents": [jpwords_example_sentences_template],
                                            },
                                            # 語音按鈕
                                            {
                                                "type": "image",
                                                "url": localImg("sound-btn.png"),
                                                "size": "20px",
                                                "aspectRatio": "1:1",
                                                "aspectMode": "fit",
                                                "flex": 0,
                                                "margin": "8px",
                                            }
                                        ],
                                        "action": {
                                            "type": "message",
                                            "text": "日文語音：" + jpwords_example_sentences.split('\n')[0].replace('{{', '').replace('}}', '')
                                        }
                                    }
                                ],
                            },
                        ],
                        "justifyContent": "center"
                    }
                }
            
            ]
        },
        quick_reply=QuickReply(
            items=[
                QuickReplyButton(
                    action=MessageAction(label = "其他單字", text = "日文單字")
                ),
            ]
        )
    )




    
    # 發送訊息
    line_bot_api.reply_message(event.reply_token, flex_message)

# 分割日文單字
def get_jpwords_split(text_phonetic):

    # 定義要拆解的字串
    # text_phonetic = "{{歩,ある}}いてきます"
    # 輸出結果 = [['歩', 'ある',1], ['いてきます', '',2]] (第三項為第一字元序列)

    # 定義正則表達式模式
    pattern = r'(\{\{.*?\}\}|[^\{\}]+)'

    # 使用 findall 函數找出所有匹配項目
    matches = re.findall(pattern, text_phonetic)

    # 解析匹配項目
    parsed_items = []
    for match in matches:
        if match.startswith('{{') and match.endswith('}}'):
            # 如果是形如{{...}}的字串，去除大括號後分隔逗號
            inner_items = match[2:-2].split(',')
            parsed_items.append(inner_items)
        else:
            # 否則將字串分成兩個部分
            for char in match:
                parsed_items.append([char, ''])
    
    # 整理解析結果
    final_result = []
    temp_text = ""
    text_index_count = 0
    for item in parsed_items:
        if item[1] == '':
            # item[1] 沒有假名時，item[0] 與前一個合併
            temp_text += item[0]
            # 計數
            text_index_count = text_index_count + 1
        else:
            # item[1] 有假名時，先將沒有假名的暫存放入結果中後，再將有將有假名的結果放入，最後清空暫存。
            if temp_text != "":
                # temp 元素一個字元位置
                first_char_index = text_index_count - len(temp_text) + 1
                # 新增
                final_result.append([temp_text, "", first_char_index])
            
            # 計數
            text_index_count = text_index_count + len(item[0])
            # 元素一個字元位置
            first_char_index = text_index_count - len(item[0]) + 1
            # 新增
            final_result.append([item[0],item[1], first_char_index])
            temp_text = ""

    # 將最後的 temp_text 加入 final_result
    if temp_text:
        # 計數
        text_index_count = text_index_count + 1
        # temp 元素一個字元位置
        first_char_index = text_index_count - len(temp_text)
        # 新增
        final_result.append([temp_text, "",first_char_index])

    # print(final_result)
    return final_result

# 日文例句
def get_jpwords_example_sentences(text):

    try:
        record_prompt = [
            {   
                "user":"入り口。入口", 
                "model":"この建物の{{入り口}}はどこですか？\n這棟建築物的{{入口}}在哪裡？"
            },
            {   
                "user":"医者。醫生", 
                "model":"この町には優秀な{{医者}}がたくさんいます。\n這個城鎮有很多優秀的{{醫生}}。"
            },
            {   
                "user":"今から。現在；現在開始", 
                "model":"{{今から}}日本語を勉強します。\n{{從現在開始}}學習日語。"
            },
            {   
                "user":"今から。現在；現在開始", 
                "model":"{{今から}}映画を見に行きます。\n{{現在}}要去看電影。"
            },
            {   
                "user":"インターネット（を）します。上網", 
                "model":"今から{{インターネットをします}}。大切なメールを確認しなければなりません。\n我現在要{{上網}}了。我必須檢查重要的郵件。"
            },
            {   
                "user":"気持ちがいい。舒服，心理上生理上舒暢", 
                "model":"この椅子はとても{{気持ちがいい}}です。這張椅子坐起來非常{{舒服}}。"
            },
            {   
                "user":"幾つ。[① 幾歲，多大, ②（數量）多少個]", 
                "model":"{{幾つ}}になりましたか？\n你{{幾歲}}了？"
            },
            {   
                "user":"幾つ。[① 幾歲，多大, ②（數量）多少個]", 
                "model":"この箱には{{幾つ}}のリンゴが入っていますか？\n這個箱子裡有{{多少個}}蘋果？"
            },
            {   
                "user":"ご主人。尊夫，您的先生：提及別人的先生時用「ご主人」", 
                "model":"私の{{ご主人}}はとても忙しいです。\n我的{{先生}}非常忙。"
            },
        ]

        system_prompt = "根據日文單字，產生日文例句，並將該日文單字用{{}}包起來。"
        user_prompt = text


        return_text = gemini_ai(user_prompt, system_prompt ,record_prompt)

    except:
        return_text = " - "

    return return_text

# 日文例句文字排版
def get_jpwords_example_sentences_template(color, text):
    segments = re.split(r'({{.*?}})', text)
    contents = []

    for segment in segments:
        if segment.startswith('{{') and segment.endswith('}}'):
            contents.append({
                "type": "span",
                "text": segment[2:-2],
                "color": "#ff6953",
                # "decoration": "underline"
            })
        else:
            segment = segment.strip()
            if segment:  # 去除空字符串
                contents.append({
                    "type": "span",
                    "text": segment
                })
    item = {
        "type": "text",
        "contents": contents,
        "margin": "8px",
        "size": "sm",
        "wrap": True,
        "weight": "bold",
        "lineSpacing": "4px",
        "color": color+"99",
    }
    return item

# 日文單字文字排版
def get_jpwords_template(jpwords):

    # 一行文字數量上限
    # row_max_text = 10
    # if len(jpwords["Kanji"]) > row_max_text:
    #     print("x")

    # 分割字串
    jpwords_split = get_jpwords_split(jpwords["Phonetic"])
    # jpwords_split = [
    #     ["お",""],
    #     ["客","きゃく"],
    #     ["さん",""],
    # ]


    row_text_contents = []
    
    # 日文平假名與片假名排版
    for text_list in jpwords_split:
        word_contents = []
        if text_list[1] != "":
            # 有注音
            word_contents = [
                {
                    "type": "text",
                    "text": text_list[1],
                    "size": "xxs",
                    "weight": "bold",
                    "align": "center",
                    "color": "#0f606699",
                },
                {
                    "type": "text",
                    "text": text_list[0],
                    "size": "xxl",
                    "weight": "bold",
                    "align": "center",
                    "color": "#0f6066",
                }
            ]
        else:
            # 無注音
            word_contents = [
                {
                    "type": "text",
                    "text": text_list[0],
                    "size": "xxl",
                    "weight": "bold",
                    "align": "center",
                    "color": "#0f6066",
                }

            ]
        word = {
            "type": "box",
            "layout": "vertical",
            "justifyContent": "flex-end",
            "flex": 0,
            "contents": word_contents,
        }
        row_text_contents.append(word)


    jpwords_contents = []


    # 一行文字
    row_text = {
        "type": "box",
        "layout": "horizontal",
        "justifyContent": "center",
        "margin": "4px",
        "contents": row_text_contents,
        "action": {
            "type": "message",
            "text": f"日文語音：{jpwords['Kanji']}（{jpwords['Kana']}）"
        }
    }

    return row_text


# 日文語音
def japaneseVoice(event, userMessage):
    userMessage = userMessage.replace('日文語音：', '')

    def get_sound(sound_id):
        response = requests.get(f'https://api.soundoftext.com/sounds/{sound_id}')
        sound_status = response.json()

        if sound_status['status'] == 'Pending':
            print('Sleeping...')
            time.sleep(2)
            return get_sound(sound_id)

        return sound_status['location']

    data = {'engine': 'Google', 'data': {'voice': 'ja-JP', 'text': userMessage}}

    response = requests.post(
        'https://api.soundoftext.com/sounds',
        headers={'Content-Type': 'application/json'},
        json=data
    )
    sound_request = response.json()
    sound_url = get_sound(sound_request['id'])

    # 回傳聲音訊息
    audio_message = AudioSendMessage(original_content_url=sound_url , duration=2000)
    line_bot_api.reply_message(event.reply_token, [audio_message])

    return