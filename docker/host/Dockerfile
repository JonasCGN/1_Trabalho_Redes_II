# Dockerfile para o host
FROM python:3.10-slim

WORKDIR /app

COPY host.py /app/host.py

# Atualizar e instalar pacotes necessários
RUN apt-get update && apt-get install -y \
    iproute2 \
    net-tools \
    iputils-ping \
    traceroute  \
    iperf3

# Comando padrão (simples)
CMD ["python", "host.py"]