from selenium import webdriver
from selenium.webdriver.support.select import Select
driver = webdriver.Chrome()
# 点击接受弹窗
driver.switch_to.alert.accept()

# 点击下拉列表
sel = driver.find_element_by_id("nr")
Select(sel).select_by_index(2)