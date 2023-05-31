import pandas as pd

df = pd.read_excel('beijing_weather.xlsx')

# 切割字符串
df["日期"] = df["日期"].str.split(' ').str[0]

df["日期"] = pd.to_datetime(df["日期"], errors='coerce')

# 清洗符号
df["最高气温"] = df["最高气温"].str[:-1]
df["最低气温"] = df["最低气温"].str[:-1]

# 提取风速
df['风向'] = df['风向'].str.extract(r'(\d+)')

df.to_csv("weather_clean.csv.csv")
