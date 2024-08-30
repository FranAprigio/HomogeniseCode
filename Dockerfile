FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN python3 -m pip install --upgrade pip && \
    pip install --upgrade pip

RUN pip install gunicorn

EXPOSE 5000

ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:80", "--workers", "3", "--timeout", "120", "main:app"]
