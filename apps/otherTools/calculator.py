# 計算機
from linebot import LineBotApi
from linebot.models import *

import os

from apps.common.common import *

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))


def calculator(event, userMessage):
    userMessage = userMessage.replace('=', '')

    expression = userMessage
    is_expression, answer = is_math_expression(expression)

    if is_expression:
        userMessage = userMessage.replace(' ', '')
        userMessage = userMessage.replace('+', ' + ')
        userMessage = userMessage.replace('-', ' - ')
        userMessage = userMessage.replace('*', ' × ')
        userMessage = userMessage.replace('/', ' ÷ ')

        # answer = format(answer, '.2f')
        outputText = str(userMessage) + " = " + str(answer)
        
        replyLineMessage = TextSendMessage(outputText)
        line_bot_api.reply_message(event.reply_token, replyLineMessage)