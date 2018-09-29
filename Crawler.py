# This program was created by Hangyu Lee, KPST
# This program uses multiple processes to speed up crawling
# Send an email for any issues
# Author shunchips@kpst.co.kr


import sys
from urllib.request import urlopen

import os
from builtins import print

from bs4 import BeautifulSoup
import urllib
from multiprocessing import Process, Pool
import time
import multiprocessing

def get_html_addr(page_number):
    html_page = urllib.request.urlopen("http://wallpaperswide.com/girls-desktop-wallpapers/page/" + str(page_number))
    soup = BeautifulSoup(html_page, 'html.parser')
    answer = list(soup.findAll("li", {'class' : 'wall'}))
    output = []
    for value in answer:
        into_soup = value.find("a")
        _url = into_soup["href"]
        # url =
        output.append("http://wallpaperswide.com" + _url)
        # output.append(url_list)
    return output


def download_image(request_url_addr):
    title_ = "Standard 4:3 800 x 600 wallpaper"
    html_page = urllib.request.urlopen(request_url_addr)
    soup = BeautifulSoup(html_page, 'html.parser')
    download_url = list(soup.findAll(title=title_))



    for value in download_url:
        url = value["href"]
        print("Processing .... " + url )
        _url = "http://wallpaperswide.com" + url
        a = url.split('/')
        mypath = sys.argv[1]
        download_path = os.path.join(mypath, a[2])
        # print(a[2])
        urllib.request.urlretrieve(_url, download_path)


Page_Number =1
url_list = []
# while(Page_Number <10):
#     html_page_ = urllib.request.urlopen("http://wallpaperswide.com/girls-desktop-wallpapers/page/" + str(Page_Number))
#     # url_list = get_html_addr(html_page_)
#     print("Page Number ... :" + str(Page_Number))
#     for i in url_list:
#         print("Downloading ..." + i)
#         print(i)
#         download_image(i, "Standard 4:3 800 x 600 wallpaper")
#     Page_Number += 1
#
def main():
    start_time = time.time()
    if len(sys.argv) == 0:
        print("--------Usage argument 1 = download path(absolute) argument 2 = number of process to use, default cpu x 3")
    # html_page_ = urllib.request.urlopen("http://wallpaperswide.com/girls-desktop-wallpapers/page/" + str(Page_Number))
    procs = []
    url_list = []
    cpus = multiprocessing.cpu_count()
    print('Number of cpu\'s to process WM: %d' % cpus)
    poolcount = 0
    if len(sys.argv) == 2:
        poolcount = cpus * 3
    if len(sys.argv) == 3:
        poolcount = int(sys.argv[2])
    print('using %d processes for this task' % poolcount)
    html_p = Pool(poolcount)
    data = html_p.map(get_html_addr, [i for i in range(1,2)])

    for r in data:
        print(r)
    html_p.close()
    html_p.join()



    download_p = Pool(poolcount)
    for urls in data:
        download_url = download_p.map(download_image, urls)
    download_p.close()
    download_p.join()

    # Tried with Process
    # procs = []
    # proc = Process(target=download_image, args=(data[0], title))
    # procs.append(proc)
    # proc.start()
    # for url in data:
    #     # download_image(url,title)
    #     proc = Process(target=download_image, args=(url, title))
    #     procs.append(proc)
    #     proc.start()
    #     print(url)
    # for proc in procs:
    #     proc.join()
    print("How long ?  " + str(time.time() - start_time) + " seconds ")

if __name__=="__main__":
    main()