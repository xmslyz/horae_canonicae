from unittest import TestCase
import datetime
from creator import (advent_start_date, is_epiphany_in_first_week,
                     baptism_sunday, easter_time, get_liturgical_season,
                     find_proper_scope, find_proper_week, first_day_of_week)


class TestAdventStartDate(TestCase):
    def test_advent_start_date_regular_year(self):
        # 1st December 2024 is the first Sunday of Advent
        year = 2024
        expected = datetime.date(2024, 12, 1)
        result = advent_start_date(year)
        self.assertEqual(result, expected)

    def test_advent_start_date_christmas_sunday(self):
        # 3rd December 2023 is the first Sunday of Advent
        year = 2023
        expected = datetime.date(2023, 12, 3)
        result = advent_start_date(year)
        self.assertEqual(result, expected)

    def test_advent_start_date_christmas_saturday(self):
        # 30th November 2025 is the first Sunday of Advent
        year = 2025
        expected = datetime.date(2025, 11, 30)
        result = advent_start_date(year)
        self.assertEqual(result, expected)

    def test_advent_start_date_christmas_monday(self):
        # 29th November 2026 is the first Sunday of Advent
        year = 2026
        expected = datetime.date(2026, 11, 29)
        result = advent_start_date(year)
        self.assertEqual(result, expected)

    def test_advent_start_date_christmas_friday(self):
        # 27th November 2022 is the first Sunday of Advent
        year = 2022
        expected = datetime.date(2022, 11, 27)
        result = advent_start_date(year)
        self.assertEqual(result, expected)


class TestEpiphanyInFirstWeek(TestCase):
    def test_epiphany_in_first_week_monday(self):
        year = 2024  # January 1, 2024 is a Monday
        expected = True
        result = is_epiphany_in_first_week(year)
        self.assertEqual(result, expected)

    def test_epiphany_not_in_first_week_tuesday(self):
        year = 2025  # January 1, 2025 is a Wednesday
        expected = False
        result = is_epiphany_in_first_week(year)
        self.assertEqual(result, expected)

    def test_epiphany_not_in_first_week_wednesday(self):
        year = 2026  # January 1, 2026 is a Thursday
        expected = False
        result = is_epiphany_in_first_week(year)
        self.assertEqual(result, expected)

    def test_epiphany_not_in_first_week_sunday(self):
        year = 2023  # January 1, 2023 is a Sunday
        expected = False
        result = is_epiphany_in_first_week(year)
        self.assertEqual(result, expected)

    def test_epiphany_not_in_first_week_friday(self):
        year = 2027  # January 1, 2027 is a Friday
        expected = False
        result = is_epiphany_in_first_week(year)
        self.assertEqual(result, expected)


class TestBaptismSunday(TestCase):
    def test_baptism_sunday_sunday(self):
        year = 2024  # January 6, 2024 is a Saturday
        expected = datetime.date(2024, 1, 7)  # The following Sunday
        result = baptism_sunday(year)
        self.assertEqual(result, expected)

    def test_baptism_sunday_monday(self):
        year = 2025  # January 6, 2025 is a Monday
        expected = datetime.date(2025, 1, 12)  # The following Sunday
        result = baptism_sunday(year)
        self.assertEqual(result, expected)

    def test_baptism_sunday_tuesday(self):
        year = 2028  # January 6, 2028 is a Tuesday
        expected = datetime.date(2028, 1, 9)  # The following Sunday
        result = baptism_sunday(year)
        self.assertEqual(result, expected)

    def test_baptism_sunday_friday(self):
        year = 2027  # January 6, 2027 is a Friday
        expected = datetime.date(2027, 1, 10)  # The following Sunday
        result = baptism_sunday(year)
        self.assertEqual(result, expected)

    def test_baptism_sunday_saturday(self):
        year = 2023  # January 6, 2023 is a Thuersday
        expected = datetime.date(2023, 1, 8)  # The following Sunday
        result = baptism_sunday(year)
        self.assertEqual(result, expected)


class TestEasterTime(TestCase):
    def test_easter_time(self):
        # Test cases with known values for Easter dates
        test_cases = [
            (
                2024,
                datetime.date(2024, 2, 14),
                datetime.date(2024, 3, 31),
                datetime.date(2024, 5, 19)
            ),
            (
                2025,
                datetime.date(2025, 3, 5),
                datetime.date(2025, 4, 20),
                datetime.date(2025, 6, 8)
            ),
            (
                2026,
                datetime.date(2026, 2, 18),
                datetime.date(2026, 4, 5),
                datetime.date(2026, 5, 24)
            ),
        ]

        for year, expected_ash_wednesday, expected_easter, expected_pentecost \
                in test_cases:
            with self.subTest(year=year):
                ash_wednesday, easter, pentecost = easter_time(year)
                self.assertEqual(ash_wednesday, expected_ash_wednesday)
                self.assertEqual(easter, expected_easter)
                self.assertEqual(pentecost, expected_pentecost)


