from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import re
import csv

options= webdriver.ChromeOptions()
options.headless = True
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

header = ['tên','giá','shop','huy hiệu shop','đã bán','sao', 
          'số lượng 1 sao','số lượt đánh giá','Xuất xứ',
          'Chất liệu','Mẫu','Kho hàng','Gửi từ']

f = open("url.txt", "r")
url = f.readlines()
f.close()
def convert_str_to_number(x):
    total_stars = 0
    num_map = {'K':1000}
    if x.isdigit():
        total_stars = int(x)
    else:
        if len(x) > 1:
            total_stars = float(x[:-1]) * num_map.get(x[-1].upper(), 1)
    return str(int(total_stars))

with open('data.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=header)
    writer.writeheader()
    for i in url:
        driver.get(i)
        sleep(1)
        b = driver.find_elements_by_xpath('//div[contains(@class,"attM6y")]/span')
        c = driver.find_elements_by_xpath('//div[contains(@class,"OitLRu _1mYa1t")]')
        d = driver.find_elements_by_xpath('//div[contains(@class,"aca9MM")]')
        e = driver.find_elements_by_xpath('//div[contains(@class,"Ybrg9j")]')
        shop = driver.find_elements_by_xpath('//div[contains(@class,"_3uf2ae")]')
        sao1 = driver.find_elements_by_xpath('//*[contains(text(), "1 Sao")]')
        danhgia = driver.find_elements_by_xpath('//div[contains(@class,"OitLRu")]')
        chitiet = driver.find_elements_by_xpath('//div[contains(@class,"aPKXeO")]')
        danhhieushop = driver.find_elements_by_xpath('//div[contains(@class,"_1x8-jJ _12TgA3 _34VdaU")]')
        try:
            danhhieushop = danhhieushop[1].text
        except:
            danhhieushop = "none"
        try:
            ten = b[0].text
        except:
            ten = "none"
        try:
            gia = e[0].text
        except:
            gia = "none"
        try:
            shop = shop[0].text
        except:
            shop = "none"
        try:
            sao = c[0].text
        except:
            sao = "none"
        try:
            daban = convert_str_to_number(d[0].text.replace(",", "."))
        except:
            daban = "0"
        # số lượng 1 sao
        try:
            sao1 = re.search(r"\(([A-Za-z0-9_]+)\)", sao1[0].text).group(1)
        except:
            sao1 = "0"
        #đánh giá
        try:
            danhgia = convert_str_to_number(danhgia[1].text.replace(",", "."))
        except:
            danhgia = "0"
        
        xuatxu, chatlieu, mau, khohang, guitu = "none", "none", "none", "none", "none"
        for i in chitiet:
            item = i.find_element_by_class_name('SFJkS3').text
            if item == 'Xuất xứ':
                xuatxu = i.find_elements_by_xpath('div')[0].text
            elif item == 'Chất liệu':
                chatlieu = i.find_elements_by_xpath('div')[0].text
            elif item == 'Mẫu':
                mau = i.find_elements_by_xpath('div')[0].text
            elif item == 'Kho hàng':
                khohang = i.find_elements_by_xpath('div')[0].text
            elif item =='Gửi từ':
                guitu = i.find_elements_by_xpath('div')[0].text
        
        
        data = [
                    {'tên': ten,
                    'giá': gia,
                    'shop': shop,
                    'huy hiệu shop': danhhieushop,
                    'đã bán': daban,
                    'sao': sao,
                    'số lượng 1 sao': sao1,
                    'số lượt đánh giá': danhgia,
                    'Xuất xứ': xuatxu,
                    'Chất liệu': chatlieu,
                    'Mẫu': mau,
                    'Kho hàng': khohang,
                    'Gửi từ': guitu
                    }
                ]
        print(data)
        writer.writerows(data)
    
