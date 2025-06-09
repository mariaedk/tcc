# Projeto CODESYS – Simulação de Vazão

## Objetivo
Este projeto foi desenvolvido com o objetivo de simular medições de vazão em duas saídas distintas, representando o funcionamento de Estações de Tratamento de Água (ETAs), para fins de validação de um protótipo de monitoramento via IoT.

O CLP é programado no ambiente CODESYS e utiliza uma lógica cíclica com temporizador para emular valores realistas de vazão. Os valores simulados são disponibilizados via protocolo OPC UA, permitindo que um cliente externo, como um Raspberry Pi, acesse e colete essas informações.

As variáveis de vazão (vazao_saida1, vazao_saida2) são declaradas em uma Global Variable List (GVL) e expostas ao servidor OPC UA. A simulação alterna os valores entre limites mínimos e máximos definidos, simulando oscilações normais de operação.

O projeto está configurado com autenticação por usuário e senha para acesso via OPC UA, seguindo práticas básicas de segurança.