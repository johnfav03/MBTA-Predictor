import pandas as pd

scores = pd.read_csv('data/scores.csv')
rmse = scores['rmse'].mean()
mae = scores['mae'].mean()

print(f'rmse: {round(rmse, 2)}')
print(f'mae: {round(mae, 2)}')