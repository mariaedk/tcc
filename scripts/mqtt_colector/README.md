# Coletor MQTT para API FastAPI

Este serviço consome dados de medições publicados via MQTT (como por exemplo de um Raspberry Pi conectado a um CLP) e os envia para uma API FastAPI para persistência e análise.

## Funcionalidade

- Escuta tópicos MQTT configurados.
- Faz autenticação JWT na API FastAPI.
- Publica os dados recebidos no endpoint de coleta da API.
- Mantém logs detalhados das operações realizadas.
- Funciona como um serviço em segundo plano no Linux (Systemd).



