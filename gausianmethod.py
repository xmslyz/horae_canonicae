# amDg
import datetime


def computus(year: int, A: int = 24, B: int = 5):
    """
    Calculating date of Easter for known year using gausian method.

    Parameters:
        year (int): known year
        A (int): first parameter
        B (int): second parameter

    Returns:
        (datetime) date of Easter
    """
    pointday = datetime.datetime.strptime(f'22-03-{year}', '%d-%m-%Y')
    a: int = year % 19
    b: int = year % 4
    c: int = year % 7

    d: int = ((a * 19) + A) % 30
    e: int = ((2 * b) + (4 * c) + (6 * d) + B) % 7

    swift = datetime.timedelta(d + e)

    return (pointday + swift).date()
