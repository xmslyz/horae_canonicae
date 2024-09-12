# amDg
import datetime

import gausianmethod


class Skeleton:
    def __init__(self, lg_day: datetime.date):
        self.lg_day = lg_day
        self.year = None
        self.dominical_cycle = None
        self.weekday_cycle = None
        self.season = None
        self.sunday_dates = []
        self.sunday_weeknumbers = []
        self.actual_sunday = None
        self.current_psalter_week = None
        self.adv_start = None
        self.adv_end = None
        self.xms_start = None
        self.xms_end = None
        self.ot1_start = None
        self.ot1_end = None
        self.ot2_start = None
        self.ot2_end = None
        self.len_start = None
        self.len_end = None
        self.palm_sunday = None
        self.fig_monday = None
        self.spy_wednesday = None
        self.maundy_thursday = None
        self.good_friday = None
        self.holy_saturday = None
        self.eas_start = None
        self.eas_end = None

        self.gen_cal()

    def __str__(self):
        return (
            f"Szukana data:\t\t{self.lg_day}\n"
            f"Rok Liturgiczny:\t{self.year} - {self.year + 1}\n"
            f"Okres liturgiczny: \t{self.season}\n"
            f"Cykl czytań:\t\t{self.dominical_cycle} [{self.weekday_cycle}]\n"
            f"Bieżąca niedziela:\t{self.actual_sunday}\n"
            f"Tydzień psałterza:\t{self.current_psalter_week}\n"
            f"ADV:\t\t\t\t{self.adv_start} - {self.adv_end}\n"
            f"XMS:\t\t\t\t{self.xms_start} - {self.xms_end}\n"
            f"ORD1:\t\t\t\t{self.ot1_start} - {self.ot1_end}\n"
            f"LEN:\t\t\t\t{self.len_start} - {self.len_end}\n"
            f"HOLY WEEK:\t\t\t{self.palm_sunday} - {self.holy_saturday}\n"
            f"EAS:\t\t\t\t{self.eas_start} - {self.eas_end}\n"
            f"ORD2:\t\t\t\t{self.ot2_start} - {self.ot2_end}"
        )

    def gen_cal(self):
        self.year = self.find_proper_scope()
        self.dominical_cycle, self.weekday_cycle = self.liturgical_cycle()
        self.advent_season()
        self.xmass_season()
        self.lent_season()
        self.easter_season()
        self.ordinary_season()
        self.ordinary_season_alter()
        self.get_liturgical_season()
        self.find_proper_week()
        self.psalter_weeks()

    def find_proper_scope(self) -> int:
        """
        Finds the year in which the new liturgical year starts.

        ...

        The function determines which liturgical year the `date` falls into
        by checking the Advent periods of the current year, and the next year.


        Returns:
            int: The year in which the new liturgical year (Advent) starts,
            which includes the `date`.
        """
        try:
            # Check the Advent period in the previous, current, and next year
            for s_year in range(self.lg_day.year - 1, self.lg_day.year + 2):
                advent = self.advent_start_date(s_year)
                next_advent = self.advent_start_date(s_year + 1)
                if advent <= self.lg_day < next_advent:
                    return s_year

        except Exception as e:
            raise Exception(e)

    @staticmethod
    def advent_start_date(y):
        """
        Searches for the first Sunday of Advent.

        Parameters:
            y (int): a searched year.

        Returns:
            datetime.date: The date of the first Sunday of the Advent season.
        """

        # Get the date for Christmas of the given year
        xmas_day = datetime.datetime.strptime(f'25-12-{y}',
                                              '%d-%m-%Y')

        # Find the last Sunday before or on Christmas
        if xmas_day.weekday() == 6:
            # If Christmas is a Sunday, the last Sunday is December 18th
            last_sunday = datetime.datetime.strptime(f'18-12-{y}',
                                                     '%d-%m-%Y')
        else:
            # Otherwise, find the previous Sunday before Christmas
            shift = 24 - xmas_day.weekday()
            last_sunday = datetime.datetime.strptime(
                f'{shift}-12-{y}', '%d-%m-%Y')

        # Advent starts 4 Sundays before Christmas (3 Sundays = 21 days)
        advent_start = last_sunday - datetime.timedelta(days=21)

        return advent_start.date()

    def liturgical_cycle(self):
        """
        Determines the liturgical cycle for the given year.

        The known liturgical cycle (epoch) is based on the year 2020, where:
            - The dominical cycle was "A".
            - The weekday cycle was "II".

        Returns:
            tuple: A tuple containing:
                - dominical_cycle (str): One of "A", "B", or "C".
                - weekday_cycle (str): "I" for even years or "II" for odd years.
        """

        # Calculate dominical cycle (A, B, C)
        dominical_cycle = {0: "B", 1: "C", 2: "A"}[(self.year - 2020) % 3]

        # Calculate weekday cycle (I, II)
        weekday_cycle = "I" if self.year % 2 == 0 else "II"

        return dominical_cycle, weekday_cycle

    def get_liturgical_season(self):
        """
        Determines the liturgical season for a given date

        Returns:
            str: The name of the liturgical season ('Advent', 'Christmas',
            'Ordinary', 'Lent', 'Easter').
        """

        # Map seasons to their corresponding functions
        seasons = {
            'adv': lambda: self.advent_season(),
            'xms': lambda: self.xmass_season(),
            'ot1': lambda: self.ordinary_season(),
            'ot2': lambda: self.ordinary_season_alter(),
            'len': lambda: self.lent_season(),
            'eas': lambda: self.easter_season(),
        }

        # Check which season the date belongs to
        for season, check_func in seasons.items():
            if check_func():
                self.season = season
                break

    def advent_season(self) -> bool:
        try:
            self.adv_start = self.advent_start_date(self.year)
            self.adv_end = datetime.datetime.strptime(f'24.12.{self.year}',
                                                      '%d.%m.%Y').date()
            query = self.adv_start <= self.lg_day <= self.adv_end
            if query:
                return query

        except Exception as e:
            print(e)

    def xmass_season(self) -> bool:
        try:
            self.xms_start = datetime.datetime.strptime(f'25.12.{self.year}',
                                                        '%d.%m.%Y').date()
            self.xms_end = self.baptism_sunday()
            query = self.xms_start <= self.lg_day <= self.xms_end
            if query:
                return query
        except Exception as e:
            print(e)

    def ordinary_season(self) -> bool:
        try:
            self.ot1_start = self.baptism_sunday() + datetime.timedelta(1)
            self.ot1_end = self.len_start - datetime.timedelta(1)
            query = self.ot1_start <= self.lg_day < self.ot1_end
            if query:
                return query
        except Exception as e:
            print(e)

    def lent_season(self) -> bool:
        try:
            self.len_start, self.eas_start, self.eas_end = self.easter_time()
            self.len_end = self.eas_start - datetime.timedelta(7)
            self.palm_sunday = self.eas_start - datetime.timedelta(6)
            self.fig_monday = self.eas_start - datetime.timedelta(5)
            self.spy_wednesday = self.eas_start - datetime.timedelta(4)
            self.maundy_thursday = self.eas_start - datetime.timedelta(3)
            self.good_friday = self.eas_start - datetime.timedelta(2)
            self.holy_saturday = self.eas_start - datetime.timedelta(1)
            query = self.len_start <= self.lg_day < self.eas_start
            if query:
                return query
        except Exception as e:
            print(e)

    def easter_season(self) -> bool:
        try:
            query = self.eas_start <= self.lg_day < self.eas_end
            if query:
                return query
        except Exception as e:
            print(e)

    def ordinary_season_alter(self) -> bool:
        try:
            self.ot2_start = self.eas_end + datetime.timedelta(1)
            self.ot2_end = (self.advent_start_date(self.year + 1) -
                            datetime.timedelta(1))
            query = self.ot2_start <= self.lg_day < self.ot2_end
            if query:
                return query
        except Exception as e:
            print(e)

    def is_epiphany_in_first_week(self):
        """
        Determines if Epiphany is celebrated in the first week of the year.

        If the first day of the year is a Monday (0) or Tuesday (1),
        the Epiphany (January 6th) will be celebrated in the first week of the year.

        Parameters:
        year (int): The queried year.

        Returns:
        bool: True if Epiphany (January 6th) falls in the first week of the year.
        """
        try:
            # Get the weekday of January 1st (0=Monday, 1=Tuesday, ..., 6=Sunday)
            first_day_no = datetime.datetime.strptime(
                f'01-01-{self.year}', '%d-%m-%Y').weekday()

            # If the first day of the year is Monday (0) or Tuesday (1), return True
            return first_day_no in [0, 1]
        except Exception as e:
            print(e)

    def baptism_sunday(self):
        """
        Finds the date of Baptism of the Lord, which is typically the Sunday after
        January 6th.

        Returns:
            datetime.date: The date of Baptism of the Lord.
        """
        try:
            # Date for January 6th (Epiphany)
            epiphany_date = datetime.datetime.strptime(f'06-01-{self.year + 1}',
                                                       '%d-%m-%Y')

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
        except Exception as e:
            print(e)

    def easter_time(self):
        """
        Computes the dates for Ash Wednesday, Easter, and Pentecost.

        Returns:
            tuple: A tuple containing the dates of Ash Wednesday, Easter, and
            Pentecost.
        """
        try:
            # Compute the date of Easter using the Gaussian method
            easter = gausianmethod.computus(self.year + 1)

            # Calculate the date of Ash Wednesday (46 days before Easter)
            lent_duration = datetime.timedelta(days=46)
            ash_wednesday = easter - lent_duration

            # Calculate the date of Pentecost (49 days after Easter)
            eastertide = datetime.timedelta(days=49)
            pentecost = easter + eastertide

            return ash_wednesday, easter, pentecost
        except Exception as e:
            print(e)

    def find_proper_week(self) -> int:
        """
        Finds the index of the week (1 to 4)

        ...

        Returns:
            int: The index of the corresponding week (1-4),
            or raises an exception if the date is invalid.

        Raises:
            ValueError: If the given dates are invalid or if `c_day` is not within
            the range `[initium, finis]`.
            IndexError: If the calculated weeks do not fit within the expected
            range.
        """
        initium = getattr(self, f"{self.season}_start")
        finis = getattr(self, f"{self.season}_end")

        try:
            if finis < initium:
                raise ValueError(f'The end date is earlier than initial date.')
            if (finis - initium).days > 207:
                raise ValueError(
                    f'The span {initium} - {finis} cannot exceed 193 days.')
            if initium == finis == c_day:
                raise ValueError(
                    f'The dates {initium}, {finis}, and {c_day} are all the '
                    f'same.')
            if self.lg_day < initium or self.lg_day > finis:
                raise ValueError(
                    f'The date {self.lg_day} is not within the range '
                    f'{initium}-{finis}.')

            # if season is ot2, needs joining
            if self.season == "ot2":
                self.sundays_in_scope(self.ot1_end, self.ot1_start)
                self.sundays_in_scope(finis, initium, True)
            else:
                self.sundays_in_scope(finis, initium)

            if self.season == "xms":
                return 1
            elif self.season == "len":
                # form Ash W. to Sat. 4th week of psalter
                if self.check_ashes_week():
                    self.actual_sunday = "Tydzień po Popielcu"
                    return 4
                else:
                    # Find the Sunday that corresponds to `lg_day`
                    self.actual_sunday = self.first_day_of_week()
                    # Find the index of the proper week
                    for index in range(4):
                        if self.actual_sunday in self.sunday_dates[index::4]:
                            return index + 1
            else:
                # Find the Sunday that corresponds to `lg_day`
                self.actual_sunday = self.first_day_of_week()
                # Find the index of the proper week
                for index in range(4):
                    if self.actual_sunday in self.sunday_dates[index::4]:
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

    def check_ashes_week(self):
        return self.len_start <= self.lg_day <= self.len_start + datetime.timedelta(
            3)

    def psalter_weeks(self):
        sun_dict = {"1": [], "2": [], "3": [], "4": []}
        # 4 week psalter
        for i in range(1, 5):
            for sun in self.sunday_dates[i - 1::4]:
                sun_dict[str(i)].append(sun)

        if self.season == "xms":
            self.current_psalter_week = 1
        else:
            for key, value in sun_dict.items():
                for sunday in value:
                    if self.season == "len":
                        if self.check_ashes_week():
                            self.current_psalter_week = 4
                        elif self.first_day_of_week() == sunday:
                            self.current_psalter_week = int(key)
                    elif self.first_day_of_week() == sunday:
                        self.current_psalter_week = int(key)

    def sundays_in_scope(self, finis: datetime.date, initium: datetime.date,
                         ot_season=False) -> int:
        """
        Creates a list of all Sundays within a given date range.

        Parameters:
            finis (date): End date of the range.
            initium (date): Start date of the range.
            ot_season (bool): extra recursion for an Ordinary season

        Returns:
            int: number of weeks in scope
        """
        # If the scope is 2nd part of OT, -13 week numbers for Lent and
        # Eastertide
        ot_mod = 13 if ot_season else 0
        scope = finis - initium
        number_of_weeks = []
        # Find all Sundays within the date range
        for i in range(scope.days + 1):
            q_day = initium + datetime.timedelta(i)
            # If queried day is a Sunday, append it to the list
            if q_day.weekday() == 6:  # Sunday has weekday number 6
                if q_day not in self.sunday_dates:
                    self.sunday_dates.append(q_day)
                if q_day.isocalendar()[
                    1] - ot_mod not in self.sunday_weeknumbers:
                    self.sunday_weeknumbers.append(
                        q_day.isocalendar()[1] - ot_mod)
                number_of_weeks.append(q_day)

        return len(number_of_weeks)

    def first_day_of_week(self):
        """
        Finds the Sunday that corresponds to the given day.

        Returns:
            datetime.date: The Sunday that corresponds to the given day.

        Raises:
            ValueError: If no valid Sunday is found for the given day.
        """
        try:
            if self.season in ["ot1", "ot2"]:
                bapism = self.sunday_dates[0] - datetime.timedelta(7)
                no_of_weeks = self.sundays_in_scope(self.ot1_end,
                                                    self.ot1_start)
                pentecost = self.eas_end
                if bapism not in self.sunday_dates:
                    self.sunday_dates.insert(0, self.sunday_dates[
                        0] - datetime.timedelta(7))
                if pentecost not in self.sunday_dates:
                    self.sunday_dates.insert(no_of_weeks + 1, self.eas_end)

            for sunday in self.sunday_dates:
                # Calculate the difference in days
                difference = (self.lg_day - sunday).days
                # If the difference is within the current week (0 to 6),
                # return the Sunday
                if 0 <= difference < 7:
                    return sunday

            # If no valid Sunday is found, raise ValueError
            raise ValueError(
                f"No valid Sunday found for the date {self.lg_day}")

        except ValueError as e:
            print(f"Error: {e}")
            raise  # Re-raise the ValueError to propagate the error
