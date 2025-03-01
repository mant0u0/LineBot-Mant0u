from linebot import LineBotApi
from linebot.models import *

import os
import random
import datetime


from apps.common.common import *
from apps.common.firebase import *

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))




# --------------------------------------------------
# 註冊
def userInfoRegister(event):
    
    source_id = getMessageSourceID(event)   # 取得訊息來源 ID
    user_id = event.source.user_id          # 取得使用者 ID
    user_name = getUserName(event)          # 取得使用者名稱
    user_pictureUrl = getUserPhoto(event)   # 取得使用者圖片
    
    latest_update = datetime.datetime.now()
    latest_update = str(latest_update.strftime("%Y-%m-%d %H:%M"))  # 最後更新時間

    # 讀取資料庫
    database_userInfo = firebaseGetData(f"userInfo/{user_id}") 
    database_groupInfo = firebaseGetData(f"groupInfo/{source_id}") 

    action = "無"

    if database_userInfo == None:
        # 寫入新資料
        new_data_userInfo = {
            user_id :{
                "user_id": user_id,
                "line_name": user_name,
                "line_img": user_pictureUrl,
                "latest_update": latest_update,
                "group": [
                    source_id
                ]
            }
        }
        firebaseUpdate("userInfo", new_data_userInfo)
        action = "更新"
    
    else:
        # 找 database_userInfo["group"] 有沒有 source_id
        temp_list = list(database_userInfo["group"])
        if source_id in temp_list:
            action = "無"
        else:
            temp_list.append(source_id)
            new_data = {"group": temp_list}
            firebaseUpdate(f"userInfo/{user_id}", new_data)
            action = "更新"

    if database_groupInfo == None:
        new_data_groupInfo = {
            source_id: {
                "member": {
                    user_id : {
                        "user_id": user_id,
                        "line_name": user_name,
                        "main_name": user_name,
                        "latest_update": latest_update,
                        "state": {
                            "coin" : 500,
                            "lv" : 1,
                            "hp" : 100,
                            "mp" : 100,
                            "ap" : 5,
                        }
                    }
                }
            }
        }
        firebaseUpdate("groupInfo", new_data_groupInfo)
        action = "更新"

        
    if action == "更新":
        text_message = TextSendMessage(text=f"註冊成功囉！")
        line_bot_api.reply_message(event.reply_token, text_message)
    if action == "無":
        text_message = TextSendMessage(text=f"你已經註冊過囉～")
        line_bot_api.reply_message(event.reply_token, text_message)

# --------------------------------------------------
# 無註冊提示訊息
def userInfoNoRegisterAlert(event, type ="user"):
    if type == "user":
        text_message = TextSendMessage(
            text="你還沒有註冊喔！點擊「註冊」進行註冊～",
            quick_reply=QuickReply(
                items=[ QuickReplyButton( action=MessageAction(label='註冊', text='註冊'), ), ]
            )
        )
    elif type == "group":
        text_message = TextSendMessage(
            text="這個群組沒有人有註冊！點擊「註冊」進行註冊～",
            quick_reply=QuickReply(
                items=[ QuickReplyButton( action=MessageAction(label='註冊', text='註冊'), ), ]
            )
        )
    line_bot_api.reply_message(event.reply_token, text_message)
# --------------------------------------------------
# 改名
def userInfoRename(event, userMessage):
    new_user_name = userMessage.replace('改名：', '')

    source_id = getMessageSourceID(event)   # 取得訊息來源 ID
    user_id = event.source.user_id          # 取得使用者 ID
    file_path = f"groupInfo/{source_id}/member/{user_id}"    # 選擇存取的路徑

    # 讀取
    userinfo_data = firebaseGetData(file_path)
    if userinfo_data == None:
        userInfoNoRegisterAlert(event)
    else:
        # 訊息文字
        message_text = userinfo_data["main_name"] + " ➜ " + new_user_name

        # 改名
        userinfo_data["main_name"] = new_user_name
        # 最後更新時間
        latest_update = datetime.datetime.now()
        latest_update = str(latest_update.strftime("%Y-%m-%d %H:%M"))
        userinfo_data["latest_update"] = latest_update

        # 寫入
        firebaseUpdate(file_path, userinfo_data)

        # 顯示訊息
        text_message = TextSendMessage(text=f"{message_text}，改名成功！")
        line_bot_api.reply_message(event.reply_token, text_message)
# --------------------------------------------------
# 個人資料顯示
def userInfoDisplay(event):
    source_id = getMessageSourceID(event)                       # 取得訊息來源 ID
    user_id = event.source.user_id                              # 取得使用者 ID
    groupInfo_path = f"groupInfo/{source_id}/member/{user_id}"  # 存取路徑
    userinfo_data = firebaseGetData(groupInfo_path)  # 讀取
    if userinfo_data == None:
        userInfoNoRegisterAlert(event)
    else:
        message_text = "【名稱】" + userinfo_data["main_name"] + "\n【金幣】" + str(userinfo_data["state"]["coin"])
        # 顯示訊息
        text_message = TextSendMessage(text=f"{message_text}")
        line_bot_api.reply_message(event.reply_token, text_message)


