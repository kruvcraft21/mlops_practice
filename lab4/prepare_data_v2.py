import pandas as pd

# Загружаем предварительно обработанный датасет v1
df = pd.read_csv('data_v1.csv')

# Заполняем пропуски в 'Age' средним значением
df['Age'] = df['Age'].fillna(df['Age'].mean())

# Сохраняем обработанный датасет как data_v2.csv
df.to_csv('data_v2.csv', index=False)