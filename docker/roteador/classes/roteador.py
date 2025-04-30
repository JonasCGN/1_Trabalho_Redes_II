import threading
import os
from classes.gerenciar_vizinhos import VizinhosManager
from classes.gerenciar_lsa import LSAManager
from classes.atualiza_rota import AtualizadorDeRotas
from classes.gerenciador_rota import GerenciadorDeRotas

class RoteadorApp:
    def __init__(self):
        self.lsdb = {}
        self.event = threading.Event()

        self.vizinhos_manager = VizinhosManager()
        self.lsa_manager = LSAManager(self.vizinhos_manager)
        self.gerenciador_de_rotas = GerenciadorDeRotas(self.lsdb, self.vizinhos_manager.vizinhos_inativos)
        self.rota_manager = AtualizadorDeRotas(self.gerenciador_de_rotas)

        self.threads = []

    def atualizar_tabela(self):
        while not self.event.is_set():
            if not self.vizinhos_manager.verifica_roteadores_ativos(self.lsdb):
                self.rota_manager.recalcular_rotas(self.vizinhos_manager.vizinhos_inativos)
            self.event.wait(0.1)

    def monitorar_vizinhos(self):
        while not self.event.is_set():
            self.vizinhos_manager.atualiza_status_vizinhos()
            self.rota_manager.recalcular_rotas(self.vizinhos_manager.vizinhos_inativos)
            self.event.wait(0.5)

    def iniciar_threads(self):
        self.threads = [
            threading.Thread(target=self.lsa_manager.enviar_lsa, args=(self.event,)),
            threading.Thread(target=self.lsa_manager.receber_lsa, args=(self.lsdb, self.event)),
            threading.Thread(target=self.atualizar_tabela),
            threading.Thread(target=self.monitorar_vizinhos)
        ]

        for t in self.threads:
            t.daemon = True
            t.start()

        self.event.wait()

    def parar(self):
        self.event.set()
        for t in self.threads:
            t.join()
            
if __name__ == "__main__":
    roteador_app = RoteadorApp()
    