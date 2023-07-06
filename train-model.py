import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.metrics import mean_squared_error, mean_absolute_error
import os

file = 'lstm-model.h5'
if not os.path.exists(file):
    # Load the CSV dataset
    df = pd.read_csv('data/LR-aggregate.csv')
    # Split the dataset into input features (X) and target variable (y)
    X = df[['stop_id', 'route_id', 'week_day', 'month_day', 'start_time']].values
    y = df['travel_time'].values
    # Normalize the input features
    X = (X - X.mean()) / X.std()
    # Normalize the input features using StandardScaler
    scaler = StandardScaler()
    X = scaler.fit_transform(X)
    # Reshape the input features to match the LSTM input shape
    X = X.reshape(X.shape[0], 1, X.shape[1])
    # Define the LSTM model
    model = Sequential()
    model.add(LSTM(units=128, input_shape=(1, X.shape[2])))
    model.add(Dense(units=1))
    # Compile the model
    model.compile(loss='mean_absolute_error', optimizer='adam')
    # Train the model
    model.fit(X, y, epochs=25, batch_size=16)
    # Save the trained model
    model.save(file)
# Load the saved model
model = load_model(file)
# Load the CSV file
df = pd.read_csv('data/LR-aggregate.csv')
# Split the data into input features (X) and target variable (y)
X = df[['stop_id', 'route_id', 'week_day', 'month_day', 'start_time']].values
y = df['travel_time'].values
# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)
# Create a scaler object
scaler = StandardScaler()
X_test_orig = X_test
# Fit and transform the input features
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)
# Reshape the input features to match the LSTM input shape
X_test = X_test.reshape(X_test.shape[0], 1, X_test.shape[1])
# Make predictions on the testing set
y_pred = model.predict(X_test)
# Calculate RMSE
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
# Calculate MAE
mae = mean_absolute_error(y_test, y_pred)
print('2023 RMSE:', rmse)
print('2023 MAE:', mae)