import pandas as pd

# Загружаем предварительно обработанный датасет v2
df = pd.read_csv('data_v2.csv')

# Применяем one-hot encoding для 'Sex'
df = pd.get_dummies(df, columns=['Sex'], drop_first=True)

# Сохраняем обработанный датасет как data_v3.csv
df.to_csv('data_v3.csv', index=False)