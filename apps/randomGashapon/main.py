# 扭蛋機

from linebot import LineBotApi
from linebot.models import *

import os
import random
import re
from apps.common.common import *
from apps.common.database import *


line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))

# 主要
def randomGashaponPlay(event):

    # flex message 訊息容器
    flex_message_contents = []

    # 取得扭蛋機內容物
    gashapon_contents = get_gashapon_list(event)
    
    if len(gashapon_contents) == 0:
        # text_message = TextSendMessage(text="扭蛋機現在沒有任何扭蛋！")
        # line_bot_api.reply_message(event.reply_token, text_message)
        gashapon_result = ""
        gashapon_info = {
            "text" : "扭蛋機目前沒有扭蛋！",
            "img": localImg(f"randomGashapon/Null.png"),
        }
    else:
        # 扭蛋機結果
        gashapon_result = random.choice(gashapon_contents) # 從陣列中隨機取一個元素
        gashapon_text = f"扭蛋為 {gashapon_result} ！"
        gashapon_img = str(random.randint(1, 5)) + ".png"
        gashapon_info = {
            "text" : gashapon_text,
            "img": localImg(f"randomGashapon/{gashapon_img}"),
        }

    # 結果顯示
    pageTemplate = pageTemplate_result(gashapon_info)
    flex_message_contents.append( pageTemplate )

    # 內容物：最後一個加一個「新增」按鈕
    gashapon_contents.append( "{{{新增按鈕}}}" )
    # 內容物顯示：陣列分成 9 個一組的子陣列
    gashapon_contents = [gashapon_contents[i:i+9] for i in range(0, len(gashapon_contents), 9)]
    for page_contents in gashapon_contents:
        pageTemplate_c = pageTemplate_contents(page_contents)
        flex_message_contents.append( pageTemplate_c )

    flexMessage_reply(event, flex_message_contents, gashapon_result)

# 新增
def randomGashaponAdd(event, userMessage):
    
    if userMessage.find('扭蛋重置新增：') == 0:
        randomGashaponReset(event)
    
    # 整理文字
    userMessage = userMessage.replace('扭蛋重置新增：', '')
    userMessage = userMessage.replace('扭蛋新增：', '')
    gashapon_list = re.split(r'[；，、;,]', userMessage)   # 字串分割
    gashapon_list = [x.strip() for x in gashapon_list if x.strip()] # 去除空白元素並移除開頭空白鍵

    source_id = getMessageSourceID(event)   # 取得訊息來源 ID
    file_path = 'randomGashapon'  # 選擇存取的檔案路徑

    # 讀取檔案
    try:
        record_data = read_database_combined(file_path, source_id)
        record_data["list"] = record_data["list"] + gashapon_list  # 追加元素
        record_data["list"] = list(set(record_data["list"]))       # 清除重複元素
        record_data["state"] = "default"
    # 如果沒有就新增一個
    except:
        record_data = {
            "list": gashapon_list,
            "state" : "default",
        }

    # 寫入 JSON 檔案
    write_database_combined(file_path, source_id, record_data)

    gashapon_info = {
        "text" : "扭蛋機新增成功！",
        "img": localImg("randomGashapon/Set.png"),
    }
    gashapon_contents = record_data["list"]


    # 結果顯示
    flex_message_contents = []
    pageTemplate = pageTemplate_result(gashapon_info)
    flex_message_contents.append( pageTemplate )


    # 內容物：最後一個加一個「新增」按鈕
    gashapon_contents.append( "{{{新增按鈕}}}" )
    # 內容物顯示：陣列分成 9 個一組的子陣列
    gashapon_contents = [gashapon_contents[i:i+9] for i in range(0, len(gashapon_contents), 9)]
    for page_contents in gashapon_contents:
        pageTemplate_c = pageTemplate_contents(page_contents)
        flex_message_contents.append( pageTemplate_c )

    flexMessage_reply(event, flex_message_contents, "")

