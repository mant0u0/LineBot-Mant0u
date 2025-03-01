# 指令說明選單（主程式）
# https://docs.fxtwitter.com/en/latest/api/status.html

from linebot import LineBotApi
from linebot.models import *

# 爬蟲
import requests

import googletrans

import os
from apps.ai.main import aiTranslateChinese
from apps.common.common import *

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
mant0u_bot_model = os.getenv("MANT0U_BOT_MODEL")

# 主要
def twitterNew(event, userMessage):

    # 整理網址：去除網址 ? 與 /photo/ 後面的部分、x 改 twitter
    twitterUrl = userMessage.split("?")[0]
    twitterUrl = userMessage.split("/photo/")[0]
    twitterUrl = twitterUrl.replace('https://x.com/', 'https://twitter.com/')
    twitterUrl = twitterUrl.replace('https://fxtwitter.com/', 'https://twitter.com/')
    twitterUrl = twitterUrl.replace('https://vxtwitter.com/', 'https://twitter.com/')

    # 將網址改為 https://d.fxtwitter.com/
    fxTwitterUrl = twitterUrl.replace( 'https://twitter.com/', 'https://api.fxtwitter.com/')

    # 發送 GET 請求
    response = requests.get(fxTwitterUrl)

    # 解析 JSON 格式的回應
    tweet_data = response.json()

    # 文字訊息
    twitterText = twitterTextPageTemplate(tweet_data, "原文")

    # 翻譯文字訊息
    tweet_text_original = tweet_data['tweet']['text']
    translator = googletrans.Translator()
    tweet_text_translate  = translator.translate(tweet_text_original, dest="zh-tw").text
    
    # 判斷推文翻譯
    if tweet_text_original != tweet_text_translate:
        
        tweet_data['tweet']['text'] = tweet_text_translate
        translation_status = "Google 翻譯"

        # if mant0u_bot_model == "private":
        #     try:
        #         tweet_data['tweet']['text'] = aiTranslateChinese(tweet_text_original)
        #         translation_status = "Gemini AI 翻譯"
        #         if tweet_data['tweet']['text'] == "" or tweet_data['tweet']['text'] == " ":
        #             tweet_data['tweet']['text'] = tweet_text_translate
        #             translation_status = "Google 翻譯"
        #     except:
        #         tweet_data['tweet']['text'] = tweet_text_translate
        #         translation_status = "Google 翻譯"
        # else:
        #     tweet_data['tweet']['text'] = tweet_text_translate
        #     translation_status = "Google 翻譯"

        twitterTextTW = twitterTextPageTemplate(tweet_data, translation_status)

        # 取得推文訊息
        # 包裝訊息
        flex_message_text_page = FlexSendMessage(
            alt_text= 'Twitter 推文擷取',
            contents={
                "type": "carousel",
                "contents": [twitterText, twitterTextTW]
                }
            )
    else:
        # 取得推文訊息
        # 包裝訊息
        flex_message_text_page = FlexSendMessage(
            alt_text= 'Twitter 推文擷取',
            contents={
                "type": "carousel",
                "contents": [twitterText]
                }
            )

    # 判斷推文是否有圖片與影片
    media_info = tweet_data['tweet'].get('media', None)
    if media_info is None:
        # 文字推文
        # 發送訊息
        line_bot_api.reply_message(event.reply_token, flex_message_text_page)
    
    else:
        # 媒體推文
        # 顯示或使用取得的資料
        tweet_data_list = tweet_data['tweet']['media']['all']

        # 判斷網址為「圖片」
        if tweet_data_list[0]['type'] == 'photo':

            # flexMessage 容器
            flex_message_contents = []

            # 取得第一張圖片比例
            imgRatio = str(tweet_data_list[0]['width']) + ":" + str(tweet_data_list[0]['height']) 

            # 將圖片代入模板，並放入 flex_message_contents 中
            for i in tweet_data_list:
                if i['type'] ==  'photo':
                    url = i['url']
                    imgUrl = i['url']
                    imgType = "圖片"
                else:
                    url = i['url']
                    imgUrl = i['thumbnail_url']
                    imgType = "影片"
                flex_message_contents.append( twitterImgPageTemplate( url, imgUrl,  imgRatio, imgType) )

            # 包裝訊息
            flex_message = FlexSendMessage(
                alt_text= 'Twitter 圖片擷取',
                contents={
                    "type": "carousel",
                    "contents": flex_message_contents
                    }
                )
            # 發送訊息
            line_bot_api.reply_message(event.reply_token, [flex_message, flex_message_text_page])


        # 判斷網址為「影片」
        elif tweet_data_list[0]['type'] == 'video' or tweet_data_list[0]['type'] == 'gif':
            
            # 整理網址：去除網址 ? 後面的部分
            videoUrl = tweet_data_list[0]['url'].split("?")[0]
            videoImg = tweet_data_list[0]['thumbnail_url']
            videoRatio = str(tweet_data_list[0]['width']) + ":" + str(tweet_data_list[0]['height']) 

            # 包裝訊息：影片無法使用 carousel 輪播屬性的 flex message
            flex_message = FlexSendMessage(
                alt_text= 'Twitter 影片擷取',
                contents= twitterVideoPageTemplate( videoUrl, videoImg, videoRatio  ),
            )
            # 發送訊息
            line_bot_api.reply_message(event.reply_token, [flex_message, flex_message_text_page])


