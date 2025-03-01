from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

import requests
import googletrans
import os
from apps.common.common import *


line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))


# 主要
def twitter_message_main(event, userMessage):
    
    twitter_url_api = fix_twitter_url(userMessage)
    twitter_url = reset_twitter_url(twitter_url_api)
    twitter_data = get_twitter_data(twitter_url_api)

    tweet_type = identify_tweet_type(twitter_data)

    # flexMessage 容器
    flex_message_contents = []
    
    if tweet_type:

        tweet_info = extract_tweet_info(twitter_data)
        
        # 不用翻譯
        if tweet_info['text'] == tweet_info['text_translation']:
            # 原文
            template = twitter_text_page_template( tweet_info, twitter_url , "原文" )
            # 包裝訊息
            flex_message_text_page = FlexSendMessage(
                alt_text= 'Twitter 文字擷取',
                contents={
                    "type": "carousel",
                    "contents": [template]
                    }
                )


        # 翻譯
        else:
            # 原文
            template = twitter_text_page_template( tweet_info, twitter_url , "原文" )
            # 翻譯
            template_translation = twitter_text_page_template( tweet_info, twitter_url , "翻譯" )
            # 包裝訊息
            flex_message_text_page = FlexSendMessage(
                alt_text= 'Twitter 文字擷取',
                contents={
                    "type": "carousel",
                    "contents": [template, template_translation]
                    }
                )

    if tweet_type == "圖片推文":
        width, height, img_urls = get_photo_info(twitter_data)
        ratio = str(width) + ":" + str(height)

        for img_url in img_urls:
            template = twitter_img_page_template( img_url, img_url, ratio, "圖片" )
            flex_message_contents.append( template )
        
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

    elif tweet_type == "影片推文" or tweet_type == "GIF 推文":
        width, height, img_urls, video_url = get_video_info(twitter_data)
        ratio = str(width) + ":" + str(height)
        template = twitter_video_page_template( video_url, img_urls, ratio )

        if tweet_type == "GIF 推文":
            alt_text = 'Twitter GIF 擷取'
        else:
            alt_text = 'Twitter 影片擷取'

        # 包裝訊息：影片無法使用 carousel 輪播屬性的 flex message
        flex_message = FlexSendMessage(
            alt_text= alt_text,
            contents= template,
        )
        # 發送訊息
        line_bot_api.reply_message(event.reply_token, [flex_message, flex_message_text_page])

    elif tweet_type == "純文字推文":
        line_bot_api.reply_message(event.reply_token, [flex_message_text_page])


# 整理網址
def fix_twitter_url(text):
    url = text

    # 整理網址：去除網址 ? 與 /photo/ 後面的部分
    url = url.split("?")[0]
    url = url.split("/photo/")[0]

    replace_list = [
        'https://x.com/',
        'https://fxtwitter.com/',
        'https://vxtwitter.com/',
        'https://twitter.com/',
        'https://d.fxtwitter.com/'
    ]

    for replace in replace_list:
        url = url.replace(replace,"https://api.fxtwitter.com/")

    return url

# 網址還原
def reset_twitter_url(url):
    url = url.replace("https://api.fxtwitter.com/", "https://twitter.com/")
    return url

