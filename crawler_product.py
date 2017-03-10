'''
|--------------------------------------------------------------------------
| 比價爬蟲
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
import re
import operator

class CrawlerProduct:

    # 初始化
    def __init__(self,keyword=''):
        self.result = []
        self.keyword = urllib.parse.quote(keyword)


    # 開始執行並按價格排序
    def exec(self):
        self.getGoHappy()
        self.getYahooShopping()
        self.getYahooMarket()
        #self.getMomo()
        self.getPchome()
        self.getBooks()
        print('\n--- 執行結束 ---\n')
        return sorted(self.result, key=operator.itemgetter('price'))


    # 取得 GoHappy 商品列表
    def getGoHappy(self):
        print('\n--- 開始抓 GO Happy ---')
        result0 = []
        domain  = 'http://www.gohappy.com.tw/ec2/'

        try:
            url     = domain+'search?search='+self.keyword
            headers = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36'}
            req     = urllib.request.Request(url, headers=headers)
            html    = urllib.request.urlopen(req).read()
            soup    = BeautifulSoup(html, 'html.parser')

            # 商品基本資料
            for item in soup.select('.prodimg-box'):
                self.result.append({'url': domain+str(item['href']),
                                    'title': str(item['title']),
                                    'img': str(item.find('img')['src']),
                                    'source': 'GO Happy'
                })

            # 商品價格
            count = 0
            for item2 in soup.select('.price-table'):
                self.result[count]['price'] = int(item2.find('strong').text.replace(',',''))
                count += 1

            print('Done.')

        except Exception as e:
            print('[ 查無商品 ]')
            pass


    # 取得 Yahoo 購物中心商品列表
    def getYahooShopping(self):
        print('\n--- 開始抓 Yahoo 購物中心 ---')
        result0 = []
        domain  = 'https://tw.search.buy.yahoo.com/search/shopping/product'

        try:
            url     = domain+'?p='+self.keyword
            headers = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36'}
            req     = urllib.request.Request(url, headers=headers)
            html    = urllib.request.urlopen(req).read()
            soup    = BeautifulSoup(html, 'html.parser')

            # 商品基本資料
            for item in soup.select('.srp-pdimage a'):
                result0.append({'url': str(item['href']),
                               'title': str(item['title']),
                               'img': str(item.find('img')['src']),
                               'source': 'Yahoo 購物中心'
                })

            # 商品價格
            count = 0
            for item2 in soup.select('.srp-listprice'):
                result0[count]['price'] = int(item2.text.replace('網路價 $','').replace(',',''))
                count += 1

            # 過濾沒價格的商品資料
            for check_item in result0:
                if 'price' in check_item:
                    self.result.append(check_item)

            print('Done.')

        except Exception as e:
            print('[ 查無商品 ]')
            pass


    # 取得 Yahoo 超級商城商品列表
    def getYahooMarket(self):
        print('\n--- 開始抓 Yahoo 超級商城 ---')
        result0 = []
        domain  = 'https://tw.search.mall.yahoo.com/search/mall/product'

        try:
            url     = domain+'?p='+self.keyword
            headers = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36'}
            req     = urllib.request.Request(url, headers=headers)
            html    = urllib.request.urlopen(req).read()
            soup    = BeautifulSoup(html, 'html.parser')

            # 商品基本資料
            for item in soup.select('.srp-pdimage a'):
                result0.append({'url': str(item['href']),
                                'title': str(item['title']),
                                'img': str(item.find('img')['src']),
                                'source': 'Yahoo 超級商城'
                })

            # 商品價格
            count = 0
            for item2 in soup.select('.srp-pdprice'):
                result0[count]['price'] = int(item2.text.replace('$','').replace(',','').replace('元','').replace('起','').replace('活動',''))
                count += 1

            # 過濾沒價格的商品資料
            for check_item in result0:
                if 'price' in check_item:
                    self.result.append(check_item)

            print('Done.')

        except Exception as e:
            print('[ 查無商品 ]')
            pass



    # 取得 Momo 商品列表
    def getMomo(self):
        print('\n--- 開始抓 Momo (會比較久) ---')
        domain  = 'https://www.momoshop.com.tw'
        driver  = webdriver.PhantomJS(executable_path=r'/usr/local/Cellar/phantomjs/2.1.1/bin/phantomjs')
        driver.get(domain+"/search/searchShop.jsp?keyword="+self.keyword)
        time.sleep(1)
        listArea = driver.find_element_by_class_name("listArea")
        ul       = listArea.find_element_by_tag_name("ul")

        for li in ul.find_elements_by_tag_name("li"):
            goodsUrl = li.find_element_by_class_name("goodsUrl")
            self.result.append({'url': str(goodsUrl.get_attribute("href")),
                                'title': str(goodsUrl.find_element_by_class_name("prdName").text),
                                'img': str(goodsUrl.find_element_by_class_name("prdImg").get_attribute("src")),
                                'price': int(goodsUrl.find_element_by_class_name("money").text.replace('$','').replace(',','').replace('(售價已折)','')),
                                'source': 'Momo 購物'
            })

        driver.close()
        print('Done.')


    # 取得 Pchome 線上購物商品列表
    def getPchome(self):
        print('\n--- 開始抓 Pchome 線上購物 (會比較久) ---')
        domain  = 'http://ecshweb.pchome.com.tw'
        driver  = webdriver.PhantomJS(executable_path=r'/usr/local/Cellar/phantomjs/2.1.1/bin/phantomjs')
        driver.get(domain+"/search/v3.3/?q="+urllib.parse.quote(keyword))
        time.sleep(1)
        ItemContainer = driver.find_element_by_id("ItemContainer")

        for dl in ItemContainer.find_elements_by_tag_name("dl"):
            dd = dl.find_elements_by_tag_name("dd")

            try:
                prod_img = dd[0].find_element_by_class_name("prod_img")
                img      = prod_img.find_element_by_tag_name("img").get_attribute("src")

            except:
                prod_img = dd[0].find_element_by_class_name("prod_noimg")
                img      = 'http://a.ecimg.tw/css/2016/style/images/v201607/product/beta/ticrf.png'

            self.result.append({'url': str(dd[1].find_element_by_class_name("prod_name").find_element_by_tag_name("a").get_attribute("href")),
                                'title': str(dd[1].find_element_by_class_name("prod_name").text),
                                'img': str(img),
                                'source': 'PChome 線上購物',
                                'price': int(dd[2].find_element_by_class_name("price_box").text.replace('$','').replace('網路價',''))
            })

        driver.close()
        print('Done.')


    # 取得博客來商品列表
    def getBooks(self):
        print('\n--- 開始抓博客來 (會比較久) ---')
        domain  = 'http://search.books.com.tw'
        driver  = webdriver.PhantomJS(executable_path=r'/usr/local/Cellar/phantomjs/2.1.1/bin/phantomjs')
        driver.get(domain+"/search/query?key="+self.keyword)
        time.sleep(1)
        searchbook = driver.find_element_by_class_name("searchbook")

        for item in searchbook.find_elements_by_class_name("item"):
            a      = item.find_element_by_tag_name("a")
            price0 = re.match(r'(.*)元',item.find_element_by_class_name("price").text,re.M|re.I)
            price  = re.sub(r'^.*折，',"",price0.group(1))
            self.result.append({'url': str(a.get_attribute("href")),
                                'title': str(a.get_attribute("title")),
                                'img': str(a.find_element_by_tag_name("img").get_attribute("src")),
                                'source': '博客來',
                                'price': int(price.replace('優惠價：','').replace(',',''))
            })

        driver.close()
        print('Done.')


# 執行範例code
try:
    keyword = input('請輸入搜尋關鍵字:\n')
    crawler_product = CrawlerProduct(keyword).exec()
    print(str(crawler_product)+"\n")

except Exception as e:
    print('\n--- input/output error: '+str(e)+' ---\n')
