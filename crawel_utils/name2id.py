import time
from selenium import webdriver
import os

if __name__ == '__main__':
    chromedriver = "/Users/acke/Downloads/chromedriver"
    os.environ["webdriver.chrome.driver"] = chromedriver
    driver = webdriver.Chrome(chromedriver)

    driver.get('http://maoyan.com/')
    # driver.get('http://www.baidu.com/')
    driver.maximize_window()
    print('wait')
    time.sleep(5)

    driver.find_element_by_name("kw")\
        .send_keys(u"一出好戏")
    driver.find_element_by_class_name("submit")\
        .click()

    # all_hand = driver.window_handles
    # 切换句柄
    # driver.switch_to_window(all_hand[-1])


    #
    # driver.find_element_by_class_name("movie-list")
    #     .click()
