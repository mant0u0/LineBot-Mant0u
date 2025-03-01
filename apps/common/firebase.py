import requests
import json
import os
import firebase_admin
from firebase_admin import credentials, initialize_app

# Firebase Realtime Database 的 URL
# firebase_url = "https://mant0u-bot-653e5-default-rtdb.asia-southeast1.firebasedatabase.app/"
firebase_url = os.getenv("FIREBASE_URL")


# Firebase 服務帳號憑證
firebase_account = {
	"type": "service_account",
    "private_key": os.getenv("FIREBASE_PRIVATE_KEY").replace('\\n', '\n'),
    "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
	"auth_uri": "https://accounts.google.com/o/oauth2/auth",
	"token_uri": "https://oauth2.googleapis.com/token",
	"auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": os.getenv("FIREBASE_CLIENT_X509_CERT_URL"),
}


# 初始化 Firebase
if not firebase_admin._apps:
	cred = credentials.Certificate(firebase_account)
	initialize_app(cred, {
		'databaseURL': firebase_url,
		'databaseAuthVariableOverride': {
			'uid': 'admin',
			'admin': True
		}
	})
	
def get_id_token():
	"""獲取身份驗證 Token """
	return credentials.Certificate(firebase_account).get_access_token().access_token


# 取得 firebase
def firebaseGetData( path = "" ):
	try:
		response = requests.get(
			f"{firebase_url}{path}.json?access_token={get_id_token()}"
		)
		
		if response.status_code == 200:
			data = response.json()
			print(f"[讀取成功] 路徑 {path}: {str(data)}")
			return data
		else:
			print(f"[錯誤] 狀態碼: {response.status_code}, 訊息: {response.text}")
			return {}
			
	except Exception as e:
		print(f"[錯誤] 讀取資料失敗: {str(e)}")
		return {}

        
# 更新覆寫 firebase
def firebaseUpdate( path = "", data = {} ):
	try:
		response = requests.patch(
			f"{firebase_url}{path}.json?access_token={get_id_token()}",
			data=json.dumps(data)
		)
		
		if response.status_code == 200:
			print(f"[更新成功] 路徑 {path}: {str(data)}")
			return True
		else:
			print(f"[錯誤] 狀態碼: {response.status_code}, 訊息: {response.text}")
			return False
			
	except Exception as e:
		print(f"[錯誤] 更新資料失敗: {str(e)}")
		return False


# 刪除資料
def firebaseDelete( path = "" ):
	try:
		response = requests.delete(
			f"{firebase_url}{path}.json?access_token={get_id_token()}"
		)
		
		if response.status_code == 200:
			print(f"[刪除成功] 路徑: {path}")
			return True
		else:
			print(f"[錯誤] 狀態碼: {response.status_code}, 訊息: {response.text}")
			return False
			
	except Exception as e:
		print(f"[錯誤] 刪除資料失敗: {str(e)}")
		return False