from unittest import TestCase
import datetime
from gausianmethod import computus


class TestComputus(TestCase):

    def test_year_33_to_1582(self):
        # Boundary condition for year 33 (Death of Christ)
        self.assertEqual(computus(33), datetime.date(33, 4, 5))
        # Middle: Year 1000
        self.assertEqual(computus(1000), datetime.date(1000, 3, 31))
        # Boundary: Year 1582
        self.assertEqual(computus(1582), datetime.date(1582, 4, 15))

    def test_year_1583_to_1699(self):
        # Boundary: Year 1583
        self.assertEqual(computus(1583), datetime.date(1583, 4, 10))
        # Middle: Year 1600
        self.assertEqual(computus(1600), datetime.date(1600, 4, 2))
        # Boundary: Year 1699
        self.assertEqual(computus(1699), datetime.date(1699, 4, 19))

    def test_year_1700_to_1799(self):
        # Boundary: Year 1700
        self.assertEqual(computus(1700), datetime.date(1700, 4, 11))
        # Middle: Year 1750
        self.assertEqual(computus(1750), datetime.date(1750, 3, 29))
        # Boundary: Year 1799
        self.assertEqual(computus(1799), datetime.date(1799, 3, 24))

    def test_year_1800_to_1899(self):
        # Boundary: Year 1800
        self.assertEqual(computus(1800), datetime.date(1800, 4, 13))
        # Middle: Year 1850
        self.assertEqual(computus(1850), datetime.date(1850, 3, 31))
        # Boundary: Year 1899
        self.assertEqual(computus(1899), datetime.date(1899, 4, 2))

    def test_year_1900_to_2099(self):
        # Boundary: Year 1900
        self.assertEqual(computus(1900), datetime.date(1900, 4, 15))
        # Middle: Year 2000
        self.assertEqual(computus(2000), datetime.date(2000, 4, 23))
        # Boundary: Year 2099
        self.assertEqual(computus(2099), datetime.date(2099, 4, 12))

    def test_year_2100_to_2199(self):
        # Boundary: Year 2100
        self.assertEqual(computus(2100), datetime.date(2100, 3, 28))
        # Middle: Year 2150
        self.assertEqual(computus(2150), datetime.date(2150, 4, 12))
        # Boundary: Year 2199
        self.assertEqual(computus(2199), datetime.date(2199, 4, 14))

    def test_year_2200_to_2299(self):
        # Boundary: Year 2200
        self.assertEqual(computus(2200), datetime.date(2200, 4, 6))
        # Middle: Year 2250
        self.assertEqual(computus(2250), datetime.date(2250, 4, 21))
        # Boundary: Year 2299
        self.assertEqual(computus(2299), datetime.date(2299, 4, 16))

    def test_year_2300_to_2999(self):
        # Test various future years with different A and B values
        self.assertEqual(computus(2300), datetime.date(2300, 4, 8))
        self.assertEqual(computus(2400), datetime.date(2400, 4, 16))
        self.assertEqual(computus(2500), datetime.date(2500, 4, 18))
        self.assertEqual(computus(2600), datetime.date(2600, 3, 23))
        self.assertEqual(computus(2700), datetime.date(2700, 4, 1))
        self.assertEqual(computus(2900), datetime.date(2900, 4, 11))
        self.assertEqual(computus(2999), datetime.date(2999, 3, 24))

    def test_exceptions(self):
        # I type exceptions

        self.assertEqual(computus(1609), datetime.date(1609, 4, 19))
        self.assertEqual(computus(1981), datetime.date(1981, 4, 19))
        self.assertEqual(computus(2076), datetime.date(2076, 4, 19))
        self.assertEqual(computus(2133), datetime.date(2133, 4, 19))
        self.assertEqual(computus(2201), datetime.date(2201, 4, 19))
        self.assertEqual(computus(2296), datetime.date(2296, 4, 19))
        self.assertEqual(computus(2448), datetime.date(2448, 4, 19))
        self.assertEqual(computus(2668), datetime.date(2668, 4, 19))
        self.assertEqual(computus(2725), datetime.date(2725, 4, 19))
        self.assertEqual(computus(2820), datetime.date(2820, 4, 19))
        # II type exceptions
        self.assertEqual(computus(1954), datetime.date(1954, 4, 18))
        self.assertEqual(computus(2049), datetime.date(2049, 4, 18))
        self.assertEqual(computus(2106), datetime.date(2106, 4, 18))


    def test_year_before_33(self):
        # Test year before 33
        with self.assertRaises(ValueError):
            computus(32)

    def test_year_3000(self):
        # Test far future year 3000
        with self.assertRaises(ValueError):
            computus(3000)


if __name__ == "__main__":
    unittest.main()
