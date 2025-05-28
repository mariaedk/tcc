# Leitor OPC UA para MQTT (Batch por Hora)

Este serviço conecta-se a um CLP via protocolo OPC UA, realiza leituras dos sensores a cada 3 minutos e publica os dados em batch no broker MQTT ao final de cada hora cheia.

## Funcionalidade

- Leitura dos sensores do CLP via OPC UA.
- Coleta dados a cada 3 minutos.
- Ao virar a hora, envia um batch (lista) de todas as leituras daquela hora para o tópico MQTT.
- Realiza reconexões automáticas ao broker MQTT e ao CLP em caso de falhas.
- Gera logs de execução e erros.