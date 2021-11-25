import socket


sock = socket.socket()
sock.bind(('127.0.0.1', 8888))
sock.listen(socket.SOMAXCONN)

response = b'ok\npalm.cpu 1.0 12\neardrum.cpu 2.0 123\n\n'

conn, addr = sock.accept()
while True:
    data = conn.recv(1024)
    if not data:
        break
    print(data.decode())
    conn.send(response)

conn.close()
sock.close()
