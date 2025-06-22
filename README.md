# Sistema de Monitoramento de Vazão com IoT

Este projeto tem como objetivo o desenvolvimento de um sistema inteligente para monitoramento de parâmetros ambientais, com foco na vazão de Estações de Tratamento de Água (ETA). Os dados são coletados, processados e disponibilizados em tempo real por meio de um dashboard web.

## Objetivo do Projeto

Este sistema foi desenvolvido como Trabalho de Conclusão de Curso em Ciência da Computação, com a finalidade de aplicar conceitos de IoT, computação em nuvem e automação para atender demandas reais de monitoramento ambiental e apoio à gestão hídrica.

## Arquitetura do Sistema

A arquitetura é composta por múltiplos módulos integrados:

* CLP (Eaton XC204): Simula sinais analógicos e digitais de sensores e disponibiliza os dados via protocolo OPC UA.

* Raspberry Pi (Model 4B): Atua como gateway, realizando a leitura via OPC UA e publicação dos dados para o broker MQTT.

* Broker MQTT (Mosquitto na AWS): Realiza a comunicação entre RP e o backend.

* API Backend (FastAPI): Responsável pelo recebimento, validação, armazenamento e disponibilização dos dados.

* Banco de Dados (MariaDB): Armazena de forma estruturada todas as medições recebidas.

* Frontend Web (Angular): Dashboard para visualização de gráficos, filtros e geração de relatórios.

## Fluxo de Dados

CLP → OPC UA

O CLP simula os dados dos sensores e os expõe via servidor OPC UA.

Raspberry Pi → Leitura OPC UA

Coleta os dados em intervalos programados, armazena localmente e organiza os lotes de envio.

Raspberry Pi → MQTT (AWS)

Publica os dados em tempo real ou em batch para o broker Mosquitto na nuvem.

Broker MQTT → API FastAPI

A API consome os dados publicados, realiza validações e os insere no banco de dados.

API → Dashboard Angular

O frontend acessa a API para exibir os dados, com filtros e relatórios exportáveis.

## Tecnologias Utilizadas

* Backend: Python, FastAPI, SQLAlchemy, Alembic, JWT Auth

* Frontend: Angular, ApexCharts

* IoT: Raspberry Pi, OPC UA, MQTT (paho-mqtt, Mosquitto)

* Banco de Dados: MariaDB (relacional)

* Infraestrutura nuvem: AWS EC2 

* CLP: Eaton XC204

## Funcionalidades Principais
```
    Coleta contínua de dados de vazão em ETA

    Armazenamento seguro e estruturado em banco relacional

    Visualização gráfica em tempo real com ApexCharts

    Geração de relatórios em PDF, Excel e PNG

    Filtros por período, sensores e tipos de medição

    Identificação de anomalias e valores fora de faixa
```
## Acesso ao Sistema

A interface de visualização está disponível online:

* Acessar Dashboard
Credenciais de Acesso

    Usuário: convidado

    Senha: pesquisa123

    A conta possui permissões limitadas para consulta e geração de relatórios.