# 擲硬幣功能（進階版本）

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

import os
import random
from apps.common.common import *

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))


def randomCoinAdvanced(event, userMessage):

	# 指令擷取
	userMessage = userMessage.replace('硬幣：', '')

	# 硬幣種類
	coinType = ["copper", "silver", "gold"]
	coinType = str(random.choice(coinType))


	# flexMessage 容器
	flex_message_contents = []
	coinMode = ""

	# 連續擲硬幣模式
	if userMessage == "正面" or userMessage== "反面":
		result =[]
		count = 0
		headCount = 0
		tailsCount = 0

		if userMessage=="正面":
			coinMode = "連續擲正面"

			# 模擬擲硬幣，擲到反面出現為止
			while True:
				result_once = random.randint(0, 1)
				count += 1
				if result_once == 1:
					headCount += 1
					result.append( 1 )
				else:
					tailsCount += 1
					result.append( 0 )
					break
			
			# 結果文字
			resultText = f"連續擲出 {str(headCount)} 次正面" 
			if headCount == 0:
				resultText = f"沒有擲出半個正面..."

			# 正面
			firstPageContents = [
				{
					"type": "box",
					"layout": "vertical",
					"width": "40%",
					"contents": [
					{
						"type": "image",
						"url": localImg(f"randomCoinAdvanced/{coinType}_heads_3.png")
					},
					{
						"type": "box",
						"layout": "vertical",
						"backgroundColor": "#ff5e3e",
						"justifyContent": "center",
						"alignItems": "center",
						"position": "absolute",
						"paddingAll": "4px",
						"paddingStart": "12px",
						"paddingEnd": "12px",
						"cornerRadius": "xxl",
						"offsetEnd": "0px",
						"offsetTop": "0px",
						"contents": [
						{
							"type": "text",
							"text": str(headCount),
							"color": "#ffffff",
							"size": "lg",
							"weight": "bold"
						}
						],
					}
					],
				},
			]

		if userMessage=="反面":
			coinMode = "連續擲反面"

			# 模擬擲硬幣，擲到正面出現為止
			while True:
				result_once = random.randint(0, 1)
				count += 1
				if result_once == 0:
					tailsCount += 1
					result.append( 0 )
				else:
					headCount += 1
					result.append( 1 )
					break

			# 結果文字
			resultText = f"連續擲出 {str(tailsCount)} 次反面"
			if tailsCount == 0:
				resultText = f"沒有擲出半個反面..."

			# 反面
			firstPageContents = [
				{
					"type": "box",
					"layout": "vertical",
					"width": "40%",
					"contents": [
					{
						"type": "image",
						"url": localImg(f"randomCoinAdvanced/{coinType}_tails.png")
					},
					{
						"type": "box",
						"layout": "vertical",
						"backgroundColor": "#87bce8",
						"justifyContent": "center",
						"alignItems": "center",
						"position": "absolute",
						"paddingAll": "4px",
						"paddingStart": "12px",
						"paddingEnd": "12px",
						"cornerRadius": "xxl",
						"offsetEnd": "0px",
						"offsetTop": "0px",
						"contents": [
						{
							"type": "text",
							"text": str(tailsCount),
							"color": "#ffffff",
							"size": "lg",
							"weight": "bold"
						}
						],
					}
					],
				}
			]

		# 第一頁
		firstPageTemplate = {
			"type": "bubble",
			"body": {
				"type": "box",
				"layout": "vertical",
				"backgroundColor": "#f2f3f4",
				"paddingAll": "0px",
				"contents": [

				# 底部背景
				{
					"type": "image",
					"url": localImg(f"randomCoinAdvanced/bottom.png"),
					"size": "full",
					"aspectMode": "cover",
					"aspectRatio": "1:1",
					"gravity": "top"
				},

				# 硬幣數量文字
				{
					"type": "box",
					"layout": "vertical",
					"contents": [
						{
							"type": "box",
							"layout": "vertical",
							"contents": [
							{
								"type": "text",
								"text": f"總共擲出 {str(count)} 次硬幣",
								"color": "#2168a3"
							}
							],
							"backgroundColor": "#ffffff",
							"justifyContent": "center",
							"alignItems": "center",
							"paddingAll": "4px",
							"paddingStart": "16px",
							"paddingEnd": "16px",
							"cornerRadius": "xxl"
						}
					],
					"width": "100%",
					"position": "absolute",
					"justifyContent": "center",
					"alignItems": "center",
					"paddingTop": "28px"
				},
				
				# 正面/反面 統計
				{
					"type": "box",
					"layout": "horizontal",
					"width": "100%",
					"height": "80%",
					"position": "absolute",
					"paddingAll": "12px",
					"spacing": "8px",
					"justifyContent": "center",
					"alignItems": "center",
					"paddingTop": "40px",
					"contents": firstPageContents
				},
				
				# 底部結果文字
				{
					"type": "box",
					"layout": "horizontal",
					"position": "absolute",
					"offsetBottom": "0px",
					"offsetStart": "0px",
					"offsetEnd": "0px",
					"paddingAll": "20px",
					"contents": [
						{
							"type": "box",
							"layout": "vertical",
							"contents": [
								{
									"type": "box",
									"layout": "horizontal",
									"contents": [
										{
											"type": "text",
											"text": resultText,
											"size": "lg",
											"color": "#2168a3",
											"weight": "bold",
											"align": "center"
										}
									]
								}
							],
							"spacing": "xs"
						}
					],
				}

				],
				"action": {
					"type": "message",
					"label": "action",
					"text": "硬幣：" + userMessage,
				},
			}
		}
		flex_message_contents.append( firstPageTemplate )

	# 擲固定次數模式
	if userMessage.isdigit() and int(userMessage)>0:

		coinMode = "固定次數"

		# 擲硬幣次數
		count = int(userMessage)

		# 產生長度為 count 的隨機 0 和 1 的列表
		result = [random.randint(0, 1) for _ in range(count)]
		
		# 統計正反面數量
		tailsCount = 0
		headCount = 0
		for i in result:
			if i == 0:
				tailsCount += 1
			else:
				headCount += 1
		
		# 結果文字
		resultText = f"正面 {str(headCount)} 枚，反面 {str(tailsCount)} 枚" 

		# 第一頁
		firstPageTemplate = {
			"type": "bubble",
			"body": {
				"type": "box",
				"layout": "vertical",
				"backgroundColor": "#f2f3f4",
				"paddingAll": "0px",
				"contents": [

				# 底部背景
				{
					"type": "image",
					"url": localImg(f"randomCoinAdvanced/bottom.png"),
					"size": "full",
					"aspectMode": "cover",
					"aspectRatio": "1:1",
					"gravity": "top"
				},

				# 硬幣數量文字
				{
					"type": "box",
					"layout": "vertical",
					"contents": [
						{
							"type": "box",
							"layout": "vertical",
							"contents": [
							{
								"type": "text",
								"text": f"擲出 {str(count)} 枚硬幣",
								"color": "#2168a3"
							}
							],
							"backgroundColor": "#ffffff",
							"justifyContent": "center",
							"alignItems": "center",
							"paddingAll": "4px",
							"paddingStart": "16px",
							"paddingEnd": "16px",
							"cornerRadius": "xxl"
						}
					],
					"width": "100%",
					"position": "absolute",
					"justifyContent": "center",
					"alignItems": "center",
					"paddingTop": "28px"
				},
				
				# 正面/反面 統計
				{
					"type": "box",
					"layout": "horizontal",
					"width": "100%",
					"height": "80%",
					"position": "absolute",
					"paddingAll": "12px",
					"spacing": "8px",
					"justifyContent": "center",
					"alignItems": "center",
					"paddingTop": "40px",
					"contents": [
						# 正面
						{
							"type": "box",
							"layout": "vertical",
							"width": "40%",
							"contents": [
							{
								"type": "image",
								"url": localImg(f"randomCoinAdvanced/{coinType}_heads_3.png")
							},
							{
								"type": "box",
								"layout": "vertical",
								"backgroundColor": "#ff5e3e",
								"justifyContent": "center",
								"alignItems": "center",
								"position": "absolute",
								"paddingAll": "4px",
								"paddingStart": "12px",
								"paddingEnd": "12px",
								"cornerRadius": "xxl",
								"offsetEnd": "0px",
								"offsetTop": "0px",
								"contents": [
								{
									"type": "text",
									"text": str(headCount),
									"color": "#ffffff",
									"size": "lg",
									"weight": "bold"
								}
								],
							}
							],
						},

						# 反面
						{
							"type": "box",
							"layout": "vertical",
							"width": "40%",
							"contents": [
							{
								"type": "image",
								"url": localImg(f"randomCoinAdvanced/{coinType}_tails.png")
							},
							{
								"type": "box",
								"layout": "vertical",
								"backgroundColor": "#87bce8",
								"justifyContent": "center",
								"alignItems": "center",
								"position": "absolute",
								"paddingAll": "4px",
								"paddingStart": "12px",
								"paddingEnd": "12px",
								"cornerRadius": "xxl",
								"offsetEnd": "0px",
								"offsetTop": "0px",
								"contents": [
								{
									"type": "text",
									"text": str(tailsCount),
									"color": "#ffffff",
									"size": "lg",
									"weight": "bold"
								}
								],
							}
							],
						}
					],

				},
				
				# 底部結果文字
				{
					"type": "box",
					"layout": "horizontal",
					"position": "absolute",
					"offsetBottom": "0px",
					"offsetStart": "0px",
					"offsetEnd": "0px",
					"paddingAll": "20px",
					"contents": [
						{
							"type": "box",
							"layout": "vertical",
							"contents": [
								{
									"type": "box",
									"layout": "horizontal",
									"contents": [
										{
											"type": "text",
											"text": resultText,
											"size": "lg",
											"color": "#2168a3",
											"weight": "bold",
											"align": "center"
										}
									]
								}
							],
							"spacing": "xs"
						}
					],
				}

				],
				"action": {
					"type": "message",
					"label": "action",
					"text": "硬幣：" + userMessage,
				},

			}
		}
		flex_message_contents.append( firstPageTemplate )


	if len(result) <= 27:

		rowContents = []

		# 顯示硬幣
		for i in range(count):
			# 反面
			if result[i] == 0:
				coinTemplate = {
					"type": "image",
					"url": localImg(f"randomCoinAdvanced/{coinType}_tails_opacity.png"),
					"aspectMode": "fit",
					"size": "sm"
				}
				if coinMode == "連續擲反面":
					coinTemplate = {
						"type": "image",
						"url": localImg(f"randomCoinAdvanced/{coinType}_tails.png"),
						"aspectMode": "fit",
						"size": "sm"
					}


			# 正面
			else:
				# 隨機 1~3
				randomNum = str(random.randint(1, 3))
				coinTemplate = {
					"type": "image",
					"url": localImg(f"randomCoinAdvanced/{coinType}_heads_{randomNum}.png"),
					"aspectMode": "fit",
					"size": "sm"
				}
				if coinMode == "連續擲反面":
					coinTemplate = {
						"type": "image",
						"url": localImg(f"randomCoinAdvanced/{coinType}_heads_opacity.png"),
						"aspectMode": "fit",
						"size": "sm"
					}
				
			
			rowContents.append( coinTemplate )
		
		# 補上空白：是否為 9 的倍數 (一頁最多 9 個硬幣)
		nullTemplate = {
			"type": "image",
			"url": localImg(f"randomCoinAdvanced/null.png"),
			"aspectMode": "fit",
			"size": "sm"
		}
		if len(rowContents) % 9 != 0:
			for i in range(9 - (len(rowContents) % 9)):
				rowContents.append( nullTemplate )

		# 分行：每 3 個放一行
		rowGroupContents = []
		for i in range(0, len(rowContents), 3):
			# 取出 3 個放一行
			rowContents_temp = rowContents[i:i+3]
			rowTemplate = {
				"type": "box",
				"layout": "horizontal",
				# "borderWidth": "1px",
				# "borderColor": "#ff0000",
				"width": "100%",
				"spacing": "4px",
				"paddingStart": "2%",
				"contents": rowContents_temp
			}
			rowGroupContents.append( rowTemplate )


		# 分頁：每 3 行放一頁
		for i in range(0, len(rowGroupContents), 3):
			# 取出 3 行放一頁
			rowGroupContents_temp = rowGroupContents[i:i+3]
			pageTemplate = {
				"type": "bubble",
				"body": {
					"type": "box",
					"layout": "vertical",
					"paddingAll": "0px",
					"backgroundColor": "#f2f3f4",
					"contents": [
						{
							"type": "box",
							"layout": "vertical",
							# "borderWidth": "1px",
							# "borderColor": "#000000",
							"width": "100%",
							"height": "100%",
							"position": "absolute",
							"paddingAll": "12px",
							"spacing": "8px",
							"justifyContent": "center",
							"contents": rowGroupContents_temp[:3]
						}
					],
				}
			}
			flex_message_contents.append( pageTemplate )


	if flex_message_contents != []:
		# 包裝訊息
		flex_message = FlexSendMessage(
				alt_text= '有人擲出硬幣！',
				contents={
					"type": "carousel",
					"contents": flex_message_contents
					},
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=MessageAction(label = "再擲一次", text = "硬幣：" + userMessage )
                        ),
                    ]
                )
			)
		
		# 發送訊息
		line_bot_api.reply_message(event.reply_token, flex_message)




