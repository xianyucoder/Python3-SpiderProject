from selenium import webdriver
import pickle

driver = webdriver.Chrome()

driver.get('http://www.baidu.com')

cookie = driver.get_cookies()
print(cookie)
pickle.dump(cookie, open("cookie.txt", "wb"))

driver.close()

web = webdriver.Chrome()
web.get('http://www.baidu.com')
cookie1 = []

cookie1 = pickle.load(open("cookie.txt", "rb"))

for cookie in cookie1:
    print(cookie)
    web.add_cookie(cookie)


web.close()