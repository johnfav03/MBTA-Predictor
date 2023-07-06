from datetime import datetime, timedelta, timezone
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error
from tensorflow.keras.models import load_model
import numpy as np

file = 'lstm-model.h5'
model = load_model(file)
df = pd.read_csv('data/LR-yesterday.csv')

X = df[['stop_id', 'route_id', 'week_day', 'month_day', 'start_time']].values
y = df['travel_time'].values

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_reshape = X_scaled.reshape(X_scaled.shape[0], 1, X_scaled.shape[1])
y_pred = model.predict(X_reshape)

rmse = np.sqrt(mean_squared_error(y, y_pred))
mae = mean_absolute_error(y, y_pred)
print('2023 RMSE:', rmse)
print('2023 MAE:', mae)

results = pd.read_csv('data/results.csv', index_col=0)
scores = pd.read_csv('data/scores.csv', index_col=0)
row = pd.DataFrame([{
    'date': (datetime.now(timezone.gmt) - timedelta(days=1)).date(),
    'rmse': round(rmse, 2),
    'mae': round(mae, 2),    
}])
scores = pd.concat([scores, row], ignore_index=True)
rows = pd.DataFrame(columns=['time_actual', 'time_predict', 'diff'])

pred = y_pred.flatten().tolist()
pred = [round(val, 2) for val in pred]
for i in range(len(pred)):
    row = pd.DataFrame([{
        'time_actual': y[i],
        'time_predict': pred[i],
        'diff': round((y[i] - pred[i]), 2),
    }])
    rows = pd.concat([rows, row], ignore_index=True)
results = pd.concat([results, rows], ignore_index=True)

scores.to_csv('data/scores.csv')
results.to_csv('data/results.csv')