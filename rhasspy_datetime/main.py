import datetime
import logging
import random

import rhasspy_datetime.data_tyoes.config as cf

log = logging.getLogger(__name__)


def get_day(config_path: str = None) -> str:
    if config_path is not None and cf.config_path is not config_path:
        cf.set_config_path(config_path)

    config = cf.get_config()
    day = config.locale.weekday_names[datetime.datetime.now(config.timezone).date().weekday()]
    return random.choice(config.locale.answers["weekday"]).format(day=day)


def get_date(config_path: str = None) -> str:
    if config_path is not None and cf.config_path is not config_path:
        cf.set_config_path(config_path)

    config = cf.get_config()
    today = datetime.datetime.now(config.timezone).date()
    month = config.locale.month_names[today.month]
    date = config.locale.date_format.format(day=today.day, month=month)
    return random.choice(config.locale.answers["date"]).format(date=date)


def get_time(config_path: str = None) -> str:
    if config_path is not None and cf.config_path is not config_path:
        cf.set_config_path(config_path)

    config = cf.get_config()
    current_time = datetime.datetime.now(config.timezone).time()
    hours = current_time.hour
    minutes = current_time.minute
    time = config.locale.format_time(hours, minutes, config.exact_time, config.use_24_hour_system)
    return random.choice(config.locale.answers["time"]).format(time=time)
