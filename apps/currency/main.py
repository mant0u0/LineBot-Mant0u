# 貨幣換算

from linebot import LineBotApi
from linebot.models import *

import os
import re
import requests
import json
from apps.common.common import *
from apps.currency.preprocess import extract_currency_conversion


line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))

# 定義貨幣
currency_dict = {
    'USD': {
        "name": "美元",
        "keyword": ['USD', '美金', '美元', '美幣'],
        "img": "",
    },
    'EUR': {
        "name": "歐元",
        "keyword": ['EUR', '歐元'],
        "img": "",
    },
    'JPY': {
        "name": "日圓",
        "keyword": ['JPY', '日圓', '日幣', '日元', '円'],
        "img": "",
    },
    'GBP': {
        "name": "英鎊",
        "keyword": ['GBP', '英鎊'],
        "img": "",
    },
    'HKD': {
        "name": "港幣",
        "keyword": ['HKD', '港幣', '港元'],
        "img": "",
    },
    'KRW': {
        "name": "韓元",
        "keyword": ['KRW', '韓幣', '韓元'],
        "img": "",
    },
    'CNY': {
        "name": "人民幣",
        "keyword": ['CNY', '人民幣'],
        "img": "",
    },
    'TWD': {
        "name": "新台幣",
        "keyword": ['TWD', '新台幣', '台幣'],
        "img": "",
    },
    'VND': {
        "name": "越南盾",
        "keyword": ['VND', '越南盾', '越南遁', '越南幣', '盾'],
        "img": "",
    },
    'BTC': {
        "name": "比特幣",
        "keyword": ['BTC', '比特幣'],
        "img": "",
    },
}


# 主要
def currencyMain(event, userMessage):
    
    # 貨幣：2000 日幣多少台幣
    currency_info = extract_currency_conversion(userMessage)

    if currency_info['state'] == 'success':

        # 原始貨幣、換算貨幣
        currency_original_type = currency_info["result"][0]
        currency_convert_type = currency_info["result"][1]

        # 原始數值、換算數值
        currency_original_value = currency_info["num"]
        currency_convert_value = currency_conversion({
            "original": currency_original_type,
            "convert": currency_convert_type,
            "value_str": currency_original_value,
        })

        # 數字轉換小數點後兩位，有千分位逗號的字串
        currency_original_float = float(currency_original_value)
        currency_convert_float = float(currency_convert_value)
        currency_original_value = "{:,.2f}".format(currency_original_float)
        currency_convert_value = "{:,.2f}".format(currency_convert_float)

        # 整理資料
        currency_data = {
            "model": "default",
            "original":{
                "value_float" : currency_original_float,
                "value_str" : currency_original_value,
                "type": currency_original_type,
            },
            "convert" :{
                "value_float" : currency_convert_float,
                "value_str" : currency_convert_value,
                "type": currency_convert_type,
            },
        }

        flexMessage_reply(event, currency_data)

# 打折
def currencyDiscount(event, userPostback):
    # 整理文字
    userPostback = userPostback.replace('貨幣打折：', '')
    discount_info = userPostback.split("、")
    # ['折數(0.9, 0.85...)','數值1','貨幣1','數值2','貨幣2']

    discount = float(discount_info[0])

    # 取得打折數值、取得相差值
    currency_original_discount = float(discount_info[1]) * discount
    currency_convert_discount = float(discount_info[3]) * discount
    currency_original_difference = float(discount_info[1]) - float(currency_original_discount)
    currency_convert_difference = float(discount_info[3]) - float(currency_convert_discount)
    
    # 數字轉換小數點後兩位，有千分位逗號的字串
    currency_original_discount = "{:,.2f}".format(float(currency_original_discount))
    currency_convert_discount = "{:,.2f}".format(float(currency_convert_discount))
    currency_original_difference = "{:,.2f}".format(float(currency_original_difference))
    currency_convert_difference = "{:,.2f}".format(float(currency_convert_difference))

    # 折扣文字
    discount_text = str( discount * 100 ).replace("0.0","").replace(".0","")
    discount_text = "打 "+ discount_text + " 折"

    # 整理資料
    currency_data = {
        "model": "discount",

        "original":{
            "value_float" : float(discount_info[1]),
            "value_str" : "{:,.2f}".format(float(discount_info[1])),
            "type": discount_info[2],
            "ratio" : discount_text,
            "discount": currency_original_discount,
            "difference" : currency_original_difference,
        },
        "convert" :{
            "value_float" : float(discount_info[3]),
            "value_str" : "{:,.2f}".format(float(discount_info[3])),
            "type": discount_info[4],
            "ratio" : discount_text,
            "discount": currency_convert_discount,
            "difference" : currency_convert_difference,
        },

    }

    flexMessage_reply(event, currency_data)

