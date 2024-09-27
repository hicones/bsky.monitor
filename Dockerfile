# Usar a imagem oficial do Python como base
FROM python:3.9-slim

# Definir o diretório de trabalho dentro do container
WORKDIR /app

# Copiar o arquivo de dependências
COPY requirements.txt requirements.txt

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante dos arquivos do projeto para o container
COPY . .

# Definir a variável de ambiente para não gerar arquivos .pyc
ENV PYTHONDONTWRITEBYTECODE 1

# Definir a variável de ambiente para a saída do buffer ser exibida (importante para logs)
ENV PYTHONUNBUFFERED 1

# Expor a porta 6789 (porta do WebSocket)
EXPOSE 6789

# Comando para rodar o script principal
CMD ["python", "monitor.py"]
