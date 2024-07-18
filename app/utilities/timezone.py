from datetime import datetime
from pytz import timezone


def transfer_timezone(zone:str, utc_time: datetime) -> datetime:
    '''
    Перевод времени UTC во время переданной таймзоны
    '''
    
    return utc_time.astimezone(timezone(zone))