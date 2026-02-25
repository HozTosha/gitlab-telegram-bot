FROM python:3.13-slim

WORKDIR /app

# Копируем файл с зависимостями
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем весь код проекта
COPY bot.py .
COPY .env .

# Команда для запуска бота
CMD ["python", "bot.py"]
