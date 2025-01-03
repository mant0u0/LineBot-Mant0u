from apps.common.common import *

# 顯示第一頁
def random_shuffle_first_page_template( pageText, card_count ):
    page_template = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": "#f2f3f4",
            "paddingAll": "0px",
            "contents": [

                # 底部背景
                {
                    "type": "image",
                    "url": localImg(f"randomShuffle/{str(card_count)}.png"),
                    "size": "full",
                    "aspectMode": "cover",
                    "aspectRatio": "1:1",
                    "gravity": "top"
                },
                # 底部結果文字
                {
                    "type": "box",
                    "layout": "horizontal",
                    "position": "absolute",
                    "offsetBottom": "0px",
                    "offsetStart": "0px",
                    "offsetEnd": "0px",
                    "paddingAll": "20px",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "vertical",
                            "spacing": "xs",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": pageText,
                                            "size": "lg",
                                            "color": "#17656d",
                                            "weight": "bold",
                                            "align": "center"
                                        }
                                    ]
                                }
                            ],
                        }
                    ],
                }
            ],
            # "action": {
            #     "type": "message",
            #     "label": "action",
            #     "text": "文字文字文字文字",
            # },
        }
    }

    return page_template

# 顯示卡片頁面
def random_shuffle_page_template( data, clickedIndex = -1 ):

    # 打亂的清單
    shuffle_list = data["shuffle_list"]

    # 翻牌紀錄
    card_state_list = data["card_state_list"]

    # 介面微調參數
    card_zoomRatio = 1.2
    page_box_gap = "16px"
    if len(shuffle_list) >= 7:
        card_zoomRatio = 1
        page_box_gap = "8px"

    # 打亂的清單 轉換成 卡片物件
    card_template_list = []
    for index, item in enumerate(shuffle_list):
        if card_state_list[index] == 0:
            card_template = unturned_card_template(item, f"翻牌：{index + 1}", card_zoomRatio)
        else:
            # 當沒有人翻牌時，文字全部正常顯示
            if clickedIndex == -1:
                card_template = flipped_card_template(item, "default", card_zoomRatio)
            # 當有人翻牌時，翻牌文字顯示為正常，已被翻牌文字顯示為透明 (強調翻牌的卡片)
            else:
                if clickedIndex == index:
                    card_template = flipped_card_template(item, "active", card_zoomRatio)
                else:
                    card_template = flipped_card_template(item, "default", card_zoomRatio)
        card_template_list.append(card_template)

    # 將卡片組成每行並加入頁面
    page_box_contents = []
    
    # 每行最多的值(最多三個卡片)，其中有四個卡片時為兩個
    row_max = 3
    if len(card_template_list) == 4:
        row_max = 2
    for i in range(0, len(card_template_list), row_max):
        row_template = {
            "type": "box",
            "layout": "horizontal",
            "width": "100%",
            "justifyContent": "center",
            "alignItems": "center",
            "spacing": "16px",
            "contents": card_template_list[i:i + row_max]
        }
        page_box_contents.append(row_template)

    # 頁面內容
    page_template = {
            "type": "bubble",
            "styles": {
                "body": {
                    "backgroundColor": "#f2f3f4"
                }
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "paddingAll": "0px",
                "contents": [
                    {
                        "type": "image",
                        "size": "full",
                        "aspectMode": "cover",
                        "aspectRatio": "1:1",
                        "gravity": "top",
                        "url": localImg(f"transparent_background.png"),
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "width": "100%",
                        "height": "100%",
                        "position": "absolute",
                        "justifyContent": "center",
                        "alignItems": "center",
                        "paddingAll": "12px",
                        "spacing": page_box_gap,
                        "contents": page_box_contents,
                    }
                ],
            },
        }


    return page_template

