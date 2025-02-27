"""PrimeClient module."""
import json
import socket


def find_primes(start, end):
    """
    Finds all prime numbers within a specified range using the Sieve of Eratosthenes algorithm.

    Args:
        start (int): The starting number of the range (inclusive).
        end (int): The ending number of the range (inclusive).

    Returns:
        list: A list of prime numbers between the start and end values.
    """
    primos = [True] * (end + 1)
    primos[0] = primos[1] = False

    for i in range(2, int(end ** 0.5) + 1):
        if primos[i]:
            for j in range(i * i, end + 1, i):
                primos[j] = False

    return [i for i in range(start, end + 1) if primos[i]]


class PrimeClient:
    """PrimeClient class represents a client that connects to a PrimeServer."""

    def __init__(self, server_host='localhost', server_port=9999):
        """
        Initializes a PrimeClient object with the given server host and port.

        Args:
            server_host (str): The hostname or IP address of the server.
            server_port (int): The port number of the server.

        Attributes:
            server_address (tuple): The address of the server as a (host, port) tuple.
            client_socket (socket.socket): The UDP socket used to communicate with the server.
        """
        self.server_address = (server_host, server_port)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def request_task(self):
        """
        Sends a request to the server to retrieve the next task range for processing.

        The request is sent as a JSON-encoded message with the type "request".
        The function waits for a response from the server and decodes the JSON message
        containing the task information or a "done" message if no tasks are available.

        Returns:
            dict: The decoded JSON response from the server, which includes either
                the task range or a "done" message indicating no tasks are left.
        """
        request = json.dumps({"type": "request"})
        self.client_socket.sendto(request.encode('utf-8'), self.server_address)
        data, _ = self.client_socket.recvfrom(4096)
        return json.loads(data.decode('utf-8'))

    def send_result(self, primes):
        """
        Sends the result of the task to the server.

        Args:
            primes (list): The list of prime numbers found within the task range.

        The result is sent as a JSON-encoded message with the type "result" and
        the list of prime numbers to the server.
        """
        result = json.dumps({"type": "result", "primes": primes})
        self.client_socket.sendto(result.encode('utf-8'), self.server_address)

    def run(self):
        """
        Runs the client, continuously requesting tasks from the server.

        This method is an infinite loop, so call it with caution!

        When no tasks are available, the client prints a message and closes
        the socket.
        """
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
