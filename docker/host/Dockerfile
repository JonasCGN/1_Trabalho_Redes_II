# Dockerfile para o host
FROM python:3.10-slim

WORKDIR /app

COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Atualizar e instalar pacotes necessários
RUN apt-get update && apt-get install -y \
    iproute2 \
    net-tools \
    iputils-ping \
    traceroute  

# Comando padrão (simples)
CMD ["/app/start.sh"]