# 圖片頁面模板
def twitterImgPageTemplate( url, imgUrl, ratio, type ):

    pageTemplate = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                # 圖片
                {
                    "type": "image",
                    "url": imgUrl,
                    "size": "full",
                    "aspectRatio": ratio,
                    "gravity": "top",
                    "aspectMode": "cover"
                },
                # 媒體類型
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "text",
                            "text": type,
                            "size": "xxs",
                            "weight": "bold",
                            "color": "#ffffff"
                        }
                        ],
                        "backgroundColor": "#00000099",
                        "paddingAll": "4px",
                        "width": "32px",
                        "cornerRadius": "4px",
                        "alignItems": "center"
                    }
                    ],
                    "position": "absolute",
                    "width": "100%",
                    "height": "100%",
                    "paddingAll": "12px",
                    "justifyContent": "flex-end",
                    "alignItems": "flex-end"
                },


            ],
            "paddingAll": "0px"
        },
        "action": {
            "type": "uri",
            "label": "action",
            "uri": url
        },
    }

    return pageTemplate

# 影片頁面模板
def twitterVideoPageTemplate( url, img, ratio ):

    pageTemplate = {
        "type": "bubble",
        "hero": {
                "type": "video",
                "url": url,
                "previewUrl": img,
                "aspectRatio": ratio,
                "action": {
                    "type": "uri",
                    "label": "瀏覽器觀看",
                        "uri": url
                },
            "altContent": {
                    "type": "image",
                    "size": "full",
                    "aspectRatio": ratio,
                    "aspectMode": "cover",
                    "url": img
                }
        },
        "styles": {
            "hero": {
                "backgroundColor": "#000000"
            }
        },
    }

    return pageTemplate


# 文字頁面模板
def twitterTextPageTemplate( tweet_data, translation_status ):

    tweet_contents = []

    # 推文資訊
    tweet_author = {
        "type": "box",
        "layout": "horizontal",
        "contents": [
        {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "image",
                "url": tweet_data['tweet']['author']['avatar_url'],
                "align": "center",
                "gravity": "center",
                "size": "48px",
            }
            ],
            "alignItems": "center",
            "cornerRadius": "24px",
            "width": "48px",
            "height": "48px",
            "backgroundColor": "#f4f6f9"
        },
        {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": tweet_data['tweet']['author']['name'],
                "weight": "bold",
                "color": "#333333",
                "offsetBottom": "2px"
            },
            {
                "type": "text",
                "text": "@"+tweet_data['tweet']['author']['screen_name'],
                "color": "#777777",
                "weight": "bold",
                "size": "xs"
            }
            ],
            "justifyContent": "center",
            "paddingStart": "12px"
        },
        {
            "type": "image",
            "url": "https://i.imgur.com/3zeMGvy.png",
            "flex": 0,
            "size": "40px"
        }
        ],
        "alignItems": "center"
    }
    # 推文內容
    tweet_text = {
        "type": "box",
        "layout": "vertical",
        "paddingTop": "12px",
        "contents": [
            {
                "type": "text",
                "text": tweet_data['tweet']['text'],
                "size": "xs",
                "color": "#777777",
                "wrap": True,
                "lineSpacing": "4px"
            }
        ],
    }
    # 翻譯標籤
    tag_width = get_char_width_ratio(translation_status) * 8.5
    translation_tag = {
        "type": "box",
        "layout": "vertical",
        "cornerRadius": "20px",
        "backgroundColor": "#cce9ff",
        "flex": 0,
        "width": str(tag_width) + "px",
        "justifyContent": "center",
        "alignItems": "center",
        "paddingAll": "4px",
        "margin": "8px",
        "contents": [
                {
                "type": "text",
                "text": translation_status,
                "color": "#02497d",
                "align": "center",
                "size": "xs",
                "weight": "bold"
                }
            ],
        }
        
    tweet_contents.append( tweet_author )
    if tweet_data['tweet']['text'] != '':
        tweet_contents.append( tweet_text )

    if translation_status != "原文":
        tweet_contents.append( translation_tag )

    # 頁面模板
    pageTemplate ={
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": tweet_contents,
            "paddingAll": "16px"
        },
        "action": {
            "type": "uri",
            "label": "action",
            "uri": tweet_data['tweet']['url']
        },
    }
    return pageTemplate