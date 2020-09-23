from datetime import datetime
from math import floor


YEAR_HOURS = 365 * 24

def get_imperial_date(datetime):
    date = datetime.date()
    year_start = date.replace(month=1, day=1)
    year_part = date.year % 1000
    timedelta = date - year_start
    hours = 24 * timedelta.days + datetime.hour + datetime.minute / 60
    year_frac = floor(1000 * hours / YEAR_HOURS)
    millenium = floor(date.year / 1000)
    return "{} {:03d} {:03d}M{}".format(
        0, year_frac, year_part, millenium)


def get_imperial_date_now():
    return get_imperial_date(datetime.now())

if __name__ == "__main__":
    print(get_imperial_date_now())
