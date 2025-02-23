import unittest
import subprocess
import time
import os

class TestServerAndClient(unittest.TestCase):

    def setUp(self):
        """
        Starts the server before running the tests.

        We start the server in a separate process, and wait for 1 second to
        ensure that the server has had time to start and listen on the socket.
        """
        self.server_process = subprocess.Popen(['python', 'src/server.py'])

    def tearDown(self):
        """
        Terminates the server process after the tests.

        This method ensures that the server process is properly terminated
        and all resources are cleaned up after the tests have been executed.
        """
        self.server_process.terminate()
        self.server_process.wait()

    def test_one_client(self):
        """
        Tests the interaction between the server and a single client.

        This test starts a client process that connects to the server. It waits
        for the client process to complete its execution. After the client has
        finished, the test checks if the "primes.txt" file has been created in
        the "data" directory to verify that the server processed the client's
        requests and recorded the results.
        """
        client_process = subprocess.Popen(['python', 'src/client.py'])

        client_process.wait()

        self.assertTrue(os.path.exists("data/primes.txt"), "O arquivo primes.txt não foi criado!")

if __name__ == '__main__':
    unittest.main()
