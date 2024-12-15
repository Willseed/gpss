import os
import requests
import json
from datetime import datetime


"""
這段程式碼從 'company_list.txt' 檔案中讀取公司名稱，並對每個公司名稱發送 HTTP GET 請求以獲取相關的 JSON 數據，然後將這些數據儲存到 'data' 資料夾中的相應 JSON 檔案中。
變數:
    doc (str): 包含公司名稱的檔案名稱。
    dir_name (str): 儲存 JSON 檔案的資料夾名稱。
步驟:
1. 打開 'company_list.txt' 檔案並讀取所有公司名稱。
2. 對每個公司名稱發送 HTTP GET 請求以獲取相關的 JSON 數據。
3. 將獲取的 JSON 數據格式化並儲存到 'data' 資料夾中的相應 JSON 檔案中。
注意:
- 請確保 'company_list.txt' 檔案存在且包含公司名稱。
- 請確保有網路連線以發送 HTTP GET 請求。
"""

def get_data(auth: str, company_name: str):
    """
    根據提供的授權碼和公司名稱，從指定的 API 獲取數據。
    參數:
    auth (str): 授權碼，用於 API 認證。
    company_name (str): 公司名稱，用於查詢數據。
    返回:
    dict: 包含 API 響應數據的字典格式。
    """

    url = f'https://tiponet.tipo.gov.tw/gpss1/gpsskmc/gpss_api?userCode={auth}&patDB=TWA,TWB,TWD&patAG=A,B&patTY=I,M,D&AX={company_name.strip()}&ID=20150101:20241231&expFld=PN,AN,ID,AD,TI&expFmt=json&expQty=10000'
    response =  requests.get(url)
    return response.json()

def write_data(company_name: str, json_data: str) -> None:
    dir_name = 'data'
    os.path.exists(dir_name) or os.makedirs(dir_name)
    with open(f'data/{company_name.strip()}.json', 'w', encoding='utf-8') as file:
        file.write(json_data)
    print(f"開始時間: {start_time}，當前時間: {datetime.now()}，公司名稱：{company_name.strip()}，已完成！")

def data_unpack(auth: str, company_name: str) -> tuple:
    """
    將 JSON 數據解包為公司名稱和數據列表。
    參數:
    json_data (dict): 包含公司名稱和數據列表的 JSON 數據。
    返回:
    tuple: 公司名稱和數據列表。
    """

    data = get_data(auth, company_name)
    json_data = json.dumps(data, indent=4, ensure_ascii=False)
    json_dict = json.loads(json_data)
    return data, json_data, json_dict

auth_doc = 'auth.txt'
with open(auth_doc, 'r', encoding='utf-8') as file:
    auth_list = file.readlines()
start_time = datetime.now()
doc = 'company_list.txt'

index = 0
auth = auth_list[index].strip()
print(f"開始時間: {start_time}，授權碼：{auth}，公司名稱檔案：{doc}，開始執行！")
with open(doc, 'r', encoding='utf-8') as file:
    data = file.readlines()
    for company_name in data:
        raw_json, json_data, json_dict = data_unpack(auth, company_name)
        if json_dict['gpss-API']['status'] == "fail":
            print(f"API 回應失敗，公司名稱：{company_name.strip()}: {json_dict['gpss-API']['status']}")
            index += 1
            auth = auth_list[index].strip()
            if index == len(auth_list):
                print(f"授權碼已用完，公司名稱：{company_name.strip()}，已結束！")
                exit()
            raw_json, json_data, json_dict = data_unpack(auth, company_name)
        write_data(company_name, json_data)
