import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
import time

with open('beijing.csv', 'a', newline='') as file:
    writer = csv.writer(file)
    for year in range(2017,2024):
        for month in range(1,13):
            url = "http://www.tianqihoubao.com/lishi/beijing/month/{}.html".format(str(year)+str(month).zfill(2))
            try:
                resp = requests.get(url)
                # print(resp)
                pass
            except Exception as e:
                # print(e)
                # logging.error("获取网页失败，将休息10秒")
                time.sleep(10)
                resp = requests.get(url)
                pass
            html = resp.content.decode('gbk')

            soup = BeautifulSoup(html, 'html.parser')

            tr_list = soup.find_all('tr')  # 搜索想要的数据：所有的tr标签
            dates, conditions, temp = [], [], []  # 只想要这三种数据
            for data in tr_list[1:]:  # tr_list[1:]是舍弃第一个tr标签，不需要
                # sub_data = data.text #获取到数据
                sub_data = data.text.split()  # 删除数据中的空白区域
                # print(sub_data)
                dates.append(sub_data[0])
                dat = sub_data[0]
                conditions.append(''.join(sub_data[1:3]))  # ''表示分隔符；数据取到1，取不到3
                con = ''.join(sub_data[1:3])
                temp.append(''.join(sub_data[3:6]))
                t = ''.join(sub_data[3:6])
                l = [dat,con,t]
                writer.writerow(l)

            # s_data = pd.DataFrame()
            # s_data['日期'] = dates  # 列名为’日期‘
            # s_data['天气状况'] = conditions
            # s_data['气温'] = temp
            # l = [dates, conditions, temp]
            # writer.writerow(l)
            print(str(year)+str(month).zfill(2)+"爬取成功")

