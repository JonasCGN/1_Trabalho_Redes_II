import time
import socket

meu_nome = socket.gethostname()
meu_ip = socket.gethostbyname(meu_nome)

print(f"[{meu_nome}] Iniciado com IP {meu_ip}.")

while True:
    time.sleep(60)
