import datetime
from unittest import TestCase
from creator import Skeleton


class TestSkeleton(TestCase):
    def setUp(self):
        self.sk = Skeleton(datetime.date.today())

    def test_psalter_first_week(self):
        test_cases = [
            (datetime.date(2012, 1, 9), 1),
            (datetime.date(2013, 1, 14), 1),
            (datetime.date(2014, 1, 13), 1),
            (datetime.date(2015, 1, 12), 1)
        ]
        for date, expected in test_cases:
            with self.subTest(date=date):
                self.sk = Skeleton(date)
                self.assertEqual(self.sk.current_psalter_week, expected)

    def test_psalter_first_week_after_pentecost(self):
        test_cases = [
            (datetime.date(2012, 5, 28), 4),
            (datetime.date(2013, 5, 20), 2),
            (datetime.date(2014, 6, 9), 1),
            (datetime.date(2015, 5, 25), 3),
            (datetime.date(2016, 5, 16), 2),
            (datetime.date(2017, 6, 5), 1),
            (datetime.date(2018, 5, 21), 3),
            (datetime.date(2019, 6, 10), 1),
            (datetime.date(2020, 6, 1), 4),
            (datetime.date(2021, 5, 24), 3)
        ]

        for date, expected in test_cases:
            with self.subTest(date=date):
                self.sk = Skeleton(date)
                self.assertEqual(self.sk.current_psalter_week, expected)

    def test_psalter_ash_weekdays(self):
        test_cases = [
            (datetime.date(2012, 2, 22), 4),
            (datetime.date(2015, 2, 18), 4),
            (datetime.date(2018, 2, 14), 4),
            (datetime.date(2021, 2, 17), 4),
            (datetime.date(2024, 2, 14), 4),
            (datetime.date(2027, 2, 10), 4)
        ]
        for date, expected in test_cases:
            with self.subTest(date=date):
                self.sk = Skeleton(date)
                self.assertEqual(self.sk.current_psalter_week, expected)

    def test_psalter_weeks_of_lent(self):
        test_cases_week_1 = [
            (datetime.date(2013, 2, 17), 1),
            (datetime.date(2016, 2, 14), 1),
            (datetime.date(2019, 3, 10), 1),
            (datetime.date(2022, 3, 6), 1),
            (datetime.date(2029, 2, 18), 1)
        ]

        test_cases_week_2 = [
            (datetime.date(2013, 2, 24), 2),
            (datetime.date(2016, 2, 21), 2),
            (datetime.date(2019, 3, 17), 2),
            (datetime.date(2022, 3, 13), 2),
            (datetime.date(2029, 2, 25), 2)
        ]
        test_cases_week_3 = [
            (datetime.date(2013, 3, 3), 3),
            (datetime.date(2016, 2, 28), 3),
            (datetime.date(2019, 3, 24), 3),
            (datetime.date(2022, 3, 20), 3),
            (datetime.date(2029, 3, 4), 3)
        ]
        test_cases_week_4 = [
            (datetime.date(2013, 3, 10), 4),
            (datetime.date(2016, 3, 6), 4),
            (datetime.date(2019, 3, 31), 4),
            (datetime.date(2022, 3, 27), 4),
            (datetime.date(2029, 3, 11), 4)
        ]
        test_cases_week_5 = [
            (datetime.date(2013, 3, 17), 1),
            (datetime.date(2016, 3, 13), 1),
            (datetime.date(2019, 4, 7), 1),
            (datetime.date(2022, 4, 3), 1),
            (datetime.date(2029, 3, 18), 1)
        ]
        test_cases_week_6 = [  # Wielki tydzień
            (datetime.date(2013, 3, 24), 2),
            (datetime.date(2016, 3, 20), 2),
            (datetime.date(2019, 4, 14), 2),
            (datetime.date(2022, 4, 10), 2),
            (datetime.date(2029, 3, 25), 2)
        ]

        test_cases_easter = [
            (datetime.date(2010, 4, 4), 1),
            (datetime.date(2012, 4, 8), 1),
            (datetime.date(2014, 4, 20), 1),
            (datetime.date(2017, 4, 16), 1),
            (datetime.date(2020, 4, 12), 1),
            (datetime.date(2023, 4, 9), 1),
            (datetime.date(2026, 4, 5), 1),
            (datetime.date(2030, 4, 21), 1)
        ]

        test_cases = [
            test_cases_week_1,
            test_cases_week_2,
            test_cases_week_3,
            test_cases_week_4,
            test_cases_week_5,
            test_cases_week_6,
            test_cases_easter
        ]

        for i, week_cases in enumerate(test_cases):
            for date, expected in week_cases:
                with self.subTest(date=date):
                    self.sk = Skeleton(date)
                    self.assertEqual(self.sk.current_psalter_week, expected)


# To run the tests
if __name__ == '__main__':
    import unittest

    unittest.main()
