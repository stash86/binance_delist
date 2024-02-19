FROM python:3.11.6-slim-bullseye
COPY requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt
COPY . .
CMD ["python3", "bot.py"]