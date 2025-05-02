import subprocess
import matplotlib.pyplot as plt
import psutil
from time import sleep

pares = [
    ("host1a", "host30a", "172.21.29.10"),
    # ("host2a", "host4b", "172.21.3.11"),
    # ("host3a", "host5b", "172.21.4.11"),
    # adicione mais se quiser
]

QTD_PACOTES = 5
latencias_resultado = {}
throughput_resultado = {}
cpu_usage = {}
mem_usage = {}

def medir_recursos():
    """Retorna uso de CPU (%) e memória (%) do host onde o script roda."""
    cpu = psutil.cpu_percent(interval=0.5)
    mem = psutil.virtual_memory().percent
    return cpu, mem

def executar_ping(origem, destino_ip, label):
    print(f"⏳ PING: {origem} -> {destino_ip}")
    resultado = subprocess.run(
        f"docker exec {origem} ping -c {QTD_PACOTES} {destino_ip}",
        shell=True, capture_output=True, text=True
    )
    latencias = [
        float(line.split("time=")[1].split(" ms")[0])
        for line in resultado.stdout.splitlines() if "time=" in line
    ]
    latencias_resultado[label] = latencias
    cpu, mem = medir_recursos()
    cpu_usage[label] = cpu
    mem_usage[label] = mem

def executar_iperf3(origem, destino, destino_ip, label):
    print(f"🚀 IPERF3: {origem} -> {destino_ip}")
    server = subprocess.Popen(f"docker exec {destino} iperf3 -s", shell=True)
    sleep(2)
    resultado = subprocess.run(
        f"docker exec {origem} iperf3 -c {destino_ip} -t 10",
        shell=True, capture_output=True, text=True
    )
    server.terminate()
    valor, unidade = 0, "Mbits/sec"
    for line in resultado.stdout.splitlines():
        if "receiver" in line:
            parts = line.split()
            valor = float(parts[6])
            unidade = parts[7]
            break
    throughput_resultado[label] = (valor, unidade)
    cpu, mem = medir_recursos()
    cpu_usage[f"{label}_iperf"] = cpu
    mem_usage[f"{label}_iperf"] = mem

def plotar_latencias():
    for label, lat in latencias_resultado.items():
        safe = label.replace("->", "_")
        plt.figure(figsize=(8,3))
        x = list(range(1, len(lat)+1))
        plt.plot(x, lat, marker="o", linestyle="-")
        # Anota cada ponto
        for xi, yi in zip(x, lat):
            plt.annotate(f"{yi:.3f}", (xi, yi), textcoords="offset points", xytext=(0,5), ha="center")
        plt.title(f"Latência: {label}")
        plt.xlabel("Pacote #")
        plt.ylabel("ms")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(f"./files/latencia_{safe}.png")
        plt.close()

def plotar_throughput():
    labels = list(throughput_resultado.keys())
    valores = [throughput_resultado[l][0] for l in labels]
    plt.figure(figsize=(6,4))
    plt.bar(labels, valores)
    plt.title("Throughput comparativo")
    plt.ylabel("Mbits/sec")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig("./files/throughput_comparativo.png")
    plt.close()

def plotar_recursos():
    # CPU
    labels = list(cpu_usage.keys())
    valores_cpu = [cpu_usage[l] for l in labels]
    plt.figure(figsize=(8,3))
    plt.bar(labels, valores_cpu)
    plt.title("Uso de CPU (%) por teste")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig("./files/cpu_usage.png")
    plt.close()
    # Memória
    valores_mem = [mem_usage[l] for l in labels]
    plt.figure(figsize=(8,3))
    plt.bar(labels, valores_mem)
    plt.title("Uso de Memória (%) por teste")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig("./files/mem_usage.png")
    plt.close()

def executar_todos_os_testes():
    for origem, destino, ip in pares:
        label = f"{origem}->{destino}"
        executar_ping(origem, ip, label)
        executar_iperf3(origem, destino, ip, label)
    plotar_latencias()
    plotar_throughput()
    plotar_recursos()
    print("✅ Todos os gráficos gerados.")

if __name__ == "__main__":
    executar_todos_os_testes()
    print("✅ Testes de estresse concluídos.")