# 倍數
def currencyMultiple(event, userPostback):
    # 整理文字
    userPostback = userPostback.replace('貨幣倍率：', '')
    multiple_info = userPostback.split("、")
    # ['倍率(2,3,4,5...)','數值1','貨幣1','數值2','貨幣2']

    multiple = float(multiple_info[0])

    # 取得倍數數值、取得相差值
    currency_original_multiple = float(multiple_info[1]) * multiple
    currency_convert_multiple = float(multiple_info[3]) * multiple

    # 數字轉換小數點後兩位，有千分位逗號的字串
    currency_original_multiple = "{:,.2f}".format(float(currency_original_multiple))
    currency_convert_multiple = "{:,.2f}".format(float(currency_convert_multiple))

    # 倍率文字
    multiple_text = "買 " + str( int(multiple) ) + " 份"

    # 整理資料
    currency_data = {
        "model": "multiple",
        "original":{
            "value_float" : float(multiple_info[1]),
            "value_str" : "{:,.2f}".format(float(multiple_info[1])),
            "type": multiple_info[2],
            "ratio" : multiple_text,
            "multiple": currency_original_multiple,
        },
        "convert" :{
            "value_float" : float(multiple_info[3]),
            "value_str" : "{:,.2f}".format(float(multiple_info[3])),
            "type": multiple_info[4],
            "ratio" : multiple_text,
            "multiple": currency_convert_multiple,
        },
    }

    flexMessage_reply(event, currency_data)

# 平分
def currencyDivide(event, userPostback):
    # 整理文字
    userPostback = userPostback.replace('貨幣平分：', '')
    divide_info = userPostback.split("、")
    # ['份數(2,3,4,5...)','數值1','貨幣1','數值2','貨幣2']

    divide = int(divide_info[0])

    # 取得倍數數值、取得相差值
    currency_original_divide = float(divide_info[1]) / divide
    currency_convert_divide = float(divide_info[3]) / divide

    # 數字轉換小數點後兩位，有千分位逗號的字串
    currency_original_divide = "{:,.2f}".format(float(currency_original_divide))
    currency_convert_divide = "{:,.2f}".format(float(currency_convert_divide))

    # 份數文字
    divide_text = "分 " + str( divide ) + " 份"

    # 整理資料
    currency_data = {
        "model": "divide",
        "original":{
            "value_float" : float(divide_info[1]),
            "value_str" : "{:,.2f}".format(float(divide_info[1])),
            "type": divide_info[2],
            "ratio" : divide_text,
            "divide": currency_original_divide,
        },
        "convert" :{
            "value_float" : float(divide_info[3]),
            "value_str" : "{:,.2f}".format(float(divide_info[3])),
            "type": divide_info[4],
            "ratio" : divide_text,
            "divide": currency_convert_divide,
        },
    }

    flexMessage_reply(event, currency_data)

