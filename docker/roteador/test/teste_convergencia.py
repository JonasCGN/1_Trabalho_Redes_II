import sys
import os
import subprocess
import time
import csv

QTD_TESTE = 4

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from classes.manipulacao import Manipulacao

def teste_de_ping():
    roteadores = Manipulacao.roteadores_encontrados()
    qtd_roteadores = len(roteadores)
    
    inicio = time.time()
    
    retry_count = 0
    converged = False
    
    while not converged:
        line_counts = {}
        success = True
        
        for router in roteadores:
            try:
                comando = f"docker exec {router} route -n"
                resultado = subprocess.run(comando, shell=True, check=True, text=True, capture_output=True)
                qtd_linha = len(Manipulacao.extrair_linhas(resultado.stdout))
                line_counts[router] = qtd_linha
            except subprocess.CalledProcessError:
                success = False
                break
        
        if success and line_counts:
            if len(set(line_counts.values())) == 1 and list(line_counts.values())[0] == (qtd_roteadores + 4):
                converged = True
            else:
                retry_count += 1
        else:
            retry_count += 1
            time.sleep(1)

    fim = time.time()
    
    return fim - inicio

def teste_de_convergencia_roteadores():
    topologia = "anel"
    qtd_host = 2
    
    lista_roteadores = [num*5 for num in range(1, QTD_TESTE+1)]
    print(f"Quantidade de roteadores: {lista_roteadores}")
    resultados = []
    for qtd_roteador in lista_roteadores:
        qtd_roteadores = qtd_roteador
        
        args = f"QTD_ROUTER={qtd_roteadores} QTD_HOST={qtd_host} TOPOLOGIA={topologia}"

        os.system(f"make gerar_compose -B criar_topologia {args}")
        retorno = os.system("docker-compose up --build -d")
        
        if retorno != 0:
            print("Erro ao executar o docker.")
            break
        else:
        
            tempo = teste_de_ping()
            
            os.system("docker-compose down")
            
            print(f"Tempo de execução do comando make: {tempo:.2f} segundos")

            resultados.append([qtd_roteadores, qtd_host, topologia, tempo])

    if resultados:
        with open('resultado_convergencia.csv', mode='w', newline='', encoding='utf-8') as arquivo_csv:
            escritor_csv = csv.writer(arquivo_csv)
            escritor_csv.writerow(["Quantidade de Roteadores", "Quantidade de Hosts", "Topologia", "Tempo de Execução (s)"])
            escritor_csv.writerows(resultados)
            
if __name__ == "__main__":
    # resultado = teste_de_ping()
    # print(f"Tempo de execução do comando make: {resultado:.2f} segundos")
    teste_de_convergencia_roteadores()
    
    print("Teste de convergência concluído.")