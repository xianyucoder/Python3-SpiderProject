from selenium import webdriver
import time
# 实现自动下拉刷新
driver = webdriver.Chrome()

driver.get('https://www.oschina.net/blog')

time.sleep(5)

for i in range(3):
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;')
    time.sleep(3)