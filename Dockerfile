FROM python:3.9-slim

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

CMD bash -c "python bot.py & cd web && gunicorn -b 0.0.0.0:$PORT app:app"
