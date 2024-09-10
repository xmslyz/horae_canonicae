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


def get_liturgical_season(target_date: datetime.date) -> str:
    """
    Determines the liturgical season for a given date

    Parameters:
        target_date (datetime.date): The date for which the liturgical season is
         determined.
        lit_year (int): The liturgical year in which to check the date.

    Returns:
        str: The name of the liturgical season ('Advent', 'Christmas',
        'Ordinary', 'Lent', 'Easter'), or 'Unknown' if the date does not fall
        within any defined liturgical period.
    """
    lit_year = find_proper_scope(target_date)

    def advent_season(target_date: datetime.date, lit_year: int) -> bool:
        start_date = advent_start_date(lit_year)
        end_date = datetime.datetime.strptime(f'24.12.{lit_year}',
                                              '%d.%m.%Y').date()

        return start_date <= target_date <= end_date

    def xmass_season(target_date: datetime.date, lit_year: int) -> bool:
        start_date = datetime.datetime.strptime(f'25.12.{lit_year}',
                                                '%d.%m.%Y').date()
        end_date = baptism_sunday(lit_year + 1)
        return start_date <= target_date < end_date

    def ordinary_season(target_date: datetime.date, lit_year: int) -> bool:
        first_part_start = baptism_sunday(lit_year + 1)
        first_part_end, _, second_part_start = easter_time(lit_year + 1)
        first_part = first_part_start < target_date < first_part_end
        second_part = second_part_start < target_date < advent_start_date(
            lit_year + 1)
        return first_part or second_part

    def lent_season(target_date: datetime.date, lit_year: int) -> bool:
        start_date, end_date, _ = easter_time(lit_year + 1)
        return start_date <= target_date < end_date

    def easter_season(target_date: datetime.date, lit_year: int) -> bool:
        _, start_date, end_date = easter_time(lit_year + 1)
        return start_date <= target_date <= end_date

    # Map seasons to their corresponding functions
    seasons = {
        'Advent': lambda: advent_season(target_date, lit_year),
        'Christmas': lambda: xmass_season(target_date, lit_year),
        'Ordinary': lambda: ordinary_season(target_date, lit_year),
        'Lent': lambda: lent_season(target_date, lit_year),
        'Easter': lambda: easter_season(target_date, lit_year),
    }

    # Check which season the date belongs to
    for season, check_func in seasons.items():
        if check_func():
            return season

    return 'Unknown'


def find_proper_scope(date_to_search: datetime.date) -> int:
    """
    Finds the year in which the new liturgical year starts.

    ...

    The function determines which liturgical year the `date` falls into
    by checking the Advent periods of the current year, and the next year.

    Parameters:
        date_to_search (datetime.date): The date for which the corresponding
        liturgical year start year is sought.

    Returns:
        int: The year in which the new liturgical year (Advent) starts, which
        includes the `date`.
    """
    try:
        search_year = date_to_search.year

        # Check the Advent period in the previous, current, and next year
        for s_year in range(search_year - 1, search_year + 2):
            advent = advent_start_date(s_year)
            next_advent = advent_start_date(s_year + 1)

            if advent <= date_to_search < next_advent:
                return s_year

    except Exception as e:
        raise Exception(e)


def find_proper_week(initium: datetime.date, finis: datetime.date,
                     c_day: datetime.date) -> int:
    """
    Finds the index of the week (1 to 4)

    ...

    Where the given day (`c_day`) belongs within the period from `initium` to
    `finis`.

    Parameters:
        initium (datetime.date): Start date of the period.
        finis (datetime.date): End date of the period.
        c_day (datetime.date): The date for which to find the corresponding
        week.

    Returns:
        int: The index of the corresponding week (1-5),
        or raises an exception if the date is invalid.

    Raises:
        ValueError: If the given dates are invalid or if `c_day` is not within
        the range `[initium, finis]`.
        IndexError: If the calculated weeks do not fit within the expected
        range.
    """
    try:
        if finis < initium:
            raise ValueError(f'The end date is earlier than initial date.')
        if (finis - initium).days > 193:
            raise ValueError(
                f'The span between {initium} and {finis} cannot exceed 193 days.')
        if initium == finis == c_day:
            raise ValueError(
                f'The dates {initium}, {finis}, and {c_day} are all the same.')
        if c_day < initium or c_day > finis:
            raise ValueError(
                f'The date {c_day} is not within the range {initium}-{finis}.')

        sundays = []
        sun_week_no = []
        scope: datetime.timedelta = finis - initium

        # Find all Sundays within the date range
        for i in range(0, scope.days + 1):
            q_day = initium + datetime.timedelta(i)
            # If queried day is a Sunday, append it to the list
            if q_day.weekday() == 6:
                sundays.append(q_day)
                sun_week_no.append(q_day.isocalendar()[1])

        # Find the Sunday that corresponds to `c_day`
        q_sunday = first_day_of_week(sundays, c_day)

        # Find the index of the proper week
        for index in range(4):
            if q_sunday in sundays[index::4]:
                return index + 1

        # If no match is found, raise an error
        raise IndexError(
            "The calculated weeks do not fit within the expected range.")

    except ValueError as ve:
        raise ve  # Re-raise ValueError to be caught by the specific tests

    except IndexError as ie:
        raise ie  # Re-raise IndexError to be caught by the specific tests

    except Exception as e:
        raise Exception(f"An error occurred: {e}")


def first_day_of_week(sundays: list, c_day: datetime.date) -> datetime.date:
    """
    Finds the Sunday that corresponds to the given day.

    Parameters:
        sundays (list): List of Sundays within a given period.
        c_day (datetime.date): The day for which the corresponding Sunday is
        found.

    Returns:
        datetime.date: The Sunday that corresponds to the given day.

    Raises:
        ValueError: If no valid Sunday is found for the given day.
    """
    try:
        for sunday in sundays:
            # Calculate the difference in days
            difference = (c_day - sunday).days

            # If the difference is within the current week (0 to 6),
            # return the Sunday
            if 0 <= difference < 7:
                return sunday

        # If no valid Sunday is found, raise ValueError
        raise ValueError(f"No valid Sunday found for the date {c_day}")

    except ValueError as e:
        print(f"Error: {e}")
        raise  # Re-raise the ValueError to propagate the error
