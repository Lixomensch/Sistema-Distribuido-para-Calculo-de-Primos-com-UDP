import json
import socket
import threading


def find_primes(start, end):
    """Retorna uma lista de números primos no intervalo [start, end]."""
    primes = []
    for num in range(start, end + 1):
        if num > 1:
            for i in range(2, int(num ** 0.5) + 1):
                if num % i == 0:
                    break
            else:
                primes.append(num)
    return primes


class PrimeServer:
    def __init__(self, host='localhost',
                 port=9999,
                 total_range=(1, 100000),
                 chunk_size=5000):
        self.host = host
        self.port = port
        self.total_range = total_range
        self.chunk_size = chunk_size
        self.prime_numbers = []
        self.current_start = total_range[0]
        self.lock = threading.Lock()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind((self.host, self.port))
        print(f"Servidor iniciado em {self.host}:{self.port}")

    def get_next_task(self):
        with self.lock:
            if self.current_start > self.total_range[1]:
                return None
            start = self.current_start
            end = min(start + self.chunk_size - 1, self.total_range[1])
            self.current_start = end + 1
            return (start, end)

    def handle_client(self, data, client_address):
        message = json.loads(data.decode('utf-8'))
        if message["type"] == "request":
            task = self.get_next_task()
            if task:
                response = json.dumps({"type": "task", "range": list(task)})
            else:
                response = json.dumps({"type": "done"})
            self.server_socket.sendto(response.encode('utf-8'), client_address)
        elif message["type"] == "result":
            with self.lock:
                self.prime_numbers.extend(message["primes"])

    def run(self):
        while True:
            data, client_address = self.server_socket.recvfrom(4096)
            self.handle_client(data, client_address)
            if self.current_start > self.total_range[1]:
                break
        print(f"Total de primos encontrados: {len(self.prime_numbers)}")
        with open("data/primes.txt", "w") as f:
            f.write("\n".join(map(str, self.prime_numbers)))
        print("Resultados salvos em primes.txt")
        self.server_socket.close()


if __name__ == "__main__":
    server = PrimeServer()
    server.run()
