from selenium import webdriver
import time

driver = webdriver.Chrome()

driver.get('https://login.taobao.com/member/login.jhtml?spm=a21bo.2017.754894437.1.5af911d9rr0hWP&f=top&redirectURL=https%3A%2F%2Fwww.taobao.com%2F')

time.sleep(10)


driver.find_element_by_id('J_Quick2Static').click()

time.sleep(13)

driver.find_element_by_id('TPL_username_1').send_keys('12346')

time.sleep(3)

driver.find_element_by_id('TPL_password_1').send_keys('12346')