# Dockerfile para o roteador
FROM python:3.9-slim

# Definir diretório de trabalho
WORKDIR /app

# Copiar os arquivos do roteador para dentro do container
COPY roteador.py /app/roteador.py
COPY dijkstra.py /app/dijkstra.py
COPY requirements.txt /app/

# Instalar dependências
RUN apt update && apt install -y iproute2 iputils-ping net-tools
RUN pip install -r requirements.txt

# Comando para iniciar o roteador
CMD ["python", "roteador.py"]