# 新增按鈕點擊
def randomGashaponAddBtnClick(event):
    source_id = getMessageSourceID(event)   # 取得訊息來源 ID
    file_path = 'randomGashapon'  # 選擇存取的檔案路徑

    # 讀取檔案
    try:
        record_data = read_database_combined(file_path, source_id)
        record_data["state"] = "add"
    
    # 如果沒有就新增一個
    except:
        record_data = {
            "list": [],
            "state" : "add",
        }

    # 寫入 JSON 檔案
    write_database_combined(file_path, source_id, record_data)

    # 包裝訊息
    flex_message_contents = []
    pageTemplate = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "paddingAll": "16px",
            "contents": [
                {
                    "type": "text",
                    "text": "想新增什麼扭蛋呢？",
                    "weight": "bold",
                    "size": "lg",
                    "align": "center",
                    "color": "#043b4a"
                },
                {
                    "type": "text",
                    "text": f"請直接輸入文字新增\n使用全形頓號「、」隔開不同項目",
                    "weight": "bold",
                    "size": "sm",
                    "align": "center",
                    "color": "#043b4aaa",
                    "margin": "8px",
                    "wrap": True,
                    "lineSpacing": "4px"
                },
            ],

        }
    }

    flex_message_contents.append( pageTemplate )
    flex_message = FlexSendMessage(
        alt_text= '有人在玩扭蛋機！',
        contents={
            "type": "carousel",
            "contents": flex_message_contents
        }
    )

    # 發送訊息
    line_bot_api.reply_message(event.reply_token, flex_message)

# 選擇
def randomGashaponSelect(event, userPostback):

    # 整理文字
    userPostback = userPostback.replace('扭蛋選擇：', '')

    # 包裝訊息
    text_message = TextSendMessage(
        text=f"選擇了「{userPostback}」！",
        quick_reply=QuickReply(
            items=[
                QuickReplyButton(
                    action=MessageAction(label = "● 移除項目", text = f"扭蛋移除：{userPostback}")
                ),
            ]
        )
    )
    # 發送訊息
    line_bot_api.reply_message(event.reply_token, text_message)

# 移除
def randomGashaponRemove(event, userMessage):
    
    # 整理文字
    userMessage = userMessage.replace('扭蛋移除：', '')

    source_id = getMessageSourceID(event)   # 取得訊息來源 ID
    file_path = 'randomGashapon'  # 選擇存取的檔案路徑

    # 讀取檔案
    try:
        # 讀取檔案、移除
        record_data = read_database_combined(file_path, source_id)
        record_data["list"].remove(userMessage)

        # 寫入 JSON 檔案
        write_database_combined(file_path, source_id, record_data)

        # 包裝訊息
        text_message = TextSendMessage(
            text=f"「{userMessage}」從扭蛋機中移除了！",
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        action=MessageAction(label = "● 進行扭蛋", text = "扭蛋機")
                    ),
                    QuickReplyButton(
                        action=PostbackAction(label = "○ 新增扭蛋", data = "扭蛋新增！" )
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, text_message)


    # 沒有這個東西
    except:
        text_message = TextSendMessage(text=f"扭蛋機中沒有「{userMessage}」這個東西！")
        line_bot_api.reply_message(event.reply_token, text_message)

# 重置
def randomGashaponReset(event):
    
    source_id = getMessageSourceID(event)   # 取得訊息來源 ID
    file_path = 'randomGashapon'  # 選擇存取的檔案路徑
    # 讀取檔案
    try:
        # 讀取檔案、移除
        record_data = read_database_combined(file_path, source_id)
        
        record_data["list"] = []
        record_data["state"] = "default"
        
        # 寫入 JSON 檔案
        write_database_combined(file_path, source_id, record_data)
    except:
        return

# 取得扭蛋內容物
def get_gashapon_list(event):

    source_id = getMessageSourceID(event)   # 取得訊息來源 ID
    file_path = 'randomGashapon'  # 選擇存取的檔案路徑
    
    # 讀取檔案
    try:
        record_data = read_database_combined(file_path, source_id)

        gashapon_list = record_data["list"]
        return gashapon_list

    except:
        gashapon_list = []
        return gashapon_list

# 檢查扭蛋機新增狀態是否被開啟
def checkGashaponJson(event, userMessage):
    try:
        source_id = getMessageSourceID(event)   # 取得訊息來源 ID
        file_path = 'randomGashapon'  # 選擇存取的檔案路徑

        # 讀取檔案
        record_data = read_database_combined(file_path, source_id)

        if record_data["state"] == "add": 
            # userMessage = "扭蛋新增："+ userMessage
            # randomGashaponAdd(event, userMessage)
            randomGashaponAddCheck(event, userMessage)

            # 取消『新增』狀態
            record_data["state"] = "default"
            write_database_combined(file_path, source_id, record_data)

        print('[訊息] 扭蛋機新增狀態 已開啟')
    except:
        print('[訊息] 扭蛋機新增狀態 未開啟')
        return

