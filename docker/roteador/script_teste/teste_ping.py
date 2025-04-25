import subprocess
from roteador import Roteador

def teste_de_ping_roteadores():
    falha = []
    
    roteadores = Roteador.roteadores_encontrados()
    for r_origem in roteadores:
        print(f"Testando {r_origem}...")
        for r_destino in roteadores:
            try:
                comando = f"docker exec {r_origem} ping -c 1 -W 0.1 172.21.{Roteador.extrair_ip_roteadores(r_destino)}.2"
                result = subprocess.run(comando, shell=True, check=True, text=True, capture_output=True)
                if result.returncode == 0:
                    print(Roteador.formatar_sucesso(f"{r_origem} -> {r_destino}  sucesso."))
            except subprocess.CalledProcessError as e:
                print(Roteador.formatar_erro(f"{r_origem} -> {r_destino}  falhou."))
                falha.append([r_origem, r_destino])
            
        print('\n')
        
    if falha:
        print("Roteadores com falha:")
        for roteador, destino in falha:
            print(Roteador.formatar_erro(f"{roteador} -> {destino}  falhou."))
        print('\n')

if __name__ == "__main__":
    teste_de_ping_roteadores()
    print("Teste de ping concluído.")