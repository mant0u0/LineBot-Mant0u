# 饅頭機器人

## 簡介

饅頭聊天機器人，主要是一個在 LINE 上的一個聊天機器人。你可以直接跟機器人對話，使用特定的「關鍵字」可以觸發「機器人功能」；也可以直接邀請至群組內，跟朋友一起遊玩。

原先是希望能做一台，有各種亂數功能的機器人，結果功能不小心越做越多。最近還加入了許多 Gemini AI 的應用在一些功能上。為了能讓大家使用起來覺得有趣，花比較多時間在處理介面的圖片繪製上，希望大家會喜歡～ (´･ω･`)

![Image](static/page/img-1.png)

## 使用方法

> [!CAUTION]  
> 免責聲明
>
> 此程式所讀取訊息、圖片，皆為暫存使用，不對其長時間保存，因此不對使用者之訊息、圖片等個人資料負責。
>
> 貨幣匯率資料僅供參考，對於因使用或依賴匯率資料而導致的任何損失或損害，概不負責。

> [!WARNING]  
> 注意事項
>
> 試用時如果有出現「Gemini API 請求失敗」的訊息，表示 Gemini 免費版的使用額度已經達到上限。如果可以的話還是建議自行架設，可以使用自己的 API KEY 來玩～
>
> 由於這個機器人沒有使用任何的資料庫來記錄使用紀錄，目前遊玩紀錄都是直接寫入暫存資料夾內，可能會被 Vercel 不定時清除。建議自行架設後，可以改寫成存入資料庫中～

- 點擊以下連結，至 LINE APP 中，將機器人加為好友；直接進行對話即可使用。

  [📔 饅頭機器人](https://liff.line.me/1645278921-kWRPP32q/?accountId=543ihgir)

## 自行架設

> [!NOTE]  
> 事前準備
>
> 需準備 Github、Vercel、Line Developers 帳號。
> 略懂 Python 程式語法。

- 此專案需部屬至 Vercel 伺服器，部屬時所需設定的環境變數（Environment Variables）

### 環境變數

1. LINE
   - `LINE_CHANNEL_ACCESS_TOKEN`：於 Line Developers 後台取得
   - `LINE_CHANNEL_SECRET`：於 Line Developers 後台取得
2. Firebase - Realtime Database
   - `FIREBASE_URL`：資料庫讀寫的網址。
   - `FIREBASE_PRIVATE_KEY`：資料庫的私密金鑰，由 serviceAccountKey.json 檔取得。
   - `FIREBASE_CLIENT_EMAIL`：一串 EMAIL，由 serviceAccountKey.json 檔取得。
   - `FIREBASE_CLIENT_X509_CERT_URL`：一串連結，由 serviceAccountKey.json 檔取得。
3. 其他
   - `IMGBB_KEY`：於 ImgBB 登入後取得，若不需要可以先移除「以圖搜圖」功能。
   - `GEMINI_KEY`：於 Google AI Studio 取得，注意選用時的方案是否免費。若不需要可以先移除「AI」功能。
   - `GROQ_API_KEY`：Groq 的 AI 服務，於 Groq 登入取得。
   - `MANT0U_BOT_MODEL`：測試用可以亂打，輸入「private」可以觸發測試語法。

- 詳細部屬教學可以參考此簡報。

  [📔 簡報 - LINE 機器人架設教學](https://mant0u.pse.is/5cnleb)

## 機器人功能

- 饅頭 AI 聊天功能 (ai)
- 搜尋引擎 (search)
- 翻譯功能 (translate)
- Twitter 擷取訊息 (fixTwitter)
- 貨幣換算 (currency)
- 海盜桶 (gamePopUpPirate)
- 一番賞 (gameIchiban)
- 扭蛋機 (randomGashapon)
- 猜拳 (gameRPS)
- 手槍 (gameGun)
- 亂數 (randomNumber)
- 硬幣 (randomCoin)
- 拉霸 (randomSlot)
- 擲筊 (randomBwaBwei)
- 骰子 (randomDice)
- 抽籤 (randomOkamikuji)
- 是不是、要不要、有沒有 (randomYesOrNo)
- 哪個 (randomWhichOne)
- 撲克牌 (randomPoker)
- 洗牌/翻牌 (randomShuffle)
- 塔羅牌 (randomTarotCards)
- 日曆 (calendar)
- 計算機 (calculator)
- 日文單字 (japanese)

![Image](static/page/img-2.png)

## 程式與目錄說明

- **index.py**

  機器人的主程式，主要是拿來設定特定訊息的「關鍵字」，會觸發什麼樣的「功能」。

- **apps**

  這個目錄下，依據不同的小功能分了很多資料夾。其中每個小功能的主要程式，皆命名為「main.py」，如果有「example.py」通常是拿來記錄 Flex Message 的 json 結構的。

- **static**

  這個路徑主要是用來放「圖片」用的，由於 LINE 的 Flex Message 或其他圖片訊息，傳送時需要「圖片連結」，為了需要獲取專案下的圖片連結，需要將圖片放在這個目錄下才拿的到圖片連結。當然也可以將圖片存在外部圖庫。

- **tmp**

  這個路徑作為伺服器暫時存放檔案用，由於這個專案使用 Vercel 進行部屬，暫存檔案一定要放進這個資料夾內，才能夠進行讀寫。雖然內部的檔案，Vercel 會不定期清除，但因為不想另外開資料庫，所以就先把一些遊戲紀錄存在這邊了。（例如：猜拳、海盜桶、扭蛋機...等使用紀錄）

- **requirements.txt**

  記錄專案所需要的第三方套件與其版本資訊。這個檔案可以提示並幫助伺服器或開發者安裝對應的第三方套件，確保專案在不同環境中能夠一致地運行。

## 程式紀錄暫存與資料庫

- 於專案目錄「/apps/common/database.py」的這個程式，主要是寫「紀錄讀取/寫入/移除」的功能。用於製作需要紀錄遊玩狀態的功能，例如：扭蛋機、一番賞、海盜桶等。
- 「database.py」程式中，針對「紀錄讀取/寫入/移除」都有寫三種寫法，分別為「temporary（暫存）」、「firebase（資料庫）」、「combined（暫存+資料庫）」。
  - temporary：資料會讀寫於專案目錄「/tmp」中，這是 Vercel 提供目錄中唯一可以寫入資料的路徑。優點是讀寫很快，但缺點是裡面的資料會不定期移除。
  - firebase：資料會保存到 Firebase 的 Realtime Database 中。只要在 firebase 開一個專案後，使用 Realtime Database 服務即可使用；詳細設定的方法下面會解釋。
  - combined：就是以上兩種的結合，為了避免讀取 firebase 時間過久，會利用 temporary 先存暫時的紀錄，必要的時候再同步紀錄。
- Firebase Realtime Database 的設定方式
  - 避免資料庫公開，使用時須設定讀寫權限，需要使用 Firebase 的認證金鑰來限制使用者。
  - 需要設定四個環境變數：`FIREBASE_URL`、`FIREBASE_PRIVATE_KEY`、`FIREBASE_CLIENT_EMAIL`、`FIREBASE_CLIENT_X509_CERT_URL`
  - 於 Firebase 專案中「專案設定 > 服務帳戶」的這個頁面，可以先看到 `databaseURL:"https://.....`，這個就是 `FIREBASE_URL` 。
  - 於該頁面下方點選「產生新的金鑰」按鈕，可以得到其他三個環境變數 `FIREBASE_PRIVATE_KEY`、`FIREBASE_CLIENT_EMAIL`、`FIREBASE_CLIENT_X509_CERT_URL`。
  - Realtime Database 的「規則」設定：
    ```json
    {
      "rules": {
        ".read": "auth.admin === true",
        ".write": "auth.admin === true"
      }
    }
    ```

## 參考網站、專案、API

- **Google Gemini**

  由 Google 所提供的 Gemini AI API。此專案是使用免費方案，製作「聊天機器人、抽籤問運勢、擲筊問運勢、塔羅牌占卜、扭蛋機項目產生、日文單字例句產生」等功能。

  [📒 官方網站 - Google AI for Developers](https://ai.google.dev/)

  [📒 官方網站 - Google AI Studio](https://aistudio.google.com/app/prompts/new_chat?hl=zh-tw)

  [📗 參考文件 - _如何使用 Google 的 Gemini 模型 API？ (基礎教學，附上 Python 範例程式)_ - 文章作者：Jia](https://blog.jiatool.com/posts/gemini_api/)

- **OpenAI**

  由 OpenAI 所提供的 AI API。因為需要付費因此沒有使用，但還是有留測試用的程式碼，如果有自己的 KEY 也可以使用。

  [📒 官方網站 - Openai](https://openai.com/index/openai-api/)

- **FixTweet (fxtwitter.com)**

  主要是用來加強 Discord、Telegram 平台上的 Twitter 訊息嵌入功能。此專案利用這個 API 製作 Twitter 訊息擷取工具，可以擷取 Twitter 的文字、圖片、影片直接使用 Flex Message 在 LINE 中顯示。

  [📕 說明文件](https://docs.fxtwitter.com/en/latest/index.html)

  [📘 專案 Github](https://github.com/FixTweet/FxTwitter/tree/readthedocs)

- **InstaFix**

  功能與 FixTweet 類似，利用個這專案提供的 Instagram 貼文資訊，擷取部分文字、圖片、影片直接使用 Flex Message 在 LINE 中顯示。

  [📘 專案 Github](https://github.com/Wikidepia/InstaFix?tab=readme-ov-file)

- **繁化姬**

  此專案使用了繁化姬的 API 服務，用來處理部分文字的簡轉繁功能。由於此專案為個人免費使用，如果要進行商葉用途，請聯繫 API 作者付費使用。

  [📒 官方網站 - 繁化姬 - 繁簡轉換、台灣化](https://zhconvert.org/)

  [📕 說明文件](https://docs.zhconvert.org/)

- **Imgbb API**

  一個免費的圖片上傳服務，提供時限自動刪除的功能。此專案利用這個圖片上傳服務，取得訊息圖片連結後，可至多個網站進行以圖搜圖。

  [📒 官方網站](https://zh-tw.imgbb.com/)

  [📕 說明文件](https://api.imgbb.com/)

- **Coinbase API**

  這個 API 提供了各國貨幣的匯率，除了一般貨幣外也有提供許多加密貨幣的匯率。此專案利用這 API 製作簡單的貨幣換算功能。

  [📒 官方網站 - Coinbase](https://www.coinbase.com/)

  [📕 說明文件](https://docs.cloud.coinbase.com/sign-in-with-coinbase/docs/api-users)

- **Soundoftext API**

  這個 API 使用 Google Translate 的文字轉語音引擎，提供語音的 MP3 連結。此專案利用這 API 製作日文單字、例句語音功能。由於 Google Translate 提供的網址，無法直接在 LINE 音訊訊息中使用，因此才選用這個 API。

  [📒 官方網站 - Coinbase](https://soundoftext.com/)

  [📕 說明文件](https://soundoftext.com/docs)

## 開源授權規定

- 本專案為個人專案，禁止擅自挪用進行商業用途。

- 此專案可供程式撰寫之參考，歡迎自行下載改寫、研究、部屬。

- 若改寫此專案，請勿再使用「Mant0u Bot、饅頭機器人」等名稱稱呼相關程式或服務，避免造成混淆。

- 如有引用此專案，請註明此專案連結（ https://github.com/mant0u0/LineBot-Mant0u ），感謝配合。

## 特別感謝

特別感謝 [GDG Kaohsiung](https://gdg.community.dev/gdg-kaohsiung/) 社群與主辦人 Andy。在每月第二個禮拜二晚上七點於高雄舉辦的 TOOCON 軟體交流聚會，感謝給我機會於 TOOCON#12 上台分享這個專案，順便附上當天的簡報～ ٩( 'ω' )و

- 感謝 GDG Kaohsiung 社群

- 感謝 TOOCON 主辦人 Andy

  [📔 簡報 - 隨機亂數在小專案開發中的應用與心得分享](https://mant0u.pse.is/5fxnt2)

## 抖內支持

如果你喜歡這個小程式，覺得這個專案有幫助到你的話。歡迎抖內，感謝大家～ (っ ´▽`)っ

- 饅頭小小貼圖：https://store.line.me/emojishop/product/62777d4502450a0831384a1a/zh-Hant
