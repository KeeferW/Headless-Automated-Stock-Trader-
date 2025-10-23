import time
from datetime import datetime, timedelta, timezone
from . import config

def wait_until(ts_utc: datetime):
    while True:
        now = datetime.now(timezone.utc)
        if now >= ts_utc:
            break
        time.sleep(min(60, max(1, (ts_utc - now).total_seconds())))

def top_of_next_hour_utc() -> datetime:
    now = datetime.now(timezone.utc)
    return (now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1))

def today_at_855am_et() -> datetime:
    now_et = datetime.now(config.ET)
    target_et = now_et.replace(hour=8, minute=55, second=0, microsecond=0)
    return target_et.astimezone(timezone.utc)

def next_855am_et_after(now_utc: datetime) -> datetime:
    candidate = today_at_855am_et()
    if candidate <= now_utc:
        tomorrow_et = (datetime.now(config.ET) + timedelta(days=1)).replace(hour=8, minute=55, second=0, microsecond=0)
        candidate = tomorrow_et.astimezone(timezone.utc)
    return candidate

def is_weekday_et(d: datetime) -> bool:
    return d.astimezone(config.ET).weekday() < 5
