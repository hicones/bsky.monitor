# Utiliza uma imagem base oficial do Python 3.12 slim
FROM python:3.12-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo requirements.txt para o container
COPY requirements.txt .

# Instala as dependências do Python listadas no requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o conteúdo da pasta local para o diretório de trabalho no container
COPY . .

# Expõe a porta que o WebSocket está usando
EXPOSE 6789

# Comando para rodar o script principal
CMD ["python", "monitor.py"]
