from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import numpy as np
import re

print("=== Создание базового датасета ===")
data = fetch_20newsgroups(subset='all')
df = pd.DataFrame({'text': data.data, 'target': data.target})

# Очистка текстов
def clean_text(text):
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\S+@\S+', '', text)
    return text
df['text'] = df['text'].apply(clean_text)

# Векторизация TF-IDF
vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
X = vectorizer.fit_transform(df['text'])

# Сохраняем в DataFrame
features_df = pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names_out())
features_df['target'] = df['target']

features_df.to_csv('data/raw/data_v1.csv', index=False)
print("Сохранено в data/raw/data_v1.csv")