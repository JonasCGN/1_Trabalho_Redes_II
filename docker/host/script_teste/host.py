import subprocess

class Host:
    
    def __init__(self):
        pass
    
    @staticmethod
    def formatar_mensagem(mensagem, cor_rgb):
        r, g, b = cor_rgb
        return f"\033[38;2;{r};{g};{b}m{mensagem}\033[0m"  # Adds custom RGB color to the message
    
    @staticmethod
    def formatar_sucesso(mensagem):
        return Host.formatar_mensagem(mensagem, (0, 255, 0))  # Green color for success
    
    @staticmethod
    def formatar_erro(mensagem):
        return Host.formatar_mensagem(mensagem, (255, 0, 0))  # Red color for error
    
    @staticmethod
    def roteadores_encontrados():
        comando = "docker ps --filter name=roteador --format '{{.Names}}'"
        result = subprocess.run(comando, shell=True, check=True, text=True, capture_output=True)
        roteadores = [r.strip("'") for r in result.stdout.split('\n') if r]
        return roteadores

    @staticmethod
    def extrair_ip_roteadores(roteador_name):
        return int(roteador_name.split('roteador')[-1]) - 1
    
    @staticmethod
    def extrair_linhas(resultado):
        linhas = resultado.split('\n')
        return linhas
    
    @staticmethod
    def traduzir_caminho(roteador,caminho):
        hops = Host.extrair_linhas(caminho)
        traducao = []
        traducao.append(roteador)
        for hop in hops:
            if 'roteador' in hop:
                nome_roteador = hop.split()[1].split('.')[0]
                traducao.append(nome_roteador)
            elif hop:
                numero_roteador = int(hop.split('(')[1].split(')')[0].split('.')[2]) + 1
                traducao.append(f'roteador{numero_roteador}',)
                
        return ' -> '.join(traducao)
    
    @staticmethod
    def host_encontrados():
        comando = "docker ps --filter name=host --format '{{.Names}}'"
        result = subprocess.run(comando, shell=True, check=True, text=True, capture_output=True)
        hosts = [h.strip("'") for h in result.stdout.split('\n') if h]
        return hosts
    
    @staticmethod
    def extrair_ip_hosts(host_name):
        base_ip = int(''.join(filter(str.isdigit, host_name.split('host')[-1][:-1])))
        suffix = host_name[-1].lower()
        offset = ord(suffix) - ord('a')
        return f"{base_ip - 1}.{10 + offset}"