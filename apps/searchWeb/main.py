# 搜尋網頁
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

import os

from apps.common.common import *
from urllib.parse import quote

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

# 網頁搜尋
def searchWeb(event, userMessage):
    userMessage = userMessage.replace('搜尋：', '')
    keyword = userMessage
    # 中文字轉換編碼
    keyword = quote(keyword)

    pege_info = {
        "banner" : localImg("banner/search.png"),
        "text_color": "#68141C",
        "title": "要使用哪一個搜尋引擎？",
        "illustrate": "搜尋：「" + userMessage + "」",
        "options": [
            {
                "labelText": "Google",
                "url": "https://www.google.com/search?q=" + keyword
            },
            {
                "labelText": "Bing",
                "url": "https://www.bing.com/search?q=" + keyword
            },
            {
                "labelText": "Yahoo",
                "url": "https://tw.search.yahoo.com/search?p=" + keyword
            },
            {
                "labelText": "Duckduckgo",
                "url": "https://duckduckgo.com/?q=" + keyword
            },
            {
                "labelText": "Wikipedia",
                "url": "https://zh.wikipedia.org/wiki/" + keyword
            },
            {
                "labelText": "Chatgpt",
                "url": "https://chatgpt.com/?hints=search&q=" + keyword
            },
            # {
            #     "labelText": "Claude",
            #     "url": "https://claude.ai/new/?q=" + keyword
            # },
            # {
            #     "labelText": "Perplexity",
            #     "url": "https://www.perplexity.ai/search?q=" + keyword
            # },
        ],
        "alt_text":"搜尋結果！",
        "quick_reply" : [
            {
                "label": "商品搜尋",
                "text" : "購物：" + userMessage,
            },
            {
                "label": "串流影片搜尋",
                "text" : "追劇：" + userMessage,
            },
            {
                "label": "音樂搜尋",
                "text" : "音樂：" + userMessage,
            },
        ]
    }
    
    
    # flexMessage 容器
    flex_message_contents = []
    pageTemplate = searchPageTemplate(pege_info)
    flex_message_contents.append( pageTemplate )
    
    flexMessage_reply(event, flex_message_contents, pege_info)

# 購物網站搜尋
def searchWebShopping(event, userMessage):
    userMessage = userMessage.replace('購物：', '')
    keyword = userMessage
    # 中文字轉換編碼
    keyword = quote(keyword)

    pege_info =  {
        "banner" : localImg("banner/shopping.png"),
        "text_color": "#68141C",
        "title": "要使用哪一個購物網站？",
        "illustrate": "搜尋：「" + userMessage + "」",
        "options": [
            {
                "labelText": "蝦皮購物",
                "url": "https://shopee.tw/search?keyword=" + keyword
            },
            {
                "labelText": "露天購物",
                "url": "https://www.ruten.com.tw/find/?q=" + keyword
            },
            {
                "labelText": "PChome",
                "url": "https://ecshweb.pchome.com.tw/search/v3.3/?q=" + keyword
            },
            {
                "labelText": "Momo 購物網",
                "url": "https://www.momoshop.com.tw/search/searchShop.jsp?keyword=" + keyword
            },
            {
                "labelText": "Coupang 酷澎",
                "url": "https://www.tw.coupang.com/search?q=" + keyword
            },
            {
                "labelText": "Biggo",
                "url": "https://biggo.com.tw/s/?q=" + keyword
            }
        ],
        "alt_text":"推坑！推坑！買買買！",
    }
    # flexMessage 容器
    flex_message_contents = []
    pageTemplate = searchPageTemplate(pege_info)
    flex_message_contents.append( pageTemplate )
    
    flexMessage_reply(event, flex_message_contents, pege_info)

