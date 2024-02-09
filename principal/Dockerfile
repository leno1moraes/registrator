# Usa uma imagem base do Python
FROM python:3.9

# Define o diretório de trabalho no contêiner
WORKDIR /app

# Copia o arquivo de requisitos para o contêiner
COPY requirements.txt requirements.txt

# Instala as dependências Python especificadas no arquivo de requisitos
RUN pip install -r requirements.txt

# Copia o código-fonte do backend para o contêiner
COPY . .

# Comando padrão para executar o servidor Flask
CMD ["python", "app.py"]
