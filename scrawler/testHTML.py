import json

import requests
import re # 需要用到正则表达式
import datefinder

url="https://m.weibo.cn/api/container/getIndex?containerid=231522type%3D61%26q%3D%23%E4%B8%AD%E5%9B%BD%E5%9C%B0%E9%93%81%E5%AE%A2%E6%B5%81%E6%97%A5%E6%8A%A5%23%26t%3D&page_type=searchall&page=40"
headers ={
    "User-Agent" : "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Mobile Safari/537.36"
}

# cookies ={
#     "cookie": "SCF=Aj9fUx2XUIo3-NOUsZCE2HbmXhGEiwe8CNuLb85wMIOyBcT2Vve7APSgQFn0J23AHUQlk4f9ms80zzINHs05GM4.; SUB=_2A25JdrcDDeRhGeFM41AQ-C3MyTSIHXVqmNlLrDV6PUJbktANLXCjkW1NQL9xLT8mBxa48NLy6EX7tAOK3KGFc9DU; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W53ZDUyjaqPkIZbPIrzpWCn5NHD95QNeonEeKn0ehzRWs4DqcjDi--Ni-iWi-2Ei--ciKLhiKnRi--Xi-z4iKyFi--ciKnpiKyFS0M4Shnt; _T_WM=9a252aaa23d8dc3e7fee4b9264e84bce; __bid_n=1886180b18e8b260134207; FPTOKEN=rAJn+aGAN1hUV40QdlYPI3pV2nrFWNPk7NlS2Qe7B18SK+7lgknkX+eYs5U+14r5MqxCgfPxuTHoeSySL5ojA3EBZDlyb4D7UGPsFuP/QaW5hpnpC2Qa/eDTdD+HcUuXIVkKdW7mR/xWpmBE0v9TSsCLnte+U8H3xok1NbK1HXnyrD7d3rD9gpxzRDwU1OELIDWWUiUlot29n+JGwvGDCw2olYjJ/zhE/cBycwJROQdb3mPHH3+G9B92kCJWc2BvAVHCd570cC4xnGCVr2vJboz1QCbqJ+6dih15LFIcu/0MecSKxnzKQvM7L9yD82yiQ1N6at+3YqHTzy1D0gRiwIxymD/w3hWymvkcjFdQ/6okCDkssMmu3p5FVZQBY5I8gcVNMqom79TbX6gt0vBaZw==|87yLNsIeS4VSo/CmSM5CgcGDEREEotx4OQbTrETK2aA=|10|e6bb30cd84920358621f31b4efdbf55c"
# }

resp = requests.get(url, headers=headers)
resp.encoding = "utf-8"
print(resp)

c = resp.text.encode('utf-8').decode("unicode_escape")



dic=json.loads(resp.text)


for cards in dic['data']['cards']:
    if cards['card_type'] == 9:
        # for card in cards:
        #     # for cad in card:
        #     if card['card_type'] == 9:
        content = cards['mblog']['text']
        content = re.sub(r'<.*?>', '', content)  # 通过正则过滤博文当中的html标签
        c =content
        # print(content)
        matches = list(datefinder.find_dates(c))

        re1 = r'北京(.*?)万'

        if (c.find("中国地铁客流日报") != -1 and len(matches) > 0):
            if (c.find("主榜风云") == -1):
                reResult = re.findall(re1, c)
                print(matches[0])
                print(reResult[0] + "万")



a="https://m.weibo.cn/api/container/getIndex?containerid=231522type%3D1%26t%3D10%26q%3D%23%E4%B8%AD%E5%9B%BD%E5%9C%B0%E9%93%81%E5%AE%A2%E6%B5%81%E6%97%A5%E6%8A%A5%23&extparam=%23%E4%B8%AD%E5%9B%BD%E5%9C%B0%E9%93%81%E5%AE%A2%E6%B5%81%E6%97%A5%E6%8A%A5%23&luicode=10000011&lfid=1076032728041997&nodup=1&page_type=searchall&page=2"
b="https://m.weibo.cn/api/container/getIndex?containerid=231522type%3D1%26t%3D10%26q%3D%23%E4%B8%AD%E5%9B%BD%E5%9C%B0%E9%93%81%E5%AE%A2%E6%B5%81%E6%97%A5%E6%8A%A5%23&extparam=%23%E4%B8%AD%E5%9B%BD%E5%9C%B0%E9%93%81%E5%AE%A2%E6%B5%81%E6%97%A5%E6%8A%A5%23&luicode=10000011&lfid=1076032728041997&nodup=1&page_type=searchall&page=2"
print(a is b)