class TestLiturgicalSeasons(TestCase):
    def test_advent_season(self):
        test_cases = [
            (datetime.date(2024, 12, 1), 'Advent'),  # Start of Advent
            (datetime.date(2024, 12, 10), 'Advent'),  # During Advent
            (datetime.date(2024, 12, 24), 'Advent'),  # End of Advent
            (datetime.date(2024, 12, 25), 'Christmas')  # Day after Advent
        ]
        for date, expected in test_cases:
            with self.subTest(date=date):
                self.assertEqual(get_liturgical_season(date), expected)

    def test_christmas_season(self):
        test_cases = [
            (datetime.date(2024, 12, 25), 'Christmas'),  # Start of Christmas
            (datetime.date(2024, 12, 30), 'Christmas'),  # During Christmas
            (datetime.date(2025, 1, 6), 'Christmas'),  # End of Christmas
            (datetime.date(2025, 1, 13), 'Ordinary')  # Day after Christmas
        ]
        for date, expected in test_cases:
            with self.subTest(date=date):
                self.assertEqual(get_liturgical_season(date), expected)

    def test_ordinary_season(self):
        test_cases = [
            (datetime.date(2025, 1, 7), 'Christmas'),  # Before Ordinary Time
            (datetime.date(2025, 2, 15), 'Ordinary'),  # OT #1 period
            (datetime.date(2025, 3, 4), 'Ordinary'),  # OT #1 period
            (datetime.date(2025, 3, 5), 'Lent'),  # Start of Lent
            (datetime.date(2025, 7, 7), 'Ordinary'),  # OT #2 period
            (datetime.date(2025, 11, 14), 'Ordinary'),  # OT #2 period
            (datetime.date(2025, 11, 30), 'Advent')  # Start of Advent

        ]
        for date, expected in test_cases:
            with self.subTest(date=date):
                self.assertEqual(get_liturgical_season(date), expected)

    def test_lent_season(self):
        test_cases = [
            (datetime.date(2025, 2, 5), 'Ordinary'),  # OT
            (datetime.date(2025, 3, 5), 'Lent'),  # Start of Lent
            (datetime.date(2025, 4, 10), 'Lent'),  # During Lent
            (datetime.date(2025, 4, 19), 'Lent'),  # End of Lent
            (datetime.date(2025, 4, 20), 'Easter')  # Easter
        ]
        for date, expected in test_cases:
            with self.subTest(date=date):
                self.assertEqual(get_liturgical_season(date), expected)

    def test_easter_season(self):
        test_cases = [
            (datetime.date(2025, 4, 20), 'Easter'),  # Start of Easter
            (datetime.date(2025, 5, 10), 'Easter'),  # During Easter
            (datetime.date(2025, 6, 8), 'Easter'),  # End of Easter
            (datetime.date(2025, 6, 9), 'Ordinary')  # Day after Pentecost
        ]
        for date, expected in test_cases:
            with self.subTest(date=date):
                self.assertEqual(get_liturgical_season(date), expected)

    def test_random_season(self):
        test_cases = [
            (datetime.date(2020, 11, 30), 'Advent'),
            (datetime.date(2024, 12, 25), 'Christmas'),
            (datetime.date(2028, 5, 21), 'Easter'),
            (datetime.date(2019, 6, 10), 'Ordinary'),
            (datetime.date(1990, 12, 31), 'Christmas')
            # not in any season
        ]
        for date, expected in test_cases:
            with self.subTest(date=date):
                self.assertEqual(get_liturgical_season(date), expected)


class TestFindProperScope(TestCase):
    def test_find_proper_scope(self):
        test_cases = [
            (datetime.date(2020, 12, 15), 2020),
            (datetime.date(2021, 1, 7), 2020),
            (datetime.date(2022, 12, 10), 2022),
            (datetime.date(2022, 5, 10), 2021),
            (datetime.date(2024, 11, 30), 2023),
        ]

        for date_to_search, expected_year in test_cases:
            with self.subTest(date_to_search=date_to_search):
                self.assertEqual(find_proper_scope(date_to_search),
                                 expected_year)


