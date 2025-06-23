# 1. Usar uma imagem base do Python
FROM python:3.9-slim

# 2. Definir o diretório de trabalho dentro do container
WORKDIR /project

# 3. Definir o PYTHONPATH para facilitar as importações entre pastas
ENV PYTHONPATH "${PYTHONPATH}:/project"

# 4. Copiar e instalar as dependências
COPY requirements.txt .
RUN pip install -r requirements.txt

# 5. Copiar todo o código do projeto para o container
COPY ./app ./app
COPY ./data_generator ./data_generator