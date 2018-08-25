#-*- coding:utf-8 -*-
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
from .rent_mysql import *

def rent_crawl(location):
    rent_obj=Housing_Resources('localhost','root','123456')
    try:
        rent_obj.createDB()
    except Exception:
        print('已经存在库')

    url = "http://gz.58.com/pinpaigongyu/pn/{page}/?PGTID={location}"

    #已完成的页数序号，初时为0
    page = 0

    # csv_file = open("rent.csv","w") 
    # csv_writer = csv.writer(csv_file, delimiter=',')
    try:
        rent_obj.useDB()
        rent_obj.createTable(location)

        while True:
            page += 1
            print("fetch: ", url.format(page=page,location=location))
            response = requests.get(url.format(page=page,location=location))
            html = BeautifulSoup(response.text)
            house_list = html.select(".list > li")

            # 循环在读不到新的房源时结束
            if not house_list:
                break

            for house in house_list:
                house_title = str(house.select("h2")[0])
                house_title_n=house_title[4:][:-5]
                house_url = urljoin(url, house.select("a")[0]["href"])
                house_info_list = house_title_n.split(" ")
                print(house_info_list)
                for x in house_info_list:
                    print(x)
                # 如果第二列是公寓名则取第一列作为地址
                if "公寓" in house_info_list[1] or "青年社区" in house_info_list[1]:
                    house_location = house_info_list[0]
                else:
                    house_location = house_info_list[1]

                house_money = house.select(".money")[0].select("b")[0].string.encode("utf8")
                rent_obj.enterData(house_title, house_location, house_money, house_url,location)

          
    #         csv_writer.writerow([house_title, house_location, house_money, house_url])
    except Exception:
        print('已经存在表,不再爬数据')

    # csv_file.close()