# 取得 Twitter 資料
def get_twitter_data(url):
    try:
        # 將 x.com 或 twitter.com 轉換為 api.fxtwitter.com
        converted_url = url.replace("https://x.com/", "https://api.fxtwitter.com/")
        converted_url = converted_url.replace("https://twitter.com/", "https://api.fxtwitter.com/")
        
        # 設定 headers
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive'
        }
        
        # 發送 GET 請求，加上 headers
        response = requests.get(converted_url, headers=headers)
        
        # 檢查狀態碼
        response.raise_for_status()
        
        # 檢查回應內容是否為空
        if not response.text:
            print("回應內容為空")
            return None
            
        # 嘗試解析 JSON
        try:
            twitter_data = response.json()
            return twitter_data
        except requests.exceptions.JSONDecodeError as e:
            print(f"JSON 解析錯誤: {e}")
            print(f"回應內容: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"請求錯誤: {e}")
        return None

# 判斷訊息種類
def identify_tweet_type(tweet_data):

    tweet = tweet_data.get('tweet', {})
    media = tweet.get('media', {})
    
    # 檢查是否有 media 欄位
    if not media:
        return "純文字推文"
    
    # 取得所有媒體內容
    all_media = media.get('all', [])
    
    if not all_media:
        return "純文字推文"
        
    # 檢查媒體類型
    first_media = all_media[0]
    media_type = first_media.get('type')
    
    if media_type == 'video':
        return "影片推文"
    elif media_type == 'gif':
        return "GIF 推文"
    elif media_type == 'photo':
        # 檢查照片數量
        photos = media.get('photos', [])
        photo_count = len(photos)
        # return f"圖片推文 ({photo_count} 張)"
        return "圖片推文"
    
    return "未知類型推文"

# 整理推文的基本資訊
def extract_tweet_info(tweet_data):

    try:
        tweet = tweet_data.get('tweet', {})
        author = tweet.get('author', {})
        
        translator = googletrans.Translator()

        # 整理所需資訊
        tweet_info = {
            'text': tweet.get('text', ''),  # 推文內容
            'text_translation' : translator.translate( tweet.get('text', ''), dest="zh-tw").text, 
            'author_name': author.get('name', ''),  # 作者名稱
            'author_screen_name': author.get('screen_name', ''),  # 作者帳號
            'author_avatar_url': author.get('avatar_url', ''),  # 作者大頭貼
            'created_at': tweet.get('created_at', ''),  # 發文時間
        }
        
        return tweet_info
        
    except Exception as e:
        print(f"解析推文時發生錯誤: {str(e)}")
        return None

# 獲取圖片推文的資訊
def get_photo_info(tweet_data):

    tweet = tweet_data.get('tweet', {})
    media = tweet.get('media', {})
    
    # 檢查是否有 media 欄位
    if not media or not media.get('all'):
        return False, None, None, []
    
    # 確認是否為圖片推文
    first_media = media['all'][0]
    if first_media.get('type') != 'photo':
        return False, None, None, []
    
    # 獲取第一張圖片的寬和高
    first_width = first_media.get('width')
    first_height = first_media.get('height')
    
    # 獲取所有圖片的 URL
    photos = media.get('photos', [])
    photo_urls = [photo.get('url') for photo in photos if photo.get('url')]
    
    return first_width, first_height, photo_urls

# 獲取影片推文的資訊
def get_video_info(twitter_data):

    try:
        # 獲取 media 資訊
        media = twitter_data.get('tweet', {}).get('media', {})
        if not media or 'videos' not in media:
            return None, None, None, None
            
        # 獲取第一個影片的資訊
        video = media['videos'][0]
        
        # 獲取寬度和高度
        width = video.get('width')
        height = video.get('height')
        
        # 獲取縮圖網址
        thumbnail_url = video.get('thumbnail_url')
        
        # 獲取影片網址（選擇最高畫質）
        variants = video.get('variants', [])
        video_variants = [v for v in variants if v.get('content_type') == 'video/mp4']
        
        if not video_variants:
            return width, height, thumbnail_url, None
            
        # 根據 bitrate 排序，選擇最高畫質
        highest_quality = max(
            video_variants,
            key=lambda x: x.get('bitrate', 0)
        )
        video_url = highest_quality.get('url')
        
        return width, height, thumbnail_url, video_url
        
    except Exception as e:
        print(f"Error processing video info: {e}")
        return None, None, None, None


# 圖片頁面模板
def twitter_img_page_template( url, imgUrl, ratio, type ):

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
def twitter_video_page_template( url, img, ratio ):

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
def twitter_text_page_template( tweet_info, url, status ):

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
                "url": tweet_info['author_avatar_url'],
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
                "text": tweet_info['author_name'],
                "weight": "bold",
                "color": "#333333",
                "offsetBottom": "2px"
            },
            {
                "type": "text",
                "text": "@"+ tweet_info['author_screen_name'],
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
    if status == "翻譯":
        tweet_text_contents = tweet_info['text_translation']
    else:
        tweet_text_contents = tweet_info['text']
    tweet_text = {
        "type": "box",
        "layout": "vertical",
        "paddingTop": "12px",
        "contents": [
            {
                "type": "text",
                "text": tweet_text_contents,
                "size": "xs",
                "color": "#777777",
                "wrap": True,
                "lineSpacing": "4px"
            }
        ],
    }

    # 翻譯標籤
    tag_width = get_char_width_ratio(status) * 12
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
                "text": status,
                "color": "#02497d",
                "align": "center",
                "size": "xs",
                "weight": "bold"
                }
            ],
        }

    tweet_contents.append( tweet_author )
    tweet_contents.append( tweet_text )
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
            "uri": url
        },
    }
    return pageTemplate