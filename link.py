from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep

options= webdriver.ChromeOptions()
options.headless = True
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
f = open("url.txt", "a")

url = ["https://shopee.vn/Th%E1%BB%9Di-Trang-Nam-cat.11035567?page=","https://shopee.vn/Th%E1%BB%9Di-Trang-N%E1%BB%AF-cat.11035639?page="]
for j in url:
    for i in range(99):
        driver.get(j+str(i))
        driver.execute_script ("document.body.style.zoom = '10% '")
        sleep(2)
        url = driver.find_elements_by_xpath("//div[@class='col-xs-2-4 shopee-search-item-result__item']/a")
    
        for a in url:
            it = a.get_attribute('href')
            f.writelines(it+"\n")
            print(it)
        print(len(url)) 
f.close()
