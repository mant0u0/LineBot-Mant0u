# 海綿寶寶梗圖

from linebot import LineBotApi
from linebot.models import *

import os
import csv
import random
import re
from difflib import SequenceMatcher

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))

# CSV 檔案路徑
def get_csv_path():
    """取得 SpongeBob.csv 檔案的絕對路徑"""
    # 獲取專案根目錄：從當前文件向上找到包含 index.py 的目錄
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(os.path.dirname(current_dir))
    csv_path = os.path.join(base_dir, 'static', 'csv', 'SpongeBob.csv')
    
    # 在 Vercel/Lambda 環境中，如果上述路徑不存在，嘗試使用 /var/task 路徑
    if not os.path.exists(csv_path):
        csv_path = '/var/task/static/csv/SpongeBob.csv'
    
    return csv_path

# 載入梗圖資料
def load_memes():
    """從 CSV 載入梗圖資料"""
    csv_path = get_csv_path()
    memes = []
    
    try:
        if not os.path.exists(csv_path):
            print(f"❌ 找不到檔案: {csv_path}")
            return memes
        
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            memes = list(reader)
        
        print(f"✅ 成功載入 {len(memes)} 個海綿寶寶梗圖")
    except Exception as e:
        print(f"❌ 載入梗圖資料失敗: {e}")
        memes = []
    
    return memes

# 計算字串相似度
def calculate_similarity(str1, str2):
    """計算兩個字串的相似度"""
    return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()

# 搜尋梗圖（返回單個結果）
def search_meme(keyword=None):
    """
    搜尋梗圖（支援模糊搜尋）
    
    Args:
        keyword: 搜尋關鍵字，如果為 None 則隨機選擇
    
    Returns:
        dict: 包含梗圖資訊的字典，如果找不到則返回 None
    """
    memes = load_memes()
    
    if not memes:
        print("❌ 沒有可用的梗圖資料")
        return None
    
    # 如果沒有關鍵字，隨機選一個
    if not keyword:
        return random.choice(memes)
    
    # 1. 先搜尋完全匹配的名稱
    exact_matched = [
        meme for meme in memes 
        if keyword.lower() == meme.get('名稱', '').lower()
    ]
    
    if exact_matched:
        print(f"✅ [完全匹配] 找到 {len(exact_matched)} 個完全匹配「{keyword}」的梗圖")
        return random.choice(exact_matched)
    
    # 2. 如果沒有完全匹配，搜尋部分匹配的項目
    partial_matched = [
        meme for meme in memes 
        if keyword.lower() in meme.get('名稱', '').lower()
    ]
    
    if partial_matched:
        print(f"✅ [部分匹配] 找到 {len(partial_matched)} 個部分符合「{keyword}」的梗圖")
        return random.choice(partial_matched)
    
    # 3. 使用模糊搜尋（相似度 > 0.6）
    fuzzy_threshold = 0.6
    fuzzy_matches = []
    
    for meme in memes:
        meme_name = meme.get('名稱', '')
        similarity = calculate_similarity(keyword, meme_name)
        if similarity >= fuzzy_threshold:
            fuzzy_matches.append((meme, similarity))
    
    if fuzzy_matches:
        # 按相似度排序，選擇最相似的幾個
        fuzzy_matches.sort(key=lambda x: x[1], reverse=True)
        print(f"✅ [模糊搜尋] 找到 {len(fuzzy_matches)} 個相似項目")
        print(f"   最佳匹配: 「{fuzzy_matches[0][0].get('名稱')}」(相似度: {fuzzy_matches[0][1]:.2f})")
        
        # 從最相似的前 5 個中隨機選一個
        top_matches = fuzzy_matches[:5]
        selected = random.choice(top_matches)
        return selected[0]
    
    # 4. 如果都找不到，隨機選擇一個
    print(f"⚠️ 找不到符合「{keyword}」的梗圖，隨機選擇一個")
    return random.choice(memes)

# 搜尋梗圖（返回多個結果）
def search_memes_multiple(keyword):
    """
    搜尋梗圖並返回多個結果（最多3個）
    
    Args:
        keyword: 搜尋關鍵字
    
    Returns:
        list: 包含梗圖資訊的列表
    """
    memes = load_memes()
    
    if not memes:
        print("❌ 沒有可用的梗圖資料")
        return []
    
    results = []
    
    # 1. 先搜尋完全匹配的名稱
    exact_matched = [
        meme for meme in memes 
        if keyword.lower() == meme.get('名稱', '').lower()
    ]
    
    if exact_matched:
        print(f"✅ [完全匹配] 找到 {len(exact_matched)} 個完全匹配「{keyword}」的梗圖")
        results = exact_matched[:3]
        return results
    
    # 2. 搜尋部分匹配的項目
    partial_matched = [
        meme for meme in memes 
        if keyword.lower() in meme.get('名稱', '').lower()
    ]
    
    if partial_matched:
        print(f"✅ [部分匹配] 找到 {len(partial_matched)} 個部分符合「{keyword}」的梗圖")
        results = partial_matched[:3]
        return results
    
    # 3. 使用模糊搜尋（相似度 > 0.6）
    fuzzy_threshold = 0.6
    fuzzy_matches = []
    
    for meme in memes:
        meme_name = meme.get('名稱', '')
        similarity = calculate_similarity(keyword, meme_name)
        if similarity >= fuzzy_threshold:
            fuzzy_matches.append((meme, similarity))
    
    if fuzzy_matches:
        # 按相似度排序，取最相似的 3 個
        fuzzy_matches.sort(key=lambda x: x[1], reverse=True)
        print(f"✅ [模糊搜尋] 找到 {len(fuzzy_matches)} 個相似項目")
        results = [meme for meme, _ in fuzzy_matches[:3]]
        return results
    
    # 4. 如果都找不到，返回空列表
    print(f"⚠️ 找不到符合「{keyword}」的梗圖")
    return []