# 串流網站搜尋
def searchWebVideo(event, userMessage):
    userMessage = userMessage.replace('追劇：', '')
    userMessage = userMessage.replace('影片：', '')
    keyword = userMessage
    # 中文字轉換編碼
    keyword = quote(keyword)

    pege_info =  {
        "banner" : localImg("banner/search.png"),
        "text_color": "#68141C",
        "title": "要搜尋哪一個串流平台？",
        "illustrate": "搜尋：「" + userMessage + "」",
        "options": [
            {
                "labelText": "Youtube",
                "url": "https://www.youtube.com/results?search_query=" + keyword
            },
            # {
            #     "labelText": "Twitch",
            #     "url": "https://www.twitch.tv/search?term=" + keyword
            # },
            {
                "labelText": "Justwatch 搜尋引擎",
                "url": "https://www.justwatch.com/tw/search?q=" + keyword
            },
            # {
            #     "labelText": "其他 OTT 影音搜尋",
            #     # "url": "https://ott-search.com/",
            #     "url": localHtml("ott-search.html")+"/?query=" + keyword
            # },

        ],
        "alt_text":"搜尋結果！",
        "quick_reply" : [
            {
                "label": "動畫搜尋",
                "text" : "動畫：" + userMessage,
            },
        ]
    }
    # flexMessage 容器
    flex_message_contents = []
    pageTemplate = searchPageTemplate(pege_info)
    flex_message_contents.append( pageTemplate )
    
    flexMessage_reply(event, flex_message_contents, pege_info)

# 動畫網站搜尋
def searchWebAnime(event, userMessage):
    userMessage = userMessage.replace('動畫：', '')
    userMessage = userMessage.replace('動漫：', '')
    keyword = userMessage
    # 中文字轉換編碼
    keyword = quote(keyword)

    pege_info =  {
        "banner" : localImg("banner/search.png"),
        "text_color": "#68141C",
        "title": "要搜尋哪一個動畫平台？",
        "illustrate": "搜尋：「" + userMessage + "」",
        "options": [
            {
                "labelText": "動畫瘋",
                "url": "https://ani.gamer.com.tw/search.php?keyword=" + keyword
            },
            {
                "labelText": "你的動畫 搜尋引擎",
                "url": "https://youranimes.tw/search?tk=" + keyword
            },
        ],
        "alt_text":"搜尋結果！",
    }
    # flexMessage 容器
    flex_message_contents = []
    pageTemplate = searchPageTemplate(pege_info)
    flex_message_contents.append( pageTemplate )
    
    flexMessage_reply(event, flex_message_contents, pege_info)

# 音樂網站搜尋
def searchWebMusic(event, userMessage):
    userMessage = userMessage.replace('音樂：', '')
    keyword = userMessage
    # 中文字轉換編碼
    keyword = quote(keyword)

    pege_info =  {
        "banner" : localImg("banner/search.png"),
        "text_color": "#68141C",
        "title": "要搜尋哪一個音樂平台？",
        "illustrate": "搜尋：「" + userMessage + "」",
        "options": [
            {
                "labelText": "Youtube Music",
                "url": "https://music.youtube.com/search?q=" + keyword
            },
            {
                "labelText": "Apple Music",
                "url": "https://music.apple.com/tw/search?term=" + keyword
            },
            {
                "labelText": "Spotify",
                "url": "https://open.spotify.com/search/recent/" + keyword,
                "url_desktop": "https://open.spotify.com/search/" + keyword
            },
            {
                "labelText": "KKBOX",
                "url": "https://www.kkbox.com/tw/tc/search?q=" + keyword
            },
            {
                "labelText": "Line Music",
                "url": "https://music-tw.line.me/search?query=" + keyword
            },
        ],
        "alt_text":"搜尋結果！",
    }
    # flexMessage 容器
    flex_message_contents = []
    pageTemplate = searchPageTemplate(pege_info)
    flex_message_contents.append( pageTemplate )
    
    flexMessage_reply(event, flex_message_contents, pege_info)

