from selenium import webdriver

mobilesetting = {"deviceName":"iPhone 6 Plus"}

options = webdriver.ChromeOptions()

options.add_experimental_option("mobileEmulation", mobilesetting)

driver = webdriver.Chrome(chrome_options=options)
# 设置大小
driver.set_window_size(400, 800)

# driver.maximize_window()
driver.get("https://www.taobao.com")
# 后退
driver.back()
# 前进
driver.forward()
# 刷新
driver.refresh()