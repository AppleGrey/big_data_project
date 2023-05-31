import pandas as pd

df1 = pd.read_csv("weather_clean.csv",index_col=["日期"])
df2 = pd.read_csv("webData_clean.csv",index_col=["日期"])
df3 = pd.read_csv("AQI_Data.csv",index_col=["日期"])

df=pd.concat([df1,df2,df3],axis=1,join="inner")
new_df = df.dropna(how='any')

new_df.to_csv("result.csv")