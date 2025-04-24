import subprocess

class Roteador:
    
    def __init__(self):
        pass
    
    @staticmethod
    def formatar_mensagem(mensagem, cor_rgb):
        r, g, b = cor_rgb
        return f"\033[38;2;{r};{g};{b}m{mensagem}\033[0m"  # Adds custom RGB color to the message
    
    @staticmethod
    def formatar_sucesso(mensagem):
        return Roteador.formatar_mensagem(mensagem, (0, 255, 0))  # Green color for success
    
    @staticmethod
    def formatar_erro(mensagem):
        return Roteador.formatar_mensagem(mensagem, (255, 0, 0))  # Red color for error
    
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
        hops = Roteador.extrair_linhas(caminho)
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