import pandas as pd
import numpy as np
from sklearn.utils import resample

print("=== Балансировка датасета ===")
df = pd.read_csv('data/raw/data_v1.csv')

# Балансировка классов
balanced_dfs = []
for class_idx in df['target'].unique():
    class_df = df[df['target'] == class_idx]
    if len(class_df) < 1000:
        class_df = resample(class_df,
                          replace=True,
                          n_samples=1000,
                          random_state=42)
    balanced_dfs.append(class_df)

balanced_df = pd.concat(balanced_dfs)
balanced_df.to_csv('data/balanced/data_v2.csv', index=False)
print("Сохранено в data/balanced/data_v2.csv")