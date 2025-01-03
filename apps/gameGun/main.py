# 手槍
from linebot import LineBotApi
from linebot.models import *

import os
import random

from apps.common.common import *
from apps.common.database import *

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))

# 子彈設定
def gameGunSet(event, userMessage):

    source_id = getMessageSourceID(event)   # 取得訊息來源 ID
    file_path = 'gameGun'         # 選擇存取的檔案路徑
    if userMessage == '手槍':
        userMessage = '手槍：6'
        
    if userMessage.find('手槍：') == 0:
        # 整理文字
        num = userMessage.replace('手槍：', '')

        # 一般模式：指定彈匣數
        if num.isdigit():
            
            if int(num) <= 0:
                text_message = TextSendMessage(text="你沒有填裝任何子彈！")
                line_bot_api.reply_message(event.reply_token, text_message)
            
            bullet_list = set_gun_bullet( int(num) )

            # 紀錄彈夾設定
            bullet_data = {
                "list": bullet_list,
                "now" : 0,
                "model": "default"
            }
            write_database_combined(file_path, source_id, bullet_data)    # 寫入 JSON 檔案

            # 設定回應資料
            reply_data = {
                "text" : f"手槍 {num} 發裝子彈！",
                "top_text": f"剩下 {num} 發",
                "img": "ready",
                "color": "#10665a",
                "top_color": "#22af9e",
                "last": num,
                "sum" : len(bullet_list),
            }

            # 取得結果畫面、顯示畫面
            pageTemplate = pageTemplate_result(reply_data)
            flexMessage_reply(event, pageTemplate, reply_data)
            return

        # 機率模式：指定子彈機率
        elif is_percentage(num):
            
            # 紀錄彈夾設定
            bullet_data = {
                "pr": num,
                "model": "probability"
            }
            write_database_combined(file_path, source_id, bullet_data)    # 寫入 JSON 檔案

            # 設定回應資料
            reply_data = {
                "text" : f"手槍機率設定為 {num}！",
                "top_text": f"開槍機率：{num}",
                "img": "ready",
                "color": "#10665a",
                "top_color": "#22af9e",
                "last": num,
                "sum" : num,
            }

            # 取得結果畫面、顯示畫面
            pageTemplate = pageTemplate_result(reply_data)
            flexMessage_reply(event, pageTemplate, reply_data)
            return

