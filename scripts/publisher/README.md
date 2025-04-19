# Publicador OPC UA → MQTT - TCC

Este projeto roda no Raspberry Pi e:

- Lê variáveis do CLP via OPC UA
- Publica os dados em formato JSON no broker MQTT da AWS
- Funciona continuamente via systemd (roda no boot)

---

## 📁 Estrutura dos arquivos

```
tcc-publicador/
├── publicador.py            # Script principal (leitura + publicação)
├── config.py                # Configurações (IP, tópico, NodeIds)
├── tcc_publicador.service   # Serviço systemd
├── install_service.sh       # Script para reinstalar o serviço
├── crontab_tcc.txt          # Entrada de backup no boot via cron
├── log.txt                  # Log de execução
├── error.log                # Log de erros
└── requirements.txt         # Dependências Python
```

---

## ▶️ Como rodar manualmente (modo teste)

```bash
python3 publicador.py
```

---

## ⚙️ Como instalar o serviço systemd (etapa completa)

1. Copie o arquivo `tcc_publicador.service` para o diretório do systemd, por exemplo:

```bash
sudo cp /home/mariaed/dev/tcc/publish/tcc_publicador.service /etc/systemd/system/
```

2. Recarregue o systemd para detectar o novo serviço:

```bash
sudo systemctl daemon-reload
sudo systemctl daemon-reexec
```

3. Habilite o serviço para iniciar automaticamente no boot:

```bash
sudo systemctl enable tcc_publicador
```

4. Inicie o serviço:

```bash
sudo systemctl start tcc_publicador
```

5. Verifique o status:

```bash
sudo systemctl status tcc_publicador
```

---

## 🧪 Como testar se o serviço está rodando

Você pode monitorar os logs:

```bash
journalctl -u tcc_publicador -f
```

Ou verificar os arquivos:

```bash
cat log.txt
cat error.log
```

---

## 🛠️ Instalação automática (opcional)

Execute o script de instalação automática:

```bash
sudo bash install_service.sh
```

---

## 🕓 Alternativa com cron (backup em caso de falha do systemd)

Você pode usar `crontab_tcc.txt` como fallback:

```bash
crontab crontab_tcc.txt
```

Isso garante que o script será executado mesmo que o serviço systemd falhe ou seja desativado.

---

## 💡 Observações

- Os dados são publicados no tópico MQTT: `tcc/monitoramento`
- O log de execução padrão vai para `log.txt`, e erros vão para `error.log`
- O serviço roda como usuário `mariaed` com base no caminho do projeto

---