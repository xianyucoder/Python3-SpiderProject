from selenium import webdriver
import time
# 此处应该更换低版本的chrome
driver = webdriver.Chrome()

driver.get("https://www.zhihu.com/signup?next=%2F")

# switch = driver.find_element_by_xpath('//*[@id="root"]/div/main/div/div/div/div[2]/div[2]/span')

switch = driver.find_element_by_xpath('//div[@class="SignContainer-switch"]/span')
if switch.text == '登录':
    switch.click()



# html = driver.page_source
# print(html)

driver.find_element_by_xpath('//div[@class="SignFlow-accountInput Input-wrapper"]/input').send_keys('')
driver.find_element_by_xpath('//div[@class="SignFlowInput"]/div/input').send_keys('')

time.sleep(5)


driver.find_element_by_xpath('//div[@class="Login-content"]/form/button').click()
driver.quit()