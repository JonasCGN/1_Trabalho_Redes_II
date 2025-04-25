import subprocess
from host import Host

def teste_de_ping_roteadores():
    roteadores = Host.roteadores_encontrados()
    hosts = Host.host_encontrados()
    for host in hosts:
        print(f"Testando {host}...")
        for r_destino in roteadores:
            try:
                comando = f"docker exec {host} ping -c 1 -W 0.1 172.21.{Host.extrair_ip_roteadores(r_destino)}.1"
                result = subprocess.run(comando, shell=True, check=True, text=True, capture_output=True)
                if result.returncode == 0:
                    print(Host.formatar_sucesso(f"{host} -> {r_destino}  sucesso."))
            except subprocess.CalledProcessError as e:
                print(Host.formatar_erro(f"{host} -> {r_destino}  falhou."))
            
        print('\n')

if __name__ == "__main__":
    teste_de_ping_roteadores()
    print("Teste de ping concluído.")