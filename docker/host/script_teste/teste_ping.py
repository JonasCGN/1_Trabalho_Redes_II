import subprocess
from host import Host

def teste_de_ping_hosts():
    falha = []
    hosts = Host.host_encontrados()
    for host in hosts:
        print(f"Testando {host}...")
        for r_destino in hosts:
            try:
                comando = f"docker exec {host} ping -c 1 -W 0.1 172.21.{Host.extrair_ip_hosts(r_destino)}"
                result = subprocess.run(comando, shell=True, check=True, text=True, capture_output=True)
                if result.returncode == 0:
                    print(Host.formatar_sucesso(f"{host} -> {r_destino}  sucesso."))
            except subprocess.CalledProcessError as e:
                print(Host.formatar_erro(f"{host} -> {r_destino}  falhou."))
                falha.append([host, r_destino])
        print('\n')
        
    if falha:
        print("Host com falha:")
        for roteador, destino in falha:
            print(Host.formatar_erro(f"{roteador} -> {destino}  falhou."))
        print('\n')

def teste_de_ping_roteadores():
    falha = []
    roteadores = Host.roteadores_encontrados()
    hosts = Host.host_encontrados()
    for host in hosts:
        print(f"Testando {host}...")
        for r_destino in roteadores:
            try:
                comando = f"docker exec {host} ping -c 1 172.21.{Host.extrair_ip_roteadores(r_destino)}.2"
                result = subprocess.run(comando, shell=True, check=True, text=True, capture_output=True)
                if result.returncode == 0:
                    print(Host.formatar_sucesso(f"{host} -> {r_destino}  sucesso."))
            except subprocess.CalledProcessError as e:
                print(Host.formatar_erro(f"{host} -> {r_destino}  falhou."))
                falha.append([host, r_destino])
            
        print('\n')

    if falha:
        print("Hosts com falha:")
        for host, roteador in falha:
            print(Host.formatar_erro(f"{host} -> {roteador}  falhou."))
        print('\n')
    
def teste():
    texto = ["host2a", "host3b", "host4c", "host5d"]

    for i in texto:
        print(Host.extrair_ip_hosts(i))

if __name__ == "__main__":
    teste_de_ping_hosts()
    print("Teste de ping concluído.")