# 確認新增狀態
def randomGashaponAddCheck(event, userMessage):

    # 整理文字
    gashapon_list = re.split(r'[；，、;,]', userMessage)   # 字串分割
    gashapon_list = [x.strip() for x in gashapon_list if x.strip()] # 去除空白元素並移除開頭空白鍵
    gashapon_list_text = str("、".join(gashapon_list))
    gashapon_list_len = str( len(gashapon_list) )

    # 包裝訊息
    flex_message_contents = []
    pageTemplate = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "paddingAll": "16px",
            "contents": [
                {
                    "type": "text",
                    "text": "扭蛋機新增",
                    "weight": "bold",
                    "size": "lg",
                    "align": "center",
                    "color": "#043b4a"
                },
                {
                    "type": "text",
                    "text": f"你確定要新增這些扭蛋項目？\n共 {gashapon_list_len} 個扭蛋。\n分別是：{gashapon_list_text}？",
                    "weight": "bold",
                    "size": "sm",
                    "align": "center",
                    "color": "#043b4aaa",
                    "margin": "8px",
                    "wrap": True,
                    "lineSpacing": "4px"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "margin": "12px",
                    "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "text",
                            "text": "重置後新增",
                            "color": "#12728c",
                            "weight": "bold"
                        }
                        ],
                        "justifyContent": "center",
                        "alignItems": "center",
                        "paddingAll": "8px",
                        "cornerRadius": "8px",
                        "action": {
                        "type": "message",
                        "label": "扭蛋重置新增",
                        "text": f"扭蛋重置新增：{gashapon_list_text}"
                        }
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "text",
                            "text": "新增",
                            "color": "#12728c",
                            "weight": "bold"
                        }
                        ],
                        "justifyContent": "center",
                        "alignItems": "center",
                        "paddingAll": "8px",
                        "cornerRadius": "8px",
                        "backgroundColor": "#7acfe522",
                        "margin": "8px",
                        "action": {
                        "type": "message",
                        "label": "新增",
                        "text": f"扭蛋新增：{gashapon_list_text}"
                        }
                    }
                    ],
                }
            ],

        }
    }

    flex_message_contents.append( pageTemplate )
    flex_message = FlexSendMessage(
        alt_text= '有人在玩扭蛋機！',
        contents={
            "type": "carousel",
            "contents": flex_message_contents
        }
    )

    # 發送訊息
    line_bot_api.reply_message(event.reply_token, flex_message)


# 扭蛋結果
def pageTemplate_result(gashapon_info):

    # 內容
    pageTemplate_contents = []

    # 扭蛋圖
    pageTemplate_background = {
        "type": "image",
        "url": gashapon_info["img"],
        "size": "full",
        "aspectMode": "cover",
        "aspectRatio": "1:1",
        "gravity": "center"
    }
    pageTemplate_contents.append( pageTemplate_background )

    # 扭蛋結果文字
    pageTemplate_bottomText = {
        "type": "box",
        "layout": "horizontal",
        "contents": [
            {
                "type": "text",
                "size": "lg",
                "weight": "bold",
                "align": "center",
                "color": "#0f5560",
                "text":  gashapon_info["text"],
            }
        ],
        "position": "absolute",
        "offsetStart": "0px",
        "paddingAll": "20px",
        "offsetBottom": "0px",
        "offsetEnd": "0px"
    }
    pageTemplate_contents.append( pageTemplate_bottomText )

    # ========================= #
    
    # 一頁完整的內容
    pageTemplate = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": pageTemplate_contents,
            "paddingAll": "0px",
            "action": {
                "type": "message",
                "label": "action",
                "text": "扭蛋機" ,
            },
        }
    }
    return pageTemplate

