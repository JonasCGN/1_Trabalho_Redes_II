#!/bin/sh
set -e

# Verifica se a variável ROTEADOR_VIZINHO está definida
if [ -z "$ROTEADOR_CONECTADO" ]; then
  echo "A variável ROTEADOR_CONECTADO não está definida!"
  exit 1
fi

# Remove a rota default
ip route del default

# Adiciona a nova rota default via o roteador vizinho (garantindo que a variável tenha o valor correto)
ip route add default via "$ROTEADOR_CONECTADO" dev eth0

exec sleep infinity