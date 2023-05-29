import requests
from bs4 import BeautifulSoup
import re  # 需要用到正则表达式
import datefinder
import time
import random
import csv
import logging

# 加载日志模块
logging.basicConfig(filename='log.txt', level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')

for j in range(0, 3550, 5):
    with open('outData.txt', 'a', encoding='utf-8') as txt:
        with open('example.csv', 'a', newline='') as file:
            writer = csv.writer(file)

            for i in range(j, j + 5):
                url = "https://weibo.cn/2728041997?page={}".format(i + 1)
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
                }

                cookies = {
                    "cookie": "SCF=Aj9fUx2XUIo3-NOUsZCE2HbmXhGEiwe8CNuLb85wMIOyBcT2Vve7APSgQFn0J23AHUQlk4f9ms80zzINHs05GM4.; SUB=_2A25JdrcDDeRhGeFM41AQ-C3MyTSIHXVqmNlLrDV6PUJbktANLXCjkW1NQL9xLT8mBxa48NLy6EX7tAOK3KGFc9DU; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W53ZDUyjaqPkIZbPIrzpWCn5NHD95QNeonEeKn0ehzRWs4DqcjDi--Ni-iWi-2Ei--ciKLhiKnRi--Xi-z4iKyFi--ciKnpiKyFS0M4Shnt; _T_WM=9a252aaa23d8dc3e7fee4b9264e84bce; __bid_n=1886180b18e8b260134207; FPTOKEN=rAJn+aGAN1hUV40QdlYPI3pV2nrFWNPk7NlS2Qe7B18SK+7lgknkX+eYs5U+14r5MqxCgfPxuTHoeSySL5ojA3EBZDlyb4D7UGPsFuP/QaW5hpnpC2Qa/eDTdD+HcUuXIVkKdW7mR/xWpmBE0v9TSsCLnte+U8H3xok1NbK1HXnyrD7d3rD9gpxzRDwU1OELIDWWUiUlot29n+JGwvGDCw2olYjJ/zhE/cBycwJROQdb3mPHH3+G9B92kCJWc2BvAVHCd570cC4xnGCVr2vJboz1QCbqJ+6dih15LFIcu/0MecSKxnzKQvM7L9yD82yiQ1N6at+3YqHTzy1D0gRiwIxymD/w3hWymvkcjFdQ/6okCDkssMmu3p5FVZQBY5I8gcVNMqom79TbX6gt0vBaZw==|87yLNsIeS4VSo/CmSM5CgcGDEREEotx4OQbTrETK2aA=|10|e6bb30cd84920358621f31b4efdbf55c"
                }
                try:
                    resp = requests.get(url, headers=headers, cookies=cookies)
                    # print(resp)
                    pass
                except Exception as e:
                    # print(e)
                    logging.error("获取网页失败，将休息10秒")
                    time.sleep(10)
                    pass

                soup = BeautifulSoup(resp.text, 'html5lib')
                contents = soup.select("div[id^='M_']")

                content_list = []

                for content in contents:
                    temp = {
                        'content': content.find("span", class_="ctt").text
                    }
                    # op = json.load(temp)
                    op = content.find("span", class_="ctt").text
                    if (op.find("中国地铁客流日报") != -1 or op.find("地铁客流排行榜") != -1):
                        if (op.find("主榜风云") == -1):
                            # print(op)
                            content_list.append(op)
                            matches = list(datefinder.find_dates(op))
                            if len(matches) > 0:
                                re1 = r'北京(.*?)万'
                                reResult = re.findall(re1, op)
                                if len(reResult) > 0:
                                    # print(matches[0])
                                    # print(reResult[0] + "万")
                                    logging.info("--成功读取:" + str(matches[0]) + " " + reResult[0] + "万")
                                    txt.write(str(matches[0]) + " " + reResult[0] + "万\n")
                                    l = [str(matches[0]), reResult[0], i + 1]
                                    writer.writerow(l)
                logging.info("成功读取第{}页数据".format(i + 1))

            x = random.randint(3, 6)
            time.sleep(x)

    txt.close()
    file.close()
