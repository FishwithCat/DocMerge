# coding=utf-8

from DocDownloader import DocDownloader
from DocHandler import DocHandler

if __name__ == '__main__':
    DocHandler.clear_path('./tmp')
    DocHandler.clear_path('./docs')
    downloader = DocDownloader('http://www.csrc.gov.cn/pub/newsite/fxjgb/scgkfxfkyj/', './docs/')
    downloader.download_page([1, 2])
    DocHandler.save_as_docx(r'./docs', r'./tmp')
    DocHandler.merge_file(r'./tmp', r'./merge.docx')
    DocHandler.clear_path('./tmp')
    print 'Done'
