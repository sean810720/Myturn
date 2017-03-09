'''
|--------------------------------------------------------------------------
| 價格爬蟲
|--------------------------------------------------------------------------
| 開發者: Sean@2017/03/07
|
| [ Mac OSX 環境安裝/執行 ]
|
| 1. 安裝 Homebrew:
| /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
|
| 2. 安裝 Python3 & 必備套件:
| brew install python3
| pip3 install BeautifulSoup4
| pip3 install selenium
|
| 3. 安裝 phantomjs
| brew install phantomjs
|
| 4. 執行:
| python3 /本程式所在路徑/crawler_product.py
|
'''
from bs4 import BeautifulSoup
import urllib
from urllib.request import urlopen
from urllib.parse import urlparse
from selenium import webdriver
import time

# 取得 GoHappy 商品列表
def getGoHappy(keyword=''):
    result = []
    domain = 'http://www.gohappy.com.tw/ec2/'

    try:
        url     = domain+'search?search='+urllib.parse.quote(keyword)
        headers = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36'}
        req     = urllib.request.Request(url, headers=headers)
        html    = urllib.request.urlopen(req).read()
        soup    = BeautifulSoup(html, 'html.parser')

        # 商品基本資料
        for item in soup.select('.prodimg-box'):
            result.append({'url': domain+str(item['href']),
                           'title': str(item['title']),
                           'img': str(item.find('img')['src']),
            })

        # 商品價格
        count = 0
        for item2 in soup.select('.price-table strong'):
            result[count]['price'] = item2.text
            count += 1

    except Exception as e:
        pass

    return result

# 取得 Yahoo 購物中心商品列表
def getYahooShopping(keyword=''):
    result0 = []
    result  = []
    domain  = 'https://tw.search.buy.yahoo.com/search/shopping/product'

    try:
        url     = domain+'?p='+urllib.parse.quote(keyword)
        headers = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36'}
        req     = urllib.request.Request(url, headers=headers)
        html    = urllib.request.urlopen(req).read()
        soup    = BeautifulSoup(html, 'html.parser')

        # 商品基本資料
        for item in soup.select('.srp-pdimage a'):
            result0.append({'url': str(item['href']),
                           'title': str(item['title']),
                           'img': str(item.find('img')['src'])
            })

        # 商品價格
        count = 0
        for item2 in soup.select('.srp-listprice'):
            result0[count]['price'] = item2.text.replace('網路價 $','').replace(',','')
            count += 1

        # 過濾沒價格的商品資料
        for check_item in result0:
            if 'price' in check_item:
                result.append(check_item)

    except Exception as e:
        pass

    return result

# 取得 Yahoo 超級商城商品列表
def getYahooMarket(keyword=''):
    result0 = []
    result  = []
    domain  = 'https://tw.search.mall.yahoo.com/search/mall/product'

    try:
        url     = domain+'?p='+urllib.parse.quote(keyword)
        headers = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36'}
        req     = urllib.request.Request(url, headers=headers)
        html    = urllib.request.urlopen(req).read()
        soup    = BeautifulSoup(html, 'html.parser')

        # 商品基本資料
        for item in soup.select('.srp-pdimage a'):
            result0.append({'url': str(item['href']),
                           'title': str(item['title']),
                           'img': str(item.find('img')['src'])
            })

        # 商品價格
        count = 0
        for item2 in soup.select('.srp-pdprice'):
            result0[count]['price'] = int(item2.text.replace('$','').replace(',','').replace('元','').replace('起','').replace('活動',''))
            count += 1

        # 過濾沒價格的商品資料
        for check_item in result0:
            if 'price' in check_item:
                result.append(check_item)

    except Exception as e:
        pass

    return result

# 取得 Momo 商品列表
def getMomo(keyword=''):
    result  = []
    domain  = 'https://www.momoshop.com.tw'
    driver = webdriver.PhantomJS(executable_path=r'/usr/local/Cellar/phantomjs/2.1.1/bin/phantomjs')
    driver.get(domain+"/search/searchShop.jsp?keyword="+urllib.parse.quote(keyword))
    time.sleep(3)
    listArea = driver.find_element_by_class_name("listArea")
    ul = listArea.find_element_by_tag_name("ul")

    for li in ul.find_elements_by_tag_name("li"):
        goodsUrl = li.find_element_by_class_name("goodsUrl")
        result.append({'url': str(goodsUrl.get_attribute("href")),
                       'title': str(goodsUrl.find_element_by_class_name("prdName").text),
                       'img': str(goodsUrl.find_element_by_class_name("prdImg").get_attribute("src")),
                       'price': int(goodsUrl.find_element_by_class_name("money").text.replace('$','').replace(',','').replace('(售價已折)',''))
        })

    driver.close()
    return result

def main():
    try:
        keyword = input('請輸入搜尋關鍵字:\n')
        print('\n--- 開始抓 GO Happy ---\n')
        print('\n'+str(getGoHappy(keyword))+'\n')
        print('\n--- 開始抓 Yahoo 購物中心 ---\n')
        print('\n'+str(getYahooShopping(keyword))+'\n')
        print('\n--- 開始抓 Yahoo 超級商城 ---\n')
        print('\n'+str(getYahooMarket(keyword))+'\n')
        print('\n--- 開始抓 Momo (會比較久) ---\n')
        print('\n'+str(getMomo(keyword))+'\n')
        print('\n--- 執行結束 ---\n')

    except:
        print('\n--- input/output error ---\n')

if __name__ == '__main__':
    main()
