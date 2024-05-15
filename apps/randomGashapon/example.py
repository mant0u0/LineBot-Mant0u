# 扭蛋機（範例介面）
from linebot import LineBotApi
from linebot.models import *

import os
from apps.common.common import *


line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))

def randomGashaponExample(event):
    # 包裝訊息
    flex_message = FlexSendMessage(
        alt_text='有人在玩扭蛋！',
        contents={
            # JSON 格式貼這邊
            "type": "carousel",
            "contents": [

                # 第一頁 (pageTemplate)
                {
                    "type": "bubble",
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            # 扭蛋結果圖片
                            {
                                "type": "image",
                                "url": localImg("randomGashapon/Set.png"),
                                "size": "full",
                                "aspectMode": "cover",
                                "aspectRatio": "1:1",
                                "gravity": "center"
                            },
                            # 扭蛋結果文字
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
                                                        "text": "扭蛋扭出...",
                                                        "size": "lg",
                                                        "color": "#0f5560",
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
                            "text": "扭蛋機"
                        },
                    }


                },
                
                # 第二頁、扭蛋內容 (pageTemplate)
                {
                    "type": "bubble",
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        # 背景
                        {
                            "type": "image",
                            "url": localImg("randomGashapon/BG.png"),
                            "aspectRatio": "1:1",
                            "size": "full"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                            # 標題
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                {
                                    "type": "text",
                                    "text": "扭蛋機內容物",
                                    "color": "#0f5560",
                                    "weight": "bold",
                                    "size": "md"
                                }
                                ],
                                "alignItems": "center",
                                "paddingBottom": "4px",
                                "paddingTop": "8px"
                            },
                            # 第一列
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                # 項目
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                    {
                                        "type": "image",
                                        "url": localImg("randomGashapon/Gashapon.png"),
                                        "size": "40px",
                                        "aspectRatio": "1:1"
                                    },
                                    {
                                        "type": "text",
                                        "text": "文字文字文文",
                                        "color": "#0f5560",
                                        "weight": "bold",
                                        "size": "xs",
                                        "maxLines": 1,
                                        "align": "center"
                                    },
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                        {
                                            "type": "text",
                                            "text": "1",
                                            "color": "#ffffff",
                                            "weight": "bold",
                                            "size": "xs"
                                        }
                                        ],
                                        "position": "absolute",
                                        "backgroundColor": "#ff7171",
                                        "cornerRadius": "xxl",
                                        "width": "24px",
                                        "height": "24px",
                                        "justifyContent": "center",
                                        "alignItems": "center",
                                        "offsetTop": "0px",
                                        "offsetEnd": "12px"
                                    }
                                    ],
                                    "alignItems": "center",
                                    "justifyContent": "center",
                                    "width": "33%",
                                    "paddingAll": "4px",
                                    "spacing": "6px",
                                    "action": {
                                    "type": "message",
                                    "label": "action",
                                    "text": "hello"
                                    },
                                    "paddingTop": "8px"
                                },
                                
                                # 項目
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                    {
                                        "type": "image",
                                        "url": localImg("randomGashapon/Gashapon.png"),
                                        "size": "40px",
                                        "aspectRatio": "1:1"
                                    },
                                    {
                                        "type": "text",
                                        "text": "文字文字文文",
                                        "color": "#0f5560",
                                        "weight": "bold",
                                        "size": "xs",
                                        "maxLines": 1,
                                        "align": "center"
                                    },
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                        {
                                            "type": "text",
                                            "text": "1",
                                            "color": "#ffffff",
                                            "weight": "bold",
                                            "size": "xs"
                                        }
                                        ],
                                        "position": "absolute",
                                        "backgroundColor": "#ff7171",
                                        "cornerRadius": "xxl",
                                        "width": "24px",
                                        "height": "24px",
                                        "justifyContent": "center",
                                        "alignItems": "center",
                                        "offsetTop": "0px",
                                        "offsetEnd": "12px"
                                    }
                                    ],
                                    "alignItems": "center",
                                    "justifyContent": "center",
                                    "width": "33%",
                                    "paddingAll": "4px",
                                    "spacing": "6px",
                                    "action": {
                                    "type": "message",
                                    "label": "action",
                                    "text": "hello"
                                    },
                                    "paddingTop": "8px"
                                },
                                
                                # 項目
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                    {
                                        "type": "image",
                                        "url": localImg("randomGashapon/Gashapon.png"),
                                        "size": "40px",
                                        "aspectRatio": "1:1"
                                    },
                                    {
                                        "type": "text",
                                        "text": "文字文字文文",
                                        "color": "#0f5560",
                                        "weight": "bold",
                                        "size": "xs",
                                        "maxLines": 1,
                                        "align": "center"
                                    },
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                        {
                                            "type": "text",
                                            "text": "1",
                                            "color": "#ffffff",
                                            "weight": "bold",
                                            "size": "xs"
                                        }
                                        ],
                                        "position": "absolute",
                                        "backgroundColor": "#ff7171",
                                        "cornerRadius": "xxl",
                                        "width": "24px",
                                        "height": "24px",
                                        "justifyContent": "center",
                                        "alignItems": "center",
                                        "offsetTop": "0px",
                                        "offsetEnd": "12px"
                                    }
                                    ],
                                    "alignItems": "center",
                                    "justifyContent": "center",
                                    "width": "33%",
                                    "paddingAll": "4px",
                                    "spacing": "6px",
                                    "action": {
                                    "type": "message",
                                    "label": "action",
                                    "text": "hello"
                                    },
                                    "paddingTop": "8px"
                                }
                                ]
                            },
                            # 第二列
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                    {
                                        "type": "image",
                                        "url": localImg("randomGashapon/Gashapon.png"),
                                        "size": "40px",
                                        "aspectRatio": "1:1"
                                    },
                                    {
                                        "type": "text",
                                        "text": "文字文字文文",
                                        "color": "#0f5560",
                                        "weight": "bold",
                                        "size": "xs",
                                        "maxLines": 1,
                                        "align": "center"
                                    },
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                        {
                                            "type": "text",
                                            "text": "99",
                                            "color": "#ffffff",
                                            "weight": "bold",
                                            "size": "xs"
                                        }
                                        ],
                                        "position": "absolute",
                                        "backgroundColor": "#ff7171",
                                        "cornerRadius": "xxl",
                                        "width": "24px",
                                        "height": "24px",
                                        "justifyContent": "center",
                                        "alignItems": "center",
                                        "offsetTop": "0px",
                                        "offsetEnd": "12px"
                                    }
                                    ],
                                    "alignItems": "center",
                                    "justifyContent": "center",
                                    "width": "33%",
                                    "paddingAll": "4px",
                                    "spacing": "6px",
                                    "action": {
                                    "type": "message",
                                    "label": "action",
                                    "text": "hello"
                                    },
                                    "paddingTop": "8px"
                                },
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                    {
                                        "type": "image",
                                        "url": localImg("randomGashapon/Gashapon.png"),
                                        "size": "40px",
                                        "aspectRatio": "1:1"
                                    },
                                    {
                                        "type": "text",
                                        "text": "文字文字文文",
                                        "color": "#0f5560",
                                        "weight": "bold",
                                        "size": "xs",
                                        "maxLines": 1,
                                        "align": "center"
                                    },
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                        {
                                            "type": "text",
                                            "text": "1",
                                            "color": "#ffffff",
                                            "weight": "bold",
                                            "size": "xs"
                                        }
                                        ],
                                        "position": "absolute",
                                        "backgroundColor": "#ff7171",
                                        "cornerRadius": "xxl",
                                        "width": "24px",
                                        "height": "24px",
                                        "justifyContent": "center",
                                        "alignItems": "center",
                                        "offsetTop": "0px",
                                        "offsetEnd": "12px"
                                    }
                                    ],
                                    "alignItems": "center",
                                    "justifyContent": "center",
                                    "width": "33%",
                                    "paddingAll": "4px",
                                    "spacing": "6px",
                                    "action": {
                                    "type": "message",
                                    "label": "action",
                                    "text": "hello"
                                    },
                                    "paddingTop": "8px"
                                },
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                    {
                                        "type": "image",
                                        "url": localImg("randomGashapon/Gashapon.png"),
                                        "size": "40px",
                                        "aspectRatio": "1:1"
                                    },
                                    {
                                        "type": "text",
                                        "text": "文字文字文文",
                                        "color": "#0f5560",
                                        "weight": "bold",
                                        "size": "xs",
                                        "maxLines": 1,
                                        "align": "center"
                                    },
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                        {
                                            "type": "text",
                                            "text": "1",
                                            "color": "#ffffff",
                                            "weight": "bold",
                                            "size": "xs"
                                        }
                                        ],
                                        "position": "absolute",
                                        "backgroundColor": "#ff7171",
                                        "cornerRadius": "xxl",
                                        "width": "24px",
                                        "height": "24px",
                                        "justifyContent": "center",
                                        "alignItems": "center",
                                        "offsetTop": "0px",
                                        "offsetEnd": "12px"
                                    }
                                    ],
                                    "alignItems": "center",
                                    "justifyContent": "center",
                                    "width": "33%",
                                    "paddingAll": "4px",
                                    "spacing": "6px",
                                    "action": {
                                    "type": "message",
                                    "label": "action",
                                    "text": "hello"
                                    },
                                    "paddingTop": "8px"
                                }
                                ]
                            }
                            ],
                            "position": "absolute",
                            "width": "100%",
                            "height": "100%",
                            "paddingAll": "16px"
                        }
                        ],
                        "paddingAll": "0px",
                        "position": "relative"
                    }
                }
            
            

            ]
            }
    )
    # 發送訊息
    line_bot_api.reply_message(event.reply_token, flex_message)












