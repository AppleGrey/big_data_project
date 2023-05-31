import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense
from keras import backend as K

# 读取数据
data = pd.read_excel('dataset.xls')

# 将日期作为索引，并将其转化为时间序列
data = data.set_index(pd.to_datetime(data['日期']))

# 按照时间顺序进行排序
data = data.sort_index()

# 对天气情况进行编码
data['天气情况'] = pd.factorize(data['天气情况'])[0]

# 将是否为假期转化为0和1
data['是否为假期'] = data['是否为假期'].apply(lambda x: 1 if x == '是' else 0)

# 将地铁每日人流量作为输出变量
y = data['地铁每日人流量']

# 将天气情况、最高温度、最低温度、是否为假期和AQI作为特征变量
X = data[['天气情况', '最高温度', '最低温度', '是否为假期', 'AQI']]

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 特征归一化
scaler = MinMaxScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 转换为PyTorch的张量
X_train_tensor = torch.tensor(X_train_scaled, dtype=torch.float32)
X_test_tensor = torch.tensor(X_test_scaled, dtype=torch.float32)
y_train_tensor = torch.tensor(y_train.values, dtype=torch.float32).view(-1, 1)
y_test_tensor = torch.tensor(y_test.values, dtype=torch.float32).view(-1, 1)

# 定义Keras模型
model = Sequential()
model.add(Dense(64, input_dim=X_train_tensor.shape[1], activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(1, activation='linear'))

# 定义PyTorch的优化器和损失函数
optimizer = optim.Adam(model.parameters(), lr=0.001)
criterion = nn.MSELoss()


# 定义Keras中的自定义回调函数来使用PyTorch的优化器和损失函数
class PyTorchCallback(K.callbacks.Callback):
    def on_train_batch_end(self, batch, logs=None):
        X_batch = torch.tensor(self.model.predict_on_batch(self.validation_data[0]), dtype=torch.float32)
        y_batch = torch.tensor(self.validation_data[1], dtype=torch.float32)

        optimizer.zero_grad()
        outputs = self.model.train_on_batch(X_batch, y_batch)
        loss = criterion(torch.tensor(outputs, dtype=torch.float32).view(-1, 1), y_batch)
        loss.backward()
        optimizer.step()


# 创建Keras模型的实例
keras_model = model

# 使用PyTorch的优化器和损失函数来训练Keras模型
keras_model.compile(loss='mean_squared_error', optimizer=optimizer)
history = keras_model.fit(X_train_scaled, y_train, epochs=100, batch_size=32, verbose=1,
                          validation_data=(X_test_scaled, y_test),
                          callbacks=[PyTorchCallback()])

# 在测试集上进行预测
y_pred = keras_model.predict(X_test_scaled)

# 反归一化预测结果
y_pred = scaler.inverse_transform(y_pred)

# 计算均方根误差（RMSE）
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

# 打印RMSE
print('BP神经网络模型的RMSE为：', rmse)

# 绘制预测结果图
plt.plot(y_test.index, y_test.values, label='True')
plt.plot(y_test.index, y_pred, label='Predicted')
plt.legend()
plt.show()
