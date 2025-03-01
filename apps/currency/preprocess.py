import re

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

def preprocess_text(text):
    """預處理文本"""
    # 將中文數字轉換為阿拉伯數字
    text = text.replace('萬', '0000')
    text = text.replace('千', '000')
    text = text.replace('百', '00')
    text = text.replace(',', '')
    return text

def find_currencies(text):
    """找出所有貨幣關鍵字及其位置"""
    currency_positions = []
    
    for currency_code, currency_info in currency_dict.items():
        for keyword in currency_info["keyword"]:
            pos = text.find(keyword)
            if pos != -1:
                currency_positions.append({
                    'code': currency_code,
                    'keyword': keyword,
                    'position': pos,
                    'length': len(keyword)
                })
    
    # 根據關鍵字位置排序
    return sorted(currency_positions, key=lambda x: x['position'])

def find_number_before_currency(text, currency_pos):
    """找出貨幣關鍵字前的數字"""
    # 取得貨幣關鍵字前的子字串
    subtext = text[:currency_pos]
    
    # 找出所有數字
    numbers = re.findall(r'\d+(?:\.\d+)?', subtext)
    
    if not numbers:
        return None
        
    # 取得最後一個數字（最接近貨幣關鍵字的數字）
    last_number = numbers[-1]
    number_pos = subtext.rfind(last_number)
    
    # 檢查數字和貨幣關鍵字之間是否只有空白
    text_between = subtext[number_pos + len(last_number):].strip()
    if text_between:
        return None
        
    return last_number

# 字串辨識貨幣與數字
def extract_currency_conversion(text):
    """提取貨幣轉換訊息"""
    # 預處理文本
    text = preprocess_text(text)
    
    # 1. 找出所有貨幣關鍵字
    currency_positions = find_currencies(text)
    # print(currency_positions)

    if not currency_positions:
        return {"num": "0", "result": [], "state": "fail"}
    
    # 2. 找出第一個貨幣關鍵字前的數字
    first_currency = currency_positions[0]
    number = find_number_before_currency(text, first_currency['position'])
    
    if not number or float(number) <= 0:
        return {"num": "0", "result": [], "state": "fail"}
    
    # 3. 處理貨幣結果
    result_currencies = []
    result_currencies.append(first_currency['code'])

    # 4. 尋找第二個貨幣關鍵字, 如果找不到第二個預設為新台幣
    if len(currency_positions) > 1:
        result_currencies.append(currency_positions[1]['code'])
    else:
        result_currencies.append("TWD")
    
    # 5. 檢查兩個貨幣是否相同
    if result_currencies[0] == result_currencies[1]:
        result_currencies[1] = "TWD"

    # 6. 檢查兩個貨幣是否為台幣
    if result_currencies[0] == "TWD" and result_currencies[1] == "TWD":
        return {"num": "0", "result": [], "state": "fail"}

    return {
        "num": number,
        "result": result_currencies,
        "state": "success"
    }


# 測試實際用例
# test_input = "40 美金轉台幣"
# result = extract_currency_conversion(test_input)
# print(f"\n實際測試 '{test_input}':")
# print(f"結果: {result}")