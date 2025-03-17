FROM python:3.8-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["gunicorn", "-b", "0.0.0.0:5000", "src.main:app"]
