# Usar a imagem base oficial do Python
FROM python:3.10-slim

# Definir o diretório de trabalho dentro do contêiner
WORKDIR /homogenise

# Copiar o arquivo de dependências para dentro do contêiner
COPY requirements.txt .

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código da aplicação para dentro do contêiner
COPY . .

# Definir as variáveis de ambiente (opcional)
ENV FLASK_APP=homogenise
ENV FLASK_RUN_HOST=0.0.0.0

# Comando para rodar o Flask
CMD ["flask", "run"]

