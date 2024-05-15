from zhdate import ZhDate
from datetime import datetime, timedelta, timezone
from zhconv import convert # 簡轉繁

dateFormats = [
    "%Y/%m/%d", "%Y年%m月%d日", "%m/%d", "%m月%d日",
]


# 檢查是否為日期格式
def checkDate(text):
    current_year = datetime.now().year  # 取得當前年份

    for format_str in dateFormats:
        try:
            date_obj = datetime.strptime(text, format_str)

            # 如果日期格式中不包含年份，則設置為當前年份
            if "%Y" not in format_str and "%y" not in format_str:
                date_obj = date_obj.replace(year=current_year)

            return date_obj

        except ValueError:
            pass

    return "None"


# 取得日期文字
def getDateText(date_obj):
    # 定義星期的中文名稱映射
    weekday_mapping = {
        'Monday': '星期一',
        'Tuesday': '星期二',
        'Wednesday': '星期三',
        'Thursday': '星期四',
        'Friday': '星期五',
        'Saturday': '星期六',
        'Sunday': '星期日'
    }
    # 格式化日期
    date_str = date_obj.strftime("%Y 年 %m 月 %d 日（%A）")
    # 替換星期的英文名稱為中文名稱
    for english_day, chinese_day in weekday_mapping.items():
        date_str = date_str.replace(english_day, chinese_day)
    return date_str

# 取得農曆文字
def getDateLunarText(text):

    # 將字串解析為 datetime 對象
    date_object = datetime.strptime( str(text) , "%Y-%m-%d %H:%M:%S")
    
    #陽曆轉農曆
    date = datetime(date_object.year, date_object.month, date_object.day)
    date_lunar = ZhDate.from_datetime(date)
    date_lunar = convert(date_lunar.chinese(), 'zh-hant') # 簡轉繁
    date_lunar = date_lunar.replace('零', '〇')
    
    date_lunar_split = date_lunar.replace(' ', '|').replace('年', '年|').replace('月', '月|')
    date_lunar_split = date_lunar_split.replace('年||(', '|').replace('年|)', '')
    date_lunar_split = date_lunar_split.split('|')
    # print(date_lunar_split)
    
    # 年月日
    date_lunar_year_num = str(ZhDate.from_datetime(date).lunar_year)
    date_lunar_year = date_lunar_split[0]
    date_lunar_month = date_lunar_split[1]
    date_lunar_day = date_lunar_split[2]
    # 干支
    date_lunar_ganzhi = date_lunar_split[3]
    # 生肖
    date_lunar_zodiac = date_lunar_split[4]
    
    # print(date_lunar)
    

    date_lunar = f"{date_lunar_year_num} 年{date_lunar_month}{date_lunar_day}（{date_lunar_ganzhi}、{date_lunar_zodiac}）"

    # date_lunar = date_lunar.replace(' (', '（').replace(')', '）')
    return date_lunar

# 取得農曆
def getDateLunar(date_obj):

    # 將字串解析為 datetime 對象
    date_object = datetime.strptime( str(date_obj) , "%Y-%m-%d %H:%M:%S")

    # 陽曆轉農曆
    date = datetime(date_object.year, date_object.month, date_object.day)
    lunar = ZhDate.from_datetime(date)

    # 處理農曆字串
    lunar_text = convert(lunar.chinese(), 'zh-hant') # 簡轉繁
    lunar_text = lunar_text.replace('零', '〇')
    lunar_split = lunar_text.replace(' ', '|').replace('年', '年|').replace('月', '月|')
    lunar_split = lunar_split.replace('年||(', '|').replace('年|)', '')
    lunar_split = lunar_split.split('|')
    # 年月日字串
    lunar_text_year = lunar_split[0]
    lunar_text_month = lunar_split[1]
    lunar_text_day = lunar_split[2]
    # 干支字串
    lunar_text_ganzhi = lunar_split[3]
    # 生肖字串
    lunar_text_zodiac = lunar_split[4]

    zodiac_list = ['鼠', '牛', '虎', '兔', '龍', '蛇', '馬', '羊', '猴', '雞', '狗', '豬']
    lunar_zodiac = zodiac_list.index(lunar_text_zodiac) + 1

    ganzhi_1_list = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
    lunar_ganzhi_1 = ganzhi_1_list.index(lunar_text_ganzhi[0]) + 1

    ganzhi_2_list = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
    lunar_ganzhi_2 = ganzhi_2_list.index(lunar_text_ganzhi[1]) + 1

    # 數值
    lunar_obj = {
        'year': lunar.lunar_year,
        'month': lunar.lunar_month,
        'day': lunar.lunar_day,
        'ganzhi_1': lunar_ganzhi_1,
        'ganzhi_2': lunar_ganzhi_2,
        'zodiac': lunar_zodiac,
    }

    # 文字
    lunar_text_obj = {
        'year': lunar_text_year,
        'month': lunar_text_month,
        'day': lunar_text_day,
        'ganzhi': lunar_text_ganzhi,
        'zodiac': lunar_text_zodiac,
    }

    return lunar_obj


# 取得民國年
def getTaiwanYear(text):
    # 將字串解析為 datetime 對象
    date_object = datetime.strptime( str(text) , "%Y-%m-%d %H:%M:%S")

    taiwanYear = date_object.year - 1911
    
    if taiwanYear > 0:
        taiwanYear =  "民國 " + str(taiwanYear) + " 年"
    else:
        taiwanYear =  "民國前 " + str((taiwanYear-1)*(-1)) + " 年"

    return taiwanYear


# 計算日期與今天的天數差異
def calculateDays(date_obj):
    if date_obj is not None:
        # 將今天的日期轉換為 UTC+8 時區
        today = datetime.now(timezone(timedelta(hours=8))).date()
        date_difference = date_obj.date() - today

        if date_difference.days > 0:
            return f"還剩 {date_difference.days} 天"
        elif date_difference.days < 0:
            days_ago = abs(date_difference.days)
            if days_ago == 1:
                return "已過 1 天（昨天）"
            elif days_ago == 2:
                return "已過 2 天（前天）"
            else:
                return f"已過 {days_ago} 天"
        else:
            return "今天"
    else:
        return None
