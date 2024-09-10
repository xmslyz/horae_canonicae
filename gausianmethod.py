# amDg
import datetime


def computus(year: int):
    """
    Calculating date of Easter for known year using gausian method.

    ...

                                   Exceptions
      YEAR      A   B       I type           II type

    33–1582	    15	6	      -	                -
    1583–1699	22	2	      -	                -
    1700–1799	23	3	      -	                -
    1800–1899	23	4	      -	                -
    1900–2099	24	5	  1981, 2076    	1954, 2049

    Parameters:
        year (int): known year

    Returns:
        (datetime) date of Easter
    """
    # Assign A and B values based on the year

    if 33 <= year <= 1582:
        A, B = 15, 6
    elif 1583 <= year <= 1699:
        A, B = 22, 2
    elif 1700 <= year <= 1799:
        A, B = 23, 3
    elif 1800 <= year <= 1899:
        A, B = 23, 4
    elif 1900 <= year <= 2099:
        A, B = 24, 5
    elif 2100 <= year <= 2199:
        A, B = 24, 6
    elif 2200 <= year <= 2299:
        A, B = 25, 0
    elif 2300 <= year <= 2399:
        A, B = 26, 1
    elif 2400 <= year <= 2499:
        A, B = 25, 1
    elif 2500 <= year <= 2599:
        A, B = 26, 2
    elif 2600 <= year <= 2699:
        A, B = 27, 3
    elif 2700 <= year <= 2899:
        A, B = 27, 4
    elif 2900 <= year <= 2999:
        A, B = 28, 5
    else:
        raise ValueError(f"Year {year} is out of range for Easter computation.")

    pointday = datetime.datetime.strptime(f'22-03-{str(year).zfill(4)}',
                                          '%d-%m-%Y')

    a: int = year % 19
    b: int = year % 4
    c: int = year % 7

    d: int = ((a * 19) + A) % 30
    e: int = ((2 * b) + (4 * c) + (6 * d) + B) % 7

    if year in [1609, 1981, 1954, 2049, 2076, 2106, 2133, 2201, 2296, 2448,
                2668, 2725, 2820]:
        swift = datetime.timedelta(d + e - 7)
    else:
        swift = datetime.timedelta(d + e)

    return (pointday + swift).date()
