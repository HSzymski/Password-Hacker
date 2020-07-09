import socket

HOST = '127.0.0.1'
PORT = 9090
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()
    with conn:
        while True:
            data = conn.recv(1024)
            if data and data.decode('utf-8') != 'draGON':
                conn.send(b"Wrong password!")
            elif data:
                conn.send(b"Connection success!")
            elif not data:
                break