# 退稅
def currencyTax(event, userPostback):

    # 整理文字
    userPostback = userPostback.replace('貨幣退稅：', '')
    
    tax_info = userPostback.split("、")
    # ['折數(0.9, 0.85...)', '數值1', '貨幣1', '數值2', '貨幣2']

    tax = float(tax_info[0]) * 0.01 + 1

    # 取得退稅數值、取得相差值
    currency_original_tax = float(tax_info[1]) / tax
    currency_convert_tax = float(tax_info[3]) / tax
    currency_original_difference = float(tax_info[1]) - float(currency_original_tax)
    currency_convert_difference = float(tax_info[3]) - float(currency_convert_tax)
    
    # 數字轉換小數點後兩位，有千分位逗號的字串
    currency_original_tax = "{:,.2f}".format(float(currency_original_tax))
    currency_convert_tax = "{:,.2f}".format(float(currency_convert_tax))
    currency_original_difference = "{:,.2f}".format(float(currency_original_difference))
    currency_convert_difference = "{:,.2f}".format(float(currency_convert_difference))

    # 退稅文字
    tax_text = "退稅 "+ tax_info[0] + "%"

    # 整理資料
    currency_data = {
        "model": "tax",

        "original":{
            "value_float" : float(tax_info[1]),
            "value_str" : "{:,.2f}".format(float(tax_info[1])),
            "type": tax_info[2],
            "ratio" : tax_text,
            "tax": currency_original_tax,
            "difference" : currency_original_difference,
        },
        "convert" :{
            "value_float" : float(tax_info[3]),
            "value_str" : "{:,.2f}".format(float(tax_info[3])),
            "type": tax_info[4],
            "ratio" : tax_text,
            "tax": currency_convert_tax,
            "difference" : currency_convert_difference,
        },

    }

    flexMessage_reply(event, currency_data)


# 控制選單
def currencyControlMenu(event, userPostback):

    # 整理文字
    userPostback = userPostback.replace('貨幣：', '')
    num_list = [{ "num":"0", "label":"0" },]
    messageText = " "
    key_word =" "
    

    if userPostback.find('打折！') == 0:
        userPostback = userPostback.replace('打折！', '')
        messageText = "需要打幾折呢？"
        key_word = "貨幣打折"
        num_list = [
            { "num":"0.95", "label":"95 折" },
            { "num":"0.9",  "label":"9 折"  },
            { "num":"0.85", "label":"85 折" },
            { "num":"0.8",  "label":"8 折"  },
            { "num":"0.75", "label":"75 折" },
            { "num":"0.7",  "label":"7 折"  },
            { "num":"0.65", "label":"65 折" },
            { "num":"0.6",  "label":"6 折"  },
            { "num":"0.55", "label":"55 折" },
            { "num":"0.5",  "label":"5 折"  },
        ]


    if userPostback.find('倍率！') == 0:
        userPostback = userPostback.replace('倍率！', '')
        messageText = "需要多買幾份呢？"
        key_word = "貨幣倍率"
        num_list = [
            { "num":"2", "label":"2 份" },
            { "num":"3", "label":"3 份" },
            { "num":"4", "label":"4 份" },
            { "num":"5", "label":"5 份" },
            { "num":"6", "label":"6 份" },
            { "num":"7", "label":"7 份" },
            { "num":"8", "label":"8 份" },
            { "num":"9", "label":"9 份" },
            { "num":"10", "label":"10 份" },
            { "num":"11", "label":"11 份" },
            { "num":"12", "label":"12 份" },
        ]


    if userPostback.find('平分！') == 0:
        userPostback = userPostback.replace('平分！', '')
        messageText = "需要平分成幾份呢？"
        key_word = "貨幣平分"
        num_list = [
            { "num":"2", "label":"2 份" },
            { "num":"3", "label":"3 份" },
            { "num":"4", "label":"4 份" },
            { "num":"5", "label":"5 份" },
            { "num":"6", "label":"6 份" },
            { "num":"7", "label":"7 份" },
            { "num":"8", "label":"8 份" },
            { "num":"9", "label":"9 份" },
            { "num":"10", "label":"10 份" },
            { "num":"11", "label":"11 份" },
            { "num":"12", "label":"12 份" },
        ]

    quickReply_list = []
    for item in num_list:
        quickReply_item = QuickReplyButton(
                action=PostbackAction(
                label = item["label"], 
                data = f"{key_word}：{item['num']}、{userPostback}"
            )
        )
        quickReply_list.append( quickReply_item ) 

    
    # 包裝訊息
    text_message = TextSendMessage(
        text=messageText,
        quick_reply=QuickReply(
            items=quickReply_list
        )
    )
    # 發送訊息
    line_bot_api.reply_message(event.reply_token, text_message)


