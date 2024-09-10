# Usar a imagem base oficial do Python
FROM python:3.10-slim

# Definir o diretório de trabalho dentro do contêiner
WORKDIR /homogenise

# Copiar o arquivo de dependências para dentro do contêiner
COPY requirements.txt .

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install python-dotenv

# Copiar o código da aplicação para dentro do contêiner
COPY . .

RUN pip install gunicorn

EXPOSE 5000

ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:80", "--workers", "3", "--timeout", "120", "main:app"]