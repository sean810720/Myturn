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
|
| 3. 執行:
| python3 /本程式所在路徑/crawler_movie.py
|
'''
import requests
from bs4 import BeautifulSoup

# 抓開眼電影
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

    # 抓電影明細資料 - iFrame
    res3 = requests.get("http://app2.atmovies.com.tw/cfrating/film_ratingdata.cfm?filmid="+movie_id)
    res3.encoding = 'utf8'

    # IMDB 評分
    movie_rating = "無評分" if BeautifulSoup(res3.text, "html.parser").find("font") is None else BeautifulSoup(res3.text, "html.parser").find("font").text

    # 輸出結果
    print('======[',(count),']=========')
    print("ID: "+movie_id)
    print("片名: "+movie_title)
    print("網址: "+movie_url)
    print("圖片: "+movie_img)
    print("IMDB: "+movie_rating)
    print("簡介: \n"+movie_intro)
    print("\n\n")
    count += 1
