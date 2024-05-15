from flask import  request, url_for
from linebot import LineBotApi
from linebot.models import *

import json
import unicodedata
import re
import os


# 上傳圖片 imgbb
import imgbbpy
imgbb_key = os.getenv("IMGBB_KEY")
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))


# 取得專案中的圖片連結
def localImg(path):
    
    # 取得機器人網址
    bot_url = request.url_root[:-1]
    # 取得圖片路徑
    img_path = 'images/' + path
    # 取得圖片網址
    image_url = bot_url + url_for('static', filename = img_path )

    return image_url


# 上傳圖片至 imgbb
def upload_img_to_imgbb(event):
    try:
        source_id = getMessageSourceID(event)    # 取得訊息來源 ID
        client = imgbbpy.SyncClient(imgbb_key) # 上傳至 imgbb 圖庫
        image = client.upload(file=f"/tmp/{source_id}.jpg")

        # 取得圖片網址
        return image.url
    
    except:
        return ""

# 取得訊息來源資訊
def getMessageSourceID(event):
    
    # 訊息來源類型 (user/group)
    source_type = event.source.type

    # 使用者 ID
    if source_type == 'user':
        source_id = event.source.user_id

    # 群組 ID
    if source_type == 'group':
        source_id = event.source.group_id

    return source_id

# 取得使用者名稱
def getUserName(event):

    user_id = event.source.user_id
    try:
        profile = line_bot_api.get_profile(user_id)
        profile = json.loads(str(profile))  # 字串轉字典型態
        user_name = str(profile['displayName'])
    except:
        user_name = '使用者'
    return user_name

# 取得使用者圖片
def getUserPhoto(event):
    user_id = event.source.user_id
    try:
        profile = line_bot_api.get_profile(user_id)
        profile = json.loads(str(profile))  # 字串轉字典型態
        user_pictureUrl = str(profile['pictureUrl'])
    except:
        user_pictureUrl = " "
    return user_pictureUrl

# 讀取 JSON 檔案
def read_json(path, id):
    # 選擇存取的檔案路徑
    path = "/tmp/"+path+".json"

    try:
        with open(path, 'r') as file:
            data = json.load(file) # 讀取檔案
        try:
            loaded_data = data[id] # 使用 ID 作為 Key 來查詢
            print("[成功] 讀取 JSON 成功")
            return loaded_data

        except:
            print("[錯誤] 無資料")

    except FileNotFoundError:
        print("[錯誤] 找不到指定的檔案")

    except json.JSONDecodeError:
        print("[錯誤] JSON 解碼失敗")
    
    return " "

# 寫入 JSON 檔案
def write_json(path, id, data):
    # 選擇存取的檔案路徑
    path = "/tmp/"+path+".json"

    try:
        with open(path, 'r') as file:
            existing_data = json.load(file)
    except FileNotFoundError:
        existing_data = {}
    existing_data[id] = data

    with open(path, 'w') as file:
        json.dump(existing_data, file, indent=4)

# 移除 JSON 資料
def remove_json(path, id):
    # 選擇存取的檔案路徑
    path = "/tmp/"+path+".json"

    try:
        with open(path, 'r') as file:
            existing_data = json.load(file)

    except FileNotFoundError:
        print("[錯誤] 找不到指定的檔案")

    except json.JSONDecodeError:
        print("[錯誤] JSON 解碼失敗")

    try:
        del existing_data[id]
        with open(path, 'w') as file:
            json.dump(existing_data, file, indent=4)
        print(f"[成功] 成功移除 ID {id} 的元素")
    except KeyError:
        print(f"[錯誤] 找不到指定 ID 的元素: {id}")


# 字元寬度比例計算
def get_char_width_ratio(string):
    full_width_count = 0 # 全形字數
    half_width_count = 0 # 半形形字數

    for char in string:
        if unicodedata.east_asian_width(char) in ('F', 'W', 'A'):
            full_width_count += 1
        else:
            half_width_count += 1

    char_width = (full_width_count * 2) + half_width_count
    return char_width

# 判斷字串以 http、https 開頭
def is_url(url):
    pattern = r'^https?://.*$'
    match = re.match(pattern, url, re.IGNORECASE)
    return bool(match)

# 判斷字串以 http、https 開頭，以 .png 或 .jpg 結尾的 URL
def is_url_with_image_extension(url):
    pattern = r'^https?://.*\.(png|jpg|jpeg)$'
    match = re.match(pattern, url, re.IGNORECASE)
    return bool(match)

# 字串連結提取
def extract_url(text):
    # 定義連結的正規表達式模式
    pattern = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+/(?:[\w./?%&=]*)'

    # 使用re.findall()函式來找到字串中的所有連結
    url_list = re.findall(pattern, text)

    return url_list

# 數學式判斷
def is_math_expression(expression):
    try:
        result = eval(expression)
        return True, result
    except (SyntaxError, TypeError):
        return False, None

