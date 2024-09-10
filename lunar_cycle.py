# amDg

import datetime
import math

# Reference date for a known new moon (Jan 6, 2000 is a common reference)
new_moon_date = datetime.datetime(2000, 1, 6)

# A lunar cycle (synodic month) in days
lunar_cycle = 29.53058867


def get_moon_phase(date):
    """Calculates the moon phase for a given date.

    Parameters:
    date (datetime): The date for which to calculate the moon phase.

    Returns:
    int: A description of the moon phase (0 New Moon, 1 Waxing,
    2 Full Moon, 3 Wanning)
    """

    # Difference between the given date and the reference new moon
    diff = date - new_moon_date
    days_since_new_moon = diff.days + (diff.seconds / 86400)  # 86400s. = 1 day

    # Calculate the phase as a fraction of the lunar cycle
    moon_phase = days_since_new_moon % lunar_cycle

    # Determine the phase
    if moon_phase < 1:
        return 0  # "New Moon"
    elif moon_phase < 7.4:
        return 1  # "First Quarter Waxing"
    elif moon_phase < 14.8:
        return 2  # "Full Moon"
    elif moon_phase < 22.1:
        return 3  # "Last Quarter Waning"
    else:
        return 4  # "New Moon approaching"


if __name__ == "__main__":
    today = datetime.datetime.now()
    phase = get_moon_phase(today)
    print(f"Today's moon phase: {phase}")
