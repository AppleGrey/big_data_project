import pandas as pd
import datetime

airDf = pd.DataFrame(columns=["日期", "AQI"])

for y in range(2018, 2024):
    day = datetime.date(y, 1, 1)
    days = 365
    if y == 2020:
        days = 366
    if y == 2023:
        days = 147
    for d in range(days):
        try:
            df = pd.read_csv('../air_dataset/beijing_{}/beijing_all_{}.csv'.format(y, day.strftime('%Y%m%d')))
            pass
        except Exception as e:
            print("--无" + day.strftime('%Y%m%d'))
            day = day + datetime.timedelta(days=1)
            continue
            pass

        # 删除无关行
        df = df[df["type"] == 'AQI']

        # 删除无关列
        df = df.drop(columns=["date", "hour", "type"])

        # 计算平均值
        mean_aqi = df.mean()
        m = pd.Series.mean(mean_aqi)
        # newLine = pd.DataFrame([day.strftime("%Y-%m-%d"), round(m, 3)])
        airDf.loc[len(airDf)] = [day.strftime("%Y-%m-%d"), round(m, 3)]
        print("成功读取" + day.strftime('%Y%m%d'))
        day = day + datetime.timedelta(days=1)
airDf.to_csv("AQI_Data.csv")
