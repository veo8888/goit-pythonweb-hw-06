FROM python:3.13-slim

WORKDIR /app

RUN pip install --no-cache-dir faker sqlalchemy alembic psycopg2-binary tabulate

COPY . .

CMD ["sh", "-c", "alembic upgrade head && python seed.py && python my_select.py && sleep infinity"]
