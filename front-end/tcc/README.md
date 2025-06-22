# Frontend - Sistema de Monitoramento de Vazão

O frontend faz parte do sistema IoT desenvolvido para o monitoramento de parâmetros ambientais em Estações de Tratamento de Água (ETA), com foco na visualização de dados de vazão em tempo real. O projeto foi desenvolvido em Angular versão 15.2.11 e consome uma API backend para apresentar os dados em dashboards interativos.
### Funcionalidades

    Visualização gráfica das leituras de vazão (ETA1 e ETA2)

    Filtros por período e tipo de sensor

    Exportação de dados em PDF, Excel e imagem

    Interface responsiva e de fácil navegação

    Comunicação com a API backend via HTTP (FastAPI)

## Acesso ao Sistema

A aplicação está disponível publicamente no seguinte endereço:

http://maria-tcc-monitoramento-ambiental.duckdns.org/login

Credenciais de Acesso:

* Usuário: convidado

* Senha: pesquisa123

* O acesso está limitado a funcionalidades de consulta e geração de relatórios para fins de demonstração e validação acadêmica.

### Instalação

1. Clone este repositório: git clone https://github.com/mariaedk/tcc.git

2. Instale as dependências:
```npm install``` 

3. Execute o servidor de desenvolvimento:
```ng serve```

4. Acesse o sistema via navegador:
```http://localhost:4200/```

### Requisitos

    Node.js v16+

    Angular CLI v15.2.11

    API Backend em funcionamento (FastAPI)