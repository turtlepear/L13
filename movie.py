import requests
from bs4 import BeautifulSoup
import csv

BASE_URL = "https://ssr1.scrape.center/page/{}"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

movies = []

for page in range(1, 11):
    print(f"正在爬第 {page} 頁...")
    url = BASE_URL.format(page)
    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")

    items = soup.select(".el-card.item.m-t.is-hover-shadow")

    for item in items:
        # 片名
        name_tag = item.select_one(".name")
        title = name_tag.get_text(strip=True) if name_tag else "N/A"

        # 類型
        tag_items = item.select(".categories button span")
        tags = ",".join(t.get_text(strip=True) for t in tag_items) if tag_items else ""

        # 分數
        score_tag = item.select_one(".score")
        score = score_tag.get_text(strip=True) if score_tag else "N/A"

        # 海報
        img_tag = item.select_one(".cover img")
        cover = img_tag["src"] if img_tag else ""

        movies.append({
            "title": title,
            "tags": tags,
            "score": score,
            "cover": cover
        })

# 輸出 CSV
with open("movie.csv", "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["title", "tags", "score", "cover"])
    writer.writeheader()
    writer.writerows(movies)

print("movie.csv 已建立成功！")
