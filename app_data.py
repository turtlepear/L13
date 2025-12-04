import streamlit as st
import requests
import pandas as pd
import sqlite3

# 固定 API KEY（不需要使用者輸入）
API_KEY = "CWA-1FFDDAEC-161F-46A3-BE71-93C32C52829F"
API_URL = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001"
DB_NAME = "weather.db"


# -----------------------------
# 初始化 SQLite 資料庫
# -----------------------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS weather (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location TEXT,
            element TEXT,
            start_time TEXT,
            end_time TEXT,
            value TEXT
        );
    """)
    conn.commit()
    conn.close()


# -----------------------------
# 儲存資料進 SQLite
# -----------------------------
def save_to_db(df):
    conn = sqlite3.connect(DB_NAME)
    df.to_sql("weather", conn, if_exists="append", index=False)
    conn.close()


# -----------------------------
# 從 SQLite 讀取資料
# -----------------------------
def load_from_db(location=None):
    conn = sqlite3.connect(DB_NAME)

    query = "SELECT * FROM weather"

    if location and location != "全部":
        query += f" WHERE location = '{location}'"

    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


# =============================
# Streamlit UI
# =============================
st.title("🌦️ 台灣天氣查詢")

init_db()

# 可選縣市
locations = [
    "宜蘭縣","花蓮縣","臺東縣","澎湖縣","金門縣","連江縣",
    "臺北市","新北市","桃園市","臺中市","臺南市","高雄市",
    "基隆市","新竹縣","新竹市","苗栗縣","彰化縣","南投縣",
    "雲林縣","嘉義縣","嘉義市","屏東縣"
]

elements = ["Wx", "PoP", "CI", "MinT", "MaxT"]

st.subheader("🔍 查詢最新天氣資料")

selected_locations = st.multiselect("選擇縣市：", locations)
selected_elements = st.multiselect("選擇天氣要素：", elements)


# -----------------------------
# 查詢按鈕
# -----------------------------
if st.button("取得最新天氣資料"):
    params = {
        "Authorization": API_KEY,
        "format": "JSON"
    }

    if selected_locations:
        params["locationName"] = selected_locations
    if selected_elements:
        params["elementName"] = selected_elements

    try:
        response = requests.get(API_URL, params=params, timeout=10, verify=False)
        response.raise_for_status()
    except Exception as e:
        st.error(f"API 錯誤：{e}")
        st.stop()

    try:
        records = response.json()["records"]["location"]
    except:
        st.error("JSON 格式錯誤")
        st.stop()

    rows = []
    for loc in records:
        loc_name = loc["locationName"]

        for weather in loc["weatherElement"]:
            ele = weather["elementName"]

            for t in weather["time"]:
                start = t.get("startTime", "")
                end = t.get("endTime", "")
                value = t["parameter"]["parameterName"]

                rows.append([loc_name, ele, start, end, value])

    df = pd.DataFrame(rows, columns=["location", "element", "start_time", "end_time", "value"])

    st.success("✔ 天氣資料取得成功！")
    st.dataframe(df)

    save_to_db(df)
    st.info("✔ 資料已寫入 SQLite（weather.db）")


# -----------------------------
# 歷史資料顯示 + 折線圖
# -----------------------------
st.subheader("📂 查詢歷史資料")

hist_loc = st.selectbox("選擇縣市（可選）", ["全部"] + locations)

if st.button("載入歷史資料"):
    df_history = load_from_db(hist_loc)

    if df_history.empty:
        st.warning("⚠ 尚無資料")
    else:
        st.dataframe(df_history)

        # 折線圖限定：MinT / MaxT / PoP
        df_plot = df_history[df_history["element"].isin(["MinT", "MaxT", "PoP"])]

        # 保留可轉換數字的資料
        df_plot = df_plot[df_plot["value"].str.replace(".", "", 1).str.isnumeric()]
        df_plot["value"] = df_plot["value"].astype(float)

        # 時間排序
        df_plot = df_plot.sort_values("start_time")

        st.subheader("📈 折線圖（MinT / MaxT / PoP）")

        if df_plot.empty:
            st.info("沒有可用來畫折線圖的資料")
        else:
            chart_data = df_plot.pivot_table(
                index="start_time",
                columns="element",
                values="value"
            )

            st.line_chart(chart_data)

