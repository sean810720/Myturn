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
| 2. 安裝Python3 & 必備套件:
| brew install python3
| pip3 install BeautifulSoup4
|
| 3. 執行:
| python3 /本程式所在路徑/crawler_product.py
|
'''
from bs4 import BeautifulSoup
import urllib
from urllib.request import urlopen
from urllib.parse import urlparse

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

def main():
    try:
        keyword = input('請輸入搜尋關鍵字:\n')
        print('\n'+str(getGoHappy(keyword))+'\n')
        print('\n'+str(getYahooShopping(keyword))+'\n')
        print('\n'+str(getYahooMarket(keyword))+'\n')

    except:
        print('\n--- input/output error ---\n')

if __name__ == '__main__':
    main()

