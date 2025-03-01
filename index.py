from flask import Flask, request, abort, url_for
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

import os
import requests
import random

from apps.example.sendMessage import *
from apps.example.lineInfo import *
from apps.example.writeReadJson import *

# 指令說明選單
from apps.menu.main import mant0u_bot_main, mant0u_bot_instructions
from apps.menu.detail import menuDetail
# from apps.menu.example import menuExample, menuDetailExample

from apps.common.common import *
from apps.common.recordMessage import recordTextMessage, readTextMessage
from apps.common.dateConverter import *
from apps.common.firebase import *
from apps.account.userInfo import *

from apps.ai.main import aiMain, aiVision, aiMant0u, aiFreeTest
from apps.ai.groq_whisper import groqWhisper
# from apps.fixTwitter.main import twitterMain
from apps.fixTwitter.v2 import twitter_message_main
# from apps.fixInstagram.new import instaNew

from apps.searchWeb.main import searchWeb, searchWebShopping, searchWebVideo, searchWebMovie, searchWebAnime, searchWebMusic, searchWebImg, searchMap

from apps.gameGun.main import gameGunSet, gameGunPlay
from apps.gameIchiban.main import gameIchibanSet, gameIchibanPlay
from apps.gamePopUpPirate.main import gamePopUpPirateSet, gamePopUpPiratePlay
from apps.gameRPS.main import gameRPSMain, gameRPSPlay

from apps.randomGashapon.main import *
from apps.randomGashapon.ai import randomGashaponAi

from apps.currency.main import currencyMain, currencyControlMenu, currencyDiscount, currencyMultiple, currencyDivide, currencyTax
from apps.currency.preprocess import extract_currency_conversion


from apps.translate.main import translateMain, translatePostback

from apps.randomDice.main import randomDiceMain
from apps.randomCoin.main import randomCoinMain
from apps.randomCoin.advanced import randomCoinAdvanced
from apps.randomNumber.main import random_number_main
from apps.randomSlot.main import random_slot_main
from apps.randomPoker.main import random_poker_main
from apps.randomBwaBwei.main import random_bwabwei_main
from apps.randomOkamikuji.main import random_okamikuji_main
from apps.randomWhichOne.main import random_which_one_main
from apps.randomShuffle.main import random_shuffle_main, random_shuffle_display, random_shuffle_flop
from apps.randomYesOrNo.main import random_yes_or_no_main, check_yes_or_no, random_yes_or_no_main_return

from apps.randomTarotCards.main import random_tarot_cards_main
from apps.questionnaire.main import questionnaireMain

from apps.japanese.question import japaneseQuestion, japaneseAnswer
from apps.japanese.wordCards import japaneseWordCards, japaneseVoice

from apps.otherTools.calculator import calculator
from apps.calendar.main import calendarMain
# from apps.calendar.example import calendarExample

# from apps.readGoogleSheetsCsv.keywordReply import keywordReply, keywordSet
# from apps.readGoogleSheetsCsv.badJoke import badJoke

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

mant0u_bot_model = os.getenv("MANT0U_BOT_MODEL")

app = Flask(__name__)

# domain root
@app.route('/')
def home():
    return 'Hello, World!'

# 忽略對 favicon.ico 的請求（避免 favicon.ico 的 404 錯誤 ）
@app.route("/favicon.ico")
def favicon():
    return url_for('static', filename='data:,')

