import requests
url="https://s.weibo.com/weibo?q=%23%E4%B8%AD%E5%9B%BD%E5%9C%B0%E9%93%81%E5%AE%A2%E6%B5%81%E6%97%A5%E6%8A%A5%23&nodup=1&page=1"
headers ={
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
    "referer" : "https://s.weibo.com/weibo?q=%23%E4%B8%AD%E5%9B%BD%E5%9C%B0%E9%93%81%E5%AE%A2%E6%B5%81%E6%97%A5%E6%8A%A5%23&nodup=1"
}

cookies ={
    "cookie": "SINAGLOBAL=9467083425031.592.1632454605113; ALF=1701704871; UOR=,,www.baidu.com; SUB=_2A25JdrcDDeRhGeFM41AQ-C3MyTSIHXVqmNlLrDV8PUJbkNANLVH_kW1NQL9xLSKhz0uLfOzS22MRoGqwo0MLyc1R; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W53ZDUyjaqPkIZbPIrzpWCn5NHD95QNeonEeKn0ehzRWs4DqcjDi--Ni-iWi-2Ei--ciKLhiKnRi--Xi-z4iKyFi--ciKnpiKyFS0M4Shnt; _s_tentry=weibo.com; Apache=6229180417822.286.1685253881750; ULV=1685253881834:7:3:2:6229180417822.286.1685253881750:1685243691942"
}

resp = requests.get(url, headers=headers, cookies=cookies)
print(resp)

with open('outHTML.txt', 'w', encoding='utf-8') as txt:
    txt.write(resp.text)
    txt.close()
