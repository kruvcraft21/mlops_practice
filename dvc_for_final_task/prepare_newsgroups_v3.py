import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

print("=== Аугментация датасета ===")
df = pd.read_csv('data/balanced/data_v2.csv')

# Простая аугментация - дублируем часть данных
augment_size = min(500, len(df)//3)  # Дублируем 500 или 1/3 данных
augmented_df = df.sample(n=augment_size, random_state=42)
final_df = pd.concat([df, augmented_df])

final_df.to_csv('data/augmented/data_v3.csv', index=False)
print("Сохранено в data/augmented/data_v3.csv")