# 貨幣換算 API
def currency_conversion(currency):

    # 構建API的URL
    url = f"https://api.coinbase.com/v2/exchange-rates?currency={currency['original']}"

    try:
        # 發送GET請求
        response = requests.get(url)
        response.raise_for_status()  # 檢查是否有錯誤

        # 將回傳的JSON資料解析為Python物件
        data = json.loads(response.text)

        # 檢查回傳的資料是否包含目標貨幣
        if currency['convert'] in data['data']['rates']:
            
            # 取得目標貨幣的匯率
            rates = float(data['data']['rates'][currency['convert']])

            # 進行貨幣換算
            convert_value = float(currency['value_str']) * rates

            # 回傳換算後的金額
            return str(convert_value)
        else:
            print("目標貨幣不支援！")
            return "0"
    
    except requests.exceptions.RequestException as e:
        print(f"發生錯誤：{e}")
        return "0"

# 訊息模板
def pageTemplate(currency_data):

    pageTemplate_contents = []
    pageTemplate_body_contents = []
    # ======================================================================= #
    # 標題
    pageTemplate_body_title = {
        "type": "box",
        "layout": "horizontal",
        "paddingBottom": "6px",
        "contents": [
            {
                "type": "text",
                "text": "貨幣換算",
                "color": "#0A553A",
                "size": "lg",
                "weight": "bold",
                "flex": 0
            },
            {
                "type": "text",
                "text": "資料來源 Coinbase",
                "color": "#0A553A66",
                "size": "xs",
                # "weight": "bold",
                "margin": "8px",
                "gravity": "center",
                "align": "end",
                "offsetTop": "2px"
            }
        ],
    }
    # 向下箭頭
    pageTemplate_body_down_arrow =  {
        "type": "box",
        "layout": "vertical",
        "alignItems": "center",
        "paddingTop": "8px",
        "contents": [
            {
                "type": "image",
                # "url": "https://line-mant0u-bot-vercel.vercel.app/static/images/currency/down-arrow.png",
                "url": localImg("currency/down-arrow.png"),
                "size": "12px"
            }
        ],
    }
    # ======================================================================= #
    # 標題
    pageTemplate_body_contents.append( pageTemplate_body_title ) 

    # 原始貨幣
    pageTemplate_body_contents.extend( pageTemplate_currency( currency_data["original"], currency_data["model"] )) 
    # 箭頭
    pageTemplate_body_contents.append( pageTemplate_body_down_arrow ) 
    
    # 換算貨幣
    pageTemplate_body_contents.extend( pageTemplate_currency( currency_data["convert"], currency_data["model"] )) 
    # ======================================================================= #

    # 頂端 banner
    pageTemplate_banner = {
        "type": "image",
        "url": localImg("banner/currency.png"),
        "size": "100%",
        "aspectMode": "fit",
        "margin": "0px",
        "position": "relative",
        "aspectRatio": "1000:280"
    }
    pageTemplate_body = {
        "type": "box",
        "layout": "vertical",
        "contents": pageTemplate_body_contents,
        "paddingAll": "16px",
        "paddingTop": "8px"
    }

    # ======================================================================= #
    pageTemplate_contents.append( pageTemplate_banner ) 
    pageTemplate_contents.append( pageTemplate_body ) 
    # ======================================================================= #

    pageTemplate = {
        "type": "carousel",
        "contents": [
            {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "paddingAll": "0px",
                    "contents": pageTemplate_contents,
                }
            }
        ]
    }

    return pageTemplate