# 未翻面的卡片
def unturned_card_template( labelText, actionText, zoomRatio = 1 ):

    # 介面微調參數
    
    width = 64 * zoomRatio
    height = 88 * zoomRatio
    aspect_ratio = str(width) + ":" + str(height)
    width_px = str(width) + "px"
    height_px = str(height) + "px"

    return {
        "type": "box",
        "layout": "vertical",
        "width": width_px,
        "height": height_px,
        "contents": [
            # 卡片陰影
            {
                "type": "box",
                "layout": "vertical",
                "contents": [],
                "width": "100%",
                "height": "100%",
                "backgroundColor": "#439aa8",
                "cornerRadius": "8px",
                "position": "absolute"
            },
            # 卡片內容（背面圖案）
            {
                "type": "box",
                "layout": "vertical",
                "position": "absolute",
                "width": "100%",
                "height": "95%",
                "cornerRadius": "8px",
                "contents": [
                    {
                        "type": "image",
                        "url": localImg(f"randomShuffle/card_back.png"),
                        "size": "xl",
                        "aspectRatio": aspect_ratio,
                        "aspectMode": "cover"
                    }
                ],
            }
        ],
        "action": {
            "type": "message",
            "label": labelText,
            "text": actionText
        }
    }

# 已翻面的卡片
def flipped_card_template( labelText, cardState = "default" ,zoomRatio = 1 ):

    # 介面微調參數
    width = 64 * zoomRatio
    height = 88 * zoomRatio
    aspect_ratio = str(width) + ":" + str(height)
    width_px = str(width) + "px"
    height_px = str(height) + "px"
    if len(labelText) == 1:
        text_size = "xl"
    elif len(labelText) <= 3:
        text_size = "md"
    elif len(labelText) == 4: 
        text_size = "md"
        if get_char_width_ratio(labelText) == 8:
            labelText = labelText[0] + labelText[1] + "\n" + labelText[2] + labelText[3]
    elif len(labelText) <= 7:
        text_size = "md"
    else:
        text_size = "xs"

    # 卡片邊框
    if zoomRatio != 1:
        border_width = "5px"
    else:
        border_width = "4px"

    # 卡片狀態
    if cardState == "default":
        text_color = "#17656d"
        box_shadow = "#439aa8"
        border_color = "#66b9cc"
        card_front_img = localImg(f"randomShuffle/card_front.png")
    elif cardState == "transparent":
        text_color = "#17656d66"
        box_shadow = "#439aa8"
        border_color = "#66b9cc"
        card_front_img = localImg(f"randomShuffle/card_front.png")
    elif cardState == "active":
        text_color = "#6d2422"
        box_shadow = "#ad2d2a"
        border_color = "#dd524b"
        card_front_img = localImg(f"randomShuffle/card_front_active.png")


    return {
        "type": "box",
        "layout": "vertical",
        "width": width_px,
        "height": height_px,
        "contents": [
            # 卡片陰影
            {
                "type": "box",
                "layout": "vertical",
                "contents": [],
                "width": "100%",
                "height": "100%",
                "backgroundColor": box_shadow,
                "cornerRadius": "8px",
                "position": "absolute"
            },
            # 卡片底圖
            {
                "type": "box",
                "layout": "vertical",
                "position": "absolute",
                "width": "100%",
                "height": "95%",
                "cornerRadius": "8px",
                "backgroundColor": "#ffffff",
                "contents": [
                    {
                        "type": "image",
                        "url": card_front_img,
                        "size": "xl",
                        "aspectRatio": aspect_ratio,
                        "aspectMode": "cover"
                    }
                ],
            },
            # 卡片內容（正面文字）
            {
                "type": "box",
                "layout": "vertical",
                "width": "100%",
                "height": "95%",
                "position": "absolute",
                "paddingAll": "2px",
                "alignItems": "center",
                "justifyContent": "center",
                "contents": [
                    {
                        "type": "text",
                        "text": labelText,
                        "size": text_size,
                        "color": text_color,
                        "maxLines": 3,
                        "wrap": True,
                        "align": "center",
                        "weight": "bold",
                        "lineSpacing": "2px"
                    }
                ],
            },
            # 卡片邊框
            {
                "type": "box",
                "layout": "vertical",
                "width": "100%",
                "height": "95%",
                "borderWidth": border_width,
                "borderColor": border_color,
                "cornerRadius": "8px",
                "position": "absolute",
                "paddingAll": "0px",
                "alignItems": "center",
                "justifyContent": "center",
                "contents": [],
            },
        ],
        # "action": {
        #     "type": "message",
        #     "label": labelText,
        #     "text": actionText
        # }
    }