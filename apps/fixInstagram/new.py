# 指令說明選單（主程式）
# https://github.com/Wikidepia/InstaFix?tab=readme-ov-file

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

# 爬蟲
import requests
from bs4 import BeautifulSoup

import os

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

# 主要
def instaNew(event, userMessage):

    # 整理網址
    igUrl = userMessage.split("?")[0]
    igUrl = igUrl.replace('https://www.instagram.com/', 'https://www.ddinstagram.com/')


    # 發送GET請求
    response = requests.get(igUrl)

    ig_data = {}

    # 檢查是否成功取得網頁內容
    if response.status_code == 200:
        # 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # 貼文作者
        og_title_meta = soup.find('meta', {'name': 'twitter:title'}).get('content')
        # print(og_title_meta)

        # 貼文文字
        og_description_meta = soup.find('meta', {'property': 'og:description'}).get('content')
        # print(og_description_meta)

        # 貼文連結
        og_url_meta = soup.find('meta', {'property': 'og:url'}).get('content')
        # print(og_description_meta)


        # 貼文影片
        og_video_meta = soup.find('meta', {'property': 'og:video'})
        # 檢查是否找到影片標籤
        if og_video_meta:
            # 取得 content 屬性的值
            og_video_content = "https://www.ddinstagram.com" + og_video_meta.get('content')
            
            # 將網頁轉址，將資料 GET 下來，取得影片連結
            try:
                og_video_response = requests.get(og_video_content)
                og_video_response.raise_for_status()
                og_video_content = og_video_response.url
                print(og_video_content)
            except requests.exceptions.RequestException as e:
                # print(f"錯誤：無法取得影片內容，原因：{e}")
                errorText = str(e)
                errorText = errorText[errorText.find("https://"):] 
                errorText = errorText.split(' ')[0]
                og_video_content = errorText
                print( og_video_content )

            og_userphoto_meta = "https://i.imgur.com/HotuY0I.png"


            ig_data = {
                "title": og_title_meta,
                "description" :og_description_meta,
                "type" : "video",
                "media-url" : og_video_content,
                "url" : og_url_meta,
                "userphoto" : og_userphoto_meta,
            }

        else:
            # 貼文圖片
            og_image_meta = soup.find('meta', {'property': 'og:image'}).get('content')
            og_image_meta = "https://www.ddinstagram.com" + og_image_meta
            og_image_meta = requests.get(og_image_meta).url
            # print(og_image_meta)

            og_userphoto_meta = "https://i.imgur.com/HotuY0I.png"


            ig_data = {
                "title": og_title_meta,
                "description" :og_description_meta,
                "type" : "image",
                "media-url" : og_image_meta,
                "url" : og_url_meta,
                "userphoto" : og_userphoto_meta,
            }

    else:
        print(f"錯誤：無法取得網頁內容，狀態碼：{response.status_code}")


    # 文字訊息
    igText = igTextPageTemplate(ig_data)
    flex_message_text_page = FlexSendMessage(
        alt_text= 'Instagram 推文擷取',
        contents={
            "type": "carousel",
            "contents": [igText]
            }
    )



    # 判斷網址為「圖片」
    if ig_data['type'] == 'image':

        # flexMessage 容器
        flex_message_contents = []

        # 取得第一張圖片比例
        imgRatio = "1:1"

        flex_message_contents.append( igImgPageTemplate( ig_data['media-url'],  imgRatio, "圖片") )

        # 包裝訊息
        flex_message = FlexSendMessage(
            alt_text= 'Instagram 圖片擷取',
            contents={
                "type": "carousel",
                "contents": flex_message_contents
                }
            )
        # 發送訊息
        line_bot_api.reply_message(event.reply_token, [flex_message, flex_message_text_page])


    # 判斷網址為「影片」
    elif ig_data['type'] == 'video':
        
        # 取得影片縮圖（爬一次原始網址）
        response = requests.get(ig_data['url'])
        if response.status_code == 200:
            # 使用BeautifulSoup解析HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            og_videoimg_meta = soup.find('meta', {'name': 'twitter:image'}).get('content')
        else:
            og_videoimg_meta = "https://i.imgur.com/aTKa7k7.png"

        # 整理網址：去除網址 ? 後面的部分
        videoUrl = ig_data['media-url']
        videoImg = og_videoimg_meta
        videoRatio = "1:1"





        # 包裝訊息：影片無法使用 carousel 輪播屬性的 flex message
        flex_message = FlexSendMessage(
            alt_text= 'Instagram 影片擷取',
            contents= igVideoPageTemplate( videoUrl, videoImg, videoRatio  ),
        )
        # 發送訊息
        line_bot_api.reply_message(event.reply_token, [flex_message, flex_message_text_page])




# 圖片頁面模板
def igImgPageTemplate( url, ratio, type ):

    pageTemplate = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                # 圖片
                {
                    "type": "image",
                    "url": url,
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
def igVideoPageTemplate( url, img, ratio ):

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
def igTextPageTemplate( ig_data ):

    # 推文資訊
    ig_author = {
        "type": "box",
        "layout": "horizontal",
        "contents": [
        {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "image",
                "url": ig_data["userphoto"],
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
                "text": ig_data['title'][1:],
                "weight": "bold",
                "color": "#333333",
                "offsetBottom": "2px"
            },
            {
                "type": "text",
                "text": ig_data['title'],
                "color": "#777777",
                "weight": "bold",
                "size": "xs"
            }
            ],
            "justifyContent": "center",
            "paddingStart": "12px"
        },
        # {
        #     "type": "image",
        #     "url": "https://i.imgur.com/3zeMGvy.png",
        #     "flex": 0,
        #     "size": "40px"
        # }
        ],
        "alignItems": "center"
    }

    # 推文內容
    ig_text = {
        "type": "box",
        "layout": "vertical",
        "contents": [
        {
            "type": "text",
            "text": ig_data['description'],
            "size": "xs",
            "color": "#777777",
            "wrap": True,
            "lineSpacing": "4px"
        }
        ],
        "paddingTop": "12px"
    }

    ig_contents = []
    ig_contents.append( ig_author )
    ig_contents.append( ig_text )

    # 頁面模板
    pageTemplate ={
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": ig_contents,
            "paddingAll": "16px"
        },
        "action": {
            "type": "uri",
            "label": "action",
            "uri": ig_data['url'],
        },
    }
    return pageTemplate