# 開槍
def gameGunPlay(event):
    
    source_id = getMessageSourceID(event)   # 取得訊息來源 ID
    file_path = 'gameGun'         # 選擇存取的檔案路徑

    try:
        # 讀取檔案
        bullet_data = read_database_combined(file_path, source_id)
        
        # 一般模式
        if bullet_data["model"] == "default":
            bullet_list = bullet_data["list"] # 彈夾狀態
            bullet_now  = bullet_data["now"]  # 目前彈夾位置
            
            # 空包彈
            if bullet_list[bullet_now] == 0:
                bullet_last = len(bullet_list) - bullet_now - 1
                result_text =f"第 {str(bullet_now + 1)} 槍，沒有發生任何事～"
                bullet_data = {
                    "list": bullet_list,
                    "now" : bullet_now + 1,
                    "model": "default",
                }
                write_database_combined(file_path, source_id, bullet_data) # 寫入 JSON 檔案

                # 設定回應資料
                reply_data = {
                    "text" : result_text,
                    "top_text": f"剩下 {str(bullet_last)} 發",
                    "img": "none",
                    "color": "#10665a",
                    "top_color": "#22af9e",
                    "last": bullet_last,
                    "sum" : len(bullet_list),
                }

                # 取得結果畫面、顯示畫面
                pageTemplate = pageTemplate_result(reply_data)
                flexMessage_reply(event, pageTemplate, reply_data)
                return

            # 射出
            if bullet_list[bullet_now] == 1:
                result_text =f"第 {str(bullet_now+1)} 槍，子彈射出！"
                bullet_data = {
                    "list": bullet_list,
                    "now" : 0,
                    "model": "default",
                }
                write_database_combined(file_path, source_id, bullet_data) # 寫入 JSON 檔案
                
                # 設定回應資料
                reply_data = {
                    "text" : result_text,
                    "top_text": "",
                    "img": "shoot",
                    "color": "#a81e18",
                    "top_color": "#a82922",
                    "last": -1,
                    "sum" : len(bullet_list),
                }

                # 移除資料
                remove_database_combined(file_path, source_id)

                # 取得結果畫面、顯示畫面
                pageTemplate = pageTemplate_result(reply_data)
                flexMessage_reply(event, pageTemplate, reply_data)
                return

        # 機率模式
        elif bullet_data["model"] == "probability":
            bullet_pr = bullet_data["pr"] # 子彈機率(字串，如："10%")
            if get_probability_bullet_result(bullet_pr):
                # 設定回應資料
                reply_data = {
                    "text" : "槍聲一響，子彈射出！",
                    "top_text": f"開槍機率：{bullet_pr}",
                    "img":  "shoot",
                    "color": "#a81e18",
                    "top_color": "#a82922",
                    "last": 0,
                    "sum" : bullet_pr,
                }
                # 取得結果畫面、顯示畫面
                pageTemplate = pageTemplate_result(reply_data)
                flexMessage_reply(event, pageTemplate, reply_data)
                return
            else:
                # 設定回應資料
                reply_data = {
                    "text" : "手槍沒有發生任何事～",
                    "top_text": f"開槍機率：{bullet_pr}",
                    "img": "none",
                    "color": "#10665a",
                    "top_color": "#22af9e",
                    "last": 0,
                    "sum" : bullet_pr,
                }
                # 取得結果畫面、顯示畫面
                pageTemplate = pageTemplate_result(reply_data)
                flexMessage_reply(event, pageTemplate, reply_data)
                return

    except:
        text_message = TextSendMessage(
            text="目前沒有裝設子彈！",
            quick_reply= QuickReply(
                items=[
                    QuickReplyButton(
                        action=MessageAction(label = "6 發手槍", text = "手槍：6" )
                    ),
                    QuickReplyButton(
                        action=MessageAction(label = "12 發手槍", text = "手槍：12" )
                    ),
                    QuickReplyButton(
                        action=MessageAction(label = "25% 機率手槍", text = "手槍：25%" )
                    ),
                    QuickReplyButton(
                        action=MessageAction(label = "50% 機率手槍", text = "手槍：50%" )
                    ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, text_message)

# 彈夾設定
def set_gun_bullet(num):

    bullet_list = [0] * num                     # 彈夾建立：一個長度為 num 的列表，所有元素初始化為 0
    bullet_index = random.randint(0, num - 1)   # 隨機放入子彈
    bullet_list[bullet_index] = 1

    return bullet_list

# 判斷字串 pr 是否為百分比 
def is_percentage(pr):
    if isinstance(pr, str) and pr.endswith('%'):
        num = pr[:-1]
        if num.replace('.', '', 1).isdigit():
            return True
    return False

# 生成一個隨機數 (0 或 1)：其中 1 的機率為 pr 值
def get_probability_bullet_result(pr):
    # 將百分比字串轉換為浮點數
    pr_float = float(pr.strip('%')) / 100
    return 1 if random.random() < pr_float else 0

# 手槍畫面顯示結果
def pageTemplate_result(reply_data):

    pageTemplate_contents = []

    # 背景圖
    pageTemplate_bg = {
        "type": "image",
        "url": localImg(f"gameGun/{reply_data['img']}.png"),
        "size": "full",
        "aspectRatio": "1:1",
        "aspectMode": "cover"
    }

    # 左上角文字
    width = get_char_width_ratio(reply_data["top_text"]) * 9
    width = str(width)+"px"
    pageTemplate_last_text = {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "text",
                "text": reply_data["top_text"],
                "color": "#ffffff",
                "align": "center",
                "size": "xs"
            }
        ],
        "position": "absolute",
        "cornerRadius": "20px",
        "backgroundColor": reply_data["top_color"],
        "paddingAll": "4px",
        "paddingStart": "8px",
        "paddingEnd": "8px",
        "offsetTop": "20px",
        "width": width,
        "offsetStart": "20px"
    }

    # 底部文字
    pageTemplate_text = {
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
                "text": reply_data['text'],
                "size": "lg",
                "color": reply_data['color'],
                "weight": "bold"
            }
        ],
    }

    pageTemplate_contents.append( pageTemplate_bg )
    # 判斷是否要接續開槍：無開槍時，顯示還剩幾發
    if reply_data["last"] != -1:
        pageTemplate_contents.append( pageTemplate_last_text ) 
    pageTemplate_contents.append( pageTemplate_text )

    # 判斷是否要接續開槍：無開槍繼續，有開槍重置遊戲
    if reply_data["last"] != -1:
        action_text = "開槍"                           # 接續開槍
    else:
        action_text = "手槍："+ str(reply_data["sum"]) # 重置遊戲
    
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
                "text": action_text
            },
        }
    }

    return pageTemplate

# 包裝訊息，發送訊息
def flexMessage_reply(event, pageTemplate, reply_data):

    # flexMessage 容器
    flex_message_contents = []

    # 將 pageTemplate 放入 flex_message_contents 中
    flex_message_contents.append( pageTemplate )

    
    if reply_data["last"] != -1:
        # 接續開槍
        quick_reply = QuickReply(
            items=[
                QuickReplyButton(
                    action=MessageAction(label = "開槍", text = "開槍")
                ),
            ]
        )
    else:
        # 重置遊戲
        quick_reply = QuickReply(
            items=[
                QuickReplyButton(
                    action=MessageAction(label = "重置手槍", text = "手槍："+ str(reply_data["sum"]) )
                ),
            ]
        )


    # 包裝訊息
    flex_message = FlexSendMessage(
        alt_text= reply_data['text'],
        contents={
            # JSON 格式貼這邊
            "type": "carousel",
            "contents": flex_message_contents
        },
        quick_reply= quick_reply
    )
    
    # 發送訊息
    line_bot_api.reply_message(event.reply_token, flex_message)
