FROM python:3.12.10

WORKDIR /app

RUN pip3 install --no-cache-dir poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root

COPY app ./app

RUN mkdir -p /app/static /app/static/uploads

COPY docker/wait-for-it.sh /app/wait-for-it.sh
RUN chmod +x /app/wait-for-it.sh

ENV PYTHONPATH=/app

CMD ["uvicorn", "app.main:application", "--host", "0.0.0.0", "--port", "8000"]