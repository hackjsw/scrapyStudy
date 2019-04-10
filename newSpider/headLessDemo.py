#coding=utf-8
from selenium import webdriver


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
client = webdriver.Chrome(chrome_options=chrome_options)
# 如果没有把chromedriver加入到PATH中,就需要指明路径 executable_path='/home/chromedriver'

client.get("https://www.baidu.com")
print(client)
client.quit()
