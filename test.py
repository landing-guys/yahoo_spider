import pandas as pd
import requests
import random
from bs4 import BeautifulSoup

# ip_path = './userful_ip.txt'
# ips = pd.read_csv(ip_path, names=['ip'])
# ip_list = [ip[0] for ip in ips.values]


def get_headers():
    user_agent_list = [ \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1" \
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6", \
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1", \
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5", \
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3", \
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24", \
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]
    UserAgent = random.choice(user_agent_list)
    headers = {'User-Agent': UserAgent}
    return headers


def get_randomips(ip_list):
    ip = random.choice(ip_list)
    proxies = {"http": "http://" + ip, "https": "https://" + ip}
    return proxies


def get_htmltext(url, proxies):
    try:
        r = requests.get(url, headers=get_headers(), proxies=get_randomip(), timeout=30)
        print(r.status_code)
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "产生异常"


# url_1 = pd.read_csv('./yahoo_url_1.csv', names=['url'])
# for i in range(len(url_1)):
#     init_url = url_1.iloc[i].values[0]
#     for j in range(200):
#         url = init_url + str(j + 1)

def get_randomip():
    url = 'https://www.kuaidaili.com/free/inha/'
    ran_page = random.randint(1, 3829)
    ip_url = url + str(ran_page)
    ip_list = []
    r = requests.get(ip_url, headers=get_headers())
    soup = BeautifulSoup(r.text, 'lxml')
    ips = soup('tr')
    for j in range(1, len(ips)):
        tds = ips[j]('td')
        ip_list.append(tds[0].text + ":" + tds[1].text)
    ip = random.choice(ip_list)
    print(ip)
    proxies = {"http": "http://" + ip, "https": "http://" + ip}
    return proxies

ip_file_path = './userful_ip.txt'
temp = pd.read_csv(ip_file_path, names=[''])
ip_list = [temp.values[i][0] for i in range(len(temp))]
test_url = 'https://movies.yahoo.co.jp/movie/330415/review/?sort=lrf&page=1'
r = requests.get(test_url, headers=get_headers(), proxies=get_randomip())
# 获取电影总评论数，以及要爬取的页数
soup = BeautifulSoup(r.text, 'lxml')
temp = soup('div', attrs={'class': 'list-controller align-center'})
n_reviews = int(temp[0].text.split('/')[-1].split('件')[0])
n_pages = n_reviews // 10