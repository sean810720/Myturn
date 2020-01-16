'''
|--------------------------------------------------------------------------
| 抓開眼電影網本週首輪爬蟲 - 陽春版
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
'''
import requests
from bs4 import BeautifulSoup

# 初始化 Firebase 連接
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
cred = credentials.Certificate("./MovieShowApp/movieshowapp-3def6-firebase-adminsdk-znxfv-9f44615ec7.json")
firebase_admin.initialize_app(cred, {'databaseURL': 'https://movieshowapp-3def6.firebaseio.com'})

# Get a database reference.
doc_ref = db.reference('MovieData')

# 抓開眼電影
movie_data =[]
res = requests.get("http://www.atmovies.com.tw/movie/now/")
res.encoding = 'utf8'
soup = BeautifulSoup(res.text, "html.parser")

print('\n*** 開眼電影網 - 本週首輪 ***\n')

count = 1

for item in soup.select(".filmListPA li"):

    # 抓電影基本資料
    movie_title = item.find('a').text
    movie_url = "http://www.atmovies.com.tw"+item.find('a')['href']
    movie_id = item.find('a')['href'][7:19]

    # 抓電影明細資料
    res2 = requests.get(movie_url)
    res2.encoding = 'utf8'
    soup2 = BeautifulSoup(res2.text, "html.parser").select("#filmTagBlock span")

    # 簡介
    movie_intro = soup2[2].text.strip().lstrip().split()[0]

    # 圖片
    movie_img = soup2[0].find('img')['src']

    # 片長
    runtime = soup2[2].select('.runtime li')[0].text[3:].split("分")[0]

    # 上映日期
    playtime = soup2[2].select('.runtime li')[1].text[5:]

    # 預告片網址
    youtube_url = BeautifulSoup(res2.text, "html.parser").select(".video_view iframe")[0]["src"]

    # 抓電影明細資料 - iFrame
    res3 = requests.get("http://app2.atmovies.com.tw/cfrating/film_ratingdata.cfm?filmid="+movie_id)
    res3.encoding = 'utf8'

    # IMDB 評分
    movie_rating = "" if BeautifulSoup(res3.text, "html.parser").find("font") is None else BeautifulSoup(res3.text, "html.parser").find("font").text

    # 輸出結果
    print('======[',(count),']=========')
    print("片名: "+movie_title)
    print("網址: "+movie_url)
    print("圖片: "+movie_img)
    print("IMDB: "+movie_rating)
    print("片長: "+runtime)
    print("上映日期: "+playtime)
    print("預告片網址: "+youtube_url)
    print("簡介: "+movie_intro)
    print("\n")

    movie_data.append({
        "title":movie_title,
        "url":movie_url,
        "img_url":movie_img,
        "imdb_rating":movie_rating,
        "runtime":runtime,
        "playtime":playtime,
        "youtube_url":youtube_url,
        "movie_intro":movie_intro
    })

    count += 1

# 寫入 database reference.
doc_ref.set(movie_data)

print("電影資料更新完成\n\n")
