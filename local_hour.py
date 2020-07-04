from datetime import datetime, timezone, timedelta


def get_local_day_datetimes():
    bogota_timezone = timezone(timedelta(hours=-5), "Bogota")
    current_time_local = datetime.now(timezone.utc).astimezone(tz=bogota_timezone)
    day_start_local = datetime(current_time_local.year, current_time_local.month, current_time_local.day, tzinfo=bogota_timezone)
    day_start_utc = day_start_local.astimezone(tz=timezone.utc)
    day_end_utc = day_start_utc + timedelta(days=1)
    return day_start_utc, day_end_utc

def get_local_day_timestamps():
    day_start_utc, day_end_utc = get_local_day_datetimes()
    day_start_timestamp = int(day_start_utc.timestamp())
    day_end_timestamp = int(day_end_utc.timestamp())
    return day_start_timestamp, day_end_timestamp

def get_local_day_dates():
    day_start_utc, day_end_utc = get_local_day_datetimes()
    return day_start_utc.date(), day_end_utc.date()
