import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('resultado_convergencia.csv')

routers = df['Quantidade de Roteadores'].values 
execution_times = df['Tempo de Execução (s)'].values 

plt.figure(figsize=(10, 7))
plt.plot(routers, execution_times, marker='o', linestyle='-', color='b', linewidth=2, markersize=8)

# Add text labels above each point
for i, txt in enumerate(execution_times):
    plt.annotate(f'{txt:.2f}s', 
                 (routers[i], execution_times[i]),
                 textcoords="offset points", 
                 xytext=(0, 10),   # Offset text 10 points above
                 ha='center',      # Horizontal alignment
                 fontsize=9)       # Text size

plt.xlabel('Quantidade de Roteadores')
plt.ylabel('Tempo de Execução (s)')
plt.title('Relação entre Quantidade de Roteadores e Tempo de Execução')
plt.grid(True)
plt.xticks(routers)  # Set x-ticks to match exactly the router quantities

plt.tight_layout()
plt.savefig('grafico_roteadores_tempo.png')
plt.show()
