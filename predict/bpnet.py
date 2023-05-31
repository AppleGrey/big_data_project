# 导入库
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import regularizers

# 加载数据
df = pd.read_csv('result.csv')
x = df[['日期', '最高气温', '最低气温']].values
y = df[['人数']].values

# 数据归一化
x_scaler = MinMaxScaler(feature_range=(-1, 1))
y_scaler = MinMaxScaler(feature_range=(-1, 1))
x = x_scaler.fit_transform(x)
y = y_scaler.fit_transform(y)

# 定义神经网络模型
model = Sequential()
model.add(Dense(3, activation='relu', input_shape=(3,), kernel_regularizer=regularizers.l2(0.01)))
model.add(Dense(16, activation='relu', kernel_regularizer=regularizers.l2(0.01)))
model.add(Dense(1, activation='linear'))

# 误差记录
optimizer = Adam(lr=0.0001)
model.compile(optimizer=optimizer, loss='mse')

# 训练模型
history = model.fit(x, y, epochs=10, batch_size=8)

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
y_pred = model.predict(x)

# 预测值反归一化
y = y_scaler.inverse_transform(y)
y_pred = y_scaler.inverse_transform(y_pred)
print("the prediction is:", y_pred)

# 将预测值存储到Excel表中
df_out = pd.DataFrame(y_pred, columns=['Prediction'])
df_out.to_excel('prediction.xlsx', index=False)

# 实际值与预测值的对比图
# 设置中文显示和解决负号显示问题
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.scatter(y, y_pred)
plt.plot([y.min(), y.max()], [y.min(), y.max()], 'k--', lw=4)
plt.xlabel("实际值")
plt.ylabel("预测值")
plt.show()