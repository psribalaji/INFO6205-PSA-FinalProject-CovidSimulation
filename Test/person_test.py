import unittest
import numpy as np

from Person import Person
import random


class MyTestCase(unittest.TestCase):
    def test_infect(self):
        p = Person(1, np.random.random() * 100, np.random.random() * 100,
                   np.random.random() * 100, np.random.random() * 100,
                   (np.random.random() + 0.5) * 100, 100, False, [], random.randint(1, 100))
        p.infect(10)
        self.assertEqual(p.infected, True)

    def test_recover(self):
        p = Person(1, np.random.random() * 100, np.random.random() * 100,
                   np.random.random() * 100, np.random.random() * 100,
                   (np.random.random() + 0.5) * 100, 100, False, [], random.randint(1, 100))
        p.recover()
        self.assertEqual(p.recovered, True)

    def test_death(self):
        p = Person(1, np.random.random() * 100, np.random.random() * 100,
                   np.random.random() * 100, np.random.random() * 100,
                   (np.random.random() + 0.5) * 100, 100, False, [], random.randint(1, 100))
        p.death_of_person()
        self.assertEqual(p.death, True)

    def test_vaccination(self):
        p = Person(1, np.random.random() * 100, np.random.random() * 100,
                   np.random.random() * 100, np.random.random() * 100,
                   (np.random.random() + 0.5) * 100, 100, False, [], random.randint(1, 100))
        p.vaccine(10)
        self.assertEqual(p.vaccinated, True)

    def test_immunity(self):
        p = Person(1, np.random.random() * 100, np.random.random() * 100,
                   np.random.random() * 100, np.random.random() * 100,
                   (np.random.random() + 0.5) * 100, 100, False, [], random.randint(1, 100))
        p.immune()
        self.assertEqual(p.vaccineImmunityBuilt, True)

    def test_check_infected(self):
        p = Person(1, np.random.random() * 100, np.random.random() * 100,
                   np.random.random() * 100, np.random.random() * 100,
                   (np.random.random() + 0.5) * 100, 100, False, [], random.randint(1, 100))
        p.infect(100)
        p.check_infected(210)
        self.assertEqual(p.recovered, True)

    def test_check_vaccinated(self):
        p = Person(1, np.random.random() * 100, np.random.random() * 100,
                   np.random.random() * 100, np.random.random() * 100,
                   (np.random.random() + 0.5) * 100, 100, False, [], random.randint(1, 100))
        p.vaccine(100)
        p.check_vaccinated(210)
        self.assertEqual(p.vaccineImmunityBuilt, True)

    def test_update_position(self):
        p = Person(1, np.random.random() * 100, np.random.random() * 100,
                   np.random.random() * 100, np.random.random() * 100,
                   (np.random.random() + 0.5) * 100, 100, False, [], random.randint(1, 100))
        p.update_pos(100, 100)
        self.assertEqual(p.posy == 100 and p.posx == 100, True)

    def test_get_color(self):
        p = Person(1, np.random.random() * 100, np.random.random() * 100,
                   np.random.random() * 100, np.random.random() * 100,
                   (np.random.random() + 0.5) * 100, 100, False, [], random.randint(1, 100))
        self.assertEqual(p.get_color() == "deepskyblue", True)
        p.infect(100)
        self.assertEqual(p.get_color() == "red", True)
        p.recover()
        self.assertEqual(p.get_color() == "green", True)
        p.immune()
        self.assertEqual(p.get_color() == "orange", True)
        p.vaccine(100)
        self.assertEqual(p.get_color() == "purple", True)
        p.death_of_person()
        self.assertEqual(p.get_color() == "black", True)

    def test_get_dist(self):
        p = Person(1, 100, 100,
                   np.random.random() * 100, np.random.random() * 100,
                   (np.random.random() + 0.5) * 100, 100, False, [], random.randint(1, 100))
        dist = p.get_dist(50, 50, p)
        self.assertEqual(dist == 70.71067811865476, True)


if __name__ == '__main__':
    unittest.main()
