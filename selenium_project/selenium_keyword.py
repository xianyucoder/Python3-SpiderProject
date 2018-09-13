from selenium import webdriver
from selenium.webdriver.common.keys import Keys
driver = webdriver.Chrome()

driver.get("http://www.baidu.com")
driver.find_element_by_id("kw").send_keys("666")
driver.find_element_by_id("kw").send_keys(Keys.BACK_SPACE)

driver.find_element_by_id("kw").send_keys(Keys.CONTROL, 'a')
