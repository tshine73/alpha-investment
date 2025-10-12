from datetime import datetime


def format_date(d: datetime, format='%Y-%m-%d %H:%M:%S'):
    return d.strftime(format)


def get_weekday_name(day_of_week):
    weekday_name_dict = {
        0: "Monday",
        1: "Tuesday",
        2: "Wednesday",
        3: "Thursday",
        4: "Friday",
        5: "Saturday",
        6: "Sunday"
    }

    return weekday_name_dict[day_of_week]
