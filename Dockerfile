# Рантайм-образ консольного калькулятора.
# Приложение использует только стандартную библиотеку, поэтому
# requirements.txt (там лежит только pytest для тестов) в образ не копируется.
FROM python:3.12-slim

WORKDIR /app

# Копируем только код приложения: тесты, .venv и кэш исключены в .dockerignore
COPY app/ ./app/

# Без буферизации stdout, чтобы ввод-вывод был виден сразу в docker logs / -it
ENV PYTHONUNBUFFERED=1

# Не запускаем от root
RUN useradd --create-home --shell /bin/bash appuser
USER appuser

# Интерактивный запуск требует TTY: docker run -it <image>
CMD ["python", "-m", "app.main"]
