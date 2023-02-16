import datetime
import time


def create_timestamp() -> float:
    dt = datetime.datetime.now()
    return time.mktime(dt.timetuple())
