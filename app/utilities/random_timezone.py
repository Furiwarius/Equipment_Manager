from random import choice
import zoneinfo


def get_random_timezone():
    '''
    Генерация случайной таймзоны
    '''
    all_timezones = list(zoneinfo.available_timezones())
    random_timezone_key = choice(all_timezones)

    return zoneinfo.ZoneInfo(key=random_timezone_key)