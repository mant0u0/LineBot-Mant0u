from apps.common.common import *

# 抽籤結果 pageTemplate
def random_tarotCards_first_page_template(result_img_url, result_text):
    page_template = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                # 背景
                {
                    "type": "image",
                    "url": localImg("randomTarotCards/BG.png"),
                    "size": "full",
                    "aspectMode": "cover",
                    "aspectRatio": "1:1",
                    "gravity": "center"
                },

                # 陰影
                {
                    "type": "box",
                    "layout": "vertical",
                    "position": "absolute",
                    "width": "100%",
                    "height": "75%",
                    "justifyContent": "center",
                    "alignItems": "center",
                    "contents": [
						{
							"type": "image",
							"url": localImg("randomTarotCards/shadow.png"),
							"size": "3xl"
						}
                    ],
                },

                # 卡片
                {
                    "type": "box",
                    "layout": "vertical",
                    "position": "absolute",
                    "width": "100%",
                    "height": "75%",
                    "justifyContent": "center",
                    "alignItems": "center",
                    "contents": [
						{
							"type": "image",
							"url": result_img_url,
							"size": "3xl"
						}
                    ],
                },

                # 文字
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
                                            "text": result_text,
                                            "size": "lg",
                                            "color": "#222d53",
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
            "paddingAll": "0px",
            # "action": {
            #     "type": "message",
            #     "label": "action",
            #     "text": "塔羅牌"
            # },
        }
    }

    return page_template

# 運勢分析結果 pageTemplate
def random_tarotCards_fortune_page_template( result_text, result_text_fortune, userMessage ):
    
	if userMessage == "我的運勢":
		fortune_contents = [
			{
				"type": "text",
				"text": f"✦ {result_text} ✦",
				"size": "lg",
				"weight": "bold",
				"color": "#222d53",
			},
			{
				"type": "text",
				"text": result_text_fortune,
				"size": "md",
				"weight": "bold",
				"wrap": True,
				"lineSpacing": "4px",
				"margin": "12px",
				"color": "#222d53aa"
			}
		]

	else:
		fortune_contents = [
			{
				"type": "text",
				"text": f"✦ {result_text} ✦",
				"size": "lg",
				"weight": "bold",
				"color": "#222d53",
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
				"color": "#222d53",
			},
			{
				"type": "text",
				"text": result_text_fortune,
				"size": "md",
				"weight": "bold",
				"wrap": True,
				"lineSpacing": "4px",
				"margin": "12px",
				"color": "#222d53aa"
			}
		]

	page_template = {
		"type": "bubble",
		"body": {
			"type": "box",
			"layout": "vertical",
			"contents": [
				# 背景
				{
					"type": "image",
					"url": localImg("randomTarotCards/BG_text.png"),
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
					"contents": fortune_contents,

				}
			],
			"paddingAll": "0px"
		}
	}

	return page_template
