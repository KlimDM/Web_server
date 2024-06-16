import socket
from RequestHandler import RequestHandler

HOST = ""
PORT = 80

if __name__ == "__main__":
    with socket.socket() as sock:
        try:
            sock.bind(('', PORT))
            print(f"Using port {PORT}")
        except OSError:
            sock.bind(('', 8080))
            print("Using port 8080")
        sock.listen(5)
        while True:
            conn, addr = sock.accept()
            print(f'Подключено: {addr}')
            requestHandler = RequestHandler(conn)
            requestHandler.start()
            requestHandler.join()
