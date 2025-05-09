import socket

HOST = '0.0.0.0'
PORT = 8089

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        data = conn.recv(1024)
        print("HTTP Request:\n", data.decode())  # 明文输出 HTTP 请求