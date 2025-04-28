import subprocess
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from classes.manipulacao import Manipulacao
from classes.mensagem import Mensagem

def teste_de_vias():
    roteadores = Manipulacao.roteadores_encontrados()
    print(roteadores)
    for r_origem in roteadores:
        print(f"Testando {r_origem}...")
        try:
            comando = f"docker exec {r_origem} ip route"
            result = subprocess.run(comando, shell=True, check=True, text=True, capture_output=True)
            if result.returncode == 0:
                print(Mensagem.formatar_mensagem(r_origem,(255,255,0)),':',Mensagem.formatar_sucesso(result.stdout))
                print("Quantidade de linhas:",len(Manipulacao.extrair_linhas(result.stdout)))
                
        except subprocess.CalledProcessError as e:
            print(Mensagem.formatar_erro(f"{r_origem} falhou."))
            
def teste_de_vias_table():
    roteadores = Manipulacao.roteadores_encontrados()
    print(roteadores)
    for r_origem in roteadores:
        print(f"Testando {r_origem}...")
        try:
            comando = f"docker exec {r_origem} route -n"
            result = subprocess.run(comando, shell=True, check=True, text=True, capture_output=True)
            if result.returncode == 0:
                print(Mensagem.formatar_mensagem(r_origem,(255,255,0)),':',Mensagem.formatar_sucesso(result.stdout))
                print("Quantidade de linhas:",len(Manipulacao.extrair_linhas(result.stdout)))
                
        except subprocess.CalledProcessError as e:
            print(Mensagem.formatar_erro(f"{r_origem} falhou."))

def teste():
    try:
        comando = f"docker exec roteador2 traceroute 172.21.7.1"
        result = subprocess.run(comando, shell=True, check=True, text=True, capture_output=True)
        if result.returncode == 0:
            print(Manipulacao.traduzir_caminho('roteador2',result.stdout))
    except subprocess.CalledProcessError as e:
        print(Mensagem.formatar_erro(f"roteador2 -> 172.21.7.1 falhou."))

if __name__ == "__main__":
    teste_de_vias()
    teste_de_vias_table()
    print("Teste de rotas concluído.")