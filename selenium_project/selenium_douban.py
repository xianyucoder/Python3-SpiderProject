from selenium import webdriver
import time


driver = webdriver.Chrome()

driver.get("https://www.douban.com/")
driver.find_element_by_id("form_email").send_keys("18450099172")
driver.find_element_by_id("form_password").send_keys("daihuang1995j")

time.sleep(3)

driver.find_element_by_class_name("bn-submit").click()

cookies = {i["name"]: i["value"] for i in driver.get_cookies()}

print(cookies)

time.sleep(5)
driver.close()