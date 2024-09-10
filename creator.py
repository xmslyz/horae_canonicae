# amDg
import datetime
import json
import calendar

import gausianmethod


def advent_start_date(year):
    """
    Searches for the first Sunday of Advent.

    Parameters:
        year (int): The queried year.

    Returns:
        datetime.date: The date of the first Sunday of the Advent season.
    """

    # Get the date for Christmas of the given year
    xmas_day = datetime.datetime.strptime(f'25-12-{year}', '%d-%m-%Y')

    # Find the last Sunday before or on Christmas
    if xmas_day.weekday() == 6:
        # If Christmas is a Sunday, the last Sunday is December 18th
        last_sunday = datetime.datetime.strptime(f'18-12-{year}', '%d-%m-%Y')
    else:
        # Otherwise, find the previous Sunday before Christmas
        shift = 24 - xmas_day.weekday()
        last_sunday = datetime.datetime.strptime(
            f'{shift}-12-{year}', '%d-%m-%Y')

    # Advent starts 4 Sundays before Christmas (3 Sundays = 21 days)
    advent_start = last_sunday - datetime.timedelta(days=21)

    return advent_start.date()


def is_epiphany_in_first_week(year):
    """
    Determines if Epiphany is celebrated in the first week of the year.

    If the first day of the year is a Monday (0) or Tuesday (1),
    the Epiphany (January 6th) will be celebrated in the first week of the year.

    Parameters:
    year (int): The queried year.

    Returns:
    bool: True if Epiphany (January 6th) falls in the first week of the year.
    """

    # Get the weekday of January 1st (0=Monday, 1=Tuesday, ..., 6=Sunday)
    first_day_no = datetime.datetime.strptime(
        f'01-01-{year}', '%d-%m-%Y').weekday()

    # If the first day of the year is Monday (0) or Tuesday (1), return True
    return first_day_no in [0, 1]


def baptism_sunday(year):
    """
    Finds the date of Baptism of the Lord, which is typically the Sunday after
    January 6th.

    Parameters:
        year (int): The queried year.

    Returns:
        datetime.date: The date of Baptism of the Lord.
    """

    # Date for January 6th (Epiphany)
    epiphany_date = datetime.datetime.strptime(f'06-01-{year}', '%d-%m-%Y')

    # Find the weekday of January 6th (0=Monday, 1=Tuesday, ..., 6=Sunday)
    epiphany_weekday = epiphany_date.weekday()

    # If January 6th is a Sunday,
    # the Baptism of the Lord is the following Sunday
    if epiphany_weekday == 6:
        days_until_next_sunday = 7
    else:
        days_until_next_sunday = (6 - epiphany_weekday) % 7

    baptism_sunday_date = epiphany_date + datetime.timedelta(
        days=days_until_next_sunday)

    return baptism_sunday_date.date()


def easter_time(year):
    """
    Computes the dates for Ash Wednesday, Easter, and Pentecost.

    Parameters:
        year (int): The queried year.

    Returns:
        tuple: A tuple containing the dates of Ash Wednesday, Easter, and
        Pentecost.
    """

    # Compute the date of Easter using the Gaussian method
    easter = gausianmethod.computus(year)

    # Calculate the date of Ash Wednesday (46 days before Easter)
    lent_duration = datetime.timedelta(days=46)
    ash_wednesday = easter - lent_duration

    # Calculate the date of Pentecost (49 days after Easter)
    eastertide = datetime.timedelta(days=49)
    pentecost = easter + eastertide

    return ash_wednesday, easter, pentecost


def advent_season(target_date: datetime.date, lit_year: int):
    start_date = advent_start_date(lit_year)
    end_date = datetime.datetime.strptime(
        f'24.12.{lit_year}', '%d.%m.%Y').date()
    return start_date <= target_date <= end_date


def xmass_season(target_date: datetime.date, lit_year: int):
    start_date = datetime.datetime.strptime(
        f'25.12.{lit_year}', '%d.%m.%Y').date()
    end_date = baptism_sunday(lit_year + 1)
    return start_date <= target_date <= end_date


def ordinary_season(target_date, lit_year: int):
    first_part_start = baptism_sunday(lit_year + 1)
    first_part_end, _,  second_part_start = easter_time(lit_year + 1)

    first_part = first_part_start < target_date < first_part_end
    second_part = second_part_start < target_date < advent_start_date(
        lit_year + 1)

    return bool(first_part | second_part)


def lent_seson(target_date, lit_year: int):
    start_date, end_date, _ = easter_time(lit_year + 1)
    return start_date <= target_date <= end_date


def easter_seson(target_date, lit_year: int):
    _, start_date, end_date = easter_time(lit_year + 1)
    return start_date <= target_date <= end_date


def find_proper_scope(search_date):
    # Szukamy przedziału Adwentu, w którym znajduje się data
    search_year = search_date.year

    # Sprawdzamy lata do przodu i wstecz, w którym przedziale znajduje się data
    for s_year in range(search_year - 1, search_year + 2):
        advent = advent_start_date(s_year)
        next_advent = advent_start_date(s_year + 1)

        if advent <= search_date < next_advent:
            return s_year

    return None  # Jeśli nie znaleziono, co teoretycznie nie powinno się zdarzyć


if __name__ == "__main__":
    target = datetime.date(2024, 2, 14)
    cal_year = find_proper_scope(target)

    print("adv", advent_season(target, cal_year))
    print("xma", xmass_season(target, cal_year))
    print("ord", ordinary_season(target, cal_year))
    print("len", lent_seson(target, cal_year))
    print("eas", easter_seson(target, cal_year))
