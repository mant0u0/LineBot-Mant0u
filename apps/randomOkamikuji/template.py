
# 抽籤結果 page_template
def random_okamikuji_first_page_template( result ):

    result_text = result["page_text"]
    result_color = result["color"]
    result_img_url  = result["first_page_img_url"]

    page_template = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "image",
                    "url": result_img_url,
                    "size": "full",
                    "aspectMode": "cover",
                    "aspectRatio": "1:1",
                    "gravity": "center"
                },
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
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": result_text,
                                            "size": "lg",
                                            "color": result_color,
                                            "weight": "bold",
                                            "align": "center"
                                        }
                                    ]
                                }
                            ],
                            "spacing": "xs"
                        }
                    ],
                }
            ],
            "paddingAll": "0px",
            "action": {
                "type": "message",
                "label": "action",
                "text": "抽籤"
            },
        }
    }

    return page_template

# 運勢分析結果 page_template
def random_okamikuji_fortune_page_template( result, fortune, userMessage ):
    
    result_name = result["result_name"]
    result_color = result["color"]
    result_bg_img_url  = result["fortune_page_img_url"]
    
    page_template = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "paddingAll": "0px",
            "contents": [
                {
                    "type": "image",
                    "url": result_bg_img_url,
                    "size": "full",
                    "aspectMode": "cover",
                    "aspectRatio": "1:1"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "position": "absolute",
                    "width": "100%",
                    "height": "100%",
                    "justifyContent": "center",
                    "alignItems": "center",
                    "paddingAll": "12%",
                    "contents": [
                        {
                            "type": "text",
                            "text": "【 " + result_name + " 】",
                            "size": "xxl",
                            "weight": "bold",
                            "color": result_color
                        },
                        {
                            "type": "text",
                            "text": userMessage,
                            "size": "md",
                            "weight": "bold",
                            "wrap": True,
                            "lineSpacing": "4px",
                            "margin": "12px",
                            "align": "center",
                            "color": result_color
                        },
                        {
                            "type": "text",
                            "text": fortune,
                            "size": "md",
                            "weight": "bold",
                            "wrap": True,
                            "lineSpacing": "4px",
                            "margin": "12px",
                            "color": result_color + "aa"
                        }

                    ],

                }
            ],

        }
    }

    return page_template