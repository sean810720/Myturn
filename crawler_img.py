'''
|--------------------------------------------------------------------------
| 抓 Google 圖片搜尋 - 陽春版
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
import os
import urllib
from urllib.request import urlopen
from urllib.parse import urlparse
import random
import json


def createDir(name):
    dir_name = name + "_" +time.strftime("%Y%m%d%H%M%S")

    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    return dir_name


def getImg(keyword='', dirpath=''):
    keyword = urllib.parse.quote(keyword)
    values = {'searchType' : 'image', 'c2coff': 1, 'safe': 'off', 'hl': 'zh-TW', 'site': 'imghp','tbm': 'isch', 'source': 'hp', 'biw': 1440, 'bih': 803}
    kwEncode = urllib.parse.urlencode(values)
    img_num = 0
    url = 'http://www.google.com/search?'+kwEncode+'&q='+keyword+'&oq='+keyword
    print('\n搜尋URL:\n'+url)
    headers = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36'}
    req = urllib.request.Request(url, headers=headers)
    html = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(html, "html.parser")
    print("\n----- 開始抓圖 ----- \n")

    for item in soup.select(".rg_meta"):
        img_link = item.text
        img_link_json = json.loads(img_link)
        img_num += 1

        try:
            img_link_json['ity'] = img_link_json['ity'] if not img_link_json['ity']=="" else "jpg"
            urllib.request.urlretrieve(str(img_link_json['ou']), dirpath +"/"+str(img_num)+'_'+img_link_json['pt']+"."+img_link_json['ity'])
            print('[ '+str(img_num)+' ] '+img_link_json['ou'])
            pass

        except:
            img_num -= 1
            print("\n----- 圖片存取失敗 -----\n")

    print("\n----- 抓圖完成 -----\n")
    print("抓到圖片張數: "+str(img_num)+"\n")


def main():
    print("\n*** Google 圖片搜尋 ***\n")

    print("請輸入搜尋關鍵字:")
    keyword = input()

    dirpath = createDir('Google 圖片搜尋 - '+keyword)
    getImg(keyword, dirpath)


if __name__ == '__main__':
	main()

