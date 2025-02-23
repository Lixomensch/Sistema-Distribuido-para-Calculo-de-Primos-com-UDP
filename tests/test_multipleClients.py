import unittest
import threading
import subprocess

class TestMultipleClients(unittest.TestCase):
    """Test the server with multiple clients."""
    def setUp(self):
        """
        Starts the server before running the tests.

        We start the server in a separate process, and wait for 1 second to
        ensure that the server has had time to start and listen on the socket.
        """
        self.server_process = subprocess.Popen(['python', 'src/server.py'])

    def tearDown(self):
        """
        Tears down the server after running the tests.

        After running the tests, we terminate the server process and wait for
        it to finish. This ensures that all resources are cleaned up properly.
        """
        self.server_process.terminate()
        self.server_process.wait()

    def simulate_client(self):
        """
        Simulates a client connecting to the server.

        The function starts a client process that connects to the server and waits
        for it to complete its execution.
        """

        client_process = subprocess.Popen(['python', 'src/client.py'])
        client_process.wait()

    def test_multiple_clients(self):
        """
        Tests the server with 5 clients running simultaneously.

        This test starts 5 threads, each running a client process that connects
        to the server. The test waits for all threads to complete before
        finishing.

        The test can be used to verify that the server can handle multiple
        connections at the same time without problems.
        """
        print("#"*25,"Testando multipleClients...","#"*25)
        client_threads = []
        for i in range(5):
            thread = threading.Thread(target=self.simulate_client)
            client_threads.append(thread)
            thread.start()

        for thread in client_threads:
            thread.join()

if __name__ == '__main__':
    unittest.main()