# 扭蛋內容物
def pageTemplate_contents(gashapon_contents):

    pageTemplate_contentsbox = []

    # 標題
    pageTemplate_title = {
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
    }
    pageTemplate_contentsbox.append( pageTemplate_title )


    # 陣列分成 3 個一組的子陣列
    gashapon_contents = [gashapon_contents[i:i+3] for i in range(0, len(gashapon_contents), 3)]

    # 列
    for row in gashapon_contents:
        
        # 扭蛋列
        pageTemplate_row = {
            "type": "box",
            "layout": "horizontal",
            "contents": [
                # pageTemplate_item,
                # pageTemplate_item,
                # pageTemplate_item,
            ],
        }
        
        for item in row:
            
            if item != "{{{新增按鈕}}}":
                # 扭蛋項目
                pageTemplate_item = {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        # 扭蛋圖片
                        {
                            "type": "image",
                            "url": localImg("randomGashapon/Gashapon.png"),
                            "size": "40px",
                            "aspectRatio": "1:1"
                        },
                        # 文字
                        {
                            "type": "text",
                            "text": item,
                            "color": "#0f5560",
                            "weight": "bold",
                            "size": "xs",
                            "maxLines": 1,
                            "align": "center"
                        },
                        # 數字
                        # {
                        #     "type": "box",
                        #     "layout": "vertical",
                        #     "contents": [
                        #     {
                        #         "type": "text",
                        #         "text": "99",
                        #         "color": "#ffffff",
                        #         "weight": "bold",
                        #         "size": "xs"
                        #     }
                        #     ],
                        #     "position": "absolute",
                        #     "backgroundColor": "#ff7171",
                        #     "cornerRadius": "xxl",
                        #     "width": "24px",
                        #     "height": "24px",
                        #     "justifyContent": "center",
                        #     "alignItems": "center",
                        #     "offsetTop": "0px",
                        #     "offsetEnd": "12px"
                        # }
                        
                    ],
                    "alignItems": "center",
                    "justifyContent": "center",
                    "width": "33%",
                    "paddingAll": "4px",
                    "paddingTop": "8px",
                    "spacing": "6px",
                    "action": {
                        "type": "postback",
                        "label": "action",
                        "data": f"扭蛋選擇：{item}"
                    },
                }
            else:
                # 新增扭蛋按鈕
                pageTemplate_item = {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        # 扭蛋圖片
                        {
                            "type": "image",
                            "url": localImg("randomGashapon/GashaponAdd.png"),
                            "size": "40px",
                            "aspectRatio": "1:1"
                        },
                        # 文字
                        {
                            "type": "text",
                            "text": "新增扭蛋",
                            "color": "#0f5560",
                            "weight": "bold",
                            "size": "xs",
                            "maxLines": 1,
                            "align": "center"
                        },
                    ],
                    "alignItems": "center",
                    "justifyContent": "center",
                    "width": "33%",
                    "paddingAll": "4px",
                    "paddingTop": "8px",
                    "spacing": "6px",
                    "action": {
                        "type": "postback",
                        "label": "action",
                        "data": f"扭蛋新增！"
                    },
                }
            pageTemplate_row["contents"].append( pageTemplate_item )

        pageTemplate_contentsbox.append( pageTemplate_row )

    # 內容
    pageTemplate = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            # 背景
            {
                "type": "image",
                "url": localImg("randomGashapon/Background.png"),
                "aspectRatio": "1:1",
                "size": "full"
            },
            # 內容
            {
                "type": "box",
                "layout": "vertical",
                "contents": pageTemplate_contentsbox,
                # [
                #     pageTemplate_title,
                #     pageTemplate_row
                # ],
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

    return pageTemplate

# 包裝訊息，發送訊息
def flexMessage_reply(event, flex_message_contents, gashapon_result):

    quick_reply_list = [
        QuickReplyButton(
            action=MessageAction(label = "● 進行扭蛋", text = "扭蛋機")
        ),
        QuickReplyButton(
            action=MessageAction(label = "○ 重置機器", text = "扭蛋重置")
        ),
        QuickReplyButton(
            action=PostbackAction(label = "○ 新增扭蛋", data = "扭蛋新增！" )
        )
    ]

    # 包裝訊息
    flex_message = FlexSendMessage(
        alt_text='有人在玩扭蛋機！',
        contents={
            # JSON 格式貼這邊
            "type": "carousel",
            "contents": flex_message_contents
        },
        quick_reply=QuickReply(
            items=quick_reply_list
        )
    )
    
    # 發送訊息
    line_bot_api.reply_message(event.reply_token, flex_message)
