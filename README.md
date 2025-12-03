# 📌 AIOT HW — 中央氣象局資料＋電影爬蟲＋Streamlit 展示

https://dqzusrnbhqcxdufard58qr.streamlit.app/


這個專案包含兩個部分：
---

## 🟦 Part 1：中央氣象局（CWA）資料處理與 Streamlit 視覺化

本專案會：

1. 呼叫中央氣象局氣象開放資料 API  
2. 下載 JSON 氣象資料  
3. 儲存到 SQLite 資料庫 `data.db`  
4. 在 Streamlit 畫面顯示  
5. 使用折線圖（matplotlib 或 plotly）視覺化資料  

### 🔗 使用連結：

| 功能 | 連結 |
|------|------|
| 中央氣象局範例網頁 | https://www.cwa.gov.tw/V8/C/W/OBS_Temp.html |
| CWA Login | https://opendata.cwa.gov.tw/userLogin |
| JSON 資料來源 | https://opendata.cwa.gov.tw/dataset/forecast/F-C0032-001 |
| API 直接下載 | http://opendata.cwa.gov.tw/fileapi/v1/opendataapi/F-A0010-001?Authorization=你的API_KEY&format=JSON |

> ⚠ 注意：Streamlit Cloud 可能會遇到 SSL 錯誤，因此本專案改使用 `http://` 避免 verify SSL 造成例外。

---

## 📂 檔案結構

project/
│── app.py # Streamlit 主程式
│── data.db # SQLite 資料庫
│── requirement.txt # 套件需求
│── README.md



# 🟧 Part 2 — 電影資料爬蟲（scrape.center）

本專案目標：  
從 [https://ssr1.scrape.center](https://ssr1.scrape.center) 爬取電影資料，共 10 頁，並存成 CSV 檔案 `movie.csv`。

---

## 🔹 功能說明

1. 爬取每頁電影資訊（共 10 頁）：
   - 片名（title）
   - 類型/標籤（tags）
   - 評分（score）
   - 海報網址（cover）
2. 將資料整理成 CSV 格式，方便後續分析或可視化。

---

## 📂 檔案結構

project/
│── movie.py # 電影爬蟲程式
│── movie.csv # 輸出結果


# 📊 movie.csv 欄位說明
欄位	說明
title	電影名稱
tags	電影類型（用逗號分隔，如 動作,劇情）
score	評分，例如 8.5
cover	海報圖片 URL
