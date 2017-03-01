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
from time import sleep

def GetImg(keyword='', page=1):
    print("\n搜尋結果:\n")
    img_num = 0

    for i in range(page):
        url = "http://www.google.com.sg/search?tbm=isch&source=hp&q="+keyword+"&btnG=Search+Images&biw=1920&bih=1075&start="+str(i-1)+"&ndsp=21"
        res = requests.get(url)
        res.encoding = 'utf8'
        soup = BeautifulSoup(res.text, "html.parser")

        for item in soup.select('img'):
            img_link = item.get('src')
            print("[ "+str(img_num+1)+" ] "+img_link)
            img_num += 1

        sleep(1)

    print("\n抓到圖片張數: "+str(img_num))

def main():
	print("\n*** Google 圖片搜尋 ***\n")

	print("請輸入搜尋關鍵字:")
	keyword = input()

	print("要抓幾頁?")
	page = int(input())
	GetImg(keyword, page)

if __name__ == '__main__':
	main()
