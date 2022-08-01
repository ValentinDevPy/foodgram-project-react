FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2-binary

RUN pip3 install -r requirements.txt --no-cache-dir

COPY . .

CMD ["gunicorn", "config.wsgi:application", "--bind", "0:8000"]