@app.route("/webhook", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    # app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 文字訊息
@line_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    # 取得「使用者」訊息
    userMessage = event.message.text

    print(userMessage)

    # if mant0u_bot_model == "private":
        # print(userMessage)

        # if userMessage == '圖片':
        #     imageMessageExample(event)
        #     return
        # if userMessage == '文字':
        #     textMessageExample(event)
        #     return
        # if userMessage == '聲音':
        #     audioMessageExample(event)
        #     return
        # if userMessage == '讀取':
        #     readJsonExample(event)
        #     return
        # if userMessage.find('寫入：') == 0:
        #     writeJsonExample(event, userMessage)
        #     return
        # if userMessage.find('移除') == 0:
        #     removeJsonExample(event)
        #     return
        # if userMessage == '目錄圖片連結':
        #     text_message = TextSendMessage(text= localImg("mant0u.jpg") )
        #     line_bot_api.reply_message(event.reply_token, text_message)
        #     return
        # if userMessage == 'ID':
        #     source_id = getMessageSourceID(event)
        #     # 包裝訊息、發送訊息
        #     text_message = TextSendMessage(text=source_id)
        #     line_bot_api.reply_message(event.reply_token, text_message)
        #     return
        # if userMessage == '快速回覆':
        #     quickReplyExample(event)
        #     return
        # if userMessage == "註冊":
        #     userInfoRegister(event)
        #     return
        # if userMessage == "個人資料" or userMessage == "個人資訊" :
        #     userInfoDisplay(event)
        #     return
        # if userMessage.find('改名：') == 0:
        #     userInfoRename(event, userMessage)
        #     return
        # if userMessage == "誰啊" or userMessage == "誰阿" or userMessage == "換誰":
        #     randomUserName(event)
        #     return
        # if userMessage == "偷錢":
        #     stealCoinSelect(event)
        #     return
    
    # =============================== #

    # 說明
    if userMessage.find('？') == 0:
        command_text = userMessage[1:]
        menu_list = [
            # ['指令名稱','JSON 檔名'],
            ['饅頭','mant0u'],                              #
            ['搜尋','search'],                              #
            ['翻譯','translate'],                           #
            ['Twitter','twitter'],                          #
            ['貨幣換算','currency'],                        #
            ['海盜桶','gamePopUpPirate'],                   #
            ['一番賞','gameIchiban'],                       #
            ['扭蛋機','randomGashapon'],                    #
            ['猜拳','gameRPS'],                             #
            ['手槍','gameGun'],                             #
            ['亂數','randomNumber'],                        #
            ['硬幣','randomCoin'],                          #
            ['拉霸','randomSlot'],                          #
            ['擲筊','randomBwaBwei'],                       #
            ['骰子','randomDice'],                          #
            ['抽籤','randomOkamikuji'],                     #
            ['是不是、要不要、有沒有','randomYesOrNo'],     #
            ['哪個','randomWhichOne'],                      #
            ['撲克牌','randomPoker'],                       #
            ['塔羅牌','randomTarotCards'],                  #
            ['洗牌','randomShuffle'],                       #
        ]
        for item in menu_list:
            if command_text == item[0]:
                fileName = item[1]
                menuDetail(event, fileName)

    elif userMessage.find('饅頭：') == 0 or userMessage.find('饅：') == 0:
        aiMant0u(event, userMessage)
    elif userMessage.find('AI：') == 0 or userMessage.find('AI:') == 0:
        aiFreeTest(event, userMessage)
    elif userMessage.find('問：') == 0:
        if mant0u_bot_model == "private":
            aiMain(event, userMessage)
        else:
            aiMant0u(event, userMessage)
    elif userMessage.find('圖：') == 0 or userMessage.find('圖:') == 0 :
        aiVision(event, userMessage)

    elif userMessage.find('https://vxtwitter.com/') == 0 or userMessage.find('https://fxtwitter.com/') == 0 or userMessage.find('https://twitter.com/') == 0 or userMessage.find('https://x.com/') == 0:
        # twitterNew(event, userMessage)
        twitter_message_main(event, userMessage)

    elif userMessage == '扭蛋機' or userMessage == '扭蛋' :
        randomGashaponPlay(event)
    elif userMessage.find('扭蛋新增：') == 0 or userMessage.find('扭蛋重置新增') == 0:
        randomGashaponAdd(event, userMessage)
    elif userMessage.find('扭蛋移除：') == 0:
        randomGashaponRemove(event, userMessage)
    elif userMessage == '扭蛋重置':
        randomGashaponReset(event)
        text_message = TextSendMessage(text="扭蛋機重置成功！")
        line_bot_api.reply_message(event.reply_token, text_message)
    elif userMessage.find('扭蛋機：') == 0 or userMessage.find('扭蛋：') == 0:
        randomGashaponAi(event, userMessage)

    elif userMessage == '一番賞':
        gameIchibanSet(event)
    elif userMessage.find('一番賞：') == 0:
        gameIchibanPlay(event, userMessage)
    elif userMessage == '海盜桶':
        gamePopUpPirateSet(event)
    elif userMessage.find('海盜桶：') == 0:
        gamePopUpPiratePlay(event, userMessage)

    elif userMessage == '猜拳' :
        gameRPSMain(event)
    elif userMessage.find('手槍') == 0:
        gameGunSet(event, userMessage)
    elif userMessage == '開槍':
        gameGunPlay(event)
    
    elif userMessage.find('骰子') >= 0:
        randomDiceMain(event, userMessage)

    elif userMessage == '硬幣':
        randomCoinMain(event)
    elif userMessage.find('硬幣：') == 0:
        randomCoinAdvanced(event, userMessage)

    elif userMessage.find('亂數') == 0:
        random_number_main(event, userMessage)
    elif userMessage == '拉霸' or userMessage == 'SLOT':
        random_slot_main(event)

    elif userMessage.find('抽籤') == 0:
        random_okamikuji_main(event, userMessage)
    elif userMessage.find('擲筊') == 0:
        random_bwabwei_main(event, userMessage)
    elif userMessage.find('哪個：') == 0 or userMessage.find('都幾：') == 0:
        random_which_one_main(event, userMessage)

    elif userMessage.find('洗牌：') == 0:
        random_shuffle_main(event, userMessage)
    elif userMessage == '翻牌' or userMessage == '抽牌':
        random_shuffle_display(event)
    elif userMessage.find('翻牌：') == 0 or userMessage.find('抽牌：') == 0:
        random_shuffle_flop(event, userMessage)

    elif userMessage.find('撲克牌') == 0:
        random_poker_main(event, userMessage)
    elif userMessage.find('塔羅牌') == 0:
        random_tarot_cards_main(event, userMessage)

    elif userMessage.find('翻譯：') == 0:
        translateMain(event, userMessage)

    elif userMessage.find('搜尋：') == 0:
        searchWeb(event, userMessage)
    elif userMessage.find('購物：') == 0:
        searchWebShopping(event, userMessage)
    elif userMessage.find('追劇：') == 0 or userMessage.find('影片：') == 0:
        searchWebVideo(event, userMessage)
    elif userMessage.find('動畫：') == 0 or userMessage.find('動漫：') == 0:
        searchWebAnime(event, userMessage)
    elif userMessage.find('音樂：') == 0:
        searchWebMusic(event, userMessage)

    elif userMessage == '搜尋！':
        previousMessage = "搜尋：" + readTextMessage(event)["message"]
        searchWeb(event, previousMessage)
    elif userMessage == '購物！':
        previousMessage = "購物：" + readTextMessage(event)["message"]
        searchWebShopping(event, previousMessage)
    elif userMessage == '追劇！' or userMessage == '影片！':
        previousMessage = "追劇：" + readTextMessage(event)["message"]
        searchWebVideo(event, previousMessage)
    elif userMessage == '動畫！':
        previousMessage = "動畫：" + readTextMessage(event)["message"]
        searchWebAnime(event, previousMessage)
    elif userMessage == '音樂！':
        previousMessage = "音樂：" + readTextMessage(event)["message"]
        searchWebMusic(event, previousMessage)
    elif userMessage.find('電影！') == 0:
        searchWebMovie(event)
    elif userMessage == '找圖！':
        imageUrl = upload_img_to_imgbb(event) # 取得圖片網址
        searchWebImg(event, imageUrl) # 以圖搜尋

    elif userMessage.find('地圖：') == 0:
        searchMap(event, userMessage)
    elif userMessage.find('題目：') == 0 or userMessage.find('問題：') == 0:
        questionnaireMain(event, userMessage)

    elif userMessage.find('日文單字：') == 0:
        japaneseQuestion(event, userMessage)
    elif userMessage == '日文單字':
        japaneseWordCards(event)
    elif userMessage.find('日文語音：') == 0:
        japaneseVoice(event, userMessage)

    # 日期格式辨識
    elif checkDate(userMessage) != "None":
        date_obj = checkDate(userMessage)
        calendarMain(event, date_obj)

    # 計算機
    elif userMessage[-1] == "=":
        calculator(event, userMessage)

    # 字串中含有連結
    elif len(extract_url(userMessage)) > 0 and event.source.type == 'user' : 

        # 包裝訊息、發送訊息
        text_message = TextSendMessage(
            text="訊息中含有連結！",
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        action=PostbackAction(label="擷取連結", data="擷取連結："+ userMessage)
                    ),
                    QuickReplyButton(
                        action=PostbackAction(label="擷取並移除參數", data="擷取並移除參數："+ userMessage)
                    ),
                    QuickReplyButton(
                        action=PostbackAction(label="縮短網址", data="縮短網址："+ userMessage)
                    ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, text_message)


    # 貨幣換算
    elif extract_currency_conversion(userMessage)['state'] == 'success':
        currencyMain(event, userMessage)

    else:
        # 紀錄群組/個人前一則訊息 
        recordTextMessage(event, userMessage)

        # 檢查扭蛋機新增狀態是否被開啟
        checkGashaponJson(event, userMessage)

        # 判斷是不是在個人/群組
        if event.source.type == 'user':
            reply_message_line = []
            #「是不是、好不好、對不對、有沒有」句型
            if check_yes_or_no(userMessage): 
                YesNo_text_message = random_yes_or_no_main_return(userMessage)
                reply_message_line.append(YesNo_text_message)
                line_bot_api.reply_message(event.reply_token, reply_message_line)
        else:
            #「是不是、好不好、對不對、有沒有」句型
            if check_yes_or_no(userMessage): 
                random_yes_or_no_main(event, userMessage)

    # 主選單
    if userMessage == '饅頭':
        mant0u_bot_main(event)
    elif userMessage == '指令說明':
        mant0u_bot_instructions(event)


# Postback
@line_handler.add(PostbackEvent)
def handle_postback(event):
    
    # 取得「使用者」postback
    userPostback = event.postback.data

    if userPostback.find('猜拳：') == 0:
        gameRPSPlay(event, userPostback)
    if userPostback.find('貨幣：') == 0:
        currencyControlMenu(event, userPostback)
    if userPostback.find('貨幣打折：') == 0:
        currencyDiscount(event, userPostback)
    if userPostback.find('貨幣倍率：') == 0:
        currencyMultiple(event, userPostback)
    if userPostback.find('貨幣平分：') == 0:
        currencyDivide(event, userPostback)
    if userPostback.find('貨幣退稅：') == 0:
        currencyTax(event, userPostback)


    if userPostback.find('扭蛋選擇：') == 0:
        randomGashaponSelect(event, userPostback)
    if userPostback == '扭蛋新增！':
        randomGashaponAddBtnClick(event)

    if userPostback.find('日文單字解答：') == 0:
        japaneseAnswer(event, userPostback)

    if userPostback.find('翻譯：') == 0:
        translatePostback(event, userPostback)

    if userPostback.find('擷取連結：') == 0:
        url_list = extract_url(userPostback)
        
        # 輸出字串
        url_text = "\n\n".join( url_list )
        
        # 包裝訊息、發送訊息
        text_message = TextSendMessage(text= url_text )
        line_bot_api.reply_message(event.reply_token, text_message)
        return

    if userPostback.find('擷取並移除參數：') == 0:
        url_list = extract_url(userPostback)

        # 輸出字串（移除網址參數）
        url_clean_list = []
        for url in url_list:
            url_clean = url.split('?')[0]
            url_clean_list.append(url_clean)
        url_clean_text = "\n".join( url_clean_list )
        
        # 包裝訊息、發送訊息
        text_message = TextSendMessage(text= url_clean_text )
        line_bot_api.reply_message(event.reply_token, text_message)
        return

    if userPostback.find('縮短網址：') == 0:
        url_list = extract_url(userPostback)

        url_short_list = []
        for url in url_list:
            api_url = 'https://ssur.cc/api.php'
            params = {
                'appkey': 'nZ9ZzSa4LZ4o',
                'format': 'json',
                'longurl': url
            }
            response = requests.get(api_url, params=params)
            data = response.json()

            if response.status_code == 200 and data['code'] == 1:
                short_url = str(data['ae_url'])
                url_short_list.append(short_url)

        # 輸出字串
        url_text = "\n\n".join( url_short_list )

        # 包裝訊息、發送訊息
        text_message = TextSendMessage(text= url_text )
        line_bot_api.reply_message(event.reply_token, text_message)
        return

    if userPostback.find('偷錢：') == 0:
        stealCoinAction(event, userPostback)


# 聲音訊息
@line_handler.add(MessageEvent, message=AudioMessage)
def handle_message_Audio(event):
    
    # 取得使用者傳送的聲音訊息
    message_id = event.message.id
    message_content = line_bot_api.get_message_content(message_id)

    # 取得訊息來源 ID
    source_id = getMessageSourceID(event)   

    # 將聲音儲存到本地端
    with open(f"/tmp/{source_id}.m4a", "wb") as f:
        f.write(message_content.content)

    # 判斷聲音長度不超過 10 秒
    if event.message.duration > 10000:
        text_message = TextSendMessage(text="你講話太長了，超過 10 秒了！")
        line_bot_api.reply_message(event.reply_token, text_message)
        return
    else:
        MessageText = groqWhisper(f"/tmp/{source_id}.m4a")
        text_message = TextSendMessage(text=MessageText)
        line_bot_api.reply_message(event.reply_token, text_message)
        return


# 圖片訊息
@line_handler.add(MessageEvent, message=ImageMessage)
def handle_message_Image(event):
    
    # 取得使用者傳送的圖片訊息
    message_id = event.message.id
    message_content = line_bot_api.get_message_content(message_id)

    # 取得訊息來源 ID
    source_id = getMessageSourceID(event)   

    # 將圖片儲存到本地端
    with open(f"/tmp/{source_id}.jpg", "wb") as f:
        f.write(message_content.content)

    print("圖片訊息")



if __name__ == "__main__":
    app.run()

