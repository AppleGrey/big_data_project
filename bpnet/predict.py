# 导入库
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model

# 数据预处理（归一化）
df = pd.read_csv('result.csv')
df = df[df['人数']>200]
df["日期"] = pd.to_datetime(df["日期"], errors='coerce')
df['月'] = df['日期'].dt.month
df['日'] = df['日期'].dt.day
df['天气'] = pd.factorize(df['天气'])[0]
x = df[['最高气温', '最低气温','AQI','风向','月','日','天气','week']].values
y = df[['人数']].values

# 数据归一化
x_scaler = MinMaxScaler(feature_range=(-1, 1))
y_scaler = MinMaxScaler(feature_range=(-1, 1))
x = x_scaler.fit_transform(x)
y = y_scaler.fit_transform(y)

# 加载预测数据
# df_test = pd.read_csv('test.csv')
df_test = pd.DataFrame(
    {"最高气温": [25, 26],
     "最低气温": [17, 25],
     "AQI":[88,65],
     "风向":[3,3],
     "月":[5,5],
     "日":[30,31],
     "天气":[7,3],
     "week":[2,3],
     }
)
df_test['天气'] = pd.factorize(df_test['天气'])[0]
print(df_test)
x_test = df_test[['最高气温', '最低气温','AQI','风向','月','日','天气','week']].values

# 预测数据归一化
x_test = x_scaler.transform(x_test)

# 加载训练好的神经网络模型
model = load_model('my_model.h5')

# 对预测数据进行预测
y_pred = model.predict(x_test)
y_pred = y_scaler.inverse_transform(y_pred)
print(y_pred)
