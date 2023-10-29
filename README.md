# Учебный проект по flask - укорачивание ссылок

## Установка
1. Склонируйте репозиторий:
```
git clone git@github.com:ghostblade3301/yacut.git
```
2. Перейдите в директорию с проектом:

```
cd yacut
```

3. Cоздайте и активируйте виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```
4. Обновите пакетный менеджер pip:
```
python3 -m pip install --upgrade pip
```
5. Установите зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```

6. Создайте репозиторий с бд с помощью команды:
```
flask db init
```
## Запуск
Запустите проект:
```
flask run
```