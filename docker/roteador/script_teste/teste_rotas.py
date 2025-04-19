import subprocess
from roteador import Roteador

roteador = Roteador()

def teste_de_rotas():
    roteadores = roteador.roteadores_encontrados()
    for r_origem in roteadores:
        print(f"Testando {r_origem}...")
        for r_destino in roteadores:
            if r_origem != r_destino:
                try:
                    comando = f"docker exec {r_origem} traceroute 172.21.{roteador.extrair_ip_roteadores(r_destino)}.1"
                    result = subprocess.run(comando, shell=True, check=True, text=True, capture_output=True)
                    if result.returncode == 0:
                        caminho = roteador.traduzir_caminho(r_origem,result.stdout)
                        print(roteador.formatar_mensagem(r_destino,(255,255,0)),':',roteador.formatar_sucesso(caminho))
                except subprocess.CalledProcessError as e:
                    print(roteador.formatar_erro(f"{r_origem} -> {r_destino} falhou."))

def teste():
    try:
        comando = f"docker exec roteador2 traceroute 172.21.7.1"
        result = subprocess.run(comando, shell=True, check=True, text=True, capture_output=True)
        if result.returncode == 0:
            print(roteador.traduzir_caminho('roteador2',result.stdout))
    except subprocess.CalledProcessError as e:
        print(roteador.formatar_erro(f"{r_origem} -> {r_destino} falhou."))

if __name__ == "__main__":
    teste_de_rotas()
    print("Teste de rotas concluído.")