# --------------------------------------------------
# 隨機顯示使用者名稱
def randomUserName(event):
    # 取得訊息來源 ID
    source_id = getMessageSourceID(event) 
    # 取得使用者 ID
    user_id = event.source.user_id
    # 選擇存取的路徑
    file_path = f"groupInfo/{source_id}/member"
    # 讀取
    group_users_info = firebaseGetData(file_path)
    if group_users_info == None:
        userInfoNoRegisterAlert(event, "group")
    else:
        # 隨機選擇一個 使用者 key
        random_user_key = random.choice(list(group_users_info.keys()))

        # 根據 使用者 key 取得對應的使用者資料
        random_user = group_users_info[random_user_key]["main_name"]

        # 隨機顯示一個使用者名稱
        text_message = TextSendMessage(text=random_user)
        line_bot_api.reply_message(event.reply_token, text_message)

# 偷錢選擇使用者
def stealCoinSelect(event):
    # 取得訊息來源 ID
    source_id = getMessageSourceID(event) 
    # 取得使用者 ID
    user_id = event.source.user_id
    # 選擇存取的路徑
    file_path = f"groupInfo/{source_id}/member"
    # 讀取
    group_users_info = firebaseGetData(file_path)
    
    if group_users_info == None:
        userInfoNoRegisterAlert(event,"group")
    else:
        quick_reply_list = []

        # 取得群組內的使用者
        for id in list(group_users_info.keys()):
            print(group_users_info[id]["main_name"])
            quick_reply_item = QuickReplyButton( 
                action=PostbackAction(
                    label=group_users_info[id]["main_name"], data=f'偷錢：{id}'
                ), 
            )
            quick_reply_list.append(quick_reply_item)

        text_message = TextSendMessage(
            text="你想要對誰執行動作？",
            quick_reply=QuickReply(
                items=quick_reply_list
            )
        )
        line_bot_api.reply_message(event.reply_token, text_message)

# 偷錢執行
def stealCoinAction(event, userPostback):
    # 取得使用者 ID
    user_1_id = event.source.user_id
    user_2_id = userPostback.replace('偷錢：', '')
    
    # 取得訊息來源 ID
    source_id = getMessageSourceID(event) 

    # 選擇存取的路徑
    file_path = f"groupInfo/{source_id}/member"
    
    # 讀取
    group_users_info = firebaseGetData(file_path)

    # 偷走的錢
    user_1_info = group_users_info[user_1_id]
    user_2_info = group_users_info[user_2_id]
    steal_coin_max = max(user_1_info["state"]["coin"], user_2_info["state"]["coin"])
    if steal_coin_max > 0:
        steal_coin = random.randint(1, steal_coin_max)
    else:
        steal_coin = random.randint(1, 200)

    # 執行動作機率
    action_random = random.randint(1, 100)
    if user_1_info["user_id"] == user_2_info["user_id"]:
        # 顯示訊息
        text_message = TextSendMessage(text=f"不可以偷自己的錢～")

    elif action_random < 50:
        # user_1
        user_1_info["state"]["coin"] = user_1_info["state"]["coin"] + steal_coin
        # user_2
        user_2_info["state"]["coin"] = user_2_info["state"]["coin"] - steal_coin

        coin_text = f"{user_1_info['main_name']}：{user_1_info['coin']}\n{user_2_info['main_name']}：{user_2_info['coin']}"

        firebaseUpdate(file_path, group_users_info)
        # 顯示訊息
        text_message = TextSendMessage(text=f"{user_1_info['main_name']} 成功從 {user_2_info['main_name']} 偷走 {str(steal_coin)} 硬幣！\n\n{coin_text}")
    
    elif action_random >= 50:
        # user_1
        user_1_info = group_users_info[user_1_id]
        user_1_info["state"]["coin"] = user_1_info["state"]["coin"] - steal_coin
        # user_2
        user_2_info = group_users_info[user_2_id]
        user_2_info["state"]["coin"] = user_2_info["state"]["coin"] + steal_coin

        coin_text = f"{user_1_info['main_name']}：{user_1_info['coin']}\n{user_2_info['main_name']}：{user_2_info['coin']}"

        firebaseUpdate(file_path, group_users_info)
        # 顯示訊息
        text_message = TextSendMessage(text=f"{user_1_info['main_name']} 偷竊失敗，上繳 {str(steal_coin)} 硬幣給 {user_2_info['main_name']}！\n\n{coin_text}")

    line_bot_api.reply_message(event.reply_token, text_message)
