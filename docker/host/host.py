import time
import os
import subprocess
import sys

def run_command(cmd):
    try:
        subprocess.run(cmd, check=True, shell=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar comando: {e}")
        return False

if __name__ == "__main__":
    
    # Verifica se a variável ROTEADOR_CONECTADO está definida
    if "ROTEADOR_CONECTADO" not in os.environ or not os.environ["ROTEADOR_CONECTADO"]:
        print("A variável ROTEADOR_CONECTADO não está definida!")
        sys.exit(1)
        
    roteador_conectado = os.environ["ROTEADOR_CONECTADO"]
    
    # Remove a rota default
    run_command("ip route del default")
    
    # Adiciona a nova rota default via o roteador vizinho
    if not run_command(f"ip route add default via {roteador_conectado} dev eth0"):
        sys.exit(1)
        
    print(f"Rota default configurada via {roteador_conectado}")
    
    # Mantem o processo rodando
    while True:
        time.sleep(1)