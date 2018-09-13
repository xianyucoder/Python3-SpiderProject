from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
driver = webdriver.Chrome()
driver.get("http://www.baidu.com")
# 控制操作的时间在10秒之内
driver.implicitly_wait(10)
# 显示等待
elem =WebDriverWait(driver,15).until(EC.presence_of_element_located((By.ID, "kw")))
# 隐式等待
# if driver.find_element_by_id("num").is_displayed():
#     xxxx