# 貨幣模板
def pageTemplate_currency( data, model ):

    # 貨幣數值（整數與小數部分）
    currency_value = data["value_str"]
    currency_value_int = currency_value.split('.')[0]
    currency_value_dec = "." + currency_value.split('.')[1]

    if model == "default":
        
        # 貨幣資訊
        currency_info = {
            "type": "box",
            "layout": "horizontal",
            "contents": [
                
                # 貨幣類型 (中文)
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                        "type": "text",
                        "text": currency_dict[data["type"]]["name"],
                        "color": "#0A553A",
                        "weight": "bold",
                        "size": "sm"
                        }
                    ],
                    "flex": 0
                }

            ],
            "paddingBottom": "4px",
            "paddingTop": "4px"
        }
        
        # 貨幣數值
        currency_num = {
            "type": "box",
            "layout": "baseline",
            "contents": [
                # 貨幣數值
                {
                    "type": "text",
                    "text": currency_value_int,
                    "color": "#0A553A",
                    "weight": "bold",
                    "align": "end",
                    "size": "xl"
                },
                # 貨幣數值（小數）
                {
                    "type": "text",
                    "text": currency_value_dec,
                    "color": "#0A553A99",
                    "weight": "bold",
                    "align": "end",
                    "size": "md",
                    "flex": 0,
                },
                # 貨幣類型 (英文)
                {
                    "type": "text",
                    "text": data["type"],
                    "color": "#0A553A",
                    "weight": "bold",
                    "align": "end",
                    "size": "md",
                    "flex": 0,
                    "margin": "8px"
                }
            ],
            "backgroundColor": "#F3F3F3",
            "paddingAll": "12px",
            "cornerRadius": "12px",
            "paddingBottom": "8px",
        }

        return currency_info, currency_num

    elif model == "discount":
        # 貨幣數值（整數與小數部分）
        currency_discount = data["discount"]
        currency_discount_int = currency_discount.split('.')[0]
        currency_discount_dec = "." + currency_discount.split('.')[1]

        # 貨幣資訊
        currency_info = {
            "type": "box",
            "layout": "horizontal",
            "contents": [
                
                # 貨幣類型 (中文)
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                        "type": "text",
                        "text": currency_dict[data["type"]]["name"],
                        "color": "#0A553A",
                        "weight": "bold",
                        "size": "sm"
                        }
                    ],
                    "flex": 0
                },

                # 有打折
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                        "type": "text",
                        "color": "#0A553A",
                        "weight": "bold",
                        "size": "sm",
                        "contents": [
                            {
                            "type": "span",
                            "text": data["value_str"],
                            "decoration": "line-through",
                            "color": "#0A553A99"
                            },
                            {
                            "type": "span",
                            "text": " · "
                            },
                            {
                            "type": "span",
                            "text": data["ratio"],
                            }
                        ]
                        }
                    ],
                    "alignItems": "flex-end"
                }
            ],
            "paddingBottom": "4px",
            "paddingTop": "4px"
        }
        
        # 貨幣數值
        currency_num = {
            "type": "box",
            "layout": "baseline",
            "contents": [
                # 貨幣數值
                {
                    "type": "text",
                    "text": currency_discount_int,
                    "color": "#0A553A",
                    "weight": "bold",
                    "align": "end",
                    "size": "xl"
                },
                # 貨幣數值（小數）
                {
                    "type": "text",
                    "text": currency_discount_dec,
                    "color": "#0A553A99",
                    "weight": "bold",
                    "align": "end",
                    "size": "md",
                    "flex": 0,
                },
                # 貨幣類型
                {
                    "type": "text",
                    "text": data["type"],
                    "color": "#0A553A",
                    "weight": "bold",
                    "align": "end",
                    "size": "md",
                    "flex": 0,
                    "margin": "8px"
                }
            ],
            "backgroundColor": "#F3F3F3",
            "paddingAll": "12px",
            "cornerRadius": "12px",
            "paddingBottom": "4px",
            "paddingTop": "8px"
        }
        
        # 貨幣相差統計
        currency_diff = {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                "type": "text",
                "text": f"便宜 {data['difference']} 元！",
                "color": "#0A553A88",
                "size": "sm",
                "weight": "bold",
                "align": "center"
                }
            ],
            "paddingTop": "6px"
        }

        return currency_info, currency_num, currency_diff
    
    elif model == "multiple":
        # 貨幣數值（整數與小數部分）
        currency_multiple = data["multiple"]
        currency_multiple_int = currency_multiple.split('.')[0]
        currency_multiple_dec = "." + currency_multiple.split('.')[1]

        # 貨幣資訊
        currency_info = {
            "type": "box",
            "layout": "horizontal",
            "contents": [
                
                # 貨幣類型 (中文)
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                        "type": "text",
                        "text": currency_dict[data["type"]]["name"],
                        "color": "#0A553A",
                        "weight": "bold",
                        "size": "sm"
                        }
                    ],
                    "flex": 0
                },

                # 有倍率
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                        "type": "text",
                        "color": "#0A553A",
                        "weight": "bold",
                        "size": "sm",
                        "contents": [
                            {
                            "type": "span",
                            "text": data["value_str"],
                            # "decoration": "line-through",
                            "color": "#0A553A99"
                            },
                            {
                            "type": "span",
                            "text": " · "
                            },
                            {
                            "type": "span",
                            "text": data["ratio"],
                            }
                        ]
                        }
                    ],
                    "alignItems": "flex-end"
                }
            ],
            "paddingBottom": "4px",
            "paddingTop": "4px"
        }
        
        # 貨幣數值
        currency_num = {
            "type": "box",
            "layout": "baseline",
            "contents": [
                # 貨幣數值
                {
                    "type": "text",
                    "text": currency_multiple_int,
                    "color": "#0A553A",
                    "weight": "bold",
                    "align": "end",
                    "size": "xl"
                },
                # 貨幣數值（小數）
                {
                    "type": "text",
                    "text": currency_multiple_dec,
                    "color": "#0A553A99",
                    "weight": "bold",
                    "align": "end",
                    "size": "md",
                    "flex": 0,
                },
                # 貨幣類型
                {
                    "type": "text",
                    "text": data["type"],
                    "color": "#0A553A",
                    "weight": "bold",
                    "align": "end",
                    "size": "md",
                    "flex": 0,
                    "margin": "8px"
                }
            ],
            "backgroundColor": "#F3F3F3",
            "paddingAll": "12px",
            "cornerRadius": "12px",
            "paddingBottom": "4px",
            "paddingTop": "8px"
        }

        return currency_info, currency_num
    
    elif model == "divide":
        # 貨幣數值（整數與小數部分）
        currency_divide   = data["divide"]
        currency_divide_int   = currency_divide.split('.')[0]  
        currency_divide_dec   = "." + currency_divide.split('.')[1] 

        # 貨幣資訊
        currency_info = {
            "type": "box",
            "layout": "horizontal",
            "contents": [
                
                # 貨幣類型 (中文)
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                        "type": "text",
                        "text": currency_dict[data["type"]]["name"],
                        "color": "#0A553A",
                        "weight": "bold",
                        "size": "sm"
                        }
                    ],
                    "flex": 0
                },

                # 有倍率
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                        "type": "text",
                        "color": "#0A553A",
                        "weight": "bold",
                        "size": "sm",
                        "contents": [
                            {
                            "type": "span",
                            "text": data["value_str"],
                            "decoration": "line-through",
                            "color": "#0A553A99"
                            },
                            {
                            "type": "span",
                            "text": " · "
                            },
                            {
                            "type": "span",
                            "text": data["ratio"],
                            }
                        ]
                        }
                    ],
                    "alignItems": "flex-end"
                }
            ],
            "paddingBottom": "4px",
            "paddingTop": "4px"
        }
        
        # 貨幣數值
        currency_num = {
            "type": "box",
            "layout": "baseline",
            "contents": [
                # 貨幣數值
                {
                    "type": "text",
                    "text": currency_divide_int,
                    "color": "#0A553A",
                    "weight": "bold",
                    "align": "end",
                    "size": "xl"
                },
                # 貨幣數值（小數）
                {
                    "type": "text",
                    "text": currency_divide_dec,
                    "color": "#0A553A99",
                    "weight": "bold",
                    "align": "end",
                    "size": "md",
                    "flex": 0,
                },
                # 貨幣類型
                {
                    "type": "text",
                    "text": data["type"],
                    "color": "#0A553A",
                    "weight": "bold",
                    "align": "end",
                    "size": "md",
                    "flex": 0,
                    "margin": "8px"
                }
            ],
            "backgroundColor": "#F3F3F3",
            "paddingAll": "12px",
            "cornerRadius": "12px",
            "paddingBottom": "4px",
            "paddingTop": "8px"
        }

        return currency_info, currency_num
    
    elif model == "tax":
        # 貨幣數值（整數與小數部分）
        currency_tax = data["tax"]
        currency_tax_int = currency_tax.split('.')[0]
        currency_tax_dec = "." + currency_tax.split('.')[1]

        # 貨幣資訊
        currency_info = {
            "type": "box",
            "layout": "horizontal",
            "contents": [
                
                # 貨幣類型 (中文)
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                        "type": "text",
                        "text": currency_dict[data["type"]]["name"],
                        "color": "#0A553A",
                        "weight": "bold",
                        "size": "sm"
                        }
                    ],
                    "flex": 0
                },

                # 有打折
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                        "type": "text",
                        "color": "#0A553A",
                        "weight": "bold",
                        "size": "sm",
                        "contents": [
                            {
                            "type": "span",
                            "text": data["value_str"],
                            "decoration": "line-through",
                            "color": "#0A553A99"
                            },
                            {
                            "type": "span",
                            "text": " · "
                            },
                            {
                            "type": "span",
                            "text": data["ratio"],
                            }
                        ]
                        }
                    ],
                    "alignItems": "flex-end"
                }
            ],
            "paddingBottom": "4px",
            "paddingTop": "4px"
        }
        
        # 貨幣數值
        currency_num = {
            "type": "box",
            "layout": "baseline",
            "contents": [
                # 貨幣數值
                {
                    "type": "text",
                    "text": currency_tax_int,
                    "color": "#0A553A",
                    "weight": "bold",
                    "align": "end",
                    "size": "xl"
                },
                # 貨幣數值（小數）
                {
                    "type": "text",
                    "text": currency_tax_dec,
                    "color": "#0A553A99",
                    "weight": "bold",
                    "align": "end",
                    "size": "md",
                    "flex": 0,
                },
                # 貨幣類型
                {
                    "type": "text",
                    "text": data["type"],
                    "color": "#0A553A",
                    "weight": "bold",
                    "align": "end",
                    "size": "md",
                    "flex": 0,
                    "margin": "8px"
                }
            ],
            "backgroundColor": "#F3F3F3",
            "paddingAll": "12px",
            "cornerRadius": "12px",
            "paddingBottom": "4px",
            "paddingTop": "8px"
        }
        
        # 貨幣相差統計
        currency_diff = {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                "type": "text",
                "text": f"退稅 {data['difference']} 元！",
                "color": "#0A553A88",
                "size": "sm",
                "weight": "bold",
                "align": "center"
                }
            ],
            "paddingTop": "6px"
        }

        return currency_info, currency_num, currency_diff


