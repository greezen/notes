"""
批量下载微博网盘音乐到本地
author: greezen
date: 2018-10-09
"""
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time
import os


def main():
    url = "http://vdisk.weibo.com/s/urec2mX_Nh83h"

    for sub in get_list(url):
        for item in get_list(sub['href']):
            song_download(item["href"], sub["title"])
            print(item["href"], sub["title"])


def song_download(url, dir_name):
    path = "E:\\mp3\\" + dir_name
    if not os.path.exists(path):
        os.mkdir(path)

    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2, "download.default_directory": path}
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_path = "D:\\anaconda3\Scripts\chromedriver.exe"
    browser = webdriver.Chrome(chrome_path, chrome_options=chrome_options)
    browser.minimize_window()
    browser.set_page_load_timeout(20)
    browser.get(url)
    browser.find_element_by_id("download_big_btn").click()
    time.sleep(3)
    browser.close()


def get_list(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    a_list = soup.find_all('a', {"class": "short_name"})

    return a_list


if __name__ == '__main__':
    main()
