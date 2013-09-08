import unittest
from m366.genetic_algorithims import convert_frombitstring, convert_fromlist


class GATests(unittest.TestCase):

    population = [
        '01111010',
        '11001101',
        '00010111',
        '10000101',
        '00001101',
        '11110011',
    ]

    def testBitStringConvert(self):
        self.assertEqual([0, 1, 1, 1, 1, 0, 1, 0], convert_frombitstring(self.population[0]))

    def testListConvert(self):
        self.assertEqual('11001101', convert_fromlist(self.population[1]))


if __name__ == '__main__':
    unittest.main()
