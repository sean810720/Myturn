import requests
from bs4 import BeautifulSoup

# 財政部頁面
res = requests.get("https://www.npcgas.com.tw/home/Oil_today", verify=False)
res.encoding = 'utf8'
soup = BeautifulSoup(res.text, "html.parser")

# 抓出本期發票號碼
award_title = soup.select(
    ".oil-box")[0].text.strip().replace('\n', '').replace(' ', '').replace('油', '油 ')
print(award_title)
