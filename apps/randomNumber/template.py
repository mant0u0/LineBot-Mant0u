from apps.common.common import *
import random


# 顯示亂數頁面
def random_number_page_template( random_number, min_number, max_number ):

    # 取得主題代號 (1~7)
    random_theme = random.randint(1, 7)

    # 取得主題顏色
    theme_color_list = ["", "#8c2937", "#934b27", "#91592a", "#2d6c3d", "#2e635e", "#294363", "#3c3b7c"]
    theme_color = theme_color_list[random_theme]


    # 數字位數分割（ 例如："123" -> ["1","2","3"] ）
    message_content_num = []
    for number in str(random_number):
        item = {
            "type": "image",
            "url": localImg("randomNumber/"+str(number)+".png"),
        }
        message_content_num.append(item)

    # 訊息排版微調
    if len(str(random_number)) < 3:
        padding = "60px"
        offsetTop = "10%"
    if len(str(random_number)) == 3:
        padding = "40px"
        offsetTop = "15%"
    if len(str(random_number)) >= 4:
        padding = "20px"
        offsetTop = "20%"

    # 介面修正：數字區間方塊寬度修正
    num_box_text_len = len(str(min_number) + str(max_number))
    num_box_max_width = num_box_text_len * 3 + 18
    if num_box_text_len > 10:
        num_box_max_width = num_box_text_len * 3.2 + 18

    # LINE 訊息包裝
    page_template = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "image",
                    "url": localImg("randomNumber/BG"+str(random_theme)+".png"),
                    "size": "full",
                    "aspectMode": "cover",
                    "aspectRatio": "1:1",
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "baseline",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": str(min_number),
                                            "align": "center",
                                            "weight": "bold",
                                            "color": theme_color,
                                            "flex": 0,
                                            "size": "md"
                                        },
                                        {
                                            "type": "icon",
                                            "url": localImg("randomNumber/ARROW"+str(random_theme)+".png"),
                                            "margin": "4px",
                                            "size": "xxs"
                                        },
                                        {
                                            "type": "text",
                                            "text": str(max_number),
                                            "align": "center",
                                            "weight": "bold",
                                            "color": theme_color,
                                            "flex": 0,
                                            "size": "md",
                                            "margin": "4px"
                                        }
                                    ],
                                    "backgroundColor": "#ffffff",
                                    "cornerRadius": "100px",
                                    "paddingAll": "4px",
                                    "paddingStart": "16px",
                                    "paddingEnd": "16px",
                                    "maxWidth": str(num_box_max_width) + "%",
                                    "justifyContent": "center"
                                },
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": message_content_num,
                                    "width": "100%",
                                    "paddingStart": padding,
                                    "paddingEnd": padding,
                                    "paddingTop": "20px"
                                }
                            ],
                            "alignItems": "center",
                            "position": "absolute",
                            "width": "100%",
                            "offsetTop": offsetTop
                        }
                    ],
                    "position": "absolute",
                    "width": "100%",
                    "height": "100%",
                    "justifyContent": "center",
                    "alignItems": "center"
                },
                {
                    "type": "image",
                    "url": localImg("randomNumber/BASE"+str(random_theme)+".png"),
                    "size": "full",
                    "aspectMode": "cover",
                    "aspectRatio": "1:1",
                    "position": "absolute",
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": str(random_number)+" !",
                                            "size": "lg",
                                            "color": theme_color,
                                            "weight": "bold",
                                            "align": "center"
                                        }
                                    ]
                                }
                            ],
                            "spacing": "xs"
                        }
                    ],
                    "position": "absolute",
                    "offsetBottom": "0px",
                    "offsetStart": "0px",
                    "offsetEnd": "0px",
                    "paddingAll": "20px"
                }
            ],
            "paddingAll": "0px",
            "action": {
                "type": "message",
                "label": "action",
                "text": "亂數："+str(min_number) + " ~ " + str(max_number)
            },
        }
    }

    return page_template