'''
|--------------------------------------------------------------------------
| 抓開眼電影網 - 本週首輪
|--------------------------------------------------------------------------
| 開發者: Sean@2017/02/22
|
| - Mac OSX 環境:
|
| 0. 安裝 Homebrew
| /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
| 
| 1. brew install python3
| 2. pip3 install requests
| 3. pip3 install bs4
| 4. 執行: python3 /本程式所在路徑/crawler_movie.py
|
'''
import requests
from bs4 import BeautifulSoup

# 抓開眼電影頁面
res = requests.get("http://www.atmovies.com.tw/movie/now/")
res.encoding = 'utf8'
soup = BeautifulSoup(res.text, "html.parser")

print ('*** 開眼電影網 - 本週首輪 ***\n\n')

count = 1

for item in soup.select(".filmListAll2 li"):

    # 抓電影基本資料
    movie_title = item.find('a').text
    movie_url = "http://www.atmovies.com.tw"+item.find('a')['href']
    movie_rating = item.find("font").text

    # 抓電影簡介
    res2 = requests.get(movie_url)
    res2.encoding = 'utf8'
    soup2 = BeautifulSoup(res2.text, "html.parser")
    intro = soup2.select("#filmTagBlock span")[2]
    movie_intro = intro.text.strip().lstrip()

    # 輸出結果
    print ('======[',(count),']=========')
    print ("片名: "+movie_title)
    print ("網址: "+movie_url)
    print ("IMDB: "+movie_rating)
    print ("簡介: \n"+movie_intro)
    print ("\n\n")
    count += 1
