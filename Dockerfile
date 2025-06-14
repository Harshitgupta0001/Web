FROM python:3.9-slim

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

CMD gunicorn web.app:app & python3 bot.py

