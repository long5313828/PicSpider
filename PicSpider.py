# -*- coding: utf-8 -*-
import HtmlClass
import UrlManager
import os
import sys
import getopt

# 爬虫调度器
class SpiderMan(object):
    def __init__(self, path, reg):
        self.index_url = UrlManager.UrlManager()
        self.path = path
        self.reg = reg

    def run(self, root_url):
        for i in range(1, 316, 1):
            url = root_url + str(i) + ".htm"
            html = HtmlClass.html_download(url).encode('utf-8')
            new_urls = HtmlClass.parser_urls(url, html, self.reg)
            self.index_url.add_new_urls(new_urls)
            while self.index_url.has_new_url():
                try:
                    new_url = self.index_url.get_new_url()
                    if new_url is None:
                        continue
                    html = HtmlClass.html_download(new_url).encode('utf-8')
                    down_urls = HtmlClass.parser_pci_urls(html, r"\w+\.jpg")
                    for du in down_urls:
                        if du is None:
                            continue
                        file_name = os.path.basename(du)
                        if file_name not in os.listdir(self.path):
                            os.system("aria2c.exe --log-level=error --console-log-level=error \
                                      -d " + self.path + " " + du)
                    print "Download total num = %s" % self.index_url.old_url_size()
                except Exception, e:
                    print "Download failed"
                    print e

# 输入参数函数
def inputPara(argv):
    file_dir = "./download/"
    url = "http://www.812dd.com/htm/piclist1/"
    regex = r"/pic\d+/\d+\.htm"
    try:
        opts, args = getopt.getopt(argv, "hd:r:u:", ["dir=", "regex=", "url="])
    except getopt.GetoptError:
        print 'PicSpider.exe -d <outputDir> -u <url> -r <regex>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'PicSpider.exe -d <outputDir> -u <url> -r <regex>'
            sys.exit()
        elif opt in ("-d", "--dir"):
            file_dir = arg
        elif opt in ("-r", "--regex"):
            regex = arg
        elif opt in ("-u", "--url"):
            url = arg
    return file_dir, regex, url

import re
# 主函数
if __name__ == "__main__":
    file_dir, regex, url = inputPara(sys.argv[1:])
    print u'输入的dir为：', file_dir
    print u'输入的url为：', url
    print u'输入的regex为：', regex

    #创建文件夹
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
        print u"文件目录" + file_dir + u"创建成功"

    spider_main = SpiderMan(file_dir, regex)
    spider_main.run(url)



    '''
    path = './download/'
    down_url = "http://download.ydstatic.cn/cidian/static/8.1/20180604/YoudaoDictSetup.exe"
    print "aria2c.exe -d " + path + " " + down_url
    os.system("aria2c.exe -d " + path + " " + down_url)
    
    patton = re.compile(regex)
    res = re.search(patton, url)
    print res.group()
    os.system("aria2c.exe -d " + file_dir + " " + url)
    
    pic = Downloader.FileDownloader()
    pic.download(
        "http://download.ydstatic.cn/cidian/static/8.1/20180604/YoudaoDictSetup.exe",
        "test.exe")
    '''
