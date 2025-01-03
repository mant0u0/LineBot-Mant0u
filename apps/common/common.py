from flask import  request, url_for
from linebot import LineBotApi
from linebot.models import *

import json
import unicodedata
import re
import os
import random

from apps.common.firebase import *

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

# 取得專案中的 HTML 連結
def localHtml(path):
    
    # 取得機器人網址
    bot_url = request.url_root[:-1]
    # 取得HTML路徑
    html_path = 'html/' + path
    # 取得HTML網址
    html_url = bot_url + url_for('static', filename = html_path )

    return html_url

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


# -------------------------------------------
# 隨機生成句子
def random_sentence():

    # 主詞表
    subject_list = [
        "我", "你", "他", "我們", "你們", "他們", "大家"
    ]

    # 時間表
    time_list = [
        "早上", "中午", "下午", "晚上", "今天", "明天", "後天", "大後天", "下週", "下個月", "今年", "明年", "未來", "之後"
    ]

    # 名詞表
    noun_list = [
        "運勢", "健康", "工作", "樂透", "股票", "考試", 
        "目標", "挑戰", "計畫", "會議", "行程", "家庭",
        "旅行", "夢想", "機會", "時間", "學業", "快樂", 
        "朋友", "天氣", "心情", "心願", "目標", "進度", 
        "成果", "問題", "方法", "專案", "新開始", "改變",
        "愛情", "友情", "關係", "健康"
    ]


    # 動詞表
    verb_list = [
        "去", "做", "參加", "完成", "開始", "結束", 
        "學習", "嘗試", "忘記", "注意", "改進", "計劃", 
        "期待", "整理", "準備", "分享", "探索", "追求", 
        "研究", "修正", "克服", "檢討", "創造", "尋找", 
        "分析", "提高", "協助", "檢查", "解決", "面對"
    ]

    # 補語表
    complement_list = [
        "一下", "好嗎", "可能嗎", "吧", "試試看"
    ]

    # 句型結構
    sentence_structures = [
        "{subject}{time}的{noun}",
        "{subject}的{noun}",
        "{time}的運勢",
        "{subject}{time}要不要{verb}{noun}{complement}",
        "{subject}可不可以{verb}{noun}{complement}",
        "{time}{subject}要不要{verb}{noun}",
        "可以幫{subject}{verb}{noun}嗎",
        "{subject}的{noun}怎麼樣",
        "{subject}需要{verb}{noun}嗎"
    ]

    # 隨機選擇句型
    structure = random.choice(sentence_structures)

    # 根據句型結構生成句子
    sentence = structure.format(
        subject=random.choice(subject_list),
        time=random.choice(time_list),
        noun=random.choice(noun_list),
        verb=random.choice(verb_list),
        complement=random.choice(complement_list)
    )
    return sentence

# --------------------------------------------


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

