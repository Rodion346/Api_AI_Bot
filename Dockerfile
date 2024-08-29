# Указываем базовый образ
FROM python:3.11

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы приложения
COPY . /app

# Устанавливаем зависимости
RUN pip install -r requirements.txt

EXPOSE 8000
