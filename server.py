import socket, ssl, threading, sys

HOST = "0.0.0.0"
PORT = 443

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile="certs/server.crt", keyfile="certs/server.key")
context.load_verify_locations(cafile="certs/ca.crt")
context.verify_mode = ssl.CERT_REQUIRED   # 🔐 exige cert do cliente

server = socket.socket()
server.bind((HOST, PORT))
server.listen(1)

print("[+] Aguardando conexão mTLS...")
conn, addr = server.accept()

try:
    tls_conn = context.wrap_socket(conn, server_side=True)
    print("[+] Cliente autenticado com sucesso")
    print("    Subject:", tls_conn.getpeercert()["subject"])
except ssl.SSLError as e:
    print("[-] Falha TLS:", e)
    conn.close()
    exit(1)

def recv_data():
    while True:
        data = tls_conn.recv(4096)
        if not data:
            break
        sys.stdout.buffer.write(data)
        sys.stdout.flush()

def send_data():
    while True:
        data = sys.stdin.buffer.read(1)
        if not data:
            break
        tls_conn.sendall(data)

threading.Thread(target=recv_data, daemon=True).start()
threading.Thread(target=send_data, daemon=True).start()

threading.Event().wait()
