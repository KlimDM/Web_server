import datetime
import threading
import os


class RequestHandler(threading.Thread):
    DIRECTORY = "./resources"

    def __init__(self, conn):
        super().__init__()
        self.conn = conn

    def run(self):
        try:
            self.handle_request()
        finally:
            self.conn.close()

    def handle_request(self):
        data = self.conn.recv(8192).decode("utf-8")
        print(f"Полученный запрос: '{data}'")
        try:
            if data:
                method, resource, version = data.split('\n')[0].split(' ')
                if resource == "/":
                    resource = "/index.html"
                filename = os.path.join(self.DIRECTORY, resource[1:])
                print(f"Запрошенный ресурс: {filename}")
                if os.path.exists(filename):
                    with open(filename, "rb") as f:
                        content = f.read()
                        self.conn.sendall(f"HTTP/1.1 200 OK\n".encode("utf-8"))
                        self.conn.sendall(f"Date: {datetime.datetime.now()}".encode("utf-8"))
                        self.conn.sendall(
                            f"Content-Type: {RequestHandler.get_content_type(filename)}\n".encode("utf-8"))
                        self.conn.sendall(f"Content-length: {len(content)}\n".encode("utf-8"))
                        self.conn.sendall(b"\n")
                        self.conn.sendall(content)
                else:
                    self.conn.send(b"HTTP/1.1 404 Not Found\n\n")
                    self.conn.sendall(b"<h1>404 Not Found</h1>")
        except Exception as e:
            print(f'Ошибка: {e}')
            self.conn.send(b"HTTP/1.1 500 Internal Server Error\n\n")
            self.conn.send(b"<h1>500 Internal Server Error</h1>")

    @staticmethod
    def get_content_type(filename: str) -> str:
        if filename.endswith(".html"):
            return "text/html"
        if filename.endswith(".css"):
            return "text/css"
        if filename.endswith(".js"):
            return "text/javascript"
        if filename.endswith(".html"):
            return "text/html"
        else:
            return "application/octet-stream"