# 包裝訊息，發送訊息
def flexMessage_reply(event, currency_data):
    quickReplyText = f"{str(currency_data['original']['value_float'])}、{currency_data['original']['type']}、{str(currency_data['convert']['value_float'])}、{currency_data['convert']['type']}"

    quickReply_list = []
    
    if currency_data["original"]["type"] == "JPY":
        quickReply_item = QuickReplyButton(
                image_url= localImg('currency/icon-percent.png'),
                action=PostbackAction(
                label = "退稅 10%", 
                data = f"貨幣退稅：10、{quickReplyText}"
            )
        )
        quickReply_list.append( quickReply_item ) 




    quickReply_item = QuickReplyButton(
                        image_url= localImg('currency/icon-percent.png'),
                        action=PostbackAction(
                        label = "打折優惠", 
                        data = f"貨幣：打折！{quickReplyText}")
                    ), QuickReplyButton(
                        image_url= localImg('currency/icon-division.png'),
                        action=PostbackAction(
                        label = "平均分攤", 
                        data = f"貨幣：平分！{quickReplyText}")
                    ), QuickReplyButton(
                        image_url= localImg('currency/icon-multiplication.png'),
                        action=PostbackAction(
                        label = "多買幾件", 
                        data = f"貨幣：倍率！{quickReplyText}")
                    )
    quickReply_list.extend( quickReply_item ) 

    # 包裝訊息
    flex_message = FlexSendMessage(
        alt_text='貨幣換算',
        contents= pageTemplate(currency_data),
        quick_reply=QuickReply(
            items=quickReply_list
        )
    )

    # 發送訊息
    line_bot_api.reply_message(event.reply_token, flex_message)