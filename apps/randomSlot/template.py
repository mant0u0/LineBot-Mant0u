from apps.common.common import *

# slot page_template
def random_slot_page_template(slot_layout, connected_elements):

    # slot 版面列印
    bubble_contents = []

    # 背景
    slotBg = {
        "type": "image",
        "url": localImg(f"randomSlot/bg/1.png"),
        "size": "full",
        "aspectMode": "cover",
        "aspectRatio": "1:1",
    }
    bubble_contents.append(slotBg)

    # 項目
    for col in range(3):
        for row in range(3):
            slotItem = {
                "type": "image",
                "url": localImg("randomSlot/"+str(col)+str(row)+"/"+str(slot_layout[col][row])+".png"),
                "size": "full",
                "aspectMode": "cover",
                "aspectRatio": "1:1",
                "position": "absolute",
            }
            bubble_contents.append(slotItem)

    # 文字
    if len(connected_elements) == 0:
        slotText = {
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
                            "layout": "baseline",
                            "justifyContent": "center",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": " 沒有任何連線～",
                                    "size": "lg",
                                    "color": "#93563b",
                                    "weight": "bold",
                                    "flex": 0,
                                }
                            ],
                        }
                    ],
                }
            ],
        }
        bubble_contents.append(slotText)
    else:
        slotText = {
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
                            "layout": "baseline",
                            "justifyContent": "center",
                            "contents": [
                                {
                                    "type": "icon",
                                    "size": "xxl",
                                    "url": localImg("randomSlot/icon/"+str(connected_elements[0])+".png"),
                                    "offsetTop": "8px",
                                },
                                {
                                    "type": "text",
                                    "text": " 出現連線了！",
                                    "size": "lg",
                                    "color": "#93563b",
                                    "weight": "bold",
                                    "flex": 0,
                                }
                            ],
                        }
                    ],
                }
            ],
        }
        bubble_contents.append(slotText)

    # flexMessage 一頁的內容
    page_template = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": bubble_contents,
            "paddingAll": "0px",
            "action": {
                "type": "message",
                "label": "action",
                "text": "拉霸"
            },
        }
    }

    return page_template