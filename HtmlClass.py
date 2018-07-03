# -*- coding: utf-8 -*-
import re
import urlparse
import requests
import time
from bs4 import BeautifulSoup

# 网页下载器
def html_download(url):
    if url is None:
        return None
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = {'User-Agent': user_agent}
    for i in range(10):
        try:
            r = requests.get(url, headers=headers)
            if r.status_code == 200:
                r.encoding = 'utf-8'
                return r.text
            else:
                continue
        except Exception, e:
            time.sleep(1)
    return None

# 解析网址内容
def parser_urls(url, html, regex):
    if url is None or html is None:
        return None
    soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
    new_urls = set()
    links = soup.find_all('a', href=re.compile(regex))
    for link in links:
        new_url = link['href']
        new_full_url = urlparse.urljoin(url, new_url)
        new_urls.add(new_full_url)
    return new_urls

# 解析图片内容
def parser_pci_urls(html, regex):
    if html is None:
        return None
    soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
    new_urls = set()
    links = soup.find_all('img', src=re.compile(regex))
    for link in links:
        new_url = link['src']
        new_urls.add(new_url)
    return new_urls
