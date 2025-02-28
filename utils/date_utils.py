from datetime import datetime


def format_date(d: datetime, format='%Y-%m-%d %H:%M:%S'):
    return d.strftime(format)
