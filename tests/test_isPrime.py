import unittest

def is_prime(num):
    """
    Determines if a number is prime.

    Args:
        num (int): The number to check for primality.

    Returns:
        bool: True if the number is prime, False otherwise.
    """

    if num <= 1:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True

class TestPrimeFile(unittest.TestCase):
    """Test cases for the is_prime() function."""
    
    def test_is_prime(self):
        """
        Tests that all numbers written to the primes.txt file are prime numbers.

        This test opens the primes.txt file and reads all lines, then checks
        each number using the is_prime() function. If any number is not
        prime, the test fails.
        """
        print("#"*25,"Testando isPrime...","#"*25)
        with open("data/primes.txt", "r") as file:
            primes = file.readlines()

        for line in primes:
            num = int(line.strip())
            self.assertTrue(is_prime(num), f"{num} não é primo!")

if __name__ == '__main__':
    unittest.main()
