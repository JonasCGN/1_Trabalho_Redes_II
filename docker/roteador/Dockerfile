FROM python:3.10-slim

# Definir diretório de trabalho
WORKDIR /app

# Copiar os arquivos do roteador para dentro do container
COPY roteador.py /app/roteador.py
COPY dijkstra.py /app/dijkstra.py
COPY script_teste/roteador.py /app/script_teste/roteador.py
COPY requirements.txt /app/

# Instalar dependências
RUN apt update && apt install -y \
    iproute2 \
    iputils-ping \
    net-tools \
    traceroute  # Instalar o traceroute

# Instalar as dependências Python
RUN pip install -r requirements.txt

# Comando para iniciar o roteador
CMD ["python", "roteador.py"]
