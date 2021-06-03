import unittest

import CompareViruses
import Simulation
import main


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)

    def test(self):
        Simulation.set_values(5,10,10,10,10,10)
        s = CompareViruses.infected_percent1
        self.assertEqual(s, 10)





if __name__ == '__main__':
    unittest.main()