class TestFindProperWeek(TestCase):
    def test_find_proper_week(self):
        # Helper function to set up test cases
        def setup_case(initium, finis, c_day, expected_week):
            self.assertEqual(find_proper_week(initium, finis, c_day),
                             expected_week)

        # Define some test cases
        test_cases = [
            # Test case 1: Week 1 within the period
            (datetime.date(2024, 1, 1), datetime.date(2024, 1, 31),
             datetime.date(2024, 1, 7), 1),

            # Test case 2: Week 2 within the period
            (datetime.date(2023, 1, 1), datetime.date(2023, 1, 31),
             datetime.date(2023, 1, 14), 2),

            # Test case 3: Week 3 within the period
            (datetime.date(2022, 1, 1), datetime.date(2022, 1, 31),
             datetime.date(2022, 1, 21), 3),

            # Test case 4: Week 4 within the period
            (datetime.date(2021, 1, 1), datetime.date(2021, 1, 31),
             datetime.date(2021, 1, 28), 4),

            # Test case 5: Day outside the range
            (datetime.date(2020, 1, 1), datetime.date(2020, 1, 31),
             datetime.date(2020, 2, 4), None),  # Expecting ValueError

            # Test case 6: Start and end date are the same (ValueError expected)
            (datetime.date(2024, 1, 1), datetime.date(2024, 1, 1),
             datetime.date(2024, 1, 10), None),  # Expecting ValueError

            # Test case 7: General case with a large range
            (datetime.date(2018, 12, 1), datetime.date(2019, 2, 1),
             datetime.date(2019, 1, 14), 3),

            # Test case 8: Period spans across different years
            (datetime.date(2012, 12, 15), datetime.date(2013, 1, 15),
             datetime.date(2013, 1, 7), 4),

            # Test case 9: No Sundays in the period (should raise IndexError)
            (datetime.date(2046, 1, 1), datetime.date(2046, 1, 6),
             datetime.date(2046, 1, 5), None),  # Expecting IndexError

            # Test case 10: All dates are the same (ValueError expected)
            (datetime.date(2020, 1, 15), datetime.date(2020, 1, 15),
             datetime.date(2020, 1, 15), None),  # Expecting ValueError

            # Test case 11: Date is the last possible Sunday in the period
            (datetime.date(2024, 1, 1), datetime.date(2024, 1, 31),
             datetime.date(2024, 1, 28), 4),

            # Test case 12: The date is exactly on the boundary of the period
            (datetime.date(2024, 1, 1), datetime.date(2024, 1, 31),
             datetime.date(2024, 1, 31), 4),

            # Test case 14: Period is one day long and matches the date to find
            (datetime.date(2024, 1, 1), datetime.date(2024, 1, 2),
             datetime.date(2024, 1, 1), None),  # Expecting ValueError

            # Test case 15: Invalid period where finis is before initium (
            # ValueError expected)
            (datetime.date(2024, 1, 31), datetime.date(2024, 1, 1),
             datetime.date(2024, 1, 15), None),  # Expecting ValueError

            # Test case 16: Boundary date is the first Sunday in the period
            (datetime.date(2024, 1, 1), datetime.date(2024, 1, 31),
             datetime.date(2024, 1, 7), 1),

            # Test case 17: Boundary date is the last Sunday in the period
            (datetime.date(2024, 1, 1), datetime.date(2024, 1, 31),
             datetime.date(2024, 1, 28), 4),
        ]

        for initium, finis, c_day, expected_week in test_cases:
            with self.subTest(initium=initium, finis=finis, c_day=c_day,
                              expected_week=expected_week):
                if expected_week is None:
                    with self.assertRaises(Exception) as cm:
                        find_proper_week(initium, finis, c_day)
                    exception_message = str(cm.exception)
                    if finis < initium:
                        expected_message = (f'The end date is earlier than '
                                            f'initial date.')
                    elif (finis - initium).days > 193:
                        expected_message = (f'The span between {initium} and '
                                            f'{finis} cannot exceed 193 days.')
                    elif initium == finis == c_day:
                        expected_message = (f'The dates {initium}, {finis}, '
                                            f'and {c_day} are all the same.')
                    elif c_day < initium or c_day > finis:
                        expected_message = (f'The date {c_day} is not within '
                                            f'the range {initium}-{finis}.')
                    else:
                        # expected_message = ("The calculated weeks do not fit "
                        #                     "within the expected range.")
                        expected_message = (f"No valid Sunday found for the "
                                            f"date {c_day}")
                    self.assertEqual(exception_message, expected_message)
                else:
                    result = find_proper_week(initium, finis, c_day)
                    print(result)
                    self.assertEqual(result, expected_week)


