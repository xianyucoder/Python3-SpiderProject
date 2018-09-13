from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

driver = webdriver.Chrome()

driver.get("http://www.baidu.com")

above = driver.find_element_by_link_text("设置")

ActionChains(driver).move_to_element(above).perform()

# ActionChains(driver).move_to_element(above).move_to_element(element)  移动

# 单击
ActionChains(driver).move_to_element(above).context_click()

# 双击
ActionChains(driver).move_to_element(above).double_click()

# ActionChains(driver).move_to_element(above).drag_and_drop(element)  拖放