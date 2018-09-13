from selenium import webdriver
# 设置不加载图片
chrome_opt = webdriver.ChromeOptions()
prefs = {
    "profile.managed_default_content_settings.images": 2
}

chrome_opt.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(chrome_options=chrome_opt)

driver.get("https://www.taobao.com")