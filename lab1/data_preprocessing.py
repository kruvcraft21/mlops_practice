import os
import pandas as pd
from sklearn.preprocessing import StandardScaler

# Функция для чтения данных из CSV-файла
def load_data(folder, filename):
    filepath = os.path.join(folder, filename)
    return pd.read_csv(filepath)

# Функция для сохранения данных в CSV-файл
def save_data_to_csv(data, folder, filename):
    filepath = os.path.join(folder, filename)
    data.to_csv(filepath, index=False)
    print(f"Preprocessed data saved to {filepath}")

# Основная функция для предобработки данных
def preprocess_data():
    train_folder = 'train'
    test_folder = 'test'
    
    train_filename = 'train_data.csv'
    test_filename = 'test_data.csv'
    
    # Загрузка данных
    train_data = load_data(train_folder, train_filename)
    test_data = load_data(test_folder, test_filename)
    
    # Извлечение признаков для масштабирования
    features_to_scale = ['pollution_level', 'wind_speed']
    
    X_train = train_data[features_to_scale]
    X_test = test_data[features_to_scale]
    
    # Создание объекта StandardScaler
    scaler = StandardScaler()
    
    # Масштабирование данных
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Создание новых DataFrame с масштабированными данными
    train_data_scaled = train_data.copy()
    test_data_scaled = test_data.copy()
    
    train_data_scaled[features_to_scale] = X_train_scaled
    test_data_scaled[features_to_scale] = X_test_scaled
    
    # Сохранение предобработанных данных
    save_data_to_csv(train_data_scaled, train_folder, 'train_data_scaled.csv')
    save_data_to_csv(test_data_scaled, test_folder, 'test_data_scaled.csv')

if __name__ == "__main__":
    preprocess_data()