import subprocess
from host import Host

def habilitar_ip_forward_em_roteadores():
    roteadores = Host.roteadores_encontrados()
    for r in roteadores:
        try:
            comando = ["docker", "exec", r, "sh", "-c", "echo 1 > /proc/sys/net/ipv4/ip_forward"]
            subprocess.run(comando, check=True, text=True)
            print(Host.formatar_sucesso(f"IP forward ativado em {r}"))
        except subprocess.CalledProcessError:
            print(Host.formatar_erro(f"Falha ao ativar IP forward em {r}"))

def teste_de_ping_hosts():
    hosts = Host.host_encontrados()
    for host in hosts:
        print(f"Testando {host}...")
        for r_destino in hosts:
            try:
                comando = f"docker exec {host} ping -c 1 -W 0.1 172.21.{Host.extrair_ip_hosts(r_destino)}.10"
                result = subprocess.run(comando, shell=True, check=True, text=True, capture_output=True)
                if result.returncode == 0:
                    print(Host.formatar_sucesso(f"{host} -> {r_destino}  sucesso."))
            except subprocess.CalledProcessError as e:
                print(Host.formatar_erro(f"{host} -> {r_destino}  falhou."))
            
        print('\n')

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

def teste():
    texto = ["host2a", "host3b", "host4c", "host5d"]
    
    for i in texto:
        print(Host.extrair_ip_hosts(i))

if __name__ == "__main__":
    habilitar_ip_forward_em_roteadores()
    teste_de_ping_hosts()
    teste_de_ping_roteadores()
    # teste()
    print("Teste de ping concluído.")