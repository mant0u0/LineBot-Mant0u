from linebot import LineBotApi
from linebot.models import *

import os
from apps.common.common import *
from apps.common.dateConverter import *

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))

# 日曆
def calendarMain(event, date_obj):

    # 計算相差天數
    diff_day = calculateDays(date_obj)

    # 西元
    year = str(date_obj.year)
    month = str(date_obj.month)
    day = str(date_obj.day)
    week = str(date_obj.weekday()+1)
    
    # 版面顏色
    template_skin = "blue"
    if week == "6":
        template_skin = "green_1"
    if week == "7":
        template_skin = "red"

    # 民國
    tw_year = int(date_obj.year) - 1911
    if tw_year > 0:
        tw_year_title = {
            "type": "image",
            "url": localImg(f"calendar/{template_skin}/year/tw.png"),
            "aspectRatio": "150:80",
            "size": "32px"
        }
    elif tw_year <= 0:
        tw_year = (tw_year-1) * (-1)
        tw_year_title = {
            "type": "image",
            "url": localImg(f"calendar/{template_skin}/year/bftw.png"),
            "aspectRatio": "210:80",
            "size": "45px"
        }

    # 農曆
    try:
        lunar_state = True
        lunar_obj = getDateLunar(date_obj)
        ganzhi_1 = str(lunar_obj["ganzhi_1"])
        ganzhi_2 = str(lunar_obj["ganzhi_2"])
        zodiac = str(lunar_obj["zodiac"])
        month_l = str(lunar_obj["month"])
        day_l = str(lunar_obj["day"])
    except:
        lunar_state = False
        # print(date_obj)
        print("無法計算農曆")

    # 民國年文字排版
    tw_year_contents = []
    tw_year = str(tw_year)
    for char in tw_year:
        tw_year_item = {
            "type": "image",
            "url": localImg(f"calendar/{template_skin}/year/{char}.png"),
            "aspectRatio": "68:76",
            "size": "14px",
            "flex": 0
        }
        tw_year_contents.append(tw_year_item)

    # 西元年文字排版
    year_contents = []
    for char in year:
        year_item = {
            "type": "image",
            "url": localImg(f"calendar/{template_skin}/year/{char}.png"),
            "aspectRatio": "68:76",
            "size": "14px",
            "flex": 0
        }
        year_contents.append(year_item)

    # 背景圖片
    template_background ={
        "type": "image",
        "url": localImg(f"calendar/{template_skin}/background.png"),
        "aspectRatio": "1:1",
        "size": "full"
    }

    # 底部結果文字的背景
    template_bottom = {
        "type": "image",
        "url": localImg(f"calendar/{template_skin}/bottom.png"),
        "position": "absolute",
        "size": "full",
        "aspectRatio": "1:1"
    }

    # 結果文字
    template_bottom_text = {
        "type": "box",
        "layout": "vertical",
        "borderWidth": "1px",
        "position": "absolute",
        "offsetBottom": "0px",
        "paddingAll": "20px",
        "width": "100%",
        "height": "24%",
        "justifyContent": "center",
        "alignItems": "center",
        "contents": [
        {
            "type": "text",
            "text": diff_day,
            "size": "lg",
            "color": "#ffffff",
            "weight": "bold"
        }
        ],
    }

    # 日期與星期
    template_day_and_week = {
        "type": "box",
        "layout": "vertical",
        "position": "absolute",
        "paddingAll": "20px",
        "width": "100%",
        "height": "75%",
        "justifyContent": "center",
        "alignItems": "center",
        "offsetTop": "0px",
        "contents": [
            {
                "type": "image",
                "url": localImg(f"calendar/{template_skin}/day/{day}.png"),
                "aspectRatio": "350:300",
                "size": "lg",
            },
            {
                "type": "image",
                "url": localImg(f"calendar/{template_skin}/week/{week}.png"),
                "aspectRatio": "280:90"
            }
        ],
    }

    # 西元 + 月份
    template_adyear_and_month = {
        "type": "box",
        "layout": "vertical",
        "position": "absolute",
        "paddingAll": "16px",
        "width": "100%",
        "height": "75%",
        "justifyContent": "flex-start",
        "alignItems": "flex-end",
        "offsetTop": "0px",
        "contents": [
        {
            "type": "image",
            "url": localImg(f"calendar/{template_skin}/year/ad.png"),
            "aspectRatio": "150:80",
            "size": "32px"
        },
        {
            "type": "box",
            "layout": "horizontal",
            "contents": year_contents,
            "margin": "4px",
            "height": "20px",
            "width": "40%",
            "justifyContent": "flex-end"
        },
        {
            "type": "image",
            "url": localImg(f"calendar/{template_skin}/month/{month}.png"),
            "size": "24px",
            "aspectRatio": "65:130",
            "margin": "2px"
        }
        ],
    }

    # 民國 + 農曆
    if lunar_state:
        template_twyear_and_lunar = {
            "type": "box",
            "layout": "vertical",
            "position": "absolute",
            "paddingAll": "16px",
            "width": "100%",
            "height": "75%",
            "justifyContent": "flex-start",
            "alignItems": "flex-start",
            "offsetTop": "0px",
            "contents": [
            tw_year_title,
            {
                "type": "box",
                "layout": "horizontal",
                "contents": tw_year_contents,
                "margin": "4px",
                "height": "20px",
                "width": "40%",
                "justifyContent": "flex-start"
            },
            {
                "type": "image",
                "url": localImg(f"calendar/{template_skin}/zodiac/{zodiac}.png"),
                "size": "24px",
                "margin": "2px",
                "aspectRatio": "1:1"
            },
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                {
                    "type": "image",
                    "url": localImg(f"calendar/{template_skin}/lunar_year/1/{ganzhi_1}.png"),
                    "aspectRatio": "68:76",
                    "size": "14px",
                    "flex": 0
                },
                {
                    "type": "image",
                    "url": localImg(f"calendar/{template_skin}/lunar_year/2/{ganzhi_2}.png"),
                    "aspectRatio": "68:76",
                    "size": "14px",
                    "flex": 0
                }
                ],
                "height": "20px",
                "width": "20%",
                "justifyContent": "flex-start",
                "margin": "2px",
                "offsetEnd": "2px"
            },
            {
                "type": "image",
                "size": "24px",
                "aspectRatio": "65:130",
                "url": localImg(f"calendar/{template_skin}/lunar_month/{month_l}.png"),
            },
            {
                "type": "image",
                "url": localImg(f"calendar/{template_skin}/lunar_day/{day_l}.png"),
                "size": "24px",
                "aspectRatio": "65:130"
            }
            ],
        }

    else:
    # 民國（無農曆）
        template_twyear_and_lunar = {
            "type": "box",
            "layout": "vertical",
            "position": "absolute",
            "paddingAll": "16px",
            "width": "100%",
            "height": "75%",
            "justifyContent": "flex-start",
            "alignItems": "flex-start",
            "offsetTop": "0px",
            "contents": [
            tw_year_title,
            {
                "type": "box",
                "layout": "horizontal",
                "contents": tw_year_contents,
                "margin": "4px",
                "height": "20px",
                "width": "40%",
                "justifyContent": "flex-start"
            },
            ],
        }


    
    pageTemplate_contents = [
        template_background,
        template_bottom,
        template_bottom_text,
        template_day_and_week,
        template_adyear_and_month,
        template_twyear_and_lunar,
    ]



    # 包裝訊息
    flex_message = FlexSendMessage(
        alt_text='日曆',
        contents={
            "type": "carousel",
            "contents": [
                {
                    "type": "bubble",
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "paddingAll": "0px",
                        "contents": pageTemplate_contents,
                    },
                    "action": {
                        "type": "uri",
                        "uri": f"https://calendar.google.com/calendar/u/0/r/eventedit?dates={date_obj.strftime('%Y%m%d')}/{date_obj.strftime('%Y%m%d')}",
                        "altUri": {
                            "desktop": f"https://calendar.google.com/calendar/u/0/r/eventedit?dates={date_obj.strftime('%Y%m%d')}/{date_obj.strftime('%Y%m%d')}"
                        }
                    }
                }
            ]
        }
    )
    # 發送訊息
    line_bot_api.reply_message(event.reply_token, flex_message)





# def pageTemplate_