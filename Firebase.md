# 資料庫結構

userInfo .................... 使用者資訊

- user_id ................... 使用者 ID
  - user_id ................. 使用者 ID
  - line_name ............... LINE 名稱
  - group ................... 群組
    - groupID ............... 群組 ID
  - latest_update ........... 最後更新時間

groupInfo ................... 群組資訊

- groupId ................... 群組/使用者/訊息來源 ID
  - member .................. 成員
    - user_id ............... 使用者 ID
      - line_name ............... LINE 名稱
      - main_name ............... 主要名稱
      - coin ................ 金幣
  - randomGashapon .......... 其他功能紀錄
  - randomDice .............. 其他功能紀錄