from enum import Enum


class eReturnValue(Enum):
    UNSUPPORTED = 0
    NOT_SPECIFIED_NAME = -1
    EXIST_ALREADY = -2
    API_NOT_RECOGNIZE = -3
    INTERNAL_SERVER_ERROR = -4
    NOT_EXIST = -5