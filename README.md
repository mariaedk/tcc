# Sistema de Monitoramento de Vazão com IoT

Este projeto tem como objetivo desenvolver um sistema de monitoramento de parâmetros ambientais, como vazão de ETA, utilizando tecnologias de automação industrial e IoT. Os dados coletados são enviados para a nuvem, onde ficam armazenados e podem ser acessados por meio de um dashboard.

## Arquitetura do Sistema

O sistema é composto por:

- Sensores + CLP (Eaton XC204): Realiza a coleta dos sinais analógicos e digitais dos sensores e disponibiliza os dados via protocolo OPC UA.
- Raspberry Pi: Faz a leitura dos dados do CLP via OPC UA, processa, armazena e publica no broker MQTT.
- Broker MQTT (AWS - EC2 com Mosquitto): Responsável pela transmissão dos dados em tempo real entre os dispositivos e o backend.
- Backend (API FastAPI): API responsável por receber, armazenar e disponibilizar os dados.
- Banco de Dados (MariaDB): Armazena os dados coletados e processados.
- Frontend (Angular): Dashboard para visualização dos dados, gráficos e geração de relatórios PDF e Excel.

### Fluxo de Dados

1. CLP (OPC UA)
   O CLP emula os dados dos sensores e os disponibiliza via protocolo OPC UA.

2. CLP -> Raspberry Pi (OPC UA)
   O Raspberry lê os dados periodicamente, processa e armazena localmente em buffer.

3. Raspberry Pi -> Broker MQTT (AWS)
   O Raspberry publica os dados em tempo real ou em lote no broker MQTT hospedado na AWS.

4. Broker MQTT -> API FastAPI
   A API consome os dados do MQTT, valida, armazena no banco de dados e disponibiliza para o dashboard.

5. API -> Frontend Angular
   O usuário acessa os dados via dashboard, podendo visualizar gráficos, aplicar filtros e gerar relatórios.

### Tecnologias Utilizadas

- Backend: Python, FastAPI, JWT Auth, MariaDB
- Frontend: Angular, ApexCharts
- IoT: Raspberry Pi, OPC UA, MQTT (Mosquitto)
- CLP: Eaton XC204 (OPC UA)
- Infraestrutura: AWS EC2 (Broker MQTT + API + DB)

### Funcionalidades Principais

- Coleta de dados de vazão de ETA em tempo real
- Armazenamento dos dados
- Visualização em gráficos no dashboard
- Geração de relatórios em PDF e Excel
- Detecção de anomalias na vazão de água
- Filtros avançados por período, sensores e tipo de dados

### Objetivo do TCC

Este sistema foi desenvolvido como Trabalho de Conclusão de Curso (TCC) do curso de Ciência da Computação, visando aplicar conceitos de IoT e automação para proporcionar monitoramento ambiental.
