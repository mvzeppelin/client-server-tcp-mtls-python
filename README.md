# Cliente/Servidor Python com mTLS

Execução remota de comandos via TLS com autenticação mútua por certificado (Linux > Linux)

## Arquitetura
```
[ Servidor Python ]
        |
        |  TLS + mTLS
        |
[ Cliente Python ]
        |
   Execução de shell
```

## Estrutura de diretórios
```
client_server/
├── certs/
│   ├── ca.crt
│   ├── ca.key
│   ├── ca.cnf
│   ├── server.crt
│   ├── server.csr
│   ├── server.key
│   ├── client.crt
│   ├── client.csr
│   └── client.key
├── server.py
└── client.py
```
