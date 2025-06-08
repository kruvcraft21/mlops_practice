# **MLOps Final Task — DVC + MinIO**

1. Клонируем и поднимаем окружение:

    - git clone https://github.com/your-name/mlops_final_task.git
    - cd mlops_final_task
    - python3 -m venv .venv && source .venv/bin/activate
    - pip install "dvc[s3]" pandas numpy scikit-learn

2. Инициализируем DVC и Git:

    - dvc init
    - git add .dvc .dvcignore
    - git commit -m "Initialize DVC"
    - git push origin main

3. Создаём структуру проекта:

    - mkdir -p data/raw data/balanced data/augmented scripts

    Загружаем свои скрипты в scripts/: load_and_preprocess_newsgroups.py , prepare_newsgroups_v2.py , prepare_newsgroups_v3.py

4. Поднимаем MinIO (локально):

    Создаем докер контейнер:
    
docker run -d -p 9000:9000 -p 9001:9001 \
  -e "MINIO_ROOT_USER=admin" \
  -e "MINIO_ROOT_PASSWORD=admin123" \
  --name minio \
  quay.io/minio/minio server /data --console-address ":9001"

    Web UI: http://localhost:9001

    Login: admin / admin123

    Создаём бакет в интерфейсе: mlops-dvc

5. Подключаем MinIO как удалённое хранилище DVC:

    - dvc remote add -d minio_remote s3://mlops-dvc
    - dvc remote modify minio_remote endpointurl http://localhost:9000
    - dvc remote modify minio_remote access_key_id admin
    - dvc remote modify minio_remote secret_access_key admin123

    - git add .dvc/config
    - git commit -m "Connect DVC to local MinIO (S3-compatible)"
    - git push origin main

6. Создаём первую версию данных (v1):

    - python3 scripts/load_and_preprocess_newsgroups.py
    - git checkout -b v1
    - dvc add data/raw/
    - git add data/raw.dvc data/.gitignore
    - git commit -m "Add raw dataset (version v1)"
    - git push origin v1
    - dvc push

7. Создаём ветку v2 от v1:

    - git checkout -b v2

8. Запускаем скрипт балансировки:

    - python3 scripts/prepare_newsgroups_v2.py

9. Добавляем папку в DVC:

    - dvc add data/balanced/

10. Фиксируем изменения в Git:

    - git add data/balanced.dvc data/.gitignore
    - git commit -m "Add balanced dataset (version v2)"
    - git push origin v2

11. Загружаем данные в MinIO (через DVC):

    - dvc push

12. Создаём ветку v3 от v2:

    - git checkout -b v3

13. Запускаем скрипт аугментации:

    - python3 scripts/prepare_newsgroups_v3.py

14. Добавляем новую папку в DVC:

    - dvc add data/augmented/

15. Фиксируем изменения в Git:

    - git add data/augmented.dvc data/.gitignore
    - git commit -m "Add augmented dataset (version v3)"
    - git push origin v3

16. Загружаем данные в MinIO:

    - dvc push

17. Посмотрим на какой ветке мы находимся?

    - git branch

    Вывод:      main
                v1
                v2
              * v3

    Это значит, что Git считает, что сейчас активна версия v3 (аугментированные данные)

18. Какие датасеты отслеживаются?

    - git ls-files | grep .dvc

    Вывод:  .dvc/.gitignore
            .dvc/config
            .dvcignore
            data/augmented.dvc
            data/balanced.dvc
            data/raw.dvc

    Здесь видно, что все три .dvc файла находятся под Git-контролем в этой ветке

19. Как перейти к v1 ?

    - git checkout v1
    - dvc checkout
    - ls data/

    Вывод:  Переключились на ветку «v1»
            
            Building workspace index                              |4.00 [00:00,  198entry/s]
            Comparing indexes                                     |4.00 [00:00,  279entry/s]
            Applying changes                                      |0.00 [00:00,     ?file/s]
            D       data/balanced/
            D       data/augmented/
            
            raw  raw.dvc

    Видно, что переключилось на ветку v1, DVC выдал, что data/balanced/ и data/augmented/ удалены, потому что они не отслеживаются в ветке v1, и по итогу DVC оставил только data/raw/, потому что в v1 отслеживается только базовая версия.

20. Хотим вернуться, например, на v3?

    - git checkout v3
    - dvc checkout
    - ls data/

    Вывод:  Переключились на ветку «v3»

            Building workspace index                              |4.00 [00:00,  204entry/s]
            Comparing indexes                                     |8.00 [00:00,  236entry/s]
            Applying changes                                      |2.00 [00:00,  7.06file/s]
            A       data/balanced/
            A       data/augmented/

            augmented  augmented.dvc  balanced  balanced.dvc  raw  raw.dvc

    Видно, что снова появились balanced/ и augmented/ с нужными файлами!


# **Вывод:**

1. Версии хранятся в ветках
2. Сами данные отслеживаются DVC
3. Данные переключаются через git checkout + dvc checkout

