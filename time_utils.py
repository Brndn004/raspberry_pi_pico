"""Time-related activities that require network connection."""

import collections
import ntptime
import time
import urequests


GMT_SAN_FRANCISCO_OFFSET_HOURS = -8


CurrentTime = collections.namedtuple("CurrentTime", "hour minute second")


def time_this_func(func, *args, **kwargs):
    """Print the duration that a function took to execute."""
    start = time.ticks_us()
    func(*args, **kwargs)
    end = time.ticks_us()
    print(f"Function took {(end - start) * 1e-6} seconds to execute.")


def get_time() -> CurrentTime:
    """Get a tuple representing the current time in GMT-8.

    Returns:
        Local time as: (year, month, mday, hour, minute, second, weekday, yearday)
        The format of the entries in the 8-tuple are:
            year includes the century (for example 2014).
            month is 1-12
            mday is 1-31
            hour is 0-23
            minute is 0-59
            second is 0-59
            weekday is 0-6 for Mon-Sun
            yearday is 1-366
    """
    time_tuple = time.localtime()
    curr_time = CurrentTime(
            (time_tuple[3] + GMT_SAN_FRANCISCO_OFFSET_HOURS) % 24,
            time_tuple[4],
            time_tuple[5],
        )
    return curr_time


def time_matches_now(hour: int, minute: int) -> bool:
    """Check if the passed-in time matches the current time."""
    curr_time = get_time()
    if curr_time.hour == hour and curr_time.minute == minute:
        return True
    return False


def minutes_are_odd() -> bool:
    """Return True if the current minutes are an odd number."""
    return get_time().minute % 2 == 1


def set_time_via_internet() -> bool:
    try:
        ntptime.settime()
        print(f"Current time is: {time.localtime()}")
        print(f"Current time is: {get_time()}")
        return True
    except Exception:
        print("Could not set time successfully.")
        return False


def print_time_from_internet() -> None:
    """Query the internet for the current time and print it.

    If an exception occurs, print it and continue.
    """
    try:
        print("\n\n2. Querying the current GMT+0 time:")
        resp = urequests.get("http://date.jsontest.com") # Server that returns GMT+0 time.
        print(resp.json())
        resp.close()
    except OSError as err:
        print(err)
