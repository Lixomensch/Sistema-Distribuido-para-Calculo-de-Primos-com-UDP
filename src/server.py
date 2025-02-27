"""PrimeServer module."""
import json
import socket
import threading


class PrimeServer:
    """PrimeServer class represents a server that handles incoming requests from clients."""

    def __init__(self, host='localhost',
                 port=9999,
                 total_range=(1, 100000),
                 chunk_size=5000):
        """
        Initializes a PrimeServer object with the given parameters.

        Args:
            host (str): The hostname or IP address of the server.
            port (int): The port number of the server.
            total_range (tuple): The start and end of the range of numbers to be checked.
            chunk_size (int): The number of numbers to be checked for primality in each task.

        Attributes:
            host (str): The hostname or IP address of the server.
            port (int): The port number of the server.
            total_range (tuple): The start and end of the range of numbers to be checked.
            chunk_size (int): The number of numbers to be checked for primality in each task.
            prime_numbers (list): The list of prime numbers found by the server.
            current_start (int): The start of the current task range.
            lock (threading.Lock): A lock to synchronize access to the server's.
            server_socket (socket.socket): The server socket object.
        """
        self.total_range = total_range
        self.chunk_size = chunk_size
        self.prime_numbers = []
        self.current_start = total_range[0]
        self.lock = threading.Lock()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind((host, port))
        self.client_addresses = []
        print(f"Servidor iniciado em {host}:{port}")

    def get_next_task(self):
        """
        Returns the next task range (start, end) to be processed.

        The range is a tuple of two integers, start and end, representing
        the lower and upper bounds of the range to be processed.

        The range is chosen such that its size is less than or equal to
        self.chunk_size.

        This method is thread-safe.
        """
        with self.lock:
            if self.current_start > self.total_range[1]:
                return None
            start = self.current_start
            end = min(start + self.chunk_size - 1, self.total_range[1])
            self.current_start = end + 1
            # print(start, end)
            return (start, end)

    def handle_client(self, message, client_address):
        """
        Handles incoming client requests by processing task requests or results.

        Args:
            data (bytes): The incoming data from the client, expected to be a JSON-encoded message.
            client_address (tuple): The address of the client as a (host, port) tuple.

        The function decodes the incoming message and checks its type. If it's a "request",
        the next task range is retrieved and sent to the client. If there are no tasks left,
        a "done" message is sent. If it's a "result", the list of prime numbers received is
        added to the server's list of primes.
        """
        if message["type"] == "request":
            task = self.get_next_task()
            if task:
                response = json.dumps({"type": "task", "range": list(task)})
                self.client_addresses.append(client_address)
            else:
                response = json.dumps({"type": "done"})
                self.client_addresses.append(client_address)
            self.server_socket.sendto(response.encode('utf-8'), client_address)
        elif message["type"] == "result":
            with self.lock:
                self.prime_numbers.extend(message["primes"])

    def send_done(self):
        """Sends a 'done' message to all connected clients after completing the task."""
        done_message = json.dumps({"type": "done"})
        for client_address in self.client_addresses:
            self.server_socket.sendto(
                done_message.encode('utf-8'), client_address)

    def run(self):
        """
        Runs the server, listening for incoming client requests and processing.

        This method is the main entry point for the server and is responsible for
        handling all incoming client requests and processing the responses.

        During execution, the server will print the total number of primes found
        and save the results to a file named "primes.txt" in the "data" directory.
        The server will also print a message indicating that the results have been
        saved.

        After execution, the server socket is closed.
        """
        while True:
            data, client_address = self.server_socket.recvfrom(4096)
            message = json.loads(data.decode('utf-8'))
            self.handle_client(message, client_address)

            if self.current_start > self.total_range[1] and message["type"] == "result":
                break

        print(f"Total de primos encontrados: {len(self.prime_numbers)}")
        with open("data/primes.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(map(str, self.prime_numbers)))
        print("Resultados salvos em primes.txt")

        self.send_done()
        self.server_socket.close()


if __name__ == "__main__":
    server = PrimeServer()
    server.run()
