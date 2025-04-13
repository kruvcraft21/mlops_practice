from catboost.datasets import titanic
import pandas as pd

# Загружаем датасет
train_df, _ = titanic()

# Оставляем нужные столбцы
df = train_df[['Pclass', 'Sex', 'Age']]

# Сохраняем
df.to_csv('data_v1.csv', index=False)
