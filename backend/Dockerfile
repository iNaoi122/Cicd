FROM python:3.11-slim

WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода
COPY src ./src

# Переменные окружения
ENV PYTHONPATH=/app
ENV DATABASE_URL=sqlite+aiosqlite:///:memory:

# Запуск приложения
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
