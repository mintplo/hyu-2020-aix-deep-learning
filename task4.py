import numpy as np
import pandas as pd
import keras
from keras.models import Sequential
from keras.layers.core import Dense, Dropout

processed_data = pd.read_csv('2018-05-trade-new.csv')
processed_data = processed_data.drop(['Unnamed: 0'], axis=1)    # Unnamed: 0 인덱스 제거
processed_data['timestamp'] = pd.to_datetime(processed_data['timestamp'], errors='coerce')
processed_data['timestamp'] = pd.to_numeric(processed_data['timestamp'], errors='coerce')

# 트레이닝 데이터와 테스트 데이터 분류
sample = np.random.choice(processed_data.index, size=int(len(processed_data)*0.9), replace=False)   # 비복원 추출
train_data, test_data = processed_data.iloc[sample], processed_data.drop(sample)

print("Number of training samples is", len(train_data))
print("Number of testing samples is", len(test_data))
print(train_data[:10])
print(test_data[:10])

# ==== Splitting the data into features and targets (labels)
# Now, as a final step before the training, we'll split the data into features (X) and targets (y).
# Also, in Keras, we need to one-hot encode the output. We'll do this with the to_categorical function.

# Separate data and one-hot encode the output
# Note: We're also turning the data into numpy arrays, in order to train the model in Keras
features = np.array(train_data.drop('side', axis=1))
targets = np.array(keras.utils.to_categorical(train_data['side'], 2))
features_test = np.array(test_data.drop('side', axis=1))
targets_test = np.array(keras.utils.to_categorical(test_data['side'], 2))

print(features[:10])
print(targets[:10])

# ==== Defining the model architecture
# Here's where we use Keras to build our neural network.

# Building the model
model = Sequential()
model.add(Dense(256, activation='relu', input_shape=(4,)))
model.add(Dropout(.2))
model.add(Dense(128, activation='relu'))
model.add(Dropout(.1))
model.add(Dense(2, activation='softmax'))

# Compiling the model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.summary()

# ==== Training the Model

# Training the model
model.fit(features, targets, epochs=300, batch_size=90, verbose=0)  # 총 912개의 데이터 Sample Batch Size를 90개씩 나눠 훈련

# ==== Scoring the Model

# Evaluating the model on the training and testing set
score = model.evaluate(features, targets)
print("\n Training Accuracy:", score[1])
score = model.evaluate(features_test, targets_test)
print("\n Testing Accuracy:", score[1])