class TestFirstDayOfWeek(TestCase):
    def setUp(self):
        self.sundays = [
            datetime.date(2023, 12, 24),  # Christmas
            datetime.date(2023, 12, 31),  # End of 2023
            datetime.date(2024, 1, 7),  # 1st week of 2024
            datetime.date(2024, 1, 14),
            datetime.date(2024, 1, 21),
            datetime.date(2024, 1, 28),
            datetime.date(2024, 2, 4)
        ]

    def test_first_week_of_new_year(self):
        # Case where the date is in the first week of the new year
        self.assertEqual(
            first_day_of_week(self.sundays, datetime.date(2024, 1, 3)),
            datetime.date(2023, 12, 31)
        )

    def test_exact_sunday(self):
        # Case where the date falls exactly on a Sunday
        self.assertEqual(
            first_day_of_week(self.sundays, datetime.date(2024, 1, 7)),
            datetime.date(2024, 1, 7)
        )

    def test_middle_of_week(self):
        # Case in the middle of the week of a new year
        self.assertEqual(
            first_day_of_week(self.sundays, datetime.date(2024, 1, 10)),
            datetime.date(2024, 1, 7)
        )

    def test_leap_year(self):
        # Case with a leap year February
        leap_year_sundays = [
            datetime.date(2020, 2, 23),
            # Last Sunday of February in a leap year
            datetime.date(2020, 3, 1),
            datetime.date(2020, 3, 8)
        ]
        self.assertEqual(
            first_day_of_week(leap_year_sundays, datetime.date(2020, 2, 29)),
            datetime.date(2020, 2, 23)
        )

    def test_no_sunday_before_list(self):
        # Case where no Sunday matches (before the first Sunday of the list)
        self.assertEqual(
            first_day_of_week(self.sundays, datetime.date(2023, 12, 25)),
            datetime.date(2023, 12, 24)
        )

    def test_last_day_of_month(self):
        # Case where the date falls on exactly the last day of a month
        self.assertEqual(
            first_day_of_week(self.sundays, datetime.date(2024, 1, 31)),
            datetime.date(2024, 1, 28)
        )

    def test_boundary_of_year(self):
        # Test with dates at the boundary of months and years
        self.assertEqual(
            first_day_of_week(self.sundays, datetime.date(2024, 1, 1)),
            datetime.date(2023, 12, 31)
        )

    def test_date_after_last_sunday(self):
        # Case where the date falls after the last Sunday in the list
        self.assertEqual(
            first_day_of_week(self.sundays, datetime.date(2024, 2, 10)),
            datetime.date(2024, 2, 4))

    def test_date_more_than_week_after_last_sunday(self):
        # Case where c-day is more than a week after the last Sunday in the list
        with self.assertRaises(ValueError):
            first_day_of_week(self.sundays, datetime.date(2024, 2, 12))

    def test_future_dates(self):
        # Test with future dates beyond 2024
        future_sundays = [
            datetime.date(2030, 12, 1),
            datetime.date(2030, 12, 8),
            datetime.date(2030, 12, 15)
        ]
        self.assertEqual(
            first_day_of_week(future_sundays, datetime.date(2030, 12, 9)),
            datetime.date(2030, 12, 8)
        )


def check_span(initium, finis):
    if (finis - initium).days > 193:
        raise ValueError(
            f'The span between {initium} and {finis} cannot exceed 193 days.')


class TestMaximalSpan(TestCase):
    def test_valid_span(self):
        initium = datetime.date(2024, 5, 24)  # Zesłanie Ducha Świętego
        finis = datetime.date(2024, 12, 3)  # Początek Adwentu
        try:
            check_span(initium, finis)
        except ValueError:
            self.fail("check_span raised ValueError unexpectedly!")

    def test_exceeding_span(self):
        initium = datetime.date(2024, 5, 24)  # Zesłanie Ducha Świętego
        finis = datetime.date(2025, 1, 1)  # Poza maksymalnym zakresem
        with self.assertRaises(ValueError):
            check_span(initium, finis)

    def test_exact_max_span(self):
        initium = datetime.date(2024, 5, 24)  # Zesłanie Ducha Świętego
        finis = initium + datetime.timedelta(days=193)  # Dokładnie
        # maksymalny zakres
        try:
            check_span(initium, finis)
        except ValueError:
            self.fail("check_span raised ValueError unexpectedly!")

    def test_span_with_same_dates(self):
        initium = datetime.date(2024, 5, 24)
        finis = initium  # identyczne daty
        try:
            check_span(initium, finis)
        except ValueError:
            self.fail("check_span raised ValueError unexpectedly!")


# To run the tests
if __name__ == '__main__':
    import unittest

    unittest.main()
