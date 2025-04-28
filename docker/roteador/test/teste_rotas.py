import subprocess
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from classes.manipulacao import Manipulacao
from classes.mensagem import Mensagem

def teste_de_rotas():
    falha = []
    roteadores = Manipulacao.roteadores_encontrados()
    for r_origem in roteadores:
        print(f"Testando {r_origem}...")
        for r_destino in roteadores:
            if r_origem != r_destino:
                try:
                    comando = f"docker exec {r_origem} traceroute {Manipulacao.extrair_ip_gateway(r_destino)}"
                    result = subprocess.run(comando, shell=True, check=True, text=True, capture_output=True)
                    if result.returncode == 0:
                        caminho = Manipulacao.traduzir_caminho(r_origem,result.stdout)
                        print(Mensagem.formatar_mensagem(r_destino,(255,255,0)),':',Mensagem.formatar_sucesso(caminho))
                except subprocess.CalledProcessError as e:
                    print(Mensagem.formatar_erro(f"{r_origem} -> {r_destino} falhou."))
                    falha.append([r_origem, r_destino])
                    
    if falha:
        print("Roteadores com falha:")
        for roteador, destino in falha:
            print(Mensagem.formatar_erro(f"{roteador} -> {destino}  falhou."))
        print('\n')

def teste():
    try:
        comando = f"docker exec roteador2 traceroute 172.21.7.1"
        result = subprocess.run(comando, shell=True, check=True, text=True, capture_output=True)
        if result.returncode == 0:
            print(Manipulacao.traduzir_caminho('roteador2',result.stdout))
    except subprocess.CalledProcessError as e:
        print(Mensagem.formatar_erro(f"roteador2 -> 172.21.7.1 falhou."))

if __name__ == "__main__":
    teste_de_rotas()
    print("Teste de rotas concluído.")