# Use a imagem base do Python
FROM python:3.12-slim

# Define o diretório de trabalho
WORKDIR /app

# Copie o requirements.txt para o diretório de trabalho
COPY requirements.txt .

# Instale as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante do código da aplicação
COPY . .

# Exponha a porta em que o Flask estará rodando
EXPOSE 5000

# Comando para rodar o aplicativo
CMD ["python", "app.py"]
