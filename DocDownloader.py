# coding=utf-8
from multiprocessing import Pool
import os
import re
import time
import urllib

from bs4 import BeautifulSoup


def download(link, targetPath):
    urllib.urlretrieve(link, targetPath)


def get_file_link(detailPageUrl):
    html = urllib.urlopen(detailPageUrl)
    parseResult = BeautifulSoup(html, 'lxml')
    for scriptContent in parseResult.find_all('script'):
        searchResult = re.search(r'file_appendix=\'<a href=\"(.*)\"\>', scriptContent.text)
        if searchResult:
            return generate_url(detailPageUrl, searchResult.group(1))
            break
    return None


def generate_url(detailPageUrl, fileRelatePath):
    tmp = detailPageUrl.split('/')
    tmp[-1] = fileRelatePath.replace('./', '')
    return '/'.join(tmp)


def download_file_from_detailPage(detailPageUrl, targetPath):
    fileLink = get_file_link(detailPageUrl)
    if fileLink is None:
        print "error"
    else:
        download(fileLink, targetPath)


class DocDownloader(object):

    def __init__(self, url, localPath):
        self.baseUrl = url
        self.localPath = os.path.abspath(localPath)
        if not os.path.exists(self.localPath):
            os.mkdir(self.localPath)
        self.taskPool = Pool()

    def download_page(self, pageRange=[]):
        print 'start download..'
        if len(pageRange) == 0:
            print 'download all files'
            index = 0
            while(True):
                pageUrl = self.generate_page_url(index)
                if not self.download_files_in_page(pageUrl):
                    break
                index += 1
        else:
            for pageIndex in pageRange:
                pageUrl = self.generate_page_url(pageIndex - 1)
                self.download_files_in_page(pageUrl)
        self.taskPool.close()
        self.taskPool.join()
        print 'download finished..'

    def download_files_in_page(self, pageUrl):
        html = urllib.urlopen(pageUrl)
        parseResult = BeautifulSoup(html, 'lxml')
        if parseResult.find(id='myul') is None:
            return False
        for link in parseResult.find(id='myul').find_all('a'):
            print 'downloading >>> ', link['title']
            detailPageLink = self.baseUrl + link['href'].replace('./', '')
            self.taskPool.apply_async(download_file_from_detailPage, (detailPageLink,
                                                                      os.path.join(self.localPath, link['title']) + '.doc', ))
        return True

    def generate_page_url(self, pageIndex):
        if pageIndex <= 0:
            return self.baseUrl + 'index.html'
        else:
            return self.baseUrl + 'index_{}.html'.format(pageIndex)

if __name__ == '__main__':
    startTime = time.time()
    downloader = DocDownloader('http://www.csrc.gov.cn/pub/newsite/fxjgb/scgkfxfkyj/', './docs/')
    downloader.download_page([1, 2])
    endTime = time.time()
    print endTime - startTime
