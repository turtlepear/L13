import requests
import streamlit as st
import pandas as pd

API_KEY = "CWA-1FFDDAEC-161F-46A3-BE71-93C32C52829F"
API_URL = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001"

COUNTIES = [
    "宜蘭縣","花蓮縣","臺東縣","澎湖縣","金門縣","連江縣",
    "臺北市","新北市","桃園市","臺中市","臺南市","高雄市",
    "基隆市","新竹縣","新竹市","苗栗縣","彰化縣","南投縣",
    "雲林縣","嘉義縣","嘉義市","屏東縣"
]

ELEMENTS = {
    "降雨機率 PoP": "PoP",
    "最低溫 MinT": "MinT",
    "最高溫 MaxT": "MaxT"
}

st.title("臺灣縣市天氣預報折線圖（氣象局 CWB API）")

location = st.selectbox("選擇縣市：", COUNTIES)
element_key = st.selectbox("選擇折線圖資料：", list(ELEMENTS.keys()))
element = ELEMENTS[element_key]

if st.button("顯示折線圖"):

    params = {
        "Authorization": API_KEY,
        "locationName": location,
        "elementName": element,
        "format": "JSON",
        "sort": "time"
    }

    response = requests.get(API_URL, params=params)
    data = response.json()

    # 找資料
    records = data["records"]["location"][0]["weatherElement"][0]["time"]

    rows = []
    for r in records:
        start = r["startTime"]
        value = r["parameter"]["parameterName"]   # 數字（字串）
        rows.append([start, float(value)])

    df = pd.DataFrame(rows, columns=["startTime", element])
    df["startTime"] = pd.to_datetime(df["startTime"])

    # 顯示原始資料表
    st.subheader("資料表")
    st.dataframe(df)

    # 折線圖
    st.subheader(f"{location} - {element_key}（折線圖）")
    st.line_chart(df.set_index("startTime")[element])
