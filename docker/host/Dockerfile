# Dockerfile para o host
FROM python:3.10-slim

WORKDIR /app

COPY host.py /app/host.py
COPY script_teste/host.py /app/script_teste/host.py

# Atualizar e instalar pacotes necessários
RUN apt-get update && apt-get install -y \
    iproute2 \
    net-tools \
    iputils-ping \
    traceroute  

# Comando padrão (simples)
CMD ["python" ,"host.py"]