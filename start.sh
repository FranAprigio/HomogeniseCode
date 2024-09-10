#!/bin/bash

# Nome da rede
#NETWORK_NAME=db

# Verifica se a rede existe
#if ! docker network ls | grep -q $NETWORK_NAME; then
#  echo "Rede '$NETWORK_NAME' não encontrada. Criando..."
#  docker network create $NETWORK_NAME
#else
#  echo "Rede '$NETWORK_NAME' já existe."
#fi

# Inicia os contêineres
docker compose up --build -d 
