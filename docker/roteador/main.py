import os
from classes.roteador import RoteadorApp

if __name__ == "__main__":
    roteador = RoteadorApp()
    print(f"[{os.getenv('ROTEADOR_ID')}] Iniciado...")
    roteador.iniciar_threads()