# 主要函式 - 隨機選擇
def spongeBobMain(event):
    """隨機選擇一張海綿寶寶梗圖"""
    meme = search_meme(None)
    send_spongebob_meme(event, meme)

# 主要函式 - 關鍵字搜尋
def spongeBobSearch(event, userMessage):
    """根據關鍵字搜尋海綿寶寶梗圖"""
    # 處理訊息，移除觸發詞
    if userMessage.startswith('海綿：'):
        keyword = userMessage.replace('海綿：', '').strip()
    else:
        keyword = userMessage.replace('海綿！', '').strip()
    
    # 如果沒有關鍵字，隨機選擇
    if not keyword:
        meme = search_meme(None)
        send_spongebob_meme(event, meme)
        return
    
    # 搜尋梗圖（返回多個結果）
    memes = search_memes_multiple(keyword)
    
    if not memes:
        # 找不到任何結果
        text_message = TextSendMessage(text="找不到梗圖喔～")
        line_bot_api.reply_message(event.reply_token, text_message)
        return
    
    if len(memes) == 1:
        # 只有一個結果，直接發送梗圖
        send_spongebob_meme(event, memes[0])
    else:
        # 有多個結果，顯示快速回覆（最多3個）附加在 flex message
        quick_reply_items = []
        for meme in memes[:3]:
            meme_name = meme.get('名稱', '海綿寶寶梗圖')
            # 限制 label 長度不超過 16 個字符，超過後加 ...
            label = (meme_name[:16] + '...') if len(meme_name) > 16 else meme_name
            quick_reply_items.append(
                QuickReplyButton(
                    action=MessageAction(label=label, text=f"海綿：{meme_name}")
                )
            )
        
        # 發送第一個梗圖的 flex message，附加快速回覆
        first_meme = memes[0]
        image_url = first_meme.get('i.imgur', '')
        meme_name = first_meme.get('名稱', '海綿寶寶梗圖')
        
        quick_reply_items.insert(0, QuickReplyButton(
            action=MessageAction(label="呼叫海綿！", text="海綿！")
        ))
        
        flex_message = FlexSendMessage(
            alt_text=meme_name,
            contents={
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "image",
                            "url": image_url,
                            "size": "full",
                            "aspectMode": "cover",
                            "aspectRatio": "1420:1080",
                            "gravity": "center"
                        }
                    ],
                    "paddingAll": "0px",
                    "action": {
                        "type": "uri",
                        "label": "開啟圖片",
                        "uri": image_url
                    }
                }
            },
            quick_reply=QuickReply(items=quick_reply_items)
        )
        
        line_bot_api.reply_message(event.reply_token, flex_message)

# 發送梗圖
def send_spongebob_meme(event, meme):
    """發送梗圖到 LINE"""
    if not meme:
        text_message = TextSendMessage(text="無法取得梗圖，請稍後再試")
        line_bot_api.reply_message(event.reply_token, text_message)
        return
    
    # 取得圖片 URL
    image_url = meme.get('i.imgur', '')
    meme_name = meme.get('名稱', '海綿寶寶梗圖')
    
    if not image_url:
        text_message = TextSendMessage(text="梗圖沒有圖片網址")
        line_bot_api.reply_message(event.reply_token, text_message)
        return
    
    # 建立 Flex Message
    flex_message = FlexSendMessage(
        alt_text=meme_name,
        contents={
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "image",
                        "url": image_url,
                        "size": "full",
                        "aspectMode": "cover",
                        "aspectRatio": "1420:1080",
                        "gravity": "center"
                    }
                ],
                "paddingAll": "0px",
                "action": {
                    "type": "uri",
                    "label": "開啟圖片",
                    "uri": image_url
                }
            }
        },
        quick_reply=QuickReply(items=[
            QuickReplyButton(
                action=MessageAction(label="呼叫海綿！", text="海綿！")
            )
        ])
    )
    
    # 發送訊息
    line_bot_api.reply_message(event.reply_token, flex_message)
