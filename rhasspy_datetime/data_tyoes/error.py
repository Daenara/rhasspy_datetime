import logging
from enum import Enum

log = logging.getLogger(__name__)


class ErrorCode(Enum):
    NO_NETWORK_ERROR = "no_network_error"
    NOT_IMPLEMENTED_ERROR = "not_implemented_error"
    DATE_ERROR = "date_error"
    CONFIG_ERROR = "config_error"
    TIME_ERROR = "time_error"
    GENERAL_ERROR = "general_error"


class Error(Exception):
    pass


class ConfigError(Error):
    def __init__(self, message: str, description: str = ""):
        self.error_code = ErrorCode.CONFIG_ERROR
        self.message = message
        self.description = description
