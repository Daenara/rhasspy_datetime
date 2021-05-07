from rhasspy_datetime.utils import round_to_x_minutes

date_format = "{day}. {month}"
weekday_names = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
month_names = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober",
               "November", "Dezember"]

answers = {
    "time": ["Es ist {time}", "{time}", "Die Uhrzeit: {time}"],
    "weekday": ["Es ist {day}", "Heute ist {day}", "{day}"],
    "date": ["Heute ist der {date}", "Es ist der {date}", "{date}"]
}


def format_time(hours, minutes, exact_time=False, use_24_hours=False):
    time_format = "{hours} Uhr {minutes}"
    hours_plus_1 = hours + 1
    if not use_24_hours:
        hours = hours % 12
        hours_plus_1 = hours_plus_1 % 12
        if hours == 0:
            hours = 12
        if hours_plus_1 == 0:
            hours_plus_1 = 12
        rounded_minutes = minutes
        if not exact_time:
            if 0 < minutes <= 5:
                time_format = "kurz nach {hours}"
            elif minutes < 30 & minutes >= 25:
                time_format = "kurz vor halb {hours_plus_1}"
            elif 25 <= minutes < 30:
                time_format = "kurz vor halb {hours_plus_1}"
            elif 30 < minutes <= 35:
                time_format = "kurz nach halb {hours_plus_1}"
            elif 55 <= minutes < 59:
                time_format = "kurz vor {hours_plus_1}"
            else:
                rounded_minutes = round_to_x_minutes(minutes, 5)
        if rounded_minutes == 0:
            minutes = rounded_minutes
            time_format = "punkt {hours}"
        elif rounded_minutes == 15:
            minutes = rounded_minutes
            time_format = "viertel nach {hours}"
        elif rounded_minutes == 30:
            minutes = rounded_minutes
            time_format = "halb {hours_plus_1}"
        elif rounded_minutes == 45:
            minutes = rounded_minutes
            time_format = "viertel vor {hours_plus_1}"
    return time_format.format(hours=hours, minutes=minutes, hours_plus_1=hours_plus_1)
