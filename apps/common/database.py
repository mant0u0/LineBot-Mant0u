# 資料庫讀寫
import json
from apps.common.firebase import *


# 讀取：暫存檔
def read_database_temporary(path, id):
    # 選擇存取的檔案路徑
    path = "/tmp/"+path+".json"

    try:
        with open(path, 'r') as file:
            data = json.load(file) # 讀取檔案
        try:
            loaded_data = data[id] # 使用 ID 作為 Key 來查詢
            print("[成功] 讀取 JSON 成功")
            return loaded_data

        except:
            print("[錯誤] 無資料")

    except FileNotFoundError:
        print("[錯誤] 找不到指定的檔案")

    except json.JSONDecodeError:
        print("[錯誤] JSON 解碼失敗")
    
    return " "

# 寫入：暫存檔
def write_database_temporary(path, id, data):
    # 選擇存取的檔案路徑
    path = "/tmp/"+path+".json"

    try:
        with open(path, 'r') as file:
            existing_data = json.load(file)
    except FileNotFoundError:
        existing_data = {}
    existing_data[id] = data

    with open(path, 'w') as file:
        json.dump(existing_data, file, indent=4)

# 移除：暫存檔
def remove_database_temporary(path, id):
    # 選擇存取的檔案路徑
    path = "/tmp/"+path+".json"

    try:
        with open(path, 'r') as file:
            existing_data = json.load(file)

    except FileNotFoundError:
        print("[錯誤] 找不到指定的檔案")

    except json.JSONDecodeError:
        print("[錯誤] JSON 解碼失敗")

    try:
        del existing_data[id]
        with open(path, 'w') as file:
            json.dump(existing_data, file, indent=4)
        print(f"[成功] 成功移除 ID {id} 的元素")
    except KeyError:
        print(f"[錯誤] 找不到指定 ID 的元素: {id}")

# -------------------------------------------- #

# Firebase 資料庫：讀取
def read_database_firebase(path, id):
    print("[讀取] read_database_firebase")
    # 選擇讀取的路徑
    file_path = f"{id}/{path}"
    # 讀取
    loaded_data = firebaseGetData(file_path)
    return loaded_data

# Firebase 資料庫：寫入
def write_database_firebase(path, id, data):
    print("[寫入] write_database_firebase")
    # 選擇讀取的路徑
    file_path = f"{id}/{path}"
    # 寫入
    firebaseUpdate(file_path, data)

# Firebase 資料庫：移除
def remove_database_firebase(path, id):
    print("[移除] remove_database_firebase")
    # 選擇讀取的路徑
    file_path = f"{id}/{path}"
    # 移除
    firebaseDelete( file_path )

# -------------------------------------------- #
# 先讀取暫存檔，再去讀取 Firebase 資料庫
# 暫存檔 + Firebase 資料庫：讀取
def read_database_combined(path, id):
    # 選擇存取的檔案路徑
    local_path = "/tmp/"+path+".json"

    # 嘗試讀取本地 JSON
    try:
        with open(local_path, 'r') as file:
            data = json.load(file)
            try:
                return data[id]
            except:
                pass
    except (FileNotFoundError, json.JSONDecodeError):
        pass

    # 讀取 Firebase
    firebase_data =  read_database_firebase(path, id)
    
    if firebase_data:
        # 備份到本地
        write_database_temporary(path, id, firebase_data)
        return firebase_data
    else:
        # 建立空資料
        empty_data = {}
        write_database_temporary(path, id, empty_data)
        write_database_firebase(path, id, empty_data)
        return empty_data
    
# 暫存檔 + Firebase 資料庫：寫入
def write_database_combined(path, id, data):
    # 選擇存取的檔案路徑
    local_path = "/tmp/"+path+".json"

    # 檢查本地 JSON
    try:
        with open(local_path, 'r') as file:
            json.load(file)
        # 有本地檔案，直接寫入
        write_database_temporary(path, id, data)
        write_database_firebase(path, id, data)
    except (FileNotFoundError, json.JSONDecodeError):
        write_database_temporary(path, id, data)
        write_database_firebase(path, id, data)
    
# 暫存檔 + Firebase 資料庫：移除
def remove_database_combined(path, id):
    remove_database_temporary(path, id)
    remove_database_firebase(path, id)

# -------------------------------------------- #
