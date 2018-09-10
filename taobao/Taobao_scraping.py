# usr/bin/env python3
# -*-coding:UTF-8-*-
import pymongo
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from pyquery import PyQuery as pq
import csv
import random
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(chrome_options=chrome_options)
wait = WebDriverWait(browser, 10)
def index_page(page):
    """
    抓取索引页
    :param page: 页码
    """
    print('正在爬取第', page, '页')
    try:
        url = 'https://daphne.tmall.com/search.htm?spm=a1z10.1-b-s.w5001-16530736392.6.e57c3a0MYNRyo&scene=taobao_shop'
        browser.get(url)
        if page > 1:
            # 锁定页面位置
            input = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.pagination>form>input:nth-of-type(4)')))
            print(11111)
            submit = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.pagination form button')))
            print(111)
            input.clear()
            input.send_keys(page)
            submit.click()
        wait.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, 'div.pagination a.page-cur'), str(page)))
        print(11111)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.J_TItems div.item5line1 dl.item')))
        get_products()
    except TimeoutException:
        print('wrong')
        time.sleep(random.randint(3,6))
        index_page(page)


def get_products():
    """
    提取商品数据
    """
    html = browser.page_source
    doc = pq(html)
    items = doc('div.J_TItems div.item5line1 dl.item dd.detail').items()
    out = open('data.csv', 'a', newline='')
    csv_write = csv.writer(out, dialect='excel')
    for item in items:
             title= item.find('a').text(),
             price= item.find('.cprice-area').text().replace('¥ ',''),
             sale=item.find('.sale-area').text().replace('总销量：','')
             product=[title[0],price[0],sale]
             print(product)
             csv_write.writerow(product)
             print('写入成功')
def main():
    """
    遍历每一页
    """
    for i in range(7,18):
        # 伪装为正常浏览
        time_wait=random.randint(10,20)
        time.sleep(time_wait)
        index_page(i)
    browser.close()


if __name__ == '__main__':
    main()