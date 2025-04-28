# Projeto de Simulação de Rede de Computadores

Este projeto tem como objetivo:

- Desenvolver uma simulação de uma rede de computadores composta por hosts e roteadores.
- Utilizar Python e Docker para implementar a simulação.
- Implementar o algoritmo de roteamento por estado de enlace (Link State Routing Algorithm) nos roteadores.

## Pré-requisitos

Certifique-se de ter o Docker e o Make instalado em sua máquina antes de prosseguir.

## Como executar

Primeiramente você deve ter o make instalado na sua máquina:

`pip install make`

Para executar o projeto, basta rodar o seguinte comando no terminal:

`make`

## Protocolo Utilizado

O protocolo utilizado para a comunicação entre os hosts e roteadores é o UDP (User Datagram Protocol). O UDP é um protocolo de transporte que permite a troca de datagramas entre dispositivos em uma rede. Ele é mais leve e rápido do que o TCP (Transmission Control Protocol), mas não garante a entrega dos pacotes, tornando-o adequado para aplicações onde a velocidade é mais importante do que a confiabilidade.

O UDP é amplamente utilizado em aplicações de streaming de áudio e vídeo, jogos online e outras aplicações em tempo real onde a latência é crítica.

### Justificativa do uso do UDP

O uso do UDP neste projeto é justificado pela necessidade de uma comunicação rápida e eficiente entre os hosts e roteadores. O protocolo UDP permite a troca de mensagens sem a sobrecarga de controle de conexão, o que é ideal para simulações onde a latência deve ser minimizada. Além disso, o UDP é mais simples de implementar e configurar em comparação com o TCP, tornando-o uma escolha adequada para este projeto.

## Topologia Construída

A topologia construída para a simulação é uma rede de computadores composta por n hosts e n roteadores. Os hosts estão conectados aos roteadores, que por sua vez estão interconectados entre si dependendo do número de roteadores definidos na configuração e da topologia escolhida, pois podemos gerar as seguintes topologias:

- Topologia em estrela
- Topologia em anel
- Topologia totalmente conectada
- Topologia em árvore
- Topologia em linha

As topologias são escolhidas aleatoriamente no inicio da execução do projeto, garantindo uma variedade de cenários para a simulação. Cada topologia tem suas próprias características e desafios, permitindo uma análise mais abrangente do desempenho da rede.

### Como a topologia é construída

A topologia é construída através da definição de n hosts e n roteadores, onde os hosts se conectam aos roteadores. A configuração da topologia é realizada aleatoriamente, permitindo a simulação de diferentes cenários de rede. Dependendo da topologia escolhida, as conexões entre os roteadores podem variar, proporcionando uma análise detalhada do desempenho da rede em diferentes condições.

## Observações

Este projeto foi desenvolvido como parte do curso de Redes II e visa demonstrar conceitos fundamentais de roteamento e simulação de redes.
