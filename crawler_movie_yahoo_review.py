'''
|--------------------------------------------------------------------------
| Yahoo電影 - 網友影評爬蟲
|--------------------------------------------------------------------------
| 開發者: Sean@2020/08/31
|
| [ Mac OSX 環境安裝/執行 ]
|
| 1. 安裝 Homebrew:
| /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
|
| 2. 安裝Python3 & 必備套件:
| brew install python3
| pip3 install requests
| pip3 install json
| pip3 install urllib
| pip3 install BeautifulSoup4
| pip3 install firebase_admin
|
| 3. 執行:
| python3 /本程式所在路徑/crawler_movie_yahoo_review.py
|
| 4. 電影基本資料來源 json:
| https://movieshowapp-3def6.firebaseio.com/MovieData.json
|
'''
import requests
from bs4 import BeautifulSoup
import urllib
import json

# 初始化 Firebase 連接
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
cred = credentials.Certificate(
    "./MovieShowApp/movieshowapp-3def6-firebase-adminsdk-znxfv-9f44615ec7.json")
firebase_admin.initialize_app(
    cred, {'databaseURL': 'https://movieshowapp-3def6.firebaseio.com'})

# Get a database reference.
doc_ref = db.reference('MovieReview_Yahoo')

# 影評資料
review_data = []

try:

    # 電影基本資料
    res = requests.get(
        'https://movieshowapp-3def6.firebaseio.com/MovieData.json')
    res.encoding = 'utf8'
    movies = json.loads(res.text)

    for movie in movies:

        # 要抓的頁數
        page_count = 11

        # Yahoo 電影 - 資料搜尋
        movie_id = ''
        movie_title = ''
        movie_keyword = urllib.parse.quote(movie['title'])
        res = requests.get(
            "https://movies.yahoo.com.tw/moviesearch_result.html?keyword={}".format(movie_keyword), verify=False)
        res.encoding = 'utf8'
        soup = BeautifulSoup(res.text, "html.parser")

        for item in soup.select(".release_movie_name"):
            movie_id = item.find_all('a')[0]['href'][-5:].replace('-', '')

            movie_title = ''
            if len(item.select('.highlight')) > 0:
                movie_title = item.select('.highlight')[0].text

        # Yahoo 電影 - 網友短評
        if len(movie_id) > 0 and len(movie_title) > 0:
            print(
                '\n*** [Yahoo電影] 網友短評 - {}({}) ***\n'.format(movie_title, movie_id))
            review_sub_data = []

            # count = 1
            for i in range(page_count):
                if i == 0:
                    pass

                else:
                    res = requests.get(
                        "https://movies.yahoo.com.tw/movieinfo_review.html/id={}?sort=update_ts&order=desc&page={}".format(movie_id, i))
                    res.encoding = 'utf8'
                    soup = BeautifulSoup(res.text, "html.parser")

                    for item in soup.select(".usercom_list li"):

                        # 發表內容
                        review_content = ''
                        review_content = str(item.find_all('span')[2].text)

                        # 發表者
                        reviewer = ''
                        reviewer = str(item.select('.user_id')[
                                       0].text).replace('發表人：', '')

                        # 發表時間
                        review_time = ''
                        review_time = str(item.select('.user_time')[
                                          0].text).replace('發表時間：', '')

                        # 五星評分
                        review_score = 0
                        review_score = item.find_all('input')[1]['value']

                        # 網友讚數
                        review_good_num = 0
                        review_good_num = item.find_all('input')[2]['value']

                        # 網友噓數
                        review_bad_num = 0
                        review_bad_num = item.find_all('input')[3]['value']

                        # 輸出結果
                        # print('======[',(count),']=========')
                        # print("發表內容: "+review_content)
                        # print("發表者: "+reviewer)
                        # print("發表時間: "+review_time)
                        # print("五星評分: ",review_score)
                        # print("網友讚數: ",review_good_num)
                        # print("網友噓數: ",review_bad_num)
                        # print("\n")
                        # count += 1

                        review_sub_data.append({
                            "review_content": review_content,
                            "reviewer": reviewer,
                            "review_time": review_time,
                            "review_score": review_score,
                            "review_good_num": review_good_num,
                            "review_bad_num": review_bad_num
                        })

            if len(review_sub_data) > 0:
                review_data.append({movie_title: review_sub_data})

                # 寫入 database reference.
                doc_ref.set(review_data)

    print("Yahoo影評資料更新完成\n")

except Exception as e:
    #print('錯誤訊息:', e)
    print("Yahoo影評資料更新完成\n")
    pass
