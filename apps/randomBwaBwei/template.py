# 擲筊結果 pageTemplate
def random_bwabwei_first_page_template(result_img_url, result_data):
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
                                            "text": result_data["text"],
                                            "size": "lg",
                                            "color": "#c93a38",
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
                "text": "擲筊"
            },
        }
    }

    return page_template



# 運勢分析結果 pageTemplate
def random_bwabwei_fortune_page_template( result_bg_img_url, result_icon_img_url, result_fortune ):
    page_template = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
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
                    "contents": [
                        {
                            "type": "image",
                            "url": result_icon_img_url,
                            "size": "xxs",
                        },
                        {
                            "type": "text",
                            "text": result_fortune,
                            "color": "#c93a38",
                            "wrap": True,
                            "size": "md",
                            "weight": "bold",
                            "lineSpacing": "8px",
                            "margin": "lg",
                        },
                        {
                            "type": "text",
                            "text": "　",
                            "wrap": True,
                            "size": "md",
                            "weight": "bold",
                            "lineSpacing": "8px",
                            "margin": "md",
                        }
                    ],
                    "position": "absolute",
                    "width": "100%",
                    "height": "100%",
                    "justifyContent": "center",
                    "alignItems": "center",
                    "paddingAll": "12%"
                }
            ],
            "paddingAll": "0px"
        }
    }

    return page_template


