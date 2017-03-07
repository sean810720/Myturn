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
def getYahoo(keyword=''):
    result = []
    domain = 'https://tw.search.buy.yahoo.com/search/shopping/product'

    try:
        url     = domain+'?p='+urllib.parse.quote(keyword)
        headers = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36'}
        req     = urllib.request.Request(url, headers=headers)
        html    = urllib.request.urlopen(req).read()
        soup    = BeautifulSoup(html, 'html.parser')
        
        # 商品基本資料
        for item in soup.select('.srp-pdimage a'):
            result.append({'url': str(item['href']),
                           'title': str(item['title']),
                           'img': str(item.find('img')['src']),
            })

        # 商品價格
        count = 0
        for item2 in soup.select('.srp-listprice'):
            result[count]['price'] = item2.text
            count += 1

    except Exception as e:
        pass

    return result

def main():
    try:
        keyword = input('請輸入搜尋關鍵字:\n')
        print('\n'+str(getGoHappy(keyword))+'\n')
        print('\n'+str(getYahoo(keyword))+'\n')

    except:
        print('\n--- input/output error ---\n')

if __name__ == '__main__':
    main()