# 電影院網站
def searchWebMovie(event):
    pege_info =  {
        "banner" : localImg("banner/movie.png"),
        "text_color": "#04437c",
        "title": "想去哪看電影呢？",
        "illustrate": "最近上映的電影",
        "options": [
            {
                "labelText": "LINE 電影",
                "url": "https://today.line.me/tw/v2/movie/incinemas/newrelease"
            },
            {
                "labelText": "威秀影城",
                "url": "https://www.vscinemas.com.tw/vsweb/film/index.aspx"
            },
            {
                "labelText": "秀泰影城",
                "url": "https://www.showtimes.com.tw/programs"
            },
            {
                "labelText": "國賓影城",
                "url": "https://www.ambassador.com.tw/home/MovieList?Type=1"
            },
            {
                "labelText": "環球影城",
                "url": "https://www.u-movie.com.tw/cinema/page.php?page_type=now&ver=tw&portal=cinema"
            },

        ],
        "alt_text":"電影資訊！",
    }
    # flexMessage 容器
    flex_message_contents = []
    pageTemplate = searchPageTemplate(pege_info)
    flex_message_contents.append( pageTemplate )
    
    flexMessage_reply(event, flex_message_contents, pege_info)

# 圖片搜尋
def searchWebImg(event, imgUrl):

    if imgUrl == "":
        replyLineMessage = TextSendMessage("目前沒有上傳任何圖片～")
        line_bot_api.reply_message(event.reply_token, replyLineMessage)

    else:

        # 第一頁
        pege_info_1 = {
            "banner" : localImg("banner/search.png"),
            "text_color": "#68141C",
            "title": "要使用哪一個搜尋引擎？",
            "illustrate": "主流搜尋引擎",
            "options": [
                {
                    "labelText": "Google",
                    "url": "https://www.google.com/searchbyimage?sbisrc=4chanx&image_url=" + imgUrl+"&safe=off"
                },
                {
                    "labelText": "Bing",
                    "url": "https://www.bing.com/images/search?view=detailv2&iss=sbi&form=SBIVSP&sbisrc=UrlPaste&q=imgurl:" + imgUrl
                },
                {
                    "labelText": "Yandex",
                    "url": "https://yandex.ru/images/touch/search?rpt=imageview&url=" + imgUrl
                },
            ],
            "alt_text":"以圖搜圖結果！",
        }
        
        # 第二頁
        pege_info_2 = {
            "banner" : localImg("banner/search.png"),
            "text_color": "#68141C",
            "title": "要使用哪一個搜尋引擎？",
            "illustrate": "ACG 圖像搜尋引擎",
            "options": [
                {
                    "labelText": "Ascii2d",
                    "url": "https://ascii2d.net/search/url/" + imgUrl
                },
                {
                    "labelText": "Saucenao",
                    "url": "https://saucenao.com/search.php?url=" + imgUrl
                },
                {
                    "labelText": "Tracemoe",
                    "url": "https://trace.moe/?url=" + imgUrl
                }
            ],
            "alt_text":"以圖搜圖結果！",
        }

        # flexMessage 容器
        flex_message_contents = []
        flex_message_contents.append( searchPageImgTemplate(imgUrl))
        flex_message_contents.append( searchPageTemplate(pege_info_1) )
        flex_message_contents.append( searchPageTemplate(pege_info_2) )


        flexMessage_reply(event, flex_message_contents, pege_info_1)

# 網頁搜尋
def searchMap(event, userMessage):
    keyword = userMessage.replace('地圖：', '')
    searchUrl = "https://www.google.com/maps/place?q=" + quote(keyword)

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
                    "url": "https://i.imgur.com/j3p7eux.png",
                    "size": "xxs",
                    "flex": 1,
                    "offsetEnd": "5px"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": keyword,
                            "weight": "bold",
                            "size": "sm",
                            "wrap": False,
                            "offsetBottom": "1px"
                        },
                        {
                            "type": "text",
                            "text": "Google Map 檢索結果",
                            "wrap": True,
                            "color": "#8c8c8c",
                            "size": "xs",
                            "offsetTop": "1px"
                        }
                    ],
                    "flex": 4
                }
            ],
            "justifyContent": "center",
            "alignItems": "center",
            "paddingAll": "16px",
            "paddingEnd": "20px"
        },
        "action": {
            "type": "uri",
            "label": "action",
            "uri": searchUrl
        }
    }
    contentsList.append(contentsItem)

    # 包裝訊息
    replyLineMessage = FlexSendMessage(
        alt_text='Google 地圖資訊',
        contents={
            "type": "carousel",
            "contents": contentsList,
        }
    )
    # 回傳訊息
    line_bot_api.reply_message(event.reply_token, replyLineMessage)

