import pandas as pd
from pandas import Series

df = pd.read_csv("../crawler/example.csv", header=None)

df.columns = ["日期", "人数", "页数"]

# 切割字符串
df["日期"] = df["日期"].str.split(' ').str[0]

df["日期"] = pd.to_datetime(df["日期"], errors='coerce')

# 清洗无效数据
df = df[df["人数"].str.len() < 10]
df['人数'] = df['人数'].str.extract(r'(\d+\.\d+)')

# 增加周几的一列
df["week"] = df["日期"].dt.dayofweek+1

# 去重
df.drop_duplicates(subset=["日期"], keep='first', inplace=True)

# 用日期排序
df.sort_values(by="日期", ascending=False, inplace=True)

df.to_csv("webData_clean.csv")
