# Projeto CODESYS – Simulação de Vazão
### Objetivo

Este projeto tem como finalidade simular medições de vazão em duas saídas distintas de uma Estação de Tratamento de Água (ETA), visando a validação de um sistema de monitoramento baseado em Internet das Coisas (IoT). Ele substitui a necessidade de sensores físicos, oferecendo uma fonte confiável de dados para desenvolvimento, integração e testes de sistemas conectados via OPC UA.
### Funcionalidades

    Emulação de vazão para duas saídas (ETA1 e ETA2)

    Oscilação contínua entre limites mínimos e máximos predefinidos

    Atualização periódica dos dados com temporizador interno

    Disponibilização das variáveis via servidor OPC UA

    Configuração de segurança com autenticação por usuário e senha

### Detalhes Técnicos

    Variáveis simuladas: vazao_saida1, vazao_saida2, horario_leitura

    Organização: Variáveis declaradas em GVL (Global Variable List)

    Protocolo de acesso: OPC UA com autenticação e criptografia

    Intervalo de atualização: A cada 10 segundos (configurável)

    Plataforma: Programado no ambiente CODESYS, compatível com CLPs que suportam OPC UA (ex: Eaton XC-204)

### Lógica de Simulação (POU)

A lógica principal foi implementada na Program Organization Unit (POU), utilizando estrutura cíclica controlada por um temporizador do tipo TON.
#### Funcionamento

    O temporizador define o intervalo entre atualizações das variáveis.

    As variáveis de vazão aumentam ou diminuem dentro dos limites definidos (60.0 a 75.0).

    O sentido da simulação é invertido automaticamente ao atingir os limites, garantindo oscilação contínua.

    A variável horario_leitura armazena a marca temporal da última simulação.

    Todas as variáveis são declaradas globalmente e expostas ao servidor OPC UA para acesso remoto.

Exemplo da lógica:
```
IF direcao_saida1 THEN
    vazao_saida1 := vazao_saida1 + incremento_saida;
    IF vazao_saida1 > 75.0 THEN
        direcao_saida1 := FALSE;
    END_IF;
ELSE
    vazao_saida1 := vazao_saida1 - incremento_saida;
    IF vazao_saida1 < 60.0 THEN
        direcao_saida1 := TRUE;
    END_IF;
END_IF;
```
Essa abordagem garante dinamismo nos dados e simula flutuações reais de processo, permitindo testes mais realistas dos sistemas de aquisição.
### Configurações OPC UA

    As variáveis simuladas são expostas por meio da configuração de símbolos no CODESYS.

    A política de segurança Basic256Sha256 foi ativada para criptografia de dados.

    A autenticação do cliente OPC UA é feita por meio de usuário e senha cadastrados diretamente no CLP.

    Apenas variáveis selecionadas são tornadas públicas, mantendo a segurança e controle sobre o acesso externo.

### Escalabilidade e Portabilidade

    A estrutura da POU permite fácil adição de novas variáveis simuladas (como nível, pressão, temperatura).

    O projeto é portátil para qualquer CLP compatível com CODESYS e OPC UA, facilitando o reaproveitamento em outros contextos industriais.

* A simulação de sinais em CODESYS permite validar o fluxo completo — da coleta à visualização — com alto grau de controle e reprodutibilidade.

### Instruções de Uso
1. Importar o Projeto no CODESYS

    Abra o CODESYS.

    Selecione "Abrir Projeto" e carregue o arquivo .project.

    Certifique-se de que o dispositivo configurado corresponde ao modelo de CLP utilizado (ex: Eaton XC-204).

    Compile o projeto (Ctrl + F11).

2. Carregar para o CLP

    Conecte o CLP à sua rede local.

    Vá em "Online" > "Login" para conectar ao CLP.

    Clique em "Carregar" para transferir o projeto.

    Execute o programa clicando em "Run" ou F5.

3. Verificar a Simulação

    No ambiente CODESYS, vá até a POU e ative a visualização de variáveis.

    Confirme a oscilação dos valores de vazao_saida1 e vazao_saida2 a cada 10 segundos.

    O horário de leitura também será atualizado.

4. Configurar Cliente OPC UA

    Use um cliente OPC UA (como UA Expert ou script Python) para se conectar ao IP do CLP.

    Porta padrão: 4840

    Caminho do endpoint: opc.tcp://<IP_DO_CLP>:4840

    Insira o usuário e senha configurados no servidor OPC UA do CODESYS.

    Navegue até as variáveis publicadas e inicie a leitura em tempo real.