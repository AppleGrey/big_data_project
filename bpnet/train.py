# 导入库
import datetime

import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense
from tensorflow.keras.optimizers import Adam

from tensorflow.keras.optimizers import SGD
from tensorflow.keras import regularizers


# 加载数据
df = pd.read_csv('result.csv')
df = df[df['人数']>600]
df["日期"] = pd.to_datetime(df["日期"], errors='coerce')
# df.filter(df['日期']>datetime.date(2021,1,1))
df = df[(df['日期'].dt.date>datetime.datetime.strptime('20230101', '%Y%m%d').date()) | (df['日期'].dt.date<datetime.datetime.strptime('20200101', '%Y%m%d').date())]
df['月'] = df['日期'].dt.month
df['日'] = df['日期'].dt.day
df['天气'] = pd.factorize(df['天气'])[0]
x = df[['最高气温', '最低气温','AQI','风向','月','日','天气','week']].values
y = df[['人数']].values

# print(min(y))
# print(max(y))

# 数据归一化
x_scaler = MinMaxScaler(feature_range=(-1, 1))
y_scaler = MinMaxScaler(feature_range=(-1, 1))
x = x_scaler.fit_transform(x)
y = y_scaler.fit_transform(y)

x, x_test, y, y_test = train_test_split(x, y, test_size=0.1, random_state=42)

# 定义神经网络模型
model = Sequential()
model.add(Dense(32, activation='relu', input_shape=(8,)))
model.add(Dense(8, activation='relu'))
model.add(Dense(1, activation='linear'))

# 误差记录
optimizer = Adam(0.0001)
# optimizer=SGD(lr=0.01, decay=0.00001, momentum=0.9, nesterov=True)
# model.compile(optimizer=optimizer, loss='mse')
model.compile(optimizer=optimizer, loss='mse')
# model.compile(loss='categorical_crossentropy', optimizer=sgd, class_mode='categorical')

# 训练模型
history = model.fit(x, y, epochs=300, batch_size=1)


# 评估模型
mse = model.evaluate(x, y)
print('Validation MSE:', mse)

# 保存模型的权重和偏差
model.save('my_model.h5')

# 误差曲线
# 设置中文显示和解决负号显示问题
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.plot(history.history['loss'])
plt.title("模型误差")
plt.ylabel("误差")
plt.xlabel("循环次数")
plt.show()

# 预测值输出
y_pred = model.predict(x_test)

mse = model.evaluate(x_test, y_test)
print('Validation MSE:', mse)

# 预测值反归一化
y_test = y_scaler.inverse_transform(y_test)
y_pred = y_scaler.inverse_transform(y_pred)
print("the prediction is:", y_pred)



# 将预测值存储到Excel表中
df_out = pd.DataFrame(y_pred, columns=['Prediction'])
df_out.to_excel('prediction.xlsx', index=False)

# 实际值与预测值的对比图
# 设置中文显示和解决负号显示问题
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.scatter(y_test, y_pred)
plt.plot([y.min(), y.max()], [y.min(), y.max()], 'k--', lw=4)
plt.xlabel("实际值")
plt.ylabel("预测值")
plt.show()

mse = model.evaluate(x_test, y_test)
print('Validation MSE:', mse)