import json
import socket


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


class PrimeClient:
    def __init__(self, server_host='localhost', server_port=9999):
        self.server_address = (server_host, server_port)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def request_task(self):
        request = json.dumps({"type": "request"})
        self.client_socket.sendto(request.encode('utf-8'), self.server_address)
        data, _ = self.client_socket.recvfrom(4096)
        return json.loads(data.decode('utf-8'))

    def send_result(self, primes):
        result = json.dumps({"type": "result", "primes": primes})
        self.client_socket.sendto(result.encode('utf-8'), self.server_address)

    def run(self):
        while True:
            task = self.request_task()
            if task["type"] == "done":
                print("Nenhuma tarefa disponível. Encerrando cliente.")
                break
            start, end = task["range"]
            primes = find_primes(start, end)
            self.send_result(primes)
        self.client_socket.close()


if __name__ == "__main__":
    client = PrimeClient()
    client.run()
