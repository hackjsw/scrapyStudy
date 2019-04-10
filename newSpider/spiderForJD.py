# coding=utf-8

import time

from pyquery import PyQuery as pq
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# 打开不同的浏览器实例


def openBrower(brower_type):
    if brower_type == 'chrome':
        chrome_options = Options()
        chrome_options.headless = True
        return webdriver.Chrome(options=chrome_options)
    elif brower_type == 'firefox':
        return webdriver.Firefox()
    elif brower_type == 'safari':
        return webdriver.Safari()
    elif brower_type == 'PhantomJS':
        return webdriver.PhantomJS()
    else:
        return webdriver.Ie()


def parse_website():
    # 通过Chrome()方法打开chrome浏览器
    browser = openBrower('chrome')
    # 访问京东网站
    browser.get("https://www.jd.com")
    # 等待50秒
    wait = WebDriverWait(browser, 10)
    # 通过css选择器的id属性获得输入框。until方法表示浏览器完全加载到对应的节点，才返回相应的对象。presence_of_all_elements_located是通过css选择器加载节点
    input = wait.until(
        EC.presence_of_all_elements_located((By.XPATH, "//input[@id='key']"))
    )

    # input = browser.find_element_by_id('key')
    # 在输入框中写入要查询的信息
    input[0].send_keys('计算机书籍')
    # 查询按钮完全加载完毕，返回查询按钮对象
    submit_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.button'))
    )
    # 点击查询按钮
    submit_button.click()

    # 模拟下滑到底部操作
    for i in range(0, 3):
        browser.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

    # 商品列表的总页数
    total = wait.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, '#J_bottomPage > span.p-skip > em:nth-child(1) > b')
        )
    )
    html = browser.page_source.replace('xmlns', 'another_attr')
    parse_book(1, html)

    for page_num in range(2, int(total[0].text) + 1):
        parse_next_page(page_num, browser, wait)

# 解析下一页


def parse_next_page(page_num, browser, wait):
    next_page_button = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#J_bottomPage>span.p-num>a.pn-next > em'))
    )
    next_page_button.click()

    # 滑动到页面底部，用于加载数据
    for i in range(0, 3):
        browser.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(10)

    # 一页显示60个商品，"#J_goodsList > ul > li:nth-child(60)确保60个商品都正常加载出来。
    wait.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "#J_goodsList > ul > li:nth-child(60)"))
    )
    # 判断翻页成功，当底部的分页界面上显示第几页时，就显示翻页成功。
    wait.until(
        EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR, "#J_bottomPage > span.p-num > a.curr"), str(page_num))
    )

    html = browser.page_source.replace('xmlns', 'another_attr')
    parse_book(page_num, html)


def parse_book(page, html):
    doc = pq(html)
    li_list = doc('.gl-item').items()
    print('-------------------第' + str(page) + '页的图书信息---------------------')
    for item in li_list:
        # image_html = item('.gl-i-wrap .p-img')
        book_img_url = item.find('img').attr('data-lazy-img')
        if book_img_url == "done":
            book_img_url = item.find('img').attr('src')
        print('图片地址:' + book_img_url)
        item('.p-name').find('font').remove()
        book_name = item('.p-name').find('em').text()
        print('书名：' + book_name)
        price = item('.p-price').find('em').text() + \
            str(item('.p-price').find('i').text())
        print('价格：' + price)
        # commit = item('.p-commit').find('strong').text()
        # print('评价数量：' + commit)
        shopnum = item('.p-shopnum').find('a').text()
        print('出版社：' + shopnum)
        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')


def main():
    parse_website()


if __name__ == "__main__":
    main()
