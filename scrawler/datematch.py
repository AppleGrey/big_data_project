import datefinder
import dateutil.parser as dp

matches = list(datefinder.find_dates("#地铁客流排行榜#</a> 2022-11-03（周四，农历十月初十）<a href=\"https://s.weibo.com/weibo?q=%23%E4%B8%AD%E5%9B%BD%E5"))
if len(matches)>0 :
    print(matches[0])