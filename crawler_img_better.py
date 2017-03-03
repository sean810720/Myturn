'''
|--------------------------------------------------------------------------
| 圖片爬蟲 - 加強版
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
| pip3 install icrawler
|
| 3. 執行:
| python3 /本程式所在路徑/crawler_img_better.py
|
'''
import os
import random
import time
from icrawler.builtin import BaiduImageCrawler, BingImageCrawler, GoogleImageCrawler

def createDir(name):
    dir_name = name + "_" +time.strftime("%Y%m%d%H%M%S")
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    return dir_name

def getImg(keywords='', dirpath='', amount=0, source=4):
    if source == 1:
        print('\n--- 開始從「Google 圖片」下載---\n')
        google_crawler = GoogleImageCrawler(parser_threads=2, downloader_threads=4,storage={'root_dir': dirpath})
        google_crawler.crawl(keyword=keywords, offset=0, max_num=amount, date_min=None, date_max=None, min_size=(200,200), max_size=None)

    elif source == 2:
        print('\n--- 開始從「Microsoft Bing」下載---\n')
        bing_crawler = BingImageCrawler(downloader_threads=4, storage={'root_dir': dirpath})
        bing_crawler.crawl(keyword=keywords, offset=0, max_num=amount, min_size=None, max_size=None)

    elif source == 3:
        print('\n--- 開始從「百度」下載---\n')
        baidu_crawler = BaiduImageCrawler(storage={'root_dir': dirpath})
        baidu_crawler.crawl(keyword=keywords, offset=0, max_num=amount, min_size=None, max_size=None)

    else:
        print('\n--- 開始從「Google 圖片」下載---\n')
        google_crawler = GoogleImageCrawler(parser_threads=2, downloader_threads=4,storage={'root_dir': dirpath})
        google_crawler.crawl(keyword=keywords, offset=0, max_num=amount, date_min=None, date_max=None, min_size=(200,200), max_size=None)
        print('\n--- 開始從「Microsoft Bing」下載---\n')
        bing_crawler = BingImageCrawler(downloader_threads=4, storage={'root_dir': dirpath})
        bing_crawler.crawl(keyword=keywords, offset=0, max_num=amount, min_size=None, max_size=None)
        print('\n--- 開始從「百度」下載---\n')
        baidu_crawler = BaiduImageCrawler(storage={'root_dir': dirpath})
        baidu_crawler.crawl(keyword=keywords, offset=0, max_num=amount, min_size=None, max_size=None)

def main():
    print("\n*** 圖片爬蟲 ***\n")
    keywords = input("輸入要搜尋的關鍵字:\n")
    amount   = int(input("想抓幾張:\n"))
    source   = int(input("選擇抓圖來源 (輸入數字): (1) Google 圖片 (2) Microsoft Bing (3) 百度 (4) 我全都要\n"))
    dirpath  = createDir('圖片搜尋(來源: '+str(source)+') - '+keywords)
    getImg(keywords, dirpath, amount, source)

if __name__ == '__main__':
	main()
