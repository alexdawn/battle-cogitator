from datetime import datetime
from math import floor, ceil


YEAR_HOURS = 365 * 24


def get_imperial_date(datetime: datetime) -> str:
    """Get imperial date from python datetime"""
    date = datetime.date()
    year_start = date.replace(month=1, day=1)
    year_part = date.year % 1000
    timedelta = date - year_start
    hours = 24 * timedelta.days + datetime.hour + datetime.minute / 60
    year_frac = floor(1000 * hours / YEAR_HOURS)
    millenium = ceil(date.year / 1000)
    return "{} {:03d} {:03d}.M{}".format(
        0, year_frac, year_part, millenium)


def get_imperial_date_from_date(year: int, month: int, day: int) -> str:
    """Get imperial date from YYYY MM DD"""
    assert month > 0 and month <= 12, "Invalid Month"
    assert day > 0 and day <= 31, "Invalid Day"
    return get_imperial_date(datetime(year, month, day))


def get_imperial_date_now() -> str:
    """Get the imperial date for now"""
    return get_imperial_date(datetime.now())


if __name__ == "__main__":
    print("now", get_imperial_date_now())
