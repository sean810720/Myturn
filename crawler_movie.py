'''
|--------------------------------------------------------------------------
| 開眼電影網 - 本週首輪爬蟲
|--------------------------------------------------------------------------
| 開發者: Sean@2017/02/22
|
| [ Mac OSX 環境安裝/執行 ]
|
| 1. 安裝 Homebrew:
| /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
|
| 2. 安裝Python3 & 必備套件:
| brew install python3
| pip3 install requests
| pip3 install BeautifulSoup4
| pip3 install firebase_admin
|
| 3. 執行:
| python3 /本程式所在路徑/crawler_movie.py
|
| 4. 儲存結果 json 連結:
| https://movieshowapp-3def6.firebaseio.com/MovieData.json
|
'''
import requests
from bs4 import BeautifulSoup
import urllib

# 初始化 Firebase 連接
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
cred = credentials.Certificate(
    "./MovieShowApp/movieshowapp-3def6-firebase-adminsdk-znxfv-9f44615ec7.json")
firebase_admin.initialize_app(
    cred, {'databaseURL': 'https://movieshowapp-3def6.firebaseio.com'})

# Get a database reference.
doc_ref = db.reference('MovieData')

# 抓開眼電影
movie_data = []
res = requests.get("http://www.atmovies.com.tw/movie/now/", verify=False)
res.encoding = 'utf8'
soup = BeautifulSoup(res.text, "html.parser").select(
    ".showtimeQuickSelect form")

print('\n*** 開眼電影網 - 本週首輪 ***\n')

if len(soup) > 0:

    count = 1
    for item in soup[0].select("option"):

        # 檢查首輪 option 是否有 value
        if item.has_attr("value"):

            # 抓電影基本資料
            movie_title = item.text.replace("★", "")
            movie_url = item["value"]
            movie_id = item["value"].split(
                "http://www.atmovies.com.tw/movie/")[1].split("/")[0]

            # 抓電影明細資料
            res2 = requests.get(movie_url)
            res2.encoding = 'utf8'
            soup2 = BeautifulSoup(res2.text, "html.parser").select(
                "#filmTagBlock span")

            # 簡介
            movie_intro = soup2[2].text.strip().lstrip().split()[0]

            # 圖片
            movie_img = soup2[0].find('img')['src']

            # 片長
            runtime = soup2[2].select('.runtime li')[0].text[3:].split("分")[0]

            # 上映日期
            open_date = "無資料" if len(soup2[2].select(
                '.runtime li')) <= 1 else soup2[2].select('.runtime li')[1].text[5:]

            # 從 Yahoo 電影補其他明細

            # 電影類型
            movie_type = ''

            # 電影導演
            movie_director = ''

            # 電影演員
            movie_actor = ''

            # Yahoo 電影搜尋
            movie_keyword = urllib.parse.quote(movie_title)
            res3 = requests.get(
                "https://movies.yahoo.com.tw/moviesearch_result.html?keyword={}".format(movie_keyword))
            res3.encoding = 'utf8'
            soup3 = BeautifulSoup(res3.text, "html.parser")

            # Yahoo 電影簡介頁 URL
            yahoo_intro_url = ''
            for item in soup3.select(".btn_s_introduction"):
                yahoo_intro_url = item['href']

            if len(yahoo_intro_url) > 0:
                res4 = requests.get(yahoo_intro_url)
                res4.encoding = 'utf8'
                soup4 = BeautifulSoup(res4.text, "html.parser")

                # 電影類型
                for item2 in soup4.select(".level_name"):
                    for item2_item in item2:
                        movie_type += item2_item.text.replace(
                            '期待度', '').replace('滿意度', '').replace('\n', '').strip()

                # 導演/演員
                movie_intro_list_tmp = []
                for item3 in soup4.select(".movie_intro_list"):
                    movie_intro_list_tmp.append(item3.text.replace('\n', '').replace(
                        '\r', '').strip().replace(' ', '').replace('導演：', '').replace('演員：', ''))

                # 電影海報
                for item4 in soup4.select(".movie_intro_foto img"):
                    movie_img = item4['src']

            movie_director = movie_intro_list_tmp[0]
            movie_actor = movie_intro_list_tmp[1]

            # 預告片網址
            youtube_url = "" if len(BeautifulSoup(res2.text, "html.parser").select(
                ".video_view iframe")) == 0 else BeautifulSoup(res2.text, "html.parser").select(".video_view iframe")[0]["src"]

            if youtube_url != "":

                # 抓電影明細資料 - iFrame
                res3 = requests.get(
                    "http://app2.atmovies.com.tw/cfrating/film_ratingdata.cfm?filmid="+movie_id)
                res3.encoding = 'utf8'

                # IMDB 評分
                movie_rating = "" if BeautifulSoup(res3.text, "html.parser").find(
                    "font") is None else BeautifulSoup(res3.text, "html.parser").find("font").text

                # 輸出結果
                print('======[', (count), ']=========')
                print("片名: "+movie_title)
                print("網址: "+movie_url)
                print("圖片: "+movie_img)
                print("IMDB: "+movie_rating)
                print("片長: "+runtime)
                print("上映日期: "+open_date)
                print("類別: "+movie_type)
                print("導演: "+movie_director)
                print("演員: "+movie_actor)
                print("預告片網址: "+youtube_url)
                print("簡介: "+movie_intro)
                print("\n")

                movie_data.append({
                    "title": movie_title,
                    "url": movie_url,
                    "img_url": movie_img,
                    "imdb_rating": movie_rating,
                    "runtime": runtime,
                    "open_date": open_date,
                    "movie_type": movie_type,
                    "movie_director": movie_director,
                    "movie_actor": movie_actor,
                    "youtube_url": youtube_url,
                    "movie_intro": movie_intro
                })

                count += 1

# 寫入 database reference.
if len(movie_data) > 0:
    doc_ref.set(movie_data)
print("電影資料更新完成\n\n")
