import unittest
import numpy as np

import random
import CompareViruses
from Person import Person


class MyTestCase(unittest.TestCase):
    def test_if_infected(self):
        p = Person(1, np.random.random() * 100, np.random.random() * 100,
                   np.random.random() * 100, np.random.random() * 100,
                   (np.random.random() + 0.5) * 100, 100, False, [], random.randint(1, 100))
        CompareViruses.check_if_infected_for_compare_viruses(4, p, 0.01)
        self.assertEqual(p.infected, True)

    def test_if_quarantine(self):
        p = Person(1, np.random.random() * 100, np.random.random() * 100,
                   np.random.random() * 100, np.random.random() * 100,
                   (np.random.random() + 0.5) * 100, 100, False, [], random.randint(1, 100))
        CompareViruses.check_if_quarantine_for_compare_viruses(2, p, 0.01)
        self.assertEqual(p.quarantine, True)

    def test_transmission(self):
        p = Person(1, np.random.random() * 100, np.random.random() * 100,
                   np.random.random() * 100, np.random.random() * 100,
                   (np.random.random() + 0.5) * 100, 100, False, [], random.randint(1, 100))
        CompareViruses.infect_person_on_transmission_for_compare_viruses(p, 2, 0.01, 1)
        self.assertEqual(p.infected, True)


if __name__ == '__main__':
    unittest.main()
