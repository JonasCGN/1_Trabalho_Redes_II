class Mensagem:
    
    def __init__(self):
        pass
    
    @staticmethod
    def formatar_mensagem(mensagem, cor_rgb):
        r, g, b = cor_rgb
        return f"\033[38;2;{r};{g};{b}m{mensagem}\033[0m"  # Adds custom RGB color to the message
    
    @staticmethod
    def formatar_sucesso(mensagem):
        return Mensagem.formatar_mensagem(mensagem, (0, 255, 0))  # Green color for success
    
    @staticmethod
    def formatar_erro(mensagem):
        return Mensagem.formatar_mensagem(mensagem, (255, 0, 0))  # Red color for error