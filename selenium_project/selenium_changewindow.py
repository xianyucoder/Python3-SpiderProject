from selenium import webdriver
driver = webdriver.Chrome()

first_win = driver.current_window_handle

all_win = driver.current_window_handle

for win in all_win:
    if win != first_win:
        driver.switch_to.window(win)

