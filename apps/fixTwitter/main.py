# 指令說明選單（主程式）

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

# 爬蟲
import requests

# 讀取圖片連結尺寸用
from PIL import Image
from io import BytesIO

import os

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

# 主要
def twitterMain(event, userMessage):

    # 整理網址：去除網址 ? 與 /photo/ 後面的部分、x 改 twitter
    twitterUrl = userMessage.split("?")[0]
    twitterUrl = userMessage.split("/photo/")[0]
    twitterUrl = twitterUrl.replace('https://x.com/', 'https://twitter.com/')
    twitterUrl = twitterUrl.replace('https://fxtwitter.com/', 'https://twitter.com/')
    twitterUrl = twitterUrl.replace('https://vxtwitter.com/', 'https://twitter.com/')

    # 將網址改為 https://d.fxtwitter.com/
    fxTwitterUrl = twitterUrl.replace( 'https://twitter.com/', 'https://d.fxtwitter.com/')

    # 將網頁資料 GET 下來
    r = requests.get(fxTwitterUrl)

    # 取得原始圖片或影片連結
    mediaUrl = r.url

    # 判斷網址為「圖片」
    if mediaUrl.find('.jpg') > 0 or mediaUrl.find('.png') > 0:
        
        # flexMessage 容器
        flex_message_contents = []

        # 第一張圖片網址
        firstMediaUrl = mediaUrl

        # 取得第一張圖片比例
        imgRatio = getImgRatio(firstMediaUrl)

        # 將圖片代入模板，並放入 flex_message_contents 中
        flex_message_contents.append( twitterImgPageTemplate(firstMediaUrl, imgRatio) )

        # 取得第二、三、四張照片
        for i in [2, 3, 4]:
            imgUrl = fxTwitterUrl + "/photo/"+ str(i)
            imgUrl = requests.get(imgUrl).url
            if imgUrl == firstMediaUrl:
                break
            else:
                print(imgUrl)
                
                # 將圖片代入模板，並放入 flex_message_contents 中
                flex_message_contents.append( twitterImgPageTemplate(imgUrl, imgRatio) )

        # 包裝訊息
        flex_message = FlexSendMessage(
            alt_text= 'Twitter 圖片擷取',
            contents={
                "type": "carousel",
                "contents": flex_message_contents
                }
            )
        # 發送訊息
        line_bot_api.reply_message(event.reply_token, flex_message)


    # 判斷網址為「影片」
    elif mediaUrl.find('.mp4') > 0 :
        
        # 整理網址：去除網址 ? 後面的部分
        videoUrl = mediaUrl.split("?")[0]

        # 包裝訊息：影片無法使用 carousel 輪播屬性的 flex message
        flex_message = FlexSendMessage(
            alt_text= 'Twitter 影片擷取',
            contents= twitterVideoPageTemplate( videoUrl ),
        )
        # 發送訊息
        line_bot_api.reply_message(event.reply_token, flex_message)



# 取得圖片比例
def getImgRatio(url):
    # 發送請求並獲取圖像
    response = requests.get(url)
    imgOpen = Image.open(BytesIO(response.content))
    width, height = imgOpen.size
    imgRatio = str(width)+":" + str(height)

    return imgRatio



# 圖片頁面模板
def twitterImgPageTemplate( url, ratio ):

    pageTemplate = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "image",
                    "url": url,
                    "size": "full",
                    "aspectRatio": ratio,
                    "gravity": "top",
                    "aspectMode": "cover"
                }
            ],
            "paddingAll": "0px"
        },
        "action": {
            "type": "uri",
            "label": "action",
            "uri": url
        }
    }

    return pageTemplate




# 影片頁面模板
def twitterVideoPageTemplate( url ):

    pageTemplate = {
        "type": "bubble",
        "size": "giga",
        "hero": {
                "type": "video",
                "url": url,
                "previewUrl": "https://i.imgur.com/rkyxRlh.png",
                "aspectRatio": "4:3",
                "action": {
                    "type": "uri",
                    "label": "瀏覽器觀看",
                        "uri": url
                },
            "altContent": {
                    "type": "image",
                    "size": "full",
                    "aspectRatio": "4:3",
                    "aspectMode": "cover",
                    "url": "https://i.imgur.com/rkyxRlh.png"
                }
        },
        "styles": {
            "hero": {
                "backgroundColor": "#000000"
            }
        },
    }

    return pageTemplate
