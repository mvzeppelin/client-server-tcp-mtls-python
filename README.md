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

## Cria a CA
```
# vim ca.cnf
[ req ]
prompt = no
distinguished_name = dn
x509_extensions = v3_ca

[ dn ]
CN = MyTestCA

[ v3_ca ]
basicConstraints = critical, CA:TRUE
keyUsage = critical, keyCertSign, cRLSign
subjectKeyIdentifier = hash

# openssl genrsa -out ca.key 4096

# openssl req -x509 \
  -new \
  -nodes \
  -key ca.key \
  -sha256 \
  -days 3650 \
  -out ca.crt \
  -config ca.cnf
```

## Gera o certificado do servidor
```
# vim server.cnf
[ req ]
default_bits       = 2048
prompt             = no
default_md         = sha256
distinguished_name = dn
req_extensions     = req_ext

[ dn ]
CN = 127.0.0.1

[ req_ext ]
subjectAltName = @alt_names

[ alt_names ]
IP.1 = 127.0.0.1
DNS.1 = server
DNS.2 = localhost

# openssl genrsa -out server.key 2048

# openssl req -new -key server.key -out server.csr -config server.cnf

# openssl x509 -req -in server.csr \
  -CA ca.crt -CAkey ca.key -CAcreateserial \
  -out server.crt -days 365 -sha256 \
  -extensions req_ext -extfile server.cnf
```

## Gera o certificado do cliente
```
# openssl genrsa -out client.key 2048

# openssl req -new -key client.key -out client.csr

# openssl x509 -req \
  -in client.csr \
  -CA ca.crt \
  -CAkey ca.key \
  -CAcreateserial \
  -out client.crt \
  -days 365 \
  -sha256

```
