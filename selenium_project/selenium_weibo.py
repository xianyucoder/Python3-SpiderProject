from selenium import webdriver
import time
# 实现微博自动登录
driver = webdriver.Chrome()

driver.get("https://weibo.com/login.php")

time.sleep(15)

driver.find_element_by_css_selector('#loginname').send_keys('')

driver.find_element_by_css_selector('.info_list.password input[name="password"]').send_keys('')

driver.find_element_by_css_selector('.info_list.login_btn a[node-type="submitBtn"]').click()

time.sleep(2)
# 记得关闭登录保护
# driver.quit()