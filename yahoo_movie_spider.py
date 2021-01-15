import requests
import re
from bs4 import BeautifulSoup
import time
import random
import os
import csv
import codecs


def get_iplist(iplist, i):
    url = 'https://www.xicidaili.com/nn/'
    ipurl = url + str(i)
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7',
        'Cache-Control': 'no-cache',
        'accept-encoding': 'gzip, deflate, br',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36',
        'Referer': 'https://www.google.com/'
    }
    r = requests.get(ipurl, headers=headers, timeout=20)
    soup = BeautifulSoup(r.text, 'lxml')
    ips = soup('tr')
    for i in range(1, len(ips)):
        tds = ips[i]('td')
        iplist.append(tds[1].text + ':' + tds[2].text)
    # for ip in iplist:
    #     try:
    #       proxy_host = "http://" + ip
    #       proxy_temp = {"http": proxy_host}
    #       res = urllib.urlopen(url, proxies=proxy_temp).read()
    #     except Exception as e:
    #       iplist.remove(ip)
    #       continue


def get_randomip(iplist):
    proxy_list = []
    for ip in iplist:
        proxy_list.append('http://' + ip)
    proxy_ip = random.choice(proxy_list)
    proxies = {'http': proxy_ip}
    return proxies


def getHTMLText(url, iplist):
    try:
        headers = {
            # 'Accept': 'application/json, text/javascript, */*; q=0.01',
            # 'Accept': '*/*',
            # 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7',
            # 'Cache-Control': 'no-cache',
            # 'accept-encoding': 'gzip, deflate, br',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36',
            'Referer': 'https://www.google.com/'
        }
        # proxy = get_randomip(iplist)
        # print(proxy)
        r = requests.get(url, headers=headers, timeout=50)  # proxies = proxy,
        print(r.status_code)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return '产生异常'


def readReviewUrlList(review_page_url, file):
    with open(file, "r") as f:
        for line in f.readlines():  # 设置文件对象并读取每一行文件
            review_page_url.append(line.strip('\n'))


def extractDataFromHtml(i, rurl, yahoo_datas_path, iplist):
    html = getHTMLText(rurl, iplist)
    movieurl = rurl.split('jp')[1].split('review')[0]
    if len(html) > 10:
        soup = BeautifulSoup(html, 'lxml')
        username = soup('a', attrs={'href': re.compile('/my/profile')})[0].string
        userid = soup('a', attrs={'href': re.compile('/my/profile')})[0].attrs['href'].split('-')[1]
        movieid = soup('div', attrs={'data-cinema-id': re.compile('')})[0].attrs['data-cinema-id']
        moviename = soup('a', attrs={'href': movieurl, 'title': re.compile('')})[0].string
        # movieyear = str(soup('h1',attrs={'class':'text-xlarge'})).split('(')[1].split(')')[0]
        totalrate = soup('ul', attrs={'class': 'list-inline text-xsmall'})[0].i.attrs['class'][1].split('-')[1]
        totalrate = int(totalrate) / 20
        rates = soup('canvas', attrs={'data-chart-val-user': re.compile("")})[0].attrs['data-chart-val-user']
        story = rates.split(',')[0]
        role = rates.split(',')[1]
        show = rates.split(',')[2]
        image = rates.split(',')[3]
        music = rates.split(',')[-1]
        # 故事，角色，演出，影像，音乐
        reviews = \
        str(soup('p', attrs={'class': 'text-small text-break text-readable p1em'})[0]).split('p1em">')[1].split('</p>')[
            0]
        reviews = re.sub('<br/>', '', re.sub('\n', '', reviews))
        with open(yahoo_datas_path, 'a', encoding='utf-8', newline='') as f:
            f.write(codecs.BOM_UTF8.decode())
            csv_writer = csv.writer(f)
            csv_writer.writerow(
                [i, movieid, moviename.strip(), userid, username, totalrate, story, role, show, image, music, reviews])
    else:
        with open(yahoo_datas_path, 'a', encoding='utf-8', newline='') as f:
            f.write(codecs.BOM_UTF8.decode())
            csv_writer = csv.writer(f)
            csv_writer.writerow([i, '', '', '', '', '', '', '', '', '', '', ''])


if __name__ == '__main__':
    start = time.perf_counter()
    review_page_url = []
    url = 'https://movies.yahoo.co.jp'
    review_page_path = r'D:\review_page_url.txt'
    yahoo_datas_path = r'D:\yahooDatas_90000to100000.csv'
    if os.path.exists(yahoo_datas_path):
        os.remove(yahoo_datas_path)
    with open(yahoo_datas_path, 'w+', encoding='utf-8', newline='') as f:
        f.write(codecs.BOM_UTF8.decode())
        csv_writer = csv.writer(f)
        csv_writer.writerow(
            ['id', 'movieid', 'moviename', 'userid', 'username', 'totalrate', 'story', 'role', 'show', 'image', 'music',
             'reviews'])
    readReviewUrlList(review_page_url, review_page_path)
    for i in range(4500, 5000):  #
        s = time.perf_counter()
        iplist = []
        # get_iplist(iplist, i+1)
        for j in range(0, 20):
            k = i * 20 + j
            rurl = review_page_url[k]
            extractDataFromHtml(k + 1, rurl, yahoo_datas_path, iplist)
        e = time.perf_counter() - s
        print("爬取到第{}条信息用了{:5f}s".format((i + 1) * 20, e))
        time.sleep(85)
    dur = time.perf_counter() - start
    print("整个程序的时间为{:5f}s".format(dur))
