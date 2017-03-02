'''
|--------------------------------------------------------------------------
| Google 圖片搜尋爬蟲 - 陽春版
|--------------------------------------------------------------------------
| 開發者: Sean@2017/03/01
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
| python3 /本程式所在路徑/crawler_img.py
|
'''
import requests
from bs4 import BeautifulSoup
import time
from time import sleep
import os
import urllib
from urllib.request import urlopen
from urllib.parse import urlparse
import random
import json


def createDir(name):
    dir_name = name + "_" +time.strftime("%Y%m%d_%H_%M_%S")

    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    return dir_name


def saveFile(file):
    pass


def getImg(keyword='', dirpath='', page=1):
    print("\n搜尋結果:\n")
    img_num = 0
    keyword = urllib.parse.quote(keyword)

    for i in range(page):

        url = "http://www.google.com.sg/search?tbm=isch&source=hp&q="+keyword+"&btnG=Search+Images&biw=1920&bih=1075&start="+str(i-1)+"&ndsp=21"
        headers = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36'}
        req = urllib.request.Request(url, headers=headers)
        html = urllib.request.urlopen(req).read()
        soup = BeautifulSoup(html, "html.parser")

        for item in soup.select(".rg_meta"):
            img_link = item.text
            img_link_json = json.loads(img_link)
            print(img_link_json['ou'])
            img_num += 1

            try:
                img_link_json['ity'] = img_link_json['ity'] if not img_link_json['ity']=="" else "jpg"
                urllib.request.urlretrieve(str(img_link_json['ou']), dirpath +"/"+str(img_num)+"."+img_link_json['ity'])
                pass

            except:
                img_num -= 1
                print("-----save image fail-----")

        sleep(1)

    print("\n抓到圖片張數: "+str(img_num))


def main():
    print("\n*** Google 圖片搜尋 ***\n")

    print("請輸入搜尋關鍵字:")
    keyword = input()

    print("要抓幾頁?")
    page = int(input())

    dirpath = createDir(keyword)
    getImg(keyword, dirpath, page)


if __name__ == '__main__':
	main()

