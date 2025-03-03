import os
import numpy as np
import pandas as pd

# Создание директорий downloads/train и downloads/test
def create_directories():
    for folder in ['train', 'test']:
        if not os.path.exists(folder):
            os.makedirs(folder)

# Генерация данных о загрязнении воздуха
def generate_air_pollution_data(days=100, noise_level=0.1, anomaly_probability=0.05):
    data = []
    for day in range(days):
        for hour in range(24):  # Для каждого часа дня
            base_pollution = 50 + 40 * np.sin(2 * np.pi * day / 365)
            
            # Влияние времени суток
            if 6 <= hour < 12:  # Утро
                time_factor = 0.8
            elif 12 <= hour < 18:  # День
                time_factor = 1.2
            elif 18 <= hour < 24:  # Вечер
                time_factor = 1.5
            else:  # Ночь
                time_factor = 0.5
            
            # Влияние скорости ветра
            wind_speed = np.random.uniform(0, 10)  # Случайная скорость ветра (м/с)
            wind_factor = max(0, 1 - wind_speed / 10)  # Чем сильнее ветер, тем меньше загрязнение
            
            # Влияние дождя
            is_rain = np.random.rand() < 0.2  # Вероятность дождя 20%
            rain_factor = 0.7 if is_rain else 1.0
            
            # Промышленная активность (выше на рабочих днях)
            is_workday = day % 7 not in [5, 6]  # Выходные дни: суббота и воскресенье
            workday_factor = 1.3 if is_workday else 0.8
            
            # Общий уровень загрязнения
            pollution_level = base_pollution * time_factor * wind_factor * rain_factor * workday_factor
            
            # Добавление случайного шума
            noise = np.random.normal(0, noise_level * 100)
            
            # Добавление аномалий
            if np.random.rand() < anomaly_probability:
                anomaly = np.random.choice([-50, 50])  # Аномалия может быть как положительной, так и отрицательной
            else:
                anomaly = 0
            
            pollution_level += noise + anomaly
            pollution_level = max(0, pollution_level)  # Уровень загрязнения не может быть меньше 0
            
            data.append({
                'day': day,
                'hour': hour,
                'pollution_level': pollution_level,
                'wind_speed': wind_speed,
                'is_rain': int(is_rain),
                'is_workday': int(is_workday)
            })
    
    return pd.DataFrame(data)

# Сохранение данных в CSV-файлы
def save_data_to_csv(data, folder, filename):
    filepath = os.path.join(folder, filename)
    data.to_csv(filepath, index=False)
    print(f"Data saved to {filepath}")

# Основная функция для создания данных
def main():
    create_directories()
    
    # Генерация обучающего и тестового наборов данных
    train_data = generate_air_pollution_data(days=80, noise_level=0.1, anomaly_probability=0.05)
    test_data = generate_air_pollution_data(days=20, noise_level=0.2, anomaly_probability=0.1)
    
    # Сохранение данных
    save_data_to_csv(train_data, 'train', 'train_data.csv')
    save_data_to_csv(test_data, 'test', 'test_data.csv')

if __name__ == "__main__":
    main() 