# =========================================================== #

# 頁面模板
def searchPageTemplate( pege_info ):

    # 頁面內容（標題 + 按鈕選項）
    pageTemplate_Contents = []

    # 標題 (pageTemplate_Title)
    pageTemplate_Title = [
        {
            "type": "text",
            "text": pege_info["title"],
            "weight": "bold",
            "size": "lg",
            "color": pege_info["text_color"],
            "align": "center"
        }, {
            "type": "text",
            "text": pege_info["illustrate"],
            "weight": "bold",
            "size": "sm",
            "color": pege_info["text_color"] + "99",
            "align": "center",
            "margin": "4px"
        }, {
            "type": "separator",
            "margin": "12px"
        },
    ]
    for i in pageTemplate_Title:
        pageTemplate_Contents.append( i )

    # 按鈕選項 (pageTemplate_Btn)
    for btn in pege_info["options"]:
        
        # 檢查是否有電腦版連結
        try:
            url_desktop = btn["url_desktop"]
        except:
            url_desktop = btn["url"]
        
        pageTemplate_Btn = [
            # 選項
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": btn["labelText"],
                        "weight": "bold",
                        "color": pege_info["text_color"],
                    }
                ],
                "paddingAll": "12px",
                "justifyContent": "center",
                "alignItems": "center",
                "action": {
                    "type": "uri",
                    "label": "action",
                    "uri": btn["url"],
                    "altUri": {
                        "desktop": url_desktop,
                    }
                }
            },
            # 分隔線
            {"type": "separator"},
        ]

        for i in pageTemplate_Btn:
            pageTemplate_Contents.append( i )

    # 清除最後一項（分隔線）
    del pageTemplate_Contents[-1]

    # 頁面 (pageTemplate)
    pageTemplate = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "image",
                    "url": pege_info["banner"],
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

    return pageTemplate


# 頁面模板(圖片)
def searchPageImgTemplate( img_url ):

    # 頁面 (pageTemplate)
    pageTemplate = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                # 圖片
                {
                    "type": "image",
                    "url": img_url,
                    "size": "full",
                    "aspectRatio": "1:1",
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
                            "text": "搜尋圖片",
                            "size": "xxs",
                            "weight": "bold",
                            "color": "#ffffff"
                        }
                        ],
                        "backgroundColor": "#00000099",
                        "paddingAll": "4px",
                        "width": "70px",
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
        }
    }

    return pageTemplate


# 包裝訊息，發送訊息
def flexMessage_reply(event, flex_message_contents, pege_info):

    # 如果有設定 快速回覆
    try:
        quick_reply_list = []
        for item in pege_info["quick_reply"]:
            quick_reply_item = QuickReplyButton(
                action=MessageAction(label = item["label"], text = item["text"] )
            )
            quick_reply_list.append( quick_reply_item )
        # 包裝訊息
        flex_message = FlexSendMessage(
            alt_text= pege_info["alt_text"],
            contents={
                "type": "carousel",
                "contents": flex_message_contents
            },
            quick_reply= QuickReply(
                items=quick_reply_list
            )
        )
        
        # 發送訊息
        line_bot_api.reply_message(event.reply_token, flex_message)


    # 沒有 快速回覆
    except:
        # 包裝訊息
        flex_message = FlexSendMessage(
            alt_text= pege_info["alt_text"],
            contents={
                "type": "carousel",
                "contents": flex_message_contents
            },
        )
        
        # 發送訊息
        line_bot_api.reply_message(event.reply_token, flex_message)


